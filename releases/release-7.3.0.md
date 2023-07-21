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

<!-- 请将 **tw@xxx** 中的 xxx 替换为这个 feature 的 writer 的 ID，这个标记会在发布前删除-->

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

### 性能

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

* TiFlash 支持副本选择策略 [#44106](https://github.com/pingcap/tidb/issues/44106) @[XuHuaiyu](https://github.com/XuHuaiyu) **tw@qiancai** <!--1394-->

    在 v7.3.0 版本之前，TiFlash 尽量使用所有节点的副本进行数据扫描及 MPP 计算，以提供最强大的性能。在 v7.3.0 版本中，TiFlash 引入副本选择策略，可以根据节点区域属性，选择特定的副本，并调度部分节点进行数据扫描及 MPP 计算。当集群部署在超过一个机房，并且每个机房都拥有完整的 TiFlash 数据副本时，可以只选择当前机房的 TiFlash 副本，在当前机房的 TiFlash 节点中进行数据扫描和 MPP 计算，避免大量跨机房的网络数据传输。新增系统变量 [`tiflash_replica_read`](/system-variables.md#tiflash_replica_read) 用于设定节点选择策略。

    更多信息，请参考[用户文档](/system-variables.md#tiflash_replica_read)。

### 稳定性

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

* 允许为 DDL 任务指定 TiDB 实例 [#issue号](链接) @[ywqzzy](https://github.com/ywqzzy)

    在繁忙的系统中，运行繁重的 DDL 工作会消耗大量计算资源，从而影响在线业务的服务质量。 TiDB 在新版本提供了对 TiDB 节点添加标记的能力，借助标签把 DDL 任务制定到部分 TiDB 节点，从而能够将 DDL 操作与在线业务的 TiDB 节点分离，提升在线业务的稳定性，保证业务的响应时间。 

    更多信息，请参考[用户文档](链接)。

### 高可用

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

### SQL 功能

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

* List、List COLUMNS 分区表支持默认分区 [#20679](https://github.com/pingcap/tidb/issues/20679) @[mjonss](https://github.com/mjonss) @[bb7133](https://github.com/bb7133) **tw@caiqian** <!--1234-->

    List、List COLUMNS 分区表需要为分区指定分区条件。如果 INSERT 语句要插入的数据不匹配任何分区条件，则该语句将执行失败或不符合分区条件的数据被忽略。在 v7.3.0 版本，TiDB 为 List、List COLUMNS 分区表引入默认分区。在创建默认分区后，如果 INSERT 语句插入的数据不匹配任何分区条件，则数据将被写入默认分区。默认分区功能可以提升 List 分区和 List COLUMNS 分区的使用便捷性，避免不符合分区的数据导致 INSERT 语句执行失败或者数据被忽略的情况。该功能自动开启。

    更多信息，请参考[用户文档](/partitioned-table.md#list-分区)。

### 数据库管理

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

### 可观测性

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

* 显示统计信息收集的进度 [#issue号](链接) @[hawkingrei](https://github.com/hawkingrei)

    对大表的统计信息收集经常会持续比较长的时间。 在过去的版本里，用户无从得知统计信息收集的进度，进而没法预测完成时间。在 v7.3.0 中，TiDB 加入了对统计信息收集进度的信息展示， 能够显示各个子任务的总体工作量，当前进度，以及对完成时间的预测。在大规模数据导入、SQL 性能优化等场景下，用户能够了解整体任务进展，提升用户体验。 

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
> 以下为从 v7.2.0 升级至当前版本 (v7.3.0) 所需兼容性变更信息。如果从 v7.1.0 或之前版本升级到当前版本，可能也需要考虑和查看中间版本 release notes 中提到的兼容性变更信息。

### 行为变更

<!-- 此小节包含 MySQL 兼容性变更-->

* 兼容性 1

* 兼容性 2

### 系统变量

| 变量名 | 修改类型 | 描述 |
|---|----|------|
|  | 新增/删除/修改 |  |
|  | 新增/删除/修改 |  |
|  | 新增/删除/修改 |  |
|  | 新增/删除/修改 |  |
|  | 新增/删除/修改 |  |

### 配置文件参数

| 配置文件 | 配置项 | 修改类型 | 描述 |
| -------- | -------- | -------- | -------- |
|  | | 新增/删除/修改 | |
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

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ TiKV

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ PD

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ TiFlash

    - 支持新的 DTFile 格式版本，减少物理文件数量（实验特性） [#7595](https://github.com/pingcap/tiflash/issues/7595) @[hongyunyan](https://github.com/hongyunyan) **tw@caiqian** <!--1234-->
    - 提升 TiFlash 在存算分离架构下的性能和稳定性（实验特性） [#6882](https://github.com/pingcap/tiflash/issues/6882)  @[JaySon-Huang](https://github.com/JaySon-Huang) @[breezewish](https://github.com/breezewish) @[JinheLin](https://github.com/JinheLin) **tw@caiqian** <!--1234-->
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

+ [Contributor 1]()
