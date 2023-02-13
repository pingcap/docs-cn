---
title: TiDB 5.0 RC Release Notes
---

# TiDB 5.0 RC Release Notes

Release date: January 12, 2021

TiDB version: 5.0.0-rc

TiDB v5.0.0-rc is the predecessor version of TiDB v5.0. In v5.0, PingCAP will be dedicated to helping enterprises quickly build applications based on TiDB, freeing them from worries about database performance, performance jitter, security, high availability, disaster recovery, troubleshooting SQL performance, and so on.

In v5.0, the key new features or improvements are as follows:

+ Clustered index. When this feature is enabled, database performance is improved. For example, in the TPC-C tpmC test, TiDB's performance, with clustered index enabled, improves by 39%.
+ Async commit. When this feature is enabled, the write latency is reduced. For example, in the Sysbench olpt-insert test, the write latency of TiDB, with async commit enabled, is reduced by 37.3%.
+ Reduced jitters. This is achieved by improving the optimizer stability and by limiting system tasks' usages of I/O, network, CPU, and memory resources. For example, in the 72-hour performance test, the standard deviation of Sysbench TPS jitter is reduced from 11.09% to 3.36%.
+ Raft Joint Consensus algorithm, which ensures the system availability during the Region membership change.
+ Optimized `EXPLAIN` features and invisible index, which helps Database Administrators (DBAs) debug SQL statements more efficiently.
+ Guaranteed reliability for enterprise data. You can back up data from TiDB to AWS S3 storage and Google Cloud GCS, or restore data from these cloud storage platforms.
+ Improved performance of data import from or data export to AWS S3 storage or TiDB/MySQL, which helps enterprises quickly build applications on the cloud. For example, in the TPC-C test, the performance of importing 1 TiB data improves by 40%, from 254 GiB/h to 366 GiB/h.

## SQL

### Support clustered index (experimental)

