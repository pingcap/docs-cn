---
title: Coprocessor Cache
summary: Learn the features of Coprocessor Cache.
aliases: ['/docs/dev/coprocessor-cache/']
---

# Coprocessor Cache

Starting from v4.0, the TiDB instance supports caching the results of the calculation that is pushed down to TiKV (the Coprocessor Cache feature), which can accelerate the calculation process in some scenarios.

## Configuration

<CustomContent platform="tidb">

You can configure Coprocessor Cache via the `tikv-client.copr-cache` configuration items in the TiDB configuration file. For details about how to enable and configure Coprocessor Cache, see [TiDB Configuration File](/tidb-configuration-file.md#tikv-clientcopr-cache-new-in-v400).

</CustomContent>

<CustomContent platform="tidb-cloud">

The Coprocessor Cache feature is enabled by default. The maximum size of the data that can be cached is 1000 MB.

</CustomContent>

## Feature description

+ When a SQL statement is executed on a single TiDB instance for the first time, the execution result is not cached.
+ Calculation results are cached in the memory of TiDB. If the TiDB instance is restarted, the cache becomes invalid.
+ The cache is not shared among TiDB instances.
+ Only push-down calculation result is cached. Even if cache is hit, TiDB still need to perform subsequent calculation.
+ The cache is in the unit of Region. Writing data to a Region causes the Region cache to be invalid. For this reason, the Coprocessor Cache feature mainly takes effect on the data that rarely changes.
+ When push-down calculation requests are the same, the cache is hit. Usually in the following scenarios, the push-down calculation requests are the same or partially the same:
    - The SQL statements are the same. For example, the same SQL statement is executed repeatedly.

        In this scenario, all the push-down calculation requests are consistent, and all requests can use the push-down calculation cache.

    - The SQL statements contain a changing condition, and the other parts are consistent. The changing condition is the primary key of the table or the partition.

        In this scenario, some of the push-down calculation requests are the same with some previous requests, and these calculation requests can use the cached (previous) push-down calculation result.

    - The SQL statements contain multiple changing conditions and the other parts are consistent. The changing conditions exactly match a compound index column.

        In this scenario, some of the push-down calculation requests are the same with some previous requests, and these calculation requests can use the cached (previous) push-down calculation result.

+ This feature is transparent to users. Enabling or disabling this feature does not affect the calculation result and only affects the SQL execution time.

## Check the cache effect

You can check the cache effect of Coprocessor by executing `EXPLAIN ANALYZE` or viewing the Grafana monitoring panel.

### Use `EXPLAIN ANALYZE`

You can view the cache hit rate in [Operators for accessing tables](/choose-index.md#operators-for-accessing-tables) by using the [`EXPLAIN ANALYZE` statement](/sql-statements/sql-statement-explain-analyze.md). See the following example:

```sql
EXPLAIN ANALYZE SELECT * FROM t USE INDEX(a);
+-------------------------------+-----------+---------+-----------+------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+--------------------------------+-----------------------+------+
| id                            | estRows   | actRows | task      | access object          | execution info                                                                                                                                                                                                                                           | operator info                  | memory                | disk |
+-------------------------------+-----------+---------+-----------+------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+--------------------------------+-----------------------+------+
| IndexLookUp_6                 | 262400.00 | 262400  | root      |                        | time:620.513742ms, loops:258, cop_task: {num: 4, max: 5.530817ms, min: 1.51829ms, avg: 2.70883ms, p95: 5.530817ms, max_proc_keys: 2480, p95_proc_keys: 2480, tot_proc: 1ms, tot_wait: 1ms, rpc_num: 4, rpc_time: 10.816328ms, copr_cache_hit_rate: 0.75} |                                | 6.685169219970703 MB  | N/A  |
| ├─IndexFullScan_4(Build)      | 262400.00 | 262400  | cop[tikv] | table:t, index:a(a, c) | proc max:93ms, min:1ms, p80:93ms, p95:93ms, iters:275, tasks:4                                                                                                                                                                                           | keep order:false, stats:pseudo | 1.7549400329589844 MB | N/A  |
| └─TableRowIDScan_5(Probe)     | 262400.00 | 0       | cop[tikv] | table:t                | time:0ns, loops:0                                                                                                                                                                                                                                        | keep order:false, stats:pseudo | N/A                   | N/A  |
+-------------------------------+-----------+---------+-----------+------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+--------------------------------+-----------------------+------+
3 rows in set (0.62 sec)
```

The column `execution info` of the execution result gives the `copr_cache_hit_ratio` information, which indicates the hit rate of the Coprocessor Cache. The `0.75` in the above example means that the hit rate is about 75%.

### View the Grafana monitoring panel

In Grafana, you can see the **copr-cache** panel in the `distsql` subsystem under the `tidb` namespace. This panel monitors the number of hits, misses, and cache discards of the Coprocessor Cache in the entire cluster.
