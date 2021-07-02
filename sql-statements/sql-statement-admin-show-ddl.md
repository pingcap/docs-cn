---
title: ADMIN SHOW DDL [JOBS|QUERIES]
summary: TiDB 数据库中 ADMIN SHOW DDL [JOBS|QUERIES] 的使用概况。
---

# ADMIN SHOW DDL [JOBS|QUERIES]

`ADMIN SHOW DDL [JOBS|QUERIES]` 语句显示了正在运行和最近完成的 DDL 作业的信息。

## 语法图

```ebnf+diagram
AdminStmt ::=
    'ADMIN' ( 'SHOW' ( 'DDL' ( 'JOBS' Int64Num? WhereClauseOptional | 'JOB' 'QUERIES' NumList )? | TableName 'NEXT_ROW_ID' | 'SLOW' AdminShowSlow ) | 'CHECK' ( 'TABLE' TableNameList | 'INDEX' TableName Identifier ( HandleRange ( ',' HandleRange )* )? ) | 'RECOVER' 'INDEX' TableName Identifier | 'CLEANUP' ( 'INDEX' TableName Identifier | 'TABLE' 'LOCK' TableNameList ) | 'CHECKSUM' 'TABLE' TableNameList | 'CANCEL' 'DDL' 'JOBS' NumList | 'RELOAD' ( 'EXPR_PUSHDOWN_BLACKLIST' | 'OPT_RULE_BLACKLIST' | 'BINDINGS' ) | 'PLUGINS' ( 'ENABLE' | 'DISABLE' ) PluginNameList | 'REPAIR' 'TABLE' TableName CreateTableStmt | ( 'FLUSH' | 'CAPTURE' | 'EVOLVE' ) 'BINDINGS' )

NumList ::=
    Int64Num ( ',' Int64Num )*

WhereClauseOptional ::=
    WhereClause?
```

## 示例

### `ADMIN SHOW DDL`

可以通过 `ADMIN SHOW DDL` 语句查看当前正在运行的 DDL 作业：

{{< copyable "sql" >}}

```sql
ADMIN SHOW DDL;
```

```sql
ADMIN SHOW DDL;
+------------+--------------------------------------+---------------+--------------+--------------------------------------+-------+
| SCHEMA_VER | OWNER_ID                             | OWNER_ADDRESS | RUNNING_JOBS | SELF_ID                              | QUERY |
+------------+--------------------------------------+---------------+--------------+--------------------------------------+-------+
|         26 | 2d1982af-fa63-43ad-a3d5-73710683cc63 | 0.0.0.0:4000  |              | 2d1982af-fa63-43ad-a3d5-73710683cc63 |       |
+------------+--------------------------------------+---------------+--------------+--------------------------------------+-------+
1 row in set (0.00 sec)
```

### `ADMIN SHOW DDL JOBS`

`ADMIN SHOW DDL JOBS` 语句用于查看当前 DDL 作业队列中的所有结果（包括正在运行以及等待运行的任务）以及已执行完成的 DDL 作业队列中的最近十条结果。

{{< copyable "sql" >}}

```sql
ADMIN SHOW DDL JOBS;
```

