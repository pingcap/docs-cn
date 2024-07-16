---
title: ADMIN SHOW DDL [JOBS|JOB QUERIES]
summary: TiDB 数据库中 ADMIN SHOW DDL [JOBS|JOB QUERIES] 的使用概况。
---

# ADMIN SHOW DDL [JOBS|JOB QUERIES]

`ADMIN SHOW DDL [JOBS|JOB QUERIES]` 语句显示了正在运行和最近完成的 DDL 作业的信息。

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

可以通过 `ADMIN SHOW DDL` 语句查看当前正在运行的 DDL 作业状态，包括当前 schema 版本号、Owner 的 DDL ID 和地址、正在执行的 DDL 任务和 SQL、当前 TiDB 实例的 DDL ID。该语句返回的结果字段描述如下：

- `SCHEMA_VER`：schema 版本号。
- `OWNER_ID`：DDL Owner 的 UUID。参见 [`TIDB_IS_DDL_OWNER()`](/functions-and-operators/tidb-functions.md)。
- `OWNER_ADDRESS`：DDL Owner 的 IP 地址。
- `RUNNING_JOBS`：正在运行的 DDL 作业的详细信息。
- `SELF_ID`：当前连接的 TiDB 节点的 UUID。如果 `SELF_ID` 与 `OWNER_ID` 相同，这意味着你当前连接的是 DDL Owner。
- `QUERY`：查询语句。

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

`ADMIN SHOW DDL JOBS` 语句用于查看当前 DDL 作业队列中的所有结果（包括正在运行以及等待运行的任务）以及已执行完成的 DDL 作业队列中的最近十条结果。该语句的返回结果字段描述如下：

