---
title: TiDB 6.1.0 Release Notes
---

# TiDB 6.1.0 Release Notes

<EmailSubscriptionWrapper />

发版日期：2022 年 6 月 13 日

TiDB 版本：6.1.0

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v6.1/quick-start-with-tidb) | [生产部署](https://docs.pingcap.com/zh/tidb/v6.1/production-deployment-using-tiup)

在 6.1.0 版本中，你可以获得以下关键特性：

- List 和 List COLUMNS 分区方式 GA，与 MySQL 5.7 兼容
- TiFlash 分区表动态裁剪 GA
- 支持兼容 MySQL 的用户级别锁管理
- 支持非事务性 DML 语法（目前仅支持 DELETE）
- TiFlash 支持按需触发物理数据整理（Compaction）
- MPP 实现窗口函数框架
- TiCDC 支持将 changelogs 以 Avro 协议输出到 Kafka
- TiCDC 支持在数据复制过程中拆分大事务，能够有效降低大事务带来的复制延迟
- DM 合库合表迁移场景的乐观 DDL 协调模式 GA

## 新功能

### SQL

* List 和 List COLUMNS 分区方式正式 GA，与 MySQL 5.7 兼容。

    用户文档：[List 分区](/partitioned-table.md#list-分区)，[List COLUMNS 分区](/partitioned-table.md#list-columns-分区)

* 支持通过 SQL 语句对 TiFlash 副本立即触发物理数据整理 (Compaction)（实验特性）

    在当前 TiFlash 后台自动整理物理数据（Compaction）机制基础上，新增 compact 命令，帮助刷新旧格式数据，提升读写性能。推荐在升级至 v6.1.0 之后，执行该语句以清理数据。此语句是对标准 SQL 语法的扩展，对 MySQL 客户端保持兼容。升级之外场景一般不需要特别关注。

    [用户文档](/sql-statements/sql-statement-alter-table-compact.md)，[#4145](https://github.com/pingcap/tiflash/issues/4145)

* 实现窗口函数框架，支持以下分析函数：

    * `RANK()`
    * `DENSE_RANK()`
    * `ROW_NUMBER()`

  [用户文档](/tiflash/tiflash-supported-pushdown-calculations.md)，[#33072](https://github.com/pingcap/tidb/issues/33072)

### 可观测性

* 持续性能分析支持 ARM 架构和 TiFlash 组件。

    [用户文档](/dashboard/continuous-profiling.md)

* Grafana 中新增 Performance Overview 面板，提供系统级别的总体性能诊断入口。

    Performance Overview 是 TiDB 监控 Grafana 可视化组件中的一个新增面板，基于数据库时间分析法和颜色优化法，按照自上而下的性能分析方法论对 TiDB 的性能指标做了重新梳理，为 TiDB 用户提供一个系统级别的总体性能诊断入口。通过 Performance Overview 面板，你可以直观地看到整个系统的性能瓶颈在哪里，数量级地缩短了性能诊断时间并降低了性能分析和诊断难度。

    [用户文档](/performance-tuning-overview.md)

### 性能

* 支持自定义 Region 大小

    从 v6.1.0 起，你可以通过 [`coprocessor.region-split-size`](/tikv-configuration-file.md#region-split-size) 设置更大的 Region 从而有效减少 Region 数量，降低 Region 管理成本，提升集群性能和稳定性。

    [用户文档](/tune-region-performance.md#使用-region-split-size-调整-region-大小)，[#11515](https://github.com/tikv/tikv/issues/11515)

* 支持使用 bucket 增加并发（实验特性）

    当 Region 调大以后，为了进一步提高查询的并发度，TiDB 引入 bucket 概念，即将每个 Region 划分为更小的区间 bucket。使用 bucket 作为并发查询单位能够优化 Region 调大时的查询性能，动态调整热点 Region 的大小来保证热点调度效率和负载均衡。该特性目前属于实验特性，不建议在生产环境使用。

    [用户文档](/tune-region-performance.md#使用-region-split-size-调整-region-大小)，[#11515](https://github.com/tikv/tikv/issues/11515)

* Raft Engine 存储引擎 GA

    TiDB 从 v6.1.0 开始默认使用引擎 [Raft Engine](https://github.com/tikv/raft-engine) 作为 TiKV 的日志存储引擎。新引擎与 RocksDB 相比，可以减少至多 40% 的 TiKV I/O 写流量和 10% 的 CPU 使用，同时在特定负载下提升 5% 左右前台吞吐，减少 20% 长尾延迟。

    [用户文档](/tikv-configuration-file.md#raft-engine)，[#95](https://github.com/tikv/raft-engine/issues/95)

* 支持 join order hint 语法

    * `LEADING` hint：提示优化器使用指定的顺序作为连接前缀，好的连接前缀顺序可以在连接初期快速地降低数据量，提升查询性能。
    * `STRAIGHT_JOIN` hint：提示优化器按照表在 `FROM` 子句中的出现顺序进行连接。

    该特性提供更多的手段帮助用户固定连接顺序，合理运用 hint 语法，可以有效提升 SQL 性能和集群稳定性。

  用户文档：[`LEADING`](/optimizer-hints.md#leadingt1_name--tl_name-)，[`STRAIGHT_JOIN`](/optimizer-hints.md#straight_join)，[#29932](https://github.com/pingcap/tidb/issues/29932)

* TiFlash 新增对以下函数的支持：

    * `FROM_DAYS`
    * `TO_DAYS`
    * `TO_SECONDS`
    * `WEEKOFYEAR`

  [用户文档](/tiflash/tiflash-supported-pushdown-calculations.md)，[#4679](https://github.com/pingcap/tiflash/issues/4679)，[#4678](https://github.com/pingcap/tiflash/issues/4678)，[#4677](https://github.com/pingcap/tiflash/issues/4677)

* 支持分区表动态裁剪

    支持分区表动态裁剪功能，以提升数据分析场景下的性能。v6.0.0 以前版本的用户升级完成后建议及时手动刷新既存分区表的统计信息，以达到最好的性能表现（全新安装，或在 v6.1.0 升级完成后新创建的分区表无需此动作）。

    用户文档：[MPP 模式访问分区表](/tiflash/use-tiflash-mpp-mode.md#mpp-模式访问分区表)，[动态裁剪模式](/partitioned-table.md#动态裁剪模式)，[#3873](https://github.com/pingcap/tiflash/issues/3873)

### 稳定性

* SST 故障自动恢复

    当 RocksDB 后台检测到故障 SST 文件后，TiKV 会尝试通过调度所涉及的故障 Peer，并利用其它副本恢复该节点数据，用户可以通过参数 `background-error-recovery-window` 设置允许的最长恢复时间。如果恢复操作未能在设置的时间窗口内完成，TiKV 将会崩溃。该特性对于可恢复存储故障进行自动检测和恢复，提升了集群稳定性。

    [用户文档](/tikv-configuration-file.md#background-error-recovery-window-从-v610-版本开始引入)，[#10578](https://github.com/tikv/tikv/issues/10578)

* 支持非事务性 DML 语法

    在大批量的数据处理场景，单一大事务 SQL 处理有可能对集群稳定性和性能造成影响。TiDB 从 v6.1.0 支持对 `DELETE` 语句提供拆分后批量处理的语法格式，拆分后的语句将牺牲事务原子性和隔离性，但是对于集群的稳定性有很大提升，详细语法请参考 [`BATCH`](/sql-statements/sql-statement-batch.md)。

    [用户文档](/non-transactional-dml.md)

* TiDB 支持设置最大 GC 等待时间

    TiDB 的事务的实现采用了 MVCC（多版本并发控制）机制，当新写入的数据覆盖旧的数据时，旧的数据不会被替换掉，而是与新写入的数据同时保留，并通过 Garbage Collection (GC) 的任务定期清理不再需要的旧数据。定期 GC 清理有助于回收存储空间，提升集群性能和稳定性，TiDB 默认每 10 分钟自动执行 GC 清理。为了保证长时间执行的事务可以访问到对应的历史数据，当有执行中的事务时，GC 清理会被推迟。为了保证 GC 清理不会被无限制推迟，TiDB 从 v6.1.0 引入了系统变量 [`tidb_gc_max_wait_time`](/system-variables.md#tidb_gc_max_wait_time-从-v610-版本开始引入) 来控制 GC 推迟的最大等待时间，超过该参数允许的时间，GC 将会被强制执行。该参数默认为 24 小时。通过该系统变量，用户可以有效地控制 GC 等待时长与长事务的关系，提升集群的稳定性。

    [用户文档](/system-variables.md#tidb_gc_max_wait_time-从-v610-版本开始引入)

* 支持设置统计信息自动采集任务的最长执行时间

    通过采集统计信息，数据库可以有效掌握数据的分布情况，从而生成合理的执行计划，提升 SQL 的执行效率。TiDB 在后台会定期对频繁变更的数据对象进行统计信息采集，但在业务高峰期时进行统计信息采集可能会对集群资源造成挤压，影响业务的稳定运行。TiDB 从 v6.1.0 开始提供系统变量 [`tidb_max_auto_analyze_time`](/system-variables.md#tidb_max_auto_analyze_time-从-v610-版本开始引入) 用来控制后台统计信息采集的最长执行时间，默认为 12 小时。当业务没有遇到资源瓶颈的情况时，建议不要修改该参数，确保数据对象的统计信息及时采集。但是当业务压力大，资源不足的时候，可以通过该变量减少统计信息采集的时长，避免统计信息采集对核心业务造成资源争抢。

    [用户文档](/system-variables.md#tidb_max_auto_analyze_time-从-v610-版本开始引入)

### 易用性

* 支持集群在 Region 多副本丢失状态下在线一键式恢复数据

    在 TiDB v6.1.0 之前，当出现多个 TiKV 因物理机故障导致 Region 的多副本丢失时，用户需要停机所有 TiKV，使用 TiKV Control 逐一对 TiKV 进行恢复。从 TiDB v6.1.0 起，该过程被完全自动化且不需要停机，恢复过程中不影响其他正常的在线业务。通过 PD Control 触发在线有损恢复数据，大幅简化了恢复步骤，缩短了恢复所需时间，提供了更加友好的恢复摘要信息。

    [用户文档](/online-unsafe-recovery.md)，[#10483](https://github.com/tikv/tikv/issues/10483)

* 历史统计信息采集持久化

    支持通过 `SHOW ANALYZE STATUS` 语句查询集群级别的统计信息收集任务。在 TiDB v6.1.0 之前，`SHOW ANALYZE STATUS` 语句仅显示实例级别的统计信息收集任务，且 TiDB 重启后历史任务记录会被清空，因此用户无法查看历史统计信息的采集时间和相关细节。从 TiDB v6.1.0 起，该信息被持久化保存，集群重启后依然可查询，可以为统计信息异常引起的查询性能问题提供排查依据。

    [用户文档](/sql-statements/sql-statement-show-analyze-status.md)

* TiDB/TiKV/TiFlash 参数支持在线修改

  在 v6.1.0 之前的版本中，配置变更后，必须重启 TiDB 集群，配置才会生效，这对在线业务会造成一定的影响。TiDB v6.1.0 引入了在线修改配置功能，参数修改后，无需重启，即可生效。具体优化如下：

    * TiDB 将部分配置项转化为系统变量，所有变量支持在线变更，并支持持久化。请注意，转化后，原有配置项将被废弃。详细变更列表请查看[配置文件参数](#配置文件参数)。
    * TiKV 支持部分参数在线变更。详细变更列表请查看[其他](#其他)。
    * TiFlash 配置项 `max_threads` 转化为系统变量 `tidb_max_tiflash_threads`，从而支持配置项在线变更和持久化。转化后，原有配置项不会废弃。

  对于从 v6.1.0 之前版本升级到 v6.1.0 的集群（包括滚动升级和停机升级），请注意：

    * 若升级前集群指定的配置文件中，存在已经配置的项，则升级过程中 TiDB 将会将配置项的值自动更新为对应系统变量的值，以保证升级后，系统的行为不会因为参数的优化发生变化。
    * 上述自动更新仅在升级过程中发生一次，升级完成之后，被废弃的配置项不再有任何效果。

  通过本次优化，客户可以在线修改参数生效并持久化，方便客户进行日常运维，避免重启生效对在线业务造成的影响。

  [用户文档](/dynamic-config.md)

* 支持全局 kill 查询或连接

    支持通过 `enable-global-kill` 配置项（默认开启）设置全局 kill 开关。

    在 TiDB v6.1.0 之前，当某个特定操作占用大量资源引发集群稳定性问题时，你需要先登陆到对应的 TiDB 节点，然后运行 `kill [TiDB] id` 命令终止对应的连接及操作。在 TiDB 节点多的情况下，这种方式使用不便，并且容易误操作。从 v6.1.0 起，当开启 `enable-global-kill` 配置项时，你可以在任意 TiDB 节点运行 kill 命令终止指定的连接及操作，而无需担心客户端和 TiDB 中间有代理时错误地终止其他查询或会话。目前 TiDB 暂时不支持用 Ctrl+C 终止查询或会话。

    [用户文档](/tidb-configuration-file.md#enable-global-kill-从-v610-版本开始引入)，[#8854](https://github.com/pingcap/tidb/issues/8854)

* TiKV API V2（实验特性）

    在 v6.1.0 之前，TiKV 作为 Raw Key Value 存储时，由于仅存储了客户端传入的原始数据，因此只提供基本的 Key Value 读写能力。

    TiKV API V2 提供了新的 Raw Key Value 存储格式与访问接口，包括：

    * 数据以 MVCC 方式存储，并记录了数据的变更时间戳。这个特性将为实现 Change Data Capture、增量备份与恢复等打下基础。
    * 数据根据不同的使用方式划分范围，支持单一集群 TiDB、事务 KV、RawKV 应用共存。

  <Warning>
  由于底层存储格式发生了重大变化，启用 API V2 后，不能将 TiKV 集群回退到 v6.1.0 之前的版本，否则可能导致数据损坏。
  </Warning>

    [用户文档](/tikv-configuration-file.md#api-version-从-v610-版本开始引入)，[#11745](https://github.com/tikv/tikv/issues/11745)

### MySQL 兼容性

* 支持兼容 MySQL 的用户级别锁管理

    用户级别锁是 MySQL 通过内置函数提供的用户命名锁管理系统。它们可以提供锁阻塞、等待、等锁管理能力。用户级别锁在 ORM 框架中也有较为广泛的应用，例如 Rails、Elixir 和 Ecto 等。TiDB 从 v6.1.0 版本开始支持兼容 MySQL 的用户级别锁管理，支持 `GET_LOCK`、`RELEASE_LOCK`、`RELEASE_ALL_LOCKS` 函数。

    [用户文档](/functions-and-operators/locking-functions.md)，[#14994](https://github.com/pingcap/tidb/issues/14994)

### 数据迁移

* DM 合库合表迁移场景的乐观 DDL 协调模式 GA

    对于合库合表迁移任务，DM 在现有乐观 DDL 协调策略的基础上增加了大量场景测试，足以覆盖 90% 日常使用场景。相比悲观协调策略，乐观协调在使用上更为简单、高效，在仔细阅读注意事项后可优先使用。

    [用户文档](/dm/feature-shard-merge-optimistic.md#使用限制)

* DM 的 WebUI 支持根据指定参数条件启动任务

    开始一个迁移任务时，允许指定“开始时间”和 “safe-mode 持续时间”。这在创建具有大量 source 的增量迁移任务时尤其有用，无需再为每个 source 精确指定 binlog 起始同步位置。

    [用户文档](/dm/dm-webui-guide.md)，[#5442](https://github.com/pingcap/tiflow/issues/5442)

### 数据共享订阅

* 支持与更丰富的第三方数据生态系统进行数据共享

    * TiCDC 支持将 TiDB 数据库的增量数据以 Avro 格式发送到 Kafka，通过 Confluent 与 KSQL、Snowflake 等第三方系统进行数据共享。

        [用户文档](/ticdc/ticdc-avro-protocol.md)，[#5338](https://github.com/pingcap/tiflow/issues/5338)

    * TiCDC 支持将 TiDB 数据库的增量数据按表分发到不同的 Kafka Topic 中，结合 Canal-json 格式可以将数据直接与 Flink 共享。

        [用户文档](/ticdc/manage-ticdc.md#自定义-kafka-sink-的-topic-和-partition-的分发规则)，[#4423](https://github.com/pingcap/tiflow/issues/4423)

    * TiCDC 支持 SASL GSSAPI 认证类型。增加了使用 Kafka 的 SASL 认证示例。

        [用户文档](/ticdc/manage-ticdc.md#ticdc-使用-kafka-的认证与授权)，[#4423](https://github.com/pingcap/tiflow/issues/4423)

* TiCDC 支持同步使用 GBK 编码的上游表。

    [用户文档](/character-set-gbk.md#组件兼容性)，[#4806](https://github.com/pingcap/tiflow/issues/4806)

## 兼容性变更

### 系统变量

| 变量名 | 修改类型 | 描述 |
|:---|:--|:----|
| [`tidb_enable_list_partition`](/system-variables.md#tidb_enable_list_partition-从-v50-版本开始引入) | 修改 | 默认值从 `OFF` 改为 `ON`。 |
| [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query) | 修改 | 增加 GLOBAL 作用域，变量值可以持久化到集群。 |
| [`tidb_query_log_max_len`](/system-variables.md#tidb_query_log_max_len) | 修改 | 变量作用域由 INSTANCE 修改为 GLOBAL，变量值可以持久化到集群。取值范围修改为 `[0, 1073741824]`。 |
| [`require_secure_transport`](/system-variables.md#require_secure_transport-从-v610-版本开始引入) | 新增 | 由 TiDB 配置项 `require-secure-transport` 转化而来。 |
| [`tidb_committer_concurrency`](/system-variables.md#tidb_committer_concurrency-从-v610-版本开始引入) | 新增 | 由 TiDB 配置项 `committer-concurrency` 转化而来。 |
| [`tidb_enable_auto_analyze`](/system-variables.md#tidb_enable_auto_analyze-从-v610-版本开始引入) | 新增 | 由 TiDB 配置项 `run-auto-analyze` 转化而来。 |
| [`tidb_enable_new_only_full_group_by_check`](/system-variables.md#tidb_enable_new_only_full_group_by_check-从-v610-版本开始引入) | 新增 | 控制 TiDB 执行 `ONLY_FULL_GROUP_BY` 检查时的行为。 |
| [`tidb_enable_outer_join_reorder`](/system-variables.md#tidb_enable_outer_join_reorder-从-v610-版本开始引入) | 新增 | 控制 TiDB 的 [Join Reorder 算法](/join-reorder.md) 支持 Outer Join，默认开启。对于从旧版本升级上来的集群，该变量的默认值也会是 `TRUE`。 |
| [`tidb_enable_prepared_plan_cache`](/system-variables.md#tidb_enable_prepared_plan_cache-从-v610-版本开始引入) | 新增 | 由 TiDB 配置项 `prepared-plan-cache.enabled` 转化而来。 |
| [`tidb_gc_max_wait_time`](/system-variables.md#tidb_gc_max_wait_time-从-v610-版本开始引入) | 新增 | 用于指定活跃事务阻碍 GC safe point 推进的最大时间。 |
| [`tidb_max_auto_analyze_time`](/system-variables.md#tidb_max_auto_analyze_time-从-v610-版本开始引入) | 新增 | 用于指定自动 ANALYZE 的最大执行时间。 |
| [`tidb_max_tiflash_threads`](/system-variables.md#tidb_max_tiflash_threads-从-v610-版本开始引入) | 新增 | 由 TiFlash 配置项 `max_threads`<br/> 转化而来，表示 TiFlash 中 request 执行的最大并发度。 |
| [`tidb_mem_oom_action`](/system-variables.md#tidb_mem_oom_action-从-v610-版本开始引入) | 新增 | 由 TiDB 配置项 `oom-action` 转化而来。 |
| [`tidb_mem_quota_analyze`](/system-variables.md#tidb_mem_quota_analyze-从-v610-版本开始引入) | 新增 | 控制 TiDB 更新统计信息时总的内存占用，包括用户执行的 [`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md) 和 TiDB 后台自动执行的统计信息更新任务。 |
| [`tidb_nontransactional_ignore_error`](/system-variables.md#tidb_nontransactional_ignore_error-从-v610-版本开始引入) | 新增 | 设置是否在非事务语句中立刻返回错误。 |
| [`tidb_prepared_plan_cache_memory_guard_ratio`](/system-variables.md#tidb_prepared_plan_cache_memory_guard_ratio-从-v610-版本开始引入) | 新增 | 由 TiDB 配置项 `prepared-plan-cache.memory-guard-ratio` 转化而来。 |
| [`tidb_prepared_plan_cache_size`](/system-variables.md#tidb_prepared_plan_cache_size-从-v610-版本开始引入) | 新增 | 由 TiDB 配置项 `prepared-plan-cache.capacity` 转化而来。 |
| [`tidb_stats_cache_mem_quota`](/system-variables.md#tidb_stats_cache_mem_quota-从-v610-版本开始引入) | 新增 | 控制 TiDB 内部统计信息缓存使用内存的上限。 |

### 配置文件参数

| 配置文件 | 配置项 | 修改类型 | 描述 |
|:---|:---|:---|:-----|
| TiDB | `committer-concurrency` | 删除 | 转化为系统变量 `tidb_committer_concurrency`。该配置项不再生效，如需修改，需修改对应的系统变量。 |
| TiDB | `lower-case-table-names` | 删除 | TiDB 目前只支持 `lower_case_table_name=2`，如果升级前设置了其他值，升级到 v6.1.0 后该值会丢失。 |
| TiDB | `mem-quota-query` | 删除 | 转化为系统变量 `tidb_mem_quota_query`。该配置项不再生效，如需修改，需修改对应的系统变量。 |
| TiDB | `oom-action` | 删除 | 转化为系统变量 `tidb_mem_oom_action`。该配置项不再生效，如需修改，需修改对应的系统变量。 |
| TiDB | `prepared-plan-cache.capacity` | 删除 | 转化为系统变量 `tidb_prepared_plan_cache_size`。该配置项不再生效，如需修改，需修改对应的系统变量。 |
| TiDB | `prepared-plan-cache.enabled` | 删除 | 转化为系统变量 `tidb_enable_prepared_plan_cache`。该配置项不再生效，如需修改，需修改对应的系统变量。 |
| TiDB | `query-log-max-len` | 删除 | 转化为系统变量 `tidb_query_log_max_len`。该配置项不再生效，如需修改，需修改对应的系统变量。 |
| TiDB | `require-secure-transport` | 删除 | 转化为系统变量 `require_secure_transport`。该配置项不再生效，如需修改，需修改对应的系统变量。 |
| TiDB | `run-auto-analyze` | 删除 | 转化为系统变量 `tidb_enable_auto_analyze`。该配置项不再生效，如需修改，需修改对应的系统变量。 |
| TiDB | [`enable-global-kill`](/tidb-configuration-file.md#enable-global-kill-从-v610-版本开始引入) | 新增 | 当该配置项值默认为 `true` ，`KILL` 语句和 `KILL TIDB` 语句均能跨节点终止查询或连接，无需担心错误地终止其他查询或连接。 |
| TiDB | [`enable-stats-cache-mem-quota`](/tidb-configuration-file.md#enable-stats-cache-mem-quota-从-v610-版本开始引入) | 新增 | 控制 TiDB 是否开启统计信息缓存的内存上限。 |
| TiKV | [`raft-engine.enable`](/tikv-configuration-file.md#enable-1) | 修改 | 默认值从 `false` 修改为 `true`。 |
| TiKV | [`region-max-keys`](/tikv-configuration-file.md#region-max-keys) | 修改 | 默认值从 1440000 修改为 `region-split-keys / 2 * 3`。 |
| TiKV | [`region-max-size`](/tikv-configuration-file.md#region-max-size) | 修改 | 默认值从 144 MB 修改为 `region-split-size / 2 * 3`。 |
| TiKV | [`coprocessor.enable-region-bucket`](/tikv-configuration-file.md#enable-region-bucket-从-v610-版本开始引入) | 新增 | 是否将 Region 划分为更小的区间 bucket。 |
| TiKV | [`coprocessor.region-bucket-size`](/tikv-configuration-file.md#region-bucket-size-从-v610-版本开始引入) | 新增 | 设置 `enable-region-bucket` 启用时 bucket 的预期大小。 |
| TiKV | [`causal-ts.renew-batch-min-size`](/tikv-configuration-file.md#renew-batch-min-size) | 新增 | 时间戳缓存的最小数量。 |
| TiKV | [`causal-ts.renew-interval`](/tikv-configuration-file.md#renew-interval) | 新增 | 刷新本地缓存时间戳的周期。 |
| TiKV | [`max-snapshot-file-raw-size`](/tikv-configuration-file.md#max-snapshot-file-raw-size-从-v610-版本开始引入) | 新增 | 当 snapshot 文件大于该配置项指定的大小时，snapshot 文件会被切割为多个文件。 |
| TiKV | [`raft-engine.memory-limit`](/tikv-configuration-file.md#memory-limit) | 新增 | 指定 Raft Engine 使用内存的上限。 |
| TiKV | [`storage.background-error-recovery-window`](/tikv-configuration-file.md#background-error-recovery-window-从-v610-版本开始引入) | 新增 | RocksDB 检测到可恢复的后台错误后，所允许的最长恢复时间。 |
| TiKV | [`storage.api-version`](/tikv-configuration-file.md#api-version-从-v610-版本开始引入) | 新增 | TiKV 作为 Raw Key Value 存储数据时使用的存储格式与接口版本。 |
| PD | [`schedule.max-store-preparing-time`](/pd-configuration-file.md#max-store-preparing-time-从-v610-版本开始引入) | 新增 | 控制 store 上线阶段的最长等待时间。 |
| TiCDC | [`enable-tls`](/ticdc/manage-ticdc.md#sink-uri-配置-kafka) | 新增 | 控制是否使用 TLS 连接 Kafka。 |
| TiCDC | `sasl-gssapi-user`<br/>`sasl-gssapi-password`<br/>`sasl-gssapi-auth-type`<br/>`sasl-gssapi-service-name`<br/>`sasl-gssapi-realm`<br/>`sasl-gssapi-key-tab-path`<br/>`sasl-gssapi-kerberos-config-path` | 新增 | 支持 Kafka SASL/GSSAPI 认证所需要的参数。详情见 [Sink URI 配置 `kafka`](/ticdc/manage-ticdc.md#sink-uri-配置-kafka)。 |
| TiCDC | [`avro-decimal-handling-mode`](/ticdc/manage-ticdc.md#sink-uri-配置-kafka)<br/>[`avro-bigint-unsigned-handling-mode`](/ticdc/manage-ticdc.md#sink-uri-配置-kafka) | 新增 | 控制 Avro 格式的输出细节。 |
| TiCDC | [`dispatchers.topic`](/ticdc/manage-ticdc.md#同步任务配置文件描述) | 新增 | 控制 TiCDC 将增量数据分发到不同 Kafka Topic 的策略 |
| TiCDC | [`dispatchers.partition`](/ticdc/manage-ticdc.md#同步任务配置文件描述) | 新增 | `dispatchers.partition` 是原 `dispatchers.dispatcher` 配置项的别名，用于控制增量数据的 Kafka Partition 分发策略。 |
| TiCDC | [`schema-registry`](/ticdc/manage-ticdc.md#ticdc-集成-kafka-connect-confluent-platform) | 新增 | 用于指定存储 Avro Schema 的 Schema Registry Endpoint。 |
| DM | `dmctl start-relay` 命令中的 worker 参数 | 删除 | 不推荐使用的方式，将通过更为简单的实现替代。 |
| DM | source 配置中的 `relay-dir` | 删除 | 由 worker 配置文件中的同名配置项替代。 |
| DM | task 配置中的 `is-sharding` | 删除 | 由 `shard-mode` 配置项替代。 |
| DM | task 配置中的 `auto-fix-gtid` | 删除 | 该配置已在 5.x 版本废弃，v6.1.0 正式移除。 |
| DM | source 配置中的 `meta-dir`、`charset` | 删除 | 该配置已在 5.x 版本废弃，v6.1.0 正式移除。 |

### 其他

* 默认开启 Prepared Plan Cache

    在新集群默认打开 Prepared Plan Cache 的开关，对 `Prepare` / `Execute` 请求的执行计划进行缓存，以便在后续执行时跳过查询计划优化这个步骤，获得性能上的提升。升级上来的集群会继承配置文件内的配置。新集群会使用新的默认值，即默认打开该特性，并且每个 Session 最大缓存计划数为 100（capacity=100）。开启后会有一定的内存消耗，详情见 [Prepared Plan Cache 的内存管理](/sql-prepared-plan-cache.md#prepared-plan-cache-的内存管理)。

* 在 TiDB v6.1.0 之前，`SHOW ANALYZE STATUS` 显示实例级别的任务，且 TiDB 重启后任务记录会被清空。从 TiDB v6.1.0 起，`SHOW ANALYZE STATUS` 显示集群级别的任务，且 TiDB 重启后仍能看到重启之前的任务记录。当 `tidb_analyze_version = 2` 时 `Job_info` 列增加了 `analyze option` 的信息。

* TiKV 中损坏的 SST 文件会导致 TiKV 进程崩溃。在 TiDB v6.1.0 之前，损坏的 SST 文件会导致 TiKV 进程立即崩溃，从 TiDB v6.1.0 起，TiKV 进程会在 SST 文件损坏的 1 小时之后崩溃。

* TiKV 中以下配置项支持[在线修改](/dynamic-config.md#在线修改-tikv-配置)：

    * `raftstore.raft-entry-max-size`
    * `quota.foreground-cpu-time`
    * `quota.foreground-write-bandwidth`
    * `quota.foreground-read-bandwidth`
    * `quota.max-delay-duration`
    * `server.grpc-memory-pool-quota`
    * `server.max-grpc-send-msg-len`
    * `server.raft-msg-max-batch-size`

* v6.1.0 中，部分配置项转化为系统变量。对于从 v6.1.0 之前版本升级到 v6.1.0 的集群（包括滚动升级和停机升级），请注意：

    * 若升级前集群指定的配置文件中，存在已经配置的项，则升级过程中 TiDB 将会将配置项的值自动更新为对应系统变量的值，以保证升级后，系统的行为不会因为参数的优化发生变化。
    * 上述自动更新仅在升级过程中发生一次，升级完成之后，被废弃的配置项不再有任何效果。

* DM WebUI 移除 Dashboard 页面。

* TiCDC 启用 `dispatchers.topic`、`dispatchers.partition` 配置后不支持降级到 v6.1.0 以前的版本。

* TiCDC 使用 Avro 协议的 Changefeed 不支持降级到 v6.1.0 以前的版本。

## 改进提升

+ TiDB

    - 提升 `UnionScanRead` 算子的性能 [#32433](https://github.com/pingcap/tidb/issues/32433)
    - 优化 `Explain` 输出中 task type 的显示（增加 MPP task type）[#33332](https://github.com/pingcap/tidb/issues/33332)
    - 支持使用 `rand()` 作为列的默认值 [#10377](https://github.com/pingcap/tidb/issues/10377)
    - 支持使用 `uuid()` 作为列的默认值 [#33870](https://github.com/pingcap/tidb/issues/33870)
    - 支持将表或列的字符集从 `latin1` 修改为 `utf8`/`utf8mb4` [#34008](https://github.com/pingcap/tidb/issues/34008)

+ TiKV

    - 提升引入内存悲观锁后 CDC 旧数据的命中率 [#12279](https://github.com/tikv/tikv/issues/12279)
    - 健康检查可以检测到无法正常工作的 Raftstore，使得 TiKV client 可以及时更新 Region Cache [#12398](https://github.com/tikv/tikv/issues/12398)
    - 支持设置 Raft Engine 的内存限制 [#12255](https://github.com/tikv/tikv/issues/12255)
    - TiKV 自动检测和删除损坏的 SST 文件，提高产品可服务性 [#10578](https://github.com/tikv/tikv/issues/10578)
    - CDC 支持 RawKV [#11965](https://github.com/tikv/tikv/issues/11965)
    - 支持将较大的 snapshot 切割为多个文件 [#11595](https://github.com/tikv/tikv/issues/11595)
    - 将 snapshot 垃圾回收 (GC) 从 Raftstore 中迁移到后台线程，防止 snapshot GC 阻塞 Raftstore 消息循环 [#11966](https://github.com/tikv/tikv/issues/11966)
    - 支持动态设置 gRPC 可发送的最大消息长度 (`max-grpc-send-msg-len`) 和单个 gPRC 消息可包含的最大 Raft 消息个数 (`raft-msg-max-batch-size`) [#12334](https://github.com/tikv/tikv/issues/12334)
    - 支持通过 Raft 执行在线有损恢复 [#10483](https://github.com/tikv/tikv/issues/10483)

+ PD

    - 支持设置 Region Label 的 Time to live (TTL) [#4694](https://github.com/tikv/pd/issues/4694)
    - 支持 Region Buckets [#4668](https://github.com/tikv/pd/issues/4668)
    - 默认关闭编译 swagger server [#4932](https://github.com/tikv/pd/issues/4932)

+ TiFlash

    - 优化聚合算子的内存统计，从而能在 Merge 阶段选择更高效的算法 [#4451](https://github.com/pingcap/tiflash/issues/4451)

+ Tools

    + Backup & Restore (BR)

        - 支持备份恢复空库 [#33866](https://github.com/pingcap/tidb/issues/33866)

    + TiDB Lightning

        - 优化 Scatter Region 为批量模式，提升 Scatter Region 过程的稳定性 [#33618](https://github.com/pingcap/tidb/issues/33618)

    + TiCDC

        - TiCDC 支持在数据复制过程中拆分大事务，能够有效降低大事务带来的复制延迟 [#5280](https://github.com/pingcap/tiflow/issues/5280)

## 错误修复

+ TiDB

    - 修复 `IN` 函数处理 `BIT` 数据类型时可能会导致 TiDB panic 的问题 [#33070](https://github.com/pingcap/tidb/issues/33070)
    - 修复 `UnionScan` 无法保序导致的查询结果不正确的问题 [#33175](https://github.com/pingcap/tidb/issues/33175)
    - 修复特定情况下 Merge Join 执行结果错误的问题 [#33042](https://github.com/pingcap/tidb/issues/33042)
    - 修复动态裁减模式下 `index join` 的结果可能会错误的问题 [#33231](https://github.com/pingcap/tidb/issues/33231)
    - 修复分区表的一些分区被 `DROP` 删除后数据可能不被 GC 垃圾回收的问题 [#33620](https://github.com/pingcap/tidb/issues/33620)
    - 修复集群的 PD 节点被替换后一些 DDL 语句会卡住一段时间的问题 [#33908](https://github.com/pingcap/tidb/issues/33908)
    - 修复了查询 `INFORMATION_SCHEMA.CLUSTER_SLOW_QUERY` 表导致 TiDB 服务器 OOM 的问题，在 Grafana dashboard 中查看慢查询记录的时候可能会触发该问题 [#33893](https://github.com/pingcap/tidb/issues/33893)
    - 修复系统变量 `max_allowed_packet` 不生效的问题 [#31422](https://github.com/pingcap/tidb/issues/31422)
    - 修复 TopSQL 模块的内存泄露问题 [#34525](https://github.com/pingcap/tidb/issues/34525)，[#34502](https://github.com/pingcap/tidb/issues/34502)
    - 修复 Plan Cache 对于 PointGet 计划有时候会出错的问题 [#32371](https://github.com/pingcap/tidb/issues/32371)
    - 修复在 RC 隔离情况下 Plan Cache 启用时可能导致查询结果错误的问题 [#34447](https://github.com/pingcap/tidb/issues/34447)

+ TiKV

    - 修复下线一个 TiKV 实例导致 Raft log lag 越来越大的问题 [#12161](https://github.com/tikv/tikv/issues/12161)
    - 修复待 merge 的 Region 无效会导致 TiKV panic 且非预期地销毁 peer 的问题 [#12232](https://github.com/tikv/tikv/issues/12232)
    - 修复从 v5.3.1、v5.4.0 升级到 v6.0.0 及以上版本时 TiKV 报 `failed to load_latest_options` 错误的问题 [#12269](https://github.com/tikv/tikv/issues/12269)
    - 修复内存资源不足时 append Raft log 导致 OOM 的问题 [#11379](https://github.com/tikv/tikv/issues/11379)
    - 修复销毁 peer 和批量分裂 Region 之间的竞争导致的 TiKV panic [#12368](https://github.com/tikv/tikv/issues/12368)
    - 修复 `stats_monitor` 线程陷入死循环导致短期内 TiKV 内存占用陡增的问题 [#12416](https://github.com/tikv/tikv/issues/12416)
    - 修复进行 Follower Read 时，可能会报 `invalid store ID 0` 错误的问题 [#12478](https://github.com/tikv/tikv/issues/12478)

+ PD

    - 修复 `not leader` 的 status code 有误的问题 [#4797](https://github.com/tikv/pd/issues/4797)
    - 修复在某些特殊情况下 TSO fallback 的问题 [#4884](https://github.com/tikv/pd/issues/4884)
    - 修复已清除的 `tombstone store` 信息在切换 PD leader 后再次出现的问题 [#4941](https://github.com/tikv/pd/issues/4941)
    - 修复 PD leader 转移后调度不能立即启动的问题 [#4769](https://github.com/tikv/pd/issues/4769)

+ TiDB Dashboard

    - 修复 Top SQL 功能无法统计到其开启时刻正在运行的 SQL 的问题 [#33859](https://github.com/pingcap/tidb/issues/33859)

+ TiFlash

    - 修复大量 INSERT 和 DELETE 操作后可能导致 TiFlash 数据不一致的问题 [#4956](https://github.com/pingcap/tiflash/issues/4956)

+ Tools

    + TiCDC

        - 优化了 ddl schema 缓存方式，降低了内存消耗 [#1386](https://github.com/pingcap/tiflow/issues/1386)
        - 修复了增量扫描特殊场景下的数据丢失问题 [#5468](https://github.com/pingcap/tiflow/issues/5468)

    + TiDB Data Migration (DM)

        - 修复 `start-time` 时区问题，从使用下游时区改为使用上游时区 [#5471](https://github.com/pingcap/tiflow/issues/5471)
        - 修复任务自动恢复后，DM 会占用更多磁盘空间的问题 [#3734](https://github.com/pingcap/tiflow/issues/3734)，[#5344](https://github.com/pingcap/tiflow/issues/5344)
        - 修复 checkpoint flush 可能导致失败行数据被跳过的问题 [#5279](https://github.com/pingcap/tiflow/issues/5279)
        - 修复了某些情况下，过滤 DDL 并在下游手动执行会导致同步任务不能自动重试恢复的问题 [#5272](https://github.com/pingcap/tiflow/issues/5272)
        - 修复在未设置 `case-sensitive: true` 时无法同步大写表的问题 [#5255](https://github.com/pingcap/tiflow/issues/5255)
        - 修复了在 `SHOW CREATE TABLE` 语句返回的索引中，主键没有排在第一位导致的 DM worker panic 的问题 [#5159](https://github.com/pingcap/tiflow/issues/5159)
        - 修复了当开启 GTID 模式或者任务自动恢复时，可能出现一段时间 CPU 占用高并打印大量日志的问题 [#5063](https://github.com/pingcap/tiflow/issues/5063)
        - 修复 DM Web UI offline 选项及其他使用问题 [#4993](https://github.com/pingcap/tiflow/issues/4993)
        - 修复上游 GTID 配置为空时，增量任务启动失败的问题 [#3731](https://github.com/pingcap/tiflow/issues/3731)
        - 修复空配置可能导致 dm-master panic 的问题 [#3732](https://github.com/pingcap/tiflow/issues/3732)

    + TiDB Lightning

        - 修复前置检查中没有检查本地磁盘空间以及集群是否可用的问题 [#34213](https://github.com/pingcap/tidb/issues/34213)
        - 修复 schema 路由错误的问题 [#33381](https://github.com/pingcap/tidb/issues/33381)
        - 修复 TiDB Lightning panic 时 PD 配置未正确恢复的问题 [#31733](https://github.com/pingcap/tidb/issues/31733)
        - 修复由 `auto_increment` 列的数据越界导致 local 模式导入失败的问题 [#29737](https://github.com/pingcap/tidb/issues/27937)
        - 修复 `auto_random`、`auto_increment` 列为空时 local 模式导入失败的问题 [#34208](https://github.com/pingcap/tidb/issues/34208)
