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

To view the currently running DDL jobs, use `ADMIN SHOW DDL`:

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

To view all the results in the current DDL job queue (including tasks that are running and waiting to be run) and the last ten results in the completed DDL job queue, use `ADMIN SHOW DDL JOBS`:

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
