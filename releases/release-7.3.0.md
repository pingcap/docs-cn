---
title: TiDB 7.3.0 Release Notes
summary: 了解 TiDB 7.3.0 版本的新功能、兼容性变更、改进提升，以及错误修复。
---

# TiDB 7.3.0 Release Notes

发版日期：2023 年 x 月 x 日

TiDB 版本：7.3.0

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v7.3/quick-start-with-tidb) | [下载离线包](https://cn.pingcap.com/product-community/)

在 7.3.0 版本中，你可以获得以下关键特性：

<!-- to be added -->


## 功能详情

### 可扩展性

### 性能

* TiFlash 支持副本选择策略 [#44106](https://github.com/pingcap/tidb/issues/44106) @[XuHuaiyu](https://github.com/XuHuaiyu) **tw@qiancai** <!--1394-->

    在 v7.3.0 之前，当 TiFlash 进行数据扫描和 MPP 计算时，会尽可能使用其所有节点的副本，以提供最强大的性能。从 v7.3.0 起，TiFlash 引入副本选择策略，该策略由系统变量 [`tiflash_replica_read`](/system-variables.md#tiflash_replica_read-从-v730-版本开始引入) 控制，可以根据节点的[区域属性](/schedule-replicas-by-topology-labels.md#设置-tidb-的-labels可选)选择特定的副本，调度部分节点进行数据扫描及 MPP 计算。

    当集群部署在多个机房且每个机房都拥有完整的 TiFlash 数据副本时，你可以设置该策略只选择使用当前机房的 TiFlash 副本，即在当前机房的 TiFlash 节点中进行数据扫描和 MPP 计算，从而避免大量跨机房的网络数据传输。

    更多信息，请参考[用户文档](/system-variables.md/system-variables.md#tiflash_replica_read-从-v730-版本开始引入)。

* TiFlash 支持节点内的 Runtime Filter [#40220](https://github.com/pingcap/tidb/issues/40220) @[elsa0520](https://github.com/elsa0520) **tw@ran-huang** <!--1130-->

    Runtime Filter 是一种在查询规划时生成的动态取值的谓词。在表连接的过程中，这些动态谓词能够进一步过滤掉不满足条件的行，减少扫描时间和网络开销，提升表连接的效率。自 v7.3.0 起，TiFlash 支持节点内的 Runtime Filter，提升了数据分析类查询的整体性能，在部分 TPC-DS 查询中可达到 10% ~ 50% 的性能提升。

    该特性在 v7.3.0 默认关闭。要启用此功能，需将变量 [`tidb_runtime_filter_mode`](#tidb_runtime_filter_mode-从-v720-版本开始引入) 设置为 `LOCAL`。

    更多信息，请参考[用户文档](/runtime-filter.md)。

* TiFlash 支持执行公共表表达式 (CTE)（实验特性）[#43333](https://github.com/pingcap/tidb/issues/43333) @[winoros](https://github.com/winoros) **tw@ran-huang** <!--1244-->

    在 v7.3.0 版本之前，TiFlash 的 MPP 引擎默认无法执行包含 CTE 的查询，你需要通过系统变量 [`tidb_opt_force_inline_cte`](/system-variables.md#tidb_opt_force_inline_cte-从-v630-版本开始引入) 将 CTE inline 展开，达到让查询尽可能在 MPP 框架下执行的效果。在 v7.3.0 中，TiFlash MPP 引擎支持执行包含 CTE 的查询，无需将 CTE inline 展开也可以尽可能地在 MPP 框架中执行查询。在 TPC-DS 基准测试中，与 inline 的执行方式相比，该功能可以将包含 CTE 的查询的总执行速度提升 20%。
    
    该功能为实验特性，默认关闭，由变量 [`tidb_opt_enable_mpp_shared_cte_execution`](/system-variables.md#tidb_opt_enable_mpp_shared_cte_execution-从-v720-版本开始引入) 控制。

### 稳定性

* 新增部分优化器提示 [#45520](https://github.com/pingcap/tidb/issues/45520) @[qw4990](https://github.com/qw4990) **tw@ran-huang** <!--1457-->

    TiDB 在 v7.3.0 新增了几个优化器提示，用来控制表之间的连接方式，包括：
   
    - [`INDEX_JOIN()`](链接) 选择 Index Nested Loop Join，利用索引过滤并将结果集作为内表连接。
    - [`NO_HASH_JOIN()`](链接) 选择哈希连接以外的连接方式。
    - [`NO_INDEX_HASH_JOIN()`](链接) 选择除 [Index Nested Loop Hash Join](/optimizer-hints#inl_hash_join) 以外的连接方式。

    更多信息，请参考[用户文档](/optimizer-hints)。

* 手工标记资源使用超出预期的查询 (实验特性) [#43691](https://github.com/pingcap/tidb/issues/43691) @[Connor1996](https://github.com/Connor1996) @[CabinfeverB](https://github.com/CabinfeverB) **tw@hfxsd** <!--1446-->

    在 v7.2.0 中，TiDB 对资源使用超出预期的查询 (Runaway Queries) 实施自动管理，运行时间超过预期的查询能够被自动降级或取消。在实际运行时，只依靠规则无法筛覆盖所有情况。 因此，在 v7.3.0 中，TiDB 补充了手工标记查询的能力。 利用新增的命令 [`QUERY WATCH`]()，用户可以根据 SQL 的文本、SQL Digest、或者执行计划对查询进行标记，命中的查询可以被降级或取消。

    手工标记 Runaway Queries 的能力，为数据库中突发的性能问题提供了有效的干预手段。针对由查询引发的性能问题，在找到问题根本原因之前，能够快速缓解其对整体性能的影响，提升系统服务质量。 

    更多信息，请参考[用户文档](/tidb-resource-control#管理资源消耗超出预期的查询-runaway-queries)。

### 高可用

### SQL 功能

* List 和 List COLUMNS 分区表支持默认分区 [#20679](https://github.com/pingcap/tidb/issues/20679) @[mjonss](https://github.com/mjonss) @[bb7133](https://github.com/bb7133) **tw@qiancai** <!--1342-->

    当使用 `INSERT` 语句向 List 或 List COLUMNS 分区表插入数据时，这些数据需要满足分区表指定的分区条件。如果要插入的数据不匹配任何分区条件，该语句将执行失败或不符合分区条件的数据被忽略。

    在 v7.3.0 中，List 和 List COLUMNS 分区表支持默认分区功能。在创建默认分区后，如果要插入的数据不匹配任何分区条件，则数据将被写入默认分区。默认分区功能可以提升 List 分区和 List COLUMNS 分区的使用便捷性，避免不符合分区条件的数据导致 `INSERT` 语句执行失败或者数据被忽略。

    更多信息，请参考[用户文档](/partitioned-table.md#list-分区)。

### 数据库管理

### 可观测性

* 显示统计信息收集的进度 [#issue号](链接) @[hawkingrei](https://github.com/hawkingrei) **tw@Oreoxmt** <!--1380-->

    对大表的统计信息收集经常会持续比较长的时间。在过去的版本里，用户无从得知统计信息收集的进度，进而没法预测完成时间。在 v7.3.0 中，TiDB 加入了对统计信息收集进度的信息展示，能够显示各个子任务的总体工作量、当前进度、以及对完成时间的预测。在大规模数据导入、SQL 性能优化等场景下，用户能够了解整体任务进展，提升用户体验。 

    更多信息，请参考[用户文档](链接)。

* Plan Replayer 支持导出历史统计信息 [#45038](https://github.com/pingcap/tidb/issues/45038) @[time-and-fate](https://github.com/time-and-fate) **tw@ran-huang** <!--1445-->

    自 v7.3.0 起，通过新增的 [`dump with stats as of timestamp`](/sql-plan-replayer.md) 子句，Plan Replayer 能够导出指定 SQL 相关对象在指定时间点的统计信息。在执行计划问题的诊断过程中，通过对历史统计信息的准确抓取，能够更精确地分析出执行计划在问题发生的时间点是如何生成的，从而找到问题的根本原因，大大提升执行计划问题的诊断效率。 

    更多信息，请参考[用户文档](/sql-plan-replayer.md)。

### 安全

### 数据迁移

* Lightning 引入新版冲突数据检测与处理的能力 [#41629](https://github.com/pingcap/tidb/issues/41629) @[lance6716](https://github.com/lance6716) **tw@hfxsd** <!--1296-->
     
    之前的版本 Lightning 逻辑导入和物理导入模式都有各自的冲突检测和处理的方式，配置较为复杂且不利于用户理解。同时使用物理导入模式，冲突的数据无法通过 replace 和 ignore 策略来处理。新版的冲突检测和处理方式，逻辑导入和物理导入都是用同一套冲突检测和处理方式即遇到冲突数据报错，或者 replace 以及 ignore 掉冲突数据。同时还支持用户设置冲突记录的上限，如处理多少冲突记录后任务中断退出，用户也可以让程序记录哪些数据发生了冲突，方便用户排查。

    在明确所需导入数据有较多的冲突数据时，推荐使用新版的冲突检测和处理策略，会有更好的性能。注意新、旧版冲突策略互斥使用，会在未来废弃掉旧版冲突检测和处理策略。
    
    更多信息，请参考[用户文档](链接)。
    
* Lightning 支持 Partitioned Raft KV（实验特性） [#15069](https://github.com/tikv/tikv/pull/15069) @[GMHDBJD](https://github.com/GMHDBJD) **tw@hfxsd** <!--1507-->
    
    该版本 Lightning 支持了 Partitioned Raft KV ，当用户使用了 Partitioned Raft KV 特性后，能提升 Lightning 导入数据的性能。
    
    更多信息，请参考[用户文档](链接)。
    
* Lightning 引入新的参数"enable-diagnose-log" 用于打印更多的诊断日志，方便定位问题 [#45497](https://github.com/pingcap/tidb/issues/45497) @[D3Hunter](https://github.com/D3Hunter) **tw@hfxsd** <!--1517-->
    
    默认情况下，此功能未启用，只会打印包含 "lightning/main" 的日志。当启用时，将打印所有包（包括 "client-go" 和 "tidb"）的日志，以帮助诊断与 "client-go" 和 "tidb" 相关的问题。
    
    更多信息，请参考[用户文档](链接)。

## 兼容性变更

> **注意：**
>
> 以下为从 v7.2.0 升级至当前版本 (v7.3.0) 所需兼容性变更信息。如果从 v7.1.0 或之前版本升级到当前版本，可能也需要考虑和查看中间版本 release notes 中提到的兼容性变更信息。

### 行为变更

<!-- 此小节包含 MySQL 兼容性变更-->

* TiDB Lightning **tw@hfxsd**

    - 逻辑导入模式插入冲突数据时执行的操作，默认配置从 on-duplicate = "replace" 改为 on-duplicate = "error" 即遇到冲突数据即报错。
    - TiDB Lightning 停止迁移任务之前能容忍的最大非严重 (non-fatal errors) 错误数的参数 "max-error" 不再包含导入数据冲突的上限。而是由新的参数 "conflict.threshold" 来控制可容忍的最大冲突的记录数。

* 兼容性 2

### 系统变量

| 变量名 | 修改类型 | 描述 |
|---|----|------|
|  | 新增/删除/修改 |  |
|  | 新增/删除/修改 |  |
|  | 新增/删除/修改 |  |
|  | 新增/删除/修改 |  |

### 配置文件参数

| 配置文件 | 配置项 | 修改类型 | 描述 |
| -------- | -------- | -------- | -------- |
|TiDB Lightning  | conflict.strategy | 新增 |TiDB Lightning 新版冲突检测与处理的策略，包含”“， error，replace，ignore 四种策略，分别表示不做冲突检测，遇到冲突数据即报错并停止导入，遇到冲突记录 replace 掉已有的冲突记录，遇到冲突记录 ignore 掉需要插入的该条冲突记录。默认值为 ” “， 即不做冲突检测 |
|TiDB Lightning  | conflict.threshold | 新增 |TiDB Lightning 新版冲突检测与处理策略允许的冲突上限，onflict.strategy="error" 时默认值为 0，当onflict.strategy="replace”/“ignore" 时默认值为 maxint |
|TiDB Lightning  | conflict.max-record-rows | 新增 |TiDB Lightning 新版冲突检测与处理策略，用于记录在数据导入过程中遇到的冲突记录，并允许设置最大上限，默认值为 100 |
|TiDB Lightning  | `tikv-importer.parallel-import` | 新增 | TiDB Lightning 并行导入参数。用于替代原有的 `tikv-importer.incremental-import` 参数，因为原有的参数容易被误认为是增量导入的参数而导致误用。 **tw:qiancai** <!--1516--> |
|TiDB Lightning  | tikv-importer.incremental-import | 删除 | TiDB Lightning 并行导入参数的旧名称，因为该参数名会被误认为增量导入的参数而误用，因此用新的参数名 tikv-importer.parallel-import 代替，且如果用户传入旧的参数会被自动转成新的参数名|
|BR  | azblob.encryption-scope | 新增 |BR 为外部存储 Azure Blob Storage 提供加密范围支持 |
|BR  | azblob.encryption-key | 新增 |BR 为外部存储 Azure Blob Storage 提供加密密钥支持 |

|  | | 新增/删除/修改 | |
|  | | 新增/删除/修改 | |
|  | | 新增/删除/修改 | |
|  | | 新增/删除/修改 | |
|  | | 新增/删除/修改 | |

## 废弃功能

- note
- note

## 改进提升

+ TiDB

    - 游标 (Cursor) 结果过大时，写入 TiDB 临时磁盘空间从而避免OOM [#43233](https://github.com/pingcap/tidb/issues/43233) @[YangKeao](https://github.com/YangKeao) <!--1430-->
    - EXPLAIN 新增开关用以展示在优化期间被执行的子查询 [#22076](https://github.com/pingcap/tidb/issues/22076) @[winoros](https://github.com/winoros] **tw@Oreoxmt** <!--983-->
    - 在启用 [`Global Kill`](/tidb-configuration-file#enable-global-kill-从-v610-版本开始引入) 的情况下，可以通过 Ctrl+C 终止当前会话。 [#8854](https://github.com/pingcap/tidb/issues/8854) @[pingyu](https://github.com/pingyu)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ TiKV

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ PD

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ TiFlash

    - 支持新的 DTFile 格式版本，减少物理文件数量（实验特性） [#7595](https://github.com/pingcap/tiflash/issues/7595) @[hongyunyan](https://github.com/hongyunyan) **tw@qiancai** <!--？-->
    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ Tools

    + Backup & Restore (BR)

        - 为外部存储 Azure Blob Storage 提供加密范围和加密密钥的支持 [#45025](https://github.com/pingcap/tidb/issues/45025) @[Leavrth](https://github.com/Leavrth) **tw@Oreoxmt** <!--1385-->
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiCDC

        - Kafka Sink 支持在消息过大时只发送 Handle Key 数据，减少数据大小 [#9382](https://github.com/pingcap/tiflow/issues/9382) @[3AceShowHand](https://github.com/3AceShowHand) **tw@ran-huang** <!--1406-->
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiDB Data Migration (DM)

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiDB Lightning

        - 更新 TiDB Lightning 并行导入的参数名称从 "tikv-importer.incremental-import" 变更为 “tikv-importer.parallel-import” ，避免用户误认为是增量导入而误用该参数。 [#45501](https://github.com/pingcap/tidb/issues/45501) @[lyzx2001](https://github.com/lyzx2001) **tw@hfxsd**
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiUP

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

## 错误修复

+ TiDB

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ TiKV

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ PD

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ TiFlash

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ Tools

    + Backup & Restore (BR)

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiCDC

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiDB Data Migration (DM)

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiDB Lightning

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiUP

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

## 贡献者

感谢来自 TiDB 社区的贡献者们：

+ [Contributor 1]()
