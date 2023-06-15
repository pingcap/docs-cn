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

* TiFlash 支持副本选择策略 [#44106](https://github.com/pingcap/tidb/issues/44106) @[XuHuaiyu](https://github.com/XuHuaiyu) **tw@qiancai** <!--1394-->

    在 v7.2.0 版本之前，TiFlash 尽量使用所有节点的副本进行数据扫描及 MPP 计算，以提供最强大的性能。在 v7.2.0 版本中，TiFlash 引入副本选择策略，可以根据节点区域属性，选择特定的副本，并调度部分节点进行数据扫描及 MPP 计算。当集群部署在超过一个机房，并且每个机房都拥有完整的 TiFlash 数据副本时，可以只选择当前机房的 TiFlash 副本，在当前机房的 TiFlash 节点中进行数据扫描和 MPP 计算，避免大量跨机房的网络数据传输。新增系统变量 [`tiflash_replica_read`](/system-variables.md#tiflash_replica_read) 用于设定节点选择策略。

    更多信息，请参考[用户文档](/system-variables.md#tiflash_replica_read)。

* TiFlash 支持 pipeline 执行模型（实验特性） [#6518](https://github.com/pingcap/tiflash/issues/6518) @[SeaRise](https://github.com/SeaRise) **tw@ran-huang** <!--1440-->

    在 v7.2.0 版本之前，TiFlash 引擎中各个任务在执行时，需要自行申请线程资源。TiFlash 引擎通过控制任务数的方式限制线程资源使用，以避免线程资源超用，但是并不能完全避免。在 v7.2.0 版本中，TiFlash 引入 pipeline 执行模型，对所有线程资源进行统一管理，并对所有任务的执行进行统一调度，充分利用线程资源，同时避免资源超用。新增系统变量 [`tidb_enable_tiflash_pipeline_model`](/system-variables.md#tidb_enable_tiflash_pipeline_model) 用于设定是否启用 pipeline 执行模型。

    更多信息，请参考[用户文档](/tiflash/tiflash-pipeline-model.md)。

* 提升统计信息收集的性能 [#issue号](链接) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes) **tw@hfxsd** <!--1352-->

    v7.2.0 优化了统计信息的收集策略，会选择跳过一部分重复的信息，以及对优化器价值不高的信息，提升统计信息收集的整体速度达 30% 。 这个提升有利于 TiDB 对数据库对象的统计信息进行更及时的更新，使得生成的执行计划更准确， 从而达到提升数据库整体性能的目的。

* 提升表和索引一致性检查的性能 [#issue号](链接) @[wjhuang2016](https://github.com/wjhuang2016) **tw@qiancai** <!--1436-->

    TiDB 在新版本中优化了数据一致性校验的方式，大幅提升了 [`ADMIN CHECK [TABLE|INDEX]`](/sql-statements/sql-statement-admin-check-table-index.md) 的执行效率， 性能提升接近 200 倍。 这个能力可以大幅减少大型表数据导入的时间， 提升数据导入的体验。 设置 [`tidb_enable_fast_table_check`](链接) 为 `TRUE` 启用这个新机制。

    更多信息，请参考[用户文档](链接)

### 稳定性

* 自动管理资源超出预期的查询 (实验特性) [#issue号](链接) @[nolouch](https://github.com/nolouch) @[glorv](https://github.com/glorv)  @[Connor1996](https://github.com/Connor1996) @[JmPotato](https://github.com/JmPotato) @[CabinfeverB](https://github.com/CabinfeverB) @[HuSharp](https://github.com/HuSharp) **tw@hfxsd** <!--1411-->

    突发的 SQL 性能问题引发数据库整体性能下降，是数据库稳定性最常见的挑战。 造成 SQL 性能问题的原因有很多， 有可能是未经充分测试的新 SQL，数据量剧烈变化，执行计划突变等等，这些问题很难从源头上完全规避。 TiDB 在 v7.2.0 加入了对资源超出预期的查询的管理能力，在上述问题发生时，能够快速降低影响范围。

    用户可以针对某个资源组 (Resource Group) 设置查询的最长执行时间。 当查询的执行时间超过设置时， 自动降低查询的优先级或者取消查询。  用户还可以设置在一段时间内通过文本立即匹配已经识别出的查询， 从而避免问题查询的并发度太高时，在识别阶段就造成大量消耗的情况。

    对资源超出预期查询的自动管理， 为用户提供了有效的手段，快速应对突发的查询性能问题，降低问题对数据库整体性能的影响，从而提升数据库的稳定性。

    更多信息，请参考[用户文档](链接)。

* 增强对历史执行计划的绑定能力 [#issue号](链接) @[qw4990](https://github.com/qw4990) **tw@Oreoxmt** <!--1349-->

    新版本的 TiDB 对历史执行计划绑定的能力做了进一步增强。 一方面加强了对复杂语句的解析和绑定， 另一方面， 也加入了对新 Hint 的支持，包括 [`AGG_TO_COP()`](/optimizer-hints.md#agg_to_cop)、[`LIMIT_TO_COP()`](/optimizer-hints.md#limit_to_cop)、[`ORDERED_INDEX`](/optimizer-hints.md#order_indext1_name-idx1_name--idx2_name)、[`NO_ORDERED_INDEX()`](/optimizer-hints.md#no_order_indext1_name-idx1_name--idx2_name)。 借助这个能力， 从历史执行计划中创建的 [SQL Binding](/sql-plan-management.md#执行计划绑定-sql-binding) 能够更加稳定的固定住执行计划。 

    更多信息，请参考[用户文档](/sql-plan-management.md#执行计划绑定-sql-binding)。


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

   更多信息，请参考 [用户文档](/ddl-introduction.md#ddl - 相关的命令介绍)。

### 可观测性

* 为统计信息收集增加进度展示 [#issue号](链接) @[hawkingrei](https://github.com/hawkingrei) **tw@Oreoxmt** <!--1380-->

    对大表的统计信息收集经常会持续比较长的时间。 在过去的版本里，用户无从得知统计信息收集的进度，进而没法预测完成时间。 在 v7.2.0 中， TiDB 加入了对统计信息收集进度的信息展示。 新加入 [`SHOW ANALYZE SUMMARY`](链接) 命令，能够以表或分区为单位展示总体工作量，当前进度，以及对完成时间的预测。 在大规模数据导入、SQL 性能优化等场景下，用户能够了解整体任务进展，提升用户体验。

    更多信息，请参考[用户文档](链接)。

### 数据迁移

* 引入新的 SQL statement “import into” （实验特性）,该 SQL 集成了 Lightning 物理导入模式（local backend）的能力,大大提升导入数据的效率。[#42930](https://github.com/pingcap/tidb/issues/42930) @[D3Hunter](https://github.com/D3Hunter) **tw@hfxsd** <!--1413-->

    "import into " 集成了 Lightning 物理导入模式（local backend）的能力，用户可直接编写 "import into“ SQL 导入数据到 TiDB，同时还支持将数据导入任务拆分成多个子任务调度到多个 TiDB 节点，进行并行导入，提升导入性能。在导入空表的场景，用户无需再部署和管理 Lightning ，降低了导入数据难度的同时，大大提升了导入数据效率。

    更多信息，请参考[用户文档](链接)。

* Lightning 物理导入模式（local backend）支持在导入数据前对需要导入的数据是否存在键值冲突进行检测并处理（实验特性）[#41629](https://github.com/pingcap/tidb/issues/41629)@[gozssky](https://github.com/gozssky) @[lance6716](https://github.com/lance6716) **tw@hfxsd** <!--1296-->

    Lightning 物理导入模式（local backend）支持在导入数据前根据目标表的 PK、UK 定义对源文件的数据是否存在键值冲突进行检测。如发现存在冲突数据，在导入过程中用户可以通过配置策略如 replace 或 ignore 来处理冲突的数据，为用户提供了便利性。同时，用户也可以在实际数据导入之前，根据检测结果，提前发现冲突的记录，并排查原因，从源头保障数据质量，保证导入数据的准确性。

    更多信息，请参考[用户文档](链接)。

* Lightning 支持将字符集为 latin1 和 utf8 的源文件导入到 TiDB。[#44434](https://github.com/pingcap/tidb/issues/44434) @[lance6716](https://github.com/lance6716) **tw@qiancai** <!--1432-->

    通过此功能，用户现在可以使用 Lightning 数据导入工具直接将字符集为 latin1 和 utf8 的源文件导入到 TiDB 中。这扩展了用户在处理各种字符集时的数据导入选项的兼容性和灵活性。以前，导入这样的文件需要额外的预处理或转换。现在用户只需在运行 Lightning 导入过程时指定源文件的字符集（latin1 或 utf8）。Lightning 工具会在导入过程中自动处理字符集转换，确保数据的完整性和准确性。

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
|        |                              |      |
|        |                              |      |
|        |                              |      |

### 配置文件参数

| 配置文件 | 配置项 | 修改类型 | 描述 |
| -------- | -------- | -------- | -------- |
|          |          |          |          |
|          |          |          |          |
| TiDB Lightning | `send-kv-pairs` | 废弃 | 从 7.2 版本开始 TiDB Lightning 配置文件的参数 "send-kv-pairs" 不再生效，由新的参数 "send-kv-size" 代替。该新参数用于指定 KV 键值对的大小阈值，单位为 KiB 或 MiB，默认值为 "16 KiB"。当 KV 键值对的大小达到设定的阈值时，它们将立即发送到 TiKV，避免在导入大宽表等一些场景因为 Lightning 节点内存积累键值对过多导致 OOM 的问题。**tw@hfxsd** <!--1420--> |
| TiDB Lightning | `send-kv-size` | 新增 | 从 7.2 版本开始在 Lightning 配置文件 "[tikv-importer]" 这个 Session 中引入 `send-kv-size` 参数，用于设置发单次送到 TiKV 的 KV pairs 的大小。当 KV 键值对的大小达到设定的阈值时，它们将被 Lightning 立即发送到 TiKV，避免在导入大宽表的时候 Lightning 节点因为内存积累键值对过多导致 OOM 的问题。通过调整 "send-kv-size" 参数，你可以在内存使用和导入速度之间找到平衡，提高导入过程的稳定性和效率。**tw@hfxsd** <!--1420-->|
| Data Migration | `strict-optimistic-shard-mode` | 新增 | 用于兼容历史版本 2.0 分库分表同步 DDL 的行为。当用户选择乐观模式时，可以启用该参数，开启后，乐观模式下，同步任务遇到二类 DDL 时，整个任务会中断，在多个表的 DDL变更有依赖关系的场景，可以及时中断，用户手动处理完各表的 DDL 后，再继续同步数据，保障上下游数据的一致性。 **tw@ran-huang** <!--1414-->|

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