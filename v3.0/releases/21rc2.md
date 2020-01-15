---
title: TiDB 2.1 RC2 Release Notes
category: Releases
aliases: ['/docs-cn/releases/21rc2/']
---

# TiDB 2.1 RC2 Release Notes

2018 年 9 月 14 日，TiDB 发布 2.1 RC2 版。相比 2.1 RC1 版本，该版本对系统稳定性、优化器、统计信息以及执行引擎做了很多改进。

## TiDB

- SQL 优化器
    - 新版 Planner 设计方案 [#7543](https://github.com/pingcap/tidb/pull/7543)
    - 提升常量传播优化规则 [#7276](https://github.com/pingcap/tidb/pull/7276)
    - 增强 Range 的计算逻辑使其能够同时处理多个 `IN` 或者等值条件 [#7577](https://github.com/pingcap/tidb/pull/7577)
    - 修复当 Range 为空时，`TableScan` 的估算结果不正确的问题 [#7583](https://github.com/pingcap/tidb/pull/7583)
    - 为 `UPDATE` 语句支持 `PointGet` 算子 [#7586](https://github.com/pingcap/tidb/pull/7586)
    - 修复 `FirstRow` 聚合函数某些情况下在执行过程中 panic 的问题 [#7624](https://github.com/pingcap/tidb/pull/7624)
- SQL 执行引擎
    - 解决 HashJoin 算子在遇到错误的情况下潜在的 DataRace 问题 [#7554](https://github.com/pingcap/tidb/pull/7554)
    - HashJoin 算子同时读取内表数据和构建 Hash 表 [#7544](https://github.com/pingcap/tidb/pull/7544)
    - 优化 Hash 聚合算子性能 [#7541](https://github.com/pingcap/tidb/pull/7541)
    - 优化 Join 算子性能 [#7493](https://github.com/pingcap/tidb/pull/7493)、[#7433](https://github.com/pingcap/tidb/pull/7433)
    - 修复 `UPDATE JOIN` 在 Join 顺序改变后结果不正确的问题 [#7571](https://github.com/pingcap/tidb/pull/7571)
    - 提升 Chunk 迭代器的性能 [#7585](https://github.com/pingcap/tidb/pull/7585)
- 统计信息
    - 解决重复自动 Analyze 统计信息的问题 [#7550](https://github.com/pingcap/tidb/pull/7550)
    - 解决统计信息无变化时更新统计信息遇到错误的问题 [#7530](https://github.com/pingcap/tidb/pull/7530)
    - `Analyze` 执行时使用低优先级以及 RC 隔离级别 [#7496](https://github.com/pingcap/tidb/pull/7496)
    - 支持只在一天中的某个时间段开启统计信息自动更新的功能 [#7570](https://github.com/pingcap/tidb/pull/7570)
    - 修复统计信息写日志时发生的 panic [#7588](https://github.com/pingcap/tidb/pull/7588)
    - 支持通过 `ANALYZE TABLE WITH BUCKETS` 语句配置直方图中桶的个数 [#7619](https://github.com/pingcap/tidb/pull/7619)
    - 修复更新空的直方图时 panic 的问题 [#7640](https://github.com/pingcap/tidb/pull/7640)
    - 使用统计信息更新 `information_schema.tables.data_length` [#7657](https://github.com/pingcap/tidb/pull/7657)
- Server
    - 增加 Trace 相关的依赖库 [#7532](https://github.com/pingcap/tidb/pull/7532)
    - 开启 Golang 的 mutex profile 功能 [#7512](https://github.com/pingcap/tidb/pull/7512)
    - `Admin` 语句需要 `Super_priv` 权限 [#7486](https://github.com/pingcap/tidb/pull/7486)
    - 禁止用户 Drop 关键的系统表 [#7471](https://github.com/pingcap/tidb/pull/7471)
    - 从 `juju/errors` 切换到 `pkg/errors` [#7151](https://github.com/pingcap/tidb/pull/7151)
    - 完成 SQL Tracing 功能原型 [#7016](https://github.com/pingcap/tidb/pull/7016)
    - 删除 goroutine pool [#7564](https://github.com/pingcap/tidb/pull/7564)
    - 支持使用 `USER1` 信号来查看 goroutine 信息 [#7587](https://github.com/pingcap/tidb/pull/7587)
    - 将 TiDB 启动时的内部 SQL 设置为高优先级 [#7616](https://github.com/pingcap/tidb/pull/7616)
    - 在监控中用不同的标签区分内部 SQL 和用户 SQL [#7631](https://github.com/pingcap/tidb/pull/7631)
    - 缓存最近一周内最慢的 30 条慢查询日志在 TiDB Server 上 [#7646](https://github.com/pingcap/tidb/pull/7646)
    - TiDB 集群设置时区的方案 [#7656](https://github.com/pingcap/tidb/pull/7656)
    - 丰富 `GC life time is shorter than transaction duration` 错误信息 [#7658](https://github.com/pingcap/tidb/pull/7658)
    - 在 TiDB 集群启动时设置集群时区信息 [#7638](https://github.com/pingcap/tidb/pull/7638)
- 兼容性
    - `Year` 类型字段增加 unsigned flag [#7542](https://github.com/pingcap/tidb/pull/7542)
    - 修复在 Prepare/Execute 模式下，`Year` 类型结果长度设置问题 [#7525](https://github.com/pingcap/tidb/pull/7525)
    - 修复 Prepare/Execute 模式下时间 0 值的处理问题 [#7506](https://github.com/pingcap/tidb/pull/7506)
    - 解决整数类型除法实现中的错误处理问题 [#7492](https://github.com/pingcap/tidb/pull/7492)
    - 解决 `ComStmtSendLongData` 处理过程中的兼容性问题 [#7485](https://github.com/pingcap/tidb/pull/7485)
    - 解决字符串转为整数类型过程中的错误处理问题 [#7483](https://github.com/pingcap/tidb/pull/7483)
    - 优化 `information_schema.columns_in_table` 表中的值精度 [#7463](https://github.com/pingcap/tidb/pull/7463)
    - 修复使用 MariaDB 客户端对字符串类型数据的写入和更新的兼容性问题 [#7573](https://github.com/pingcap/tidb/pull/7573)
    - 修复返回值别名的兼容性问题 [#7600](https://github.com/pingcap/tidb/pull/7600)
    - 修复 `information_schema.COLUMNS` 表中浮点数的 `NUMERIC_SCALE` 值不正确的问题 [#7602](https://github.com/pingcap/tidb/pull/7602)
    - 解决单行注释内容为空 Parser 报错的问题 [#7612](https://github.com/pingcap/tidb/pull/7612)
- 表达式
    - 在 `insert` 函数中检查 `max_allowed_packet` 的值 [#7528](https://github.com/pingcap/tidb/pull/7528)
    - 支持内建函数 `json_contains` [#7443](https://github.com/pingcap/tidb/pull/7443)
    - 支持内建函数 `json_contains_path` [#7596](https://github.com/pingcap/tidb/pull/7596)
    - 支持内建函数 `encode/decode` [#7622](https://github.com/pingcap/tidb/pull/7622)
    - 修复一些时间相关的函数在某些情况下和 MySQL 行为不兼容的问题 [#7636](https://github.com/pingcap/tidb/pull/7636)
    - 解决从字符串中解析时间类型数据的兼容性问题 [#7654](https://github.com/pingcap/tidb/pull/7654)
    - 解决计算 `DateTime` 类型数据的默认值时没有考虑时区的问题 [#7655](https://github.com/pingcap/tidb/pull/7655)
- DML
    - `InsertOnDuplicateUpdate` 语句设置正确的 `last_insert_id` [#7534](https://github.com/pingcap/tidb/pull/7534)
    - 减少需要更新 `auto_increment_id` 计数器的情况 [#7515](https://github.com/pingcap/tidb/pull/7515)
    - 优化 `Duplicate Key` 错误的报错信息 [#7495](https://github.com/pingcap/tidb/pull/7495)
    - 修复 `insert...select...on duplicate key update` 问题 [#7406](https://github.com/pingcap/tidb/pull/7406)
    - 支持 `LOAD DATA IGNORE LINES` 语句 [#7576](https://github.com/pingcap/tidb/pull/7576)
- DDL
    - 在监控中增加 DDL Job 的类型和当前 Schema 版本的信息 [#7472](https://github.com/pingcap/tidb/pull/7472)
    - 完成 `Admin Restore Table` 功能方案设计 [#7383](https://github.com/pingcap/tidb/pull/7383)
    - 解决 Bit 类型的默认值超过 128 的问题 [#7249](https://github.com/pingcap/tidb/pull/7249)
    - 解决 Bit 类型默认值不能为 `NULL` 的问题 [#7604](https://github.com/pingcap/tidb/pull/7604)
    - 减少 DDL 队列中检查 `CREATE TABLE/DATABASE` 任务的时间间隔 [#7608](https://github.com/pingcap/tidb/pull/7608)
    - 使用 `ddl/owner/resign` HTTP 接口释放 DDL Owner 并开启新一轮 Owner 选举 [#7649](https://github.com/pingcap/tidb/pull/7649)
- TiKV Go Client
    - 支持 `Seek` 操作只获取 `Key` [#7419](https://github.com/pingcap/tidb/pull/7419)
- [Table Partition](https://github.com/pingcap/tidb/projects/6)（实验性）
    - 解决无法使用 Bigint 类型列作为 Partition Key 的问题 [#7520](https://github.com/pingcap/tidb/pull/7520)
    - 支持 Partitioned Table 添加索引过程中遇到问题回滚操作 [#7437](https://github.com/pingcap/tidb/pull/7437)

## PD

- 新特性
    - 支持 `GetAllStores`的接口 [#1228](https://github.com/pingcap/pd/pull/1228)
    - Simulator 添加评估调度的统计信息 [#1218](https://github.com/pingcap/pd/pull/1218)
- 功能改进
    - 优化 Down Store 的处理流程，尽快地补副本 [#1222](https://github.com/pingcap/pd/pull/1222)
    - 优化 Coordinator 的启动，减少重启 PD 带来的不必要调度 [#1225](https://github.com/pingcap/pd/pull/1225)
    - 优化内存使用，减少 heartbeat 带来的内存开销 [#1195](https://github.com/pingcap/pd/pull/1195)
    - 优化错误处理，完善日志信息 [#1227](https://github.com/pingcap/pd/pull/1227)
    - pd-ctl 支持查询指定 store 的 Region 信息 [#1231](https://github.com/pingcap/pd/pull/1231)
    - pd-ctl 支持查询按 version 比对的 topN 的 Region 信息 [#1233](https://github.com/pingcap/pd/pull/1233)
    - pd-ctl 支持更精确的 TSO 解码 [#1242](https://github.com/pingcap/pd/pull/1242)
- Bug 修复
    - 修复 pd-ctl 使用 hot store 命令错误退出的问题 [#1244](https://github.com/pingcap/pd/pull/1244)

## TiKV

- 性能优化
    - 支持基于统计估算进行 Region split，减少 I/O 开销 [#3511](https://github.com/tikv/tikv/pull/3511)
    - 减少部分组件的内存拷贝 [#3530](https://github.com/tikv/tikv/pull/3530)
- 功能改进
    - 增加大量内建函数下推支持
    - 增加 `leader-transfer-max-log-lag` 配置解决特定场景 leader 调度失败的问题 [#3507](https://github.com/tikv/tikv/pull/3507)
    - 增加 `max-open-engines` 配置限制 `tikv-importer` 同时打开的 engine 个数 [#3496](https://github.com/tikv/tikv/pull/3496)
    - 限制垃圾数据的清理速度，减少对 `snapshot apply` 的影响 [#3547](https://github.com/tikv/tikv/pull/3547)
    - 对关键 Raft 消息广播 commit 信息，避免不必要的延迟 [#3592](https://github.com/tikv/tikv/pull/3592)
- Bug 修复
    - 修复新分裂 Region 的 PreVote 消息被丢弃导致的 leader 选举问题 [#3557](https://github.com/tikv/tikv/pull/3557)
    - 修复 Region merge 以后 follower 的相关统计信息 [#3573](https://github.com/tikv/tikv/pull/3573)
    - 修复 local reader 使用过期 Region 信息的问题 [#3565](https://github.com/tikv/tikv/pull/3565)
