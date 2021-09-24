---
title: TiDB 5.0.4 Release Notes
---

# TiDB 5.0.4 Release Notes

发版日期：2021 年 9 月 27 日

TiDB 版本：5.0.4

## 兼容性更改

+ TiDB

    - 修复在新会话中执行 `SHOW VARIABLES` 速度较慢的问题。该修复回退了 [#19341](https://github.com/pingcap/tidb/pull/19341) 中的部分更改，可能会引起兼容性问题。[#24326](https://github.com/pingcap/tidb/issues/24326)
    - 将系统变量 `tidb_stmt_summary_max_stmt_count` 的默认值从 `200` 修改为 `3000` [#25873](https://github.com/pingcap/tidb/pull/25873)
    + 以下 Bug 修复涉及执行结果变化，可能引起兼容性变化，对业务造成影响：
        - 修复了当 `UNION` 的子计划包含 `NULL` 值时 TiDB 返回错误结果的问题 [#26559](https://github.com/pingcap/tidb/issues/26559)
        - 修复了 `greatest(datetime) union null` 返回空字符串的问题 [#26532](https://github.com/pingcap/tidb/issues/26532)
        - 修复了 `last_day` 函数的行为在 SQL 模式下不兼容的问题 [#26000](https://github.com/pingcap/tidb/pull/26000)
        - 修复了 `having` 可能执行错误的问题 [#26496](https://github.com/pingcap/tidb/issues/26496)
        - 修复了当 `between` 表达式两边的 collation 不一致会导致查询结果错误的问题 [#27146](https://github.com/pingcap/tidb/issues/27146)
        - 修复了当 `group_concat` 函数包含非 `bin` 的 collation 时查询结果错误的问题 [#27429](https://github.com/pingcap/tidb/issues/27429)
        - 修复了当开启 New Collation 时，在多列上执行 `count(distinct)` 表达式结果错误的问题 [#27091](https://github.com/pingcap/tidb/issues/27091)
        - 修复了 `extract` 函数的参数是负数时查询结果错误的问题 [#27236](https://github.com/pingcap/tidb/issues/27236)
        - 修复了当 `SQL_MODE` 为 'STRICT_TRANS_TABLES' 时，插入非法时间不报错的问题 [#26762](https://github.com/pingcap/tidb/issues/26762)
        - 修复了当 `SQL_MODE` 为 'NO_ZERO_IN_DATE' 时，使用非法的默认时间不报错的问题 [#26766](https://github.com/pingcap/tidb/issues/26766)
        - 修复了索引前缀的查询范围问题 [#26029](https://github.com/pingcap/tidb/issues/26029)
        - 修复了 `LOAD DATA` 语句可能会异常导入非 utf8 数据的问题 [#25979](https://github.com/pingcap/tidb/issues/25979)
        - 修复了当二级索引包含主键中的列时，`insert ignore on duplicate update` 可能插入错误数据的问题 [#25809](https://github.com/pingcap/tidb/issues/25809)
        - 修复了当分区表有聚簇索引时，`insert ignore duplicate update` 可能插入错误数据的问题 [#25846](https://github.com/pingcap/tidb/issues/25846)
        - 修复了当 point get 或 batch point get 的查找键是 `ENUM` 类型时，查询结果可能错误的问题 [#24562](https://github.com/pingcap/tidb/issues/24562)
        - 修复了 `BIT` 类型做除法时查询结果不正确的问题 [#23479](https://github.com/pingcap/tidb/issues/23479)
        - 修复了 `prepared` 语句和直接查询的结果可能不一致的问题 [#22949](https://github.com/pingcap/tidb/issues/22949)
        - 修复了当 `YEAR` 类型与字符串或整数类型比较时，结果可能错误的问题 [#23262](https://github.com/pingcap/tidb/issues/23262)

## 功能增强

+ TiDB

    - 支持将系统变量 `tidb_enforce_mpp` 的值设为 `1` 以忽略优化器代价估算，强制使用 MPP 模式 [#26382](https://github.com/pingcap/tidb/pull/26382)

+ TiKV

    - 支持动态修改 TiCDC 配置 [#10645](https://github.com/tikv/tikv/issues/10645)

+ PD

    - 为 TiDB Dashboard 增加基于 OIDC 的 SSO 支持 [#3884](https://github.com/tikv/pd/pull/3884)

+ TiFlash

    - 支持 `HAVING()` 函数
    - 支持 `DATE()` 函数
    - 为 Grafana 面板增加每个实例的写入吞吐

## 提升改进

+ TiDB

    - 基于直方图的 row count 来触发 auto-analyze [#24237](https://github.com/pingcap/tidb/issues/24237)
    - 当一个 TiFlash 节点此前因宕机重启过，TiDB 一段时间内不给该节点发送请求 [#26757](https://github.com/pingcap/tidb/pull/26757)
    - 增加 `split region` 的速度限制，使 `split table` 和 `presplit` 更稳定 [#22969](https://github.com/pingcap/tidb/issues/22969)
    - 支持 MPP 查询的重试 [#26483](https://github.com/pingcap/tidb/pull/26483)
    - 在发起 MPP 查询之前检查 TiFlash 的可用性 [#1807](https://github.com/pingcap/tics/issues/1807)
    - 支持稳定结果模式，使查询结果更稳定 [#26084](https://github.com/pingcap/tidb/pull/26084)
    - 支持 MySQL 系统变量 `init_connect` 及相关功能 [#18894](https://github.com/pingcap/tidb/issues/18894)
    - 在 MPP 模式下彻底下推 `COUNT(DISTINCT)` 聚合函数 [#25861](https://github.com/pingcap/tidb/pull/25861)
    - 当聚合函数在 `EXPLAIN` 语句中不能被下推时打印警告日志 [#25736](https://github.com/pingcap/tidb/pull/25736)
    - 在 Grafana 监控中给 `TiFlashQueryTotalCounter` 加上错误标签 [#25327](https://github.com/pingcap/tidb/pull/25327)
    - 支持在 HTTP API 中通过二级索引查询聚簇索引表的 MVCC 数据 [#24209](https://github.com/pingcap/tidb/issues/24209)
    - 优化 `prepared` 语句在解析器的内存分配 [#24371](https://github.com/pingcap/tidb/pull/24371)

+ TiKV

    - 分离处理读写的 ready 状态以减少读延迟 [#10475](https://github.com/tikv/tikv/issues/10475)
    - 减少 Resolved TS 消息的大小以节省网络带宽 [#2448](https://github.com/pingcap/ticdc/issues/2448)
    - 当 slogger 线程过载且队列已满时，删除日志而不是阻塞线程 [#10841](https://github.com/tikv/tikv/issues/10841)
    - TiKV Coprocessor 慢日志只考虑处理请求所花费的时间 [#10841](https://github.com/tikv/tikv/issues/10841)
    - 使预写尽可能具有幂等性，以减少出现未确定错误的可能 [#10587](https://github.com/tikv/tikv/pull/10587)
    - 避免在低写入流量下误报 "GC can not work" [#10662](https://github.com/tikv/tikv/pull/10662)
    - 数据库在备份时总是与原始集群大小相匹配 [#10643](https://github.com/tikv/tikv/pull/10643)
    - 确保 Panic 信息刷新到日志 [#9955](https://github.com/tikv/tikv/pull/9955)

+ PD

    - 提升了 PD 之间同步 Region 信息的性能 [#3993](https://github.com/tikv/pd/pull/3993)

+ Tools

    + Dumpling

        - 支持对 MySQL 兼容的特定数据库进行备份，这些数据库不支持 `START TRANSACTION ... WITH CONSISTENT SNAPSHOT` 和 `SHOW CREATE TABLE` 语法 [#309](https://github.com/pingcap/dumpling/issues/309)

    + TiCDC

        - 优化 Unified Sorter 使用内存排序时的内存管理 [#2553](https://github.com/pingcap/ticdc/issues/2553)
        - 禁止使用不同的 major 和 minor 版本启动 TiCDC 节点 [#2598](https://github.com/pingcap/ticdc/pull/2598)
        - 当某张表的 Region 从某个 TiKV 节点全部迁移走时，减少 goroutine 资源的使用 [#2284](https://github.com/pingcap/ticdc/issues/2284)
        - 移除 `file sorter` 文件排序器 [#2326](https://github.com/pingcap/ticdc/pull/2326)
        - 总是从 TiKV 获取行变更的历史值 (old value)，输出会根据 `enable-old-value` 配置进行调整 [#2301](https://github.com/pingcap/ticdc/issues/2301)
        - 优化连接 PD 时缺少证书情况下的报错提示 [#1973](https://github.com/pingcap/ticdc/issues/1973)
        - 在高并发下减少 workerpool 中创建的 goroutine 数量 [#2211](https://github.com/pingcap/ticdc/issues/2211)
        - 为所有 KV 客户端创建全局共享的 gRPC 连接池 [#2533](https://github.com/pingcap/ticdc/pull/2533)

## Bug 修复

+ TiDB

    - 修复了当查询分区表且分区键带有 `IS NULL` 条件时，TiDB 可能 panic 的问题 [#23802](https://github.com/pingcap/tidb/issues/23802)
    - 修复了 `FLOAT64` 类型的溢出检查与 MySQL 不一致的问题 [#23897](https://github.com/pingcap/tidb/issues/23897)
    - 修复了 `case when` 表达式的字符集和排序规则错误的问题 [#26662](https://github.com/pingcap/tidb/issues/26662)
    - 修复了提交悲观事务可能会导致写冲突的问题 [#25964](https://github.com/pingcap/tidb/issues/25964)
    - 修复了在悲观事务中索引键值可能会被重复提交的问题 [#26359](https://github.com/pingcap/tidb/issues/26359) [#10600](https://github.com/tikv/tikv/pull/10600)
    - 修复了清除 Async Commit 锁时可能会导致 TiDB panic 的问题 [#25778](https://github.com/pingcap/tidb/issues/25778)
    - 修复了使用 `INDEX MERGE` 时可能找不到列的问题 [#25045](https://github.com/pingcap/tidb/issues/25045)
    - 修复了使用 `ALTER USER REQUIRE SSL` 会清空用户的 `authentication_string` 的问题 [#25225](https://github.com/pingcap/tidb/issues/25225)
    - 修复了新集群上系统变量 `tidb_gc_scan_lock_mode` 的值显示为 "PHYSICAL" 而实际是 "LEGACY" 的问题 [#25100](https://github.com/pingcap/tidb/issues/25100)
    - 修复了系统表 `TIKV_REGION_PEERS` 没有正确显示 `DOWN` 状态的问题 [#24879](https://github.com/pingcap/tidb/issues/24879)
    - 修复了使用 HTTP API 时导致内存泄漏的问题 [#24649](https://github.com/pingcap/tidb/pull/24649)
    - 修复了视图不支持 `DEFINER` 的问题 [#24414](https://github.com/pingcap/tidb/issues/24414)
    - 修复了 `tidb-server --help` 退出状态是 `2` 的问题 [#24046](https://github.com/pingcap/tidb/issues/24046)
    - 修复了设置全局系统变量 `dml_batch_size` 不生效的问题 [#24709](https://github.com/pingcap/tidb/issues/24709)
    - 修复了同时使用 `read_from_storage` 和分区表会报错的问题 [#20372](https://github.com/pingcap/tidb/issues/20372)
    - 修复了 TiDB 在执行投影算子时会 Panic 的问题 [#24264](https://github.com/pingcap/tidb/issues/24264)
    - 修复了统计信息可能导致查询 Panic 的问题 [#24061](https://github.com/pingcap/tidb/pull/24061)
    - 修复了在 `BIT` 类型的列上使用 `approx_percentile` 函数可能 Panic 的问题 [#23662](https://github.com/pingcap/tidb/issues/23662)
    - 修复了 Grafana 上 `Coprocessor Cache` 面板的数据显示不正确的问题 [#26338](https://github.com/pingcap/tidb/issues/26338)
    - 修复了并发 truncate 同一个分区会导致 DDL 语句执行卡住的问题 [#26229](https://github.com/pingcap/tidb/issues/26229)
    - 修复当会话变量用作 `GROUP BY` 项时查询结果出错的问题 [#27106](https://github.com/pingcap/tidb/issues/27106)
    - 修复连接表时 `VARCHAR` 类型与时间戳之间错误的隐式转换 [#25902](https://github.com/pingcap/tidb/issues/25902)
    - 修复相关子查询语句中的错误结果 [#27233](https://github.com/pingcap/tidb/issues/27233)

+ TiKV

    ?- 修复当有快照文件未被 GC 回收时，快照在 GC 的过程中可能遗留 GC 快照文件的问题 [#10813](https://github.com/tikv/tikv/issues/10813)
    - 修复了 TiKV 在启用 Titan 并从 5.0 以前的版本升级时出现 Panic 的问题 [#10843](https://github.com/tikv/tikv/pull/10843)
    - 修复了高版本的 TiKV 无法回滚到 v5.0.x 的问题 [#10843](https://github.com/tikv/tikv/pull/10843)
    - 修复了启用 Titan 并从 v5.0 以前的版本升级到 v5.0 及以后的版本时 TiKV 崩溃的问题（例如，如果集群从 TiKV v3.x 升级并在升级之前启用了 Titan，则该集群可能会遇到该问题）[#10774](https://github.com/tikv/tikv/issues/10774)
    - 修复了遗留的悲观锁导致的解析失败的问题 [#26404](https://github.com/pingcap/tidb/issues/26404)
    - 修复在某些平台上计算时间间隔出现 Panic 的问题 [#10571](https://github.com/tikv/tikv/pull/10571)
    - 修复 Load Base Split 中 `batch_get_command` 的键值未编码问题 [#10542](https://github.com/tikv/tikv/issues/10542)

+ PD

    - 修复 PD 未能及时修复 Down Peer 副本的问题 [#4077](https://github.com/tikv/pd/issues/4077)
    - 修复了 `replication.max-replicas` 更新后默认的 Placement Rules 副本数量不变的问题 [#3886](https://github.com/tikv/pd/issues/3886)
    - 修复了 PD 在扩容 TiKV 时可能会 Panic 的问题 [#3868](https://github.com/tikv/pd/issues/3868)
    - 修复多个调度器运行时会造成调度冲突的问题 [#3807](https://github.com/tikv/pd/issues/3807)
    - 修复了删除调度器后调度器可能再次出现的问题 [#2572](https://github.com/tikv/pd/issues/2572)

+ TiFlash

    - 修复执行扫表任务时潜在的进程崩溃问题
    - 修复执行 MPP 任务时潜在的内存泄漏问题
    - 修复处理 DAG 请求时出现 `duplicated region` 报错的问题
    - 修复执行 `COUNT` 或 `COUNT DISTINCT` 函数时出现非预期结果的问题
    - 修复执行 MPP 任务时潜在的进程崩溃问题
    - 修复 TiFlash 多盘部署时无法恢复数据的潜在问题
    - 修复析构 `SharedQueryBlockInputStream` 时出现进程崩溃的潜在问题
    - 修复析构 `MPPTask` 时出现进程崩溃的潜在问题
    - 修复 TiFlash 无法建立 MPP 连接时出现非预期结果的问题
    - 修复解锁时潜在的进程崩溃问题
    - 修复写入压力大时 metrics 中 store size 不准确的问题
    - 修复当查询过滤条件包含诸如 `CONSTANT` `<` | `<=` | `>` | `>=` `COLUMN` 时出现错误结果的问题
    - 修复 TiFlash 长时间运行后无法回收 Delta 数据的潜在问题
    - 修复 metrics 显示错误数值的潜在问题
    - 修复多盘部署时数据不一致的潜在问题

+ Tools

    + Dumpling

        - 修复在 MySQL 8.0.3 或更高版本执行 `show table status` 语句卡住的问题 [#322](https://github.com/pingcap/dumpling/issues/322)

    + TiCDC

        - 修复将 `mysql.TypeString, mysql.TypeVarString, mysql.TypeVarchar` 等类型的数据编码为 JSON 时进程崩溃的问题 [#2758](https://github.com/pingcap/ticdc/issues/2758)
        - 修复重新调度一张表时多个处理器将数据写入同一张表引发的数据不一致的问题 [#2417](https://github.com/pingcap/ticdc/pull/2417)
        - 降低 gRPC 窗口大小来避免 Region 数量过多时触发内存溢出 [#2724](https://github.com/pingcap/ticdc/pull/2724)
        - 修复内存压力大时 gRPC 连接频繁断开的错误 [#2202](https://github.com/pingcap/ticdc/issues/2202)
        - 修复 TiCDC 在处理无符号 `TINYINT` 类型时崩溃的问题 [#2648](https://github.com/pingcap/ticdc/issues/2648)
        - 修复 TiCDC Open Protocol 在上游插入事务并删除同一行数据的情况下输出空值的问题 [#2612](https://github.com/pingcap/ticdc/issues/2612)
        - 修复同步任务从一个表结构变更的 finish TS 开始时 DDL 处理失败的问题 [#2603](https://github.com/pingcap/ticdc/issues/2603)
        - 修复无响应的下游中断 old owner 中的同步任务直到该任务超时的问题 [#2295](https://github.com/pingcap/ticdc/issues/2295)
        - 修复元信息管理问题 [#2558](https://github.com/pingcap/ticdc/pull/2558)
        - 修复 sink Close 不正确导致多个节点写同一张表的问题 [#2230](https://github.com/pingcap/ticdc/issues/2230)
        - 修复 `capture list` 命令输出中出现已过期 capture 的问题 [#2388](https://github.com/pingcap/ticdc/issues/2388)
        - 修复集成测试中遇到的由于 DDL Job 重复导致的 `ErrSchemaStorageTableMiss` 错误 [#2422](https://github.com/pingcap/ticdc/issues/2422)
        - 修复遇到 `ErrGCTTLExceeded` 错误时 changefeed 无法被删除的问题 [#2391](https://github.com/pingcap/ticdc/issues/2391)
        - 修复同步数据量大的表到 cdclog 失败的问题 [#1259](https://github.com/pingcap/ticdc/issues/1259) [#2424](https://github.com/pingcap/ticdc/issues/2424)
        - 修复客户端向后兼容性问题 [#2373](https://github.com/pingcap/ticdc/issues/2373)
        - 修复 `SinkManager` 中对 map 的不安全并发访问 [#2299](https://github.com/pingcap/ticdc/pull/2299)
        - 修复 owner 在执行 DDL 语句时崩溃可能导致 DDL 任务丢失的问题 [#1260](https://github.com/pingcap/ticdc/issues/1260)
        - 修复在 Region 初始化时立刻执行清锁的问题 [#2188](https://github.com/pingcap/ticdc/issues/2188)
        - 修复创建新的分区表时部分分区被重复分发的问题 [#2263](https://github.com/pingcap/ticdc/pull/2263)
        - 修复同步任务已删除但 TiCDC 持续报警的问题 [#2156](https://github.com/pingcap/ticdc/issues/2156)
