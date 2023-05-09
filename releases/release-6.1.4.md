---
title: TiDB 6.1.4 Release Notes
summary: 了解 TiDB 6.1.4 版本的新功能、兼容性变更、改进提升，以及错误修复。
---

# TiDB 6.1.4 Release Notes

发版日期：2023 年 2 月 8 日

TiDB 版本：6.1.4

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v6.1/quick-start-with-tidb) | [生产部署](https://docs.pingcap.com/zh/tidb/v6.1/production-deployment-using-tiup) | [下载离线包](https://cn.pingcap.com/product-community/?version=v6.1.4#version-list)

## 兼容性变更

- TiDB

    - 由于可能存在正确性问题，分区表目前不再支持修改列类型 [#40620](https://github.com/pingcap/tidb/issues/40620) @[mjonss](https://github.com/mjonss)

## 提升改进

- TiFlash

    - 减少了高强度更新负载下的 TiFlash 实例的 IOPS 和写放大倍数，IOPS 最高减少 95%，写放大最高减少 65% [#6460](https://github.com/pingcap/tiflash/issues/6460) @[flowbehappy](https://github.com/flowbehappy)

- Tools

    - TiCDC

        - 增加了 DML batch 操作功能，提升了批量生成 SQL 语句场景下的吞吐 [#7653](https://github.com/pingcap/tiflow/issues/7653) @[asddongmen](https://github.com/asddongmen)
        - 支持将 redo log 存储至兼容 GCS 或 Azure 协议的对象存储 [#7987](https://github.com/pingcap/tiflow/issues/7987) @[CharlesCheung96](https://github.com/CharlesCheung96)

    - TiDB Lightning

        - 将 precheck 检查项 `clusterResourceCheckItem` 和 `emptyRegionCheckItem` 的严重级别从 `Critical` 改为 `Warning` [#37654](https://github.com/pingcap/tidb/issues/37654) @[niubell](https://github.com/niubell)

## Bug 修复

+ TiDB

    - 修复了创建表时列的默认值和列类型不一致且没有自动修正的问题 [#34881](https://github.com/pingcap/tidb/issues/34881) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger) @[mjonss](https://github.com/mjonss)
    - 修复 `LazyTxn.LockKeys` 函数中的数据争用问题 [#40355](https://github.com/pingcap/tidb/issues/40355) @[HuSharp](https://github.com/HuSharp)
    - 修复 `INSERT` 或 `REPLACE` 语句在长会话连接中执行可能造成 Panic 的问题 [#40351](https://github.com/pingcap/tidb/issues/40351) @[fanrenhoo](https://github.com/fanrenhoo)
    - 修复使用 "Cursor Read" 方式读取数据时可能因为 GC 而报错的问题 [#39447](https://github.com/pingcap/tidb/issues/39447) @[zyguan](https://github.com/zyguan)
    - 修复 [`pessimistic-auto-commit`](/tidb-configuration-file.md#pessimistic-auto-commit) 配置项对 "Point Get" 查询不生效的问题 [#39928](https://github.com/pingcap/tidb/issues/39928) @[zyguan](https://github.com/zyguan)
    - 修复查询 `INFORMATION_SCHEMA.TIKV_REGION_STATUS` 返回不正确结果的问题 [#37436](https://github.com/pingcap/tidb/issues/37436) @[zimulala](https://github.com/zimulala)
    - 修复使用 `IN` 或 `NOT IN` 的子查询在某些情况下会报错 `Can't find column` 的问题 [#37032](https://github.com/pingcap/tidb/issues/37032) @[AilinKid](https://github.com/AilinKid) @[lance6716](https://github.com/lance6716)

- PD

    - 修复 PD 可能会非预期地向 Region 添加多个 Learner 的问题 [#5786](https://github.com/tikv/pd/issues/5786) @[HunDunDM](https://github.com/HunDunDM)

+ TiKV

    - 修复 Gitpod 环境中存在多个 `cgroup` 和 `mountinfo` 时 TiDB 启动异常的问题 [#13660](https://github.com/tikv/tikv/issues/13660) @[tabokie](https://github.com/tabokie)
    - 修复 tikv-ctl 执行 `reset-to-version` 命令时被终止的问题 [#13829](https://github.com/tikv/tikv/issues/13829) @[tabokie](https://github.com/tabokie)
    - 修复误报 `PessimisticLockNotFound` 的问题 [#13425](https://github.com/tikv/tikv/issues/13425) @[sticnarf](https://github.com/sticnarf)
    - 修复单次写入超过 2 GiB 时 TiKV panic 的问题 [#13848](https://github.com/tikv/tikv/issues/13848) @[YuJuncen](https://github.com/YuJuncen)
    - 修复 TiDB 中事务在执行悲观 DML 失败后，再执行其他 DML 时，如果 TiDB 和 TiKV 之间存在网络故障，可能会造成数据不一致的问题 [#14038](https://github.com/tikv/tikv/issues/14038) @[MyonKeminta](https://github.com/MyonKeminta)
    - 修复当未启用 new collation 时 `LIKE` 操作符中的 `_` 无法匹配非 ASCII 字符的问题 [#13769](https://github.com/tikv/tikv/issues/13769) @[YangKeao](https://github.com/YangKeao)

+ TiFlash

    - 修复小概率情况下出现的 TiFlash 全局锁被长时间阻塞的问题 [#6418](https://github.com/pingcap/tiflash/issues/6418) @[SeaRise](https://github.com/SeaRise)
    - 修复高更新负载可能导致 OOM 的问题 [#6407](https://github.com/pingcap/tiflash/issues/6407) @[JaySon-Huang](https://github.com/JaySon-Huang)

+ Tools

    + Backup & Restore (BR)

        - 修复在某些情况下因无法获取 Region 大小导致恢复失败的问题 [#36053](https://github.com/pingcap/tidb/issues/36053) @[YuJuncen](https://github.com/YuJuncen)
        - 修复使用 `br debug` 命令解析 backupmeta 文件导致的 panic 的问题 [#40878](https://github.com/pingcap/tidb/issues/40878) @[MoCuishle28](https://github.com/MoCuishle28)

    + TiCDC

        - 修复在同步大量表时 checkpoint 不推进问题 [#8004](https://github.com/pingcap/tiflow/issues/8004) @[asddongmen](https://github.com/asddongmen)
        - 修复不能通过配置文件修改 `transaction_atomicity` 和 `protocol` 参数的问题 [#7935](https://github.com/pingcap/tiflow/issues/7935) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - 修复当 TiFlash 的版本高于 TiCDC 时，TiCDC 会误报错的问题 [#7744](https://github.com/pingcap/tiflow/issues/7744) @[overvenus](https://github.com/overvenus)
        - 修复同步大事务时会出现 OOM 的问题 [#7913](https://github.com/pingcap/tiflow/issues/7913) @[overvenus](https://github.com/overvenus)
        - 修复没有配置大事务拆分时，同步数据超过 context deadline 的问题 [#7982](https://github.com/pingcap/tiflow/issues/7982) @[hi-rustin](https://github.com/hi-rustin)
        - 修复 `changefeed query` 的输出中 `sasl-password` 显示为明文的问题 [#7182](https://github.com/pingcap/tiflow/issues/7182) @[dveeden](https://github.com/dveeden)
        - 修复用户快速删除、创建同名同步任务可能导致的数据丢失问题 [#7657](https://github.com/pingcap/tiflow/issues/7657) @[overvenus](https://github.com/overvenus)

    + TiDB Data Migration (DM)

        - 修复当 `SHOW GRANTS` 结果中的下游数据库名包含通配符 `*` 时 precheck 报错的问题 [#7645](https://github.com/pingcap/tiflow/issues/7645) @[lance6716](https://github.com/lance6716)
        - 修复当 binlog 中 query event 为 COMMIT 时 DM 打印过多日志的问题 [#7525](https://github.com/pingcap/tiflow/issues/7525) @[liumengya94](https://github.com/liumengya94)
        - 修复当 SSL 参数仅指定 `ssl-ca` 时 DM 任务无法启动的问题 [#7941](https://github.com/pingcap/tiflow/issues/7941) @[liumengya94](https://github.com/liumengya94)
        - 修复当在某个表上同时指定 `UPDATE` 和非 `UPDATE` 类型的表达式过滤规则 `expression-filter` 时，所有 `UPDATE` 操作被跳过的问题 [#7831](https://github.com/pingcap/tiflow/issues/7831) @[lance6716](https://github.com/lance6716)
        - 修复当某个表上仅指定 `update-old-value-expr` 或 `update-new-value-expr` 时，过滤规则不生效或 DM 发生 panic 的问题 [#7774](https://github.com/pingcap/tiflow/issues/7774) @[lance6716](https://github.com/lance6716)

    + TiDB Lightning

        - 修复 TiDB Lightning 导入巨大数据源文件时的内存泄漏问题 [#39331](https://github.com/pingcap/tidb/issues/39331) @[dsdashun](https://github.com/dsdashun)
        - 修复 precheck 检查项有时无法监测到之前的导入失败遗留的脏数据的问题 [#39477](https://github.com/pingcap/tidb/issues/39477) @[dsdashun](https://github.com/dsdashun)
