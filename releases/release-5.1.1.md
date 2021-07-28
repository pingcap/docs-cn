---
title: TiDB 5.1.1 Release Notes
---

# TiDB 5.1.1 Release Notes

## 兼容性更改

## 功能增强

+ TiFlash

    - 支持 DAG 请求中的 `HAVING()` 函数

## 改进提升

## Bug 修复

+ TiFlash

    - 修复处理扫表任务时出现进程崩溃的潜在问题
    - 修复处理 DAG 请求时出现  `duplicated region` 报错的问题
    - 修复读负载高的情况下进程崩溃的问题
    - 修复执行 `DateFormat` 函数时出现进程崩溃的潜在问题
    - 修复处理 MPP 任务时出现内存泄漏的潜在问题
    - 修复执行 `COUNT` 或 `COUNT DISTINCT` 函数时出现非预期结果的问题
    - 修复多盘部署时出现数据无法恢复的潜在问题
    - 修复 TiDB Dashboard 无法正确显示 TiFlash 磁盘信息的问题
    - 修复析构 `SharedQueryBlockInputStream` 时出现进程崩溃的潜在问题
    - 修复析构 `MPPTask` 时出现进程崩溃的潜在问题
