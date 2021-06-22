---
title: TiDB 5.1 Release Notes
---

# TiDB 5.1 Release Notes

发版日期：2021 年 6 月 24 日

TiDB 版本：5.1

在 5.1 版本中，你可以获得以下关键特性：

- 支持 MySQL 8 中的公共表表达式 (Common Table Expression)，提高了 SQL 语句的可读性与执行效率。
- 支持 MySQL 8 中的动态权限 (Dynamic Privileges) 配置，实现对某些操作更细粒度的控制。
- 支持通过 Stale Read 功能直接读取本地副本数据，降低读取延迟，提升查询性能。
- 新增锁视图 (Lock View) 功能方便 DBA 观察事务加锁情况以及排查死锁问题（实验特性）。
- 新增 TiKV 后台任务写入限制（TiKV Write Rate Limiter)，保证读写请求的延迟稳定性。

## 兼容性更改

> **注意：**
>
> 当从一个早期的 TiDB 版本升级到 TiDB 5.1 时，如需了解所有中间版本对应的兼容性更改说明，请查看对应版本的 [Release Note](/releases/release-notes.md)。 

### 系统变量

| 变量名   | 修改类型   | 描述   |
|:----------|:-----------|:-----------|
| `tidb_enable_enhanced_security`  | 新增 | 表示所连接的 TiDB 服务器是否启用了安全增强模式（SEM），在不重新启动 TiDB 服务器的情况下不能改变该变量。 |
| `cte_max_recursion_depth`  | 新增 | 用于控制公共表表达式最大递归深度。 |
| `init_connect`  | 新增 | 用于控制初始连接。 |
| `tidb_analyze_version`  | 新增 | 用于控制所收集到的统计信息。默认值从 `1` 修改为 `2`，默认作为实验特性启用。 |
| `tidb_enforce_mpp` | 新增 | 用于忽略优化器代价估算，强制使用 MPP 模式。`BOOL` 类型，默认值为 `false`。 |

### 配置文件参数

| 配置文件   | 配置项   | 修改类型   | 描述   |
|:----------|:-----------|:-----------|:-----------|
| TiDB 配置文件  | `security.enable-sem`  | 新增  | 控制是否启用安全增强模式 (SEM)。默认值为 `false`，代表未启用。 |
| TiDB 配置文件  | `performance.tcp-no-delay`  | 新增  | 控制是否在 TiDB 在 TCP 层开启 no delay。 默认值为 `true`，代表开启。 |
| TiDB 配置文件  | `performance.committer-concurrency`  | 修改  | 在单个事务的提交阶段，控制用于执行提交操作相关请求的 goroutine 数量。默认值从 `16` 修改为 `128`。|
| TiDB 配置文件  | `pessimistic-txn.deadlock-history-capacity`  | 新增  | 控制单个 TiDB 节点的 [`INFORMATION_SCHEMA.DEADLOCKS`](/information-schema/information-schema-deadlocks.md) 表最多可记录的死锁事件个数，默认值为 “10”。 |
| TiKV 配置文件  | `storage.io-rate-limit`  | 新增  | 控制 TiKV 写入的 IO 速率。`storage.io-rate-limit.max-bytes-per-sec` 默认值为 “0MB”。 |
| TiKV 配置文件  | `abort-on-panic`  | 新增  | 设置 TiKV panic 时 abort 进程是否允许系统生成 core dump 文件。默认值为 false, 代表不允许生成 core dump 文件。 |
| TiKV 配置文件  | `soft-pending-compaction-bytes-limit`  | 修改  | pending compaction bytes 的软限制，默认值从 "64GB" 修改为 "192GB"。 |
| TiKV 配置文件  | `hibernate-regions`  | 修改  | 默认值从 `false` 修改为 `true`。 如果 Region 长时间处于非活跃状态，即被自动设置为静默状态。 |
| TiKV 配置文件  | `resolved-ts.enable`  | 新增  | 为所有 Region leader 维护 `resolved-ts`，默认值为 `true`。 |
| TiKV 配置文件  | `resolved-ts.advance-ts-interval`  | 新增  | 推进 `resolved-ts` 的间隔，默认为 "1s"，支持动态更改。 |
| TiKV 配置文件  | `resolved-ts.scan-lock-pool-size`  | 新增  | 用于初始化 `resolved-ts` 时扫锁的线程数，默认值为 `2`。 |

