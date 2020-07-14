---
title: TiDB 3.0.10 Release Notes
aliases: ['/docs/dev/releases/release-3.0.10/','/docs/dev/releases/3.0.10/']
---

# TiDB 3.0.10 Release Notes

Release date: February 20, 2020

TiDB version: 3.0.10

TiDB Ansible version: 3.0.10

> **Warning:**
>
> Some known issues are found in this version, and these issues are fixed in new versions. It is recommended that you use the latest 3.0.x version.

## TiDB

- Fix wrong `Join` results when `IndexLookUpJoin` uses `OtherCondition` to construct `InnerRange` [#14599](https://github.com/pingcap/tidb/pull/14599)
- Delete the `tidb_pprof_sql_cpu` configuration item and add the `tidb_pprof_sql_cpu` variable [#14416](https://github.com/pingcap/tidb/pull/14416)
- Fix the issue that users can query all databases only when they have global privileges [#14386](https://github.com/pingcap/tidb/pull/14386)
- Fix the issue that data visibility does not meet expectations due to transaction timeout when executing `PointGet` operations [#14480](https://github.com/pingcap/tidb/pull/14480)
- Change the timing of pessimistic transaction activation to delayed activation, consistent with the optimistic transaction mode [#14474](https://github.com/pingcap/tidb/pull/14474)
- Fix the incorrect time zone results when the `unixtimestamp` expression calculates the time zone of the table partitions [#14476](https://github.com/pingcap/tidb/pull/14476)
- Add the `tidb_session_statement_deadlock_detect_duration_seconds` monitoring item to monitor deadlock detection duration [#14484](https://github.com/pingcap/tidb/pull/14484)
- Fix the system panic issue caused by some logic errors of GC workers [#14439](https://github.com/pingcap/tidb/pull/14439)
- Correct the expression name of the `IsTrue` function [#14516](https://github.com/pingcap/tidb/pull/14516)
- Fix the issue that some memory usage is counted inaccurately [#14533](https://github.com/pingcap/tidb/pull/14533)
- Fix the system panic issue caused by incorrect processing logic during CM-Sketch statistics initialization [#14470](https://github.com/pingcap/tidb/pull/14470)
- Fix the issue of inaccurate partition pruning when querying partitioned tables [#14546](https://github.com/pingcap/tidb/pull/14546)
- Fix the issue that the default database name of the SQL statement in SQL bindings is set incorrectly [#14548](https://github.com/pingcap/tidb/pull/14548)
- Fix the issue that `json_key` is not compatible with MySQL [#14561](https://github.com/pingcap/tidb/pull/14561)
- Add the feature of automatically updating the statistics of partitioned tables [#14566](https://github.com/pingcap/tidb/pull/14566)
- Fix the issue that the plan ID changes when the `PointGet` operation is executed (the plan ID is expected to be `1` always) [#14595](https://github.com/pingcap/tidb/pull/14595)
- Fix the system panic issue caused by incorrect processing logic when SQL bindings do not match exactly [#14263](https://github.com/pingcap/tidb/pull/14263)
- Add the `tidb_session_statement_pessimistic_retry_count` monitoring item to monitor the number of retries after the failure to lock pessimistic transactions [#14619](https://github.com/pingcap/tidb/pull/14619)
- Fix the incorrect privilege check for `show binding` statements [#14618](https://github.com/pingcap/tidb/pull/14618)
- Fix the issue that the query cannot be killed because the `backoff` logic does not include checking the `killed` tag [#14614](https://github.com/pingcap/tidb/pull/14614)
- Improve the performance of statement summary by reducing the time to hold internal locks [#14627](https://github.com/pingcap/tidb/pull/14627)
- Fix the issue that TiDB's result of parsing strings to time is incompatible with MySQL [#14570](https://github.com/pingcap/tidb/pull/14570)
- Record the user login failures in audit logs [#14620](https://github.com/pingcap/tidb/pull/14620)
- Add the `tidb_session_ statement_lock_keys_count` monitoring item to monitor the number of lock keys for pessimistic transactions [#14634](https://github.com/pingcap/tidb/pull/14634)
- Fix the issue that characters in JSON such as `&`, `<`, and `>` are incorrectly escaped [#14637](https://github.com/pingcap/tidb/pull/14637)
- Fix the system panic issue caused by excessive memory usage when the `HashJoin` operation is building a hash table [#14642](https://github.com/pingcap/tidb/pull/14642)
- Fix the panic issue caused by incorrect processing logic when an SQL binding processes illegal records [#14645](https://github.com/pingcap/tidb/pull/14645)
- ix a MySQL incompatibility issue by adding Truncated error detection to decimal division calculation [#14673](https://github.com/pingcap/tidb/pull/14673)
- Fix the issue of successfully granting users privileges on a table that does not exist [#14611](https://github.com/pingcap/tidb/pull/14611)

## TiKV

+ Raftstore
    - Fix the system panic issue #6460 or data loss issue #598 caused by Region merge failure [#6481](https://github.com/tikv/tikv/pull/6481)
    - Support `yield` to optimize scheduling fairness, and support pre-transfering the leader to improve leader scheduling stability [#6563](https://github.com/tikv/tikv/pull/6563)

## PD

- Fix the invalid cache issue by supporting automatically updating the Region cache information when the system traffic changes [#2103](https://github.com/pingcap/pd/pull/2103)
- Use leader lease time to determine TSO service validity [#2117](https://github.com/pingcap/pd/pull/2117)

## Tools

+ TiDB Binlog
    - Support relay log in Drainer [#893](https://github.com/pingcap/tidb-binlog/pull/893)
+ TiDB Lightning
    - Make some configuration items use default values when a config file is missing [#255](https://github.com/pingcap/tidb-lightning/pull/255)
    - Fix the issue that the web interface cannot be opened in the non-server mode [#259](https://github.com/pingcap/tidb-lightning/pull/259)

## TiDB Ansible

- Fix the issue that the command execution fails due to the failure to obtain PD leader in some scenarios [#1121](https://github.com/pingcap/tidb-ansible/pull/1121)
- Add the `Deadlock Detect Duration` monitoring item in the TiDB dashboard [#1127](https://github.com/pingcap/tidb-ansible/pull/1127)
- Add the `Statement Lock Keys Count` monitoring item in the TiDB dashboard [#1132](https://github.com/pingcap/tidb-ansible/pull/1132)
- Add the `Statement Pessimistic Retry Count` monitoring item in the TiDB dashboard [#1133](https://github.com/pingcap/tidb-ansible/pull/1133)
