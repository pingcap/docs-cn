---
title: TiDB 2.1 GA Release Notes
category: Releases
---

# TiDB 2.1 GA Release Notes

2018 年 11 月 30 日，TiDB 发布 2.1 GA 版。相比 2.0 版本，该版本对系统稳定性、性能、兼容性、易用性做了大量改进。

## TiDB

+ SQL 优化器

    - 优化 `Index Join` 选择范围，提升执行性能
    - 优化 `Index Join` 外表选择，使用估算的行数较少的表作为外表
    - 扩大 Join Hint `TIDB_SMJ` 的作用范围，在没有合适索引可用的情况下也可使用 Merge Join
    - 加强 Join Hint `TIDB_INLJ` 的能力，可以指定 Join 中的内表
    - 优化关联子查询，包括下推 Filter 和扩大索引选择范围，部分查询的效率有数量级的提升
    - 支持在 `UPDATE` 和 `DELETE` 语句中使用 Index Hint 和 Join Hint
    - 支持更多函数下推：`ABS`/`CEIL`/`FLOOR`/`IS TRUE`/`IS FALSE`
    - 优化内建函数 `IF` 和 `IFNULL` 的常量折叠算法
    - 优化 `EXPLAIN` 语句输出格式, 使用层级结构表示算子之间的上下游关系

+ SQL 执行引擎

    - 重构所有聚合函数，提升 `Stream` 和 `Hash` 聚合算子的执行效率
    - 实现并行 `Hash Aggregate` 算子，部分场景下有 350% 的性能提升
    - 实现并行 `Project` 算子，部分场景有 74% 的性能提升
    - 并发地读取 `Hash Join` 的 `Inner` 表和 `Outer` 表的数据，提升执行性能
    - 优化 `REPLACE INTO` 语句的执行速度，性能提升 10x
    - 优化时间类型的内存占用，时间类型数据的内存使用降低为原来的一半
    - 优化点查的查询性能，Sysbench 点查效率提升 60%
    - TiDB 插入和更新宽表，性能提升接近 20 倍
    - 支持在配置文件中设置单个查询的内存使用上限
    - 优化 `Hash Join` 的执行过程，当 Join 类型为 `Inner Join` 或者 `Semi Join` 时，如果内表为空，不再读取外表数据，快速返回结果
    - 支持 `EXPLAIN ANALYZE` 语句，用于查看 Query 执行过程中各个算子的运行时间，返回结果行数等运行时统计信息

+ 统计信息

    - 支持只在一天中的某个时间段开启统计信息自动 ANALYZE 的功能
    - 支持根据查询的反馈自动更新表的统计信息
    - 支持通过 `ANALYZE TABLE WITH BUCKETS` 语句配置直方图中桶的个数
    - 优化等值查询和范围查询混合的情况下使用直方图估算 Row Count 的算法

+ 表达式

    + 支持内建函数：

        - `json_contains`
        - `json_contains_path`
        - `encode/decode`

+ Server

    - 支持在单个 tidb-server 实例内部对冲突事务排队，优化事务间冲突频繁的场景下的性能
    - 支持 Server Side Cursor
    - 新增 HTTP 管理接口
    - 打散 table 的 Regions 在 TiKV 集群中的分布
    - 控制是否打开 `general log`
    - 在线修改日志级别
    - 查询 TiDB 集群信息
    - 添加 `auto_analyze_ratio` 系统变量控制自动 Analyze 的阈值
    - 添加 `tidb_retry_limit` 系统变量控制事务自动重试的次数
    - 添加 `tidb_disable_txn_auto_retry` 系统变量控制事务是否自动重试
    - 支持使用 `admin show slow` 语句来获取慢查询语句
    - 增加环境变量 `tidb_slow_log_threshold` 动态设置 slow log 的阈值
    - 增加环境变量 `tidb_query_log_max_len` 动态设置日志中被截断的原始 SQL 语句的长度

+ DDL

    - 支持 Add Index 语句与其他 DDL 语句并行执行，避免耗时的 Add Index 操作阻塞其他操作
    - 优化 `Add Index` 的速度，在某些场景下速度大幅提升
    - 支持 `select tidb_is_ddl_owner()` 语句，方便判断 TiDB 是否为 `DDL Owner`
    - 支持 `ALTER TABLE FORCE` 语法
    - 支持 `ALTER TABLE RENAME KEY TO` 语法
    - `Admin Show DDL Jobs` 输出结果中添加表名、库名等信息
    - 支持使用 `ddl/owner/resign` HTTP 接口释放 DDL Owner 并开启新一轮 DDL Owner 选举

+ 兼容性

    - 支持更多 MySQL 语法
    - `BIT` 聚合函数支持 `ALL` 参数
    - 支持 `SHOW PRIVILEGES` 语句
    - 支持 `LOAD DATA` 语句的 `CHARACTER SET` 语法
    - 支持 `CREATE USER` 语句的 `IDENTIFIED WITH` 语法
    - 支持 `LOAD DATA IGNORE LINES` 语句
    - `Show ProcessList` 语句返回更准确信息

