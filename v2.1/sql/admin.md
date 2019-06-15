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

The `UniqueID` field returned from `SHOW MASTER STATUS` is the current `TSO` obtained directly from `PD`. The `TSO` is used during binlog increment and [`mydumper`](../tools/mydumper.md) replication.

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

This statement is a TiDB extension syntax, used to view the status of TiDB.

```sql
ADMIN SHOW DDL
ADMIN SHOW DDL JOBS
ADMIN SHOW DDL JOB QUERIES job_id [, job_id] ...
ADMIN CANCEL DDL JOBS job_id [, job_id] ...
```

- `ADMIN SHOW DDL`: To view the currently running DDL jobs.
- `ADMIN SHOW DDL JOBS`: To view all the results in the current DDL job queue (including tasks that are running and waiting to be run) and the last ten results in the completed DDL job queue.
- `ADMIN SHOW DDL JOB QUERIES job_id [, job_id] ...`: To view the original SQL statement of the DDL task corresponding to the `job_id`; the `job_id` only searches the running DDL job and the last ten results in the DDL history job queue
- `ADMIN CANCEL DDL JOBS job_id [, job_id] ...`: To cancel the currently running DDL jobs and return whether the corresponding jobs are successfully cancelled. If the operation fails to cancel the jobs, specific reasons are displayed.

  > **Note:**
  >
  > - This operation can cancel multiple DDL jobs at the same time. You can get the ID of DDL jobs using the `ADMIN SHOW DDL JOBS` statement. 
  > - If the jobs you want to cancel are finished, the cancellation operation fails. 
