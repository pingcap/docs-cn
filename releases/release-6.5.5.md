---
title: TiDB 6.5.5 Release Notes
summary: 了解 TiDB 6.5.5 版本的兼容性变更、改进提升，以及错误修复。
---

# TiDB 6.5.5 Release Notes

发版日期：2023 年 x 月 x 日

TiDB 版本：6.5.5

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v6.5/quick-start-with-tidb) | [生产部署](https://docs.pingcap.com/zh/tidb/v6.5/production-deployment-using-tiup) | [下载离线包](https://cn.pingcap.com/product-community/?version=v6.5.5#version-list)

## 改进提升

+ TiDB **tw@qiancai**

    - (dup): release-7.3.0.md > # 稳定性 * 新增部分优化器提示，包括 [`NO_MERGE_JOIN()`]、[`NO_INDEX_JOIN()`](/optimizer-hints.md#no_index_joint1_name--tl_name-)、[`NO_INDEX_MERGE_JOIN()`](/optimizer-hints.md#no_index_merge_joint1_name--tl_name-)、[`NO_HASH_JOIN()`](/optimizer-hints.md#no_hash_joint1_name--tl_name-)、[`NO_INDEX_HASH_JOIN()`](/optimizer-hints.md#no_index_hash_joint1_name--tl_name-) [#45520](https://github.com/pingcap/tidb/issues/45520) @[qw4990](https://github.com/qw4990)
    - 添加 coprocessor 相关的 request source 信息 [#46514](https://github.com/pingcap/tidb/issues/46514) @[you06](https://github.com/you06)

+ TiKV **tw@qiancai**

    - 新增 PD Client 连接重试过程中的 backoff 机制。异常错误重试期间，逐步增加重试时间间隔，减小 PD 压力 [#15428](https://github.com/tikv/tikv/issues/15428) @[nolouch](https://github.com/nolouch)
    - 增加 snapshot 相关的监控指标 [#15401](https://github.com/tikv/tikv/issues/15401) @[SpadeA-Tang](https://github.com/SpadeA-Tang)
    - 提高 PiTR checkpoint lag 在 leader 转移时的稳定性 [#13638](https://github.com/tikv/tikv/issues/13638) @[YuJuncen](https://github.com/YuJuncen)
    - 增加 `safe-ts` 相关的日志和监控指标 [#15082](https://github.com/tikv/tikv/issues/15082) @[ekexium](https://github.com/ekexium)
    - 为 `resolved-ts` 提供更多的相关日志和监控指标 [#15082](https://github.com/tikv/tikv/issues/15082) @[ekexium](https://github.com/ekexium)

+ Tools **tw@Oreoxmt**

    + Backup & Restore (BR)

        - 减少日志备份 `resolve lock` 的 CPU 开销 [#40759](https://github.com/pingcap/tidb/issues/40759) @[3pointer](https://github.com/3pointer)

    + TiDB Lightning


## 错误修复

+ TiDB **tw@Oreoxmt**

    - 修复读副本选择会可能选到不可用副本的问题 [#46198](https://github.com/pingcap/tidb/issues/46198) @[zyguan](https://github.com/zyguan)
    - 修复 Stale Read 和 Schema Cache 不适配导致额外开销的问题 [#43481](https://github.com/pingcap/tidb/issues/43481) @[crazycs520](https://github.com/crazycs520)

+ TiKV **tw@Oreoxmt**

    - 修复错误: 当tikv一个节点失败时，对应region的peers不应该不正确的进入休眠模式 [#14547](https://github.com/tikv/tikv/issues/14547) @[hicqu](https://github.com/hicqu)
    - 当size based split触发时发现没有可以分裂的key时，触发一次手动compaction用来消除过多的MVCC版本 [#15282](https://github.com/tikv/tikv/issues/15282) @[SpadeA-Tang](https://github.com/SpadeA-Tang)
    - 修复在线恢复数据时无法处理merge abort的问题 [#15580](https://github.com/tikv/tikv/issues/15580) @[v01dstar](https://github.com/v01dstar)
    - 修复PiTR潜在可能被阻塞的问题，当PD和TiKV之间网络隔离时. [#15279](https://github.com/tikv/tikv/issues/15279) @[YuJuncen](https://github.com/YuJuncen)

+ PD **tw@ran-huang**

    - 修复调度器启动时间长的问题 [#6920](https://github.com/tikv/pd/issues/6920) @[HuSharp](https://github.com/HuSharp)
    - 修复 Scatter Region 处理 Leader 和 Peer 的逻辑不一致的问题 [#6962](https://github.com/tikv/pd/issues/6962) @[bufferflies](https://github.com/bufferflies)

+ Tools

    + Backup & Restore (BR) **tw@ran-huang**

        - 修复 PITR 恢复隐式主键可能冲突的问题 [#46520](https://github.com/pingcap/tidb/issues/46520) @[3pointer](https://github.com/3pointer)
        - 修复 PITR 恢复 meta-kv 出错的问题 [#46578](https://github.com/pingcap/tidb/issues/46578) @[Leavrth](https://github.com/Leavrth)
        - 修复 br 集成测试用例出错的问题 [#45561](https://github.com/pingcap/tidb/issues/46561) @[purelind](https://github.com/purelind)
        - (dup): release-7.0.0.md > 错误修复> Tools> Backup & Restore (BR) - 缓解了 Region leadership 迁移导致 PITR 日志备份进度延迟变高的问题 [#13638](https://github.com/tikv/tikv/issues/13638) @[YuJuncen](https://github.com/YuJuncen)

    + TiCDC

        - 修复 PD 节点出现网络隔离时引起 TiCDC 同步延时变高的问题 [#9565](https://github.com/pingcap/tiflow/issues/9565)
        - 修复采用 CSV 格式时将 `UPDATE` 操作错误修改为 `INSERT` 的问题 [#9658](https://github.com/pingcap/tiflow/issues/9658)
        <!--以上 **tw@ran-huang**-->
        - 修复在部分日志中记录了用户密码的问题 [#9690](https://github.com/pingcap/tiflow/issues/9690)
        - 修复使用 SASL 认证时可能导致 TiCDC出现 panic 的问题 [#9669](https://github.com/pingcap/tiflow/issues/9669)
        - 修复 TiCDC 同步任务在某些特殊场景可能失败的问题 [#9685](https://github.com/pingcap/tiflow/issues/9685)[#9697](https://github.com/pingcap/tiflow/issues/9697)[#9695](https://github.com/pingcap/tiflow/issues/9695)[#9736](https://github.com/pingcap/tiflow/issues/9736)
        - 修复上游在 Region 非常多时，TiKV 节点出现故障导致 TiCDC 不能同步任务以及不能快速恢复的问题 [#9741](https://github.com/pingcap/tiflow/issues/9741)
         <!--以上 **tw@hfxsd**-->
    + TiDB Lightning **tw@hfxsd**

        - 修复 TiDB Lightning 在目标服务器部署 TiCDC 时无法启动的问题 [#41040](https://github.com/pingcap/tidb/issues/41040) @[lance6716](https://github.com/lance6716)
        - 修复 TiDB Lightning 在 PD 拓扑变更时无法启动的问题 [#46688](https://github.com/pingcap/tidb/issues/46688) @[lance6716](https://github.com/lance6716)
        - 修复 TiDB Lightning 在 PD 切换 Leader 后无法继续导入数据的问题 [#46540](https://github.com/pingcap/tidb/issues/46540) @[lance6716](https://github.com/lance6716)
        - (dup): release-6.6.0.md > 错误修复> Tools> TiDB Lightning - 修复 precheck 无法准确检测目标集群是否存在运行中的 TiCDC 的问题 [#41040](https://github.com/pingcap/tidb/issues/41040) @[lance6716](https://github.com/lance6716)
