---
title: TiDB 7.5.7 Release Notes
summary: 了解 TiDB 7.5.7 版本的兼容性变更、改进提升，以及错误修复。
---

# TiDB 7.5.7 Release Notes

发版日期：2025 年 x 月 x 日

TiDB 版本：7.5.7

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v7.5/quick-start-with-tidb) | [生产部署](https://docs.pingcap.com/zh/tidb/v7.5/production-deployment-using-tiup) | [下载离线包](https://cn.pingcap.com/product-community/?version=v7.5.7#version-list)

## 兼容性变更

- note [#issue](https://github.com/pingcap/${repo-name}/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

## 改进提升

+ TiDB

    - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - (dup): release-8.5.3.md > 改进提升> TiDB - 新增导入期间分裂 region 和 ingest 数据的流控接口 [#61553](https://github.com/pingcap/tidb/issues/61553) @[tangenta](https://github.com/tangenta)
    - (dup): release-8.2.0.md > 改进提升> TiDB - 优化对大数据量的表进行简单查询时获取数据分布信息的性能 [#53850](https://github.com/pingcap/tidb/issues/53850) @[you06](https://github.com/you06)
    - (dup): release-8.5.3.md > 改进提升> TiDB - 新增加索引的导入速度监控 [#60925](https://github.com/pingcap/tidb/issues/60925) @[CbcWestwolf](https://github.com/CbcWestwolf)

+ TiKV

    - note [#issue](https://github.com/tikv/tikv/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/tikv/tikv/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - (dup): release-8.5.3.md > 改进提升> TiKV - 优化 raftstore 中 `CompactedEvent` 的处理逻辑，将其移至 `split-check` worker 执行 [#18532](https://github.com/tikv/tikv/issues/18532) @[LykxSassinator](https://github.com/LykxSassinator)
    - (dup): release-8.1.0.md > 改进提升> TiKV - 增加每个线程内存使用量的监控指标 [#15927](https://github.com/tikv/tikv/issues/15927) @[Connor1996](https://github.com/Connor1996)
    - (dup): release-8.5.3.md > 改进提升> TiKV - 移除 “sst ingest is too slow” 的日志，避免引发性能抖动 [#18549](https://github.com/tikv/tikv/issues/18549) @[LykxSassinator](https://github.com/LykxSassinator)
    - (dup): release-7.1.6.md > 改进提升> TiKV - 优化 TiKV 重启时由于需要等待应用之前的日志而造成访问延时抖动的情况，提升了 TiKV 的稳定性 [#15874](https://github.com/tikv/tikv/issues/15874) @[LykxSassinator](https://github.com/LykxSassinator)
    - (dup): release-8.5.3.md > 改进提升> TiKV - (dup): release-9.0.0.md > 改进提升> TiKV - 优化残留数据清理机制，减少对请求延迟的影响 [#18107](https://github.com/tikv/tikv/issues/18107) @[LykxSassinator](https://github.com/LykxSassinator)
    - (dup): release-8.5.3.md > 改进提升> TiKV - 修复 TiKV 正常退出时未能中止正在进行的手动 Compaction 任务的问题 [#18396](https://github.com/tikv/tikv/issues/18396) @[LykxSassinator](https://github.com/LykxSassinator)
    - (dup): release-8.5.3.md > 改进提升> TiKV - 优化 Raft-Engine 中 `fetch_entries_to` 的性能，减少竞争，提升混合负载下的执行性能 [#18605](https://github.com/tikv/tikv/issues/18605) @[LykxSassinator](https://github.com/LykxSassinator)
    - (dup): release-8.4.0.md > 改进提升> TiKV - 支持在线更改写入流量控制 (flow-control) 的相关配置 [#17395](https://github.com/tikv/tikv/issues/17395) @[glorv](https://github.com/glorv)
    - (dup): release-8.5.3.md > 改进提升> TiKV - 支持在不阻塞前台写入的情况下导入 SST 文件，降低延迟影响 [#18081](https://github.com/tikv/tikv/issues/18081) @[hhwyt](https://github.com/hhwyt)
    - (dup): release-8.5.3.md > 改进提升> TiKV - 优化 TiDB 执行 `ADD INDEX` 操作期间的尾延迟 [#18081](https://github.com/tikv/tikv/issues/18081) @[overvenus](https://github.com/overvenus)
    - (dup): release-8.5.3.md > 改进提升> TiKV - 改进分盘部署场景下 kvdb 磁盘 I/O 抖动的检测机制 [#18463](https://github.com/tikv/tikv/issues/18463) @[LykxSassinator](https://github.com/LykxSassinator)
    - (dup): release-6.5.9.md > 改进提升> TiKV - 增加 peer 和 store 消息的 slow log [#16600](https://github.com/tikv/tikv/issues/16600) @[Connor1996](https://github.com/Connor1996)

+ PD

    - note [#issue](https://github.com/tikv/pd/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/tikv/pd/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - (dup): release-8.5.3.md > 改进提升> PD - 优化了 balance region 调度器的算分公式 [#9145](https://github.com/tikv/pd/issues/9145) @[bufferflies](https://github.com/bufferflies)
    - (dup): release-8.5.3.md > 改进提升> PD - 增加了 GO Runtime 相关监控 [#8931](https://github.com/tikv/pd/issues/8931) @[bufferflies](https://github.com/bufferflies)

+ TiFlash

    - note [#issue](https://github.com/pingcap/tiflash/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/pingcap/tiflash/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - (dup): release-8.5.3.md > 改进提升> TiFlash - 增强 TiFlash 在宽表场景下 OOM 风险相关的监测指标 [#10272](https://github.com/pingcap/tiflash/issues/10272) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - (dup): release-8.5.3.md > 改进提升> TiFlash - 增加 TiFlash 获取存储层快照重试次数来增强大表上查询的稳定性 [#10300](https://github.com/pingcap/tiflash/issues/10300) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - (dup): release-8.1.0.md > 改进提升> TiFlash - 降低 TiFlash 在开启 TLS 后因更新证书而导致 panic 的概率 [#8535](https://github.com/pingcap/tiflash/issues/8535) @[windtalker](https://github.com/windtalker)

+ Tools

    + Backup & Restore (BR)

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - (dup): release-8.5.3.md > 改进提升> Tools> Backup & Restore (BR) - 如今即便指定了 `-f` 来过滤表，BR 也会对集群内是否存在表进行检查 [#61592](https://github.com/pingcap/tidb/issues/61592) @[RidRisR](https://github.com/RidRisR)
        - (dup): release-8.5.3.md > 改进提升> Tools> Backup & Restore (BR) - 如今，TiKV 的 Download API 支持裁切掉 SST 中某段时间的数据 [#18399](https://github.com/tikv/tikv/issues/18399) @[3pointer](https://github.com/3pointer)

    + TiCDC

        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - (dup): release-8.5.3.md > 改进提升> Tools> TiCDC - 修复在包含虚拟列的表中计算事件过滤表达式时出现的 Panic 错误 [#12206](https://github.com/pingcap/tiflow/issues/12206) @[lidezhu](https://github.com/lidezhu)
        - (dup): release-8.5.3.md > 改进提升> Tools> TiCDC - 修复 dispatcher 配置中列名/索引名大小写敏感匹配的问题 [#12103](https://github.com/pingcap/tiflow/issues/12103) @[wk989898](https://github.com/wk989898)
        - (dup): release-8.5.3.md > 改进提升> Tools> TiCDC - 修复在相同 IP 地址上扩缩容 TiKV 节点后，因使用过期的 store ID 导致 resolved ts 延迟持续上升的问题 [#12162](https://github.com/pingcap/tiflow/issues/12162) @[3AceShowHand](https://github.com/3AceShowHand)

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

    - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - (dup): release-8.5.3.md > 错误修复> TiDB - 修复 IndexMerge/IndexLookUp 算子下发查询时共享 kv request 导致的 data race [#60175](https://github.com/pingcap/tidb/issues/60175) @[you06](https://github.com/you06)
    - (dup): release-9.0.0.md > 错误修复> TiDB - 修复 Hash Aggregation 算子可能存在 goroutine 泄漏的问题 [#58004](https://github.com/pingcap/tidb/issues/58004) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - (dup): release-7.6.0.md > 错误修复> TiDB - 修复当生成列上的索引设置为可见时，可能无法选中 MPP 计划的问题 [#47766](https://github.com/pingcap/tidb/issues/47766) @[AilinKid](https://github.com/AilinKid)
    - (dup): release-8.5.3.md > 错误修复> TiDB - 为包含 `_charset(xxx), _charset(xxx2), ...` 的 SQL 生成同样的 digest [#58447](https://github.com/pingcap/tidb/issues/58447) @[xhebox](https://github.com/xhebox)
    - (dup): release-8.5.3.md > 错误修复> TiDB - 修复频繁合并 region 导致 TTL 任务无法启动的问题 [#61512](https://github.com/pingcap/tidb/issues/61512) @[YangKeao](https://github.com/YangKeao)
    - (dup): release-8.5.3.md > 错误修复> TiDB - 修复执行有损 DDL 后，查询 TiFlash 数据不一致的问题 [#61455](https://github.com/pingcap/tidb/issues/61455) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - (dup): release-8.5.3.md > 错误修复> TiDB - 修复了 `ALTER RANGE meta SET PLACEMENT POLICY` key 范围错误的问题 [#60888](https://github.com/pingcap/tidb/issues/60888) @[nolouch](https://github.com/nolouch)
    - (dup): release-8.5.2.md > 错误修复> TiDB - 修复 Grafana 中 **Stats Healthy Distribution** 面板的数据可能错误的问题 [#57176](https://github.com/pingcap/tidb/issues/57176) @[hawkingrei](https://github.com/hawkingrei)
    - (dup): release-8.5.3.md > 错误修复> TiDB - 修复 latin1_bin   与 utf8mb4_bin, utf8_bin 的比较方式不相同的问题 [#60701](https://github.com/pingcap/tidb/issues/60701) @[hawkingrei](https://github.com/hawkingrei)
    - (dup): release-8.5.3.md > 错误修复> TiDB - 修复禁用 MDL 后，DDL 更新 schema 版本失败后卡住的问题 [#61210](https://github.com/pingcap/tidb/issues/61210) @[wjhuang2016](https://github.com/wjhuang2016)
    - (dup): release-8.5.2.md > 错误修复> TiDB - 修复 Redact 日志开启后在部分场景不生效的问题 [#59279](https://github.com/pingcap/tidb/issues/59279) @[tangenta](https://github.com/tangenta)
    - (dup): release-9.0.0.md > 错误修复> TiDB - 修复当 Fix Control #44855 开启时，TiDB 的会话可能崩溃的问题 [#59762](https://github.com/pingcap/tidb/issues/59762) @[winoros](https://github.com/winoros)
    - (dup): release-8.5.3.md > 错误修复> TiDB - 删除 IndexLookup 算子发生 context cancel 错误时没用的日志信息 [#61072](https://github.com/pingcap/tidb/issues/61072) @[yibin87](https://github.com/yibin87)
    - (dup): release-8.5.2.md > 错误修复> TiDB - 修复对统计信息的异常处理不当导致后台任务超时的时候，内存内的统计信息被误删除的问题 [#57901](https://github.com/pingcap/tidb/issues/57901) @[hawkingrei](https://github.com/hawkingrei)
    - (dup): release-8.5.2.md > 错误修复> TiDB - 修复执行 `ADD UNIQUE INDEX` 可能导致数据不一致的问题  [#60339](https://github.com/pingcap/tidb/issues/60339) @[tangenta](https://github.com/tangenta)
    - (dup): release-8.5.3.md > 错误修复> TiDB - 修复统计信息系统表展示非 public 索引的问题 [#60430](https://github.com/pingcap/tidb/issues/60430) @[tangenta](https://github.com/tangenta)
    - (dup): release-8.5.3.md > 错误修复> TiDB - 修复 HashJoin 算子因为内存超限导致的 goroutine leak 问题 [#60926](https://github.com/pingcap/tidb/issues/60926) @[xzhangxian1008](https://github.com/xzhangxian1008)

+ TiKV

    - note [#issue](https://github.com/tikv/tikv/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/tikv/tikv/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - (dup): release-8.5.3.md > 错误修复> TiKV - 修复 TiKV 可能使用客户端无法解码的压缩算法的问题 [#18079](https://github.com/tikv/tikv/issues/18079) @[ekexium](https://github.com/ekexium)
    - (dup): release-8.5.3.md > 错误修复> TiKV - 修复高并发场景下 TiKV 过量放行 SST 导入请求的问题 [#18452](https://github.com/tikv/tikv/issues/18452) @[hbisheng](https://github.com/hbisheng)
    - (dup): release-8.3.0.md > 错误修复> TiKV - 修复 Grafana TiKV 组件中的 `Ingestion picked level` 和 `Compaction Job Size(files)` 显示不正确的问题 [#15990](https://github.com/tikv/tikv/issues/15990) @[Connor1996](https://github.com/Connor1996)
    - (dup): release-9.0.0.md > 错误修复> TiKV - 修复 TiKV 重启后出现非预期的 `Server is busy` 报错 [#18233](https://github.com/tikv/tikv/issues/18233) @[LykxSassinator](https://github.com/LykxSassinator)
    - (dup): release-6.5.9.md > 错误修复> TiKV - 修复巴西和埃及时区转换错误的问题 [#16220](https://github.com/tikv/tikv/issues/16220) @[overvenus](https://github.com/overvenus)
    - (dup): release-8.5.3.md > 错误修复> TiKV - 修复 slowlog 中 `StoreMsg` 的误导性日志问题 [#18561](https://github.com/tikv/tikv/issues/18561) @[LykxSassinator](https://github.com/LykxSassinator)
    - (dup): release-9.0.0.md > 错误修复> TiKV - 修复错误的线程内存监控指标 [#18125](https://github.com/tikv/tikv/issues/18125) @[Connor1996](https://github.com/Connor1996)

+ PD

    - note [#issue](https://github.com/tikv/pd/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/tikv/pd/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - (dup): release-8.5.2.md > 错误修复> PD - 修复 `lease` 默认值未被正确设置的问题 [#9156](https://github.com/tikv/pd/issues/9156) @[rleungx](https://github.com/rleungx)
    - (dup): release-8.3.0.md > 错误修复> PD - 修复反复修改 `split-merge-interval` 的值（例如从 `1s` 改为 `1h`，再改回 `1s`）可能导致该配置不生效的问题 [#8404](https://github.com/tikv/pd/issues/8404) @[lhy1024](https://github.com/lhy1024)
    - (dup): release-8.5.3.md > 错误修复> PD - 修复了 TiDB Dashboard 导致的 goroutine 泄露问题 [#9402](https://github.com/tikv/pd/issues/9402) @[baurine](https://github.com/baurine)

+ TiFlash

    - note [#issue](https://github.com/pingcap/tiflash/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - 修复在运行 `IMPORT INTO` 或 `BR restore` 的时候，部分 SST 文件可能被意外删除导致 TiFlash panic 的问题 [#10141](https://github.com/pingcap/tiflash/issues/10141) @[CalvinNeo](https://github.com/CalvinNeo)
    - (dup): release-8.5.3.md > 错误修复> TiFlash - 修复创建 `((NULL))` 形式的表达式索引会导致 TiFlash panic 的问题 [#9891](https://github.com/pingcap/tiflash/issues/9891) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - (dup): release-8.5.2.md > 错误修复> TiFlash - 修复 TiFlash 处理带有不规则 key-range 的 Region snapshot 时可能 panic 的问题 [#10147](https://github.com/pingcap/tiflash/issues/10147) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - (dup): release-8.5.2.md > 错误修复> TiFlash - 修复当集群的表中存在大量 `ENUM` 类型列时，TiFlash 的内存可能会大量消耗问题 [#9947](https://github.com/pingcap/tiflash/issues/9947) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - (dup): release-8.5.2.md > 错误修复> TiFlash - 修复插入单行超过 16 MiB 的数据后，TiFlash 可能无法正常重启的问题 [#10052](https://github.com/pingcap/tiflash/issues/10052) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - (dup): release-8.5.3.md > 错误修复> TiFlash - 修复 resource control low token signal 丢失导致查询被限速的问题 [#10137](https://github.com/pingcap/tiflash/issues/10137) @[guo-shaoge](https://github.com/guo-shaoge)
    - (dup): release-8.5.2.md > 错误修复> TiFlash - 修复执行包含 `GROUP BY ... WITH ROLLUP` 的 SQL 语句时，可能会出现 `Exception: Block schema mismatch` 报错的问题 [#10110](https://github.com/pingcap/tiflash/issues/10110) @[gengliqi](https://github.com/gengliqi)

+ Tools

    + Backup & Restore (BR)

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - (dup): release-8.5.2.md > 错误修复> Tools> Backup & Restore (BR) - 修复 PITR 无法恢复大于 3072 字节的索引的问题 [#58430](https://github.com/pingcap/tidb/issues/58430) @[YuJuncen](https://github.com/YuJuncen)
        - (dup): release-8.5.3.md > 错误修复> Tools> Backup & Restore (BR) - 修复了日志备份上传较大数据到 Azure Blob Storage 时会非常缓慢的问题。 [#18410](https://github.com/tikv/tikv/issues/18410) @[YuJuncen](https://github.com/YuJuncen)

    + TiCDC

        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - (dup): release-8.5.2.md > 错误修复> Tools> TiCDC - 修复同步流量超过了下游 Kafka 的流量阀值后，Changefeed 可能会卡住的问题 [#12110](https://github.com/pingcap/tiflow/issues/12110) @[3AceShowHand](https://github.com/3AceShowHand)
        - (dup): release-6.5.12.md > 错误修复> Tools> TiCDC - 修复使用 `--overwrite-checkpoint-ts` 参数执行 `changefeed pause` 命令可能导致 Changefeed 卡住的问题 [#12055](https://github.com/pingcap/tiflow/issues/12055) @[hongyunyan](https://github.com/hongyunyan)

    + TiDB Data Migration (DM)

        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + TiDB Lightning

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - (dup): release-8.5.2.md > 错误修复> Tools> TiDB Lightning - 修复将 Parquet 文件从云存储导入到 TiDB 时，TiDB Lightning 可能会卡住达数小时的问题 [#60224](https://github.com/pingcap/tidb/issues/60224) @[joechenrh](https://github.com/joechenrh)
        - (dup): release-8.5.3.md > 错误修复> Tools> TiDB Lightning - 修复 lightning 向 TiKV 发起的 RPC 请求超时后返回 context deadline 的问题 [#61326](https://github.com/pingcap/tidb/issues/61326) @[OliverS929](https://github.com/OliverS929)

    + Dumpling

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + TiUP

        - note [#issue](https://github.com/pingcap/tiup/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiup/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + NG Monitoring

        - (dup): release-8.5.2.md > 错误修复> Tools> NG Monitoring - 修复 TSDB 在高时序基数下内存占用高的问题，提供 TSDB 内存配置项 [#295](https://github.com/pingcap/ng-monitoring/issues/295) @[mornyx](https://github.com/mornyx)
