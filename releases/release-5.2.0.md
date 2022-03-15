---
title: TiDB 5.2 Release Notes
---

# TiDB 5.2 Release Notes

发版日期：2021 年 8 月 27 日

TiDB 版本：5.2.0

> **警告：**
>
> 该版本存在一些已知问题，已在新版本中修复，建议使用 5.2.x 的最新版本。

在 5.2 版本中，你可以获得以下关键特性：

- 支持基于部分函数创建表达式索引 (Expression index)，极大提升查询的性能。
- 提升优化器的估算准确度 (Cardinality Estimation)，有助于选中最优的执行计划。
- 锁视图 (Lock View) 成为 GA 特性，提供更直观方便的方式观察事务加锁情况以及排查死锁问题。
- 新增 TiFlash I/O 限流功能，提升 TiFlash 读写稳定性。
- 为 TiKV 引入新的流控机制代替之前的 RocksDB write stall 流控机制，提升 TiKV 流控稳定性。
- 简化 Data Migration (DM) 工具运维，降低运维管理的成本。
- TiCDC 支持 HTTP 协议 OpenAPI 对 TiCDC 任务进行管理，在 Kubernetes 以及 On-Premises 环境下提供更友好的运维方式。(实验特性)

## 兼容性更改

> **注意：**
>
> 当从一个早期的 TiDB 版本升级到 TiDB 5.2 时，如需了解所有中间版本对应的兼容性更改说明，请查看对应版本的 [Release Note](/releases/release-notes.md)。

### 系统变量

