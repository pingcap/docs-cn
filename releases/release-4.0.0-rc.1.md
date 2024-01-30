---
title: TiDB 4.0 RC.1 Release Notes
aliases: ['/docs/dev/releases/release-4.0.0-rc.1/','/docs/dev/releases/4.0.0-rc.1/']
summary: TiDB 4.0 RC.1 was released on April 28, 2020. The release includes compatibility changes, important bug fixes, new features, and bug fixes for TiKV, TiDB, TiFlash, TiCDC, Backup & Restore (BR), and Placement Driver (PD). The bug fixes address issues such as data inconsistency, deadlock, and replication failure. New features include support for sending Coprocessor requests to TiFlash in batches and enabling the load-based split region operation. Additionally, TiFlash now supports pushing down the fromUnixTime and dateFormat functions.
---

# TiDB 4.0 RC.1 Release Notes

Release date: April 28, 2020

TiDB version: 4.0.0-rc.1

## Compatibility Changes

+ TiKV

    - Disable the Hibernate Region feature by default [#7618](https://github.com/tikv/tikv/pull/7618)

+ TiDB Binlog

    - Support the sequence DDL operation in Drainer [#950](https://github.com/pingcap/tidb-binlog/pull/950)

## Important Bug Fixes

+ TiDB

    - Fix the issue that the `INSERT ... ON DUPLICATE UPDATE` statement might be incorrectly executed on multiple rows in an explicit transaction because `MemBuffer` is not checked [#16689](https://github.com/pingcap/tidb/pull/16689)
    - Fix the data inconsistency when locking duplicated keys on multiple rows [#16769](https://github.com/pingcap/tidb/pull/16769)
    - Fix the panic that occurs when recycling the non-superbatch idle connection between TiDB instances [#16303](https://github.com/pingcap/tidb/pull/16303)

+ TiKV

    - Fix the deadlock issue caused by the probe request from TiDB [#7540](https://github.com/tikv/tikv/pull/7540)
    - Fix the issue that the minimum commit timestamp of a transaction might overflow which affects data correctness [#7638](https://github.com/tikv/tikv/pull/7638)

+ TiFlash

    - Fix the data loss issue caused by the `rename table` operation when multiple data paths are configured
    - Fix the issue that an error occurs when reading data from a merged Region
    - Fix the issue that an error occurs when reading data from a Region that is in the abnormal state
    - Modify the mapping of table names in TiFlash to correctly support `recover table`/`flashback table`
    - Modify the storage path to fix the potential data loss issue that occurs when renaming the table
    - Fix the potential panic of TiDB when Super Batch is enabled
    - Modify the read mode in the online update scenario to improve the read performance

+ TiCDC

    - Fix the replication failure that occurs because the schema internally maintained in TiCDC fails to correctly handle the timing issue of read and write operations [#438](https://github.com/pingcap/tiflow/pull/438) [#450](https://github.com/pingcap/tiflow/pull/450) [#478](https://github.com/pingcap/tiflow/pull/478) [#496](https://github.com/pingcap/tiflow/pull/496)
    - Fix the bug that the TiKV client fails to correctly maintain the internal resources when encountering some TiKV anomalies [#499](https://github.com/pingcap/tiflow/pull/499) [#492](https://github.com/pingcap/tiflow/pull/492)
    - Fix the bug that meta data is not correctly cleaned up and abnormally remains in the TiCDC nodes [#488](https://github.com/pingcap/tiflow/pull/488) [#504](https://github.com/pingcap/tiflow/pull/504)
    - Fix the issue that the TiKV client fails to correctly handle the repeated sending of the prewrite event [#446](https://github.com/pingcap/tiflow/pull/446)
    - Fix the issue that the TiKV client fails to correctly handle the redundant prewrite events received before the initialization [#448](https://github.com/pingcap/tiflow/pull/448)

+ Backup & Restore (BR)

    - Fix the issue that checksum is still executed when checksum is disabled [#223](https://github.com/pingcap/br/pull/223)
    - Fix the incremental replication failure when `auto-random` or `alter-pk` is enabled in TiDB [#230](https://github.com/pingcap/br/pull/230) [#231](https://github.com/pingcap/br/pull/231)

## New Features

+ TiDB

    - Support sending Coprocessor requests to TiFlash in batches [#16226](https://github.com/pingcap/tidb/pull/16226)
    - Enable the Coprocessor cache feature by default [#16710](https://github.com/pingcap/tidb/pull/16710)
    - Parse only the registered sections of a statement in the special comment of the SQL statement [#16157](https://github.com/pingcap/tidb/pull/16157)
    - Support using the `SHOW CONFIG` syntax to show the configurations of PD and TiKV instances [#16475](https://github.com/pingcap/tidb/pull/16475)

+ TiKV

    - Support using the user-owned KMS key for the server-side encryption when backing up data to S3 [#7630](https://github.com/tikv/tikv/pull/7630)
    - Enable the load-based `split region` operation [#7623](https://github.com/tikv/tikv/pull/7623)
    - Support validating common names [#7468](https://github.com/tikv/tikv/pull/7468)
    - Add the file lock check to avoid starting multiple TiKV instances that are bound to the same address [#7447](https://github.com/tikv/tikv/pull/7447)
    - Support AWS KMS in encryption at rest [#7465](https://github.com/tikv/tikv/pull/7465)

+ Placement Driver (PD)

    - Remove `config manager` to let other components control their component configurations [#2349](https://github.com/pingcap/pd/pull/2349)

+ TiFlash

    - Add the metrics report related to the read and write workloads of DeltaTree engine
    - Cache the `handle` and `version` columns to reduce the disk I/O of a single read or write request
    - Support pushing down the `fromUnixTime` and `dateFormat` functions
    - Evaluate the global state according to the first disk and report this evaluation
    - Add the graphics in Grafana related to the read and write workloads of DeltaTree engine
    - Optimize the decimal data encoding in the `Chunk` codec
    - Implement the gRPC API of Diagnostics (SQL diagnosis) to support querying system tables such as `INFORMATION_SCHEMA.CLUSTER_INFO`

+ TiCDC

    - Support sending messages in batches in the Kafka sink module [#426](https://github.com/pingcap/tiflow/pull/426)
    - Support file sorting in the processor [#477](https://github.com/pingcap/tiflow/pull/477)
    - Support automatic `resolve lock` [#459](https://github.com/pingcap/tiflow/pull/459)
    - Add the feature that automatically updates the TiCDC service GC safe point to PD [#487](https://github.com/pingcap/tiflow/pull/487)
    - Add the timezone setting for data replication [#498](https://github.com/pingcap/tiflow/pull/498)

+ Backup and Restore (BR)

    - Support configuring S3/GCS in the storage URL [#246](https://github.com/pingcap/br/pull/246)

## Bug Fixes

+ TiDB

- Fix the issue that negative numbers cannot be correctly displayed in the system table because the columns are defined as unsigned [#16004](https://github.com/pingcap/tidb/pull/16004)
- Add a warning when the `use_index_merge` hint contains the invalid index name [#15960](https://github.com/pingcap/tidb/pull/15960)
- Forbid multiple instances of a TiDB server sharing the same temporary directory [#16026](https://github.com/pingcap/tidb/pull/16026)
- Fix the panic that occurs during the execution of `explain for connection` when the plan cache is enabled [#16285](https://github.com/pingcap/tidb/pull/16285)
- Fix the issue that the result of the `tidb_capture_plan_baselines` system variable is incorrectly displayed [#16048](https://github.com/pingcap/tidb/pull/16048)
- Fix the issue that the `group by` clause in the `prepare` statement is incorrectly parsed [#16377](https://github.com/pingcap/tidb/pull/16377)
- Fix the panic that might occur during the execution of the `analyze primary key` statement [#16081](https://github.com/pingcap/tidb/pull/16081)
- Fix the issue that the TiFlash store information in the `cluster_info` system table is wrong [#16024](https://github.com/pingcap/tidb/pull/16024)
- Fix the panic that might occur during the Index Merge process [#16360](https://github.com/pingcap/tidb/pull/16360)
- Fix the issue that an incorrect result might occur when the Index Merge reader reads the generated columns [#16359](https://github.com/pingcap/tidb/pull/16359)
- Fix the incorrect display of the default sequence value in the `show create table` statement [#16526](https://github.com/pingcap/tidb/pull/16526)
- Fix the issue that the `not-null` error is returned because the sequence is used as the default values of the primary key [#16510](https://github.com/pingcap/tidb/pull/16510)
- Fix the issue that no error is reported for a blocked SQL execution when TiKV continues to return the `StaleCommand` error [#16530](https://github.com/pingcap/tidb/pull/16530)
- Fix the issue that an error is reported if you only specify `COLLATE` when creating a database; add the missing `COLLATE` part in the result of `SHOW CREATE DATABASE` [#16540](https://github.com/pingcap/tidb/pull/16540)
- Fix the partition pruning failure when the plan cache is enabled [#16723](https://github.com/pingcap/tidb/pull/16723)
- Fix the bug that `PointGet` returns wrong results when handling the overflow [#16755](https://github.com/pingcap/tidb/pull/16755)
- Fix the issue that a wrong result is returned when querying the `slow_query` system table with equal time values [#16806](https://github.com/pingcap/tidb/pull/16806)

+ TiKV

    - Address the OpenSSL security issue: CVE-2020-1967 [#7622](https://github.com/tikv/tikv/pull/7622)
    - Avoid protecting rollback records written by `BatchRollback` to improve performance when many write conflicts exist in optimistic transactions [#7604](https://github.com/tikv/tikv/pull/7604)
    - Fix the issue that the needless wake-up of transactions results in useless retry and performance reduction in heavy lock-race workloads [#7551](https://github.com/tikv/tikv/pull/7551)
    - Fix the issue that the Region might be stuck in the multi-time merging [#7518](https://github.com/tikv/tikv/pull/7518)
    - Fix the issue that the learner is not deleted when deleting the learner [#7518](https://github.com/tikv/tikv/pull/7518)
    - Fix the issue that follower read might cause panic in raft-rs [#7408](https://github.com/tikv/tikv/pull/7408)
    - Fix the bug that a SQL operation might fail because of the `group by constant` error [#7383](https://github.com/tikv/tikv/pull/7383)
    - Fix the issue that an optimistic lock might block reads if the corresponding primary lock is a pessimistic lock [#7328](https://github.com/tikv/tikv/pull/7328)

+ PD

    - Fix the issue that some APIs might fail in the TLS validation [#2363](https://github.com/pingcap/pd/pull/2363)
    - Fix the issue that the configuration API cannot accept a configuration item with a prefix [#2354](https://github.com/pingcap/pd/pull/2354)
    - Fix the issue that the `500` error is returned when the scheduler is not found [#2328](https://github.com/pingcap/pd/pull/2328)
    - Fix the issue that the `404` error is returned for the `scheduler config balance-hot-region-scheduler list` command [#2321](https://github.com/pingcap/pd/pull/2321)

+ TiFlash

    - Disable the coarse-grained index optimization for the storage engine
    - Fix the bug that an exception is thrown when resolving locks for Regions and some locks need to be skipped
    - Fix the null pointer exception (NPE) when collecting the Coprocessor statistics
    - Fix the check for Region meta to ensure that the process of Region Split/Region Merge is correct
    - Fix the issue that the message size exceeds the limit for gRPC because the size of Coprocessor response is not estimated
    - Fix the handling of the `AdminCmdType::Split` command in TiFlash
