---
title: TiDB 7.0.0 Release Notes
---

# TiDB 7.0.0 Release Notes

发版日期：2023 年 x 月 x 日

TiDB 版本：7.0.0

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v7.0/quick-start-with-tidb) | [下载离线包](https://cn.pingcap.com/product-community/)

在 7.0.0 版本中，你可以获得以下关键特性：

@yiwen92

## 功能详情

### 可扩展性

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接)

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

* TiFlash 引擎支持存算分离和对象存储（实验特性） [#6882](https://github.com/pingcap/tiflash/issues/6882) @[flowbehappy](https://github.com/flowbehappy)

    在 v7.0.0 之前的版本中，TiFlash 引擎以存算一体的方式部署，即 TiFlash 节点即是存储节点，也是计算节点；同时，TiFlash 节点只能使用本地存储。存算一体的部署方式使得 TiFlash 的计算能力和存储能力无法独立扩展。在 v7.0.0 版本中，TiFlash 引擎新增存算分离架构，并在存算分离架构下，支持兼容 S3 API 的对象存储。在 TiFlash 存算分离架构下，TiFlash 节点分为计算节点和写节点。这两种节点都可以单独扩缩容，独立调整计算或数据存储能力。TiFlash 引擎的存算分离架构不能和存算一体架构混合使用、相互转换，需要在部署 TiFlash 时进行相应的配置设定，确定使用存算分离架构或者存算一体架构。

    更多信息，请参考[用户文档](/tiflash/tiflash-disaggregated-and-s3.md)。

### 性能

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接)

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

* TiFlash 引擎支持 `Null-Aware Semi Join` 和 `Null-Aware Anti Semi Join` 算子 [#6674](https://github.com/pingcap/tiflash/issues/6674) @[gengliqi](https://github.com/gengliqi)

    `IN`、`NOT IN`、`=ANY`、`!= ALL` 算子引导的关联子查询会转化为 `Semi Join` 或 `Anti Semi Join`，从而提升计算性能。当转换后的 JOIN KEY 的列可能为 NULL 时，需要具有 Null-Aware 特性的 Join 算法，即需要 [`Null-Aware Semi Join`](/explain-subqueries#null-aware-semi-joinin-和--any-子查询) 和 [`Null-Aware Anti Semi Join`](/explain-subqueries#null-aware-anti-semi-joinnot-in-和--all-子查询) 算子。在 v7.0.0 之前的版本中，TiFlash 引擎不支持 `Null-Aware Semi Join` 和 `Null-Aware Anti Semi Join` 算子，所以这几种子查询无法直接下推至 TiFlash 引擎进行计算。在 v7.0.0 版本中，TiFlash 引擎支持了 `Null-Aware Semi Join` 和 `Null-Aware Anti Semi Join` 算子。当 SQL 包含这几种关联子查询，查询的表包含 TiFlash 副本，且启用 [MPP 模式](/tiflash/use-tiflash-mpp-mode.md)时，优化器将自动判断是否将 `Null-Aware Semi Join` 和 `Null-Aware Anti Semi Join` 算子下推至 TiFlash 引擎进行计算以提升整体性能。

    更多信息，请参考[用户文档](/tiflash/tiflash-supported-pushdown-calculations)。

* TiFlash 引擎支持 FastScan 功能 [#5252](https://github.com/pingcap/tiflash/issues/5252) @[hongyunyan](https://github.com/hongyunyan)

    TiFlash 引擎从 v6.3.0 版本发布了实验特性的快速扫描功能 (FastScan)。在 v7.0.0 版本中，该功能正式 GA。通过使用系统变量 [`tiflash_fastscan`](/system-variables.md#tiflash_fastscan-从-v630-版本开始引入) 可以启用快速扫描功能。快速扫描功能通过牺牲强一致性保证，可以大幅提升扫表性能。如果对应的表只有 INSERT 操作，没有 UPDATE/DELETE 操作，则快速扫描功能在提升扫表性能的同时，不会损失强一致性。

    更多信息，请参考[用户文档](/develop/dev-guide-use-fastscan.md)。

* TiFlash 引擎支持 Selection 延迟物化功能（实验特性） [#5829](https://github.com/pingcap/tiflash/issues/5829) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)

    当 SELECT 语句中包含过滤条件（ WHERE 子句）时，普通的处理方式是扫描所有数据后进行过滤。Selection 延迟物化功能可以先扫描过滤条件相关列数据，过滤得到符合条件的行后，再扫描这些行的其他列数据，继续后续计算，从而减少扫描 IO 和数据解析的计算量。在 v7.0.0 中，TiFlash 引擎支持 Selection 延迟物化功能，并通过 variable 控制是否启用该功能。当功能启用时，优化器会根据过滤条件的信息，自动判断是否使用 Selection 延迟物化功能。

    更多信息，请参考[用户文档]()。

* 非 prepared 语句的执行计划可以被缓存(实验特性) [#issue号](链接) @[qw4990](https://github.com/qw4990)

    执行计划缓存是提升并发 OLTP 负载能力的重要手段， TiDB 已经支持对 [prepared 语句的计划进行缓存](/sql-prepared-plan-cache.md)。 在 v7.0.0 中， 非 prepared 语句的执行计划也能够被缓存，使得执行计划缓存能够被应用在更广泛场景下，进而提升 TiDB 的并发处理能力。 

    这个功能目前默认关闭， 用户通过变量 [`tidb_enable_non_prepared_plan_cache`](/system-variables.md#tidb_enable_non_prepared_plan_cache) 打开。 出于稳定性考虑，在当前版本中，TiDB 开辟了一块新的区域用于缓存非 prepare 语句的执行计划，通过变量 [`tidb_non_prepared_plan_cache_size`](/system-variables.md#tidb_non_prepared_plan_cache_size) 设置缓存大小；另外，对 SQL 的模式也有一定的限制，具体参见[文档](/sql-non-prepared-plan-cache.md#限制)。

    更多信息，请参考[用户文档](/sql-non-prepared-plan-cache.md)。

### 稳定性

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接)

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

* TiFlash 引擎支持 Spill-to-disk 功能 [#5252](https://github.com/pingcap/tiflash/issues/5252) @[windtalker](https://github.com/windtalker)

    为了执行性能，TiFlash 引擎尽量将数据全部放在内存中运行。当数据量太大，超过内存总大小时，TiFlash 会终止查询，避免内存潮用引发系统崩溃。因此，TiFlash 可处理的数据量受限于内存大小。从 v7.0.0 版本开始，TiFlash 引擎支持 Spill-to-disk 功能，当算子使用内存超过一定阈值时，会自动将数据落盘，牺牲一定的性能，从而处理更多数据。

    更多信息，请参考[用户文档]()。

### 高可用

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接)

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

### SQL 功能

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接)

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

### 数据库管理

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接)

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

### 可观测性

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接)

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

### 安全

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接)

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

### 数据迁移

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接)

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

## 兼容性变更

> **注意：**
>
> 以下为从 v6.6.0 升级至当前版本 (v7.0.0) 所需兼容性变更信息。如果从 v6.5.0 或之前版本升级到当前版本，可能也需要考虑和查看中间版本 release notes 中提到的兼容性变更信息。

### MySQL 兼容性

* 兼容性 1

* 兼容性 2

### 系统变量

| 变量名  | 修改类型（包括新增/修改/删除）    | 描述 |
|--------|------------------------------|------|
|        |                              |      |
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

### 其他

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
