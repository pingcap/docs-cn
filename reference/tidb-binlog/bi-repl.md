---
title: 双向同步
category: reference
---

# 基本需求

两个 TiDB cluster 之间双向同步，比如 A <-> B, A 写入的数据要同步到 B，B 写入的数据要同步到 A，但本身同一个表 A，B 写入的数据不会有冲突，即不会在两边修改同一主键或者唯一索引的行。

# 实现方案

## 思路

![Architect](/media/binlog/bi-repl1.jpg)

- 为两个集群 cluster A 和 cluster B 分别启动 tidb binlog 同步程序

- tidb binlog 的 drainer 新增逻辑
    * 写目标 cluster 的时候，对每个事务加入一个对表 `_drainer_repl_mark` 的 dml event。
    * 解析 binlog event 的时候，发现事务带有对表 `_drainer_repl_mark` 的 dml event，放弃同步该事务。
    * DDL 没有事务概念采取单向同步的方案。

## 示意图

![Mark Table](/media/binlog/bi-repl2.jpg)

对 `_drainer_repl_mark` 表的 update 一定要有数据改动才会产生 binlog。

## 标识表

表结构如下：

```
CREATE TABLE `_drainer_repl_mark` (
  `id` bigint(20) NOT NULL,
  `channel_id` bigint(20) NOT NULL DEFAULT '0',
  `val` bigint(20) DEFAULT '0',
  `channel_info` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`id`,`channel_id`)
);
```

drainer 使用如下 SQL 更新保证一定有数据改动：

```sql
update drainer_repl_mark set val = val + 1 where id = ? && channel_id = ?;
```

drainer 跟下游的每个连接可以使用一个 id 避免冲突，channel_id 用来表示做双向同步的一个通道，A, B 集群做双向同步要配置使用相同值。

# 关于 DDL 同步

DDL 没法加入标识表，采用单向同步方案。

A -> B 开启 ddl 同步， B -> A 关闭 ddl 同步， DDL 操作全部在 A 上执行。

注意 DDL 没法在两个集群同时执行，执行 DDL 同时有 DML 操作或者 DML binlog 没同步完，会可能出现上下游表结构不相同的 DML 数据同步。

当有添加或者删除列时会出现要同步到下游的数据多或者少列的情况，drainer 通过添加配置来允许这种情况，会忽略多了的列值或者给少了的列写默认值。

# 部署配置

针对双向同步 drainer 需要添加如下对应配置:

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
