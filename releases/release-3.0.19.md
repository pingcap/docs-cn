---
title: TiDB 3.0.19 Release Notes
---

# TiDB 3.0.19 Release Notes

发版日期：2020 年 9 月 25 日

TiDB 版本：3.0.19

## 兼容性变化


## 提升改进

+ TiDB

    - 
    
+ TiKV

    - 永久开启 `sync_log` [#8636](https://github.com/tikv/tikv/pull/8636)

+ PD

    -

## Bug 修复

+ TiDB

    - 

+ TiKV

    - 修复 TiKV 的 status server 解析响应出错导致 panic 的问题 [#8540](https://github.com/tikv/tikv/pull/8540)

+ Tools

    + TiDB Lightning

        - 修复了严格模式下 CSV 中遇到不合法 UTF 字符集没有及时退出的问题 [#378](https://github.com/pingcap/tidb-lightning/pull/378)
