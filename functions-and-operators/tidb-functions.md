---
title: TiDB 特有的函数
summary: 学习使用 TiDB 特有的函数。
---

# TiDB 特有的函数

本文档介绍 TiDB 特有的函数。

## TIDB_BOUNDED_STALENESS

`TIDB_BOUNDED_STALENESS` 是 TiDB 的内部函数，用于指定一个时间范围。用法为 `TIDB_BOUNDED_STALENESS(t1, t2)`，其中 t1 和 t2 为时间范围的两端，支持使用日期时间和时间函数。

使用该函数，TiDB 会在指定的时间范围内选择一个合适的时间戳，该时间戳能保证所访问的副本上不存在开始于这个时间戳之前且还没有提交的相关事务，即能保证所访问的可用副本上执行读取操作而且不会被阻塞。

## TIDB_DECODE_KEY

`TIDB_DECODE_KEY` 函数用于将 TiDB 编码的键输入解码为包含 `_tidb_rowid` 和 `table_id` 的 JSON 结构。你可以在一些系统表和日志输出中找到 TiDB 的编码键。

### 语法图

```ebnf+diagram
TableStmt ::=
    "TIDB_DECODE_KEY(" STR ")"
```

### 示例

以下示例中，表 `t1` 有一个隐藏的 `rowid`，该 `rowid` 由 TiDB 生成。语句中使用了 `TIDB_DECODE_KEY` 函数。结果显示，隐藏的 `rowid` 被解码后并输出，这是典型的非聚簇主键结果。

{{< copyable "sql" >}}

```sql
SELECT START_KEY, TIDB_DECODE_KEY(START_KEY) FROM information_schema.tikv_region_status WHERE table_name='t1' AND REGION_ID=2\G
```

```sql
*************************** 1. row ***************************
                 START_KEY: 7480000000000000FF3B5F728000000000FF1DE3F10000000000FA
TIDB_DECODE_KEY(START_KEY): {"_tidb_rowid":1958897,"table_id":"59"}
1 row in set (0.00 sec)
```

以下示例中，表 `t2` 有一个复合聚簇主键。由 JSON 输出可知，输出结果的 `handle` 项中包含了主键部分两列的信息，即两列的名称和对应的值。

{{< copyable "sql" >}}

```sql
show create table t2\G
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

{{< copyable "sql" >}}

```sql
select * from information_schema.tikv_region_status where table_name='t2' limit 1\G
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

{{< copyable "sql" >}}

```sql
select tidb_decode_key('7480000000000000FF3E5F720400000000FF0000000601633430FF3338646232FF2D64FF3531632D3131FF65FF622D386337352DFFFF3830653635303138FFFF61396265000000FF00FB000000000000F9');
```

```sql
+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| tidb_decode_key('7480000000000000FF3E5F720400000000FF0000000601633430FF3338646232FF2D64FF3531632D3131FF65FF622D386337352DFFFF3830653635303138FFFF61396265000000FF00FB000000000000F9') |
+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| {"handle":{"a":"6","id":"c4038db2-d51c-11eb-8c75-80e65018a9be"},"table_id":62}                                                                                                        |
+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.001 sec)
```

### MySQL 兼容性

`TIDB_DECODE_KEY` 是 TiDB 特有的函数，和 MySQL 不兼容。

## TIDB_DECODE_PLAN

`TIDB_DECODE_PLAN` 函数用于解码 TiDB 执行计划。你可以在慢查询日志中找到 TiDB 执行计划。

### 语法图

```ebnf+diagram
TableStmt ::=
    "TIDB_DECODE_PLAN(" STR ")"
```

### 示例

{{< copyable "sql" >}}

```sql
SELECT tidb_decode_plan('8QIYMAkzMV83CQEH8E85LjA0CWRhdGE6U2VsZWN0aW9uXzYJOTYwCXRpbWU6NzEzLjHCtXMsIGxvb3BzOjIsIGNvcF90YXNrOiB7bnVtOiAxLCBtYXg6IDU2OC41wgErRHByb2Nfa2V5czogMCwgcnBjXxEpAQwFWBAgNTQ5LglZyGNvcHJfY2FjaGVfaGl0X3JhdGlvOiAwLjAwfQkzLjk5IEtCCU4vQQoxCTFfNgkxXzAJMwm2SGx0KHRlc3QudC5hLCAxMDAwMCkNuQRrdgmiAHsFbBQzMTMuOMIBmQnEDDk2MH0BUgEEGAoyCTQzXzUFVwX1oGFibGU6dCwga2VlcCBvcmRlcjpmYWxzZSwgc3RhdHM6cHNldWRvCTk2ISE2aAAIMTUzXmYA')\G
```