```sql
ADMIN SHOW DDL JOBS;
+--------+---------+--------------------+--------------+----------------------+-----------+----------+-----------+---------------------+---------------------+---------+
| JOB_ID | DB_NAME | TABLE_NAME         | JOB_TYPE     | SCHEMA_STATE         | SCHEMA_ID | TABLE_ID | ROW_COUNT | START_TIME          | END_TIME            | STATE   |
+--------+---------+--------------------+--------------+----------------------+-----------+----------+-----------+---------------------+---------------------+---------+
|     59 | test    | t1                 | add index    | write reorganization |         1 |       55 |     88576 | 2020-08-17 07:51:58 | NULL                | running |
|     60 | test    | t2                 | add index    | none                 |         1 |       57 |         0 | 2020-08-17 07:51:59 | NULL                | none    |
|     58 | test    | t2                 | create table | public               |         1 |       57 |         0 | 2020-08-17 07:41:28 | 2020-08-17 07:41:28 | synced  |
|     56 | test    | t1                 | create table | public               |         1 |       55 |         0 | 2020-08-17 07:41:02 | 2020-08-17 07:41:02 | synced  |
|     54 | test    | t1                 | drop table   | none                 |         1 |       50 |         0 | 2020-08-17 07:41:02 | 2020-08-17 07:41:02 | synced  |
|     53 | test    | t1                 | drop index   | none                 |         1 |       50 |         0 | 2020-08-17 07:35:44 | 2020-08-17 07:35:44 | synced  |
|     52 | test    | t1                 | add index    | public               |         1 |       50 |    451010 | 2020-08-17 07:34:43 | 2020-08-17 07:35:16 | synced  |
|     51 | test    | t1                 | create table | public               |         1 |       50 |         0 | 2020-08-17 07:34:02 | 2020-08-17 07:34:02 | synced  |
|     49 | test    | t1                 | drop table   | none                 |         1 |       47 |         0 | 2020-08-17 07:34:02 | 2020-08-17 07:34:02 | synced  |
|     48 | test    | t1                 | create table | public               |         1 |       47 |         0 | 2020-08-17 07:33:37 | 2020-08-17 07:33:37 | synced  |
|     46 | mysql   | stats_extended     | create table | public               |         3 |       45 |         0 | 2020-08-17 06:42:38 | 2020-08-17 06:42:38 | synced  |
|     44 | mysql   | opt_rule_blacklist | create table | public               |         3 |       43 |         0 | 2020-08-17 06:42:38 | 2020-08-17 06:42:38 | synced  |
+--------+---------+--------------------+--------------+----------------------+-----------+----------+-----------+---------------------+---------------------+---------+
12 rows in set (0.00 sec)
```

由上述 `ADMIN` 查询结果可知：

- `job_id` 为 59 的 DDL 作业当前正在进行中（`STATE` 列显示为 `running`）。`SCHEMA_STATE` 列显示了表当前处于 `write reorganization` 状态，一旦任务完成，将更改为 `public`，以便用户会话可以公开观察到状态变更。`end_time` 列显示为 `NULL`，表明当前作业的完成时间未知。

- `job_id` 为 60 的 `JOB_TYPE` 显示为 `add index`，表明正在排队等待 `job_id` 为 59 的作业完成。当作业 59 完成时，作业 60 的 `STATE` 将更改为 `running`。

- 对于破坏性的更改（例如删除索引或删除表），当作业完成时，`SCHEMA_STATE` 将变为 `none`。对于附加更改，`SCHEMA_STATE` 将变为 `public`。

若要限制表中显示的行数，可以指定 `NUM` 和 `WHERE` 条件：

```sql
ADMIN SHOW DDL JOBS [NUM] [WHERE where_condition];
```

* `NUM`：用于查看已经执行完成的 DDL 作业队列中最近 `NUM` 条结果；未指定时，默认值为 10。
* `WHERE`：`WHERE` 子句，用于添加过滤条件。

### `ADMIN SHOW DDL JOB QUERIES`

`ADMIN SHOW DDL JOB QUERIES` 语句用于查看 `job_id` 对应的 DDL 任务的原始 SQL 语句：

{{< copyable "sql" >}}

```sql
ADMIN SHOW DDL JOBS;
ADMIN SHOW DDL JOB QUERIES 51;
```

```sql
ADMIN SHOW DDL JOB QUERIES 51;
+--------------------------------------------------------------+
| QUERY                                                        |
+--------------------------------------------------------------+
| CREATE TABLE t1 (id INT NOT NULL PRIMARY KEY auto_increment) |
+--------------------------------------------------------------+
1 row in set (0.02 sec)
```

只能在 DDL 历史作业队列中最近十条结果中搜索与 `job_id` 对应的正在运行中的 DDL 作业。

## MySQL 兼容性

`ADMIN SHOW DDL [JOBS|QUERIES]` 语句是 TiDB 对 MySQL 语法的扩展。

## 另请参阅

* [ADMIN CANCEL DDL](/sql-statements/sql-statement-admin-cancel-ddl.md)
