---
title: TiDB 特有的函数
summary: 学习使用 TiDB 特有的函数。
---

# TiDB 特有的函数

以下函数为 TiDB 中特有的函数，与 MySQL 不兼容：

| 函数名 | 函数说明 |
| :-------------- | :------------------------------------- |
| `TIDB_BOUNDED_STALENESS()` |  `TIDB_BOUNDED_STALENESS` 函数指示 TiDB 在指定时间范围内读取尽可能新的数据。参见[使用 AS OF TIMESTAMP 语法读取历史数据](/as-of-timestamp.md)。 |
| [`TIDB_DECODE_KEY(str)`](#tidb_decode_key) | `TIDB_DECODE_KEY` 函数用于将 TiDB 编码的键输入解码为包含 `_tidb_rowid` 和 `table_id` 的 JSON 结构。你可以在一些系统表和日志输出中找到 TiDB 的编码键。 |
| [`TIDB_DECODE_PLAN(str)`](#tidb_decode_plan) | `TIDB_DECODE_PLAN` 函数用于解码 TiDB 执行计划。 |
| `TIDB_IS_DDL_OWNER()` | `TIDB_IS_DDL_OWNER` 函数用于检查你连接的 TiDB 实例是否是 DDL Owner。DDL Owner 代表集群中所有其他节点执行 DDL 语句的 TiDB 实例。 |
| [`TIDB_PARSE_TSO(num)`](#tidb_parse_tso) | `TIDB_PARSE_TSO` 函数用于从 TiDB TSO 时间戳中提取物理时间戳。参见 [`tidb_current_ts`](/system-variables.md#tidb_current_ts)。 |
| `TIDB_PARSE_TSO_LOGICAL(num)` | `TIDB_PARSE_TSO_LOGICAL` 函数用于从 TiDB TSO 时间戳中提取逻辑时间戳。|
| [`TIDB_VERSION()`](#tidb_version) | `TIDB_VERSION` 函数用于获取当前连接的 TiDB 服务器版本和构建详细信息。 |
| [`TIDB_DECODE_SQL_DIGESTS(digests, stmtTruncateLength)`](#tidb_decode_sql_digests) | `TIDB_DECODE_SQL_DIGESTS` 函数用于在集群中查询一组 SQL Digest 所对应的 SQL 语句的归一化形式（即去除格式和参数后的形式）。 |
| `VITESS_HASH(str)` |  `VITESS_HASH` 函数返回与 Vitess 的 `HASH` 函数兼容的字符串哈希值，有助于从 Vitess 迁移数据。 |
| `TIDB_SHARD()` | `TIDB_SHARD` 函数用于创建一个 SHARD INDEX 来打散热点索引。SHARD INDEX 是一种以 `TIDB_SHARD` 函数为前缀的表达式索引。 |
| `TIDB_ROW_CHECKSUM()` | `TIDB_ROW_CHECKSUM()` 函数用于查询行数据的 Checksum 值。该函数只能用于 FastPlan 流程的 `SELECT` 语句，即你可通过形如 `SELECT TIDB_ROW_CHECKSUM() FROM t WHERE id = ?` 或 `SELECT TIDB_ROW_CHECKSUM() FROM t WHERE id IN (?, ?, ...)` 的语句进行查询。参见[数据正确性校验](/ticdc/ticdc-integrity-check.md)。 |
| `CURRENT_RESOURCE_GROUP()` | `CURRENT_RESOURCE_GROUP()` 用于查询当前连接绑定的资源组名。参见[使用资源管控 (Resource Control) 实现资源隔离](/tidb-resource-control.md)。 |

## 示例

下面为部分以上函数的示例。

### TIDB_DECODE_KEY

`TIDB_DECODE_KEY` 函数用于将 TiDB 编码的键输入解码为包含 `_tidb_rowid` 和 `table_id` 的 JSON 结构。你可以在一些系统表和日志输出中找到 TiDB 的编码键。

以下示例中，表 `t1` 有一个隐藏的 `rowid`，该 `rowid` 由 TiDB 生成。语句中使用了 `TIDB_DECODE_KEY` 函数。结果显示，隐藏的 `rowid` 被解码后并输出，这是典型的非聚簇主键结果。

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

`TIDB_DECODE_KEY` 在解码成功时返回有效的 JSON，在解码失败时返回传入的参数值。

### TIDB_DECODE_PLAN

你可以在慢查询日志中找到编码形式的 TiDB 执行计划，然后使用 `TIDB_DECODE_PLAN()` 函数将编码的执行计划解码为易读的形式。

该函数很有用，因为在执行语句时 TiDB 会捕获执行计划。重新执行 `EXPLAIN` 中的语句可能会产生不同的结果，因为数据分布和统计数据会随着时间的推移而变化。

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

### TIDB_PARSE_TSO

`TIDB_PARSE_TSO` 函数用于从 TiDB TSO 时间戳中提取物理时间戳。

TSO 指 Time Stamp Oracle，是 PD (Placement Driver) 为每个事务提供的单调递增的时间戳。TSO 是一串数字，包含以下两部分：

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

以上示例使用 `TIDB_PARSE_TSO` 函数从 `tidb_current_ts` 会话变量提供的可用时间戳编号中提取物理时间戳。因为每个事务都会分配到时间戳，所以此函数在事务中运行。

### TIDB_VERSION

`TIDB_VERSION` 函数用于获取当前连接的 TiDB 服务器版本和构建详细信息。向 GitHub 上提交 issue 时，你可使用此函数获取相关信息。

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

### TIDB_DECODE_SQL_DIGESTS

`TIDB_DECODE_SQL_DIGESTS()` 函数用于在集群中查询一组 SQL Digest 所对应的 SQL 语句的归一化形式（即去除格式和参数后的形式）。函数接受 1 个或 2 个参数：

* `digests`：字符串类型，该参数应符合 JSON 字符串数组的格式，数组中的每个字符串应为一个 SQL Digest。
* `stmtTruncateLength`：可选参数，整数类型，用来限制返回结果中每条 SQL 语句的长度，超过指定的长度会被截断。0 表示不限制长度。

返回一个字符串，符合 JSON 字符串数组的格式，数组中的第 *i* 项为参数 `digests` 中的第 *i* 个元素所对应的语句。如果参数 `digests` 中的某一项不是一个有效的 SQL Digest 或系统无法查询到其对应的 SQL 语句，则返回结果中对应项为 `null`。如果指定了截断长度（`stmtTruncateLength > 0`），则返回结果中每条超过该长度的语句，保留前 `stmtTruncateLength` 个字符，并在尾部增加 `"..."` 后缀表示发生了截断。如果参数 `digests` 为 `NULL`，则函数的返回值为 `NULL`。

> **注意：**
>
> * 仅持有 [PROCESS](https://dev.mysql.com/doc/refman/8.0/en/privileges-provided.html#priv_process) 权限的用户可以使用该函数。
> * `TIDB_DECODE_SQL_DIGESTS` 执行时，TiDB 内部从 Statement Summary 一系列表中查询每个 SQL Digest 所对应的语句，因而并不能保证对任意 SQL Digest 都总是能查询到对应的语句，只有在集群中执行过的语句才有可能被查询到，且是否能查询到受 Statement Summary 表相关配置的影响。有关 Statement Summary 表的详细说明，参见 [Statement Summary Tables](/statement-summary-tables.md)。
> * 该函数开销较大，在行数很多的查询中（比如在规模较大、比较繁忙的集群上查询 `information_schema.cluster_tidb_trx` 全表时）直接使用该函数可能导致查询运行时间较长。请谨慎使用。
>     * 该函数开销大的原因是，其每次被调用时，都会在内部发起对 `STATEMENTS_SUMMARY`、`STATEMENTS_SUMMARY_HISTORY`、`CLUSTER_STATEMENTS_SUMMARY` 和 `CLUSTER_STATEMENTS_SUMMARY_HISTORY` 这几张表的查询，且其中涉及 `UNION` 操作。且该函数目前不支持向量化，即对于多行数据调用该函数时，对每行都会独立进行一次上述的查询。

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

上述调用指定了第二个参数（即截断长度）为 10，而查询结果中的第三条语句的长度大于 10，因而仅保留了前 10 个字符，并在尾部添加了 `"..."` 表示发生了截断。

另请参阅：

- [`Statement Summary Tables`](/statement-summary-tables.md)
- [`INFORMATION_SCHEMA.TIDB_TRX`](/information-schema/information-schema-tidb-trx.md)

### TIDB_SHARD

`TIDB_SHARD` 函数用于创建一个 SHARD INDEX 来打散热点索引。SHARD INDEX 是一种以 `TIDB_SHARD` 函数为前缀的表达式索引。

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

`TIDB_SHARD` 函数的使用示例如下：

- 使用 `TIDB_SHARD` 函数计算 SHARD 值

    以下示例说明如何使用 `TIDB_SHARD` 函数计算 `12373743746` 的 SHARD 值。

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

- 使用 `TIDB_SHARD` 函数创建 SHARD INDEX

    ```sql
    CREATE TABLE test(id INT PRIMARY KEY CLUSTERED, a INT, b INT, UNIQUE KEY uk((tidb_shard(a)), a));
    ```

### TIDB_ROW_CHECKSUM

`TIDB_ROW_CHECKSUM` 函数用于查询行数据的 Checksum 值。该函数只能用于 FastPlan 流程的 `SELECT` 语句，即你可通过形如 `SELECT TIDB_ROW_CHECKSUM() FROM t WHERE id = ?` 或 `SELECT TIDB_ROW_CHECKSUM() FROM t WHERE id IN (?, ?, ...)` 的语句进行查询。

在 TiDB 中开启行数据 Checksum 功能 [`tidb_enable_row_level_checksum`](/system-variables.md#tidb_enable_row_level_checksum-从-v710-版本开始引入)：

```sql
SET GLOBAL tidb_enable_row_level_checksum = ON;
```

创建表 `t` 并插入数据：

```sql
USE test;
CREATE TABLE t (id INT PRIMARY KEY, k INT, c int);
INSERT INTO TABLE t values (1, 10, a);
```

查询表 `t` 中 `id = 1` 的行数据的 Checksum 值：

```sql
SELECT *, TIDB_ROW_CHECKSUM() FROM t WHERE id = 1;
```

输出结果如下：

```sql
+----+------+------+---------------------+
| id | k    | c    | TIDB_ROW_CHECKSUM() |
+----+------+------+---------------------+
|  1 |   10 | a    | 3813955661          |
+----+------+------+---------------------+
1 row in set (0.000 sec)
```

### CURRENT_RESOURCE_GROUP

`CURRENT_RESOURCE_GROUP` 函数用于查询当前连接绑定的资源组名称。当开启[资源管控 (Resource Control)](/tidb-resource-control.md) 功能时，执行 SQL 语句对资源的占用会受到所绑定的资源组资源配置的限制。

在会话建立时，TiDB 默认会将连接绑定至登录用户绑定的资源组，如果用户没有绑定任何资源组，则会将连接绑定至 `default` 资源组。在会话建立之后，绑定的资源组默认不会发生变化，即使执行了[修改用户绑定的资源组](/sql-statements/sql-statement-alter-user.md#修改用户绑定的资源组)。如需修改当前会话绑定的资源组，可以使用 [`SET RESOURCE GROUP`](/sql-statements/sql-statement-set-resource-group.md) 语句。

#### 示例

创建一个用户 `user1`，创建两个资源组 `rg1` 和 `rg2`，并将用户 `user1` 绑定资源组 `rg1`：

```sql
CREATE USER 'user1';
CREATE RESOURCE GROUP 'rg1' RU_PER_SEC = 1000;
CREATE RESOURCE GROUP 'rg2' RU_PER_SEC = 2000;
ALTER USER 'user1' RESOURCE GROUP `rg1`;
```

使用 `user1` 登录，查看当前用户绑定的资源组：

```sql
SELECT CURRENT_RESOURCE_GROUP();
```

```sql
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

```sql
+--------------------------+
| CURRENT_RESOURCE_GROUP() |
+--------------------------+
| rg2                      |
+--------------------------+
1 row in set (0.00 sec)
```
