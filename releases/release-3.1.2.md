---
title: TiDB 3.1.2 Release Notes
---

# TiDB 3.1.2 Release Notes

发版日期：2020 年 6 月 4 日

TiDB 版本：3.1.2

## Bug 修复

+ TiKV

    - 修复 S3 和 GCS 备份恢复时的错误处理问题 [#7965](https://github.com/tikv/tikv/pull/7965)
    - 修复备份过程中的 `DefaultNotFound` 错误 [#7838](https://github.com/tikv/tikv/pull/7938)

+ Tools

    - Backup & Restore (BR)

        - 提升备份恢复到 S3 和 GCS 存储的稳定性，在网络较差时会自动重试 [#314](https://github.com/pingcap/br/pull/314) [#7965](https://github.com/tikv/tikv/pull/7965)
        - 修复恢复数据时因找不到 Region leader 出现的 `NotLeader` 错误，BR 会自动重试 [#303](https://github.com/pingcap/br/pull/303)
        - 修复恢复数据时 `rowID` 大于 `2^(63)` 的数据丢失问题 [#323](https://github.com/pingcap/br/pull/323)
        - 修复恢复数据时无法恢复空库空表的问题 [#318](https://github.com/pingcap/br/pull/318)
        - 增加备份恢复 S3 时的 AWS KMS 服务端加密 (SSE) 支持 [#261](https://github.com/pingcap/br/pull/261)
