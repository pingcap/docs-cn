---
title: TiDB 5.0.3 Release Notes
---

# TiDB 5.0.3 Release Notes

发版日期：2021 年 6 月 30 日

TiDB 版本：5.0.3

## 兼容性更改

## 新功能

## 提升改进

+ TiDB

    - 支持将 `TopN` 算子下推到 TiFlash [#25162](https://github.com/pingcap/tidb/pull/25162)
    - 支持将内置函数 `json_unquote()` 下推到 TiKV [#25720](https://github.com/pingcap/tidb/pull/25720)
    - 支持在 Dual 表上移除 `Union` 算子的优化 [#25614](https://github.com/pingcap/tidb/pull/25614)
    - 支持将内置函数 `replace()` 下推到 TiFlash [#25565](https://github.com/pingcap/tidb/pull/25565)
    - 支持将内置函数 `unix_timestamp()`、`concat()`、`year()`、`day()`、`datediff()`、`datesub()`、`castTimeAsString()`、`concat_ws()` 下推到 TiFlash [#25564](https://github.com/pingcap/tidb/pull/25564)
    - 修改聚合算子的代价常数 [#25241](https://github.com/pingcap/tidb/pull/25241)
    - 支持将 `Limit` 算子下推到 TiFlash [#25159](https://github.com/pingcap/tidb/pull/25159)
    - 支持将内置函数 `str_to_date()` 下推到 TiFlash [#25148](https://github.com/pingcap/tidb/pull/25148)
    - 允许 MPP outer join 根据表行数选择构建表 [#25142](https://github.com/pingcap/tidb/pull/25142)
    - 支持将内置函数 `left()`、`right()`、`abs()` 下推到 TiFlash [#25133](https://github.com/pingcap/tidb/pull/25133)
    - 支持将 Broadcast Cartesian Join 下推到 TiFlash [#25106](https://github.com/pingcap/tidb/pull/25106)
    - 支持将 `Union All` 算子下推到 TiFlash [#25051](https://github.com/pingcap/tidb/pull/25051)
    - 支持 MPP 查询任务按 Region 均衡到不同 TiFlash 节点上 [#24724](https://github.com/pingcap/tidb/pull/24724)
    - 支持执行 MPP 查询后将缓存中过时的 Region 无效化 [#24432](https://github.com/pingcap/tidb/pull/24432)

+ TiKV

    - 限制 TiCDC sink 的内存消耗 [#10305](https://github.com/tikv/tikv/pull/10305)
    - 为 TiCDC old value 缓存增加基于内存使用量的上限 [#10313](https://github.com/tikv/tikv/pull/10313)

+ TiFlash

    - 支持将 `STRING` 类型转换为 `DOUBLE` 类型
    - 支持 `STR_TO_DATE()` 函数
    - 通过多线程优化右外连接中的非连接数据
    - 支持笛卡尔积 Join
    - 支持 `LEFT()` 和 `RIGHT()` 函数
    - 支持在 MPP 查询中自动清理过期的 Region 信息
    - 支持 `ABS()` 函数

## Bug 修复

+ TiDB

    - 修复在 `SET` 类型列上 Merge Join 结果不正确的问题 [#25694](https://github.com/pingcap/tidb/pull/25694)
    - 修复 `IN` 表达式参数的数据腐蚀问题 [#25666](https://github.com/pingcap/tidb/pull/25666)
    - 避免 GC 的 session 受全局变量的影响 [#25609](https://github.com/pingcap/tidb/pull/25609)
    - 修复了在窗口函数查询中使用 `Limit` 时出现 panic 问题 [#25517](https://github.com/pingcap/tidb/pull/25517)
    - 修复查询分区表时使用 `Limit` 返回错误值的问题 [#25139](https://github.com/pingcap/tidb/pull/25139)
    - 修复了 `IFNULL` 在 `ENUM` 或 `SET` 类型上不能正确生效的问题 [#25116](https://github.com/pingcap/tidb/pull/25116)
    - 修复了 Join 子查询中的 `count` 被改写为 `first_row` 导致结果不正确的问题 [#25062](https://github.com/pingcap/tidb/pull/25062)
    - 修复了 `TopN` 算子下使用 `ParallelApply` 查询时卡住的问题 [#25011](https://github.com/pingcap/tidb/pull/25011)
    - 修复了使用含有多列的前缀索引查询时出现多余结果的问题 [#24635](https://github.com/pingcap/tidb/pull/24635)
    - 修复了操作符 `<=>` 不能正确生效的问题 [#24633](https://github.com/pingcap/tidb/pull/24633)
    - 修复并行 `Apply` 算子的数据竞争问题 [#24345](https://github.com/pingcap/tidb/pull/24345)
    ?- 修复在分区表上对 union IndexMerge 结果排序时出现的 `index out of range` 错误 [#24155](https://github.com/pingcap/tidb/pull/24155)
    - 禁止设置一个未来的读时间戳 [#25761](https://github.com/pingcap/tidb/pull/25761)
    - 修复 ODBC 类常数（例如 `{d '2020-01-01'}`）不能被用作表达式的问题 [#25577](https://github.com/pingcap/tidb/pull/25577)
    - 修复 `SELECT DISTINCT` 被转化为 Batch Get 而导致结果不正确的问题 [#25533](https://github.com/pingcap/tidb/pull/25533)
    - 修复无法触发将查询从 TiFlash 回退到 TiKV 的问题 [#24600](https://github.com/pingcap/tidb/pull/24600)
    - 修复在检查 `only_full_group_by` 时的 `index-out-of-range` 错误 [#24016](https://github.com/pingcap/tidb/pull/24016)

+ TiKV

    - 修复错误的 `tikv_raftstore_hibernated_peer_state` 监控指标 [#10431](https://github.com/tikv/tikv/pull/10431)
    - 修复 coprocessor 中 `json_unquote()` 函数错误的参数类型 [#10424](https://github.com/tikv/tikv/pull/10424)
    - 修复在 Backup & Restore 数据恢复期间开启 TDE 会报出文件已存在的错误 [#10421](https://github.com/tikv/tikv/pull/10421)
    - 正常关机时跳过清理 Raftstore 的回调从而避免在某些情况下破坏事务的 ACID [#10396](https://github.com/tikv/tikv/pull/10396)
    - 修复在 Leader 上 Replica Read 共享 Read Index 的问题 [#10391](https://github.com/tikv/tikv/pull/10391)
    - 修复 coprocessor 转换 `DOUBLE` 到 `DOUBLE` 的错误函数 [#10388](https://github.com/tikv/tikv/pull/10388)

+ TiFlash

    - 修复因 split 失败而不断重启的问题
    ?- 修复无法 GC Delta 数据的潜在问题
    - 修复在 `CAST` 函数中为非二进制字符串填充错误数据的问题
    - 修复处理包含复杂 `GROUP BY` 列的聚合查询时结果不正确的问题
    - 修复写入压力过大时出现进程崩溃的问题
    - 修复右连接键不为空且左连接键可为空时进程崩溃的问题
    - 修复 `read-index` 请求耗时长的潜在问题
