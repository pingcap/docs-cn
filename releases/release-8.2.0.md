---
title: TiDB 8.2.0 Release Notes
summary: 了解 TiDB 8.2.0 版本的新功能、兼容性变更、改进提升，以及错误修复。
---

# TiDB 8.2.0 Release Notes

发版日期：2024 年 x 月 x 日

TiDB 版本：8.2.0

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v8.2/quick-start-with-tidb) | [下载离线包](https://cn.pingcap.com/product-community/?version=v8.2.0-DMR#version-list)

在 8.2.0 版本中，你可以获得以下关键特性：

## 功能详情

### 可扩展性

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

### 性能

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

* 支持下推以下字符串函数到 TiKV [#50601](https://github.com/pingcap/tidb/issues/50601) @[dbsid](https://github.com/dbsid)  **tw@Oreoxmt** <!--1663-->

    * `JSON_ARRAY_APPEND()`
    * `JSON_MERGE_PATCH()`
    * `JSON_REPLACE()`

  更多信息，请参考[用户文档](/functions-and-operators/expressions-pushed-down.md)。

* TiDB 支持并行排序功能 [#49217](https://github.com/pingcap/tidb/issues/49217) [#50746](https://github.com/pingcap/tidb/issues/50746) @[xzhangxian1008](https://github.com/xzhangxian1008) **tw@Oreoxmt** <!--1665-->

    在 v8.2.0 版本之前，TiDB 进行排序计算时只能以非并行的方式进行处理，当需要对大量数据进行排序时，查询性能收到影响。

    在 v8.2.0 版本中，TiDB 支持并行排序功能，所有的排序计算性能都将得到提升。该功能不需要单独开启，TiDB 将根据变量 [`tidb_executor_concurrency`](/system-variables.md#tidb_executor_concurrency-从-v50-版本开始引入) 的设定，确定使用并行方式或非并行方式进行排序。

* TiDB 的并发 HashAgg 算法支持数据落盘（GA）[#35637](https://github.com/pingcap/tidb/issues/35637) @[xzhangxian1008](https://github.com/xzhangxian1008)  **tw@Oreoxmt** <!--1842-->

    在 v8.0.0 中，TiDB 以实验特性发布了并发 HashAgg 算法支持数据落盘功能。

    在 v8.2.0 中，TiDB 正式发布该功能。TiDB 在使用并发 HashAgg 算法时，将根据内存使用情况自动触发数据落盘，从而兼顾性能和数据处理量。该功能默认打开，变量 `tidb_enable_concurrent_hashagg_spill` 将被废弃。

### 稳定性

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

* 统计信息加载效率提升 10 倍 [#52831](https://github.com/pingcap/tidb/issues/52831) @[hawkingrei](https://github.com/hawkingrei) **tw@hfxsdt** <!--1754-->

    SaaS 或 PaaS 类业务应用中可能存在大量的数据表，这会拖慢了初始统计信息加载的速度，也会降低运行时加载的成功率。TiDB 的启动时间，以及执行计划的准确性都相应会受到影响。在 v8.2.0 中，我们从并发模型，内存分配方式等多个角度了优化统计信息的加载过程，降低延迟，提升吞吐，避免由于统计信息加载问题造成的大规模性能回退，进一步提升了数据库的稳定性。

    新增支持自适应的并行加载。默认情况下，配置项[`stats-load-concurrency`](/tidb-configuration-file.md#stats-load-concurrency-从-v540-版本开始引入)的值为 `0`，统计信息加载的并行度会根据硬件规格自动选择。 

    更多信息，请参考[用户文档](/tidb-configuration-file.md#stats-load-concurrency-从-v540-版本开始引入)。

### 高可用

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

* TiProxy 支持多种负载均衡策略 [#465](https://github.com/pingcap/tiproxy/issues/465) @[djshow832](https://github.com/djshow832) @[xhebox](https://github.com/xhebox)  **tw@Oreoxmt** <!--1777-->

    TiProxy 是 TiDB 的官方代理组件，位于客户端和 TiDB server 之间，为 TiDB 集群提供负载均衡、连接保持功能。在 v8.2.0 之前，TiProxy 默认使用 v1.0.0 版本，只能基于状态和连接数进行负载均衡。
    在 v8.2.0 中，TiProxy 默认使用 v1.1.0 版本，引入了多种负载均衡策略，除了状态和连接数，还可以根据健康度、资源、地理位置等信息，对 TiDB 集群的连接进行动态负载均衡调度，使整个 TiDB 集群更加稳定。

    TiProxy 的负载均衡策略可以通过配置项进行配置，具体策略包括：
    * `resource`: 资源优先策略，优先级顺序依次为基于状态、健康度、内存、CPU、地理位置、连接数的负载均衡。
    * `location`: 地理优先策略，优先级顺序依次为基于状态、地理位置、健康度、内存、CPU、连接数的负载均衡。
    * `connection`: 最小连接数策略，优先级顺序依次为基于状态、连接数的负载均衡。

    更多信息，请参考[用户文档](/tiproxy/tiproxy-load-balance.md)。

### SQL 功能

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

* TiDB 支持 JSON Schema Validation 函数 [#52780](https://github.com/pingcap/tidb/pull/52780) @[dveeden](https://github.com/dveeden) **tw@hfxsd** <!--1840-->

    在 v8.2.0 版本之前，用户需要依赖外部工具或自定义验证逻辑进行 JSON 数据验证，增加了开发和维护的复杂度，降低了开发效率。 引入该功能后，允许用户在 TiDB 中直接验证 JSON 数据的有效性，提高数据的完整性和一致性，提升了用户的开发效率。

    更多信息，请参考[用户文档](链接)。

### 数据库管理

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

* TiUP 支持部署 PD 微服务 [#5766](https://github.com/tikv/pd/issues/5766) @[rleungx](https://github.com/rleungx) **tw@qiancai** <!--1841-->

   通过将 PD 拆分成多个单独的服务，独立部署进行管理，可以更好地控制资源的使用和隔离，减少不同服务相互之间的影响。从 v8.2.0 开始，TiUP 支持将 PD 以微服务的模式进行部署，用户可以将 TSO 微服务和 Scheduling 微服务，单独进行部署，实现资源隔离以及快速迭代的目的。 

    更多信息，请参考[用户文档]()。

* 为切换资源组的操作增加权限控制 [#issue号](链接) @[glorv](https://github.com/glorv) **tw@lilin90** <!--1740-->

    TiDB 允许用户利用命令 [`SET RESOURCE GROUP`](/sql-statements/sql-statement-set-resource-group.md) 或 Hint [`RESOURCE_GROUP()`](/optimizer-hints.md#resource_groupresource_group_name) 切换到其他资源组，这可能会造成部分数据库用户对资源组的滥用。TiDB v8.2.0 增加了对资源组切换行为的管控，只有被授予动态权限 `RESOURCE_GROUP_ADMIN` 或者 `RESOURCE_GROUP_USER` 的数据库用户，才能切换到其他资源组，加强对系统资源的保护。

    为了维持兼容性，从旧版本升级的集群维持原行为不变。通过设置新增变量 [`tidb_resource_control_strict_mode`](/system-variables.md) 为 `ON` ，开启上述的增强权限控制。

    更多信息，请参考[用户文档](/tidb-resource-control.md#绑定资源组)。

### 可观测性

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

* 记录执行计划没有被缓存的原因 [#issue号](链接) @[qw4990](https://github.com/qw4990) **tw@hfxsdt** <!--1819-->

    在一些场景下，用户希望多数执行计划能够被缓存，以节省执行开销，并降低延迟。目前执行计划缓存对 SQL 有一定限制，部分形态 SQL 的执行计划无法被缓存，但是用户很难识别出无法被缓存的 SQL 以及对应的原因。因此，在新版本中，我们向系统表 [`STATEMENTS_SUMMARY`](/statement-summary-tables.md) 中增加了新的列，解释计划无法被缓存的原因，协助用户做性能调优。

    更多信息，请参考[用户文档](/statement-summary-tables.md#表的字段介绍)。

### 安全

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

* 增强 TiFlash 日志脱敏 [#8977](https://github.com/pingcap/tiflash/issues/8977) @[JaySon-Huang](https://github.com/JaySon-Huang) **tw@Oreoxmt** <!--1818-->

    在 v8.0.0 版本，TiDB 增强了日志脱敏功能，可以控制是否对日志信息进行脱敏，以实现在不同场景下安全使用 TiDB 日志，提升了使用日志脱敏能力的安全性和灵活性。在 v8.2.0 版本中，TiFlash 进行了类似的日志脱敏功能增强。要使用此功能，需要将 tiflash-server 中 `security.redact_info_log` 配置项的值设为 `MARKER`。

    更多信息，请参考[用户文档](/tiflash/tiflash-configuration.md#配置文件-tiflashtoml)。

### 数据迁移

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

## 兼容性变更

> **注意：**
>
> 以下为从 v8.1.0 升级至当前版本 (v8.2.0) 所需兼容性变更信息。如果从 v8.0.0 或之前版本升级到当前版本，可能也需要考虑和查看中间版本 Release Notes 中提到的兼容性变更信息。

### 行为变更

* TiDB Lightning，从 v8.2.0 开始当用户设置 strict-format = true，来切分大的 CSV 文件为多个小的 CSV 文件来提升并发和导入性能时，需要显式指定行结束符 terminator 参数的取值为  \r，\n 或 \r\n 。否则可能导致 CSV 文件数据解析异常。
* Import Into SQL 语法，从 v8.2.0 开始，当用户导入 CSV 文件，且指定 split 参数来切分大的 CSV 文件为多个小的 CSV 文件来提升并发和导入性能时，需显式指定行结束符 LINES_TERMINATED_BY 参数的取值为  \r，\n 或 \r\n 。否则可能导致 CSV 文件数据解析异常。

* 行为变更 2

### MySQL 兼容性

* 兼容性 1

* 兼容性 2

### 系统变量

| 变量名  | 修改类型（包括新增/修改/删除）    | 描述 |
|--------|------------------------------|------|
| [`tidb_enable_historical_stats`](/system-variables.md#tidb_enable_historical_stats) | 修改 | 自 v8.2.0，默认不保存历史统计信息，避免潜在的稳定性问题 **tw@hfxsdt** <!--1759--> |
| [`tidb_analyze_skip_column_types`](/system-variables.md#tidb_analyze_skip_column_types-从-v720-版本开始引入) | 修改 | 默认设置下，TiDB 不会收集类型为 `mediumtext` 和 `longtext` 的列，避免潜在的 OOM 风险。 |
|        |                              |      |
|        |                              |      |

### 系统表

### 其他

## 离线包变更

## 废弃功能

* 废弃功能 1

* 变量 [`tidb_enable_concurrent_hashagg_spill`](/system-variables.md#tidb_enable_concurrent_hashagg_spill-从-v800-版本开始引入) 将被废弃。

## 改进提升

+ TiDB

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - 优化客户端读取数据超时无法终止查询的问题 [#44009](https://github.com/pingcap/tidb/issues/44009) @[wshwsh12](https://github.com/wshwsh12)  **tw@Oreoxmt** <!--1636-->
    - 优化对大数据量的表进行简单查询的性能 [#53850](https://github.com/pingcap/tidb/issues/53850) @[you06](https://github.com/you06)  **tw@Oreoxmt** <!--1561-->
    - 聚合的结果集能够作为 Index Join 的内表 [#37068](https://github.com/pingcap/tidb/issues/37068) @[elsa0520](https://github.com/elsa0520) **tw@hfxsdt** <!--1510-->

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