---
title: TiDB 4.0.8 Release Notes
---

# TiDB 4.0.8 Release Notes

发版日期：2020 年 10 月 29 日

TiDB 版本：4.0.8

## 新功能

+ TiDB

    - 

+ Tools

    + TiCDC

        - 支持快照级别一致性复制 [#932](https://github.com/pingcap/ticdc/pull/932)

## 优化提升

+ TiDB

    - 

+ TiKV

    - 

+ PD

    - 

+ TiFlash

    - 

+ Tools

    + Backup & Restore (BR)

        - 通过将 split 和 restore 流水线来加速恢复 [#428](https://github.com/pingcap/br/pull/428)
        - 支持手动恢复 PD 的调度器 [#530](https://github.com/pingcap/br/pull/530)
        - 将移除 PD 调度器接口改为暂停调度器 [#551](https://github.com/pingcap/br/pull/551)

    + TiCDC

        - 在 MySQL 中定期输出统计信息 [#1023](https://github.com/pingcap/ticdc/pull/1023)

    + Dumpling

        - 支持导出 S3 [#155](https://github.com/pingcap/dumpling/pull/155)
        - 支持导出 View [#158](https://github.com/pingcap/dumpling/pull/158)
        - 支持导出全是生成列的数据表 [#166](https://github.com/pingcap/dumpling/pull/166)

    + TiDB Lightning

        - 支持多字节的 csv delimiter 和 separator [#406](https://github.com/pingcap/tidb-lightning/pull/406)
        - 通过禁止一些 PD 调度器加速导入 [#408](https://github.com/pingcap/tidb-lightning/pull/408)
        - 在 v4.0 集群上使用 GC TTL 接口来防止 checksum 阶段的 GC 报错 [#396](https://github.com/pingcap/tidb-lightning/pull/396)

## Bug 修复

+ TiDB

    - 

+ TiKV

    - 

+ PD

    - 

+ TiFlash

    - 

+ Tools

    + Backup & Restore (BR)

        - 修复 restore 期间可能发生的 `send on closed channel panic` 问题 [#559](https://github.com/pingcap/br/pull/559)

    + TiCDC

        - 解决 owner 因更新 GC safe point 失败而非预期退出 [#979](https://github.com/pingcap/ticdc/pull/979)
        - 解决非预期的任务信息更新 [#1017](https://github.com/pingcap/ticdc/pull/1017)
        - 解决非预期的空 Maxwell 消息 [#978](https://github.com/pingcap/ticdc/pull/978)

    + TiDB Lightning

        - 解决 column 信息错误的问题 [#420](https://github.com/pingcap/tidb-lightning/pull/420)
        - 解决 local 模式下获取 Region 信息的死循环 [#418](https://github.com/pingcap/tidb-lightning/pull/418)
