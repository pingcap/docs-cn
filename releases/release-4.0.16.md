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

        - drainer: fix kafka message limit problem [#1078](https://github.com/pingcap/tidb-binlog/pull/1078)

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
    - 修复了一个优化器在某些 join 的场景中会缓存无效的查询计划的问题 [#28087](https://github.com/pingcap/tidb/issues/28087)
    - 修复了当 `sql_mode` 为空时，TiDB 无法插入 `null` 到非 `null` 列的问题 [#11648](https://github.com/pingcap/tidb/issues/11648)
    - 修正了 `greatest`/`least` 函数的返回值类型 [#29019](https://github.com/pingcap/tidb/issues/29019)
    - 修复了`grant` 和 `revoke` 操作在授予全局权限时，报错 'privilege check fail' 的问题 [#29675](https://github.com/pingcap/tidb/issues/29675)
    - 修复 `case when` 函数和 enum 类型一起使用时的一处崩溃 [#29357](https://github.com/pingcap/tidb/issues/29357)
    - 修复 `microsecond` 函数的向量化表达式版本结果不正确的问题 [#29244](https://github.com/pingcap/tidb/issues/29244)
    - 修复 `hour` 函数的向量化表达式版本结果不正确的问题 [#28643](https://github.com/pingcap/tidb/issues/28643)
    - 修复了乐观事务冲突导致可能相互阻塞的问题 [#11148](https://github.com/tikv/tikv/issues/11148)
    - 修复 auto analyze 一处日志信息不全 [#29188](https://github.com/pingcap/tidb/issues/29188)
    - 修复了 `NO_ZERO_IN_DATE` 对默认值未生效的问题 [#26766](https://github.com/pingcap/tidb/issues/26766)
    - 修复了 copt-cache 的监控信息，现在在 Grafana 中会显示 hits/miss/evict 的数据 [#26338](https://github.com/pingcap/tidb/issues/26338)
    - 修复并发 truncate 相同的分区导致 DDL 卡死的问题 [#26229](https://github.com/pingcap/tidb/issues/26229)
    - expression: fix wrong flen when cast decimal to string. [#29417](https://github.com/pingcap/tidb/issues/29417)
    - planner: change redundantSchema to fullSchema to correctly handle natural and "using" joins. [#29481](https://github.com/pingcap/tidb/issues/29481)
    - planner: fix topn wrongly pushed to index scan side when it's a prefix index [#29711](https://github.com/pingcap/tidb/issues/29711)
    - insert: fix the auto id retry won't cast the datum to origin type. [#29892](https://github.com/pingcap/tidb/issues/29892)

+ TiKV

    - 修复在极端情况下merge, conf change和snapshot同时发生时出现panic的问题 [#11475](https://github.com/tikv/tikv/issues/11475)
    - 修复decimal除法结果为0时 符号为负的问题 [#29586](https://github.com/pingcap/tidb/issues/29586)
    - 修复不正确的by-instance gGrpc 平均时间 [#11299](https://github.com/tikv/tikv/issues/11299)
    - 修复在缺失downstream时CDC panic的问题[#11123](https://github.com/tikv/tikv/issues/11123)
    - 修复在channel 满时会断开raft client 的grpc连接的问题 [#11047](https://github.com/tikv/tikv/issues/11047)
    - 修复在Max/Min 中无法正确识别int64是否为有符号整数从而导致Max/Min结果不正确的问题。[#10158](https://github.com/tikv/tikv/issues/10158)
    - 修复CDC频繁incremental扫描重试导致的Congest错误. [#11082](https://github.com/tikv/tikv/issues/11082)

+ PD

    - 修复 TiKV 节点缩容后可能导致 Panic 的问题 [#4344](https://github.com/tikv/pd/issues/4344)
    - 修复 PD 在旧 leader 下台后无法尽快选举出新 leader 的问题 [#3936](https://github.com/tikv/pd/issues/3936)
    - `evict-leader-scheduler` 支持调度有不健康 Peer 的 Region [#4093](https://github.com/tikv/pd/issues/4093)

+ TiFlash

+ Tools

    + TiCDC

        - 修复监控 checkpoint lag 出现负值的问题 [#3010](https://github.com/pingcap/ticdc/issues/3010)
        - 修复在容器环境中 OOM 的问题 [#1798](https://github.com/pingcap/ticdc/issues/1798)
        - 修复在多个 TiKV 崩溃或强制重启时可能遇到复制中断的问题 [#3288](https://github.com/pingcap/ticdc/issues/3288)
        - 修复处理 DDL 后的内存泄漏 [#3174](https://github.com/pingcap/ticdc/issues/3174)
        - 当发生 ErrGCTTLExceeded 错误时，修复 changefeed 不快速失败的问题 [#3111](https://github.com/pingcap/ticdc/issues/3111)
        - 修复了当发生 region 合并时，回退的 resolvedTs 事件会阻止 resolve lock [#3061](https://github.com/pingcap/ticdc/issues/3061)
        - 当遇到 ErrPrewriteNotMatch 时，关闭 gPRC 流并重新创建它，以避免重复请求错误 [#2386](https://github.com/pingcap/ticdc/issues/2386)
        - 修复 Kafka Sink 由于 `max-message-size` 选项的限制而无法发送消息的问题 [#2962](https://github.com/pingcap/ticdc/issues/2962)
        - 修复 tikv_cdc_min_resolved_ts_no_change_for_1m 监控在没有 changefeed 的情况下持续启动 [#11017](https://github.com/tikv/tikv/issues/11017)
        - 修复 Kafka 生产者报告错误时可能出现的死锁 [#2978](https://github.com/pingcap/ticdc/issues/2978)
        - 在没有有效索引的分区表中添加分区后，修复 DML 不被同步的问题 [#2834](https://github.com/pingcap/ticdc/issues/2834)
        - 修复了在创建新的 changefeed 时可能发生的内存泄漏问题 [#2389](https://github.com/pingcap/ticdc/issues/2389)
        - 让 Sink 组件在汇报 resoved ts 时不要跳过 flush 操作 [#3503](https://github.com/pingcap/ticdc/issues/3503)
        - 将创建服务 gc safepoint ttl 扩展到 1 小时，以支持创建需要长时间初始化的 changefeeds [#2470](https://github.com/pingcap/ticdc/issues/2470)
