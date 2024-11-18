---
title: TiDB 5.3.1 Release Notes
---

# TiDB 5.3.1 Release Notes

发版日期：2022 年 3 月 3 日

TiDB 版本：5.3.1

## 兼容性更改

+ Tools

    + TiDB Lightning

        - 将 `regionMaxKeyCount` 的默认值从 1_440_000 调整为 1_280_000，以避免数据导入后出现过多空 Region [#30018](https://github.com/pingcap/tidb/issues/30018)

## 提升改进

+ TiDB

    - 优化用户登录模式匹配的逻辑，增强与 MySQL 的兼容性 [#32648](https://github.com/pingcap/tidb/issues/32648)

+ TiKV

    - 通过减少需要进行清理锁 (Resolve Locks) 步骤的 Region 数量来减少 TiCDC 恢复时间 [#11993](https://github.com/tikv/tikv/issues/11993)
    - 通过增加对 Raft log 进行垃圾回收 (GC) 时的 write batch 大小来加快 GC 速度 [#11404](https://github.com/tikv/tikv/issues/11404)
    - 将 proc filesystem (procfs) 升级至 0.12.0 版本 [#11702](https://github.com/tikv/tikv/issues/11702)

- PD

    - 优化 `DR_STATE` 文件内容的格式 [#4341](https://github.com/tikv/pd/issues/4341)

+ Tools

    + TiCDC

        - 暴露 Kafka producer 配置参数，使之在 TiCDC 中可配置 [#4385](https://github.com/pingcap/tiflow/issues/4385)
        - 当指定 S3 为存储后端时，在 TiCDC 启动前增加预清理逻辑 [#3878](https://github.com/pingcap/tiflow/issues/3878)
        - TiCDC 客户端能在未指定证书名的情况下工作 [#3627](https://github.com/pingcap/tiflow/issues/3627)
        - 修复因 checkpoint 不准确导致的潜在的数据丢失问题 [#3545](https://github.com/pingcap/tiflow/issues/3545)
        - 为 changefeed 重启操作添加指数退避机制 [#3329](https://github.com/pingcap/tiflow/issues/3329)
        - 将 Kafka Sink `partition-num` 的默认值改为 3，使 TiCDC 更加平均地分发消息到各个 Kafka partition [#3337](https://github.com/pingcap/tiflow/issues/3337)
        - 减少 "EventFeed retry rate limited" 日志的数量 [#4006](https://github.com/pingcap/tiflow/issues/4006)
        - 将 `max-message-bytes` 默认值设置为 10M [#4041](https://github.com/pingcap/tiflow/issues/4041)
        - 增加更多 Prometheus 和 Grafana 监控告警参数，包括 `no owner alert`、`mounter row`、`table sink total row` 和 `buffer sink total row` [#4054](https://github.com/pingcap/tiflow/issues/4054) [#1606](https://github.com/pingcap/tiflow/issues/1606)
        - 减少 TiKV 节点宕机后 KV client 恢复的时间 [#3191](https://github.com/pingcap/tiflow/issues/3191)

    - TiDB Lightning

        - 优化了本地磁盘空间检查失败时前置检查的提示信息 [#30395](https://github.com/pingcap/tidb/issues/30395)

## Bug 修复

+ TiDB

    - 修复 date_format 对 `'\n'` 的处理与 MySQL 不兼容的问题 [#32232](https://github.com/pingcap/tidb/issues/32232)
    - 修复 `alter column set default` 错误地修改表定义的问题 [#31074](https://github.com/pingcap/tidb/issues/31074)
    - 修复开启 `tidb_restricted_read_only` 后 `tidb_super_read_only` 没有自动开启的问题 [#31745](https://github.com/pingcap/tidb/issues/31745)
    - 修复带有 collation 的 `greatest` 或 `least` 函数结果出错的问题 [#31789](https://github.com/pingcap/tidb/issues/31789)
    - 修复执行查询时报 MPP task list 为空错误的问题 [#31636](https://github.com/pingcap/tidb/issues/31636)
    - 修复 innerWorker panic 导致的 index join 结果错误的问题 [#31494](https://github.com/pingcap/tidb/issues/31494)
    - 修复将 `FLOAT` 列改为 `DOUBLE` 列后查询结果有误的问题 [#31372](https://github.com/pingcap/tidb/issues/31372)
    - 修复查询时用到 index lookup join 导致 `invalid transaction` 报错的问题 [#30468](https://github.com/pingcap/tidb/issues/30468)
    - 修复针对 `Order By` 的优化导致查询结果有误的问题 [#30271](https://github.com/pingcap/tidb/issues/30271)
    - 修复 `MaxDays` 和 `MaxBackups` 配置项对慢日志不生效的问题 [#25716](https://github.com/pingcap/tidb/issues/25716)
    - 修复 `INSERT ... SELECT ... ON DUPLICATE KEY UPDATE` 语句 panic 的问题 [#28078](https://github.com/pingcap/tidb/issues/28078)

+ TiKV

    - 修复 Peer 状态为 Applying 时快照文件被删除会造成 Panic 的问题 [#11746](https://github.com/tikv/tikv/issues/11746)
    - 修复开启流量控制且显式设置 `level0_slowdown_trigger` 时出现 QPS 下降的问题 [#11424](https://github.com/tikv/tikv/issues/11424)
    - 修复 cgroup controller 没有被挂载会造成 Panic 的问题 [#11569](https://github.com/tikv/tikv/issues/11569)
    - 修复 TiKV 停止后 Resolved TS 延迟会增加的问题 [#11351](https://github.com/tikv/tikv/issues/11351)
    - 修复 GC worker 繁忙后无法执行范围删除（即执行 `unsafe_destroy_range` 参数）的问题 [#11903](https://github.com/tikv/tikv/issues/11903)
    - 修复删除 Peer 可能造成高延迟的问题 [#10210](https://github.com/tikv/tikv/issues/10210)
    - 修复 Region 没有数据时 `any_value` 函数结果错误的问题 [#11735](https://github.com/tikv/tikv/issues/11735)
    - 修复删除未初始化的副本可能会造成旧副本被重新创建的问题 [#10533](https://github.com/tikv/tikv/issues/10533)
    - 修复在已完成重新选举但没有通知被隔离的 Peer 的情况下执行 `Prepare Merge` 会导致元数据损坏的问题 [#11526](https://github.com/tikv/tikv/issues/11526)
    - 修复协程的执行速度太快时偶尔出现的死锁问题 [#11549](https://github.com/tikv/tikv/issues/11549)
    - 修复某个 TiKV 节点停机会导致 Resolved Timestamp 进度落后的问题 [#11351](https://github.com/tikv/tikv/issues/11351)
    - 修复 Raft client 中 batch 消息过大的问题 [#9714](https://github.com/tikv/tikv/issues/9714)
    - 修复在极端情况下同时进行 Region Merge、ConfChange 和 Snapshot 时，TiKV 会出现 Panic 的问题 [#11475](https://github.com/tikv/tikv/issues/11475)
    - 修复逆序扫表时 TiKV 无法正确读到内存锁的问题 [#11440](https://github.com/tikv/tikv/issues/11440)
    - 修复当达到磁盘容量满时 RocksDB flush 或 compaction 导致的 panic [#11224](https://github.com/tikv/tikv/issues/11224)
    - 修复 tikv-ctl 无法正确输出 Region 相关信息的问题 [#11393](https://github.com/tikv/tikv/issues/11393)
    - 修复 TiKV 监控项中实例级别 gRPC 的平均延迟时间不准确的问题 [#11299](https://github.com/tikv/tikv/issues/11299)

+ PD

    - 修复特定情况下调度带有不需要的 JointConsensus 步骤的问题 [#4362](https://github.com/tikv/pd/issues/4362)
    - 修复对单个 Voter 直接进行降级时无法执行调度的问题 [#4444](https://github.com/tikv/pd/issues/4444)
    - 修复更新副本同步模式的配置时出现的数据竞争问题 [#4325](https://github.com/tikv/pd/issues/4325)
    - 修复特定情况下读锁不释放的问题 [#4354](https://github.com/tikv/pd/issues/4354)
    - 修复当 Region 心跳低于 60 秒时热点 Cache 不能清空的问题 [#4390](https://github.com/tikv/pd/issues/4390)

+ TiFlash

    - 修复 `cast(arg as decimal(x,y))` 在入参 `arg` 大于 `decimal(x,y)` 的表示范围时，计算结果出错的问题
    - 修复开启 `max_memory_usage` 和 `max_memory_usage_for_all_queries` 配置项时，TiFlash 崩溃的问题
    - 修复 `cast(string as real)` 在部分场景下计算结果出错的问题
    - 修复 `cast(string as decimal)` 在部分场景下计算结果出错的问题
    - 修复在把主键列类型修改为一个范围更大的整型类型时，数据索引可能不一致的问题
    - 修复 `in` 表达式在形如 `(arg0, arg1) in (x,y)` 的多个参数的情况下计算结果出错的问题
    - 修复当 MPP 查询被终止时，TiFlash 偶发的崩溃问题
    - 修复 `str_to_date` 函数在入参以 0 开头时，计算结果出错的问题
    - 修复当查询的过滤条件形如 `where <string>` 时，计算结果出错的问题
    - 修复 `cast(string as datetime)` 在入参形如 `%Y-%m-%d\n%H:%i:%s` 时，查询结果出错的问题

+ Tools

    + Backup & Restore (BR)

        - 修复当恢复完成后，Region 有可能分布不均的问题 [#31034](https://github.com/pingcap/tidb/issues/31034)

    + TiCDC

        - 修复了 varchar 类型值长度过长时的 `Column length too big` 错误 [#4637](https://github.com/pingcap/tiflow/issues/4637)
        - 修复了 TiCDC 进程在 PD leader 被杀死时的异常退出问题 [#4248](https://github.com/pingcap/tiflow/issues/4248)
        - 修复了 UPDATE 语句在安全模式下执行错误会导致 DM 进程挂掉的问题 [#4317](https://github.com/pingcap/tiflow/issues/4317)
        - 修复 `cached region` 监控指标为负数的问题 [#4300](https://github.com/pingcap/tiflow/issues/4300)
        - 修复了 HTTP API 在查询的组件不存在时导致 CDC 挂掉的问题 [#3840](https://github.com/pingcap/tiflow/issues/3840)
        - 修复了移除一个暂停的同步时，CDC Redo Log 无法被正确清理的问题 [#4740](https://github.com/pingcap/tiflow/issues/4740)
        - 修复在容器环境中 OOM 的问题 [#1798](https://github.com/pingcap/tiflow/issues/1798)
        - 修复了停止加载中的任务会导致它被意外调度的问题 [#3771](https://github.com/pingcap/tiflow/issues/3771)
        - 纠正了在 Loader 上使用 `query-status` 命令查询到错误的进度的问题 [#3252](https://github.com/pingcap/tiflow/issues/3252)
        - 修复了 HTTP API 在集群中存在不同版本 TiCDC 节点时无法正常工作的问题 [#3483](https://github.com/pingcap/tiflow/issues/3483)
        - 修复了当 TiCDC Redo Log 配置在 S3 存储上时 TiCDC 异常退出问题 [#3523](https://github.com/pingcap/tiflow/issues/3523)
        - 修复不支持同步默认值的问题 [#3793](https://github.com/pingcap/tiflow/issues/3793)
        - 修复 MySQL sink 在禁用 `batch-replace-enable` 参数时生成重复 `replace` SQL 语句的错误 [#4501](https://github.com/pingcap/tiflow/issues/4501)
        - 修复部分 syncer metrics 只有在查询状态时才得以更新的问题 [#4281](https://github.com/pingcap/tiflow/issues/4281)
        - 修复当 Kafka 为下游时 `txn_batch_size` 监控指标数据不准确的问题 [#3431](https://github.com/pingcap/tiflow/issues/3431)
        - 修复当 `min.insync.replicas` 小于 `replication-factor` 时不能同步的问题 [#3994](https://github.com/pingcap/tiflow/issues/3994)
        - 修复当 Kafka 为下游时 `txn_batch_size` 监控指标数据不准确的问题 [#3431](https://github.com/pingcap/tiflow/issues/3431)
        - 修复在移除同步任务后潜在的 panic 问题 [#3128](https://github.com/pingcap/tiflow/issues/3128)
        - 修复潜在的同步流控死锁问题 [#4055](https://github.com/pingcap/tiflow/issues/4055)
        - 修复人为删除 etcd 任务的状态时导致 TiCDC panic 的问题 [#2980](https://github.com/pingcap/tiflow/issues/2980)
        - 修复 DDL 特殊注释导致的同步停止的问题 [#3755](https://github.com/pingcap/tiflow/issues/3755)
        - Kafka sink 模块添加默认的元数据获取超时时间配置 (`config.Metadata.Timeout`) [#3352](https://github.com/pingcap/tiflow/issues/3352)
        - 修复 `cdc server` 命令在 Red Hat Enterprise Linux 系统的部分版本（如 6.8、6.9 等）上运行时出现时区错误的问题  [#3584](https://github.com/pingcap/tiflow/issues/3584)
        - 修复集群升级后 `stopped` 状态的 changefeed 自动恢复的问题 [#3473](https://github.com/pingcap/tiflow/issues/3473)
        - 修复不支持同步默认值的问题 [#3793](https://github.com/pingcap/tiflow/issues/3793)
        - 修复 MySQL sink 模块出现死锁时告警过于频繁的问题 [#2706](https://github.com/pingcap/tiflow/issues/2706)
        - 修复 Canal 协议下 TiCDC 没有自动开启 `enable-old-value` 选项的问题 [#3676](https://github.com/pingcap/tiflow/issues/3676)
        - 修复 Avro sink 模块不支持解析 JSON 类型列的问题 [#3624](https://github.com/pingcap/tiflow/issues/3624)
        - 修复监控 checkpoint lag 出现负值的问题 [#3010](https://github.com/pingcap/tiflow/issues/3010)

    + TiDB Data Migration (DM)

        - 修复了 DM 的 master/worker 线程以特定顺序重启后中继状态错误的问题 [#3478](https://github.com/pingcap/tiflow/issues/3478)
        - 修复了 DM worker 在重启后无法完成初始化的问题 [#3344](https://github.com/pingcap/tiflow/issues/3344)
        - 修复了 DM 任务在分区表相关 DDL 执行时间过长时失败的问题 [#3854](https://github.com/pingcap/tiflow/issues/3854)
        - 修复了 DM 在上游是 MySQL 8.0 时报错 "invalid sequence" 的问题 [#3847](https://github.com/pingcap/tiflow/issues/3847)
        - 修复了 DM 采用细粒度失败重试策略导致数据丢失问题 [#3487](https://github.com/pingcap/tiflow/issues/3487)
        - 修复 `CREATE VIEW` 语句中断复制任务的问题 [#4173](https://github.com/pingcap/tiflow/issues/4173)
        - 修复 skip DDL 后需要重置 Schema 的问题 [#4177](https://github.com/pingcap/tiflow/issues/4177)

    + TiDB Lightning

        - 修复在某些导入操作没有包含源文件时，TiDB Lightning 不会删除 metadata schema 的问题 [#28144](https://github.com/pingcap/tidb/issues/28144)
        - 修复存储 URL 前缀为 "gs://xxx" 而不是 "gcs://xxx" 时，TiDB Lightning 报错的问题 [#32742](https://github.com/pingcap/tidb/issues/32742)
        - 修复设置 --log-file="-" 时，没有 log 输出到 stdout 的问题 [#29876](https://github.com/pingcap/tidb/issues/29876)
        - 修复 S3 存储路径不存在时 TiDB Lightning 不报错的问题 [#30709](https://github.com/pingcap/tidb/issues/30709)
