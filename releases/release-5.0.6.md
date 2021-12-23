---
title: TiDB 5.0.6 Release Notes
---

# TiDB 5.0.6 Release Notes

发版日期：2021 年 12 月 28 日

TiDB 版本：5.0.6

## 兼容性更改

+ Tools

    + TiCDC

        - cdc server 命令错误输出从标准输出改成标准错误. [#3133](https://github.com/pingcap/tiflow/issues/3133)

## 提升改进

+ TiDB

    (dup) - 修复乐观事务冲突可能导致事务相互阻塞的问题 [#11148](https://github.com/tikv/tikv/issues/11148)
    (dup) - 修复运行 MPP 查询时出现 `invalid cop task execution summaries length` 相关日志的问题 [#1791](https://github.com/pingcap/tics/issues/1791)
    (dup) - 当 coprocessor 遇到锁时，在调试日志中显示受影响的 SQL 语句帮助诊断问题 [#27718](https://github.com/pingcap/tidb/issues/27718)

+ TiKV

    - 将插入 SST 文件时的校验操作移动到了 import 线程池以提高 SST 文件插入速度. [#11239](https://github.com/tikv/tikv/issues/11239)
    - 为 raft 日志回收模块增加了更多监控以定位问题. [#11374](https://github.com/tikv/tikv/issues/11374)
    - 折叠了部分 Storage 相关的不常用监控 [#11681](https://github.com/tikv/tikv/issues/11681)

+ PD

    (dup) - 优化调度器退出的速度 [#4146](https://github.com/tikv/pd/issues/4146)
    - 通过允许空 Region 调度和修复配置的方式使 scatter-range-scheduler运行更好 [#4116](https://github.com/tikv/pd/pull/4116)

+ Tools

    + TiCDC

        (dup) - 优化 TiKV 重新加载时的速率限制控制，缓解 changefeed 初始化时 gPRC 的拥堵问题 [#3110](https://github.com/pingcap/tiflow/issues/3110)
        - 减少 Sink 模块锁冲突 [#2760](https://github.com/pingcap/tiflow/pull/2760)
        (dup) - 修复当扫描存量数据耗时过长时，可能由于 TiKV 进行 GC 而导致存量数据扫描失败的问题 [#2470](https://github.com/pingcap/tiflow/issues/2470)
        (dup) - 修复当发生 ErrGCTTLExceeded 错误时，changefeed 不快速失败的问题 [#3111](https://github.com/pingcap/tiflow/issues/3111)
        (dup) - 为 EtcdWorker 添加 tick 频率限制，防止 PD 的 etcd 写入次数过于频繁影响 PD 服务 [#3112](https://github.com/pingcap/tiflow/issues/3112)
        - 支持消息 Batch 操作减少 EtcdWorker tick [3112](https://github.com/pingcap/tiflow/issues/3112)
        (dup) - 修复在容器环境中 OOM 的问题 [#1798](https://github.com/pingcap/tiflow/issues/1798)
        - Kafka sink 模块支持默认的元数据获取超时时间 config.Metadata.Timeout [#3352](https://github.com/pingcap/tiflow/issues/3352)
        - Kafka sink 模块设置 `MaxMessageBytes` 默认值为 1MB [#3081](https://github.com/pingcap/tiflow/issues/3081)
        - 增加更多 Promethous 和 grafana 监控告警参数，包括 "no owner alert" [#3834](https://github.com/pingcap/tiflow/pull/3834), "mounter row", "table sink total row", "buffer sink total row" [#1606](https://github.com/pingcap/tiflow/issue/1606), "go gc", "go_max_procs" [#2998](https://github.com/pingcap/tiflow/pull/2998), "cached region" [#2733](https://github.com/pingcap/tiflow/pull/2733).

    + (Backup & Restore) BR

        - 支持 pd request 和 TiKV IO 超时错误重试 [#27787](https://github.com/pingcap/tidb/issues/27787)

## Bug 修复

+ TiDB

    (dup) - 修复 `grant` 和 `revoke` 操作在授予和撤销全局权限时，报 `privilege check fail` 错误的问题 [#29675](https://github.com/pingcap/tidb/issues/29675)
    - 修复 ADD INDEX 在某些场景下 panic 的问题 [#27687](https://github.com/pingcap/tidb/issues/27687)
    - 修复配置项 `enforce-mpp` 在 v5.0.4 中不生效的问题 [#29252](https://github.com/pingcap/tidb/issues/29252)
    (dup) - 修复当 `CASE WHEN` 函数和 `ENUM` 类型一起使用时的崩溃问题 [#29357](https://github.com/pingcap/tidb/issues/29357)
    (dup) - 修复 `microsecond` 函数的向量化表达式版本结果不正确的问题 [#29244](https://github.com/pingcap/tidb/issues/29244)
    (dup) - 修复 `auto analyze` 输出的日志信息不完整的问题 [#29188](https://github.com/pingcap/tidb/issues/29188)
    (dup) - 修复 `hour` 函数在向量化表达式中执行结果错误的问题 [#28643](https://github.com/pingcap/tidb/issues/28643)
    (dup) - 修复当不支持的 `cast` 被下推到 TiFlash 时出现的非预期错误，例如 `tidb_cast to Int32 is not supported` [#23907](https://github.com/pingcap/tidb/issues/23907)
    (dup) - 修复 MPP 节点的可用性检测在某些边界场景中无法工作的问题 [#3118](https://github.com/pingcap/tics/issues/3118)
    (dup) - 修复分配 `MPP task ID` 时出现 `DATA RACE` 的问题 [#27952](https://github.com/pingcap/tidb/issues/27952)
    (dup) - 修复删除空的 `dual table` 后 MPP 查询出现 `index out of range` 报错的问题 [#28250](https://github.com/pingcap/tidb/issues/28250)
    - 修复并行插入无效时间类型值时，TiDB panic 的问题 [#25393](https://github.com/pingcap/tidb/issues/25393)
    - 修复查询在 MPP 模式下，报错 `can not found column in Schema column` 的问题 [#28147](https://github.com/pingcap/tidb/pull/28147)
    (dup) - 修复 TiDB 在 TiFlash 关闭时可能出现 panic 的问题 [#28096](https://github.com/pingcap/tidb/issues/28096)
    - 修复优化器在进行 join reorder 优化时，报错 `index out of range` 的问题 [#24095](https://github.com/pingcap/tidb/issues/24095).
    (dup) - 修复当 `ENUM` 类型作为 `IF` 或 `CASE WHEN` 等控制函数的参数时，返回结果不正确的问题 [#23114](https://github.com/pingcap/tidb/issues/23114)
    - 修复 `concat(ifnull(time(3))` 计算结果出错的问题 [#29498](https://github.com/pingcap/tidb/issues/29498)
    - 修复 `greatest/least` 表达式在入参包含无符号整型时，计算结果出错的问题 [#30101](https://github.com/pingcap/tidb/issues/30101)
    - 修复当 SQL 中存在 json 类型列 与 char 类型列 join 时，SQL 出错的问题 [#29401](https://github.com/pingcap/tidb/issues/29401)
    - 修复 update 语句未更新索引处理优化，可能导致数据索引不一致的问题 [#30410](https://github.com/pingcap/tidb/issues/30410)
    - 修复窗口函数在使用事务时，计算结果与不使用事务不一样的问题 [#29947](https://github.com/pingcap/tidb/issues/29947)
    - 修复 SQL 形如`cast(integer as char) union string` 计算结果出错的问题 [#29513](https://github.com/pingcap/tidb/issues/29513)
    (dup) - 修复将 `Decimal` 转为 `String` 时长度信息错误的问题 [#29417](https://github.com/pingcap/tidb/issues/29417)
    - 修复使用 NATURAL JOIN 时，报错 `Column 'col_name' in field list is ambiguous` 的问题 [#25041](https://github.com/pingcap/tidb/issues/25041)
    (dup) - 修复由于 `tidb_enable_vectorized_expression` 设置的值不同（`on` 或 `off`）导致 `GREATEST` 函数返回结果不一致的问题 [#29434](https://github.com/pingcap/tidb/issues/29434)
    (dup) - 修复在某些情况下 Planner 可能缓存无效 `join` 计划的问题 [#28087](https://github.com/pingcap/tidb/issues/28087)
    - 修复 SQL 在 join 上计算聚合函数时，报错 `index out of range [1] with length 1` 的问题 [#1978](https://github.com/pingcap/tics/issues/1978)

+ TiKV

    - 修复某个 TiKV 节点停机导致 Resolve Timestamp 进度落后的问题 [#11351](https://github.com/tikv/tikv/issues/11351)
    (dup) - 修复 Raft client 中 batch 消息过大的问题 [#9714](https://github.com/tikv/tikv/issues/9714)
    (dup) - 修复在极端情况下同时进行 Region Merge、ConfChange 和 Snapshot 时，TiKV 会出现 Panic 的问题 [#11475](https://github.com/tikv/tikv/issues/11475)
    - 修复逆序范围查询时没有正确读到内存锁的问题 [#11440](https://github.com/tikv/tikv/issues/11440)
    (dup) - 修复 Decimal 除法计算的结果为 0 时符号为负的问题 [#29586](https://github.com/pingcap/tidb/issues/29586)
    - 修复历史版本回收任务堆积导致的内存耗尽问题  [#11410](https://github.com/tikv/tikv/issues/11410)
    - 修复监控项  "gRPC average duration by-instance" 的错误表达式导致该监控不显示的问题. [#11299](https://github.com/tikv/tikv/issues/11299)
    - 修复 label 泄漏导致 OOM 的问题. [#11195](https://github.com/tikv/tikv/issues/11195)
    - 修复 CDC 因为缺失下游而宕机的问题. [#11123](https://github.com/tikv/tikv/issues/11123)
    - 修复 CDC 因为增量同步请求过于频繁导致的 `Congest` 错误. [#11082](https://github.com/tikv/tikv/issues/11082)
    - 修复消息队列满了导致 raft 连接断开的问题  [#11047](https://github.com/tikv/tikv/issues/11047)
    - 修复 Lightning 导入数据期间 TiKV 因为文件不存在而宕机的问题 [#10438](https://github.com/tikv/tikv/issues/10438)
    - 修复比较有符号与无符号的 int64 的 Max 与 Min 函数的错误 [#10158](https://github.com/tikv/tikv/issues/10158)
    - 修复从副本从主副本获取快照后未能正确修改元信息导致 TiKV 节点宕机的问题。  [#10225](https://github.com/tikv/tikv/issues/10225)
    - 修复 backup 线程池泄漏的问题 [#10287](https://github.com/tikv/tikv/issues/10287)
    - 修复将不合法字符串转化为浮点数的问题 [#23322](https://github.com/pingcap/tidb/issues/23322)

+ PD

    - 修复在某些情况下 TiKV 缩容引起 PD panic 的问题 [#4344](https://github.com/tikv/pd/issues/4344)
    - 修复 Operator 被 Down Store 阻塞的问题 [#3353](https://github.com/tikv/pd/issues/3353)
    - 修复 PD 掉 Leader 后不能立刻发起选举的问题 [#3936](https://github.com/tikv/pd/issues/3936)
    - 修复 `evict-leader-scheduler` 不能调度含有不健康副本的 Region 的问题 [#4093](https://github.com/tikv/pd/issues/4093)
    - 修复 Down Store 的 Remove Peer 速度受限问题[#4090](https://github.com/tikv/pd/issues/4090)
    - 修复当 Region 心跳低于60秒导致热点 Cache 不能清空的问题 [#4390](https://github.com/tikv/pd/issues/4390)

+ TiFlash

    - 修复当在同时使用且扩大主键列类型时，潜在的数据不一致问题。
    - 修复当 ARM 架构的机器在使用系统的 libnsl.so 编译 TiFlash 时的错误，修改 INSTALL_DIR 编译 libnsl.so 的选项。
    - 修复 TiFlash 统计面板中的 store size 不准确的问题，当 PageStorage 中类型为 checkpoint 的文件删除时，没有减少空间。
    - 修复当 PageStorage GC 时会误删新创建的 PageFile 导致的异常。
    - 修复当用户更新 TiFlash 版本后，同步表时发生的异常。
    - 修复当查询被取消时，TiFlash 偶发的崩溃问题。
    - 修复在 substringUTF8 中的常数异常。
    - 当 DAG 请求失败后，加了一个重试 DAG 请求。
    - 修复当查询带了 where <string> 会变成 int 类型的导致查询结构出错的问题。
    - 修复 main_capacity_quota_ 变量的检查问题。
    - 修复在 TiFlash 与 TiDB/TiKV 之间，关于 CastStringAsDecimal 行为不一致的问题。
    - 修复 Nullable(Int64) 与 Int64 类型不一致的异常，同步表后以避免类型不一致。
    - 修复列类型为 Nullable(Nothing) 导致的异常。
    - 修复 Decimal 类型比较时，可能导致数据溢出并比较失败的问题。

+ Tools

    + TiCDC

        - 修复分区表没有唯一索引时无法复制下发表数据问题 [#2834](https://github.com/pingcap/tiflow/issues/2834)
        - 修复 cdc cli 接收到非预期参数时截断用户参数，导致用户输入数据丢失问题 [#2303](https://github.com/pingcap/tiflow/issues/2303)
        - 修复 cdc 调度逻辑过早调用表问题 [#2625](https://github.com/pingcap/tiflow/issues/2625)
        - 修复 Kafka asyncClient 出错导致的 Kafka_producer 死锁问题 [#2978](https://github.com/pingcap/tiflow/issues/2978)
        - 修复 MQ sink 模块不支持非 binary json 类型列解析 [#2758](https://github.com/pingcap/tiflow/issues/2758)
        - 修复 Kafka sink 模块因为 `max-message-size` 参数过大导致的消息无法发送问题 [#2962](https://github.com/pingcap/tiflow/issues/2962)
        - 修复 TiKV 发生 region merge 导致的锁解析逻辑无法触发问题 [#3061](https://github.com/pingcap/tiflow/issues/3061)
        - 修复 region 重复请求问题[#2386](https://github.com/pingcap/tiflow/issues/2386)
        - 修复 TiKV 崩溃或者强制重启时出现的 region 异常丢失问题 [#3288](https://github.com/pingcap/tiflow/issues/3288)
        - 修复 changefeed checkpoint lag 监控指标出现负值的问题 [#3010](https://github.com/pingcap/tiflow/issues/3010)
        - 修复 MySQL sink 模块出现死锁时告警过于频繁问题 [#2706](https://github.com/pingcap/tiflow/issues/2706)
        - 修复 Avro sink 模块不支持 json type 列类型解析 [#3624](https://github.com/pingcap/tiflow/issues/3624)
        - 修复 TiKV 重启时 cdc 读取到错误的元数据快照问题 [#2603](https://github.com/pingcap/tiflow/issues/2603)
        - 修复过多 DDL 导致的 OOM 问题和元数据 GC 逻辑异常问题 [#3174](https://github.com/pingcap/tiflow/issues/3174)
        - 修复 Canal 和 Maxwell 协议没有自动开启 old value 选项问题 [#3676](https://github.com/pingcap/tiflow/issues/3676)
        - 修复 cdc server 在一些 RHEL 系统(6.8, 6.9 etc)上运行出现的时区错误问题.  [#3584](https://github.com/pingcap/tiflow/issues/3584)
        - 修复 Kafka sink 模块监控变量 txn_batch_size 不准确问题 [#3431](https://github.com/pingcap/tiflow/issues/3431)
        - 修复 Kafka sink 模块当用户关闭 auto-create-topic 选项时没有检查分区数问题 [#3337](https://github.com/pingcap/tiflow/issues/3337)
        - 修复 Kafka message 过大导致的 broker 错误问题. [#3337](https://github.com/pingcap/tiflow/issues/3337)
        - 修复 EtcdWorker row 监控参数错误问题. [#4000](https://github.com/pingcap/tiflow/pull/4000)
        - 修复没有任何任务时 tikv_cdc_min_resolved_ts_no_change_for_1m 告警规则持续告警问题 [#11017](https://github.com/tikv/tikv/issues/11017)
        - 修复 cdc 和 TiKV 出现的 gPRC 连接阻塞导致增量扫慢的问题 [#3110](https://github.com/pingcap/tiflow/issues/3110)

    + (Backup & Restore) BR

        - 修复 Grpc 错误没有重试问题 [#27421](https://github.com/pingcap/tidb/issues/27421)
        - 修复使用了 expression index 的表使用本地 backend 导入时出现错误问题. [#1404](https://github.com/pingcap/br/issues/1404)
        - 修复 BR 中平均速度不准确的问题 [#1405](https://github.com/pingcap/br/issues/1405)

    + Dumpling

        - 修复 dumping 包含 primary/unique key 表时出现的过慢问题. [#29386](https://github.com/pingcap/tidb/issues/29386)