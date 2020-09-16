---
title: TiDB 4.0.6 Release Notes
---

# TiDB 4.0.6 Release Notes

Release date: September 15, 2020

TiDB version: 4.0.6

## New Features

+ TiFlash

    - Support outer join in TiFlash broadcast join

+ TiDB Dashboard

    - Add Query Editor and execution UI (experimental) [#713](https://github.com/pingcap-incubator/tidb-dashboard/pull/713)
    - Support store location topology visualization [#719](https://github.com/pingcap-incubator/tidb-dashboard/pull/719)
    - Add cluster configuration UI (experimental) [#733](https://github.com/pingcap-incubator/tidb-dashboard/pull/733)
    - Support sharing the current session [#741](https://github.com/pingcap-incubator/tidb-dashboard/pull/741)
    - Support displaying the number of execution plans in SQL Statement list [#746](https://github.com/pingcap-incubator/tidb-dashboard/pull/746)

+ Tools

    + TiCDC

        - Support outputting data in the `maxwell` format [#869](https://github.com/pingcap/ticdc/pull/869)

## Improvements

+ TiDB

    - Replace error codes and messages with standard errors [#19888](https://github.com/pingcap/tidb/pull/19888)
    - Improve the write performance of partitioned table [#19649](https://github.com/pingcap/tidb/pull/19649)
    - Record more RPC runtime information in `Cop Runtime` statistics [#19264](https://github.com/pingcap/tidb/pull/19264)
    - Forbid creating tables in `metrics_schema` and `performance_schema` [#19792](https://github.com/pingcap/tidb/pull/19792)
    - Support adjusting the concurrency of the union executor [#19886](https://github.com/pingcap/tidb/pull/19886)
    - Support out join in broadcast join [#19664](https://github.com/pingcap/tidb/pull/19664)
    - Add SQL digest for the process list [#19829](https://github.com/pingcap/tidb/pull/19829)
    - Switch to the pessimistic transaction mode for autocommit statement retry [#19796](https://github.com/pingcap/tidb/pull/19796)
    - Support the `%r` and `%T` data format in `Str_to_date()` [#19693](https://github.com/pingcap/tidb/pull/19693)
    - Enable `SELECT INTO OUTFILE` to require the file privilege [#19577](https://github.com/pingcap/tidb/pull/19577)
    - Support the `stddev_pop` function [#19541](https://github.com/pingcap/tidb/pull/19541)
    - Add the `TiDB-Runtime` dashboard [#19396](https://github.com/pingcap/tidb/pull/19396)
    - Improve compatibility for the `ALTER TABLE` algorithms [#19364](https://github.com/pingcap/tidb/pull/19364)
    - Encode `insert`/`delete`/`update` plans in the slow log `plan` field [#19269](https://github.com/pingcap/tidb/pull/19269)

+ TiKV

    - Reduce QPS drop when `DropTable` or `TruncateTable` is being executed [#8627](https://github.com/tikv/tikv/pull/8627)
    - Support generating metafile of error codes [#8619](https://github.com/tikv/tikv/pull/8619)
    - Add performance statistics for cf scan details [#8618](https://github.com/tikv/tikv/pull/8618)
    - Add the `rocksdb perf context` panel in the Grafana default template [#8467](https://github.com/tikv/tikv/pull/8467)

+ PD

    - Update TiDB Dashboard to v2020.09.08.1 [#2928](https://github.com/pingcap/pd/pull/2928)
    - Add more metrics for Region and store heartbeat [#2891](https://github.com/tikv/pd/pull/2891)
    - Change back to the original way to control the low space threshold [#2875](https://github.com/pingcap/pd/pull/2875)
    - Support standard error codes
        - [#2918](https://github.com/tikv/pd/pull/2918) [#2911](https://github.com/tikv/pd/pull/2911) [#2913](https://github.com/tikv/pd/pull/2913) [#2915](https://github.com/tikv/pd/pull/2915) [#2912](https://github.com/tikv/pd/pull/2912)
        - [#2907](https://github.com/tikv/pd/pull/2907) [#2906](https://github.com/tikv/pd/pull/2906) [#2903](https://github.com/tikv/pd/pull/2903) [#2806](https://github.com/tikv/pd/pull/2806) [#2900](https://github.com/tikv/pd/pull/2900) [#2902](https://github.com/tikv/pd/pull/2902)

+ TiFlash

    - Add Grafana panels for data replication (`apply Region snapshots` and `ingest SST files`)
    - Add Grafana panels for `write stall`
    - Add `dt_segment_force_merge_delta_rows` and `dt_segment_force_merge_delta_deletes` to adjust the threshold of `write stall`
    - Support setting `raftstore.snap-handle-pool-size` to `0` in TiFlash-Proxy to disable applying Region snapshot by multi-thread to reduce memory consumption during data replication
    - Support CN check on `https_port` and `metrics_port`

+ Tools

    + TiCDC

        - Skip resolved lock during puller initialization [#910](https://github.com/pingcap/ticdc/pull/910)
        - Reduce PD write frequency [#937](https://github.com/pingcap/ticdc/pull/937)

    + Backup & Restore (BR)

        - Add real time cost in summary log [#486](https://github.com/pingcap/br/issues/486)

    + Dumpling

        - Support outputting `INSERT` with column names [#135](https://github.com/pingcap/dumpling/pull/135)
        - Unify the `--filesize` and `--statement-size` definitions with those of mydumper [#142](https://github.com/pingcap/dumpling/pull/142)

    + TiDB Lightning

        - Split and ingest Regions in more precise sizes [#369](https://github.com/pingcap/tidb-lightning/pull/369)

    + TiDB Binlog

        - Support setting GC time in `go time` package format [#996](https://github.com/pingcap/tidb-binlog/pull/996)

## Bug Fixes

+ TiDB

    - Fix an issue of collecting the `tikv_cop_wait` time in metric profile [#19881](https://github.com/pingcap/tidb/pull/19881)
    - Fix the wrong result of `SHOW GRANTS` [#19834](https://github.com/pingcap/tidb/pull/19834)
    - Fix the incorrect query result of `!= ALL (subq)` [#19831](https://github.com/pingcap/tidb/pull/19831)
    - Fix a bug of converting the `enum` and `set` types [#19778](https://github.com/pingcap/tidb/pull/19778)
    - Add a privilege check for `SHOW STATS_META` and `SHOW STATS_BUCKET` [#19760](https://github.com/pingcap/tidb/pull/19760)
    - Fix the error of unmatched column lengths caused by `builtinGreatestStringSig` and `builtinLeastStringSig` [#19758](https://github.com/pingcap/tidb/pull/19758)
    - If unnecessary errors or warnings occur, the vectorized control expresions fall back to their scalar execution [#19749](https://github.com/pingcap/tidb/pull/19749)
    - Fix the error of the `Apply` operator when the type of the correlation column is `Bit` [#19692](https://github.com/pingcap/tidb/pull/19692)
    - Fix the issue that occurs when the user queries `processlist` and `cluster_log` in MySQL 8.0 client [#19690](https://github.com/pingcap/tidb/pull/19690)
    - Fix the issue that plans of the same type have different plan digests [#19684](https://github.com/pingcap/tidb/pull/19684)
    - Forbid changing the column type from `Decimal` to `Int` [#19682](https://github.com/pingcap/tidb/pull/19682)
    - Fix the issue that `SELECT ... INTO OUTFILE` returns the runtime error [#19672](https://github.com/pingcap/tidb/pull/19672)
    - Fix the incorrect implementation of `builtinRealIsFalseSig` [#19670](https://github.com/pingcap/tidb/pull/19670)
    - Fix the issue that the partition expression check misses the parentheses expression [#19614](https://github.com/pingcap/tidb/pull/19614)
    - Fix a query error when there is an `Apply` operator upon `HashJoin` [#19611](https://github.com/pingcap/tidb/pull/19611)
    - Fix an incorrect result of vectorization that casts `Real` as `Time` [#19594](https://github.com/pingcap/tidb/pull/19594)
    - Fix the bug that the `SHOW GRANTS` statement shows grants for non-existent users [#19588](https://github.com/pingcap/tidb/pull/19588)
    - Fix a query error when there is an `Apply` executor upon `IndexLookupJoin` [#19566](https://github.com/pingcap/tidb/pull/19566)
    - Fix the wrong results when converting `Apply` to `HashJoin` on a partitioned table [#19546](https://github.com/pingcap/tidb/pull/19546)
    - Fix incorrect results when there is an `IndexLookUp` executor on the inner side of an `Apply` [#19508](https://github.com/pingcap/tidb/pull/19508)
    - Fix an unexpected panic when using view [#19491](https://github.com/pingcap/tidb/pull/19491)
    - Fix the incorrect result of the `anti-semi-join` query [#19477](https://github.com/pingcap/tidb/pull/19477)
    - Fix the bug that the `TopN` statistics is not deleted when the statistics is dropped [#19465](https://github.com/pingcap/tidb/pull/19465)
    - Fix a wrong result caused by mistaken usage of batch point get [#19460](https://github.com/pingcap/tidb/pull/19460)
    - Fix the bug that a column cannot be found in `indexLookupJoin` with a virtual generated column [#19439](https://github.com/pingcap/tidb/pull/19439)
    - Fix an error that different plans of the `select` and `update` queries compare datum [#19403](https://github.com/pingcap/tidb/pull/19403)
    - Fix a data race for TiFlash work index in Region cache [#19362](https://github.com/pingcap/tidb/pull/19362)
    - Fix the bug that the `logarithm` function does not show a warning [#19291](https://github.com/pingcap/tidb/pull/19291)
    - Fix an unexpected error that occurs when TiDB persists data to disks [#19272](https://github.com/pingcap/tidb/pull/19272)
    - Support using a single partitioned table on the inner side of index join [#19197](https://github.com/pingcap/tidb/pull/19197)
    - Fix the wrong hash key value generated for decimal [#19188](https://github.com/pingcap/tidb/pull/19188)
    - Fix the issue that TiDB returns a `no regions` error when table endKey and Region endKey are the same [#19895](https://github.com/pingcap/tidb/pull/19895)
    - Fix the unexpected success of alter partition [#19891](https://github.com/pingcap/tidb/pull/19891)
    - Fix the wrong value of the default maximum packet length allowed for pushed down expressions [#19876](https://github.com/pingcap/tidb/pull/19876)
    - Fix a wrong behavior for the `Max`/`Min` functions on the `ENUM`/`SET` columns [#19869](https://github.com/pingcap/tidb/pull/19869)
    - Fix the read failure from the `tiflash_segments` and `tiflash_tables` system tables when some TiFlash nodes are offline [#19748](https://github.com/pingcap/tidb/pull/19748)
    - Fix a wrong result of the `Count(col)` aggregation function [#19628](https://github.com/pingcap/tidb/pull/19628)
    - Fix a runtime error of the `TRUNCATE` operation [#19445](https://github.com/pingcap/tidb/pull/19445)
    - Fix the issue that `PREPARE statement FROM @Var` will fail when `Var` contains uppercase characters [#19378](https://github.com/pingcap/tidb/pull/19378)
    - Fix the bug that schema charset modification in an uppercase schema will cause panic [#19302](https://github.com/pingcap/tidb/pull/19302)
    - Fix the inconsistency of plans between `information_schema.statements_summary` and `explain`, when the information contains `tikv/tiflash` [#19159](https://github.com/pingcap/tidb/pull/19159)
    - Fix the error in tests that the file does not exist for `select into outfile` [#19725](https://github.com/pingcap/tidb/pull/19725)
    - Fix the issue that `INFORMATION_SCHEMA.CLUSTER_HARDWARE` does not have raid device information [#19457](https://github.com/pingcap/tidb/pull/19457)
    - Make the `add index` operation that has a generated column with the `case-when` expression can exit normally when it encounters a parse error [#19395](https://github.com/pingcap/tidb/pull/19395)
    - Fix the bug that the DDL operation takes too long to retry [#19488](https://github.com/pingcap/tidb/pull/19488)
    - Make statements like `alter table db.t1 add constraint fk foreign key (c2) references t2(c1)` execute without first executing `use db` [#19471](https://github.com/pingcap/tidb/pull/19471)
    - Change the dispatch error from the `Error` to the `Info` message in the server log file [#19454](https://github.com/pingcap/tidb/pull/19454)

+ TiKV

    - Fix the estimation error for a non-index column when collation is enabled [#8620](https://github.com/tikv/tikv/pull/8620)
    - Fix the issue that Green GC might miss locks during the process of Region transfer [#8460](https://github.com/tikv/tikv/pull/8460)
    - Fix a panic issue that occurs when TiKV runs very slowly during Raft membership change [#8497](https://github.com/tikv/tikv/pull/8497)
    - Fix the deadlock issue that occurs between the PD client thread and other threads when calling PD sync requests [#8612](https://github.com/tikv/tikv/pull/8612)
    - Upgrade jemalloc to v5.2.1 to address the issue of memory allocation in huge page [#8463](https://github.com/tikv/tikv/pull/8463)
    - Fix the issue that the unified thread pool hangs for long-running queries [#8427](https://github.com/tikv/tikv/pull/8427)

+ PD

    - Add the `initial-cluster-token` configuration to prevent different clusters from communicating with each other during bootstrap [#2922](https://github.com/pingcap/pd/pull/2922)
    - Fix the unit of store limit rate when the mode is `auto` [#2826](https://github.com/pingcap/pd/pull/2826)
    - Fix the issue that some schedulers persist configuration without solving errors [#2818](https://github.com/tikv/pd/pull/2818)
    - Fix the empty HTTP response in scheduler [#2871](https://github.com/tikv/pd/pull/2871) [#2874](https://github.com/tikv/pd/pull/2874)

+ TiFlash

    - Fix the issue that after renaming the primary key column in previous versions, TiFlash might not start after upgrading to v4.0.4/v4.0.5
    - Fix the exceptions that occur after modifying the column's `nullable` attribute
    - Fix the crash caused by computing a table's replication status
    - Fix the issue that TiFlash is not available for data reads after users applied unsupported DDL operations
    - Fix the exceptions caused by unsupported collations which are treated as `utf8mb4_bin`
    - Fix the issue that the QPS panel for the TiFlash coprocessor executor always displays `0` in Grafana
    - Fix the wrong result of the `FROM_UNIXTIME` function when input is `NULL`

+ Tools

    + TiCDC

        - Fix the issue that TiCDC leaks memory in some cases [#942](https://github.com/pingcap/ticdc/pull/942)
        - Fix the issue that TiCDC might panic in Kafka sink [#912](https://github.com/pingcap/ticdc/pull/912)
        - Fix the issue that CommitTs or ResolvedTs (CRTs) might be less than `resolvedTs` in puller [#927](https://github.com/pingcap/ticdc/pull/927)
        - Fix the issue that `changefeed` might be blocked by MySQL driver [#936](https://github.com/pingcap/ticdc/pull/936)
        - Fix the incorrect Resolved Ts interval of TiCDC [#8573](https://github.com/tikv/tikv/pull/8573)

    + Backup & Restore (BR)

        - Fix a panic that might occur during checksum [#479](https://github.com/pingcap/br/pull/479)
        - Fix a panic that might occur after the change of PD Leader [#496](https://github.com/pingcap/br/pull/496)

    + Dumpling

        - Fix the issue that the `NULL` value for the binary type is not handled properly [#137](https://github.com/pingcap/dumpling/pull/137)

    + TiDB Lightning

        - Fix the issue that all failed operations of writes and ingests are mistakenly displayed as successful [#381](https://github.com/pingcap/tidb-lightning/pull/381)
        - Fix the issue that some checkpoint updates might not be written to the database before TiDB Lightning exits [#386](https://github.com/pingcap/tidb-lightning/pull/386)
