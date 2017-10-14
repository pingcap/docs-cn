---
title: Database Administration Statements
category: user guide
---

# Database Administration Statements

TiDB manages the database using a number of statements, including granting privileges, modifying system variables, and querying database status.

## Privilege Management

See [Privilege Management](privilege.md).

## `SET` Statement

The `SET` statement has multiple functions and forms.

### Assign Values to Variables

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

You can use the above syntax to assign values to variables in TiDB, which include system variables and user-defined variables. All user-defined variables are session variables. The system variables set using `@@global.` or `GLOBAL` are global variables, otherwise session variables. For more information, see [The System Variables](variable.md).

### `SET CHARACTER` Statement and `SET NAMES`

```sql
SET {CHARACTER SET | CHARSET}
    {'charset_name' | DEFAULT}

SET NAMES {'charset_name'
    [COLLATE 'collation_name'] | DEFAULT}
```

This statement sets three session system variables (`character_set_client`, `character_set_results` and `character_set_connection`) as given character set. Currently, the value of `character_set_connection` differs from MySQL and is set as the value of `character_set_database` in MySQL.

### Set the Password

```sql
SET PASSWORD [FOR user] = password_option

password_option: {
    'auth_string'
  | PASSWORD('auth_string')
}
```

This statement is used to set user passwords. For more information, see [Privilege Management](privilege.md).

### Set the Isolation Level

```sql
SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;
```

This statement is used to set the transaction isolation level. For more information, see [Transaction Isolation Level](transaction.md#transaction-isolation-level).

## `SHOW` Statement

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

# TiDB-specific statements for viewing statistics
SHOW STATS_META [like_or_where]
SHOW STATS_HISTOGRAMS [like_or_where]
SHOW STATS_BUCKETS [like_or_where]


like_or_where:
    LIKE 'pattern'
  | WHERE expr
```

> **Note**:
> 
> - To view statistics using the `SHOW` statement, see [View Statistics](statistics.md#view-statistics).
> - For more information about the `SHOW` statement, see [SHOW Syntax in MySQL](https://dev.mysql.com/doc/refman/5.7/en/show.html).

## `ADMIN` Statement

This statement is a TiDB extension syntax, used to view the status of TiDB.

```sql
ADMIN SHOW DDL
ADMIN SHOW DDL JOBS
```

- `ADMIN SHOW DDL`: To view the currently running DDL jobs  
- `ADMIN SHOW DDL JOBS`: To view all the results in the current DDL job queue (including tasks that are running and waiting to be run) and the last ten results in the completed DDL job queue
