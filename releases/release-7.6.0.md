---
title: TiDB 7.6.0 Release Notes
summary: 了解 TiDB 7.6.0 版本的新功能、兼容性变更、改进提升，以及错误修复。
---

# TiDB 7.6.0 Release Notes

发版日期：202x 年 x 月 x 日

TiDB 版本：7.6.0

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v7.6/quick-start-with-tidb) | [下载离线包](https://cn.pingcap.com/product-community/?version=v7.6.0-DMR#version-list)

在 7.6.0 版本中，你可以获得以下关键特性：

## 功能详情

### 可扩展性

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

### 性能

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

* TiDB 提供支持落盘的并发 HashAgg 算法（实验特性） [#35637](https://github.com/pingcap/tidb/issues/35637) @[xzhangxian1008](https://github.com/xzhangxian1008) **tw@qiancai** <!--1365-->

    在之前的版本中，TiDB 的 HashAgg 算子的并发算法不支持落盘，所有数据必须在内存中进行处理。这导致数据量较大、超过内存总量，需要使用 HashAgg 的落盘功能时，必须选择非并发算法，从而无法通过并发提升性能。在 7.6.0 版本中，TiDB 提供支持落盘的并发 HashAgg 算法。在任意并发条件下，HashAgg 算子都可以根据内存使用情况自动触发数据落盘，从而兼顾性能和处理数据量。目前，该功能作为实验特性，引入变量 `tidb_enable_concurrent_hashagg_spill` 控制是否启用支持落盘的并发 HashAgg 算法。当该变量设置为 `true` 时，HashAgg 将使用支持落盘的并发算法。该变量将在功能正式发布时废弃。

    更多信息，请参考[用户文档](链接)。

* 支持下推字符串函数 `LOWER` 到 TiKV [#48170](https://github.com/pingcap/tidb/issues/48170) @[gengliqi](https://github.com/gengliqi) **tw@qiancai** <!--1607-->

    * `LOWER`

    更多信息，请参考[用户文档](/functions-and-operators/expressions-pushed-down.md)。

* 新增支持下推以下 JSON 函数到 TiFlash [#48350](https://github.com/pingcap/tidb/issues/48350) [#48986](https://github.com/pingcap/tidb/issues/48986) [#48994](https://github.com/pingcap/tidb/issues/48994) @[SeaRise](https://github.com/SeaRise) @[yibin87](https://github.com/yibin87) **tw@qiancai** <!--1608-->

    * `JSON_UNQUOTE`
    * `JSON_ARRAY`
    * `JSON_DEPTH`

    更多信息，请参考[用户文档](/tiflash/tiflash-supported-pushdown-calculations.md)。

* 包含分区表的执行计划可以被缓存 [#issue号](链接) @[mjonss](https://github.com/mjonss)

    执行计划缓存是提升交易系统性能的有效手段。 自 7.6.0 开始， TiDB 解除了分区表的执行计划无法进入执行计划缓存的限制， 包含分区表的 SQL 语句能够从执行计划缓存中受益。 这将进一步提升分区表在 TiDB 的应用场景， 客户可以更多的利用分区技术降低数据读取的数量，提升数据库性能。 

    更多信息，请参考[用户文档](/sql-prepared-plan-cache.md)。 

### 稳定性

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

* 跨数据库绑定执行计划 [#issue号](链接) @[qw4990](https://github.com/qw4990)

    我们看到越来越多的用户用 TiDB 支撑 SaaS 平台。 SaaS 平台的一种普遍的建模方式，是把平台上每个租户的数据存入不同的“数据库”，而且业务逻辑完全相同。 这样我们能看到上百个数据库拥有相同的数据表和索引定义，运行类似的 SQL 语句。 在这种场景下，当我们需要对一条 SQL 语句的执行计划进行绑定(SQL Binding)， 这条绑定通常也会对运行在其他数据库的 SQL 有帮助。 

    针对这种应用场景，TiDB 引入了 "通用绑定" (Universal SQL Binding) 进行跨数据库绑定。 一个执行计划绑定能够匹配模式相同的 SQL，即使他们运行在不同数据库上。  比如，当我们创建了下面绑定， 只要 `t1` 和 `t2` 位于相同的数据库中， TiDB 都会尝试用此绑定的规则来生成执行计划， 而不需要为每个数据库上的 SQL 单独创建。 

    ```sql
    CREATE GLOBAL UNIVERSAL BINDING for
        SELECT * FROM t1, t2 WHERE t1.id = t2.id
    USING
        SELECT /*+ merge_join(t1, t2) */ * FROM t1, t2 WHERE t1.id = t2.id;
    ```

    "通用绑定" 还能够有效缓解 Saas 场景中一个常见问题。 SaaS 客户的数据量可能因为其业务本身需要而剧烈变化， 这是通常是 SaaS 服务商无法预测的。 由于统计信息无法及时更新， 数据量由小及大的快速变化经常会引发 SQL 性能问题。 在这种情况下， SaaS 服务商可以用 "通用绑定" 固定大数据量租户已经验证过的执行计划，这样能够减少这类问题造成的影响。 针对 SaaS 平台的用户，这一功能的引入为客户带来了显著的便利和体验提升。

    由于 "通用绑定" 会引入一个很小的系统开销（小于1%）， 默认将其关闭。 有需要的用户通过设置变量 [`tidb_opt_enable_universal_binding`]() 为 `YES` 开启。 

    更多信息，请参考[用户文档](/sql-plan-management.md)。

### 高可用

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

* 支持代理组件 TiProxy （实验特性） [#413](https://github.com/pingcap/tiproxy/issues/413) @[djshow832](https://github.com/djshow832) @[xhebox](https://github.com/xhebox) **tw@ran-huang** <!--1596-->

    TiProxy 是 TiDB 的官方代理组件，放置在客户端和 TiDB server 之间，为 TiDB 提供负载均衡、连接保持功能，让 TiDB 集群的负载更加均衡，以及维护操作时不影响用户对数据库的连接访问。
    * 在 TiDB 集群进行滚动重启、滚动升级、缩容等维护操作时，TiDB server 会发生变动，客户端对发生变动的 TiDB server 的连接将被中断。TiProxy 可以在这些维护操作过程中，平滑的将连接迁移至其他 TiDB server，从而让客户端不受到影响。
    * 所有客户端对 TiDB server 的连接都无法动态迁移至其他 TiDB server。当多个 TiDB server 的负载不均衡时，可能出现整体集群资源充足，但是个别 TiDB server 资源耗尽导致延迟大幅度增加的情况。TiProxy 提供连接动态迁移功能，在客户端无感的前提下，将连接从一个 TiDB server 迁移至其他 TiDB server，从而实现 TiDB 集群的负载均衡。
    
    TiProxy 被集成至 TiUP、TiOperator、Dashboard 等 TiDB 的基本组件中，可以方便的进行配置、部署、运维。

    更多信息，请参考[用户文档](/tiproxy/tiproxy-overview.md)。
    
### SQL 功能

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

### 数据库管理

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

* 简化执行计划绑定的语法 [#issue号](链接) @[qw4990](https://github.com/qw4990)

    TiDB 在新版本中简化的创建执行计划绑定的语法。 在命令中无需提供原 SQL 语句， TiDB 会根据带有 hint 的语句识别出原 SQL。 提升了创建执行计划绑定的便利性。 例如：

    ```sql
    CREATE GLOBAL BINDING
    USING
    SELECT /*+ merge_join(t1, t2) */ * FROM t1, t2 WHERE t1.id = t2.id;
    ```

    更多信息，请参考[用户文档](/sql-plan-management.md)。

### 可观测性

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

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
> 以下为从 v7.5.0 升级至当前版本 (v7.6.0) 所需兼容性变更信息。如果从 v7.4.0 或之前版本升级到当前版本，可能也需要考虑和查看中间版本 Release Notes 中提到的兼容性变更信息。

### 行为变更

* 行为变更 1

* 行为变更 2

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

## 离线包变更

## 废弃功能

* 废弃功能 1

* 废弃功能 2

## 改进提升

+ TiDB

    - 终止查询时及时通知 TiKV 以避免执行未开始的数据扫描任务 [#issue](链接) @[wshwsh12](https://github.com/wshwsh12) **tw@qiancai** <!--1634-->
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