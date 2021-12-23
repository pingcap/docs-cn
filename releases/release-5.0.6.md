---
title: TiDB 5.0.6 Release Notes
---

# TiDB 5.0.6 Release Notes

发版日期：2021 年 12 月 28 日

TiDB 版本：5.0.6

## 兼容性更改

+ Tools

    + TiCDC

        - cdc server 命令错误输出从标准输出改成标准错误. [#3875](https://github.com/pingcap/tiflow/pull/3875)

## 提升改进

+ TiDB

    - 优化乐观事务写入冲突死锁情况下的回滚流程，降低阻塞延迟 [#11148](https://github.com/tikv/tikv/issues/11148)
    - 避免 MPP 查询时候的日志 `invalid cop task execution summaries length`，以防用户疑惑 [#28262](https://github.com/pingcap/tidb/pull/28262)
    - 优化 Coprocessor 的 debug 日志，在遇到锁时，打印语句内容，提高问题定位的效率 [#27718](https://github.com/pingcap/tidb/issues/27718)

+ TiKV

    - 为 raft 日志回收模块增加了更多监控以定位问题. [#11374](https://github.com/tikv/tikv/issues/11374)
    - 折叠了部分 Storage 相关的不常用监控 [#11001](https://github.com/tikv/tikv/pull/11001)
    - 将插入 SST 文件时的校验操作移动到了 import 线程池以提高 SST 文件插入速度. [#11239](https://github.com/tikv/tikv/issues/11239)

+ PD

    - 在 PD 切换 Leader 后加速调度器退出 [#4146](https://github.com/tikv/pd/issues/4146)
    - 通过允许空 Region 调度和修复配置的方式使 scatter-range-scheduler运行更好 [#4116](https://github.com/tikv/pd/pull/4116)

+ Tools

    + TiCDC

        - 优化 TiKV 重启时限速控制逻辑 [#3110](https://github.com/pingcap/tiflow/issues/3110)
        - 减少 Sink 模块锁冲突 [#2760](https://github.com/pingcap/tiflow/pull/2760)
        - 向 TiKV 注册的 GC safepoint TTL 延迟至1小时，有效支持增量扫时间过长的任务 [#2470](https://github.com/pingcap/tiflow/issues/2470)
        - 出现 ErrGCTTLExceeded 错误时支持快速失败 [#3111](https://github.com/pingcap/tiflow/issues/3111)
        - 增加限速逻辑控制 EtcdWorker tick 频率 [#3268](https://github.com/pingcap/tiflow/pull/3268)
        - 支持消息 Batch 操作减少 EtcdWorker tick [#3750](https://github.com/pingcap/tiflow/issues/3750)
        - Unified sorter 组件支持 cgroup 限制，控制资源消耗 [#3441](https://github.com/pingcap/tiflow/pull/3441)
        - Kafka sink 模块支持默认的元数据获取超时时间 config.Metadata.Timeout [#3539](https://github.com/pingcap/tiflow/pull/3539)
        - Kafka sink 模块设置 `MaxMessageBytes` 默认值为 1MB [#3081](https://github.com/pingcap/tiflow/issues/3081)
        - 增加更多 Promethous 和 grafana 监控告警参数，包括 "no owner alert" [#3834](https://github.com/pingcap/tiflow/pull/3834), "mounter row" [#2830](https://github.com/pingcap/tiflow/pull/2830), "table sink total row" [#2830](https://github.com/pingcap/tiflow/pull/2830), "buffer sink total row" [#2830](https://github.com/pingcap/tiflow/pull/2830), "go gc" [#2998](https://github.com/pingcap/tiflow/pull/2998), "go_max_procs" [#2998](https://github.com/pingcap/tiflow/pull/2998), "cached region" [#2733](https://github.com/pingcap/tiflow/pull/2733).

    + (Backup & Restore) BR

        - 支持 pd request 和 TiKV IO 超时错误重试 [#1436](https://github.com/pingcap/br/pull/1436)

## Bug 修复

+ TiDB

    - 修复在 grant/revoke 语句中，使用全局标识符 `*.*` 报错的问题 [#29675](https://github.com/pingcap/tidb/issues/29675)
    - 修复 ADD INDEX 在某些场景下 panic 的问题 [#27687](https://github.com/pingcap/tidb/issues/27687)
    - 修复配置项 `enforce-mpp` 在 v5.0.4 中不生效的问题 [#29252](https://github.com/pingcap/tidb/issues/29252)
    - 修复 `case-when` 表达式在入参为 `enum` 类型时 panic 的问题 [#29357](https://github.com/pingcap/tidb/issues/29357)
    - 修复 `microsecond` 表达式在向量化模式下，计算结果出错的问题 [#29244](https://github.com/pingcap/tidb/issues/29244)
    - 修复 auto analyze 失败时，日志中未记录 SQL 内容的问题 [#29188](https://github.com/pingcap/tidb/issues/29188)
    - 修复 `hour` 表达式在向量化模式下，计算结果出错的问题  [#28643](https://github.com/pingcap/tidb/issues/28643)
    - 修复查询在 MPP 模式下，报错 `tidb_cast to Int32 is not supported` 的问题 [#23907](https://github.com/pingcap/tidb/issues/23907)
    - 修复在一些临界情况下, MPP 节点可用性检测失效的问题 [#3118](https://github.com/pingcap/tics/issues/3118)
    - 修复分配 MPP 任务 id 时可能出现的 data-race 问题 [#27952](https://github.com/pingcap/tidb/issues/27952)
    - 修复 SQL 中包含 `Union` 且运行在 MPP 模式时报错 `index out of range [-1]` 的问题 [#28250](https://github.com/pingcap/tidb/issues/28250)
    - 修复并行插入无效时间类型值时，TiDB panic 的问题 [#25393](https://github.com/pingcap/tidb/issues/25393)
    - 修复查询在 MPP 模式下，报错 `can not found column in Schema column` 的问题 [#28147](https://github.com/pingcap/tidb/pull/28147)
    - 修复在 TiFlash 停机时，TiDB 可能会 panic 的问题 [#28096](https://github.com/pingcap/tidb/issues/28096)
    - 修复优化器在进行 join reorder 优化时，报错 `index out of range` 的问题 [#24095](https://github.com/pingcap/tidb/issues/24095).
    - 修复 `if`,`case-when`,`elt` 等表达式在入参为 enum 类型时，结果出错的问题 [#23114](https://github.com/pingcap/tidb/issues/23114)
    - 修复 `concat(ifnull(time(3))` 计算结果出错的问题 [#29498](https://github.com/pingcap/tidb/issues/29498)
    - 修复 `greatest/least` 表达式在入参包含无符号整型时，计算结果出错的问题 [#30101](https://github.com/pingcap/tidb/issues/30101)
    - 修复当 SQL 中存在 json 类型列 与 char 类型列 join 时，SQL 出错的问题 [#29401](https://github.com/pingcap/tidb/issues/29401)
    - 修复 update 语句未更新索引处理优化，可能导致数据索引不一致的问题 [#30410](https://github.com/pingcap/tidb/issues/30410)
    - 修复窗口函数在使用事务时，计算结果与不使用事务不一样的问题 [#29947](https://github.com/pingcap/tidb/issues/29947)
    - 修复 SQL 形如`cast(integer as char) union string` 计算结果出错的问题 [#29513](https://github.com/pingcap/tidb/issues/29513)
    - 修复 `concat(decimal_col)` 结果出错的问题 [#29417](https://github.com/pingcap/tidb/issues/29417)
    - 修复使用 NATURAL JOIN 时，报错 `Column 'col_name' in field list is ambiguous` 的问题 [#25041](https://github.com/pingcap/tidb/issues/25041)
    - 修复 `greatest` 表达式在开启及关闭 `tidb_enable_vectorized_expression` 时，计算结果不同的问题 [#29434](https://github.com/pingcap/tidb/issues/29434)
    - 修复优化器在某些 join 场景下缓存无效的执行计划的问题 [#28087](https://github.com/pingcap/tidb/issues/28087)
    - 修复 SQL 在 join 上计算聚合函数时，报错 `index out of range [1] with length 1` 的问题 [#1978](https://github.com/pingcap/tics/issues/1978)

+ TiKV

    - 修复某个 TiKV 节点停机导致 Resolve Timestamp 进度落后的问题 [#11351](https://github.com/tikv/tikv/issues/11351)
    - 修复多条日志合并在同一条消息导致消息发送失败的问题。 [#9714](https://github.com/tikv/tikv/issues/9714)
    - 修复 `region` 合并以及发送快照、成员变更这三种情况同时发生时导致 TiKV 宕机的问题 [#11475](https://github.com/tikv/tikv/issues/11475)
    - 修复逆序范围查询时没有正确读到内存锁的问题. [#11440](https://github.com/tikv/tikv/issues/11440)
    - 修复表达式除法计算中得到的结果为零时的正负符号问题 [#29586](https://github.com/pingcap/tidb/issues/29586)
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

        - 修复分区表没有唯一索引时无法复制下发表数据问题 [#2864](https://github.com/pingcap/tiflow/pull/2864)
        - 修复 cdc cli 接收到非预期参数时截断用户参数，导致用户输入数据丢失问题 [#2888](https://github.com/pingcap/tiflow/pull/2888)
        - 修复 cdc 调度逻辑过早调用表问题 [#2625](https://github.com/pingcap/tiflow/issues/2625)
        - 修复 Kafka asyncClient 出错导致的 Kafka_producer 死锁问题 [#3016](https://github.com/pingcap/tiflow/pull/3016)
        - 修复 MQ sink 模块不支持非 binary json 类型列解析 [#2758](https://github.com/pingcap/tiflow/issues/2758)
        - 修复 Kafka sink 模块因为 `max-message-size` 参数过大导致的消息无法发送问题 [#2962](https://github.com/pingcap/tiflow/issues/2962)
        - 修复 TiKV 发生 region merge 导致的锁解析逻辑无法触发问题 [#3061](https://github.com/pingcap/tiflow/issues/3061)
        - 修复 region 重复请求问题[#2386](https://github.com/pingcap/tiflow/issues/2386)
        - 修复 TiKV 崩溃或者强制重启时出现的 region 异常丢失问题 [#3288](https://github.com/pingcap/tiflow/issues/3288)
        - 修复 changefeed checkpoint lag 监控指标出现负值的问题 [#3010](https://github.com/pingcap/tiflow/issues/3010)
        - 修复 MySQL sink 模块出现死锁时告警过于频繁问题 [#2706](https://github.com/pingcap/tiflow/issues/2706)
        - 修复 Avro sink 模块不支持 json type 列类型解析 [#3624](https://github.com/pingcap/tiflow/issues/3624)
        - 修复 TiKV 重启时 cdc 读取到错误的元数据快照问题 [#2603](https://github.com/pingcap/tiflow/issues/2603)
        - 修复过多 DDL 导致的 OOM 问题和元数据 GC 逻辑异常问题 [#3275](https://github.com/pingcap/tiflow/pull/3275)
        - 修复 Canal 和 Maxwell 协议没有自动开启 old value 选项问题 [#3676](https://github.com/pingcap/tiflow/issues/3676)
        - 修复 cdc server 在一些 RHEL 系统(6.8, 6.9 etc)上运行出现的时区错误问题.  [#3584](https://github.com/pingcap/tiflow/issues/3584)
        - 修复 Kafka sink 模块监控变量 txn_batch_size 不准确问题 [#3820](https://github.com/pingcap/tiflow/pull/3820)
        - 修复 Kafka sink 模块当用户关闭 auto-create-topic 选项时没有检查分区数问题 [#3337](https://github.com/pingcap/tiflow/issues/3337)
        - 修复 Kafka message 过大导致的 broker 错误问题. [#3337](https://github.com/pingcap/tiflow/issues/3337)
        - 修复 EtcdWorker row 监控参数错误问题. [#4000](https://github.com/pingcap/tiflow/pull/4000)
        - 修复没有任何任务时 tikv_cdc_min_resolved_ts_no_change_for_1m 告警规则持续告警问题 [#11017](https://github.com/tikv/tikv/issues/11017)
        - 修复 cdc 和 TiKV 出现的 gPRC 连接阻塞导致增量扫慢的问题 [#3110](https://github.com/pingcap/tiflow/issues/3110)

    + (Backup & Restore) BR

        - 修复 Grpc 错误没有重试问题 [#1438](https://github.com/pingcap/br/pull/1438)
        - 修复使用了 expression index 的表使用本地 backend 导入时出现错误问题. [#1404](https://github.com/pingcap/br/issues/1404)
        - 修复 BR 中平均速度不准确的问题 [#1405](https://github.com/pingcap/br/issues/1405)

    + Dumpling

        - 修复 dumping 包含 primary/unique key 表时出现的过慢问题. [#29386](https://github.com/pingcap/tidb/issues/29386)