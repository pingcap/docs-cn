---
title: TiDB Roadmap
summary: Learn about the roadmap of TiDB.
category: Roadmap
---

# TiDB Roadmap

This document defines the roadmap for TiDB development.

## TiDB:

+ [ ] Optimizer
    - [ ] Statistics Optimization
    - [ ] Multi-Column Statistics
    - [ ] Cascades Planner
    - [ ] Plan Management
    - [ ] SQL Tuning Advisor
    - [ ] Robust Access Path Selection: add the heuristic rule and improve the accuracy of index selection in OLTP scenarios
    - [ ] Adaptive Query Optimization
+ [ ] Execution Engine
    - [ ] Parallel Operators
    - [ ] Memory Control
    - [ ] Concurrency Control
    - [ ] Shuffle Operators
    - [ ] Vectorized Expression Evaluation
    - [ ] UDF
+ [ ] SQL Features
    - [ ] Support Views
    - [ ] Support Window Functions
    - [ ] Support Common Table Expressions
    - [ ] Support Hash Partitioned Tables
    - [ ] Support the utf8mb4_0900_ai_ci Collation
+ [ ] Improve DDL
    - [ ] Support Table Lock
    - [ ] Support Change Column Type
    - [ ] Support Multiple DDL Operations in a Single Statement
    - [ ] Support Invisible Indexes
+ [ ] Support Plugin System
    - [ ] Support White List Plugin
    - [ ] Support Audit Log Plugin
    - [ ] Support RBAC Plugin
    - [ ] Support Diagnostic Plugin
+ [ ] Support Query Tracing
+ [ ] Support Hybrid Column/Row-oriented Storage Engine
+ [ ] Support New Storage Row Format: improve performance and reduce memory usage
+ [ ] Support Non-integer Type of RowID
+ [ ] Transaction
    - [ ] Reduce Read-write Conflicts
    - [ ] Optimize Transaction Scheduling Mechanism
    - [ ] Refine Model and Reduce Latency
    - [ ] Support Minimal Transaction (like the mini-transaction of InnoDB)

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
