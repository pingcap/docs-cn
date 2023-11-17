---
title: TiDB 7.5.0 Release Notes
summary: 了解 TiDB 7.5.0 版本的新功能、兼容性变更、改进提升，以及错误修复。
---

# TiDB 7.5.0 Release Notes

发版日期：2023 年 x 月 x 日

TiDB 版本：7.5.0

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v7.5/quick-start-with-tidb) | [生产部署](https://docs.pingcap.com/zh/tidb/v7.5/production-deployment-using-tiup) | [下载离线包](https://cn.pingcap.com/product-community/?version=v7.5.0#version-list)

TiDB 7.5.0 为长期支持版本 (Long-Term Support Release, LTS)。

相比于前一个 LTS（即 7.1.0 版本），7.5.0 版本包含 [7.2.0-DMR](/releases/release-7.2.0.md)、[7.3.0-DMR](/releases/release-7.3.0.md) 和 [7.4.0-DMR](/releases/release-7.4.0.md) 中已发布的新功能、提升改进和错误修复。下表列出了从 7.2.0 到 7.5.0 的一些关键特性：

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
    <td>可扩展性与性能</td>
    <td>支持并行运行多个 <code>ADD INDEX</code> 语句 {/* tw@ran-huang */}</td>
    <td>与分布式和并行 DDL 任务不同，在该功能中，原来为同步运行的任务可以变为并发运行。以前同时运行 DDL 语句 X 和 Y 需要花费 X 的时间 + Y 的时间，并发运行后，DDL 总耗时显著减少了。尤其是在宽表的场景，内部测试数据显示最高性能可提升 94%。</td>
  </tr>
  <tr>
    <td rowspan="3">稳定性与高可用</td>
    <td><a href="https://docs.pingcap.com/tidb/v7.5/tidb-global-sort" target="_blank">Global sort</a> optimization {/* tw@ran-huang */}</td>
    <td>Laying the groundwork with the <a href="https://docs.pingcap.com/tidb/v7.5/tidb-distributed-execution-framework" target="_blank">distributed framework</a> in v7.2, TiDB introduces global sorting to eliminate the unnecessary I/O, CPU, and memory spikes caused from temporarily out of order data during data re-organization tasks. The global sorting will take advantage of external shared object storage (S3 in this first iteration) to store intermediary files during the job, adding flexibility and cost savings.Operations like ADD INDEX and IMPORT INTO will be faster, more resilient, more stable, more flexible, and cost less to run.</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/zh/tidb/v7.5/tidb-resource-control#管理后台任务" target="_blank">资源管控</a>支持自动管理后台任务（实验特性） {/* tw@Oreoxmt */}</td>
    <td>从 v7.1.0 开始，<a href="https://docs.pingcap.com/zh/tidb/v7.5/tidb-resource-control#use-resource-control-to-achieve-resource-isolation" target="_blank">资源管控</a>成为正式功能，该特性有助于缓解不同工作负载间的资源与存储访问干扰。TiDB v7.4.0 将此资源控制应用于后台任务。资源管控可以识别和管理后台任务，例如自动收集统计信息、备份和恢复、TiDB Lightning 批量数据导入以及在线 DDL。未来，所有后台任务都将纳入资源管控。</td>
  </tr>
  <tr>
    <td>资源组支持<a href="https://docs.pingcap.com/zh/tidb/v7.5/tidb-resource-control#管理资源消耗超出预期的查询-runaway-queries">管理资源消耗超出预期的查询</a>（实验特性）{/* tw@hfxsd */}</td>
    <td><a href="https://docs.pingcap.com/zh/tidb/v7.5/tidb-resource-control" target="_blank">资源管控 (Resource Group)</a> 是一个通过资源组 (Resource Group) 对工作负载进行资源隔离的框架，但它并不调用单个查询如何影响每个组内的工作。TiDB v7.2.0 引入了管控资源消耗超出预期的查询 (Runaway Queries)，你可以控制 TiDB 如何识别和处理每个资源组的查询。根据需要，长时间运行的查询可能会被终止或节流，你可以通过准确的 SQL test、SQL Digest 或其 Plan Digest来识别查询。在 TiDB v7.3.0，你可以主动监视已知的不良查询，类似于数据库级别的 SQL Blocklist。</td>
  </tr>
  <tr>
    <td>SQL</td>
    <td>MySQL 8.0 兼容性 {/* tw@Oreoxmt */}</td>
    <td>MySQL 8.0 的默认字符集为 utf8mb4，其默认排序规则是 <code>utf8mb4_0900_ai_ci</code>。TiDB v7.4.0 增强了与 MySQL 8.0 的兼容性。现在你可以更轻松地将在 MySQL 8.0 中使用默认排序规则创建的数据库迁移或复制到 TiDB。</td>
  </tr>
  <tr>
    <td rowspan="3">数据库管理与可观测性</td>
    <td><a href="https://docs.pingcap.com/zh/tidb/v7.5/sql-statement-import-into"><code>IMPORT INTO</code></a> 语句集成 TiDB Lightning 物理导入模式的能力 (GA) {/* tw@qiancai */}</td>
    <td>在 v7.2 之前，如需基于文件系统进行数据导入，你需要安装 <a href="https://docs.pingcap.com/zh/tidb/v7.5/tidb-lightning-overview">TiDB Lightning</a> 并使用其物理导入模式。目前，该功能已集成到 <code>IMPORT INTO</code> 语句中，你可以使用此语句快速导入数据，而无需安装任何额外的工具。该语句还支持<a href="https://docs.pingcap.com/zh/tidb/v7.5/tidb-distributed-execution-framework" target="_blank">分布式执行框架</a>，可分布式执行导入任务，提升了大规模数据导入时的效率。</td>
  </tr>
  <tr>
    <td>选择<a href="https://docs.pingcap.com/zh/tidb/v7.5/system-variables#tidb_service_scope-从-v740-版本开始引入" target="_blank">适用的 TiDB 节点</a>来并行执行 <code>ADD INDEX</code> 或 <code>IMPORT INTO</code> SQL 语句 (GA) {/* tw@hfxsd */}</td>
    <td>你可以选择在现有 TiDB 节点、或者新增 TiDB 节点执行 <code>ADD INDEX</code> 和 <code>IMPORT INTO</code> SQL 语句。该方法可以实现与其他 TiDB 节点的资源隔离，确保在执行上述语句时的最佳性能，并避免对已有业务造成性能影响。在 v7.5.0 中，该功能正式 GA。</td>
  </tr>
  <tr>
    <td>DDL 任务支持<a href="https://docs.pingcap.com/zh/tidb/v7.5/ddl-introduction#ddl-相关的命令介绍">暂停和恢复操作</a> {/* tw@ran-huang */}</td>
    <td>添加索引可能会消耗大量资源并影响在线流量。即使在资源组中进行了限制，或对标记的节点进行了隔离，你仍然可能需要在紧急情况下暂停这些任务。从 v7.2 开始，TiDB 原生支持同时暂停任意数量的后台任务，释放所需的资源，无需取消或重启任务。</td>
  </tr>
</tbody>
</table>

## 功能详情

### 可扩展性

* 支持设置 TiDB 节点的服务范围，用于选择适用的 TiDB 节点来执行并行的 `ADD INDEX` 或 `IMPORT INTO` 任务 (GA) [#46258](https://github.com/pingcap/tidb/issues/46258) @[ywqzzy](https://github.com/ywqzzy)<!--**tw@hfxsd** 1581-->

    在资源密集型集群中，并行执行 `ADD INDEX` 或 `IMPORT INTO` 任务可能占用大量 TiDB 节点的资源，从而导致集群性能下降。为了避免对已有业务造成性能影响，v7.4.0 以实验特性引入了变量 [`tidb_service_scope`](/system-variables.md#tidb_service_scope-从-v740-版本开始引入)，用于控制 [TiDB 后端任务分布式框架](/tidb-distributed-execution-framework.md)下各 TiDB 节点的服务范围。你可以从现有 TiDB 节点中选择几个节点，或者对新增 TiDB 节点设置服务范围，所有并行执行的 `ADD INDEX` 和 `IMPORT INTO` 的任务只会运行在这些节点。在 v7.5.0 中，该功能正式 GA。

    更多信息，请参考[用户文档](/system-variables.md#tidb_service_scope-从-v740-版本开始引入)。

### 性能

* TiDB 后端任务分布式并行执行框架成为正式功能 (GA)，提升并行执行的 `ADD INDEX` 或 `IMPORT INTO` 任务的性能和稳定性 [#45719](https://github.com/pingcap/tidb/issues/45719) @[wjhuang2016](https://github.com/wjhuang2016) <!--**tw@ran-huang** 1580-->

    在 v6.6.0 中引入的 TiDB 后端任务分布式并行执行框架成为正式功能 (GA)。TiDB v7.1.0 之前的版本中，在同一时间只有一个 TiDB 节点能够执行 DDL 任务。从 v7.1.0 开始，在分布式并行执行框架下，多个 TiDB 节点可以并行执行同一项 DDL 任务。从 v7.2.0 开始，分布式并行执行框架支持多个 TiDB 节点并行执行同一个 `IMPORT INTO` 任务，从而更好地利用 TiDB 集群的资源，大幅提升 DDL 和 `IMPORT INTO` 任务的性能。此外，你还可以通过增加 TiDB 节点来线性提升 DDL 和 `IMPORT INTO` 任务的性能。

    如果要使用分布式并行执行框架，只需将 [`tidb_enable_dist_task`](/system-variables.md#tidb_enable_dist_task-从-v710-版本开始引入) 的值设置为 `ON`：

    ```sql
    SET GLOBAL tidb_enable_dist_task = ON;
    ```

    更多信息，请参考[用户文档](/tidb-distributed-execution-framework.md)。

* 提升了在一个 SQL 语句中同时添加多个索引的性能 [#41602](https://github.com/pingcap/tidb/issues/41602) @[tangenta](https://github.com/tangenta) <!--**tw@ran-huang** 1582-->

    在 v7.5.0 之前，用户在一个 SQL 语句里添加多个索引 (`ADD INDEX`) 时，其性能与使用多个独立的 SQL 语句添加多个索引的性能接近。从 v7.5.0 起，在一个 SQL 语句中添加多个索引的性能有了显著的变化，尤其是在宽表的场景，内部测试数据显示最高性能可提升 94%。

### 数据库管理

* DDL 任务支持暂停和恢复操作成为正式功能 (GA) [#18015](https://github.com/pingcap/tidb/issues/18015) @[godouxm](https://github.com/godouxm) <!--**tw@ran-huang** 1611-->

    在 v7.2.0 中引入的 DDL 任务的暂停和恢复功能成为正式功能 (GA)。该功能允许临时暂停资源密集型的 DDL 操作（如创建索引），以节省资源并最小化对在线流量的影响。当资源允许时，你可以无缝恢复 DDL 任务，而无需取消和重新开始。DDL 任务的暂停和恢复功能提高了资源利用率，改善了用户体验，并简化了 schema 变更过程。

    你可以通过如下 `ADMIN PAUSE DDL JOBS` 或 `ADMIN RESUME DDL JOBS` 语句暂停或者恢复多个 DDL 任务：

    ```sql
    ADMIN PAUSE DDL JOBS 1,2;
    ADMIN RESUME DDL JOBS 1,2;
    ```

    更多信息，请参考[用户文档](/ddl-introduction.md#ddl-相关的命令介绍)。

* BR 支持备份和恢复统计信息 [#48008](https://github.com/pingcap/tidb/issues/48008) @[Leavrth](https://github.com/Leavrth) <!--**tw@hfxsd** 1437-->

    从 TiDB v7.5.0 开始，BR 备份工具支持备份和恢复数据库统计信息，在备份命令中引入了参数 `--ignore-stats`。当指定该参数值为 `false` 时，BR 备份工具支持备份和恢复数据库的列、索引、和表级别的统计信息。因此，从备份中恢复的 TiDB 数据库不再需要手动运行统计信息收集任务，也无需等待自动收集任务的完成，从而简化了数据库维护工作，并提升了查询性能。

    更多信息，请参考[用户文档](/br/br-snapshot-manual.md#备份统计信息)。

### 数据迁移

* `IMPORT INTO` SQL 语句成为正式功能 (GA) [#46704](https://github.com/pingcap/tidb/issues/46704) @[D3Hunter](https://github.com/D3Hunter)<!--**tw@qiancai** 1579-->

    在 v7.5.0 中，`IMPORT INTO` SQL 语句正式 GA。该语句集成了 TiDB Lightning [物理导入模式](/tidb-lightning/tidb-lightning-physical-import-mode.md)的能力，可以将 CSV、SQL 和 PARQUET 等格式的数据快速导入到 TiDB 的一张空表中。这种导入方式无需单独部署和管理 TiDB Lightning，在降低了数据导入难度的同时，大幅提升了数据导入效率。

    更多信息，请参考[用户文档](/sql-statements/sql-statement-import-into.md)。

* Data Migration (DM) 支持拦截不兼容（破坏数据一致性）的 DDL 变更 [#9692](https://github.com/pingcap/tiflow/issues/9692) @[GMHDBJD](https://github.com/GMHDBJD) <!--**tw@hfxsd** 1523-->

    在 v7.5.0 之前，使用 DM 的 Binlog Filter 功能只能迁移或过滤指定的 Event，且颗粒度比较粗，例如只能过滤 `ALTER` 这种大颗粒度的 DDL Event。这种方式在某些业务场景会受限，如业务允许 `ADD COLUMN`，但是不允许 `DROP COLUMN`，但之前的 DM 版本都会被 `ALTER` Event 过滤。

    因此，v7.5.0 细化了 DDL Event 的处理粒度，如支持过滤 `MODIFY COLUMN`（修改列数据类型）、`DROP COLUMN` 等会导致数据丢失、数据被截断、精度损失等问题的细粒度 DDL Event。你可以按需配置。同时还支持拦截不兼容的 DDL 变更，并报错提示，你可以及时介入手工处理，避免对下游的业务数据产生影响。

    更多信息，请参考[用户文档](/dm/dm-binlog-event-filter.md#参数解释)。

* 支持实时更新增量数据校验的 checkpoint [#8463](https://github.com/pingcap/tiflow/issues/8463) @[lichunzhu](https://github.com/lichunzhu) <!--**tw@ran-huang** 1496-->

    在 v7.5.0 之前，你可以使用[增量数据校验功能](/dm/dm-continuous-data-validation.md)来判断 DM 同步到下游的数据是否与上游一致，并以此作为业务流量从上游数据库割接到 TiDB 的依据。然而，由于增量校验 checkpoint 受到较多限制，如同步延迟、不一致的数据等待重新校验等因素，需要每隔几分钟刷新一次校验后的 checkpoint。对于某些只有几十秒割接时间的业务场景来说，这是无法接受的。

    v7.5.0 引入实时更新增量数据校验的 checkpoint 后，你可以传入上游数据库填写的 binlog 位置。一旦增量校验程序在内存里校验到该 binlog 位置，会立即刷新 checkpoint，而不是每隔几分钟刷新 checkpoint。因此，你可以根据该立即返回的 checkpoint 快速进行割接操作。

    更多信息，请参考[用户文档](/dm/dm-continuous-data-validation.md#设置增量校验切换点)。

## 兼容性变更

> **注意：**
>
> 以下为从 v7.4.0 升级至当前版本 (v7.5.0) 所需兼容性变更信息。如果从 v7.3.0 或之前版本升级到当前版本，可能也需要考虑和查看中间版本 Release Notes 中提到的兼容性变更信息。

### 系统变量

| 变量名  | 修改类型     | 描述 |
|--------|------------------------------|------|
| [`tidb_enable_fast_analyze`](/system-variables.md#tidb_enable_fast_analyze) | 废弃 | 用于控制是否启用统计信息快速分析功能。自 v7.5.0 起，统计信息快速分析功能被废弃。 |
| [`tidb_analyze_partition_concurrency`](/system-variables.md#tidb_analyze_partition_concurrency) |  修改 | 经进一步的测试后，默认值由 `1` 改为 `2`。 |
| [`tidb_build_stats_concurrency`](/system-variables.md#tidb_build_stats_concurrency) | 修改 | 经进一步的测试后，默认值由 `4` 改为 `2`。 |
| [`tidb_merge_partition_stats_concurrency`](/system-variables.md#tidb_merge_partition_stats_concurrency) | 修改 | 该变量从 v7.5.0 开始生效，用于设置 TiDB analyze 分区表时，对分区表统计信息进行合并时的并发度。 |
| [`tidb_build_sampling_stats_concurrency`](/system-variables.md#tidb_build_sampling_stats_concurrency-从-v750-版本开始引入) | 新增 | 设置 `ANALYZE` 过程中的采样并发度。 |
| [`tidb_enable_async_merge_global_stats`](/system-variables.md#tidb_enable_async_merge_global_stats-从-v750-版本开始引入) | 新增 | 设置 TiDB 使用异步方式合并统计信息，以避免 OOM 问题。|
| [`tidb_gogc_tuner_max_value`](/system-variables.md#tidb_gogc_tuner_max_value-从-v750-版本开始引入) | 新增 | 控制 GOGC Tuner 可调节 GOGC 的最大值。 |
| [`tidb_gogc_tuner_min_value`](/system-variables.md#tidb_gogc_tuner_min_value-从-v750-版本开始引入) | 新增 | 控制 GOGC Tuner 可调节 GOGC 的最小值。 |

### 配置文件参数

| 配置文件 | 配置项 | 修改类型 | 描述 |
| -------- | -------- | -------- | -------- |
| BR | [`--ignore-stats`](/br/br-snapshot-manual.md#备份统计信息) | 新增 | 用于备份和恢复数据库统计信息。当指定该参数值为 `false` 时，BR 备份工具支持备份和恢复数据库的列、索引、和表级别的统计信息。 |
| TiCDC | [`case-sensitive`](/ticdc/ticdc-changefeed-config.md) | 修改 | 经进一步的测试后，默认值由 `true` 改为 `false`，即默认情况下 TiCDC 配置文件中涉及的表名、库名大小写不敏感。 |
| TiCDC | [`sink.dispatchers.partition`](/ticdc/ticdc-changefeed-config.md) | 修改 | 控制增量数据的 Kafka Partition 分发策略，可选值新增 `columns` 选项，即使用明确指定的列值计算 partition 编号。 |
| TiCDC | [`sink.column-selectors`](/ticdc/ticdc-changefeed-config.md) | 新增 | 控制 TiCDC 将增量数据分发到 Kafka 时，只发送指定的列的数据变更事件。 |
| TiCDC | [`sql-mode`](/ticdc/ticdc-changefeed-config.md) | 新增 | 设置 TiCDC 解析 DDL 时使用的 SQL 模式，默认值和 TiDB 的默认 SQL 模式一致。 |
| TiDB Lightning | `--importer` | 删除 | 该配置项用于指定 TiKV-importer 的地址。从 v7.5.0 起，TiKV-importer 组件被废弃。 |

### 其他

## 离线包变更

从 v7.5.0 开始，`TiDB-community-toolkit` [二进制软件包](/binary-package.md)中移除了以下内容：<!--**tw@Oreoxmt** 1593+1594 -->

- `tikv-importer-{version}-linux-{arch}.tar.gz`
- `mydumper`
- `spark-{version}-any-any.tar.gz`
- `tispark-{version}-any-any.tar.gz`

## 废弃功能

* [Mydumper](https://docs.pingcap.com/zh/tidb/v4.0/mydumper-overview) 在 v7.5.0 中废弃，其绝大部分功能已经被 [Dumpling](/dumpling-overview.md) 取代，强烈建议切换到 Dumpling。<!--**tw@Oreoxmt** 1593-->

* TiKV-importer 组件在 v7.5.0 中废弃，建议使用 [TiDB Lightning 物理导入模式](/tidb-lightning/tidb-lightning-physical-import-mode.md)作为替代方案。<!--**tw@Oreoxmt** 1594-->

* 从 v7.5.0 开始，不再提供 [TiDB Binlog](/tidb-binlog/tidb-binlog-overview.md) 数据同步功能的技术支持，强烈建议使用 [TiCDC](/ticdc/ticdc-overview.md) 实现高效稳定的数据同步。尽管 TiDB Binlog 在 v7.5.0 仍支持 Point-in-Time Recovery (PITR) 场景，但是该组件在未来 LTS 版本中将被完全废弃，推荐使用 [PITR](/br/br-pitr-guide.md) 替代。<!--**tw@Oreoxmt** 1575-->

* 统计信息的[快速分析](/system-variables.md#tidb_enable_fast_analyze)（实验特性）在 v7.5.0 中废弃。<!--**tw@Oreoxmt** -->

* 统计信息的[增量收集](https://docs.pingcap.com/zh/tidb/v7.4/statistics#增量收集)（实验特性）在 v7.5.0 中废弃。<!--**tw@Oreoxmt** -->

## 改进提升

+ TiDB

    - 优化合并 GlobalStats 的并发模型：引入 [`tidb_enable_async_merge_global_stats`](/system-variables.md#tidb_enable_async_merge_global_stats-从-v750-版本开始引入) 实现同时加载统计信息并进行合并，从而加速分区表场景下 GlobalStats 的生成。同时优化合并 GlobalStats 的内存使用，以避免 OOM 并减少内存分配 [#47219](https://github.com/pingcap/tidb/issues/47219) @[hawkingrei](https://github.com/hawkingrei) <!--**tw@hfxsd** -->
    - 优化 `ANALYZE` 流程：引入 [`tidb_build_sampling_stats_concurrency`](/system-variables.md#tidb_build_sampling_stats_concurrency-从-v750-版本开始引入) 精细化控制 `ANALYZE` 并发度，减少资源消耗。同时优化 `ANALYZE` 的内存使用，通过复用部分中间结果，减少内存分配，避免频繁 GC [#47275](https://github.com/pingcap/tidb/issues/47275) @[hawkingrei](https://github.com/hawkingrei) <!--**tw@hfxsd** -->
    - 改进 Placement Policy 的使用：增加对全局范围的策略配置，完善常用场景的语法支持 [#45384](https://github.com/pingcap/tidb/issues/45384) @[nolouch](https://github.com/nolouch) <!--**tw@qiancai** -->
    <!--**tw@Oreoxmt**: 1-->
    - 提升启用索引加速功能 `tidb_ddl_enable_fast_reorg` 后添加索引的性能，在内部测试中 v7.5.0 相比 v6.5.0 性能最高提升 62.5% [#47757](https://github.com/pingcap/tidb/issues/47757) @[tangenta](https://github.com/tangenta)

+ TiKV

    - (dup): release-7.1.2.md > 改进提升> TiKV - 避免写 Titan manifest 文件时持有锁导致影响其他线程 [#15351](https://github.com/tikv/tikv/issues/15351) @[Connor1996](https://github.com/Connor1996)

+ PD

  <!--**tw@Oreoxmt**: 1-->
    - 提升 `evict-slow-trend` 调度的稳定性和易用性 [#7156](https://github.com/tikv/pd/issues/7156) @[LykxSassinato](https://github.com/LykxSassinator)

+ TiFlash

+ Tools

    + Backup & Restore (BR)

      <!--**tw@Oreoxmt**: 1-->
        - 快照备份恢复支持通过 AWS 会话令牌和 IAM 角色设置权限 [#39832](https://github.com/pingcap/tidb/issues/39832) @[3pointer](https://github.com/3pointer)

    + TiCDC

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

  <!--**tw@ran-huang**: 4-->
    - (dup): release-7.1.2.md > 错误修复> TiDB - 禁止非整型聚簇索引进行 split table 操作 [#47350](https://github.com/pingcap/tidb/issues/47350) @[tangenta](https://github.com/tangenta)
    - (dup): release-7.1.2.md > 错误修复> TiDB - 修复使用错误的时区信息对时间字段进行编码的问题 [#46033](https://github.com/pingcap/tidb/issues/46033) @[tangenta](https://github.com/tangenta)
    - (dup): release-7.1.2.md > 错误修复> TiDB - 修复 Sort 算子在落盘过程中可能导致 TiDB 崩溃的问题 [#47538](https://github.com/pingcap/tidb/issues/47538) @[windtalker](https://github.com/windtalker)
    - (dup): release-7.1.2.md > 错误修复> TiDB - 修复查询使用 `GROUP_CONCAT` 时报错 `Can't find column` 的问题 [#41957](https://github.com/pingcap/tidb/issues/41957) @[AilinKid](https://github.com/AilinKid)
    - (dup): release-7.1.2.md > 错误修复> TiDB - 修复 `client-go` 中 `batch-client` panic 的问题 [#47691](https://github.com/pingcap/tidb/issues/47691) @[crazycs520](https://github.com/crazycs520)
    - 修复 INDEX_LOOKUP_HASH_JOIN 内存使用量估算错误的问题 [#47788](https://github.com/pingcap/tidb/issues/47788) @[SeaRise](https://github.com/SeaRise)
    - 修复长时间下线的 TiFlash 节点重新加入集群后造成的负载不均衡的问题 [#35418](https://github.com/pingcap/tidb/issues/35418) @[windtalker](https://github.com/windtalker)
    - 修复 HashJoin 算子 Probe 时 Chunk 无法复用的问题 [#48082](https://github.com/pingcap/tidb/issues/48082) @[wshwsh12](https://github.com/wshwsh12)
    - 修复 COALESCE 函数对于 Date 类型参数返回结果类型不正确的问题 [#46475](https://github.com/pingcap/tidb/issues/46475) @[xzhangxian1008](https://github.com/xzhangxian1008)

+ TiKV

    - (dup): release-5.4.0.md > Bug 修复> TiKV - 修复悲观事务中 prewrite 请求重试在极少数情况下影响数据一致性的风险 [#11187](https://github.com/tikv/tikv/issues/11187)

+ PD

  <!--**tw@qiancai**: 8-->
    - (dup): release-7.1.2.md > 错误修复> PD - 修复 `evict-leader-scheduler` 丢失配置的问题 [#6897](https://github.com/tikv/pd/issues/6897) @[HuSharp](https://github.com/HuSharp)
    - 修复 store 下线后对应的打点统计数据未删除的问题 [#7180](https://github.com/tikv/pd/issues/7180) @[rleungx](https://github.com/rleungx)
    - 修复 DR-AutoSync 在 Placement Rule 配置比较复杂时，canSync 和 hasMajority 可能计算错误的问题 [#7201](https://github.com/tikv/pd/issues/7201) @[disksing](https://github.com/disksing)
    - 修复 rule checker 未按照设定的 Placement Rule 添加 Learner 的问题 [#7185](https://github.com/tikv/pd/issues/7185) @[nolouch](https://github.com/nolouch)
    - 修复 TiDB Dashboard 不能正常抓取 PD Trace 数据的问题 [#7253](https://github.com/tikv/pd/issues/7253) @[nolouch](https://github.com/nolouch)
    - 修复 PD 内部获取的 Region 可能为空导致 PD Panic 的问题 [#7261](https://github.com/tikv/pd/issues/7261) @[lhy1024](https://github.com/lhy1024)
    - 修复 DR-AutoSync available_stores 计算错误的问题 [#7221](https://github.com/tikv/pd/issues/7221) @[disksing](https://github.com/disksing)
    - 修复 TiKV 节点不可用时有一定几率删除正常 Peers 的问题 [#7249](https://github.com/tikv/pd/issues/7249) @[lhy1024](https://github.com/lhy1024)
    - 修复在大集群中添加多个 TiKV 节点可能导致 TiKV 心跳上报变慢或卡住的问题 [#7248](https://github.com/tikv/pd/issues/7248) @[rleungx](https://github.com/rleungx)

+ TiFlash

  <!--**tw@Oreoxmt**: 3-->
    - 修复 `UPPER()` 和 `LOWER()` 函数在 TiDB 和 TiFlash 中计算结果不一致的问题 [#7695](https://github.com/pingcap/tiflash/issues/7695) @[windtalker](https://github.com/windtalker)
    - 修复在空分区上执行查询报错的问题 [#8220](https://github.com/pingcap/tiflash/issues/8220) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复同步 TiFlash 副本时可能创建表失败导致 panic 的问题 [#8217](https://github.com/pingcap/tiflash/issues/8217) @[hongyunyan](https://github.com/hongyunyan)

+ Tools

    + Backup & Restore (BR)

      <!--**tw@Oreoxmt**: 1-->
        - (dup): release-7.1.2.md > 错误修复> Tools> Backup & Restore (BR) - 修复 PITR 可能跳过恢复 `CREATE INDEX` DDL 的问题 [#47482](https://github.com/pingcap/tidb/issues/47482) @[Leavrth](https://github.com/Leavrth)
        - 修复大宽表场景下，日志备份在某些场景中可能卡住的问题 [#15714](https://github.com/tikv/tikv/issues/15714) @[YuJuncen](https://github.com/YuJuncen)

    + TiCDC

      <!--**tw@hfxsd**: 8-->
        - 修复同步数据到对象存储时访问 NFS 目录导致的性能问题 [#10041](https://github.com/pingcap/tiflow/issues/10041) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - 修复开启 `claim-check` 导致时存储路径拼写错误的问题 [#10036](https://github.com/pingcap/tiflow/issues/10036) @[3AceShowHand](https://github.com/3AceShowHand)
        - 修复开启 `column filter` 时列设置错误的问题 [#10042](https://github.com/pingcap/tiflow/issues/10042) @[3AceShowHand](https://github.com/3AceShowHand)
        - 修复 TiCDC 在某些情况下调度不均衡的问题 [#9845](https://github.com/pingcap/tiflow/issues/9845) @[3AceShowHand](https://github.com/3AceShowHand)
        - 修复同步数据到 Kafka 时可能丢失 Callback 的问题 [#9855](https://github.com/pingcap/tiflow/issues/9855) @[hicqu](https://github.com/hicqu)
        - 修复某些场景下 Processor 可能 panic 的问题 [#9849](https://github.com/pingcap/tiflow/issues/9849) [#9915](https://github.com/pingcap/tiflow/issues/9915) @[hicqu](https://github.com/hicqu) @[3AceShowHand](https://github.com/3AceShowHand)
        - 修复开启 `kv-client.enable-multiplexing` 导致同步任务卡住的问题 [#9673](https://github.com/pingcap/tiflow/issues/9673) @[fubinzh](https://github.com/fubinzh)
        - 修复开启 Redo log 时，NFS 出现故障导致 Owner 节点卡住的问题 [#9886](https://github.com/pingcap/tiflow/issues/9886) @[3AceShowHand](https://github.com/3AceShowHand)

    + TiDB Data Migration (DM)

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiDB Lightning

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiUP

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

## 性能测试

如需了解 TiDB v7.5.0 的性能表现，你可以参考 TiDB Dedicated 集群的 [TPC-C 性能测试报告](https://docs.pingcap.com/tidbcloud/v7.5.0-performance-benchmarking-with-tpcc)和 [Sysbench 性能测试报告](https://docs.pingcap.com/tidbcloud/v7.5.0-performance-benchmarking-with-sysbench)（英文版）。

## 贡献者

感谢来自 TiDB 社区的贡献者们：

- [jgrande](https://github.com/jgrande)（首次贡献者）
- [shawn0915](https://github.com/shawn0915)