```sql
*************************** 1. row ***************************
  tidb_decode_plan('8QIYMAkzMV83CQEH8E85LjA0CWRhdGE6U2VsZWN0aW9uXzYJOTYwCXRpbWU6NzEzLjHCtXMsIGxvb3BzOjIsIGNvcF90YXNrOiB7bnVtOiAxLCBtYXg6IDU2OC41wgErRHByb2Nfa2V5czogMCwgcnBjXxEpAQwFWBAgNTQ5LglZyGNvcHJfY2FjaGVfaGl0X3JhdGlvOiAwLjAwfQkzLjk5IEtCCU4vQQoxCTFfNgkxXz:     id                     task         estRows    operator info                              actRows    execution info                                                                                                                         memory     disk
    TableReader_7          root         319.04     data:Selection_6                           960        time:713.1µs, loops:2, cop_task: {num: 1, max: 568.5µs, proc_keys: 0, rpc_num: 1, rpc_time: 549.1µs, copr_cache_hit_ratio: 0.00}    3.99 KB    N/A
    └─Selection_6          cop[tikv]    319.04     lt(test.t.a, 10000)                        960        tikv_task:{time:313.8µs, loops:960}                                                                                                   N/A        N/A
      └─TableFullScan_5    cop[tikv]    960        table:t, keep order:false, stats:pseudo    960        tikv_task:{time:153µs, loops:960}                                                                                                     N/A        N/A
```

### MySQL 兼容性

`TIDB_DECODE_PLAN` 是 TiDB 特有的函数，和 MySQL 不兼容。

## TIDB_IS_DDL_OWNER

`TIDB_IS_DDL_OWNER` 函数用于检查你连接的 TiDB 实例是否是 DDL Owner。DDL Owner 代表集群中所有其他节点执行 DDL 语句的 TiDB 实例。

### 语法图

```ebnf+diagram
TableStmt ::=
    "TIDB_IS_DDL_OWNER())"
```

### 示例

{{< copyable "sql" >}}

```sql
SELECT tidb_is_ddl_owner();
```

```sql
+---------------------+
| tidb_is_ddl_owner() |
+---------------------+
|                   1 |
+---------------------+
1 row in set (0.00 sec)
```

### MySQL 兼容性

`TIDB_IS_DDL_OWNER` 是 TiDB 特有的函数，和 MySQL 不兼容。

### 另请参阅

- [ADMIN SHOW DDL](/sql-statements/sql-statement-admin-show-ddl.md)
- [ADMIN CANCEL DDL](/sql-statements/sql-statement-admin-cancel-ddl.md)

## TIDB_PARSE_TSO

`TIDB_PARSE_TSO` 函数用于从 TiDB TSO 时间戳中提取物理时间戳。

TSO 指 Time Stamp Oracle，是 PD (Placement Driver) 为每个事务提供的单调递增的时间戳。

TSO 是一串数字，包含以下两部分：

- 一个物理时间戳
- 一个逻辑计数器

### 语法图

```ebnf+diagram
TableStmt ::=
    "TIDB_PARSE_TSO(" NUM ")"
```

### 示例

{{< copyable "sql" >}}

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

以上示例使用 `TIDB_PARSE_TSO` 函数从 `tidb_current_ts` 会话变量提供的可用时间戳编号中提取物理时间戳。因为每个事务都会分配到时间戳，所以此函数在事务中运行。

### MySQL 兼容性

`TIDB_PARSE_TSO` 是 TiDB 特有的函数，和 MySQL 不兼容。

### 另请参阅

