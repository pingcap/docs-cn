---
title: ALTER TABLE ... SET TIFLASH MODE ...
summary: An overview of the usage of ALTER TABLE ... SET TIFLASH MODE ... for the TiDB database.
---

# `ALTER TABLE ... SET TIFLASH MODE ...`

> **Warning:**
>
> This statement is experimental and its form and usage may change in subsequent versions.

You can use the `ALTER TABLE...SET TIFLASH MODE...` statement to enable or disable FastScan on the corresponding table in TiFlash:

- `Normal Mode`: the default option. In this mode, FastScan is disabled and the accuracy of query results and data consistency are guaranteed.
- `Fast Mode`: in this mode, FastScan is enabled. TiFlash provides more efficient query performance, but does not guarantee the accuracy of query results and data consistency.

The execution of `ALTER TABLE ... SET TIFLASH MODE ...` does not block existing SQL statements or interrupt other TiDB features, such as transactions, DDL, and GC. At the same time, data accessed through SQL statements is not altered. This statement ends normally when the mode is switched.

You can only execute this statement to switch the FastScan option for tables in TiFlash. Therefore, option change only affects reading tables in TiFlash.

The FastScan switch takes effect only if the table has TiFlash replicas. If no TiFlash replica is present when you switch the option, the option takes effect only after TiFlash replicas are configured. You can use [`ALTER TABLE ... SET TIFLASH REPLICA ...`](/sql-statements/sql-statement-alter-table.md) to configure TiFlash replicas.

You can query the current TiFlash table switch of the corresponding table using the system table `information_schema.tiflash_replica`.

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

The default option of the `test` table is Normal Mode. You can query the table option with the following statement.

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

To enable FastScan for the `test` table, execute the following statement and then check whether FastScan is enabled for this table.

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

To disable FastScan, execute the following statement.

```sql
ALTER TABLE test SET tiflash mode NORMAL
```

## MySQL compatibility

`ALTER TABLE ... SET TiFLASH MODE ...` is an extension to the standard SQL syntax introduced by TiDB. Although there is no equivalent MySQL syntax, you can still execute this statement from a MySQL client, or from database drivers that follow the MySQL protocol.

## TiDB Binlog and TiCDC compatibility

When the downstream is also TiDB, `ALTER TABLE ... SET TiFLASH MODE ...` will be synchronized downstream by TiDB Binlog. In other scenarios, TiDB Binlog does not synchronize this statement.

FastScan does not support TiCDC.

## See also

- [ALTER TABLE](/sql-statements/sql-statement-alter-table.md)