- `JOB_ID`：每个 DDL 操作对应一个 DDL 任务，`JOB_ID` 全局唯一。
- `DB_NAME`：执行 DDL 操作的数据库的名称。
- `TABLE_NAME`：执行 DDL 操作的表的名称。
- `JOB_TYPE`：DDL 任务的类型。常见的任务类型包括：
    - `create schema`：[`CREATE SCHEMA`](/sql-statements/sql-statement-create-database.md) 操作。
    - `create table`：[`CREATE TABLE`](/sql-statements/sql-statement-create-table.md) 操作。
    - `create view`：[`CREATE VIEW`](/sql-statements/sql-statement-create-view.md) 操作。
    - `ingest`：通过 [`tidb_ddl_enable_fast_reorg`](/system-variables.md#tidb_ddl_enable_fast_reorg-从-v630-版本开始引入) 配置的加速索引回填的 ingest 任务。
    - `txn`：基本的事务性回填。
    - `add index /* txn-merge */`：在回填完成时，将临时索引与原始索引合并的事务性回填。
- `SCHEMA_STATE`：DDL 所操作的 schema 对象的当前状态。如果 `JOB_TYPE` 是 `ADD INDEX`，则为索引的状态；如果是 `ADD COLUMN`，则为列的状态；如果是 `CREATE TABLE`，则为表的状态。常见的状态有以下几种：
    - `none`：表示不存在。一般 `DROP` 操作或者 `CREATE` 操作失败回滚后，会变为 `none` 状态。
    - `delete only`、`write only`、`delete reorganization`、`write reorganization`：这四种状态是中间状态，具体含义请参考 [TiDB 中在线 DDL 异步变更的原理](/ddl-introduction.md#tidb-在线-ddl-异步变更的原理)。由于中间状态转换很快，一般操作中看不到这几种状态，只有执行 `ADD INDEX` 操作时能看到处于 `write reorganization` 状态，表示正在添加索引数据。
    - `public`：表示存在且对用户可用。一般 `CREATE TABLE` 和 `ADD INDEX`（或 `ADD COLUMN`）等操作完成后，会变为 `public` 状态，表示新建的表、列、索引可以正常读写了。
- `SCHEMA_ID`：执行 DDL 操作的数据库的 ID。
- `TABLE_ID`：执行 DDL 操作的表的 ID。
- `ROW_COUNT`：执行 `ADD INDEX` 操作时，当前已经添加完成的数据行数。
- `CREATE_TIME`：DDL 操作的创建时间。
- `START_TIME`：DDL 操作的开始时间。
- `END_TIME`：DDL 操作的结束时间。
- `STATE`：DDL 操作的状态。常见的状态有以下几种：
    - `none`：表示该操作尚未开始。
    - `queueing`：表示该操作任务已经进入 DDL 任务队列中，但尚未执行，因为还在排队等待前面的 DDL 任务完成。另一种原因可能是执行 `DROP` 操作后，`queueing` 状态会变为 `done` 状态，但是很快会更新为 `synced` 状态，表示所有 TiDB 实例都已经同步到该状态。
    - `running`：表示该操作正在执行。
    - `synced`：表示该操作已经执行成功，且所有 TiDB 实例都已经同步该状态。
    - `rollback done`：表示该操作执行失败，回滚完成。
    - `rollingback`：表示该操作执行失败，正在回滚。
    - `cancelling`：表示正在取消该操作。这个状态只有在用 [`ADMIN CANCEL DDL JOBS`](/sql-statements/sql-statement-admin-cancel-ddl.md) 命令取消 DDL 任务时才会出现。
    - `cancelled`：表示该操作已经取消。
    - `pausing`：表示正在暂停该操作。
    - `paused`：表示 DDL 已被暂停运行。这个状态只有在用 [`ADMIN PAUSED DDL JOBS`](/sql-statements/sql-statement-admin-pause-ddl.md) 命令暂停 DDL 任务时才会出现。可以通过 [`ADMIN RESUME DDL JOBS`](/sql-statements/sql-statement-admin-resume-ddl.md) 命令进行恢复运行。
    - `done`：表示该操作在 TiDB owner 节点已经执行成功，但其他 TiDB 节点还没有同步该 DDL 任务所执行的变更。

示例如下：

```sql
ADMIN SHOW DDL JOBS;
```

```sql
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

### `ADMIN SHOW DDL JOB QUERIES LIMIT m OFFSET n`

`ADMIN SHOW DDL JOB QUERIES LIMIT m OFFSET n` 语句用于查看指定范围 `[n+1, n+m]` 的 `job_id` 对应的 DDL 任务的原始 SQL 语句：

```sql
ADMIN SHOW DDL JOB QUERIES LIMIT m;           # -- 取出前 m 行
ADMIN SHOW DDL JOB QUERIES LIMIT n, m;        # -- 取出第 n+1 到 n+m 行
ADMIN SHOW DDL JOB QUERIES LIMIT m OFFSET n;  # -- 取出第 n+1 到 n+m 行
```

以上语法中 `n` 和 `m` 都是非负整数。语法的具体示例如下：

```sql
ADMIN SHOW DDL JOB QUERIES LIMIT 3;  # Retrieve first 3 rows
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
ADMIN SHOW DDL JOB QUERIES LIMIT 6, 2;  # Retrieve rows 7-8
+--------+----------------------------------------------------------------------------+
| JOB_ID | QUERY                                                                      | 
+--------+----------------------------------------------------------------------------+
|     52 | ALTER TABLE t1 ADD INDEX index1 (col1)                                     | 
|     51 | CREATE TABLE IF NOT EXISTS t1 (id INT NOT NULL PRIMARY KEY auto_increment) | 
+--------+----------------------------------------------------------------------------+
3 rows in set (0.00 sec)
```

```sql
ADMIN SHOW DDL JOB QUERIES LIMIT 3 OFFSET 4;  # Retrieve rows 5-7
+--------+----------------------------------------+
| JOB_ID | QUERY                                  | 
+--------+----------------------------------------+
|     54 | DROP TABLE IF EXISTS t3                |
|     53 | ALTER TABLE t1 DROP INDEX index1       |
|     52 | ALTER TABLE t1 ADD INDEX index1 (col1) | 
+--------+----------------------------------------+
3 rows in set (0.00 sec)
```

该语句可以在 DDL 历史作业队列任意指定范围中搜索与 `job_id` 对应的正在运行中的 DDL 作业，没有 `ADMIN SHOW DDL JOB QUERIES` 语句的最近 10 条结果的限制。

## MySQL 兼容性

`ADMIN SHOW DDL [JOBS|JOB QUERIES]` 语句是 TiDB 对 MySQL 语法的扩展。

## 另请参阅

* [DDL 语句的执行原理及最佳实践](/ddl-introduction.md)
* [ADMIN CANCEL DDL](/sql-statements/sql-statement-admin-cancel-ddl.md)
* [ADMIN PAUSE DDL](/sql-statements/sql-statement-admin-pause-ddl.md)
* [ADMIN RESUME DDL](/sql-statements/sql-statement-admin-resume-ddl.md)
* [INFORMATION_SCHEMA.DDL_JOBS](/information-schema/information-schema-ddl-jobs.md)
