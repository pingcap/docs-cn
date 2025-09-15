---
title: TiDB 8.5.2 Release Notes
summary: 了解 TiDB 8.5.2 版本的改进提升和错误修复。
---

# TiDB 8.5.2 Release Notes

发版日期：2025 年 6 月 12 日

TiDB 版本：8.5.2

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v8.5/quick-start-with-tidb) | [生产部署](https://docs.pingcap.com/zh/tidb/v8.5/production-deployment-using-tiup) | [下载离线包](https://cn.pingcap.com/product-community/?version=v8.5.2#version-list)

## 改进提升

+ TiDB

    - 将 TTL 表的 GC 及相关统计信息收集任务限定在 owner 节点执行，从而降低开销 [#59357](https://github.com/pingcap/tidb/issues/59357) @[lcwangchao](https://github.com/lcwangchao)

+ TiKV

    - 支持在线修改 `import.num-threads` 配置项 [#17807](https://github.com/tikv/tikv/issues/17807) @[RidRisR](https://github.com/RidRisR)

+ Tools

    + Backup & Restore (BR)

        - 移除对 AWS region 名称的检查，避免新支持的 AWS region 因无法通过检查而导致备份报错的问题 [#18159](https://github.com/tikv/tikv/issues/18159) @[3pointer](https://github.com/3pointer)

    + TiDB Lightning

        - 在解析 CSV 文件时，新增行宽检查以防止 OOM 问题 [#58590](https://github.com/pingcap/tidb/issues/58590) @[D3Hunter](https://github.com/D3Hunter)

## 错误修复

+ TiDB

    - 修复设置 `zone` 标签后，验证时间戳的过程中获取 TSO 失败的问题 [#59402](https://github.com/pingcap/tidb/issues/59402) @[ekexium](https://github.com/ekexium)
    - 修复当 Hash Join 执行出错时，返回错误结果但未报错的问题 [#59377](https://github.com/pingcap/tidb/issues/59377) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - 修复 TiFlash 可能崩溃或返回错误结果的问题 [#60517](https://github.com/pingcap/tidb/issues/60517) @[wintalker](https://github.com/wintalker)
    - 修复当 `ORDER BY` 进行并行排序遇到错误或者查询被取消时，执行卡住的问题 [#59655](https://github.com/pingcap/tidb/issues/59655) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - 修复在查询包含生成列的分区表时报错的问题 [#58475](https://github.com/pingcap/tidb/issues/58475) @[joechenrh](https://github.com/joechenrh)
    - 修复创建两个相同名称的视图而没有报错的问题 [#58769](https://github.com/pingcap/tidb/issues/58769) @[tiancaiamao](https://github.com/tiancaiamao)
    - 修复 Join 的等值条件两边数据类型不同，可能导致 TiFlash 产生错误结果的问题 [#59877](https://github.com/pingcap/tidb/issues/59877) @[yibin87](https://github.com/yibin87)
    - 修复 Hash 类型分区表在查询 `is null` 条件时 panic 的问题 [#58374](https://github.com/pingcap/tidb/issues/58374) @[Defined2014](https://github.com/Defined2014/)
    - 修复当集群中存在存算分离架构 TiFlash 节点时，执行 `ALTER TABLE ... PLACEMENT POLICY ...` 之后，Region peer 可能会被意外地添加到 TiFlash Compute 节点的问题 [#58633](https://github.com/pingcap/tidb/issues/58633) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复手动加载统计信息时，统计信息文件中包含 null 可能导致加载失败的问题 [#53966](https://github.com/pingcap/tidb/issues/53966) @[King-Dylan](https://github.com/King-Dylan)
    - 修复 TTL 任务可能被忽略或处理多次的问题 [#59347](https://github.com/pingcap/tidb/issues/59347) @[YangKeao](https://github.com/YangKeao)
    - 修复 exchange partition 错误判断导致执行失败的问题 [#59534](https://github.com/pingcap/tidb/issues/59534) @[mjonss](https://github.com/mjonss)
    - 修复对统计信息的异常处理不当导致后台任务超时的时候，内存内的统计信息被误删除的问题 [#57901](https://github.com/pingcap/tidb/issues/57901) @[hawkingrei](https://github.com/hawkingrei)
    - 修复 Grafana 中 **Stats Healthy Distribution** 面板的数据可能错误的问题 [#57176](https://github.com/pingcap/tidb/issues/57176) @[hawkingrei](https://github.com/hawkingrei)
    - 修复被取消的 TTL 任务可能会将未提交的 Session 放到全局 Session 池的问题 [#58900](https://github.com/pingcap/tidb/issues/58900) @[YangKeao](https://github.com/YangKeao)
    - 修复 Redact 日志开启后在部分场景不生效的问题 [#59279](https://github.com/pingcap/tidb/issues/59279) @[tangenta](https://github.com/tangenta)
    - 修复 `rowContainer` 在部分场景下会导致 TiDB panic 的问题 [#59976](https://github.com/pingcap/tidb/issues/59976) @[YangKeao](https://github.com/YangKeao)
    - 修复分区表在 `Point_Get` 场景下可能会出现分区裁剪错误的问题 [#59827](https://github.com/pingcap/tidb/issues/59827) @[mjonss](https://github.com/mjonss)
    - 修复在 DDL 执行过程中更新分区表记录可能会导致数据错误的问题 [#57588](https://github.com/pingcap/tidb/issues/57588) @[Defined2014](https://github.com/Defined2014)
    - 修复部分场景下 `information_schema` 的性能和稳定性受到影响的问题 [#58142](https://github.com/pingcap/tidb/issues/58142) [#58363](https://github.com/pingcap/tidb/issues/58363) [#58712](https://github.com/pingcap/tidb/issues/58712) @[tiancaiamao](https://github.com/tiancaiamao)
    - 修复在启用分布式执行框架 (Distributed eXecution Framework, DXF) 时，TiDB 内部会话中的 `tidb_txn_entry_size_limit` 不能动态调整的问题 [#59506](https://github.com/pingcap/tidb/issues/59506) @[D3Hunter](https://github.com/D3Hunter)
    - 修复在全局排序配置下，数据导入功能 `IMPORT INTO` 不能正确处理唯一键冲突的问题 [#59650](https://github.com/pingcap/tidb/issues/59650) @[lance6716](https://github.com/lance6716)
    - 修复在全局排序数据路径上注入网络延迟故障导致执行 `IMPORT INTO` 失败的问题 [#50451](https://github.com/pingcap/tidb/issues/50451) @[D3Hunter](https://github.com/D3Hunter) 
    - 修复执行 `ADD UNIQUE INDEX` 可能导致数据不一致的问题  [#60339](https://github.com/pingcap/tidb/issues/60339) @[tangenta](https://github.com/tangenta)
    - 修复查询 `INFORMATION_SCHEMA.TIDB_SERVERS_INFO` 时，`LABELS` 列的值错误显示在 `BINLOG_STATUS` 列中的问题 [#59245](https://github.com/pingcap/tidb/issues/59245) @[lance6716](https://github.com/lance6716)
    - 修复在添加索引操作时，注入 kill PD Leader 故障可能导致数据不一致的问题 [#59701](https://github.com/pingcap/tidb/issues/59701) @[tangenta](https://github.com/tangenta)
    - 修复在创建约 650 万张表后 TiDB OOM 的问题 [#58368](https://github.com/pingcap/tidb/issues/58368) @[lance6716](https://github.com/lance6716)
    - 修复开启全局排序功能后，导入大量数据时新增唯一键 (Unique Key) 可能会失败的问题 [#59725](https://github.com/pingcap/tidb/issues/59725) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - 修复 TiDB 访问 S3 外部存储报错后，错误信息不可读的问题 [#59326](https://github.com/pingcap/tidb/issues/59326) @[lance6716](https://github.com/lance6716)
    - 修复查询 `information_schema.tables` 时，返回结果中 `table_schema` 和 `table_name` 不匹配的问题 [#60593](https://github.com/pingcap/tidb/issues/60593) @[tangenta](https://github.com/tangenta)
    - 修复当内部 SQL 提交失败时，DDL notifier 可能无法正确转达的问题 [#59055](https://github.com/pingcap/tidb/issues/59055) @[lance6716](https://github.com/lance6716)
    - 修复当数据分片 Region 大小为 256 MiB 时，`ADD INDEX` DDL 在开启全局排序功能后仍按 96 MiB 切分 SST 文件的问题 [#59962](https://github.com/pingcap/tidb/issues/59962) @[D3Hunter](https://github.com/D3Hunter)
    - 修复在开启全局排序功能并导入数据时，内存使用超过 80% 后 TiDB server 发生 OOM 的问题 [#59508](https://github.com/pingcap/tidb/issues/59508) @[D3Hunter](https://github.com/D3Hunter)

+ TiKV

    - 修复 `txn_status_cache` 中可能出现死锁的问题 [#18384](https://github.com/tikv/tikv/issues/18384) @[ekexium](https://github.com/ekexium)
    - 修复 Resolved-TS 监控和日志可能显示异常的问题 [#17989](https://github.com/tikv/tikv/issues/17989) @[ekexium](https://github.com/ekexium)
    - 修复 Region 合并时可能因 Raft index 匹配异常而导致 TiKV 异常退出的问题 [#18129](https://github.com/tikv/tikv/issues/18129) @[glorv](https://github.com/glorv)
    - 修复磁盘卡住时，TiKV 无法向 PD 上报心跳的问题 [#17939](https://github.com/tikv/tikv/issues/17939) @[LykxSassinator](https://github.com/LykxSassinator)
    - 修复 GC Worker 负载过高时可能出现的死锁问题 [#18214](https://github.com/tikv/tikv/issues/18214) @[zyguan](https://github.com/zyguan)
    - 修复时钟回退导致 RocksDB 流控异常，进而引发性能抖动的问题 [#17995](https://github.com/tikv/tikv/issues/17995) @[LykxSassinator](https://github.com/LykxSassinator)
    - 修复 CDC 连接在遇到异常时可能发生资源泄漏的问题 [#18245](https://github.com/tikv/tikv/issues/18245) @[wlwilliamx](https://github.com/wlwilliamx)
    - 修复 Region Split 后可能无法快速选出 Leader 的问题 [#17602](https://github.com/tikv/tikv/issues/17602) @[LykxSassinator](https://github.com/LykxSassinator)
    - 修复在仅启用一阶段提交 (1PC) 而未启用异步提交 (Async Commit) 时，可能无法读取最新写入数据的问题 [#18117](https://github.com/tikv/tikv/issues/18117) @[zyguan](https://github.com/zyguan)
    - 修复 GC Worker 意外打印错误日志的问题 [#18213](https://github.com/tikv/tikv/issues/18213) @[ekexium](https://github.com/ekexium)

+ PD

    - 修复在启用微服务的场景中，转发 TSO 可能引起的并发问题 [#9091](https://github.com/tikv/pd/issues/9091) @[lhy1024](https://github.com/lhy1024)
    - 修复调用 `BatchScanRegions` 时，返回结果未被正确限制的问题 [#9216](https://github.com/tikv/pd/issues/9216) @[lhy1024](https://github.com/lhy1024)
    - 修复 follower 发生网络隔离时，触发非预期选举的问题 [#9020](https://github.com/tikv/pd/issues/9020) @[lhy1024](https://github.com/lhy1024)
    - 修复当资源管控中存在 `QUERY_LIMIT` 时，无法触发 `COOLDOWN` 或 `SWITCH_GROUP` 的问题 [#60404](https://github.com/pingcap/tidb/issues/60404) @[JmPotato](https://github.com/JmPotato)
    - 修复 `StoreInfo` 可能存在错误覆盖的问题 [#9185](https://github.com/tikv/pd/issues/9185) @[okJiang](https://github.com/okJiang)
    - 修复在导入或添加索引场景中，因 PD 网络不稳定可能导致操作失败的问题 [#8962](https://github.com/tikv/pd/issues/8962) @[okJiang](https://github.com/okJiang)
    - 修复单个日志文件 `max-size` 默认值未被正确设置的问题 [#9037](https://github.com/tikv/pd/issues/9037) @[rleungx](https://github.com/rleungx)
    - 修复 TSO 分配过程中可能出现的内存泄漏问题 [#9004](https://github.com/tikv/pd/issues/9004) @[rleungx](https://github.com/rleungx)
    - 修复设置 `tidb_enable_tso_follower_proxy` 系统变量可能不生效的问题 [#8947](https://github.com/tikv/pd/issues/8947) @[JmPotato](https://github.com/JmPotato)
    - 修复当某个 PD 节点不是 Leader 时，仍可能生成 TSO 的问题 [#9051](https://github.com/tikv/pd/issues/9051) @[rleungx](https://github.com/rleungx)
    - 修复 PD Leader 切换过程中，Region syncer 未能及时退出的问题 [#9017](https://github.com/tikv/pd/issues/9017) @[rleungx](https://github.com/rleungx)
    - 修复 `lease` 默认值未被正确设置的问题 [#9156](https://github.com/tikv/pd/issues/9156) @[rleungx](https://github.com/rleungx)

+ TiFlash

    - 修复排序过程中发生数据落盘可能导致 TiFlash 崩溃的问题 [#9999](https://github.com/pingcap/tiflash/issues/9999) @[windtalker](https://github.com/windtalker)
    - 修复执行包含 `GROUP BY ... WITH ROLLUP` 的 SQL 语句时，可能会出现 `Exception: Block schema mismatch` 报错的问题 [#10110](https://github.com/pingcap/tiflash/issues/10110) @[gengliqi](https://github.com/gengliqi)
    - 修复在存算分离架构下，TiFlash 计算节点可能被错误选为添加 Region peer 的目标节点的问题 [#9750](https://github.com/pingcap/tiflash/issues/9750) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复在某些情况下 TiFlash 意外退出时无法打印错误堆栈的问题 [#9902](https://github.com/pingcap/tiflash/issues/9902) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复在导入大量数据后，TiFlash 可能持续占用较高内存的问题 [#9812](https://github.com/pingcap/tiflash/issues/9812) @[CalvinNeo](https://github.com/CalvinNeo)
    - 修复当 `profiles.default.init_thread_count_scale` 设置为 `0` 时，TiFlash 启动可能会卡住的问题 [#9906](https://github.com/pingcap/tiflash/issues/9906) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复在分区表上执行 `ALTER TABLE ... RENAME COLUMN` 后，查询该表可能报错的问题 [#9787](https://github.com/pingcap/tiflash/issues/9787) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - 修复在查询涉及虚拟列并且触发远程读时，可能会出现 `Not found column` 错误的问题 [#9561](https://github.com/pingcap/tiflash/issues/9561) @[guo-shaoge](https://github.com/guo-shaoge)
    - 修复当集群的表中存在大量 `ENUM` 类型列时，TiFlash 的内存可能会大量消耗问题 [#9947](https://github.com/pingcap/tiflash/issues/9947) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复插入单行超过 16 MiB 的数据后，TiFlash 可能无法正常重启的问题 [#10052](https://github.com/pingcap/tiflash/issues/10052) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复在包含向量索引的表中插入数据后，部分磁盘数据可能无法被正确清理从而导致磁盘空间异常占用的问题 [#9946](https://github.com/pingcap/tiflash/issues/9946) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复在同一个表上创建多个向量索引后，先前创建的向量索引可能被意外删除而导致性能下降的问题 [#9971](https://github.com/pingcap/tiflash/issues/9971) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - 修复在存算分离架构下，TiFlash 无法利用向量索引加速向量搜索查询的问题 [#9847](https://github.com/pingcap/tiflash/issues/9847) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - 修复在存算分离架构下，可能会产生大量 `tag=EnumParseOverflowContainer` 日志的问题 [#9955](https://github.com/pingcap/tiflash/issues/9955) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复执行 `SELECT ... AS OF TIMESTAMP` 查询时，TiFlash 未按预期跳过 Learner Read 的问题 [#10046](https://github.com/pingcap/tiflash/issues/10046) @[CalvinNeo](https://github.com/CalvinNeo)
    - 修复 TiFlash 处理带有不规则 key-range 的 Region snapshot 时可能 panic 的问题 [#10147](https://github.com/pingcap/tiflash/issues/10147) @[JaySon-Huang](https://github.com/JaySon-Huang)

+ Tools

    + Backup & Restore (BR)

        - 修复在极端情况下，数据恢复过程中重复下载 SST 文件导致 TiKV panic 的问题 [#18335](https://github.com/tikv/tikv/issues/18335) @[3pointer](https://github.com/3pointer)
        - 修复使用 `br log status --json` 查询日志备份任务时，返回结果中缺少任务状态 `status` 字段的问题 [#57959](https://github.com/pingcap/tidb/issues/57959) @[Leavrth](https://github.com/Leavrth)
        - 修复 BR 向 TiKV 发送请求时收到 `rpcClient is idle` 错误导致恢复失败的问题 [#58845](https://github.com/pingcap/tidb/issues/58845) @[Tristan1900](https://github.com/Tristan1900)
        - 修复日志备份在无法访问 PD 时，遇到致命错误无法正确退出的问题 [#18087](https://github.com/tikv/tikv/issues/18087) @[YuJuncen](https://github.com/YuJuncen)
        - 修复 PITR 无法恢复大于 3072 字节的索引的问题 [#58430](https://github.com/pingcap/tidb/issues/58430) @[YuJuncen](https://github.com/YuJuncen)

    + TiCDC

        - 修复同步流量超过了下游 Kafka 的流量阀值后，Changefeed 可能会卡住的问题 [#12110](https://github.com/pingcap/tiflow/issues/12110) @[3AceShowHand](https://github.com/3AceShowHand)
        - 修复使用 `pulsar+http` 或者 `pulsar+https` 协议时，Kafka Sink 的分发规则不生效的问题 [#12068](https://github.com/pingcap/tiflow/issues/12068) @[SandeepPadhi](https://github.com/SandeepPadhi)
        - 修复切换 PD leader 后，TiCDC 未能及时发现从而导致同步延迟升高的问题 [#11997](https://github.com/pingcap/tiflow/issues/11997) @[lidezhu](https://github.com/lidezhu)
        - 修复 TiCDC 通过 Avro 协议同步 `default NULL` SQL 语句时报错的问题 [#11994](https://github.com/pingcap/tiflow/issues/11994) @[wk989898](https://github.com/wk989898)
        - 修复当上游将一个新增的列的默认值从 `NOT NULL` 修改为 `NULL` 后，下游默认值错误的问题 [#12037](https://github.com/pingcap/tiflow/issues/12037) @[wk989898](https://github.com/wk989898)
        - 修复 PD 缩容后 TiCDC 无法正确连接 PD 的问题 [#12004](https://github.com/pingcap/tiflow/issues/12004) @[lidezhu](https://github.com/lidezhu)
        - 修复 TiCDC 同步 `CREATE TABLE IF NOT EXISTS` 或 `CREATE DATABASE IF NOT EXISTS` 语句时可能出现 panic 的问题 [#11839](https://github.com/pingcap/tiflow/issues/11839) @[CharlesCheung96](https://github.com/CharlesCheung96)

    + TiDB Data Migration (DM)

        - 修复当同时配置 TLS 和 `shard-mode` 时，`start-task` 会在前置检查中报错的问题 [#11842](https://github.com/pingcap/tiflow/issues/11842) @[sunxiaoguang](https://github.com/sunxiaoguang)

    + TiDB Lightning

        - 修复在高并发场景下，从云存储导入数据时性能下降的问题 [#57413](https://github.com/pingcap/tidb/issues/57413) @[xuanyu66](https://github.com/xuanyu66)
        - 修复使用 TiDB Lightning 导入数据时，错误报告输出被截断的问题 [#58085](https://github.com/pingcap/tidb/issues/58085) @[lance6716](https://github.com/lance6716)
        - 修复日志没有正确脱敏的问题 [#59086](https://github.com/pingcap/tidb/issues/59086) @[GMHDBJD](https://github.com/GMHDBJD)
        - 修复当使用外部账号执行 GCS 存储操作时，鉴权会失败并且报 `context canceled` 错误的问题 [#60155](https://github.com/pingcap/tidb/issues/60155) @[lance6716](https://github.com/lance6716)
        - 修复将 Parquet 文件从云存储导入到 TiDB 时，TiDB Lightning 可能会卡住达数小时的问题 [#60224](https://github.com/pingcap/tidb/issues/60224) @[joechenrh](https://github.com/joechenrh)
        - 修复当导入大量数据时，在 write 或 ingest SST 文件到 TiKV 集群期间，TiDB Lightning 可能会 OOM 的问题 [#59947](https://github.com/pingcap/tidb/issues/59947) @[OliverS929](https://github.com/OliverS929)
        - 修复 TiDB Lightning 建表的最大 QPS 过低且访问 `information_schema.tables` 变慢，导致在百万张表场景下 TiDB Lightning 调度任务运行缓慢的问题 [#58141](https://github.com/pingcap/tidb/issues/58141) @[D3Hunter](https://github.com/D3Hunter)

    + NG Monitoring

        - 修复 DocDB 在高负载下内存占用高的问题，以 SQLite 作为 DocDB 的可选后端 [#267](https://github.com/pingcap/ng-monitoring/issues/267) @[mornyx](https://github.com/mornyx)
        - 修复 TSDB 在高时序基数下内存占用高的问题，提供 TSDB 内存配置项 [#295](https://github.com/pingcap/ng-monitoring/issues/295) @[mornyx](https://github.com/mornyx)
