---
title: 使用 Physical Import Mode
summary: 了解如何使用 TiDB Lightning 的 Physical Import Mode。
---

# 使用 Physical Import Mode

本文档介绍如何编写 Physical Import Mode 的配置文件，如何进行性能调优、使用磁盘资源配额等内容。

## 配置及使用

可以通过以下配置文件使用 Physical Import Mode 执行数据导入：

```toml
[lightning]
# 日志
level = "info"
file = "tidb-lightning.log"
max-size = 128 # MB
max-days = 28
max-backups = 14

# 启动之前检查集群是否满足最低需求。
check-requirements = true

[mydumper]
# 本地源数据目录或外部存储 URL
data-source-dir = "/data/my_database"

[tikv-importer]
# 导入模式配置，设为 local 即使用 Physical Import Mode
backend = "local"

# 冲突数据处理方式
duplicate-resolution = 'remove'

# 本地进行 KV 排序的路径。
sorted-kv-dir = "./some-dir"

# 限制 TiDB Lightning 向每个 TiKV 节点写入的带宽大小，默认为 0，表示不限制。
# store-write-bwlimit = "128MiB"

[tidb]
# 目标集群的信息。tidb-server 的地址，填一个即可。
host = "172.16.31.1"
port = 4000
user = "root"
# 设置连接 TiDB 的密码，可为明文或 Base64 编码。
password = ""
# 必须配置。表结构信息从 TiDB 的“status-port”获取。
status-port = 10080
# 必须配置。pd-server 的地址，填一个即可。
pd-addr = "172.16.31.4:2379"
# tidb-lightning 引用了 TiDB 库，并生成产生一些日志。
# 设置 TiDB 库的日志等级。
log-level = "error"

[post-restore]
# 配置是否在导入完成后对每一个表执行 `ADMIN CHECKSUM TABLE <table>` 操作来验证数据的完整性。
# 可选的配置项：
# - "required"（默认）。在导入完成后执行 CHECKSUM 检查，如果 CHECKSUM 检查失败，则会报错退出。
# - "optional"。在导入完成后执行 CHECKSUM 检查，如果报错，会输出一条 WARN 日志并忽略错误。
# - "off"。导入结束后不执行 CHECKSUM 检查。
# 默认值为 "required"。从 v4.0.8 开始，checksum 的默认值由此前的 "true" 改为 "required"。
#
# 注意：
# 1. Checksum 对比失败通常表示导入异常（数据丢失或数据不一致），因此建议总是开启 Checksum。
# 2. 考虑到与旧版本的兼容性，依然可以在本配置项设置 `true` 和 `false` 两个布尔值，其效果与 `required` 和 `off` 相同。
checksum = "required"
# 配置是否在 CHECKSUM 结束后对所有表逐个执行 `ANALYZE TABLE <table>` 操作。
# 此配置的可选配置项与 `checksum` 相同，但默认值为 "optional"。
analyze = "optional"
```

Lightning 的完整配置文件可参考[完整配置及命令行参数](/tidb-lightning/tidb-lightning-configuration.md)。

## 冲突数据检测

冲突数据，即两条或两条以上的记录存在 PK/UK 列数据重复的情况。当数据源中的记录存在冲突数据，将导致该表真实总行数和使用唯一索引查询的总行数不一致的情况。冲突数据检测支持三种策略：

- record: 仅将冲突记录添加到目的 TiDB 中的 `lightning_task_info.conflict_error_v1` 表中。注意，该方法要求目的 TiKV 的版本为 v5.2.0 或更新版本。如果版本过低，则会启用 'none' 模式。
- remove: 推荐方式。记录所有的冲突记录，和 'record' 模式相似。但是会删除所有的冲突记录，以确保目的 TiDB 中的数据状态保持一致。
- none: 关闭冲突数据检测。该模式是三种模式中性能最佳的，但是可能会导致目的 TiDB 中出现数据不一致的情况。

