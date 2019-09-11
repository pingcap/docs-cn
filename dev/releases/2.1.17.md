---
title: TiDB 2.1.17 Release Notes
category: Releases
---

# TiDB 2.1.17 Release Notes

Release date: September 11, 2019

TiDB version: 2.1.17

TiDB Ansible version: 2.1.17

+ New features
    - Add the  `WHERE` clause in TiDB’s `SHOW TABLE REGIONS` syntax
    - Add the `config-check` feature in TiKV and PD to check the configuration items
    - Add the `remove-tomestone` command in pd-ctl to clear tombstone store records
    - Add the `worker-count` and `txn-batch` configuration items in Reparo to control the recovery speed

+ Improvements
    - Optimize PD’s scheduling process by supporting actively pushing operators
    - Optimize TiKV’s starting process to reduce jitters caused by restarting nodes

+ Changed behaviors
    - Change `start ts` in TiDB slow query logs from the last retry time to the first execution time
    - Replace the `Index_ids` field in TiDB slow query logs with the `Index_names` field to improve the usability of slow query logs
    - Add the `split-region-max-num` parameter in TiDB’s configuration files to modify the maximum number of Regions allowed by the `SPLIT TABLE` syntax, which is increased from 1,000 to 10,000 in the default configuration

## TiDB

