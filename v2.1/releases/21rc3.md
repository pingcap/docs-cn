---
title: TiDB 2.1 RC3 Release Notes
category: Releases
---

# TiDB 2.1 RC3 Release Notes

On September 29, 2018, TiDB 2.1 RC3 is released. Compared with TiDB 2.1 RC2, this release has great improvement in stability, compatibility, SQL optimizer, and execution engine.

## TiDB

+ SQL Optimizer
    - Fix the incorrect result issue when a statement contains embedded `LEFT OUTER JOIN` [#7689](https://github.com/pingcap/tidb/pull/7689)
    - Enhance the optimization rule of predicate pushdown on the `JOIN` statement [#7645](https://github.com/pingcap/tidb/pull/7645)
    - Fix the optimization rule of predicate pushdown for the `UnionScan` operator [#7695](https://github.com/pingcap/tidb/pull/7695)
    - Fix the issue that the unique key property of the `Union` operator is not correctly set [#7680](https://github.com/pingcap/tidb/pull/7680)
    - Enhance the optimization rule of constant folding [#7696](https://github.com/pingcap/tidb/pull/7696)
    - Optimize the data source in which the filter is null after propagation to table dual [#7756](https://github.com/pingcap/tidb/pull/7756)
+ SQL Execution Engine
    - Optimize the performance of read requests in a transaction [#7717](https://github.com/pingcap/tidb/pull/7717)
    - Optimize the cost of allocating Chunk memory in some executors [#7540](https://github.com/pingcap/tidb/pull/7540)
    - Fix the "index out of range" panic caused by the columns where point queries get all NULL values [#7790](https://github.com/pingcap/tidb/pull/7790)
+ Server
    - Fix the issue that the memory quota in the configuration file does not take effect [#7729](https://github.com/pingcap/tidb/pull/7729)
    - Add the `tidb_force_priority` system variable to set the execution priority for each statement [#7694](https://github.com/pingcap/tidb/pull/7694)
    - Support using the `admin show slow` statement to obtain the slow query log [#7785](https://github.com/pingcap/tidb/pull/7785)
+ Compatibility
    - Fix the issue that the result of `charset/collation` is incorrect in `information_schema.schemata` [#7751](https://github.com/pingcap/tidb/pull/7751)
    - Fix the issue that the value of the `hostname` system variable is empty [#7750](https://github.com/pingcap/tidb/pull/7750)
+ Expressions
    - Support the `init_vecter` argument in the `AES_ENCRYPT`/`AES_DECRYPT` built-in function [#7425](https://github.com/pingcap/tidb/pull/7425)
    - Fix the issue that the result of `Format` is incorrect in some expressions [#7770](https://github.com/pingcap/tidb/pull/7770)
    - Support the `JSON_LENGTH` built-in function [#7739](https://github.com/pingcap/tidb/pull/7739)
    - Fix the incorrect result issue when casting the unsigned integer type to the decimal type [#7792](https://github.com/pingcap/tidb/pull/7792)
+ DML
    - Fix the issue that the result of the `INSERT … ON DUPLICATE KEY UPDATE` statement is incorrect while updating the unique key [#7675](https://github.com/pingcap/tidb/pull/7675)
+ DDL
    - Fix the issue that the index value is not converted between time zones when you create a new index on a new column of the timestamp type [#7724](https://github.com/pingcap/tidb/pull/7724)
    - Support appending new values for the enum type [#7767](https://github.com/pingcap/tidb/pull/7767)
    - Support creating an etcd session quickly, which improves the cluster availability after network isolation [#7774](https://github.com/pingcap/tidb/pull/7774)

## PD

+ New feature
    - Add the API to get the Region list by size in reverse order [#1254](https://github.com/pingcap/pd/pull/1254)
+ Improvement
    - Return more detailed information in the Region API [#1252](https://github.com/pingcap/pd/pull/1252)
+ Bug fix
    - Fix the issue that `adjacent-region-scheduler` might lead to a crash after PD switches the leader [#1250](https://github.com/pingcap/pd/pull/1250)

## TiKV

+ Performance
    - Optimize the concurrency for coprocessor requests [#3515](https://github.com/tikv/tikv/pull/3515)
+ New features
    - Add the support for Log functions [#3603](https://github.com/tikv/tikv/pull/3603)
    - Add the support for the `sha1` function [#3612](https://github.com/tikv/tikv/pull/3612)
    - Add the support for the `truncate_int` function [#3532](https://github.com/tikv/tikv/pull/3532)
    - Add the support for the `year` function [#3622](https://github.com/tikv/tikv/pull/3622)
    - Add the support for the `truncate_real` function [#3633](https://github.com/tikv/tikv/pull/3633)
+ Bug fixes
    - Fix the reporting error behavior related to time functions [#3487](https://github.com/tikv/tikv/pull/3487), [#3615](https://github.com/tikv/tikv/pull/3615)
    - Fix the issue that the time parsed from string is inconsistent with that in TiDB [#3589](https://github.com/tikv/tikv/pull/3589)