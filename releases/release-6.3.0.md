---
title: TiDB 6.3.0 Release Notes
summary: 了解 TiDB 6.3.0 版本的新功能、兼容性变更、改进提升，以及错误修复。
---

# TiDB 6.3.0 Release Notes

发版日期：2022 年 9 月 30 日

TiDB 版本：6.3.0-DMR

> **注意：**
>
> TiDB 6.3.0-DMR 的用户文档已[归档](https://docs-archive.pingcap.com/zh/tidb/v6.3)。如无特殊需求，建议使用 TiDB 数据库的[最新 LTS 版本](https://docs.pingcap.com/zh/tidb/stable)。

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v6.3/quick-start-with-tidb) | [下载离线包](https://cn.pingcap.com/product-community/?version=v6.3.0-DMR#version-list)

在 6.3.0-DMR 版本中，你可以获得以下关键特性：

- TiKV 静态加密支持国密算法 SM4。
- TiDB 支持基于国密算法 SM3 插件的身份验证。
- SQL 语句 `CREATE USER` 和 `ALTER USER` 支持 `ACCOUNT LOCK/UNLOCK` 选项。
- JSON 数据类型和 JSON 函数 GA。
- TiDB 支持 Null-Aware Anti Join。
- TiDB 提供 SQL 查询执行时间的细粒度指标。
- 分区表新增简化 Range 分区的语法糖。
- Range COLUMNS 分区方式支持定义多列。
- TiDB 添加索引的速度提升为原来的 3 倍。
- 降低资源消耗型查询对轻量查询响应时间的影响超 50%。

## 新功能

### SQL

* 新增简化 Range 分区定义的语法糖 (syntactic sugar) Range INTERVAL 分区特性（实验特性）[#35683](https://github.com/pingcap/tidb/issues/35683) @[mjonss](https://github.com/mjonss)

    提供了新的定义 Range 分区的方式 [Range INTERVAL 分区](/partitioned-table.md#range-interval-分区)，不需要枚举所有分区，可大幅度缩短现有 Range 分区表定义语句冗长的书写方式。语义与原有 Range 分区等价。

* Range COLUMNS 分区方式支持定义多列 [#36636](https://github.com/pingcap/tidb/issues/36636) @[mjonss](https://github.com/mjonss)

    支持 [Range COLUMNS 分区](/partitioned-table.md#range-columns-分区)，`column_list` 不再限定为单一列，基本功能与 MySQL 等同。

* 分区表 [EXCHANGE PARTITION 功能](/partitioned-table.md#分区管理) GA [#35996](https://github.com/pingcap/tidb/issues/35996) @[ymkzpx](https://github.com/ymkzpx)

* 新增支持下推两个[窗口函数](/tiflash/tiflash-supported-pushdown-calculations.md) 至 TiFlash [#5579](https://github.com/pingcap/tiflash/issues/5579) @[SeaRise](https://github.com/SeaRise)

    * `LEAD()`
    * `LAG()`

* 提供轻量级元数据锁，提升 DDL 变更过程 DML 的成功率（实验特性）[#37275](https://github.com/pingcap/tidb/issues/37275) @[wjhuang2016](https://github.com/wjhuang2016)

    在 TiDB 中，对元数据对象的更改采用的是在线异步变更算法。事务在执行时会获取开始时对应的元数据快照。如果事务执行过程中相关表上发生了元数据的更改，为了保证数据的一致性，TiDB 会返回 `Information schema is changed` 的错误，导致用户事务提交失败。为了解决这个问题，在 TiDB v6.3.0 中，online DDL 算法中引入了[元数据锁](/metadata-lock.md)特性。通过协调表元数据变更过程中 DML 语句和 DDL 语句的优先级，让执行中的 DDL 语句等待持有旧版本元数据的 DML 语句提交，尽可能避免 DML 语句报错。

* 提升添加索引的性能，减少对 DML 事务的影响（实验特性）[#35983](https://github.com/pingcap/tidb/issues/35983) @[benjamin2037](https://github.com/benjamin2037)

    TiDB v6.3.0 支持开启[添加索引加速](/system-variables.md#tidb_ddl_enable_fast_reorg-从-v630-版本开始引入)功能，提升了创建索引回填过程的速度。开启该功能后，TiDB 添加索引的性能提升约为原来的 3 倍。

### 安全

* TiKV 静态加密支持国密算法 SM4 [#13041](https://github.com/tikv/tikv/issues/13041) @[jiayang-zheng](https://github.com/jiayang-zheng)

    TiKV 的静态加密新增 [SM4 算法](/encryption-at-rest.md)，用户在配置静态加密时，可将 `data-encryption-method` 参数设为 `sm4-ctr`，以启用基于国密算法 SM4 的静态加密能力。

* TiDB 支持国密算法 SM3 的身份验证 [#36192](https://github.com/pingcap/tidb/issues/36192) @[CbcWestwolf](https://github.com/CbcWestwolf)

    TiDB 身份验证新增基于国密算法 SM3 的插件 [`tidb_sm3_password`](/system-variables.md#default_authentication_plugin)，启用此插件后，用户密码将通过 SM3 进行加密存储和验证。

* TiDB-JDBC 支持国密算法 SM3 的身份验证 [#25](https://github.com/pingcap/mysql-connector-j/issues/25) @[lastincisor](https://github.com/lastincisor)

    用户密码的身份验证需要客户端的支持，现在 [TiDB-JDBC 支持国密算法 SM3](/develop/dev-guide-choose-driver-or-orm.md#java-drivers)，你可以使用国密算法 SM3 的身份验证能力通过 TiDB-JDBC 连接到 TiDB。

### 可观测性

* 提供 TiDB SQL 查询执行时间的细粒度指标 [#34106](https://github.com/pingcap/tidb/issues/34106) @[cfzjywxk](https://github.com/cfzjywxk)

    TiDB v6.3.0 提供了细粒度的数据指标，用于[对执行时间进行细化观测](/latency-breakdown.md)。通过完整且细分的指标数据，可以清晰地了解 SQL 查询主要的时间消耗，从而快速发现关键问题，节省故障诊断的时间。

* 增强慢日志和 `TRACE` 语句的输出 [#34106](https://github.com/pingcap/tidb/issues/34106) @[cfzjywxk](https://github.com/cfzjywxk)

    TiDB v6.3.0 增强了慢日志的内容和 `TRACE` 的输出。你可以观测到 SQL 语句执行过程中，从 TiDB 解析到 KV RocksDB 落盘[全链路的延迟数据](/latency-breakdown.md)，进一步增强 TiDB 的诊断能力。

* TiDB Dashboard 中显示死锁的历史记录 [#34106](https://github.com/pingcap/tidb/issues/34106) @[cfzjywxk](https://github.com/cfzjywxk)

    从 v6.3.0 起，死锁的历史记录将添加到 TiDB Dashboard。当你通过 TiDB Dashboard 的慢日志等手段发现某些 SQL 等待锁的时间较长时，可以分析 TiDB Dashboard 上的死锁历史记录来定位问题，提升了诊断的易用性。

### 性能

* TiFlash 调整 FastScan 功能使用方式（实验特性）[#5252](https://github.com/pingcap/tiflash/issues/5252) @[hongyunyan](https://github.com/hongyunyan)

    TiFlash 从 v6.2.0 版本开始引入的快速扫描功能 (FastScan)，性能上符合预期，但是使用方式上不够灵活。因此，TiFlash 在 v6.3.0 版本[调整 FastScan 功能的使用方式](/tiflash/use-fastscan.md)：废弃了 `ALTER TABLE ...SET TiFLASH MODE ...` 语法启用方式，改为使用系统变量 [`tiflash_fastscan`](/system-variables.md#tiflash_fastscan-从-v630-版本开始引入) 进行控制。

    从 v6.2.0 版本升级到 v6.3.0 版本时，在 v6.2.0 版本的 FastScan 设置将失效，但不影响数据的正常读取。你需要重新使用变量方式设置 FastScan。从 v6.2.0 及更早版本升级到 v6.3.0 时，所有会话默认不开启 FastScan 功能，而是保持一致性的数据扫描功能。

* TiFlash 优化提升多并发场景下的数据扫描性能 [#5376](https://github.com/pingcap/tiflash/issues/5376) @[JinheLin](https://github.com/JinheLin)

    TiFlash 通过合并相同数据的读取操作，减少了对相同数据的重复读取，优化了多并发任务情况下的资源开销，[提升多并发下的数据扫描性能](/tiflash/tiflash-configuration.md#配置文件-tiflashtoml)。避免了以往在多并发任务下，如果涉及相同数据，同一份数据需要在每个任务中分别进行读取的情况，以及可能出现在同一时间内对同一份数据进行多次读取的情况。

    该功能在 v6.2.0 版本以实验特性发布，在 v6.3.0 版本作为正式功能发布。

* TiFlash 副本同步性能优化 [#5237](https://github.com/pingcap/tiflash/issues/5237) @[breezewish](https://github.com/breezewish)

    TiFlash 使用 Raft 协议与 TiKV 进行副本数据同步。在 v6.3.0 版本之前，同步大量副本数据往往耗时较长。v6.3.0 版本优化了 TiFlash 副本同步机制，大幅提升了副本同步速度。因此，使用 BR 恢复数据、使用 TiDB Lightning 导入数据、或全新增加 TiFlash 副本时，副本将迅速地完成同步，你可以及时地使用 TiFlash 进行查询。此外，在 TiFlash 扩容、缩容、或修改 TiFlash 副本数时，TiFlash 副本也将更快地达到安全、均衡的状态。

* TiFlash 针对单个 `COUNT(DISTINCT)` 进行三阶段聚合 [#37202](https://github.com/pingcap/tidb/issues/37202) @[fixdb](https://github.com/fixdb)

     TiFlash 将有且仅有单个 `COUNT(DISTINCT)` 聚合的查询改写为[三阶段分布式执行的聚合](/system-variables.md#tidb_opt_three_stage_distinct_agg-从-v630-版本开始引入)，从而提高并发度，并提升性能。

* TiKV 支持日志回收 [#214](https://github.com/tikv/raft-engine/issues/214) @[LykxSassinator](https://github.com/LykxSassinator)

    TiKV Raft Engine 支持[日志回收](/tikv-configuration-file.md#enable-log-recycle-从-v630-版本开始引入)功能。该特性能够显著降低网络磁盘上 Raft 日志追加过程中的长尾延迟，提升了 TiKV 写入负载下的性能。

* TiDB 支持 Null-Aware Anti Join [#37525](https://github.com/pingcap/tidb/issues/37525) @[Arenatlx](https://github.com/Arenatlx)

    TiDB v6.3.0 引入了新的连接类型 [Null-Aware Anti Join (NAAJ)](/explain-subqueries.md#null-aware-anti-semi-joinnot-in-和--all-子查询)。NAAJ 在处理集合操作时能够感知集合是否为空，或是否有空值，优化了 `IN` 和 `= ANY` 等操作的执行效率，提升 SQL 性能。

* 增加优化器 hint 控制哈希连接的驱动端 [#35439](https://github.com/pingcap/tidb/issues/35439) @[Reminiscent](https://github.com/Reminiscent)

    在 v6.3.0 版本中，优化器引入了两个新的 hint，[`HASH_JOIN_BUILD()` 和 `HASH_JOIN_PROBE()`](/optimizer-hints.md)，用于隐式地指定哈希连接的行为，同时分别指定哈希连接的构建端和探测端。如果优化器未选到最优执行计划，可以使用这两个 hint 来干预执行计划。

* 允许在会话级别内联展开公共表表达式 (CTE) [#36514](https://github.com/pingcap/tidb/issues/36514) @[elsa0520](https://github.com/elsa0520)

    在 v6.2.0 中，引入了优化器提示 `MERGE`，允许对 CTE 内联进行展开，使得 CTE 查询结果的消费者能够在 TiFlash 内并行执行。在 v6.3.0 中，又进一步添加了会话级变量 [`tidb_opt_force_inline_cte`](/system-variables.md#tidb_opt_force_inline_cte-从-v630-版本开始引入)，允许在会话中修改这个行为，提升了易用性。

### 事务

* 悲观事务可以延迟唯一约束检查 [#36579](https://github.com/pingcap/tidb/issues/36579) @[ekexium](https://github.com/ekexium)

    你可以通过系统变量 [`tidb_constraint_check_in_place_pessimistic`](/system-variables.md#tidb_constraint_check_in_place_pessimistic-从-v630-版本开始引入) 来控制悲观事务中[唯一约束](/constraints.md#悲观事务)检查的时间点。该变量默认关闭。当开启该变量时（设为 `ON`），TiDB 会将悲观事务中的加锁操作和唯一约束检测推迟到必要的时候进行，以此提升批量 DML 操作的性能。

* 优化 Read-Committed 隔离级别中对 TSO 的获取 [#36812](https://github.com/pingcap/tidb/issues/36812) @[TonsnakeLin](https://github.com/TonsnakeLin)

    在 Read-Committed 隔离级别中，引入新的系统变量 [`tidb_rc_write_check_ts`](/system-variables.md#tidb_rc_write_check_ts-从-v630-版本开始引入) 控制语句对 TSO 的获取方式。在 Plan Cache 命中的情况下，通过降低对 TSO 的获取频率，提升批量 DML 的执行效率，降低跑批类任务的执行时间。

### 稳定性

* 降低资源消耗型查询对轻量查询响应时间的影响 [#13313](https://github.com/tikv/tikv/issues/13313) @[glorv](https://github.com/glorv)

  当资源消耗型查询与轻量查询同时运行时，轻量查询的响应时间会被严重影响。在这种情况下，通常希望优先快速处理轻量查询，以保证交易类负载的服务质量。因此 TiKV 在 v6.3.0 中优化了读请求的调度机制，使资源消耗型的查询在每一轮执行的时间更符合预期。这个特性大幅降低了资源消耗型查询对轻量查询的影响，使混合工作负载的 P99 延迟降低了 50% 以上。

* 修改优化器统计信息过期时的默认统计信息使用策略 [#27601](https://github.com/pingcap/tidb/issues/27601) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes)

    在 v5.3.0 版本，TiDB 引入系统变量 [`tidb_enable_pseudo_for_outdated_stats`](/system-variables.md#tidb_enable_pseudo_for_outdated_stats-从-v530-版本开始引入) 控制优化器在统计信息过期时的行为，默认为 `ON`，即保持旧版本行为不变：当 SQL 涉及的对象的统计信息过期时，优化器认为该表上除总行数以外的统计信息不再可靠，转而使用 pseudo 统计信息。经过一系列测试和用户实际场景分析，TiDB 在新版本中将 `tidb_enable_pseudo_for_outdated_stats` 的默认值改为 `OFF`，即使统计信息过期，优化器也仍会使用该表上的统计信息，这有利于执行计划的稳定性。

* TiKV 正式支持关闭 Titan 引擎 @[tabokie](https://github.com/tabokie)

    正式支持对在线 TiKV 节点[关闭 Titan 引擎](/storage-engine/titan-configuration.md#关闭-titan)。

* 缺少 GlobalStats 时自动选择分区静态剪裁 [#37535](https://github.com/pingcap/tidb/issues/37535) @[Yisaer](https://github.com/Yisaer)

    当启用分区[动态剪裁](/partitioned-table.md#动态裁剪模式)时，优化器依赖 [GlobalStats](/statistics.md#动态裁剪模式下的分区表统计信息) 进行执行计划的选择。在 [GlobalStats](/statistics.md#动态裁剪模式下的分区表统计信息) 收集完成前，使用 pseudo 统计信息可能会造成性能回退。在 v6.3.0 版本中，如果在 [GlobalStats](/statistics.md#动态裁剪模式下的分区表统计信息) 收集未完成的情况下打开动态分区裁剪开关，TiDB 会维持静态分区剪裁的状态，直到 GlobalStats 收集完成。该方式确保在切换分区剪裁策略时系统性能保持稳定。

### 易用性

* 解决基于 SQL 的数据放置规则功能和构建 TiFlash 副本功能的冲突 [#37171](https://github.com/pingcap/tidb/issues/37171) @[lcwangchao](https://github.com/lcwangchao)

    TiDB 在 v6.0.0 版本提供[基于 SQL 的数据放置规则](/placement-rules-in-sql.md)功能，但是由于实现机制问题，该功能和构建 TiFlash 副本功能有冲突。v6.3.0 版本进行改进优化，解决了这两个功能的冲突，使这两个功能更加方便易用。

### MySQL 兼容性

* 新增支持 `REGEXP_INSTR()`、`REGEXP_LIKE()`、`REGEXP_REPLACE()` 和 `REGEXP_SUBSTR()` 4 个正则表达式函数，提升 TiDB 与 MySQL 8.0 的兼容性 [#23881](https://github.com/pingcap/tidb/issues/23881) @[windtalker](https://github.com/windtalker)

    这些函数与 MySQL 的兼容性可参考[正则函数与 MySQL 的兼容性](/functions-and-operators/string-functions.md#正则函数与-mysql-的兼容性)。

* `CREATE USER` 和 `ALTER USER` 支持 `ACCOUNT LOCK/UNLOCK` 选项 [#37051](https://github.com/pingcap/tidb/issues/37051) @[CbcWestwolf](https://github.com/CbcWestwolf)

    在执行 [`CREATE USER`](/sql-statements/sql-statement-create-user.md) 创建用户时，允许使用 `ACCOUNT LOCK/UNLOCK` 选项，限定被创建的用户是否被锁定。锁定后的用户不能正常登录数据库。

    对于已存在的用户，可以通过 [`ALTER USER`](/sql-statements/sql-statement-alter-user.md) 使用 `ACCOUNT LOCK/UNLOCK` 选项，修改用户的锁定状态。

* JSON 数据类型和 JSON 函数 GA [#36993](https://github.com/pingcap/tidb/issues/36993) @[xiongjiwei](https://github.com/xiongjiwei)

    JSON 是一种流行的数据格式，被大量的程序设计所采用。TiDB 在早期版本就引入了 [JSON 支持](/data-type-json.md)，兼容 MySQL 的 JSON 数据类型和一部分 JSON 函数。在 v6.3.0 版本中，这些功能正式 GA，为 TiDB 提供了更丰富的数据类型支持，同时[表达式索引](/sql-statements/sql-statement-create-index.md#表达式索引)和[生成列](/generated-columns.md)也增加了对 JSON 函数的支持，进一步提升了 TiDB 对 MySQL 的兼容能力。

### 备份恢复

* PITR 支持 [GCS 和 Azure Blob Storage](/br/backup-and-restore-storages.md) 作为备份存储 @[joccau](https://github.com/joccau)

    部署在 Google Cloud 或者 Azure 上的用户，将 TiDB 集群升级至 v6.3.0 就可以使用 PITR 功能。

* BR 支持 AWS S3 Object Lock [#13442](https://github.com/tikv/tikv/issues/13442) @[3pointer](https://github.com/3pointer)

    你可以在 AWS 开启 [S3 Object Lock](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html) 功能来防止备份数据写入后被修改或者删除。

### 数据迁移

* TiDB Lightning 支持[将 Apache Hive 导出的 Parquet 文件导入到 TiDB](/tidb-lightning/tidb-lightning-data-source.md#parquet) [#37536](https://github.com/pingcap/tidb/issues/37536) @[buchuitoudegou](https://github.com/buchuitoudegou)

* DM 新增配置项 `safe-mode-duration` [#6224](https://github.com/pingcap/tiflow/issues/6224) @[okJiang](https://github.com/okJiang)

    DM 任务配置文件中新增一个配置项 [`safe-mode-duration`](/dm/task-configuration-file-full.md#完整配置文件示例)，用户可以自行调节 DM 异常重启后进入安全模式的持续时间，默认值 60 秒。当设置为 "0s" 时，表示 DM 异常重启后尝试进入安全模式会报错。

### 数据共享与订阅

* TiCDC 支持对多个异地目标数据源进行数据复制 [#5301](https://github.com/pingcap/tiflow/issues/5301) @[sdojjy](https://github.com/sdojjy)

    为了支持从一个 TiDB 集群复制数据到多个不同的异地数据系统，自 v6.3.0 开始，TiCDC 节点可以[部署到多个不同的异地的机房](/ticdc/deploy-ticdc.md)中，用于分别负责对应机房的数据复制任务，以支撑各种复杂的异地数据复制使用场景和部署形态。

* TiCDC 支持维护上下游数据一致性快照 (Sync point) [#6977](https://github.com/pingcap/tiflow/issues/6977) @[asddongmen](https://github.com/asddongmen)

    在灾备复制场景下，TiCDC 支持[周期性地维护一个下游数据快照](/ticdc/ticdc-upstream-downstream-check.md)，使得该下游快照能与上游数据的快照保持一致。借助此能力，TiCDC 能更好地匹配读写分离应用场景，帮助用户降本增效。

* TiCDC 支持平滑升级 [#4757](https://github.com/pingcap/tiflow/issues/4757) @[overvenus](https://github.com/overvenus) @[3AceShowHand](https://github.com/3AceShowHand)

    用户使用 [TiUP](/ticdc/deploy-ticdc.md#使用-tiup-升级-ticdc-集群) (>=v1.11.0) 和 [TiDB Operator](https://docs.pingcap.com/zh/tidb-in-kubernetes/v1.3/configure-a-tidb-cluster#配置-ticdc-平滑升级) (>=v1.3.8) 可以平滑滚动升级 TiCDC 集群。升级期间数据同步延时保持在 30 秒内，提高了稳定性，让 TiCDC 能更好地支持延时敏感型业务。

## 兼容性变更

### 系统变量

| 变量名 | 修改类型 | 描述 |
| ------ | ------ | ------ |
| [`default_authentication_plugin`](/system-variables.md#default_authentication_plugin) | 修改 | 扩展可选值范围：增加 `tidb_sm3_password`。设置为 `tidb_sm3_password` 时，用户密码验证的加密算法为国密算法 SM3。 |
| [`sql_require_primary_key`](/system-variables.md#sql_require_primary_key-从-v630-版本开始引入)   |  新增  |  用于控制表是否必须有主键。启用该变量后，如果在没有主键的情况下创建或修改表，将返回错误。 |
| [`tidb_adaptive_closest_read_threshold`](/system-variables.md#tidb_adaptive_closest_read_threshold-从-v630-版本开始引入) | 新增 | 用于控制当 [`tidb_replica_read`](/system-variables.md#tidb_replica_read-从-v40-版本开始引入) 设置为 `closest-adaptive` 时，优先将读请求发送至 TiDB server 所在区域副本的阈值。 |
| [`tidb_constraint_check_in_place_pessimistic`](/system-variables.md#tidb_constraint_check_in_place_pessimistic-从-v630-版本开始引入) | 新增 |  用于控制悲观事务中唯一约束检查的时间点。 |
| [`tidb_ddl_disk_quota`](/system-variables.md#tidb_ddl_disk_quota-从-v630-版本开始引入) | 新增 | 用于设置创建索引的回填过程中本地存储空间的使用限制。仅在 [`tidb_ddl_enable_fast_reorg`](/system-variables.md#tidb_ddl_enable_fast_reorg-从-v630-版本开始引入) 开启的情况下生效。 |
| [`tidb_ddl_enable_fast_reorg`](/system-variables.md#tidb_ddl_enable_fast_reorg-从-v630-版本开始引入) | 新增 | 用于控制是否开启添加索引加速功能，来提升创建索引回填过程的速度。 |
| [`tidb_ddl_flashback_concurrency`](/system-variables.md#tidb_ddl_flashback_concurrency-从-v630-版本开始引入) | 新增 | 用于控制 `flashback cluster` 的并发数。在 v6.3.0，该变量控制的功能尚未完全生效，请保留默认值。  |
| [`tidb_enable_exchange_partition`](/system-variables.md#tidb_enable_exchange_partition) | 废弃 | 用于设置是否启用 [`exchange partitions with tables`](/partitioned-table.md#分区管理) 特性。自 v6.3.0 开始，其取值将固定为默认值 `ON`，即默认开启 `exchange partitions with tables`。  |
| [`tidb_enable_foreign_key`](/system-variables.md#tidb_enable_foreign_key-从-v630-版本开始引入) | 新增 |  用于控制是否开启 `FOREIGN KEY` 特性。在 v6.3.0，该变量控制的功能尚未完全生效，请保留默认值。 |
| `tidb_enable_general_plan_cache` | 新增 |  用于控制是否开启 General Plan Cache。在 v6.3.0，该变量控制的功能尚未完全生效，请保留默认值。 |
| [`tidb_enable_metadata_lock`](/system-variables.md#tidb_enable_metadata_lock-从-v630-版本开始引入)|  新增 | 用于设置是否开启[元数据锁](/metadata-lock.md)特性。 |
| [`tidb_enable_null_aware_anti_join`](/system-variables.md#tidb_enable_null_aware_anti_join-从-v630-版本开始引入) | 新增 |  用于控制 TiDB 对特殊集合算子 `NOT IN` 和 `!= ALL` 引导的子查询产生的 Anti Join 是否采用 Null-Aware Hash Join 的执行方式。|
| [`tidb_enable_pseudo_for_outdated_stats`](/system-variables.md#tidb_enable_pseudo_for_outdated_stats-从-v530-版本开始引入) | 修改 | 用于控制优化器在统计信息过期时的行为。 默认值由 `ON` 改为 `OFF`，即使统计信息过期，优化器也仍会使用该表上的统计信息。  |
| [`tidb_enable_rate_limit_action`](/system-variables.md#tidb_enable_rate_limit_action) | 修改 | 用于控制是否为读数据的算子开启动态内存控制功能。打开该变量可能会导致内存不受 [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query) 控制，而加剧 OOM 风险，故将默认值由 `ON` 调整为 `OFF`。 |
| [`tidb_enable_tiflash_read_for_write_stmt`](/system-variables.md#tidb_enable_tiflash_read_for_write_stmt-从-v630-版本开始引入) | 新增 |  用于控制写 SQL 中的读取是否会下推到 TiFlash。在 v6.3.0，该变量控制的功能尚未完全生效，请保留默认值。 |
| [`tidb_enable_unsafe_substitute`](/system-variables.md#tidb_enable_unsafe_substitute-从-v630-版本开始引入) | 新增 | 用于控制是否对生成列中表达式替换使用不安全的替换方式。 |
| `tidb_general_plan_cache_size` | 新增 | 用于控制 General Plan Cache 最多能够缓存的计划数量。在 v6.3.0，该变量控制的功能尚未完全生效，请保留默认值。 |
| [`tidb_last_plan_replayer_token`](/system-variables.md#tidb_last_plan_replayer_token-从-v630-版本开始引入) | 新增 | 只读变量，用于获取当前会话中最后一个 `PLAN REPLAYER DUMP` 的结果。 |
| [`tidb_max_paging_size`](/system-variables.md#tidb_max_paging_size-从-v630-版本开始引入) | 新增 | 用来设置 coprocessor 协议中 paging size 的最大的行数。 |
| [`tidb_opt_force_inline_cte`](/system-variables.md#tidb_opt_force_inline_cte-从-v630-版本开始引入) | 新增 | 用于控制是否强制开启 inline CTE。默认值为 `OFF`，即默认不强制开启 inline CTE。 |
| [`tidb_opt_three_stage_distinct_agg`](/system-variables.md#tidb_opt_three_stage_distinct_agg-从-v630-版本开始引入) | 新增 | 用于控制在 MPP 模式下是否将 `COUNT(DISTINCT)` 聚合改写为三阶段分布式执行的聚合。默认为 `ON`。 |
| [`tidb_partition_prune_mode`](/system-variables.md#tidb_partition_prune_mode-从-v51-版本开始引入) | 修改 | 用于设置是否开启分区表动态裁剪模式。自 v6.3.0 起，该变量默认值修改为 `dynamic`。 |
| [`tidb_rc_read_check_ts`](/system-variables.md#tidb_rc_read_check_ts-从-v600-版本开始引入) | 修改 | 用于优化读语句时间戳的获取，适用于悲观事务 RC 隔离级别下读写冲突较少的场景。由于这个行为只针对特定业务负载，而对其他类型的负载可能造成性能回退。自 v6.3.0 起，该变量的作用域由 GLOBAL 或 SESSION 修改为 INSTANCE 级别，允许只针对部分 TiDB 实例打开。 |
| [`tidb_rc_write_check_ts`](/system-variables.md#tidb_rc_write_check_ts-从-v630-版本开始引入)  | 新增 | 用于优化时间戳的获取，适用于悲观事务 RC 隔离级别下点写冲突较少的场景，开启此变量可以避免点写语句获取全局 timestamp 带来的延迟和开销。 |
| [`tiflash_fastscan`](/system-variables.md#tiflash_fastscan-从-v630-版本开始引入) | 新增 | 用于控制是否启用 FastScan 功能。如果开启 FastScan 功能（设置为 `ON` 时），TiFlash 可以提供更高效的查询性能，但不保证查询结果的精度和数据一致性。 |

### 配置文件参数

| 配置文件 | 配置项 | 修改类型 | 描述 |
| -------- | -------- | -------- | -------- |
| TiDB | [`temp-dir`](/tidb-configuration-file.md#temp-dir-从-v630-版本开始引入) | 新增 | TiDB 用于存放临时数据的路径。需要使用 TiDB 节点本地存储的功能会将数据临时存放在这个目录下。默认值为 `/tmp/tidb`。 |
| TiKV | [`auto-adjust-pool-size`](/tikv-configuration-file.md#auto-adjust-pool-size-从-v630-版本开始引入) | 新增 | 控制是否开启自动调整线程池的大小。开启此配置可以基于当前的 CPU 使用情况，自动调整统一处理读请求的线程池 (UnifyReadPool) 的大小，优化 TiKV 的读性能。|
| TiKV | [`data-encryption-method`](/tikv-configuration-file.md#data-encryption-method) | 修改 | 扩展可选值范围：增加 `sm4-ctr`。设置为 `sm4-ctr` 时，数据将采用国密算法 SM4 加密后进行存储。 |
| TiKV | [`enable-log-recycle`](/tikv-configuration-file.md#enable-log-recycle-从-v630-版本开始引入) | 新增 | 控制 Raft Engine 是否回收过期的日志文件。该配置项启用时，Raft Engine 将保留逻辑上被清除的日志文件，用于日志回收，减少写负载的长尾延迟。仅在 `format-version` 的值大于等于 2 时，该配置项才生效。 |
| TiKV | [`format-version`](/tikv-configuration-file.md#format-version-从-v630-版本开始引入) | 新增 | 指定 Raft Engine 的日志文件格式版本。v6.3.0 以前的默认值为 `1`。v6.1.0 及以后版本的 TiKV 可以读取该格式。v6.3.0 及以后版本，该配置项默认值为 `2`，TiKV 可以读取该格式。 |
| TiKV | [`log-backup.enable`](/tikv-configuration-file.md#enable-从-v620-版本开始引入) | 修改 | 默认值在 v6.3.0 以前是 `false`，v6.3.0 开始设为 `true`。 |
| TiKV | [`log-backup.max-flush-interval`](/tikv-configuration-file.md#max-flush-interval-从-v620-版本开始引入) | 修改 | 默认值在 v6.3.0 以前是 `5min`，v6.3.0 开始设为 `3min`。 |
| PD | [enable-diagnostic](/pd-configuration-file.md#enable-diagnostic-从-v630-版本开始引入) | 新增 | 控制是否开启诊断功能。默认值为 `false`。 |
| TiFlash | [`dt_enable_read_thread`](/tiflash/tiflash-configuration.md#配置文件-tiflashtoml) | 废弃 | 该参数从 v6.3.0 开始废弃，默认开启此功能且不能关闭。 |
| DM | [`safe-mode-duration`](/dm/task-configuration-file-full.md#完整配置文件示例) | 新增 | 自动安全模式的持续时间。
| TiCDC | [`enable-sync-point`](/ticdc/ticdc-changefeed-config.md#ticdc-changefeed-配置文件说明) | 新增 | 控制是否开启 sync point 功能。 |
| TiCDC | [`sync-point-interval`](/ticdc/ticdc-changefeed-config.md#ticdc-changefeed-配置文件说明) | 新增 | 控制 sync point 功能对齐上下游 snapshot 的时间间隔。 |
| TiCDC | [`sync-point-retention`](/ticdc/ticdc-changefeed-config.md#ticdc-changefeed-配置文件说明) | 新增 | sync point 功能在下游表中保存的数据的时长，超过这个时间的数据会被清理。 |
| TiCDC | [`sink-uri.memory`](/ticdc/ticdc-changefeed-config.md#ticdc-changefeed-命令行参数) | 废弃 | 废弃 `memory` 排序方式，不建议在任何情况下使用。 |

### 其他

* 日志备份支持 GCS 和 Azure Blob Storage 作为备份存储。
* 日志备份功能兼容分区交换 (Exchange Partition) DDL。
* 不再支持通过 `ALTER TABLE ...SET TiFLASH MODE ...` 语法启用或禁用 [FastScan](/tiflash/use-fastscan.md) 功能。从 v6.2.0 版本升级到 v6.3.0 版本时，在 v6.2.0 版本的 FastScan 设置将失效，但不影响数据的正常读取。你需要重新使用变量方式设置 FastScan。从 v6.2.0 及更早版本升级到 v6.3.0 时，所有会话默认不开启 FastScan 功能，而是保持一致性的数据扫描功能。
* 在 Linux AMD64 架构的硬件平台部署 TiFlash 时，CPU 必须支持 AVX2 指令集。确保命令 `cat /proc/cpuinfo | grep avx2` 有输出。而在 Linux ARM64 架构的硬件平台部署 TiFlash 时，CPU 必须支持 ARMv8 架构。确保命令 `cat /proc/cpuinfo | grep 'crc32' | grep 'asimd'` 有输出。通过使用向量扩展指令集，TiFlash 的向量化引擎能提供更好的性能。
* TiDB 支持的最小 HAProxy 版本为 v1.5。使用 v1.5 到 v2.1 之间的 HAProxy 时，需要在 `mysql-check` 中配置 `post-41`。建议使用 HAProxy v2.2 或更高版本。

## 废弃功能

自 v6.3.0 起，TiCDC 不再支持配置 Pulsar Sink。建议使用 StreamNative 官方维护的 [kop](https://github.com/streamnative/kop) 作为替代方案。

## 改进提升

+ TiDB

    - 改进表名检查方式，由大小写敏感变为大小写不敏感 [#34610](https://github.com/pingcap/tidb/issues/34610) @[tiancaiamao](https://github.com/tiancaiamao)
    - 为 `init_connect`  值增加解析器检查流程，提升了与 MySQL 的兼容性 [#35324](https://github.com/pingcap/tidb/issues/35324) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - 改进新连接产生时的警告日志 [#34964](https://github.com/pingcap/tidb/issues/34964) @[xiongjiwei](https://github.com/xiongjiwei)
    - 优化用于查询 DDL 历史任务的 HTTP API，提供对 `start_job_id` 参数的支持 [#35838](https://github.com/pingcap/tidb/issues/35838) @[tiancaiamao](https://github.com/tiancaiamao)
    - 在 JSON 路径的语法有误时报错 [#22525](https://github.com/pingcap/tidb/issues/22525) [#34959](https://github.com/pingcap/tidb/issues/34959) @[xiongjiwei](https://github.com/xiongjiwei)
    - 修复一个伪共享问题，提升 Join 操作的性能 [#37641](https://github.com/pingcap/tidb/issues/37641) @[gengliqi](https://github.com/gengliqi)
    - `PLAN REPLAYER` 命令支持一次导出多条 SQL 语句的执行计划信息，提升了问题排查效率 [#37798](https://github.com/pingcap/tidb/issues/37798) @[Yisaer](https://github.com/Yisaer)

+ TiKV

    - 支持配置 `unreachable_backoff` 避免 Raftstore 发现某个 Peer 无法连接时广播过多消息 [#13054](https://github.com/tikv/tikv/issues/13054) @[5kbpers](https://github.com/5kbpers)
    - 提升 TSO 服务不可用的容忍度 [#12794](https://github.com/tikv/tikv/issues/12794) @[pingyu](https://github.com/pingyu)
    - 支持动态调整 RocksDB 进行 subcompaction 的并发个数 (`rocksdb.max-sub-compactions`) [#13145](https://github.com/tikv/tikv/issues/13145) @[ethercflow](https://github.com/ethercflow)
    - 优化合并空 Region 的性能 [#12421](https://github.com/tikv/tikv/issues/12421) @[tabokie](https://github.com/tabokie)
    - 支持更多正则表达式函数 [#13483](https://github.com/tikv/tikv/issues/13483) @[gengliqi](https://github.com/gengliqi)
    - 支持根据 CPU 使用情况自动调整 UnifyReadPool 线程池的大小 [#13313](https://github.com/tikv/tikv/issues/13313) @[glorv](https://github.com/glorv)

+ PD

    - 更新 TiDB Dashboard 中 TiKV IO MBps 指标的计算方式 [#5366](https://github.com/tikv/pd/issues/5366) @[YiniXu9506](https://github.com/YiniXu9506)
    - 将 TiDB Dashboard 中 `metrics` 更改为 `monitoring` [#5366](https://github.com/tikv/pd/issues/5366) @[YiniXu9506](https://github.com/YiniXu9506)

+ TiFlash

    - 支持下推 `elt` 到 TiFlash [#5104](https://github.com/pingcap/tiflash/issues/5104) @[Willendless](https://github.com/Willendless)
    - 支持下推 `leftShift` 到 TiFlash [#5099](https://github.com/pingcap/tiflash/issues/5099) @[AnnieoftheStars](https://github.com/AnnieoftheStars)
    - 支持下推 `castTimeAsDuration` 到 TiFlash [#5306](https://github.com/pingcap/tiflash/issues/5306) @[AntiTopQuark](https://github.com/AntiTopQuark)
    - 支持下推 `HexIntArg/HexStrArg` 到 TiFlash [#5107](https://github.com/pingcap/tiflash/issues/5107) @[YangKeao](https://github.com/YangKeao)
    - 重构改进 TiFlash 的执行流解释器，支持新的解释器 Planner [#4739](https://github.com/pingcap/tiflash/issues/4739) @[SeaRise](https://github.com/SeaRise)
    - 改进了 TiFlash memory tracker 的准确度 [#5609](https://github.com/pingcap/tiflash/issues/5609) @[bestwoody](https://github.com/bestwoody)
    - 提升了 UTF8_BIN/ASCII_BIN/LATIN1_BIN/UTF8MB4_BIN collation 的列相关运算的速度 [#5294](https://github.com/pingcap/tiflash/issues/5294) @[solotzg](https://github.com/solotzg)
    - 在后台计算 ReadLimiter 的 I/O 吞吐量 [#5401](https://github.com/pingcap/tiflash/issues/5401) [#5091](https://github.com/pingcap/tiflash/issues/5091) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)

+ Tools

    + Backup & Restore (BR)

        - PITR 可以聚合日志备份中生成的小日志文件，大幅减小文件数量 [#13232](https://github.com/tikv/tikv/issues/13232) @[Leavrth](https://github.com/Leavrth)
        - PITR 支持在恢复完成后自动按照上游集群配置设置 TiFlash 副本 [#37208](https://github.com/pingcap/tidb/issues/37208) @[YuJuncen](https://github.com/YuJuncen)

    + TiCDC

        - 提升上游 TiDB 引入并行 DDL 框架后 TiCDC 的兼容性 [#6506](https://github.com/pingcap/tiflow/issues/6506) @[lance6716](https://github.com/lance6716)
        - 支持在 MySL sink 出错时将 DML 语句的 `start ts` 输出到日志文件 [#6460](https://github.com/pingcap/tiflow/issues/6460) @[overvenus](https://github.com/overvenus)
        - 优化 API `api/v1/health`，使其返回的 TiCDC 集群健康状态更准确 [#4757](https://github.com/pingcap/tiflow/issues/4757) @[overvenus](https://github.com/overvenus)
        - 采用异步的模式实现 MQ sink 和 MySQL sink，提升 sink 的吞吐能力 [#5928](https://github.com/pingcap/tiflow/issues/5928) @[hicqu](https://github.com/hicqu) @[hi-rustin](https://github.com/Rustin170506)
        - 删除已经废弃了的 pulsar sink [#7087](https://github.com/pingcap/tiflow/issues/7087) @[hi-rustin](https://github.com/Rustin170506)
        - 忽略掉与 changefeed 不相关的 DDL 语句以提升同步性能 [#6447](https://github.com/pingcap/tiflow/issues/6447) @[asddongmen](https://github.com/asddongmen)

    + TiDB Data Migration (DM)

        - 提升与 MySQL 8.0 数据源的兼容性 [#6448](https://github.com/pingcap/tiflow/issues/6448) @[lance6716](https://github.com/lance6716)
        - 优化 DDL 执行逻辑，当执行 DDL 超时时，转为异步查询 DDL 执行结果 [#4689](https://github.com/pingcap/tiflow/issues/4689) @[lyzx2001](https://github.com/lyzx2001)

    + TiDB Lightning

        - 在 S3 URL 中添加新参数 `role-arn` 和 `external-id`，支持从其他账户访问 S3 数据 [#36891](https://github.com/pingcap/tidb/issues/36891) @[dsdashun](https://github.com/dsdashun)

## 错误修复

+ TiDB

    - 修复权限检查跳过 `PREPARE` 语句的问题 [#35784](https://github.com/pingcap/tidb/issues/35784) @[lcwangchao](https://github.com/lcwangchao)
    - 修复系统变量 `tidb_enable_noop_variable` 能够设置为 `WARN` 的问题 [#36647](https://github.com/pingcap/tidb/issues/36647) @[lcwangchao](https://github.com/lcwangchao)
    - 修复存在表达式索引定义时，`INFORMATION_SCHEMA.COLUMNS` 表的 `ORDINAL_POSITION` 列可能不正确的问题 [#31200](https://github.com/pingcap/tidb/issues/31200) @[bb7133](https://github.com/bb7133)
    - 修复时间戳大于 `MAXINT32` 时 TiDB 不报错的问题  [#31585](https://github.com/pingcap/tidb/issues/31585) @[bb7133](https://github.com/bb7133)
    - 修复使用企业版插件时无法启动 TiDB server 的问题 [#37319](https://github.com/pingcap/tidb/issues/37319) @[xhebox](https://github.com/xhebox)
    - 修复 `SHOW CREATE PLACEMENT POLICY` 输出结果不正确的问题 [#37526](https://github.com/pingcap/tidb/issues/37526) @[xhebox](https://github.com/xhebox)
    - 修复临时表能用于交换分区的问题 [#37201](https://github.com/pingcap/tidb/issues/37201) @[lcwangchao](https://github.com/lcwangchao)
    - 修复查询 `INFORMATION_SCHEMA.TIKV_REGION_STATUS` 返回不正确结果的问题 @[zimulala](https://github.com/zimulala)
    - 修复使用 `EXPLAIN` 查询视图时不进行权限检查的问题 [#34326](https://github.com/pingcap/tidb/issues/34326) @[hawkingrei](https://github.com/hawkingrei)
    - 修复 JSON `null` 不能被更新为 `NULL` 的问题 [#37852](https://github.com/pingcap/tidb/issues/37852) @[YangKeao](https://github.com/YangKeao)
    - 修复 DDL 任务的 `row_count` 不准确的问题 [#25968](https://github.com/pingcap/tidb/issues/25968) @[Defined2014](https://github.com/Defined2014)
    - 修复 `FLASHBACK TABLE` 运行不正常的问题 [#37386](https://github.com/pingcap/tidb/issues/37386) @[tiancaiamao](https://github.com/tiancaiamao)
    - 修复无法处理典型 MySQL 协议中 `prepared` 语句 flag 的问题  [#36731](https://github.com/pingcap/tidb/issues/36731) @[dveeden](https://github.com/dveeden)
    - 修复在极端情况下，启动 TiDB 可能进入错误状态的问题 [#36791](https://github.com/pingcap/tidb/issues/36791) @[xhebox](https://github.com/xhebox)
    - 修复 `INFORMATION_SCHEMA.VARIABLES_INFO` 不遵循安全增强模式 (SEM) 的问题 [#37586](https://github.com/pingcap/tidb/issues/37586) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - 修复带 UNION 算子的查询中转换字符串出错的问题 [#31678](https://github.com/pingcap/tidb/issues/31678) @[cbcwestwolf](https://github.com/cbcwestwolf)
    - 修复在 TiFlash 中为分区表开启动态模式时结果出错的问题 [#37254](https://github.com/pingcap/tidb/issues/37254) @[wshwsh12](https://github.com/wshwsh12)
    - 修复 TiDB 中二进制字符串和 JSON 之间的转换和对比行为与 MySQL 不兼容的问题 [#31918](https://github.com/pingcap/tidb/issues/31918) [#25053](https://github.com/pingcap/tidb/issues/25053) @[YangKeao](https://github.com/YangKeao)
    - 修复 TiDB 中的 `JSON_OBJECTAGG` 和 `JSON_ARRAYAGG` 在二进制值上与 MySQL 不兼容的问题 [#25053](https://github.com/pingcap/tidb/issues/25053) @[YangKeao](https://github.com/YangKeao)
    - 修复比较 JSON opaque 值时造成崩溃的问题 [#37315](https://github.com/pingcap/tidb/issues/37315) @[YangKeao](https://github.com/YangKeao)
    - 修复 JSON 聚合函数不能使用单精度浮点数的问题 [#37287](https://github.com/pingcap/tidb/issues/37287) @[YangKeao](https://github.com/YangKeao)
    - 修复 `UNION` 运算符可能会非预期地返回空结果的问题 [#36903](https://github.com/pingcap/tidb/issues/36903) @[tiancaiamao](https://github.com/tiancaiamao)
    - 修复 `castRealAsTime` 表达式的结果和 MySQL 不兼容的问题 [#37462](https://github.com/pingcap/tidb/issues/37462) @[mengxin9014](https://github.com/mengxin9014)
    - 修复悲观 DML 操作锁定非唯一索引键的问题 [#36235](https://github.com/pingcap/tidb/issues/36235) @[ekexium](https://github.com/ekexium)
    - 修复与自动提交 (auto-commit) 模式更改相关的事务提交行为 [#36581](https://github.com/pingcap/tidb/issues/36581) @[cfzjywxk](https://github.com/cfzjywxk)
    - 修复带 DML 算子的 `EXPLAIN ANALYZE` 语句可能在事务提交完成前返回结果的问题 [#37373](https://github.com/pingcap/tidb/issues/37373) @[cfzjywxk](https://github.com/cfzjywxk)
    - 修复在某些情况下 `UPDATE` 语句错误地消除了 projection 导致 `Can't find column` 报错的问题 [#37568](https://github.com/pingcap/tidb/issues/37568) @[AilinKid](https://github.com/AilinKid)
    - 修复执行 Join Reorder 操作时，会错误地下推 Outer Join 条件的问题 [#37238](https://github.com/pingcap/tidb/issues/37238) @[AilinKid](https://github.com/AilinKid)
    - 修复 `IN` 和 `NOT IN` 子查询在某些 pattern 下会报 `Can't find column` 的问题 [#37032](https://github.com/pingcap/tidb/issues/37032) @[AilinKid](https://github.com/AilinKid)
    - 修复 `UPDATE` 语句中带公共表表达式 (CTE) 的情况下会报 `Can't find column` 的问题 [#35758](https://github.com/pingcap/tidb/issues/35758) @[AilinKid](https://github.com/AilinKid)
    - 修复错误的 `PromQL` [#35856](https://github.com/pingcap/tidb/issues/35856) @[Defined2014](https://github.com/Defined2014)

+ TiKV

    - 修复 PD Region heartbeat 连接异常中断后未重新连接的问题 [#12934](https://github.com/tikv/tikv/issues/12934) @[bufferflies](https://github.com/bufferflies)
    - 修复 Raftstore 线程繁忙时，可能会出现 Region 重叠的问题 [#13160](https://github.com/tikv/tikv/issues/13160) @[5kbpers](https://github.com/5kbpers)
    - 修复 PD 客户端可能会出现死锁的问题 [#13191](https://github.com/tikv/tikv/issues/13191) @[bufferflies](https://github.com/bufferflies) [#12933](https://github.com/tikv/tikv/issues/12933) @[BurtonQin](https://github.com/BurtonQin)
    - 修复关闭加密时 TiKV panic 的问题 [#13081](https://github.com/tikv/tikv/issues/13081) @[jiayang-zheng](https://github.com/jiayang-zheng)
    - 修复 Dashboard 中 Unified Read Pool CPU 表达式错误的问题 [#13086](https://github.com/tikv/tikv/issues/13086) @[glorv](https://github.com/glorv)
    - 修复当有一个 TiKV 实例出现网络隔离时，一段时间内服务不可用问题 [#12966](https://github.com/tikv/tikv/issues/12966) @[cosven](https://github.com/cosven)
    - 修复误报 `PessimisticLockNotFound` 的问题 [#13425](https://github.com/tikv/tikv/issues/13425) @[sticnarf](https://github.com/sticnarf)
    - 修复某些场景下 PITR 可能丢失数据的问题 [#13281](https://github.com/tikv/tikv/issues/13281) @[YuJuncen](https://github.com/YuJuncen)
    - 修复存在时间较长的悲观事务时，checkpoint 没有推进的问题 [#13304](https://github.com/tikv/tikv/issues/13304) @[YuJuncen](https://github.com/YuJuncen)
    - 修复 TiKV 无法区分 JSON 中时间类型（`DATETIME`、`DATE`、`TIMESTAMP` 和 `TIME`）和 `STRING` 类型的问题 [#13417](https://github.com/tikv/tikv/issues/13417) @[YangKeao](https://github.com/YangKeao)
    - 修复 JSON bool 和其他 JSON value 的比较行为与 MySQL 不兼容的问题 [#13386](https://github.com/tikv/tikv/issues/13386) [#37481](https://github.com/pingcap/tidb/issues/37481) @[YangKeao](https://github.com/YangKeao)

+ PD

    - 修复开启 `enable-forwarding` 时，gRPC 处理返回错误不当导致 PD panic 的问题 [#5373](https://github.com/tikv/pd/issues/5373) @[bufferflies](https://github.com/bufferflies)
    - 修复不健康的 Region 可能导致 PD panic 的问题 [#5491](https://github.com/tikv/pd/issues/5491) @[nolouch](https://github.com/nolouch)
    - 修复 PD 可能没创建 TiFlash Learner 副本的问题 [#5401](https://github.com/tikv/pd/issues/5401) @[HunDunDM](https://github.com/HunDunDM)

+ TiFlash

    - 修复取消查询时 window function 可能会导致 TiFlash 崩溃的问题 [#5814](https://github.com/pingcap/tiflash/issues/5814) @[SeaRise](https://github.com/SeaRise)
    - 修复 `CAST(value AS datetime)` 输入数据无法转成 `DATETIME` 时会导致 TiFlash sys CPU 异常高的问题 [#5097](https://github.com/pingcap/tiflash/issues/5097) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - 修复 `CAST(Real/Decimal AS time)` 函数执行结果与 MySQL 不一致的问题 [#3779](https://github.com/pingcap/tiflash/issues/3779) @[mengxin9014](https://github.com/mengxin9014)
    - 修复存储中的过时数据可能无法删除的问题 [#5570](https://github.com/pingcap/tiflash/issues/5570) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复 page GC 可能导致无法创建表格的问题 [#5697](https://github.com/pingcap/tiflash/issues/5697) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复使用包含 `NULL` 值的列创建主键时导致崩溃的问题 [#5859](https://github.com/pingcap/tiflash/issues/5859) @[JaySon-Huang](https://github.com/JaySon-Huang)

+ Tools

    + Backup & Restore (BR)

        - 修复导致 PITR 的 checkpoint 信息过时的问题 [#36423](https://github.com/pingcap/tidb/issues/36423) @[YuJuncen](https://github.com/YuJuncen)
        - 修复在恢复时配置过高的 concurrency 会导致 Region 不均衡的问题 [#37549](https://github.com/pingcap/tidb/issues/37549) @[3pointer](https://github.com/3pointer)
        - 修复在 TiCDC 存在时，PITR 进度无法推进的问题 [#37822](https://github.com/pingcap/tidb/issues/37822) @[YuJuncen](https://github.com/YuJuncen)
        - 修复当外部存储的鉴权 Key 中存在某些特殊符号时，会导致备份恢复失败的问题 [#37469](https://github.com/pingcap/tidb/issues/37469) @[MoCuishle28](https://github.com/MoCuishle28)

    + TiCDC

        - 修复 TiCDC 对含有 grpc 服务的非法 PD 地址报错不准确的问题 [#6458](https://github.com/pingcap/tiflow/issues/6458) @[crelax](https://github.com/crelax)
        - 修复 `cdc cli changefeed list` 命令不返回 failed changefeed 的问题 [#6334](https://github.com/pingcap/tiflow/issues/6334) @[asddongmen](https://github.com/asddongmen)
        - 修复如果 changefeed 初始化失败会导致 TiCDC 不可用的问题 [#6859](https://github.com/pingcap/tiflow/issues/6859) @[asddongmen](https://github.com/asddongmen)

    + TiDB Binlog

        - 修复 compressor 设为 `gzip` 时 Drainer 无法正确发送请求至 Pump 的问题 [#1152](https://github.com/pingcap/tidb-binlog/issues/1152) @[lichunzhu](https://github.com/lichunzhu)

    + TiDB Data Migration (DM)

        - 修复 DM 报错 `Specified key was too long` 的问题 [#5315](https://github.com/pingcap/tiflow/issues/5315) @[lance6716](https://github.com/lance6716)
        - 修复 relay 报错时可能导致 goroutine 泄露问题 [#6193](https://github.com/pingcap/tiflow/issues/6193) @[lance6716](https://github.com/lance6716)
        - 修复当 `collation_compatible` 设置为 `"strict"` 时，DM 可能生成有重复排序规则的 SQL 语句的问题 [#6832](https://github.com/pingcap/tiflow/issues/6832) @[lance6716](https://github.com/lance6716)
        - 修复 DM-worker 日志中出现过多警告信息 "found error when get timezone from binlog status_vars" 的问题 [#6628](https://github.com/pingcap/tiflow/issues/6628) @[lyzx2001](https://github.com/lyzx2001)
        - 修复数据同步过程中，latin1 字符集数据可能损坏的问题 [#7028](https://github.com/pingcap/tiflow/issues/7028) @[lance6716](https://github.com/lance6716)

    + TiDB Lightning

        - 修复 TiDB Lightning 不支持 Parquet 文件中以斜线 (`/`)、数字、非 ASCII 字符开头的特殊列名的问题 [#36980](https://github.com/pingcap/tidb/issues/36980) @[D3Hunter](https://github.com/D3Hunter)

## 贡献者

感谢来自 TiDB 社区的贡献者们：

- @[An-DJ](https://github.com/An-DJ)
- @[AnnieoftheStars](https://github.com/AnnieoftheStars)
- @[AntiTopQuark](https://github.com/AntiTopQuark)
- @[blacktear23](https://github.com/blacktear23)
- @[BurtonQin](https://github.com/BurtonQin)（首次贡献者）
- @[crelax](https://github.com/crelax)
- @[eltociear](https://github.com/eltociear)
- @[fuzhe1989](https://github.com/fuzhe1989)
- @[erwadba](https://github.com/erwadba)
- @[jianzhiyao](https://github.com/jianzhiyao)
- @[joycse06](https://github.com/joycse06)
- @[morgo](https://github.com/morgo)
- @[onlyacat](https://github.com/onlyacat)
- @[peakji](https://github.com/peakji)
- @[rzrymiak](https://github.com/rzrymiak)
- @[tisonkun](https://github.com/tisonkun)
- @[whitekeepwork](https://github.com/whitekeepwork)
- @[Ziy1-Tan](https://github.com/Ziy1-Tan)
