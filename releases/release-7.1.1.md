---
title: TiDB 7.1.1 Release Notes
summary: 了解 TiDB 7.1.1 版本的兼容性变更、改进提升，以及错误修复。
---

# TiDB 7.1.1 Release Notes

发版日期：2023 年 7 月 24 日

TiDB 版本：7.1.1

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v7.1/quick-start-with-tidb) | [生产部署](https://docs.pingcap.com/zh/tidb/v7.1/production-deployment-using-tiup)

## 兼容性变更

- TiDB 新增 `tidb_lock_unchanged_keys` 变量用于控制是否对于没有修改的 key 加锁 [#44714](https://github.com/pingcap/tidb/issues/44714) @[ekexium](https://github.com/ekexium)

### 行为变更

- TiCDC 在处理 Update 事件时，如果事件的主键或者非空唯一索引的列值发生改变，则会将该条事件拆分为 Delete 和 Insert 两条事件。更多信息，请参考[用户文档](/ticdc/ticdc-split-update-behavior.md#含有单条-update-变更的事务拆分)。

## 改进提升

+ TiDB

    - 执行计划缓存支持带有超过 200 个参数的查询 [#44823](https://github.com/pingcap/tidb/issues/44823) @[qw4990](https://github.com/qw4990)
    - 优化与落盘相关的 chunk 读取的性能 [#45125](https://github.com/pingcap/tidb/issues/45125) @[YangKeao](https://github.com/YangKeao)
    - 优化构造索引扫描范围的逻辑，支持将一些复杂条件转化为索引扫描范围 [#41572](https://github.com/pingcap/tidb/issues/41572) [#44389](https://github.com/pingcap/tidb/issues/44389) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes)
    - 当 Stale Read 的 retry leader 遇到 lock 时，resolve lock 之后强制重试 leader，避免无谓开销 [#43659](https://github.com/pingcap/tidb/issues/43659) @[you06](https://github.com/you06)

+ PD

    - 未开启 Swagger server 时，PD 默认屏蔽 Swagger API [#6786](https://github.com/tikv/pd/issues/6786) @[bufferflies](https://github.com/bufferflies)

+ Tools

    + TiCDC

        - 优化 TiCDC 同步到对象存储时对二进制字段的编码格式 [#9373](https://github.com/pingcap/tiflow/issues/9373) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - 在同步到 Kafka 场景下，支持 OAUTHBEARER 认证方式 [#8865](https://github.com/pingcap/tiflow/issues/8865) @[hi-rustin](https://github.com/Rustin170506)

    + TiDB Lightning

        - 改进 TiDB Lightning 在 checksum 阶段对 PD `ClientTSOStreamClosed` 错误的重试逻辑 [#45301](https://github.com/pingcap/tidb/issues/45301) @[lance6716](https://github.com/lance6716)
        - 数据导入完成后使用 SQL 方式校验 checksum，提升数据校验的稳定性 [#41941](https://github.com/pingcap/tidb/issues/41941) @[GMHDBJD](https://github.com/GMHDBJD)

    + Dumpling

        - 避免 Dumpling 在使用 `--sql` 参数时执行表查询语句，从而减少导出开销 [#45239](https://github.com/pingcap/tidb/issues/45239) @[lance6716](https://github.com/lance6716)

    + TiDB Binlog

        - 优化表信息的获取方式，降低 Drainer 的初始化时间和内存占用 [#1137](https://github.com/pingcap/tidb-binlog/issues/1137) @[lichunzhu](https://github.com/lichunzhu)

## 错误修复

+ TiDB

    - 修复 GC resolve lock 可能错过一些悲观锁的问题 [#45134](https://github.com/pingcap/tidb/issues/45134)  @[MyonKeminta](https://github.com/MyonKeminta)
    - 修复创建新会话时 Stats Collector 可能会造成死锁的问题 [#44502](https://github.com/pingcap/tidb/issues/44502) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes)
    - 修复 memory tracker 潜在的泄露问题 [#44612](https://github.com/pingcap/tidb/issues/44612) @[wshwsh12](https://github.com/wshwsh12)
    - 修复 batch coprocessor 重试时可能会生成错误 Region 信息导致查询失败的问题 [#44622](https://github.com/pingcap/tidb/issues/44622) @[windtalker](https://github.com/windtalker)
    - 修复 index scan 中可能存在的数据竞争问题 [#45126](https://github.com/pingcap/tidb/issues/45126) @[wshwsh12](https://github.com/wshwsh12)
    - 修复当开启 `tidb_enable_parallel_apply` 时，MPP 模式下的查询结果出错的问题 [#45299](https://github.com/pingcap/tidb/issues/45299) @[windtalker](https://github.com/windtalker)
    - 修复带 `indexMerge` 的查询被 kill 时可能会 hang 住的问题 [#45279](https://github.com/pingcap/tidb/issues/45279) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - 修复极端情况下，统计 SQL execution detail 的信息占用太多内存导致 TiDB OOM 的问题 [#44047](https://github.com/pingcap/tidb/issues/44047) @[wshwsh12](https://github.com/wshwsh12)
    - 修复对于过长的 SQL 输入，`FormatSQL()` 方法无法正常截断的问题 [#44542](https://github.com/pingcap/tidb/issues/44542) @[hawkingrei](https://github.com/hawkingrei)
    - 修复集群升级过程中，DDL 操作卡住导致升级失败的问题 [#44158](https://github.com/pingcap/tidb/issues/44158) @[zimulala](https://github.com/zimulala)
    - 修复在 TiDB 节点故障后其它 TiDB 节点没有接管 TTL 任务的问题 [#45022](https://github.com/pingcap/tidb/issues/45022) @[lcwangchao](https://github.com/lcwangchao)
    - 修复当使用 MySQL 的 Cursor Fetch 协议时，结果集占用的内存超过 `tidb_mem_quota_query` 的限制导致 TiDB OOM 的问题。修复后，TiDB 会自动将结果集写入磁盘以释放内存资源 [#43233](https://github.com/pingcap/tidb/issues/43233) @[YangKeao](https://github.com/YangKeao)
    - 修复即使用户没有权限，也能查看 `INFORMATION_SCHEMA.TIFLASH_REPLICA` 表信息的问题 [#45320](https://github.com/pingcap/tidb/issues/45320) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - 修复 `ADMIN SHOW DDL JOBS` 语句的返回结果中 `ROW_COUNT` 不准确的问题 [#44044](https://github.com/pingcap/tidb/issues/44044) @[tangenta](https://github.com/tangenta)
    - 修复查询 Range COLUMNS 分区表时可能遇到报错的问题 [#43459](https://github.com/pingcap/tidb/issues/43459) @[mjonss](https://github.com/mjonss)
    - 修复 DDL 任务从暂停状态到恢复时，恢复出错的问题 [#44217](https://github.com/pingcap/tidb/issues/44217) @[dhysum](https://github.com/dhysum)
    - 修复内存悲观锁导致 `FLASHBACK` 失败并且数据不一致的问题 [#44292](https://github.com/pingcap/tidb/issues/44292) @[JmPotato](https://github.com/JmPotato)
    - 修复删除表之后还能从 `INFORMATION_SCHEMA` 读取到该表的问题 [#43714](https://github.com/pingcap/tidb/issues/43714) @[tangenta](https://github.com/tangenta)
    - 修复集群升级前，如果有暂停的 DDL，会出现升级失败的问题 [#44225](https://github.com/pingcap/tidb/issues/44225) @[zimulala](https://github.com/zimulala)
    - 修复通过 BR 恢复 `AUTO_ID_CACHE=1` 的表时，会遇到 `duplicate entry` 报错的问题 [#44716](https://github.com/pingcap/tidb/issues/44716) @[tiancaiamao](https://github.com/tiancaiamao)
    - 修复 DDL owner 切换数次之后导致数据索引不一致的问题 [#44619](https://github.com/pingcap/tidb/issues/44619) @[tangenta](https://github.com/tangenta)
    - 修复当取消处于 `none` 状态的 `ADD INDEX` DDL 任务时，因为分布式执行框架任务队列没有清理此任务而导致的内存泄漏问题 [#44205](https://github.com/pingcap/tidb/issues/44205) @[tangenta](https://github.com/tangenta)
    - 修复代理协议在处理某些错误数据时报错 `Header read timeout` 的问题 [#43205](https://github.com/pingcap/tidb/issues/43205) @[blacktear23](https://github.com/blacktear23)
    - 修复 PD 隔离可能会导致运行的 DDL 阻塞的问题 [#44267](https://github.com/pingcap/tidb/issues/44267) @[wjhuang2016](https://github.com/wjhuang2016)
    - 修复 `SELECT CAST(n AS CHAR)` 语句中的 `n` 为负数时，查询结果出错的问题 [#44786](https://github.com/pingcap/tidb/issues/44786) @[xhebox](https://github.com/xhebox)
    - 修复创建大量空分区表后内存占用过多的问题 [#44308](https://github.com/pingcap/tidb/issues/44308) @[hawkingrei](https://github.com/hawkingrei)
    - 修复 Join Reorder 可能会造成 Outer Join 结果错误的问题 [#44314](https://github.com/pingcap/tidb/issues/44314) @[AilinKid](https://github.com/AilinKid)
    - 修复包含 CTE 的查询可能导致磁盘可用空间不足的问题 [#44477](https://github.com/pingcap/tidb/issues/44477) @[guo-shaoge](https://github.com/guo-shaoge)
    - 修复删除数据库导致 GC 推进慢的问题 [#33069](https://github.com/pingcap/tidb/issues/33069) @[tiancaiamao](https://github.com/tiancaiamao)
    - 修复在 ingest 模式下创建索引失败的问题 [#44137](https://github.com/pingcap/tidb/issues/44137) @[tangenta](https://github.com/tangenta)
    - 修复当分区表定义中使用了 `FLOOR()` 函数对分区列进行取整时 `SELECT` 语句返回错误的问题 [#42323](https://github.com/pingcap/tidb/issues/42323) @[jiyfhust](https://github.com/jiyfhust)
    - 修复 follower read 未处理 flashback 错误而进行重试，导致查询报错的问题 [#43673](https://github.com/pingcap/tidb/issues/43673) @[you06](https://github.com/you06)
    - 修复 `memTracker` 配合 cursor fetch 使用导致内存泄漏的问题 [#44254](https://github.com/pingcap/tidb/issues/44254) @[YangKeao](https://github.com/YangKeao)
    - 修复 `SHOW PROCESSLIST` 语句无法显示子查询时间较长语句的事务的 TxnStart 的问题 [#40851](https://github.com/pingcap/tidb/issues/40851) @[crazycs520](https://github.com/crazycs520)
    - 修复 `LEADING` hint 不支持查询块别名 (query block alias) 的问题 [#44645](https://github.com/pingcap/tidb/issues/44645) @[qw4990](https://github.com/qw4990)
    - 修复 `PREPARE stmt FROM "ANALYZE TABLE xxx"` 会被 `tidb_mem_quota_query` kill 掉的问题 [#44320](https://github.com/pingcap/tidb/issues/44320) @[chrysan](https://github.com/chrysan)
    - 修复 `processInfo` 为空导致的 panic 问题 [#43829](https://github.com/pingcap/tidb/issues/43829) @[zimulala](https://github.com/zimulala)
    - 修复 `ON UPDATE` 语句没有正确更新主键导致数据索引不一致的问题 [#44565](https://github.com/pingcap/tidb/issues/44565) @[zyguan](https://github.com/zyguan)
    - 修复开启 `tidb_opt_agg_push_down` 时查询可能返回错误结果的问题 [#44795](https://github.com/pingcap/tidb/issues/44795) @[AilinKid](https://github.com/AilinKid)
    - 修复同时使用 CTE 和关联子查询可能导致查询结果出错或者 panic 的问题 [#44649](https://github.com/pingcap/tidb/issues/44649) [#38170](https://github.com/pingcap/tidb/issues/38170) [#44774](https://github.com/pingcap/tidb/issues/44774) @[winoros](https://github.com/winoros) @[guo-shaoge](https://github.com/guo-shaoge)
    - 修复取消处于 rollback 状态的 DDL 任务导致相关元数据出错的问题 [#44143](https://github.com/pingcap/tidb/issues/44143) @[wjhuang2016](https://github.com/wjhuang2016)
    - 修复 `UPDATE` 语句因为检查外键约束导致执行报错的问题 [#44848](https://github.com/pingcap/tidb/issues/44848) @[crazycs520](https://github.com/crazycs520)

+ PD

    - 修复 Resource Manager 重复初始化 default 资源组的问题 [#6787](https://github.com/tikv/pd/issues/6787) @[glorv](https://github.com/glorv)
    - 修复 Placement Rules in SQL 设置的 `location-labels` 在特定条件下不按预期调度的问题 [#6662](https://github.com/tikv/pd/issues/6662) @[rleungx](https://github.com/rleungx)
    - 修复在特殊情况下冗余副本无法自动修复的问题 [#6573](https://github.com/tikv/pd/issues/6573) @[nolouch](https://github.com/nolouch)

+ TiFlash

    - 修复存算分离模式下，TiFlash 计算节点获取的 CPU 核数信息不准确的问题 [#7436](https://github.com/pingcap/tiflash/issues/7436) @[guo-shaoge](https://github.com/guo-shaoge)
    - 修复 TiFlash 在使用 Online Unsafe Recovery 之后重启时间过长的问题 [#7671](https://github.com/pingcap/tiflash/issues/7671) @[hongyunyan](https://github.com/hongyunyan)

+ Tools

    + Backup & Restore (BR)

        - 修复某些情况下误报 `checksum mismatch` 的问题 [#44472](https://github.com/pingcap/tidb/issues/44472) @[Leavrth](https://github.com/Leavrth)
        - 修复当 TiDB 集群不存在 PITR 备份任务时，`resolve lock` 频率过高的问题 [#40759](https://github.com/pingcap/tidb/issues/40759) @[joccau](https://github.com/joccau)

    + TiCDC

        - 修复 PD 异常时可能导致同步任务卡住的问题 [#8808](https://github.com/pingcap/tiflow/issues/8808) [#9054](https://github.com/pingcap/tiflow/issues/9054) @[asddongmen](https://github.com/asddongmen) @[fubinzh](https://github.com/fubinzh)
        - 修复同步到对象存储时内存消耗过大的问题 [#8894](https://github.com/pingcap/tiflow/issues/8894) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - 修复在打开 redo log 且下游出现异常时可能会导致同步任务卡住的问题 [#9172](https://github.com/pingcap/tiflow/issues/9172) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - 修复在下游出现故障时 TiCDC 持续重试导致重试时间过长的问题 [#9272](https://github.com/pingcap/tiflow/issues/9272) @[asddongmen](https://github.com/asddongmen)
        - 修复同步到 Kafka 场景下，读取下游 Metadata 太频繁导致下游压力过大的问题 [#8959](https://github.com/pingcap/tiflow/issues/8959) @[hi-rustin](https://github.com/Rustin170506)
        - 修复当下游为 Kafka 时，TiCDC 查询下游的元信息频率过高导致下游负载过大的问题 [#8957](https://github.com/pingcap/tiflow/issues/8957) [#8959](https://github.com/pingcap/tiflow/issues/8959) @[hi-rustin](https://github.com/Rustin170506)
        - 修复在某些特殊场景下 sorter 组件内存使用过多导致 OOM 的问题 [#8974](https://github.com/pingcap/tiflow/issues/8974) @[hicqu](https://github.com/hicqu)
        - 修复使用 Avro 或 CSV 协议场景下 `UPDATE` 操作不能输出旧值的问题 [#9086](https://github.com/pingcap/tiflow/issues/9086) @[3AceShowHand](https://github.com/3AceShowHand)
        - 修复同步数据到存储服务时，下游 DDL 语句对应的 JSON 文件中没有记录表中字段默认值的问题 [#9066](https://github.com/pingcap/tiflow/issues/9066) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - 修复同步到 TiDB 或 MySQL 场景下，频繁设置下游双向复制相关变量导致下游日志过多的问题 [#9180](https://github.com/pingcap/tiflow/issues/9180) @[asddongmen](https://github.com/asddongmen)
        - 修复当 Kafka 消息过大导致同步出错时，在 Log 中记录了消息体的问题 [#9031](https://github.com/pingcap/tiflow/issues/9031) @[darraes](https://github.com/darraes)
        - 修复 PD 出现网络隔离或 PD Owner 节点重启等故障时 TiCDC 卡住问题 [#8808](https://github.com/pingcap/tiflow/issues/8808) [#8812](https://github.com/pingcap/tiflow/issues/8812) [#8877](https://github.com/pingcap/tiflow/issues/8877) @[asddongmen](https://github.com/asddongmen)
        - 修复 Avro 协议识别到错误的 Enum 类型数据值的问题 [#9259](https://github.com/pingcap/tiflow/issues/9259) @[3AceShowHand](https://github.com/3AceShowHand)

    + TiDB Data Migration (DM)

        - 修复 DM-master 在迁移唯一索引包含空列的表时异常退出的问题 [#9247](https://github.com/pingcap/tiflow/issues/9247) @[lance6716](https://github.com/lance6716)

    + TiDB Lightning

        - 修复 TiDB Lightning 连接 PD 失败无法重试的问题，提高导入成功率 [#43400](https://github.com/pingcap/tidb/issues/43400) @[lichunzhu](https://github.com/lichunzhu)
        - 修复 TiDB Lightning 写入数据到 TiKV 返回空间不足的错误时无法正确显示错误信息的问题 [#44733](https://github.com/pingcap/tidb/issues/44733) @[lance6716](https://github.com/lance6716)
        - 修复 checksum 过程中报错 `Region is unavailable` 的问题 [#45462](https://github.com/pingcap/tidb/issues/45462) @[D3Hunter](https://github.com/D3Hunter)
        - 修复开启 `experimental.allow-expression-index` 且默认值是 UUID 时导致 TiDB Lightning panic 的问题 [#44497](https://github.com/pingcap/tidb/issues/44497) @[lichunzhu](https://github.com/lichunzhu)
        - 修复竞态条件可能导致磁盘配额 (disk quota) 不准确的问题 [#44867](https://github.com/pingcap/tidb/issues/44867) @[D3Hunter](https://github.com/D3Hunter)
        - 修复逻辑导入模式下，导入期间下游删除表可能导致 TiDB Lightning 元信息未及时更新的问题 [#44614](https://github.com/pingcap/tidb/issues/44614) @[dsdashun](https://github.com/dsdashun)

    + Dumpling

        - 修复 Dumpling 在 `--sql` 查询结果集为空时异常退出的问题 [#45200](https://github.com/pingcap/tidb/issues/45200) @[D3Hunter](https://github.com/D3Hunter)

    + TiDB Binlog

        - 修复 TiDB 在 PD 地址完全变更后无法通过 `SHOW PUMP STATUS` 或 `SHOW DRAINER STATUS` 正确查询 Binlog 节点状态的问题 [#42643](https://github.com/pingcap/tidb/issues/42643) @[lichunzhu](https://github.com/lichunzhu)
        - 修复 TiDB 在 PD 地址完全变更后无法写 binlog 的问题 [#42643](https://github.com/pingcap/tidb/issues/42643) @[lance6716](https://github.com/lance6716)
        - 修复 etcd client 初始化时没有自动同步最新节点信息的问题 [#1236](https://github.com/pingcap/tidb-binlog/issues/1236) @[lichunzhu](https://github.com/lichunzhu)
