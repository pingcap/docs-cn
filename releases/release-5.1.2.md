---
title: TiDB 5.1.2 Release Notes
---

# TiDB 5.1.2 Release Notes

发版日期：2021 年 9 月 27 日

TiDB 版本：5.1.2

## 兼容性更改

+ Tools

    + TiCDC

        - 将兼容版本从 `5.1.0-alpha` 改为 `5.2.0-alpha` [#2659](https://github.com/pingcap/ticdc/pull/2659)
        - 禁止跨主要和次要版本操作 TiCDC 集群 [#2599](https://github.com/pingcap/ticdc/pull/2599)
        - 修复 CLI 在默认 `sort-engine` 选项上与 4.0.x 集群的兼容性问题 [#2373](https://github.com/pingcap/ticdc/issues/2373)

## 功能增强

+ Tools

    + Dumpling

        - 支持备份一些无法执行 `START TRANSACTION ... WITH CONSISTENT SNAPSHOT` 和 `SHOW CREATE TABLE` 语句的 MySQL 兼容数据库 [#309](https://github.com/pingcap/dumpling/issues/309)
        - 添加一个全局 gRPC 连接池并在 KV 客户端之间共享 gRPC 连接 [#2534](https://github.com/pingcap/ticdc/pull/2534)

## 改进提升

+ TiDB

    - 根据直方图行数来触 auto-analyze，提升 auto-analyze 触发的准确度 [#24237](https://github.com/pingcap/tidb/issues/24237)
    - 下推 `mod()` 到 TiFlash，提升查询性能 [#2318](https://github.com/pingcap/tics/issues/2318)

+ TiKV

    - 支持动态更改 TiCDC 配置项 [#10645](https://github.com/tikv/tikv/issues/10645)
    - 减少 Resolved TS 消息的大小以节省网络带宽 [#2448](https://github.com/pingcap/ticdc/issues/2448)
    - 支持限制每个 Store 发送的心跳包信息中 peer stats 的数量 [#10621](https://github.com/tikv/tikv/pull/10621)

+ PD

    - 允许空 Region 被调度在 scatter range 调度器，并可以在该调度器中使用单独的 `tolerance` 配置项 [#4117](https://github.com/tikv/pd/pull/4117)
    - 提升 PD 之间同步 Region 信息的性能 [#3933](https://github.com/tikv/pd/pull/3933)
    - 支持根据 Operator 的生成情况动态调整 Store 的重试次数 [#3744](https://github.com/tikv/pd/issues/3744)

+ TiFlash

    - 支持 `DATE()` 函数
    - 在 Grafana 面板增加每个实例的写入吞吐量
    - 优化 `leader-read` 流程的性能
    - 加速 `MPP` 任务取消的流程

+ Tools

    + TiCDC

        - 当统一分类器使用内存进行分类时，优化内存管理 [#2712](https://github.com/pingcap/ticdc/pull/2712)
        - 当并发性高时，优化 workerpool 以减少 goroutines 的数量 [#2488](https://github.com/pingcap/ticdc/pull/2488)
        - 当一个表的区域从一个 TiKV 节点转移出去时，减少 goroutine 的使用 [#2284](https://github.com/pingcap/ticdc/issues/2284)

## Bug 修复

+ TiDB

    - 修复 hash 列为 `ENUM` 类型时 index hash join 的结果可能出错的问题 [#27893](https://github.com/pingcap/tidb/issues/27893)
    - 修复极少数情况下 batch client 复用空闲连接可能阻塞请求发送的问题 [#27678](https://github.com/pingcap/tidb/pull/27678)
    - 通过使用与 MySQL 相同的 logic 以修复 overflow 检查的兼容性问题 [#23897](https://github.com/pingcap/tidb/issues/23897)
    - 修复 TiDB 把 `pd is timeout` 错误返回成 `unkonwn` 的问题 [#26147](https://github.com/pingcap/tidb/issues/26147)
    - 修复错误的字符集和排序规则导致 `case when` 函数出错的问题 [#26662](https://github.com/pingcap/tidb/issues/26662)
    - 修复 `greatest(datetime) union null` 返回空结果的问题 [#26532](https://github.com/pingcap/tidb/issues/26532)
    - 修复 MPP 查询可能返回 `can not found column in Schema column` 错误的问题 [#28148](https://github.com/pingcap/tidb/pull/28148)
    - 修复 TiFlash 宕机可能导致 TiDB Panic 的问题 [#28096](https://github.com/pingcap/tidb/issues/28096)
    - 修复使用谓词 `enum like 'x%'` 可能导致错误结果的问题 [#27130](https://github.com/pingcap/tidb/issues/27130)
    - 修复 `between` 表达式推导 collation 错误的问题 [#27146](https://github.com/pingcap/tidb/issues/27146)
    - 修复当使用 IndexLookupJoin 时公共表达式 (CTE) 死锁的问题 [#27410](https://github.com/pingcap/tidb/issues/27410)
    - 修复死锁重试被错误记录到 `INFORMATION_SCHEMA.DEADLOCKS` 表的问题 [#27400](https://github.com/pingcap/tidb/issues/27400)
    - 修复 `GROUP_CONCAT` 函数未考虑 collation 的问题 [#27429](https://github.com/pingcap/tidb/issues/27429)
    - 修复当开启 New Collation 时 `COUNT(DISTINCT)` 多列返回错误结果的问题 [#27091](https://github.com/pingcap/tidb/issues/27091)
    - 修复分区表上的 `TABLESAMPLE` 查询结果排序不生效的问题 [#27349](https://github.com/pingcap/tidb/issues/27349)
    - 修复 `EXTRACT` 函数在参数为负数时返回错误结果的问题 [#27236](https://github.com/pingcap/tidb/issues/27236)
    - 移除未使用的 `/debug/sub-optimal-plan` HTTP 接口相关逻辑 [#27265](https://github.com/pingcap/tidb/pull/27265)
    - 修复当聚合函数包含 `HAVING` 条件时导致的错误 Selection 下推 [#26496](https://github.com/pingcap/tidb/issues/26496)
    - 修复 hash 分区表处理无符号数据时查询返回错误结果的问题 [#26569](https://github.com/pingcap/tidb/issues/26569)
    - 修复转换非法字符串为 `DATE` 类型时出现的非预期行为 [#26762](https://github.com/pingcap/tidb/issues/26762)
    - 修复当 `NO_UNSIGNED_SUBTRACTION` 被设置时创建分区出错的问题 [#26765](https://github.com/pingcap/tidb/issues/26765)
    - 修复 `Apply` 转换为 Join 时缺失 `distinct` 的问题 [#26958](https://github.com/pingcap/tidb/issues/26958)
    - 修复 `NO_ZERO_IN_DATE` 对默认值不生效的问题 [#26766](https://github.com/pingcap/tidb/issues/26766)
    - 为处于恢复状态的 TiFlash 节点设置一段屏蔽时间，避免在此时间内阻塞查询 [#26897](https://github.com/pingcap/tidb/pull/26897)
    - 修复 CTE 被引用多次时可能出现的 bug 的问题 [#26212](https://github.com/pingcap/tidb/issues/26212)
    - 修复使用 MergeJoin 时可能造成 CTE 出现 bug 的问题 [#25474](https://github.com/pingcap/tidb/issues/25474)
    - 修复当 Join 分区表和普通表时 `select for update` 不能正确上锁的问题 [#26251](https://github.com/pingcap/tidb/issues/26251)
    - 修复当 Join 分区表和普通表时 `select for update` 语句结果报错的问题 [#26250](https://github.com/pingcap/tidb/issues/26250)
    - 修复 `PointGet` 不能使用轻量清锁的问题 [#26562](https://github.com/pingcap/tidb/pull/26562)

+ TiKV

    - 修复当 TiKV 从 v3.x 升级至较高版本时，在导入快照文件时出现文件导入不完整的问题 [#10902](https://github.com/tikv/tikv/issues/10902)
    - 修复损坏的快照文件可能会造成磁盘空间无法回收的问题 [#10813](https://github.com/tikv/tikv/issues/10813)
    - 当 slogger 线程过载且队列已满时，删除日志而不是阻塞线程 [#10841](https://github.com/tikv/tikv/issues/10841)
    - 使 TiKV Coprocessor 慢日志只考虑处理请求所花费的时间 [#10841](https://github.com/tikv/tikv/issues/10841)
    - 修复当处理 Coprocessor 请求时因超时而导致 Panic 的问题 [#10852](https://github.com/tikv/tikv/issues/10852)
    - 修复 TiKV 在启用 Titan 并从 v5.0 以前的版本升级时出现 Panic 的问题 [#10842](https://github.com/tikv/tikv/pull/10842)
    - 修复高版本的 TiKV 无法回滚到 v5.0.x 的问题 [#10842](https://github.com/tikv/tikv/pull/10842)
    - 修复 TiKV 可能会在 RocksDB 读取文件之前删除文件的错误 [#10438](https://github.com/tikv/tikv/issues/10438)
    - 修复遗留的悲观锁导致的解析失败的问题 [#26404](https://github.com/pingcap/tidb/issues/26404)

+ PD

    - 修复 PD 未能及时修复 Down Peer 副本的问题 [#4077](https://github.com/tikv/pd/issues/4077)
    - 修复 `replication.max-replicas` 更新后默认的 Placement Rules 副本数量不变的问题 [#3886](https://github.com/tikv/pd/issues/3886)
    - 修复 PD 在扩容 TiKV 时可能会 Panic 的问题 [#3868](https://github.com/tikv/pd/issues/3868)
    - 修复当集群中存在 evict leader 调度器时，PD 热点调度无法工作的问题 [#3697](https://github.com/tikv/pd/issues/3697)

+ TiFlash

    - 修复无法建立 MPP 连接时出现异常结果的问题
    - 修复多盘部署时可能出现的数据不一致问题
    - 修复高负载时出现 MPP 查询结果错误的问题
    - 修复 MPP 查询卡死的潜在问题
    - 修复节点初始化与 DDL 操作并发执行时出现异常的问题
    - 修复查询过滤条件包含诸如 `CONSTANT`、`<`、`<=`、`>`、`>=` 或 `COLUMN` 时出现错误结果的问题
    - 修复多个 DDL 操作和 Apply Snapshot 操作并发执行时出现异常的潜在问题
    - 修复写压力大时 metrics 中 store size 不准确的问题
    - 修复长时间运行后无法回收 Delta 历史数据的潜在问题
    - 修复开启 New Collation 时查询结果错误的问题
    - 修复解锁出现异常的潜在问题
    - 修复 metrics 显示错误值的问题

+ Tools

    + Backup & Restore (BR)

        - 修复了备份数据和恢复数据时显示的平均速度数值不正确的问题 [#1405](https://github.com/pingcap/br/issues/1405)

    + Dumpling

        - 修复特定 MySQL 版本（8.0.3，8.0.23）下，`show table status` 返回结果不正确导致 dump 阶段卡死的问题 [#333](https://github.com/pingcap/dumpling/pull/333)

    + TiCDC

        - 修复未充分考虑字符串类型的值可能是 `string` 或 `[]byte` 时，转换为 JSON 格式可能导致 TiCDC 进程崩溃的问题 [#2758](https://github.com/pingcap/ticdc/issues/2758)
        - 降低 gRPC 的 window size 以避免出现 OOM 的情况 [#2202](https://github.com/pingcap/ticdc/issues/2202)
        - 修复内存压力较高时 gRPC 的 keepalive 错误 [#2202](https://github.com/pingcap/ticdc/issues/2202)
        - 修复 `unsigned tinyint` 导致 TiCDC 崩溃的问题 [#2648](https://github.com/pingcap/ticdc/issues/2648)
        - 修复 TiCDC Open Protocol 下输出空值的问题。修复后，在开放协议下，未包含变更的事务 TiCDC 处理时不再输出空值 [#2612](https://github.com/pingcap/ticdc/issues/2612)
        - 修复手动重启 TiCDC 时 DDL 处理存在的问题 [#2603](https://github.com/pingcap/ticdc/issues/2603)
        - 修复操作元数据时，`EtcdWorker` 的快照隔离可能被破坏的问题 [#2559](https://github.com/pingcap/ticdc/pull/2559)
        - 修复表被重新调度时，可能被多个进程同时写入的问题 [#2230](https://github.com/pingcap/ticdc/issues/2230)
        - 修复日志中出现的 `ErrSchemaStorageTableMiss` 错误且 `changefeed` 被意外重置的问题 [#2422](https://github.com/pingcap/ticdc/issues/2422)
        - 修复遇到 `GcTTL Exceeded` 错误时 `changefeed` 无法被移除的问题 [#2391](https://github.com/pingcap/ticdc/issues/2391)
        - 修复同步大表到 cdclog 失败的问题 [#1259](https://github.com/pingcap/ticdc/issues/1259)[#2424](https://github.com/pingcap/ticdc/issues/2424)
