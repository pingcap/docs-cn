---
title: TiDB 5.2.2 Release Notes
---

# TiDB 5.2.2 Release Notes

发版日期：2021 年 10 月 29 日

TiDB 版本：5.2.2

## 兼容性更改

## 功能增强

## 提升改进

+ TiDB

    - 在调试日志中显示关于 coprocessor 遇到锁的 SQL 语句信息。[#27718](https://github.com/pingcap/tidb/issues/27718)
    - SQL 逻辑层数据备份和恢复时，支持显示备份和恢复数据大小的功能。[#27247](https://github.com/pingcap/tidb/issues/27247)

+ TiKV

    - 简化 L0 层流控算法 [#10879](https://github.com/tikv/tikv/issues/10879)
    - 优化 raft client 错误日志的收集 [#10983](https://github.com/tikv/tikv/pull/10983)
    - 使 TiKV Coprocessor 慢日志只考虑处理请求所花费的时间 [#10841](https://github.com/tikv/tikv/issues/10841)
    - 当 slogger 线程过载且队列已满时，删除日志而不是阻塞线程 [#10841](https://github.com/tikv/tikv/issues/10841)
    - 加入更多的写入查询统计类型 [#10507](https://github.com/tikv/tikv/issues/10507)

+ PD

    - 热点调度器的 QPS 维度支持更多写请求类型 [#3869](https://github.com/tikv/pd/issues/3869)
    - 通过动态调整 Balance Region 调度器的重试上限，优化该调度器的性能 [#3744](https://github.com/tikv/pd/issues/3744)
    - 将 TiDB Dashboard 升级至 v2021.10.08.1 [#4070](https://github.com/tikv/pd/pull/4070)
    - 允许 evict leader 调度器调度拥有不健康副本的 Region [#4093](https://github.com/tikv/pd/issues/4093)
    - 优化收到进程结束信号后调度器的退出速度 [#4146](https://github.com/tikv/pd/issues/4146)

+ Tools

    + TiCDC

        - 将 Kafka sink 配置项默认值由 `MaxMessageBytes` 64MB 改为 1MB，消息因体积过大而被 Kafka Broker 拒收。[#3104](https://github.com/pingcap/ticdc/pull/3104)
        - 降低同步链路中的内存占用 [#3037](https://github.com/pingcap/ticdc/pull/3037) [#2726](https://github.com/pingcap/ticdc/pull/2726) [#2642](https://github.com/pingcap/ticdc/pull/2642)
        - 优化监控项和告警规则，提升了同步链路、内存 GC、存量数据扫描过程的可观测性。[#2735](https://github.com/pingcap/ticdc/pull/2735) [#2828](https://github.com/pingcap/ticdc/pull/2828) [#3000](https://github.com/pingcap/ticdc/pull/3000 [#3035](https://github.com/pingcap/ticdc/pull/3035) [#3026](https://github.com/pingcap/ticdc/pull/3026)
        - 当同步任务状态正常时，不再显示历史上的错误信息，避免误导用户。[#2979](https://github.com/pingcap/ticdc/pull/2979)

## Bug 修复

+ TiDB

    - 修复了 `plan cache` 无法感知 `unsigned` 标志的问题 [#28254](https://github.com/pingcap/tidb/issues/28254)
    - 修复了出现 `out of range` 时 `partition pruning` 出错的问题 [#28233](https://github.com/pingcap/tidb/issues/28233)
    - 修复了在某些情况下可能缓存无效 `join` 计划的问题 [#28087](https://github.com/pingcap/tidb/issues/28087)
    - 修复了 hash 列为 `enum` 时构建错误 `IndexLookUpJoin` 的问题。 [#27893](https://github.com/pingcap/tidb/issues/27893)
    - 修复了批处理客户端在某些罕见情况下回收空闲连接可能会阻塞发送请求的问题。[#28345](https://github.com/pingcap/tidb/pull/28345)
    - 修复了当 Lightning 在目标集群上执行校验失败时的恐慌问题。[#27686](https://github.com/pingcap/tidb/pull/27686)
    - 修复了某些情况下 `date_add` 和 `date_sub` 执行结果错误的问题。[#27232](https://github.com/pingcap/tidb/issues/27232)
    - 修复了 `hour` 函数在向量化表达式中执行结果错误的问题 [#28643](https://github.com/pingcap/tidb/issues/28643)
    - 修复了 MySQL 5.1 和更旧的客户端存在的认证问题 [#27855](https://github.com/pingcap/tidb/issues/27855)
    - 修复了自动分析可能会触发超出指定时间的问题。[#28698](https://github.com/pingcap/tidb/issues/28698)
    - 修复了设置任何会话变量都会使 `tidb_snapshot` 失效的问题。[#28683](https://github.com/pingcap/tidb/pull/28683)
    - 修复了在有大量 `miss-peer region` 的集群中 BR 不可用的问题。” [#27534](https://github.com/pingcap/tidb/issues/27534)
    - 修复了当不支持的 `cast` 被下推到 TiFlash 时出现的错误，如 `tidb_cast to Int32 is not supported`。[#23907](https://github.com/pingcap/tidb/issues/23907)
    - 修复了 `%s value is out of range in '%s'` 错误没有填充 `DECIMAL overflow` 信息的问题。 [#27964](https://github.com/pingcap/tidb/issues/27964)
    - 修复了 MPP 节点的可用性检测在某些边界场景中无法工作的问题。 [#3118](https://github.com/pingcap/tics/issues/3118)
    - 修复了分配 `MPP task ID` 时的 `DATA RACE` 问题。[#27952](https://github.com/pingcap/tidb/issues/27952)
    - 修复了 MPP 查询时删除空的 `dual table` 时出现 `index out of range` 错误的问题。[#28250](https://github.com/pingcap/tidb/issues/28250)
    - 避免运行 MPP 查询时出现误报 `invalid cop task execution summaries length` 相关日志的问题。[#28264](https://github.com/pingcap/tidb/pull/28264)
    - 修复 MPP 查询时出现 `can not found column in Schema column` 报错的问题。[#28149](https://github.com/pingcap/tidb/pull/28149)
    - 修复了 TiDB 在 TiFlash 关闭时可能出现 `panic` 的问题。 [#28096](https://github.com/pingcap/tidb/issues/28096)
    - 移除对基于 3DES 的 TLS 加密套件的支持。[#27859](https://github.com/pingcap/tidb/pull/27859)
    - 修复了 Lightning 前置检查会连接已下线的 TiKV 节点导致导入失败的问题。[#27826](https://github.com/pingcap/tidb/pull/27826)
    - 修复了在导入太多文件到表时预检查花费太多时间的问题。[#27605](https://github.com/pingcap/tidb/issues/27605)
    - 修复了表达式重写时 `between` 推断出错误排序规则的问题。[#27146](https://github.com/pingcap/tidb/issues/27146)
    - 修复了 `group_concat` 函数没有考虑排序规则的问题。[#27429](https://github.com/pingcap/tidb/issues/27429)
    - 修复了 `extract` 函数处理负值时的问题。[#27236](https://github.com/pingcap/tidb/issues/27236)
    - 修复了当设置了 `no_unsigned_subtract` 时创建分区失败的问题。[#26765](https://github.com/pingcap/tidb/issues/26765)
    - 避免在列修剪和聚合下推中使用有副作用的表达式。[#27106](https://github.com/pingcap/tidb/issues/27106)
    - 删除无用的 GRPC 日志。[#27239](https://github.com/pingcap/tidb/pull/27239)
    - 限制有效的 `decimal` 长度以修复精度相关的问题。[28649](https://github.com/pingcap/tidb/pull/28649)
    - 修复了 `plus` 表达式中检查溢出方法出错的问题。[27419](https://github.com/pingcap/tidb/pull/27419)
    - 修复了当导出带有 `new collation` 数据的表的统计信息时报 `data too long` 错误的问题。[27302](https://github.com/pingcap/tidb/pull/27302)
    - 修复 `TIDB_TRX` 中不包含重试事务的问题。[28670](https://github.com/pingcap/tidb/pull/28670)

+ TiKV

    - 修复 Congest 错误导致 CDC 频繁增加 scan 重试的问题 [#11082](https://github.com/tikv/tikv/issues/11082)
    - 修复因 channel 打满而导致的 Raft 断连情况 [#11047](https://github.com/tikv/tikv/issues/11047)
    - 修复 Raft client 中 batch 消息过大的问题 [#9714](https://github.com/tikv/tikv/issues/9714)
    - 修复 `resolved_ts` 中协程泄漏的问题 [#10965](https://github.com/tikv/tikv/issues/10965)
    - 修复当 response 大小超过 4 GiB 时 Coprocessor panic 的问题 [#9012](https://github.com/tikv/tikv/issues/9012)
    - 修复当一个 snapshot 文件无法被 GC 的时 snapshot GC 会缺失 GC snapshot 文件的问题 [#10813](https://github.com/tikv/tikv/issues/10813)
    - 修复当处理 Coprocessor 请求时因超时而导致 Panic 的问题 [#10852](https://github.com/tikv/tikv/issues/10852)

+ PD

    - 修复因超过副本配置数量而导致错误删除带有数据且处于 pending 状态的副本的问题 [#4045](https://github.com/tikv/pd/issues/4045)
    - 修复 PD 未能及时修复 Down Peer 副本的问题 [#4077](https://github.com/tikv/pd/issues/4077)
    - 修复 Scatter Range 调度器无法对空 Region 进行调度的问题 [#4118](https://github.com/tikv/pd/pull/4118)
    - 修复 key manager 占用过多 CPU 的问题 [#4071](https://github.com/tikv/pd/issues/4071)
    - 修复热点调度器变更配置过程中可能存在的数据竞争问题 [#4159](https://github.com/tikv/pd/issues/4159)
    - 修复因  Region syncer 卡住而导致 leader 选举慢的问题 [#3936](https://github.com/tikv/pd/issues/3936) 

+ TiFlash

    - 修复 TiFlash 在部分平台上由于缺失 `nsl` 库而无法启动的问题

+ Tools

    + TiCDC

        - 修复当上游 TiDB 实例意外退出时，TiCDC 同步任务推进可能停滞的问题。[#3061](https://github.com/pingcap/ticdc/issues/3061)
        - 修复 TiCDC 进程 PANIC `tikv reported duplicated request to the same region, which is not expected`。[#3093](https://github.com/pingcap/ticdc/pull/3093)
        - 修复在验证下游 TiDB/MySQL 可用性时导致的无意义的 CPU 消耗。[#3077](https://github.com/pingcap/ticdc/pull/3077)
        - 修复 TiCDC 产生的 Kafka 消息体积不受 `max-message-size` 约束的问题。[#3049](https://github.com/pingcap/ticdc/pull/3049)
        - 修复当写入 Kafka 消息发生错误时，TiCDC 同步任务推进可能停滞的问题。[#3018](https://github.com/pingcap/ticdc/pull/3018)
        - 修复当开启 `force-replicate` 时，可能有些没有有效索引的分区表被非预期的忽略的问题。[#2866](https://github.com/pingcap/ticdc/pull/2866)
        - 修复当扫描存量数据耗时过长时，可能由于 TiKV 进行 GC 而导致存量数据扫描失败的问题。[#2854](https://github.com/pingcap/ticdc/pull/2854)
        - 修复在将某些类型的列编码为 Open Protocol 格式时，TiCDC 进程可能 PANIC `interface conversion: interface {} is string, not []uint8`。[#2784](https://github.com/pingcap/ticdc/pull/2784)
        - 修复在将某些类型的列编码为 Avro 格式时，TiCDC 进程可能 PANIC `interface conversion: interface {} is uint64, not int64`。[#2657](https://github.com/pingcap/ticdc/pull/2657)
    
    + TiDB Binlog

        - 修复当大部分表被过滤掉时，在某些特殊的负载下，checkpoint 不更新的问题。[#1075](https://github.com/pingcap/tidb-binlog/pull/1075)