---
title: About TiDB
summary: Learn about what TiDB is, and the key features, architecture and roadmap of TiDB.
category: introduction
---

# About TiDB

## TiDB introduction

TiDB (The pronunciation is: /'taɪdiːbi:/ tai-D-B, etymology: titanium) is an open-source distributed scalable Hybrid Transactional and Analytical Processing (HTAP) database. It features infinite horizontal scalability, strong consistency, and high availability. TiDB is MySQL compatible and serves as a one-stop data warehouse for both OLTP (Online Transactional Processing) and OLAP (Online Analytical Processing) workloads.

- __Horizontal scalability__

    TiDB provides horizontal scalability simply by adding new nodes. Never worry about infrastructure capacity ever again.

- __MySQL compatibility__

    Easily replace MySQL with TiDB to power your applications without changing a single line of code in most cases and still benefit from the MySQL ecosystem.

- __Distributed transaction__

    TiDB is your source of truth, guaranteeing ACID compliance, so your data is accurate and reliable anytime, anywhere.

- __Cloud Native__

    TiDB is designed to work in the cloud -- public, private, or hybrid -- making deployment, provisioning, and maintenance drop-dead simple.

- __No more ETL__

    ETL (Extract, Transform and Load) is no longer necessary with TiDB's hybrid OLTP/OLAP architecture, enabling you to create new values for your users, easier and faster.

- __High availability__

    With TiDB, your data and applications are always on and continuously available, so your users are never disappointed.

TiDB is designed to support both OLTP and OLAP scenarios. For complex OLAP scenarios, use [TiSpark](tispark/tispark-user-guide.md).

Read the following three articles to understand TiDB techniques:

- [Data Storage](https://pingcap.github.io/blog/2017/07/11/tidbinternal1/)
- [Computing](https://pingcap.github.io/blog/2017/07/11/tidbinternal2/)
- [Scheduling](https://pingcap.github.io/blog/2017/07/20/tidbinternal3/)

## Roadmap

Read the [Roadmap](https://github.com/pingcap/docs/blob/master/ROADMAP.md).

## Connect with us

- **Twitter**: [@PingCAP](https://twitter.com/PingCAP)
- **Reddit**: https://www.reddit.com/r/TiDB/
- **Stack Overflow**: https://stackoverflow.com/questions/tagged/tidb
- **Mailing list**: [Google Group](https://groups.google.com/forum/#!forum/tidb-user)

## TiDB architecture

To better understand TiDB's features, you need to understand the TiDB architecture. The TiDB cluster includes three key components: the TiDB server, the PD server, and the TiKV server. In addition, TiDB also provides the [TiSpark](https://github.com/pingcap/tispark/) component for the complex OLAP requirements.

![image alt text](media/tidb-architecture.png)

### TiDB server

The TiDB server is in charge of the following operations:

1. Receiving the SQL requests

2. Processing the SQL related logics

3. Locating the TiKV address for storing and computing data through Placement Driver (PD)

4. Exchanging data with TiKV

5. Returning the result

The TiDB server is stateless. It does not store data and it is for computing only. TiDB is horizontally scalable and provides the unified interface to the outside through the load balancing components such as Linux Virtual Server (LVS), HAProxy, or F5.

### Placement Driver server

The Placement Driver (PD) server is the managing component of the entire cluster and is in charge of the following three operations:

1. Storing the metadata of the cluster such as the region location of a specific key.

2. Scheduling and load balancing regions in the TiKV cluster, including but not limited to data migration and Raft group leader transfer.

3. Allocating the transaction ID that is globally unique and monotonic increasing.

As a cluster, PD needs to be deployed to an odd number of nodes. Usually it is recommended to deploy to 3 online nodes at least.

### TiKV server

The TiKV server is responsible for storing data. From an external view, TiKV is a distributed transactional Key-Value storage engine. Region is the basic unit to store data. Each Region stores the data for a particular Key Range which is a left-closed and right-open interval from StartKey to EndKey. There are multiple Regions in each TiKV node. TiKV uses the Raft protocol for replication to ensure the data consistency and disaster recovery. The replicas of the same Region on different nodes compose a Raft Group. The load balancing of the data among different TiKV nodes are scheduled by PD. Region is also the basic unit for scheduling the load balance.

### TiSpark

TiSpark deals with the complex OLAP requirements. TiSpark makes Spark SQL directly run on the storage layer of the TiDB cluster, combines the advantages of the distributed TiKV cluster, and integrates into the big data ecosystem. With TiSpark, TiDB can support both OLTP and OLAP scenarios in one cluster, so the users never need to worry about data replication.

## Features

### Horizontal scalability

Horizontal scalability is the most important feature of TiDB. The scalability includes two aspects: the computing capability and the storage capacity. The TiDB server processes the SQL requests. As the business grows, the overall processing capability and higher throughput can be achieved by simply adding more TiDB server nodes. Data is stored in TiKV. As the size of the data grows, the scalability of data can be resolved by adding more TiKV server nodes. PD schedules data in Regions among the TiKV nodes and migrates part of the data to the newly added node. So in the early stage, you can deploy only a few service instances. For example, it is recommended to deploy at least 3 TiKV nodes, 3 PD nodes and 2 TiDB nodes. As business grows, more TiDB and TiKV instances can be added on-demand.

### High availability

High availability is another important feature of TiDB. All of the three components, TiDB, TiKV and PD, can tolerate the failure of some instances without impacting the availability of the entire cluster. For each component, See the following for more details about the availability, the consequence of a single instance failure and how to recover.

#### TiDB

TiDB is stateless and it is recommended to deploy at least two instances. The front-end provides services to the outside through the load balancing components. If one of the instances is down, the Session on the instance will be impacted. From the application’s point of view, it is a single request failure but the service can be regained by reconnecting to the TiDB server. If a single instance is down, the service can be recovered by restarting the instance or by deploying a new one.

#### PD

PD is a cluster and the data consistency is ensured using the Raft protocol. If an instance is down but the instance is not a Raft Leader, there is no impact on the service at all. If the instance is a Raft Leader, a new Leader will be elected to recover the service. During the election which is approximately 3 seconds, PD cannot provide service. It is recommended to deploy three instances. If one of the instances is down, the service can be recovered by restarting the instance or by deploying a new one.

#### TiKV

TiKV is a cluster and the data consistency is ensured using the Raft protocol. The number of the replicas can be configurable and the default is 3 replicas. The load of TiKV servers are balanced through PD. If one of the node is down, all the Regions in the node will be impacted. If the failed node is the Leader of the Region, the service will be interrupted and a new election will be initiated. If the failed node is a Follower of the Region, the service will not be impacted. If a TiKV node is down for a period of time (default 30 minutes), PD will move the data to another TiKV node.
