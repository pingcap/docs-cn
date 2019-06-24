---
title: TiDB 2.0.5 Release Notes
category: Releases
aliases: ['/docs/releases/205/']
---

# TiDB 2.0.5 Release Notes

On July 6, 2018, TiDB 2.0.5 is released. Compared with TiDB 2.0.4, this release has great improvement in system compatibility and stability.

## TiDB

- New Features
    - Add the `tidb_disable_txn_auto_retry` system variable which is used to disable the automatic retry of transactions [#6877](https://github.com/pingcap/tidb/pull/6877)
- Improvements
    - Optimize the cost calculation of `Selection` to make the result more accurate [#6989](https://github.com/pingcap/tidb/pull/6989)
    - Select the query condition that completely matches the unique index or the primary key as the query path directly [#6966](https://github.com/pingcap/tidb/pull/6966)
    - Execute necessary cleanup when failing to start the service [#6964](https://github.com/pingcap/tidb/pull/6964)
    - Handle `\N` as NULL in the `Load Data` statement [#6962](https://github.com/pingcap/tidb/pull/6962)
    - Optimize the code structure of CBO [#6953](https://github.com/pingcap/tidb/pull/6953)
    - Report the monitoring metrics earlier when starting the service [#6931](https://github.com/pingcap/tidb/pull/6931)
    - Optimize the format of slow queries by removing the line breaks in SQL statements and adding user information [#6920](https://github.com/pingcap/tidb/pull/6920)
    - Support multiple asterisks in comments [#6858](https://github.com/pingcap/tidb/pull/6858)
- Bug Fixes
    - Fix the issue that `KILL QUERY` always requires SUPER privilege [#7003](https://github.com/pingcap/tidb/pull/7003)
    - Fix the issue that users might fail to login when the number of users exceeds 1024 [#6986](https://github.com/pingcap/tidb/pull/6986)
    - Fix an issue about inserting unsigned `float`/`double` data [#6940](https://github.com/pingcap/tidb/pull/6940)
    - Fix the compatibility of the `COM_FIELD_LIST` command to resolve the panic issue in some MariaDB clients [#6929](https://github.com/pingcap/tidb/pull/6929)
    - Fix the `CREATE TABLE IF NOT EXISTS LIKE` behavior [#6928](https://github.com/pingcap/tidb/pull/6928)
    - Fix an issue in the process of TopN pushdown [#6923](https://github.com/pingcap/tidb/pull/6923)
    - Fix the ID record issue of the currently processing row when an error occurs in executing `Add Index` [#6903](https://github.com/pingcap/tidb/pull/6903)

## PD

- Fix the issue that replicas migration uses up TiKV disks space in some scenarios
- Fix the crash issue caused by `AdjacentRegionScheduler`

## TiKV

- Fix the potential overflow issue in decimal operations
- Fix the dirty read issue that might occur in the process of merging