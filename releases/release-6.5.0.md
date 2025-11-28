---
title: TiDB 6.5.0 Release Notes
summary: 了解 TiDB 6.5.0 版本的新功能、兼容性变更、改进提升，以及错误修复。
---

# TiDB 6.5.0 Release Notes

发版日期：2022 年 12 月 29 日

TiDB 版本：6.5.0

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v6.5/quick-start-with-tidb) | [生产部署](https://docs.pingcap.com/zh/tidb/v6.5/production-deployment-using-tiup)

TiDB 6.5.0 为长期支持版本 (Long-Term Support Release, LTS)。

与 TiDB [6.4.0-DMR](/releases/release-6.4.0.md) 相比，TiDB 6.5.0 引入了以下关键特性：

> **Tip:**
>
> 与前一个 LTS（即 6.1.0 版本）相比，TiDB 6.5.0 还引入了 [6.2.0-DMR](/releases/release-6.2.0.md)、[6.3.0-DMR](/releases/release-6.3.0.md)、[6.4.0-DMR](/releases/release-6.4.0.md) 中已发布的新功能、提升改进和错误修复。
>
> - 要了解 6.1.0 LTS 和 6.5.0 LTS 之间的完整变更，除了参阅当前页面的 release notes，还需参阅 [6.2.0-DMR release notes](/releases/release-6.2.0.md)、[6.3.0-DMR release notes](/releases/release-6.3.0.md)、[6.4.0-DMR release notes](/releases/release-6.4.0.md)。
> - 要快速对比 6.1.0 LTS 和 6.5.0 LTS 的关键特性，可以查看 [TiDB 功能概览](/basic-features.md)中的 `v6.1` 和 `v6.5` 列。

- [添加索引加速](/system-variables.md#tidb_ddl_enable_fast_reorg-从-v630-版本开始引入)特性 GA，添加索引的性能约提升为 v6.1.0 的 10 倍。
- TiDB 全局内存控制特性 GA，通过 [`tidb_server_memory_limit`](/system-variables.md#tidb_server_memory_limit-从-v640-版本开始引入) 即可管理全局内存阈值。
- 支持高性能、全局单调递增的 [`AUTO_INCREMENT` 列属性](/auto-increment.md#兼容-mysql-的自增列模式) GA，兼容 MySQL。
- [`FLASHBACK CLUSTER TO TIMESTAMP`](/sql-statements/sql-statement-flashback-cluster.md) 特性新增对 TiCDC 和 PITR 的兼容性支持，该特性已 GA。
- 优化器引入的更精准的代价模型 [Cost Model Version 2](/cost-model.md#cost-model-version-2) GA，同时优化器增强索引合并 [INDEX MERGE](/glossary.md#index-merge) 功能对 `AND` 连接的表达式的支持。
- 支持下推 `JSON_EXTRACT()` 函数至 TiFlash。
- 支持[密码管理](/password-management.md)策略，满足密码合规审计需求。
- TiDB Lightning 和 Dumpling 支持[导入](/tidb-lightning/tidb-lightning-data-source.md)和[导出](/dumpling-overview.md#通过并发提高-dumpling-的导出效率)压缩格式文件。
- TiDB Data Migration (DM) 的[增量数据校验](/dm/dm-continuous-data-validation.md)特性 GA。
- TiDB 快照备份支持断点续传，此外 [PITR](/br/br-pitr-guide.md#进行-pitr) 的恢复性能提升了 50%，通用场景下 RPO 降低到 5 分钟。
- TiCDC [同步数据到 Kafka](/replicate-data-to-kafka.md)，吞吐从 4000 行每秒提升到 35000 行每秒，复制延迟降低到 2 秒。
- 提供行级别 [Time to live (TTL)](/time-to-live.md) 管理数据生命周期（实验特性）。
- TiCDC 支持 Amazon S3、Azure Blob Storage、NFS 的[对象存储](/ticdc/ticdc-sink-to-cloud-storage.md)（实验特性）。

## 新功能

### SQL

* TiDB 添加索引的性能约提升为原来的 10 倍 (GA) [#35983](https://github.com/pingcap/tidb/issues/35983) @[benjamin2037](https://github.com/benjamin2037) @[tangenta](https://github.com/tangenta)

    TiDB v6.3.0 引入了[添加索引加速](/system-variables.md#tidb_ddl_enable_fast_reorg-从-v630-版本开始引入)作为实验特性，提升了添加索引回填过程的速度。该功能在 v6.5.0 正式 GA 并默认打开，预期大表添加索引的性能约提升为 v6.1.0 的 10 倍。添加索引加速适用于单条 SQL 语句串行添加索引的场景，在多条 SQL 并行添加索引时仅对其中一条添加索引的 SQL 语句生效。

* 提供轻量级元数据锁，提升 DDL 变更过程 DML 的成功率 (GA) [#37275](https://github.com/pingcap/tidb/issues/37275) @[wjhuang2016](https://github.com/wjhuang2016)

    TiDB v6.3.0 引入了[元数据锁](/metadata-lock.md)作为实验特性，通过协调表元数据变更过程中 DML 语句和 DDL 语句的优先级，让执行中的 DDL 语句等待持有旧版本元数据的 DML 语句提交，尽可能避免 DML 语句的 `Information schema is changed` 错误。该功能在 v6.5.0 正式 GA 并默认打开，适用于各类 DDL 变更场景。当集群从 v6.5.0 之前的版本升级到 v6.5.0 及之后的版本时，TiDB 默认自动开启该功能。如果需要关闭该功能，你可以将系统变量 [`tidb_enable_metadata_lock`](/system-variables.md#tidb_enable_metadata_lock-从-v630-版本开始引入) 设置为 `OFF`。

    更多信息，请参考[用户文档](/metadata-lock.md)。

* 支持通过 `FLASHBACK CLUSTER TO TIMESTAMP` 命令将集群快速回退到特定的时间点 (GA) [#37197](https://github.com/pingcap/tidb/issues/37197) [#13303](https://github.com/tikv/tikv/issues/13303) @[Defined2014](https://github.com/Defined2014) @[bb7133](https://github.com/bb7133) @[JmPotato](https://github.com/JmPotato) @[Connor1996](https://github.com/Connor1996) @[HuSharp](https://github.com/HuSharp) @[CalvinNeo](https://github.com/CalvinNeo)

    TiDB v6.4.0 引入了 [`FLASHBACK CLUSTER TO TIMESTAMP`](/sql-statements/sql-statement-flashback-cluster.md) 语句作为实验特性，支持在 Garbage Collection (GC) life time 内快速回退整个集群到指定的时间点。该功能在 v6.5.0 新增对 TiCDC 和 PITR 的兼容性支持并正式 GA，适用于快速撤消 DML 误操作、支持集群分钟级别的快速回退、支持在时间线上多次回退以确定特定数据更改发生的时间。

    更多信息，请参考[用户文档](/sql-statements/sql-statement-flashback-cluster.md)。

* 完整支持包含 `INSERT`、`REPLACE`、`UPDATE` 和 `DELETE` 的非事务 DML 语句 [#33485](https://github.com/pingcap/tidb/issues/33485) @[ekexium](https://github.com/ekexium)

    在大批量的数据处理场景，单一大事务 SQL 处理可能对集群稳定性和性能造成影响。非事务 DML 语句将一个 DML 语句拆成多个 SQL 语句在内部执行。拆分后的语句将牺牲事务原子性和隔离性，但是对于集群的稳定性有很大提升。TiDB 从 v6.1.0 开始支持非事务 `DELETE` 语句，v6.5.0 新增对非事务 `INSERT`、`REPLACE` 和 `UPDATE` 语句的支持。

    更多信息，请参考[非事务 DML 语句](/non-transactional-dml.md) 和 [`BATCH` 语句](/sql-statements/sql-statement-batch.md)。

* 支持 Time to live (TTL)（实验特性）[#39262](https://github.com/pingcap/tidb/issues/39262) @[lcwangchao](https://github.com/lcwangchao)

    TTL 提供了行级别的生命周期控制策略。在 TiDB 中，设置了 TTL 属性的表会根据配置自动检查并删除过期的行数据。TTL 设计的目标是在不影响在线读写负载的前提下，帮助用户周期性且及时地清理不需要的数据。

    更多信息，请参考[用户文档](/time-to-live.md)。

* 支持通过 `INSERT INTO SELECT` 语句保存 TiFlash 查询结果（实验特性）[#37515](https://github.com/pingcap/tidb/issues/37515) @[gengliqi](https://github.com/gengliqi)

    从 v6.5.0 起，TiDB 支持下推 `INSERT INTO SELECT` 语句中的 `SELECT` 子句（分析查询）到 TiFlash，你可以将 TiFlash 的查询结果方便地保存到 `INSERT INTO` 指定的 TiDB 表中供后续分析使用，起到了结果缓存（即结果物化）的效果。例如：

    ```sql
    INSERT INTO t2 SELECT Mod(x,y) FROM t1;
    ```

    在实验特性阶段，该功能默认关闭。要开启此功能，请设置系统变量 [`tidb_enable_tiflash_read_for_write_stmt`](/system-variables.md#tidb_enable_tiflash_read_for_write_stmt-从-v630-版本开始引入) 为 `ON`。使用该特性时，`INSERT INTO` 指定的结果表没有特殊限制，你可以自由选择是否为该表添加 TiFlash 副本。该特性典型的使用场景包括：

    - 使用 TiFlash 做复杂分析
    - 需重复使用 TiFlash 查询结果或响应高并发的在线请求
    - 与查询的输入数据相比，所需的结果集比较小，推荐 100 MiB 以内

  更多信息，请参考[用户文档](/tiflash/tiflash-results-materialization.md)。

* 支持绑定历史执行计划（实验特性）[#39199](https://github.com/pingcap/tidb/issues/39199) @[fzzf678](https://github.com/fzzf678)

    受 SQL 语句执行时各种因素的影响，之前最优的执行计划偶尔会被新的执行计划替代，进而影响 SQL 性能。在这种场景下，最优的执行计划可能仍旧在 SQL 执行历史中，还没有被清除。

    在 v6.5.0 中，TiDB 扩展了 [`CREATE [GLOBAL | SESSION] BINDING`](/sql-statements/sql-statement-create-binding.md) 语句中的绑定对象，支持根据历史执行计划创建绑定。当 SQL 语句的执行计划发生改变时，只要原来的执行计划仍然在 SQL 执行历史内存表（例如，`statements_summary`）中，就可以在 `CREATE [GLOBAL | SESSION] BINDING` 语句中通过指定 `plan_digest` 绑定原来的执行计划，快速恢复 SQL 性能。此方式可以简化执行计划突变问题的处理，提升运维效率。

    更多信息，请参考[用户文档](/sql-plan-management.md#根据历史执行计划创建绑定)。

### 安全

* 支持密码复杂度策略 [#38928](https://github.com/pingcap/tidb/issues/38928) @[CbcWestwolf](https://github.com/CbcWestwolf)

    TiDB 启用密码复杂度策略功能后，在用户设置密码时，TiDB 会检查密码长度、大写和小写字符个数、数字字符个数、特殊字符个数、密码字典匹配、是否与用户名相同等，以此确保用户设置了安全的密码。

    TiDB 支持密码强度检查函数 `VALIDATE_PASSWORD_STRENGTH()`，用于判定一个给定密码的强度。

    更多信息，请参考[用户文档](/password-management.md#密码复杂度策略)。

* 支持密码过期策略 [#38936](https://github.com/pingcap/tidb/issues/38936) @[CbcWestwolf](https://github.com/CbcWestwolf)

    TiDB 支持密码过期策略，包括手动密码过期、全局级别自动密码过期、账户级别自动密码过期。启用密码过期策略功能后，用户必须定期修改密码，防止密码长期使用带来的泄露风险，提高密码安全性。

    更多信息，请参考[用户文档](/password-management.md#密码过期策略)。

* 支持密码重用策略 [#38937](https://github.com/pingcap/tidb/issues/38937) @[keeplearning20221](https://github.com/keeplearning20221)

    TiDB 支持密码重用策略，包括全局级别密码重用策略、账户级别密码重用策略。启用密码重用策略功能后，用户不能使用最近一段时间使用过的密码或最近几次使用过的密码，以此降低密码的重复使用带来的泄漏风险，提高密码安全性。

    更多信息，请参考[用户文档](/password-management.md#密码重用策略)。

* 支持密码连续错误限制登录策略 [#38938](https://github.com/pingcap/tidb/issues/38938) @[lastincisor](https://github.com/lastincisor)

    TiDB 启用密码连续错误限制登录策略功能后，当用户登录时，如果连续多次密码错误，账户将被临时锁定，达到锁定时间后将自动解锁。

    更多信息，请参考[用户文档](/password-management.md#密码连续错误限制登录策略)。

### 可观测性

* TiDB Dashboard 在 Kubernetes 环境支持独立 Pod 部署 [#1447](https://github.com/pingcap/tidb-dashboard/issues/1447) @[SabaPing](https://github.com/SabaPing)

    TiDB v6.5.0 且 TiDB Operator v1.4.0 之后，在 Kubernetes 上支持将 TiDB Dashboard 作为独立的 Pod 部署。在 TiDB Operator 环境，可直接访问该 Pod 的 IP 来打开 TiDB Dashboard。

    独立部署 TiDB Dashboard，可以获得以下收益：

    - TiDB Dashboard 的计算将不会再对 PD 节点有压力，可以更好的保障集群运行。
    - 如果 PD 节点因异常不可访问，也还可以继续使用 TiDB Dashboard 进行集群诊断。
    - 在开放 TiDB Dashboard 到外网时，不用担心 PD 中的特权端口的权限问题，降低集群的安全风险。

  更多信息，请参考 [TiDB Operator 部署独立的 TiDB Dashboard](https://docs.pingcap.com/zh/tidb-in-kubernetes/v1.5/get-started#部署独立的-tidb-dashboard)。

* Performance Overview 面板中新增 TiFlash 和 CDC (Change Data Capture) 面板 [#39230](https://github.com/pingcap/tidb/issues/39230) @[dbsid](https://github.com/dbsid)

    TiDB 从 v6.1.0 起在 Grafana 中引入了 Performance Overview 面板，为 TiDB、TiKV、PD 提供了系统级别的总体性能诊断入口。在 v6.5.0 中，Performance Overview 面板中新增了 TiFlash 和 CDC 面板。通过此次新增，从 v6.5.0 起，使用单个 Performance Overview 面板即可分析 TiDB 集群中所有组件的性能。

    TiFlash 和 CDC 面板重新编排了 TiFlash 和 TiCDC 相关的监控信息，可以帮助你大幅提高 TiFlash 和 TiCDC 的性能分析和故障诊断效率：

    - 通过 [TiFlash 面板](/grafana-performance-overview-dashboard.md#tiflash)，你可以直观地了解 TiFlash 集群的请求类型、延迟分析和资源使用概览。
    - 通过 [CDC 面板](/grafana-performance-overview-dashboard.md#cdc)，你可以直观地了解 TiCDC 集群的健康状况、同步延迟、数据流和下游写入延迟等信息。

  更多信息，请参考[用户文档](/performance-tuning-methods.md)。

### 性能

* 索引合并 [INDEX MERGE](/glossary.md#index-merge) 功能支持 `AND` 连接的表达式 [#39333](https://github.com/pingcap/tidb/issues/39333) @[guo-shaoge](https://github.com/guo-shaoge) @[time-and-fate](https://github.com/time-and-fate) @[hailanwhu](https://github.com/hailanwhu)

    在 v6.5.0 前，TiDB 只支持对 `OR` 连接词的过滤条件使用索引合并特性。自 v6.5.0 起，TiDB 支持对于在 `WHERE` 子句中使用 `AND` 连接的过滤条件使用索引合并特性。TiDB 的索引合并至此可以覆盖更多普遍的查询过滤条件组合，不再限定于并集 (`OR`) 关系。v6.5.0 仅支持优化器自动选择 `OR` 条件下的索引合并。要开启对于 `AND` 连接的索引合并，你需要使用 [`USE_INDEX_MERGE`](/optimizer-hints.md#use_index_merget1_name-idx1_name--idx2_name-) Hint。

    关于索引合并功能的更多信息，请参阅 [v5.4.0 Release Notes](/releases/release-5.4.0.md#性能)，以及优化器相关的[用户文档](/explain-index-merge.md)。

* 新增支持下推以下 JSON 函数至 TiFlash [#39458](https://github.com/pingcap/tidb/issues/39458) @[yibin87](https://github.com/yibin87)

    * `->`
    * `->>`
    * `JSON_EXTRACT()`

  JSON 格式为应用设计提供了灵活的建模方式，目前越来越多的应用采用 JSON 格式进行数据交换和数据存储。通过将 JSON 函数下推至 TiFlash，你可以提高 JSON 类型数据的分析效率，拓展 TiDB 实时分析的应用场景。

* 新增支持下推以下字符串函数至 TiFlash [#6115](https://github.com/pingcap/tiflash/issues/6115) @[xzhangxian1008](https://github.com/xzhangxian1008)

    * `regexp_like`
    * `regexp_instr`
    * `regexp_substr`

* 新增全局 Hint 干预[视图](/views.md)内查询计划的生成 [#37887](https://github.com/pingcap/tidb/issues/37887) @[Reminiscent](https://github.com/Reminiscent)

    部分视图访问的场景需要用 Hint 对视图内查询的执行计划进行干预，以获得最佳性能。在 v6.5.0 中，TiDB 允许针对视图内的查询块添加全局 Hint，使查询中定义的 Hint 能够在视图内部生效。该特性为包含复杂视图嵌套的 SQL 提供 Hint 的注入手段，增强了执行计划控制能力，进而稳定复杂 SQL 的执行性能。全局 Hint 通过[查询块命名](/optimizer-hints.md#第-1-步使用-qb_name-hint-重命名视图内的查询块)和 [Hint 引用](/optimizer-hints.md#第-2-步添加实际需要的-hint)来开启。

    更多信息，请参考[用户文档](/optimizer-hints.md#全局生效的-hint)。

* 支持将[分区表](/partitioned-table.md)的排序操作下推至 TiKV [#26166](https://github.com/pingcap/tidb/issues/26166) @[winoros](https://github.com/winoros)

    [分区表](/partitioned-table.md)特性在 v6.1.0 正式 GA 后，TiDB 仍然在持续提升分区表相关的性能。在 v6.5.0 中，TiDB 支持将 `ORDER BY` 和 `LIMIT` 等排序操作下推至 TiKV 进行计算和过滤，降低网络 I/O 的开销，提升了使用分区表时 SQL 的性能。

* 优化器引入更精准的代价模型 Cost Model Version 2 (GA) [#35240](https://github.com/pingcap/tidb/issues/35240) @[qw4990](https://github.com/qw4990)

    TiDB v6.2.0 引入了代价模型 [Cost Model Version 2](/cost-model.md#cost-model-version-2) 作为实验特性，通过更准确的代价估算方式，有利于最优执行计划的选择。尤其在部署了 TiFlash 的情况下，Cost Model Version 2 自动选择合理的存储引擎，避免过多的人工介入。经过一段时间真实场景的测试，这个模型在 v6.5.0 正式 GA。新创建的集群将默认使用 Cost Model Version 2。对于升级到 v6.5.0 的集群，由于 Cost Model Version 2 可能会改变原有的执行计划，在经过充分的性能测试之后，你可以通过设置变量 [`tidb_cost_model_version = 2`](/system-variables.md#tidb_cost_model_version-从-v620-版本开始引入) 使用新的代价模型。

    Cost Model Version 2 成为正式功能大幅提升了 TiDB 优化器的整体能力，并使 TiDB 切实地向更加强大的 HTAP 数据库演进。

    更多信息，请参考[用户文档](/cost-model.md#cost-model-version-2)。

* TiFlash 对获取表行数的操作进行优化 [#37165](https://github.com/pingcap/tidb/issues/37165) @[elsa0520](https://github.com/elsa0520)

    在数据分析的场景中，通过无过滤条件的 `COUNT(*)` 获取表的实际行数是一个常见操作。TiFlash 在 v6.5.0 中优化了 `COUNT(*)` 的改写，自动选择带有“非空”属性且列定义最短的列进行计数，这样可以有效降低 TiFlash 上发生的 I/O 数量，进而提升获取表行数的执行效率。

### 稳定性

* TiDB 全局内存控制成为正式功能 (GA) [#37816](https://github.com/pingcap/tidb/issues/37816) @[wshwsh12](https://github.com/wshwsh12)

    TiDB v6.4.0 引入了全局内存控制作为实验特性。自 v6.5.0 起，全局内存控制成为正式功能，能够跟踪到 TiDB 中主要的内存消耗。当全局内存消耗达到 [`tidb_server_memory_limit`](/system-variables.md#tidb_server_memory_limit-从-v640-版本开始引入) 所定义的阈值时，TiDB 会尝试 GC 或取消 SQL 操作等方法限制内存使用，保证 TiDB 的稳定性。

    需要注意的是，会话中事务所消耗的内存（由配置项 [`txn-total-size-limit`](/tidb-configuration-file.md#txn-total-size-limit) 设置最大值）如今被内存管理模块跟踪：当单个会话的内存消耗达到系统变量 [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query) 所定义的阀值时，将会触发系统变量 [`tidb_mem_oom_action`](/system-variables.md#tidb_mem_oom_action-从-v610-版本开始引入) 所定义的行为（默认为 `CANCEL`，即取消操作）。为了保证向前兼容，当配置 [`txn-total-size-limit`](/tidb-configuration-file.md#txn-total-size-limit) 为非默认值时，TiDB 仍旧会保证事务可以使用到 `txn-total-size-limit` 所设定的内存量而不被取消。

    在使用 v6.5.0 及以上版本时，建议移除配置项 [`txn-total-size-limit`](/tidb-configuration-file.md#txn-total-size-limit)，取消对事务内存做单独的限制，转而使用系统变量 [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query) 和 [`tidb_server_memory_limit`](/system-variables.md#tidb_server_memory_limit-从-v640-版本开始引入) 对全局内存进行管理，从而提高内存的使用效率。

    更多信息，请参考[用户文档](/configure-memory-usage.md)。

### 易用性

* 完善 `EXPLAIN ANALYZE` 输出结果中 TiFlash 的 TableFullScan 算子的执行信息 [#5926](https://github.com/pingcap/tiflash/issues/5926) @[hongyunyan](https://github.com/hongyunyan)

    `EXPLAIN ANALYZE` 语句可以输出执行计划及运行时的统计信息。在 v6.5.0 中，TiFlash 对 TableFullScan 算子的执行信息进行了完善，补充了 DMFile 相关的执行信息。你可以更加直观地查看 TiFlash 的数据扫描状态信息，方便进行性能分析。

    更多信息，请参考[用户文档](/sql-statements/sql-statement-explain-analyze.md)。

* 支持将执行计划打印为 JSON 格式 [#39261](https://github.com/pingcap/tidb/issues/39261) @[fzzf678](https://github.com/fzzf678)

    在 v6.5.0 中，TiDB 扩展了执行计划的打印格式。通过在 `EXPLAIN` 语句中指定 `FORMAT = "tidb_json"` 能够将 SQL 的执行计划以 JSON 格式输出。借助这个能力，SQL 调试工具和诊断工具能够更方便准确地解读执行计划，进而提升 SQL 诊断调优的易用性。

    更多信息，请参考[用户文档](/sql-statements/sql-statement-explain.md)。

### MySQL 兼容性

* 支持高性能、全局单调递增的 `AUTO_INCREMENT` 列属性 (GA) [#38442](https://github.com/pingcap/tidb/issues/38442) @[tiancaiamao](https://github.com/tiancaiamao)

    TiDB v6.4.0 引入了 `AUTO_INCREMENT` 的兼容 MySQL 的自增列模式作为实验特性，通过中心化分配自增 ID，实现了自增 ID 在所有 TiDB 实例上单调递增。使用该特性能够更容易地实现查询结果按自增 ID 排序。该功能在 v6.5.0 正式 GA。使用该功能的单表写入 TPS 预期超过 2 万，并支持通过弹性扩容提升单表和整个集群的写入吞吐。要使用兼容 MySQL 的自增列模式，你需要在建表时将 `AUTO_ID_CACHE` 设置为 `1`。

    ```sql
    CREATE TABLE t(a int AUTO_INCREMENT key) AUTO_ID_CACHE 1;
    ```

    更多信息，请参考[用户文档](/auto-increment.md#兼容-mysql-的自增列模式)。

### 数据迁移

* 支持导出和导入 gzip、snappy、zstd 三种压缩格式的 SQL、CSV 文件 [#38514](https://github.com/pingcap/tidb/issues/38514) @[lichunzhu](https://github.com/lichunzhu)

    Dumpling 支持将数据导出为 gzip、snappy、zstd 三种压缩格式的 SQL、CSV 的压缩文件。TiDB Lightning 也支持导入这些格式的压缩文件。

    有这个功能之前，导出数据或者导入数据都需要较大的存储空间，用于存储已经导出或即将导入的 CSV 和 SQL 文件，需要较高的存储成本。该功能发布后，通过压缩数据文件，可以大幅降低存储成本。

    更多信息，请参考[用户文档](/dumpling-overview.md#通过并发提高-dumpling-的导出效率)。

* 优化了 binlog 解析能力 [#924](https://github.com/pingcap/dm/issues/924) @[gmhdbjd](https://github.com/GMHDBJD)

    该功能允许过滤掉不在迁移任务里的库和表对象的 binlog event，不做解析，从而提升解析效率和稳定性。该策略在 v6.5.0 版本默认生效，无需额外操作。

    有这个功能之前，即使仅迁移几张表，也需要解析上游整个 binlog 文件，即仍要解析该 binlog 文件中不需要迁移的表的 binlog event，效率较低。同时，如果不在迁移任务里的库表的 binlog event 不支持解析，还会导致任务失败。推出该功能后，通过只解析在迁移任务里的库表对象的 binlog event，可以大大提升 binlog 解析效率，提升任务稳定性。

* Disk quota 功能 GA [#446](https://github.com/pingcap/tidb-lightning/issues/446) @[buchuitoudegou](https://github.com/buchuitoudegou)

    你可以为 TiDB Lightning 配置磁盘配额 (disk quota)。当磁盘配额不足时，TiDB Lightning 会暂停读取源数据以及写入临时文件，而是优先将已经完成排序的 key-value 写入 TiKV。TiDB Lightning 删除本地临时文件后，再继续导入过程。

    有这个功能之前，TiDB Lightning 在使用物理模式导入数据时，会在本地磁盘创建大量的临时文件，用来对原始数据进行编码、排序、分割。当用户本地磁盘空间不足时，TiDB Lightning 会由于写入文件失败而报错退出。推出该功能后，可避免 TiDB Lightning 任务写满本地磁盘。

    更多信息，请参考[用户文档](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#磁盘资源配额-从-v620-版本开始引入)。

* DM 增量数据校验的功能 GA [#4426](https://github.com/pingcap/tiflow/issues/4426) @[D3Hunter](https://github.com/D3Hunter)

    在将增量数据从上游迁移到下游数据库的过程中，数据的流转有小概率导致错误或者丢失的情况。对于需要依赖强数据一致的场景，如信贷、证券等业务，你可以在数据迁移完成之后再对数据进行全量校验，确保数据的一致性。然而，在某些增量复制的业务场景下，上游和下游的写入是持续的、不会中断的。由于上下游的数据在不断变化，导致用户难以对表里的全部数据进行一致性校验。

    过去，需要中断业务才能进行全量数据校验，会影响业务。推出该功能后，你无需中断业务即可实现增量数据校验。

    更多信息，请参考[用户文档](/dm/dm-continuous-data-validation.md)。

### 数据共享与订阅

* TiCDC 支持输出变更数据至 storage sink（实验特性）[#6797](https://github.com/pingcap/tiflow/issues/6797) @[zhaoxinyu](https://github.com/zhaoxinyu)

    TiCDC 支持将 changed log 输出到 Amazon S3、Azure Blob Storage、NFS，以及兼容 Amazon S3 协议的存储服务中。Cloud storage 价格便宜，使用方便。对于不使用 Kafka 的用户，可以选择使用 storage sink。使用该功能，TiCDC 会将 changed log 保存到文件，发送到存储系统中。用户自研的消费程序定时从存储系统读取新产生的 changed log 进行数据处理。

    Storage sink 支持格式为 canal-json 和 csv 的 changed log。更多信息，请参考[用户文档](/ticdc/ticdc-sink-to-cloud-storage.md)。

* TiCDC 支持在两个 TiDB 集群之间进行双向复制 [#38587](https://github.com/pingcap/tidb/issues/38587) @[xiongjiwei](https://github.com/xiongjiwei) @[asddongmen](https://github.com/asddongmen)

    TiCDC 支持在两个 TiDB 集群之间进行双向复制。如果业务上需要构建异地多活的 TiDB 集群架构，可以使用该功能作为 TiDB 多活的解决方案。只要为 TiDB 集群到另一个 TiDB 集群的 TiCDC 同步任务配置 `bdr-mode = true` 参数，就可以实现两个 TiDB 集群之间的数据相互复制。

    更多信息，请参考[用户文档](/ticdc/ticdc-bidirectional-replication.md)。

* TiCDC 支持在线更新 TLS 证书 [tiflow#7908](https://github.com/pingcap/tiflow/issues/7908) @[CharlesCheung96](https://github.com/CharlesCheung96)

    为确保系统数据安全，用户会对系统使用的证书设置相应的过期策略，经过固定的时间后会将系统使用的证书更换成新证书。TiCDC v6.5.0 支持在线更新 TLS 证书，在不影响同步任务的前提下，TiCDC 会自动检测和更新证书，无需用户手动操作，满足用户对证书更新的需求。

* TiCDC 性能提升 [#7540](https://github.com/pingcap/tiflow/issues/7540) [#7478](https://github.com/pingcap/tiflow/issues/7478) [#7532](https://github.com/pingcap/tiflow/issues/7532) @[sdojjy](https://github.com/sdojjy) @[3AceShowHand](https://github.com/3AceShowHand)

    在 TiDB 场景测试验证中，TiCDC 的性能得到了比较大的提升。

    在同步到 Kafka 的场景中，单台 TiCDC 节点能处理的最大行变更吞吐可以达到 30K rows/s，同步延迟降低到 10s。即使在常规的 TiKV/TiCDC 滚动升级场景，同步延迟也小于 30s。
    
    在容灾场景测试中，打开 TiCDC redo log 和 Syncpoint 后，吞吐从 4000 行每秒提升到 35000 行每秒，容灾复制延迟可以保持在 2s。

### 备份和恢复

* TiDB 快照备份支持断点续传 [#38647](https://github.com/pingcap/tidb/issues/38647) @[Leavrth](https://github.com/Leavrth)

    TiDB 快照备份功能支持断点续传。当 BR 遇到可恢复的错误时会进行重试，但是超过固定重试次数之后会备份退出。断点续传功能允许对持续更长时间的可恢复故障进行重试恢复，比如几十分钟的网络故障。

    需要注意的是，如果你没有在 BR 退出后一个小时内完成故障恢复，那么还未备份的快照数据可能会被 GC 机制回收，从而造成备份失败。更多信息，请参考[用户文档](/br/br-checkpoint-backup.md#确保在-gc-前重试)。

* PITR 性能大幅提升 @[joccau](https://github.com/joccau)

  PITR 恢复的日志恢复阶段，单台 TiKV 的恢复速度可以达到 9 MiB/s，提升了 50%，并且恢复速度可扩展，有效地降低容灾场景的 RTO 指标；容灾场景的 RPO 优化到 5 分钟，在常规的集群运维，如滚动升级，单 TiKV 故障等场景下，可以达到 RPO = 5 min 的目标。

* TiKV-BR 工具 GA，支持 RawKV 的备份和恢复 [#67](https://github.com/tikv/migration/issues/67) @[pingyu](https://github.com/pingyu) @[haojinming](https://github.com/haojinming)

    TiKV-BR 是一个 TiKV 集群的备份和恢复工具。TiKV 可以独立于 TiDB，与 PD 构成 KV 数据库，此时的产品形态为 RawKV。TiKV-BR 工具支持对使用 RawKV 的产品进行备份和恢复，也支持将 TiKV 集群中的数据从 `API V1` 备份为 `API V2` 数据，以实现 TiKV 集群 [`api-version`](/tikv-configuration-file.md#api-version-从-v610-版本开始引入) 的升级。

    更多信息，请参考[用户文档](https://tikv.org/docs/latest/concepts/explore-tikv-features/backup-restore/)。

## 兼容性变更

### 系统变量

| 变量名  | 修改类型                      | 描述 |
|--------|------------------------------|------|
|`tidb_enable_amend_pessimistic_txn` | 废弃 | 从 v6.5.0 起，该变量被废弃，TiDB 会默认使用[元数据锁](/metadata-lock.md)机制解决 `Information schema is changed` 报错的问题。|
| [`tidb_enable_outer_join_reorder`](/system-variables.md#tidb_enable_outer_join_reorder-从-v610-版本开始引入) | 修改 | 经进一步的测试后，该变量默认值从 `OFF` 修改为 `ON`，表示默认启用 Outer Join 的 [Join Reorder 算法](/join-reorder.md)。|
| [`tidb_cost_model_version`](/system-variables.md#tidb_cost_model_version-从-v620-版本开始引入) | 修改 | 经进一步的测试后，该变量默认值从 `1` 修改为 `2`，表示默认使用 Cost Model Version 2 进行索引选择和算子选择。 |
| [`tidb_enable_gc_aware_memory_track`](/system-variables.md#tidb_enable_gc_aware_memory_track) |  修改 | 该变量默认值由 `ON` 修改为 `OFF`。由于在测试中发现 GC-Aware memory track 不准确，导致 Analyze 追踪到的内存过大的情况，因此先关闭内存追踪。在 Golang 1.19 下，GC-Aware memory track 追踪的内存对整体内存的影响变小。|
| [`tidb_enable_metadata_lock`](/system-variables.md#tidb_enable_metadata_lock-从-v630-版本开始引入) | 修改 | 经进一步的测试后，该变量默认值从 `OFF` 修改为 `ON`，表示默认开启元数据锁。 |
| [`tidb_enable_tiflash_read_for_write_stmt`](/system-variables.md#tidb_enable_tiflash_read_for_write_stmt-从-v630-版本开始引入) | 修改 | 该变量从 v6.5.0 开始生效，默认值为 `OFF`，用来控制包含增删改的 SQL 语句中的读取操作能否下推到 TiFlash。|
| [`tidb_ddl_enable_fast_reorg`](/system-variables.md#tidb_ddl_enable_fast_reorg-从-v630-版本开始引入) | 修改 | 经进一步的测试后，该变量默认值从 `OFF` 修改为 `ON`，表示默认开启创建索引加速功能。 |
| [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query) | 修改 | 在 v6.5.0 之前的版本中，该变量用来设置单条查询的内存使用限制。在 v6.5.0 及之后的版本中，为了对 DML 语句的内存进行更准确地控制，该变量用来设置单个会话整体的内存使用限制。 |
| [`tidb_replica_read`](/system-variables.md#tidb_replica_read-从-v40-版本开始引入) | 修改 | 从 v6.5.0 起，为了优化各个 TiDB 节点的负载均衡，当该变量的值为 `closest-adaptive` 时，如果一个读请求的预估返回结果大于或等于 [`tidb_adaptive_closest_read_threshold`](/system-variables.md#tidb_adaptive_closest_read_threshold-从-v630-版本开始引入)，在每个可用区中 `closest-adaptive` 配置实际生效的 TiDB 节点数总是与包含 TiDB 节点最少的可用区中的 TiDB 节点数相同。对于生效的节点，TiDB 会优先选择分布在同一可用区的副本执行读取操作，其他多出的 TiDB 节点将自动切换为读取 leader 副本。 |
| [`tidb_server_memory_limit`](/system-variables.md#tidb_server_memory_limit-从-v640-版本开始引入) |  修改 | 该变量默认值由 `0` 修改为 `80%`，因为 TiDB 全局内存控制特性 GA，该调整默认开启 TiDB 实例的内存限制，并将默认的内存限制设为总内存的 80%。|
| [`default_password_lifetime`](/system-variables.md#default_password_lifetime-从-v650-版本开始引入) | 新增 | 用于设置全局自动密码过期策略，要求用户定期修改密码。默认值为 `0`，表示禁用全局自动密码过期策略。 |
| [`disconnect_on_expired_password`](/system-variables.md#disconnect_on_expired_password-从-v650-版本开始引入) | 新增 | 该变量是一个只读变量，用来显示 TiDB 是否会直接断开密码已过期用户的连接。 |
| [`tidb_store_batch_size`](/system-variables.md#tidb_store_batch_size) | 新增 | 该变量默认关闭，其控制的功能尚未稳定，不建议在生产环境中修改该变量值。 |
| [`password_history`](/system-variables.md#password_history-从-v650-版本开始引入) | 新增 | 基于密码更改次数的密码重用策略，不允许用户重复使用最近设置次数内使用过的密码。默认值为 `0`，表示禁用基于密码更改次数的密码重用策略。 |
| [`password_reuse_interval`](/system-variables.md#password_reuse_interval-从-v650-版本开始引入) | 新增 | 基于经过时间限制的密码重用策略，不允许用户重复使用最近设置天数内使用过的密码。默认值为 `0`，表示禁用基于密码更改时间内的密码重用策略。 |
| [`tidb_auto_build_stats_concurrency`](/system-variables.md#tidb_auto_build_stats_concurrency-从-v650-版本开始引入) | 新增 | 该变量用于设置执行统计信息自动更新的并发度，默认值为 `1`。 |
| [`tidb_cdc_write_source`](/system-variables.md#tidb_cdc_write_source-从-v650-版本开始引入) | 新增 | 当变量非 `0` 时，该 SESSION 写入的数据将被视为是由 TiCDC 写入的。这个变量仅由 TiCDC 设置，任何时候都不应该手动调整该变量。 |
| [`tidb_enable_plan_replayer_capture`](/system-variables.md#tidb_enable_plan_replayer_capture) | 新增 | 在 v6.5.0，该变量控制的功能尚未完全生效，请保留默认值。 |
| [`tidb_index_merge_intersection_concurrency`](/system-variables.md#tidb_index_merge_intersection_concurrency-从-v650-版本开始引入) | 新增 | 这个变量用来设置索引合并进行交集操作时的最大并发度，仅在以动态裁剪模式访问分区表时有效。 |
| [`tidb_source_id`](/system-variables.md#tidb_source_id-从-v650-版本开始引入) | 新增 | 设置在[双向复制](/ticdc/ticdc-bidirectional-replication.md)系统内不同集群的 ID。|
| [`tidb_sysproc_scan_concurrency`](/system-variables.md#tidb_sysproc_scan_concurrency-从-v650-版本开始引入) | 新增 | 该变量用于设置 TiDB 执行内部 SQL 语句（例如统计信息自动更新）时 scan 操作的并发度，默认值为 `1`。 |
| [`tidb_ttl_delete_batch_size`](/system-variables.md#tidb_ttl_delete_batch_size-从-v650-版本开始引入) | 新增 | 这个变量用于设置 TTL 任务中单个删除事务中允许删除的最大行数。|
| [`tidb_ttl_delete_rate_limit`](/system-variables.md#tidb_ttl_delete_rate_limit-从-v650-版本开始引入) | 新增 | 这个变量用于限制在 TTL 任务中单个节点每秒允许 `DELETE` 语句执行的最大次数。当此变量设置为 `0` 时，则表示不做限制。|
| [`tidb_ttl_delete_worker_count`](/system-variables.md#tidb_ttl_delete_worker_count-从-v650-版本开始引入) | 新增 | 这个变量用于设置每个 TiDB 节点上 TTL 删除任务的最大并发数。|
| [`tidb_ttl_job_enable`](/system-variables.md#tidb_ttl_job_enable-从-v650-版本开始引入) | 新增 | 这个变量用于控制是否启动 TTL 后台清理任务。如果设置为 `OFF`，所有具有 TTL 属性的表会自动停止清理过期数据。|
| `tidb_ttl_job_run_interval` | 新增 | 这个变量用于控制 TTL 后台清理任务的调度周期。比如，如果当前值设置成了 `1h0m0s`，则代表每张设置了 TTL 属性的表会每小时清理一次过期数据。|
| [`tidb_ttl_job_schedule_window_start_time`](/system-variables.md#tidb_ttl_job_schedule_window_start_time-从-v650-版本开始引入) | 新增 | 这个变量用于控制 TTL 后台清理任务的调度窗口的起始时间。请谨慎调整此参数，过小的窗口有可能会造成过期数据的清理无法完成。|
| [`tidb_ttl_job_schedule_window_end_time`](/system-variables.md#tidb_ttl_job_schedule_window_end_time-从-v650-版本开始引入) | 新增 | 这个变量用于控制 TTL 后台清理任务的调度窗口的结束时间。请谨慎调整此参数，过小的窗口有可能会造成过期数据的清理无法完成。|
| [`tidb_ttl_scan_batch_size`](/system-variables.md#tidb_ttl_scan_batch_size-从-v650-版本开始引入) | 新增 | 这个变量用于设置 TTL 任务中用来扫描过期数据的每个 `SELECT` 语句的 `LIMIT` 的值。|
| [`tidb_ttl_scan_worker_count`](/system-variables.md#tidb_ttl_scan_worker_count-从-v650-版本开始引入) | 新增 | 这个变量用于设置每个 TiDB 节点 TTL 扫描任务的最大并发数。|
| [`validate_password.check_user_name`](/system-variables.md#validate_passwordcheck_user_name-从-v650-版本开始引入) | 新增 | 密码复杂度策略检查项，设置的用户密码不允许密码与当前会话账户的用户名部分相同。只有 [`validate_password.enable`](/system-variables.md#validate_passwordenable-从-v650-版本开始引入) 开启时，该变量才生效。默认值为 `ON`。 |
| [`validate_password.dictionary`](/system-variables.md#validate_passworddictionary-从-v650-版本开始引入) | 新增 | 密码复杂度策略检查项，密码字典功能，设置的用户密码不允许包含字典中的单词。只有 [`validate_password.enable`](/system-variables.md#validate_passwordenable-从-v650-版本开始引入) 开启且 [validate_password.policy](/system-variables.md#validate_passwordpolicy-从-v650-版本开始引入) 设置为 `2` (STRONG) 时，该变量才生效。默认值为空。 |
| [`validate_password.enable`](/system-variables.md#validate_passwordenable-从-v650-版本开始引入) | 新增 | 密码复杂度策略检查的开关，设置为 `ON` 后，TiDB 才进行密码复杂度检查。默认值为 `OFF`。 |
| [`validate_password.length`](/system-variables.md#validate_passwordlength-从-v650-版本开始引入) | 新增 | 密码复杂度策略检查项，限定了用户密码最小长度。只有 [`validate_password.enable`](/system-variables.md#validate_passwordenable-从-v650-版本开始引入) 开启时，该变量才生效。默认值为 `8`。 |
| [`validate_password.mixed_case_count`](/system-variables.md#validate_passwordmixed_case_count-从-v650-版本开始引入) | 新增 | 密码复杂度策略检查项，限定了用户密码中大写字符和小写字符的最小数量。只有 [`validate_password.enable`](/system-variables.md#validate_passwordenable-从-v650-版本开始引入) 开启且 [validate_password.policy](/system-variables.md#validate_passwordpolicy-从-v650-版本开始引入) 大于或等于 `1` (MEDIUM) 时，该变量才生效。默认值为 `1`。 |
| [`validate_password.number_count`](/system-variables.md#validate_passwordnumber_count-从-v650-版本开始引入) | 新增 | 密码复杂度策略检查项，限定了用户密码中数字字符的最小数量。只有 [`validate_password.enable`](/system-variables.md#validate_passwordenable-从-v650-版本开始引入) 开启且 [validate_password.policy](/system-variables.md#validate_passwordpolicy-从-v650-版本开始引入) 大于或等于 `1` (MEDIUM) 时，该变量才生效。默认值为 `1`。 |
| [`validate_password.policy`](/system-variables.md#validate_passwordpolicy-从-v650-版本开始引入) | 新增 | 密码复杂度策略检查的强度，强度等级分为 `[0, 1, 2]`。只有 [`validate_password.enable`](/system-variables.md#validate_passwordenable-从-v650-版本开始引入) 开启时，该变量才生效。默认值为 `1`。 |
| [`validate_password.special_char_count`](/system-variables.md#validate_passwordspecial_char_count-从-v650-版本开始引入) | 新增 | 密码复杂度策略检查项，限定了用户密码中特殊字符的最小数量。只有 [`validate_password.enable`](/system-variables.md#validate_passwordenable-从-v650-版本开始引入) 开启且 [validate_password.policy](/system-variables.md#validate_passwordpolicy-从-v650-版本开始引入) 大于或等于 `1` (MEDIUM) 时，该变量才生效。默认值为 `1`。 |

### 配置文件参数

| 配置文件 | 配置项 | 修改类型 | 描述 |
| -------- | -------- | -------- | -------- |
| TiDB | [`server-memory-quota`](/tidb-configuration-file.md#server-memory-quota-从-v409-版本开始引入) | 废弃 | 自 v6.5.0 起，该配置项被废弃。请使用 [`tidb_server_memory_limit`](/system-variables.md#tidb_server_memory_limit-从-v640-版本开始引入) 系统变量进行设置。 |
| TiDB | [`disconnect-on-expired-password`](/tidb-configuration-file.md#disconnect-on-expired-password-从-v650-版本开始引入) | 新增 | 该配置用于控制 TiDB 服务端是否直接断开密码已过期用户的连接，默认值为 `true`，表示 TiDB 服务端将直接断开密码已过期用户的连接。 |
| TiKV | `raw-min-ts-outlier-threshold` | 删除 | 从 v6.4.0 起，该配置项被废弃。从 v6.5.0 起，该配置项被删除。 |
| TiKV | [`raft-engine.bytes-per-sync`](/tikv-configuration-file.md#bytes-per-sync-2) | 废弃 | 从 v6.5.0 起，Raft Engine 在写入日志时不会缓存而是直接落盘，因此该配置项被废弃，且不再生效。 |
| TiKV | [`cdc.min-ts-interval`](/tikv-configuration-file.md#min-ts-interval) | 修改 | 为了降低 CDC 延迟，该配置的默认值从 `"1s"` 修改为 `"200ms"`。 |
| TiKV | [`memory-use-ratio`](/tikv-configuration-file.md#memory-use-ratio-从-v650-版本开始引入) | 新增 | 表示 PITR 日志恢复功能中可用内存与系统总内存的占比。 |
| TiCDC | [`sink.terminator`](/ticdc/ticdc-changefeed-config.md#ticdc-changefeed-配置文件说明) | 新增 | 换行符，用来分隔两个数据变更事件。默认值为空，表示使用 `\r\n` 作为换行符。 |
| TiCDC | [`sink.date-separator`](/ticdc/ticdc-changefeed-config.md#ticdc-changefeed-配置文件说明) | 新增 | 文件路径的日期分隔类型。可选类型有 `none`、`year`、`month`、`day`。默认值为 `none`，即不使用日期分隔。|
| TiCDC | [`sink.enable-partition-separator`](/ticdc/ticdc-changefeed-config.md#ticdc-changefeed-配置文件说明) | 新增 | 是否使用 partition 作为分隔字符串，默认值为 false，即一张表中各个 partition 的数据不会分不同的目录来存储。 |
| TiCDC | [`sink.csv.delimiter`](/ticdc/ticdc-changefeed-config.md#ticdc-changefeed-配置文件说明) | 新增 | 字段之间的分隔符。必须为 ASCII 字符，默认值为 `,`。 |
| TiCDC | [`sink.csv.quote`](/ticdc/ticdc-changefeed-config.md#ticdc-changefeed-配置文件说明) | 新增 | 用于包裹字段的引号字符。空值代表不使用引号字符。默认值为 `"`。 |
| TiCDC | [`sink.csv.null`](/ticdc/ticdc-changefeed-config.md#ticdc-changefeed-配置文件说明) | 新增 | 用于确定 CSV 列为 null 时将以什么字符来表示。默认值为 `\N`。 |
| TiCDC | [`sink.csv.include-commit-ts`](/ticdc/ticdc-changefeed-config.md#ticdc-changefeed-配置文件说明) | 新增| 是否在 CSV 行中包含 commit-ts。默认值为 `false`。 |

### 其他

- 从 v6.5.0 起，`mysql.user` 表新增 `Password_reuse_history` 和 `Password_reuse_time` 两个字段。
- 从 v6.5.0 起，[添加索引加速功能](/system-variables.md#tidb_ddl_enable_fast_reorg-从-v630-版本开始引入)默认开启。该功能和[单条 `ALTER TABLE` 语句增删改多个列或索引](/sql-statements/sql-statement-alter-table.md)功能未完全兼容，在使用索引加速功能添加唯一索引时，请避免在单条语句添加唯一索引的同时操作其他列或者索引对象。同时，该功能与 [PITR (Point-in-time recovery)](/br/br-pitr-guide.md) 不兼容。在使用索引加速功能时，需要确保后台没有启动 PITR 备份任务，否则可能会出现非预期结果。详情请参考 [`tidb_ddl_enable_fast_reorg`](/system-variables.md#tidb_ddl_enable_fast_reorg-从-v630-版本开始引入)。

## 废弃功能

从 v6.5.0 起，废弃 v4.0.7 版本引入的 `AMEND TRANSACTION` 机制，并使用[元数据锁](/metadata-lock.md)替代。

## 改进提升

+ TiDB

    - 对于 `BIT` 和 `CHAR` 类型的列，使 `INFORMATION_SCHEMA.COLUMNS` 的显示结果与 MySQL 一致 [#25472](https://github.com/pingcap/tidb/issues/25472) @[hawkingrei](https://github.com/hawkingrei)
    - 优化 TiDB 在 TiFlash MPP 模式下对 TiFlash 节点的探活机制，缓解节点异常时对性能的影响 [#39686](https://github.com/pingcap/tidb/issues/39686) @[hackersean](https://github.com/hackersean)

+ TiKV

    - 当剩余空间不足时停止 Raft Engine 的写入以避免硬盘空间耗尽 [#13642](https://github.com/tikv/tikv/issues/13642) @[jiayang-zheng](https://github.com/jiayang-zheng)
    - 支持将 `json_valid` 函数下推至 TiKV [#13571](https://github.com/tikv/tikv/issues/13571) @[lizhenhuan](https://github.com/lizhenhuan)
    - 支持在一个备份请求中同时备份多个范围的数据 [#13701](https://github.com/tikv/tikv/issues/13701) @[Leavrth](https://github.com/Leavrth)
    - 更新 rusoto 库以支持备份到 AWS 的 Asia Pacific (Jakarta) 区域 (ap-southeast-3) [#13751](https://github.com/tikv/tikv/issues/13751) @[3pointer](https://github.com/3pointer)
    - 减少悲观事务冲突 [#13298](https://github.com/tikv/tikv/issues/13298) @[MyonKeminta](https://github.com/MyonKeminta)
    - 缓存外部存储对象以提升恢复性能 [#13798](https://github.com/tikv/tikv/issues/13798) @[YuJuncen](https://github.com/YuJuncen)
    - 在专用线程中运行 CheckLeader 以缩短 TiCDC 的复制延迟 [#13774](https://github.com/tikv/tikv/issues/13774) @[overvenus](https://github.com/overvenus)
    - Checkpoint 支持拉取模式 [#13824](https://github.com/tikv/tikv/issues/13824) @[YuJuncen](https://github.com/YuJuncen)
    - 升级 crossbeam-channel 以优化发送端的自旋问题 [#13815](https://github.com/tikv/tikv/issues/13815) @[sticnarf](https://github.com/sticnarf)
    - TiKV 支持批量处理 Coprocessor 任务 [#13849](https://github.com/tikv/tikv/issues/13849) @[cfzjywxk](https://github.com/cfzjywxk)
    - 故障恢复时通知 TiKV 唤醒休眠的 Region 以减少等待时间 [#13648](https://github.com/tikv/tikv/issues/13648) @[LykxSassinator](https://github.com/LykxSassinator)
    - 通过代码优化减少内存申请的大小 [#13827](https://github.com/tikv/tikv/issues/13827) @[BusyJay](https://github.com/BusyJay)
    - 引入 Raft extension 以提升代码可扩展性 [#13827](https://github.com/tikv/tikv/issues/13827) @[BusyJay](https://github.com/BusyJay)
    - tikv-ctl 支持查询某个 key 范围中包含哪些 Region [#13760](https://github.com/tikv/tikv/issues/13760) @[HuSharp](https://github.com/HuSharp)
    - 改进持续对特定行只加锁但不更新的情况下的读写性能 [#13694](https://github.com/tikv/tikv/issues/13694) @[sticnarf](https://github.com/sticnarf)

+ PD

    - 优化锁的粒度以减少锁争用，提升高并发下心跳的处理能力 [#5586](https://github.com/tikv/pd/issues/5586) @[rleungx](https://github.com/rleungx)
    - 优化调度器在大规模集群下的性能，提升调度策略生产速度 [#5473](https://github.com/tikv/pd/issues/5473) @[bufferflies](https://github.com/bufferflies)
    - 提高 PD 加载 Region 的速度 [#5606](https://github.com/tikv/pd/issues/5606) @[rleungx](https://github.com/rleungx)
    - 优化心跳处理过程，减少不必要的开销 [#5648](https://github.com/tikv/pd/issues/5648) @[rleungx](https://github.com/rleungx)
    - 增加了自动清理 tombstone store 的功能 [#5348](https://github.com/tikv/pd/issues/5348) @[nolouch](https://github.com/nolouch)

+ TiFlash

    - 提升了 TiFlash 在 SQL 端没有攒批场景时的写入性能 [#6404](https://github.com/pingcap/tiflash/issues/6404) @[lidezhu](https://github.com/lidezhu)
    - 在 `explain analyze` 结果中增加更多关于 TableFullScan 算子的信息 [#5926](https://github.com/pingcap/tiflash/issues/5926) @[hongyunyan](https://github.com/hongyunyan)

+ Tools

    + TiDB Dashboard

        - 在慢查询页面新增以下三个字段：`是否由 prepare 语句生成`、`查询计划是否来自缓存`、`查询计划是否来自绑定` [#1451](https://github.com/pingcap/tidb-dashboard/issues/1451) @[shhdgit](https://github.com/shhdgit)

    + Backup & Restore (BR)

        - 优化清理备份日志数据时 BR 的内存使用 [#38869](https://github.com/pingcap/tidb/issues/38869) @[Leavrth](https://github.com/Leavrth)
        - 修复恢复过程中由于 PD leader 切换导致恢复失败的问题 [#36910](https://github.com/pingcap/tidb/issues/36910) @[MoCuishle28](https://github.com/MoCuishle28)
        - 日志备份的 TLS 功能使用 OpenSSL 协议，提升 TLS 的兼容性 [#13867](https://github.com/tikv/tikv/issues/13867) @[YuJuncen](https://github.com/YuJuncen)

    + TiCDC

        - 提升 Kafka 相关协议的编码性能  [#7540](https://github.com/pingcap/tiflow/issues/7540) [#7532](https://github.com/pingcap/tiflow/issues/7532) [#7543](https://github.com/pingcap/tiflow/issues/7543) @[3AceShowHand](https://github.com/3AceShowHand) @[sdojjy](https://github.com/sdojjy)

    + TiDB Data Migration (DM)

        - 通过不再解析黑名单中表的数据提升 DM 同步数据的性能 [#7622](https://github.com/pingcap/tiflow/pull/7622) @[GMHDBJD](https://github.com/GMHDBJD)
        - 通过异步写与批量写的方式提升 DM relay 的写数据效率 [#7580](https://github.com/pingcap/tiflow/pull/7580) @[GMHDBJD](https://github.com/GMHDBJD)
        - 改进 DM 前置检查的错误提示信息 [#7621](https://github.com/pingcap/tiflow/issues/7621) @[buchuitoudegou](https://github.com/buchuitoudegou)
        - 改进 DM 针对老版本 MySQL 使用 `SHOW SLAVE HOSTS` 获取结果时的兼容性 [#5017](https://github.com/pingcap/tiflow/issues/5017) @[lyzx2001](https://github.com/lyzx2001)

## 错误修复

+ TiDB

    - 修复 chunk 复用功能在部分情况下内存 chunk 被错误使用的问题 [#38917](https://github.com/pingcap/tidb/issues/38917) @[keeplearning20221](https://github.com/keeplearning20221)
    - 修复 `tidb_constraint_check_in_place_pessimistic` 可能被全局设置影响内部 session 的问题 [#38766](https://github.com/pingcap/tidb/issues/38766) @[ekexium](https://github.com/ekexium)
    - 修复了 `AUTO_INCREMENT` 列无法和 `CHECK` 约束一起使用的问题 [#38894](https://github.com/pingcap/tidb/issues/38894) @[YangKeao](https://github.com/YangKeao)
    - 修复使用 `INSERT IGNORE INTO` 往 `SMALLINT` 类型的自增列插入 `STRING` 类型的数据会报错的问题 [#38483](https://github.com/pingcap/tidb/issues/38483) @[hawkingrei](https://github.com/hawkingrei)
    - 修复了重命名分区表的分区列操作出现空指针报错的问题 [#38932](https://github.com/pingcap/tidb/issues/38932) @[mjonss](https://github.com/mjonss)
    - 修复了修改分区表的分区列导致 DDL 卡死的问题 [#38530](https://github.com/pingcap/tidb/issues/38530) @[mjonss](https://github.com/mjonss)
    - 修复了从 v4.0.16 升级到 v6.4.0 后 `ADMIN SHOW JOB` 操作崩溃的问题 [#38980](https://github.com/pingcap/tidb/issues/38980) @[tangenta](https://github.com/tangenta)
    - 修复了 `tidb_decode_key` 函数未正确处理分区表编码的问题 [#39304](https://github.com/pingcap/tidb/issues/39304) @[Defined2014](https://github.com/Defined2014)
    - 修复了日志轮转时，gRPC 的错误日志信息未被重定向到正确的日志文件的问题 [#38941](https://github.com/pingcap/tidb/issues/38941) @[xhebox](https://github.com/xhebox)
    - 修复了 `BEGIN; SELECT... FOR UPDATE;` 点查在读数据存储引擎 (`tidb_isolation_read_engines`) 未配置 TiKV 时生成非预期执行计划的问题 [#39344](https://github.com/pingcap/tidb/issues/39344) @[Yisaer](https://github.com/Yisaer)
    - 修复了错误地下推 `StreamAgg` 到 TiFlash 导致结果错误的问题 [#39266](https://github.com/pingcap/tidb/issues/39266) @[fixdb](https://github.com/fixdb)

+ TiKV

    - 修复 Raft Engine ctl 中的错误 [#11119](https://github.com/tikv/tikv/issues/11119) @[tabokie](https://github.com/tabokie)
    - 修复 tikv-ctl 执行 `compact raft` 命令时报错的问题 [#13515](https://github.com/tikv/tikv/issues/13515) @[guoxiangCN](https://github.com/guoxiangCN)
    - 修复当启用 TLS 时日志备份无法使用的问题 [#13867](https://github.com/tikv/tikv/issues/13867) @[YuJuncen](https://github.com/YuJuncen)
    - 修复对 Geometry 字段类型的支持问题 [#13651](https://github.com/tikv/tikv/issues/13651) @[dveeden](https://github.com/dveeden)
    - 修复当未启用 new collation 时 `LIKE` 操作符中的 `_` 无法匹配非 ASCII 字符的问题 [#13769](https://github.com/tikv/tikv/issues/13769) @[YangKeao](https://github.com/YangKeao)
    - 修复 tikv-ctl 执行 `reset-to-version` 命令时被终止的问题 [#13829](https://github.com/tikv/tikv/issues/13829) @[tabokie](https://github.com/tabokie)

+ PD

    - 修复热点调度配置在没有修改的情况下不持久化的问题 [#5701](https://github.com/tikv/pd/issues/5701) @[HunDunDM](https://github.com/HunDunDM)
    - 修复 `rank-formula-version` 在升级过程中没有保持升级前的配置的问题 [#5698](https://github.com/tikv/pd/issues/5698) @[HunDunDM](https://github.com/HunDunDM)

+ TiFlash

    - 修复 TiFlash 重启后 delta 层的小文件无法合并 (compact) 的问题 [#6159](https://github.com/pingcap/tiflash/issues/6159) @[lidezhu](https://github.com/lidezhu)
    - 修复 TiFlash File Open OPS 过高的问题 [#6345](https://github.com/pingcap/tiflash/issues/6345) @[JaySon-Huang](https://github.com/JaySon-Huang)

+ Tools

    + Backup & Restore (BR)

        - 修复 BR 删除日志备份数据时，会删除不应被删除的数据的问题 [#38939](https://github.com/pingcap/tidb/issues/38939) @[Leavrth](https://github.com/Leavrth)
        - 修复数据库或数据表中使用旧的排序规则框架时，数据恢复失败的问题 [#39150](https://github.com/pingcap/tidb/issues/39150) @[MoCuishle28](https://github.com/MoCuishle28)
        - 修复阿里云和华为云与 S3 存储不完全兼容导致的备份失败问题 [#39545](https://github.com/pingcap/tidb/issues/39545) @[3pointer](https://github.com/3pointer)

    + TiCDC

        - 修复 PD leader crash 时 TiCDC 卡住的问题 [#7470](https://github.com/pingcap/tiflow/issues/7470) @[zeminzhou](https://github.com/zeminzhou)
        - 修复在执行 DDL 后，暂停然后恢复 changefeed 会导致数据丢失的问题 [#7682](https://github.com/pingcap/tiflow/issues/7682) @[asddongmen](https://github.com/asddongmen)
        - 修复存在高版本 TiFlash 时，TiCDC 会误报错的问题 [#7744](https://github.com/pingcap/tiflow/issues/7744) @[overvenus](https://github.com/overvenus)
        - 修复下游网络发生异常时 sink 模块卡住的问题 [#7706](https://github.com/pingcap/tiflow/issues/7706) @[hicqu](https://github.com/hicqu)
        - 修复用户快速删除、创建同名同步任务可能导致的数据丢失问题 [#7657](https://github.com/pingcap/tiflow/issues/7657) @[overvenus](https://github.com/overvenus)

    + TiDB Data Migration (DM)

        - 修复在上游开启 `GTID` mode 且无数据时，无法启动 `all` mode 任务的问题 [#7037](https://github.com/pingcap/tiflow/issues/7037) @[liumengya94](https://github.com/liumengya94)
        - 修复当 DM worker 即将退出时新 worker 调度过快导致数据被重复同步的问题 [#7658](https://github.com/pingcap/tiflow/issues/7658) @[GMHDBJD](https://github.com/GMHDBJD)
        - 修复上游数据库使用正则匹配授权时 DM 前置检查不通过的错误 [#7645](https://github.com/pingcap/tiflow/issues/7645) @[lance6716](https://github.com/lance6716)

    + TiDB Lightning

        - 修复 TiDB Lightning 导入巨大数据源文件时的内存泄漏问题 [#39331](https://github.com/pingcap/tidb/issues/39331) @[dsdashun](https://github.com/dsdashun)
        - 修复 TiDB Lightning 在并行导入冲突检测时无法正确检测的问题 [#39476](https://github.com/pingcap/tidb/issues/39476) @[dsdashun](https://github.com/dsdashun)

## 贡献者

感谢来自 TiDB 社区的贡献者们：

- [e1ijah1](https://github.com/e1ijah1)
- [guoxiangCN](https://github.com/guoxiangCN)（首次贡献者）
- [jiayang-zheng](https://github.com/jiayang-zheng)
- [jiyfhust](https://github.com/jiyfhust)
- [mikechengwei](https://github.com/mikechengwei)
- [pingandb](https://github.com/pingandb)
- [sashashura](https://github.com/sashashura)
- [sourcelliu](https://github.com/sourcelliu)
- [wxbty](https://github.com/wxbty)
