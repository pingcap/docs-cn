---
title: TiDB 9.0.0 Release Notes
summary: 了解 TiDB 9.0.0 版本的新功能、兼容性变更、改进提升，以及错误修复。
---

# TiDB 9.0.0 Release Notes

<EmailSubscriptionWrapper />

发版日期：2025 年 xx 月 xx 日

TiDB 版本：9.0.0

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v8.5/quick-start-with-tidb) | [生产部署](https://docs.pingcap.com/zh/tidb/v9.0/production-deployment-using-tiup) | [下载离线包](https://cn.pingcap.com/product-community/?version=v9.0.0#version-list)

在 9.0.0 版本中，你可以获得以下关键特性：

<table>
<thead>
  <tr>
    <th>分类</th>
    <th>功能</th>
    <th>描述</th>
  </tr>
</thead>
<tbody>
  <tr>

  </tr>
</tbody>
</table>

## 功能详情

### 可扩展性



### 性能



### 稳定性



### SQL 功能



### 安全



## 兼容性变更

> **注意：**
>
> 以下为从 v8.5.0 升级至当前版本 (v9.0.0) 所需兼容性变更信息。如果从 v8.4.0 或之前版本升级到当前版本，可能也需要考虑和查看中间版本 Release Notes 中提到的兼容性变更信息。

### 行为变更



### 系统变量

| 变量名  | 修改类型    | 描述 |
|--------|------------------------------|------|
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |


### 配置参数

| 配置文件或组件 | 配置项 | 修改类型 | 描述 |
| -------- | -------- | -------- | -------- |
|  |  | |  |
|  |  |  | |


### 操作系统支持变更

升级 TiDB 前，请务必确保你的操作系统版本符合[操作系统及平台要求](/hardware-and-software-requirements.md#操作系统及平台要求)。



## 移除功能

* 以下为已移除的功能：

    

* 以下为计划在未来版本中移除的功能：

    * 从 v8.0.0 开始，TiDB Lightning 废弃了物理导入模式下的[旧版冲突检测](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#旧版冲突检测从-v800-开始已被废弃)策略，支持通过 [`conflict.strategy`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-任务配置) 参数统一控制逻辑导入和物理导入模式的冲突检测策略。旧版冲突检测的参数 [`duplicate-resolution`](/tidb-lightning/tidb-lightning-configuration.md) 将在未来版本中被移除。

## 废弃功能

以下为计划将在未来版本中废弃的功能：

* TiDB 在 v8.0.0 引入了系统变量 [`tidb_enable_auto_analyze_priority_queue`](/system-variables.md#tidb_enable_auto_analyze_priority_queue-从-v800-版本开始引入)，用于控制是否启用优先队列来优化自动收集统计信息任务的排序。在未来版本中，优先队列将成为自动收集统计信息任务的唯一排序方式，该系统变量将被废弃。
* TiDB 在 v7.5.0 引入了系统变量 [`tidb_enable_async_merge_global_stats`](/system-variables.md#tidb_enable_async_merge_global_stats-从-v750-版本开始引入)，用于设置 TiDB 使用异步方式合并分区统计信息，以避免 OOM 问题。在未来版本中，分区统计信息将统一使用异步方式进行合并，该系统变量将被废弃。
* 计划在后续版本重新设计[执行计划绑定的自动演进](/sql-plan-management.md#自动演进绑定-baseline-evolution)，相关的变量和行为会发生变化。
* TiDB 在 v8.0.0 引入了系统变量 [`tidb_enable_parallel_hashagg_spill`](/system-variables.md#tidb_enable_parallel_hashagg_spill-从-v800-版本开始引入)，用于控制 TiDB 是否支持并行 HashAgg 进行落盘。在未来版本中，该系统变量将被废弃。
* TiDB 在 v5.1 引入了系统变量 [`tidb_partition_prune_mode`](/system-variables.md#tidb_partition_prune_mode-从-v51-版本开始引入)，用于设置是否开启分区表动态裁剪模式。从 v8.5.0 开始，将该变量设置为 `static` 或 `static-only` 时会产生警告。在未来版本中，该系统变量将被废弃。
* TiDB Lightning 参数 [`conflict.max-record-rows`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-任务配置) 计划在未来版本中废弃，并在后续版本中删除。该参数将由 [`conflict.threshold`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-任务配置) 替代，即记录的冲突记录数和单个导入任务允许出现的冲突记录数的上限数保持一致。
* 从 v6.3.0 开始，分区表默认使用[动态裁剪模式](/partitioned-table.md#动态裁剪模式)，相比静态裁剪模式，动态裁剪模式支持 IndexJoin、Plan Cache 等特性，性能表现更好。在未来版本中，静态裁剪模式将被废弃。

## 改进提升

+ TiDB

    

+ TiKV

    

+ PD

    

+ TiFlash

    

+ Tools

    + Backup & Restore (BR)

       

    + TiDB Data Migration (DM)

        
## 错误修复

+ TiDB

    

+ TiKV

   

+ PD

    

+ TiFlash

    

+ Tools

    + Backup & Restore (BR)

        

    + TiCDC

        

    + TiDB Lightning

       

## 性能测试

如需了解 TiDB v9.0.0 的性能表现，你可以参考 TiDB Cloud Dedicated 集群的[性能测试报告](https://docs.pingcap.com/tidbcloud/v9.0-performance-highlights)（英文版）。

## 贡献者

感谢来自 TiDB 社区的贡献者们：

