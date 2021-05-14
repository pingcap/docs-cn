---
title: 集群实时增量同步
---

# 集群实时增量同步

本文档介绍如何将一个 TiDB 集群的数据实时同步到另一个 TiDB/MySQL 集群。

## 使用场景

当需要为一个运行中的 TiDB 集群设置从集群，并行进行数据同步的时候，可使用 BR/Dumpling/TiDB Binlog 进行操作。例如要将集群 A 的数据同步到新集群 B。


## 实现原理

任何写入 TiDB 的事务均指定了唯一的 commitTS，可以通过该 TS 获取一个 TiDB 集群全局一致的状态。

同步过程分为全量同步和增量同步

1. 执行全量备份恢复，并且获取到备份数据的 snapshot.
2. 执行增量同步，确保增量同步的起始点是备份数据的 snapshot.

> **注意：**
>
> * 

Drainer 与下游的每个连接可以使用一个 ID 以避免冲突。`channel_id` 用来表示进行双向同步的一个通道。A 和 B 两个集群进行双向同步的配置应使用相同的值。

当有添加或者删除列时，要同步到下游的数据可能会出现多列或者少列的情况。Drainer 通过添加配置来允许这种情况，会忽略多了的列值或者给少了的列写入默认值。

## 标识表

`_drainer_repl_mark` 标识表的结构如下：

{{< copyable "sql" >}}

```sql
CREATE TABLE `_drainer_repl_mark` (
  `id` bigint(20) NOT NULL,
  `channel_id` bigint(20) NOT NULL DEFAULT '0',
  `val` bigint(20) DEFAULT '0',
  `channel_info` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`id`,`channel_id`)
);
```

Drainer 使用如下 SQL 语句更新 `_drainer_repl_mark` 可保证数据改动，从而保证产生 binlog：

{{< copyable "sql" >}}

```sql
update drainer_repl_mark set val = val + 1 where id = ? && channel_id = ?;
```

## 同步 DDL

因为 Drainer 无法为 DDL 操作加入标识表，所以采用单向同步的方式来同步 DDL 操作。

比如集群 A 到集群 B 开启了 DDL 同步，则集群 B 到集群 A 会关闭 DDL 同步。即 DDL 操作全部在 A 上执行。

> **注意：**
>
> DDL 操作无法在两个集群上同时执行。执行 DDL 时，若同时有 DML 操作或者 DML binlog 没同步完，会可能出现 DML 同步的上下游表结构不一致的情况。

## 配置并开启双向同步

若要在集群 A 和集群 B 间进行双向同步，假设统一在集群 A 上执行 DDL。在集群 A 到集群 B 的同步路径上，向 Drainer 添加以下配置：

{{< copyable "" >}}

```toml
[syncer]
loopback-control = true
channel-id = 1 # 互相同步的两个集群配置相同的 ID。
sync-ddl = true # 需要同步 DDL 操作

[syncer.to]
# 1 表示 SyncFullColumn，2 表示 SyncPartialColumn。
# 若设为 SyncPartialColumn，Drainer 会允许下游表结构比当前要同步的数据多或者少列
# 并且去掉 SQL mode 的 STRICT_TRANS_TABLES，来允许少列的情况，并插入零值到下游。
sync-mode = 2

# 忽略 checkpoint 表。
[[syncer.ignore-table]]
db-name = "tidb_binlog"
tbl-name = "checkpoint"
```

在集群 B 到集群 A 的同步路径上，向 Drainer 添加以下配置：

{{< copyable "" >}}

```toml
[syncer]
loopback-control = true
channel-id = 1 # 互相同步的两个集群配置相同的 ID。
sync-ddl = false  # 不需要同步 DDL 操作。

[syncer.to]
# 1 表示 SyncFullColumn，2 表示 SyncPartialColumn。
# 若设为 SyncPartialColumn，Drainer 会允许下游表结构比当前要同步的数据多或者少列
# 并且去掉 SQL mode 的 STRICT_TRANS_TABLES，来允许少列的情况，并插入零值到下游。
sync-mode = 2

# 忽略 checkpoint 表。
[[syncer.ignore-table]]
db-name = "tidb_binlog"
tbl-name = "checkpoint"
```
