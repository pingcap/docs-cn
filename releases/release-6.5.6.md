---
title: TiDB 6.5.6 Release Notes
summary: 了解 TiDB 6.5.6 版本的兼容性变更、改进提升，以及错误修复。
---

# TiDB 6.5.6 Release Notes

发版日期：2023 年 x 月 x 日

TiDB 版本：6.5.6

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v6.5/quick-start-with-tidb) | [生产部署](https://docs.pingcap.com/zh/tidb/v6.5/production-deployment-using-tiup) | [下载离线包](https://cn.pingcap.com/product-community/?version=v6.5.6#version-list)

## 兼容性变更  **tw@qiancai --2 条**

- 经进一步的测试后，TiCDC 配置项 [`case-sensitive`](/ticdc/ticdc-changefeed-config.md) 默认值由 `true` 改为 `false`，即默认情况下 TiCDC 配置文件中涉及的表名、库名大小写不敏感 [#10047](https://github.com/pingcap/tiflow/issues/10047) @[sdojjy](https://github.com/sdojjy)
- 在 SEM 模式下禁止设置 `require_secure_transport` 为 `ON` [#47665](https://github.com/pingcap/tidb/issues/47665) @[tiancaiamao](https://github.com/tiancaiamao)
- (dup): release-7.1.2.md > 改进提升> TiKV - 引入系统变量 [`tidb_opt_enable_hash_join`](https://docs.pingcap.com/zh/tidb/v7.1/system-variables#tidb_opt_enable_hash_join-从-v712-版本开始引入) 控制是否选择表的哈希连接 [#46695](https://github.com/pingcap/tidb/issues/46695) @[coderplay](https://github.com/coderplay)

## 改进提升

+ TiKV **tw@Oreoxmt --1 条**

    - (dup): release-7.4.0.md > 改进提升> TiKV - 改进 Resolver 的内存使用，防止 OOM [#15458](https://github.com/tikv/tikv/issues/15458) @[overvenus](https://github.com/overvenus)
    - (dup): release-7.1.2.md > 改进提升> TiKV - 优化数据整理检查机制，当触发 Region Split 时，如果没有可以分裂的 key，触发一次数据整理，以消除过多的 MVCC 版本 [#15282](https://github.com/tikv/tikv/issues/15282) @[SpadeA-Tang](https://github.com/SpadeA-Tang)
    - (dup): release-7.4.0.md > 改进提升> TiKV - 消除 Router 对象中的 LRUCache，降低内存占用，防止 OOM [#15430](https://github.com/tikv/tikv/issues/15430) @[Connor1996](https://github.com/Connor1996)
    - 将 `apply_router` 和 `raft_router` 的指标拆分为 alive 和 leak 分开监控。[#15357](https://github.com/tikv/tikv/issues/15357)@[tonyxuqqi](https://github.com/tonyxuqqi)

+ PD **tw@qiancai --1 条**

    - 为 DR Auto-Sync 添加 Status 和 Sync Progress 面板 [#6975](https://github.com/tikv/pd/issues/6975) @[disksing](https://github.com/disksing)

+ Tools

    + Backup & Restore (BR) **tw@qiancai --4 条**

        - (dup): release-7.5.0.md > 改进提升> BR - 快照备份恢复在遇到某些网络错误时会进行重试 [#48528](https://github.com/pingcap/tidb/issues/48528) @[Leavrth](https://github.com/Leavrth)
        - 增加 pitr 对 delete range 场景的集成测试 [#47738](https://github.com/pingcap/tidb/issues/47738) @[Leavrth](https://github.com/Leavrth)
        - 提供了 flashback cluster to tso 语法支持 [#48372](https://github.com/pingcap/tidb/issues/48372) @[BornChanger](https://github.com/BornChanger)
        - 快照恢复增加对 region 打散超时失败或者被取消情况下的重试 [#47236](https://github.com/pingcap/tidb/issues/47236) @[Leavrth](https://github.com/Leavrth)
        - 使用 merge-schedule-limit 配置项来暂停 pd merge [#7148](https://github.com/tikv/pd/issues/7148) @[BornChanger](https://github.com/3pointer)

    + TiCDC **tw@qiancai  --5 条**

        - 增加 redo 模块的调优配置，用户可以根据不同的机器规格，设置不同的并发参数 [#10048](https://github.com/pingcap/tiflow/issues/10048) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - 增加同步到对象存储时，用户可以设置自动清理历史数据的功能 [#10109](https://github.com/pingcap/tiflow/issues/10109) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - 增加控制参数，可以设置 redo 文件的压缩算法 [#10176](https://github.com/pingcap/tiflow/issues/10176)
        - 增加控制参数，可以设置与标准的 canal-json 协议完全兼容的模式 [#10106](https://github.com/pingcap/tiflow/issues/10106) @[3AceShowHand](https://github.com/3AceShowHand)
        - (dup): release-7.4.0.md > 改进提升> Tools> TiCDC - 优化同步 `ADD INDEX` DDL 的执行逻辑，从而不阻塞后续的 DML 语句 [#9644](https://github.com/pingcap/tiflow/issues/9644) @[sdojjy](https://github.com/sdojjy)

    + TiDB Data Migration (DM)

        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + TiDB Lightning

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + Dumpling

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + TiUP

        - note [#issue](https://github.com/pingcap/tiup/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiup/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + TiDB Binlog

        - note [#issue](https://github.com/pingcap/tidb-binlog/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb-binlog/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

## 错误修复

+ TiDB **tw@ran-huang --19 条**

    - (dup): release-7.5.0.md > 错误修复> TiDB - 修复 HashJoin 算子 Probe 时无法复用 chunk 的问题 [#48082](https://github.com/pingcap/tidb/issues/48082) @[wshwsh12](https://github.com/wshwsh12)
    - (dup): release-7.4.0.md > 错误修复> TiDB - 修复 `AUTO_ID_CACHE=1` 时可能导致 `Duplicate entry` 的问题 [#46444](https://github.com/pingcap/tidb/issues/46444) @[tiancaiamao](https://github.com/tiancaiamao)
    - (dup): release-7.4.0.md > 错误修复> TiDB - 修复当 JOIN 两个子查询时执行 `TIDB_INLJ` Hint 不生效的问题 [#46160](https://github.com/pingcap/tidb/issues/46160) @[qw4990](https://github.com/qw4990)
    - (dup): release-7.1.2.md > 错误修复> TiDB - 修复 TiDB 重启后 DDL 操作可能卡住的问题 [#46751](https://github.com/pingcap/tidb/issues/46751) @[wjhuang2016](https://github.com/wjhuang2016)
    - (dup): release-7.1.2.md > 错误修复> TiDB - 修复由于 MDL 处理不正确可能导致 DDL 永久阻塞的问题 [#46920](https://github.com/pingcap/tidb/issues/46920) @[wjhuang2016](https://github.com/wjhuang2016)
    - (dup): release-7.4.0.md > 错误修复> TiDB - 修复 `MERGE_JOIN` 的结果错误的问题 [#46580](https://github.com/pingcap/tidb/issues/46580) @[qw4990](https://github.com/qw4990)
    - (dup): release-7.1.2.md > 错误修复> TiDB - 修复 Sort 算子在落盘过程中可能导致 TiDB 崩溃的问题 [#47538](https://github.com/pingcap/tidb/issues/47538) @[windtalker](https://github.com/windtalker)
    - (dup): release-7.4.0.md > 错误修复> TiDB - 修复 `cast(col)=range` 条件在 CAST 无精度损失的情况下会导致 FullScan 的问题 [#45199](https://github.com/pingcap/tidb/issues/45199) @[AilinKid](https://github.com/AilinKid)
    - (dup): release-7.1.2.md > 错误修复> TiDB - 修复 `RENAME TABLE` 操作导致表中出现重复列的问题 [#47064](https://github.com/pingcap/tidb/issues/47064) @[jiyfhust](https://github.com/jiyfhust)
    - (dup): release-7.1.2.md > 错误修复> TiDB - 修复 `client-go` 中 `batch-client` panic 的问题 [#47691](https://github.com/pingcap/tidb/issues/47691) @[crazycs520](https://github.com/crazycs520)
    - (dup): release-7.1.2.md > 错误修复> TiDB - 禁止非整型聚簇索引进行 split table 操作 [#47350](https://github.com/pingcap/tidb/issues/47350) @[tangenta](https://github.com/tangenta)
    - (dup): release-7.1.0.md > 错误修复> TiDB - 修复时间转换时 Prepared Plan Cache 与 Non-Prepared Plan Cache 的行为不兼容性的问题 [#42439](https://github.com/pingcap/tidb/issues/42439) @[qw4990](https://github.com/qw4990)
    - (dup): release-6.6.0.md > 错误修复> TiDB - 修复了部分情况下空表无法使用 ingest 模式添加索引的问题 [#39641](https://github.com/pingcap/tidb/issues/39641) @[tangenta](https://github.com/tangenta)
    - (dup): release-7.4.0.md > 错误修复> TiDB - 修复交换分区时，无法检测出不符合分区定义的数据的问题 [#46492](https://github.com/pingcap/tidb/issues/46492) @[mjonss](https://github.com/mjonss)
    - (dup): release-7.4.0.md > 错误修复> TiDB - 修复 `group_concat` 无法解析 `ORDER BY` 列的问题 [#41986](https://github.com/pingcap/tidb/issues/41986) @[AilinKid](https://github.com/AilinKid)
    - (dup): release-7.4.0.md > 错误修复> TiDB - 修复深嵌套的表达式的 HashCode 重复计算导致的高内存占用和 OOM 问题 [#42788](https://github.com/pingcap/tidb/issues/42788) @[AilinKid](https://github.com/AilinKid)
    - (dup): release-7.4.0.md > 错误修复> TiDB - 修复 MPP 执行计划中通过 Union 下推 Aggregation 导致的结果错误 [#45850](https://github.com/pingcap/tidb/issues/45850) @[AilinKid](https://github.com/AilinKid)
    - (dup): release-7.5.0.md > 错误修复> TiDB - 修复 `INDEX_LOOKUP_HASH_JOIN` 内存使用量估算错误的问题 [#47788](https://github.com/pingcap/tidb/issues/47788) @[SeaRise](https://github.com/SeaRise)
    - 修复 `plan replayer` 生成的 zip 包无法被导入回 TiDB 的问题 [#46474](https://github.com/pingcap/tidb/issues/46474) @[YangKeao](https://github.com/YangKeao)
    - 修复当 `LIMIT N` 中的 N 过大时产生的错误代价估算 [#43285](https://github.com/pingcap/tidb/issues/43285) @[qw4990](https://github.com/qw4990)
    - 修复构造统计信息的 TopN 结构时可能的 panic 问题 [#35948](https://github.com/pingcap/tidb/issues/35948) @[hi-rustin](https://github.com/hi-rustin)
    - 修复 MPP 计算 COUNT(INT) 时结果可能出错的问题 [#48643](https://github.com/pingcap/tidb/issues/48643) @[AilinKid](https://github.com/AilinKid)
    - 修复 `tidb_enable_ordered_result_mode` 开启时可能 panic 的问题 [#45044](https://github.com/pingcap/tidb/issues/45044) @[qw4990](https://github.com/qw4990)
    - (dup): release-7.5.0.md > 错误修复> TiDB - 修复优化器为减少窗口函数引入的 sort 而错误地选择了 `IndexFullScan` 的问题 [#46177](https://github.com/pingcap/tidb/issues/46177) @[qw4990](https://github.com/qw4990)
    - 修复谓词下推入公共表达式时结果可能出错的问题 [#47881](https://github.com/pingcap/tidb/issues/47881) @[winoros](https://github.com/winoros)
    - 修复 UNION ALL 第一个子节点是 Table Dual 时，执行可能报错的问题 [#48755](https://github.com/pingcap/tidb/issues/48755) @[winoros](https://github.com/winoros)
    - 修复列裁剪特定情况下会 panic 的问题 [#47331](https://github.com/pingcap/tidb/issues/47331) @[hi-rustin](https://github.com/hi-rustin)
    - 修复当包含聚合或者窗口函数的公共表达式被其他递归公共表达式引用时，可能抛出语法错误的问题 [#47603](https://github.com/pingcap/tidb/issues/47603) [#47711](https://github.com/pingcap/tidb/issues/47711)  @[elsa0520](https://github.com/elsa0520)
    - 修复在 prepare 语句中使用 QB_NAME hint 时可能执行异常的问题 [#46817](https://github.com/pingcap/tidb/issues/46817) @[jackysp](https://github.com/jackysp)
    - 修复使用 `AUTO_ID_CACHE=1` 时 goroutine 泄漏的问题 [#46324](https://github.com/pingcap/tidb/issues/46324) @[tiancaiamao](https://github.com/tiancaiamao)
    - 修复 TiDB 在关闭时可能 panic 的问题 [#32110](https://github.com/pingcap/tidb/issues/32110) @[july2993](https://github.com/july2993)
    - 修复 TiDB schema cache 中读取 schema diff commit 版本使用 mvcc 接口没有处理 lock 的问题 [#48281](https://github.com/pingcap/tidb/issues/48281) @[cfzjywxk](https://github.com/cfzjywxk)
    - 修复表改名重复错误[#47141](https://github.com/pingcap/tidb/pull/47141)@[jiyfhust](https://github.com/jiyfhust)
    - 修复 load data replace 问题[#47995](https://github.com/pingcap/tidb/issues/47995)) @[lance6716](https://github.com/lance6716)
    - 修复 pd leader 故障 1分钟导致 import into 任务失败 [#48307](https://github.com/pingcap/tidb/issues/48307) @[D3Hunter](https://github.com/D3Hunter)
    - 修复创建日期型字段索引问题 [#47426]([https://github.com/pingcap/tidb/issues/47426]) @[tangenta](https://github.com/tangenta)
    - 修复 tablesample 未排序问题 [#48253](https://github.com/pingcap/tidb/issues/48253) @[tangenta](https://github.com/tangenta)
    - 修复当 DDL jobID 恢复为 0 导致 TiDB 节点 panic [#46296](https://github.com/pingcap/tidb/issues/46296) @[jiyfhust](https://github.com/jiyfhust)

+ TiKV **tw@Oreoxmt --14 条**

    - (dup): release-7.1.2.md > 错误修复> TiKV - 修复在移动 Peer 时可能导致 Follower Read 性能变差的问题 [#15468](https://github.com/tikv/tikv/issues/15468) @[YuJuncen](https://github.com/YuJuncen)
    - (dup): release-7.4.0.md > 错误修复> TiKV - 修复 raftstore-applys 不断增长的数据错误 [#15371](https://github.com/tikv/tikv/issues/15371) @[Connor1996](https://github.com/Connor1996)
    - (dup): release-7.1.2.md > 错误修复> TiKV - 修复有线上负载时，TiDB Lightning 的 Checksum Coprocessor 请求超时的问题 [#15565](https://github.com/tikv/tikv/issues/15565) @[lance6716](https://github.com/lance6716)
    - 升级 `lz4-sys` 版本到 1.9.4 以修复安全问题 [#15621](https://github.com/tikv/tikv/issues/15621) @[SpadeA-Tang](https://github.com/SpadeA-Tang)
    - 升级 `tokio` 版本到 6.5 以修复安全问题 [#15621](https://github.com/tikv/tikv/issues/15621) @[LykxSassinator](https://github.com/LykxSassinator)
    - 移除 `flatbuffer`，因为其存在安全问题 [#15621](https://github.com/tikv/tikv/issues/15621) @[tonyxuqqi](https://github.com/tonyxuqqi)
    - resolved-ts: 在存储分网络隔离时加快推进速度 [#15679](https://github.com/tikv/tikv/issues/15679) @[hicqu](https://github.com/hicqu)
    - 修复当 TiKV 存在很多未 apply 的 Raft 日志时重启 TiKV 出现的内存溢出问题。[#15770](https://github.com/tikv/tikv/issues/15770) @[overvenus](https://github.com/overvenus)
    - 修复 Region 合并后，历史 peer 残留并阻塞 resolved ts 的问题 [#15919](https://github.com/tikv/tikv/issues/15919) @[overvenus](https://github.com/overvenus)
    - 修复云环境中 Grafana中scheduler命令变量错误的问题 [#15832](https://github.com/tikv/tikv/issues/15832) @[Connor1996](https://github.com/Connor1996)
    - 修复 titan `blob-run-mode` 无法在线更新的问题 [#15978](https://github.com/tikv/tikv/issues/15978) @[tonyxuqqi](https://github.com/tonyxuqqi)
    - 修复 Regon 元信息不一致导致的 TiKV panic 问题。[#13311](https://github.com/tikv/tikv/issues/13311)@[cfzjywxk](https://github.com/cfzjywxk)
    - 修复 online recovery 在 Leader 强制退出时的 panic 问题 [#15629](https://github.com/tikv/tikv/issues/15629)@[Connor1996](https://github.com/Connor1996)
    - 修复在进行扩容时可能导致 dr auto sync 的 joint state 超时问题 [#15817](https://github.com/tikv/tikv/issues/15817) @[Connor1996](https://github.com/Connor1996)
    - 修复 TiKV coprocessor 在移除 Raft peer 时可能返回陈旧数据的问题 [#16069](https://github.com/tikv/tikv/issues/16069) @[overvenus](https://github.com/overvenus)
    - 修复 resolved ts 可能被阻塞 2 小时的问题。[#39130](https://github.com/pingcap/tidb/issues/39130) @[overvenus](https://github.com/overvenus)
    - 修复在 Flashback 时遇到 `notLeader` 或 `regionNotFound` 导致 Flashback 卡住的问题。[#15712](https://github.com/tikv/tikv/issues/15712)@[HuSharp](https://github.com/HuSharp)

+ PD **tw@Oreoxmt --4 条**

    - (dup): release-7.1.2.md > 错误修复> PD - 修复 Plugin 目录、文件内容可能存在安全隐患的问题 [#7094](https://github.com/tikv/pd/issues/7094) @[HuSharp](https://github.com/HuSharp)
    - (dup): release-7.4.0.md > 错误修复> PD - 修复修改隔离等级时未同步到默认放置规则中的问题 [#7121](https://github.com/tikv/pd/issues/7121) @[rleungx](https://github.com/rleungx)
    - (dup): release-7.1.2.md > 错误修复> PD - 修复 `evict-leader-scheduler` 丢失配置的问题 [#6897](https://github.com/tikv/pd/issues/6897) @[HuSharp](https://github.com/HuSharp)
    - 修复空 region 统计口径可能导致 BR Restore Regions 不均衡的问题 [#7148](https://github.com/tikv/pd/issues/7148) @[Cabinfever](https://github.com/CabinfeverB)
    - (dup): release-7.5.0.md > 错误修复> PD - 修复采用自适应同步部署模式 (DR Auto-Sync) 的集群在 Placement Rule 的配置较复杂时，`canSync` 和 `hasMajority` 可能计算错误的问题 [#7201](https://github.com/tikv/pd/issues/7201) @[disksing](https://github.com/disksing)
    - (dup): release-7.5.0.md > 错误修复> PD - 修复采用自适应同步部署模式 (DR Auto-Sync) 的集群 `available_stores` 计算错误的问题 [#7221](https://github.com/tikv/pd/issues/7221) @[disksing](https://github.com/disksing)
    - 修复 DR Auto-Sync 集群在备机房挂掉时主机房不能添加 TiKV 节点的问题 [#7218](https://github.com/tikv/pd/issues/7218) @[disksing](https://github.com/disksing)
    - (dup): release-7.5.0.md > 错误修复> PD - 修复在大集群中添加多个 TiKV 节点可能导致 TiKV 心跳上报变慢或卡住的问题 [#7248](https://github.com/tikv/pd/issues/7248) @[rleungx](https://github.com/rleungx)
    - (dup): release-7.5.0.md > 错误修复> PD - 修复当 TiKV 节点不可用时 PD 可能删除正常 Peers 的问题 [#7249](https://github.com/tikv/pd/issues/7249) @[lhy1024](https://github.com/lhy1024)
    - 修复 DR Auto-Sync Ledaer 切换时间过长的问题 [#6988](https://github.com/tikv/pd/issues/6988) @[HuSharp](https://github.com/HuSharp)
    - 升级 Gin 版本从 v1.8.1 到 v1.9.1 以解决部分安全问题 [#7438](https://github.com/tikv/pd/issues/7438) @[niubell](https://github.com/niubell)

+ TiFlash **tw@hfxsd --2 条**

    - 修复 Grafana 的 Read snapshot 面板上无法正确显示当前运行的最长查询时长的问题 [#7713](https://github.com/pingcap/tiflash/issues/7713) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复执行 `ALTER TABLE ... EXCHANGE PARTITION ...` 语句后 panic 的问题 [#8372](https://github.com/pingcap/tiflash/issues/8372) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - (dup): release-7.1.2.md > 错误修复> TiFlash - 修复 MemoryTracker 提供的内存使用数据不准确的问题 [#8128](https://github.com/pingcap/tiflash/issues/8128) @[JinheLin](https://github.com/JinheLin)

+ Tools

    + Backup & Restore (BR) **tw@hfxsd --5 条**

        - (dup): release-7.5.0.md > 错误修复> Tools> Backup & Restore (BR) - 修复大宽表场景下，日志备份在某些场景中可能卡住的问题 [#15714](https://github.com/tikv/tikv/issues/15714) @[YuJuncen](https://github.com/YuJuncen)
        - 修复频繁 flush 导致 log backup 卡死的问题 [#15602](https://github.com/tikv/tikv/issues/15602) @[3pointer](https://github.com/3pointer)
        - 修复在 aws 云上, 连接 ec2metadata 连接被重置后, 重试导致备份恢复性能下降的问题 [#46750](https://github.com/pingcap/tidb/issues/47650) @[Leavrth](https://github.com/Leavrth)
        - (dup): release-7.1.2.md > 错误修复> Tools> Backup & Restore (BR) - 修复 1 分钟之内多次执行 PITR 可能导致数据丢失的问题 [#15483](https://github.com/tikv/tikv/issues/15483) @[YuJuncen](https://github.com/YuJuncen)
        - 让 BR SQL 命令使用和 CLP 同样的默认参数 [#48000](https://github.com/pingcap/tidb/issues/48000) @[YuJuncen](https://github.com/YuJuncen)
        - 修复 pd owner 发生转移情况下, log backup 可能 panic 的问题 [#47533](https://github.com/pingcap/tidb/issues/47533) @[YuJuncen](https://github.com/YuJuncen)
        - 修复一个是用本地存储文件目录命名的问题 [#48452](https://github.com/pingcap/tidb/issues/48452) @[3AceShowHand](https://github.com/3AceShowHand)

    + TiCDC **tw@hfxsd --12 条**

        - 修复上游在执行有损 DDL 场景下，CDC server 可能发生 panic 的问题 [#9739](https://github.com/pingcap/tiflow/issues/9739) @[hicqu](https://github.com/hicqu)
        - 修复在开启 Redo log 功能， 执行 resume 命令场景下同步任务出现报错的问题 [#9769](https://github.com/pingcap/tiflow/issues/9769) @[hicqu](https://github.com/hicqu)
        - 修复 tikv 节点 crash 时，同步延迟上升的问题 [#9741](https://github.com/pingcap/tiflow/issues/9741)
        - 修复 cdc server 在某些特殊操作系统下设置 gcTuner 不合理的问题 [#9762](https://github.com/pingcap/tiflow/issues/9762) @[sdojjy](https://github.com/sdojjy)
        - 修复同步到 TiDB/mysql 某些场景下，SQL 语句 where 没有采用 PK 作为条件的问题 [#9988](https://github.com/pingcap/tiflow/issues/9988)
        - 修复某些特殊场景下同步任务在 CDC 节点分配不均衡的问题 [#9839](https://github.com/pingcap/tiflow/issues/9839) @[3AceShowHand](https://github.com/3AceShowHand)
        - 修复 Redo log 在 NFS 出现问题可能导致 CDC server 卡住的问题 [#9986](https://github.com/pingcap/tiflow/issues/9986)
        - 优化 CDC 在做增量扫对上游 tikv 的影响问题 [#11390](https://github.com/tikv/tikv/issues/11390)
        - 修复 Redo log 开启的场景下，DDL 同步时间间隔过长的问题 [#9960](https://github.com/pingcap/tiflow/issues/9960)
        - 修复开启 BDR 时，drop/create 同一张表 DML 事件不能正确同步的问题 [#10079](https://github.com/pingcap/tiflow/issues/10079)
        - 修复同步到对象存储时，NFS 文件过多时同步延迟上升的问题 [#10041](https://github.com/pingcap/tiflow/issues/10041) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - 增加同步到对象存储时，某些特殊场景下导致 server Panic 的问题 [#10137](https://github.com/pingcap/tiflow/issues/10137) @[sdojjy](https://github.com/sdojjy)
        - (dup): release-7.4.0.md > 错误修复> Tools> TiCDC - 修复 PD 做扩缩容场景下 TiCDC 访问无效旧地址的问题 [#9584](https://github.com/pingcap/tiflow/issues/9584) @[fubinzh](https://github.com/fubinzh) @[asddongmen](https://github.com/asddongmen)
        - (dup): release-7.1.2.md > 错误修复> Tools> TiCDC - 修复在某些特殊的操作系统下，获取错误内存信息可能导致 OOM 的问题 [#9762](https://github.com/pingcap/tiflow/issues/9762) @[sdojjy](https://github.com/sdojjy)

    + TiDB Data Migration (DM)

        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - (dup): release-7.4.0.md > 错误修复> Tools> TiDB Data Migration (DM) - 修复 DM 在乐观模式中跳过 Partition DDL 的问题 [#9788](https://github.com/pingcap/tiflow/issues/9788) @[GMHDBJD](https://github.com/GMHDBJD)
        - (dup): release-7.4.0.md > 错误修复> Tools> TiDB Data Migration (DM) - 修复 DM 在跳过 Online DDL 时无法正确追踪上游表结构的问题 [#9587](https://github.com/pingcap/tiflow/issues/9587) @[GMHDBJD](https://github.com/GMHDBJD)
        - (dup): release-7.4.0.md > 错误修复> Tools> TiDB Data Migration (DM) - 修复 DM 在跳过失败 DDL 并且后续无 DDL 执行时显示延迟持续增长的问题 [#9605](https://github.com/pingcap/tiflow/issues/9605) @[D3Hunter](https://github.com/D3Hunter)
        - (dup): release-7.4.0.md > 错误修复> Tools> TiDB Data Migration (DM) - 修复 DM 在乐观模式恢复任务时跳过所有 DML 的问题 [#9588](https://github.com/pingcap/tiflow/issues/9588) @[GMHDBJD](https://github.com/GMHDBJD)

    + TiDB Lightning

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + Dumpling

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + TiUP

        - note [#issue](https://github.com/pingcap/tiup/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiup/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + TiDB Binlog

        - (dup): release-7.1.2.md > 错误修复> Tools> TiDB Binlog - 修复传输事务超过 1 GB 时 Drainer 会退出的问题 [#28659](https://github.com/pingcap/tidb/issues/28659) @[jackysp](https://github.com/jackysp)