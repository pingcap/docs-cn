---
title: TiDB 5.4 Release Notes
summary: TiDB 5.4.0 版本发布日期为 2022 年 2 月 15 日。此版本新增了许多功能和改进，包括支持 GBK 字符集、索引合并、有界限过期数据读取、统计信息采集配置持久化等。同时还修复了许多 bug，提升了稳定性和性能。
---

# TiDB 5.4 Release Notes

发版日期：2022 年 2 月 15 日

TiDB 版本：5.4.0

在 v5.4.0 版本中，你可以获得以下关键特性：

+ 支持 GBK 字符集
+ 支持索引合并 (Index Merge) 数据访问方法，能够合并多个列上索引的条件过滤结果
+ 支持通过 session 变量实现有界限过期数据读取
+ 支持统计信息采集配置持久化
+ 支持使用 Raft Engine 作为 TiKV 的日志存储引擎（实验特性）
+ 优化备份对集群的影响
+ 支持 Azure Blob Storage 作为备份目标存储
+ 持续提升 TiFlash 列式存储引擎和 MPP 计算引擎的稳定性和性能
+ 为 TiDB Lightning 增加已存在数据表是否允许导入的开关
+ 优化持续性能分析（实验特性）
+ TiSpark 支持用户认证与鉴权

## 兼容性变化

> **注意：**
>
> 当从一个早期的 TiDB 版本升级到 TiDB v5.4.0 时，如需了解所有中间版本对应的兼容性更改说明，请查看对应版本的 [Release Notes](/releases/_index.md)。

### 系统变量

