---
title: TiFlash Late Materialization
summary: Describe how to use the TiFlash late materialization feature to accelerate queries in OLAP scenarios.
---

# TiFlash Late Materialization

> **Note:**
>
> TiFlash late materialization does not take effect in the [fast scan mode](/tiflash/use-fastscan.md).

TiFlash late materialization is an optimization method to accelerate queries in OLAP scenarios. You can use the [`tidb_opt_enable_late_materialization`](/system-variables.md#tidb_opt_enable_late_materialization-new-in-v700) system variable to control whether to enable or disable TiFlash late materialization.

- When it is disabled, to process a `SELECT` statement with filter conditions (`WHERE` clause), TiFlash reads all the data from the columns required by the query, and then filters and aggregates the data based on the query conditions.
- When it is enabled, TiFlash supports pushing down part of the filter conditions to the TableScan operator. That is, TiFlash first scans the column data related to the filter conditions that are pushed down to the TableScan operator, filters the rows that meet the condition, and then scans the other column data of these rows for further calculation, thereby reducing IO scans and computations of data processing.

To improve the performance of certain queries in OLAP scenarios, starting from v7.1.0, the TiFlash late materialization feature is enabled by default. The TiDB optimizer can determine which filter conditions to be pushed down based on statistics and filter conditions, and prioritize pushing down the filter conditions with high filtration rates. For detailed algorithms, see the [RFC document](https://github.com/pingcap/tidb/tree/master/docs/design/2022-12-06-support-late-materialization.md).

For example:

```sql
EXPLAIN SELECT a, b, c FROM t1 WHERE a < 1;
```

```
+-------------------------+----------+--------------+---------------+-------------------------------------------------------+
| id                      | estRows  | task         | access object | operator info                                         |
+-------------------------+----------+--------------+---------------+-------------------------------------------------------+
| TableReader_12          | 12288.00 | root         |               | MppVersion: 1, data:ExchangeSender_11                 |
| └─ExchangeSender_11     | 12288.00 | mpp[tiflash] |               | ExchangeType: PassThrough                             |
|   └─TableFullScan_9     | 12288.00 | mpp[tiflash] | table:t1      | pushed down filter:lt(test.t1.a, 1), keep order:false |
+-------------------------+----------+--------------+---------------+-------------------------------------------------------+
```

In this example, the filter condition `a < 1` is pushed down to the TableScan operator. TiFlash first reads all data from column `a`, and then filters the rows that meet the `a < 1` condition. Next, TiFlash reads columns `b` and `c` from these filtered rows.

## Enable or disable TiFlash late materialization

By default, the `tidb_opt_enable_late_materialization` system variable is `ON` at both the session and global levels, which means that the TiFlash late materialization feature is enabled. You can use the following statement to view the corresponding variable information:

```sql
SHOW VARIABLES LIKE 'tidb_opt_enable_late_materialization';
```

```
+--------------------------------------+-------+
| Variable_name                        | Value |
+--------------------------------------+-------+
| tidb_opt_enable_late_materialization | ON    |
+--------------------------------------+-------+
```

```sql
SHOW GLOBAL VARIABLES LIKE 'tidb_opt_enable_late_materialization';
```

```
+--------------------------------------+-------+
| Variable_name                        | Value |
+--------------------------------------+-------+
| tidb_opt_enable_late_materialization | ON    |
+--------------------------------------+-------+
```

You can modify the `tidb_opt_enable_late_materialization` variable at the session level or at the global level.

- To disable TiFlash late materialization in the current session, use the following statement:

    ```sql
    SET SESSION tidb_opt_enable_late_materialization=OFF;
    ```

- To disable TiFlash late materialization at the global level, use the following statement:

    ```sql
    SET GLOBAL tidb_opt_enable_late_materialization=OFF;
    ```

    After this setting, the `tidb_opt_enable_late_materialization` variable will be enabled by default for both session and global levels in new sessions.

To enable TiFlash late materialization, use the following statements:

```sql
SET SESSION tidb_opt_enable_late_materialization=ON;
```

```sql
SET GLOBAL tidb_opt_enable_late_materialization=ON;
```

## Implementation mechanism

When filter conditions are pushed down to the TableScan operator, the execution process of the TableScan operator mainly includes the following steps:

1. Reads the three columns `<handle, del_mark, version>`, performs multi-version concurrency control (MVCC) filtering, and then generates the MVCC Bitmap.
2. Reads the columns related to the filter conditions, filters the rows that meet the conditions, and then generates the Filter Bitmap.
3. Performs an `AND` operation between the MVCC Bitmap and Filter Bitmap to generate the Final Bitmap.
4. Reads the corresponding rows of the remaining columns according to the Final Bitmap.
5. Merges the data read in steps 2 and 4, and then returns the results.
