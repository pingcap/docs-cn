---
title: Fast Mode
summary: Introduces a way to speed up the querying of OLAP scenarios by using Fast Mode.
---

# Fast Mode

> **Warning:**
>
> This feature is still an experimental feature. It is NOT recommended that you use it in the production environment.

This document describes how to use Fast Mode to speed up queries in Online Analytical Processing (OLAP) scenarios.

TiFlash supports the following modes:

- `Normal Mode`. The default mode. This mode guarantees the precision of query results and data consistency.
- `Fast Mode`. This mode does not guarantee the accuracy of query results and data consistency, but provides more efficient query performance.

Some OLAP scenarios allow for some tolerance to the accuracy of the query results. In these cases, if you need higher query performance, you can switch the corresponding table to TiFlash's Fast Mode for querying.

The mode switch takes effect globally only for those tables whose mode is set to Fast Mode by [ALTER TABLE SET TIFLASH MODE](/sql-statements/sql-statement-set-tiflash-mode.md). TiFlash-related operations are not supported for temporary tables, in-memory tables, system tables, and tables with non-utf-8 characters in the column names, and therefore changing TiFlash table mode is not supported for them.

For more information, see [ALTER TABLE SET TIFLASH MODE](/sql-statements/sql-statement-set-tiflash-mode.md).

## Switch to Fast Mode

By default, all tables are in Normal Mode. You can use the following statement to view the current table mode.

```sql
SELECT table_mode FROM information_schema.tiflash_replica WHERE table_name = 'table_name' AND table_schema = 'database_name'
```

Use the following statement to switch the corresponding table to Fast Mode.

```sql
ALTER TABLE table_name SET TIFLASH MODE FAST
```

Once the switch is complete, subsequent queries in TiFlash will be performed in Fast Mode.

You can switch back to Normal Mode using the following statement.

```sql
ALTER TABLE table_name SET TIFLASH MODE NORMAL
```

## Mechanism of Fast Mode

The data in the storage layer of TiFlash is stored in two layers: Delta layer and Stable layer.

The overall TableScan algorithm process in Normal Mode consists of the following steps:

1. Read data: separate data streams are created in the Delta layer and Stable layer to read the respective data.
2. Sort Merge: the data streams created in Step 1 are sorted and merged, and the data is returned in (handle, version) order.
3. Range Filter: according to the data range, filter the data generated in Step 2, and then return the data.
4. MVCC + Column Filter: filter the data generated in step 3 through MVCC. Meanwhile, filter out the unneeded columns, and then return the data.

Fast Mode gains faster query performance by sacrificing some data consistency. The TableScan process in Fast Mode omits Step 2 and the MVCC part in Step 4 in the Normal Mode process, thus improving query performance.
