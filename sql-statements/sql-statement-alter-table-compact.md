---
title: ALTER TABLE ... COMPACT
summary: An overview of the usage of ALTER TABLE ... COMPACT for the TiDB database.
---

# ALTER TABLE ... COMPACT

To enhance read performance and reduce disk usage, TiDB automatically schedules data compaction on storage nodes in the background. During the compaction, storage nodes rewrite physical data, including cleaning up deleted rows and merging multiple versions of data caused by updates. The `ALTER TABLE ... COMPACT` statement allows you to initiate compaction for a specific table immediately, without waiting until compaction is triggered in the background.

The execution of this statement does not block existing SQL statements or affect any TiDB features, such as transactions, DDL, and GC. Data that can be selected via SQL statements will not be changed either. Executing this statement consumes some IO and CPU resources. Be careful to choose an appropriate timing for execution, such as when resources are available, to avoid negative impact on the business.

The compaction statement will be finished and returned when all replicas of a table are compacted. During the execution process, you can safely interrupt the compaction by executing the [`KILL`](/sql-statements/sql-statement-kill.md) statement. Interrupting a compaction does not break data consistency or lead to data loss, nor does it affect subsequent manual or background compactions.

This data compaction statement is currently supported only for TiFlash replicas, not for TiKV replicas.

## Synopsis

```ebnf+diagram
AlterTableCompactStmt ::=
    'ALTER' 'TABLE' TableName 'COMPACT' ( 'PARTITION' PartitionNameList )? ( 'TIFLASH' 'REPLICA' )?
```

Since v6.2.0, the `TIFLASH REPLICA` part of the syntax can be omitted. When omitted, the semantic of the statement remains unchanged, and takes effect only for TiFlash.

## Examples

### Compact TiFlash replicas in a table

The following takes an `employees` table as an example, which has 4 partitions with 2 TiFlash replicas:

```sql
CREATE TABLE employees (
    id INT NOT NULL,
    hired DATE NOT NULL DEFAULT '1970-01-01',
    store_id INT
)
PARTITION BY LIST (store_id) (
    PARTITION pNorth VALUES IN (1, 2, 3, 4, 5),
    PARTITION pEast VALUES IN (6, 7, 8, 9, 10),
    PARTITION pWest VALUES IN (11, 12, 13, 14, 15),
    PARTITION pCentral VALUES IN (16, 17, 18, 19, 20)
);
ALTER TABLE employees SET TIFLASH REPLICA 2;
```

You can execute the following statement to immediately initiate the compaction for the 2 TiFlash replicas for all partitions in the `employees` table:

{{< copyable "sql" >}}

```sql
ALTER TABLE employees COMPACT TIFLASH REPLICA;
```

### Compact TiFlash replicas of specified partitions in a table

The following takes an `employees` table as an example, which has 4 partitions with 2 TiFlash replicas:

```sql
CREATE TABLE employees (
    id INT NOT NULL,
    hired DATE NOT NULL DEFAULT '1970-01-01',
    store_id INT
)
PARTITION BY LIST (store_id) (
    PARTITION pNorth VALUES IN (1, 2, 3, 4, 5),
    PARTITION pEast VALUES IN (6, 7, 8, 9, 10),
    PARTITION pWest VALUES IN (11, 12, 13, 14, 15),
    PARTITION pCentral VALUES IN (16, 17, 18, 19, 20)
);

ALTER TABLE employees SET TIFLASH REPLICA 2;
```

You can execute the following statement to immediately initiate the compaction for the 2 TiFlash replicas of the `pNorth` and `pEast` partitions in the `employees` table:

```sql
ALTER TABLE employees COMPACT PARTITION pNorth, pEast TIFLASH REPLICA;
```

## Concurrency

The `ALTER TABLE ... COMPACT` statement compacts all replicas in a table simultaneously.

To avoid a significant impact on online business, each TiFlash instance only compacts data in one table at a time by default (except for the compaction triggered in the background). This means that if you execute the `ALTER TABLE ... COMPACT` statement on multiple tables at the same time, their executions will be queued on the same TiFlash instance, rather than being executed simultaneously.

<CustomContent platform="tidb">

To obtain greater table-level concurrency with higher resource usage, you can modify the TiFlash configuration [`manual_compact_pool_size`](/tiflash/tiflash-configuration.md). For example, when `manual_compact_pool_size` is set to 2, compaction for 2 tables can be processed simultaneously.

</CustomContent>

## Observe data compaction progress

You can observe the progress of data compaction or determine whether to initiate compaction for a table by checking the `TOTAL_DELTA_ROWS` column in the `INFORMATION_SCHEMA.TIFLASH_TABLES` table. The larger the value of `TOTAL_DELTA_ROWS`, the more data that can be compacted. If `TOTAL_DELTA_ROWS` is `0`, all data in the table is in the best state and does not need to be compacted.

<details>
  <summary>Example: Check the compaction state of a non-partitioned table</summary>

