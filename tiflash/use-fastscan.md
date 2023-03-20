---
title: Use FastScan
summary: Introduces a way to speed up querying in OLAP scenarios by using FastScan.
aliases: ['/tidb/dev/sql-statement-set-tiflash-mode/','/tidb/dev/dev-guide-use-fastscan/']
---

# Use FastScan

This document describes how to use FastScan to speed up queries in Online Analytical Processing (OLAP) scenarios.

By default, TiFlash guarantees the precision of query results and data consistency. With the feature FastScan, TiFlash provides more efficient query performance, but does not guarantee the accuracy of query results and data consistency.

Some OLAP scenarios allow for some tolerance to the accuracy of the query results. In these cases, if you need higher query performance, you can enable the FastScan feature at the session or global level. You can choose whether to enable the FastScan feature by configuring the variable `tiflash_fastscan`.

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
2. Sort Merge: merge the data streams created in step 1. Then return the data after sorting in (handle, version) order.
3. Range Filter: according to the data range, filter the data generated in step 2, and then return the data.
4. MVCC + Column Filter: filter the data generated in step 3 through MVCC and filter out unneeded columns, and then return the data.

FastScan gains faster query speed by sacrificing some data consistency. Step 2 and the MVCC part in step 4 in the normal scan process are omitted in FastScan, thus improving query performance.
