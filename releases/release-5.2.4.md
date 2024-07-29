---
title: TiDB 5.2.4 Release Notes
category: Releases
---

# TiDB 5.2.4 Release Notes

发版日期：2022 年 4 月 26 日

TiDB 版本：5.2.4

## 兼容性更改

+ TiDB

    - 将系统变量 [`tidb_analyze_version`](/system-variables.md#tidb_analyze_version-从-v510-版本开始引入) 的默认值从 `2` 修改为 `1` [#31748](https://github.com/pingcap/tidb/issues/31748)

+ TiKV

    - 新增 [`raft-log-compact-sync-interval`](https://docs.pingcap.com/zh/tidb/v5.2/tikv-configuration-file#raft-log-compact-sync-interval-从-v524-版本开始引入) 配置项，用于压缩非必要的 Raft 日志的时间间隔，默认值为 `"2s"` [#11404](https://github.com/tikv/tikv/issues/11404)
    - 将 [`raft-log-gc-tick-interval`](/tikv-configuration-file.md#raft-log-gc-tick-interval) 的默认值从 `"10s"` 修改为 `"3s"` [#11404](https://github.com/tikv/tikv/issues/11404)
    - 当 [`storage.flow-control.enable`](/tikv-configuration-file.md#enable) 的值为 `true` 时，[`storage.flow-control.hard-pending-compaction-bytes-limit`](/tikv-configuration-file.md#hard-pending-compaction-bytes-limit) 的配置会覆盖 [`rocksdb.(defaultcf|writecf|lockcf).hard-pending-compaction-bytes-limit`](/tikv-configuration-file.md#hard-pending-compaction-bytes-limit-1) 的配置 [#11424](https://github.com/tikv/tikv/issues/11424)

+ Tools

    + TiDB Lightning

        - 将 `regionMaxKeyCount` 的默认值从 1_440_000 调整为 1_280_000，以避免数据导入后出现过多空 Region [#30018](https://github.com/pingcap/tidb/issues/30018)

## 提升改进

+ TiKV

    - 通过将 leader 转让给 CDC observer 减少延迟抖动 [#12111](https://github.com/tikv/tikv/issues/12111)
    - 通过减少需要进行清理锁 (Resolve Locks) 步骤的 Region 数量来减少 TiCDC 恢复时间 [#11993](https://github.com/tikv/tikv/issues/11993)
    - 将 proc filesystem (procfs) 升级至 0.12.0 版本 [#11702](https://github.com/tikv/tikv/issues/11702)
    - 通过增加对 Raft log 进行垃圾回收 (GC) 时的 write batch 大小来加快 GC 速度 [#11404](https://github.com/tikv/tikv/issues/11404)
    - 将插入 SST 文件时的校验操作从 Apply 线程池移动到 Import 线程池，从而提高 SST 文件的插入速度 [#11239](https://github.com/tikv/tikv/issues/11239)

+ Tools

    + TiCDC

        - 将 Kafka Sink `partition-num` 的默认值改为 3，使 TiCDC 更加平均地分发消息到各个 Kafka partition [#3337](https://github.com/pingcap/tiflow/issues/3337)
        - 减少 TiKV 节点宕机后 KV client 恢复的时间 [#3191](https://github.com/pingcap/tiflow/issues/3191)
        - 在 Grafana 中添加 `Lag analyze` 监控面板 [#4891](https://github.com/pingcap/tiflow/issues/4891)
        - 暴露 Kafka producer 配置参数，使之在 TiCDC 中可配置 [#4385](https://github.com/pingcap/tiflow/issues/4385)
        - 为 changefeed 重启操作添加指数退避机制 [#3329](https://github.com/pingcap/tiflow/issues/3329)
        - 减少 "EventFeed retry rate limited" 日志的数量 [#4006](https://github.com/pingcap/tiflow/issues/4006)
        - 将 `max-message-bytes` 默认值设置为 10M [#4041](https://github.com/pingcap/tiflow/issues/4041)
        - 增加更多 Prometheus 和 Grafana 监控告警参数，包括 `no owner alert`、`mounter row`、`table sink total row` 和 `buffer sink total row` [#4054](https://github.com/pingcap/tiflow/issues/4054) [#1606](https://github.com/pingcap/tiflow/issues/1606)
        - 在 Grafana 监控面板中支持多个 Kubernetes 集群 [#4665](https://github.com/pingcap/tiflow/issues/4665)
        - 在 `changefeed checkpoint` 监控项中添加监控指标预计追加时间 (catch-up ETA) [#5232](https://github.com/pingcap/tiflow/issues/5232)

## Bug 修复

+ TiDB

    - 修复 Nulleq 函数作用在 Enum 类型上可能出现结果错误的问题 [#32428](https://github.com/pingcap/tidb/issues/32428)
    - 修复 INDEX HASH JOIN 报 `send on closed channel` 的问题 [#31129](https://github.com/pingcap/tidb/issues/31129)
    - 修复并发的列类型变更导致 schema 与数据不一致的问题 [#31048](https://github.com/pingcap/tidb/issues/31048)
    - 修复乐观事务下数据索引可能不一致的问题 [#30410](https://github.com/pingcap/tidb/issues/30410)
    - 修复当 SQL 语句中存在 JSON 类型列与 `CHAR` 类型列连接时，SQL 出错的问题 [#29401](https://github.com/pingcap/tidb/issues/29401)
    - 修复窗口函数在使用事务时，计算结果与不使用事务时的计算结果不一致的问题 [#29947](https://github.com/pingcap/tidb/issues/29947)
    - 修复 SQL 语句中带有 NATURAL JOIN 时，意外报错 `Column 'col_name' in field list is ambiguous` 的问题 [#25041](https://github.com/pingcap/tidb/issues/25041)
    - 修复将 `Decimal` 转为 `String` 时长度信息错误的问题 [#29417](https://github.com/pingcap/tidb/issues/29417)
    - 修复由于 `tidb_enable_vectorized_expression` 设置的值不同（`on` 或 `off`）导致 `GREATEST` 函数返回结果不一致的问题 [#29434](https://github.com/pingcap/tidb/issues/29434)
    - 修复使用 left join 同时删除多张表数据时可能出现错误结果的问题 [#31321](https://github.com/pingcap/tidb/issues/31321)
    - 修复 TiDB 可能向 TiFlash 发送重复任务的问题 [#32814](https://github.com/pingcap/tidb/issues/32814)
    - 修复执行查询时报 MPP task list 为空错误的问题 [#31636](https://github.com/pingcap/tidb/issues/31636)
    - 修复 innerWorker panic 导致的 index join 结果错误的问题 [#31494](https://github.com/pingcap/tidb/issues/31494)
    - 修复 `INSERT ... SELECT ... ON DUPLICATE KEY UPDATE` 语句 panic 的问题 [#28078](https://github.com/pingcap/tidb/issues/28078)
    - 修复针对 `Order By` 的优化导致查询结果有误的问题 [#30271](https://github.com/pingcap/tidb/issues/30271)
    - 修复使用 `ENUM` 类型的列进行 Join 时结果可能不正确的问题 [#27831](https://github.com/pingcap/tidb/issues/27831)
    - 修复当 `CASE WHEN` 函数和 `ENUM` 类型一起使用时的崩溃问题 [#29357](https://github.com/pingcap/tidb/issues/29357)
    - 修复 `microsecond` 函数的向量化表达式版本结果不正确的问题 [#29244](https://github.com/pingcap/tidb/issues/29244)
    - 修复窗口函数执行时本应报错但是让 TiDB 崩溃的问题 [#30326](https://github.com/pingcap/tidb/issues/30326)
    - 修复特定情况下 Merge Join 执行结果错误的问题 [#33042](https://github.com/pingcap/tidb/issues/33042)
    - 修复关联子查询返回结果中有常量时导致执行结果出错的问题  [#32089](https://github.com/pingcap/tidb/issues/32089)
    - 修复 `ENUM` 或 `SET` 类型的列因为编码错误导致写入数据错误的问题 [#32302](https://github.com/pingcap/tidb/issues/32302)
    - 修复开启 New Collation 时，作用在 `ENUM` 或`SET` 列上的 `MAX` 或 `MIN` 函数结果出错的问题 [#31638](https://github.com/pingcap/tidb/issues/31638)
    - 修复某些情况下 IndexHashJoin 算子没有正常退出的问题 [#31062](https://github.com/pingcap/tidb/issues/31062)
    - 修复有虚拟列时可能导致 TiDB 读到错误数据的问题 [#30965](https://github.com/pingcap/tidb/issues/30965)
    - 修复日志级别的设置没有对慢查询日志生效的问题 [#30309](https://github.com/pingcap/tidb/issues/30309)
    - 修复某些情况下分区表无法充分利用索引来扫描数据的问题 [#33966](https://github.com/pingcap/tidb/issues/33966)
    - 修复 TiDB 的后台 HTTP 服务可能没有正确关闭导致集群状态异常的问题 [#30571](https://github.com/pingcap/tidb/issues/30571)
    - 修复 TiDB 会非预期地打印很多鉴权失败相关日志的问题 [#29709](https://github.com/pingcap/tidb/issues/29709)
    - 修复系统变量 `max_allowed_packet` 不生效的问题 [#31422](https://github.com/pingcap/tidb/issues/31422)
    - 修复当 auto ID 超出范围时，`REPLACE` 语句错误地修改了其它行的问题 [#29483](https://github.com/pingcap/tidb/issues/29483)
    - 修复慢查询日志无法正常输出而且可能消耗大量内存的问题 [#32656](https://github.com/pingcap/tidb/issues/32656)
    - 修复 NATURAL JOIN 可能输出多余列的问题 [#29481](https://github.com/pingcap/tidb/issues/29481)
    - 修复使用前缀列索引时，ORDER + LIMIT 语句可能导致结果出错的问题 [#29711](https://github.com/pingcap/tidb/issues/29711)
    - 修复乐观事务重试时，DOUBLE 类型的自增列可能在重试时值发生改变的问题 [#29892](https://github.com/pingcap/tidb/issues/29892)
    - 修复 STR_TO_DATE 函数无法正确处理微秒部分的前导 0 的问题 [#30078](https://github.com/pingcap/tidb/issues/30078)
    - 修复在 TiFlash 不支持使用空范围读表的情况，依然选择 TiFlash 导致查询结果错误的问题 [#33083](https://github.com/pingcap/tidb/issues/33083)

+ TiKV

    - 修复旧信息造成 TiKV panic 的问题 [#12023](https://github.com/tikv/tikv/issues/12023)
    - 修复因内存统计指标溢出而造成的间歇性丢包和内存不足 (OOM) 的问题 [#12160](https://github.com/tikv/tikv/issues/12160)
    - 修复在 Ubuntu 18.04 下进行性能分析会造成 TiKV panic 的问题 [#9765](https://github.com/tikv/tikv/issues/9765)
    - 修复 tikv-ctl 对 `bad-ssts` 结果字符串进行错误匹配的问题 [#12329](https://github.com/tikv/tikv/issues/12329)
    - 修复 Replica Read 可能违反线性一致性的问题 [#12109](https://github.com/tikv/tikv/issues/12109)
    - 修复 TiKV 运行 2 年以上可能 panic 的问题 [#11940](https://github.com/tikv/tikv/issues/11940)
    - 修复开启流量控制且显式设置 `level0_slowdown_trigger` 时出现 QPS 下降的问题 [#11424](https://github.com/tikv/tikv/issues/11424)
    - 修复 cgroup controller 没有被挂载会造成 panic 的问题 [#11569](https://github.com/tikv/tikv/issues/11569)
    - 修复在滞后的 Region peer 上执行 Region Merge 导致的元数据损坏问题 [#11526](https://github.com/tikv/tikv/issues/11526)
    - 修复 TiKV 停止后 Resolved TS 延迟会增加的问题 [#11351](https://github.com/tikv/tikv/issues/11351)
    - 修复在极端情况下同时进行 Region Merge、ConfChange 和 snapshot 时，TiKV 会出现 panic 的问题 [#11475](https://github.com/tikv/tikv/issues/11475)
    - 修复 tikv-ctl 无法正确输出 Region 相关信息的问题 [#11393](https://github.com/tikv/tikv/issues/11393)
    - 修复 Decimal 除法计算的结果为 0 时符号为负的问题 [#29586](https://github.com/pingcap/tidb/issues/29586)
    - 修复悲观事务中 prewrite 请求重试在极少数情况下影响数据一致性的风险 [#11187](https://github.com/tikv/tikv/issues/11187)
    - 修复因统计线程监控数据导致的内存泄漏 [#11195](https://github.com/tikv/tikv/issues/11195)
    - 修复 TiKV 监控项中实例级别 gRPC 的平均延迟时间不准确的问题 [#11299](https://github.com/tikv/tikv/issues/11299)
    - 修复 Peer 状态为 Applying 时快照文件被删除会造成 panic 的问题 [#11746](https://github.com/tikv/tikv/issues/11746)
    - 修复 GC worker 繁忙后无法执行范围删除（即执行内部命令 `unsafe_destroy_range`）的问题 [#11903](https://github.com/tikv/tikv/issues/11903)
    - 修复删除未初始化的副本可能会造成旧副本被重新创建的问题 [#10533](https://github.com/tikv/tikv/issues/10533)
    - 修复逆序扫表时 TiKV 无法正确读到内存锁的问题 [#11440](https://github.com/tikv/tikv/issues/11440)
    - 修复协程的执行速度太快时偶尔出现的死锁问题 [#11549](https://github.com/tikv/tikv/issues/11549)
    - 修复删除 Peer 可能造成高延迟的问题 [#10210](https://github.com/tikv/tikv/issues/10210)
    - 修复待 merge 的 Region 无效会导致 TiKV panic 且非预期地销毁 peer 的问题 [#12232](https://github.com/tikv/tikv/issues/12232)
    - 修复合并 Region 时因 target peer 被一个未进行初始化就被销毁的 peer 所替换，从而引起 TiKV panic 的问题 [#12048](https://github.com/tikv/tikv/issues/12048)
    - 修复 apply snapshot 被暂停时会引起 TiKV panic 的问题 [#11618](https://github.com/tikv/tikv/issues/11618)
    - 修复了在 operator 执行失败时，TiKV 无法正确地计算正在发送的 snapshot 数量的问题 [#11341](https://github.com/tikv/tikv/issues/11341)

+ PD

    - 修复 Region Scatterer 生成的调度缺失部分 Peer 的问题 [#4565](https://github.com/tikv/pd/issues/4565)
    - 修复热点统计中无法剔除冷热点数据的问题 [#4390](https://github.com/tikv/pd/issues/4390)

+ TiFlash

    - 修复 MPP 任务可能永远泄漏线程的问题 [#4238](https://github.com/pingcap/tiflash/issues/4238)
    - 修复 `IN` 函数的结果在多值表达式中不正确的问题 [#4016](https://github.com/pingcap/tiflash/issues/4016)
    - 修复日期格式将 `'\n'` 处理为非法分隔符的问题 [#4036](https://github.com/pingcap/tiflash/issues/4036)
    - 修复在读取工作量大时添加列后可能出现的查询错误 [#3967](https://github.com/pingcap/tiflash/issues/3967)
    - 修复错误地配置存储目录会导致非预期行为的问题 [#4093](https://github.com/pingcap/tiflash/issues/4093)
    - 修复一些异常没有被正确地处理的问题 [#4101](https://github.com/pingcap/tiflash/issues/4101)
    - 修复 `STR_TO_DATE()` 函数对微秒前导零的错误解析 [#3557](https://github.com/pingcap/tiflash/issues/3557)
    - 修复将 `INT` 类型转换为 `DECIMAL` 类型可能造成溢出的问题 [#3920](https://github.com/pingcap/tiflash/issues/3920)
    - 修复将 `DATETIME` 转换为 `DECIMAL` 时结果错误的问题 [#4151](https://github.com/pingcap/tiflash/issues/4151)
    - 修复将 `FLOAT` 类型转换为 `DECIMAL` 类型可能造成溢出的问题 [#3998](https://github.com/pingcap/tiflash/issues/3998)
    - 修复 `CastStringAsReal` 在 TiFlash 的行为与在 TiDB、TiKV 的行为不一致的问题 [#3475](https://github.com/pingcap/tiflash/issues/3475)
    - 修复 `CastStringAsDecimal` 在 TiFlash 的行为与在 TiDB、TiKV 的行为不一致的问题 [#3619](https://github.com/pingcap/tiflash/issues/3619)
    - 修复 TiFlash 重启时偶发的 `EstablishMPPConnection` 错误 [#3615](https://github.com/pingcap/tiflash/issues/3615)
    - 修复当设置 TiFlash 副本数为 0（即删除数据）后数据无法回收的问题 [#3659](https://github.com/pingcap/tiflash/issues/3659)
    - 修复当主键为 handle 时，扩宽主键列可能导致的数据不一致问题 [#3569](https://github.com/pingcap/tiflash/issues/3569)
    - 修复 SQL 语句中含有极长嵌套表达式时可能出现的解析错误 [#3354](https://github.com/pingcap/tiflash/issues/3354)
    - 修复查询语句包含 `where <string>` 时查询结果出错的问题 [#3447](https://github.com/pingcap/tiflash/issues/3447)
    - 修复 `new_collations_enabled_on_first_bootstrap` 开启后查询结果可能出错的问题 [#3388](https://github.com/pingcap/tiflash/issues/3388), [#3391](https://github.com/pingcap/tiflash/issues/3391)
    - 修复启用 TLS 时可能导致的崩溃 [#4196](https://github.com/pingcap/tiflash/issues/4196)
    - 修复启用内存限制后 TiFlash 崩溃的问题 [#3902](https://github.com/pingcap/tiflash/issues/3902)
    - 修复当 MPP 查询被终止时，TiFlash 偶发的崩溃问题 [#3401](https://github.com/pingcap/tiflash/issues/3401)
    - 修复非预期的 `Unexpected type of column: Nullable(Nothing)` 错误 [#3351](https://github.com/pingcap/tiflash/issues/3351)
    - 修复在滞后的 Region peer 上执行 Region Merge 导致的元数据损坏问题 [#4437](https://github.com/pingcap/tiflash/issues/4437)
    - 修复在执行带有 `JOIN` 的查询遇到错误时可能被挂起的问题 [#4195](https://github.com/pingcap/tiflash/issues/4195)
    - 修复不正确的执行计划可能导致 MPP 查询出错的问题 [#3389](https://github.com/pingcap/tiflash/issues/3389)

+ Tools

    + Backup & Restore (BR)

        - 修复 BR 无法备份 RawKV 的问题 [#32607](https://github.com/pingcap/tidb/issues/32607)

    + TiCDC

        - 修复不支持同步默认值的问题 [#3793](https://github.com/pingcap/tiflow/issues/3793)
        - 修复某些情况下序列对象被错误同步的问题 [#4552](https://github.com/pingcap/tiflow/issues/4552)
        - 修复了 TiCDC 进程在 PD leader 被杀死时的异常退出问题 [#4248](https://github.com/pingcap/tiflow/issues/4248)
        - 修复 MySQL sink 在禁用 `batch-replace-enable` 参数时生成重复 `replace` SQL 语句的错误 [#4501](https://github.com/pingcap/tiflow/issues/4501)
        - 修复输出默认列值时的 panic 问题和数据不一致的问题 [#3929](https://github.com/pingcap/tiflow/issues/3929)
        - 修复 `mq sink write row` 没有监控数据的问题 [#3431](https://github.com/pingcap/tiflow/issues/3431)
        - 修复当 `min.insync.replicas` 小于 `replication-factor` 时不能同步的问题 [#3994](https://github.com/pingcap/tiflow/issues/3994)
        - 修复在移除同步任务后潜在的 panic 问题 [#3128](https://github.com/pingcap/tiflow/issues/3128)
        - 修复了 HTTP API 在查询的组件不存在时导致 CDC 挂掉的问题 [#3840](https://github.com/pingcap/tiflow/issues/3840)
        - 修复因 checkpoint 不准确导致的潜在的数据丢失问题 [#3545](https://github.com/pingcap/tiflow/issues/3545)
        - 修复潜在的同步流控死锁问题 [#4055](https://github.com/pingcap/tiflow/issues/4055)
        - 修复人为删除 etcd 任务的状态时导致 TiCDC panic 的问题 [#2980](https://github.com/pingcap/tiflow/issues/2980)
        - 修复 DDL 特殊注释导致的同步停止的问题 [#3755](https://github.com/pingcap/tiflow/issues/3755)
        - 修复 `config.Metadata.Timeout` 没有正确配置而导致的同步停止问题 [#3352](https://github.com/pingcap/tiflow/issues/3352)
        - 修复在某些 RHEL 发行版上因时区问题导致服务无法启动的问题 [#3584](https://github.com/pingcap/tiflow/issues/3584)
        - 修复集群升级后 `stopped` 状态的 changefeed 自动恢复的问题 [#3473](https://github.com/pingcap/tiflow/issues/3473)
        - 修复 MySQL sink 模块出现死锁时告警过于频繁的问题 [#2706](https://github.com/pingcap/tiflow/issues/2706)
        - 修复 Canal 协议下 TiCDC 没有自动开启 `enable-old-value` 选项的问题 [#3676](https://github.com/pingcap/tiflow/issues/3676)
        - 修复 Avro sink 模块不支持解析 JSON 类型列的问题 [#3624](https://github.com/pingcap/tiflow/issues/3624)
        - 修复监控 checkpoint lag 出现负值的问题 [#3010](https://github.com/pingcap/tiflow/issues/3010)
        - 修复在容器环境中 OOM 的问题 [#1798](https://github.com/pingcap/tiflow/issues/1798)
        - 修复执行 DDL 后的内存泄漏的问题 [#3174](https://github.com/pingcap/tiflow/issues/3174)
        - 修复在同一节点反复调入调出一张表可能会导致同步任务 (changefeed) 被卡住的问题 [#4464](https://github.com/pingcap/tiflow/issues/4464)
        - 修复当 PD 状态不正常时 OpenAPI 可能会卡住的问题 [#4778](https://github.com/pingcap/tiflow/issues/4778)
        - 修复切换 owner 会导致其 metrics 数据不正确的问题 [#4774](https://github.com/pingcap/tiflow/issues/4774)
        - 修复 Unified Sorter 的 workerpool 稳定性问题 [#4447](https://github.com/pingcap/tiflow/issues/4447)
        - 修复 `cached region` 监控指标为负数的问题 [#4300](https://github.com/pingcap/tiflow/issues/4300)

    + TiDB Lightning

        - 修复当 TiDB Lightning 没有权限访问 `mysql.tidb` 表时，导入的结果不正确的问题 [#31088](https://github.com/pingcap/tidb/issues/31088)
        - 修复了 checksum 报错 “GC life time is shorter than transaction duration” [#32733](https://github.com/pingcap/tidb/issues/32733)
        - 修复在某些导入操作没有包含源文件时，TiDB Lightning 不会删除 metadata schema 的问题 [#28144](https://github.com/pingcap/tidb/issues/28144)
        - 修复 S3 存储路径不存在时 TiDB Lightning 不报错的问题 [#28031](https://github.com/pingcap/tidb/issues/28031) [#30709](https://github.com/pingcap/tidb/issues/30709)
        - 修复在 GCS 上遍历超过 1000 个 key 时会出错的问题 [#30377](https://github.com/pingcap/tidb/issues/30377)