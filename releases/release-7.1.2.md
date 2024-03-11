---
title: TiDB 7.1.2 Release Notes
summary: 了解 TiDB 7.1.2 版本的兼容性变更、改进提升，以及错误修复。
---

# TiDB 7.1.2 Release Notes

发版日期：2023 年 10 月 25 日

TiDB 版本：7.1.2

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v7.1/quick-start-with-tidb) | [生产部署](https://docs.pingcap.com/zh/tidb/v7.1/production-deployment-using-tiup) | [下载离线包](https://cn.pingcap.com/product-community/?version=v7.1.2#version-list)

## 兼容性变更

- 在安全增强模式 (SEM) 下禁止设置 [`require_secure_transport`](https://docs.pingcap.com/zh/tidb/v7.1/system-variables#require_secure_transport-从-v610-版本开始引入) 为 `ON`，避免用户无法连接的问题 [#47665](https://github.com/pingcap/tidb/issues/47665) @[tiancaiamao](https://github.com/tiancaiamao)
- 默认关闭[平滑升级](/smooth-upgrade-tidb.md)功能，需要通过发送 `/upgrade/start` 和 `upgrade/finish` HTTP 请求开启此功能 [#47172](https://github.com/pingcap/tidb/issues/47172) @[zimulala](https://github.com/zimulala)
- 引入系统变量 [`tidb_opt_enable_hash_join`](https://docs.pingcap.com/zh/tidb/v7.1/system-variables#tidb_opt_enable_hash_join-从-v712-版本开始引入) 控制是否选择表的哈希连接 [#46695](https://github.com/pingcap/tidb/issues/46695) @[coderplay](https://github.com/coderplay)
- 默认关闭 RocksDB 的周期性 compaction，使 TiKV RocksDB 的默认行为和 v6.5.0 之前的版本保持一致，避免在升级之后集中产生大量 compaction 影响系统的性能。同时，TiKV 新增 [`rocksdb.[defaultcf|writecf|lockcf].periodic-compaction-seconds`](https://docs.pingcap.com/zh/tidb/v7.1/tikv-configuration-file#periodic-compaction-seconds-从-v712-版本开始引入) 和 [`rocksdb.[defaultcf|writecf|lockcf].ttl`](https://docs.pingcap.com/zh/tidb/v7.1/tikv-configuration-file#ttl-从-v712-版本开始引入) 配置项，支持手动配置 RocksDB 的周期性 compaction [#15355](https://github.com/tikv/tikv/issues/15355) @[LykxSassinator](https://github.com/LykxSassinator)
- 新增 TiCDC 配置项 [`sink.csv.binary-encoding-method`](/ticdc/ticdc-changefeed-config.md#ticdc-changefeed-配置文件说明)，控制 CSV 协议中二进制类型数据的编码方式，默认值为 `'base64'` [#9373](https://github.com/pingcap/tiflow/issues/9373) @[CharlesCheung96](https://github.com/CharlesCheung96)
- 新增 TiCDC 配置项 [`large-message-handle-option`](/ticdc/ticdc-sink-to-kafka.md#处理超过-kafka-topic-限制的消息)。默认为空，即消息大小超过 Kafka Topic 的限制后，同步任务失败。设置为 "handle-key-only" 时，如果消息超过大小，只发送 handle key 以减少消息的大小；如果依旧超过大小，则同步任务失败 [#9680](https://github.com/pingcap/tiflow/issues/9680) @[3AceShowHand](https://github.com/3AceShowHand)

### 行为变更

- 对于包含多条变更的事务，如果 Update 事件的主键或者非空唯一索引的列值发生改变，TiCDC 会将该其拆分为 Delete 和 Insert 两条事件，并确保将所有事件有序，以保证 Delete 事件在 Insert 事件之前。更多信息，请参考[用户文档](/ticdc/ticdc-behavior-change.md#含有多条-update-变更的事务拆分)。

## 改进提升

+ TiDB

    - 新增部分优化器提示，包括 [`NO_MERGE_JOIN()`](/optimizer-hints.md#no_merge_joint1_name--tl_name-)、[`NO_INDEX_JOIN()`](/optimizer-hints.md#no_index_joint1_name--tl_name-)、[`NO_INDEX_MERGE_JOIN()`](/optimizer-hints.md#no_index_merge_joint1_name--tl_name-)、[`NO_HASH_JOIN()`](/optimizer-hints.md#no_hash_joint1_name--tl_name-)、[`NO_INDEX_HASH_JOIN()`](/optimizer-hints.md#no_index_hash_joint1_name--tl_name-) [#45520](https://github.com/pingcap/tidb/issues/45520) @[qw4990](https://github.com/qw4990)
    - 添加 coprocessor 相关的 request source 信息 [#46514](https://github.com/pingcap/tidb/issues/46514) @[you06](https://github.com/you06)

+ TiKV

    - 优化数据整理检查机制，当触发 Region Split 时，如果没有可以分裂的 key，触发一次数据整理，以消除过多的 MVCC 版本 [#15282](https://github.com/tikv/tikv/issues/15282) @[SpadeA-Tang](https://github.com/SpadeA-Tang)
    - 消除 Router 对象中的 LRUCache，降低内存占用，防止 OOM [#15430](https://github.com/tikv/tikv/issues/15430) @[Connor1996](https://github.com/Connor1996)
    - 添加 `Max gap of safe-ts` 和 `Min safe ts region` 监控项以及 `tikv-ctl get-region-read-progress` 命令，用于更好地观测和诊断 resolved-ts 和 safe-ts 的状态 [#15082](https://github.com/tikv/tikv/issues/15082) @[ekexium](https://github.com/ekexium)
    - 在 TiKV 中暴露部分 RocksDB 配置，允许用户禁用 TTL 和定期数据整理等特性 [#14873](https://github.com/tikv/tikv/issues/14873) @[LykxSassinator](https://github.com/LykxSassinator)
    - 新增 PD Client 连接重试过程中的 backoff 机制。异常错误重试期间，逐步增加重试时间间隔，减小 PD 压力 [#15428](https://github.com/tikv/tikv/issues/15428) @[nolouch](https://github.com/nolouch)
    - 避免写 Titan manifest 文件时持有锁导致影响其他线程 [#15351](https://github.com/tikv/tikv/issues/15351) @[Connor1996](https://github.com/Connor1996)
    - 改进 Resolver 的内存使用，防止 OOM [#15458](https://github.com/tikv/tikv/issues/15458) @[overvenus](https://github.com/overvenus)

+ PD

    - 优化 PD 调用方的 backoff 机制，减少在调用失败时的 RPC 请求频率 [#6556](https://github.com/tikv/pd/issues/6556) @[nolouch](https://github.com/nolouch) @[rleungx](https://github.com/rleungx) @[HuSharp](https://github.com/HuSharp)
    - 增加 `GetRegions` 接口的 Cancel 机制，在调用方断连时及时释放 CPU 和内存资源 [#6835](https://github.com/tikv/pd/issues/6835) @[lhy1024](https://github.com/lhy1024)

+ TiFlash

    - 在 Grafana 中新增关于索引数据内存使用的监控指标 [#8050](https://github.com/pingcap/tiflash/issues/8050) @[hongyunyan](https://github.com/hongyunyan)

+ Tools

    + Backup & Restore (BR)

        - 通过设置 HTTP 客户端 `MaxIdleConns` 和 `MaxIdleConnsPerHost` 参数，增强日志备份以及 PITR 恢复任务对连接复用的支持 [#46011](https://github.com/pingcap/tidb/issues/46011) @[Leavrth](https://github.com/Leavrth)
        - 减少日志备份 `resolve lock` 的 CPU 开销 [#40759](https://github.com/pingcap/tidb/issues/40759) @[3pointer](https://github.com/3pointer)
        - 新增 restore 参数 `WaitTiflashReady`。当打开这个参数时，restore 操作将会等待 TiFlash 副本复制成功后才结束 [#43828](https://github.com/pingcap/tidb/issues/43828) [#46302](https://github.com/pingcap/tidb/issues/46302) @[3pointer](https://github.com/3pointer)

    + TiCDC

        - 优化 TiCDC 部分监控项和报警项 [#9047](https://github.com/pingcap/tiflow/issues/9047) @[asddongmen](https://github.com/asddongmen)
        - Kafka Sink 支持在消息过大时[只发送 Handle Key 数据](/ticdc/ticdc-sink-to-kafka.md#只发送-handle-key)，避免因消息大小超限导致同步任务失败 [#9680](https://github.com/pingcap/tiflow/issues/9680) @[3AceShowHand](https://github.com/3AceShowHand)
        - 优化同步 `ADD INDEX` DDL 的执行逻辑，从而不阻塞后续的 DML 语句 [#9644](https://github.com/pingcap/tiflow/issues/9644) @[sdojjy](https://github.com/sdojjy)
        - 优化 TiCDC 在故障重试时的状态展示信息 [#9483](https://github.com/pingcap/tiflow/issues/9483) @[asddongmen](https://github.com/asddongmen)

    + TiDB Data Migration (DM)

        - 对不兼容的 DDL 支持严格的乐观模式 [#9112](https://github.com/pingcap/tiflow/issues/9112) @[GMHDBJD](https://github.com/GMHDBJD)

    + TiDB Lightning

        - 将 `checksum-via-sql` 默认值修改为 `false`，提升导入任务执行性能 [#45368](https://github.com/pingcap/tidb/issues/45368) [#45094](https://github.com/pingcap/tidb/issues/45094) @[GMHDBJD](https://github.com/GMHDBJD)
        - 优化 TiDB Lightning 在导入数据阶段对 `no leader` 错误的重试逻辑 [#46253](https://github.com/pingcap/tidb/issues/46253) @[lance6716](https://github.com/lance6716)

## 错误修复

+ TiDB

    - 修复 `group_concat` 无法解析 `ORDER BY` 列的问题 [#41986](https://github.com/pingcap/tidb/issues/41986) @[AilinKid](https://github.com/AilinKid)
    - 修复某些情况下查询系统表 `INFORMATION_SCHEMA.TIKV_REGION_STATUS` 返回结果错误的问题 [#45531](https://github.com/pingcap/tidb/issues/45531) @[Defined2014](https://github.com/Defined2014)
    - 修复读取元数据时间超过一个 DDL lease 导致升级 TiDB 卡住的问题 [#45176](https://github.com/pingcap/tidb/issues/45176) @[zimulala](https://github.com/zimulala)
    - 修复执行带 CTE 的 DML 会导致 panic 的问题 [#46083](https://github.com/pingcap/tidb/issues/46083) @[winoros](https://github.com/winoros)
    - 修复交换分区时，无法检测出不符合分区定义的数据的问题 [#46492](https://github.com/pingcap/tidb/issues/46492) @[mjonss](https://github.com/mjonss)
    - 修复 `MERGE_JOIN` 的结果错误的问题 [#46580](https://github.com/pingcap/tidb/issues/46580) @[qw4990](https://github.com/qw4990)
    - 修复无符号类型与 `Duration` 类型常量比较时产生的结果错误 [#45410](https://github.com/pingcap/tidb/issues/45410) @[wshwsh12](https://github.com/wshwsh12)
    - 修复 `AUTO_ID_CACHE=1` 时可能导致 `Duplicate entry` 的问题 [#46444](https://github.com/pingcap/tidb/issues/46444) @[tiancaiamao](https://github.com/tiancaiamao)
    - 修复 TTL 运行过程中内存泄漏的问题 [#45510](https://github.com/pingcap/tidb/issues/45510) @[lcwangchao](https://github.com/lcwangchao)
    - 修复 kill 连接之后可能会出现 go coroutine 泄露的问题 [#46034](https://github.com/pingcap/tidb/issues/46034) @[pingyu](https://github.com/pingyu)
    - 修复 Index Join 出错可能导致查询卡住的问题 [#45716](https://github.com/pingcap/tidb/issues/45716) @[wshwsh12](https://github.com/wshwsh12)
    - 修复 `BatchPointGet` 算子在 Hash 分区表下执行结果错误的问题 [#46779](https://github.com/pingcap/tidb/issues/46779) @[jiyfhust](https://github.com/jiyfhust)
    - 修复在交换分区失败或被取消时，分区表的限制残留在原表上的问题 [#45920](https://github.com/pingcap/tidb/issues/45920) [#45791](https://github.com/pingcap/tidb/issues/45791) @[mjonss](https://github.com/mjonss)
    - 修复当 JOIN 两个子查询时执行 `TIDB_INLJ` Hint 不生效的问题 [#46160](https://github.com/pingcap/tidb/issues/46160) @[qw4990](https://github.com/qw4990)
    - 修复 `DATETIME` 或 `TIMESTAMP` 列与数字值比较时，行为与 MySQL 不一致的问题 [#38361](https://github.com/pingcap/tidb/issues/38361) @[yibin87](https://github.com/yibin87)
    - 修复深嵌套的表达式的 HashCode 重复计算导致的高内存占用和 OOM 问题 [#42788](https://github.com/pingcap/tidb/issues/42788) @[AilinKid](https://github.com/AilinKid)
    - 修复 access path 的启发式规则会忽略 `READ_FROM_STORAGE(TIFLASH[...])` Hint 导致 `Can't find a proper physical plan` 的问题 [#40146](https://github.com/pingcap/tidb/issues/40146) @[AilinKid](https://github.com/AilinKid)
    - 修复 `cast(col)=range` 条件在 CAST 无精度损失的情况下会导致 FullScan 的问题 [#45199](https://github.com/pingcap/tidb/issues/45199) @[AilinKid](https://github.com/AilinKid)
    - 修复 `plan replayer dump explain` 会报错的问题 [#46197](https://github.com/pingcap/tidb/issues/46197) @[time-and-fate](https://github.com/time-and-fate)
    - 修复 `tmp-storage-quota` 配置无法生效的问题 [#45161](https://github.com/pingcap/tidb/issues/45161) [#26806](https://github.com/pingcap/tidb/issues/26806) @[wshwsh12](https://github.com/wshwsh12)
    - 修复 TiDB parser 状态残留导致解析失败的问题 [#45898](https://github.com/pingcap/tidb/issues/45898) @[qw4990](https://github.com/qw4990)
    - 修复 MPP 执行计划中通过 Union 下推 Aggregation 导致的结果错误 [#45850](https://github.com/pingcap/tidb/issues/45850) @[AilinKid](https://github.com/AilinKid)
    - 修复 `AUTO_ID_CACHE=1` 时 TiDB panic 后恢复过慢的问题 [#46454](https://github.com/pingcap/tidb/issues/46454) @[tiancaiamao](https://github.com/tiancaiamao)
    - 修复 Sort 算子在落盘过程中可能导致 TiDB 崩溃的问题 [#47538](https://github.com/pingcap/tidb/issues/47538) @[windtalker](https://github.com/windtalker)
    - 修复使用 BR 恢复 `AUTO_ID_CACHE=1` 的非聚簇索引表时发生重复主键的问题 [#46093](https://github.com/pingcap/tidb/issues/46093) @[tiancaiamao](https://github.com/tiancaiamao)
    - 修复在静态裁剪模式下查询分区表且查询计划中带有 `IndexLookUp` 时可能报错的问题 [#45757](https://github.com/pingcap/tidb/issues/45757) @[Defined2014](https://github.com/Defined2014)
    - 修复在对分区表和有 Placement Policy 的表进行分区交换后，往分区表中插入数据可能失败的问题 [#45791](https://github.com/pingcap/tidb/issues/45791) @[mjonss](https://github.com/mjonss)
    - 修复使用错误的时区信息对时间字段进行编码的问题 [#46033](https://github.com/pingcap/tidb/issues/46033) @[tangenta](https://github.com/tangenta)
    - 修复当 `tmp` 路径不存在时快速添加索引的 DDL 会卡住的问题 [#45456](https://github.com/pingcap/tidb/issues/45456) @[tangenta](https://github.com/tangenta)
    - 修复同时升级多个 TiDB 节点时可能阻塞升级过程的问题 [#46228](https://github.com/pingcap/tidb/issues/46228) @[zimulala](https://github.com/zimulala)
    - 修复分区表由于 split Region 使用参数有误导致 Region 打散效果差的问题 [#46135](https://github.com/pingcap/tidb/issues/46135) @[zimulala](https://github.com/zimulala)
    - 修复 TiDB 重启后 DDL 操作可能卡住的问题 [#46751](https://github.com/pingcap/tidb/issues/46751) @[wjhuang2016](https://github.com/wjhuang2016)
    - 禁止非整型聚簇索引进行 split table 操作 [#47350](https://github.com/pingcap/tidb/issues/47350) @[tangenta](https://github.com/tangenta)
    - 修复由于 MDL 处理不正确可能导致 DDL 永久阻塞的问题 [#46920](https://github.com/pingcap/tidb/issues/46920) @[wjhuang2016](https://github.com/wjhuang2016)
    - 修复表改名导致 `information_schema.columns` 中出现重复行的问题 [#47064](https://github.com/pingcap/tidb/issues/47064) @[jiyfhust](https://github.com/jiyfhust)
    - 修复 `client-go` 中 `batch-client` panic 的问题 [#47691](https://github.com/pingcap/tidb/issues/47691) @[crazycs520](https://github.com/crazycs520)
    - 修复分区表统计信息收集的内存使用超出限制时不能被及时 kill 的问题 [#45706](https://github.com/pingcap/tidb/issues/45706) @[hawkingrei](https://github.com/hawkingrei)
    - 修复查询包含 `UNHEX` 条件时结果不准确的问题 [#45378](https://github.com/pingcap/tidb/issues/45378) @[qw4990](https://github.com/qw4990)
    - 修复查询使用 `GROUP_CONCAT` 时报错 `Can't find column` 的问题 [#41957](https://github.com/pingcap/tidb/issues/41957) @[AilinKid](https://github.com/AilinKid)

+ TiKV

    - 修复 `ttl-check-poll-interval` 配置项对 RawKV API V2 不生效的问题 [#15142](https://github.com/tikv/tikv/issues/15142) @[pingyu](https://github.com/pingyu)
    - 修复 raftstore-applys 不断增长的数据错误 [#15371](https://github.com/tikv/tikv/issues/15371) @[Connor1996](https://github.com/Connor1996)
    - 修复自适应同步模式下 sync-recover 阶段 QPS 下降到 0 的问题 [#14975](https://github.com/tikv/tikv/issues/14975) @[nolouch](https://github.com/nolouch)
    - 修复当一个 TiKV 节点被隔离而另一个节点重启时，可能导致读取不一致的问题 [#15035](https://github.com/tikv/tikv/issues/15035) @[overvenus](https://github.com/overvenus)
    - 修复 Online Unsafe Recovery 时无法处理 merge abort 的问题 [#15580](https://github.com/tikv/tikv/issues/15580) @[v01dstar](https://github.com/v01dstar)
    - 修复 PD 和 TiKV 之间的网络中断可能导致 PITR 卡住的问题 [#15279](https://github.com/tikv/tikv/issues/15279) @[YuJuncen](https://github.com/YuJuncen)
    - 修复在执行 `FLASHBACK` 后 Region Merge 可能被阻塞的问题 [#15258](https://github.com/tikv/tikv/issues/15258) @[overvenus](https://github.com/overvenus)
    - 减少 Store 心跳重试次数，修复心跳风暴的问题 [#15184](https://github.com/tikv/tikv/issues/15184) @[nolouch](https://github.com/nolouch)
    - 修复 Online Unsafe Recovery 超时未中止的问题 [#15346](https://github.com/tikv/tikv/issues/15346) @[Connor1996](https://github.com/Connor1996)
    - 修复部分写入时加密可能导致数据损坏的问题 [#15080](https://github.com/tikv/tikv/issues/15080) @[tabokie](https://github.com/tabokie)
    - 修复由于 Region 的元数据不正确造成 TiKV panic 的问题 [#13311](https://github.com/tikv/tikv/issues/13311) @[cfzjywxk](https://github.com/cfzjywxk)
    - 修复有线上负载时，TiDB Lightning 的 Checksum Coprocessor 请求超时的问题 [#15565](https://github.com/tikv/tikv/issues/15565) @[lance6716](https://github.com/lance6716)
    - 修复在移动 Peer 时可能导致 Follower Read 性能变差的问题 [#15468](https://github.com/tikv/tikv/issues/15468) @[YuJuncen](https://github.com/YuJuncen)

+ PD

    - 修复热点 Region 在 v2 调度策略下可能不调度的问题 [#6645](https://github.com/tikv/pd/issues/6645) @[lhy1024](https://github.com/lhy1024)
    - 修复空集群下 TLS 握手导致 CPU 资源消耗过高的问题 [#6913](https://github.com/tikv/pd/issues/6913) @[nolouch](https://github.com/nolouch)
    - 修复 PD 节点间注入错误可能导致 panic 的问题 [#6858](https://github.com/tikv/pd/issues/6858) @[HuSharp](https://github.com/HuSharp)
    - 修复 Store 信息同步可能导致 PD Leader 退出卡住的问题 [#6918](https://github.com/tikv/pd/issues/6918) @[rleungx](https://github.com/rleungx)
    - 修复 Flashback 后 Region 信息没有更新的问题 [#6912](https://github.com/tikv/pd/issues/6912) @[overvenus](https://github.com/overvenus)
    - 修复 PD 退出时可能 panic 的问题 [#7053](https://github.com/tikv/pd/issues/7053) @[HuSharp](https://github.com/HuSharp)
    - 修复 context timeout 可能导致 `lease timeout` 的问题 [#6926](https://github.com/tikv/pd/issues/6926) @[rleungx](https://github.com/rleungx)
    - 修复 Peer 没有按照 Group 进行 scatter，可能会导致 leader 分布不均衡的问题 [#6962](https://github.com/tikv/pd/issues/6962) @[rleungx](https://github.com/rleungx)
    - 修复 pd-ctl 更新隔离级别标签不同步的问题 [#7121](https://github.com/tikv/pd/issues/7121) @[rleungx](https://github.com/rleungx)
    - 修复 `evict-leader-scheduler` 丢失配置的问题 [#6897](https://github.com/tikv/pd/issues/6897) @[HuSharp](https://github.com/HuSharp)
    - 修复 Plugin 目录、文件内容可能存在安全隐患的问题 [#7094](https://github.com/tikv/pd/issues/7094) @[HuSharp](https://github.com/HuSharp)
    - 修复开启资源管控后 DDL 可能不能保证原子性的问题 [#45050](https://github.com/pingcap/tidb/issues/45050) @[glorv](https://github.com/glorv)
    - 修复在 rule checker 选定 peer 时，unhealthy peer 无法被移除的问题 [#6559](https://github.com/tikv/pd/issues/6559) @[nolouch](https://github.com/nolouch)
    - 修复当 etcd 已经启动，但 client 尚未连接上 etcd 时，调用 client 会导致 PD panic 的问题 [#6860](https://github.com/tikv/pd/issues/6860) @[HuSharp](https://github.com/HuSharp)
    - 修复 RU 消耗小于 0 导致 PD 崩溃的问题 [#6973](https://github.com/tikv/pd/issues/6973) @[CabinfeverB](https://github.com/CabinfeverB)
    - 修复在集群规模大时 client-go 周期性更新 `min-resolved-ts` 可能造成 PD OOM 的问题 [#46664](https://github.com/pingcap/tidb/issues/46664) @[HuSharp](https://github.com/HuSharp)

+ TiFlash

    - 修复 MemoryTracker 提供的内存使用数据不准确的问题 [#8128](https://github.com/pingcap/tiflash/issues/8128) @[JinheLin](https://github.com/JinheLin)
    - 修复由于 Region 的边界的 Key 不合法导致 TiFlash 数据不一致的问题 [#7762](https://github.com/pingcap/tiflash/issues/7762) @[lidezhu](https://github.com/lidezhu)
    - 修复在更改 `DATETIME`、`TIMESTAMP`、`TIME` 数据类型的 `fsp` 之后查询失败的问题 [#7809](https://github.com/pingcap/tiflash/issues/7809) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复当同一个 MPP Task 内有多个 HashAgg 算子时，可能导致 MPP Task 编译时间过长而严重影响查询性能的问题 [#7810](https://github.com/pingcap/tiflash/issues/7810) @[SeaRise](https://github.com/SeaRise)

+ Tools

    + Backup & Restore (BR)

        - 修复 PITR 恢复隐式主键可能冲突的问题 [#46520](https://github.com/pingcap/tidb/issues/46520) @[3pointer](https://github.com/3pointer)
        - 修复 GCS 上 PITR 恢复失败的问题 [#47022](https://github.com/pingcap/tidb/issues/47022) @[Leavrth](https://github.com/Leavrth)
        - 修复 RawKV 模式下细粒度备份阶段可能出错的问题 [#37085](https://github.com/pingcap/tidb/issues/37085) @[pingyu](https://github.com/pingyu)
        - 修复 PITR 恢复数据元信息 (meta-kv) 出错的问题 [#46578](https://github.com/pingcap/tidb/issues/46578) @[Leavrth](https://github.com/Leavrth)
        - 修复 BR 集成测试用例出错的问题 [#46561](https://github.com/pingcap/tidb/issues/46561) @[purelind](https://github.com/purelind)
        - 将 BR 使用的全局参数 `TableColumnCountLimit` 和 `IndexLimit` 的默认值提升到最大值，修复恢复过程失败的问题 [#45793](https://github.com/pingcap/tidb/issues/45793) @[Leavrth](https://github.com/Leavrth)
        - 修复 br CLI 客户端扫描恢复后的数据时卡住的问题 [#45476](https://github.com/pingcap/tidb/issues/45476) @[3pointer](https://github.com/3pointer)
        - 修复 PITR 可能跳过恢复 `CREATE INDEX` DDL 的问题 [#47482](https://github.com/pingcap/tidb/issues/47482) @[Leavrth](https://github.com/Leavrth)
        - 修复 1 分钟之内多次执行 PITR 可能导致数据丢失的问题 [#15483](https://github.com/tikv/tikv/issues/15483) @[YuJuncen](https://github.com/YuJuncen)

    + TiCDC

        - 修复处于异常状态的同步任务阻塞上游 GC 的问题 [#9543](https://github.com/pingcap/tiflow/issues/9543) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - 修复同步到对象存储可能导致数据不一致的问题 [#9592](https://github.com/pingcap/tiflow/issues/9592) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - 修复开启 `redo-resolved-ts` 可能导致 Changefeed 失败的问题 [#9769](https://github.com/pingcap/tiflow/issues/9769) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - 修复在某些特殊的操作系统下，获取错误内存信息可能导致 OOM 的问题 [#9762](https://github.com/pingcap/tiflow/issues/9762) @[sdojjy](https://github.com/sdojjy)
        - 修复开启 `scale-out` 时流量在节点间分配不均匀问题 [#9665](https://github.com/pingcap/tiflow/issues/9665) @[sdojjy](https://github.com/sdojjy)
        - 修复日志中记录了用户敏感信息的问题 [#9690](https://github.com/pingcap/tiflow/issues/9690) @[sdojjy](https://github.com/sdojjy)
        - 修复可能无法正确同步 rename DDL 操作的问题 [#9488](https://github.com/pingcap/tiflow/issues/9488) [#9378](https://github.com/pingcap/tiflow/issues/9378) [#9531](https://github.com/pingcap/tiflow/issues/9531) @[asddongmen](https://github.com/asddongmen)
        - 修复所有 changefeed 被移除时会阻塞上游 TiDB GC 的问题 [#9633](https://github.com/pingcap/tiflow/issues/9633) @[sdojjy](https://github.com/sdojjy)
        - 修复 TiCDC 同步任务在某些特殊场景可能失败的问题 [#9685](https://github.com/pingcap/tiflow/issues/9685) [#9697](https://github.com/pingcap/tiflow/issues/9697) [#9695](https://github.com/pingcap/tiflow/issues/9695) [#9736](https://github.com/pingcap/tiflow/issues/9736) @[hicqu](https://github.com/hicqu) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - 修复 PD 节点出现网络隔离时引起 TiCDC 同步延时变高的问题 [#9565](https://github.com/pingcap/tiflow/issues/9565) @[asddongmen](https://github.com/asddongmen)
        - 修复 PD 做扩缩容场景下 TiCDC 访问无效旧地址的问题 [#9584](https://github.com/pingcap/tiflow/issues/9584) @[fubinzh](https://github.com/fubinzh) @[asddongmen](https://github.com/asddongmen)
        - 修复上游在 Region 非常多时，TiKV 节点出现故障导致 TiCDC 同步任务不能快速恢复的问题 [#9741](https://github.com/pingcap/tiflow/issues/9741) @[sdojjy](https://github.com/sdojjy)
        - 修复采用 CSV 格式时将 `UPDATE` 操作错误修改为 `INSERT` 的问题 [#9658](https://github.com/pingcap/tiflow/issues/9658) @[3AceShowHand](https://github.com/3AceShowHand)
        - 修复在上游同一条 DDL 中重命名多个表的场景下同步出错的问题 [#9476](https://github.com/pingcap/tiflow/issues/9476) [#9488](https://github.com/pingcap/tiflow/issues/9488) @[CharlesCheung96](https://github.com/CharlesCheung96) @[asddongmen](https://github.com/asddongmen)
        - 修复同步到 Kafka 时重试间隔过短导致同步任务失败的问题 [#9504](https://github.com/pingcap/tiflow/issues/9504) @[3AceShowHand](https://github.com/3AceShowHand)
        - 修复在上游同一个事务中修改多行唯一键场景下，TiCDC 可能导致同步写冲突的问题 [#9430](https://github.com/pingcap/tiflow/issues/9430) @[sdojjy](https://github.com/sdojjy)
        - 修复下游发生短时间故障导致同步任务卡住的问题 [#9542](https://github.com/pingcap/tiflow/issues/9542) [#9272](https://github.com/pingcap/tiflow/issues/9272) [#9582](https://github.com/pingcap/tiflow/issues/9582) [#9592](https://github.com/pingcap/tiflow/issues/9592) @[hicqu](https://github.com/hicqu)
        - 修复下游发生故障重试时同步任务可能卡住的问题 [#9450](https://github.com/pingcap/tiflow/issues/9450) @[hicqu](https://github.com/hicqu)

    + TiDB Data Migration (DM)

        - 修复 DM 在跳过失败 DDL 并且后续无 DDL 执行时显示延迟持续增长的问题 [#9605](https://github.com/pingcap/tiflow/issues/9605) @[D3Hunter](https://github.com/D3Hunter)
        - 修复 DM 在大小写不敏感的 collation 下无法正确处理冲突的问题 [#9489](https://github.com/pingcap/tiflow/issues/9489) @[hihihuhu](https://github.com/hihihuhu)
        - 修复 DM validator 死锁问题并增强重试 [#9257](https://github.com/pingcap/tiflow/issues/9257) @[D3Hunter](https://github.com/D3Hunter)
        - 修复 DM 在乐观模式恢复任务时跳过所有 DML 的问题 [#9588](https://github.com/pingcap/tiflow/issues/9588) @[GMHDBJD](https://github.com/GMHDBJD)
        - 修复 DM 在跳过 Online DDL 时无法正确追踪上游表结构的问题 [#9587](https://github.com/pingcap/tiflow/issues/9587) @[GMHDBJD](https://github.com/GMHDBJD)
        - 修复 DM 在乐观模式中跳过 Partition DDL 的问题 [#9788](https://github.com/pingcap/tiflow/issues/9788) @[GMHDBJD](https://github.com/GMHDBJD)

    + TiDB Lightning

        - 修复导入表设置 `AUTO_ID_CACHE=1` 会导致分配错误的 `row_id` 的问题 [#46100](https://github.com/pingcap/tidb/issues/46100) @[D3Hunter](https://github.com/D3Hunter)
        - 修复保存 `NEXT_GLOBAL_ROW_ID` 时类型错误问题 [#45427](https://github.com/pingcap/tidb/issues/45427) @[lyzx2001](https://github.com/lyzx2001)
        - 修复 `checksum = "optional"` 时 Checksum 阶段仍然报错的问题 [#45382](https://github.com/pingcap/tidb/issues/45382) @[lyzx2001](https://github.com/lyzx2001)
        - 修复当 PD 集群地址变更时数据导入失败的问题 [#43436](https://github.com/pingcap/tidb/issues/43436) @[lichunzhu](https://github.com/lichunzhu)
        - 修复 TiDB Lightning 在 PD 拓扑变更时无法启动的问题 [#46688](https://github.com/pingcap/tidb/issues/46688) @[lance6716](https://github.com/lance6716)
        - 修复导入 CSV 数据时，route 可能 panic 的问题 [#43284](https://github.com/pingcap/tidb/issues/43284) @[lyzx2001](https://github.com/lyzx2001)

    + TiDB Binlog

        - 修复传输事务超过 1 GB 时 Drainer 会退出的问题 [#28659](https://github.com/pingcap/tidb/issues/28659) @[jackysp](https://github.com/jackysp)