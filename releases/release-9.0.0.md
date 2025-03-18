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


### 数据库管理

* TiDB 索引推荐 [#12303](https://github.com/pingcap/tidb/issues/12303) @[qw4990](https://github.com/qw4990)

    索引设计在数据库性能优化中扮演非常重要的作用。自 v9.0.0 起，TiDB 在内核中加入了索引推荐。索引推荐能够分析高频查询的模式并推荐最佳索引策略，协助用户快速实现数据库性能调优，同时降低技术团队的学习门槛。

    通过 [`RECOMMEND INDEX`](/index-advisor.md) 语法，用户可以选择为某条 SQL 语句生成索引推荐，也可以自动读取历史负载中的高频 SQL 语句，做批量索引推荐。推荐结果保存在 `mysql.index_advisor_results` 中，可在后续随时查看。

    更多信息，请参考[用户文档](/index-advisor.md)。

### 可观测性

* TiDB Workload Repository [#58247](https://github.com/pingcap/tidb/issues/58247) @[xhebox](https://github.com/xhebox) @[henrybw](https://github.com/henrybw) @[wddevries](https://github.com/wddevries)

    很多高频更新的负载指标和状态信息被维护在实例的内存中，这些历史负载数据可以作为数据库的一部分持久化下来。主要用于以下目的：
    
    * **故障诊断：** 在对过往问题的诊断过程中，需要回顾历史活动和事件。持久化的负载数据可以帮助用户复盘过去某个时间段内的状态信息变化，找出异常点；或者精确定位某个数据库会话或 SQL 语句在特定时刻的具体行为。
    
    * **自动化运维：** 数据库自治是提升用户体验并降低使用门槛的必然趋势，而实现数据库自动调优需要历史数据作为支撑。基于持久化的历史工作负载数据，TiDB 可以逐步向自动化运维迈进，例如：索引推荐（Index Advisor）、统计信息推荐（Statistics Advisor）、SQL 绑定推荐（SQL Binding Advisor）等。

    在 v9.0.0 中，通过设置变量 [`tidb_workload_repository_dest`](/system-variables.md#tidb_workload_repository_dest) 启用 `Workload Repository`，TiDB 会把一部分内存表的快照持续写入 `workload_schema`，持久化到 TiKV 中。当前版本默认关闭。被持久化的内存表分为两类：

    * **存储累计指标的内存表**体积较大，快照和存储成本比较高，这些表会依据 [`tidb_workload_repository_snapshot_interval`](/system-variables.md#tidb_workload_repository_snapshot_interval) 的设置做批量快照，最小间隔 15 分钟。通过比较任意两个快照间指标的变化，得出这一段时间各个指标的增量。包括以下内存表：

        * [`INFORMATION_SCHEMA.TIDB_INDEX_USAGE`](/information-schema/information-schema-tidb-index-usage.md)
        * [`INFORMATION_SCHEMA.TIDB_STATEMENTS_STATS`](/statement-summary-tables.md) (由 `STATEMENTS_SUMMARY` 派生的内存表，计划在未来取代 `STATEMENTS_SUMMARY`。)
        * [`INFORMATION_SCHEMA.CLIENT_ERRORS_SUMMARY_BY_HOST`](/information-schema/client-errors-summary-by-host.md)
        * [`INFORMATION_SCHEMA.CLIENT_ERRORS_SUMMARY_BY_USER`](/information-schema/client-errors-summary-by-user.md)
        * [`INFORMATION_SCHEMA.CLIENT_ERRORS_SUMMARY_GLOBAL`](/information-schema/client-errors-summary-global.md)

    * **保存即时状态的内存表**刷新很快，通常体积不大，需要做很小间隔的快照才有作用。通过设置 [`tidb_workload_repository_active_sampling_interval`](/system-variables.md#tidb_workload_repository_active_sampling_interval) 的值指定时间间隔，默认为 5 秒。设置为 0 则关闭这个类型的快照。被持久化的这类内存表包括：

        * [`INFORMATION_SCHEMA.PROCESSLIST`](/information-schema/information-schema-processlist.md)
        * [`INFORMATION_SCHEMA.DATA_LOCK_WAITS`](/information-schema/information-schema-data-lock-waits.md)
        * [`INFORMATION_SCHEMA.TIDB_TRX`](/information-schema/information-schema-tidb-trx.md)
        * [`INFORMATION_SCHEMA.MEMORY_USAGE`](/information-schema/information-schema-memory-usage.md)
        * [`INFORMATION_SCHEMA.DEADLOCKS`](/information-schema/information-schema-deadlocks.md)
    
    `Workload Repository` 中的数据会被自动清理，默认保存 7 天。通过设置 [`tidb_workload_repository_retention_days`](/system-variables.md#tidb_workload_repository_retention_days) 修改保存时间。

    通过持久化数据库的历史工作负载，TiDB 可以更好地进行故障排查和优化推荐，并在未来推出一系列围绕历史负载的自动化工具，提升数据库运维和诊断的用户体验。

    更多信息，请参考[用户文档](/workloadrepo.md)。

* SQL 跨可用区流量观测 [#57543](https://github.com/pingcap/tidb/issues/57543) @[nolouch](https://github.com/nolouch) @[yibin87](https://github.com/yibin87)

    跨可用区 (Avaiable Zone) 部署能够提升集群的容灾能力。在云服务环境中，这种部署方式会产生额外的网络流量费用，例如亚马逊 AWS 会对跨区域和跨可用区的流量计费。对于运行在云服务上的 TiDB 集群来说，更精确监控和分析网络流量变得尤为重要。

    自 v9.0.0 开始，TiDB 会记录 SQL 处理的网络流量，并区分跨可用区的流量。相关记录写入 [Statements 日志](/statement-summary-tables.md) 和 [慢日志](/identify-slow-queries.md)。这个特性主要用于协助用户跟踪 TiDB 集群内部的主要数据传输，分析跨区域的流量产生的原因，从而更好地理解和控制相关成本。
    
    需要注意的是，当前版本只观测 **查询在集群内** (TiDB, TiKV, TiFlash) 之间产生的网络传输，不包括 DML 和 DDL；另外，所记录的流量数据为解包后的流量，和实际物理流量会有差异。并不能作为网络计费的依据。

    更多信息，请参考[用户文档]()。

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

