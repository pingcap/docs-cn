---
title: ALTER TABLE ... SET TIFLASH MODE ...
summary: An overview of the usage of ALTER TABLE ... SET TIFLASH MODE ... for the TiDB database.
---

# `ALTER TABLE ... SET TIFLASH MODE ...`

> **Warning:**
>
> This statement is still an experimental feature. It is NOT recommended that you use it in the production environment.

You can use the `ALTER TABLE...SET TIFLASH MODE...` statement to switch the mode of the corresponding table in TiFlash. The following modes are currently supported.

- `Normal Mode`. The default mode. This mode guarantees the accuracy of query results and data consistency.
- `Fast Mode`. This mode does not guarantee the accuracy of query results and data consistency, but provides more efficient query performance.

This statement executes without blocking the execution of existing SQL statements or the running of TiDB features, such as transactions, DDL, and GC, and without changing the data content accessed through the SQL statement. The statement will end normally when the mode switch is completed.

This statement only supports changing the mode to tables in TiFlash, so the mode change only affects reads involving the TiFlash table.

The mode change to tables in TiFlash takes effect only if the table has a TiFlash Replica. If the TiFlash Replica of the table is empty when you change the mode, the mode will take effect only after the TiFlash Replica is subsequently reset. You can use [`ALTER TABLE ... SET TIFLASH REPLICA ...`](/sql-statements/sql-statement-alter-table.md) to reset the TiFlash Replica.

You can query the current TiFlash table mode of the corresponding table using the system table `information_schema.tiflash_replica`.

## Synopsis

```ebnf+diagram
AlterTableSetTiFlashModeStmt ::=
    'ALTER' 'TABLE' TableName 'SET' 'TIFLASH' 'MODE' mode
```

## Example

Assume that the `test` table has a TiFlash replica.

```sql
USE TEST;
CREATE TABLE test (a INT NOT NULL, b INT);
ALTER TABLE test SET TIFLASH REPLICA 1;
```

The default mode of the `test` table is Normal Mode. You can query the table mode with the following statement.

```sql
SELECT table_mode FROM information_schema.tiflash_replica WHERE table_name = 'test' AND table_schema = 'test'
```

```
+------------+
| table_mode |
+------------+
| NORMAL     |
+------------+
```

If you want to enable Fast Mode to query the `test` table, execute the following statement to switch the mode, and you can query the mode of the current table.

```sql
ALTER TABLE test SET tiflash mode FAST
SELECT table_mode FROM information_schema.tiflash_replica WHERE table_name = 'test' AND table_schema = 'test'
```

```
+------------+
| table_mode |
+------------+
| FAST       |
+------------+
```

If you want to switch back to Normal Mode mode, execute the following statement to switch.

```sql
ALTER TABLE test SET tiflash mode NORMAL
```

## MySQL compatibility

`ALTER TABLE ... SET TiFLASH MODE ...` is an extension to the standard SQL syntax introduced by TiDB. Although there is no equivalent MySQL syntax, you can still execute this statement from a MySQL client, or from database drivers that follow the MySQL protocol.

## TiDB Binlog and TiCDC compatibility

When the downstream is also TiDB, `ALTER TABLE ... SET TiFLASH MODE ...` will be synchronized downstream by TiDB Binlog. In other scenarios, TiDB Binlog does not synchronize this statement.

Fast mode does not support TiCDC.

## See also

- [ALTER TABLE](/sql-statements/sql-statement-alter-table.md)