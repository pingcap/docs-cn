---
title: TiDB 5.3.2 Release Notes
---

# TiDB 5.3.2 Release Notes

发版日期：2022 年 6 月 x 日

TiDB 版本：5.3.2

## 兼容性更改

## 功能增强

## 提升改进

## Bug 修复

+ TiFlash

    - 修复配置文件的一些问题 [#4093](https://github.com/pingcap/tiflash/issues/4093), [#4091](https://github.com/pingcap/tiflash/issues/4091)
    - 修复在设置副本数为 0 之后不能完全清理文件的问题 [#4414](https://github.com/pingcap/tiflash/issues/4414)
    - 修复在添加一些 `NOT NULL` 的列时报错的问题 [#4596](https://github.com/pingcap/tiflash/issues/4596)
    - 修复在重启过程中出现 `commit state jump backward` 错误的问题 [#2576](https://github.com/pingcap/tiflash/issues/2576)
    - 修复在大量 insert 后，TiFlash 副本可能会出现数据不一致的问题 [#4956](https://github.com/pingcap/tiflash/issues/4956)