|  变量名    |  修改类型    |  描述    |
| :---------- | :----------- | :----------- |
| [`default_authentication_plugin`](/system-variables.md#default_authentication_plugin) | 新增 | 设置服务器对外通告的默认身份验证方式，默认值为 `mysql_native_password`。 |
| [`tidb_enable_auto_increment_in_generated`](/system-variables.md#tidb_enable_auto_increment_in_generated) | 新增 | 控制是否允许在创建生成列或者表达式索引时引用自增列，默认值为`OFF`。 |
| [`tidb_opt_enable_correlation_adjustment`](/system-variables.md#tidb_opt_enable_correlation_adjustment) | 新增 | 控制优化器是否开启交叉估算，默认值为`ON`。 |
| [`tidb_opt_limit_push_down_threshold`](/system-variables.md#tidb_opt_limit_push_down_threshold) | 新增 | 设置将 Limit 和 TopN 算子下推到 TiKV 的阈值，默认值为`100`。 |
| [`tidb_stmt_summary_max_stmt_count`](/system-variables.md#tidb_stmt_summary_max_stmt_count-从-v40-版本开始引入) | 修改 | 表示 statement summary 在内存中保存的语句的最大数量。默认值从 `200` 修改为 `3000`。 |
| `tidb_enable_streaming` | 废弃 | 系统变量 `enable-streaming`已废弃，不建议再使用。 |

### 配置文件参数

|  配置文件    |  配置项    |  修改类型    |  描述    |
| :---------- | :----------- | :----------- | :----------- |
| TiDB 配置文件 | [`pessimistic-txn.deadlock-history-collect-retryable`](/tidb-configuration-file.md#deadlock-history-collect-retryable) | 新增 | 控制 [`INFORMATION\_SCHEMA.DEADLOCKS`](/information-schema/information-schema-deadlocks.md) 表中是否收集可重试的死锁错误信息。 |
| TiDB 配置文件 | [`security.auto-tls`](/tidb-configuration-file.md#auto-tls) | 新增 | 控制 TiDB 启动时是否自动生成 TLS 证书，默认值为 `false`。 |
| TiDB 配置文件 | [`stmt-summary.max-stmt-count`](/tidb-configuration-file.md#max-stmt-count) | 修改 | 表示 statement summary tables 中保存的 SQL 种类的最大数量。默认值从 `200` 修改为 `3000`。 |
| TiDB 配置文件 | `experimental.allow-expression-index`  | 废弃 | 废弃 TiDB 配置文件中`allow-expression-index` 配置项 |
| TiKV 配置文件 | [`raftstore.cmd-batch`](/tikv-configuration-file.md#cmd-batch)  | 新增 | 对请求进行攒批的控制开关，开启后可显著提升写入性能。默认值为 `true`。 |
| TiKV 配置文件 | [`raftstore.inspect-interval`](/tikv-configuration-file.md#inspect-interval)  | 新增 | TiKV 每隔一段时间会检测 Raftstore 组件的延迟情况，该配置项设置检测的时间间隔。当检测的延迟超过该时间，该检测会被记为超时。默认值为 `500ms`。|
| TiKV 配置文件 | [`raftstore.max-peer-down-duration`](/tikv-configuration-file.md#max-peer-down-duration)  | 修改 | 表示副本允许的最长未响应时间，超过将被标记为 `down`，后续 PD 会尝试将其删掉。默认值从 `5m` 修改为 `10m`。 |
| TiKV 配置文件 | [`server.raft-client-queue-size`](/tikv-configuration-file.md#raft-client-queue-size)  | 新增 | 指定 TiKV 中发送 Raft 消息的缓冲区大小。默认值为 8192。 |
| TiKV 配置文件 | [`storage.flow-control.enable`](/tikv-configuration-file.md#enable)  | 新增 | 表示是否开启 TiKV 流量控制机制。默认值为 `true`。 |
| TiKV 配置文件 | [`storage.flow-control.memtables-threshold`](/tikv-configuration-file.md#memtables-threshold)  | 新增 | 当 KvDB 的 memtable 的个数达到该阈值时，流控机制开始工作。默认值为 5。 |
| TiKV 配置文件 | [`storage.flow-control.l0-files-threshold`](/tikv-configuration-file.md#l0-files-threshold)  | 新增 | 当 KvDB 的 L0 文件个数达到该阈值时，流控机制开始工作。默认值为 9。 | 
| TiKV 配置文件 | [`storage.flow-control.soft-pending-compaction-bytes-limit`](/tikv-configuration-file.md#soft-pending-compaction-bytes-limit)  | 新增 | 当 KvDB 的 pending compaction bytes 达到该阈值时，流控机制开始拒绝部分写入请求并报错。默认值为 "192GB"。 |
| TiKV 配置文件 | [`storage.flow-control.hard-pending-compaction-bytes-limit`](/tikv-configuration-file.md#hard-pending-compaction-bytes-limit)  | 新增 | 当 KvDB 的 pending compaction bytes 达到该阈值时，流控机制开始拒绝所有写入请求并报错。默认值为 "1024GB"。 |

### 其他

- 升级前，请检查系统变量 [`tidb_evolve_plan_baselines`](/system-variables.md#tidb_evolve_plan_baselines-从-v40-版本开始引入) 的值是否为 `ON`。如果为 `ON`，需要将其改成 `OFF`，否则会导致升级失败。
- v4.0 集群升级到 v5.2 集群后，[`tidb_multi_statement_mode`](/system-variables.md#tidb_multi_statement_mode-从-v4011-版本开始引入) 变量的默认值由 `WARN` 变为 `OFF`。
- 升级前，请检查 TiDB 配置项 [`feedback-probability`](/tidb-configuration-file.md#feedback-probability) 的值。如果不为 0，升级后会触发 "panic in the recoverable goroutine" 报错，但不影响升级。
- 兼容 MySQL 5.7 的 noop 变量 `innodb_default_row_format`，配置此变量无实际效果 [#23541](https://github.com/pingcap/tidb/issues/23541)。

- 从 TiDB 5.2 起，为了提高系统安全性，建议（但不要求）对来自客户端的连接进行传输层加密，TiDB 提供 Auto TLS 功能在 TiDB 服务器端自动配置并开启加密。要使用 Auto TLS 功能，请在 TiDB 升级前将 TiDB 配置文件中的 [`security.auto-tls`](/tidb-configuration-file.md#auto-tls) 设置为 `true`。

- 支持 `caching_sha2_password` 身份验证方式，简化了从 MySQL 8.0 的迁移操作，并提升了安全性。

## 新功能

### SQL

- **支持基于部分函数创建表达式索引 (Expression index)**

    表达式索引是一种特殊的索引，能将索引建立于表达式上。创建了表达式索引后，TiDB 支持基于表达式的查询，极大提升查询的性能。

    [用户文档](/sql-statements/sql-statement-create-index.md)，[#25150](https://github.com/pingcap/tidb/issues/25150)

- **支持 Oracle 中的 `translate`函数**

    `translate` 函数可以将字符串中出现的所有指定字符替换为其它字符， TiDB 中的 `translate` 函数不会像 Oracle 一样将空字符串视为`NULL`。

    [用户文档](/functions-and-operators/string-functions.md)

- **支持 Spilling HashAgg**

    支持 HashAgg 的落盘。当包含 HashAgg 算子的 SQL 语句引起 OOM 时，可以尝试设置算子的并发度为 1 来触发落盘，缓解 TiDB 内存压力。

    [用户文档](/configure-memory-usage.md#tidb-server-其它内存控制策略)，[#25882](https://github.com/pingcap/tidb/issues/25882)

- **提升优化器的估算准确度 (Cardinality Estimation)**

    - 提升 TiDB 对 TopN/Limit 估算的准确度。例如，对于包含 `order by col limit x` 的大表分页查询，TiDB 可以更容易地选对索引，降低查询响应时间。
    - 提升对越界估算的准确度。例如，在当天统计信息尚未更新的情况下，对于包含 `where date=Now()` 的查询，TiDB 也能准确地选中对应索引。
    - 引入变量 `tidb_opt_limit_push_down_threshold` 控制优化器对 Limit/TopN 的下推行为，可以解决部分情况下因为估算误差导致 Limit/TopN 不能下推的问题。

    [用户文档](/system-variables.md#tidb_opt_limit_push_down_threshold)，[#26085](https://github.com/pingcap/tidb/issues/26085)

- **提升优化器的索引过滤规则 (Index Selection)**

    新增加了一些索引选择的裁剪规则，在通过统计信息进行对比之前，通过规则进一步对可能的选择的索引范围进行缩小。从而减小各种情况下选到不优索引的概率。

    [用户文档](/choose-index.md)

### 事务

- **锁视图 (Lock View) 成为 GA 特性**

    Lock View 用于提供关于悲观锁的锁冲突和锁等待的更多信息，方便 DBA 通过锁视图功能来观察事务加锁情况以及排查死锁问题等。

    在 5.2 中，Lock View 新增以下特性：

    - 对于 Lock View 所属的各张表中的 SQL Digest 列， v5.2 额外增加了一列显示对应的归一化的 SQL 语句文本，无需手动查询 SQL Digest 对应的语句。
    - 增加了 `TIDB_DECODE_SQL_DIGESTS` 函数用于在集群中查询一组 SQL Digest 所对应的 SQL 语句的归一化形式（即去除格式和参数后的形式），简化了查询某一事务历史执行过的语句的操作
    - 在 `DATA_LOCK_WAITS` 和 `DEADLOCKS` 系统表中，增加一列显示 key 中解出的表名、row id、索引值等信息，简化了定位 key 所属的表、解读 key 的内容等信息的操作。
    - 支持在 `DEADLOCKS` 表中收集可重试的死锁错误的信息，以便于排查因可重试的死锁引发的问题。默认不收集，可通过配置选项 `pessimistic-txn.deadlock-history-collect-retryable` 启用 。
    - `TIDB_TRX` 系统表支持区分正在执行查询的事务和闲置中的事务，即将原来的 `Normal` 状态拆分成 `Running` 和 `Idle` 状态。

    用户文档：

    - 查看集群中所有 TiKV 节点上当前正在发生的悲观锁等锁：[`DATA_LOCK_WAITS`](/information-schema/information-schema-data-lock-waits.md)
    - 查看 TiDB 节点上最近发生的若干次死锁错误：[`DEADLOCKS`](/information-schema/information-schema-deadlocks.md)
    - 查看 TiDB 节点上正在执行的事务的信息：[`TIDB_TRX`](/information-schema/information-schema-tidb-trx.md)

- 对带有 `AUTO_RANDOM` 或者 `SHARD_ROW_ID_BITS` 属性的表，优化其大部分添加索引操作的场景。

### 稳定性

- **新增 TiFlash I/O 限流功能**

    TiFlash I/O 限流功能主要针对磁盘带宽较小且明确知道磁盘带宽大小的云盘场景，默认关闭。

    TiFlash I/O Rate Limiter 提供了一个新的防止“读/写”任务之间过度竞争系统 IO 资源的机制，可以平衡系统对“读”和“写”任务的响应，并且可以根据读/写负载的情况自动限速。

    [用户文档](/tiflash/tiflash-configuration.md)

- **提升 TiKV 流控稳定性**

    TiKV 引入了新的流控机制代替之前的 RocksDB write stall 流控机制。相比于 write stall 机制，新的流控机制通过以下改进减少了流控对前台写入稳定性的影响：

    - 当 RocksDB compaction 压力堆积时，通过在 TiKV scheduler 层进行流控而不是在 RocksDB 层进行流控，避免 RocksDB write stall 造成的 raftstore 卡顿并造成 Raft 选举超时导致发生节点 leader 迁移的问题。
    - 改善流控算法，有效降低大写入压力下导致 QPS 下降的问题

    [用户文档](/tikv-configuration-file.md#storageflow-control)， [#10137](https://github.com/tikv/tikv/issues/10137)

- **自动检测并恢复集群中单个 TiKV 变慢带来的影响**

    在 TiKV 中引入了慢节点检测机制，通过检测 TiKV Raftstore 的快慢来计算出一个分数，并通过 Store Heartbeat 上报给 PD。并且在 PD 上增加了 `evict-slow-store-scheduler` 调度器，能够自动驱逐单个变慢的 TiKV 节点上的 Leader，以降低其对整个集群性能的影响。同时，还增加了慢节点相关的报警项，帮助用户快速发现并处理问题。

    [用户文档](/tikv-configuration-file.md#inspect-interval)，[#10539](https://github.com/tikv/tikv/issues/10539)

### 数据迁移

- **简化 Data Migration (DM) 工具运维**

    DM v2.0.6 支持自动识别使用 VIP 的数据源实例切换事件（failover/计划切换），自动连接上新的数据源实例，减少数据复制的延迟和减少运维操作步骤

- TiDB Lightning 支持自定义 CSV 数据的终止符，兼容 MySQL LOAD DATA CSV 数据格式 。使得 TiDB Lightning 可以直接使用在用户数据流转架构体系中。[#1297](https://github.com/pingcap/br/pull/1297)

### TiDB 数据共享订阅

TiCDC 支持 HTTP 协议 OpenAPI 对 TiCDC 任务进行管理，在 Kubernetes 以及 On-Premises 环境下提供更友好的运维方式。(实验特性）

[#2411](https://github.com/pingcap/tiflow/issues/2411)

### 部署及运维

支持在使用 Apple M1 芯片的本地 Mac 机器上使用 `tiup playground` 命令。

## 功能增强

+ Tools

    + TiCDC

        - 新增专为 TiDB 设计的比基于 JSON 的开放协议更紧凑的二进制 MQ 格式 [#1621](https://github.com/pingcap/tiflow/pull/1621)
        - 移除对 file sorter 的支持 [#2114](https://github.com/pingcap/tiflow/pull/2114)
        - 支持日志轮替配置 [#2182](https://github.com/pingcap/tiflow/pull/2182)

    + TiDB Lightning

        - 支持 CSV 文件中除 `\r` 和 `\n` 之外的自定义行尾 [#1297](https://github.com/pingcap/br/pull/1297)
        - 支持表达式索引和依赖于虚拟生成列的索引 [#1407](https://github.com/pingcap/br/pull/1407)

    + Dumpling
        - 支持备份兼容 MySQL 但不支持 `START TRANSACTION ... WITH CONSISTENT SNAPSHOT` 和 `SHOW CREATE TABLE` 语句的数据库 [#311](https://github.com/pingcap/dumpling/pull/311)

## 提升改进

+ TiDB

    - 支持将内置函数 `json_unquote()` 下推到 TiKV [#24415](https://github.com/pingcap/tidb/issues/24415)
    - 支持在 Dual 表上移除 `Union` 算子的优化 [#25614](https://github.com/pingcap/tidb/pull/25614)
    - 优化聚合算子的代价常数 [#25241](https://github.com/pingcap/tidb/pull/25241)
    - 允许 MPP outer join 根据表行数选择构建表 [#25142](https://github.com/pingcap/tidb/pull/25142)
    - 支持 MPP 查询任务按 Region 均衡到不同 TiFlash 节点上 [#24724](https://github.com/pingcap/tidb/pull/24724)
    - 支持执行 MPP 查询后将缓存中过时的 Region 无效化 [#24432](https://github.com/pingcap/tidb/pull/24432)
    - 提升内置函数 `str_to_date` 在格式指定器中 `%b/%M/%r/%T` 的 MySQL 兼容性 [#25767](https://github.com/pingcap/tidb/pull/25767)
    - 修复因对同一条查询重复创建不同 binding 可能导致的多个 TiDB 上 binding cache 不一致的问题 [#26015](https://github.com/pingcap/tidb/pull/26015)
    - 修复升级可能会导致的 binding 无法被加载到缓存的问题 [#23295](https://github.com/pingcap/tidb/pull/23295)
    - 对 `SHOW BINDINGS` 结果按照 (original_sql, update_time) 有序输出 [#26139](https://github.com/pingcap/tidb/pull/26139)
    - 改进使用 binding 优化查询的逻辑，减少对查询的优化次数 [#26141](https://github.com/pingcap/tidb/pull/26141)
    - 支持标记为删除状态的 binding 进行自动垃圾回收 [#26206](https://github.com/pingcap/tidb/pull/26206)
    - 在 `EXPLAIN VERBOSE` 的结果中显示查询优化是否使用了某个 binding [#26930](https://github.com/pingcap/tidb/pull/26930)
    - 增加新的状态变量 `last_plan_binding_update_time` 用于查看当前 TiDB 实例中 binding cache 对应的时间戳 [#26340](https://github.com/pingcap/tidb/pull/26340)
    - 在打开 binding 演进或者执行 `admin evolve bindings` 时提供报错，避免自动演进绑定（目前为试验特性，已在当前 TiDB 版本关闭）影响到其他功能 [#26333](https://github.com/pingcap/tidb/pull/26333)

+ PD

    - 热点调度增加对 QPS 维度的支持，同时支持调整维度的优先级顺序[#3869](https://github.com/tikv/pd/issues/3869)
    - 热点调度支持对 TiFlash 的写热点进行调度 [#3900](https://github.com/tikv/pd/pull/3900)

+ TiFlash

    - 新增若干运算符的支持：`MOD / %`, `LIKE`
    - 新增若干字符串函数的支持：`ASCII()`, `COALESCE()`, `LENGTH()`, `POSITION()`, `TRIM()`
    - 新增若干数学函数的支持：`CONV()`, `CRC32()`, `DEGREES()`, `EXP()`, `LN()`, `LOG()`, `LOG10()`, `LOG2()`, `POW()`, `RADIANS()`, `ROUND(decimal)`, `SIN()`, `MOD()`
    - 新增若干日期函数的支持： `ADDDATE(string, real)`, `DATE_ADD(string, real)`, `DATE()`
    - 新增更多的函数支持：`INET_NTOA()`, `INET_ATON()`, `INET6_ATON`, `INET6_NTOA()`
    - 当 new collation 打开时，支持 MPP 模式下的 Shuffled Hash Join 和 Shuffled Hash Aggregation 运算
    - 优化基础代码提升 MPP 性能
    - 支持将 `STRING` 类型转换为 `DOUBLE` 类型
    - 通过多线程优化右外连接中的非连接数据
    - 支持在 MPP 查询中自动清理过期的 Region 信息

+ Tools

    + TiCDC
        - 为 kv client 增量扫添加并发限制 [#1899](https://github.com/pingcap/tiflow/pull/1899)
        - 始终在 TiCDC 内部拉取 old value [#2271](https://github.com/pingcap/tiflow/pull/2271)
        - 当遇到不可恢复的 DML 错误，TiCDC 快速失败并退出 [#1928](https://github.com/pingcap/tiflow/pull/1928)
        - 在 Region 初始化后不立即执行 resolve lock [#2235](https://github.com/pingcap/tiflow/pull/2235)
        - 优化 workerpool 以降低在高并发情况下 goroutine 的数量 [#2201](https://github.com/pingcap/tiflow/pull/2201)

    + Dumpling
        - 通过 `tidb_rowid` 对 TiDB v3.x 的表进行数据划分以节省 TiDB 的内存 [#301](https://github.com/pingcap/dumpling/pull/301)
        - 减少 Dumpling 对 `information_schema` 库的访问以提高稳定性 [#305](https://github.com/pingcap/dumpling/pull/305)

## Bug 修复

+ TiDB

    - 修复在 `SET` 类型列上 Merge Join 结果不正确的问题 [#25669](https://github.com/pingcap/tidb/issues/25669)
    - 修复 `IN` 表达式参数的数据腐蚀问题 [#25591](https://github.com/pingcap/tidb/issues/25591)
    - 避免 GC 的 session 受全局变量的影响 [#24976](https://github.com/pingcap/tidb/issues/24976)
    - 修复了在窗口函数查询中使用 `Limit` 时出现 panic 问题 [#25344](https://github.com/pingcap/tidb/issues/25344)
    - 修复查询分区表时使用 `Limit` 返回错误值的问题 [#24636](https://github.com/pingcap/tidb/issues/24636)
    - 修复了 `IFNULL` 在 `ENUM` 或 `SET` 类型上不能正确生效的问题 [#24944](https://github.com/pingcap/tidb/issues/24944)
    - 修复了 Join 子查询中的 `count` 被改写为 `first_row` 导致结果不正确的问题 [#24865](https://github.com/pingcap/tidb/issues/24865)
    - 修复了 `TopN` 算子下使用 `ParallelApply` 查询时卡住的问题 [#24930](https://github.com/pingcap/tidb/issues/24930)
    - 修复了使用含有多列的前缀索引查询时出现多余结果的问题 [#24356](https://github.com/pingcap/tidb/issues/24356)
    - 修复了操作符 `<=>` 不能正确生效的问题 [#24477](https://github.com/pingcap/tidb/issues/24477)
    - 修复并行 `Apply` 算子的数据竞争问题 [#23280](https://github.com/pingcap/tidb/issues/23280)
    - 修复对 PartitionUnion 算子的 IndexMerge 结果排序时出现 `index out of range` 错误 [#23919](https://github.com/pingcap/tidb/issues/23919)
    - 修复 `tidb_snapshot` 被允许设置为非预期的过大值，而可能造成事务隔离性被破坏的问题 [#25680]( https://github.com/pingcap/tidb/issues/25680)
    - 修复 ODBC 类常数（例如 `{d '2020-01-01'}`）不能被用作表达式的问题 [#25531](https://github.com/pingcap/tidb/issues/25531)
    - 修复 `SELECT DISTINCT` 被转化为 Batch Get 而导致结果不正确的问题 [#25320](https://github.com/pingcap/tidb/issues/25320)
    - 修复无法触发将查询从 TiFlash 回退到 TiKV 的问题 [#23665](https://github.com/pingcap/tidb/issues/23665) [#24421](https://github.com/pingcap/tidb/issues/24421)
    - 修复在检查 `only_full_group_by` 时的 `index-out-of-range` 错误 [#23839](https://github.com/pingcap/tidb/issues/23839)
    - 修复关联子查询中 Index Join 的结果不正确问题 [#25799](https://github.com/pingcap/tidb/issues/25799)

+ TiKV

    - 修复错误的 `tikv_raftstore_hibernated_peer_state` 监控指标 [#10330](https://github.com/tikv/tikv/issues/10330)
    - 修复 coprocessor 中 `json_unquote()` 函数错误的参数类型 [#10176](https://github.com/tikv/tikv/issues/10176)
    - 正常关机时跳过清理 Raftstore 的回调从而避免在某些情况下破坏事务的 ACID [#10353](https://github.com/tikv/tikv/issues/10353) [#10307](https://github.com/tikv/tikv/issues/10307)
    - 修复在 Leader 上 Replica Read 共享 Read Index 的问题 [#10347](https://github.com/tikv/tikv/issues/10347)
    - 修复 coprocessor 转换 `DOUBLE` 到 `DOUBLE` 的错误函数 [#25200](https://github.com/pingcap/tidb/issues/25200)

+ PD

    - 修复多个调度器之间存在调度冲突时无法产生预期调度的问题 [#3807](https://github.com/tikv/pd/issues/3807) [#3778](https://github.com/tikv/pd/issues/3778)

+ TiFlash

    - 修复因 split 失败而不断重启的问题
    - 修复无法删除 Delta 历史数据的潜在问题
    - 修复在 `CAST` 函数中为非二进制字符串填充错误数据的问题
    - 修复处理包含复杂 `GROUP BY` 列的聚合查询时结果不正确的问题
    - 修复写入压力过大时出现进程崩溃的问题
    - 修复右连接键不为空且左连接键可为空时进程崩溃的问题
    - 修复 `read-index` 请求耗时长的潜在问题
    - 修复读负载高的情况下进程崩溃的问题
    - 修复 `Date_Format` 函数在参数类型为 `STRING` 且包含 `NULL` 值时可能导致 TiFlash server 崩溃的问题

+ Tools

    + TiCDC

        - 修复 TiCDC owner 在刷新 checkpoint 时异常退出的问题 [#1902](https://github.com/pingcap/tiflow/issues/1902)
        - 修复 changefeed 创建成功后立即失败的问题 [#2113](https://github.com/pingcap/tiflow/issues/2113)
        - 修复不合法格式的 rules filter 导致 changefeed 失败的问题 [#1625](https://github.com/pingcap/tiflow/issues/1625)
        - 修复 TiCDC Owner 崩溃时潜在的 DDL 丢失问题 [#1260](https://github.com/pingcap/tiflow/issues/1260)
        - 修复 CLI 在默认的 sort-engine 选项上与 4.0.x 集群的兼容性问题 [#2373](https://github.com/pingcap/tiflow/issues/2373)
        - 修复 TiCDC 遇到 `ErrSchemaStorageTableMiss` 错误时可能导致 changefeed 被意外重置的问题 [#2422](https://github.com/pingcap/tiflow/issues/2422)
        - 修复 TiCDC 遇到 `ErrGCTTLExceeded` 错误时 changefeed 不能被 remove 的问题 [#2391](https://github.com/pingcap/tiflow/issues/2391)
        - 修复 TiCDC 同步大表到 cdclog 失败的问题 [#1259](https://github.com/pingcap/tiflow/issues/1259) [#2424](https://github.com/pingcap/tiflow/issues/2424)
        - 修复 TiCDC 在重新调度 table 时多个 processors 可能向同一个 table 写数据的问题 [#2230](https://github.com/pingcap/tiflow/issues/2230)

    + Backup & Restore (BR)

        - 修复 BR 恢复中忽略了所有系统表的问题 [#1197](https://github.com/pingcap/br/issues/1197) [#1201](https://github.com/pingcap/br/issues/1201)
        - 修复 BR 恢复 cdclog 时漏掉 DDL 操作的问题 [#870](https://github.com/pingcap/br/issues/870)

    + TiDB Lightning

        - 修复 TiDB Lightning 解析 Parquet 文件中 `DECIMAL` 类型数据失败的问题 [#1272](https://github.com/pingcap/br/pull/1272)
        - 修复 TiDB Lightning 恢复 table schema 时报错 "Error 9007: Write conflict" 的问题 [#1290](https://github.com/pingcap/br/issues/1290)
        - 修复 TiDB Lightning 因 int handle 溢出导致导入数据失败的问题 [#1291](https://github.com/pingcap/br/issues/1291)
        - 修复 TiDB Lightning 在 local backend 模式下因数据丢失可能遇到 checksum 不匹配的问题 [#1403](https://github.com/pingcap/br/issues/1403)
        - 修复 TiDB Lightning 恢复 table schema 时与 clustered index 不兼容的问题 [#1362](https://github.com/pingcap/br/issues/1362)

    + Dumpling

        - 修复 Dumpling GC safepoint 设置过晚导致数据导出失败的问题 [#290](https://github.com/pingcap/dumpling/pull/290)
        - 修复 Dumpling 在特定 MySQL 版本下获取上游表名时卡住的问题 [#322](https://github.com/pingcap/dumpling/issues/322)
