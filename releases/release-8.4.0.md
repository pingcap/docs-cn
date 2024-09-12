---
title: TiDB 8.4.0 Release Notes
summary: 了解 TiDB 8.4.0 版本的新功能、兼容性变更、改进提升，以及错误修复。
---

# TiDB 8.4.0 Release Notes

发版日期：2024 年 xx 月 xx 日

TiDB 版本：8.4.0

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v8.4/quick-start-with-tidb) | [下载离线包](https://cn.pingcap.com/product-community/?version=v8.4.0-DMR#version-list)

在 8.4.0 版本中，你可以获得以下关键特性：

## 功能详情

### 可扩展性

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

### 性能

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

* 增加获取 TSO 的 RPC 模式，降低获取 TSO 的延迟 [#54960](https://github.com/pingcap/tidb/issues/54960) @[MyonKeminta](https://github.com/MyonKeminta) **tw@qiancai** <!--1893-->

    TiDB 在向 PD 请求 TSO 时，会将一段时间内的请求汇总起来并以同步的方式进行批处理，以减少 RPC (Remote Procedure Call) 请求数量从而降低 PD 负载。对于延迟敏感的场景，这种模式的性能并不理想。在 v8.4.0 中，TiDB 新增 TSO 请求的异步批处理模式，并提供不同的并发能力。异步模式可以降低获取 TSO 的延迟，但可能会增加 PD 的负载。你可以通过 [tidb_tso_client_rpc_mode](/system-variables.md#tidb_tso_client_rpc_mode-从-v840-版本开始引入) 变量设定获取 TSO 的 RPC 模式。

    更多信息，请参考[用户文档](/system-variables.md#tidb_tso_client_rpc_mode-从-v840-版本开始引入)。

* 优化 TiDB 的 Hash Join 算子实现效率（实验特性） [#55153](https://github.com/pingcap/tidb/issues/55153) [#53127](https://github.com/pingcap/tidb/issues/53127) @[windtalker](https://github.com/windtalker) @[xzhangxian1008](https://github.com/xzhangxian1008) @[XuHuaiyu](https://github.com/XuHuaiyu) @[wshwsh12](https://github.com/wshwsh12) **tw@qiancai** <!--1633-->

    在 v8.4.0 版本之前，TiDB 的 Hash Join 算子实现效率不高。从 v8.4.0 开始，TiDB 将对 Hash Join 算子进行重构优化，提升执行效率。在 v8.4.0 版本，该功能为实验特性，只有 INNER JOIN 和 OUTER JOIN 可以使用重构后的高性能 Hash Join 算子。当该功能启用时，执行器会根据高性能 Hash Join 算子对关联操作的支持情况，自动选择是否使用高性能 Hash Join 算子。你可以通过 [tidb_hash_join_use_new_impl](/system-variables.md#tidb_hash_join_use_new_impl-从-v840-版本开始引入) 变量控制是否启用高性能 Hash Join 算子。

    更多信息，请参考[用户文档](/system-variables.md#tidb_hash_join_use_new_impl-从-v840-版本开始引入)。

* 支持下推以下字符串函数到 TiKV [#17529](https://github.com/tikv/tikv/issues/17529) @[gengliqi](https://github.com/gengliqi) **tw@qiancai** <!--1716-->

    * `DATE_ADD()`
    * `DATE_SUB()`

  更多信息，请参考[用户文档](/functions-and-operators/expressions-pushed-down.md)。

### 稳定性

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

* 超出预期的查询 (Runaway Queries) 新增 "处理行数" 和 RU 作为阈值 [#issue号](链接) @[HuSharp](https://github.com/HuSharp) **tw@lilin90** <!--1800-->

    TiDB 在 v8.4.0 可以依据 "处理行数 (`PROCESSED_KEYS`)" 和 "Request Unit (`RU`)" 定义超出预期的查询。和"执行时间(`EXEC_ELAPSED`)"相比，新增阈值能够更准确的定义查询的资源消耗，避免整体性能下降时发生识别偏差。
    
    支持同时设置多个条件，满足任意条件即识别为 `Runaway Queries`。

    用户可以观测 [`Statement Summary Tables`](/statement-summary-tables.md) 中的几个对应字段 (`RESOURCE_GROUP`、`MAX_REQUEST_UNIT_WRITE`、`MAX_REQUEST_UNIT_READ`、`MAX_PROCESSED_KEYS`)，根据历史执行情况决定条件值的大小。

    更多信息，请参考[用户文档](/tidb-resource-control.md#管理资源消耗超出预期的查询-runaway-queries)。

* 超出预期的查询 (Runaway Queries) 支持切换资源组 [#issue号](链接) @[JmPotato](https://github.com/JmPotato) **tw@hfxsd** <!--1832-->

    v8.4.0 新增支持将 `Runaway Queries` 切换到指定资源组。在降低优先级 (COOLDOWN) 仍旧无法有效降低资源消耗的情况下，用户可以创建一个资源组 [`RESOURCE GROUP`](/tidb-resource-control.md#管理资源组)，并指定将识别到的查询切换到该资源组中，会话的后续查询仍旧会遵循原资源组。切换资源组的行为能够更精确地限制资源使用，对 `Runaway Queries` 的资源消耗做更加严格的控制。

    更多信息，请参考[用户文档](/tidb-resource-control.md#管理资源消耗超出预期的查询-runaway-queries)。

### 高可用

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

### SQL 功能

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

* 支持向量搜索功能（实验特性） [#54245](https://github.com/pingcap/tidb/issues/54245) [#9032](https://github.com/pingcap/tiflash/issues/9032) @[breezewish](https://github.com/breezewish) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger) @[EricZequan](https://github.com/EricZequan) @[zimulala](https://github.com/zimulala) @[JaySon-Huang](https://github.com/JaySon-Huang) **tw@qiancai** <!--1898-->

    向量搜索是一种优先考虑数据语义以提供相关结果的搜索方法，是 AI 和语言大模型的重要基础功能之一。通过向量索引，加速向量搜索的性能，数据库能够针对不同的距离函数快速查询相似向量，从而支撑 检索增强生成 (Retrieval-Augmented Generation, RAG)、语义搜索、推荐引擎等多种场景。
    TiDB 从 v8.4 版本开始，支持向量数据类型和向量索引，提供强大的向量搜索能力。TiDB 的向量数据类型支持最大 16383 维度，支持的距离函数包括：L2 距离（欧式距离）、余弦距离、负内积、L1 距离（曼哈顿距离）。
    使用时，创建包含向量类型的表并写入数据后，就可以进行向量搜索查询，或向量和传统关系数据的混合查询。
    TiDB 的向量索引依赖于 TiFlash。因此，使用向量索引前，需要先为你的 TiDB 集群增加 TiFlash 节点。

    更多信息，请参考[用户文档](/vector-search-overview.md)。
    
### 数据库管理

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

### 可观测性

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

* 在系统表中显示 TiDB 和 TiKV 的 CPU 时间 [#55542](https://github.com/pingcap/tidb/issues/55542) @[yibin87](https://github.com/yibin87) **tw@hfxsd** <!--1877-->

    [TiDB Dashboard](/dashboard/dashboard-intro.md) 的 [TOP SQL 页面](/dashboard/top-sql.md)能够展示 CPU 消耗高的 SQL 语句。v8.4.0 开始，TiDB 将 CPU 时间消耗信息加入系统表展示，与会话或 SQL 的其他指标并列，方便客户从多角度对高 CPU 消耗的操作进行观测。在实例 CPU 飙升 或集群读写热点的场景下，这些信息能够协助客户快速发现问题的原因。

    - [`STATEMENTS_SUMMARY`](/statement-summary-tables.md) 增加 `AVG_TIDB_CPU_TIME` 和 `AVG_TIKV_CPU_TIME`，显示单个 SQL 语句在历史上消耗的平均 CPU 时间。
    - [`INFORMATION_SCHEMA.PROCESSLIST`](/information-schema/information-schema-processlist.md) 增加 `TIDB_CPU` 和 `TIKV_CPU`，显示会话当前正在执行 SQL 的累计 CPU 消耗。
    - [慢日志](/analyze-slow-queries.md)中增加字段 `Tidb_cpu_time` 和 `Tikv_cpu_time`，显示被捕捉到的 SQL 语句的 CPU 时间。

    其中，TiKV 的 CPU 时间默认显示；采集 TiDB 的 CPU 时间会引入额外开销（大概在8%），因此仅在开启 [Top SQL 特性](/dashboard/top-sql.md)时，TiDB 的 CPU 时间才会显示为实际值，否则始终显示为 `0`。

* TOP SQL 可按 `Schema` 或 `Table` 维度聚合 [#issue号](链接) @[nolouch](https://github.com/nolouch) **tw@lilin90** <!--1878-->

    当前的 [TOP SQL](/dashboard/top-sql.md) 以 SQL 为单位来聚合 CPU 时间。如果 CPU 时间不是由少数几个 SQL 贡献，按 SQL 聚合并不能有效发现问题。从 v8.4.0 开始，用户可以选择按照 `Schema` 或 `Table` 聚合 CPU 时间。在多系统融合的场景下，新的聚合方式能够更有效地识别来自某个特定系统的负载变化，提升问题诊断的效率。

    更多信息，请参考[用户文档](/dashboard/top-sql.md)。

### 安全

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

### 数据迁移

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

## 兼容性变更

> **注意：**
>
> 以下为从 v8.3.0 升级至当前版本 (v8.4.0) 所需兼容性变更信息。如果从 v8.2.0 或之前版本升级到当前版本，可能也需要考虑和查看中间版本 Release Notes 中提到的兼容性变更信息。

### 行为变更

* 行为变更 1

### 系统变量

| 变量名  | 修改类型（包括新增/修改/删除）    | 描述 |
|--------|------------------------------|------|
| [`tidb_enable_inl_join_inner_multi_pattern`](/system-variables.md#tidb_enable_inl_join_inner_multi_pattern-从-v700-版本开始引入) |   修改  |   默认值改为 `ON`。当内表上有 `Selection` 或 `Projection` 算子时默认支持 Index Join  |
|        |                              |      |
|        |                              |      |
|        |                              |      |

### 配置文件参数

| 配置文件 | 配置项 | 修改类型 | 描述 |
| -------- | -------- | -------- | -------- |
|          |          |          |          |
|          |          |          |          |
|          |          |          |          |
|          |          |          |          |

### 系统表

## 离线包变更

## 废弃功能

* 以下为从 v8.4.0 开始已废弃的功能：

    * 废弃功能 1

* 以下为计划将在未来版本中废弃的功能：

    * TiDB 在 v8.0.0 引入了系统变量 [`tidb_enable_auto_analyze_priority_queue`](/system-variables.md#tidb_enable_auto_analyze_priority_queue-从-v800-版本开始引入)，用于控制是否启用优先队列来优化自动收集统计信息任务的排序。在未来版本中，优先队列将成为自动收集统计信息任务的唯一排序方式，系统变量 [`tidb_enable_auto_analyze_priority_queue`](/system-variables.md#tidb_enable_auto_analyze_priority_queue-从-v800-版本开始引入) 将被废弃。
    * TiDB 在 v7.5.0 引入了系统变量 [`tidb_enable_async_merge_global_stats`](/system-variables.md#tidb_enable_async_merge_global_stats-从-v750-版本开始引入)，用于设置 TiDB 使用异步方式合并分区统计信息，以避免 OOM 问题。在未来版本中，分区统计信息将统一使用异步方式进行合并，系统变量 [`tidb_enable_async_merge_global_stats`](/system-variables.md#tidb_enable_async_merge_global_stats-从-v750-版本开始引入) 将被废弃。
    * 计划在后续版本重新设计[执行计划绑定的自动演进](/sql-plan-management.md#自动演进绑定-baseline-evolution)，相关的变量和行为会发生变化。
    * TiDB 在 v8.0.0 引入了系统变量 [`tidb_enable_parallel_hashagg_spill`](/system-variables.md#tidb_enable_parallel_hashagg_spill-从-v800-版本开始引入)，用于控制 TiDB 是否支持并行 HashAgg 进行落盘。在未来版本中，系统变量 [`tidb_enable_parallel_hashagg_spill`](/system-variables.md#tidb_enable_parallel_hashagg_spill-从-v800-版本开始引入) 将被废弃。
    * TiDB Lightning 参数 [`conflict.max-record-rows`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-任务配置) 计划在未来版本中废弃，并在后续版本中删除。该参数将由 [`conflict.threshold`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-任务配置) 替代，即记录的冲突记录数和单个导入任务允许出现的冲突记录数的上限数保持一致。

* 以下为计划将在未来版本中移除的功能：

    * 从 v8.0.0 开始，TiDB Lightning 废弃了物理导入模式下的[旧版冲突检测](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#旧版冲突检测从-v800-开始已被废弃)策略，支持通过 [`conflict.strategy`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-任务配置) 参数统一控制逻辑导入和物理导入模式的冲突检测策略。旧版冲突检测的参数 [`duplicate-resolution`](/tidb-lightning/tidb-lightning-configuration.md) 将在未来版本中被移除。

## 改进提升

+ TiDB
  - 优化扫描大量数据时构造 BatchCop Task 的效率 [#55915](https://github.com/pingcap/tidb/issues/55915) [#55413](https://github.com/pingcap/tidb/issues/55413) @[wshwsh12](https://github.com/wshwsh12) **tw@caiqian** <!--1902-->
  - 优化 MEMDB 实现，降低事务中的写操作延时与 TiDB CPU 使用 [#55287](https://github.com/pingcap/tidb/issues/55287) @[you06](https://github.com/you06) **tw@hfxsd** <!--1892-->
  - 优化处理大量数据 DML 的性能 [#50215](https://github.com/pingcap/tidb/issues/50215) @[ekexium](https://github.com/ekexium) **tw@qiancai** <!--1860-->
  - 优化器估行的最小值为`1`，与其他数据库行为一致 [#47400](https://github.com/pingcap/tidb/issues/47400) @[terry1purcell](https://github.com/terry1purcell) **tw@Oreoxmt** <!--1929-->
  - 为日志表 [`mysql.tidb_runaway_queries`](/mysql-schema/mysql-schema.md#runaway-queries-相关系统表) 增加写入控制，降低并发大量写入引发的开销 [#issue号](链接) @[HuSharp](https://github.com/HuSharp) <!--1908--> **tw@lilin90** 
  - 当内表上有 `Selection` 或 `Projection` 算子时默认支持 Index Join [#issue号](链接) @[winoros](https://github.com/winoros) **tw@qiancai** <!--1860-->
  - 默认不允许使用 SQL 全量恢复数据到非空集群 [#55087](https://github.com/pingcap/tidb/issues/55087) @[BornChanger](https://github.com/BornChanger) **tw@Oreoxmt** <!--1711-->
  - 减少部分场景的 DELETE 操作从 TiKV 获取的列信息数量，降低 DELETE 操作的资源开销。[#issue号](链接) [winoros](https://github.com/winoros) **tw@Oreoxmt** <!--1798-->
  - 优化 Priority Queue 基于 Meta Cache V2 的运行效率 [#49972](https://github.com/pingcap/tidb/issues/49972) [Rustin170506](https://github.com/Rustin170506)  <!--1935-->
  
+ TiKV

+ PD

+ TiFlash

+ Tools

    + Backup & Restore (BR)

    + TiCDC

    + TiDB Data Migration (DM)

    + TiDB Lightning

    + Dumpling

    + TiUP

    + TiDB Binlog

## 错误修复

+ TiDB

+ TiKV

+ PD

+ TiFlash

+ Tools

    + Backup & Restore (BR)

    + TiCDC

    + TiDB Data Migration (DM)

    + TiDB Lightning

    + Dumpling

    + TiUP

    + TiDB Binlog

## 贡献者

感谢来自 TiDB 社区的贡献者们：
