---
title: TiDB 8.8.6 Release Notes
summary: 了解 TiDB 8.8.6 版本的兼容性变更、改进提升，以及错误修复。
---

# TiDB 8.8.6 Release Notes

发版日期：2026 年 x 月 x 日

TiDB 版本：8.8.6

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v8.8/quick-start-with-tidb) | [生产部署](https://docs.pingcap.com/zh/tidb/v8.8/production-deployment-using-tiup) | [下载离线包](https://pingkai.cn/download#tidb-community)

## 兼容性变更

- note [#issue](https://github.com/pingcap/${repo-name}/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

## 改进提升

+ TiDB

    - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

+ TiKV

    - note [#issue](https://github.com/tikv/tikv/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/tikv/tikv/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - (dup): release-8.5.4.md > 改进提升> TiKV - 优化 gRPC 线程池线程数量默认值的计算方式，将原固定值调整为根据总的 CPU 配置动态计算，避免因 gRPC 线程数量过小导致的性能瓶颈 [#18613](https://github.com/tikv/tikv/issues/18613) @[LykxSassinator](https://github.com/LykxSassinator)
    - (dup): release-8.5.5.md > 改进提升> TiKV - 在 TiKV 内存占用高时，对 BR 的日志恢复请求进行限流，防止 TiKV OOM [#18124](https://github.com/tikv/tikv/issues/18124) @[3pointer](https://github.com/3pointer)

+ PD

    - note [#issue](https://github.com/tikv/pd/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/tikv/pd/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - (dup): release-8.5.5.md > 改进提升> PD - 优化了高基数指标，降低 PD 的内存占用和监控系统压力 [#9357](https://github.com/tikv/pd/issues/9357) @[rleungx](https://github.com/rleungx)
    - (dup): release-7.5.7.md > 改进提升> PD - 减少非必要的错误日志 [#9370](https://github.com/tikv/pd/issues/9370) @[bufferflies](https://github.com/bufferflies)

+ TiFlash

    - note [#issue](https://github.com/pingcap/tiflash/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/pingcap/tiflash/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

+ Tools

    + Backup & Restore (BR)

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + TiCDC

        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

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

## 错误修复

+ TiDB

    - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

+ TiKV

    - note [#issue](https://github.com/tikv/tikv/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/tikv/tikv/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - (dup): release-5.1.4.md > Bug 修复> TiKV - 修复悲观事务中 prewrite 请求重试在极少数情况下影响数据一致性的风险 [#11187](https://github.com/tikv/tikv/issues/11187)

+ PD

    - note [#issue](https://github.com/tikv/pd/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/tikv/pd/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - (dup): release-8.5.4.md > 错误修复> PD - 修复 Resource Manager 错误分配 token 导致查询卡住的问题 [#9455](https://github.com/tikv/pd/issues/9455) @[JmPotato](https://github.com/JmPotato)

+ TiFlash

    - note [#issue](https://github.com/pingcap/tiflash/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/pingcap/tiflash/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

+ Tools

    + Backup & Restore (BR)

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - (dup): release-8.5.5.md > 错误修复> Tools> Backup & Restore (BR) - 修复集群中存在大量 Region 时，开启日志备份导致内存占用过高的问题 [#18719](https://github.com/tikv/tikv/issues/18719) @[YuJuncen](https://github.com/YuJuncen)

    + TiCDC

        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

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

## Other dup notes

- (dup): release-8.5.4.md > 新功能 * 支持表级别数据打散功能（实验特性）[#63260](https://github.com/pingcap/tidb/issues/63260) @[bufferflies](https://github.com/bufferflies)
- (dup): release-8.5.5.md > # 性能> 如需重建索引，则采用更高效的 Ingest 流程，大幅提升索引重建性能。 * 支持表级数据亲和性 (AFFINITY)，提升查询性能（实验特性） [#9764](https://github.com/tikv/pd/issues/9764) @[lhy1024](https://github.com/lhy1024)
- (dup): release-9.0.0.md > # 数据迁移 * 将 sync-diff-inspector 从 `pingcap/tidb-tools` 迁移至 `pingcap/tiflow` 代码仓库 [#11672](https://github.com/pingcap/tiflow/issues/11672) @[joechenrh](https://github.com/joechenrh)
- (dup): release-8.4.0.md > # 稳定性 * 支持为资源管控的后台任务设置资源上限 [#56019](https://github.com/pingcap/tidb/issues/56019) @[glorv](https://github.com/glorv)
- (dup): release-8.5.5.md > # SQL 功能 * 支持在线修改分布式 `ADD INDEX` 任务的并发和吞吐 [#64947](https://github.com/pingcap/tidb/issues/64947) @[joechenrh](https://github.com/joechenrh)