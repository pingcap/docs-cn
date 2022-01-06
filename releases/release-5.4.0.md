---
title: TiDB 5.4 Release Notes
---

# TiDB 5.4 Release Notes

发版日期：2022 年 x 月 x 日

TiDB 版本：5.4.0

在 v5.4.0 版本中，你可以获得以下关键特性：

+
+
+


## 兼容性变化

> **注意：**
>
> 当从一个早期的 TiDB 版本升级到 TiDB v5.4.0 时，如需了解所有中间版本对应的兼容性更改说明，请查看对应版本的 [Release Notes](/releases/release-notes.md)。

### 系统变量

|  变量名    |  修改类型    |  描述    |
| :---------- | :----------- | :----------- |
|  `tidb_backoff_lock_fast` | 修改 | 默认值由 `100` 修改为 `10` |
| `tidb_enable_index_merge` | 修改 | 默认值由 `OFF` 改为 `ON`。如果从 TiDB v4.0（不包含 v4.0.0）升级到 v5.4.0 及更新的集群，该变量值默认保持 `OFF`。 |
| `tidb_enable_paging`  | 新增 | 此变量用于控制 `IndexLookUp` 算子是否使用 paging 方式发送 coprocessor 请求，默认值为 `OFF`。对于使用 `IndexLookUp` 和 `Limit` 并且 `Limit` 无法下推到 `IndexScan` 上的读请求，可能出现延迟高、TiKV 的 unified read pool CPU 使用高的情况。在这种情况下，由于 `Limit` 算子限制只需要少部分数据，开启 `tidb_enable_paging`，能够减少处理数据的数量，降低延迟，减少资源消耗。 |
| `tidb_read_staleness` | 新增 |  |
| `tidb_stats_load_sync_wait` | 新增 |  |
| `tidb_stats_load_pseudo_timeout` | 新增 |  |

### 配置文件参数

