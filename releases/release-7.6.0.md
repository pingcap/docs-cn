---
title: TiDB 7.6.0 Release Notes
summary: 了解 TiDB 7.6.0 版本的新功能、兼容性变更、改进提升，以及错误修复。
---

# TiDB 7.6.0 Release Notes

发版日期：2024 年 1 月 x 日

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
    <td rowspan="4">可扩展性与性能</td>
    <td><a href="https://docs.pingcap.com/zh/tidb/v7.6/sql-plan-management#跨数据库绑定执行计划-cross-db-binding">跨数据库绑定执行计划</a> {/* tw@Oreoxmt */}</td>
    <td>在处理上百个 schema 相同的数据库时，针对一个 schema 的 SQL binding 可能需要跨 schema 生效。例如 SaaS 或 PaaS 数据平台为每个用户维护独立数据库，这些数据库有相同的结构，运行类似的 SQL。对每个 schema 逐一做 SQL 绑定有时是不切实际的。TiDB v7.6.0 引入跨数据库绑定执行计划，支持在所有 schema 相同的数据库之间匹配绑定计划。</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/zh/tidb/v7.6/br-snapshot-guide#恢复快照备份数据">BR 快照恢复速度最高提升 10 倍（实验特性）</a> {/* tw@Oreoxmt */}</td>
    <td>BR v7.6.0 实验性地引入了粗粒度打散 Region 算法，用于准备集群的快照恢复。在 TiKV 节点较多的集群中，该算法显著提高了集群资源利用率，更均匀地分配了负载，同时更好地利用了每个节点的网络带宽。在实际案例中，该改进将恢复速度最高提升约 10 倍。</td>
  </tr>
  <tr>
    <td><a href="">建表性能提升 10 倍（实验特性）</a>  {/* tw@hfxsd */}</td>
    <td>在 v7.6.0 中引入了新的 DDL 架构，批量建表的性能提高了 10 倍。这一重大改进极大地缩短了创建大量表所需的时间。特别是在 SaaS 场景中，快速创建大量表（从数万到数十万不等）是一个常见的挑战，使用该特性能显著提升 SaaS 场景的建表速度。</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/zh/tidb/v7.6/tune-region-performance#通过-active-pd-follower-提升-pd-region-信息查询服务的扩展能力">通过 Active PD Follower 提升 PD Region 信息查询服务的扩展能力（实验特性）</a>  {/* tw@ Oreoxmt */}</td>
    <td>TiDB v7.6.0 实验性地引入了 Active PD Follower 特性，允许 PD follower 提供 Region 信息查询服务。在 TiDB 节点数量较多和 Region 数量较多的集群中，该功能提升了 PD 集群处理 GetRegion、ScanRegions 请求的能力，减轻了 PD leader 的 CPU 压力。</td>
  </tr>
  <tr>
    <td rowspan="2">稳定性与高可用</td>
    <td><a href="https://docs.pingcap.com/tidb/v7.6/tiproxy/tiproxy-overview">支持 TiProxy（实验特性）</a>  {/* tw@ran-huang */}</td>
    <td>全面支持 TiProxy，可通过部署工具轻松部署。TiProxy 可以管理和维护客户端与 TiDB 的连接，在滚动重启、升级以及扩缩容过程中保持连接。</td>
  </tr>
  <tr>
    <td><a href="">Data Migration (DM) 正式支持迁移 MySQL 8.0 (GA)</a>  {/* tw@hfxsd */}</td>
    <td>在 v7.6.0 之前，DM 迁移 MySQL 8.0 仅为实验特性，不能用于生产环境。TiDB v7.6.0 增强了该功能的稳定性、兼容性，可在生产环境帮助你平滑、快速地将数据从 MySQL 8.0 迁移到 TiDB。在 v7.6.0 中，该功能正式 GA。</td>
  </tr>
</tbody>
</table>

## 功能详情

### 可扩展性

