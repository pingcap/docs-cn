---
title: TiDB 8.1.1 Release Notes
summary: 了解 TiDB 8.1.1 版本的兼容性变更、改进提升，以及错误修复。
---

# TiDB 8.1.1 Release Notes

发版日期：2024 年 8 月 xx 日

TiDB 版本：8.1.1

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v8.1/quick-start-with-tidb) | [生产部署](https://docs.pingcap.com/zh/tidb/v8.1/production-deployment-using-tiup) | [下载离线包](https://cn.pingcap.com/product-community/?version=v8.1.1#version-list)

## 兼容性变更

- 使用 TiDB Lightning 导入 CSV 文件时，如果设置了严格格式 `strict-format = true` 将一个大 CSV 文件切分为多个小 CSV 文件来提升并发和导入性能，需要显式指定行结束符 `terminator`，参数的取值为 `\r`、`\n` 或 `\r\n`。如果没有指定行结束符，可能导致 CSV 文件数据解析异常。 [#37338](https://github.com/pingcap/tidb/issues/37338) @[lance6716](https://github.com/lance6716)
- 使用 [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md) 导入 CSV 文件时，如果指定 `SPLIT_FILE` 参数将一个大 CSV 文件切分为多个小 CSV 文件来提升并发和导入性能，需显式指定行结束符 `LINES_TERMINATED_BY`，参数的取值为 `\r`、`\n` 或 `\r\n`。如果没有指定行结束符，可能导致 CSV 文件数据解析异常。[#37338](https://github.com/pingcap/tidb/issues/37338) @[lance6716](https://github.com/lance6716)

## 改进提升

+ TiDB

    - 通过批量删除 TiFlash placement rule 的方式，提升对分区表执行 `TRUNCATE`、`DROP` 后数据 GC 的处理速度 [#54068](https://github.com/pingcap/tidb/issues/54068) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - 在 MPP 负载均衡时移除不包含任何 Region 的 Store [#52313](https://github.com/pingcap/tidb/issues/52313) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - 将统计信息同步加载任务的优先级暂时调整为 `High`，避免在 TiKV 高负载时同步加载任务大面积超时，从而导致统计信息无法加载 [#50332](https://github.com/pingcap/tidb/issues/50332) @[winoros](https://github.com/winoros)

+ PD

    - 改进 HTTP client 的重试逻辑 [#8142](https://github.com/tikv/pd/issues/8142) @[JmPotato](https://github.com/JmPotato)

+ TiFlash

    - 降低 TiFlash 在开启 TLS 后因更新证书而导致 panic 的概率 [#8535](https://github.com/pingcap/tiflash/issues/8535) @[windtalker](https://github.com/windtalker)
    - 减少数据高并发读取下的锁冲突，优化短查询性能 [#9125](https://github.com/pingcap/tiflash/issues/9125) @[JinheLin](https://github.com/JinheLin)

+ Tools

    + Backup & Restore (BR)

        - 支持对日志备份过程中生成的临时文件进行加密 [#15083](https://github.com/tikv/tikv/issues/15083) @[YuJuncen](https://github.com/YuJuncen)
        - 去掉除了 `br log restore` 子命令之外其它 `br log` 子命令对 TiDB `domain` 数据结构的载入，降低内存消耗 [#52088](https://github.com/pingcap/tidb/issues/52088) @[Leavrth](https://github.com/Leavrth)
        - 支持通过环境变量设置阿里云访问身份 [#45551](https://github.com/pingcap/tidb/issues/45551) @[RidRisR](https://github.com/RidRisR)
        - 在 TiKV 下载每个 SST 文件之前，新增对 TiKV 是否有足够磁盘空间的检查；如果空间不足，BR 会终止恢复并返回错误 [#17224](https://github.com/tikv/tikv/issues/17224) @[RidRisR](https://github.com/RidRisR)

    + TiCDC

        - 支持使用 Simple Protocol 的 changefeed 在启动时将所有表的 BOOTSTRAP 消息一次性发送到下游 [#11315](https://github.com/pingcap/tiflow/issues/11315) @[asddongmen](https://github.com/asddongmen)
        - 支持当下游为消息队列 (Message Queue, MQ) 或存储服务时直接输出原始事件 [#11211](https://github.com/pingcap/tiflow/issues/11211) @[CharlesCheung96](https://github.com/CharlesCheung96)

## 错误修复

+ TiDB

    - 修复当 SQL 异常中断时，`INDEX_HASH_JOIN` 无法正常退出的问题 [#54688](https://github.com/pingcap/tidb/issues/54688) @[wshwsh12](https://github.com/wshwsh12)
    - 修复可以创建非严格自增的 RANGE 分区表的问题 [#54829](https://github.com/pingcap/tidb/issues/54829) @[Defined2014](https://github.com/Defined2014)
    - 修复可以生成 `_tidb_rowid` 的点查 (`PointGet`) 执行计划的问题 [#54583](https://github.com/pingcap/tidb/issues/54583) @[Defined2014](https://github.com/Defined2014)
    - 修复慢日志中内部语句中的 SQL 默认被脱敏为空的问题 [#54190](https://github.com/pingcap/tidb/issues/54190) [#52743](https://github.com/pingcap/tidb/issues/52743) [#53264](https://github.com/pingcap/tidb/issues/53264) @[lcwangchao](https://github.com/lcwangchao)
    - 修复 `UPDATE` 操作在多表场景下导致 TiDB OOM 的问题 [#53742](https://github.com/pingcap/tidb/issues/53742) @[hawkingrei](https://github.com/hawkingrei)
    - 修复窗口函数中有某些子查询时可能会 panic 的问题 [#42734](https://github.com/pingcap/tidb/issues/42734) @[hi-rustin](https://github.com/hi-rustin)
    - 修复当排序规则为 `utf8_bin` 或 `utf8mb4_bin` 时意外消除 `LENGTH()` 条件的错误 [#53730](https://github.com/pingcap/tidb/issues/53730) @[elsa0520](https://github.com/elsa0520)
    - 修复在事务内的语句被 OOM 终止之后，如果在当前事务内继续执行下一条语句，可能报错 `Trying to start aggressive locking while it's already started` 并发生 panic 的问题 [#53540](https://github.com/pingcap/tidb/issues/53540) @[MyonKeminta](https://github.com/MyonKeminta)
    - 修复使用 `PREPARE`/`EXECUTE` 方式执行带 `CONV` 表达式的语句，且 `CONV` 表达式包含 `?` 参数时，多次执行可能导致查询结果错误的问题 [#53505](https://github.com/pingcap/tidb/issues/53505) @[qw4990](https://github.com/qw4990)
    - 修复递归的 CTE 算子错误地跟踪内存使用的问题 [#54181](https://github.com/pingcap/tidb/issues/54181) @[guo-shaoge](https://github.com/guo-shaoge)
    - 修复使用 `SHOW WARNINGS;` 获取警告时可能导致 panic 的问题 [#48756](https://github.com/pingcap/tidb/issues/48756) @[xhebox](https://github.com/xhebox)
    - 修复 TopN 算子可能被错误地下推的问题 [#37986](https://github.com/pingcap/tidb/issues/37986) @[qw4990](https://github.com/qw4990)
    - 修复执行谓词总是为 `true` 的 `SHOW ERRORS` 语句导致 TiDB panic 的问题 [#46962](https://github.com/pingcap/tidb/issues/46962) @[elsa0520](https://github.com/elsa0520)
    - 修复 `INFORMATION_SCHEMA.TIDB_TRX` 表中 `STATE` 字段的 `size` 未定义导致 `STATE` 显示为空的问题 [#53026](https://github.com/pingcap/tidb/issues/53026) @[cfzjywxk](https://github.com/cfzjywxk)
    - 修复执行 `SELECT DISTINCT CAST(col AS DECIMAL), CAST(col AS SIGNED) FROM ...` 查询时结果出错的问题 [#53726](https://github.com/pingcap/tidb/issues/53726) @[hawkingrei](https://github.com/hawkingrei)
    - 修复 DDL 错误使用 etcd 导致任务排队的问题 [#52335](https://github.com/pingcap/tidb/issues/52335) @[wjhuang2016](https://github.com/wjhuang2016)
    - 修复 GlobalStats 中的 `Distinct_count` 信息可能错误的问题 [#53752](https://github.com/pingcap/tidb/issues/53752) @[hawkingrei](https://github.com/hawkingrei)
    - 修复在自动收集统计信息时，系统变量 `tidb_enable_async_merge_global_stats` 和 `tidb_analyze_partition_concurrency` 未生效的问题 [#53972](https://github.com/pingcap/tidb/issues/53972) @[hi-rustin](https://github.com/hi-rustin)
    - 修复当第一个参数是 `month` 并且第二个参数是负数时，`TIMESTAMPADD()` 函数会进入无限循环的问题 [#54908](https://github.com/pingcap/tidb/issues/54908) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - 修复某些连接在握手完成之前退出导致 Grafana 监控指标中的连接数 (Connection Count) 不正确的问题 [#54428](https://github.com/pingcap/tidb/issues/54428) @[YangKeao](https://github.com/YangKeao)
    - 修复使用 TiProxy 和资源组 (Resource Group) 功能时，每个资源组的连接数 (Connection Count) 显示不正确的问题 [#54545](https://github.com/pingcap/tidb/issues/54545) @[YangKeao](https://github.com/YangKeao)
    - 修复在递归 CTE 中无法使用视图的问题 [#49721](https://github.com/pingcap/tidb/issues/49721) @[hawkingrei](https://github.com/hawkingrei)
    - 修复 Massively Parallel Processing (MPP) 中 `final` AggMode 和 `non-final` AggMode 无法共存的问题 [#51362](https://github.com/pingcap/tidb/issues/51362) @[AilinKid](https://github.com/AilinKid)
    - 修复使用 Optimizer Hints 时，可能输出错误的 WARNINGS 信息的问题 [#53767](https://github.com/pingcap/tidb/issues/53767) @[hawkingrei](https://github.com/hawkingrei)
    - 修复在 `HashJoin` 或 `IndexLookUp` 算子作为 `Apply` 算子的被驱动侧子节点时，由于 `memTracker` 未被析构而导致的内存异常高的问题 [#54005](https://github.com/pingcap/tidb/issues/54005) @[XuHuaiyu](https://github.com/XuHuaiyu)
    - 修复某些情况下可以创建非法的 `DECIMAL(0,0)` 列类型的问题 [#53779](https://github.com/pingcap/tidb/issues/53779) @[tangenta](https://github.com/tangenta)
    - 修复在 `(*PointGetPlan).StatsInfo()` 执行过程中可能遇到数据竞争的问题 [#49803](https://github.com/pingcap/tidb/issues/49803) [#43339](https://github.com/pingcap/tidb/issues/43339) @[qw4990](https://github.com/qw4990)
    - 修复在某些情况下，元数据锁使用不当可能导致使用 plan cache 时写入异常数据的问题 [#53634](https://github.com/pingcap/tidb/issues/53634) @[zimulala](https://github.com/zimulala)
    - 修复 JSON 相关函数在某些情况下报错信息与 MySQL 不一致的问题 [#53799](https://github.com/pingcap/tidb/issues/53799) @[dveeden](https://github.com/dveeden)
    - 修复创建带有外键的表时，TiDB 未创建对应的统计信息元信息 (`stats_meta`) 的问题 [#53652](https://github.com/pingcap/tidb/issues/53652) @[hawkingrei](https://github.com/hawkingrei)
    - 修复 `memory_quota` Hint 在子查询中可能不生效的问题 [#53834](https://github.com/pingcap/tidb/issues/53834) @[qw4990](https://github.com/qw4990)
    - 修复 TiDB 启动加载统计信息时可能因为 GC 推进报错的问题 [#53592](https://github.com/pingcap/tidb/issues/53592) @[you06](https://github.com/you06)
    - 修复并发执行 `CREATE OR REPLACE VIEW` 可能报错 `table doesn't exist` 的问题 [#53673](https://github.com/pingcap/tidb/issues/53673) @[tangenta](https://github.com/tangenta)
    - 修复 information schema 缓存未命中导致 stale read 查询延迟上升的问题 [#53428](https://github.com/pingcap/tidb/issues/53428) @[crazycs520](https://github.com/crazycs520)
    - 修复在聚簇索引作为谓词时 `SELECT INTO OUTFILE` 不生效的问题 [#42093](https://github.com/pingcap/tidb/issues/42093) @[qw4990](https://github.com/qw4990)
    - 修复 `YEAR` 类型的列与超出范围的无符号整数进行比较导致错误结果的问题 [#50235](https://github.com/pingcap/tidb/issues/50235) @[qw4990](https://github.com/qw4990)
    - 修复在包含数据修改操作的事务中查询带有虚拟列的表时，查询结果可能错误的问题 [#53951](https://github.com/pingcap/tidb/issues/53951) @[qw4990](https://github.com/qw4990)
    - 修复使用 `auth_socket` 认证插件时，TiDB 在某些情况下未能拒绝不符合身份认证的用户连接的问题 [#54031](https://github.com/pingcap/tidb/issues/54031) @[lcwangchao](https://github.com/lcwangchao)
    - 修复当查询包含非关联子查询和 `LIMIT` 子句时，列剪裁可能不完善导致计划不优的问题 [#54213](https://github.com/pingcap/tidb/issues/54213) @[qw4990](https://github.com/qw4990)
    - 修复将数据从 `FLOAT` 类型转换为 `UNSIGNED` 类型时结果错误的问题 [#41736](https://github.com/pingcap/tidb/issues/41736) @[guo-shaoge](https://github.com/guo-shaoge)
    - 修复通过分布式执行框架添加索引时，设置 `max-index-length` 导致 TiDB panic 的问题 [#53281](https://github.com/pingcap/tidb/issues/53281) @[zimulala](https://github.com/zimulala)
    - 修复查询中的某些过滤条件可能导致 planner 模块发生 `invalid memory address or nil pointer dereference` 报错的问题 [#53582](https://github.com/pingcap/tidb/issues/53582) [#53580](https://github.com/pingcap/tidb/issues/53580) [#53594](https://github.com/pingcap/tidb/issues/53594) [#53603](https://github.com/pingcap/tidb/issues/53603) @[YangKeao](https://github.com/YangKeao)
    - 修复递归 CTE 查询可能导致无效指针的问题 [#54449](https://github.com/pingcap/tidb/issues/54449) @[hawkingrei](https://github.com/hawkingrei)
    - 修复 `Longlong` 类型在谓词中溢出的问题 [#45783](https://github.com/pingcap/tidb/issues/45783) @[hawkingrei](https://github.com/hawkingrei)
    - 修复在 `GROUP BY` 语句中引用间接占位符 `?` 无法找到列的问题 [#53872](https://github.com/pingcap/tidb/issues/53872) @[qw4990](https://github.com/qw4990)
    - 修复事务占用的内存可能被多次重复统计的问题 [#53984](https://github.com/pingcap/tidb/issues/53984) @[ekexium](https://github.com/ekexium)
    - 修复使用 `CURRENT_DATE()` 作为列默认值时查询结果错误的问题 [#53746](https://github.com/pingcap/tidb/issues/53746) @[tangenta](https://github.com/tangenta)
    - 修复使用全局排序添加索引时性能不稳定的问题 [#54147](https://github.com/pingcap/tidb/issues/54147) @[tangenta](https://github.com/tangenta)
    - 修复从 v7.1 升级后 `SHOW IMPORT JOBS` 报错 `Unknown column 'summary'` 的问题 [#54241](https://github.com/pingcap/tidb/issues/54241) @[tangenta](https://github.com/tangenta)
    - 修复 `root` 用户无法查询 `tidb_mdl_view` 的问题 [#53292](https://github.com/pingcap/tidb/issues/53292) @[tangenta](https://github.com/tangenta)
    - 修复使用分布式框架添加索引期间出现网络分区可能导致数据索引不一致的问题 [#54897](https://github.com/pingcap/tidb/issues/54897) @[tangenta](https://github.com/tangenta)
    - 修复 TiDB Lightning 物理导入模式初始化期间报错可能导致资源泄露的问题 [#53659](https://github.com/pingcap/tidb/issues/53659) @[D3Hunter](https://github.com/D3Hunter)
    - 修复当视图定义中使用子查询作为列定义时，通过 `information_schema.columns` 获取列信息返回告警 Warning 1356 的问题 [#54343](https://github.com/pingcap/tidb/issues/54343) @[lance6716](https://github.com/lance6716)
    - 修复使用索引加速添加唯一索引在遇到 owner 切换时可能导致 `Duplicate entry` 报错的问题 [#49233](https://github.com/pingcap/tidb/issues/49233) @[lance6716](https://github.com/lance6716)
    - 修复设置 `global.tidb_cloud_storage_uri` 时报错信息不清晰的问题 [#54096](https://github.com/pingcap/tidb/issues/54096) @[lance6716](https://github.com/lance6716)
    - 修复 Sync Load QPS 监控指标显示不正确的问题 [#53558](https://github.com/pingcap/tidb/issues/53558) @[hawkingrei](https://github.com/hawkingrei)
    - 修复并发加载初始统计信息时可能遗漏加载的问题 [#53607](https://github.com/pingcap/tidb/issues/53607) @[hawkingrei](https://github.com/hawkingrei)
    - 修复针对 `SELECT ... FOR UPDATE` 复用了错误点查询计划的问题 [#54652](https://github.com/pingcap/tidb/issues/54652) @[qw4990](https://github.com/qw4990)

+ TiKV

    - 修复 `advance-ts-interval` 配置未被用于限制 CDC 和 log-backup 模块中 `check_leader` 操作的 timeout，导致在某些情况下 TiKV 正常重启时 `resolved_ts` lag 过大的问题 [#17107](https://github.com/tikv/tikv/issues/17107) @[MyonKeminta](https://github.com/MyonKeminta)
    - 修复设置 gRPC 消息的压缩算法 (`grpc-compression-type`) 对 TiKV 发送到 TiDB 的消息不起作用的问题 [#17176](https://github.com/tikv/tikv/issues/17176) @[ekexium](https://github.com/ekexium)
    - 修复执行 `make docker` 和 `make docker_test` 失败的问题 [#17075](https://github.com/tikv/tikv/issues/17075) @[shunki-fujita](https://github.com/shunki-fujita)
    - 修复 **gRPC request sources duration** 在监控中显示错误的问题 [#17133](https://github.com/tikv/tikv/issues/17133) @[King-Dylan](https://github.com/King-Dylan)
    - 修复 tikv-ctl 的 `raft region` 命令的输出中未包含 Region 状态信息的问题 [#17037](https://github.com/tikv/tikv/issues/17037) @[glorv](https://github.com/glorv)
    - 修复在线变更 `raftstore.periodic-full-compact-start-times` 配置项可能会导致 TiKV panic 的问题 [#17066](https://github.com/tikv/tikv/issues/17066) @[SpadeA-Tang](https://github.com/SpadeA-Tang)
    - 修复 TiKV 在应用损坏的 Raft 数据快照时反复 panic 的问题 [#15292](https://github.com/tikv/tikv/issues/15292) @[LykxSassinator](https://github.com/LykxSassinator)
    - 修复缓存条目在尚未被持久化时就被释放导致 TiKV panic 的问题 [#17040](https://github.com/tikv/tikv/issues/17040) @[glorv](https://github.com/glorv)

+ PD

    - 修复获取表属性时错误调用 PD API 的问题 [#55188](https://github.com/pingcap/tidb/issues/55188) @[JmPotato](https://github.com/JmPotato)
    - 修复 `INFORMATION_SCHEMA.RUNAWAY_WATCHES` 表中时间类型不正确的问题 [#54770](https://github.com/pingcap/tidb/issues/54770) @[HuSharp](https://github.com/HuSharp)
    - 修复部分日志未脱敏的问题 [#8419](https://github.com/tikv/pd/issues/8419) @[rleungx](https://github.com/rleungx)
    - 修复 `Filter` 监控项缺少部分数据的问题 [#8098](https://github.com/tikv/pd/issues/8098) @[nolouch](https://github.com/nolouch)
    - 修复 HTTP 客户端在开启 TLS 时可能 panic 的问题 [#8237](https://github.com/tikv/pd/issues/8237) @[okJiang](https://github.com/okJiang)
    - 修复加密管理器在使用前未初始化的问题 [#8384](https://github.com/tikv/pd/issues/8384) @[rleungx](https://github.com/rleungx)
    - 修复资源组 (Resource Group) 在高并发场景下无法有效限制资源使用的问题 [#8435](https://github.com/tikv/pd/issues/8435) @[nolouch](https://github.com/nolouch)
    - 修复 `store limit` 相关的数据竞争问题 [#8253](https://github.com/tikv/pd/issues/8253) @[lhy1024](https://github.com/lhy1024)
    - 修复开启 `scheduling` 微服务后，扩缩容进度显示错误的问题 [#8331](https://github.com/tikv/pd/issues/8331) @[rleungx](https://github.com/rleungx)
    - 修复开启 `tso` 微服务后，TSO 节点无法动态更新的问题 [#8154](https://github.com/tikv/pd/issues/8154) @[rleungx](https://github.com/rleungx)
    - 修复资源组遇到的数据竞争问题 [#8267](https://github.com/tikv/pd/issues/8267) @[HuSharp](https://github.com/HuSharp)
    - 修复资源组在请求 token 超过 500 ms 时遇到超出配额限制的问题 [#8349](https://github.com/tikv/pd/issues/8349) @[nolouch](https://github.com/nolouch)
    - 修复手动切换 PD leader 可能失败的问题 [#8225](https://github.com/tikv/pd/issues/8225) @[HuSharp](https://github.com/HuSharp)
    - 修复 etcd client 中已经删除的节点仍然出现在候选连接列表中的问题 [#8286](https://github.com/tikv/pd/issues/8286) @[JmPotato](https://github.com/JmPotato)
    - 修复 `ALTER PLACEMENT POLICY` 无法修改 placement policy 的问题 [#52257](https://github.com/pingcap/tidb/issues/52257) [#51712](https://github.com/pingcap/tidb/issues/51712) @[jiyfhust](https://github.com/jiyfhust)
    - 修复写热点调度可能会违反放置策略 (placement policy) 约束的问题 [#7848](https://github.com/tikv/pd/issues/7848) @[lhy1024](https://github.com/lhy1024)
    - 修复使用 Placement Rules 的情况下，down peer 可能无法恢复的问题 [#7808](https://github.com/tikv/pd/issues/7808) @[rleungx](https://github.com/rleungx)
    - 修复取消资源组查询导致大量重试的问题 [#8217](https://github.com/tikv/pd/issues/8217) @[nolouch](https://github.com/nolouch)
    - 修复 PD 在进行 operator 检查时遇到的数据竞争问题 [#8263](https://github.com/tikv/pd/issues/8263) @[lhy1024](https://github.com/lhy1024)
    - 修复将角色 (role) 绑定到资源组时未报错的问题 [#54417](https://github.com/pingcap/tidb/issues/54417) @[JmPotato](https://github.com/JmPotato)
    - 修复将 TiKV 配置项 [`coprocessor.region-split-size`](/tikv-configuration-file.md#region-split-size) 设置为小于 1 MiB 的值会导致 PD panic 的问题 [#8323](https://github.com/tikv/pd/issues/8323) @[JmPotato](https://github.com/JmPotato)

+ TiFlash

    - 修复 TiFlash 与任意 PD 之间发生网络分区（即网络连接断开），可能导致读请求超时报错的问题 [#9243](https://github.com/pingcap/tiflash/issues/9243) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - 修复函数 `SUBSTRING_INDEX()` 可能导致 TiFlash Crash 的问题 [#9116](https://github.com/pingcap/tiflash/issues/9116) @[wshwsh12](https://github.com/wshwsh12)
    - 修复通过 BR 或 TiDB Lightning 导入数据后，FastScan 模式下可能读到大量重复行数据的问题 [#9118](https://github.com/pingcap/tiflash/issues/9118) @[JinheLin](https://github.com/JinheLin)
    - 修复数据库创建后短时间内被删除时，TiFlash 可能 panic 的问题 [#9266](https://github.com/pingcap/tiflash/issues/9266) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复将 TiFlash 中 SSL 证书配置项设置为空字符串会错误开启 TLS 并导致 TiFlash 启动失败的问题 [#9235](https://github.com/pingcap/tiflash/issues/9235) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复在存算分离架构下，DDL 新增带有 not null 属性的列后，查询可能返回错误的 null 值的问题 [#9084](https://github.com/pingcap/tiflash/issues/9084) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - 修复跨数据库对含空分区的分区表执行 `RENAME TABLE ... TO ...` 后，TiFlash 可能 panic 的问题 [#9132](https://github.com/pingcap/tiflash/issues/9132) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复在含空分区的分区表上执行查询时，可能会超时的问题 [#9024](https://github.com/pingcap/tiflash/issues/9024) @[JinheLin](https://github.com/JinheLin)
    - 修复开启延迟物化后，部分查询在执行时可能报列类型不匹配错误的问题 [#9175](https://github.com/pingcap/tiflash/issues/9175) @[JinheLin](https://github.com/JinheLin)
    - 修复开启延迟物化后，带有虚拟生成列的查询可能返回错误结果的问题 [#9188](https://github.com/pingcap/tiflash/issues/9188) @[JinheLin](https://github.com/JinheLin)

+ Tools

    + Backup & Restore (BR)

        - 修复断点备份过程中查找 Region leader 中断导致备份性能受影响问题 [#17168](https://github.com/tikv/tikv/issues/17168) @[Leavrth](https://github.com/Leavrth)
        - 修复增量备份过程中扫描 DDL 作业的效率较低的问题 [#54139](https://github.com/pingcap/tidb/issues/54139) @[3pointer](https://github.com/3pointer)
        - 修复在恢复过程中，由于多层重试导致 BR 无法正确识别错误的问题 [#54053](https://github.com/pingcap/tidb/issues/54053) @[RidRisR](https://github.com/RidRisR)
        - 修复由于 `EndKey` 为空导致恢复事务 KV 集群失败的问题 [#52574](https://github.com/pingcap/tidb/issues/52574) @[3pointer](https://github.com/3pointer)
        - 修复日志备份在 advancer owner 发生迁移后可能被暂停的问题 [#53561](https://github.com/pingcap/tidb/issues/53561) @[RidRisR](https://github.com/RidRisR)
        - 修复增量恢复过程中 `ADD INDEX`、`MODIFY COLUMN` 等需要回填的 DDL 可能无法正确恢复的问题 [#54426](https://github.com/pingcap/tidb/issues/54426) @[3pointer](https://github.com/3pointer)
        - 修复 PD 连接失败导致日志备份 advancer owner 所在的 TiDB 可能崩溃的问题 [#52597](https://github.com/pingcap/tidb/issues/52597) @[YuJuncen](https://github.com/YuJuncen)

    + TiCDC

        - 修复 Region 变更导致下游 panic 的问题 [#17233](https://github.com/tikv/tikv/issues/17233) @[hicqu](https://github.com/hicqu)
        - 修复当上游未启用新的排序规则时，TiCDC 无法正确解码聚簇索引表中的主键的问题 [#11371](https://github.com/pingcap/tiflow/issues/11371) @[lidezhu](https://github.com/lidezhu)
        - 修复拆分 `UPDATE` 事件后校验码未正确设置为 `0` 的问题 [#11402](https://github.com/pingcap/tiflow/issues/11402) @[3AceShowHand](https://github.com/3AceShowHand)
        - 修复在多节点环境下进行大量 `UPDATE` 操作时，反复重启 Changefeed 可能导致的数据不一致问题 [#11219](https://github.com/pingcap/tiflow/issues/11219) @[lidezhu](https://github.com/lidezhu)
        - 修复当下游 Kafka 无法访问时，Processor 模块可能卡住的问题 [#11340](https://github.com/pingcap/tiflow/issues/11340) @[asddongmen](https://github.com/asddongmen)

    + TiDB Data Migration (DM)

        - 修复同步 MariaDB 数据时 `SET` 语句导致 DM panic 的问题 [#10206](https://github.com/pingcap/tiflow/issues/10206) @[dveeden](https://github.com/dveeden)
        - 升级 `go-mysql` 以修复连接阻塞的问题 [#11041](https://github.com/pingcap/tiflow/issues/11041) @[D3Hunter](https://github.com/D3Hunter)
        - 修复当索引长度超过 `max-index-length` 默认值时数据同步中断的问题 [#11459](https://github.com/pingcap/tiflow/issues/11459) @[michaelmdeng](https://github.com/michaelmdeng)
        - 修复 schema tracker 无法正确处理 LIST 分区表导致 DM 报错的问题 [#11408](https://github.com/pingcap/tiflow/issues/11408) @[lance6716](https://github.com/lance6716)

    + TiDB Lightning

        - 修复 TiDB Lightning 获取 keyspace 失败时输出的 `WARN` 日志可能引起用户混淆的问题 [#54232](https://github.com/pingcap/tidb/issues/54232) @[kennytm](https://github.com/kennytm)

    + Dumpling

        - 修复 Dumpling 在同时导出表和视图时报错的问题 [#53682](https://github.com/pingcap/tidb/issues/53682) @[tangenta](https://github.com/tangenta)

    + TiDB Binlog

        - 修复开启 TiDB Binlog 后，在 `ADD COLUMN` 执行过程中删除行可能报错 `data and columnID count not match` 的问题 [#53133](https://github.com/pingcap/tidb/issues/53133) @[tangenta](https://github.com/tangenta)
