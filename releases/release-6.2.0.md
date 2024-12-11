---
title: TiDB 6.2.0 Release Notes
summary: 了解 TiDB 6.2.0 版本的新功能、兼容性变更、改进提升，以及错误修复。
---

# TiDB 6.2.0 Release Notes

发版日期：2022 年 8 月 23 日

TiDB 版本：6.2.0-DMR

> **注意：**
>
> TiDB 6.2.0-DMR 的用户文档已[归档](https://docs-archive.pingcap.com/zh/tidb/v6.2)。如无特殊需求，建议使用 TiDB 数据库的[最新 LTS 版本](https://docs.pingcap.com/zh/tidb/stable)。

在 6.2.0-DMR 版本中，你可以获得以下关键特性：

- TiDB Dashboard 支持[可视化执行计划](https://docs.pingcap.com/zh/tidb/v6.2/dashboard-slow-query#图形化执行计划介绍)，查询计划展示更直观。
- TiDB Dashboard 新增 [Monitoring 页面](/dashboard/dashboard-monitoring.md)用于性能分析和优化。
- TiDB [锁视图支持乐观事务被阻塞的信息](/information-schema/information-schema-data-lock-waits.md)，方便快速定位锁冲突。
- TiFlash 引入[新的存储格式 PageStorage V3](/tiflash/tiflash-configuration.md#配置文件-tiflashtoml)，提升稳定性和性能。
- 实现[细粒度数据交换 (shuffle)](/system-variables.md#tiflash_fine_grained_shuffle_batch_size-从-v620-版本开始引入) 使窗口函数 (Window function) 可以利用多线程并行计算。
- 引入新的 DDL 并行执行框架，减少 DDL 阻塞，大幅提升执行效率。
- TiKV 支持[自适应调整 CPU 使用率](/tikv-configuration-file.md#后台限流)，确保数据库稳定高效运行。
- 支持 [point-in-time recovery (PITR)](/br/backup-and-restore-overview.md)，允许恢复备份集群的历史任意时间点的快照。
- TiDB Lightning 使用物理导入模式[导入时限制调度范围从集群降低到表级别](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#导入时暂停-pd-调度的范围)。
- Backup & Restore (BR) 支持[恢复用户和权限数据](/br/br-snapshot-guide.md#恢复-mysql-数据库下的表)，备份恢复体验更平滑。
- TiCDC 支持[过滤指定类型的 DDL 事件](/ticdc/ticdc-filter.md#event-filter-事件过滤器-从-v620-版本开始引入)，解锁更多数据同步场景。
- 事务中支持 [`SAVEPOINT` 机制](/sql-statements/sql-statement-savepoint.md)，可以灵活地控制事务内的回退节点。
- [单 `ALTER TABLE` 语句增删改多个列或索引](/sql-statements/sql-statement-alter-table.md)，方便实现 SQL 功能，提升产品易用性。
- 支持 [RawKV 跨集群复制](/tikv-configuration-file.md#api-version-从-v610-版本开始引入)。

## 新功能

### SQL

* 正式支持通过 SQL 语句对 TiFlash 副本立即触发物理数据整理 (Compaction)

    TiFlash 后台会依据特定条件、自动对物理数据进行整理 (Compaction)，减少无用数据的积压，并优化数据存储结构。在数据整理被自动触发前，TiFlash 数据表中往往存在一定量的无用数据。该特性支持用户自行选择合适的时机、手动执行 SQL 语句来对 TiFlash 中的物理数据立即进行整理，从而减少存储空间占用，并提升查询性能。此功能在 TiDB v6.1 作为一项实验功能引入，在 v6.2.0 版本正式发布。

    [用户文档](/sql-statements/sql-statement-alter-table-compact.md#alter-table--compact) [#4145](https://github.com/pingcap/tiflash/issues/4145) @[breezewish](https://github.com/breezewish)

### 可观测性

* TiDB Dashboard 从 PD 拆离

    将 TiDB Dashboard 拆分到 Monitoring 节点，减少监控组件对 PD 节点的影响，让 PD 节点更加稳定。

    @[Hawkson-jee](https://github.com/Hawkson-jee)

* TiDB Dashboard 新增 Monitoring 页面

    TiDB Dashboard 新增 Monitoring 页面，展示在业务性能调优中所需的核心指标。用户可基于数据库时间的[系统优化方法](/performance-tuning-methods.md)，利用该页面进行性能分析和优化。用户可以从全局、自顶向下的角度分析用户响应时间和数据库时间，确认用户响应时间的瓶颈是否在数据库中。如果瓶颈在数据库中，你可以通过数据库时间概览和 SQL 延迟的分解，定位数据库内部的瓶颈点，并进行针对性的优化。

    [用户文档](/dashboard/dashboard-monitoring.md) [#1381](https://github.com/pingcap/tidb-dashboard/issues/1381) @[YiniXu9506](https://github.com/YiniXu9506)

* TiDB Dashboard 支持可视化执行计划

    在 Statements 和 Slow Query 中提供可视化执行计划和基础问题诊断的能力。这是一种全新的查询计划的展示方式，目标是通过图形化的手段展示 Query 查询计划的每个步骤，从而使得用户能够更加直观方便地了解查询执行计划的细节。对于复杂的大型查询语句，可视化的展示方式对于深入理解其执行过程大有裨益。另外，系统会自动对每一个 Query 的执行计划进行分析，发现执行计划中潜在问题，提供优化方向。用户可以采用这些优化建议，降低特定 Query 的查询时长。

    [用户文档](https://docs.pingcap.com/zh/tidb/v6.2/dashboard-slow-query#图形化执行计划介绍) [#1224](https://github.com/pingcap/tidb-dashboard/issues/1224) @[time-and-fate](https://github.com/time-and-fate)

* 锁视图支持乐观事务被阻塞的信息

    大量锁冲突往往会造成严重的性能问题，而定位锁冲突是这类性能问题排查的必要手段之一。TiDB v6.2.0 之前，支持通过系统视图 `INFORMATION_SCHEMA.DATA_LOCK_WAITS` 查看锁冲突的关系，但是不支持乐观事务被悲观锁阻塞的情况。TiDB v6.2.0 扩展 [`DATA_LOCK_WAITS`](/information-schema/information-schema-data-lock-waits.md) 视图，提供乐观事务被悲观锁阻塞情况下的冲突关系，帮助用户快速定位锁冲突，同时为业务改进提供依据，从而减少这类锁冲突的发生频率，提升系统整体性能。

    [用户文档](/information-schema/information-schema-data-lock-waits.md) [#34609](https://github.com/pingcap/tidb/issues/34609) @[longfangsong](https://github.com/longfangsong)

### 性能

* 优化器增加对外连接顺序的提示

    在 v6.1.0 中引入的优化器提示 `LEADING` 可干预表的连接顺序，但是这个提示并不能应用在包含了外连接的查询中，见 [`LEADING` 文档](/optimizer-hints.md#leadingt1_name--tl_name-)。在 v6.2.0 中 TiDB 解除了这个限制，`LEADING` 提示对外连接同样生效。在包含外连接的查询中，你同样可以利用 `LEADING` 指定表的连接顺序，获得更好的 SQL 执行性能，并避免执行计划的突变。

    [用户文档](/optimizer-hints.md#leadingt1_name--tl_name-) [#29932](https://github.com/pingcap/tidb/issues/29932) @[Reminiscent](https://github.com/Reminiscent)

* 引入新的优化器提示 `SEMI_JOIN_REWRITE` 改善 `EXISTS` 查询性能

    在部分场景下，带有 `EXISTS` 的查询并不能选择最优的执行计划，导致查询运行时间过长。在 v6.2.0 版本中，优化器增加了新的改写规则，用于优化此类场景下执行计划的选择，并通过 `SEMI_JOIN_REWRITE` 提示强制优化器进行改写，从而得到更好的查询性能。

    [用户文档](/optimizer-hints.md#semi_join_rewrite) [#35323](https://github.com/pingcap/tidb/issues/35323) @[winoros](https://github.com/winoros)

* 引入一个优化器提示 `MERGE`，提升分析类查询性能

    公共表表达式 (CTE) 是简化查询逻辑的有效方法，广泛应用于复杂查询的编写。在 v6.2.0 前，CTE 在 TiFlash 环境中还不能自动展开，这在一定程度上限制了 MPP 的运行效率。在 v6.2.0 中，TiDB 引入一个 MySQL 兼容的优化器提示 `MERGE`。利用这个提示，优化器允许对 CTE 内联进行展开，使得 CTE 查询结果的消费者能够在 TiFlash 内并行执行，从而提升此类分析查询的性能。

    [用户文档](/optimizer-hints.md#merge) [#36122](https://github.com/pingcap/tidb/issues/36122) @[dayicklp](https://github.com/dayicklp)

* 优化了个别分析场景的聚合操作性能

    在使用 TiFlash 的 OLAP 场景下对列进行聚合操作时，如果被聚合列因分布不均而存在严重数据倾斜，并且被聚合列有大量不同的取值，那么该列的 `COUNT(DISTINCT)` 查询效率偏低。在 v6.2.0 版本中，引入了新的改写规则，针对单列的 `COUNT(DISTINCT)` 查询进行了优化，提升此类场景下的查询性能。

    [用户文档](/system-variables.md#tidb_opt_skew_distinct_agg-从-v620-版本开始引入) [#36169](https://github.com/pingcap/tidb/issues/36169) @[fixdb](https://github.com/fixdb)

* TiDB 支持 DDL 并发执行

    TiDB v6.2.0 引入新的 DDL 并行执行框架，在不同表对象上的 DDL 可以并发执行，解决了之前不同表之间 DDL 相互阻塞的问题。同时在不同表对象的追加索引、列类型变更等场景下支持并行执行，大幅提升执行效率。

    [#32031](https://github.com/pingcap/tidb/issues/32031) @[wjhuang2016](https://github.com/wjhuang2016)

* 优化器增强了对字符串条件匹配的估算方式

    在字符串条件匹配场景下，行数估算偏差有可能影响最优执行计划的生成，例如条件 `like '%xyz'` 或者借助 `regex()` 的正则表达式匹配。为了提升此类场景下估算的准确度，TiDB v6.2.0 增强了这个场景下的估算方式。新的方法会结合统计信息的 TopN 信息以及系统变量，在提升估算准确率的同时，还引入了手动调整的方法，进而提升此场景下的 SQL 性能。

    [用户文档](/system-variables.md#tidb_default_string_match_selectivity-从-v620-版本开始引入) [#36209](https://github.com/pingcap/tidb/issues/36209) @[time-and-fate](https://github.com/time-and-fate)

* 支持窗口函数下推到 TiFlash 进行多线程并行计算

    通过实现执行过程中的细粒度的数据交换 (shuffle) 能力，窗口函数的计算由单线程变为多线程并行计算，成倍降低查询响应时间。此性能改进不改变用户使用行为。你可以通过控制变量 [`tiflash_fine_grained_shuffle_batch_size`](/system-variables.md#tiflash_fine_grained_shuffle_batch_size-从-v620-版本开始引入) 来控制 shuffle 的粒度。

    [用户文档](/system-variables.md#tiflash_fine_grained_shuffle_batch_size-从-v620-版本开始引入) [#4631](https://github.com/pingcap/tiflash/issues/4631) @[guo-shaoge](https://github.com/guo-shaoge)

* TiFlash 支持新版本的存储格式

    TiFlash 通过改进存储格式，大幅减轻了在高并发、高负载场景下 GC 造成 CPU 占用高的问题，可以有效减少后台任务 IO 流量，提升高并发、高负载下的稳定性。同时新版本存储格式可以显著降低空间放大，减少磁盘空间浪费。

    v6.2.0 默认以新版本存储格式保存数据。从更低版本升级到 6.2.0 版本后，不支持原地降级，否则更低版本的 TiFlash 无法识别新版本的数据格式。

    建议用户在升级前阅读 [TiFlash 升级帮助](/tiflash-upgrade-guide.md)。

    [用户文档](/tiflash/tiflash-configuration.md#配置文件-tiflashtoml) [#3594](https://github.com/pingcap/tiflash/issues/3594) @[JaySon-Huang](https://github.com/JaySon-Huang) @[lidezhu](https://github.com/lidezhu) @[jiaqizho](https://github.com/jiaqizho)

* TiFlash 优化提升多并发场景下的数据扫描性能（实验特性）

    在 v6.2.0，TiFlash 通过合并相同数据的读取操作，减少对于相同数据的重复读取，优化了多并发任务情况下的资源开销，提升多并发下的数据扫描性能。避免了以往在多并发任务下，如果涉及相同数据，同一份数据需要在每个任务中分别进行读取的情况，以及可能出现在同一时间内对相同数据进行多次读取的情况。

    [用户文档](/tiflash/tiflash-configuration.md#配置文件-tiflashtoml) [#5376](https://github.com/pingcap/tiflash/issues/5376) @[JinheLin](https://github.com/JinheLin)

* TiFlash 新增 FastScan 功能，降低一致性保证，提高读写速度（实验特性）

    TiDB 从 v6.2.0 版本引入快速扫描功能 (FastScan)，支持跳过一致性检测以大幅提高速度，适用于离线分析任务等对于数据的精度和一致性要求不高的场景。以往，为了保证数据一致性，TiFlash 在数据扫描过程中需要对数据进行一致性检查，从多个不同版本的数据中找到符合要求的数据。

    从更低的版本升级到 v6.2.0 版本时，所有的表默认不开启 FastScan 功能，而是保持一致性的数据扫描功能。你可以为每一张表独立开启 FastScan 功能。如果在 v6.2.0 版本设定表开启 FastScan 功能后，当降级到更低版本时 FastScan 功能设置将失效，但不影响数据的正常读取。这种情况等同于强一致性的数据扫描功能。

    [用户文档](/tiflash/use-fastscan.md) [#5252](https://github.com/pingcap/tiflash/issues/5252) @[hongyunyan](https://github.com/hongyunyan)

### 稳定性

* TiKV 支持自适应调整 CPU 使用率（实验特性）

    数据库通常会使用后台进程来执行一些内部操作，通过采集各种统计信息，帮助用户定位性能问题，生成更优的执行计划，从而提升数据库的稳定性和性能。然而如何平衡后台操作和前台操作的资源开销，在不影响用户日常数据库使用的基础上如何更高效地采集信息，一直是数据库领域最为头疼的问题之一。

    从 v6.2.0 开始，TiDB 支持通过 TiKV 配置文件设置后台请求的 CPU 使用率，进而限制自动统计信息收集等后台操作在 TiKV 的 CPU 使用比例，避免极端情况下后台操作抢占对用户操作的资源，确保数据库稳定高效运行。

    同时，TiDB 还支持 CPU 使用率自动调节的功能，这时 TiKV 会根据实例的 CPU 占用情况，自适应地对后台请求占用的 CPU 资源进行动态调整。该功能默认关闭。

    [用户文档](/tikv-configuration-file.md#后台限流) [#12503](https://github.com/tikv/tikv/issues/12503) @[BornChanger](https://github.com/BornChanger)

### 易用性

* TiKV 支持通过命令行参数提供更详细的配置信息

    TiKV 配置文件可以实现对 TiKV 实例的管理。但是对运行时间长且多人管理的 TiKV 实例，用户修改了哪些配置文件，配置的默认值是什么，难以进行方便地比对。这在集群升级、迁移时容易造成困扰。从 TiDB v6.2.0 开始，tikv-server 新增命令行参数 [`—-config-info`](/command-line-flags-for-tikv-configuration.md#--config-info-format)，支持输出 TiKV 所有配置项的默认值和当前值，帮助用户快速验证 TiKV 进程的启动参数，提升易用性。

    [用户文档](/command-line-flags-for-tikv-configuration.md#--config-info-format) [#12492](https://github.com/tikv/tikv/issues/12492) @[glorv](https://github.com/glorv)

### MySQL 兼容性

* TiDB 支持使用一个 `ALTER TABLE` 语句增删改多个列或索引

    在 v6.2.0 之前，TiDB 仅支持单一 DDL 变更，导致用户在迁移异构数据库时经常会遇见 DDL 操作不兼容的情况，需要耗费额外的精力将复杂的 DDL 修改成 TiDB 支持的多个简单 DDL。同时还有一些用户依赖 ORM 框架，实现 SQL 组装，最终出现了 SQL 不兼容等问题。TiDB 从 v6.2.0 开始，支持使用 `ALTER TABLE` 语句修改一个表的多个模式对象，方便了用户 SQL 实现，也提升了产品易用性。

    [用户文档](/sql-statements/sql-statement-alter-table.md) [#14766](https://github.com/pingcap/tidb/issues/14766) @[tangenta](https://github.com/tangenta)

* 事务中支持 `SAVEPOINT`

    事务是数据库保证 ACID 特性的一系列连续操作的逻辑集合。在一些复杂业务场景下，你可能需要管理一个事务的大量操作，有时候需要在事务内实现部分操作的回退能力。Savepoint 就是针对事务内部实现的可命名保存点机制，通过这个机制，你可以灵活地控制事务内的回退节点，从而实现更复杂的事务管理能力，实现更为多样的业务设计。

    [用户文档](/sql-statements/sql-statement-savepoint.md) [#6840](https://github.com/pingcap/tidb/issues/6840) @[crazycs520](https://github.com/crazycs520)

### 数据迁移

* BR 支持恢复用户和权限数据

    BR 快照备份和恢复支持恢复用户和权限数据，用户不再需要额外的方案恢复用户和权限数据，只需要在使用 BR 恢复数据时指定参数 `--with-sys-table`。

    [用户文档](/br/br-snapshot-guide.md#恢复-mysql-数据库下的表) [#35395](https://github.com/pingcap/tidb/issues/35395) @[D3Hunter](https://github.com/D3Hunter)

* 支持基于变更日志的备份和恢复实现 Point-in-time recovery

    基于变更日志和快照数据的备份恢复实现 PITR (point-in-time recovery) 功能，允许用户在新集群上恢复备份集群的历史任意时间点的快照。该功能可以满足以下的用户需求：

    - 降低灾备场景下的 RPO，如实现十几分钟的 RPO；
    - 用于处理业务数据写错的案例，如回滚业务数据到出错事件前；
    - 业务历史数据审计，满足司法审查的需求。
    - 该功能初版存在着一些使用限制，详细情况请参考功能使用文档。

    [用户文档](/br/br-use-overview.md) [#29501](https://github.com/pingcap/tidb/issues/29501) @[joccau](https://github.com/joccau)

* DM 支持增量持续数据校验（实验特性）

    增量持续数据校验用于在数据同步过程中，持续对比上游 binlog 与下游实际写入记录是否存在异常，例如错误同步、记录缺失等。此特性用以解决常见的全量数据校验方案的滞后性，资源消耗过重等问题。

    [用户文档](/dm/dm-continuous-data-validation.md) [#4426](https://github.com/pingcap/tiflow/issues/4426) @[D3Hunter](https://github.com/D3Hunter) @[buchuitoudegou](https://github.com/buchuitoudegou)

* 自动识别 Amazon S3 bucket 所在的区域

    数据迁移任务可自动判断 S3 bucket 所在区域，不再需要显式传递区域参数。

    [#34275](https://github.com/pingcap/tidb/issues/34275) @[WangLe1321](https://github.com/WangLe1321)

* 支持为 TiDB Lightning 配置磁盘资源配额（实验特性）

    当 TiDB Lightning 使用物理导入模式 (backend='local') 进行导入时，sorted-kv-dir 需要具备足以容纳数据源总量的空间，当空间不足时可能致使导入任务失败。新增的 `disk_quota` 配置项可以用于限定 TiDB Lightning 的磁盘空间使用总量，当 sorted-kv-dir 存储空间较少时也可以正常完成导入任务。

    [用户文档](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#磁盘资源配额-从-v620-版本开始引入) [#446](https://github.com/pingcap/tidb-lightning/issues/446) @[buchuitoudegou](https://github.com/buchuitoudegou)

* TiDB Lightning 支持使用物理导入模式导入数据到生产集群

    TiDB Lightning 原有的物理导入模式 (backend='local') 对目标集群影响较大，例如导入过程将停止 PD 调度等，因此仅适用于目标集群初次导入数据。

    TiDB Lightning 在现有基础上做了改进，导入时可以暂停对应表的调度，从而将影响范围由集群级别降低到表级别，即非导入的表仍可进行读写操作。

    此特性无需手动配置，目标 TiDB 集群版本在 v6.1.0 及以上且 TiDB Lightning 在 v6.2.0 及以上时自动生效。

    [用户文档](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#导入时暂停-pd-调度的范围) [#35148](https://github.com/pingcap/tidb/issues/35148) @[sleepymole](https://github.com/sleepymole)

* 调整 [TiDB Lightning 在线文档](/tidb-lightning/tidb-lightning-overview.md)，使其目录结构更加合理和清晰。同时对文档中关于“后端模式”的描述进行了修改，使用物理导入模式替代原有 `local` 后端模式，使用逻辑导入模式替代原有 `tidb` 后端模式，以降低新用户的理解难度。

### 数据共享与订阅

* 支持 RawKV 跨集群复制（实验特性）

    支持订阅 RawKV 的数据变更，并通过新的 TiKV-CDC 组件将变更实时同步到下游 TiKV 集群，从而实现 RawKV 的跨集群复制能力。

    [用户文档](/tikv-configuration-file.md#api-version-从-v610-版本开始引入) [#11965](https://github.com/tikv/tikv/issues/11965) @[pingyu](https://github.com/pingyu)

* 支持过滤 DDL 和 DML 事件

    在一些特殊的场景下，用户可能希望对 TiDB 增量数据变更日志进行一定规则的过滤，例如过滤 Drop Table 等高风险 DDL。自 v6.2.0 起，TiCDC 支持过滤指定类型的 DDL 事件，支持基于 SQL 表达式过滤 DML 事件，从而适应更多的数据同步场景。

    [用户文档](/ticdc/ticdc-filter.md#event-filter-事件过滤器-从-v620-版本开始引入) [#6160](https://github.com/pingcap/tiflow/issues/6160) @[asddongmen](https://github.com/asddongmen)

## 兼容性变更

### 系统变量

| 变量名 | 修改类型 | 描述 |
| ------ | ------ | ------ |
| [tidb_enable_new_cost_interface](/system-variables.md#tidb_enable_new_cost_interface-从-v620-版本开始引入) | 新增 | 控制是否使用重构后的代价模型 [Cost Model Version 2](/cost-model.md#cost-model-version-2)。 |
| [tidb_cost_model_version](/system-variables.md#tidb_cost_model_version-从-v620-版本开始引入) | 新增 | TiDB 在进行物理优化时会使用代价模型来进行索引选择和算子选择，该变量用于选择代价模型的版本。TiDB v6.2.0 引入了代价模型 Cost Model Version 2，在内部测试中比此前版本的代价模型更加准确。 |
| [tiflash_fine_grained_shuffle_stream_count](/system-variables.md#tiflash_fine_grained_shuffle_stream_count-从-v620-版本开始引入) | 新增 | 当窗口函数下推到 TiFlash 执行时，可以通过该变量控制窗口函数执行的并行度。 |
| [tiflash_fine_grained_shuffle_batch_size](/system-variables.md#tiflash_fine_grained_shuffle_batch_size-从-v620-版本开始引入) | 新增 | 细粒度 shuffle 功能开启时，该变量控制发送端发送数据的攒批大小，即发送端累计行数超过该值就会进行一次数据发送。 |
| [tidb_default_string_match_selectivity](/system-variables.md#tidb_default_string_match_selectivity-从-v620-版本开始引入) | 新增 | 设置过滤条件中的 `like`、`rlike`、`regexp` 函数在行数估算时的默认选择率，以及是否对这些函数启用 TopN 辅助估算。 |
| [tidb_enable_analyze_snapshot](/system-variables.md#tidb_enable_analyze_snapshot-从-v620-版本开始引入) | 新增 | 控制 `ANALYZE` 读取历史时刻的数据还是读取最新的数据。 |
| [tidb_generate_binary_plan](/system-variables.md#tidb_generate_binary_plan-从-v620-版本开始引入) | 新增 | 用于指定是否在 slow log 和 statement summary 里包含以二进制格式编码的执行计划。 |
| [tidb_opt_skew_distinct_agg](/system-variables.md#tidb_opt_skew_distinct_agg-从-v620-版本开始引入) | 新增 | 用于设置优化器是否将带有 `DISTINCT` 的聚合函数（例如 `SELECT b, COUNT(DISTINCT a) FROM t GROUP BY b`）改写为两层聚合函数（例如 `SELECT b, COUNT(a) FROM (SELECT b, a FROM t GROUP BY b, a) t GROUP BY b`）。 |
| [tidb_enable_noop_variables](/system-variables.md#tidb_enable_noop_variables-从-v620-版本开始引入) | 新增 | 用于设置 `SHOW [GLOBAL] VARIABLES` 是否显示 noop 变量。 |
| tidb_enable_concurrent_ddl | 新增 | 用于控制是否让 TiDB 使用并发 DDL 语句。 |
| [tidb_min_paging_size](/system-variables.md#tidb_min_paging_size-从-v620-版本开始引入) | 新增 | 用来设置 coprocessor 协议中 paging size 的最小的行数。 |
| [tidb_txn_commit_batch_size](/system-variables.md#tidb_txn_commit_batch_size-从-v620-版本开始引入) | 新增 | 用于控制 TiDB 向 TiKV 发送的事务提交请求的批量大小。 |
| tidb_enable_change_multi_schema | 删除 | 删除原因：从 v6.2.0 起，TiDB 默认支持使用一个 `ALTER TABLE` 语句增删改多个列或索引。 |
| [tidb_enable_outer_join_reorder](/system-variables.md#tidb_enable_outer_join_reorder-从-v610-版本开始引入) | 修改 | 用来控制 TiDB 的 join reorder 是否支持 outer join，在 v6.1.0 中为 `ON`，即默认开启。自 v6.2.0 起，该变量默认为 `OFF`，即默认关闭。 |

### 配置文件参数

| 配置文件 | 配置项 | 修改类型 | 描述 |
| -------- | -------- | -------- | -------- |
| TiDB | feedback-probability | 删除 | 该配置不再生效，不推荐使用。 |
| TiDB | query-feedback-limit | 删除 | 该配置不再生效，不推荐使用。 |
| TiKV | [server.simplify-metrics](/tikv-configuration-file.md#simplify-metrics-从-v620-版本开始引入) | 新增 | 控制是否开启精简返回的 Metrics 数据。 |
| TiKV | [quota.background-cpu-time](/tikv-configuration-file.md#background-cpu-time-从-v620-版本开始引入) | 新增 | 限制处理 TiKV 后台读写请求所使用的 CPU 资源使用量。 |
| TiKV | [quota.background-write-bandwidth](/tikv-configuration-file.md#background-write-bandwidth-从-v620-版本开始引入) | 新增 | 限制后台事务写入的带宽（暂未生效）。|
| TiKV | [quota.background-read-bandwidth](/tikv-configuration-file.md#background-read-bandwidth-从-v620-版本开始引入) | 新增 | 限制后台事务读取数据和 Coprocessor 读取数据的带宽（暂未生效）。 |
| TiKV | [quota.enable-auto-tune](/tikv-configuration-file.md#enable-auto-tune-从-v620-版本开始引入) | 新增 | 是否支持 quota 动态调整。如果打开该配置项，TiKV 会根据 TiKV 实例的负载情况动态调整对后台请求的限制 quota。 |
| TiKV | [rocksdb.defaultcf.format-version](/tikv-configuration-file.md#format-version-从-v620-版本开始引入) | 新增 | 设置 SST 文件的格式版本。 |
| TiKV | [rocksdb.lockcf.format-version](/tikv-configuration-file.md#format-version-从-v620-版本开始引入) | 新增 | 设置 SST 文件的格式版本。 |
| TiKV | [rocksdb.writecf.format-version](/tikv-configuration-file.md#format-version-从-v620-版本开始引入) | 新增 | 设置 SST 文件的格式版本。 |
| TiKV | rocksdb.enable-pipelined-commit | 删除 | 该配置不再生效。 |
| TiKV | gc-merge-rewrite | 删除 | 该配置不再生效。 |
| TiKV | [log-backup.enable](/tikv-configuration-file.md#enable-从-v620-版本开始引入) | 新增 | TiKV 是否开启日志备份功能。 |
| TiKV | [log-backup.file-size-limit](/tikv-configuration-file.md#file-size-limit-从-v620-版本开始引入) | 新增 | 日志备份任务备份的数据达到一定大小时，自动 flush 到外部存储中。 |
| TiKV | [log-backup.initial-scan-pending-memory-quota](/tikv-configuration-file.md#initial-scan-pending-memory-quota-从-v620-版本开始引入) | 新增 | 增量扫描数据时，用于存放扫描数据的缓存大小。 |
| TiKV | [log-backup.max-flush-interval](/tikv-configuration-file.md#max-flush-interval-从-v620-版本开始引入) | 新增 | 日志备份任务将备份数据写入到 External Storage 的最大间隔时间。 |
| TiKV | [log-backup.initial-scan-rate-limit](/tikv-configuration-file.md#initial-scan-rate-limit-从-v620-版本开始引入) | 新增 | 增量扫描数据时，用于扫描时吞吐限流参数。 |
| TiKV | [log-backup.num-threads](/tikv-configuration-file.md#num-threads-从-v620-版本开始引入) | 新增 | 日志备份功能使用的线程数。 |
| TiKV | [log-backup.temp-path](/tikv-configuration-file.md#temp-path-从-v620-版本开始引入) | 新增 | 临时目录路径，TiKV 备份日志预先先写入临时目录，然后 flush 到外部存储中。 |
| PD | replication-mode.dr-auto-sync.wait-async-timeout | 删除 | 废弃未生效的配置项。 |
| PD | replication-mode.dr-auto-sync.wait-sync-timeout | 删除 | 废弃未生效的配置项。|
| TiFlash | [`storage.format_version`](/tiflash/tiflash-configuration.md#tiflash-配置参数) | 修改 | `format_version` 默认值变更为 4，v6.2.0 及以后版本的默认文件格式，优化了写放大问题，同时减少了后台线程消耗。 |
| TiFlash | [profiles.default.dt_enable_read_thread](/tiflash/tiflash-configuration.md#配置文件-tiflashtoml) | 新增 | 控制存储引擎是否使用线程池读取数据。默认值为 false，不使用线程池读取数据。 |
| TiFlash | [profiles.default.dt_page_gc_threshold](/tiflash/tiflash-configuration.md#配置文件-tiflashtoml) | 新增 | 表示 PageStorage 单个数据文件中有效数据的最低比例。 |
| TiCDC | [--overwrite-checkpoint-ts](/ticdc/ticdc-manage-changefeed.md#恢复同步任务) | 新增 | 在 cdc cli changefeed resume 子命令下新增的参数。 |
| TiCDC | [--no-confirm](/ticdc/ticdc-manage-changefeed.md#恢复同步任务) | 新增 | 在 cdc cli changefeed resume 子命令下新增的参数。 |
| DM | [mode](/dm/task-configuration-file-full.md#完整配置文件示例) | 新增 | Validator 参数，取值可以是 full、fast，默认是 none，即不开启校验。 |
| DM | [worker-count](/dm/task-configuration-file-full.md#完整配置文件示例) | 新增 | Validator 参数，后台校验的 validation worker 数量，默认是 4 个。 |
| DM | [row-error-delay](/dm/task-configuration-file-full.md#完整配置文件示例) | 新增 | Validator 参数，某一行多久没有验证通过会报错，默认是 30 min。 |
| TiDB Lightning | [tikv-importer.store-write-bwlimit](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-任务配置) | 新增 | 限制 TiDB Lightning 向每个 TiKV Store 写入带宽带宽大小，默认为 0，表示不限制。 |
| TiDB Lightning | [tikv-importer.disk-quota](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#磁盘资源配额-从-v620-版本开始引入) | 新增 | 用于设置 TiDB Lightning 可以使用的磁盘配额。 |

### 其他

- TiFlash 的存储格式 (`format_version`) 不能直接从 4 降级到 3，详情请参考 [TiFlash 升级帮助](/tiflash-upgrade-guide.md)。
- 在 v6.2.0 以及后续版本，**强烈建议**保留 `dt_enable_logical_split` 的默认值 `false`，不要将其修改为 `true`。具体请参考已知问题 [#5576](https://github.com/pingcap/tiflash/issues/5576)。
- 如果备份集群包含 TiFlash，执行 PITR 后恢复集群的数据不包含 TiFlash 副本，需要手动恢复 TiFlash 副本；执行 exchange partition DDL 会导致 PITR restore 出错；上游数据库使用 TiDB Lightning Physical 方式导入的数据，无法作为数据日志备份下来，数据导入后需要执行一次全量备份。关于 PITR 功能使用的其他事项，请参考 [PITR 使用限制](/br/backup-and-restore-overview.md#使用须知)。
- 从 v6.2.0 开始，BR 支持通过手动指定参数 `--with-sys-table=true` 来恢复 mysql schema 下的表。
- 使用 `ALTER TABLE` 增删改多个列或索引时，TiDB 会根据执行前的 schema 结构来验证一致性，而不管同一 DDL 语句中的更改。同时，语句的执行顺序上 TiDB 和 MySQL 在某些场景不兼容。
- 在集群中，如果 TiDB 组件的版本为 v6.2.0 及以上，则 TiKV 组件版本不得低于 v6.2.0。
- TiKV 新增配置项 `split.region-cpu-overload-threshold-ratio` 支持在线修改。
- 慢查询日志以及 `INFORMATION_SCHEMA` 中的系统表 `statements_summary` 和 `slow_query` 新增输出 `binary_plan`，即以二进制格式编码的执行计划。
- `SHOW TABLE ... REGIONS` 返回的结果中新增两列：`SCHEDULING_CONSTRAINTS` 以及 `SCHEDULING_STATE`，表示对应 Region 在 Placement In SQL 中设置的调度规则以及当前的调度状态。
- 从 v6.2.0 开始，你可以通过 [TiKV-CDC](https://github.com/tikv/migration/tree/main/cdc) 组件实现 RawKV 的 Change Data Capture (CDC)。
- 使用 `ROLLBACK TO SAVEPOINT` 语句将事务回滚到指定保存点时，MySQL 会释放该保存点之后才持有的锁，但在 TiDB 悲观事务中，不会立即释放该保存点之后才持有的锁，而是等到事务提交或者回滚时，才释放全部持有的锁。
- 从 v6.2.0 开始, 执行 `SELECT tidb_version()` 返回的信息中会包含 Store 类型（tikv 或者 unistore）
- TiDB 不再有隐藏的系统变量。
- 新增两个系统表：

    - `INFORMATION_SCHEMA.VARIABLES_INFO`：用于查看 TiDB 系统变量相关的信息。
    - `PERFORMANCE_SCHEMA.SESSION_VARIABLES`：用于查看 TiDB session 系统变量相关的信息。

## 废弃功能

从 TiDB v6.2.0 起，使用 BR 备份和恢复 RawKV 的功能废弃。

## 改进提升

+ TiDB

    - 支持了 `SHOW COUNT(*) WARNINGS` 以及 `SHOW COUNT(*) ERRORS` [#25068](https://github.com/pingcap/tidb/issues/25068) @[likzn](https://github.com/likzn)
    - 对某些系统变量增加一些合法性验证 [#35048](https://github.com/pingcap/tidb/issues/35048) @[morgo](https://github.com/morgo)
    - 优化了一些类型转换的错误提示 [#32744](https://github.com/pingcap/tidb/issues/32744) @[fanrenhoo](https://github.com/fanrenhoo)
    - `KILL` 命令增加了对 DDL 操作的支持 [#24144](https://github.com/pingcap/tidb/issues/24144) @[morgo](https://github.com/morgo)
    - 提升了 `SHOW TABLES/DATABASES LIKE …` 命令的输出与 MySQL 的兼容性，输出的列名称中会包含 `LIKE` 的值 [#35116](https://github.com/pingcap/tidb/issues/35116) @[likzn](https://github.com/likzn)
    - 提升了 JSON 相关函数的性能 [#35859](https://github.com/pingcap/tidb/issues/35859) @[wjhuang2016](https://github.com/wjhuang2016)
    - 提升了使用 SHA-2 时登录密码的验证速度 [#35998](https://github.com/pingcap/tidb/issues/35998) @[virusdefender](https://github.com/virusdefender)
    - 精简了一些日志的输出 [#36011](https://github.com/pingcap/tidb/issues/36011) @[dveeden](https://github.com/dveeden)
    - 优化了 coprocessor 通信协议，大幅度降低读取数据时 TiDB 进程的内存消耗，进而可进一步缓解扫全表场景及 Dumpling 导出数据场景下的 OOM 问题。该通信协议是否开启由 `tidb_enable_paging` 系统变量控制（作用域为 SESSION 或 GLOBAL)，当前默认关闭。可将该变量值设为 `true` 进行开启 [#35633](https://github.com/pingcap/tidb/issues/35633) @[tiancaiama](https://github.com/tiancaiamao) @[wshwsh12](https://github.com/wshwsh12)
    - 进一步优化了部分算子（HashJoin、HashAgg、Update、Delete）内存追踪的准确度 ([#35634](https://github.com/pingcap/tidb/issues/35634), [#35631](https://github.com/pingcap/tidb/issues/35631), [#35635](https://github.com/pingcap/tidb/issues/35635), @[wshwsh12](https://github.com/wshwsh12)) ([#34096](https://github.com/pingcap/tidb/issues/34096), @[ekexium](https://github.com/ekexium))
    - 系统表 `INFORMATION_SCHEMA.DATA_LOCK_WAIT` 支持记录乐观事务的锁信息 [#34609](https://github.com/pingcap/tidb/issues/34609) @[longfangson](https://github.com/longfangsong)
    - 新增部分事务相关的监控指标 [#34456](https://github.com/pingcap/tidb/issues/34456) @[longfangsong](https://github.com/longfangsong)

+ TiKV

    - 支持通过 gzip 压缩 metrics 响应减少 HTTP body 大小 [#12355](https://github.com/tikv/tikv/issues/12355) @[glorv](https://github.com/glorv)
    - 优化了 TiKV Grafana Dashboard 的可读性 [#12007](https://github.com/tikv/tikv/issues/12007) @[kevin-xianliu](https://github.com/kevin-xianliu)
    - 优化 Apply 算子的写入性能 [#12898](https://github.com/tikv/tikv/issues/12898) @[ethercflow](https://github.com/ethercflow)
    - 支持动态调整 RocksDB 进行 subcompaction 的并发个数 (`rocksdb.max-sub-compactions`) [#13145](https://github.com/tikv/tikv/issues/13145) @[ethercflow](https://github.com/ethercflow)

+ PD

    - 支持 Region CPU 维度统计信息并增强 Load Base Split 的覆盖场景 [#12063](https://github.com/tikv/tikv/issues/12063) @[Jmpotato](https://github.com/JmPotato)

+ TiFlash

    - 优化了 TiFlash MPP 的错误处理流程，增强了稳定性 [#5095](https://github.com/pingcap/tiflash/issues/5095) @[windtalker](https://github.com/windtalker) @[yibin87](https://github.com/yibin87)
    - 优化了 UTF8_BIN/UTF8MB4_BIN Collation 的比较和排序操作 [#5294](https://github.com/pingcap/tiflash/issues/5294) @[solotzg](https://github.com/solotzg)

+ Tools

    + Backup & Restore (BR)

        - 优化了全量备份数据组织形式，解决大规模集群备份时遇到的 S3 限流问题 [#30087](https://github.com/pingcap/tidb/issues/30087) @[MoCuishle28](https://github.com/MoCuishle28)

    + TiCDC

        - 优化了多 Region 场景下，runtime 上下文切换带来过多性能开销的问题 [#5610](https://github.com/pingcap/tiflow/issues/5610) @[hicqu](https://github.com/hicqu)
        - 优化了 redo log 的性能、修复 meta 和数据不一致的问题 ([#6011](https://github.com/pingcap/tiflow/issues/6011) @[CharlesCheung96](https://github.com/CharlesCheung96)) ([#5924](https://github.com/pingcap/tiflow/issues/5924) @[zhaoxinyu](https://github.com/zhaoxinyu)) ([#6277](https://github.com/pingcap/tiflow/issues/6277) @[hicqu](https://github.com/hicqu))

    + TiDB Lightning

        - 增加更多可重试错误，包括 EOF、Read index not ready、Coprocessor 超时等 [#36674](https://github.com/pingcap/tidb/issues/36674), [#36566](https://github.com/pingcap/tidb/issues/36566) @[D3Hunter](https://github.com/D3Hunter)

    + TiUP

        - 使用 TiUP 新部署集群时，Node-exporter 组件将使用 1.3.1 版本，Blackbox-exporter 组件将使用 0.21.1 版本，使用新版本组件可以确保在不同系统环境下成功部署

## 错误修复

+ TiDB

    - 修复了在查询分区表中如果查询条件中有分区键且两者使用了不同的 COLLATE 时会错误的进行分区裁剪的问题 [#32749](https://github.com/pingcap/tidb/issues/32749) @[mjonss](https://github.com/mjonss)
    - 修复了 `SET ROLE` 中如果 host 中有大写字母无法匹配到已经 GRANT 的 ROLE 的问题 [#33061](https://github.com/pingcap/tidb/issues/33061) @[morgo](https://github.com/morgo)
    - 修复了无法 DROP AUTO_INCREMENT 的列的问题 [#34891](https://github.com/pingcap/tidb/issues/34891) @[Defined2014](https://github.com/Defined2014)
    - 修复了 `SHOW CONFIG` 会显示一些已经移除掉的配置项的问题 [#34867](https://github.com/pingcap/tidb/issues/34867) @[morgo](https://github.com/morgo)
    - 修复了 `SHOW DATABASES LIKE …` 大小写敏感的问题 [#34766](https://github.com/pingcap/tidb/issues/34766) @[e1ijah1](https://github.com/e1ijah1)
    - 修复了 `SHOW TABLE STATUS LIKE …` 大小写敏感的问题 [#7518](https://github.com/pingcap/tidb/issues/7518) @[likzn](https://github.com/likzn)
    - 修复了 `max-index-length` 检查在非严格模式下仍然报错的问题 [#34931](https://github.com/pingcap/tidb/issues/34931) @[e1ijah1](https://github.com/e1ijah1)
    - 修复了 `ALTER COLUMN ... DROP DEFAULT` 不起作用的问题 [#35018](https://github.com/pingcap/tidb/issues/35018) @[Defined2014](https://github.com/Defined2014)
    - 修复了创建表时列的默认值和列类型不一致没有自动修正的问题 [#34881](https://github.com/pingcap/tidb/issues/34881) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - 修复了在 `DROP USER` 之后 `mysql.columns_priv` 表中相关的数据没有被同步删除的问题 [#35059](https://github.com/pingcap/tidb/issues/35059) @[lcwangchao](https://github.com/lcwangchao)
    - 通过禁止在一些系统的 schema 内创建表，修复了由此导致的 DDL 卡住的问题 [#35205](https://github.com/pingcap/tidb/issues/35205) @[tangenta](https://github.com/tangenta)
    - 修复了某些情况下查询分区表可能导致“index-out-of-range”和“non used index”的问题 [#35181](https://github.com/pingcap/tidb/issues/35181) @[mjonss](https://github.com/mjonss)
    - 通过支持 `INTERVAL expr unit + expr` 形式的语法，修复了该语句会报错的问题 [#30253](https://github.com/pingcap/tidb/issues/30253) @[mjonss](https://github.com/mjonss)
    - 修复了在事务中创建的本地临时表无法找到的问题 [#35644](https://github.com/pingcap/tidb/issues/35644) @[djshow832](https://github.com/djshow832)
    - 修复了给 `ENUM` 列设置 COLLATE 导致 panic 的问题 [#31637](https://github.com/pingcap/tidb/issues/31637) @[wjhuang2016](https://github.com/wjhuang2016)
    - 修复了当某台 PD 宕机时，由于没有重试其他 PD 节点，导致查询表 `INFORMATION_SCHEMA.TIKV_REGION_STATUS` 时请求失败的问题 [#35708](https://github.com/pingcap/tidb/issues/35708) @[tangenta](https://github.com/tangenta)
    - 修复在 `SET character_set_results = GBK` 后 `SHOW CREATE TABLE …` 不能正确显示 `SET` 和 `ENUM` 列的问题 [#31338](https://github.com/pingcap/tidb/issues/31338) @[tangenta](https://github.com/tangenta)
    - 修复了系统变量 `tidb_log_file_max_days` 和 `tidb_config` 的作用域不正确的问题 [#35190](https://github.com/pingcap/tidb/issues/35190) @[morgo](https://github.com/morgo)
    - 修复了类型是 `ENUM` 或者 `SET` 的列在 `SHOW CREATE TABLE` 的输出与 MySQL 不兼容的问题 [#36317](https://github.com/pingcap/tidb/issues/36317) @[Defined2014](https://github.com/Defined2014)
    - 修复了创建表时指定类型为 `LONG BYTE` 列的行为与 MySQL 不兼容的问题 [#36239](https://github.com/pingcap/tidb/issues/36239) @[Defined2014](https://github.com/Defined2014)
    - 修复了设置 `auto_increment = x` 对临时表无效的问题 [#36224](https://github.com/pingcap/tidb/issues/36224) @[djshow832](https://github.com/djshow832)
    - 修复了在并发修改列的情况下可能导致 DEFAULT VALUE 不正确的问题 [#35846](https://github.com/pingcap/tidb/issues/35846) @[wjhuang2016](https://github.com/wjhuang2016)
    - 避免向非健康状态的 TiKV 节点发送请求，以提升可用性 [#34906](https://github.com/pingcap/tidb/issues/34906) @[sticnarf](https://github.com/sticnarf)
    - 修复了 `LOAD DATA` 语句中列的列表不生效的问题 [#35198](https://github.com/pingcap/tidb/issues/35198) @[SpadeA-Tang](https://github.com/SpadeA-Tang)
    - 修复部分场景非唯一二级索引被误加悲观锁的问题 [#36235](https://github.com/pingcap/tidb/issues/36235) @[ekexium](https://github.com/ekexium)

+ TiKV

    - 避免在悲观事务中报出 `Write Conflict` 错误 [#11612](https://github.com/tikv/tikv/issues/11612) @[sticnarf](https://github.com/sticnarf)
    - 修复了在悲观事务中使用 Async Commit 导致重复提交记录的问题 [#12615](https://github.com/tikv/tikv/issues/12615) @[sticnarf](https://github.com/sticnarf)
    - 修复了 TiKV API 从 `storage.api-version = 1` 升级为 `storage.api-version = 2` 时 panic 的问题 [#12600](https://github.com/tikv/tikv/issues/12600) @[pingyu](https://github.com/pingyu)
    - 修复了 TiKV 和 PD 配置文件中 Region size 不一致的问题 [#12518](https://github.com/tikv/tikv/issues/12518) @[5kbpers](https://github.com/5kbpers)
    - 修复了 TiKV 持续重连 PD 的问题 [#12506](https://github.com/tikv/tikv/issues/12506), [#12827](https://github.com/tikv/tikv/issues/12827) @[Connor1996](https://github.com/Connor1996)
    - 修复了对空字符串进行类型转换导致 TiKV panic 的问题 [#12673](https://github.com/tikv/tikv/issues/12673) @[wshwsh12](https://github.com/wshwsh12)
    - 修复了 `DATETIME` 类型的数据包含小数部分和 `Z` 后缀导致检查报错的问题 [#12739](https://github.com/tikv/tikv/issues/12739) @[gengliqi](https://github.com/gengliqi)
    - 修复 Apply 写入 TiKV RocksDB 的 perf context 粒度过大的问题 [#11044](https://github.com/tikv/tikv/issues/11044) @[LykxSassinator](https://github.com/LykxSassinator)
    - 修复当 [backup](/tikv-configuration-file.md#backup)/[import](/tikv-configuration-file.md#import)/[cdc](/tikv-configuration-file.md#cdc) 配置项设置错误时 TiKV 无法启动的问题 [#12771](https://github.com/tikv/tikv/issues/12771) @[3pointer](https://github.com/3pointer)
    - 修复同时分裂和销毁一个 peer 时可能导致 panic 的问题 [#12825](https://github.com/tikv/tikv/issues/12825) @[BusyJay](https://github.com/BusyJay)
    - 修复在 Region merge 时 source peer 通过 snapshot 追日志时可能导致 panic 的问题 [#12663](https://github.com/tikv/tikv/issues/12663) @[BusyJay](https://github.com/BusyJay)
    - 修复 `max_sample_size` 为 `0` 时 ANALYZE 可能导致 panic 的问题 [#11192](https://github.com/tikv/tikv/issues/11192) @[LykxSassinator](https://github.com/LykxSassinator)
    - 修复了启用 Raft Engine 时未清理加密密钥的问题 [#12890](https://github.com/tikv/tikv/issues/12890) @[tabokie](https://github.com/tabokie)
    - 修复了 `get_valid_int_prefix` 函数与 TiDB 不兼容的问题，例如 `FLOAT` 类型被错误地转换成 `INT` [#13045](https://github.com/tikv/tikv/issues/13045) @[guo-shaoge](https://github.com/guo-shaoge)
    - 修复了新创建的 Region Commit Log Duration 较高导致 QPS 下降的问题 [#13077](https://github.com/tikv/tikv/issues/13077) @[Connor1996](https://github.com/Connor1996)
    - 修复 PD Region heartbeat 连接异常中断后未重新连接的问题 [#12934](https://github.com/tikv/tikv/issues/12934) @[bufferflies](https://github.com/bufferflies)

+ Tools

    + Backup & Restore (BR)

        修复了限速备份后，BR 没有重置速度限制的问题 [#31722](https://github.com/pingcap/tidb/issues/31722) @[MoCuishle28](https://github.com/MoCuishle28)

## 贡献者

感谢来自 TiDB 社区的贡献者们：

- [e1ijah1](https://github.com/e1ijah1)
- [PrajwalBorkar](https://github.com/PrajwalBorkar)
- [likzn](https://github.com/likzn)
- [rahulk789](https://github.com/rahulk789)
- [virusdefender](https://github.com/virusdefender)
- [joycse06](https://github.com/joycse06)
- [morgo](https://github.com/morgo)
- [ixuh12](https://github.com/ixuh12)
- [blacktear23](https://github.com/blacktear23)
- [johnhaxx7](https://github.com/johnhaxx7)
- [GoGim1](https://github.com/GoGim1)
- [renbaoshuo](https://github.com/renbaoshuo)
- [Zheaoli](https://github.com/Zheaoli)
- [fanrenhoo](https://github.com/fanrenhoo)
- [njuwelkin](https://github.com/njuwelkin)
- [wirybeaver](https://github.com/wirybeaver)
- [hey-kong](https://github.com/hey-kong)
- [fatelei](https://github.com/fatelei)
- [eastfisher](https://github.com/eastfisher)：首次贡献者
- [Juneezee](https://github.com/Juneezee)：首次贡献者
