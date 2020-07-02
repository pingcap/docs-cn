---
title: TiDB 3.0.16 Release Notes
category: Releases
---

# TiDB 3.0.16 Release Notes

发版日期：2020 年 7 月 3 日

TiDB 版本：3.0.16

+ TiDB
    - 修复当锁住的 primary key 在当前事务被插入/删除时可能造成的结果不一致问题 [#18248](https://github.com/pingcap/tidb/pull/18248)
    - 修复因字段含义不一致导致日志中出现大量 "Got too many pings" grpc 错误的问题 [#17944](https://github.com/pingcap/tidb/pull/17944)
    - 修复当 HashJoin 返回 Null 类型列可能造成的 panic 问题 [#17935](https://github.com/pingcap/tidb/pull/17935)
    - 调整 job.DecodeArgs 中 json.Unmarshal 的使用以兼容新的 Go 版本 [#17887](https://github.com/pingcap/tidb/pull/17887)
    - 丢弃来自 `delete` / `update` 语句的 feedbacks [#17841](https://github.com/pingcap/tidb/pull/17841)
    - 调整访问被拒绝时的错误信息 [#17722](https://github.com/pingcap/tidb/pull/17722)
    - 修复 JSON 数据中 int 和 float 类型比较的问题 [#17715](https://github.com/pingcap/tidb/pull/17715)
    - 修复 Failpoint 测试造成的 DATA RACE 问题 [#17710](https://github.com/pingcap/tidb/pull/17710)
    - 修复 region 预分裂超时在创建表时可能不生效的问题 [#17617](https://github.com/pingcap/tidb/pull/17617)
    - 去掉 BatchClient 中因为失败可能导致的主动 panic [#17378](https://github.com/pingcap/tidb/pull/17378)
    - 在 hash partition pruning 中支持 `is null` 过滤条件 [#17308](https://github.com/pingcap/tidb/pull/17308)
    - 修复 flashback 表某些情况下可能失败的问题 [#17165](https://github.com/pingcap/tidb/pull/17165)
    - 修复只有 string 列时 range 范围计算可能不准确的问题 [#16658](https://github.com/pingcap/tidb/pull/16658)
    - 修复 `only_full_group_by` 模式下的错误 [#16620](https://github.com/pingcap/tidb/pull/16620)
    - 修复 `case when` 函数返回字段长度不准确的问题 [#16562](https://github.com/pingcap/tidb/pull/16562)


## Bug 修复

+ TiDB

    - 移除 `slow log` 和 `statement summary` 中一些敏感信息 [#18128](https://github.com/pingcap/tidb/pull/18128)
    - 修复 `count` 聚合函数对 `decimal` 类型推断的问题 [#17702](https://github.com/pingcap/tidb/pull/17702)
    - 添加新 partition 更新已有 partition 的分裂信息 [#17668](https://github.com/pingcap/tidb/pull/17668)
    - 为每个 `region` 设置单独的 `Backoff` 避免多个 `region` 同时失败引起等待时间过长 [#17583](https://github.com/pingcap/tidb/pull/17583)


+ TiKV



+ PD

    - 修复一些情况下使用 pd-ctl 查询 Region 报 404 错误的问题
