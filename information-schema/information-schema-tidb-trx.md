---
title: TIDB_TRX
summary: 了解 information_schema 表 `TIDB_TRX`。
---

# TIDB_TRX

`TIDB_TRX` 表提供了当前 TiDB 节点上正在执行的事务的信息。

{{< copyable "sql" >}}

```sql
USE information_schema;
DESC tidb_trx;
```

```sql
+-------------------------+-----------------------------------------------------------------+------+------+---------+-------+
| Field                   | Type                                                            | Null | Key  | Default | Extra |
+-------------------------+-----------------------------------------------------------------+------+------+---------+-------+
| ID                      | bigint(21) unsigned                                             | NO   | PRI  | NULL    |       |
| START_TIME              | timestamp(6)                                                    | YES  |      | NULL    |       |
| CURRENT_SQL_DIGEST      | varchar(64)                                                     | YES  |      | NULL    |       |
| CURRENT_SQL_DIGEST_TEXT | text                                                            | YES  |      | NULL    |       |
| STATE                   | enum('Idle','Running','LockWaiting','Committing','RollingBack') | YES  |      | NULL    |       |
| WAITING_START_TIME      | timestamp(6)                                                    | YES  |      | NULL    |       |
| MEM_BUFFER_KEYS         | bigint(64)                                                      | YES  |      | NULL    |       |
| MEM_BUFFER_BYTES        | bigint(64)                                                      | YES  |      | NULL    |       |
| SESSION_ID              | bigint(21) unsigned                                             | YES  |      | NULL    |       |
| USER                    | varchar(16)                                                     | YES  |      | NULL    |       |
| DB                      | varchar(64)                                                     | YES  |      | NULL    |       |
| ALL_SQL_DIGESTS         | text                                                            | YES  |      | NULL    |       |
+-------------------------+-----------------------------------------------------------------+------+------+---------+-------+
```

`TIDB_TRX` 表中各列的字段含义如下：

* `ID`：事务 ID，即事务的开始时间戳 `start_ts`。
* `START_TIME`：事务的开始时间，即事务的 `start_ts` 所对应的物理时间。
* `CURRENT_SQL_DIGEST`：该事务当前正在执行的 SQL 语句的 Digest。
* `CURRENT_SQL_DIGEST_TEXT`：该事务当前正在执行的 SQL 语句的归一化形式，即去除了参数和格式的 SQL 语句。与 `CURRENT_SQL_DIGEST` 对应。
* `STATE`：该事务当前所处的状态。其可能的值包括:
    * `Idle`：事务处于闲置状态，即正在等待用户输入查询。
    * `Running`：事务正在正常执行一个查询。
    * `LockWaiting`：事务处于正在等待悲观锁上锁完成的状态。需要注意的是，事务刚开始进行悲观锁上锁操作时即进入该状态，无论是否有被其它事务阻塞。
    * `Committing`：事务正在提交过程中。
    * `RollingBack`：事务正在回滚过程中。
