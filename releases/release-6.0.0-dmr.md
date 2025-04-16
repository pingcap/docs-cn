---
title: TiDB 6.0.0 Release Notes
---

# TiDB 6.0.0 Release Notes

发版日期：2022 年 4 月 7 日

TiDB 版本：6.0.0-DMR

> **注意：**
>
> TiDB 6.0.0-DMR 的用户文档已[归档](https://docs-archive.pingcap.com/zh/tidb/v6.0)。如无特殊需求，建议使用 TiDB 数据库的[最新 LTS 版本](https://docs.pingcap.com/zh/tidb/stable)。

在 6.0.0-DMR 版本中，你可以获得以下关键特性：

- 基于 SQL 的数据放置规则，提供更灵活的数据放置管理能力。
- 内核层面的数据索引一致性检查，通过极低的资源开销提升系统稳定性和健壮性。
- 面向非专家的性能诊断功能 Top SQL，提供一体化、自助的数据库性能观测及诊断能力。
- 支持持续性能分析，持续记录集群的故障现场性能数据，缩短技术专家故障诊断时间。
- 热点小表缓存，大幅提高访问性能，提升吞吐，降低访问延迟。
- 内存悲观锁优化，在悲观锁性能瓶颈下，可以有效降低 10% 延迟，提升 10% QPS。
- 增强 Prepared Statement 执行计划共享，降低 CPU 资源消耗，提升 SQL 执行效率。
- 提升 MPP 引擎计算性能，支持更多表达式下推，正式引入弹性线程池。
- 新增 DM WebUI，方便地通过图形化的方式管理大量迁移任务。
- 提升 TiCDC 在大规模集群下同步数据的稳定性和资源利用效率，支持高达 10 万张表的同时同步。
- TiKV 节点重启后 leader 平衡加速，提升业务恢复速度。
- 支持手动取消统计信息的自动更新，减少资源争抢，降低对业务 SQL 性能的影响。
- PingCAP Clinic 自动诊断服务（Technical Preview 版本）
- TiDB Enterprise Manager 企业级数据库管理平台

另：作为 TiDB HTAP 方案的核心组件，TiFlash<sup>TM</sup> 于本次发布同时正式开放源码。详见 [GitHub](https://github.com/pingcap/tiflash)。

## 版本策略变更

从 TiDB v6.0.0 开始，TiDB 的发版会有两个系列：

- 长期支持版本 (Long-Term Support Releases)

    长期支持版本约每六个月发布一次，会引入新的功能和改进，并会按需在版本生命周期内发布 Bug 修订版本。例如：v6.1.0。

- 开发里程碑版 (Development Milestone Releases, DMR)

    DMR 版本约每两个月发布一次，会引入新的功能和改进。TiDB 不提供基于 DMR 的 Bug 修订版本，不推荐在生产环境使用。例如：v6.0.0-DMR。

v6.0.0 是 DMR 版本，版本名称为 6.0.0-DMR。

## 新功能

### SQL

- 基于 SQL 的数据放置规则

    TiDB 是具有优秀扩展能力的分布式数据库，通常数据横跨多个服务器甚至多数据中心部署，数据调度管理是 TiDB 最重要的基础能力之一。大多数情况下用户无需关心数据如何调度管理，但是随着业务复杂度的提升，因隔离性和访问延迟导致的数据部署变更是 TiDB 面对的新的挑战。TiDB 从 6.0.0 版本开始正式提供基于 SQL 接口的数据调度管理能力，支持针对任意数据提供副本数、角色类型、放置位置等维度的灵活调度管理能力，在多业务共享集群、跨 AZ 部署下提供更灵活的数据放置管理能力。

    [用户文档](/placement-rules-in-sql.md)

- 新增按库构建 TiFlash 副本功能。用户仅需使用一条 SQL 即可对某一个数据库中所有的表添加 TiFlash 副本，极大地节约了运维成本。

    [用户文档](/tiflash/create-tiflash-replicas.md#按库构建-tiflash-副本)

### 事务

- 内核层面增加数据索引一致性检查

    在事务执行过中增加数据索引一致性检查，通过极低的资源开销提升系统稳定性和健壮性。你可以通过 `tidb_enable_mutation_checker` 和 `tidb_txn_assertion_level` 参数控制检查行为。默认配置下，大多数场景下 QPS 下降控制在 2% 以内。关于数据索引一致性检查的报错说明，请参考[用户文档](/troubleshoot-data-inconsistency-errors.md)。

### 可观测性

- Top SQL：面向非专家的 SQL 性能诊断功能

    Top SQL 是一个面向运维人员及应用开发者的一体化、自助的数据库性能观测和诊断功能，集成于 TiDB Dashboard 图形化界面，在 TiDB v6.0.0 正式发布。

    与现有 TiDB Dashboard 中各个面向数据库专家的诊断功能不同的是，Top SQL 完全面向非专家：你不需要观察几千张监控图表寻找相关性，也不需要理解诸如 Raft Snapsnot、RocksDB、MVCC、TSO 等 TiDB 内部机制，仅需要知道常见的数据库概念，如索引、锁冲突、执行计划等，就可以通过 Top SQL 快速分析数据库负载情况，并提升应用程序的性能。

    Top SQL 功能功能默认关闭。启用后，通过 Top SQL 提供的各个 TiDB 或 TiKV 节点实时 CPU 负载情况，你可以直观了解各节点的高 CPU 负载来自哪些 SQL 语句，从而快速分析诸如数据库热点和负载陡升等问题。例如，你可以通过 Top SQL 分析某个 TiKV 节点上正在消耗 90% CPU 负载的 SQL 查询语句的具体内容及执行情况。

    [用户文档](/dashboard/top-sql.md)

- 持续性能分析

    持续性能分析 (Continuous Profiling) 功能集成于 TiDB Dashboard，在 TiDB v6.0.0 中正式发布。该功能默认关闭，启用该功能后，集群将以极低的开销自动收集各 TiDB、TiKV 及 PD 实例每时每刻的性能数据。通过这些历史性能数据，技术专家可以在事后回溯、分析该集群任意时刻（如曾经出现过高内存占用）的问题根因，无需等待问题复现，从而有助于缩短故障诊断时间。

    [用户文档](/dashboard/continuous-profiling.md)

### 性能

- 热点小表缓存

    用户业务遇到热点小表访问场景下，支持显式将热点表缓存于内存中，大幅提高访问性能，提升吞吐，降低访问延迟。该方案可以有效避免引入三方缓存中间件，降低架构复杂性，减少运维管理成本，适用于高频访问低频更新的小表场景，例如配置表，汇率表等。

    [用户文档](/cached-tables.md)，[#25293](https://github.com/pingcap/tidb/issues/25293)

- 内存悲观锁优化

    TiDB 从 v6.0.0 开始默认开启内存悲观锁功能。开启后，悲观事务锁管理将在内存中完成，避免悲观锁持久化，也避免了锁信息的 Raft 复制，大大降低悲观事务锁管理的开销。在悲观锁性能瓶颈下，通过悲观锁内存优化，可以有效降低 10% 延迟，提升 10% QPS。

    [用户文档](/pessimistic-transaction.md#内存悲观锁)，[#11452](https://github.com/tikv/tikv/issues/11452)

- RC 隔离级别下优化 TSO 获取开销

    在 [RC 隔离级别](/transaction-isolation-levels.md#读已提交隔离级别-read-committed)下，增加 `tidb_rc_read_check_ts` 变量，用于在读写冲突较少情况下，减少不必要 TSO 获取，从而降低查询延迟。该参数默认关闭，开启后，在没有读写冲突的场景下，该优化几乎可以避免重复 TSO 获取，降低延迟。但是在高读写冲突场景下，开启该参数有可能造成性能回退，请验证后使用。

    [用户文档](/transaction-isolation-levels.md#读已提交隔离级别-read-committed)，[#33159](https://github.com/pingcap/tidb/issues/33159)

- 增强 Prepared Statement 执行计划共享

    SQL 执行计划复用可以有效减少 SQL 解析时间，降低 CPU 资源消耗，提升 SQL 执行效率。有效复用 SQL 执行计划是 SQL 调优的重要手段之一。TiDB 已经支持 Prepared Statement 下的计划共享。但是在 Prepared Statement close 时，TiDB 会主动清空对应的 Plan Cache。这会对重复执行的 SQL 造成不必要的解析，影响语句的执行效率。TiDB 从 v6.0.0 开始支持通过 `tidb_ignore_prepared_cache_close_stmt` 参数控制是否忽视 `COM_STMT_CLOSE` 指令，该参数默认关闭。开启该参数后，TiDB 可以忽视 Prepared Statement 的 close 指令，并在缓存中保留对应的执行计划，从而提升执行计划的复用率。

    [用户文档](/sql-prepared-plan-cache.md#忽略-com_stmt_close-指令和-deallocate-prepare-语句)，[#31056](https://github.com/pingcap/tidb/issues/31056)

- 增强查询的下推功能

    TiDB 是原生计算存储分离架构，算子下推可以在存储层过滤无效数据，大大减少 TiDB 与 TiKV 的数据传输，提升查询效率。TiDB 在 v6.0.0 支持更多的表达式和 `BIT` 数据类型下推至 TiKV，以提升运算该类内容时的查询效率。

    [用户文档](/functions-and-operators/expressions-pushed-down.md)，[#30738](https://github.com/pingcap/tidb/issues/30738)

- 热点索引优化

    在二级索引上批量写入单调递增的值会形成索引热点，影响整体写入吞吐。自 v6.0.0 起，TiDB 支持通过 `tidb_shard` 函数将热点索引打散，以提升写入性能。目前 `tidb_shard` 只能打散二级唯一索引的热点。该方案不需要用户修改原有查询条件，对业务非常友好，适用于高吞吐写入、点查询、批量点查询场景。请注意如果业务中使用范围查询打散后的数据，可能造成性能回退，请验证后使用。

    [用户文档](/functions-and-operators/tidb-functions.md#tidb_shard)，[#31040](https://github.com/pingcap/tidb/issues/31040)

- TiFlash MPP 引擎支持分区表的动态裁剪模式（实验特性）

    在该模式下，TiDB 也可以使用 TiFlash MPP 引擎读取和计算分区表的数据，从而大大提升分区表的查询性能。

    [用户文档](/tiflash/use-tiflash-mpp-mode.md#mpp-模式访问分区表)

- 持续提升 MPP 引擎计算性能

    - 支持更多函数和算子下推至 MPP 引擎

        - 逻辑函数： `IS`，`IS NOT`
        - 字符串函数：`REGEXP()`，`NOT REGEXP()`
        - 数学函数：`GREATEST(int/real)`，`LEAST(int/real)`
        - 日期函数：`DAYNAME()`，`DAYOFMONTH()`，`DAYOFWEEK()`，`DAYOFYEAR()`，`LAST_DAY()`，`MONTHNAME()`
        - 算子：Anti Left Outer Semi Join, Left Outer Semi Join

        [用户文档](/tiflash/tiflash-supported-pushdown-calculations.md)

    - 正式引入弹性线程池，提升 CPU 利用率，默认开启此功能

        [用户文档](/tiflash/tiflash-configuration.md#配置文件-tiflashtoml)

### 稳定性

- 执行计划自动捕获增强

    增强了执行计划自动捕获的易用性，增加了黑名单功能，支持表名、频率和用户名三个维度的黑名单设置。引入新的算法来优化绑定缓存的内存管理机制。开启自动捕获后，可以为绝大多数 OLTP 类查询自动创建绑定，从而固定被绑定语句的执行计划，避免因执行计划变动导致的性能问题。通常用于大版本升级和集群迁移等场景，可以有效减少因计划回退造成的性能问题。

    [用户文档](/sql-plan-management.md#自动捕获绑定-baseline-capturing)，[#32466](https://github.com/pingcap/tidb/issues/32466)

- TiKV 过载资源保护增强 (实验特性）

    当 TiKV 部署的机型资源受限时，如果前台处理的读写请求量过大，会导致后台处理请求的 CPU 资源被前台占用，最终影响 TiKV 性能的稳定性。TiDB v6.0.0 支持手动限制 TiKV 前台各类请求的资源用量，包括 CPU、读写带宽等，以提升集群在长期高负载压力下的稳定性。

    [用户文档](/tikv-configuration-file.md#quota)，[#12131](https://github.com/tikv/tikv/issues/12131)

- TiFlash 新增支持 zstd 压缩算法

    新增 `profiles.default.dt_compression_method` 和 `profiles.default.dt_compression_level` 两个参数，用户可根据对性能和容量的平衡，选择不同的压缩算法。

    [用户文档](/tiflash/tiflash-configuration.md#配置文件-tiflashtoml)

- TiFlash 默认开启支持所有 I/O 的校验 (Checksum)。

    此项功能曾作为实验特性在 v5.4 释出。除增强了数据的正确性安全性外，对用户使用不产生明显的直接影响。

    警告：新版本数据格式将不支持原地降级为早于 v5.4 的版本，需要在降级处理时删除 TiFlash Replica 待降级完成后重新同步；或使用[离线工具进行数据版本降级](/tiflash/tiflash-command-line-flags.md#dttool-migrate)。

    [用户文档](/tiflash/tiflash-data-validation.md)

- TiFlash 引入异步 gRPC 和 Min-TSO 调度机制，更好的管理线程使用，防止线程数过高导致的系统崩溃。

    [用户文档](/tiflash/monitor-tiflash.md#coprocessor)

### 数据迁移

#### DM

- WebUI（实验特性）

    新增 WebUI 方便地通过图形化的方式管理大量迁移任务。已支持的功能有：

    - 在 Dashboard 上显示迁移任务信息
    - 管理迁移任务
    - 配置上游参数
    - 查询同步状态
    - 查看 Master 和 Worker 信息

    此特性为实验性，尚存在不完善之处。建议仅用于体验，且已知与 dmctl 操作同一任务可能存在问题，此现象将于后续版本改进。

    [用户文档](/dm/dm-webui-guide.md)

- 增强错误处理机制

    当迁移任务中断时，增加更多命令以方便的解决遇到的错误。例如：

    - 遇到 schema 错误时，可以通过 `binlog-schema update` 命令的 `--from-source`/`--from-target` 参数直接更新，无需单独编写 schema 文件。
    - 可以指定某个 binlog position，inject/replace/skip/revert DDL 语句。

    [用户文档](/dm/dm-manage-schema.md)

- 支持存储全量数据至 Amazon S3

    DM 执行 all/full 类型的迁移任务时，需要足够的硬盘空间存放上游的全量数据。相比 EBS，Amazon S3 具有更低的成本和近似无限的容量。DM 现在可以将 dump 目录配置为 Amazon S3 路径，执行 all/full 类型的迁移任务时则直接使用 Amazon S3 存放全量数据。

    [用户文档](/dm/task-configuration-file-full.md#完整配置文件示例)

- 支持从指定的时间点启动迁移任务

    启动任务时新增了参数 `--start-time`，支持 `'2021-10-21 00:01:00'` 或 `'2021-10-21T00:01:00'` 格式的自定义时间。

    此特性在多个 MySQL 实例合并增量迁移场景尤其有用，无需为每个上游增量同步设置 binlog 起始位置，而是通过 `--start-time` 参数配合 safe-mode 即可更快的完成增量任务配置。

    [用户文档](/dm/dm-create-task.md#参数解释)

#### TiDB Lightning

- 最大可容忍错误

    增加 `lightning.max-error` 配置项，默认值为 0 以保持原有行为。当值 > 0 时，表示 max-error 功能开启。Lightning 在进行编码时，如果出现报错，则会在目标 TiDB 的 `lightning_task_info.type_error_v1` 表中增加一条记录包含此报错行的信息，并忽略此行；当出现的报错行数超过配置值时 Lightning 将立即退出。

    与之相匹配的配置项 `lightning.task-info-schema-name` 用于定义保存出错数据记录的库名。

    此特性尚不能涵盖所有类型的错误，例如 syntax error。

    [用户文档](/tidb-lightning/tidb-lightning-error-resolution.md#类型错误-type-error)

### TiDB 数据共享订阅

- 支持高达 10 万张表的同时同步

    TiCDC 针对数据处理流程进行了优化，降低了处理每张表增量数据时所需要的资源，极大地提升了 TiCDC 在大规模集群下同步数据的稳定性和资源利用效率。在测试中，TiCDC 可以稳定支持 10 万张表的增量数据的同时同步。

### 部署及运维

- 默认采用新 Collation 规则

    TiDB 从 v4.0 开始支持新 collation 规则，在大小写不敏感、口音不敏感、padding 规则上与 MySQL 行为保持一致。新 Collation 规则可以通过 `new_collations_enabled_on_first_bootstrap` 参数控制，默认关闭。从 v6.0.0 开始，TiDB 默认开启新 Collation 规则，请注意该配置仅在集群初始化时生效。

    [用户文档](/tidb-configuration-file.md#new_collations_enabled_on_first_bootstrap)

- TiKV 节点重启后 leader 平衡加速

    TiKV 节点重启后，需要将分布不均匀的 leader 重分配以达到负载均衡的效果。在大规模集群下，leader 平衡时间与 Region 数量正相关。例如，在 100K Region 下，leader 平衡耗时可能达到 20-30 分钟，容易引发负载不均导致的性能问题，造成稳定性风险。TiDB v6.0.0 提供了 leader 平衡的并发度参数控制，并调整默认值为原来的 4 倍，大幅缩短 leader 重平衡的时间，提升 TiKV 节点重启后的业务恢复速度。

    [用户文档](/pd-control.md#scheduler-config-balance-leader-scheduler)，[#4610](https://github.com/tikv/pd/issues/4610)

- 支持手动取消统计信息的自动更新

    统计信息是影响 SQL 性能的最重要基础数据之一，为了保证统计信息的完整性和及时性，TiDB 会在后台定期自动更新对象的统计信息。但是，统计信息自动更新可能造成资源争抢，影响业务 SQL 性能。为了避免这个问题，TiDB v6.0.0 支持手动取消统计信息的自动更新。

    [用户文档](/statistics.md#自动更新)

- PingCAP Clinic 诊断服务 Technical Preview 版本上线

    [PingCAP Clinic](https://clinic.pingcap.com.cn) 为 TiDB 集群提供诊断服务，支持远程定位集群问题和本地快速检查集群状态，用于从全生命周期确保 TiDB 集群稳定运行、预测可出现的集群问题、降低问题出现概率、快速定位并修复问题。

    当 TiDB 集群出现问题，需要邀请 PingCAP 技术支持人员协助定位问题时，你可以通过 PingCAP Clinic 服务采集并上传诊断数据，从而大大提高定位问题的速度。

    [用户文档](/clinic/clinic-introduction.md)

- 企业级数据库管理平台 TiDB Enterprise Manager

    TiDB Enterprise Manager 是一款以 TiDB 数据库为核心的企业级数据库管理平台，帮助用户在本地部署环境或公有云环境中管理 TiDB 集群。

    TiDB Enterprise Manager 不仅为 TiDB 集群提供全生命周期的可视化管理，也同时一站式提供 TiDB 数据库的参数管理、数据库版本升级、克隆集群、主备集群切换、数据导入导出、数据同步、数据备份恢复服务，能有效提高 TiDB 集群运维效率，降低企业运维成本。

    TiDB Enterprise Manager 当前为企业版特性。要获取 TiDB Enterprise Manager 及其文档，请在 [TiDB 产品页面](https://pingcap.com/zh/product/#SelectProduct)**企业版**下点击**立即咨询**与 PingCAP 取得联系。

- 支持监控组件的自定义配置

    使用 TiUP 部署 TiDB 集群时，TiUP 会同时自动部署 Prometheus、Grafana 和 Alertmanager 等监控组件，并且在集群扩容中自动为新增节点添加监控配置。通过在 `topology.yaml` 文件中添加对应的配置项，你可以对监控组件进行自定义配置。

    [用户文档](/tiup/customized-montior-in-tiup-environment.md)

## 兼容性变化

> **注意：**
>
> 当从一个早期的 TiDB 版本升级到 TiDB v6.0.0 时，如需了解所有中间版本对应的兼容性更改说明，请查看对应版本的 [Release Notes](/releases/release-notes.md)。

### 系统变量

| 变量名 | 修改类型 | 描述 |
|:---|:---|:---|
| `placement_checks` | 删除 | 该变量用于控制 DDL 语句是否验证通过 [Placement Rules in SQL](/placement-rules-in-sql.md) 指定的放置规则。已被 `tidb_placement_mode` 替代。 |
| `tidb_enable_alter_placement` | 删除 | 该变量用于开启 [Placement Rules in SQL](/placement-rules-in-sql.md)。 |
| `tidb_mem_quota_hashjoin`<br/>`tidb_mem_quota_indexlookupjoin`<br/>`tidb_mem_quota_indexlookupreader` <br/>`tidb_mem_quota_mergejoin`<br/>`tidb_mem_quota_sort`<br/>`tidb_mem_quota_topn` | 删除 | 从 TiDB v5.0.0 起，这几个变量被 `tidb_mem_quota_query` 取代并从系统变量文档中移除，为了保证兼容性代码中还保留。从 TiDB v6.0.0 起，代码中也正式移除这些变量。 |
| [`tidb_enable_mutation_checker`](/system-variables.md#tidb_enable_mutation_checker-从-v600-版本开始引入) | 新增 | 设置是否开启 mutation checker，默认开启。如果从低于 v6.0.0 的版本升级到 v6.0.0，升级后默认关闭。 |
| [`tidb_ignore_prepared_cache_close_stmt`](/system-variables.md#tidb_ignore_prepared_cache_close_stmt-从-v600-版本开始引入) | 新增 | 设置是否忽略关闭 Prepared Statement 的指令，默认值为 `OFF`。 |
| [`tidb_mem_quota_binding_cache`](/system-variables.md#tidb_mem_quota_binding_cache-从-v600-版本开始引入) | 新增 | 设置存放 `binding` 的缓存的内存使用阈值，默认值为 `67108864` (64 MiB)。 |
| [`tidb_placement_mode`](/system-variables.md#tidb_placement_mode-从-v600-版本开始引入) | 新增 | 控制 DDL 语句是否忽略 [Placement Rules in SQL](/placement-rules-in-sql.md) 指定的放置规则。默认值为 `strict`，表示不忽略。 |
| [`tidb_rc_read_check_ts`](/system-variables.md#tidb_rc_read_check_ts-从-v600-版本开始引入) | 新增 | <ul><li> 优化事务内读语句延迟。如果读写冲突较为严重，开启此变量会增加额外开销和延迟，造成性能回退。默认关闭。</li><li>该变量与 [replica-read](/system-variables.md#tidb_replica_read-从-v40-版本开始引入) 尚不兼容，开启 `tidb_rc_read_check_ts` 的读请求无法使用 [replica-read](/system-variables.md#tidb_replica_read-从-v40-版本开始引入)，请勿同时开启两个变量。</li></ul> |
| [`tidb_sysdate_is_now`](/system-variables.md#tidb_sysdate_is_now-从-v600-版本开始引入) | 新增 | 控制 `SYSDATE` 函数是否替换为 `NOW` 函数，效果与 MySQL 中的 [`sysdate-is-now`](https://dev.mysql.com/doc/refman/8.0/en/server-options.html#option_mysqld_sysdate-is-now) 一致。默认值为 `OFF`。 |
| [`tidb_table_cache_lease`](/system-variables.md#tidb_table_cache_lease-从-v600-版本开始引入) | 新增 | 用来控制缓存表（新增 feature）的 lease 时间，默认值是 3 秒。 |
| [`tidb_top_sql_max_meta_count`](/system-variables.md#tidb_top_sql_max_meta_count-从-v600-版本开始引入) | 新增 | 用于控制 [Top SQL](/dashboard/top-sql.md) 每分钟最多收集 SQL 语句类型的数量，默认值为 `5000`。 |
| [`tidb_top_sql_max_time_series_count`](/system-variables.md#tidb_top_sql_max_time_series_count-从-v600-版本开始引入) | 新增 | 用于控制 [Top SQL](/dashboard/top-sql.md) 每分钟保留消耗负载最大的前多少条 SQL（即 Top N）的数据，默认值为 `100`。 |
| [`tidb_txn_assertion_level`](/system-variables.md#tidb_txn_assertion_level-从-v600-版本开始引入) | 新增 | 设置 assertion 级别，assertion 是一项在事务提交过程中进行的数据索引一致性校验。默认仅开启对性能影响微小的检查，包含大部分检查效果。如果从低于 v6.0.0 的版本升级到 v6.0.0，升级后默认关闭检查。 |

### 配置文件参数

| 配置文件 | 配置项 | 修改类型 | 描述 |
|:---|:---|:---|:---|
| TiDB | `stmt-summary.enable` <br/> `stmt-summary.enable-internal-query` <br/> `stmt-summary.history-size` <br/> `stmt-summary.max-sql-length` <br/> `stmt-summary.max-stmt-count` <br/> `stmt-summary.refresh-interval` | 删除 | 系统表 [statement summary tables](/statement-summary-tables.md) 的相关配置，所有配置项现已移除，统一改成用 SQL variable 控制。 |
| TiDB | [`new_collations_enabled_on_first_bootstrap`](/tidb-configuration-file.md#new_collations_enabled_on_first_bootstrap) | 修改 | 用于开启新的 collation 支持。自 v6.0.0 起默认值从 false 改为 true。该配置项只有在初次初始化集群时生效，初始化集群后，无法通过更改该配置项打开或关闭新的 collation 框架。 |
| TiKV | [`backup.num-threads`](/tikv-configuration-file.md#num-threads-1) | 修改 | 修改可调整范围为 `[1, CPU]`。 |
| TiKV | [`raftstore.apply-max-batch-size`](/tikv-configuration-file.md#apply-max-batch-size) | 修改 | 添加最大值为 `10240`。 |
| TiKV | [`raftstore.raft-max-size-per-msg`](/tikv-configuration-file.md#raft-max-size-per-msg) | 修改 | <ul><li>修改最小值（由 `0` 修改为大于 `0`）</li><li>添加最大值为 `3GB`</li><li>添加单位（由 `MB` 增加为 <code>KB\|MB\|GB</code>）</li></ul> |
| TiKV | [`raftstore.store-max-batch-size`](/tikv-configuration-file.md#store-max-batch-size) | 修改 | 添加最大值为 `10240`。 |
| TiKV | [`readpool.unified.max-thread-count`](/tikv-configuration-file.md#max-thread-count) | 修改 | 修改可调整范围为 `[min-thread-count, MAX(4, CPU)]`。 |
| TiKV | [`rocksdb.enable-pipelined-write`](/tikv-configuration-file.md#enable-pipelined-write) | 修改 | 修改默认值为 `false`。开启时会使用旧的 Pipelined Write，关闭时会使用新的 Pipelined Commit 机制。 |
| TiKV | [`rocksdb.max-background-flushes`](/tikv-configuration-file.md#max-background-flushes) | 修改 | 在 CPU 核数为 10 时修改默认值为 `3`，在 CPU 核数量为 8 时默认为 `2`。 |
| TiKV | [`rocksdb.max-background-jobs`](/tikv-configuration-file.md#max-background-jobs) | 修改 | 在 CPU 核数为 10 时修改默认值为 `9`，在 CPU 核数量为 8 时默认为 `7`。 |
| TiFlash | [`profiles.default.dt_enable_logical_split`](/tiflash/tiflash-configuration.md#配置文件-tiflashtoml) | 修改 | 存储引擎的 segment 分裂是否使用逻辑分裂。自 v6.0.0 起默认值从 `true` 改为 `false`。 |
| TiFlash | [`profiles.default.enable_elastic_threadpool`](/tiflash/tiflash-configuration.md#配置文件-tiflashtoml) | 修改 | 是否启用可自动扩展的线程池。自 v6.0.0 起默认值从 `false` 改为 `true`。 |
| TiFlash | [`storage.format_version`](/tiflash/tiflash-configuration.md#配置文件-tiflashtoml) | 修改 | 该配置项控制 TiFlash 存储引擎的校验功能，自 v6.0.0 起默认值从 `2` 改为 `3`。`format_version` 设置为 `3` 时， 支持对 TiFlash 的所有数据的读操作进行一致性校验，避免由于硬件故障而读到错误的数据。<br/>注意：新版本数据格式不支持原地降级为早于 5.4 的版本。 |
| TiDB | [`pessimistic-txn.pessimistic-auto-commit`](/tidb-configuration-file.md#pessimistic-auto-commit) | 新增 | 用来控制开启全局悲观事务模式下 (`tidb_txn_mode='pessimistic'`) 时，自动提交的事务使用的事务模式。 |
| TiKV | [`pessimistic-txn.in-memory`](/tikv-configuration-file.md#in-memory-从-v600-版本开始引入) | 新增 | 开启内存悲观锁功能。开启该功能后，悲观事务会尽可能在 TiKV 内存中存储悲观锁，而不将悲观锁写入磁盘，也不将悲观锁同步给其他副本，从而提升悲观事务的性能。但有较低概率出现悲观锁丢失的情况，可能会导致悲观事务提交失败。该参数默认值为 `true`。 |
| TiKV | [`quota`](/tikv-configuration-file.md#quota) | 新增 | 新增前台限流相关的配置项，可以限制前台各类请求所占用的资源。前台限流功能为实验特性，默认关闭。新增的相关配置项为 `foreground-cpu-time`、`foreground-write-bandwidth`、`foreground-read-bandwidth`、`max-delay-duration`。 |
| TiFlash | [`profiles.default.dt_compression_method`](/tiflash/tiflash-configuration.md#配置文件-tiflashtoml) | 新增 | TiFlash 存储引擎的压缩算法，支持 LZ4、zstd 和 LZ4HC，大小写不敏感。默认使用 LZ4 算法。 |
| TiFlash | [`profiles.default.dt_compression_level`](/tiflash/tiflash-configuration.md#配置文件-tiflashtoml) | 新增 | TiFlash 存储引擎的压缩级别，默认值 `1`。 |
| DM | [`loaders.<name>.import-mode`](/dm/task-configuration-file-full.md#完整配置文件示例) | 新增 | 该配置项控制全量阶段数据导入的模式。自 v6.0.0 起全量阶段默认使用 TiDB Lightning 的 TiDB-backend 方式导入，替换原来的 Loader 组件。此变动为内部组件替换，对日常使用没有明显影响。<br/>默认值 `sql` 表示启用 tidb-backend 组件，可能在极少数场景下存在未能完全兼容的情况，可以通过配置为 "loader" 回退。 |
| DM | [`loaders.<name>.on-duplicate`](/dm/task-configuration-file-full.md#完整配置文件示例) | 新增 | 该配置项控制全量导入阶段出现的冲突数据的解决方式。默认值为 `replace`，覆盖重复数据。 |
| TiCDC | [`dial-timeout`](/ticdc/ticdc-sink-to-kafka.md#sink-uri-配置-kafka) | 新增 | 和下游 Kafka 建立连接的超时时长，默认值为 `10s` |
| TiCDC | [`read-timeout`](/ticdc/ticdc-sink-to-kafka.md#sink-uri-配置-kafka) | 新增 | 读取下游 Kafka 返回的 response 的超时时长，默认值 `10s` |
| TiCDC | [`write-timeout`](/ticdc/ticdc-sink-to-kafka.md#sink-uri-配置-kafka) | 新增 | 向下游 Kafka 发送 request 的超时时长，默认值为 `10s` |

### 其他

- 数据放置策略的兼容性变更：
    - 不支持绑定，并从语法中删除直接放置 (direct placement) 选项。
    - `CREATE PLACEMENT POLICY` 和 `ALTER PLACEMENT POLICY` 语句不再支持 `VOTERS` 和 `VOTER_CONSTRAINTS` 放置选项。
    - TiDB 数据迁移工具（TiDB Binlog、TiCDC、BR）现在兼容 placement rules。Placement 选项移到 binlog 的特殊注释中。
    - 系统表 `information_schema.placement_rules` 重命名为 `information_schema.placement_policies`。此表现在只展示放置策略的信息。
    - 系统变量 `placement_checks` 被 `tidb_placement_mode` 替代。
    - 禁止在有 TiFlash 副本的表上添加带放置规则的分区。
    - 将 `TIDB_DIRECT_PLACEMENT` 列从 `INFORMATION_SCHEMA` 表中删除。
- 执行计划管理（SPM）绑定的 status 值变更：
    - 删除 `using`。
    - 新增 `enabled`（可用），取代之前版本的 `using` 状态。
    - 新增 `disabled`（不可用）。
- DM 修改 OpenAPI 接口
    - 由于内部机制变更，任务管理相关接口与之前的实验特性版本无法保持兼容，需要参阅新的 [OpenAPI 文档](/dm/dm-open-api.md)进行适配。
- DM 全量数据冲突处理方式变化
    - 新增 `loader.<name>.on-duplicate` 参数，默认值为 `replace`，表示覆盖冲突数据。若希望保持以前版本的行为，可以改为 `error`。此参数仅影响全量数据导入阶段的行为。
- DM 需使用对应版本的 dmctl 工具
    - 由于内部机制变更，升级 DM 集群版本至 v6.0.0 后，也必须升级 dmctl 与之匹配。
- 在 v5.4 及之前版本中，TiDB 允许将一些 noop 系统变量设置为不正确的值。从 v6.0.0 起，TiDB 不再允许将系统变量设置为不正确的值 [#31538](https://github.com/pingcap/tidb/issues/31538)

## 离线包变更

TiDB 提供两个[离线包下载](https://pingcap.com/zh/product-community/)：`v6.0.0 TiDB-community-server` 软件包和 `v6.0.0 TiDB-community-toolkit` 软件包。

在 6.0.0-DMR 版本中，两个离线包的内容物做了一些调整。在 `v6.0.0 TiDB-community-server` 软件包中，离线包的内容物包含：

* `tidb-{version}-linux-amd64.tar.gz`
* `tikv-{version}-linux-amd64.tar.gz`
* `tiflash-{version}-linux-amd64.tar.gz`
* `pd-{version}-linux-amd64.tar.gz`
* `ctl-{version}-linux-amd64.tar.gz`
* `grafana-{version}-linux-amd64.tar.gz`
* `alertmanager-{version}-linux-amd64.tar.gz`
* `blackbox_exporter-{version}-linux-amd64.tar.gz`
* `prometheus-{version}-linux-amd64.tar.gz`
* `node_exporter-{version}-linux-amd64.tar.gz`
* `tiup-linux-amd64.tar.gz`
* `tiup-{version}-linux-amd64.tar.gz`
* `local_install.sh`
* `cluster-{version}-linux-amd64.tar.gz`
* `insight-{version}-linux-amd64.tar.gz`
* `diag-{version}-linux-amd64.tar.gz`
* `influxdb-{version}-linux-amd64.tar.gz`
* `playground-{version}-linux-amd64.tar.gz`

在 `v6.0.0 TiDB-community-toolkit` 软件包中，离线包的内容物包含：

* `tikv-importer-{version}-linux-amd64.tar.gz`
* `pd-recover-{version}-linux-amd64.tar.gz`
* `etcdctl`
* `tiup-linux-amd64.tar.gz`
* `tiup-{version}-linux-amd64.tar.gz`
* `tidb-lightning-{version}-linux-amd64.tar.gz`
* `tidb-lightning-ctl`
* `dumpling-{version}-linux-amd64.tar.gz`
* `cdc-{version}-linux-amd64.tar.gz`
* `dm-{version}-linux-amd64.tar.gz`
* `dm-worker-{version}-linux-amd64.tar.gz`
* `dm-master-{version}-linux-amd64.tar.gz`
* `dmctl-{version}-linux-amd64.tar.gz`
* `br-{version}-linux-amd64.tar.gz`
* `spark-{version}-any-any.tar.gz`
* `tispark-{version}-any-any.tar.gz`
* `package-{version}-linux-amd64.tar.gz`
* `bench-{version}-linux-amd64.tar.gz`
* `errdoc-{version}-linux-amd64.tar.gz`
* `dba-{version}-linux-amd64.tar.gz`
* `PCC-{version}-linux-amd64.tar.gz`
* `pump-{version}-linux-amd64.tar.gz`
* `drainer-{version}-linux-amd64.tar.gz`
* `binlogctl`
* `sync_diff_inspector`
* `reparo`
* `arbiter`
* `mydumper`

## 提升改进

+ TiDB

    - 当通过 `FLASHBACK` 或 `RECOVER` 语句恢复一张表之后，自动清除该表的放置规则信息 [#31668](https://github.com/pingcap/tidb/issues/31668)
    - 新增一个性能概览监控面板，展示典型关键路径上的核心性能指标，使 TiDB 上的指标分析更加容易 [#31676](https://github.com/pingcap/tidb/issues/31676)
    - 支持在 `LOAD DATA LOCAL INFILE` 语句中使用 `REPLACE` 关键字 [#24515](https://github.com/pingcap/tidb/issues/24515)
    - 支持在 Range 类型分区表中对 `IN` 表达式进行分区裁剪 [#26739](https://github.com/pingcap/tidb/issues/26739)
    - 消除 MPP 聚合查询中可能冗余的 Exchange 操作，提高查询效率 [#31762](https://github.com/pingcap/tidb/issues/31762)
    - 允许在 `TRUNCATE PARTITION` 和 `DROP PARTITION` 语句中使用重复的分区名，提高与 MySQL 的兼容性 [#31681](https://github.com/pingcap/tidb/issues/31681)
    - 支持在 `ADMIN SHOW DDL JOBS` 语句的执行结果中显示 `​​CREATE_TIME` 信息 [#23494](https://github.com/pingcap/tidb/issues/23494)
    - 新增内置函数 `CHARSET()` [#3931](https://github.com/pingcap/tidb/issues/3931)
    - 支持通过用户名过滤自动捕获的黑名单 [#32558](https://github.com/pingcap/tidb/issues/32558)
    - 支持在自动捕获的黑名单中使用通配符 [#32714](https://github.com/pingcap/tidb/issues/32714)
    - 优化 `ADMIN SHOW DDL JOBS` 和 `SHOW TABLE STATUS` 语句的执行结果，支持根据当前的 `time_zone` 显示结果中的时间 [#26642](https://github.com/pingcap/tidb/issues/26642​​)
    - 支持下推 `DAYNAME()`和 `MONTHNAME()` 函数到 TiFlash [#32594](https://github.com/pingcap/tidb/issues/32594)
    - 支持下推 `REGEXP` 函数到 TiFlash [#32637](https://github.com/pingcap/tidb/issues/32637)
    - 支持下推 `DAYOFMONTH()`，`LAST_DAY()` 函数到 TiFlash [#33012](https://github.com/pingcap/tidb/issues/33012)
    - 支持下推 `DAYOFWEEK()` 和 `DAYOFYEAR()` 函数到 TiFlash [#33130](https://github.com/pingcap/tidb/issues/33130)
    - 支持下推 `IS_TRUE`、`IS_FALSE`、`IS_TRUE_WITH_NULL` 函数到 TiFlash [#33047](https://github.com/pingcap/tidb/issues/33047)
    - 支持下推 `GREATEST` 和 `LEAST` 函数到 TiFlash [#32787](https://github.com/pingcap/tidb/issues/32787)
    - 支持追踪 `UnionScan` 算子的执行情况 [#32631](https://github.com/pingcap/tidb/issues/32631)
    - 支持读取 `_tidb_rowid` 列的查询能够使用 PointGet 计划 [#31543](https://github.com/pingcap/tidb/issues/31543)
    - 支持在 `EXPLAIN` 语句的输出中显示原有的分区名而不转换为小写 [#32719](https://github.com/pingcap/tidb/issues/32719)
    - 支持对 RANGE COLUMNS 分区表在 IN 条件和字符串类型上进行分区裁剪 [#32626](https://github.com/pingcap/tidb/issues/32626)
    - 当设置系统变量为 NULL 时提供错误提示 [#32850](https://github.com/pingcap/tidb/issues/32850)
    - 移除非 MPP 模式的 Broadcast Join [#31465](https://github.com/pingcap/tidb/issues/31465)
    - 支持在动态裁剪模式的分区表上执行 MPP 计划 [#32347](https://github.com/pingcap/tidb/issues/32347)
    - 支持对公共表表达式 (CTE) 进行谓词下推 [#28163](https://github.com/pingcap/tidb/issues/28163)
    - 简化 `Statement Summary` 和 `Capture Plan Baselines` 的配置为只在全局基础上可用 [#30557](https://github.com/pingcap/tidb/issues/30557)
    - 更新 gopsutil 的版本到 v3.21.12，避免在 macOS 12 上构建二进制时出现警告 [#31607](https://github.com/pingcap/tidb/issues/31607)

+ TiKV

    - 提升 Raftstore 对含有较多 key ranges 的 batch 的采样准确度 [#12327](https://github.com/tikv/tikv/issues/12327)
    - 为 `debug/pprof/profile` 添加正确的 Content-Type，使 Profile 更容易被识别 [#11521](https://github.com/tikv/tikv/issues/11521)
    - 当 Raftstore 在心跳或处理读请求时，通过更新其租约时间来无限延长 leader 的租约时间，减少 leader 切换导致的延迟抖动 [#11579](https://github.com/tikv/tikv/issues/11579)
    - 切换 leader 时以选择代价最小的 store 为目标，提升性能稳定性 [#10602](https://github.com/tikv/tikv/issues/10602)
    - 异步获取 Raft log，减少阻塞 Raftstore 带来的性能抖动 [#11320](https://github.com/tikv/tikv/issues/11320)
    - 向量计算支持 `QUARTER` 函数 [#5751](https://github.com/tikv/tikv/issues/5751)
    - 支持 `BIT` 数据类型下推至 TiKV [#30738](https://github.com/pingcap/tidb/issues/30738)
    - 支持 `MOD` 函数和 `SYSDATE` 函数下推至 TiKV [#11916](https://github.com/tikv/tikv/issues/11916)
    - 通过减少需要进行清理锁 (Resolve Locks) 步骤的 Region 数量来减少 TiCDC 恢复时间 [#11993](https://github.com/tikv/tikv/issues/11993)
    - 支持动态修改 `raftstore.raft-max-inflight-msgs` [#11865](https://github.com/tikv/tikv/issues/11865)
    - 支持 `EXTRA_PHYSICAL_TABLE_ID_COL_ID`，以实现动态裁剪模式 [#11888](https://github.com/tikv/tikv/issues/11888)
    - 支持以 buckets 为单位进行计算 [#11759](https://github.com/tikv/tikv/issues/11759)
    - 将 RawKV API V2 的 Key 编码为 `user-key` + `memcomparable-padding` + `timestamp` [#11965](https://github.com/tikv/tikv/issues/11965)
    - 将 RawKV API V2 的 Value 编码为 `user-value` + `ttl` + `ValueMeta`，并且将 `delete` 编码在 `ValueMeta` 中 [#11965](https://github.com/tikv/tikv/issues/11965)
    - 支持动态修改 `raftstore.raft-max-size-per-msg` [#12017](https://github.com/tikv/tikv/issues/12017)
    - 使 Grafana 支持 multi-k8s 的监控 [#12104](https://github.com/tikv/tikv/issues/12104)
    - 通过将 leader 转让给 CDC observer 减少延迟抖动 [#12111](https://github.com/tikv/tikv/issues/12111)
    - 支持动态修改 `raftstore.apply_max_batch_size` 和 `raftstore.store_max_batch_size` [#11982](https://github.com/tikv/tikv/issues/11982)
    - 支持 RawKV API V2 在收到 `raw_get` 或 `raw_scan` 请求时会返回最新的版本 [#11965](https://github.com/tikv/tikv/issues/11965)
    - 支持 RCCheckTS 的一致性读 [#12097](https://github.com/tikv/tikv/issues/12097)
    - 支持动态修改 `storage.scheduler-worker-pool-size`（Scheduler 线程池中线程的数量） [#12067](https://github.com/tikv/tikv/issues/12067)
    - 通过全局的前台限流器来控制 CPU 与带宽的使用，增加 TiKV 性能的稳定性 [#11855](https://github.com/tikv/tikv/issues/11855)
    - 支持动态修改 `readpool.unified.max-thread-count`（UnifyReadPool 线程池中线程的数量） [#11781](https://github.com/tikv/tikv/issues/11781)
    - 使用 TiKV 内部的 pipeline 替代 RocksDB pipeline，废弃 `rocksdb.enable-multibatch-write` 参数 [#12059](https://github.com/tikv/tikv/issues/12059)

+ PD

    - 支持驱逐 leader 时自动选择最快的目标进行迁移，加速驱逐过程 [#4229](https://github.com/tikv/pd/issues/4229)
    - 禁止直接从有 2 副本的 Raft Group 中删除一个 Voter，防止 Region 不可用 [#4564](https://github.com/tikv/pd/issues/4564)
    - 提升 Balance Leader 的调度速度 [#4652](https://github.com/tikv/pd/issues/4652)

+ TiFlash

    - 禁止了 TiFlash 文件的逻辑分裂（默认参数调整为 `profiles.default.dt_enable_logical_split = false`，详见[用户文档](/tiflash/tiflash-configuration.md#tiflash-配置参数)），优化了 TiFlash 列存储的空间使用效率，使得同一个表在同步到 TiFlash 后所占用空间与 TiKV 相近
    - TiFlash 优化了集群管理和 replica 数据同步机制。将原有的集群管理模块迁移整合进了 TiDB，并提高了为小表创建 TiFlash replica 的速度 [#29924](https://github.com/pingcap/tidb/issues/29924)

+ Tools

    + Backup & Restore (BR)

        - 默认开启批量建表功能，备份数据恢复速度提升。在模拟测试中恢复 16 TB 的备份数据到 15 个节点的 TiKV 集群（每个节点有 16 个 CPU 核心），恢复吞吐可以达到 2.66 GiB/s [#27036](https://github.com/pingcap/tidb/issues/27036)
        - 支持导入与导出放置规则 (Placement Rule)。增加参数 `--with-tidb-placement-mode` 来控制导入时是否忽略放置规则 [#32290](https://github.com/pingcap/tidb/issues/32290)

    + TiCDC

        - 在 Grafana 中添加 `Lag analyze` 监控面板 [#4891](https://github.com/pingcap/tiflow/issues/4891)
        - 支持放置规则 (placement rules) [#4846)](https://github.com/pingcap/tiflow/issues/4846)
        - 同步处理 HTTP API [#1710](https://github.com/pingcap/tiflow/issues/1710)
        - 为 changefeed 重启操作添加指数退避机制 [#3329](https://github.com/pingcap/tiflow/issues/3329)
        - 设置 MySQL sink 的默认隔离级别为 Read Committed，以减少 MySQL 中的死锁 [#3589](https://github.com/pingcap/tiflow/issues/3589)
        - 在创建 changefeed 时验证参数合法，优化报错信息 [#1716](https://github.com/pingcap/tiflow/issues/1716) [#1718](https://github.com/pingcap/tiflow/issues/1718) [#1719](https://github.com/pingcap/tiflow/issues/1719) [#4472](https://github.com/pingcap/tiflow/issues/4472)
        - 暴露 Kafka producer 配置参数，使之在 TiCDC 中可配置 [#4385](https://github.com/pingcap/tiflow/issues/4385)

    + TiDB Data Migration (DM)

        - 支持在“乐观协调”模式（optimistic）下，上游表结构不一致的情况下仍能启动任务 [#3629](https://github.com/pingcap/tiflow/issues/3629) [#3708](https://github.com/pingcap/tiflow/issues/3708) [#3786](https://github.com/pingcap/tiflow/issues/3786)
        - 支持在 `stopped` 状态下创建任务 [#4484](https://github.com/pingcap/tiflow/issues/4484)
        - 支持 Syncer 使用 DM-worker 的工作目录写内部文件，不再使用 /tmp 目录。任务停止后会清理掉该目录 [#4107](https://github.com/pingcap/tiflow/issues/4107)
        - 优化了 Precheck 功能。不再允许跳过某些重要的检查 [#3608](https://github.com/pingcap/tiflow/issues/3608)

    + TiDB Lightning

        - 增加了更多重试错误类型 [#31376](https://github.com/pingcap/tidb/issues/31376)
        - 支持 base64 格式的密码字符串 [#31194](https://github.com/pingcap/tidb/issues/31194)
        - 标准化错误码和错误输出 [#32239](https://github.com/pingcap/tidb/issues/32239)

## Bug 修复

+ TiDB

    - 修复了当 `SCHEDULE = majority_in_primary`，且 `PrimaryRegion` 和 `Regions` 的值相同时创建 placement rule 会报错的问题 [#31271](https://github.com/pingcap/tidb/issues/31271)
    - 修复查询时用到 index lookup join 导致 `invalid transaction` 报错的问题 [#30468](https://github.com/pingcap/tidb/issues/30468)
    - 修复了当授予大于等于 2 个权限时 `show grants` 返回不正确的结果的问题 [#30855](https://github.com/pingcap/tidb/issues/30855)
    - 修复了在默认值为 `CURRENT_TIMESTAMP` 的字段执行 `INSERT INTO t1 SET tsCol = DEFAULT` 语句时插入零值的问题 [#29926](https://github.com/pingcap/tidb/issues/29926)
    - 通过避免编码字符串类型的最大值和最小非空值，修复读取结果时的报错问题 [#31721](https://github.com/pingcap/tidb/issues/31721)
    - 修复 LOAD DATA 语句处理转义字符时可能 panic 的问题 [#31589](https://github.com/pingcap/tidb/issues/31589)
    - 修复带有 collation 的 `greatest` 或 `least` 函数结果出错的问题 [#31789](https://github.com/pingcap/tidb/issues/31789)
    - 修复 date_add 和 date_sub 函数可能返回错误数据类型的问题 [#31809](https://github.com/pingcap/tidb/issues/31809)
    - 修复使用 insert 语句插入数据到虚拟生成列时可能出现 panic 的问题 [#31735](https://github.com/pingcap/tidb/issues/31735)
    - 修复创建 list column 分区表时出现重复列不报错的问题 [#31784](https://github.com/pingcap/tidb/issues/31784)
    - 修复 `select for update union select` 语句使用错误快照导致结果可能错误的问题 [#31530](https://github.com/pingcap/tidb/issues/31530)
    - 修复当恢复完成后，Region 有可能分布不均的问题 [#31034](https://github.com/pingcap/tidb/issues/31034)
    - 修复 `json` 类型 Coercibility 值不正确的问题 [#31541](https://github.com/pingcap/tidb/issues/31541)
    - 修复了 `json` 类型在 builtin-func 中推导 collation 错误的问题 [#31320](https://github.com/pingcap/tidb/issues/31320)
    - 修复当设置 TiFlash 副本数为 0 时 PD 规则没有被删除的问题 [#32190](https://github.com/pingcap/tidb/issues/32190)
    - 修复 `alter column set default` 错误地修改表定义的问题 [#31074](https://github.com/pingcap/tidb/issues/31074)
    - 修复 date_format 对 `'\n'` 的处理与 MySQL 不兼容的问题 [#32232](https://github.com/pingcap/tidb/issues/32232)
    - 修复使用 join 更新分区表时可能报错的问题 [#31629](https://github.com/pingcap/tidb/issues/31629)
    - 修复 Nulleq 函数作用在 Enum 类型上可能出现结果错误的问题 [#32428](https://github.com/pingcap/tidb/issues/32428)
    - 修复 upper 和 lower 函数可能造成 panic 的问题 [#32488](https://github.com/pingcap/tidb/issues/32488)
    - 修复了将其他类型列更改为时间戳类型列时可能遇到的时区问题 [#29585](https://github.com/pingcap/tidb/issues/29585)
    - 修复使用 ChunkRPC 导出数据时可能造成 TiDB OOM 的问题 [#31981](https://github.com/pingcap/tidb/issues/31981) [#30880](https://github.com/pingcap/tidb/issues/30880)
    - 修复动态分区裁剪模式下访问分区表时 Limit 在子查询中不能生效的问题 [#32516](https://github.com/pingcap/tidb/issues/32516)
    - 修复 `INFORMATION_SCHEMA.COLUMNS` 表中 `bit` 类型默认值格式错误或或不一致问题 [#32655](https://github.com/pingcap/tidb/issues/32655)
    - 修复重启实例后 list 分区表的分区裁剪可能不生效的问题 [#32416](https://github.com/pingcap/tidb/issues/32416)
    - 修复了在执行 `SET timestamp` 语句后，`add column` 语句可能会使用错误的默认时间戳的问题 [#31968](https://github.com/pingcap/tidb/issues/31968)
    - 修复使用 MySQL 5.5/5.6 客户端连接 TiDB 无密码用户时可能失败的问题 [#32334](https://github.com/pingcap/tidb/issues/32334)
    - 修复在事务中使用动态模式读取分区表时结果不正确的问题 [#29851](https://github.com/pingcap/tidb/issues/29851)
    - 修复 TiDB 可能向 TiFlash 发送重复任务的问题 [#32814](https://github.com/pingcap/tidb/issues/32814)
    - 修复 `timdiff` 函数的输入包含毫秒时可能出现结果错误的问题 [#31680](https://github.com/pingcap/tidb/issues/31680)
    - 修复显式读取分区并使用 IndexJoin 计划时可能出现结果错误的问题 [#32007](https://github.com/pingcap/tidb/issues/32007)
    - 修复重命名列时并发修改列类型会导致重命名错误的问题 [#31075](https://github.com/pingcap/tidb/issues/31075)
    - 修复 TiFlash 执行计划网络成本计算公式未与 TiKV 对齐的问题 [#30103](https://github.com/pingcap/tidb/issues/30103)
    - 修复 `KILL TIDB` 在空闲链接上无法立即生效的问题 [#24031](https://github.com/pingcap/tidb/issues/24031)
    - 修复读取生成列时可能出现结果错误的问题 [#33038](https://github.com/pingcap/tidb/issues/33038)
    - 修复使用 left join 同时删除多张表数据时可能出现错误结果的问题 [#31321](https://github.com/pingcap/tidb/issues/31321)
    - 修复 `subtime` 函数在出现 Overflow 时可能返回错误结果的问题 [#31868](https://github.com/pingcap/tidb/issues/31868)
    - 修复当聚合查询包含 having 条件时 selection 算子不能被下推的问题 [#33166](https://github.com/pingcap/tidb/issues/33166)
    - 修复查询报错时可能阻塞 CTE 的问题 [#31302](https://github.com/pingcap/tidb/issues/31302)
    - 修复了在非严格模式下，创建表时 varbinary 或 varchar 类型列的长度太大导致报错的问题 [#30328](https://github.com/pingcap/tidb/issues/30328)
    - 修复未指定 follower 时 `information_schema.placement_policies` 中显示的 follower 值有误的问题 [#31702](https://github.com/pingcap/tidb/issues/31702)
    - 修复创建索引时允许指定列前缀长度为 0 的问题 [#31972](https://github.com/pingcap/tidb/issues/31972)
    - ​​修复允许分区名以空格结尾的问题 [#31535](https://github.com/pingcap/tidb/issues/31535)
    - 修正 `RENAME TABLE` 语句的报错信息 [#29893](https://github.com/pingcap/tidb/issues/29893)

+ TiKV

    - 修复 Peer 状态为 Applying 时快照文件被删除会造成 panic 的问题 [#11746](https://github.com/tikv/tikv/issues/11746)
    - 修复开启流量控制且显式设置 `level0_slowdown_trigger` 时出现 QPS 下降的问题 [#11424](https://github.com/tikv/tikv/issues/11424)
    - 修复删除 Peer 可能造成高延迟的问题 [#10210](https://github.com/tikv/tikv/issues/10210)
    - 修复 GC worker 繁忙后无法执行范围删除（即执行内部命令 `unsafe_destroy_range`）的问题 [#11903](https://github.com/tikv/tikv/issues/11903)
    - 修复在某些边界场景中 `StoreMeta` 内数据被意外删除会引发 TiKV panic 的问题 [#11852](https://github.com/tikv/tikv/issues/11852)
    - 修复在 ARM 平台上进行性能分析造成 TiKV panic 的问题 [#10658](https://github.com/tikv/tikv/issues/10658)
    - 修复 TiKV 运行 2 年以上可能 panic 的问题 [#11940](https://github.com/tikv/tikv/issues/11940)
    - 修复因缺少 SSE 指令集导致的 ARM64 架构下的编译问题 [#12034](https://github.com/tikv/tikv/issues/12034)
    - 修复删除未初始化的副本可能会造成旧副本被重新创建的问题 [#10533](https://github.com/tikv/tikv/issues/10533)
    - 修复旧信息造成 TiKV panic 的问题 [#12023](https://github.com/tikv/tikv/issues/12023)
    - 修复 TsSet 转换可能发生未定义行为 (UB) 的问题 [#12070](https://github.com/tikv/tikv/issues/12070)
    - 修复 Replica Read 可能违反线性一致性的问题 [#12109](https://github.com/tikv/tikv/issues/12109)
    - 修复在 Ubuntu 18.04 下进行性能分析会造成 TiKV panic 的问题 [#9765](https://github.com/tikv/tikv/issues/9765)
    - 修复 tikv-ctl 对 `bad-ssts` 结果字符串进行错误匹配的问题 [#12329](https://github.com/tikv/tikv/issues/12329)
    - 修复因内存统计指标溢出而造成的间歇性丢包和内存不足 (OOM) 的问题 [#12160](https://github.com/tikv/tikv/issues/12160)
    - 修复 TiKV 在退出时可能误报 panic 的问题 [#12231](https://github.com/tikv/tikv/issues/12231)

+ PD

    - 修复 PD 生成带有无意义的 Joint Consensus 步骤的 Operator 的问题 [#4362](https://github.com/tikv/pd/issues/4362)
    - 修复关闭 PD Client 时撤销 TSO 的流程可能会卡住的问题 [#4549](https://github.com/tikv/pd/issues/4549)
    - 修复 Region Scatterer 生成的调度缺失部分 Peer 的问题 [#4565](https://github.com/tikv/pd/issues/4565)
    - 修复不能动态设置 `dr-autosync` 的 `Duration` 字段的问题 [#4651](https://github.com/tikv/pd/issues/4651)

+ TiFlash

    - 修复启用内存限制时 TiFlash 崩溃的问题 [#3902](https://github.com/pingcap/tiflash/issues/3902)
    - 修复过期数据回收缓慢的问题 [#4146](https://github.com/pingcap/tiflash/issues/4146)
    - 修复并发执行多个 DDL 操作和 Apply Snapshot 操作时 TiFlash 可能会崩溃问题 [#4072](https://github.com/pingcap/tiflash/issues/4072)
    - 修复在读取工作量大时添加列后可能出现的查询错误 [#3967](https://github.com/pingcap/tiflash/issues/3967)
    - 修复 `SQRT` 函数中传入负值后返回 `NaN` 而不是 `Null` 的问题 [#3598](https://github.com/pingcap/tiflash/issues/3598)
    - 修复将 `INT` 类型转换为 `DECIMAL` 类型可能造成溢出的问题 [#3920](https://github.com/pingcap/tiflash/issues/3920)
    - 修复 `IN` 函数的结果在多值表达式中不正确的问题 [#4016](https://github.com/pingcap/tiflash/issues/4016)
    - 修复日期格式将 `'\n'` 处理为非法分隔符的问题 [#4036](https://github.com/pingcap/tiflash/issues/4036)
    - 修复在高并发场景下 Learner 读过程时间过长的问题 [#3555](https://github.com/pingcap/tiflash/issues/3555)
    - 修复将 `DATETIME` 转换为 `DECIMAL` 时结果错误的问题 [#4151](https://github.com/pingcap/tiflash/issues/4151)
    - 修复查询被取消时出现的内存泄露问题 [#4098](https://github.com/pingcap/tiflash/issues/4098)
    - 修复开启弹性线程池可能导致内存泄漏的问题 [#4098](https://github.com/pingcap/tiflash/issues/4098)
    - 修复启用本地隧道时取消 MPP 查询可能导致任务永远挂起的问题 [#4229](https://github.com/pingcap/tiflash/issues/4229)
    - 修复 HashJoin 构建端失败可能导致 MPP 查询永远挂起的问题 [#4195](https://github.com/pingcap/tiflash/issues/4195)
    - 修复 MPP 任务可能永远泄漏线程的问题 [#4238](https://github.com/pingcap/tiflash/issues/4238)

+ Tools

    + Backup & Restore (BR)

        - 修复了当恢复操作遇到一些无法恢复的错误时，BR 被卡住的问题 [#33200](https://github.com/pingcap/tidb/issues/33200)
        - 修复了在备份重试过程中加密信息丢失导致的恢复操作失败的问题 [#32423](https://github.com/pingcap/tidb/issues/32423)

    + TiCDC

        - 修复 MySQL sink 在禁用 `batch-replace-enable` 参数时生成重复 `replace` SQL 语句的错误 [#4501](https://github.com/pingcap/tiflow/issues/4501)
        - 修复了 TiCDC 进程在 PD leader 被杀死时的异常退出问题 [#4248](https://github.com/pingcap/tiflow/issues/4248)
        - 修复使用某些版本 MySQL sink 时可能遇到 `Unknown system variable 'transaction_isolation'` 报错的问题 [#4504](https://github.com/pingcap/tiflow/issues/4504)
        - 修复 `Canal-JSON` 错误处理 `string` 格式可能导致的 TiCDC panic 问题 [#4635](https://github.com/pingcap/tiflow/issues/4635)
        - 修复某些情况下序列对象被错误同步的问题 [#4552](https://github.com/pingcap/tiflow/issues/4552)
        - 修复 `Canal-JSON` 不支持 nil 可能导致的 TiCDC panic 问题 [#4736](https://github.com/pingcap/tiflow/issues/4736)
        - 修复对 Enum/Set 和 TinyText/MediumText/Text/LongText 类型 avro 编码的数据映射错误 [#4454](https://github.com/pingcap/tiflow/issues/4454)
        - 修复 Avro 把 `NOT NULL` 列转换成 `nullable` 字段的错误 [#4818](https://github.com/pingcap/tiflow/issues/4818)
        - 修复 TiCDC 无法退出的问题 [#4699](https://github.com/pingcap/tiflow/issues/4699)

    + TiDB Data Migration (DM)

        - 修复部分 syncer metrics 只有在查询状态时才得以更新的问题 [#4281](https://github.com/pingcap/tiflow/issues/4281)
        - 修复了 UPDATE 语句在安全模式下执行错误会导致 DM 进程挂掉的问题 [#4317](https://github.com/pingcap/tiflow/issues/4317)
        - 修复了 varchar 类型值长度过长时的 `Column length too big` 错误 [#4637](https://github.com/pingcap/tiflow/issues/4637)
        - 修复了多个 DM-worker 写入来自同一上游的数据导致的冲突问题 [#3737](https://github.com/pingcap/tiflow/issues/3737)
        - 修复了日志中出现数百条 "checkpoint has no change, skip sync flush checkpoint" 以及迁移性能下降的问题 [#4619](https://github.com/pingcap/tiflow/issues/4619)
        - 修复了悲观模式下对上游增量数据进行分库分表合并迁移时有可能会丢 DML 的问题 [#5002](https://github.com/pingcap/tiflow/issues/5002)

    + TiDB Lightning

        - 修复在某些导入操作没有包含源文件时，TiDB Lightning 不会删除 metadata schema 的问题 [#28144](https://github.com/pingcap/tidb/issues/28144)
        - 修复了源文件和目标集群中的表格名称不一致导致数据迁移失败的问题 [#31771](https://github.com/pingcap/tidb/issues/31771)
        - 修复了 checksum 报错 “GC life time is shorter than transaction duration” [#32733](https://github.com/pingcap/tidb/issues/32733)
        - 修复了检查空表失败导致 TiDB Lightning 卡住的问题 [#31797](https://github.com/pingcap/tidb/issues/31797)

    + Dumpling

        - 修复了执行 `dumpling --sql $query` 进度显示不准确的问题 [#30532](https://github.com/pingcap/tidb/issues/30532)
        - 修复了 Amazon S3 无法正确计算压缩数据大小的问题 [#30534](https://github.com/pingcap/tidb/issues/30534)

    + TiDB Binlog

        - 修复了上游写大事务向 Kafka 同步时可能会导致 TiDB Binlog 被跳过的问题 [#1136](https://github.com/pingcap/tidb-binlog/issues/1136)

如果你在使用 TiDB v6.0.0 的过程中遇到问题，可以到 [AskTUG 论坛](https://asktug.com/tags/tidb-v6)浏览、搜索或反馈问题。
