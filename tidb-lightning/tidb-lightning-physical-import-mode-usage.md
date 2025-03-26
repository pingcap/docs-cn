---
title: 使用物理导入模式
summary: 了解如何使用 TiDB Lightning 的物理导入模式。
---

# 使用物理导入模式

本文档介绍如何编写[物理导入模式](/tidb-lightning/tidb-lightning-physical-import-mode.md) 的配置文件，如何进行性能调优、使用磁盘资源配额等内容。

使用物理导入模式有一些限制，使用前请务必阅读[必要条件及限制](/tidb-lightning/tidb-lightning-physical-import-mode.md#必要条件及限制)。

## 配置及使用

可以通过以下配置文件使用物理导入模式执行数据导入：

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
# 本地源数据目录或外部存储 URI。关于外部存储 URI 详情可参考 https://docs.pingcap.com/zh/tidb/v6.6/backup-and-restore-storages#uri-%E6%A0%BC%E5%BC%8F。
data-source-dir = "/data/my_database"

[conflict]
# 从 v7.3.0 开始引入的新版冲突数据处理策略。默认值为 ""。从 v8.0.0 开始，TiDB Lightning 优化了物理导入模式和逻辑导入模式的冲突策略。
# - ""：不进行冲突数据检测和处理。如果源文件存在主键或唯一键冲突的记录，后续步骤会报错
# - "error"：检测到导入的数据存在主键或唯一键冲突的数据时，终止导入并报错
# - "replace"：遇到主键或唯一键冲突的数据时，保留最新的数据，覆盖旧的数据。
#              冲突数据将被记录到目标 TiDB 集群中的 `lightning_task_info.conflict_view` 视图中。
#              在 `lightning_task_info.conflict_view` 视图中，如果某行的 `is_precheck_conflict` 字段为 `0`，表示该行记录的冲突数据是通过后置冲突检测发现的；如果某行的 `is_precheck_conflict` 字段为 `1`，表示该行记录的冲突数据是通过前置冲突检测发现的。
#              你可以根据业务需求选择正确的记录重新手动写入到目标表中。注意，该方法要求目标 TiKV 的版本为 v5.2.0 或更新版本。
strategy = ""
# 控制是否开启前置冲突检测，即导入数据到 TiDB 前，先检查所需导入的数据是否存在冲突。该参数默认值为 false，表示仅开启后置冲突检测。取值为 true 时，表示同时开启前置冲突检测和后置冲突检测。冲突记录数量高于 1,000,000 的场景建议配置 `precheck-conflict-before-import = true`，可以提升冲突检测的性能，反之建议关闭。
# precheck-conflict-before-import = false
# threshold = 10000
# 从 v8.1.0 开始，TiDB Lightning 会自动将 `max-record-rows` 的值设置为 `threshold` 的值，并忽略用户输入，因此无需再单独配置 `max-record-rows`。`max-record-rows` 将在未来版本中废弃。
# max-record-rows = 10000

[tikv-importer]
# 导入模式配置，设为 local 即使用物理导入模式
backend = "local"

# 冲突数据处理方式
# `duplicate-resolution` 参数从 v8.0.0 开始已被废弃，并将在未来版本中被移除。详情参考 <https://docs.pingcap.com/zh/tidb/stable/tidb-lightning-physical-import-mode-usage#旧版冲突检测从-v800-开始已被废弃>。
# 如果 `duplicate-resolution` 设置为 'none' 且 `conflict.strategy` 未设置，TiDB Lightning 会自动将 `conflict.strategy` 赋值为 ""。
# 如果 `duplicate-resolution` 设置为 'remove' 且 `conflict.strategy` 未设置，TiDB Lightning 会自动将 `conflict.strategy` 赋值为 "replace" 开启新版冲突检测。
duplicate-resolution = 'none'

# 本地进行 KV 排序的路径。
sorted-kv-dir = "./some-dir"

# 限制 TiDB Lightning 向每个 TiKV 节点写入的带宽大小，默认为 0，表示不限制。
# store-write-bwlimit = "128MiB"

# 物理导入模式是否通过 SQL 方式添加索引。默认为 `false`，表示 TiDB Lightning 会将行数据以及索引数据都编码成 KV pairs 后一同导入 TiKV，实现机制和历史版本保持一致。如果设置为 `true`，即 TiDB Lightning 会导完数据后，再使用 add index 的 SQL 来添加索引。
# 通过 SQL 方式添加索引的优点是将导入数据与导入索引分开，可以快速导入数据，即使导入数据后，索引添加失败，也不会影响数据的一致性。
# add-index-by-sql = false

[tidb]
# 目标集群的信息。tidb-server 的地址，填一个即可。
host = "172.16.31.1"
port = 4000
user = "root"
# 设置连接 TiDB 的密码，可为明文或 Base64 编码。
password = ""
# 必须配置。表结构信息从 TiDB 的“status-port”获取。
status-port = 10080
# 必须配置。pd-server 的地址。从 v7.6.0 开始支持设置多个地址。
pd-addr = "172.16.31.4:2379,56.78.90.12:3456"
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

冲突数据是指两条或两条以上记录中存在主键或唯一键列数据重复。当数据源中的记录存在冲突数据，如果没有启用冲突数据检测功能，将导致该表的实际总行数与使用唯一索引查询的总行数不一致。

冲突数据检测采用新版冲突检测 (`conflict`) 模式。旧版冲突检测 (`tikv-importer.duplicate-resolution`) 模式从 v8.0.0 开始已被废弃。`tikv-importer.duplicate-resolution` 参数将在未来版本中被移除。

### 新版冲突检测

具体配置及含义如下：

| 配置 | 冲突时默认行为                                        | 类比 SQL 语句 |
|:---|:-----------------------------------------------|:---|
| `"replace"` | 保留最新的数据，覆盖旧的数据 | `REPLACE INTO ...` |
| `"error"` | 终止导入并报错                                        | `INSERT INTO ...` |
| `""` | 不进行冲突检查和处理，但如果存在有主键和唯一键冲突的数据，会在后续步骤 checksum 时报错          | 无 |

> **注意：**
>
> 由于 TiDB Lightning 内部并发处理以及实现限制，物理导入模式下的冲突检测效果不会与 SQL 语句完全一致。

配置为 `"error"` 时，遇到冲突数据时，TiDB Lightning 会报错并退出。配置为 `"replace"` 时，冲突数据被视作[冲突错误 (Conflict error)](/tidb-lightning/tidb-lightning-error-resolution.md#冲突错误-conflict-error)。配置了大于 `0` 的 [`conflict.threshold`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-任务配置) 后，TiDB Lightning 可以容忍一定数目的冲突错误，默认值为 `9223372036854775807`，意味着几乎能容忍全部错误。详见[可容忍错误](/tidb-lightning/tidb-lightning-error-resolution.md)功能介绍。

新版冲突检测具有如下的限制：

- 在导入之前，前置冲突检测会先读取全部数据并编码，以检测潜在的冲突数据。检测过程中会使用 `tikv-importer.sorted-kv-dir` 存储临时文件。检测完成后，会保留检查结果至导入阶段以供读取。因此，这将带来额外的耗时、磁盘空间占用以及数据读取 API 请求开销。
- 新版冲突检测只能在单节点完成，不适用于并行导入以及开启了 `disk-quota` 参数的场景。

新版冲突检测通过 `precheck-conflict-before-import` 配置项控制是否开启前置冲突检测。在原数据冲突数据较多的情况下，前置和后置冲突检测的总耗时相比旧版更少。因此，建议在已知数据的冲突数据比例大于或等于 1%、且本地磁盘空间充足的单节点导入任务中开启前置冲突检测。

### 旧版冲突检测（从 v8.0.0 开始已被废弃）

从 v8.0.0 起，旧版冲突检测 (`tikv-importer.duplicate-resolution`) 已被废弃。`tikv-importer.duplicate-resolution` 参数将在未来版本中被移除。如果 `tikv-importer.duplicate-resolution` 为 `remove` 且 `conflict.strategy` 未设置，TiDB Lightning 会自动将 `conflict.strategy` 赋值为 `"replace"` 开启新版冲突检测。需要注意 `tikv-importer.duplicate-resolution` 不能与 `conflict.strategy` 同时配置，否则将报错。

- 在 v7.3.0 到 v7.6.0 之间的版本中，当配置 `tikv-importer.duplicate-resolution` 不为空时，TiDB Lightning 会开启旧版冲突检测。
- 在 v7.2.0 及之前的版本中，TiDB Lightning 仅支持旧版冲突检测。

旧版冲突数据检测支持两种策略：

- `remove`：推荐方式。记录并删除所有的冲突记录，以确保目的 TiDB 中的数据状态保持一致。
- `none`：关闭冲突数据检测。该模式是两种模式中性能最佳的，但是可能会导致目的 TiDB 中出现数据不一致的情况。

在 v5.3 之前，TiDB Lightning 不具备冲突数据检测特性，若存在冲突数据将导致导入过程最后的 Checksum 环节失败。开启冲突检测特性的情况下，只要检测到冲突数据，TiDB Lightning 都会跳过最后的 Checksum 环节（因为必定失败）。

假设一张表 `order_line` 的表结构如下：

```sql
CREATE TABLE IF NOT EXISTS `order_line` (
  `ol_o_id` int NOT NULL,
  `ol_d_id` int NOT NULL,
  `ol_w_id` int NOT NULL,
  `ol_number` int NOT NULL,
  `ol_i_id` int NOT NULL,
  `ol_supply_w_id` int DEFAULT NULL,
  `ol_delivery_d` datetime DEFAULT NULL,
  `ol_quantity` int DEFAULT NULL,
  `ol_amount` decimal(6,2) DEFAULT NULL,
  `ol_dist_info` char(24) DEFAULT NULL,
  PRIMARY KEY (`ol_w_id`,`ol_d_id`,`ol_o_id`,`ol_number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
```

若在导入过程中检测到冲突数据，则可以查询 `lightning_task_info.conflict_error_v3` 表得到以下内容：

```sql
mysql> select table_name,index_name,key_data,row_data from conflict_error_v3 limit 10;
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

## 导入时暂停 PD 调度的范围

自 TiDB Lightning v6.2.0 版本起，TiDB Lightning 提供机制控制导入数据过程对在线业务的影响。TiDB Lightning 不会暂停全局的调度，而是只暂停目标表数据范围所在 region 的调度，降低了对在线业务的影响。

自 TiDB v7.1.0 版本起，你可以通过 TiDB Lightning 的参数 [`pause-pd-scheduler-scope`](/tidb-lightning/tidb-lightning-configuration.md) 来控制暂停调度的范围。默认为 `"table"`，即只暂停目标表数据所在 Region 的调度。当集群没有业务流量时，建议设置为 `"global"` 以减少来自调度器对导入的干扰。

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

测试结果表明，TPCC 并发越小，TiDB Lightning 导入对 TPCC 结果影响越大。当 TPCC 并发达到 64 或以上时，TiDB Lightning 导入对 TPCC 结果无显著影响。

因此，如果你的 TiDB 生产集群上有延迟敏感型业务，并且并发较小，**强烈建议**不要使用 TiDB Lightning 导入数据到该集群，否则会给在线业务带来较大影响。

## 性能调优

**提高 Lightning 物理导入模式导入性能最直接有效的方法：**

- **升级 Lightning 所在节点的硬件，尤其重要的是 CPU 和 sorted-key-dir 所在存储设备的性能。**
- **使用[并行导入](/tidb-lightning/tidb-lightning-distributed-import.md)特性实现水平扩展。**

当然，Lightning 也提供了部分并发相关配置以影响物理导入模式的导入性能。但是从长期实践的经验总结来看，以下四个配置项一般保持默认值即可，调整其数值并不会带来显著的性能提升，可作为了解内容阅读。

```toml
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