在 v5.3 版本之前，Lightning 不具备冲突数据检测特性，若存在冲突数据将导致导入过程最后的 checksum 环节失败；开启冲突检测特性的情况下，无论 `record` 还是 `remove` 策略，只要检测到冲突数据，Lightning 都会跳过最后的 checksum 环节（因为必定失败）。

假设一张表 `order_line` 的表结构如下：

```sql
CREATE TABLE IF NOT EXISTS `order_line` (
  `ol_o_id` int(11) NOT NULL,
  `ol_d_id` int(11) NOT NULL,
  `ol_w_id` int(11) NOT NULL,
  `ol_number` int(11) NOT NULL,
  `ol_i_id` int(11) NOT NULL,
  `ol_supply_w_id` int(11) DEFAULT NULL,
  `ol_delivery_d` datetime DEFAULT NULL,
  `ol_quantity` int(11) DEFAULT NULL,
  `ol_amount` decimal(6,2) DEFAULT NULL,
  `ol_dist_info` char(24) DEFAULT NULL,
  PRIMARY KEY (`ol_w_id`,`ol_d_id`,`ol_o_id`,`ol_number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
```

若在导入过程中检测到冲突数据，则可以查询 `lightning_task_info.conflict_error_v1` 表得到以下内容：

```sql
mysql> select table_name,index_name,key_data,row_data from conflict_error_v1 limit 10;
+---------------------+------------+----------+-----------------------------------------------------------------------------+
|  table_name         | index_name | key_data | row_data                                                                    |
+---------------------+------------+----------+-----------------------------------------------------------------------------+
| `tpcc`.`order_line` | PRIMARY    | 21829216 | (2677, 10, 10, 11, 75656, 10, NULL, 5, 5831.97, "HT5DN3EVb6kWTd4L37bsbogj") |
| `tpcc`.`order_line` | PRIMARY    | 49931672 | (2677, 10, 10, 11, 75656, 10, NULL, 5, 5831.97, "HT5DN3EVb6kWTd4L37bsbogj") |
| `tpcc`.`order_line` | PRIMARY    | 21829217 | (2677, 10, 10, 12, 76007, 10, NULL, 5, 9644.36, "bHuVoRfidQ0q2rJ6ZC9Hd12E") |
| `tpcc`.`order_line` | PRIMARY    | 49931673 | (2677, 10, 10, 12, 76007, 10, NULL, 5, 9644.36, "bHuVoRfidQ0q2rJ6ZC9Hd12E") |
| `tpcc`.`order_line` | PRIMARY    | 21829218 | (2677, 10, 10, 13, 85618, 10, NULL, 5, 7427.98, "t3rsesgi9rVAKi9tf6an5Rpv") |
| `tpcc`.`order_line` | PRIMARY    | 49931674 | (2677, 10, 10, 13, 85618, 10, NULL, 5, 7427.98, "t3rsesgi9rVAKi9tf6an5Rpv") |
| `tpcc`.`order_line` | PRIMARY    | 21829219 | (2677, 10, 10, 14, 15873, 10, NULL, 5, 133.21, "z1vH0e31tQydJGhfNYNa4ScD")  |
| `tpcc`.`order_line` | PRIMARY    | 49931675 | (2677, 10, 10, 14, 15873, 10, NULL, 5, 133.21, "z1vH0e31tQydJGhfNYNa4ScD")  |
| `tpcc`.`order_line` | PRIMARY    | 21829220 | (2678, 10, 10, 1, 44644, 10, NULL, 5, 8463.76, "TWKJBt5iJA4eF7FIVxnugNmz")  |
| `tpcc`.`order_line` | PRIMARY    | 49931676 | (2678, 10, 10, 1, 44644, 10, NULL, 5, 8463.76, "TWKJBt5iJA4eF7FIVxnugNmz")  |
+---------------------+------------+----------------------------------------------------------------------------------------+
10 rows in set (0.14 sec)

