---
title: TiDB 3.0.14 Release Notes
aliases: ['/docs/dev/releases/release-3.0.14/','/docs/dev/releases/3.0.14/']
summary: TiDB 3.0.14 was released on May 9, 2020. The release includes compatibility changes, important bug fixes, new features, bug fixes, and improvements for TiDB, TiKV, and Tools. Some of the bug fixes include issues with query results, panic occurrences, and incorrect behavior. New features include enhanced syntax support and improved performance.
---

# TiDB 3.0.14 Release Notes

Release date: May 9, 2020

TiDB version: 3.0.14

## Compatibility Changes

+ TiDB

    - Adjust the user privilege in `performance_schema` and `metrics_schema` from read-write to read-only [#15417](https://github.com/pingcap/tidb/pull/15417)

## Important Bug Fixes

+ TiDB

    - Fix the issue that the query result of `index join` is incorrect when the `join` condition has multiple equivalent conditions on the column with the `handle` attribute [#15734](https://github.com/pingcap/tidb/pull/15734)
    - Fix the panic that occurs when performing the `fast analyze` operation on the column with the `handle` attribute [#16079](https://github.com/pingcap/tidb/pull/16079)
    - Fix the issue that the `query` field in the DDL job structure is incorrect when the DDL statement is executed in a way of `prepare`. This issue might cause data inconsistency between the upstream and the downstream when Binlog is used for data replication. [#15443](https://github.com/pingcap/tidb/pull/15443)

+ TiKV

    - Fix the issue that repeated requests on the cleanup of lock might destroy the atomicity of the transaction [#7388](https://github.com/tikv/tikv/pull/7388)

## New Features

+ TiDB

    - Add the schema name column and the table name column to the query results of the `admin show ddl jobs` statement [#16428](https://github.com/pingcap/tidb/pull/16428)
    - Enhance the `RECOVER TABLE` syntax to support recovering truncated tables [#15458](https://github.com/pingcap/tidb/pull/15458)
    - Support the privilege check for the `SHOW GRANTS` statement [#16168](https://github.com/pingcap/tidb/pull/16168)
    - Support the privilege check for the `LOAD DATA` statement [#16736](https://github.com/pingcap/tidb/pull/16736)
    - Improve the performance of partition pruning when functions related to time and date are used as partition keys [#15618](https://github.com/pingcap/tidb/pull/15618)
    - Adjust the log level of `dispatch error` from `WARN` to `ERROR` [#16232](https://github.com/pingcap/tidb/pull/16232)
    - Support the `require-secure-transport` startup option to force clients to use TLS [#15415](https://github.com/pingcap/tidb/pull/15415)
    - Support HTTP communication between TiDB components when TLS is configured [#15419](https://github.com/pingcap/tidb/pull/15419)
    - Add the `start_ts` information of the current transaction to the `information_schema.processlist` table [#16160](https://github.com/pingcap/tidb/pull/16160)
    - Support automatically reloading the TLS certificate information used for communication among clusters [#15162](https://github.com/pingcap/tidb/pull/15162)
    - Improve the read performance of the partitioned tables by restructuring the partition pruning [#15628](https://github.com/pingcap/tidb/pull/15628)
    - Support the partition pruning feature when `floor(unix_timestamp(a))` is used as the partition expression of the `range` partition table [#16521](https://github.com/pingcap/tidb/pull/16521)
    - Allow executing the `update` statement that contains a `view` and does not update the `view` [#16787](https://github.com/pingcap/tidb/pull/16787)
    - Prohibit creating nested `view`s [#15424](https://github.com/pingcap/tidb/pull/15424)
    - Prohibit truncating `view` [#16420](https://github.com/pingcap/tidb/pull/16420)
    - Prohibit using the `update` statement to explicitly update the values of a column when this column is not in the `public` state [#15576](https://github.com/pingcap/tidb/pull/15576)
    - Prohibit starting TiDB when the `status` port is occupied [#15466](https://github.com/pingcap/tidb/pull/15466)
    - Change the character set of the `current_role` function from `binary` to `utf8mb4` [#16083](https://github.com/pingcap/tidb/pull/16083)
    - Improve `max-execution-time` usability by checking the interrupt signal when the data of a new Region is read [#15615](https://github.com/pingcap/tidb/pull/15615)
    - Add the `ALTER TABLE ... AUTO_ID_CACHE` syntax for explicitly setting the cache step of `auto_id` [#16287](https://github.com/pingcap/tidb/pull/16287)

+ TiKV

    - Improve the performance when many conflicts and the `BatchRollback` condition exist in optimistic transactions [#7605](https://github.com/tikv/tikv/pull/7605)
    - Fix the issue of decreased performance that occurs because the pessimistic lock `waiter` is frequently awakened when many conflicts exist in pessimistic transactions [#7584](https://github.com/tikv/tikv/pull/7584)

+ Tools

    + TiDB Lightning

        - Support printing the TiKV cluster mode using the `fetch-mode` sub-command of tidb-lightning-ctl [#287](https://github.com/pingcap/tidb-lightning/pull/287)

## Bug Fixes

+ TiDB

    - Fix the issue that `WEEKEND` function is not compatible with MySQL when the SQL mode is `ALLOW_INVALID_DATES` [#16170](https://github.com/pingcap/tidb/pull/16170)
    - Fix the issue that the `DROP INDEX` statement fails to execute when the index column contains the auto-increment primary key [#16008](https://github.com/pingcap/tidb/pull/16008)
    - Fix the issue of incorrect values of the `TABLE_NAMES` column in the Statement Summary [#15231](https://github.com/pingcap/tidb/pull/15231)
    - Fix the issue that some expressions have incorrect results when the plan cache is enabled [#16184](https://github.com/pingcap/tidb/pull/16184)
    - Fix the issue that the result of the `not`/`istrue`/`isfalse` function is incorrect [#15916](https://github.com/pingcap/tidb/pull/15916)
    - Fix the panic caused by the `MergeJoin` operation on tables with redundant indexes [#15919](https://github.com/pingcap/tidb/pull/15919)
    - Fix the issue caused by incorrectly simplifying the link when the predicate only refers to the outer table [#16492](https://github.com/pingcap/tidb/pull/16492)
    - Fix the issue that the `CURRENT_ROLE` function reports an error caused by the `SET ROLE` statement [#15569](https://github.com/pingcap/tidb/pull/15569)
    - Fix the issue that the result of the `LOAD DATA` statement is incompatible with MySQL when this statement encounters `\` [#16633](https://github.com/pingcap/tidb/pull/16633)
    - Fix the issue that the database visibility is incompatible with MySQL [#14939](https://github.com/pingcap/tidb/pull/14939)
    - Fix the issue of incorrect privilege check for the `SET DEFAULT ROLE ALL` statement [#15585](https://github.com/pingcap/tidb/pull/15585)
    - Fix the issue of partition pruning failure caused by the plan cache [#15818](https://github.com/pingcap/tidb/pull/15818)
    - Fix the issue that `schema change` is reported during the transaction commit when concurrent DDL operations are performed on a table and blocking exists, because the transaction does not lock the related table [#15707](https://github.com/pingcap/tidb/pull/15707)
    - Fix the incorrect behavior of `IF(not_int, *, *)` [#15356](https://github.com/pingcap/tidb/pull/15356)
    - Fix the incorrect behavior of `CASE WHEN (not_int)` [#15359](https://github.com/pingcap/tidb/pull/15359)
    - Fix the issue that the `Unknown column` error message is returned when using a `view` that is not in the current schema [#15866](https://github.com/pingcap/tidb/pull/15866)
    - Fix the issue that the result of parsing time strings is incompatible with MySQL [#16242](https://github.com/pingcap/tidb/pull/16242)
    - Fix the possible panic of the collation operator in `left join` when a `null` column exists in the right child node [#16528](https://github.com/pingcap/tidb/pull/16528)
    - Fix the issue that no error message is returned even though the SQL execution is blocked when TiKV keeps returning the `StaleCommand` error message [#16528](https://github.com/pingcap/tidb/pull/16528)
    - Fix the possible panic caused by the port probing when the audit plugin is enabled [#15967](https://github.com/pingcap/tidb/pull/15967)
    - Fix the panic caused when `fast analyze` works on indices only [#15967](https://github.com/pingcap/tidb/pull/15967)
    - Fix the possible panic of the `SELECT * FROM INFORMATION_SCHEMA.PROCESSLIST` statement execution in some cases [#16309](https://github.com/pingcap/tidb/pull/16309)
    - Fix the issue of TiDB OOM caused by specifying a large number of partitions (for example, `9999999999999`) when the hash partition table is created without checking the number of partitions before allocating memory [#16218](https://github.com/pingcap/tidb/pull/16218)
    - Fix the issue of incorrect information of partitioned tables in `information_schema.tidb_hot_table` [#16726](https://github.com/pingcap/tidb/pull/16726)
    - Fix the issue that the partition selection algorithm does not take effect on the hash partitioned table [#16070](https://github.com/pingcap/tidb/pull/16070)
    - Fix the issue that the HTTP API of the MVCC series does not support partitioned tables [#16191](https://github.com/pingcap/tidb/pull/16191)
    - Keep the error handling of the `UNION` statement consistent with that of the `SELECT` statement [#16137](https://github.com/pingcap/tidb/pull/16137)
    - Fix the issue of incorrect behavior when the parameter type of the `VALUES` function is `bit(n)` [#15486](https://github.com/pingcap/tidb/pull/15486)
    - Fix the issue that the processing logic of TiDB is inconsistent with MySQL when the `view` column name is too long. In this case, the system automatically generates a short column name. [#14873](https://github.com/pingcap/tidb/pull/14873 )
    - Fix the issue that `(not not col)` is incorrectly optimized as `col` [#16094](https://github.com/pingcap/tidb/pull/16094)
    - Fix the issue of incorrect `range` of the inner table built by `IndexLookupJoin` plans [#15753](https://github.com/pingcap/tidb/pull/15753)
    - Fix the issue that `only_full_group_by` fails to correctly check expressions with brackets [#16012](https://github.com/pingcap/tidb/pull/16012)
    - Fix the issue that an error is returned when the `select view_name.col_name from view_name` statement is executed [#15572](https://github.com/pingcap/tidb/pull/15572)

+ TiKV

    - Fix the issue that the node cannot be deleted correctly after the isolation recovery in some cases [#7703](https://github.com/tikv/tikv/pull/7703)
    - Fix the issue of data loss during network isolation caused by the Region Merge operation [#7679](https://github.com/tikv/tikv/pull/7679)
    - Fix the issue that learner cannot be removed correctly in some cases [#7598](https://github.com/tikv/tikv/pull/7598)
    - Fix the issue that the scanning result of raw key-value pairs might be out of order [#7597](https://github.com/tikv/tikv/pull/7597)
    - Fix the issue of reconnection when the batch of Raft messages is too large [#7542](https://github.com/tikv/tikv/pull/7542)
    - Fix the issue of gRPC thread deadlock caused by the empty request [#7538](https://github.com/tikv/tikv/pull/7538)
    - Fix the issue that the processing logic of restarting the learner is incorrect during the merge process [#7457](https://github.com/tikv/tikv/pull/7457)
    - Fix the issue that repeated requests on the cleanup of lock might destroy the atomicity of the transaction [#7388](https://github.com/tikv/tikv/pull/7388)
