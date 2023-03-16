---
title: Multiple Availability Zones in One Region Deployment
summary: Learn the deployment solution to multiple availability zones in one region.
aliases: ['/docs/dev/how-to/deploy/geographic-redundancy/overview/','/docs/dev/geo-redundancy-deployment/','/tidb/dev/geo-redundancy-deployment']
---

# Multiple Availability Zones in One Region Deployment

<!-- Localization note for TiDB:

- English: use distributed SQL, and start to emphasize HTAP
- Chinese: can keep "NewSQL" and emphasize one-stop real-time HTAP ("一栈式实时 HTAP")
- Japanese: use NewSQL because it is well-recognized

-->

As a distributed SQL database, TiDB combines the best features of the traditional relational database and the scalability of the NoSQL database, and is highly available across availability zones (AZs). This document introduces the deployment of multiple AZs in one region.

The term "region" in this document refers to a geographic area, while the capitalized "Region" refers to a basic unit of data storage in TiKV. "AZ" refers to an isolated location within a region, and each region has multiple AZs. The solution described in this document also applies to the scenario where multiple data centers are located in a single city.

## Raft protocol

Raft is a distributed consensus algorithm. Using this algorithm, both PD and TiKV, among components of the TiDB cluster, achieve disaster recovery of data, which is implemented through the following mechanisms:

- The essential role of Raft members is to perform log replication and act as a state machine. Among Raft members, data replication is implemented by replicating logs. Raft members change their own states in different conditions to elect a leader to provide services.
- Raft is a voting system that follows the majority protocol. In a Raft group, if a member gets the majority of votes, its membership changes to leader. In other words, when the majority of nodes remain in the Raft group, a leader can be elected to provide services.

To take advantage of Raft's reliability, the following conditions must be met in a real deployment scenario:

- Use at least three servers in case one server fails.
- Use at least three racks in case one rack fails.
- Use at least three AZs in case one AZ fails.
- Deploy TiDB in at least three regions in case data safety issue occurs in one region.

The native Raft protocol does not have good support for an even number of replicas. Considering the impact of cross-region network latency, three AZs in the same region might be the most suitable solution to a highly available and disaster tolerant Raft deployment.

## Three AZs in one region deployment

TiDB clusters can be deployed in three AZs in the same region. In this solution, data replication across the three AZs is implemented using the Raft protocol within the cluster. These three AZs can provide read and write services at the same time. Data consistency is not affected even if one AZ fails.

### Simple architecture

TiDB, TiKV, and PD are distributed among three AZs, which is the most common deployment with the highest availability.

![3-AZ Deployment Architecture](/media/deploy-3dc.png)

**Advantages:**

- All replicas are distributed among three AZs, with high availability and disaster recovery capability.
- No data will be lost if one AZ is down (RPO = 0).
- Even if one AZ is down, the other two AZs will automatically start leader election and automatically resume services within a certain period (within 20 seconds in most cases). See the following diagram for more information:

![Disaster Recovery for 3-AZ Deployment](/media/deploy-3dc-dr.png)

**Disadvantages:**

The performance can be affected by the network latency.

- For writes, all the data has to be replicated to at least two AZs. Because TiDB uses a two-phase commit for writes, the write latency is at least twice the latency of the network between two AZs.
- The read performance will also be affected by the network latency if the leader is not in the same AZ with the TiDB node that sends the read request.
- Each TiDB transaction needs to obtain TimeStamp Oracle (TSO) from the PD leader. So if the TiDB and PD leaders are not in the same AZ, the performance of the transactions will also be affected by the network latency because each transaction with the write request has to obtain TSO twice.

### Optimized architecture

If not all of the three AZs need to provide services to the applications, you can dispatch all the requests to one AZ and configure the scheduling policy to migrate the TiKV Region leader and PD leader to the same AZ. In this way, neither obtaining TSO nor reading TiKV Regions will be impacted by the network latency across AZs. If this AZ is down, the PD leader and TiKV Region leader will be automatically elected in other surviving AZs, and you just need to switch the requests to the AZs that are still alive.

![Read Performance Optimized 3-AZ Deployment](/media/deploy-3dc-optimize.png)

**Advantages:**

The cluster's read performance and the capability to get TSO are improved. A configuration template of scheduling policy is as follows:

```shell
-- Evicts all leaders of other AZs to the AZ that provides services to the application.
config set label-property reject-leader LabelName labelValue

-- Migrates PD leaders and sets priority.
member leader transfer pdName1
member leader_priority pdName1 5
member leader_priority pdName2 4
member leader_priority pdName3 3
```

> **Note:**
>
> Starting from TiDB v5.2, the `label-property` configuration is not supported by default. To set the replica policy, use the [placement rules](/configure-placement-rules.md).

**Disadvantages:**

