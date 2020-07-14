---
title: TiDB 3.1.2 Release Notes
aliases: ['/docs/dev/releases/release-3.1.2/']
---

# TiDB 3.1.2 Release Notes

Release date: June 4, 2020

TiDB version: 3.1.2

## Bug Fixes

+ TiKV

    - Fix the error handling issue during backup and restoration with S3 and GCS [#7965](https://github.com/tikv/tikv/pull/7965)
    - Fix the `DefaultNotFound` error that occurs during restoration [#7838](https://github.com/tikv/tikv/pull/7938)

+ Tools

    - Backup & Restore (BR)

        - Retry automatically when the network is poor to improve stability with S3 and GCS storages [#314](https://github.com/pingcap/br/pull/314) [#7965](https://github.com/tikv/tikv/pull/7965)
        - Fix a restoration failure that occurs because the Region leader cannot be found when restoring small tables [#303](https://github.com/pingcap/br/pull/303)
        - Fix a data loss issue during restoration when a table’s row ID exceeds `2^(63)` [#323](https://github.com/pingcap/br/pull/323)
        - Fix the issue that empty databases and tables cannot be restored [#318](https://github.com/pingcap/br/pull/318)
        - Support using AWS KMS for server-side encryption (SSE) when targeting the S3 storage [#261](https://github.com/pingcap/br/pull/261)
