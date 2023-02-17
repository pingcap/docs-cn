---
title: TiDB 6.4.0 Release Notes
---

# TiDB 6.4.0 Release Notes

Release date: November 17, 2022

TiDB version: 6.4.0-DMR

Quick access: [Quick start](https://docs.pingcap.com/tidb/v6.4/quick-start-with-tidb) | [Installation packages](https://www.pingcap.com/download/?version=v6.4.0#version-list)

In v6.4.0-DMR, the key new features and improvements are as follows:

- Support restoring a cluster to a specific point in time by using [`FLASHBACK CLUSTER TO TIMESTAMP`](/sql-statements/sql-statement-flashback-to-timestamp.md) (experimental).
- Support [tracking the global memory usage](/configure-memory-usage.md) of TiDB instances (experimental).
- Be compatible with [the Linear Hash partitioning syntax](/partitioned-table.md#how-tidb-handles-linear-hash-partitions).
- Support a high-performance and globally monotonic [`AUTO_INCREMENT`](/auto-increment.md#mysql-compatibility-mode) (experimental).
- Support range selection of array data in [the JSON type](/data-type-json.md).
- Accelerate fault recovery in extreme situations such as disk failures and stuck I/O.
- Add the [dynamic planning algorithm](/join-reorder.md#example-the-dynamic-programming-algorithm-of-join-reorder) to determine table join order.
- Introduce [a new optimizer hint `NO_DECORRELATE`](/optimizer-hints.md#no_decorrelate) to control whether to perform decorrelation for correlated subqueries.
- The [cluster diagnostics](/dashboard/dashboard-diagnostics-access.md) feature becomes GA.
- TiFlash supports the SM4 algorithm for [encryption at rest](/encryption-at-rest.md#tiflash).
- Support using a SQL statement to [compact TiFlash replicas of specified partitions in a table immediately](/sql-statements/sql-statement-alter-table-compact.md#compact-tiflash-replicas-of-specified-partitions-in-a-table).
- Support [backing up a TiDB cluster using EBS volume snapshots](https://docs.pingcap.com/tidb-in-kubernetes/v1.4/backup-to-aws-s3-by-snapshot).
- DM supports [writing upstream data source information to the extended columns of the downstream merged table](/dm/dm-table-routing.md#extract-table-schema-and-source-information-and-write-into-the-merged-table).

## New features

### SQL

* Support using a SQL statement to compact TiFlash replicas of specified partitions in a table immediately [#5315](https://github.com/pingcap/tiflash/issues/5315) @[hehechen](https://github.com/hehechen)

    Since v6.2.0, TiDB has supported the feature of [compacting physical data immediately](/sql-statements/sql-statement-alter-table-compact.md#alter-table--compact) on a full-table replica of TiFlash. You can choose the right time to manually execute SQL statements to immediately compact the physical data in TiFlash, which helps to reduce storage space and improve query performance. In v6.4.0, we refine the granularity of TiFlash replica data to be compacted and support compacting TiFlash replicas of specified partitions in a table immediately.

    By executing the SQL statement `ALTER TABLE table_name COMPACT [PARTITION PartitionNameList] [engine_type REPLICA]`, you can immediately compact TiFlash replicas of specified partitions in a table.

    For more information, see [User document](/sql-statements/sql-statement-alter-table-compact.md#compact-tiflash-replicas-of-specified-partitions-in-a-table).

* Support restoring a cluster to a specific point in time by using `FLASHBACK CLUSTER TO TIMESTAMP` (experimental) [#37197](https://github.com/pingcap/tidb/issues/37197) [#13303](https://github.com/tikv/tikv/issues/13303) @[Defined2014](https://github.com/Defined2014) @[bb7133](https://github.com/bb7133) @[JmPotato](https://github.com/JmPotato) @[Connor1996](https://github.com/Connor1996) @[HuSharp](https://github.com/HuSharp) @[CalvinNeo](https://github.com/CalvinNeo)

    You can use the `FLASHBACK CLUSTER TO TIMESTAMP` syntax to restore a cluster to a specific point in time quickly within the Garbage Collection (GC) lifetime. This feature helps you to easily and quickly undo DML misoperations. For example, you can use this syntax to restore the original cluster in minutes after mistakenly executing `DELETE` without a `WHERE` clause. This feature does not rely on database backups and supports rolling back data at different time points to determine the exact time when data changes. Note that `FLASHBACK CLUSTER TO TIMESTAMP` cannot replace database backups.

    Before executing `FLASHBACK CLUSTER TO TIMESTAMP`, you need to pause PITR and replication tasks running on such tools as TiCDC and restart them after the `FLASHBACK` is completed. Otherwise, replication tasks might fail.

    For more information, see [User document](/sql-statements/sql-statement-flashback-to-timestamp.md).

* Support restoring a deleted database by using `FLASHBACK DATABASE` [#20463](https://github.com/pingcap/tidb/issues/20463) @[erwadba](https://github.com/erwadba)

    By using `FLASHBACK DATABASE`, you can restore a database and its data deleted by `DROP` within the garbage collection (GC) life time. This feature does not depend on any external tools. You can quickly restore data and metadata using SQL statements.

    For more information, see [User document](/sql-statements/sql-statement-flashback-database.md).

### Security

* TiFlash supports the SM4 algorithm for encryption at rest [#5953](https://github.com/pingcap/tiflash/issues/5953) @[lidezhu](https://github.com/lidezhu)

    Add the SM4 algorithm for TiFlash encryption at rest. When you configure encryption at rest, you can enable the SM4 encryption capacity by setting the value of the `data-encryption-method` configuration to `sm4-ctr` in the `tiflash-learner.toml` configuration file.

    For more information, see [User document](/encryption-at-rest.md#tiflash).

### Observability

* Cluster diagnostics becomes GA [#1438](https://github.com/pingcap/tidb-dashboard/issues/1438) @[Hawkson-jee](https://github.com/Hawkson-jee)

    The [cluster diagnostics](/dashboard/dashboard-diagnostics-access.md) feature in TiDB Dashboard diagnoses the problems that might exist in a cluster within a specified time range, and summarizes the diagnostic results and the cluster-related load monitoring information into [a diagnostic report](/dashboard/dashboard-diagnostics-report.md). This diagnostic report is in the form of a web page. You can browse the page offline and circulate this page link after saving the page from a browser.

    With the diagnostic reports, you can quickly understand the basic health information of the cluster, including the load, component status, time consumption, and configurations. If the cluster has some common problems, you can locate the causes in the result of the built-in automatic diagnosis in the [diagnostic information](/dashboard/dashboard-diagnostics-report.md#diagnostic-information) section.

### Performance

* Introduce the concurrency adaptive mechanism for coprocessor tasks [#37724](https://github.com/pingcap/tidb/issues/37724) @[you06](https://github.com/you06)

    As the number of coprocessor tasks increases, based on TiKV's processing speed, TiDB automatically increases concurrency (adjust the value of [`tidb_distsql_scan_concurrency`](/system-variables.md#tidb_distsql_scan_concurrency)) to reduce the coprocessor task queue and thus reduce latency.

* Add the dynamic planning algorithm to determine table join order [#37825](https://github.com/pingcap/tidb/issues/37825) @[winoros](https://github.com/winoros)

    In earlier versions, TiDB uses the greedy algorithm to determine the join order of tables. In v6.4.0, the TiDB optimizer introduces the [dynamic planning algorithm](/join-reorder.md#example-the-dynamic-programming-algorithm-of-join-reorder). The dynamic planning algorithm can enumerate more possible join orders than the greedy algorithm, so it increases the possibility to find a better execution plan and improves SQL execution efficiency in some scenarios.

    Because the dynamic programming algorithm consumes more time, the selection of the TiDB Join Reorder algorithms is controlled by the [`tidb_opt_join_reorder_threshold`](/system-variables.md#tidb_opt_join_reorder_threshold) variable. If the number of nodes participating in Join Reorder is greater than this threshold, TiDB uses the greedy algorithm. Otherwise, TiDB uses the dynamic programming algorithm.

    For more information, see [User document](/join-reorder.md).

* The prefix index supports filtering null values. [#21145](https://github.com/pingcap/tidb/issues/21145) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes)

    This feature is an optimization for the prefix index. When a column in a table has a prefix index, the `IS NULL` or `IS NOT NULL` condition of the column in the SQL statement can be directly filtered by the prefix, which avoids table lookup in this case and improves the performance of the SQL execution.

    For more information, see [User document](/system-variables.md#tidb_opt_prefix_index_single_scan-new-in-v640).

* Enhance the TiDB chunk reuse mechanism [#38606](https://github.com/pingcap/tidb/issues/38606) @[keeplearning20221](https://github.com/keeplearning20221)

    In earlier versions, TiDB only reuses chunks in the `writechunk` function. TiDB v6.4.0 extends the chunk reuse mechanism to operators in Executor. By reusing chunks, TiDB does not need to frequently request memory release and SQL queries are executed more efficiently in some scenarios. You can use the system variable [`tidb_enable_reuse_chunk`](/system-variables.md#tidb_enable_reuse_chunk-new-in-v640) to control whether to reuse chunk objects, which is enabled by default.

    For more information, see [User document](/system-variables.md#tidb_enable_reuse_chunk-new-in-v640).

* Introduce a new optimizer hint `NO_DECORRELATE` to control whether to perform decorrelation for correlated subqueries [#37789](https://github.com/pingcap/tidb/issues/37789) @[time-and-fate](https://github.com/time-and-fate)

    By default, TiDB always tries to rewrite correlated subqueries to perform decorrelation, which usually improves execution efficiency. However, in some scenarios, decorrelation reduces the execution efficiency. In v6.4.0, TiDB introduces the optimizer hint `NO_DECORRELATE` to tell the optimizer not to perform decorrelation for specified query blocks to improve query performance in some scenarios.

    For more information, see [User document](/optimizer-hints.md#no_decorrelate).

* Improve the performance of statistics collection on partitioned tables [#37977](https://github.com/pingcap/tidb/issues/37977) @[Yisaer](https://github.com/Yisaer)

    In v6.4.0, TiDB optimizes the strategy of collecting statistics on partitioned tables. You can use the system variable [`tidb_auto_analyze_partition_batch_size`](/system-variables.md#tidb_auto_analyze_partition_batch_size-new-in-v640) to set the concurrency of collecting statistics on partitioned tables in parallel to speed up the collection and shorten the analysis time.

### Stability

* Accelerate fault recovery in extreme situations such as disk failures and stuck I/O [#13648](https://github.com/tikv/tikv/issues/13648) @[LykxSassinator](https://github.com/LykxSassinator)

    For enterprise users, database availability is one of the most important metrics. While in complex hardware environments, how to quickly detect and recover from failures has always been one of the challenges of database availability. In v6.4.0, TiDB fully optimizes the state detection mechanism of TiKV nodes. Even in extreme situations such as disk failures and stuck I/O, TiDB can still report node state quickly and use the active wake-up mechanism to launch Leader election in advance, which accelerates cluster self-healing. Through this optimization, TiDB can shorten the cluster recovery time by about 50% in the case of disk failures.

* Global control on TiDB memory usage [#37816](https://github.com/pingcap/tidb/issues/37816) @[wshwsh12](https://github.com/wshwsh12)

    In v6.4.0, TiDB introduces global control of memory usage as an experimental feature that tracks the global memory usage of TiDB instances. You can use the system variable [`tidb_server_memory_limit`](/system-variables.md#tidb_server_memory_limit-new-in-v640) to set the upper limit for the global memory usage. When the memory usage reaches the threshold, TiDB tries to reclaim and release more free memory. When the memory usage exceeds the threshold, TiDB identifies and cancels the SQL operation that has the highest memory usage to avoid system issues caused by excessive memory usage.

    When the memory consumption of TiDB instances has potential risks, TiDB will collect diagnostic information in advance and write it to the specified directory to facilitate the issue diagnosis. At the same time, TiDB provides system table views [`INFORMATION_SCHEMA.MEMORY_USAGE`](/information-schema/information-schema-memory-usage.md) and [`INFORMATION_SCHEMA.MEMORY_USAGE_OPS_HISTORY`](/information-schema/information-schema-memory-usage-ops-history.md) that show the memory usage and operation history to help you better understand the memory usage.

    Global memory control is a milestone in TiDB memory management. It introduces a global view for instances and adopts systematic management for memory, which can greatly enhance database stability and service availability in more key scenarios.

    For more information, see [User document](/configure-memory-usage.md).

* Control the memory usage of the range-building optimizer [#37176](https://github.com/pingcap/tidb/issues/37176) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes)

    In v6.4.0, the system variable [`tidb_opt_range_max_size`](/system-variables.md#tidb_opt_range_max_size-new-in-v640) is introduced to limit the maximum memory usage of the optimizer that builds ranges. When the memory usage exceeds the limit, the optimizer will build more coarse-grained ranges instead of more exact ranges to reduce memory consumption. If a SQL statement has many `IN` conditions, this optimization can significantly reduce the memory usage of compiling and ensure system stability.

    For more information, see [User document](/system-variables.md#tidb_opt_range_max_size-new-in-v640).

* Support synchronously loading statistics (GA) [#37434](https://github.com/pingcap/tidb/issues/37434) @[chrysan](https://github.com/chrysan)

    TiDB v6.4.0 enables the synchronously loading statistics feature by default. This feature allows TiDB to synchronously load large-sized statistics (such as histograms, TopN, and Count-Min Sketch statistics) into memory when you execute SQL statements, which improves the completeness of statistics for SQL optimization.

    For more information, see [User document](/system-variables.md#tidb_stats_load_sync_wait-new-in-v540).

### Ease of use

* TiKV API V2 becomes generally available (GA) [#11745](https://github.com/tikv/tikv/issues/11745) @[pingyu](https://github.com/pingyu)

    Before v6.1.0, TiKV only provides basic Key Value read and write capability because it only stores the raw data passed in by the client. In addition, due to different coding methods and unscoped data ranges, TiDB, Transactional KV, and RawKV cannot be used at the same time in the same TiKV cluster; instead, multiple clusters are needed in this case, thus increasing machine and deployment costs.

    TiKV API V2 provides a new RawKV storage format and access interface, which delivers the following benefits:

    - Store data in MVCC with the change timestamp of the data recorded, based on which Change Data Capture (CDC) is implemented. This feature is experimental and is detailed in [TiKV-CDC](https://github.com/tikv/migration/blob/main/cdc/README.md).
    - Data is scoped according to different usage and API V2 supports co-existence of TiDB, Transactional KV, and RawKV applications in a single cluster.
    - Reserve the Key Space field to support features such as multi-tenancy.

  To enable TiKV API V2, set `api-version = 2` in the `[storage]` section of the TiKV configuration file.

  For more information, see [User document](/tikv-configuration-file.md#api-version-new-in-v610).

* Improve the accuracy of TiFlash data replication progress [#4902](https://github.com/pingcap/tiflash/issues/4902) @[hehechen](https://github.com/hehechen)

    In TiDB, the `PROGRESS` field of the `INFORMATION_SCHEMA.TIFLASH_REPLICA` table is used to indicate the progress of data replication from the corresponding tables in TiKV to the TiFlash replicas. In earlier TiDB versions, the `PROCESS` field only provides the progress of data replication during the creation of the TiFlash replicas. After a TiFlash replica is created, if new data is imported to a corresponding table in TiKV, this field will not be updated to show the replication progress from TiKV to TiFlash for the new data.

    In v6.4.0, TiDB improves the update mechanism of data replication progress for TiFlash replicas. After a TiFlash replica is created, if new data is imported to a corresponding table in TiKV, the `PROGRESS` value in the [`INFORMATION_SCHEMA.TIFLASH_REPLICA`](/information-schema/information-schema-tiflash-replica.md) table will be updated to show the actual replication progress from TiKV to TiFlash for the new data. With this improvement, you can easily view the actual progress of TiFlash data replication.

    For more information, see [User document](/information-schema/information-schema-tiflash-replica.md).

### MySQL compatibility

* Be compatible with the Linear Hash partitioning syntax [#38450](https://github.com/pingcap/tidb/issues/38450) @[mjonss](https://github.com/mjonss)

    In the earlier version, TiDB has supported the Hash, Range, and List partitioning. Starting from v6.4.0, TiDB can also be compatible with the syntaxt of [MySQL Linear Hash partitioning](https://dev.mysql.com/doc/refman/5.7/en/partitioning-linear-hash.html).

    In TiDB, you can execute the existing DDL statements of your MySQL Linear Hash partitions directly, and TiDB will create the corresponding Hash partition tables (note that there is no Linear Hash partition inside TiDB). You can also execute the existing DML statements of your MySQL Linear Hash partitions directly, and TiDB will return the query result of the corresponding TiDB Hash partitions normally. This feature ensures the TiDB syntax compatibility with MySQL Linear Hash partitions and facilitates seamless migration from MySQL-based applications to TiDB.

    If the number of partitions is a power of 2, the rows in a TiDB Hash partitioned table are distributed the same as that in the MySQL Linear Hash partitioned table. Otherwise, the distribution of these rows in TiDB is different from MySQL.

    For more information, see [User document](/partitioned-table.md#how-tidb-handles-linear-hash-partitions).

* Support a high-performance and globally monotonic `AUTO_INCREMENT` (experimental) [#38442](https://github.com/pingcap/tidb/issues/38442) @[tiancaiamao](https://github.com/tiancaiamao)

    TiDB v6.4.0 introduces the `AUTO_INCREMENT` MySQL compatibility mode. This mode introduces a centralized auto-increment ID allocating service that ensures IDs monotonically increase on all TiDB instances. This feature makes it easier to sort query results by auto-increment IDs. To use the MySQL compatibility mode, you need to set `AUTO_ID_CACHE` to `1` when creating a table. The following is an example:

    ```sql
    CREATE TABLE t (a INT AUTO_INCREMENT PRIMARY KEY) AUTO_ID_CACHE = 1;
    ```

    For more information, see [User document](/auto-increment.md#mysql-compatibility-mode).

* Support range selection of array data in the JSON type [#13644](https://github.com/tikv/tikv/issues/13644) @[YangKeao](https://github.com/YangKeao)

    Starting from v6.4.0, you can use the MySQL-compatible [range selection syntax](https://dev.mysql.com/doc/refman/8.0/en/json.html#json-paths) in TiDB.

    - With the keyword `to`, you can specify the start and end positions of array elements and select elements of a continuous range in an array. With `0`, you can specify the position of the first element in an array. For example, using `$[0 to 2]`, you can select the first three elements of an array.

    - With the keyword `last`, you can specify the position of the last element in an array, which allows you to set the position from right to left. For example, using `$[last-2 to last]`, you can select the last three elements of an array.

   This feature simplifies the process of writing SQL statements, further improves the JSON type compatibility, and reduces the difficulty of migrating MySQL applications to TiDB.

* Support adding additional descriptions for database users [#38172](https://github.com/pingcap/tidb/issues/38172) @[CbcWestwolf](https://github.com/CbcWestwolf)

    In TiDB v6.4, you can use the [`CREATE USER`](/sql-statements/sql-statement-create-user.md) or [`ALTER USER`](/sql-statements/sql-statement-alter-user.md) to add additional descriptions for database users. TiDB provides two description formats. You can add a text comment using `COMMENT` and add a set of structured attributes in JSON format using `ATTRIBUTE`.

    In addition, TiDB v6.4.0 adds the [`USER_ATTRIBUTES`](/information-schema/information-schema-user-attributes.md) table, where you can view the information of user comments and user attributes.

    ```sql
    CREATE USER 'newuser1'@'%' COMMENT 'This user is created only for test';
    CREATE USER 'newuser2'@'%' ATTRIBUTE '{"email": "user@pingcap.com"}';
    SELECT * FROM INFORMATION_SCHEMA.USER_ATTRIBUTES;
    ```

    ```sql
    +-----------+------+---------------------------------------------------+
    | USER      | HOST | ATTRIBUTE                                         |
    +-----------+------+---------------------------------------------------+
    | newuser1  | %    | {"comment": "This user is created only for test"} |
    | newuser1  | %    | {"email": "user@pingcap.com"}                     |
    +-----------+------+---------------------------------------------------+
    2 rows in set (0.00 sec)
    ```

    This feature improves TiDB compatibility with MySQL syntax and makes it easier to integrate TiDB into tools or platforms in the MySQL ecosystem.

### Backup and restore

* Support backing up a TiDB cluster using EBS volume snapshots [#33849](https://github.com/pingcap/tidb/issues/33849) @[fengou1](https://github.com/fengou1)

    If your TiDB cluster is deployed on EKS and uses AWS EBS volumes, and you have the following requirements when backing up TiDB cluster data, you can use TiDB Operator to back up the data by volume snapshots and metadata to AWS S3:

    - Minimize the impact of backup, for example, to keep the impact on QPS and transaction latency less than 5%, and to occupy no cluster CPU and memory.
    - Back up and restore data in a short time. For example, finish backup within 1 hour and restore data in 2 hours.

  For more information, see [User document](https://docs.pingcap.com/tidb-in-kubernetes/v1.4/backup-to-aws-s3-by-snapshot).

### Data migration

* DM supports writing upstream data source information to the extended columns of the downstream merged table [#37797](https://github.com/pingcap/tidb/issues/37797) @[lichunzhu](https://github.com/lichunzhu)

    When merging sharded schemas and tables from upstream to TiDB, you can manually add several fields (extended columns) in the target table and specify their values when configuring the DM task. For example, if you specify the names of the upstream sharded schema and table for the extended columns, the data written to the downstream by DM will include the schema name and table name. When the downstream data looks unusual, you can use this feature to quickly locate the data source information in the target table, such as the schema name and table name.

    For more information, see [Extract table, schema, and source information and write into the merged table](/dm/dm-table-routing.md#extract-table-schema-and-source-information-and-write-into-the-merged-table).

* DM optimizes the pre-check mechanism by changing some mandatory check items to optional ones [#7333](https://github.com/pingcap/tiflow/issues/7333) @[lichunzhu](https://github.com/lichunzhu)

    To run a data migration task smoothly, DM triggers [a precheck](/dm/dm-precheck.md) automatically at the start of the task and returns the check results. DM starts the migration only after the precheck is passed.

    In v6.4.0, DM changes the following three check items from mandatory to optional, which improves the pass rate of the pre-check:

    - Check whether the upstream tables use character sets that are incompatible with TiDB.
    - Check whether the upstream tables have primary key constraints or unique key constraints
    - Check whether the database ID `server_id` for the upstream database has been specified in the primary-secondary configuration.

* DM supports configuring binlog position and GTID as optional parameters for incremental migration tasks [#7393](https://github.com/pingcap/tiflow/issues/7393) @[GMHDBJD](https://github.com/GMHDBJD)

    Since v6.4.0, you can perform incremental migration directly without specifying the binlog position or GTID. DM automatically obtains the binlog files generated after the task starts from upstream and migrates these incremental data to the downstream. This relieves users from laborious understanding and complicated configuration.

    For more information, see [DM Advanced Task Configuration File](/dm/task-configuration-file-full.md).

* DM adds more status indicators for migration tasks [#7343](https://github.com/pingcap/tiflow/issues/7343) @[okJiang](https://github.com/okJiang)

    In v6.4.0, DM adds more performance and progress indicators for migration tasks, which helps you understand the migration performance and progress more intuitively and provides you with a reference for troubleshooting.

    * Add status indicators (in bytes/s) showing data importing and exporting performance.
    * Rename the performance indicator for writing data to the downstream database from TPS to RPS (in rows/s).
    * Add progress indicators showing the data export progress of DM full migration tasks.

    For more information about these indicators, see [Query Task Status in TiDB Data Migration](/dm/dm-query-status.md).

### TiDB data share subscription

- TiCDC supports replicating data to Kafka of the `3.2.0` version [#7191](https://github.com/pingcap/tiflow/issues/7191) @[3AceShowHand](https://github.com/3AceShowHand)

    From v6.4.0, TiCDC supports [replicating data to Kafka](/replicate-data-to-kafka.md) of the `3.2.0` version and earlier.

## Compatibility changes

### System variables

| Variable name | Change type | Description |
|--------|------------------------------|------|
| [`tidb_constraint_check_in_place_pessimistic`](/system-variables.md#tidb_constraint_check_in_place_pessimistic-new-in-v630) | Modified | Removes the GLOBAL scope and allows you to modify the default value using the [`pessimistic-txn.constraint-check-in-place-pessimistic`](/tidb-configuration-file.md#constraint-check-in-place-pessimistic-new-in-v640) configuration item. This variable controls when TiDB checks the unique constraints in pessimistic transactions. |
| [`tidb_ddl_flashback_concurrency`](/system-variables.md#tidb_ddl_flashback_concurrency-new-in-v630) | Modified | Takes effect starting from v6.4.0 and controls the concurrency of [`FLASHBACK CLUSTER TO TIMESTAMP`](/sql-statements/sql-statement-flashback-to-timestamp.md). The default value is `64`. |
| [`tidb_enable_clustered_index`](/system-variables.md#tidb_enable_clustered_index-new-in-v50) | Modified | Changes the default value from `INT_ONLY` to `ON`, meaning that primary keys are created as clustered indexes by default.|
| [`tidb_enable_paging`](/system-variables.md#tidb_enable_paging-new-in-v540) | Modified | Changes the default value from `OFF` to `ON`, meaning that the method of paging to send coprocessor requests is used by default. |
| [`tidb_enable_prepared_plan_cache`](/system-variables.md#tidb_enable_prepared_plan_cache-new-in-v610) | Modified | Adds the SESSION scope. This variable controls whether to enable [Prepared Plan Cache](/sql-prepared-plan-cache.md). |
| [`tidb_memory_usage_alarm_ratio`](/system-variables.md#tidb_memory_usage_alarm_ratio) | Modified | Changes the default value from `0.8` to `0.7`. This variable controls the memory usage ratio that triggers the tidb-server memory alarm. |
| [`tidb_opt_agg_push_down`](/system-variables.md#tidb_opt_agg_push_down) | Modified | Adds the GLOBAL scope. This variable controls whether the optimizer executes the optimization operation of pushing down the aggregate function to the position before Join, Projection, and UnionAll. |
| [`tidb_prepared_plan_cache_size`](/system-variables.md#tidb_prepared_plan_cache_size-new-in-v610) | Modified | Adds the SESSION scope. This variable controls the maximum number of plans that can be cached in a session. |
| [`tidb_stats_load_sync_wait`](/system-variables.md#tidb_stats_load_sync_wait-new-in-v540) | Modified | Changes the default value from `0` to `100`, meaning that the SQL execution can wait for at most 100 milliseconds by default to synchronously load complete column statistics. |
| [`tidb_stats_load_pseudo_timeout`](/system-variables.md#tidb_stats_load_pseudo_timeout-new-in-v540) | Modified | Changes the default value from `OFF` to `ON`, meaning that the SQL optimization gets back to using pseudo statistics after reaching the timeout of synchronously loading complete column statistics. |
| [`last_sql_use_alloc`](/system-variables.md#last_sql_use_alloc-new-in-v640) | Newly added | Shows whether the previous statement uses a cached chunk object (chunk allocation). This variable is read-only and the default value is `OFF`. |
| [`tidb_auto_analyze_partition_batch_size`](/system-variables.md#tidb_auto_analyze_partition_batch_size-new-in-v640) | Newly added | Specifies the number of partitions that TiDB can [automatically analyzes](/statistics.md#automatic-update) at a time when analyzing a partitioned table (which means automatically collecting statistics on a partitioned table). The default value is `1`.|
| [`tidb_enable_external_ts_read`](/system-variables.md#tidb_enable_external_ts_read-new-in-v640) | Newly added | Controls whether TiDB reads data with the timestamp specified by [`tidb_external_ts`](/system-variables.md#tidb_external_ts-new-in-v640). The default value is `OFF`. |
| [`tidb_enable_gogc_tuner`](/system-variables.md#tidb_enable_gogc_tuner-new-in-v640) | Newly added | Controls whether to enable GOGC Tuner. The default value is `ON`. |
| [`tidb_enable_reuse_chunk`](/system-variables.md#tidb_enable_reuse_chunk-new-in-v640) | Newly added | Controls whether TiDB enables chunk objects cache. The default value is `ON`, meaning that TiDB prefers to use the cached chunk object and only requests from the system if the requested object is not in the cache. If the value is `OFF`, TiDB requests chunk objects from the system directly. |
| [`tidb_enable_prepared_plan_cache_memory_monitor`](/system-variables.md#tidb_enable_prepared_plan_cache_memory_monitor-new-in-v640) | Newly added | Controls whether to count the memory consumed by the execution plans cached in the Prepared Plan Cache. The default value is `ON`.|
| [`tidb_external_ts`](/system-variables.md#tidb_external_ts-new-in-v640) | Newly added | The default value is `0`. If [`tidb_enable_external_ts_read`](/system-variables.md#tidb_enable_external_ts_read-new-in-v640) is set to `ON`, TiDB reads data with the timestamp specified by this variable.|
| [`tidb_gogc_tuner_threshold`](/system-variables.md#tidb_gogc_tuner_threshold-new-in-v640) | Newly added | Specifies the maximum memory threshold for tuning GOGC. When the memory exceeds this threshold, GOGC Tuner stops working. The default value is `0.6`. |
| [`tidb_memory_usage_alarm_keep_record_num`](/system-variables.md#tidb_memory_usage_alarm_keep_record_num-new-in-v640) | Newly added | When the tidb-server memory usage exceeds the memory alarm threshold and triggers an alarm, TiDB only retains the status files generated during the recent 5 alarms by default. You can adjust this number with this variable. |
| [`tidb_opt_prefix_index_single_scan`](/system-variables.md#tidb_opt_prefix_index_single_scan-new-in-v640) | Newly added | Controls whether the TiDB optimizer pushes down some filter conditions to the prefix index to avoid unnecessary table lookup and to improve query performance. The default value is `ON`. |
| [`tidb_opt_range_max_size`](/system-variables.md#tidb_opt_range_max_size-new-in-v640) | Newly added | Specifies the upper limit of memory usage for the optimizer to construct a scan range. The default value is `67108864` (64 MiB). |
| [`tidb_server_memory_limit`](/system-variables.md#tidb_server_memory_limit-new-in-v640) | Newly added | Controls the upper limit of memory usage for the optimizer to build scan ranges (experimental). The default value is `0`, meaning that there is no memory limit. |
| [`tidb_server_memory_limit_gc_trigger`](/system-variables.md#tidb_server_memory_limit_gc_trigger-new-in-v640) | Newly added | Controls the threshold at which TiDB tries to trigger GC (experimental). The default value is `70%`. |
| [`tidb_server_memory_limit_sess_min_size`](/system-variables.md#tidb_server_memory_limit_sess_min_size-new-in-v640) | Newly added | After you enable the memory limit, TiDB will terminate the SQL statement with the highest memory usage on the current instance. This variable specifies the minimum memory usage of the SQL statement to be terminated. The default value is `134217728` (128 MiB).|

### Configuration file parameters

| Configuration file | Configuration parameter | Change type | Description |
| -------- | -------- | -------- | -------- |
| TiDB | `tidb_memory_usage_alarm_ratio` | Deleted | This configuration item is no longer effective. |
| TiDB | `memory-usage-alarm-ratio` | Deleted | Replaced by the system variable [`tidb_memory_usage_alarm_ratio`](/system-variables.md#tidb_memory_usage_alarm_ratio). If this configuration item has been configured in a TiDB version earlier than v6.4.0, it will not take effect after the upgrade. |
| TiDB | [`pessimistic-txn.constraint-check-in-place-pessimistic`](/tidb-configuration-file.md#constraint-check-in-place-pessimistic-new-in-v640) | Newly added | Controls the default value of the system variable [`tidb_constraint_check_in_place_pessimistic`](/system-variables.md#tidb_constraint_check_in_place_pessimistic-new-in-v630). The default value is `true`. |
| TiDB | [`tidb-max-reuse-chunk`](/tidb-configuration-file.md#tidb-max-reuse-chunk-new-in-v640) | Newly added | Controls the maximum cached chunk objects of chunk allocation. The default value is `64`.|
| TiDB | [`tidb-max-reuse-column`](/tidb-configuration-file.md#tidb-max-reuse-column-new-in-v640) | Newly added | Controls the maximum cached column objects of chunk allocation. The default value is `256`. |
| TiKV | [`cdc.raw-min-ts-outlier-threshold`](https://docs.pingcap.com/tidb/v6.2/tikv-configuration-file#raw-min-ts-outlier-threshold-new-in-v620) | Deprecated | This configuration item is no longer effective. |
| TiKV | [`causal-ts.alloc-ahead-buffer`](/tikv-configuration-file.md#alloc-ahead-buffer-new-in-v640) | Newly added | The pre-allocated TSO cache size (in duration). The default value is `3s`. |
| TiKV | [`causal-ts.renew-batch-max-size`](/tikv-configuration-file.md#renew-batch-max-size-new-in-v640)| Newly added | Controls the maximum number of TSOs in a timestamp request. The default value is `8192`. |
| TiKV | [`raftstore.apply-yield-write-size`](/tikv-configuration-file.md#apply-yield-write-size-new-in-v640) | Newly added | Controls the maximum number of bytes that the Apply thread can write for one FSM (Finite-state Machine) in one round of poll. The default value is `32KiB`. This is a soft limit. |
| PD | [`tso-update-physical-interval`](/pd-configuration-file.md#tso-update-physical-interval) | Newly added | Takes effect starting from v6.4.0 and controls the interval at which PD updates the physical time of TSO. The default value is `50ms`. |
| TiFlash | [`data-encryption-method`](/tiflash/tiflash-configuration.md#configure-the-tiflash-learnertoml-file) | Modified | Introduces a new value option `sm4-ctr`. When this configuration item is set to `sm4-ctr`, data is encrypted using SM4 before being stored. |
| DM | [`routes.route-rule-1.extract-table`](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced) | Newly added | Optional. Used in the sharding scenario for extracting the source information of sharded tables. The extracted information will be written to the merged table in the downstream to identify the data source. If this parameter is configured, you need to manually create a merged table in the downstream in advance. |
| DM | [`routes.route-rule-1.extract-schema`](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced) | Newly added | Optional. Used in the sharding scenario for extracting the source information of sharded schemas. The extracted information will be written to the merged table in the downstream to identify the data source. If this parameter is configured, you need to manually create a merged table in the downstream in advance. |
| DM | [`routes.route-rule-1.extract-source`](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced) | Newly added | Optional. Used in the sharding scenario for extracting the source instance information. The extracted information will be written to the merged table in the downstream to identify the data source. If this parameter is configured, you need to manually create a merged table in the downstream in advance. |
| TiCDC | [`transaction-atomicity`](/ticdc/ticdc-sink-to-mysql.md#configure-sink-uri-for-mysql-or-tidb) | Modified | Changes the default value from `table` to `none`. This change helps reduce replication latency and OOM risks. In addition, TiCDC now only splits a few transactions (the size of a single transaction exceeds 1024 rows), instead of all transactions. |

### Others

- Starting from v6.4.0, the `mysql.user` table adds two new columns: `User_attributes` and `Token_issuer`. If you [restore system tables in the `mysql` schema](/br/br-snapshot-guide.md#restore-tables-in-the-mysql-schema) from backup data of earlier TiDB versions to TiDB v6.4.0, BR will report the `column count mismatch` error for the `mysql.user` table. If you do not restore system tables in the `mysql` schema, this error will not be reported.
- For files whose names match the [format of Dumpling exported files](/dumpling-overview.md#format-of-exported-files) but end with uncompressed formats (such as `test-schema-create.sql.origin` and `test.table-schema.sql.origin`), the way how TiDB Lightning handles them is changed. Before v6.4.0, if the files to be imported include such files, TiDB Lightning skips importing such files. Starting from v6.4.0, TiDB Lightning assumes that such files use unsupported compression formats, so the import task will fail.
- Starting with v6.4.0, only the changefeed with the `SYSTEM_VARIABLES_ADMIN` or `SUPER` privilege can use the TiCDC Syncpoint feature.

## Improvements

+ TiDB

    - Allow modifying the noop variable `lc_messages` [#38231](https://github.com/pingcap/tidb/issues/38231) @[djshow832](https://github.com/djshow832)
    - Support the `AUTO_RANDOM` column as the first column of the clustered composite index [#38572](https://github.com/pingcap/tidb/issues/38572) @[tangenta](https://github.com/tangenta)
    - Use pessimistic transactions in internal transaction retry to avoid retry failure and reduce time consumption [#38136](https://github.com/pingcap/tidb/issues/38136) @[jackysp](https://github.com/jackysp)

+ TiKV

    - Add a new configuration item `apply-yield-write-size` to control the maximum number of bytes that the Apply thread can write for one Finite-state Machine in one round of poll, and relieve Raftstore congestion when the Apply thread writes a large volume of data [#13313](https://github.com/tikv/tikv/issues/13313) @[glorv](https://github.com/glorv)
    - Warm up the entry cache before migrating the leader of Region to avoid QPS jitter during the leader transfer process [#13060](https://github.com/tikv/tikv/issues/13060) @[cosven](https://github.com/cosven)
    - Support pushing down the `json_constains` operator to Coprocessor [#13592](https://github.com/tikv/tikv/issues/13592) @[lizhenhuan](https://github.com/lizhenhuan)
    - Add the asynchronous function for `CausalTsProvider` to improve the flush performance in some scenarios [#13428](https://github.com/tikv/tikv/issues/13428) @[zeminzhou](https://github.com/zeminzhou)

+ PD

    - The v2 algorithm of the hot Region scheduler becomes GA. In some scenarios, the v2 algorithm can achieve better balancing in both configured dimensions and reduce invalid scheduling [#5021](https://github.com/tikv/pd/issues/5021) @[HundunDM](https://github.com/hundundm)
    - Optimize the timeout mechanism of operator step to avoid premature timeout [#5596](https://github.com/tikv/pd/issues/5596) @[bufferflies](https://github.com/bufferflies)
    - Improve the performance of the scheduler in large clusters [#5473](https://github.com/tikv/pd/issues/5473) @[bufferflies](https://github.com/bufferflies)
    - Support using external timestamp which is not provided by PD [#5637](https://github.com/tikv/pd/issues/5637) @[lhy1024](https://github.com/lhy1024)

+ TiFlash

    - Refactor the TiFlash MPP error handling logic to further improve the stability of MPP [#5095](https://github.com/pingcap/tiflash/issues/5095) @[windtalker](https://github.com/windtalker)
    - Optimize the sorting of the TiFlash computation process, and optimize the key handling for Join and Aggregation [#5294](https://github.com/pingcap/tiflash/issues/5294) @[solotzg](https://github.com/solotzg)
    - Optimize the memory usage for decoding and remove redundant transfer columns to improve Join performance [#6157](https://github.com/pingcap/tiflash/issues/6157) @[yibin87](https://github.com/yibin87)

+ Tools

    + TiDB Dashboard

        - Support displaying TiFlash metrics on the Monitoring page and optimize the presentation of metrics on that page [#1440](https://github.com/pingcap/tidb-dashboard/issues/1440) @[YiniXu9506](https://github.com/YiniXu9506)
        - Show the number of rows for results in the Slow Query list and SQL Statement list [#1443](https://github.com/pingcap/tidb-dashboard/issues/1443) @[baurine](https://github.com/baurine)
        - Optimize the Dashboard to not report the Alertmanager errors when Alertmanager does not exist [#1444](https://github.com/pingcap/tidb-dashboard/issues/1444) @[baurine](https://github.com/baurine)

    + Backup & Restore (BR)

        - Improve the mechanism for loading the metadata. The metadata is loaded into memory only when necessary, which significantly reduces the memory usage during PITR [#38404](https://github.com/pingcap/tidb/issues/38404) @[YuJuncen](https://github.com/YuJuncen)

    + TiCDC

        - Support replicating the exchange partition DDL statements [#639](https://github.com/pingcap/tiflow/issues/639) @[asddongmen](https://github.com/asddongmen)
        - Improve non-batch sending performance for the MQ sink module [#7353](https://github.com/pingcap/tiflow/issues/7353) @[hi-rustin](https://github.com/hi-rustin)
        - Improve performance of TiCDC puller when a table has a large number of Regions [#7078](https://github.com/pingcap/tiflow/issues/7078) [#7281](https://github.com/pingcap/tiflow/issues/7281) @[sdojjy](https://github.com/sdojjy)
        - Support reading historical data in the downstream TiDB by using the `tidb_enable_external_ts_read` variable when Syncpoint is enabled [#7419](https://github.com/pingcap/tiflow/issues/7419) @[asddongmen](https://github.com/asddongmen)
        - Enable transaction split and disable safeMode by default to improve the replication stability [#7505](https://github.com/pingcap/tiflow/issues/7505) @[asddongmen](https://github.com/asddongmen)

    + TiDB Data Migration (DM)

        - Remove the useless `operate-source update` command from dmctl [#7246](https://github.com/pingcap/tiflow/issues/7246) @[buchuitoudegou](https://github.com/buchuitoudegou)
        - Fix the issue that DM full import fails if the upstream database uses DDL statements that are incompatible with TiDB. You can create the schema of target tables in TiDB manually in advance using DDL statements supported by TiDB to ensure successful import  [#37984](https://github.com/pingcap/tidb/issues/37984) @[lance6716](https://github.com/lance6716)

    + TiDB Lightning

        - Optimize the file scanning logic to accelerate the scan of schema files [#38598](https://github.com/pingcap/tidb/issues/38598) @[dsdashun](https://github.com/dsdashun)

## Bug fixes

+ TiDB

    - Fix the potential issue of index inconsistency that occurs after you create a new index [#38165](https://github.com/pingcap/tidb/issues/38165) @[tangenta](https://github.com/tangenta)
    - Fix a permission issue of the `INFORMATION_SCHEMA.TIKV_REGION_STATUS` table [#38407](https://github.com/pingcap/tidb/issues/38407) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - Fix the issue that the `grantor` field is missing in the `mysql.tables_priv` table [#38293](https://github.com/pingcap/tidb/issues/38293) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - Fix the issue that the join result of common table expressions might be wrong [#38170](https://github.com/pingcap/tidb/issues/38170) @[wjhuang2016](https://github.com/wjhuang2016)
    - Fix the issue that the union result of common table expressions might be wrong [#37928](https://github.com/pingcap/tidb/issues/37928) @[YangKeao](https://github.com/YangKeao)
    - Fix the issue that the information in the **transaction region num** monitoring panel is incorrect [#38139](https://github.com/pingcap/tidb/issues/38139) @[jackysp](https://github.com/jackysp)
    - Fix the issue that the system variable [`tidb_constraint_check_in_place_pessimistic`](/system-variables.md#tidb_constraint_check_in_place_pessimistic-new-in-v630) might affect internal transactions. The variable scope is modified to SESSION. [#38766](https://github.com/pingcap/tidb/issues/38766) @[ekexium](https://github.com/ekexium)
    - Fix the issue that conditions in a query are mistakenly pushed down to projections [#35623](https://github.com/pingcap/tidb/issues/35623) @[Reminiscent](https://github.com/Reminiscent)
    - Fix the issue that the wrong `isNullRejected` check results for `AND` and `OR` cause wrong query results [#38304]( https://github.com/pingcap/tidb/issues/38304) @[Yisaer](https://github.com/Yisaer)
    - Fix the issue that `ORDER BY` in `GROUP_CONCAT` is not considered when the outer join is eliminated, which causes wrong query results [#18216](https://github.com/pingcap/tidb/issues/18216) @[winoros](https://github.com/winoros)
    - Fix the issue of the wrong query result that occurs when the mistakenly pushed-down conditions are discarded by Join Reorder [#38736](https://github.com/pingcap/tidb/issues/38736) @[winoros](https://github.com/winoros)

+ TiKV

    - Fix the issue that TiDB fails to start on Gitpod when there are multiple `cgroup` and `mountinfo` records [#13660](https://github.com/tikv/tikv/issues/13660) @[tabokie](https://github.com/tabokie)
    - Fix the wrong expression of a TiKV metric `tikv_gc_compaction_filtered` [#13537](https://github.com/tikv/tikv/issues/13537) @[Defined2014](https://github.com/Defined2014)
    - Fix the performance issue caused by the abnormal `delete_files_in_range` [#13534](https://github.com/tikv/tikv/issues/13534) @[tabokie](https://github.com/tabokie)
    - Fix abnormal Region competition caused by expired lease during snapshot acquisition [#13553](https://github.com/tikv/tikv/issues/13553) @[SpadeA-Tang](https://github.com/SpadeA-Tang)
    - Fix errors occurred when `FLASHBACK` fails in the first batch [#13672](https://github.com/tikv/tikv/issues/13672) [#13704](https://github.com/tikv/tikv/issues/13704) [#13723](https://github.com/tikv/tikv/issues/13723) @[HuSharp](https://github.com/HuSharp)

+ PD

    - Fix inaccurate Stream timeout and accelerate leader switchover [#5207](https://github.com/tikv/pd/issues/5207) @[CabinfeverB](https://github.com/CabinfeverB)

+ TiFlash

    - Fix the OOM issue due to oversized WAL files that occurs when PageStorage GC does not clear the Page deletion marker properly [#6163](https://github.com/pingcap/tiflash/issues/6163) @[JaySon-Huang](https://github.com/JaySon-Huang)

+ Tools

    + TiDB Dashboard

        - Fix the TiDB OOM issue when querying execution plans of certain complex SQL statements [#1386](https://github.com/pingcap/tidb-dashboard/issues/1386) @[baurine](https://github.com/baurine)
        - Fix the issue that the Top SQL switch might not take effect when NgMonitoring loses the connection to the PD nodes [#164](https://github.com/pingcap/ng-monitoring/issues/164) @[zhongzc](https://github.com/zhongzc)

    + Backup & Restore (BR)

        - Fix the restoration failure issue caused by PD leader switch during the restoration process [#36910](https://github.com/pingcap/tidb/issues/36910) @[MoCuishle28](https://github.com/MoCuishle28)
        - Fix the issue that the log backup task cannot be paused [#38250](https://github.com/pingcap/tidb/issues/38250) @[joccau](https://github.com/joccau)
        - Fix the issue that when BR deletes log backup data, it mistakenly deletes data that should not be deleted [#38939](https://github.com/pingcap/tidb/issues/38939) @[Leavrth](https://github.com/leavrth)
        - Fix the issue that BR fails to delete data when deleting the log backup data stored in Azure Blob Storage or Google Cloud Storage for the first time [#38229](https://github.com/pingcap/tidb/issues/38229) @[Leavrth](https://github.com/leavrth)

    + TiCDC

        - Fix the issue that `sasl-password` in the `changefeed query` result is not masked [#7182](https://github.com/pingcap/tiflow/issues/7182) @[dveeden](https://github.com/dveeden)
        - Fix the issue that TiCDC might become unavailable when too many operations in an etcd transaction are committed [#7131](https://github.com/pingcap/tiflow/issues/7131) @[asddongmen](https://github.com/asddongmen)
        - Fix the issue that redo logs might be deleted incorrectly [#6413](https://github.com/pingcap/tiflow/issues/6413) @[asddongmen](https://github.com/asddongmen)
        - Fix performance regression when replicating wide tables in Kafka Sink V2 [#7344](https://github.com/pingcap/tiflow/issues/7344) @[hi-rustin](https://github.com/hi-rustin)
        - Fix the issue that checkpoint ts might be advanced incorrectly [#7274](https://github.com/pingcap/tiflow/issues/7274) @[hi-rustin](https://github.com/hi-rustin)
        - Fix the issue that too many logs are printed due to improper log level of the mounter module [#7235](https://github.com/pingcap/tiflow/issues/7235) @[hi-rustin](https://github.com/hi-rustin)
        - Fix the issue that a TiCDC cluster might have two owners [#4051](https://github.com/pingcap/tiflow/issues/4051) @[asddongmen](https://github.com/asddongmen)

    + TiDB Data Migration (DM)

        - Fix the issue that DM WebUI generates the wrong `allow-list` parameter [#7096](https://github.com/pingcap/tiflow/issues/7096) @[zoubingwu](https://github.com/zoubingwu)
        - Fix the issue that a DM-worker has a certain probability of triggering data race when it starts or stops [#6401](https://github.com/pingcap/tiflow/issues/6401) @[liumengya94](https://github.com/liumengya94)
        - Fix the issue that when DM replicates an `UPDATE` or `DELETE` statement but the corresponding row data does not exist, DM silently ignores the event [#6383](https://github.com/pingcap/tiflow/issues/6383) @[GMHDBJD](https://github.com/GMHDBJD)
        - Fix the issue that the `secondsBehindMaster` field is not displayed after you run the `query-status` command [#7189](https://github.com/pingcap/tiflow/issues/7189) @[GMHDBJD](https://github.com/GMHDBJD)
        - Fix the issue that updating the checkpoint may trigger a large transaction [#5010](https://github.com/pingcap/tiflow/issues/5010) @[lance6716](https://github.com/lance6716)
        - Fix the issue that in full task mode, when a task enters the sync stage and fails immediately, DM may lose upstream table schema information [#7159](https://github.com/pingcap/tiflow/issues/7159) @[lance6716](https://github.com/lance6716)
        - Fix the issue that deadlock may be triggered when the consistency check is enabled [#7241](https://github.com/pingcap/tiflow/issues/7241) @[buchuitoudegou](https://github.com/buchuitoudegou)
        - Fix the issue that task precheck requires the `SELECT` privilege for the `INFORMATION_SCHEMA` table [#7317](https://github.com/pingcap/tiflow/issues/7317) @[lance6716](https://github.com/lance6716)
        - Fix the issue that an empty TLS configuration causes an error [#7384](https://github.com/pingcap/tiflow/issues/7384) @[liumengya94](https://github.com/liumengya94)

    + TiDB Lightning

        - Fix the import performance degradation when importing the Apache Parquet files to the target tables that contain the string type columns in the`binary` encoding format [#38351](https://github.com/pingcap/tidb/issues/38351) @[dsdashun](https://github.com/dsdashun)

    + TiDB Dumpling

        - Fix the issue that Dumpling might time out when exporting a lot of tables [#36549](https://github.com/pingcap/tidb/issues/36549) @[lance6716](https://github.com/lance6716)
        - Fix lock errors reported when consistency lock is enabled but the upstream has no target table [#38683](https://github.com/pingcap/tidb/issues/38683) @[lance6716](https://github.com/lance6716)

## Contributors

We would like to thank the following contributors from the TiDB community:

- [645775992](https://github.com/645775992)
- [An-DJ](https://github.com/An-DJ)
- [AndrewDi](https://github.com/AndrewDi)
- [erwadba](https://github.com/erwadba)
- [fuzhe1989](https://github.com/fuzhe1989)
- [goldwind-ting](https://github.com/goldwind-ting) (First-time contributor)
- [h3n4l](https://github.com/h3n4l)
- [igxlin](https://github.com/igxlin) (First-time contributor)
- [ihcsim](https://github.com/ihcsim)
- [JigaoLuo](https://github.com/JigaoLuo)
- [morgo](https://github.com/morgo)
- [Ranxy](https://github.com/Ranxy)
- [shenqidebaozi](https://github.com/shenqidebaozi) (First-time contributor)
- [taofengliu](https://github.com/taofengliu) (First-time contributor)
- [TszKitLo40](https://github.com/TszKitLo40)
- [wxbty](https://github.com/wxbty) (First-time contributor)
- [zgcbj](https://github.com/zgcbj)
