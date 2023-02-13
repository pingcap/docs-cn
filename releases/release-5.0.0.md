---
title: What's New in TiDB 5.0
---

# What's New in TiDB 5.0

Release date: April 7, 2021

TiDB version: 5.0.0

In v5.0, PingCAP is dedicated to helping enterprises quickly build applications based on TiDB, freeing them from worries about database performance, performance jitter, security, high availability, disaster recovery, troubleshooting SQL performance, and so on.

In v5.0, the key new features or improvements are as follows:

+ Introduce Massively Parallel Processing (MPP) architecture through TiFlash nodes, which shares the execution workloads of large join queries among TiFlash nodes. When the MPP mode is enabled, TiDB, based on cost, determines whether to use the MPP framework to perform the calculation. In the MPP mode, the join keys are redistributed through the `Exchange` operation while being calculated, which distributes the calculation pressure to each TiFlash node and speeds up the calculation. According to the benchmark, with the same cluster resource, TiDB 5.0 MPP shows 2 to 3 times of speedup over Greenplum 6.15.0 and Apache Spark 3.1.1, and some queries have 8 times better performance.
+ Introduce the clustered index feature to improve database performance. For example, in the TPC-C tpmC test, the performance of TiDB, with clustered index enabled, improves by 39%.
+ Enable the async commit feature to reduce the write latency. For example, in the 64-thread Sysbench test, the average latency of updating indexes, with async commit enabled, is reduced by 41.7%, from 12.04 ms to 7.01 ms.
+ Reduce jitters. This is achieved by improving the optimizer stability and by limiting system tasks' usages of I/O, network, CPU, and memory resources. For example, in the 8-hour performance test, the standard deviation of TPC-C tpmC does not exceed 2%.
+ Enhance system stability by improving scheduling and by keeping execution plans stable as much as possible.
+ Introduces Raft Joint Consensus algorithm, which ensures the system availability during the Region membership change.
+ Optimize `EXPLAIN` features and invisible index, which helps Database Administrators (DBAs) debug SQL statements more efficiently.
+ Guarantee reliability for enterprise data. You can back up data from TiDB to Amazon S3 storage and Google Cloud GCS, or restore data from these cloud storage platforms.
+ Improve performance of data import from or data export to Amazon S3 storage or TiDB/MySQL, which helps enterprises quickly build applications on the cloud. For example, in the TPC-C test, the performance of importing 1 TiB data improves by 40%, from 254 GiB/h to 366 GiB/h.

## Compatibility changes

### System variables

