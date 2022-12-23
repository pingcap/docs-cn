---
title: Cached Tables
summary: Learn the cached table feature in TiDB, which is used for rarely-updated small hotspot tables to improve read performance.
---

# Cached Tables

In v6.0.0, TiDB introduces the cached table feature for frequently accessed but rarely updated small hotspot tables. When this feature is used, the data of an entire table is loaded into the memory of the TiDB server, and TiDB directly gets the table data from the memory without accessing TiKV, which improves the read performance.

This document describes the usage scenarios of cached tables, the examples, and the compatibility restrictions with other TiDB features.

## Usage scenarios

The cached table feature is suitable for tables with the following characteristics:

- The data volume of the table is small.
- The table is read-only or rarely updated.
- The table is frequently accessed, and you expect a better read performance.

When the data volume of the table is small but the data is frequently accessed, the data is concentrated on a Region in TiKV and makes it a hotspot Region, which affects the performance. Therefore, the typical usage scenarios of cached tables are as follows:

- Configuration tables, from which applications read the configuration information.
- The tables of exchange rates in the financial sector. These tables are updated only once a day but not in real-time.
- Bank branch or network information tables, which are rarely updated.

Take configuration tables as an example. When the application restarts, the configuration information is loaded in all connections, which causes a high read latency. In this case, you can solve this problem by using the cached tables feature.

## Examples

This section describes the usage of cached tables by examples.

### Set a normal table to a cached table

Suppose that there is a table `users`:

{{< copyable "sql" >}}

```sql
CREATE TABLE users (
    id BIGINT,
    name VARCHAR(100),
    PRIMARY KEY(id)
);
```

To set this table to a cached table, use the `ALTER TABLE` statement:

{{< copyable "sql" >}}

```sql
ALTER TABLE users CACHE;
```

```sql
Query OK, 0 rows affected (0.01 sec)
```

### Verify a cached table

To verify a cached table, use the `SHOW CREATE TABLE` statement. If the table is cached, the returned result contains the `CACHED ON` attribute:

{{< copyable "sql" >}}

```sql
SHOW CREATE TABLE users;
```

```sql
+-------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Table | Create Table                                                                                                                                                                                                               |
+-------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| users | CREATE TABLE `users` (
  `id` bigint(20) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`) /*T![clustered_index] CLUSTERED */
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin /* CACHED ON */ |
+-------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

After reading data from a cached table, TiDB loads the data in memory. You can use the `trace` statement to check whether the data is loaded into memory. When the cache is not loaded, the returned result contains the `regionRequest.SendReqCtx` attribute, which indicates that TiDB reads data from TiKV.

{{< copyable "sql" >}}

```sql
TRACE SELECT * FROM users;
```

```sql
+------------------------------------------------+-----------------+------------+
| operation                                      | startTS         | duration   |
+------------------------------------------------+-----------------+------------+
| trace                                          | 17:47:39.969980 | 827.73µs   |
|   ├─session.ExecuteStmt                        | 17:47:39.969986 | 413.31µs   |
|   │ ├─executor.Compile                         | 17:47:39.969993 | 198.29µs   |
|   │ └─session.runStmt                          | 17:47:39.970221 | 157.252µs  |
|   │   └─TableReaderExecutor.Open               | 17:47:39.970294 | 47.068µs   |
|   │     └─distsql.Select                       | 17:47:39.970312 | 24.729µs   |
|   │       └─regionRequest.SendReqCtx           | 17:47:39.970454 | 189.601µs  |
|   ├─*executor.UnionScanExec.Next               | 17:47:39.970407 | 353.073µs  |
|   │ ├─*executor.TableReaderExecutor.Next       | 17:47:39.970411 | 301.106µs  |
|   │ └─*executor.TableReaderExecutor.Next       | 17:47:39.970746 | 6.57µs     |
|   └─*executor.UnionScanExec.Next               | 17:47:39.970772 | 17.589µs   |
|     └─*executor.TableReaderExecutor.Next       | 17:47:39.970776 | 6.59µs     |
+------------------------------------------------+-----------------+------------+
12 rows in set (0.01 sec)
```

After executing `trace` again, the returned result no longer contains the `regionRequest.SendReqCtx` attribute, which indicates that TiDB no longer reads data from TiKV but reads data from the memory instead.

{{< copyable "sql" >}}

```sql
+----------------------------------------+-----------------+------------+
| operation                              | startTS         | duration   |
+----------------------------------------+-----------------+------------+
| trace                                  | 17:47:40.533888 | 453.547µs  |
|   ├─session.ExecuteStmt                | 17:47:40.533894 | 402.341µs  |
|   │ ├─executor.Compile                 | 17:47:40.533903 | 205.54µs   |
|   │ └─session.runStmt                  | 17:47:40.534141 | 132.084µs  |
|   │   └─TableReaderExecutor.Open       | 17:47:40.534202 | 14.749µs   |
|   ├─*executor.UnionScanExec.Next       | 17:47:40.534306 | 3.21µs     |
|   └─*executor.UnionScanExec.Next       | 17:47:40.534316 | 1.219µs    |
+----------------------------------------+-----------------+------------+
7 rows in set (0.00 sec)
```

Note that the `UnionScan` operator is used to read the cached tables, so you can see `UnionScan` in the execution plan of the cached tables through `explain`:

{{< copyable "sql" >}}

