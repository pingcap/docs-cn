---
title: TiDB 3.0.16 Release Notes
---

# TiDB 3.0.16 Release Notes

发版日期：2020 年 7 月 3 日

TiDB 版本：3.0.16

## 优化

+ TiDB

    - 在 hash partition pruning 中支持 `is null` 过滤条件 [#17308](https://github.com/pingcap/tidb/pull/17308)
    - 为每个 Region 设置单独的 `Backoffer` 避免多个 Region 同时失败引起等待时间过长 [#17583](https://github.com/pingcap/tidb/pull/17583)
    - 添加新 partition 更新已有 partition 的分裂信息 [#17668](https://github.com/pingcap/tidb/pull/17668)
    - 丢弃来自 `delete` / `update` 语句的 feedbacks [#17841](https://github.com/pingcap/tidb/pull/17841)
    - 调整 `job.DecodeArgs` 中 `json.Unmarshal` 的使用以兼容新的 Go 版本 [#17887](https://github.com/pingcap/tidb/pull/17887)
    - 移除 `slow log` 和 `statement summary` 中一些敏感信息 [#18128](https://github.com/pingcap/tidb/pull/18128)
    - `Datetime` 解析的分隔符和 MySQL 兼容 [#17499](https://github.com/pingcap/tidb/pull/17499)
    - 解析日期的 `%h` 时限定在 `1..12` 范围内 [#17496](https://github.com/pingcap/tidb/pull/17496)

+ TiKV

    - 避免在收到 snapshot 之后发送心跳给 PD 以提高稳定性 [#8145](https://github.com/tikv/tikv/pull/8145)
    - 优化了 PD client 的日志 [#8091](https://github.com/tikv/tikv/pull/8091)

## Bug 修复

+ TiDB

    - 修复当锁住的 primary key 在当前事务被插入/删除时可能造成的结果不一致问题 [#18248](https://github.com/pingcap/tidb/pull/18248)
    - 修复因字段含义不一致导致日志中出现大量 `Got too many pings` gRPC 错误的问题 [#17944](https://github.com/pingcap/tidb/pull/17944)
    - 修复当 HashJoin 返回 `Null` 类型列可能造成的 panic 问题 [#17935](https://github.com/pingcap/tidb/pull/17935)
    - 修复访问被拒绝时的错误信息 [#17722](https://github.com/pingcap/tidb/pull/17722)
    - 修复 JSON 数据中 `int` 和 `float` 类型比较的问题 [#17715](https://github.com/pingcap/tidb/pull/17715)
    - 修复 Failpoint 测试造成的 data race 问题 [#17710](https://github.com/pingcap/tidb/pull/17710)
    - 修复 Region 预分裂超时在创建表时可能不生效的问题 [#17617](https://github.com/pingcap/tidb/pull/17617)
    - 修复 `BatchClient` 中因为失败可能导致的主动 panic [#17378](https://github.com/pingcap/tidb/pull/17378)
    - 修复 `FLASHBACK TABLE` 在某些情况下可能失败的问题 [#17165](https://github.com/pingcap/tidb/pull/17165)
    - 修复只有 string 列时 range 范围计算可能不准确的问题 [#16658](https://github.com/pingcap/tidb/pull/16658)
    - 修复 `only_full_group_by` 模式下的错误 [#16620](https://github.com/pingcap/tidb/pull/16620)
    - 修复 `case when` 函数返回字段长度不准确的问题 [#16562](https://github.com/pingcap/tidb/pull/16562)
    - 修复 `count` 聚合函数对 `decimal` 类型推断的问题 [#17702](https://github.com/pingcap/tidb/pull/17702)

+ TiKV

    - 修复了潜在的 ingest file 导致的读取结果错误的问题 [#8039](https://github.com/tikv/tikv/pull/8039)
    - 修复了多次 merge 过程中被隔离的节点上的副本无法被正确移除的问题 [#8005](https://github.com/tikv/tikv/pull/8005)

+ PD

    - 修复一些情况下使用 PD Control 查询 Region 报 `404` 错误的问题 [#2577](https://github.com/pingcap/pd/pull/2577)
