---
title: TiDB 4.0.16 Release Notes
---

# TiDB 4.0.16 Release Notes

发版日期：2021 年 12 月 10 日

TiDB 版本：4.0.16

## 兼容性更改

+ TiKV

    - 当将一个非法的utf8 字符串转为Real类型时，把该字符串中合法的Utf8前缀转成Real类型，而不是直接报错 [#11466](https://github.com/tikv/tikv/issues/11466)

+ Tools

    + TiDB Binlog

        - Drainer: 修复了 Kafka message 大于 1GB 时无法发送到下游的问题。[#1078](https://github.com/pingcap/tidb-binlog/pull/1078)

    + TiCDC

        - 将 Kafka Sink `max-message-bytes` 的默认值改为 1MB。[#2962](https://github.com/pingcap/ticdc/issues/2962)
        - 将 Kafka Sink `partition-num` 的默认值改为 3。[#3337](https://github.com/pingcap/ticdc/issues/3337)

## 提升改进

+ TiKV

    - sst_importer: 当使用BR-Restore或者Lighting-Local-backend时，采用 zstd 算法压缩SST以减小使用空间 [#11469](https://github.com/tikv/tikv/issues/11469)

+ Tools

    + Backup & Restore (BR)

        - 增强恢复的鲁棒性 [#27421](https://github.com/pingcap/tidb/issues/27421)

    + TiCDC

        - 为 EtcdWorker 添加 Tick 频率限制。[#3112](https://github.com/pingcap/ticdc/issues/3112)
        - 优化 TiKV 重新加载时的速率限制控制，并解决 gPRC 的拥堵问题，这可能导致初始化阶段的缓慢。[#3110](https://github.com/pingcap/ticdc/issues/3110)
        - 忽略 changefeed 更新命令的全局标志 [#2803](https://github.com/pingcap/ticdc/issues/2803)
        - 禁止跨主要和次要版本操作 TiCDC 集群。[#3352](https://github.com/pingcap/ticdc/issues/3352)

## Bug fixes

+ TiDB

    - 修复了在统计信息模块的估算代价中，在执行 range 转 point 时，一处由于数值溢出而导致的查询崩溃 [#23625](https://github.com/pingcap/tidb/issues/23625)
    - 修复了 enum 类型作为 `if`, `case when` 等控制函数参数时，返回结果不正确的问题 [#23114](https://github.com/pingcap/tidb/issues/23114)
    - 修复了 `greatest` 函数在开启和关闭向量化表达式时，返回结果不一致的问题 [#29434](https://github.com/pingcap/tidb/issues/29434)
    - 修复了一些 index join 作用在前缀索引上时崩溃的问题 [#24547](https://github.com/pingcap/tidb/issues/24547)
    - (dup) 修复在某些情况下 Planner 可能缓存无效 `join` 计划的问题 [#28087](https://github.com/pingcap/tidb/issues/28087)
    - 修复了当 `sql_mode` 为空时，TiDB 无法插入 `null` 到非 `null` 列的问题 [#11648](https://github.com/pingcap/tidb/issues/11648)
    - 修正了 `greatest`/`least` 函数的返回值类型 [#29019](https://github.com/pingcap/tidb/issues/29019)
    - 修复了`grant` 和 `revoke` 操作在授予全局权限时，报错 'privilege check fail' 的问题 [#29675](https://github.com/pingcap/tidb/issues/29675)
    - 修复 `case when` 函数和 enum 类型一起使用时的一处崩溃 [#29357](https://github.com/pingcap/tidb/issues/29357)
    - 修复 `microsecond` 函数的向量化表达式版本结果不正确的问题 [#29244](https://github.com/pingcap/tidb/issues/29244)
    - (dup) 修复 `hour` 函数在向量化表达式中执行结果错误的问题 [#28643](https://github.com/pingcap/tidb/issues/28643)
    - 修复了乐观事务冲突导致可能事务相互阻塞的问题 [#11148](https://github.com/tikv/tikv/issues/11148)
    - 修复 `auto analyze` 输出日志信息不完整的问题 [#29188](https://github.com/pingcap/tidb/issues/29188)
    - 修复了 `NO_ZERO_IN_DATE` 对默认值不生效的问题 [#26766](https://github.com/pingcap/tidb/issues/26766)
    - 修复了 Grafana 的 Coprocessor Cache 监控面板不显示数据的问题。现在 Grafana 会显示 `hits`/`miss`/`evict` 的数据 [#26338](https://github.com/pingcap/tidb/issues/26338)
    - 修复并发 truncate 相同的分区导致 DDL 卡死的问题 [#26229](https://github.com/pingcap/tidb/issues/26229)
    - 修复 `CONCAT` 函数的参数为负浮点数时，该参数在返回结果中被截断末位数的问题 [#29417](https://github.com/pingcap/tidb/issues/29417)
    - 修复使用 `NATUAL JOIN` 连接多张表时，查询结果中多出一列的问题 [#29481](https://github.com/pingcap/tidb/issues/29481)
    - 修复 `IndexScan` 使用前缀索引时，`TopN` 被错误下推至 `indexPlan` 的问题  [#29711](https://github.com/pingcap/tidb/issues/29711)
    - 修复在 `DOUBLE` 类型的自增列上重试事务会导致数据错误的问题 [#29892](https://github.com/pingcap/tidb/issues/29892)

+ TiKV

    - 修复在极端情况下merge, conf change和snapshot同时发生时出现panic的问题 [#11475](https://github.com/tikv/tikv/issues/11475)
    - 修复decimal除法结果为0时 符号为负的问题 [#29586](https://github.com/pingcap/tidb/issues/29586)
    - 修复不正确的by-instance gGrpc 平均时间 [#11299](https://github.com/tikv/tikv/issues/11299)
    - 修复在缺失downstream时CDC panic的问题[#11123](https://github.com/tikv/tikv/issues/11123)
    - (dup) 修复因 channel 打满而导致的 Raft 断连情况 [#11047](https://github.com/tikv/tikv/issues/11047)
    - 修复在Max/Min 中无法正确识别int64是否为有符号整数从而导致Max/Min结果不正确的问题。[#10158](https://github.com/tikv/tikv/issues/10158)
    - (dup) 修复因 Congest 错误而导致的 CDC 频繁增加 scan 重试的问题 [#11082](https://github.com/tikv/tikv/issues/11082)

+ PD

    - 修复 TiKV 节点缩容后可能导致 Panic 的问题 [#4344](https://github.com/tikv/pd/issues/4344)
    - (dup) 修复因 Region syncer 卡住而导致 leader 选举慢的问题 [#3936](https://github.com/tikv/pd/issues/3936)
    - (dup) 允许 Evict Leader 调度器调度拥有不健康副本的 Region [#4093](https://github.com/tikv/pd/issues/4093)

+ TiFlash

+ Tools

    + TiCDC

        - 修复监控 checkpoint lag 出现负值的问题 [#3010](https://github.com/pingcap/ticdc/issues/3010)
        - 修复在容器环境中 OOM 的问题 [#1798](https://github.com/pingcap/ticdc/issues/1798)
        - 修复在多个 TiKV 崩溃或强制重启时可能遇到复制中断的问题 [#3288](https://github.com/pingcap/ticdc/issues/3288)
        - 修复处理 DDL 后的内存泄漏 [#3174](https://github.com/pingcap/ticdc/issues/3174)
        - 修复当发生 ErrGCTTLExceeded 错误时，changefeed 不快速失败的问题 [#3111](https://github.com/pingcap/ticdc/issues/3111)
        - (dup) 修复当上游 TiDB 实例意外退出时，TiCDC 同步任务推进可能停滞的问题 [#3061](https://github.com/pingcap/ticdc/issues/3061)
        - (dup) 修复当 TiKV 向同一 Region 发送重复请求时，TiCDC 进程 panic 的问题 [#2386](https://github.com/pingcap/ticdc/issues/2386)
        - (dup) 修复 TiCDC 产生的 Kafka 消息体积不受 `max-message-size` 约束的问题 [#2962](https://github.com/pingcap/ticdc/issues/2962)
        - 修复 tikv_cdc_min_resolved_ts_no_change_for_1m 监控在没有 changefeed 的情况下持续启动 [#11017](https://github.com/tikv/tikv/issues/11017)
        - (dup) 修复当写入 Kafka 消息发生错误时，TiCDC 同步任务推进可能停滞的问题 [#2978](https://github.com/pingcap/ticdc/issues/2978)
        - (dup) 修复当开启 `force-replicate` 时，可能某些没有有效索引的分区表被忽略的问题 [#2834](https://github.com/pingcap/ticdc/issues/2834)
        - 修复在创建新的 changefeed 时可能发生的内存泄漏问题 [#2389](https://github.com/pingcap/ticdc/issues/2389)
        - 让 Sink 组件在汇报 resoved ts 时不要跳过 flush 操作 [#3503](https://github.com/pingcap/ticdc/issues/3503)
        - (dup) 修复当扫描存量数据耗时过长时，可能由于 TiKV 进行 GC 而导致存量数据扫描失败的问题 [#2470](https://github.com/pingcap/ticdc/issues/2470)