|  配置文件    |  配置项    |  修改类型    |  描述    |
| :---------- | :----------- | :----------- | :----------- |
| TiDB | `stats-load-concurrency` | 新增 |               |
| TiDB | `stats-load-queue-size`   | 新增 |               |
| TiKV | `backup.enable-auto-tune` | 修改 | 在 v5.3.0 中默认值为 `false`，自 v5.4.0 起默认值改为 `true`。表示在集群资源占用率较高的情况下，是否允许 BR 自动限制备份使用的资源以求减少对集群的影响。在默认配置下，备份速度可能下降。 |
| TiKV | `log.level`、`log.format`、`log.enable-timestamp`、`log.file.filename`、`log.file.max-size`、`log.file.max-days`、`log.file.max-backups` | 新增  | 参数说明见[统一各组件的日志格式和日志归档轮转规则](#统一各组件的日志格式和日志归档轮转规则)。 |
| TiKV | `log-level`、`log-format`、`log-file`、`log-rotation-size`、`log-rotation-timespan` | 删除 | 废弃 TiKV log 参数，改为使用与 TiDB log 参数一致的命名方式，即 `log.level`、`log.format`、`log.enable-timestamp`。如果 TiKV log 参数为非默认值则保持兼容；如果同时配置 TiKV log 参数和 TiDB log 命名方式的参数，使用 TiDB log 命名方式的参数。详情参见[统一各组件的日志格式和日志归档轮转规则](#统一各组件的日志格式和日志归档轮转规则)。 |
| TiKV | `raft-engine` | 新增 | 包含 `enable`、`dir`、`batch-compression-threshold`、`bytes-per-sync`、`target-file-size`、`purge-threshold`、`recovery-mode`、`recovery-read-block-size`、`recovery-read-block-size`、`recovery-threads`，详情参见 [TiKV 配置文件：raft-engine](/tikv-configuration-file.md#raft-engine)。
| PD | `log.level` | 修改 | 默认值由 "INFO" 改为 "info"，保证大小写不敏感 |
| PD | `hot-regions-write-interval` | 新增 |  设置 PD 存储 Hot Region 信息的时间间隔。默认值为 `10m`。 |
| PD | `hot-regions-reserved-days` | 新增 | 设置 PD 保留的 Hot Region 信息的最长时间。默认为 7 天。
| TiFlash | `profile.default.enable_elastic_threadpool` | 新增  |  表示是否启用可自动扩展的线程池。打开该配置项可以显著提高 TiFlash 在高并发场景的 CPU 利用率。默认值为 `false`。|
| TiDB Data Migration (DM) | `collation_compatible` | 同步 CREATE 语句中缺省 Collation 的方式，可选 "loose" 和 "strict"，默认为 "loose"。 |
| TiFlash | `storage.format_version` | 新增可选值 | 表示 DTFile 储存文件格式，默认值为 `2`。|
| TiFlash | `logger.count` | 修改 | 默认值修改为 `10` |
| TiFlash | `status.metrics_port` | 修改 | 默认值修改为 `8234` |

#### 统一各组件的日志格式和日志归档轮转规则

TiDB 提供了多个用户可见的组件，为了保证使用体验的一致性，从 v5.4.0 版本开始 TiDB Server、PD Server 和 TiKV Server 将采用统一的参数命名方式来管理日志命名、输出格式、轮转和过期的规则。具体日志设置如下：

```
level = "info"
设置日志输出等级，默认为 info，支持 debug, info, warn, error, fatal 五个等级。

format = "text"
设置日志输出格式，默认为 text，支持 text 和 json 两种格式。

enable-timestamp = true
设置时间戳输出开关，默认为 true。

filename = ""
设置日志文件名前缀，默认为无前缀。

max-size = 300
设置日志分割大小，默认为 300 MB，最大支持 4096 MB。

max-days = 0
设置日志最大保留天数，默认全保留不清理。

max-backups = 0
设置日志备份的最大保留文件数，默认全保留不清理。
```

### 其他

- TiDB Dashboard 默认不再使用 `root` + 空密码登录。

    从 v5.4.0开始，使用 TiUP 启动集群时推荐使用 `start --initial`。执行该操作启动集群后，会为 `root` 账号自动生成一个随机密码，`root` 账号登录 Dashboard 需要使用这个密码。

- 从 TiDB v4.0（不包含 v4.0.0）升级到 v5.4.0 及更新的集群，`tidb_enable_index_merge` 变量默认关闭。


## 新功能

### SQL

- **功能 1**

    <功能描述 （功能是什么 + 能给用户带来什么好处 + 需要用户注意什么）>

    <功能支持情况，告诉用户 TiDB 默认开始还是关闭此功能，如果默认关闭，如何开启>

    <如果功能限制或此功能特定的兼容性问题，需要提及>

    [用户文档](/)

- **TiDB 从 v5.4.0 起支持 GBK 字符集**

    在 v5.4.0 前，TiDB 支持 `ascii`、`binary`、`latin1`、`utf8` 和 `utf8mb4` 字符集。为了更好的支持中文用户，TiDB 从 v5.4.0 版本开始支持 GBK 字符集，同时支持 `gbk_bin` 和 `gbk_chinese_ci` 两种排序规则。

    在使用 GBK 字符集时，请注意以下兼容性限制：

    - TiFlash 暂不支持 GBK 字符。
    - TiCDC 暂不支持 GBK 字符。
    - 如果 `character_set_client` 和 `character_set_connection` 都是 `gbk` 时，处理非法 GBK 字符与 MySQL 存在兼容性问题。
    - `character_set_client` 在处理 `prepare` 语句时可能出现兼容性问题。
    - TiDB 不支持 `_gbk"xxx"` 的用法，但是支持 `_utf8mb4"xxx"` 的用法。而 MySQL 对于 `_charset"xxx"` 的用法都支持。
    - TiDB Lightning 在 v5.4.0 之前不支持导入 `charset=GBK` 的表。BR 在 v5.3.0 之前不支持恢复 `charset=GBK` 的表。

### 事务

- **功能 3**

    <功能描述 （功能是什么 + 能给用户带来什么好处 + 需要用户注意什么）>

    <功能支持情况，告诉用户 TiDB 默认开始还是关闭此功能，如果默认关闭，如何开启>

    <如果功能限制或此功能特定的兼容性问题，需要提及>

    [用户文档](/)

- **功能 4**

    <功能描述 （功能是什么 + 能给用户带来什么好处 + 需要用户注意什么）>

    <功能支持情况，告诉用户 TiDB 默认开始还是关闭此功能，如果默认关闭，如何开启>

    <如果功能限制或此功能特定的兼容性问题，需要提及>

    [用户文档](/)

### 安全

- **功能 5**

    <功能描述 （功能是什么 + 能给用户带来什么好处 + 需要用户注意什么）>

    <功能支持情况，告诉用户 TiDB 默认开始还是关闭此功能，如果默认关闭，如何开启>

    <如果功能限制或此功能特定的兼容性问题，需要提及>

    [用户文档](/)

- **TiSpark 支持用户认证与鉴权**

    TiSpark 提供数据库和表级别的读写授权验证以及数据库用户认证验证。开启该功能后，能避免业务侧未经授权运行抽数等批量任务获取数据，提高线上集群的稳定性和数据安全性。从 TiSpark v2.5.0 起开始支持。

    该功能默认关闭。开启后，如果用户没有对应的权限，通过 TiSpark 操作会抛出对应的异常。

### 性能

- **功能 6**

    <功能描述 （功能是什么 + 能给用户带来什么好处 + 需要用户注意什么）>

    <功能支持情况，告诉用户 TiDB 默认开始还是关闭此功能，如果默认关闭，如何开启>

    <如果功能限制或此功能特定的兼容性问题，需要提及>

    [用户文档](/)

- **新增 Raft Engine（实验特性）**

    支持使用 [Raft Engine](https://github.com/tikv/raft-engine) 作为 TiKV 的日志存储引擎。与使用 RocksDB 相比，Raft Engine 可以减少至多 40% 的 TiKV I/O 写流量和 10% 的 CPU 使用，同时在特定负载下提升 5% 左右前台吞吐，减少 20% 尾延迟。

    由于 Raft Engine 涉及数据格式改动，目前仍属于实验特性，并默认关闭。同时请注意最新的 Raft Engine 不与 v5.4.0 版本前的 Raft Engine 兼容。因此在进行跨越 v5.4.0 版本的升级和降级之前，需要确保已有 TiKV 节点上的 Raft Engine 已被关闭。

    [用户文档](/tikv-configuration-file.md#raft-engine)

- TiFlash

  - 支持将更多函数下推至 MPP 引擎
      - 字符串函数：`LPAD()`、`RPAD()`、`STRCMP()`
      - 日期时间函数：`ADDDATE()`、`DATE_ADD()`、`DATE_SUB()`、`SUBDATE()`、`QUARTER()`
  - 引入动态线程池，提升资源利用率
  - 新增或修改一些 TiFlash 已有配置的默认值，提升 TiFlash 的性能和稳定性

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


### 稳定性

- **功能 7**

    <功能描述 （功能是什么 + 能给用户带来什么好处 + 需要用户注意什么）>

    <功能支持情况，告诉用户 TiDB 默认开始还是关闭此功能，如果默认关闭，如何开启>

    <如果功能限制或此功能特定的兼容性问题，需要提及>

    [用户文档](/)

- **支持统计信息采集配置持久化**

    统计信息是优化器生成执行计划时所参考的基础信息之一，统计信息的准确性直接影响生成的执行计划是否合理。为了保证统计信息的准确性，有时候需要针对不同的表、分区、索引设置不同的采集配置项。

    TiDB 从 v5.4.0 版本开始支持通过 `analyze` 命令采集统计信息并持久化指定的配置项，方便后续的统计信息采集沿用已有配置项。具体配置项信息请参考 [`Analyze` 文档](/sql-statements/sql-statement-analyze-table.md#analyze)的 `AnalyzeOption` 章节。

    - 开启采集配置项持久化

        设置 `tidb_analyze_version = 2` 且 `tidb_persist_analyze_options = true` 会开启配置项持久化。开启后，手动 analyze 指定的所有配置项会被持久化并覆盖已有选项。后续的手动或自动 analyze 任务会沿用已有配置项进行统计信息采集，直到持久化功能关闭或用户手动指定新的采集配置项。

    - 关闭采集配置项持久化

        设置 `tidb_analyze_version = 1` 或 `tidb_persist_analyze_options = false` 会关闭采集配置项持久化功能。持久化关闭后，已有配置项不会被删除，但不记录新增配置项。新采集任务不会沿用已有的持久化配置项，再次开启采集配置项持久化将会直接使用已有的配置项进行统计信息采集。如果需要更新已有的配置项，请手动执行 `analyze` 命令并指定新的采集配置项。


## 高可用和容灾

- **功能 8**

    <功能描述 （功能是什么 + 能给用户带来什么好处 + 需要用户注意什么）>

    <功能支持情况，告诉用户 TiDB 默认开始还是关闭此功能，如果默认关闭，如何开启>

    <如果功能限制或此功能特定的兼容性问题，需要提及>

    [用户文档](/)

- **优化备份对集群的影响**

    Backup & Restore (BR) 增加了备份线程自动调节功能。该功能通过监控集群资源的使用率自动调节备份的线程数的方式，降低备份过程对集群的影响。在某些 Case 验证中，通过增加集群用于备份的资源和开启备份线程自动调节功能，备份的影响可以降低到 10% 以下。

    该功能默认开启，但是如果你在离线环境中进行备份，可以关闭该功能来获得更高的备份速度。

    详细文档请阅读 [BR 自动调节](/br/br-features.md#自动调节-从-v54-版本开始引入)。

- **支持 Azure Blob Storage 作为备份目标存储（实验特性）**

    Backup & Restore (BR) 支持 Azure Blob Storage 作为备份的远端目标存储。在 Azure Cloud 环境部署 TiDB 的用户，可以支持使用该功能将集群数据备份到 Azure Blob Storage 服务中。

    该功能目前是实验特性，详细情况参考 [BR 支持 Azure Blob Storage 远端存储](/br/backup-and-restore-azblob.md)。


### 数据迁移

- **功能 9**

    <功能描述 （功能是什么 + 能给用户带来什么好处 + 需要用户注意什么）>

    <功能支持情况，告诉用户 TiDB 默认开始还是关闭此功能，如果默认关闭，如何开启>

    <如果功能限制或此功能特定的兼容性问题，需要提及>

    [用户文档](/)

- **为 TiDB Lightning 增加已存在数据表是否允许导入的开关**

    为 TiDB Lightning 增加 `incremental-import` 开关。默认值为 `false`，表明目标表已存在数据时将不会执行导入。将默认值改为 `true` 则继续导入。注意，当使用并行导入特性时，需要将该配置项设为 `true`。

- **在 TiDB Lightning 中添加重复数据的检测**

    在 `backend=local` 模式下，数据导入完成之前 TiDB Lightning 会输出冲突数据，然后从数据库中删除这些冲突数据。用户可以在导入完成后解析冲突数据，并根据业务规则选择适合的数据进行插入。建议根据冲突数据清洗上游数据源，避免在后续增量数据迁移阶段遇到冲突数据而造成数据不一致。

- **在 TiDB Data Migration (DM) 中 优化 relay log 的使用方式**

    - 恢复 `source` 配置中 `enable-relay` 开关
    - 增加 `start-relay` 或 `stop-relay` 命令中动态开启或关闭 relay log 的功能
    - relay log 的开启状态与 `source` 绑定，source 迁移到任意 DM-worker 均保持原有开启或关闭状态
    - relay log 的存放路径移至 DM-worker 配置文件

- **在 DM 中优化排序规则的处理方式**

    增加 `collation_compatible` 开关，支持 `strict` 和 `loose`（默认）两种模式。如果对排序规则要求不严格，允许排序规则不一致，使用默认的 `loose` 模式可使同步正常进行；如果对排序规则要求严格，排序规则不一致导致报错，则可以使用 `strict` 模式。

- **在 DM 中 优化 `transfer source`，支持平滑执行同步任务**

    当 DM-worker 所在各节点负载不均衡时，`transfer source` 命令可用于手动将某 `source` 配置迁移到其他节点。优化后的 `transfer source` 简化了用户操作步骤，不再要求先暂停所有关联 task 而是直接执行平滑迁移，DM 将在内部完成所需操作。

- **DM OpenAPI 特性 GA**

    DM 支持通过 API 的方式进行日常管理，包括增加数据源、管理任务等。本次更新 OpenAPI 从实验特性转为正式特性。


- **优化 TiCDC 对集群的影响**

    大幅降低了 TiCDC 启用后，对 TiDB 集群的性能影响。在实验室环境中，TiCDC 对 TiDB 的性能影响可以降低到 5% 以下。

### 问题诊断效率

- **功能 10**

    <功能描述 （功能是什么 + 能给用户带来什么好处 + 需要用户注意什么）>

    <功能支持情况，告诉用户 TiDB 默认开始还是关闭此功能，如果默认关闭，如何开启>

    <如果功能限制或此功能特定的兼容性问题，需要提及>

    [用户文档](/)

- **Top SQL（实验特性）**

    新推出实验性特性 Top SQL（默认关闭），帮助用户轻松找到节点中负载贡献较大的查询。

    [用户文档](/dashboard/top-sql.md)

### TiDB 数据共享订阅

- **功能 11**

    <功能描述 （功能是什么 + 能给用户带来什么好处 + 需要用户注意什么）>

    <功能支持情况，告诉用户 TiDB 默认开始还是关闭此功能，如果默认关闭，如何开启>

    <如果功能限制或此功能特定的兼容性问题，需要提及>

    [用户文档](/)


### 部署及运维

- **功能 12**

    <功能描述 （功能是什么 + 能给用户带来什么好处 + 需要用户注意什么）>

    <功能支持情况，告诉用户 TiDB 默认开始还是关闭此功能，如果默认关闭，如何开启>

    <如果功能限制或此功能特定的兼容性问题，需要提及>

    [用户文档](/)

- **持续性能分析（实验特性）**

    - 支持更多组件：支持 TiFlash 组件查看 CPU Profiling
    - 支持更方便的查看形式：支持以火焰图形式查看 CPU Profiling 和 Goroutine 结果。
    - 支持更多部署环境：支持在 TiDB Operator 部署环境下启用持续性能分析功能。

    该功能默认关闭，需进入 TiDB Dashboard 持续性能分析页面开启，开启方法见[用户文档](/dashboard/continuous-profiling.md)。

    要使用持续性能分析功能，集群须由 TiUP v1.9.0 及以上版本或 TiDB Operator vx.x.x（TBD）及以上版本升级或安装。

## 遥测

- **功能 13**

    <功能描述 （功能是什么 + 能给用户带来什么好处 + 需要用户注意什么）>

    <功能支持情况，告诉用户 TiDB 默认开始还是关闭此功能，如果默认关闭，如何开启>

    <如果功能限制或此功能特定的兼容性问题，需要提及>

    [用户文档](/)

## 提升改进

+ TiDB

    - 新增系统变量 `tidb_enable_paging`，开启该功能可显著降低使用 `IndexLookUp` 和 `Limit` 并且 `Limit` 数据较小且无法下推到 `IndexScan` 上的读请求的延迟 [#30578](https://github.com/pingcap/tidb/issues/30578)


## Bug 修复


