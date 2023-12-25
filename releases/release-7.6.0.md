---
title: TiDB 7.6.0 Release Notes
summary: 了解 TiDB 7.6.0 版本的新功能、兼容性变更、改进提升，以及错误修复。
---

# TiDB 7.6.0 Release Notes

发版日期：202x 年 x 月 x 日

TiDB 版本：7.6.0

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v7.6/quick-start-with-tidb) | [下载离线包](https://cn.pingcap.com/product-community/?version=v7.6.0-DMR#version-list)

在 7.6.0 版本中，你可以获得以下关键特性：

## 功能详情

### 可扩展性

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

### 性能

* BR 快照恢复速度最大提升 10 倍 [#33937](https://github.com/pingcap/tidb/issues/33937) @[3pointer](https://github.com/3pointer) **tw@Oreoxmt** <!--1647-->

    随着 TiDB 集群规模的不断扩大，在故障时快速恢复集群以减少业务中断时间变得愈发关键。`br` v7.6.0 之前的版本中， `region` 打散算法一直是性能恢复的瓶颈。然而，在 `br` v7.6.0 中，我们对 `region` 打散算法进行了优化，迅速地将恢复任务拆分成大量小任务并批量散布到所有的 TiKV 节点。通过充分利用每个 TiKV 节点的所有资源，我们成功实现了并行快速恢复，在大规模 `region` 场景下，将集群快照恢复速度提升了 10 倍。

    我们为用户提供了 `--granularity` 命令行参数，通过设置该参数可以启用新的并行恢复算法。例如：(命令行参数例子待研发提供)

    ```sql

    ```

    更多信息，请参考[用户文档](链接)。

* TiDB 提供支持落盘的并发 HashAgg 算法（实验特性） [#35637](https://github.com/pingcap/tidb/issues/35637) @[xzhangxian1008](https://github.com/xzhangxian1008) **tw@qiancai** <!--1365-->

    在之前的版本中，TiDB 的 HashAgg 算子的并发算法不支持落盘，所有数据必须在内存中进行处理。这导致数据量较大、超过内存总量，需要使用 HashAgg 的落盘功能时，必须选择非并发算法，从而无法通过并发提升性能。在 7.6.0 版本中，TiDB 提供支持落盘的并发 HashAgg 算法。在任意并发条件下，HashAgg 算子都可以根据内存使用情况自动触发数据落盘，从而兼顾性能和处理数据量。目前，该功能作为实验特性，引入变量 `tidb_enable_concurrent_hashagg_spill` 控制是否启用支持落盘的并发 HashAgg 算法。当该变量设置为 `true` 时，HashAgg 将使用支持落盘的并发算法。该变量将在功能正式发布时废弃。

    更多信息，请参考[用户文档](链接)。

* 支持下推字符串函数 `LOWER` 到 TiKV [#48170](https://github.com/pingcap/tidb/issues/48170) @[gengliqi](https://github.com/gengliqi) **tw@qiancai** <!--1607-->

    * `LOWER`

    更多信息，请参考[用户文档](/functions-and-operators/expressions-pushed-down.md)。

* 新增支持下推以下 JSON 函数到 TiFlash [#48350](https://github.com/pingcap/tidb/issues/48350) [#48986](https://github.com/pingcap/tidb/issues/48986) [#48994](https://github.com/pingcap/tidb/issues/48994) [#49345](https://github.com/pingcap/tidb/issues/49345) @[SeaRise](https://github.com/SeaRise) @[yibin87](https://github.com/yibin87) **tw@qiancai** <!--1608-->

    * `JSON_UNQUOTE`
    * `JSON_ARRAY`
    * `JSON_DEPTH`

    更多信息，请参考[用户文档](/tiflash/tiflash-supported-pushdown-calculations.md)。

* 包含分区表的执行计划可以被缓存 [#issue号](链接) @[mjonss](https://github.com/mjonss) **tw@qiancai** <!--1662-->

    执行计划缓存是提升交易系统性能的有效手段。 自 7.6.0 开始， TiDB 解除了分区表的执行计划无法进入执行计划缓存的限制， 包含分区表的 SQL 语句能够从执行计划缓存中受益。 这将进一步提升分区表在 TiDB 的应用场景， 客户可以更多的利用分区技术降低数据读取的数量，提升数据库性能。

    更多信息，请参考[用户文档](/sql-prepared-plan-cache.md)。

* 批量建表的性能提升 10 倍 [#issue号](链接) @[gmhdbjd](https://github.com/gmhdbjd) **tw@hfxsd** <!--1408-->

    在之前的版本里，用户将上游数据库上万张表迁移到 TiDB 时， TiDB 需要消耗较长的时间来创建这些表，效率较低。在 7.6 版本引入新的 DDL 架构，可通过系统参数 tidb_ddl_v2 开启，新版本的 DDL 相比之前版本的 DDL 在批量建表的性能有 10 倍的提升，可大大减少用户建表的时间。

    更多信息，请参考[用户文档](链接)。

* 优化器增强对多值索引的支持 [#47759](https://github.com/pingcap/tidb/issues/47759) [#46539](https://github.com/pingcap/tidb/issues/46539) @[Arenatlx](https://github.com/Arenatlx) @[time-and-fate](https://github.com/time-and-fate) **tw@ran-huang** <!--1405/1584-->

    TiDB 自 v6.6.0 开始引入[多值索引](/sql-statements/sql-statement-create-index.md#多值索引)，提升对 JSON 数据类型的检索性能。在 v7.6.0，优化器增强了对多值索引的支持能力，在复杂使用场景中，能够正确识别和利用多值索引对查询进行优化。

    * 多值索引上的统计信息会被收集，并应用于优化器估算，当一条 SQL 可能选择到数个多值索引时，能够识别开销更小的索引。
    * 当出现用 OR 连接的多个 "member of" 条件时，优化器能够利用 `Index Merge` 操作做更高效的条件过滤。

    更多信息，请参考[用户文档](/sql-statements/sql-statement-create-index.md#多值索引)。

### 稳定性

* 跨数据库绑定执行计划 [#issue号](链接) @[qw4990](https://github.com/qw4990) **tw@Oreoxmt** <!--1613-->

    我们看到越来越多的用户运行 TiDB 支撑其 SaaS 平台。SaaS 平台的一种普遍的建模方式，是把平台上每个租户的数据存入不同的“数据库”，而业务逻辑完全相同。这样我们能看到上百个数据库拥有相同的表和索引定义，运行类似的 SQL 语句。在这种场景下，当我们要对一条 SQL 语句的执行计划进行绑定(SQL Binding)，这条绑定通常对运行在其他数据库的 SQL 也有帮助。

    针对这种应用场景，TiDB 引入了 "通用绑定" (Universal SQL Binding) 进行跨数据库绑定。 用一个执行计划绑定匹配模式相同的 SQL，即使他们运行在不同数据库上。比如，当我们创建了下面绑定，无论 `t1` 和 `t2` 位于哪个数据库，TiDB 都会尝试用此绑定的规则来生成执行计划，而不需要为每个数据库上的 SQL 单独创建。

    ```sql
    CREATE GLOBAL UNIVERSAL BINDING for
        SELECT * FROM t1, t2 WHERE t1.id = t2.id
    USING
        SELECT /*+ merge_join(t1, t2) */ * FROM t1, t2 WHERE t1.id = t2.id;
    ```

    "通用绑定" 还能够有效缓解 Saas 场景中一个常见问题。SaaS 客户的数据及负载可能因为客户业务本身的需要而剧烈变化，通常 SaaS 服务商无法预测。在这个场景下，由于统计信息无法及时更新，数据量由小及大的快速变化经常会引发 SQL 性能问题。为解决这个问题，SaaS 服务商可以用 "通用绑定" 固定大数据量客户已经验证过的执行计划，所有客户的执行计划都会被固定。 针对 SaaS 平台，这一功能的引入为客户带来了显著的便利和体验提升。

    由于 "通用绑定" 会引入一个很小的系统开销（小于1%）， 默认将其关闭。 有需要的用户通过设置变量 [`tidb_opt_enable_universal_binding`]() 为 `YES` 开启。

    更多信息，请参考[用户文档](/sql-plan-management.md)。

### 高可用

* 支持代理组件 TiProxy （实验特性） [#413](https://github.com/pingcap/tiproxy/issues/413) @[djshow832](https://github.com/djshow832) @[xhebox](https://github.com/xhebox) **tw@ran-huang** <!--1596-->

    TiProxy 是 TiDB 的官方代理组件，放置在客户端和 TiDB server 之间，为 TiDB 提供负载均衡、连接保持功能，让 TiDB 集群的负载更加均衡，以及维护操作时不影响用户对数据库的连接访问。

    * 在 TiDB 集群进行滚动重启、滚动升级、缩容等维护操作时，TiDB server 会发生变动，客户端对发生变动的 TiDB server 的连接将被中断。TiProxy 可以在这些维护操作过程中，平滑的将连接迁移至其他 TiDB server，从而让客户端不受到影响。
    * 所有客户端对 TiDB server 的连接都无法动态迁移至其他 TiDB server。当多个 TiDB server 的负载不均衡时，可能出现整体集群资源充足，但是个别 TiDB server 资源耗尽导致延迟大幅度增加的情况。TiProxy 提供连接动态迁移功能，在客户端无感的前提下，将连接从一个 TiDB server 迁移至其他 TiDB server，从而实现 TiDB 集群的负载均衡。

    TiProxy 被集成至 TiUP、TiOperator、Dashboard 等 TiDB 的基本组件中，可以方便的进行配置、部署、运维。

    更多信息，请参考[用户文档](/tiproxy/tiproxy-overview.md)。

### SQL 功能

* LOAD DATA 支持显示事务和回滚 [#49079](https://github.com/pingcap/tidb/pull/49079) @[ekexium](https://github.com/ekexium) **tw@Oreoxmt** <!--1422-->

    在 TiDB v7.6.0 之前，使用 `LOAD DATA` 语句来批量导入数据时，提交方式经历了一些变化。在 TiDB v4.0.0 之前，每导入 20000 行数据就会进行一次提交；从 v4.0.0 到 v6.6.0 版本，默认在一个事务中提交所有行，但也支持通过设置 [`tidb_dml_batch_size`](/system-variables.md#tidb_dml_batch_size) 参数实现分批次提交；自 TiDB v7.0.0 起，仅支持导入后一次性提交数据，[`tidb_dml_batch_size`](/system-variables.md#tidb_dml_batch_size) 参数不再生效。与 MySQL 的 `LOAD DATA` 相比，TiDB v7.6.0 之前的 `LOAD DATA` 在不同版本的事务行为都存在差异，因此在使用该语句时，用户需要额外的调整。

    从 TiDB v7.6.0 版本起，TiDB 的 `LOAD DATA` 的事务行为和其他普通 DML 一致。特别是和 MySQL 的事务行为一致， 事务内的`LOAD DATA` 语句本身不再自动提交当前事务，也不会开启新事务，并且事务内的 `LOAD DATA` 语句可以被显式提交或者回滚。此外，`LOAD DATA` 语句还受 TiDB 事务模式设置（乐观/悲观）影响。这些改进使得用户在从 MySQL 到 TiDB 迁移时不再需要额外的适配工作，让数据导入体验更加一致和可控。

    更多信息，请参考[用户文档](/sql-statements/sql-statement-load-data.md)。

### 数据库管理
* 闪回功能支持精确 TSO [#48372](https://github.com/pingcap/tidb/issues/48372) @[BornChanger](https://github.com/BornChanger/BornChanger) **tw@qiancai** <!--1615-->

    TiDB v7.6.0 提供了更加强大和精确的闪回功能，不仅支持回溯到过去指定的时间点，还可以通过 `FLASHBACK CLUSTER TO TSO` 精确地指定恢复的 [TSO](tso.md) 时间戳，实现更加灵活的数据恢复。例如，此功能可和 TiCDC 联合使用，允许下游 TiDB 集群在暂停数据同步、开启预上线读写测试后，优雅快速地回溯到暂停的 TSO 时间戳并继续通过 TiCDC 同步数据，简化了预上线验证流程和数据管理。
    

    ```sql
    FLASHBACK CLUSTER TO TSO 445494839813079041;
    ````

* 支持自动终止长时间未提交的空闲事务 [#48714](https://github.com/pingcap/tidb/pull/48714) @[crazycs520](https://github.com/crazycs520) **tw@Oreoxmt** <!--1598-->

    我们经常碰到这样的情况，由于网络异常断开或者应用程序的小问题，有时 `commit / rollback` 语句无法正常传送到数据库，导致锁没有被释放，从而触发了事务锁等待问题和数据库的连接数的快速上涨。在测试环境，这种情况经常发生，线上环境偶尔也会出现，而且有的时候很难诊断。因此，TiDB v7.6.0 版本开始支持通过设置 [`tidb_idle_transaction_timeout`](/system-variables.md#tidb_idle_transaction_timeout-从-v760-版本开始引入) 参数，自动终止长时间运行的空闲事务，以防止这种情况的发生。该参数单位是秒，当一个事务空闲时间超过设定的阈值时，系统会自动强制结束该事务的数据库连接并回滚事务。

    更多信息，请参考[用户文档](/system-variables.md#tidb_idle_transaction_timeout-从-v760-版本开始引入)。

* 简化执行计划绑定的语法 [#issue号](链接) @[qw4990](https://github.com/qw4990) **tw@Oreoxmt** <!--1613-->

    TiDB 在新版本中简化的创建执行计划绑定的语法。 在命令中无需提供原 SQL 语句， TiDB 会根据带有 hint 的语句识别出原 SQL。 提升了创建执行计划绑定的便利性。 例如：

    ```sql
    CREATE GLOBAL BINDING
    USING
    SELECT /*+ merge_join(t1, t2) */ * FROM t1, t2 WHERE t1.id = t2.id;
    ```

    更多信息，请参考[用户文档](/sql-plan-management.md)。

* 支持动态调整单行记录大小限制 [#49237](https://github.com/pingcap/tidb/pull/49237) @[zyguan](https://github.com/zyguan) **tw@Oreoxmt** <!--1452-->

    TiDB v7.6.0 之前，事务中单行记录的大小受 TiDB 的配置文件参数 [`txn-entry-size-limit`](/tidb-configuration-file.md#txn-entry-size-limit-从-v50-版本开始引入) 限制。如果超出该限制，TiDB 将返回 `entry too large` 错误。在这种情况下，用户需要修改 TiDB 配置文件并重启 TiDB 才能够生效。为了降低用户的管理成本，TiDB 从 v7.6.0 开始新增了系统变量 [`tidb_txn_entry_size_limit`](/system-variables.md#tidb_txn_entry_size_limit-从-v760-版本开始引入)，支持动态修改该配置项的值。该变量的默认值为 `0`，表示默认使用 [`txn-entry-size-limit`](/tidb-configuration-file.md#txn-entry-size-limit-从-v50-版本开始引入) 的值。但如果设置为非 `0` 值，就会优先使用该变量作为事务中的单行记录大小的限制。这一改进旨在使用户更灵活地调整系统配置，而无需重启 TiDB 生效。

    更多信息，请参考[用户文档](/system-variables.md#tidb_txn_entry_size_limit-从-v760-版本开始引入) 。

* 增强 Bi-directional replication(BDR) 对 DDL 的同步 [#48519](https://github.com/pingcap/tidb/issues/48519) @[okJiang](https://github.com/okJiang) **tw@hfxsd** <!--1521/1525-->

    在使用 TiCDC 对多个 TiDB 集群进行双向同步时，为了避免 DDL 循环同步，禁止了 DDL 的同步。7.6 版本引入 BDR Role 后，集群可以通过正确设置 BDR Role，使某些 DDL 正常同步。

    更多信息，请参考[用户文档](链接)。

* 全局排序功能成为正式功能（GA）该功能可提升 'Add Index',，’Import Into‘ 的性能和稳定性 [#issue号](链接) @[D3Hunter](https://github.com/D3Hunter) **tw@ran-huang** <!--1580/1579-->

    在 v7.4.0 以前，使用[分布式并行执行框架](https://docs.pingcap.com/zh/tidb/v7.4/tidb-distributed-execution-framework)执行 ADD INDEX 或 IMPORT INTO 等任务时，由于 TiDB 本地存储空间有限，只能对部分数据进行局部排序后再导入到 TiKV，这导导入到 TiKV 的数据范围有较多的重叠，需要额外的资源进行处理，降低了 TiKV 的性能和稳定性。

    随着 v7.4.0 引入全局排序特性，可以将数据暂时存储在外部存储（如 S3）中进行全局排序后再导入到 TiKV 中。这一改进降低了 TiKV 对资源的额外消耗，并显著提高了 ADD INDEX 和 IMPORT INTO 等操作的性能和稳定性。该功能在 7.6 版本成为正式功能（GA）。

    更多信息，请参考[用户文档](链接)。

* BR 默认恢复用户账号等系统表数据 [#48567](https://github.com/pingcap/tidb/issues/48567) @[BornChanger](https://github.com/BornChanger) **tw@Oreoxmt** <!--1570/1628-->

    `br` 备份恢复工具从 v5.1.0 开始引入了对 **mysql schema** 下的系统表数据的默认自动备份，但默认情况下不会恢复系统表数据。随后，在 `br` v6.2.0 版本中，我们引入了新的恢复参数 `--with-sys-table`，使用户在恢复数据的同时选择性地恢复部分系统表相关数据，提供了更多的操作灵活性。

    为了进一步简化用户的管理成本，同时为用户提供更直观的默认行为。从 `br` v7.6.0 开始，我们决定将恢复参数 `--with-sys-table` 的默认值设置为开启，并取消 `cloud_admin` 账号过滤。这意味着， `br` 默认支持在数据恢复时同时恢复部分系统表相关数据，特别是用户账号和表的统计信息数据。这一改进旨在使备份恢复操作更加直观且符合用户期望，减轻用户手动配置的负担，提升整体操作体验。

    更多信息，请参考[用户文档](/br/br-snapshot-guide.md)。

### 可观测性

* 资源管控相关观测性增强 [#49318](https://github.com/pingcap/tidb/issues/49318) @[glorv](https://github.com/glorv) @[bufferflies](https://github.com/bufferflies) @[nolouch](https://github.com/nolouch) **tw@hfxsd** <!--1668-->

    随着更多客户利用资源组对业务应用进行隔离，资源管控提供了更丰富的基于资源组的数据，协助客户对资源组的负载，以及资源组设置进行观测。确保发生问题时能够快速发现并缩小诊断范围。其中包括：

    * [慢日志](/identify-slow-queries.md) 增加资源组名称，RU消耗，以及对等待资源耗时。
    * [Statement Summary Tables](/statement-summary-tables.md) 增加资源组名称，RU消耗，以及对等待资源耗时。
    * 增加变量[`ru_by_last_statement`]()，用来立即获取前一条 SQL 的RU消耗。
    * 增加基于资源组的数据库指标：QPS/TPS，执行时间(P999/P99/P95)，失败次数，连接数。

    请参考[慢日志](/identify-slow-queries.md)，[Statement Summary Tables](/statement-summary-tables.md)，[资源管控 (Resource Control) 监控指标详解](/grafana-resource-control-dashboard.md)。

### 安全

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

### 数据迁移

* DataMigration（DM）迁移 MySQL8.0 的功能成为正式功能（GA） [#issue号](链接) @[lyzx2001](https://github.com/lyzx2001) **tw@hfxsd** <!--1617-->

    之前 DM 迁移 MySQL8.0 仅为实验特性，不可用于生产环境。本次对该功能的稳定性，兼容性做了增强，可在生产环境帮助用户平滑、快速地将数据从 MySQL 8.0 迁移到 TiDB。

    更多信息，请参考[用户文档](链接)。

## 兼容性变更

> **注意：**
>
> 以下为从 v7.5.0 升级至当前版本 (v7.6.0) 所需兼容性变更信息。如果从 v7.4.0 或之前版本升级到当前版本，可能也需要考虑和查看中间版本 Release Notes 中提到的兼容性变更信息。

### 行为变更

* 行为变更 1

* 行为变更 2

### MySQL 兼容性

* 兼容性 1

* 兼容性 2

### 系统变量

| 变量名  | 修改类型（包括新增/修改/删除）    | 描述 |
|--------|------------------------------|------|
| tidb_ddl_version |新增                              | 默认取值为 ’1‘ ，表示使用当前的 DDL 架构执行 DDL 任务。如果取值为 ’2‘  表示使用 v2 版本的 DDL 架构执行 DDL 任务，V2 版本对 DDL 功能做了提升，开启后，建表 DDL 的执行速度相比 v1 版本可以成倍提升 |
| [`tidb_idle_transaction_timeout`](/system-variables.md#tidb_idle_transaction_timeout-从-v760-版本开始引入) | 新增 | 用来控制用户会话中事务的空闲超时。当用户会话处于事务状态且空闲时间超过该变量设定的值时，会话会被 Kill 掉。默认值 `0` 表示没有时间限制。 |
| [`tidb_txn_entry_size_limit`](/system-variables.md#tidb_txn_entry_size_limit-从-v760-版本开始引入) | 新增 | 用于动态修改 TiDB 配置项 [`performance.txn-entry-size-limit`](/tidb-configuration-file.md#txn-entry-size-limit-从-v50-版本开始引入)，即限制 TiDB 单行数据的大小。默认值为 `0`，表示默认使用配置项的值。当设置为非 `0` 值时，优先使用该变量的值作为 `txn-entry-size-limit` 的值。 |
|        |                              |      |

### 配置文件参数

| 配置文件 | 配置项 | 修改类型 | 描述 |
| -------- | -------- | -------- | -------- |
| TiKV | [`raftstore.periodic-full-compact-start-times`](/tikv-configuration-file.md#periodic-full-compact-start-times-从-v760-版本开始引入) | 新增 | 设置 TiKV 启动周期性全量数据整理 (Compaction) 的时间。默认值 `[]` 表示默认情况下禁用周期性全量数据整理。 |
| TiKV | [`raftstore.periodic-full-compact-start-max-cpu`](/tikv-configuration-file.md#periodic-full-compact-start-max-cpu-从-v760-版本开始引入) | 新增 | 设置 TiKV 执行周期性全量数据整理时的 CPU 使用率阈值，默认值为 `0.1`。 |
|          |          |          |          |
|          |          |          |          |
|          |          |          |          |

### 系统表

- 新增系统表 [`INFORMATION_SCHEMA.KEYWORDS`](/information-schema/information-schema-keywords.md) 用来展示 TiDB 支持的所有关键字的信息。**tw@Oreoxmt**

### 其他

## 离线包变更

## 废弃功能

* 实验特性 [执行计划的自动演进绑定](https://docs.pingcap.com/zh/tidb/stable/sql-plan-management#%E8%87%AA%E5%8A%A8%E6%BC%94%E8%BF%9B%E7%BB%91%E5%AE%9A-baseline-evolution) 将在 v8.0.0 被废弃，等同的功能将会在后续版本被重新设计。 

* 废弃功能 2

## 改进提升

+ TiDB

    - 终止查询时及时通知 TiKV 以避免执行未开始的数据扫描任务 [#issue](链接) @[wshwsh12](https://github.com/wshwsh12) **tw@qiancai** <!--1634-->
    - 当使用非二进制排序规则并且查询条件中包含 `LIKE` 时，优化器可以生成 IndexRangeScan 以提高执行效率 [#48181](https://github.com/pingcap/tidb/issues/48181) @[time-and-fate](https://github.com/time-and-fate)


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