- Write scenarios are still affected by network latency across AZs. This is because Raft follows the majority protocol and all written data must be replicated to at least two AZs.
- The TiDB server that provides services is only in one AZ.
- All application traffic is processed by one AZ and the performance is limited by the network bandwidth pressure of that AZ.
- The capability to get TSO and the read performance are affected by whether the PD server and TiKV server are up in the AZ that processes application traffic. If these servers are down, the application is still affected by the cross-center network latency.

### Deployment example

This section provides a topology example, and introduces TiKV labels and TiKV labels planning.

#### Topology example

The following example assumes that three AZs (AZ1, AZ2, and AZ3) are located in one region; each AZ has two sets of racks and each rack has three servers. The example ignores the hybrid deployment or the scenario where multiple instances are deployed on one machine. The deployment of a TiDB cluster (three replicas) on three AZs in one region is as follows:

![3-AZ in One Region](/media/multi-data-centers-in-one-city-deployment-sample.png)

#### TiKV labels

TiKV is a Multi-Raft system where data is divided into Regions and the size of each Region is 96 MB by default. Three replicas of each Region form a Raft group. For a TiDB cluster of three replicas, because the number of Region replicas is independent of the TiKV instance numbers, three replicas of a Region are only scheduled to three TiKV instances. This means that even if the cluster is scaled out to have N TiKV instances, it is still a cluster of three replicas.

Because a Raft group of three replicas tolerates only one replica failure, even if the cluster is scaled out to have N TiKV instances, this cluster still tolerates only one replica failure. Two failed TiKV instances might cause some Regions to lose replicas and the data in this cluster is no longer complete. SQL requests that access data from these Regions will fail. The probability of two simultaneous failures among N TiKV instances is much higher than the probability of two simultaneous failures among three TiKV instances. This means that the more TiKV instances the Multi-Raft system is scaled out to have, the less the availability of the system.

Because of the preceding limitation, `label` is used to describe the location information of TiKV. The label information is refreshed to the TiKV startup configuration file with deployment or rolling upgrade operations. The started TiKV reports its latest label information to PD. Based on the user-registered label name (the label metadata) and the TiKV topology, PD optimally schedules Region replicas and improves the system availability.

#### TiKV labels planning example

To improve the availability and disaster recovery of the system, you need to design and plan TiKV labels according to your existing physical resources and the disaster recovery capability. You also need to edit the cluster initialization configuration file according to the planned topology:

```ini
server_configs:
  pd:
    replication.location-labels: ["zone","az","rack","host"]

tikv_servers:
  - host: 10.63.10.30
    config:
      server.labels: { zone: "z1", az: "az1", rack: "r1", host: "30" }
  - host: 10.63.10.31
    config:
      server.labels: { zone: "z1", az: "az1", rack: "r1", host: "31" }
  - host: 10.63.10.32
    config:
      server.labels: { zone: "z1", az: "az1", rack: "r2", host: "32" }
  - host: 10.63.10.33
    config:
      server.labels: { zone: "z1", az: "az1", rack: "r2", host: "33" }

  - host: 10.63.10.34
    config:
      server.labels: { zone: "z2", az: "az2", rack: "r1", host: "34" }
  - host: 10.63.10.35
    config:
      server.labels: { zone: "z2", az: "az2", rack: "r1", host: "35" }
  - host: 10.63.10.36
    config:
      server.labels: { zone: "z2", az: "az2", rack: "r2", host: "36" }
  - host: 10.63.10.37
    config:
      server.labels: { zone: "z2", az: "az2", rack: "r2", host: "37" }

  - host: 10.63.10.38
    config:
      server.labels: { zone: "z3", az: "az3", rack: "r1", host: "38" }
  - host: 10.63.10.39
    config:
      server.labels: { zone: "z3", az: "az3", rack: "r1", host: "39" }
  - host: 10.63.10.40
    config:
      server.labels: { zone: "z3", az: "az3", rack: "r2", host: "40" }
  - host: 10.63.10.41
    config:
      server.labels: { zone: "z3", az: "az3", rack: "r2", host: "41" }
```

In the preceding example, `zone` is the logical availability zone layer that controls the isolation of replicas (three replicas in the example cluster).

Considering that the AZs might be scaled out in the future, the three-layer label structure (`az`, `rack`, and `host`) is not directly adopted. Assuming that `AZ2`, `AZ3`, and `AZ4` are to be scaled out, you only need to scale out the AZs in the corresponding availability zone and scale out the racks in the corresponding AZ.

If this three-layer label structure is directly adopted, after scaling out an AZ, you might need to apply new labels and the data in TiKV needs to be rebalanced.

### High availability and disaster recovery analysis

The multiple AZs in one region deployment can guarantee that if one AZ fails, the cluster can automatically recover services without manual intervention. Data consistency is also guaranteed. Note that scheduling policies are used to optimize performance, but when a failure occurs, these policies prioritize availability over performance.
