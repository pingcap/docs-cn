---
title: TiDB 4.0.4 Release Notes
---

# TiDB 4.0.4 Release Notes

发版日期：2020 年 7 月 31 日

TiDB 版本：4.0.4

## Bug 修复

+ TiDB

    - 修复 BatchPointGet 算子结果不正确的问题
    - 修复查询 `information_schema.columns` 卡死的问题
    - 修复 PointGet 和 BatchPointGet 在遇到 `in(null)` 条件时出错的问题
    - 修复 HashJoin 算子在遇到 `set`, `enum` 类型时查询结果不正确的问题 
