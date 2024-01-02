---
title: TiDB 7.6.0 Release Notes
summary: 了解 TiDB 7.6.0 版本的新功能、兼容性变更、改进提升，以及错误修复。
---

# TiDB 7.6.0 Release Notes

发版日期：202x 年 x 月 x 日

TiDB 版本：7.6.0

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v7.6/quick-start-with-tidb) | [下载离线包](https://cn.pingcap.com/product-community/?version=v7.6.0-DMR#version-list)

在 7.6.0 版本中，你可以获得以下关键特性：

<table>
<thead>
  <tr>
    <th>分类</th>
    <th>功能/增强</th>
    <th>描述</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td rowspan="3">可扩展性与性能<br></td>
    <td><a href="https://docs.pingcap.com/tidb/v7.6/sql-plan-management#universal-binding">Universal SQL binding</a> {/* tw@Oreoxmt */}</td>
    <td>In use cases with hundreds or thousands of same-schema databases -- such as SaaS data platforms storing a database per customer with equivalent business logic -- having up-to-date stats at all times is challenging. For this, SQL bindings can be used to lock in performance. However, doing so across so many tables is infeasible. Therefore, universal SQL bindings allow for broadcasting bindings across all schema-equivalent databases.</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/tidb/v7.6/br-snapshot-guide#restore-cluster-snapshots">Up to 10x acceleration to snapshot restore</a> {/* tw@Oreoxmt */}</td>
    <td>A new 2-phase region scatter algorithm for preparing a snapshot restore to a cluster was introduced. In clusters with many TiKV nodes, this dramatically improves the cluster resource efficiency by more evenly distributing loading across the nodes, more effectively using per-node network bandwidth. In several real world cases, this causes a 1,000% acceleration of restore speeds.</td>
  </tr>
  <tr>
    <td><a href="">建表性能提升 10 倍</a>  {/* tw@hfxsd */}</td>
    <td>在 v7.6.0 中引入了新的 DDL 架构，批量表创建的性能提高了 10 倍。这一重大改进大大缩短了创建大量表所需的时间。尤其是在 SaaS 场景中，快速创建大量表格（从数万到数十万不等）是一个常见的挑战，使用该特性能显著提升 SaaS 场景的建表速度。</td>
  </tr>
  <tr>
    <td rowspan="2">稳定性与高可用<br></td>
    <td><a href="https://docs.pingcap.com/tidb/v7.6/tiproxy/tiproxy-overview">TiProxy support</a>  {/* tw@ran-huang */}</td>
    <td>全面支持 TiProxy，可通过部署工具轻松部署。TiProxy 可以管理和维护客户端与 TiDB 的连接，在滚动重启、升级以及扩缩容过程中保持连接。</td>
  </tr>
  <tr>
    <td><a href="">Data Migration (DM) 正式支持迁移 MySQL 8.0 (GA)</a>  {/* tw@hfxsd */}</td>
    <td>之前 DM 迁移 MySQL8.0 仅为实验特性，不能用于生产环境。TiDB v7.6.0 增强了该功能的稳定性、兼容性，可在生产环境帮助你平滑、快速地将数据从MySQL 8.0 迁移到 TiDB。在 v7.6.0 中，该功能正式 GA。</td>
  </tr>
</tbody>
</table>

## 功能详情

### 性能

* BR 快照恢复速度最高提升 10 倍 [#33937](https://github.com/pingcap/tidb/issues/33937) @[3pointer](https://github.com/3pointer) **tw@Oreoxmt** <!--1647-->

    随着 TiDB 集群规模的不断扩大，故障时快速恢复集群以减少业务中断时间显得尤为重要。在 v7.6.0 之前的版本中，Region 打散算法是性能恢复的主要瓶颈。在 v7.6.0 中，BR 优化了 Region 打散算法，可以迅速将恢复任务拆分为大量小任务，并批量分散到所有 TiKV 节点上。新的并行恢复算法充分利用每个 TiKV 节点的所有资源，从而实现了并行快速恢复。内部测试结果显示，在大规模 Region 场景下，集群快照恢复速度提升约 10 倍。

    要使用新的并行恢复算法，可以配置 `br` 命令行参数 `--granularity`。例如：(命令行参数例子待研发提供)

    ```sql

    ```

    更多信息，请参考[用户文档](链接)。

* TiDB 的并发 HashAgg 算法支持数据落盘（实验特性） [#35637](https://github.com/pingcap/tidb/issues/35637) @[xzhangxian1008](https://github.com/xzhangxian1008) **tw@qiancai** <!--1365-->

    在之前的 TiDB 版本中， HashAgg 算子的并发算法不支持数据落盘。当 SQL 语句的执行计划包含并发的 HashAgg 算子时，该 SQL 语句的所有数据都只能在内存中进行处理。这导致内存需要处理大量数据，当超过内存限制时，TiDB 只能选择非并发 HashAgg 算法，无法通过并发提升性能。

    在 v7.6.0 中，TiDB 的并发 HashAgg 算法支持数据落盘。在任意并发条件下，HashAgg 算子都可以根据内存使用情况自动触发数据落盘，从而兼顾性能和数据处理量。目前，该功能作为实验特性，引入变量 `tidb_enable_concurrent_hashagg_spill` 控制是否启用支持落盘的并发 HashAgg 算法。当该变量为 `ON` 时，代表启用。该变量将在功能正式发布时废弃。

    更多信息，请参考[用户文档](/system-variables.md#tidb_enable_concurrent_hashagg_spill-从-v760-版本开始引入)。

* 支持下推以下字符串函数到 TiKV [#48170](https://github.com/pingcap/tidb/issues/48170) @[gengliqi](https://github.com/gengliqi) **tw@qiancai** <!--1607-->

    * `LOWER()`
    * `UPPER()`

    更多信息，请参考[用户文档](/functions-and-operators/expressions-pushed-down.md)。

* 新增支持下推以下 JSON 函数到 TiFlash [#48350](https://github.com/pingcap/tidb/issues/48350) [#48986](https://github.com/pingcap/tidb/issues/48986) [#48994](https://github.com/pingcap/tidb/issues/48994) [#49345](https://github.com/pingcap/tidb/issues/49345) [#49392](https://github.com/pingcap/tidb/issues/49392) @[SeaRise](https://github.com/SeaRise) @[yibin87](https://github.com/yibin87) **tw@qiancai** <!--1608-->

    * `JSON_UNQUOTE()`
    * `JSON_ARRAY()`
    * `JSON_DEPTH()`
    * `JSON_VALID()`
    * `JSON_KEYS()`
    * `JSON_CONTAINS_PATH()`

    更多信息，请参考[用户文档](/tiflash/tiflash-supported-pushdown-calculations.md)。

* 包含分区表的执行计划可以被缓存 [#issue号](链接) @[mjonss](https://github.com/mjonss) **tw@qiancai** <!--1622-->

    执行计划缓存是提升交易系统性能的有效手段。 自 7.6.0 开始， TiDB 解除了分区表的执行计划无法进入执行计划缓存的限制， 包含分区表的 SQL 语句能够从执行计划缓存中受益。 这将进一步提升分区表在 TiDB 的应用场景， 客户可以更多的利用分区技术降低数据读取的数量，提升数据库性能。

    更多信息，请参考[用户文档](/sql-prepared-plan-cache.md)。

* 建表性能提升 10 倍 [#49752](https://github.com/pingcap/tidb/issues/49752) @[gmhdbjd](https://github.com/gmhdbjd) **tw@hfxsd** <!--1408-->

    在之前的版本里，将上游数据库上万张表迁移到 TiDB 时，TiDB 创建这些表耗时长，效率低。从 v7.6.0 开始，引入了新的 DDL 架构，可通过系统参数 `tidb_ddl_v2` 开启。相比之前的版本，新版本的 DDL 批量建表性能实现了高达 10 倍的提升，大幅减少了建表时间。

    更多信息，请参考[用户文档](链接)。

* 优化器增强对多值索引的支持 [#47759](https://github.com/pingcap/tidb/issues/47759) [#46539](https://github.com/pingcap/tidb/issues/46539) @[Arenatlx](https://github.com/Arenatlx) @[time-and-fate](https://github.com/time-and-fate) **tw@ran-huang** <!--1405/1584-->

    TiDB 自 v6.6.0 开始引入[多值索引](/sql-statements/sql-statement-create-index.md#多值索引)，提升对 JSON 数据类型的检索性能。在 v7.6.0 中，优化器增强了对多值索引的支持能力，在复杂使用场景下，能够正确识别和利用多值索引来优化查询。

    * 多值索引上的统计信息会被收集，并应用于优化器估算。当一条 SQL 可能选择到数个多值索引时，优化器可以识别开销更小的索引。
    * 当出现用 `OR` 连接的多个 `member of` 条件时，优化器能够为每个 DNF Item（`member of` 条件）匹配一个有效的 Index Partial Path 路径，并将多条路径以 Union 的方式综合起来组成 `Index Merge` 来做更高效的条件过滤和数据读取。

    更多信息，请参考[用户文档](/sql-statements/sql-statement-create-index.md#多值索引)。

### 稳定性

* 跨数据库绑定执行计划 [#48875](https://github.com/pingcap/tidb/issues/48875) @[qw4990](https://github.com/qw4990) **tw@Oreoxmt** <!--1613-->

    在 TiDB 上运行 SaaS 服务时，为了方便数据维护和管理，通常会将每个租户的数据独立存储于不同数据库中，并执行相同的业务逻辑。这导致数百个数据库中存在相同的表和索引定义，执行类似的 SQL 语句。在这种场景下，对一条 SQL 语句的执行计划进行绑定 (SQL Binding) 时，这条绑定通常也适用于其他数据库中的 SQL。

    针对这种应用场景，TiDB v7.6.0 引入跨数据库绑定，可以为模式相同的 SQL 语句绑定相同的执行计划，即使这些 SQL 运行在不同的数据库上。例如，创建绑定时将数据库名用通配符 `*` 表示，如下所示。此时，无论 `t1` 和 `t2` 表位于哪个数据库，TiDB 都将尝试使用此绑定来生成执行计划，无需为每个数据库中的 SQL 单独创建绑定。

    ```sql
    CREATE GLOBAL BINDING FOR
    USING
        SELECT /*+ merge_join(t1, t2) */ t1.id, t2.amount FROM *.t1, *.t2 WHERE t1.id = t2.id;
    ```

    此外，跨数据库绑定能有效缓解由于用户数据和负载的不均衡及其快速变化所引发的 SQL 性能问题。SaaS 服务商可以通过跨数据库绑定，固定大数据量用户已验证的执行计划，从而固定所有用户的执行计划。对于 SaaS 服务商，该功能提供了显著的便利性和体验提升。

    由于跨数据库绑定会带来系统开销（小于 1%），TiDB 默认将其关闭。要使用跨数据库绑定，首先需要开启 [`tidb_opt_enable_fuzzy_binding`](/system-variables.md#tidb_opt_enable_fuzzy_binding-从-v760-版本开始引入) 系统变量。

    更多信息，请参考[用户文档](/sql-plan-management.md#跨数据库绑定执行计划-cross-db-binding)。

### 高可用

* 支持代理组件 TiProxy （实验特性） [#413](https://github.com/pingcap/tiproxy/issues/413) @[djshow832](https://github.com/djshow832) @[xhebox](https://github.com/xhebox) **tw@ran-huang** <!--1596-->

    TiProxy 是 TiDB 的官方代理组件，位于客户端和 TiDB server 之间，为 TiDB 提供负载均衡、连接保持功能，让 TiDB 集群的负载更加均衡，并在维护操作期间不影响用户对数据库的连接访问。

    * 在 TiDB 集群进行滚动重启、滚动升级、缩容等维护操作时，TiDB server 会发生变动，导致客户端与发生变化的 TiDB server 的连接中断。通过使用 TiProxy，可以在这些维护操作过程中平滑地将连接迁移至其他 TiDB server，从而让客户端不受影响。
    * 所有客户端对 TiDB server 的连接都无法动态迁移至其他 TiDB server。当多个 TiDB server 的负载不均衡时，可能出现整体集群资源充足，但某些 TiDB server 资源耗尽导致延迟大幅度增加的情况。为解决此问题，TiProxy 提供连接动态迁移功能，在客户端无感的前提下，将连接从一个 TiDB server 迁移至其他 TiDB server，从而实现 TiDB 集群的负载均衡。

    TiProxy 已集成至 TiUP、TiDB Operator、TiDB Dashboard 等 TiDB 基本组件中，可以方便地进行配置、部署和运维。

    更多信息，请参考[用户文档](/tiproxy/tiproxy-overview.md)。

### SQL 功能

* `LOAD DATA` 支持显式事务和回滚 [#49079](https://github.com/pingcap/tidb/pull/49079) @[ekexium](https://github.com/ekexium) **tw@Oreoxmt** <!--1422-->

    在 TiDB v7.6.0 之前，使用 `LOAD DATA` 语句批量导入数据时，其事务提交方式经历了多次变更。具体来说：在 v4.0.0 之前，每导入 20000 行数据就会进行一次提交。从 v4.0.0 到 v6.6.0，TiDB 默认在一个事务中提交所有行，但也支持通过设置 [`tidb_dml_batch_size`](/system-variables.md#tidb_dml_batch_size) 系统变量实现每固定的行数进行一次提交。自 v7.0.0 起，`tidb_dml_batch_size` 对 `LOAD DATA` 语句不再生效，TiDB 将在一个事务中提交所有行。与 MySQL 相比，TiDB v7.6.0 之前的 `LOAD DATA` 在不同版本中的事务行为都存在差异，导致用户使用该语句时需要额外调整。

    从 v7.6.0 开始，`LOAD DATA` 在事务中与其它普通 DML 的处理方式一致，特别是和 MySQL 的事务行为一致。事务内的 `LOAD DATA` 语句本身不再自动提交当前事务，也不会开启新事务，并且事务内的 `LOAD DATA` 语句可以被显式提交或者回滚。此外，`LOAD DATA` 语句会受 TiDB 事务模式设置（乐观/悲观）影响。这些改进简化了用户从 MySQL 到 TiDB 的迁移过程，使得数据导入体验更加统一和可控。

    更多信息，请参考[用户文档](/sql-statements/sql-statement-load-data.md)。

### 数据库管理

* 闪回功能支持精确 TSO [#48372](https://github.com/pingcap/tidb/issues/48372) @[BornChanger](https://github.com/BornChanger/BornChanger) **tw@qiancai** <!--1615-->

    TiDB v7.6.0 提供了更加强大和精确的闪回功能，不仅支持回溯到过去指定的时间点，还可以通过 `FLASHBACK CLUSTER TO TSO` 精确地指定恢复的 [TSO](tso.md) 时间戳，实现更加灵活的数据恢复。例如，此功能可和 TiCDC 联合使用，允许下游 TiDB 集群在暂停数据同步、开启预上线读写测试后，优雅快速地回溯到暂停的 TSO 时间戳并继续通过 TiCDC 同步数据，简化了预上线验证流程和数据管理。

    ```sql
    FLASHBACK CLUSTER TO TSO 445494839813079041;
    ````

* 支持自动终止长时间未提交的空闲事务 [#48714](https://github.com/pingcap/tidb/pull/48714) @[crazycs520](https://github.com/crazycs520) **tw@Oreoxmt** <!--1598-->

    在网络异常断开或应用程序故障时，`COMMIT`/`ROLLBACK` 语句可能无法正常传送到数据库。这种情况可能导致数据库锁未能及时释放，进而引起事务锁等待以及数据库连接数快速增加。这类问题在测试环境中较常见，但在线上环境也会偶尔发生，并且有时难以迅速诊断。为有效防止此类问题的发生，TiDB v7.6.0 引入 [`tidb_idle_transaction_timeout`](/system-variables.md#tidb_idle_transaction_timeout-从-v760-版本开始引入) 系统变量，以自动终止长时间运行的空闲事务。当用户会话处于事务状态且空闲时间超过该变量设定的值时，TiDB 会自动强制结束该事务的数据库连接并回滚事务。

    更多信息，请参考[用户文档](/system-variables.md#tidb_idle_transaction_timeout-从-v760-版本开始引入)。

* 简化执行计划绑定的语法 [#48876](https://github.com/pingcap/tidb/issues/48876) @[qw4990](https://github.com/qw4990) **tw@Oreoxmt** <!--1613-->

    TiDB v7.6.0 简化了创建执行计划绑定的语法。在创建执行计划绑定的命令中无需提供原 SQL 语句，TiDB 可以根据带 hint 的语句识别出对应的原 SQL。这一改进提高了创建执行计划绑定的便利性。例如：

    ```sql
    CREATE GLOBAL BINDING
    USING
    SELECT /*+ merge_join(t1, t2) */ * FROM t1, t2 WHERE t1.id = t2.id;
    ```

    更多信息，请参考[用户文档](/sql-plan-management.md)。

* 支持动态调整 TiDB 单行记录大小限制 [#49237](https://github.com/pingcap/tidb/pull/49237) @[zyguan](https://github.com/zyguan) **tw@Oreoxmt** <!--1452-->

    在 v7.6.0 之前，事务中单行记录的大小受 TiDB 配置项 [`txn-entry-size-limit`](/tidb-configuration-file.md#txn-entry-size-limit-从-v50-版本开始引入) 限制。如果记录大小超出此限制，TiDB 将返回 `entry too large` 错误。此时，用户需要修改 TiDB 配置文件并重启 TiDB 才能够生效。为降低用户的管理成本，TiDB v7.6.0 新增系统变量 [`tidb_txn_entry_size_limit`](/system-variables.md#tidb_txn_entry_size_limit-从-v760-版本开始引入)，支持动态修改 `txn-entry-size-limit` 配置项的值。该变量的默认值为 `0`，表示默认使用 `txn-entry-size-limit` 配置项的值。当设置为非 `0` 值时，TiDB 优先使用该变量的值作为事务中的单行记录大小的限制。这一改进旨在提高用户调整系统配置的灵活性，无需重启 TiDB 即可生效。

    更多信息，请参考[用户文档](/system-variables.md#tidb_txn_entry_size_limit-从-v760-版本开始引入) 。

* 全局排序功能成为正式功能 (GA)，提升 `ADD INDEX` 和 `ADD INDEX` 的性能和稳定性 [#45719](https://github.com/pingcap/tidb/issues/45719) @[wjhuang2016](https://github.com/wjhuang2016) @[D3Hunter](https://github.com/D3Hunter) **tw@ran-huang** <!--1580/1579-->

    在 v7.4.0 以前，使用[分布式并行执行框架](/tidb-distributed-execution-framework.md)执行 `ADD INDEX` 或 `IMPORT INTO` 等任务时，由于 TiDB 本地存储空间有限，只能对部分数据进行局部排序后再导入到 TiKV。这些导入到 TiKV 的数据范围有较多的重叠，需要额外的资源进行处理，降低了 TiKV 的性能和稳定性。

    随着 v7.4.0 引入全局排序特性，可以将数据暂时存储在外部存储（如 S3）中进行全局排序后再导入到 TiKV 中。这一改进降低了 TiKV 对资源的额外消耗，并显著提高了 `ADD INDEX` 和 `IMPORT INTO` 等操作的性能和稳定性。该功能在 v7.6.0 成为正式功能（GA）。

    更多信息，请参考[用户文档](/tidb-global-sort.md)。

* BR 默认恢复用户账号等系统表数据 [#48567](https://github.com/pingcap/tidb/issues/48567) @[BornChanger](https://github.com/BornChanger) **tw@Oreoxmt** <!--1570/1628-->

    从 `br` v5.1.0 开始，快照备份时默认自动备份 **mysql schema** 下的系统表数据，但恢复数据时默认不恢复系统表数据。在 v6.2.0 中，`br` 增加恢复参数 `--with-sys-table` 支持恢复数据的同时恢复部分系统表相关数据，提供更多的操作灵活性。

    为了进一步降低用户的管理成本，并提供更直观的默认行为。从 v7.6.0 开始，`br` 默认开启恢复参数 `--with-sys-table`，并支持恢复 `user` 为 `cloud_admin` 的用户数据。这意味着 `br` 默认支持恢复数据的同时恢复部分系统表相关数据，特别是用户账号和表的统计信息数据。这一改进旨在使备份恢复操作更加直观和符合用户预期，减轻手动配置的负担，从而提升整体的操作体验。

    更多信息，请参考[用户文档](/br/br-snapshot-guide.md)。

### 可观测性

* 增强资源管控相关的观测性 [#49318](https://github.com/pingcap/tidb/issues/49318) @[glorv](https://github.com/glorv) @[bufferflies](https://github.com/bufferflies) @[nolouch](https://github.com/nolouch) **tw@hfxsd** <!--1668-->

    随着越来越多用户利用资源组对业务应用进行隔离，资源管控提供了更丰富的基于资源组的数据，协助你观测资源组负载、资源组设置，确保出现问题时能够快速发现并精准诊断。其中包括：

    * [慢查询日志](/identify-slow-queries.md) 增加资源组名称、RU 消耗、以及等待资源耗时。
    * [Statement Summary Tables](/statement-summary-tables.md) 增加资源组名称、RU 消耗、以及对等待资源耗时。
    * 向变量 [`tidb_last_query_info`](/system-variables.md#tidb_last_query_info-从-v4014-版本开始引入) 中增加 SQL 的 [RU](/tidb-resource-control.md#什么是-request-unit-ru) 消耗，客户可以利用此变量获取会话中上一条语句的资源消耗。
    * 增加基于[资源组的数据库指标](/grafana-resource-control-dashboard.md)：QPS/TPS、执行时间 (P999/P99/P95)、失败次数、连接数。
    * 增加系统表 [`request_unit_by_group`]() 记录资源组每天的历史资源消耗。

    更多信息，请参考[慢查询日志](/identify-slow-queries.md)、[Statement Summary Tables](/statement-summary-tables.md)、[资源管控 (Resource Control) 监控指标详解](/grafana-resource-control-dashboard.md)。

### 数据迁移

* Data Migration (DM) 支持迁移 MySQL 8.0 的功能成为正式功能（GA）[#10405](https://github.com/pingcap/tiflow/issues/10405) @[lyzx2001](https://github.com/lyzx2001) **tw@hfxsd** <!--1617-->

    之前 DM 迁移 MySQL8.0 仅为实验特性，不能用于生产环境。TiDB v7.6.0 增强了该功能的稳定性、兼容性，可在生产环境帮助你平滑、快速地将数据从 MySQL 8.0 迁移到 TiDB。在 v7.6.0 中，该功能正式 GA。

    更多信息，请参考[用户文档](链接)。

* TiCDC 支持通过双向复制模式 (Bi-Directional Replication, BDR) 同步 DDL 语句 [#10301](https://github.com/pingcap/tiflow/issues/10301) [#48519](https://github.com/pingcap/tidb/issues/48519) @[okJiang](https://github.com/okJiang) @[asddongmen](https://github.com/asddongmen) **tw@hfxsd** <!--1460-->

    从 v7.6.0 开始，TiCDC 支持在配置了双向复制的情况下同步 DDL 语句。以前，TiCDC 不支持复制 DDL 语句，因此要使用 TiCDC 双向复制必须将 DDL 语句分别应用到两个 TiDB 集群。有了该特性，TiCDC 可以为一个集群分配 `PRIMARY` BDR role，并将该集群的 DDL 语句复制到下游集群。

    更多信息，请参考[用户文档](/ticdc/ticdc-bidirectional-replication.md).
## 兼容性变更

> **注意：**
>
> 以下为从 v7.5.0 升级至当前版本 (v7.6.0) 所需兼容性变更信息。如果从 v7.4.0 或之前版本升级到当前版本，可能也需要考虑和查看中间版本 Release Notes 中提到的兼容性变更信息。

*  TiCDC 支持查询 changefeed 的下游同步状态  [#10289](https://github.com/pingcap/tiflow/issues/10289) @[hongyunyan](https://github.com/hongyunyan) **tw@qiancai** <!--1627-->

    从 v7.6.0 起，TiCDC 引入了一个新的 API，用于查询指定同步任务 (changefeed) 的下游同步状态。通过此 API，你可以判断 TiCDC 是否已将所接收到的上游数据完全同步到下游。

    更多信息，请参考[用户文档](/ticdc/ticdc-open-api-v2.md#查询特定同步任务是否完成)。

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
|  [`tidb_analyze_distsql_scan_concurrency`](/system-variables.md#tidb_analyze_distsql_scan_concurrency-从-v760-版本开始引入)       |    新增       |    用于设置执行 `ANALYZE` 时 `scan` 操作的并发度。   |

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

    - 修复损坏的 SST 文件可能会扩散到其他 TiKV 节点导致 panic 的问题 [#15986](https://github.com/tikv/tikv/issues/15986) @[Connor1996](https://github.com/Connor1996) **tw@Oreoxmt** <!--1631-->
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