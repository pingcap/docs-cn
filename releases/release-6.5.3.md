---
title: TiDB 6.5.3 Release Notes
summary: 了解 TiDB 6.5.3 版本的兼容性变更、改进提升，以及错误修复。
---

# TiDB 6.5.3 Release Notes

发版日期：2023 年 6 月 14 日

TiDB 版本：6.5.3

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v6.5/quick-start-with-tidb) | [生产部署](https://docs.pingcap.com/zh/tidb/v6.5/production-deployment-using-tiup) | [下载离线包](https://cn.pingcap.com/product-community/?version=v6.5.3#version-list)

## 兼容性变更

### 行为变更

- TiCDC 在处理 Update 事件时，如果事件的主键或者非空唯一索引的列值发生改变，则会将该条事件拆分为 Delete 和 Insert 两条事件。更多信息，请参考[用户文档](/ticdc/ticdc-split-update-behavior.md#含有单条-update-变更的事务拆分)。

## 改进提升

+ TiDB

    - 提升了对带有 Placement Rules 的分区表的 `TRUNCATE` 操作速度 [#43070](https://github.com/pingcap/tidb/issues/43070) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - 在 resolve lock 之后避免无效的 Stale Read 重试 [#43659](https://github.com/pingcap/tidb/issues/43659) @[you06](https://github.com/you06)
    - 在 Stale Read 遇到 `DataIsNotReady` 报错时使用 leader read 来降低延迟 [#765](https://github.com/tikv/client-go/pull/765) @[Tema](https://github.com/Tema)
    - 为 Stale Read 增加 `Stale Read OPS` 和 `Stale Read MBps` 指标，用于监控命中率和流量 [#43325](https://github.com/pingcap/tidb/issues/43325) @[you06](https://github.com/you06)

+ TiKV

    - 使用 gzip 压缩 `check_leader` 请求以减少流量 [#14839](https://github.com/tikv/tikv/issues/14839) @[cfzjywxk](https://github.com/cfzjywxk)

+ PD

    - PD Leader 选举使用单独的 gRPC 链接，防止受到其他请求的影响 [#6403](https://github.com/tikv/pd/issues/6403) @[rleungx](https://github.com/rleungx)

+ Tools

    + TiCDC

        - 优化 TiCDC 对 DDL 的处理方式，使 DDL 不阻塞其他无关的 DML Event 的使用，同时减少内存使用 [#8106](https://github.com/pingcap/tiflow/issues/8106) @[asddongmen](https://github.com/asddongmen)
        - 调整 Decoder 接口，增加了新方法 `AddKeyValue` [#8861](https://github.com/pingcap/tiflow/issues/8861) @[3AceShowHand](https://github.com/3AceShowHand)
        - 优化同步数据到对象存储的场景下发生 DDL 事件时的目录结构 [#8890](https://github.com/pingcap/tiflow/issues/8890) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - 支持同步到 Kafka-on-Pulsar 下游 [#8892](https://github.com/pingcap/tiflow/issues/8892) @[hi-rustin](https://github.com/hi-rustin)
        - 当同步数据到 Kafka 时，支持 OAuth 协议验证方式 [#8865](https://github.com/pingcap/tiflow/issues/8865) @[hi-rustin](https://github.com/hi-rustin)
        - 优化采用 Avro 或 CSV 协议同步数据时 TiCDC 对 `UPDATE` 语句的处理方式，即将其拆分为 `DELETE` 和 `INSERT` 语句，这样用户从 `DELETE` 语句中即可获取修改前的 old value [#9086](https://github.com/pingcap/tiflow/issues/9086) @[3AceShowHand](https://github.com/3AceShowHand)
        - 增加一个配置项 `insecure-skip-verify`，控制在同步数据到 Kafka 的场景下启用 TLS 时是否设置认证算法 [#8867](https://github.com/pingcap/tiflow/issues/8867) @[hi-rustin](https://github.com/hi-rustin)
        - TiCDC 优化 DDL 同步操作，减轻 DDL 操作对下游延迟的影响 [#8686](https://github.com/pingcap/tiflow/issues/8686) @[hi-rustin](https://github.com/hi-rustin)
        - 优化 TiCDC 在同步任务失败时对上游 GC TLS 的设置方法 [#8403](https://github.com/pingcap/tiflow/issues/8403) @[charleszheng44](https://github.com/charleszheng44)

    + TiDB Lightning

        - 在导入数据期间遇到 `unknown RPC` 错误时，增加了重试机制 [#43291](https://github.com/pingcap/tidb/issues/43291) @[D3Hunter](https://github.com/D3Hunter)

    + TiDB Binlog

        - 优化表信息的获取方式，降低 Drainer 的初始化时间和内存占用 [#1137](https://github.com/pingcap/tidb-binlog/issues/1137) @[lichunzhu](https://github.com/lichunzhu)

## 错误修复

+ TiDB

    - 修复 `min, max` 查询结果出错的问题 [#43805](https://github.com/pingcap/tidb/issues/43805) @[wshwsh12](https://github.com/wshwsh12)
    - 修复窗口函数计算下推到 TiFlash 时执行计划构造错误的问题 [#43922](https://github.com/pingcap/tidb/issues/43922) @[gengliqi](https://github.com/gengliqi)
    - 修复使用 CTE 的查询导致 TiDB 卡住的问题 [#43749](https://github.com/pingcap/tidb/issues/43749) [#36896](https://github.com/pingcap/tidb/issues/36896) @[guo-shaoge](https://github.com/guo-shaoge)
    - 修复在使用 `AES_DECRYPT` 表达式时，SQL 报错 `runtime error: index out of range` 的问题 [#43063](https://github.com/pingcap/tidb/issues/43063) @[lcwangchao](https://github.com/lcwangchao)
    - 修复 `SHOW PROCESSLIST` 语句无法显示子查询时间较长语句的事务的 TxnStart 的问题 [#40851](https://github.com/pingcap/tidb/issues/40851) @[crazycs520](https://github.com/crazycs520)
    - 修复 PD 隔离可能会导致运行的 DDL 阻塞的问题 [#44014](https://github.com/pingcap/tidb/issues/44014) [#43755](https://github.com/pingcap/tidb/issues/43755) [#44267](https://github.com/pingcap/tidb/issues/44267) @[wjhuang2016](https://github.com/wjhuang2016)
    - 修复使用 `UNION` 查询联合视图和临时表时 TiDB panic 的问题 [#42563](https://github.com/pingcap/tidb/issues/42563) @[lcwangchao](https://github.com/lcwangchao)
    - 修复 Placement Rule 在分区表下的行为问题，使得删除的分区 Placement Rule 可以被正确设置并回收 [#44116](https://github.com/pingcap/tidb/issues/44116) @[lcwangchao](https://github.com/lcwangchao)
    - 修复在 TRUNCATE 分区表的某个分区时可能造成分区的 Placement Rule 失效的问题 [#44031](https://github.com/pingcap/tidb/issues/44031) @[lcwangchao](https://github.com/lcwangchao)
    - 修复在重命名表期间 TiCDC 可能丢失部分行变更的问题 [#43338](https://github.com/pingcap/tidb/issues/43338) @[tangenta](https://github.com/tangenta)
    - 修复使用 BR 导入表后 DDL 作业历史记录丢失的问题 [#43725](https://github.com/pingcap/tidb/issues/43725) @[tangenta](https://github.com/tangenta)
    - 修复了 `JSON_OBJECT` 在某些情况下会报错的问题 [#39806](https://github.com/pingcap/tidb/issues/39806) @[YangKeao](https://github.com/YangKeao)
    - 修复 IPv6 环境下的集群无法查询部分系统视图的问题 [#43286](https://github.com/pingcap/tidb/issues/43286) @[Defined2014](https://github.com/Defined2014) @[nexustar](https://github.com/nexustar)
    - 修复当 PD 成员地址发生变化时，为 `AUTO_INCREMENT` 列分配 ID 会被长时间阻塞的问题 [#42643](https://github.com/pingcap/tidb/issues/42643) @[tiancaiamao](https://github.com/tiancaiamao)
    - 修复回收放置规则时，TiDB 向 PD 发送重复请求造成 PD 日志中出现大量 `full config reset` 的问题 [#33069](https://github.com/pingcap/tidb/issues/33069) @[tiancaiamao](https://github.com/tiancaiamao)
    - 修复了 `SHOW PRIVILEGES` 命令显示的权限列表不完整的问题 [#40591](https://github.com/pingcap/tidb/issues/40591) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - 修复 `ADMIN SHOW DDL JOBS LIMIT` 返回错误结果的问题 [#42298](https://github.com/pingcap/tidb/issues/42298) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - 修复在开启密码强度校验时对 `tidb_auth_token` 用户进行校验导致用户创建失败的问题 [#44098](https://github.com/pingcap/tidb/issues/44098) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - 修复动态裁剪模式下内连接表时找不到分区的问题 [#43686](https://github.com/pingcap/tidb/issues/43686) @[mjonss](https://github.com/mjonss)
    - 修复在分区表上执行 `MODIFY COLUMN` 时输出 `Data Truncated` 相关报错的问题 [#41118](https://github.com/pingcap/tidb/issues/41118) @[mjonss](https://github.com/mjonss)
    - 修复 IPv6 环境下显示错误的 TiDB 地址的问题 [#43260](https://github.com/pingcap/tidb/issues/43260) @[nexustar](https://github.com/nexustar)
    - 修复在谓词下推的情况下 CTE 结果错误的问题 [#43645](https://github.com/pingcap/tidb/issues/43645) @[winoros](https://github.com/winoros)
    - 修复在带有非关联子查询的语句中使用公共表表达式 (CTE) 可能导致结果错误的问题 [#44051](https://github.com/pingcap/tidb/issues/44051) @[winoros](https://github.com/winoros)
    - 修复 Join Reorder 可能会造成 Outer Join 结果错误的问题 [#44314](https://github.com/pingcap/tidb/issues/44314) @[AilinKid](https://github.com/AilinKid)
    - 修复在一些极端情况下，悲观事务的第一条语句发生重试时，对该事务进行 resolve lock 可能影响事务正确性的问题 [#42937](https://github.com/pingcap/tidb/issues/42937) @[MyonKeminta](https://github.com/MyonKeminta)
    - 修复在一些罕见的情况下，悲观事务的残留悲观锁在 GC resolve lock 时可能影响数据正确性的问题 [#43243](https://github.com/pingcap/tidb/issues/43243) @[MyonKeminta](https://github.com/MyonKeminta)
    - 修复了 `batch cop` 在执行过程中的 scan detail 信息不准确的问题 [#41582](https://github.com/pingcap/tidb/issues/41582) @[you06](https://github.com/you06)
    - 修复在同时使用 Stale Read 和 `PREPARE` 语句时 TiDB 无法读取到数据更新的问题 [#43044](https://github.com/pingcap/tidb/issues/43044) @[you06](https://github.com/you06)
    - 修复执行 `LOAD DATA` 语句可能误报 `assertion failed` 的问题 [#43849](https://github.com/pingcap/tidb/issues/43849) @[you06](https://github.com/you06)
    - 修复使用 Stale Read 过程中，当 coprocessor 遇到 `region data not ready` 情况时无法 fallback 到 leader 的问题 [#43365](https://github.com/pingcap/tidb/issues/43365) @[you06](https://github.com/you06)

+ TiKV

    - 修复当一个 TiKV 节点失败时，对应 Region 的 peers 错误地进入休眠模式的问题 [#14547](https://github.com/tikv/tikv/issues/14547) @[hicqu](https://github.com/hicqu)
    - 修复 Continuous Profiling 中的文件句柄泄露的问题 [#14224](https://github.com/tikv/tikv/issues/14224) @[tabokie](https://github.com/tabokie)
    - 修复 PD 宕机可能造成 PITR 无法推进的问题 [#14184](https://github.com/tikv/tikv/issues/14184) @[YuJuncen](https://github.com/YuJuncen)
    - 修复加密 Key ID 冲突会导致旧 Key 被删除的问题 [#14585](https://github.com/tikv/tikv/issues/14585) @[tabokie](https://github.com/tabokie)
    - 修复 autocommit 和 point get replica read 可能破坏线性一致性的问题 [#14715](https://github.com/tikv/tikv/issues/14715) @[cfzjywxk](https://github.com/cfzjywxk)
    - 修复集群从较低版本升级到 v6.5 或更高版本时，由于累计的 Lock 记录可能导致性能下降的问题 [#14780](https://github.com/tikv/tikv/issues/14780) @[MyonKeminta](https://github.com/MyonKeminta)
    - 修复 TiDB Lightning 可能导致 SST 文件泄露的问题 [#14745](https://github.com/tikv/tikv/issues/14745) @[YuJuncen](https://github.com/YuJuncen)
    - 修复加密密钥和 raft log 文件删除之间的潜在冲突导致 TiKV 无法启动的问题 [#14761](https://github.com/tikv/tikv/issues/14761) @[Connor1996](https://github.com/Connor1996)

+ TiFlash

    - 修复分区表 TableScan 算子在 Region 迁移时性能劣化的问题 [#7519](https://github.com/pingcap/tiflash/issues/7519) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - 修复在 GENERATED 类型表字段与 TIMESTAMP 或 TIME 类型同时存在的情况下，查询 TiFlash 可能会报错的问题 [#7468](https://github.com/pingcap/tiflash/issues/7468) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - 修复大的更新事务可能会导致 TiFlash 反复报错重启的问题 [#7316](https://github.com/pingcap/tiflash/issues/7316) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复 `INSERT SELECT` 语句从 TiFlash 读取数据时报错 "Truncate error cast decimal as decimal" 的问题 [#7348](https://github.com/pingcap/tiflash/issues/7348) @[windtalker](https://github.com/windtalker)
    - 修复查询在 Join build 侧数据非常大，且包含许多小型字符串类型列时，消耗的内存可能会超过实际需要的问题 [#7416](https://github.com/pingcap/tiflash/issues/7416) @[yibin87](https://github.com/yibin87)

+ Tools

    + Backup & Restore (BR)

        - 修复备份失败时 BR 的报错信息 "resolve lock timeout" 具有误导性，掩盖了实际错误的问题 [#43236](https://github.com/pingcap/tidb/issues/43236) @[YuJuncen](https://github.com/YuJuncen)

    + TiCDC

        - 修复在表数量多达 50000 个时可能出现 OOM 的问题 [#7872](https://github.com/pingcap/tiflow/issues/7872) @[sdojjy](https://github.com/sdojjy)
        - 修复 TiCDC 在上游 TiDB 发生 OOM 时卡住的问题 [#8561](https://github.com/pingcap/tiflow/issues/8561) @[overvenus](https://github.com/overvenus)
        - 修复 PD 出现网络隔离或 PD Owner 节点重启等故障时 TiCDC 卡住问题 [#8808](https://github.com/pingcap/tiflow/issues/8808) [#8812](https://github.com/pingcap/tiflow/issues/8812) [#8877](https://github.com/pingcap/tiflow/issues/8877) @[asddongmen](https://github.com/asddongmen)
        - 修复 TiCDC 的时区设置问题 [#8798](https://github.com/pingcap/tiflow/issues/8798) @[hi-rustin](https://github.com/hi-rustin)
        - 修复上游 TiKV 节点 crash 时 checkpoint lag 上升的问题 [#8858](https://github.com/pingcap/tiflow/issues/8858) @[hicqu](https://github.com/hicqu)
        - 修复在同步数据到下游 MySQL 的场景中，当上游 TiDB 执行 `FLASHBACK CLUSTER TO TIMESTAMP` 语句后同步出错的问题 [#8040](https://github.com/pingcap/tiflow/issues/8040) @[asddongmen](https://github.com/asddongmen)
        - 修复当同步数据到对象存储时上游的 `EXCHANGE PARTITION` 操作没有正常同步到下游的问题 [#8914](https://github.com/pingcap/tiflow/issues/8914) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - 修复在某些特殊场景下 sorter 组件内存使用过多导致 OOM 的问题 [#8974](https://github.com/pingcap/tiflow/issues/8974) @[hicqu](https://github.com/hicqu)
        - 修复当下游为 Kafka 时，TiCDC 查询下游的元信息频率过高导致下游负载过大的问题 [#8957](https://github.com/pingcap/tiflow/issues/8957) [#8959](https://github.com/pingcap/tiflow/issues/8959) @[hi-rustin](https://github.com/hi-rustin)
        - 修复当 Kafka 消息过大导致同步出错时，在 Log 中记录了消息体的问题 [#9031](https://github.com/pingcap/tiflow/issues/9031) @[darraes](https://github.com/darraes)
        - 修复下游 Kafka 滚动重启时 TiCDC 节点发生 panic 的问题 [#9023](https://github.com/pingcap/tiflow/issues/9023) @[asddongmen](https://github.com/asddongmen)
        - 修复同步数据到存储服务时，下游 DDL 语句对应的 JSON 文件中没有记录表中字段默认值的问题 [#9066](https://github.com/pingcap/tiflow/issues/9066) @[CharlesCheung96](https://github.com/CharlesCheung96)

    + TiDB Lightning

        - 修复宽表导入时可能出现 OOM 的问题 [#43728](https://github.com/pingcap/tidb/issues/43728) @[D3Hunter](https://github.com/D3Hunter)
        - 修复大数据量导入时报 `write to tikv with no leader returned` 错误的问题 [#43055](https://github.com/pingcap/tidb/issues/43055) @[lance6716](https://github.com/lance6716)
        - 修复当数据文件中存在未闭合的 delimiter 时可能 OOM 的问题 [#40400](https://github.com/pingcap/tidb/issues/40400) @[buchuitoudegou](https://github.com/buchuitoudegou) @[lance6716](https://github.com/lance6716)

    + TiDB Binlog

        - 修复遇到状态为 `CANCELED` 的 DDL 时 TiDB Binlog 报错的问题 [#1228](https://github.com/pingcap/tidb-binlog/issues/1228) @[okJiang](https://github.com/okJiang)
