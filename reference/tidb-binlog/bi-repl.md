---
title: 集群间双向同步
category: reference
---

# 集群间双向同步

## 使用场景

当需要在两个 TiDB 集群之间双向同步数据时，可在 TiDB Binlog 进行操作。例如要将写入集群 A 的数据同步到集群 B，而且要将写入集群 B 的数据同步到集群 A。写入的数据与两个集群中的相同表无冲突，即不会在两个集群修改表的同一主键或者唯一索引的行。

## 实现原理

实现原理如下图所示：

![Architect](/media/binlog/bi-repl1.jpg)

- 为 A 和 B 两个集群分别启动 TiDB Binlog 同步程序。

- 为 TiDB Binlog 的 Drainer 新增以下逻辑：
    * 写目标 cluster 的时候，对每个事务加入一个对表 `_drainer_repl_mark` 的 dml event。
    * 解析 binlog event 的时候，发现事务带有对表 `_drainer_repl_mark` 的 dml event，放弃同步该事务。
    * DDL 没有事务概念采取单向同步的方案。

## 示意图

![Mark Table](/media/binlog/bi-repl2.jpg)

更新 `_drainer_repl_mark` 表时，一定要有数据改动才会产生 binlog。

## 标识表

`_drainer_repl_mark` 标识表的结构如下：

```
CREATE TABLE `_drainer_repl_mark` (
  `id` bigint(20) NOT NULL,
  `channel_id` bigint(20) NOT NULL DEFAULT '0',
  `val` bigint(20) DEFAULT '0',
  `channel_info` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`id`,`channel_id`)
);
```

Drainer 使用如以下 SQL 语句更新 `_drainer_repl_mark` 一定会有数据改动：

```sql
update drainer_repl_mark set val = val + 1 where id = ? && channel_id = ?;
```

Drainer 与下游的每个连接可以使用一个 ID 以避免冲突。`channel_id` 用来表示进行双向同步的一个通道。A 和 B 两个集群进行双向同步的配置应使用相同的值。

## DDL 同步

DDL 操作无法加入标识表，因此采用单向同步方案。

集群 A 到集群 B 开启 DDL 同步，集群 B 到集群 A 关闭 DDL 同步。DDL 操作全部在 A 上执行。

> **注意：**
>
> DDL 无法在两个集群同时执行。执行 DDL 时，若同时有 DML 操作或者 DML binlog 没同步完，会可能出现 DML 同步的上下游表结构不一致的情况。

当有添加或者删除列时，要同步到下游的数据可能会出现多列或者少列的情况。Drainer 通过添加配置来允许这种情况，会忽略多了的列值或者给少了的列写入默认值。

## 部署配置

若要进行双向同步，需在 Drainer 中添加以下配置：

```toml
[syncer]
loopback-control = true
channel-id = 1 # 互相同步的两个集群配置相同值
sync-ddl = false  # 不做 ddl 的那一边配置 false

[syncer.to]
# 1: SyncFullColumn, 2: SyncPartialColumn
# 当设置成 SyncPartialColumn， drainer 会允许下游表结构比当前要同步的数据多或者少列。
# 并且去掉 sql mode 的 STRICT_TRANS_TABLES 来允许对于缺少的列，插入零值到下游。
sync-mode = 2

# 忽略 checkpoint 表
[[syncer.ignore-table]]
db-name = "tidb_binlog"
tbl-name = "checkpoint"
```
