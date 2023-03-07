---
title: TiDB 6.5.1 Release Notes
summary: 了解 TiDB 6.5.1 版本的兼容性变更、改进提升，以及错误修复。
---

# TiDB 6.5.1 Release Notes

发版日期：2023 年 1 月 xx 日

TiDB 版本：6.5.1

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v6.5/quick-start-with-tidb) | [生产部署](https://docs.pingcap.com/zh/tidb/v6.5/production-deployment-using-tiup) | [下载离线包](https://cn.pingcap.com/product-community/?version=v6.5.1#version-list)

## 兼容性变更

- 自 2023 年 2 月 20 日起，新发布的 TiDB 和 TiDB Dashboard 版本（包含 6.5.1），默认关闭[遥测功能](/telemetry.md)，即默认不再收集使用情况信息分享给 PingCAP。如果升级至这些版本前使用默认的遥测配置，则升级后遥测功能处于关闭状态。具体的版本可参考 [TiDB 版本发布时间线](/releases/release-timeline.md)。

    - 系统变量 [`tidb_enable_telemetry`](/system-variables.md#tidb_enable_telemetry-从-v402-版本开始引入) 默认值由 `ON` 修改为 `OFF`。
    - TiDB 配置项 [`enable-telemetry`](/tidb-configuration-file.md#enable-telemetry-从-v402-版本开始引入) 默认值由 `true` 改为 `false`。
    - PD 配置项 [`enable-telemetry`](/pd-configuration-file.md#enable-telemetry) 默认值由 `true` 改为 `false`。

- 从 v1.11.3 起，新部署的 TiUP 默认关闭遥测功能，即默认不再收集使用情况信息。如果从 v1.11.3 之前的 TiUP 版本升级至 v1.11.3 或更高 TiUP 版本，遥测保持升级前的开启或关闭状态。

- (dup): release-6.1.4.md > 兼容性变更> TiDB - 由于可能存在正确性问题，分区表目前不再支持修改列类型 [#40620](https://github.com/pingcap/tidb/issues/40620) @[mjonss](https://github.com/mjonss)

## 改进提升

+ TiDB

    - (dup): release-6.6.0.md > - 支持指定集群初次启动时的初始化 SQL 脚本 [#35624](https://github.com/pingcap/tidb/issues/35624) @[morgo](https://github.com/morgo)

        TiDB 集群初次启动时，可通过命令行参数 `--initialize-sql-file` 指定执行的 SQL 脚本。该功能可用于修改系统变量的值、创建用户或分配权限等。更多信息，请参考[用户文档](/tidb-configuration-file.md#initialize-sql-file-从-v660-版本开始引入)。

    - (dup): release-6.6.0.md > 改进提升> TiDB - 定期清理过期的 Region 缓存，避免内存泄漏和性能下降问题 [#40461](https://github.com/pingcap/tidb/issues/40461) @[sticnarf](https://github.com/sticnarf)
    - 添加 `-proxy protocol fallbackable` 选项，让 TiDB 可以处理客户端 IP 在 proxy 协议允许的 IP 列表中的原始连接。[#41409](https://github.com/pingcap/tidb/issues/41409) @[blacktear23](https://github.com/blacktear23)
    - 改进了 memory tracker 的准确度 [#40900](https://github.com/pingcap/tidb/issues/40900) [#40500](https://github.com/pingcap/tidb/issues/40500) @[wshwsh12](https://github.com/wshwsh12)
    - note [#issue](链接) @[贡献者 GitHub ID](链接) https://github.com/pingcap/tidb/issues/40900

+ TiKV

    - (dup): release-6.6.0.md > 改进提升> TiKV - 支持在小于 1 core 的 CPU 下启动 TiKV [#13586](https://github.com/tikv/tikv/issues/13586) [#13752](https://github.com/tikv/tikv/issues/13752) [#14017](https://github.com/tikv/tikv/issues/14017) @[andreid-db](https://github.com/andreid-db)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ PD

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ TiFlash

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ Tools

    + Backup & Restore (BR)

        - (dup): release-6.6.0.md > 改进提升> Tools> Backup & Restore (BR) - 优化 TiKV 端下载日志备份文件的并发度，提升常规场景下 PITR 恢复的性能 [#14206](https://github.com/tikv/tikv/issues/14206) @[YuJuncen](https://github.com/YuJuncen)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiCDC

        - (dup): release-6.6.0.md > 改进提升> Tools> TiCDC - 支持 Batch UPDATE DML 语句，提升 TiCDC 的同步性能 [#8084](https://github.com/pingcap/tiflow/issues/8084) @[amyangfei](https://github.com/amyangfei)
        - (dup): release-6.1.4.md > 提升改进> Tools> TiCDC - 支持将 redo log 存储至兼容 GCS 或 Azure 协议的对象存储 [#7987](https://github.com/pingcap/tiflow/issues/7987) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - (dup): release-6.6.0.md > 改进提升> Tools> TiCDC - 采用异步模式实现 MQ sink 和 MySQL sink，提升 sink 的吞吐能力 [#5928](https://github.com/pingcap/tiflow/issues/5928) @[hicqu](https://github.com/hicqu) @[hi-rustin](https://github.com/hi-rustin)

    + TiDB Data Migration (DM)

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiDB Lightning

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiUP

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

## 错误修复

+ TiDB

    - (dup): release-6.1.4.md > Bug 修复> TiDB - 修复 [`pessimistic-auto-commit`](/tidb-configuration-file.md#pessimistic-auto-commit) 配置项对 "Point Get" 查询不生效的问题 [#39928](https://github.com/pingcap/tidb/issues/39928) @[zyguan](https://github.com/zyguan)
    - (dup): release-6.1.4.md > Bug 修复> TiDB - 修复 `INSERT` 或 `REPLACE` 语句在长会话连接中执行可能造成 Panic 的问题 [#40351](https://github.com/pingcap/tidb/issues/40351) @[fanrenhoo](https://github.com/fanrenhoo)
    - (dup): release-6.1.4.md > Bug 修复> TiDB - 修复 `LazyTxn.LockKeys` 函数中的数据争用问题 [#40355](https://github.com/pingcap/tidb/issues/40355) @[HuSharp](https://github.com/HuSharp)
    - (dup): release-6.6.0.md > 错误修复> TiDB - 修复了 `auto analyze` 导致 graceful shutdown 耗时长的问题 [#40038](https://github.com/pingcap/tidb/issues/40038) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes)
    - (dup): release-6.6.0.md > 错误修复> TiDB - 修复了 DDL 在 ingest 过程中可能会发生数据竞争的问题 [#40970](https://github.com/pingcap/tidb/issues/40970) @[tangenta](https://github.com/tangenta)
    - (dup): release-6.6.0.md > 错误修复> TiDB - 修复了 ingest 模式下创建唯一索引可能会导致数据和索引不一致的问题 [#40464](https://github.com/pingcap/tidb/issues/40464) @[tangenta](https://github.com/tangenta)
    - (dup): release-6.6.0.md > 错误修复> TiDB - 修复了 TiDB 在初始化时有可能死锁的问题 [#40408](https://github.com/pingcap/tidb/issues/40408) @[Defined2014](https://github.com/Defined2014)
    - (dup): release-6.6.0.md > 错误修复> TiDB - 修复了 TiDB 构造 key 范围时对 `NULL` 值处理不当，导致读取非预期数据的问题 [#40158](https://github.com/pingcap/tidb/issues/40158) @[tiancaiamao](https://github.com/tiancaiamao)
    - (dup): release-6.6.0.md > 错误修复> TiDB - 修复了内存重用导致的在某些情况下系统变量的值会被错误修改的问题 [#40979](https://github.com/pingcap/tidb/issues/40979) @[lcwangchao](https://github.com/lcwangchao)
    - (dup): release-6.6.0.md > 错误修复> TiDB - 修复了在执行 TTL 任务时，如果表的主键包含 `ENUM` 类型的列任务会失败的问题 [#40456](https://github.com/pingcap/tidb/issues/40456) @[lcwangchao](https://github.com/lcwangchao)
    - (dup): release-6.6.0.md > 错误修复> TiDB - 修复了在添加唯一索引时有可能会 panic 的问题 [#40592](https://github.com/pingcap/tidb/issues/40592) @[tangenta](https://github.com/tangenta)
    - (dup): release-6.6.0.md > 错误修复> TiDB - 修复了并发 truncate 同一张表时，部分 truncate 操作无法被 MDL 阻塞的问题 [#40484](https://github.com/pingcap/tidb/issues/40484) @[wjhuang2016](https://github.com/wjhuang2016)
    - (dup): release-6.6.0.md > 错误修复> TiDB - 修复了当动态裁剪模式下的分区表有 global binding 时，TiDB 重启失败的问题 [#40368](https://github.com/pingcap/tidb/issues/40368) @[Yisaer](https://github.com/Yisaer)
    - (dup): release-6.6.0.md > 错误修复> TiDB - 修复了某些情况下唯一索引仍然可能产生重复数据的问题 [#40217](https://github.com/pingcap/tidb/issues/40217) @[tangenta](https://github.com/tangenta)
    - (dup): release-6.6.0.md > 错误修复> TiDB - 修复了添加索引时可能导致数据竞争的问题 [#40879](https://github.com/pingcap/tidb/issues/40879) @[tangenta](https://github.com/tangenta)
    - (dup): release-6.6.0.md > 错误修复> TiDB - 修复了表 Region 比较多时因 Region 缓存失效导致加索引效率低下的问题 [#38436](https://github.com/pingcap/tidb/issues/38436) @[tangenta](https://github.com/tangenta)
    - (dup): release-6.1.4.md > Bug 修复> TiDB - 修复使用 "Cursor Read" 方式读取数据时可能因为 GC 而报错的问题 [#39447](https://github.com/pingcap/tidb/issues/39447) @[zyguan](https://github.com/zyguan)
    - 修复“show processlist”信息中未显示“execute”语句的问题 [#41156](https://github.com/pingcap/tidb/issues/41156) @[YangKeao](https://github.com/YangKeao)
    - 修复了 `globalMemoryControl ` 在 kill query 时可能会遇上 kill 不结束的问题 [#41057](https://github.com/pingcap/tidb/issues/41057) @[wshwsh12](https://github.com/wshwsh12)
    - 修复了 `indexMerge` 遇到错误之后可能会导致 TiDB crash 的问题 [#41047](https://github.com/pingcap/tidb/issues/41047) [#40877](https://github.com/pingcap/tidb/issues/40877) @[guo-shaoge](https://github.com/guo-shaoge) @[windtalker](https://github.com/windtalker)
    - 修复 `analyze` 语句可能会被 kill 的问题 [#41825](https://github.com/pingcap/tidb/issues/41825) @[XuHuaiyu](https://github.com/XuHuaiyu)
    - 修复了 `indexMerge` 中可能会出现 goroutine 泄露的问题 [#41545](https://github.com/pingcap/tidb/issues/41545) [#41605](https://github.com/pingcap/tidb/issues/41605) @[guo-shaoge](https://github.com/guo-shaoge)
    - 修复了 `unsigned tinyint/smallint/int` 和小于 0 的 `decimal/float/double` 比较时结果可能出错的问题 [#41736](https://github.com/pingcap/tidb/issues/41736) @[LittleFall](https://github.com/LittleFall)
    - 修复了开启 `tidb_enable_reuse_chunk` 后可能会 memory leak 的问题 [#40987](https://github.com/pingcap/tidb/issues/40987) @[guo-shaoge](https://github.com/guo-shaoge)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ TiKV

    - (dup): release-6.6.0.md > 错误修复> TiKV - 修复 Resolved TS 导致网络流量升高的问题 [#14092](https://github.com/tikv/tikv/issues/14092) @[overvenus](https://github.com/overvenus)
    - (dup): release-6.1.4.md > Bug 修复> TiKV - 修复 TiDB 中事务在执行悲观 DML 失败后，再执行其他 DML 时，如果 TiDB 和 TiKV 之间存在网络故障，可能会造成数据不一致的问题 [#14038](https://github.com/tikv/tikv/issues/14038) @[MyonKeminta](https://github.com/MyonKeminta)
    - (dup): release-6.6.0.md > 错误修复> TiKV - 修复转换 `const Enum` 类型到其他类型时报错的问题 [#14156](https://github.com/tikv/tikv/issues/14156) @[wshwsh12](https://github.com/wshwsh12)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ PD

    - (dup): release-6.6.0.md > 错误修复> PD - 修复 `replace-down-peer` 在特定条件下执行变慢的问题 [#5788](https://github.com/tikv/pd/issues/5788) @[HundunDM](https://github.com/HunDunDM)
    - (dup): release-6.1.4.md > Bug 修复> PD - 修复 PD 可能会非预期地向 Region 添加多个 Learner 的问题 [#5786](https://github.com/tikv/pd/issues/5786) @[HunDunDM](https://github.com/HunDunDM)
    - (dup): release-6.6.0.md > 错误修复> PD - 修复 Region Scatter 任务会生成非预期的多余副本的问题 [#5909](https://github.com/tikv/pd/issues/5909) @[HundunDM](https://github.com/HunDunDM)
    - (dup): release-6.1.5.md > Bug 修复> PD - 修复调用 `ReportMinResolvedTS` 过于频繁导致 PD OOM 的问题 [#5965](https://github.com/tikv/pd/issues/5965) @[HundunDM](https://github.com/HunDunDM)	
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ TiFlash

    - (dup): release-6.6.0.md > 错误修复> TiFlash - 修复半连接在计算笛卡尔积时，使用内存过量的问题 [#6730](https://github.com/pingcap/tiflash/issues/6730) @[gengliqi](https://github.com/gengliqi)
    - 修复 TiFlash 配置不支持 ipv6 的问题 (https://github.com/pingcap/tiflash/issues/6734) @[ywqzzy](https://github.com/ywqzzy)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ Tools

    + Backup & Restore (BR)

        - (dup): release-6.6.0.md > 错误修复> Tools> Backup & Restore (BR) - 修复 PD 与 TiDB server 的连接故障导致 PITR 备份进度不推进的问题 [#41082](https://github.com/pingcap/tidb/issues/41082) @[YuJuncen](https://github.com/YuJuncen)
        - (dup): release-6.6.0.md > 错误修复> Tools> Backup & Restore (BR) - 修复 PD 与 TiKV 的连接故障导致 TiKV 不能监听 PITR 任务的问题 [#14159](https://github.com/tikv/tikv/issues/14159) @[YuJuncen](https://github.com/YuJuncen)
        - (dup): release-6.6.0.md > 错误修复> Tools> Backup & Restore (BR) - 修复 PITR 不支持 PD 集群配置变更的问题 [#14165](https://github.com/tikv/tikv/issues/14165) @[YuJuncen](https://github.com/YuJuncen)
        - (dup): release-6.6.0.md > 错误修复> Tools> Backup & Restore (BR) - 修复 PITR 功能不支持 CA-bundle 认证的问题 [#38775](https://github.com/pingcap/tidb/issues/38775) @[YuJuncen](https://github.com/YuJuncen)
        - (dup): release-6.6.0.md > 错误修复> Tools> Backup & Restore (BR) - 修复 PITR 备份任务被删除时，存在备份信息残留导致新任务出现数据不一致的问题 [#40403](https://github.com/pingcap/tidb/issues/40403) @[joccau](https://github.com/joccau)
        - (dup): release-6.1.4.md > Bug 修复> Tools> Backup & Restore (BR) - 修复使用 `br debug` 命令解析 backupmeta 文件导致的 panic 的问题 [#40878](https://github.com/pingcap/tidb/issues/40878) @[MoCuishle28](https://github.com/MoCuishle28)
        - (dup): release-6.1.4.md > Bug 修复> Tools> Backup & Restore (BR) - 修复在某些情况下因无法获取 Region 大小导致恢复失败的问题 [#36053](https://github.com/pingcap/tidb/issues/36053) @[YuJuncen](https://github.com/YuJuncen)
        - (dup): release-6.6.0.md > 错误修复> Tools> Backup & Restore (BR) - 修复当 TiDB 集群不存在 PITR 备份任务时，`resolve lock` 频率过高的问题 [#40759](https://github.com/pingcap/tidb/issues/40759) @[joccau](https://github.com/joccau)
        - (dup): release-6.6.0.md > 错误修复> Tools> Backup & Restore (BR) - 修复恢复数据到正在运行日志备份的集群，导致日志备份文件无法恢复的问题 [#40797](https://github.com/pingcap/tidb/issues/40797) @[Leavrth](https://github.com/Leavrth)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiCDC

        - (dup): release-6.6.0.md > 错误修复> Tools> TiCDC - 优化 pull-based sink 打开时 TiCDC 在 CPU 利用率、内存控制、吞吐等方面若干性能问题 [#8142](https://github.com/pingcap/tiflow/issues/8142) [#8157](https://github.com/pingcap/tiflow/issues/8157) [#8001](https://github.com/pingcap/tiflow/issues/8001) [#5928](https://github.com/pingcap/tiflow/issues/5928) @[hicqu](https://github.com/hicqu) @[hi-rustin](https://github.com/hi-rustin)
        - (dup): release-6.6.0.md > 错误修复> Tools> TiCDC - 修复 changefeed 在 TiKV、TiCDC 节点扩缩容等特殊场景下卡住的问题 [#8174](https://github.com/pingcap/tiflow/issues/8174) @[hicqu](https://github.com/hicqu)
        - (dup): release-6.6.0.md > 错误修复> Tools> TiCDC - 修复 redo log 存储路径没做权限预检查的问题 [#6335](https://github.com/pingcap/tiflow/issues/6335) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - (dup): release-6.6.0.md > 错误修复> Tools> TiCDC - 修复 redo log 容忍 S3 存储故障的时间过短的问题 [#8089](https://github.com/pingcap/tiflow/issues/8089) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - (dup): release-6.1.4.md > Bug 修复> Tools> TiCDC - 修复不能通过配置文件修改 `transaction_atomicity` 和 `protocol` 参数的问题 [#7935](https://github.com/pingcap/tiflow/issues/7935) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - (dup): release-6.1.4.md > Bug 修复> Tools> TiCDC - 修复在同步大量表时 checkpoint 不推进问题 [#8004](https://github.com/pingcap/tiflow/issues/8004) @[asddongmen](https://github.com/asddongmen)		
        - (dup): release-6.1.5.md > Bug 修复> Tools> TiCDC - 修复当同步的延迟过大时 apply redo log 可能会出现 OOM 的问题 [#8085](https://github.com/pingcap/tiflow/issues/8085) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - (dup): release-6.1.5.md > Bug 修复> Tools> TiCDC - 修复当开启 redo log 写 meta 时性能下降的问题 [#8074](https://github.com/pingcap/tiflow/issues/8074) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - (dup): release-6.1.4.md > Bug 修复> Tools> TiCDC - 修复没有配置大事务拆分时，同步数据超过 context deadline 的问题 [#7982](https://github.com/pingcap/tiflow/issues/7982) @[hi-rustin](https://github.com/hi-rustin)
        - 默认打开 pull-based sink 功能提升系统的吞吐 [#8232](https://github.com/pingcap/tiflow/issues/8232) @[hi-rustin](https://github.com/hi-rustin)
        - 修复在PD 异常时，暂停一个 changefeed 会错误设置状态的问题 [#8330](https://github.com/pingcap/tiflow/issues/8330) @[sdojjy](https://github.com/sdojjy)
        - 修复下游为 tidb/mysql ，无主键且非空唯一索引所在列指定了 CHARACTER SET 同步时可能会出现数据不一致的问题。[#8420](https://github.com/pingcap/tiflow/issues/8420) @[asddongmen](https://github.com/asddongmen)

    + TiDB Data Migration (DM)

        - (dup): release-6.1.5.md > Bug 修复> Tools> TiDB Data Migration (DM) - 修复 `binlog-schema delete` 命令执行失败的问题 [#7373](https://github.com/pingcap/tiflow/issues/7373) @[liumengya94](https://github.com/liumengya94)
        - (dup): release-6.1.5.md > Bug 修复> Tools> TiDB Data Migration (DM) - 修复当最后一个 binlog 是被 skip 的 DDL 时，checkpoint 不推进的问题 [#8175](https://github.com/pingcap/tiflow/issues/8175) @[D3Hunter](https://github.com/D3Hunter)
        - (dup): release-6.1.4.md > Bug 修复> Tools> TiDB Data Migration (DM) - 修复当在某个表上同时指定 `UPDATE` 和非 `UPDATE` 类型的表达式过滤规则 `expression-filter` 时，所有 `UPDATE` 操作被跳过的问题 [#7831](https://github.com/pingcap/tiflow/issues/7831) @[lance6716](https://github.com/lance6716)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiDB Lightning

        - (dup): release-6.1.4.md > Bug 修复> Tools> TiDB Lightning - 修复 precheck 检查项有时无法监测到之前的导入失败遗留的脏数据的问题 [#39477](https://github.com/pingcap/tidb/issues/39477) @[dsdashun](https://github.com/dsdashun)
        - (dup): release-6.6.0.md > 错误修复> Tools> TiDB Lightning - 修复 TiDB Lightning 在 split-region 阶段发生 panic 的问题 [#40934](https://github.com/pingcap/tidb/issues/40934) @[lance6716](https://github.com/lance6716)
        - (dup): release-6.6.0.md > 错误修复> Tools> TiDB Lightning - 修复冲突处理逻辑 (`duplicate-resolution`) 可能导致 checksum 不一致的问题 [#40657](https://github.com/pingcap/tidb/issues/40657) @[gozssky](https://github.com/gozssky)
        - (dup): release-6.6.0.md > 错误修复> Tools> TiDB Lightning - 修复在并行导入时，当除最后一个 TiDB Lightning 实例外的其他实例都遇到本地重复记录时，TiDB Lightning 可能会错误地跳过冲突处理的问题 [#40923](https://github.com/pingcap/tidb/issues/40923) @[lichunzhu](https://github.com/lichunzhu)	
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiUP

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)