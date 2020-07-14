---
title: ADMIN | TiDB SQL Statement Reference
summary: An overview of the usage of ADMIN for the TiDB database.
aliases: ['/docs/dev/sql-statements/sql-statement-admin/','/docs/dev/reference/sql/statements/admin/']
---

# ADMIN

This statement is a TiDB extension syntax, used to view the status of TiDB and check the data of tables in TiDB.

## DDL related statement

### `admin show DDL`

To view the currently running DDL jobs, use `ADMIN SHOW DDL`:

{{< copyable "sql" >}}

```sql
ADMIN SHOW DDL;
```

### `admin show DDL jobs`

To view all the results in the current DDL job queue (including tasks that are running and waiting to be run) and the last ten results in the completed DDL job queue, use `ADMIN SHOW DDL JOBS`:

{{< copyable "sql" >}}

```sql
ADMIN SHOW DDL JOBS [NUM] [WHERE where_condition];
```

* `NUM`: to view the last `NUM` results in the completed DDL job queue. If not specified, `NUM` is by default 10.
* `WHERE`: to add filter conditions.

### `admin show DDL queries`

To view the original SQL statements of the DDL job corresponding to `job_id`, use `ADMIN SHOW DDL JOB QUERIES`:

{{< copyable "sql" >}}

```sql
ADMIN SHOW DDL JOB QUERIES job_id [, job_id] ...;
```

You can only searches the running DDL job corresponding to `job_id` and the last ten results in the DDL history job queue.

### `admin cancel DDL jobs`

To cancel the currently running DDL jobs and return whether the corresponding jobs are successfully cancelled, use `ADMIN CANCEL DDL JOBS`:

{{< copyable "sql" >}}

```sql
ADMIN CANCEL DDL JOBS job_id [, job_id] ...;
```

If the operation fails to cancel the jobs, specific reasons are displayed.

> **Note:**
>
> - Only this operation can cancel DDL jobs. All other operations and environment changes (such as machine restart and cluster restart) cannot cancel these jobs.
> - This operation can cancel multiple DDL jobs at the same time. You can get the ID of DDL jobs using the `ADMIN SHOW DDL JOBS` statement.
> - If the jobs you want to cancel are finished, the cancellation operation fails.

## `ADMIN CHECK` related statement

To check the consistency of all the data and corresponding indexes in the `tbl_name` table, use `ADMIN CHECK TABLE`:

{{< copyable "sql" >}}

```sql
ADMIN CHECK TABLE tbl_name [, tbl_name] ...;
```

If the consistency check is passed, an empty result is returned. Otherwise, an error message is returned indicating that the data is inconsistent.

{{< copyable "sql" >}}

```sql
ADMIN CHECK INDEX tbl_name idx_name;
```

The above statement is used to check the consistency of the column data and index data corresponding to the `idx_name` index in the `tbl_name` table. If the consistency check is passed, an empty result is returned; otherwise, an error message is returned indicating that the data is inconsistent.

{{< copyable "sql" >}}

```sql
ADMIN CHECK INDEX tbl_name idx_name (lower_val, upper_val) [, (lower_val, upper_val)] ...;
```

The above statement is used to check the consistency of the column data and index data corresponding to the `idx_name` index in the `tbl_name` table, with the data range (to be checked) specified. If the consistency check is passed, an empty result is returned. Otherwise, an error message is returned indicating that the data is inconsistent.

### `admin checksum`

{{< copyable "sql" >}}

```sql
ADMIN CHECKSUM TABLE tbl_name [, tbl_name] ...;
```

The above statement is used to get the 64-bit checksum value of `tbl_name`. This value is obtained by calculating CRC64 of all key-value pairs (including row data and index data) in the table.

## `ADMIN RELOAD` statement

{{< copyable "sql" >}}

```sql
ADMIN RELOAD expr_pushdown_blacklist;
```

The above statement is used to reload the blacklist pushed down by the expression.

{{< copyable "sql" >}}

```sql
ADMIN RELOAD opt_rule_blacklist;
```

The above statement is used to reload the blacklist of logic optimization rules.

## `ADMIN PLUGINS` related statement

{{< copyable "sql" >}}

```sql
ADMIN PLUGINS ENABLE plugin_name [, plugin_name] ...;
```

The above statement is used to enable the `plugin_name` plugin.

{{< copyable "sql" >}}

```sql
ADMIN PLUGINS DISABLE plugin_name [, plugin_name] ...;
```

The above statement is used to disable the `plugin_name` plugin.

## `ADMIN BINDINGS` related statement

{{< copyable "sql" >}}

```sql
ADMIN FLUSH bindings;
```

The above statement is used to persist SQL Plan binding information.

{{< copyable "sql" >}}

```sql
ADMIN CAPTURE bindings;
```

The above statement can generate the binding of SQL Plan from the `SELECT` statement that occurs more than once.

{{< copyable "sql" >}}

```sql
ADMIN EVOLVE bindings;
```

After the automatic binding feature is enabled, the evolution of SQL Plan binding information is triggered every `bind-info-leave` (the default value is `3s`). The above statement is used to proactively trigger this evolution.