### 其他

- 为了提升 TiDB 性能，TiDB 的 Go 编译器版本从 go1.13.7 升级到了 go1.16.4。如果你是 TiDB 的开发者，为了能保证顺利编译，请对应升级你的 Go 编译器版本。
- 请避免在对使用 TiDB Binlog 的集群进行滚动升级的过程中新创建聚簇索引表。
- 请避免在 TiDB 滚动升级时执行 `alter table ... modify column` 或 `alter table ... change column`。
- 当按表构建 TiFlash 副本时，v5.1 版本及后续版本将不再支持设置系统表的副本。在集群升级前，需要清除相关系统表的副本，否则升级到较高版本后将无法再修改系统表的副本设置。
- 在 TiCDC 的 `cdc cli changefeed` 命令中废弃 `--sort-dir` 参数，用户可在 `cdc server` 命令中设定 `--sort-dir`。[#1795](https://github.com/pingcap/ticdc/pull/1795)

## 新功能

### SQL

- 新增 MySQL 8 中的公共表表达式 (Common Table Expression)，为 TiDB 带来递归或非递归查询层次结构数据的能力，满足了人力资源、制造业、金融市场和教育在内的多种应用领域需要使用树形查询实现业务逻辑的需求。在 TiDB 中，你可以通过 `WITH` 语句使用公共表表达式。
[用户文档](/sql-statements/sql-statement-with.md)，[#17472](https://github.com/pingcap/tidb/issues/17472)

- 新增 MySQL 8 中的动态权限 (Dynamic Privileges)。动态权限用于限制 `SUPER` 权限，为 TiDB 提供更灵活的权限配置，实现对某些操作更细粒度的控制。例如，你可以使用动态权限来创建一个只能执行 `BACKUP` 和 `RESTORE` 操作的用户帐户。

    支持的动态权限包括：

    - `BACKUP_ADMIN`
    - `RESTORE_ADMIN`
    - `ROLE_ADMIN`
    - `CONNECTION_ADMIN`
    - `SYSTEM_VARIABLES_ADMIN`

    你也可以使用插件来添加新的权限。若要查看全部的动态权限，请执行 `SHOW PRIVILEGES` 语句。[用户文档](/privilege-management.md)

- 新增安全增强模式 (Security Enhanced Mode) 配置项，用于对 TiDB 管理员进行更细粒度的权限划分。安全增强模式默认关闭，如需开启，请参考[用户文档](/system-variables.md#tidb_enable_enhanced_security)。

- 全面加强列类型的在线变更能力，支持通过 `ALTER TABLE` 语句进行列的在线类型修改, 包括但不限于：

    - 从 `VARCHAR` 转换为 `BIGINT`
    - `DECIMAL` 精度修改
    - 从 `VARCHAR(10)` 到 `VARCHAR(5)` 的长度压缩

    [用户文档](/sql-statements/sql-statement-modify-column.md)

- 引入新的语法 `AS OF TIMESTAMP`，支持通过 Stale Read 功能从指定的时间点或时间范围内读取历史数据。

    [用户文档](/as-of-timestamp.md)，[#21094](https://github.com/pingcap/tidb/issues/21094)

    `AS OF TIMESTAMP` 语法示例如下：

    ```sql
    SELECT * FROM t AS OF TIMESTAMP  '2020-09-06 00:00:00';
    START TRANSACTION READ ONLY AS OF TIMESTAMP '2020-09-06 00:00:00';
    SET TRANSACTION READ ONLY as of timestamp '2020-09-06 00:00:00';
    ```

### 事务

+ 新增锁视图 (Lock View)（实验特性）

    [用户文档](/information-schema/information-schema-data-lock-waits.md)，[#24199](https://github.com/pingcap/tidb/issues/24199)

    Lock View 用于提供关于悲观锁的锁冲突和锁等待的更多信息，方便 DBA 通过锁视图功能来观察事务加锁情况以及排查死锁问题等

### 性能

+ 数据副本非一致性读 (Stale Read)

    直接读取本地副本数据，降低读取延迟，提升查询性能

    [用户文档](/stale-read.md)，[#21094](https://github.com/pingcap/tidb/issues/21094)

+ 默认开启 Hibernate Region 特性 [#10266](https://github.com/tikv/tikv/pull/10266)

### 稳定性

+ TiCDC 复制稳定性问题解决

    - 改善 TiCDC 内存使用，避免在以下场景出现 OOM

        - 同步中断期间积累大量数据，超过 1TB，重新同步出现 OOM 问题
        - 大量数据写入造成 TiCDC 出现 OOM 问题

    - 改善 TiCDC 同步中断问题，缓解以下场景的问题 [project#11](https://github.com/pingcap/ticdc/projects/11)

        - 网络不稳定情况下出现的同步中断问题
        - 在部分 TiKV/PD/TiCDC 节点宕机情况下出现的同步中断问题

+ TiFlash 存储内存控制

    优化了 Region 快照生成的速度和内存使用量，减少了 OOM 的可能性

+ 新增 TiKV 后台任务写入限制 (TiKV Write Rate Limiter)

    TiKV Write Rate Limiter 通过平滑 TiKV 后台任务如 GC，Compaction 等的写入流量，保证读写请求的延迟稳定性。TiKV 后台任务写入限制默认值为 "0MB"，建议将此限制设置为磁盘的最佳 I/O 带宽，例如云盘厂商指定的最大 I/O 带宽。

    [用户文档](/tikv-configuration-file.md#storageio-rate-limit)，[#9156](https://github.com/tikv/tikv/issues/9156)

+ 解决多个扩缩容时的调度稳定性问题

### 遥测

TiDB 在遥测中新增收集集群请求的运行状态，包括执行情况、失败情况等。

若要了解所收集的信息详情及如何禁用该行为，请参见[遥测](https://docs.pingcap.com/zh/tidb/stable/telemetry)文档。

## 提升改进

+ TiDB

    - 支持 `VITESS_HASH()` 函数 [#23915](https://github.com/pingcap/tidb/pull/23915)
    - 支持枚举类型下推到 TiKV ，提升 WHERE 子句中使用枚举类型时的性能 [#23619](https://github.com/pingcap/tidb/issues/23619)
    - 优化 Window Function 计算过程，解决了使用 ROW_NUMBER() 对数据分页时 TiDB OOM 的问题  [#23807](https://github.com/pingcap/tidb/issues/23807)
    - 优化 UNION ALL 的计算过程，解决了使用 UNION ALL 连接大量 SELECT 语句时 TiDB OOM 的问题  [#21441](https://github.com/pingcap/tidb/issues/21441)
    - 解决多种情况下出现的 `Region is Unavailable` 问题 [project#62](https://github.com/pingcap/tidb/projects/62)

        - 修复频繁调度情况下可能出现的多个 `Region is Unavailable` 问题
        - 解决部分高压力写入情况下可能出现的 `Region is Unavailable` 问题

    - 当内存中的统计信息缓存是最新的时，避免后台作业频繁读取 `mysql.stats_histograms` 表造成高 CPU 使用率 [#24317](https://github.com/pingcap/tidb/pull/24317)

+ TiKV

    - 使用 `zstd` 压缩 Region Snapshot，防止大量调度或扩缩容情况下出现各节点之间空间差异比较大的问题 [#10005](https://github.com/tikv/tikv/pull/10005)
    - 解决多种情况下的 OOM 问题 [#10183](https://github.com/tikv/tikv/issues/10183)

        - 增加各模块内存使用情况追踪
        - 解决 Raft entries cache 过大导致的 OOM 问题
        - 解决 GC tasks 堆积导致的 OOM 问题
        - 解决一次性从 Raft log 取太多 Raft entries 到内存导致 OOM 问题

    - 让 Region 分裂更均匀，缓解有写入热点时 Region 大小的增长速度超过分裂速度的问题 [#9785](https://github.com/tikv/tikv/issues/9785)

+ TiFlash

    - 新增对 `Union All`、`TopN`、`Limit` 函数的支持
    - 新增 MPP 模式下对笛卡尔积 left outer join 和 semi anti join 的支持
    - 优化锁操作以避免 DDL 语句和读数据相互阻塞
    - 优化 TiFlash 对过期数据的清理
    - 新增支持对 `timestamp` 列的查询过滤条件在 TiFlash 存储层进一步过滤
    - 在集群中有大量表时，优化 TiFlash 的启动速度及扩容速度
    - 提升 TiFlash 在未知 CPU 上运行的兼容性

+ PD
    - 避免在添加 `scatter region` 调度器后出现的非预期统计行为 [#3602](https://github.com/pingcap/pd/pull/3602)
    - 解决扩缩容过程中出现的多个调度问题

        - 优化副本 snapshot 生成流程，解决扩缩容调度慢问题：[#3563](https://github.com/tikv/pd/issues/3563) [#10059](https://github.com/tikv/tikv/pull/10059) [#10001](https://github.com/tikv/tikv/pull/10001)
        - 解决由于流量变化引带来的心跳压力引起的调度慢问题 [#3693](https://github.com/tikv/pd/issues/3693) [#3739](https://github.com/tikv/pd/issues/3739) [#3728](https://github.com/tikv/pd/issues/3728) [#3751](https://github.com/tikv/pd/issues/3751)
        - 减少大集群由于调度产生的空间差异问题，并优化调度公式防止由于压缩率差异大引发的类似异构空间集群的爆盘问题 [#3592](https://github.com/tikv/pd/issues/3592) [#10005](https://github.com/tikv/tikv/pull/10005)

+ Tools

    + Backup & Restore (BR)

        - 支持备份和恢复 `mysql` schema 下的用户数据表 [#1143](https://github.com/pingcap/br/pull/1143) [#1078](https://github.com/pingcap/br/pull/1078)
        - BR 支持 S3 兼容的存储（基于 virtual-host 寻址模式）[#10243](https://github.com/tikv/tikv/pull/10243)
        - BR 改进 backupmeta 格式，减少内存占用 [#1171](https://github.com/pingcap/br/pull/1171)

    + TiCDC

        - 改进了部分日志信息的描述使其更加明确清晰，对诊断问题更有帮助 [#1759](https://github.com/pingcap/ticdc/pull/1759)
        - 为 TiCDC 扫描的速度添加感知下游处理能力的 (back pressure) 功能 [#10151](https://github.com/tikv/tikv/pull/10151)
        - 减少 TiCDC 进行初次扫描的内存使用量 [#10133](https://github.com/tikv/tikv/pull/10133)
        - 提升了悲观事务中 TiCDC Old Value 的缓存命中率 [#10089](https://github.com/tikv/tikv/pull/10089)

    + Dumpling

        - 改善从 TiDB v4.0 导出数据的逻辑避免 TiDB OOM [#273](https://github.com/pingcap/dumpling/pull/273)
        - 修复备份失败却没有错误输出的问题 [#280](https://github.com/pingcap/dumpling/pull/280)

    + TiDB Lightning

        - 提升导入速度。优化结果显示，导入 TPC-C 数据速度提升在 30% 左右，导入索引比较多（5 个索引）的大表 (2TB+) 速度提升超过 50% [#753](https://github.com/pingcap/br/pull/753)
        - 导入前对导入数据和目标集群进行检查，如果不符合导入要求，则报错拒绝导入程序的运行 [#999](https://github.com/pingcap/br/pull/999)
        - 优化 Local 后端更新 checkpoint 的时机，提升断点重启时的性能 [#1080](https://github.com/pingcap/br/pull/1080)

## Bug 修复

+ TiDB

    - 修复投影消除在投影结果为空时执行结果可能错误的问题 [#23887](https://github.com/pingcap/tidb/issues/23887)
    - 修复列包含 `NULL` 值时查询结果在某些情况下可能错误的问题 [#23891](https://github.com/pingcap/tidb/issues/23891)
    - 当有虚拟列参与扫描时不允许生成 MPP 计划 [#23886](https://github.com/pingcap/tidb/issues/23886)
    - 修复 Plan Cache 中对 `PointGet` 和 `TableDual` 错误的重复使用 [#23187](https://github.com/pingcap/tidb/issues/23187) [#23144](https://github.com/pingcap/tidb/issues/23144) [#23304](https://github.com/pingcap/tidb/issues/23304) [#23290](https://github.com/pingcap/tidb/issues/23290)
    - 修复优化器在为聚簇索引构建 `IndexMerge` 执行计划时出现的错误 [#23906](https://github.com/pingcap/tidb/issues/23906)
    - 修复 BIT 类型相关错误的类型推导 [#23832](https://github.com/pingcap/tidb/issues/23832)
    - 修复某些优化器 Hint 在 `PointGet` 算子存在时无法生效的问题 [#23570](https://github.com/pingcap/tidb/issues/23570)
    - 修复 DDL 遇到错误回滚时可能失败的问题 [#23893](https://github.com/pingcap/tidb/issues/23893)
    - 修复二进制字面值常量的索引范围构造错误的问题 [#23672](https://github.com/pingcap/tidb/issues/23672)
    - 修复某些情况下 `IN` 语句的执行结果可能错误的问题 [#23889](https://github.com/pingcap/tidb/issues/23889)
    - 修复某些字符串函数的返回结果错误的问题 [#23759](https://github.com/pingcap/tidb/issues/23759)
    - 执行 `REPLACE` 语句需要用户同时拥有 `INSERT` 和 `DELETE` 权限 [#23909](https://github.com/pingcap/tidb/issues/23909)
    - 修复点查时出现的的性能回退 [#24070](https://github.com/pingcap/tidb/pull/24070)
    - 修复因错误比较二进制与字节而导致的 `TableDual` 计划错误的问题 [#23846](https://github.com/pingcap/tidb/issues/23846)
    - 修复了在某些情况下，使用前缀索引和 Index Join 导致的 panic 的问题 [#24547](https://github.com/pingcap/tidb/issues/24547) [#24716](https://github.com/pingcap/tidb/issues/24716) [#24717](https://github.com/pingcap/tidb/issues/24717)
    - 修复了 `point get` 的 prepare plan cache 被事务中的 `point get` 语句不正确使用的问题 [#24741](https://github.com/pingcap/tidb/issues/24741)
    - 修复了当排序规则为 `ascii_bin` 或 `latin1_bin` 时，写入错误的前缀索引值的问题 [#24569](https://github.com/pingcap/tidb/issues/24569)
    - 修复了正在执行的事务被 GC worker 中断的问题 [#24591](https://github.com/pingcap/tidb/issues/24591))
    - 修复了当 `new-collation` 开启且 `new-row-format` 关闭的情况下，点查在聚簇索引下可能出错的问题 [#24541](https://github.com/pingcap/tidb/issues/24541)
    - 为 Shuffle Hash Join 重构分区键的转换功能 [#24490](https://github.com/pingcap/tidb/pull/24490)
    - 修复了当查询包含 `HAVING` 子句时，在构建计划的过程中 panic 的问题 [#24045](https://github.com/pingcap/tidb/issues/24045)
    - 修复了列裁剪优化导致 `Apply` 算子和 `Join` 算子执行结果错误的问题 [#23887](https://github.com/pingcap/tidb/issues/23887)
    - 修复了从 Async Commit 回退的主锁无法被清除的问题 [#24384](https://github.com/pingcap/tidb/issues/24384)
    - 修复了一个统计信息 GC 的问题，该问题可能导致重复的 fm-sketch 记录 [#24357](https://github.com/pingcap/tidb/pull/24357)
    - 当悲观锁事务收到 `ErrKeyExists` 错误时，避免不必要的悲观事务回滚 [#23799](https://github.com/pingcap/tidb/issues/23799)
    - 修复了当 sql_mode 包含 `ANSI_QUOTES` 时，数值字面值无法被识别的问题 [#25015](https://github.com/pingcap/tidb/pull/25015)
    - 禁止如 `INSERT INTO table PARTITION (<partitions>) ... ON DUPLICATE KEY UPDATE` 的语句从 non-listed partitions 读取数据 [#24746](https://github.com/pingcap/tidb/issues/24746)
    - 修复了当 SQL 语句包含 `GROUP BY` 以及 `UNION` 时，可能会出现的 `index out of range` 的问题 [#24281](https://github.com/pingcap/tidb/issues/24281)
    - 修复了 `CONCAT` 函数错误处理排序规则的问题 [#24296](https://github.com/pingcap/tidb/issues/24296)
    - 修复了全局变量 `collation_server` 对新会话无法生效的问题 [#24156](https://github.com/pingcap/tidb/pull/24156)

+ TiKV

    - 修复了 Coprocessor 未正确处理 `IN` 表达式有符号整数或无符号整数类型数据的问题 [#9821](https://github.com/tikv/tikv/issues/9821)
    - 修复了在批量 ingest SST 文件后产生大量空 Region 的问题 [#964](https://github.com/pingcap/br/issues/964)
    - 修复了 file dictionary 文件损坏之后 TiKV 无法启动的问题 [#9886](https://github.com/tikv/tikv/issues/9886)
    - 修复了由于读取旧值而导致的 TiCDC OOM 问题 [#9996](https://github.com/tikv/tikv/issues/9996) [#9981](https://github.com/tikv/tikv/issues/9981)
    - 修复了聚簇主键列在次级索引上的 `latin1_bin` 字符集出现空值的问题 [#24548](https://github.com/pingcap/tidb/issues/24548)
    - 新增 `abort-on-panic` 配置，允许 TiKV 在 panic 时生成 core dump 文件。用户仍需正确配置环境以开启 core dump。 [#10216](https://github.com/tikv/tikv/pull/10216)
    - 修复了 TiKV 不繁忙时 `point get` 查询性能回退的问题 [#10046](https://github.com/tikv/tikv/issues/10046)

+ PD

    - 修复在 store 数量多的情况下，切换 PD Leader 慢的问题 [#3697](https://github.com/tikv/pd/issues/3697)
    - 修复删除不存在的 evict leader 调度器时出现 panic 的问题 [#3660](https://github.com/tikv/pd/issues/3660)
    - 修复 offline peer 在合并完后未更新统计的问题 [#3611](https://github.com/tikv/pd/issues/3611)

+ TiFlash

    - 修复 `TIME` 类型转换为 `INT` 类型时产生错误结果的问题
    - 修复 `receiver` 可能无法在 10 秒内找到对应任务的问题
    - 修复 `cancelMPPQuery` 中可能存在无效迭代器的问题
    - 修复 `bitwise` 算子和 TiDB 行为不一致的问题
    - 修复当使用 `prefix key` 时出现范围重叠报错的问题
    - 修复字符串转换为 `INT` 时产生错误结果的问题
    - 修复连续快速写入可能导致 TiFlash 内存溢出的问题
    - 修复 Table GC 时会引发空指针的问题
    - 修复向已被删除的表写数据时 TiFlash 进程崩溃的问题
    - 修复当使用 BR 恢复数据时 TiFlash 进程可能崩溃的问题
    - 修复并发复制共享 Delta 索引导致结果错误的问题
    - 修复 TiFlash 在 Compaction Filter 特性开启时可能崩溃的问题
    - 修复了从 Async Commit 回退的锁无法被 TiFlash 清除的问题
    - 修复当 `TIMEZONE` 类型的转换结果包含 `TIMESTAMP` 类型时返回错误结果的问题
    - 修复 TiFlash 在 Segment Split 期间异常退出的问题

+ Tools

    + TiDB Lightning

        - 修复在生成 KV 数据时可能发生的 panic 问题 [#1127](https://github.com/pingcap/br/pull/1127)
        - 修复数据导入期间 Batch Split Region 因键的总大小超过 Raft 条目限制而可能失败的问题 [#969](https://github.com/pingcap/br/issues/969)

            - 修复在导入 CSV 文件时，如果文件的最后一行未包含换行符(`\r\n`)会导入报错的问题 [#1133](https://github.com/pingcap/br/issues/1133)
        - 修复在导入目标表包含 double 类型的自增列会导致表的 auto_Increment 值异常的问题 [#1178](https://github.com/pingcap/br/pull/1178)

    + Backup & Restore (BR)

        - 修复备份期间少数 TiKV 节点不可用导致的备份中断问题 [#980](https://github.com/pingcap/br/issues/980)

    + TiCDC

        - 修复 Unified Sorter 中的并发问题并过滤无用的错误消息 [#1678](https://github.com/pingcap/ticdc/pull/1678)
        - 修复同步到 MinIO 时，重复创建目录会导致同步中断的问题 [#1463](https://github.com/pingcap/ticdc/issues/1463)
        - 默认开启会话变量 `explicit_defaults_for_timestamp`，使得下游 MySQL 5.7 和上游 TiDB 的行为保持一致 [#1585](https://github.com/pingcap/ticdc/issues/1585)
        - 修复错误地处理 `io.EOF` 可能导致同步中断的问题 [#1633](https://github.com/pingcap/ticdc/issues/1633)
        - 修正 TiCDC 面板中的 TiKV CDC endpoint CPU 统计信息 [#1645](https://github.com/pingcap/ticdc/pull/1645)
        - 增加 `defaultBufferChanSize` 来避免某些情况下同步阻塞的问题 [#1259](https://github.com/pingcap/ticdc/issues/1259)
        - 修复 Avro 输出中丢失时区信息的问题 [#1712](https://github.com/pingcap/ticdc/pull/1712)
        - 支持清理 Unified Sorter 过期的文件并禁止共享 `sort-dir` 目录 [#1742](https://github.com/pingcap/ticdc/pull/1742)
        - 修复存在大量过期 Region 信息时 KV 客户端可能锁死的问题 [#1599](https://github.com/pingcap/ticdc/issues/1599)
        - 修复 `--cert-allowed-cn` 参数中错误的帮助消息 [#1697](https://github.com/pingcap/ticdc/pull/1697)
        - 修复因更新 `explicit_defaults_for_timestamp` 而需要 MySQL `SUPER` 权限的问题 [#1750](https://github.com/pingcap/ticdc/pull/1750)
        - 添加 sink 流控以降低内存溢出的风险 [#1840](https://github.com/pingcap/ticdc/pull/1840)
        - 修复调度数据表时可能发生的同步终止问题 [#1828](https://github.com/pingcap/ticdc/pull/1828)
        - 修复 TiCDC changefeed 断点卡住导致 TiKV GC safe point 不推进的问题 [#1759](https://github.com/pingcap/ticdc/pull/1759)
