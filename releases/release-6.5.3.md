---
title: TiDB 6.5.3 Release Notes
summary: 了解 TiDB 6.5.3 版本的兼容性变更、改进提升，以及错误修复。
---

# TiDB 6.5.3 Release Notes

发版日期：2023 年 x 月 x 日

TiDB 版本：6.5.3

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v6.5/quick-start-with-tidb) | [生产部署](https://docs.pingcap.com/zh/tidb/v6.5/production-deployment-using-tiup) | [下载离线包](https://cn.pingcap.com/product-community/?version=v6.5.3#version-list)

## 兼容性变更

- note 1

## 改进提升

+ TiDB

    - note 1

+ TiKV

    - note 1

+ PD

    - note 1

+ TiFlash

    - note 1

+ Tools

    + Backup & Restore (BR)

        - note 1

    + TiCDC

        - note 1

    + TiDB Data Migration (DM)

        - note 1

    + TiDB Lightning

        - note 1

    + Dumpling

        - note 1

## 错误修复

+ TiDB

    - 修复一个 min, max 查询结果出错的问题  [#43805](https://github.com/pingcap/tidb/issues/43805) @[wshwsh12](https://github.com/wshwsh12)
    - 修复一个窗口函数计算下推到 tiflash 时执行计划构造错误的问题 [#43981](https://github.com/pingcap/tidb/issues/43981) @[gengliqi](https://github.com/gengliqi)
    - 修复一个使用 CTE 的查询 hang 住的问题 [#43758](https://github.com/pingcap/tidb/issues/43758) @[guo-shaoge](https://github.com/guo-shaoge)
    - 修复一个使用 AES_DECRYPT 表达时，sql 报错 runtime error: index out of range 的问题 [#43086](https://github.com/pingcap/tidb/issues/43086) @[lcwangchao](https://github.com/lcwangchao)

+ TiKV

    - note 1

+ PD

    - note 1

+ TiFlash

    - 修复一个分区表查询报错的问题 [#7519](https://github.com/pingcap/tiflash/issues/7519) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - 修复在表字段同时存在 TIMESTAMP 或者 TIME 类型和 GENERATED 类型情况下，查询 TiFlash 可能会报错的问题 [#7468](https://github.com/pingcap/tiflash/issues/7468) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - 修复大的更新事务可能会导致 TiFlash 反复报错重启的问题 [#7316](https://github.com/pingcap/tiflash/issues/7316) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复一个 insert select 语句从 tiflash 读取数据时，sql 报错 Truncate error cast decimal as decimal 的问题 [#7348](https://github.com/pingcap/tiflash/issues/7348) @[windtalker](https://github.com/windtalker)
   - 修复查询在 Join build 侧数据非常大，且包含许多小型字符串类型列时，可能会使用比实际需要更大的内存的问题。 [#7416](https://github.com/pingcap/tiflash/issues/7416) @[yibin87](https://github.com/yibin87)

+ Tools

    + Backup & Restore (BR)

        - note 1

    + TiCDC

        - note 1

    + TiDB Data Migration (DM)

        - note 1

    + TiDB Lightning

        - note 1

    + Dumpling

        - note 1
