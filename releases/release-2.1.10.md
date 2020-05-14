---
title: TiDB 2.1.10 Release Notes
category: Releases
---

# TiDB 2.1.10 Release Notes

Release date: May 22, 2019

TiDB version: 2.1.10

TiDB Ansible version: 2.1.10

## TiDB

- Fix the issue that some abnormalities cause incorrect table schema when using `tidb_snapshot` to read the history data [#10359](https://github.com/pingcap/tidb/pull/10359)
- Fix the issue that the `NOT` function causes wrong read results in some cases [#10363](https://github.com/pingcap/tidb/pull/10363)
- Fix the wrong behavior of `Generated Column` in the `Replace` or `Insert on duplicate update` statement [#10385](https://github.com/pingcap/tidb/pull/10385)
- Fix a bug of the `BETWEEN` function in the `DATE`/`DATETIME` comparison [#10407](https://github.com/pingcap/tidb/pull/10407)
- Fix the issue that a single line of a slow log that is too long causes an error report when using the `SLOW_QUERY` table to query a slow log [#10412](https://github.com/pingcap/tidb/pull/10412)
- Fix the issue that the result of `DATETIME` plus `INTERVAL` is not the same with that of MySQL in some cases [#10416](https://github.com/pingcap/tidb/pull/10416), [#10418](https://github.com/pingcap/tidb/pull/10418)
- Add the check for the invalid time of February in a leap year [#10417](https://github.com/pingcap/tidb/pull/10417)
- Execute the internal initialization operation limitation only in the DDL owner to avoid a large number of conflict error reports when initializing the cluster [#10426](https://github.com/pingcap/tidb/pull/10426)
- Fix the issue that `DESC` is incompatible with MySQL when the default value of the output timestamp column is `default current_timestamp on update current_timestamp` [#10337](https://github.com/pingcap/tidb/issues/10337)
- Fix the issue that an error occurs during the privilege check in the `Update` statement [#10439](https://github.com/pingcap/tidb/pull/10439)
- Fix the issue that wrong calculation of `RANGE` causes a wrong result in the `CHAR` column in some cases [#10455](https://github.com/pingcap/tidb/pull/10455)
- Fix the issue that the data might be overwritten after decreasing `SHARD_ROW_ID_BITS` [#9868](https://github.com/pingcap/tidb/pull/9868)
- Fix the issue that `ORDER BY RAND()` does not return random numbers [#10064](https://github.com/pingcap/tidb/pull/10064)
- Prohibit the `ALTER` statement modifying the precision of decimals [#10458](https://github.com/pingcap/tidb/pull/10458)
- Fix the compatibility issue of the `TIME_FORMAT` function with MySQL [#10474](https://github.com/pingcap/tidb/pull/10474)
- Check the parameter validity of `PERIOD_ADD` [#10430](https://github.com/pingcap/tidb/pull/10430)
- Fix the issue that the behavior of the invalid `YEAR` string in TiDB is incompatible with that in MySQL [#10493](https://github.com/pingcap/tidb/pull/10493)
- Support the `ALTER DATABASE` syntax [#10503](https://github.com/pingcap/tidb/pull/10503)
- Fix the issue that the `SLOW_QUERY` memory engine reports an error when no  `;` exists in the slow query statement [#10536](https://github.com/pingcap/tidb/pull/10536)
- Fix the issue that the `Add index` operation in partitioned tables cannot be canceled in some cases [#10533](https://github.com/pingcap/tidb/pull/10533)
- Fix the issue that the OOM panic cannot be recovered in some cases [#10545](https://github.com/pingcap/tidb/pull/10545)
- Improve the security of the DDL operation rewriting the table metadata [#10547](https://github.com/pingcap/tidb/pull/10547)

## PD

- Fix the issue that the priority of the leader does not take effect [#1533](https://github.com/pingcap/pd/pull/1533)

## TiKV

- Reject transferring the leader in a Region whose configuration has been changed recently to avoid transfer failure [#4684](https://github.com/tikv/tikv/pull/4684)
- Add the priority label for Coprocessor metrics [#4643](https://github.com/tikv/tikv/pull/4643)
- Fix the possible dirty read issue during transferring the leader [#4724](https://github.com/tikv/tikv/pull/4724)
- Fix the issue that `CommitMerge` causes the restart failure of TiKV in some cases [#4615](https://github.com/tikv/tikv/pull/4615)
- Fix unknown logs [#4730](https://github.com/tikv/tikv/pull/4730)

## Tools

- TiDB Lightning
    - Add the retry feature when TiDB Lightning fails to send data to `importer` [#176](https://github.com/pingcap/tidb-lightning/pull/176)
- TiDB Binlog
    - Optimize the Pump storage log to facilitate troubleshooting [#607](https://github.com/pingcap/tidb-binlog/pull/607)

## TiDB Ansible

- Update the configuration file of TiDB Lightning and add the `tidb_lightning_ctl` script [#d3a4a368](https://github.com/pingcap/tidb-ansible/commit/d3a4a368810a421c49980899a286cf010569b4c7)