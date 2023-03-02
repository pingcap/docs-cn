---
title: ADMIN SHOW DDL [JOBS|JOB QUERIES] | TiDB SQL Statement Reference
summary: An overview of the usage of ADMIN for the TiDB database.
---

# ADMIN SHOW DDL [JOBS|JOB QUERIES]

The `ADMIN SHOW DDL [JOBS|JOB QUERIES]` statement shows information about running and recently completed DDL jobs.

## Synopsis

```ebnf+diagram
AdminStmt ::=
    'ADMIN' ( 'SHOW' ( 'DDL' ( 'JOBS' Int64Num? WhereClauseOptional | 'JOB' 'QUERIES' NumList | 'JOB' 'QUERIES' 'LIMIT' m 'OFFSET' n )? | TableName 'NEXT_ROW_ID' | 'SLOW' AdminShowSlow ) | 'CHECK' ( 'TABLE' TableNameList | 'INDEX' TableName Identifier ( HandleRange ( ',' HandleRange )* )? ) | 'RECOVER' 'INDEX' TableName Identifier | 'CLEANUP' ( 'INDEX' TableName Identifier | 'TABLE' 'LOCK' TableNameList ) | 'CHECKSUM' 'TABLE' TableNameList | 'CANCEL' 'DDL' 'JOBS' NumList | 'RELOAD' ( 'EXPR_PUSHDOWN_BLACKLIST' | 'OPT_RULE_BLACKLIST' | 'BINDINGS' ) | 'PLUGINS' ( 'ENABLE' | 'DISABLE' ) PluginNameList | 'REPAIR' 'TABLE' TableName CreateTableStmt | ( 'FLUSH' | 'CAPTURE' | 'EVOLVE' ) 'BINDINGS' )

NumList ::=
    Int64Num ( ',' Int64Num )*

WhereClauseOptional ::=
    WhereClause?
```

## Examples

### `ADMIN SHOW DDL`

To view the status of the currently running DDL jobs, use `ADMIN SHOW DDL`. The output includes the current schema version, the DDL ID and address of the owner, the running DDL jobs and SQL statements, and the DDL ID of the current TiDB instance.

{{< copyable "sql" >}}

```sql
ADMIN SHOW DDL;
```

```sql
mysql> ADMIN SHOW DDL;
+------------+--------------------------------------+---------------+--------------+--------------------------------------+-------+
| SCHEMA_VER | OWNER_ID                             | OWNER_ADDRESS | RUNNING_JOBS | SELF_ID                              | QUERY |
+------------+--------------------------------------+---------------+--------------+--------------------------------------+-------+
|         26 | 2d1982af-fa63-43ad-a3d5-73710683cc63 | 0.0.0.0:4000  |              | 2d1982af-fa63-43ad-a3d5-73710683cc63 |       |
+------------+--------------------------------------+---------------+--------------+--------------------------------------+-------+
1 row in set (0.00 sec)
```

### `ADMIN SHOW DDL JOBS`

The `ADMIN SHOW DDL JOBS` statement is used to view all the results in the current DDL job queue, including running and queuing tasks, as well as the latest ten results in the completed DDL job queue. The returned result fields are described as follows:

<CustomContent platform="tidb">

