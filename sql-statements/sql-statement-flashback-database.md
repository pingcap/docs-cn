---
title: FLASHBACK DATABASE
summary: Learn the usage of FLASHBACK DATABASE in TiDB databases.
---

# FLASHBACK DATABASE

TiDB v6.4.0 introduces the `FLASHBACK DATABASE` syntax. You can use `FLASHBACK DATABASE` to restore a database and its data that are deleted by the `DROP` statement within the Garbage Collection (GC) life time.

You can set the retention time of historical data by configuring the [`tidb_gc_life_time`](/system-variables.md#tidb_gc_life_time-new-in-v50) system variable. The default value is `10m0s`. You can query the current `safePoint`, that is, the time point GC has been performed up to, using the following SQL statement:

```sql
SELECT * FROM mysql.tidb WHERE variable_name = 'tikv_gc_safe_point';
```

As long as a database is deleted by `DROP` after the `tikv_gc_safe_point` time, you can use `FLASHBACK DATABASE` to restore the database.

## Syntax

```sql
FLASHBACK DATABASE DBName [TO newDBName]
```

### Synopsis

```ebnf+diagram
FlashbackDatabaseStmt ::=
    'FLASHBACK' DatabaseSym DBName FlashbackToNewName
FlashbackToNewName ::=
    ( 'TO' Identifier )?
```

## Notes

* If the database is deleted before the `tikv_gc_safe_point` time, you cannot restore the data using the `FLASHBACK DATABASE` statement. The `FLASHBACK DATABASE` statement returns an error similar to `ERROR 1105 (HY000): Can't find dropped database 'test' in GC safe point 2022-11-06 16:10:10 +0800 CST`.

* You cannot restore the same database multiple times using the `FLASHBACK DATABASE` statement. Because the database restored by `FLASHBACK DATABASE` has the same schema ID as the original database, restoring the same database multiple times leads to duplicate schema IDs. In TiDB, the database schema ID must be globally unique.

* When TiDB Binlog is enabled, note the following when you use `FLASHBACK DATABASE`:

    * The downstream secondary database must support `FLASHBACK DATABASE`.
    * The GC life time of the secondary database must be longer than that of the primary database. Otherwise, the latency between the upstream and the downstream might lead to data restoration failure in the downstream.
    * If TiDB Binlog replication encounters an error, you need to filter out the database in TiDB Binlog and then manually import full data for this database.

## Example

- Restore the `test` database that is deleted by `DROP`:

    ```sql
    DROP DATABASE test;
    ```

    ```sql
    FLASHBACK DATABASE test;
    ```

- Restore the `test` database that is deleted by `DROP` and rename it to `test1`:

    ```sql
    DROP DATABASE test;
    ```

    ```sql
    FLASHBACK DATABASE test TO test1;
    ```

## MySQL compatibility

This statement is a TiDB extension to MySQL syntax.
