---
title: TiDB 3.1.1 Release Notes
aliases: ['/docs/dev/releases/release-3.1.1/','/docs/dev/releases/3.1.1/']
---

# TiDB 3.1.1 Release Notes

Release date: April 30, 2020

TiDB version: 3.1.1

TiDB Ansible version: 3.1.1

## New Features

+ TiDB

    - Add the table option for `auto_rand_base` [#16812](https://github.com/pingcap/tidb/pull/16812)
    - Add the `Feature ID` comment: In the special comments of SQL statements, only the registered statement fragment can be parsed by the parser; otherwise, the statement is ignored [#16155](https://github.com/pingcap/tidb/pull/16155)

+ TiFlash

    - Cache the `handle` and `version` columns to reduce the disk I/O for a single read request
    - Add in Grafana the graphics related to the read and write workloads of DeltaTree engine
    - Optimize the decimal data encoding in the `Chunk` codec
    - Reduce the number of open file descriptors when TiFlash is in low workload

## Bug Fixes

+ TiDB

    - Fix the issue that the isolation read setting at the instance level does not take effect, and that the isolation read setting is incorrectly retained after TiDB is upgraded [#16482](https://github.com/pingcap/tidb/pull/16482) [#16802](https://github.com/pingcap/tidb/pull/16802)
    - Fix the partition selection syntax on the hash partitioned table so that an error is not reported for syntaxes such as `partition (P0)` [#16076](https://github.com/pingcap/tidb/pull/16076)
    - Fix the issue that when an `UPDATE` SQL statement only queries from a view but does not update the view, the update statement still reports an error [#16789](https://github.com/pingcap/tidb/pull/16789)
    - Fix the issue of wrong results caused by removing the `not not` from the nested query [#16423](https://github.com/pingcap/tidb/pull/16423)

+ TiFlash

    - Fix the issue that an error occurs when reading data from a Region that is in the abnormal state
    - Modify the mapping of table names in TiFlash to correctly support `recover table`/`flashback table`
    - Modify the storage path to fix the potential data loss issue that occurs when renaming a table
    - Modify the read mode in the online update scenario to improve the read performance
    - Fix the issue that TiFlash fails to start normally after upgrade if the database/table name contains special characters

+ Tools

    - Backup & Restore (BR)

        * Fix the issue that after BR restores a table with the `auto_random` attribute, inserting data might trigger the duplicate entry error [#241](https://github.com/pingcap/br/issues/241)
