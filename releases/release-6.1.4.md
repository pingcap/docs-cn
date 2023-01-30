---
title: TiDB 6.1.4 Release Notes
---

# TiDB 6.1.4 Release Notes

发版日期：2023 年 2 月 8 日

TiDB 版本：6.1.4

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v6.1/quick-start-with-tidb) | [生产部署](https://docs.pingcap.com/zh/tidb/v6.1/production-deployment-using-tiup) | [下载离线包](https://cn.pingcap.com/product-community/?version=v6.1.4#version-list)

## 兼容性变更

- Tools

    - TiCDC

        - 

## 提升改进

- PD

    - 

- TiFlash

    - Reduce the IOPS and write amplification of TiFlash under high update throughput workloads. [#6460](https://github.com/pingcap/tiflash/issues/6460) @[ti-chi-bot](https://github.com/ti-chi-bot)

- Tools

    - TiCDC

        - 
    
    - Lightning

        - Change severity of clusterResourceCheckItem,emptyRegionCheckItem from Critical to Warn [#37654](https://github.com/pingcap/tidb/issues/37654) @[lance6716](https://github.com/lance6716) 

## Bug 修复

+ TiDB

    tidb

    (dup: release-6.2.0.md > Bug fixes> TiDB)- Fix the issue that when you create a table, the default value and the type of a column are not consistent and are not automatically corrected [#34881](https://github.com/pingcap/tidb/issues/34881) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger) @[mjonss](https://github.com/mjonss)

    transaction

    - session: fix data race in the LazyTxn.LockKeys [#40355](https://github.com/pingcap/tidb/issues/40355) @[HuSharp](https://github.com/HuSharp)
    - Fix the case that INSERT/REPLACE might panic in a long session connection [#40351](https://github.com/pingcap/tidb/issues/40351) @[fanrenhoo](https://github.com/fanrenhoo)

    sql-infra
    
    - Block modify column of partitioned table, even if it was not changing data when put into the DDL queue. [#40620](https://github.com/pingcap/tidb/issues/40620) @[ti-chi-bot](https://github.com/ti-chi-bot)
    - 

    planner

    (dup: release-6.3.0.md > Bug fixes> TiDB> Fix the issue that querying `INFORMATION_SCHEMA.TIKV_REGION_STATUS` returns an incorrect result @[zimulala](https://github.com/zimulala))- Fix the issue that the `IN` and `NOT IN` subqueries in some patterns report the `Can't find column` error [#37032](https://github.com/pingcap/tidb/issues/37032) @[AilinKid](https://github.com/AilinKid) @[lance6716](https://github.com/lance6716)

- PD

    - Fix an issue that PD may repeatedly add Learner to a Region. [#5786](https://github.com/tikv/pd/issues/5786) @[ti-chi-bot](https://github.com/ti-chi-bot)   

+ TiKV

    (dup: release-6.4.0.md > Bug fixes> TiKV)- Fix the issue that TiDB fails to start on Gitpod when there are multiple `cgroup` and `mountinfo` records [#13660](https://github.com/tikv/tikv/issues/13660) @[tabokie](https://github.com/tabokie) @[ti-srebot](https://github.com/ti-srebot)
    (dup: release-6.5.0.md > Bug fixes> TiKV)- Fix the issue that tikv-ctl is terminated unexpectedly when executing the `reset-to-version` command [#13829](https://github.com/tikv/tikv/issues/13829) @[tabokie](https://github.com/tabokie) @[ti-chi-bot](https://github.com/ti-chi-bot)
    - Fixed a problem that when a transaction in TiDB fails to execute a pessimistic DML and then executes another DML, if there are random network failures between TiDB and TiKV, it has risk to cause data inconsistency. [#40114](https://github.com/pingcap/tidb/issues/40114) @[ti-chi-bot](https://github.com/ti-chi-bot)
    - Fix panic when the size of one single write exceeds 2GiB. [#13848](https://github.com/tikv/tikv/issues/13848) @[YuJuncen](https://github.com/YuJuncen)
    (dup: release-6.3.0.md > Bug fixes> TiKV)- Fix the issue that TiKV mistakenly reports a `PessimisticLockNotFound` error [#13425](https://github.com/tikv/tikv/issues/13425) @[sticnarf](https://github.com/sticnarf) @[ti-srebot](https://github.com/ti-srebot)
    - Fixed a problem that when a transaction in TiDB fails to execute a pessimistic DML and then executes another DML, if there are random network failures between TiDB and TiKV, it has risk to cause data inconsistency. [#14038](https://github.com/tikv/tikv/issues/14038) @[ti-chi-bot](https://github.com/ti-chi-bot)
    (dup: release-6.5.0.md > Bug fixes> TiKV)- Fix the issue that `_` in the `LIKE` operator cannot match non-ASCII characters when new collation is not enabled [#13769](https://github.com/tikv/tikv/issues/13769) @[YangKeao](https://github.com/YangKeao) @[tonyxuqqi](https://github.com/tonyxuqqi)

+ TiFlash

    - Avoid tiflash global locks with small probability of long term blocking. [#6418](https://github.com/pingcap/tiflash/issues/6418) @[SeaRise](https://github.com/SeaRise)
    - Fix an issue that causes OOM with high throughput write [#6407](https://github.com/pingcap/tiflash/issues/6407) @[hehechen](https://github.com/hehechen)
    - Reduce memory usage under heavy write pressure. [#6431](https://github.com/pingcap/tiflash/issues/6431) @[SeaRise](https://github.com/SeaRise)

+ Tools

    + Backup & Restore (BR)

        - Fixed a bug that may cause BR reject to restore unexpectedly. [#36053](https://github.com/pingcap/tidb/issues/36053) @[lance6716](https://github.com/lance6716)        - 

    + TiCDC

        - Fix an issue that checkpoint can not advance when replicating many tables. [#8004](https://github.com/pingcap/tiflow/issues/8004) @[asddongmen](https://github.com/asddongmen)
        - Fix the issue of transaction-atomicity and protocol can't be updated via config file. [#7935](https://github.com/pingcap/tiflow/issues/7935) @[ti-chi-bot](https://github.com/ti-chi-bot)
        (dup: release-6.5.0.md > Bug fixes> Tools> TiCDC)- Fix the issue that TiCDC mistakenly reports an error when there is a later version of TiFlash [#7744](https://github.com/pingcap/tiflow/issues/7744) @[overvenus](https://github.com/overvenus) @[ti-chi-bot](https://github.com/ti-chi-bot)
        - Fix an OOM issue when TiCDC replicates big transactions [#7913](https://github.com/pingcap/tiflow/issues/7913) @[ti-chi-bot](https://github.com/ti-chi-bot)
        - Fix the bug that context deadline was exceeded when replicating data without split big txn [#7982](https://github.com/pingcap/tiflow/issues/7982) @[asddongmen](https://github.com/asddongmen)
        (dup: release-6.4.0.md > Bug fixes> Tools> TiCDC)- Fix the issue that `sasl-password` in the `changefeed query` result is not masked [#7182](https://github.com/pingcap/tiflow/issues/7182) @[dveeden](https://github.com/dveeden) @[ti-chi-bot](https://github.com/ti-chi-bot)
        (dup: release-6.5.0.md > Bug fixes> Tools> TiCDC)- Fix the issue that data is lost when a user quickly deletes a replication task and then creates another one with the same task name [#7657](https://github.com/pingcap/tiflow/issues/7657) @[overvenus](https://github.com/overvenus) @[ti-chi-bot](https://github.com/ti-chi-bot)

    + TiDB Data Migration (DM)

        (dup: release-6.5.0.md > Bug fixes> Tools> TiDB Data Migration (DM))- Fix the issue that DM precheck is not passed when the upstream database uses regular expressions to grant privileges [#7645](https://github.com/pingcap/tiflow/issues/7645) @[lance6716](https://github.com/lance6716) @[ti-chi-bot](https://github.com/ti-chi-bot)
        - Fix a bug that when both "update" and "non-update" type expression filters are used in one table, all UPDATE row changes are skipped [#7831](https://github.com/pingcap/tiflow/issues/7831) @[ti-chi-bot](https://github.com/ti-chi-bot)
        - Fix a bug when only one of `update-old-value-expr` or `update-new-value-expr` is set for a table, it does not take effect or panic [#7774](https://github.com/pingcap/tiflow/issues/7774) @[amyangfei](https://github.com/amyangfei)
