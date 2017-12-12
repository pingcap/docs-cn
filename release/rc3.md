---
title: TiDB RC3 Release Notes
category: releases
---

# TiDB RC3 Release Notes

On June 20, 2017, TiDB RC4 is released!This release is focused on MySQL compatibility, SQL optimization, stability, and performance.

## Highlight:

- The privilege management is refined to enable users to manage the data access privileges using the same way as in MySQL.
- DDL is accelerated. 
- The load balancing policy and process are optimized for performance.
- TiDB-Ansible is open sourced. By using TiDB-Ansilbe, you can deploy, upgrade, start and shutdown a TiDB cluster with one click.

## Detailed updates:

## TiDB:

+ The following features are added or improved in the SQL query optimizer:
    - Support incremental statistics
    - Support the ` Merge Sort Join ` operator
    - Support the ` Index Lookup Join` operator
    - Support the ` Optimizer Hint` Syntax
    - Optimize the memory consumption of the `Scan`, `Join`, `Aggregation` operators
    - Optimize the Cost Based Optimizer (CBO) framework
    - Refactor `Expression`
+ Support more complete privilege management
+ DDL acceleration
+ Support using HTTP API to get the data distribution information of tables
+ Support using system variables to control the query concurrency 
+ Add more MySQL built-in functions
+ Support using system variables to automatically split a big transaction into smaller ones to commit

## Placement Driver (PD):

+ Support gRPC
+ Provide the Disaster Recovery Toolkit
+ Use Garbage Collection to clear stale data automatically
+ Support more efficient data balance
+ Support hot Region scheduling to enable load balancing and speed up the data importing
+ Performance
    - Accelerate getting Client TSO
    - Improve the efficiency of Region Heartbeat processing
+ Improve the `pd-ctl` function
    - Update the Replica configuration dynamically 
    - Get the Timestamp Oracle (TSO)
    - Use ID to get the Region information
 
## TiKV:

+ Support gRPC
+ Support the Sorted String Table (SST) format snapshot to improve the load balancing speed of a cluster
+ Support using the Heap Profile to uncover memory leaks
+ Support Streaming SIMD Extensions (SSE) and speed up the CRC32 calculation
+ Accelerate transferring leader for faster load balancing
+ Use Batch Apply to reduce CPU usage and improve the write performance
+ Support parallel Prewrite to improve the transaction write speed
+ Optimize the scheduling of the coprocessor thread pool to reduce the impact of big queries on point get
+ The new Loader supports data importing at the table level, as well as splitting a big table into smaller logical blocks to import concurrently to improve the data importing speed.
