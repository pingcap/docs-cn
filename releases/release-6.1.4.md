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

    - 降低了在高强度的更新负载下的 IOPS 和写放大 [#6460](https://github.com/pingcap/tiflash/issues/6460) @[flowbehappy](https://github.com/flowbehappy)

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

    - Fix data race in the LazyTxn.LockKeys [#40355](https://github.com/pingcap/tidb/issues/40355) @[HuSharp](https://github.com/HuSharp)
    - Fix the case that INSERT/REPLACE might panic in a long session connection [#40351](https://github.com/pingcap/tidb/issues/40351) @[fanrenhoo](https://github.com/fanrenhoo)
    - Fix the issue that hcursor read being canceled by GC [#39447](https://github.com/pingcap/tidb/issues/39447)@[zyguan](https://github.com/zyguan)
    - Fix the issue that the pessimistic autocommit configuration does not work for point get plans [#39928](https://github.com/pingcap/tidb/issues/39928)@[zyguan](https://github.com/zyguan)

    sql-infra
    
    - Block modify column of partitioned table, even if it was not changing data when put into the DDL queue. [#40620](https://github.com/pingcap/tidb/issues/40620) @[mjonss](https://github.com/mjonss)
    - 

    planner

    (dup: release-6.3.0.md > Bug fixes> TiDB> Fix the issue that querying `INFORMATION_SCHEMA.TIKV_REGION_STATUS` returns an incorrect result @[zimulala](https://github.com/zimulala))- Fix the issue that the `IN` and `NOT IN` subqueries in some patterns report the `Can't find column` error [#37032](https://github.com/pingcap/tidb/issues/37032) @[AilinKid](https://github.com/AilinKid) @[lance6716](https://github.com/lance6716)

- PD

    - Fix an issue that PD may repeatedly add Learner to a Region. [#5786](https://github.com/tikv/pd/issues/5786) @[HunDunDM](https://github.com/HunDunDM) 

+ TiKV

    - 修复 Gitpod 环境中存在多个 `cgroup` 和 `mountinfo` 时 TiDB 启动异常的问题 [#13660](https://github.com/tikv/tikv/issues/13660) @[tabokie](https://github.com/tabokie)
    - 修复 tikv-ctl 执行 `reset-to-version` 命令时异常终止的问题 [#13829](https://github.com/tikv/tikv/issues/13829) @[tabokie](https://github.com/tabokie)
    - 修复误报 `PessimisticLockNotFound` 的问题 [#13425](https://github.com/tikv/tikv/issues/13425) @[sticnarf](https://github.com/sticnarf)
    - 修复单次写入超过 2GiB 时会发生 panic 的问题。[#13848](https://github.com/tikv/tikv/issues/13848) @[YuJuncen](https://github.com/YuJuncen)
    - 修复了悲观事务内，当 TiDB 和 TiKV 间存在网络问题时，执行语句出错后可能出现的数据一致性问题。 [#14038](https://github.com/tikv/tikv/issues/14038) @[MyonKeminta](https://github.com/MyonKeminta)
    - 修复当未启用 new collation 时 `LIKE` 操作符中的 `_` 无法匹配非 ASCII 字符的问题 [#13769](https://github.com/tikv/tikv/issues/13769) @[YangKeao](https://github.com/YangKeao)

+ TiFlash

    - 修复小概率情况下出现的 tiflash 全局锁长时间阻塞的问题 [#6418](https://github.com/pingcap/tiflash/issues/6418) @[SeaRise](https://github.com/SeaRise)
    - 修复一个在高更新负载下会可能导致 OOM 的问题 [#6407](https://github.com/pingcap/tiflash/issues/6407) @[JaySon-Huang](https://github.com/JaySon-Huang)

+ Tools

    + Backup & Restore (BR)

        - 修复在某些情况下因无法获取 region size 导致恢复失败的问题. [#36053](https://github.com/pingcap/tidb/issues/36053) @[YuJuncen](https://github.com/YuJuncen)
        - 修复使用 br debug 命令解析 backupmeta 文件 panic 的问题.[#40878](https://github.com/pingcap/tidb/issues/40878) @[MoCuishle28](https://github.com/MoCuishle28)

    + TiCDC

        - Fix an issue that checkpoint can not advance when replicating many tables. [#8004](https://github.com/pingcap/tiflow/issues/8004) @[asddongmen](https://github.com/asddongmen)
        - Fix the issue of transaction-atomicity and protocol can't be updated via config file. [#7935](https://github.com/pingcap/tiflow/issues/7935) @[CharlesCheung96](https://github.com/CharlesCheung96)        ```
        (dup: release-6.5.0.md > Bug fixes> Tools> TiCDC)- Fix the issue that TiCDC mistakenly reports an error when there is a later version of TiFlash [#7744](https://github.com/pingcap/tiflow/issues/7744) @[overvenus](https://github.com/overvenus)
        - Fix an OOM issue when TiCDC replicates big transactions [#7913](https://github.com/pingcap/tiflow/issues/7913)
        - Fix the bug that context deadline was exceeded when replicating data without split big txn [#7982](https://github.com/pingcap/tiflow/issues/7982) @[asddongmen](https://github.com/asddongmen)
        (dup: release-6.4.0.md > Bug fixes> Tools> TiCDC)- Fix the issue that `sasl-password` in the `changefeed query` result is not masked [#7182](https://github.com/pingcap/tiflow/issues/7182) @[dveeden](https://github.com/dveeden)
        (dup: release-6.5.0.md > Bug fixes> Tools> TiCDC)- Fix the issue that data is lost when a user quickly deletes a replication task and then creates another one with the same task name [#7657](https://github.com/pingcap/tiflow/issues/7657) @[overvenus](https://github.com/overvenus) 

    + TiDB Data Migration (DM)

        - 修复当 SHOW GRANTS 结果的数据库名包含"*"时导致 precheck 报错的问题 [#7645](https://github.com/pingcap/tiflow/issues/7645) @[lance6716]
        - 修复 DM 因 binlog 中 query event 为 COMMIT 时打印过多日志的问题 [#7525](https://github.com/pingcap/tiflow/issues/7525) @[liumengya94]
        - 修复当 SSL 参数仅指定 "ssl-ca" 时 DM 任务无法启动的问题 [#7941](https://github.com/pingcap/tiflow/issues/7941) @[liumengya94]
        - 修复当在某个表上同时指定 "update" 和 "non-update" 类型的 expression filters 时, 导致所有 UPDATE 被跳过的问题 [#7831](https://github.com/pingcap/tiflow/issues/7831) @[lance6716]
        - 修复当某个表上仅指定 `update-old-value-expr` 或 `update-new-value-expr` 时不生效或导致 panic 的问题 [#7774](https://github.com/pingcap/tiflow/issues/7774) @[lance6716]
