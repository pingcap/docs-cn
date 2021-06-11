---
title: TIDB_TRX
summary: 了解 information_schema 表 `TIDB_TRX`。
---

# TIDB_TRX

`TIDB_TRX` 表提供了当前 TiDB 节点上正在执行的事务的信息。

> **警告：**
>
> * 该功能目前为实验性功能，表结构的定义和行为在未来版本中可能有较大改动。
> * 目前 `TIDB_TRX` 表暂不支持显示 TiDB 内部事务相关的信息。

{{< copyable "sql" >}}

```sql
USE information_schema;
DESC tidb_trx;
```

```sql
+--------------------+---------------------------------------------------------+------+------+---------+-------+
| Field              | Type                                                    | Null | Key  | Default | Extra |
+--------------------+---------------------------------------------------------+------+------+---------+-------+
| ID                 | bigint(21) unsigned                                     | NO   | PRI  | NULL    |       |
| START_TIME         | timestamp(6)                                            | YES  |      | NULL    |       |
| CURRENT_SQL_DIGEST | varchar(64)                                             | YES  |      | NULL    |       |
| STATE              | enum('Normal','LockWaiting','Committing','RollingBack') | YES  |      | NULL    |       |
| WAITING_START_TIME | timestamp(6)                                            | YES  |      | NULL    |       |
| MEM_BUFFER_KEYS    | bigint(64)                                              | YES  |      | NULL    |       |
| MEM_BUFFER_BYTES   | bigint(64)                                              | YES  |      | NULL    |       |
| SESSION_ID         | bigint(21) unsigned                                     | YES  |      | NULL    |       |
| USER               | varchar(16)                                             | YES  |      | NULL    |       |
| DB                 | varchar(64)                                             | YES  |      | NULL    |       |
| ALL_SQL_DIGESTS    | text                                                    | YES  |      | NULL    |       |
+--------------------+---------------------------------------------------------+------+------+---------+-------+
```

`TIDB_TRX` 表中各列的字段含义如下：

* `ID`：事务 ID，即事务的开始时间戳 `start_ts`。
* `START_TIME`：事务的开始时间，即事务的 `start_ts` 所对应的物理时间。
* `CURRENT_SQL_DIGEST`：该事务当前正在执行的 SQL 语句的 Digest。
* `STATE`：该事务当前所处的状态。其可能的值包括:
    * `Normal`：事务正在正常执行，或者处于闲置状态。
    * `LockWaiting`：事务处于正在等待悲观锁上锁完成的状态。需要注意的是，事务刚开始进行悲观锁上锁操作时即进入该状态，无论是否有被其它事务阻塞。
    * `Committing`：事务正在提交过程中。
    * `RollingBack`：事务正在回滚过程中。
* `WAITING_START_TIME`：当 `STATE` 值为 `LockWaiting` 时，该列显示等待的开始时间。
* `MEM_BUFFER_KEYS`：当前事务写入内存缓冲区的 key 的个数。
* `MEM_BUFFER_BYTES`：当前事务写入内存缓冲区的 key 和 value 的总字节数。
* `SESSION_ID`：该事务所属的 session 的 ID。
* `USER`：执行该事务的用户名。
* `DB`：执行该事务的 session 当前的默认数据库名。
* `ALL_SQL_DIGESTS`：该事务已经执行过的语句的 Digest 的列表。每个事务最多记录前 50 条语句。

## 示例

{{< copyable "sql" >}}

```sql
select * from information_schema.tidb_trx\G
```

```sql
*************************** 1. row ***************************
                ID: 425403705115541506
        START_TIME: 2021-06-04 05:59:10.691000
CURRENT_SQL_DIGEST: NULL
             STATE: Normal
WAITING_START_TIME: NULL
   MEM_BUFFER_KEYS: 2
  MEM_BUFFER_BYTES: 48
        SESSION_ID: 7
              USER: root
                DB: test
   ALL_SQL_DIGESTS: [e6f07d43b5c21db0fbb9a31feac2dc599787763393dd5acbfad80e247eb02ad5, 04fa858fa491c62d194faec2ab427261cc7998b3f1ccf8f6844febca504cb5e9, f7530877a35ae65300c42250abd8bc731bbaf0a7cabc05dab843565230611bb2]
1 row in set (0.00 sec)
```

