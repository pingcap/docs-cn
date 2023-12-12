---
title: TiDB 7.1.3 Release Notes
summary: 了解 TiDB 7.1.3 版本的兼容性变更、改进提升，以及错误修复。
---

# TiDB 7.1.3 Release Notes

发版日期：2023 年 x 月 x 日

TiDB 版本：7.1.3

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v7.1/quick-start-with-tidb) | [生产部署](https://docs.pingcap.com/zh/tidb/v7.1/production-deployment-using-tiup) | [下载离线包](https://cn.pingcap.com/product-community/?version=v7.1.3#version-list)

## 兼容性变更

- note [#issue](https://github.com/pingcap/${repo-name}/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
- (dup): release-6.5.6.md > 兼容性变更 - 在安全增强模式 (SEM) 下禁止设置 [`require_secure_transport`](https://docs.pingcap.com/zh/tidb/v6.5/system-variables#require_secure_transport-从-v610-版本开始引入) 为 `ON`，避免用户无法连接的问题 [#47665](https://github.com/pingcap/tidb/issues/47665) @[tiancaiamao](https://github.com/tiancaiamao)
- (dup): release-6.5.6.md > 兼容性变更 - 经进一步的测试后，TiCDC Changefeed 配置项 [`case-sensitive`](/ticdc/ticdc-changefeed-config.md) 默认值由 `true` 改为 `false`，即默认情况下 TiCDC 配置文件中涉及的表名、库名大小写不敏感 [#10047](https://github.com/pingcap/tiflow/issues/10047) @[sdojjy](https://github.com/sdojjy)
- (dup): release-6.5.6.md > 兼容性变更> TiCDC Changefeed 新增以下配置项： - [`compression`](/ticdc/ticdc-changefeed-config.md)：你可以设置 redo log 文件的压缩行为 [#10176](https://github.com/pingcap/tiflow/issues/10176) @[sdojjy](https://github.com/sdojjy)
- (dup): release-6.5.6.md > 兼容性变更> TiCDC Changefeed 新增以下配置项： - [`encoding-worker-num`](/ticdc/ticdc-changefeed-config.md) 和 [`flush-worker-num`](/ticdc/ticdc-changefeed-config.md)：你可以根据不同的机器规格，设置 redo 模块不同的并发参数 [#10048](https://github.com/pingcap/tiflow/issues/10048) @[CharlesCheung96](https://github.com/CharlesCheung96)
- (dup): release-6.5.6.md > 兼容性变更> TiCDC Changefeed 新增以下配置项： - [`sink.cloud-storage-config`](/ticdc/ticdc-changefeed-config.md)：你可以设置同步数据到对象存储时自动清理历史数据的功能 [#10109](https://github.com/pingcap/tiflow/issues/10109) @[CharlesCheung96](https://github.com/CharlesCheung96)

## 改进提升

+ TiDB

    - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

+ TiKV

    - note [#issue](https://github.com/tikv/tikv/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/tikv/tikv/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - (dup): release-7.3.0.md > 改进提升> TiKV - 添加 `Max gap of safe-ts` 和 `Min safe ts region` 监控项以及 `tikv-ctl get-region-read-progress` 命令，用于更好地观测和诊断 resolved-ts 和 safe-ts 的状态 [#15082](https://github.com/tikv/tikv/issues/15082) @[ekexium](https://github.com/ekexium)

+ PD

    - note [#issue](https://github.com/tikv/pd/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/tikv/pd/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - (dup): release-7.4.0.md > 改进提升> PD - 改进 resource control client 的配置获取方式，使其可以动态获取最新配置 [#7043](https://github.com/tikv/pd/issues/7043) @[nolouch](https://github.com/nolouch)

+ TiFlash

    - note [#issue](https://github.com/pingcap/tiflash/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/pingcap/tiflash/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

+ Tools

    + Backup & Restore (BR)

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - (dup): release-6.5.6.md > 改进提升> Tools> Backup & Restore (BR) - 当遇到 Region 打散超时失败或被取消的情况时，快照恢复支持自动重试 Region 打散 [#47236](https://github.com/pingcap/tidb/issues/47236) @[Leavrth](https://github.com/Leavrth)
        - (dup): release-7.5.0.md > 改进提升> Tools> Backup & Restore (BR) - 快照备份恢复在遇到某些网络错误时会进行重试 [#48528](https://github.com/pingcap/tidb/issues/48528) @[Leavrth](https://github.com/Leavrth)
        - (dup): release-6.5.6.md > 改进提升> Tools> Backup & Restore (BR) - 新增支持 [`FLASHBACK CLUSTER TO TSO`](https://docs.pingcap.com/zh/tidb/v6.5/sql-statement-flashback-cluster) 语法 [#48372](https://github.com/pingcap/tidb/issues/48372) @[BornChanger](https://github.com/BornChanger)
        - (dup): release-6.5.6.md > 改进提升> Tools> Backup & Restore (BR) - 新增 PITR 对 delete range 场景的集成测试，提升 PITR 稳定性 [#47738](https://github.com/pingcap/tidb/issues/47738) @[Leavrth](https://github.com/Leavrth)
- Fixed a bug that may cause log backup started but not work properly if there are connective issue to PD during initializing the task. [#16056](https://github.com/tikv/tikv/issues/16056) @[YuJuncen](https://github.com/YuJuncen)

    + TiCDC

        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - (dup): release-6.5.6.md > 改进提升> Tools> TiCDC - 减少 TiCDC 在做增量扫描时对上游 TiKV 的影响 [#11390](https://github.com/tikv/tikv/issues/11390) @[hicqu](https://github.com/hicqu)
        - (dup): release-6.5.6.md > 改进提升> Tools> TiCDC - 支持通过在 `sink-uri` 中设置 `content-compatible=true` 使 TiCDC Canal-JSON [兼容 Canal 官方输出的内容格式](/ticdc/ticdc-canal-json.md#兼容-canal-官方实现) [#10106](https://github.com/pingcap/tiflow/issues/10106) @[3AceShowHand](https://github.com/3AceShowHand)

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

+ TiDB

    - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - (dup): release-6.5.6.md > 错误修复> TiDB - 修复 `UNION ALL` 第一个子节点是 DUAL Table 时，执行可能报错的问题 [#48755](https://github.com/pingcap/tidb/issues/48755) @[winoros](https://github.com/winoros)
    - (dup): release-6.5.6.md > 错误修复> TiDB - 修复当 DDL `jobID` 恢复为 0 时 TiDB 节点 panic 的问题 [#46296](https://github.com/pingcap/tidb/issues/46296) @[jiyfhust](https://github.com/jiyfhust)
    - (dup): release-6.5.6.md > 错误修复> TiDB - 修复 `TABLESAMPLE` 返回的行数据未排序的问题 [#48253](https://github.com/pingcap/tidb/issues/48253) @[tangenta](https://github.com/tangenta)
    - (dup): release-6.5.6.md > 错误修复> TiDB - 修复 `tidb_enable_ordered_result_mode` 开启时可能发生 panic 的问题 [#45044](https://github.com/pingcap/tidb/issues/45044) @[qw4990](https://github.com/qw4990)
    - (dup): release-7.5.0.md > 错误修复> TiDB - 修复优化器为减少窗口函数引入的 sort 而错误地选择了 `IndexFullScan` 的问题 [#46177](https://github.com/pingcap/tidb/issues/46177) @[qw4990](https://github.com/qw4990)
    - (dup): release-6.5.6.md > 错误修复> TiDB - 修复 TiDB schema cache 中读取 schema diff commit 版本时，未处理 MVCC 接口中的 lock 的问题 [#48281](https://github.com/pingcap/tidb/issues/48281) @[cfzjywxk](https://github.com/cfzjywxk)
    - (dup): release-7.5.0.md > 错误修复> TiDB - 修复 `INDEX_LOOKUP_HASH_JOIN` 内存使用量估算错误的问题 [#47788](https://github.com/pingcap/tidb/issues/47788) @[SeaRise](https://github.com/SeaRise)
    - (dup): release-6.5.6.md > 错误修复> TiDB - 修复 PD leader 故障 1 分钟导致 `IMPORT INTO` 任务失败的问题 [#48307](https://github.com/pingcap/tidb/issues/48307) @[D3Hunter](https://github.com/D3Hunter)
    - (dup): release-7.5.0.md > 错误修复> TiDB - 修复 `client-go` 中 `batch-client` panic 的问题 [#47691](https://github.com/pingcap/tidb/issues/47691) @[crazycs520](https://github.com/crazycs520)
    - (dup): release-6.5.6.md > 错误修复> TiDB - 修复列裁剪在特定情况下会导致 panic 的问题 [#47331](https://github.com/pingcap/tidb/issues/47331) @[hi-rustin](https://github.com/hi-rustin)
    - (dup): release-7.5.0.md > 错误修复> TiDB - 修复 TiDB 在通过 `systemd` 启动时无法读取 `cgroup` 资源限制的问题 [#47442](https://github.com/pingcap/tidb/issues/47442) @[hawkingrei](https://github.com/hawkingrei)
    - (dup): release-6.5.6.md > 错误修复> TiDB - 修复当包含聚合或者窗口函数的公共表达式被其他递归公共表达式引用时，可能抛出语法错误的问题 [#47603](https://github.com/pingcap/tidb/issues/47603) [#47711](https://github.com/pingcap/tidb/issues/47711)  @[elsa0520](https://github.com/elsa0520)
    - (dup): release-6.5.6.md > 错误修复> TiDB - 修复构造统计信息的 TopN 结构时可能发生的 panic 问题 [#35948](https://github.com/pingcap/tidb/issues/35948) @[hi-rustin](https://github.com/hi-rustin)
    - (dup): release-6.5.6.md > 错误修复> TiDB - 修复 MPP 计算 `COUNT(INT)` 时结果可能出错的问题 [#48643](https://github.com/pingcap/tidb/issues/48643) @[AilinKid](https://github.com/AilinKid)
    - (dup): release-7.5.0.md > 错误修复> TiDB - 修复 HashJoin 算子 Probe 时无法复用 chunk 的问题 [#48082](https://github.com/pingcap/tidb/issues/48082) @[wshwsh12](https://github.com/wshwsh12)

+ TiKV

    - note [#issue](https://github.com/tikv/tikv/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/tikv/tikv/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - (dup): release-6.5.6.md > 错误修复> TiKV - 修复 resolved-ts 可能被阻塞 2 小时的问题 [#39130](https://github.com/pingcap/tidb/issues/39130) @[overvenus](https://github.com/overvenus)
    - (dup): release-6.5.6.md > 错误修复> TiKV - 修复扩容时可能导致 DR Auto-Sync 的 joint state 超时问题 [#15817](https://github.com/tikv/tikv/issues/15817) @[Connor1996](https://github.com/Connor1996)
    - (dup): release-6.5.6.md > 错误修复> TiKV - 修复云环境中 Grafana 中 scheduler 命令变量错误的问题 [#15832](https://github.com/tikv/tikv/issues/15832) @[Connor1996](https://github.com/Connor1996)
    - (dup): release-6.5.6.md > 错误修复> TiKV - 修复 Region 合并后，历史 peer 残留并阻塞 resolved-ts 的问题 [#15919](https://github.com/tikv/tikv/issues/15919) @[overvenus](https://github.com/overvenus)
    - (dup): release-6.5.5.md > 错误修复> TiKV - 修复 Online Unsafe Recovery 时无法处理 merge abort 的问题 [#15580](https://github.com/tikv/tikv/issues/15580) @[v01dstar](https://github.com/v01dstar)
    - (dup): release-6.5.6.md > 错误修复> TiKV - 修复重启 TiKV 时，由于存在大量未 apply 的 Raft 日志导致的内存溢出问题 [#15770](https://github.com/tikv/tikv/issues/15770) @[overvenus](https://github.com/overvenus)
    - (dup): release-6.5.6.md > 错误修复> TiKV - 升级 `lz4-sys` 版本到 1.9.4 以修复安全问题 [#15621](https://github.com/tikv/tikv/issues/15621) @[SpadeA-Tang](https://github.com/SpadeA-Tang)
    - (dup): release-6.5.6.md > 错误修复> TiKV - 修复 Titan `blob-run-mode` 无法在线更新的问题 [#15978](https://github.com/tikv/tikv/issues/15978) @[tonyxuqqi](https://github.com/tonyxuqqi)
    - (dup): release-6.5.4.md > 错误修复> TiKV - 修复 PD 和 TiKV 之间的网络中断可能导致 PITR 卡住的问题 [#15279](https://github.com/tikv/tikv/issues/15279) @[YuJuncen](https://github.com/YuJuncen)
    - (dup): release-6.5.6.md > 错误修复> TiKV - 修复 TiKV coprocessor 在移除 Raft peer 时可能返回陈旧数据的问题 [#16069](https://github.com/tikv/tikv/issues/16069) @[overvenus](https://github.com/overvenus)

+ PD

    - note [#issue](https://github.com/tikv/pd/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/tikv/pd/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - (dup): release-7.5.0.md > 错误修复> PD - 修复在大集群中添加多个 TiKV 节点可能导致 TiKV 心跳上报变慢或卡住的问题 [#7248](https://github.com/tikv/pd/issues/7248) @[rleungx](https://github.com/rleungx)
    - (dup): release-7.5.0.md > 错误修复> PD - 修复 TiDB Dashboard 不能正常读取 PD `trace` 数据的问题 [#7253](https://github.com/tikv/pd/issues/7253) @[nolouch](https://github.com/nolouch)
    - (dup): release-6.5.6.md > 错误修复> PD - 将 Gin Web Framework 的版本从 v1.8.1 升级到 v1.9.1 以修复部分安全问题 [#7438](https://github.com/tikv/pd/issues/7438) @[niubell](https://github.com/niubell)
    - (dup): release-7.5.0.md > 错误修复> PD - 修复 rule checker 未按照设定的 Placement Rule 添加 Learner 的问题 [#7185](https://github.com/tikv/pd/issues/7185) @[nolouch](https://github.com/nolouch)
    - (dup): release-7.5.0.md > 错误修复> PD - 修复当 TiKV 节点不可用时 PD 可能删除正常 Peers 的问题 [#7249](https://github.com/tikv/pd/issues/7249) @[lhy1024](https://github.com/lhy1024)
    - (dup): release-6.5.6.md > 错误修复> PD - 修复自适应同步部署模式 (DR Auto-Sync) 下 leader 切换时间过长的问题 [#6988](https://github.com/tikv/pd/issues/6988) @[HuSharp](https://github.com/HuSharp)

+ TiFlash

    - note [#issue](https://github.com/pingcap/tiflash/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/pingcap/tiflash/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - (dup): release-6.5.6.md > 错误修复> TiFlash - 修复执行 `ALTER TABLE ... EXCHANGE PARTITION ...` 语句后 panic 的问题 [#8372](https://github.com/pingcap/tiflash/issues/8372) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复当查询遇到 memory limit 限制后发生内存泄漏的问题 [#8447](https://github.com/pingcap/tiflash/issues/8447) @[JinheLin](https://github.com/JinheLin)
    - 修复在执行 `FLASHBACK DATABASE` 后 TiFlash 副本的数据仍会被 GC 回收的问题 [#8450](https://github.com/pingcap/tiflash/issues/8450) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复 Grafana 中部分面板的最大分位数耗时显示不正确的问题 [#8076](https://github.com/pingcap/tiflash/issues/8076) @[JaySon-Huang](https://github.com/JaySon-Huang)

+ Tools

    + Backup & Restore (BR)

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - (dup): release-6.5.6.md > 错误修复> Tools> Backup & Restore (BR) - 修复由于 BR SQL 命令和 CLI 的默认参数不同可能导致的 OOM 问题 [#48000](https://github.com/pingcap/tidb/issues/48000) @[YuJuncen](https://github.com/YuJuncen)
        - (dup): release-7.5.0.md > 错误修复> Tools> Backup & Restore (BR) - 修复大宽表场景下，日志备份在某些场景中可能卡住的问题 [#15714](https://github.com/tikv/tikv/issues/15714) @[YuJuncen](https://github.com/YuJuncen)
        - (dup): release-6.5.6.md > 错误修复> Tools> Backup & Restore (BR) - 修复生成外部存储文件 URI 错误的问题 [#48452](https://github.com/pingcap/tidb/issues/48452) @[3AceShowHand](https://github.com/3AceShowHand)
        - (dup): release-6.5.6.md > 错误修复> Tools> Backup & Restore (BR) - 修复在 EC2 metadata 连接被重置后，重试导致备份恢复性能下降的问题 [#46750](https://github.com/pingcap/tidb/issues/47650) @[Leavrth](https://github.com/Leavrth)

    + TiCDC

        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - (dup): release-6.5.6.md > 错误修复> Tools> TiCDC - 修复开启双向复制时，`DROP` 一张表后再重新 `CREATE` 该表，Changefeed 无法同步 DML 事件的问题 [#10079](https://github.com/pingcap/tiflow/issues/10079) @[asddongmen](https://github.com/asddongmen)
        - (dup): release-7.5.0.md > 错误修复> Tools> TiCDC - 修复同步数据到对象存储时访问 NFS 目录导致的性能问题 [#10041](https://github.com/pingcap/tiflow/issues/10041) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - (dup): release-6.5.6.md > 错误修复> Tools> TiCDC - 修复同步数据到对象存储时，可能会出现 TiCDC Server panic 的问题 [#10137](https://github.com/pingcap/tiflow/issues/10137) @[sdojjy](https://github.com/sdojjy)
        - (dup): release-6.5.6.md > 错误修复> Tools> TiCDC - 修复 redo log 开启时，DDL 同步时间间隔过长的问题 [#9960](https://github.com/pingcap/tiflow/issues/9960) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - (dup): release-7.5.0.md > 错误修复> Tools> TiCDC - 修复开启 Redo log 时，NFS 出现故障导致 Owner 节点卡住的问题 [#9886](https://github.com/pingcap/tiflow/issues/9886) @[3AceShowHand](https://github.com/3AceShowHand)

    + TiDB Data Migration (DM)

        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + TiDB Lightning

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - (dup): release-6.5.6.md > 错误修复> Tools> TiDB Lightning - 修复 TiDB Lightning 在 `writeToTiKV` 时卡住的问题 [#46321](https://github.com/pingcap/tidb/issues/46321) @[lance6716](https://github.com/lance6716)
        - (dup): release-6.5.6.md > 错误修复> Tools> TiDB Lightning - 修复 HTTP 重试请求未使用本次的请求内容导致导入失败的问题 [#47930](https://github.com/pingcap/tidb/issues/47930) @[lance6716](https://github.com/lance6716)
        - (dup): release-6.5.6.md > 错误修复> Tools> TiDB Lightning - 移除物理导入模式下不必要的 `get_regions` 调用 [#45507](https://github.com/pingcap/tidb/issues/45507) @[mittalrishabh](https://github.com/mittalrishabh)

    + Dumpling

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + TiUP

        - note [#issue](https://github.com/pingcap/tiup/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiup/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + TiDB Binlog

        - note [#issue](https://github.com/pingcap/tidb-binlog/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb-binlog/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
