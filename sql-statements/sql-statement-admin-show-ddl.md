---
title: ADMIN SHOW DDL [JOBS|JOB QUERIES] | TiDB SQL 语句参考
summary: TiDB 数据库中 ADMIN 使用概览。
---

# ADMIN SHOW DDL [JOBS|JOB QUERIES]

`ADMIN SHOW DDL [JOBS|JOB QUERIES]` 语句显示正在运行和最近完成的 DDL 作业的信息。

## 语法图

```ebnf+diagram
AdminShowDDLStmt ::=
    'ADMIN' 'SHOW' 'DDL'
    ( 
        'JOBS' Int64Num? WhereClauseOptional 
    |   'JOB' 'QUERIES' NumList 
    |   'JOB' 'QUERIES' 'LIMIT' m ( ('OFFSET' | ',') n )?
    )?

NumList ::=
    Int64Num ( ',' Int64Num )*

WhereClauseOptional ::=
    WhereClause?
```

## 示例

### `ADMIN SHOW DDL`

要查看当前正在运行的 DDL 作业的状态，使用 `ADMIN SHOW DDL`。输出包括当前的 schema 版本、owner 的 DDL ID 和地址、正在运行的 DDL 作业和 SQL 语句，以及当前 TiDB 实例的 DDL ID。返回结果字段说明如下：

- `SCHEMA_VER`：表示 schema 的版本号。
- `OWNER_ID`：DDL owner 的 UUID。另请参阅 [`TIDB_IS_DDL_OWNER()`](/functions-and-operators/tidb-functions.md)。
- `OWNER_ADDRESS`：DDL owner 的 IP 地址。
- `RUNNING_JOBS`：正在运行的 DDL 作业的详细信息。
- `SELF_ID`：当前连接的 TiDB 节点的 UUID。如果 `SELF_ID` 与 `OWNER_ID` 相同，表示你当前连接的是 DDL owner。
- `QUERY`：查询的语句。

```sql
ADMIN SHOW DDL\G;
```

```sql
*************************** 1. row ***************************
   SCHEMA_VER: 26
     OWNER_ID: 2d1982af-fa63-43ad-a3d5-73710683cc63
OWNER_ADDRESS: 0.0.0.0:4000
 RUNNING_JOBS: 
      SELF_ID: 2d1982af-fa63-43ad-a3d5-73710683cc63
        QUERY: 
1 row in set (0.00 sec)
```

### `ADMIN SHOW DDL JOBS`

`ADMIN SHOW DDL JOBS` 语句用于查看当前 DDL 作业队列中的所有结果，包括正在运行和排队的任务，以及已完成的 DDL 作业队列中的最新十个结果。返回结果字段说明如下：

- `JOB_ID`：每个 DDL 操作对应一个 DDL 作业。`JOB_ID` 是全局唯一的。
- `DB_NAME`：执行 DDL 操作的数据库名称。
- `TABLE_NAME`：执行 DDL 操作的表名。
- `JOB_TYPE`：DDL 操作的类型。常见的作业类型包括：
    - `create schema`：用于 [`CREATE SCHEMA`](/sql-statements/sql-statement-create-database.md) 操作。
    - `create table`：用于 [`CREATE TABLE`](/sql-statements/sql-statement-create-table.md) 操作。
    - `create view`：用于 [`CREATE VIEW`](/sql-statements/sql-statement-create-view.md) 操作。
    - `ingest`：使用由 [`tidb_ddl_enable_fast_reorg`](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630) 配置的加速索引回填。
    - `txn`：基本事务回填。
    - `add index /* txn-merge */`：使用临时索引的事务回填，该索引在回填完成后与原始索引合并。
