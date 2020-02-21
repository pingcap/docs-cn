---
title: TiDB 2.1.15 Release Notes
category: Releases
---

# TiDB 2.1.15 Release Notes

Release date: July 16, 2019

TiDB version: 2.1.15

TiDB Ansible version: 2.1.15

## TiDB

+ Fix the issue that the `DATE_ADD` function returns wrong results due to incorrect alignment when dealing with microseconds [#11289](https://github.com/pingcap/tidb/pull/11289)
+ Fix the issue that an error is reported when the empty value in the string column is compared with `FLOAT` or `INT` [#11279](https://github.com/pingcap/tidb/pull/11279)
+ Fix the issue that the `INSERT` function fails to correctly return the `NULL` value when a parameter is `NULL` [#11249](https://github.com/pingcap/tidb/pull/11249)
+ Fix the issue that an error occurs when indexing the column of the non-string type and `0` length [#11215](https://github.com/pingcap/tidb/pull/11215)
+ Add the `SHOW TABLE REGIONS` statement to query the Region distribution of a table through SQL statements [#11238](https://github.com/pingcap/tidb/pull/11238)
+ Fix the issue that an error is reported when using the `UPDATE … SELECT` statement because the projection elimination is used to optimize rules in the `SELECT` subqueries [#11254](https://github.com/pingcap/tidb/pull/11254)
+ Add the `ADMIN PLUGINS ENABLE`/`ADMIN PLUGINS DISABLE` SQL statement to dynamically enable or disable plugins [#11189](https://github.com/pingcap/tidb/pull/11189)
+ Add the session connection information in the Audit plugin [#11189](https://github.com/pingcap/tidb/pull/11189)
+ Fix the panic issue that happens when a column is queried on multiple times and the returned result is `NULL` during point queries [#11227](https://github.com/pingcap/tidb/pull/11227)
+ Add the `tidb_scatter_region` configuration item to scatter table Regions when creating a table [#11213](https://github.com/pingcap/tidb/pull/11213)
+ Fix the data race issue caused by non-thread safe `rand.Rand` when using the `RAND` function [#11170](https://github.com/pingcap/tidb/pull/11170)
+ Fix the issue that the comparison result of integers and non-integers is incorrect in some cases [#11191](https://github.com/pingcap/tidb/pull/11191)
+ Support modifying the collation of a database or a table, but the character set of the database/table has to be UTF-8 or utf8mb4 [#11085](https://github.com/pingcap/tidb/pull/11085)
+ Fix the issue that the precision shown by the `SHOW CREATE TABLE` statement is incomplete when `CURRENT_TIMESTAMP` is used as the default value of the column and the float precision is specified [#11087](https://github.com/pingcap/tidb/pull/11087)

## TiKV

+ Unify the log format [#5083](https://github.com/tikv/tikv/pull/5083)
+ Improve the accuracy of Region's approximate size or keys in extreme cases to improve the accuracy of scheduling [#5085](https://github.com/tikv/tikv/pull/5085)

## PD

+ Unify the log format [#1625](https://github.com/pingcap/pd/pull/1625)

## Tools

TiDB Binlog

+ Optimize the Pump GC strategy and remove the restriction that the unconsumed binlog cannot be cleaned to make sure that the resources are not occupied for a long time [#663](https://github.com/pingcap/tidb-binlog/pull/663)

TiDB Lightning

+ Fix the import error that happens when the column names specified by the SQL dump are not in lowercase [#210](https://github.com/pingcap/tidb-lightning/pull/210)

## TiDB Ansible

+ Add the `parse duration` and `compile duration` monitoring items in TiDB Dashboard to monitor the time that it takes to parse SQL statements and execute compilation [#815](https://github.com/pingcap/tidb-ansible/pull/815)
