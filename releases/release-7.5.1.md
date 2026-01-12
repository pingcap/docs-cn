---
title: TiDB 7.5.1 Release Notes
summary: 了解 TiDB 7.5.1 版本的兼容性变更、改进提升，以及错误修复。
---

# TiDB 7.5.1 Release Notes

发版日期：2024 年 2 月 29 日

TiDB 版本：7.5.1

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v7.5/quick-start-with-tidb) | [生产部署](https://docs.pingcap.com/zh/tidb/v7.5/production-deployment-using-tiup)

## 兼容性变更

- 在安全增强模式 (SEM) 下禁止设置 [`require_secure_transport`](https://docs.pingcap.com/zh/tidb/v7.5/system-variables#require_secure_transport-从-v610-版本开始引入) 为 `ON`，避免用户无法连接的问题 [#47665](https://github.com/pingcap/tidb/issues/47665) @[tiancaiamao](https://github.com/tiancaiamao)
- 为减少日志打印的开销，TiFlash 配置项 `logger.level` 默认值由 `"debug"` 改为 `"info"` [#8641](https://github.com/pingcap/tiflash/issues/8641) @[JaySon-Huang](https://github.com/JaySon-Huang)
- 新增 TiKV 配置项 [`gc.num-threads`](https://docs.pingcap.com/zh/tidb/v7.5/tikv-configuration-file#num-threads-从-v658-和-v751-版本开始引入)，用于设置当 `enable-compaction-filter` 为 `false` 时 GC 的线程个数 [#16101](https://github.com/tikv/tikv/issues/16101) @[tonyxuqqi](https://github.com/tonyxuqqi)
- TiCDC Changefeed 新增以下配置项：
    - [`compression`](/ticdc/ticdc-changefeed-config.md)：你可以设置 redo log 文件的压缩行为 [#10176](https://github.com/pingcap/tiflow/issues/10176) @[sdojjy](https://github.com/sdojjy)
    - [`sink.cloud-storage-config`](/ticdc/ticdc-changefeed-config.md)：你可以设置同步数据到对象存储时自动清理历史数据的功能 [#10109](https://github.com/pingcap/tiflow/issues/10109) @[CharlesCheung96](https://github.com/CharlesCheung96)
    - [`consistent.flush-concurrency`](/ticdc/ticdc-changefeed-config.md)：你可以设置 redo log 上传单个文件的并发数 [#10226](https://github.com/pingcap/tiflow/issues/10226) @[sdojjy](https://github.com/sdojjy)

## 改进提升

+ TiDB

    - 在 DDL schema 重载过程中使用 `tikv_client_read_timeout`，以降低 Meta Region Leader 读不可用对集群的影响 [#48124](https://github.com/pingcap/tidb/issues/48124) @[cfzjywxk](https://github.com/cfzjywxk)
    - 增强资源管控相关的观测性 [#49318](https://github.com/pingcap/tidb/issues/49318) @[glorv](https://github.com/glorv) @[bufferflies](https://github.com/bufferflies) @[nolouch](https://github.com/nolouch)

        随着越来越多用户利用资源组对业务应用进行隔离，资源管控提供了更丰富的基于资源组的数据，协助你观测资源组负载、资源组设置，确保出现问题时能够快速发现并精准诊断。其中包括：

        - [慢查询日志](/identify-slow-queries.md)增加资源组名称、RU 消耗、以及等待资源耗时。
        - [Statement Summary Tables](/statement-summary-tables.md) 增加资源组名称、RU 消耗、以及等待资源耗时。
        - 在变量 [`tidb_last_query_info`](/system-variables.md#tidb_last_query_info-从-v4014-版本开始引入) 中增加了 SQL 的 [RU](/tidb-resource-control-ru-groups.md#什么是-request-unit-ru) 消耗信息 `ru_consumption`，你可以利用此变量获取会话中上一条语句的资源消耗。
        - 增加基于[资源组的数据库指标](/grafana-resource-control-dashboard.md)：QPS/TPS、执行时间 (P999/P99/P95)、失败次数、连接数。

    - 将 `CANCEL IMPORT JOB` 命令调整为同步命令 [#48736](https://github.com/pingcap/tidb/issues/48736) @[D3Hunter](https://github.com/D3Hunter)
    - 新增支持 [`FLASHBACK CLUSTER TO TSO`](https://docs.pingcap.com/zh/tidb/v7.5/sql-statement-flashback-cluster) 语法 [#48372](https://github.com/pingcap/tidb/issues/48372) @[BornChanger](https://github.com/BornChanger)
    - 改进 TiDB 在处理部分类型转换时的实现，并修复相关问题 [#47945](https://github.com/pingcap/tidb/issues/47945) [#47864](https://github.com/pingcap/tidb/issues/47864) [#47829](https://github.com/pingcap/tidb/issues/47829) [#47816](https://github.com/pingcap/tidb/issues/47816) @[YangKeao](https://github.com/YangKeao) @[lcwangchao](https://github.com/lcwangchao)
    - 当使用非二进制排序规则并且查询条件中包含 `LIKE` 时，优化器可以生成 IndexRangeScan 以提升执行效率 [#48181](https://github.com/pingcap/tidb/issues/48181) [#49138](https://github.com/pingcap/tidb/issues/49138) @[time-and-fate](https://github.com/time-and-fate)
    - 增强特定情况下 `OUTER JOIN` 转 `INNER JOIN` 的能力 [#49616](https://github.com/pingcap/tidb/issues/49616) @[qw4990](https://github.com/qw4990)
    - 允许多个快速加索引 DDL 任务排队执行，而非回退为普通加索引任务 [#47758](https://github.com/pingcap/tidb/issues/47758) @[tangenta](https://github.com/tangenta)
    - 提升空表加索引的速度 [#49682](https://github.com/pingcap/tidb/issues/49682) @[zimulala](https://github.com/zimulala)

+ TiKV

    - 改善慢节点检测的判定算法，提升算法检测的灵敏度，同时降低了算法对于热读写场景下的误判率 [#15909](https://github.com/tikv/tikv/issues/15909) @[LykxSassinator](https://github.com/LykxSassinator)

+ TiFlash

    - 改进 [RU (Request Unit)](/tidb-resource-control-ru-groups.md#什么是-request-unit-ru) 计算方法，以提高 RU 值的稳定性 [#8391](https://github.com/pingcap/tiflash/issues/8391) @[guo-shaoge](https://github.com/guo-shaoge)
    - 降低磁盘性能抖动对读取延迟的影响 [#8583](https://github.com/pingcap/tiflash/issues/8583) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 减少后台数据 GC 任务对读、写任务延迟的影响 [#8650](https://github.com/pingcap/tiflash/issues/8650) @[JaySon-Huang](https://github.com/JaySon-Huang)

+ Tools

    + Backup & Restore (BR)

        - 使用更优的算法，提升数据恢复过程中 SST 文件合并的速度 [#50613](https://github.com/pingcap/tidb/issues/50613) @[Leavrth](https://github.com/Leavrth)
        - 支持在数据恢复过程中批量创建数据库 [#50767](https://github.com/pingcap/tidb/issues/50767) @[Leavrth](https://github.com/Leavrth)
        - 支持在数据恢复过程中批量 ingest SST 文件 [#16267](https://github.com/tikv/tikv/issues/16267) @[3pointer](https://github.com/3pointer)
        - 在日志备份过程中，增加了在日志和监控指标中打印影响 global checkpoint 推进的最慢的 Region 的信息 [#51046](https://github.com/pingcap/tidb/issues/51046) @[YuJuncen](https://github.com/YuJuncen)
        - 提升了 `RESTORE` 语句在大数据量表场景下的建表性能 [#48301](https://github.com/pingcap/tidb/issues/48301) @[Leavrth](https://github.com/Leavrth)
        - BR 支持通过设置 `merge-schedule-limit` 配置项为 `0` 来暂停 Region 合并 [#7148](https://github.com/tikv/pd/issues/7148) @[3pointer](https://github.com/3pointer)
        - 重构 BR 异常处理机制，提高对未知错误的容忍度 [#47656](https://github.com/pingcap/tidb/issues/47656) @[3pointer](https://github.com/3pointer)

    + TiCDC

        - 支持在 TiDB Dashboard 中搜索 TiCDC 日志 [#10263](https://github.com/pingcap/tiflow/issues/10263) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - 支持[查询 changefeed 的下游同步状态](https://docs.pingcap.com/zh/tidb/v7.5/ticdc-open-api-v2#查询特定同步任务是否完成)，以确认 TiCDC 是否已将所接收到的上游变更完全同步到下游 [#10289](https://github.com/pingcap/tiflow/issues/10289) @[hongyunyan](https://github.com/hongyunyan)
        - 通过增加并行，优化了 TiCDC 同步数据到对象存储的性能 [#10098](https://github.com/pingcap/tiflow/issues/10098) @[CharlesCheung96](https://github.com/CharlesCheung96)

    + TiDB Lightning

        - 优化导入大量数据量较小的表时的性能 [#50105](https://github.com/pingcap/tidb/issues/50105) @[D3Hunter](https://github.com/D3Hunter)

## 错误修复

+ TiDB

    - 修复设置系统变量 `tidb_service_scope` 未生效的问题 [#49245](https://github.com/pingcap/tidb/issues/49245) @[ywqzzy](https://github.com/ywqzzy)
    - 修复开启压缩时，通讯协议无法处理大于或等于 16 MB 报文的问题 [#47157](https://github.com/pingcap/tidb/issues/47157) [#47161](https://github.com/pingcap/tidb/issues/47161) @[dveeden](https://github.com/dveeden)
    - 修复 `approx_percentile` 函数可能导致 TiDB panic 的问题 [#40463](https://github.com/pingcap/tidb/issues/40463) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - 修复 TiDB 在字符串函数参数为 `NULL` 常量时可能会隐式插入 `from_binary` 函数导致一些表达式无法下推到 TiFlash 的问题 [#49526](https://github.com/pingcap/tidb/issues/49526) @[YangKeao](https://github.com/YangKeao)
    - 修复当 `HashJoin` 算子落盘失败时 goroutine 可能泄露的问题 [#50841](https://github.com/pingcap/tidb/issues/50841) @[wshwsh12](https://github.com/wshwsh12)
    - 修复 `BIT` 类型的列在参与一些函数计算时，可能会因为 decode 失败导致查询出错的问题 [#49566](https://github.com/pingcap/tidb/issues/49566) [#50850](https://github.com/pingcap/tidb/issues/50850) [#50855](https://github.com/pingcap/tidb/issues/50855) @[jiyfhust](https://github.com/jiyfhust)
    - 修复 CTE 查询使用的内存超限时可能会导致 goroutine 泄露的问题 [#50337](https://github.com/pingcap/tidb/issues/50337) @[guo-shaoge](https://github.com/guo-shaoge)
    - 修复在 TiFlash 延迟物化在处理关联列时结果可能出错的问题 [#49241](https://github.com/pingcap/tidb/issues/49241) [#51204](https://github.com/pingcap/tidb/issues/51204) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - 修复 TiDB 记录历史统计信息时，后台工作线程可能 panic 的问题 [#49076](https://github.com/pingcap/tidb/issues/49076) @[hawkingrei](https://github.com/hawkingrei)
    - 修复 TiDB 合并分区表全局统计信息的直方图时可能报错问题 [#49023](https://github.com/pingcap/tidb/issues/49023) @[hawkingrei](https://github.com/hawkingrei)
    - 修复删掉分区后，`stats_meta` 表的历史统计信息没有更新的问题 [#49334](https://github.com/pingcap/tidb/issues/49334) @[hi-rustin](https://github.com/Rustin170506)
    - 修复多值索引被误选为 `Index Join` 的 Probe 端导致查询结果不准确的问题 [#50382](https://github.com/pingcap/tidb/issues/50382) @[AilinKid](https://github.com/AilinKid)
    - 修复 `USE_INDEX_MERGE` hint 对多值索引不生效的问题 [#50553](https://github.com/pingcap/tidb/issues/50553) @[AilinKid](https://github.com/AilinKid)
    - 修复用户查询 `INFORMATION_SCHEMA.ANALYZE_STATUS` 系统表时可能遇到报错的问题 [#48835](https://github.com/pingcap/tidb/issues/48835) @[hi-rustin](https://github.com/Rustin170506)
    - 修复 TiDB 错误地消除 `group by` 中的常量值导致查询结果出错的问题 [#38756](https://github.com/pingcap/tidb/issues/38756) @[hi-rustin](https://github.com/Rustin170506)
    - 修复表的 `ANALYZE` 任务统计的 `processed_rows` 可能超过表的总行数的问题 [#50632](https://github.com/pingcap/tidb/issues/50632) @[hawkingrei](https://github.com/hawkingrei)
    - 修复如果开启 `tidb_enable_prepared_plan_cache` 变量之后再关闭此变量，使用 `EXECUTE` 语句执行 `PREPARE STMT` 时可能 panic 的问题 [#49344](https://github.com/pingcap/tidb/issues/49344) @[qw4990](https://github.com/qw4990)
    - 修复查询使用 `NATURAL JOIN` 时可能报错 `Column ... in from clause is ambiguous` 的问题 [#32044](https://github.com/pingcap/tidb/issues/32044) @[AilinKid](https://github.com/AilinKid)
    - 修复当 JSON 数组为空数组时，使用多值索引访问可能返回错误结果的问题 [#50125](https://github.com/pingcap/tidb/issues/50125) @[YangKeao](https://github.com/YangKeao)
    - 修复使用聚合函数分组计算时可能报错 `Can't find column ...` 的问题 [#50926](https://github.com/pingcap/tidb/issues/50926) @[qw4990](https://github.com/qw4990)
    - 修复使用 `SET_VAR` 控制字符串类型的变量可能会失效的问题 [#50507](https://github.com/pingcap/tidb/issues/50507) @[qw4990](https://github.com/qw4990)
    - 修复 `tidb_server_memory_limit` 导致内存长期压力较高时，TiDB CPU 利用率过高的问题 [#48741](https://github.com/pingcap/tidb/issues/48741) @[XuHuaiyu](https://github.com/XuHuaiyu)
    - 修复有依赖关系的两个 DDL 任务的完成时间顺序不正确的问题 [#49498](https://github.com/pingcap/tidb/issues/49498) @[tangenta](https://github.com/tangenta)
    - 修复不合法的优化器 hint 可能会导致合法 hint 不生效的问题 [#49308](https://github.com/pingcap/tidb/issues/49308) @[hawkingrei](https://github.com/hawkingrei)
    - 修复 `CHECK` 约束的 DDL 卡住的问题 [#47632](https://github.com/pingcap/tidb/issues/47632) @[jiyfhust](https://github.com/jiyfhust)
    - 修复 `CHECK` 约束的 `ENFORCED` 选项的行为与 MySQL 8.0 不一致的问题 [#47567](https://github.com/pingcap/tidb/issues/47567) [#47631](https://github.com/pingcap/tidb/issues/47631) @[jiyfhust](https://github.com/jiyfhust)
    - 修复 CTE 查询在重试过程中可能会报错 `type assertion for CTEStorageMap failed` 的问题 [#46522](https://github.com/pingcap/tidb/issues/46522) @[tiancaiamao](https://github.com/tiancaiamao)
    - 修复开启 `tidb_multi_statement_mode` 模式时，使用索引点查的 `DELETE` 和 `UPDATE` 语句可能会报错的问题 [#50012](https://github.com/pingcap/tidb/issues/50012) @[tangenta](https://github.com/tangenta)
    - 修复包含递归 (`WITH RECURSIVE`) CTE 的 `UPDATE` 或 `DELETE` 语句可能会产生错误结果的问题 [#48969](https://github.com/pingcap/tidb/issues/48969) @[winoros](https://github.com/winoros)
    - 修复特定情况下优化器将 TiFlash 选择路径错误转化为 DUAL Table 的问题 [#49285](https://github.com/pingcap/tidb/issues/49285) @[AilinKid](https://github.com/AilinKid)
    - 修复某些情况下相同的查询计划拥有不同的 `PLAN_DIGEST` 的问题 [#47634](https://github.com/pingcap/tidb/issues/47634) @[King-Dylan](https://github.com/King-Dylan)
    - 修复设置统计信息自动更新的时间窗口后，时间窗口外统计信息仍然可能更新的问题 [#49552](https://github.com/pingcap/tidb/issues/49552) @[hawkingrei](https://github.com/hawkingrei)
    - 修复 `ENUM` 类型列作为 join 键时，查询结果错误的问题 [#48991](https://github.com/pingcap/tidb/issues/48991) @[winoros](https://github.com/winoros)
    - 修复执行包含 `ORDER BY` 的 `UNIQUE` 索引点查时可能报错的问题 [#49920](https://github.com/pingcap/tidb/issues/49920) @[jackysp](https://github.com/jackysp)
    - 修复多级嵌套的 `UNION` 查询中 `LIMIT` 无效的问题 [#49874](https://github.com/pingcap/tidb/issues/49874) @[Defined2014](https://github.com/Defined2014)
    - 修复 MPP 计算 `COUNT(INT)` 时结果可能出错的问题 [#48643](https://github.com/pingcap/tidb/issues/48643) @[AilinKid](https://github.com/AilinKid)
    - 修复在解析 `ENUM` 或 `SET` 类型的非法值时会导致 SQL 语句报错的问题 [#49487](https://github.com/pingcap/tidb/issues/49487) @[winoros](https://github.com/winoros)
    - 修复 TiDB panic 并报错 `invalid memory address or nil pointer dereference` 的问题 [#42739](https://github.com/pingcap/tidb/issues/42739) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - 修复 `UNION ALL` 第一个子节点是 DUAL Table 时，执行可能报错的问题 [#48755](https://github.com/pingcap/tidb/issues/48755) @[winoros](https://github.com/winoros)
    - 修复常见 hint 在 `UNION ALL` 语句中未生效的问题 [#50068](https://github.com/pingcap/tidb/issues/50068) @[hawkingrei](https://github.com/hawkingrei)
    - 修复 TiDB server 在优雅关闭 (graceful shutdown) 时可能 panic 的问题 [#36793](https://github.com/pingcap/tidb/issues/36793) @[bb7133](https://github.com/bb7133)
    - 修复在某些时区下夏令时显示有误的问题 [#49586](https://github.com/pingcap/tidb/issues/49586) @[overvenus](https://github.com/overvenus)
    - 修复静态 `CALIBRATE RESOURCE` 依赖 Prometheus 数据的问题 [#49174](https://github.com/pingcap/tidb/issues/49174) @[glorv](https://github.com/glorv)
    - 修复无法在 `REPLACE INTO` 语句中使用 hint 的问题 [#34325](https://github.com/pingcap/tidb/issues/34325) @[YangKeao](https://github.com/YangKeao)
    - 修复查询语句包含 `GROUP_CONCANT(ORDER BY)` 语法时，执行可能出错的问题 [#49986](https://github.com/pingcap/tidb/issues/49986) @[AilinKid](https://github.com/AilinKid)
    - 修复 TiDB server 在使用企业插件审计日志时可能占用大量资源的问题 [#49273](https://github.com/pingcap/tidb/issues/49273) @[lcwangchao](https://github.com/lcwangchao)
    - 修复使用旧接口导致表的元信息可能不一致的问题 [#49751](https://github.com/pingcap/tidb/issues/49751) @[hawkingrei](https://github.com/hawkingrei)
    - 修复关闭 `tidb_enable_collect_execution_info` 导致 Coprocessor Cache panic 的问题 [#48212](https://github.com/pingcap/tidb/issues/48212) @[you06](https://github.com/you06)
    - 修复当分区列类型为 `DATETIME` 时，执行 `ALTER TABLE ... LAST PARTITION` 失败的问题 [#48814](https://github.com/pingcap/tidb/issues/48814) @[crazycs520](https://github.com/crazycs520)
    - 修复通过 `COM_STMT_EXECUTE` 方式执行的 `COMMIT` 或 `ROLLBACK` 操作无法结束已超时事务的问题 [#49151](https://github.com/pingcap/tidb/issues/49151) @[zyguan](https://github.com/zyguan)
    - 修复直方图的边界包含 `NULL` 时，直方图统计信息可能无法解析成可读字符串的问题 [#49823](https://github.com/pingcap/tidb/issues/49823) @[AilinKid](https://github.com/AilinKid)
    - 修复当内存使用超限时包含公共表表达式 (CTE) 的查询非预期卡住的问题 [#49096](https://github.com/pingcap/tidb/issues/49096) @[AilinKid](https://github.com/AilinKid)
    - 修复在分布式框架下，DDL Owner 网络隔离后执行 `ADD INDEX` 操作导致数据不一致的问题 [#49773](https://github.com/pingcap/tidb/issues/49773) @[tangenta](https://github.com/tangenta)
    - 修复使用 `AUTO_ID_CACHE=1` 的自增列时，由于并发冲突导致自增 ID 分配报错的问题 [#50519](https://github.com/pingcap/tidb/issues/50519) @[tiancaiamao](https://github.com/tiancaiamao)
    - 修复包含 Apply 操作的查询在报错 `fatal error: concurrent map writes` 后导致 TiDB 崩溃的问题 [#50347](https://github.com/pingcap/tidb/issues/50347) @[SeaRise](https://github.com/SeaRise)
    - 修复当 DDL `jobID` 恢复为 0 时 TiDB 节点 panic 的问题 [#46296](https://github.com/pingcap/tidb/issues/46296) @[jiyfhust](https://github.com/jiyfhust)
    - 修复由于 `STREAM_AGG()` 错误处理 CI 导致查询结果有误的问题 [#49902](https://github.com/pingcap/tidb/issues/49902) @[wshwsh12](https://github.com/wshwsh12)
    - 缓解当要处理的表的数量或表的分区数量过多时，TiDB 节点 OOM 的问题 [#50077](https://github.com/pingcap/tidb/issues/50077) @[zimulala](https://github.com/zimulala)
    - 修复 `LEADING` hint 在 `UNION ALL` 语句中无法生效的问题 [#50067](https://github.com/pingcap/tidb/issues/50067) @[hawkingrei](https://github.com/hawkingrei)
    - 修复在嵌套的 `UNION` 查询中 `LIMIT` 和 `OPRDERBY` 可能无效的问题 [#49377](https://github.com/pingcap/tidb/issues/49377) @[AilinKid](https://github.com/AilinKid)
    - 修复包含 IndexHashJoin 算子的查询由于内存超过 `tidb_mem_quota_query` 而卡住的问题 [#49033](https://github.com/pingcap/tidb/issues/49033) @[XuHuaiyu](https://github.com/XuHuaiyu)
    - 修复常量传播在处理 `ENUM` 或 `SET` 类型时结果出错的问题 [#49440](https://github.com/pingcap/tidb/issues/49440) @[winoros](https://github.com/winoros)
    - 修复使用 `PREPARE` 方式执行 `SELECT INTO OUTFILE` 语句时，应报错却返回执行成功的问题 [#49166](https://github.com/pingcap/tidb/issues/49166) @[qw4990](https://github.com/qw4990)
    - 修复当查询使用了会强制排序的优化器 hint（例如 `STREAM_AGG()`）且其执行计划包含 `IndexMerge` 时，强制排序可能会失效的问题 [#49605](https://github.com/pingcap/tidb/issues/49605) @[AilinKid](https://github.com/AilinKid)
    - 修复在有大量表时，`AUTO_ID_CACHE=1` 的表可能造成 gRPC 客户端泄漏的问题 [#48869](https://github.com/pingcap/tidb/issues/48869) @[tiancaiamao](https://github.com/tiancaiamao)
    - 修复在非严格模式下 (`sql_mode = ''`)，`INSERT` 过程中产生截断仍然会报错的问题 [#49369](https://github.com/pingcap/tidb/issues/49369) @[tiancaiamao](https://github.com/tiancaiamao)
    - 修复数据中包含后导空格时，在 `LIKE` 中使用 `_` 通配符可能会导致查询结果出错的问题 [#48983](https://github.com/pingcap/tidb/issues/48983) @[time-and-fate](https://github.com/time-and-fate)
    - 修复更新 `tidb_mem_quota_query` 系统变量后执行 `ADMIN CHECK` 报错 `ERROR 8175` 的问题 [#49258](https://github.com/pingcap/tidb/issues/49258) @[tangenta](https://github.com/tangenta)
    - 修复构造统计信息时因为 Golang 隐式转换算法导致统计信息误差过大的问题 [#49801](https://github.com/pingcap/tidb/issues/49801) @[qw4990](https://github.com/qw4990)
    - 修复当 `tidb_max_chunk_size` 值较小时，包含 CTE 的查询出现 `runtime error: index out of range [32] with length 32` 错误的问题 [#48808](https://github.com/pingcap/tidb/issues/48808) @[guo-shaoge](https://github.com/guo-shaoge)

+ TiKV

    - 修复开启 `tidb_enable_row_level_checksum` 可能导致 TiKV panic 的问题 [#16371](https://github.com/tikv/tikv/issues/16371) @[cfzjywxk](https://github.com/cfzjywxk)
    - 修复 gRPC threads 在检查 `is_shutdown` 时可能出现 panic 的问题 [#16236](https://github.com/tikv/tikv/issues/16236) @[pingyu](https://github.com/pingyu)
    - 修复巴西和埃及时区转换错误的问题 [#16220](https://github.com/tikv/tikv/issues/16220) @[overvenus](https://github.com/overvenus)
    - 修复 Titan `blob-run-mode` 无法在线更新的问题 [#15978](https://github.com/tikv/tikv/issues/15978) @[tonyxuqqi](https://github.com/tonyxuqqi)
    - 修复 TiDB 和 TiKV 处理 `DECIMAL` 算术乘法截断时结果不一致的问题 [#16268](https://github.com/tikv/tikv/issues/16268) @[solotzg](https://github.com/solotzg)
    - 修复在 Flashback 时遇到 `notLeader` 或 `regionNotFound` 时卡住的问题 [#15712](https://github.com/tikv/tikv/issues/15712) @[HuSharp](https://github.com/HuSharp)
    - 修复损坏的 SST 文件可能会扩散到其他 TiKV 节点的问题 [#15986](https://github.com/tikv/tikv/issues/15986) @[Connor1996](https://github.com/Connor1996)
    - 修复如果 TiKV 运行极慢，在 Region Merge 之后可能 panic 的问题 [#16111](https://github.com/tikv/tikv/issues/16111) @[overvenus](https://github.com/overvenus)
    - 修复扩容时可能导致 DR Auto-Sync 的 joint state 超时问题 [#15817](https://github.com/tikv/tikv/issues/15817) @[Connor1996](https://github.com/Connor1996)
    - 修复 Resolved TS 可能被阻塞两小时的问题 [#11847](https://github.com/tikv/tikv/issues/11847) [#15520](https://github.com/tikv/tikv/issues/15520) [#39130](https://github.com/pingcap/tidb/issues/39130) @[overvenus](https://github.com/overvenus)
    - 修复 `cast_duration_as_time` 可能返回错误结果的问题 [#16211](https://github.com/tikv/tikv/issues/16211) @[gengliqi](https://github.com/gengliqi)
    - 修复在某些异常场景下（如阻塞在 Disk I/O 操作上）TiKV 假死而影响可用性的问题 [#16368](https://github.com/tikv/tikv/issues/16368) @[LykxSassinator](https://github.com/LykxSassinator)

+ PD

    - 修复批量查询 Resource Group 可能会导致 PD Panic 的问题 [#7206](https://github.com/tikv/pd/issues/7206) @[nolouch](https://github.com/nolouch)
    - 修复 PD 在通过 `systemd` 启动时无法读取资源限制的问题 [#7628](https://github.com/tikv/pd/issues/7628) @[bufferflies](https://github.com/bufferflies)
    - 修复 PD 磁盘时延持续抖动可能导致 PD 无法选出新 Leader 的问题 [#7251](https://github.com/tikv/pd/issues/7251) @[HuSharp](https://github.com/HuSharp)
    - 修复 PD 存在网络分区时可能导致调度延迟触发的问题 [#7016](https://github.com/tikv/pd/issues/7016) @[HuSharp](https://github.com/HuSharp)
    - 修复 PD 监控项 `learner-peer-count` 在发生 Leader 切换后未同步旧监控值的问题 [#7728](https://github.com/tikv/pd/issues/7728) @[CabinfeverB](https://github.com/CabinfeverB)
    - 修复 PD Leader 切换且新 Leader 与调用方之间存在网络隔离时，调用方不能正常更新 Leader 信息的问题 [#7416](https://github.com/tikv/pd/issues/7416) @[CabinfeverB](https://github.com/CabinfeverB)
    - 将 Gin Web Framework 的版本从 v1.8.1 升级到 v1.9.1 以修复部分安全问题 [#7438](https://github.com/tikv/pd/issues/7438) @[niubell](https://github.com/niubell)
    - 修复在不满足副本数量需求时，删除 orphan peer 的问题 [#7584](https://github.com/tikv/pd/issues/7584) @[bufferflies](https://github.com/bufferflies)
    - 修复使用 `pd-ctl` 查询没有 Leader 的 Region 时可能导致 PD panic 的问题 [#7630](https://github.com/tikv/pd/issues/7630) @[rleungx](https://github.com/rleungx)

+ TiFlash

    - 修复副本迁移时，因 TiFlash 与 PD 之间网络连接不稳定可能引发的 TiFlash panic 的问题 [#8323](https://github.com/pingcap/tiflash/issues/8323) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复移除 TiFlash 副本后重新添加可能导致 TiFlash 数据损坏的问题 [#8695](https://github.com/pingcap/tiflash/issues/8695) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复在插入数据后立即执行 `DROP TABLE` 以及 `FLASHBACK TABLE` 或 `RECOVER TABLE` 操作后，部分 TiFlash 副本数据无法恢复的潜在问题 [#8395](https://github.com/pingcap/tiflash/issues/8395) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复 Grafana 中部分面板显示的最大分位数耗时数据不正确的问题 [#8076](https://github.com/pingcap/tiflash/issues/8076) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复 TiFlash 发生远程读时可能会 crash 的问题 [#8685](https://github.com/pingcap/tiflash/issues/8685) @[guo-shaoge](https://github.com/guo-shaoge)
    - 修复 TiFlash 错误处理 `ENUM` 偏移量为 0 的问题 [#8311](https://github.com/pingcap/tiflash/issues/8311) @[solotzg](https://github.com/solotzg)
    - 修复成功执行的短查询打印过多信息日志的问题 [#8592](https://github.com/pingcap/tiflash/issues/8592) @[windtalker](https://github.com/windtalker)
    - 修复慢查询导致内存使用显著增加的问题 [#8564](https://github.com/pingcap/tiflash/issues/8564) @[JinheLin](https://github.com/JinheLin)
    - 修复 lowerUTF8/upperUTF8 不允许大小写字符占据不同字节数的错误 [#8484](https://github.com/pingcap/tiflash/issues/8484) @[gengliqi](https://github.com/gengliqi)
    - 修复在 stream 读时扫描多个分区表可能导致潜在的 OOM 问题 [#8505](https://github.com/pingcap/tiflash/issues/8505) @[gengliqi](https://github.com/gengliqi)
    - 修复当查询遇到内存限制后发生内存泄漏的问题 [#8447](https://github.com/pingcap/tiflash/issues/8447) @[JinheLin](https://github.com/JinheLin)
    - 修复在 TiDB 执行并发 DDL 遇到冲突时 TiFlash panic 的问题 [#8578](https://github.com/pingcap/tiflash/issues/8578) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复在执行 `ALTER TABLE ... MODIFY COLUMN ... NOT NULL` 时，将原本可为空的列修改为不可为空之后，导致 TiFlash panic 的问题 [#8419](https://github.com/pingcap/tiflash/issues/8419) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复在查询带有类似 `ColumnRef in (Literal, Func...)` 的过滤条件时，查询结果出错的问题 [#8631](https://github.com/pingcap/tiflash/issues/8631) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - 修复在执行 `FLASHBACK DATABASE` 后 TiFlash 副本的数据仍会被 GC 回收的问题 [#8450](https://github.com/pingcap/tiflash/issues/8450) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复存算分离架构下，可能无法正常选出对象存储数据 GC owner 的问题 [#8519](https://github.com/pingcap/tiflash/issues/8519) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复 `GREATEST` 或 `LEAST` 函数在包含常量字符串参数时，可能发生的随机无效内存访问的问题 [#8604](https://github.com/pingcap/tiflash/issues/8604) @[windtalker](https://github.com/windtalker)
    - 修复在执行 PITR 恢复任务或 `FLASHBACK CLUSTER TO` 后，TiFlash 副本数据可能被意外删除，导致数据异常的问题 [#8777](https://github.com/pingcap/tiflash/issues/8777) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复当 TiFlash Anti Semi Join 存在非等值连接条件时，可能出现错误结果的问题 [#8791](https://github.com/pingcap/tiflash/issues/8791) @[windtalker](https://github.com/windtalker)

+ Tools

    + Backup & Restore (BR)

        - 修复由于某个 TiKV 节点缺少 Leader 导致数据恢复变慢的问题 [#50566](https://github.com/pingcap/tidb/issues/50566) @[Leavrth](https://github.com/Leavrth)
        - 修复全量恢复指定 `--filter` 选项后，仍然要求目标集群为空的问题 [#51009](https://github.com/pingcap/tidb/issues/51009) @[3pointer](https://github.com/3pointer)
        - 修复数据恢复失败后，使用断点重启报错 `the target cluster is not fresh` 的问题 [#50232](https://github.com/pingcap/tidb/issues/50232) @[Leavrth](https://github.com/Leavrth)
        - 修复停止日志备份任务导致 TiDB crash 的问题 [#50839](https://github.com/pingcap/tidb/issues/50839) @[YuJuncen](https://github.com/YuJuncen)
        - 修复从旧版本的备份恢复数据时报错 `Unsupported collation` 的问题 [#49466](https://github.com/pingcap/tidb/issues/49466) @[3pointer](https://github.com/3pointer)
        - 修复在任务初始化阶段出现与 PD 的连接错误导致日志备份任务虽然启动但无法正常工作的问题 [#16056](https://github.com/tikv/tikv/issues/16056) @[YuJuncen](https://github.com/YuJuncen)
        - 修复生成外部存储文件 URI 错误的问题 [#48452](https://github.com/pingcap/tidb/issues/48452) @[3AceShowHand](https://github.com/3AceShowHand)
        - 修复在同一节点上更改 TiKV IP 地址导致日志备份卡住的问题 [#50445](https://github.com/pingcap/tidb/issues/50445) @[3pointer](https://github.com/3pointer)
        - 修复从 S3 读文件内容时出错后无法重试的问题 [#49942](https://github.com/pingcap/tidb/issues/49942) @[Leavrth](https://github.com/Leavrth)

    + TiCDC

        - 修复开启 Syncpoint 时 (`enable-sync-point = true`)，sink 模块遇到错误后无法正确重启的问题 [#10091](https://github.com/pingcap/tiflow/issues/10091) @[hicqu](https://github.com/hicqu)
        - 修复使用 storage sink 时，在存储服务生成的文件序号可能出现回退的问题 [#10352](https://github.com/pingcap/tiflow/issues/10352) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - 修复 Syncpoint 表可能被错误同步的问题 [#10576](https://github.com/pingcap/tiflow/issues/10576) @[asddongmen](https://github.com/asddongmen)
        - 修复当使用 Apache Pulsar 作为下游时，无法正常启用 OAuth2.0、TLS 和 mTLS 的问题 [#10602](https://github.com/pingcap/tiflow/issues/10602) @[asddongmen](https://github.com/asddongmen)
        - 修复并发创建多个 changefeed 时 TiCDC 返回 `ErrChangeFeedAlreadyExists` 错误的问题 [#10430](https://github.com/pingcap/tiflow/issues/10430) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - 修复在极端情况下 changefeed 的 `resolved ts` 不推进的问题 [#10157](https://github.com/pingcap/tiflow/issues/10157) @[sdojjy](https://github.com/sdojjy)
        - 修复在某些特殊场景下，TiCDC 错误地关闭与 TiKV 的连接的问题 [#10239](https://github.com/pingcap/tiflow/issues/10239) @[hicqu](https://github.com/hicqu)
        - 修复同步数据到对象存储时，可能会出现 TiCDC Server panic 的问题 [#10137](https://github.com/pingcap/tiflow/issues/10137) @[sdojjy](https://github.com/sdojjy)
        - 修复上游表执行了 `TRUNCATE PARTITION` 后 changefeed 报错的问题 [#10522](https://github.com/pingcap/tiflow/issues/10522) @[sdojjy](https://github.com/sdojjy)
        - 修复在 `ignore-event` 中设置了过滤掉 `add table partition` 事件后，TiCDC 未将相关分区的其它类型 DML 变更事件同步到下游的问题 [#10524](https://github.com/pingcap/tiflow/issues/10524) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - 修复 `kv-client` 初始化过程中可能出现数据竞争的问题 [#10095](https://github.com/pingcap/tiflow/issues/10095) @[3AceShowHand](https://github.com/3AceShowHand)

    + TiDB Data Migration (DM)

        - 修复下游表结构包含 `shard_row_id_bits` 时同步任务报错的问题 [#10308](https://github.com/pingcap/tiflow/issues/10308) @[GMHDBJD](https://github.com/GMHDBJD)
        - 修复 DM 遇到 `event type truncate not valid` 错误导致升级失败的问题 [#10282](https://github.com/pingcap/tiflow/issues/10282) @[GMHDBJD](https://github.com/GMHDBJD)
