---
title: TiDB 5.2.2 Release Notes
---

# TiDB 5.2.2 Release Notes

Release Date: October 29, 2021

TiDB version: 5.2.2

## Improvements

+ TiDB

    - Show the affected SQL statements in the debug log when the coprocessor encounters a lock, which is helpful in diagnosing problems [#27718](https://github.com/pingcap/tidb/issues/27718)
    - Support showing the size of the backup and restore data when backing up and restoring data in the SQL logical layer [#27247](https://github.com/pingcap/tidb/issues/27247)

+ TiKV

    - Simplify the algorithm of L0 flow control [#10879](https://github.com/tikv/tikv/issues/10879)
    - Improve the error log report in the raft client module [#10983](https://github.com/tikv/tikv/pull/10983)
    - Improve logging threads to avoid them becoming a performance bottleneck [#10841](https://github.com/tikv/tikv/issues/10841)
    - Add more statistics types of write queries [#10507](https://github.com/tikv/tikv/issues/10507)

+ PD

    - Add more types of write queries to QPS dimensions in the hotspot scheduler [#3869](https://github.com/tikv/pd/issues/3869)
    - Support dynamically adjusting the retry limit of the balance region scheduler to improve the performance of the scheduler [#3744](https://github.com/tikv/pd/issues/3744)
    - Update TiDB Dashboard to v2021.10.08.1 [#4070](https://github.com/tikv/pd/pull/4070)
    - Support that the evict leader scheduler can schedule regions with unhealthy peers [#4093](https://github.com/tikv/pd/issues/4093) 
    - Speed up the exit process of schedulers [#4146](https://github.com/tikv/pd/issues/4146)

+ Tools

    + TiCDC 

        - Reduce the default value of the Kafka sink configuration item `MaxMessageBytes` from 64 MB to 1 MB to fix the issue that large messages are rejected by the Kafka Broker [#3104](https://github.com/pingcap/ticdc/pull/3104)
        - Reduce memory usage in the relpication pipeline [#2553](https://github.com/pingcap/ticdc/issues/2553)[#3037](https://github.com/pingcap/ticdc/pull/3037) [#2726](https://github.com/pingcap/ticdc/pull/2726)
        - Optimize monitoring items and alert rules to improve observability of synchronous links, memory GC, and stock data scanning processes [#2735](https://github.com/pingcap/ticdc/pull/2735) [#1606](https://github.com/pingcap/ticdc/issues/1606) [#3000](https://github.com/pingcap/ticdc/pull/3000) [#2985](https://github.com/pingcap/ticdc/issues/2985) [#2156](https://github.com/pingcap/ticdc/issues/2156) 
        - When the sync task status is normal, no more historical error messages are displayed to avoid misleading users [#2242](https://github.com/pingcap/ticdc/issues/2242) 
    
## Bug Fixes

+ TiDB

    - Fix the issue that plan-cache cannot detect changes of unsigned flags [#28254](https://github.com/pingcap/tidb/issues/28254)
    - Fix the wrong partition pruning when the partition function is out of range [#28233](https://github.com/pingcap/tidb/issues/28233)
    - Fix the issue that planner might cache invalid plans for `join` in some cases [#28087](https://github.com/pingcap/tidb/issues/28087)
    - Fix wrong index hash join when hash column type is enum [#27893](https://github.com/pingcap/tidb/issues/27893)
    - Fix a batch client bug that recycling idle connection might block sending requests in some rare cases [#27688](https://github.com/pingcap/tidb/pull/27688)
    - Fix the TiDB Lightning panic issue when it fails to perform checksum on a target cluster [#27686](https://github.com/pingcap/tidb/pull/27686)
    - Fix wrong results of the `date_add` and `date_sub` functions in some cases [#27232](https://github.com/pingcap/tidb/issues/27232)
    - Fix wrong results of the `hour` function in vectorized expression [#28643](https://github.com/pingcap/tidb/issues/28643)
    - Fix the authenticating issue when connecting to MySQL 5.1 or an older client version  [#27855](https://github.com/pingcap/tidb/issues/27855)
    - Fix the issue that auto analyze might be triggered out of the specified time when a new index is added [#28698](https://github.com/pingcap/tidb/issues/28698)
    - Fix a bug that setting any session variable invalidates `tidb_snapshot` [#28683](https://github.com/pingcap/tidb/pull/28683)
    - Fix a bug that BR is not working for clusters with many missing-peer regions [#27534](https://github.com/pingcap/tidb/issues/27534)
    - Fix  the unexpected error like `tidb_cast to Int32 is not supported` when the unsupported `cast` is pushed down to TiFlash [#23907](https://github.com/pingcap/tidb/issues/23907)
    - Fix the issue that `DECIMAL overflow` is missing in the `%s value is out of range in '%s'`error message  [#27964](https://github.com/pingcap/tidb/issues/27964)
    - Fix a bug that the availability detection of MPP node does not work in some corner cases [#3118](https://github.com/pingcap/tics/issues/3118)
    - Fix the `DATA RACE` issue when assigning `MPP task ID` [#27952](https://github.com/pingcap/tidb/issues/27952)
    - Fix the `INDEX OUT OF RANGE` error for a MPP query after deleting an empty `dual table`. [#28250](https://github.com/pingcap/tidb/issues/28250)
    - Fix the issue of false positive error log `invalid cop task execution summaries length` for MPP queries [#1791](https://github.com/pingcap/tics/issues/1791)
    - Fix the issue of error log `cannot found column in Schema column` for MPP queries [#28149](https://github.com/pingcap/tidb/pull/28149)
    - Fix the issue that TiDB might panic when TiFlash is shuting down [#28096](https://github.com/pingcap/tidb/issues/28096)
    - Remove the support for insecure 3DES (Triple Data Encryption Algorithm) based TLS cipher suites [#27859](https://github.com/pingcap/tidb/pull/27859)
    - Fix the issue that Lightning connects to offline TiKV nodes during pre-check and causes import failures [#27826](https://github.com/pingcap/tidb/pull/27826)
    - Fix the issue that pre-check cost too much time when importing many files to tables [#27605](https://github.com/pingcap/tidb/issues/27605)
    - Fix the issue that rewriting expressions makes `between` infer wrong collation [#27146](https://github.com/pingcap/tidb/issues/27146)
    - Fix the issue that `group_concat` function did not consider the collation [#27429](https://github.com/pingcap/tidb/issues/27429)
    - Fix the result wrong that occurs when the argument of the `extract` function is a negative duration [#27236](https://github.com/pingcap/tidb/issues/27236)
    - Fix the issue that creating partition fails if `NO_UNSIGNED_SUBTRACTION` is set [#26765](https://github.com/pingcap/tidb/issues/26765)
    - Avoid expressions with side effects in column pruning and aggregation pushdown [#27106](https://github.com/pingcap/tidb/issues/27106)
    - Remove useless gRPC logs [#24190](https://github.com/pingcap/tidb/issues/24190)
    - Limit the valid decimal length to fix precision-related issues [#3091](https://github.com/pingcap/tics/issues/3091)
    - Fix the issue of a wrong way to check for overflow in `plus` expression [#26977](https://github.com/pingcap/tidb/issues/26977)
    - Fix the issue of `data too long` error when dumping statistics from the table with `new collation` data [#27024](https://github.com/pingcap/tidb/issues/27024)
    - Fix the issue that the retried transactions' statements are not included in `TIDB_TRX` [#28670](https://github.com/pingcap/tidb/pull/28670)

+ TiKV

    - Fix the issue that CDC adds scan retries frequently due to the Congest error [#11082](https://github.com/tikv/tikv/issues/11082)
    - Fix the issue that the raft connection is broken when the channel is full [#11047](https://github.com/tikv/tikv/issues/11047)
    - Fix the issue that batch messages are too large in Raft client implementation [#9714](https://github.com/tikv/tikv/issues/9714)
    - Fix the issue that some coroutines leak in `resolved_ts` [#10965](https://github.com/tikv/tikv/issues/10965)
    - Fix a panic issue that occurs to the coprocessor when the size of response exceeds 4 GiB [#9012](https://github.com/tikv/tikv/issues/9012)
    - Fix the issue that snapshot Garbage Collection (GC) misses GC snapshot files when snapshot files cannot be garbage collected [#10813](https://github.com/tikv/tikv/issues/10813)
    - Fix a panic issue caused by timeout when processing Coprocessor requests [#10852](https://github.com/tikv/tikv/issues/10852)

+ PD

    - Fix the issue that PD incorrectly delete the peers with data and in pending status because the number of peers exceeds the number of configured peers [#4045](https://github.com/tikv/pd/issues/4045)
    - Fix the issue that PD does not fix down peers in time [#4077](https://github.com/tikv/pd/issues/4077)
    - Fix the issue that the scatter range scheduler cannot schedule empty regions [#4118](https://github.com/tikv/pd/pull/4118)
    - Fix the issue that the key manager cost too much CPU [#4071](https://github.com/tikv/pd/issues/4071)
    - Fix the data race issue that might occur when setting configurations of hot region scheduler [#4159](https://github.com/tikv/pd/issues/4159)
    - Fix slow leader election caused by stucked region syncer[#3936](https://github.com/tikv/pd/issues/3936)

+ TiFlash

    - Fix the issue that TiFlash fails to start up on some platforms due to the absence of library `nsl`

+ Tools

    + TiCDC
        - Fix the issue that TiCDC replication task might terminate when the upstream TiDB instance unexpectedly exits [#3061](https://github.com/pingcap/ticdc/issues/3061)
        - Fix the issue that TiCDC process might panic when TiKV sends duplicate requests to the same Region [#2386](https://github.com/pingcap/ticdc/issues/2386)
        - Fix unnecessary CPU consumption when verifying downstream TiDB/MySQL availability [#3073](https://github.com/pingcap/ticdc/issues/3073)
        - Fix the issue that the volume of Kafka messages generated by TiCDC is not constrained by `max-message-size` [#2962](https://github.com/pingcap/ticdc/issues/2962)
        - Fix the issue that TiCDC sync task might pause when an error occurs during writing a Kafka message [#2978](https://github.com/pingcap/ticdc/issues/2978)
        - Fix the issue that some partitioned tables without valid indexes might be ignored when `force-replicate` is enabled [#2834](https://github.com/pingcap/ticdc/issues/2834)
        - Fix the issue that scanning stock data might fail due to TiKV performing GC when scanning stock data takes too long [#2470](https://github.com/pingcap/ticdc/issues/2470)
        - Fix a possible panic issue when encoding some types of columns into Open Protocol format [#2758](https://github.com/pingcap/ticdc/issues/2758)
        - Fix a possible panic issue when encoding some types of columns into Avro format [#2648](https://github.com/pingcap/ticdc/issues/2648)

    + TiDB Binlog

        - Fix the issue that when most tables are filtered out, checkpoint can not be updated under some special load [#1075](https://github.com/pingcap/tidb-binlog/pull/1075)