- [`tidb_current_ts`](/system-variables.md#tidb_current_ts)

## TIDB_VERSION

`TIDB_VERSION` 函数用于获取当前连接的 TiDB 服务器版本和构建详细信息。向 GitHub 上提交 issue 时，你可使用此函数获取相关信息。

### 语法图

```ebnf+diagram
TableStmt ::=
    "TIDB_VERSION()"
```

### 示例

{{< copyable "sql" >}}

```sql
SELECT TIDB_VERSION()\G
```

```sql
*************************** 1. row ***************************
TIDB_VERSION(): Release Version: v5.1.0-alpha-13-gd5e0ed0aa-dirty
Edition: Community
Git Commit Hash: d5e0ed0aaed72d2f2dfe24e9deec31cb6cb5fdf0
Git Branch: master
UTC Build Time: 2021-05-24 14:39:20
GoVersion: go1.13
Race Enabled: false
TiKV Min Version: v3.0.0-60965b006877ca7234adaced7890d7b029ed1306
Check Table Before Drop: false
1 row in set (0.00 sec)
```

### MySQL 兼容性

`TIDB_VERSION` 是 TiDB 特有的函数，和 MySQL 不兼容。如果要求兼容 MySQL，可以使用 `VERSION` 获取版本信息，但结果不包含详细的构建信息。

## TIDB_DECODE_SQL_DIGESTS

`TIDB_DECODE_SQL_DIGESTS` 函数用于在集群中查询一组 SQL Digest 所对应的 SQL 语句的归一化形式（即去除格式和参数后的形式）。函数接受 1 个或 2 个参数：

* `digests`：字符串类型，该参数应符合 JSON 字符串数组的格式，数组中的每个字符串应为一个 SQL Digest。
* `stmtTruncateLength`：可选参数，整数类型，用来限制返回结果中每条 SQL 语句的长度，超过指定的长度会被截断。0 表示不限制长度。

返回一个字符串，符合 JSON 字符串数组的格式，数组中的第 *i* 项为参数 `digests` 中的第 *i* 个元素所对应的语句。如果参数 `digests` 中的某一项不是一个有效的 SQL Digest 或系统无法查询到其对应的 SQL 语句，则返回结果中对应项为 `null`。如果指定了截断长度（`stmtTruncateLength > 0`），则返回结果中每条超过该长度的语句，保留前 `stmtTruncateLength` 个字符，并在尾部增加 `"..."` 后缀表示发生了截断。如果参数 `digests` 为 `NULL`，则函数的返回值为 `NULL`。

> **注意：**
>
> * 仅持有 [PROCESS](https://dev.mysql.com/doc/refman/8.0/en/privileges-provided.html#priv_process) 权限的用户可以使用该函数。
> * `TIDB_DECODE_SQL_DIGESTS` 执行时，内部从 Statement Summary 一系列表中查询每个 SQL Digest 所对应的语句，因而并不能保证对任意 SQL Digest 都总是能查询到对应的语句，只有在集群中执行过的语句才有可能被查询到，且是否能查询到受 Statement Summary 表相关配置的影响。有关 Statement Summary 表的详细说明，参见 [Statement Summary Tables](/statement-summary-tables.md)。
> 该函数开销较大，在行数很多的查询中（比如在规模较大、比较繁忙的集群上查询 `information_schema.cluster_tidb_trx` 全表时）直接使用该函数可能导致查询运行时间较长。请谨慎使用。

### 语法图

```ebnf+diagram
DecodeSQLDigestsExpr ::=
    "TIDB_DECODE_SQL_DIGESTS" "(" digests ( "," stmtTruncateLength )? ")"
```

### 示例

{{< copyable "sql" >}}

```sql
set @digests = '["e6f07d43b5c21db0fbb9a31feac2dc599787763393dd5acbfad80e247eb02ad5","38b03afa5debbdf0326a014dbe5012a62c51957f1982b3093e748460f8b00821","e5796985ccafe2f71126ed6c0ac939ffa015a8c0744a24b7aee6d587103fd2f7"]';

select tidb_decode_sql_digests(@digests);
```

```sql
+------------------------------------+
| tidb_decode_sql_digests(@digests)  |
+------------------------------------+
| ["begin",null,"select * from `t`"] |
+------------------------------------+
1 row in set (0.00 sec)
```

上面的例子中，参数是一个包含 3 个 SQL Digest 的 JSON 数组，其对应的 SQL 语句分别为查询结果中给出的三项。但是其中第二条 SQL Digest 所对应的 SQL 语句未能从集群中找到，因而结果中的第二项为 `null`。

{{< copyable "sql" >}}

```sql
select tidb_decode_sql_digests(@digests, 10);
```

```sql
+---------------------------------------+
| tidb_decode_sql_digests(@digests, 10) |
+---------------------------------------+
| ["begin",null,"select * f..."]        |
+---------------------------------------+
1 row in set (0.01 sec)
```

上述调用指定了第二个参数（即阶段长度）为 10，而查询结果中的第三条语句的长度大于 10，因而仅保留了前 10 个字符，并在尾部添加了 `"..."` 表示发生了截断。

### MySQL 兼容性

`TIDB_DECODE_SQL_DIGESTS` 是 TiDB 特有的函数，和 MySQL 不兼容。

### 另请参阅

- [`Statement Summary Tables`](/statement-summary-tables.md)
- [`INFORMATION_SCHEMA.TIDB_TRX`](/information-schema/information-schema-tidb-trx.md)
