---
title: TiDB 6.3.0 Release Notes
---

# TiDB v6.3.0 Release Notes

发版日期：2022 年 x 月 xx 日

TiDB 版本：6.3.0-DMR

在 6.3.0-DMR 版本中，你可以获得以下关键特性：

- TiKV/TiFlash 静态加密支持国密算法 SM4
- TiDB 支持基于国密算法 SM3 插件的身份验证
- SQL语句CREATE USER / ALTER USER支持ACCOUNT LOCK/UNLOCK 选项
- JSON 数据类型和 JSON 函数 GA
- TiDB 支持 Null Aware Anti Join
- 提供“执行时间”的细粒度指标
- 分区表新增简化 Range 分区的语法糖衣，避免在 DDL 中枚举所有分区
- Range Columns 分区方式在 PARTITION BY RANGE COLUMNS (column_list) 处支持定义多列

## 新功能

### SQL

* 新增简化 Range 分区定义的语法糖衣

    新的定义 Range 分区的方式，不需要枚举所有分区，可大幅度缩短现有 Range 分区表定义语句冗长的书写方式，语义与原有 Range 分区等价。

    [用户文档]() [#issue]() @[mjonss](https://github.com/mjonss)

* Range Columns 分区方式支持定义多列

    PARTITION BY RANGE COLUMNS (column_list)处，`column_list` 不再限定为单一列，基本功能与 MySQL 等同。

    [用户文档]() [#issue]() @[mjonss](https://github.com/mjonss)

* 分区表 EXCHANGE PARTITION 功能 GA

    EXCHANGE PARTITION 功能通过性能和稳定性提升，由实验功能转为正式功能。

    [用户文档]() [#35996](https://github.com/pingcap/tidb/issues/35996) @[ymkzpx](https://github.com/ymkzpx)

* 增加支持以下窗口分析函数：

    * `LEAD()`
    * `LAG()`

  [用户文档](/tiflash/tiflash-supported-pushdown-calculations.md)，[#5579](https://github.com/pingcap/tiflash/issues/5579) @[SeaRise](https://github.com/SeaRise)

* CREATE USER 支持 ACCOUNT LOCK/UNLOCK 选项

    在执行CREATE USER创建用户时，允许使用ACCOUNT LOCK / UNLOCK 选项，限定被创建的用户是否被锁定。锁定后的用户不能正常登录数据库。

    [用户文档]( / sql-statements/sql-statement-create-user.md),[#37051](https://github.com/pingcap/tidb/issues/37051) @[CbcWestwolf](https://github.com/CbcWestwolf)

* ALTER USER 支持 ACCOUNT LOCK/UNLOCK 选项

    对于已存在的用户，可以通过ALTER USER 使用 ACCOUNT LOCK / UNLOCK 选项，修改用户的锁定状态。

    [用户文档]( /sql-statements/sql-statement-alter-user.md),[#37051](https://github.com/pingcap/tidb/issues/37051) @[CbcWestwolf](https://github.com/CbcWestwolf)

* JSON 数据类型和 JSON 函数 GA

    JSON 是一种流行的数据格式，被大量的程序设计所采用。TiDB 在早期版本就引入了 JSON 支持， 兼容 MySQL 的 JSON 数据类型 和一部分 JSON 函数。在 v6.3.0 版本中，我们正式将这些功能 GA ，用户可以安全地在生产环境中使用 JSON 相关的功能。 JSON 功能的 GA，为 TiDB 提供了更丰富的数据类型支持，同时也进一步提升的 TiDB 对 MySQL 的兼容能力。

    [用户文档](/data-type-json.md) [#36993](https://github.com/pingcap/tidb/issues/36993) @[xiongjiwei](https://github.com/xiongjiwei)

* 提供轻量级元数据锁提升 DDL 变更过程 DML 的成功率

    TiDB 采用 F1 论文中的在线异步变更算法实现 DDL 变更：事务在执行时会获取开始时对应的元数据快照，如果事务执行过程中相关表上发生了元数据的更改，为了保证数据的一致性，TiDB 会返回 `Information schema is changed` 的异常，导致用户事务提交失败。为了解决这个问题，在 v6.3.0 版本中，TiDB 在 Online DDL 算法中引入了元数据锁特性，通过协调表元数据变更过程中 DML 语句和 DDL 语句的优先级，让执行中的 DDL 语句等待持有旧版本元数据的 DML 语句提交，尽可能避免 DML 语句报错。

    [用户文档](/metadata-lock.md) [#37275](https://github.com/pingcap/tidb/issues/37275) @[wjhuang2016](https://github.com/wjhuang2016)

* 提升添加索引的性能并减少对 DML 事务的影响

    开启该特性后，TiDB 预期提升添加索引性能为原来的 3 倍。

    [用户文档](/system-variables.md#tidb_ddl_enable_fast_reorg-从-v630-版本开始引入) [#35983](https://github.com/pingcap/tidb/issues/35983) @[benjamin2037](https://github.com/benjamin2037)

* TiDB 支持更多正则表达式

    TiDB 新增支持 `REGEXP_SUBSTR`、`REGEXP_REPLACE`、`REGEXP_LIKE` 和 `REGEXP_INSTR` 4 个正则表达式函数，支持基于模式的模糊查询和正则替换等操作。

    [用户文档](/functions-and-operators/string-functions.md#支持的函数) [#](https://github.com/pingcap/tidb/issues/) @[windtalker](https://github.com/windtalker)

### 安全

* 静态加密 TiKV 支持国密算法SM4

    TiKV 静态加密中新增加密算法SM4，用户在配置静态加密时，支持配置 data-encryption-method 参数为 "sm4-ctr"，以启用基于国密算法SM4的静态加密能力。

    [用户文档](/encryption-at-rest.md) [#13041](https://github.com/tikv/tikv/issues/13041) @[jiayang-zheng](https://github.com/jiayang-zheng)

* 静态加密 TiFlash 支持国密算法SM4

    TiFlash 静态加密中新增加密算法SM4，用户在配置静态加密时，支持配置 data-encryption-method 参数为 "sm4-ctr"，以启用基于国密算法SM4的静态加密能力。

    [用户文档](/encryption-at-rest.md) [#5714](https://github.com/pingcap/tiflash/issues/5714) @[lidezhu](https://github.com/lidezhu)

* TiDB 支持国密算法 SM3 的身份验证

    TiDB 身份验证新增基于国密算法 SM3 的插件 “tidb_sm3_password”，启用此插件后，用户密码将通过SM3进行加密存储和验证。

    [用户文档](/system-variables.md) [#36192](https://github.com/pingcap/tidb/issues/36192) @[CbcWestwolf](https://github.com/CbcWestwolf)

* JDBC 支持国密算法 SM3 的身份验证

    用户密码的身份验证需要客户端的支持，现在 JDBC 支持国密算法 SM3 的能力，用户可以通过 JDBC 连接到 TiDB 使用国密算法 SM3 的身份验证能力。

    [用户文档]() []() @[lastincisor](https://github.com/lastincisor)

### 可观测性

* 提供“执行时间”的细粒度指标

    性能问题的诊断通常从时间入手。 对执行时间的细粒度观测能力，是衡量数据库可观测性的重要标准。 TiDB 在新版中正式提供了细化数据指标，用于对执行时间进行细化观测。 通过完整而又细分的指标数据，用户可以清晰的了解数据库的主要的时间消耗，进而快速发现关键问题，节省故障诊断的时间。 “执行时间”的细粒度观测能力，使得 TiDB 的观测性迈上了一个新的台阶。

    [用户文档](/latency-breakdown.md) [#34106](https://github.com/pingcap/tidb/issues/34106) @[cfzjywxk](https://github.com/cfzjywxk)

* 增强的 slow log 和 trace 语句

    在新版本中 TiDB 增强了 slow log 的内容和 trace 命令的输出。用户可以观测到 SQL 语句执行过程中，从 tidb parse 到 kv rocksdb 落盘全链路的延迟数据，进一步增强 TiDB 的诊断能力。

    [用户文档]() [#34487](https://github.com/pingcap/tidb/issues/34487) @[cfzjywxk](https://github.com/cfzjywxk)

* Dashboard 中显示死锁的历史记录

    新版本将死锁的历史记录加入到了 Dashboard 中。 当用户通过 Dashboard 的慢日志等手段发现某些 SQL 等待锁的时间较长的时候，Dashboard 上的死锁的历史记录有助于对问题的分析，提供了诊断的易用性。

     [用户文档]() [#issue]() @[cfzjywxk](https://github.com/cfzjywxk)

### 性能

* TiFlash 调整 FastScan 功能使用方式（实验特性）

    TiFlash 从 v6.2.0 版本开始引入的快速扫描功能 (FastScan)，性能上符合预期，但是使用方式上缺乏灵活性。因此，TiFlash 在 v6.3.0 版本调整 FastScan 功能的使用方式，停止使用对表设定是否开启 FastScan 功能的方式，改为使用系统变量 [`tiflash_fastscan`](/system-variables.md#tiflash_fastscan-从-v630-版本开始引入) 控制是否开启 FastScan 功能。

    从 v6.2.0 版本升级到 v6.3.0 版本时，在 v6.2.0 版本的所有 FastScan 设定将失效，需要重新使用变量方式进行 FastScan 设定，但不影响数据的正常读取。从更早版本升级到 v6.3.0 时，所有会话默认不开启 FastScan 功能，而是保持一致性的数据扫描功能。

    [用户文档](/develop/dev-guide-use-fastscan.md) [#5252](https://github.com/pingcap/tiflash/issues/5252) @[hongyunyan](https://github.com/hongyunyan)

* TiFlash 优化提升多并发场景下的数据扫描性能

    TiFlash 通过合并相同数据的读取操作，减少对于相同数据的重复读取，优化了多并发任务情况下的资源开销，提升多并发下的数据扫描性能。避免了以往在多并发任务下，如果涉及相同数据，同一份数据需要在每个任务中分别进行读取的情况，以及可能出现在同一时间内对相同数据进行多次读取的情况。

    该功能在 v6.2.0 版本以实验特性发布，并在 v6.3.0 版本作为正式功能发布。

    [用户文档](/tiflash/tiflash-configuration.md#配置文件-tiflashtoml) [#5376](https://github.com/pingcap/tiflash/issues/5376) @[JinheLin](https://github.com/JinheLin)

* TiFlash 副本同步性能优化

    TiFlash 使用 Raft 协议与 TiKV 进行副本数据同步。在 v6.3.0 版本之前，同步大量副本数据时往往需要比较长的时间。v6.3.0 版本优化了 TiFlash 副本同步机制，大幅度提升了副本同步速度。因此，使用 BR 恢复数据、使用 Lightning 导入数据，或全新增加 TiFlash 副本时，副本将更迅速地完成同步，用户可以更及时地使用 TiFlash 进行查询。此外，在 TiFlash 扩缩容或修改 TiFlash 副本数时，TiFlash 副本也将更快地达到安全、均衡的状态。

    [#5237](https://github.com/pingcap/tiflash/issues/5237) @[breezewish](https://github.com/breezewish)

* TiKV 日志循环使用

    TiKV Raft Engine 默认开启日志循环功能。该特性显著降低 Raft 日志追加过程中的长尾延迟，提升了 TiKV 写入负载下的性能。

    [用户文档](/tikv-configuration-file.md#enable-log-recycle-new-in-v630) [raft-engine#214](https://github.com/tikv/raft-engine/issues/214) @[LykxSassinator](https://github.com/LykxSassinator)

* TiDB 支持 Null Aware Anti Join

    TiDB 在新版本中引入了新的连接类型 Null Aware Anti Join (NAAJ)。 NAAJ 在集合操作时能够感知集合是否为空，或是否有空值，优化了一部分操作比如`IN`、`= ANY` 的执行效率，提升 SQL 性能。

    [用户文档](/explain-subqueries.md) [#issue]() @[Arenatlx](https://github.com/Arenatlx)

* 增加优化器 hint 控制哈希连接的驱动端

    在新版本中，优化器引入了两个新的 hint `HASH_JOIN_BUILD()` 和 `HASH_JOIN_PROBE()` 用来指定哈希连接，并指定其驱动端和被驱动端。 在没有选到最优执行计划的情况下，提供了更丰富的干预手段。

    [用户文档](/explain-subqueries.md) [#issue]() @[Reminiscent](https://github.com/Reminiscent)

### 事务

* 悲观事务可以延迟唯一性检查

    提供系统变量 `tidb_constraint_check_in_place_pessimistic` 来控制悲观事务中唯一约束检查的时间点。当变量设为 `ON` 时，TiDB 会把加锁操作和唯一约束检测推迟到必要的时候进行，以此提升批量DML操作的性能。

    [用户文档](/constraints.md#唯一约束) [#36579](https://github.com/pingcap/tidb/issues/36579) @[ekexium](https://github.com/ekexium)

* 优化 Read-Committed 隔离级别中对 TSO 的获取

    在 Read-Committed 隔离级别中， 引入新的系统变量控制语句对 TSO 的获取方式。 在 Plan Cache 命中的情况下，通过降低对 TSO 的获取频率提升批量 DML 的执行效率，降低跑批类任务的执行时间。

    [用户文档]() [#36812](https://github.com/pingcap/tidb/issues/36812) @[TonsnakeLin](https://github.com/TonsnakeLin)

### 稳定性

* TiKV 后台 IO 任务限制增强 (TiKV I/O Rate Limiter)

    改进算法，提供对磁盘读 I/O 的动态限流能力。

    [用户文档](/tikv-configuration-file.md#storageio-rate-limit) [#10867](https://github.com/tikv/tikv/issues/10867) @[tabokie](https://github.com/tabokie)

* 优化 `IN` 条件元素过多引发的大量内存消耗

    当 SQL 中的 `IN` 条件包含的元素过多时，TiDB在执行过程中可能会消耗大量的内存。 在新版中，TiDB 引入了新的内存控制机制对这类操作进行了优化，减少内存消耗，提升SQL执行效率和系统稳定性。

    [用户文档]() [#30755](https://github.com/pingcap/tidb/issues/30755) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes)

* 修改优化统计信息过期时的默认加载策略

    在 v5.3.0 版本时，TiDB 引入系统变量 `tidb_enable_pseudo_for_outdated_stats` 控制优化器过期的加载策略，默认为 `ON`，即保持旧版本行为不变：当 SQL 涉及的对象的统计信息过期时，优化器认为该表上除总行数以外的统计信息不再可靠，转而使用 pseudo 统计信息。 经过一系列测试和用户实际场景分析， TiDB 在新版本中将  `tidb_enable_pseudo_for_outdated_stats` 的默认值改为 `OFF`，即使统计信息过期，优化器也仍会使用该表上的统计信息，这有利于执行计划的稳定性。

    [用户文档]() [#issue]() @[xuyifangreeneyes](https://github.com/xuyifangreeneyes)

* TiKV Titan 关闭功能正式发布

    正式支持对在线 TiKV 节点关闭 Titan 引擎。

    [用户文档](/titan-configuration#disable-titan) [#issue]() @[tabokie](https://github.com/tabokie)

### 易用性

* 优化 TiFlash 数据同步进度的准确性

    TiDB 的 `information_schema.tiflash_replica` 表中的 `PROGRESS` 字段表示对应表 TiFlash 副本与 TiKV 数据的同步进度。在之前的版本中，`PROCESS` 字段只显示创建 TiFlash 副本过程中的数据同步进度。当 TiFlash 副本创建完毕，进行数据导入后，该值不会更新数据同步进度。

    v6.3.0 版本改进了 TiFlash 副本数据同步进度更新机制，在创建 TiFlash 副本后，进行数据导入等操作，TiFlash 副本需要和 TiKV 数据进行同步时，`information_schema.tiflash_replica` 表中的 `PROGRESS` 值将会更新，显示实际的数据同步进度。通过 TiFlash 数据同步进度的准确性优化，用户可以了解数据同步的实际进度，具有更好的使用体验。

    [用户文档](/information-schema/information-schema-tiflash-replica.md) [#4902](https://github.com/pingcap/tiflash/issues/4902) @[hehechen](https://github.com/hehechen)

### MySQL 兼容性

* 完善基于 SQL 的数据放置规则功能的兼容性

    TiDB 在 v6.0.0 版本提供基于 SQL 的数据放置规则功能，但是由于实现机制冲突，该功能和构建 TiFlash 副本功能不兼容。v6.3.0 版本进行改进优化，完善了这两个功能的兼容性。

    [用户文档](/placement-rules-in-sql.md#使用限制) [#37171](https://github.com/pingcap/tidb/issues/37171) @[lcwangchao](https://github.com/lcwangchao)

### 备份恢复

* PITR 支持 GCS 和 Azure Blob Storage 作为备份存储

    PITR 支持以 GCS 或 Azure Blob Storage 作为备份存储目标。部署在 GCP 或者 Azure 上的用户，升级 TiDB 集群到 v6.3.0 后，就可以使用 PITR 功能了。

    [用户文档](xxx) [#issue]() @[joccau](https://github.com/joccau)

### 数据迁移

* 功能标题

* TiDB Lightning 支持将 Apache Hive 导出的 Parquet 文件导入到 TiDB

    TiDB Lightning 支持将 Apache Hive 导出的 Parquet 文件导入到 TiDB ，从而实现 Hive 到 TiDB 之间的数据流转。

    [用户文档]() [#issue]() @[buchuitoudegou](https://github.com/buchuitoudegou)

* DM支持对同步到TiDB的表增加字段并对该字段赋值

    DM支持对同步到TiDB的表增加字段并对该字段赋值。在上游分库分表合并到下游TiDB的场景，可以用于区分目标表的记录是来自于上游那个分库分表。

    [用户文档]() [#3262](https://github.com/pingcap/tiflow/pull/3262), [#3340](https://github.com/pingcap/tiflow/issues/3340) @[yufan022](https://github.com/yufan022)

### 数据共享与订阅

* TiCDC 支持对多个异地目标数据源进行数据复制的复杂部署形态

    为了提供一套 TiDB 集群的数据能复制到多个不同的异地数据系统的能力，自 v6.3.0 开始，TiCDC 节点可以部署到多个不同的异地的机房中，来分别负责对应机房的数据复制任务，以支撑各种复杂的异地数据复制使用场景和部署形态。

    [用户文档]() [#issue]() @[sdojjy](https://github.com/sdojjy)

* TiCDC 支持维护上下游数据一致性快照（Sync point）

    在灾备复制场景下，TiCDC 支持周期性的维护一个下游数据快照，使得该下游快照能保持与上游数据的快照一致性。借助此能力，TiCDC 能更好的匹配读写分离应用场景，帮助用户降本增效。

    [用户文档]() [#issue]() @[asddongmen](https://github.com/asddongmen)

## 兼容性变更

### 系统变量

| 变量名 | 修改类型（包括新增/修改/删除） | 描述 |
| ------ | ------ | ------ |
| default_authentication_plugin | 修改 | 扩展可选值范围：增加 tidb_sm3_password，设置为 tidb_sm3_password 时，用户密码验证的加密算法为国密算法SM3 |
|  tidb_constraint_check_in_place_pessimistic | 新增 | 控制悲观事务中唯一约束检查的时间点 |
| tidb_enable_pseudo_for_outdated_stats | 修改 | 控制优化器过期的加载策略。 默认值由 `ON` 改为 `OFF`，即使统计信息过期，优化器也仍会使用该表上的统计信息。  |
|  |  |  |

### 配置文件参数

| 配置文件 | 配置项 | 修改类型 | 描述 |
| -------- | -------- | -------- | -------- |
| TiKV | data-encryption-method | 修改 | 扩展可选值范围：增加：sm4-ctr，设置为 sm4-ctr 时，数据将采用国密算法SM4加密后进行存储 |
| TiFlash | data-encryption-method | 修改 | 扩展可选值范围：增加：sm4-ctr，设置为 sm4-ctr 时，数据将采用国密算法SM4加密后进行存储 |
|          |          |          |          |
|          |          |          |          |
|          |          |          |          |

### 其他

* 提升对 MySQL 的兼容性：修复 MySQL 兼容性不支持项 “TiDB 不支持 ACCOUNT LOCK 和 ACCOUNT UNLOCK 选项”

## 废弃功能

## 改进提升

+ TiDB

    - note [#issue]() @[贡献者 GitHub ID]()

+ TiKV

    - note [#issue]() @[贡献者 GitHub ID]()

+ PD

    - note [#issue]() @[贡献者 GitHub ID]()

+ TiFlash

    - note [#issue]() @[贡献者 GitHub ID]()

+ Tools

    + TiDB Dashboard

        - 优化 TiDB Dashboard 的展示样式 [#issue]() @[贡献者 GitHub ID]()
        - 在 SQL 语句分析、慢查询等页面，提供当前返回的数据行数 [#issue]() @[贡献者 GitHub ID]()
        - 优化一些报错信息展示样式  [#issue]() @[贡献者 GitHub ID]()

    + Backup & Restore (BR)

        - note [#issue]() @[贡献者 GitHub ID]()

    + TiCDC

        - note [#issue]() @[贡献者 GitHub ID]()

    + TiDB Data Migration (DM)

        - note [#issue]() @[贡献者 GitHub ID]()

    + TiDB Lightning

        - note [#issue]() @[贡献者 GitHub ID]()

    + TiUP

        - note [#issue]() @[贡献者 GitHub ID]()

## 错误修复

+ TiDB

    - note [#issue]() @[贡献者 GitHub ID]()

+ TiKV

    - note [#issue]() @[贡献者 GitHub ID]()

+ PD

    - note [#issue]() @[贡献者 GitHub ID]()

+ TiFlash

    - note [#issue]() @[贡献者 GitHub ID]()

+ Tools

    + Backup & Restore (BR)

        - note [#issue]() @[贡献者 GitHub ID]()

    + TiCDC

        - note [#issue]() @[贡献者 GitHub ID]()

    + TiDB Data Migration (DM)

        - note [#issue]() @[贡献者 GitHub ID]()

    + TiDB Lightning

        - note [#issue]() @[贡献者 GitHub ID]()

    + TiUP

        - note [#issue]() @[贡献者 GitHub ID]()

## 贡献者

感谢来自 TiDB 社区的贡献者们：

- [贡献者 GitHub ID]()
