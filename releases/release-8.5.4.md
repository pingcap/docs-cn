---
title: TiDB 8.5.4 Release Notes
summary: 了解 TiDB 8.5.4 版本的兼容性变更、改进提升，以及错误修复。
---

# TiDB 8.5.4 Release Notes

发版日期：2025 年 x 月 x 日

TiDB 版本：8.5.4

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v8.5/quick-start-with-tidb) | [生产部署](https://docs.pingcap.com/zh/tidb/v8.5/production-deployment-using-tiup) | [下载离线包](https://cn.pingcap.com/product-community/?version=v8.5.4#version-list)

## 兼容性变更

### 系统变量

- 系统变量 [`tidb_mpp_store_fail_ttl`](/system-variables.md#tidb_mpp_store_fail_ttl) 默认值从 `60s` 修改为 `0s`，意味着 TiDB 不再需要额外等待即可向新启动的 TiFlash 节点发送查询请求，无需再通过延迟来避免查询失败 [#61826](https://github.com/pingcap/tidb/issues/61826) @[gengliqi](https://github.com/gengliqi) <!--tw@qiancai -->

- 系统变量 [`tidb_replica_read`](/system-variables.md#tidb_replica_read-从-v40-版本开始引入) 从 v8.5.4 开始仅对只读 SQL 语句生效，以提高数据读取的安全性并减少与其他功能的重叠 [#62856](https://github.com/pingcap/tidb/issues/62856) @[you06](https://github.com/you06) <!--tw@qiancai -->

- 新增以下系统变量：

    - [`tidb_enable_binding_usage`](https://docs.pingcap.com/zh/tidb/v8.5/system-variables.md#tidb_enable_binding_usage-从-v854-版本开始引入)：控制是否收集 SQL 执行计划绑定的使用统计信息，默认值为 `OFF` [#63407](https://github.com/pingcap/tidb/issues/63407) @[hawkingrei](https://github.com/hawkingrei) <!--tw@qiancai -->
    - [`tidb_opt_enable_no_decorrelate_in_select`](https://docs.pingcap.com/zh/tidb/v8.5/system-variables.md#tidb_opt_enable_no_decorrelate_in_select-从-v854-版本开始引入)：控制是否对 `SELECT` 列表中的子查询进行解关联操作，默认值为 `OFF` [#51116](https://github.com/pingcap/tidb/issues/51116) @[terry1purcell](https://github.com/terry1purcell) <!--tw@Oreoxmt -->
    - [`tidb_opt_enable_semi_join_rewrite`](https://docs.pingcap.com/zh/tidb/v8.5/system-variables.md#tidb_opt_enable_semi_join_rewrite-从-v854-版本开始引入)：控制是否改写 `EXISTS` 子查询，默认值为 `OFF` [#44850](https://github.com/pingcap/tidb/issues/44850) @[terry1purcell](https://github.com/terry1purcell) <!--tw@Oreoxmt -->
    - [`tidb_stats_update_during_ddl`](https://docs.pingcap.com/zh/tidb/v8.5/system-variables.md#tidb_stats_update_during_ddl-从-v854-版本开始引入)：控制是否开启 DDL 的内嵌 Analyze 的行为，默认值为 `OFF` [#57948](https://github.com/pingcap/tidb/issues/57948) @[terry1purcell](https://github.com/terry1purcell) @[AilinKid](https://github.com/AilinKid) <!--tw@hfxsd -->

### 配置参数

- (dup): release-7.5.7.md > 兼容性变更 - 废弃以下 TiKV 配置项，并由新的 [`gc.auto-compaction`](https://docs.pingcap.com/zh/tidb/v8.5/tikv-configuration-file/#gcauto-compaction) 配置项替代，用于控制自动 compaction 行为 [#18727](https://github.com/tikv/tikv/issues/18727) @[v01dstar](https://github.com/v01dstar)

    - 废弃配置项：[`region-compact-check-interval`](https://docs.pingcap.com/zh/tidb/v8.5/tikv-configuration-file#region-compact-check-interval)、[`region-compact-check-step`](https://docs.pingcap.com/zh/tidb/v8.5/tikv-configuration-file#region-compact-check-step)、[`region-compact-min-tombstones`](https://docs.pingcap.com/zh/tidb/v8.5/tikv-configuration-file#region-compact-min-tombstones)、[`region-compact-tombstones-percent`](https://docs.pingcap.com/zh/tidb/v8.5/tikv-configuration-file#region-compact-tombstones-percent)、[`region-compact-min-redundant-rows`](https://docs.pingcap.com/zh/tidb/v8.5/tikv-configuration-file#region-compact-min-redundant-rows-从-v710-版本开始引入) 和 [`region-compact-redundant-rows-percent`](https://docs.pingcap.com/zh/tidb/v8.5/tikv-configuration-file#region-compact-redundant-rows-percent-从-v710-版本开始引入)。
    - 新增配置项：[`gc.auto-compaction.check-interval`](https://docs.pingcap.com/zh/tidb/v8.5/tikv-configuration-file#check-interval-从-v757-和-v854-版本开始引入)、[`gc.auto-compaction.tombstone-num-threshold`](https://docs.pingcap.com/zh/tidb/v8.5/tikv-configuration-file#tombstone-num-threshold-从-v757-和-v854-版本开始引入)、[`gc.auto-compaction.tombstone-percent-threshold`](https://docs.pingcap.com/zh/tidb/v8.5/tikv-configuration-file#tombstone-percent-threshold-从-v757-和-v854-版本开始引入)、[`gc.auto-compaction.redundant-rows-threshold`](https://docs.pingcap.com/zh/tidb/v8.5/tikv-configuration-file#redundant-rows-threshold-从-v757-和-v854-版本开始引入)、[`gc.auto-compaction.redundant-rows-percent-threshold`](https://docs.pingcap.com/zh/tidb/v8.5/tikv-configuration-file#redundant-rows-percent-threshold-从-v757-和-v854-版本开始引入) 和 [`gc.auto-compaction.bottommost-level-force`](https://docs.pingcap.com/zh/tidb/v8.5/tikv-configuration-file#bottommost-level-force-从-v757-和-v854-版本开始引入)。

- 新增 TiFlash 配置项 [`graceful_wait_shutdown_timeout`](https://docs.pingcap.com/zh/tidb/v8.5/tiflash-configuration#graceful_wait_shutdown_timeout-从-v854-版本开始引入)，用于控制在关闭 TiFlash 服务器时的最长等待时间，默认值为 `600` 秒。在此期间，TiFlash 允许尚未完成的 MPP 任务继续执行，但不再接收新的 MPP 任务。如果所有正在运行的 MPP 任务都在此超时时间之前完成，TiFlash 将立即关闭；否则将在等待时间结束后强制关闭。 [#10266](https://github.com/pingcap/tiflash/issues/10266) @[gengliqi](https://github.com/gengliqi) <!--tw@qiancai -->

## 改进提升

+ TiDB <!--tw@Oreoxmt: 11 notes-->

    - 支持表级别数据打散（实验特性）：你可以通过 [`SHOW TABLE DISTRIBUTION`](/sql-statements/sql-statement-show-distribution-jobs.md) 语句查看某张表在集群中所有 TiKV 节点上的数据分布情况。如果存在数据分布不均衡，可以通过 [`DISTRIBUTE TABLE`](/sql-statements/sql-statement-distribute-table.md) 语句对该表进行数据打散，以提升负载均衡性 [#63260](https://github.com/pingcap/tidb/issues/63260) @[bufferflies](https://github.com/bufferflies) <!--tw@qiancai-->

    - (dup): release-9.0.0.md(beta.1) > # SQL 功能 - 支持对分区表的非唯一列创建[全局索引](/partitioned-table.md#全局索引)，以提升全局索引的易用性 [#58650](https://github.com/pingcap/tidb/issues/58650) @[Defined2014](https://github.com/Defined2014) @[mjonss](https://github.com/mjonss)
    - (dup): release-9.0.0.md(beta.1) > 改进提升> TiDB - 支持由 `IN` 子查询而来的 Semi Join 使用 `semi_join_rewrite` 的 Hint [#58829](https://github.com/pingcap/tidb/issues/58829) @[qw4990](https://github.com/qw4990)
    - 优化系统变量 `tidb_opt_ordering_index_selectivity_ratio` 生效时的估算策略 [#62817](https://github.com/pingcap/tidb/issues/62817) @[terry1purcell](https://github.com/terry1purcell)
    - 调整优化器的选择逻辑，使新创建的索引在某些情况下更容易被选中 [#57948](https://github.com/pingcap/tidb/issues/57948) @[terry1purcell](https://github.com/terry1purcell)
    - 优化 NDV (number of distinct values) 较小的列的查询估算逻辑 [#61792](https://github.com/pingcap/tidb/issues/61792) @[terry1purcell](https://github.com/terry1purcell)
    - 优化 Index Join 查询中包含 `LIMIT OFFSET` 时的估算策略 [#45077](https://github.com/pingcap/tidb/issues/45077) @[qw4990](https://github.com/qw4990)
    - 优化统计信息未及时收集时的越界估算策略 [#58068](https://github.com/pingcap/tidb/issues/58068) @[terry1purcell](https://github.com/terry1purcell)
    - 在 Grafana 上的 **Performance Overview** > **SQL Execute Time Overview** 面板中新增 `backoff` 时间指标，便于调试 [#61441](https://github.com/pingcap/tidb/issues/61441) @[dbsid](https://github.com/dbsid)
    - 在审计日志插件中新增语句 ID 信息 [#63525](https://github.com/pingcap/tidb/issues/63525) @[YangKeao](https://github.com/YangKeao)

+ TiKV <!--tw@lilin90: 6 notes-->

    - 将 BR 模块中部分可自动恢复的错误日志级别从 `ERROR` 调整为 `WARN`，减少不必要的告警 [#18493](https://github.com/tikv/tikv/issues/18493) @[YuJuncen](https://github.com/YuJuncen)
    - 将 TiKV 的部分错误日志级别从 `ERROR` 调整为 `WARN`，减少不必要的告警 [#18745](https://github.com/tikv/tikv/issues/18745) @[exit-code-1](https://github.com/exit-code-1)
    - 将 Raft 模块检查 GC 的流程拆分为两个阶段，以提升 Region 中冗余的 MVCC 版本 GC 的效率 [#18695](https://github.com/tikv/tikv/issues/18695) @[v01dstar](https://github.com/v01dstar)
    - 基于 GC safe point 和 RocksDB 的统计信息计算 MVCC 的冗余度，提升 Compaction 的效率和准确性 [#18697](https://github.com/tikv/tikv/issues/18697) @[v01dstar](https://github.com/v01dstar)
    - 将 Region MVCC 的 GC 处理逻辑更改为由 GC Worker 线程执行，从而统一 GC 的处理逻辑 [#18727](https://github.com/tikv/tikv/issues/18727) @[v01dstar](https://github.com/v01dstar)
    - 优化 gRPC 线程池线程数量默认值的计算方式，将原固定值调整为根据总的 CPU 配置动态计算，避免因 gRPC 线程数量过小导致的性能瓶颈 [#18613](https://github.com/tikv/tikv/issues/18613) @[LykxSassinator](https://github.com/LykxSassinator)
    - (dup): release-7.5.7.md > 改进提升> TiKV - 优化在存在大量 SST 文件的环境中 async snapshot 和 write 的尾延迟 [#18743](https://github.com/tikv/tikv/issues/18743) @[Connor1996](https://github.com/Connor1996)

+ PD <!--tw@Oreoxmt: 3 notes-->

    - 减少非必要的错误日志 [#9370](https://github.com/tikv/pd/issues/9370) @[bufferflies](https://github.com/bufferflies)
    - 将 Golang 版本从 1.23.0 升级至 1.23.12，并更新相关依赖项 [#9788](https://github.com/tikv/pd/issues/9788) @[JmPotato](https://github.com/JmPotato)
    - 支持按表级别维度打散 Region 数量，以在 `scatter-role` 和 `engine` 维度实现均衡分布 [#8986](https://github.com/tikv/pd/issues/8986) @[bufferflies](https://github.com/bufferflies)

+ TiFlash <!--tw@qiancai: 5 notes-->

    - 跳过不必要数据读取，提升 `TableScan` 读取性能 [#9875](https://github.com/pingcap/tiflash/issues/9875) @[gengliqi](https://github.com/gengliqi)
    - 优化 TiFlash 在列多且稀疏（大量 `NULL` 或空值）的宽表上执行 `TableScan` 的性能 [#10361](https://github.com/pingcap/tiflash/issues/10361) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 在集群存在大量表的场景中，降低添加向量索引时 TiFlash 的 CPU 开销 [#10357](https://github.com/pingcap/tiflash/issues/10357) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - 减少处理无用 Raft 命令时产生的不必要日志输出，降低日志量 [#10467](https://github.com/pingcap/tiflash/issues/10467) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 优化 TiFlash 在小数据量分区表上执行 `TableScan` 的性能 [#10487](https://github.com/pingcap/tiflash/issues/10487) @[JaySon-Huang](https://github.com/JaySon-Huang)

+ Tools

    + TiDB Data Migration (DM) <!--tw@hfxsd: 1 note-->

        - 获取上游 `GTID_MODE` 时，支持兼容大小写 [#12167](https://github.com/pingcap/tiflow/issues/12167) @[OliverS929](https://github.com/OliverS929)

## 错误修复

+ TiDB <!--tw@lilin90: the following 14 notes-->

    - 修复当 `tidb_isolation_read_engines` 设置为 `tiflash` 时，`use index` Hint 无法生效的问题 [#60869](https://github.com/pingcap/tidb/issues/60869) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - 修复 `max_execution_time` 对 `SELECT FOR UPDATE` 语句不生效的问题 [#62960](https://github.com/pingcap/tidb/issues/62960) @[ekexium](https://github.com/ekexium)
    - (dup): release-7.5.7.md > 错误修复> TiDB - 修复估算跨月或跨年的行数时，结果可能过分偏大的问题 [#50080](https://github.com/pingcap/tidb/issues/50080) @[terry1purcell](https://github.com/terry1purcell)
    - 修复预处理语句中处理 `Decimal` 的方式与 MySQL 不一致的问题 [#62602](https://github.com/pingcap/tidb/issues/62602) @[ChangRui-Ryan](https://github.com/ChangRui-Ryan)
    - 修复 `TRUNCATE()` 函数中短路径处理错误的问题 [#57608](https://github.com/pingcap/tidb/issues/57608) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - 修复当触发 `Out Of Quota For Local Temporary Space` 错误时，落盘文件可能未被全部删除的问题 [#63216](https://github.com/pingcap/tidb/issues/63216) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - 修复使用正则表达式查询 `INFORMATION_SCHEMA` 表时，结果不正确的问题 [#62347](https://github.com/pingcap/tidb/issues/62347) @[River2000i](https://github.com/River2000i)
    - 修复从 PD 获取时间戳异常时，没有返回错误的问题 [#58871](https://github.com/pingcap/tidb/issues/58871) @[joechenrh](https://github.com/joechenrh)
    - 修复在执行 `MODIFY COLUMN` 操作时，owner TiDB 与非 owner TiDB 查询结果不一致的问题 [#60264](https://github.com/pingcap/tidb/issues/60264) @[tangenta](https://github.com/tangenta)
    - 修复动态调参后，`ADMIN ALTER DDL JOBS` 显示参数不正确的问题 [#63201](https://github.com/pingcap/tidb/issues/63201) @[fzzf678](https://github.com/fzzf678)
    - 修复通过事务加索引时，GC savepoint 不推进的问题 [#62424](https://github.com/pingcap/tidb/issues/62424) @[wjhuang2016](https://github.com/wjhuang2016)
    - 修复过大的 SST 文件 Ingest 到 L0 中导致流控的问题 [#63466](https://github.com/pingcap/tidb/issues/63466) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - 修复当 CPU 和内存比例为 1:2 时，阻塞全局排序的问题 [#60951](https://github.com/pingcap/tidb/issues/60951) @[wjhuang2016](https://github.com/wjhuang2016)
    - 修复超过 16 个分布式执行框架 (Distributed eXecution Framework, DXF) 任务上限时，无法取消 Pending 任务的问题 [#63896](https://github.com/pingcap/tidb/issues/63896) @[D3Hunter](https://github.com/D3Hunter)
    - 修复取消 DXF 任务后，其他任务无法退出的问题 [#63927](https://github.com/pingcap/tidb/issues/63927) @[D3Hunter](https://github.com/D3Hunter) <!--tw@hfxsd: the following 14 notes-->
    - 修复开启 `Apply` 算子并发后 (`tidb_enable_parallel_apply = on`)，由于缺少实现 Clone 导致计划生成失败的问题 [#59863](https://github.com/pingcap/tidb/issues/59863) @[hawkingrei](https://github.com/hawkingrei)
    - 修复查询使用 `ATAN2` 函数可能导致结果错误的问题 [#60093](https://github.com/pingcap/tidb/issues/60093) @[guo-shaoge](https://github.com/guo-shaoge)
    - 修复 `select 1 from duml` 无法使用实例级别的计划缓存的问题 [#63075](https://github.com/pingcap/tidb/issues/63075) @[time-and-fate](https://github.com/time-and-fate)
    - 修复 Join Order 变更顺序后可能导致无法规划的问题 [#61715](https://github.com/pingcap/tidb/issues/61715) @[hawkingrei](https://github.com/hawkingrei)
    - 修复 `set_var` Hint 使用 Binding 导致无法恢复为原始变量设置的问题 [#59822](https://github.com/pingcap/tidb/issues/59822) @[wddevries](https://github.com/wddevries)
    - 修复 `ONLY_FULL_GROUP_BY` 取值为负数时导致检查失败的问题 [#62617](https://github.com/pingcap/tidb/issues/62617) @[AilinKid](https://github.com/AilinKid)
    - 修复 `ONLY_FULL_GROUP_BY` 检查大小写不敏感的问题 [#62672](https://github.com/pingcap/tidb/issues/62672) @[AilinKid](https://github.com/AilinKid)
    - 修复 DP Join Order 算法可能产生错误 Plan 的问题 [#63353](https://github.com/pingcap/tidb/issues/63353) @[winoros](https://github.com/winoros)
    - 修复 Outer Join 改写为 Inner Join 可能出错的问题 [#61327](https://github.com/pingcap/tidb/issues/61327) @[hawkingrei](https://github.com/hawkingrei)
    - 修复执行查询可能导致内部 panic 的问题 [#58600](https://github.com/pingcap/tidb/issues/58600) @[Defined2014](https://github.com/Defined2014)
    - 修复全局索引在某些 `ALTER PARTITION` 操作期间可能读取错误数据的问题 [#64084](https://github.com/pingcap/tidb/pull/64084) @[mjonss](https://github.com/mjonss)
    - 修复全局索引在某些情况下返回错误结果的问题 [#61083](https://github.com/pingcap/tidb/issues/61083) @[Defined2014](https://github.com/Defined2014)
    - 修复 `character_set_results` 在遇到错误字符时进行截断而非替换的问题 [#61085](https://github.com/pingcap/tidb/issues/61085) @[xhebox](https://github.com/xhebox)
    - 修复 `ADD COLUMN` 与 `UPDATE` 并发执行时出错的问题 [#60047](https://github.com/pingcap/tidb/issues/60047) @[L-maple](https://github.com/L-maple)
    - 修复 Merge Join 在计算成本时可能遗漏过滤条件的问题 [#62917](https://github.com/pingcap/tidb/issues/62917) @[qw4990](https://github.com/qw4990) <!--tw@Oreoxmt-->


+ PD <!--tw@qiancai: 8 notes-->

    - 修复 PD Client 重试策略未正确初始化的问题 [#9013](https://github.com/tikv/pd/issues/9013) @[rleungx](https://github.com/rleungx)
    - 修复 TSO HTTP API `/config` 和 `/members` 的错误输出 [#9797](https://github.com/tikv/pd/issues/9797) @[lhy1024](https://github.com/lhy1024)
    - 修复 TSO Follower Proxy 的错误处理逻辑 [#9188](https://github.com/tikv/pd/issues/9188) @[Tema](https://github.com/Tema)
    - 修复在关闭 bucket 上报功能后，split bucket 依然生效的问题 [#9726](https://github.com/tikv/pd/issues/9726) @[bufferflies](https://github.com/bufferflies)
    - 修复 Resource Manager 错误分配 token 导致查询卡住的问题 [#9455](https://github.com/tikv/pd/issues/9455) @[JmPotato](https://github.com/JmPotato)
    - 修复 PD leader 切换后，Placement Rule 未生效问题 [#9602](https://github.com/tikv/pd/issues/9602) @[okJiang](https://github.com/okJiang)
    - 修复 PD 在解析以科学计数法表示的大数值时可能失败，从而导致部分 TTL 相关的配置不生效的问题 [#9343](https://github.com/tikv/pd/issues/9343) @[lhy1024](https://github.com/lhy1024)

+ TiFlash <!--tw@hfxsd: 5 notes-->

    - 修复当查询的列存储大量 `NULL` 值时，可能导致查询失败的问题 [#10340](https://github.com/pingcap/tiflash/issues/10340) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - 修复 TiFlash 消耗 RU 的统计数据不准确的问题 [#10380](https://github.com/pingcap/tiflash/issues/10380) @[JinheLin](https://github.com/JinheLin)
    - 修复在存算分离架构下，当存在慢查询时 TiFlash 容易发生 OOM 的问题 [#10278](https://github.com/pingcap/tiflash/issues/10278) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复在存算分离架构下，TiFlash 遇到与 S3 的网络分区时可能无限重试的问题 [#10424](https://github.com/pingcap/tiflash/issues/10424) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复当参数为 `DECIMAL` 类型时，`FLOOR()` 和 `CEIL()` 函数结果可能不正确的问题 [#10365](https://github.com/pingcap/tiflash/issues/10365) @[ChangRui-Ryan](https://github.com/ChangRui-Ryan) 

+ Tools

    + Backup & Restore (BR) <!--tw@qiancai: 7 notes-->

        - 修复日志备份中 zstd 压缩未生效，导致输出未被压缩的问题 [#18836](https://github.com/tikv/tikv/issues/18836) @[3pointer](https://github.com/3pointer)
        - 修复备份数据到 Azure Blob Storage 时 flush 偶尔会很慢的问题 [#18410](https://github.com/tikv/tikv/issues/18410) @[YuJuncen](https://github.com/YuJuncen)
        - 修复删除文件失败时可能出现 `log truncate` 的问题 [#63358](https://github.com/pingcap/tidb/issues/63358) @[YuJuncen](https://github.com/YuJuncen)
        - 修复在备份数据时如果设置 `--checksum` 为 `false` 可能导致恢复后 `mysql.stats_meta` 表的 count 列为 `0` 的问题 [#60978](https://github.com/pingcap/tidb/issues/60978) @[Leavrth](https://github.com/Leavrth)
        - 降低了 S3 兼容存储服务在启用带宽限制时使用 BR 恢复数据失败的概率 [#18846](https://github.com/tikv/tikv/issues/18846) @[kennytm](https://github.com/kennytm)
        - 修复 `log backup observer` 可能丢失对某个 Region 的监听，从而导致日志备份进度无法推进的问题 [#18243](https://github.com/tikv/tikv/issues/18243) @[Leavrth](https://github.com/Leavrth)
        - 修复当备份的表中存在一些特殊的 schema 时，可能导致 `restore point` 创建失败的问题 [#63663](https://github.com/pingcap/tidb/issues/63663) @[RidRisR](https://github.com/RidRisR)

    + TiCDC <!--tw@Oreoxmt: 7 notes-->

        - 修复在配置包含虚拟列的 Column 类型分区分发器时可能导致的 panic 问题 [#12241](https://github.com/pingcap/tiflow/issues/12241) @[wk989898](https://github.com/wk989898)
        - 修复在关闭 DDL puller 时可能引发的 panic 问题 [#12244](https://github.com/pingcap/tiflow/issues/12244) @[wk989898](https://github.com/wk989898)
        - 支持在 `filter` 配置中通过 `ignore-txn-start-ts` 参数过滤不支持的 DDL 类型 [#12286](https://github.com/pingcap/tiflow/issues/12286) @[asddongmen](https://github.com/asddongmen)
        - 修复使用 Azure Blob Storage 作为下游时可能出现数据同步任务卡住的问题 [#12277](https://github.com/pingcap/tiflow/issues/12277) @[zurakutsia](https://github.com/zurakutsia)
        - 修复 `DROP FOREIGN KEY` DDL 没有同步到下游的问题 [#12328](https://github.com/pingcap/tiflow/issues/12328) @[3AceShowHand](https://github.com/3AceShowHand)
        - 修复订阅 Region 时遇到回滚和预写条目导致 TiCDC panic 的问题 [#19048](https://github.com/tikv/tikv/issues/19048) @[3AceShowHand](https://github.com/3AceShowHand)
        - 修复 TiKV 中的断言错误可能导致 TiCDC panic 的问题 [#18498](https://github.com/tikv/tikv/issues/18498) @[tharanga](https://github.com/tharanga)
