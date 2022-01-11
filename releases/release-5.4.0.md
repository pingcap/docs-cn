---
title: TiDB 5.4 Release Notes
---

# TiDB 5.4 Release Notes

发版日期：2022 年 x 月 x 日

TiDB 版本：5.4.0

在 v5.4.0 版本中，你可以获得以下关键特性：

+ 支持 GBK 字符集
+ 支持索引合并 (Index Merge) 数据访问方法，能够合并多个列上索引的条件过滤结果
+ 支持通过 session 变量实现有界限过期数据读取
+ 支持统计信息采集配置持久化
+ 支持使用 Raft Engine 作为 TiKV 的日志存储引擎
+ 优化备份对集群的影响
+ 支持 Azure Blob Storage 作为备份目标存储（实验特性）
+ 持续提升 TiFlash 列式存储引擎和 MPP 计算引擎的稳定性和性能
+ 为 TiDB Lightning 增加已存在数据表是否允许导入的开关
+ 优化持续性能分析实验特性
+ TiSpark 支持用户认证与鉴权

## 兼容性变化

> **注意：**
>
> 当从一个早期的 TiDB 版本升级到 TiDB v5.4.0 时，如需了解所有中间版本对应的兼容性更改说明，请查看对应版本的 [Release Notes](/releases/release-notes.md)。

### 系统变量

