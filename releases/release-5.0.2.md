---
title: TiDB 5.0.2 Release Notes
---

# TiDB 5.0.2 Release Notes

发版日期：2021 年 6 月 9 日

TiDB 版本：5.0.2

## 兼容性更改

## 新功能

## 提升改进

+ TiFlash

    - 优化 apply region snapshots 操作的内存占用
    - 优化锁操作以避免 DDL 和读数据相互阻塞
    - 支持 integer 和 real 类型转化为 real 类型

## Bug 修复

+ TiFlash

    - 修复并发复制共享 delta 索引导致结果错误的问题
    - 修复当存在数据缺失的情况下 TiFlash 无法启动的问题
    - 修复旧的 dm 文件无法被自动清理的问题
    - 修复 TiFlash 与 `compaction filter` 特性的兼容性问题
    - 修复 `ExchangeSender` 可能传输重复数据的问题
    - 修复 TiFlash 与 `async commit` 的兼容性问题
    - 修复当 timezone 类型转换结果包含 timestamp 类型时返回错误结果的问题
    - 修复 TiFlash 在 Segment Split 期间异常退出的问题
    - 修复非根节点 MPP 任务的执行信息显示不正确的问题
