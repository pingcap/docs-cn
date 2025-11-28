---
title: TiDB 6.5.6 Release Notes
summary: 了解 TiDB 6.5.6 版本的兼容性变更、改进提升，以及错误修复。
---

# TiDB 6.5.6 Release Notes

发版日期：2023 年 12 月 7 日

TiDB 版本：6.5.6

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v6.5/quick-start-with-tidb) | [生产部署](https://docs.pingcap.com/zh/tidb/v6.5/production-deployment-using-tiup)

## 兼容性变更

- 在安全增强模式 (SEM) 下禁止设置 [`require_secure_transport`](https://docs.pingcap.com/zh/tidb/v6.5/system-variables#require_secure_transport-从-v610-版本开始引入) 为 `ON`，避免用户无法连接的问题 [#47665](https://github.com/pingcap/tidb/issues/47665) @[tiancaiamao](https://github.com/tiancaiamao)
- 引入系统变量 [`tidb_opt_enable_hash_join`](https://docs.pingcap.com/zh/tidb/v6.5/system-variables#tidb_opt_enable_hash_join-从-v656-版本开始引入) 控制是否选择表的哈希连接 [#46695](https://github.com/pingcap/tidb/issues/46695) @[coderplay](https://github.com/coderplay)
- 经进一步的测试后，TiCDC Changefeed 配置项 [`case-sensitive`](/ticdc/ticdc-changefeed-config.md) 默认值由 `true` 改为 `false`，即默认情况下 TiCDC 配置文件中涉及的表名、库名大小写不敏感 [#10047](https://github.com/pingcap/tiflow/issues/10047) @[sdojjy](https://github.com/sdojjy)
- TiCDC Changefeed 新增以下配置项：
    - [`sql-mode`](/ticdc/ticdc-changefeed-config.md)：你可以设置 TiCDC 同步数据时解析 DDL 语句所使用的 [SQL 模式](/ticdc/ticdc-ddl.md#sql-模式) [#9876](https://github.com/pingcap/tiflow/issues/9876) @[asddongmen](https://github.com/asddongmen)
    - [`encoding-worker-num`](/ticdc/ticdc-changefeed-config.md) 和 [`flush-worker-num`](/ticdc/ticdc-changefeed-config.md)：你可以根据不同的机器规格，设置 redo 模块不同的并发参数 [#10048](https://github.com/pingcap/tiflow/issues/10048) @[CharlesCheung96](https://github.com/CharlesCheung96)
    - [`compression`](/ticdc/ticdc-changefeed-config.md)：你可以设置 redo log 文件的压缩行为 [#10176](https://github.com/pingcap/tiflow/issues/10176) @[sdojjy](https://github.com/sdojjy)
    - [`changefeed-error-stuck-duration`](/ticdc/ticdc-changefeed-config.md)：你可以设置 changefeed 发生内部错误和异常时允许自动重试的时间 [#9875](https://github.com/pingcap/tiflow/issues/9875) @[asddongmen](https://github.com/asddongmen)
    - [`sink.cloud-storage-config`](/ticdc/ticdc-changefeed-config.md)：你可以设置同步数据到对象存储时自动清理历史数据的功能 [#10109](https://github.com/pingcap/tiflow/issues/10109) @[CharlesCheung96](https://github.com/CharlesCheung96)

## 改进提升

+ TiDB

    - 新增支持 [`FLASHBACK CLUSTER TO TSO`](https://docs.pingcap.com/zh/tidb/v6.5/sql-statement-flashback-cluster) 语法 [#48372](https://github.com/pingcap/tidb/issues/48372) @[BornChanger](https://github.com/BornChanger)

+ TiKV

    - 改进 Resolver 的内存使用，防止 OOM [#15458](https://github.com/tikv/tikv/issues/15458) @[overvenus](https://github.com/overvenus)
    - 消除 Router 对象中的 LRUCache，降低内存占用，防止 OOM [#15430](https://github.com/tikv/tikv/issues/15430) @[Connor1996](https://github.com/Connor1996)
    - 为 `apply_router` 和 `raft_router` 指标增加 alive 和 leak 监控维度 [#15357](https://github.com/tikv/tikv/issues/15357) @[tonyxuqqi](https://github.com/tonyxuqqi)

+ PD

    - 在 Grafana 面板上为 `DR Auto-Sync` 添加 `Status`、`Sync Progress` 等监控指标 [#6975](https://github.com/tikv/pd/issues/6975) @[disksing](https://github.com/disksing)

+ Tools

    + Backup & Restore (BR)

        - 快照备份恢复在遇到某些网络错误时会进行重试 [#48528](https://github.com/pingcap/tidb/issues/48528) @[Leavrth](https://github.com/Leavrth)
        - 新增 PITR 对 delete range 场景的集成测试，提升 PITR 稳定性 [#47738](https://github.com/pingcap/tidb/issues/47738) @[Leavrth](https://github.com/Leavrth)
        - 当遇到 Region 打散超时失败或被取消的情况时，快照恢复支持自动重试 Region 打散 [#47236](https://github.com/pingcap/tidb/issues/47236) @[Leavrth](https://github.com/Leavrth)
        - BR 支持通过设置 `merge-schedule-limit` 配置项为 `0` 来暂停 Region 合并 [#7148](https://github.com/tikv/pd/issues/7148) @[3pointer](https://github.com/3pointer)

    + TiCDC

        - 支持通过在 `sink-uri` 中设置 `content-compatible=true` 使 TiCDC Canal-JSON [兼容 Canal 官方输出的内容格式](https://docs.pingcap.com/zh/tidb/v6.5/ticdc-canal-json#兼容-canal-官方实现) [#10106](https://github.com/pingcap/tiflow/issues/10106) @[3AceShowHand](https://github.com/3AceShowHand)
        - 优化同步 `ADD INDEX` DDL 的执行逻辑，从而不阻塞后续的 DML 语句 [#9644](https://github.com/pingcap/tiflow/issues/9644) @[sdojjy](https://github.com/sdojjy)
        - 减少 TiCDC 在做增量扫描时对上游 TiKV 的影响 [#11390](https://github.com/tikv/tikv/issues/11390) @[hicqu](https://github.com/hicqu)

## 错误修复

+ TiDB

    - 修复 HashJoin 算子 Probe 时无法复用 chunk 的问题 [#48082](https://github.com/pingcap/tidb/issues/48082) @[wshwsh12](https://github.com/wshwsh12)
    - 修复 `AUTO_ID_CACHE=1` 时可能导致 `Duplicate entry` 的问题 [#46444](https://github.com/pingcap/tidb/issues/46444) @[tiancaiamao](https://github.com/tiancaiamao)
    - 修复当 JOIN 两个子查询时执行 `TIDB_INLJ` Hint 不生效的问题 [#46160](https://github.com/pingcap/tidb/issues/46160) @[qw4990](https://github.com/qw4990)
    - 修复 TiDB 重启后 DDL 操作可能卡住的问题 [#46751](https://github.com/pingcap/tidb/issues/46751) @[wjhuang2016](https://github.com/wjhuang2016)
    - 修复由于 MDL 处理不正确可能导致 DDL 永久阻塞的问题 [#46920](https://github.com/pingcap/tidb/issues/46920) @[wjhuang2016](https://github.com/wjhuang2016)
    - 修复 `MERGE_JOIN` 的结果错误的问题 [#46580](https://github.com/pingcap/tidb/issues/46580) @[qw4990](https://github.com/qw4990)
    - 修复 Sort 算子在落盘过程中可能导致 TiDB 崩溃的问题 [#47538](https://github.com/pingcap/tidb/issues/47538) @[windtalker](https://github.com/windtalker)
    - 修复 `cast(col)=range` 条件在 CAST 无精度损失的情况下会导致 FullScan 的问题 [#45199](https://github.com/pingcap/tidb/issues/45199) @[AilinKid](https://github.com/AilinKid)
    - 修复 `client-go` 中 `batch-client` panic 的问题 [#47691](https://github.com/pingcap/tidb/issues/47691) @[crazycs520](https://github.com/crazycs520)
    - 禁止非整型聚簇索引进行 split table 操作 [#47350](https://github.com/pingcap/tidb/issues/47350) @[tangenta](https://github.com/tangenta)
    - 修复时间转换时 Prepared Plan Cache 与 Non-Prepared Plan Cache 的行为不兼容性的问题 [#42439](https://github.com/pingcap/tidb/issues/42439) @[qw4990](https://github.com/qw4990)
    - 修复了部分情况下空表无法使用 ingest 模式添加索引的问题 [#39641](https://github.com/pingcap/tidb/issues/39641) @[tangenta](https://github.com/tangenta)
    - 修复交换分区时，无法检测出不符合分区定义的数据的问题 [#46492](https://github.com/pingcap/tidb/issues/46492) @[mjonss](https://github.com/mjonss)
    - 修复 `group_concat` 无法解析 `ORDER BY` 列的问题 [#41986](https://github.com/pingcap/tidb/issues/41986) @[AilinKid](https://github.com/AilinKid)
    - 修复深嵌套的表达式的 HashCode 重复计算导致的高内存占用和 OOM 问题 [#42788](https://github.com/pingcap/tidb/issues/42788) @[AilinKid](https://github.com/AilinKid)
    - 修复 MPP 执行计划中通过 Union 下推 Aggregation 导致的结果错误 [#45850](https://github.com/pingcap/tidb/issues/45850) @[AilinKid](https://github.com/AilinKid)
    - 修复 `INDEX_LOOKUP_HASH_JOIN` 内存使用量估算错误的问题 [#47788](https://github.com/pingcap/tidb/issues/47788) @[SeaRise](https://github.com/SeaRise)
    - 修复 `plan replayer` 生成的 zip 包无法被导入回 TiDB 的问题 [#46474](https://github.com/pingcap/tidb/issues/46474) @[YangKeao](https://github.com/YangKeao)
    - 修复当 `LIMIT N` 中的 N 过大时产生的错误代价估算 [#43285](https://github.com/pingcap/tidb/issues/43285) @[qw4990](https://github.com/qw4990)
    - 修复构造统计信息的 TopN 结构时可能发生的 panic 问题 [#35948](https://github.com/pingcap/tidb/issues/35948) @[hi-rustin](https://github.com/Rustin170506)
    - 修复 MPP 计算 `COUNT(INT)` 时结果可能出错的问题 [#48643](https://github.com/pingcap/tidb/issues/48643) @[AilinKid](https://github.com/AilinKid)
    - 修复 `tidb_enable_ordered_result_mode` 开启时可能发生 panic 的问题 [#45044](https://github.com/pingcap/tidb/issues/45044) @[qw4990](https://github.com/qw4990)
    - 修复优化器为减少窗口函数引入的 sort 而错误地选择了 `IndexFullScan` 的问题 [#46177](https://github.com/pingcap/tidb/issues/46177) @[qw4990](https://github.com/qw4990)
    - 修复谓词下推入公共表达式时结果可能出错的问题 [#47881](https://github.com/pingcap/tidb/issues/47881) @[winoros](https://github.com/winoros)
    - 修复 `UNION ALL` 第一个子节点是 DUAL Table 时，执行可能报错的问题 [#48755](https://github.com/pingcap/tidb/issues/48755) @[winoros](https://github.com/winoros)
    - 修复列裁剪在特定情况下会导致 panic 的问题 [#47331](https://github.com/pingcap/tidb/issues/47331) @[hi-rustin](https://github.com/Rustin170506)
    - 修复当包含聚合或者窗口函数的公共表达式被其他递归公共表达式引用时，可能抛出语法错误的问题 [#47603](https://github.com/pingcap/tidb/issues/47603) [#47711](https://github.com/pingcap/tidb/issues/47711)  @[elsa0520](https://github.com/elsa0520)
    - 修复在 prepare 语句中使用 `QB_NAME` hint 时可能执行异常的问题 [#46817](https://github.com/pingcap/tidb/issues/46817) @[jackysp](https://github.com/jackysp)
    - 修复使用 `AUTO_ID_CACHE=1` 时 Goroutine 泄漏的问题 [#46324](https://github.com/pingcap/tidb/issues/46324) @[tiancaiamao](https://github.com/tiancaiamao)
    - 修复 TiDB 在关闭时可能 panic 的问题 [#32110](https://github.com/pingcap/tidb/issues/32110) @[july2993](https://github.com/july2993)
    - 修复 TiDB schema cache 中读取 schema diff commit 版本时，未处理 MVCC 接口中的 lock 的问题 [#48281](https://github.com/pingcap/tidb/issues/48281) @[cfzjywxk](https://github.com/cfzjywxk)
    - 修复表改名导致 `information_schema.columns` 中出现重复行的问题 [#47064](https://github.com/pingcap/tidb/issues/47064) @[jiyfhust](https://github.com/jiyfhust)
    - 修复 `LOAD DATA REPLACE INTO` 语句的问题 [#47995](https://github.com/pingcap/tidb/issues/47995) @[lance6716](https://github.com/lance6716)
    - 修复 PD leader 故障 1 分钟导致 `IMPORT INTO` 任务失败的问题 [#48307](https://github.com/pingcap/tidb/issues/48307) @[D3Hunter](https://github.com/D3Hunter)
    - 修复创建日期型字段索引导致 `ADMIN CHECK` 失败的问题 [#47426](https://github.com/pingcap/tidb/issues/47426) @[tangenta](https://github.com/tangenta)
    - 修复 `TABLESAMPLE` 返回的行数据未排序的问题 [#48253](https://github.com/pingcap/tidb/issues/48253) @[tangenta](https://github.com/tangenta)
    - 修复当 DDL `jobID` 恢复为 0 时 TiDB 节点 panic 的问题 [#46296](https://github.com/pingcap/tidb/issues/46296) @[jiyfhust](https://github.com/jiyfhust)

+ TiKV

    - 修复在移动 Peer 时可能导致 Follower Read 性能变差的问题 [#15468](https://github.com/tikv/tikv/issues/15468) @[YuJuncen](https://github.com/YuJuncen)
    - 修复 raftstore-applys 不断增长的数据错误 [#15371](https://github.com/tikv/tikv/issues/15371) @[Connor1996](https://github.com/Connor1996)
    - 修复有线上负载时，TiDB Lightning 的 Checksum Coprocessor 请求超时的问题 [#15565](https://github.com/tikv/tikv/issues/15565) @[lance6716](https://github.com/lance6716)
    - 升级 `lz4-sys` 版本到 1.9.4 以修复安全问题 [#15621](https://github.com/tikv/tikv/issues/15621) @[SpadeA-Tang](https://github.com/SpadeA-Tang)
    - 升级 `tokio` 版本到 6.5 以修复安全问题 [#15621](https://github.com/tikv/tikv/issues/15621) @[LykxSassinator](https://github.com/LykxSassinator)
    - 移除存在安全问题的 `flatbuffer` [#15621](https://github.com/tikv/tikv/issues/15621) @[tonyxuqqi](https://github.com/tonyxuqqi)
    - 修复在 TiKV store 分区时，resolved-ts 延时变长的问题 [#15679](https://github.com/tikv/tikv/issues/15679) @[hicqu](https://github.com/hicqu)
    - 修复重启 TiKV 时，由于存在大量未 apply 的 Raft 日志导致的内存溢出问题 [#15770](https://github.com/tikv/tikv/issues/15770) @[overvenus](https://github.com/overvenus)
    - 修复 Region 合并后，历史 peer 残留并阻塞 resolved-ts 的问题 [#15919](https://github.com/tikv/tikv/issues/15919) @[overvenus](https://github.com/overvenus)
    - 修复云环境中 Grafana 中 scheduler 命令变量错误的问题 [#15832](https://github.com/tikv/tikv/issues/15832) @[Connor1996](https://github.com/Connor1996)
    - 修复 Titan `blob-run-mode` 无法在线更新的问题 [#15978](https://github.com/tikv/tikv/issues/15978) @[tonyxuqqi](https://github.com/tonyxuqqi)
    - 修复 Region 元信息不一致导致的 TiKV panic 问题 [#13311](https://github.com/tikv/tikv/issues/13311) @[cfzjywxk](https://github.com/cfzjywxk)
    - 修复 Online Unsafe Recovery 在 leader 强制退出时 panic 的问题 [#15629](https://github.com/tikv/tikv/issues/15629) @[Connor1996](https://github.com/Connor1996)
    - 修复扩容时可能导致 DR Auto-Sync 的 joint state 超时问题 [#15817](https://github.com/tikv/tikv/issues/15817) @[Connor1996](https://github.com/Connor1996)
    - 修复 TiKV coprocessor 在移除 Raft peer 时可能返回陈旧数据的问题 [#16069](https://github.com/tikv/tikv/issues/16069) @[overvenus](https://github.com/overvenus)
    - 修复 resolved-ts 可能被阻塞 2 小时的问题 [#39130](https://github.com/pingcap/tidb/issues/39130) @[overvenus](https://github.com/overvenus)
    - 修复在 Flashback 时遇到 `notLeader` 或 `regionNotFound` 时卡住的问题 [#15712](https://github.com/tikv/tikv/issues/15712) @[HuSharp](https://github.com/HuSharp)

+ PD

    - 修复 Plugin 目录、文件内容可能存在安全隐患的问题 [#7094](https://github.com/tikv/pd/issues/7094) @[HuSharp](https://github.com/HuSharp)
    - 修复修改隔离等级时未同步到默认放置规则中的问题 [#7121](https://github.com/tikv/pd/issues/7121) @[rleungx](https://github.com/rleungx)
    - 修复 `evict-leader-scheduler` 丢失配置的问题 [#6897](https://github.com/tikv/pd/issues/6897) @[HuSharp](https://github.com/HuSharp)
    - 修复空 Region 的统计方法可能导致 BR 恢复过程中 Region 不均衡的问题 [#7148](https://github.com/tikv/pd/issues/7148) @[Cabinfever](https://github.com/CabinfeverB)
    - 修复采用自适应同步部署模式 (DR Auto-Sync) 的集群在 Placement Rule 的配置较复杂时，`canSync` 和 `hasMajority` 可能计算错误的问题 [#7201](https://github.com/tikv/pd/issues/7201) @[disksing](https://github.com/disksing)
    - 修复采用自适应同步部署模式 (DR Auto-Sync) 的集群 `available_stores` 计算错误的问题 [#7221](https://github.com/tikv/pd/issues/7221) @[disksing](https://github.com/disksing)
    - 修复采用自适应同步部署模式 (DR Auto-Sync) 的集群在从 AZ 宕机时主 AZ 不能添加 TiKV 节点的问题 [#7218](https://github.com/tikv/pd/issues/7218) @[disksing](https://github.com/disksing)
    - 修复在大集群中添加多个 TiKV 节点可能导致 TiKV 心跳上报变慢或卡住的问题 [#7248](https://github.com/tikv/pd/issues/7248) @[rleungx](https://github.com/rleungx)
    - 修复当 TiKV 节点不可用时 PD 可能删除正常 Peers 的问题 [#7249](https://github.com/tikv/pd/issues/7249) @[lhy1024](https://github.com/lhy1024)
    - 修复自适应同步部署模式 (DR Auto-Sync) 下 leader 切换时间过长的问题 [#6988](https://github.com/tikv/pd/issues/6988) @[HuSharp](https://github.com/HuSharp)
    - 将 Gin Web Framework 的版本从 v1.8.1 升级到 v1.9.1 以修复部分安全问题 [#7438](https://github.com/tikv/pd/issues/7438) @[niubell](https://github.com/niubell)

+ TiFlash

    - 修复 Grafana 的 Read Snapshots 面板上 `max_snapshot_lifetime` 监控指标显示有误的问题 [#7713](https://github.com/pingcap/tiflash/issues/7713) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复执行 `ALTER TABLE ... EXCHANGE PARTITION ...` 语句后 panic 的问题 [#8372](https://github.com/pingcap/tiflash/issues/8372) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复 MemoryTracker 提供的内存使用数据不准确的问题 [#8128](https://github.com/pingcap/tiflash/issues/8128) @[JinheLin](https://github.com/JinheLin)

+ Tools

    + Backup & Restore (BR)

        - 修复大宽表场景下，日志备份在某些场景中可能卡住的问题 [#15714](https://github.com/tikv/tikv/issues/15714) @[YuJuncen](https://github.com/YuJuncen)
        - 修复频繁 Flush 导致日志部分卡死的问题 [#15602](https://github.com/tikv/tikv/issues/15602) @[3pointer](https://github.com/3pointer)
        - 修复在 EC2 metadata 连接被重置后，重试导致备份恢复性能下降的问题 [#47650](https://github.com/pingcap/tidb/issues/47650) @[Leavrth](https://github.com/Leavrth)
        - 修复 1 分钟之内多次执行 PITR 可能导致数据丢失的问题 [#15483](https://github.com/tikv/tikv/issues/15483) @[YuJuncen](https://github.com/YuJuncen)
        - 修复由于 BR SQL 命令和 CLI 的默认参数不同可能导致的 OOM 问题 [#48000](https://github.com/pingcap/tidb/issues/48000) @[YuJuncen](https://github.com/YuJuncen)
        - 修复 PD Owner 转移时，日志备份可能 panic 的问题 [#47533](https://github.com/pingcap/tidb/issues/47533) @[YuJuncen](https://github.com/YuJuncen)
        - 修复生成外部存储文件 URI 错误的问题 [#48452](https://github.com/pingcap/tidb/issues/48452) @[3AceShowHand](https://github.com/3AceShowHand)

    + TiCDC

        - 修复上游在执行有损 DDL 时，TiCDC Server 可能 panic 的问题 [#9739](https://github.com/pingcap/tiflow/issues/9739) @[hicqu](https://github.com/hicqu)
        - 修复在开启 redo log 功能后，执行 `RESUME` 时同步任务报错的问题 [#9769](https://github.com/pingcap/tiflow/issues/9769) @[hicqu](https://github.com/hicqu)
        - 修复 TiKV 节点 crash 时，同步延迟变长的问题 [#9741](https://github.com/pingcap/tiflow/issues/9741) @[sdojjy](https://github.com/sdojjy)
        - 修复同步数据到 TiDB 或 MySQL 时，`WHERE` 语句没有采用主键作为条件的问题 [#9988](https://github.com/pingcap/tiflow/issues/9988) @[asddongmen](https://github.com/asddongmen)
        - 修复同步任务在 TiCDC 节点分配不均衡的问题 [#9839](https://github.com/pingcap/tiflow/issues/9839) @[3AceShowHand](https://github.com/3AceShowHand)
        - 修复 redo log 开启时，DDL 同步时间间隔过长的问题 [#9960](https://github.com/pingcap/tiflow/issues/9960) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - 修复开启双向复制时，`DROP` 一张表后再重新 `CREATE` 该表，Changefeed 无法同步 DML 事件的问题 [#10079](https://github.com/pingcap/tiflow/issues/10079) @[asddongmen](https://github.com/asddongmen)
        - 修复同步数据到对象存储时，NFS 文件过多导致同步延迟变长的问题 [#10041](https://github.com/pingcap/tiflow/issues/10041) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - 修复同步数据到对象存储时，可能会出现 TiCDC Server panic 的问题 [#10137](https://github.com/pingcap/tiflow/issues/10137) @[sdojjy](https://github.com/sdojjy)
        - 修复 PD 做扩缩容场景下 TiCDC 访问无效旧地址的问题 [#9584](https://github.com/pingcap/tiflow/issues/9584) @[fubinzh](https://github.com/fubinzh) @[asddongmen](https://github.com/asddongmen)
        - 修复在某些特殊的操作系统下，获取错误内存信息可能导致 OOM 的问题 [#9762](https://github.com/pingcap/tiflow/issues/9762) @[sdojjy](https://github.com/sdojjy)

    + TiDB Data Migration (DM)

        - 修复 DM 在乐观模式中跳过 Partition DDL 的问题 [#9788](https://github.com/pingcap/tiflow/issues/9788) @[GMHDBJD](https://github.com/GMHDBJD)
        - 修复 DM 在跳过 Online DDL 时无法正确追踪上游表结构的问题 [#9587](https://github.com/pingcap/tiflow/issues/9587) @[GMHDBJD](https://github.com/GMHDBJD)
        - 修复 DM 在跳过失败 DDL 并且后续无 DDL 执行时显示延迟持续增长的问题 [#9605](https://github.com/pingcap/tiflow/issues/9605) @[D3Hunter](https://github.com/D3Hunter)
        - 修复 DM 在乐观模式恢复任务时跳过所有 DML 的问题 [#9588](https://github.com/pingcap/tiflow/issues/9588) @[GMHDBJD](https://github.com/GMHDBJD)

    + TiDB Lightning

        - 修复遇到 `write to tikv with no leader returned` 错误时数据导入失败的问题 [#45673](https://github.com/pingcap/tidb/issues/45673) @[lance6716](https://github.com/lance6716)
        - 修复 HTTP 重试请求未使用本次的请求内容导致导入失败的问题 [#47930](https://github.com/pingcap/tidb/issues/47930) @[lance6716](https://github.com/lance6716)
        - 修复 TiDB Lightning 在 `writeToTiKV` 时卡住的问题 [#46321](https://github.com/pingcap/tidb/issues/46321) @[lance6716](https://github.com/lance6716)
        - 移除物理导入模式下不必要的 `get_regions` 调用 [#45507](https://github.com/pingcap/tidb/issues/45507) @[mittalrishabh](https://github.com/mittalrishabh)

    + TiDB Binlog

        - 修复传输事务超过 1 GB 时 Drainer 会退出的问题 [#28659](https://github.com/pingcap/tidb/issues/28659) @[jackysp](https://github.com/jackysp)