{{< copyable "sql" >}}

```sql
ADMIN RELOAD bindings;
```

The above statement is used to reload SQL Plan binding information.

## `ADMIN REPAIR` statement

To overwrite the metadata of the stored table in an untrusted way in extreme cases, use `ADMIN REPAIR TABLE`:

{{< copyable "sql" >}}

```sql
ADMIN REPAIR TABLE tbl_name CREATE TABLE STATEMENT;
```

Here “untrusted” means that you need to manually ensure that the metadata of the original table can be covered by the `CREATE TABLE STATEMENT` operation. To use this `REPAIR` statement, enable the [`repair-mode`](/tidb-configuration-file.md#repair-mode) configuration item, and make sure that the tables to be repaired are listed in the [`repair-table-list`](/tidb-configuration-file.md#repair-table-list).

## `ADMIN SHOW SLOW` statement

{{< copyable "sql" >}}

```sql
ADMIN SHOW SLOW RECENT N;
```

{{< copyable "sql" >}}

```sql
ADMIN SHOW SLOW TOP [INTERNAL | ALL] N;
```

For details, refer to [admin show slow statement](/identify-slow-queries.md#admin-show-slow-command)

## Synopsis

**AdminStmt:**

![AdminStmt](/media/sqlgram/AdminStmt.png)

## Examples

Run the following command to view the last 10 completed DDL jobs in the currently running DDL job queue. When `NUM` is not specified, only the last 10 completed DDL jobs is presented by default.

{{< copyable "sql" >}}

```sql
admin show ddl jobs;
```

```
+--------+---------+------------+---------------------+----------------+-----------+----------+-----------+-----------------------------------+-----------------------------------+---------------+
| JOB_ID | DB_NAME | TABLE_NAME | JOB_TYPE            | SCHEMA_STATE   | SCHEMA_ID | TABLE_ID | ROW_COUNT | START_TIME                        | END_TIME                          | STATE         |
+--------+---------+------------+---------------------+----------------+-----------+----------+-----------+-----------------------------------+-----------------------------------+---------------+
| 45     | test    | t1         | add index     | write reorganization | 32        | 37       | 0         | 2019-01-10 12:38:36.501 +0800 CST |                                   | running       |
| 44     | test    | t1         | add index     | none                 | 32        | 37       | 0         | 2019-01-10 12:36:55.18 +0800 CST  | 2019-01-10 12:36:55.852 +0800 CST | rollback done |
| 43     | test    | t1         | add index     | public               | 32        | 37       | 6         | 2019-01-10 12:35:13.66 +0800 CST  | 2019-01-10 12:35:14.925 +0800 CST | synced        |
| 42     | test    | t1         | drop index    | none                 | 32        | 37       | 0         | 2019-01-10 12:34:35.204 +0800 CST | 2019-01-10 12:34:36.958 +0800 CST | synced        |
| 41     | test    | t1         | add index     | public               | 32        | 37       | 0         | 2019-01-10 12:33:22.62 +0800 CST  | 2019-01-10 12:33:24.625 +0800 CST | synced        |
| 40     | test    | t1         | drop column   | none                 | 32        | 37       | 0         | 2019-01-10 12:33:08.212 +0800 CST | 2019-01-10 12:33:09.78 +0800 CST  | synced        |
| 39     | test    | t1         | add column    | public               | 32        | 37       | 0         | 2019-01-10 12:32:55.42 +0800 CST  | 2019-01-10 12:32:56.24 +0800 CST  | synced        |
| 38     | test    | t1         | create table  | public               | 32        | 37       | 0         | 2019-01-10 12:32:41.956 +0800 CST | 2019-01-10 12:32:43.956 +0800 CST | synced        |
| 36     | test    |            | drop table    | none                 | 32        | 34       | 0         | 2019-01-10 11:29:59.982 +0800 CST | 2019-01-10 11:30:00.45 +0800  CST | synced        |
| 35     | test    |            | create table  | public               | 32        | 34       | 0         | 2019-01-10 11:29:40.741 +0800 CST | 2019-01-10 11:29:41.682 +0800 CST | synced        |
| 33     | test    |            | create schema | public               | 32        | 0        | 0         | 2019-01-10 11:29:22.813 +0800 CST | 2019-01-10 11:29:23.954 +0800 CST | synced        |
+--------+---------+------------+---------------------+----------------+-----------+----------+-----------+-----------------------------------+-----------------------------------+---------------+
```

Run the following command to view the last 5 completed DDL jobs in the currently running DDL job queue:

{{< copyable "sql" >}}

```sql
admin show ddl jobs 5;
```

```
+--------+---------+------------+---------------------+----------------+-----------+----------+-----------+-----------------------------------+-----------------------------------+---------------+
| JOB_ID | DB_NAME | TABLE_NAME | JOB_TYPE            | SCHEMA_STATE   | SCHEMA_ID | TABLE_ID | ROW_COUNT | START_TIME                        | END_TIME                          | STATE         |
+--------+---------+------------+---------------------+----------------+-----------+----------+-----------+-----------------------------------+-----------------------------------+---------------+
| 45     | test    | t1         | add index     | write reorganization | 32        | 37       | 0         | 2019-01-10 12:38:36.501 +0800 CST |                                   | running       |
| 44     | test    | t1         | add index     | none                 | 32        | 37       | 0         | 2019-01-10 12:36:55.18 +0800 CST  | 2019-01-10 12:36:55.852 +0800 CST | rollback done |
| 43     | test    | t1         | add index     | public               | 32        | 37       | 6         | 2019-01-10 12:35:13.66 +0800 CST  | 2019-01-10 12:35:14.925 +0800 CST | synced        |
| 42     | test    | t1         | drop index    | none                 | 32        | 37       | 0         | 2019-01-10 12:34:35.204 +0800 CST | 2019-01-10 12:34:36.958 +0800 CST | synced        |
| 41     | test    | t1         | add index     | public               | 32        | 37       | 0         | 2019-01-10 12:33:22.62 +0800 CST  | 2019-01-10 12:33:24.625 +0800 CST | synced        |
| 40     | test    | t1         | drop column   | none                 | 32        | 37       | 0         | 2019-01-10 12:33:08.212 +0800 CST | 2019-01-10 12:33:09.78 +0800 CST  | synced        |
+--------+---------+------------+---------------------+----------------+-----------+----------+-----------+-----------------------------------+-----------------------------------+---------------+
```

Run the following command to view the uncompleted DDL jobs in the test database. The results include the DDL jobs that are running and the last 5 DDL jobs that are completed but failed.

{{< copyable "sql" >}}

```sql
admin show ddl jobs 5 where state!='synced' and db_name='test';
```

```
+--------+---------+------------+---------------------+----------------+-----------+----------+-----------+-----------------------------------+-----------------------------------+---------------+
| JOB_ID | DB_NAME | TABLE_NAME | JOB_TYPE            | SCHEMA_STATE   | SCHEMA_ID | TABLE_ID | ROW_COUNT | START_TIME                        | END_TIME                          | STATE         |
+--------+---------+------------+---------------------+----------------+-----------+----------+-----------+-----------------------------------+-----------------------------------+---------------+
| 45     | test    | t1         | add index     | write reorganization | 32        | 37       | 0         | 2019-01-10 12:38:36.501 +0800 CST |                                   | running       |
| 44     | test    | t1         | add index     | none                 | 32        | 37       | 0         | 2019-01-10 12:36:55.18 +0800 CST  | 2019-01-10 12:36:55.852 +0800 CST | rollback done |
+--------+---------+------------+---------------------+----------------+-----------+----------+-----------+-----------------------------------+-----------------------------------+---------------+
```

* `JOB_ID`: each DDL operation corresponds to one DDL job. `JOB_ID` is globally unique.
* `DB_NAME`: the name of the database on which the DDL operations are performed.
* `TABLE_NAME`: the name of the table on which the DDL operations are performed.
* `JOB_TYPE`: the type of the DDL operations.
* `SCHEMA_STATE`: the current state of the schema. If the `JOB_TYPE` is `add index`, it is the state of the index; if the `JOB_TYPE` is `add column`, it is the state of the column; if the `JOB_TYPE` is `create table`, it is the state of the table. The common states include:
    * `none`: it indicates not existing. When the `drop` or `create` operation fails and rolls back, it usually becomes the `none` state.
    * `delete only`, `write only`, `delete reorganization`, `write reorganization`: these four states are intermediate states. For details, see the paper [Online, Asynchronous Schema Change in F1](http://static.googleusercontent.com/media/research.google.com/zh-CN//pubs/archive/41376.pdf). These states are not visible in common operations, because the conversion from the intermediate states is so quick. You can see the `write reorganization` state only in `add index` operations, which means that the index data is being added.
    * `public`: it indicates existing and usable. When operations like `create table` and `add index/column` are finished, it usually becomes the `public` state, which means that the created table/column/index can be normally read and written now.
* `SCHEMA_ID`: the ID of the database on which the DDL operations are performed.
* `TABLE_ID`: the ID of the table on which the DDL operations are performed.
* `ROW_COUNT`: the number of the data rows that have been added when running the `add index` operation.
* `START_TIME`: the start time of the DDL operations.
* `END_TIME`: the end time of the DDL operations.
* `STATE`: the state of the DDL operations. The common states include:
    * `none`: it indicates that the operation task has been put in the DDL job queue but has not been performed yet, because it is waiting for the previous tasks to complete. Another reason might be that it becomes the `none` state after running the drop operation, but it will soon be updated to the `synced` state, which means that all TiDB instances have been synced to this state.
    * `running`: it indicates that the operation is being performed.
    * `synced`: it indicates that the operation has been performed successfully and all TiDB instances have been synced to this state.
    * `rollback done`: it indicates that the operation has failed and has finished rolling back.
    * `rollingback`: it indicates that the operation has failed and is rolling back.
    * `cancelling`: it indicates that the operation is being cancelled. This state only occurs when you cancel DDL jobs using the `ADMIN CANCEL DDL JOBS` command.

## MySQL compatibility

This statement is a TiDB extension to MySQL syntax.
