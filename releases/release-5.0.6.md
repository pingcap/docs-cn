---
title: TiDB 5.0.6 Release Notes
---

# TiDB 5.0.6 Release Notes

发版日期：2021 年 12 月 31 日

TiDB 版本：5.0.6

## 兼容性更改

+ Tools

    + TiCDC

        - 将 cdc server 命令的错误输出从标准输出 (stdout) 改为标准错误 (stderr) [#3133](https://github.com/pingcap/tiflow/issues/3133)
        - 将 Kafka sink 模块的 `max-message-bytes` 默认值设置为 `10M` [#3081](https://github.com/pingcap/tiflow/issues/3081)
        - 将 Kafka Sink `partition-num` 的默认值改为 3，使 TiCDC 更加平均地分发消息到各个 Kafka partition [#3337](https://github.com/pingcap/tiflow/issues/3337)

## 提升改进

+ TiDB

    - 当 coprocessor 遇到锁时，在调试日志中显示受影响的 SQL 语句帮助诊断问题 [#27718](https://github.com/pingcap/tidb/issues/27718)

+ TiKV

    - 将插入 SST 文件时的校验操作从 Apply 线程池移动到 Import 线程池，从而提高 SST 文件的插入速度 [#11239](https://github.com/tikv/tikv/issues/11239)
    - 在 Raft 日志垃圾回收模块中添加了更多监控指标，从而定位该模块中出现的性能问题 [#11374](https://github.com/tikv/tikv/issues/11374)
    - 折叠了 Grafana Dashboard 中与 Storage 相关的不常用的监控指标 [#11681](https://github.com/tikv/tikv/issues/11681)

+ PD

    - 优化调度器退出的速度 [#4146](https://github.com/tikv/pd/issues/4146)
    - 通过允许 `scatter-range-scheduler` 调度器调度空 Region 和修复该调度器的配置，使该调度器的调度结果更加均匀 [#4497](https://github.com/tikv/pd/issues/4497)
    - 允许 Evict Leader 调度器调度拥有不健康副本的 Region [#4093](https://github.com/tikv/pd/issues/4093)

+ Tools

    + TiCDC

        - 优化 TiKV 重新加载时的速率限制控制，缓解 changefeed 初始化时 gPRC 的拥堵问题 [#3110](https://github.com/pingcap/tiflow/issues/3110)
        - 为 EtcdWorker 添加 tick 频率限制，防止 PD 的 etcd 写入次数过于频繁影响 PD 服务 [#3112](https://github.com/pingcap/tiflow/issues/3112)
        - Kafka sink 模块添加默认的元数据获取超时时间配置 (`config.Metadata.Timeout`) [#3352](https://github.com/pingcap/tiflow/issues/3352)
        - 将参数 `max-message-bytes` 的默认值设置为 `10M`，减少 Kafka 不能发送消息的概率 [#3081](https://github.com/pingcap/tiflow/issues/3081)
        - 增加更多 Prometheus 和 Grafana 监控告警参数，包括 `no owner alert`、`mounter row`、`table sink total row` 和 `buffer sink total row` [#4054](https://github.com/pingcap/tiflow/issues/4054) [#1606](https://github.com/pingcap/tiflow/issues/1606)

    + Backup & Restore (BR)

        - 遇到 PD 请求错误或 TiKV I/O 超时错误时重试 BR 任务 [#27787](https://github.com/pingcap/tidb/issues/27787)
        - 增强恢复的鲁棒性 [#27421](https://github.com/pingcap/tidb/issues/27421)

    + TiDB Lightning

        - 支持导入数据到带有表达式索引或带有基于虚拟生成列的索引的表中 [#1404](https://github.com/pingcap/br/issues/1404)

## Bug 修复

+ TiDB

    - 修复乐观事务冲突可能导致事务相互阻塞的问题 [#11148](https://github.com/tikv/tikv/issues/11148)
    - 修复运行 MPP 查询时出现 `invalid cop task execution summaries length` 相关日志的问题 [#1791](https://github.com/pingcap/tics/issues/1791)
    - 修复 DML 和 DDL 语句并发执行时可能发生 panic 的问题 [#30940](https://github.com/pingcap/tidb/issues/30940)
    - 修复 `grant` 和 `revoke` 操作在授予和撤销全局权限时，报 `privilege check fail` 错误的问题 [#29675](https://github.com/pingcap/tidb/issues/29675)
    - 修复在某些场景下执行 `ALTER TABLE.. ADD INDEX` 语句时 TiDB panic 的问题 [#27687](https://github.com/pingcap/tidb/issues/27687)
    - 修复配置项 `enforce-mpp` 在 v5.0.4 中不生效的问题 [#29252](https://github.com/pingcap/tidb/issues/29252)
    - 修复当 `CASE WHEN` 函数和 `ENUM` 类型一起使用时的崩溃问题 [#29357](https://github.com/pingcap/tidb/issues/29357)
    - 修复 `microsecond` 函数的向量化表达式版本结果不正确的问题 [#29244](https://github.com/pingcap/tidb/issues/29244)
    - 修复 `auto analyze` 输出的日志信息不完整的问题 [#29188](https://github.com/pingcap/tidb/issues/29188)
    - 修复 `hour` 函数在向量化表达式中执行结果错误的问题 [#28643](https://github.com/pingcap/tidb/issues/28643)
    - 修复当不支持的 `cast` 被下推到 TiFlash 时出现的非预期错误，例如 `tidb_cast to Int32 is not supported` [#23907](https://github.com/pingcap/tidb/issues/23907)
    - 修复 MPP 节点的可用性检测在某些边界场景中无法工作的问题 [#3118](https://github.com/pingcap/tics/issues/3118)
    - 修复分配 `MPP task ID` 时出现 `DATA RACE` 的问题 [#27952](https://github.com/pingcap/tidb/issues/27952)
    - 修复删除空的 `dual table` 后 MPP 查询出现 `index out of range` 报错的问题 [#28250](https://github.com/pingcap/tidb/issues/28250)
    - 修复并行插入无效日期类型值时，TiDB panic 的问题 [#25393](https://github.com/pingcap/tidb/issues/25393)
    - 修复在 MPP 模式下查询时，报 `can not found column in Schema column` 错误的问题 [#30980](https://github.com/pingcap/tidb/issues/30980)
    - 修复 TiDB 在 TiFlash 关闭时可能出现 panic 的问题 [#28096](https://github.com/pingcap/tidb/issues/28096)
    - 修复优化器在进行 join reorder 优化时，报 `index out of range` 错误的问题 [#24095](https://github.com/pingcap/tidb/issues/24095)
    - 修复当 `ENUM` 类型作为 `IF` 或 `CASE WHEN` 等控制函数的参数时，返回结果不正确的问题 [#23114](https://github.com/pingcap/tidb/issues/23114)
    - 修复 `CONCAT(IFNULL(TIME(3))` 计算结果出错的问题 [#29498](https://github.com/pingcap/tidb/issues/29498)
    - 修复当 `GREATEST` 和 `LEAST`  函数传入无符号整型值时，计算结果出错的问题 [#30101](https://github.com/pingcap/tidb/issues/30101)
    - 修复当 SQL 语句中存在 JSON 类型列与 `CHAR` 类型列连接时，SQL 出错的问题 [#29401](https://github.com/pingcap/tidb/issues/29401)
    - 修复错误使用 lazy existence 检查和 untouched key optimization 可能导致数据索引不一致的问题 [#30410](https://github.com/pingcap/tidb/issues/30410)
    - 修复窗口函数在使用事务时，计算结果与不使用事务时的计算结果不一致的问题 [#29947](https://github.com/pingcap/tidb/issues/29947)
    - 修复 SQL 语句中包含 `cast(integer as char) union string` 时计算结果出错的问题 [#29513](https://github.com/pingcap/tidb/issues/29513)
    - 修复将 `Decimal` 转为 `String` 时长度信息错误的问题 [#29417](https://github.com/pingcap/tidb/issues/29417)
    - 修复 SQL 语句中带有 NATURAL JOIN 时，意外报错 `Column 'col_name' in field list is ambiguous` 的问题 [#25041](https://github.com/pingcap/tidb/issues/25041)
    - 修复由于 `tidb_enable_vectorized_expression` 设置的值不同（`on` 或 `off`）导致 `GREATEST` 函数返回结果不一致的问题 [#29434](https://github.com/pingcap/tidb/issues/29434)
    - 修复在某些情况下 Planner 可能缓存无效 `join` 计划的问题 [#28087](https://github.com/pingcap/tidb/issues/28087)
    - 修复在某些情况下 SQL 语句在 join 结果上计算聚合函数时，报错 `index out of range [1] with length 1` 的问题 [#1978](https://github.com/pingcap/tics/issues/1978)

+ TiKV

    - 修复某个 TiKV 节点停机会导致 Resolved Timestamp 进度落后的问题 [#11351](https://github.com/tikv/tikv/issues/11351)
    - 修复 Raft client 中 batch 消息过大的问题 [#9714](https://github.com/tikv/tikv/issues/9714)
    - 修复在极端情况下同时进行 Region Merge、ConfChange 和 Snapshot 时，TiKV 会出现 Panic 的问题 [#11475](https://github.com/tikv/tikv/issues/11475)
    - 修复逆序扫表时 TiKV 无法正确读到内存锁的问题 [#11440](https://github.com/tikv/tikv/issues/11440)
    - 修复 Decimal 除法计算的结果为 0 时符号为负的问题 [#29586](https://github.com/pingcap/tidb/issues/29586)
    - 修复垃圾回收任务的堆积可能会导致 TiKV 内存耗尽的问题 [#11410](https://github.com/tikv/tikv/issues/11410)
    - 修复 TiKV 监控项中实例级别 gRPC 的平均延迟时间不准确的问题 [#11299](https://github.com/tikv/tikv/issues/11299)
    - 修复因统计线程监控数据导致的内存泄漏 [#11195](https://github.com/tikv/tikv/issues/11195)
    - 修复在缺失下游数据库时出现 TiCDC Panic 的问题 [#11123](https://github.com/tikv/tikv/issues/11123)
    - 修复因 Congest 错误而导致的 TiCDC 频繁增加 scan 重试的问题 [#11082](https://github.com/tikv/tikv/issues/11082)
    - 修复因 channel 打满而导致的 Raft 断连的问题 [#11047](https://github.com/tikv/tikv/issues/11047)
    - 修复在 TiDB Lightning 导入数据时 TiKV 会因为文件不存在而出现 Panic 的问题 [#10438](https://github.com/tikv/tikv/issues/10438)
    - 修复由于无法在 `Max`/`Min` 函数中正确识别 Int64 是否为有符号整数，导致  `Max`/`Min` 函数的计算结果不正确的问题 [#10158](https://github.com/tikv/tikv/issues/10158)
    - 修复当 TiKV 副本节点获取了快照后，TiKV 会因为无法准确地修改元信息而导致该副本节点宕机的问题 [#10225](https://github.com/tikv/tikv/issues/10225)
    - 修复 backup 线程池泄漏的问题 [#10287](https://github.com/tikv/tikv/issues/10287)
    - 修复将不合法字符串转化为浮点数的问题 [#23322](https://github.com/pingcap/tidb/issues/23322)

+ PD

    - 修复 TiKV 节点缩容后可能导致 Panic 的问题 [#4344](https://github.com/tikv/pd/issues/4344)
    - 修复 Operator 被停止服务的节点阻塞的问题 [#3353](https://github.com/tikv/pd/issues/3353)
    - 修复因 Region syncer 卡住而导致 leader 选举慢的问题 [#3936](https://github.com/tikv/pd/issues/3936)
    - 修复当对宕机的节点进行修复时删除副本的速度会受限的问题 [#4090](https://github.com/tikv/pd/issues/4090)
    - 修复当 Region 心跳低于 60 秒时热点 Cache 不能清空的问题 [#4390](https://github.com/tikv/pd/issues/4390)

+ TiFlash

    - 修复整数类型主键的列类型设置为较大范围后数据可能不一致的问题
    - 修复在某些平台 TiFlash 由于找不到 `libnsl.so` 库而无法启动的问题，比如某些 ARM 平台
    - 修复 TiFlash 的 Store size 统计信息与实际容量不一致的问题
    - 修复 TiFlash 由于 `Cannot open file` 错误而导致的进程失败
    - 修复当 MPP 查询被终止时，TiFlash 偶发的崩溃问题
    - 修复查询报错 `3rd arguments of function substringUTF8 must be constants`
    - 修复由于过多 `OR` 条件导致的查询报错
    - 修复 `where <string>` 查询结果出错的问题
    - 修复在 TiFlash 与 TiDB/TiKV 之间 `CastStringAsDecimal` 行为不一致的问题。
    - 修复由于 "different types: expected Nullable(Int64), got Int64" 错误而导致查询报错的问题
    - 修复由于 "Unexpected type of column: Nullable(Nothing)" 错误而导致的查询报错
    - 修复 `Decimal` 类型比较时，可能导致数据溢出并导致查询失败的问题

+ Tools

    + TiCDC

        - 修复当开启 `force-replicate` 时，可能某些没有有效索引的分区表被忽略的问题 [#2834](https://github.com/pingcap/tiflow/issues/2834)
        - 修复 cdc cli 接收到非预期参数时截断用户参数，导致用户输入数据丢失问题 [#2303](https://github.com/pingcap/tiflow/issues/2303)
        - 修复当写入 Kafka 消息发生错误时，TiCDC 同步任务推进可能停滞的问题 [#2978](https://github.com/pingcap/tiflow/issues/2978)
        - 修复 MQ sink 模块不支持非 binary json 类型列解析 [#2758](https://github.com/pingcap/tiflow/issues/2758)
        - 将参数 `max-message-bytes` 的默认值设置为 `10M`，减少 Kafka 发送过大消息的概率 [#3081](https://github.com/pingcap/tiflow/issues/3081)
        - 修复当上游 TiDB 实例意外退出时，TiCDC 同步任务推进可能停滞的问题 [#3061](https://github.com/pingcap/tiflow/issues/3061)
        - 修复当 TiKV 向同一 Region 发送重复请求时，TiCDC 进程 Panic 的问题 [#2386](https://github.com/pingcap/tiflow/issues/2386)
        - 修复在多个 TiKV 崩溃或强制重启时可能遇到复制中断的问题 [#3288](https://github.com/pingcap/tiflow/issues/3288)
        - 修复监控 checkpoint lag 出现负值的问题 [#3010](https://github.com/pingcap/tiflow/issues/3010)
        - 修复 MySQL sink 模块出现死锁时告警过于频繁的问题 [#2706](https://github.com/pingcap/tiflow/issues/2706)
        - 修复 Avro sink 模块不支持解析 JSON 类型列的问题 [#3624](https://github.com/pingcap/tiflow/issues/3624)
        - 修复 TiKV owner 重启时 TiCDC 从 TiKV 读取到错误的元数据快照的问题 [#2603](https://github.com/pingcap/tiflow/issues/2603)
        - 修复执行 DDL 后的内存泄漏的问题 [#3174](https://github.com/pingcap/tiflow/issues/3174)
        - 修复 Canal 协议下 TiCDC 没有自动开启 `enable-old-value` 选项的问题 [#3676](https://github.com/pingcap/tiflow/issues/3676)
        - 修复 `cdc server` 命令在 Red Hat Enterprise Linux 系统的部分版本（如 6.8、6.9 等）上运行时出现时区错误的问题  [#3584](https://github.com/pingcap/tiflow/issues/3584)
        - 修复当 Kafka 为下游时 `txn_batch_size` 监控指标数据不准确的问题 [#3431](https://github.com/pingcap/tiflow/issues/3431)
        - 修复 tikv_cdc_min_resolved_ts_no_change_for_1m 监控在没有 changefeed 的情况下持续更新的问题 [#11017](https://github.com/tikv/tikv/issues/11017)
        - 修复人为删除 etcd 任务的状态时导致 TiCDC panic 的问题 [#2980](https://github.com/pingcap/tiflow/issues/2980)
        - 修复当发生 ErrGCTTLExceeded 错误时，changefeed 不快速失败的问题 [#3111](https://github.com/pingcap/tiflow/issues/3111)
        - 修复当扫描存量数据耗时过长时，可能由于 TiKV 进行 GC 而导致存量数据扫描失败的问题 [#2470](https://github.com/pingcap/tiflow/issues/2470)
        - 修复在容器环境中 OOM 的问题 [#1798](https://github.com/pingcap/tiflow/issues/1798)

    + Backup & Restore (BR)

        - 修复 BR 中平均速度 (average-speed) 不准确的问题 [#1405](https://github.com/pingcap/br/issues/1405)

    + Dumpling

        - 修复 Dumpling 在导出包含复合主键或唯一约束的表时导出速度过慢的问题 [#29386](https://github.com/pingcap/tidb/issues/29386)
