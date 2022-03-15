---
title: BR 数据恢复批量建表
summary: 了解 BR 数据恢复批量建表功能，在集群 restore 的情况下，BR 通过批量建表加速数据恢复。
---

# BR 批量建表 <span class="version-mark">从 v6.0 版本开始引入</span>

在 TiDB v6.0.0 之前，使用 BR 工具进行恢复任务时会使用的 TiDB 接口先做建库建表操作，而后进行数据恢复。在建表过程中，BR 调用 TiDB 接口，类似于 SQL 的 create table。对于恢复中大量的建表， 每个 SQL Create Table 由 TiDB ddl owner 依次串行执行。这导致表比较多的场景中，建表时间过长。为了减少恢复任务建表时间过长，从 TiDB v6.0.0 起，BR 引入了恢复批量建表功能，此功能会默认开启。BR 可以通过该功能加速建表，从而减少数据恢复的时间。

## 使用场景

该功能默认打开，在表数量较多的时候，数据恢复效果较为明显。

## 使用方法

数据恢复批量建表功能默认打开，并默认设置 `--ddl-batch-size=128` 来恢复数据，无需额外配置。该参数在 restore 阶段并发的批量创建表。如需要关闭此功能，只需要设置 `--ddl-batch-size=0`， BR 会以老的方式来串行建表。

在 restore 数据中存在大量的表，可以尝试增加并发参数 `--concurrency=1024` 与 `--ddl-batch-size=256` 一起使用，示例如下：

{{< copyable "shell-regular" >}}

```shell
bin/br restore table --db batchmark --table order_line -s local:///br_data/ --pd 172.16.5.198:2379 --log-file restore-concurrency.log --concurrency 1024 --ddl-batch-size=256
```

* 此参数在数据恢复时，可以加速建表速度，测试显示6万张表恢复建表时间仅需5分钟

## 使用限制

数据恢复批量建表是默认以一次128张表为批，并发批量建表的方案。且它需要 TiDB 和 BR 都大于 v6.0.0 版本。如果 TiDB 或者 BR 同时或者任意一方版本低于 v6.0.0 版本，BR 数据恢复会回退到老的建表方式，依次串行建表。

该功能的已知问题及其解决方案如下：

- BR 恢复存档时报错 `entry too large, the max entry size is 6291456, the size of data is 7690800`。
    - 解决方法：可以尝试降低并发大小，如设置 `--ddl-batch-size=128` 或者更小的值。当你已经设置了 `--ddl-batch-size` 参数值后，在使用 BR 恢复数据时，BR 会先调用内部接口 `BatchCreateTableWithInfo`，然后使用内部 DDL job `ActionCreateTables`，最后根据已设置的 `--ddl-batch-size` 的值来在 TiDB 建表。当 TiDB 执行这个 DDL job 时，TiDB 会把 job 队列写到 TiKV 上。由于 TiDB 能够一次性发送的 job message 默认的最大值为 6 MB（**不建议**修改此值），因此，单次发送的所有表的 schema 总和不可以超过 6 MB，否则，会报 `entry too large, the max entry size is 6291456, the size of data is 7690800` 错误。如需了解有关单个写入请求的数据量的具体限制，请参阅 TiDB 配置项 [txn-entry-size-limit](/tidb-configuration-file.md#txn-entry-size-limit-从-v50-版本开始引入) 和 TiKV 配置项 [raft-entry-max-size](/tikv-configuration-file.md#raft-entry-max-size)。

## 实现原理

在 v6.0.0 以前，BR使用老的建表方法，老的建表方法是类似于 SQL 层 create table, 每张表会引起一次 schema version 的变更， 每次 schema 变更需要 需要同步到其他 BR 和其他的 TiDB.在 v6.0.0 及以后，数据恢复批量建表会按批来建表，每次建一批表且 TiDB schema version 变更一次。此方法极大的提高了建表速度。

### 以下集群配置测试结果

* 集群配置：15 个 TiKV 配备 16 个 CPU 80G 内存， 3个 TiDB, 3个 PD.
* 数据规模：`total-kv-size=16.16TB`
* TiKV [import.num-threads](/tikv-configuration-file.md#num-threads) 设置为 16

v6.0.0 测试结果：

‘[2022/03/12 22:37:49.060 +08:00] [INFO] [collector.go:67] ["Full restore success summary"] [total-ranges=751760] [ranges-succeed=751760] [ranges-failed=0] [split-region=1h33m18.078448449s] [restore-ranges=542693] [total-take=1h41m35.471476438s] [restore-data-size(after-compressed)=8.337TB] [Size=8336694965072] [BackupTS=431773933856882690] [total-kv=148015861383] [total-kv-size=16.16TB] [average-speed=2.661GB/s]’

* 恢复吞吐：`average-speed=2.661GB/s`
* 单个 TiKV 实例的平均恢复速度：`average-speed(GB/s)`/`tikv_count` = `181.65(MB/s)`