- `JOB_ID`: each DDL operation corresponds to a DDL job. `JOB_ID` is globally unique.
- `DB_NAME`: the name of the database where the DDL operation is performed.
- `TABLE_NAME`: the name of the table where the DDL operation is performed.
- `JOB_TYPE`: the type of DDL operation.
- `SCHEMA_STATE`: the current state of the schema object that the DDL operates on. If `JOB_TYPE` is `ADD INDEX`, it is the state of the index; if `JOB_TYPE` is `ADD COLUMN`, it is the state of the column; if `JOB_TYPE` is `CREATE TABLE`, it is the state of the table. Common states include the following:
    - `none`: indicates that it does not exist. Generally, after the `DROP` operation or after the `CREATE` operation fails and rolls back, it will become the `none` state.
    - `delete only`, `write only`, `delete reorganization`, `write reorganization`: these four states are intermediate states. For their specific meanings, see [How the Online DDL Asynchronous Change Works in TiDB](/ddl-introduction.md#how-the-online-ddl-asynchronous-change-works-in-tidb). As the intermediate state conversion is fast, these states are generally not visible during operation. Only when performing `ADD INDEX` operation can the `write reorganization` state be seen, indicating that index data is being added.
    - `public`: indicates that it exists and is available to users. Generally, after `CREATE TABLE` and `ADD INDEX` (or `ADD COLUMN`) operations are completed, it will become the `public` state, indicating that the newly created table, column, and index can be read and written normally.
- `SCHEMA_ID`: the ID of the database where the DDL operation is performed.
- `TABLE_ID`: the ID of the table where the DDL operation is performed.
- `ROW_COUNT`: when performing the `ADD INDEX` operation, it is the number of data rows that have been added.
- `START_TIME`: the start time of the DDL operation.
- `STATE`: the state of the DDL operation. Common states include the following:
    - `queueing`: indicates that the operation job has entered the DDL job queue but has not been executed because it is still waiting for an earlier DDL job to complete. Another reason might be that after executing the `DROP` operation, it will become the `none` state, but it will soon be updated to the `synced` state, indicating that all TiDB instances have been synchronized to that state.
    - `running`: indicates that the operation is being executed.
    - `synced`: indicates that the operation has been executed successfully and all TiDB instances have been synchronized to this state.
    - `rollback done`: indicates that the operation has failed and the rollback has been completed.
    - `rollingback`: indicates that the operation has failed and is rolling back.
    - `cancelling`: indicates that the operation is being canceled. This state only appears when you use the `ADMIN CANCEL DDL JOBS` command to cancel the DDL job.

</CustomContent>

<CustomContent platform="tidb-cloud">

- `JOB_ID`: each DDL operation corresponds to a DDL job. `JOB_ID` is globally unique.
- `DB_NAME`: the name of the database where the DDL operation is performed.
- `TABLE_NAME`: the name of the table where the DDL operation is performed.
- `JOB_TYPE`: the type of DDL operation.
- `SCHEMA_STATE`: the current state of the schema object that the DDL operates on. If `JOB_TYPE` is `ADD INDEX`, it is the state of the index; if `JOB_TYPE` is `ADD COLUMN`, it is the state of the column; if `JOB_TYPE` is `CREATE TABLE`, it is the state of the table. Common states include the following:
    - `none`: indicates that it does not exist. Generally, after the `DROP` operation or after the `CREATE` operation fails and rolls back, it will become the `none` state.
    - `delete only`, `write only`, `delete reorganization`, `write reorganization`: these four states are intermediate states. For their specific meanings, see [How the Online DDL Asynchronous Change Works in TiDB](https://docs.pingcap.com/tidb/stable/ddl-introduction#how-the-online-ddl-asynchronous-change-works-in-tidb). As the intermediate state conversion is fast, these states are generally not visible during operation. Only when performing `ADD INDEX` operation can the `write reorganization` state be seen, indicating that index data is being added.
    - `public`: indicates that it exists and is available to users. Generally, after `CREATE TABLE` and `ADD INDEX` (or `ADD COLUMN`) operations are completed, it will become the `public` state, indicating that the newly created table, column, and index can be read and written normally.
- `SCHEMA_ID`: the ID of the database where the DDL operation is performed.
- `TABLE_ID`: the ID of the table where the DDL operation is performed.
- `ROW_COUNT`: when performing the `ADD INDEX` operation, it is the number of data rows that have been added.
- `START_TIME`: the start time of the DDL operation.
- `STATE`: the state of the DDL operation. Common states include the following:
    - `queueing`: indicates that the operation job has entered the DDL job queue but has not been executed because it is still waiting for an earlier DDL job to complete. Another reason might be that after executing the `DROP` operation, it will become the `none` state, but it will soon be updated to the `synced` state, indicating that all TiDB instances have been synchronized to that state.
    - `running`: indicates that the operation is being executed.
    - `synced`: indicates that the operation has been executed successfully and all TiDB instances have been synchronized to this state.
    - `rollback done`: indicates that the operation has failed and the rollback has been completed.
    - `rollingback`: indicates that the operation has failed and is rolling back.
    - `cancelling`: indicates that the operation is being canceled. This state only appears when you use the `ADMIN CANCEL DDL JOBS` command to cancel the DDL job.

</CustomContent>

The following example shows the results of `ADMIN SHOW DDL JOBS`:

{{< copyable "sql" >}}

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

From the output above:

- Job 59 is currently in progress (`STATE` of `running`). The schema state is currently in `write reorganization`, but will switch to `public` once the task is completed to note that the change can be observed publicly by user sessions. The `end_time` column is also `NULL` indicating that the completion time for the job is currently not known.

- Job 60 is an `add index` job, which is currently queued waiting for job 59 to complete. When job 59 completes, the `STATE` of job 60 will switch to `running`.

- For destructive changes such as dropping an index or dropping a table, the `SCHEMA_STATE` will change to `none` when the job is complete. For additive changes, the `SCHEMA_STATE` will change to `public`.

To limit the number of rows shown, specify a number and a where condition:

```sql
ADMIN SHOW DDL JOBS [NUM] [WHERE where_condition];
```

* `NUM`: to view the last `NUM` results in the completed DDL job queue. If not specified, `NUM` is by default 10.
* `WHERE`: to add filter conditions.

### `ADMIN SHOW DDL JOB QUERIES`

To view the original SQL statements of the DDL job corresponding to `job_id`, use `ADMIN SHOW DDL JOB QUERIES`:

{{< copyable "sql" >}}

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

You can only search the running DDL job corresponding to `job_id` within the last ten results in the DDL history job queue.

### `ADMIN SHOW DDL JOB QUERIES LIMIT m OFFSET n`

 To view the original SQL statements of the DDL job within a specified range `[n+1, n+m]` corresponding to `job_id`, use `ADMIN SHOW DDL JOB QUERIES LIMIT m OFFSET n`:

 {{< copyable "sql" >}}

```sql
 ADMIN SHOW DDL JOB QUERIES LIMIT m;  # Retrieve first m rows
 ADMIN SHOW DDL JOB QUERIES LIMIT n, m;  # Retrieve rows [n+1, n+m]
 ADMIN SHOW DDL JOB QUERIES LIMIT m OFFSET n;  # Retrieve rows [n+1, n+m]
 ```

 where `n` and `m` are integers greater or equal to 0.

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

 You can search the running DDL job corresponding to `job_id` within an arbitrarily specified range of results in the DDL history job queue. This syntax does not have the limitation of the last ten results of `ADMIN SHOW DDL JOB QUERIES`.

## MySQL compatibility

This statement is a TiDB extension to MySQL syntax.

## See also

* [ADMIN CANCEL DDL](/sql-statements/sql-statement-admin-cancel-ddl.md)
