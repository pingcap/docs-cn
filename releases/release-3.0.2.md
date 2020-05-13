---
title: TiDB 3.0.2 Release Notes
category: Releases
---

# TiDB 3.0.2 Release Notes

发版日期：2019 年 8 月 7 日

TiDB 版本：3.0.2

TiDB Ansible 版本：3.0.2

## TiDB

+ SQL 优化器
    - 修复当同一张表在查询里出现多次且逻辑上查询结果恒为空时报错 “Can’t find column in schema” 的问题 [#11247](https://github.com/pingcap/tidb/pull/11247)
    - 修复了 `TIDB_INLJ` Hint 无法以指定表为 Inner 表构建 IndexJoin 时仍，会强制将其作为 Outer 表构建 IndexJoin，同时 Hint 可能会在不应生效的地方生效的错误，该错误是由于强制选取 IndexJoin 的判断逻辑有误，以及对表别名的处理有误导致的；该错误仅对包含 `TIDB_INLJ` 的查询产生影响 [#11362](https://github.com/pingcap/tidb/pull/11362)
    - 修复某些情况下（例如 `SELECT IF(1,c,c) FROM t`），查询结果的列名称不正确的问题 [#11379](https://github.com/pingcap/tidb/pull/11379)
    - 修复 `LIKE` 表达式某些情况下被隐式转换为 0，导致诸如 `SELECT 0 LIKE 'a string'` 返回结果为 `TRUE` 的问题 [#11411](https://github.com/pingcap/tidb/pull/11411)
    - 支持在 `SHOW` 语句中使用子查询，现在可以支持诸如 `SHOW COLUMNS FROM tbl WHERE FIELDS IN (SELECT 'a')` 的写法 [#11459](https://github.com/pingcap/tidb/pull/11459)
    - 修复 `outerJoinElimination` 优化规则没有正确处理列的别名，导致找不到聚合函数的相关列而查询报错的问题；改进了优化过程中对别名的解析，以使得优化可以覆盖更多类型的查询 [#11377](https://github.com/pingcap/tidb/pull/11377)
    - 修复 Window Function 中多个违反语义约束（例如 `UNBOUNDED PRECEDING` 不允许在 Frame 定义的最后）时没有报错的问题 [#11543](https://github.com/pingcap/tidb/pull/11543)
    - 修复 `ERROR 3593 (HY000): You cannot use the window function FUNCTION_NAME in this context` 报错信息中，`FUNCTION_NAME` 不为小写的问题，导致与 MySQL 不兼容 [#11535](https://github.com/pingcap/tidb/pull/11535)
    - 修复 Window Function 中 `IGNORE NULLS` 语法尚未实现，但使用时没有报错的问题 [#11593](https://github.com/pingcap/tidb/pull/11593)
    - 修复优化器对时间类型数据的等值条件代价估算不准确的问题 [#11512](https://github.com/pingcap/tidb/pull/11512)
    - 支持根据反馈信息对统计信息 Top-N 进行更新 [#11507](https://github.com/pingcap/tidb/pull/11507)
+ SQL 执行引擎
    - 修复 `INSERT` 函数在参数中包含 `NULL` 时，返回值不为 `NULL` 的问题 [#11248](https://github.com/pingcap/tidb/pull/11248)
    - 修复 `ADMIN CHECKSUM` 语句在检查分区表时计算结果不正确的问题 [#11266](https://github.com/pingcap/tidb/pull/11266)
    - 修复 INDEX JOIN 在使用前缀索引时可能结果不正确的问题 [#11246](https://github.com/pingcap/tidb/pull/11246)
    - 修复 `DATE_ADD` 函数在进行涉及微秒的日期减法时，没有正确地对日期的小数位数进行对齐导致结果不正确的问题 [#11288](https://github.com/pingcap/tidb/pull/11288)
    - 修复 `DATE_ADD` 函数没有正确地对 INTERVAL 中的负数部分处理导致结果不正确的问题 [#11325](https://github.com/pingcap/tidb/pull/11325)
    - 修复 `Mod(%)`、`Multiple(*)` 和 `Minus(-)` 返回结果为 0 时，在小数位数较多（例如 `select 0.000 % 0.11234500000000000000`）的情况下与 MySQL 位数不一致的问题 [#11251](https://github.com/pingcap/tidb/pull/11251)
    - 修复 `CONCAT` 和 `CONCAT_WS` 函数在返回结果长度超过 `max_allowed_packet` 时，没有正确返回 NULL 和 Warning 的问题 [#11275](https://github.com/pingcap/tidb/pull/11275)
    - 修复 `SUBTIME` 和 `ADDTIME` 函数在参数不合法时，没有正确返回 NULL 和 Warning 的问题 [#11337](https://github.com/pingcap/tidb/pull/11337)
    - 修复 `CONVERT_TZ` 函数在参数不合法时，没有正确返回 NULL 的问题 [#11359](https://github.com/pingcap/tidb/pull/11359)
    - `EXPLAIN ANALYZE` 结果中添加了 `MEMORY` 列，显示 QUERY 的内存使用 [#11418](https://github.com/pingcap/tidb/pull/11418)
    - `EXPLAIN` 结果中，为笛卡尔积 Join 添加了 `CARTESIAN` 关键字 [#11429](https://github.com/pingcap/tidb/pull/11429)
    - 修复类型为 FLOAT 和 DOUBLE 的自增列数据不正确的问题 [#11385](https://github.com/pingcap/tidb/pull/11385)
    - 修复 Dump Pseudo Statistics 时，由于部分信息为 `nil` 导致 panic 的问题 [#11460](https://github.com/pingcap/tidb/pull/11460)
    - 修复常量折叠优化导致 `SELECT … CASE WHEN … ELSE NULL …` 查询结果不正确的问题 [#11441](https://github.com/pingcap/tidb/pull/11441)
    - 修复 `floatStrToIntStr` 对诸如 `+999.9999e2` 的输入没有正确解析的问题 [#11473](https://github.com/pingcap/tidb/pull/11473)
    - 修复 `DATE_ADD` 和 `DATE_SUB` 函数结果超出合法范围时，某些情况下不会返回 `NULL` 的问题 [#11476](https://github.com/pingcap/tidb/pull/11476)
    - 修复长字符串转换为整型时，若字符串包含不合法字符，转换结果与 MySQL 不一致的问题 [#11469](https://github.com/pingcap/tidb/pull/11469)
    - 修复 `REGEXP BINARY` 函数对大小写敏感，导致与 MySQL 不兼容的问题 [#11504](https://github.com/pingcap/tidb/pull/11504)
    - 修复 `GRANT ROLE` 语句在接受 `CURRENT_ROLE` 时报错的问题；修复 `REVOKE ROLE` 语句没有能够正确收回 `mysql.default_role` 权限的问题 [#11356](https://github.com/pingcap/tidb/pull/11356)
    - 修复执行诸如 `SELECT ADDDATE('2008-01-34', -1)` 时，`Incorrect datetime value` Warning 信息的显示格式问题 [#11447](https://github.com/pingcap/tidb/pull/11447)
    - 修复将 JSON 数据中的 Float 类型字段转为 Int 类型溢出时，报错信息中应当提示 `constant … overflows bigint` 而不应当为 `constant … overflows float` 的问题 [#11534](https://github.com/pingcap/tidb/pull/11534)
    - 修复 `DATE_ADD` 函数接受 `FLOAT`、`DOUBLE` 和 `DECIMAL` 类型的列参数时，没有正确地进行类型转换而导致结果可能不正确的问题 [#11527](https://github.com/pingcap/tidb/pull/11527)
    - 修复 `DATE_ADD` 函数中，没有正确处理 INTERVAL 小数部分的符号而导致结果不正确的问题 [#11615](https://github.com/pingcap/tidb/pull/11615)
    - 修复 `Ranger` 没有正确处理前缀索引，导致 Index Lookup Join 中包含前缀索引时，查询结果不正确的问题 [#11565](https://github.com/pingcap/tidb/pull/11565)
    - 修复 `NAME_CONST` 函数第二个参数为负数时执行会报 `Incorrect arguments to NAME_CONST` 的问题 [#11268](https://github.com/pingcap/tidb/pull/11268)
    - 修复一条 SQL 语句在涉及当前时间计算时（例如 `CURRENT_TIMSTAMP` 或者 `NOW`），多次取当前时间值，结果与 MySQL不兼容的问题：现在同一条SQL语句中取当前时间时，均使用相同值 [#11394](https://github.com/pingcap/tidb/pull/11394)
    - 修复了父 Executor `Close` 出现错误时，没有对 `ChildExecutor` 调用 `Close` 的问题，该问题可能导致 `KILL` 语句失效时，子 `ChildExecutor` 没有关闭而导致 Goroutine 泄露 [#11576](https://github.com/pingcap/tidb/pull/11576)
+ Server
    - 修复 `LOAD DATA` 处理 CSV 文件中缺失的 `TIMESTAMP` 字段时，自动补充的值是 0 不是当前时间戳的问题 [#11250](https://github.com/pingcap/tidb/pull/11250)
    - 修复 `SHOW CREATE USER` 语句没有正确检查相关权限的问题，以及 `SHOW CREATE USER CURRENT_USER()` 结果中 USER、HOST 可能不正确的问题 [#11229](https://github.com/pingcap/tidb/pull/11229)
    - 修复在 JDBC 中使用 `executeBatch` 可能返回结果不正确的问题 [#11290](https://github.com/pingcap/tidb/pull/11290)
    - TiKV Server 在更换端口时，减少 Streaming Client 的报错信息的日志打印 [#11370](https://github.com/pingcap/tidb/pull/11370)
    - 优化 Streaming Client 在重新与 TiKV Server 连接时的逻辑：现在 Streaming Client 不会长时间被 Block [#11372](https://github.com/pingcap/tidb/pull/11372)
    - `INFORMATION_SCHEMA.TIDB_HOT_REGIONS` 中新增 `REGION_ID`[#11350](https://github.com/pingcap/tidb/pull/11350)
    - 取消了从 PD API 获取 Region 相关信息时的超时时间，保证在 Region 数量较大时，调用 TiDB API `http://{TiDBIP}:10080/regions/hot` 不会因为 PD 超时而获取失败 [#11383](https://github.com/pingcap/tidb/pull/11383)
    - 修复 HTTP API 中，与 Region 相关的请求没有返回分区表相关的 Region 问题 [#11466](https://github.com/pingcap/tidb/pull/11466)
    - 做以下改动以降低用户手动验证悲观锁时，操作较慢导致锁超时的概率 [#11521](https://github.com/pingcap/tidb/pull/11521)：
        - 悲观锁的默认 TTL 时间由 30 秒提升为 40 秒
        - 最大允许的 TTL 时间由 60 秒提升为 120 秒
        - 悲观锁的持续时间改为从第一次 `LockKeys` 请求时开始计算
    - 修改 TiKV Client 中的 `SendRequest` 函数逻辑：当连接无法建立时，由一直等待改为尽快尝试连接其他 Peer [#11531](https://github.com/pingcap/tidb/pull/11531)
    - 优化 Region Cache：当一个 Store 下线，同时另一个 Store 以同样的地址上线时，将已下线的 Store 标记为失效以尽快在 Cache 中更新 Store 的信息 [#11567](https://github.com/pingcap/tidb/pull/11567)
    - 为 `http://{TiDB_ADDRESS:TIDB_IP}/mvcc/key/{db}/{table}/{handle}` API 的返回结果添加 Region ID 信息 [#11557](https://github.com/pingcap/tidb/pull/11557)
    - 修复 Scatter Table API 没有对 Range Key 进行转义导致 Scatter Table 不生效的问题 [#11298](https://github.com/pingcap/tidb/pull/11298)
    - 优化 Region Cache：当 Region 所在的 Store 无法访问时，将对应的 Store 信息标记失效以避免对这些 Store 的访问造成查询性能下降 [#11498](https://github.com/pingcap/tidb/pull/11498)
    - 修复了多次 DROP 同名 DATABASE 后，DATABASE 内的表结构仍然能够通过 HTTP API 获取到的错误 [#11585](https://github.com/pingcap/tidb/pull/11585)
+ DDL
    - 修复在非字符串类型且长度为 0 的列建立索引时出错的问题 [#11214](https://github.com/pingcap/tidb/pull/11214)
    - 禁止对带有外键约束和全文索引的列进行修改（注意：TiDB 仍然仅在语法上支持外键约束和全文索引）[#11274](https://github.com/pingcap/tidb/pull/11274)
    - 修复并发使用 `ALTER TABLE` 语句更改的位置和列的默认值时，可能导致列的索引 Offset 出错的问题 [#11346](https://github.com/pingcap/tidb/pull/11346)
    - 修复解析 JSON 文本的两个问题：
        - `ConvertJSONToFloat` 中使用 `int64` 作为 `uint64` 的中间解析结果，导致精度溢出的问题 [#11433](https://github.com/pingcap/tidb/pull/11433)
        - `ConvertJSONToInt` 中使用 `int64` 作为 `uint64` 的中间解析结果，导致精度溢出的问题 [#11551](https://github.com/pingcap/tidb/pull/11551)
    - 禁止 DROP 自增列索引，修复因为 DROP 自增列上的索引导致自增列结果可能出错的问题 [#11399](https://github.com/pingcap/tidb/pull/11399)
    - 修复以下问题 [#11492](https://github.com/pingcap/tidb/pull/11492)：
        - 修复显式指定列的排序规则但没有指定字符集时，列的字符集与排序规则不一致的问题
        - 修复 `ALTER TABLE … MODIFY COLUMN` 指定的字符集和排序规则冲突时，没有正确报错的问题
        - 修复 `ALTER TABLE … MODIFY COLUMN` 指定多次字符集和排序规则时，行为与 MySQL 不兼容的问题
    - 为 `TRACE` 语句的结果添加子查询的 trace 细节信息 [#11458](https://github.com/pingcap/tidb/pull/11458)
    - 优化 `ADMIN CHECK TABLE` 执行性能，大幅降低了语句的执行耗时 [#11547](https://github.com/pingcap/tidb/pull/11547)
    - 为 `SPLIT TABLE … REGIONS/INDEX` 添加了返回结果，结果包含 `TOTAL_SPLIT_REGION` 和 `SCATTER_FINISH_RATIO` 展示在超时时间内，切分成功的 Region 数量 [#11484](https://github.com/pingcap/tidb/pull/11484)
    - 修复 `ON UPDATE CURRENT_TIMESTAMP` 作为列的属性且指定浮点精度时，`SHOW CREATE TABLE` 等语句显示精度不完整的问题 [#11591](https://github.com/pingcap/tidb/pull/11591)
    - 修复一个虚拟生成列的表达式中含有另一个虚拟生成列时，该列的索引结果不能正确被计算的问题 [#11475](https://github.com/pingcap/tidb/pull/11475)
    - 修复 `ALTER TABLE … ADD PARTITION …` 语句中，`VALUE LESS THAN` 后不能出现负号的问题 [#11581](https://github.com/pingcap/tidb/pull/11581)
+ Monitor
    - 修复 `TiKVTxnCmdCounter` 监控指标没有注册导致数据没有被收集上报的问题 [#11316](https://github.com/pingcap/tidb/pull/11316)
    - 为 Bind Info 添加了 `BindUsageCounter`、`BindTotalGauge` 和 `BindMemoryUsage` 监控指标 [#11467](https://github.com/pingcap/tidb/pull/11467)

## TiKV

- 修复由于 Raft Log 写入不及时可能导致 TiKV panic 的 bug [#5160](https://github.com/tikv/tikv/pull/5160)
- 修复 TiKV panic 后 panic 信息不会写入日志的 bug [#5198](https://github.com/tikv/tikv/pull/5198)
- 修复了悲观事务下 Insert 行为可能不正确的 bug [#5203](https://github.com/tikv/tikv/pull/5203)
- 降低一部分不需要人工干预的日志输出级别为 INFO [#5193](https://github.com/tikv/tikv/pull/5193)
- 提高存储引擎大小监控项的准确程度 [#5200](https://github.com/tikv/tikv/pull/5200)
- 提高 tikc-ctl 中 Region size 的准确程度 [#5195](https://github.com/tikv/tikv/pull/5195)
- 提高悲观锁死锁检测性能 [#5192](https://github.com/tikv/tikv/pull/5192)
- 提高 Titan 存储引擎 GC 性能 [#5197](https://github.com/tikv/tikv/pull/5197)

## PD

- 修复 Scatter Region 调度器不能工作的 bug [#1642](https://github.com/pingcap/pd/pull/1642)
- 修复 pd-ctl 中不能进行 merge Region 操作的 bug [#1653](https://github.com/pingcap/pd/pull/1653)
- 修复 pd-ctl 中不能进行 remove-tombstone 操作的 bug [#1651](https://github.com/pingcap/pd/pull/1651)
- 修复 scan region 不能找到 key 范围相交的 Region 的问题 [#1648](https://github.com/pingcap/pd/pull/1648)
- 增加重试机制确保 PD 增加成员成功 [#1643](https://github.com/pingcap/pd/pull/1643)

## Tools

TiDB Binlog

- 增加启动时配置项检查功能，遇到不合法配置项会退出运行并给出错误信息 [#687](https://github.com/pingcap/tidb-binlog/pull/687)
- Drainer 增加 `node-id` 配置，用于指定固定逻辑 Drainer [#684](https://github.com/pingcap/tidb-binlog/pull/684)

TiDB Lightning

- 修复 2 个 checksum 同时运行的情况下，`tikv_gc_life_time` 没有正常修改回原本值的问题 [#218](https://github.com/pingcap/tidb-lightning/pull/218)
- 增加启动时配置项检查功能，遇到不合法配置项会退出运行并给出错误信息 [#217](https://github.com/pingcap/tidb-lightning/pull/217)

## TiDB Ansible

- 修复 Disk Performance 监控把 second 作为 ms 的单位错误的问题 [#840](https://github.com/pingcap/tidb-ansible/pull/840)
- Spark 新增 log4j 日志配置 [#841](https://github.com/pingcap/tidb-ansible/pull/841)
- 修复在开启了 Binlog 并且设置了 Kafka 或者 ZooKeeper 时导致生成的 Prometheus 配置文件格式错误的问题 [#844](https://github.com/pingcap/tidb-ansible/pull/844)
- 修复生成的 TiDB 配置文件中遗漏 `pessimistic-txn` 配置参数的问题 [#850](https://github.com/pingcap/tidb-ansible/pull/850)
- TiDB Dashboard 新增和优化 Metrics [#853](https://github.com/pingcap/tidb-ansible/pull/853)
- TiDB Dashboard 上每个监控项增加描述 [#854](https://github.com/pingcap/tidb-ansible/pull/854)
- 新增 TiDB Summary Dashboard，用于更好的查看集群状态和排查问题 [#855](https://github.com/pingcap/tidb-ansible/pull/855)
- TiKV Dashboard 更新 Allocator Stats 监控项 [#857](https://github.com/pingcap/tidb-ansible/pull/857)
- 修复 Node Exporter 的告警表达式单位错误的问题 [#860](https://github.com/pingcap/tidb-ansible/pull/860)
- 更新 tispark jar 包为 v2.1.2 版本 [#862](https://github.com/pingcap/tidb-ansible/pull/862)
- 更新 Ansible Task 功能描述 [#867](https://github.com/pingcap/tidb-ansible/pull/867)
- 兼容 TiDB 变更，TiDB Dashboard 更新 Local reader requests 监控项的表达式 [#874](https://github.com/pingcap/tidb-ansible/pull/874)
- Overview Dashboard 更新 TiKV Memory 监控项的表达式，修复监控显示错误的问题 [#879](https://github.com/pingcap/tidb-ansible/pull/879)
- 移除 Kafka 模式 Binlog 的支持 [#878](https://github.com/pingcap/tidb-ansible/pull/878)
- 修复执行 `rolling_update.yml` 操作时，切换 PD Leader 失效的 bug [#887](https://github.com/pingcap/tidb-ansible/pull/887)
