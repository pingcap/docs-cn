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

* 新增支持下推以下两个[窗口函数](/tiflash/tiflash-supported-pushdown-calculations.md) 到 TiFlash [#7427](https://github.com/pingcap/tiflash/issues/7427)  @[xzhangxian1008](https://github.com/xzhangxian1008) **tw@qiancai** <!--1310-->

    * `FIRST_VALUE`
    * `LAST_VALUE`

* TiFlash 支持 Pipeline 执行模型（实验特性） [#6518](https://github.com/pingcap/tiflash/issues/6518) @[SeaRise](https://github.com/SeaRise) **tw@ran-huang** <!--1440-->

    在 v7.2.0 版本之前，TiFlash 引擎中各个任务在执行时，需要自行申请线程资源。TiFlash 引擎通过控制任务数的方式限制线程资源使用，以避免线程资源超用，但并不能完全避免此问题。因此，在 v7.2.0 中，TiFlash 引入 Pipeline 执行模型，对所有线程资源进行统一管理，并对所有任务的执行进行统一调度，充分利用线程资源，同时避免资源超用。新增系统变量 [`tidb_enable_tiflash_pipeline_model`](/system-variables.md#tidb_enable_tiflash_pipeline_model) 用于设置是否启用 Pipeline 执行模型。

    更多信息，请参考[用户文档](/tiflash/tiflash-pipeline-model.md)。

* 降低 TiFlash 等待 schema 同步的时延 [#7630](https://github.com/pingcap/tiflash/issues/7630) @[hongyunyan](https://github.com/hongyunyan) **tw@qiancai** <!--1361-->

    当表的 schema 发生变化时，TiFlash 需要及时从 TiKV 同步新的表结构信息。在 v7.2.0 之前，当 TiFlash 访问表数据时，只要检测到数据库中的某张表的 schema 发生了变化，TiFlash 就会重新同步该数据库中所有表的 schema 信息。即使一张表没有 TiFlash 副本，TiFlash 也会同步该表的 schema 信息。当数据库中有大量表时，通过 TiFlash 只读取一张表的数据也可能因为需要等待所有表的 schema 信息同步完成而造成较高的时延。
    
    在 v7.2.0 中，TiFlash 优化了 schema 的同步机制，只同步拥有 TiFlash 副本的表的 schema 信息。当检测到某张有 TiFlash 副本的表的 schema 有变化时，TiFlash 只同步该表的 schema 信息，从而降低了 TiFlash 同步 schema 的时延。该优化自动生效，无须任何设置。

* 提升统计信息收集的性能 [#44725](https://github.com/pingcap/tidb/issues/44725) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes) **tw@hfxsd** <!--1352-->

    TiDB v7.2.0 优化了统计信息的收集策略，会选择跳过一部分重复的信息，以及对优化器价值不高的信息，从而将统计信息收集的整体速度提升了 30%。这一改进有利于 TiDB 更及时地更新数据库对象的统计信息，生成更准确的执行计划，从而提升数据库整体性能。

    默认设置下，统计信息收集会跳过类型为 `json`、`blob`、`mediumblob`、`longblob` 的列。你可以通过设置系统变量 [`tidb_analyze_skip_column_types`](/system-variables.md#tidb_analyze_skip_column_types-从-v720-版本开始引入) 来修改默认行为。当前支持设置跳过 `JSON`、`BLOB`、`TEXT` 这几个类型及其子类型。
    
    更多信息，请参考[用户文档](/system-variables.md#tidb_analyze_skip_column_types-从-v720-版本开始引入)。

* 提升数据和索引一致性检查的性能 [#43693](https://github.com/pingcap/tidb/issues/43693) @[wjhuang2016](https://github.com/wjhuang2016) **tw@qiancai** <!--1436-->

    [`ADMIN CHECK [TABLE|INDEX]`](/sql-statements/sql-statement-admin-check-table-index.md) 语句用于校验表中数据和对应索引的一致性。在 v7.2.0 中，TiDB 优化了数据一致性的校验方式，大幅提升了 [`ADMIN CHECK [TABLE|INDEX]`](/sql-statements/sql-statement-admin-check-table-index.md) 语句的执行效率，在大数据量场景中性能能够提升百倍。
    
    该优化默认开启 ([`tidb_enable_fast_table_check`](/system-variables.md#tidb_enable_fast_table_check-从-v720-版本开始引入) 默认为 `ON`)，可以大幅减少大型表数据一致性检查的时间， 提升运维体验。

    更多信息，请参考[用户文档](/system-variables.md#tidb_enable_fast_table_check-从-v720-版本开始引入)。

### 稳定性

* 自动管理资源超出预期的查询（实验特性）[#43691](https://github.com/pingcap/tidb/issues/43691) @[Connor1996](https://github.com/Connor1996) @[CabinfeverB](https://github.com/CabinfeverB) @[glorv](https://github.com/glorv) @[HuSharp](https://github.com/HuSharp) @[nolouch](https://github.com/nolouch) **tw@hfxsd** <!--1411-->

    突发的 SQL 性能问题引发数据库整体性能下降，是数据库稳定性最常见的挑战。造成 SQL 性能问题的原因有很多，例如未经充分测试的新 SQL、数据量剧烈变化、执行计划突变等，这些问题很难从源头上完全规避。TiDB v7.2.0 增加了对资源超出预期的查询的管理能力，在上述问题发生时，能够快速降低影响范围。

    你可以针对某个资源组 (Resource Group) 设置查询的最长执行时间。当查询的执行时间超过设置值时，自动降低查询的优先级或者取消查询。你还可以设置在一段时间内通过文本立即匹配已经识别出的查询，从而避免问题查询的并发度太高时，在识别阶段就造成大量资源消耗的情况。

    对资源超出预期查询的自动管理能力，为你提供了有效的手段，快速应对突发的查询性能问题，降低对数据库整体性能的影响，从而提升数据库的稳定性。

    更多信息，请参考[用户文档](/tidb-resource-control.md#管理资源消耗超出预期的查询-runaway-queries)。

* 增强根据历史执行计划创建绑定的能力 [#39199](https://github.com/pingcap/tidb/issues/39199) @[qw4990](https://github.com/qw4990) **tw@Oreoxmt** <!--1349-->

    TiDB v7.2.0 进一步增强[根据历史执行计划创建绑定](/sql-plan-management.md#根据历史执行计划创建绑定)的能力，加强对复杂语句的解析和绑定，使绑定更稳固，并新增支持对以下 Hint 的绑定。
    
   - [`AGG_TO_COP()`](/optimizer-hints.md#agg_to_cop)
   - [`LIMIT_TO_COP()`](/optimizer-hints.md#limit_to_cop)
   - [`ORDER_INDEX`](/optimizer-hints.md#order_indext1_name-idx1_name--idx2_name) 
   - [`NO_ORDER_INDEX()`](/optimizer-hints.md#no_order_indext1_name-idx1_name--idx2_name)。

    更多信息，请参考[用户文档](/sql-plan-management.md)。

* 提供 Optimizer Fix Controls 机制对优化器行为进行细粒度控制 [#43169](https://github.com/pingcap/tidb/issues/43169) @[time-and-fate](https://github.com/time-and-fate) **tw@hfxsd**

    为了生成更合理的执行计划，TiDB 优化器的行为会随产品迭代而不断演进。但在某些特定场景下，这些变化可能引发性能回退。因此 TiDB 引入了 Optimizer Fix Controls 来控制优化器的一部分细粒度行为，你可以对一些新的变化进行回滚或控制。

    每一个可控的行为，都有一个与 Fix 号码对应的 GitHub Issue 进行说明。所有可控的行为列举在文档 [Optimizer Fix Controls](/optimizer-fix-controls.md) 中。通过设置系统变量 [`tidb_opt_fix_control`](/system-variables.md#tidb_opt_fix_control-从-v710-版本开始引入) 可以为一个或多个行为设置目标值，进而达到行为控制的目的。 

    Optimizer Fix Controls 机制加强了你对 TiDB 优化器的细粒度管控能力，为升级过程引发的性能问题提供了新的修复手段，提升 TiDB 的稳定性。 

    更多信息，请参考[用户文档](/optimizer-fix-controls.md)。

### SQL 功能

* 支持 `CHECK` 约束 [#41711](https://github.com/pingcap/tidb/issues/41711) @[fzzf678] (https://github.com/fzzf678) **tw@qiancai** <!--1404-->

    从 v7.2.0 开始，你可以通过 `CHECK` 约束限制表中的一个或者多个字段值必须满足特定的条件。当为表添加 `CHECK` 约束后，在插入或者更新表的数据时，TiDB 会先检查约束条件是否满足，只允许满足约束的数据写入。

    更多信息，请参考[用户文档](/constraints.md#check-约束)。

### 数据库管理

* DDL 任务支持暂停和恢复操作（实验特性）[#18015](https://github.com/pingcap/tidb/issues/18015) @[godouxm](https://github.com/godouxm) **tw@ran-huang** <!--1185-->

    TiDB v7.2.0 之前的版本中，当 DDL 任务在执行期间遇到业务高峰时，为了减少对业务的影响，只能手动取消 DDL 任务。TiDB v7.2.0 引入了 DDL 任务的暂停和恢复功能，你可以在高峰时间点暂停 DDL 任务，等到业务高峰时间结束后再恢复 DDL 任务，从而避免了 DDL 操作对业务负载的影响。

    例如，可以通过如下 `ADMIN PAUSE DDL JOBS` 或 `ADMIN RESUME DDL JOBS` 语句暂停或者恢复多个 DDL 任务：

    ```sql
    ADMIN PAUSE DDL JOBS 1,2;
    ADMIN RESUME DDL JOBS 1,2;
    ```

   更多信息，请参考[用户文档](/ddl-introduction.md#ddl-相关的命令介绍)。

### 可观测性

### 数据迁移

* 引入新的 SQL 语句 `IMPORT INTO`，大幅提升导入效率（实验特性）[#42930](https://github.com/pingcap/tidb/issues/42930) @[D3Hunter](https://github.com/D3Hunter) **tw@qiancai** <!--1413-->

    `IMPORT INTO` 集成了 TiDB Lightning 的[物理导入模式](/tidb-lightning/tidb-lightning-physical-import-mode.md) 的能力。通过该语句，你可以将 `CSV`、`SQL`、`PARQUET` 等格式的数据快速导入到 TiDB 的一张空表中。这种导入方式无需单独部署和管理 TiDB Lightning，在降低了数据导入难度的同时，大幅提升了数据导入效率。
    
    对于存储在 Amazon S3 或 GCS 的数据文件，在开启了[后端任务分布式框架](/tidb-distributed-execution-framework.md) 后，`IMPORT INTO` 还支持将数据导入任务拆分成多个子任务，并将子任务调度到多个 TiDB 节点并行导入，进一步提升导入性能。

    更多信息，请参考[用户文档](sql-statements/sql-statement-import-into.md)。

* TiDB Lightning 支持将字符集为 latin1 的源文件导入到 TiDB 中 [#44434](https://github.com/pingcap/tidb/issues/44434) @[lance6716](https://github.com/lance6716) **tw@qiancai** <!--1432-->

    通过此功能，你可以使用 TiDB Lightning 将字符集为 latin1 的源文件直接导入到 TiDB 中。在 v7.2.0 之前，导入这样的文件需要额外的预处理或转换。从 v7.2.0 起，你只需在配置 TiDB Lightning 导入任务时指定 `character-set = "latin1"`，TiDB Lightning 就会在导入过程中自动处理字符集的转换，确保数据的完整性和准确性。

    更多信息，请参考[用户文档](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-任务配置)

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
| [`last_insert_id`](/system-variables.md#last_insert_id-从-v530-版本开始引入)  | 修改 |  该变量的最大值从 `9223372036854775807` 修改为 `18446744073709551615`，和 MySQL 保持一致。  |
| [`tidb_remove_orderby_in_subquery`](/system-variables.md#tidb_remove_orderby_in_subquery-从-v610-版本开始引入) | 修改 | 经进一步的测试后，该变量默认值从 `OFF` 修改为 `ON`，即优化器改写会移除子查询中的 `ORDER BY` 子句。 |
| [`tidb_analyze_skip_column_types`](/system-variables.md#tidb_analyze_skip_column_types-从-v720-版本开始引入) | 新增 | 这个变量表示在执行 `ANALYZE` 命令收集统计信息时，跳过哪些类型的列的统计信息收集。该变量仅适用于 [`tidb_analyze_version = 2`](#tidb_analyze_version-从-v510-版本开始引入) 的情况。使用 `ANALYZE TABLE t COLUMNS c1, ..., cn` 语法时，如果指定的列的类型在 `tidb_analyze_skip_column_types` 中，则不会收集该列的统计信息。 |
| [`tidb_enable_fast_table_check`](/system-variables.md#tidb_enable_fast_table_check-从-v720-版本开始引入)      |  新增 |  这个变量用于控制是否使用基于校验和的方式来快速检查表中数据和索引的一致性。默认值 `ON` 表示该功能默认开启。  |
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
| TiDB Lightning | `character-set` | 修改 | 扩展支持导入的字符集，新增 `latin1` 选项，用于导入字符集为 latin1 的源文件。|
| TiDB Lightning | [`send-kv-size`](/tidb-lightning/tidb-lightning-configuration.md) | 新增 | 用于设置单次发送到 TiKV 的键值对的大小。当键值对的大小达到设定的阈值时，它们将被 TiDB Lightning 立即发送到 TiKV，避免在导入大宽表的时候由于 TiDB Lightning 节点内存积累键值对过多导致 OOM 的问题。通过调整该参数，你可以在内存使用和导入速度之间找到平衡，提高导入过程的稳定性和效率。**tw@hfxsd** <!--1420-->|
| Data Migration | [`strict-optimistic-shard-mode`](/dm/feature-shard-merge-optimistic.md) | 新增 | 用于兼容历史版本 TiDB Data Migration v2.0 的分库分表同步 DDL 的行为。当用户选择乐观模式时，可以启用该参数，开启后，乐观模式下，同步任务遇到二类 DDL 时，整个任务会中断。在多个表的 DDL 变更有依赖关系的场景，可以及时中断同步，在用户手动处理完各表的 DDL 后，再继续同步数据，保障上下游数据的一致性。 **tw@ran-huang** <!--1414-->|
｜ TiCDC ｜ [`sink.protocol`](/ticdc/ticdc-changefeed-config.md) ｜ 修改 ｜ 扩展下游类型是 Kafka 时的可选值范围：增加 `"open-protocol"`。用于指定编码消息时使用的格式协议。｜
｜ TiCDC ｜ [`sink.delete-only-output-handle-key-columns`](/ticdc/ticdc-changefeed-config.md) ｜ 新增 ｜ 指定 Delete 事件的输出内容，只对 canal-json 和 open-protocol 协议有效。默认值为 false，即输出所有列的内容。当设置为 true 时，只输出主键列，或唯一索引列的内容。 ｜

## 废弃功能

- note [#issue](链接) @[贡献者 GitHub ID](链接)

## 改进提升

+ TiDB

    - 优化构造索引扫描范围的逻辑，支持将一些复杂条件转化为索引扫描范围 [#41572](https://github.com/pingcap/tidb/issues/41572) [#44389](https://github.com/pingcap/tidb/issues/44389) @xuyifangreeneyes
    - note [#issue](链接) @[贡献者 GitHub ID](链接)
- 为 stale read 新增相关监控指标 [#43325](https://github.com/pingcap/tidb/issues/43325) @[you06](https://github.com/you06)
- 当 stale read retry leader 遇到 lock，resolve lock 之后强制走 leader 避免无谓开销 [#43659](https://github.com/pingcap/tidb/issues/43659) @[you06](https://github.com/you06)
- 使用估计时间计算 stale read ts，减少 stale read 开销 [#44215](https://github.com/pingcap/tidb/issues/44215) @[you06](https://github.com/you06)
- 添加 long running 事务日志和系统变量 [#41471](https://github.com/pingcap/tidb/issues/41471) @[crazycs520](https://github.com/crazycs520)

+ TiKV

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - 使用 gzip 压缩 check leader 请求减少流量消耗   [#14553](https://github.com/tikv/tikv/issues/14553) @[you06](https://github.com/you06)
    - 添加 check leader 相关 metric [#14658](https://github.com/tikv/tikv/issues/14658) @[you06](https://github.com/you06)
    - 详细记录 write command 处理时间细节 [#12362](https://github.com/tikv/tikv/issues/12362) @[cfzjywxk](https://github.com/cfzjywxk)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ PD

    - PD Leader 选举使用单独的 gRPC 链接，防止受到其他请求的影响 [#6403](https://github.com/tikv/pd/issues/6403) @[rleungx](https://github.com/rleungx)
    - 默认打开 bucket split，改善 Multi-Region 的热点问题 [#6433](https://github.com/tikv/pd/issues/6433) @[bufferflies](https://github.com/bufferflies)
    - 新增历史负载信息，避免了存储引擎为 raft-kv2 时，热点调度器对不稳定负载所在的 Region 进行频繁调度 [#6297](https://github.com/tikv/pd/issues/6297) @[bufferflies](https://github.com/bufferflies)
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

    - 修复关联子查询中含有 CTE 时可能出现的查询 hang 住的问题 [#36896](https://github.com/pingcap/tidb/issues/36896) @[guo-shaoge](https://github.com/guo-shaoge)
    - 修复某些情况下 max/min 结果出错的问题 [#43805](https://github.com/pingcap/tidb/issues/43508)@[wshwsh12](https://github.com/wshwsh12)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - 修复当 query 包含子查询时，information schema 显示中 `TxnStart` 字段为空的问题 [#40851](https://github.com/pingcap/tidb/issues/40851) @[crazycs520](https://github.com/crazycs520)
    - 修复 cop task 中 txn scope 缺失导致 stale read global optimization 不生效的问题 [#43365](https://github.com/pingcap/tidb/issues/43365) @[you06](https://github.com/you06)
    - 修复 follower read 未处理 flashback 错误进行重试导致查询报错的问题 [#43673](https://github.com/pingcap/tidb/issues/43673) @[you06](https://github.com/you06)
    - 修复 prepared stale read 语句无法读到预期结果机会的问题 [#43044](https://github.com/pingcap/tidb/issues/43044) @[you06](https://github.com/you06)
    - 修复 on update 语句没有正确更新 primary key 导致数据索引不一致问题 @[zyguan](https://github.com/zyguan)
    - 修复 RC 模式悲观锁缓存可能导致数据不一致的问题 [43294](https://github.com/pingcap/tidb/issues/43294) @[ekexium](https://github.com/ekexium)
```suggestion
 - 修复部分 TiDB 内部 SQL 解析错误问题 [#43392] (https://github.com/pingcap/tidb/issues/43392) @[guo-shaoge](https://github.com/guo-shaoge)
 - 修改 UNIX_TIMESTAMP 函数的上限为 `3001-01-19 03:14:07.999999 UTC` 和 MySQL 8.0.28+ 保持一致 [#43987](https://github.com/pingcap/tidb/issues/43987) @[YangKeao](https://github.com/YangKeao)
 - 修复了 add Index 在 ingest 模式下失败的问题 [#44137](https://github.com/pingcap/tidb/issues/44137) @[tangenta](https://github.com/tangenta)
 - 修复了 cancel 处于在 rollback 状态的 DDL 任务导致相关元数据出错的问题 [#44143](https://github.com/pingcap/tidb/issues/44143)  @[wjhuang2016](https://github.com/wjhuang2016)
 - 修复了 memtracker 配合 cursor 使用导致内存泄漏的问题 [#44254](https://github.com/pingcap/tidb/issues/44254) @[YangKeao](https://github.com/YangKeao)
 - 修复了删除 database 导致 GC 推进慢的问题 [#33069](https://github.com/pingcap/tidb/issues/33069) @[tiancaiamao](https://github.com/tiancaiamao)
 - 修复了分区表在 Index join 的 probe 阶段找不到对应行而报错的问题 [#43686](https://github.com/pingcap/tidb/issues/43686) @[AilinKid](https://github.com/AilinKid) @[mjonss](https://github.com/mjonss)
 - 修复了创建 subpartition 的报错信息 [#41198](https://github.com/pingcap/tidb/issues/41198) [#41200](https://github.com/pingcap/tidb/issues/41200) @[mjonss](https://github.com/mjonss)
 - 修复了执行时间超过 `MAX_EXECUTION_TIME` 被 kill 的返回值和 MySQL 不一致的问题 [#43031] (https://github.com/pingcap/tidb/issues/43031) @[dveeden](https://github.com/dveeden)
+ TiKV

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - 修复锁堆积优化在老版本升级情况下不生效的问题 #[14780](https://github.com/tikv/tikv/issues/14780) @[ekexium](https://github.com/ekexium)
    - 修复 fair lock 在出现 stale req 情况下的正确性问题 #[13298](https://github.com/tikv/tikv/issues/13298) @[cfzjywxk](https://github.com/cfzjywxk)
    - 修复 autocommit point get 在 follower read 情况下线性一致性可能被破坏的问题 #[14715](https://github.com/tikv/tikv/issues/14715) @[cfzjywxkj](https://github.com/cfzjywxk)

+ PD

    - 修复在特殊情况下冗余副本无法自动修复的问题 [#6573](https://github.com/tikv/pd/issues/6573) @[nolouch](https://github.com/nolouch)
    - 修复 region health 监控项在 pd leader 发生变化后丢失的问题 [#6366](https://github.com/tikv/pd/issues/6366)@[iosmanthus](https://github.com/iosmanthus)
    - 修复 nightling 在使用 region label 暂停调度时，导致不健康的副本无法自动修复的问题 [#6426](https://github.com/tikv/pd/issues/6426) @[nolouch](https://github.com/nolouch)
    - 修复使用 pd control 标记 tikv, tikv 重启后 label 丢失的问题 [#6467](https://github.com/tikv/pd/issues/6467) @[JmPotato](https://github.com/JmPotato)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ TiFlash

    - 修复在 join 的 build 端数据量很大且含有大量短字符串时内存消耗过大的问题 [#7416](https://github.com/pingcap/tiflash/issues/7416) @[yibin87](https://github.com/yibin87)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ Tools

    + Backup & Restore (BR)

        - 为外部存储 Azure Blob Storage 提供 SAS (shared access signature) 的访问方式 [#44199](https://github.com/pingcap/tidb/issues/44199) @Leavrth 
        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ TiCDC

- 优化 CDC 同步任务失败时设置 gc ttl 的方法  [#8403](https://github.com/pingcap/tiflow/issues/8403)
- 优化 canal-json 协议在发生 update 操作时输出数据的格式  [#8706](https://github.com/pingcap/tiflow/issues/8706)
- 优化同步到对象存储场景下发生 DDL 时存放数据文件目录的结构  [#8891](https://github.com/pingcap/tiflow/issues/8891)
- 修复同步到对象存储场下上游执行 exchange partition 命令时不能正常执行的问题  [#8914](https://github.com/pingcap/tiflow/issues/8914)
- 优化 CDC 同步有损 DDL 时的行为  [#8686](https://github.com/pingcap/tiflow/issues/8686)
- 增加在 Kafka 场景下 OAuth 认证方式的支持 [#8865](https://github.com/pingcap/tiflow/issues/8865)
- 修复在某些特殊情况下 resolved ts 不能正常推进的问题  [#8963](https://github.com/pingcap/tiflow/issues/8963)
- 修复使用 Avro 或 csv 协议场景下 update  操作不能输出旧值的问题  [#9086](https://github.com/pingcap/tiflow/issues/9086)
- 修复同步到 Kafka 场景下，读取下游 meta 信息太频繁导致下游压力过大的问题  [#8959](https://github.com/pingcap/tiflow/issues/8959)
- 增加同步到 Kafka 场景下，对于 delete 操作，用户可以只选择输出 handle key 的方式  [#9143](https://github.com/pingcap/tiflow/issues/9143)
- 修复同步到 TiDB/MySQL场景下频繁设置下游 BDR 相关变量导致下游日志过多的问题   [#9180](https://github.com/pingcap/tiflow/issues/9180)
- 修复 PD 节点 crash 时导致 CDC节点重启的问题  [#8868](https://github.com/pingcap/tiflow/issues/8868)
- 优化 CDC 做增量扫时的并发控制逻辑，降低 CDC 节点在 crash 时对同步延时的影响  [#8858](https://github.com/pingcap/tiflow/issues/8858)
- 修复 TiCDC 同步到 KOP 时不能正确建立链接的问题  [#8892](https://github.com/pingcap/tiflow/issues/8892)
- 优化 CDC 同步任务失败时设置 gc ttl 的方法  [#8403](https://github.com/pingcap/tiflow/issues/8403)

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