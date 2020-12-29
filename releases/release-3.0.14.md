---
title: TiDB 3.0.14 Release Notes
---

# TiDB 3.0.14 Release Notes

发版日期：2020 年 5 月 9 日

TiDB 版本：3.0.14

## 兼容性变化

+ TiDB

    - `performance_schema` 和 `metrics_schema` 由读写改为只读 [#15417](https://github.com/pingcap/tidb/pull/15417)

## 重点修复的 Bug

+ TiDB

    - 修复 join 条件在 handle 列上存在多个等值条件时，index join 查询结果错误的问题 [#15734](https://github.com/pingcap/tidb/pull/15734)
    - 修复 fast analyze handle 列 panic 的问题 [#16079](https://github.com/pingcap/tidb/pull/16079)
    - 修复通过 prepare 方式执行 DDL 语句时，DDL job 结构中 query 字段错误的问题，该问题可能导致使用 Binlog 同步时，上下游数据产生不一致 [#15443](https://github.com/pingcap/tidb/pull/15443)

+ TiKV

    - 修复重复清锁请求可能破坏事务原子性的问题 [#7388](https://github.com/tikv/tikv/pull/7388)

## 新功能

+ TiDB

    - `admin show ddl jobs` 查询结果中添加库名和表名列 [#16428](https://github.com/pingcap/tidb/pull/16428)
    - `RECOVER TABLE` 支持恢复被 `TRUNCATE` 的表 [#15458](https://github.com/pingcap/tidb/pull/15458)
    - 新增 `SHOW GRANTS` 语句权限检查的功能 [#16168](https://github.com/pingcap/tidb/pull/16168)
    - 新增 `LOAD DATA` 语句权限检查 [#16736](https://github.com/pingcap/tidb/pull/16736)
    - 提升时间日期相关函数作为 partition key 时，分区裁剪的性能 [#15618](https://github.com/pingcap/tidb/pull/15618)
    - `dispatch error` 的日志级别从 `WARN` 调整为 `ERROR` [#16232](https://github.com/pingcap/tidb/pull/16232)
    - 新增支持 `require-secure-transport` 启动项，以强制要求客户端必须使用 TLS [#15415](https://github.com/pingcap/tidb/pull/15415)
    - 支持内部组件间 http 通信使用 TLS [#15419](https://github.com/pingcap/tidb/pull/15419)
    - `information_schema.processlist` 表中添加显示当前事务 `start_ts` 信息 [#16160](https://github.com/pingcap/tidb/pull/16160)
    - 新增自动重加载集群间通讯 TLS 证书信息的功能 [#15162](https://github.com/pingcap/tidb/pull/15162)
    - 通过重构分区裁剪的实现，提升分区表的读操作的性能 [#15628](https://github.com/pingcap/tidb/pull/15628)
    - 新增当使用 `floor(unix_timestamp(a))` 作为 `range` 分区表的分区表达式时，支持分区裁剪功能 [#16521](https://github.com/pingcap/tidb/pull/16521)
    - 修改 `update` 语句中包含 `view` 且不对该 `view` 进行 update 时的行为，由不允许执行改为正常执行 [#16787](https://github.com/pingcap/tidb/pull/16787)
    - 禁止创建嵌套 `view` [#15424](https://github.com/pingcap/tidb/pull/15424)
    - 禁止 truncate `view` [#16420](https://github.com/pingcap/tidb/pull/16420)
    - 当列处于非 public 状态时，禁止用 `update` 语句显式的更新此列的值 [#15576](https://github.com/pingcap/tidb/pull/15576)
    - 当 status 端口被占用时，禁止启动 TiDB [#15466](https://github.com/pingcap/tidb/pull/15466)
    - `current_role` 函数的字符集由 binary 调整为 utf8mb4 [#16083](https://github.com/pingcap/tidb/pull/16083)
    - 通过在处理完每个 Region 后增加检查 `max-execution-time` 是否符合条件，提升系统处理 `max-execution-time` 的响应灵敏度 [#15615](https://github.com/pingcap/tidb/pull/15615)
    - 新增语法 `ALTER TABLE ... AUTO_ID_CACHE` 用于显式设置 `auto_id` 的缓存步长 [#16287](https://github.com/pingcap/tidb/pull/16287)

+ TiKV

    - 提升乐观事务存在大量冲突及 `BatchRollback` 存在时的性能 [#7605](https://github.com/tikv/tikv/pull/7605)
    - 提升悲观事务冲突严重的场景下悲观锁 waiter 被频繁唤醒导致性能下降的问题 [#7584](https://github.com/tikv/tikv/pull/7584)

+ Tools

    + TiDB Lightning

        - tidb-lightning-ctl 新增 `fetch-mode` 子命令，输出 TiKV 集群模式 [#287](https://github.com/pingcap/tidb-lightning/pull/287)

## Bug 修复

+ TiDB

    - 修复 `WEEKEND` 函数在 SQL mode 为 `ALLOW_INVALID_DATES` 时结果与 MySQL 不兼容的问题 [#16170](https://github.com/pingcap/tidb/pull/16170)
    - 修复当索引列上包含自增主键时，`DROP INDEX` 执行失败的问题 [#16008](https://github.com/pingcap/tidb/pull/16008)
    - 修复 Statement Summary 中，`TABLE_NAMES`  列值有时会不正确的问题 [#15231](https://github.com/pingcap/tidb/pull/15231)
    - 修复因 Plan Cache 启动后部分表达式计算结果错误的问题 [#16184](https://github.com/pingcap/tidb/pull/16184)
    - 修复函数 `not`/`istrue` /`isfalse` 计算结果错误的问题 [#15916](https://github.com/pingcap/tidb/pull/15916)
    - 修复带有冗余索引的表 MergeJoin 时 Panic 的问题 [#15919](https://github.com/pingcap/tidb/pull/15919)
    - 修复谓词只跟外表有联接的情况下错误地化简外链接的问题 [#16492](https://github.com/pingcap/tidb/pull/16492)
    - 修复 `SET ROLE` 导致的 `CURRENT_ROLE` 函数报错问题 [#15569](https://github.com/pingcap/tidb/pull/15569)
    - 修复 `LOAD DATA` 在遇到 `\` 时，处理结果与 MySQL 不兼容的问题 [#16633](https://github.com/pingcap/tidb/pull/16633)
    - 修复数据库可见性与 MySQL 不兼容的问题 [#14939](https://github.com/pingcap/tidb/pull/14939)
    - 修复 `SET DEFAULT ROLE ALL` 语句的权限检查不正确的问题 [#15585](https://github.com/pingcap/tidb/pull/15585)
    - 修复 plan cache 导致的分区裁剪失效问题 [#15818](https://github.com/pingcap/tidb/pull/15818)
    - 修复因事务未对相关表进行加锁，该表存在并发的 DDL 操作且有阻塞时导致事务提交时报 `schema change` 的问题 [#15707](https://github.com/pingcap/tidb/pull/15707)
    - 修复 `IF(not_int, *, *)` 行为不正确的问题 [#15356](https://github.com/pingcap/tidb/pull/15356)
    - 修复 `CASE WHEN (not_int)` 行为不正确的问题 [#15359](https://github.com/pingcap/tidb/pull/15359)
    - 修复在使用非当前 schema 中的视图时报 `Unknown column` 错误的问题 [#15866](https://github.com/pingcap/tidb/pull/15866)
    - 修复解析时间字符串的结果与 MySQL 不兼容的问题 [#16242](https://github.com/pingcap/tidb/pull/16242)
    - 修复 left join 右孩子节点有 `null` 列可能会导致 join 上的排序算子 panic 的问题 [#15798](https://github.com/pingcap/tidb/pull/15798)
    - 修复当 TiKV 持续返回 `StaleCommand` 错误期间，执行 SQL 的流程被阻塞且不报错的问题 [#16528](https://github.com/pingcap/tidb/pull/16528)
    - 修复启用审计插件后端口探活可能会导致 panic 的问题 [#16064](https://github.com/pingcap/tidb/pull/16064)
    - 修复 `fast analyze` 作用于 index 时导致 panic 的问题 [#15967](https://github.com/pingcap/tidb/pull/15967)
    - 修复某些情况下 `SELECT * FROM INFORMATION_SCHEMA.PROCESSLIST` 语句 panic 的问题 [#16309](https://github.com/pingcap/tidb/pull/16309)
    - 修复哈希分区表在建表时由于分配内存之前未及时检查分区数量导致当指定非常大的分区数量（例如 9999999999999）时，导致 TiDB OOM 的问题 [#16218](https://github.com/pingcap/tidb/pull/16218)
    - 修复 `information_schema.tidb_hot_table` 对于分区表信息不准确的问题 [#16726](https://github.com/pingcap/tidb/pull/16726)
    - 修复分区选择算法在哈希分区表上不生效的问题 [#16070](https://github.com/pingcap/tidb/pull/16070)
    - 修复 mvcc 系列的 HTTP API 不支持分区表的问题 [#16191](https://github.com/pingcap/tidb/pull/16191)
    - 保持 `UNION` 语句和 `SELECT` 语句对于错误处理的行为一致 [#16137](https://github.com/pingcap/tidb/pull/16137)
    - 修复当 `VALUES` 函数参数类型为 `bit(n)` 时行为不正确的问题 [#15486](https://github.com/pingcap/tidb/pull/15486)
    - 修复 `view` 列名过长时处理逻辑与 MySQL 不一致的问题，当列名过长时，系统自动生成一个短的列名 [#14873](https://github.com/pingcap/tidb/pull/14873)
    - 修复 `(not not col)` 被错误地优化为 `col` 的问题 [#16094](https://github.com/pingcap/tidb/pull/16094)
    - 修复 index join 构造内表 range 错误的问题 [#15753](https://github.com/pingcap/tidb/pull/15753)
    - 修复 `only_full_group_by` 对含括号的表达式检查错误的问题 [#16012](https://github.com/pingcap/tidb/pull/16012)
    - 修复 `select view_name.col_name from view_name` 报错的问题 [#15572](https://github.com/pingcap/tidb/pull/15572)

+ TiKV

    - 修复某些情况节点隔离恢复之后无法被正确删掉的问题 [#7703](https://github.com/tikv/tikv/pull/7703)
    - 修复网络隔离时 Region Merge 可能导致数据丢失的问题 [#7679](https://github.com/tikv/tikv/pull/7679)
    - 修复某些情况 learner 无法被正确移除的问题 [#7598](https://github.com/tikv/tikv/pull/7598)
    - 修复扫描 raw kv 时可能乱序的问题 [#7597](https://github.com/tikv/tikv/pull/7597)
    - 修复由于 Raft 消息 batch 过大时导致连接重连的问题 [#7542](https://github.com/tikv/tikv/pull/7542)
    - 修复 empty request 造成 gRPC 线程死锁的问题 [#7538](https://github.com/tikv/tikv/pull/7538)
    - 修复 merge 过程中 learner 重启的处理逻辑不正确的问题 [#7457](https://github.com/tikv/tikv/pull/7457)
    - 修复重复清锁请求可能破坏事务原子性的问题 [#7388](https://github.com/tikv/tikv/pull/7388)
