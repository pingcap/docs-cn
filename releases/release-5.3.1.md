---
title: TiDB 5.3.1 Release Notes
---

# TiDB 5.3.1 Release Notes

发版日期：2022 年 x 月 x 日

TiDB 版本：5.3.1

## 兼容性更改
- Tools

    - Lightning
    
        - 将 `regionMaxKeyCount` 的默认值从 1_440_000 调整为 1_280_000，以避免数据导入后出现过多空 Region [#30018](https://github.com/pingcap/tidb/issues/30018)

## 功能增强

- TiDB

    - 优化用户登录模式匹配的逻辑，增强与 MySQL 的兼容性 [#30450](https://github.com/pingcap/tidb/pull/30450)

- TiKV

    - 通过减少需要进行 Resolve Locks（清理锁）步骤的 Region 数量来减少 TiCDC 恢复时间 [#11993](https://github.com/tikv/tikv/issues/11993)
    - 通过增加对 Raft log 进行垃圾回收 (GC) 时的 write batch 大小来加快 GC 速度 [#11404](https://github.com/tikv/tikv/issues/11404)

    (dup) - Update the proc filesystem (procfs) to v0.12.0 [#11702](https://github.com/tikv/tikv/issues/11702)

- PD

    - 优化 `DR_STATE` 文件内容的格式 [#4341](https://github.com/tikv/pd/issues/4341)

- Tools

   - TiCDC

      - 暴露 Kafka producer 配置参数以使之在 TiCDC 中可配置 [#4385](https://github.com/pingcap/tiflow/issues/4385)
      - 在 S3 启动前增加一个预清理进程 [#3878](https://github.com/pingcap/tiflow/issues/3878)
      - TiCDC 客户端能在未指定证书名的情况下工作 [#3627](https://github.com/pingcap/tiflow/issues/3627)
      - 为每个表维护单独的 checkpoint，避免 checkpoint 被意外推进 [#3545](https://github.com/pingcap/tiflow/issues/3545)

      (dup) - Add the exponential backoff mechanism for restarting a changefeed. [#3329](https://github.com/pingcap/tiflow/issues/3329)
      (dup) - Change the default value of Kafka Sink `partition-num` to 3 so that TiCDC distributes messages across Kafka partitions more evenly [#3337](https://github.com/pingcap/tiflow/issues/3337)
      (dup) - Reduce the count of "EventFeed retry rate limited" logs [#4006](https://github.com/pingcap/tiflow/issues/4006)
      (dup) - Set the default value of `max-message-bytes` to 10M [#4041](https://github.com/pingcap/tiflow/issues/4041)
      (dup) - Add more Promethous and Grafana monitoring metrics and alerts, including `no owner alert`, `mounter row`, `table sink total row`, and `buffer sink total row` [#4054](https://github.com/pingcap/tiflow/issues/4054) [#1606](https://github.com/pingcap/tiflow/issues/1606)
      (dup) - Reduce the time for the KV client to recover when a TiKV store is down [#3191](https://github.com/pingcap/tiflow/issues/3191)

    - Lightning

        - 优化了本地磁盘空间检查失败时前置检查的提示信息 [#30395](https://github.com/pingcap/tiflow/issues/30395)

## Bug 修复

- TiDB

    - 修复 date_format 对 `'\n'` 的处理与 MySQL 不兼容的问题 [#32503](https://github.com/pingcap/tidb/pull/32503)
    - 修复 `alter column set default` 错误地修改表定义的问题 [#31074](https://github.com/pingcap/tidb/issues/31074)
    - 修复开启 `tidb_restricted_read_only` 后 `tidb_super_read_only` 没有自动开启的问题 [#31745](https://github.com/pingcap/tidb/issues/31745)
    - 修复带有 collation 的 `greatest` 或 `least` 函数结果出错的问题 [#31789](https://github.com/pingcap/tidb/issues/31789)
    - 修复执行查询时报 MPP task list 为空错误的问题 [#31636](https://github.com/pingcap/tidb/issues/31636)
    - 修复 innerWorker panic 导致的 index join 结果错误的问题 [#31494](https://github.com/pingcap/tidb/issues/31494)
    - 修复将 `FLOAT` 列改为 `DOUBLE` 列后查询结果有误的问题 [#31372](https://github.com/pingcap/tidb/issues/31372)
    - 修复查询时用到 index lookup join 导致 `invalid transaction` 报错的问题 [#30468](https://github.com/pingcap/tidb/issues/30468)
    - 修复针对 `Order By` 的优化导致查询结果有误的问题 [#30271](https://github.com/pingcap/tidb/issues/30271)
    - 修复 `MaxDays` 和 `MaxBackups` 的配置对慢查询日志不生效的问题 [#25716](https://github.com/pingcap/tidb/issues/25716)

    (dup) - 修复 `INSERT ... SELECT ... ON DUPLICATE KEY UPDATE` panic 的问题 [#28078](https://github.com/pingcap/tidb/issues/28078)

- TiKV

    - 修复 peer 状态为 Applying 时快照文件被删除会造成 Panic 的问题 [#11746](https://github.com/tikv/tikv/issues/11746)
    - 修复开启流量控制且显式设置 `level0_slowdown_trigger` 时出现 QPS 下降的问题 [#11424](https://github.com/tikv/tikv/issues/11424)
    - 修复 cgroup controller 没有被挂载会造成 Panic 的问题 [#11569](https://github.com/tikv/tikv/issues/11569)
    - 修复 TiKV 停止后 Resolved TS 延迟会增加的问题 [#11352](https://github.com/tikv/tikv/pull/11352)

    (dup) - Fix a bug that TiKV cannot delete a range of data (`unsafe_destroy_range` cannot be executed) when the GC worker is busy [#11903](https://github.com/tikv/tikv/issues/11903)
    (dup) - Fix the issue that destroying a peer might cause high latency [#10210](https://github.com/tikv/tikv/issues/10210)
    (dup) - Fix a bug that the `any_value` function returns a wrong result when regions are empty [#11735](https://github.com/tikv/tikv/issues/11735)
    (dup) - Fix the issue that deleting an uninitialized replica might cause an old replica to be recreated [#10533](https://github.com/tikv/tikv/issues/10533)
    (dup) - Fix the metadata corruption issue when `Prepare Merge` is triggered after a new election is finished but the isolated peer is not informed [#11526](https://github.com/tikv/tikv/issues/11526)
    (dup) - Fix the deadlock issue that happens occasionally when coroutines run too fast [#11549](https://github.com/tikv/tikv/issues/11549)
    (dup) - Fix the issue that a down TiKV node causes the resolved timestamp to lag [#11351](https://github.com/tikv/tikv/issues/11351)
    (dup) - Fix the issue that batch messages are too large in Raft client implementation [#9714](https://github.com/tikv/tikv/issues/9714)
    (dup) - Fix a panic issue that occurs when Region merge, ConfChange, and Snapshot happen at the same time in extreme conditions [#11475](https://github.com/tikv/tikv/issues/11475)
    (dup) - Fix the issue that TiKV cannot detect the memory lock when TiKV perform a reverse table scan [#11440](https://github.com/tikv/tikv/issues/11440)
    (dup) - Fix the issue that RocksDB flush or compaction causes panic when the disk capacity is full [#11224](https://github.com/tikv/tikv/issues/11224)
    (dup) - Fix a bug that tikv-ctl cannot return the correct Region-related information [#11393](https://github.com/tikv/tikv/issues/11393)
    (dup) - Fix the issue that the average latency of the by-instance gRPC requests is inaccurate in TiKV metrics [#11299](https://github.com/tikv/tikv/issues/11299)

- PD

    - 修复特定情况下调度带有不需要的 JointConsensus 步骤的问题 [#4362](https://github.com/tikv/pd/issues/4362)
    - 修复对单个 Voter 直接进行降级时无法执行调度的问题 [#4444](https://github.com/tikv/pd/issues/4444)
    - 修复更新副本同步模式的配置时出现的数据竞争问题 [#4325](https://github.com/tikv/pd/issues/4325)
    - 修复特定情况下读锁不释放的问题 [#4354](https://github.com/tikv/pd/issues/4354)

    (dup) - Fix the issue that the cold hotspot data cannot be deleted from the hotspot statistics [#4390](https://github.com/tikv/pd/issues/4390)

- TiFlash

    - 修复 `cast(arg as decimal(x,y))` 在入参 `arg` 大于 `decimal(x,y)` 表示范围时，计算结果出错的问题
    - 修复启用 `max_memory_usage` 和 `max_memory_usage_for_all_queries` 配置项时，TiFlash 崩溃的问题
    - 修复 `cast(string as real)` 在部分场景下计算结果出错的问题
    - 修复 `cast(string as decimal)` 在部分场景下计算结果出错的问题
    - 修复在修改主键列类型为一个范围更大的整型类型时，数据索引不一致的问题
    - 修复 `in` 表达式在形如 `(arg0, arg1) in (x,y)` 的多个参数的情况下计算结果出错的问题
    - (dup) 修复当 MPP 查询被终止时，TiFlash 偶发的崩溃问题
    - 修复 `str_to_date` 函数在入参以 0 开头时计算结果出错的问题
    - 修复当查询的过滤条件形如 `where <string>` 时，计算结果出错的问题
    - 修复 `cast(string as datetime)` 在入参形如 `%Y-%m-%d\n%H:%i:%s` 时，查询结果出错的问题

- PD

    - 修复特定情况下调度带有不需要的 JointConsensus 步骤的问题 [#4362](https://github.com/tikv/pd/issues/4362)
    - 修复无法执行对 Voter 直接进行降级的调度的问题 [#4444](https://github.com/tikv/pd/issues/4444)
    - 修复更新副本同步模式的配置时出现的数据竞争问题 [#4325](https://github.com/tikv/pd/issues/4325)
    - 修复特定情况下读锁不释放的问题 [#4354](https://github.com/tikv/pd/issues/4354)

    (dup) - Fix the issue that the cold hotspot data cannot be deleted from the hotspot statistics [#4390](https://github.com/tikv/pd/issues/4390)

- Tools

    - Backup & Restore (BR)

        - 修复当恢复完成后，Region 有可能分布不均的问题 [#31034](https://github.com/pingcap/tiflow/issues/31034)

    - TiCDC

        - 修复了 varchar 类型值长度过长时的 `Column length too big` 错误 [#4637](https://github.com/pingcap/tiflow/issues/4637)
        - 修复了 TiCDC 进程在 PD leader 被杀死时的异常退出问题 [#4248](https://github.com/pingcap/tiflow/issues/4248)
        - 修复了 UPDATE 语句在安全模式下执行错误会导致 DM 进程挂掉的问题 [#4317](https://github.com/pingcap/tiflow/issues/4317)
        - 修复了监控面板中 cached region 项出现负值的问题 [#4300](https://github.com/pingcap/tiflow/issues/4300)
        - 修复了 HTTP API 在查询的组件不存在时导致 CDC 挂掉的问题 [#3840](https://github.com/pingcap/tiflow/issues/3840)
        - 修复了 DM 的 master/worker 线程以特定顺序重启后中继状态错误的问题 [#3478](https://github.com/pingcap/tiflow/issues/3478)
        - 修复了 DM worker 在重启后无法完成初始化的问题 [#3344](https://github.com/pingcap/tiflow/issues/3344)
        - 修复了 DM 任务在分区表相关 DDL 执行时间过长时失败的问题 [#3854](https://github.com/pingcap/tiflow/issues/3854)
        - 修复了 DM 在上游是 MySQL 8.0 时报错 "invalid sequence" 的问题 [#3847](https://github.com/pingcap/tiflow/issues/3847)
        - 修复了移除一个暂停的同步时，CDC Redo Log 无法被正确清理的问题 [#3919](https://github.com/pingcap/tiflow/pull/3919)
        - 修复了 DM 采用细粒度失败重试策略导致数据丢失问题 [#3487](https://github.com/pingcap/tiflow/issues/3487)
        - 修复容器环境中的 OOM 现象 [#1798](https://github.com/pingcap/tiflow/issues/1798)
        - 修复了停止加载中的任务会导致它被意外调度的问题 [#3771](https://github.com/pingcap/tiflow/issues/3771)
        - 纠正了在 Loader 上 query-status 查询到错误的进度的问题 [#3252](https://github.com/pingcap/tiflow/issues/3252)
        - 修复了 HTTP API 在集群中存在不同版本 TiCDC 节点时无法正常工作的问题 [#3483](https://github.com/pingcap/tiflow/issues/3483)
        - 修复了当 CDC Redo Log 配置在 S3 存储上时 TiCDC 异常退出问题 [#3523](https://github.com/pingcap/tiflow/issues/3523)

        (dup) - Fix the issue that default values cannot be replicated [#3793](https://github.com/pingcap/tiflow/issues/3793)
        (dup) - Fix a bug that MySQL sink generates duplicated `replace` SQL statements if `batch-replace-enable` is disabled [#4501](https://github.com/pingcap/tiflow/issues/4501)
        (dup) - Fix the issue that syncer metrics are updated only when querying the status [#4281](https://github.com/pingcap/tiflow/issues/4281)
        (dup) - Fix the issue that `mq sink write row` does not have monitoring data [#3431](https://github.com/pingcap/tiflow/issues/3431)
        (dup) - Fix the issue that replication cannot be performed when `min.insync.replicas` is smaller than `replication-factor` [#3994](https://github.com/pingcap/tiflow/issues/3994)
        (dup) - Fix the issue that the `CREATE VIEW` statement interrupts data replication [#4173](https://github.com/pingcap/tiflow/issues/4173)
        (dup) - Fix the issue the schema needs to be reset after a DDL statement is skipped [#4177](https://github.com/pingcap/tiflow/issues/4177)
        (dup) - Fix the issue that `mq sink write row` does not have monitoring data [#3431](https://github.com/pingcap/tiflow/issues/3431)
        (dup) - Fix the potential panic issue that occurs when a replication task is removed [#3128](https://github.com/pingcap/tiflow/issues/3128)
        (dup) - Fix the potential issue that the deadlock causes a replication task to get stuck [#4055](https://github.com/pingcap/tiflow/issues/4055)
        (dup) - Fix the TiCDC panic issue that occurs when manually cleaning the task status in etcd [#2980](https://github.com/pingcap/tiflow/issues/2980)
        (dup) - Fix the issue that special comments in DDL statements cause the replication task to stop [#3755](https://github.com/pingcap/tiflow/issues/3755)
        (dup) - Fix the issue of replication stop caused by the incorrect configuration of `config.Metadata.Timeout` [#3352](https://github.com/pingcap/tiflow/issues/3352)
        (dup) - Fix the issue that the service cannot be started because of a timezone issue in the RHEL release [#3584](https://github.com/pingcap/tiflow/issues/3584)
        (dup) - Fix the issue that `stopped` changefeeds resume automatically after a cluster upgrade [#3473](https://github.com/pingcap/tiflow/issues/3473)
        (dup) - Fix the issue that default values cannot be replicated [#3793](https://github.com/pingcap/tiflow/issues/3793)
        (dup) - Fix the issue of overly frequent warnings caused by MySQL sink deadlock [#2706](https://github.com/pingcap/tiflow/issues/2706)
        (dup) - Fix the bug that the `enable-old-value` configuration item is not automatically set to `true` on Canal and Maxwell protocols [#3676](https://github.com/pingcap/tiflow/issues/3676)
        (dup) - Fix the issue that Avro sink does not support parsing JSON type columns [#3624](https://github.com/pingcap/tiflow/issues/3624)
        (dup) - Fix the negative value error in the changefeed checkpoint lag [#3010](https://github.com/pingcap/tiflow/issues/3010)

    - TiDB Lightning

        - 修复在某些导入操作没有包含源文件时，Lightning 不会删除 metadata schema 的问题 [#28144](https://github.com/pingcap/tidb/issues/28144)
        - 修复存储 URL 前缀为 "gs://xxx" 而不是 "gcs://xxx" 时，Lightning 报错的问题 [#30254](https://github.com/pingcap/tidb/pull/30254)
        - 修复设置 --log-file="-" 时，没有 log 输出到 stdout 的问题 [#29876](https://github.com/pingcap/tidb/issues/29876) 

        (dup) - Fix the issue that TiDB Lightning does not report errors when the S3 storage path does not exist #28031 [#30709](https://github.com/pingcap/tiflow/issues/30709)
