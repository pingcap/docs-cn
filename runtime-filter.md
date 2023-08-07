---
title: Runtime Filter
summary: Learn the working principles of Runtime Filter and how to use it.
---

# Runtime Filter

Runtime Filter is a new feature introduced in TiDB v7.3, which aims to improve the performance of hash join in MPP scenarios. By generating filters dynamically to filter the data of hash join in advance, TiDB can reduce the amount of data scanning and the amount of calculation of hash join at runtime, ultimately improving the query performance.

## Concepts

- Hash join: a way to implement the join relational algebra. It gets the result of Join by building a hash table on one side and continuously matching the hash table on the other side.
- Build side: one side of hash join used to build a hash table. In this document, the right table of hash join is called the build side by default.
- Probe side: one side of hash join used to continuously match the hash table. In this document, the left table of hash join is called the probe side by default.
- Filter: also known as predicate, which refers to the filter condition in this document.

## Working principles of Runtime Filter

Hash join performs the join operation by building a hash table based on the right table and continuously probing the hash table using the left table. If some join key values cannot hit the hash table during the probing process, it means that the data does not exist in the right table and will not appear in the final join result. Therefore, if TiDB can **filter out the join key data in advance** during scanning, it will reduce the scanning time and network overhead, thereby greatly improving the join efficiency.

Runtime Filter is a **dynamic predicate** generated during the query planning phase. This predicate has the same function as other predicates in the TiDB Selection operator. These predicates are all applied to the Table Scan operation to filter out rows that do not match the predicate. The only difference is that the parameter values in Runtime Filter come from the results generated during the hash join build process.

### Example

Assume that there is a join query between the `store_sales` table and the `date_dim` table, and the join method is hash join. `store_sales` is a fact table that mainly stores the sales data of stores, and the number of rows is 1 million. `date_dim` is a time dimension table that mainly stores date information. You want to query the sales data of the year 2001, so 365 rows of the `date_dim` table are involved in the join operation.

```sql
SELECT * FROM store_sales, date_dim
WHERE ss_date_sk = d_date_sk
    AND d_year = 2001;
```

The execution plan of hash join is usually as follows:

```
                 +-------------------+
                 | PhysicalHashJoin  |
        +------->|                   |<------+
        |        +-------------------+       |
        |                                    |
        |                                    |
  100w  |                                    | 365
        |                                    |
        |                                    |
+-------+-------+                   +--------+-------+
| TableFullScan |                   | TableFullScan  |
|  store_sales  |                   |    date_dim    |
+---------------+                   +----------------+
```

*(The above figure omits the exchange node and other nodes.)*

The execution process of Runtime Filter is as follows:

1. Scan the data of the `date_dim` table.
2. `PhysicalHashJoin` calculates a filter condition based on the data of the build side, such as `date_dim in (2001/01/01~2001/12/31)`.
3. Send the filter condition to the `TableFullScan` operator that is waiting to scan `store_sales`.
4. The filter condition is applied to `store_sales`, and the filtered data is passed to `PhysicalHashJoin`, thereby reducing the amount of data scanned by the probe side and the amount of calculation of matching the hash table.

```
                         2. Build RF values
            +-------->+-------------------+
            |         |PhysicalHashJoin   |<-----+
            |    +----+                   |      |
4. After RF |    |    +-------------------+      | 1. Scan T2
    5000    |    |3. Send RF                     |      365
            |    | filter data                   |
            |    |                               |
      +-----+----v------+                +-------+--------+
      |  TableFullScan  |                | TabelFullScan  |
      |  store_sales    |                |    date_dim    |
      +-----------------+                +----------------+
```

*(RF is short for Runtime Filter)*

From the above two figures, you can see that the amount of data scanned by `store_sales` is reduced from 1 million to 5000. By reducing the amount of data scanned by `TableFullScan`, Runtime Filter can reduce the number of times to match the hash table, avoiding unnecessary I/O and network transmission, thus significantly improving the efficiency of the join operation.

