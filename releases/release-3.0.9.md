---
title: TiDB 3.0.9 Release Notes
---

# TiDB 3.0.9 Release Notes

发版日期：2020 年 1 月 14 日

TiDB 版本：3.0.9

TiDB Ansible 版本：3.0.9

> **警告：**
>
> 该版本存在一些已知问题，已在新版本中修复，建议使用 3.0.x 的最新版本。

## TiDB

+ Executor
    - 修复聚合函数作用于枚举和集合列时结果不正确的问题 [#14364](https://github.com/pingcap/tidb/pull/14364)
+ Server
    - 支持系统变量 `auto_increment_increment` 和 `auto_increment_offset` [#14396](https://github.com/pingcap/tidb/pull/14396)
    - 新增 `tidb_tikvclient_ttl_lifetime_reach_total` 监控项，监控悲观事务 TTL 达到 10 分钟的数量 [#14300](https://github.com/pingcap/tidb/pull/14300)
    - 执行 SQL 过程中当发生 panic 时输出导致 panic 的 SQL 信息 [#14322](https://github.com/pingcap/tidb/pull/14322)
    - statement summary 系统表新增 `plan` 和 `plan_digest` 字段，记录当前正在执行的 `plan` 和 `plan` 的签名 [#14285](https://github.com/pingcap/tidb/pull/14285)
    - 配置项 `stmt-summary.max-stmt-count` 的默认值从 `100` 调整至 `200` [#14285](https://github.com/pingcap/tidb/pull/14285)
    - slow query 表新增 `plan_digest` 字段，记录 `plan` 的签名 [#14292](https://github.com/pingcap/tidb/pull/14292)
+ DDL
    - 修复 `alter table ... add index` 语句创建匿名索引行为与 MySQL 不一致的问题 [#14310](https://github.com/pingcap/tidb/pull/14310)
    - 修复 `drop table` 错误删除视图的问题 [#14052](https://github.com/pingcap/tidb/pull/14052)
+ Planner
    - 提升类似 `select max(a), min(a) from t` 语句的性能。如果 `a` 列表上有索引，该语句会被优化为 `select * from (select a from t order by a desc limit 1) as t1, (select a from t order by a limit 1) as t2` 以避免全表扫 [#14410](https://github.com/pingcap/tidb/pull/14410)

## TiKV

+ Raftstore
    - 提升 Raft 成员变更的速度 [#6421](https://github.com/tikv/tikv/pull/6421)
+ Transaction
    - 新增 `tikv_lock_manager_waiter_lifetime_duration`、`tikv_lock_manager_detect_duration`、`tikv_lock_manager_detect_duration` 监控项，用于监控 `waiter` 的生命周期、死锁检测耗费时间、`wait table` 的状态 [#6392](https://github.com/tikv/tikv/pull/6422)
    - 通过优化配置项 `wait-for-lock-time` 默认值从 `3s` 调整到 `1s`、`wake-up-delay-duration` 默认值从 `100ms` 调整为 `20ms`，以降低极端场景下 Region Leader 切换、切换死锁检测的 leader 导致的事务执行延迟 [#6429](https://github.com/tikv/tikv/pull/6429)
    - 修复 Region Merge 过程中可能导致死锁检测器 leader 角色误判的问题 [#6431](https://github.com/tikv/tikv/pull/6431)

## PD

+ 新增 location label 的名字中允许使用斜杠 `/` 的功能 [#2083](https://github.com/pingcap/pd/pull/2083)
+ 修复因为不正确地统计了 tombstone 的标签，导致该统计信息不准的问题 [#2060](https://github.com/pingcap/pd/issues/2060)

## Tools

+ TiDB Binlog
    - Drainer 输出的 binlog 协议中新增 unique key 信息 [#862](https://github.com/pingcap/tidb-binlog/pull/862)
    - Drainer 支持使用加密后的数据库连接密码 [#868](https://github.com/pingcap/tidb-binlog/pull/868)

## TiDB Ansible

+ 优化 Lightning 部署，自动创建相关目录 [#1105](https://github.com/pingcap/tidb-ansible/pull/1105)