此示例的查询结果表示：当前节点有一个事务正在执行（`STATE` 为 `Normal`），该事务目前处于闲置状态（`CURRENT_SQL_DIGEST` 为 `NULL`）， 该事务已经执行过 3 条语句（`ALL_SQL_DIGESTS` 列表中有三条记录，分别为执行过的 3 条语句的 Digest）。

## CLUSTER_TIDB_TRX

`TIDB_TRX` 表仅提供单个 TiDB 节点中正在执行的事务信息。如果要查看整个集群上所有 TiDB 节点中正在执行的事务信息，需要查询 `CLUSTER_TIDB_TRX` 表。与 `TIDB_TRX` 表的查询结果相比，`CLUSTER_TIDB_TRX` 表的查询结果额外包含了 `INSTANCE` 字段。`INSTANCE` 字段展示了集群中各节点的 IP 地址和端口，用于区分事务所在的 TiDB 节点。

{{< copyable "sql" >}}

```sql
USE information_schema;
DESC cluster_tidb_trx;
```

```sql
+--------------------+---------------------------------------------------------+------+------+---------+-------+
| Field              | Type                                                    | Null | Key  | Default | Extra |
+--------------------+---------------------------------------------------------+------+------+---------+-------+
| INSTANCE           | varchar(64)                                             | YES  |      | NULL    |       |
| ID                 | bigint(21) unsigned                                     | NO   | PRI  | NULL    |       |
| START_TIME         | timestamp(6)                                            | YES  |      | NULL    |       |
| CURRENT_SQL_DIGEST | varchar(64)                                             | YES  |      | NULL    |       |
| STATE              | enum('Normal','LockWaiting','Committing','RollingBack') | YES  |      | NULL    |       |
| WAITING_START_TIME | timestamp(6)                                            | YES  |      | NULL    |       |
| MEM_BUFFER_KEYS    | bigint(64)                                              | YES  |      | NULL    |       |
| MEM_BUFFER_BYTES   | bigint(64)                                              | YES  |      | NULL    |       |
| SESSION_ID         | bigint(21) unsigned                                     | YES  |      | NULL    |       |
| USER               | varchar(16)                                             | YES  |      | NULL    |       |
| DB                 | varchar(64)                                             | YES  |      | NULL    |       |
| ALL_SQL_DIGESTS    | text                                                    | YES  |      | NULL    |       |
+--------------------+---------------------------------------------------------+------+------+---------+-------+
```

## SQL Digest

`TIDB_TRX` 表只记录 SQL Digest，不记录 SQL 语句原文。

SQL Digest 是 SQL 归一化之后的哈希值。如需查找 SQL Digest 对应的 SQL 原文，请进行以下操作之一：

- 对于当前 TiDB 节点在最近一段时间内执行过的语句，你可以从 `STATEMENTS_SUMMARY` 或 `STATEMENTS_SUMMARY_HISTORY` 中根据 SQL Digest 查找到对应的 SQL 原文。
- 对于整个集群所有 TiDB 节点在最近一段时间内执行过的语句，你可以从 `CLUSTER_STATEMENTS_SUMMARY` 或`CLUSTER_STATEMENTS_SUMMARY_HISTORY` 中根据 SQL Digest 查找到对应的 SQL 原文。

{{< copyable "sql" >}}

```sql
select digest, digest_text from information_schema.statements_summary where digest = "f7530877a35ae65300c42250abd8bc731bbaf0a7cabc05dab843565230611bb2";
```

```sql
+------------------------------------------------------------------+---------------------------------------+
| digest                                                           | digest_text                           |
+------------------------------------------------------------------+---------------------------------------+
| f7530877a35ae65300c42250abd8bc731bbaf0a7cabc05dab843565230611bb2 | update `t` set `v` = ? where `id` = ? |
+------------------------------------------------------------------+---------------------------------------+
```

关于 SQL Digest 和 `STATEMENTS_SUMMARY`、`STATEMENTS_SUMMARY_HISTORY` 、`CLUSTER_STATEMENTS_SUMMARY`、`CLUSTER_STATEMENTS_SUMMARY_HISTORY` 表的详细说明，请参阅 [Statement Summary Tables](/statement-summary-tables.md)。