+ Add the [`tidb_executor_concurrency`](/system-variables.md#tidb_executor_concurrency-new-in-v50) system variable to control the concurrency of multiple operators. The previous `tidb_*_concurrency` settings (such as `tidb_projection_concurrency`) still take effect but with a warning when you use them.
+ Add the [`tidb_skip_ascii_check`](/system-variables.md#tidb_skip_ascii_check-new-in-v50) system variable to specify whether to skip the ASCII validation check when the ASCII character set is written. This default value is `OFF`.
+ Add the [`tidb_enable_strict_double_type_check`](/system-variables.md#tidb_enable_strict_double_type_check-new-in-v50) system variable to determine whether the syntax like `double(N)` can be defined in the table schema. This default value is `OFF`.
+ Change the default value of [`tidb_dml_batch_size`](/system-variables.md#tidb_dml_batch_size) from `20000` to `0`. This means that batch DML statements are no longer used by default in `LOAD`/`INSERT INTO SELECT ...`. Instead, large transactions are used to comply with the strict ACID semantics.

    > **Note:**
    >
    > The scope of the variable is changed from session to global, and the default value is changed from `20000` to `0`. If the application relies on the original default value, you need to use the `set global` statement to modify the variable to the original value after the upgrade.

+ Control temporary tables' syntax compatibility using the [`tidb_enable_noop_functions`](/system-variables.md#tidb_enable_noop_functions-new-in-v40) system variable. When this variable value is `OFF`, the `CREATE TEMPORARY TABLE` syntax returns an error.
+ Add the following system variables to directly control the garbage collection-related parameters:
    - [`tidb_gc_concurrency`](/system-variables.md#tidb_gc_concurrency-new-in-v50)
    - [`tidb_gc_enable`](/system-variables.md#tidb_gc_enable-new-in-v50)
    - [`tidb_gc_life_time`](/system-variables.md#tidb_gc_life_time-new-in-v50)
    - [`tidb_gc_run_interval`](/system-variables.md#tidb_gc_run_interval-new-in-v50)
    - [`tidb_gc_scan_lock_mode`](/system-variables.md#tidb_gc_scan_lock_mode-new-in-v50)
+ Change the default value of [`enable-joint-consensus`](/pd-configuration-file.md#enable-joint-consensus-new-in-v50) from `false` to `true`, which enables the Joint Consensus feature by default.
+ Change the value of `tidb_enable_amend_pessimistic_txn` from `0` or `1` to `ON` or `OFF`.
+ Change the default value of [`tidb_enable_clustered_index`](/system-variables.md#tidb_enable_clustered_index-new-in-v50) from `OFF` to `INT_ONLY` with the following new meanings:
    + `ON`: clustered index is enabled. Adding or deleting non-clustered indexes is supported.
    + `OFF`: clustered index is disabled. Adding or deleting non-clustered indexes is supported.
    + `INT_ONLY`: the default value. The behavior is consistent with that before v5.0. You can control whether to enable clustered index for the INT type together with `alter-primary-key = false`.

    > **Note:**
    >
    > The `INT_ONLY` value of `tidb_enable_clustered_index` in 5.0 GA has the same meaning as the `OFF` value in 5.0 RC. After upgrading from a 5.0 RC cluster with the `OFF` setting to 5.0 GA, it will be displayed as `INT_ONLY`.

### Configuration file parameters

+ Add the [`index-limit`](/tidb-configuration-file.md#index-limit-new-in-v50) configuration item for TiDB. Its value defaults to `64` and ranges between `[64,512]`. A MySQL table supports 64 indexes at most. If its value exceeds the default setting and more than 64 indexes are created for a table, when the table schema is re-imported into MySQL, an error will be reported.
+ Add the [`enable-enum-length-limit`](/tidb-configuration-file.md#enable-enum-length-limit-new-in-v50) configuration item for TiDB to be compatible and consistent with MySQL's ENUM/SET length (ENUM length < 255). The default value is `true`.
+ Replace the `pessimistic-txn.enable` configuration item with the [`tidb_txn_mode`](/system-variables.md#tidb_txn_mode) environment variable.
+ Replace the `performance.max-memory` configuration item with [`performance.server-memory-quota`](/tidb-configuration-file.md#server-memory-quota-new-in-v409)
+ Replace the `tikv-client.copr-cache.enable` configuration item with [`tikv-client.copr-cache.capacity-mb`](/tidb-configuration-file.md#capacity-mb). If the item's value is `0.0`, this feature is disabled. If the item's value is greater than `0.0`, this feature is enabled. Its default value is `1000.0`.
+ Replace the `rocksdb.auto-tuned` configuration item with [`rocksdb.rate-limiter-auto-tuned`](/tikv-configuration-file.md#rate-limiter-auto-tuned-new-in-v50).
+ Delete the `raftstore.sync-log` configuration item. By default, written data is forcibly spilled to the disk. Before v5.0, you can explicitly disable `raftstore.sync-log`. Since v5.0, the configuration value is forcibly set to `true`.
+ Change the default value of the `gc.enable-compaction-filter` configuration item from `false` to `true`.
+ Change the default value of the `enable-cross-table-merge` configuration item from `false` to `true`.
+ Change the default value of the [`rate-limiter-auto-tuned`](/tikv-configuration-file.md#rate-limiter-auto-tuned-new-in-v50) configuration item from `false` to `true`.

### Others

+ Before the upgrade, check the value of the TiDB configuration [`feedback-probability`](https://docs.pingcap.com/tidb/v5.0/tidb-configuration-file#feedback-probability). If the value is not 0, the "panic in the recoverable goroutine" error will occur after the upgrade, but this error does not affect the upgrade.
+ Forbid conversion between `VARCHAR` type and `CHAR` type during the column type change to avoid data correctness issues.

## New features

### SQL

#### List partitioning (**Experimental**)

[User document](/partitioned-table.md#list-partitioning)

With the list partitioning feature, you can effectively query and maintain tables with a large amount of data.

With this feature enabled, partitions and how data is distributed among partitions are defined according to the `PARTITION BY LIST(expr) PARTITION part_name VALUES IN (...)` expression. The partitioned tables' data set supports at most 1024 distinct integer values. You can define the values using the `PARTITION ... VALUES IN (...)` clause.

To enable list partitioning, set the session variable [`tidb_enable_list_partition`](/system-variables.md#tidb_enable_list_partition-new-in-v50) to `ON`.

#### List COLUMNS partitioning (**Experimental**)

[User document](/partitioned-table.md#list-columns-partitioning)

List COLUMNS partitioning is a variant of list partitioning. You can use multiple columns as partition keys. Besides the integer data type, you can also use the columns in the string, `DATE`, and `DATETIME` data types as partition columns.

To enable List COLUMNS partitioning, set the session variable [`tidb_enable_list_partition`](/system-variables.md#tidb_enable_list_partition-new-in-v50) to `ON`.

#### Invisible indexes

[User document](/sql-statements/sql-statement-alter-index.md), [#9246](https://github.com/pingcap/tidb/issues/9246)

When you tune performance or select optimal indexes, you can set an index to be `Visible` or `Invisible` by using SQL statements. This setting can avoid performing resource-consuming operations, such as `DROP INDEX` and `ADD INDEX`.

To modify the visibility of an index, use the `ALTER INDEX` statement. After the modification, the optimizer decides whether to add this index to the index list based on the index visibility.

#### `EXCEPT` and `INTERSECT` operators

[User document](/functions-and-operators/set-operators.md), [#18031](https://github.com/pingcap/tidb/issues/18031)

The `INTERSECT` operator is a set operator, which returns the intersection of the result sets of two or more queries. To some extent, it is an alternative to the `Inner Join` operator.

The `EXCEPT` operator is a set operator, which combines the result sets of two queries and returns elements that are in the first query result but not in the second.

### Transaction

[#18005](https://github.com/pingcap/tidb/issues/18005)

In the pessimistic transaction mode, if the tables involved in a transaction contain concurrent DDL operations or `SCHEMA VERSION` changes, the system automatically updates the transaction's `SCHEMA VERSION` to the latest to ensure the successful transaction commit, and to avoid that the client receives the `Information schema is changed` error when the transaction is interrupted by DDL operations or `SCHEMA VERSION` changes.

This feature is disabled by default. To enable the feature, modify the value of `tidb_enable_amend_pessimistic_txn` system variable. This feature is introduced in v4.0.7 and has the following issues fixed in v5.0:

+ The compatibility issue that occurs when TiDB Binlog executes `Add Column` operations
+ The data inconsistency issue that occurs when using the feature together with the unique index
+ The data inconsistency issue that occurs when using the feature together with the added index

Currently, this feature still has the following incompatibility issues:

+ Transaction's semantics might change when there are concurrent transactions
+ Known compatibility issue that occurs when using the feature together with TiDB Binlog
+ Incompatibility with `Change Column`

### Character set and collation

- Support the `utf8mb4_unicode_ci` and `utf8_unicode_ci` collations. [User document](/character-set-and-collation.md#new-framework-for-collations), [#17596](https://github.com/pingcap/tidb/issues/17596)
- Support the case-insensitive comparison sort for collations

### Security

[User document](/log-redaction.md), [#18566](https://github.com/pingcap/tidb/issues/18566)

To meet security compliance requirements (such as *General Data Protection Regulation*, or GDPR), the system supports desensitizing information (such as ID and credit card number) in the output error messages and logs, which can avoid leaking sensitive information.

TiDB supports desensitizing the output log information. To enable this feature, use the following switches:

+ The global variable [`tidb_redact_log`](/system-variables.md#tidb_redact_log). Its default value is `0`, which means that desensitization is disabled. To enable desensitization for tidb-server logs, set the variable value to `1`.
+ The configuration item `security.redact-info-log`. Its default value is `false`, which means that desensitization is disabled. To enable desensitization for tikv-server logs, set the variable value to `true`.
+ The configuration item `security.redact-info-log`. Its default value is `false`, which means that desensitization is disabled. To enable desensitization for pd-server logs, set the variable value to `true`.
+ The configuration item `security.redact_info_log` for tiflash-server and `security.redact-info-log` for tiflash-learner. Their default values are both `false`, which means that desensitization is disabled. To enable desensitization for tiflash-server and tiflash-learner logs, set the values of both variables to `true`.

This feature is introduced in v5.0. To use the feature, enable the system variable and all configuration items above.

## Performance optimization

### MPP architecture

[User document](/tiflash/use-tiflash-mpp-mode.md)

TiDB introduces the MPP architecture through TiFlash nodes. This architecture allows multiple TiFlash nodes to share the execution workload of large join queries.

When the MPP mode is on, TiDB determines whether to send a query to the MPP engine for computation based on the calculation cost. In the MPP mode, TiDB distributes the computation of table joins to each running TiFlash node by redistributing the join key during data calculation (`Exchange` operation), and thus accelerates the calculation. Furthermore, with the aggregation computing feature that TiFlash has already supported, TiDB can pushdown the computation of a query to the TiFlash MPP cluster. Then the distributed environment can help accelerate the entire execution process and dramatically increase the speed of analytic queries.

In the TPC-H 100 benchmark test, TiFlash MPP delivers significant processing speed over analytic engines of traditional analytic databases and SQL on Hadoop. With this architecture, you can perform large-scale analytic queries directly on the latest transaction data, with a higher performance than traditional offline analytic solutions. According to the benchmark, with the same cluster resource, TiDB 5.0 MPP shows 2 to 3 times of speedup over Greenplum 6.15.0 and Apache Spark 3.1.1, and some queries have 8 times better performance.

Currently, the main features that the MPP mode does not support are as follows (For details, refer to [Use TiFlash](/tiflash/use-tiflash-mpp-mode.md)):

+ Table partitioning
+ Window Function
+ Collation
+ Some built-in functions
+ Reading data from TiKV
+ OOM spill
+ Union
+ Full Outer Join

### Clustered index

[User document](/clustered-indexes.md), [#4841](https://github.com/pingcap/tidb/issues/4841)

When you are designing table structures or analyzing database behaviors, it is recommended to use the clustered index feature if you find that some columns with primary keys are often grouped and sorted, queries on these columns often return a certain range of data or a small amount of data with different values, and the corresponding data does not cause read or write hotspot issues.

Clustered indexes, also known as _index-organized tables_ in some database management systems, is a storage structure associated with the data of a table. When creating a clustered index, you can specify one or more columns from the table as the keys for the index. TiDB stores these keys in a specific structure, which allows TiDB to quickly and efficiently find the rows associated with the keys, thus improves the performance of querying and writing data.

When the clustered index feature is enabled, the TiDB performance improves significantly (for example in the TPC-C tpmC test, the performance of TiDB, with clustered index enabled, improves by 39%) in the following cases:

+ When data is inserted, the clustered index reduces one write of the index data from the network.
+ When a query with an equivalent condition only involves the primary key, the clustered index reduces one read of index data from the network.
+ When a query with a range condition only involves the primary key, the clustered index reduces multiple reads of index data from the network.
+ When a query with an equivalent or range condition involves the primary key prefix, the clustered index reduces multiple reads of index data from the network.

Each table can either use a clustered or non-clustered index to sort and store data. The differences of these two storage structures are as follows:

+ When creating a clustered index, you can specify one or more columns in the table as the key value of the index. A clustered index sorts and stores the data of a table according to the key value. Each table can have only one clustered index. If a table has a clustered index, it is called a clustered index table. Otherwise, it is called a non-clustered index table.
+ When you create a non-clustered index, the data in the table is stored in an unordered structure. You do not need to explicitly specify the key value of the non-clustered index, because TiDB automatically assigns a unique ROWID to each row of data. During a query, the ROWID is used to locate the corresponding row. Because there are at least two network I/O operations when you query or insert data, the performance is degraded compared with clustered indexes.

When table data is modified, the database system automatically maintains clustered indexes and non-clustered indexes for you.

All primary keys are created as non-clustered indexes by default. You can create a primary key as a clustered index or non-clustered index in either of the following two ways:

+ Specify the keyword `CLUSTERED | NONCLUSTERED` in the statement when creating a table, then the system creates the table in the specified way. The syntax is as follows:

```sql
CREATE TABLE `t` (`a` VARCHAR(255), `b` INT, PRIMARY KEY (`a`, `b`) CLUSTERED);
```

Or

```sql
CREATE TABLE `t` (`a` VARCHAR(255) PRIMARY KEY CLUSTERED, `b` INT);
```

You can execute the statement `SHOW INDEX FROM tbl-name` to query whether a table has a clustered index.

+ Configure the system variable `tidb_enable_clustered_index` to control the clustered index feature. Supported values are `ON`, `OFF`, and `INT_ONLY`.
    + `ON`: Indicates that the clustered index feature is enabled for all types of primary keys. Adding and dropping non-clustered indexes are supported.
    + `OFF`: Indicates that the clustered index feature is disabled for all types of primary keys. Adding and dropping non-clustered indexes are supported.
    + `INT_ONLY`: The default value. If the variable is set to `INT_ONLY` and `alter-primary-key` is set to `false`, the primary keys which consist of single integer columns are created as clustered indexes by default. The behavior is consistent with that of TiDB v5.0 and earlier versions.

If a `CREATE TABLE` statement contains the keyword `CLUSTERED | NONCLUSTERED`, the statement overrides the configuration of the system variable and the configuration item.

You are recommended to use the clustered index feature by specifying the keyword `CLUSTERED | NONCLUSTERED` in statements. In this way, it is more flexible for TiDB to use all data types of clustered and non-clustered indexes in the system at the same time as required.

It is not recommended to use `tidb_enable_clustered_index = INT_ONLY`, because `INT_ONLY` is temporarily used to make this feature compatible and will be deprecated in the future.

Limitations for the clustered index are as follows:

+ Mutual conversion between clustered indexes and non-clustered indexes is not supported.
+ Dropping clustered indexes is not supported.
+ Adding, dropping, and altering clustered indexes using `ALTER TABLE` statements are not supported.
+ Reorganizing and re-creating a clustered index is not supported.
+ Enabling or disabling indexes is not supported, which means the invisible index feature is not effective for clustered indexes.
+ Creating a `UNIQUE KEY` as a clustered index is not supported.
+ Using the clustered index feature together with TiDB Binlog is not supported. After TiDB Binlog is enabled, TiDB only supports creating a single integer primary key as a clustered index. TiDB Binlog does not replicate data changes of existing tables with clustered indexes to the downstream.
+ Using the clustered index feature together with the attributes `SHARD_ROW_ID_BITS` and `PRE_SPLIT_REGIONS` is not supported.
+ If the cluster is upgraded to a later version then rolls back, you need to downgrade newly-added tables by exporting table data before the rollback and importing the data after the rollback. Other tables are not affected.

### Async Commit

[User document](/system-variables.md#tidb_enable_async_commit-new-in-v50), [#8316](https://github.com/tikv/tikv/issues/8316)

The client of the database will wait for the database system to complete the transaction commit in two phases (2PC) synchronously. The transaction returns the result to the client after the first phase commit is successful, and the system executes the second phase commit operation in the background asynchronously to reduce the transaction commit latency. If the transaction write involves only one Region, the second phase is omitted directly, and the transaction becomes a one-phase commit.

After the Async Commit feature is enabled, with the same hardware and configuration, when Sysbench is set to test the Update index with 64 threads, the average latency decreases by 41.7% from 12.04ms to 7.01ms.

When Async Commit feature is enabled, to reduce one network interaction latency and improve the performance of data writes, database application developers are recommended to consider reducing the consistency of transactions from linear consistency to [causal consistency](/transaction-overview.md#causal-consistency). The SQL statement to enable causal consistency is `START TRANSACTION WITH CAUSAL CONSISTENCY`.

After the causal consistency is enabled, with the same hardware and configuration, when Sysbench is set to test oltp_write_only with 64 threads, the average latency decreased by 5.6% from 11.86ms to 11.19ms.

After the consistency of transactions is reduced from the linear consistency to causal consistency, if there is no interdependence between multiple transactions in the application, the transactions do not have a globally consistent order.

**The Async Commit feature is enabled by default for newly created v5.0 clusters.**

This feature is disabled by default for clusters upgraded from earlier versions to v5.0. You can enable this feature by executing the `set global tidb_enable_async_commit = ON;` and `set global tidb_enable_1pc = ON;` statements.

The limitation for the Async Commit feature is as follows:

+ Direct downgrade is not supported.

### Enable the Coprocessor cache feature by default

[User document](/tidb-configuration-file.md#tikv-clientcopr-cache-new-in-v400), [#18028](https://github.com/pingcap/tidb/issues/18028)

In 5.0 GA, the Coprocessor cache feature is enabled by default. After this feature is enabled, to reduce the latency of reading data, TiDB caches the calculation results of the operators pushed down to tikv-server in tidb-server.

To disable the Coprocessor cache feature, you can modify the `capacity-mb` configuration item of `tikv-client.copr-cache` to `0.0`.

### Improve the execution performance of `delete from table where id <? Limit ?` statement

[#18028](https://github.com/pingcap/tidb/issues/18028)

The p99 performance of the `delete from table where id <? limit ?` statement is improved by 4 times.

### Optimize load base split strategy to solve the performance problem that data cannot be split in some small table hotspot read scenarios

[#18005](https://github.com/pingcap/tidb/issues/18005)

## Improve stability

### Optimize the performance jitter issue caused by imperfect scheduling

[#18005](https://github.com/pingcap/tidb/issues/18005)

The TiDB scheduling process occupies resources such as I/O, network, CPU, and memory. If TiDB does not control the scheduled tasks, QPS and delay might cause performance jitter due to resource preemption.

After the following optimizations, in the 8-hour performance test, the standard deviation of TPC-C tpmC does not exceed 2%.

#### Introduce new scheduling calculation formulas to reduce unnecessary scheduling and performance jitter

When the node capacity is always near the waterline set in the system, or when the `store-limit` is set too large, to balance the capacity load, the system frequently schedules Regions to other nodes or even schedules Regions back to their original nodes. Because scheduling occupies resources, such as I/O, network, CPU, and memory, and causes performance jitter, this type of scheduling is not necessary.

To mitigate this issue, PD introduces a new set of default scheduling calculation formulas. You can switch back to the old formulas by configuring `region-score-formula-version = v1`.

#### Enable the cross-table Region merge feature by default

[User document](/pd-configuration-file.md#enable-cross-table-merge)

Before v5.0, TiDB disables the cross-table Region merge feature by default. Starting from v5.0, this feature is enabled by default to reduce the number of empty Regions and the overhead of network, memory, and CPU. You can disable this feature by modifying the `schedule.enable-cross-table-merge` configuration item.

#### Enable the system to automatically adjust the data compaction speed by default to balance the contention for I/O resources between background tasks and foreground reads and writes

[User document](/tikv-configuration-file.md#rate-limiter-auto-tuned-new-in-v50)

Before v5.0, to balance the contention for I/O resources between background tasks and foreground reads and writes, the feature that the system automatically adjusts the data compaction speed is disabled by default. Starting from v5.0, TiDB enables this feature by default and optimizes the algorithm so that the latency jitter is significantly reduced.

You can disable this feature by modifying the `rate-limiter-auto-tuned` configuration item.

#### Enable the GC Compaction Filter feature by default to reduce GC's consumption of CPU and I/O resources

[User document](/garbage-collection-configuration.md#gc-in-compaction-filter), [#18009](https://github.com/pingcap/tidb/issues/18009)

When TiDB performs garbage collection (GC) and data compaction, partitions occupy CPU and I/O resources. Overlapping data exists during the execution of these two tasks.

To reduce GC's consumption of CPU and I/O resources, the GC Compaction Filter feature combines these two tasks into one and executes them in the same task. This feature is enabled by default. You can disable it by configuring `gc.enable-compaction-filter = false`.

#### TiFlash limits the compression and data sorting's use of I/O resources (**experimental feature**)

This feature alleviates the contention for I/O resources between background tasks and foreground reads and writes.

This feature is disabled by default. You can enable this feature by modifying the `bg_task_io_rate_limit` configuration item.

#### Improve the performance of checking scheduling constraints and the performance of fixing the unhealthy Regions in a large cluster

### Ensure that the execution plans are unchanged as much as possible to avoid performance jitter

[User document](/sql-plan-management.md)

#### SQL Binding supports the `INSERT`、`REPLACE`、`UPDATE`、`DELETE` statements

When tuning performance or maintaining the database, if you find that the system performance is unstable due to unstable execution plans, you can select a manually optimized SQL statement according to your judgement or tested by `EXPLAIN ANALYZE`. You can bind the optimized SQL statement to the SQL statement to be executed in the application code to ensure stable performance.

When manually binding SQL statements using the SQL BINDING statement, you need to ensure that the optimized SQL statement has the same syntax as the original SQL statement.

You can view the manually or automatically bound execution plan information by running the `SHOW {GLOBAL | SESSION} BINDINGS` command. The output is the same as that of versions earlier than v5.0.

#### Automatically capture and bind execution plans

When upgrading TiDB, to avoid performance jitter, you can enable the baseline capturing feature to allow the system to automatically capture and bind the latest execution plan and store it in the system table. After TiDB is upgraded, you can export the bound execution plan by running the `SHOW GLOBAL BINDING` command and decide whether to delete these plans.

This feature is disbled by default. You can enable it by modifying the server or setting the `tidb_capture_plan_baselines` global system variable to `ON`. When this feature is enabled, the system fetches the SQL statements that appear at least twice from the Statement Summary every `bind-info-lease` (the default value is `3s`), and automatically captures and binds these SQL statements.

### Improve stability of TiFlash queries

Add a system variable [`tidb_allow_fallback_to_tikv`](/system-variables.md#tidb_allow_fallback_to_tikv-new-in-v50) to fall back queries to TiKV when TiFlash fails. The default value is `OFF`.

### Improve TiCDC stability and alleviate the OOM issue caused by replicating too much incremental data

[User document](/ticdc/ticdc-manage-changefeed.md#unified-sorter), [#1150](https://github.com/pingcap/tiflow/issues/1150)

In TiCDC v4.0.9 or earlier versions, replicating too much data change might cause OOM. In v5.0, the Unified Sorter feature is enabled by default to mitigate OOM issues caused by the following scenarios:

- The data replication task in TiCDC is paused for a long time, during which a large amount of incremental data is accumulated and needs to be replicated.
- The data replication task is started from an early timestamp, so it becomes necessary to replicate a large amount of incremental data.

Unified Sorter is integrated with the `memory`/`file` sort-engine options of earlier versions. You do not need to manually configure the change.

Limitations:

- You need to provide sufficient disk capacity according to the amount of your incremental data. It is recommended to use SSDs with free capacity greater than 128 GB.

## High availability and disaster recovery

### Improve system availability during Region membership change

[User document](/pd-configuration-file.md#enable-joint-consensus-new-in-v50), [#18079](https://github.com/pingcap/tidb/issues/18079), [#7587](https://github.com/tikv/tikv/issues/7587), [#2860](https://github.com/tikv/pd/issues/2860)

In the process of Region membership changes, "adding a member" and "deleting a member" are two operations performed in two steps. If a failure occurs when the membership change finishes, the Regions will become unavailable and an error of foreground application is returned.

The introduced Raft Joint Consensus algorithm can improve the system availability during Region membership change. "adding a member" and "deleting a member" operations during the membership change are combined into one operation and sent to all members. During the change process, Regions are in an intermediate state. If any modified member fails, the system is still available.

This feature is enabled by default. You can disable it by running the `pd-ctl config set enable-joint-consensus` command to set the `enable-joint-consensus` value to `false`.

### Optimize the memory management module to reduce system OOM risks

Track the memory usage of aggregate functions. This feature is enabled by default. When SQL statements with aggregate functions are executed, if the total memory usage of the current query exceeds the threshold set by `mem-quota-query`, the system automatically performs operations defined by `oom-action`.

### Improve the system availability during network partition

## Data migration

### Migrate data from S3/Aurora to TiDB

TiDB data migration tools support using Amazon S3 (and other S3-compatible storage services) as the intermediate for data migration and initializing Aurora snapshot data directly into TiDB, providing more options for migrating data from Amazon S3/Aurora to TiDB.

To use this feature, refer to the following documents:

- [Export data to Amazon S3 cloud storage](/dumpling-overview.md#export-data-to-amazon-s3-cloud-storage), [#8](https://github.com/pingcap/dumpling/issues/8)
- [Migrate from Amazon Aurora MySQL Using TiDB Lightning](/migrate-aurora-to-tidb.md), [#266](https://github.com/pingcap/tidb-lightning/issues/266)

### Optimize the data import performance of TiDB Cloud

TiDB Lightning optimizes its data import performance specifically for AWS T1.standard configurations (or equivalent) of TiDB Cloud. Test results show that TiDB Lightning improves its speed of importing 1TB of TPC-C data into TiDB by 40%, from 254 GiB/h to 366 GiB/h.

## Data sharing and subscription

### Integrate TiDB to Kafka Connect (Confluent Platform) using TiCDC (**experimental feature**)

[User document](/ticdc/integrate-confluent-using-ticdc.md), [#660](https://github.com/pingcap/tiflow/issues/660)

To support the business requirements of streaming TiDB data to other systems, this feature enables you to stream TiDB data to the systems such as Kafka, Hadoop, and Oracle.

The Kafka connectors protocol provided by the Confluent platform is widely used in the community, and it supports transferring data to either relational or non-relational databases in different protocols. By integrating TiCDC to Kafka Connect of the Confluent platform, TiDB extends the ability to stream TiDB data to other heterogeneous databases or systems.

## Diagnostics

[User document](/sql-statements/sql-statement-explain.md#explain)

During the troubleshooting of SQL performance issues, detailed diagnostic information is needed to determine the causes of performance issues. Before TiDB 5.0, the information collected by the `EXPLAIN` statements was not detailed enough. The root causes of the issues can only be determined based on log information, monitoring information, or even on guess, which might be inefficient.

In TiDB v5.0, the following improvements are made to help you troubleshoot performance issues more efficiently:

+ Support using the `EXPLAIN ANALYZE` statement to analyze all DML statements to show the actual performance plans and the execution information of each operator. [#18056](https://github.com/pingcap/tidb/issues/18056)
+ Support using the `EXPLAIN FOR CONNECTION` statement to check the real-time status of all the SQL statements being executed. For example, you can use the statement to check the execution duration of each operator and the number of processed rows. [#18233](https://github.com/pingcap/tidb/issues/18233)
+ Provide more details about the operator execution in the output of the `EXPLAIN ANALYZE` statement, including the number of RPC requests sent by operators, the duration of resolving lock conflicts, network latency, the scanned volume of deleted data in RocksDB, and the hit rate of RocksDB caches. [#18663](https://github.com/pingcap/tidb/issues/18663)
+ Support automatically recording the detailed execution information of SQL statements in the slow log. The execution information in the slow log is consistent with the output information of the `EXPLAIN ANALYZE` statement, which includes the time consumed by each operator, the number of processed rows, and the number of sent RPC requests. [#15009](https://github.com/pingcap/tidb/issues/15009)

## Deployment and maintenance

### Optimize the logic of cluster deployment operations, to help DBAs deploy a set of standard TiDB production cluster faster

[User Document](/production-deployment-using-tiup.md)

In previous TiDB versions, DBAs using TiUP to deploy TiDB clusters find that the environment initialization is complicated, the checksum configuration is excessive, and the cluster topology file is difficult to edit. All of these issues lead to low deployment efficiency for DBAs. In TiDB v5.0, the TiDB deployment efficiency using TiUP is improved for DBAs through the following items:

+ TiUP Cluster supports the `check topo.yaml` command to perform a more comprehensive one-click environment check and provide repair recommendations.
+ TiUP Cluster supports the `check topo.yaml --apply` command to automatically repair environmental problems found during the environment check.
+ TiUP Cluster supports the `template` command to get the cluster topology template file for DBAs to edit and support modifying the global node parameters.
+ TiUP supports editing the `remote_config` parameter using the `edit-config` command to configure remote Prometheus.
+ TiUP supports editing the `external_alertmanagers` parameter to configure different AlertManagers using the `edit-config` command.
+ When editing the topology file using the `edit-config` subcommand in tiup-cluster, you can modify the data types of the configuration item values.

### Improve upgrade stability

Before TiUP v1.4.0, during the upgrade of a TiDB cluster using tiup-cluster, the SQL responses of the cluster jitter for a long period of time, and during PD online rolling upgrades, the QPS of the cluster jitter between 10s to 30s.

TiUP v1.4.0 adjusts the logic and makes the following optimizations:

+ During the upgrade of PD nodes, TiUP automatically checks the status of the restarted PD node, and then rolls to upgrade the next PD node after confirming that the status is ready.
+ TiUP identifies the PD role automatically, first upgrades the PD nodes of the follower role, and finally upgrades the PD Leader node.

### Optimize the upgrade time

Before TiUP v1.4.0, when DBAs upgrade TiDB clusters using tiup-cluster, for clusters with a large number of nodes, the total upgrade time is long and cannot meet the upgrade time window requirement for certain users.

Starting from v1.4.0, TiUP optimizes the following items:

+ Supports fast offline upgrades using the `tiup cluster upgrade --offline` subcommand.
+ Speeds up the Region Leader relocation for users using rolling upgrades during upgrades by default, so that reduces the time of rolling TiKV upgrades.
+ Checks the status of the Region monitor using the `check` subcommand before running a rolling upgrade. Ensure that the cluster is in a normal state before the upgrade, thus reducing the probability of upgrade failures.

### Support the breakpoint feature

Before TiUP v1.4.0, when DBAs upgrade TiDB clusters using tiup-cluster, if the execution of a command is interrupted, all the upgrade operations have to be performed again from the beginning.

TiUP v1.4.0 supports retrying failed operations from breakpoints using the tiup-cluster `replay` subcommand, to avoid re-executing all operations after an upgrade interruption.

### Enhance the functionalities of maintenance and operations

TiUP v1.4.0 further enhances the functionalities for operating and maintaining TiDB clusters.

+ Supports the upgrade or patch operation on the downtime TiDB and DM clusters to adapt to more usage scenarios.
+ Adds the `--version` parameter to the `display` subcommand of tiup-cluster to get the cluster version.
+ When only Prometheus is included in the node being scaled out, the operation of updating the monitoring configuration is not performed, to avoid scale-out failure due to the absence of the Prometheus node.
+ Adds user input to the error message when the results of the input TiUP commands are incorrect, so that you can locate the cause of the problem more quickly.

## Telemetry

TiDB adds cluster usage metrics in telemetry, such as the number of data tables, the number of queries, and whether new features are enabled.

To learn more about details and how to disable this behavior, refer to [telemetry](/telemetry.md).
