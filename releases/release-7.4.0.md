---
title: TiDB 7.4.0 Release Notes
summary: 了解 TiDB 7.4.0 版本的新功能、兼容性变更、改进提升，以及错误修复。
---

# TiDB 7.4.0 Release Notes

发版日期：2023 年 x 月 x 日

TiDB 版本：7.4.0

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v7.3/quick-start-with-tidb) | [下载离线包](https://cn.pingcap.com/product-community/)

在 7.4.0 版本中，你可以获得以下关键特性：

<!-- to be added -->

## 功能详情

### 可扩展性

<!-- 请将 **tw@xxx** 中的 xxx 替换为这个 feature 的 writer 的 ID，这个标记会在发布前删除-->

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。
* TiDB 引入设置 TiDB Service scope 的功能，用于选择适用的 TiDB 节点来执行并行的 Add index 或 import into 任务 [#46453](https://github.com/pingcap/tidb/pull/46453) @[ywqzzy](https://github.com/ywqzzy) **tw@hfxsd** <!--1505-->

    功能描述 
    在资源密集型集群中并行执行 Add index 或 import into 任务可能占用大量 TiDB 节点的资源，从而导致集群性能下降的问题。现在，TiDB 引入了该功能，用户可以对存量 TiDB 节点选择其中几个节点，或者对新增 TiDB 节点设置 TiDB Service Scope 后，所有并行执行的 Add index 和 import into 的任务只会运行在这些节点，避免对已有业务造成性能影响。

    更多信息，请参考[用户文档](链接)。
### 性能

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。


* 新增支持下推 [运算符](/functions-and-operators/expressions-pushed-down.md)到 TiKV [#46307](https://github.com/pingcap/tidb/issues/46307) @[wshwsh12](https://github.com/wshwsh12)  **tw@caiqian** <!--1234-->

    * `value MEMBER OF(json_array)`

* 支持下推包含任何帧定义的窗口函数到 TiFlash [#7376](https://github.com/pingcap/tiflash/issues/7376) @[xzhangxian1008](https://github.com/xzhangxian1008)  **tw@caiqian** <!--1234-->

    在 v7.4.0 之前的版本中，TiFlash 不支持包含 PRECEDING 或 FOLLOWING 的窗口函数，所有包含此类帧定义的窗口函数都无法下推至 TiFlash。从 v7.4.0 开始，TiFlash 支持了所有的窗口函数的帧定义。该功能自动启用，满足要求时，会自动下推至 TiFlash 执行。

    更多信息，请参考[用户文档](/tiflash/tiflash-supported-pushdown-calculations.md)。
* 引入基于云存储的全局排序能力，提升并行执行的 Add index 或 import into 任务的性能和稳定性[#issue号](链接) @[贡献者 GitHub ID](链接) **tw@ran-huang** <!--1456-->

    功能描述
    原先用户执行分布式并行执行框架的 Add index 或 import into 任务的 TiDB 节点，需要准备一块较大的本地磁盘，用于编码后的索引 kv pairs 以及表数据的 kv Paris 进行排序，如果磁盘空间不够大，各个 TiDB 节点本地编码排序后的数据之间会存在 overlap 的情况，导致把这些 kv pairs 导入 TiKV 时，TiKV 需要不断地进行 compaction ，降低了执行 Add index 或 import into 的性能和稳定性。引入该特性后，编码后的数据从写入本地并排序改成写入云存储并在云存储进行全局排序，之后将全局排序后的索引数据和表数据并行导入到 TiKV，从而提升性能和稳定性。 
    更多信息，请参考[用户文档](链接)。

* 优化 Parallel Multi Schema Change ，提升 1 个 SQL 添加多个索引的性能 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1307-->

    功能描述 
    原先用户使用 Parallel Multi Schema Change 在 1 个 SQL 中提交多个 Add index 操作，性能和多个独立的 SQL 执行 Add index 操作的性能是一样的，优化后，可大幅提升在 1 个 SQL 中添加多个索引的性能。

    更多信息，请参考[用户文档](链接)。
* 支持缓存非 Prepare 语句的执行计划（GA）[#36598](https://github.com/pingcap/tidb/issues/36598) @[qw4990](https://github.com/qw4990)

    自 v7.4.0，非 Prepare 语句的执行计划缓存基本可用。执行计划缓存技术将会被应用于更广泛的场景，从而提升 TiDB 的并发处理能力。

    为了保持数据库行为向前兼容，非 Prepare 语句的执行计划缓存默认关闭，用户可以通过系统变量 [`tidb_enable_non_prepared_plan_cache`](/system-variables.md#tidb_enable_non_prepared_plan_cache) 按需打开，并通过系统变量 [`tidb_session_plan_cache_size`](/system-variables.md#tidb_session_plan_cache_size-从-v710-版本开始引入) 设置缓存大小。
    
    此外，该功能暂时不对 DML 语句生效，对 SQL 的模式也有一定的限制，具体参见[使用限制](/sql-non-prepared-plan-cache.md#限制)。


    更多信息，请参考[用户文档](/sql-non-prepared-plan-cache.md)。

### 稳定性

* TiFlash 引擎支持查询级别数据落盘 [#7738](https://github.com/pingcap/tiflash/issues/7738) @[windtalker](https://github.com/windtalker)  **tw@caiqian** <!--1234-->

    在 v7.0.0 版本中，TiFlash 支持 `GROUP BY`，`ORDER BY`，`JOIN` 三种算子的数据落盘功能，以避免数据量超过内存总大小时，TiFlash 会终止查询甚至系统崩溃的问题。控制单个算子的数据落盘，对于用户并不友好，在实际使用中，无法有效的进行整体资源控制。
    在 v7.4.0 版本中，TiFlash 支持查询级别数据落盘功能。通过设定单个查询在单个 TiFlash 节点使用内存的上限[`tiflash_mem_quota_query_per_node`](/system-variables.md#tiflash_mem_quota_query_per_node-从-v740-版本开始引入)及触发数据落盘的内存阈值[`tiflash_query_spill_ratio`](/system-variables.md#tiflash_query_spill_ratio-从-v740-版本开始引入)，可以方便的控制单个查询的内存使用，更好的管控 TiFlash 内存资源。

    更多信息，请参考[用户文档](/tiflash/tiflash-spill-disk.md)。

* 部分系统变量可通过优化器提示设置 [#issue号](链接) @[winoros](https://github.com/winoros) 

    TiDB 新增支持了 MySQL 8.0 相似的优化器提示 [`SET_VAR()`]()。 通过在 SQL 添加 hint `SET_VAR()`，能够在语句运行过程中临时修改部分系统变量，达到针对不同语句设置环境的目的。 比如主动提升高消耗的 SQL 的并行度，或者利用变量修改优化器行为。 
    
    支持修改的系统变量请参考[用户文档](/system-variables.md)，不建议在提示中设置文档中没有明确支持的变量，可能造成不可预知的结果。 

    更多信息，请参考[用户文档](/optimizer-hints.md)。

* TiFlash 支持资源管控特性 [#7660](https://github.com/pingcap/tiflash/issues/7660) @[guo-shaoge](https://github.com/guo-shaoge)  **tw@caiqian** <!--1234-->

    TiDB 在 v7.1.0 中正式发布了基于资源组的资源管控特性，但是这个特性还不包含 TiFlash。在 v7.4.0 中，TiFlash 支持了资源管控特性，完善了整体 TiDB 的资源管控能力。TiFlash 的资源管控和已有的 TiDB 资源管控特性完全兼容，现有的资源组将同时管控 TiDB/TiKV/TiFlash 中的资源。

    通过 TiFlash 配置参数 `enable_resource_control` 启用 TiFlash 资源管控特性后，TiFlash 将根据 TiDB 的资源组配置，进行资源调度管理，确保整体资源的合理分配使用。

    更多信息，请参考[用户文档](/tidb-resource-control.md)。

* TiFlash Pipeline 执行模型正式发布（GA）[#6518](https://github.com/pingcap/tiflash/issues/6518) @[SeaRise](https://github.com/SeaRise)

    在 v7.2.0 版本中，TiFlash 以实验特性发布了 Pipeline 执行模型。TiFlash 引入 Pipeline 执行模型，对所有线程资源进行统一管理，并对所有任务的执行进行统一调度，充分利用线程资源，同时避免资源超用。从 v7.4.0 开始，TiFlash 完善了线程资源使用量的统计，将正式发布 Pipeline 执行模型。控制该特性是否启用的系统变量 [`tidb_enable_tiflash_pipeline_model`](/system-variables.md#tidb_enable_tiflash_pipeline_model-从-v720-版本开始引入) 的默认值将调整为 `true`，并且作用域调整为 `GLOBAL`。

    更多信息，请参考[用户文档](/tiflash/tiflash-pipeline-model.md)。

* 新增优化器模式选择 [#46080](https://github.com/pingcap/tidb/issues/46080) @[time-and-fate](https://github.com/time-and-fate)

    TiDB 在 v7.4.0 引入了一个新的系统变量 [`tidb_opt_objective`](/system-variables.md#tidb_opt_objective-从-v740-版本开始引入)，用于控制优化器的估算方式。 默认值 `moderate` 维持从前的优化器行为，优化器会利用运行时统计到的数据修改来校正估算。 如果设置为 `determinate`，优化器则不考虑运行时校正，只根据统计信息来生成执行计划。

    对于长期稳定的 OLTP 业务，或者如果用户对已有的执行计划非常有把握，则推荐测试后切换到 `determinate` 模式减少执行计划跳变的可能。

    更多信息，请参考[用户文档](/system-variables.md#tidb_opt_objective-从-v740-版本开始引入)。

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

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

    在 v7.4.0 之前，TiDB 中的分区表不能调整分区类型。从 v7.4.0 开始，TiDB 支持将分区表修改为非分区表、将非分区表修改为分区表、修改分区类型功能。你可以根据需要灵活调整表的分区类型、数量。例如，通过 `ALTER TABLE t PARTITION BY ...` 语句修改分区类型。

    更多信息，请参考[用户文档](/partitioned-table.md#分区管理)。

* TiDB 支持 ROLLUP 修饰符 和 GROUPING 函数 [#44487](https://github.com/pingcap/tidb/issues/44487) @[AilinKid](https://github.com/AilinKid) **tw@qiancai** <!--1370-->

    在 v7.4.0 之前，TiDB 不支持 ROLLUP 修饰符和 GROUPING 函数。ROLLUP 修饰符和 GROUPING 函数是数据分析中常用的功能，用于对数据进行分级汇总。从 v7.4.0 开始，TiDB 支持 ROLLUP 修饰符和 GROUPING 函数。ROLLUP 修饰符的使用方式为：`SELECT ... FROM ... GROUP BY ... WITH ROLLUP`

    更多信息，请参考[用户文档](/functions-and-operators/aggregate-group-by-functions.md#group-by-修饰符)。

### 数据库管理

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

* 新增排序规则 `utf8mb4_0900_ai_ci` 和 `utf8mb4_0900_bin` [#37566](https://github.com/pingcap/tidb/issues/37566) @[YangKeao](https://github.com/YangKeao) @[zimulala](https://github.com/zimulala) @[bb7133](https://github.com/bb7133)

    TiDB 在新版本中增强了从 MySQL 8.0 迁移的支持。新增两个排序规则 (Collation) `utf8mb4_0900_ai_ci` 和 `utf8mb4_0900_bin`， 其中 `utf8mb4_0900_ai_ci` 为 MySQL 8.0 的默认排序规则。

    同时新增支持 MySQL 8.0 兼容的系统变量 [`default_collation_for_utf8mb4`]()， 允许用户为 utf8mb4 字符集选择默认排序方式， 兼容从 MySQL 5.7 或更旧版本的迁移或数据复制场景。

    更多信息，请参考[用户文档](/character-set-and-collation#支持的字符集和排序规则)。

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
* DataMigration(DM) 支持拦截不兼容（破坏数据一致性）的 DDL 变更 [#9692](https://github.com/pingcap/tiflow/issues/9692) @[GMHDBJD](https://github.com/GMHDBJD) **tw@hfxsd** <!--1523-->

    功能描述 
    之前用户使用 DM 的 binlog filter 功能颗粒度比较粗，例如只能过滤 alter 这种大颗粒度的 DDL event，这在一些业务场景是受限的，例如业务允许将 Decimal 字段类型的精度调大，但是不允许减小。因此引入一个新的 event name “incompatible DDL changes” 用于拦截那些变更后会导致数据丢失，数据被截断，精度损失等问题的 DDL，并报错提示给用户及时介入处理，避免对下游的业务数据产生影响。  

    更多信息，请参考[用户文档](链接)。
    
* 支持实时更新增量数据校验的 checkpoint [#issue号](链接) @[lichunzhu](https://github.com/lichunzhu) **tw@ranh-huang** <!--1496-->

    功能描述 
    过去，用户使用增量数据校验功能，判断 DM 同步到下游的数据是否和上游是一致的，并以此作为业务流量从上游数据库割接到 TiDB 的判断依据。而增量校验 checkpoint 受同步延迟，不一致的数据等待一段时间后重新校验等机制限制，需要每隔几分钟的时间来刷新校验后的 checkpoint，这在一些割接时间只有几十秒的业务场景是不可接受的，引入该功能后，用户可以传入上游数据库填写的 binlog Postion，一旦增量校验程序在内存里校验到该 binlog Postion 后会立即刷新 checkpoint，而不是每隔几分钟刷新 checkpoint，从而用户可以根据该立即返回的 checkpoint 来快速地割接。

    更多信息，请参考[用户文档](链接)。
    
* import into 支持对导入的数据通过云存储进行全局排序提升导入性能和稳定性 [#46704](https://github.com/pingcap/tidb/issues/46704) @[D3Hunter](https://github.com/D3Hunter) **tw@qiancai** <!--1494-->

    功能描述 
    原先用户使用 import into 导入数据，会把该任务拆分成多个子任务调度到各个 TiDB 节点并行执行，这些 TiDB 节点，需要准备一块较大的本地磁盘，用于对编码后的索引 kv pairs 以及表 kv Paris 数据进行排序，如果磁盘空间不够大，各个 TiDB 节点本地编码排序后的数据之间会存在 overlap 的情况，导致把这些 kv pairs 导入 TiKV 时，TiKV 需要不断地进行 compaction ，降低了执行 import into 的性能和稳定性。引入该特性后，编码后的数据从写入本地并排序改成写入云存储并在云存储进行全局排序，之后将全局排序后的表数据和索引数据并行导入到 TiKV，从而提升性能和稳定性。 
    更多信息，请参考[用户文档](链接)。
## 兼容性变更

> **注意：**
>
> 以下为从 v7.3.0 升级至当前版本 (v7.4.0) 所需兼容性变更信息。如果从 v7.2.0 或之前版本升级到当前版本，可能也需要考虑和查看中间版本 release notes 中提到的兼容性变更信息。

### 行为变更

<!-- 此小节包含 MySQL 兼容性变更-->

* 兼容性 1

* 兼容性 2

### 系统变量

| 变量名 | 修改类型 | 描述 |
|---|----|------|
| [`default_collation_for_utf8mb4`]() | 新增 | 为 utf8mb4 字符集选择默认排序方式， 兼容从 MySQL 5.7 或更旧版本的迁移或数据复制场景。 |
| [`tidb_opt_objective`](/system-variables.md#tidb_opt_objective-从-v740-版本开始引入) | 新增 | 该变量用于设置优化器优化目标。moderate 维持旧版本的默认行为，优化器会利用更多信息尝试生成更优的计划；determinate 则倾向于保守，保持执行计划稳定。 |
|  | 新增/删除/修改 |  |
|  | 新增/删除/修改 |  |
|  | 新增/删除/修改 |  |

### 配置文件参数

| 配置文件 | 配置项 | 修改类型 | 描述 |
| -------- | -------- | -------- | -------- |
| Import into |SPLIT_FILE | 新增| 对需要导入的大型 CSV 文件切割成多个 256 MiB 大小的 CSV 文件|
|  | | 新增/删除/修改 | |
|  | | 新增/删除/修改 | |
|  | | 新增/删除/修改 | |
|  | | 新增/删除/修改 | |
|  | | 新增/删除/修改 | |

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
    - 提升 TiFlash 在存算分离架构下的性能和稳定性（实验特性） [#6882](https://github.com/pingcap/tiflash/issues/6882)  @[JaySon-Huang](https://github.com/JaySon-Huang) @[breezewish](https://github.com/breezewish) @[JinheLin](https://github.com/JinheLin) **tw@caiqian** <!--1234-->
    - 改进 TiFlash Compact Log 策略，提升随机写入负载下的读性能 [#7564](https://github.com/pingcap/tiflash/issues/7564) @[CalvinNeo](https://github.com/CalvinNeo) **tw@caiqian** <!--1234-->
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
