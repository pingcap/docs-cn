---
title: TiDB 2.1.19 Release Notes
---

# TiDB 2.1.19 Release Notes

发版日期：2019 年 12 月 27 日

TiDB 版本：2.1.19

TiDB Ansible 版本：2.1.19

## TiDB

+ SQL 优化器
    - 优化 `select max(_tidb_rowid) from t` 的场景，避免全表扫 [#13294](https://github.com/pingcap/tidb/pull/13294)
    - 修复当查询语句中赋予用户变量错误的值且将谓词下推后导致错误的输出结果 [#13230](https://github.com/pingcap/tidb/pull/13230)
    - 修复更新统计信息时可能存在数据竞争，导致统计信息不准确的问题 [#13690](https://github.com/pingcap/tidb/pull/13690)
    - 修复 `UPDATE` 语句中同时包含子查询和 stored generated column 时结果错误的问题；修复 `UPDATE` 语句中包含不同数据库的两个表名相同时，`UPDATE` 执行报错的问题 [#13357](https://github.com/pingcap/tidb/pull/13357)
    - 修复 `PhysicalUnionScan` 算子没有正确设置统计信息，导致查询计划可能选错的问题 [#14134](https://github.com/pingcap/tidb/pull/14134)
    - 移除 `minAutoAnalyzeRatio` 约束使自动 `ANALYZE` 更及时 [#14013](https://github.com/pingcap/tidb/pull/14013)
    - 当 `WHERE` 子句上有 `UNIQUE KEY` 的等值条件时，估算行数应该不大于 `1` [#13385](https://github.com/pingcap/tidb/pull/13385)
+ SQL 执行引擎
    - 修复 `ConvertJSONToInt` 中使用 `int64` 作为 `uint64` 的中间解析结果，导致精度溢出的问题 [#13036](https://github.com/pingcap/tidb/pull/13036)
    - 修复查询中包含 `SLEEP` 函数时（例如 `select 1 from (select sleep(1)) t;)`），由于列裁剪导致查询中的 `sleep(1)` 失效的问题 [#13039](https://github.com/pingcap/tidb/pull/13039)
    - 通过实现在 `INSERT ON DUPLICATE UPDATE` 语句中复用 `Chunk` 来降低内存开销 [#12999](https://github.com/pingcap/tidb/pull/12999)
    - 给 `slow_query` 表添加事务相关的信息段 [#13129](https://github.com/pingcap/tidb/pull/13129)，如下：
        - `Prewrite_time`
        - `Commit_time`
        - `Get_commit_ts_time`
        - `Commit_backoff_time`
        - `Backoff_types`
        - `Resolve_lock_time`
        - `Local_latch_wait_time`
        - `Write_key`
        - `Write_size`
        - `Prewrite_region`
        - `Txn_retry`
    - 修复 `UPDATE` 语句中包含子查询时转换子查询出现的错误和当 `UPDATE` 的 `WHERE` 条件中包含子查询时更新失败的问题 [#13120](https://github.com/pingcap/tidb/pull/13120)
    - 支持在分区表上执行 `ADMIN CHECK TABLE` [#13143](https://github.com/pingcap/tidb/pull/13143)
    - 修复 `ON UPDATE CURRENT_TIMESTAMP` 作为列的属性且指定浮点精度时，`SHOW CREATE TABLE` 等语句显示精度不完整的问题 [#12462](https://github.com/pingcap/tidb/pull/12462)
    - 修复在 `DROP/MODIFY/CHANGE COLUMN` 时没有检查外键导致执行 `SELECT * FROM information_schema.KEY_COLUMN_USAGE` 语句时发生 panic 的问题 [#14162](https://github.com/pingcap/tidb/pull/14162)
    - 修复 TiDB 开启 `Streaming` 后返回数据可能重复的问题 [#13255](https://github.com/pingcap/tidb/pull/13255)
    - 修复夏令时导致的“无效时间格式”问题 [#13624](https://github.com/pingcap/tidb/pull/13624)
    - 修复整型数据被转换为无符号 `Real`/`Decimal` 类型时，精度可能丢失的问题 [#13756](https://github.com/pingcap/tidb/pull/13756)
    - 修复 `Quote` 函数处理 `null` 值时返回值类型出错的问题 [#13681](https://github.com/pingcap/tidb/pull/13681)
    - 修复从字符串解析日期时，由于使用 `golang time.Local` 本地时区导致解析结果的时区不正确的问题 [#13792](https://github.com/pingcap/tidb/pull/13792)
    - 修复 `builtinIntervalRealSig` 的实现中，由于 `binSearch` 方法不会返回 error，导致最终结果可能不正确的问题 [#13768](https://github.com/pingcap/tidb/pull/13768)
    - 修复 `INSERT` 语句在进行字符串类型到浮点类型转换时，可能会报错的问题 [#14009](https://github.com/pingcap/tidb/pull/14009)
    - 修复 `sum(distinct)` 函数输出结果不正确的问题 [#13041](https://github.com/pingcap/tidb/pull/13041)
    - 修复由于对 `jsonUnquoteFunction` 函数的返回类型长度赋值不正确的值，导致在 `union` 中同位置数据上进行 `cast` 转换时会截断数据的问题 [#13645](https://github.com/pingcap/tidb/pull/13645)
    - 修复由于权限检查过于严格导致设置密码失败的问题 [#13805](https://github.com/pingcap/tidb/pull/13805)
+ Server
    - 修复 `KILL CONNECTION` 可能出现 goroutine 泄漏的问题 [#13252](https://github.com/pingcap/tidb/pull/13252)
    - 新增通过 HTTP API 的 `info/all` 接口获取所有 TiDB 节点的 binlog 状态功能 [#13188](https://github.com/pingcap/tidb/pull/13188)
    - 修复在 Windows 上 build TiDB 项目失败的问题 [#13650](https://github.com/pingcap/tidb/pull/13650)
    - 新增 `server-version` 配置项来控制修改 TiDB server 版本的功能 [#13904](https://github.com/pingcap/tidb/pull/13904)
    - 修复通过 Go1.13 版本编译的二进制程序 `plugin` 不能正常运行的问题 [#13527](https://github.com/pingcap/tidb/pull/13527)
+ DDL
    - 新增创建表时如果表包含 `COLLATE` 则列的 `COLLATE` 使用表的 `COLLATE` [#13190](https://github.com/pingcap/tidb/pull/13190)
    - 新增创建表时限制索引名字的长度的功能 [#13311](https://github.com/pingcap/tidb/pull/13311)
    - 修复 rename table 时未检查表名长度的问题 [#13345](https://github.com/pingcap/tidb/pull/13345)
    - 新增 `BIT` 列的宽度范围检查的功能 [#13511](https://github.com/pingcap/tidb/pull/13511)
    - 优化 `change/modify column` 的输出的错误信息，让人更容易理解 [#13798](https://github.com/pingcap/tidb/pull/13798)
    - 修复执行 `drop column` 操作且下游 Drainer 还没有执行此 `drop column` 操作时，下游可能会收到不带此列的 DML 的问题 [#13974](https://github.com/pingcap/tidb/pull/13974)

## TiKV

+ Raftstore
    - 修复 Region merge 和应用 Compact log 过程中系统若有重启，当重启时由于未正确设置 `is_merging` 的值导致系统 panic 的问题 [#5884](https://github.com/tikv/tikv/pull/5884)
+ Importer
    - 取消 gRPC 的消息长度限制 [#5809](https://github.com/tikv/tikv/pull/5809)

## PD

- 提升获取 Region 列表的 HTTP API 性能 [#1988](https://github.com/pingcap/pd/pull/1988)
- 升级 etcd，修复 etcd PreVote 无法选出 leader 的问题（升级后无法降级） [#2052](https://github.com/pingcap/pd/pull/2052)

## Tools

+ TiDB Binlog
    - 优化通过 binlogctl 输出的节点状态信息 [#777](https://github.com/pingcap/tidb-binlog/pull/777)
    - 修复当 Drainer 过滤配置为 `nil` 时 panic 的问题 [#802](https://github.com/pingcap/tidb-binlog/pull/802)
    - 优化 Pump 的 `Graceful` 退出方式 [#825](https://github.com/pingcap/tidb-binlog/pull/825)
    - 新增 Pump 写 binlog 数据时更详细的监控指标 [#830](https://github.com/pingcap/tidb-binlog/pull/830)
    - 优化 Drainer 在执行 DDL 后刷新表结构信息的逻辑 [#836](https://github.com/pingcap/tidb-binlog/pull/836)
    - 修复 Pump 在没有收到 DDL 的 commit binlog 时该 binlog 被忽略的问题 [#855](https://github.com/pingcap/tidb-binlog/pull/855)

## TiDB Ansible

- TiDB 服务 `Uncommon Error OPM` 监控项更名为 `Write Binlog Error` 并增加对应的告警 [#1038](https://github.com/pingcap/tidb-ansible/pull/1038)
- 升级 TiSpark 版本为 2.1.8 [#1063](https://github.com/pingcap/tidb-ansible/pull/1063)
