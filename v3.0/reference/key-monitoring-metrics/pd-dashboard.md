---
title: Key Monitoring Metrics of PD
summary: Learn some key metrics displayed on the Grafana PD dashboard.
category: reference
aliases: ['/docs/op-guide/dashboard-pd-info/','/docs/dev/reference/key-monitoring-metrics/pd/']
---

# Key Monitoring Metrics of PD

If you use Ansible to deploy the TiDB cluster, the monitoring system is deployed at the same time. For more information, see [Overview of the Monitoring Framework](/v3.0/how-to/monitor/overview.md).

The Grafana dashboard is divided into a series of sub dashboards which include Overview, PD, TiDB, TiKV, Node\_exporter, Disk Performance, and so on. A lot of metrics are there to help you diagnose.

You can get an overview of the component PD status from the PD dashboard, where the key metrics are displayed. This document provides a detailed description of these key metrics.

## Key metrics description

To understand the key metrics displayed on the Overview dashboard, check the following table:

Service | Panel name | Description | Normal range
---------------- | ---------------- | ---------------------------------- | --------------
Cluster | PD role | It indicates whether the current PD is the leader or a follower. |
Cluster | Storage capacity | The total capacity size of the cluster |
Cluster | Current storage size | The current storage size of the cluster |
Cluster | Number of Regions | The total number of Regions without replicas |
Cluster | Leader balance ratio | The leader ratio difference of the instances with the biggest leader ratio and the smallest leader ratio | It is less than 5% for a balanced situation and becomes bigger when you restart an instance |
Cluster | Region balance ratio | The Region ratio difference of the instances with the biggest Region ratio and the smallest Region ratio | It is less than 5% for a balanced situation and becomes bigger when you add or remove an instance |
Cluster | Normal stores | The count of healthy stores |
Cluster | Abnormal stores | The count of unhealthy stores | The normal value is `0`. If the number is bigger than `0`, it means at least one instance is abnormal.
Cluster | Current storage usage | The current storage size and used ratio of the cluster |
Cluster | Current peer count | The current peer count of the cluster |
Cluster | Metadata information | It records the cluster ID, the last ID the allocator generated, and the last timestamp TSO generated. |
Cluster | Region label isolation level | The number of Regions in different label levels |
Cluster | Region health | It records the unusual Regions' count which may include pending peers, down peers, extra peers, offline peers, missing peers, learner peers or incorrect namespaces | The number of pending peers should be less than `100`. The missing peers should not be persistently greater than `0`.
Balance | Store capacity | The capacity size of each TiKV instance |
Balance | Store available | The available capacity size of each TiKV instance |
Balance | Store used | The used capacity size of each TiKV instance |
Balance | Size amplification | The size amplification, which is equal to Store Region size over Store used capacity size, of each TiKV instance |
Balance | Size available ratio | It is equal to Store available capacity size over Store capacity size for each TiKV instance |
Balance | Store leader score | The leader score of each TiKV instance |
Balance | Store Region score | The Region score of each TiKV instance |
Balance | Store leader size | The total leader size of each TiKV instance |
Balance | Store Region size | The total Region size of each TiKV instance |
Balance | Store leader count | The leader count of each TiKV instance |
Balance | Store Region count | The Region count of each TiKV instance |
HotRegion | Hot write Region's leader distribution | The total number of leader Regions under hot write on each TiKV instance |
HotRegion | Hot write Region's peer distribution | The total number of Regions which are not leader under hot write on each TiKV instance |
HotRegion | Hot write Region's leader written bytes | The total bytes of hot write on leader Regions for each TiKV instance |
HotRegion | Hot write Region's peer written bytes | The total bytes of hot write on Regions which are not leader for each TiKV instance |
HotRegion | Hot read Region's leader distribution | The total number of leader Regions under hot read on each TiKV instance |
HotRegion | Hot read Region's peer distribution | The total number of Regions which are not leader under hot read on each TiKV instance |
HotRegion | Hot read Region's leader read bytes | The total bytes of hot read on leader Regions for each TiKV instance |
HotRegion | Hot read Region's peer read bytes | The total bytes of hot read on Regions which are not leader for each TiKV instance |
Scheduler | Scheduler is running | The current running schedulers |
Scheduler | Balance leader movement | The leader movement details among TiKV instances |
Scheduler | Balance Region movement | The Region movement details among TiKV instances |
Scheduler | Balance leader event | The count of balance leader events |
Scheduler | Balance Region event | The count of balance Region events |
Scheduler | Balance leader scheduler | The inner status of balance leader scheduler |
Scheduler | Balance Region scheduler | The inner status of balance Region scheduler |
Scheduler | Namespace checker | The namespace checker's status |
Scheduler | Replica checker | The replica checker's status |
Scheduler | Region merge checker | The merge checker's status |
Operator | Schedule operator create | The number of different operators that are newly created |
Operator | Schedule operator check | The number of different operators that have been checked. It mainly checks if the current step is finished; if yes, it returns the next step to be executed. |
Operator | Schedule operator finish | The number of different operators that are finished |
Operator | Schedule operator timeout | The number of different operators that are timeout |
Operator | Schedule operator replaced or canceled | The number of different operators that are replaced or canceled |
Operator | Schedule operators count by state | The number of operators in different status |
Operator | 99% Operator finish duration | The time consumed when the operator is finished in `.99` |
Operator | 50% Operator finish duration | The time consumed when the operator is finished in `.50` |
Operator | 99% Operator step duration | The time consumed when the operator step is finished in `.99` |
Operator | 50% Operator step duration | The time consumed when the operator step is finished in `.50` |
gRPC | Completed commands rate | The rate of completing each kind of gRPC commands |
gRPC | 99% Completed commands duration | The time consumed of completing each kind of gRPC commands in `.99` |
etcd | Handle transactions count | The count of etcd transactions |
etcd | 99% Handle transactions duration | The time consumed of handling etcd transactions in `.99` |
etcd | 99% WAL fsync duration | The time consumed of writing WAL into the persistent storage in `.99` | The value is less than `1s`.
etcd | 99% Peer round trip time seconds | The latency of the network in `.99` | The value is less than `1s`.
etcd | etcd disk wal fsync rate | The rate of writing WAL into the persistent storage |
etcd | Raft term | The current term of Raft |
etcd | Raft committed index | The last committed index of Raft |
etcd | Raft applied index | The last applied index of Raft |
TiDB | Handle requests count | The count of TiDB requests |
TiDB | Handle requests duration | The time consumed of handling TiDB requests | It should be less than `100ms` in `.99`.
Heartbeat | Region heartbeat report | The count of the heartbeats which each TiKV instance reports to PD |
Heartbeat | Region heartbeat report error | The count of the heartbeats with the `error` status |
Heartbeat | Region heartbeat report active | The count of the heartbeats with the `ok` status |
Heartbeat | Region schedule push | The count of the corresponding schedule commands which PD sends to each TiKV instance |
Heartbeat | 99% Region heartbeat latency | The heartbeat latency of each TiKV instance in `.99` |

## PD dashboard interface

### Cluster

![PD Dashboard - Cluster metrics](/media/pd-dashboard-cluster.png)

### Balance

![PD Dashboard - Balance metrics](/media/pd-dashboard-balance.png)

### HotRegion

![PD Dashboard - HotRegion metrics](/media/pd-dashboard-hot-region.png)

### Scheduler

![PD Dashboard - Scheduler metrics](/media/pd-dashboard-scheduler.png)

### Operator

![PD Dashboard - Operator metrics](/media/pd-dashboard-operator.png)

### gRPC

![PD Dashboard - gRPC metrics](/media/pd-dashboard-grpc.png)

### etcd

![PD Dashboard - etcd metrics](/media/pd-dashboard-etcd.png)

### TiDB

![PD Dashboard - TiDB metrics](/media/pd-dashboard-tidb.png)

### Heartbeat

![PD Dashboard - Heartbeat metrics](/media/pd-dashboard-heartbeat.png)
