---
title: TiDB 5.0.4 Release Notes
---

# TiDB 5.0.4 Release Notes

Release Date: September 27, 2021

TiDB version: 5.0.4

## Compatibility changes

+ TiDB

    - Fix the issue that executing `SHOW VARIABLES` in a new session is slow. This fix reverts some changes made in [#19341](https://github.com/pingcap/tidb/pull/19341) and might cause compatibility issues. [#24326](https://github.com/pingcap/tidb/issues/24326)
    - Change the default value of the `tidb_stmt_summary_max_stmt_count` variable from `200` to `3000` [#25873](https://github.com/pingcap/tidb/pull/25873)
    + The following bug fixes change execution results, which might cause upgrade incompatibilities:
        - Fix the issue that TiDB returns wrong result when the children of `UNION` contain the `NULL` value [#26559](https://github.com/pingcap/tidb/issues/26559)
        - Fix the issue that `greatest(datetime) union null` returns empty string [#26532](https://github.com/pingcap/tidb/issues/26532)
        - Fix the issue that the behavior of the `last_day` function is incompatible in SQL mode [#26000](https://github.com/pingcap/tidb/pull/26000)
        - Fix the issue that the `having` clause might not work correctly [#26496](https://github.com/pingcap/tidb/issues/26496)
        - Fix the wrong execution results that occur when the collations around the `between` expression are different [#27146](https://github.com/pingcap/tidb/issues/27146)
        - Fix the wrong execution results that occur when the column in the `group_concat` function has a non-bin collation [#27429](https://github.com/pingcap/tidb/issues/27429)
        - Fix an issue that using a `count(distinct)` expression on multiple columns returns wrong result when the new collation is enabled [#27091](https://github.com/pingcap/tidb/issues/27091)
        - Fix the result wrong that occurs when the argument of the `extract` function is a negative duration [#27236](https://github.com/pingcap/tidb/issues/27236)
        - Fix the issue that inserting an invalid date does not report an error when the `SQL_MODE` is 'STRICT_TRANS_TABLES' [#26762](https://github.com/pingcap/tidb/issues/26762)
        - Fix the issue that using an invalid default date does not report an error when the `SQL_MODE` is 'NO_ZERO_IN_DATE' [#26766](https://github.com/pingcap/tidb/issues/26766)
        - Fix a bug on the query range of prefix index [#26029](https://github.com/pingcap/tidb/issues/26029)
        - Fix the issue that the `LOAD DATA` statement might abnormally import non-utf8 data [#25979](https://github.com/pingcap/tidb/issues/25979)
        - Fix the issue that `insert ignore on duplicate update` might insert wrong data when the secondary index has the same column with the primary key [#25809](https://github.com/pingcap/tidb/issues/25809)
        - Fix the issue that `insert ignore duplicate update` might insert wrong data when a partitioned table has a clustered index [#25846](https://github.com/pingcap/tidb/issues/25846)
        - Fix the issue that the query result might be wrong when the key is the `ENUM` type in point get or batch point get [#24562](https://github.com/pingcap/tidb/issues/24562)
        - Fix the wrong result that occurs when dividing a `BIT`-type value [#23479](https://github.com/pingcap/tidb/issues/23479)
        - Fix the issue that the results of `prepared` statements and direct queries might be inconsistent [#22949](https://github.com/pingcap/tidb/issues/22949)
        - Fix the issue that the query result might be wrong when a `YEAR` type is compared with a string or an integer type [#23262](https://github.com/pingcap/tidb/issues/23262)

## Feature enhancements

+ TiDB

    - Support setting `tidb_enforce_mpp=1` to ignore the optimizer estimation and forcibly use the MPP mode [#26382](https://github.com/pingcap/tidb/pull/26382)

+ TiKV

    - Support changing TiCDC configurations dynamically [#10645](https://github.com/tikv/tikv/issues/10645)

+ PD

    - Add OIDC-based SSO support for TiDB Dashboard [#3884](https://github.com/tikv/pd/pull/3884)

+ TiFlash

    - Support the `HAVING()` function in DAG requests
    - Support the `DATE()` function
    - Add Grafana panels for write throughput per instance

## Improvements

+ TiDB

    - Trigger auto-analyze based on the histogram row count [#24237](https://github.com/pingcap/tidb/issues/24237)
    - Stop sending requests to a TiFlash node for a period if the node has failed and restarted before [#26757](https://github.com/pingcap/tidb/pull/26757)
    - Increase the `split region` upper limit to make `split table` and `presplit` more stable [#26657](https://github.com/pingcap/tidb/pull/26657)
    - Support retry for MPP queries [#26483](https://github.com/pingcap/tidb/pull/26483)
    - Check the availability of TiFlash before launching MPP queries [#1807](https://github.com/pingcap/tics/issues/1807)
    - Support the stable result mode to make the query result more stable [#26084](https://github.com/pingcap/tidb/pull/26084)
    - Support the MySQL system variable `init_connect` and its associated features [#18894](https://github.com/pingcap/tidb/issues/18894)
    - Thoroughly push down the `COUNT(DISTINCT)` aggregation function in the MPP mode [#25861](https://github.com/pingcap/tidb/pull/25861)
    - Print log warnings when the aggregation function cannot be pushed down in `EXPLAIN` statements [#25736](https://github.com/pingcap/tidb/pull/25736)
    - Add error labels for `TiFlashQueryTotalCounter` in Grafana dashboard [#25327](https://github.com/pingcap/tidb/pull/25327)
    - Support getting the MVCC data of a clustered index table through a secondary index by HTTP API [#24209](https://github.com/pingcap/tidb/issues/24209)
    - Optimize the memory allocation of `prepared` statement in parser [#24371](https://github.com/pingcap/tidb/pull/24371)

+ TiKV

    - Handle read ready and write ready separately to reduce read latency [#10475](https://github.com/tikv/tikv/issues/10475)
    - Reduce the size of Resolved TS messages to save network bandwidth [#2448](https://github.com/pingcap/ticdc/issues/2448)
    - Drop log instead of blocking threads when the slogger thread is overloaded and the queue is filled up [#10841](https://github.com/tikv/tikv/issues/10841)
    - Make the slow log of TiKV coprocessor only consider the time spent on processing requests [#10841](https://github.com/tikv/tikv/issues/10841)
    - Make prewrite as idempotent as possible to reduce the chance of undetermined errors [#10587](https://github.com/tikv/tikv/pull/10587)
    - Avoid the false "GC can not work" alert under low write flow [#10662](https://github.com/tikv/tikv/pull/10662)
    - Make the database to be restored always match the original cluster size during backup. [#10643](https://github.com/tikv/tikv/pull/10643)
    - Ensure that the panic output is flushed to the log [#9955](https://github.com/tikv/tikv/pull/9955)

+ PD

    - Improve the performance of synchronizing Region information between PDs [#3993](https://github.com/tikv/pd/pull/3993)

+ Tools

    + Dumpling

        - Support backing up MySQL-compatible databases that do not support the `START TRANSACTION ... WITH CONSISTENT SNAPSHOT` or the `SHOW CREATE TABLE` syntax [#309](https://github.com/pingcap/dumpling/issues/309)

    + TiCDC

        - Optimize memory management when Unified Sorter is using memory to sort [#2553](https://github.com/pingcap/ticdc/issues/2553)
        - Prohibit operating TiCDC clusters across major or minor versions [#2598](https://github.com/pingcap/ticdc/pull/2598)
        - Reduce the goroutine usage when a table's Regions are all transferred away from a TiKV node [#2284](https://github.com/pingcap/ticdc/issues/2284)
        - Remove `file sorter` [#2326](https://github.com/pingcap/ticdc/pull/2326)
        - Always pull the old values from TiKV and the output is adjusted according to `enable-old-value` [#2301](https://github.com/pingcap/ticdc/issues/2301)
        - Improve the error message returned when a PD endpoint misses the certificate [#1973](https://github.com/pingcap/ticdc/issues/1973)
        - Optimize workerpool for fewer goroutines when concurrency is high [#2211](https://github.com/pingcap/ticdc/issues/2211)
        - Add a global gRPC connection pool and share gRPC connections among KV clients [#2533](https://github.com/pingcap/ticdc/pull/2533)

## Bug Fixes

+ TiDB

    - Fix the issue that TiDB might panic when querying a partitioned table and the partition key has the `IS NULL` condition [#23802](https://github.com/pingcap/tidb/issues/23802)
    - Fix the issue that the overflow check of the `FLOAT64` type is different with that of MySQL [#23897](https://github.com/pingcap/tidb/issues/23897)
    - Fix the wrong character set and collation for the `case when` expression [#26662](https://github.com/pingcap/tidb/issues/26662)
    - Fix the issue that committing pessimistic transactions might cause write conflicts [#25964](https://github.com/pingcap/tidb/issues/25964)
    - Fix a bug that the index keys in a pessimistic transaction might be repeatedly committed [#26359](https://github.com/pingcap/tidb/issues/26359) [#10600](https://github.com/tikv/tikv/pull/10600)
    - Fix the issue that TiDB might panic when resolving the async commit locks [#25778](https://github.com/pingcap/tidb/issues/25778)
    - Fix a bug that a column might not be found when using `INDEX MERGE` [#25045](https://github.com/pingcap/tidb/issues/25045)
    - Fix a bug that `ALTER USER REQUIRE SSL` clears users' `authentication_string` [#25225](https://github.com/pingcap/tidb/issues/25225)
    - Fix a bug that the value of the `tidb_gc_scan_lock_mode` global variable on a new cluster shows "PHYSICAL" instead of the actual default mode "LEGACY" [#25100](https://github.com/pingcap/tidb/issues/25100)
    - Fix the bug that the `TIKV_REGION_PEERS` system table does not show the correct `DOWN` status [#24879](https://github.com/pingcap/tidb/issues/24879)
    - Fix the issue of memory leaks that occurs when HTTP API is used [#24649](https://github.com/pingcap/tidb/pull/24649)
    - Fix the issue that views do not support `DEFINER` [#24414](https://github.com/pingcap/tidb/issues/24414)
    - Fix the issue that `tidb-server --help` exits with the code `2` [#24046](https://github.com/pingcap/tidb/issues/24046)
    - Fix the issue that setting the global variable `dml_batch_size` does not take effect [#24709](https://github.com/pingcap/tidb/issues/24709)
    - Fix the issue that using `read_from_storage` and partitioned table at the same time causes an error [#20372](https://github.com/pingcap/tidb/issues/20372)
    - Fix the issue that TiDB panics when executing the projection operator [#24264](https://github.com/pingcap/tidb/issues/24264)
    - Fix the issue that statistics might cause queries to panic [#24061](https://github.com/pingcap/tidb/pull/24061)
    - Fix the issue that using the `approx_percentile` function on a `BIT` column might panic [#23662](https://github.com/pingcap/tidb/issues/23662)
    - Fix the issue that the metrics on the **Coprocessor Cache** panel in Grafana are wrong [#26338](https://github.com/pingcap/tidb/issues/26338)
    - Fix the issue that concurrently truncating the same partition causes DDL statements to stuck [#26229](https://github.com/pingcap/tidb/issues/26229)
    - Fix the issue of wrong query results that occurs when the session variable is used as the `GROUP BY` item [#27106](https://github.com/pingcap/tidb/issues/27106)
    - Fix the wrong implicit conversion between `VARCHAR` and timestamp when joining tables [#25902](https://github.com/pingcap/tidb/issues/25902)
    - Fix the wrong results in associated subquery statements [#27233](https://github.com/pingcap/tidb/issues/27233)

+ TiKV

    - Fix the potential disk full issue caused by corrupted snapshot files [#10813](https://github.com/tikv/tikv/issues/10813)
    - Fix the TiKV panic issue that occurs when upgrading from a pre-5.0 version with Titan enabled [#10843](https://github.com/tikv/tikv/pull/10843)
    - Fix the issue that TiKV of a newer version cannot be rolled back to v5.0.x [#10843](https://github.com/tikv/tikv/pull/10843)
    - Fix the TiKV panic issue that occurs when upgrading from a pre-5.0 version to a 5.0 version or later. If a cluster was upgraded from TiKV v3.x with Titan enabled before the upgrade, this cluster might encounter the issue. [#10774](https://github.com/tikv/tikv/issues/10774)
    - Fix the parsing failure caused by the left pessimistic locks [#26404](https://github.com/pingcap/tidb/issues/26404)
    - Fix the panic that occurs when calculating duration on certain platforms [#10571](https://github.com/tikv/tikv/pull/10571)
    - Fix the issue that the keys of `batch_get_command` in Load Base Split are unencoded [#10542](https://github.com/tikv/tikv/issues/10542)

+ PD

    - Fix the issue that PD does not fix the down peers in time [#4077](https://github.com/tikv/pd/issues/4077)
    - Fix the issue that the replica count of the default placement rules stays constant after `replication.max-replicas` is updated [#3886](https://github.com/tikv/pd/issues/3886)
    - Fix a bug that PD might panic when scaling out TiKV [#3868](https://github.com/tikv/pd/issues/3868)
    - Fix the scheduling conflict issue that occurs when multiple schedulers are running at same time [#3807](https://github.com/tikv/pd/issues/3807)
    - Fix the issue that the scheduler might appear again even if it has been deleted [#2572](https://github.com/tikv/pd/issues/2572)

+ TiFlash

    - Fix the potential panic issue that occurs when running table scan tasks
    - Fix the potential memory leak issue that occurs when executing MPP tasks
    - Fix a bug that TiFlash raises the `duplicated region` error when handling DAQ requests
    - Fix the issue of unexpected results when executing the aggregation functions `COUNT` or `COUNT DISTINCT`
    - Fix the potential panic issue that occurs when executing MPP tasks
    - Fix a potential bug that TiFlash cannot restore data when deployed on multiple disks
    - Fix the potential panic issue that occurs when deconstructing `SharedQueryBlockInputStream`
    - Fix the potential panic issue that occurs when deconstructing `MPPTask`
    - Fix the issue of unexpected results when TiFlash fails to establish MPP connections
    - Fix the potential panic issue that occurs when resolving locks
    - Fix the issue that the store size in metrics is inaccurate under heavy writing
    - Fix a bug of incorrect results that occurs when queries contain filters like `CONSTANT`, `<`, `<=`, `>`, `>=`, or `COLUMN`
    - Fix the potential issue that TiFlash cannot garbage-collect the delta data after running for a long time
    - Fix a potential bug that metrics display wrong values
    - Fix the potential issue of data inconsistency that occurs when TiFlash is deployed on multiple disks

+ Tools

    + Dumpling

        - Fix the issue that the execution of `show table status` is stuck in MySQL 8.0.3 or a later version [#322](https://github.com/pingcap/dumpling/issues/322)

    + TiCDC

        - Fix the issue of process panic that occurs when encoding the data types such as `mysql.TypeString, mysql.TypeVarString, mysql.TypeVarchar` into JSON [#2758](https://github.com/pingcap/ticdc/issues/2758)
        - Fix a data inconsistency issue that occurs because multiple processors might write data to the same table when this table is being re-scheduled [#2417](https://github.com/pingcap/ticdc/pull/2417)
        - Decrease the gRPC window size to avoid the OOM that occurs when TiCDC captures too many Regions [#2724](https://github.com/pingcap/ticdc/pull/2724)
        - Fix the error that the gRPC connection is frequently broken when the memory pressure is high [#2202](https://github.com/pingcap/ticdc/issues/2202)
        - Fix a bug that causes TiCDC to panic on the unsigned `TINYINT` type [#2648](https://github.com/pingcap/ticdc/issues/2648)
        - Fix the issue that TiCDC Open Protocol outputs an empty value when inserting a transaction and deleting data of the same row in the upstream [#2612](https://github.com/pingcap/ticdc/issues/2612)
        - Fix a bug that DDL handling fails when a changefeed starts at the finish TS of a schema change [#2603](https://github.com/pingcap/ticdc/issues/2603)
        - Fix the issue that irresponsive downstreams interrupt the replication task in old owner until the task times out [#2295](https://github.com/pingcap/ticdc/issues/2295)
        - Fix a bug in metadata management [#2558](https://github.com/pingcap/ticdc/pull/2558)
        - Fix the issue of data inconsistency that occurs after the TiCDC owner switch [#2230](https://github.com/pingcap/ticdc/issues/2230)
        - Fix the issue that outdated capture might appear in the output of the `capture list` command [#2388](https://github.com/pingcap/ticdc/issues/2388)
        - Fix the `ErrSchemaStorageTableMiss` error that occurs when the DDL Job duplication is encountered in the integrated test [#2422](https://github.com/pingcap/ticdc/issues/2422)
        - Fix the bug that a changefeed cannot be removed if the `ErrGCTTLExceeded` error occurs [#2391](https://github.com/pingcap/ticdc/issues/2391)
        - Fix a bug that replicating large tables to cdclog fails [#1259](https://github.com/pingcap/ticdc/issues/1259) [#2424](https://github.com/pingcap/ticdc/issues/2424)
        - Fix the CLI backward compatibility issue [#2373](https://github.com/pingcap/ticdc/issues/2373)
        - Fix the issue of insecure concurrent access to the map in `SinkManager` [#2299](https://github.com/pingcap/ticdc/pull/2299)
        - Fix the issue of potential DDL loss when the owner crashes when executing DDL statements [#1260](https://github.com/pingcap/ticdc/issues/1260)
        - Fix the issue that the lock is resolved immediately after a Region is initialized [#2188](https://github.com/pingcap/ticdc/issues/2188)
        - Fix the issue of extra partition dispatching that occurs when adding a new partitioned table [#2263](https://github.com/pingcap/ticdc/pull/2263)
        - Fix the issue that TiCDC keeps warning on removed changefeeds [#2156](https://github.com/pingcap/ticdc/issues/2156)
