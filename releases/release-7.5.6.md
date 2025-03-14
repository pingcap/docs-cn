---
title: TiDB 7.5.6 Release Notes
summary: 了解 TiDB 7.5.6 版本的兼容性变更、改进提升，以及错误修复。
---

# TiDB 7.5.6 Release Notes

发版日期：2025 年 3 月 14 日

TiDB 版本：7.5.6

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v7.5/quick-start-with-tidb) | [生产部署](https://docs.pingcap.com/zh/tidb/v7.5/production-deployment-using-tiup) | [下载离线包](https://cn.pingcap.com/product-community/?version=v7.5.6#version-list)

## 兼容性变更

- 支持 openEuler 22.03 LTS SP3/SP4 操作系统。详情请参考[操作系统及平台要求](https://docs.pingcap.com/zh/tidb/v7.5/hardware-and-software-requirements#操作系统及平台要求)。

## 改进提升

+ TiDB

    - 当某个统计信息完全由 TopN 构成，且对应表的统计信息中修改行数不为 0 时，对于未命中 TopN 的等值条件，估算结果从 0 调整为 1 [#47400](https://github.com/pingcap/tidb/issues/47400) @[terry1purcell](https://github.com/terry1purcell)
    - 增强时间戳合法性检查 [#57786](https://github.com/pingcap/tidb/issues/57786) @[MyonKeminta](https://github.com/MyonKeminta)
    - 将 TTL 表的 GC 及相关统计信息收集任务限定在 owner 节点执行，从而降低开销 [#59357](https://github.com/pingcap/tidb/issues/59357) @[lcwangchao](https://github.com/lcwangchao)

+ TiKV

    - 增加对非法 `max_ts` 更新的检测机制 [#17916](https://github.com/tikv/tikv/issues/17916) @[ekexium](https://github.com/ekexium)
    - 增加 peer 和 store 消息的 slow log [#16600](https://github.com/tikv/tikv/issues/16600) @[Connor1996](https://github.com/Connor1996)
    - 优化 TiKV 重启时由于需要等待应用之前的日志而造成访问延时抖动的情况，提升了 TiKV 的稳定性 [#15874](https://github.com/tikv/tikv/issues/15874) @[LykxSassinator](https://github.com/LykxSassinator)

+ TiFlash

    - 降低 TiFlash 在开启 TLS 后因更新证书而导致 panic 的概率 [#8535](https://github.com/pingcap/tiflash/issues/8535) @[windtalker](https://github.com/windtalker)

+ Tools

    + Backup & Restore (BR)

        - 在进行全量备份时，默认不计算表级别的 checksum (`--checksum=false`) 以提升备份性能 [#56373](https://github.com/pingcap/tidb/issues/56373) @[Tristan1900](https://github.com/Tristan1900)
        - 对于非全量恢复，新增对目标集群中是否存在同名表的检查 [#55087](https://github.com/pingcap/tidb/issues/55087) @[RidRisR](https://github.com/RidRisR)

    + TiDB Lightning

        - 在解析 CSV 文件时，新增行宽检查以防止 OOM 问题 [#58590](https://github.com/pingcap/tidb/issues/58590) @[D3Hunter](https://github.com/D3Hunter)

## 错误修复

+ TiDB

    - 修复在构造 `IndexMerge` 时可能丢失部分谓词的问题 [#58476](https://github.com/pingcap/tidb/issues/58476) @[hawkingrei](https://github.com/hawkingrei)
    - 修复 `ONLY_FULL_GROUP_BY` 设置对于视图中的语句不生效的问题 [#53175](https://github.com/pingcap/tidb/issues/53175) @[mjonss](https://github.com/mjonss)
    - 修复创建两个相同名称的视图而没有报错的问题 [#58769](https://github.com/pingcap/tidb/issues/58769) @[tiancaiamao](https://github.com/tiancaiamao)
    - 修复将数据从 `BIT` 类型换为 `CHAR` 类型时可能导致 TiKV 崩溃的问题 [#56494](https://github.com/pingcap/tidb/issues/56494) @[lcwangchao](https://github.com/lcwangchao)
    - 修复某个 TTL 任务丢失心跳会阻塞其他任务获取心跳的问题 [#57915](https://github.com/pingcap/tidb/issues/57915) @[YangKeao](https://github.com/YangKeao)
    - 修复查询分区表时，`IN` 条件中的值类型不匹配且转换错误，导致查询结果出错的问题 [#54746](https://github.com/pingcap/tidb/issues/54746) @[mjonss](https://github.com/mjonss)
    - 修复 `BIT` 列默认值错误的问题 [#57301](https://github.com/pingcap/tidb/issues/57301) @[YangKeao](https://github.com/YangKeao)
    - 修复在 Prepare 协议中，客户端使用非 UTF8 相关字符集报错的问题 [#58870](https://github.com/pingcap/tidb/issues/58870) @[xhebox](https://github.com/xhebox)
    - 修复在 `CREATE VIEW` 语句中使用变量或参数时未报错的问题 [#53176](https://github.com/pingcap/tidb/issues/53176) @[mjonss](https://github.com/mjonss)
    - 修复手动加载统计信息时，统计信息文件中包含 null 可能导致加载失败的问题 [#53966](https://github.com/pingcap/tidb/issues/53966) @[King-Dylan](https://github.com/King-Dylan)
    - 修复查询 `information_schema.cluster_slow_query` 表时，如果不加时间过滤条件，则只会查询最新的慢日志文件的问题 [#56100](https://github.com/pingcap/tidb/issues/56100) @[crazycs520](https://github.com/crazycs520)
    - 修复某些情况下查询临时表会产生 TiKV 请求的问题 [#58875](https://github.com/pingcap/tidb/issues/58875) @[tiancaiamao](https://github.com/tiancaiamao)
    - 修复 Grafana 中 **Stats Healthy Distribution** 面板的数据可能错误的问题 [#57176](https://github.com/pingcap/tidb/issues/57176) @[hawkingrei](https://github.com/hawkingrei)
    - 修复在修改 `tidb_ttl_delete_rate_limit` 时，部分 TTL 任务可能挂起的问题 [#58484](https://github.com/pingcap/tidb/issues/58484) @[lcwangchao](https://github.com/lcwangchao)
    - 修复对统计信息的异常处理不当导致后台任务超时的时候，内存内的统计信息被误删除的问题 [#57901](https://github.com/pingcap/tidb/issues/57901) @[hawkingrei](https://github.com/hawkingrei)
    - 修复查询 `cluster_slow_query` 表时，使用 `ORDER BY` 可能导致结果乱序的问题 [#51723](https://github.com/pingcap/tidb/issues/51723) @[Defined2014](https://github.com/Defined2014)
    - 修复虚拟生成列依赖包含 `ON UPDATE` 属性的列时，更新行的数据与其索引数据不一致问题 [#56829](https://github.com/pingcap/tidb/issues/56829) @[joechenrh](https://github.com/joechenrh)
    - 修复 TiDB 丢失心跳时，TTL 任务无法被取消的问题 [#57784](https://github.com/pingcap/tidb/issues/57784) @[YangKeao](https://github.com/YangKeao)
    - 当参数为 `Enum`、`Bit` 或 `Set` 类型时，不再将 `Conv()` 函数下推至 TiKV [#51877](https://github.com/pingcap/tidb/issues/51877) @[yibin87](https://github.com/yibin87)
    - 修复当集群中存在存算分离架构 TiFlash 节点时，执行 `ALTER TABLE ... PLACEMENT POLICY ...` 之后，Region peer 可能会被意外地添加到 TiFlash Compute 节点的问题 [#58633](https://github.com/pingcap/tidb/issues/58633) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复 DDL owner 变更时，作业状态被覆盖的问题 [#52747](https://github.com/pingcap/tidb/issues/52747) @[D3Hunter](https://github.com/D3Hunter)
    - 修复 Hash 类型分区表在查询 `is null` 条件时 panic 的问题 [#58374](https://github.com/pingcap/tidb/issues/58374) @[Defined2014](https://github.com/Defined2014/)
    - 修复在查询包含生成列的分区表时报错的问题 [#58475](https://github.com/pingcap/tidb/issues/58475) @[joechenrh](https://github.com/joechenrh)
    - 修复 TTL 任务可能被忽略或处理多次的问题 [#59347](https://github.com/pingcap/tidb/issues/59347) @[YangKeao](https://github.com/YangKeao)
    - 修复 exchange partition 错误判断导致执行失败的问题 [#59534](https://github.com/pingcap/tidb/issues/59534) @[mjonss](https://github.com/mjonss)
    - 修复 `tidb_audit_log` 变量设置多级相对路径，导致日志目录出错的问题 [#58971](https://github.com/pingcap/tidb/issues/58971) @[lcwangchao](https://github.com/lcwangchao)
    - 修复 Join 的等值条件两边数据类型不同，可能导致 TiFlash 产生错误结果的问题 [#59877](https://github.com/pingcap/tidb/issues/59877) @[yibin87](https://github.com/yibin87)

+ TiKV

    - 修复 Region Split 后可能无法快速选出 Leader 的问题 [#17602](https://github.com/tikv/tikv/issues/17602) @[LykxSassinator](https://github.com/LykxSassinator)
    - 修复时钟回退导致 RocksDB 流控异常，进而引发性能抖动的问题 [#17995](https://github.com/tikv/tikv/issues/17995) @[LykxSassinator](https://github.com/LykxSassinator)
    - 修复在仅启用一阶段提交 (1PC) 而未启用异步提交 (Async Commit) 时，可能无法读取最新写入数据的问题 [#18117](https://github.com/tikv/tikv/issues/18117) @[zyguan](https://github.com/zyguan)
    - 修复巴西和埃及时区转换错误的问题 [#16220](https://github.com/tikv/tikv/issues/16220) @[overvenus](https://github.com/overvenus)
    - 修复 GC Worker 负载过高时可能出现的死锁问题 [#18214](https://github.com/tikv/tikv/issues/18214) @[zyguan](https://github.com/zyguan)
    - 修复磁盘卡住可能导致 Leader 无法迁移，进而引发性能抖动的问题 [#17363](https://github.com/tikv/tikv/issues/17363) @[hhwyt](https://github.com/hhwyt)
    - 修复处理 GBK/GB18030 编码的数据时可能出现编码失败的问题 [#17618](https://github.com/tikv/tikv/issues/17618) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - 修复 CDC 连接在遇到异常时可能发生资源泄漏的问题 [#18245](https://github.com/tikv/tikv/issues/18245) @[wlwilliamx](https://github.com/wlwilliamx)
    - 修复 Region 合并时可能因 Raft index 匹配异常而导致 TiKV 异常退出的问题 [#18129](https://github.com/tikv/tikv/issues/18129) @[glorv](https://github.com/glorv)
    - 修复 Resolved-TS 监控和日志可能显示异常的问题 [#17989](https://github.com/tikv/tikv/issues/17989) @[ekexium](https://github.com/ekexium)
    - 修复由于 Titan 组件兼容性异常导致的升级失败问题 [#18263](https://github.com/tikv/tikv/issues/18263) @[v01dstar](https://github.com/v01dstar) @[LykxSassinator](https://github.com/LykxSassinator)

+ PD

    - 修复单个日志文件 `max-size` 默认值未被正确设置的问题 [#9037](https://github.com/tikv/pd/issues/9037) @[rleungx](https://github.com/rleungx)
    - 修复重启后 `flow-round-by-digit` 配置项的值可能被覆盖的问题 [#8980](https://github.com/tikv/pd/issues/8980) @[nolouch](https://github.com/nolouch)
    - 修复在导入或添加索引场景中，因 PD 网络不稳定可能导致操作失败的问题 [#8962](https://github.com/tikv/pd/issues/8962) @[okJiang](https://github.com/okJiang)
    - 修复启用 `tidb_enable_tso_follower_proxy` 系统变量后，PD 可能出现 panic 的问题 [#8950](https://github.com/tikv/pd/issues/8950) @[okJiang](https://github.com/okJiang)
    - 修复设置 `tidb_enable_tso_follower_proxy` 系统变量可能不生效的问题 [#8947](https://github.com/tikv/pd/issues/8947) @[JmPotato](https://github.com/JmPotato)
    - 修复 TSO 分配过程中可能出现的内存泄漏问题 [#9004](https://github.com/tikv/pd/issues/9004) @[rleungx](https://github.com/rleungx)
    - 修复 PD Leader 切换过程中，Region syncer 未能及时退出的问题 [#9017](https://github.com/tikv/pd/issues/9017) @[rleungx](https://github.com/rleungx)
    - 修复当某个 PD 节点不是 Leader 时，仍可能生成 TSO 的问题 [#9051](https://github.com/tikv/pd/issues/9051) @[rleungx](https://github.com/rleungx)

+ TiFlash

    - 修复 TiFlash 在内存占用较低的情况下，可能意外拒绝处理 Raft 消息的问题 [#9745](https://github.com/pingcap/tiflash/issues/9745) @[CalvinNeo](https://github.com/CalvinNeo)
    - 修复在导入大量数据后，TiFlash 可能持续占用较高内存的问题 [#9812](https://github.com/pingcap/tiflash/issues/9812) @[CalvinNeo](https://github.com/CalvinNeo)
    - 修复在分区表上执行 `ALTER TABLE ... RENAME COLUMN` 后，查询该表可能报错的问题 [#9787](https://github.com/pingcap/tiflash/issues/9787) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - 修复在某些情况下 TiFlash 意外退出时无法打印错误堆栈的问题 [#9902](https://github.com/pingcap/tiflash/issues/9902) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复当 `profiles.default.init_thread_count_scale` 设置为 `0` 时，TiFlash 启动可能会卡住的问题 [#9906](https://github.com/pingcap/tiflash/issues/9906) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复在查询涉及虚拟列并且触发远程读时，可能会出现 `Not found column` 错误的问题 [#9561](https://github.com/pingcap/tiflash/issues/9561) @[guo-shaoge](https://github.com/guo-shaoge)
    - 修复在存算分离架构下，TiFlash 计算节点可能被错误选为添加 Region peer 的目标节点的问题 [#9750](https://github.com/pingcap/tiflash/issues/9750) @[JaySon-Huang](https://github.com/JaySon-Huang)

+ Tools

    + Backup & Restore (BR)

        - 修复日志备份在无法访问 PD 时，遇到致命错误无法正确退出的问题 [#18087](https://github.com/tikv/tikv/issues/18087) @[YuJuncen](https://github.com/YuJuncen)
        - 修复 BR 向 TiKV 发送请求时收到 `rpcClient is idle` 错误导致恢复失败的问题 [#58845](https://github.com/pingcap/tidb/issues/58845) @[Tristan1900](https://github.com/Tristan1900)
        - 修复 PITR 无法恢复大于 3072 字节的索引的问题 [#58430](https://github.com/pingcap/tidb/issues/58430) @[YuJuncen](https://github.com/YuJuncen)
        - 修复使用 `br log status --json` 查询日志备份任务时，返回结果中缺少任务状态 `status` 字段的问题 [#57959](https://github.com/pingcap/tidb/issues/57959) @[Leavrth](https://github.com/Leavrth)
        - 修复日志备份在 advancer owner 切换时可能会异常进入暂停状态的问题 [#58031](https://github.com/pingcap/tidb/issues/58031) @[3pointer](https://github.com/3pointer)

    + TiCDC

        - 修复在较多小表场景中启用 TiCDC 可能导致 TiKV 重启的问题 [#18142](https://github.com/tikv/tikv/issues/18142) @[hicqu](https://github.com/hicqu)
        - 修复当上游将一个新增的列的默认值从 `NOT NULL` 修改为 `NULL` 后，下游默认值错误的问题 [#12037](https://github.com/pingcap/tiflow/issues/12037) @[wk989898](https://github.com/wk989898)
        - 修复由于 Sarama 客户端乱序重发消息导致 Kafka 消息乱序的问题 [#11935](https://github.com/pingcap/tiflow/issues/11935) @[3AceShowHand](https://github.com/3AceShowHand)
        - 修复 TiCDC 在 `RENAME TABLE` 操作中使用了错误的表名进行过滤的问题 [#11946](https://github.com/pingcap/tiflow/issues/11946) @[wk989898](https://github.com/wk989898)
        - 修复在删除 Changefeed 后 goroutine 泄漏的问题 [#11954](https://github.com/pingcap/tiflow/issues/11954) @[hicqu](https://github.com/hicqu)
        - 修复使用 `--overwrite-checkpoint-ts` 参数执行 `changefeed pause` 命令可能导致 Changefeed 卡住的问题 [#12055](https://github.com/pingcap/tiflow/issues/12055) @[hongyunyan](https://github.com/hongyunyan)
        - 修复 TiCDC 通过 Avro 协议同步 `default NULL` SQL 语句时报错的问题 [#11994](https://github.com/pingcap/tiflow/issues/11994) @[wk989898](https://github.com/wk989898)
        - 修复 PD 缩容后 TiCDC 无法正确连接 PD 的问题 [#12004](https://github.com/pingcap/tiflow/issues/12004) @[lidezhu](https://github.com/lidezhu)

    + TiDB Lightning

        - 修复日志没有正确脱敏的问题 [#59086](https://github.com/pingcap/tidb/issues/59086) @[GMHDBJD](https://github.com/GMHDBJD)
