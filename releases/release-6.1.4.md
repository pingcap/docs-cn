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

    - Fix the issue that the default value might be wrong when sql is not normative. [#34881](https://github.com/pingcap/tidb/issues/34881) @[mjonss](https://github.com/mjonss)

    transaction

    - session: fix data race in the LazyTxn.LockKeys [#40355](https://github.com/pingcap/tidb/issues/40355) @[HuSharp](https://github.com/HuSharp)
    - Fix the case that INSERT/REPLACE might panic in a long session connection [#40351](https://github.com/pingcap/tidb/issues/40351) @[fanrenhoo](https://github.com/fanrenhoo)

    sql-infra
    
    - Block modify column of partitioned table, even if it was not changing data when put into the DDL queue. [#40620](https://github.com/pingcap/tidb/issues/40620) @[ti-chi-bot](https://github.com/ti-chi-bot)
    - 

    planner

    - Make the both side operand of NAAJ & refuse partial column substitute in projection elimination [#37032](https://github.com/pingcap/tidb/issues/37032) @[lance6716](https://github.com/lance6716)    - 

- PD

    - Fix an issue that PD may repeatedly add Learner to a Region. [#5786](https://github.com/tikv/pd/issues/5786) @[ti-chi-bot](https://github.com/ti-chi-bot)    - 

+ TiKV

    - Fix panic when there are multiple cgroup2 mountinfos [#13660](https://github.com/tikv/tikv/issues/13660) @[ti-srebot](https://github.com/ti-srebot)
    - Fix a segfault when executing reset-to-version with tikv-ctl [#13829](https://github.com/tikv/tikv/issues/13829) @[ti-chi-bot](https://github.com/ti-chi-bot)
    - Fixed a problem that when a transaction in TiDB fails to execute a pessimistic DML and then executes another DML, if there are random network failures between TiDB and TiKV, it has risk to cause data inconsistency. [#40114](https://github.com/pingcap/tidb/issues/40114) @[ti-chi-bot](https://github.com/ti-chi-bot)
    - Fix panic when the size of one single write exceeds 2GiB. [#13848](https://github.com/tikv/tikv/issues/13848) @[YuJuncen](https://github.com/YuJuncen)
    - Reduce false-positive PessimisticLockNotFound errors in conflicting auto-commit workloads. [#13425](https://github.com/tikv/tikv/issues/13425) @[ti-srebot](https://github.com/ti-srebot)
    - Fixed a problem that when a transaction in TiDB fails to execute a pessimistic DML and then executes another DML, if there are random network failures between TiDB and TiKV, it has risk to cause data inconsistency. [#14038](https://github.com/tikv/tikv/issues/14038) @[ti-chi-bot](https://github.com/ti-chi-bot)
    - Fix the issue that `_` pattern in `like` failed to handle non-ascii character without new collation enabled. [#13769](https://github.com/tikv/tikv/issues/13769) @[tonyxuqqi](https://github.com/tonyxuqqi)

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
        - Fix the issue that TiCDC mistakenly reports error where there is a higher version TiFlash [#7744](https://github.com/pingcap/tiflow/issues/7744) @[ti-chi-bot](https://github.com/ti-chi-bot)
        - Fix an OOM issue when TiCDC replicates big transactions [#7913](https://github.com/pingcap/tiflow/issues/7913) @[ti-chi-bot](https://github.com/ti-chi-bot)
        - Fix the bug that context deadline was exceeded when replicating data without split big txn [#7982](https://github.com/pingcap/tiflow/issues/7982) @[asddongmen](https://github.com/asddongmen)
        - The `sasl-password` in the `sink-uri` is masked in the `changefeed query` output [#7182](https://github.com/pingcap/tiflow/issues/7182) @[ti-chi-bot](https://github.com/ti-chi-bot)
        - Add recreating changefeed peace period (30s) after a changefeed is removed. [#7657](https://github.com/pingcap/tiflow/issues/7657) @[ti-chi-bot](https://github.com/ti-chi-bot)

    + TiDB Data Migration (DM)

        - Fix a bug that DM may raise error at prechecking when downstream database name in SHOW GRANTS contains wildcard [#7645](https://github.com/pingcap/tiflow/issues/7645) @[ti-chi-bot](https://github.com/ti-chi-bot)
        - Fix a bug that when both "update" and "non-update" type expression filters are used in one table, all UPDATE row changes are skipped [#7831](https://github.com/pingcap/tiflow/issues/7831) @[ti-chi-bot](https://github.com/ti-chi-bot)
        - Fix a bug when only one of `update-old-value-expr` or `update-new-value-expr` is set for a table, it does not take effect or panic [#7774](https://github.com/pingcap/tiflow/issues/7774) @[amyangfei](https://github.com/amyangfei)
