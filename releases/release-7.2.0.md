---
title: TiDB 7.2.0 Release Notes
summary: 了解 TiDB 7.2.0 版本的新功能、兼容性变更、改进提升，以及错误修复。
---

# TiDB 7.2.0 Release Notes

发版日期：2023 年 6 月 29 日

TiDB 版本：7.2.0

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v7.2/quick-start-with-tidb) | [下载离线包](https://cn.pingcap.com/product-community/?version=v7.2.0-DMR#version-list)

在 7.2.0 版本中，你可以获得以下关键特性：

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
    <td rowspan="2">可扩展性与性能</td>
    <td>资源组支持<a href="https://docs.pingcap.com/zh/tidb/v7.2/tidb-resource-control#管理资源消耗超出预期的查询-runaway-queries">管理资源消耗超出预期的查询</a>（实验特性）</td>
    <td>通过此功能，你可以更细粒度地管理执行时间超时的查询，根据查询的不同类型实现不同的行为。符合指定阈值的查询将按照你的设置被降低优先级或者终止执行。
    </td>
  </tr>
  <tr>
    <td>TiFlash 支持 <a href="https://docs.pingcap.com/zh/tidb/v7.2/tiflash-pipeline-model">Pipeline 执行模型</a>（实验特性）</td>
    <td>TiFlash 支持 Pipeline 执行模型，优化对线程资源的控制。</td>
  </tr>
  <tr>
    <td rowspan="1">SQL</td>
    <td>支持新的 SQL 语句 <a href="https://docs.pingcap.com/zh/tidb/v7.2/sql-statement-import-into"><code>IMPORT INTO</code></a>，可以通过 TiDB 进行数据导入（实验特性）</td>
    <td>TiDB 引入了一个新的 SQL 语句 <code>IMPORT INTO</code>。该语句集成了 TiDB Lightning 的物理导入模式的能力，使你无需单独部署和管理 TiDB Lightning 即可导入数据文件到 TiDB 中。例如，通过该语句，你可以直接从 Amazon S3 或 Google Cloud Storage (GCS) 远程导入数据到 TiDB 中。</td>
  </tr>
  <tr>
    <td rowspan="2">数据库管理与可观测性</td>
    <td>DDL 任务支持<a href="https://docs.pingcap.com/zh/tidb/v7.2/ddl-introduction#ddl-相关的命令介绍">暂停和恢复操作</a>（实验特性）</td>
    <td>该功能允许临时暂停资源密集型的 DDL 操作，例如索引创建，以节省资源并最小化对在线流量的影响。当资源许可时，你可以无缝恢复 DDL 任务，而无需取消和重新开始。该功能提高了资源利用率，改善了用户体验，并简化了 schema 更改过程。</td>
  </tr>
</tbody>
</table>

## 功能详情

### 性能

* 新增支持下推以下两个[窗口函数](/tiflash/tiflash-supported-pushdown-calculations.md)到 TiFlash [#7427](https://github.com/pingcap/tiflash/issues/7427) @[xzhangxian1008](https://github.com/xzhangxian1008)

    * `FIRST_VALUE`
    * `LAST_VALUE`

* TiFlash 支持 Pipeline 执行模型（实验特性）[#6518](https://github.com/pingcap/tiflash/issues/6518) @[SeaRise](https://github.com/SeaRise)

    在 v7.2.0 版本之前，TiFlash 引擎中各个任务在执行时，需要自行申请线程资源。TiFlash 引擎通过控制任务数的方式限制线程资源使用，以避免线程资源超用，但并不能完全避免此问题。因此，在 v7.2.0 中，TiFlash 引入 Pipeline 执行模型，对所有线程资源进行统一管理，并对所有任务的执行进行统一调度，充分利用线程资源，同时避免资源超用。新增系统变量 [`tidb_enable_tiflash_pipeline_model`](https://docs.pingcap.com/zh/tidb/v7.2/system-variables#tidb_enable_tiflash_pipeline_model-从-v720-版本开始引入) 用于设置是否启用 Pipeline 执行模型。

    更多信息，请参考[用户文档](/tiflash/tiflash-pipeline-model.md)。

* 降低 TiFlash 等待 schema 同步的时延 [#7630](https://github.com/pingcap/tiflash/issues/7630) @[hongyunyan](https://github.com/hongyunyan)

    当表的 schema 发生变化时，TiFlash 需要及时从 TiKV 同步新的表结构信息。在 v7.2.0 之前，当 TiFlash 访问表数据时，只要检测到数据库中某张表的 schema 发生了变化，TiFlash 就会重新同步该数据库中所有表的 schema 信息。即使一张表没有 TiFlash 副本，TiFlash 也会同步该表的 schema 信息。当数据库中有大量表时，通过 TiFlash 只读取一张表的数据也可能因为需要等待所有表的 schema 信息同步完成而造成较高的时延。

    在 v7.2.0 中，TiFlash 优化了 schema 的同步机制，只同步拥有 TiFlash 副本的表的 schema 信息。当检测到某张有 TiFlash 副本的表的 schema 有变化时，TiFlash 只同步该表的 schema 信息，从而降低了 TiFlash 同步 schema 的时延，同时减少了 DDL 操作对于 TiFlash 同步数据的影响。该优化自动生效，无须任何设置。

* 提升统计信息收集的性能 [#44725](https://github.com/pingcap/tidb/issues/44725) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes)

    TiDB v7.2.0 优化了统计信息的收集策略，会选择跳过一部分重复的信息，以及对优化器价值不高的信息，从而将统计信息收集的整体速度提升了 30%。这一改进有利于 TiDB 更及时地更新数据库对象的统计信息，生成更准确的执行计划，从而提升数据库整体性能。

    默认设置下，统计信息收集会跳过类型为 `JSON`、`BLOB`、`MEDIUMBLOB`、`LONGBLOB` 的列。你可以通过设置系统变量 [`tidb_analyze_skip_column_types`](/system-variables.md#tidb_analyze_skip_column_types-从-v720-版本开始引入) 来修改默认行为。当前支持设置跳过 `JSON`、`BLOB`、`TEXT` 这几个类型及其子类型。

    更多信息，请参考[用户文档](/system-variables.md#tidb_analyze_skip_column_types-从-v720-版本开始引入)。

* 提升数据和索引一致性检查的性能 [#43693](https://github.com/pingcap/tidb/issues/43693) @[wjhuang2016](https://github.com/wjhuang2016)

    [`ADMIN CHECK [TABLE|INDEX]`](/sql-statements/sql-statement-admin-check-table-index.md) 语句用于校验表中数据和对应索引的一致性。在 v7.2.0 中，TiDB 优化了数据一致性的校验方式，大幅提升了 [`ADMIN CHECK [TABLE|INDEX]`](/sql-statements/sql-statement-admin-check-table-index.md) 语句的执行效率，在大数据量场景中性能能够提升百倍。

    该优化默认开启（[`tidb_enable_fast_table_check`](/system-variables.md#tidb_enable_fast_table_check-从-v720-版本开始引入) 默认为 `ON`），可以大幅减少大型表数据一致性检查的时间，提升运维体验。

    更多信息，请参考[用户文档](/system-variables.md#tidb_enable_fast_table_check-从-v720-版本开始引入)。

### 稳定性

* 自动管理资源超出预期的查询（实验特性）[#43691](https://github.com/pingcap/tidb/issues/43691) @[Connor1996](https://github.com/Connor1996) @[CabinfeverB](https://github.com/CabinfeverB) @[glorv](https://github.com/glorv) @[HuSharp](https://github.com/HuSharp) @[nolouch](https://github.com/nolouch)

    突发的 SQL 性能问题引发数据库整体性能下降，是数据库稳定性最常见的挑战。造成 SQL 性能问题的原因有很多，例如未经充分测试的新 SQL、数据量剧烈变化、执行计划突变等，这些问题很难从源头上完全规避。TiDB v7.2.0 增加了对资源超出预期的查询的管理能力，在上述问题发生时，能够快速降低影响范围。

    你可以针对某个资源组 (Resource Group) 设置查询的最长执行时间。当查询的执行时间超过设置值时，自动降低查询的优先级或者取消查询。你还可以设置在一段时间内通过文本或者执行计划立即匹配已经识别出的查询，从而避免问题查询的并发度太高时，在识别阶段就造成大量资源消耗的情况。

    对资源超出预期查询的自动管理能力，为你提供了有效的手段，快速应对突发的查询性能问题，降低对数据库整体性能的影响，从而提升数据库的稳定性。

    更多信息，请参考[用户文档](/tidb-resource-control.md#管理资源消耗超出预期的查询-runaway-queries)。

* 增强根据历史执行计划创建绑定的能力 [#39199](https://github.com/pingcap/tidb/issues/39199) @[qw4990](https://github.com/qw4990)

    TiDB v7.2.0 进一步增强[根据历史执行计划创建绑定](/sql-plan-management.md#根据历史执行计划创建绑定)的能力，加强对复杂语句的解析和绑定，使绑定更稳固，并新增支持对以下 Hint 的绑定：

    - [`AGG_TO_COP()`](/optimizer-hints.md#agg_to_cop)
    - [`LIMIT_TO_COP()`](/optimizer-hints.md#limit_to_cop)
    - [`ORDER_INDEX`](/optimizer-hints.md#order_indext1_name-idx1_name--idx2_name- )
    - [`NO_ORDER_INDEX()`](/optimizer-hints.md#no_order_indext1_name-idx1_name--idx2_name-)

  更多信息，请参考[用户文档](/sql-plan-management.md)。

* 提供 Optimizer Fix Controls 机制对优化器行为进行细粒度控制 [#43169](https://github.com/pingcap/tidb/issues/43169) @[time-and-fate](https://github.com/time-and-fate)

    为了生成更合理的执行计划，TiDB 优化器的行为会随产品迭代而不断演进。但在某些特定场景下，这些变化可能引发性能回退。因此 TiDB 引入了 Optimizer Fix Controls 来控制优化器的一部分细粒度行为，你可以对一些新的变化进行回滚或控制。

    每一个可控的行为，都有一个与 Fix 号码对应的 GitHub Issue 进行说明。所有可控的行为列举在文档 [Optimizer Fix Controls](/optimizer-fix-controls.md) 中。通过设置系统变量 [`tidb_opt_fix_control`](/system-variables.md#tidb_opt_fix_control-从-v653-和-v710-版本开始引入) 可以为一个或多个行为设置目标值，进而达到行为控制的目的。

    Optimizer Fix Controls 机制加强了你对 TiDB 优化器的细粒度管控能力，为升级过程引发的性能问题提供了新的修复手段，提升 TiDB 的稳定性。

    更多信息，请参考[用户文档](/optimizer-fix-controls.md)。

* 轻量统计信息初始化 GA [#42160](https://github.com/pingcap/tidb/issues/42160) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes)

    轻量统计信息初始化自 v7.2.0 成为正式功能。轻量级的统计信息初始化可以大幅减少启动时必须加载的统计信息的数量，从而提升启动过程中统计信息的加载速度。该功能提升了 TiDB 在复杂运行环境下的稳定性，并降低了部分 TiDB 节点重启对整体服务的影响。

    从 v7.2.0 起，新建的集群在启动阶段将默认加载轻量级统计信息，并在加载完成后再对外提供服务。对于从旧版本升级上来的集群，可通过修改 TiDB 配置项 [`lite-init-stats`](/tidb-configuration-file.md#lite-init-stats-从-v710-版本开始引入) 和 [`force-init-stats`](/tidb-configuration-file.md#force-init-stats-从-v657-和-v710-版本开始引入) 为 `true` 开启此功能。

    更多信息，请参考[用户文档](/statistics.md#统计信息的加载)。

### SQL 功能

* 支持 `CHECK` 约束 [#41711](https://github.com/pingcap/tidb/issues/41711) @[fzzf678](https://github.com/fzzf678)

    从 v7.2.0 开始，你可以通过 `CHECK` 约束限制表中的一个或者多个字段值必须满足特定的条件。当为表添加 `CHECK` 约束后，在插入或者更新表的数据时，TiDB 会先检查约束条件是否满足，只允许满足约束的数据写入。

    该功能默认关闭，你可以通过将变量 [`tidb_enable_check_constraint`](/system-variables.md#tidb_enable_check_constraint-从-v720-版本开始引入) 设置为 `ON` 开启该功能。

    更多信息，请参考[用户文档](/constraints.md#check-约束)。

### 数据库管理

* DDL 任务支持暂停和恢复操作（实验特性）[#18015](https://github.com/pingcap/tidb/issues/18015) @[godouxm](https://github.com/godouxm)

    TiDB v7.2.0 之前的版本中，当 DDL 任务在执行期间遇到业务高峰时，为了减少对业务的影响，只能手动取消 DDL 任务。TiDB v7.2.0 引入了 DDL 任务的暂停和恢复功能，你可以在高峰时间点暂停 DDL 任务，等到业务高峰时间结束后再恢复 DDL 任务，从而避免了 DDL 操作对业务负载的影响。

    例如，可以通过如下 `ADMIN PAUSE DDL JOBS` 或 `ADMIN RESUME DDL JOBS` 语句暂停或者恢复多个 DDL 任务：

    ```sql
    ADMIN PAUSE DDL JOBS 1,2;
    ADMIN RESUME DDL JOBS 1,2;
    ```

    更多信息，请参考[用户文档](/ddl-introduction.md#ddl-相关的命令介绍)。

### 数据迁移

* 引入新的 SQL 语句 `IMPORT INTO`，大幅提升数据导入效率（实验特性）[#42930](https://github.com/pingcap/tidb/issues/42930) @[D3Hunter](https://github.com/D3Hunter)

    `IMPORT INTO` 集成了 TiDB Lightning [物理导入模式](/tidb-lightning/tidb-lightning-physical-import-mode.md)的能力。通过该语句，你可以将 CSV、SQL 和 PARQUET 等格式的数据快速导入到 TiDB 的一张空表中。这种导入方式无需单独部署和管理 TiDB Lightning，在降低了数据导入难度的同时，大幅提升了数据导入效率。

    对于存储在 Amazon S3 或 GCS 的数据文件，在开启了 [TiDB 分布式执行框架](/tidb-distributed-execution-framework.md)后，`IMPORT INTO` 还支持将数据导入任务拆分成多个子任务，并将子任务调度到多个 TiDB 节点并行导入，进一步提升导入性能。

    更多信息，请参考[用户文档](/sql-statements/sql-statement-import-into.md)。

* TiDB Lightning 支持将字符集为 latin1 的源文件导入到 TiDB 中 [#44434](https://github.com/pingcap/tidb/issues/44434) @[lance6716](https://github.com/lance6716)

    通过此功能，你可以使用 TiDB Lightning 将字符集为 latin1 的源文件直接导入到 TiDB 中。在 v7.2.0 之前，导入这样的文件需要额外的预处理或转换。从 v7.2.0 起，你只需在配置 TiDB Lightning 导入任务时指定 `character-set = "latin1"`，TiDB Lightning 就会在导入过程中自动处理字符集的转换，以确保数据的完整性和准确性。

    更多信息，请参考[用户文档](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-任务配置)。

## 兼容性变更

> **注意：**
>
> 以下为从 v7.1.0 升级至当前版本 (v7.2.0) 所需兼容性变更信息。如果从 v7.0.0 或之前版本升级到当前版本，可能也需要考虑和查看中间版本 release notes 中提到的兼容性变更信息。

### 行为变更

- TiCDC 在处理 Update 事件时，如果事件的主键或者非空唯一索引的列值发生改变，则会将该条事件拆分为 Delete 和 Insert 两条事件。更多信息，请参考[用户文档](/ticdc/ticdc-split-update-behavior.md#含有单条-update-变更的事务拆分)。

### 系统变量

| 变量名  | 修改类型                      | 描述  |
|--------|------------------------------|------|
| [`last_insert_id`](/system-variables.md#last_insert_id-从-v530-版本开始引入) | 修改 | 该变量的最大值从 `9223372036854775807` 修改为 `18446744073709551615`，和 MySQL 保持一致。  |
| [`tidb_enable_non_prepared_plan_cache`](/system-variables.md#tidb_enable_non_prepared_plan_cache) | 修改 | 经进一步的测试后，该变量默认值从 `OFF` 修改为 `ON`，即默认开启非 Prepare 语句执行计划缓存。 |
| [`tidb_remove_orderby_in_subquery`](/system-variables.md#tidb_remove_orderby_in_subquery-从-v610-版本开始引入) | 修改 | 经进一步的测试后，该变量默认值从 `OFF` 修改为 `ON`，即优化器改写会移除子查询中的 `ORDER BY` 子句。 |
| [`tidb_analyze_skip_column_types`](/system-variables.md#tidb_analyze_skip_column_types-从-v720-版本开始引入) | 新增 | 这个变量表示在执行 `ANALYZE` 命令收集统计信息时，跳过哪些类型的列的统计信息收集。该变量仅适用于 [`tidb_analyze_version = 2`](/system-variables.md#tidb_analyze_version-从-v510-版本开始引入) 的情况。使用 `ANALYZE TABLE t COLUMNS c1, ..., cn` 语法时，如果指定的列的类型在 `tidb_analyze_skip_column_types` 中，则不会收集该列的统计信息。 |
| [`tidb_enable_check_constraint`](/system-variables.md#tidb_enable_check_constraint-从-v720-版本开始引入) | 新增 | 这个变量用于控制 `CHECK` 约束功能是否开启。默认值 `OFF` 表示该功能默认关闭。 |
| [`tidb_enable_fast_table_check`](/system-variables.md#tidb_enable_fast_table_check-从-v720-版本开始引入) | 新增 | 这个变量用于控制是否使用基于校验和的方式来快速检查表中数据和索引的一致性。默认值 `ON` 表示该功能默认开启。  |
| [`tidb_enable_tiflash_pipeline_model`](https://docs.pingcap.com/zh/tidb/v7.2/system-variables#tidb_enable_tiflash_pipeline_model-从-v720-版本开始引入) | 新增 | 这个变量用来控制是否启用 TiFlash 新的执行模型 [Pipeline Model](/tiflash/tiflash-pipeline-model.md)，默认值为 `OFF`，即关闭 Pipeline Model。 |
| [`tidb_expensive_txn_time_threshold`](/system-variables.md#tidb_expensive_txn_time_threshold-从-v720-版本开始引入) | 新增 | 控制打印 expensive transaction 日志的阈值时间，默认值是 600 秒。expensive transaction 日志会将尚未 COMMIT 或 ROLLBACK 且持续时间超过该阈值的事务的相关信息打印出来。 |

### 配置文件参数

| 配置文件 | 配置项 | 修改类型 | 描述 |
| -------- | -------- | -------- | -------- |
| TiDB | [`lite-init-stats`](/tidb-configuration-file.md#lite-init-stats-从-v710-版本开始引入) | 修改 | 经进一步的测试后，默认值从 `false` 修改为 `true`，表示 TiDB 启动时默认采用轻量级的统计信息初始化，以提高启动时统计信息初始化的效率。 |
| TiDB | [`force-init-stats`](/tidb-configuration-file.md#force-init-stats-从-v657-和-v710-版本开始引入) | 修改 | 配合 `lite-init-stats`，默认值从 `false` 修改为 `true`，表示 TiDB 启动时会等到统计信息初始化完成后再对外提供服务。 |
| TiKV | [<code>rocksdb.\[defaultcf\|writecf\|lockcf\].compaction-guard-min-output-file-size</code>](/tikv-configuration-file.md#compaction-guard-min-output-file-size) | 修改 | 为减小 RocksDB 中 compaction 任务的数据量，该变量默认值从 `"8MB"` 修改为 `"1MB"`。 |
| TiKV | [<code>rocksdb.\[defaultcf\|writecf\|lockcf\].optimize-filters-for-memory</code>](/tikv-configuration-file.md#optimize-filters-for-memory-从-v720-版本开始引入) | 新增 | 控制是否生成能够最小化内存碎片的 Bloom/Ribbon filter。 |
| TiKV | [<code>rocksdb.\[defaultcf\|writecf\|lockcf\].periodic-compaction-seconds</code>](/tikv-configuration-file.md#periodic-compaction-seconds-从-v720-版本开始引入) | 新增 | 控制周期性 compaction 的时间，修改时间超过此值的 SST 文件将被选中进行 compaction，并被重新写入这些 SST 文件所在的层级。 |
| TiKV | [<code>rocksdb.\[defaultcf\|writecf\|lockcf\].ribbon-filter-above-level</code>](/tikv-configuration-file.md#ribbon-filter-above-level-从-v720-版本开始引入) | 新增 | 控制是否对于大于等于该值的 level 使用 Ribbon filter，对于小于该值的 level，使用非 block-based bloom filter。 |
| TiKV | [<code>rocksdb.\[defaultcf\|writecf\|lockcf\].ttl</code>](/tikv-configuration-file.md#ttl-从-v720-版本开始引入) | 新增 | 设置 SST 文件被自动选中执行 compaction 的 TTL 时间。更新时间超过 TTL 的 SST 文件将被选中并进行 compaction。 |
| TiDB Lightning | `send-kv-pairs` | 废弃 | 从 v7.2.0 版本开始，`send-kv-pairs` 不再生效。你可以使用新参数 [`send-kv-size`](/tidb-lightning/tidb-lightning-configuration.md) 来指定物理导入模式下向 TiKV 发送数据时一次请求的最大大小。 |
| TiDB Lightning | [`character-set`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-任务配置) | 修改 | 扩展支持导入的字符集，新增 `latin1` 选项，用于导入字符集为 latin1 的源文件。|
| TiDB Lightning | [`send-kv-size`](/tidb-lightning/tidb-lightning-configuration.md) | 新增 | 用于设置单次发送到 TiKV 的键值对的大小。当键值对的大小达到设定的阈值时，它们将被 TiDB Lightning 立即发送到 TiKV，避免在导入大宽表的时候由于 TiDB Lightning 节点内存积累键值对过多导致 OOM 的问题。通过调整该参数，你可以在内存使用和导入速度之间找到平衡，提高导入过程的稳定性和效率。|
| Data Migration | [`strict-optimistic-shard-mode`](/dm/feature-shard-merge-optimistic.md) | 新增 | 用于兼容历史版本 TiDB Data Migration v2.0 的分库分表同步 DDL 的行为。当用户选择乐观模式时，可以启用该参数，开启后，乐观模式下，同步任务遇到二类 DDL 时，整个任务会中断。在多个表的 DDL 变更有依赖关系的场景，可以及时中断同步，在用户手动处理完各表的 DDL 后，再继续同步数据，保障上下游数据的一致性。|
| TiCDC | [`sink.protocol`](/ticdc/ticdc-changefeed-config.md) | 修改 | 扩展下游类型是 Kafka 时的可选值范围：增加 `"open-protocol"`。用于指定编码消息时使用的格式协议。|
| TiCDC | [`sink.delete-only-output-handle-key-columns`](/ticdc/ticdc-changefeed-config.md) | 新增 | 指定 DELETE 事件的输出内容，只对 `"canal-json"` 和 `"open-protocol"` 协议有效。默认值为 `false`，即输出所有列的内容。当设置为 `true` 时，只输出主键列，或唯一索引列的内容。 |

## 改进提升

+ TiDB

    - 优化构造索引扫描范围的逻辑，支持将一些复杂条件转化为索引扫描范围 [#41572](https://github.com/pingcap/tidb/issues/41572) [#44389](https://github.com/pingcap/tidb/issues/44389) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes)
    - 新增 `Stale Read OPS`、`Stale Read Traffic` 监控指标 [#43325](https://github.com/pingcap/tidb/issues/43325) @[you06](https://github.com/you06)
    - 当 Stale Read 的 retry leader 遇到 lock 时，resolve lock 之后强制重试 leader，避免无谓开销 [#43659](https://github.com/pingcap/tidb/issues/43659) @[you06](https://github.com/you06)
    - 使用估计时间计算 Stale Read ts，减少 Stale Read 的开销 [#44215](https://github.com/pingcap/tidb/issues/44215) @[you06](https://github.com/you06)
    - 添加 long-running 事务日志和系统变量 [#41471](https://github.com/pingcap/tidb/issues/41471) @[crazycs520](https://github.com/crazycs520)
    - 支持通过压缩的 MySQL 协议连接 TiDB，提升数据密集型查询在低网络质量下的性能，并节省带宽成本。该功能支持基于 `zlib` 和 `zstd` 的压缩算法 [#22605](https://github.com/pingcap/tidb/issues/22605) @[dveeden](https://github.com/dveeden)
    - 支持将 `utf8` 和 `utf8mb3` 识别为旧的三字节 UTF-8 字符集编码，有助于将具有旧字符集编码的表从 MySQL 8.0 迁移到 TiDB [#26226](https://github.com/pingcap/tidb/issues/26226) @[dveeden](https://github.com/dveeden)
    - 支持在 `UPDATE` 语句中使用 `:=` 进行赋值操作 [#44751](https://github.com/pingcap/tidb/issues/44751) @[CbcWestwolf](https://github.com/CbcWestwolf)

+ TiKV

    - 支持通过 `pd.retry-interval` 配置在连接请求失败等场景下 PD 连接的重试间隔 [#14964](https://github.com/tikv/tikv/issues/14964) @[rleungx](https://github.com/rleungx)
    - 优化资源管控调度算法，将全局的资源使用量作为调度因素 [#14604](https://github.com/tikv/tikv/issues/14604) @[Connor1996](https://github.com/Connor1996)
    - 使用 gzip 压缩 `check_leader` 请求以减少流量 [#14553](https://github.com/tikv/tikv/issues/14553) @[you06](https://github.com/you06)
    - 为 `check_leader` 请求增加相关监控项 [#14658](https://github.com/tikv/tikv/issues/14658) @[you06](https://github.com/you06)
    - 详细记录 TiKV 处理写入命令过程中的时间信息 [#12362](https://github.com/tikv/tikv/issues/12362) @[cfzjywxk](https://github.com/cfzjywxk)

+ PD

    - PD Leader 选举使用单独的 gRPC 连接，防止受到其他请求的影响 [#6403](https://github.com/tikv/pd/issues/6403) @[rleungx](https://github.com/rleungx)
    - 默认开启 bucket split 以改善多 Region 的热点问题 [#6433](https://github.com/tikv/pd/issues/6433) @[bufferflies](https://github.com/bufferflies)

+ Tools

    + Backup & Restore (BR)

        - 为外部存储 Azure Blob Storage 提供共享访问签名 (SAS) 的访问方式 [#44199](https://github.com/pingcap/tidb/issues/44199) @[Leavrth](https://github.com/Leavrth)

    + TiCDC

        - 优化同步到对象存储场景下发生 DDL 时存放数据文件目录的结构 [#8891](https://github.com/pingcap/tiflow/issues/8891) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - 在同步到 Kafka 场景下，支持 OAUTHBEARER 认证方式 [#8865](https://github.com/pingcap/tiflow/issues/8865) @[hi-rustin](https://github.com/Rustin170506)
        - 在同步到 Kafka 场景下，对于 `DELETE` 操作，支持选择只输出 Handle Key [#9143](https://github.com/pingcap/tiflow/issues/9143) @[3AceShowHand](https://github.com/3AceShowHand)

    + TiDB Data Migration (DM)

        - 支持读取 MySQL 8.0 中的压缩 binlog 作为增量同步的数据源 [#6381](https://github.com/pingcap/tiflow/issues/6381) @[dveeden](https://github.com/dveeden)

    + TiDB Lightning

        - 优化导入数据过程中的重试机制，避免因 leader 切换而导致的错误 [#44263](https://github.com/pingcap/tidb/issues/44263) @[lance6716](https://github.com/lance6716)
        - 数据导入完成后使用 SQL 方式校验 checksum，提升数据校验的稳定性 [#41941](https://github.com/pingcap/tidb/issues/41941) @[GMHDBJD](https://github.com/GMHDBJD)
        - 优化导入宽表时 TiDB Lightning 发生 OOM 的问题 [#43853](https://github.com/pingcap/tidb/issues/43853) @[D3Hunter](https://github.com/D3Hunter)

## 错误修复

+ TiDB

    - 修复使用 CTE 的查询导致 TiDB 卡住的问题 [#43749](https://github.com/pingcap/tidb/issues/43749) [#36896](https://github.com/pingcap/tidb/issues/36896) @[guo-shaoge](https://github.com/guo-shaoge)
    - 修复 `min, max` 查询结果出错的问题 [#43805](https://github.com/pingcap/tidb/issues/43805) @[wshwsh12](https://github.com/wshwsh12)
    - 修复 `SHOW PROCESSLIST` 语句无法显示子查询时间较长语句的事务的 TxnStart 的问题 [#40851](https://github.com/pingcap/tidb/issues/40851) @[crazycs520](https://github.com/crazycs520)
    - 修复由于 Coprocessor task 中 `TxnScope` 缺失导致 Stale Read 全局优化不生效的问题 [#43365](https://github.com/pingcap/tidb/issues/43365) @[you06](https://github.com/you06)
    - 修复 follower read 未处理 flashback 错误而进行重试，导致查询报错的问题 [#43673](https://github.com/pingcap/tidb/issues/43673) @[you06](https://github.com/you06)
    - 修复 `ON UPDATE` 语句没有正确更新主键导致数据索引不一致的问题 [#44565](https://github.com/pingcap/tidb/issues/44565) @[zyguan](https://github.com/zyguan)
    - 修复权限表中一些列大小写敏感的问题 [#41048](https://github.com/pingcap/tidb/issues/41048) @[bb7133](https://github.com/bb7133)
    - 修改 `UNIX_TIMESTAMP()` 函数的上限为 `3001-01-19 03:14:07.999999 UTC`，与 MySQL 8.0.28+ 保持一致 [#43987](https://github.com/pingcap/tidb/issues/43987) @[YangKeao](https://github.com/YangKeao)
    - 修复在 ingest 模式下创建索引失败的问题 [#44137](https://github.com/pingcap/tidb/issues/44137) @[tangenta](https://github.com/tangenta)
    - 修复取消处于 rollback 状态的 DDL 任务导致相关元数据出错的问题 [#44143](https://github.com/pingcap/tidb/issues/44143) @[wjhuang2016](https://github.com/wjhuang2016)
    - 修复 `memTracker` 配合 cursor fetch 使用导致内存泄漏的问题 [#44254](https://github.com/pingcap/tidb/issues/44254) @[YangKeao](https://github.com/YangKeao)
    - 修复删除数据库导致 GC 推进慢的问题 [#33069](https://github.com/pingcap/tidb/issues/33069) @[tiancaiamao](https://github.com/tiancaiamao)
    - 修复分区表在 Index Join 的 probe 阶段找不到对应行而报错的问题 [#43686](https://github.com/pingcap/tidb/issues/43686) @[AilinKid](https://github.com/AilinKid) @[mjonss](https://github.com/mjonss)
    - 修复在创建分区表时使用 `SUBPARTITION` 没有警告提醒的问题 [#41198](https://github.com/pingcap/tidb/issues/41198) [#41200](https://github.com/pingcap/tidb/issues/41200) @[mjonss](https://github.com/mjonss)
    - 修复执行时间超过 `MAX_EXECUTION_TIME` 的 query 被 kill 时的报错信息和 MySQL 不一致的问题 [#43031](https://github.com/pingcap/tidb/issues/43031) @[dveeden](https://github.com/dveeden)
    - 修复 `LEADING` hint 不支持查询块别名 (query block alias) 的问题 [#44645](https://github.com/pingcap/tidb/issues/44645) @[qw4990](https://github.com/qw4990)
    - 修复 `LAST_INSERT_ID()` 函数的返回类型，从 VARCHAR 变更为 LONGLONG，与 MySQL 一致 [#44574](https://github.com/pingcap/tidb/issues/44574) @[Defined2014](https://github.com/Defined2014)
    - 修复在带有非关联子查询的语句中使用公共表表达式 (CTE) 可能导致结果错误的问题 [#44051](https://github.com/pingcap/tidb/issues/44051) @[winoros](https://github.com/winoros)
    - 修复 Join Reorder 可能会造成 Outer Join 结果错误的问题 [#44314](https://github.com/pingcap/tidb/issues/44314) @[AilinKid](https://github.com/AilinKid)
    - 修复 `PREPARE stmt FROM "ANALYZE TABLE xxx"` 会被 `tidb_mem_quota_query` kill 掉的问题 [#44320](https://github.com/pingcap/tidb/issues/44320) @[chrysan](https://github.com/chrysan)

+ TiKV

    - 修复处理 stale 悲观锁冲突时事务返回值不正确的问题 [#13298](https://github.com/tikv/tikv/issues/13298) @[cfzjywxk](https://github.com/cfzjywxk)
    - 修复内存悲观锁可能导致 Flashback 失败和数据不一致的问题 [#13303](https://github.com/tikv/tikv/issues/13303) @[JmPotato](https://github.com/JmPotato)
    - 修复处理过期请求时 fair lock 的正确性问题 [#13298](https://github.com/tikv/tikv/issues/13298) @[cfzjywxk](https://github.com/cfzjywxk)
    - 修复 autocommit 和 point get replica read 可能破坏线性一致性的问题 [#14715](https://github.com/tikv/tikv/issues/14715) @[cfzjywxk](https://github.com/cfzjywxk)

+ PD

    - 修复在特殊情况下冗余副本无法自动修复的问题 [#6573](https://github.com/tikv/pd/issues/6573) @[nolouch](https://github.com/nolouch)

+ TiFlash

    - 修复查询在 Join build 侧数据非常大，且包含许多小型字符串类型列时，消耗的内存可能会超过实际需要的问题 [#7416](https://github.com/pingcap/tiflash/issues/7416) @[yibin87](https://github.com/yibin87)

+ Tools

    + Backup & Restore (BR)

        - 修复某些情况下误报 `checksum mismatch` 的问题 [#44472](https://github.com/pingcap/tidb/issues/44472) @[Leavrth](https://github.com/Leavrth)
        - 修复某些情况下误报 `resolved lock timeout` 的问题 [#43236](https://github.com/pingcap/tidb/issues/43236) @[YuJuncen](https://github.com/YuJuncen)
        - 修复在恢复统计信息的时候可能会 panic 的问题 [#44490](https://github.com/pingcap/tidb/issues/44490) @[tangenta](https://github.com/tangenta)

    + TiCDC

        - 修复在某些特殊情况下 Resolved TS 不能正常推进的问题 [#8963](https://github.com/pingcap/tiflow/issues/8963) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - 修复使用 Avro 或 CSV 协议场景下 `UPDATE` 操作不能输出旧值的问题 [#9086](https://github.com/pingcap/tiflow/issues/9086) @[3AceShowHand](https://github.com/3AceShowHand)
        - 修复同步到 Kafka 场景下，读取下游 Metadata 太频繁导致下游压力过大的问题 [#8959](https://github.com/pingcap/tiflow/issues/8959) @[hi-rustin](https://github.com/Rustin170506)
        - 修复同步到 TiDB 或 MySQL 场景下，频繁设置下游双向复制相关变量导致下游日志过多的问题 [#9180](https://github.com/pingcap/tiflow/issues/9180) @[asddongmen](https://github.com/asddongmen)
        - 修复 PD 节点宕机导致 TiCDC 节点重启的问题 [#8868](https://github.com/pingcap/tiflow/issues/8868) @[asddongmen](https://github.com/asddongmen)
        - 修复 TiCDC 同步到 Kafka-on-Pulsar 时不能正确建立连接的问题 [#8892](https://github.com/pingcap/tiflow/issues/8892) @[hi-rustin](https://github.com/Rustin170506)

    + TiDB Lightning

        - 修复开启 `experimental.allow-expression-index` 且默认值是 UUID 时导致 TiDB Lightning panic 的问题 [#44497](https://github.com/pingcap/tidb/issues/44497) @[lichunzhu](https://github.com/lichunzhu)
        - 修复划分数据文件时任务退出导致 TiDB Lightning panic 的问题 [#43195](https://github.com/pingcap/tidb/issues/43195) @[lance6716](https://github.com/lance6716)

## 贡献者

感谢来自 TiDB 社区的贡献者们：

- [asjdf](https://github.com/asjdf)
- [blacktear23](https://github.com/blacktear23)
- [Cavan-xu](https://github.com/Cavan-xu)
- [darraes](https://github.com/darraes)
- [demoManito](https://github.com/demoManito)
- [dhysum](https://github.com/dhysum)
- [happy-v587](https://github.com/happy-v587)
- [jiyfhust](https://github.com/jiyfhust)
- [L-maple](https://github.com/L-maple)
- [nyurik](https://github.com/nyurik)
- [SeigeC](https://github.com/SeigeC)
- [tangjingyu97](https://github.com/tangjingyu97)