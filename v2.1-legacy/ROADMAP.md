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
    - [x] Optimize the cost model
    - [ ] Cascades model planner
    - [ ] Join Reorder
+ [ ] Statistics
    - [x] Update statistics dynamically according to the query feedback
    - [x] Analyze table automatically
    - [x] Improve the accuracy of Row Count estimation
+ [ ] Execution Engine
    - [ ] Push down the Projection operator to the Coprocessor
    - [x] Improve the performance of the HashJoin operator
    + [ ] Parallel Operators
        - [x] Projection
        - [x] Aggregation
        - [ ] Sort
    - [x] Compact Row Format to reduce memory usage
    - [ ] File Sort
- [ ] View
- [ ] Window Function
- [ ] Common Table Expression
+ [ ] Table Partition
    - [x] Range Partition
    - [ ] Hash Partition
- [ ] Cluster Index
- [ ] New storage row format
- [ ] Query Tracing
+ [ ] Improve DDL
    - [x] Speed up Add Index operation
    - [x] Parallel DDL
    - [ ] Support locking table
    - [ ] Support modifying the column type
    - [ ] Support modifying the primary key
    - [ ] Support multiple DDL operations in a single statement
- [ ] Support `utf8_general_ci` collation

## TiKV:

+ Raft
    - [x] Region Merge - Merge small Regions together to reduce overhead
    - [x] Local Read Thread - Process read requests in a local read thread
    - [x] Split Region in Batch - Speed up Region split for large Regions
    - [x] Raft Learner - Support Raft learner to smooth the configuration change process
    - [x] Raft Pre-vote - Support Raft pre-vote to avoid unnecessary leader election on network isolation
    - [ ] Joint Consensus - Change multi members safely.
    - [ ] Multi-thread Raftstore - Process Region Raft logic in multiple threads
    - [ ] Multi-thread apply pool - Apply Region Raft committed entries in multiple threads
+ Engine
    - [ ] Titan - Separate large key-values from LSM-Tree
    - [ ] Pluggable Engine Interface - Clean up the engine wrapper code and provide more extensibility
+ Storage
    - [ ] Flow Control - Do flow control in scheduler to avoid write stall in advance
+ Transaction
    - [x] Optimize transaction conflicts
    - [ ] Distributed GC - Distribute MVCC garbage collection control to TiKV
+ Coprocessor
    - [x] Streaming - Cut large data set into small chunks to optimize memory consumption
    - [ ] Chunk Execution - Process data in chunk to improve performance
    - [ ] Request Tracing - Provide per-request execution details
+ Tools
    - [x] TiKV Importer - Speed up data importing by SST file ingestion
+ Client
    - [ ] TiKV client (Rust crate)
    - [ ] Batch gRPC Message - Reduce message overhead

## PD:

- [x] Improve namespace
    - [x] Different replication policies for different namespaces and tables
- [x] Decentralize scheduling table Regions
- [x] Scheduler supports prioritization to be more controllable
- [ ] Use machine learning to optimize scheduling
- [ ] Optimize Region metadata - Save Region metadata in detached storage engine

## TiSpark:

- [ ] Limit/Order push-down
- [x] Access through the DAG interface and deprecate the Select interface
- [ ] Index Join and parallel merge join
- [ ] Data Federation

## Tools:

- [X] Tool for automating TiDB deployment
- [X] High-Performance data import tool (lightning)
- [X] Backup and restore tool (incremental backup supported by drainer, incremental restore supported by reparo)
- [X] New TiDB-binlog with improved architecture
- [ ] Data online migration tool (premium edition of Syncer)
- [ ] Diagnostic tools
