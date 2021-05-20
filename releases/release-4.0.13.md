---
title: TiDB 4.0.13 Release Notes
---

# TiDB 4.0.13 Release Notes

发版日期：TBD

TiDB 版本：4.0.13

## 兼容性更改

## 新功能

## 提升改进

+ PD

    - 优化 tso 处理时间的统计 metrics [#3524](https://github.com/pingcap/pd/pull/3524)
    - 更新 dashboard 的版本至  v2021.03.12.1 [#3469](https://github.com/pingcap/pd/pull/3469)

+ TiFlash

    - 自动清除过期历史数据以释放磁盘空间

## Bug 修复

+ TiFlash

    - 修复未向 Prometheus 报告 `delta-merge-tasks` 数量的问题
    - 修复 `Segment Split` 期间发生进程崩溃的问题
    - 修复 Grafana 中面板 `Region write Duration` 位置错误的问题
    - 修复了存储引擎无法删除数据的潜在问题
    - 修复 `TIME` 类型转换为 `INT` 类型时产生错误结果的问题
    - 修复 `bitwise` 算子和 TiDB 行为不一致的问题
    - 修复字符串转换为 `INT` 时产生错误结果的问题
    - 修复连续快速写入可能导致 TiFlash 内存溢出的问题
    - 修复 Table GC 时会引发空指针的问题
    - 修复向已被删除的表写数据时 TiFlash 进程崩溃的问题
    - 修复当使用 BR 恢复数据时 TiFlash 进程可能崩溃的问题
    - 修复当使用通用 CI Collation 时字符权重错误的问题
    - 修复被逻辑删除的表丢失数据的潜在问题
    - 修复比较包含空字符的字符串时产生错误结果的问题
    - 修复输入列包含空常量时逻辑函数返回错误结果的问题
    - 修复逻辑函数仅接受受数字类型输入的问题
    - 修复时间戳值为 `1970-01-01` 且时区偏移为负时计算结果不正确的问题
    - 修复 Decimal256 的哈希值计算结果不稳定的问题
