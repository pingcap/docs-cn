---
title: TiDB 2.1.18 Release Notes
aliases: ['/docs/dev/releases/release-2.1.18/','/docs/dev/releases/2.1.18/']
---

# TiDB 2.1.18 Release Notes

Release date: November 4, 2019

TiDB version: 2.1.18

TiDB Ansible version: 2.1.18

## TiDB

+ SQL Optimizer
    - Fix the issue that invalid query ranges might appear when split by feedback [#12172](https://github.com/pingcap/tidb/pull/12172)
    - Fix the issue that the privilege check is incorrect in point get plan [#12341](https://github.com/pingcap/tidb/pull/12341)
    - Optimize execution performance of the `select ... limit ... offset …` statement by pushing the Limit operator down to the `IndexLookUpReader` execution logic [#12380](https://github.com/pingcap/tidb/pull/12380)
    - Support using parameters in `ORDER BY`, `GROUP BY` and `LIMIT OFFSET` [#12514](https://github.com/pingcap/tidb/pull/12514)
    - Fix the issue that `IndexJoin` on the partition table returns incorrect results [#12713](https://github.com/pingcap/tidb/pull/12713)
    - Fix the issue that the `str_to_date` function in TiDB returns a different result from MySQL when the date string and the format string do not match [#12757](https://github.com/pingcap/tidb/pull/12757)
    - Fix the issue that outer join is incorrectly converted to inner join when the `cast` function is included in the query conditions [#12791](https://github.com/pingcap/tidb/pull/12791)
    - Fix incorrect expression passing in the join condition of `AntiSemiJoin` [#12800](https://github.com/pingcap/tidb/pull/12800)
+ SQL Engine
    - Fix the incorrectly rounding of time (for example, `2019-09-11 11:17:47.999999666` should be rounded to `2019-09-11 11:17:48`) [#12259](https://github.com/pingcap/tidb/pull/12259)
    - Fix the issue that the duration by `sql_type` for the `PREPARE` statement is not shown in the monitoring record [#12329](https://github.com/pingcap/tidb/pull/12329)
    - Fix the panic issue when the `from_unixtime` function handles null [#12572](https://github.com/pingcap/tidb/pull/12572)
    - Fix the compatibility issue that when an invalid value is inserted as the `YEAR` type, the result is `NULL` instead of `0000` [#12744](https://github.com/pingcap/tidb/pull/12744)
    - Improve the behavior of the `AutoIncrement` column when it is implicitly allocated, to keep it consistent with the default mode of MySQL auto-increment locking (["consecutive" lock mode](https://dev.mysql.com/doc/refman/5.7/en/innodb-auto-increment-handling.html)): for the implicit allocation of multiple `AutoIncrement` IDs in a single-line `Insert` statement, TiDB guarantees the continuity of the allocated values. This improvement ensures that the JDBC `getGeneratedKeys()` method will get the correct results in any scenario [#12619](https://github.com/pingcap/tidb/pull/12619)
    - Fix the issue that the query is hanged when `HashAgg` serves as a child node of `Apply` [#12769](https://github.com/pingcap/tidb/pull/12769)
    - Fix the issue that the `AND` and `OR` logical expressions return incorrect results when it comes to type conversion [#12813](https://github.com/pingcap/tidb/pull/12813)
+ Server
    - Fix the issue that the `SLEEP()` function is invalid for the `KILL TIDB QUERY` statements [#12159](https://github.com/pingcap/tidb/pull/12159)
    - Fix the issue that no error is reported when `AUTO_INCREMENT` incorrectly allocates `MAX int64` and `MAX uint64` [#12210](https://github.com/pingcap/tidb/pull/12210)
    - Fix the issue that the slow query logs are not recorded when the log level is `ERROR` [#12373](https://github.com/pingcap/tidb/pull/12373)
    - Adjust the number of times that TiDB caches schema changes and corresponding changed table information from 100 to 1024, and support modification by using the `tidb_max_delta_schema_count` system variable [#12515](https://github.com/pingcap/tidb/pull/12515)
    - Change the query start time from the point of "starting to execute" to “starting to compile” to make SQL statistics more accurate [#12638](https://github.com/pingcap/tidb/pull/12638)
    - Add the record of `set session autocommit` in TiDB logs [#12568](https://github.com/pingcap/tidb/pull/12568)
    - Record SQL query start time in `SessionVars` to prevent it from being reset during plan execution [#12676](https://github.com/pingcap/tidb/pull/12676)
    - Support `?` placeholder in `ORDER BY`, `GROUP BY` and `LIMIT OFFSET` [#12514](https://github.com/pingcap/tidb/pull/12514)
    - Add the `Prev_stmt` field in slow query logs to output the previous statement when the last statement is `COMMIT` [#12724](https://github.com/pingcap/tidb/pull/12724)
    - Record the last statement before `COMMIT` into the log when the `COMMIT` fails in an explicitly committed transaction [#12747](https://github.com/pingcap/tidb/pull/12747)
    - Optimize the saving method of the previous statement when the TiDB server executes a SQL statement to improve performance [#12751](https://github.com/pingcap/tidb/pull/12751)
    - Fix the panic issue caused by `FLUSH PRIVILEGES` statements under the `skip-grant-table=true` configuration [#12816](https://github.com/pingcap/tidb/pull/12816)
    - Increase the default minimum step of applying AutoID from `1000` to `30000` to avoid performance bottleneck when there are many write requests in a short time [#12891](https://github.com/pingcap/tidb/pull/12891)
    - Fix the issue that the failed `Prepared` statement is not print in the error log when TiDB panics [#12954](https://github.com/pingcap/tidb/pull/12954)
    - Fix the issue that the `COM_STMT_FETCH` time record in slow query logs is inconsistent with that in MySQL [#12953](https://github.com/pingcap/tidb/pull/12953)
    - Add an error code in the error message for write conflicts to quickly locate the cause [#12878](https://github.com/pingcap/tidb/pull/12878)
+ DDL
    - Disallow dropping the `AUTO INCREMENT` attribute of a column by default. Modify the value of the `tidb_allow_remove_auto_inc` variable if you do need to drop this attribute. See [System Variables](/system-variables.md#tidb_allow_remove_auto_inc-new-in-v2118-and-v304) for more details. [#12146](https://github.com/pingcap/tidb/pull/12146)
    - Support multiple `unique`s when creating a unique index in the `Create Table` statement [#12469](https://github.com/pingcap/tidb/pull/12469)
    - Fix a compatibility issue that if the foreign key constraint in `CREATE TABLE` statement has no schema, schema of the created table should be used instead of returning a `No Database selected` error [#12678](https://github.com/pingcap/tidb/pull/12678)
    - Fix the issue that the `invalid list index` error is reported when executing `ADMIN CANCEL DDL JOBS` [#12681](https://github.com/pingcap/tidb/pull/12681)
+ Monitor
    - Add types for backoff monitoring and supplement the backoff time that is not recorded before, such as the backoff time when committing [#12326](https://github.com/pingcap/tidb/pull/12326)
    - Add a new metric to monitor `Add Index` operation progress [#12389](https://github.com/pingcap/tidb/pull/12389)

## PD

- Improve the `--help` command output of pd-ctl [#1772](https://github.com/pingcap/pd/pull/1772)

## Tools

+ TiDB Binlog
    - Fix the issue that `ALTER DATABASE` related DDL operations cause Drainer to exit abnormally [#770](https://github.com/pingcap/tidb-binlog/pull/770)
    - Support querying the transaction status information for Commit binlog to improve replication efficiency [#761](https://github.com/pingcap/tidb-binlog/pull/761)
    - Fix the issue that a Pump panic might occur when Drainer's `start_ts` is greater than Pump's largest `commit_ts` [#759](https://github.com/pingcap/tidb-binlog/pull/759)

## TiDB Ansible

- Add two monitoring items "queue size" and “query histogram” for TiDB Binlog [#952](https://github.com/pingcap/tidb-ansible/pull/952)
- Update TiDB alerting rules [#961](https://github.com/pingcap/tidb-ansible/pull/961)
- Check the configuration file before the deployment and upgrade [#973](https://github.com/pingcap/tidb-ansible/pull/973)
- Add a new metric to monitor index speed in TiDB [#987](https://github.com/pingcap/tidb-ansible/pull/987)
- Update TiDB Binlog monitoring dashboard to make it compatible with Grafana v4.6.3 [#993](https://github.com/pingcap/tidb-ansible/pull/993)
