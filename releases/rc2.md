---
title: TiDB RC2 Release Notes
category: releases
---

# TiDB RC2 Release Notes

On August 4, 2017, TiDB RC4 is released! This release is focused on the compatibility with MySQL, SQL query optimizer, system stability and performance in this version. What’s more, a new permission management mechanism is added and users can control data access in the same way as the MySQL privilege management system.

## TiDB

+ Query optimizer
    - Collect column/index statistics and use them in the query optimizer
    - Optimize the correlated subquery
    - Optimize the Cost Based Optimizer (CBO) framework
    - Eliminate aggregation using unique key information
    - Refactor expression evaluation framework
    - Convert Distinct to GroupBy
    - Support the topn operation push-down
+ Support basic privilege management
+ Add lots of MySQL built-in functions
+ Improve the Alter Table statement and support the modification of table name, default value and comment
+ Support the Create Table Like statement
+ Support the Show Warnings statement
+ Support the Rename Table statement
+ Restrict the size of a single transaction to avoid the cluster blocking of large transactions
+ Automatically split data in the process of Load Data
+ Optimize the performance of the AddIndex and Delete statement
+ Support "ANSI_QUOTES" sql_mode
+ Improve the monitoring system
+ Fix Bugs
+ Solve the problem of memory leak

## PD

+ Support location aware replica scheduling
+ Conduct fast scheduling based on the number of region
+ pd-ctl support more features
    - Add or delete PD
    - Obtain Region information with Key
    - Add or delete scheduler and operator
    - Obtain cluster label information

## TiKV

+ Support Async Apply to improve the entire write performance
+ Use prefix seek to improve the read performance of Write CF
+ Use memory hint prefix to improve the insert performance of Raft CF
+ Optimize the single read transaction performance
+ Support more push-down expressions
+ Improve the monitoring system
+ Fix Bugs
