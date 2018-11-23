---
title: TiDB RC1 Release Notes
category: releases
---

# TiDB RC1 Release Notes

On December 23, 2016, TiDB RC1 is released. See the following updates in this release:

## TiKV:
+ The write speed has been improved.
+ The disk space usage is reduced.
+ Hundreds of TBs of data can be supported.
+ The stability is improved and TiKV can support a cluster with 200 nodes.
+ Supports the Raw KV API and the Golang client.

Placement Driver (PD):
+ The scheduling strategy framework is optimized and now the strategy is more flexible and reasonable.
+ The support for `label` is added to support Cross Data Center scheduling.
+ PD Controller is provided to operate the PD cluster more easily.

## TiDB:
+ The following features are added or improved in the SQL query optimizer:
    - Eager aggregation
    - More detailed `EXPLAIN` information
    - Parallelization of the `UNION` operator
    - Optimization of the subquery performance
    - Optimization of the conditional push-down
    - Optimization of the Cost Based Optimizer (CBO) framework
+ The implementation of the time related data types are refactored to improve the compatibility with MySQL.
+  More built-in functions in MySQL are supported.
+  The speed of the `add index` statement is enhanced.
+  The following statements are supported:
    -  Use the `CHANGE COLUMN` statement to change the name of a column.
    -  Use `MODIFY COLUMN` and `CHANGE COLUMN` of the `ALTER TABLE` statement for some of the column type transfer.

## New tools:
+ `Loader` is added to be compatible with the `mydumper` data format in Percona and provides the following functions:
    - Multi-thread import
    - Retry if error occurs
    - Breakpoint resume
    - Targeted optimization for TiDB
+ The tool for one-click deployment is added.