```

根据上述信息人工甄别需要保留的重复数据，手动插回原表即可。

## 导入数据到生产集群

自 TiDB Lightning v6.2.0 版本起，TiDB Lightning 支持使用 Physical Import Mode 向已经投入生产的 TiDB 集群导入数据，并提供机制控制导入数据过程对在线业务的影响。

在技术实现上，TiDB Lightning 不会暂停全局的调度，而是只暂停目标表数据范围所在 region 的调度，大大降低了对在线业务的影响。

> **注意：**
>
> TiDB Lightning 不支持导入数据到已有业务写入的数据表。
>
> TiDB 集群版本需大于等于 v6.1.0，更低的版本 TiDB Lightning 会保持原有行为，暂停全局调度，数据导入期间会给在线业务带来严重影响。

TiDB Lightning 默认情况下会在最小范围内暂停集群调度，无需额外配置。但默认配置下，TiDB 集群仍然会因为数据导入太快，使在线业务的性能受到影响，所以你需要额外配置几个选项来控制导入速度和其他可能影响集群性能的因素：

```toml
[tikv-importer]
# 限制 TiDB Lightning 向每个 TiKV 节点写入的带宽大小。
store-write-bwlimit = "128MiB"

[tidb]
# 使用更小的并发以降低计算 checksum 和执行 analyze 对事务延迟的影响。
distsql-scan-concurrency = 3

[cron]
# 避免将 TiKV 切换到 import 模式。
switch-mode = '0'
```

在测试中用 TPCC 测试模拟在线业务，同时用 TiDB Lightning 向 TiDB 集群导入数据，测试导入数据对 TPCC 测试结果的影响。测试结果如下：

| 线程数 | TPM | P99 | P90 | AVG |
| ----- | --- | --- | --- | --- |
| 1     | 20%~30% | 60%~80% | 30%~50% | 30%~40% |
| 8     | 15%~25% | 70%~80% | 35%~45% | 20%~35% |
| 16    | 20%~25% | 55%~85% | 35%~40% | 20%~30% |
| 64    | 无显著影响 |
| 256   | 无显著影响 |

表格中的百分比含义为 TiDB Lightning 导入对 TPCC 结果的影响大小。对于 TPM，数值表示 TPM 下降的百分比；对于延迟 P99、P90、AVG，数值表示延迟上升的百分比。

测试结果表明，TPCC 并发越小，TiDB Lightning 导入对 TPCC 结果影响越大。当 TPCC 并发达到 64 或以上时，Lightning 导入对 TPCC 结果无显著影响。

因此，如果你的 TiDB 生产集群上有延迟敏感型业务，并且并发较小，**强烈建议**不使用 TiDB Lightning 导入数据到该集群，这会给在线业务带来较大影响。

## 性能调优

**提高 Lightning Physical Import Mode 导入性能最直接有效的方法：**

- **升级 Lightning 所在节点的硬件，尤其重要的是 CPU 和 sorted-key-dir 所在存储设备的性能。**
- **使用[并行导入](/tidb-lightning/tidb-lightning-distributed-import.md)特性实现水平扩展。**

当然，Lightning 也提供了部分并发相关配置以影响 Physical Import Mode 的导入性能。但是从长期实践的经验总结来看，以下四个配置项一般保持默认值即可，调整其数值并不会带来显著的性能提升，可作为了解内容阅读。

```
[lightning]
# 引擎文件的最大并行数。
# 每张表被切分成一个用于存储索引的“索引引擎”和若干存储行数据的“数据引擎”。
# 这两项设置控制两种引擎文件的最大并发数。
index-concurrency = 2
table-concurrency = 6

# 数据的并发数。默认与逻辑 CPU 的数量相同。
# region-concurrency =