+ SQL Optimizer
    - Fix the issue that the error message is not returned correctly when an error occurs during `EvalSubquery` building `Executor` [#11811](https://github.com/pingcap/tidb/pull/11811)
    - Fix the issue that the query result might be incorrect when the number of rows in the outer table is greater than that in a single batch in Index Lookup Join; expand the functional scope of Index Lookup Join; `UnionScan` can be used as a subnode of `IndexJoin` [#11843](https://github.com/pingcap/tidb/pull/11843)
    - Add the display of invalid keys (like `invalid encoded key flag 252` ) in the `SHOW STAT_BUCKETS` syntax, for the situation where invalid keys might occur during the statistics feedback process [#12098](https://github.com/pingcap/tidb/pull/12098)
+ SQL Execution Engine
    - Fix some incorrect results (like `select cast(13835058000000000000 as double)`) caused by the number value that is first converted to  `UINT` when the `CAST` function is converting the number value type [#11712](https://github.com/pingcap/tidb/pull/11712)
    - Fix the issue that the calculation result might be incorrect when the dividend of the `DIV` calculation is a decimal and this calculation contains a negative number [#11812](https://github.com/pingcap/tidb/pull/11812)
    - Add the `ConvertStrToIntStrict` function to fix the MySQL incompatibility issue caused by some strings being converted to the `INT` type when executing the `SELECT`/`EXPLAIN` statement [#11892](https://github.com/pingcap/tidb/pull/11892)
    - Fix the issue that the `Explain` result might be incorrect caused by wrong configuration of `stmtCtx` when `EXPLAIN ... FOR CONNECTION` is used [#11978](https://github.com/pingcap/tidb/pull/11978)
    - Fix the issue that the result returned by the `unaryMinus` function is incompatible with MySQL, caused by the non-decimal result when the integer result overflows [#11990](https://github.com/pingcap/tidb/pull/11990)
    - Fix the issue that `last_insert_id()` might be incorrect, caused by the counting order when the `LOAD DATA` statement is being executed [#11994](https://github.com/pingcap/tidb/pull/11994)
    - Fix the issue that `last_insert_id()` might be incorrect when the user writes auto-increment column data in an explicit-implicit mixed way [#12001](https://github.com/pingcap/tidb/pull/12001)
    - Fix an over-quoted bug for the `JSON_UNQUOTE` function: only values enclosed by double quote marks (`"`) should be unquoted. For example, the result of “`SELECT JSON_UNQUOTE("\\\\")`” should be “`\\`” (not changed) [#12096](https://github.com/pingcap/tidb/pull/12096)
+ Server
    - Change `start ts` recorded in slow query logs from the last retry time to the first execution time when retrying TiDB transactions [#11878](https://github.com/pingcap/tidb/pull/11878)
    - Add the number of keys of a transaction in `LockResolver` to avoid the scan operation on the whole Region and reduce costs of resolving locking when the number of keys is reduced [#11889](https://github.com/pingcap/tidb/pull/11889)
    - Fix the issue that the `succ` field value might be incorrect in slow query logs [#11886](https://github.com/pingcap/tidb/pull/11886)
    - Replace the `Index_ids` filed in slow query logs with the `Index_names` field to improve the usability of slow query logs [#12063](https://github.com/pingcap/tidb/pull/12063)
    - Fix the connection break issue caused by TiDB parsing `-` into EOF Error when `Duration` contains `-` (like `select time(‘--’)`) [#11910](https://github.com/pingcap/tidb/pull/11910)
    - Remove an invalid Region from `RegionCache` more quickly to reduce the number of requests sent to this Region [#11931](https://github.com/pingcap/tidb/pull/11931)
    - Fix the connection break issue caused by incorrectly handling the OOM panic issue when `oom-action = "cancel"` and OOM occurs in the `Insert Into … Select` syntax [#12126](https://github.com/pingcap/tidb/pull/12126)
+ DDL
    - Add the reverse scan interface for `tikvSnapshot` to efficiently query DDL history jobs. After using this interface, the execution time of `ADMIN SHOW DDL JOBS` is remarkably decreased [#11789](https://github.com/pingcap/tidb/pull/11789)
    - Improve the `CREATE TABLE ... PRE_SPLIT_REGION` syntax: change the number of pre-splitting Regions from 2^(N-1) to 2^N when `PRE_SPLIT_REGION = N` [#11797](https://github.com/pingcap/tidb/pull/11797/files)
    - Decrease the default parameter value for the background worker thread of the `Add Index` operation to avoid great impacts on online workloads [#11875](https://github.com/pingcap/tidb/pull/11875)
    - Improve the `SPLIT TABLE` syntax behavior: generate N data Region(s) and one index Region when `SPLIT TABLE ... REGIONS N` is used to divide Regions [#11929](https://github.com/pingcap/tidb/pull/11929)
    - Add the `split-region-max-num` parameter (`10000` by default) in the configuration file to make the maximum number of Regions allowed by the `SPLIT TABLE` syntax adjustable [#12080](https://github.com/pingcap/tidb/pull/12080)
    - Fix the issue that the `CREATE TABLE` clause cannot be parsed by the downstream MySQL, caused by uncommented `PRE_SPLIT_REGIONS` in this clause when the system writes the binlog [#12121](https://github.com/pingcap/tidb/pull/12121)
    - Add the `WHERE` sub-clause in `SHOW TABLE … REGIONS` and `SHOW TABLE .. INDEX … REGIONS` [#12124](https://github.com/pingcap/tidb/pull/12124)
+ Monitor
    - Add the `connection_transient_failure_count` monitoring metric to count gRPC connection errors of `tikvclient` [#12092](https://github.com/pingcap/tidb/pull/12092)

## TiKV

- Fix the incorrect result of counting keys in a Region in some cases [#5415](https://github.com/tikv/tikv/pull/5415)
- Add the `config-check` option in TiKV to check whether the TiKV configuration item is valid [#5391](https://github.com/tikv/tikv/pull/5391)
- Optimize the starting process to reduce jitters caused by restarting nodes [#5277](https://github.com/tikv/tikv/pull/5277)
- Optimize the resolving locking process in some cases to speed up resolving locking for transactions [#5339](https://github.com/tikv/tikv/pull/5339)
- Optimize the `get_txn_commit_info` process to speed up committing transactions [#5062](https://github.com/tikv/tikv/pull/5062)
- Simplify Raft-related logs [#5425](https://github.com/tikv/tikv/pull/5425)
- Resolve the issue that TiKV exits abnormally in some cases [#5441](https://github.com/tikv/tikv/pull/5441)

## PD

- Add the `config-check` option in PD to check whether the PD configuration item is valid [#1725](https://github.com/pingcap/pd/pull/1725)
- Add the `remove-tomestone` command in pd-ctl to support clearing tombstone store records [#1705](https://github.com/pingcap/pd/pull/1705)
- Support actively pushing operators to speed up scheduling [#1686](https://github.com/pingcap/pd/pull/1686)

## Tools

+ TiDB Binlog
    - Add  `worker-count` and `txn-batch` configuration items in Reparo to control the recovery speed [#746](https://github.com/pingcap/tidb-binlog/pull/746)
    - Optimize the memory usage of Drainer to improve the parallel execution efficiency [#735](https://github.com/pingcap/tidb-binlog/pull/735)
    - Fix the bug that Pump cannot quit normally in some cases [#739](https://github.com/pingcap/tidb-binlog/pull/739)
    - Optimize the processing logic of `LevelDB` in Pump to improve the execution efficiency of GC [#720](https://github.com/pingcap/tidb-binlog/pull/720)
+ TiDB Lightning
    - Fix the bug that tidb-lightning might crash caused by re-importing data from the checkpoint [#239](https://github.com/pingcap/tidb-lightning/pull/239)

## TiDB Ansible

- Update the Spark version to 2.4.3, and update the TiSpark version to 2.2.0 that is compatible with Spark 2.4.3 [#914](https://github.com/pingcap/tidb-ansible/pull/914), [#919](https://github.com/pingcap/tidb-ansible/pull/927)
- Fix the issue that there is a long waiting time when the remote machine password has expired [#937](https://github.com/pingcap/tidb-ansible/pull/937), [#948](https://github.com/pingcap/tidb-ansible/pull/948)
