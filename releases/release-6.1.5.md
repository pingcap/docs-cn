---
title: TiDB 6.1.5 Release Notes
summary: Learn about the compatibility changes, improvements, and bug fixes in TiDB 6.1.5.
---

# TiDB 6.1.5 Release Notes

Release date: February 28, 2023

TiDB version: 6.1.5

Quick access: [Quick start](https://docs.pingcap.com/tidb/v6.1/quick-start-with-tidb) | [Production deployment](https://docs.pingcap.com/tidb/v6.1/production-deployment-using-tiup) | [Installation packages](https://www.pingcap.com/download/?version=v6.1.5#version-list)

## Compatibility changes

- Starting from February 20, 2023, the [telemetry feature](/telemetry.md) is disabled by default in new versions of TiDB and TiDB Dashboard, including v6.1.5, and usage information is not collected and shared with PingCAP. Before upgrading to these versions, if the cluster uses the default telemetry configuration, the telemetry feature is disabled after the upgrade. See [TiDB Release Timeline](/releases/release-timeline.md) for a specific version.

    - The default value of the [`tidb_enable_telemetry`](/system-variables.md#tidb_enable_telemetry-new-in-v402) system variable is changed from `ON` to `OFF`.
    - The default value of the TiDB [`enable-telemetry`](/tidb-configuration-file.md#enable-telemetry-new-in-v402) configuration item is changed from `true` to `false`.
    - The default value of the PD [`enable-telemetry`](/pd-configuration-file.md#enable-telemetry) configuration item is changed from `true` to `false`.

- Starting from v1.11.3, the telemetry feature is disabled by default in newly deployed TiUP, and usage information is not collected. If you upgrade from a TiUP version earlier than v1.11.3 to v1.11.3 or a later version, the telemetry feature keeps the same status as before the upgrade.

## Improvements

- TiDB

    - Support the `AUTO_RANDOM` column as the first column of the clustered composite index [#38572](https://github.com/pingcap/tidb/issues/38572) @[tangenta](https://github.com/tangenta)

## Bug fixes

+ TiDB

    - Fix the issue that data race might cause TiDB to restart [#27725](https://github.com/pingcap/tidb/issues/27725) @[XuHuaiyu](https://github.com/XuHuaiyu)
    - Fix the issue that the `UPDATE` statement might not read the latest data when the Read Committed isolation level is used [#41581](https://github.com/pingcap/tidb/issues/41581) @[cfzjywxk](https://github.com/cfzjywxk)

- PD

    - Fix the PD OOM issue that occurs when the calls of `ReportMinResolvedTS` are too frequent [#5965](https://github.com/tikv/pd/issues/5965) @[HundunDM](https://github.com/HunDunDM)

+ Tools

    + TiCDC

        - Fix the issue that applying redo log might cause OOM when the replication lag is excessively high [#8085](https://github.com/pingcap/tiflow/issues/8085) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - Fix the issue that the performance degrades when redo log is enabled to write meta [#8074](https://github.com/pingcap/tiflow/issues/8074) @[CharlesCheung96](https://github.com/CharlesCheung96)

    + TiDB Data Migration (DM)

        - Fix the issue that the `binlog-schema delete` command fails to execute [#7373](https://github.com/pingcap/tiflow/issues/7373) @[liumengya94](https://github.com/liumengya94)
        - Fix the issue that the checkpoint does not advance when the last binlog is a skipped DDL [#8175](https://github.com/pingcap/tiflow/issues/8175) @[D3Hunter](https://github.com/D3Hunter)
