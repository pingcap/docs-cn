---
title: TiDB 6.5.2 Release Notes
summary: 了解 TiDB 6.5.2 版本的兼容性变更、改进提升，以及错误修复。
---

# TiDB 6.5.2 Release Notes

发版日期：2023 年 4 月 21 日

TiDB 版本：6.5.2

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v6.5/quick-start-with-tidb) | [生产部署](https://docs.pingcap.com/zh/tidb/v6.5/production-deployment-using-tiup) | [下载离线包](https://cn.pingcap.com/product-community/?version=v6.5.2#version-list)

## 兼容性变更

- TiCDC 修复了 Avro 编码 `FLOAT` 类型数据错误的问题 [#8490](https://github.com/pingcap/tiflow/issues/8490) @[3AceShowHand](https://github.com/3AceShowHand)

    在升级 TiCDC 集群到 v6.5.2 或更高的 v6.5.x 版本时，如果使用 Avro 同步的表包含 `FLOAT` 类型数据，请在升级前手动调整 Confluent Schema Registry 的兼容性策略为 `None`，使 changefeed 能够成功更新 schema。否则，在升级之后 changefeed 将无法更新 schema 并进入错误状态。

- 为了解决同步分区表到存储服务时可能丢数据的问题，TiCDC 配置项 [`sink.enable-partition-separator`](/ticdc/ticdc-changefeed-config.md#ticdc-changefeed-配置文件说明) 默认值从 `false` 修改为 `true`，代表默认会将表中各个分区的数据分不同的目录来存储。建议保持该配置项为 `true` 以避免该问题。[#8724](https://github.com/pingcap/tiflow/issues/8724) @[CharlesCheung96](https://github.com/CharlesCheung96)

## 改进提升

+ TiDB

    - Prepared Plan Cache 支持缓存 BatchPointGet 计划 [#42125](https://github.com/pingcap/tidb/issues/42125) @[qw4990](https://github.com/qw4990)
    - Index Join 支持更多的 SQL 格式 [#40505](https://github.com/pingcap/tidb/issues/40505) @[Yisaer](https://github.com/Yisaer)
    - 将 Index Merge Reader 中的一些 Log 等级从 `"info"` 降低为 `"debug"` [#41949](https://github.com/pingcap/tidb/issues/41949) @[yibin87](https://github.com/yibin87)
    - 优化带 Limit 的 Range 类型分区表的 `distsql_concurrency` 设置以降低查询延迟 [#41480](https://github.com/pingcap/tidb/issues/41480) @[you06](https://github.com/you06)

+ TiFlash

    - 减少了 TiFlash 在读取过程中的任务调度对 CPU 的消耗 [#6495](https://github.com/pingcap/tiflash/issues/6495) @[JinheLin](https://github.com/JinheLin)
    - 提升默认参数下 BR 和 TiDB Lightning 向 TiFlash 导入数据的性能 [#7272](https://github.com/pingcap/tiflash/issues/7272) @[breezewish](https://github.com/breezewish)

+ Tools

    + TiCDC

        - 发布 TiCDC Open API v2.0 [#8743](https://github.com/pingcap/tiflow/issues/8743) @[sdojjy](https://github.com/sdojjy)
        - 引入 `gomemlimit` 以防止 TiCDC 出现 OOM 问题 [#8675](https://github.com/pingcap/tiflow/issues/8675) @[amyangfei](https://github.com/amyangfei)
        - 采用 multi-statement 的方式优化批量执行 `UPDATE` 场景下的同步性能 [#8057](https://github.com/pingcap/tiflow/issues/8057) @[amyangfei](https://github.com/amyangfei)
        - 支持在 redo applier 中拆分事务以提升 apply 吞吐，降低灾难场景的 RTO [#8318](https://github.com/pingcap/tiflow/issues/8318) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - 支持在 redo log 里 apply DDL 事件 [#8361](https://github.com/pingcap/tiflow/issues/8361) @[CharlesCheung96](https://github.com/CharlesCheung96)

    + TiDB Lightning

        - 支持导入带有 BOM header 的 CSV 数据文件 [#40744](https://github.com/pingcap/tidb/issues/40744) @[dsdashun](https://github.com/dsdashun)

## 错误修复

+ TiDB

    - 修复缓存表执行新增列操作后，新增列值为 `NULL` 而非列的默认值的问题 [#42928](https://github.com/pingcap/tidb/issues/42928) @[lqs](https://github.com/lqs)
    - 修复分区特别多并且带有 TiFlash 副本的分区表在执行 `TRUNCATE TABLE` 时，出现写冲突导致 DDL 重试的问题 [#42940](https://github.com/pingcap/tidb/issues/42940) @[mjonss](https://github.com/mjonss)
    - 修复对于执行中的 `DROP TABLE` 操作，`ADMIN SHOW DDL JOBS` 的结果中缺少表名的问题 [#42268](https://github.com/pingcap/tidb/issues/42268) @[tiancaiamao](https://github.com/tiancaiamao)
    - 修复读取 cgroup 信息出错导致 TiDB Server 无法启动的问题，报错信息为 "can't read file memory.stat from cgroup v1: open /sys/memory.stat no such file or directory" [#42659](https://github.com/pingcap/tidb/issues/42659) @[hawkingrei](https://github.com/hawkingrei)
    - 修复在分区表上执行修改列操作时，数据截断没有正确发出警告的问题 [#24427](https://github.com/pingcap/tidb/issues/24427) @[mjonss](https://github.com/mjonss)
    - 修复了生成执行计划过程中，因为获取的 InfoSchema 不一致而导致的 TiDB panic 的问题 [#41622](https://github.com/pingcap/tidb/issues/41622) @[tiancaiamao](https://github.com/tiancaiamao)
    - 修复了使用 DDL 修改浮点类型时，保持长度不变且减少小数位后，旧数据仍然保持原样的问题 [#41281](https://github.com/pingcap/tidb/issues/41281) @[zimulala](https://github.com/zimulala)
    - 修复事务内执行 PointUpdate 之后，`SELECT` 结果不正确的问题 [#28011](https://github.com/pingcap/tidb/issues/28011) @[zyguan](https://github.com/zyguan)
    - 修复在使用 Cursor Fetch 且在 Execute、Fetch、Close 之间运行其它语句后，Fetch 与 Close 命令可能会返回错误结果或造成 TiDB Panic 的问题 [#40094](https://github.com/pingcap/tidb/issues/40094) @[YangKeao](https://github.com/YangKeao)
    - 修复 `INSERT IGNORE` 和 `REPLACE` 语句对不修改 value 的 key 没有加锁的问题 [#42121](https://github.com/pingcap/tidb/issues/42121) @[zyguan](https://github.com/zyguan)
    - 修复 TiFlash 执行中遇到生成列会报错的问题 [#40663](https://github.com/pingcap/tidb/issues/40663) @[guo-shaoge](https://github.com/guo-shaoge)
    - 修复当同一个 SQL 中出现多个不同的分区表时，TiDB 可能执行得到错误结果的问题 [#42135](https://github.com/pingcap/tidb/issues/42135) @[mjonss](https://github.com/mjonss)
    - 修复在开启 Prepared Plan Cache 的情况下，索引全表扫可能会报错的问题 [#42150](https://github.com/pingcap/tidb/issues/42150) @[fzzf678](https://github.com/fzzf678)
    - 修复在开启 Prepared Plan Cache 时 Index Merge 可能得到错误结果的问题 [#41828](https://github.com/pingcap/tidb/issues/41828) @[qw4990](https://github.com/qw4990)
    - 修复了设置 `max_prepared_stmt_count` 不生效的问题 [#39735](https://github.com/pingcap/tidb/issues/39735) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes)
    - 修复全局内存控制可能错误地 Kill 内存使用量小于 `tidb_server_memory_limit_sess_min_size` 的 SQL 的问题 [#42662](https://github.com/pingcap/tidb/issues/41828) @[XuHuaiyu](https://github.com/XuHuaiyu)
    - 修复分区表动态裁剪模式下 Index Join 可能导致 panic 的问题 [#40596](https://github.com/pingcap/tidb/issues/40596) @[tiancaiamao](https://github.com/tiancaiamao)

+ TiKV

    - 修复 TiKV 解析 cgroup path 没有正确解析 `:` 符号的问题 [#14538](https://github.com/tikv/tikv/issues/14538) @[SpadeA-Tang](https://github.com/SpadeA-Tang)

+ PD

    - 修复 PD 可能会非预期地向 Region 添加多个 Learner 的问题 [#5786](https://github.com/tikv/pd/issues/5786) @[HunDunDM](https://github.com/HunDunDM)
    - 修复了切换 Placement Rule 时可能存在的 leader 分布不均衡的问题 [#6195](https://github.com/tikv/pd/issues/6195) @[bufferflies](https://github.com/bufferflies)

+ TiFlash

    - 修复 TiFlash 无法识别生成列的问题 [#6801](https://github.com/pingcap/tiflash/issues/6801) @[guo-shaoge](https://github.com/guo-shaoge)
    - 修复了 Decimal 除法在某些情况下最后一位未进位的问题 [#7022](https://github.com/pingcap/tiflash/issues/7022) @[LittleFall](https://github.com/LittleFall)
    - 修复了 Decimal 转换在某些情况下进位错误的问题 [#6994](https://github.com/pingcap/tiflash/issues/6994) @[windtalker](https://github.com/windtalker)
    - 修复了开启 new collation 后 TopN/Sort 算子结果可能出错的问题 [#6807](https://github.com/pingcap/tiflash/issues/6807) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - 修复由于不兼容 TiCDC 导致 TiFlash 进程失败的问题 [#7212](https://github.com/pingcap/tiflash/issues/7212) @[hongyunyan](https://github.com/hongyunyan)

+ Tools

    + Backup & Restore (BR)

        - 修复当 TiDB 集群不存在 PITR 备份任务时，`resolve lock` 频率过高的问题 [#40759](https://github.com/pingcap/tidb/issues/40759) @[joccau](https://github.com/joccau)
        - 修复了在 PITR 恢复过程中等待 split Region 重试的时间不足的问题 [#42001](https://github.com/pingcap/tidb/issues/42001) @[joccau](https://github.com/joccau)

    + TiCDC

        - 修复同步到对象存储时，partition 分隔符不生效问题 [#8581](https://github.com/pingcap/tiflow/issues/8581) @[CharlesCheung96](https://github.com/CharlesCheung96) @[hi-rustin](https://github.com/Rustin170506)
        - 修复同步到对象存储时，表调度可能导致数据丢失的问题 [#8256](https://github.com/pingcap/tiflow/issues/8256) @[zhaoxinyu](https://github.com/zhaoxinyu)
        - 修复不可重入的 DDL 导致同步卡住的问题 [#8662](https://github.com/pingcap/tiflow/issues/8662) @[hicqu](https://github.com/hicqu)
        - 修复同步到对象存储时，TiCDC 扩缩容可能导致数据丢失的问题 [#8666](https://github.com/pingcap/tiflow/issues/8666) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - 修复在部分场景中 `cgroup` 的内存限制不生效问题 [#8588](https://github.com/pingcap/tiflow/issues/8588) @[amyangfei](https://github.com/amyangfei)
        - 修复 Redo log 在 apply 时，特殊情况下出现数据丢失的问题 [#8591](https://github.com/pingcap/tiflow/issues/8591) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - 修复 `db sorter` 使用内存时未受 `cgroup memory limit` 限制的问题 [#8588](https://github.com/pingcap/tiflow/issues/8588) @[amyangfei](https://github.com/amyangfei)
        - 修复同步数据时由于 `UPDATE` 和 `INSERT` 语句乱序可能导致 `Duplicate entry` 错误的问题 [#8597](https://github.com/pingcap/tiflow/issues/8597) @[sdojjy](https://github.com/sdojjy)
        - 修复由于 PD 和 TiCDC 之间的网络隔离引起 TiCDC 程序异常退出的问题 [#8562](https://github.com/pingcap/tiflow/issues/8562) @[overvenus](https://github.com/overvenus)
        - 修复了 Kubernetes 上不能平滑升级 (graceful upgrade) TiCDC 集群的问题 [#8484](https://github.com/pingcap/tiflow/issues/8484) @[overvenus](https://github.com/overvenus)
        - 修复了当所有 Kafka server 不可访问时会导致 TiCDC server panic 的问题 [#8523](https://github.com/pingcap/tiflow/issues/8523) @[3AceShowHand](https://github.com/3AceShowHand)
        - 修复了重启 changefeed 可能导致数据丢失或者 checkpoint 无法推进的问题 [#8242](https://github.com/pingcap/tiflow/issues/8242) @[overvenus](https://github.com/overvenus)
