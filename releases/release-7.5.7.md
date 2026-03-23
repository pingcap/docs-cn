---
title: TiDB 7.5.7 Release Notes
summary: 了解 TiDB 7.5.7 版本的兼容性变更、改进提升，以及错误修复。
---

# TiDB 7.5.7 Release Notes

发版日期：2025 年 9 月 4 日

TiDB 版本：7.5.7

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v7.5/quick-start-with-tidb) | [生产部署](https://docs.pingcap.com/zh/tidb/v7.5/production-deployment-using-tiup) | [下载离线包](https://pingkai.cn/download#tidb-community)

## 兼容性变更

- 将系统变量 [`tidb_enable_historical_stats`](https://docs.pingcap.com/zh/tidb/v7.5/system-variables/#tidb_enable_historical_stats) 的默认值从 `ON` 修改为 `OFF`，即默认关闭历史统计信息，避免潜在的稳定性问题 [#53048](https://github.com/pingcap/tidb/issues/53048) @[hawkingrei](https://github.com/hawkingrei)
- TiKV 废弃以下配置项，并由新的 [`gc.auto-compaction`](https://docs.pingcap.com/zh/tidb/v7.5/tikv-configuration-file/#gcauto-compaction) 配置项替代，用于控制自动 compaction 行为 [#18727](https://github.com/tikv/tikv/issues/18727) @[v01dstar](https://github.com/v01dstar)

    - 废弃配置项：[`region-compact-check-interval`](https://docs.pingcap.com/zh/tidb/v7.5/tikv-configuration-file#region-compact-check-interval)、[`region-compact-check-step`](https://docs.pingcap.com/zh/tidb/v7.5/tikv-configuration-file#region-compact-check-step)、[`region-compact-min-tombstones`](https://docs.pingcap.com/zh/tidb/v7.5/tikv-configuration-file#region-compact-min-tombstones)、[`region-compact-tombstones-percent`](https://docs.pingcap.com/zh/tidb/v7.5/tikv-configuration-file#region-compact-tombstones-percent)、[`region-compact-min-redundant-rows`](https://docs.pingcap.com/zh/tidb/v7.5/tikv-configuration-file#region-compact-min-redundant-rows-从-v710-版本开始引入) 和 [`region-compact-redundant-rows-percent`](https://docs.pingcap.com/zh/tidb/v7.5/tikv-configuration-file#region-compact-redundant-rows-percent-从-v710-版本开始引入)。
    - 新增配置项：[`gc.auto-compaction.check-interval`](https://docs.pingcap.com/zh/tidb/v7.5/tikv-configuration-file#check-interval-从-v757-版本开始引入)、[`gc.auto-compaction.tombstone-num-threshold`](https://docs.pingcap.com/zh/tidb/v7.5/tikv-configuration-file#tombstone-num-threshold-从-v757-版本开始引入)、[`gc.auto-compaction.tombstone-percent-threshold`](https://docs.pingcap.com/zh/tidb/v7.5/tikv-configuration-file#tombstone-percent-threshold-从-v757-版本开始引入)、[`gc.auto-compaction.redundant-rows-threshold`](https://docs.pingcap.com/zh/tidb/v7.5/tikv-configuration-file#redundant-rows-threshold-从-v757-版本开始引入)、[`gc.auto-compaction.redundant-rows-percent-threshold`](https://docs.pingcap.com/zh/tidb/v7.5/tikv-configuration-file#redundant-rows-percent-threshold-从-v757-版本开始引入) 和 [`gc.auto-compaction.bottommost-level-force`](https://docs.pingcap.com/zh/tidb/v7.5/tikv-configuration-file#bottommost-level-force-从-v757-版本开始引入)。

## 改进提升

+ TiDB

    - 新增数据导入期间 Region 分裂与数据 ingest 的流控接口 [#61553](https://github.com/pingcap/tidb/issues/61553) @[tangenta](https://github.com/tangenta)
    - 优化对大数据量的表进行简单查询时获取数据分布信息的性能 [#53850](https://github.com/pingcap/tidb/issues/53850) @[you06](https://github.com/you06)
    - 为索引添加过程新增监控指标，便于观察写入 TiKV 的速度 [#60925](https://github.com/pingcap/tidb/issues/60925) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - 优化 DML 在 DDL 执行期间的加锁逻辑，减少 DML 与 DDL 的锁冲突，提高部分场景下 DDL 的性能。但是由于引入了额外的二级索引加锁操作，可能会导致 DML 性能轻微下降 [#62337](https://github.com/pingcap/tidb/issues/62337) @[lcwangchao](https://github.com/lcwangchao)
    - 改进当系统变量 [`tidb_opt_ordering_index_selectivity_threshold`](/system-variables.md#tidb_opt_ordering_index_selectivity_threshold-从-v700-版本开始引入) 的值设置为 `1` 时的行为，增强该变量的控制能力 [#60242](https://github.com/pingcap/tidb/issues/60242) @[time-and-fate](https://github.com/time-and-fate)
    - 避免 `ANALYZE` 语句执行完成后需要刷新整个集群的统计信息，从而缩短 `ANALYZE` 的执行时间 [#57631](https://github.com/pingcap/tidb/issues/57631) @[0xPoe](https://github.com/0xPoe)
    - 常量折叠支持在带有 `NOT NULL` 约束的列上，将 `IS NULL` 计算折叠为 `FALSE` [#62050](https://github.com/pingcap/tidb/issues/62050) @[hawkingrei](https://github.com/hawkingrei)
    - 优化器支持在更多类型的 `JOIN` 中进行常量传播 [#51700](https://github.com/pingcap/tidb/issues/51700) @[hawkingrei](https://github.com/hawkingrei)
    - 优化在 DML 与 DDL 存在大量锁冲突时，合并临时索引 (temp index) 的性能 [#61433](https://github.com/pingcap/tidb/issues/61433) @[tangenta](https://github.com/tangenta)

+ TiKV

    - 优化 TiKV compaction 的触发逻辑，按回收效率排序对所有数据段依次处理，降低 MVCC 冗余数据对性能的影响 [#18571](https://github.com/tikv/tikv/issues/18571) @[v01dstar](https://github.com/v01dstar)
    - 优化在存在大量 SST 文件的环境中 async snapshot 和 write 的尾延迟 [#18743](https://github.com/tikv/tikv/issues/18743) @[Connor1996](https://github.com/Connor1996)
    - 优化空表和小 Region 场景下 Region Merge 的速度 [#17376](https://github.com/tikv/tikv/issues/17376) @[LykxSassinator](https://github.com/LykxSassinator)
    - 优化 Raftstore 中 `CompactedEvent` 的处理逻辑，将其移至 `split-check` worker 中执行，减少对 Raftstore 主线程的阻塞 [#18532](https://github.com/tikv/tikv/issues/18532) @[LykxSassinator](https://github.com/LykxSassinator)
    - 增加每个线程内存使用量的监控指标 [#15927](https://github.com/tikv/tikv/issues/15927) @[Connor1996](https://github.com/Connor1996)
    - 在 SST ingest 太慢时，仅输出 `SST ingest is experiencing slowdowns` 日志，不再调用 `get_sst_key_ranges` 打印详细 key range，以避免引发性能抖动 [#18549](https://github.com/tikv/tikv/issues/18549) @[LykxSassinator](https://github.com/LykxSassinator)
    - 优化 TiKV 重启时由于需要等待应用之前的日志而造成访问延时抖动的情况，提升了 TiKV 的稳定性 [#15874](https://github.com/tikv/tikv/issues/15874) @[LykxSassinator](https://github.com/LykxSassinator)
    - 优化残留数据清理机制，减少对请求延迟的影响 [#18107](https://github.com/tikv/tikv/issues/18107) @[LykxSassinator](https://github.com/LykxSassinator)
    - 优化 Raft Engine 中 `fetch_entries_to` 的性能，减少竞争，提升混合负载下的执行性能 [#18605](https://github.com/tikv/tikv/issues/18605) @[LykxSassinator](https://github.com/LykxSassinator)
    - 支持在线更改写入流量控制 (flow-control) 的相关配置 [#17395](https://github.com/tikv/tikv/issues/17395) @[glorv](https://github.com/glorv)
    - 支持在不阻塞前台写入的情况下导入 SST 文件，降低延迟带来的影响 [#18081](https://github.com/tikv/tikv/issues/18081) @[hhwyt](https://github.com/hhwyt)
    - 优化 KvDB 和 RaftDB 分盘部署场景下 KvDB 磁盘 I/O 抖动的检测机制 [#18463](https://github.com/tikv/tikv/issues/18463) @[LykxSassinator](https://github.com/LykxSassinator)
    - 增加 peer 和 store 消息的 slow log [#16600](https://github.com/tikv/tikv/issues/16600) @[Connor1996](https://github.com/Connor1996)

+ PD

    - 在 Prometheus 中新增 GO Runtime 相关监控指标 [#8931](https://github.com/tikv/pd/issues/8931) @[bufferflies](https://github.com/bufferflies)
    - 减少非必要的错误日志 [#9370](https://github.com/tikv/pd/issues/9370) @[bufferflies](https://github.com/bufferflies)

+ TiFlash

    - 增强 TiFlash 在宽表场景下 OOM 风险相关的监测指标 [#10272](https://github.com/pingcap/tiflash/issues/10272) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 增加 TiFlash 获取存储层快照的重试次数，以增强大表上查询的稳定性 [#10300](https://github.com/pingcap/tiflash/issues/10300) @[JaySon-Huang](https://github.com/JaySon-Huang)

+ Tools

    + Backup & Restore (BR)

        - 在 Amazon EC2 上部署 TiDB 时，BR 支持 AWS 的 Instance Metadata Service Version 2 (IMDSv2)。你可以在 EC2 实例上进行相关配置，使 BR 可以使用与实例关联的 IAM 角色以适当的权限访问 Amazon S3 [#16443](https://github.com/tikv/tikv/issues/16443) @[pingyu](https://github.com/pingyu)
        - TiKV 的 Download API 在下载备份文件时，支持过滤掉某段时间范围内的数据，以避免恢复时导入过旧或过新的数据版本 [#18399](https://github.com/tikv/tikv/issues/18399) @[3pointer](https://github.com/3pointer)

## 错误修复

+ TiDB

    - 修复 `IndexMerge` 和 `IndexLookUp` 算子下发查询时，共享 KV Request 导致数据竞争 (Data Race) 的问题 [#60175](https://github.com/pingcap/tidb/issues/60175) @[you06](https://github.com/you06)
    - 修复 Hash Aggregation 算子可能存在 goroutine 泄漏的问题 [#58004](https://github.com/pingcap/tidb/issues/58004) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - 修复当生成列上的索引设置为可见时，可能无法选中 MPP 计划的问题 [#47766](https://github.com/pingcap/tidb/issues/47766) @[AilinKid](https://github.com/AilinKid)
    - 修复包含 `_charset(xxx), _charset(xxx2), ...` 的 SQL 语句生成不同 Digest 的问题 [#58447](https://github.com/pingcap/tidb/issues/58447) @[xhebox](https://github.com/xhebox)
    - 修复频繁合并 Region 导致 TTL 任务无法启动的问题 [#61512](https://github.com/pingcap/tidb/issues/61512) @[YangKeao](https://github.com/YangKeao)
    - 修复执行有损 DDL 后，查询 TiFlash 数据结果不一致的问题 [#61455](https://github.com/pingcap/tidb/issues/61455) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - 修复 `ALTER RANGE meta SET PLACEMENT POLICY` 的 key 范围错误的问题 [#60888](https://github.com/pingcap/tidb/issues/60888) @[nolouch](https://github.com/nolouch)
    - 修复 Grafana 中 **Stats Healthy Distribution** 面板的数据可能错误的问题 [#57176](https://github.com/pingcap/tidb/issues/57176) @[hawkingrei](https://github.com/hawkingrei)
    - 修复 `latin1_bin` 与 `utf8mb4_bin`、`utf8_bin` 的比较方式不相同的问题 [#60701](https://github.com/pingcap/tidb/issues/60701) @[hawkingrei](https://github.com/hawkingrei)
    - 修复禁用元数据锁 (Metadata Locking, MDL) 后，DDL 更新 schema 版本失败后卡住的问题 [#61210](https://github.com/pingcap/tidb/issues/61210) @[wjhuang2016](https://github.com/wjhuang2016)
    - 修复 Redact 日志开启后在部分场景不生效的问题 [#59279](https://github.com/pingcap/tidb/issues/59279) @[tangenta](https://github.com/tangenta)
    - 修复当 Fix Control #44855 开启时，TiDB 的会话可能崩溃的问题 [#59762](https://github.com/pingcap/tidb/issues/59762) @[winoros](https://github.com/winoros)
    - 删除 IndexLookup 算子发生 `context canceled` 错误时冗余的日志信息 [#61072](https://github.com/pingcap/tidb/issues/61072) @[yibin87](https://github.com/yibin87)
    - 修复对统计信息的异常处理不当导致后台任务超时的时候，内存内的统计信息被误删除的问题 [#57901](https://github.com/pingcap/tidb/issues/57901) @[hawkingrei](https://github.com/hawkingrei)
    - 修复执行 `ADD UNIQUE INDEX` 可能导致数据不一致的问题 [#60339](https://github.com/pingcap/tidb/issues/60339) @[tangenta](https://github.com/tangenta)
    - 修复统计信息系统表展示非 `public` 索引的问题 [#60430](https://github.com/pingcap/tidb/issues/60430) @[tangenta](https://github.com/tangenta)
    - 修复 `PhysicalExchangeSender.HashCol` 浅拷贝 (Shallow Copy) 导致的 TiFlash crash 或者结果错误的问题 [#60517](https://github.com/pingcap/tidb/issues/60517) @[windtalker](https://github.com/windtalker)
    - 修复 `BIT` 类型表的统计信息无法加载的问题 [#62289](https://github.com/pingcap/tidb/issues/62289) @[YangKeao](https://github.com/YangKeao)
    - 修复无法将 `BIT` 类型的列的统计信息加载入内存的问题 [#59759](https://github.com/pingcap/tidb/issues/59759) @[YangKeao](https://github.com/YangKeao)
    - 修复 Hash Join v1 算子的 `Close()` 方法 panic 时没有恢复的问题 [#60926](https://github.com/pingcap/tidb/issues/60926) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - 修复极端情况下当 `ANALYZE` 语句的落盘操作耗时太长时，可能导致其他 TiDB 节点无法更新最新统计信息的问题 [#54552](https://github.com/pingcap/tidb/issues/54552) @[0xPoe](https://github.com/0xPoe)
    - 修复当收集的列统计信息完全为 TopN 时，即使有后续写入操作，估算也有可能一直为 0 的问题 [#47400](https://github.com/pingcap/tidb/issues/47400) @[terry1purcell](https://github.com/terry1purcell)
    - 修复 `explain format="cost_trace"` 展示的估算代价可能有误的问题 [#61155](https://github.com/pingcap/tidb/issues/61155) @[hawkingrei](https://github.com/hawkingrei)
    - 修复 `explain format="cost_trace"` 展示的代价计算公式中可能包含空括号的问题 [#61127](https://github.com/pingcap/tidb/issues/61127) @[hawkingrei](https://github.com/hawkingrei)
    - 修复外键定义成环时的死循环问题 [#60985](https://github.com/pingcap/tidb/issues/60985) @[hawkingrei](https://github.com/hawkingrei)
    - 修复内部查询在使用 `NULL` 构造索引范围查询时可能构造能力不足的问题 [#62196](https://github.com/pingcap/tidb/issues/62196) @[hawkingrei](https://github.com/hawkingrei)
    - 修复 Plan Cache 缓存了错误的执行计划导致执行报错的问题 [#56772](https://github.com/pingcap/tidb/issues/56772) @[dash12653](https://github.com/dash12653)
    - 修复估算跨月或跨年的行数时，结果可能过分偏大的问题 [#50080](https://github.com/pingcap/tidb/issues/50080) @[terry1purcell](https://github.com/terry1purcell)
    - 修复 `ANALYZE` 子任务并发数大幅超出设置的上限的问题 [#61785](https://github.com/pingcap/tidb/issues/61785) @[hawkingrei](https://github.com/hawkingrei)
    - 修复在 TopN 下推过程中错误地生成带表达式的 TopN 排序项 [#60655](https://github.com/pingcap/tidb/issues/60655) @[hawkingrei](https://github.com/hawkingrei)
    - 修复当缺少列或索引的统计信息时，TiDB 可能在后台打印 panic 日志的问题 [#61733](https://github.com/pingcap/tidb/issues/61733) @[winoros](https://github.com/winoros)
    - 修复当缺少列或索引的统计信息时，`JOIN` 的行数估算可能偏差过大的问题 [#61602](https://github.com/pingcap/tidb/issues/61602) @[qw4990](https://github.com/qw4990)
    - 修复系统变量 `tidb_cost_model_version` 的默认值设置错误的问题 [#61565](https://github.com/pingcap/tidb/issues/61565) @[hawkingrei](https://github.com/hawkingrei)
    - 修复当表的第一列为虚拟生成列时，统计信息可能出错的问题 [#61606](https://github.com/pingcap/tidb/issues/61606) @[winoros](https://github.com/winoros)
    - 修复错误地跳过 Plan Cache，并出现谓词简化的问题 [#61513](https://github.com/pingcap/tidb/issues/61513) @[hawkingrei](https://github.com/hawkingrei)
    - 修复加索引时执行 `ADMIN CANCEL DDL JOBS` 导致加索引卡住的问题 [#61087](https://github.com/pingcap/tidb/issues/61087) @[tangenta](https://github.com/tangenta)
    - 修复在某些内部 SQL 执行失败后，`ADMIN CHECK` 仍然返回成功的问题 [#61612](https://github.com/pingcap/tidb/issues/61612) @[joechenrh](https://github.com/joechenrh)
    - 修复通过 multi-schema change 加多个索引后，数据索引不一致的问题 [#61255](https://github.com/pingcap/tidb/issues/61255) @[tangenta](https://github.com/tangenta)

+ TiKV

    - 修复 CPU profiling 期间可能触发死锁的问题 [#18474](https://github.com/tikv/tikv/issues/18474) @[YangKeao](https://github.com/YangKeao)
    - 修复 Online Unsafe Recovery 可能被某些 TiFlash 副本阻塞，导致 commit index 无法推进的问题 [#18197](https://github.com/tikv/tikv/issues/18197) @[v01dstar](https://github.com/v01dstar)
    - 修复 TiKV 可能使用客户端无法解码的压缩算法的问题 [#18079](https://github.com/tikv/tikv/issues/18079) @[ekexium](https://github.com/ekexium)
    - 修复高并发场景下 TiKV 过量放行 SST 导入请求的问题 [#18452](https://github.com/tikv/tikv/issues/18452) @[hbisheng](https://github.com/hbisheng)
    - 修复 Grafana TiKV 组件中的 `Ingestion picked level` 和 `Compaction Job Size(files)` 显示不正确的问题 [#15990](https://github.com/tikv/tikv/issues/15990) @[Connor1996](https://github.com/Connor1996)
    - 修复 TiKV 重启后出现非预期的 `Server is busy` 报错 [#18233](https://github.com/tikv/tikv/issues/18233) @[LykxSassinator](https://github.com/LykxSassinator)
    - 修复巴西和埃及时区转换错误的问题 [#16220](https://github.com/tikv/tikv/issues/16220) @[overvenus](https://github.com/overvenus)
    - 修复慢日志中 `StoreMsg` 日志信息存在误导性描述的问题 [#18561](https://github.com/tikv/tikv/issues/18561) @[LykxSassinator](https://github.com/LykxSassinator)
    - 修复错误的线程内存监控指标 [#18125](https://github.com/tikv/tikv/issues/18125) @[Connor1996](https://github.com/Connor1996)
    - 修复 TiKV 在正常退出时未能终止正在进行的手动 compaction 任务的问题 [#18396](https://github.com/tikv/tikv/issues/18396) @[LykxSassinator](https://github.com/LykxSassinator)

+ PD

    - 修复反复修改 `split-merge-interval` 的值（例如从 `1s` 改为 `1h`，再改回 `1s`）可能导致该配置不生效的问题 [#8404](https://github.com/tikv/pd/issues/8404) @[lhy1024](https://github.com/lhy1024)
    - 修复 `lease` 默认值未被正确设置的问题 [#9156](https://github.com/tikv/pd/issues/9156) @[rleungx](https://github.com/rleungx)
    - 修复 TiDB Dashboard TCP 链接未正确关闭，导致 PD goroutine 泄露的问题 [#9402](https://github.com/tikv/pd/issues/9402) @[baurine](https://github.com/baurine)
    - 修复新上线的 TiKV 节点可能无法被调度问题 [#9145](https://github.com/tikv/pd/issues/9145) @[bufferflies](https://github.com/bufferflies)
    - 修复开启 `tidb_enable_tso_follower_proxy` 后，TSO 服务可能不可用的问题 [#9188](https://github.com/tikv/pd/issues/9188) @[Tema](https://github.com/Tema)

+ TiFlash

    - 修复在运行 `IMPORT INTO` 或 `BR restore` 的时候，部分 SST 文件可能被意外删除导致 TiFlash panic 的问题 [#10141](https://github.com/pingcap/tiflash/issues/10141) @[CalvinNeo](https://github.com/CalvinNeo)
    - 修复创建 `((NULL))` 形式的表达式索引会导致 TiFlash panic 的问题 [#9891](https://github.com/pingcap/tiflash/issues/9891) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复 TiFlash 处理带有不规则 key-range 的 Region snapshot 时可能 panic 的问题 [#10147](https://github.com/pingcap/tiflash/issues/10147) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复当集群的表中存在大量 `ENUM` 类型列时，TiFlash 的内存可能会大量消耗问题 [#9947](https://github.com/pingcap/tiflash/issues/9947) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复插入单行超过 16 MiB 的数据后，TiFlash 可能无法正常重启的问题 [#10052](https://github.com/pingcap/tiflash/issues/10052) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复 Resource Control Low Token Signal 丢失导致查询被限速的问题 [#10137](https://github.com/pingcap/tiflash/issues/10137) @[guo-shaoge](https://github.com/guo-shaoge)
    - 修复执行包含 `GROUP BY ... WITH ROLLUP` 的 SQL 语句时，可能会出现 `Exception: Block schema mismatch` 报错的问题 [#10110](https://github.com/pingcap/tiflash/issues/10110) @[gengliqi](https://github.com/gengliqi)

+ Tools

    + Backup & Restore (BR)

        - 修复 PITR 无法恢复大于 3072 字节的索引的问题 [#58430](https://github.com/pingcap/tidb/issues/58430) @[YuJuncen](https://github.com/YuJuncen)
        - 修复日志备份上传大量数据至 Azure Blob Storage 时速度缓慢的问题 [#18410](https://github.com/tikv/tikv/issues/18410) @[YuJuncen](https://github.com/YuJuncen)
        - 修复当指定了 `-f` 来过滤表时，BR 未检查集群内是否已存在对应表的问题 [#61592](https://github.com/pingcap/tidb/issues/61592) @[RidRisR](https://github.com/RidRisR)

    + TiCDC

        - 修复当使用外部存储作为下游时 Changefeed 可能会卡住的问题 [#9162](https://github.com/pingcap/tiflow/issues/9162) @[asddongmen](https://github.com/asddongmen)
        - 修复同步流量超过了下游 Kafka 的流量阀值后，Changefeed 可能会卡住的问题 [#12110](https://github.com/pingcap/tiflow/issues/12110) @[3AceShowHand](https://github.com/3AceShowHand)
        - 修复使用 `--overwrite-checkpoint-ts` 参数执行 `changefeed pause` 命令可能导致 Changefeed 卡住的问题 [#12055](https://github.com/pingcap/tiflow/issues/12055) @[hongyunyan](https://github.com/hongyunyan)
        - 修复在包含虚拟列的表中计算事件过滤表达式时 panic 的问题 [#12206](https://github.com/pingcap/tiflow/issues/12206) @[lidezhu](https://github.com/lidezhu)
        - 修复 dispatcher 配置中列名和索引名大小写敏感匹配的问题 [#12103](https://github.com/pingcap/tiflow/issues/12103) @[wk989898](https://github.com/wk989898)
        - 修复在相同 IP 地址上扩缩容 TiKV 节点后，因使用过期的 store ID 导致 resolved ts 延迟持续上升的问题 [#12162](https://github.com/pingcap/tiflow/issues/12162) @[3AceShowHand](https://github.com/3AceShowHand)

    + TiDB Lightning

        - 修复将 Parquet 文件从云存储导入到 TiDB 时，TiDB Lightning 可能会卡住达数小时的问题 [#60224](https://github.com/pingcap/tidb/issues/60224) @[joechenrh](https://github.com/joechenrh)
        - 修复 TiDB Lightning 向 TiKV 发起的 RPC 请求超时后返回 `context deadline exceeded` 的问题 [#61326](https://github.com/pingcap/tidb/issues/61326) @[OliverS929](https://github.com/OliverS929)

    + NG Monitoring

        - 修复 TSDB 在高时序基数下内存占用高的问题，提供 TSDB 内存配置项 [#295](https://github.com/pingcap/ng-monitoring/issues/295) @[mornyx](https://github.com/mornyx)
