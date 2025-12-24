---
title: TiDB 6.1.5 Release Notes
summary: 了解 TiDB 6.1.5 版本的兼容性变更、改进提升，以及错误修复。
---

# TiDB 6.1.5 Release Notes

发版日期：2023 年 2 月 28 日

TiDB 版本：6.1.5

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v6.1/quick-start-with-tidb) | [生产部署](https://docs.pingcap.com/zh/tidb/v6.1/production-deployment-using-tiup)

## 兼容性变更

- 自 2023 年 2 月 20 日起，新发布的 TiDB 和 TiDB Dashboard 版本（包含 6.1.5），默认关闭[遥测功能](/telemetry.md)，即默认不再收集使用情况信息分享给 PingCAP。如果升级至这些版本前使用默认的遥测配置，则升级后遥测功能处于关闭状态。具体的版本可参考 [TiDB 版本发布时间线](/releases/release-timeline.md)。

    - 系统变量 [`tidb_enable_telemetry`](/system-variables.md#tidb_enable_telemetry-从-v402-版本开始引入) 默认值由 `ON` 修改为 `OFF`。
    - TiDB 配置项 [`enable-telemetry`](/tidb-configuration-file.md#enable-telemetry-从-v402-版本开始引入) 默认值由 `true` 改为 `false`。
    - PD 配置项 [`enable-telemetry`](/pd-configuration-file.md#enable-telemetry) 默认值由 `true` 改为 `false`。

- 从 v1.11.3 起，新部署的 TiUP 默认关闭遥测功能，即默认不再收集使用情况信息。如果从 v1.11.3 之前的 TiUP 版本升级至 v1.11.3 或更高 TiUP 版本，遥测保持升级前的开启或关闭状态。

## 提升改进

- TiDB

    - 允许 `AUTO_RANDOM` 列作为聚簇复合索引中的第一列 [#38572](https://github.com/pingcap/tidb/issues/38572) @[tangenta](https://github.com/tangenta)

## Bug 修复

+ TiDB

    - 修复 data race 可能导致 TiDB 重启的问题 [#27725](https://github.com/pingcap/tidb/issues/27725) @[XuHuaiyu](https://github.com/XuHuaiyu)
    - 修复当使用 Read Committed 隔离级别时 `UPDATE` 语句可能读不到最新数据的问题 [#41581](https://github.com/pingcap/tidb/issues/41581) @[cfzjywxk](https://github.com/cfzjywxk)

- PD

    - 修复调用 `ReportMinResolvedTS` 过于频繁导致 PD OOM 的问题 [#5965](https://github.com/tikv/pd/issues/5965) @[HundunDM](https://github.com/HunDunDM)

+ Tools

    + TiCDC

        - 修复当同步的延迟过大时 apply redo log 可能会出现 OOM 的问题 [#8085](https://github.com/pingcap/tiflow/issues/8085) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - 修复当开启 redo log 写 meta 时性能下降的问题 [#8074](https://github.com/pingcap/tiflow/issues/8074) @[CharlesCheung96](https://github.com/CharlesCheung96)

    + TiDB Data Migration (DM)

        - 修复 `binlog-schema delete` 命令执行失败的问题 [#7373](https://github.com/pingcap/tiflow/issues/7373) @[liumengya94](https://github.com/liumengya94)
        - 修复当最后一个 binlog 是被 skip 的 DDL 时，checkpoint 不推进的问题 [#8175](https://github.com/pingcap/tiflow/issues/8175) @[D3Hunter](https://github.com/D3Hunter)
