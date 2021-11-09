---
title: TiDB 5.3 Release Notes
---

# TiDB 5.3 Release Notes

发版日期：2021 年 11 月 16 日

TiDB 版本：5.3.0

在 5.3 版本中，你可以获得以下关键特性：

+ 
+ 
+ 

## 兼容性变化

> **注意：**
>
> 当从一个早期的 TiDB 版本升级到 TiDB 5.3.0 时，如需了解所有中间版本对应的兼容性更改说明，请查看对应版本的 [Release Note](/releases/release-notes.md)。

### 系统变量

|  变量名    |  修改类型    |  描述    |
| :---------- | :----------- | :----------- |
|tidb_enable_noop_functions  | 修改 | 此变量的控制范围不再包括 `CREATE TEMPORARY TABLE` 和 `DROP TEMPORARY TABLE` 行为。 |
| [`tidb_enable_pseudo_for_outdated_stats`](/system-variables.md#tidb_enable_pseudo_for_outdated_stats-从-v530-版本开始引入) | 新增 | 此变量用于控制优化器在一张表上的统计信息过期时的行为。默认值为 `ON`，当表数据被修改的行数大于该表总行数的 80% （该比例可通过 [`pseudo-estimate-ratio`](/tidb-configuration-file.md#pseudo-estimate-ratio) 配置项调整） 时，优化器认为该表上除总行数以外的统计信息不再可靠，转而使用 pseudo 统计信息。将该变量值设为 `OFF` 后，即使统计信息过期，优化器也仍会使用该表上的统计信息。|
|[`tidb_enable_tso_follower_proxy`](/system-variables.md#tidb_enable_tso_follower_proxy-从-v53-版本开始引入) | 新增  | 此变量用于开启或关闭 TSO Follower Proxy 特性。默认值为 `OFF`，代表关闭TSO Follower Proxy 特性。此时，TiDB 仅会从 PD leader 获取 TSO。当开启该特性之后，TiDB 在获取 TSO 时会将请求均匀地发送到所有 PD 节点上，通过 PD follower 转发 TSO 请求，从而降低 PD leader 的 CPU 压力。 |
|[`tidb_tso_client_batch_max_wait_time`](/system-variables.md#tidb_tso_client_batch_max_wait_time-从-v53-版本开始引入) | 新增 | 此变量用于设置 TiDB 向 PD 请求 TSO 时进行一次攒批操作的最大等待时长。默认值为 `0`，即不进行额外的等待。 |
| `tmp_table_size` | 修改 | 更名为 `tidb_tmp_table_size`，不再保留 `tmp_table_size`。升级前global 级别tmp_table_size 有值，升级后需要手动转换为tidb_tmp_table_size。 |
| tidb_tmp_table_max_size | 新增  | 此变量用于限制单个[临时表](/temporary-table.md)的最大大小，临时表超出该大小后报错。 |
|  |  |  |

### 配置文件参数

|  配置文件    |  配置项    |  修改类型    |  描述    |
| :---------- | :----------- | :----------- | :----------- |
| TiDB | [`tidb_tmp_table_max_size`](/system-variables.md#tidb_tmp_table_max_size-从-v53-版本开始引入) | 新增 | 此变量用于限制单个[临时表](/temporary-table.md)的最大大小，临时表超出该大小后报错。｜
| TiDB | [`prepared-plan-cache.capacity`](/tidb-configuration-file.md#capacity)  | 此配置项用于控制缓存语句的数量。默认值从 `100` 修改为 `1000`。 |
| TiKV | [`storage.reserve-space`](/tikv-configuration-file.md#reserve-space）| 此配置项用于控制 TiKV 启动时用于保护磁盘的预留空间。从 v5.3.0 起，预留空间的 80% 用作磁盘空间不足时运维操作所需要的额外磁盘空间，剩余的 20% 为磁盘临时文件。 |
|  | memory-usage-limit  | 以前的版本没有 memory-usage-limit 参数， 升级后改参数值根据 storage.block-cache.capacity来计算 |
| PD | [`log.file.max-days`](/pd-configuration-file.md#max-days) | 修改 | 此配置项用于控制日志保留的最长天数。默认值从 `1` 修改为 `0`。 ｜
| PD | [`log.file.max-backups`](/pd-configuration-file.md#max-backups) | 修改 | 此配置项用于控制日志文件保留的最大个数。默认值从 `7` 修改为 `0`。｜
| PD | [`patrol-region-interval`](/pd-configuration-file.md#patrol-region-interval) | 修改 |此配置项用于控制 replicaChecker 检查 Region 健康状态的运行频率，越短则运行越快，通常状况不需要调整。默认值从 `100ms` 修改为 `10ms`。 ｜
| PD | [`max-snapshot-count`](/pd-configuration-file.md#max-snapshot-count) | 修改 |此配置项用于控制单个 store 最多同时接收或发送的 snapshot 数量，调度受制于这个配置来防止抢占正常业务的资源。默认值从 `3` 修改为 `64`。 ｜
| PD | [`max-pending-peer-count`](/pd-configuration-file.md#max-pending-peer-count) | 修改 |此配置项用于控制单个 store 的 pending peer 上限，调度受制于这个配置来防止在部分节点产生大量日志落后的 Region。默认值从 `16` 修改为 `64`。 ｜

### 其他

- 临时表：

    - 如果在 v5.3.0 升级前创建了本地临时表，这些临时表实际为普通表，在升级后也会被 TiDB 当成普通表处理。在 v5.3.0 上创建的全局临时表在降级后会被当作普通表处理，导致数据错误。
    - TiCDC 和 BR 从 v5.3.0 开始支持[全局临时表](/temporary-table.md#全局临时表)。如果使用 v5.3.0 以下版本同步全局临时表到下游，会导致表定义错误。 
    - 通过 TiDB 生态工具导入的集群、恢复后的集群、同步的下游集群必须是 TiDB v5.3.0 及以上版本，否则报错。
    - 关于临时表的更多兼容性信息，请参考 [与 MySQL 临时表的兼容性](/temporary-table.md#与-mysql-临时表的兼容性) 和 [与其他 TiDB 功能的兼容性限制](/temporary-table.md#与其他-tidb-功能的兼容性限制)。

- 修正 `SHOW CREATE VIEW` 不需要 `SHOW VIEW` 权限的问题，现在用户必须具备 `SHOW VIEW` 才允许执行 `SHOW CREATE VIEW` 语句。
- 系统变量 `sql_auto_is_null` 被加入 Noop Funciton 中，当 `tidb_enable_noop_functions = 0/OFF` 时，修改改变量会报错。
- 不再允许执行 `GRANT ALL ON performance_schema.*` 语法，现在 TiDB 执行该语句会报错。
- v5.3.0之前，对于新增索引，analyze 时间不受设定时间的限制，tidb_auto_analyze_start_time 和 tidb_auto_analyze_end_time 时间段内将不会出发 auto analyze
- plugin 的默认路径从 "" 改为 /data/deploy/plugin

## 新功能

### SQL

- **SQL 接口设置数据放置规则（实验特性）**

    增加 `[CREATE | ALTER] PLACEMENT POLICY` 语句支持，提供 SQL 接口设置数据放置规则。通过该功能，用户可以指定任意连续数据按照不同地域，机房，机柜，主机，硬件，副本数规则进行部署，满足低成本，高可用，灵活多变的业务诉求。该功能可以实现以下业务场景：

    - 跨区域放置数据以改善局部访问性能
    - 多业务数据库合并，降低大量数据库的常规运维管理成本，并通过规则配置实现业务资源隔离
    - 增加更重要数据的副本数，提高业务可用性，数据可靠性
    - 将最新数据存入 SSD，历史数据存入 HDD，降低归档数据存储成本
    - 把热点数据的 leader 放到高性能的 TiKV 实例上
    - 将不相关的数据分离到不同的存储中以提高可用性

    [用户文档](/)

- **临时表**

    增加 CREATE [GLOBAL] TEMPORARY TABLE 语句支持，支持创建临时表，方便业务管理中间计算的临时数据。临时表中的数据均保存在内存中，用户可通过 tidb_tmp_table_max_size 变量限制临时表的内存大小。TiDB 支持以下两种临时表：

    - Global 临时表
        - 对集群内所有 session 可见，表结构持久化。
        - 提供事务级别的数据隔离，数据只在事务内有效，事务结束后自动删除数据。
    - Local 临时表
        - 只对当前 session 可见，表结构不持久化。
        - 支持重名，用户无需为业务设计复杂的表命名规则。
        - 提供会话级别的数据隔离，降低业务设计复杂度，会话结束后删除临时表。

    [用户文档](/)    

- **支持 `FOR UPDATE OF TABLES` 语法**

    对于存在多表 join 的语句，支持只对 `OF TABLES` 中包含的表关联的行进行悲观锁加锁操作。 

    [用户文档](/sql-statement-select.md), [#28689](https://github.com/pingcap/tidb/issues/28689) 

- **表/分区表属性设置**

    增加 `ALTER TABLE [PARTITION] ATTRIBUTES` 语句支持，允许用户设置表和分区的表属性。目前支持设置 `merge_option` 属性。通过设置 `merge_option` 属性，用户可以显式控制 Region 是否合并。

    应用场景：当用户 `SPLIT TABLE` 之后，如果超过一定时间后没有插入数据，空 Region 默认会被自动合并。此时，可以通过该功能设置表属性为 `merge_option=deny`，避免 Region 的自动合并。

    [用户文档](/table-attributes.md), [#3839](https://github.com/tikv/pd/issues/3839)

### 安全

- **支持为 TiDB Dashboard 创建最小权限用户**

    TiDB Dashboard 的账号体系与 TiDB SQL 用户一致，并基于 TiDB SQL 用户的权限进行 TiDB Dashboard 授权验证。TiDB Dashboard 所需的权限较少，甚至可以只有只读权限。可以基于最小权限原则配置合适的用户访问 TiDB Dashboard，减少高权限用户的使用场景。

    建议为访问 TiDB Dashboard 创建一个最小权限的 SQL 用户，并用该用户登录 TiDB Dashboard，避免使用高权限用户，提升安全性。

    [用户文档](/dashboard/dashboard-user.md)   

### 性能

- **优化 PD 时间戳处理流程**

    优化 TiDB 时间戳处理流程，支持通过开启 PD follower proxy 和调整 PD client 批量请求 TSO 的最大等待时长，降低 PD leader 时间戳处理负载，提升系统整体可扩展性。

    - 支持通过 [`tidb_enable_tso_follower_proxy`](/system-variables.md#tidb_enable_tso_follower_proxy-从-v53-版本开始引入) 系统变量设置 PD follower proxy 功能开关。在 PD 时间戳请求负载过高的情况下，通过开启 PD follower proxy，可以将 follower 上请求周期内收集到的 TSO request 批量转发到 leader 节点，有效减少 client 与 leader 的直接交互次数，降低 leader 的负载，提升 TiDB 整体性能。

    > **注意：**
    >
    > 在 client 数较少的情况下，PD leader 负载不高的情况下，不建议开启 PD follower proxy 功能。

    - 支持通过 [`tidb_tso_client_batch_max_wait_time`](/system-variables.md#tidb_tso_client_batch_max_wait_time-从-v53-版本开始引入) 系统变量设置 PD client 批量请求 TSO 的最大等待时间，单位毫秒。在 PD TSO 请求负载过高的情况下，通过调大该参数，可以提升一次请求 TSO 的数量，降低 PD 负载，提升吞吐。

    > **注意：**
    >
    > 在 TSO 请求负载不高的情况下，不建议调整该参数。 

    [用户文档](/system-variables.md#tidb_tso_client_batch_max_wait_time-从-v53-版本开始引入), [#3149](https://github.com/tikv/pd/issues/3149)  

### 稳定性

- **支持 Raft 多数副本丢失时数据的在线恢复能力（实验特性）**

    增加 PD-CTL RECOVER-STORE-FAILURE 语句支持，提供在线恢复 TiKV 实例能力。通过该功能，可以实现：

    - 在线恢复所有 Raft 多数副本丢失的 Region 可读写。
    - 保证恢复所有 Region 后没有数据空洞。

    需要注意的是，Raft 多数副本失败的情况下无法避免已提交数据的丢失。

    [用户文档](/online-unsafe-recovery.md), [#10483](https://github.com/tikv/tikv/issues/10483)  

### 数据迁移

- **提高 DM 复制性能**

    支持以下功能，实现以更低的延迟将数据从 MySQL 同步数据到 TiDB。

    - 合并单行数据的多次变更（Compact multiple updates on a single row into one statement）
    - 点查更新合并为批量操作（Merge batch updates of multiple rows into one statement）
    - 异步保存检查点（Async Checkpoint）

- **增加 DM 的 OpenAPI 以更方便地管理集群（实验特性）**

    DM 提供 OpenAPI 功能，用户可通过 OpenAPI 对 DM 集群进行查询和运维操作。OpenAPI 的总体功能和 [dmctl 工具](https://docs.pingcap.com/zh/tidb-data-migration/stable/dmctl-introduction)类似。

    当前 OpenAPI 功能为实验特性，默认关闭，不建议在生产环境中使用。
   
    [用户文档](https://docs.pingcap.com/zh/tidb-data-migration/stable/open-api)  

- **TiDB Lightning 分布式并行导入**

    TiDB Lightning 支持用户同时部署多个 Lightning，并行地将单表或者多表数据迁移 TiDB。 该功能无需特别的配置，在不改变用户使用习惯的同时，极大提高了用户的数据迁移能力，助力大数据量业务架构升级，在生产环境使用 TiDB。

    在产品性能测试中，使用 x 个 Lightning 导入整体大小 x TB MySQL 分表数据到 TiDB 单表，总耗时 x h，平均单台 Lightning 速度达到 x GB/h。（数据待更新）。此外在 MySQL 分表数据聚合迁移到 TiDB 的场景中，MySQL 分表之间可能有冲突数据（主键/唯一键索引相同的数据），Lightning 也支持了数据导入过程中检查冲突数据的功能，用户可以使用该功能发现冲突数据，然后按照业务规则进行处理，冲突检测使用文档（待更新）。

    [用户文档](/tidb-lightning/tidb-lightning-distributed-import.md)  

- **TiDB Lightning 执行任务前的检查项**

    TiDB Lightning 增加了执行前检查配置的功能。默认开启。该功能会自动进行一些磁盘空间和执行配置的常规检查，主要目的是确保后续的整个导入过程顺利。

    [用户文档](tidb-lightning/tidb-lightning-prechecks.md) 

- **Lightning 支持导入 GBK 编码文件** 

    [用户文档](/tidb-lightning/tidb-lightning-configuration.md)

- **Lightning 支持忽略部分错误行（实验特性）**

    从 TiDB 5.3.0 开始，你可以配置 TiDB Lightning 以跳过诸如无效类型转换、唯一键冲突等错误，让导入任务持续进行，就如同出现错误的行数据不存在一样。你可以依据生成的报告，手动修复这些错误。该功能适用于以下场景：

    - 要导入的数据有少许错误
    - 手动定位错误比较困难
    - 如果遇到错误就重启 TiDB Lightning，代价太大

    TiDB Lightning 错误处理功能是实验特性。**不建议**在生产环境中仅依赖该功能处理相关错误。

    [用户文档](/tidb-lightning/tidb-lightning-error-resolution.md)

- **Sync-diff-inspector 优化**

    - 大幅提升了对比速度，由原来的 375 MB/s 提升至 700 MB/s
    - 对比过程中对 TiDB 节点的内存消耗降低近一半
    - 优化了用户交互界面，在对比过程中可以显示进度
   
     [用户文档](/sync-diff-inspector/sync-diff-inspector-overview.md)

### 问题诊断效率

- **保存和恢复集群现场信息**

    在定位排查 TiDB 集群问题时，用户经常需要提供系统和查询计划相关的信息。为了帮助用户更方便地获取相关信息，更高效地排查集群问题，TiDB 在 v5.3.0 中引入了 `PLAN REPLAYER` 命令，用于“一键”保存和恢复现场问题的相关信息，提升查询计划问题诊断的效率，同时方便将问题归档管理。

    `PLAN REPLAYER` 主要功能如下：

    - 导出排查现场 TiDB 集群的相关信息，导出为 ZIP 格式的文件用于保存。
    - 在任意 TiDB 集群上导入另一 TiDB 集群现场信息的 ZIP 文件。

    [用户文档](/sql-plan-replayer.md), [#26325](https://github.com/pingcap/tidb/issues/26325)

### TiDB 数据共享订阅

- **TiCDC 支持灾备场景下的最终一致性复制**

    在主从灾备架构下，当生产集群（即 TiCDC 同步的上游集群）发生灾难、且短时间内无法恢复对外提供服务时，TiCDC 具备保证从集群数据一致性的能力，并允许业务快速的将流量切换至从集群，避免数据库长时间不可用而对业务造成影响。

    该功能支持 TiCDC 将 TiDB 集群的增量数据复制到备用关系型数据库 TiDB/Aurora/MySQL/MariaDB，在 TiCDC 正常同步没有延迟的情况下，上游发生灾难后，可以在 30 分钟内将下游集群恢复到上游的某个 snapshot 状态，并且允许丢失的数据小于 5 分钟。即 RPO <= 30min，RTO <= 5min。

    [用户文档](/ticdc/manage-ticdc.md)  

### 部署及运维

- **持续性能分析（实验特性）**

    TiDB Dashboard 引入持续性能分析功能，提供在集群运行状态时自动保存实例性能分析结果的能力，通过火焰图的形式提高了 TiDB 集群性能的可观测性，有助于缩短故障诊断时间。

    该功能默认关闭，需进入 TiDB Dashboard 持续性能分析页面开启。

    持续性能分析功能必须使用 TiUP 1.7.0 及以上版本升级或安装的集群才可使用。

    [用户文档](/dashboard/continuous-profiling.md)  

### 遥测

TiDB 在遥测中新增收集 <列出本次新增遥测内容>。

若要了解所收集的信息详情及如何禁用该行为，请参见[遥测](/telemetry.md)文档。

## 移除功能

从 TiCDC v5.3.0 版本开始, TiDB 集群之间的环形同步功能（v5.0 实验特性）被移除。

## 提升改进

+ TiDB

    - 当 coprocessor 遇到锁时，在调试日志中显示受影响的 SQL 语句帮助诊断问题 [#27718](https://github.com/pingcap/tidb/issues/27718)
    - 在 SQL 逻辑层备份和恢复数据时，支持显示备份和恢复数据的大小 [#27247](https://github.com/pingcap/tidb/issues/27247)
    - 改进 `tidb_analyze_version=2` 时 ANALYZE 默认的收集逻辑，提高收集速度并且降低资源开销
    - 引入语法 `ANALYZE TABLE table_name COLUMNS col_1, col_2, ..., col_n`，为宽表提供只收集一部分列统计信息的方案。提高宽表收集统计信息的速度。

+ TiKV

    - 增强磁盘空间防护能力，提升存储稳定性。

        针对 TiKV 遇到磁盘写满错误时可能 Panic 的问题，为磁盘剩余空间引入两级阈值防御机制，避免超额流量耗尽磁盘空间。同时，提供阈值触发时的空间回收能力。当剩余空间触发阈值时，部分写操作会失败，并返回 disk full 错误和盘满节点列表。此时，可以通过 `Drop/Truncate Table` 或者扩容等方式来回收空间，恢复服务。

    - 简化 L0 层流控算法 [#10879](https://github.com/tikv/tikv/issues/10879)
    - 优化 raft client 错误日志的收集 [#10944](https://github.com/tikv/tikv/pull/10944)
    - 优化日志线程以避免其成为性能瓶颈 [#10841](https://github.com/tikv/tikv/issues/10841)
    - 添加更多的写入查询统计类型 [#10507](https://github.com/tikv/tikv/issues/10507)

+ PD

    - 热点调度器的 QPS 维度支持更多的写请求类型 [#3869](https://github.com/tikv/pd/issues/3869)
    - 通过动态调整 Balance Region 调度器的重试上限，优化该调度器的性能 [#3744](https://github.com/tikv/pd/issues/3744)
    - 将 TiDB Dashboard 升级至 v2021.10.08.1 [#4070](https://github.com/tikv/pd/pull/4070)
    - 允许 Evict Leader 调度器调度拥有不健康副本的 Region [#4093](https://github.com/tikv/pd/issues/4093)
    - 优化调度器退出的速度 [#4146](https://github.com/tikv/pd/issues/4146)

+ TiFlash

    - 显著优化了 TableScan 算子的执行效率
    - 优化了 Exchange 算子的执行效率
    - 减少了存储引擎的 GC 过程中的写放大和内存使用
    - 改进了 TiFlash 重启时的稳定性和可用性，减少了重启结束后短时间内查询可能失败的情况
    - 增加支持下推多个新的字符串，时间等函数到 MPP 引擎

        - 字符串函数：LIKE pattern，FORMAT(), LOWER(), LTRIM(), RTRIM(), SUBSTRING_INDEX(), TRIM(), UCASE(), UPPER()
        - 数学函数：ROUND(decimal, int)
        - 日期时间函数：HOUR(), MICROSECOND(), MINUTE(), SECOND(), SYSDATE()
        - 类型转换函数：CAST(time, real)
        - 聚合函数：GROUP_CONCAT(), SUM(enum)

    - 提供了 512 位 SIMD 支持
    - 增强了对过期的数据版本的清理算法，减少磁盘使用量及提高读文件性能
    - 解决了用户在某些非Linux平台系统上查看 dashboard 时，无法获取内存或CPU等相关信息
    - 统一 TiFlash 日志文件的命名风格（与 TiKV 保持一致），并支持动态修改 logger.count、logger.size
    - 完善了列存文件的数据校验能力（checksums，实验功能）

+ Tools

    + TiCDC

        - 通过修改 Kafka sink 配置项 `MaxMessageBytes` 的默认值，由 64 MB 减小为 1 MB，以修复消息过大会被 Kafka Broker 拒收的问题 [#3104](https://github.com/pingcap/ticdc/pull/3104)
        - 减少同步链路中的内存占用 [#2553](https://github.com/pingcap/ticdc/issues/2553)[#3037](https://github.com/pingcap/ticdc/pull/3037) [#2726](https://github.com/pingcap/ticdc/pull/2726) 
        - 优化监控项和告警规则，提升了同步链路、内存 GC、存量数据扫描过程的可观测性 [#2735](https://github.com/pingcap/ticdc/pull/2735) [#1606](https://github.com/pingcap/ticdc/issues/1606) [#3000](https://github.com/pingcap/ticdc/pull/3000) [#2985](https://github.com/pingcap/ticdc/issues/2985) [#2156](https://github.com/pingcap/ticdc/issues/2156)
        - 当同步任务状态正常时，不再显示历史错误信息，避免误导用户 [#2242](https://github.com/pingcap/ticdc/issues/2242)

## Bug 修复

+ TiDB

    - 修复在分区中下推聚合算子时，因浅拷贝 schema 列导致执行计划出错，进而导致执行时报错的问题 [#27797](https://github.com/pingcap/tidb/issues/27797) [#26554](https://github.com/pingcap/tidb/issues/26554)
    - 修复 `plan cache` 无法感知 `unsigned` 标志变化的问题 [#28254](https://github.com/pingcap/tidb/issues/28254)
    - 修复当分区功能出现 `out of range` 时 `partition pruning` 出错的问题 [#28233](https://github.com/pingcap/tidb/issues/28233)
    - 修复在某些情况下 Planner 可能缓存无效 `join` 计划的问题 [#28087](https://github.com/pingcap/tidb/issues/28087)
    - 修复 hash 列为 `enum` 时构建错误 `IndexLookUpJoin` 的问题 [#27893](https://github.com/pingcap/tidb/issues/27893)
    - 修复批处理客户端在某些罕见情况下回收空闲连接可能会阻塞发送请求的问题 [#27688](https://github.com/pingcap/tidb/pull/27688)
    - 修复当 TiDB Lightning 在目标集群上执行校验失败时 panic 的问题 [#27686](https://github.com/pingcap/tidb/pull/27686)
    - 修复某些情况下 `date_add` 和 `date_sub` 函数执行结果错误的问题 [#27232](https://github.com/pingcap/tidb/issues/27232)
    - 修复 `hour` 函数在向量化表达式中执行结果错误的问题 [#28643](https://github.com/pingcap/tidb/issues/28643)
    - 修复连接到 MySQL 5.1 或更早的客户端时存在的认证问题 [#27855](https://github.com/pingcap/tidb/issues/27855)
    - 修复当新增索引时自动分析可能会在指定时间之外触发的问题 [#28698](https://github.com/pingcap/tidb/issues/28698)
    - 修复设置任何会话变量都会使 `tidb_snapshot` 失效的问题 [#28683](https://github.com/pingcap/tidb/pull/28683)
    - 修复在有大量 `miss-peer region` 的集群中 BR 不可用的问题 [#27534](https://github.com/pingcap/tidb/issues/27534)
    - 修复当不支持的 `cast` 被下推到 TiFlash 时出现的非预期错误，例如 `tidb_cast to Int32 is not supported` [#23907](https://github.com/pingcap/tidb/issues/23907)
    - 修复 `%s value is out of range in '%s'` 报错中缺失 `DECIMAL overflow` 信息的问题 [#27964](https://github.com/pingcap/tidb/issues/27964)
    - 修复 MPP 节点的可用性检测在某些边界场景中无法工作的问题 [#3118](https://github.com/pingcap/tics/issues/3118)
    - 修复分配 `MPP task ID` 时出现 `DATA RACE` 的问题 [#27952](https://github.com/pingcap/tidb/issues/27952)
    - 修复删除空的 `dual table` 后 MPP 查询出现 `index out of range` 报错的问题 [#28250](https://github.com/pingcap/tidb/issues/28250)
    - 修复运行 MPP 查询时出现 `invalid cop task execution summaries length` 相关日志的问题 [#1791](https://github.com/pingcap/tics/issues/1791)
    - 修复运行 MPP 查询时出现 `cannot found column in Schema column` 报错的问题 [#28149](https://github.com/pingcap/tidb/pull/28149)
    - 修复 TiDB 在 TiFlash 关闭时可能出现 panic 的问题 [#28096](https://github.com/pingcap/tidb/issues/28096)
    - 移除对基于 3DES (三重数据加密算法) 不安全的 TLS 加密套件的支持 [#27859](https://github.com/pingcap/tidb/pull/27859)
    - 修复因 Lightning 前置检查会连接已下线的 TiKV 节点而导致导入失败的问题 [#27826](https://github.com/pingcap/tidb/pull/27826)
    - 修复在导入太多文件到表时前置检查花费太多时间的问题 [#27605](https://github.com/pingcap/tidb/issues/27605)
    - 修复表达式重写时 `between` 推断出错误排序规则的问题 [#27146](https://github.com/pingcap/tidb/issues/27146)
    - 修复 `group_concat` 函数没有考虑排序规则的问题 [#27429](https://github.com/pingcap/tidb/issues/27429)
    - 修复 `extract` 函数处理负值时的问题 [#27236](https://github.com/pingcap/tidb/issues/27236)
    - 修复当设置 `NO_UNSIGNED_SUBTRACTION` 时创建分区失败的问题 [#26765](https://github.com/pingcap/tidb/issues/26765)
    - 避免在列修剪和聚合下推中使用有副作用的表达式 [#27106](https://github.com/pingcap/tidb/issues/27106)
    - 删除无用的 gRPC 日志 [#24190](https://github.com/pingcap/tidb/issues/24190)
    - 限制有效的小数点长度以修复精度相关的问题 [3091](https://github.com/pingcap/tics/issues/3091)
    - 修复 `plus` 表达式中检查溢出方法出错的问题 [26977](https://github.com/pingcap/tidb/issues/26977)
    - 修复当导出带有 `new collation` 数据的表的统计信息时报 `data too long` 错误的问题 [27024](https://github.com/pingcap/tidb/issues/27024)
    - 修复 `TIDB_TRX` 中不包含重试事务的问题 [28670](https://github.com/pingcap/tidb/pull/28670)
    - 修复配置项 `plugin_dir` 的默认值错误问题 [28084](https://github.com/pingcap/tidb/issues/28084)  

+ TiKV

    - 修复 Region 迁移时 Raftstore 模块出现死锁导致 TiKV 不可用的问题。用户可通过关闭调度并重启出问题的 TiKV 来临时应对。[#10909](https://github.com/tikv/tikv/issues/10909)
    - 修复因 Congest 错误而导致的 CDC 频繁增加 scan 重试的问题 [#11082](https://github.com/tikv/tikv/issues/11082)
    - 修复因 channel 打满而导致的 Raft 断连情况 [#11047](https://github.com/tikv/tikv/issues/11047)
    - 修复 Raft client 中 batch 消息过大的问题 [#9714](https://github.com/tikv/tikv/issues/9714)
    - 修复 `resolved_ts` 中协程泄漏的问题 [#10965](https://github.com/tikv/tikv/issues/10965)
    - 修复当 response 大小超过 4 GiB 时 Coprocessor panic 的问题 [#9012](https://github.com/tikv/tikv/issues/9012)
    - 修复当一个 snapshot 文件无法被垃圾清理 (GC) 时 snapshot GC 会缺失 GC snapshot 文件的问题 [#10813](https://github.com/tikv/tikv/issues/10813)
    - 修复当处理 Coprocessor 请求时因超时而导致 panic 的问题 [#10852](https://github.com/tikv/tikv/issues/10852)
    - 修复因统计线程监控数据导致的内存泄漏 [#11195](https://github.com/tikv/tikv/issues/11195)
    - 修复在某些平台获取 cgroup 信息导致 panic 的问题 [#10980](https://github.com/tikv/tikv/pull/10980) 
+ PD

    - 修复因超过副本配置数量而导致错误删除带有数据且处于 pending 状态的副本的问题 [#4045](https://github.com/tikv/pd/issues/4045)
    - 修复 PD 未能及时修复 Down Peer 副本的问题 [#4077](https://github.com/tikv/pd/issues/4077)
    - 修复 Scatter Range 调度器无法对空 Region 进行调度的问题 [#4118](https://github.com/tikv/pd/pull/4118)
    - 修复 key manager 占用过多 CPU 的问题 [#4071](https://github.com/tikv/pd/issues/4071)
    - 修复热点调度器变更配置的过程中可能会存在的数据竞争问题 [#4159](https://github.com/tikv/pd/issues/4159)
    - 修复因 Region syncer 卡住而导致 leader 选举慢的问题 [#3936](https://github.com/tikv/pd/issues/3936)

+ TiFlash

    - 修复 TiFlash 在部分平台上由于缺失 `nsl` 库而无法启动的问题
    - 阻止 wait index 无限等待，防止写入压力较重时 TiFlash 长时间等待数据同步而无法提供服务的问题（新增默认超时为5分钟）
    - 解决了当日志体量很大时，用户搜索日志很慢或搜索不出的问题
    - 解决了搜索比较久远的历史日志时，只能搜索出最近的一部分日志的问题
    - 修复在打开 new collation 的情况下可能出现的结果错误
    - 修复 SQL 语句中含有极长嵌套表达式时可能出现的解析错误
    - 修复 Exchange 算子中可能出现的 `Block schema mismatch` 错误
    - 修复 Decimal 类型比较时可能出现的 `Can't compare` 错误
    - 修复 `left/substring` 函数中的 `3rd arguments of function substringUTF8 must be constants` 错误 

+ Tools

    + TiCDC

        - 修复当上游 TiDB 实例意外退出时，TiCDC 同步任务推进可能停滞的问题 [#3061](https://github.com/pingcap/ticdc/issues/3061)
        - 修复当 TiKV 向同一 Region 发送重复请求时，TiCDC 进程 panic 的问题 [#2386](https://github.com/pingcap/ticdc/issues/2386)
        - 修复在验证下游 TiDB/MySQL 可用性时产生的不必要的 CPU 消耗 [#3073](https://github.com/pingcap/ticdc/issues/3073)
        - 修复 TiCDC 产生的 Kafka 消息体积不受 `max-message-size` 约束的问题 [#2962](https://github.com/pingcap/ticdc/issues/2962)
        - 修复当写入 Kafka 消息发生错误时，TiCDC 同步任务推进可能停滞的问题 [#2978](https://github.com/pingcap/ticdc/issues/2978)
        - 修复当开启 `force-replicate` 时，可能某些没有有效索引的分区表被忽略的问题 [#2834](https://github.com/pingcap/ticdc/issues/2834)
        - 修复当扫描存量数据耗时过长时，可能由于 TiKV 进行 GC 而导致存量数据扫描失败的问题 [#2470](https://github.com/pingcap/ticdc/issues/2470)
        - 修复在将某些类型的列编码为 Open Protocol 格式时，TiCDC 进程可能 panic 的问题 [#2758](https://github.com/pingcap/ticdc/issues/2758)
        - 修复在将某些类型的列编码为 Avro 格式时，TiCDC 进程可能 panic 的问题 [#2648](https://github.com/pingcap/ticdc/issues/2648)
    
    + TiDB Binlog

        - 修复当大部分表被过滤掉时，在某些特殊的负载下，checkpoint 不更新的问题 [#1075](https://github.com/pingcap/tidb-binlog/pull/1075)