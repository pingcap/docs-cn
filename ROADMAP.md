---
title: TiDB Roadmap
category: Roadmap
---

# TiDB Roadmap

This document defines the roadmap for TiDB development.

## TiDB:

- [ ] Optimizer
  - [x] Refactor Ranger
  - [ ] Optimize the cost model
  - [ ] Join Reorder
- [ ] Statistics
  - [x] Update statistics dynamically according to the query feedback
  - [x] Analyze table automatically
  - [ ] Improve the accuracy of Row Count estimation
- [ ] Executor
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
  - [ ] Pre-vote
- [x] RocksDB
  - [x] DeleteRange
- [x] Transaction
  - [x] Optimize transaction conflicts
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

## TiSpark:

- [ ] Limit / Order push-down
- [x] Access through the DAG interface and deprecate the Select interface
- [ ] Index Join and parallel merge join
- [ ] Data Federation

## SRE & tools:

- [ ] Kubernetes based intergration for the on-premise version 
- [ ] Dashboard UI for the on-premise version
- [ ] The cluster backup and recovery tool
- [ ] The data migration tool (Wormhole V2)
- [ ] Security and system diagnosis
