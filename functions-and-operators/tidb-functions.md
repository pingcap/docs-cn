---
title: TiDB 特有函数
summary: 了解 TiDB 特有函数的使用方法。
---

# TiDB 特有函数

以下函数是 TiDB 的扩展，在 MySQL 中不存在：

<CustomContent platform="tidb">

| 函数名称 | 函数描述 |
| :-------------- | :------------------------------------- |
| [`CURRENT_RESOURCE_GROUP()`](#current_resource_group)  | 返回当前会话绑定的资源组的名称。请参阅[使用资源控制实现资源隔离](/tidb-resource-control.md)。 |
| [`TIDB_BOUNDED_STALENESS()`](#tidb_bounded_staleness) | 指示 TiDB 读取指定时间范围内最新的数据。请参阅[使用 `AS OF TIMESTAMP` 子句读取历史数据](/as-of-timestamp.md)。 |
| [`TIDB_CURRENT_TSO()`](#tidb_current_tso) | 返回 TiDB 中当前的 [TimeStamp Oracle (TSO)](/tso.md)。 |
| [`TIDB_DECODE_BINARY_PLAN()`](#tidb_decode_binary_plan) | 解码二进制计划。 |
| [`TIDB_DECODE_KEY()`](#tidb_decode_key) | 将 TiDB 编码的键条目解码为包含 `_tidb_rowid` 和 `table_id` 的 JSON 结构。这些编码的键可以在一些系统表和日志输出中找到。 |
| [`TIDB_DECODE_PLAN()`](#tidb_decode_plan) | 解码 TiDB 执行计划。 |
| [`TIDB_DECODE_SQL_DIGESTS()`](#tidb_decode_sql_digests) | 查询集群中一组 SQL 摘要对应的规范化 SQL 语句（一种没有格式和参数的形式）。 |
| [`TIDB_ENCODE_SQL_DIGEST()`](#tidb_encode_sql_digest) | 获取查询字符串的摘要。 |
| [`TIDB_IS_DDL_OWNER()`](#tidb_is_ddl_owner) | 检查您连接的 TiDB 实例是否为 DDL Owner。DDL Owner 是负责代表集群中所有其他节点执行 DDL 语句的 TiDB 实例。 |
| [`TIDB_PARSE_TSO()`](#tidb_parse_tso) | 从 TiDB TSO 时间戳中提取物理时间戳。另请参阅：[`tidb_current_ts`](/system-variables.md#tidb_current_ts)。 |
| [`TIDB_PARSE_TSO_LOGICAL()`](#tidb_parse_tso_logical) | 从 TiDB TSO 时间戳中提取逻辑时间戳。 |
| [`TIDB_ROW_CHECKSUM()`](#tidb_row_checksum) | 查询行的校验和值。此函数只能在 FastPlan 进程中的 `SELECT` 语句中使用。也就是说，您可以通过 `SELECT TIDB_ROW_CHECKSUM() FROM t WHERE id = ?` 或 `SELECT TIDB_ROW_CHECKSUM() FROM t WHERE id IN (?, ?, ...)` 等语句进行查询。另请参阅：[单行数据的数据完整性验证](/ticdc/ticdc-integrity-check.md)。 |
| [`TIDB_SHARD()`](#tidb_shard) | 创建一个分片索引来分散索引热点。分片索引是以 `TIDB_SHARD` 函数作为前缀的表达式索引。|
| [`TIDB_VERSION()`](#tidb_version) | 返回包含其他构建信息的 TiDB 版本。 |
| [`VITESS_HASH()`](#vitess_hash) | 返回数字的哈希值。此函数与 Vitess 的 `HASH` 函数兼容，旨在帮助从 Vitess 迁移数据。 |

</CustomContent>

<CustomContent platform="tidb-cloud">

| 函数名称 | 函数描述 |
| :-------------- | :------------------------------------- |
| [`CURRENT_RESOURCE_GROUP()`](#current_resource_group)  | 返回当前会话绑定的资源组的名称。请参阅[使用资源控制实现资源隔离](/tidb-resource-control.md)。 |
| [`TIDB_BOUNDED_STALENESS()`](#tidb_bounded_staleness) | 指示 TiDB 读取指定时间范围内最新的数据。请参阅[使用 `AS OF TIMESTAMP` 子句读取历史数据](/as-of-timestamp.md)。 |
| [`TIDB_CURRENT_TSO()`](#tidb_current_tso) | 返回 TiDB 中当前的 [TimeStamp Oracle (TSO)](/tso.md)。 |
| [`TIDB_DECODE_BINARY_PLAN()`](#tidb_decode_binary_plan) | 解码二进制计划。 |
| [`TIDB_DECODE_KEY()`](#tidb_decode_key) | 将 TiDB 编码的键条目解码为包含 `_tidb_rowid` 和 `table_id` 的 JSON 结构。这些编码的键可以在一些系统表和日志输出中找到。 |
| [`TIDB_DECODE_PLAN()`](#tidb_decode_plan) | 解码 TiDB 执行计划。 |
| [`TIDB_DECODE_SQL_DIGESTS()`](#tidb_decode_sql_digests) | 查询集群中一组 SQL 摘要对应的规范化 SQL 语句（一种没有格式和参数的形式）。 |
| [`TIDB_ENCODE_SQL_DIGEST()`](#tidb_encode_sql_digest) | 获取查询字符串的摘要。 |
| [`TIDB_IS_DDL_OWNER()`](#tidb_is_ddl_owner) | 检查您连接的 TiDB 实例是否为 DDL Owner。DDL Owner 是负责代表集群中所有其他节点执行 DDL 语句的 TiDB 实例。 |
| [`TIDB_PARSE_TSO()`](#tidb_parse_tso) | 从 TiDB TSO 时间戳中提取物理时间戳。另请参阅：[`tidb_current_ts`](/system-variables.md#tidb_current_ts)。 |
| [`TIDB_PARSE_TSO_LOGICAL()`](#tidb_parse_tso_logical) | 从 TiDB TSO 时间戳中提取逻辑时间戳。 |
| [`TIDB_ROW_CHECKSUM()`](#tidb_row_checksum) | 查询行的校验和值。此函数只能在 FastPlan 进程中的 `SELECT` 语句中使用。也就是说，您可以通过 `SELECT TIDB_ROW_CHECKSUM() FROM t WHERE id = ?` 或 `SELECT TIDB_ROW_CHECKSUM() FROM t WHERE id IN (?, ?, ...)` 等语句进行查询。另请参阅：[单行数据的数据完整性验证](https://docs.pingcap.com/tidb/stable/ticdc-integrity-check)。 |
| [`TIDB_SHARD()`](#tidb_shard) | 创建一个分片索引来分散索引热点。分片索引是以 `TIDB_SHARD` 函数作为前缀的表达式索引。|
| [`TIDB_VERSION()`](#tidb_version) | 返回包含其他构建信息的 TiDB 版本。 |
| [`VITESS_HASH()`](#vitess_hash) | 返回数字的哈希值。此函数与 Vitess 的 `HASH` 函数兼容，旨在帮助从 Vitess 迁移数据。 |

</CustomContent>

## CURRENT_RESOURCE_GROUP

`CURRENT_RESOURCE_GROUP()` 函数用于显示当前会话绑定的资源组名称。当 [资源管控](/tidb-resource-control.md) 功能启用时，SQL 语句可用的资源会受到绑定资源组的资源配额限制。

当会话建立时，TiDB 默认将该会话绑定到登录用户所绑定的资源组。如果用户未绑定到任何资源组，则该会话将绑定到 `default` 资源组。会话建立后，默认情况下绑定的资源组不会更改，即使通过 [修改用户绑定的资源组](/sql-statements/sql-statement-alter-user.md#modify-basic-user-information) 更改了用户的绑定资源组。要更改当前会话的绑定资源组，可以使用 [`SET RESOURCE GROUP`](/sql-statements/sql-statement-set-resource-group.md)。

示例：

创建用户 `user1`，创建两个资源组 `rg1` 和 `rg2`，并将用户 `user1` 绑定到资源组 `rg1`：

```sql
CREATE USER 'user1';
CREATE RESOURCE GROUP rg1 RU_PER_SEC = 1000;
CREATE RESOURCE GROUP rg2 RU_PER_SEC = 2000;
ALTER USER 'user1' RESOURCE GROUP `rg1`;
```

使用 `user1` 登录并查看绑定到当前用户的资源组：

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

执行 `SET RESOURCE GROUP` 将当前会话的资源组设置为 `rg2`，然后查看绑定到当前用户的资源组：

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

`TIDB_BOUNDED_STALENESS()` 函数用于 [`AS OF TIMESTAMP`](/as-of-timestamp.md) 语法的一部分。

## TIDB_CURRENT_TSO

`TIDB_CURRENT_TSO()` 函数返回当前事务的 [TSO](/tso.md)。这类似于 [`tidb_current_ts`](/system-variables.md#tidb_current_ts) 系统变量。

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

`TIDB_DECODE_BINARY_PLAN(binary_plan)` 函数解码二进制计划，例如 [`STATEMENTS_SUMMARY`](/statement-summary-tables.md) 表的 `BINARY_PLAN` 列中的二进制计划。

必须将 [`tidb_generate_binary_plan`](/system-variables.md#tidb_generate_binary_plan-new-in-v620) 变量设置为 `ON`，二进制计划才可用。

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

`TIDB_DECODE_KEY()` 函数将 TiDB 编码的键条目解码为包含 `_tidb_rowid` 和 `table_id` 的 JSON 结构。这些编码的键存在于某些系统表和日志输出中。

在以下示例中，表 `t1` 具有由 TiDB 生成的隐藏 `rowid`。 `TIDB_DECODE_KEY()` 函数用于该语句中。 从结果中，您可以看到隐藏的 `rowid` 被解码并输出，这是非聚集主键的典型结果。

```sql
SELECT START_KEY, TIDB_DECODE_KEY(START_KEY) FROM information_schema.tikv_region_status WHERE table_name='t1' AND REGION_ID=2\G
```

```sql
*************************** 1. row ***************************
                 START_KEY: 7480000000000000FF3B5F728000000000FF1DE3F10000000000FA
TIDB_DECODE_KEY(START_KEY): {"_tidb_rowid":1958897,"table_id":"59"}
1 row in set (0.00 sec)
```

在以下示例中，表 `t2` 具有复合聚集主键。 从 JSON 输出中，您可以看到一个 `handle`，其中包含作为主键一部分的两个列的名称和值。

```sql
SHOW CREATE TABLE t2\G
```

```sql
*************************** 1. row ***************************
       Table: t2
Create Table: CREATE TABLE `t2` (
  `id` binary(36) NOT NULL,
  `a` tinyint(3) unsigned NOT NULL,
  `v` varchar(512) DEFAULT NULL,
  PRIMARY KEY (`a`,`id`) /*T![clustered_index] CLUSTERED */
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
1 row in set (0.001 sec)
```

```sql
SELECT * FROM information_schema.tikv_region_status WHERE table_name='t2' LIMIT 1\G
```

```sql
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

```sql
+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| tidb_decode_key('7480000000000000FF3E5F720400000000FF0000000601633430FF3338646232FF2D64FF3531632D3131FF65FF622D386337352DFFFF3830653635303138FFFF61396265000000FF00FB000000000000F9') |
+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| {"handle":{"a":"6","id":"c4038db2-d51c-11eb-8c75-80e65018a9be"},"table_id":62}                                                                                                        |
+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.001 sec)
```

在以下示例中，表的第一个 Region 以仅具有表的 `table_id` 的键开头。 该表的最后一个 Region 以 `table_id + 1` 结尾。 之间的任何 Region 都有更长的键，其中包括 `_tidb_rowid` 或 `handle`。

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

```sql
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

`TIDB_DECODE_KEY` 成功时返回有效的 JSON，如果解码失败，则返回参数值。

## TIDB_DECODE_PLAN

你可以在慢查询日志中找到编码形式的 TiDB 执行计划。 `TIDB_DECODE_PLAN()` 函数用于将编码后的计划解码为人类可读的形式。

此函数很有用，因为计划是在语句执行时捕获的。 在 `EXPLAIN` 中重新执行该语句可能会产生不同的结果，因为数据分布和统计信息会随着时间的推移而演变。

```sql
SELECT tidb_decode_plan('8QIYMAkzMV83CQEH8E85LjA0CWRhdGE6U2VsZWN0aW9uXzYJOTYwCXRpbWU6NzEzLjHCtXMsIGxvb3BzOjIsIGNvcF90YXNrOiB7bnVtOiAxLCBtYXg6IDU2OC41wgErRHByb2Nfa2V5czogMCwgcnBjXxEpAQwFWBAgNTQ5LglZyGNvcHJfY2FjaGVfaGl0X3JhdGlvOiAwLjAwfQkzLjk5IEtCCU4vQQoxCTFfNgkxXzAJMwm2SGx0KHRlc3QudC5hLCAxMDAwMCkNuQRrdgmiAHsFbBQzMTMuOMIBmQnEDDk2MH0BUgEEGAoyCTQzXzUFVwX1oGFibGU6dCwga2VlcCBvcmRlcjpmYWxzZSwgc3RhdHM6cHNldWRvCTk2ISE2aAAIMTUzXmYA')\G
```

```sql
*************************** 1. row ***************************
  tidb_decode_plan('8QIYMAkzMV83CQEH8E85LjA0CWRhdGE6U2VsZWN0aW9uXzYJOTYwCXRpbWU6NzEzLjHCtXMsIGxvb3BzOjIsIGNvcF90YXNrOiB7bnVtOiAxLCBtYXg6IDU2OC41wgErRHByb2Nfa2V5czogMCwgcnBjXxEpAQwFWBAgNTQ5LglZyGNvcHJfY2FjaGVfaGl0X3JhdGlvOiAwLjAwfQkzLjk5IEtCCU4vQQoxCTFfNgkxXzAJMwm2SGx0KHRlc3QudC5hLCAxMDAwMCkNuQRrdgmiAHsFbBQzMTMuOMIBmQnEDDk2MH0BUgEEGAoyCTQzXzUFVwX1oGFibGU6dCwga2VlcCBvcmRlcjpmYWxzZSwgc3RhdHM6cHNldWRvCTk2ISE2aAAIMTUzXmYA'):     id                     task         estRows    operator info                              actRows    execution info                                                                                                                         memory     disk
    TableReader_7          root         319.04     data:Selection_6                           960        time:713.1µs, loops:2, cop_task: {num: 1, max: 568.5µs, proc_keys: 0, rpc_num: 1, rpc_time: 549.1µs, copr_cache_hit_ratio: 0.00}    3.99 KB    N/A
    └─Selection_6          cop[tikv]    319.04     lt(test.t.a, 10000)                        960        tikv_task:{time:313.8µs, loops:960}                                                                                                   N/A        N/A
      └─TableFullScan_5    cop[tikv]    960        table:t, keep order:false, stats:pseudo    960        tikv_task:{time:153µs, loops:960}                                                                                                     N/A        N/A
```

## TIDB_DECODE_SQL_DIGESTS

`TIDB_DECODE_SQL_DIGESTS()` 函数用于查询集群中 SQL 摘要集合对应的规范化 SQL 语句（一种不包含格式和参数的形式）。此函数接受 1 个或 2 个参数：

* `digests`: 一个字符串。此参数的格式为 JSON 字符串数组，数组中的每个字符串都是一个 SQL 摘要。
* `stmtTruncateLength`: 一个整数（可选）。它用于限制返回结果中每个 SQL 语句的长度。如果 SQL 语句超过指定的长度，则该语句将被截断。`0` 表示长度不受限制。

此函数返回一个字符串，其格式为 JSON 字符串数组。数组中的第 *i* 项是 `digests` 参数中第 *i* 个元素对应的规范化 SQL 语句。如果 `digests` 参数中的某个元素不是有效的 SQL 摘要，或者系统无法找到相应的 SQL 语句，则返回结果中对应的项为 `null`。如果指定了截断长度 (`stmtTruncateLength > 0`)，对于返回结果中超过此长度的每个语句，将保留前 `stmtTruncateLength` 个字符，并在末尾添加 `"..."` 后缀以指示截断。如果 `digests` 参数为 `NULL`，则该函数的返回值为 `NULL`。

> **注意：**
>
> * 只有具有 [PROCESS](https://dev.mysql.com/doc/refman/8.0/en/privileges-provided.html#priv_process) 权限的用户才能使用此函数。
> * 当执行 `TIDB_DECODE_SQL_DIGESTS` 时，TiDB 会从语句摘要表中查询每个 SQL 摘要对应的语句，因此不能保证始终可以为任何 SQL 摘要找到相应的语句。只能找到在集群中执行过的语句，并且是否可以查询到这些 SQL 语句也受到语句摘要表相关配置的影响。有关语句摘要表的详细描述，请参见 [语句摘要表](/statement-summary-tables.md)。
> * 此函数开销很高。在具有大量行的查询中（例如，在大规模且繁忙的集群上查询 `information_schema.cluster_tidb_trx` 的全表），使用此函数可能会导致查询运行时间过长。请谨慎使用。
>     * 此函数开销很高，因为它每次调用时，都会在内部查询 `STATEMENTS_SUMMARY`、`STATEMENTS_SUMMARY_HISTORY`、`CLUSTER_STATEMENTS_SUMMARY` 和 `CLUSTER_STATEMENTS_SUMMARY_HISTORY` 表，并且查询涉及 `UNION` 操作。此函数目前不支持向量化，也就是说，当为多行数据调用此函数时，上述查询会为每一行单独执行。

```sql
SET @digests = '["e6f07d43b5c21db0fbb9a31feac2dc599787763393dd5acbfad80e247eb02ad5","38b03afa5debbdf0326a014dbe5012a62c51957f1982b3093e748460f8b00821","e5796985ccafe2f71126ed6c0ac939ffa015a8c0744a24b7aee6d587103fd2f7"]';

SELECT TIDB_DECODE_SQL_DIGESTS(@digests);
```

```sql
+------------------------------------+
| TIDB_DECODE_SQL_DIGESTS(@digests)  |
+------------------------------------+
| ["begin",null,"select * from `t`"] |
+------------------------------------+
1 row in set (0.00 sec)
```

在上面的示例中，参数是一个包含 3 个 SQL 摘要的 JSON 数组，相应的 SQL 语句是查询结果中的三个项。但是无法从集群中找到与第二个 SQL 摘要对应的 SQL 语句，因此结果中的第二项为 `null`。

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

上面的调用将第二个参数（即截断长度）指定为 10，并且查询结果中第三个语句的长度大于 10。因此，仅保留前 10 个字符，并在末尾添加 `"..."`，表示截断。

另请参阅：

- [语句摘要表](/statement-summary-tables.md)
- [`INFORMATION_SCHEMA.TIDB_TRX`](/information-schema/information-schema-tidb-trx.md)

## TIDB_ENCODE_SQL_DIGEST

`TIDB_ENCODE_SQL_DIGEST(query_str)` 返回查询字符串的 SQL 摘要。

在以下示例中，你可以看到两个查询都获得了相同的查询摘要，这是因为对于它们来说，摘要都将是 `select ?`。

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

`TIDB_IS_DDL_OWNER()` 函数用于判断你当前连接的实例是否为 DDL Owner，如果是则返回 `1`。

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

`TIDB_PARSE_TSO()` 函数从 TiDB TSO 时间戳中提取物理时间戳。[TSO](/tso.md) 代表时间戳预言机（Time Stamp Oracle），是由 PD (Placement Driver) 为每个事务发出的单调递增的时间戳。

TSO 是一个由两部分组成的数字：

- 一个物理时间戳
- 一个逻辑计数器

```sql
BEGIN;
SELECT TIDB_PARSE_TSO(@@tidb_current_ts);
ROLLBACK;
```

```sql
+-----------------------------------+
| TIDB_PARSE_TSO(@@tidb_current_ts) |
+-----------------------------------+
| 2021-05-26 11:33:37.776000        |
+-----------------------------------+
1 row in set (0.0012 sec)
```

这里 `TIDB_PARSE_TSO` 用于从 `tidb_current_ts` 会话变量中可用的时间戳数字中提取物理时间戳。因为时间戳是为每个事务发出的，所以此函数在事务中运行。

## TIDB_PARSE_TSO_LOGICAL

`TIDB_PARSE_TSO_LOGICAL(tso)` 函数返回 [TSO](/tso.md) 时间戳的逻辑部分。

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

`TIDB_ROW_CHECKSUM()` 函数用于查询行的校验和值。此函数只能在 FastPlan 进程中的 `SELECT` 语句中使用。也就是说，你可以通过类似 `SELECT TIDB_ROW_CHECKSUM() FROM t WHERE id = ?` 或 `SELECT TIDB_ROW_CHECKSUM() FROM t WHERE id IN (?, ?, ...)` 的语句进行查询。

要启用 TiDB 中单行数据的校验和功能（由系统变量 [`tidb_enable_row_level_checksum`](/system-variables.md#tidb_enable_row_level_checksum-new-in-v710) 控制），请运行以下语句：

```sql
SET GLOBAL tidb_enable_row_level_checksum = ON;
```

此配置仅对新创建的会话生效，因此你需要重新连接到 TiDB。

创建表 `t` 并插入数据：

```sql
USE test;
CREATE TABLE t (id INT PRIMARY KEY, k INT, c CHAR(1));
INSERT INTO t VALUES (1, 10, 'a');
```

以下语句展示了如何查询表 `t` 中 `id = 1` 的行的校验和值：

```sql
SELECT *, TIDB_ROW_CHECKSUM() FROM t WHERE id = 1;
```

输出如下：

```sql
+----+------+------+---------------------+
| id | k    | c    | TIDB_ROW_CHECKSUM() |
+----+------+------+---------------------+
|  1 |   10 | a    | 3813955661          |
+----+------+------+---------------------+
1 row in set (0.000 sec)
```

## TIDB_SHARD

`TIDB_SHARD()` 函数用于创建 shard 索引，以分散索引热点。shard 索引是以 `TIDB_SHARD()` 函数为前缀的表达式索引。

- 创建：

    要为索引字段 `a` 创建 shard 索引，可以使用 `uk((tidb_shard(a)), a))`。当唯一二级索引 `uk((tidb_shard(a)), a))` 中的索引字段 `a` 上存在由单调递增或递减数据引起的热点时，索引的前缀 `tidb_shard(a)` 可以分散热点，从而提高集群的可扩展性。

- 场景：

    - 唯一二级索引上存在由单调递增或递减的键引起的写入热点，并且该索引包含整数类型字段。
    - SQL 语句基于二级索引的所有字段执行等值查询，无论是单独的 `SELECT` 还是由 `UPDATE`、`DELETE` 等生成的内部查询。等值查询包括两种方式：`a = 1` 或 `a IN (1, 2, ......)`。

- 限制：

    - 不能用于不等值查询。
    - 不能用于包含 `OR` 且与最外层 `AND` 运算符混合的查询。
    - 不能用于 `GROUP BY` 子句。
    - 不能用于 `ORDER BY` 子句。
    - 不能用于 `ON` 子句。
    - 不能用于 `WHERE` 子查询。
    - 只能用于分散整数字段的唯一索引。
    - 可能在复合索引中不起作用。
    - 不能通过 FastPlan 过程，这会影响优化器性能。
    - 不能用于准备执行计划缓存。

以下示例展示了如何使用 `TIDB_SHARD()` 函数。

- 使用 `TIDB_SHARD()` 函数计算 SHARD 值。

    以下语句展示了如何使用 `TIDB_SHARD()` 函数计算 `12373743746` 的 SHARD 值：

    ```sql
    SELECT TIDB_SHARD(12373743746);
    ```

- SHARD 值为：

    ```sql
    +-------------------------+
    | TIDB_SHARD(12373743746) |
    +-------------------------+
    |                     184 |
    +-------------------------+
    1 row in set (0.00 sec)
    ```

- 使用 `TIDB_SHARD()` 函数创建 shard 索引：

    ```sql
    CREATE TABLE test(id INT PRIMARY KEY CLUSTERED, a INT, b INT, UNIQUE KEY uk((tidb_shard(a)), a));
    ```

## TIDB_VERSION

`TIDB_VERSION()` 函数用于获取你所连接的 TiDB 服务器的版本和构建详情。你可以在 GitHub 上报告问题时使用此函数。

```sql
SELECT TIDB_VERSION()\G
```

```sql
*************************** 1. row ***************************
TIDB_VERSION(): Release Version: v8.1.2
Edition: Community
Git Commit Hash: 821e491a20fbab36604b36b647b5bae26a2c1418
Git Branch: HEAD
UTC Build Time: 2024-12-26 19:16:25
GoVersion: go1.21.10
Race Enabled: false
Check Table Before Drop: false
Store: tikv
1 row in set (0.00 sec)
```

## VITESS_HASH

`VITESS_HASH(num)` 函数用于以与 Vitess 相同的方式哈希一个数字。这有助于从 Vitess 迁移到 TiDB。

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