- `SCHEMA_STATE`：DDL 操作的 schema 对象的当前状态。如果 `JOB_TYPE` 是 `ADD INDEX`，则是索引的状态；如果是 `ADD COLUMN`，则是列的状态；如果是 `CREATE TABLE`，则是表的状态。常见状态包括：
    - `none`：表示不存在。通常在 `DROP` 操作之后或 `CREATE` 操作失败并回滚后，会变成 `none` 状态。
    - `delete only`、`write only`、`delete reorganization`、`write reorganization`：这四个状态是中间状态。有关它们的具体含义，请参阅[TiDB 中在线 DDL 异步变更的工作原理](/ddl-introduction.md#tidb-中在线-ddl-异步变更的工作原理)。由于中间状态转换很快，这些状态在操作过程中通常不可见。只有在执行 `ADD INDEX` 操作时才能看到 `write reorganization` 状态，表示正在添加索引数据。
    - `public`：表示存在且可供用户使用。通常在 `CREATE TABLE` 和 `ADD INDEX`（或 `ADD COLUMN`）操作完成后，会变成 `public` 状态，表示新创建的表、列和索引可以正常读写。
- `SCHEMA_ID`：执行 DDL 操作的数据库的 ID。
- `TABLE_ID`：执行 DDL 操作的表的 ID。
- `ROW_COUNT`：执行 `ADD INDEX` 操作时，表示已添加的数据行数。
- `CREATE_TIME`：DDL 操作的创建时间。
- `START_TIME`：DDL 操作的开始时间。
- `END_TIME`：DDL 操作的结束时间。
- `STATE`：DDL 操作的状态。常见状态包括：
    - `none`：表示操作尚未开始。
    - `queueing`：表示操作作业已进入 DDL 作业队列但尚未执行，因为它仍在等待早期的 DDL 作业完成。另一个原因可能是执行 `DROP` 操作后，`queueing` 状态会变成 `done` 状态，但很快会更新为 `synced` 状态，表示所有 TiDB 实例都已同步到该状态。
    - `running`：表示正在执行操作。
    - `synced`：表示操作已成功执行，所有 TiDB 实例都已同步到此状态。
    - `rollback done`：表示操作失败且回滚已完成。
    - `rollingback`：表示操作失败且正在回滚。
    - `cancelling`：表示正在取消操作。此状态仅在使用 [`ADMIN CANCEL DDL JOBS`](/sql-statements/sql-statement-admin-cancel-ddl.md) 命令取消 DDL 作业时出现。
    - `cancelled`：表示操作已被取消。
    - `pausing`：表示正在暂停操作。
    - `paused`：表示操作已暂停。此状态仅在使用 [`ADMIN PAUSED DDL JOBS`](/sql-statements/sql-statement-admin-pause-ddl.md) 命令暂停 DDL 作业时出现。你可以使用 [`ADMIN RESUME DDL JOBS`](/sql-statements/sql-statement-admin-resume-ddl.md) 命令恢复 DDL 作业。
    - `done`：表示操作已在 TiDB owner 节点上成功执行，但其他 TiDB 节点尚未同步此 DDL 作业执行的更改。

以下示例显示 `ADMIN SHOW DDL JOBS` 的结果：

```sql
ADMIN SHOW DDL JOBS;
```

```sql
mysql> ADMIN SHOW DDL JOBS;
+--------+---------+--------------------+--------------+----------------------+-----------+----------+-----------+-----------------------------------------------------------------+---------+
| JOB_ID | DB_NAME | TABLE_NAME         | JOB_TYPE     | SCHEMA_STATE         | SCHEMA_ID | TABLE_ID | ROW_COUNT | CREATE_TIME         | START_TIME          | END_TIME            | STATE   |
+--------+---------+--------------------+--------------+----------------------+-----------+----------+-----------+---------------------+-------------------------------------------+---------+
|     59 | test    | t1                 | add index    | write reorganization |         1 |       55 |     88576 | 2020-08-17 07:51:58 | 2020-08-17 07:51:58 | NULL                | running |
|     60 | test    | t2                 | add index    | none                 |         1 |       57 |         0 | 2020-08-17 07:51:59 | 2020-08-17 07:51:59 | NULL                | none    |
|     58 | test    | t2                 | create table | public               |         1 |       57 |         0 | 2020-08-17 07:41:28 | 2020-08-17 07:41:28 | 2020-08-17 07:41:28 | synced  |
|     56 | test    | t1                 | create table | public               |         1 |       55 |         0 | 2020-08-17 07:41:02 | 2020-08-17 07:41:02 | 2020-08-17 07:41:02 | synced  |
|     54 | test    | t1                 | drop table   | none                 |         1 |       50 |         0 | 2020-08-17 07:41:02 | 2020-08-17 07:41:02 | 2020-08-17 07:41:02 | synced  |
|     53 | test    | t1                 | drop index   | none                 |         1 |       50 |         0 | 2020-08-17 07:35:44 | 2020-08-17 07:35:44 | 2020-08-17 07:35:44 | synced  |
|     52 | test    | t1                 | add index    | public               |         1 |       50 |    451010 | 2020-08-17 07:34:43 | 2020-08-17 07:34:43 | 2020-08-17 07:35:16 | synced  |
|     51 | test    | t1                 | create table | public               |         1 |       50 |         0 | 2020-08-17 07:34:02 | 2020-08-17 07:34:02 | 2020-08-17 07:34:02 | synced  |
|     49 | test    | t1                 | drop table   | none                 |         1 |       47 |         0 | 2020-08-17 07:34:02 | 2020-08-17 07:34:02 | 2020-08-17 07:34:02 | synced  |
|     48 | test    | t1                 | create table | public               |         1 |       47 |         0 | 2020-08-17 07:33:37 | 2020-08-17 07:33:37 | 2020-08-17 07:33:37 | synced  |
|     46 | mysql   | stats_extended     | create table | public               |         3 |       45 |         0 | 2020-08-17 06:42:38 | 2020-08-17 06:42:38 | 2020-08-17 06:42:38 | synced  |
|     44 | mysql   | opt_rule_blacklist | create table | public               |         3 |       43 |         0 | 2020-08-17 06:42:38 | 2020-08-17 06:42:38 | 2020-08-17 06:42:38 | synced  |
+--------+---------+--------------------+--------------+----------------------+-----------+----------+-----------+---------------------+---------------------+-------------------------------+
12 rows in set (0.00 sec)
```

从上面的输出可以看出：

- 作业 59 当前正在进行中（`STATE` 为 `running`）。schema 状态当前为 `write reorganization`，但一旦任务完成，将切换到 `public` 以表示用户会话可以公开观察到此更改。`end_time` 列也是 `NULL`，表示当前不知道作业的完成时间。

- 作业 60 是一个 `add index` 作业，当前正在排队等待作业 59 完成。当作业 59 完成时，作业 60 的 `STATE` 将切换为 `running`。

- 对于删除索引或删除表等破坏性更改，作业完成时 `SCHEMA_STATE` 将变为 `none`。对于添加性更改，`SCHEMA_STATE` 将变为 `public`。

要限制显示的行数，可以指定数字和 where 条件：

```sql
ADMIN SHOW DDL JOBS [NUM] [WHERE where_condition];
```

* `NUM`：查看已完成的 DDL 作业队列中的最后 `NUM` 个结果。如果未指定，`NUM` 默认为 10。
* `WHERE`：添加过滤条件。

### `ADMIN SHOW DDL JOB QUERIES`

要查看与 `job_id` 对应的 DDL 作业的原始 SQL 语句，使用 `ADMIN SHOW DDL JOB QUERIES`：

```sql
ADMIN SHOW DDL JOBS;
ADMIN SHOW DDL JOB QUERIES 51;
```

```sql
mysql> ADMIN SHOW DDL JOB QUERIES 51;
+--------------------------------------------------------------+
| QUERY                                                        |
+--------------------------------------------------------------+
| CREATE TABLE t1 (id INT NOT NULL PRIMARY KEY auto_increment) |
+--------------------------------------------------------------+
1 row in set (0.02 sec)
```

你只能在 DDL 历史作业队列的最后十个结果中搜索与 `job_id` 对应的正在运行的 DDL 作业。

### `ADMIN SHOW DDL JOB QUERIES LIMIT m OFFSET n`

要查看与 `job_id` 对应的指定范围 `[n+1, n+m]` 内的 DDL 作业的原始 SQL 语句，使用 `ADMIN SHOW DDL JOB QUERIES LIMIT m OFFSET n`：

```sql
ADMIN SHOW DDL JOB QUERIES LIMIT m;  # 检索前 m 行
ADMIN SHOW DDL JOB QUERIES LIMIT n, m;  # 检索第 [n+1, n+m] 行
ADMIN SHOW DDL JOB QUERIES LIMIT m OFFSET n;  # 检索第 [n+1, n+m] 行
```

其中 `n` 和 `m` 是大于等于 0 的整数。

```sql
ADMIN SHOW DDL JOB QUERIES LIMIT 3;  # 检索前 3 行
+--------+--------------------------------------------------------------+
| JOB_ID | QUERY                                                        |
+--------+--------------------------------------------------------------+
|     59 | ALTER TABLE t1 ADD INDEX index2 (col2)                       |
|     60 | ALTER TABLE t2 ADD INDEX index1 (col1)                       |
|     58 | CREATE TABLE t2 (id INT NOT NULL PRIMARY KEY auto_increment) |
+--------+--------------------------------------------------------------+
3 rows in set (0.00 sec)
```

```sql
ADMIN SHOW DDL JOB QUERIES LIMIT 6, 2;  # 检索第 7-8 行
+--------+----------------------------------------------------------------------------+
| JOB_ID | QUERY                                                                      |
+--------+----------------------------------------------------------------------------+
|     52 | ALTER TABLE t1 ADD INDEX index1 (col1)                                     |
|     51 | CREATE TABLE IF NOT EXISTS t1 (id INT NOT NULL PRIMARY KEY auto_increment) |
+--------+----------------------------------------------------------------------------+
3 rows in set (0.00 sec)
```

```sql
ADMIN SHOW DDL JOB QUERIES LIMIT 3 OFFSET 4;  # 检索第 5-7 行
+--------+----------------------------------------+
| JOB_ID | QUERY                                  |
+--------+----------------------------------------+
|     54 | DROP TABLE IF EXISTS t3                |
|     53 | ALTER TABLE t1 DROP INDEX index1       |
|     52 | ALTER TABLE t1 ADD INDEX index1 (col1) |
+--------+----------------------------------------+
3 rows in set (0.00 sec)
```

你可以在 DDL 历史作业队列中任意指定范围内搜索与 `job_id` 对应的正在运行的 DDL 作业。此语法没有 `ADMIN SHOW DDL JOB QUERIES` 最后十个结果的限制。

## MySQL 兼容性

此语句是 TiDB 对 MySQL 语法的扩展。

## 另请参阅

* [DDL 简介](/ddl-introduction.md)
* [ADMIN CANCEL DDL](/sql-statements/sql-statement-admin-cancel-ddl.md)
* [ADMIN PAUSE DDL](/sql-statements/sql-statement-admin-pause-ddl.md)
* [ADMIN RESUME DDL](/sql-statements/sql-statement-admin-resume-ddl.md)
* [INFORMATION_SCHEMA.DDL_JOBS](/information-schema/information-schema-ddl-jobs.md)
