---
title: TiDB 3.0.5 Release Notes
category: Releases
---

# TiDB 3.0.5 Release Notes

Release date: October 25, 2019

TiDB version: 3.0.5

TiDB Ansible version: 3.0.5

## TiDB

+ SQL Optimizer
    - Support boundary checking on Window Functions [#12404](https://github.com/pingcap/tidb/pull/12404)
    - Fix the issue that `IndexJoin` on the partition table returns incorrect results [#12712](https://github.com/pingcap/tidb/pull/12712)
    - Fix the issue that the `ifnull` function on the top of the outer join `Apply` operator returns incorrect results [#12694](https://github.com/pingcap/tidb/pull/12694)
    - Fix the issue of update failure when a subquery was included in the `where` condition of `UPDATE` [#12597](https://github.com/pingcap/tidb/pull/12597)
    - Fix the issue that outer join was incorrectly converted to inner join when the `cast` function was included in the query conditions [#12790](https://github.com/pingcap/tidb/pull/12790)
    - Fix incorrect expression passing in the join condition of `AntiSemiJoin` [#12799](https://github.com/pingcap/tidb/pull/12799)
    - Fix the statistics error caused by shallow copy when initializing statistics [#12817](https://github.com/pingcap/tidb/pull/12817)
    - Fix the issue that the `str_to_date` function in TiDB returns a different result from MySQL when the date string and the format string do not match [#12725](https://github.com/pingcap/tidb/pull/12725)
+ SQL Execution Engine
    - Fix the panic issue when the `from_unixtime` function handles null [#12551](https://github.com/pingcap/tidb/pull/12551)
    - Fix the `invalid list index` error reported when canceling DDL jobs [#12671](https://github.com/pingcap/tidb/pull/12671)
    - Fix the issue that arrays were out of bounds when Window Functions are used [#12660](https://github.com/pingcap/tidb/pull/12660)
    - Improve the behavior of the `AutoIncrement` column when it is implicitly allocated, to keep it consistent with the default mode of MySQL auto-increment locking (["consecutive" lock mode](https://dev.mysql.com/doc/refman/5.7/en/innodb-auto-increment-handling.html)): for the implicit allocation of multiple `AutoIncrement` IDs in a single-line `Insert` statement, TiDB guarantees the continuity of the allocated values. This improvement ensures that the JDBC `getGeneratedKeys()` method will get the correct results in any scenario. [#12602](https://github.com/pingcap/tidb/pull/12602)
    - Fix the issue that the query is hanged when `HashAgg` serves as a child node of `Apply` [#12766](https://github.com/pingcap/tidb/pull/12766)
    - Fix the issue that the `AND` and `OR` logical expressions return incorrect results when it comes to type conversion [#12811](https://github.com/pingcap/tidb/pull/12811)
+ Server
    - Implement the interface function that modifies transaction TTL to help support large transactions later [#12397](https://github.com/pingcap/tidb/pull/12397)
    - Support extending the transaction TTL as needed (up to 10 minutes) to support pessimistic transactions [#12579](https://github.com/pingcap/tidb/pull/12579)
    - Adjust the number of times that TiDB caches schema changes and corresponding changed table information from 100 to 1024, and support modification by using the `tidb_max_delta_schema_count` system variable [#12502](https://github.com/pingcap/tidb/pull/12502)
    - Update the behavior of the `kvrpc.Cleanup` protocol to no longer clean locks of transactions that are not overtime [#12417](https://github.com/pingcap/tidb/pull/12417)
    - Support logging Partition table information to the `information_schema.tables` table [#12631](https://github.com/pingcap/tidb/pull/12631)
    - Support modifying the TTL of Region Cache by configuring `region-cache-ttl` [#12683](https://github.com/pingcap/tidb/pull/12683)
    - Support printing the execution plan compression-encoded information in the slow log. This feature is enabled by default and can be controlled by using the `slow-log-plan` configuration or the `tidb_record_plan_in_slow_log` variable. In addition, the `tidb_decode_plan` function can decode the execution plan column encoded information in the slow log into execution plan information. [#12808](https://github.com/pingcap/tidb/pull/12808)
    - Support displaying memory usage information in the `information_schema.processlist` table [#12801](https://github.com/pingcap/tidb/pull/12801)
    - Fix the issue that an error and an unexpected alarm might occur when the TiKV Client judges an idle connection [#12846](https://github.com/pingcap/tidb/pull/12846)
    - Fix the issue that the `INSERT IGNORE` statement performance is decreased because `tikvSnapshot` does not properly cache the KV results of `BatchGet()` [#12872](https://github.com/pingcap/tidb/pull/12872)
    - Fix the issue that the TiDB response speed was relatively low because of slow connection to some KV services [#12814](https://github.com/pingcap/tidb/pull/12814)
+ DDL
    - Fix the issue that the `Create Table` operation does not correctly set the Int type default value for the Set column [#12267](https://github.com/pingcap/tidb/pull/12267)
    - Support multiple `unique`s when creating a unique index in the `Create Table` statement [#12463](https://github.com/pingcap/tidb/pull/12463)
    - Fix the issue that populating the default value of this column for existing rows might cause an error when adding a Bit type column using `Alter Table` [#12489](https://github.com/pingcap/tidb/pull/12489)
    - Fix the failure of adding a partition when the Range partitioned table uses a Date or Datetime type column as the partitioning key [#12815](https://github.com/pingcap/tidb/pull/12815)
    - Support checking the consistency of the partition type and the partition key type when creating a table or adding a partition, for the Range partitioned table with the Date or Datetime type column as the partition key [#12792](https://github.com/pingcap/tidb/pull/12792)
    - Add a check that the Unique Key column set needs to be greater than or equal to the partitioned column set when creating a Range partitioned table [#12718](https://github.com/pingcap/tidb/pull/12718)
+ Monitor
    - Add the monitoring metrics of Commit and Rollback operations to the `Transaction OPS` dashboard [#12505](https://github.com/pingcap/tidb/pull/12505)
    - Add the monitoring metrics of `Add Index` operation progress [#12390](https://github.com/pingcap/tidb/pull/12390)

## TiKV

+ Storage
    - Add a new feature of pessimistic transactions: the transaction cleanup interface supports only cleaning up locks whose TTL is outdated [#5589](https://github.com/tikv/tikv/pull/5589)
    - Fix the issue that Rollback of the transaction Primary key is collapsed [#5646](https://github.com/tikv/tikv/pull/5646), [#5671](https://github.com/tikv/tikv/pull/5671)
    - Fix the issue that under pessimistic locks, point queries might return the previous version data [#5634](https://github.com/tikv/tikv/pull/5634)
+ Raftstore
    - Reduce message flush operations in Raftstore to improve performance and reduce CPU usage [#5617](https://github.com/tikv/tikv/pull/5617)
    - Optimize the cost of obtaining the Region size and estimated number of keys, to reduce heartbeat overhead and CPU usage [#5620](https://github.com/tikv/tikv/pull/5620)
    - Fix the issue that Raftstore prints an error log and encounters a panic when getting invalid data [#5643](https://github.com/tikv/tikv/pull/5643)
+ Engine
    - Enable RocksDB `force_consistency_checks` to improve data safety [#5662](https://github.com/tikv/tikv/pull/5662)
    - Fix the issue that concurrent flush operations in Titan might cause data loss [#5672](https://github.com/tikv/tikv/pull/5672)
    - Update the rust-rocksdb version to avoid the issue of TiKV crash and restart caused by intra-L0 compaction [#5710](https://github.com/tikv/tikv/pull/5710)

## PD

- Improve the precision of storage occupied by Regions [#1782](https://github.com/pingcap/pd/pull/1782)
- Improve the output of the `--help` command [#1763](https://github.com/pingcap/pd/pull/1763)
- Fix the issue that the HTTP request fails to redirect after TLS is enabled [#1777](https://github.com/pingcap/pd/pull/1777)
- Fix the panic issue occurred when pd-ctl uses the `store shows limit` command [#1808](https://github.com/pingcap/pd/pull/1808)
- Improve readability of label monitoring metrics and reset the original leader's monitoring data when the leader switches, to avoid false reports [#1815](https://github.com/pingcap/pd/pull/1815)

## Tools

+ TiDB Binlog
    - Fix the issue that `ALTER DATABASE` related DDL operations cause Drainer to exit abnormally [#769](https://github.com/pingcap/tidb-binlog/pull/769)
    - Support querying the transaction status information for Commit binlog to improve replication efficiency [#757](https://github.com/pingcap/tidb-binlog/pull/757)
    - Fix the issue that a Pump panic might occur when Drainer's `start_ts` is greater than Pump's largest `commit_ts` [#758](https://github.com/pingcap/tidb-binlog/pull/758)
+ TiDB Lightning
    - Integrate the full logic import feature of Loader and support configuring the backend mode [#221](https://github.com/pingcap/tidb-lightning/pull/221)

## TiDB Ansible

- Add the monitoring metrics of adding index speed [#986](https://github.com/pingcap/tidb-ansible/pull/986)
- Simplify the configuration file content and remove parameters that users do not need to configure [#1043c](https://github.com/pingcap/tidb-ansible/commit/1043c3df7ddb72eb234c55858960e9fdd3830a14), [#998](https://github.com/pingcap/tidb-ansible/pull/998)
- Fix the monitoring expression error of performance read and performance write [#e90e7](https://github.com/pingcap/tidb-ansible/commit/e90e79f5117bb89197e01b1391fd02e25d57a440)
- Update the monitoring display method and the alarm rules of Raftstore CPU usage [#992](https://github.com/pingcap/tidb-ansible/pull/992)
- Update the TiKV CPU monitoring item in the Overview monitoring dashboard to filter out the excess monitoring content [#1001](https://github.com/pingcap/tidb-ansible/pull/1001)