* `WAITING_START_TIME`：当 `STATE` 值为 `LockWaiting` 时，该列显示等待的开始时间。
* `MEM_BUFFER_KEYS`：当前事务写入内存缓冲区的 key 的个数。
* `MEM_BUFFER_BYTES`：当前事务写入内存缓冲区的 key 和 value 的总字节数。
* `SESSION_ID`：该事务所属的 session 的 ID。
* `USER`：执行该事务的用户名。
* `DB`：执行该事务的 session 当前的默认数据库名。
* `ALL_SQL_DIGESTS`：该事务已经执行过的语句的 Digest 的列表，表示为一个 JSON 格式的字符串数组。每个事务最多记录前 50 条语句。通过 [`TIDB_DECODE_SQL_DIGESTS`](/functions-and-operators/tidb-functions.md#tidb_decode_sql_digests) 函数可以将该列的信息变换为对应的归一化 SQL 语句的列表。

> **注意：**
>
> * 仅拥有 [PROCESS](https://dev.mysql.com/doc/refman/8.0/en/privileges-provided.html#priv_process) 权限的用户可以获取该表中的完整信息。没有 PROCESS 权限的用户则只能查询到当前用户所执行的事务的信息。
> * `CURRENT_SQL_DIGEST` 和 `ALL_SQL_DIGESTS` 列中的信息（SQL Digest）为 SQL 语句进行归一化后计算得到的哈希值。`CURRENT_SQL_DIGEST_TEXT` 列中的信息和函数 `TIDB_DECODE_SQL_DIGESTS` 所得到的结果均为内部从 Statements Summary 系列表中查询得到，因而存在内部查询不到对应语句的可能性。关于 SQL Digest 和 Statements Summary 相关表的详细说明，请参阅[Statement Summary Tables](/statement-summary-tables.md)。
> * [`TIDB_DECODE_SQL_DIGESTS`](/functions-and-operators/tidb-functions.md#tidb_decode_sql_digests) 函数调用开销较大，如果对大量事务的信息调用该函数查询历史 SQL，可能查询耗时较长。如果集群规模较大、同一时刻并发运行的事务较多，请避免直接在查询 `TIDB_TRX` 全表的同时直接将该函数用于 `ALL_SQL_DIGEST` 列（即尽量避免 ``select *, tidb_decode_sql_digests(all_sql_digests) from tidb_trx`` 这样的用法）。
> * 目前 `TIDB_TRX` 表暂不支持显示 TiDB 内部事务相关的信息。

## 示例

{{< copyable "sql" >}}

```sql
select * from information_schema.tidb_trx\G
```

```sql
*************************** 1. row ***************************
                     ID: 426789913200689153
             START_TIME: 2021-08-04 10:51:54.883000
     CURRENT_SQL_DIGEST: NULL
CURRENT_SQL_DIGEST_TEXT: NULL
                  STATE: Idle
     WAITING_START_TIME: NULL
        MEM_BUFFER_KEYS: 1
       MEM_BUFFER_BYTES: 29
             SESSION_ID: 7
                   USER: root
                     DB: test
        ALL_SQL_DIGESTS: ["e6f07d43b5c21db0fbb9a31feac2dc599787763393dd5acbfad80e247eb02ad5","04fa858fa491c62d194faec2ab427261cc7998b3f1ccf8f6844febca504cb5e9","b83710fa8ab7df8504920e8569e48654f621cf828afbe7527fd003b79f48da9e"]
*************************** 2. row ***************************
                     ID: 426789921471332353
             START_TIME: 2021-08-04 10:52:26.433000
     CURRENT_SQL_DIGEST: 38b03afa5debbdf0326a014dbe5012a62c51957f1982b3093e748460f8b00821
CURRENT_SQL_DIGEST_TEXT: update `t` set `v` = `v` + ? where `id` = ?
                  STATE: LockWaiting
     WAITING_START_TIME: 2021-08-04 10:52:35.106568
        MEM_BUFFER_KEYS: 0
       MEM_BUFFER_BYTES: 0
             SESSION_ID: 9
                   USER: root
                     DB: test
        ALL_SQL_DIGESTS: ["e6f07d43b5c21db0fbb9a31feac2dc599787763393dd5acbfad80e247eb02ad5","38b03afa5debbdf0326a014dbe5012a62c51957f1982b3093e748460f8b00821"]
2 rows in set (0.01 sec)
```

此示例的查询结果表示：当前节点有两个运行中的事务，第一个事务正在闲置状态（`STATE` 为 `Idle`，`CURRENT_SQL_DIGEST` 为 `NULL`），该事务已经执行过 3 条语句（`ALL_SQL_DIGESTS` 列表中有三条记录，分别为执行过的 3 条语句的 Digest）；第二个事务正在执行一条语句并正在等锁（`STATE` 为 `LockWaiting`，`WAITING_START_TIME` 显示了等锁开始的时间），该事务已经执行过两条语句，当前正在执行的语句形如 ``"update `t` set `v` = `v` + ? where `id` = ?"``。

{{< copyable "sql" >}}

```sql
select id, all_sql_digests, tidb_decode_sql_digests(all_sql_digests) as all_sqls from information_schema.tidb_trx\G
```

```sql
*************************** 1. row ***************************
             id: 426789913200689153
all_sql_digests: ["e6f07d43b5c21db0fbb9a31feac2dc599787763393dd5acbfad80e247eb02ad5","04fa858fa491c62d194faec2ab427261cc7998b3f1ccf8f6844febca504cb5e9","b83710fa8ab7df8504920e8569e48654f621cf828afbe7527fd003b79f48da9e"]
       all_sqls: ["begin","insert into `t` values ( ... )","update `t` set `v` = `v` + ?"]
*************************** 2. row ***************************
             id: 426789921471332353
all_sql_digests: ["e6f07d43b5c21db0fbb9a31feac2dc599787763393dd5acbfad80e247eb02ad5","38b03afa5debbdf0326a014dbe5012a62c51957f1982b3093e748460f8b00821"]
       all_sqls: ["begin","update `t` set `v` = `v` + ? where `id` = ?"]
```

此查询

## CLUSTER_TIDB_TRX

`TIDB_TRX` 表仅提供单个 TiDB 节点中正在执行的事务信息。如果要查看整个集群上所有 TiDB 节点中正在执行的事务信息，需要查询 `CLUSTER_TIDB_TRX` 表。与 `TIDB_TRX` 表的查询结果相比，`CLUSTER_TIDB_TRX` 表的查询结果额外包含了 `INSTANCE` 字段。`INSTANCE` 字段展示了集群中各节点的 IP 地址和端口，用于区分事务所在的 TiDB 节点。

{{< copyable "sql" >}}

```sql
USE information_schema;
DESC cluster_tidb_trx;
```

```sql
mysql> desc cluster_tidb_trx;
+-------------------------+-----------------------------------------------------------------+------+------+---------+-------+
| Field                   | Type                                                            | Null | Key  | Default | Extra |
+-------------------------+-----------------------------------------------------------------+------+------+---------+-------+
| INSTANCE                | varchar(64)                                                     | YES  |      | NULL    |       |
| ID                      | bigint(21) unsigned                                             | NO   | PRI  | NULL    |       |
| START_TIME              | timestamp(6)                                                    | YES  |      | NULL    |       |
| CURRENT_SQL_DIGEST      | varchar(64)                                                     | YES  |      | NULL    |       |
| CURRENT_SQL_DIGEST_TEXT | text                                                            | YES  |      | NULL    |       |
| STATE                   | enum('Idle','Running','LockWaiting','Committing','RollingBack') | YES  |      | NULL    |       |
| WAITING_START_TIME      | timestamp(6)                                                    | YES  |      | NULL    |       |
| MEM_BUFFER_KEYS         | bigint(64)                                                      | YES  |      | NULL    |       |
| MEM_BUFFER_BYTES        | bigint(64)                                                      | YES  |      | NULL    |       |
| SESSION_ID              | bigint(21) unsigned                                             | YES  |      | NULL    |       |
| USER                    | varchar(16)                                                     | YES  |      | NULL    |       |
| DB                      | varchar(64)                                                     | YES  |      | NULL    |       |
| ALL_SQL_DIGESTS         | text                                                            | YES  |      | NULL    |       |
+-------------------------+-----------------------------------------------------------------+------+------+---------+-------+
```
