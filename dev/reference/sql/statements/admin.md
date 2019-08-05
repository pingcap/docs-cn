---
title: ADMIN | TiDB SQL Statement Reference
summary: An overview of the usage of ADMIN for the TiDB database.
category: reference
---

# ADMIN

This statement is a TiDB extension syntax, used to view the status of TiDB and check the data of tables in TiDB.

```sql
ADMIN SHOW DDL
ADMIN SHOW DDL JOBS
ADMIN SHOW DDL JOB QUERIES job_id [, job_id] ...
ADMIN CANCEL DDL JOBS job_id [, job_id] ...
ADMIN CHECK TABLE tbl_name [, tbl_name] ...
```

- `ADMIN SHOW DDL`: To view the currently running DDL jobs.
- `ADMIN SHOW DDL JOBS`: To view all the results in the current DDL job queue (including tasks that are running and waiting to be run) and the last ten results in the completed DDL job queue.

## Synopsis

**AdminStmt:**

![AdminStmt](/media/sqlgram-dev/AdminStmt.png)

## Examples

```sql
mysql> admin show ddl jobs;
+--------+---------+------------+---------------+----------------------+-----------+----------+-----------+-----------------------------------+---------------+
| JOB_ID | DB_NAME | TABLE_NAME | JOB_TYPE      | SCHEMA_STATE         | SCHEMA_ID | TABLE_ID | ROW_COUNT | START_TIME                        | STATE         |
+--------+---------+------------+---------------+----------------------+-----------+----------+-----------+-----------------------------------+---------------+
| 45     | test    | t1         | add index     | write reorganization | 32        | 37       | 0         | 2019-01-10 12:38:36.501 +0800 CST | running       |
| 44     | test    | t1         | add index     | none                 | 32        | 37       | 0         | 2019-01-10 12:36:55.18 +0800 CST  | rollback done |
| 43     | test    | t1         | add index     | public               | 32        | 37       | 6         | 2019-01-10 12:35:13.66 +0800 CST  | synced        |
| 42     | test    | t1         | drop index    | none                 | 32        | 37       | 0         | 2019-01-10 12:34:35.204 +0800 CST | synced        |
| 41     | test    | t1         | add index     | public               | 32        | 37       | 0         | 2019-01-10 12:33:22.62 +0800 CST  | synced        |
| 40     | test    | t1         | drop column   | none                 | 32        | 37       | 0         | 2019-01-10 12:33:08.212 +0800 CST | synced        |
| 39     | test    | t1         | add column    | public               | 32        | 37       | 0         | 2019-01-10 12:32:55.42 +0800 CST  | synced        |
| 38     | test    | t1         | create table  | public               | 32        | 37       | 0         | 2019-01-10 12:32:41.956 +0800 CST | synced        |
| 36     | test    |            | drop table    | none                 | 32        | 34       | 0         | 2019-01-10 11:29:59.982 +0800 CST | synced        |
| 35     | test    |            | create table  | public               | 32        | 34       | 0         | 2019-01-10 11:29:40.741 +0800 CST | synced        |
| 33     | test    |            | create schema | public               | 32        | 0        | 0         | 2019-01-10 11:29:22.813 +0800 CST | synced        |
+--------+---------+------------+---------------+----------------------+-----------+----------+-----------+-----------------------------------+---------------+
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
* `STATE`: the state of the DDL operations. The common states include:
    * `none`: it indicates that the operation task has been put in the DDL job queue but has not been performed yet, because it is waiting for the previous tasks to complete. Another reason might be that it becomes the `none` state after running the drop operation, but it will soon be updated to the `synced` state, which means that all TiDB instances have been synced to this state.
    * `running`: it indicates that the operation is being performed.
    * `synced`: it indicates that the operation has been performed successfully and all TiDB instances have been synced to this state.
    * `rollback done`: it indicates that the operation has failed and has finished rolling back.
    * `rollingback`: it indicates that the operation has failed and is rolling back.
    * `cancelling`: it indicates that the operation is being cancelled. This state only occurs when you cancel DDL tasks using the `ADMIN CANCEL DDL JOBS` command.

- `ADMIN SHOW DDL JOB QUERIES job_id [, job_id] ...`: To view the original SQL statement of the DDL task corresponding to the `job_id`; the `job_id` only searches the running DDL job and the last ten results in the DDL history job queue
- `ADMIN CANCEL DDL JOBS job_id [, job_id] ...`: To cancel the currently running DDL jobs and return whether the corresponding jobs are successfully cancelled. If the operation fails to cancel the jobs, specific reasons are displayed.

    > **Note:**
    >
    > - This operation can cancel multiple DDL jobs at the same time. You can get the ID of DDL jobs using the `ADMIN SHOW DDL JOBS` statement.
    > - If the jobs you want to cancel are finished, the cancellation operation fails.

- `ADMIN CHECK TABLE tbl_name [, tbl_name] ...`: To check the consistency of all the data in the specified table and corresponding indexes. If the check is passed, an empty result will be returned. On failure, an error message will indicate that data is inconsistent.

## MySQL compatibility

This statement is a TiDB extension to MySQL syntax.