* 通过 Active PD Follower 提升 PD 上 Region 信息查询服务的扩展能力（实验特性）[#7431](https://github.com/tikv/pd/issues/7431) @[CabinfeverB](https://github.com/CabinfeverB) **tw@Oreoxmt** <!--1667-->

    当集群的 Region 数量较多时，PD leader 处理心跳和调度任务的开销也较大，可能导致 CPU 资源紧张。如果同时集群中的 TiDB 实例数量较多，查询 Region 信息请求并发量较大，PD leader CPU 压力将变得更大，可能会造成 PD 服务不可用。

    为确保服务的高可用性，TiDB v7.6.0 引入了 Active PD Follower 特性提升 PD 上 Region 信息查询服务的扩展能力。你可以通过设置系统变量 [`pd_enable_follower_handle_region`](/system-variables.md#pd_enable_follower_handle_region-从-v760-版本开始引入) 开启 Active PD Follower 特性。启用该特性后，TiDB 在获取 Region 信息时会将请求均匀地发送到所有 PD 节点上，使 PD follower 也可以处理 Region 请求，从而减轻 PD leader 的 CPU 压力。

    更多信息，请参考[用户文档](/tune-region-performance.md#通过-active-pd-follower-提升-pd-region-信息查询服务的扩展能力)。

### 性能

* BR 快照恢复速度最高提升 10 倍（实验特性）[#33937](https://github.com/pingcap/tidb/issues/33937) @[3pointer](https://github.com/3pointer) **tw@Oreoxmt** <!--1647-->

    随着 TiDB 集群规模的不断扩大，故障时快速恢复集群以减少业务中断时间显得尤为重要。在 v7.6.0 之前的版本中，Region 打散算法是性能恢复的主要瓶颈。在 v7.6.0 中，BR 优化了 Region 打散算法，可以迅速将恢复任务拆分为大量小任务，并批量分散到所有 TiKV 节点上。新的并行恢复算法充分利用每个 TiKV 节点的所有资源，实现了并行快速恢复。在实际案例中，大规模 Region 场景下，集群快照恢复速度最高提升约 10 倍。

    目前，新的粗粒度 Region 打散算法为实验特性，你可以配置 `br` 新增的命令行参数 `--granularity="coarse-grained"` 使用新算法，同时通过设置 `--tikv-max-restore-concurrency` 控制每个 TiKV 节点下载任务的并发度。例如：

    ```bash
    br restore full \
    --pd "${PDIP}:2379" \
    --storage "s3://${Bucket}/${Folder}" \
    --s3.region "${region}" \
    --granularity "coarse-grained" \
    --tikv-max-restore-concurrency 128 \
    --send-credentials-to-tikv=true \
    --log-file restorefull.log
    ```

    更多信息，请参考[用户文档](/br/br-snapshot-guide.md#恢复快照备份数据)。

* 默认开启 Titan 引擎 [#16245] (https://github.com/tikv/tikv/issues/16245) @[Connor1996](https://github.com/Connor1996) @[v01dstar](https://github.com/v01dstar) @[tonyxuqqi](https://github.com/tonyxuqqi)

    为了更好地支持 TiDB 宽表写入场景，特别是在支持 JSON 之后，从 TiDB v7.6.0 开始，默认开启 Titan 引擎，自动将超过 32 KB 的大 Value 从 RocksDB 的 LSM Tree 中分离出来，单独存储在 Titan 中，以提升对大 Value 的处理性能。Titan 引擎与 TiKV 所使用的 RocksDB 特性完全兼容。这一变更不仅降低了写入放大效应，在处理大 Value 的写入、更新和点查场景时也表现得更加出色。同时，在 Range Scan 场景下，通过对 Titan 引擎的优化，默认配置下 Titan 引擎的性能测试结果和 RocksDB 基本持平。

    该配置的变更对历史版本兼容，已有的 TiDB 集群在升级到 TiDB v7.6.0 或之后版本时，仍会默认保持关闭 Titan 引擎。你可以根据实际的需求手动开启或者关闭 Titan 引擎。

    更多信息，请参考[用户文档](/storage-engine/titan-overview.md)。

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

* 建表性能提升 10 倍（实验特性）[#49752](https://github.com/pingcap/tidb/issues/49752) @[gmhdbjd](https://github.com/gmhdbjd) **tw@hfxsd** <!--1408-->

    在之前的版本里，将上游数据库上万张表迁移到 TiDB 时，TiDB 创建这些表耗时长，效率低。从 v7.6.0 开始，引入了新的 TiDB DDL V2 架构，你可以通过设置系统变量 [`tidb_ddl_version`](/system-variables.md#tidb_ddl_version-从-v760-版本开始引入) 开启。相比之前的版本，新版本的 DDL 批量建表性能实现了高达 10 倍的提升，大幅减少了建表时间。

    更多信息，请参考[用户文档](/ddl-v2.md)。

* 优化器增强对多值索引的支持 [#47759](https://github.com/pingcap/tidb/issues/47759) [#46539](https://github.com/pingcap/tidb/issues/46539) @[Arenatlx](https://github.com/Arenatlx) @[time-and-fate](https://github.com/time-and-fate) **tw@ran-huang** <!--1405/1584-->

    TiDB 自 v6.6.0 开始引入[多值索引](/sql-statements/sql-statement-create-index.md#多值索引)，提升对 JSON 数据类型的检索性能。在 v7.6.0 中，优化器增强了对多值索引的支持能力，在复杂使用场景下，能够正确识别和利用多值索引来优化查询。

    * 多值索引上的统计信息会被收集，并应用于优化器估算。当一条 SQL 可能选择到数个多值索引时，优化器可以识别开销更小的索引。
    * 当出现用 `OR` 连接的多个 `member of` 条件时，优化器能够为每个 DNF Item（`member of` 条件）匹配一个有效的 Index Partial Path 路径，并将多条路径以 Union 的方式综合起来组成 `Index Merge` 来做更高效的条件过滤和数据读取。

    更多信息，请参考[用户文档](/sql-statements/sql-statement-create-index.md#多值索引)。

* 支持周期性全量数据整理（实验特性）[#12729](https://github.com/tikv/tikv/issues/12729) **tw@Oreoxmt** <!--1610-->

    从 v7.6.0 开始，TiDB 支持 TiKV 周期性全量数据整理。该功能可以作为垃圾回收 (GC) 的增强，用以消除冗余的数据版本。在业务活动呈现明显的高峰和低谷的场景中，利用该功能可在系统空闲时段进行数据整理，以提升高峰期间业务处理的性能。

    你可以通过配置 TiKV 配置项 [`periodic-full-compact-start-times`]((/tikv-configuration-file.md#periodic-full-compact-start-times-从-v760-版本开始引入)) 指定启动周期性全量数据整理的时间，并通过 [`periodic-full-compact-start-max-cpu`](/tikv-configuration-file.md#periodic-full-compact-start-max-cpu-从-v760-版本开始引入) 控制 TiKV 执行周期性全量数据整理时的 CPU 使用率阈值。`periodic-full-compact-start-max-cpu` 默认是 10%，即为了减少对业务流量的影响，只有当 TiKV 的 CPU 利用率低于 10% 时，才会触发周期性全量数据整理。

     更多信息，请参考[用户文档](/tikv-configuration-file.md#periodic-full-compact-start-times-从-v760-版本开始引入)。

### 稳定性

* 跨数据库绑定执行计划 [#48875](https://github.com/pingcap/tidb/issues/48875) @[qw4990](https://github.com/qw4990) **tw@Oreoxmt** <!--1613-->

    在 TiDB 上运行 SaaS 服务时，为了方便数据维护和管理，通常会将每个租户的数据独立存储于不同数据库中，并执行相同的业务逻辑。这导致数百个数据库中存在相同的表和索引定义，执行类似的 SQL 语句。在这种场景下，对一条 SQL 语句的执行计划进行绑定 (SQL Binding) 时，这条绑定通常也适用于其他数据库中的 SQL 语句。

    针对这种应用场景，TiDB v7.6.0 引入跨数据库绑定，可以为模式相同的 SQL 语句绑定相同的执行计划，即使这些 SQL 运行在不同的数据库上。创建跨数据库绑定时，需要将数据库名用通配符 `*` 表示，如下所示。此时，无论 `t1` 和 `t2` 表位于哪个数据库，TiDB 都将尝试使用此绑定来生成执行计划，无需为每个数据库中的 SQL 单独创建绑定。

    ```sql
    CREATE GLOBAL BINDING FOR
    USING
        SELECT /*+ merge_join(t1, t2) */ t1.id, t2.amount FROM *.t1, *.t2 WHERE t1.id = t2.id;
    ```

    此外，跨数据库绑定能有效缓解由于用户数据和负载的不均衡及其快速变化所引发的 SQL 性能问题。通过跨数据库绑定，SaaS 服务商可以固定由拥有大量数据的用户已验证的执行计划，从而固定所有用户的执行计划。对于 SaaS 服务商，该功能提供了显著的便利性和体验提升。

    由于跨数据库绑定会带来系统开销（小于 1%），TiDB 默认将其关闭。要使用跨数据库绑定，首先需要开启 [`tidb_opt_enable_fuzzy_binding`](/system-variables.md#tidb_opt_enable_fuzzy_binding-从-v760-版本开始引入) 系统变量。

    更多信息，请参考[用户文档](/sql-plan-management.md#跨数据库绑定执行计划-cross-db-binding)。

### 高可用

* 支持代理组件 TiProxy（实验特性）[#413](https://github.com/pingcap/tiproxy/issues/413) @[djshow832](https://github.com/djshow832) @[xhebox](https://github.com/xhebox) **tw@ran-huang** <!--1596-->

    TiProxy 是 TiDB 的官方代理组件，位于客户端和 TiDB server 之间，为 TiDB 提供负载均衡、连接保持功能，让 TiDB 集群的负载更加均衡，并在维护操作期间不影响用户对数据库的连接访问。其应用场景如下：

    * 在 TiDB 集群进行滚动重启、滚动升级、缩容等维护操作时，TiDB server 会发生变动，导致客户端与发生变化的 TiDB server 的连接中断。通过使用 TiProxy，可以在这些维护操作过程中平滑地将连接迁移至其他 TiDB server，从而让客户端不受影响。
    * 所有客户端对 TiDB server 的连接都无法动态迁移至其他 TiDB server。当多个 TiDB server 的负载不均衡时，可能出现整体集群资源充足，但某些 TiDB server 资源耗尽导致延迟大幅度增加的情况。为解决此问题，TiProxy 提供连接动态迁移功能，在客户端无感的前提下，将连接从一个 TiDB server 迁移至其他 TiDB server，从而实现 TiDB 集群的负载均衡。

    TiProxy 已集成至 TiUP、TiDB Operator、TiDB Dashboard 等 TiDB 基本组件中，可以方便地进行配置、部署和运维。

    更多信息，请参考[用户文档](/tiproxy/tiproxy-overview.md)。

### SQL 功能

* `LOAD DATA` 支持显式事务和回滚 [#49079](https://github.com/pingcap/tidb/pull/49079) @[ekexium](https://github.com/ekexium) **tw@Oreoxmt** <!--1422-->

   与 MySQL 相比，v7.6.0 之前的 `LOAD DATA` 语句在不同 TiDB 版本中的事务行为存在差异，导致使用该语句时可能需要额外进行调整。具体来说：在 v4.0.0 之前，每导入 20000 行数据就会进行一次提交。从 v4.0.0 到 v6.6.0，TiDB 默认在一个事务中提交所有行，但也支持通过设置 [`tidb_dml_batch_size`](/system-variables.md#tidb_dml_batch_size) 系统变量实现每固定的行数进行一次提交。自 v7.0.0 起，`tidb_dml_batch_size` 对 `LOAD DATA` 语句不再生效，TiDB 将在一个事务中提交所有行。

    从 v7.6.0 开始，`LOAD DATA` 在事务中与其它普通 DML 的处理方式一致，特别是和 MySQL 的事务行为一致。事务内的 `LOAD DATA` 语句本身不再自动提交当前事务，也不会开启新事务，并且事务内的 `LOAD DATA` 语句可以被显式提交或者回滚。此外，`LOAD DATA` 语句会受 TiDB 事务模式设置（乐观/悲观）影响。这些改进简化了数据从 MySQL 到 TiDB 的迁移过程，使得数据导入体验更加统一和可控。

    更多信息，请参考[用户文档](/sql-statements/sql-statement-load-data.md)。

### 数据库管理

* 闪回功能支持精确 TSO [#48372](https://github.com/pingcap/tidb/issues/48372) @[BornChanger](https://github.com/BornChanger/BornChanger) **tw@qiancai** <!--1615-->

    TiDB v7.6.0 提供了更加强大和精确的闪回功能 `FLASHBACK CLUSTER`，不仅支持回溯到过去指定的时间点，还可以通过 `FLASHBACK CLUSTER TO TSO` 精确地指定要恢复的 [TSO](/tso.md) 时间戳，实现更加灵活的数据恢复。例如，与 TiCDC 结合使用时，该功能允许下游 TiDB 集群在暂停数据同步、开启预上线读写测试后，快速且优雅地回溯到暂停同步时的 TSO 时间戳，并继续通过 TiCDC 同步数据，从而简化了预上线验证流程和数据管理。

    ```sql
    FLASHBACK CLUSTER TO TSO 445494839813079041;
    ````

    更多信息，请参考[用户文档](/sql-statements/sql-statement-flashback-cluster.md)。

* 支持自动终止长时间未提交的空闲事务 [#48714](https://github.com/pingcap/tidb/pull/48714) @[crazycs520](https://github.com/crazycs520) **tw@Oreoxmt** <!--1598-->

    在网络异常断开或应用程序故障时，`COMMIT`/`ROLLBACK` 语句可能无法正常传送到数据库。这种情况可能导致数据库锁未能及时释放，进而引起事务锁等待以及数据库连接数快速增加。这类问题在测试环境中较常见，但在线上环境也会偶尔发生，并且有时难以迅速诊断。为有效防止此类问题的发生，TiDB v7.6.0 引入 [`tidb_idle_transaction_timeout`](/system-variables.md#tidb_idle_transaction_timeout-从-v760-版本开始引入) 系统变量，可以自动终止长时间运行的空闲事务。当用户会话处于事务状态且空闲时间超过该变量设定的值时，TiDB 会自动强制结束该事务的数据库连接并回滚事务。

    更多信息，请参考[用户文档](/system-variables.md#tidb_idle_transaction_timeout-从-v760-版本开始引入)。

* 简化执行计划绑定的语法 [#48876](https://github.com/pingcap/tidb/issues/48876) @[qw4990](https://github.com/qw4990) **tw@Oreoxmt** <!--1613-->

    TiDB v7.6.0 简化了创建执行计划绑定的语法。在创建执行计划绑定的命令中无需提供原 SQL 语句，TiDB 可以根据带 hint 的语句识别出对应的原 SQL。这一改进提高了创建执行计划绑定的便利性。例如：

    ```sql
    CREATE GLOBAL BINDING
    USING
    SELECT /*+ merge_join(t1, t2) */ * FROM t1, t2 WHERE t1.id = t2.id;
    ```

    更多信息，请参考[用户文档](/sql-plan-management.md#根据-sql-创建绑定)。

* 支持动态调整 TiDB 单行记录大小限制 [#49237](https://github.com/pingcap/tidb/pull/49237) @[zyguan](https://github.com/zyguan) **tw@Oreoxmt** <!--1452-->

    在 v7.6.0 之前，事务中单行记录的大小受 TiDB 配置项 [`txn-entry-size-limit`](/tidb-configuration-file.md#txn-entry-size-limit-从-v50-版本开始引入) 限制。如果单行记录的大小超出此限制，TiDB 将返回 `entry too large` 错误。此时，用户需要修改 TiDB 配置文件并重启 TiDB 才能够生效。为降低用户的管理成本，TiDB v7.6.0 新增系统变量 [`tidb_txn_entry_size_limit`](/system-variables.md#tidb_txn_entry_size_limit-从-v760-版本开始引入)，支持动态修改 `txn-entry-size-limit` 配置项的值。该变量的默认值为 `0`，表示默认使用 `txn-entry-size-limit` 配置项的值作为限制。当设置为非 `0` 值时，TiDB 优先使用该变量的值作为事务中的单行记录大小的限制。这一改进旨在提高用户调整系统配置的灵活性，无需重启 TiDB 即可生效。

    更多信息，请参考[用户文档](/system-variables.md#tidb_txn_entry_size_limit-从-v760-版本开始引入)。

* BR 默认恢复用户账号等系统表数据 [#48567](https://github.com/pingcap/tidb/issues/48567) @[BornChanger](https://github.com/BornChanger) **tw@Oreoxmt** <!--1570/1628-->

    从 `br` v5.1.0 开始，快照备份时默认自动备份 **mysql schema** 下的系统表数据，但恢复数据时默认不恢复系统表数据。在 v6.2.0 中，`br` 增加恢复参数 `--with-sys-table` 支持恢复数据的同时恢复部分系统表相关数据，提供更多的操作灵活性。

    为了进一步降低用户的管理成本，并提供更直观的默认行为。从 v7.6.0 开始，`br` 默认开启恢复参数 `--with-sys-table`，并支持恢复 `user` 为 `cloud_admin` 的用户数据。这意味着 `br` 默认支持恢复数据的同时恢复部分系统表相关数据，特别是用户账号和表的统计信息数据。这一改进旨在使备份恢复操作更加直观，减轻手动配置的负担，从而提升整体的操作体验。

    更多信息，请参考[用户文档](/br/br-snapshot-guide.md)。

### 可观测性

* 增强资源管控相关的观测性 [#49318](https://github.com/pingcap/tidb/issues/49318) @[glorv](https://github.com/glorv) @[bufferflies](https://github.com/bufferflies) @[nolouch](https://github.com/nolouch) **tw@hfxsd** <!--1668-->

    随着越来越多用户利用资源组对业务应用进行隔离，资源管控提供了更丰富的基于资源组的数据，协助你观测资源组负载、资源组设置，确保出现问题时能够快速发现并精准诊断。其中包括：

    * [慢查询日志](/identify-slow-queries.md) 增加资源组名称、RU 消耗、以及等待资源耗时。
    * [Statement Summary Tables](/statement-summary-tables.md) 增加资源组名称、RU 消耗、以及等待资源耗时。
    * 在变量 [`tidb_last_query_info`](/system-variables.md#tidb_last_query_info-从-v4014-版本开始引入) 中增加了 SQL 的 [RU](/tidb-resource-control.md#什么是-request-unit-ru) 消耗信息 `ru_consumption`，你可以利用此变量获取会话中上一条语句的资源消耗。
    * 增加基于[资源组的数据库指标](/grafana-resource-control-dashboard.md)：QPS/TPS、执行时间 (P999/P99/P95)、失败次数、连接数。
    * 增加系统表 [`request_unit_by_group`](/mysql-schema.md#资源管控相关系统表) 记录资源组每天的历史资源消耗。

    更多信息，请参考[慢查询日志](/identify-slow-queries.md)、[Statement Summary Tables](/statement-summary-tables.md)、[资源管控 (Resource Control) 监控指标详解](/grafana-resource-control-dashboard.md)。

### 数据迁移

* Data Migration (DM) 支持迁移 MySQL 8.0 的功能成为正式功能（GA）[#10405](https://github.com/pingcap/tiflow/issues/10405) @[lyzx2001](https://github.com/lyzx2001) **tw@hfxsd** <!--1617-->

    之前 DM 迁移 MySQL8.0 仅为实验特性，不能用于生产环境。TiDB v7.6.0 增强了该功能的稳定性、兼容性，可在生产环境帮助你平滑、快速地将数据从 MySQL 8.0 迁移到 TiDB。在 v7.6.0 中，该功能正式 GA。

    更多信息，请参考[用户文档](/dm/dm-compatibility-catalog.md)。

* TiCDC 支持通过双向复制模式 (Bi-Directional Replication, BDR) 同步 DDL 语句（实验特性）[#10301](https://github.com/pingcap/tiflow/issues/10301) [#48519](https://github.com/pingcap/tidb/issues/48519) @[okJiang](https://github.com/okJiang) @[asddongmen](https://github.com/asddongmen) **tw@hfxsd** <!--1460/1521/1525-->

    从 v7.6.0 开始，TiCDC 支持在配置了双向复制的情况下同步 DDL 语句。以前，TiCDC 不支持复制 DDL 语句，因此要使用 TiCDC 双向复制必须将 DDL 语句分别应用到两个 TiDB 集群。有了该特性，TiCDC 可以为一个集群分配 `PRIMARY` BDR role，并将该集群的 DDL 语句复制到下游集群。

    更多信息，请参考[用户文档](/ticdc/ticdc-bidirectional-replication.md)。

* TiCDC 支持查询 changefeed 的下游同步状态 [#10289](https://github.com/pingcap/tiflow/issues/10289) @[hongyunyan](https://github.com/hongyunyan) **tw@qiancai** <!--1627-->

    从 v7.6.0 起，TiCDC 引入了一个新的 API `GET /api/v2/changefeed/{changefeed_id}/synced`，用于查询指定同步任务 (changefeed) 的下游同步状态。通过此 API，你可以判断 TiCDC 是否已将所接收到的上游数据完全同步到下游。

    更多信息，请参考[用户文档](/ticdc/ticdc-open-api-v2.md#查询特定同步任务是否完成)。

* TiCDC 增加支持将 CSV 格式中的 delimiter 设置为 3 个字符 [#9969](https://github.com/pingcap/tiflow/issues/9969) @[zhangjinpeng1987](https://github.com/zhangjinpeng1987) **tw@hfxsd** <!--1653-->

    从 v7.6.0 开始，你可以将 TiCDC 输出的 CSV 格式中的 delimiter 设置为 1 到 3 个字符。例如，你可以指定 TiCDC 使用 2 个字符的 delimiter （例如 `||` 或 `$^`）或 3 个字符的 delimiter（例如 `|@|`）分隔字段。

    更多信息，请参考[用户文档](/ticdc/ticdc-csv.md)。

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
| [`tidb_auto_analyze_partition_batch_size`](/system-variables.md#tidb_auto_analyze_partition_batch_size-从-v640-版本开始引入) | 修改 | 经进一步的测试后，该变量默认值从 `1` 修改为 `128`。 |
| [`tidb_sysproc_scan_concurrency`](/system-variables.md#tidb_sysproc_scan_concurrency-从-v650-版本开始引入) | 修改 | 在大规模集群里，`scan` 操作的并发度可以调整的更高，以满足 `ANALYZE` 的需要，因此将该变量最大值由 `256` 修改为 `4294967295`。 |
| [`tidb_analyze_distsql_scan_concurrency`](/system-variables.md#tidb_analyze_distsql_scan_concurrency-从-v760-版本开始引入)       |    新增       |    用于设置执行 `ANALYZE` 时 `scan` 操作的并发度。默认值为 `4`。   |
| [`tidb_ddl_version`](/system-variables.md#tidb_ddl_version-从-v760-版本开始引入)  |  新增  | 用于控制是否开启 [TiDB DDL V2](/ddl-v2.md)。将该变量的值设置为 `2` 可以开启该功能，设置为 `1` 关闭该功能。默认值为 `1`。开启后，将使用新版本的实现执行 DDL 语句。TiDB DDL V2 对 DDL 功能做了提升，建表 DDL 的执行速度相比 V1 版本提升 10 倍。 |
| [`tidb_enable_global_index`](/system-variables.md#tidb_enable_global_index-从-v760-版本开始引入)  |  新增  | 用于控制是否支持对分区表创建 `Global index`。默认值为 `OFF`。`Global index` 当前正处于开发阶段，**不推荐修改该变量值**。 |
| [`tidb_idle_transaction_timeout`](/system-variables.md#tidb_idle_transaction_timeout-从-v760-版本开始引入) | 新增 | 用来控制用户会话中事务的空闲超时。当用户会话处于事务状态且空闲时间超过该变量设定的值时，会话会被 Kill 掉。默认值 `0` 表示没有时间限制。 |
| [`tidb_opt_enable_fuzzy_binding`](/system-variables.md#tidb_opt_enable_fuzzy_binding-从-v760-版本开始引入) | 新增 | 用于控制是否开启跨数据库绑定执行计划功能，默认值 `OFF` 表示默认关闭。 |
| [`tidb_txn_entry_size_limit`](/system-variables.md#tidb_txn_entry_size_limit-从-v760-版本开始引入) | 新增 | 用于动态修改 TiDB 配置项 [`performance.txn-entry-size-limit`](/tidb-configuration-file.md#txn-entry-size-limit-从-v50-版本开始引入)，即限制 TiDB 单行数据的大小。默认值为 `0`，表示默认使用配置项的值。当设置为非 `0` 值时，优先使用该变量的值作为 `txn-entry-size-limit` 的值。 |
| [`pd_enable_follower_handle_region`](/system-variables.md#pd_enable_follower_handle_region-从-v760-版本开始引入) | 新增 | 用于控制是否开启 [Active PD Follower](/tune-region-performance.md#通过-active-pd-follower-提升-pd-region-信息查询服务的扩展能力)（实验特性）。当该值为 `OFF` 时，TiDB 仅从 PD leader 获取 Region 信息。当该值为 `ON` 时，TiDB 在获取 Region 信息时会将请求均匀地发送到所有 PD 节点上，因此 PD follower 也可以处理 Region 信息请求，从而减轻 PD leader 的 CPU 压力。 |

### 配置文件参数

| 配置文件 | 配置项 | 修改类型 | 描述 |
| -------- | -------- | -------- | -------- |
| TiDB | [`tls-version`](tidb-configuration-file.md#tls-version) | 修改 | 默认值为空，TiDB 默认支持的 TLS 版本从 `TLS1.1` 及更高提升为 `TLS1.2` 及更高。 |
| TiKV | [`blob-file-compression`](/tikv-configuration-file.md#blob-file-compression) | 修改 | Titan 中 value 所使用的压缩算法。从 v7.6.0 开始，默认采用 `zstd` 压缩算法。 |
| TiKV | [`rocksdb.titan.enabled`](/tikv-configuration-file.md#enabled) | 修改 | 开启 Titan 开关。v7.5.0 及更早的版本默认值为 `false`。从 v7.6.0 开始，新建集群默认值是 `true`，已有集群升级到 v7.6.0 或更高版本则会维持原有的配置。 |
| TiDB Lightning | [`tidb.pd-addr`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-任务配置) | 修改 | 配置 PD Server 的地址，从 v7.6.0 开始支持设置多个地址。 |
| TiDB Lightning | [`block-size`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-任务配置) | 新增 | 控制物理导入模式 (`backend='local'`) 中本地排序文件的 I/O 块大小。默认值为 `16KiB`。当 IOPS 成为瓶颈时，可以将该参数的值调大。 |

| TiKV | [`raftstore.periodic-full-compact-start-times`](/tikv-configuration-file.md#periodic-full-compact-start-times-从-v760-版本开始引入) | 新增 | 设置 TiKV 启动周期性全量数据整理 (Compaction) 的时间。默认值 `[]` 表示默认情况下禁用周期性全量数据整理。 |
| TiKV | [`raftstore.periodic-full-compact-start-max-cpu`](/tikv-configuration-file.md#periodic-full-compact-start-max-cpu-从-v760-版本开始引入) | 新增 | 设置 TiKV 执行周期性全量数据整理时的 CPU 使用率阈值，默认值为 `0.1`。 |
| TiKV | [`zstd-dict-size`](/tikv-configuration-file.md#zstd-dict-size) | 新增 | 指定 zstd 字典大小，默认值为 `0KB`，表示关闭 `zstd` 字典压缩。 |
| BR | `--granularity` | 新增 | 通过设置 `--granularity="coarse-grained"` 启用粗粒度的 Region 打散算法（实验特性）进行恢复，加快大规模 Region 场景下的 Region 恢复速度。 |
| BR | `--tikv-max-restore-concurrency` | 新增 | 设置启用粗粒度的 Region 打散算法时，单 TiKV 节点的下载任务并发度。 |
| TiCDC | [`encoding-worker-num`](/ticdc/ticdc-changefeed-config.md) | 新增 | 控制 redo 模块中编解码 worker 的数量，默认值为 16。 |
| TiCDC | [`flush-worker-num`](/ticdc/ticdc-changefeed-config.md) | 新增 | 控制 redo 模块中上传文件 worker 的数量，默认值为 8。 |
| TiCDC | [`compression`](/ticdc/ticdc-changefeed-config.md) | 新增 | 设置 redo log 文件的压缩行为。 |
| TiCDC | [`sink.cloud-storage-config`](/ticdc/ticdc-changefeed-config.md) | 新增 | 设置同步数据到对象存储时自动清理历史数据的功能。 |

### 系统表

- 新增系统表 [`INFORMATION_SCHEMA.KEYWORDS`](/information-schema/information-schema-keywords.md) 用来展示 TiDB 支持的所有关键字的信息。**tw@Oreoxmt**
- 在系统表 [`INFORMATION_SCHEMA.SLOW_QUERY`](/information-schema/information-schema-slow-query.md) 中增加了以下资源管控 (Resource Control) 相关的字段：
    - `Resource_group`：语句执行所绑定的资源组。
    - `Request_unit_read`：执行语句消耗的总读 RU。
    - `Request_unit_write`：执行语句消耗的总写 RU。
    - `Time_queued_by_rc`：执行语句过程中等待可用资源的总耗时。

### 其他

## 离线包变更

从 v7.6.0 开始，`TiDB-community-server` [二进制软件包](/binary-package.md)中新增代理组件 [TiProxy](tiproxy/tiproxy-overview.md) 的安装包 `tiproxy-{version}-linux-{arch}.tar.gz`。

## 废弃功能

* [执行计划的自动演进绑定](/sql-plan-management.md#自动演进绑定-baseline-evolution)（实验特性）将从 v8.0.0 开始废弃，等同的功能将会在后续版本中重新设计。
* 系统变量 [`tidb_disable_txn_auto_retry`](/system-variables.md#tidb_disable_txn_auto_retry) 将从 TiDB v8.0.0 开始废弃，废弃后将不再支持乐观事务的自动重试。

## 改进提升

+ TiDB <!--tw@Oreoxmt 12 条-->

    - 当使用非二进制排序规则并且查询条件中包含 `LIKE` 时，优化器可以生成 IndexRangeScan 以提升执行效率 [#48181](https://github.com/pingcap/tidb/issues/48181) [#49138](https://github.com/pingcap/tidb/issues/49138) @[time-and-fate](https://github.com/time-and-fate)
    - (dup): release-6.5.7.md > 改进提升> TiDB - 增强特定情况下 `OUTER JOIN` 转 `INNER JOIN` 的能力 [#49616](https://github.com/pingcap/tidb/issues/49616) @[qw4990](https://github.com/qw4990)
    - 提升分布式执行框架任务在节点重启场景下的均衡性 [#47298](https://github.com/pingcap/tidb/issues/47298) @[ywqzzy](https://github.com/ywqzzy)
    - 允许多个快速加索引 DDL 任务排队执行，而非回退为普通加索引任务 [#47758](https://github.com/pingcap/tidb/issues/47758) @[tangenta](https://github.com/tangenta)
    - 增强 `ALTER TABLE ... ROW_FORMAT` 的兼容性 [#48754](https://github.com/pingcap/tidb/issues/48754) @[hawkingrei](https://github.com/hawkingrei)
    - 将 `CANCEL IMPORT JOB` 命令调整为同步命令 [#48736](https://github.com/pingcap/tidb/issues/48736) @[D3Hunter](https://github.com/D3Hunter)
    - 提升空表加索引的速度 [#49682](https://github.com/pingcap/tidb/issues/49682) @[zimulala](https://github.com/zimulala)
    - 当关联子查询的列未被上层算子引用时，可以直接消除该关联子查询 [#45822](https://github.com/pingcap/tidb/issues/45822) @[King-Dylan](https://github.com/King-Dylan)
    - `EXCHANGE PARTITION` 操作会触发统计信息的维护更新 [#47354](https://github.com/pingcap/tidb/issues/47354) @[hi-rustin](https://github.com/hi-rustin)
    - TiDB 支持构建符合联邦信息处理标准 (FIPS) 要求的二进制文件 [#47948](https://github.com/pingcap/tidb/issues/47948) @[tiancaiamao](https://github.com/tiancaiamao)
    - 改进 TiDB 在处理部分类型转换时的实现，并修复相关问题 [#47945](https://github.com/pingcap/tidb/issues/47945) [#47864](https://github.com/pingcap/tidb/issues/47864) [#47829](https://github.com/pingcap/tidb/issues/47829) [#47816](https://github.com/pingcap/tidb/issues/47816) @[YangKeao](https://github.com/YangKeao) @[lcwangchao](https://github.com/lcwangchao)
    - 在获取 schema 版本时，默认使用 KV timeout 特性读取，减少 meta Region leader 读取慢对 schema 版本更新的影响 [#48125](https://github.com/pingcap/tidb/pull/48125) @[cfzjywxk](https://github.com/cfzjywxk)

+ TiKV <!--tw@ran-huang 4 条-->

    - 增加查询异步任务的 API endpoint `/async_tasks` [#15759](https://github.com/tikv/tikv/issues/15759) @[YuJuncen](https://github.com/YuJuncen)
    - 给 gRPC 监控增加优先级的标签，从而显示资源管理中的各个不同优先级的资源组的数据 [#49318](https://github.com/pingcap/tidb/issues/49318) @[bufferflies](https://github.com/bufferflies)
    - 支持动态调整参数 `readpool.unified.max-tasks-per-worker` 的值，可根据优先级单独核算正在运行的任务数 [#16026](https://github.com/tikv/tikv/issues/16026) @[glorv](https://github.com/glorv)
    - 支持动态调整 GC 的线程数，默认值为 `1` [#16101](https://github.com/tikv/tikv/issues/16101) @[tonyxuqqi](https://github.com/tonyxuqqi)

+ PD <!--tw@ran-huang 1 条-->

    - 提升 PD TSO 在磁盘抖动时的可用性 [#7377](https://github.com/tikv/pd/issues/7377) @[HuSharp](https://github.com/HuSharp)

+ TiFlash <!--tw@ran-huang 4 条-->

    - (dup): release-6.5.7.md > 改进提升> TiFlash - 降低磁盘性能抖动对读取延迟的影响 [#8583](https://github.com/pingcap/tiflash/issues/8583) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 减少后台数据 GC 任务对读、写任务延迟的影响 [#8650](https://github.com/pingcap/tiflash/issues/8650) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 支持在存算分离架构下通过合并相同数据的读取操作，提升多并发下的数据扫描性能 [#6834](https://github.com/pingcap/tiflash/issues/6834) @[JinheLin](https://github.com/JinheLin)
    - 为减少日志打印的开销，TiFlash 配置项 `logger.level` 默认值由 `"debug"` 改为 `"INFO"` [#8563](https://github.com/pingcap/tiflash/issues/8563) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 优化 `JOIN ON` 条件中仅包含 JOIN KEY 等值条件时，半连接 (SEMI JOIN ) 及 LEFT OUTER SEMIJOIN 的执行性能 [#47424](https://github.com/pingcap/tidb/issues/47424) @[gengliqi](https://github.com/gengliqi)

+ Tools

    + Backup & Restore (BR)

        - (dup): release-7.1.3.md > 改进提升> Tools> Backup & Restore (BR) - 新增 PITR 对 delete range 场景的集成测试，提升 PITR 稳定性 [#47738](https://github.com/pingcap/tidb/issues/47738) @[Leavrth](https://github.com/Leavrth)
        - (dup): release-6.5.7.md > 改进提升> Tools> Backup & Restore (BR) - 提升了 `RESTORE` 语句在大数据量表场景下的建表性能 [#48301](https://github.com/pingcap/tidb/issues/48301) @[Leavrth](https://github.com/Leavrth)

    + TiCDC <!--tw@Oreoxmt 3 条-->

        - (dup): release-7.1.3.md > 改进提升> Tools> TiCDC - 通过增加并行，优化了 TiCDC 同步数据到对象存储的性能 [#10098](https://github.com/pingcap/tiflow/issues/10098) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - (dup): release-7.1.3.md > 改进提升> Tools> TiCDC - 支持通过在 `sink-uri` 中设置 `content-compatible=true` 使 TiCDC Canal-JSON [兼容 Canal 官方输出的内容格式](/ticdc/ticdc-canal-json.md#兼容-canal-官方实现) [#10106](https://github.com/pingcap/tiflow/issues/10106) @[3AceShowHand](https://github.com/3AceShowHand)

    + TiDB Data Migration (DM) <!--tw@ran-huang 1 条-->

        - 为 DM OpenAPI 增加了全量物理导入的相关配置 [#10193](https://github.com/pingcap/tiflow/issues/10193) @[GMHDBJD](https://github.com/GMHDBJD)

    + TiDB Lightning <!--tw@hfxsd 2 条-->

        - 支持配置多个 PD 地址以增强稳定性 [#49515](https://github.com/pingcap/tidb/issues/49515) @[mittalrishabh](https://github.com/mittalrishabh)
        - 支持通过配置参数 `block-size` 来控制 TiDB Lightning 内部 I/O 操作大小，提升性能 [#45037](https://github.com/pingcap/tidb/issues/45037) @[mittalrishabh](https://github.com/mittalrishabh)

## 错误修复

+ TiDB

    - (dup): release-6.5.7.md > 错误修复> TiDB - 修复 TiDB panic 并报错 `invalid memory address or nil pointer dereference` 的问题 [#42739](https://github.com/pingcap/tidb/issues/42739) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - (dup): release-7.1.3.md > 错误修复> TiDB - 修复当 DDL `jobID` 恢复为 0 时 TiDB 节点 panic 的问题 [#46296](https://github.com/pingcap/tidb/issues/46296) @[jiyfhust](https://github.com/jiyfhust)
    - (dup): release-6.5.7.md > 错误修复> TiDB - 修复某些情况下相同的查询计划拥有不同的 `PLAN_DIGEST` 的问题 [#47634](https://github.com/pingcap/tidb/issues/47634) @[King-Dylan](https://github.com/King-Dylan)
    - (dup): release-7.1.3.md > 错误修复> TiDB - 修复 `UNION ALL` 第一个子节点是 DUAL Table 时，执行可能报错的问题 [#48755](https://github.com/pingcap/tidb/issues/48755) @[winoros](https://github.com/winoros)
    - (dup): release-6.5.7.md > 错误修复> TiDB - 修复当 `tidb_max_chunk_size` 值较小时，包含 CTE 的查询出现 `runtime error: index out of range [32] with length 32` 错误的问题 [#48808](https://github.com/pingcap/tidb/issues/48808) @[guo-shaoge](https://github.com/guo-shaoge)
    - (dup): release-6.5.6.md > 错误修复> TiDB - 修复使用 `AUTO_ID_CACHE=1` 时 Goroutine 泄漏的问题 [#46324](https://github.com/pingcap/tidb/issues/46324) @[tiancaiamao](https://github.com/tiancaiamao)
    - (dup): release-7.1.3.md > 错误修复> TiDB - 修复 MPP 计算 `COUNT(INT)` 时结果可能出错的问题 [#48643](https://github.com/pingcap/tidb/issues/48643) @[AilinKid](https://github.com/AilinKid)
    - (dup): release-7.1.3.md > 错误修复> TiDB - 修复当分区列类型为 `DATETIME` 时，执行 `ALTER TABLE ... LAST PARTITION` 失败的问题 [#48814](https://github.com/pingcap/tidb/issues/48814) @[crazycs520](https://github.com/crazycs520)
    - (dup): release-6.5.7.md > 错误修复> TiDB - 修复数据中包含后导空格时，在 `LIKE` 中使用 `_` 通配符可能会导致查询结果出错的问题 [#48983](https://github.com/pingcap/tidb/issues/48983) @[time-and-fate](https://github.com/time-and-fate)
    - (dup): release-6.5.7.md > 错误修复> TiDB - 修复 `tidb_server_memory_limit` 导致内存长期压力较高时，TiDB CPU 利用率过高的问题 [#48741](https://github.com/pingcap/tidb/issues/48741) @[XuHuaiyu](https://github.com/XuHuaiyu)
    - (dup): release-7.1.3.md > 错误修复> TiDB - 修复 `ENUM` 类型列作为 join 键时，查询结果错误的问题 [#48991](https://github.com/pingcap/tidb/issues/48991) @[winoros](https://github.com/winoros)
    - (dup): release-6.5.7.md > 错误修复> TiDB - 修复当内存使用超限时包含公共表表达式 (CTE) 的查询非预期卡住的问题 [#49096](https://github.com/pingcap/tidb/issues/49096) @[AilinKid](https://github.com/AilinKid})
    - (dup): release-6.5.7.md > 错误修复> TiDB - 修复 TiDB server 在使用企业插件审计日志时可能占用大量资源的问题 [#49273](https://github.com/pingcap/tidb/issues/49273) @[lcwangchao](https://github.com/lcwangchao)
    - (dup): release-6.5.7.md > 错误修复> TiDB - 修复特定情况下优化器将 TiFlash 选择路径错误转化为 DUAL Table 的问题 [#49285](https://github.com/pingcap/tidb/issues/49285) @[AilinKid](https://github.com/AilinKid)
    - (dup): release-6.5.7.md > 错误修复> TiDB - 修复包含递归 (`WITH RECURSIVE`) CTE 的 `UPDATE` 或 `DELETE` 语句可能会产生错误结果的问题 [#48969](https://github.com/pingcap/tidb/issues/48969) @[winoros](https://github.com/winoros)
    - (dup): release-6.5.7.md > 错误修复> TiDB - 修复包含 IndexHashJoin 算子的查询由于内存超过 `tidb_mem_quota_query` 而卡住的问题 [#49033](https://github.com/pingcap/tidb/issues/49033) @[XuHuaiyu](https://github.com/XuHuaiyu)
    - (dup): release-6.5.7.md > 错误修复> TiDB - 修复在非严格模式下 (`sql_mode = ''`)，`INSERT` 过程中产生截断仍然会报错的问题 [#49369](https://github.com/pingcap/tidb/issues/49369) @[tiancaiamao](https://github.com/tiancaiamao)
    - (dup): release-6.5.7.md > 错误修复> TiDB - 修复 CTE 查询在重试过程中可能会报错 `type assertion for CTEStorageMap failed` 的问题 [#46522](https://github.com/pingcap/tidb/issues/46522) @[tiancaiamao](https://github.com/tiancaiamao)
    - (dup): release-6.5.7.md > 错误修复> TiDB - 修复在嵌套的 `UNION` 查询中 `LIMIT` 和 `OPRDERBY` 可能无效的问题 [#49377](https://github.com/pingcap/tidb/issues/49377) @[AilinKid](https://github.com/AilinKid)
    - (dup): release-6.5.7.md > 错误修复> TiDB - 修复在解析 `ENUM` 或 `SET` 类型的非法值时会导致 SQL 语句报错的问题 [#49487](https://github.com/pingcap/tidb/issues/49487) @[winoros](https://github.com/winoros)
    - (dup): release-6.5.7.md > 错误修复> TiDB - 修复构造统计信息时因为 Golang 隐式转换算法导致统计信息误差过大的问题 [#49801](https://github.com/pingcap/tidb/issues/49801) @[qw4990](https://github.com/qw4990)
    - (dup): release-6.5.7.md > 错误修复> TiDB - 修复在某些时区下夏令时显示有误的问题 [#49586](https://github.com/pingcap/tidb/issues/49586) @[overvenus](https://github.com/overvenus)
    - (dup): release-7.1.3.md > 错误修复> TiDB - 修复在有大量表时，`AUTO_ID_CACHE=1` 的表可能造成 gRPC 客户端泄漏的问题 [#48869](https://github.com/pingcap/tidb/issues/48869) @[tiancaiamao](https://github.com/tiancaiamao)
    - (dup): release-6.5.7.md > 错误修复> TiDB - 修复 TiDB server 在优雅关闭 (graceful shutdown) 时可能 panic 的问题 [#36793](https://github.com/pingcap/tidb/issues/36793) @[bb7133](https://github.com/bb7133)  <!--tw@hfxsd 以下 21 条-->
    - 修复 `ADMIN RECOVER INDEX` 在处理包含 `CommonHandle` 的表时报错 `ERROR 1105` 的问题 [#47687](https://github.com/pingcap/tidb/issues/47687) @[Defined2014](https://github.com/Defined2014)
    - 修复执行 `ALTER TABLE t PARTITION BY` 时指定 Placement Rules 报错 `ERROR 8239` 的问题 [#48630](https://github.com/pingcap/tidb/issues/48630) @[mjonss](https://github.com/mjonss)
    - 修复 `INFORMATION_SCHEMA.CLUSTER_INFO` 中 `START_TIME` 列类型不合理的问题 [#45221](https://github.com/pingcap/tidb/issues/45221) @[dveeden](https://github.com/dveeden)
    - 修复 `INFORMATION_SCHEMA.COLUMNS` 中 `EXTRA` 列类型不合理导致报错 `Data Too Long, field len 30, data len 45` 的问题 [#42030](https://github.com/pingcap/tidb/issues/42030) @[tangenta](https://github.com/tangenta)
    - 修复 `IN (...)` 语句导致 `INFORMATION_SCHEMA.STATEMENTS_SUMMARY` 中的 `PLAN_DIGEST` 不同的问题 [#33559](https://github.com/pingcap/tidb/issues/33559) @[King-Dylan](https://github.com/King-Dylan)
    - 修复 `TIME` 类型转换为 `YEAR` 类型时，返回的结果混合了 `TIME` 和年份的问题 [#48557](https://github.com/pingcap/tidb/issues/48557) @[YangKeao](https://github.com/YangKeao)
    - 修复关闭 `tidb_enable_collect_execution_info` 导致 Coprocessor Cache panic 的问题 [#48212](https://github.com/pingcap/tidb/issues/48212) @[you06](https://github.com/you06)
    - 修复 `shuffleExec` 意外退出导致 TiDB 崩溃的问题 [#48230](https://github.com/pingcap/tidb/issues/48230) @[wshwsh12](https://github.com/wshwsh12)
    - 修复静态 `CALIBRATE RESOURCE` 依赖 Prometheus 数据的问题 [#49174](https://github.com/pingcap/tidb/issues/49174) @[glorv](https://github.com/glorv)
    - 修复在日期中加上数值较大的 Interval 时返回错误结果的问题。修复后，带有无效前缀或字符串 `true` 的 Interval 将被视为零值，与 MySQL 8.0 保持一致 [#49227](https://github.com/pingcap/tidb/issues/49227) @[lcwangchao](https://github.com/lcwangchao)
    - 修复 `ROW` 函数对 `null` 类型推断有误导致意外报错的问题 [#49015](https://github.com/pingcap/tidb/issues/49015) @[wshwsh12](https://github.com/wshwsh12)
    - 修复在某些情况下 `ILIKE` 函数可能导致数据竞争的问题 [#49677](https://github.com/pingcap/tidb/issues/49677) @[lcwangchao](https://github.com/lcwangchao)
    - 修复由于 `STREAM_AGG()` 错误处理 CI 导致查询结果有误的问题 [#49902](https://github.com/pingcap/tidb/issues/49902) @[wshwsh12](https://github.com/wshwsh12)
    - 修复将字节转换为 `TIME` 时出现编码失败的问题 [#47346](https://github.com/pingcap/tidb/issues/47346) @[wshwsh12](https://github.com/wshwsh12)
    - 修复 `CHECK` 约束的 `ENFORCED` 选项的行为与 MySQL 8.0 不一致的问题 [#47567](https://github.com/pingcap/tidb/issues/47567) [#47631](https://github.com/pingcap/tidb/issues/47631) @[jiyfhust](https://github.com/jiyfhust)
    - 修复 `CHECK` 约束的 DDL 卡住的问题 [#47632](https://github.com/pingcap/tidb/issues/47632) @[jiyfhust](https://github.com/jiyfhust)
    - 修复由于内存不足导致 DDL 快速加索引失败的问题 [#47862](https://github.com/pingcap/tidb/issues/47862) @[GMHDBJD](https://github.com/GMHDBJD)
    - 修复在执行加索引的过程中升级集群可能导致数据与索引不一致的问题 [#46306](https://github.com/pingcap/tidb/issues/46306) @[zimulala](https://github.com/zimulala)
    - 修复更新 `tidb_mem_quota_query` 系统变量后执行 `ADMIN CHECK` 报错 `ERROR 8175` 的问题 [#49258](https://github.com/pingcap/tidb/issues/49258) @[tangenta](https://github.com/tangenta)
    - 修复 `ALTER TABLE` 修改外键引用列的类型时，`DECIMAL` 精度发生变化没有报错的问题 [#49836](https://github.com/pingcap/tidb/issues/49836) @[yoshikipom](https://github.com/yoshikipom)
    - 修复 `ALTER TABLE` 修改外键引用列的类型时，`INTEGER` 长度发生变化误报错的问题 [#47702](https://github.com/pingcap/tidb/issues/47702) @[yoshikipom](https://github.com/yoshikipom)
    - 修复某些场景下表达式索引没有发现除数是 0 的问题 [#50053](https://github.com/pingcap/tidb/issues/50053) @[lcwangchao](https://github.com/lcwangchao) <!--tw@qiancai 以下 26 条-->
    - 缓解当要处理的表的数量过多时，TiDB 节点 OOM 的问题 [#50077](https://github.com/pingcap/tidb/issues/50077) @[zimulala](https://github.com/zimulala)
    - 修复集群滚动重启时 DDL 卡在运行中状态的问题 [#50073](https://github.com/pingcap/tidb/issues/50073) @[tangenta](https://github.com/tangenta)
    - 修复使用 `PointGet` 或 `BatchPointGet` 算子访问分区表的全局索引时，结果可能出错的问题 [#47539](https://github.com/pingcap/tidb/issues/47539) @[L-maple](https://github.com/L-maple)
    - 修复当生成列上的索引设置为可见时，可能无法选中 MPP 计划的问题 [#47766](https://github.com/pingcap/tidb/issues/47766) @[AilinKid](https://github.com/AilinKid)
    - 修复 `LIMIT` 可能无法推入到 `OR` 类型的 `Index Merge` 的问题 [#48588](https://github.com/pingcap/tidb/issues/48588) @[AilinKid](https://github.com/AilinKid)
    - 修复 BR 导入后，`mysql.bind_info` 表中可能存在重复的内置 (builtin) 行的问题 [#46527](https://github.com/pingcap/tidb/issues/46527) @[qw4990](https://github.com/qw4990)
    - 修复删除分区后，分区表的统计信息更新行为不合理的问题 [#48182](https://github.com/pingcap/tidb/issues/48182) @[hi-rustin](https://github.com/hi-rustin)
    - 修复并发合并分区表的全局统计信息时可能遇到报错的问题 [#48713](https://github.com/pingcap/tidb/issues/48713) @[hawkingrei](https://github.com/hawkingrei)
    - 修复在具有补齐空格 (PADDING SPACE) 的列上使用 `LIKE` 运算符进行索引范围扫描时，查询结果可能出错的问题 [#48821](https://github.com/pingcap/tidb/issues/48821) @[time-and-fate](https://github.com/time-and-fate)
    - 修复生成列可能触发对内存的并发读写导致数据竞争的问题 [#44919](https://github.com/pingcap/tidb/issues/44919) @[tangenta](https://github.com/tangenta)
    - 修复当指定 `WITH 0 TOPN`（即不收集 TopN 的统计信息）时，`ANALYZE TABLE` 仍然可能收集 Top1 的统计信息的问题 [#49080](https://github.com/pingcap/tidb/issues/49080) @[hawkingrei](https://github.com/hawkingrei)
    - 修复不合法的优化器 hint 可能会导致合法 hint 不生效的问题 [#49308](https://github.com/pingcap/tidb/issues/49308) @[hawkingrei](https://github.com/hawkingrei)
    - 修复对 Hash 类型的分区表进行分区的增删重组或 `TRUNCATE` 操作时，统计信息没有对应更新的问题 [#48235](https://github.com/pingcap/tidb/issues/48235) [#48233](https://github.com/pingcap/tidb/issues/48233) [#48226](https://github.com/pingcap/tidb/issues/48226) [#48231](https://github.com/pingcap/tidb/issues/48231) @[hi-rustin](https://github.com/hi-rustin)
    - 修复设置统计信息自动更新的时间窗口后，时间窗口外统计信息仍然可能更新的问题 [#49552](https://github.com/pingcap/tidb/issues/49552) @[hawkingrei](https://github.com/hawkingrei)
    - 修复从分区表转为非分区表时，旧统计信息不会自动删除的问题 [#49547](https://github.com/pingcap/tidb/issues/49547) @[hi-rustin](https://github.com/hi-rustin)
    - 修复当使用 `TRUNCATE TABLE` 清空非分区表的数据时，旧统计信息不会自动删除的问题 [#49663](https://github.com/pingcap/tidb/issues/49663) @[hi-rustin](https://github.com/hi-rustin)
    - 修复当查询使用了会强制排序的优化器 hint（例如 `STREAM_AGG()`）且其执行计划包含 `IndexMerge` 时，强制排序可能会失效的问题 [#49605](https://github.com/pingcap/tidb/issues/49605) @[AilinKid](https://github.com/AilinKid)
    - 修复直方图的边界包含 `NULL` 时，直方图统计信息可能无法解析成可读字符串的问题 [#49823](https://github.com/pingcap/tidb/issues/49823) @[AilinKid](https://github.com/AilinKid)
    - 修复查询语句包含 `GROUP_CONCANT(ORDER BY)` 语法时，执行可能出错的问题 [#49986](https://github.com/pingcap/tidb/issues/49986) @[AilinKid](https://github.com/AilinKid)
    - 修复当未使用严格的 `SQL_MODE` 时，`UPDATE`、`DELETE`、`INSERT` 语句返回溢出错误而非警告的问题 [#49137](https://github.com/pingcap/tidb/issues/49137) @[YangKeao](https://github.com/YangKeao)
    - 修复当表中存在由多值索引和非 `BINARY` 类型字符串组成的复合索引时，数据无法插入的问题 [#49680](https://github.com/pingcap/tidb/issues/49680) @[YangKeao](https://github.com/YangKeao)
    - 修复多级嵌套的 `UNION` 查询中 `LIMIT` 无效的问题 [#49874](https://github.com/pingcap/tidb/issues/49874) @[Defined2014](https://github.com/Defined2014)
    - 修复当使用 `BETWEEN ... AND ...` 条件查询分区表时结果有误的问题 [#49842](https://github.com/pingcap/tidb/issues/49842) @[Defined2014](https://github.com/Defined2014)
    - 修复无法在 `REPLACE INTO` 语句中使用 hint 的问题 [#34325](https://github.com/pingcap/tidb/issues/34325) @[YangKeao](https://github.com/YangKeao)
    - 修复在查询 Hash 分区表时 TiDB 可能选择错误的分区导致结果有误的问题 [#50044](https://github.com/pingcap/tidb/issues/50044) @[Defined2014](https://github.com/Defined2014)
    - 修复使用 MariaDB Connector/J 并配置启用压缩时发生连接错误的问题 [#49845](https://github.com/pingcap/tidb/issues/49845) @[onlyacat](https://github.com/onlyacat)

+ TiKV <!--tw@Oreoxmt 10 条-->

    - 修复损坏的 SST 文件可能会扩散到其他 TiKV 节点导致 panic 的问题 [#15986](https://github.com/tikv/tikv/issues/15986) @[Connor1996](https://github.com/Connor1996) **tw@Oreoxmt** <!--1631-->
    - (dup): release-7.1.3.md > 错误修复> TiKV - 修复 Online Unsafe Recovery 时无法处理 merge abort 的问题 [#15580](https://github.com/tikv/tikv/issues/15580) @[v01dstar](https://github.com/v01dstar)
    - (dup): release-7.1.3.md > 错误修复> TiKV - 修复扩容时可能导致 DR Auto-Sync 的 joint state 超时问题 [#15817](https://github.com/tikv/tikv/issues/15817) @[Connor1996](https://github.com/Connor1996)
    - (dup): release-7.1.3.md > 错误修复> TiKV - 修复 Titan `blob-run-mode` 无法在线更新的问题 [#15978](https://github.com/tikv/tikv/issues/15978) @[tonyxuqqi](https://github.com/tonyxuqqi)
    - (dup): release-6.5.6.md > 错误修复> TiKV - 修复 resolved-ts 可能被阻塞 2 小时的问题 [#39130](https://github.com/pingcap/tidb/issues/39130) @[overvenus](https://github.com/overvenus)
    - (dup): release-7.1.3.md > 错误修复> TiKV - 修复 Resolved TS 可能被阻塞两小时的问题 [#15520](https://github.com/tikv/tikv/issues/15520) [#39130](https://github.com/pingcap/tidb/issues/39130) @[overvenus](https://github.com/overvenus)
    - (dup): release-6.5.6.md > 错误修复> TiKV - 修复在 Flashback 时遇到 `notLeader` 或 `regionNotFound` 时卡住的问题 [#15712](https://github.com/tikv/tikv/issues/15712) @[HuSharp](https://github.com/HuSharp)
    - (dup): release-7.1.3.md > 错误修复> TiKV - 修复如果 TiKV 运行极慢，在 Region Merge 之后可能 panic 的问题 [#16111](https://github.com/tikv/tikv/issues/16111) @[overvenus](https://github.com/overvenus)
    - 修复 GC 扫描过期 lock 时无法读取内存悲观锁的问题 [#15066](https://github.com/tikv/tikv/issues/15066) @[cfzjywxk](https://github.com/cfzjywxk)
    - 修复 Titan 监控中 blob 文件大小不正确的问题 [#15971](https://github.com/tikv/tikv/issues/15971) @[Connor1996](https://github.com/Connor1996)
    - 修复 TiCDC 同步大表可能导致 TiKV OOM 的问题 [#16035](https://github.com/tikv/tikv/issues/16035) @[overvenus](https://github.com/overvenus)
    - 修复 resolve ts 可能被阻塞 2 小时的问题 [#11847](https://github.com/tikv/tikv/issues/11847) @[overvenus](https://github.com/overvenus)
    - 修复日志备份任务可能出现内存泄露以及备份任务启动后无法正常运行的问题 [#16070](https://github.com/tikv/tikv/issues/16070) @[YuJuncen](https://github.com/YuJuncen)
    - 修复 TiDB 和 TiKV 处理 `DECIMAL` 算术乘法截断时结果不一致的问题 [#16268](https://github.com/tikv/tikv/issues/16268) @[solotzg](https://github.com/solotzg)
    - 修复 `cast_duration_as_time` 可能返回错误结果的问题 [#16211](https://github.com/tikv/tikv/issues/16211) @[gengliqi](https://github.com/gengliqi)
    - 修复巴西和埃及时区转换错误的问题 [#16220](https://github.com/tikv/tikv/issues/16220) @[overvenus](https://github.com/overvenus)
    - 修复 gRPC threads 在检查 `is_shutdown` 时可能出现 panic 的问题 [#16236](https://github.com/tikv/tikv/issues/16236) @[pingyu](https://github.com/pingyu)

    + PD <!--tw@ran-huang 1 条-->

    - 修复 PD 内 etcd 健康检查没有移除过期地址的问题 [#7226](https://github.com/tikv/pd/issues/7226) @[iosmanthus](https://github.com/iosmanthus)
    - (dup): release-7.1.3.md > 错误修复> PD - 修复 PD Leader 切换且新 Leader 与调用方之间存在网络隔离时，调用方不能正常更新 Leader 信息的问题 [#7416](https://github.com/tikv/pd/issues/7416) @[CabinfeverB](https://github.com/CabinfeverB)
    - (dup): release-7.1.3.md > 错误修复> PD - 将 Gin Web Framework 的版本从 v1.8.1 升级到 v1.9.1 以修复部分安全问题 [#7438](https://github.com/tikv/pd/issues/7438) @[niubell](https://github.com/niubell)
    - (dup): release-6.5.7.md > 错误修复> PD - 修复在不满足副本数量需求时，删除 orphan peer 的问题 [#7584](https://github.com/tikv/pd/issues/7584) @[bufferflies](https://github.com/bufferflies)

+ TiFlash <!--tw@ran-huang 11 条-->

    - (dup): release-6.5.7.md > 错误修复> TiFlash - 修复当查询遇到内存限制后发生内存泄漏的问题 [#8447](https://github.com/pingcap/tiflash/issues/8447) @[JinheLin](https://github.com/JinheLin)
    - (dup): release-6.5.7.md > 错误修复> TiFlash - 修复在执行 `FLASHBACK DATABASE` 后 TiFlash 副本的数据仍会被 GC 回收的问题 [#8450](https://github.com/pingcap/tiflash/issues/8450) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - (dup): release-6.5.7.md > 错误修复> TiFlash - 修复慢查询导致内存使用显著增加的问题 [#8564](https://github.com/pingcap/tiflash/issues/8564) @[JinheLin](https://github.com/JinheLin)
    - 修复在 `CREATE TABLE`、`DROP TABLE` 频繁执行的场景下，部分 TiFlash 副本数据无法通过 `RECOVER TABLE` 或 `FLASHBACK TABLE` 恢复的问题 [#1664](https://github.com/pingcap/tiflash/issues/1664) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复在查询带有类似 `ColumnRef in (Literal, Func...)` 的过滤条件时，查询结果出错的问题 [#8631](https://github.com/pingcap/tiflash/issues/8631) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - 修复在 TiDB 执行并发 DDL 遇到冲突时 TiFlash panic 的问题 [#8578](https://github.com/pingcap/tiflash/issues/8578) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复存算分离架构下，可能无法正常选出对象存储数据 GC owner 的问题 [#8519](https://github.com/pingcap/tiflash/issues/8519) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复 lowerUTF8/upperUTF8 不允许大小写字符占据不同字节数的错误 [#8484](https://github.com/pingcap/tiflash/issues/8484) @[gengliqi](https://github.com/gengliqi)
    - 修复 TiFlash 错误处理 enum 偏移量为 0 的问题 [#8311](https://github.com/pingcap/tiflash/issues/8311) @[solotzg](https://github.com/solotzg)
    - 修复表达式 `INET_NTOA()` 中的兼容性问题 [#8211](https://github.com/pingcap/tiflash/issues/8211) @[solotzg](https://github.com/solotzg)
    - 修复在 stream 读时扫描多个分区表可能导致潜在的 OOM 问题 [#8505](https://github.com/pingcap/tiflash/issues/8505) @[gengliqi](https://github.com/gengliqi)
    - 修复成功执行的短查询打印过多的信息日志的问题 [#8592](https://github.com/pingcap/tiflash/issues/8592) @[windtalker](https://github.com/windtalker)
    - 修复 TiFlash 在停止时可能崩溃的问题 [#8550](https://github.com/pingcap/tiflash/issues/8550) @[guo-shaoge](https://github.com/guo-shaoge)
    - 修复 `GREATEST` 或 `LEAST` 函数在包含常量字符串参数时，可能发生的随机无效内存访问的问题 [#8604](https://github.com/pingcap/tiflash/issues/8604) @[windtalker](https://github.com/windtalker)

+ Tools

    + Backup & Restore (BR)

        - (dup): release-7.1.3.md > 错误修复> Tools> Backup & Restore (BR) - 修复生成外部存储文件 URI 错误的问题 [#48452](https://github.com/pingcap/tidb/issues/48452) @[3AceShowHand](https://github.com/3AceShowHand)
        - (dup): release-6.5.7.md > 错误修复> Tools> Backup & Restore (BR) - 修复在任务初始化阶段出现与 PD 的连接错误导致日志备份任务虽然启动但无法正常工作的问题 [#16056](https://github.com/tikv/tikv/issues/16056) @[YuJuncen](https://github.com/YuJuncen)

    + TiCDC

        - (dup): release-7.1.3.md > 错误修复> Tools> TiCDC - 修复某些场景下在同步 `DELETE` 语句时，`WHERE` 条件没有采用主键作为条件的问题 [#9812](https://github.com/pingcap/tiflow/issues/9812) @[asddongmen](https://github.com/asddongmen)
        - (dup): release-7.1.3.md > 错误修复> Tools> TiCDC - 修复同步数据到对象存储时，可能会出现 TiCDC Server panic 的问题 [#10137](https://github.com/pingcap/tiflow/issues/10137) @[sdojjy](https://github.com/sdojjy)
        - (dup): release-6.5.7.md > 错误修复> Tools> TiCDC - 修复 `kv-client` 初始化过程中可能出现数据竞争的问题 [#10095](https://github.com/pingcap/tiflow/issues/10095) @[3AceShowHand](https://github.com/3AceShowHand)
        - (dup): release-7.1.3.md > 错误修复> Tools> TiCDC - 修复在某些特殊场景下，TiCDC 错误地关闭与 TiKV 的连接的问题 [#10239](https://github.com/pingcap/tiflow/issues/10239) @[hicqu](https://github.com/hicqu)
        - (dup): release-6.5.6.md > 错误修复> Tools> TiCDC - 修复上游在执行有损 DDL 时，TiCDC Server 可能 panic 的问题 [#9739](https://github.com/pingcap/tiflow/issues/9739) @[hicqu](https://github.com/hicqu)
        - (dup): release-6.5.7.md > 错误修复> Tools> TiCDC - 修复数据同步到下游 MySQL 时可能出现 `checkpoint-ts` 卡住的问题 [#10334](https://github.com/pingcap/tiflow/issues/10334) @[zhangjinpeng1987](https://github.com/zhangjinpeng1987)

    + TiDB Data Migration (DM) <!--tw@ran-huang 3 条-->

        - 修复 DM 遇到 “event type truncate not valid” 错误导致升级失败的问题 [#10282](https://github.com/pingcap/tiflow/issues/10282) @[GMHDBJD](https://github.com/GMHDBJD)
        - 修复 GTID 模式同步时性能可能会下降的问题 [#9676](https://github.com/pingcap/tiflow/issues/9676) @[feran-morgan-pingcap](https://github.com/feran-morgan-pingcap)
        - 修复下游表结构包含 `shard_row_id_bits` 时同步任务报错的问题 [#10308](https://github.com/pingcap/tiflow/issues/10308) @[GMHDBJD](https://github.com/GMHDBJD)

## 贡献者

感谢来自 TiDB 社区的贡献者们：

- [0o001](https://github.com/0o001)（首次贡献者）
- [bagechengzi](https://github.com/bagechengzi)（首次贡献者）
- [feran-morgan-pingcap](https://github.com/feran-morgan-pingcap)（首次贡献者）
- [highpon](https://github.com/highpon)
- [jiyfhust](https://github.com/jiyfhust)
- [L-maple](https://github.com/L-maple)
- [lkshminarayanan](https://github.com/lkshminarayanan)（首次贡献者）
- [lyang24](https://github.com/lyang24)（首次贡献者）
- [mittalrishabh](https://github.com/mittalrishabh)
- [morgo](https://github.com/morgo)
- [nkg-](https://github.com/nkg-)（首次贡献者）
- [onlyacat](https://github.com/onlyacat)
- [shawn0915](https://github.com/shawn0915)
- [Smityz](https://github.com/Smityz)
- [szpnygo](https://github.com/szpnygo)（首次贡献者）
- [ub-3](https://github.com/ub-3)（首次贡献者）
- [xiaoyawei](https://github.com/xiaoyawei)（首次贡献者）
- [yorkhellen](https://github.com/yorkhellen)
- [yoshikipom](https://github.com/yoshikipom)（首次贡献者）
- [Zheaoli](https://github.com/Zheaoli)
