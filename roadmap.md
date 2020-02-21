---
title: TiDB v4.0 Roadmap
summary: Learn about the v4.0 roadmap of TiDB.
category: Roadmap
aliases: ['/docs/ROADMAP/','/docs/roadmap/']
---

<!-- markdownlint-disable MD001 -->

# TiDB v4.0 Roadmap

This document describes the roadmap for TiDB development.

## TiDB

### TiDB Server

#### Features

* Support TiFlash storage engine
* Support Optimizer Trace
* Support multi-column statistics
* Support TopN statistics for regular CM-Sketch
* Improve the Plan Cache feature
* Support self-adaptive SQL engine
* Support SQL Tuning Advisor
* Support SQL plan management
* Transaction
    + Pessimistic locking general availability (GA)
    + Support an unlimited number of statements in a transaction
    + Support 10 GB transactions

#### Performance

* Improve CSV/data loading performance
* Improve `Prepare` statement performance
* Support index for generated columns
* Optimize some operators of the SQL engine
    + Improve performance of queries by using indexes to return to the table
    + Split Index Join to Index Merge Join and Index Hash Join
    + Radix Hash Join
    + Index Merge
    + Parallel Stream Aggregate
    + Parallel Merge Sort
    + Parallel Merge Join
    + Full Vectorized Expression Evaluation
* Indexes on expressions
* Multi-index scan
* Support external storage for Join, Aggregate, and Sort operators
* Optimize the execution engine concurrency model
* Support new Cascades Optimizer and Cascades Planner to increase the Optimizer searching space

#### Usability

* Improve the Optimizer Hint feature
* Quickly restore database or table metadata and data
* Dynamically modify configuration items
* Automatically terminate idle connections
* Improve support for DDL statements in MySQL 5.7
* Refactor log content
* Support `admin checksum from … to …` to verify data integrity
* Support using standard SQL statements to query the DDL history
* Support using standard SQL statements to manage Binlog
* Support using standard SQL statements to manage the cluster
* Integrate multiple Ctrl tools into one tool

#### High Availability

* Support high service availability with TiDB Binlog
* Support high data reliability with TiDB Binlog

### TiKV Server

#### Features

* Support up to 200+ nodes in a cluster
* Fast full backup and restoration
* Dynamically split and merge hot spot Regions
* Fine-grained memory control
* Raft
    + Joint consensus
    + Read-only replicas

#### Performance

* Improve scan performance
* Dynamically increase the number of worker threads
* Flexibly increase read-only replicas
* Optimize the scheduling system to prevent QPS jitter

#### Usability

* Refactor log content

### TiFlash

#### Features

* Column-based storage
* Replicate data from TiKV by using Raft learner
* Snapshot read

### TiSpark

#### Features

* Support batch write
* Support accessing TiFlash

## Data Migration

### Features

* Improve forward checking
* Visualized management of replication rules
* Visualized management of replication tasks
* Online verification on data replication

### Usability

* Refactor log format and content

### High Availability

* Support high service availability
* Support high data reliability

## TiDB Toolkit

### Features

* Integrate Loader into TiDB
* Integrate TiDB Lightning into TiDB

### Performance

* Support parallel data importing by using multiple `lightning` and `importer` instances in TiDB Lightning

## TiDB Future Plan

### TiDB Server

#### Features

* Common table expression
* Invisible index
* Support modifying column types
* Support second-level partitions for partitioned tables
* Support conversion between partitioned tables and regular tables
* Support inserts and updates for Views
* Multi-schema change
* Configure the number of replicas and distribution strategy by tables
* Fine-grained QoS control
* Flash back to any point-in-time

#### Performance

* Coprocessor cache
* New row storage format
* Distributed execution engine

#### Usability

* Full link Trace tool
* Complete Help information

#### Security

* Column-level privileges

### TiKV Server

#### Features

* Fast incremental backup and restoration
* Flash back to any point-in-time
* Hierarchical storage
* Fine-grained QoS control
* Configure the number of replicas and distribution strategy by Regions
* Raft
    + Chain replication of data
    + Witness role
* Storage engine
    + Support splitting SSTables according to Guards During compaction in RocksDB
    + Separate cold and hot data

#### Performance

* Improve fast backup performance
* Improve fast restoration performance
* 1PC
* Support storage class memory hardware
* New Raft engine
