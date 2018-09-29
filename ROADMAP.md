---
title: TiDB Roadmap
summary: Learn about the roadmap of TiDB.
category: Roadmap
---

# TiDB Roadmap

This document defines the roadmap for TiDB development.

## TiDB:

+ [ ] Optimizer
    - [x] Refactor Ranger
    - [ ] Optimize the cost model
    - [ ] Join Reorder
+ [ ] Statistics
    - [x] Update statistics dynamically according to the query feedback
    - [x] Analyze table automatically
    - [ ] Improve the accuracy of Row Count estimation
+ [ ] Executor
    - [ ] Push down the Projection operator to the Coprocessor
    - [ ] Improve the performance of the HashJoin operator
    - [ ] Parallel Operators
        - [x] Projection
        - [ ] Aggregation
        - [ ] Sort
    - [x] Compact Row Format to reduce memory usage
    - [ ] File Sort
- [ ] View
- [ ] Window Function
- [ ] Common Table Expression
- [ ] Table Partition
- [ ] Cluster Index
- [ ] Improve DDL
  - [x] Speed up Add Index operation
  - [ ] Parallel DDL
- [ ] Support `utf8_general_ci` collation

## TiKV:

- [ ] Raft
    - [x] Region merge
    - [ ] Local read thread
    - [ ] Multi-thread raftstore
    - [x] None voter
    - [x] Pre-vote
    - [ ] Multi-thread apply pool
    - [ ] Split region in batch
    - [ ] Raft Engine
- [x] RocksDB 
    - [x] DeleteRange
    - [ ] BlobDB 
- [x] Transaction
    - [x] Optimize transaction conflicts
    - [ ] Distributed GC
- [x] Coprocessor
    - [x] Streaming
- [ ] Tool
    - [x] Import distributed data
    - [ ] Export distributed data
    - [ ] Disaster Recovery
- [ ] Flow control and degradation

## PD:

- [x] Improve namespace
    - [x] Different replication policies for different namespaces and tables
- [x] Decentralize scheduling table Regions
- [x] Scheduler supports prioritization to be more controllable
- [ ] Use machine learning to optimize scheduling
- [ ] Cluster Simulator

## TiSpark:

- [ ] Limit/Order push-down
- [x] Access through the DAG interface and deprecate the Select interface
- [ ] Index Join and parallel merge join
- [ ] Data Federation

## Tools:

- [X] Tool for automating TiDB deployment
- [X] High-Performance data import tool
- [X] Backup and restore tool (incremental backup supported)
- [ ] Data online migration tool (premium edition of Syncer)
- [ ] Diagnostic tools
