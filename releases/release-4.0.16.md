---
title: TiDB 4.0.16 Release Notes
summary: TiDB 4.0.16 发布，包含兼容性更改、提升改进和 Bug 修复。TiKV 改进了对非法 UTF-8 字符串的处理，Tools 中 TiCDC 改变了 Kafka Sink 默认值。TiDB 升级了 Grafana，TiKV 使用 zstd 算法压缩 SST 文件。Bug 修复包括统计信息模块的查询崩溃、`ENUM` 类型控制函数返回结果不正确等问题。TiKV 修复了多个问题，包括 Decimal 除法计算结果为负、监控项中 gRPC 平均延迟时间不准确等问题。PD 修复了节点缩容后可能导致 Panic 的问题。TiFlash 修复了无法启动的问题。Tools 中 TiDB Binlog 修复了 Drainer 传输事务超过 1 GB 时退出的问题，TiCDC 修复了多个问题。
---

# TiDB 4.0.16 Release Notes

发版日期：2021 年 12 月 17 日

TiDB 版本：4.0.16

## 兼容性更改

+ TiKV

    - 在 v4.0.16 以前，当把一个非法的 UTF-8 字符串转换为 Real 类型时会直接报错。自 v4.0.16 起，TiDB 会依照该字符串中的合法 UTF-8 前缀进行转换 [#11466](https://github.com/tikv/tikv/issues/11466)

+ Tools

    + TiCDC

        - 将 Kafka Sink `max-message-bytes` 的默认值改为 1 MB，防止 TiCDC 发送过大消息到 Kafka 集群 [#2962](https://github.com/pingcap/tiflow/issues/2962)
        - 将 Kafka Sink `partition-num` 的默认值改为 3，使 TiCDC 更加平均地分发消息到各个 Kafka partition [#3337](https://github.com/pingcap/tiflow/issues/3337)

## 提升改进

+ TiDB

    - 升级 Grafana 到 v7.5.11，规避老版本的安全漏洞

+ TiKV

    - 当使用 Backup & Restore 恢复数据或使用 TiDB Lightning 的 Local-backend 导入数据时，采用 zstd 算法压缩 SST 文件，从而减小磁盘使用空间 [#11469](https://github.com/tikv/tikv/issues/11469)

+ Tools

    + Backup & Restore (BR)

        - 增强恢复的鲁棒性 [#27421](https://github.com/pingcap/tidb/issues/27421)

    + TiCDC

        - 为 EtcdWorker 添加 tick 频率限制，防止 PD 的 etcd 写入次数过于频繁影响 PD 服务 [#3112](https://github.com/pingcap/tiflow/issues/3112)
        - 优化 TiKV 重新加载时的速率限制控制，缓解 changefeed 初始化时 gPRC 的拥堵问题 [#3110](https://github.com/pingcap/tiflow/issues/3110)

## Bug 修复

+ TiDB

    - 修复在统计信息模块的估算代价中，当执行 range 转 points 时由于数值溢出而导致的查询崩溃 [#23625](https://github.com/pingcap/tidb/issues/23625)
    - 修复当 `ENUM` 类型作为 `IF` 或 `CASE WHEN` 等控制函数的参数时，返回结果不正确的问题 [#23114](https://github.com/pingcap/tidb/issues/23114)
    - 修复由于 `tidb_enable_vectorized_expression` 设置的值不同（`on` 或 `off`）导致 `GREATEST` 函数返回结果不一致的问题 [#29434](https://github.com/pingcap/tidb/issues/29434)
    - 修复 `Index Join` 在使用前缀索引时某些情况下崩溃的问题 [#24547](https://github.com/pingcap/tidb/issues/24547)
    - 修复在某些情况下 Planner 可能缓存无效 `join` 计划的问题 [#28087](https://github.com/pingcap/tidb/issues/28087)
    - 修复当 `sql_mode` 为空时，TiDB 无法插入 `null` 到非 null 列的问题 [#11648](https://github.com/pingcap/tidb/issues/11648)
    - 修正 `GREATEST` 和 `LEAST` 函数的返回值类型错误 [#29019](https://github.com/pingcap/tidb/issues/29019)
    - 修复 `grant` 和 `revoke` 操作在授予和撤销全局权限时，报 `privilege check fail` 错误的问题 [#29675](https://github.com/pingcap/tidb/issues/29675)
    - 修复当 `CASE WHEN` 函数和 `ENUM` 类型一起使用时的崩溃问题 [#29357](https://github.com/pingcap/tidb/issues/29357)
    - 修复 `microsecond` 函数的向量化表达式版本结果不正确的问题 [#29244](https://github.com/pingcap/tidb/issues/29244)
    - 修复 `hour` 函数在向量化表达式中执行结果错误的问题 [#28643](https://github.com/pingcap/tidb/issues/28643)
    - 修复乐观事务冲突可能导致事务相互阻塞的问题 [#11148](https://github.com/tikv/tikv/issues/11148)
    - 修复 `auto analyze` 输出的日志信息不完整的问题 [#29188](https://github.com/pingcap/tidb/issues/29188)
    - 修复当 `SQL_MODE` 为 'NO_ZERO_IN_DATE' 时，使用非法的默认时间不报错的问题 [#26766](https://github.com/pingcap/tidb/issues/26766)
    - 修复 Grafana 上 Coprocessor Cache 监控面板不显示数据的问题。现在 Grafana 会显示 `hits`/`miss`/`evict` 的数据 [#26338](https://github.com/pingcap/tidb/issues/26338)
    - 修复并发 truncate 同一个分区会导致 DDL 语句执行卡住的问题 [#26229](https://github.com/pingcap/tidb/issues/26229)
    - 修复将 `Decimal` 转为 `String` 时长度信息错误的问题 [#29417](https://github.com/pingcap/tidb/issues/29417)
    - 修复使用 `NATUAL JOIN` 连接多张表时，查询结果中多出一列的问题 [#29481](https://github.com/pingcap/tidb/issues/29481)
    - 修复 `IndexScan` 使用前缀索引时，`TopN` 被错误下推至 `indexPlan` 的问题 [#29711](https://github.com/pingcap/tidb/issues/29711)
    - 修复在 `DOUBLE` 类型的自增列上重试事务会导致数据错误的问题 [#29892](https://github.com/pingcap/tidb/issues/29892)

+ TiKV

    - 修复在极端情况下同时进行 Region Merge、ConfChange 和 Snapshot 时，TiKV 会出现 Panic 的问题 [#11475](https://github.com/tikv/tikv/issues/11475)
    - 修复 Decimal 除法计算的结果为 0 时符号为负的问题 [#29586](https://github.com/pingcap/tidb/issues/29586)
    - 修复 TiKV 监控项中实例级别 gRPC 的平均延迟时间不准确的问题 [#11299](https://github.com/tikv/tikv/issues/11299)
    - 修复在缺失下游数据库时出现 TiCDC Panic 的问题 [#11123](https://github.com/tikv/tikv/issues/11123)
    - 修复因 channel 打满而导致的 Raft 断连的问题 [#11047](https://github.com/tikv/tikv/issues/11047)
    - 修复由于无法在 `Max`/`Min` 函数中正确识别 Int64 是否为有符号整数，导致  `Max`/`Min` 函数的计算结果不正确的问题 [#10158](https://github.com/tikv/tikv/issues/10158)
    - 修复因 Congest 错误而导致的 CDC 频繁增加 scan 重试的问题 [#11082](https://github.com/tikv/tikv/issues/11082)

+ PD

    - 修复 TiKV 节点缩容后可能导致 Panic 的问题 [#4344](https://github.com/tikv/pd/issues/4344)
    - 修复因 Region syncer 卡住而导致 leader 选举慢的问题 [#3936](https://github.com/tikv/pd/issues/3936)
    - 允许 Evict Leader 调度器调度拥有不健康副本的 Region [#4093](https://github.com/tikv/pd/issues/4093)

+ TiFlash

    - 修复 TiFlash 在部分平台上由于缺失 nsl 库而无法启动的问题

+ Tools

    + TiDB Binlog

        - 修复传输事务超过 1 GB 时 Drainer 会退出的问题 [#28659](https://github.com/pingcap/tidb/issues/28659)

    + TiCDC

        - 修复监控 checkpoint lag 出现负值的问题 [#3010](https://github.com/pingcap/tiflow/issues/3010)
        - 修复在容器环境中 OOM 的问题 [#1798](https://github.com/pingcap/tiflow/issues/1798)
        - 修复在多个 TiKV 崩溃或强制重启时可能遇到复制中断的问题 [#3288](https://github.com/pingcap/tiflow/issues/3288)
        - 修复执行 DDL 后的内存泄漏的问题 [#3174](https://github.com/pingcap/tiflow/issues/3174)
        - 修复当发生 ErrGCTTLExceeded 错误时，changefeed 不快速失败的问题 [#3111](https://github.com/pingcap/tiflow/issues/3111)
        - 修复当上游 TiDB 实例意外退出时，TiCDC 同步任务推进可能停滞的问题 [#3061](https://github.com/pingcap/tiflow/issues/3061)
        - 修复当 TiKV 向同一 Region 发送重复请求时，TiCDC 进程 Panic 的问题 [#2386](https://github.com/pingcap/tiflow/issues/2386)
        - 修复 TiCDC 产生的 Kafka 消息体积不受 `max-message-size` 约束的问题 [#2962](https://github.com/pingcap/tiflow/issues/2962)
        - 修复 tikv_cdc_min_resolved_ts_no_change_for_1m 监控在没有 changefeed 的情况下持续更新的问题 [#11017](https://github.com/tikv/tikv/issues/11017)
        - 修复当写入 Kafka 消息发生错误时，TiCDC 同步任务推进可能停滞的问题 [#2978](https://github.com/pingcap/tiflow/issues/2978)
        - 修复当开启 `force-replicate` 时，可能某些没有有效索引的分区表被忽略的问题 [#2834](https://github.com/pingcap/tiflow/issues/2834)
        - 修复在创建新的 changefeed 时可能发生的内存泄漏问题 [#2389](https://github.com/pingcap/tiflow/issues/2389)
        - 修复可能因为 Sink 组件提前推进 resolved ts 导致数据不一致的问题 [#3503](https://github.com/pingcap/tiflow/issues/3503)
        - 修复当扫描存量数据耗时过长时，可能由于 TiKV 进行 GC 而导致存量数据扫描失败的问题 [#2470](https://github.com/pingcap/tiflow/issues/2470)
        - 修复 changefeed 更新命令无法识别全局命令行参数的问题 [#2803](https://github.com/pingcap/tiflow/issues/2803)