|  变量名    |  修改类型    |  描述    |
| :---------- | :----------- | :----------- |
|  `tidb_backoff_lock_fast` | 修改 | 默认值由 `100` 修改为 `10` |
|  [`tidb_enable_column_tracking`](/system-variables.md#tidb_enable_column_tracking-从-v540-版本开始引入) | 新增 | 用于控制是否开启 TiDB 对 `PREDICATE COLUMNS` 的收集，默认值为 `OFF` |
| `tidb_enable_index_merge` | 修改 | 默认值由 `OFF` 改为 `ON`。如果从低于 v4.0.0 版本升级到 v5.4.0 及以上版本的集群，该变量值默认保持 `OFF`。如果从 v4.0.0 及以上版本升级到 v5.4.0 及以上版本的集群，该变量开关保持升级前的状态。对于 v5.4.0 及以上版本的新建集群，该变量开关默认保持 `ON`。 |
| [`tidb_enable_paging`](/system-variables.md#tidb_enable_paging-从-v540-版本开始引入)  | 新增 | 此变量用于控制 `IndexLookUp` 算子是否使用分页 (paging) 方式发送 Coprocessor 请求，默认值为 `OFF`。对于使用 `IndexLookUp` 和 `Limit` 并且 `Limit` 无法下推到 `IndexScan` 上的读请求，可能会出现读请求的延迟高、TiKV 的 Unified read pool CPU 使用率高的情况。在这种情况下，由于 `Limit` 算子只需要少部分数据，开启 `tidb_enable_paging`，能够减少处理数据的数量，从而降低延迟、减少资源消耗。 |
| `tidb_read_staleness` | 新增 | 用于设置当前会话允许读取的历史数据范围，默认值为 `0` |
| [`tidb_stats_load_sync_wait`](/system-variables.md#tidb_stats_load_sync_wait-从-v540-版本开始引入) | 新增 | 这个变量用于控制是否开启统计信息的同步加载模式（默认为 `OFF` 代表不开启，即为异步加载模式），以及开启的情况下，SQL 执行同步加载完整统计信息等待多久后会超时。 |
| [`tidb_stats_load_pseudo_timeout`](/system-variables.md#tidb_stats_load_pseudo_timeout-从-v540-版本开始引入) | 新增 | 用于控制统计信息同步加载超时后，SQL 是执行失败 (`OFF`) 还是退回使用 pseudo 的统计信息 (`ON`)，默认值为 `ON` |
| [`tidb_persist_analyze_options`](/system-variables.md#tidb_persist_analyze_options-从-v540-版本开始引入)  | 新增  | 用于控制是否开启 [ANALYZE 配置持久化](/statistics.md#analyze-配置持久化)特性，默认值为 `OFF` |
| `tidb_store_limit` | 修改 | v5.4.0 前支持实例级别及集群级别的设置，现在只支持集群级别的设置 |

### 配置文件参数

|  配置文件    |  配置项    |  修改类型    |  描述    |
| :---------- | :----------- | :----------- | :----------- |
| TiDB | [`stats-load-concurrency`](/tidb-configuration-file.md#stats-load-concurrency-从-v540-版本开始引入) | 新增 |  用于设置 TiDB 统计信息同步加载功能可以并发处理的最大列数，默认值为 `5`             |
| TiDB | [`stats-load-queue-size`](/tidb-configuration-file.md#stats-load-queue-size-从-v540-版本开始引入)   | 新增 |  用于设置 TiDB 统计信息同步加载功能最多可以缓存多少列的请求，默认值为 `1000`             |
| TiKV | `snap-generator-pool-size` | 新增 | `snap-generator` 线程池大小，默认值为 `2` |
| TiKV | `log.file.max-size`、`log.file.max-days`、`log.file.max-backups` | 新增  | 参数说明见 [TiKV 配置文件 - log.file](/tikv-configuration-file.md#logfile-从-v540-版本开始引入)。 |
| TiKV | `raft-engine` | 新增 | 包含 `enable`、`dir`、`batch-compression-threshold`、`bytes-per-sync`、`target-file-size`、`purge-threshold`、`recovery-mode`、`recovery-read-block-size`、`recovery-read-block-size`、`recovery-threads`，详情参见 [TiKV 配置文件：raft-engine](/tikv-configuration-file.md#raft-engine)。|
| TiKV | `raftstore.raft-log-compact-sync-interval` | 新增 | 控制 CompactLog 命令的间隔，默认值为 `2s` |
| TiKV | [`backup.enable-auto-tune`](/tikv-configuration-file.md#enable-auto-tune-从-v54-版本开始引入) | 修改 | 在 v5.3.0 中默认值为 `false`，自 v5.4.0 起默认值改为 `true`。表示在集群资源占用率较高的情况下，是否允许 BR 自动限制备份使用的资源，减少对集群的影响。在默认配置下，备份速度可能下降。 |
| TiKV | `log-level`、`log-format`、`log-file`、`log-rotation-size` | 修改 | 将 TiKV log 参数名替换为与 TiDB log 参数一致的参数名，即 `log.level`、`log.format`、`log.file.filename`、`log.enable-timestamp`。如果只设置了原参数、且把其值设为非默认值，原参数与新参数会保持兼容；如果同时设置了原参数和新参数，则会使用新参数。详情参见 [TiKV 配置文件 - log](/tikv-configuration-file.md#log-从-v540-版本开始引入)。 |
| TiKV | `raftstore.raft-log-gc-tick-interval` | 修改 | 默认值修改为 `3s` |
| TiKV  |  `log-rotation-timespan`  | 删除 |  轮换日志的时间跨度。当超过该时间跨度，日志文件会被轮换，即在当前日志文件的文件名后附加一个时间戳，并创建一个新文件。 |
| PD | `log.level` | 修改 | 默认值由 "INFO" 改为 "info"，保证大小写不敏感 |
| TiFlash | `profile.default.enable_elastic_threadpool` | 新增  |  表示是否启用可自动扩展的线程池。打开该配置项可以显著提高 TiFlash 在高并发场景的 CPU 利用率。默认值为 `false`。|
| TiDB Data Migration (DM) | [`collation_compatible`](/dm/task-configuration-file-full.md#完整配置文件示例) | 同步 CREATE 语句中缺省 Collation 的方式，可选 "loose" 和 "strict"，默认为 "loose"。 |
| TiFlash | [`storage.format_version`](/tiflash/tiflash-configuration.md#配置文件-tiflashtoml) | 新增 | 表示 DTFile 储存文件格式，默认值为 `2`，该格式在数据文件中内嵌哈希值。也可以设置为 `3`，该格式包含元数据，标记数据校验，支持多种哈希算法。|
| TiFlash | `logger.count` | 修改 | 默认值修改为 `10` |
| TiFlash | `status.metrics_port` | 修改 | 默认值修改为 `8234` |
| TiFlash | `raftstore.apply-pool-size` | 新增 | 处理 Raft 数据落盘的线程池中线程的数量，默认值为 `4`。 |
| TiFlash | `raftstore.store-pool-size` | 新增 | 处理 Raft 的线程池中线程的数量，即 Raftstore 线程池的大小，默认值为 `4`。 |
| TiCDC | `enable-tidb-extension` | 新增 |  开启该配置项后，TiCDC 在 Canal-JSON 协议格式中附加 TiDB 扩展字段。                  |
| TiCDC | `max-message-bytes` | 修改 | 将 Kafka sink 模块的 `max-message-bytes` 默认值设置为 `10M`  |
| TiCDC | `partition-num`      | 修改 | 将 Kafka Sink `partition-num` 的默认值改由 `4` 为 `3`，使 TiCDC 更加平均地分发消息到各个 Kafka partition |
| TiDB Lightning | `meta-schema-name` |  新增  | 在并行导入模式下，在目标集群保存各个 TiDB Lightning 实例元信息的 schema 名字，默认值为 "lightning_metadata"  |
| TiDB Lightning | `incremental-import` | 新增 | 是否允许向已存在数据的表导入数据。默认值为 false |

### 其他

- TiDB Dashboard 默认不再使用 `root` + 空密码登录。

    从 v5.4.0开始，使用 TiUP 启动集群时推荐使用 `start --initial`。执行该操作启动集群后，会为 `root` 账号自动生成一个随机密码，`root` 账号登录 Dashboard 需要使用这个密码。

- 为 TiDB 和 PD 之间新增接口。使用 `information_schema.TIDB_HOT_REGIONS_HISTORY` 系统表时，TiDB 需要使用匹配的 PD 版本。
- TiDB Server、PD Server 和 TiKV Server 将采用统一的参数命名方式来管理日志命名、输出格式、轮转和过期的规则。参见 [TiKV 配置文件 - log](/tikv-configuration-file.md#log-从-v540-版本开始引入)。

## 新功能

### SQL

- **TiDB 从 v5.4.0 起支持 GBK 字符集**

    在 v5.4.0 前，TiDB 支持 `ascii`、`binary`、`latin1`、`utf8` 和 `utf8mb4` 字符集。为了更好的支持中文用户，TiDB 从 v5.4.0 版本开始支持 GBK 字符集，同时支持 `gbk_bin` 和 `gbk_chinese_ci` 两种排序规则（在使用这两种排序规则前需要开启 TiDB 配置项 `new_collations_enabled_on_first_bootstrap`）。

在使用 GBK 字符集时，需要注意兼容性限制，详情参考[字符集和排序 - GBK](/character-set-gbk.md)。

### 安全

- **TiSpark 支持用户认证与鉴权**

    TiSpark 提供数据库和表级别的读写授权验证以及数据库用户认证验证。开启该功能后，能避免业务侧未经授权运行抽数等批量任务获取数据，提高线上集群的稳定性和数据安全性。从 TiSpark v2.5.0 起开始支持。

    该功能默认关闭。开启后，如果用户没有对应的权限，通过 TiSpark 操作会抛出对应的异常。

### 性能

- **新增 Raft Engine（实验特性）**

    支持使用 [Raft Engine](https://github.com/tikv/raft-engine) 作为 TiKV 的日志存储引擎。与使用 RocksDB 相比，Raft Engine 可以减少至多 40% 的 TiKV I/O 写流量和 10% 的 CPU 使用，同时在特定负载下提升 5% 左右前台吞吐，减少 20% 尾延迟。

    由于 Raft Engine 涉及数据格式改动，目前仍属于实验特性，并默认关闭。同时请注意最新的 Raft Engine 不与 v5.4.0 版本前的 Raft Engine 兼容。因此在进行跨越 v5.4.0 版本的升级和降级之前，需要确保已有 TiKV 节点上的 Raft Engine 已被关闭。

    [用户文档](/tikv-configuration-file.md#raft-engine)

- **持续提升 TiFlash 列式存储引擎和 MPP 计算引擎的稳定性和性能**

    - 支持将更多函数下推至 MPP 引擎
        - 字符串函数：`LPAD()`、`RPAD()`、`STRCMP()`
        - 日期时间函数：`ADDDATE()`、`DATE_ADD()`、`DATE_SUB()`、`SUBDATE()`、`QUARTER()`
    - 引入动态线程池，提升资源利用率（实验特性）
    - 新增或修改一些 TiFlash 已有配置的默认值，提升 TiFlash 的性能和稳定性
    - 提升由行存到列存数据同步处理时对 raft log 的解码 (decoding) 效率，使 CPU 使用率降低达 90%
    - TiFlash 调整了文件系统中 Delta Tree 相关的默认参数，使之更适合一般的生产环境

- **通过 session 变量实现有界限过期数据读取**

    TiDB 是基于 Raft 协议的多副本分布式数据库。面对高并发，高吞吐业务场景，可以通过follower 节点实现读性能扩展，构建读写分离架构。

    针对不同的业务场景，follower 提供强一致读和弱一致过期读两种读模式。强一致读满足数据实时性要求严格的业务场景，但是因为 leader 和 follower 的数据同步延迟、吞吐较低、延迟较高，特别是在跨机房架构下延迟问题被进一步放大。

    在对数据实时性要求不高的业务场景下，可以选择过期读模式。使用该模式可以降低延迟和提升吞吐。TiDB 目前支持通过显示只读事务或 SQL 语句的方式实现过期读。两种方式均支持指定时间的精确过期读和指定时间边界的过期读两种模式，详细用法请参考[过期读文档](/read-historical-data.md)。

    从 v5.4.0 版本开始 TiDB 支持通过 session 变量设置有界限过期读，进一步提升易用性，具体设置如下：

    ```sql
    set @@tidb_replica_read=leader_and_follower
    set @@tidb_read_staleness="-5"
    ```

    通过该设置，可以实现就近选取 leader 或 follower 节点，并读取 5 秒钟前的最新过期数据，满足准实时场景下低延迟高吞吐数据访问的业务诉求，降低研发门槛，提升易用性。

- **TiDB 正式发布索引合并 (Index Merge) 功能**

    [索引合并](/explain-index-merge.md) 是在 TiDB v4.0 版本中作为实验特性引入的一种查询执行方式的优化，可以大幅提高查询在扫描多列数据时条件过滤的效率。例如对以下的查询，若 `WHERE` 子句中两个 `OR` 连接的过滤条件在各自包含的 _key1_ 与 _key2_ 两个列上都存在索引，则 _索引合并_ 可以同时利用  _key1_ 与 _key2_ 上的索引分别进行过滤，然后合并出最终的结果。

    ```sql
    SELECT * FROM table WHERE key1 <= 100 OR key2 = 200;
    ```

    以往 TiDB 在一个表上的查询只能使用一个索引，无法同时使用多个索引进行条件过滤。相较以往，_索引合并_ 避免了此情况下可能不必要的大量数据扫描，也可以使得需要灵活查询不特定多列数据组合的用户利用单列上的索引达到高效稳定的查询，无需大量构建多列复合索引。

    本版本正式发布了 _索引合并 (Index Merge)_ 特性，但仍存在以下的使用条件和限制（详情请参见[用户文档](/explain-index-merge.md)）：

    目前 TiDB 的 _索引合并_ 优化只限于 _析取范式_ (X<sub>1</sub> ⋁ X<sub>2</sub> ⋁ …X<sub>n</sub>)，即 `WHERE` 子句中过滤条件连接词为 `OR`。

    如果全新部署的集群版本为 v5.4.0 或以上，此特性默认开启。如果从 v5.4.0 以前的版本升级到 v5.4.0 或以上，默认保持升级前此特性的开关状态（v4.0.0 之前无此项特性的版本默认关闭），由用户决定是否开启。

- **支持收集部分列的统计信息（实验特性）**
    
    执行 SQL 语句时，优化器在大多数情况下只会用到部分列（例如， `WHERE`、`JOIN`、`ORDER BY`、`GROUP BY` 子句中用到的列）的统计信息。这些被优化器用到的列称为 `PREDICATE COLUMNS`。
    
    从 v5.4.0 开始，TiDB 引入了收集部分列的统计信息的特性（默认关闭），支持只收集指定列或者 `PREDICATE COLUMNS` 的统计信息，极大地降低了收集统计信息的开销。
    
    [用户文档](/statistics.md#收集部分列的统计信息)
    
- **支持统计信息的同步加载（实验特性）**

    从 v5.4.0 开始，TiDB 引入了统计信息同步加载的特性（默认关闭），支持执行当前 SQL 语句时将直方图、TopN、CMSketch 等占用空间较大的统计信息同步加载到内存，提高该 SQL 语句优化时统计信息的完整性。
    
    [用户文档](/statistics.md#统计信息的加载)

### 稳定性

- **支持统计信息采集配置持久化**

    统计信息是优化器生成执行计划时所参考的基础信息之一，统计信息的准确性直接影响生成的执行计划是否合理。为了保证统计信息的准确性，有时候需要针对不同的表、分区、索引设置不同的采集配置项。

    TiDB 从 v5.4.0 版本开始支持 `ANALYZE` 配置持久化功能，方便后续收集统计信息时沿用已有配置项。
    
    `ANALYZE` 配置持久化功能默认开启（系统变量 `tidb_analyze_version = 2` 且 `tidb_persist_analyze_options = true`），用于记录手动执行 `ANALYZE` 语句时指定的持久化配置项。记录后，当 TiDB 下一次自动更新统计信息或者你手动收集统计信息但未指定配置项时，TiDB 会按照记录的配置项收集统计信息。
    
    [用户文档](/statistics.md#analyze-配置持久化)


## 高可用和容灾

- **优化备份对集群的影响**

    Backup & Restore (BR) 增加了备份线程自动调节功能（默认开启）。该功能通过监控集群资源的使用率自动调节备份的线程数的方式，降低备份过程对集群的影响。在某些 Case 验证中，通过增加集群用于备份的资源和开启备份线程自动调节功能，备份的影响可以降低到 10% 以下。
    详细文档请阅读 [BR 自动调节](/br/br-features.md#自动调节-从-v54-版本开始引入)。

- **支持 Azure Blob Storage 作为备份目标存储（实验特性）**

    Backup & Restore (BR) 支持 Azure Blob Storage 作为备份的远端目标存储。在 Azure Cloud 环境部署 TiDB 的用户，可以支持使用该功能将集群数据备份到 Azure Blob Storage 服务中。

    该功能目前是实验特性，详细情况参考 [BR 支持 Azure Blob Storage 远端存储](/br/backup-and-restore-azblob.md)。


### 数据迁移

- **为 TiDB Lightning 增加已存在数据表是否允许导入的开关**

    为 TiDB Lightning 增加 `incremental-import` 开关。默认值为 `false`，表明目标表已存在数据时将不会执行导入。将默认值改为 `true` 则继续导入。注意，当使用并行导入特性时，需要将该配置项设为 `true`。

- **为 TiDB Lightning 增加新参数，用于在并行导入模式下保存各个 TiDB Lightning 实例元信息的 schema 名字 **

     为 TiDB Lightning 增加 `meta-schema-name` 参数。在并行导入模式下，该参数用于在目标集群保存各个 TiDB Lightning 实例元信息的 schema 名字，默认值为 "lightning_metadata"。对于参与同一批并行导入的每个 TiDB Lightning 实例，必须将此配置项设置为相同的值，否则将无法确保导入数据的正确性。

- **在 TiDB Lightning 中添加重复数据的检测**

    在 `backend=local` 模式下，数据导入完成之前 TiDB Lightning 会输出冲突数据，然后从数据库中删除这些冲突数据。用户可以在导入完成后解析冲突数据，并根据业务规则选择适合的数据进行插入。建议根据冲突数据清洗上游数据源，避免在后续增量数据迁移阶段遇到冲突数据而造成数据不一致。

- **在 TiDB Data Migration (DM) 中 优化 relay log 的使用方式**

    - 恢复 `source` 配置中 `enable-relay` 开关
    - 增加 `start-relay` 或 `stop-relay` 命令中动态开启或关闭 relay log 的功能
    - relay log 的开启状态与 `source` 绑定，source 迁移到任意 DM-worker 均保持原有开启或关闭状态
    - relay log 的存放路径移至 DM-worker 配置文件

- **在 DM 中优化排序规则的处理方式**

    增加 `collation_compatible` 开关，支持 `strict` 和 `loose`（默认）两种模式。如果对排序规则要求不严格，允许排序规则在上下游不一致，使用默认的 `loose` 模式可使同步正常进行；如果对排序规则要求严格，排序规则在上下游不一致会导致业务报错，则可以使用 `strict` 模式。

- **在 DM 中优化 `transfer source`，支持平滑执行同步任务**

    当 DM-worker 所在各节点负载不均衡时，`transfer source` 命令可用于手动将某 `source` 配置迁移到其他节点。优化后的 `transfer source` 简化了用户操作步骤，不再要求先暂停所有关联 task 而是直接执行平滑迁移，DM 将在内部完成所需操作。

- **DM OpenAPI 特性 GA**

    DM 支持通过 API 的方式进行日常管理，包括增加数据源、管理任务等。本次更新 OpenAPI 从实验特性转为正式特性。

### 问题诊断效率

- **Top SQL（实验特性）**

    新推出实验性特性 Top SQL（默认关闭），帮助用户轻松找到节点中负载贡献较大的查询。

    [用户文档](/dashboard/top-sql.md)

### TiDB 数据共享订阅

- **优化 TiCDC 对集群的影响**

    大幅降低了 TiCDC 启用后，对 TiDB 集群的性能影响。在实验室环境中，TiCDC 对 TiDB 的性能影响可以降低到 5% 以下。

### 部署及运维

- **持续性能分析（实验特性）**

    - 支持更多组件：除了 TiDB、PD 和 TiKV 外，v5.4.0 版本中还支持查看 TiFlash CPU Profiling
    - 支持更方便的查看形式：支持以火焰图形式查看 CPU Profiling 和 Goroutine 结果。
    - 支持更多部署环境：支持在 TiDB Operator 部署环境下启用持续性能分析功能。

    该功能默认关闭，需进入 TiDB Dashboard 持续性能分析页面开启，开启方法见[用户文档](/dashboard/continuous-profiling.md)。

    持续性能分析仅支持由 v1.9.0 及以上版本 TiUP 或 v1.3.0 及以上版本 TiDB Operator 升级或安装的集群。

## 提升改进

+ TiDB

    - 新增系统变量 `tidb_enable_paging`，开启该功能可显著降低使用 `IndexLookUp` 和 `Limit` 并且 `Limit` 数据较小且无法下推到 `IndexScan` 上的读请求的延迟 [#30578](https://github.com/pingcap/tidb/issues/30578)
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
- 优化在文件数较多且读写频繁的场景下 RocksDB 的全局锁争用问题 [rocksdb#250](https://github.com/tikv/rocksdb/pull/250)

+ PD

+ TiFlash

+ Tools

    + Backup & Restore (BR)

    + TiCDC

    + TiDB Data Migration (DM)

    + TiDB Lightning

    + Dumpling

    + TiDB Binlog

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

+ TiFlash

+ Tools

    + Backup & Restore (BR)

    + TiCDC

    + TiDB Data Migration (DM)

    + TiDB Lightning

        - 修复当 TiDB Lightning 没有权限访问 `mysql.tidb` 表时，导入的结果不正确的问题 [#31088](https://github.com/pingcap/tidb/issues/31088)

    + Dumpling

    + TiDB Binlog


