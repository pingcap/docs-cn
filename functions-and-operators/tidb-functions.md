---
title: TiDB 特有的函数
summary: 学习使用 TiDB 特有的函数。
---

# TiDB 特有的函数

以下函数为 TiDB 中特有的函数，与 MySQL 不兼容：

| 函数名 | 函数说明 |
| :-------------- | :------------------------------------- |
| [`CURRENT_RESOURCE_GROUP()`](#current_resource_group) | 用于查询当前连接绑定的资源组名。参见[使用资源管控 (Resource Control) 实现资源组限制和流控](/tidb-resource-control-ru-groups.md)。 |
| [`TIDB_BOUNDED_STALENESS()`](#tidb_bounded_staleness) | 指示 TiDB 在指定时间范围内读取尽可能新的数据。参见[使用 `AS OF TIMESTAMP` 语法读取历史数据](/as-of-timestamp.md)。 |
| [`TIDB_CURRENT_TSO()`](#tidb_current_tso) | 返回当前的 [TimeStamp Oracle (TSO)](/tso.md)。 |
| [`TIDB_DECODE_BINARY_PLAN()`](#tidb_decode_binary_plan) | 用于解码以二进制格式编码的执行计划。 |
| [`TIDB_DECODE_KEY()`](#tidb_decode_key) | 用于将 TiDB 编码的键输入解码为包含 `_tidb_rowid` 和 `table_id` 的 JSON 结构。一些系统表和日志输出中有 TiDB 编码的键。 |
| [`TIDB_DECODE_PLAN()`](#tidb_decode_plan) | 用于解码 TiDB 执行计划。 |
| [`TIDB_DECODE_SQL_DIGESTS()`](#tidb_decode_sql_digests) | 用于在集群中查询一组 SQL digest 所对应的 SQL 语句的归一化形式（即去除格式和参数后的形式）。 |
| [`TIDB_ENCODE_INDEX_KEY()`](#tidb_encode_index_key) | 对索引键进行编码。 |
| [`TIDB_ENCODE_RECORD_KEY()`](#tidb_encode_record_key) | 对记录键进行编码。 |
| [`TIDB_ENCODE_SQL_DIGEST()`](#tidb_encode_sql_digest) | 用于为查询字符串获取 digest。 |
| [`TIDB_IS_DDL_OWNER()`](#tidb_is_ddl_owner) | 用于检查你连接的 TiDB 实例是否是 DDL Owner。DDL Owner 是代表集群中所有其他节点执行 DDL 语句的 TiDB 实例。 |
| [`TIDB_MVCC_INFO()`](#tidb_mvcc_info) | 返回关于某个键的多版本并发控制 ([Multi-Version Concurrency Control, MVCC](/glossary.md#multi-version-concurrency-control-mvcc)) 信息。 |
| [`TIDB_PARSE_TSO()`](#tidb_parse_tso) | 用于从 TiDB TSO 时间戳中提取物理时间戳。参见 [`tidb_current_ts`](/system-variables.md#tidb_current_ts)。 |
| [`TIDB_PARSE_TSO_LOGICAL()`](#tidb_parse_tso_logical) | 用于从 TiDB TSO 时间戳中提取逻辑时间戳。|
| [`TIDB_ROW_CHECKSUM()`](#tidb_row_checksum) | 用于查询行数据的 Checksum 值。该函数只能用于 FastPlan 流程的 `SELECT` 语句，即你可通过类似 `SELECT TIDB_ROW_CHECKSUM() FROM t WHERE id = ?` 或 `SELECT TIDB_ROW_CHECKSUM() FROM t WHERE id IN (?, ?, ...)` 的语句进行查询。参见[数据正确性校验](/ticdc/ticdc-integrity-check.md)。 |
| [`TIDB_SHARD()`](#tidb_shard) | 用于创建一个 SHARD INDEX 来打散热点索引。SHARD INDEX 是一种以 `TIDB_SHARD` 函数为前缀的表达式索引。 |
| [`TIDB_VERSION()`](#tidb_version) | 用于获取当前连接的 TiDB 服务器的版本以及构建信息。 |
| [`VITESS_HASH()`](#vitess_hash) | 返回与 Vitess 的 `HASH` 函数兼容的数值的哈希值，有助于从 Vitess 迁移至 TiDB。 |

## CURRENT_RESOURCE_GROUP

`CURRENT_RESOURCE_GROUP()` 函数用于查询当前连接绑定的资源组名称。当开启[资源管控 (Resource Control)](/tidb-resource-control-ru-groups.md) 功能时，执行 SQL 语句对资源的占用会受到所绑定的资源组资源配置的限制。

在会话建立时，TiDB 默认会将连接绑定至登录用户绑定的资源组，如果用户没有绑定任何资源组，则会将连接绑定至 `default` 资源组。在会话建立之后，绑定的资源组默认不会发生变化，即使执行了[修改用户绑定的资源组](/sql-statements/sql-statement-alter-user.md#修改用户绑定的资源组)。如需修改当前会话绑定的资源组，可以使用 [`SET RESOURCE GROUP`](/sql-statements/sql-statement-set-resource-group.md) 语句。

示例：

创建一个用户 `user1`，创建两个资源组 `rg1` 和 `rg2`，并将用户 `user1` 绑定资源组 `rg1`：

```sql
CREATE USER 'user1';
CREATE RESOURCE GROUP rg1 RU_PER_SEC = 1000;
CREATE RESOURCE GROUP rg2 RU_PER_SEC = 2000;
ALTER USER 'user1' RESOURCE GROUP `rg1`;
```

使用 `user1` 登录，查看当前用户绑定的资源组：

```sql
SELECT CURRENT_RESOURCE_GROUP();
```

```
+--------------------------+
| CURRENT_RESOURCE_GROUP() |
+--------------------------+
| rg1                      |
+--------------------------+
1 row in set (0.00 sec)
```

执行 `SET RESOURCE GROUP` 将当前会话的资源组设置为 `rg2`，然后查看当前用户绑定的资源组：

```sql
SET RESOURCE GROUP `rg2`;
SELECT CURRENT_RESOURCE_GROUP();
```

```
+--------------------------+
| CURRENT_RESOURCE_GROUP() |
+--------------------------+
| rg2                      |
+--------------------------+
1 row in set (0.00 sec)
```

## TIDB_BOUNDED_STALENESS

`TIDB_BOUNDED_STALENESS()` 函数用作 [`AS OF TIMESTAMP`](/as-of-timestamp.md) 语法的一部分。

## TIDB_CURRENT_TSO

`TIDB_CURRENT_TSO()` 函数返回当前事务的 [TSO](/tso.md)，类似于 [`tidb_current_ts`](/system-variables.md#tidb_current_ts) 变量。

```sql
BEGIN;
```

```
Query OK, 0 rows affected (0.00 sec)
```

```sql
SELECT TIDB_CURRENT_TSO();
```

```
+--------------------+
| TIDB_CURRENT_TSO() |
+--------------------+
| 450456244814610433 |
+--------------------+
1 row in set (0.00 sec)
```

```sql
SELECT @@tidb_current_ts;
```

```
+--------------------+
| @@tidb_current_ts  |
+--------------------+
| 450456244814610433 |
+--------------------+
1 row in set (0.00 sec)
```

## TIDB_DECODE_BINARY_PLAN

`TIDB_DECODE_BINARY_PLAN(binary_plan)` 函数用于解码以二进制格式编码的执行计划，例如 [`STATEMENTS_SUMMARY`](/statement-summary-tables.md) 表中 `BINARY_PLAN` 列的计划。

必须将 [`tidb_generate_binary_plan`](/system-variables.md#tidb_generate_binary_plan-从-v620-版本开始引入) 变量设置为 `ON`，二进制计划才可用。

示例：

```sql
SELECT BINARY_PLAN,TIDB_DECODE_BINARY_PLAN(BINARY_PLAN) FROM information_schema.STATEMENTS_SUMMARY LIMIT 1\G
```

```
*************************** 1. row ***************************
                         BINARY_PLAN: lQLwPgqQAgoMUHJvamVjdGlvbl8zEngKDk1lbVRhYmxlU2Nhbl80KQAAAAAAiMNAMAM4AUABSioKKAoSaW5mb3JtYQU00HNjaGVtYRISU1RBVEVNRU5UU19TVU1NQVJZWhV0aW1lOjI5LjPCtXMsIGxvb3BzOjJw////CQIEAXgJCBD///8BIQFnDOCb+EA6cQCQUjlDb2x1bW4jOTIsIHRpZGJfZGVjb2RlX2JpbmFyeV9wbGFuKBUjCCktPg0MEDEwM1oWBYAIMTA4NoEAeGINQ29uY3VycmVuY3k6NXDIZXj///////////8BGAE=
TIDB_DECODE_BINARY_PLAN(BINARY_PLAN):
| id               | estRows  | estCost   | actRows | task | access object            | execution info                       | operator info                                             | memory  | disk  |
| Projection_3     | 10000.00 | 100798.00 | 3       | root |                          | time:108.3µs, loops:2, Concurrency:5 | Column#92, tidb_decode_binary_plan(Column#92)->Column#103 | 12.7 KB | N/A   |
| └─MemTableScan_4 | 10000.00 | 0.00      | 3       | root | table:STATEMENTS_SUMMARY | time:29.3µs, loops:2                 |                                                           | N/A     | N/A   |

1 row in set (0.00 sec)
```

## TIDB_DECODE_KEY

`TIDB_DECODE_KEY()` 函数用于将 TiDB 编码的键输入解码为包含 `_tidb_rowid` 和 `table_id` 的 JSON 结构。在一些系统表和日志输出中有 TiDB 编码的键。

以下示例中，表 `t1` 有一个隐藏的 `rowid`，该 `rowid` 由 TiDB 生成。语句中使用了 `TIDB_DECODE_KEY()` 函数。结果显示，隐藏的 `rowid` 被解码后并输出，这是典型的非聚簇主键结果。

```sql
SELECT START_KEY, TIDB_DECODE_KEY(START_KEY) FROM information_schema.tikv_region_status WHERE table_name='t1' AND REGION_ID=2\G
```

```
*************************** 1. row ***************************
                 START_KEY: 7480000000000000FF3B5F728000000000FF1DE3F10000000000FA
TIDB_DECODE_KEY(START_KEY): {"_tidb_rowid":1958897,"table_id":"59"}
1 row in set (0.00 sec)
```

以下示例中，表 `t2` 有一个复合聚簇主键。由 JSON 输出可知，输出结果的 `handle` 项中包含了主键部分两列的信息，即两列的名称和对应的值。

```sql
SHOW CREATE TABLE t2\G
```

```
*************************** 1. row ***************************
       Table: t2
Create Table: CREATE TABLE `t2` (
  `id` binary(36) NOT NULL,
  `a` tinyint unsigned NOT NULL,
  `v` varchar(512) DEFAULT NULL,
  PRIMARY KEY (`a`,`id`) /*T![clustered_index] CLUSTERED */
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
1 row in set (0.001 sec)
```

```sql
SELECT * FROM information_schema.tikv_region_status WHERE table_name='t2' LIMIT 1\G
```

```
*************************** 1. row ***************************
                REGION_ID: 48
                START_KEY: 7480000000000000FF3E5F720400000000FF0000000601633430FF3338646232FF2D64FF3531632D3131FF65FF622D386337352DFFFF3830653635303138FFFF61396265000000FF00FB000000000000F9
                  END_KEY:
                 TABLE_ID: 62
                  DB_NAME: test
               TABLE_NAME: t2
                 IS_INDEX: 0
                 INDEX_ID: NULL
               INDEX_NAME: NULL
           EPOCH_CONF_VER: 1
            EPOCH_VERSION: 38
            WRITTEN_BYTES: 0
               READ_BYTES: 0
         APPROXIMATE_SIZE: 136
         APPROXIMATE_KEYS: 479905
  REPLICATIONSTATUS_STATE: NULL
REPLICATIONSTATUS_STATEID: NULL
1 row in set (0.005 sec)
```

```sql
SELECT tidb_decode_key('7480000000000000FF3E5F720400000000FF0000000601633430FF3338646232FF2D64FF3531632D3131FF65FF622D386337352DFFFF3830653635303138FFFF61396265000000FF00FB000000000000F9');
```

```
+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| tidb_decode_key('7480000000000000FF3E5F720400000000FF0000000601633430FF3338646232FF2D64FF3531632D3131FF65FF622D386337352DFFFF3830653635303138FFFF61396265000000FF00FB000000000000F9') |
+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| {"handle":{"a":"6","id":"c4038db2-d51c-11eb-8c75-80e65018a9be"},"table_id":62}                                                                                                        |
+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.001 sec)
```

以下示例中，表中的第一个 Region 以一个仅包含 `table_id` 的 key 开头，表中的最后一个 Region 以 `table_id + 1` 结束。中间的 Region 有着更长的 key，包含 `_tidb_rowid` 或 `handle`。

```sql
SELECT
  TABLE_NAME,
  TIDB_DECODE_KEY(START_KEY),
  TIDB_DECODE_KEY(END_KEY)
FROM
  information_schema.TIKV_REGION_STATUS
WHERE
  TABLE_NAME='stock'
  AND IS_INDEX=0
ORDER BY
  START_KEY;
```

```
+------------+-----------------------------------------------------------+-----------------------------------------------------------+
| TABLE_NAME | TIDB_DECODE_KEY(START_KEY)                                | TIDB_DECODE_KEY(END_KEY)                                  |
+------------+-----------------------------------------------------------+-----------------------------------------------------------+
| stock      | {"table_id":143}                                          | {"handle":{"s_i_id":"32485","s_w_id":"3"},"table_id":143} |
| stock      | {"handle":{"s_i_id":"32485","s_w_id":"3"},"table_id":143} | {"handle":{"s_i_id":"64964","s_w_id":"5"},"table_id":143} |
| stock      | {"handle":{"s_i_id":"64964","s_w_id":"5"},"table_id":143} | {"handle":{"s_i_id":"97451","s_w_id":"7"},"table_id":143} |
| stock      | {"handle":{"s_i_id":"97451","s_w_id":"7"},"table_id":143} | {"table_id":145}                                          |
+------------+-----------------------------------------------------------+-----------------------------------------------------------+
4 rows in set (0.031 sec)
```

`TIDB_DECODE_KEY` 在解码成功时返回有效的 JSON，在解码失败时返回传入的参数值。

## TIDB_DECODE_PLAN

你可以在慢查询日志中找到编码形式的 TiDB 执行计划，然后使用 `TIDB_DECODE_PLAN()` 函数将编码的执行计划解码为易读的形式。

该函数很有用，因为在执行语句时 TiDB 会捕获执行计划。重新执行 `EXPLAIN` 中的语句可能会产生不同的结果，因为数据分布和统计数据会随着时间的推移而变化。

```sql
SELECT tidb_decode_plan('8QIYMAkzMV83CQEH8E85LjA0CWRhdGE6U2VsZWN0aW9uXzYJOTYwCXRpbWU6NzEzLjHCtXMsIGxvb3BzOjIsIGNvcF90YXNrOiB7bnVtOiAxLCBtYXg6IDU2OC41wgErRHByb2Nfa2V5czogMCwgcnBjXxEpAQwFWBAgNTQ5LglZyGNvcHJfY2FjaGVfaGl0X3JhdGlvOiAwLjAwfQkzLjk5IEtCCU4vQQoxCTFfNgkxXzAJMwm2SGx0KHRlc3QudC5hLCAxMDAwMCkNuQRrdgmiAHsFbBQzMTMuOMIBmQnEDDk2MH0BUgEEGAoyCTQzXzUFVwX1oGFibGU6dCwga2VlcCBvcmRlcjpmYWxzZSwgc3RhdHM6cHNldWRvCTk2ISE2aAAIMTUzXmYA')\G
```

```
*************************** 1. row ***************************
  tidb_decode_plan('8QIYMAkzMV83CQEH8E85LjA0CWRhdGE6U2VsZWN0aW9uXzYJOTYwCXRpbWU6NzEzLjHCtXMsIGxvb3BzOjIsIGNvcF90YXNrOiB7bnVtOiAxLCBtYXg6IDU2OC41wgErRHByb2Nfa2V5czogMCwgcnBjXxEpAQwFWBAgNTQ5LglZyGNvcHJfY2FjaGVfaGl0X3JhdGlvOiAwLjAwfQkzLjk5IEtCCU4vQQoxCTFfNgkxXz:     id                     task         estRows    operator info                              actRows    execution info                                                                                                                         memory     disk
    TableReader_7          root         319.04     data:Selection_6                           960        time:713.1µs, loops:2, cop_task: {num: 1, max: 568.5µs, proc_keys: 0, rpc_num: 1, rpc_time: 549.1µs, copr_cache_hit_ratio: 0.00}    3.99 KB    N/A
    └─Selection_6          cop[tikv]    319.04     lt(test.t.a, 10000)                        960        tikv_task:{time:313.8µs, loops:960}                                                                                                   N/A        N/A
      └─TableFullScan_5    cop[tikv]    960        table:t, keep order:false, stats:pseudo    960        tikv_task:{time:153µs, loops:960}                                                                                                     N/A        N/A
```

## TIDB_DECODE_SQL_DIGESTS

`TIDB_DECODE_SQL_DIGESTS()` 函数用于在集群中查询一组 SQL Digest 所对应的 SQL 语句的归一化形式（即去除格式和参数后的形式）。函数接受 1 个或 2 个参数：

* `digests`：字符串类型，该参数应符合 JSON 字符串数组的格式，数组中的每个字符串应为一个 SQL Digest。
* `stmtTruncateLength`：可选参数，整数类型，用来限制返回结果中每条 SQL 语句的长度，超过指定的长度会被截断。`0` 表示不限制长度。

该函数返回一个字符串，符合 JSON 字符串数组的格式，数组中的第 *i* 项为参数 `digests` 中的第 *i* 个元素所对应的语句。如果参数 `digests` 中的某一项不是一个有效的 SQL Digest 或系统无法查询到其对应的 SQL 语句，则返回结果中对应项为 `null`。如果指定了截断长度 (`stmtTruncateLength > 0`)，则返回结果中每条超过该长度的语句，保留前 `stmtTruncateLength` 个字符，并在尾部增加 `"..."` 后缀表示发生了截断。如果参数 `digests` 为 `NULL`，则函数的返回值为 `NULL`。

> **注意：**
>
> * 仅持有 [PROCESS](https://dev.mysql.com/doc/refman/8.0/en/privileges-provided.html#priv_process) 权限的用户可以使用该函数。
> * `TIDB_DECODE_SQL_DIGESTS` 执行时，TiDB 内部从 Statement Summary 一系列表中查询每个 SQL Digest 所对应的语句，因而并不能保证对任意 SQL Digest 都总是能查询到对应的语句，只有在集群中执行过的语句才有可能被查询到，且是否能查询到受 Statement Summary 表相关配置的影响。有关 Statement Summary 表的详细说明，参见 [Statement Summary Tables](/statement-summary-tables.md)。
> * 该函数开销较大，在行数很多的查询中（比如在规模较大、比较繁忙的集群上查询 `information_schema.cluster_tidb_trx` 全表时）直接使用该函数可能导致查询运行时间较长。请谨慎使用。
>     * 该函数开销大的原因是，其每次被调用时，都会在内部发起对 `STATEMENTS_SUMMARY`、`STATEMENTS_SUMMARY_HISTORY`、`CLUSTER_STATEMENTS_SUMMARY` 和 `CLUSTER_STATEMENTS_SUMMARY_HISTORY` 这几张表的查询，且其中涉及 `UNION` 操作。且该函数目前不支持向量化，即对于多行数据调用该函数时，对每行都会独立进行一次上述的查询。

```sql
SET @digests = '["e6f07d43b5c21db0fbb9a31feac2dc599787763393dd5acbfad80e247eb02ad5","38b03afa5debbdf0326a014dbe5012a62c51957f1982b3093e748460f8b00821","e5796985ccafe2f71126ed6c0ac939ffa015a8c0744a24b7aee6d587103fd2f7"]';

SELECT TIDB_DECODE_SQL_DIGESTS(@digests);
```

```
+------------------------------------+
| TIDB_DECODE_SQL_DIGESTS(@digests)  |
+------------------------------------+
| ["begin",null,"select * from `t`"] |
+------------------------------------+
1 row in set (0.00 sec)
```

上面的例子中，参数是一个包含 3 个 SQL Digest 的 JSON 数组，其对应的 SQL 语句分别为查询结果中给出的三项。但是其中第二条 SQL Digest 所对应的 SQL 语句未能从集群中找到，因而结果中的第二项为 `null`。

```sql
SELECT TIDB_DECODE_SQL_DIGESTS(@digests, 10);
```

```sql
+---------------------------------------+
| TIDB_DECODE_SQL_DIGESTS(@digests, 10) |
+---------------------------------------+
| ["begin",null,"select * f..."]        |
+---------------------------------------+
1 row in set (0.01 sec)
```

上述调用指定了第二个参数（即截断长度）为 10，而查询结果中的第三条语句的长度大于 10，因而仅保留了前 10 个字符，并在尾部添加了 `"..."` 表示发生了截断。

另请参阅：

- [Statement Summary Tables](/statement-summary-tables.md)
- [`INFORMATION_SCHEMA.TIDB_TRX`](/information-schema/information-schema-tidb-trx.md)

## TIDB_ENCODE_SQL_DIGEST

`TIDB_ENCODE_SQL_DIGEST(query_str)` 函数返回查询字符串的 SQL digest。

在以下示例中，你可以看到两个查询都获得了相同的查询 digest，这是因为两个查询的 digest 都是 `select ?`。

```sql
SELECT TIDB_ENCODE_SQL_DIGEST('SELECT 1');
```

```
+------------------------------------------------------------------+
| TIDB_ENCODE_SQL_DIGEST('SELECT 1')                               |
+------------------------------------------------------------------+
| e1c71d1661ae46e09b7aaec1c390957f0d6260410df4e4bc71b9c8d681021471 |
+------------------------------------------------------------------+
1 row in set (0.00 sec)
```

```sql
SELECT TIDB_ENCODE_SQL_DIGEST('SELECT 2');
```

```
+------------------------------------------------------------------+
| TIDB_ENCODE_SQL_DIGEST('SELECT 2')                               |
+------------------------------------------------------------------+
| e1c71d1661ae46e09b7aaec1c390957f0d6260410df4e4bc71b9c8d681021471 |
+------------------------------------------------------------------+
1 row in set (0.00 sec)
```

## TIDB_IS_DDL_OWNER

如果你连接的 TiDB 实例是 DDL Owner，`TIDB_IS_DDL_OWNER()` 函数返回 `1`。

```sql
SELECT TIDB_IS_DDL_OWNER();
```

```
+---------------------+
| TIDB_IS_DDL_OWNER() |
+---------------------+
|                   1 |
+---------------------+
1 row in set (0.00 sec)
```

## TIDB_PARSE_TSO

`TIDB_PARSE_TSO()` 函数用于从 TiDB TSO 时间戳中提取物理时间戳。

TSO 指 Time Stamp Oracle，是 PD (Placement Driver) 为每个事务提供的单调递增的时间戳。TSO 是一串数字，包含以下两部分：

- 一个物理时间戳
- 一个逻辑计数器

```sql
BEGIN;
SELECT TIDB_PARSE_TSO(@@tidb_current_ts);
ROLLBACK;
```

```
+-----------------------------------+
| TIDB_PARSE_TSO(@@tidb_current_ts) |
+-----------------------------------+
| 2021-05-26 11:33:37.776000        |
+-----------------------------------+
1 row in set (0.0012 sec)
```

以上示例使用 `TIDB_PARSE_TSO()` 函数从 `tidb_current_ts` 会话变量提供的可用时间戳编号中提取物理时间戳。因为每个事务都会分配到时间戳，所以此函数在事务中运行。

## TIDB_PARSE_TSO_LOGICAL

`TIDB_PARSE_TSO_LOGICAL(tso)` 函数返回从 TiDB [TSO](/tso.md) 时间戳中提取的逻辑时间戳。

```sql
SELECT TIDB_PARSE_TSO_LOGICAL(450456244814610433);
```

```
+--------------------------------------------+
| TIDB_PARSE_TSO_LOGICAL(450456244814610433) |
+--------------------------------------------+
|                                          1 |
+--------------------------------------------+
1 row in set (0.00 sec)
```

```sql
SELECT TIDB_PARSE_TSO_LOGICAL(450456244814610434);
```

```
+--------------------------------------------+
| TIDB_PARSE_TSO_LOGICAL(450456244814610434) |
+--------------------------------------------+
|                                          2 |
+--------------------------------------------+
1 row in set (0.00 sec)
```

## TIDB_ROW_CHECKSUM

`TIDB_ROW_CHECKSUM()` 函数用于查询行数据的 Checksum 值。该函数只能用于 FastPlan 流程的 `SELECT` 语句，即你可通过形如 `SELECT TIDB_ROW_CHECKSUM() FROM t WHERE id = ?` 或 `SELECT TIDB_ROW_CHECKSUM() FROM t WHERE id IN (?, ?, ...)` 的语句进行查询。

在 TiDB 中开启行数据 Checksum 功能 [`tidb_enable_row_level_checksum`](/system-variables.md#tidb_enable_row_level_checksum-从-v710-版本开始引入)：

```sql
SET GLOBAL tidb_enable_row_level_checksum = ON;
```

上述配置仅对新创建的会话生效，因此需要重新连接 TiDB。

创建表 `t` 并插入数据：

```sql
USE test;
CREATE TABLE t (id INT PRIMARY KEY, k INT, c CHAR(1));
INSERT INTO t VALUES (1, 10, 'a');
```

查询表 `t` 中 `id = 1` 的行数据的 Checksum 值：

```sql
SELECT *, TIDB_ROW_CHECKSUM() FROM t WHERE id = 1;
```

输出结果如下：

```
+----+------+------+---------------------+
| id | k    | c    | TIDB_ROW_CHECKSUM() |
+----+------+------+---------------------+
|  1 |   10 | a    | 3813955661          |
+----+------+------+---------------------+
1 row in set (0.000 sec)
```

## TIDB_SHARD

`TIDB_SHARD()` 函数用于创建一个 SHARD INDEX 来打散热点索引。SHARD INDEX 是一种以 `TIDB_SHARD()` 函数为前缀的表达式索引。

- 创建方式：

    使用 `uk((tidb_shard(a)), a))` 为字段 `a` 创建一个 SHARD INDEX。当二级唯一索引 `uk((tidb_shard(a)), a))` 的索引字段 `a` 上存在因单调递增或递减而产生的热点时，索引的前缀 `tidb_shard(a)` 会打散热点，从而提升集群可扩展性。

- 适用场景：

    - 二级唯一索引上 key 值存在单调递增或递减导致的写入热点，且该索引包含的列是整型。
    - 业务中 SQL 语句根据该二级索引的全部字段做等值查询，查询可以是单独的 `SELECT`，也可以是 `UPDATE`，`DELETE` 等产生的内部查询，等值查询包括 `a = 1` 或 `a IN (1, 2, ......)` 两种方式。

- 使用限制：

    - 非等值查询无法使用索引。
    - 查询条件中 `AND` 和 `OR` 混合且最外层是 `AND` 算子时无法使用 SHARD INDEX。
    - `GROUP BY` 无法使用 SHARD INDEX。
    - `ORDER BY` 无法使用 SHARD INDEX。
    - `ON` 子句无法使用 SHARD INDEX。
    - `WHERE` 子查询无法使用 SHARD INDEX。
    - SHARD INDEX 只能打散整型字段的唯一索引。
    - SHARD INDEX 联合索引可能失效。
    - SHARD INDEX 无法走 FastPlan 流程，影响优化器性能。
    - SHARD INDEX 无法使用执行计划缓存。

`TIDB_SHARD()` 函数的使用示例如下：

- 使用 `TIDB_SHARD()` 函数计算 SHARD 值：

    以下示例说明如何使用 `TIDB_SHARD()` 函数计算 `12373743746` 的 SHARD 值。

    ```sql
    SELECT TIDB_SHARD(12373743746);
    ```

- 计算得出 SHARD 值为：

    ```sql
    +-------------------------+
    | TIDB_SHARD(12373743746) |
    +-------------------------+
    |                     184 |
    +-------------------------+
    1 row in set (0.00 sec)
    ```

- 使用 `TIDB_SHARD()` 函数创建 SHARD INDEX：

    ```sql
    CREATE TABLE test(id INT PRIMARY KEY CLUSTERED, a INT, b INT, UNIQUE KEY uk((tidb_shard(a)), a));
    ```

## TIDB_VERSION

`TIDB_VERSION()` 函数用于获取当前连接的 TiDB 服务器版本和构建详细信息。向 GitHub 上提交 issue 时，你可使用此函数获取相关信息。

```sql
SELECT TIDB_VERSION()\G
```

```sql
*************************** 1. row ***************************
TIDB_VERSION(): Release Version: v8.5.1
Edition: Community
Git Commit Hash: 821e491a20fbab36604b36b647b5bae26a2c1418
Git Branch: HEAD
UTC Build Time: 2025-01-17 19:16:25
GoVersion: go1.21.10
Race Enabled: false
Check Table Before Drop: false
Store: tikv
1 row in set (0.00 sec)
```

## VITESS_HASH

`VITESS_HASH(num)` 函数以与 Vitess 相同的方式返回数值的哈希值。这有助于将数据从 Vitess 迁移到 TiDB。

示例：

```sql
SELECT VITESS_HASH(123);
```

```
+---------------------+
| VITESS_HASH(123)    |
+---------------------+
| 1155070131015363447 |
+---------------------+
1 row in set (0.00 sec)
```

## TIDB_ENCODE_INDEX_KEY

对索引键进行编码。

```sql
CREATE TABLE t(id int PRIMARY KEY, a int, KEY `idx` (a));
```

```
Query OK, 0 rows affected (0.00 sec)
```

```sql
INSERT INTO t VALUES(1,1);
```

```
Query OK, 1 row affected (0.00 sec)
```

```sql
SELECT TIDB_ENCODE_INDEX_KEY('test', 't', 'idx', 1, 1);
```

```
+----------------------------------------------------------------------------+
| TIDB_ENCODE_INDEX_KEY('test', 't', 'idx', 1, 1)                            |
+----------------------------------------------------------------------------+
| 74800000000000007f5f698000000000000001038000000000000001038000000000000001 |
+----------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

## TIDB_ENCODE_RECORD_KEY

对记录键进行编码。

```sql
CREATE TABLE t(id int PRIMARY KEY, a int, KEY `idx` (a));
```

```
Query OK, 0 rows affected (0.00 sec)
```

```sql
INSERT INTO t VALUES(1,1);
```

```
Query OK, 1 row affected (0.00 sec)
```

```sql
SELECT TIDB_ENCODE_RECORD_KEY('test', 't', 1);
```

```
+----------------------------------------+
| TIDB_ENCODE_RECORD_KEY('test', 't', 1) |
+----------------------------------------+
| 7480000000000000845f728000000000000001 |
+----------------------------------------+
1 row in set (0.00 sec)
```

```sql
SELECT TIDB_DECODE_KEY('7480000000000000845f728000000000000001');
```

```
+-----------------------------------------------------------+
| TIDB_DECODE_KEY('7480000000000000845f728000000000000001') |
+-----------------------------------------------------------+
| {"id":1,"table_id":"132"}                                 |
+-----------------------------------------------------------+
1 row in set (0.00 sec)
```

## TIDB_MVCC_INFO

返回关于某个键的多版本并发控制 ([Multi-Version Concurrency Control, MVCC](/glossary.md#multi-version-concurrency-control-mvcc)) 信息。你可以使用 [`TIDB_ENCODE_INDEX_KEY`](#tidb_encode_index_key) 函数获取键。

```sql
SELECT JSON_PRETTY(TIDB_MVCC_INFO('74800000000000007f5f698000000000000001038000000000000001038000000000000001')) AS info\G
```

```
*************************** 1. row ***************************
info: [
  {
    "key": "74800000000000007f5f698000000000000001038000000000000001038000000000000001",
    "mvcc": {
      "info": {
        "values": [
          {
            "start_ts": 454654803134119936,
            "value": "MA=="
          }
        ],
        "writes": [
          {
            "commit_ts": 454654803134119937,
            "short_value": "MA==",
            "start_ts": 454654803134119936
          }
        ]
      }
    }
  }
]
1 row in set (0.00 sec)
```
