---
title: Pre-GA release notes
category: releases
---

# Pre-GA Release Notes

On August 30, 2017, TiDB Pre-GA is released! This release is focused on MySQL compatibility, SQL optimization, stability, and performance.

## TiDB:

+ The SQL query optimizer:
    - Adjust the cost model
    - Use index scan to handle the `where` clause with the `compare` expression which has different types on each side
    - Support the Greedy algorithm based Join Reorder
+ Many enhancements have been introduced to be more compatible with MySQL
+ Support `Natural Join`
+ Support the JSON type (Experimental), including the query, update and index of the JSON fields
+ Prune the useless data to reduce the consumption of the executor memory 
+ Support configuring prioritization in the SQL statements and automatically set the prioritization for some of the statements according to the query type
+ Completed the expression refactor and the speed is increased by about 30%

## Placement Driver (PD):

+ Support manually changing the leader of the PD cluster

## TiKV:

+ Use dedicated Rocksdb instance to store Raft log
+ Use `DeleteRange` to speed up the deleting of replicas
+ Coprocessor now supports more pushdown operators
+ Improve the performance and stability

## TiDB Connector for Spark Beta Release:

+ Implement the predicates pushdown
+ Implement the aggregation pushdown
+ Implement range pruning
+ Capable of running full set of TPC+H except for one query that needs view support