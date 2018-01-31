---
title: TiDB Roadmap
category: Roadmap
---

# TiDB Roadmap

This document defines the roadmap for TiDB development.

## TiDB：
- [ ] Optimizer
  - [ ] Refactor Ranger
  - [ ] Optimize the statistics info 
  - [ ] Optimize the cost model
- [ ] Executor
  - [ ] Parallel Operators
  - [ ] Compact Row Format to reduce memory usage
  - [ ] File Sort
- [ ] Support View
- [ ] Support Window Function
- [ ] Common Table Expression
- [ ] Table Partition
- [ ] Hash time index to resolve the issue with hot regions
- [ ] Reverse Index
- [ ] Cluster Index
- [ ] Improve DDL
- [ ] Support `utf8_general_ci` collation

## TiKV:

- [ ] Raft
  - [ ] Region merge
  - [ ] Local read thread
  - [ ] Multi-thread raftstore
  - [ ] None voter
  - [ ] Pre-vote
- [ ] RocksDB
  - [ ] DeleteRange
- [ ] Transaction
  - [ ] Optimize transaction conflicts
- [ ] Coprocessor
  - [ ] Streaming
- [ ] Tool
  - [ ] Import distributed data
  - [ ] Export distributed data
  - [ ] Disaster Recovery
- [ ] Flow control and degradation

## PD:
- [ ] Improve namespace 
  - [ ] Different replication policies for different namespaces and tables

  - [ ] Decentralize scheduling table regions
  - [ ] Scheduler supports prioritization to be more controllable 

- [ ] Use machine learning to optimize scheduling

## TiSpark:

- [ ] Limit / Order push-down
- [ ] Access through the DAG interface and deprecate the Select interface
- [ ] Index Join and parallel merge join
- [ ] Data Federation

## SRE & tools:

- [ ] Kubernetes based intergration for the on-premise version 
- [ ] Dashboard UI for the on-premise version
- [ ] The cluster backup and recovery tool
- [ ] The data migration tool (Wormhole V2)
- [ ] Security and system diagnosis
