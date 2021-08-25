---
title: TiDB 4.0 RC.2 Release Notes
---

# TiDB 4.0 RC.2 Release Notes

发版日期：2020 年 5 月 15 日

TiDB 版本：4.0.0-rc.2

## 兼容性变化

+ TiDB

    - 去掉了特别为开启 Binlog 时定义的事务容量上限 (100 MB)，现在事务的容量上限统一为 10 GB，但若开启 Binlog 且下游是 Kafka，由于 Kafka 消息大小的限制是 1 GB，请根据情况调整 `txn-total-size-limit` 配置参数 [#16941](https://github.com/pingcap/tidb/pull/16941)
    - 查询 `CLUSTER_LOG` 表时，如果未指定时间范围，由默认时间范围变更为返回错误且用户必须指定时间范围 [#17003](https://github.com/pingcap/tidb/pull/17003)
    - `CREATE TABLE` 创建分区表时指定未支持的 sub-partition 或 linear hash 选项，将会创建非分区普通表，而不是选项未生效的分区表 [#17197](https://github.com/pingcap/tidb/pull/17197)

+ TiKV

    - 将加密相关的配置移到 security 分类下，即调整配置项 `[encryption]` 为 `[security.encryption]` [#7810](https://github.com/tikv/tikv/pull/7810)

+ Tools

    + TiDB Lightning

        - 导入数据时将 SQL Mode 由默认改成 `ONLY_FULL_GROUP_BY,NO_AUTO_CREATE_USER`，提高兼容性 [#316](https://github.com/pingcap/tidb-lightning/pull/316)
        - 在 tidb-backend 模式下禁止访问 PD 或者 TiKV 端口 [#312](https://github.com/pingcap/tidb-lightning/pull/312)
        - 日志信息默认输出到 tmp 文件且在启动时输出 tmp 文件的路径 [#313](https://github.com/pingcap/tidb-lightning/pull/313)

## 重点修复的 Bug

+ TiDB

    - 修复当 `WHERE` 语句只有一个等值条件时错误选择分区表分区的问题 [#17054](https://github.com/pingcap/tidb/pull/17054)
    - 修复当 `WHERE` 语句只包含字符串列时构造错误的 Index Range 导致结果错误的问题 [#16660](https://github.com/pingcap/tidb/pull/16660)
    - 修复事务中执行 `DELETE` 之后再进行唯一索引点查语句 Panic 的问题 [#16991](https://github.com/pingcap/tidb/pull/16991)
    - 修复 GC worker 在有错误发生时可能死锁的问题 [#16915](https://github.com/pingcap/tidb/pull/16915)
    - 避免 TiKV 未宕机仅响应慢情况下的无故 RegionMiss 重试 [#16956](https://github.com/pingcap/tidb/pull/16956)
    - 修改客户端 MySQL 协议握手阶段日志级别为 `DEBUG`，以解决干扰日志输出的问题 [#16881](https://github.com/pingcap/tidb/pull/16881)
    - 修复 `TRUNCATE` 后未按照表定义的 `PRE_SPLIT_REGIONS` 信息进行预切分 Region 的问题 [#16776](https://github.com/pingcap/tidb/pull/16776)
    - 修复两阶段提交中第二阶段遇到 TiKV 不可用重试导致的 Goroutine 暴涨的问题 [#16876](https://github.com/pingcap/tidb/pull/16876)
    - 修复部分表达式不能下推可能导致语句执行 Panic 的问题 [#16869](https://github.com/pingcap/tidb/pull/16869)
    - 修复 IndexMerge 在分区表上执行结果错误的问题 [#17124](https://github.com/pingcap/tidb/pull/17124)
    - 修复因 Memory Tracker 锁竞争引起的宽表性能回退问题 [#17234](https://github.com/pingcap/tidb/pull/17234)

+ TiFlash

    - 修复库名、表名含特殊字符，系统升级后无法正常启动的问题

## 新功能

+ TiDB

    - 新增 `BACKUP` 和 `RESTORE` 语句进行备份与恢复 [#16960](https://github.com/pingcap/tidb/pull/16960)
    - 支持在提交前预检查单个 Region 提交数据量，并在超过阈值时预切分 Region 后再进行提交 [#16959](https://github.com/pingcap/tidb/pull/16959)
    - 新增 Session 作用域变量 `LAST_PLAN_FROM_CACHE`，用于指示上一条语句是否命中 Plan Cache [#16830](https://github.com/pingcap/tidb/pull/16830)
    - 支持在慢日志和 `SLOW_LOG` 表中记录 `Cop_time` 信息 [#16904](https://github.com/pingcap/tidb/pull/16904)
    - 支持在 Grafana 中展示更多 Go Runtime 内存监控指标 [#16928](https://github.com/pingcap/tidb/pull/16928)
    - 支持在 General Log 中输出 `forUpdateTS` 和 `Read Consistency` 隔离级别信息 [#16946](https://github.com/pingcap/tidb/pull/16946)
    - 支持对 TiKV Region Resolve Lock 请求进行去重 [#16925](https://github.com/pingcap/tidb/pull/16925)
    - 支持 `SET CONFIG` 语句进行 PD/TiKV 节点配置修改 [#16853](https://github.com/pingcap/tidb/pull/16853)
    - 支持在 `CREATE TABLE` 语句中指定 `auto_random` 选项 [#16813](https://github.com/pingcap/tidb/pull/16813)
    - 通过为 DistSQL 请求分配 TaskID 让 TiKV 更好地调度处理请求 [#17155](https://github.com/pingcap/tidb/pull/17155)
    - 支持在 MySQL 客户端登录后显示 TiDB server 版本信息 [#17187](https://github.com/pingcap/tidb/pull/17187)
    - 支持在 `GROUP_CONCAT` 中指定 `ORDER BY` 子句 [#16990](https://github.com/pingcap/tidb/pull/16990)
    - 支持在 Slow Log 中展示 `Plan_from_cache` 信息，用于指示语句是否命中 Plan Cache [#17121](https://github.com/pingcap/tidb/pull/17121)
    - Dashboard 支持显示 TiFlash 多盘部署容量信息功能
    - Dashboard 支持通过 SQL 查询 TiFlash 日志的功能

+ TiKV

    - 加密存储适配 tikv-ctl，适配后开启加密存储后通过 tikv-ctl 操作管理集群 [#7698](https://github.com/tikv/tikv/pull/7698)
    - 新增加密码 Snapshot 中的 `lock column famliy` 的功能 [#7712](https://github.com/tikv/tikv/pull/7712)
    - 修改 Raftstore latency 在 Grafana 面板显示方式，采用 heatmap 方便诊断性能抖动问题 [#7717](https://github.com/tikv/tikv/pull/7717)
    - 支持配置 gRPC 消息大小的上限 [#7824](https://github.com/tikv/tikv/pull/7824)
    - Grafana 面板中添加了 encryption 相关的监控 [#7827](https://github.com/tikv/tikv/pull/7827)
    - TiKV 支持 ALPN 协议 [#7825](https://github.com/tikv/tikv/pull/7825)
    - 添加了更多的关于 Titan 的统计信息 [#7818](https://github.com/tikv/tikv/pull/7818)
    - 统一线程池支持用客户端提供的 task ID 来区分任务，以避免一个请求被来自同一个事务的另一个请求降低优先级 [#7814](https://github.com/tikv/tikv/pull/7814)
    - 提升了 batch insert 请求的性能 [#7718](https://github.com/tikv/tikv/pull/7718)

+ PD

    - 下线节点时放开 Remove peer 的速度 [#2372](https://github.com/pingcap/pd/pull/2372)

+ TiFlash

    - 调整 Grafana 中 Read Index 的 Count 图表的名称为 Ops
    - 优化系统负载较低时打开文件描述符的数据，降低系统资源占用量
    - 新增 capacity 配置参数用于限制存储数据容量

+ Tools

    - TiDB Lightning

        - tidb-lightning-ctl 新增 `fetch-mode` 子命令，输出 TiKV 集群模式 [#287](https://github.com/pingcap/tidb-lightning/pull/287)

    - TiCDC

        - 支持通过 `cdc cli` 来管理同步任务 (changefeed) [#546](https://github.com/pingcap/ticdc/pull/546)

    - Backup & Restore (BR)

        - 支持备份时候自动调整 GC 时间 [#257](https://github.com/pingcap/br/pull/257)
        - 优化恢复数据时的 PD 参数，以加速恢复 [#198](https://github.com/pingcap/br/pull/198)

## Bug 修复

+ TiDB

    - 完善多个算子中判断是否使用向量化进行表达式执行的逻辑 [#16383](https://github.com/pingcap/tidb/pull/16383)
    - 修复 IndexMerge Hint 未能正确检查数据库名称的问题 [#16932](https://github.com/pingcap/tidb/pull/16932)
    - 修复 Sequence 可以被 `TRUNCATE` 的问题 [#17037](https://github.com/pingcap/tidb/pull/17037)
    - 修复 Sequence 可以被 `INSERT`/`UPDATE`/`ANALYZE`/`DELETE` 的问题 [#16957](https://github.com/pingcap/tidb/pull/16957)
    - 修复启动阶段执行的内部 SQL 在 Statement Summary 表中未能正确记录为内部 SQL 的问题 [#17062](https://github.com/pingcap/tidb/pull/17062)
    - 修复因 TiFlash 支持但 TiKV 不支持的过滤条件仅被下推到 IndexLookupJoin 算子之下导致的语句报错问题 [#17036](https://github.com/pingcap/tidb/pull/17036)
    - 修复开启 Collation 后，`LIKE` 表达式可能出现的并发问题 [#16997](https://github.com/pingcap/tidb/pull/16997)
    - 修复开启 Collation 后，`LIKE` 函数无法正确构造 Range 查询索引的问题 [#16783](https://github.com/pingcap/tidb/pull/16783)
    - 修复触发填充 Plan Cache 语句后执行 `@@LAST_PLAN_FROM_CACHE` 返回值错误的问题 [#16831](https://github.com/pingcap/tidb/pull/16831)
    - 修复为 IndexMerge 计算候选路径时漏掉 Index 上的 `TableFilter` 的问题 [#16947](https://github.com/pingcap/tidb/pull/16947)
    - 修复使用 MergeJoin Hint 并存在 TableDual 算子时无法产生物理查询计划的问题 [#17016](https://github.com/pingcap/tidb/pull/17016)
    - 修复 Statement Summary 表的 `Stmt_Type` 列值大小写错误的问题 [#17018](https://github.com/pingcap/tidb/pull/17018)
    - 修复因不同用户使用相同的 tmp-storage-path 导致服务无法启动报 `Permission Denied` 错误问题 [#16996](https://github.com/pingcap/tidb/pull/16996)
    - 修复返回结果类型由多个输入列决定的表达式（例如：`CASE WHEN`）结果类型 `NotNullFlag` 标识推导不正确的问题 [#16995](https://github.com/pingcap/tidb/pull/16995)
    - 修复 Green GC 在有 Dirty Store 的情况下可能遗留锁的问题 [#16949](https://github.com/pingcap/tidb/pull/16949)
    - 修复 Green GC 在遇到单个 key 有多个不同锁的情况下会遗留下锁的问题 [#16948](https://github.com/pingcap/tidb/pull/16948)
    - 修复 `INSERT VALUE` 中子查询引用父查询列导致插入值错误的问题 [#16952](https://github.com/pingcap/tidb/pull/16952)
    - 修复对 Float 值进行 `AND` 操作结果不正的问题 [#16666](https://github.com/pingcap/tidb/pull/16666)
    - 修复 Expensive Log 日志中 `WAIT_TIME` 字段信息错误的问题 [#16907](https://github.com/pingcap/tidb/pull/16907)
    - 修复悲观事务模式执行语句 `SELECT FOR UPDATE` 不能被记录到 Slow Log 的问题 [#16897](https://github.com/pingcap/tidb/pull/16897)
    - 修复在 `Enum` 或 `Set` 类型列上执行 `SELECT DISTINCT` 时结果错误的问题 [#16892](https://github.com/pingcap/tidb/pull/16892)
    - 修复 `auto_random_base` 在 `SHOW CREATE TABLE` 的显示问题 [#16864](https://github.com/pingcap/tidb/pull/16864)
    - 修复 `WHERE string_value` 结果不正确的问题 [#16559](https://github.com/pingcap/tidb/pull/16559)
    - 修复 `GROUP BY` Window Function 错误消息和 MySQL 不一致问题 [#16165](https://github.com/pingcap/tidb/pull/16165)
    - 修复 `FLASH TABLE` 语句在数据库名有大写字母时执行失败的问题 [#17167](https://github.com/pingcap/tidb/pull/17167)
    - 修复 Projection 执行器内存消耗记录不准确的问题 [#17118](https://github.com/pingcap/tidb/pull/17118)
    - 修复 `SLOW_QUERY` 表在不同时区下时间过滤不正确的问题 [#17164](https://github.com/pingcap/tidb/pull/17164)
    - 修复 IndexMerge 和虚拟生成列一起使用时 Panic 的问题 [#17126](https://github.com/pingcap/tidb/pull/17126)
    - 修复 `INSTR` 和 `LOCATE` 函数大小写问题 [#17068](https://github.com/pingcap/tidb/pull/17068)
    - 修复开启 `tidb_allow_batch_cop` 配置后频繁出现 `tikv server timeout` 错误的问题 [#17161](https://github.com/pingcap/tidb/pull/17161)
    - 修复 Float 类型进行 `XOR` 操作结果和 MySQL 8.0 不一致的问题 [#16978](https://github.com/pingcap/tidb/pull/16978)
    - 修复 `ALTER TABLE REORGANIZE PARTITION` 不支持但执行未报错的问题 [#17178](https://github.com/pingcap/tidb/pull/17178)
    - 修复 `EXPLAIN FORMAT="dot"  FOR CONNECTION ID` 可能遇到不支持展示的 Plan 发生报错的问题 [#17160](https://github.com/pingcap/tidb/pull/17160)
    - 修复 Prepared Statement 在 Statement Summary 表中 `EXEC_COUNT` 列的记录问题 [#17086](https://github.com/pingcap/tidb/pull/17086)
    - 修复设置 Statement Summary 系统变量时未检查值是否合法的问题 [#17129](https://github.com/pingcap/tidb/pull/17129)
    - 修复启用 Plan Cache 时使用越界值查询 `UNSIGNED BIGINT` 主键报错的问题 [#17120](https://github.com/pingcap/tidb/pull/17120)
    - 修复 Grafana TiDB Summary 面板基于机器实例和请求类型展示 QPS 不正确的问题 [#17105](https://github.com/pingcap/tidb/pull/17105)

+ TiKV

    - 修复 restore 后生成大量空 Region 的问题 [#7632](https://github.com/tikv/tikv/pull/7632)
    - 修复 Raftstore 收到乱序 read index 响应时会引发 panic 的问题 [#7370](https://github.com/tikv/tikv/pull/7370)
    - 修复启用统一线程池时，不会验证 storage 或 `coprocessor read pool` 配置是否无效的问题 [#7513](https://github.com/tikv/tikv/pull/7513)
    - 修复 TiKV server 关闭时，join 可能 panic 的问题 [#7713](https://github.com/tikv/tikv/pull/7713)
    - 修复通过诊断 API 搜索慢日志无返回结果的问题 [#7776](https://github.com/tikv/tikv/pull/7776)
    - 修复节点长时间运行时，系统会产生较多内存碎片的问题 [#7556](https://github.com/tikv/tikv/pull/7556)
    - 修复部分情况下因存储无效日期导致 SQL 执行失败的问题 [#7268](https://github.com/tikv/tikv/pull/7268)
    - 修复从 GCS 进行恢复数据不能正确运行的问题 [#7739](https://github.com/tikv/tikv/pull/7739)
    - 修复存储加密时未进行 KMS Key Id 验证的问题 [#7719](https://github.com/tikv/tikv/pull/7719)
    - 修复 Coprocessor 在不同架构编译器下潜在正确性问题 [#7714](https://github.com/tikv/tikv/pull/7714) [#7730](https://github.com/tikv/tikv/pull/7730)
    - 修复启用加密时出现 `snapshot ingestion` 错误的问题 [#7815](https://github.com/tikv/tikv/pull/7815)
    - 修复当改写配置文件时发生 `Invalid cross-device link` 的问题 [#7817](https://github.com/tikv/tikv/pull/7817)
    - 修复将配置文件写入到空文件中时会出现错误的 toml 格式的问题 [#7817](https://github.com/tikv/tikv/pull/7817)
    - 修复 Raftstore 中已销毁的 Peer 仍然可能处理请求的问题 [#7836](https://github.com/tikv/tikv/pull/7836)

+ PD

    - 修复 pd-ctl 中使用 `region key` 命令时发生 `404` 错误的问题 [#2399](https://github.com/pingcap/pd/pull/2399)
    - 修复 Grafana 面板中缺失关于 TSO 和 ID 分配的监控的问题 [#2405](https://github.com/pingcap/pd/pull/2405)
    - 修复 Docker 镜像中不包含 `pd-recover` 的问题 [#2406](https://github.com/pingcap/pd/pull/2406)
    - 将数据目录的路径解析为绝对路径以解决 TiDB Dashboard 可能不能正确显示 PD 信息的问题 [#2420](https://github.com/pingcap/pd/pull/2420)
    - 修复在 pd-ctl 中使用 `scheduler config shuffle-region-scheduler` 命令时没有默认输出的问题 [#2416](https://github.com/pingcap/pd/pull/2416)

+ TiFlash

    - 修复部分场景错误上报已使用空间信息的问题

+ Tools

    - TiDB Binlog

        - 修复当下游为 Kafka 时对 `mediumint` 类型数据未处理的问题 [#962](https://github.com/pingcap/tidb-binlog/pull/962)
        - 修复当 DDL 中库名为关键字时 reparo 解析失败的问题 [#961](https://github.com/pingcap/tidb-binlog/pull/961)

    - TiCDC

        - 修复当环境变量 `TZ` 未设置时使用错误时区的问题 [#512](https://github.com/pingcap/ticdc/pull/512)
        - 修复 owner 因为部分错误没有正确处理导致 server 退出时没有清理资源的问题 [#528](https://github.com/pingcap/ticdc/pull/528)
        - 修复重连 TiKV 可能导致 TiCDC 阻塞的问题 [#531](https://github.com/pingcap/ticdc/pull/531)
        - 优化初始化表结构时的内存使用 [#534](https://github.com/pingcap/ticdc/pull/534)
        - 使用 watch 模式监听同步状态变更并进行准实时更新，减少同步延迟 [#481](https://github.com/pingcap/ticdc/pull/481)

    - Backup & Restore (BR)
        - 修复 BR 恢复带有 `auto_random` 属性的表之后，插入数据有一定概率触发 duplicate entry 错误的问题 [#241](https://github.com/pingcap/br/issues/241)
