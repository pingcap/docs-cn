---
title: TiDB 5.2.3 Release Note
---

# TiDB 5.2.3 Release Note

Release date: December 3, 2021

TiDB version: 5.2.3

## Bug fix

+ TiKV

    - Fix the issue that the `GcKeys` task does not work when it is called by multiple keys. Caused by this issue, compaction filer GC might not drop the MVCC deletion information. [#11217](https://github.com/tikv/tikv/issues/11217)
