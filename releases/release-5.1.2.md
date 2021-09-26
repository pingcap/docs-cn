---
title: TiDB 5.1.2 Release Notes
---

# TiDB 5.1.2 Release Notes

发版日期：2021 年 9 月 27 日

TiDB 版本：5.1.2  

## 兼容性更改

+ Tools

    + TiCDC

        - 将兼容版本从`5.1.0-alpha`改为`5.2.0-alpha` [#2659](https://github.com/pingcap/ticdc/pull/2659)
        - 禁止跨主要和次要版本操作TiCDC集群 [#2599](https://github.com/pingcap/ticdc/pull/2599)
        - 修复 CLI 在默认的 sort-engine 选项上与 4.0.x 集群的兼容性问题 [#2414](https://github.com/pingcap/ticdc/pull/2414)

## 功能增强

+ Tools

    + Dumpling

        - 支持备份一些无法执行 `START TRANSACTION ... WITH CONSISTENT SNAPSHOT` 和 `SHOW CREATE TABLE` 语句的 MySQL 兼容数据库 [#328](https://github.com/pingcap/dumpling/pull/328)
        - 添加一个全局 `gRPC` 连接池并在 `kv` 客户端之间共享 `gRPC` 连接 [#2534](https://github.com/pingcap/ticdc/pull/2534)

## 改进提升

+ TiDB

    - 根据直方图行数来触 auto-analyze [#26708](https://github.com/pingcap/tidb/pull/26708)
    - 下推 mod() 到 TiFlash [#27865](https://github.com/pingcap/tidb/pull/27865)

+ TiKV

    - 支持动态更改 CDC (Change Data Capture) 配置项 [#10686] (https://github.com/tikv/tikv/pull/10686)
    - 减少 Resolved TS 的消息大小，以节省网络带宽 [#10679](https://github.com/tikv/tikv/pull/10679)
    - 支持限制每个 Store 发送的心跳包信息中 peer 状态（PeerStat）信息的数量 [#10621](https://github.com/tikv/tikv/pull/10621)

+ PD

    - 允许空 Region 被调度在 scatter range 调度器，并可以在该调度器中使用单独的 tolerance 配置项 [#4117](https://github.com/tikv/pd/pull/4117)
    - 提升 PD 之间同步 Region 信息的性能 [#3933](https://github.com/tikv/pd/pull/3933) 
    - 支持根据 Operator 的生成情况动态调整 Store 的重试次数 [#4048](https://github.com/tikv/pd/pull/4048)

+ TiFlash

    - 支持 `DATE()` 函数
    - 在 Grafana 面板增加每个实例的写入吞吐量
    - 优化 `leader-read` 流程的性能
    - 加速 `MPP` 任务取消的流程

+ Tools

    + TiCDC

        - 当统一分类器使用内存进行分类时，优化内存管理 [#2712](https://github.com/pingcap/ticdc/pull/2712)
        - 当并发性高时，优化`workerpool`以减少`goroutines`的数量 [#2488](https://github.com/pingcap/ticdc/pull/2488)
        - 当一个表的区域从一个 TiKV 节点转移出去时，减少`goroutine`的使用 [#2378](https://github.com/pingcap/ticdc/pull/2378)

## Bug 修复

+ TiDB

    - 修复 hash 列为 ENUM 类型时 index hash join 的结果可能出错的问题 [#28081](https://github.com/pingcap/tidb/pull/28081)
    - 修复极少数情况下 batch client 复用空闲连接可能阻塞请求发送的问题 [#27678](https://github.com/pingcap/tidb/pull/27678)
    - 通过使用与 MySQL 相同的 logic 以修复 overflow 检查的兼容性问题 [#26725](https://github.com/pingcap/tidb/pull/26725)
    - 修复 TiDB 把 `pd is timeout` 错误返回成 `unkonwn` 的问题 [#26682](https://github.com/pingcap/tidb/pull/26682)
    - 修复错误的 charset 和 collation 导致 case when 函数出错的问题 [#26673](https://github.com/pingcap/tidb/pull/26673)
    - 修复 `greatest(datetime) union null` 返回空结果的问题 [#26566](https://github.com/pingcap/tidb/pull/26566)
    - 修复 MPP 查询可能返回 `can not found column in Schema column` 错误的问题 [#28148](https://github.com/pingcap/tidb/pull/28148)
    - 修复 TiFlash 宕机可能导致 TiDB panic 的问题 [#28139](https://github.com/pingcap/tidb/pull/28139)
    - 修复谓词 `enum like 'x%'` 可能导致错误结果的问题 [#28066](https://github.com/pingcap/tidb/pull/28066)
    - 修复 `between` 表达式推导 collation 错误的问题 [#27549](https://github.com/pingcap/tidb/pull/27549)
    - 修复 CTE 和 IndexJoin 可能导致死锁的问题 [#27536](https://github.com/pingcap/tidb/pull/27536)
    - 修复死锁重试记录被错误的记录到 `INFORMATION_SCHEMA.DEADLOCKS` 的问题 [#27535](https://github.com/pingcap/tidb/pull/27535)
    - 修复 `group_concat` 不考虑 collation 的问题 [#27529](https://github.com/pingcap/tidb/pull/27529)
    - 修复在 new collation 打开时 distinct 多列返回错误数据的问题 [#27506](https://github.com/pingcap/tidb/pull/27506)
    - 修复分区表上的 `TABLESAMPLE` 查询排序不生效的问题 [#27411](https://github.com/pingcap/tidb/pull/27411)
    - 修复 `extract` 在参数为负数时可能出错的问题 [#27367](https://github.com/pingcap/tidb/pull/27367)
    - 移除 `/debug/sub-optimal-plan` HTTP 接口相关逻辑 [#27265](https://github.com/pingcap/tidb/pull/27265)
    - 修复当聚合包含 Having 条件时可能导致的错误 Selection 下推 [#27258](https://github.com/pingcap/tidb/pull/27258)
    - 修复 hash 分区在 unsigned 时可能返回错误数据的问题 [#27164](https://github.com/pingcap/tidb/pull/27164)
    - 修复转换非法字符串为 date 类型时可能出现的错误行为 [#27112](https://github.com/pingcap/tidb/pull/27112)
    - 修复当 `NO_UNSIGNED_SUBTRACTION` 被设置时创建分区可能出错的问题 [#27053](https://github.com/pingcap/tidb/pull/27053)
    - 修复 Apply 转换为 Join 时可能缺失 distinct 的问题 [#26969](https://github.com/pingcap/tidb/pull/26969)
    - 修复 `NO_ZERO_IN_DATE` 可能对默认值不生效的问题 [#26904](https://github.com/pingcap/tidb/pull/26904)
    - 当 TiFlash 在恢复状态时对其进行保护性屏蔽一段时间 [#26897](https://github.com/pingcap/tidb/pull/26897)
    - 修复 CTE 被引用多次时可能出现的 bug 的问题 [#26661](https://github.com/pingcap/tidb/pull/26661)
    - 修复使用 MergeJoin 时可能造成 CTE bug 的问题 [#26658](https://github.com/pingcap/tidb/pull/26658)
    - 修复当 Join 分区表和普通表时 `select for update` 不能正确上锁的问题 [#26631](https://github.com/pingcap/tidb/pull/26631)
    - 修复分区表 Join 时 `select for update` 可能造成 panic 的问题 [#26563](https://github.com/pingcap/tidb/pull/26563)
    - 修复 `PointGet` 不能使用轻量清锁的问题 [#26562](https://github.com/pingcap/tidb/pull/26562)

+ TiKV

    - 修复当TiKV从3.x,4.x升级至5.x时，在导入快照文件时可能出现的文件泄露问题. [#10912](https://github.com/tikv/tikv/pull/10912)
    - 修复在快照文件垃圾回收过程中，单个文件回收失败（比如损坏文件）会阻塞所有文件回收的问题. [#10873](https://github.com/tikv/tikv/pull/10873)
    - 在判断日志记录是否过慢时，仅考量请求的处理时间。当日志线程过载，队列塞满时丢弃日志而不是阻塞线程。 [#10865](https://github.com/tikv/tikv/pull/10865)
    - 修复处理coprocessor请求时超时造成的panic错误 [#10856](https://github.com/tikv/tikv/pull/10856)
    - 修复TiKV在启用Titan，并升级（从5.0之前）时出现的panic错误。修复无法回退至5.0.x的错误。 [#10842](https://github.com/tikv/tikv/pull/10842)
    - 修复TiKV可能会在RocksDB读取文件之前，将文件删除的错误。 [#10741](https://github.com/tikv/tikv/pull/10741)
    - 修复在resolve lock时因“遗留”悲观锁所造成的错误。 [#10653](https://github.com/tikv/tikv/pull/10653)

+ PD

    - 修复down-peer region无法及时被修复 [#4083](https://github.com/tikv/pd/pull/4083)
    - 修复max-replica 不一致问题 [#3915](https://github.com/tikv/pd/pull/3915)
    - 修复PD出现Panic在扩容场景下[#3911](https://github.com/tikv/pd/pull/3911)
    - 修复集群存在evict leader 调度器时，PD 热点调度无法工作[#3697](https://github.com/tikv/pd/pull/3697)

+ TiFlash

    - 修复无法建立 `MPP` 连接时出现异常结果的问题
    - 修复多盘部署时可能出现的数据不一致问题
    - 修复高负载时出现 `MPP` 查询结果错误的问题
    - 修复 `MPP` 查询卡死的潜在问题
    - 修复节点初始化与 `DDL` 操作并发执行时出现异常的问题
    - 修复当查询过滤条件包含诸如 `CONSTANT` `<` | `<=` | `>` | `>=` `COLUMN` 时出现错误结果的问题
    - 修复多个 `DDL` 操作和 `Apply Snapshot` 操作并发执行时出现异常的潜在问题
    - 修复写压力大时 metrics 中 store size 不准确的问题
    - 修复长时间运行后无法回收 delta 历史数据的潜在问题
    - 修复开启 `new collation` 时导致查询结果错误的问题
    - 修复解锁操作出现异常的潜在问题
    - 修复 metrics 显示错误值的问题

+ Tools

    + Backup & Restore (BR)

        - 修复了备份数据和恢复数据时显示的`平均速度`的数值不正确的问题[#1412](https://github.com/pingcap/br/pull/1412)

    + Dumpling

        - 修复特定 MySQL 版本（8.0.3，8.0.23）下，`show table status`返回结果不正确导致 dump 阶段卡死的问题 [#333](https://github.com/pingcap/dumpling/pull/333)

    + TiCDC

        - 修复未充分考虑字符串类型的值可能是`string`或`[]byte`时，转换为`json` 格式可能导致 TiCDC 进程崩溃的问题 [#2783](https://github.com/pingcap/ticdc/pull/2783)
        - 降低`gRPC`的`window size`以避免出现`OOM`的情况 [#2725](https://github.com/pingcap/ticdc/pull/2725)
        - 修复内存压力较高时`gRPC`的`keepalive`错误 [#2720](https://github.com/pingcap/ticdc/pull/2720)
        - 修复`unsigned tinyint`导致 TiCDC 崩溃的问题 [#2656](https://github.com/pingcap/ticdc/pull/2656)
        - 修复开放协议下输出空值的问题。修复后，在开放协议下，未包含变更的事务 TiCDC 处理时不再输出空值  [#2621](https://github.com/pingcap/ticdc/pull/2621)
        - 修复手动重启 TiCDC 时`DDL`处理上的一个问题 [#2607](https://github.com/pingcap/ticdc/pull/2607)
        - 修复一个元数据管理上的问题 [#2559](https://github.com/pingcap/ticdc/pull/2559)
        - 修复当表正在被重新调度时可能被多个进程同时写入的问题 [#2493](https://github.com/pingcap/ticdc/pull/2493)
        - 修复日志中出现的`ErrSchemaStorageTableMiss`错误且`changefeed`被意外重置的问题 [#2459](https://github.com/pingcap/ticdc/pull/2459)
        - 修复遇到`GcTTL Exceeded`错误时`changefeed`无法被移除的问题 [#2454](https://github.com/pingcap/ticdc/pull/2454)
        - 修复一个同步大表到`cdclog`失败的问题 [#2446](https://github.com/pingcap/ticdc/pull/2446)
