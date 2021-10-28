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

    - 在调试日志中显示关于 coprocessor 遇到锁的 SQL 语句信息。[#27924](https://github.com/pingcap/tidb/pull/27924)
    - SQL 逻辑层数据备份和恢复时，支持显示备份和恢复数据大小的功能。[#27727](https://github.com/pingcap/tidb/pull/27727)

+ PD

    - 热点调度器 `QPS` 统计维度支持更多写请求类型 [#4028](https://github.com/tikv/pd/pull/4028)
    - 通过动态调整重试上限，优化 `balance region` 调度器的性能 [#4046](https://github.com/tikv/pd/pull/4046)
    - 将 TiDB Dashboard 升级至 v2021.10.08.1 [#4070](https://github.com/tikv/pd/pull/4070)
    - 允许` evict leader` 调度器调度拥有不健康副本的 `region` [#4132](https://github.com/tikv/pd/pull/4132)
    - 优化收到进程结束信号后调度器的退出速度 [#4199](https://github.com/tikv/pd/pull/4199)

+ Tools

    + TiCDC

        - 将 Kafka sink 配置项默认值由 `MaxMessageBytes` 64MB 改为 1MB，消息因体积过大而被 Kafka Broker 拒收。[#3104](https://github.com/pingcap/ticdc/pull/3104)
        - 降低同步链路中的内存占用 [#3037](https://github.com/pingcap/ticdc/pull/3037) [#2726](https://github.com/pingcap/ticdc/pull/2726) [#2642](https://github.com/pingcap/ticdc/pull/2642)
        - 优化监控项和告警规则，提升了同步链路、内存 GC、存量数据扫描过程的可观测性。[#2735](https://github.com/pingcap/ticdc/pull/2735) [#2828](https://github.com/pingcap/ticdc/pull/2828) [#3000](https://github.com/pingcap/ticdc/pull/3000 [#3035](https://github.com/pingcap/ticdc/pull/3035) [#3026](https://github.com/pingcap/ticdc/pull/3026)
        - 当同步任务状态正常时，不再显示历史上的错误信息，避免误导用户。[#2979](https://github.com/pingcap/ticdc/pull/2979)

## Bug 修复

+ TiDB

    - 修复了 `plan cache` 无法感知 `unsigned` 标志的问题 [#28837](https://github.com/pingcap/tidb/pull/28837)
    - 修复了出现 `out of range` 时 `partition pruning` 出错的问题 [#28820](https://github.com/pingcap/tidb/pull/28820)
    - 修复了在某些情况下可能缓存无效 `join` 计划的问题 [#28447](https://github.com/pingcap/tidb/pull/28447)
    - 修复了 hash 列为 `enum` 时构建错误 `IndexLookUpJoin` 的问题。 [#28082](https://github.com/pingcap/tidb/pull/28082)
    - 修复了批处理客户端在某些罕见情况下回收空闲连接可能会阻塞发送请求的问题。[#28345](https://github.com/pingcap/tidb/pull/28345)
    - 修复了当 Lightning 在目标集群上执行校验失败时的恐慌问题。[#27686](https://github.com/pingcap/tidb/pull/27686)
    - 修复了某些情况下 `date_add` 和 `date_sub` 执行结果错误的问题。[#27454](https://github.com/pingcap/tidb/pull/27454)
    - 修复了 `hour` 函数在向量化表达式中执行结果错误的问题 [#28874](https://github.com/pingcap/tidb/pull/28874)
    - 修复了 MySQL 5.1 和更旧的客户端存在的认证问题 [#28734](https://github.com/pingcap/tidb/pull/28734)
    - 修复了自动分析可能会触发超出指定时间的问题。[#28725](https://github.com/pingcap/tidb/pull/28725)
    - 修复了设置任何会话变量都会使 `tidb_snapshot` 失效的问题。[#28683](https://github.com/pingcap/tidb/pull/28683)
    - 修复了在有大量 `miss-peer region` 的集群中 BR 不可用的问题。” [#28680](https://github.com/pingcap/tidb/pull/28680)
    - 修复了当不支持的 `cast` 被下推到 TiFlash 时出现的错误，如 `tidb_cast to Int32 is not supported`。[#28654](https://github.com/pingcap/tidb/pull/28654)
    - 修复了 `%s value is out of range in '%s'` 错误没有填充 `DECIMAL overflow` 信息的问题。 [#28439](https://github.com/pingcap/tidb/pull/28439)
    - 修复了 MPP 节点的可用性检测在某些边界场景中无法工作的问题。 [#28289](https://github.com/pingcap/tidb/pull/28289)
    - 修复了分配 `MPP task ID` 时的 `DATA RACE` 问题。[#28283](https://github.com/pingcap/tidb/pull/28283)
    - 修复了 MPP 查询时删除空的 `dual table` 时出现 `index out of range` 错误的问题。[#28280](https://github.com/pingcap/tidb/pull/28280)
    - 避免运行 MPP 查询时出现误报 `invalid cop task execution summaries length` 相关日志的问题。[#28264](https://github.com/pingcap/tidb/pull/28264)
    - 修复 MPP 查询时出现 `can not found column in Schema column` 报错的问题。[#28149](https://github.com/pingcap/tidb/pull/28149)
    - 修复了 TiDB 在 TiFlash 关闭时可能出现 `panic` 的问题。 [#28140](https://github.com/pingcap/tidb/pull/28140)
    - 移除对基于 3DES 的 TLS 加密套件的支持。[#27859](https://github.com/pingcap/tidb/pull/27859)
    - 修复了 Lightning 前置检查会连接已下线的 TiKV 节点导致导入失败的问题。[#27826](https://github.com/pingcap/tidb/pull/27826)
    - 修复了在导入太多文件到表时预检查花费太多时间的问题。[#27623](https://github.com/pingcap/tidb/pull/27623)
    - 修复了表达式重写时 `between` 推断出错误排序规则的问题。[#27550](https://github.com/pingcap/tidb/pull/27550)
    - 修复了 `group_concat` 函数没有考虑排序规则的问题。[#27530](https://github.com/pingcap/tidb/pull/27530)
    - 修复了 `extract` 函数处理负值时的问题。[#27366](https://github.com/pingcap/tidb/pull/27366)
    - 修复了当设置了 `no_unsigned_subtract` 时创建分区失败的问题。[#27100](https://github.com/pingcap/tidb/pull/27100)
    - 避免在列修剪和聚合下推中使用有副作用的表达式。[#27370](https://github.com/pingcap/tidb/pull/27370)
    - 删除无用的 GRPC 日志。[#27239](https://github.com/pingcap/tidb/pull/27239)
    - 限制有效的 `decimal` 长度以修复精度相关的问题。[28649](https://github.com/pingcap/tidb/pull/28649)
    - 修复了 `plus` 表达式中检查溢出方法出错的问题。[27419](https://github.com/pingcap/tidb/pull/27419)
    - 修复了当导出带有 `new collation` 数据的表的统计信息时报 `data too long` 错误的问题。[27302](https://github.com/pingcap/tidb/pull/27302)
    - 修复 `TIDB_TRX` 中不包含重试事务的问题。[28670](https://github.com/pingcap/tidb/pull/28670)
        
+ PD

    - 修复因为超过副本配置数量而错误删除有数据且处于 `pending` 状态的副本的问题 [#4075](https://github.com/tikv/pd/pull/4075)
    - 修复 `down peer` 无法及时修复的问题 [#4084](https://github.com/tikv/pd/pull/4084)
    - 修复 `scatter range` 调度器无法对空 `region` 进行调度的问题 [#4118](https://github.com/tikv/pd/pull/4118)
    - 修复 `key manager` 占用过多 CPU 的问题 [#4153](https://github.com/tikv/pd/pull/4153)
    - 修复热点调度器变更配置过程中可能存在的数据竞争问题 [#4170](https://github.com/tikv/pd/pull/4170)
    - 修复 `region syncer` 卡住导致 `leader` 选举慢的问题 [#4220](https://github.com/tikv/pd/pull/4220) 

+ TiFlash

    - 修复 TiFlash 在部分平台上由于缺失 `nsl` 库而无法启动的问题

+ Tools

    + TiCDC

        - 修复当上游 TiDB 实例意外退出时，TiCDC 同步任务推进可能停滞的问题。[#3102](https://github.com/pingcap/ticdc/pull/3102)
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