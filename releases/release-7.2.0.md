---
title: TiDB 7.2.0 Release Notes
summary: 了解 TiDB 7.2.0 版本的新功能、兼容性变更、改进提升，以及错误修复。
---

# TiDB 7.2.0 Release Notes

发版日期：2023 年 x 月 x 日

TiDB 版本：7.2.0

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v7.2/quick-start-with-tidb) | [下载离线包](https://cn.pingcap.com/product-community/)

在 7.2.0 版本中，你可以获得以下关键特性：

<!-- 关键特性表格 placeholder-->

## 功能详情

### 性能

* 新增支持下推两个[窗口函数](/tiflash/tiflash-supported-pushdown-calculations.md) 至 TiFlash [#7427](https://github.com/pingcap/tiflash/issues/7427)  @[xzhangxian1008](https://github.com/xzhangxian1008) **tw@qiancai** <!--1310-->

    * `FIRST_VALUE`
    * `LAST_VALUE`

* TiFlash 支持 pipeline 执行模型（实验特性） [#6518](https://github.com/pingcap/tiflash/issues/6518) @[SeaRise](https://github.com/SeaRise) **tw@ran-huang** <!--1440-->

    在 v7.2.0 版本之前，TiFlash 引擎中各个任务在执行时，需要自行申请线程资源。TiFlash 引擎通过控制任务数的方式限制线程资源使用，以避免线程资源超用，但是并不能完全避免。在 v7.2.0 版本中，TiFlash 引入 pipeline 执行模型，对所有线程资源进行统一管理，并对所有任务的执行进行统一调度，充分利用线程资源，同时避免资源超用。新增系统变量 [`tidb_enable_tiflash_pipeline_model`](/system-variables.md#tidb_enable_tiflash_pipeline_model) 用于设定是否启用 pipeline 执行模型。

    更多信息，请参考[用户文档](/tiflash/tiflash-pipeline-model.md)。

* 降低 TiFlash 等待 schema 同步的时延 [#7630](https://github.com/pingcap/tiflash/issues/7630) @[hongyunyan](https://github.com/hongyunyan) **tw@qiancai** <!--1361-->

    当表的 schema 变动时，TiFlash 需要及时和 TiKV 同步表的 schema 信息。在 v7.2.0 版本之前，TiFlash 访问表数据时，如果检测到某张表的 schema 变动时，会同步所有表的 schema 信息。即使一张表没有 TiFlash 副本，TiFlash 也会同步该表的 schema 信息。当数据库中有大量表时，读取一张表的数据需要同步所有表的 schema 信息，schema 同步的时延非常高。在 v7.2.0 版本中，TiFlash 优化 schema 同步机制，只同步包含 TiFlash 副本的表的 schema 信息，并且当检测到某张表的 schema 变动时，只同步该表的 schema 信息，降低 TiFlash 同步 schema 的时延。该优化自动生效，不需要任何设定调整。

* 提升统计信息收集的性能 [#44725](https://github.com/pingcap/tidb/issues/44725) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes) **tw@hfxsd** <!--1352-->

    TiDB v7.2.0 优化了统计信息的收集策略，会选择跳过一部分重复的信息，以及对优化器价值不高的信息。统计信息收集的整体速度提升了 30%。该提升有利于 TiDB 对数据库对象的统计信息进行更及时的更新，使得生成的执行计划更准确，从而达到提升数据库整体性能的目的。
    
    更多信息，请参考[用户文档](/system-variables.md#tidb_analyze_skip_column_types-从-v720-版本开始引入)。

* 提升表和索引一致性检查的性能 [#43693](https://github.com/pingcap/tidb/issues/43693) @[wjhuang2016](https://github.com/wjhuang2016) **tw@qiancai** <!--1436-->

    TiDB 在新版本中优化了数据一致性校验的方式，大幅提升了 [`ADMIN CHECK [TABLE|INDEX]`](/sql-statements/sql-statement-admin-check-table-index.md) 的执行效率， 性能提升接近 200 倍。 这个能力可以大幅减少大型表数据一致性检查的时间， 提升运维体验。 设置 [`tidb_enable_fast_table_check`](链接) 为 `TRUE` 启用这个新机制。

    更多信息，请参考[用户文档](链接)

### 稳定性

* 自动管理资源超出预期的查询（实验特性）[#43691](https://github.com/pingcap/tidb/issues/43691) @[Connor1996](https://github.com/Connor1996) @[CabinfeverB](https://github.com/CabinfeverB) @[glorv](https://github.com/glorv) @[HuSharp](https://github.com/HuSharp) @[nolouch](https://github.com/nolouch) **tw@hfxsd** <!--1411-->

    突发的 SQL 性能问题引发数据库整体性能下降，是数据库稳定性最常见的挑战。造成 SQL 性能问题的原因有很多，例如未经充分测试的新 SQL、数据量剧烈变化、执行计划突变。这些问题很难从源头上完全规避。TiDB v7.2.0 增加了对资源超出预期的查询的管理能力，在上述问题发生时，能够快速降低影响范围。

    你可以针对某个资源组 (Resource Group) 设置查询的最长执行时间。当查询的执行时间超过设置时，自动降低查询的优先级或者取消查询。你还可以设置在一段时间内通过文本立即匹配已经识别出的查询，从而避免问题查询的并发度太高时，在识别阶段就造成大量资源消耗的情况。

    对资源超出预期查询的自动管理，为你提供了有效的手段，快速应对突发的查询性能问题，降低对数据库整体性能的影响，从而提升数据库的稳定性。

    更多信息，请参考[用户文档](/tidb-resource-control.md#管理资源消耗超出预期的查询-runaway-queries)。

* 增强对历史执行计划的绑定能力 [#39199](https://github.com/pingcap/tidb/issues/39199) @[qw4990](https://github.com/qw4990) **tw@Oreoxmt** <!--1349-->

    新版本的 TiDB 对历史执行计划绑定的能力做了进一步增强。 一方面加强了对复杂语句的解析和绑定， 另一方面， 也加入了对新 Hint 的支持，包括 [`AGG_TO_COP()`](/optimizer-hints.md#agg_to_cop)、[`LIMIT_TO_COP()`](/optimizer-hints.md#limit_to_cop)、[`ORDERED_INDEX`](/optimizer-hints.md#order_indext1_name-idx1_name--idx2_name)、[`NO_ORDERED_INDEX()`](/optimizer-hints.md#no_order_indext1_name-idx1_name--idx2_name)。 借助这个能力， 从历史执行计划中创建的 [SQL Binding](/sql-plan-management.md#执行计划绑定-sql-binding) 能够更加稳定的固定住执行计划。

    更多信息，请参考[用户文档](/sql-plan-management.md#执行计划绑定-sql-binding)。

* 提供 Optimizer Fix Controls 机制对优化器行为进行细粒度控制 [#43169](https://github.com/pingcap/tidb/issues/43169) @[time-and-fate](https://github.com/time-and-fate) **tw@hfxsd**

    为了生成更合理的执行计划，TiDB 优化器的行为会随产品迭代而不断演进。但在某些特定场景下，这些变化可能引发性能回退。因此 TiDB 引入了 Optimizer Fix Controls 来控制优化器的一部分细粒度行为，你可以对一些新的变化进行回滚或控制。

    每一个可控的行为，都有一个与 Fix 号码对应的 GitHub Issue 进行说明。所有可控的行为列举在文档 [Optimizer Fix Controls](/optimizer-fix-controls.md) 中。通过设置系统变量 [`tidb_opt_fix_control`](/system-variables.md#tidb_opt_fix_control-从-v710-版本开始引入) 可以为一个或多个行为设置目标值，进而达到行为控制的目的。 

    Optimizer Fix Controls 机制加强了你对 TiDB 优化器的细粒度管控能力，为升级过程引发的性能问题提供了新的修复手段，提升 TiDB 的稳定性。 

    更多信息，请参考[用户文档](/optimizer-fix-controls.md)。

### SQL 功能

* 支持 `CHECK` 约束 [#41711](https://github.com/pingcap/tidb/issues/41711) @[fzzf678] (https://github.com/fzzf678) **tw@qiancai** <!--1404-->

    v7.2.0 版本开始，用户可以通过 `CHECK` 约束功能约束表中一个或者多个字段值必须满足特定条件。添加 `CHECK` 约束后，TiDB 会在数据插入或者更新时检查约束条件是否满足，只允许满足约束的数据写入。

    更多信息，请参考[用户文档](链接)。

### 数据库管理

* DDL 任务支持暂停和恢复操作（实验特性）[#18015](https://github.com/pingcap/tidb/issues/18015) @[godouxm](https://github.com/godouxm) **tw@ran-huang** <!--1185-->

    TiDB v7.2.0 之前的版本中，当 DDL 任务执行期间遇到业务高峰时间点时，为了减少对业务的影响，只能手动取消 DDL 任务。TiDB v7.2.0 引入了 DDL 任务的暂停和恢复功能，你可以在高峰时间点暂停 DDL 任务，等到业务高峰时间结束后再恢复 DDL 任务，从而避免了 DDL 操作对业务负载的影响。

    例如，可以通过如下 `ADMIN PAUSE DDL JOBS` 或 `ADMIN RESUME DDL JOBS` 语句暂停或者恢复多个 DDL 任务：

    ```sql
    ADMIN PAUSE DDL JOBS 1,2;
    ADMIN RESUME DDL JOBS 1,2;
```

   更多信息，请参考 [用户文档](/ddl-introduction.md#ddl - 相关的命令介绍)。

### 可观测性

### 数据迁移

* 引入新的 SQL statement “import into” （实验特性）,该 SQL 集成了 Lightning 物理导入模式（local backend）的能力,大大提升导入数据的效率。[#42930](https://github.com/pingcap/tidb/issues/42930) @[D3Hunter](https://github.com/D3Hunter) **tw@qiancai** <!--1413-->

    "import into " 集成了 Lightning 物理导入模式（local backend）的能力，用户可直接编写 "import into“ SQL 导入数据到 TiDB，同时还支持将数据导入任务拆分成多个子任务调度到多个 TiDB 节点，进行并行导入，提升导入性能。在导入空表的场景，用户无需再部署和管理 Lightning ，降低了导入数据难度的同时，大大提升了导入数据效率。

    更多信息，请参考[用户文档](链接)。

* Lightning 支持将字符集为 latin1 的源文件导入到 TiDB。[#44434](https://github.com/pingcap/tidb/issues/44434) @[lance6716](https://github.com/lance6716) **tw@qiancai** <!--1432-->

    通过此功能，用户现在可以使用 Lightning 数据导入工具直接将字符集为 latin1 的源文件导入到 TiDB 中。这扩展了用户在处理各种字符集时的数据导入选项的兼容性和灵活性。以前，导入这样的文件需要额外的预处理或转换。现在用户只需在运行 Lightning 导入过程时指定源文件的字符集。Lightning 工具会在导入过程中自动处理字符集转换，确保数据的完整性和准确性。

    更多信息，请参考[用户文档](https://github.com/pingcap/docs-cn/pull/14172/files)

## 兼容性变更

> **注意：**
>
> 以下为从 v7.1.0 升级至当前版本 (v7.2.0) 所需兼容性变更信息。如果从 v7.0.0 或之前版本升级到当前版本，可能也需要考虑和查看中间版本 release notes 中提到的兼容性变更信息。

### 行为变更

<!-- 此小节包含 MySQL 兼容性变更-->

* 兼容性 1

* 兼容性 2

### 系统变量

| 变量名  | 修改类型（包括新增/修改/删除）    | 描述 |
|--------|------------------------------|------|
| [`tidb_remove_orderby_in_subquery`](/system-variables.md#tidb_remove_orderby_in_subquery-从-v610-版本开始引入) | 修改 | 经进一步的测试后，该变量默认值从 `OFF` 修改为 `ON`，即优化器改写会移除子查询中的 `ORDER BY` 子句。 |
|  [`tidb_analyze_skip_column_types`](/system-variables.md#tidb_analyze_skip_column_types-从-v720-版本开始引入)      |                              新增 |  这个变量表示在执行 `ANALYZE` 命令收集统计信息时，跳过哪些类型的列的统计信息收集。该变量仅适用于 [`tidb_analyze_version = 2`](#tidb_analyze_version-从-v510-版本开始引入) 的情况。使用 `ANALYZE TABLE t COLUMNS c1, ..., cn` 语法时，如果指定的列的类型在 `tidb_analyze_skip_column_types` 中，则不会收集该列的统计信息。    |
| [`tidb_expensive_txn_time_threshold`](/system-variables.md#tidb_expensive_txn_time_threshold-从-v720-版本开始引入) | 新增 | 控制打印 expensive transaction 日志的阈值时间，默认值是 600 秒。expensive transaction 日志会将尚未 COMMIT 或 ROLLBACK 且持续时间超过该阈值的事务的相关信息打印出来。 |
|        |                              |      |
| [`tidb_enable_tiflash_pipeline_model`](/system-variables.md#tidb_enable_tiflash_pipeline_model-从-v720-版本开始引入) | 新增 | 这个变量用来控制是否启用 TiFlash 新的执行模型 [Pipeline Model](/tiflash/tiflash-pipeline-model.md)，默认值为 `OFF`，即关闭 Pipeline Model。 |

### 配置文件参数

| 配置文件 | 配置项 | 修改类型 | 描述 |
| -------- | -------- | -------- | -------- |
|          |          |          |          |
|          |          |          |          |
| TiKV | [<code>rocksdb.\[defaultcf\|writecf\|lockcf\].optimize-filters-for-memory</code>](/tikv-configuration-file.md#optimize-filters-for-memory-从-v710-版本开始引入) | 新增 | 控制是否生成能够最小化内存碎片的 Bloom/Ribbon filter。 |
| TiKV | [<code>rocksdb.\[defaultcf\|writecf\|lockcf\].ribbon-filter-above-level</code>](/tikv-configuration-file.md#ribbon-filter-above-level-从-v710-版本开始引入) | 新增 | 控制是否对于大于等于该值的 level 使用 Ribbon filter，对于小于该值的 level，使用非 block-based bloom filter。 |
| TiDB Lightning | `send-kv-pairs` | 废弃 | 从 v7.2.0 版本开始，`send-kv-pairs` 不再生效。你可以使用新参数 [`send-kv-size`](/tidb-lightning/tidb-lightning-configuration.md) 来指定物理导入模式下向 TiKV 发送数据时一次请求的最大大小。**tw@hfxsd** <!--1420--> |
| TiDB Lightning | [`send-kv-size`](/tidb-lightning/tidb-lightning-configuration.md) | 新增 | 用于设置单次发送到 TiKV 的 KV Pairs 的大小。当 KV 键值对的大小达到设定的阈值时，它们将被 TiDB Lightning 立即发送到 TiKV，避免在导入大宽表的时候由于 TiDB Lightning 节点内存积累键值对过多导致 OOM 的问题。通过调整该参数，你可以在内存使用和导入速度之间找到平衡，提高导入过程的稳定性和效率。**tw@hfxsd** <!--1420-->|
| Data Migration | [`strict-optimistic-shard-mode`](/dm/feature-shard-merge-optimistic.md) | 新增 | 用于兼容历史版本 TiDB Data Migration v2.0 的分库分表同步 DDL 的行为。当用户选择乐观模式时，可以启用该参数，开启后，乐观模式下，同步任务遇到二类 DDL 时，整个任务会中断。在多个表的 DDL 变更有依赖关系的场景，可以及时中断同步，在用户手动处理完各表的 DDL 后，再继续同步数据，保障上下游数据的一致性。 **tw@ran-huang** <!--1414-->|
｜ TiCDC ｜ [`sink.protocol`](/ticdc/ticdc-changefeed-config.md) ｜ 修改 ｜ 扩展下游类型是 Kafka 时的可选值范围：增加 `"open-protocol"`。用于指定编码消息时使用的格式协议。｜
｜ TiCDC ｜ [`sink.delete-only-output-handle-key-columns`](/ticdc/ticdc-changefeed-config.md) ｜ 新增 ｜ 指定 Delete 事件的输出内容，只对 canal-json 和 open-protocol 协议有效。默认值为 false，即输出所有列的内容。当设置为 true 时，只输出主键列，或唯一索引列的内容。 ｜

## 废弃功能

- note [#issue](链接) @[贡献者 GitHub ID](链接)

## 改进提升

+ TiDB

    - 优化构造索引扫描范围的逻辑，支持将一些复杂条件转化为索引扫描范围 [#41572](https://github.com/pingcap/tidb/issues/41572) [#44389](https://github.com/pingcap/tidb/issues/44389) @xuyifangreeneyes
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

- [贡献者 GitHub ID](链接)