---
title: TiDB 5.2.1 Release Notes
---

# TiDB 5.2.1 Release Notes

Release date: September 9, 2021

TiDB version: 5.2.1

## Bug fixes

+ TiDB

    - Fix an error that occurs during execution caused by the wrong execution plan. The wrong execution plan is caused by the shallow copy of schema columns when pushing down the aggregation operators on partitioned tables. [#27797](https://github.com/pingcap/tidb/issues/27797) [#26554](https://github.com/pingcap/tidb/issues/26554)

+ TiKV

    - Fix the issue of unavailable TiKV caused by Raftstore deadlock when migrating Regions. The workaround is to disable the scheduling and restart the unavailable TiKV. [#10909](https://github.com/tikv/tikv/issues/10909)
