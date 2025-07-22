---
title: TiDB 8.5.3 Release Notes
summary: 了解 TiDB 8.5.3 版本的兼容性变更、改进提升，以及错误修复。
---

# TiDB 8.5.3 Release Notes

发版日期：2025 年 x 月 x 日

TiDB 版本：8.5.3

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v8.5/quick-start-with-tidb) | [生产部署](https://docs.pingcap.com/zh/tidb/v8.5/production-deployment-using-tiup) | [下载离线包](https://cn.pingcap.com/product-community/?version=v8.5.3#version-list)

## 兼容性变更

- note [#issue](https://github.com/pingcap/${repo-name}/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
- 重新引入了 telemetry 功能支持，但对其实现方式进行了优化：将原有的网络上报机制调整为本地日志输出方式 [#61766](https://github.com/pingcap/tidb/issues/61766) @[Defined2014](https://github.com/Defined2014)

## 改进提升

+ TiDB

    - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - (dup): release-7.5.5.md > 改进提升> TiDB - 当某个统计信息完全由 TopN 构成，且对应表的统计信息中修改行数不为 0 时，对于未命中 TopN 的等值条件，估算结果从 0 调整为 1 [#47400](https://github.com/pingcap/tidb/issues/47400) @[terry1purcell](https://github.com/terry1purcell)
    - 提升使用全局排序添加唯一索引的性能，并优化添加重复唯一索引的报错信息 [#61689](https://github.com/pingcap/tidb/issues/61689) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - import into 使用全局排序时，禁用 TiKV 切换到导入模式 [#60361](https://github.com/pingcap/tidb/issues/60361) @[D3Hunter](https://github.com/D3Hunter)
    - 新增加索引的导入速度监控 [#60925](https://github.com/pingcap/tidb/issues/60925) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - 优化预读缓冲区的使用，提升读取效率 [#59754](https://github.com/pingcap/tidb/issues/59754) @[lance6716](https://github.com/lance6716)
    - 优化 merge sort 子任务的分发逻辑，提升速度 [#60375](https://github.com/pingcap/tidb/issues/60375) @[tangenta](https://github.com/tangenta)
    - 提升创建大量外建表的建表速度并优化内存使用 [#61126](https://github.com/pingcap/tidb/issues/61126) @[GMHDBJD](https://github.com/GMHDBJD)
    - 优化读取 tables 系统表的速度 [#62020](https://github.com/pingcap/tidb/issues/62020) @[tangenta](https://github.com/tangenta)
    - 新增导入期间分裂 region 和 ingest 数据的流控接口 [#61553](https://github.com/pingcap/tidb/issues/61553) @[tangenta](https://github.com/tangenta)
    
+ TiKV

    - 支持在不阻塞前台写入的情况下导入 SST 文件，降低延迟影响 [#18081](https://github.com/tikv/tikv/issues/18081) @[hhwyt](https://github.com/hhwyt)
    - 修复 flow controller 引发的延迟抖动问题 [#18625](https://github.com/tikv/tikv/issues/18625) @[hhwyt](https://github.com/hhwyt)
    - 优化 TiDB 执行 `ADD INDEX` 操作期间的尾延迟 [#18081](https://github.com/tikv/tikv/issues/18081) @[overvenus](https://github.com/overvenus)
    - 修复 TiKV 正常退出时未能中止正在进行的手动 Compaction 任务的问题 [#18396](https://github.com/tikv/tikv/issues/18396) @[LykxSassinator](https://github.com/LykxSassinator)
    - 优化 raftstore 中 `CompactedEvent` 的处理逻辑，将其移至 `split-check` worker 执行 [#18532](https://github.com/tikv/tikv/issues/18532) @[LykxSassinator](https://github.com/LykxSassinator)
    - 移除 “sst ingest is too slow” 的日志，避免引发性能抖动 [#18549](https://github.com/tikv/tikv/issues/18549) @[LykxSassinator](https://github.com/LykxSassinator)
    - 改进分盘部署场景下 kvdb 磁盘 I/O 抖动的检测机制 [#18463](https://github.com/tikv/tikv/issues/18463) @[LykxSassinator](https://github.com/LykxSassinator)
    - 优化 Raft-Engine 中 `fetch_entries_to` 的性能，减少竞争，提升混合负载下的执行性能 [#18605](https://github.com/tikv/tikv/issues/18605) @[LykxSassinator](https://github.com/LykxSassinator)
    - (dup): release-9.0.0.md > 改进提升> TiKV - 优化残留数据清理机制，减少对请求延迟的影响 [#18107](https://github.com/tikv/tikv/issues/18107) @[LykxSassinator](https://github.com/LykxSassinator)

+ PD

    - 增加了 GO Runtime 相关监控 [#8931](https://github.com/tikv/pd/issues/8931) @[bufferflies](https://github.com/bufferflies)
    - 延长了触发慢节点驱逐 leader 后的恢复时间 [#9329](https://github.com/tikv/pd/issues/9329) @[rleungx](https://github.com/rleungx)
    - 优化了 balance region 调度器的算分公式 [#9145](https://github.com/tikv/pd/issues/9145) @[bufferflies](https://github.com/bufferflies)

+ TiFlash

    - note [#issue](https://github.com/pingcap/tiflash/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/pingcap/tiflash/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - 增加 TiFlash 获取存储层快照重试次数来增强大表上查询的稳定性 [#10300](https://github.com/pingcap/tiflash/issues/10300) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 增强 TiFlash 在宽表场景下 OOM 风险相关的监测指标 [#10272](https://github.com/pingcap/tiflash/issues/10272) @[JaySon-Huang](https://github.com/JaySon-Huang)

+ Tools

    + Backup & Restore (BR)

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - (dup): release-9.0.0.md > 改进提升> Tools> Backup & Restore (BR) - 采用并行方式，提升 PITR 恢复过程中的索引修复速度 [#59158](https://github.com/pingcap/tidb/issues/59158) @[Leavrth](https://github.com/Leavrth)
        - 如今，TiKV 的 Download API 支持裁切掉 SST 中某段时间的数据 [#18399](https://github.com/tikv/tikv/issues/18399) @[3pointer](https://github.com/3pointer)
        - 通过过滤元数据文件，优化了 PiTR 恢复读取元数据的耗时 [#61318](https://github.com/pingcap/tidb/issues/61318) @[3pointer](https://github.com/3pointer)
        - 如今即便指定了 `-f` 来过滤表，BR 也会对集群内是否存在表进行检查 [#61592](https://github.com/pingcap/tidb/issues/61592) @[RidRisR](https://github.com/RidRisR)

    + TiCDC

        - 修复在包含虚拟列的表中计算事件过滤表达式时出现的 Panic 错误 [#12206](https://github.com/pingcap/tiflow/issues/12206) @[lidezhu](https://github.com/lidezhu)
        - 修复在相同 IP 地址上扩缩容 TiKV 节点后，因使用过期的 store ID 导致 resolved ts 延迟持续上升的问题 [#12162](https://github.com/pingcap/tiflow/issues/12162) @[3AceShowHand](https://github.com/3AceShowHand)
        - 修复 dispatcher 配置中列名/索引名大小写敏感匹配的问题 [#12103](https://github.com/pingcap/tiflow/issues/12103) @[wk989898](https://github.com/wk989898)
        - 修复使用 Debezium 协议配置 column-selector 时的 Panic 问题 [#12208](https://github.com/pingcap/tiflow/issues/12208) @[wk989898](https://github.com/wk989898)
        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + TiDB Data Migration (DM)

        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + TiDB Lightning

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + Dumpling

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + TiUP

        - note [#issue](https://github.com/pingcap/tiup/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiup/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

## 错误修复

+ TiDB

    - 修复了 `ALTER RANGE meta SET PLACEMENT POLICY` key 范围错误的问题 [#60888](https://github.com/pingcap/tidb/issues/60888) @[nolouch](https://github.com/nolouch)
    - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - (dup): release-9.0.0.md > 错误修复> TiDB - 修复在添加索引过程中减少 Worker 数量可能导致任务卡住的问题 [#59267](https://github.com/pingcap/tidb/issues/59267) @[D3Hunter](https://github.com/D3Hunter)
    - (dup): release-9.0.0.md > 错误修复> TiDB - 修复 `ADMIN SHOW DDL JOBS` 语句无法正确显示行数的问题 [#59897](https://github.com/pingcap/tidb/issues/59897) @[tangenta](https://github.com/tangenta)
    - (dup): release-9.0.0.md > 错误修复> TiDB - 修复在添加索引过程中动态调整 Worker 数量可能导致的数据竞争问题 [#59016](https://github.com/pingcap/tidb/issues/59016) @[D3Hunter](https://github.com/D3Hunter)
    - (dup): release-7.5.5.md > 错误修复> TiDB - 修复 Grafana 中 **Stats Healthy Distribution** 面板的数据可能错误的问题 [#57176](https://github.com/pingcap/tidb/issues/57176) @[hawkingrei](https://github.com/hawkingrei)
    - (dup): release-9.0.0.md > 错误修复> TiDB - 修复使用 `IMPORT INTO ... FROM SELECT` 导入 TiFlash 时发生错误的问题 [#58443](https://github.com/pingcap/tidb/issues/58443) @[D3Hunter](https://github.com/D3Hunter)
    - (dup): release-9.0.0.md > 错误修复> TiDB - 修复启用 `tidb_enable_dist_task` 导致 TiDB 升级失败的问题 [#54061](https://github.com/pingcap/tidb/issues/54061) @[tangenta](https://github.com/tangenta)
    - (dup): release-7.5.6.md > 错误修复> TiDB - 修复对统计信息的异常处理不当导致后台任务超时的时候，内存内的统计信息被误删除的问题 [#57901](https://github.com/pingcap/tidb/issues/57901) @[hawkingrei](https://github.com/hawkingrei)
    - (dup): release-9.0.0.md > 错误修复> TiDB - 修复在分布式执行框架下执行添加索引操作没有正确更新行数的问题 [#58573](https://github.com/pingcap/tidb/issues/58573) @[D3Hunter](https://github.com/D3Hunter)
    - 修复执行有损 DDL 后，查询 TiFlash 数据不一致的问题 [#61455](https://github.com/pingcap/tidb/issues/61455) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - 修复使用全局排序加索引时，merge sort 阶段监控缺失的问题 [#61025](https://github.com/pingcap/tidb/issues/61025) @[fzzf678](https://github.com/fzzf678)
    - 修复使用 GCS 遇到 EOF 错误没有重试的问题 [#59754](https://github.com/pingcap/tidb/issues/59754) @[D3Hunter](https://github.com/D3Hunter)
    - 修复使用全局排序时遇到不合法的 KV 范围问题 [#59841](https://github.com/pingcap/tidb/issues/59841) @[GMHDBJD](https://github.com/GMHDBJD)
    - 修复`CREATE INDEX IF NOT EXISTS`语句生成空索引名的问题 [#61265](https://github.com/pingcap/tidb/issues/61265) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - 修复禁用 MDL 后，DDL 更新 schema 版本失败后卡住的问题 [#61210](https://github.com/pingcap/tidb/issues/61210) @[wjhuang2016](https://github.com/wjhuang2016)
    - 修复统计信息系统表展示非 public 索引的问题 [#60430](https://github.com/pingcap/tidb/issues/60430) @[tangenta](https://github.com/tangenta)
    - 删除 IndexLookup 算子发生 context cancel 错误时没用的日志信息 [#61072](https://github.com/pingcap/tidb/issues/61072) @[yibin87](https://github.com/yibin87)
    - 修复 HashAgg 算子 memory tracker 内存信息收集错误导致大量 ERROR 日志打印的问题 [#58822](https://github.com/pingcap/tidb/issues/58822) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - 修复 HashAgg 算子 spill 过程中, basePartialResult4GroupConcat 中 buffer 为 nil 导致的 panic [#61749](https://github.com/pingcap/tidb/issues/61749) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - 修复聚合表达式计算过程中编码逻辑返回值问题导致的查询 panic  [#61735](https://github.com/pingcap/tidb/issues/61735) @[YangKeao](https://github.com/YangKeao)
    - 修复 HashJoin 算子因为内存超限导致的 goroutine leak 问题 [#60926](https://github.com/pingcap/tidb/issues/60926) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - 修复 IndexMerge/IndexLookUp 算子下发查询时共享 kv request 导致的 data race [#60175](https://github.com/pingcap/tidb/issues/60175) @[you06](https://github.com/you06)
    - 通过减少 fmt.Sprintf() 调用来优化 IndexScan 的计划构造流程 [#56649](https://github.com/pingcap/tidb/issues/56649) @[crazycs520](https://github.com/crazycs520)
    - 为包含 `_charset(xxx), _charset(xxx2), ...` 的 SQL 生成同样的 digest [#58447](https://github.com/pingcap/tidb/issues/58447) @[xhebox](https://github.com/xhebox)
    - 修复处理非法 UTF8 字符时可能 panic 的问题 [#47521](https://github.com/pingcap/tidb/issues/47521) @[Defined2014](https://github.com/Defined2014)
    - 修复插入夏令营时间戳时，非法时间戳正常插入的问题，使其变为 0000-00-00. [#61334](https://github.com/pingcap/tidb/issues/61334) @[mjonss](https://github.com/mjonss)
    -修复频繁合并 region 导致 TTL 任务无法启动的问题 [#61512](https://github.com/pingcap/tidb/issues/61512) @[YangKeao](https://github.com/YangKeao)
    - 当使用 INSERT IGNORE 插入非法夏令营时间戳，且 sql_mode 为严格模式，自动调整为下一个合法时间戳，并警告 [#61439](https://github.com/pingcap/tidb/issues/61439) @[mjonss](https://github.com/mjonss)
    - 修复 TiDB 在类型未知时，于网络协议中返回长度零的问题 [#60503](https://github.com/pingcap/tidb/issues/60503) @[xhebox](https://github.com/xhebox)
    - 在网络协议中为 blob 类型返回正确的类型，匹配 MySQL [#60195](https://github.com/pingcap/tidb/issues/60195) @[dveeden](https://github.com/dveeden)
    - 修复 `cast` 函数返回的长度与 MySQL 不兼容的问题 [#61350](https://github.com/pingcap/tidb/issues/61350) @[YangKeao](https://github.com/YangKeao)
    - 修复 latin1_bin   与 utf8mb4_bin, utf8_bin 的比较方式不相同的问题 [#60701](https://github.com/pingcap/tidb/issues/60701) @[hawkingrei](https://github.com/hawkingrei)
+ TiKV

    - 修复集群升级导致默认 Region 大小被意外更改的问题 [#18503](https://github.com/tikv/tikv/issues/18503) @[LykxSassinator](https://github.com/LykxSassinator)
    - 修复 TiKV 可能使用客户端无法解码的压缩算法的问题 [#18079](https://github.com/tikv/tikv/issues/18079) @[ekexium](https://github.com/ekexium)
    - 修复关闭 Titan 后，Blob 索引可能导致快照应用失败的问题 [#18434](https://github.com/tikv/tikv/issues/18434) @[v01dstar](https://github.com/v01dstar)
    - 修复 slowlog 中 `StoreMsg` 的误导性日志问题 [#18561](https://github.com/tikv/tikv/issues/18561) @[LykxSassinator](https://github.com/LykxSassinator)
    - 修复高并发场景下 TiKV 过量放行 SST 导入请求的问题 [#18452](https://github.com/tikv/tikv/issues/18452) @[hbisheng](https://github.com/hbisheng)
    - 修复扫描 lock 可能返回导致重复结果导致 tikv panic 问题 [#16818](https://github.com/tikv/tikv/issues/16818) @[cfzjywxk](https://github.com/cfzjywxk)
+ PD

    - 修复了慢节点检测机制中 `recovery-duration` 没有生效的问题 [#9384](https://github.com/tikv/pd/issues/9384) @[rleungx](https://github.com/rleungx)
    - 修复了 evict leader 调度器可能在集群升级后被错误暂停的问题 [#9416](https://github.com/tikv/pd/issues/9416) @[rleungx](https://github.com/rleungx)
    - 修复了 TiDB Dashboard 导致的 goroutine 泄露问题 [#9402](https://github.com/tikv/pd/issues/9402) @[baurine](https://github.com/baurine)

+ TiFlash

    - note [#issue](https://github.com/pingcap/tiflash/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/pingcap/tiflash/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - 修复创建 `((NULL))` 形式的表达式索引会导致 TiFlash panic 的问题 [#9891](https://github.com/pingcap/tiflash/issues/9891) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复 Join 算子中因为 mutex 没有对齐导致 tiflash 在特定系统环境下 crash 的问题 [#10163](https://github.com/pingcap/tiflash/issues/10163) @[windtalker](https://github.com/windtalker)
    - 修复 resource control low token signal 丢失导致查询被限速的问题 [#10137](https://github.com/pingcap/tiflash/issues/10137) @[guo-shaoge](https://github.com/guo-shaoge)
+ Tools

    + Backup & Restore (BR)

        - (dup): release-9.0.0.md > 错误修复> Tools> Backup & Restore (BR) - 修复在断点恢复时额外检查存储节点可用空间的问题 [#54316](https://github.com/pingcap/tidb/issues/54316) @[Leavrth](https://github.com/Leavrth)
        - 修复 PITR 无法恢复大于 3072 字节的索引的问题 [#58430](https://github.com/pingcap/tidb/issues/58430) @[YuJuncen](https://github.com/YuJuncen)
        - 修复在全量备份过程中 RangeTree 结构内存使用效率低下的问题 [#58587](https://github.com/pingcap/tidb/issues/58587) @[3pointer](https://github.com/3pointer)
        - 增加了和 External Storage 交互时对 HTTP/2 GOAWAY 错误的容忍度 [#60143](https://github.com/pingcap/tidb/issues/60143) @[joechenrh](https://github.com/joechenrh)
        - 修复了恢复过程中因为 swtich mode 导致的 “keepalive watchdog timedout” 的问题 [#18541](https://github.com/tikv/tikv/issues/18541) @[Leavrth](https://github.com/Leavrth)
        - 修复了日志备份上传较大数据到 Azure Blob Storage 时会非常缓慢的问题。 [#18410](https://github.com/tikv/tikv/issues/18410) @[YuJuncen](https://github.com/YuJuncen)
        - (dup): release-9.0.0.md > 错误修复> Tools> Backup & Restore (BR) - 修复 PITR 无法恢复大于 3072 字节的索引的问题 [#58430](https://github.com/pingcap/tidb/issues/58430) @[YuJuncen](https://github.com/YuJuncen)
        - (dup): release-9.0.0.md > 错误修复> Tools> Backup & Restore (BR) - 修复在全量备份过程中 RangeTree 结果内存使用效率低下的问题 [#58587](https://github.com/pingcap/tidb/issues/58587) @[3pointer](https://github.com/3pointer)

    + TiCDC

        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + TiDB Data Migration (DM)

        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + TiDB Lightning

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - 修复 lightning 向 TiKV 发起的 RPC 请求超时后返回 context deadline 的问题 [#61326](https://github.com/pingcap/tidb/issues/61326) @[OliverS929](https://github.com/OliverS929)

    + Dumpling

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + TiUP

        - note [#issue](https://github.com/pingcap/tiup/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiup/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