|  变量名    |  修改类型    |  描述    |
| :---------- | :----------- | :----------- |
|  [`tidb_enable_column_tracking`](/system-variables.md#tidb_enable_column_tracking-从-v540-版本开始引入) | 新增 | 用于控制是否开启 TiDB 对 `PREDICATE COLUMNS` 的收集，默认值为 `OFF`。 |
| [`tidb_enable_paging`](/system-variables.md#tidb_enable_paging-从-v540-版本开始引入)  | 新增 | 此变量用于控制 `IndexLookUp` 算子是否使用分页 (paging) 方式发送 Coprocessor 请求，默认值为 `OFF`。对于使用 `IndexLookUp` 和 `Limit` 并且 `Limit` 无法下推到 `IndexScan` 上的读请求，可能会出现读请求的延迟高、TiKV 的 Unified read pool CPU 使用率高的情况。在这种情况下，由于 `Limit` 算子只需要少部分数据，开启 `tidb_enable_paging`，能够减少处理数据的数量，从而降低延迟、减少资源消耗。 |
| [`tidb_enable_top_sql`](/system-variables.md#tidb_enable_top_sql-从-v540-版本开始引入) | 新增 | 用于控制是否开启 Top SQL 特性，默认值为 OFF。 |
| [`tidb_persist_analyze_options`](/system-variables.md#tidb_persist_analyze_options-从-v540-版本开始引入)  | 新增  | 用于控制是否开启 [ANALYZE 配置持久化](/statistics.md#持久化-analyze-配置)特性，默认值为 `ON`。 |
| [`tidb_read_staleness`](/system-variables.md#tidb_read_staleness-从-v540-版本开始引入) | 新增 | 用于设置当前会话允许读取的历史数据范围，默认值为 `0`。 |
| [`tidb_regard_null_as_point`](/system-variables.md#tidb_regard_null_as_point-从-v540-版本开始引入) | 新增 | 用于控制优化器是否可以将包含 null 的等值条件作为前缀条件来访问索引。 |
| [`tidb_stats_load_sync_wait`](/system-variables.md#tidb_stats_load_sync_wait-从-v540-版本开始引入) | 新增 | 这个变量用于控制是否开启统计信息的同步加载模式（默认为 `0` 代表不开启，即为异步加载模式），以及开启的情况下，SQL 执行同步加载完整统计信息等待多久后会超时。 |
| [`tidb_stats_load_pseudo_timeout`](/system-variables.md#tidb_stats_load_pseudo_timeout-从-v540-版本开始引入) | 新增 | 用于控制统计信息同步加载超时后，SQL 是执行失败 (`OFF`) 还是退回使用 pseudo 的统计信息 (`ON`)，默认值为 `OFF`。 |
|  [`tidb_backoff_lock_fast`](/system-variables.md#tidb_backoff_lock_fast) | 修改 | 默认值由 `100` 修改为 `10`。 |
| [`tidb_enable_index_merge`](/system-variables.md#tidb_enable_index_merge-从-v40-版本开始引入) | 修改 | 默认值由 `OFF` 改为 `ON`。如果从低于 v4.0.0 版本升级到 v5.4.0 及以上版本的集群，该变量值默认保持 `OFF`。如果从 v4.0.0 及以上版本升级到 v5.4.0 及以上版本的集群，该变量开关保持升级前的状态。对于 v5.4.0 及以上版本的新建集群，该变量开关默认保持 `ON`。 |
| [`tidb_store_limit`](/system-variables.md#tidb_store_limit-从-v304-和-v40-版本开始引入) | 修改 | v5.4.0 前支持实例级别及集群级别的设置，现在只支持集群级别的设置。 |

### 配置文件参数

|  配置文件    |  配置项    |  修改类型    |  描述    |
| :---------- | :----------- | :----------- | :----------- |
| TiDB | [`stats-load-concurrency`](/tidb-configuration-file.md#stats-load-concurrency-从-v540-版本开始引入) | 新增 |  用于设置 TiDB 统计信息同步加载功能可以并发处理的最大列数，默认值为 `5`。             |
| TiDB | [`stats-load-queue-size`](/tidb-configuration-file.md#stats-load-queue-size-从-v540-版本开始引入)   | 新增 |  用于设置 TiDB 统计信息同步加载功能最多可以缓存多少列的请求，默认值为 `1000`。             |
| TiKV | [`snap-generator-pool-size`](/tikv-configuration-file.md#snap-generator-pool-size-从-v540-版本开始引入) | 新增 | 配置 `snap-generator` 线程池大小，默认值为 `2`。 |
| TiKV | `log.file.max-size`、`log.file.max-days`、`log.file.max-backups` | 新增  | 参数说明见 [TiKV 配置文件 - log.file](/tikv-configuration-file.md#logfile-从-v540-版本开始引入)。 |
| TiKV | `raft-engine` | 新增 | 包含 `enable`、`dir`、`batch-compression-threshold`、`bytes-per-sync`、`target-file-size`、`purge-threshold`、`recovery-mode`、`recovery-read-block-size`、`recovery-read-block-size`、`recovery-threads`，详情参见 [TiKV 配置文件：raft-engine](/tikv-configuration-file.md#raft-engine)。|
| TiKV | [`backup.enable-auto-tune`](/tikv-configuration-file.md#enable-auto-tune-从-v54-版本开始引入) | 修改 | 在 v5.3.0 中默认值为 `false`，自 v5.4.0 起默认值改为 `true`。表示在集群资源占用率较高的情况下，是否允许 BR 自动限制备份使用的资源，减少对集群的影响。在默认配置下，备份速度可能下降。 |
| TiKV | `log-level`、`log-format`、`log-file`、`log-rotation-size` | 修改 | 将 TiKV log 参数名替换为与 TiDB log 参数一致的参数名，即 `log.level`、`log.format`、`log.file.filename`、`log.enable-timestamp`。如果只设置了原参数、且把其值设为非默认值，原参数与新参数会保持兼容；如果同时设置了原参数和新参数，则会使用新参数。详情参见 [TiKV 配置文件 - log](/tikv-configuration-file.md#log-从-v540-版本开始引入)。 |
| TiKV  |  `log-rotation-timespan`  | 删除 |  轮换日志的时间跨度。当超过该时间跨度，日志文件会被轮换，即在当前日志文件的文件名后附加一个时间戳，并创建一个新文件。 |
| TiKV | `allow-remove-leader` | 删除  | 决定是否允许删除主开关。 |
| TiKV | `raft-msg-flush-interval` | 删除 | Raft 消息攒批发出的间隔时间。每隔该配置项指定的间隔，Raft 消息会攒批发出。 |
| PD | [`log.level`](/pd-configuration-file.md#level) | 修改 | 默认值由 "INFO" 改为 "info"，保证大小写不敏感。 |
| TiFlash | [`profile.default.enable_elastic_threadpool`](/tiflash/tiflash-configuration.md#配置文件-tiflashtoml) | 新增  |  表示是否启用可自动扩展的线程池。打开该配置项可以显著提高 TiFlash 在高并发场景的 CPU 利用率。默认值为 `false`。|
| TiFlash | [`storage.format_version`](/tiflash/tiflash-configuration.md#配置文件-tiflashtoml) | 新增 | 表示 DTFile 储存文件格式，默认值为 `2`，该格式在数据文件中内嵌哈希值。也可以设置为 `3`，该格式包含元数据，标记数据校验，支持多种哈希算法。|
| TiFlash | [`logger.count`](/tiflash/tiflash-configuration.md#配置文件-tiflashtoml) | 修改 | 默认值修改为 `10`。 |
| TiFlash | [`status.metrics_port`](/tiflash/tiflash-configuration.md#配置文件-tiflashtoml) | 修改 | 默认值修改为 `8234`。 |
| TiFlash | [`raftstore.apply-pool-size`](/tiflash/tiflash-configuration.md#配置文件-tiflash-learnertoml) | 新增 | 处理 Raft 数据落盘的线程池中线程的数量，默认值为 `4`。 |
| TiFlash | [`raftstore.store-pool-size`](/tiflash/tiflash-configuration.md#配置文件-tiflash-learnertoml) | 新增 | 处理 Raft 的线程池中线程的数量，即 Raftstore 线程池的大小，默认值为 `4`。 |
| TiDB Data Migration (DM)  | [`collation_compatible`](/dm/task-configuration-file-full.md#完整配置文件示例) | 新增 | 同步 CREATE 语句中缺省 Collation 的方式，可选 "loose" 和 "strict"，默认为 "loose"。 |
| TiCDC | `max-message-bytes` | 修改 | 将 Kafka sink 模块的 `max-message-bytes` 默认值设置为 `104857601`（10MB）。  |
| TiCDC | `partition-num`      | 修改 | 将 Kafka Sink `partition-num` 的默认值改由 `4` 为 `3`，使 TiCDC 更加平均地分发消息到各个 Kafka partition。 |
| TiDB Lightning | `meta-schema-name` | 修改 | 此配置项控制 TiDB Lightning 在目标 TiDB 中保存 metadata 对应的 schema name。从 v5.4.0 开始，只在开启了并行导入功能时（对应配置为 `tikv-importer.incremental-import = true` ），才会在目标 TiDB 中创建此库。 |
| TiDB Lightning | `task-info-schema-name` |  新增  | 用于配置当 TiDB Lightning 检测到冲突数据时，对应冲突数据存储的库名，默认值为 "lightning_task_info"。如果没有开启冲突检测功能，则无需配置此参数。  |
| TiDB Lightning | `incremental-import` | 新增 | 是否允许向已存在数据的表导入数据。默认值为 false。 |

### 其他

- 为 TiDB 和 PD 之间新增接口。使用 `information_schema.TIDB_HOT_REGIONS_HISTORY` 系统表时，TiDB 需要使用匹配的 PD 版本。
- 对 log 相关参数，TiDB Server、PD Server 和 TiKV Server 将采用统一的参数命名方式来管理日志命名、输出格式、轮转和过期的规则。参见 [TiKV 配置文件 - log](/tikv-configuration-file.md#log-从-v540-版本开始引入)。
- 自 v5.4.0 起，对于通过 Plan Cache 已经缓存的执行计划，如果为其创建绑定 (Binding)，会使得对应查询已经缓存的计划失效。v5.4.0 前已经缓存的计划不受新 Binding 的影响。
- 在 v5.3 及更早版本中，[TiDB Data Migration (DM)](https://docs.pingcap.com/zh/tidb-data-migration/v5.3/) 文档独立于 TiDB 文档。自 v5.4 起，TiDB Data Migration 的文档已合并入相同版本的 TiDB 文档，无需跳转到 DM 文档站，你可以直接在 TiDB 文档站阅读 [DM 文档](/dm/dm-overview.md)。
- 移除 cdclog。自 v5.4.0 起，不再支持 cdclog。
- 改进了给系统变量设置为字符串 "DEFAULT" 的行为，以便与 MySQL 更兼容 [#29680](https://github.com/pingcap/tidb/pull/29680)
- 将系统变量 `lc_time_names` 改成只读 [#30084](https://github.com/pingcap/tidb/pull/30084)
- 将系统变量 `tidb_store_limit` 的作用域从 INSTANCE 或 GLOBAL 更改为 GLOBAL [#30756](https://github.com/pingcap/tidb/pull/30756)
- 当列数据中有零时，禁止列从整型类型转成时间类型 [#25728](https://github.com/pingcap/tidb/pull/25728)
- 修复插入浮点值时对 `Inf` 和 `NaN` 值不报错问题 [#30148](https://github.com/pingcap/tidb/pull/30148)
- 修复了当 Auto ID 超出范围时，`REPLACE` 语句更改其他行 ID 值的问题 [#30301](https://github.com/pingcap/tidb/pull/30301)

## 新功能

### SQL

- **TiDB 从 v5.4.0 起支持 GBK 字符集**

    在 v5.4.0 前，TiDB 支持 `ascii`、`binary`、`latin1`、`utf8` 和 `utf8mb4` 字符集。

    为了更好的支持中文用户，TiDB 从 v5.4.0 起支持 GBK 字符集。在初次初始化 TiDB 集群时开启 TiDB 配置项 [`new_collations_enabled_on_first_bootstrap`](/tidb-configuration-file.md#new_collations_enabled_on_first_bootstrap) 后，TiDB GBK 字符集同时支持 `gbk_bin` 和 `gbk_chinese_ci` 这两种排序规则。

    在使用 GBK 字符集时，需要注意兼容性限制。

    [用户文档](/character-set-gbk.md)

### 安全

- **TiSpark 支持用户认证与鉴权**

    TiSpark 提供数据库和表级别的读写授权验证以及数据库用户认证验证。开启该功能后，能避免业务侧未经授权运行抽数等批量任务获取数据，提高线上集群的稳定性和数据安全性。从 TiSpark v2.5.0 起开始支持。

    该功能默认关闭。开启后，如果用户没有对应的权限，通过 TiSpark 操作会抛出对应的异常。

    [用户文档](https://docs.pingcap.com/zh/tidb/v5.4/tispark-overview#安全)

- **TiUP 部署方式支持为 root 用户生成初始密码**

    集群启动命令增加了 `--init` 参数，有了该参数，在 TiUP 部署场景，TiUP 会为数据库 root 用户生成一个初始的强密码，避免 root 用户使用空密码所带来的安全风险，增强数据库的安全性。

    [用户文档](/production-deployment-using-tiup.md#第-7-步启动集群)

### 性能

- **持续提升 TiFlash 列式存储引擎和 MPP 计算引擎的稳定性和性能**

    - 支持将更多函数下推至 MPP 引擎
        - 字符串函数：`LPAD()`、`RPAD()`、`STRCMP()`
        - 日期时间函数：`ADDDATE(string, real)`、`DATE_ADD(string, real)`、`DATE_SUB(string, real)`、`SUBDATE(string, real)`、`QUARTER()`
    - 引入可扩缩容弹性线程池，提升资源利用率（实验特性）
    - 提升从 TiKV 同步数据时，由行存格式到列存格式的数据转换效率，整体的数据同步性能提升 50%
    - 调整一些配置项的默认值，提升 TiFlash 的性能和稳定性。HTAP 混合负载下，单表简单查询的性能最高提升 20%

    用户文档：[TiFlash 支持的计算下推](/tiflash/tiflash-supported-pushdown-calculations.md)，[TiFlash 配置文件](/tiflash/tiflash-configuration.md#配置文件-tiflashtoml)

- **通过 session 变量实现有界限过期数据读取**

    TiDB 是基于 Raft 协议的多副本分布式数据库。面对高并发，高吞吐业务场景，可以通过 follower 节点实现读性能扩展，构建读写分离架构。

    针对不同的业务场景，follower 提供强一致读和弱一致过期读两种读模式。强一致读模式可以满足数据实时性要求严格的业务场景。然而，当采用该模式时，特别是在跨机房架构下，由于会出现 leader 和 follower 的数据同步延迟、吞吐量降低等情况，会出现延迟问题。

    在对数据实时性要求不高的业务场景下，可以选择过期读模式。使用该模式可以降低延迟和提升吞吐。TiDB 目前支持通过以下方式实现过期读：使用 SQL 语句读取一个基于历史时间的数据和开启基于历史时间的只读事务。通过这两种方式，你均可以从指定时间点或时间范围内读取对应的历史数据。具体用法，请参考[使用 `AS OF TIMESTAMP` 语法读取历史数据](/as-of-timestamp.md)。

    从 v5.4.0 版本开始 TiDB 支持通过 session 变量设置有界限过期读，进一步提升易用性，满足准实时场景下低延迟高吞吐数据访问的业务诉求。具体设置示例如下：

    ```sql
    set @@tidb_replica_read=leader_and_follower
    set @@tidb_read_staleness="-5"
    ```

    通过该设置，TiDB 可以实现就近选取 leader 或 follower 节点，并读取 5 秒钟内的最新过期数据。

    [用户文档](/tidb-read-staleness.md)

- **TiDB 正式发布索引合并功能**

    索引合并 (Index Merge) 是在 TiDB v4.0 版本中作为实验特性引入的一种查询执行方式的优化，可以大幅提高查询在扫描多列数据时条件过滤的效率。例如对以下的查询，若 `WHERE` 子句中两个 `OR` 连接的过滤条件在各自包含的 key1 与 key2 两个列上都存在索引，则索引合并可以同时利用 key1 与 key2 上的索引分别进行过滤，然后合并出最终的结果。

    ```sql
    SELECT * FROM table WHERE key1 <= 100 OR key2 = 200;
    ```

    以往 TiDB 在一个表上的查询只能使用一个索引，无法同时使用多个索引进行条件过滤。相较以往，索引合并避免了此情况下可能不必要的大量数据扫描，也可以使得需要灵活查询不特定多列数据组合的用户利用单列上的索引达到高效稳定的查询，无需大量构建多列复合索引。

    本版本正式发布了索引合并特性，但仍存在以下的使用条件和限制：

    - 目前 TiDB 的索引合并优化只限于*析取范式* (X<sub>1</sub> ⋁ X<sub>2</sub> ⋁ …X<sub>n</sub>)，即 `WHERE` 子句中过滤条件连接词为 `OR`。

    - 如果全新部署的集群版本为 v5.4.0 或以上，此特性默认开启。如果从 v5.4.0 以前的版本升级到 v5.4.0 或以上，默认保持升级前此特性的开关状态（v4.0.0 之前无此项特性的版本默认关闭），由用户决定是否开启。

    [用户文档](/explain-index-merge.md)

- **新增 Raft Engine（实验特性）**

    支持使用 [Raft Engine](https://github.com/tikv/raft-engine) 作为 TiKV 的日志存储引擎。与使用 RocksDB 相比，Raft Engine 可以减少至多 40% 的 TiKV I/O 写流量和 10% 的 CPU 使用，同时在特定负载下提升 5% 左右前台吞吐，减少 20% 尾延迟。此外，Raft Engine 提升了日志回收效率，修复了极端条件下日志堆积的问题。

    Raft Engine 目前仍属于实验特性，并默认关闭。另外请注意 v5.4.0 版本的 Raft Engine 数据格式与之前版本不兼容，对集群做升级操作之前，需要确保所有 TiKV 节点上的 Raft Engine 已被关闭。只建议在 v5.4.0 及以后的版本使用 Raft Engine。

    [用户文档](/tikv-configuration-file.md#raft-engine)

- **支持收集 `PREDICATE COLUMNS` 的统计信息（实验特性）**

    执行 SQL 语句时，优化器在大多数情况下只会用到部分列（例如， `WHERE`、`JOIN`、`ORDER BY`、`GROUP BY` 子句中出现的列）的统计信息，这些用到的列称为 `PREDICATE COLUMNS`。

    从 v5.4.0 开始，你可以设置系统变量 [`tidb_enable_column_tracking`](/system-variables.md#tidb_enable_column_tracking-从-v540-版本开始引入) 的值为 `ON` 开启 TiDB 对 `PREDICATE COLUMNS` 的收集。

    开启后，TiDB 将每隔 100 - [`stats-lease`](/tidb-configuration-file.md#stats-lease) 时间将 `PREDICATE COLUMNS` 信息写入系统表 `mysql.column_stats_usage`。等到业务的查询模式稳定以后，使用 `ANALYZE TABLE TableName PREDICATE COLUMNS` 语法收集 `PREDICATE COLUMNS` 列的统计信息，可以极大地降低收集统计信息的开销。

    [用户文档](/statistics.md#收集部分列的统计信息)

- **支持统计信息的同步加载（实验特性）**

    从 v5.4.0 开始，TiDB 引入了统计信息同步加载的特性（默认关闭），支持执行当前 SQL 语句时将直方图、TopN、CMSketch 等占用空间较大的统计信息同步加载到内存，提高该 SQL 语句优化时统计信息的完整性。

    [用户文档](/statistics.md#加载统计信息)

### 稳定性

- **支持统计信息采集配置持久化**

    统计信息是优化器生成执行计划时所参考的基础信息之一，统计信息的准确性直接影响生成的执行计划是否合理。为了保证统计信息的准确性，有时候需要针对不同的表、分区、索引设置不同的采集配置项。

    TiDB 从 v5.4.0 版本开始支持 `ANALYZE` 配置持久化功能，方便后续收集统计信息时沿用已有配置项。

    `ANALYZE` 配置持久化功能默认开启（系统变量 `tidb_analyze_version` 为默认值 `2`，[`tidb_persist_analyze_options`](/system-variables.md#tidb_persist_analyze_options-从-v540-版本开始引入) 为默认值 `ON`），用于记录手动执行 `ANALYZE` 语句时指定的持久化配置项。记录后，当 TiDB 下一次自动更新统计信息或者你手动收集统计信息但未指定配置项时，TiDB 会按照记录的配置项收集统计信息。

    [用户文档](/statistics.md#持久化-analyze-配置)

### 高可用和容灾

- **优化备份对集群的影响**

    Backup & Restore (BR) 增加了备份线程自动调节功能（默认开启）。该功能通过监控集群资源的使用率自动调节备份的线程数的方式，降低备份过程对集群的影响。在某些 Case 验证中，通过增加集群用于备份的资源和开启备份线程自动调节功能，备份的影响可以降低到 10% 以下。

    [用户文档](/br/br-auto-tune.md)

- **支持 Azure Blob Storage 作为备份目标存储**

    Backup & Restore (BR) 支持 Azure Blob Storage 作为备份的远端目标存储。在 Azure Cloud 环境部署 TiDB 的用户，可以支持使用该功能将集群数据备份到 Azure Blob Storage 服务中。

    [用户文档](/br/backup-and-restore-storages.md)

### 数据迁移

- **为 TiDB Lightning 增加已存在数据表是否允许导入的开关**

    为 TiDB Lightning 增加 `incremental-import` 开关。默认值为 `false`，表明目标表已存在数据时将不会执行导入。将默认值改为 `true` 则继续导入。注意，当使用并行导入特性时，需要将该配置项设为 `true`。

    [用户文档](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-任务配置)

- **增加新配置允许自定义用于保存 TiDB Lightning 并行导入特性的元信息的 schema 名称**

     为 TiDB Lightning 增加 `meta-schema-name` 配置。在并行导入模式下，该参数用于在目标集群保存各个 TiDB Lightning 实例元信息的 schema 名称，默认值为 "lightning_metadata"。对于参与同一批并行导入的每个 TiDB Lightning 实例，必须将此配置项设置为相同的值，否则将无法确保导入数据的正确性。

    [用户文档](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-任务配置)

- **在 TiDB Lightning 中添加重复数据的检测**

    在 `backend=local` 模式下，数据导入完成之前 TiDB Lightning 会输出冲突数据，然后从数据库中删除这些冲突数据。用户可以在导入完成后解析冲突数据，并根据业务规则选择适合的数据进行插入。建议根据冲突数据清洗上游数据源，避免在后续增量数据迁移阶段遇到冲突数据而造成数据不一致。

    [用户文档](/tidb-lightning/tidb-lightning-error-resolution.md)

- **在 TiDB Data Migration (DM) 中优化 relay log 的使用方式**

    - 恢复 `source` 配置中 `enable-relay` 开关。
    - 增加通过 `start-relay` 和 `stop-relay` 命令动态开启和关闭 relay log 的功能。
    - relay log 的开启状态与 `source` 绑定，source 迁移到任意 DM-worker 均保持原有开启或关闭状态。
    - relay log 的存放路径移至 DM-worker 配置文件。

    [用户文档](/dm/relay-log.md)

- **在 DM 中优化[排序规则](/character-set-and-collation.md)的处理方式**

    增加 `collation_compatible` 开关，支持 strict 和 loose（默认）两种模式：

    - 如果对排序规则要求不严格，允许上下游查询结果排序规则不一致，使用默认的 loose 模式可以避免报错。
    - 如果对排序规则要求严格，业务要求排序规则必须一致，则应当使用 strict 模式。但如果下游不支持上游缺省的 collation，同步可能会报错。

    [用户文档](/dm/task-configuration-file-full.md#完整配置文件示例)

- **在 DM 中优化 `transfer source`，支持平滑执行同步任务**

    当 DM-worker 所在各节点负载不均衡时，`transfer source` 命令可用于手动将某 `source` 配置迁移到其他节点。优化后的 `transfer source` 简化了用户操作步骤，不再要求先暂停所有关联 task 而是直接执行平滑迁移，DM 将在内部完成所需操作。

- **DM OpenAPI 特性 GA**

    DM 支持通过 API 的方式进行日常管理，包括增加数据源、管理任务等。本次更新 OpenAPI 从实验特性转为正式特性。

    [用户文档](/dm/dm-open-api.md)

### 问题诊断效率

- **Top SQL（实验特性）**

    新推出实验性特性 Top SQL（默认关闭），帮助用户轻松找到节点中消耗负载较大的查询。

    [用户文档](/dashboard/top-sql.md)

### TiDB 数据共享订阅

- **优化 TiCDC 对集群的影响**

    大幅降低了 TiCDC 启用后，对 TiDB 集群的性能影响。在实验室环境中，TiCDC 对 TiDB 的性能影响可以降低到 5% 以下。

### 部署及运维

- **增强持续性能分析（实验特性）**

    - 支持更多组件：除了 TiDB、PD 和 TiKV 外，v5.4.0 版本中还支持查看 TiFlash CPU Profiling。
    - 支持更方便的查看形式：支持以火焰图形式查看 CPU Profiling 和 Goroutine 结果。
    - 支持更多部署环境：支持在 TiDB Operator 部署环境下启用持续性能分析功能。

    该功能默认关闭，需进入 TiDB Dashboard 持续性能分析页面开启。

    持续性能分析仅支持由 v1.9.0 及以上版本 TiUP 或 v1.3.0 及以上版本 TiDB Operator 升级或安装的集群。

    [用户文档](/dashboard/continuous-profiling.md)

## 提升改进

+ TiDB

    - 支持 `ADMIN {SESSION | INSTANCE | GLOBAL} PLAN_CACHE` 语法，用于清空缓存的查询计划 [#30370](https://github.com/pingcap/tidb/pull/30370)

+ TiKV

    - Coprocessor 支持分页 API 进行流式处理 [#11448](https://github.com/tikv/tikv/issues/11448)
    - 支持 `read-through-lock`，使读操作不需要等待清理 secondary lock [#11402](https://github.com/tikv/tikv/issues/11402)
    - 增加了磁盘保护机制，尽量避免磁盘空间耗尽导致 panic [#10537](https://github.com/tikv/tikv/issues/10537)
    - 日志支持存档和轮替 [#11651](https://github.com/tikv/tikv/issues/11651)
    - 减少 Raft 客户端的系统调用并提高 CPU 效率 [#11309](https://github.com/tikv/tikv/issues/11309)
    - Coprocessor 支持下推 substring 到 TiKV [#11495](https://github.com/tikv/tikv/issues/11495)
    - 通过跳过读锁提高在 RC 隔离级别中扫描的性能 [#11485](https://github.com/tikv/tikv/issues/11485)
    - 减少备份使用的默认线程池大小，并在压力大时限制其使用 [#11000](https://github.com/tikv/tikv/issues/11000)
    - 支持动态调整 Apply 和 Store 线程池大小 [#11159](https://github.com/tikv/tikv/issues/11159)
    - 支持配置 `snap-generator` 线程池大小 [#11247](https://github.com/tikv/tikv/issues/11247)
    - 优化在文件数较多且读写频繁的场景下 RocksDB 的全局锁争用问题 [#250](https://github.com/tikv/rocksdb/pull/250)

+ PD

    - 默认开启历史热点记录功能 [#25281](https://github.com/pingcap/tidb/issues/25281)
    - 新增 HTTP Component 的签名，用于标识请求来源 [#4490](https://github.com/tikv/pd/issues/4490)
    - TiDB Dashboard 更新至 v2021.12.31 [#4257](https://github.com/tikv/pd/issues/4257)

+ TiFlash

    - 优化本地算子通讯
    - 调高 gRPC 非临时线程数，避免频繁创建/销毁线程

+ Tools

    + Backup & Restore (BR)

        - 增加 BR 加密备份时，对密钥的合法性检查 [#29794](https://github.com/pingcap/tidb/issues/29794)

    + TiCDC

        - 减少 "EventFeed retry rate limited" 日志的数量 [#4006](https://github.com/pingcap/tiflow/issues/4006)
        - 降低在同步大量表时的同步延时 [#3900](https://github.com/pingcap/tiflow/issues/3900)
        - 减少 TiKV 节点宕机后 KV client 恢复的时间 [#3191](https://github.com/pingcap/tiflow/issues/3191)

    + TiDB Data Migration (DM)

        - 降低开启 relay 时的 CPU 使用率 [#2214](https://github.com/pingcap/dm/issues/2214)

    + TiDB Lightning

        - 在 TiDB-backend 模式下，默认改用乐观事务进行写入来提升性能 [#30953](https://github.com/pingcap/tidb/pull/30953)

    + Dumpling

        - 提升 Dumpling 检查数据库版本时的兼容性 [#29500](https://github.com/pingcap/tidb/pull/29500)
        - 在导出 `CREATE DATABASE` 和 `CREATE TABLE` 时添加默认的 collation [#3420](https://github.com/pingcap/tiflow/issues/3420)

## Bug 修复

+ TiDB

    - 修复当从 v4.x 版本升级到 v5.x 版本后 `tidb_analyze_version` 的值变化的问题 [#25422](https://github.com/pingcap/tidb/issues/25422)
    - 修复在子查询中使用不同的 collation 导致查询结果错误的问题 [#30748](https://github.com/pingcap/tidb/issues/30748)
    - 修复 `concat(ifnull(time(3))` 的结果与 MySQL 不一致的问题 [#29498](https://github.com/pingcap/tidb/issues/29498)
    - 修复乐观事务下数据索引可能不一致的问题 [#30410](https://github.com/pingcap/tidb/issues/30410)
    - 修复当表达式不能下推给 TiKV 时 IndexMerge 查询计划错误的问题 [#30200](https://github.com/pingcap/tidb/issues/30200)
    - 修复并发的列类型变更导致 schema 与数据不一致的问题 [#31048](https://github.com/pingcap/tidb/issues/31048)
    - 修复当有子查询时 IndexMerge 的查询结果错误的问题 [#30913](https://github.com/pingcap/tidb/issues/30913)
    - 修复当客户端设置过大的 FetchSize 后 TiDB 执行会 panic 的问题 [#30896](https://github.com/pingcap/tidb/issues/30896)
    - 修复 LEFT JOIN 有时会被错误地转换成 INNER JOIN 的问题 [#20510](https://github.com/pingcap/tidb/issues/20510)
    - 修复当 `CASE-WHEN` 表达式与 collation 同时使用时可能 panic 的问题 [#30245](https://github.com/pingcap/tidb/issues/30245)
    - 修复当 `IN` 的值中带有二进制常量时查询结果错误的问题 [#31261](https://github.com/pingcap/tidb/issues/31261)
    - 修复当 CTE 中带有子查询时查询结果错误的问题 [#31255](https://github.com/pingcap/tidb/issues/31255)
    - 修复 `INSERT ... SELECT ... ON DUPLICATE KEY UPDATE` 语句 panic 的问题 [#28078](https://github.com/pingcap/tidb/issues/28078)
    - 修复 INDEX HASH JOIN 报 `send on closed channel` 的问题 [#31129](https://github.com/pingcap/tidb/issues/31129)

+ TiKV

    - 修复 MVCC 删除记录可能不会被 GC 删除的问题 [#11217](https://github.com/tikv/tikv/issues/11217)
    - 修复悲观事务中 prewrite 请求重试在极少数情况下影响数据一致性的风险 [#11187](https://github.com/tikv/tikv/issues/11187)
    - 修复 GC 扫描导致的内存溢出 [#11410](https://github.com/tikv/tikv/issues/11410)
    - 修复当达到磁盘容量满时 RocksDB flush 或 compaction 导致的 panic [#11224](https://github.com/tikv/tikv/issues/11224)

+ PD

    - 修复 Region 统计不受 `flow-round-by-digit` 影响的问题 [#4295](https://github.com/tikv/pd/issues/4295)
    - 修复调度 Operator 因为目标 Store 处于 Down 的状态而无法快速失败的问题 [#3353](https://github.com/tikv/pd/issues/3353)
    - 修复不能 Merge 在 Offline Store 上面的 Region 的问题 [#4119](https://github.com/tikv/pd/issues/4119)
    - 修复热点统计中无法剔除冷热点数据的问题 [#4390](https://github.com/tikv/pd/issues/4390)

+ TiFlash

    - 修复当 MPP 查询被终止时，TiFlash 偶发的崩溃问题
    - 修复 `where <string>` 查询结果出错的问题
    - 修复整数类型主键的列类型设置为较大范围后数据可能不一致的问题
    - 修复输入早于 1970-01-01 00:00:01 UTC 时，`unix_timestamp` 行为与 TiDB/MySQL 不一致的问题
    - 修复 TiFlash 重启时偶发的 `EstablishMPPConnection` 错误
    - 修复在 TiFlash 与 TiDB/TiKV 之间 `CastStringAsDecimal` 行为不一致的问题
    - 修复查询报错 `DB::Exception: Encode type of coprocessor response is not CHBlock`
    - 修复在 TiFlash 与 TiDB/TiKV 之间 `castStringAsReal` 行为不一致的问题
    - 修复 TiFlash 的 `date_add_string_xxx` 函数返回值与 MySQL 不一致的问题

+ Tools

    + Backup & Restore (BR)

        - 修复当恢复完成后，Region 有可能分布不均的问题 [#30425](https://github.com/pingcap/tidb/issues/30425)
        - 修复当使用 `minio` 作为备份存储时，不能在 endpoint 中指定 `'/'` 的问题 [#30104](https://github.com/pingcap/tidb/issues/30104)
        - 修复因为并发备份系统表，导致表名更新失败，无法恢复系统表的问题 [#29710](https://github.com/pingcap/tidb/issues/29710)

    + TiCDC

        - 修复当 `min.insync.replicas` 小于 `replication-factor` 时不能同步的问题 [#3994](https://github.com/pingcap/tiflow/issues/3994)
        - 修复 `cached region` 监控指标为负数的问题 [#4300](https://github.com/pingcap/tiflow/issues/4300)
        - 修复 `mq sink write row` 没有监控数据的问题 [#3431](https://github.com/pingcap/tiflow/issues/3431)
        - 修复 `sql mode` 兼容性问题 [#3810](https://github.com/pingcap/tiflow/issues/3810)
        - 修复在移除同步任务后潜在的 panic 问题 [#3128](https://github.com/pingcap/tiflow/issues/3128)
        - 修复输出默认列值时的 panic 问题和数据不一致的问题 [#3929](https://github.com/pingcap/tiflow/issues/3929)
        - 修复不支持同步默认值的问题 [#3793](https://github.com/pingcap/tiflow/issues/3793)
        - 修复潜在的同步流控死锁问题 [#4055](https://github.com/pingcap/tiflow/issues/4055)
        - 修复在磁盘写满时无日志输出的问题 [#3362](https://github.com/pingcap/tiflow/issues/3362)
        - 修复 DDL 特殊注释导致的同步停止的问题 [#3755](https://github.com/pingcap/tiflow/issues/3755)
        - 修复在某些 RHEL 发行版上因时区问题导致服务无法启动的问题 [#3584](https://github.com/pingcap/tiflow/issues/3584)
        - 修复因 checkpoint 不准确导致的潜在的数据丢失问题 [#3545](https://github.com/pingcap/tiflow/issues/3545)
        - 修复在容器环境中 OOM 的问题 [#1798](https://github.com/pingcap/tiflow/issues/1798)
        - 修复 `config.Metadata.Timeout` 没有正确配置而导致的同步停止问题 [#3352](https://github.com/pingcap/tiflow/issues/3352)

    + TiDB Data Migration (DM)

        - 修复 `CREATE VIEW` 语句中断复制任务的问题 [#4173](https://github.com/pingcap/tiflow/issues/4173)
        - 修复 skip DDL 后需要重置 Schema 的问题 [#4177](https://github.com/pingcap/tiflow/issues/4177)
        - 修复 skip DDL 后未及时更新表检查点的问题 [#4184](https://github.com/pingcap/tiflow/issues/4184)
        - 修复 TiDB 和 Parser 版本兼容问题 [#4298](https://github.com/pingcap/tiflow/issues/4298)
        - 修复部分 syncer metrics 只有在查询状态时才得以更新的问题 [#4281](https://github.com/pingcap/tiflow/issues/4281)

    + TiDB Lightning

        - 修复当 TiDB Lightning 没有权限访问 `mysql.tidb` 表时，导入的结果不正确的问题 [#31088](https://github.com/pingcap/tidb/issues/31088)
        - 修复 TiDB Lightning 重启时，跳过某些检查的问题 [#30772](https://github.com/pingcap/tidb/issues/30772)
        - 修复当 S3 路径不存在时，TiDB Lightning 没有及时报错的问题 [#30674](https://github.com/pingcap/tidb/pull/30674)

    + TiDB Binlog

        - 修复 Drainer 不兼容 `CREATE PLACEMENT POLICY` 语句导致处理失败的问题 [#1118](https://github.com/pingcap/tidb-binlog/issues/1118)
