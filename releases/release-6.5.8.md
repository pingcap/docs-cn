---
title: TiDB 6.5.8 Release Notes
summary: 了解 TiDB 6.5.8 版本的兼容性变更、改进提升，以及错误修复。
---

# TiDB 6.5.8 Release Notes

发版日期：2024 年 x 月 x 日

TiDB 版本：6.5.8

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v6.5/quick-start-with-tidb) | [生产部署](https://docs.pingcap.com/zh/tidb/v6.5/production-deployment-using-tiup) | [下载离线包](https://cn.pingcap.com/product-community/?version=v6.5.8#version-list)

## 兼容性变更

<--tw @Oreoxmt (1)-->
- 新增 TiKV 配置项 [`gc.num-threads`](https://docs.pingcap.com/zh/tidb/v6.5/tikv-configuration-file#num-threads-从-v658-版本开始引入)，用于设置当 `enable-compaction-filter` 为 `false` 时 GC 的线程个数 [#16101](https://github.com/tikv/tikv/issues/16101) @[tonyxuqqi](https://github.com/tonyxuqqi)

## 改进提升

+ TiDB

    - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

+ TiKV

    - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

+ PD

    - note [#issue](https://github.com/tikv/pd/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/tikv/pd/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

+ TiFlash

    - (dup): release-7.6.0.md > 改进提升> TiFlash - 减少后台数据 GC 任务对读、写任务延迟的影响 [#8650](https://github.com/pingcap/tiflash/issues/8650) @[JaySon-Huang](https://github.com/JaySon-Huang)

+ Tools

    + Backup & Restore (BR)

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + TiCDC
        <--tw @qiancai (1)-->
        - 支持[查询 changefeed 的下游同步状态](https://docs.pingcap.com/zh/tidb/v6.5/ticdc-open-api-v2#查询特定同步任务是否完成)，以确认 TiCDC 是否已将所接收到的上游变更完全同步到下游 [#10289](https://github.com/pingcap/tiflow/issues/10289) @[hongyunyan](https://github.com/hongyunyan)

    + TiDB Data Migration (DM)

        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + TiDB Lightning
        <--tw @hfxsd (1)-->
        - 优化导入大量表时的性能 [#50105](https://github.com/pingcap/tidb/issues/50105) @[D3Hunter](https://github.com/D3Hunter)

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

    <--tw @Oreoxmt (6)-->
    - (dup): release-7.6.0.md > 错误修复> TiDB - 修复当查询使用了会强制排序的优化器 hint（例如 `STREAM_AGG()`）且其执行计划包含 `IndexMerge` 时，强制排序可能会失效的问题 [#49605](https://github.com/pingcap/tidb/issues/49605) @[AilinKid](https://github.com/AilinKid)
    - (dup): release-7.6.0.md > 错误修复> TiDB - 修复直方图的边界包含 `NULL` 时，直方图统计信息可能无法解析成可读字符串的问题 [#49823](https://github.com/pingcap/tidb/issues/49823) @[AilinKid](https://github.com/AilinKid)
    - (dup): release-7.6.0.md > 错误修复> TiDB - 修复无法在 `REPLACE INTO` 语句中使用 hint 的问题 [#34325](https://github.com/pingcap/tidb/issues/34325) @[YangKeao](https://github.com/YangKeao)
    - (dup): release-7.6.0.md > 错误修复> TiDB - 修复由于 `STREAM_AGG()` 错误处理 CI 导致查询结果有误的问题 [#49902](https://github.com/pingcap/tidb/issues/49902) @[wshwsh12](https://github.com/wshwsh12)
    - 修复某些情况下，由于错误的分区裁剪导致查询 Range Partition 的结果不正确的问题 [#50082](https://github.com/pingcap/tidb/issues/49823) @[Defined2014](https://github.com/Defined2014)
    - 修复使用 `AUTO_ID_CACHE=1` 的自增列时，由于并发冲突导致自增 ID 分配报错的问题 [#50519](https://github.com/pingcap/tidb/issues/50519) @[tiancaiamao](https://github.com/tiancaiamao)
    - 缓解当要处理的表的数量或表的分区数量过多时，TiDB 节点 OOM 的问题 [#50077](https://github.com/pingcap/tidb/issues/50077) @[zimulala](https://github.com/zimulala)
    - 修复在分布式框架下，DDL Owner 网络隔离后执行 `ADD INDEX` 操作导致数据不一致的问题 [#49773](https://github.com/pingcap/tidb/issues/49773) @[tangenta](https://github.com/tangenta)
    - 修复包含 Apply 操作的查询在报错 `fatal error: concurrent map writes` 后导致 TiDB 崩溃的问题 [#50347](https://github.com/pingcap/tidb/issues/50347) @[SeaRise](https://github.com/SeaRise)
    - 修复通过 `COM_STMT_EXECUTE` 方式执行的 COMMIT/ROLLBACK 操作无法结束已超时事务的问题 [#49151](https://github.com/pingcap/tidb/issues/49151) @[zyguan](https://github.com/zyguan)
    <--tw @hfxsd (3)-->
    - 使用 PREPARE 方式执行 SELECT INTO OUTFILE 语句是应该报错而不是执行成功 [#49166](https://github.com/pingcap/tidb/issues/49166) @[qw4990](https://github.com/qw4990)
    - 修复特别简单的 UNIQUE 索引点查 + ORDER BY 可能执行报错的问题 [#49920](https://github.com/pingcap/tidb/issues/49920) @[jackysp](https://github.com/jackysp)
    - 修复 multi-statement 模式下，使用索引点查的 DELETE/UPDATE 语句可能会报错的问题 [#50012](https://github.com/pingcap/tidb/issues/50012) @[tangenta](https://github.com/tangenta)
    <--tw @ran-huang (3)-->
    - 修复短时间发送大量 DDL 语句时，CREATE TABLE 语句可能不会同步建立该表对心的统计信息元信息的问题 [#36004](https://github.com/pingcap/tidb/issues/36004) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes)
    - 修复 LEADING hint 在 UNION ALL 语句中无法生效的问题 [#50067](https://github.com/pingcap/tidb/issues/50067) @[hawkingrei](https://github.com/hawkingrei)
    - 修复使用旧接口导致表元信息可能不一致的问题 [#49751](https://github.com/pingcap/tidb/issues/49751) @[hawkingrei](https://github.com/hawkingrei)
    <--tw @qiancai (2)-->
    - 修复常见 hint 在 UNION ALL 语句中无法正确生效的问题 [#50068](https://github.com/pingcap/tidb/issues/50068) @[hawkingrei](https://github.com/hawkingrei)
    - 修复 6.5.7 为修复 [#49487](https://github.com/pingcap/tidb/issues/49487) 导致执行过程中遇到 ENUM/SET 类型的非法值时会直接报错的问题 [#49440](https://github.com/pingcap/tidb/issues/49440) @[winoros](https://github.com/winoros)

+ TiKV

    - (dup): release-7.6.0.md > 错误修复> TiKV - 修复 gRPC threads 在检查 `is_shutdown` 时可能出现 panic 的问题 [#16236](https://github.com/tikv/tikv/issues/16236) @[pingyu](https://github.com/pingyu)
    - (dup): release-7.6.0.md > 错误修复> TiKV - 修复巴西和埃及时区转换错误的问题 [#16220](https://github.com/tikv/tikv/issues/16220) @[overvenus](https://github.com/overvenus)
    - (dup): release-7.6.0.md > 错误修复> TiKV - 修复 TiDB 和 TiKV 处理 `DECIMAL` 算术乘法截断时结果不一致的问题 [#16268](https://github.com/tikv/tikv/issues/16268) @[solotzg](https://github.com/solotzg)

+ PD
    <--tw @hfxsd (1)-->
    - 修复 pd-ctl 查询没有 Leader 的 Region 时可能导致 PD Panic 的问题 [#7630](https://github.com/tikv/pd/issues/7630) @[rleungx](https://github.com/rleungx)

+ TiFlash
    <--tw @hfxsd (2)-->
    - (dup): release-7.6.0.md > 错误修复> TiFlash - 修复 lowerUTF8/upperUTF8 不允许大小写字符占据不同字节数的错误 [#8484](https://github.com/pingcap/tiflash/issues/8484) @[gengliqi](https://github.com/gengliqi)
    - 修复在执行 `ALTER TABLE ... MODIFY COLUMN ... NOT NULL` 将可为空的列转为不可为空之后，导致 tiflash panic 的问题 [#8419](https://github.com/pingcap/tiflash/issues/8419) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复杀查询导致 TiFlash 上大量任务被同时取消时，由于并发数据冲突导致 TiFlash 崩溃的问题 [#7432](https://github.com/pingcap/tiflash/issues/7432) @[SeaRise](https://github.com/SeaRise)

+ Tools

    + Backup & Restore (BR)
        <--tw @ran-huang (2)-->
        - (dup): release-7.6.0.md > 错误修复> Tools> Backup & Restore (BR) - 修复从旧版本的备份恢复数据时报错 `Unsupported collation` 的问题 [#49466](https://github.com/pingcap/tidb/issues/49466) @[3pointer](https://github.com/3pointer)
        - 修复了从 S3 读文件内容时出错但无法重试的问题 [#49942](https://github.com/pingcap/tidb/issues/49942) @[Leavrth](https://github.com/Leavrth)
        - 修复了在同一节点上更改 TiKV IP 地址导致日志备份卡住的问题 [#50445](https://github.com/pingcap/tidb/issues/50445) @[3pointer](https://github.com/3pointer)

    + TiCDC
        <--tw @qiancai (4)-->
        - 修复在 `ignore-event` 中设置了过滤掉 `add table partition` 事件后，TiCDC 未将相关分区的其它类型 DML 变更事件同步到下游的问题 [#10524](https://github.com/pingcap/tiflow/issues/10524) @[CharlesCheung96](https://github.com/CharlesCheung96) 
        - 修复上游表执行了 `TRUNCATE PARTITION` 后 changefeed 报错的问题 [#10522](https://github.com/pingcap/tiflow/issues/10522) @[sdojjy](https://github.com/sdojjy)
        - 修复在极端情况下 changefeed  的 `resolved ts` 不推进的问题 [#10157](https://github.com/pingcap/tiflow/issues/10157) @[sdojjy](https://github.com/sdojjy)
        - 修复并发创建多个 changefeed 时 TiCDC 返回 `ErrChangeFeedAlreadyExists` 错误的问题 [#10430](https://github.com/pingcap/tiflow/issues/10430) @[CharlesCheung96](https://github.com/CharlesCheung96)

    + TiDB Data Migration (DM)

        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + TiDB Lightning
        <--tw @ran-huang (2)-->
        - 修复 EBS BR 运行时 Lightning 可能导入失败的问题 [#49517](https://github.com/pingcap/tidb/issues/49517) @[mittalrishabh](https://github.com/mittalrishabh)
        - 修复以 MultiIngest 模式导入数据到 TiKV 时，数据可能丢失的问题 [#50198](https://github.com/pingcap/tidb/issues/50198) @[D3Hunter](https://github.com/D3Hunter)

    + Dumpling

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + TiUP

        - note [#issue](https://github.com/pingcap/tiup/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiup/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + TiDB Binlog

        - note [#issue](https://github.com/pingcap/tidb-binlog/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb-binlog/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