## Use Runtime Filter

To use Runtime Filter, you need to create a table with TiFlash replicas and set [`tidb_runtime_filter_mode`](/system-variables.md#tidb_runtime_filter_mode-new-in-v720) to `LOCAL`.

Taking the TPC-DS dataset as an example, this section uses the `catalog_sales` table and the `date_dim` table for join operations to illustrate how Runtime Filter improves query efficiency.

### Step 1. Create TiFlash replicas for tables to be joined

Add a TiFlash replica to each of the `catalog_sales` table and the `date_dim` table.

```sql
ALTER TABLE catalog_sales SET tiflash REPLICA 1;
ALTER TABLE date_dim SET tiflash REPLICA 1;
```

Wait until the TiFlash replicas of the two tables are ready, that is, the `AVAILABLE` and `PROGRESS` fields of the replicas are both `1`.

```sql
SELECT * FROM INFORMATION_SCHEMA.TIFLASH_REPLICA WHERE TABLE_NAME='catalog_sales';
+--------------+---------------+----------+---------------+-----------------+-----------+----------+
| TABLE_SCHEMA | TABLE_NAME    | TABLE_ID | REPLICA_COUNT | LOCATION_LABELS | AVAILABLE | PROGRESS |
+--------------+---------------+----------+---------------+-----------------+-----------+----------+
| tpcds50      | catalog_sales |     1055 |             1 |                 |         1 |        1 |
+--------------+---------------+----------+---------------+-----------------+-----------+----------+

SELECT * FROM INFORMATION_SCHEMA.TIFLASH_REPLICA WHERE TABLE_NAME='date_dim';
+--------------+------------+----------+---------------+-----------------+-----------+----------+
| TABLE_SCHEMA | TABLE_NAME | TABLE_ID | REPLICA_COUNT | LOCATION_LABELS | AVAILABLE | PROGRESS |
+--------------+------------+----------+---------------+-----------------+-----------+----------+
| tpcds50      | date_dim   |     1015 |             1 |                 |         1 |        1 |
+--------------+------------+----------+---------------+-----------------+-----------+----------+
```

### Step 2. Enable Runtime Filter

To enable Runtime Filter, set the value of the system variable [`tidb_runtime_filter_mode`](/system-variables.md#tidb_runtime_filter_mode-new-in-v720  ) to `LOCAL`.

```sql
SET tidb_runtime_filter_mode="LOCAL";
```

Check whether the change is successful:

```sql
SHOW VARIABLES LIKE "tidb_runtime_filter_mode";
+--------------------------+-------+
| Variable_name            | Value |
+--------------------------+-------+
| tidb_runtime_filter_mode | LOCAL |
+--------------------------+-------+
```

If the value of the system variable is `LOCAL`, Runtime Filter is enabled.

### Step 3. Execute the query

Before executing the query, use the [`EXPLAIN` statement](/sql-statements/sql-statement-explain.md) to show the execution plan and check whether Runtime Filter has taken effect.

```sql
EXPLAIN SELECT cs_ship_date_sk FROM catalog_sales, date_dim
WHERE d_date = '2002-2-01' AND
     cs_ship_date_sk = d_date_sk;
```

When Runtime Filter takes effect, the corresponding Runtime Filter is mounted on the `HashJoin` node and the `TableScan` node, indicating that Runtime Filter is applied successfully.

```
TableFullScan: runtime filter:0[IN] -> tpcds50.catalog_sales.cs_ship_date_sk
HashJoin: runtime filter:0[IN] <- tpcds50.date_dim.d_date_sk |
```

The complete query execution plan is as follows:

```
+----------------------------------------+-------------+--------------+---------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
| id                                     | estRows     | task         | access object       | operator info                                                                                                                                 |
+----------------------------------------+-------------+--------------+---------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
| TableReader_53                         | 37343.19    | root         |                     | MppVersion: 1, data:ExchangeSender_52                                                                                                         |
| └─ExchangeSender_52                    | 37343.19    | mpp[tiflash] |                     | ExchangeType: PassThrough                                                                                                                     |
|   └─Projection_51                      | 37343.19    | mpp[tiflash] |                     | tpcds50.catalog_sales.cs_ship_date_sk                                                                                                         |
|     └─HashJoin_48                      | 37343.19    | mpp[tiflash] |                     | inner join, equal:[eq(tpcds50.date_dim.d_date_sk, tpcds50.catalog_sales.cs_ship_date_sk)], runtime filter:0[IN] <- tpcds50.date_dim.d_date_sk |
|       ├─ExchangeReceiver_29(Build)     | 1.00        | mpp[tiflash] |                     |                                                                                                                                               |
|       │ └─ExchangeSender_28            | 1.00        | mpp[tiflash] |                     | ExchangeType: Broadcast, Compression: FAST                                                                                                    |
|       │   └─TableFullScan_26           | 1.00        | mpp[tiflash] | table:date_dim      | pushed down filter:eq(tpcds50.date_dim.d_date, 2002-02-01 00:00:00.000000), keep order:false                                                  |
|       └─Selection_31(Probe)            | 71638034.00 | mpp[tiflash] |                     | not(isnull(tpcds50.catalog_sales.cs_ship_date_sk))                                                                                            |
|         └─TableFullScan_30             | 71997669.00 | mpp[tiflash] | table:catalog_sales | pushed down filter:empty, keep order:false, runtime filter:0[IN] -> tpcds50.catalog_sales.cs_ship_date_sk                                     |
+----------------------------------------+-------------+--------------+---------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
9 rows in set (0.01 sec)
```

Now, execute the SQL query, and Runtime Filter is applied.

```sql
SELECT cs_ship_date_sk FROM catalog_sales, date_dim
WHERE d_date = '2002-2-01' AND
     cs_ship_date_sk = d_date_sk;
```

### Step 4. Performance comparison

This example uses the 50 GB TPC-DS data. After Runtime Filter is enabled, the query time is reduced from 0.38 seconds to 0.17 seconds, and efficiency is improved by 50%. You can use the `ANALYZE` statement to view the execution time of each operator after Runtime Filter takes effect.

The following is the execution information of the query when Runtime Filter is not enabled:

```sql
EXPLAIN ANALYZE SELECT cs_ship_date_sk FROM catalog_sales, date_dim WHERE d_date = '2002-2-01' AND cs_ship_date_sk = d_date_sk;
+----------------------------------------+-------------+----------+--------------+---------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------+---------+------+
| id                                     | estRows     | actRows  | task         | access object       | execution info                                                                                                                                                                                                                                                                                                                                                                                    | operator info                                                                                | memory  | disk |
+----------------------------------------+-------------+----------+--------------+---------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------+---------+------+
| TableReader_53                         | 37343.19    | 59574    | root         |                     | time:379.7ms, loops:83, RU:0.000000, cop_task: {num: 48, max: 0s, min: 0s, avg: 0s, p95: 0s, copr_cache_hit_ratio: 0.00}                                                                                                                                                                                                                                                                          | MppVersion: 1, data:ExchangeSender_52                                                        | 12.0 KB | N/A  |
| └─ExchangeSender_52                    | 37343.19    | 59574    | mpp[tiflash] |                     | tiflash_task:{proc max:377ms, min:375.3ms, avg: 376.1ms, p80:377ms, p95:377ms, iters:1160, tasks:2, threads:16}                                                                                                                                                                                                                                                                                   | ExchangeType: PassThrough                                                                    | N/A     | N/A  |
|   └─Projection_51                      | 37343.19    | 59574    | mpp[tiflash] |                     | tiflash_task:{proc max:377ms, min:375.3ms, avg: 376.1ms, p80:377ms, p95:377ms, iters:1160, tasks:2, threads:16}                                                                                                                                                                                                                                                                                   | tpcds50.catalog_sales.cs_ship_date_sk                                                        | N/A     | N/A  |
|     └─HashJoin_48                      | 37343.19    | 59574    | mpp[tiflash] |                     | tiflash_task:{proc max:377ms, min:375.3ms, avg: 376.1ms, p80:377ms, p95:377ms, iters:1160, tasks:2, threads:16}                                                                                                                                                                                                                                                                                   | inner join, equal:[eq(tpcds50.date_dim.d_date_sk, tpcds50.catalog_sales.cs_ship_date_sk)]    | N/A     | N/A  |
|       ├─ExchangeReceiver_29(Build)     | 1.00        | 2        | mpp[tiflash] |                     | tiflash_task:{proc max:291.3ms, min:290ms, avg: 290.6ms, p80:291.3ms, p95:291.3ms, iters:2, tasks:2, threads:16}                                                                                                                                                                                                                                                                                  |                                                                                              | N/A     | N/A  |
|       │ └─ExchangeSender_28            | 1.00        | 1        | mpp[tiflash] |                     | tiflash_task:{proc max:290.9ms, min:0s, avg: 145.4ms, p80:290.9ms, p95:290.9ms, iters:1, tasks:2, threads:1}                                                                                                                                                                                                                                                                                      | ExchangeType: Broadcast, Compression: FAST                                                   | N/A     | N/A  |
|       │   └─TableFullScan_26           | 1.00        | 1        | mpp[tiflash] | table:date_dim      | tiflash_task:{proc max:3.88ms, min:0s, avg: 1.94ms, p80:3.88ms, p95:3.88ms, iters:1, tasks:2, threads:1}, tiflash_scan:{dtfile:{total_scanned_packs:2, total_skipped_packs:12, total_scanned_rows:16384, total_skipped_rows:97625, total_rs_index_load_time: 0ms, total_read_time: 0ms}, total_create_snapshot_time: 0ms, total_local_region_num: 1, total_remote_region_num: 0}                  | pushed down filter:eq(tpcds50.date_dim.d_date, 2002-02-01 00:00:00.000000), keep order:false | N/A     | N/A  |
|       └─Selection_31(Probe)            | 71638034.00 | 71638034 | mpp[tiflash] |                     | tiflash_task:{proc max:47ms, min:34.3ms, avg: 40.6ms, p80:47ms, p95:47ms, iters:1160, tasks:2, threads:16}                                                                                                                                                                                                                                                                                        | not(isnull(tpcds50.catalog_sales.cs_ship_date_sk))                                           | N/A     | N/A  |
|         └─TableFullScan_30             | 71997669.00 | 71997669 | mpp[tiflash] | table:catalog_sales | tiflash_task:{proc max:34ms, min:17.3ms, avg: 25.6ms, p80:34ms, p95:34ms, iters:1160, tasks:2, threads:16}, tiflash_scan:{dtfile:{total_scanned_packs:8893, total_skipped_packs:4007, total_scanned_rows:72056474, total_skipped_rows:32476901, total_rs_index_load_time: 8ms, total_read_time: 579ms}, total_create_snapshot_time: 0ms, total_local_region_num: 194, total_remote_region_num: 0} | pushed down filter:empty, keep order:false                                                   | N/A     | N/A  |
+----------------------------------------+-------------+----------+--------------+---------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------+---------+------+
9 rows in set (0.38 sec)
```

The following is the execution information of the query when Runtime Filter is enabled:

```sql
EXPLAIN ANALYZE SELECT cs_ship_date_sk FROM catalog_sales, date_dim
    -> WHERE d_date = '2002-2-01' AND
    ->      cs_ship_date_sk = d_date_sk;
+----------------------------------------+-------------+---------+--------------+---------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+---------+------+
| id                                     | estRows     | actRows | task         | access object       | execution info                                                                                                                                                                                                                                                                                                                                                                                       | operator info                                                                                                                                 | memory  | disk |
+----------------------------------------+-------------+---------+--------------+---------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+---------+------+
| TableReader_53                         | 37343.19    | 59574   | root         |                     | time:162.1ms, loops:82, RU:0.000000, cop_task: {num: 47, max: 0s, min: 0s, avg: 0s, p95: 0s, copr_cache_hit_ratio: 0.00}                                                                                                                                                                                                                                                                             | MppVersion: 1, data:ExchangeSender_52                                                                                                         | 12.7 KB | N/A  |
| └─ExchangeSender_52                    | 37343.19    | 59574   | mpp[tiflash] |                     | tiflash_task:{proc max:160.8ms, min:154.3ms, avg: 157.6ms, p80:160.8ms, p95:160.8ms, iters:86, tasks:2, threads:16}                                                                                                                                                                                                                                                                                  | ExchangeType: PassThrough                                                                                                                     | N/A     | N/A  |
|   └─Projection_51                      | 37343.19    | 59574   | mpp[tiflash] |                     | tiflash_task:{proc max:160.8ms, min:154.3ms, avg: 157.6ms, p80:160.8ms, p95:160.8ms, iters:86, tasks:2, threads:16}                                                                                                                                                                                                                                                                                  | tpcds50.catalog_sales.cs_ship_date_sk                                                                                                         | N/A     | N/A  |
|     └─HashJoin_48                      | 37343.19    | 59574   | mpp[tiflash] |                     | tiflash_task:{proc max:160.8ms, min:154.3ms, avg: 157.6ms, p80:160.8ms, p95:160.8ms, iters:86, tasks:2, threads:16}                                                                                                                                                                                                                                                                                  | inner join, equal:[eq(tpcds50.date_dim.d_date_sk, tpcds50.catalog_sales.cs_ship_date_sk)], runtime filter:0[IN] <- tpcds50.date_dim.d_date_sk | N/A     | N/A  |
|       ├─ExchangeReceiver_29(Build)     | 1.00        | 2       | mpp[tiflash] |                     | tiflash_task:{proc max:132.3ms, min:130.8ms, avg: 131.6ms, p80:132.3ms, p95:132.3ms, iters:2, tasks:2, threads:16}                                                                                                                                                                                                                                                                                   |                                                                                                                                               | N/A     | N/A  |
|       │ └─ExchangeSender_28            | 1.00        | 1       | mpp[tiflash] |                     | tiflash_task:{proc max:131ms, min:0s, avg: 65.5ms, p80:131ms, p95:131ms, iters:1, tasks:2, threads:1}                                                                                                                                                                                                                                                                                                | ExchangeType: Broadcast, Compression: FAST                                                                                                    | N/A     | N/A  |
|       │   └─TableFullScan_26           | 1.00        | 1       | mpp[tiflash] | table:date_dim      | tiflash_task:{proc max:3.01ms, min:0s, avg: 1.51ms, p80:3.01ms, p95:3.01ms, iters:1, tasks:2, threads:1}, tiflash_scan:{dtfile:{total_scanned_packs:2, total_skipped_packs:12, total_scanned_rows:16384, total_skipped_rows:97625, total_rs_index_load_time: 0ms, total_read_time: 0ms}, total_create_snapshot_time: 0ms, total_local_region_num: 1, total_remote_region_num: 0}                     | pushed down filter:eq(tpcds50.date_dim.d_date, 2002-02-01 00:00:00.000000), keep order:false                                                  | N/A     | N/A  |
|       └─Selection_31(Probe)            | 71638034.00 | 5308995 | mpp[tiflash] |                     | tiflash_task:{proc max:39.8ms, min:24.3ms, avg: 32.1ms, p80:39.8ms, p95:39.8ms, iters:86, tasks:2, threads:16}                                                                                                                                                                                                                                                                                       | not(isnull(tpcds50.catalog_sales.cs_ship_date_sk))                                                                                            | N/A     | N/A  |
|         └─TableFullScan_30             | 71997669.00 | 5335549 | mpp[tiflash] | table:catalog_sales | tiflash_task:{proc max:36.8ms, min:23.3ms, avg: 30.1ms, p80:36.8ms, p95:36.8ms, iters:86, tasks:2, threads:16}, tiflash_scan:{dtfile:{total_scanned_packs:660, total_skipped_packs:12451, total_scanned_rows:5335549, total_skipped_rows:100905778, total_rs_index_load_time: 2ms, total_read_time: 47ms}, total_create_snapshot_time: 0ms, total_local_region_num: 194, total_remote_region_num: 0} | pushed down filter:empty, keep order:false, runtime filter:0[IN] -> tpcds50.catalog_sales.cs_ship_date_sk                                     | N/A     | N/A  |
+----------------------------------------+-------------+---------+--------------+---------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+---------+------+
9 rows in set (0.17 sec)
```

By comparing the execution information of the two queries, you can find the following improvements:

* IO reduction: by comparing the `total_scanned_rows` of the TableFullScan operator, you can see that the scan volume of `TableFullScan` is reduced by 2/3 after Runtime Filter is enabled.
* Hash join performance improvement: the execution duration of the `HashJoin` operator is reduced from 376.1 ms to 157.6 ms.

### Best practices

Runtime Filter is applicable to the scenario where a large table and a small table are joined, such as a join query of a fact table and a dimension table. When the dimension table has a small amount of hit data, it means that the filter has fewer values, so the fact table can filter out the data that does not meet the conditions more effectively. Compared with the default scenario where the entire fact table is scanned, this significantly improves the query performance.

The join operation of the `Sales` table and the `date_dim` table in TPC-DS is a typical example.

## Configure Runtime Filter

When using Runtime Filter, you can configure the mode and predicate type of Runtime Filter.

### Runtime Filter mode

The mode of Runtime Filter is the relationship between the **Filter Sender operator** and **Filter Receiver operator**. There are three modes: `OFF`, `LOCAL`, and `GLOBAL`. In v7.3.0, only `OFF` and `LOCAL` modes are supported. The Runtime Filter mode is controlled by the system variable [`tidb_runtime_filter_mode`](/system-variables.md#tidb_runtime_filter_mode-new-in-v720).

- `OFF`: Runtime Filter is disabled. After it is disabled, the query behavior is the same as in previous versions.
- `LOCAL`: Runtime Filter is enabled in the local mode. In the local mode, the **Filter Sender operator** and **Filter Receiver operator** are in the same MPP task. In other words, Runtime Filter can be applied to the scenario where the HashJoin operator and TableScan operator are in the same task. Currently, Runtime Filter only supports the local mode. To enable this mode, set it to `LOCAL`.
- `GLOBAL`: currently, the global mode is not supported. You cannot set Runtime Filter to this mode.

### Runtime Filter type

The type of Runtime Filter is the type of the predicate used by the generated Filter operator. Currently, only one type is supported: `IN`, which means that the generated predicated is similar to `k1 in (xxx)`. The Runtime Filter type is controlled by the system variable [`tidb_runtime_filter_type`](/system-variables.md#tidb_runtime_filter_type-new-in-v720).

- `IN`: the default type. It means that the generated Runtime Filter uses the `IN` type predicate.

## Limitations

- Runtime Filter is an optimization in the MPP architecture and can only be applied to queries pushed down to TiFlash.
- Join type: Left outer, Full outer, and Anti join (when the left table is the probe side) do not support Runtime Filter. Because Runtime Filter filters the data involved in the join in advance, the preceding types of join do not discard the unmatched data, so Runtime Filter cannot be used.
- Equal join expression: When the probe column in the equal join expression is a complex expression, or when the probe column type is JSON, Blob, Array, or other complex data types, Runtime Filter is not generated. The main reason is that the preceding types of columns are rarely used as the join column. Even if the Filter is generated, the filtering rate is usually low.

For the preceding limitations, if you need to confirm whether Runtime Filter is generated correctly, you can use the [`EXPLAIN` statement](/sql-statements/sql-statement-explain.md) to verify the execution plan.
