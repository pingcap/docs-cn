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

* TiDB 引入设置 TiDB Service Scope 的功能，用于选择适用的 TiDB 节点来执行并行的 `ADD INDEX` 或 `IMPORT INTO` 任务（实验特性）[#46453](https://github.com/pingcap/tidb/pull/46453) @[ywqzzy](https://github.com/ywqzzy) **tw@hfxsd** <!--1505-->

    在资源密集型集群中并行执行 `ADD INDEX` 或 `IMPORT INTO` 任务可能占用大量 TiDB 节点的资源，从而导致集群性能下降。TiDB v7.4.0 引入了设置 TiDB Service Scope 的功能作为实验特性，你可以在存量 TiDB 节点中选择几个节点，或者对新增 TiDB 节点设置 TiDB Service Scope，所有并行执行的 `ADD INDEX` 和 `IMPORT INTO` 的任务只会运行在这些节点，避免对已有业务造成性能影响。

    更多信息，请参考[用户文档](/system-variables.md#tidb_service_scope-从-v740-版本开始引入)。
    
* 增强 Partitioned Raft KV 存储引擎（实验特性）[#issue号](链接) @[busyjay](https://github.com/busyjay) @[tonyxuqqi](https://github.com/tonyxuqqi) @[tabokie](https://github.com/tabokie) @[bufferflies](https://github.com/bufferflies) @[5kbpers](https://github.com/5kbpers) @[SpadeA-Tang](https://github.com/SpadeA-Tang) @[nolouch](https://github.com/nolouch)  **tw@Oreoxmt** <!--1292-->

    TiDB v6.6.0 引入了 Partitioned Raft KV 存储引擎作为实验特性，该引擎使用多个 RocksDB 实例存储 TiKV 的 Region 数据，每个 Region 的数据都独立存储在单独的 RocksDB 实例中。

    在 TiDB v7.4.0 中，Partitioned Raft KV 引擎在兼容性和稳定性方面得到了进一步提升。通过大规模数据测试，确保了 Partitioned Raft KV 引擎与 DM、Dumpling、TiDB Lightning、TiCDC、BR、PITR 等关键生态组件或功能的兼容性。同时，在读写混合工作负载下，Partitioned Raft KV 引擎提供了更稳定的性能，特别适合写多读少的场景。此外，每个 TiKV 节点支持 8 core CPU，并可搭配 8 TB 的数据存储和 64 GB 的内存。

    更多信息，请参考[用户文档](/partitioned-raft-kv.md)。
 
 * TiFlash 存算分离架构成为正式功能 (GA) [#6882](https://github.com/pingcap/tiflash/issues/6882)  @[JaySon-Huang](https://github.com/JaySon-Huang) @[JinheLin](https://github.com/JinheLin) @[breezewish](https://github.com/breezewish) @[lidezhu](https://github.com/lidezhu) @[CalvinNeo](https://github.com/CalvinNeo)  **tw@qiancai** <!--1360-->

    在 v7.0.0 中，TiFlash 以实验特性引入了存算分离架构。经过一系列的改进，从 v7.4.0 起，TiFlash 正式支持存算分离架构。
    
    在存算分离架构下，TiFlash 节点分为 Compute Node （计算节点）和 Write Node（写入节点）两种类型，并使用兼容 S3 API 的对象存储。这两种节点都可以单独扩缩容，独立调整计算或数据存储能力。在存算分离架构下，TiFlash 的使用方式与存算一体架构一致，例如创建 TiFlash 副本、查询、指定优化器 Hint 等。
    
   需要注意的是，TiFlash 的存算分离架构和存算一体架构不能混合使用、相互转换，需要在部署 TiFlash 时进行相应的配置指定使用其中的一种架构。

    更多信息，请参考[用户文档](/tiflash/tiflash-disaggregated-and-s3.md)。

### 性能

* 支持下推 JSON [运算符](/functions-and-operators/expressions-pushed-down.md) `MEMBER OF` 到 TiKV [#46307](https://github.com/pingcap/tidb/issues/46307) @[wshwsh12](https://github.com/wshwsh12)  **tw@qiancai** <!--1551-->

    * `value MEMBER OF(json_array)`

    更多信息，请参考[用户文档](/functions-and-operators/expressions-pushed-down.md)。

* 支持下推包含任意帧定义类型的窗口函数到 TiFlash [#7376](https://github.com/pingcap/tiflash/issues/7376) @[xzhangxian1008](https://github.com/xzhangxian1008)  **tw@qiancai** <!--1381-->

    在 v7.4.0 之前的版本中，TiFlash 不支持包含 `PRECEDING` 或 `FOLLOWING` 的窗口函数，所有包含此类帧定义的窗口函数都无法下推至 TiFlash。从 v7.4.0 开始，TiFlash 支持了所有的窗口函数的帧定义。该功能自动启用，满足要求时，包含帧定义的窗口函数会自动下推至 TiFlash 执行。

* 引入基于云存储的全局排序能力，提升并行执行的 `ADD INDEX` 或 `IMPORT INTO` 任务的性能和稳定性 [#45719](https://github.com/pingcap/tidb/issues/45719) @[wjhuang2016](https://github.com/wjhuang2016) **tw@ran-huang** <!--1456-->

    在 v7.4.0 以前，当用户执行分布式并行执行框架的 `ADD INDEX` 或 `IMPORT INTO` 任务时，TiDB 节点需要准备一块较大的本地磁盘，对编码后的索引 KV pairs 和表数据 KV pairs 进行排序。由于无法从全局角度进行排序，各个 TiDB 节点间以及节点内部导入的数据可能存在重叠情况。这会导致在将这些 KV pairs 导入到 TiKV 时，TiKV 需要不断进行数据整理 (compaction) 操作，降低了 `ADD INDEX` 或 `IMPORT INTO` 的性能和稳定性。

    v7.4.0 引入全局排序特性后，编码后的数据不再写入本地进行排序，而是写入云存储，并在云存储中进行全局排序。然后，TiDB 将经过全局排序的索引数据和表数据并行导入到 TiKV 中，从而提升了性能和稳定性。

    更多信息，请参考[用户文档](/tidb-global-sort.md)。

* 优化 Parallel Multi Schema Change，提升一个 SQL 语句添加多个索引的性能 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@ran-huang** <!--1307-->

    在 v7.4.0 之前，用户使用 Parallel Multi Schema Change 在一个 SQL 语句中提交多个 `ADD INDEX` 操作时，其性能与使用多个独立的 SQL 语句进行 `ADD INDEX` 操作的性能相同。经过 v7.4.0 的优化后，在一个 SQL 语句中添加多个索引的性能得到了大幅提升。

    更多信息，请参考[用户文档](链接)。

* 支持缓存非 Prepare 语句的执行计划 (GA) [#36598](https://github.com/pingcap/tidb/issues/36598) @[qw4990](https://github.com/qw4990) **tw@Oreoxmt** <!--1355-->

    TiDB v7.0.0 引入了非 Prepare 语句的执行计划缓存作为实验特性，以提升在线交易场景的并发处理能力。在 v7.4.0 中，该功能正式 GA。执行计划缓存技术将会被应用于更广泛的场景，从而提升 TiDB 的并发处理能力。

    开启非 Prepare 语句执行计划缓存可能会带来额外的内存和 CPU 开销，并不一定适用于所有场景。从 v7.4.0 开始，非 Prepare 语句的执行计划缓存默认关闭。你可以通过系统变量 [`tidb_enable_non_prepared_plan_cache`](/system-variables.md#tidb_enable_non_prepared_plan_cache) 控制是否开启该功能并通过 [`tidb_session_plan_cache_size`](/system-variables.md#tidb_session_plan_cache_size-从-v710-版本开始引入) 设置缓存大小。

    此外，该功能默认不支持 DML 语句，对 SQL 的模式也有一定的限制，具体参见[使用限制](/sql-non-prepared-plan-cache.md#限制)。

    更多信息，请参考[用户文档](/sql-non-prepared-plan-cache.md)。

### 稳定性

* TiFlash 引擎支持查询级别的数据落盘 [#7738](https://github.com/pingcap/tiflash/issues/7738) @[windtalker](https://github.com/windtalker)  **tw@qiancai** <!--1493-->

    从 v7.0.0 起，TiFlash 支持控制 `GROUP BY`、`ORDER BY`、`JOIN` 这三种算子的数据落盘功能，避免数据量超过内存总大小时，导致查询终止甚至系统崩溃的问题。然而，单独控制每个算子的落盘较为麻烦，也无法有效进行整体资源控制。

    在 v7.4.0 中，TiFlash 引入了查询级别数的据落盘功能。通过设置单个查询在单个 TiFlash 节点使用内存的上限 [`tiflash_mem_quota_query_per_node`](/system-variables.md#tiflash_mem_quota_query_per_node-从-v740-版本开始引入)及触发数据落盘的内存阈值 [`tiflash_query_spill_ratio`](/system-variables.md#tiflash_query_spill_ratio-从-v740-版本开始引入)，你可以方便地控制单个查询的内存使用，更好地管控 TiFlash 内存资源。

    更多信息，请参考[用户文档](/tiflash/tiflash-spill-disk.md)。


* 引入自定义 TiKV 读取超时时间 [#45380](https://github.com/pingcap/tidb/issues/45380) @[crazycs520](https://github.com/crazycs520) **tw@hfxsd** <!--1560-->

    在通常情况下，TiKV 处理请求非常快，只需几毫秒。但是，当某个 TiKV 节点遇到磁盘 I/O 抖动或网络延迟时，请求处理时间可能会大幅增加。在 v7.4.0 以前的版本中，TiKV 请求的超时限制是固定的，不能调整，因此当 TiKV 节点出现问题时，TiDB 必须等待超时响应，这导致了抖动期间应用程序的查询性能受到明显影响。

    TiDB 在 v7.4.0 中引入了一个新参数 [`TIDB_KV_READ_TIMEOUT(N)`](/system-variables.md#tidb_kv_read_timeout-从-v740-版本开始引入)，你可以自定义查询语句中 TiDB 发送给 TiKV 的 RPC 读请求的超时时间。这意味着，当某个 TiKV 节点因磁盘或网络问题导致请求延迟时，TiDB 可以更快地超时并将请求重新发送给其他 TiKV 节点，从而降低查询延迟。如果所有 TiKV 节点的请求都超时，TiDB 将使用默认的超时时间进行重试。该参数也支持通过 Hint [`TIDB_KV_READ_TIMEOUT(N)`](/optimizer-hints.md#tidb_kv_read_timeoutn) 来设置查询语句中 TiDB 发送 TiKV RPC 读请求的超时时间。这一改进将使 TiDB 在面对不稳定的网络或存储环境时，更灵活地适应各种情况，提高查询性能，提升用户体验。
    
    更多的信息，请参考[用户文档](/system-variables.md#tidb_kv_read_timeout-从-v740-版本开始引入)。

* 支持通过优化器提示临时修改部分系统变量的值 [#issue号](链接) @[winoros](https://github.com/winoros) **tw@Oreoxmt** <!--923-->

    TiDB v7.4.0 新增支持与 MySQL 8.0 相似的优化器提示 `SET_VAR()`。通过在 SQL 语句中添加 Hint `SET_VAR()`，可以在语句运行过程中临时修改部分系统变量，以针对不同语句设置环境。例如，可以主动提升高消耗 SQL 的并行度，或者通过变量修改优化器行为。

    支持使用 Hint `SET_VAR()` 修改的系统变量请参考[系统变量](/system-variables.md)。强烈建议不要利用此 Hint 修改没有明确支持的变量，这可能会引发不可预知的行为。

    更多信息，请参考[用户文档](/optimizer-hints.md)。

* TiFlash 支持资源管控特性 [#7660](https://github.com/pingcap/tiflash/issues/7660) @[guo-shaoge](https://github.com/guo-shaoge)  **tw@Oreoxmt** <!--1506-->

    在 TiDB v7.1.0 中，资源管控成为正式功能，提供对 TiDB 和 TiKV 的资源管理能力。在 v7.4.0 中，TiFlash 支持资源管控特性，完善了 TiDB 整体的资源管控能力。TiFlash 的资源管控与已有的 TiDB 资源管控特性完全兼容，现有的资源组将同时管控 TiDB、TiKV 和 TiFlash 中的资源。

    通过配置 TiFlash 参数 `enable_resource_control`，你可以控制是否开启 TiFlash 资源管控特性。开启后，TiFlash 将根据 TiDB 的资源组配置进行资源调度管理，确保整体资源的合理分配和使用。

    更多信息，请参考[用户文档](/tidb-resource-control.md)。

* TiFlash 支持 Pipeline 执行模型 (GA) [#6518](https://github.com/pingcap/tiflash/issues/6518) @[SeaRise](https://github.com/SeaRise) **tw@Oreoxmt** <!--1549-->

    在 v7.2.0 中，TiFlash 引入了 Pipeline 执行模型作为实验特性。该模型对所有线程资源进行统一管理，并对所有任务的执行进行统一调度，充分利用线程资源，同时避免资源超用。从 v7.4.0 开始，TiFlash 完善了线程资源使用量的统计，Pipeline 执行模型成为正式功能 (GA) 并默认开启。由于该功能与 TiFlash 资源管控特性相互依赖，TiDB v7.4.0 移除了之前版本中用于控制是否启用 Pipeline 执行模型的变量 `tidb_enable_tiflash_pipeline_model`。现在你可以通过 TiFlash 参数 `tidb_enable_resource_control` 同时开启或关闭 Pipeline 执行模型和 TiFlash 资源管控特性。

    更多信息，请参考[用户文档](/tiflash/tiflash-pipeline-model.md)。

* 新增优化器模式选择 [#46080](https://github.com/pingcap/tidb/issues/46080) @[time-and-fate](https://github.com/time-and-fate) **tw@ran-huang** <!--1527-->

    TiDB 在 v7.4.0 引入了一个新的系统变量 [`tidb_opt_objective`](/system-variables.md#tidb_opt_objective-从-v740-版本开始引入)，用于控制优化器的估算方式。默认值 `moderate` 维持从前的优化器行为，即优化器会利用运行时统计到的数据修改来校正估算。如果设置为 `determinate`，则优化器不考虑运行时校正，只根据统计信息来生成执行计划。

    对于长期稳定的 OLTP 业务，或者如果用户对已有的执行计划非常有把握的情况下，推荐在测试后切换到 `determinate` 模式，减少执行计划跳变的可能。

    更多信息，请参考[用户文档](/system-variables.md#tidb_opt_objective-从-v740-版本开始引入)。

* 资源管控支持自动管理后台任务（实验特性）[#issue号](链接) @[glorv](https://github.com/glorv) **tw@Oreoxmt** <!--1448-->

    后台任务是指那些优先级不高但是需要消耗大量资源的任务，如数据备份和自动统计信息收集等。这些任务通常定期或不定期触发，在执行的时候会消耗大量资源，从而影响在线的高优先级任务的性能。在 TiDB v7.4.0 中，资源管控引入了对后台任务的自动管理。该功能有助于降低低优先级任务对在线业务的性能影响，实现资源的合理分配，大幅提升集群的稳定性。

    目前 TiDB 支持如下几种后台任务的类型：

    - `lightning`：使用 [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md) 执行导入任务。同时支持 TiDB Lightning 的物理和逻辑导入模式。
    - `br`：使用 [BR](/br/backup-and-restore-overview.md) 执行数据备份和恢复。目前不支持 PITR。
    - `ddl`：对于 Reorg DDL，控制批量数据回写阶段的资源使用。
    - `analyze`：对应手动执行或系统自动触发的[收集统计信息](/statistics.md#统计信息的收集)任务。

    默认情况下，被标记为后台任务的任务类型为空，此时后台任务的管理功能处于关闭状态，其行为与 TiDB v7.4.0 之前版本保持一致。你需要手动修改 `default` 资源组的后台任务类型以开启后台任务管理。

    更多信息，请参考[用户文档](/tidb-resource-control.md)。

* 增强锁定统计信息的能力 [#issue号](链接) @[hi-rustin](https://github.com/hi-rustin) **tw@ran-huang** <!--1557-->

    在 v7.4.0 中，TiDB 增强了[锁定统计信息](/statistics.md#锁定统计信息)的能力。现在，锁定和解锁统计信息需要赋予与收集统计信息 (`ANALYZE TABLE`) 相同的权限，以确保操作的安全性。此外，还新增了对特定分区的统计信息进行锁定和解锁操作的支持，提高了功能灵活性。当用户对数据库中的查询和执行计划有把握，并且不希望发生变化时，可以使用锁定统计信息来提升统计信息的稳定性。

    更多信息，请参考[用户文档](/statistics.md#锁定统计信息)。

### 高可用

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

### SQL 功能

* TiDB 支持完整的分区类型管理功能 [#42728](https://github.com/pingcap/tidb/issues/42728) @[mjonss](https://github.com/mjonss) **tw@qiancai** <!--1370-->

    在 v7.4.0 之前，TiDB 中的分区表不能调整分区类型。从 v7.4.0 开始，TiDB 支持将分区表修改为非分区表、将非分区表修改为分区表、修改分区类型功能。你可以根据需要灵活调整表的分区类型、数量。例如，通过 `ALTER TABLE t PARTITION BY ...` 语句修改分区类型。

    更多信息，请参考[用户文档](/partitioned-table.md#分区管理)。

* TiDB 支持 ROLLUP 修饰符和 GROUPING 函数 [#44487](https://github.com/pingcap/tidb/issues/44487) @[AilinKid](https://github.com/AilinKid) **tw@qiancai** <!--1287-->

    在 v7.4.0 之前，TiDB 不支持 ROLLUP 修饰符和 GROUPING 函数。ROLLUP 修饰符和 GROUPING 函数是数据分析中常用的功能，用于对数据进行分级汇总。从 v7.4.0 开始，TiDB 支持 ROLLUP 修饰符和 GROUPING 函数。ROLLUP 修饰符的使用方式为：`SELECT ... FROM ... GROUP BY ... WITH ROLLUP`

    更多信息，请参考[用户文档](/functions-and-operators/aggregate-group-by-functions.md#group-by-修饰符)。

### 数据库管理

* 新增排序规则 `utf8mb4_0900_ai_ci` 和 `utf8mb4_0900_bin` [#37566](https://github.com/pingcap/tidb/issues/37566) @[YangKeao](https://github.com/YangKeao) @[zimulala](https://github.com/zimulala) @[bb7133](https://github.com/bb7133) **tw@Oreoxmt** <!--1186-->

    TiDB v7.4.0 增强了从 MySQL 8.0 迁移数据的支持。新增两个排序规则 (Collation) `utf8mb4_0900_ai_ci` 和 `utf8mb4_0900_bin`。其中 `utf8mb4_0900_ai_ci` 为 MySQL 8.0 的默认排序规则。

    同时新增支持 MySQL 8.0 兼容的系统变量 `default_collation_for_utf8mb4`，允许用户为 utf8mb4 字符集指定默认的排序方式，以兼容从 MySQL 5.7 或之前版本迁移或数据复制的场景。

    更多信息，请参考[用户文档](/character-set-and-collation#支持的字符集和排序规则)。

### 可观测性

* 向日志中添加会话标识和会话别名 [#46071](https://github.com/pingcap/tidb/issues/46071) @[lcwangchao](https://github.com/lcwangchao) **tw@hfxsd** <!--无 FD 及用户文档，只提供 release notes-->

    在对 SQL 执行问题做故障定位的时候，经常需要把 TiDB 各组件日志中的内容进行关联，由此找到问题的根本原因。从 v7.4.0 开始，TiDB 将会话标识 (`CONNECTION_ID`) 写入与会话相关的日志内容中，包括 TiDB 日志、慢查询日志、以及 TiKV 上 coprocessor 的慢日志记录。你可以根据会话标识，将几个日志中的内容关联起来，提升故障定位和诊断的效率。 

    除此之外，通过设置会话级变量 [`tidb_session_alias`](/system-variables.md#tidb_session_alias-从-v740-版本开始引入)，你可以向上述日志中添加自定义的标识。借助这个能力，把业务识别信息注入日志，可以将日志中的内容与业务关联，打通了业务到日志的链路，降低了诊断工作的难度。

* TiDB Dashboard 提供表格视图的执行计划 [#1589](https://github.com/pingcap/tidb-dashboard/issues/1589) @[baurine](https://github.com/baurine) **tw@Oreoxmt** <!--1434-->

    在 v7.4.0 中，TiDB Dashboard 的 **Slow Query** 页面和 **SQL Statement** 页面提供表格视图的执行计划，以提升用户的诊断体验。

    更多信息，请参考[用户文档](链接)。

### 安全

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

### 数据迁移

* Data Migration (DM) 支持拦截不兼容（破坏数据一致性）的 DDL 变更（实验特性） [#9692](https://github.com/pingcap/tiflow/issues/9692) @[GMHDBJD](https://github.com/GMHDBJD) **tw@hfxsd** <!--1523-->

    在 v7.4.0 之前，使用 DM 的 Binlog Filter 功能颗粒度比较粗，例如只能过滤 ALTER 这种大颗粒度的 DDL Event，这种方式在某些业务场景会收到限制，例如业务允许将 Decimal 字段类型的精度调大，但是不允许减小。
    
    因此，在 v7.4.0 引入一个新的 Event Name `incompatible DDL changes`，用于拦截那些变更后会导致数据丢失、数据被截断、精度损失等问题的 DDL，并报错提示，让你可以及时介入处理，避免对下游的业务数据产生影响。

    更多信息，请参考[用户文档](链接)。

* 支持实时更新增量数据校验的 checkpoint [#issue号](链接) @[lichunzhu](https://github.com/lichunzhu) **tw@ran-huang** <!--1496-->

    在 v7.4.0 之前，你可以使用[增量数据校验功能](/dm/dm-continuous-data-validation.md)来判断 DM 同步到下游的数据是否与上游一致，并以此作为业务流量从上游数据库割接到 TiDB 的依据。然而，由于增量校验 checkpoint 受到较多限制，如同步延迟、不一致的数据等待重新校验等因素，需要每隔几分钟刷新一次校验后的 checkpoint。对于某些只有几十秒割接时间的业务场景来说，这是无法接受的。

    v7.4.0 引入实时更新增量数据校验的 checkpoint 后，你可以传入上游数据库填写的 binlog position。一旦增量校验程序在内存里校验到该 binlog postion，会立即刷新 checkpoint，而不是每隔几分钟刷新 checkpoint。因此，用户可以根据该立即返回的 checkpoint 来快速进行割接操作。

    更多信息，请参考[用户文档](链接)。

* 增强 `IMPORT INTO` 功能，支持对导入的数据通过云存储进行全局排序（实验特性），并提升导入性能和稳定性 [#46704](https://github.com/pingcap/tidb/issues/46704) @[D3Hunter](https://github.com/D3Hunter) **tw@qiancai** <!--1494-->

    从 v7.4.0 起，你可以通过在  `IMPORT INTO` 的 `CLOUD_STORAGE_URI` 选项中指定编码后数据的云存储地址，开启[全局排序功能](/....md)，提升性能和稳定性。
    
    此外，在 v7.4.0 中，`IMPORT INTO`  还引入了以下功能：
    
    - 支持配置 `Split_File` 选项，可将单个大 CSV 文件切分成多个 256 MiB 的小 CSV 文件进行并行处理，提升导入性能。
    - 支持导入压缩后的 CSV 和 SQL 文件，支持的压缩格式包括 `.gzip`、`.gz`、`.zstd`、`.zst` 和 `.snappy` 。`
·
    更多信息，请参考[用户文档](sql-statements/sql-statement-import-into.md)。
    
* Dumpling 在将数据导出为 CSV 文件时支持用户自定义换行符 [#46982](https://github.com/pingcap/tidb/issues/46982) @[GMHDBJD](https://github.com/GMHDBJD) **tw@hfxsd** <!--1571-->

    在 v7.4.0 之前，Dumpling 导出数据为 CSV 文件时，换行符默认为 "\r\n"，无法被一些只能解析 "\n" 换行符的下游系统解析该 CSV 文件，或者要通过第三方工具转换后才能解析。在 v7.4.0 引入了新的参数 `--csv-line-terminator`，你将数据导出为 CSV 文件时，可以通过该参数传入所需的换行符。该参数支持 "\r\n" 和 "\n" ，默认值为 "\r\n" ，即和历史版本保持一致。 

    更多信息，请参考[用户文档](链接)。
    
* TiCDC 支持同步数据至 Pulsar [#9413](https://github.com/pingcap/tiflow/issues/9413) @[yumchina](https://github.com/yumchina) @[asddongmen](https://github.com/asddongmen) **tw@hfxsd** <!--1552-->

    TiCDC 现在支持与 Pulsar 无缝集成。Pulsar 是一款云原生的分布式消息流平台，它可以提升您的实时数据流体验。借助这一新功能，TiCDC 赋予你轻松捕获和同步 TiDB 变更数据到 Pulsar 的能力，为数据处理和分析功能提供新的可能性。你可以开发自己的消费应用程序，从 Pulsar 中读取并处理新生成的变更数据，以满足特定的业务需求。TiCDC 目前支持以 `canal-json` 格式同步变更数据。

    更多信息，请参考[用户文档](/ticdc/ticdc-sink-to-pulsar.md)。

* TiCDC 支持 Claim-Check 功能，改进对大型消息的处理 [#9153](https://github.com/pingcap/tiflow/issues/9153) @[3AceShowHand](https://github.com/3AceShowHand) **tw@ran-huang** <!--1550 英文 comment 原文 https://internal.pingcap.net/jira/browse/FD-1550?focusedCommentId=149207&page=com.atlassian.jira.plugin.system.issuetabpanels:comment-tabpanel#comment-149207-->

    在 v7.4.0 之前，TiCDC 无法向下游发送超过 Kafka 最大消息大小 (`max.message.bytes`) 的大型消息。从  v7.4.0 开始，在配置下游为 Kafka 的 Changefeed 的时候，你可以指定一个外部存储位置，用于存储超过 Kafka 限制的大型消息，并将一条包含该大型消息在外部存储中的地址的引用消息发送到 Kafka。当消费者收到该引用消息后，可以根据其中记录的外部存储地址信息，获取对应的消息内容。

    更多信息，请参考[用户文档](链接)。

## 兼容性变更

> **注意：**
>
> 以下为从 v7.3.0 升级至当前版本 (v7.4.0) 所需兼容性变更信息。如果从 v7.2.0 或之前版本升级到当前版本，可能也需要考虑和查看中间版本 release notes 中提到的兼容性变更信息。

### 行为变更

<!-- 此小节包含 MySQL 兼容性变更-->

* 自 v7.4.0 起， TiDB 已经兼容 MySQL 8.0 的核心功能，`version()` 将返回以 `8.0.11` 为前缀的版本信息。 

* 兼容性 2

### 系统变量

| 变量名 | 修改类型 | 描述 |
|---|----|------|
| [`default_collation_for_utf8mb4`]() | 新增 | 为 utf8mb4 字符集选择默认排序方式， 兼容从 MySQL 5.7 或更旧版本的迁移或数据复制场景。 |
| [`tidb_opt_objective`](/system-variables.md#tidb_opt_objective-从-v740-版本开始引入) | 新增 | 该变量用于设置优化器优化目标。moderate 维持旧版本的默认行为，优化器会利用更多信息尝试生成更优的计划；determinate 则倾向于保守，保持执行计划稳定。 |
| [`tidb_session_alias`](/system-variables.md#tidb_session_alias-从-v740-版本开始引入) | 新增 | 用来自定义当前会话相关日志中 `session_alias` 列的值。 |
|  | 新增/删除/修改 |  |
|  | 新增/删除/修改 |  |

### 配置文件参数

| 配置文件 | 配置项 | 修改类型 | 描述 |
| -------- | -------- | -------- | -------- |
| Import into |SPLIT_FILE | 新增| 对需要导入的大型 CSV 文件切割成多个 256 MiB 大小的 CSV 文件|
| Dumpling  | `--csv-line-terminator` | 新增 | 你可以通过该参数传入导出数据为 CSV 文件的换行符，支持 "\r\n" 和 "\n"，默认值为 "\r\n"，即和历史版本保持一致。 |
|  | | 新增/删除/修改 | |
|  | | 新增/删除/修改 | |
|  | | 新增/删除/修改 | |
|  | | 新增/删除/修改 | |

## 改进提升

+ TiDB

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ TiKV

      - [内存优化]改进resolver的内存使用，防止OOM [#15458](https://github.com/tikv/tikv/issues/15458) @[overvenus](https://github.com/overvenus)
      - [内存优化]消除Router对象中的LRUCache，降低内存占用防止OOM[#15430](https://github.com/tikv/tikv/issues/15430) @[Connor1996](https://github.com/Connor1996)
      - [内存优化] 降低TICDC Resolver的内存使用 [#15412] (https://github.com/tikv/tikv/issues/15412) @[overvenus](https://github.com/overvenus)
      - [内存优化] 降低RocksDB compaction带来的内存抖动 [#15324] (https://github.com/tikv/tikv/issues/15324) @[overvenus](https://github.com/overvenus)
      - [内存优化] 降低Partitioned-raft-kv中流控模块的内存占用 [#15269] (https://github.com/tikv/tikv/issues/15269) @[overvenus](https://github.com/overvenus)
      - [PD调用优化]减少PD的MemberList请求[#15428](https://github.com/tikv/tikv/issues/15428)  @[nolouch](https://github.com/nolouch)
      - [动态调参]增加动态调整rocksdb background_compaction的支持[#15424](https://github.com/tikv/tikv/issues/15424)  @[glorv](https://github.com/glorv)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ PD

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ TiFlash
    - 改进 TiFlash 写入过程的落盘策略，提升随机写入负载下的写性能 [#7564](https://github.com/pingcap/tiflash/issues/7564) @[CalvinNeo](https://github.com/CalvinNeo)   **tw@qiancai** <!--1309-->

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

    - [Titan] 用lightning导入数据，挂起集群然后取消集群后，tikv陷入 CrashLoopBackOff[#15454](https://github.com/tikv/tikv/issues/15454)  @[Connor1996](https://github.com/Connor1996)
    - [监控] 修复Thread Voluntary/Nonvoluntary面板没有数据的问题 [#15413] (https://github.com/tikv/tikv/issues/15413) @[SpadeA-Tang] (https://github.com/SpadeA-Tang)
    - [监控] 修复raftstore-applys一直不断增长的数据错误[#15371](https://github.com/tikv/tikv/issues/15371)  @[Connor1996] (https://github.com/Connor1996)
    - [Jepsen] 修复由于meta数据不正确造成tikv的panic [#13311] (https://github.com/tikv/tikv/issues/13311) @[zyguan](https://github.com/zyguan]
    - [dr-autosync] 切换sync_recovery到sync之后qps掉0 [#15366] (https://github.com/tikv/tikv/issues/13366) @[nolouch](https://github.com/nolouch)
    - [dr-autosync] 当集群以sync-recover模式切换到备用集群后，在线恢复超时 [#15346] (https://github.com/tikv/tikv/issues/15346) @[Connor1996] (https://github.com/Connor1996)
    - [内存泄漏] 修复CpuRecord可能的内存泄漏 [#15304] (https://github.com/tikv/tikv/issues/15304) @[overvenus] (https://github.com/overvenus)
    - [dr-autosync] 当备用集群关闭后，主集群查询出现9002错误: tikv超时 [#12914] (https://github.com/tikv/tikv/issues/12914) @[Connor1996] (https://github.com/Connor1996)
    - [dr-autosync]当主集群恢复后tikv再次启动，dr tikv会卡住 [#12320] (https://github.com/tikv/tikv/issues/12320) @[disksing] (https://github.com/disksing)
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

+ [yumchina](https://github.com/yumchina)
