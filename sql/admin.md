---
title: Database Administration Statements
summary: Use administration statements to manage the TiDB database. 
category: user guide
---

# Database Administration Statements

TiDB manages the database using a number of statements, including granting privileges, modifying system variables, and querying database status.

## Privilege management

See [Privilege Management](../sql/privilege.md).

## `SET` statement

The `SET` statement has multiple functions and forms.

### Assign values to variables

```sql
SET variable_assignment [, variable_assignment] ...

variable_assignment:
      user_var_name = expr
    | param_name = expr
    | local_var_name = expr
    | [GLOBAL | SESSION]
        system_var_name = expr
    | [@@global. | @@session. | @@]
        system_var_name = expr
```

You can use the above syntax to assign values to variables in TiDB, which include system variables and user-defined variables. All user-defined variables are session variables. The system variables set using `@@global.` or `GLOBAL` are global variables, otherwise session variables. For more information, see [The System Variables](../sql/variable.md).

### `SET CHARACTER` statement and `SET NAMES`

```sql
SET {CHARACTER SET | CHARSET}
    {'charset_name' | DEFAULT}

SET NAMES {'charset_name'
    [COLLATE 'collation_name'] | DEFAULT}
```

This statement sets three session system variables (`character_set_client`, `character_set_results` and `character_set_connection`) as given character set. Currently, the value of `character_set_connection` differs from MySQL and is set as the value of `character_set_database` in MySQL.

### Set the password

```sql
SET PASSWORD [FOR user] = password_option

password_option: {
    'auth_string'
  | PASSWORD('auth_string')
}
```

This statement is used to set user passwords. For more information, see [Privilege Management](../sql/privilege.md).

### Set the isolation level

```sql
SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;
```

This statement is used to set the transaction isolation level. For more information, see [Transaction Isolation Level](../sql/transaction.md#transaction-isolation-level).

## `SHOW` statement

TiDB supports part of `SHOW` statements, used to view the Database/Table/Column information and the internal status of the database. Currently supported statements:

```sql
# Supported and similar to MySQL
SHOW CHARACTER SET [like_or_where]
SHOW COLLATION [like_or_where]
SHOW [FULL] COLUMNS FROM tbl_name [FROM db_name] [like_or_where]
SHOW CREATE {DATABASE|SCHEMA} db_name
SHOW CREATE TABLE tbl_name
SHOW DATABASES [like_or_where]
SHOW GRANTS FOR user
SHOW INDEX FROM tbl_name [FROM db_name]
SHOW PRIVILEGES
SHOW [FULL] PROCESSLIST
SHOW [GLOBAL | SESSION] STATUS [like_or_where]
SHOW TABLE STATUS [FROM db_name] [like_or_where]
SHOW [FULL] TABLES [FROM db_name] [like_or_where]
SHOW [GLOBAL | SESSION] VARIABLES [like_or_where]
SHOW WARNINGS

# Supported to improve compatibility but return null results
SHOW ENGINE engine_name {STATUS | MUTEX}
SHOW [STORAGE] ENGINES
SHOW PLUGINS
SHOW PROCEDURE STATUS [like_or_where]
SHOW TRIGGERS [FROM db_name] [like_or_where]
SHOW EVENTS
SHOW FUNCTION STATUS [like_or_where]
SHOW MASTER STATUS

# TiDB-specific statements for viewing statistics
SHOW STATS_META [like_or_where]
SHOW STATS_HISTOGRAMS [like_or_where]
SHOW STATS_BUCKETS [like_or_where]


like_or_where:
    LIKE 'pattern'
  | WHERE expr
```

> **Note:**
> 
> - To view statistics using the `SHOW` statement, see [View Statistics](../sql/statistics.md#view-statistics).
> - For more information about the `SHOW` statement, see [SHOW Syntax in MySQL](https://dev.mysql.com/doc/refman/5.7/en/show.html).

The `UniqueID` field returned from `SHOW MASTER STATUS` is the current `TSO` obtained directly from `PD`. The `TSO` is used during binlog increment and [`mydumper`](../tools/mydumper.md) synchronization.

```sql
mysql> show master status;
+-------------|--------------------|--------------|------------------|-------------------+
| File        | UniqueID           | Binlog_Do_DB | Binlog_Ignore_DB | Executed_Gtid_Set |
+-------------|--------------------|--------------|------------------|-------------------+
| tidb-binlog | 403756327834484736 |              |                  |                   |
+-------------|--------------------|--------------|------------------|-------------------+
1 row in set (0.00 sec)
```

## `ADMIN` statement

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
- `ADMIN CHECK TABLE tbl_name [, tbl_name] ...`: To check the consistency of all the data in the specified table and corresponding indexes. If the check is passed, an empty result will be returned. On failure, an error message will indicate that data is inconsistent.

  > **Note:**
  >
  > - This operation can cancel multiple DDL jobs at the same time. You can get the ID of DDL jobs using the `ADMIN SHOW DDL JOBS` statement. 
  > - If the jobs you want to cancel are finished, the cancellation operation fails. 
