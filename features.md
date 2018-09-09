---
title: TiDB Key Features
summary: Key features of the TiDB database platform
category: introduction
---

# TiDB Key Features

## Horizontal scalability

Horizontal scalability is the most important feature of TiDB. The scalability includes two aspects: the computing capability and the storage capacity. The TiDB server processes the SQL requests. As the business grows, the overall processing capability and higher throughput can be achieved by simply adding more TiDB server nodes. Data is stored in TiKV. As the size of the data grows, the scalability of data can be resolved by adding more TiKV server nodes. PD schedules data in Regions among the TiKV nodes and migrates part of the data to the newly added node. So in the early stage, you can deploy only a few service instances. For example, it is recommended to deploy at least 3 TiKV nodes, 3 PD nodes and 2 TiDB nodes. As business grows, more TiDB and TiKV instances can be added on-demand.

## High availability

High availability is another important feature of TiDB. All of the three components, TiDB, TiKV and PD, can tolerate the failure of some instances without impacting the availability of the entire cluster. For each component, See the following for more details about the availability, the consequence of a single instance failure and how to recover.

### TiDB

TiDB is stateless and it is recommended to deploy at least two instances. The front-end provides services to the outside through the load balancing components. If one of the instances is down, the Session on the instance will be impacted. From the application’s point of view, it is a single request failure but the service can be regained by reconnecting to the TiDB server. If a single instance is down, the service can be recovered by restarting the instance or by deploying a new one.

### PD

PD is a cluster and the data consistency is ensured using the Raft protocol. If an instance is down but the instance is not a Raft Leader, there is no impact on the service at all. If the instance is a Raft Leader, a new Leader will be elected to recover the service. During the election which is approximately 3 seconds, PD cannot provide service. It is recommended to deploy three instances. If one of the instances is down, the service can be recovered by restarting the instance or by deploying a new one.

### TiKV

TiKV is a cluster and the data consistency is ensured using the Raft protocol. The number of the replicas can be configurable and the default is 3 replicas. The load of TiKV servers are balanced through PD. If one of the node is down, all the Regions in the node will be impacted. If the failed node is the Leader of the Region, the service will be interrupted and a new election will be initiated. If the failed node is a Follower of the Region, the service will not be impacted. If a TiKV node is down for a period of time (default 30 minutes), PD will move the data to another TiKV node.
