---
title: TiDB 3.0.10 Release Notes
---

# TiDB 3.0.10 Release Notes

发版日期：2020 年 2 月 20 日

TiDB 版本：3.0.10

TiDB Ansible 版本：3.0.10

> **警告：**
>
> 该版本存在一些已知问题，已在新版本中修复，建议使用 3.0.x 的最新版本。

## TiDB

- 修复 IndexLookUpJoin 在利用 OtherCondition 构造 InnerRange 时出现错误 Join 结果 [#14599](https://github.com/pingcap/tidb/pull/14599)
- 删除 `tidb_pprof_sql_cpu` 配置项，新增 Server 级别的 `tidb_pprof_sql_cpu` 变量 [#14416](https://github.com/pingcap/tidb/pull/14416)
- 修复用户只在具有全局权限时才能查询所有数据库的问题 [#14386](https://github.com/pingcap/tidb/pull/14386)
- 修复执行 point-get 时由于事务超时导致数据的可见性不符合预期的问题 [#14480](https://github.com/pingcap/tidb/pull/14480)
- 将悲观事务激活的时机改为延迟激活，与乐观事务模型保持一致 [#14474](https://github.com/pingcap/tidb/pull/14474)
- 修复 unixtimestamp 表达式在计算分区表分区的时区不正确的问题 [#14476](https://github.com/pingcap/tidb/pull/14476)
- 新增`tidb_session_statement_deadlock_detect_duration_seconds` 监控项，用于监控死锁检测时间 [#14484](https://github.com/pingcap/tidb/pull/14484)
- 修复 GC worker 由于部分逻辑不正确导致系统 panic 的问题 [#14439](https://github.com/pingcap/tidb/pull/14439)
- 修复 IsTrue 函数的表达式名称不正确的问题 [#14516](https://github.com/pingcap/tidb/pull/14516)
- 修复部分内存使用统计不准确的问题 [#14533](https://github.com/pingcap/tidb/pull/14533)
- 修复统计信息 CM-Sketch 初始化时由于处理逻辑不正确导致系统 panic 的问题 [#14470](https://github.com/pingcap/tidb/pull/14470)
- 修复查询分区表时分区裁剪 (partition pruning) 不准确的问题 [#14546](https://github.com/pingcap/tidb/pull/14546)
- 修复 SQL 绑定中 SQL 语句默认数据库名设置不正确的问题 [#14548](https://github.com/pingcap/tidb/pull/14548)
- 修复 json_key 与 MySQL 不兼容的问题 [#14561](https://github.com/pingcap/tidb/pull/14561)
- 新增分区表自动更新统计信息的功能 [#14566](https://github.com/pingcap/tidb/pull/14566)
- 修复执行 point-get 时 plan id 会变化的问题，正常情况 plan id 始终是 1 [#14595](https://github.com/pingcap/tidb/pull/14595)
- 修复 SQL 绑定不完全匹配时处理逻辑不正确导致系统 panic 的问题 [#14263](https://github.com/pingcap/tidb/pull/14263)
- 新增 `tidb_session_statement_pessimistic_retry_count` 监控项，用于监控悲观事务加锁失败后重试次数 [#14619](https://github.com/pingcap/tidb/pull/14619)
- 修复 `show binding` 语句权限检查不正确的问题 [#14618](https://github.com/pingcap/tidb/pull/14618)
- 修复由于 backoff 的逻辑里没有检查 killed 标记，导致 kill 无法正确执行的问题 [#14614](https://github.com/pingcap/tidb/pull/14614)
- 通过减少持有内部锁的时间来提高 statement summary 的性能 [#14627](https://github.com/pingcap/tidb/pull/14627)
- 修复 TiDB 从字符串解析成时间与 MySQL 不兼容的问题 [#14570](https://github.com/pingcap/tidb/pull/14570)
- 新增审计日志记录用户登录失败的功能 [#14620](https://github.com/pingcap/tidb/pull/14620)
- 新增 `tidb_session_ statement_lock_keys_count` 监控项，用于监控悲观事务的 lock keys 的数量 [#14634](https://github.com/pingcap/tidb/pull/14634)
- 修复 json 对 `&` `<` `>` 等字符输出转义不正确的问题 [#14637](https://github.com/pingcap/tidb/pull/14637)
- 修复 hash-join 在建 hash-table 时由于内存使用过多导致系统 panic 的问题 [#14642](https://github.com/pingcap/tidb/pull/14642)
- 修复 SQL 绑定处理不合法记录时处理逻辑不正确导致 panic 的问题 [#14645](https://github.com/pingcap/tidb/pull/14645)
- 修复 Decimal 除法计算与 MySQL 不兼容的问题，Decimal 除法计算中增加 Truncated 错误检测 [#14673](https://github.com/pingcap/tidb/pull/14673)
- 修复给用户授权不存在的表执行成功的问题 [#14611](https://github.com/pingcap/tidb/pull/14611)

## TiKV

+ Raftstore
    - 修复由于 Region merge 失败导致系统 Panic [#6460](https://github.com/tikv/tikv/issues/6460) 或者数据丢失 [#598](https://github.com/tikv/tikv/issues/5981) 的问题 [#6481](https://github.com/tikv/tikv/pull/6481)
    - 支持 yield 优化调度公平性，支持预迁移 leader 优化 leader 调度的稳定性 [#6563](https://github.com/tikv/tikv/pull/6563)

## PD

- 当系统流量有变化时，系统自动更新 Region 缓存信息，解决缓存失效的问题 [#2103](https://github.com/pingcap/pd/pull/2103)
- 采用 leader 租约时间确定 TSO 的有效时间 [#2117](https://github.com/pingcap/pd/pull/2117)

## Tools

+ TiDB Binlog
    - Drainer 支持 relay log [#893](https://github.com/pingcap/tidb-binlog/pull/893)
+ TiDB Lightning
    - 优化配置项，部分配置项在没有设置的时候使用默认配置 [#255](https://github.com/pingcap/tidb-lightning/pull/255)
    - 修复在非 server mode 模式下 web 界面无法打开的问题 [#259](https://github.com/pingcap/tidb-lightning/pull/259)

## TiDB Ansible

- 修复某些场景获取不到 PD Leader 导致命令执行失败的问题 [#1121](https://github.com/pingcap/tidb-ansible/pull/1121)
- TiDB Dashboard 新增 `Deadlock Detect Duration` 监控项 [#1127](https://github.com/pingcap/tidb-ansible/pull/1127)
- TiDB Dashboard 新增 `Statement Lock Keys Count` 监控项 [#1132](https://github.com/pingcap/tidb-ansible/pull/1132)
- TiDB Dashboard 新增 `Statement Pessimistic Retry Count` 监控项 [#1133](https://github.com/pingcap/tidb-ansible/pull/1133)
