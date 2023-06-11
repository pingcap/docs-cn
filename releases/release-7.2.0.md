---
title: TiDB 7.2.0 Release Notes
summary: 了解 TiDB 7.2.0 版本的新功能、兼容性变更、改进提升，以及错误修复。
---

# TiDB 7.2.0 Release Notes

发版日期：2023 年 x 月 x 日

TiDB 版本：7.2.0

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v7.2/quick-start-with-tidb) | [下载离线包](https://cn.pingcap.com/product-community/)

在 7.2.0 版本中，你可以获得以下关键特性：

<!-- 关键特性表格 placeholder-->

## 功能详情

### 可扩展性

<!-- 请将 **tw@xxx** 中的 xxx 替换为这个 feature 的 writer 的 ID，这个标记会在发布前删除-->

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

### 性能

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

* 新增支持下推两个[窗口函数](/tiflash/tiflash-supported-pushdown-calculations.md) 至 TiFlash [#7427](https://github.com/pingcap/tiflash/issues/7427)  @[xzhangxian1008](https://github.com/xzhangxian1008) **tw@qiancai** <!--1310-->

    * `FIRST_VALUE`
    * `LAST_VALUE`

* TiFlash 支持副本选择策略 [#44106](https://github.com/pingcap/tidb/issues/44106) @[XuHuaiyu](https://github.com/XuHuaiyu) **tw@qiancai** <!--1394-->

    在 v7.2.0 版本之前，TiFlash 尽量使用所有节点的副本进行数据扫描及 MPP 计算，以提供最强大的性能。在 v7.2.0 版本中，TiFlash 引入副本选择策略，可以根据节点区域属性，选择特定的副本，并调度部分节点进行数据扫描及 MPP 计算。当集群部署在超过一个机房，并且每个机房都拥有完整的 TiFlash 数据副本时，可以只选择当前机房的 TiFlash 副本，在当前机房的 TiFlash 节点中进行数据扫描和 MPP 计算，避免大量跨机房的网络数据传输。新增系统变量 [`tiflash_replica_read`](/system-variables.md#tiflash_replica_read) 用于设定节点选择策略。

    更多信息，请参考[用户文档](/system-variables.md#tiflash_replica_read)。

* 提升统计信息收集的性能 [#issue号](链接) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes)

    v7.2.0 优化了统计信息的收集策略，会选择跳过一部分重复的信息，以及对优化器价值不高的信息，提升统计信息收集的整体速度达 30% 。 这个提升有利于 TiDB 对数据库对象的统计信息进行更及时的更新，使得生成的执行计划更准确， 从而达到提升数据库整体性能的目的。

### 稳定性

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

* 自动管理资源超出预期的查询 (实验特性) [#issue号](链接) @[nolouch](https://github.com/nolouch) @[glorv](https://github.com/glorv)  @[Connor1996](https://github.com/Connor1996) @[JmPotato](https://github.com/JmPotato) @[CabinfeverB](https://github.com/CabinfeverB) @[HuSharp](https://github.com/HuSharp)

    突发的 SQL 性能问题引发数据库整体性能下降，是数据库稳定性最常见的挑战。 造成 SQL 性能问题的原因有很多， 有可能是未经充分测试的新 SQL，数据量剧烈变化，执行计划突变等等，这些问题很难从源头上完全规避。 TiDB 在 v7.2.0 加入了对资源超出预期的查询的管理能力，在上述问题发生时，能够快速降低影响范围。 

    用户可以针对某个资源组 (Resource Group) 设置查询的最长执行时间。 当查询的执行时间超过设置时， 自动降低查询的优先级或者取消查询。  用户还可以设置在一段时间内通过文本立即匹配已经识别出的查询， 从而避免问题查询的并发度太高时，在识别阶段就造成大量消耗的情况。 

    对资源超出预期查询的自动管理， 为用户提供了有效的手段，快速应对突发的查询性能问题，降低问题对数据库整体性能的影响，从而提升数据库的稳定性。 

    更多信息，请参考[用户文档](链接)。
    

### 高可用

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

### SQL 功能

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

* TiDB 支持完整的分区类型管理功能 [#42728](https://github.com/pingcap/tidb/issues/42728) @[mjonss](https://github.com/mjonss) **tw@qiancai** <!--1370-->

    在 v7.2.0 之前，TiDB 中的分区表不能调整分区类型。从 v7.2.0 开始，TiDB 支持将分区表修改为非分区表、将非分区表修改为分区表、修改分区类型功能。你可以根据需要灵活调整表的分区类型、数量。例如，通过 `ALTER TABLE t PARTITION BY ...` 语句修改分区类型。

    更多信息，请参考[用户文档](/partitioned-table.md#分区管理)。

* LIST 分区表支持 DEFAULT 分区功能 [#42728](https://github.com/pingcap/tidb/issues/42728) @[mjonss](https://github.com/mjonss) **tw@qiancai** <!--1342-->

    LIST 分区表必须指定所有的分区，不满足任何分区条件的数据，无法正常写入该表。从 v7.2.0 开始，TiDB 支持 [默认 LIST 分区](/partitioned-table.md#list-分区) 功能。该功能启用时，所有不符合已有 LIST 分区的数据将被保存在默认 LIST 分区中。通过系统变量 `tidb_enable_default_list_partition` 控制是否启用默认 LIST 分区gonna。
    
    更多信息，请参考[用户文档](/partitioned-table.md#list-分区)。

### 数据库管理

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

### 可观测性

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

* 为统计信息收集增加进度展示 [#issue号](链接) @[hawkingrei](https://github.com/hawkingrei)

    对大表的统计信息收集经常会持续比较长的时间。 在过去的版本里，用户无从得知统计信息收集的进度，进而没法预测完成时间。 在 v7.2.0 中， TiDB 加入了对统计信息收集进度的信息展示。 新加入 [`SHOW ANALYZE SUMMARY`]() 命令，能够以表或分区为单位展示总体工作量，当前进度，以及对完成时间的预测。 在大规模数据导入、SQL 性能优化等场景下，用户能够了解整体任务进展，提升用户体验。 

    更多信息，请参考[用户文档](链接)。

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
> 以下为从 v7.1.0 升级至当前版本 (v7.2.0) 所需兼容性变更信息。如果从 v7.0.0 或之前版本升级到当前版本，可能也需要考虑和查看中间版本 release notes 中提到的兼容性变更信息。

### 行为变更

<!-- 此小节包含 MySQL 兼容性变更-->

* 兼容性 1

* 兼容性 2

### 系统变量

| 变量名  | 修改类型（包括新增/修改/删除）    | 描述 |
|--------|------------------------------|------|
| [`tidb_remove_orderby_in_subquery`](/system-variables.md#tidb_remove_orderby_in_subquery-从-v610-版本开始引入)| 修改 | 从 v7.2.0 及之后版本中默认为 `ON`， 即优化器改写会考虑消除子查询中的排序操作。 |
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

## 废弃功能

## 改进提升

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

- [贡献者 GitHub ID]()