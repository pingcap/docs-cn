---
title: TiDB 3.1 Beta Release Notes
summary: TiDB 3.1 Beta 发布说明：发版日期为 2019 年 12 月 20 日，TiDB 版本为 3.1.0-beta，TiDB Ansible 版本为 3.1.0-beta。TiDB 新增 SQL 优化器和丰富的 SQL hint 功能。另外，TiDB 还支持 Follower Read 功能。TiKV 新增支持分布式备份恢复功能和 Follower Read 功能。PD 也新增支持分布式备份恢复功能。
---

# TiDB 3.1 Beta Release Notes

发版日期：2019 年 12 月 20 日

TiDB 版本：3.1.0-beta

TiDB Ansible 版本：3.1.0-beta

## TiDB

+ SQL 优化器
    - 丰富 SQL hint [#12192](https://github.com/pingcap/tidb/pull/12192)
+ 新功能
    - TiDB 支持 Follower Read 功能 [#12535](https://github.com/pingcap/tidb/pull/12535)

## TiKV

- 支持分布式备份恢复功能 [#5532](https://github.com/tikv/tikv/pull/5532)
- TiKV 支持 Follower Read 功能 [#5562](https://github.com/tikv/tikv/pull/5562)

## PD

- 支持分布式备份恢复功能 [#1896](https://github.com/pingcap/pd/pull/1896)
