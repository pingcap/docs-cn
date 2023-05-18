---
title: TiDB 3.0.6 Release Notes
aliases: ['/docs-cn/dev/releases/release-3.0.6/','/docs-cn/dev/releases/3.0.6/']
---

# TiDB 3.0.6 Release Notes

发版日期：2019 年 11 月 28 日

TiDB 版本：3.0.6

TiDB Ansible 版本：3.0.6

## TiDB

+ SQL 优化器
    - 修复窗口函数 AST Restore SQL 文本后结果不正确问题，`over w` 不应被 restore 成 `over (w)` [#12933](https://github.com/pingcap/tidb/pull/12933)
    - 修复 stream aggregation 下推给 double read 的问题 [#12690](https://github.com/pingcap/tidb/pull/12690)
    - 修复 SQL bind 中引号处理不正确的问题 [#13117](https://github.com/pingcap/tidb/pull/13117)
    - 优化 `select max(_tidb_rowid) from t` 场景，避免全表扫 [#13095](https://github.com/pingcap/tidb/pull/13095)
    - 修复当查询语句中包含变量赋值表达式时查询结果不正确的问题 [#13231](https://github.com/pingcap/tidb/pull/13231)
    - 修复 `UPDATE` 语句中同时包含子查询和 generated column 时结果错误的问题；修复 `UPDATE` 语句中包含不同数据库的两个表名相同的表时，`UPDATE` 执行报错的问题 [#13350](https://github.com/pingcap/tidb/pull/13350)
    - 支持用 `_tidb_rowid` 做点查 [#13416](https://github.com/pingcap/tidb/pull/13416)
    - 修复分区表统计信息使用错误导致生成执行计划不正确的问题 [#13628](https://github.com/pingcap/tidb/pull/13628)
+ SQL 执行引擎
    - 修复 year 类型对于无效值的处理时和 MySQL 不兼容问题 [#12745](https://github.com/pingcap/tidb/pull/12745)
    - 在 `INSERT ON DUPLICATE UPDATE` 语句中复用 `Chunk` 以降低内存开销 [#12998](https://github.com/pingcap/tidb/pull/12998)
    - 添加内置函数 `JSON_VALID` 的支持 [#13133](https://github.com/pingcap/tidb/pull/13133)
    - 支持在分区表上执行 `ADMIN CHECK TABLE` [#13140](https://github.com/pingcap/tidb/pull/13140)
    - 修复对空表进行 `FAST ANALYZE` 时 panic 的问题 [#13343](https://github.com/pingcap/tidb/pull/13343)
    - 修复在包含多列索引的空表上执行 Fast Analyze 时 panic 的问题 [#13394](https://github.com/pingcap/tidb/pull/13394)
    - 修复当 `WHERE` 子句上有 UNIQUE KEY 的等值条件时，估算行数大于 1 的问题 [#13382](https://github.com/pingcap/tidb/pull/13382)
    - 修复当 TiDB 开启 `Streaming` 后返回数据有可能重复的问题 [#13254](https://github.com/pingcap/tidb/pull/13254)
    - 将 `CMSketch` 中出现次数最多的 N 个值抽取出来，提高估算准确度 [#13429](https://github.com/pingcap/tidb/pull/13429)
+ Server
    - 当 gRPC 请求超时时，提前让发往 TiKV 的请求失败 [#12926](https://github.com/pingcap/tidb/pull/12926)
    - 添加以下虚拟表：[#13009](https://github.com/pingcap/tidb/pull/13009)
        - `performance_schema.tidb_profile_allocs`
        - `performance_schema.tidb_profile_block`
        - `performance_schema.tidb_profile_cpu`
        - `performance_schema.tidb_profile_goroutines`
    - 修复 query 在等待悲观锁时，kill query 不生效的问题 [#12989](https://github.com/pingcap/tidb/pull/12989)
    - 当悲观事务上锁失败，且事务只涉及一个 key 的修改时，不再异步回滚 [#12707](https://github.com/pingcap/tidb/pull/12707)
    - 修复 split Region 请求的 response 为空时 panic 的问题 [#13092](https://github.com/pingcap/tidb/pull/13092)
    - 悲观事务在其他事务先锁住导致上锁失败时，避免重复 backoff [#13116](https://github.com/pingcap/tidb/pull/13116)
    - 修改 TiDB 检查配置时的行为，出现不能识别的配置选项时，打印警告日志 [#13272](https://github.com/pingcap/tidb/pull/13272)
    - 支持通过 `/info/all` 接口获取所有 TiDB 节点的 binlog 状态 [#13187](https://github.com/pingcap/tidb/pull/13187)
    - 修复 kill connection 时可能出现 goroutine 泄漏的问题 [#13251](https://github.com/pingcap/tidb/pull/13251)
    - 让 `innodb_lock_wait_timeout` 参数在悲观事务中生效，用于控制悲观锁的等锁超时时间 [#13165](https://github.com/pingcap/tidb/pull/13165)
    - 当悲观事务的 query 被 kill 后，停止更新悲观事务的 TTL，避免其他的事务做不必要的等待 [#13046](https://github.com/pingcap/tidb/pull/13046)
+ DDL
    - 修复 `SHOW CREATE VIEW` 结果与 MySQL 不一致的问题 [#12912](https://github.com/pingcap/tidb/pull/12912)
    - 支持基于 UNION 创建 View，例如 `create view v as select * from t1 union select * from t2` [#12955](https://github.com/pingcap/tidb/pull/12955)
    - 给 `slow_query` 表添加更多事务相关的字段：[#13072](https://github.com/pingcap/tidb/pull/13072)
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
    - 创建表时如果表包含 collate 则列使用表的 collate 而不是系统默认的字符集 [#13174](https://github.com/pingcap/tidb/pull/13174)
    - 创建表时限制索引名字的长度 [#13310](https://github.com/pingcap/tidb/pull/13310)
    - 修复 rename table 时未检查表名长度的问题 [#13346](https://github.com/pingcap/tidb/pull/13346)
    - 新增 `alter-primary-key` 配置来支持 TiDB add/drop primary key，该配置默认关闭 [#13522](https://github.com/pingcap/tidb/pull/13522)

## TiKV

- 修复 `acquire_pessimistic_lock` 接口返回错误 `txn_size` 的问题 [#5740](https://github.com/tikv/tikv/pull/5740)
- 限制 GC worker 每秒写入量，降低对性能的影响 [#5735](https://github.com/tikv/tikv/pull/5735)
- 优化 lock manager 的准确度 [#5845](https://github.com/tikv/tikv/pull/5845)
- 悲观锁支持 `innodb_lock_wait_timeout` [#5848](https://github.com/tikv/tikv/pull/5848)
- 添加 Titan 相关配置检测 [#5720](https://github.com/tikv/tikv/pull/5720)
- 支持用 tikv-ctl 动态修改 GC 限流配置：`tikv-ctl --host=ip:port modify-tikv-config -m server -n gc.max_write_bytes_per_sec -v 10MB` [#5957](https://github.com/tikv/tikv/pull/5957)
- 减少无用的 clean up 请求，降低死锁检测器的压力 [#5965](https://github.com/tikv/tikv/pull/5965)
- 悲观事务 prewrite 时避免 TTL 被缩短 [#6056](https://github.com/tikv/tikv/pull/6056)
- 修复 Titan 可能发生 missing blob file 的问题 [#5968](https://github.com/tikv/tikv/pull/5968)
- 修复 Titan 可能导致 `RocksDBOptions` 不生效的问题 [#6009](https://github.com/tikv/tikv/pull/6009)

## PD

- 为每个过滤器添加一个名为 `ActOn` 的新维度，以指示每个 scheduler 和 checker 受过滤器的影响。删除两个未使用的过滤器：`disconnectFilter` 和 `rejectLeaderFilter` [#1911](https://github.com/pingcap/pd/pull/1911)
- 当 PD 生成时间戳的时间超过5毫秒时，将打印一条 warning 日志 [#1867](https://github.com/pingcap/pd/pull/1867)
- 当存在 endpoint 不可用时，降低 client 日志级别 [#1856](https://github.com/pingcap/pd/pull/1856)
- 修复 `region_syncer` 同步时 gRPC 消息包可能过大的问题 [#1952](https://github.com/pingcap/pd/pull/1952)

## Tools

+ TiDB Binlog
    - Drainer 配置 `initial-commit-ts` 为 -1 时，从 PD 处获取初始同步时间戳 [#788](https://github.com/pingcap/tidb-binlog/pull/788)
    - Drainer checkpoint 存储与下游解耦，支持选择配置 checkpoint 保存到 MySQL 或者本地文件 [#790](https://github.com/pingcap/tidb-binlog/pull/790)
    - 修复 Drainer 在配置同步库表过滤使用空值会导致 Panic 的问题 [#801](https://github.com/pingcap/tidb-binlog/pull/801)
    - 修复 Drainer 因为向下游应用 Binlog 失败而 Panic 后进程没有退出而是进入死锁状态的问题 [#807](https://github.com/pingcap/tidb-binlog/pull/807)
    - 修复 Pump 下线因为 gRPC 的 `GracefulStop` 流程而 hang 住的问题 [#817](https://github.com/pingcap/tidb-binlog/pull/817)
    - 修复 Drainer 在 TiDB 执行 `DROP COLUMN` DDL 期间收到缺少一列的 binlog 而同步出错的问题（要求 TiDB 3.0.6 以上）[#827](https://github.com/pingcap/tidb-binlog/pull/827)
+ TiDB Lightning
    - TiDB Backend 模式新增 `max-allowed-packet` 配置项，默认值为 64M [#248](https://github.com/pingcap/tidb-lightning/pull/248)
