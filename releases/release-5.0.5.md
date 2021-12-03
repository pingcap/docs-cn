---
title: TiDB 5.0.5 Release Notes
---

# TiDB 5.0.5 Release Notes

Release date: December 3, 2021

TiDB version: 5.0.5

## Improvement

+ TiDB

    - Upgrade the Grafana version from 7.5.7 to 7.5.11

## Bug fix

+ TiKV

    - Fix the issue that the `GcKeys` task does not work when it is called by multiple keys. Caused by this issue, compaction filer GC might not drop the MVCC deletion information. [#11217](https://github.com/tikv/tikv/issues/11217)
