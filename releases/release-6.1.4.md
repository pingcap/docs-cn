---
title: TiDB 6.1.4 Release Notes
summary: Learn about the new features, compatibility changes, improvements, and bug fixes in TiDB 6.1.4.
---

# TiDB 6.1.4 Release Notes

Release date: February 8, 2023

TiDB version: 6.1.4

Quick access: [Quick start](https://docs.pingcap.com/tidb/v6.1/quick-start-with-tidb) | [Production deployment](https://docs.pingcap.com/tidb/v6.1/production-deployment-using-tiup) | [Installation packages](https://www.pingcap.com/download/?version=v6.1.4#version-list)

## Compatibility changes

- TiDB

    - No longer support modifying column types on partitioned tables because of potential correctness issues [#40620](https://github.com/pingcap/tidb/issues/40620) @[mjonss](https://github.com/mjonss)

## Improvements

- TiFlash

    - Reduce the IOPS by up to 95% and the write amplification by up to 65% for TiFlash instances under high update throughput workloads [#6460](https://github.com/pingcap/tiflash/issues/6460) @[flowbehappy](https://github.com/flowbehappy)

- Tools

    - TiCDC

        - Add the DML batch operation mode to improve the throughput when SQL statements are generated in batches [#7653](https://github.com/pingcap/tiflow/issues/7653) @[asddongmen](https://github.com/asddongmen)
        - Support storing redo logs to GCS- or Azure-compatible object storage [#7987](https://github.com/pingcap/tiflow/issues/7987) @[CharlesCheung96](https://github.com/CharlesCheung96)

    - TiDB Lightning

        - Change the severity of the precheck items `clusterResourceCheckItem` and `emptyRegionCheckItem` from `Critical` to `Warning` [#37654](https://github.com/pingcap/tidb/issues/37654) @[niubell](https://github.com/niubell)

## Bug fixes

+ TiDB

    - Fix the issue that when you create a table, the default value and the type of a column are not consistent and are not automatically corrected [#34881](https://github.com/pingcap/tidb/issues/34881) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger) @[mjonss](https://github.com/mjonss)
    - Fix the data race issue in the `LazyTxn.LockKeys` function [#40355](https://github.com/pingcap/tidb/issues/40355) @[HuSharp](https://github.com/HuSharp)
    - Fix the issue that the `INSERT` or `REPLACE` statements might panic in long session connections [#40351](https://github.com/pingcap/tidb/issues/40351) @[fanrenhoo](https://github.com/fanrenhoo)
    - Fix the issue that reading data using the "cursor read" method might return an error because of GC [#39447](https://github.com/pingcap/tidb/issues/39447) @[zyguan](https://github.com/zyguan)
    - Fix the issue that the [`pessimistic-auto-commit`](/tidb-configuration-file.md#pessimistic-auto-commit-new-in-v600) configuration item does not take effect for point-get queries [#39928](https://github.com/pingcap/tidb/issues/39928) @[zyguan](https://github.com/zyguan)
    - Fix the issue that querying the `INFORMATION_SCHEMA.TIKV_REGION_STATUS` table returns an incorrect result [#37436](https://github.com/pingcap/tidb/issues/37436) @[zimulala](https://github.com/zimulala)
    - Fix the issue that the `IN` and `NOT IN` subqueries in some patterns report the `Can't find column` error [#37032](https://github.com/pingcap/tidb/issues/37032) @[AilinKid](https://github.com/AilinKid) @[lance6716](https://github.com/lance6716)

- PD

    - Fix the issue that PD might unexpectedly add multiple Learners to a Region [#5786](https://github.com/tikv/pd/issues/5786) @[HunDunDM](https://github.com/HunDunDM)

+ TiKV

    - Fix the issue that TiDB fails to start on Gitpod when there are multiple `cgroup` and `mountinfo` records [#13660](https://github.com/tikv/tikv/issues/13660) @[tabokie](https://github.com/tabokie)
    - Fix the issue that tikv-ctl is terminated unexpectedly when executing the `reset-to-version` command [#13829](https://github.com/tikv/tikv/issues/13829) @[tabokie](https://github.com/tabokie)
    - Fix the issue that TiKV mistakenly reports a `PessimisticLockNotFound` error [#13425](https://github.com/tikv/tikv/issues/13425) @[sticnarf](https://github.com/sticnarf)
    - Fix the issue that TiKV might panic when the size of one single write exceeds 2 GiB [#13848](https://github.com/tikv/tikv/issues/13848) @[YuJuncen](https://github.com/YuJuncen)
    - Fix the data inconsistency issue caused by network failure between TiDB and TiKV during the execution of a DML after a failed pessimistic DML [#14038](https://github.com/tikv/tikv/issues/14038) @[MyonKeminta](https://github.com/MyonKeminta)
    - Fix the issue that `_` in the `LIKE` operator cannot match non-ASCII characters when new collation is not enabled [#13769](https://github.com/tikv/tikv/issues/13769) @[YangKeao](https://github.com/YangKeao) @[tonyxuqqi](https://github.com/tonyxuqqi)

+ TiFlash

    - Fix the issue that TiFlash global locks are blocked for a long time occasionally [#6418](https://github.com/pingcap/tiflash/issues/6418) @[SeaRise](https://github.com/SeaRise)
    - Fix the issue that high throughput writes cause OOM [#6407](https://github.com/pingcap/tiflash/issues/6407) @[JaySon-Huang](https://github.com/JaySon-Huang)

+ Tools

    + Backup & Restore (BR)

        - Fix the issue that restore is interrupted due to failure in getting the Region size [#36053](https://github.com/pingcap/tidb/issues/36053) @[YuJuncen](https://github.com/YuJuncen)
        - Fix the issue that causes panic when BR debugs the `backupmeta` file [#40878](https://github.com/pingcap/tidb/issues/40878) @[MoCuishle28](https://github.com/MoCuishle28)

    + TiCDC

        - Fix the issue that the checkpoint cannot advance when TiCDC replicates an excessively large number of tables [#8004](https://github.com/pingcap/tiflow/issues/8004) @[asddongmen](https://github.com/asddongmen)
        - Fix the issue that `transaction_atomicity` and `protocol` cannot be updated via the configuration file [#7935](https://github.com/pingcap/tiflow/issues/7935) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - Fix the issue that TiCDC mistakenly reports an error when the version of TiFlash is later than that of TiCDC [#7744](https://github.com/pingcap/tiflow/issues/7744) @[overvenus](https://github.com/overvenus)
        - Fix the issue that OOM occurs when TiCDC replicates large transactions [#7913](https://github.com/pingcap/tiflow/issues/7913) @[overvenus](https://github.com/overvenus)
        - Fix a bug that the context deadline is exceeded when TiCDC replicates data without splitting large transactions [#7982](https://github.com/pingcap/tiflow/issues/7982) @[hi-rustin](https://github.com/hi-rustin)
        - Fix the issue that `sasl-password` in the `changefeed query` result is not masked [#7182](https://github.com/pingcap/tiflow/issues/7182) @[dveeden](https://github.com/dveeden)
        - Fix the issue that data is lost when a user quickly deletes a replication task and then creates another one with the same task name [#7657](https://github.com/pingcap/tiflow/issues/7657) @[overvenus](https://github.com/overvenus)

    + TiDB Data Migration (DM)

        - Fix a bug that DM might raise an error during precheck when the downstream database name in `SHOW GRANTS` contains a wildcard ("*") [#7645](https://github.com/pingcap/tiflow/issues/7645) @[lance6716](https://github.com/lance6716)
        - Fix the issue that DM prints too many logs caused by "COMMIT" in binlog query events [#7525](https://github.com/pingcap/tiflow/issues/7525) @[liumengya94](https://github.com/liumengya94)
        - Fix the issue that the DM task fails to start when only `ssl-ca` is configured for SSL [#7941](https://github.com/pingcap/tiflow/issues/7941) @[liumengya94](https://github.com/liumengya94)
        - Fix a bug that when the expression filters of both "update" and "non-update" types are specified in one table, all `UPDATE` statements are skipped [#7831](https://github.com/pingcap/tiflow/issues/7831) @[lance6716](https://github.com/lance6716)
        - Fix a bug that when only one of `update-old-value-expr` or `update-new-value-expr` is set for a table, the filter rule does not take effect or DM panics [#7774](https://github.com/pingcap/tiflow/issues/7774) @[lance6716](https://github.com/lance6716)

    + TiDB Lightning

        - Fix the memory leakage issue when TiDB Lightning imports a huge source data file [#39331](https://github.com/pingcap/tidb/issues/39331) @[dsdashun](https://github.com/dsdashun)
        - Fix the issue that TiDB Lightning prechecks cannot find dirty data left by previously failed imports [#39477](https://github.com/pingcap/tidb/issues/39477) @[dsdashun](https://github.com/dsdashun)
