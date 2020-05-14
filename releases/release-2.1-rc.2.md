---
title: TiDB 2.1 RC2 Release Notes
category: Releases
---

# TiDB 2.1 RC2 Release Notes

On September 14, 2018, TiDB 2.1 RC2 is released. Compared with TiDB 2.1 RC1, this release has great improvement in stability, SQL optimizer, statistics information, and execution engine.

## TiDB

* SQL Optimizer
    * Put forward a proposal of the next generation Planner [#7543](https://github.com/pingcap/tidb/pull/7543)
    * Improve the optimization rules of constant propagation [#7276](https://github.com/pingcap/tidb/pull/7276)
    * Enhance the computing logic of `Range` to enable it to handle multiple `IN` or `EQUAL` conditions simultaneously [#7577](https://github.com/pingcap/tidb/pull/7577)
    * Fix the issue that the estimation result of `TableScan` is incorrect when `Range` is empty [#7583](https://github.com/pingcap/tidb/pull/7583)
    * Support the `PointGet` operator for the `UPDATE` statement [#7586](https://github.com/pingcap/tidb/pull/7586)
    * Fix the panic issue during the process of executing the `FirstRow` aggregate function in some conditions [#7624](https://github.com/pingcap/tidb/pull/7624)
* SQL Execution Engine
    * Fix the potential `DataRace` issue when the `HashJoin` operator encounters an error [#7554](https://github.com/pingcap/tidb/pull/7554)
    * Make the `HashJoin` operator read the inner table and build the hash table simultaneously [#7544](https://github.com/pingcap/tidb/pull/7544)
    * Optimize the performance of Hash aggregate operators [#7541](https://github.com/pingcap/tidb/pull/7541)
    * Optimize the performance of Join operators [#7493](https://github.com/pingcap/tidb/pull/7493), [#7433](https://github.com/pingcap/tidb/pull/7433)
    * Fix the issue that the result of `UPDATE JOIN` is incorrect when the Join order is changed [#7571](https://github.com/pingcap/tidb/pull/7571)
    * Improve the performance of Chunk’s iterator [#7585](https://github.com/pingcap/tidb/pull/7585)
* Statistics
    * Fix the issue that the auto Analyze work repeatedly analyzes the statistics [#7550](https://github.com/pingcap/tidb/pull/7550)
    * Fix the statistics update error that occurs when there is no statistics change [#7530](https://github.com/pingcap/tidb/pull/7530)
    * Use the RC isolation level and low priority when building `Analyze` requests [#7496](https://github.com/pingcap/tidb/pull/7496)
    * Support enabling statistics auto-analyze on certain period of a day [#7570](https://github.com/pingcap/tidb/pull/7570)
    * Fix the panic issue when logging the statistics information [#7588](https://github.com/pingcap/tidb/pull/7588)
    * Support configuring the number of buckets in the histogram using the `ANALYZE TABLE WITH BUCKETS` statement [#7619](https://github.com/pingcap/tidb/pull/7619)
    * Fix the panic issue when updating an empty histogram [#7640](https://github.com/pingcap/tidb/pull/7640)
    * Update `information_schema.tables.data_length` using the statistics information [#7657](https://github.com/pingcap/tidb/pull/7657)
* Server
    * Add Trace related dependencies [#7532](https://github.com/pingcap/tidb/pull/7532)
    * Enable the `mutex profile` feature of Golang  [#7512](https://github.com/pingcap/tidb/pull/7512)
    * The `Admin` statement requires the `Super_priv` privilege [#7486](https://github.com/pingcap/tidb/pull/7486)
    * Forbid users to `Drop` crucial system tables [#7471](https://github.com/pingcap/tidb/pull/7471)
    * Switch from `juju/errors` to `pkg/errors` [#7151](https://github.com/pingcap/tidb/pull/7151)
    * Complete the functional prototype of SQL Tracing [#7016](https://github.com/pingcap/tidb/pull/7016)
    * Remove the goroutine pool [#7564](https://github.com/pingcap/tidb/pull/7564)
    * Support viewing the goroutine information using the `USER1` signal [#7587](https://github.com/pingcap/tidb/pull/7587)
    * Set the internal SQL to high priority while TiDB is started [#7616](https://github.com/pingcap/tidb/pull/7616)
    * Use different labels to filter internal SQL and user SQL in monitoring metrics [#7631](https://github.com/pingcap/tidb/pull/7631)
    * Store the top 30 slow queries in the last week to the TiDB server [#7646](https://github.com/pingcap/tidb/pull/7646)
    * Put forward a proposal of setting the global system time zone for the TiDB cluster [#7656](https://github.com/pingcap/tidb/pull/7656)
    * Enrich the error message of “GC life time is shorter than transaction duration” [#7658](https://github.com/pingcap/tidb/pull/7658)
    * Set the global system time zone when starting the TiDB cluster [#7638](https://github.com/pingcap/tidb/pull/7638)
* Compatibility
    * Add the unsigned flag for the `Year` type [#7542](https://github.com/pingcap/tidb/pull/7542)
    * Fix the issue of configuring the result length of the `Year` type in the `Prepare`/`Execute` mode [#7525](https://github.com/pingcap/tidb/pull/7525)
    * Fix the issue of inserting zero timestamp in the `Prepare`/`Execute` mode [#7506](https://github.com/pingcap/tidb/pull/7506)
    * Fix the error handling issue of the integer division [#7492](https://github.com/pingcap/tidb/pull/7492)
    * Fix the compatibility issue when processing `ComStmtSendLongData` [#7485](https://github.com/pingcap/tidb/pull/7485)
    * Fix the error handling issue during the process of converting string to integer [#7483](https://github.com/pingcap/tidb/pull/7483)
    * Optimize the accuracy of values in the `information_schema.columns_in_table` table [#7463](https://github.com/pingcap/tidb/pull/7463)
    * Fix the compatibility issue when writing or updating the string type of data using the MariaDB client [#7573](https://github.com/pingcap/tidb/pull/7573)
    * Fix the compatibility issue of aliases of the returned value [#7600](https://github.com/pingcap/tidb/pull/7600)
    * Fix the issue that the `NUMERIC_SCALE` value of the float type is incorrect in the `information_schema.COLUMNS` table [#7602](https://github.com/pingcap/tidb/pull/7602)
    * Fix the issue that Parser reports an error when the single line comment is empty [#7612](https://github.com/pingcap/tidb/pull/7612)
* Expressions
    * Check the value of `max_allowed_packet` in the `insert` function [#7528](https://github.com/pingcap/tidb/pull/7528)
    * Support the built-in function `json_contains`  [#7443](https://github.com/pingcap/tidb/pull/7443)
    * Support the built-in function `json_contains_path` [#7596](https://github.com/pingcap/tidb/pull/7596)
    * Support the built-in function `encode/decode` [#7622](https://github.com/pingcap/tidb/pull/7622)
    * Fix the issue that some time related functions are not compatible with the MySQL behaviors in some cases [#7636](https://github.com/pingcap/tidb/pull/7636)
    * Fix the compatibility issue of parsing the time type of data in string [#7654](https://github.com/pingcap/tidb/pull/7654)
    * Fix the issue that the time zone is not considered when computing the default value of the `DateTime` data [#7655](https://github.com/pingcap/tidb/pull/7655)
* DML
    * Set correct `last_insert_id` in the `InsertOnDuplicateUpdate` statement [#7534](https://github.com/pingcap/tidb/pull/7534)
    * Reduce the cases of updating the `auto_increment_id` counter [#7515](https://github.com/pingcap/tidb/pull/7515)
    * Optimize the error message of `Duplicate Key` [#7495](https://github.com/pingcap/tidb/pull/7495)
    * Fix the `insert...select...on duplicate key update` issue [#7406](https://github.com/pingcap/tidb/pull/7406)
    * Support the `LOAD DATA IGNORE LINES` statement [#7576](https://github.com/pingcap/tidb/pull/7576)
* DDL
    * Add the DDL job type and the current schema version information in the monitor [#7472](https://github.com/pingcap/tidb/pull/7472)
    * Complete the design of the `Admin Restore Table` feature [#7383](https://github.com/pingcap/tidb/pull/7383)
    * Fix the issue that the default value of the `Bit` type exceeds 128 [#7249](https://github.com/pingcap/tidb/pull/7249)
    * Fix the issue that the default value of the `Bit` type cannot be `NULL` [#7604](https://github.com/pingcap/tidb/pull/7604)
    * Reduce the interval of checking `CREATE TABLE/DATABASE` in the DDL queue [#7608](https://github.com/pingcap/tidb/pull/7608)
    * Use the `ddl/owner/resign` HTTP interface ro release the DDL owner and start electing a new owner [#7649](https://github.com/pingcap/tidb/pull/7649)
* TiKV Go Client
    * Support the issue that the `Seek` operation only obtains `Key` [#7419](https://github.com/pingcap/tidb/pull/7419)
* [Table Partition](https://github.com/pingcap/tidb/projects/6) (Experimental)
    * Fix the issue that the `Bigint` type cannot be used as the partition key  [#7520](https://github.com/pingcap/tidb/pull/7520)
    * Support the rollback operation when an issue occurs during adding an index in the partitioned table [#7437](https://github.com/pingcap/tidb/pull/7437)

## PD

* Features
    * Support the `GetAllStores` interface [#1228](https://github.com/pingcap/pd/pull/1228)
    * Add the statistics of scheduling estimation in Simulator [#1218](https://github.com/pingcap/pd/pull/1218)
* Improvements
    * Optimize the handling process of down stores to make up replicas as soon as possible [#1222](https://github.com/pingcap/pd/pull/1222)
    * Optimize the start of Coordinator to reduce the unnecessary scheduling caused by restarting PD [#1225](https://github.com/pingcap/pd/pull/1225)
    * Optimize the memory usage to reduce the overhead caused by heartbeats [#1195](https://github.com/pingcap/pd/pull/1195)
    * Optimize error handling and improve the log information [#1227](https://github.com/pingcap/pd/pull/1227)
    * Support querying the Region information of a specific store in pd-ctl [#1231](https://github.com/pingcap/pd/pull/1231)
    * Support querying the topN Region information based on version comparison in pd-ctl [#1233](https://github.com/pingcap/pd/pull/1233)
    * Support more accurate TSO decoding in pd-ctl [#1242](https://github.com/pingcap/pd/pull/1242)
* Bug fix
    * Fix the issue that pd-ctl uses the `hot store` command to exit wrongly [#1244](https://github.com/pingcap/pd/pull/1244)

## TiKV

* Performance
    * Support splitting Regions based on statistics estimation to reduce the I/O cost [#3511](https://github.com/tikv/tikv/pull/3511)
    * Reduce clone in the transaction scheduler [#3530](https://github.com/tikv/tikv/pull/3530)
* Improvements
    * Add the pushdown support for a large number of built-in functions
    * Add the `leader-transfer-max-log-lag` configuration to fix the failure issue of leader scheduling in specific scenarios [#3507](https://github.com/tikv/tikv/pull/3507)
    * Add the `max-open-engines` configuration to limit the number of engines opened by `tikv-importer` simultaneously [#3496](https://github.com/tikv/tikv/pull/3496)
    * Limit the cleanup speed of garbage data to reduce the impact on `snapshot apply` [#3547](https://github.com/tikv/tikv/pull/3547)
    * Broadcast the commit message for crucial Raft messages to avoid unnecessary delay [#3592](https://github.com/tikv/tikv/pull/3592)
* Bug fixes
    * Fix the leader election issue caused by discarding the `PreVote` message of the newly split Region [#3557](https://github.com/tikv/tikv/pull/3557)
    * Fix follower related statistics after merging Regions [#3573](https://github.com/tikv/tikv/pull/3573)
    * Fix the issue that the local reader uses obsolete Region information [#3565](https://github.com/tikv/tikv/pull/3565)