## PD (Placement Driver)

+ 可用性优化

    - 引入 TiKV 版本控制机制，支持集群滚动兼容升级
    - PD 节点间开启 `Raft PreVote`，避免网络隔离后恢复时产生的重新选举
    - 开启 `raft learner` 功能，降低调度时出现宕机导致数据不可用的风险
    - TSO 分配不再受系统时间回退影响
    - 支持 `Region merge` 功能，减少元数据带来的开销

+ 调度器优化

    - 优化 Down Store 的处理流程，加快发生宕机后补副本的速度
    - 优化热点调度器，在流量统计信息抖动时适应性更好
    - 优化 Coordinator 的启动，减少重启 PD 时带来的不必要调度
    - 优化 Balance Scheduler 频繁调度小 Region 的问题
    - 优化 Region merge，调度时考虑 Region 中数据的行数
    - 新增一些控制调度策略的开关
    - 完善调度模拟器，添加调度场景模拟

+ API 及运维工具

    - 新增 `GetPrevRegion` 接口，用于支持 TiDB reverse scan 功能
    - 新增 `BatchSplitRegion` 接口，用于支持 TiKV 快速 Region 分裂
    - 新增 `GCSafePoint` 接口，用于支持 TiDB 并发分布式 GC
    - 新增 `GetAllStores` 接口，用于支持 TiDB 并发分布式 GC
    + pd-ctl 新增：

        - 使用统计信息进行 Region split
        - 调用 `jq` 来格式化 JSON 输出
        - 查询指定 store 的 Region 信息
        - 查询按 version 排序的 topN 的 Region 列表
        - 查询按 size 排序的 topN 的 Region 列表
        - 更精确的 TSO 解码

    - pd-recover 不再需要提供 max-replica 参数

+ 监控

    - 增加 `Filter` 相关的监控
    - 新增 etcd Raft 状态机相关监控

+ 性能优化

    - 优化处理 Region heartbeat 的性能，减少 heartbeat 带来的内存开销
    - 优化 Region tree 性能
    - 优化计算热点统计的性能问题

## TiKV

+ Coprocessor

    - 新增支持大量内建函数
    - 新增 Coprocessor ReadPool，提高请求处理并发度
    - 修复时间函数解析以及时区相关问题
    - 优化下推聚合计算的内存使用

+ Transaction

    - 优化 MVCC 读取逻辑以及内存使用效率，提高扫描操作的性能，Count 全表性能比 2.0 版本提升 1 倍
    - 折叠 MVCC 中连续的 Rollback 记录，保证记录的读取性能
    - 新增 `UnsafeDestroyRange` API 用于在 drop table/index 的情况下快速回收空间
    - GC 模块独立出来，减少对正常写入的影响
    - kv_scan 命令支持设置 upper bound

+ Raftstore

    - 优化 snapshot 文件写入流程避免导致 RocksDB stall
    - 增加 LocalReader 线程专门处理读请求，降低读请求的延迟
    - 支持 `BatchSplit` 避免大量写入导致产生特别大的 Region
    - 支持按照统计信息进行 Region Split，减少 IO 开销
    - 支持按照 Key 的数量进行 Region Split，提高索引扫描的并发度
    - 优化部分 Raft 消息处理流程，避免 Region Split 带来不必要的延迟
    - 启用 `PreVote` 功能，减少网络隔离对服务的影响

+ 存储引擎

    - 修复 RocksDB `CompactFiles` 的 bug，可能影响 Lightning 导入的数据
    - 升级 RocksDB 到 v5.15，解决 snapshot 文件可能会被写坏的问题
    - 优化 `IngestExternalFile`，避免 flush 卡住写入的问题

+ tikv-ctl

    - 新增 ldb 命令，方便排查 RocksDB 相关问题
    - compact 命令支持指定是否 compact bottommost 层的数据

## Tools

- 全量数据快速导入工具 TiDB Lightning
- 支持新版本 TiDB Binlog

## 升级兼容性说明

+ 由于新版本存储引擎更新，不支持在升级后回退至 2.0.x 或更旧版本
+ 从 2.0.6 之前的版本升级到 2.1 之前，最好确认集群中是否存在正在运行中的 DDL 操作，特别是耗时的 Add Index 操作，等 DDL 操作完成后再执行升级操作
+ 因为 2.1 版本启用了并行 DDL，对于早于 2.0.1 版本的集群，无法滚动升级到 2.1，可以选择下面两种方案：

    - 停机升级，直接从早于 2.0.1 的 TiDB 版本升级到 2.1
    - 先滚动升级到 2.0.1 或者之后的 2.0.x 版本，再滚动升级到 2.1 版本