```sql
+-------------------------+---------+-----------+---------------+--------------------------------+
| id                      | estRows | task      | access object | operator info                  |
+-------------------------+---------+-----------+---------------+--------------------------------+
| UnionScan_5             | 1.00    | root      |               |                                |
| └─TableReader_7         | 1.00    | root      |               | data:TableFullScan_6           |
|   └─TableFullScan_6     | 1.00    | cop[tikv] | table:users   | keep order:false, stats:pseudo |
+-------------------------+---------+-----------+---------------+--------------------------------+
3 rows in set (0.00 sec)
```

### Write data to a cached table

Cached tables support data writes. For example, you can insert a record into the `users` table:

{{< copyable "sql" >}}

```sql
INSERT INTO users(id, name) VALUES(1001, 'Davis');
```

```sql
Query OK, 1 row affected (0.00 sec)
```

{{< copyable "sql" >}}

```sql
SELECT * FROM users;
```

```sql
+------+-------+
| id   | name  |
+------+-------+
| 1001 | Davis |
+------+-------+
1 row in set (0.00 sec)
```

> **Note:**
>
> When you insert data to a cached table, second-level write latency might occur. The latency is controlled by the global environment variable [`tidb_table_cache_lease`](/system-variables.md#tidb_table_cache_lease-new-in-v600). You can decide whether to use the cached table feature by checking whether the latency is acceptable based on your application. For example, in a read-only scenario, you can increase the value of `tidb_table_cache_lease`:
>
> ```sql
> set @@global.tidb_table_cache_lease = 10;
> ```
>
> The write latency of cached tables is high, because the cached table feature is implemented with a complex mechanism that requires a lease to be set for each cache. When there are multiple TiDB instances, one instance does not know whether the other instances have cached data. If an instance modifies the table data directly, the other instances read the old cache data. To ensure correctness, the cached table implementation uses a lease mechanism to ensure that the data is not modified before the lease expires. That is why the write latency is high.

The metadata of cached tables is stored in the `mysql.table_cache_meta` table. This table records the IDs of all cached tables, the current lock status (`lock_type`), and the lock lease information (`lease`). This table is only internally used in TiDB and you are not recommended to modify it. Otherwise, unexpected errors might occur.

```sql
SHOW CREATE TABLE mysql.table_cache_meta\G
*************************** 1. row ***************************
       Table: table_cache_meta
Create Table: CREATE TABLE `table_cache_meta` (
  `tid` bigint(11) NOT NULL DEFAULT '0',
  `lock_type` enum('NONE','READ','INTEND','WRITE') NOT NULL DEFAULT 'NONE',
  `lease` bigint(20) NOT NULL DEFAULT '0',
  `oldReadLease` bigint(20) NOT NULL DEFAULT '0',
  PRIMARY KEY (`tid`) /*T![clustered_index] CLUSTERED */
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
1 row in set (0.00 sec)
```

### Revert a cached table to a normal table

> **Note:**
>
> Executing DDL statements on a cached table will fail. Before executing DDL statements on a cached table, you need to remove the cache attribute first and set the cached table back to a normal table.

{{< copyable "sql" >}}

```sql
TRUNCATE TABLE users;
```

```sql
ERROR 8242 (HY000): 'Truncate Table' is unsupported on cache tables.
```

{{< copyable "sql" >}}

```sql
mysql> ALTER TABLE users ADD INDEX k_id(id);
```

```sql
ERROR 8242 (HY000): 'Alter Table' is unsupported on cache tables.
```

To revert a cached table to a normal table, use `ALTER TABLE t NOCACHE`:

{{< copyable "sql" >}}

```sql
ALTER TABLE users NOCACHE;
```

```sql
Query OK, 0 rows affected (0.00 sec)
```

## Size limit of cached tables

Cached tables are only suitable for scenarios with small tables, because TiDB loads the data of an entire table into memory, and the cached data becomes invalid after modification and needs to be reloaded.

Currently, the size limit of a cached table is 64 MB in TiDB. If the table data exceeds 64 MB, executing `ALTER TABLE t CACHE` will fail.

## Compatibility restrictions with other TiDB features

Cached tables **DO NOT** support the following features:

- Performing the `ALTER TABLE t ADD PARTITION` operation on partitioned tables is not supported.
- Performing the `ALTER TABLE t CACHE` operation on temporary tables is not supported.
- Performing the `ALTER TABLE t CACHE` operation on views is not supported.
- Stale Read is not supported.
- Direct DDL operations on a cached table are not supported. You need to set the cached table back to a normal table first by using `ALTER TABLE t NOCACHE` before performing DDL operations.

Cached tables **CANNOT** be used in the following scenarios:

- Setting the system variable `tidb_snapshot` to read historical data.
- During modification, the cached data becomes invalid until the data is reloaded.

## Compatibility with TiDB migration tools

The cached table is a TiDB extension to MySQL syntax. Only TiDB can recognize the `ALTER TABLE ... CACHE` statement. TiDB migration tools **DO NOT** support cached tables, including Backup & Restore (BR), TiCDC, and Dumpling. These tools treat cached tables as normal tables.

That is to say, when a cached table is backed up and restored, it becomes a normal table. If the downstream cluster is a different TiDB cluster and you want to continue using the cached table feature, you can manually enable cached tables on the downstream cluster by executing `ALTER TABLE ... CACHE` on the downstream table.

## See also

* [ALTER TABLE](/sql-statements/sql-statement-alter-table.md)
* [System Variables](/system-variables.md)
