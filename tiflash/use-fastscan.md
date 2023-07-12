---
title: Use FastScan
summary: Introduces a way to speed up querying in OLAP scenarios by using FastScan.
aliases: ['/tidb/dev/sql-statement-set-tiflash-mode/','/tidb/dev/dev-guide-use-fastscan/']
---

# Use FastScan

This document describes how to use FastScan to speed up queries in Online Analytical Processing (OLAP) scenarios.

By default, TiFlash guarantees the precision of query results and data consistency. With the feature FastScan, TiFlash provides more efficient query performance, but does not guarantee the accuracy of query results and data consistency.

Some OLAP scenarios allow for some tolerance to the accuracy of the query results. In these cases, if you need higher query performance, you can enable the FastScan feature at the session or global level. You can choose whether to enable the FastScan feature by configuring the variable `tiflash_fastscan`.

## Restrictions

When the FastScan feature is enabled, your query results might include old data of a table. This means that you might get multiple historical versions of data with the same primary key or data that has been deleted.

For example:

```sql
CREATE TABLE t1 (a INT PRIMARY KEY, b INT);
ALTER TABLE t1 SET TIFLASH REPLICA 1;
INSERT INTO t1 VALUES(1,2);
INSERT INTO t1 VALUES(10,20);
UPDATE t1 SET b = 4 WHERE a = 1;
DELETE FROM t1 WHERE a = 10;
SET SESSION tidb_isolation_read_engines='tiflash';

SELECT * FROM t1;
+------+------+
| a    | b    |
+------+------+
|    1 |    4 |
+------+------+

SET SESSION tiflash_fastscan=ON;
SELECT * FROM t1;
+------+------+
| a    | b    |
+------+------+
|    1 |    2 |
|    1 |    4 |
|   10 |   20 |
+------+------+
```

Although TiFlash can automatically initiate compaction of old data in the background, the old data will not be cleaned up physically until it has been compacted and its data versions are older than the GC safe point. After the physical cleaning, the cleaned old data will no longer be returned in FastScan mode. The timing of data compaction is automatically triggered by various factors. You can also manually trigger data compaction using the [`ALTER TABLE ... COMPACT`](/sql-statements/sql-statement-alter-table-compact.md) statement.

## Enable and disable FastScan

By default, the variable is `tiflash_fastscan=OFF` at the session level and global level, that is, the FastScan feature is not enabled. You can view the variable information by using the following statement.

```
show variables like 'tiflash_fastscan';

+------------------+-------+
| Variable_name    | Value |
+------------------+-------+
| tiflash_fastscan | OFF   |
+------------------+-------+
```

```
show global variables like 'tiflash_fastscan';

+------------------+-------+
| Variable_name    | Value |
+------------------+-------+
| tiflash_fastscan | OFF   |
+------------------+-------+
```

You can configure the variable `tiflash_fastscan` at the session level and global level. If you need to enable FastScan in the current session, you can do so with the following statement:

```
set session tiflash_fastscan=ON;
```

You can also set `tiflash_fastscan` at the global level. The new setting will take effect in new sessions, but will not take effect in the current and previous sessions. Besides, in new sessions, `tiflash_fastscan` of the session level and global level will both take the new value.

```
set global tiflash_fastscan=ON;
```

You can disable FastScan using the following statement.

```
set session tiflash_fastscan=OFF;
set global tiflash_fastscan=OFF;
```

## Mechanism of FastScan

Data in the storage layer of TiFlash is stored in two layers: Delta layer and Stable layer.

By default, FastScan is not enabled, and the TableScan operator processes data in the following steps:

1. Read data: create separate data streams in the Delta layer and Stable layer to read the respective data.
2. Sort Merge: merge the data streams created in step 1. Then return the data after sorting in the order of (primary key column, timestamp column).
3. Range Filter: according to the data range, filter the data generated in step 2, and then return the data.
4. MVCC + Column Filter: filter the data generated in step 3 through MVCC (that is, filtering the data version according to the primary key column and the timestamp column) and through columns (that is, filtering out unneeded columns), and then return the data.

FastScan gains faster query speed by sacrificing some data consistency. Step 2 and the MVCC part in step 4 in the normal scan process are omitted in FastScan, thus improving query performance.
