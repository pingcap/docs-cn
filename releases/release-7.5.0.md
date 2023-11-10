---
title: TiDB 7.5.0 Release Notes
summary: 了解 TiDB 7.5.0 版本的新功能、兼容性变更、改进提升，以及错误修复。
---

# TiDB 7.5.0 Release Notes

发版日期：2023 年 x 月 x 日

TiDB 版本：7.5.0

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v7.5/quick-start-with-tidb) | [生产部署](https://docs.pingcap.com/zh/tidb/v7.5/production-deployment-using-tiup) | [下载离线包](https://cn.pingcap.com/product-community/?version=v7.5.0#version-list)

TiDB 7.5.0 为长期支持版本 (Long-Term Support Release, LTS)。

相比于前一个 LTS（即 7.1.0 版本），7.5.0 版本包含 [7.2.0-DMR](/releases/release-7.2.0.md)、[7.3.0-DMR](/releases/release-7.3.0.md) 和 [7.4.0-DMR](/releases/release-7.4.0.md) 中已发布的新功能、提升改进和错误修复，并引入了以下关键特性：

<table>
<thead>
  <tr>
    <th>Category</th>
    <th>Feature</th>
    <th>Description</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>Scalability and Performance</td>
    <td>Support for running multiple <code>ADD INDEX</code> statements in parallel {/* tw@ran-huang */}</td>
    <td>Different from distributed and parallel DDL jobs, this feature allows for concurrent jobs to run where they were otherwise running syncrhonsously. Where running DDL statements x, y at the same time used to take x-time +y-time, they now take significantly less.</td>
  </tr>
  <tr>
    <td rowspan="3">Reliability and Availability</td>
    <td><a href="https://docs.pingcap.com/tidb/v7.5/tidb-global-sort" target="_blank">Global sort</a> optimization {/* tw@ran-huang */}</td>
    <td>Laying the groundwork with the <a href="https://docs.pingcap.com/tidb/v7.5/tidb-distributed-execution-framework" target="_blank">distributed framework</a> in v7.2, TiDB introduces global sorting to eliminate the unnecessary I/O, CPU, and memory spikes caused from temporarily out of order data during data re-organization tasks. The global sorting will take advantage of external shared object storage (S3 in this first iteration) to store intermediary files during the job, adding flexibility and cost savings.Operations like ADD INDEX and IMPORT INTO will be faster, more resilient, more stable, more flexible, and cost less to run.</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/tidb/v7.5/tidb-resource-control#manage-background-tasks" target="_blank">Resource control</a> for background tasks (experimental) {/* tw@Oreoxmt */}</td>
    <td>In v7.1.0, the <a href="https://docs.pingcap.com/tidb/v7.5/tidb-resource-control#use-resource-control-to-achieve-resource-isolation" target="_blank">Resource Control</a> feature was introduced to mitigate resource and storage access interference between workloads. TiDB v7.4.0 applies this control to background tasks as well. In v7.4.0, Resource Control now identifies and manages the resources produced by background tasks, such as auto-analyze, Backup & Restore, bulk load with TiDB Lightning, and online DDL. This will eventually apply to all background tasks.</td>
  </tr>
  <tr>
    <td>Resource groups support <a href="https://docs.pingcap.com/tidb/v7.5/tidb-resource-control#manage-queries-that-consume-more-resources-than-expected-runaway-queries"> managing runaway queries</a> (experimental) {/* tw@hfxsd */}</td>
    <td><a href="https://docs.pingcap.com/tidb/v7.5/tidb-resource-control#use-resource-control-to-achieve-resource-isolation" target="_blank">Resource Control</a> is a framework for resource-isolating workloads by Resource Groups, but it makes no calls on how individual queries affect work inside of each group. TiDB v7.2 introduced "runaway query conrol" to let operators control how TiDB identifies and treats these queries per Resource Group. Depending on need, long running queries may be terminated or throttled, and the queries can be identified by exact SQL text or their plan digests, for better generalization. In v7.4, TiDB allows operators to proactively watch for known bad queries, similar to a SQL blocklist at the database level. </td>
  </tr>
  <tr>
    <td>SQL</td>
    <td>MySQL 8.0 compatibility {/* tw@Oreoxmt */}</td>
    <td>In MySQL 8.0, the default characterset is utf8mb4, and the default collation of utf8mb4 is <code>utf8mb4_0900_ai_ci</code>. TiDB v7.4.0 adding support for this enhances compatibility with MySQL 8.0 so that migrations and replications from MySQL 8.0 databases with the default collation are now much smoother.</td>
  </tr>
  <tr>
    <td rowspan="3">DB Operations and Observability</td>
    <td>TiDB Lightning's physical import mode integrated into TiDB with <a href="https://docs.pingcap.com/tidb/v7.5/sql-statement-import-into">IMPORT INTO</a> {/* tw@qiancai */}</td>
    <td>Prior to v7.2, file system level (backdoor) importing was done with <a href="https://docs.pingcap.com/tidb/v7.5/tidb-lightning-overview">TiDB Lightning</a>. The same functionality is now incorporated into TiDB server nodes and is operated by the SQL interface using the IMPORT INTO command. This feature also uses the new distributed execution framework and global sort feature, which speeds it up and allows for more stability during very large imports (i.e., 100TB tables).</td>
  </tr>
  <tr>
    <td>Specify<a href="https://docs.pingcap.com/tidb/v7.5/system-variables#tidb_service_scope-new-in-v740" target="_blank"> the respective TiDB nodes</a> to execute the <code>IMPORT INTO</code> and <code>ADD INDEX</code> SQL statements (experimental) {/* tw@hfxsd */}</td>
    <td>You have the flexibility to specify whether to execute <code>IMPORT INTO</code> or <code>ADD INDEX</code> SQL statements on some of the existing TiDB nodes or newly added TiDB nodes. This approach enables resource isolation from the rest of the TiDB nodes, preventing any impact on business operations while ensuring optimal performance for executing the preceding SQL statements.</td>
  </tr>
  <tr>
    <td>DDL supports <a href="https://docs.pingcap.com/tidb/v7.5/ddl-introduction#ddl-related-commands">pause and resume operations</a> {/* tw@ran-huang */}</td>
    <td>Adding indexes can be big resource consumers and can affect online traffic. Even when throttled in a Resource Group or isolated to labeled nodes, there may still be a need to suspend these jobs in emergencies. As of v7.2, TiDB now natively supports suspending any number of these background jobs at once, freeing up needed resources while avoiding have to cancel and restart the jobs.</td>
  </tr>
</tbody>
</table>

## 功能详情

### 可扩展性

* 支持设置 TiDB 节点的服务范围，用于选择适用的 TiDB 节点来执行并行的 `ADD INDEX` 或 `IMPORT INTO` 任务 (GA) [#46258](https://github.com/pingcap/tidb/issues/46258) @[ywqzzy](https://github.com/ywqzzy)<!--**tw@hfxsd** 1581-->

    在资源密集型集群中，并行执行 `ADD INDEX` 或 `IMPORT INTO` 任务可能占用大量 TiDB 节点的资源，从而导致集群性能下降。为了避免对已有业务造成性能影响，v7.4.0 以试验特性引入了变量 [`tidb_service_scope`](/system-variables.md#tidb_service_scope-从-v740-版本开始引入)，用于控制 [TiDB 后端任务分布式框架](/tidb-distributed-execution-framework.md)下各 TiDB 节点的服务范围。你可以从现有 TiDB 节点中选择几个节点，或者对新增 TiDB 节点设置服务范围，所有并行执行的 `ADD INDEX` 和 `IMPORT INTO` 的任务只会运行在这些节点。在 v7.5.0 中，该功能正式 GA。

    更多信息，请参考[用户文档](/system-variables.md#tidb_service_scope-从-v740-版本开始引入)。

### 性能

* TiDB 后端任务分布式并行执行框架成为正式功能（GA），其中基于云存储的全局排序功能也成为正式功能，提升并行执行的 `ADD INDEX` 或 `IMPORT INTO` 任务的性能和稳定性 [#45719](https://github.com/pingcap/tidb/issues/45719) @[wjhuang2016](https://github.com/wjhuang2016) <!--**tw@ran-huang** 1580-->

    在 v7.4.0 以前，当用户执行分布式并行执行框架的 `ADD INDEX` 或 `IMPORT INTO` 任务时，TiDB 节点需要准备一块较大的本地磁盘，对编码后的索引 KV pairs 和表数据 KV pairs 进行排序。由于无法从全局角度进行排序，各个 TiDB 节点间以及节点内部导入的数据可能存在重叠情况。这会导致在将这些 KV pairs 导入到 TiKV 时，TiKV 需要频繁进行数据整理 (compaction)，降低了 `ADD INDEX` 或 `IMPORT INTO` 的性能和稳定性。

    v7.4.0 引入全局排序特性后，编码后的数据不再写入本地进行排序，而是写入云存储，并在云存储中进行全局排序。然后，TiDB 将经过全局排序的索引数据和表数据并行导入到 TiKV 中，从而提升了性能和稳定性。

    更多信息，请参考[用户文档](/tidb-global-sort.md)。

* 提升了在一个 SQL 语句中同时添加多个索引的性能 [#41602](https://github.com/pingcap/tidb/issues/41602) @[tangenta](https://github.com/tangenta) <!--**tw@ran-huang** 1582-->

    在 v7.5.0 之前，用户在一个 SQL 语句里添加多个索引 (`ADD INDEX`) 时，其性能与使用多个独立的 SQL 语句添加多个索引的性能接近。从 v7.5.0 起，在一个 SQL 语句中添加多个索引的性能有了显著的变化，提升了 XX （等待最终测试结果数据），可大大缩短业务添加索引所需的时间。

### 稳定性

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接)

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

### 高可用

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接)

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

### SQL 功能

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接)

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。


### 数据库管理

* DDL 任务支持暂停和恢复操作成为正式功能 (GA) [#issue](issue链接) @[contributor](https://github.com/xxx) <!--**tw@ran-huang** 1611-->

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

### 可观测性

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接)

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

### 安全

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接)

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

### 数据迁移

* `IMPORT INTO` SQL 语句成为正式功能（GA）[#46704](https://github.com/pingcap/tidb/issues/46704) @[D3Hunter](https://github.com/D3Hunter)<!--**tw@qiancai** 1579-->

   在 v7.5.0 中，`IMPORT INTO` SQL 语句正式 GA。该语句集成了 TiDB Lightning [物理导入模式](/tidb-lightning/tidb-lightning-physical-import-mode.md)的能力，可以将 CSV、SQL 和 PARQUET 等格式的数据快速导入到 TiDB 的一张空表中。这种导入方式无需单独部署和管理 TiDB Lightning，在降低了数据导入难度的同时，大幅提升了数据导入效率。

  此外，你可以通过在 `IMPORT INTO` 的 `CLOUD_STORAGE_URI` 选项中指定编码后数据的云存储地址，开启[全局排序功能](/tidb-global-sort.md)，提升导入的性能和稳定性。

    更多信息，请参考[用户文档](/sql-statements/sql-statement-import-into.md)。

* Data Migration (DM) 支持拦截不兼容（破坏数据一致性）的 DDL 变更 [#9692](https://github.com/pingcap/tiflow/issues/9692) @[GMHDBJD](https://github.com/GMHDBJD) <!--**tw@hfxsd** 1523-->

    在 v7.5.0 之前，使用 DM 的 Binlog Filter 功能只能迁移或过滤指定的 Event，且颗粒度比较粗，例如只能过滤 `ALTER` 这种大颗粒度的 DDL Event。这种方式在某些业务场景会受限，如业务允许 `ADD COLUMN`，但是不允许 `DROP COLUMN`，但之前的 DM 版本都会被 `ALTER` Event 过滤。

    因此，v7.5.0 细化了 DDL Event 的处理粒度，如支持过滤 `MODIFY COLUMN`（修改列数据类型）、`DROP COLUMN` 等会导致数据丢失、数据被截断、精度损失等问题的细粒度 DDL Event。你可以按需配置。同时还支持拦截不兼容的 DDL 变更，并报错提示，你可以及时介入手工处理，避免对下游的业务数据产生影响。

    更多信息，请参考[用户文档](/dm/dm-binlog-event-filter.md#参数解释)。

* 支持实时更新增量数据校验的 checkpoint [issue号](链接) @[lichunzhu](https://github.com/lichunzhu) <!--**tw@ran-huang** 1496-->

    在 v7.5.0 之前，你可以使用[增量数据校验功能](/dm/dm-continuous-data-validation.md)来判断 DM 同步到下游的数据是否与上游一致，并以此作为业务流量从上游数据库割接到 TiDB 的依据。然而，由于增量校验 checkpoint 受到较多限制，如同步延迟、不一致的数据等待重新校验等因素，需要每隔几分钟刷新一次校验后的 checkpoint。对于某些只有几十秒割接时间的业务场景来说，这是无法接受的。

    v7.5.0 引入实时更新增量数据校验的 checkpoint 后，你可以传入上游数据库填写的 binlog 位置。一旦增量校验程序在内存里校验到该 binlog 位置，会立即刷新 checkpoint，而不是每隔几分钟刷新 checkpoint。因此，你可以根据该立即返回的 checkpoint 快速进行割接操作。

    更多信息，请参考[用户文档](/dm/dm-continuous-data-validation.md#设置增量校验切换点)。

## 兼容性变更

> **注意：**
>
> 以下为从 v7.4.0 升级至当前版本 (v7.5.0) 所需兼容性变更信息。如果从 v7.3.0 或之前版本升级到当前版本，可能也需要考虑和查看中间版本 Release Notes 中提到的兼容性变更信息。

### 行为变更

* 行为变更 1

* 行为变更 2

### MySQL 兼容性

* 兼容性 1

* 兼容性 2

### 系统变量

| 变量名  | 修改类型（包括新增/修改/删除）    | 描述 |
|--------|------------------------------|------|
|  [`tidb_build_sampling_stats_concurrency`](/system-variables.md#tidb_build_sampling_stats_concurrency-从-v750-版本开始引入)      |   新增 | 该变量用来设置 `ANALYZE` 过程中的采样并发度。     |
|  [`tidb_enable_async_merge_global_stats`](/system-variables.md#tidb_enable_async_merge_global_stats-从-v750-版本开始引入)      |   新增 | 该变量用于 TiDB 使用异步方式合并统计信息, 以避免 OOM 问题。    |
|        |                              |      |
|        |                              |      |
|        |                              |      |

### 配置文件参数

| 配置文件 | 配置项 | 修改类型 | 描述 |
| -------- | -------- | -------- | -------- |
|    BR      |   [`--ignore-stats`](/br/br-snapshot-manual.md#备份统计信息)       |   新增       |   用于备份和恢复数据库统计信息。当指定该参数值为 `false` 时，BR 备份工具支持备份和恢复数据库的列、索引、和表级别的统计信息。      |
| TiCDC | [`sink.column-selectors`](/ticdc/ticdc-changefeed-config.md) | 新增 | 控制 TiCDC 将增量数据分发到 Kafka 时，只发送指定的列的数据变更事件。 |
| TiCDC | [`sink.dispatchers.partition`](/ticdc/ticdc-changefeed-config.md) | 修改 | 控制增量数据的 Kafka Partition 分发策略，可选值新增 `columns` 选项，即使用明确指定的列值计算 partition 编号。 |
| TiCDC | [`sql-mode`](/ticdc/ticdc-changefeed-config.md) | 新增 | 设置 TiCDC 解析 DDL 时使用的 SQL 模式，默认值和 TiDB 的默认 SQL 模式一致。 |
|          |          |          |          |

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

* 统计信息的[快速分析](https://docs.pingcap.com/zh/tidb/v7.4/system-variables#tidb_enable_fast_analyze)（实验特性）在 v7.5.0 中废弃。<!--**tw@Oreoxmt** -->

* 统计信息的[增量收集](https://docs.pingcap.com/zh/tidb/v7.4/statistics#增量收集)（实验特性）在 v7.5.0 中废弃。<!--**tw@Oreoxmt** -->

## 改进提升

+ TiDB

    - 优化合并 GlobalStats 的并发模型：引入 [`tidb_enable_async_merge_global_stats`](/system-variables.md#tidb_enable_async_merge_global_stats-从-v750-版本开始引入) 实现同时加载统计信息并进行合并，从而加速分区表场景下 GlobalStats 的生成。同时优化合并 GlobalStats 的内存使用，以避免 OOM 并减少内存分配 [#47219](https://github.com/pingcap/tidb/issues/47219) @[hawkingrei](https://github.com/hawkingrei) <!--**tw@hfxsd** -->
    - 优化 `ANALYZE` 流程：引入 [`tidb_build_sampling_stats_concurrency`](/system-variables.md#tidb_build_sampling_stats_concurrency-从-v750-版本开始引入) 精细化控制 `ANALYZE` 并发度，减少资源消耗。同时优化 `ANALYZE` 的内存使用，通过复用部分中间结果，减少内存分配，避免频繁 GC [#47275](https://github.com/pingcap/tidb/issues/47275) @[hawkingrei](https://github.com/hawkingrei) <!--**tw@hfxsd** -->
    - 改进 Placement Policy 的使用：增加对全局范围的策略配置，完善常用场景的语法支持  [#45384](https://github.com/pingcap/tidb/issues/45384) @[nolouch](https://github.com/nolouch) <!--**tw@qiancai** -->

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

## 性能测试

如需了解 TiDB v7.5.0 的性能表现，你可以参考 TiDB Dedicated 集群的 [TPC-C 性能测试报告](https://docs.pingcap.com/tidbcloud/v7.5.0-performance-benchmarking-with-tpcc)和 [Sysbench 性能测试报告](https://docs.pingcap.com/tidbcloud/v7.5.0-performance-benchmarking-with-sysbench)（英文版）。

## 贡献者

感谢来自 TiDB 社区的贡献者们：

- [贡献者 GitHub ID]()
