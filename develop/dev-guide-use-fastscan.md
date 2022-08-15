---
title: FastScan
summary: Introduces a way to speed up querying in OLAP scenarios by using FastScan.
---

# FastScan

> **Warning:**
>
> This feature is experimental and its form and usage may change in subsequent versions.

This document describes how to use FastScan to speed up queries in Online Analytical Processing (OLAP) scenarios.

By default, TiFlash guarantees the precision of query results and data consistency. With the feature FastScan, TiFlash provides more efficient query performance, but does not guarantee the accuracy of query results and data consistency.

Some OLAP scenarios allow for some tolerance to the accuracy of the query results. In these cases, if you need higher query performance, you can enable FastScan for the corresponding table for querying.

FastScan takes effect globally on tables that you enable FastScan by running [ALTER TABLE SET TIFLASH MODE](/sql-statements/sql-statement-set-tiflash-mode.md). TiFlash-related operations are not supported for temporary tables, in-memory tables, system tables, and tables with non-UTF-8 characters in column names.

For more information, see [ALTER TABLE SET TIFLASH MODE](/sql-statements/sql-statement-set-tiflash-mode.md).

## Enable FastScan

By default, FastScan is disabled for all tables. You can use the following statement to view the FastScan status.

```sql
SELECT table_mode FROM information_schema.tiflash_replica WHERE table_name = 'table_name' AND table_schema = 'database_name'
```

Use the following statement to enable FastScan for the corresponding table.

```sql
ALTER TABLE table_name SET TIFLASH MODE FAST
```

Once enabled, subsequent queries of this table in TiFlash will use the function of FastScan.

You can disable FastScan using the following statement.

```sql
ALTER TABLE table_name SET TIFLASH MODE NORMAL
```

## Mechanism of FastScan

Data in the storage layer of TiFlash is stored in two layers: Delta layer and Stable layer.

In Normal Mode, the TableScan operator processes data in the following steps:

1. Read data: create separate data streams in the Delta layer and Stable layer to read the respective data.
2. Sort Merge: merge the data streams created in step 1. Then return the data after sorting in (handle, version) order.
3. Range Filter: according to the data range, filter the data generated in step 2, and then return the data.
4. MVCC + Column Filter: filter the data generated in step 3 through MVCC and filter out unneeded columns, and then return the data.

FastScan gains faster query speed by sacrificing some data consistency. Step 2 and the MVCC part in step 4 in the normal scan process are omitted in FastScan, thus improving query performance.
