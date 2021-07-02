---
title: TiDB 5.0.3 Release Notes
---

# TiDB 5.0.3 Release Notes

发版日期：2021 年 7 月 2 日

TiDB 版本：5.0.3

## 兼容性更改

+ TiDB

    - v4.0 集群升级到 v5.0 或更高版本（dev 和 v5.1）的集群后，`tidb_multi_statement_mode` 变量的默认值由 `WARN` 变为 `OFF`

## 功能增强

+ Tools

    + TiCDC

        - 增加 HTTP API 获取 TiCDC changefeed 信息和节点健康信息 [#1955](https://github.com/pingcap/ticdc/pull/1955)
        - 为 kafka 下游增加 SASL/SCRAM 支持 [#1942](https://github.com/pingcap/ticdc/pull/1942)
        - 使 TiCDC 在 server 级别支持 `--data-dir` 配置 [#2070](https://github.com/pingcap/ticdc/pull/2070)

## 提升改进

+ TiDB

    - 支持将 `TopN` 算子下推到 TiFlash [#25162](https://github.com/pingcap/tidb/pull/25162)
    - 支持将内置函数 `json_unquote()` 下推到 TiKV [#25720](https://github.com/pingcap/tidb/pull/25720)
    - 支持在 Dual 表上移除 `Union` 算子的优化 [#25614](https://github.com/pingcap/tidb/pull/25614)
    - 支持将内置函数 `replace()` 下推到 TiFlash [#25565](https://github.com/pingcap/tidb/pull/25565)
    - 支持将内置函数 `unix_timestamp()`、`concat()`、`year()`、`day()`、`datediff()`、`datesub()`、`concat_ws()` 下推到 TiFlash [#25564](https://github.com/pingcap/tidb/pull/25564)
    - 优化聚合算子的代价常数 [#25241](https://github.com/pingcap/tidb/pull/25241)
    - 支持将 `Limit` 算子下推到 TiFlash [#25159](https://github.com/pingcap/tidb/pull/25159)
    - 支持将内置函数 `str_to_date()` 下推到 TiFlash [#25148](https://github.com/pingcap/tidb/pull/25148)
    - 允许 MPP outer join 根据表行数选择构建表 [#25142](https://github.com/pingcap/tidb/pull/25142)
    - 支持将内置函数 `left()`、`right()`、`abs()` 下推到 TiFlash [#25133](https://github.com/pingcap/tidb/pull/25133)
    - 支持将 Broadcast Cartesian Join 下推到 TiFlash [#25106](https://github.com/pingcap/tidb/pull/25106)
    - 支持将 `Union All` 算子下推到 TiFlash [#25051](https://github.com/pingcap/tidb/pull/25051)
    - 支持 MPP 查询任务按 Region 均衡到不同 TiFlash 节点上 [#24724](https://github.com/pingcap/tidb/pull/24724)
    - 支持执行 MPP 查询后将缓存中过时的 Region 无效化 [#24432](https://github.com/pingcap/tidb/pull/24432)
    - 提升内置函数 `str_to_date` 在格式指定器中 `%b/%M/%r/%T` 的 MySQL 兼容性 [#25767](https://github.com/pingcap/tidb/pull/25767)

+ TiKV

    - 限制 TiCDC sink 的内存消耗 [#10305](https://github.com/tikv/tikv/pull/10305)
    - 为 TiCDC old value 缓存增加基于内存使用量的上限 [#10313](https://github.com/tikv/tikv/pull/10313)

+ PD

    - 将 TiDB Dashboard 升级至 v2021.06.15.1 [#3798](https://github.com/pingcap/pd/pull/3798)

+ TiFlash

    - 支持将 `STRING` 类型转换为 `DOUBLE` 类型
    - 支持 `STR_TO_DATE()` 函数
    - 通过多线程优化右外连接中的非连接数据
    - 支持笛卡尔积 Join
    - 支持 `LEFT()` 和 `RIGHT()` 函数
    - 支持在 MPP 查询中自动清理过期的 Region 信息
    - 支持 `ABS()` 函数

+ Tools

    + TiCDC

        - 优化 gRPC 的重连逻辑，提升 KV client 的吞吐 [#1586](https://github.com/pingcap/ticdc/issues/1586) [#1501](https://github.com/pingcap/ticdc/issues/1501#issuecomment-820027078) [#1682](https://github.com/pingcap/ticdc/pull/1682) [#1393](https://github.com/pingcap/ticdc/issues/1393) [#184s7](https://github.com/pingcap/ticdc/pull/1847) [#1905](https://github.com/pingcap/ticdc/issues/1905) [#1904](https://github.com/pingcap/ticdc/issues/1904)
        - 优化 sorter I/O 报错信息

## Bug 修复

+ TiDB

    - 修复在 `SET` 类型列上 Merge Join 结果不正确的问题 [#25669](https://github.com/pingcap/tidb/issues/25669)
    - 修复 `IN` 表达式参数的数据腐蚀问题 [#25591](https://github.com/pingcap/tidb/issues/25591)
    - 避免 GC 的 session 受全局变量的影响 [#24976](https://github.com/pingcap/tidb/issues/24976)
    - 修复了在窗口函数查询中使用 `Limit` 时出现 panic 问题 [#25344](https://github.com/pingcap/tidb/issues/25344)
    - 修复查询分区表时使用 `Limit` 返回错误值的问题 [#24636](https://github.com/pingcap/tidb/issues/24636)
    - 修复了 `IFNULL` 在 `ENUM` 或 `SET` 类型上不能正确生效的问题 [#24944](https://github.com/pingcap/tidb/issues/24944)
    - 修复了 Join 子查询中的 `count` 被改写为 `first_row` 导致结果不正确的问题 [#24865](https://github.com/pingcap/tidb/issues/24865)
    - 修复了 `TopN` 算子下使用 `ParallelApply` 查询时卡住的问题 [#24930](https://github.com/pingcap/tidb/issues/24930)
    - 修复了使用含有多列的前缀索引查询时出现多余结果的问题 [#24356](https://github.com/pingcap/tidb/issues/24356)
    - 修复了操作符 `<=>` 不能正确生效的问题 [#24477](https://github.com/pingcap/tidb/issues/24477)
    - 修复并行 `Apply` 算子的数据竞争问题 [#23280](https://github.com/pingcap/tidb/issues/23280)
    - 修复对 PartitionUnion 算子的 IndexMerge 结果排序时出现 `index out of range` 错误 [#23919](https://github.com/pingcap/tidb/issues/23919)
    - 修复 `tidb_snapshot` 被允许设置为非预期的过大值，而可能造成事务隔离性被破坏的问题 [25680]( https://github.com/pingcap/tidb/issues/25680)
    - 修复 ODBC 类常数（例如 `{d '2020-01-01'}`）不能被用作表达式的问题 [#25531](https://github.com/pingcap/tidb/issues/25531)
    - 修复 `SELECT DISTINCT` 被转化为 Batch Get 而导致结果不正确的问题 [#25320](https://github.com/pingcap/tidb/issues/25320)
    - 修复无法触发将查询从 TiFlash 回退到 TiKV 的问题 [#23665](https://github.com/pingcap/tidb/issues/23665) [#24421](https://github.com/pingcap/tidb/issues/24421)
    - 修复在检查 `only_full_group_by` 时的 `index-out-of-range` 错误 [#23839](https://github.com/pingcap/tidb/issues/23839)
    - 修复使用 `TABLESAMPLE` 在空表上进行查询返回预期外的行数据的问题 [#25257](https://github.com/pingcap/tidb/issues/25257)
    - 修复关联子查询中 Index Join 的结果不正确问题 [#25799](https://github.com/pingcap/tidb/issues/25799)

+ TiKV

    - 修复错误的 `tikv_raftstore_hibernated_peer_state` 监控指标 [#10330](https://github.com/tikv/tikv/issues/10330)
    - 修复 coprocessor 中 `json_unquote()` 函数错误的参数类型 [#10176](https://github.com/tikv/tikv/issues/10176)
    - 正常关机时跳过清理 Raftstore 的回调从而避免在某些情况下破坏事务的 ACID [#10353](https://github.com/tikv/tikv/issues/10353) [#10307](https://github.com/tikv/tikv/issues/10307)
    - 修复在 Leader 上 Replica Read 共享 Read Index 的问题 [#10347](https://github.com/tikv/tikv/issues/10347)
    - 修复 coprocessor 转换 `DOUBLE` 到 `DOUBLE` 的错误函数 [#25200](https://github.com/pingcap/tidb/issues/25200)
+ PD

    - 修复在 scheduler 启动之后，加载 TTL 配置产生的数据竞争问题 [#3771](https://github.com/tikv/pd/issues/3771)
    - 修复 `is_learner` 字段在 TiDB 的 `TIKV_REGION_PEERS` 表中显示异常的问题 [#3372](https://github.com/tikv/pd/issues/3372) [#24293](https://github.com/pingcap/tidb/issues/24293)
    - 修复在一个 zone 内所有 TiKV 节点下线或宕机的情况下，PD 不往其他 zone 调度数据的问题 [#3705](https://github.com/tikv/pd/issues/3705)
    - 修复在添加 scatter range 调度器后导致 PD 挂掉的问题 [#3762](https://github.com/tikv/pd/pull/3762)

+ TiFlash

    - 修复因 split 失败而不断重启的问题
    - 修复无法删除 Delta 历史数据的潜在问题
    - 修复在 `CAST` 函数中为非二进制字符串填充错误数据的问题
    - 修复处理包含复杂 `GROUP BY` 列的聚合查询时结果不正确的问题
    - 修复写入压力过大时出现进程崩溃的问题
    - 修复右连接键不为空且左连接键可为空时进程崩溃的问题
    - 修复 `read-index` 请求耗时长的潜在问题
    - 修复读负载高的情况下进程崩溃的问题
    - 修复 `Date_Format` 函数在参数类型为 `STRING` 且包含 `NULL` 值时可能导致 TiFlash server 崩溃的问题

+ Tools

    + TiCDC

        - 修复 TiCDC owner 在刷新 checkpoint 时异常退出的问题 [#1902](https://github.com/pingcap/ticdc/issues/1902)
        - 修复写 MySQL 下游出错暂停时 MySQL 连接泄漏的问题 [#1946](https://github.com/pingcap/ticdc/pull/1946)
        - 修复 TiCDC 读取 `/proc/meminfo` 失败时出现的 panic 问题 [#2024](https://github.com/pingcap/ticdc/pull/2024)
        - 减少 TiCDC 运行时的内存使用 [#2012](https://github.com/pingcap/ticdc/pull/2012) [#1958](https://github.com/pingcap/ticdc/pull/1958)
        - 修复 resolved ts 计算慢导致 TiCDC panic 的问题 [#1576](https://github.com/pingcap/ticdc/issues/1576)
        - 修复 processor 潜在的死锁问题 [#2142](https://github.com/pingcap/ticdc/pull/2142)

    + Backup & Restore (BR)

        - 修复 BR 恢复中忽略了所有系统表的问题 [#1197](https://github.com/pingcap/br/issues/1197) [#1201](https://github.com/pingcap/br/issues/1201)
        - 修复在 Backup & Restore 数据恢复期间开启 TDE 会报出文件已存在的错误 [#1179](https://github.com/pingcap/br/issues/1179)

    + TiDB Lightning

        - 修复 TiDB Lightning 在特殊数据下 panic 的问题 [#1213](https://github.com/pingcap/br/issues/1213)
        - 修复 TiDB Lightning 导入大文件拆分时遇到的 EOF 报错问题 [#1133](https://github.com/pingcap/br/issues/1133)
        - 修复 TiDB Lightning 导入含 `auto_increment` 的 `DOUBLE` 或 `FLOAT` 类型列的表时生成极大 base 值的问题 [#1186](https://github.com/pingcap/br/pull/1186)
        - 修复 TiDB Lightning 解析 Parquet 文件中 `DECIMAL` 类型数据失败的问题 [#1277](https://github.com/pingcap/br/pull/1277)
