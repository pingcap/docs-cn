---
title: TiDB 5.1.3 Release Note
summary: TiDB 5.1.3 was released on December 3, 2021. This version includes a bug fix for TiKV, addressing an issue where the `GcKeys` task does not work when called by multiple keys, leading to potential problems with compaction filter GC.
---

# TiDB 5.1.3 Release Note

Release date: December 3, 2021

TiDB version: 5.1.3

## Bug fix

+ TiKV

    - Fix the issue that the `GcKeys` task does not work when it is called by multiple keys. Caused by this issue, compaction filter GC might not drop the MVCC deletion information. [#11217](https://github.com/tikv/tikv/issues/11217)
