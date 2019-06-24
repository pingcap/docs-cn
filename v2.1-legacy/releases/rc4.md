---
title: TiDB RC4 Release Notes
category: releases
---

# TiDB RC4 Release Notes

On August 4, 2017, TiDB RC4 is released! This release is focused on MySQL compatibility, SQL optimization, stability, and performance.

## Highlight:

+ For performance, the write performance is improved significantly, and the computing task scheduling supports prioritizing to avoid the impact of OLAP on OLTP.
+ The optimizer is revised for a more accurate query cost estimating and for an automatic choice of the `Join` physical operator based on the cost.
+ Many enhancements have been introduced to be more compatible with MySQL.
+ TiSpark is now released to better support the OLAP business scenarios. You can now use Spark to access the data in TiKV.

## Detailed updates:

### TiDB:

+ The SQL query optimizer refactoring:
    - Better support for TopN queries
    - Support the automatic choice of the of the `Join` physical operator based on the cost
    - Improved Projection Elimination
+ The version check of schema is based on Table to avoid the impact of DDL on the ongoing transactions
+ Support ` BatchIndexJoin`
+ Improve the `Explain` statement
+ Improve the `Index Scan` performance
+ Many enhancements have been introduced to be more compatible with MySQL
+ Support the JSON type and operations
+ Support the configuration of query prioritizing and isolation level

### Placement Driver (PD):

+ Support using PD to set the TiKV location labels
+ Optimize the scheduler
    - PD is now supported to initialize the scheduling commands to TiKV.
    - Accelerate the response speed of the region heartbeat.
    - Optimize the `balance` algorithm
+ Optimize data loading to speed up failover

### TiKV:

+ Support the configuration of query prioritizing
+ Support the RC isolation level
+ Improve Jepsen test results and the stability
+ Support Document Store
+ Coprocessor now supports more pushdown functions
+ Improve the performance and stability

### TiSpark Beta Release:

+ Implement the prediction pushdown
+ Implement the aggregation pushdown
+ Implement range pruning
+ Capable of running full set of TPC-H except one query that needs view support
