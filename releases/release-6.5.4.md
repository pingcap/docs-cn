---
title: TiDB 6.5.4 Release Notes
summary: 了解 TiDB 6.5.4 版本的兼容性变更、改进提升，以及错误修复。
---

# TiDB 6.5.4 Release Notes

发版日期：2023 年 8 月 28 日

TiDB 版本：6.5.4

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v6.5/quick-start-with-tidb) | [生产部署](https://docs.pingcap.com/zh/tidb/v6.5/production-deployment-using-tiup) | [下载离线包](https://cn.pingcap.com/product-community/?version=v6.5.4#version-list)

## 兼容性变更

- 为了修复当使用 `Cursor Fetch` 获取大结果集时 TiDB 占用大量内存的问题，TiDB 会自动将结果集写入磁盘以释放内存资源 [#43233](https://github.com/pingcap/tidb/issues/43233) @[YangKeao](https://github.com/YangKeao)
- 默认关闭 RocksDB 的周期性 compaction，使 TiKV RocksDB 的默认行为和 v6.5.0 之前的版本保持一致，避免在升级之后集中产生大量 compaction 影响系统的性能。同时，TiKV 新增 [`rocksdb.[defaultcf|writecf|lockcf].periodic-compaction-seconds`](https://docs.pingcap.com/zh/tidb/v6.5/tikv-configuration-file#periodic-compaction-seconds-从-v654-版本开始引入) 和 [`rocksdb.[defaultcf|writecf|lockcf].ttl`](https://docs.pingcap.com/zh/tidb/v6.5/tikv-configuration-file#ttl-从-v654-版本开始引入) 配置项，支持手动配置 RocksDB 的周期性 compaction [#15355](https://github.com/tikv/tikv/issues/15355) @[LykxSassinator](https://github.com/LykxSassinator)

### 行为变更

- 对于包含多条变更的事务，如果 Update 事件的主键或者非空唯一索引的列值发生改变，TiCDC 会将该其拆分为 Delete 和 Insert 两条事件，并确保将所有事件有序，以保证 Delete 事件在 Insert 事件之前。更多信息，请参考[用户文档](/ticdc/ticdc-split-update-behavior.md#含有多条-update-变更的事务拆分)。

## 改进提升

+ TiDB

    - 优化 `LOAD DATA` 语句中包含赋值表达式时 `LOAD DATA` 的执行性能 [#46081](https://github.com/pingcap/tidb/issues/46081) @[gengliqi](https://github.com/gengliqi)
    - 优化与落盘相关的 chunk 读取的性能 [#45125](https://github.com/pingcap/tidb/issues/45125) @[YangKeao](https://github.com/YangKeao)
    - 新增 `halt-scheduling` 配置项，用于关闭 PD 调度 [#6493](https://github.com/tikv/pd/issues/6493) @[JmPotato](https://github.com/JmPotato)

+ TiKV

    - 使用 gzip 压缩 `check_leader` 请求以减少流量 [#14553](https://github.com/tikv/tikv/issues/14553) @[you06](https://github.com/you06)
    - 添加 `Max gap of safe-ts` 和 `Min safe ts region` 监控项以及 `tikv-ctl get-region-read-progress` 命令，用于更好地观测和诊断 resolved-ts 和 safe-ts 的状态 [#15082](https://github.com/tikv/tikv/issues/15082) @[ekexium](https://github.com/ekexium)
    - 在 TiKV 中暴露部分 RocksDB 配置，允许用户禁用 TTL 和定期数据整理等特性 [#14873](https://github.com/tikv/tikv/issues/14873) @[LykxSassinator](https://github.com/LykxSassinator)
    - 避免写 Titan manifest 文件时持有锁导致影响其他线程 [#15351](https://github.com/tikv/tikv/issues/15351) @[Connor1996](https://github.com/Connor1996)
    - 优化数据整理检查机制，当触发 Region Split 时，如果没有可以分裂的 key，触发一次数据整理，以消除过多的 MVCC 版本 [#15282](https://github.com/tikv/tikv/issues/15282) @[SpadeA-Tang](https://github.com/SpadeA-Tang)

+ PD

    - 未开启 Swagger server 时，PD 默认屏蔽 Swagger API [#6786](https://github.com/tikv/pd/issues/6786) @[bufferflies](https://github.com/bufferflies)
    - 提升 etcd 的高可用性 [#6554](https://github.com/tikv/pd/issues/6554) [#6442](https://github.com/tikv/pd/issues/6442) @[lhy1024](https://github.com/lhy1024)
    - 减少 `GetRegions` 请求的内存占用 [#6835](https://github.com/tikv/pd/issues/6835) @[lhy1024](https://github.com/lhy1024)
    - 支持重复使用 HTTP 连接 [#6913](https://github.com/tikv/pd/issues/6913) @[nolouch](https://github.com/nolouch)

+ TiFlash

    - 通过 IO 攒批优化提升了 TiFlash 的数据写入性能 [#7735](https://github.com/pingcap/tiflash/issues/7735) @[lidezhu](https://github.com/lidezhu)
    - 通过去掉不必要的文件 fsync 操作提升了 TiFlash 的数据写入性能 [#7736](https://github.com/pingcap/tiflash/issues/7736) @[lidezhu](https://github.com/lidezhu)
    - 限制了 TiFlash coprocessor task 队列的最大长度，避免过多的 coprocessor task 排队导致 TiFlash 无法正常服务的问题 [#7747](https://github.com/pingcap/tiflash/issues/7747) @[LittleFall](https://github.com/LittleFall)

+ Tools

    + Backup & Restore (BR)

        - 通过设置 HTTP 客户端 MaxIdleConns 和 MaxIdleConnsPerHost 参数，增强对连接复用的支持 [#46011](https://github.com/pingcap/tidb/issues/46011) @[Leavrth](https://github.com/Leavrth)
        - 增强 BR 在连接 PD 或者是外部 S3 存储出错时的容错能力 [#42909](https://github.com/pingcap/tidb/issues/42909) @[Leavrth](https://github.com/Leavrth)
        - 新增 restore 参数 `WaitTiflashReady`。当打开这个参数时，restore 操作将会等待 TiFlash 副本复制成功后才结束 [#43828](https://github.com/pingcap/tidb/issues/43828) [#46302](https://github.com/pingcap/tidb/issues/46302) @[3pointer](https://github.com/3pointer)

    + TiCDC

        - 优化 TiCDC 在故障重试时的状态展示信息 [#9483](https://github.com/pingcap/tiflow/issues/9483) @[asddongmen](https://github.com/asddongmen)
        - 优化同步到 Kafka 时对超过限制的消息的处理方式，支持只发送主键到下游 [#9574](https://github.com/pingcap/tiflow/issues/9574) @[3AceShowHand](https://github.com/3AceShowHand)
        - Storage Sink 支持对 HEX 格式的数据进行十六进制编码输出，使其兼容 AWS DMS 的格式规范 [#9373](https://github.com/pingcap/tiflow/issues/9373) @[CharlesCheung96](https://github.com/CharlesCheung96)

    + TiDB Data Migration (DM)

        - 对不兼容的 DDL 支持严格的乐观模式 [#9112](https://github.com/pingcap/tiflow/issues/9112) @[GMHDBJD](https://github.com/GMHDBJD)

    + Dumpling

        - 当使用 `--sql` 参数导出数据时跳过查询所有数据库和表，减少导出开销 [#45239](https://github.com/pingcap/tidb/issues/45239) @[lance6716](https://github.com/lance6716)

## 错误修复

+ TiDB

    - 修复下推 `STREAM_AGG()` 算子时，可能报错 `index out of range` 的问题 [#40857](https://github.com/pingcap/tidb/issues/40857) @[Dousir9](https://github.com/Dousir9)
    - 修复 `CREATE TABLE` 语句包含子分区定义时，TiDB 会忽略所有分区信息创建出普通表的问题 [#41198](https://github.com/pingcap/tidb/issues/41198) [#41200](https://github.com/pingcap/tidb/issues/41200) @[mjonss](https://github.com/mjonss)
    - 修复 `stale_read_ts` 设置不正确可能导致 `PREPARE stmt` 读数据不正确的问题 [#43044](https://github.com/pingcap/tidb/issues/43044) @[you06](https://github.com/you06)
    - 修复 ActivateTxn 可能出现数据竞争的问题 [#42092](https://github.com/pingcap/tidb/issues/42092) @[hawkingrei](https://github.com/hawkingrei)
    - 修复 batch client 重连不及时的问题 [#44431](https://github.com/pingcap/tidb/issues/44431) @[crazycs520](https://github.com/crazycs520)
    - 修复 SQL compile 报错的日志未脱敏的问题 [#41831](https://github.com/pingcap/tidb/issues/41831) @[lance6716](https://github.com/lance6716)
    - 修复同时使用 CTE 和关联子查询可能导致查询结果出错或者 panic 的问题 [#44649](https://github.com/pingcap/tidb/issues/44649) [#38170](https://github.com/pingcap/tidb/issues/38170) [#44774](https://github.com/pingcap/tidb/issues/44774) @[winoros](https://github.com/winoros) @[guo-shaoge](https://github.com/guo-shaoge)
    - 修复 TTL 任务不能及时触发统计信息更新的问题 [#40109](https://github.com/pingcap/tidb/issues/40109) @[YangKeao](https://github.com/YangKeao)
    - 修复 GC resolve lock 可能错过一些悲观锁的问题 [#45134](https://github.com/pingcap/tidb/issues/45134) @[MyonKeminta](https://github.com/MyonKeminta)
    - 修复在使用 binary protocol 连接 TiDB 且大量地执行 `PREPARE` 和 `EXECUTE` 语句的场景下，导致内存泄漏、duration 持续升高的问题 [#44612](https://github.com/pingcap/tidb/issues/44612) @[wshwsh12](https://github.com/wshwsh12)
    - 修复 `INFORMATION_SCHEMA.DDL_JOBS` 表中 `QUERY` 列的数据长度可能超出列定义的问题 [#42440](https://github.com/pingcap/tidb/issues/42440) @[tiancaiamao](https://github.com/tiancaiamao)
    - 修复使用 `Prepare` 或 `Execute` 查询某些虚拟表时无法将表 ID 下推，导致在大量 Region 的情况下 PD OOM 的问题 [#39605](https://github.com/pingcap/tidb/issues/39605) @[djshow832](https://github.com/djshow832)
    - 修复在为分区表添加新的索引之后，该分区表可能无法正确触发统计信息的自动收集的问题 [#41638](https://github.com/pingcap/tidb/issues/41638) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes)
    - 修复极端情况下，统计 SQL execution detail 的信息占用太多内存导致 TiDB OOM 的问题 [#44047](https://github.com/pingcap/tidb/issues/44047) @[wshwsh12](https://github.com/wshwsh12)
    - 修复 batch coprocessor 重试时可能会生成错误 Region 信息导致查询失败的问题 [#44622](https://github.com/pingcap/tidb/issues/44622) @[windtalker](https://github.com/windtalker)
    - 修复带 `indexMerge` 的查询被 kill 时可能会卡住的问题 [#45279](https://github.com/pingcap/tidb/issues/45279) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - 修复某些情况下查询系统表 `INFORMATION_SCHEMA.TIKV_REGION_STATUS` 返回结果错误的问题 [#45531](https://github.com/pingcap/tidb/issues/45531) @[Defined2014](https://github.com/Defined2014)
    - 修复当开启 `tidb_enable_parallel_apply` 时，MPP 模式下的查询结果出错的问题 [#45299](https://github.com/pingcap/tidb/issues/45299) @[windtalker](https://github.com/windtalker)
    - 修复开启 `tidb_opt_agg_push_down` 时查询可能返回错误结果的问题 [#44795](https://github.com/pingcap/tidb/issues/44795) @[AilinKid](https://github.com/AilinKid)
    - 修复由虚拟列引发的 `can't find proper physical plan` 问题 [#41014](https://github.com/pingcap/tidb/issues/41014) @[AilinKid](https://github.com/AilinKid)
    - 修复 `processInfo` 为空导致的 panic 问题 [#43829](https://github.com/pingcap/tidb/issues/43829) @[zimulala](https://github.com/zimulala)
    - 修复 `SELECT CAST(n AS CHAR)` 语句中的 `n` 为负数时，查询结果出错的问题 [#44786](https://github.com/pingcap/tidb/issues/44786) @[xhebox](https://github.com/xhebox)
    - 修复当使用 MySQL 的 Cursor Fetch 协议时，结果集占用的内存超过 `tidb_mem_quota_query` 的限制导致 TiDB OOM 的问题。修复后，TiDB 会自动将结果集写入磁盘以释放内存资源 [#43233](https://github.com/pingcap/tidb/issues/43233) @[YangKeao](https://github.com/YangKeao)
    - 修复通过 BR 恢复 `AUTO_ID_CACHE=1` 的表时，会遇到 `duplicate entry` 报错的问题 [#44716](https://github.com/pingcap/tidb/issues/44716) @[tiancaiamao](https://github.com/tiancaiamao)
    - 修复当分区表定义中使用了 `FLOOR()` 函数对分区列进行取整时 `SELECT` 语句返回错误的问题 [#42323](https://github.com/pingcap/tidb/issues/42323) @[jiyfhust](https://github.com/jiyfhust)
    - 修复并发视图模式可能会造成 DDL 操作卡住的问题 [#40352](https://github.com/pingcap/tidb/issues/40352) @[zeminzhou](https://github.com/zeminzhou)
    - 修复收集统计信息任务因为错误的 `datetime` 值而失败的问题 [#39336](https://github.com/pingcap/tidb/issues/39336) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes)
    - 修复集群的 PD 节点被替换后一些 DDL 语句会卡住一段时间的问题 [#33908](https://github.com/pingcap/tidb/issues/33908)
    - 修复 resolve lock 在 PD 时间跳变的情况下可能卡住的问题 [#44822](https://github.com/pingcap/tidb/issues/44822) @[zyguan](https://github.com/zyguan)
    - 修复 index scan 中可能存在的数据竞争问题 [#45126](https://github.com/pingcap/tidb/issues/45126) @[wshwsh12](https://github.com/wshwsh12)
    - 修复对于过长的 SQL 输入，`FormatSQL()` 方法无法正常截断的问题 [#44542](https://github.com/pingcap/tidb/issues/44542) @[hawkingrei](https://github.com/hawkingrei)
    - 修复即使用户没有权限，也能查看 `INFORMATION_SCHEMA.TIFLASH_REPLICA` 表信息的问题 [#45320](https://github.com/pingcap/tidb/issues/45320) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - 修复 `DATETIME` 或 `TIMESTAMP` 列与数字值比较时，行为与 MySQL 不一致的问题 [#38361](https://github.com/pingcap/tidb/issues/38361) @[yibin87](https://github.com/yibin87)
    - 修复 Index Join 出错可能导致查询卡住的问题 [#45716](https://github.com/pingcap/tidb/issues/45716) @[wshwsh12](https://github.com/wshwsh12)
    - 修复 kill 连接之后可能会出现 go coroutine 泄露的问题 [#46034](https://github.com/pingcap/tidb/issues/46034) @[pingyu](https://github.com/pingyu)
    - 修复 `tmp-storage-quota` 配置无法生效的问题 [#45161](https://github.com/pingcap/tidb/issues/45161) [#26806](https://github.com/pingcap/tidb/issues/26806) @[wshwsh12](https://github.com/wshwsh12)
    - 修复集群中有 TiFlash 节点宕机时，TiFlash 副本可能不可用的问题 [#38484](https://github.com/pingcap/tidb/issues/38484) @[hehechen](https://github.com/hehechen)
    - 修复并发读写 `Config.Labels` 时可能出现数据竞争导致 TiDB crash 的问题 [#45561](https://github.com/pingcap/tidb/issues/45561) @[genliqi](https://github.com/gengliqi)
    - 修复在集群规模大时 client-go 周期性更新 `min-resolved-ts` 可能造成 PD OOM 的问题 [#46664](https://github.com/pingcap/tidb/issues/46664) @[HuSharp](https://github.com/HuSharp)

+ TiKV

    - 修复 `ttl-check-poll-interval` 配置项对 RawKV API V2 不生效的问题 [#15142](https://github.com/tikv/tikv/issues/15142) @[pingyu](https://github.com/pingyu)
    - 修复 Online Unsafe Recovery 超时未中止的问题 [#15346](https://github.com/tikv/tikv/issues/15346) @[Connor1996](https://github.com/Connor1996)
    - 修复在执行 `FLASHBACK` 后 Region Merge 可能被阻塞的问题 [#15258](https://github.com/tikv/tikv/issues/15258) @[overvenus](https://github.com/overvenus)
    - 修复当一个 TiKV 节点被隔离而另一个节点重启时，可能导致读取不一致的问题 [#15035](https://github.com/tikv/tikv/issues/15035) @[overvenus](https://github.com/overvenus)
    - 修复自适应同步模式下 sync-recover 阶段 QPS 下降到 0 的问题 [#14975](https://github.com/tikv/tikv/issues/14975) @[nolouch](https://github.com/nolouch)
    - 修复部分写入时加密可能导致数据损坏的问题 [#15080](https://github.com/tikv/tikv/issues/15080) @[tabokie](https://github.com/tabokie)
    - 减少 Store 心跳重试次数，修复心跳风暴的问题 [#15184](https://github.com/tikv/tikv/issues/15184) @[nolouch](https://github.com/nolouch)
    - 修复当待处理的数据整理字节数较高时流量控制可能无效的问题 [#14392](https://github.com/tikv/tikv/issues/14392) @[Connor1996](https://github.com/Connor1996)
    - 修复 PD 和 TiKV 之间的网络中断可能导致 PITR 卡住的问题 [#15279](https://github.com/tikv/tikv/issues/15279) @[YuJuncen](https://github.com/YuJuncen)
    - 修复在启用了 TiCDC 的 Old Value 功能时，TiKV 可能会使用更多内存的问题 [#14815](https://github.com/tikv/tikv/issues/14815) @[YuJuncen](https://github.com/YuJuncen)

+ PD

    - 修复当 etcd 已经启动，但 client 尚未连接上 etcd 时，调用 client 会导致 PD panic 的问题 [#6860](https://github.com/tikv/pd/issues/6860) @[HuSharp](https://github.com/HuSharp)
    - 修复 leader 长时间无法退出的问题 [#6918](https://github.com/tikv/pd/issues/6918) @[bufferflies](https://github.com/bufferflies)
    - 修复 Placement Rule 在使用 `LOCATION_LABELS` 时，SQL 和 Rule Checker 不兼容的问题 [#38605](https://github.com/pingcap/tidb/issues/38605) @[nolouch](https://github.com/nolouch)
    - 修复 PD 可能会非预期地向 Region 添加多个 Learner 的问题 [#5786](https://github.com/tikv/pd/issues/5786) @[HunDunDM](https://github.com/HunDunDM)
    - 修复在 rule checker 选定 peer 时，unhealthy peer 无法被移除的问题 [#6559](https://github.com/tikv/pd/issues/6559) @[nolouch](https://github.com/nolouch)
    - 修复 `unsafe recovery` 中失败的 learner peer 在 `auto-detect` 模式中被忽略的问题 [#6690](https://github.com/tikv/pd/issues/6690) @[v01dstar](https://github.com/v01dstar)

+ TiFlash

    - 修复在更改 `DATETIME`、`TIMESTAMP`、`TIME` 数据类型的 `fsp` 之后查询失败的问题 [#7809](https://github.com/pingcap/tiflash/issues/7809) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复由于 Region 的边界的 Key 不合法导致 TiFlash 数据不一致的问题 [#7762](https://github.com/pingcap/tiflash/issues/7762) @[lidezhu](https://github.com/lidezhu)
    - 修复当同一个 MPP Task 内有多个 HashAgg 算子时，可能导致 MPP Task 编译时间过长而严重影响查询性能的问题 [#7810](https://github.com/pingcap/tiflash/issues/7810) @[SeaRise](https://github.com/SeaRise)
    - 修复 TiFlash 在使用 Online Unsafe Recovery 之后重启时间过长的问题 [#7671](https://github.com/pingcap/tiflash/issues/7671) @[hongyunyan](https://github.com/hongyunyan)
    - 修复 TiFlash 在进行除法运算时对 `DECIMAL` 结果 round 进位错误的问题 [#6462](https://github.com/pingcap/tiflash/issues/6462) @[LittleFall](https://github.com/LittleFall)

+ Tools

    + Backup & Restore (BR)

        - 将 BR 使用的全局参数 `TableColumnCountLimit` 和 `IndexLimit` 的默认值提升到最大值，修复恢复过程失败的问题 [#45793](https://github.com/pingcap/tidb/issues/45793) @[Leavrth](https://github.com/Leavrth)
        - 修复 PITR 中处理 DDL meta 信息时 rewrite 出错的问题 [#43184](https://github.com/pingcap/tidb/issues/43184) @[Leavrth](https://github.com/Leavrth)
        - 修复 PITR 执行中没有检查函数返回而导致 panic 的问题 [#45853](https://github.com/pingcap/tidb/issues/45853) @[Leavrth](https://github.com/Leavrth)
        - 修复当使用非 Amazon S3 而是其他 S3 兼容的存储时，获取无效 region ID 的问题 [#41916](https://github.com/pingcap/tidb/issues/41916) [#42033](https://github.com/pingcap/tidb/issues/42033) @[3pointer](https://github.com/3pointer)
        - 修复 RawKV 模式下细粒度备份阶段可能出错的问题 [#37085](https://github.com/pingcap/tidb/issues/37085) @[pingyu](https://github.com/pingyu)
        - 修复当 TiDB 集群不存在 PITR 备份任务时，`resolve lock` 频率过高的问题 [#40759](https://github.com/pingcap/tidb/issues/40759) @[joccau](https://github.com/joccau)
        - 缓解了 Region leadership 迁移导致 PITR 日志备份进度延迟变高的问题 [#13638](https://github.com/tikv/tikv/issues/13638) @[YuJuncen](https://github.com/YuJuncen)

    + TiCDC

        - 修复下游发生故障重试时同步任务可能卡住的问题 [#9450](https://github.com/pingcap/tiflow/issues/9450) @[hicqu](https://github.com/hicqu)
        - 修复同步到 Kafka 时重试间隔过短导致同步任务失败的问题 [#9504](https://github.com/pingcap/tiflow/issues/9504) @[3AceShowHand](https://github.com/3AceShowHand)
        - 修复在上游同一个事务中修改多行唯一键场景下，TiCDC 可能导致同步写冲突的问题 [#9430](https://github.com/pingcap/tiflow/issues/9430) @[sdojjy](https://github.com/sdojjy)
        - 修复可能无法正确同步 rename DDL 操作的问题 [#9488](https://github.com/pingcap/tiflow/issues/9488) [#9378](https://github.com/pingcap/tiflow/issues/9378) [#9531](https://github.com/pingcap/tiflow/issues/9531) @[asddongmen](https://github.com/asddongmen)
        - 修复下游发生短时间故障导致同步任务卡住的问题 [#9542](https://github.com/pingcap/tiflow/issues/9542) [#9272](https://github.com/pingcap/tiflow/issues/9272)[#9582](https://github.com/pingcap/tiflow/issues/9582) [#9592](https://github.com/pingcap/tiflow/issues/9592) @[hicqu](https://github.com/hicqu)
        - 修复在 TiCDC 节点状态发生改变时可能引发的 panic 问题 [#9354](https://github.com/pingcap/tiflow/issues/9354) @[sdojjy](https://github.com/sdojjy)
        - 修复当 Kafka Sink 遇到错误时可能会无限阻塞同步任务推进的问题 [#9309](https://github.com/pingcap/tiflow/issues/9309) @[hicqu](https://github.com/hicqu)
        - 修复当下游为 Kafka 时，TiCDC 查询下游的元信息频率过高导致下游负载过大的问题 [#8957](https://github.com/pingcap/tiflow/issues/8957) [#8959](https://github.com/pingcap/tiflow/issues/8959) @[hi-rustin](https://github.com/hi-rustin)
        - 修复 TiCDC 部分节点发生网络隔离时可能引发的数据不一致问题 [#9344](https://github.com/pingcap/tiflow/issues/9344) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - 修复在打开 redo log 且下游出现异常时可能会导致同步任务卡住的问题 [#9172](https://github.com/pingcap/tiflow/issues/9172) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - 修复由于 PD 短暂不可用而导致同步任务报错的问题 [#9294](https://github.com/pingcap/tiflow/issues/9294) @[asddongmen](https://github.com/asddongmen)
        - 修复同步到 TiDB 或 MySQL 场景下，频繁设置下游双向复制相关变量导致下游日志过多的问题 [#9180](https://github.com/pingcap/tiflow/issues/9180) @[asddongmen](https://github.com/asddongmen)
        - 修复对默认 `ENUM` 值编码错误的问题 [#9259](https://github.com/pingcap/tiflow/issues/9259) @[3AceShowHand](https://github.com/3AceShowHand)

    + TiDB Data Migration (DM)

        - 修复唯一键列名为空时导致 panic 问题 [#9247](https://github.com/pingcap/tiflow/issues/9247) @[lance6716](https://github.com/lance6716)
        - 修复 validator 处理错误时可能死锁的问题，并优化了 retry 机制 [#9257](https://github.com/pingcap/tiflow/issues/9257) @[D3Hunter](https://github.com/D3Hunter)
        - 修复计算 causality key 时未考虑 collation 的问题 [#9489](https://github.com/pingcap/tiflow/issues/9489) @[hihihuhu](https://github.com/hihihuhu)

    + TiDB Lightning

        - 修复当存在正在导入数据的 engine 时 disk quota 检查可能阻塞的问题 [#44867](https://github.com/pingcap/tidb/issues/44867) @[D3Hunter](https://github.com/D3Hunter)
        - 修复当目标集群启用 SSL 时 checksum 报错 `Region is unavailable` 的问题 [#45462](https://github.com/pingcap/tidb/issues/45462) @[D3Hunter](https://github.com/D3Hunter)
        - 修复无法正确输出编码错误的问题 [#44321](https://github.com/pingcap/tidb/issues/44321) @[lyzx2001](https://github.com/lyzx2001)
        - 修复导入 CSV 数据时，route 可能 panic 的问题 [#43284](https://github.com/pingcap/tidb/issues/43284) @[lyzx2001](https://github.com/lyzx2001)
        - 修复逻辑导入模式下导入 A 表时可能误报 B 表不存在的问题 [#44614](https://github.com/pingcap/tidb/issues/44614) @[dsdashun](https://github.com/dsdashun)
        - 修复保存 `NEXT_GLOBAL_ROW_ID` 时类型错误问题 [#45427](https://github.com/pingcap/tidb/issues/45427) @[lyzx2001](https://github.com/lyzx2001)
        - 修复 `checksum = "optional"` 时 Checksum 阶段仍然报错的问题 [#45382](https://github.com/pingcap/tidb/issues/45382) @[lyzx2001](https://github.com/lyzx2001)
        - 修复当 PD 集群地址变更时数据导入失败的问题 [#43436](https://github.com/pingcap/tidb/issues/43436) @[lichunzhu](https://github.com/lichunzhu)
        - 修复部分 PD 节点失败导致数据导入失败的问题 [#43400](https://github.com/pingcap/tidb/issues/43400) @[lichunzhu](https://github.com/lichunzhu)
        - 修复当表使用 `AUTO_ID_CACHE=1` 且使用自增列时，ID 分配器 base 值错误的问题 [#46100](https://github.com/pingcap/tidb/issues/46100) @[D3Hunter](https://github.com/D3Hunter)

    + Dumpling

        - 修复导出到 Amazon S3 时未处理 file writer 关闭报错导致导出文件丢失的问题 [#45353](https://github.com/pingcap/tidb/issues/45353) @[lichunzhu](https://github.com/lichunzhu)

    + TiDB Binlog

        - 修复 etcd client 初始化时没有自动同步最新节点信息的问题 [#1236](https://github.com/pingcap/tidb-binlog/issues/1236) @[lichunzhu](https://github.com/lichunzhu)
