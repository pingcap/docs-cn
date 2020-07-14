---
title: TiDB 3.0.13 Release Notes
aliases: ['/docs/dev/releases/release-3.0.13/','/docs/dev/releases/3.0.13/']
---

# TiDB 3.0.13 Release Notes

Release date: April 22, 2020

TiDB version: 3.0.13

## Bug Fixes

+ TiDB

    - Fix the issue caused by unchecked `MemBuffer` that the `INSERT ... ON DUPLICATE KEY UPDATE` statement might be executed incorrectly within a transaction when users need to insert multiple rows of duplicate data [#16690](https://github.com/pingcap/tidb/pull/16690)

+ TiKV

    - Fix the issue that the system might get stuck and the service is unavailable if `Region Merge` is executed repeatedly [#7612](https://github.com/tikv/tikv/pull/7612)
