---
title: The System Variables
summary: Learn how to use the system variables in TiDB.
category: reference
---

# The System Variables

The system variables in MySQL are the system parameters that modify the operation of the database runtime. These variables have two types of scope, Global Scope and Session Scope. TiDB supports all the system variables in MySQL 5.7. Most of the variables are only supported for compatibility and do not affect the runtime behaviors.

## Set the system variables

You can use the [`SET`](/reference/sql/statements/set-variable.md) statement to change the value of the system variables. Before you change, consider the scope of the variable. For more information, see [MySQL Dynamic System Variables](https://dev.mysql.com/doc/refman/5.7/en/dynamic-system-variables.html).

### Set Global variables

Add the `GLOBAL` keyword before the variable or use `@@global.` as the modifier:

```sql
SET GLOBAL autocommit = 1;
SET @@global.autocommit = 1;
```

### Set Session Variables

Add the `SESSION` keyword before the variable, use `@@session.` as the modifier, or use no modifier:

```sql
SET SESSION autocommit = 1;
SET @@session.autocommit = 1;
SET @@autocommit = 1;
```

> **Note:**
>
> `LOCAL` and `@@local.` are the synonyms for `SESSION` and `@@session.`

### The working mechanism of system variables

* Session variables will only initialize their own values based on global variables when a session is created. Changing a global variable does not change the value of the system variable being used by the session that has already been created.

    ```sql
    mysql> SELECT @@GLOBAL.autocommit;
    +---------------------+
    | @@GLOBAL.autocommit |
    +---------------------+
    | ON                  |
    +---------------------+
    1 row in set (0.00 sec)
    
    mysql> SELECT @@SESSION.autocommit;
    +----------------------+
    | @@SESSION.autocommit |
    +----------------------+
    | ON                   |
    +----------------------+
    1 row in set (0.00 sec)
    
    mysql> SET GLOBAL autocommit = OFF;
    Query OK, 0 rows affected (0.01 sec)
    
    mysql> SELECT @@SESSION.autocommit; -- Session variables do not change, and the transactions in the session are executed in the form of autocommit.
    +----------------------+
    | @@SESSION.autocommit |
    +----------------------+
    | ON                   |
    +----------------------+
    1 row in set (0.00 sec)
    
    mysql> SELECT @@GLOBAL.autocommit;
    +---------------------+
    | @@GLOBAL.autocommit |
    +---------------------+
    | OFF                 |
    +---------------------+
    1 row in set (0.00 sec)
    
    mysql> exit
    Bye
    $ mysql -h127.0.0.1 -P4000 -uroot -D test
    Welcome to the MySQL monitor.  Commands end with ; or \g.
    Your MySQL connection id is 3
    Server version: 5.7.25-TiDB-None MySQL Community Server (Apache License 2.0)
    
    Copyright (c) 2000, 2019, Oracle and/or its affiliates. All rights reserved.
    
    Oracle is a registered trademark of Oracle Corporation and/or its
    affiliates. Other names may be trademarks of their respective
    owners.
    
    Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.
    
    mysql> SELECT @@SESSION.autocommit; -- The newly created session uses a new global variable.
    +----------------------+
    | @@SESSION.autocommit |
    +----------------------+
    | OFF                  |
    +----------------------+
    1 row in set (0.00 sec)
    ```

## The fully supported MySQL system variables in TiDB

The following MySQL system variables are fully supported in TiDB and have the same behaviors as in MySQL.

| Name | Scope | Description |
| ---------------- | -------- | -------------------------------------------------- |
| autocommit | GLOBAL \| SESSION | whether automatically commit a transaction|
| sql_mode | GLOBAL \| SESSION | support some of the MySQL SQL modes|
| time_zone | GLOBAL \| SESSION | the time zone of the database |
| tx_isolation | GLOBAL \| SESSION | the isolation level of a transaction |
| hostname | NONE | the hostname of the TiDB server |

## TiDB Specific System Variables

See [TiDB Specific System Variables](/reference/configuration/tidb-server/tidb-specific-variables.md).
