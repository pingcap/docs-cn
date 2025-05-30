---
title: TiDB 7.1.6 Release Notes
summary: 了解 TiDB 7.1.6 版本的兼容性变更、改进提升，以及错误修复。
---

# TiDB 7.1.6 Release Notes

发版日期：2024 年 11 月 21 日

TiDB 版本：7.1.6

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v7.1/quick-start-with-tidb) | [生产部署](https://docs.pingcap.com/zh/tidb/v7.1/production-deployment-using-tiup) | [下载离线包](https://cn.pingcap.com/product-community/?version=v7.1.6#version-list)

## 兼容性变更

- 通过 [TiDB HTTP API](https://github.com/pingcap/tidb/blob/release-7.1/docs/tidb_http_api.md) 获取 DDL 历史任务时，默认获取任务数量的上限为 2048，以避免历史任务数量过多导致 OOM 的问题 [#55711](https://github.com/pingcap/tidb/issues/55711) @[joccau](https://github.com/joccau)
- 在之前的版本中，TiCDC 在处理包含 `UPDATE` 变更的事务时，如果事件的主键或者非空唯一索引的列值发生改变，则会将该条事件拆分为 `DELETE` 和 `INSERT` 两条事件。从 v7.1.6 开始，当使用 MySQL Sink 时，如果 `UPDATE` 变更所在事务的 `commitTS` 小于对应表开始向下游同步数据时从 PD 获取的当前时间戳 `thresholdTS`，TiCDC 就会将该 `UPDATE` 事件拆分为 `DELETE` 和 `INSERT` 两条事件，然后写入 Sorter 模块。该行为变更解决了由于 TiCDC 接收到的 `UPDATE` 事件顺序可能不正确，导致拆分后的 `DELETE` 和 `INSERT` 事件顺序也可能不正确，从而引发下游数据不一致的问题。更多信息，请参考[用户文档](https://docs.pingcap.com/zh/tidb/v7.1/ticdc-split-update-behavior#mysql-sink-拆分-update-事件行为说明)。[#10918](https://github.com/pingcap/tiflow/issues/10918) @[lidezhu](https://github.com/lidezhu)
- 使用 TiDB Lightning 的严格格式 `strict-format` 导入 CSV 文件时，必须设置行分隔符 [#37338](https://github.com/pingcap/tidb/issues/37338) @[lance6716](https://github.com/lance6716)
- TiKV 配置项 [`server.grpc-compression-type`](/tikv-configuration-file.md#grpc-compression-type) 的作用范围发生变更：

    - 在 v7.1.6 之前的 7.1.x 版本中，该配置项只影响 TiKV 节点之间的 gRPC 消息的压缩算法。
    - 从 v7.1.6 起，该配置项也会影响 TiKV 向 TiDB 发送的 gRPC（响应）消息的压缩算法，开启压缩可能消耗更多 CPU 资源。[#17176](https://github.com/tikv/tikv/issues/17176) @[ekexium](https://github.com/ekexium)

## 改进提升

+ TiDB

    - 当某个统计信息完全由 TopN 构成，且对应表的统计信息中修改行数不为 0 时，对于未命中 TopN 的等值条件，估算结果从 0 调整为 1 [#47400](https://github.com/pingcap/tidb/issues/47400) @[terry1purcell](https://github.com/terry1purcell)
    - 在 MPP 负载均衡时移除不包含任何 Region 的 Store [#52313](https://github.com/pingcap/tidb/issues/52313) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - 优化表达式默认值在 `SHOW CREATE TABLE` 结果中的 MySQL 兼容性 [#52939](https://github.com/pingcap/tidb/issues/52939) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - 通过批量删除 TiFlash placement rule 的方式，提升对分区表执行 `TRUNCATE`、`DROP` 后数据 GC 的处理速度 [#54068](https://github.com/pingcap/tidb/issues/54068) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - 改进 sync load 的性能，减少加载统计信息的延时 [#52994](https://github.com/pingcap/tidb/issues/52294) [hawkingrei](https://github.com/hawkingrei)

+ TiKV

    - 增加 peer 和 store 消息的 slow log [#16600](https://github.com/tikv/tikv/issues/16600) @[Connor1996](https://github.com/Connor1996)
    - 优化存在大量 DELETE 版本时 RocksDB 的 compaction 触发机制，以加快磁盘空间回收 [#17269](https://github.com/tikv/tikv/issues/17269) @[AndreMouche](https://github.com/AndreMouche)
    - 优化 TiKV 重启时由于需要等待应用之前的日志而造成访问延时抖动的情况，提升了 TiKV 的稳定性 [#15874](https://github.com/tikv/tikv/issues/15874) @[LykxSassinator](https://github.com/LykxSassinator)
    - 删除非必要的 async block 以减少内存使用 [#16540](https://github.com/tikv/tikv/issues/16540) @[overvenus](https://github.com/overvenus)

+ TiFlash

    - 优化 `LENGTH()` 和 `ASCII()` 函数执行效率 [#9344](https://github.com/pingcap/tiflash/issues/9344) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - 降低 TiFlash 在开启 TLS 后因更新证书而导致 panic 的概率 [#8535](https://github.com/pingcap/tiflash/issues/8535) @[windtalker](https://github.com/windtalker)
    - 改进 JOIN 算子的取消机制，使得 JOIN 算子内部能及时响应取消请求 [#9430](https://github.com/pingcap/tiflash/issues/9430) @[windtalker](https://github.com/windtalker)
    - 减少数据高并发读取下的锁冲突，优化短查询性能 [#9125](https://github.com/pingcap/tiflash/issues/9125) @[JinheLin](https://github.com/JinheLin)
    - 提升聚簇索引表在后台回收过期数据的速度 [#9529](https://github.com/pingcap/tiflash/issues/9529) @[JaySon-Huang](https://github.com/JaySon-Huang)

+ Tools

    + Backup & Restore (BR)

        - 提高日志备份对 Merge 的容忍度，如果遇到合理的长时间 Merge 操作，日志备份任务不容易进入 Error 状态 [#16554](https://github.com/tikv/tikv/issues/16554) @[YuJuncen](https://github.com/YuJuncen)
        - BR 在恢复数据过程中，会清理空的 SST 文件 [#16005](https://github.com/tikv/tikv/issues/16005) @[Leavrth](https://github.com/Leavrth)
        - 增加由于 DNS 错误而导致的失败的重试次数 [#53029](https://github.com/pingcap/tidb/issues/53029) @[YuJuncen](https://github.com/YuJuncen)
        - 增加因 Region 没有 leader 导致的失败重试次数 [#54017](https://github.com/pingcap/tidb/issues/54017) @[Leavrth](https://github.com/Leavrth)
        - 去掉除了 `br log restore` 子命令之外其它 `br log` 子命令对 TiDB `domain` 数据结构的载入，降低内存消耗 [#52088](https://github.com/pingcap/tidb/issues/52088) @[Leavrth](https://github.com/Leavrth)
        - 在 TiKV 下载每个 SST 文件之前，新增对 TiKV 是否有足够磁盘空间的检查；如果空间不足，BR 会终止恢复并返回错误 [#17224](https://github.com/tikv/tikv/issues/17224) @[RidRisR](https://github.com/RidRisR)
        - 支持通过环境变量设置阿里云访问身份 [#45551](https://github.com/pingcap/tidb/issues/45551) @[RidRisR](https://github.com/RidRisR)
        - 减少备份过程中无效日志的打印 [#55902](https://github.com/pingcap/tidb/issues/55902) @[Leavrth](https://github.com/Leavrth)

    + TiCDC

        - 支持当下游为消息队列 (Message Queue, MQ) 或存储服务时直接输出原始事件 [#11211](https://github.com/pingcap/tiflow/issues/11211) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - 提升使用 redo log 恢复数据过程中的内存稳定性，减少 OOM 的概率 [#10900](https://github.com/pingcap/tiflow/issues/10900) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - 当下游为 TiDB 且授予 `SUPER` 权限时，TiCDC 支持从下游数据库查询 `ADD INDEX DDL` 的执行状态，以避免某些情况下因重试执行 DDL 语句超时而导致数据同步失败 [#10682](https://github.com/pingcap/tiflow/issues/10682) @[CharlesCheung96](https://github.com/CharlesCheung96)

    + TiDB Data Migration (DM)

        - 升级 `go-mysql` 到 1.9.1 以支持使用 19 个字符以上的密码连接到 MySQL server 8.0 [#11603](https://github.com/pingcap/tiflow/pull/11603) @[fishiu](https://github.com/fishiu)

## 错误修复

+ TiDB

    - 修复添加唯一索引时并发 DML 导致数据索引不一致的问题 [#52914](https://github.com/pingcap/tidb/issues/52914) @[wjhuang2016](https://github.com/wjhuang2016)
    - 修复 `YEAR` 类型的列与超出范围的无符号整数进行比较导致错误结果的问题 [#50235](https://github.com/pingcap/tidb/issues/50235) @[qw4990](https://github.com/qw4990)
    - 修复当 SQL 异常中断时，`INDEX_HASH_JOIN` 无法正常退出的问题 [#54688](https://github.com/pingcap/tidb/issues/54688) @[wshwsh12](https://github.com/wshwsh12)
    - 修复使用分布式框架添加索引期间出现网络分区可能导致数据索引不一致的问题 [#54897](https://github.com/pingcap/tidb/issues/54897) @[tangenta](https://github.com/tangenta)
    - 修复使用 `SHOW WARNINGS;` 获取警告时可能导致 panic 的问题 [#48756](https://github.com/pingcap/tidb/issues/48756) @[xhebox](https://github.com/xhebox)
    - 修复查询 `INFORMATION_SCHEMA.CLUSTER_SLOW_QUERY` 表可能导致 TiDB panic 的问题 [#54324](https://github.com/pingcap/tidb/issues/54324) @[tiancaiamao](https://github.com/tiancaiamao)
    - 修复在 `HashJoin` 或 `IndexLookUp` 算子作为 `Apply` 算子的被驱动侧子节点时，由于 `memTracker` 未被析构而导致的内存异常高的问题 [#54005](https://github.com/pingcap/tidb/issues/54005) @[XuHuaiyu](https://github.com/XuHuaiyu)
    - 修复递归 CTE 查询可能导致无效指针的问题 [#54449](https://github.com/pingcap/tidb/issues/54449) @[hawkingrei](https://github.com/hawkingrei)
    - 修复空 Projection 导致 TiDB panic 的问题 [#49109](https://github.com/pingcap/tidb/issues/49109) @[winoros](https://github.com/winoros)
    - 修复在包含数据修改操作的事务中查询带有虚拟列的表时，查询结果可能错误的问题 [#53951](https://github.com/pingcap/tidb/issues/53951) @[qw4990](https://github.com/qw4990)
    - 修复当表中包含 `AUTO_ID_CACHE=1` 的自增列时，系统变量 `auto_increment_increment` 和 `auto_increment_offset` 配置为非默认值可能导致自增 ID 分配错误的问题 [#52622](https://github.com/pingcap/tidb/issues/52622) @[tiancaiamao](https://github.com/tiancaiamao)
    - 修复 `ALL` 函数中包含子查询时可能会出现错误结果的问题 [#52755](https://github.com/pingcap/tidb/issues/52755) @[hawkingrei](https://github.com/hawkingrei)
    - 修复当 SQL 查询的过滤条件中包含虚拟列，且执行条件中包含 `UnionScan` 时，谓词无法正常下推的问题 [#54870](https://github.com/pingcap/tidb/issues/54870) @[qw4990](https://github.com/qw4990)
    - 修复 `UPDATE` List 中包含子查询可能会导致 TiDB panic 的问题 [#52687](https://github.com/pingcap/tidb/issues/52687) @[winoros](https://github.com/winoros)
    - 修复在 `GROUP BY` 语句中引用间接占位符 `?` 无法找到列的问题 [#53872](https://github.com/pingcap/tidb/issues/53872) @[qw4990](https://github.com/qw4990)
    - 修复 `Sort` 算子发生落盘且查询出错后，磁盘文件可能没被删除的问题 [#55061](https://github.com/pingcap/tidb/issues/55061) @[wshwsh12](https://github.com/wshwsh12)
    - 修复针对 `SELECT ... FOR UPDATE` 复用了错误点查询计划的问题 [#54652](https://github.com/pingcap/tidb/issues/54652) @[qw4990](https://github.com/qw4990)
    - 修复 `max_execute_time` 多层设置相互影响的问题 [#50914](https://github.com/pingcap/tidb/issues/50914) @[jiyfhust](https://github.com/jiyfhust)
    - 修复重启 TiDB 后，主键列统计信息中的直方图和 TopN 未被加载的问题 [#37548](https://github.com/pingcap/tidb/issues/37548) @[hawkingrei](https://github.com/hawkingrei)
    - 修复 TopN 算子可能被错误地下推的问题 [#37986](https://github.com/pingcap/tidb/issues/37986) @[qw4990](https://github.com/qw4990)
    - 修复 `SELECT ... WHERE ... ORDER BY ...` 语句在某些情况下执行效率低的性能问题 [#54969](https://github.com/pingcap/tidb/issues/54969) @[tiancaiamao](https://github.com/tiancaiamao)
    - 修复 TiDB 关闭连接时，在某些情况下会在日志中报错的问题 [#53689](https://github.com/pingcap/tidb/issues/53689) @[jackysp](https://github.com/jackysp)
    - 修复某些情况下可以创建非法的 `DECIMAL(0,0)` 列类型的问题 [#53779](https://github.com/pingcap/tidb/issues/53779) @[tangenta](https://github.com/tangenta)
    - 修复当视图定义中使用子查询作为列定义时，通过 `information_schema.columns` 获取列信息返回告警 Warning 1356 的问题 [#54343](https://github.com/pingcap/tidb/issues/54343) @[lance6716](https://github.com/lance6716)
    - 修复当查询条件为 `column IS NULL` 访问唯一索引时，优化器将行数错误地估算为 1 的问题 [#56116](https://github.com/pingcap/tidb/issues/56116) @[hawkingrei](https://github.com/hawkingrei)
    - 修复在聚簇索引作为谓词时 `SELECT INTO OUTFILE` 不生效的问题 [#42093](https://github.com/pingcap/tidb/issues/42093) @[qw4990](https://github.com/qw4990)
    - 修复使用 Optimizer Hints 时，可能输出错误的 WARNINGS 信息的问题 [#53767](https://github.com/pingcap/tidb/issues/53767) @[hawkingrei](https://github.com/hawkingrei)
    - 修复 Sync Load QPS 监控指标显示不正确的问题 [#53558](https://github.com/pingcap/tidb/issues/53558) @[hawkingrei](https://github.com/hawkingrei)
    - 修复并发执行 `CREATE OR REPLACE VIEW` 可能报错 `table doesn't exist` 的问题 [#53673](https://github.com/pingcap/tidb/issues/53673) @[tangenta](https://github.com/tangenta)
    - 修复通过 `RESTORE` 语句恢复 `AUTO_ID_CACHE=1` 的表时，会遇到 `Duplicate entry` 报错的问题 [#52680](https://github.com/pingcap/tidb/issues/52680) @[tiancaiamao](https://github.com/tiancaiamao)
    - 修复 `INFORMATION_SCHEMA.STATISTICS` 表中 `SUB_PART` 值为空的问题 [#55812](https://github.com/pingcap/tidb/issues/55812) @[Defined2014](https://github.com/Defined2014)
    - 修复 `Longlong` 类型在谓词中溢出的问题 [#45783](https://github.com/pingcap/tidb/issues/45783) @[hawkingrei](https://github.com/hawkingrei)
    - 修复当被缓存的执行计划包含日期类型和 `unix_timestamp` 的比较时，结果出现错误的问题 [#48165](https://github.com/pingcap/tidb/issues/48165) @[qw4990](https://github.com/qw4990)
    - 修复当排序规则为 `utf8_bin` 或 `utf8mb4_bin` 时意外消除 `LENGTH()` 条件的错误 [#53730](https://github.com/pingcap/tidb/issues/53730) @[elsa0520](https://github.com/elsa0520)
    - 修复当 `UPDATE` 或 `DELETE` 语句包含递归的 CTE 时，语句可能报错或不生效的问题 [#55666](https://github.com/pingcap/tidb/issues/55666) @[time-and-fate](https://github.com/time-and-fate)
    - 修复执行一条包含关联子查询和 CTE 的查询时，TiDB 可能卡住或返回错误结果的问题 [#55551](https://github.com/pingcap/tidb/issues/55551) @[guo-shaoge](https://github.com/guo-shaoge)
    - 修复统计信息初始化时，使用非二进制排序规则的字符串类型列的统计信息可能无法正常加载的问题 [#55684](https://github.com/pingcap/tidb/issues/55684) @[winoros](https://github.com/winoros)
    - 修复 IndexJoin 在 Left Outer Anti Semi 类型下计算哈希值时产生重复行的问题 [#52902](https://github.com/pingcap/tidb/issues/52902) @[yibin87](https://github.com/yibin87)
    - 修复包含 `UNION` 的查询语句可能返回错误结果的问题 [#52985](https://github.com/pingcap/tidb/issues/52985) @[XuHuaiyu](https://github.com/XuHuaiyu)
    - 修复 `StreamAggExec` 中的空 `groupOffset` 可能会导致 panic 的问题 [#53867](https://github.com/pingcap/tidb/issues/53867) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - 修复可以创建非严格自增的 RANGE 分区表的问题 [#54829](https://github.com/pingcap/tidb/issues/54829) @[Defined2014](https://github.com/Defined2014)
    - 修复由于查询超出 `tidb_mem_quota_query` 设定的内存使用限制，导致终止查询时可能卡住的问题 [#55042](https://github.com/pingcap/tidb/issues/55042) @[yibin87](https://github.com/yibin87)
    - 修复 `INFORMATION_SCHEMA.TIDB_TRX` 表中 `STATE` 字段的 `size` 未定义导致 `STATE` 显示为空的问题 [#53026](https://github.com/pingcap/tidb/issues/53026) @[cfzjywxk](https://github.com/cfzjywxk)
    - 修复 `IndexNestedLoopHashJoin` 中存在数据竞争的问题 [#49692](https://github.com/pingcap/tidb/issues/49692) @[solotzg](https://github.com/solotzg)
    - 修复错误的 TableDual 计划导致查询结果为空的问题 [#50051](https://github.com/pingcap/tidb/issues/50051) @[onlyacat](https://github.com/onlyacat)
    - 修复 `mysql.stats_histograms` 表的 `tot_col_size` 列可能为负数的潜在风险 [#55126](https://github.com/pingcap/tidb/issues/55126) @[qw4990](https://github.com/qw4990)
    - 修复将数据从 `FLOAT` 类型转换为 `UNSIGNED` 类型时结果错误的问题 [#41736](https://github.com/pingcap/tidb/issues/41736) @[guo-shaoge](https://github.com/guo-shaoge)
    - 修复使用 `auth_socket` 认证插件时，TiDB 在某些情况下未能拒绝不符合身份认证的用户连接的问题 [#54031](https://github.com/pingcap/tidb/issues/54031) @[lcwangchao](https://github.com/lcwangchao)
    - 修复 `memory_quota` Hint 在子查询中可能不生效的问题 [#53834](https://github.com/pingcap/tidb/issues/53834) @[qw4990](https://github.com/qw4990)
    - 修复元数据锁在计划缓存场景下未能阻止 DDL 推进的问题 [#51407](https://github.com/pingcap/tidb/issues/51407) @[wjhuang2016](https://github.com/wjhuang2016)
    - 修复使用 `CURRENT_DATE()` 作为列默认值时查询结果错误的问题 [#53746](https://github.com/pingcap/tidb/issues/53746) @[tangenta](https://github.com/tangenta)
    - 修复 `COALESCE()` 函数对于 `DATE` 类型参数返回结果类型不正确的问题 [#46475](https://github.com/pingcap/tidb/issues/46475) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - 通过重置 `PipelinedWindow` 的 `Open` 方法中的参数，修复当 `PipelinedWindow` 作为 apply 的子节点使用时，由于重复的打开和关闭操作导致重用之前的参数值而发生的意外错误 [#53600](https://github.com/pingcap/tidb/issues/53600) @[XuHuaiyu](https://github.com/XuHuaiyu)
    - 修复关联子查询中 TopN 算子结果不正确的问题 [#52777](https://github.com/pingcap/tidb/issues/52777) @[yibin87](https://github.com/yibin87)
    - 修复递归的 CTE 算子错误地跟踪内存使用的问题 [#54181](https://github.com/pingcap/tidb/issues/54181) @[guo-shaoge](https://github.com/guo-shaoge)
    - 修复使用 `SHOW COLUMNS` 查看视图中的列时报错的问题 [#54964](https://github.com/pingcap/tidb/issues/54964) @[lance6716](https://github.com/lance6716)
    - 修复在 TTL 任务执行过程中，减小 `tidb_ttl_delete_worker_count` 的值导致任务无法完成的问题 [#55561](https://github.com/pingcap/tidb/issues/55561) @[lcwangchao](https://github.com/lcwangchao)
    - 修复在递归 CTE 中无法使用视图的问题 [#49721](https://github.com/pingcap/tidb/issues/49721) @[hawkingrei](https://github.com/hawkingrei)
    - 修复创建带有外键的表时，TiDB 未创建对应的统计信息元信息 (`stats_meta`) 的问题 [#53652](https://github.com/pingcap/tidb/issues/53652) @[hawkingrei](https://github.com/hawkingrei)
    - 修复查询被 kill 之后可能返回错误结果而非报错的问题 [#50089](https://github.com/pingcap/tidb/issues/50089) @[D3Hunter](https://github.com/D3Hunter)
    - 修复在查询并发较高时，统计信息同步加载机制可能意外加载失败的问题 [#52294](https://github.com/pingcap/tidb/issues/52294) @[hawkingrei](https://github.com/hawkingrei)
    - 修复查询中的某些过滤条件可能导致 planner 模块发生 `invalid memory address or nil pointer dereference` 报错的问题 [#53582](https://github.com/pingcap/tidb/issues/53582) [#53580](https://github.com/pingcap/tidb/issues/53580) [#53594](https://github.com/pingcap/tidb/issues/53594) [#53603](https://github.com/pingcap/tidb/issues/53603) @[YangKeao](https://github.com/YangKeao)
    - 修复 TiDB 统计信息同步加载机制无限重试加载空统计信息并打印 `fail to get stats version for this histogram` 日志的问题 [#52657](https://github.com/pingcap/tidb/issues/52657) @[hawkingrei](https://github.com/hawkingrei)
    - 修复当第一个参数是 `month` 并且第二个参数是负数时，`TIMESTAMPADD()` 函数会进入无限循环的问题 [#54908](https://github.com/pingcap/tidb/issues/54908) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - 修复启用 `tidb_mem_quota_analyze` 时，更新统计信息使用的内存超过限制可能导致 TiDB crash 的问题 [#52601](https://github.com/pingcap/tidb/issues/52601) @[hawkingrei](https://github.com/hawkingrei)
    - 修复添加唯一索引时可能遇到 `duplicate entry` 的问题 [#56161](https://github.com/pingcap/tidb/issues/56161) @[tangenta](https://github.com/tangenta)
    - 修复 information schema 缓存未命中导致 stale read 查询延迟上升的问题 [#53428](https://github.com/pingcap/tidb/issues/53428) @[crazycs520](https://github.com/crazycs520)
    - 修复 GlobalStats 中的 `Distinct_count` 信息可能错误的问题 [#53752](https://github.com/pingcap/tidb/issues/53752) @[hawkingrei](https://github.com/hawkingrei)
    - 修复执行 `SELECT DISTINCT CAST(col AS DECIMAL), CAST(col AS SIGNED) FROM ...` 查询时结果出错的问题 [#53726](https://github.com/pingcap/tidb/issues/53726) @[hawkingrei](https://github.com/hawkingrei)
    - 修复当一个查询有索引合并 (Index Merge) 执行计划可用时，`read_from_storage` hint 可能不生效的问题 [#56217](https://github.com/pingcap/tidb/issues/56217) @[AilinKid](https://github.com/AilinKid)
    - 修复 `TIMESTAMPADD()` 函数结果错误的问题 [#41052](https://github.com/pingcap/tidb/issues/41052) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - 修复使用 `PREPARE`/`EXECUTE` 方式执行带 `CONV` 表达式的语句，且 `CONV` 表达式包含 `?` 参数时，多次执行可能导致查询结果错误的问题 [#53505](https://github.com/pingcap/tidb/issues/53505) @[qw4990](https://github.com/qw4990)
    - 修复事务占用的内存可能被多次重复统计的问题 [#53984](https://github.com/pingcap/tidb/issues/53984) @[ekexium](https://github.com/ekexium)
    - 修复列裁剪未对数组进行浅拷贝可能导致 TiDB panic 的问题 [#52768](https://github.com/pingcap/tidb/issues/52768) @[winoros](https://github.com/winoros)
    - 修复当一条 SQL 绑定涉及窗口函数时，有一定概率不生效的问题 [#55981](https://github.com/pingcap/tidb/issues/55981) @[winoros](https://github.com/winoros)
    - 修复解析索引数据时可能发生 panic 的问题 [#47115](https://github.com/pingcap/tidb/issues/47115) @[zyguan](https://github.com/zyguan)
    - 修复 TiDB 启动加载统计信息时可能因为 GC 推进报错的问题 [#53592](https://github.com/pingcap/tidb/issues/53592) @[you06](https://github.com/you06)
    - 修复 DML 语句中包含嵌套的生成列时报错的问题 [#53967](https://github.com/pingcap/tidb/issues/53967) @[wjhuang2016](https://github.com/wjhuang2016)
    - 修复执行谓词总是为 `true` 的 `SHOW ERRORS` 语句导致 TiDB panic 的问题 [#46962](https://github.com/pingcap/tidb/issues/46962) @[elsa0520](https://github.com/elsa0520)
    - 修复在某些情况下，元数据锁使用不当可能导致使用 plan cache 时写入异常数据的问题 [#53634](https://github.com/pingcap/tidb/issues/53634) @[zimulala](https://github.com/zimulala)
    - 修复添加索引时重试导致数据索引不一致的问题 [#55808](https://github.com/pingcap/tidb/issues/55808) @[lance6716](https://github.com/lance6716)
    - 修复 `UPDATE` 语句可能因为列的唯一 ID 不稳定导致查询报错的问题 [#53236](https://github.com/pingcap/tidb/issues/53236) @[winoros](https://github.com/winoros)
    - 修复在事务内的语句被 OOM 终止之后，如果在当前事务内继续执行下一条语句，可能报错 `Trying to start aggressive locking while it's already started` 并发生 panic 的问题 [#53540](https://github.com/pingcap/tidb/issues/53540) @[MyonKeminta](https://github.com/MyonKeminta)
    - 修复执行 `RECOVER TABLE BY JOB JOB_ID;` 可能导致 panic 的问题 [#55113](https://github.com/pingcap/tidb/issues/55113) @[crazycs520](https://github.com/crazycs520)
    - 修复分布式执行框架下，在 PD 修改成员后 `ADD INDEX` 可能失败的问题 [#48680](https://github.com/pingcap/tidb/issues/48680) @[lance6716](https://github.com/lance6716)
    - 修复可能同时存在两个 DDL Owner 的问题 [#54689](https://github.com/pingcap/tidb/issues/54689) @[joccau](https://github.com/joccau)
    - 修复 `ADD INDEX` 过程中 TiDB 滚动重启导致索引添加失败的问题 [#52805](https://github.com/pingcap/tidb/issues/52805) @[tangenta](https://github.com/tangenta)
    - 修复 `LOAD DATA ... REPLACE INTO` 导致的数据不一致问题 [#56408](https://github.com/pingcap/tidb/issues/56408) @[fzzf678](https://github.com/fzzf678)
    - 修复通过 `IMPORT INTO` 导入数据后，`AUTO_INCREMENT` 字段没有正确设置的问题 [#56476](https://github.com/pingcap/tidb/issues/56476) @[D3Hunter](https://github.com/D3Hunter)
    - 修复在从 checkpoint 恢复之前，没有检查是否存在本地文件的问题 [#53009](https://github.com/pingcap/tidb/issues/53009) @[lance6716](https://github.com/lance6716)
    - 修复 DM schema tracker 无法创建超过默认长度索引的问题 [#55138](https://github.com/pingcap/tidb/issues/55138) @[lance6716](https://github.com/lance6716)
    - 修复 `ALTER TABLE` 没有正确处理 `AUTO_INCREMENT` 字段的问题 [#47899](https://github.com/pingcap/tidb/issues/47899) @[D3Hunter](https://github.com/D3Hunter)
    - 修复未释放的会话资源可能导致的内存泄漏问题 [#56271](https://github.com/pingcap/tidb/issues/56271) @[lance6716](https://github.com/lance6716)
    - 修复浮点数或整数溢出影响计划缓存的问题 [#46538](https://github.com/pingcap/tidb/issues/46538) @[hawkingrei](https://github.com/hawkingrei)
    - 修复 `IndexLookUp` 算子部分内存未被追踪的问题 [#56440](https://github.com/pingcap/tidb/issues/56440) @[wshwsh12](https://github.com/wshwsh12)
    - 修复由于 stale read 未对读操作的时间戳进行严格校验，导致 TSO 和真实物理时间存在偏移，有小概率影响事务一致性的问题 [#56809](https://github.com/pingcap/tidb/issues/56809) @[MyonKeminta](https://github.com/MyonKeminta)
    - 修复 TTL 在未选用 TiKV 作为存储引擎时可能失败的问题 [#56402](https://github.com/pingcap/tidb/issues/56402) @[YangKeao](https://github.com/YangKeao)
    - 修复写冲突时 TTL 任务可能无法取消的问题 [#56422](https://github.com/pingcap/tidb/issues/56422) @[YangKeao](https://github.com/YangKeao)
    - 修复插入科学计数法形式的超大数字时报错 `ERROR 1264 (22003)` 的问题，使其行为与 MySQL 保持一致 [#47787](https://github.com/pingcap/tidb/issues/47787) @[lcwangchao](https://github.com/lcwangchao)
    - 修复取消 TTL 任务时，没有强制 Kill 对应 SQL 的问题 [#56511](https://github.com/pingcap/tidb/issues/56511) @[lcwangchao](https://github.com/lcwangchao)
    - 修复 `INSERT ... ON DUPLICATE KEY` 语句不兼容 `mysql_insert_id` 的问题 [#55965](https://github.com/pingcap/tidb/issues/55965) @[tiancaiamao](https://github.com/tiancaiamao)
    - 修复 SQL 无法构建执行计划时，审计日志过滤不生效的问题 [#50988](https://github.com/pingcap/tidb/issues/50988) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - 修复集群从 v6.5 升级到 v7.5 或更高版本后，已有 TTL 任务执行意外频繁的问题 [#56539](https://github.com/pingcap/tidb/issues/56539) @[lcwangchao](https://github.com/lcwangchao)
    - 修复由于 `CAST` 函数不支持显式设置字符集导致报错的问题 [#55677](https://github.com/pingcap/tidb/issues/55677) @[Defined2014](https://github.com/Defined2014)
    - 修复执行 `ADD INDEX` 时，未检查索引长度限制的问题 [#56930](https://github.com/pingcap/tidb/issues/56930) @[fzzf678](https://github.com/fzzf678)

+ TiKV

    - 新增 `RawKvMaxTimestampNotSynced` 报错，并在 `errorpb.Error.max_ts_not_synced` 中记录该报错的详细信息。针对 `must_raw_put` 操作，在遇到该错误时增加了重试机制 [#16789](https://github.com/tikv/tikv/issues/16789) @[pingyu](https://github.com/pingyu)
    - 修复删除大表或分区后可能导致的流量控制问题 [#17304](https://github.com/tikv/tikv/issues/17304) @[SpadeA-Tang](https://github.com/SpadeA-Tang)
    - 修复读线程在从 Raft Engine 中的 MemTable 读取过时索引时出现的 panic 问题 [#17383](https://github.com/tikv/tikv/issues/17383) @[LykxSassinator](https://github.com/LykxSassinator)
    - 修复 `advance-ts-interval` 配置未被用于限制 CDC 和 log-backup 模块中 `check_leader` 操作的 timeout，导致在某些情况下 TiKV 正常重启时 `resolved_ts` lag 过大的问题 [#17107](https://github.com/tikv/tikv/issues/17107) @[SpadeA-Tang](https://github.com/SpadeA-Tang)
    - 修复重启 TiKV 后由 TiDB Lightning 导入的 SST 文件丢失的问题 [#15912](https://github.com/tikv/tikv/issues/15912) @[lance6716](https://github.com/lance6716)
    - 修复 ingest 已被删除的 sst_importer SST 文件导致 TiKV panic 的问题 [#15053](https://github.com/tikv/tikv/issues/15053) @[lance6716](https://github.com/lance6716)
    - 修复当 TiKV 实例中有大量 Region 时，数据导入过程中可能出现 OOM 的问题 [#16229](https://github.com/tikv/tikv/issues/16229) @[SpadeA-Tang](https://github.com/SpadeA-Tang)
    - 修复早期版本（早于 v7.1）和之后的版本的 bloom filter 无法兼容的问题 [#17272](https://github.com/tikv/tikv/issues/17272) @[v01dstar](https://github.com/v01dstar)
    - 修复设置 gRPC 消息的压缩算法 (`grpc-compression-type`) 对 TiKV 发送到 TiDB 的消息不起作用的问题 [#17176](https://github.com/tikv/tikv/issues/17176) @[ekexium](https://github.com/ekexium)
    - 修复测试用例不稳定的问题，确保每次测试都使用独立的临时目录，从而避免在线配置更改影响其他测试用例 [#16871](https://github.com/tikv/tikv/issues/16871) @[glorv](https://github.com/glorv)
    - 修复当大量事务在排队等待同一个 key 上的锁被释放且该 key 被频繁更新时，TiKV 可能因死锁检测压力过大而出现 OOM 的问题 [#17394](https://github.com/tikv/tikv/issues/17394) @[MyonKeminta](https://github.com/MyonKeminta)
    - 修复 `DECIMAL` 类型的小数部分在某些情况下不正确的问题 [#16913](https://github.com/tikv/tikv/issues/16913) @[gengliqi](https://github.com/gengliqi)
    - 修复查询中 `CONV()` 函数在进行数制转换时可能 overflow 导致 TiKV panic 的问题 [#16969](https://github.com/tikv/tikv/issues/16969) @[gengliqi](https://github.com/gengliqi)
    - 修复过期副本处理 Raft 快照时，由于分裂操作过慢并且随后立即删除新副本，可能导致 TiKV panic 的问题 [#17469](https://github.com/tikv/tikv/issues/17469) @[hbisheng](https://github.com/hbisheng)
    - 修复高并发的 Coprocessor 请求可能导致 TiKV OOM 的问题 [#16653](https://github.com/tikv/tikv/issues/16653) @[overvenus](https://github.com/overvenus)
    - 修复当主密钥存储于 KMS (Key Management Service) 时无法轮换主密钥的问题 [#17410](https://github.com/tikv/tikv/issues/17410) @[hhwyt](https://github.com/hhwyt)
    - 修复 tikv-ctl 的 `raft region` 命令的输出中未包含 Region 状态信息的问题 [#17037](https://github.com/tikv/tikv/issues/17037) @[glorv](https://github.com/glorv)
    - 修复 Grafana 上 TiKV 面板的 **Storage async write duration** 监控指标不准确的问题 [#17579](https://github.com/tikv/tikv/issues/17579) @[overvenus](https://github.com/overvenus)
    - 修复巴西和埃及时区转换错误的问题 [#16220](https://github.com/tikv/tikv/issues/16220) @[overvenus](https://github.com/overvenus)

+ PD

    - 修复 label 统计中的内存泄露问题 [#8700](https://github.com/tikv/pd/issues/8700) @[lhy1024](https://github.com/lhy1024)
    - 修复资源组 (Resource Group) 打印过多日志的问题 [#8159](https://github.com/tikv/pd/issues/8159) @[nolouch](https://github.com/nolouch)
    - 修复频繁创建随机数生成器导致性能抖动的问题 [#8674](https://github.com/tikv/pd/issues/8674) @[rleungx](https://github.com/rleungx)
    - 修复 Region 统计中的内存泄露问题 [#8710](https://github.com/tikv/pd/issues/8710) @[rleungx](https://github.com/rleungx)
    - 修复热点缓存中可能存在的内存泄露问题 [#8698](https://github.com/tikv/pd/issues/8698) @[lhy1024](https://github.com/lhy1024)
    - 修复 `evict-leader-scheduler` 在使用相同 Store ID 重复创建后无法正常工作的问题 [#8756](https://github.com/tikv/pd/issues/8756) @[okJiang](https://github.com/okJiang)
    - 修复设置 `replication.strictly-match-label` 为 `true` 导致 TiFlash 启动失败的问题 [#8480](https://github.com/tikv/pd/issues/8480) @[rleungx](https://github.com/rleungx)
    - 修复通过配置文件更改日志级别不生效的问题 [#8117](https://github.com/tikv/pd/issues/8117) @[rleungx](https://github.com/rleungx)
    - 修复资源组 (Resource Group) 在高并发场景下无法有效限制资源使用的问题 [#8435](https://github.com/tikv/pd/issues/8435) @[nolouch](https://github.com/nolouch)
    - 修复 PD 在进行 operator 检查时遇到的数据竞争问题 [#8263](https://github.com/tikv/pd/issues/8263) @[lhy1024](https://github.com/lhy1024)
    - 修复资源组在请求 token 超过 500 ms 时遇到超出配额限制的问题 [#8349](https://github.com/tikv/pd/issues/8349) @[nolouch](https://github.com/nolouch)
    - 修复部分日志未脱敏的问题 [#8419](https://github.com/tikv/pd/issues/8419) @[rleungx](https://github.com/rleungx)
    - 修复将角色 (role) 绑定到资源组时未报错的问题 [#54417](https://github.com/pingcap/tidb/issues/54417) @[JmPotato](https://github.com/JmPotato)
    - 修复存在大量 Region 时，无法请求 PD 的 Region API 的问题 [#55872](https://github.com/pingcap/tidb/issues/55872) @[rleungx](https://github.com/rleungx)
    - 修复取消资源组查询导致大量重试的问题 [#8217](https://github.com/tikv/pd/issues/8217) @[nolouch](https://github.com/nolouch)
    - 修复加密管理器在使用前未初始化的问题 [#8384](https://github.com/tikv/pd/issues/8384) @[rleungx](https://github.com/rleungx)
    - 修复 PD 的 `Filter target` 监控指标未提供 scatter range 信息的问题 [#8125](https://github.com/tikv/pd/issues/8125) @[HuSharp](https://github.com/HuSharp)
    - 修复资源组遇到的数据竞争问题 [#8267](https://github.com/tikv/pd/issues/8267) @[HuSharp](https://github.com/HuSharp)
    - 修复将 TiKV 配置项 [`coprocessor.region-split-size`](/tikv-configuration-file.md#region-split-size) 设置为小于 1 MiB 的值会导致 PD panic 的问题 [#8323](https://github.com/tikv/pd/issues/8323) @[JmPotato](https://github.com/JmPotato)
    - 修复在 `evict-leader-scheduler` 中使用了错误的参数后，PD 不能正确报错且导致部分 scheduler 不可用的问题 [#8619](https://github.com/tikv/pd/issues/8619) @[rleungx](https://github.com/rleungx)
    - 修复资源组 (Resource Group) 客户端中未完全删除的 slot 导致分配 token 低于给定值的问题 [#7346](https://github.com/tikv/pd/issues/7346) @[guo-shaoge](https://github.com/guo-shaoge)
    - 修复使用 Placement Rules 的情况下，down peer 可能无法恢复的问题 [#7808](https://github.com/tikv/pd/issues/7808) @[rleungx](https://github.com/rleungx)

+ TiFlash

    - 修复从低于 v6.5.0 的集群升级到 v6.5.0 及以上版本后，可能出现 TiFlash 元数据损坏以及进程 panic 的问题 [#9039](https://github.com/pingcap/tiflash/issues/9039) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复开启延迟物化后，部分查询在执行时可能报列类型不匹配错误的问题 [#9175](https://github.com/pingcap/tiflash/issues/9175) @[JinheLin](https://github.com/JinheLin)
    - 修复开启延迟物化后，部分查询可能报错的问题 [#9472](https://github.com/pingcap/tiflash/issues/9472) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - 修复一些 TiFlash 不支持的 JSON 函数被错误地下推到 TiFlash 的问题 [#9444](https://github.com/pingcap/tiflash/issues/9444) @[windtalker](https://github.com/windtalker)
    - 修复将 TiFlash 中 SSL 证书配置项设置为空字符串会错误开启 TLS 并导致 TiFlash 启动失败的问题 [#9235](https://github.com/pingcap/tiflash/issues/9235) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复 TiFlash 与任意 PD 之间发生网络分区（即网络连接断开），可能导致读请求超时报错的问题 [#9243](https://github.com/pingcap/tiflash/issues/9243) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - 修复通过 BR 或 TiDB Lightning 导入数据后，FastScan 模式下可能读到大量重复行数据的问题 [#9118](https://github.com/pingcap/tiflash/issues/9118) @[JinheLin](https://github.com/JinheLin)
    - 修复当表里含 Bit 类型列并且带有表示非法字符的默认值时，TiFlash 无法解析表 schema 的问题 [#9461](https://github.com/pingcap/tiflash/issues/9461) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - 修复开启延迟物化后，带有虚拟生成列的查询可能返回错误结果的问题 [#9188](https://github.com/pingcap/tiflash/issues/9188) @[JinheLin](https://github.com/JinheLin)
    - 修复跨数据库执行 `ALTER TABLE ... EXCHANGE PARTITION` 后可能导致 TiFlash 同步 schema 失败的问题 [#7296](https://github.com/pingcap/tiflash/issues/7296) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复数据库创建后短时间内被删除时，TiFlash 可能 panic 的问题 [#9266](https://github.com/pingcap/tiflash/issues/9266) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复使用 `CAST()` 函数将字符串转换为带时区或非法字符的日期时间时，结果错误的问题 [#8754](https://github.com/pingcap/tiflash/issues/8754) @[solotzg](https://github.com/solotzg)
    - 修复 TiFlash 在高并发读的情况下，可能返回瞬时不正确结果的问题 [#8845](https://github.com/pingcap/tiflash/issues/8845) @[JinheLin](https://github.com/JinheLin)
    - 修复函数 `SUBSTRING_INDEX()` 可能导致 TiFlash Crash 的问题 [#9116](https://github.com/pingcap/tiflash/issues/9116) @[wshwsh12](https://github.com/wshwsh12)
    - 修复当集群中长时间频繁执行 `EXCHANGE PARTITION` 和 `DROP TABLE` 操作时，可能导致 TiFlash 表元信息同步缓慢以及查询性能下降的问题 [#9227](https://github.com/pingcap/tiflash/issues/9227) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复 key range 为空的查询导致 TiFlash 上没有正确生成读取任务，从而可能阻塞 TiFlash 查询的问题 [#9108](https://github.com/pingcap/tiflash/issues/9108) @[JinheLin](https://github.com/JinheLin)
    - 修复在特定情况下 `CAST AS DECIMAL` 函数的返回结果存在正负号错误的问题 [#9301](https://github.com/pingcap/tiflash/issues/9301) @[guo-shaoge](https://github.com/guo-shaoge)
    - 修复 `SUBSTRING()` 函数不支持部分整数类型的 `pos` 和 `len` 参数导致查询报错的问题 [#9473](https://github.com/pingcap/tiflash/issues/9473) @[gengliqi](https://github.com/gengliqi)
    - 修复对大表执行 `DROP TABLE` 可能导致 TiFlash OOM 的问题 [#9437](https://github.com/pingcap/tiflash/issues/9437) @[JaySon-Huang](https://github.com/JaySon-Huang)

+ Tools

    + Backup & Restore (BR)

        - 修复 BR 集成测试用例不稳定的问题，并新增用于模拟快照或者日志备份文件损坏的测试用例 [#53835](https://github.com/pingcap/tidb/issues/53835) @[Leavrth](https://github.com/Leavrth)
        - 修复增量恢复过程中 `ADD INDEX`、`MODIFY COLUMN` 等需要回填的 DDL 可能无法正确恢复的问题 [#54426](https://github.com/pingcap/tidb/issues/54426) @[3pointer](https://github.com/3pointer)
        - 修复当 PITR 日志备份任务失败时，用户停止了该任务后，PD 中与该任务相关的 safepoint 未被正确清除的问题 [#17316](https://github.com/tikv/tikv/issues/17316) @[Leavrth](https://github.com/Leavrth)
        - 修复日志备份在 advancer owner 发生迁移后可能被暂停的问题 [#53561](https://github.com/pingcap/tidb/issues/53561) @[RidRisR](https://github.com/RidRisR)
        - 修复增量备份过程中扫描 DDL 作业的效率较低的问题 [#54139](https://github.com/pingcap/tidb/issues/54139) @[3pointer](https://github.com/3pointer)
        - 修复断点备份过程中查找 Region leader 中断导致备份性能受影响问题 [#17168](https://github.com/tikv/tikv/issues/17168) @[Leavrth](https://github.com/Leavrth)
        - 修复开启日志备份时，BR 日志可能打印权限凭证敏感信息的问题 [#55273](https://github.com/pingcap/tidb/issues/55273) @[RidRisR](https://github.com/RidRisR)
        - 修复在恢复过程中，由于多层重试导致 BR 无法正确识别错误的问题 [#54053](https://github.com/pingcap/tidb/issues/54053) @[RidRisR](https://github.com/RidRisR)
        - 修复恢复暂停的日志备份任务时，如果与 PD 的网络连接不稳定可能导致 TiKV panic 的问题 [#17020](https://github.com/tikv/tikv/issues/17020) @[YuJuncen](https://github.com/YuJuncen)
        - 修复备份过程中由于 TiKV 没有响应导致备份任务无法结束的问题 [#53480](https://github.com/pingcap/tidb/issues/53480) @[Leavrth](https://github.com/Leavrth)
        - 修复备份恢复的断点路径在一些外部存储中不兼容的问题 [#55265](https://github.com/pingcap/tidb/issues/55265) @[Leavrth](https://github.com/Leavrth)
        - 修复在 BR 恢复数据或 TiDB Lightning 物理导入模式下导入数据时，从 PD 获取到的 Region 没有 Leader 的问题 [#51124](https://github.com/pingcap/tidb/issues/51124) [#50501](https://github.com/pingcap/tidb/issues/50501) @[Leavrth](https://github.com/Leavrth)
        - 修复 PD leader 发生迁移可能导致恢复数据时 panic 的问题 [#53724](https://github.com/pingcap/tidb/issues/53724) @[Leavrth](https://github.com/Leavrth)
        - 修复日志备份在暂停、停止、再重建任务操作后，虽然任务状态显示正常，但 Checkpoint 不推进的问题 [#53047](https://github.com/pingcap/tidb/issues/53047) @[RidRisR](https://github.com/RidRisR)
        - 修复日志备份不能及时解决残留锁导致 Checkpoint 无法推进的问题 [#57134](https://github.com/pingcap/tidb/issues/57134) @[3pointer](https://github.com/3pointer)

    + TiCDC

        - 修复 `TIMEZONE` 类型的值没有按照正确的时区设置默认值的问题 [#10931](https://github.com/pingcap/tiflow/issues/10931) @[3AceShowHand](https://github.com/3AceShowHand)
        - 修复 Sorter 模块读取磁盘数据时 TiCDC 可能 Panic 的问题 [#10853](https://github.com/pingcap/tiflow/issues/10853) @[hicqu](https://github.com/hicqu)
        - 修复在多节点环境下进行大量 `UPDATE` 操作时，反复重启 Changefeed 可能导致的数据不一致问题 [#11219](https://github.com/pingcap/tiflow/issues/11219) @[lidezhu](https://github.com/lidezhu)
        - 修复在 `ignore-event` 中设置了过滤掉 `add table partition` 事件后，TiCDC 未将相关分区的其它类型 DML 变更事件同步到下游的问题 [#10524](https://github.com/pingcap/tiflow/issues/10524) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - 修复同步数据到 Kafka 时可能卡住的问题 [#9855](https://github.com/pingcap/tiflow/issues/9855) @[hicqu](https://github.com/hicqu)
        - 修复没有正确同步 `DROP PRIMARY KEY` 和 `DROP UNIQUE KEY` 的问题 [#10890](https://github.com/pingcap/tiflow/issues/10890) @[asddongmen](https://github.com/asddongmen)
        - 修复当下游 Kafka 无法访问时，Processor 模块可能卡住的问题 [#11340](https://github.com/pingcap/tiflow/issues/11340) @[asddongmen](https://github.com/asddongmen)

    + TiDB Data Migration (DM)

        - 修复 DM 在处理 `ALTER DATABASE` 语句时未设置默认数据库导致同步报错的问题 [#11503](https://github.com/pingcap/tiflow/issues/11503) @[lance6716](https://github.com/lance6716)
        - 修复多个 DM-master 节点可能同时成为 Leader 导致数据不一致的问题 [#11602](https://github.com/pingcap/tiflow/issues/11602) @[GMHDBJD](https://github.com/GMHDBJD)
        - 升级 `go-mysql` 以修复连接阻塞的问题 [#11041](https://github.com/pingcap/tiflow/issues/11041) @[D3Hunter](https://github.com/D3Hunter)
        - 修复当索引长度超过 `max-index-length` 默认值时数据同步中断的问题 [#11459](https://github.com/pingcap/tiflow/issues/11459) @[michaelmdeng](https://github.com/michaelmdeng)
        - 修复 DM 在同步针对 LIST 分区表的 `ALTER TABLE ... DROP PARTITION` 语句时报错的问题 [#54760](https://github.com/pingcap/tidb/issues/54760) @[lance6716](https://github.com/lance6716)

    + TiDB Lightning

        - 修复 TiDB Lightning 因 TiKV 发送的消息过大而接收失败的问题 [#56114](https://github.com/pingcap/tidb/issues/56114) @[fishiu](https://github.com/fishiu)
        - 修复在关闭 TiDB Lightning 的导入模式后进行数据导入时，TiKV 数据可能损坏的问题 [#15003](https://github.com/tikv/tikv/issues/15003) [#47694](https://github.com/pingcap/tidb/issues/47694) @[lance6716](https://github.com/lance6716)
        - 修复使用 TiDB Lightning 导入数据时报事务冲突的问题 [#49826](https://github.com/pingcap/tidb/issues/49826) @[lance6716](https://github.com/lance6716)
        - 修复 EBS BR 运行时 TiDB Lightning 可能导入失败的问题 [#49517](https://github.com/pingcap/tidb/issues/49517) @[mittalrishabh](https://github.com/mittalrishabh)
        - 修复两个实例同时并行开始导入任务时，由于分配到的任务 ID 相同导致 TiDB Lightning 报 `verify allocator base failed` 错误的问题 [#55384](https://github.com/pingcap/tidb/issues/55384) @[ei-sugimoto](https://github.com/ei-sugimoto)
        - 修复 TiDB Lightning 导入数据时，kill PD Leader 会导致 `invalid store ID 0` 报错的问题 [#50501](https://github.com/pingcap/tidb/issues/50501) @[Leavrth](https://github.com/Leavrth)

    + Dumpling

        - 修复 Dumpling 在同时导出表和视图时报错的问题 [#53682](https://github.com/pingcap/tidb/issues/53682) @[tangenta](https://github.com/tangenta)

    + TiDB Binlog
    
        - 修复开启 TiDB Binlog 后，在 `ADD COLUMN` 执行过程中删除行可能报错 `data and columnID count not match` 的问题 [#53133](https://github.com/pingcap/tidb/issues/53133) @[tangenta](https://github.com/tangenta)
