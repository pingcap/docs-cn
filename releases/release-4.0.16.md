---
title: TiDB 4.0.16 Release Notes
---

# TiDB 4.0.16 Release Notes

发版日期：2021 年 12 月 10 日

TiDB 版本：4.0.16

## 兼容性更改

+ TiKV

    - 当将一个非法的utf8 字符串转为Real类型时，把该字符串中合法的Utf8前缀转成Real类型，而不是直接报错. [#9870](https://github.com/tikv/tikv/pull/9870)
    - [cdc: reduce events batch to solve congest error (#11086) by ti-srebot · Pull Request #11089 · tikv/tikv](https://github.com/tikv/tikv/pull/11089)

+ TiDB Binlog

    - [drainer: fix kafka message limit problem (#1039) by ti-chi-bot · Pull Request #1078 · pingcap/tidb-binlog](https://github.com/pingcap/tidb-binlog/pull/1078)

## 提升改进

+ TiDB

+ TiKV

    - sst_importer: 当使用BR-Restore或者Lighting-Local-backend时，采用 zstd 算法压缩SST以减小使用空间 [#10642](https://github.com/tikv/tikv/pull/10642)


+ Tools

    + Backup & Restore (BR)

        - 增强恢复的鲁棒性 [#1445](https://github.com/pingcap/br/pull/1445)

    + TiCDC

        - 为 EtcdWorker 添加 Tick 频率限制。 [#3267](https://github.com/pingcap/ticdc/pull/3267)
        - 优化 TiKV 重新加载时的速率限制控制，并解决 gPRC 的拥堵问题，这可能导致初始化阶段的缓慢。[#3131](https://github.com/pingcap/ticdc/pull/3131)
        - 将 Kafka Sink `MaxMessageBytes` 的默认值改为 1MB。 [#3106](https://github.com/pingcap/ticdc/pull/3106)
        - 忽略 changefeed 更新命令的全局标志。 [#2875](https://github.com/pingcap/ticdc/pull/2875)
        - 将创建服务 gc safepoint ttl 扩展到 1 小时，以支持创建需要长时间初始化的 changefeeds。 [#2851](https://github.com/pingcap/ticdc/pull/2851)
        - 禁止跨主要和次要版本操作 TiCDC 集群。 [#2601](https://github.com/pingcap/ticdc/pull/2601)

## Bug fixes

+ TiDB

    - 修复了在统计信息模块的估算代价中，在执行 range 转 point 时，一处由于数值溢出而导致的查询崩溃 [#30017](https://github.com/pingcap/tidb/pull/30017)
    - 修复了 enum 类型作为 `if`, `case when` 等控制函数参数时，返回结果不正确的问题 [#30011](https://github.com/pingcap/tidb/pull/30011)
    - 修复了 `greatest` 函数在开启和关闭向量化表达式时，返回结果不一致的问题 [#29916](https://github.com/pingcap/tidb/pull/29916)
    - 修复了一些 index join 作用在前缀索引上时崩溃的问题 [#29217](https://github.com/pingcap/tidb/pull/29217)
    - 修复了一个优化器在某些 join 的场景中会缓存无效的查询计划的问题 [#28444](https://github.com/pingcap/tidb/pull/28444)
    - 修复了当 `sql_mode` 为空时，TiDB 无法插入 `null` 到非 `null` 列的问题 [#27832](https://github.com/pingcap/tidb/pull/27832)
    - 修正了 `greatest`/`least` 函数的返回值类型 [#29911](https://github.com/pingcap/tidb/pull/29911)
    - 修复了`grant` 和 `revoke` 操作在授予全局权限时，报错 'privilege check fail' 的问题 [#29899](https://github.com/pingcap/tidb/pull/29899)
    - 修复 `case when` 函数和 enum 类型一起使用时的一处崩溃 [#29508](https://github.com/pingcap/tidb/pull/29508)
    - 修复 `microsecond` 函数的向量化表达式版本结果不正确的问题 [#29384](https://github.com/pingcap/tidb/pull/29384)
    - 修复 `hour` 函数的向量化表达式版本结果不正确的问题 [#28870](https://github.com/pingcap/tidb/pull/28870)
    - 修复了乐观事务冲突导致可能相互阻塞的问题 [#29775](https://github.com/pingcap/tidb/pull/29775)
    - 修复 auto analyze 一处日志信息不全 [#29227](https://github.com/pingcap/tidb/pull/29227)
    - 修复了 `NO_ZERO_IN_DATE` 对默认值未生效的问题 [#26902](https://github.com/pingcap/tidb/pull/26902)
    - 修复了 copt-cache 的监控信息，现在在 Grafana 中会显示 hits/miss/evict 的数据 [#26342](https://github.com/pingcap/tidb/pull/26342)
    - 修复并发 truncate 相同的分区导致 DDL 卡死的问题 [#26237](https://github.com/pingcap/tidb/pull/26237)

+ TiKV

    - 修复在极端情况下merge, conf change和snapshot同时发生时出现panic的问题[#11509](https://github.com/tikv/tikv/pull/11509)
    - 修复decimal除法结果为0时 符号为负的问题 [#11332](https://github.com/tikv/tikv/pull/11332)
    - 修复不正确的by-instance gGrpc 平均时间 [#11326](https://github.com/tikv/tikv/pull/11326)
    - 修复在缺失downstream时CDC panic的问题[#11135](https://github.com/tikv/tikv/pull/11135)
    - 修复在channel 满时会断开raft client 的grpc连接的问题 [#11069](https://github.com/tikv/tikv/pull/11069)
    - 修复在Max/Min 中无法正确识别int64是否为有符号整数从而导致Max/Min结果不正确的问题。[#10616](https://github.com/tikv/tikv/pull/10616)
    -  修复CDC频繁incremental扫描重试导致的Congest错误. [#11089](https://github.com/tikv/tikv/pull/11089)

+ PD

    - 修复 TiKV 节点缩容后可能导致 Panic 的问题 [#4378](https://github.com/tikv/pd/pull/4378)
    - 修复 PD 在旧 leader 下台后无法尽快选举出新 leader 的问题 [#4219](https://github.com/tikv/pd/pull/4219)
    - `evict-leader-scheduler` 支持调度有不健康 Peer 的 Region [#4133](https://github.com/tikv/pd/pull/4133)

+ TiFlash

+ Tools

    + TiCDC

        - 修复监控 checkpoint lag 出现负值的问题。 [#3532](https://github.com/pingcap/ticdc/pull/3532)
        - 修复在容器环境中 OOM 的问题。 [#3440](https://github.com/pingcap/ticdc/pull/3440)
        - 修复在多个 TiKV 崩溃或强制重启时可能遇到复制中断的问题。 [#3290](https://github.com/pingcap/ticdc/pull/3290)
        - 修复处理 DDL 后的内存泄漏。 [#3274](https://github.com/pingcap/ticdc/pull/3274)
        - 当发生 ErrGCTTLExceeded 错误时，修复 changefeed 不快速失败的问题。 [#3134](https://github.com/pingcap/ticdc/pull/3134)
        - 修复了当发生 region 合并时，回退的 resolvedTs 事件会阻止 resolve lock。 [#3099](https://github.com/pingcap/ticdc/pull/3099)
        - 当遇到 ErrPrewriteNotMatch 时，关闭 gPRC 流并重新创建它，以避免重复请求错误。 [#3094](https://github.com/pingcap/ticdc/pull/3094)
        - 修复 Kafka Sink 由于 `max-message-size` 选项的限制而无法发送消息的问题。 [#3046](https://github.com/pingcap/ticdc/pull/3046)
        - 修复 tikv_cdc_min_resolved_ts_no_change_for_1m 监控在没有 changefeed 的情况下持续启动。 [#3023](https://github.com/pingcap/ticdc/pull/3023)
        - 修复 Kafka 生产者报告错误时可能出现的死锁。[#3015](https://github.com/pingcap/ticdc/pull/3015)
        - 在没有有效索引的分区表中添加分区后，修复 DML 不被同步的问题。 [#2863](https://github.com/pingcap/ticdc/pull/2863)
        - 修复了在创建新的 changefeed 时可能发生的内存泄漏问题。 [#2623](https://github.com/pingcap/ticdc/pull/2623)
        - 正确设置 Kafka 生产者请求元数据的超时时间，防止数据同步卡住。 [#3669](https://github.com/pingcap/ticdc/pull/3669)

## 未抓取到的 critical bug

+ TiDB

+ TiKV

+ TiFlash

+ Tools

+ PD
