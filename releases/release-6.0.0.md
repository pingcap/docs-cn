---
title: TiDB 6.0.0 Release Notes
---

# TiDB 6.0.0 Release Notes

Release date：x x, 2022

TiDB version: 6.0.0

## Improvements

+ TiDB

    - 当通过 `flashback` 或者 `recover` 恢复一张表之后，这张表的放置规则信息将会被清除 [#31670](https://github.com/pingcap/tidb/pull/31670)
    - 添加一个性能概览监控板，在一个监控板中的典型关键路径上显示核心性能指标，并使 TiDB 上的指标分析更加容易 [#31677](https://github.com/pingcap/tidb/pull/31677)
    - 支持 `LOAD DATA LOCAL INFILE` 语句中的 `REPLACE` 关键字 [#31303](https://github.com/pingcap/tidb/pull/31303)
    - 支持 Range 分区表上对 IN 表达式进行分区裁剪 [#31493](https://github.com/pingcap/tidb/pull/31493)
    - 消除 MPP 聚合查询中可能冗余的 Exchange 操作 [#31766](https://github.com/pingcap/tidb/pull/31766)
    - 允许在 TRUNCATE/DROP PARTITION 语句中使用重复的分区名 [#31782](https://github.com/pingcap/tidb/pull/31782)
    - 当没有指定 follower 时读取 information_schema.placement_policies 默认显示 follower 为 2 [#31927](https://github.com/pingcap/tidb/pull/31927)
    - 禁止创建索引时指定列前缀长度为 0 [#32176](https://github.com/pingcap/tidb/pull/32176)
    - ​​禁止分区名以空格结尾 [#31785](https://github.com/pingcap/tidb/pull/31785)
    - 支持新的开关可让悲观锁模式下打开自动事务提交 [#32056](https://github.com/pingcap/tidb/pull/32056)
    - 使重命名表时如果遇到错误返回的错误信息更加合理 [#32170](https://github.com/pingcap/tidb/pull/32170)
    - 支持新的系统变量 sysdate_is_now 打开后 sysdate 函数将会使用 now 函数的结果 [#31881](https://github.com/pingcap/tidb/pull/31881)
    - 支持变量 `tidb_last_ddl_info`，用于获取当前会话中的最后一个 DDL 的信息 [#32414](https://github.com/pingcap/tidb/pull/32414)
    - 给 `admin show ddl jobs` 语句的执行结果添加 `​​CREATE_TIME` 信息 [#32435](https://github.com/pingcap/tidb/pull/32435)
    - 支持新的内置函数 charset [#32470](https://github.com/pingcap/tidb/pull/32470)
    - 自动捕获的黑名单支持使用用户名来进行过滤 [#32460](https://github.com/pingcap/tidb/pull/32460)
    - 根据当前的 time_zone 对 admin show ddl jobs 的时间显示进行调整 [#32450](https://github.com/pingcap/tidb/pull/32450)
    - 支持下推 dayname monthname 函数到 TiFlash [#32595](https://github.com/pingcap/tidb/pull/32595)
    - 支持下推 regexp 函数到 TiFlash [#32636](https://github.com/pingcap/tidb/pull/32636)
    - 支持对 UnionScan 的执行情况进行追踪 [#32635](https://github.com/pingcap/tidb/pull/32635)
    - 执行 SHOW TABLE STATUS 根据当前的 time_zone 对结果进行调节 [#32449](https://github.com/pingcap/tidb/pull/32449)
    - 支持下推 greatest, least 函数到 TiFlash [#32788](https://github.com/pingcap/tidb/pull/32788)
    - 支持读取 `_tidb_rowid` 列的查询能够使用 PointGet 计划 [#32705](https://github.com/pingcap/tidb/pull/32705)
    - 支持在自动捕获的黑名单中使用通配符 [#32715](https://github.com/pingcap/tidb/pull/32715)
    - 使 explain 中输出原有的分区名而不做小写转换 [#32817](https://github.com/pingcap/tidb/pull/32817)
    - 支持对 RANGE COLUMNS 分区表在 IN 条件和字符串类型上进行分区裁剪 [#32721](https://github.com/pingcap/tidb/pull/32721)
    - 移除废弃的的系统变量 `tidb_mem_quota_hashjoin`, `tidb_mem_quota_mergejoin`, `tidb_mem_quota_sort`, `tidb_mem_quota_topn`, `tidb_mem_quota_indexlookupreader`, `tidb_mem_quota_indexlookupjoin` [#32724](https://github.com/pingcap/tidb/pull/32724)
    - 当设置系统变量为 NULL 时返回错误提示 [#32879](https://github.com/pingcap/tidb/pull/32879)
    - 移除非 MPP 模式的 broadcast join [#31459](https://github.com/pingcap/tidb/pull/31459)
    - 移除废弃的系统变量 tidb-enable-streaming [#32765](https://github.com/pingcap/tidb/pull/32765)
    - 支持下推 `dayofmonth`，`lastday` 函数到 TiFlash [#33011](https://github.com/pingcap/tidb/pull/33011)
    - 支持下推 `is_true`，`is_false`, `is_true_with_null` 函数到 TiFlash [#33048](https://github.com/pingcap/tidb/pull/33048)
    - 支持在分区表上执行 MPP 计划 [#31043](https://github.com/pingcap/tidb/pull/31043)
    - 支持 instance 级别的系统变量 [#32888](https://github.com/pingcap/tidb/pull/32888)
    - 支持下推 `dayofweek` 和 `dayofyear` 函数到 TiFlash [#33131](https://github.com/pingcap/tidb/pull/33131)
    - 支持 read-consistency 读取可在 read-committed 隔离级别下打开优化事务内读语句延迟 [#32922](https://github.com/pingcap/tidb/pull/32922)
    - 支持对 CTE 进行谓词下推 [#33158](https://github.com/pingcap/tidb/pull/33158)
    - 将 `Statement Summary` 和 `Capture Plan Baselines` 的配置设置成只在全局基础上可用 [#30756](https://github.com/pingcap/tidb/pull/30756)

+ TiKV

    - 支持日志归档，让日志格式与 TiDB/PD 统一 [#11657](https://github.com/tikv/tikv/pull/11657)
    - Raft 在心跳时更新租期 [#6427](https://github.com/tikv/tikv/pull/6427)
    - 提升 Raftstore 对大 batch 的采样准确度 [#11039](v)
    - 为 `debug/pprof/profile` 添加正确的 Content-Type，让 profile 更容易被识别 [#10951](https://github.com/tikv/tikv/pull/10951)
    - 在处理读请求时更新 Raftstore 的租期，防止延迟抖动 [#11579](https://github.com/tikv/tikv/pull/11579)
    - 默认使用 Raft Engine 来存储 Raft log [#11119](https://github.com/tikv/tikv/issues/11119)
    - 在切换 leader 时选择代价最小的 store 为目标，提升性能稳定性 [#10602](https://github.com/tikv/tikv/issues/10602)
    - 异步 fetch Raft log，减少阻塞 Raftstore 带来的性能抖动 [#11320](https://github.com/tikv/tikv/issues/11320)
    - 实现 quarter 向量化函数 [#5751](https://github.com/tikv/tikv/issues/5751)
    - 支持 Bit column 下推 [#12037](https://github.com/tikv/tikv/pull/12037)
    - 支持 mod, sysdate 函数下推 [#11916](https://github.com/tikv/tikv/issues/11916)
    - 通过减少需要 resolve lock 的 region 数量加速 CDC 恢复 [#11993](https://github.com/tikv/tikv/issues/11993)
    - 支持动态调整 max_inflight_msgs [#11865](https://github.com/tikv/tikv/issues/11865)
    - 支持 EXTRA_PHYSICAL_TABLE_ID_COL_ID [#11888](https://github.com/tikv/tikv/issues/11888)
    - 支持以 buckets 为单位进行计算 [#11759](https://github.com/tikv/tikv/issues/11759)
    - 将 RawKV API V2 的 Key 编码为 user-key + memcomparable-padding + timestamp [#11965](https://github.com/tikv/tikv/issues/11965)
    - 将 RawKV API V2 的 Value 编码为 user-value + ttl + ValueMeta，并且将 delete 编码在 ValueMeta 中 [#11965](https://github.com/tikv/tikv/issues/11965)
    - Coprocessor 支持 Projection 算子 [#12114](https://github.com/tikv/tikv/issues/12114)
    - 支持动态修改 `raftstore.raft-max-size-per-msg` [#12017](https://github.com/tikv/tikv/issues/12017)
    - 使 Grafana 支持 multi-k8s 的监控 [#12104](https://github.com/tikv/tikv/issues/12104)
    - 通过将 leader 转让给 CDC observer 减少延迟抖动 [#12111](https://github.com/tikv/tikv/issues/12111)
    - 支持动态修改 `raftstore.apply_max_batch_size` 和 `raftstore.store_max_batch_size` [#11982](https://github.com/tikv/tikv/issues/11982)
    - RawKV API V2 在收到 raw_get/raw_scan 请求时会返回最新的版本 [#11965](https://github.com/tikv/tikv/issues/11965)
    - 支持 RCCheckTS 的一致性读 [#12097](https://github.com/tikv/tikv/issues/12097)
    - 支持动态调整 scheduler pool 的线程数 [#12067](https://github.com/tikv/tikv/pull/12067)
    - 通过全局的前台限流器来控制 CPU 与带宽的使用，增加稳定性 [#11855](https://github.com/tikv/tikv/issues/11855)
    - 支持动态调整 unified-read pool 的线程数 [#11781](https://github.com/tikv/tikv/issues/11781)
    - 使用 TiKV 内部的 pipeline 替代 RocksDB pipeline，废弃 `rocksdb.enable-multibatch-write` 参数 [#12059](https://github.com/tikv/tikv/issues/12059)

+ PD

+ TiFlash

    - 禁止了TiFlash 文件的逻辑分裂（默认参数调整为：profiles.default.dt_enable_logical_split = false，详见[用户文档](https://docs.pingcap.com/zh/tidb/stable/tiflash-configuration/#tiflash-%E9%85%8D%E7%BD%AE%E5%8F%82%E6%95%B0)），优化了 TiFlash 列存储的空间使用效率，使得同一个表在同步到 TiFlash 后所占用空间与 TiKV 相近。

+ Tools

    + Backup & Restore (BR)

        - 备份数据恢复速度提升。备份数据恢复速度在 V6.0 版本有所提升，在模拟测试中恢复 16T 的备份数据到 15 台  TiKV 集群（16C），恢复吞吐可以达到 2.66 GiB/s
        - 支持放置规则 (Placement Rule) 的导入与导出。增加参数 --with-tidb-placement-mode 来控制导入时是否忽略放置规则。

    + TiCDC

        - Add changefeed lag analyze panels [#4892](https://github.com/pingcap/tiflow/issues/4891)
        - Support placement rules [#4960](https://github.com/pingcap/tiflow/issues/4846)
        - Synchronize HTTP API handling [#4494](https://github.com/pingcap/tiflow/issues/1710)
        - Add exponential backoff mechanism for restarting a changefeed. [#4262](https://github.com/pingcap/tiflow/issues/3329)
        - Set MySQL sink default isolation level to read-committed to reduce `deadlock` in MySQL [#4138](https://github.com/pingcap/tiflow/issues/3589)
        - Validate changefeed parameters on creation and revise error message [#4482](https://github.com/pingcap/tiflow/issues/1716)
        - Allow user set the configuration of Kafka producer dial/write/read timeout [#4512](https://github.com/pingcap/tiflow/issues/4385)

    + TiDB Data Migration (DM)

        - support start task with inconsistent upstream table schemas in optimistic shard mode [#3903](https://github.com/pingcap/tiflow/pull/3903)
        - support create a task in `stopped` state [#4510](https://github.com/pingcap/tiflow/pull/4510)
        - Syncer will use working directory of DM-worker rather than /tmp to write internal files, and clean it after task is stopped [[#4732]](https://github.com/pingcap/tiflow/pull/4732)

    + TiDB Lightning

        - Add more retryable error type [[#31484]](https://github.com/pingcap/tidb/pull/31484)
        - Tolerate tikv node address changes during importing [[#32876]](https://github.com/pingcap/tidb/pull/32876)

    + Dumpling

## Bug 修复

+ TiDB

    - 修复了当 `SCHEDULE = majority_in_primary`,  且 `PrimaryRegion` 和 `Regions` 的值相同时 placement rule 会报错的问题 [#31312](https://github.com/pingcap/tidb/pull/31312)
    - 修复了使用 `index lookup join` 方式执行查询时可能导致 `invalid transaction` 错误的 data race [#30487](https://github.com/pingcap/tidb/pull/30487)
    - 修复了当授予大于等于 2 个权限时 `show grants` 返回不正确的结果的问题  [#31322](https://github.com/pingcap/tidb/pull/31322)
    - 删除 noop 变量的验证，如 `rpl_semi_sync_master_wait_point`，以防它是一个空字符串，以解决升级的问题 [#31566](https://github.com/pingcap/tidb/pull/31566)
    - 通过更新 gopsutil 版本到 v3.21.12，从而修复在 macOS 12 上构建二进制时出现的警告 [#31607](https://github.com/pingcap/tidb/issues/31607)
    - 修复了给默认值为 `CURRENT_TIMESTAMP` 的字段，执行 `INSERT INTO t SET tsCol = DEFAULT` 语句时，插入零值的问题。[#29926](https://github.com/pingcap/tidb/issues/29926)
    - ​​通过避免编码字符串类型的最大值和最小非空值，修复读取结果时的报错问题。[#31743](https://github.com/pingcap/tidb/pull/31743)
    - 修复 LOAD DATA 语句处理跳脱符时可能 panic 的问题 [#30868](https://github.com/pingcap/tidb/pull/30868)
    - 修复 greatest 和 least 函数处理 collation 不正确可能导致结果错误的问题 [#31806](https://github.com/pingcap/tidb/pull/31806)
    - 修复 date_add 和 date_sub 函数可能返回错误数据类型的问题 [#31817](https://github.com/pingcap/tidb/pull/31817)
    - 修复使用 insert 语句插入数据到虚拟生成列时可能出现 panic 的问题 [#31850](https://github.com/pingcap/tidb/pull/31850)
    - 修复创建 list column 分区表时出现重复值报错的问题 [#31953](https://github.com/pingcap/tidb/pull/31953)
    - 修复 `select for update union select` 语句使用错误快照导致结果可能错误的问题 [#31956](https://github.com/pingcap/tidb/pull/31956)
    - 修复备份恢复后 region 可能不均衡的问题 [#31691](https://github.com/pingcap/tidb/pull/31691)
    - 修复 Coercibility 和 Collation 函数对 JSON 类型推导出错的问题 [#31576](https://github.com/pingcap/tidb/pull/31576)
    - 修复当设置 TiFlash 副本数为 0 时 PD 规则没有被删除的问题 [#32192](https://github.com/pingcap/tidb/pull/32192)
    - 修改数据索引不一致的错误信息帮助更易定位问题 [#31547](https://github.com/pingcap/tidb/pull/31547)
    - 修复了 `alter column set default` 语句在特殊情况下可能会错误地更新列信息 [#32249](https://github.com/pingcap/tidb/pull/32249)
    - 修复一些内置函数处理 JSON 类型时出现类型错误的问题 [#32301](https://github.com/pingcap/tidb/pull/32301)
    - 修复 date_format 对 ‘\n’ 字符处理错误的问题 [#32358](https://github.com/pingcap/tidb/pull/32358)
    - 修复使用 join 更新分区表时可能报错的问题 [#31779](https://github.com/pingcap/tidb/pull/31779)
    - 修复 Nulleq 函数作用在 Enum 类型上可能出现结果错误的问题 [#32440](https://github.com/pingcap/tidb/pull/32440)
    - 修复 upper 和 lower 函数可能造成 panic 的问题 [#32505](https://github.com/pingcap/tidb/pull/32505)
    - 修复了将其他类型列更改为时间戳类型列时可能遇到的时区问题 [#31843](https://github.com/pingcap/tidb/pull/31843)
    - 修复使用 ChunkRPC 导出数据时可能造成 TiDB OOM 的问题 [#32554](https://github.com/pingcap/tidb/pull/32554)
    - 修复动态模式下访问分区表时 Limit 在子查询中不能生效的问题 [#32548](https://github.com/pingcap/tidb/pull/32548)
    - 修复 `INFORMATION_SCHEMA.COLUMNS` 表中 `bit` 类型默认值格式显示问题 [#32701](https://github.com/pingcap/tidb/pull/32701)
    - 修复重启实例后 list 分区表的分区裁剪可能不生效的问题 [#32621](https://github.com/pingcap/tidb/pull/32621)
    - 修复了在执行 `SET timestamp` 语句后，`add column` 语句可能会使用错误的默认时间戳的问题 [#32384](https://github.com/pingcap/tidb/pull/32384)
    - 修复使用 MySQL 5.5/5.6 客户端连接 TiDB 无密码用户时可能失败的问题 [#32338](https://github.com/pingcap/tidb/pull/32338)
    - 修复在事务中使用动态模式读取分区表结果有误的问题 [#31634](https://github.com/pingcap/tidb/pull/31634)
    - 修复 TiDB 可能向 TiFlash 发送重复任务的问题 [#32813](https://github.com/pingcap/tidb/pull/32813)
    - 修复 `timdiff` 函数在输入包含毫秒时可能出现结果错误的问题 [#32896](https://github.com/pingcap/tidb/pull/32896)
    - 修复用 `select … from pt partition(p)` 显式读取分区并使用 IndexJoin 计划时可能出现结果错误的问题 [#32093](https://github.com/pingcap/tidb/pull/32093)
    - 修复重命名列和修改列类型并发执行时出错的问题 [#32993](https://github.com/pingcap/tidb/pull/32993)
    - 修复错误的 MPP 计划的网络代价公式 [#32942](https://github.com/pingcap/tidb/pull/32942)
    - 修复 `KILL TIDB` 在空闲链接上无法立即生效的问题 [#32809](https://github.com/pingcap/tidb/pull/32809)
    - 修复使用包含过滤条件的 UnionScan 读取生成列时可能出现结果错误的问题 [#33050](https://github.com/pingcap/tidb/pull/33050)
    - 修复使用 left join 同时删除多张表数据时可能出现错误结果的问题 [#33055](https://github.com/pingcap/tidb/pull/33055)
    - 修复 `subtime` 函数在出现 Overflow 时可能返回错误结果的问题 [#32903](https://github.com/pingcap/tidb/pull/32903)
    - 修复当聚合查询包含 having 条件时 Selection 算子不能被下推的问题 [#33168](https://github.com/pingcap/tidb/pull/33168)
    - 修复查询报错时可能阻塞 CTE 的问题 [#33085](https://github.com/pingcap/tidb/pull/33085)

+ TiKV

    - 修复 Peer 状态为 Applying 时快照文件被删除会造成 Panic 的问题 [#11746](https://github.com/tikv/tikv/issues/11746)
    - 修复开启流量控制且显式设置 level0_slowdown_trigger 时出现 QPS 下降的问题 [#11424](https://github.com/tikv/tikv/issues/11424)
    - 修复删除 Peer 可能造成高延迟的问题 [#10210](https://github.com/tikv/tikv/issues/10210)
    - 修复在某些 corner case 下 storeMeta 内数据被意外删除引发 panic 的问题 [#11852](https://github.com/tikv/tikv/issues/11852)
    - 修复 GC worker 繁忙后无法执行范围删除（即执行 unsafe_destroy_range 参数）的问题 [#11903](https://github.com/tikv/tikv/issues/11903)
    - 关闭 ARM 上的 profiling，防止 TiKV panic [#10658](https://github.com/tikv/tikv/issues/10658)
    - 修复 TiKV 运行 2 年以上可能 panic 的问题 [#11940](https://github.com/tikv/tikv/issues/11940)
    - 修复因缺少 SSE 指令集在 arm64 上的编译问题 [#12034](https://github.com/tikv/tikv/issues/12034)
    - 修复删除未初始化的副本可能会造成旧副本被重新创建的问题 [#10533](https://github.com/tikv/tikv/issues/10533)
    - 修复 stale message 造成 TiKV panic 的问题 [#12023](https://github.com/tikv/tikv/issues/12023)
    - 修复 TsSet 转换可能发生 UB 的问题 [#12070](https://github.com/tikv/tikv/issues/12070)
    - 修复在 replica read 下可能违反 linearizability 的问题 [#12109](https://github.com/tikv/tikv/issues/12109)
    - 修复在 Ubuntu 18.04 下 profiling 会造成 TiKV 崩溃的问题 [#9765](https://github.com/tikv/tikv/issues/9765)
    - 修复 tikv-ctl 对 `bad-ssts` 结果字符串的错误匹配问题 [#12049](https://github.com/tikv/tikv/pull/12049)

+ PD

    *

+ TiFlash

    - Fix the problem of TiFlash crashing when the memory limit is enabled [https://github.com/pingcap/tiflash/issues/3902](https://github.com/pingcap/tiflash/issues/3902)
    - Fix the problem that expired data was recycled slowly [https://github.com/pingcap/tiflash/issues/4146](https://github.com/pingcap/tiflash/issues/4146)
    - Avoid the potential of crash when apply snapshot under heavy ddl scenario [https://github.com/pingcap/tiflash/issues/4072](https://github.com/pingcap/tiflash/issues/4072)
    - Fix potential query error after adding column under heavy read workload [https://github.com/pingcap/tiflash/issues/3967](https://github.com/pingcap/tiflash/issues/3967)
    - Fix sqrt with neg arg to return Null instead of NaN [https://github.com/pingcap/tiflash/issues/3598](https://github.com/pingcap/tiflash/issues/3598)
    - Fix cast to decimal may cause overflow [https://github.com/pingcap/tiflash/issues/3920](https://github.com/pingcap/tiflash/issues/3920)
    - Fix wrong result for function `in` [https://github.com/pingcap/tiflash/issues/4016](https://github.com/pingcap/tiflash/issues/4016)
    - Fix date format identifies '\n' as invalid separator [https://github.com/pingcap/tiflash/issues/4036](https://github.com/pingcap/tiflash/issues/4036)
    - Fix the issue that learner read process takes too much time under high concurrency scenarios [https://github.com/pingcap/tiflash/issues/3555](https://github.com/pingcap/tiflash/issues/3555)
    - Fix wrong result when cast datetime to decimal [https://github.com/pingcap/tiflash/issues/4151](https://github.com/pingcap/tiflash/issues/4151)
    - Fix memory leak when a query is canceled [https://github.com/pingcap/tiflash/issues/4098](https://github.com/pingcap/tiflash/issues/4098)
    - Fix bug that enable elastic thread pool may introduce memory leak [https://github.com/pingcap/tiflash/issues/4098](https://github.com/pingcap/tiflash/issues/4098)
    - Fix the bug that canceled MPP query may cause tasks hang forever when local tunnel is enabled [https://github.com/pingcap/tiflash/issues/4229](https://github.com/pingcap/tiflash/issues/4229)
    - Fix bug that failure of HashJoin build side may cause MPP query hang forever [https://github.com/pingcap/tiflash/issues/4195](https://github.com/pingcap/tiflash/issues/4195)
    - Fix bug that MPP tasks may leak threads forever [https://github.com/pingcap/tiflash/issues/4238](https://github.com/pingcap/tiflash/issues/4238)

+ Tools

    + Backup & Restore (BR)

        - Fix a bug that caused BR get stuck when restore meets some unrecoverable error.[#33200](https://github.com/pingcap/tidb/issues/33200)
        - Fix a bug that encrypt info lost  during backup retry which cause restore failed. [#32423] (https://github.com/pingcap/tidb/issues/32423)

    + TiCDC

        - Fix the problem that TiCDC cannot send messages when `min.insync.replicas` is less than `replication-factor` [#4263](https://github.com/pingcap/tiflow/issues/3994)
        - Fix a bug that MySQL sink will generate duplicated replace SQL if `batch-replace-enable` is disabled. [#4502](https://github.com/pingcap/tiflow/issues/4501)
        - Fix a bug that owner exits abnormally when PD leader is killed [#4474](https://github.com/pingcap/tiflow/issues/4248)
        - Fix `Unknown system variable 'transaction_isolation'` for some mysql versions [#4569](https://github.com/pingcap/tiflow/issues/4504)
        - Fix `Canal-JSON` meet `unsigned` SQL typed in `string`, which cause CDC server panic. [#4629](https://github.com/pingcap/tiflow/issues/4635)
        - Fix a bug that sequence should not be replicated even if force-replication is true. [#4563](https://github.com/pingcap/tiflow/issues/4552)
        - Fix `Canal-JSON` meet `unsigned` SQL Type and nullable, which cause CDC server panic. [#4741](https://github.com/pingcap/tiflow/issues/4736)
        - Fix the wrong data mapping for avro codec of type Enum/Set and TinyText/MediumText/Text/LongText. [#4704](https://github.com/pingcap/tiflow/issues/4454)
        - Fix converting not null column to Avro nullable field schema. [#4829](https://github.com/pingcap/tiflow/issues/4818)
        - Fix an issue that TiCDC can not exit. [#4831](https://github.com/pingcap/tiflow/issues/4699)

    + TiDB Data Migration (DM)

        - Fix a bug that upstream metrics won't update if no query-status [#4281]([https://github.com/pingcap/tiflow/issues/4281](https://github.com/pingcap/tiflow/issues/4281))
        - Fix the issue that update statement execute error in safemode may cause DM-worker panic [#4317]([https://github.com/pingcap/tiflow/issues/4317](https://github.com/pingcap/tiflow/issues/4317))
        - Fix a bug that multiple worker write for same upstream [#3737]([https://github.com/pingcap/tiflow/issues/3737](https://github.com/pingcap/tiflow/issues/3737))
        - Fix a bug that long varchar will report error of "Column length too big                    [#4637]([https://github.com/pingcap/tiflow/issues/4637](https://github.com/pingcap/tiflow/issues/4637))
        - Fix that there are lot of log of "checkpoint has no change, skip sync flush checkpoint" and performance may drop [#4619]([https://github.com/pingcap/tiflow/issues/4619](https://github.com/pingcap/tiflow/issues/4619))

    + TiDB Lightning

        - Fix storage not exist error [#31656]([https://github.com/pingcap/tidb/issues/31656](https://github.com/pingcap/tidb/issues/31656))
        - Fix the bug that lightning may not clean up metadata schema when some of the import contains no source files [#28144]([https://github.com/pingcap/tidb/issues/28144](https://github.com/pingcap/tidb/issues/28144))
        - Fix panic when table name in source file and target cluster is different          [#31771]([https://github.com/pingcap/tidb/issues/31771](https://github.com/pingcap/tidb/issues/31771))
        - Fix checksum encountered “GC life time is shorter than transaction duration” error [#32733]([https://github.com/pingcap/tidb/issues/32733](https://github.com/pingcap/tidb/issues/32733))
        - Fix lightning get stuck when check table empty failed [#31797]([https://github.com/pingcap/tidb/issues/31797](https://github.com/pingcap/tidb/issues/31797)

    + Dumpling

        - Fix incorrect progress report when dump with --sql [#30532]([https://github.com/pingcap/tidb/issues/30532](https://github.com/pingcap/tidb/issues/30532))
        - Fix the problem that dumpling can't dump with --compress and s3 output directory [#30534]([https://github.com/pingcap/tidb/issues/30534](https://github.com/pingcap/tidb/issues/30534))