When the clustered index feature is enabled, TiDB performance improves significantly (for example in the TPC-C tpmC test, TiDB's performance, with clustered index enabled, improves by 39%) in the following cases:

+ When data is inserted, the clustered index reduces one write of the index data from the network.
+ When a query with an equivalent condition only involves the primary key, the clustered index reduces one read of index data from the network.
+ When a query with a range condition only involves the primary key, the clustered index reduces multiple reads of index data from the network.
+ When a query with an equivalent or range condition involves the primary key prefix, the clustered index reduces multiple reads of index data from the network.

Clustered index defines the physical storage order of data in a table. The data in the table is sorted only according to the definition of the clustered index. Each table has only one clustered index.

Users can enable the clustered index feature by modifying the `tidb_enable_clustered_index` variable. When enabled, the feature takes effect only on newly created tables and applies to the primary key that has multiple columns or is non-integer types in a single column. If the primary key is an integer type in a single column, or if the table has no primary key, the data is sorted in the same way as before, without being affected by the clustered index.

For example, to check whether a table (`tbl_name`) has a clustered index, execute `select tidb_pk_type from information_schema.tables where table_name = '{tbl_name}'`.

+ [User document](/system-variables.md#tidb_enable_clustered_index-new-in-v50)
+ Related issue: [#4841](https://github.com/pingcap/tidb/issues/4841)

### Support invisible indexes

When users tune performance or select optimal indexes, they can set an index to be `Visible` or `Invisible` by using SQL statements. This setting can avoid performing resource-consuming operations, such as `DROP INDEX` and `ADD INDEX`.

To modify the visibility of an index, use the `ALTER INDEX` statement. After the modification, the optimizer decides whether to add this index to the index list based on the index visibility.

+ [User document](/sql-statements/sql-statement-alter-index.md)
+ Related issue: [#9246](https://github.com/pingcap/tidb/issues/9246)

### Support `EXCEPT` and `INTERSECT` operators

The `INTERSECT` operator is a set operator, which returns the intersection of the result sets of two or more queries. To some extent, it is an alternative to the `InnerJoin` operator.

The `EXCEPT` operator is a set operator, which combines the result sets of two queries and returns elements that are in the first query result but not in the second.

+ [User document](/functions-and-operators/set-operators.md)
+ Related issue: [#18031](https://github.com/pingcap/tidb/issues/18031)

## Transaction

### Increase the success rate of executing pessimistic transactions

In the pessimistic transaction mode, if the tables involved in a transaction contain concurrent DDL operations or `SCHEMA VERSION` changes, the system automatically updates the transaction's `SCHEMA VERSION` to the latest to avoid the transaction being interrupted by DDL operations and to ensure the successful transaction commit. If the transaction is interrupted, the client receives the `Information schema is changed` error message.

+ Related issue: [#18005](https://github.com/pingcap/tidb/issues/18005)

## Character set and collation

Support case-insensitive comparison sort for character sets.

+ [User document](/character-set-and-collation.md#new-framework-for-collations)
+ Related issue: [#17596](https://github.com/pingcap/tidb/issues/17596)

## Security

### Support desensitizing error messages and log files

TiDB now supports desensitizing error messages and log files to avoid leaking sensitive information such as ID information and credit card number.

Users can enable the desensitization feature for different components:

+ For the TiDB side, set the `tidb_redact_log=1` variable using SQL statements in tidb-server.
+ For the TiKV side, set the `security.redact-info-log = true` configuration in tikv-server.
+ For the PD side, set the `security.redact-info-log = true` configuration in pd-server. [#2852](https://github.com/tikv/pd/issues/2852) [#3011](https://github.com/tikv/pd/pull/3011)
+ For the TiFlash side, set the `security.redact_info_log = true` configuration in tiflash-server and set `security.redact-info-log = true` in tiflash-learner.

[User document](/log-redaction.md)

Related issue: [#18566](https://github.com/pingcap/tidb/issues/18566)

## Performance improvements

### Support async commit (experimental)

Enabling the async commit feature can significantly reduce the latency of transactions. For example, with this feature enabled, the latency of transactions in the Sysbench oltp-insert test is 37.3% lower than that when this feature is disabled.

Previously without the async commit feature, the statements being written were only returned to the client after the two-phase transaction commit finished. Now the async commit feature supports returning the result to the client after the first phase of the two-phase commit finishes. The second phase is then performed asynchronously in the background, thus reducing the latency of transaction commit.

However, when async commit is enabled, the external consistency of transactions can be guaranteed **only** when `tidb_guarantee_external_consistency = ON` is set. With async commit enabled, the performance might drop.

Users can enable this feature by setting the global variable `tidb_enable_async_commit = ON`.

+ [User document](/system-variables.md#tidb_enable_async_commit-new-in-v50)
+ Related issue: [#8316](https://github.com/tikv/tikv/issues/8316)

### Improve the optimizer's stability in index selection (experimental)

The optimizer's ability to always select a relatively suitable index greatly determines whether the latency of queries is stable. We have improved and refactored the statistics module to ensure that, for the same SQL statements, the optimizer does not select a different index from multiple candidate indexes each time due to missing or inaccurate statistics. The main improvements to help the optimizer select a relatively suitable index are as follows:

+ Add more information to the statistics module, such as the multi-column NDV, the multi-column order dependency, and the multi-column function dependency.
+ Refactor the statistics module.
    + Delete `TopN` values from `CMSKetch`.
    + Refactor the search logic of `TopN`.
    + Delete the `TopN` information from the histogram and create an index of the histogram for easy maintenance of Bucket NDV.

Related issue: [#18065](https://github.com/pingcap/tidb/issues/18065)

### Optimize performance jitter caused by imperfect scheduling or imperfect I/O flow control

The TiDB scheduling process occupies resources such as I/O, network, CPU, and memory. If TiDB does not control the scheduled tasks, QPS and delay might cause performance jitter due to resource preemption. After the following optimizations, in the 72-hour test, the standard deviation of Sysbench TPS jitter is reduced from 11.09% to 3.36%.

+ Reduce the redundant scheduling issues caused by fluctuations of node capacity (always near the waterline) and caused by PD's `store-limit` configuration value set too large. This is achieved by introducing a new set of scheduling calculation formulas enabled via the `region-score-formula-version = v2` configuration item. [#3269](https://github.com/tikv/pd/pull/3269)
+ Enable the cross-Region merge feature by modifying `enable-cross-table-merge = true` to reduce the number of empty Regions. [#3129](https://github.com/tikv/pd/pull/3129)
+ Data compaction in the TiKV background occupies a lot of I/O resources. The system automatically adjusts the compaction rate to balance the contention for I/O resources between background tasks and foreground reads and writes. After enabling this feature via the `rate-limiter-auto-tuned` configuration item, the delay jitter is greatly reduced. [#18011](https://github.com/pingcap/tidb/issues/18011)
+ When TiKV performs garbage collection (GC) and data compaction, partitions occupy CPU and I/O resources. Overlapping data exists during the execution of these two tasks. To reduce I/O usage, the GC Compaction Filter feature combines these two tasks into one and executes them in the same task. This feature is still experimental and you can enable it via `gc.enable-compaction-filter = true`. [#18009](https://github.com/pingcap/tidb/issues/18009)
+ When TiFlash compresses or sorts data, it occupies a lot of I/O resources. The system alleviates contention for resources by limiting the compression and data sorting's use of I/O resources. This feature is still experimental and you can enable it via `bg_task_io_rate_limit`.

Related issue: [#18005](https://github.com/pingcap/tidb/issues/18005)

### Improve the stability of TiFlash in Real-time BI / Data Warehousing scenarios

+ Limit the memory usage of DeltaIndex to avoid system out of memory (OOM) caused by excessive memory usage in the scenarios of huge data volume.
+ Limit the I/O write traffic used by the background data sorting task to reduce the impact on the foreground tasks.
+ Add new thread pools to queue coprocessor tasks, which avoids system OOM caused by excessive memory usage when processing coprocessors in high concurrency.

### Other performance optimizations

+ Improve the execution performance of `delete from table where id <?` statement. Its P99 performance improves by four times. [#18028](https://github.com/pingcap/tidb/issues/18028)
+ TiFlash supports concurrently reading and writing data in multiple local disks to improve performance.

## High availability and disaster recovery

### Improve system availability during Region membership change (experimental)

In the process of Region membership changes, "adding a member" and "deleting a member" are two operations performed in two steps. If a failure occurs when the membership change finishes, the Regions will become unavailable and an error of foreground application is returned. The introduced Raft Joint Consensus algorithm can improve the system availability during Region membership change. "adding a member" and "deleting a member" operations during the membership change are combined into one operation and sent to all members. During the change process, Regions are in an intermediate state. If any modified member fails, the system is still available. Users can enable this feature by modifying the membership variable by executing `pd-ctl config set enable-joint-consensus true`. [#7587](https://github.com/tikv/tikv/issues/7587) [#2860](https://github.com/tikv/pd/issues/2860)

+ [User document](/pd-configuration-file.md#enable-joint-consensus-new-in-v50)
+ Related issue: [#18079](https://github.com/pingcap/tidb/issues/18079)

### Optimize the memory management module to reduce system OOM risks

+ Reduce the memory consumption of caching statistics.
+ Reduce the memory consumption of exporting data using the Dumpling tool.
+ Reduced the memory consumption by storing the encrypted intermediate results of data to the disk.

## Backup and restore

+ The Backup & Restore tool (BR) supports backing up data to AWS S3 and Google Cloud GCS. ([User document](/br/backup-and-restore-storages.md))
+ The Backup & Restore tool (BR) supports restoring data from AWS S3 and Google Cloud GCS to TiDB. ([User document](/br/backup-and-restore-storages.md))
+ Related issue: [#89](https://github.com/pingcap/br/issues/89)

## Data import and export

+ TiDB Lightning supports importing Aurora snapshot data from AWS S3 storage to TiDB. (Related issue: [#266](https://github.com/pingcap/tidb-lightning/issues/266))
+ In the TPC-C test of importing 1 TiB of data into DBaaS T1.standard, the performance improves by 40%, from 254 GiB/h to 366 GiB/h.
+ Dumpling supports exporting data from TiDB/MySQL to AWS S3 storage (experimental) (Related issue: [#8](https://github.com/pingcap/dumpling/issues/8), [User document](/dumpling-overview.md#export-data-to-amazon-s3-cloud-storage))

## Diagnostics

### Optimized `EXPLAIN` features with more collected information help users troubleshoot performance issues

When users troubleshoot SQL performance issues, they need detailed diagnostic information to determine the causes of performance issues. In previous TiDB versions, the information collected by the `EXPLAIN` statements was not detailed enough. DBAs performed troubleshooting only based on log information, monitoring information, or even on guess, which might be inefficient. The following improvements are made in TiDB v5.0 to help users troubleshoot performance issues more efficiently:

+ `EXPLAIN ANALYZE` supports analyzing all DML statements and shows the actual performance plans and the execution information of each operator. [#18056](https://github.com/pingcap/tidb/issues/18056)
+ Users can use `EXPLAIN FOR CONNECTION` to analyze the status information of the SQL statements that are being executed. This information includes the execution duration of each operator and the number of processed rows. [#18233](https://github.com/pingcap/tidb/issues/18233)
+ More information is available in the output of `EXPLAIN ANALYZE`, including the number of RPC requests sent by operators, the duration of resolving lock conflicts, network latency, the scanned volume of deleted data in RocksDB, and the hit rate of RocksDB caches. [#18663](https://github.com/pingcap/tidb/issues/18663)
+ The detailed execution information of SQL statements is recorded in the slow log, which is consistent with the output information of `EXPLAIN ANALYZE`. This information includes the time consumed by each operator, the number of processed rows, and the number of sent RPC requests. [#15009](https://github.com/pingcap/tidb/issues/15009)

[User document](/sql-statements/sql-statement-explain.md)

## Deployment and maintenance

+ Previously, when the configuration information of TiDB Ansible was imported to TiUP, TiUP put the user configuration in the `ansible-imported-configs` directory. When users later needed to edit the configuration using `tiup cluster edit-config`, the imported configuration was not displayed in the editor interface, which could be confusing for users. In TiDB v5.0, when TiDB Ansible configuration is imported, TiUP puts the configuration information both in `ansible-imported-configs` and in the editor interface. With this improvement, users can see the imported configuration when they are editing the cluster configuration.
+ Enhanced `mirror` command that supports merging multiple mirrors into one, publishing components in the local mirror, and adding component owners in the local mirror. [#814](https://github.com/pingcap/tiup/issues/814)
    + For a large enterprise, especially for the financial industry, any change in the production environment is given careful consideration. It can be troublesome if each version requires users to use a CD for installation. In TiDB v5.0, the `merge` command of TiUP supports merging multiple installation packages into one, which makes the installation easier.
    + In v4.0, users had to start tiup-server to publish the self-built mirror, which was not convenient enough. In v5.0, users can publish the self-built mirror simply by using `tiup mirror set` to set the current mirror to the local mirror.
