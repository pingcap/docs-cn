---
title: TiDB 4.0.9 Release Notes
---

# TiDB 4.0.9 Release Notes

Release date: December 21, 2020

TiDB version: 4.0.9

## Compatibility Changes

+ TiDB

    - Deprecate the `enable-streaming` configuration item [#21055](https://github.com/pingcap/tidb/pull/21055)

+ TiKV

    - Reduce I/O and mutex contention when encryption at rest is enabled. The change is backwardly incompatible. If users need to downgrade the cluster to a version earlier than v4.0.9, `security.encryption.enable-file-dictionary-log` must be disabled and TiKV must be restarted before the downgrade. [#9195](https://github.com/tikv/tikv/pull/9195)

## New Features

+ TiFlash

    - Support storing the latest data of the storage engine on multiple disks (experimental)

+ TiDB Dashboard

    - Support displaying and sorting by all fields in the **SQL Statements** page [#749](https://github.com/pingcap/tidb-dashboard/pull/749)
    - Support zooming and panning the topology graph [#772](https://github.com/pingcap/tidb-dashboard/pull/772)
    - Support displaying the disk usage information in the **SQL Statements** and **Slow Queries** pages [#777](https://github.com/pingcap/tidb-dashboard/pull/777)
    - Support exporting list data in the **SQL Statements** and **Slow Queries** pages [#778](https://github.com/pingcap/tidb-dashboard/pull/778)
    - Support customizing the Prometheus address [#808](https://github.com/pingcap/tidb-dashboard/pull/808)
    - Add a page for cluster statistics [#815](https://github.com/pingcap/tidb-dashboard/pull/815)
    - Add more time-related fields in the **Slow Queries** details [#810](https://github.com/pingcap/tidb-dashboard/pull/810)

## Improvements

+ TiDB

    - Avoid the (index) merge join in a heuristical way when converting equal conditions to other conditions [#21146](https://github.com/pingcap/tidb/pull/21146)
    - Differentiate the types of user variables [#21107](https://github.com/pingcap/tidb/pull/21107)
    - Support setting the `GOGC` variable in the configuration file [#20922](https://github.com/pingcap/tidb/pull/20922)
    - Make the dumped binary time (`Timestamp` and `Datetime`) more compatible with MySQL [#21135](https://github.com/pingcap/tidb/pull/21135)
    - Provide an error message for statements that use the `LOCK IN SHARE MODE` syntax [#21005](https://github.com/pingcap/tidb/pull/21005)
    - Avoid outputting unnecessary warnings or errors when folding constants in shortcut-able expressions [#21040](https://github.com/pingcap/tidb/pull/21040)
    - Raise an error when preparing the `LOAD DATA` statement [#21199](https://github.com/pingcap/tidb/pull/21199)
    - Ignore the attribute of the integer zero-fill size when changing the integer column types [#20986](https://github.com/pingcap/tidb/pull/20986)
    - Add the executor-related runtime information of DML statements in the result of `EXPLAIN ANALYZE` [#21066](https://github.com/pingcap/tidb/pull/21066)
    - Disallow multiple updates on the primary key in a singe SQL statements [#21113](https://github.com/pingcap/tidb/pull/21113)
    - Add a monitoring metric for the connection idle time [#21301](https://github.com/pingcap/tidb/pull/21301)
    - Temporarily enable the slow log when the `runtime/trace` tool is running [#20578](https://github.com/pingcap/tidb/pull/20578)

+ TiKV

    - Add the tag to trace the source of the `split` command [#8936](https://github.com/tikv/tikv/pull/8936)
    - Support dynamically changing the `pessimistic-txn.pipelined` configuration [#9100](https://github.com/tikv/tikv/pull/9100)
    - Reduce the impact on performance when running Backup & Restore and TiDB Lightning [#9098](https://github.com/tikv/tikv/pull/9098)
    - Add monitoring metrics for the ingesting SST errors [#9096](https://github.com/tikv/tikv/pull/9096)
    - Prevent the leader from being hibernated when some peers still need to replicate logs [#9093](https://github.com/tikv/tikv/pull/9093)
    - Increase the success rate of the pipelined pessimistic locking [#9086](https://github.com/tikv/tikv/pull/9086)
    - Change the default value of `apply-max-batch-size` and `store-max-batch-size` to `1024` [#9020](https://github.com/tikv/tikv/pull/9020)
    - Add the `max-background-flushes` configuration item [#8947](https://github.com/tikv/tikv/pull/8947)
    - Disable `force-consistency-checks` by default to improve performance [#9029](https://github.com/tikv/tikv/pull/9029)
    - Offload the queries on the Region size from `pd heartbeat worker` to `split check worker` [#9185](https://github.com/tikv/tikv/pull/9185)

+ PD

    - Check the TiKV cluster version when a TiKV stores become `Tombstone`, which prevents users from enabling incompatible features during the process of downgrade or upgrade [#3213](https://github.com/pingcap/pd/pull/3213)
    - Disallow the TiKV store of a lower version to change from `Tombstone` back to `Up` [#3206](https://github.com/pingcap/pd/pull/3206)

+ TiDB Dashboard

    - Keep expanding when "Expand" is clicked for SQL statements [#775](https://github.com/pingcap/tidb-dashboard/pull/775)
    - Open detail pages in new windows for **SQL Statements** and **Slow Queries** [#816](https://github.com/pingcap/tidb-dashboard/pull/816)
    - Improve descriptions for time-related fields in **Slow Queries** details [#817](https://github.com/pingcap/tidb-dashboard/pull/817)
    - Display detailed error messages [#794](https://github.com/pingcap/tidb-dashboard/pull/794)

+ TiFlash

    - Reduce the latency of replica reads
    - Refine TiFlash's error messages
    - Limit the memory usage of cache data when the data volume is huge
    - Add a monitoring metric for the number of coprocessor tasks being handled

+ Tools

    + Backup & Restore (BR)

        - Disallow the ambiguous `--checksum false` argument in the command line, which does not correctly disable checksum. Only `--checksum=false` is accepted. [#588](https://github.com/pingcap/br/pull/588)
        - Support changing the PD configuration temporarily so that PD can recover the original configuration after BR accidentally exists [#596](https://github.com/pingcap/br/pull/596)
        - Support analyzing tables after restore [#622](https://github.com/pingcap/br/pull/622)
        - Retry for the `read index not ready` and `proposal in merging mode` errors [#626](https://github.com/pingcap/br/pull/626)

    + TiCDC

        - Add an alert for enabling TiKV's Hibernate Region feature [#1120](https://github.com/pingcap/ticdc/pull/1120)
        - Reduce memory usage in the schema storage [#1127](https://github.com/pingcap/ticdc/pull/1127)
        - Add the feature of unified sorter, which accelerates replication when the data size of the incremental scan is large (experimental) [#1122](https://github.com/pingcap/ticdc/pull/1122)
        - Support configuring the maximum message size and the maximum message batch in the TiCDC Open Protocol message (only for Kafka sink) [#1079](https://github.com/pingcap/ticdc/pull/1079)

    + Dumpling

        - Retry dumping data on failed chunks [#182](https://github.com/pingcap/dumpling/pull/182)
        - Support configuring both the `-F` and `-r` arguments at the same time [#177](https://github.com/pingcap/dumpling/pull/177)
        - Exclude system databases in `--filter` by default [#194](https://github.com/pingcap/dumpling/pull/194)
        - Support the `--transactional-consistency` parameter and support rebuilding MySQL connections during retry [#199](https://github.com/pingcap/dumpling/pull/199)
        - Support using the `-c,--compress` parameter to specify the compression algorithm used by Dumpling. An empty string means no compression. [#202](https://github.com/pingcap/dumpling/pull/202)

    + TiDB Lightning

        - Filter out all system schemas by default [#459](https://github.com/pingcap/tidb-lightning/pull/459)
        - Support setting a default value for the auto-random primary key for the Local-backend or Importer-backend [#457](https://github.com/pingcap/tidb-lightning/pull/457)
        - Use range properties to make the range split more precise in Local-backend [#422](https://github.com/pingcap/tidb-lightning/pull/422)
        - Support a human-readable format (such as "2.5 GiB") in `tikv-importer.region-split-size`, `mydumper.read-block-size`, `mydumper.batch-size`, and `mydumper.max-region-size` [#471](https://github.com/pingcap/tidb-lightning/pull/471)

    + TiDB Binlog

        - Exit the Drainer process with the non-zero code if the upstream PD is down or if applying DDL or DML statements to the downstream fails [#1012](https://github.com/pingcap/tidb-binlog/pull/1012)

## Bug Fixes

+ TiDB

    - Fix the issue of incorrect results when using a prefix index with the `OR` condition [#21287](https://github.com/pingcap/tidb/pull/21287)
    - Fix a bug that might cause panic when automatic retry is enabled [#21285](https://github.com/pingcap/tidb/pull/21285)
    - Fix a bug that occurs when checking partition definition according to column type [#21273](https://github.com/pingcap/tidb/pull/21273)
    - Fix a bug that the value type of the partition expression is not consistent with the partition column type [#21136](https://github.com/pingcap/tidb/pull/21136)
    - Fix a bug that the hash-type partition does not check whether the partition name is unique [#21257](https://github.com/pingcap/tidb/pull/21257)
    - Fix the wrong results returned after inserting a value of the non-`INT` type into the hash partitioned table [#21238](https://github.com/pingcap/tidb/pull/21238)
    - Fix the unexpected error when using index join in the `INSERT` statement in some cases [#21249](https://github.com/pingcap/tidb/pull/21249)
    - Fix the issue that the `BigInt` unsigned column value in the `CASE WHEN` operator is incorrectly converted to the `BigInt` signed value [#21236](https://github.com/pingcap/tidb/pull/21236)
    - Fix a bug that index hash join and index merge join do not consider collation [#21219](https://github.com/pingcap/tidb/pull/21219)
    - Fix a bug that the partitioned table does not consider collation in the `CREATE TABLE` and `SELECT` syntax [#21181](https://github.com/pingcap/tidb/pull/21181)
    - Fix the issue that the query result of `slow_query` might miss some rows [#21211](https://github.com/pingcap/tidb/pull/21211)
    - Fix the issue that `DELETE` might not delete data correctly when the database name is not in a pure lower representation [#21206](https://github.com/pingcap/tidb/pull/21206)
    - Fix a bug that causes schema change after DML operations [#21050](https://github.com/pingcap/tidb/pull/21050)
    - Fix the bug that the coalesced column cannot be queried when using join [#21021](https://github.com/pingcap/tidb/pull/21021)
    - Fix the wrong results of some semi-join queries [#21019](https://github.com/pingcap/tidb/pull/21019)
    - Fix the issue that the table lock does not take effect on the `UPDATE` statement [#21002](https://github.com/pingcap/tidb/pull/21002)
    - Fix the issue of stack overflow that occurs when building the recursive view [#21001](https://github.com/pingcap/tidb/pull/21001)
    - Fix the unexpected result returned when performing index merge join operations on outer join [#20954](https://github.com/pingcap/tidb/pull/20954)
    - Fix the issue that sometimes a transaction that has an undetermined result might be treated as failed [#20925](https://github.com/pingcap/tidb/pull/20925)
    - Fix the issue that `EXPLAIN FOR CONNECTION` cannot show the last query plan [#21315](https://github.com/pingcap/tidb/pull/21315)
    - Fix the issue that when Index Merge is used in a transaction with the Read Committed isolation level, the result might be incorrect [#21253](https://github.com/pingcap/tidb/pull/21253)
    - Fix the auto-ID allocation failure caused by the transaction retry after the write conflict [#21079](https://github.com/pingcap/tidb/pull/21079)
    - Fix the issue that JSON data cannot be correctly imported to TiDB using `LOAD DATA` [#21074](https://github.com/pingcap/tidb/pull/21074)
    - Fix the issue that the default value of newly added `Enum`-type columns is incorrect [#20998](https://github.com/pingcap/tidb/pull/20998)
    - Fix the issue that the `adddate` function inserts invalid characters [#21176](https://github.com/pingcap/tidb/pull/21176)
    - Fix the issue that the wrong `PointGet` plan generated in some situations causes wrong results [#21244](https://github.com/pingcap/tidb/pull/21244)
    - Ignore the conversion of daylight saving time in the `ADD_DATE` function to be compatible with MySQL [#20888](https://github.com/pingcap/tidb/pull/20888)
    - Fix a bug that prevents inserting strings with trailing spaces that exceed `varchar` or `char`'s length constraint [#21282](https://github.com/pingcap/tidb/pull/21282)
    - Fix a bug that does not converting the integer from `[1, 69]` to `[2001, 2069]` or from `[70, 99]` to `[1970, 1999]` when comparing `int` with `year` [#21283](https://github.com/pingcap/tidb/pull/21283)
    - Fix the panic caused by the overflowing result of the `sum()` function when calculating the `Double` type field [#21272](https://github.com/pingcap/tidb/pull/21272)
    - Fix a bug that `DELETE` fails to add lock on the unique key [#20705](https://github.com/pingcap/tidb/pull/20705)
    - Fix a bug that snapshot reads hits the lock cache [#21539](https://github.com/pingcap/tidb/pull/21539)
    - Fix an issue of potential memory leak after reading a lot of data in a long-lived transaction [#21129](https://github.com/pingcap/tidb/pull/21129)
    - Fix the issue that omitting the table alias in a subquery will have a syntax error returned [#20367](https://github.com/pingcap/tidb/pull/20367)

+ TiKV

    - Fix the issue that Coprocessor might return wrong results when there are more than 255 columns [#9131](https://github.com/tikv/tikv/pull/9131)
    - Fix the issue that Region Merge might cause data loss during network partition [#9108](https://github.com/tikv/tikv/pull/9108)
    - Fix the issue that the `ANALYZE` statement might cause panic when using the `latin1` character set [#9082](https://github.com/tikv/tikv/pull/9082)
    - Fix the wrong results returned when converting the numeric type to the time type [#9031](https://github.com/tikv/tikv/pull/9031)
    - Fix a bug that TiDB Lightning fails to ingest SST files to TiKV with the Importer-backend or Local-backend when Transparent Data Encryption (TDE) is enabled [#8995](https://github.com/tikv/tikv/pull/8995)
    - Fix the invalid `advertise-status-addr` value (`0.0.0.0`) [#9036](https://github.com/tikv/tikv/pull/9036)
    - Fix the issue that an error is returned indicating that a key exists when this key is locked and deleted in a committed transaction [#8930](https://github.com/tikv/tikv/pull/8930)
    - Fix the issue that the RocksDB cache mapping error causes data corruption [#9029](https://github.com/tikv/tikv/pull/9029)
    - Fix a bug that Follower Read might return stale data after the leader is transferred [#9240](https://github.com/tikv/tikv/pull/9240)
    - Fix the issue that stale old values might be read in the pessimistic lock [#9282](https://github.com/tikv/tikv/pull/9282)
    - Fix a bug that replica read might get stale data after the leader transfer [#9240](https://github.com/tikv/tikv/pull/9240)
    - Fix the issue of TiKV crash that occurs when receiving `SIGPROF` after profiling [#9229](https://github.com/tikv/tikv/pull/9229)

+ PD

    - Fix the issue that the leader roles specified using placement rules do not take effect in some cases [#3208](https://github.com/pingcap/pd/pull/3208)
    - Fix the issue that the `trace-region-flow` value is unexpectedly set to `false` [#3120](https://github.com/pingcap/pd/pull/3120)
    - Fix a bug that the service safepoint with infinite Time To Live (TTL) does not work [#3143](https://github.com/pingcap/pd/pull/3143)

+ TiDB Dashboard

    - Fix a display issue of time in the Chinese language [#755](https://github.com/pingcap/tidb-dashboard/pull/755)
    - Fix a bug that the browser compatibility notice does not work [#776](https://github.com/pingcap/tidb-dashboard/pull/776)
    - Fix the issue that the transaction `start_ts` is incorrectly displayed in some scenarios [#793](https://github.com/pingcap/tidb-dashboard/pull/793)
    - Fix the issue that some SQL texts are incorrectly formatted [#805](https://github.com/pingcap/tidb-dashboard/pull/805)

+ TiFlash

    - Fix the issue that `INFORMATION_SCHEMA.CLUSTER_HARDWARE` might contain the information of disks that are not in use
    - Fix the issue that the estimate on memory usage of Delta Cache is smaller than the actual usage
    - Fix the memory leak caused by thread information statistics

+ Tools

    + Backup & Restore (BR)

        - Fix the failure caused by special characters in S3 secret access keys [#617](https://github.com/pingcap/br/pull/617)

    + TiCDC

        - Fix the issue that multiple owners might exist when the owner campaign key is deleted [#1104](https://github.com/pingcap/ticdc/pull/1104)
        - Fix a bug that TiCDC might fail to continue replicating data when a TiKV node crashes or recovers from a crash. This bug only exists in v4.0.8. [#1198](https://github.com/pingcap/ticdc/pull/1198)
        - Fix the issue that the metadata is repeatedly flushed to etcd before a table is initialized [#1191](https://github.com/pingcap/ticdc/pull/1191)
        - Fix an issue of replication interruption caused by early GC or the latency of updating `TableInfo` when the schema storage caches TiDB tables [#1114](https://github.com/pingcap/ticdc/pull/1114)
        - Fix the issue that the schema storage costs too much memory when DDL operations are frequent [#1127](https://github.com/pingcap/ticdc/pull/1127)
        - Fix the goroutine leak when a changefeed is paused or stopped [#1075](https://github.com/pingcap/ticdc/pull/1075)
        - Increase the maximum retry timeout to 600 seconds in Kafka producer to prevent replication interruption caused by the service or network jitter in the downstream Kafka [#1118](https://github.com/pingcap/ticdc/pull/1118)
        - Fix a bug that the Kafka batch size does not take effect [#1112](https://github.com/pingcap/ticdc/pull/1112)
        - Fix a bug that some tables' row change might be lost when the network between TiCDC and PD has jitter and when there are paused changefeeds being resumed at the same time [#1213](https://github.com/pingcap/ticdc/pull/1213)
        - Fix a bug that the TiCDC process might exit when the network between TiCDC and PD is not stable [#1218](https://github.com/pingcap/ticdc/pull/1218)
        - Use a singleton PD client in TiCDC and fix a bug that TiCDC closes PD client by accident which causes replication block [#1217](https://github.com/pingcap/ticdc/pull/1217)
        - Fix a bug that the TiCDC owner might consume too much memory in the etcd watch client [#1224](https://github.com/pingcap/ticdc/pull/1224)

    + Dumpling

        - Fix the issue that Dumpling might get blocked when its connection to the MySQL database server is closed [#190](https://github.com/pingcap/dumpling/pull/190)

    + TiDB Lightning

        - Fix the issue that keys are encoded using the wrong field information [#437](https://github.com/pingcap/tidb-lightning/pull/437)
        - Fix the issue that GC life time TTL does not take effect [#448](https://github.com/pingcap/tidb-lightning/pull/448)
        - Fix the issue that causes panic when manually stops the running TiDB Lightning in the Local-backend mode [#484](https://github.com/pingcap/tidb-lightning/pull/484)
