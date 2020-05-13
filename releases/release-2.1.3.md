---
title: TiDB 2.1.3 Release Notes
category: Releases
---

# TiDB 2.1.3 Release Notes

2019 年 01 月 28 日，TiDB 发布 2.1.3 版，TiDB Ansible 相应发布 2.1.3 版本。相比 2.1.2 版本，该版本对系统稳定性、优化器、统计信息以及执行引擎做了很多改进。

## TiDB

+ 优化器/执行器
    - 修复某些情况下 Prepared Plan Cache panic 的问题 [#8826](https://github.com/pingcap/tidb/pull/8826)
    - 修复在有前缀索引的某些情况下，Range 计算错误的问题 [#8851](https://github.com/pingcap/tidb/pull/8851)
    - 当 `SQL_MODE` 不为 STRICT 时, `CAST(str AS TIME(N))` 在 `str` 为非法的 TIME 格式的字符串时返回 NULL [#8966](https://github.com/pingcap/tidb/pull/8966)
    - 修复某些情况下 Generated Column 在 Update 中 Panic 的问题 [#8980](https://github.com/pingcap/tidb/pull/8980)
    - 修复统计信息直方图某些情况下上界溢出的问题 [#8989](https://github.com/pingcap/tidb/pull/8989)
    - 支持对 `_tidb_rowid` 构造查询的 Range，避免全表扫，减轻集群压力 [#9059](https://github.com/pingcap/tidb/pull/9059)
    - `CAST(AS TIME)` 在精度太大的情况下返回一个错误 [#9058](https://github.com/pingcap/tidb/pull/9058)
    - 允许把 `Sort Merge Join` 用于笛卡尔积 [#9037](https://github.com/pingcap/tidb/pull/9037)
    - 修复统计信息的 worker 在某些情况下 panic 之后无法恢复的问题 [#9085](https://github.com/pingcap/tidb/pull/9085)
    - 修复某些情况下 `Sort Merge Join` 结果不正确的问题 [#9046](https://github.com/pingcap/tidb/pull/9046)
    - 支持在 `CASE` 子句返回 JSON 类型 [#8355](https://github.com/pingcap/tidb/pull/8355)
+ Server
    - 当语句中有非 TiDB hint 的注释时返回警告，而不是错误 [#8766](https://github.com/pingcap/tidb/pull/8766)
    - 验证设置的 TIMEZONE 的合法性 [#8879](https://github.com/pingcap/tidb/pull/8879)
    - 优化 Metrics 项 `QueryDurationHistogram`，展示更多语句的类型 [#8875](https://github.com/pingcap/tidb/pull/8875)
    - 修复 bigint 某些情况下下界溢出的问题 [#8544](https://github.com/pingcap/tidb/pull/8544)
    - 支持 `ALLOW_INVALID_DATES` SQL mode [#9110](https://github.com/pingcap/tidb/pull/9110)
+ DDL
    - 修复一个 RENAME TABLE 的兼容性问题，保持行为跟 MySQL 一致 [#8808](https://github.com/pingcap/tidb/pull/8808)
    - 支持 `ADD INDEX` 的并发修改即时生效 [#8786](https://github.com/pingcap/tidb/pull/8786)
    - 修复在 `ADD COLUMN` 的过程中，某些情况 Update 语句 panic 的问题 [#8906](https://github.com/pingcap/tidb/pull/8906)
    - 修复某些情况下并发创建 Table Partition 的问题 [#8902](https://github.com/pingcap/tidb/pull/8902)
    - 支持把 `utf8` 字符集转换为 `utf8mb4` 字符集 [#8951](https://github.com/pingcap/tidb/pull/8951) [#9152](https://github.com/pingcap/tidb/pull/9152)
    - 处理 Shard Bits 溢出的问题 [#8976](https://github.com/pingcap/tidb/pull/8976)
    - 支持 `SHOW CREATE TABLE` 输出列的字符集 [#9053](https://github.com/pingcap/tidb/pull/9053)
    - 修复 varchar 最大支持字符数在 `utf8mb4` 下限制的问题 [#8818](https://github.com/pingcap/tidb/pull/8818)
    - 支持 `ALTER TABLE TRUNCATE TABLE PARTITION` [#9093](https://github.com/pingcap/tidb/pull/9093)
    - 修复创建表的时候缺省字符集推算的问题 [#9147](https://github.com/pingcap/tidb/pull/9147)

## PD

- 修复 Leader 选举相关的 Watch 问题 [#1396](https://github.com/pingcap/pd/pull/1396)

## TiKV

- 支持了使用 HTTP 方式获取监控信息 [#3855](https://github.com/tikv/tikv/pull/3855)
- 修复 `data_format` 遇到 NULL 时的问题 [#4075](https://github.com/tikv/tikv/pull/4075)
- 添加验证 Scan 请求的边界合法性 [#4124](https://github.com/tikv/tikv/pull/4124)

## Tools

+ TiDB Binlog
    - 修复在启动或者重启时 `no available pump` 的问题 [#157](https://github.com/pingcap/tidb-tools/pull/158)
    - 开启 Pump client log 输出 [#165](https://github.com/pingcap/tidb-tools/pull/165)
    - 修复表只有 unique key 没有 primary key 的情况下，unique key 包含 NULL 值导致数据更新不一致的问题
  