# TiDB Documentation

## Documentation List

+ [About TiDB](overview.md)
  - [TiDB Introduction](overview.md#tidb-introduction)
  - [TiDB Architecture](overview.md#tidb-architecture)
- [TiDB Quick Start Guide](./QUICKSTART.md)
+ [TiDB Operations Guide](op-guide/op-guide.md)
  - [Hardware and Software Requirements](op-guide/op-guide.md#hardware-and-software-requirements)
  - [Deploy](op-guide/op-guide.md#deploy)
  - [Configure](op-guide/op-guide.md#configure)
  - [Monitor](op-guide/op-guide.md#monitor)
  - [Scale](op-guide/op-guide.md#scale)
  - [Upgrade](op-guide/op-guide.md#upgrade)
  - [Performance Tuning](op-guide/op-guide.md#performance-tuning)
  - [Backup and Migrate](op-guide/op-guide.md#backup-and-migrate)
  - [Deploy TiDB Using the Binary](op-guide/op-guide.md#deploy-tidb-using-the-binary)
+ [TiDB User Guide](sql/user-manual.md)
  - [TiDB Server Administration](sql/user-manual.md#tidb-server-administration)
  - [SQL Optimization](sql/user-manual.md#sql-optimization)
  - [Language Structure](sql/user-manual.md#language-structure)
  - [Globalization](sql/user-manual.md#globalization)
  - [Data Types](sql/user-manual.md#data-types)
  - [Functions and Operators](sql/user-manual.md#functions-and-operators)
  - [SQL Statement Syntax](sql/user-manual.md#sql-statement-syntax)
  - [JSON Functions and Generated Column](sql/user-manual.md#json-functions-and-generated-column)
  - [Connectors and APIs](sql/user-manual.md#connectors-and-apis)
  - [Compatibility with MySQL](sql/mysql-compatibility.md)
+ Advanced Usage
  - [Read Data From History Versions](op-guide/history-read.md) 
+ Tools
  - [Syncer User Guide](tools/syncer.md)
  - [Loader User Guide](tools/loader.md)
  - [TiDB-Binlog User Guide](tools/tidb-binlog.md)
  - [PD Control User Guide](tools/pd-control.md)
+ The TiDB Connector for Spark
  - [Quick Start Guide](tispark/tispark-quick-start-guide.md)
  - [User Guide](tispark/tispark-user-guide.md)
- [Frequently Asked Questions (FAQ)](./FAQ.md)
- [Troubleshoot](./trouble-shooting.md)
- [TiDB Best Practices](https://pingcap.github.io/blog/2017/07/24/tidbbestpractice/)
- [Releases](release/rn.md)
+ More Resources
  - [Frequently Used Tools](https://github.com/pingcap/tidb-tools)
  - [PingCAP Blog](https://pingcap.github.io/blog/)
  - [Weekly Update](http://weekly.pingcap.com/)

## What is TiDB?

TiDB (The pronunciation is: /'taɪdiːbi:/ tai-D-B, etymology: titanium) is a Hybrid Transactional/Analytical Processing (HTAP) database. Inspired by the design of Google F1 and Google Spanner, TiDB features infinite horizontal scalability, strong consistency, and high availability. The goal of TiDB is to serve as a one-stop solution for online transactions and analyses.

- __Horizontal scalability__

Grow TiDB as your business grows. You can increase the capacity for storage and computation simply by adding more machines.

- __Compatible with MySQL protocol__

Use TiDB as MySQL. You can replace MySQL with TiDB to power your application without changing a single line of code in most cases.

- __Automatic Failover and high availability__

Your data and applications are always-on. TiDB automatically handles malfunctions and protects your applications from machine failures or even downtime of an entire data-center.

- __Consistent distributed transactions__

Think of TiDB as a single-machine RDBMS. You can start a transaction that crosses multiple machines without worrying about consistency. TiDB makes your application code simple and robust.

- __Online DDL__

Evolve TiDB schemas as your requirement changes. You can add new columns and indexes without stopping or affecting the on-going operations.

- __Multiple storage engine support__

Power TiDB with your most favorite engines. TiDB supports local storage engines such as GolevelDB and BoltDB, as well as [TiKV](https://github.com/pingcap/tikv), a distributed storage engine.


## Roadmap

Read the [Roadmap](https://github.com/pingcap/docs/blob/master/ROADMAP.md).

## TiDB Architecture

To better understand TiDB’s features, you need to understand the TiDB architecture.

![TiDB Architecture](media/tidb-architecture.png)

The TiDB cluster has three components: the TiDB Server, the PD Server,  and the TiKV server.

### TiDB Server

The TiDB server is in charge of the following operations:

1. Receiving the SQL requests

2. Processing the SQL related logics

3. Locating the TiKV address for storing and computing data through the Placement Driver (PD)

4. Exchanging data with TiKV

5. Returning the result

The TiDB server is stateless. It doesn’t store data and it is for computing only. TiDB is horizontally scalable and provides the unified interface to the outside through the load balancing components such as Linux Virtual Server (LVS), HAProxy, or F5.

### Placement Driver Server

Placement Driver (PD) is the managing component of the entire cluster and is in charge of the following three operations:

1. Storing the metadata of the cluster such as the region location of a specific key.

2. Scheduling and load balancing regions in the TiKV cluster, including but not limited to data migration and Raft group leader transfer.

3. Allocating the transaction ID that is globally unique and monotonic increasing.

As a cluster, PD needs to be deployed to an odd number of nodes. Usually it is recommended to deploy to 3 online nodes at least.

### TiKV Server

TiKV server is responsible for storing data. From an external view, TiKV is a distributed transactional Key-Value storage engine. Region is the basic unit to store data. Each Region stores the data for a particular Key Range which is a left-closed and right-open interval from StartKey to EndKey. There are multiple Regions in each TiKV node. TiKV uses the Raft protocol for replication to ensure the data consistency and disaster recovery. The replicas of the same Region on different nodes compose a Raft Group. The load balancing of the data among different TiKV nodes are scheduled by PD. Region is also the basic unit for scheduling the load balance.

## Horizontal Scalability

Horizontal scalability is the most important feature of TiDB. The scalability includes two aspects: the computing capability and the storage capacity. The TiDB server processes the SQL requests. As the business grows, the overall processing capability and higher throughput can be achieved by simply adding more TiDB server nodes. Data is stored in TiKV. As the size of the data grows, the scalability of data can be resolved by adding more TiKV server nodes. PD schedules data in Regions among the TiKV nodes and migrates part of the data to the newly added node. So in the early stage, you can deploy only a few service instances. For example, it is recommended to deploy at least 3 TiKV nodes, 3 PD nodes and 2 TiDB nodes. As business grows, more TiDB and TiKV instances can be added on-demand.

## High availability

High availability is another important feature of TiDB. All of the three components, TiDB, TiKV and PD, can tolerate the failure of some instances without impacting the availability of the entire cluster. For each component, See the following for more details about the availability, the consequence of a single instance failure and how to recover.

### TiDB

TiDB is stateless and it is recommended to deploy at least two instances. The front-end provides services to the outside through the load balancing components. If one of the instances is down, the Session on the instance will be impacted. From the application’s point of view, it is a single request failure but the service can be regained by reconnecting to the TiDB server. If a single instance is down, the service can be recovered by restarting the instance or by deploying a new one.

### PD

PD is a cluster and the data consistency is ensured using the Raft protocol. If an instance is down but the instance is not a Raft Leader, there is no impact on the service at all. If the instance is a Raft Leader, a new Leader will be elected to recover the service. During the election which is approximately 3 seconds, PD cannot provide service. It is recommended to deploy three instances. If one of the instances is down, the service can be recovered by restarting the instance or by deploying a new one.

### TiKV

TiKV is a cluster and the data consistency is ensured using the Raft protocol. The number of the replicas can be configurable and the default is 3 replicas. The load of TiKV servers are balanced through PD. If one of the node is down, all the Regions in the node will be impacted. If the failed node is the Leader of the Region, the service will be interrupted and a new election will be initiated. If the failed node is a Follower of the Region, the service will not be impacted. If a TiKV node is down for a period of time (the default value is 10 minutes), PD will move the data to another TiKV node.
