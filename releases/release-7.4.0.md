---
title: TiDB 7.4.0 Release Notes
summary: 了解 TiDB 7.4.0 版本的新功能、兼容性变更、改进提升，以及错误修复。
---

# TiDB 7.4.0 Release Notes

发版日期：2023 年 10 月 12 日

TiDB 版本：7.4.0

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v7.4/quick-start-with-tidb) | [下载离线包](https://cn.pingcap.com/product-community/?version=v7.4.0-DMR#version-list)

在 7.4.0 版本中，你可以获得以下关键特性：

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
    <td rowspan="3">稳定性与高可用</td>
    <td>引入<a href="https://docs.pingcap.com/zh/tidb/v7.4/tidb-global-sort" target="_blank">全局排序能力</a>，提升<code>IMPORT INTO</code>和<code>ADD INDEX</code>任务的性能和稳定性（实验特性）</td>
    <td>在 v7.4.0 以前，使用<a href="https://docs.pingcap.com/zh/tidb/v7.4/tidb-distributed-execution-framework" target="_blank">分布式并行执行框架</a>执行 <code>ADD INDEX</code> 或 <code>IMPORT INTO</code> 等任务时，只能对部分数据进行局部排序。这导致 TiKV 需要采取额外操作，并且在将数据导入到 TiKV 之前，TiDB 节点还需要为其分配本地磁盘空间以进行排序。<br/>随着 v7.4.0 引入全局排序特性，可以将数据暂时存储在外部存储（如 S3）中进行全局排序后再导入到 TiKV 中。这一改进降低了 TiKV 对资源的额外消耗，并显著提高了 <code>ADD INDEX</code> 和 <code>IMPORT INTO</code> 等操作的性能和稳定性。</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/zh/tidb/v7.4/tidb-resource-control#管理后台任务" target="_blank">资源管控</a>支持自动管理后台任务（实验特性）</td>
    <td>从 v7.1.0 开始，资源管控成为正式功能，该特性有助于缓解不同工作负载间的资源与存储访问干扰。TiDB v7.4.0 将此资源控制应用于后台任务。资源管控可以识别和管理后台任务，例如自动收集统计信息、备份和恢复、TiDB Lightning 批量数据导入以及在线 DDL。未来，所有后台任务都将纳入资源管控。</td>
  </tr>
  <tr>
    <td>TiFlash 支持<a href="https://docs.pingcap.com/zh/tidb/v7.4/tiflash-disaggregated-and-s3" target="_blank">存储计算资源分离和 S3 共享存储</a> (GA) </td>
    <td>TiFlash 存算分离架构和 S3 共享存储成为正式功能：
      <ul>
        <li>支持分离 TiFlash 的存储和计算资源，提升 HTAP 资源的弹性能力。</li>
        <li>支持基于 S3 的存储引擎，以更低的成本提供共享存储。</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td rowspan="2">SQL</td>
    <td>TiDB 支持完整的<a href="https://docs.pingcap.com/zh/tidb/v7.4/partitioned-table#将分区表转换为非分区表" target="_blank">分区类型管理功能</a> </td>
    <td>在 v7.4.0 之前，Range/List 分区表支持分区管理操作包括 <code>TRUNCATE</code>、<code>EXCHANGE</code>、<code>ADD</code>、<code>DROP</code>、<code>REORGANIZE</code> 等，Hash/Key 分区表支持分区管理操作包括 <code>ADD</code> 和 <code>COALESCE</code> 等。
    <p>现在 TiDB 新增支持了以下分区类型管理操作：</p>
    <ul>
        <li>将分区表转换为非分区表</li>
        <li>对现有的非分区表进行分区</li>
        <li>修改现有分区表的分区类型</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td>MySQL 8.0 兼容性：支持<a href="https://docs.pingcap.com/zh/tidb/v7.4/character-set-and-collation#支持的字符集和排序规则" target="_blank">排序规则 <code>utf8mb4_0900_ai_ci</code></a></td>
    <td>MySQL 8.0 的一个显著变化是默认字符集更改为 utf8mb4，其默认排序规则是 <code>utf8mb4_0900_ai_ci</code>。TiDB v7.4.0 增强了与 MySQL 8.0 的兼容性。现在你可以更轻松地将在 MySQL 8.0 中使用默认排序规则创建的数据库迁移或复制到 TiDB。</td>
  </tr>
  <tr>
    <td>数据库管理与可观测性</td>
    <td>选择<a href="https://docs.pingcap.com/zh/tidb/v7.4/system-variables#tidb_service_scope-从-v740-版本开始引入" target="_blank">适用的 TiDB 节点</a>来并行执行 <code>ADD INDEX</code> 或 <code>IMPORT INTO</code> SQL 语句（实验特性）</td>
    <td>你可以选择在现有 TiDB 节点、或者新增 TiDB 节点执行 <code>ADD INDEX</code> 和 <code>IMPORT INTO</code> SQL 语句。该方法可以实现与其他 TiDB 节点的资源隔离，确保在执行上述语句时的最佳性能，并避免对已有业务造成性能影响。</td>
  </tr>
</tbody>
</table>

## 功能详情

### 可扩展性

* 支持设置 TiDB 节点的服务范围，用于选择适用的 TiDB 节点来执行并行的 `ADD INDEX` 或 `IMPORT INTO` 任务（实验特性）[#46453](https://github.com/pingcap/tidb/pull/46453) @[ywqzzy](https://github.com/ywqzzy)

    在资源密集型集群中，并行执行 `ADD INDEX` 或 `IMPORT INTO` 任务可能占用大量 TiDB 节点的资源，从而导致集群性能下降。从 v7.4.0 起，你可以通过变量 [`tidb_service_scope`](/system-variables.md#tidb_service_scope-从-v740-版本开始引入) 控制 [TiDB 分布式执行框架](/tidb-distributed-execution-framework.md)下各 TiDB 节点的服务范围。你可以从现有 TiDB 节点中选择几个节点，或者对新增 TiDB 节点设置服务范围。所有并行执行的 `ADD INDEX` 和 `IMPORT INTO` 的任务只会运行在这些节点，避免对已有业务造成性能影响。

    更多信息，请参考[用户文档](/system-variables.md#tidb_service_scope-从-v740-版本开始引入)。

* 增强 Partitioned Raft KV 存储引擎（实验特性）[#11515](https://github.com/tikv/tikv/issues/11515) [#12842](https://github.com/tikv/tikv/issues/12842) @[busyjay](https://github.com/busyjay) @[tonyxuqqi](https://github.com/tonyxuqqi) @[tabokie](https://github.com/tabokie) @[bufferflies](https://github.com/bufferflies) @[5kbpers](https://github.com/5kbpers) @[SpadeA-Tang](https://github.com/SpadeA-Tang) @[nolouch](https://github.com/nolouch)

    TiDB v6.6.0 引入了 Partitioned Raft KV 存储引擎作为实验特性，该引擎使用多个 RocksDB 实例存储 TiKV 的 Region 数据，每个 Region 的数据都独立存储在单独的 RocksDB 实例中。

    在 TiDB v7.4.0 中，Partitioned Raft KV 引擎在兼容性和稳定性方面得到了进一步提升。通过大规模数据测试，确保了 Partitioned Raft KV 引擎与 DM、Dumpling、TiDB Lightning、TiCDC、BR、PITR 等关键生态组件或功能的兼容性。同时，在读写混合工作负载下，Partitioned Raft KV 引擎提供了更稳定的性能，特别适合写多读少的场景。此外，每个 TiKV 节点支持 8 core CPU，并可搭配 8 TB 的数据存储和 64 GB 的内存。

    更多信息，请参考[用户文档](/partitioned-raft-kv.md)。

* TiFlash 存算分离架构成为正式功能 (GA) [#6882](https://github.com/pingcap/tiflash/issues/6882) @[JaySon-Huang](https://github.com/JaySon-Huang) @[JinheLin](https://github.com/JinheLin) @[breezewish](https://github.com/breezewish) @[lidezhu](https://github.com/lidezhu) @[CalvinNeo](https://github.com/CalvinNeo) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)

    在 v7.0.0 中，TiFlash 以实验特性引入了存算分离架构。经过一系列的改进，从 v7.4.0 起，TiFlash 正式支持存算分离架构。

    在存算分离架构下，TiFlash 节点分为 Compute Node（计算节点）和 Write Node（写入节点）两种类型，并使用兼容 S3 API 的对象存储。这两种节点都可以单独扩缩容，独立调整计算或数据存储能力。在存算分离架构下，TiFlash 的使用方式与存算一体架构一致，例如创建 TiFlash 副本、查询、指定优化器 Hint 等。

    需要注意的是，TiFlash 的存算分离架构和存算一体架构不能混合使用、相互转换，需要在部署 TiFlash 时进行相应的配置指定使用其中的一种架构。

    更多信息，请参考[用户文档](/tiflash/tiflash-disaggregated-and-s3.md)。

### 性能

* 支持下推 JSON 运算符 `MEMBER OF` 到 TiKV [#46307](https://github.com/pingcap/tidb/issues/46307) @[wshwsh12](https://github.com/wshwsh12)

    * `value MEMBER OF(json_array)`

  更多信息，请参考[用户文档](/functions-and-operators/expressions-pushed-down.md)。

* 支持下推包含任意帧定义类型的窗口函数到 TiFlash [#7376](https://github.com/pingcap/tiflash/issues/7376) @[xzhangxian1008](https://github.com/xzhangxian1008)

    在 v7.4.0 之前的版本中，TiFlash 不支持包含 `PRECEDING` 或 `FOLLOWING` 的窗口函数，所有包含此类帧定义的窗口函数都无法下推至 TiFlash。从 v7.4.0 开始，TiFlash 支持了所有的窗口函数的帧定义。该功能自动启用，满足要求时，包含帧定义的窗口函数会自动下推至 TiFlash 执行。

* 引入基于云存储的全局排序能力，提升并行执行的 `ADD INDEX` 或 `IMPORT INTO` 任务的性能和稳定性（实验特性）[#45719](https://github.com/pingcap/tidb/issues/45719) @[wjhuang2016](https://github.com/wjhuang2016)

    在 v7.4.0 以前，当用户执行分布式并行执行框架的 `ADD INDEX` 或 `IMPORT INTO` 任务时，TiDB 节点需要准备一块较大的本地磁盘，对编码后的索引 KV pairs 和表数据 KV pairs 进行排序。由于无法从全局角度进行排序，各个 TiDB 节点间以及节点内部导入的数据可能存在重叠情况。这会导致在将这些 KV pairs 导入到 TiKV 时，TiKV 需要频繁进行数据整理 (compaction)，降低了 `ADD INDEX` 或 `IMPORT INTO` 的性能和稳定性。

    v7.4.0 引入全局排序特性后，编码后的数据不再写入本地进行排序，而是写入云存储，并在云存储中进行全局排序。然后，TiDB 将经过全局排序的索引数据和表数据并行导入到 TiKV 中，从而提升了性能和稳定性。

    更多信息，请参考[用户文档](/tidb-global-sort.md)。

* 支持缓存非 Prepare 语句的执行计划 (GA) [#36598](https://github.com/pingcap/tidb/issues/36598) @[qw4990](https://github.com/qw4990)

    TiDB v7.0.0 引入了非 Prepare 语句的执行计划缓存作为实验特性，以提升在线交易场景的并发处理能力。在 v7.4.0 中，该功能正式 GA。执行计划缓存技术将会被应用于更广泛的场景，从而提升 TiDB 的并发处理能力。

    开启非 Prepare 语句执行计划缓存可能会带来额外的内存和 CPU 开销，并不一定适用于所有场景。从 v7.4.0 开始，非 Prepare 语句的执行计划缓存默认关闭。你可以通过系统变量 [`tidb_enable_non_prepared_plan_cache`](/system-variables.md#tidb_enable_non_prepared_plan_cache) 控制是否开启该功能并通过 [`tidb_session_plan_cache_size`](/system-variables.md#tidb_session_plan_cache_size-从-v710-版本开始引入) 设置缓存大小。

    此外，该功能默认不支持 DML 语句，对 SQL 的模式也有一定的限制，具体参见[使用限制](/sql-non-prepared-plan-cache.md#限制)。

    更多信息，请参考[用户文档](/sql-non-prepared-plan-cache.md)。

### 稳定性

* TiFlash 支持查询级别的数据落盘 [#7738](https://github.com/pingcap/tiflash/issues/7738) @[windtalker](https://github.com/windtalker)

    从 v7.0.0 起，TiFlash 支持控制 `GROUP BY`、`ORDER BY`、`JOIN` 这三种算子的数据落盘功能，避免数据量超过内存总大小时，导致查询终止甚至系统崩溃的问题。然而，单独控制每个算子的落盘较为麻烦，也无法有效进行整体资源控制。

    在 v7.4.0 中，TiFlash 引入了查询级别数的据落盘功能。通过设置单个查询在单个 TiFlash 节点使用内存的上限 [`tiflash_mem_quota_query_per_node`](/system-variables.md#tiflash_mem_quota_query_per_node-从-v740-版本开始引入) 及触发数据落盘的内存阈值 [`tiflash_query_spill_ratio`](/system-variables.md#tiflash_query_spill_ratio-从-v740-版本开始引入)，你可以方便地控制单个查询的内存使用，更好地管控 TiFlash 内存资源。

    更多信息，请参考[用户文档](/tiflash/tiflash-spill-disk.md)。

* 支持自定义 TiKV 读取超时时间 [#45380](https://github.com/pingcap/tidb/issues/45380) @[crazycs520](https://github.com/crazycs520)

    在通常情况下，TiKV 处理请求非常快，只需几毫秒。但是，当某个 TiKV 节点遇到磁盘 I/O 抖动或网络延迟时，请求处理时间可能会大幅增加。在 v7.4.0 以前的版本中，TiKV 请求的超时限制是固定的，不能调整。因此，当 TiKV 节点出现问题时，TiDB 必须等待固定时长的超时响应，这导致了抖动期间应用程序的查询性能受到明显影响。

    TiDB 在 v7.4.0 中引入了一个新系统变量 [`tikv_client_read_timeout`](/system-variables.md#tikv_client_read_timeout-从-v740-版本开始引入)，你可以自定义查询语句中 TiDB 发送给 TiKV 的 RPC 读请求的超时时间。这意味着，当某个 TiKV 节点因磁盘或网络问题导致请求延迟时，TiDB 可以更快地超时并将请求重新发送给其他 TiKV 节点，从而降低查询延迟。如果所有 TiKV 节点的请求都超时，TiDB 将使用默认的超时时间进行重试。此外，你也可以在查询语句中使用 Optimizer Hint `/*+ SET_VAR(TIKV_CLIENT_READ_TIMEOUT=N) */` 来设置 TiDB 发送 TiKV RPC 读请求的超时时间。这一改进将使 TiDB 在面对不稳定的网络或存储环境时，更灵活地适应各种情况，提高查询性能，提升用户体验。

    更多的信息，请参考[用户文档](/system-variables.md#tikv_client_read_timeout-从-v740-版本开始引入)。

* 支持通过优化器提示临时修改部分系统变量的值 [#45892](https://github.com/pingcap/tidb/issues/45892) @[winoros](https://github.com/winoros)

    TiDB v7.4.0 新增支持与 MySQL 8.0 相似的优化器提示 `SET_VAR()`。通过在 SQL 语句中添加 Hint `SET_VAR()`，可以在语句运行过程中临时修改部分系统变量，以针对不同语句设置环境。例如，可以主动提升高消耗 SQL 的并行度，或者通过变量修改优化器行为。

    支持使用 Hint `SET_VAR()` 修改的系统变量请参考[系统变量](/system-variables.md)。强烈建议不要利用此 Hint 修改没有明确支持的变量，这可能会引发不可预知的行为。

    更多信息，请参考[用户文档](/optimizer-hints.md)。

* TiFlash 支持资源管控特性 [#7660](https://github.com/pingcap/tiflash/issues/7660) @[guo-shaoge](https://github.com/guo-shaoge)

    在 TiDB v7.1.0 中，资源管控成为正式功能，提供对 TiDB 和 TiKV 的资源管理能力。在 v7.4.0 中，TiFlash 支持资源管控特性，完善了 TiDB 整体的资源管控能力。TiFlash 的资源管控与已有的 TiDB 资源管控特性完全兼容，现有的资源组将同时管控 TiDB、TiKV 和 TiFlash 中的资源。

    通过配置 TiFlash 参数 `enable_resource_control`，你可以控制是否开启 TiFlash 资源管控特性。开启后，TiFlash 将根据 TiDB 的资源组配置进行资源调度管理，确保整体资源的合理分配和使用。

    更多信息，请参考[用户文档](/tidb-resource-control.md)。

* TiFlash 支持 Pipeline 执行模型 (GA) [#6518](https://github.com/pingcap/tiflash/issues/6518) @[SeaRise](https://github.com/SeaRise)

    在 v7.2.0 中，TiFlash 引入了 Pipeline 执行模型作为实验特性。该模型对所有线程资源进行统一管理，并对所有任务的执行进行统一调度，充分利用线程资源，同时避免资源超用。从 v7.4.0 开始，TiFlash 完善了线程资源使用量的统计，Pipeline 执行模型成为正式功能 (GA) 并默认开启。由于该功能与 TiFlash 资源管控特性相互依赖，TiDB v7.4.0 移除了之前版本中用于控制是否启用 Pipeline 执行模型的变量 `tidb_enable_tiflash_pipeline_model`。现在你可以通过 TiFlash 参数 `tidb_enable_resource_control` 同时开启或关闭 Pipeline 执行模型和 TiFlash 资源管控特性。

    更多信息，请参考[用户文档](/tiflash/tiflash-pipeline-model.md)。

* 新增优化器模式选择 [#46080](https://github.com/pingcap/tidb/issues/46080) @[time-and-fate](https://github.com/time-and-fate)

    TiDB 在 v7.4.0 引入了一个新的系统变量 [`tidb_opt_objective`](/system-variables.md#tidb_opt_objective-从-v740-版本开始引入)，用于控制优化器的估算方式。默认值 `moderate` 维持之前版本的优化器行为，即优化器会利用运行时统计到的数据修改来校正估算。如果设置为 `determinate`，则优化器不考虑运行时校正，只根据统计信息来生成执行计划。

    对于长期稳定的 OLTP 业务，或者用户对已有的执行计划非常有把握的情况，推荐在测试后切换到 `determinate` 模式，减少执行计划跳变的可能。

    更多信息，请参考[用户文档](/system-variables.md#tidb_opt_objective-从-v740-版本开始引入)。

* 资源管控支持自动管理后台任务（实验特性）[#44517](https://github.com/pingcap/tidb/issues/44517) @[glorv](https://github.com/glorv)

    后台任务是指那些优先级不高但是需要消耗大量资源的任务，如数据备份和自动统计信息收集等。这些任务通常定期或不定期触发，在执行的时候会消耗大量资源，从而影响在线的高优先级任务的性能。在 TiDB v7.4.0 中，资源管控引入了对后台任务的自动管理。该功能有助于降低低优先级任务对在线业务的性能影响，实现资源的合理分配，大幅提升集群的稳定性。

    目前 TiDB 支持如下几种后台任务的类型：

    - `lightning`：使用 [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md) 或 [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md) 执行导入任务。
    - `br`：使用 [BR](/br/backup-and-restore-overview.md) 执行数据备份和恢复。目前不支持 PITR。
    - `ddl`：对于 Reorg DDL，控制批量数据回写阶段的资源使用。
    - `stats`：对应手动执行或系统自动触发的[收集统计信息](/statistics.md#统计信息的收集)任务。

  默认情况下，被标记为后台任务的任务类型为空，此时后台任务的管理功能处于关闭状态，其行为与 TiDB v7.4.0 之前版本保持一致。你需要手动修改 `default` 资源组的后台任务类型以开启后台任务管理。

    更多信息，请参考[用户文档](/tidb-resource-control.md#管理后台任务)。

* 锁定统计信息成为正式功能 (GA) [#46351](https://github.com/pingcap/tidb/issues/46351) @[hi-rustin](https://github.com/hi-rustin)

    在 v7.4.0 中，TiDB [锁定统计信息](/statistics.md#锁定统计信息)成为正式功能 (GA)。现在，锁定和解锁统计信息需要与收集统计信息 (`ANALYZE TABLE`) 相同的权限，以确保操作的安全性。此外，还新增了对特定分区的统计信息进行锁定和解锁操作的支持，提高了功能灵活性。当用户对数据库中的查询和执行计划有把握，并且不希望发生变化时，可以使用锁定统计信息来提升统计信息的稳定性。

    更多信息，请参考[用户文档](/statistics.md#锁定统计信息)。

* 引入系统变量控制是否选择表的哈希连接 [#46695](https://github.com/pingcap/tidb/issues/46695) @[coderplay](https://github.com/coderplay)

    表的哈希连接是 MySQL 8.0 引入的新特性，主要用于连接两个相对较大的表和结果集。但对于交易类负载，或者一部分在 MySQL 5.7 稳定运行的业务来说，选择表的哈希连接可能会对性能产生风险。MySQL 通过[优化器开关 `optimizer_switch`](https://dev.mysql.com/doc/refman/8.0/en/switchable-optimizations.html#optflag_block-nested-loop)能够在全局或者会话级控制哈希连接的选择。

    从 v7.4.0 开始，TiDB 引入系统变量 [`tidb_opt_enable_hash_join`](/system-variables.md#tidb_opt_enable_hash_join-从-v656v712-和-v740-版本开始引入) 对表的哈希连接进行控制。默认开启 (`ON`)。如果你非常确定执行计划中不需要选择表之间的哈希连接，则可以修改变量为 `OFF`，降低执行计划回退的可能性，提升系统稳定性。

    更多信息，请参考[用户文档](/system-variables.md#tidb_opt_enable_hash_join-从-v656v712-和-v740-版本开始引入)。

### SQL 功能

* TiDB 支持完整的分区类型管理功能 [#42728](https://github.com/pingcap/tidb/issues/42728) @[mjonss](https://github.com/mjonss)

    在 v7.4.0 之前，TiDB 中的分区表不能调整分区类型。从 v7.4.0 开始，TiDB 支持将分区表修改为非分区表、将非分区表修改为分区表、修改分区类型功能。你可以根据需要灵活调整表的分区类型、数量。例如，通过 `ALTER TABLE t PARTITION BY ...` 语句修改分区类型。

    更多信息，请参考[用户文档](/partitioned-table.md#分区管理)。

* TiDB 支持 `WITH ROLLUP` 修饰符和 `GROUPING` 函数 [#44487](https://github.com/pingcap/tidb/issues/44487) @[AilinKid](https://github.com/AilinKid)

    `WITH ROLLUP` 修饰符和 `GROUPING` 函数是数据分析中常用的功能，用于对数据进行多维度的汇总。从 v7.4.0 开始，TiDB 支持在 `GROUP BY` 子句中使用 `WITH ROLLUP` 修饰符和 `GROUPING` 函数。例如，你可以通过 `SELECT ... FROM ... GROUP BY ... WITH ROLLUP` 语法使用 `WITH ROLLUP` 修饰符。

    更多信息，请参考[用户文档](/functions-and-operators/group-by-modifier.md)。

### 数据库管理

* 新增排序规则 `utf8mb4_0900_ai_ci` 和 `utf8mb4_0900_bin` [#37566](https://github.com/pingcap/tidb/issues/37566) @[YangKeao](https://github.com/YangKeao) @[zimulala](https://github.com/zimulala) @[bb7133](https://github.com/bb7133)

    TiDB v7.4.0 增强了从 MySQL 8.0 迁移数据的支持。新增两个排序规则 (Collation) `utf8mb4_0900_ai_ci` 和 `utf8mb4_0900_bin`。其中 `utf8mb4_0900_ai_ci` 为 MySQL 8.0 的默认排序规则。

    同时新增支持 MySQL 8.0 兼容的系统变量 `default_collation_for_utf8mb4`，允许用户为 utf8mb4 字符集指定默认的排序方式，以兼容从 MySQL 5.7 或之前版本迁移或数据复制的场景。

    更多信息，请参考[用户文档](/character-set-and-collation.md#支持的字符集和排序规则)。

### 可观测性

* 支持向日志中添加会话标识和会话别名 [#46071](https://github.com/pingcap/tidb/issues/46071) @[lcwangchao](https://github.com/lcwangchao)

    在对 SQL 执行问题做故障定位的时候，经常需要把 TiDB 各组件日志中的内容进行关联，由此找到问题的根本原因。从 v7.4.0 开始，TiDB 将会话标识 (`CONNECTION_ID`) 写入与会话相关的日志内容中，包括 TiDB 日志、慢查询日志、以及 TiKV 上 coprocessor 的慢日志记录。你可以根据会话标识，将几个日志中的内容关联起来，提升故障定位和诊断的效率。

    除此之外，通过设置会话级变量 [`tidb_session_alias`](/system-variables.md#tidb_session_alias-从-v740-版本开始引入)，你可以向上述日志中添加自定义的标识。借助这个能力，把业务识别信息注入日志，可以将日志中的内容与业务关联，打通了业务到日志的链路，降低了诊断工作的难度。

* TiDB Dashboard 提供表格视图的执行计划 [#1589](https://github.com/pingcap/tidb-dashboard/issues/1589) @[baurine](https://github.com/baurine)

    在 v7.4.0 中，TiDB Dashboard 的 **Slow Query** 页面和 **SQL Statement** 页面提供表格视图的执行计划，以提升用户的诊断体验。

    更多信息，请参考[用户文档](/dashboard/dashboard-statement-details.md)。

### 数据迁移

* 增强 `IMPORT INTO` 功能 [#46704](https://github.com/pingcap/tidb/issues/46704) @[D3Hunter](https://github.com/D3Hunter)

    从 v7.4.0 起，你可以通过在 `IMPORT INTO` 的 `CLOUD_STORAGE_URI` 选项中指定编码后数据的云存储地址，开启[全局排序功能](/tidb-global-sort.md)（实验特性），提升性能和稳定性。

    此外，在 v7.4.0 中，`IMPORT INTO`  还引入了以下功能：

    - 支持配置 `Split_File` 选项，可将单个大 CSV 文件切分成多个 256 MiB 的小 CSV 文件进行并行处理，提升导入性能。
    - 支持导入压缩后的 CSV 和 SQL 文件，支持的压缩格式包括 `.gzip`、`.gz`、`.zstd`、`.zst` 和 `.snappy`。

  更多信息，请参考[用户文档](/sql-statements/sql-statement-import-into.md)。

* Dumpling 在将数据导出为 CSV 文件时支持用户自定义换行符 [#46982](https://github.com/pingcap/tidb/issues/46982) @[GMHDBJD](https://github.com/GMHDBJD)

    在 v7.4.0 之前，Dumpling 导出数据为 CSV 文件时，换行符为 `"\r\n"`，导致一些只能解析 `"\n"` 换行符的下游系统无法解析该 CSV 文件，或者要通过第三方工具转换后才能解析。

    从 v7.4.0 起，Dumpling 引入了新的参数 `--csv-line-terminator`。当你将数据导出为 CSV 文件时，可以通过该参数传入所需的换行符。该参数支持 `"\r\n\"` 和 `"\n"`，默认值为 `"\r\n"`，即和历史版本保持一致。

    更多信息，请参考[用户文档](/dumpling-overview.md#dumpling-主要选项表)。

* TiCDC 支持同步数据至 Pulsar [#9413](https://github.com/pingcap/tiflow/issues/9413) @[yumchina](https://github.com/yumchina) @[asddongmen](https://github.com/asddongmen)

    Pulsar 是一款云原生的分布式消息流平台，它能够显著提升你的实时数据流体验。从 v7.4.0 起，TiCDC 支持以 `canal-json` 格式同步变更数据至 Pulsar，实现与 Pulsar 的无缝集成。通过该功能，TiCDC 可以让你轻松捕获和同步 TiDB 变更数据到 Pulsar，为数据处理和分析功能提供新的可能性。你可以开发自己的消费应用程序，从 Pulsar 中读取并处理新生成的变更数据，以满足特定的业务需求。

    更多信息，请参考[用户文档](/ticdc/ticdc-sink-to-pulsar.md)。

* TiCDC 支持 Claim-Check 功能，改进对大型消息的处理 [#9153](https://github.com/pingcap/tiflow/issues/9153) @[3AceShowHand](https://github.com/3AceShowHand)

    在 v7.4.0 之前，TiCDC 无法向下游发送超过 Kafka 最大消息大小 (`max.message.bytes`) 的大型消息。从 v7.4.0 开始，在配置下游为 Kafka 的 Changefeed 的时候，你可以指定一个外部存储位置，用于存储超过 Kafka 限制的大型消息。TiCDC 会向 Kafka 发送一条引用消息，其中记录了该大型消息在外部存储中的地址。当消费者收到该引用消息后，可以根据其中记录的外部存储地址信息，获取对应的消息内容。

    更多信息，请参考[用户文档](/ticdc/ticdc-sink-to-kafka.md#发送大消息到外部存储)。

## 兼容性变更

> **注意：**
>
> 以下为从 v7.3.0 升级至当前版本 (v7.4.0) 所需兼容性变更信息。如果从 v7.2.0 或之前版本升级到当前版本，可能也需要考虑和查看中间版本 release notes 中提到的兼容性变更信息。

### 行为变更

- 自 v7.4.0 起，TiDB 已经兼容 MySQL 8.0 的主要功能，`version()` 将返回以 `8.0.11` 为前缀的版本信息。

- 升级到 TiFlash v7.4.0 后，不支持原地降级到之前的版本。这是因为，从 v7.4.0 开始，为了减少数据整理时产生的读、写放大，TiFlash 对 PageStorage V3 数据整理时的逻辑进行了优化，导致底层部分存储文件名发生了改动。详情请参考 [TiFlash 升级帮助](/tiflash-upgrade-guide.md#从-v6x-或-v7x-升级至-v74-或以上版本)。

- 新增函数 [`TIDB_PARSE_TSO_LOGICAL()`](/functions-and-operators/tidb-functions.md#tidb-特有的函数)，用于从 TiDB TSO 时间戳中提取逻辑时间戳。

- 新增表 [`information_schema.CHECK_CONSTRAINTS`](/information-schema/information-schema-check-constraints.md)，提高与 MySQL 8.0 的兼容性。
- 对于包含多条变更的事务，如果 Update 事件的主键或者非空唯一索引的列值发生改变，TiCDC 会将该其拆分为 Delete 和 Insert 两条事件，并确保将所有事件有序，以保证 Delete 事件在 Insert 事件之前。更多信息，请参考[用户文档](/ticdc/ticdc-split-update-behavior.md#含有多条-update-变更的事务拆分)。

### 系统变量

| 变量名 | 修改类型 | 描述 |
|---|----|------|
| `tidb_enable_tiflash_pipeline_model` | 删除 | 这个变量用来控制是否启用 TiFlash Pipeline Model。从 v7.4.0 开启，开启 TiFlash 资源管控功能时，Pipeline Model 模型将自动启用。 |
| [`tidb_enable_non_prepared_plan_cache`](/system-variables.md#tidb_enable_non_prepared_plan_cache) | 修改 | 经进一步的测试后，该变量默认值从 `ON` 修改为 `OFF`，即默认关闭非 Prepare 语句执行计划缓存。 |
| [`default_collation_for_utf8mb4`](/system-variables.md#default_collation_for_utf8mb4-从-v740-版本开始引入) | 新增 | 该变量用于设置 utf8mb4 字符集的默认排序规则，默认值为 `utf8mb4_bin`。 |
| [`tidb_cloud_storage_uri`](/system-variables.md#tidb_cloud_storage_uri-从-v740-版本开始引入) | 新增 | 该变量用于指定[全局排序](/tidb-global-sort.md)中使用的云存储的 URI。 |
| [`tidb_opt_enable_hash_join`](/system-variables.md#tidb_opt_enable_hash_join-从-v656v712-和-v740-版本开始引入) | 新增 | 控制优化器是否会选择表的哈希连接。默认打开 (`ON`)。设置为 `OFF` 时，除非没有计划可用，否则优化器会避免选择表的哈希连接。 |
| [`tidb_opt_objective`](/system-variables.md#tidb_opt_objective-从-v740-版本开始引入) | 新增 | 该变量用于设置优化器优化目标。`moderate` 维持旧版本的默认行为，优化器会利用更多信息尝试生成更优的计划；`determinate` 则倾向于保守，保持执行计划稳定。 |
| [`tidb_request_source_type`](/system-variables.md#tidb_request_source_type-从-v740-版本开始引入) | 新增 | 该变量用于显式指定当前会话的任务类型，用于[资源管控](/tidb-resource-control.md)识别并控制。如 `SET @@tidb_request_source_type = "background"`。 |
| [`tidb_schema_version_cache_limit`](/system-variables.md#tidb_schema_version_cache_limit-从-v740-版本开始引入) | 新增 | 该变量用于限制 TiDB 实例可以缓存多少个历史版本的表结构信息。默认值为 `16`，即默认缓存 16 个历史版本的表结构信息。|
| [`tidb_service_scope`](/system-variables.md#tidb_service_scope-从-v740-版本开始引入) | 新增 | 该变量是一个实例级别的变量，用于控制 [TiDB 分布式执行框架](/tidb-distributed-execution-framework.md)下各 TiDB 节点的服务范围。当设置 TiDB 节点的 `tidb_service_scope` 为 `background` 时，分布式执行框架将调度该节点执行任务（如 [`ADD INDEX`](/sql-statements/sql-statement-add-index.md) 和 [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md)）。 |
| [`tidb_session_alias`](/system-variables.md#tidb_session_alias-从-v740-版本开始引入) | 新增 | 用来自定义当前会话相关日志中 `session_alias` 列的值。 |
| [`tiflash_mem_quota_query_per_node`](/system-variables.md#tiflash_mem_quota_query_per_node-从-v740-版本开始引入) | 新增 | 用于设置单个查询在单个 TiFlash 节点上的内存使用上限，超过该限制时 TiFlash 会报错并终止该查询。默认值为 `0`，表示无限制。 |
| [`tiflash_query_spill_ratio`](/system-variables.md#tiflash_query_spill_ratio-从-v740-版本开始引入) | 新增 |  用于控制 TiFlash [查询级别的落盘](/tiflash/tiflash-spill-disk.md#查询级别的落盘)机制的阈值。默认值为 `0.7`。  |
| [`tikv_client_read_timeout`](/system-variables.md#tikv_client_read_timeout-从-v740-版本开始引入) | 新增 | 该变量用于设置查询语句中 TiDB 发送 TiKV RPC 读请求的超时时间。默认值 `0`，表示使用默认的超时时间（通常是 40 秒）。 |

### 配置文件参数

| 配置文件 | 配置项 | 修改类型 | 描述 |
| -------- | -------- | -------- | -------- |
| TiDB | [`enable-stats-cache-mem-quota`](/tidb-configuration-file.md#enable-stats-cache-mem-quota-从-v610-版本开始引入) | 修改 | 默认值由 `false` 改为 `true`，即默认开启 TiDB 统计信息缓存的内存上限。 |
| TiKV | [<code>rocksdb.\[defaultcf\|writecf\|lockcf\].periodic-compaction-seconds</code>](/tikv-configuration-file.md#periodic-compaction-seconds-从-v720-版本开始引入) | 修改 | 默认值从 `"30d"` 修改为 `"0s"`，默认关闭 RocksDB 的周期性 compaction 以避免升级后集中触发大量 compaction 影响前台读写性能。 |
| TiKV | [<code>rocksdb.\[defaultcf\|writecf\|lockcf\].ttl</code>](/tikv-configuration-file.md#ttl-从-v720-版本开始引入) | 修改 | 默认值从 `"30d"` 修改为 `"0s"`，SST 文件默认不会由于 TTL 触发 compaction，避免影响前台读写性能。 |
| TiFlash | [`flash.compact_log_min_gap`](/tiflash/tiflash-configuration.md) | 新增 | 在当前 Raft 状态机推进的 `applied_index` 和上次落盘时的 `applied_index` 的差值高于 `compact_log_min_gap` 时，TiFlash 将执行来自 TiKV 的 CompactLog 命令，并进行数据落盘。 |
| TiFlash | [`profiles.default.enable_resource_control`](/tiflash/tiflash-configuration.md) | 新增 | 控制是否开启 TiFlash 资源管控功能。 |
| TiFlash | [`storage.format_version`](/tiflash/tiflash-configuration.md) | 修改 | 默认值从 `4` 修改为 `5`，该格式可以合并小文件从而减少了物理文件数量。 |
| Dumpling  | [`--csv-line-terminator`](/dumpling-overview.md#dumpling-主要选项表) | 新增 | 控制导出数据为 CSV 文件的换行符，支持 `"\r\n"` 和 `"\n"`，默认值为 `"\r\n"`，即和历史版本保持一致。 |
| TiCDC | [`claim-check-storage-uri`](/ticdc/ticdc-sink-to-kafka.md#发送大消息到外部存储) | 新增 | 当指定 `large-message-handle-option` 为 `claim-check` 时，`claim-check-storage-uri` 必须设置为一个有效的外部存储服务地址，否则创建 Changefeed 将会报错。|
| TiCDC | [`large-message-handle-compression`](/ticdc/ticdc-sink-to-kafka.md#ticdc-层数据压缩功能) | 新增 | 控制是否开启编码时的压缩功能，默认为空，即不开启。|
| TiCDC | [`large-message-handle-option`](/ticdc/ticdc-sink-to-kafka.md#发送大消息到外部存储) | 修改 | 该配置项新增一个可选值 `claim-check`。当设置为 `claim-check` 时，TiCDC Kafka sink 支持在消息大小超过限制时将该条消息发送到外部存储服务，同时向 Kafka 发送一条含有该大消息在外部存储服务中的地址的消息。 |

## 废弃和删除的功能

+ [Mydumper](https://docs.pingcap.com/zh/tidb/v4.0/mydumper-overview) 计划在 v7.5.0 中废弃，其绝大部分功能已经被 [Dumpling](/dumpling-overview.md) 取代，强烈建议切换到 Dumpling。
+ TiKV-importer 组件计划在 v7.5.0 中废弃，建议使用 [TiDB Lightning 物理导入模式](/tidb-lightning/tidb-lightning-physical-import-mode.md)作为替代方案。
+ TiCDC 移除 `enable-old-value` 参数 [#9667](https://github.com/pingcap/tiflow/issues/9667) @[3AceShowHand](https://github.com/3AceShowHand)

## 改进提升

+ TiDB

    - 优化 `ANALYZE` 分区表的内存使用和性能 [#47071](https://github.com/pingcap/tidb/issues/47071) [#47104](https://github.com/pingcap/tidb/issues/47104) [#46804](https://github.com/pingcap/tidb/issues/46804) @[hawkingrei](https://github.com/hawkingrei)
    - 优化统计信息垃圾回收的内存使用和性能 [#31778](https://github.com/pingcap/tidb/issues/31778) @[winoros](https://github.com/winoros)
    - 优化索引合并进行交集操作时的 `limit` 下推，提高查询性能 [#46863](https://github.com/pingcap/tidb/issues/46863) @[AilinKid](https://github.com/AilinKid)
    - 改进代价模型 (Cost Model) 以尽量避免在 `IndexLookup` 回表任务多时错误地选择全表扫描 [#45132](https://github.com/pingcap/tidb/issues/45132) @[qw4990](https://github.com/qw4990)
    - 优化 join 消除规则，提高 `join on unique keys` 时的查询性能 [#46248](https://github.com/pingcap/tidb/issues/46248) @[fixdb](https://github.com/fixdb)
    - 将多值索引列的排序规则变更为 `binary`，避免执行失败 [#46717](https://github.com/pingcap/tidb/issues/46717) @[YangKeao](https://github.com/YangKeao)

+ TiKV

    - 改进 Resolver 的内存使用，防止 OOM [#15458](https://github.com/tikv/tikv/issues/15458) @[overvenus](https://github.com/overvenus)
    - 消除 Router 对象中的 LRUCache，降低内存占用，防止 OOM [#15430](https://github.com/tikv/tikv/issues/15430) @[Connor1996](https://github.com/Connor1996)
    - 降低 TiCDC Resolver 的内存占用 [#15412](https://github.com/tikv/tikv/issues/15412) @[overvenus](https://github.com/overvenus)
    - 降低 RocksDB compaction 带来的内存抖动 [#15324](https://github.com/tikv/tikv/issues/15324) @[overvenus](https://github.com/overvenus)
    - 降低 Partitioned Raft KV 中流控模块的内存占用 [#15269](https://github.com/tikv/tikv/issues/15269) @[overvenus](https://github.com/overvenus)
    - 新增 PD Client 连接重试过程中的 backoff 机制。异常错误重试期间，逐步增加重试时间间隔，减小 PD 压力 [#15428](https://github.com/tikv/tikv/issues/15428) @[nolouch](https://github.com/nolouch)
    - 支持动态调整 RocksDB 的 `background_compaction` [#15424](https://github.com/tikv/tikv/issues/15424) @[glorv](https://github.com/glorv)

+ PD

    - 优化 TSO 的追踪信息，方便调查 TSO 相关问题 [#6856](https://github.com/tikv/pd/pull/6856) @[tiancaiamao](https://github.com/tiancaiamao)
    - 支持复用 HTTP Client 连接，降低内存占用 [#6913](https://github.com/tikv/pd/issues/6913) @[nolouch](https://github.com/nolouch)
    - 优化无法连接到备份集群时 PD 自动更新集群状态的速度 [#6883](https://github.com/tikv/pd/issues/6883) @[disksing](https://github.com/disksing)
    - 改进 resource control client 的配置获取方式，使其可以动态获取最新配置 [#7043](https://github.com/tikv/pd/issues/7043) @[nolouch](https://github.com/nolouch)

+ TiFlash

    - 改进 TiFlash 写入过程的落盘策略，提升随机写入负载下的写性能 [#7564](https://github.com/pingcap/tiflash/issues/7564) @[CalvinNeo](https://github.com/CalvinNeo)
    - 为 TiFlash 处理 Raft 同步过程添加更多观测指标 [#8068](https://github.com/pingcap/tiflash/issues/8068) @[CalvinNeo](https://github.com/CalvinNeo)
    - 改进 TiFlash 文件格式，减少小文件数量以避免造成文件系统 inode 耗尽的问题 [#7595](https://github.com/pingcap/tiflash/issues/7595) @[hongyunyan](https://github.com/hongyunyan)

+ Tools

    + Backup & Restore (BR)

        - 缓解了 Region leadership 迁移导致 PITR 日志备份进度延迟变高的问题 [#13638](https://github.com/tikv/tikv/issues/13638) @[YuJuncen](https://github.com/YuJuncen)
        - 通过设置 HTTP 客户端 `MaxIdleConns` 和 `MaxIdleConnsPerHost` 参数，增强日志备份以及 PITR 恢复任务对连接复用的支持 [#46011](https://github.com/pingcap/tidb/issues/46011) @[Leavrth](https://github.com/Leavrth)
        - 增强 BR 在连接 PD 或外部 S3 存储出错时的容错能力 [#42909](https://github.com/pingcap/tidb/issues/42909) @[Leavrth](https://github.com/Leavrth)
        - 新增 restore 参数 `WaitTiflashReady`。当打开这个参数时，restore 操作将会等待 TiFlash 副本复制成功后才结束 [#43828](https://github.com/pingcap/tidb/issues/43828) [#46302](https://github.com/pingcap/tidb/issues/46302) @[3pointer](https://github.com/3pointer)
        - 减少日志备份 `resolve lock` 的 CPU 开销 [#40759](https://github.com/pingcap/tidb/issues/40759) @[3pointer](https://github.com/3pointer)

    + TiCDC

        - 优化同步 `ADD INDEX` DDL 的执行逻辑，从而不阻塞后续的 DML 语句 [#9644](https://github.com/pingcap/tiflow/issues/9644) @[sdojjy](https://github.com/sdojjy)

    + TiDB Lightning

        - 优化 TiDB Lightning 在 Region scatter 阶段的重试逻辑 [#46203](https://github.com/pingcap/tidb/issues/46203) @[mittalrishabh](https://github.com/mittalrishabh)
        - 优化 TiDB Lightning 在导入数据阶段对 `no leader` 错误的重试逻辑 [#46253](https://github.com/pingcap/tidb/issues/46253) @[lance6716](https://github.com/lance6716)

## 错误修复

+ TiDB

    - 修复 `BatchPointGet` 算子在非 Hash 分区表下执行结果错误的问题 [#45889](https://github.com/pingcap/tidb/issues/45889) @[Defined2014](https://github.com/Defined2014)
    - 修复 `BatchPointGet` 算子在 Hash 分区表下执行结果错误的问题 [#46779](https://github.com/pingcap/tidb/issues/46779) @[jiyfhust](https://github.com/jiyfhust)
    - 修复 TiDB parser 状态残留导致解析失败的问题 [#45898](https://github.com/pingcap/tidb/issues/45898) @[qw4990](https://github.com/qw4990)
    - 修复 `EXCHANGE PARTITION` 没有检查约束的问题 [#45922](https://github.com/pingcap/tidb/issues/45922) @[mjonss](https://github.com/mjonss)
    - 修复 `tidb_enforce_mpp` 系统变量不能被正确还原的问题 [#46214](https://github.com/pingcap/tidb/issues/46214) @[djshow832](https://github.com/djshow832)
    - 修复 `LIKE` 语句中 `_` 没有被正确处理的问题 [#46287](https://github.com/pingcap/tidb/issues/46287) [#46618](https://github.com/pingcap/tidb/issues/46618) @[Defined2014](https://github.com/Defined2014)
    - 修复当获取 schema 失败时会导致 `schemaTs` 被设置为 0 的问题 [#46325](https://github.com/pingcap/tidb/issues/46325) @[hihihuhu](https://github.com/hihihuhu)
    - 修复 `AUTO_ID_CACHE=1` 时可能导致 `Duplicate entry` 的问题 [#46444](https://github.com/pingcap/tidb/issues/46444) @[tiancaiamao](https://github.com/tiancaiamao)
    - 修复 `AUTO_ID_CACHE=1` 时 TiDB panic 后恢复过慢的问题 [#46454](https://github.com/pingcap/tidb/issues/46454) @[tiancaiamao](https://github.com/tiancaiamao)
    - 修复 `AUTO_ID_CACHE=1` 时 `SHOW CREATE TABLE` 中 `next_row_id` 错误的问题 [#46545](https://github.com/pingcap/tidb/issues/46545) @[tiancaiamao](https://github.com/tiancaiamao)
    - 修复在子查询中使用 CTE 时，解析出现 panic 的问题 [#45838](https://github.com/pingcap/tidb/issues/45838) @[djshow832](https://github.com/djshow832)
    - 修复在交换分区失败或被取消时，分区表的限制残留在原表上的问题 [#45920](https://github.com/pingcap/tidb/issues/45920) [#45791](https://github.com/pingcap/tidb/issues/45791) @[mjonss](https://github.com/mjonss)
    - 修复 List 分区的定义中不允许同时使用 `NULL` 和空字符串的问题 [#45694](https://github.com/pingcap/tidb/issues/45694) @[mjonss](https://github.com/mjonss)
    - 修复交换分区时，无法检测出不符合分区定义的数据的问题 [#46492](https://github.com/pingcap/tidb/issues/46492) @[mjonss](https://github.com/mjonss)
    - 修复 `tmp-storage-quota` 配置无法生效的问题 [#45161](https://github.com/pingcap/tidb/issues/45161) [#26806](https://github.com/pingcap/tidb/issues/26806) @[wshwsh12](https://github.com/wshwsh12)
    - 修复函数 `WEIGHT_STRING()` 不匹配排序规则的问题 [#45725](https://github.com/pingcap/tidb/issues/45725) @[dveeden](https://github.com/dveeden)
    - 修复 Index Join 出错可能导致查询卡住的问题 [#45716](https://github.com/pingcap/tidb/issues/45716) @[wshwsh12](https://github.com/wshwsh12)
    - 修复 `DATETIME` 或 `TIMESTAMP` 列与数字值比较时，行为与 MySQL 不一致的问题 [#38361](https://github.com/pingcap/tidb/issues/38361) @[yibin87](https://github.com/yibin87)
    - 修复无符号类型与 `Duration` 类型常量比较时产生的结果错误 [#45410](https://github.com/pingcap/tidb/issues/45410) @[wshwsh12](https://github.com/wshwsh12)
    - 修复 access path 的启发式规则会忽略 `READ_FROM_STORAGE(TIFLASH[...])` Hint 导致 `Can't find a proper physical plan` 的问题 [#40146](https://github.com/pingcap/tidb/issues/40146) @[AilinKid](https://github.com/AilinKid)
    - 修复 `group_concat` 无法解析 `ORDER BY` 列的问题 [#41986](https://github.com/pingcap/tidb/issues/41986) @[AilinKid](https://github.com/AilinKid)
    - 修复深嵌套的表达式的 HashCode 重复计算导致的高内存占用和 OOM 问题 [#42788](https://github.com/pingcap/tidb/issues/42788) @[AilinKid](https://github.com/AilinKid)
    - 修复 `cast(col)=range` 条件在 CAST 无精度损失的情况下会导致 FullScan 的问题 [#45199](https://github.com/pingcap/tidb/issues/45199) @[AilinKid](https://github.com/AilinKid)
    - 修复 MPP 执行计划中通过 Union 下推 Aggregation 导致的结果错误 [#45850](https://github.com/pingcap/tidb/issues/45850) @[AilinKid](https://github.com/AilinKid)
    - 修复带 `in (?)` 条件的 binding 无法匹配 `in (?,...?)` 的问题 [#44298](https://github.com/pingcap/tidb/issues/44298) @[qw4990](https://github.com/qw4990)
    - 修复 `non-prep plan cache` 复用执行计划时未考虑 connection collation 导致的错误 [#47008](https://github.com/pingcap/tidb/issues/47008) @[qw4990](https://github.com/qw4990)
    - 修复执行计划没有命中 plan cache 但不报 warning 的问题 [#46159](https://github.com/pingcap/tidb/issues/46159) @[qw4990](https://github.com/qw4990)
    - 修复 `plan replayer dump explain` 会报错的问题 [#46197](https://github.com/pingcap/tidb/issues/46197) @[time-and-fate](https://github.com/time-and-fate)
    - 修复执行带 CTE 的 DML 会导致 panic 的问题 [#46083](https://github.com/pingcap/tidb/issues/46083) @[winoros](https://github.com/winoros)
    - 修复当 JOIN 两个子查询时执行 `TIDB_INLJ` Hint 不生效的问题 [#46160](https://github.com/pingcap/tidb/issues/46160) @[qw4990](https://github.com/qw4990)
    - 修复 `MERGE_JOIN` 的结果错误的问题 [#46580](https://github.com/pingcap/tidb/issues/46580) @[qw4990](https://github.com/qw4990)

+ TiKV

    - 修复开启 Titan 后，TiKV 遇到 `Blob file deleted twice` 报错无法正常启动的问题 [#15454](https://github.com/tikv/tikv/issues/15454) @[Connor1996](https://github.com/Connor1996)
    - 修复 Thread Voluntary 和 Thread Nonvoluntary 监控面板没有数据的问题 [#15413](https://github.com/tikv/tikv/issues/15413) @[SpadeA-Tang](https://github.com/SpadeA-Tang)
    - 修复 raftstore-applys 不断增长的数据错误 [#15371](https://github.com/tikv/tikv/issues/15371) @[Connor1996](https://github.com/Connor1996)
    - 修复由于 Region 的元数据不正确造成 TiKV panic 的问题 [#13311](https://github.com/tikv/tikv/issues/13311) @[zyguan](https://github.com/zyguan)
    - 修复切换 sync_recovery 到 sync 后 QPS 降至 0 的问题 [#15366](https://github.com/tikv/tikv/issues/15366) @[nolouch](https://github.com/nolouch)
    - 修复 Online Unsafe Recovery 超时未中止的问题 [#15346](https://github.com/tikv/tikv/issues/15346) @[Connor1996](https://github.com/Connor1996)
    - 修复 CpuRecord 可能导致的内存泄漏 [#15304](https://github.com/tikv/tikv/issues/15304) @[overvenus](https://github.com/overvenus)
    - 修复当备用集群关闭后，查询主集群出现 `"Error 9002: TiKV server timeout"` 的问题 [#12914](https://github.com/tikv/tikv/issues/12914) @[Connor1996](https://github.com/Connor1996)
    - 修复当主集群恢复后 TiKV 再次启动时，备用 TiKV 会卡住的问题 [#12320](https://github.com/tikv/tikv/issues/12320) @[disksing](https://github.com/disksing)

+ PD

    - 修复在 Flashback 时不更新保存 Region 信息的问题 [#6912](https://github.com/tikv/pd/issues/6912) @[overvenus](https://github.com/overvenus)
    - 修复因为同步 store config 慢而导致 PD Leader 切换慢的问题 [#6918](https://github.com/tikv/pd/issues/6918) @[bufferflies](https://github.com/bufferflies)
    - 修复 Scatter Peer 时未考虑 Group 的问题 [#6962](https://github.com/tikv/pd/issues/6962) @[bufferflies](https://github.com/bufferflies)
    - 修复 RU 消耗小于 0 导致 PD 崩溃的问题 [#6973](https://github.com/tikv/pd/issues/6973) @[CabinfeverB](https://github.com/CabinfeverB)
    - 修复修改隔离等级时未同步到默认放置规则中的问题 [#7121](https://github.com/tikv/pd/issues/7121) @[rleungx](https://github.com/rleungx)
    - 修复在集群规模大时 client-go 周期性更新 `min-resolved-ts` 可能造成 PD OOM 的问题 [#46664](https://github.com/pingcap/tidb/issues/46664) @[HuSharp](https://github.com/HuSharp)

+ TiFlash

    - 修复 Grafana 面板的 `max_snapshot_lifetime` 监控指标显示有误的问题 [#7713](https://github.com/pingcap/tiflash/issues/7713) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复 TiFlash 部分监控页面最长耗时指标显示错误的问题 [#8076](https://github.com/pingcap/tiflash/issues/8076) @[CalvinNeo](https://github.com/CalvinNeo)
    - 修复 TiDB 误报 MPP 任务失败的问题 [#7177](https://github.com/pingcap/tiflash/issues/7177) @[yibin87](https://github.com/yibin87)

+ Tools

    + Backup & Restore (BR)

        - 修复备份失败时 BR 误报 `resolve lock timeout` 掩盖了实际错误的问题 [#43236](https://github.com/pingcap/tidb/issues/43236) @[YuJuncen](https://github.com/YuJuncen)
        - 修复 PITR 恢复隐式主键可能冲突的问题 [#46520](https://github.com/pingcap/tidb/issues/46520) @[3pointer](https://github.com/3pointer)
        - 修复 PITR 恢复数据元信息 (meta-kv) 出错的问题 [#46578](https://github.com/pingcap/tidb/issues/46578) @[Leavrth](https://github.com/Leavrth)
        - 修复 BR 集成测试用例出错的问题 [#46561](https://github.com/pingcap/tidb/issues/46561) @[purelind](https://github.com/purelind)

    + TiCDC

        - 修复 PD 做扩缩容场景下 TiCDC 访问无效旧地址的问题 [#9584](https://github.com/pingcap/tiflow/issues/9584) @[fubinzh](https://github.com/fubinzh) @[asddongmen](https://github.com/asddongmen)
        - 修复某些特殊场景下 changefeed 失败的问题 [#9309](https://github.com/pingcap/tiflow/issues/9309) [#9450](https://github.com/pingcap/tiflow/issues/9450) [#9542](https://github.com/pingcap/tiflow/issues/9542) [#9685](https://github.com/pingcap/tiflow/issues/9685) @[hicqu](https://github.com/hicqu) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - 修复在上游同一个事务中修改多行唯一键场景下，TiCDC 可能导致同步写冲突的问题 [#9430](https://github.com/pingcap/tiflow/issues/9430) @[sdojjy](https://github.com/sdojjy)
        - 修复在上游同一条 DDL 中重命名多个表的场景下同步出错的问题 [#9476](https://github.com/pingcap/tiflow/issues/9476) [#9488](https://github.com/pingcap/tiflow/issues/9488) @[CharlesCheung96](https://github.com/CharlesCheung96) @[asddongmen](https://github.com/asddongmen)
        - 修复 CSV 格式下没有校验中文分隔符的问题 [#9609](https://github.com/pingcap/tiflow/issues/9609) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - 修复所有 changefeed 被移除时会阻塞上游 TiDB GC 的问题 [#9633](https://github.com/pingcap/tiflow/issues/9633) @[sdojjy](https://github.com/sdojjy)
        - 修复开启 `scale-out` 时流量在节点间分配不均匀问题 [#9665](https://github.com/pingcap/tiflow/issues/9665) @[sdojjy](https://github.com/sdojjy)
        - 修复日志中记录了用户敏感信息的问题 [#9690](https://github.com/pingcap/tiflow/issues/9690) @[sdojjy](https://github.com/sdojjy)

    + TiDB Data Migration (DM)

        - 修复 DM 在大小写不敏感的 collation 下无法正确处理冲突的问题 [#9489](https://github.com/pingcap/tiflow/issues/9489) @[hihihuhu](https://github.com/hihihuhu)
        - 修复 DM validator 死锁问题并增强重试 [#9257](https://github.com/pingcap/tiflow/issues/9257) @[D3Hunter](https://github.com/D3Hunter)
        - 修复 DM 在跳过失败 DDL 并且后续无 DDL 执行时显示延迟持续增长的问题 [#9605](https://github.com/pingcap/tiflow/issues/9605) @[D3Hunter](https://github.com/D3Hunter)
        - 修复 DM 在跳过 Online DDL 时无法正确追踪上游表结构的问题 [#9587](https://github.com/pingcap/tiflow/issues/9587) @[GMHDBJD](https://github.com/GMHDBJD)
        - 修复 DM 在乐观模式恢复任务时跳过所有 DML 的问题 [#9588](https://github.com/pingcap/tiflow/issues/9588) @[GMHDBJD](https://github.com/GMHDBJD)
        - 修复 DM 在乐观模式中跳过 Partition DDL 的问题 [#9788](https://github.com/pingcap/tiflow/issues/9788) @[GMHDBJD](https://github.com/GMHDBJD)

    + TiDB Lightning

        - 修复 TiDB Lightning 导入 `NONCLUSTERED auto_increment` 和 `AUTO_ID_CACHE=1` 表后，插入数据报错的问题 [#46100](https://github.com/pingcap/tidb/issues/46100) @[tiancaiamao](https://github.com/tiancaiamao)
        - 修复 `checksum = "optional"` 时 Checksum 阶段仍然报错的问题 [#45382](https://github.com/pingcap/tidb/issues/45382) @[lyzx2001](https://github.com/lyzx2001)
        - 修复当 PD 集群地址变更时数据导入失败的问题 [#43436](https://github.com/pingcap/tidb/issues/43436) @[lichunzhu](https://github.com/lichunzhu)

## 贡献者

感谢来自 TiDB 社区的贡献者们：

- [aidendou](https://github.com/aidendou)
- [coderplay](https://github.com/coderplay)
- [fatelei](https://github.com/fatelei)
- [highpon](https://github.com/highpon)
- [hihihuhu](https://github.com/hihihuhu) （首次贡献者）
- [isabella0428](https://github.com/isabella0428)
- [jiyfhust](https://github.com/jiyfhust)
- [JK1Zhang](https://github.com/JK1Zhang)
- [joker53-1](https://github.com/joker53-1)（首次贡献者）
- [L-maple](https://github.com/L-maple)
- [mittalrishabh](https://github.com/mittalrishabh)
- [paveyry](https://github.com/paveyry)
- [shawn0915](https://github.com/shawn0915)
- [tedyu](https://github.com/tedyu)
- [yumchina](https://github.com/yumchina)
- [ZzzhHe](https://github.com/ZzzhHe)
