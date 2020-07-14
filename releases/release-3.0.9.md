---
title: TiDB 3.0.9 Release Notes
aliases: ['/docs/dev/releases/release-3.0.9/','/docs/dev/releases/3.0.9/']
---

# TiDB 3.0.9 Release Notes

Release date: January 14, 2020

TiDB version: 3.0.9

TiDB Ansible version: 3.0.9

> **Warning:**
>
> Some known issues are found in this version, and these issues are fixed in new versions. It is recommended that you use the latest 3.0.x version.

## TiDB

+ Executor
    - Fix the incorrect result when the aggregate function is applied to the `ENUM` column and the collection column [#14364](https://github.com/pingcap/tidb/pull/14364)
+ Server
    - Support the `auto_increment_increment` and `auto_increment_offset` system variables [#14396](https://github.com/pingcap/tidb/pull/14396)
    - Add the `tidb_tikvclient_ttl_lifetime_reach_total` monitoring metric to monitor the number of pessimistic transactions with a TTL of 10 minutes [#14300](https://github.com/pingcap/tidb/pull/14300)
    - Output the SQL information in the log when the SQL query causes a panic during its execution [#14322](https://github.com/pingcap/tidb/pull/14322)
    - Add the `plan` and `plan_digest` fields in the statement summary table to record the `plan` that is being executed and the `plan` signature [#14285](https://github.com/pingcap/tidb/pull/14285)
    - Adjust the default value of the `stmt-summary.max-stmt-count` configuration item from `100` to `200` [#14285](https://github.com/pingcap/tidb/pull/14285)
    - Add the `plan_digest` field in the slow query table to record the `plan` signature [#14292](https://github.com/pingcap/tidb/pull/14292)
+ DDL
    - Fix the issue that the results of anonymous indexes created using `alter table ... add index` on the `primary` column is inconsistent with MySQL [#14310](https://github.com/pingcap/tidb/pull/14310)
    - Fix the issue that `VIEW`s are mistakenly dropped by the  `drop table` syntax [#14052](https://github.com/pingcap/tidb/pull/14052)
+ Planner
    - Optimize the performance of statements such as `select max(a), min(a) from t`. If an index exists in the `a` column, the statement is optimized to `select * from (select a from t order by a desc limit 1) as t1, (select a from t order by a limit 1) as t2` to avoid full table scan [#14410](https://github.com/pingcap/tidb/pull/14410)

## TiKV

+ Raftstore
    - Speed up the configuration change to speed up the Region scattering [#6421](https://github.com/tikv/tikv/pull/6421)
+ Transaction
    - Add the `tikv_lock_manager_waiter_lifetime_duration`, `tikv_lock_manager_detect_duration`, and `tikv_lock_manager_detect_duration`  monitoring metrics to monitor `waiter`s’ lifetime, the time cost of detecting deadlocks, and the status of `Wait` table [#6392](https://github.com/tikv/tikv/pull/6392)
    - Optimize the following configuration items to reduce transaction execution latency caused by changing Region leader or the leader of deadlock detector in extreme situations [#6429](https://github.com/tikv/tikv/pull/6429)
        - Change the default value of `wait-for-lock-time` from `3s` to `1s`
        - Change the default value of `wake-up-delay-duration` from `100ms` to `20ms`
    - Fix the issue that the leader of the deadlock detector might be incorrect during the Region Merge process [#6431](https://github.com/tikv/tikv/pull/6431)

## PD

+ Support using backlash `/` in the location label name [#2083](https://github.com/pingcap/pd/pull/2083)
+ Fix the incorrect statistics because the tombstone store is mistakenly included by the label counter [#2067](https://github.com/pingcap/pd/pull/2067)

## Tools

+ TiDB Binlog
    - Add the unique key information in the binlog protocol output by Drainer [#862](https://github.com/pingcap/tidb-binlog/pull/862)
    - Support using the encrypted password for database connection for Drainer [#868](https://github.com/pingcap/tidb-binlog/pull/868)

## TiDB Ansible

+ Support automatically creating directories to optimize the deployment of TiDB Lightning [#1105](https://github.com/pingcap/tidb-ansible/pull/1105)
