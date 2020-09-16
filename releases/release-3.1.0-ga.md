---
title: TiDB 3.1.0 GA Release Notes
aliases: ['/docs/dev/releases/release-3.1.0-ga/','/docs/dev/releases/3.1.0-ga/']
---

# TiDB 3.1.0 GA Release Notes

Release date: April 16, 2020

TiDB version: 3.1.0 GA

TiDB Ansible version: 3.1.0 GA

## Compatibility Changes

+ TiDB

    - Support directly stopping starting TiDB if the HTTP listening port is unavailable when the `report-status` configuration item is enabled [#16291](https://github.com/pingcap/tidb/pull/16291)

+ Tools

    - Backup & Restore (BR)

        * BR does not support restoring data from the TiKV cluster earlier than 3.1 GA [#233](https://github.com/pingcap/br/pull/233)

## New Features

+ TiDB

    - Support displaying the information of Coprocessor tasks in `explain format = "dot"` [#16125](https://github.com/pingcap/tidb/pull/16125)
    - Reduce the redundant stack information of log using the `disable-error-stack` configuration item [#16182](https://github.com/pingcap/tidb/pull/16182)

+ Placement Driver (PD)

    - Optimize the hot Region scheduling [#2342](https://github.com/pingcap/pd/pull/2342)

+ TiFlash

    - Add the metrics report related to the read and write workloads of DeltaTree engine
    - Support pushing down the `fromUnixTime` and `dateFormat` functions
    - Disable the rough set filter by default

+ TiDB Ansible

    - Add TiFlash monitor [#1253](https://github.com/pingcap/tidb-ansible/pull/1253) [#1257](https://github.com/pingcap/tidb-ansible/pull/1257)
    - Optimize the configuration parameters of TiFlash [#1262](https://github.com/pingcap/tidb-ansible/pull/1262) [#1265](https://github.com/pingcap/tidb-ansible/pull/1265) [#1271](https://github.com/pingcap/tidb-ansible/pull/1271)
    - Optimize the TiDB starting script [#1268](https://github.com/pingcap/tidb-ansible/pull/1268)

## Bug Fixes

+ TiDB

    - Fix the panic issue caused by the merge join operation in some scenarios [#15920](https://github.com/pingcap/tidb/pull/15920)
    - Fix the issue that some expressions are repeatedly counted in selectivity calculation [#16052](https://github.com/pingcap/tidb/pull/16052)
    - Fix the panic issue occurred when loading the statistics information in extreme cases [#15710](https://github.com/pingcap/tidb/pull/15710)
    - Fix the issue that an error is returned in some cases when equivalent expressions cannot be recognized in SQL query [#16015](https://github.com/pingcap/tidb/pull/16015)
    - Fix the issue that an error is returned when querying the `view` of one database from another database [#15867](https://github.com/pingcap/tidb/pull/15867)
    - Fix the panic issue that occurs when the column is handled using `fast analyze` [#16080](https://github.com/pingcap/tidb/pull/16080)
    - Fix the incorrect character set of the `current_role` print result [#16084](https://github.com/pingcap/tidb/pull/16084)
    - Refine the log of MySQL connection handshake error [#15799](https://github.com/pingcap/tidb/pull/15799)
    - Fix the panic issue caused by port probing after the audit plugin is loaded [#16065](https://github.com/pingcap/tidb/pull/16065)
    - Fix the panic issue of the `sort` operator on left join because the `TypeNull` class is mistaken as a variable-length type [#15739](https://github.com/pingcap/tidb/pull/15739)
    - Fix the issue of inaccurate count of monitoring session retry errors [#16120](https://github.com/pingcap/tidb/pull/16120)
    - Fix the issue of wrong results of `weekday` in the `ALLOW_INVALID_DATES` mode [#16171](https://github.com/pingcap/tidb/pull/16171)
    - Fix the issue that Garbage Collection (GC) might not work normally when the cluster has TiFlash nodes [#15761](https://github.com/pingcap/tidb/pull/15761)
    - Fix the issue that TiDB goes out of memory (OOM) when users set a large partition count when creating the hash partitioned table [#16219](https://github.com/pingcap/tidb/pull/16219)
    - Fix the issue that warnings are mistaken as errors, and make the `UNION` statement have the same behavior as the `SELECT` statement [#16138](https://github.com/pingcap/tidb/pull/16138)
    - Fix the execution error when `TopN` is pushed down to mocktikv [#16200](https://github.com/pingcap/tidb/pull/16200)
    - Increase the initial length of `chunk.column.nullBitMap` to avoid unnecessary overhead of `runtime.growslice` [#16142](https://github.com/pingcap/tidb/pull/16142)

+ TiKV

    - Fix the panic issue caused by replica read [#7418](https://github.com/tikv/tikv/pull/7418) [#7369](https://github.com/tikv/tikv/pull/7369)
    - Fix the issue that the restoration process creates empty Regions [#7419](https://github.com/tikv/tikv/pull/7419)
    - Fix the issue that repeated resolve lock requests might harm the atomicity of pessimistic transactions [#7389](https://github.com/tikv/tikv/pull/7389)

+ TiFlash

    - Fix the potential issue of the `rename table` operation when replicating the schema from TiDB
    - Fix the issue of data loss caused by the `rename table` operation under multiple data path configurations
    - Fix the issue that TiFlash reports incorrect storage space in some scenarios
    - Fix the potential issue caused by reading from TiFlash when Region Merge is enabled

+ Tools

    - TiDB Binlog

        * Fix the issue that TiFlash-related DDL jobs might interrupt the replication of Drainer [#948](https://github.com/pingcap/tidb-binlog/pull/948) [#942](https://github.com/pingcap/tidb-binlog/pull/942)

    - Backup & Restore (BR)

        * Fix the issue that the `checksum` operation is still executed when it is disabled [#223](https://github.com/pingcap/br/pull/223)
        * Fix the issue that incremental backup fails when TiDB enables `auto-random` or `alter-pk` [#230](https://github.com/pingcap/br/pull/230) [#231](https://github.com/pingcap/br/pull/231)
