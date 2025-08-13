---
title: TiDB 8.5.3 Release Notes
summary: 了解 TiDB 8.5.3 版本的兼容性变更、改进提升，以及错误修复。
---

# TiDB 8.5.3 Release Notes

发版日期：2025 年 8 月 14 日

TiDB 版本：8.5.3

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v8.5/quick-start-with-tidb) | [生产部署](https://docs.pingcap.com/zh/tidb/v8.5/production-deployment-using-tiup) | [下载离线包](https://cn.pingcap.com/product-community/?version=v8.5.3#version-list)

## 兼容性变更

- 新增以下用于[代价模型](/cost-model.md)内部使用的系统变量，**不建议**修改这些变量的值：[`tidb_opt_hash_agg_cost_factor`](https://docs.pingcap.com/zh/tidb/v8.5/system-variables/#tidb_opt_hash_agg_cost_factor-从-v853-和-v900-版本开始引入)、[`tidb_opt_hash_join_cost_factor`](https://docs.pingcap.com/zh/tidb/v8.5/system-variables/#tidb_opt_hash_join_cost_factor-从-v853-和-v900-版本开始引入)、[`tidb_opt_index_join_cost_factor`](https://docs.pingcap.com/zh/tidb/v8.5/system-variables/#tidb_opt_index_join_cost_factor-从-v853-和-v900-版本开始引入)、[`tidb_opt_index_lookup_cost_factor`](https://docs.pingcap.com/zh/tidb/v8.5/system-variables/#tidb_opt_index_lookup_cost_factor-从-v853-和-v900-版本开始引入)、[`tidb_opt_index_merge_cost_factor`](https://docs.pingcap.com/zh/tidb/v8.5/system-variables/#tidb_opt_index_merge_cost_factor-从-v853-和-v900-版本开始引入)、[`tidb_opt_index_reader_cost_factor`](https://docs.pingcap.com/zh/tidb/v8.5/system-variables/#tidb_opt_index_reader_cost_factor-从-v853-和-v900-版本开始引入)、[`tidb_opt_index_scan_cost_factor`](https://docs.pingcap.com/zh/tidb/v8.5/system-variables/#tidb_opt_index_scan_cost_factor-从-v853-和-v900-版本开始引入)、[`tidb_opt_limit_cost_factor`](https://docs.pingcap.com/zh/tidb/v8.5/system-variables/#tidb_opt_limit_cost_factor-从-v853-和-v900-版本开始引入)、[`tidb_opt_merge_join_cost_factor`](https://docs.pingcap.com/zh/tidb/v8.5/system-variables/#tidb_opt_merge_join_cost_factor-从-v853-和-v900-版本开始引入)、[`tidb_opt_sort_cost_factor`](https://docs.pingcap.com/zh/tidb/v8.5/system-variables/#tidb_opt_sort_cost_factor-从-v853-和-v900-版本开始引入)、[`tidb_opt_stream_agg_cost_factor`](https://docs.pingcap.com/zh/tidb/v8.5/system-variables/#tidb_opt_stream_agg_cost_factor-从-v853-和-v900-版本开始引入)、[`tidb_opt_table_full_scan_cost_factor`](https://docs.pingcap.com/zh/tidb/v8.5/system-variables/#tidb_opt_table_full_scan_cost_factor-从-v853-和-v900-版本开始引入)、[`tidb_opt_table_range_scan_cost_factor`](https://docs.pingcap.com/zh/tidb/v8.5/system-variables/#tidb_opt_table_range_scan_cost_factor-从-v853-和-v900-版本开始引入)、[`tidb_opt_table_reader_cost_factor`](https://docs.pingcap.com/zh/tidb/v8.5/system-variables/#tidb_opt_table_reader_cost_factor-从-v853-和-v900-版本开始引入)、[`tidb_opt_table_rowid_cost_factor`](https://docs.pingcap.com/zh/tidb/v8.5/system-variables/#tidb_opt_table_rowid_cost_factor-从-v853-和-v900-版本开始引入)、[`tidb_opt_table_tiflash_scan_cost_factor`](https://docs.pingcap.com/zh/tidb/v8.5/system-variables/#tidb_opt_table_tiflash_scan_cost_factor-从-v853-和-v900-版本开始引入)、[`tidb_opt_topn_cost_factor`](https://docs.pingcap.com/zh/tidb/v8.5/system-variables/#tidb_opt_topn_cost_factor-从-v853-和-v900-版本开始引入) [#60357](https://github.com/pingcap/tidb/issues/60357) @[terry1purcell](https://github.com/terry1purcell)
- 重新引入对[遥测](https://docs.pingcap.com/zh/tidb/v8.5/telemetry)功能的支持，但其行为已更改为仅将遥测相关信息输出到日志文件，不再通过网络发送给 PingCAP [#61766](https://github.com/pingcap/tidb/issues/61766) @[Defined2014](https://github.com/Defined2014)

## 改进提升

+ TiDB

    - 当某个统计信息完全由 TopN 构成，且对应表的统计信息中修改行数不为 0 时，对于未命中 TopN 的等值条件，估算结果从 0 调整为 1 [#47400](https://github.com/pingcap/tidb/issues/47400) @[terry1purcell](https://github.com/terry1purcell)
    - 提升使用全局排序添加唯一索引的性能，并优化添加重复唯一索引时的报错信息 [#61689](https://github.com/pingcap/tidb/issues/61689) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - 当 `IMPORT INTO` 启用全局排序时，禁用 TiKV 切换到导入模式 [#60361](https://github.com/pingcap/tidb/issues/60361) @[D3Hunter](https://github.com/D3Hunter)
    - 为索引添加过程新增监控指标，便于观察写入 TiKV 的速度 [#60925](https://github.com/pingcap/tidb/issues/60925) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - 优化 `merge sort` 子任务的调度逻辑，提升排序性能 [#60375](https://github.com/pingcap/tidb/issues/60375) @[tangenta](https://github.com/tangenta)
    - 提升创建大量带外键的表时的建表速度，并优化内存使用效率 [#61126](https://github.com/pingcap/tidb/issues/61126) @[GMHDBJD](https://github.com/GMHDBJD)
    - 提升 `information_schema.tables` 表的读取效率 [#62020](https://github.com/pingcap/tidb/issues/62020) @[tangenta](https://github.com/tangenta)
    - 新增数据导入期间 Region 分裂与数据 ingest 的流控接口 [#61553](https://github.com/pingcap/tidb/issues/61553) @[tangenta](https://github.com/tangenta)
    - 通过减少 `fmt.Sprintf()` 调用，优化 IndexScan 的计划构造流程 [#56649](https://github.com/pingcap/tidb/issues/56649) @[crazycs520](https://github.com/crazycs520)
    - 使用全局排序加索引时，增加 Merge Sort 阶段的监控信息 [#61025](https://github.com/pingcap/tidb/issues/61025) @[fzzf678](https://github.com/fzzf678)
    - 删除 IndexLookup 算子发生 `context canceled` 错误时冗余的日志信息 [#61072](https://github.com/pingcap/tidb/issues/61072) @[yibin87](https://github.com/yibin87)
    - 优化 `tidb_replica_read` 设置为 `closest-adaptive` 时的性能 [#61745](https://github.com/pingcap/tidb/issues/61745) @[you06](https://github.com/you06)
    - 通过减少大规模集群中监控指标 (metrics) 的数据量，降低运维成本 [#59990](https://github.com/pingcap/tidb/issues/59990) @[zimulala](https://github.com/zimulala)

+ TiKV

    - 支持在不阻塞前台写入的情况下导入 SST 文件，降低延迟带来的影响 [#18081](https://github.com/tikv/tikv/issues/18081) @[hhwyt](https://github.com/hhwyt)
    - 降低流量控制 (flow controller) 引发的性能抖动 [#18625](https://github.com/tikv/tikv/issues/18625) @[hhwyt](https://github.com/hhwyt)
    - 优化 TiDB 在执行 `ADD INDEX` 操作期间的尾延迟 [#18081](https://github.com/tikv/tikv/issues/18081) @[overvenus](https://github.com/overvenus)
    - 优化 Raftstore 中 `CompactedEvent` 的处理逻辑，将其移至 `split-check` worker 中执行，减少对 Raftstore 主线程的阻塞 [#18532](https://github.com/tikv/tikv/issues/18532) @[LykxSassinator](https://github.com/LykxSassinator)
    - 在 SST ingest 太慢时，仅输出 `SST ingest is experiencing slowdowns` 日志，不再调用 `get_sst_key_ranges` 打印详细 key range，以避免引发性能抖动 [#18549](https://github.com/tikv/tikv/issues/18549) @[LykxSassinator](https://github.com/LykxSassinator)
    - 优化 KvDB 和 RaftDB 分盘部署场景下 KvDB 磁盘 I/O 抖动的检测机制 [#18463](https://github.com/tikv/tikv/issues/18463) @[LykxSassinator](https://github.com/LykxSassinator)
    - 优化 Raft Engine 中 `fetch_entries_to` 的性能，减少竞争，提升混合负载下的执行性能 [#18605](https://github.com/tikv/tikv/issues/18605) @[LykxSassinator](https://github.com/LykxSassinator)
    - 优化残留数据清理机制，减少对请求延迟的影响 [#18107](https://github.com/tikv/tikv/issues/18107) @[LykxSassinator](https://github.com/LykxSassinator)

+ PD

    - 在 Prometheues 中新增 GO Runtime 相关监控指标 [#8931](https://github.com/tikv/pd/issues/8931) @[bufferflies](https://github.com/bufferflies)
    - 将触发慢节点驱逐 leader 后的恢复时间从 600 秒延长到 900 秒（15 分钟）[#9329](https://github.com/tikv/pd/issues/9329) @[rleungx](https://github.com/rleungx)

+ TiFlash

    - 增加 TiFlash 获取存储层快照的重试次数，以增强大表上查询的稳定性 [#10300](https://github.com/pingcap/tiflash/issues/10300) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 增强 TiFlash 在宽表场景下 OOM 风险相关的监测指标 [#10272](https://github.com/pingcap/tiflash/issues/10272) @[JaySon-Huang](https://github.com/JaySon-Huang)

+ Tools

    + Backup & Restore (BR)

        - 采用并行方式，提升 PITR 恢复过程中的索引修复速度 [#59158](https://github.com/pingcap/tidb/issues/59158) @[Leavrth](https://github.com/Leavrth)
        - TiKV 的 Download API 在下载备份文件时，支持过滤掉某段时间范围内的数据，以避免恢复时导入过旧或过新的数据版本 [#18399](https://github.com/tikv/tikv/issues/18399) @[3pointer](https://github.com/3pointer)
        - 支持按时间戳过滤日志备份的元数据文件，以缩短 PITR 恢复读取元数据的耗时 [#61318](https://github.com/pingcap/tidb/issues/61318) @[3pointer](https://github.com/3pointer)

## 错误修复

+ TiDB

    - 修复 `ALTER RANGE meta SET PLACEMENT POLICY` 的 key 范围错误的问题 [#60888](https://github.com/pingcap/tidb/issues/60888) @[nolouch](https://github.com/nolouch)
    - 修复在添加索引过程中减少 Worker 数量可能导致任务卡住的问题 [#59267](https://github.com/pingcap/tidb/issues/59267) @[D3Hunter](https://github.com/D3Hunter)
    - 修复 `ADMIN SHOW DDL JOBS` 语句无法正确显示行数的问题 [#59897](https://github.com/pingcap/tidb/issues/59897) @[tangenta](https://github.com/tangenta)
    - 修复在添加索引过程中动态调整 Worker 数量可能导致的数据竞争问题 [#59016](https://github.com/pingcap/tidb/issues/59016) @[D3Hunter](https://github.com/D3Hunter)
    - 修复 Grafana 中 **Stats Healthy Distribution** 面板的数据可能错误的问题 [#57176](https://github.com/pingcap/tidb/issues/57176) @[hawkingrei](https://github.com/hawkingrei)
    - 修复使用 `IMPORT INTO ... FROM SELECT` 导入 TiFlash 时发生错误的问题 [#58443](https://github.com/pingcap/tidb/issues/58443) @[D3Hunter](https://github.com/D3Hunter)
    - 修复启用 `tidb_enable_dist_task` 导致 TiDB 升级失败的问题 [#54061](https://github.com/pingcap/tidb/issues/54061) @[tangenta](https://github.com/tangenta)
    - 修复对统计信息的异常处理不当导致后台任务超时的时候，内存内的统计信息被误删除的问题 [#57901](https://github.com/pingcap/tidb/issues/57901) @[hawkingrei](https://github.com/hawkingrei)
    - 修复在分布式执行框架下执行添加索引操作没有正确更新行数的问题 [#58573](https://github.com/pingcap/tidb/issues/58573) @[D3Hunter](https://github.com/D3Hunter)
    - 修复执行有损 DDL 后，查询 TiFlash 数据结果不一致的问题 [#61455](https://github.com/pingcap/tidb/issues/61455) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - 修复使用 GCS 遇到 EOF 错误没有重试的问题 [#59754](https://github.com/pingcap/tidb/issues/59754) @[D3Hunter](https://github.com/D3Hunter)
    - 修复使用全局排序时遇到不合法的 KV 范围的问题 [#59841](https://github.com/pingcap/tidb/issues/59841) @[GMHDBJD](https://github.com/GMHDBJD)
    - 修复执行 `CREATE INDEX IF NOT EXISTS` 语句生成空索引名的问题 [#61265](https://github.com/pingcap/tidb/issues/61265) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - 修复禁用元数据锁 (Metadata Locking, MDL) 后，DDL 更新 schema 版本失败后卡住的问题 [#61210](https://github.com/pingcap/tidb/issues/61210) @[wjhuang2016](https://github.com/wjhuang2016)
    - 修复统计信息系统表展示非 `public` 索引的问题 [#60430](https://github.com/pingcap/tidb/issues/60430) @[tangenta](https://github.com/tangenta)
    - 修复 HashAgg 算子的 Memory Tracker 内存信息收集错误导致出现大量 ERROR 日志的问题 [#58822](https://github.com/pingcap/tidb/issues/58822) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - 修复 HashAgg 算子落盘过程中，`basePartialResult4GroupConcat` 中 buffer 为 `nil` 导致 panic 的问题 [#61749](https://github.com/pingcap/tidb/issues/61749) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - 修复聚合表达式计算过程中，编码逻辑返回值问题导致查询 panic 的问题 [#61735](https://github.com/pingcap/tidb/issues/61735) @[YangKeao](https://github.com/YangKeao)
    - 修复 HashJoin 算子因为内存超限导致的 Goroutine 泄露的问题 [#60926](https://github.com/pingcap/tidb/issues/60926) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - 修复 `IndexMerge` 和 `IndexLookUp` 算子下发查询时，共享 KV Request 导致数据竞争 (Data Race) 的问题 [#60175](https://github.com/pingcap/tidb/issues/60175) @[you06](https://github.com/you06)
    - 修复包含 `_charset(xxx), _charset(xxx2), ...` 的 SQL 语句生成不同 Digest 的问题 [#58447](https://github.com/pingcap/tidb/issues/58447) @[xhebox](https://github.com/xhebox)
    - 修复处理非法 UTF-8 字符时可能 panic 的问题 [#47521](https://github.com/pingcap/tidb/issues/47521) @[Defined2014](https://github.com/Defined2014)
    - 修复插入夏令时间戳时，非法时间戳变为 `0000-00-00` 的问题 [#61334](https://github.com/pingcap/tidb/issues/61334) @[mjonss](https://github.com/mjonss)
    - 修复使用 `INSERT IGNORE` 插入非法夏令时间戳且 `sql_mode` 为严格模式时，产生的时间戳与 MySQL 不一致的问题 [#61439](https://github.com/pingcap/tidb/issues/61439) @[mjonss](https://github.com/mjonss)
    - 修复频繁合并 Region 导致 TTL 任务无法启动的问题 [#61512](https://github.com/pingcap/tidb/issues/61512) @[YangKeao](https://github.com/YangKeao)
    - 修复 TiDB 在网络协议中返回的列信息长度可能为零的问题；若为零，则返回各字段类型的默认长度 [#60503](https://github.com/pingcap/tidb/issues/60503) @[xhebox](https://github.com/xhebox)
    - 修复网络协议中为 `blob` 类型返回的类型与 MySQL 不一致的问题 [#60195](https://github.com/pingcap/tidb/issues/60195) @[dveeden](https://github.com/dveeden)
    - 修复 `CAST()` 函数返回的长度与 MySQL 不兼容的问题 [#61350](https://github.com/pingcap/tidb/issues/61350) @[YangKeao](https://github.com/YangKeao)
    - 修复 `latin1_bin` 与 `utf8mb4_bin`、`utf8_bin` 的比较方式不相同的问题 [#60701](https://github.com/pingcap/tidb/issues/60701) @[hawkingrei](https://github.com/hawkingrei)
    - 修复在查询被终止时可能遗留下悲观锁的问题 [#61454](https://github.com/pingcap/tidb/issues/61454) @[zyguan](https://github.com/zyguan)
    - 修复 TiDB 在执行大查询时，可能因为单次从 PD 加载的 Region 数量过多而报错的问题 [#1704](https://github.com/tikv/client-go/issues/1704) @[you06](https://github.com/you06)

+ TiKV

    - 修复 TiKV 在正常退出时未能终止正在进行的手动 compaction 任务的问题 [#18396](https://github.com/tikv/tikv/issues/18396) @[LykxSassinator](https://github.com/LykxSassinator)
    - 修复升级集群后，默认 Region 大小被意外更改的问题 [#18503](https://github.com/tikv/tikv/issues/18503) @[LykxSassinator](https://github.com/LykxSassinator)
    - 修复 TiKV 可能使用客户端无法解码的压缩算法的问题 [#18079](https://github.com/tikv/tikv/issues/18079) @[ekexium](https://github.com/ekexium)
    - 修复关闭 Titan 后，Blob 索引可能导致 apply snapshot 失败的问题 [#18434](https://github.com/tikv/tikv/issues/18434) @[v01dstar](https://github.com/v01dstar)
    - 修复慢日志中 `StoreMsg` 日志信息存在误导性描述的问题 [#18561](https://github.com/tikv/tikv/issues/18561) @[LykxSassinator](https://github.com/LykxSassinator)
    - 修复高并发场景下 TiKV 过量放行 SST 导入请求的问题 [#18452](https://github.com/tikv/tikv/issues/18452) @[hbisheng](https://github.com/hbisheng)
    - 修复扫描锁时可能出现重复结果导致 TiKV panic 问题 [#16818](https://github.com/tikv/tikv/issues/16818) @[cfzjywxk](https://github.com/cfzjywxk)

+ PD

    - 修复慢节点检测机制中 `recovery-duration` 未生效的问题 [#9384](https://github.com/tikv/pd/issues/9384) @[rleungx](https://github.com/rleungx)
    - 修复 Evict Leader 调度器可能在集群升级后被错误暂停的问题 [#9416](https://github.com/tikv/pd/issues/9416) @[rleungx](https://github.com/rleungx)
    - 修复 TiDB Dashboard TCP 链接未正确关闭，导致 PD goroutine 泄露的问题 [#9402](https://github.com/tikv/pd/issues/9402) @[baurine](https://github.com/baurine)
    - 修复新上线的 TiKV 节点可能无法被调度问题 [#9145](https://github.com/tikv/pd/issues/9145) @[bufferflies](https://github.com/bufferflies)

+ TiFlash

    - 修复创建 `((NULL))` 形式的表达式索引会导致 TiFlash panic 的问题 [#9891](https://github.com/pingcap/tiflash/issues/9891) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复 Join 算子中因为 mutex 没有对齐导致 TiFlash 在特定系统环境下 crash 的问题 [#10163](https://github.com/pingcap/tiflash/issues/10163) @[windtalker](https://github.com/windtalker)
    - 修复 Resource Control Low Token Signal 丢失导致查询被限速的问题 [#10137](https://github.com/pingcap/tiflash/issues/10137) @[guo-shaoge](https://github.com/guo-shaoge)

+ Tools

    + Backup & Restore (BR)

        - 修复在断点恢复时额外检查存储节点可用空间的问题 [#54316](https://github.com/pingcap/tidb/issues/54316) @[Leavrth](https://github.com/Leavrth)
        - 修复从外部存储导入数据时，遇到 HTTP/2 GOAWAY 报错未自动重试的问题 [#60143](https://github.com/pingcap/tidb/issues/60143) @[joechenrh](https://github.com/joechenrh)
        - 修复恢复过程中因导入模式切换导致的 `keepalive watchdog timedout` 问题 [#18541](https://github.com/tikv/tikv/issues/18541) @[Leavrth](https://github.com/Leavrth)
        - 修复日志备份上传大量数据至 Azure Blob Storage 时速度缓慢的问题 [#18410](https://github.com/tikv/tikv/issues/18410) @[YuJuncen](https://github.com/YuJuncen)
        - 修复当指定了 `-f` 来过滤表时，BR 未检查集群内是否已存在对应表的问题 [#61592](https://github.com/pingcap/tidb/issues/61592) @[RidRisR](https://github.com/RidRisR)
        - 修复 PITR 无法恢复大于 3072 字节的索引的问题 [#58430](https://github.com/pingcap/tidb/issues/58430) @[YuJuncen](https://github.com/YuJuncen)
        - 修复在全量备份过程中 RangeTree 结果内存使用效率低下的问题 [#58587](https://github.com/pingcap/tidb/issues/58587) @[3pointer](https://github.com/3pointer)

    + TiCDC

        - 修复在包含虚拟列的表中计算事件过滤表达式时 panic 的问题 [#12206](https://github.com/pingcap/tiflow/issues/12206) @[lidezhu](https://github.com/lidezhu)
        - 修复在相同 IP 地址上扩缩容 TiKV 节点后，因使用过期的 store ID 导致 resolved ts 延迟持续上升的问题 [#12162](https://github.com/pingcap/tiflow/issues/12162) @[3AceShowHand](https://github.com/3AceShowHand)
        - 修复 dispatcher 配置中列名和索引名大小写敏感匹配的问题 [#12103](https://github.com/pingcap/tiflow/issues/12103) @[wk989898](https://github.com/wk989898)
        - 修复使用 Debezium 协议配置 column-selector 时 panic 的问题 [#12208](https://github.com/pingcap/tiflow/issues/12208) @[wk989898](https://github.com/wk989898)

    + TiDB Lightning

        - 修复 TiDB Lightning 向 TiKV 发起的 RPC 请求超时后返回 `context deadline exceeded` 的问题 [#61326](https://github.com/pingcap/tidb/issues/61326) @[OliverS929](https://github.com/OliverS929)
