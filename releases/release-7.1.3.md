---
title: TiDB 7.1.3 Release Notes
summary: 了解 TiDB 7.1.3 版本的兼容性变更、改进提升，以及错误修复。
---

# TiDB 7.1.3 Release Notes

发版日期：2023 年 12 月 21 日

TiDB 版本：7.1.3

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v7.1/quick-start-with-tidb) | [生产部署](https://docs.pingcap.com/zh/tidb/v7.1/production-deployment-using-tiup) | [下载离线包](https://cn.pingcap.com/product-community/?version=v7.1.3#version-list)

## 兼容性变更

- 经进一步的测试后，TiCDC Changefeed 配置项 [`case-sensitive`](/ticdc/ticdc-changefeed-config.md) 默认值由 `true` 改为 `false`，即默认情况下 TiCDC 配置文件中涉及的表名、库名大小写不敏感 [#10047](https://github.com/pingcap/tiflow/issues/10047) @[sdojjy](https://github.com/sdojjy)
- TiCDC Changefeed 新增以下配置项：
    - [`sql-mode`](/ticdc/ticdc-changefeed-config.md)：你可以设置 TiCDC 同步数据时解析 DDL 语句所使用的 [SQL 模式](https://docs.pingcap.com/zh/tidb/v7.1/ticdc-ddl#sql-模式) [#9876](https://github.com/pingcap/tiflow/issues/9876) @[asddongmen](https://github.com/asddongmen)
    - [`encoding-worker-num`](/ticdc/ticdc-changefeed-config.md) 和 [`flush-worker-num`](/ticdc/ticdc-changefeed-config.md)：你可以根据不同的机器规格，设置 redo 模块不同的并发参数 [#10048](https://github.com/pingcap/tiflow/issues/10048) @[CharlesCheung96](https://github.com/CharlesCheung96)
    - [`compression`](/ticdc/ticdc-changefeed-config.md)：你可以设置 redo log 文件的压缩行为 [#10176](https://github.com/pingcap/tiflow/issues/10176) @[sdojjy](https://github.com/sdojjy)
    - [`sink.cloud-storage-config`](/ticdc/ticdc-changefeed-config.md)：你可以设置同步数据到对象存储时自动清理历史数据的功能 [#10109](https://github.com/pingcap/tiflow/issues/10109) @[CharlesCheung96](https://github.com/CharlesCheung96)

## 改进提升

+ TiDB

    - 新增支持 [`FLASHBACK CLUSTER TO TSO`](https://docs.pingcap.com/zh/tidb/v7.1/sql-statement-flashback-cluster) 语法 [#48372](https://github.com/pingcap/tidb/issues/48372) @[BornChanger](https://github.com/BornChanger)

+ PD

    - 改进 resource control client 的配置获取方式，使其可以动态获取最新配置 [#7043](https://github.com/tikv/pd/issues/7043) @[nolouch](https://github.com/nolouch)

+ Tools

    + Backup & Restore (BR)

        - 当遇到 Region 打散超时失败或被取消的情况时，快照恢复支持自动重试 Region 打散 [#47236](https://github.com/pingcap/tidb/issues/47236) @[Leavrth](https://github.com/Leavrth)
        - 快照备份恢复在遇到某些网络错误时会进行重试 [#48528](https://github.com/pingcap/tidb/issues/48528) @[Leavrth](https://github.com/Leavrth)
        - 新增 PITR 对 delete range 场景的集成测试，提升 PITR 稳定性 [#47738](https://github.com/pingcap/tidb/issues/47738) @[Leavrth](https://github.com/Leavrth)

    + TiCDC

        - 优化 TiCDC 节点同步数据到 TiDB 时的内存消耗 [#9935](https://github.com/pingcap/tiflow/issues/9935) @[3AceShowHand](https://github.com/3AceShowHand)
        - 优化部分报警规则 [#9266](https://github.com/pingcap/tiflow/issues/9266) @[asddongmen](https://github.com/asddongmen)
        - 优化了 redo log 的相关性能，包括并行写入 S3 和支持 lz4 压缩算法 [#10176](https://github.com/pingcap/tiflow/issues/10176) [#10226](https://github.com/pingcap/tiflow/issues/10226) @[sdojjy](https://github.com/sdojjy)
        - 通过增加并行，优化了 TiCDC 同步数据到对象存储的性能 [#10098](https://github.com/pingcap/tiflow/issues/10098) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - 减少 TiCDC 在做增量扫描时对上游 TiKV 的影响 [#11390](https://github.com/tikv/tikv/issues/11390) @[hicqu](https://github.com/hicqu)
        - 支持通过在 `sink-uri` 中设置 `content-compatible=true` 使 TiCDC Canal-JSON [兼容 Canal 官方输出的内容格式](/ticdc/ticdc-canal-json.md#兼容-canal-官方实现) [#10106](https://github.com/pingcap/tiflow/issues/10106) @[3AceShowHand](https://github.com/3AceShowHand)

    + TiDB Lightning

        - 增加由于 PD Leader change 导致 `GetTS` 失败的重试机制 [#45301](https://github.com/pingcap/tidb/issues/45301) @[lance6716](https://github.com/lance6716)

## 错误修复

+ TiDB

    - 修复当内存使用超限时包含公共表表达式 (CTE) 的查询非预期卡住的问题 [#49096](https://github.com/pingcap/tidb/issues/49096) @[AilinKid](https://github.com/AilinKid)
    - 修复 `tidb_server_memory_limit` 导致内存长期压力较高时，TiDB CPU 利用率过高的问题 [#48741](https://github.com/pingcap/tidb/issues/48741) @[XuHuaiyu](https://github.com/XuHuaiyu)
    - 修复 `tidb_max_chunk_size` 值较小时，包含 CTE 的查询出现 `runtime error: index out of range [32] with length 32` 错误的问题 [#48808](https://github.com/pingcap/tidb/issues/48808) @[guo-shaoge](https://github.com/guo-shaoge)
    - 修复 `ENUM` 类型列作为 join 键时，查询结果错误的问题 [#48991](https://github.com/pingcap/tidb/issues/48991) @[winoros](https://github.com/winoros)
    - 修复递归 CTE 中包含聚合函数或者窗口函数导致的解析错误 [#47711](https://github.com/pingcap/tidb/issues/47711) @[elsa0520](https://github.com/elsa0520)
    - 修复 `UPDATE` 语句可能被错误地转成 PointGet 的问题 [#47445](https://github.com/pingcap/tidb/issues/47445) @[hi-rustin](https://github.com/Rustin170506)
    - 修复对 `stats_history` 表进行垃圾回收时可能导致 OOM 的问题 [#48431](https://github.com/pingcap/tidb/issues/48431) @[hawkingrei](https://github.com/hawkingrei)
    - 修复某些情况下相同的查询计划拥有不同的 `PLAN_DIGEST` 的问题 [#47634](https://github.com/pingcap/tidb/issues/47634) @[King-Dylan](https://github.com/King-Dylan)
    - 修复 `GenJSONTableFromStats` 占用大量内存时无法被 kill 的问题 [#47779](https://github.com/pingcap/tidb/issues/47779) @[hawkingrei](https://github.com/hawkingrei)
    - 修复谓词下推入公共表达式时结果可能出错的问题 [#47881](https://github.com/pingcap/tidb/issues/47881) @[winoros](https://github.com/winoros)
    - 修复 `AUTO_ID_CACHE=1` 时可能导致 `Duplicate entry` 的问题 [#46444](https://github.com/pingcap/tidb/issues/46444) @[tiancaiamao](https://github.com/tiancaiamao)
    - 修复 TiDB server 在使用企业插件审计日志时可能占用大量资源的问题 [#49273](https://github.com/pingcap/tidb/issues/49273) @[lcwangchao](https://github.com/lcwangchao)
    - 修复 TiDB server 在优雅关闭 (graceful shutdown) 时可能 panic 的问题 [#36793](https://github.com/pingcap/tidb/issues/36793) @[bb7133](https://github.com/bb7133)
    - 修复在有大量表时，`AUTO_ID_CACHE=1` 的表可能造成 gRPC 客户端泄漏的问题 [#48869](https://github.com/pingcap/tidb/issues/48869) @[tiancaiamao](https://github.com/tiancaiamao)
    - 修复 `ErrLoadDataInvalidURI`（无效的 S3 URI 错误）报错中的信息内容 [#48164](https://github.com/pingcap/tidb/issues/48164) @[lance6716](https://github.com/lance6716)
    - 修复当分区列类型为 `DATETIME` 时，执行 `ALTER TABLE ... LAST PARTITION` 失败的问题 [#48814](https://github.com/pingcap/tidb/issues/48814) @[crazycs520](https://github.com/crazycs520)
    - 修复执行 `IMPORT INTO` 时，真实错误信息可能被其它错误信息覆盖的问题 [#47992](https://github.com/pingcap/tidb/issues/47992) [#47781](https://github.com/pingcap/tidb/issues/47781) @[D3Hunter](https://github.com/D3Hunter)
    - 修复无法检测到 TiDB 部署在 cgroup v2 容器的问题 [#48342](https://github.com/pingcap/tidb/issues/48342) @[D3Hunter](https://github.com/D3Hunter)
    - 修复 `UNION ALL` 第一个子节点是 DUAL Table 时，执行可能报错的问题 [#48755](https://github.com/pingcap/tidb/issues/48755) @[winoros](https://github.com/winoros)
    - 修复当 DDL `jobID` 恢复为 0 时 TiDB 节点 panic 的问题 [#46296](https://github.com/pingcap/tidb/issues/46296) @[jiyfhust](https://github.com/jiyfhust)
    - 修复 `TABLESAMPLE` 返回的行数据未排序的问题 [#48253](https://github.com/pingcap/tidb/issues/48253) @[tangenta](https://github.com/tangenta)
    - 修复 `tidb_enable_ordered_result_mode` 开启时可能发生 panic 的问题 [#45044](https://github.com/pingcap/tidb/issues/45044) @[qw4990](https://github.com/qw4990)
    - 修复优化器为减少窗口函数引入的 sort 而错误地选择了 `IndexFullScan` 的问题 [#46177](https://github.com/pingcap/tidb/issues/46177) @[qw4990](https://github.com/qw4990)
    - 修复 TiDB schema cache 中读取 schema diff commit 版本时，未处理 MVCC 接口中的 lock 的问题 [#48281](https://github.com/pingcap/tidb/issues/48281) @[cfzjywxk](https://github.com/cfzjywxk)
    - 修复 `INDEX_LOOKUP_HASH_JOIN` 内存使用量估算错误的问题 [#47788](https://github.com/pingcap/tidb/issues/47788) @[SeaRise](https://github.com/SeaRise)
    - 修复 PD leader 故障 1 分钟导致 `IMPORT INTO` 任务失败的问题 [#48307](https://github.com/pingcap/tidb/issues/48307) @[D3Hunter](https://github.com/D3Hunter)
    - 修复 `client-go` 中 `batch-client` panic 的问题 [#47691](https://github.com/pingcap/tidb/issues/47691) @[crazycs520](https://github.com/crazycs520)
    - 修复列裁剪在特定情况下会导致 panic 的问题 [#47331](https://github.com/pingcap/tidb/issues/47331) @[hi-rustin](https://github.com/Rustin170506)
    - 修复 TiDB 在通过 `systemd` 启动时无法读取 `cgroup` 资源限制的问题 [#47442](https://github.com/pingcap/tidb/issues/47442) @[hawkingrei](https://github.com/hawkingrei)
    - 修复当包含聚合或者窗口函数的公共表达式被其他递归公共表达式引用时，可能抛出语法错误的问题 [#47603](https://github.com/pingcap/tidb/issues/47603) [#47711](https://github.com/pingcap/tidb/issues/47711)  @[elsa0520](https://github.com/elsa0520)
    - 修复构造统计信息的 TopN 结构时可能发生的 panic 问题 [#35948](https://github.com/pingcap/tidb/issues/35948) @[hi-rustin](https://github.com/Rustin170506)
    - 修复 MPP 计算 `COUNT(INT)` 时结果可能出错的问题 [#48643](https://github.com/pingcap/tidb/issues/48643) @[AilinKid](https://github.com/AilinKid)
    - 修复 HashJoin 算子 Probe 时无法复用 chunk 的问题 [#48082](https://github.com/pingcap/tidb/issues/48082) @[wshwsh12](https://github.com/wshwsh12)

+ TiKV

    - 修复如果 TiKV 运行极慢，在 Region Merge 之后可能 panic 的问题 [#16111](https://github.com/tikv/tikv/issues/16111) @[overvenus](https://github.com/overvenus)
    - 修复 Resolved TS 可能被阻塞两小时的问题 [#15520](https://github.com/tikv/tikv/issues/15520) [#39130](https://github.com/pingcap/tidb/issues/39130) @[overvenus](https://github.com/overvenus)
    - 修复 TiKV 由于无法 append Raft log 导致报错 `ServerIsBusy` [#15800](https://github.com/tikv/tikv/issues/15800) @[tonyxuqqi](https://github.com/tonyxuqqi)
    - 修复 BR 崩溃时快照备份卡住的问题 [#15684](https://github.com/tikv/tikv/issues/15684) @[YuJuncen](https://github.com/YuJuncen)
    - 修复跟踪大型事务时，Stale Read 中的 Resolved TS 可能导致 TiKV OOM 的问题 [#14864](https://github.com/tikv/tikv/issues/14864) @[overvenus](https://github.com/overvenus)
    - 修复损坏的 SST 文件可能会扩散到其他 TiKV 节点的问题 [#15986](https://github.com/tikv/tikv/issues/15986) @[Connor1996](https://github.com/Connor1996)
    - 修复扩容时可能导致 DR Auto-Sync 的 joint state 超时问题 [#15817](https://github.com/tikv/tikv/issues/15817) @[Connor1996](https://github.com/Connor1996)
    - 修复云环境中 Grafana 中 scheduler 命令变量错误的问题 [#15832](https://github.com/tikv/tikv/issues/15832) @[Connor1996](https://github.com/Connor1996)
    - 修复 Region 合并后，历史 peer 残留并阻塞 resolved-ts 的问题 [#15919](https://github.com/tikv/tikv/issues/15919) @[overvenus](https://github.com/overvenus)
    - 修复 Online Unsafe Recovery 时无法处理 merge abort 的问题 [#15580](https://github.com/tikv/tikv/issues/15580) @[v01dstar](https://github.com/v01dstar)
    - 修复重启 TiKV 时，由于存在大量未 apply 的 Raft 日志导致的内存溢出问题 [#15770](https://github.com/tikv/tikv/issues/15770) @[overvenus](https://github.com/overvenus)
    - 升级 `lz4-sys` 版本到 1.9.4 以修复安全问题 [#15621](https://github.com/tikv/tikv/issues/15621) @[SpadeA-Tang](https://github.com/SpadeA-Tang)
    - 修复 Titan `blob-run-mode` 无法在线更新的问题 [#15978](https://github.com/tikv/tikv/issues/15978) @[tonyxuqqi](https://github.com/tonyxuqqi)
    - 修复 PD 和 TiKV 之间的网络中断可能导致 PITR 卡住的问题 [#15279](https://github.com/tikv/tikv/issues/15279) @[YuJuncen](https://github.com/YuJuncen)
    - 修复 TiKV coprocessor 在移除 Raft peer 时可能返回陈旧数据的问题 [#16069](https://github.com/tikv/tikv/issues/16069) @[overvenus](https://github.com/overvenus)

+ PD

    - 修复执行 `CALIBRATE RESOURCE` 导致 TiDB Dashboard 上的 `resource_manager_resource_unit` metric 为空的问题 [#45166](https://github.com/pingcap/tidb/issues/45166) @[CabinfeverB](https://github.com/CabinfeverB)
    - 修复 Calibrate by Workload 页面报错的问题 [#48162](https://github.com/pingcap/tidb/issues/48162) @[CabinfeverB](https://github.com/CabinfeverB)
    - 修复删除 Resource Group 可能破坏 DDL 原子性的问题 [#45050](https://github.com/pingcap/tidb/issues/45050) @[glorv](https://github.com/glorv)
    - 修复 PD Leader 切换且新 Leader 与调用方之间存在网络隔离时，调用方不能正常更新 Leader 信息的问题 [#7416](https://github.com/tikv/pd/issues/7416) @[CabinfeverB](https://github.com/CabinfeverB)
    - 修复在大集群中添加多个 TiKV 节点可能导致 TiKV 心跳上报变慢或卡住的问题 [#7248](https://github.com/tikv/pd/issues/7248) @[rleungx](https://github.com/rleungx)
    - 修复 TiDB Dashboard 不能正常读取 PD `trace` 数据的问题 [#7253](https://github.com/tikv/pd/issues/7253) @[nolouch](https://github.com/nolouch)
    - 将 Gin Web Framework 的版本从 v1.8.1 升级到 v1.9.1 以修复部分安全问题 [#7438](https://github.com/tikv/pd/issues/7438) @[niubell](https://github.com/niubell)
    - 修复 rule checker 未按照设定的 Placement Rule 添加 Learner 的问题 [#7185](https://github.com/tikv/pd/issues/7185) @[nolouch](https://github.com/nolouch)
    - 修复当 TiKV 节点不可用时 PD 可能删除正常 Peers 的问题 [#7249](https://github.com/tikv/pd/issues/7249) @[lhy1024](https://github.com/lhy1024)
    - 修复自适应同步部署模式 (DR Auto-Sync) 下 leader 切换时间过长的问题 [#6988](https://github.com/tikv/pd/issues/6988) @[HuSharp](https://github.com/HuSharp)

+ TiFlash

    - 修复执行 `ALTER TABLE ... EXCHANGE PARTITION ...` 语句后 panic 的问题 [#8372](https://github.com/pingcap/tiflash/issues/8372) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复当查询遇到内存限制后发生内存泄漏的问题 [#8447](https://github.com/pingcap/tiflash/issues/8447) @[JinheLin](https://github.com/JinheLin)
    - 修复在执行 `FLASHBACK DATABASE` 后 TiFlash 副本的数据仍会被 GC 回收的问题 [#8450](https://github.com/pingcap/tiflash/issues/8450) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复 Grafana 中部分面板的最大分位数耗时显示不正确的问题 [#8076](https://github.com/pingcap/tiflash/issues/8076) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复查询非预期报错 `Block schema mismatch in FineGrainedShuffleWriter-V1` 的问题 [#8111](https://github.com/pingcap/tiflash/issues/8111) @[SeaRise](https://github.com/SeaRise)

+ Tools

    + Backup & Restore (BR)

        - 修复由于 BR SQL 命令和 CLI 的默认参数不同可能导致的 OOM 问题 [#48000](https://github.com/pingcap/tidb/issues/48000) @[YuJuncen](https://github.com/YuJuncen)
        - 修复大宽表场景下，日志备份在某些场景中可能卡住的问题 [#15714](https://github.com/tikv/tikv/issues/15714) @[YuJuncen](https://github.com/YuJuncen)
        - 修复生成外部存储文件 URI 错误的问题 [#48452](https://github.com/pingcap/tidb/issues/48452) @[3AceShowHand](https://github.com/3AceShowHand)
        - 修复在 EC2 metadata 连接被重置后，重试导致备份恢复性能下降的问题 [#47650](https://github.com/pingcap/tidb/issues/47650) @[Leavrth](https://github.com/Leavrth)
        - 修复在任务初始化阶段出现与 PD 的连接错误导致日志备份任务虽然启动但无法正常工作的问题 [#16056](https://github.com/tikv/tikv/issues/16056) @[YuJuncen](https://github.com/YuJuncen)

    + TiCDC

        - 修复某些场景下在同步 `DELETE` 语句时，`WHERE` 条件没有采用主键作为条件的问题 [#9812](https://github.com/pingcap/tiflow/issues/9812) @[asddongmen](https://github.com/asddongmen)
        - 修复同步数据到对象存储时，某些特殊场景下同步任务卡住的问题 [#10041](https://github.com/pingcap/tiflow/issues/10041) [#10044](https://github.com/pingcap/tiflow/issues/10044) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - 修复在开启 sync-point 和 redo log 后，某些特殊场景下同步任务卡住的问题 [#10091](https://github.com/pingcap/tiflow/issues/10091) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - 修复在某些特殊场景下，TiCDC 错误地关闭与 TiKV 的连接的问题 [#10239](https://github.com/pingcap/tiflow/issues/10239) @[hicqu](https://github.com/hicqu)
        - 修复开启双向复制时，`DROP` 一张表后再重新 `CREATE` 该表，Changefeed 无法同步 DML 事件的问题 [#10079](https://github.com/pingcap/tiflow/issues/10079) @[asddongmen](https://github.com/asddongmen)
        - 修复同步数据到对象存储时，访问 NFS 目录导致的性能问题 [#10041](https://github.com/pingcap/tiflow/issues/10041) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - 修复同步数据到对象存储时，可能会出现 TiCDC Server panic 的问题 [#10137](https://github.com/pingcap/tiflow/issues/10137) @[sdojjy](https://github.com/sdojjy)
        - 修复 redo log 开启时，DDL 同步时间间隔过长的问题 [#9960](https://github.com/pingcap/tiflow/issues/9960) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - 修复开启 redo log 时，NFS 出现故障导致 Owner 节点卡住的问题 [#9886](https://github.com/pingcap/tiflow/issues/9886) @[3AceShowHand](https://github.com/3AceShowHand)

    + TiDB Data Migration (DM)

        - 修复 `CompareGTID` 采用不合适的算法导致 DM 性能下降的问题 [#9676](https://github.com/pingcap/tiflow/issues/9676) @[GMHDBJD](https://github.com/GMHDBJD)

    + TiDB Lightning

        - 修复由于 PD Leader 被 KILL 或 PD 请求处理慢导致数据导入失败的问题 [#46950](https://github.com/pingcap/tidb/issues/46950) [#48075](https://github.com/pingcap/tidb/issues/48075) @[D3Hunter](https://github.com/D3Hunter)
        - 修复 TiDB Lightning 在 `writeToTiKV` 时卡住的问题 [#46321](https://github.com/pingcap/tidb/issues/46321) [#48352](https://github.com/pingcap/tidb/issues/48352) @[lance6716](https://github.com/lance6716)
        - 修复 HTTP 重试请求未使用本次的请求内容导致导入失败的问题 [#47930](https://github.com/pingcap/tidb/issues/47930) @[lance6716](https://github.com/lance6716)
        - 移除物理导入模式下不必要的 `get_regions` 调用 [#45507](https://github.com/pingcap/tidb/issues/45507) @[mittalrishabh](https://github.com/mittalrishabh)