# I/O 最大并发数。I/O 并发量太高时，会因硬盘内部缓存频繁被刷新
# 而增加 I/O 等待时间，导致缓存未命中和读取速度降低。
# 对于不同的存储介质，此参数可能需要调整以达到最佳效率。
io-concurrency = 5
```

导入时，每张表被切分成一个用于存储索引的“索引引擎”和若干存储行数据的“数据引擎”，`index-concurrency`用于调整"索引引擎"的并发度。

在调整 `index-concurrency` 时，需要注意 `index-concurrency * 每个表对应的源文件数量 > region-concurrency` 以确保 cpu 被充分利用，一般比例大概在 1.5 ~ 2 左右为优。`index-concurrency` 不应该设置的过大，但不低于 2 (默认)，过大会导致太多导入的 pipeline 变差，大量 index-engine 的 import 阶段堆积。

`table-concurrency` 同理，需要确保`table-concurrency * 每个表对应的源文件数量 > region-concurrency` 以确保 cpu 被充分利用。 推荐值为`region-concurrency * 4 / 每个表对应的源文件数量` 左右，最少设置为 4.

如果表非常大，Lightning 会按照 100 GiB 的大小将表分割成多个批次处理，并发度由 `table-concurrency` 控制。

上述两个参数对导入速度影响不大，使用默认值即可。

`io-concurrency` 用于控制文件读取并发度，默认值为 5。可以认为在某个时刻只有 5 个句柄在执行读操作。由于文件读取速度一般不会是瓶颈，所以使用默认值即可。

读取文件数据后，lightning 还需要做后续处理，例如将数据在本地进行编码和排序。此类操作的并发度由 `region-concurrency` 配置控制。`region-concurrency` 的默认值为 CPU 核数，通常无需调整，建议不要将 Lightning 与其它组件部署在同一主机，如果客观条件限制必须混合部署，则需要根据实际负载调低 `region-concurrency`。

此外，TiKV 的 [num-threads](/tikv-configuration-file.md#num-threads) 配置也可能影响性能，新集群建议设置为 CPU 核数。

## 磁盘资源配额 <span class="version-mark">从 v6.2.0 版本开始引入</span>

> **警告：**
>
> 磁盘资源配额目前是实验性功能，不建议在生产环境中使用。

TiDB Lightning 在使用物理模式导入数据时，会在本地磁盘创建大量的临时文件，用来对原始数据进行编码、排序、分割。当用户本地磁盘空间不足时，TiDB Lightning 会由于写入文件失败而报错退出。

为了减少这种情况的发生，你可以为 TiDB Lightning 配置磁盘配额 (disk quota)。当磁盘配额不足时，TiDB Lightning 会暂停读取源数据以及写入临时文件的过程，优先将已经完成排序的 key-value 写入到 TiKV，TiDB Lightning 删除本地临时文件后，再继续导入过程。

为 TiDB Lightning 开启磁盘配额，你需要在配置文件中加入配置项：

```toml
[tikv-importer]
# 默认为 MaxInt64，即 9223372036854775807 字节
disk-quota = "10GB"
backend = "local"

[cron]
# 检查磁盘配额的时间间隔，默认为 60 秒。
check-disk-quota = "30s"
```

`disk-quota` 配置项可以设置磁盘配额，默认为 MaxInt64，即 9223372036854775807 字节，这个值远远大于实际情况中可能需要的磁盘空间，相当于没开启。

`check-disk-quota` 配置项是检查磁盘配额的时间间隔，默认为 60 秒。由于检查临时文件使用空间的过程需要加锁，会使所有的导入线程都暂停，如果在每次写入之前都检查一次磁盘空间的使用情况，则会大大降低写入文件的效率（相当于单线程写入）。为了维持高效的写入，磁盘配额不会在每次写入之前检查，而是每隔一段时间暂停所有线程的写入并检查当前磁盘空间的使用情况。也就是说，当 `check-disk-quota` 配置项设置为一个非常大的值时，磁盘的使用空间有可能会大大超出磁盘配额，这样的情况下，磁盘配额功能可以说是不生效的。因此，`check-disk-quota` 的值建议不要设置太大，而具体设置多少则需要由 TiDB Lightning 具体运行的环境决定，因为不同的环境下，TiDB Lightning 写入临时文件的速度是不一样的。理论上来说，写入临时文件的速度越快，`check-disk-quota` 需要设置得越小。