```sql
USE test;

CREATE TABLE foo(id INT);

ALTER TABLE foo SET TIFLASH REPLICA 1;

SELECT TOTAL_DELTA_ROWS, TOTAL_STABLE_ROWS FROM INFORMATION_SCHEMA.TIFLASH_TABLES
    WHERE IS_TOMBSTONE = 0 AND
    `TIDB_DATABASE` = "test" AND `TIDB_TABLE` = "foo";
+------------------+-------------------+
| TOTAL_DELTA_ROWS | TOTAL_STABLE_ROWS |
+------------------+-------------------+
|                0 |                 0 |
+------------------+-------------------+

INSERT INTO foo VALUES (1), (3), (7);

SELECT TOTAL_DELTA_ROWS, TOTAL_STABLE_ROWS FROM INFORMATION_SCHEMA.TIFLASH_TABLES
    WHERE IS_TOMBSTONE = 0 AND
    `TIDB_DATABASE` = "test" AND `TIDB_TABLE` = "foo";
+------------------+-------------------+
| TOTAL_DELTA_ROWS | TOTAL_STABLE_ROWS |
+------------------+-------------------+
|                3 |                 0 |
+------------------+-------------------+
-- Newly written data can be compacted

ALTER TABLE foo COMPACT TIFLASH REPLICA;

SELECT TOTAL_DELTA_ROWS, TOTAL_STABLE_ROWS FROM INFORMATION_SCHEMA.TIFLASH_TABLES
    WHERE IS_TOMBSTONE = 0 AND
    `TIDB_DATABASE` = "test" AND `TIDB_TABLE` = "foo";
+------------------+-------------------+
| TOTAL_DELTA_ROWS | TOTAL_STABLE_ROWS |
+------------------+-------------------+
|                0 |                 3 |
+------------------+-------------------+
-- All data is in the best state and no compaction is needed
```

</details>

<details>
  <summary>Example: Check the compaction state of a partitioned table</summary>

```sql
USE test;

CREATE TABLE employees
    (id INT NOT NULL, store_id INT)
    PARTITION BY LIST (store_id) (
        PARTITION pNorth VALUES IN (1, 2, 3, 4, 5),
        PARTITION pEast VALUES IN (6, 7, 8, 9, 10),
        PARTITION pWest VALUES IN (11, 12, 13, 14, 15),
        PARTITION pCentral VALUES IN (16, 17, 18, 19, 20)
    );

ALTER TABLE employees SET TIFLASH REPLICA 1;

INSERT INTO employees VALUES (1, 1), (6, 6), (10, 10);

SELECT PARTITION_NAME, TOTAL_DELTA_ROWS, TOTAL_STABLE_ROWS
    FROM INFORMATION_SCHEMA.TIFLASH_TABLES t, INFORMATION_SCHEMA.PARTITIONS p
    WHERE t.IS_TOMBSTONE = 0 AND t.TABLE_ID = p.TIDB_PARTITION_ID AND
    p.TABLE_SCHEMA = "test" AND p.TABLE_NAME = "employees";
+----------------+------------------+-------------------+
| PARTITION_NAME | TOTAL_DELTA_ROWS | TOTAL_STABLE_ROWS |
+----------------+------------------+-------------------+
| pNorth         |                1 |                 0 |
| pEast          |                2 |                 0 |
| pWest          |                0 |                 0 |
| pCentral       |                0 |                 0 |
+----------------+------------------+-------------------+
-- Some partitions can be compacted

ALTER TABLE employees COMPACT TIFLASH REPLICA;

SELECT PARTITION_NAME, TOTAL_DELTA_ROWS, TOTAL_STABLE_ROWS
    FROM INFORMATION_SCHEMA.TIFLASH_TABLES t, INFORMATION_SCHEMA.PARTITIONS p
    WHERE t.IS_TOMBSTONE = 0 AND t.TABLE_ID = p.TIDB_PARTITION_ID AND
    p.TABLE_SCHEMA = "test" AND p.TABLE_NAME = "employees";
+----------------+------------------+-------------------+
| PARTITION_NAME | TOTAL_DELTA_ROWS | TOTAL_STABLE_ROWS |
+----------------+------------------+-------------------+
| pNorth         |                0 |                 1 |
| pEast          |                0 |                 2 |
| pWest          |                0 |                 0 |
| pCentral       |                0 |                 0 |
+----------------+------------------+-------------------+
-- Data in all partitions is in the best state and no compaction is needed
```

</details>

> **Note:**
>
> - If data is updated during compaction, `TOTAL_DELTA_ROWS` might still be a non-zero value after compaction is done. This is normal and indicates that these updates have not been compacted. To compact these updates, execute the `ALTER TABLE ... COMPACT` statement again.
>
> - `TOTAL_DELTA_ROWS` indicates the data version, not the number of rows. For example, if you insert a row and then delete it, `TOTAL_DELTA_ROWS` will increase by 2.

## Compatibility

### MySQL compatibility

The `ALTER TABLE ... COMPACT` syntax is TiDB specific, which is an extension to the standard SQL syntax. Although there is no equivalent MySQL syntax, you can still execute this statement by using MySQL clients or various database drivers that comply with the MySQL protocol.

### TiDB Binlog and TiCDC compatibility

The `ALTER TABLE ... COMPACT` statement does not result in logical data changes and are therefore not replicated to downstream by TiDB Binlog or TiCDC.

## See also

- [ALTER TABLE](/sql-statements/sql-statement-alter-table.md)
- [KILL TIDB](/sql-statements/sql-statement-kill.md)