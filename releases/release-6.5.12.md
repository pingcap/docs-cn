---
title: TiDB 6.5.12 Release Notes
summary: 了解 TiDB 6.5.12 版本的兼容性变更、改进提升，以及错误修复。
---

# TiDB 6.5.12 Release Notes

发版日期：2025 年 2 月 27 日

TiDB 版本：6.5.12

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v6.5/quick-start-with-tidb) | [生产部署](https://docs.pingcap.com/zh/tidb/v6.5/production-deployment-using-tiup) | [下载离线包](https://cn.pingcap.com/product-community/?version=v6.5.12#version-list)

## 兼容性变更

- 通过 [TiDB HTTP API](https://github.com/pingcap/tidb/blob/release-6.5/docs/tidb_http_api.md) 获取 DDL 历史任务时，默认获取任务数量的上限为 2048，以避免历史任务数量过多导致 OOM 的问题 [#55711](https://github.com/pingcap/tidb/issues/55711) @[joccau](https://github.com/joccau)
- 新增系统变量 [`tidb_ddl_reorg_max_write_speed`](https://docs.pingcap.com/zh/tidb/v6.5/system-variables#tidb_ddl_reorg_max_write_speed-从-v6512-版本开始引入)，用于限制加索引时 ingest 阶段速度的上限 [#57156](https://github.com/pingcap/tidb/issues/57156) @[CbcWestwolf](https://github.com/CbcWestwolf)

## 改进提升

+ TiDB

    - 增强读时间戳的合法性检测 [#57786](https://github.com/pingcap/tidb/issues/57786) @[MyonKeminta](https://github.com/MyonKeminta)

+ TiKV

    - 增加对非法 `max_ts` 更新的检测机制 [#17916](https://github.com/tikv/tikv/issues/17916) @[ekexium](https://github.com/ekexium)

+ TiFlash

    - 提升聚簇索引表在后台回收过期数据的速度 [#9529](https://github.com/pingcap/tiflash/issues/9529) @[JaySon-Huang](https://github.com/JaySon-Huang)

+ Tools

    + Backup & Restore (BR)

        - 对于全量恢复，新增对目标集群是否为空集群的检查 [#35744](https://github.com/pingcap/tidb/issues/35744) @[3pointer](https://github.com/3pointer)
        - 对于非全量恢复，新增对目标集群中是否存在同名表的检查 [#55087](https://github.com/pingcap/tidb/issues/55087) @[RidRisR](https://github.com/RidRisR)
        - 去掉除了 `br log restore` 子命令之外其它 `br log` 子命令对 TiDB `domain` 数据结构的载入，降低内存消耗 [#52088](https://github.com/pingcap/tidb/issues/52088) @[Leavrth](https://github.com/Leavrth)
        - 在进行全量备份时，默认不计算表级别的 checksum (`--checksum=false`) 以提升备份性能 [#56373](https://github.com/pingcap/tidb/issues/56373) @[Tristan1900](https://github.com/Tristan1900)

    + TiDB Lightning

        - 在解析 CSV 文件时，新增行宽检查以防止 OOM 问题 [#58590](https://github.com/pingcap/tidb/issues/58590) @[D3Hunter](https://github.com/D3Hunter)

## 错误修复

+ TiDB

    - 修复使用 `NATURAL JOIN` 或者 `USING` 子句之后，再使用子查询可能会报错的问题 [#53766](https://github.com/pingcap/tidb/issues/53766) @[dash12653](https://github.com/dash12653)
    - 修复由于 `CAST` 函数不支持显式设置字符集导致报错的问题 [#55677](https://github.com/pingcap/tidb/issues/55677) @[Defined2014](https://github.com/Defined2014)
    - 修复 `LOAD DATA ... REPLACE INTO` 导致的数据不一致问题 [#56408](https://github.com/pingcap/tidb/issues/56408) @[fzzf678](https://github.com/fzzf678)
    - 修复执行 `ADD INDEX` 时，未检查索引长度限制的问题 [#56930](https://github.com/pingcap/tidb/issues/56930) @[fzzf678](https://github.com/fzzf678)
    - 修复当公共表表达式 (CTE) 有多个数据消费者时，如果某个消费者在未读取数据时就退出，可能导致非法内存访问的问题 [#55881](https://github.com/pingcap/tidb/issues/55881) @[windtalker](https://github.com/windtalker)
    - 修复在构造 `IndexMerge` 时可能丢失部分谓词的问题 [#58476](https://github.com/pingcap/tidb/issues/58476) @[hawkingrei](https://github.com/hawkingrei)
    - 修复将数据从 `BIT` 类型换为 `CHAR` 类型时可能导致 TiKV 崩溃的问题 [#56494](https://github.com/pingcap/tidb/issues/56494) @[lcwangchao](https://github.com/lcwangchao)
    - 修复在 `CREATE VIEW` 语句中使用变量或参数时未报错的问题 [#53176](https://github.com/pingcap/tidb/issues/53176) @[mjonss](https://github.com/mjonss)
    - 修复未释放的会话资源可能导致的内存泄漏问题 [#56271](https://github.com/pingcap/tidb/issues/56271) @[lance6716](https://github.com/lance6716)
    - 修复分布式执行框架下，在 PD 修改成员后 `ADD INDEX` 可能失败的问题 [#48680](https://github.com/pingcap/tidb/issues/48680) @[lance6716](https://github.com/lance6716)
    - 修复查询 `cluster_slow_query` 表时，使用 `ORDER BY` 可能导致结果乱序的问题 [#51723](https://github.com/pingcap/tidb/issues/51723) @[Defined2014](https://github.com/Defined2014)
    - 修复由于 stale read 未对读操作的时间戳进行严格校验，导致 TSO 和真实物理时间存在偏移，有小概率影响事务一致性的问题 [#56809](https://github.com/pingcap/tidb/issues/56809) @[MyonKeminta](https://github.com/MyonKeminta)
    - 修复 `INFORMATION_SCHEMA.columns` 查询性能下降的问题 [#58184](https://github.com/pingcap/tidb/issues/58184) @[lance6716](https://github.com/lance6716)
    - 修复 `INSERT ... ON DUPLICATE KEY` 语句不兼容 `mysql_insert_id` 的问题 [#55965](https://github.com/pingcap/tidb/issues/55965) @[tiancaiamao](https://github.com/tiancaiamao)
    - 修复当查询条件为 `column IS NULL` 访问唯一索引时，优化器将行数错误地估算为 1 的问题 [#56116](https://github.com/pingcap/tidb/issues/56116) @[hawkingrei](https://github.com/hawkingrei)
    - 修复 `IndexLookUp` 算子部分内存未被追踪的问题 [#56440](https://github.com/pingcap/tidb/issues/56440) @[wshwsh12](https://github.com/wshwsh12)
    - 修复 TiDB 内部协程可能出现数据竞争的问题 [#57798](https://github.com/pingcap/tidb/issues/57798) [#56053](https://github.com/pingcap/tidb/issues/56053) @[fishiu](https://github.com/fishiu) @[tiancaiamao](https://github.com/tiancaiamao)
    - 修复当一个查询有索引合并 (Index Merge) 执行计划可用时，`read_from_storage` hint 可能不生效的问题 [#56217](https://github.com/pingcap/tidb/issues/56217) @[AilinKid](https://github.com/AilinKid)
    - 修复无法为带别名的多表删除语句 `DELETE` 创建执行计划绑定的问题 [#56726](https://github.com/pingcap/tidb/issues/56726) @[hawkingrei](https://github.com/hawkingrei)
    - 修复 `INDEX_HASH_JOIN` 在异常退出时可能卡住的问题 [#54055](https://github.com/pingcap/tidb/issues/54055) @[wshwsh12](https://github.com/wshwsh12)
    - 修复可能同时存在两个 DDL Owner 的问题 [#54689](https://github.com/pingcap/tidb/issues/54689) @[joccau](https://github.com/joccau)
    - 修复查询 `information_schema.cluster_slow_query` 表时，如果不加时间过滤条件，则只会查询最新的慢日志文件的问题 [#56100](https://github.com/pingcap/tidb/issues/56100) @[crazycs520](https://github.com/crazycs520)
    - 修复添加唯一索引时可能遇到 `duplicate entry` 的问题 [#56161](https://github.com/pingcap/tidb/issues/56161) @[tangenta](https://github.com/tangenta)
    - 修复在某些类型转换出错的情况下报错信息不对的问题 [#41730](https://github.com/pingcap/tidb/issues/41730) @[hawkingrei](https://github.com/hawkingrei)
    - 修复 `VIEW` 中定义的 CTE 被错误 inline 的问题 [#56582](https://github.com/pingcap/tidb/issues/56582) @[elsa0520](https://github.com/elsa0520)
    - 修复如果 CTE 包含 `ORDER BY`、`LIMIT`、`SELECT DISTINCT` 子句，并且被另外一个 CTE 的递归部分所引用时，可能被错误地 inline 导致执行报错的问题 [#56603](https://github.com/pingcap/tidb/issues/56603) @[elsa0520](https://github.com/elsa0520)
    - 修复在 CTE 中解析数据库名时，返回错误的数据库名的问题 [#54582](https://github.com/pingcap/tidb/issues/54582) @[hawkingrei](https://github.com/hawkingrei)
    - 修复 `UPDATE` 语句更新 `ENUM` 类型的值时更新错误的问题 [#56832](https://github.com/pingcap/tidb/issues/56832) @[xhebox](https://github.com/xhebox)
    - 修复某些情况下在新增 `DATE` 类型的列后执行 `UPDATE` 语句报错 `Incorrect date value: '0000-00-00'` 的问题 [#59047](https://github.com/pingcap/tidb/issues/59047) @[mjonss](https://github.com/mjonss)
    - 修复在 Prepare 协议中，客户端使用非 UTF8 相关字符集报错的问题 [#58870](https://github.com/pingcap/tidb/issues/58870) @[xhebox](https://github.com/xhebox)
    - 修复某些情况下查询临时表会产生 TiKV 请求的问题 [#58875](https://github.com/pingcap/tidb/issues/58875) @[tiancaiamao](https://github.com/tiancaiamao)
    - 修复 `ONLY_FULL_GROUP_BY` 设置对于视图中的语句不生效的问题 [#53175](https://github.com/pingcap/tidb/issues/53175) @[mjonss](https://github.com/mjonss)
    - 修复查询分区表时，`IN` 条件中的值类型不匹配且转换错误，导致查询结果出错的问题 [#54746](https://github.com/pingcap/tidb/issues/54746) @[mjonss](https://github.com/mjonss)
    - 修复当某些项的值为空时，查询慢日志可能失败的问题 [#58147](https://github.com/pingcap/tidb/issues/58147) @[yibin87](https://github.com/yibin87)
    - 修复 `RADIANS()` 函数计算顺序错误的问题 [#57671](https://github.com/pingcap/tidb/issues/57671) @[gengliqi](https://github.com/gengliqi)
    - 修复 `BIT` 列默认值错误的问题 [#57301](https://github.com/pingcap/tidb/issues/57301) @[YangKeao](https://github.com/YangKeao)
    - 修复无法为带别名的多表删除进行绑定的问题 [#56726](https://github.com/pingcap/tidb/issues/56726) @[hawkingrei](https://github.com/hawkingrei)
    - 修复如果 CTE 包含 `ORDER BY`、`LIMIT` 或 `SELECT DISTINCT` 子句并且被另外一个 CTE 的递归部分引用，可能出现内联 (Inline) 错误 [#56603](https://github.com/pingcap/tidb/issues/56603) @[elsa0520](https://github.com/elsa0520)
    - 修复统计信息同步加载超时可能处理不正确的问题 [#57710](https://github.com/pingcap/tidb/issues/57710) @[hawkingrei](https://github.com/hawkingrei)
    - 修复在 CTE 中解析数据库名时，可能得到错误的数据库名的问题 [#54582](https://github.com/pingcap/tidb/issues/54582) @[hawkingrei](https://github.com/hawkingrei)
    - 修复 TiDB 启动时由于非法绑定数据可能导致 panic 的问题 [#58016](https://github.com/pingcap/tidb/issues/58016) @[qw4990](https://github.com/qw4990)
    - 修复代价估算在某些极端场景下估算出非法 INF/NaN 值，进而可能导致 Join Reorder 结果错误的问题 [#56704](https://github.com/pingcap/tidb/issues/56704) @[winoros](https://github.com/winoros)
    - 修复手动加载统计信息时，统计信息文件中包含 null 可能导致加载失败的问题 [#53966](https://github.com/pingcap/tidb/issues/53966) @[King-Dylan](https://github.com/King-Dylan)
    - 修复创建两个相同名称的视图而没有报错的问题 [#58769](https://github.com/pingcap/tidb/issues/58769) @[tiancaiamao](https://github.com/tiancaiamao)
    - 修复虚拟生成列依赖包含 `ON UPDATE` 属性的列时，更新行的数据与其索引数据不一致问题 [#56829](https://github.com/pingcap/tidb/issues/56829) @[joechenrh](https://github.com/joechenrh)
    - 修复系统表 `INFORMATION_SCHEMA.TABLES` 返回结果不正确的问题 [#57345](https://github.com/pingcap/tidb/issues/57345) @[tangenta](https://github.com/tangenta)

+ TiKV

    - 修复 Follower Read 可能读取到过期数据的问题 [#17018](https://github.com/tikv/tikv/issues/17018) @[glorv](https://github.com/glorv)
    - 修复销毁 Peer 时可能出现的 TiKV panic 问题 [#18005](https://github.com/tikv/tikv/issues/18005) @[glorv](https://github.com/glorv)
    - 修复时钟回退导致 RocksDB 流控异常，进而引发性能抖动的问题 [#17995](https://github.com/tikv/tikv/issues/17995) @[LykxSassinator](https://github.com/LykxSassinator)
    - 修复磁盘卡住可能导致 Leader 无法迁移，进而引发性能抖动的问题 [#17363](https://github.com/tikv/tikv/issues/17363) @[hhwyt](https://github.com/hhwyt)
    - 修复在仅启用一阶段提交 (1PC) 而未启用异步提交 (Async Commit) 时，可能无法读取最新写入数据的问题 [#18117](https://github.com/tikv/tikv/issues/18117) @[zyguan](https://github.com/zyguan)
    - 修复 GC Worker 负载过高时可能出现的死锁问题 [#18214](https://github.com/tikv/tikv/issues/18214) @[zyguan](https://github.com/zyguan)
    - 修复 Grafana 上 TiKV 面板的 **Storage async write duration** 监控指标不准确的问题 [#17579](https://github.com/tikv/tikv/issues/17579) @[overvenus](https://github.com/overvenus)
    - 修复使用 `RADIANS()` 或 `DEGREES()` 函数时可能导致 TiKV panic 的问题 [#17852](https://github.com/tikv/tikv/issues/17852) @[gengliqi](https://github.com/gengliqi)
    - 修复 TiKV 处理 destroyed peer 时可能遇到的 panic 的问题 [#17840](https://github.com/tikv/tikv/issues/17840) @[glorv](https://github.com/glorv))
    - 修复 Region Split 后可能无法快速选出 Leader 的问题 [#17602](https://github.com/tikv/tikv/issues/17602) @[LykxSassinator](https://github.com/LykxSassinator)
    - 修复处理 GBK/GB18030 编码的数据时可能出现编码失败的问题 [#17618](https://github.com/tikv/tikv/issues/17618) @[CbcWestwolf](https://github.com/CbcWestwolf)

+ PD

    - 修复 TSO 分配过程中可能出现的内存泄漏问题 [#9004](https://github.com/tikv/pd/issues/9004) @[rleungx](https://github.com/rleungx)
    - 修复设置 `tidb_enable_tso_follower_proxy` 系统变量可能不生效的问题 [#8947](https://github.com/tikv/pd/issues/8947) @[JmPotato](https://github.com/JmPotato)
    - 修复一个可能导致 PD panic 的潜在问题 [#8915](https://github.com/tikv/pd/issues/8915) @[bufferflies](https://github.com/bufferflies)
    - 修复长期运行的集群中可能出现的内存泄漏问题 [#9047](https://github.com/tikv/pd/issues/9047) @[bufferflies](https://github.com/bufferflies)
    - 修复当某个 PD 节点不是 Leader 时，仍可能生成 TSO 的问题 [#9051](https://github.com/tikv/pd/issues/9051) @[rleungx](https://github.com/rleungx)
    - 修复 PD Leader 切换过程中，Region syncer 未能及时退出的问题 [#9017](https://github.com/tikv/pd/issues/9017) @[rleungx](https://github.com/rleungx)
    - 修复创建 `evict-leader-scheduler` 或 `grant-leader-scheduler` 遇到错误时，未能将错误信息返回到 pd-ctl 的问题 [#8759](https://github.com/tikv/pd/issues/8759) @[okJiang](https://github.com/okJiang)
    - 修复热点缓存中可能存在的内存泄露问题 [#8698](https://github.com/tikv/pd/issues/8698) @[lhy1024](https://github.com/lhy1024)
    - 修复存在大量 Region 时，无法请求 PD 的 Region API 的问题 [#55872](https://github.com/pingcap/tidb/issues/55872) @[rleungx](https://github.com/rleungx)
    - 修复 `evict-leader-scheduler` 在使用相同 Store ID 重复创建后无法正常工作的问题 [#8756](https://github.com/tikv/pd/issues/8756) @[okJiang](https://github.com/okJiang)
    - 将 Gin Web Framework 的版本从 v1.9.1 升级到 v1.10.0 以修复潜在的安全问题 [#8643](https://github.com/tikv/pd/issues/8643) @[JmPotato](https://github.com/JmPotato)
    - 修复在 `evict-leader-scheduler` 中使用了错误的参数后，PD 不能正确报错且导致部分 scheduler 不可用的问题 [#8619](https://github.com/tikv/pd/issues/8619) @[rleungx](https://github.com/rleungx)
    - 修复 label 统计中的内存泄露问题 [#8700](https://github.com/tikv/pd/issues/8700) @[lhy1024](https://github.com/lhy1024)
    - 修复 TiDB Dashboard 不能正常读取 PD `trace` 数据的问题 [#7253](https://github.com/tikv/pd/issues/7253) @[nolouch](https://github.com/nolouch)
    - 修复 Region 统计中的内存泄露问题 [#8710](https://github.com/tikv/pd/issues/8710) @[rleungx](https://github.com/rleungx)
    - 修复 etcd Leader 切换时 PD 不能快速重新选举的问题 [#8823](https://github.com/tikv/pd/issues/8823) @[rleungx](https://github.com/rleungx)

+ TiFlash

    - 修复 `SUBSTRING()` 函数不支持部分整数类型的 `pos` 和 `len` 参数导致查询报错的问题 [#9473](https://github.com/pingcap/tiflash/issues/9473) @[gengliqi](https://github.com/gengliqi)
    - 修复一些 TiFlash 不支持的 JSON 函数被错误地下推到 TiFlash 的问题 [#9444](https://github.com/pingcap/tiflash/issues/9444) @[windtalker](https://github.com/windtalker)
    - 修复当 `SUBSTRING()` 函数的第二个参数为负数时，可能返回错误结果的问题 [#9604](https://github.com/pingcap/tiflash/issues/9604) @[guo-shaoge](https://github.com/guo-shaoge)
    - 修复当 `LPAD()` 和 `RPAD()` 函数在某些情况下返回错误结果的问题 [#9465](https://github.com/pingcap/tiflash/issues/9465) @[guo-shaoge](https://github.com/guo-shaoge)
    - 修复对大表执行 `DROP TABLE` 可能导致 TiFlash OOM 的问题 [#9437](https://github.com/pingcap/tiflash/issues/9437) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复获取 CPU 数量时因出现零除错误而导致 TiFlash 启动失败的问题 [#9212](https://github.com/pingcap/tiflash/issues/9212) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - 修复在导入大量数据后，TiFlash 可能持续占用较高内存的问题 [#9812](https://github.com/pingcap/tiflash/issues/9812) @[CalvinNeo](https://github.com/CalvinNeo)

+ Tools

    + Backup & Restore (BR)

        - 修复 BR 向 TiKV 发送请求时收到 `rpcClient is idle` 错误导致恢复失败的问题 [#58845](https://github.com/pingcap/tidb/issues/58845) @[Tristan1900](https://github.com/Tristan1900)
        - 修复使用 `br log status --json` 查询日志备份任务时，返回结果中缺少任务状态 `status` 字段的问题 [#57959](https://github.com/pingcap/tidb/issues/57959) @[Leavrth](https://github.com/Leavrth)
        - 修复日志备份时 PD Leader I/O 延迟可能导致 checkpoint 延迟增加的问题 [#58574](https://github.com/pingcap/tidb/issues/58574) @[YuJuncen](https://github.com/YuJuncen)
        - 修复通过 `tiup br restore` 命令进行库表级别恢复时，遗漏检查目标集群中表是否已存在，可能会覆盖已有表的问题 [#58168](https://github.com/pingcap/tidb/issues/58168) @[RidRisR](https://github.com/RidRisR)
        - 修复日志备份在 advancer owner 切换时可能会异常进入暂停状态的问题 [#58031](https://github.com/pingcap/tidb/issues/58031) @[3pointer](https://github.com/3pointer)
        - 修复日志备份不能及时解决残留锁导致 Checkpoint 无法推进的问题 [#57134](https://github.com/pingcap/tidb/issues/57134) @[3pointer](https://github.com/3pointer)
        - 修复 BR 集成测试用例不稳定的问题，并新增用于模拟快照或者日志备份文件损坏的测试用例 [#53835](https://github.com/pingcap/tidb/issues/53835) @[Leavrth](https://github.com/Leavrth)
        - 修复日志可能打印加密信息的问题 [#57585](https://github.com/pingcap/tidb/issues/57585) @[kennytm](https://github.com/kennytm)
        - 修复当集群存在大量表但实际数据量较小时，PITR 数据恢复任务可能出现 `Information schema is out of date` 报错的问题 [#57743](https://github.com/pingcap/tidb/issues/57743) @[Tristan1900](https://github.com/Tristan1900)

    + TiCDC

        - 修复 TiCDC 在 `RENAME TABLE` 操作中使用了错误的表名进行过滤的问题 [#11946](https://github.com/pingcap/tiflow/issues/11946) @[wk989898](https://github.com/wk989898)
        - 修复 TiCDC 通过 Avro 协议同步 `default NULL` SQL 语句时报错的问题 [#11994](https://github.com/pingcap/tiflow/issues/11994) @[wk989898](https://github.com/wk989898)
        - 修复 PD 缩容后 TiCDC 无法正确连接 PD 的问题 [#12004](https://github.com/pingcap/tiflow/issues/12004) @[lidezhu](https://github.com/lidezhu)
        - 修复 Changefeed 停止或删除后，Initial Scan 未被取消的问题 [#11638](https://github.com/pingcap/tiflow/issues/11638) @[3AceShowHand](https://github.com/3AceShowHand)
        - 修复当上游将一个新增的列的默认值从 `NOT NULL` 修改为 `NULL` 后，下游默认值错误的问题 [#12037](https://github.com/pingcap/tiflow/issues/12037) @[wk989898](https://github.com/wk989898)
        - 修复使用 `--overwrite-checkpoint-ts` 参数执行 `changefeed pause` 命令可能导致 Changefeed 卡住的问题 [#12055](https://github.com/pingcap/tiflow/issues/12055) @[hongyunyan](https://github.com/hongyunyan)
        - 修复 TiCDC 同步 `CREATE TABLE IF NOT EXISTS` 或 `CREATE DATABASE IF NOT EXISTS` 语句时可能出现 panic 的问题 [#11839](https://github.com/pingcap/tiflow/issues/11839) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - 修复同步 `TRUNCATE TABLE` DDL 并且该表没有有效索引时，TiCDC 可能会报错的问题 [#11765](https://github.com/pingcap/tiflow/issues/11765) @[asddongmen](https://github.com/asddongmen)
        - 修复 TiDB DDL owner 变更导致 DDL 任务的 schema 版本出现非递增时，TiCDC 错误丢弃 DDL 任务的问题 [#11714](https://github.com/pingcap/tiflow/issues/11714) @[wlwilliamx](https://github.com/wlwilliamx)
        - 修复在集群扩容出新的 TiKV 节点后 Changefeed 可能会卡住的问题 [#11766](https://github.com/pingcap/tiflow/issues/11766) @[lidezhu](https://github.com/lidezhu)
        - 修复由于 Sarama 客户端乱序重发消息导致 Kafka 消息乱序的问题 [#11935](https://github.com/pingcap/tiflow/issues/11935) @[3AceShowHand](https://github.com/3AceShowHand)
        - 修复 Puller 模块 Resolved TS 延迟监控显示不正确的问题 [#11561](https://github.com/pingcap/tiflow/issues/11561) @[wlwilliamx](https://github.com/wlwilliamx)
        - 修复 redo 模块无法正确上报错误的问题 [#11744](https://github.com/pingcap/tiflow/issues/11744) @[CharlesCheung96](https://github.com/CharlesCheung96)

    + TiDB Data Migration (DM)

        - 修复多个 DM-master 节点可能同时成为 Leader 导致数据不一致的问题 [#11602](https://github.com/pingcap/tiflow/issues/11602) @[GMHDBJD](https://github.com/GMHDBJD)
        - 修复当密码长度超过 19 个字符时无法连接 MySQL 8.0 的问题 [#11603](https://github.com/pingcap/tiflow/issues/11603) @[fishiu](https://github.com/fishiu)
        - 修复当同时配置 TLS 和 `shard-mode` 时，`start-task` 会在前置检查中报错的问题 [#11842](https://github.com/pingcap/tiflow/issues/11842) @[sunxiaoguang](https://github.com/sunxiaoguang)

    + TiDB Lightning

        - 修复日志没有正确脱敏的问题 [#59086](https://github.com/pingcap/tidb/issues/59086) @[GMHDBJD](https://github.com/GMHDBJD)
        - 修复编码阶段因未缓存导致的性能回退问题 [#56705](https://github.com/pingcap/tidb/issues/56705) @[OliverS929](https://github.com/OliverS929)
        - 修复在高并发场景下，从云存储导入数据时性能下降的问题 [#57413](https://github.com/pingcap/tidb/issues/57413) @[xuanyu66](https://github.com/xuanyu66)
        - 修复 TiDB Lightning 在更新任务元数据时遇到 `Lock wait timeout` 错误未自动重试的问题 [#53042](https://github.com/pingcap/tidb/issues/53042) @[guoshouyan](https://github.com/guoshouyan)
        - 修复 TiDB Lightning 因 TiKV 发送的消息过大而接收失败的问题 [#56114](https://github.com/pingcap/tidb/issues/56114) @[fishiu](https://github.com/fishiu)
        - 修复使用 TiDB Lightning 导入数据时，错误报告输出被截断的问题 [#58085](https://github.com/pingcap/tidb/issues/58085) @[lance6716](https://github.com/lance6716)

    + Dumpling

        - 修复当 Google Cloud Storage (GCS) 返回 503 错误时 Dumpling 未正确重试的问题 [#56127](https://github.com/pingcap/tidb/issues/56127) @[OliverS929](https://github.com/OliverS929)
