---
title: Follower Read
summary: This document describes the use and implementation of Follower Read.
aliases: ['/docs/dev/follower-read/','/docs/dev/reference/performance/follower-read/']
---

# Follower Read

When a read hotspot appears in a Region, the Region leader can become a read bottleneck for the entire system. In this situation, enabling the Follower Read feature can significantly reduce the load of the leader, and improve the throughput of the whole system by balancing the load among multiple followers. This document introduces the use and implementation mechanism of Follower Read.

## Overview

The Follower Read feature refers to using any follower replica of a Region to serve a read request under the premise of strongly consistent reads. This feature improves the throughput of the TiDB cluster and reduces the load of the leader. It contains a series of load balancing mechanisms that offload TiKV read loads from the leader replica to the follower replica in a Region. TiKV's Follower Read implementation provides users with strongly consistent reads.

> **Note:**
>
> To achieve strongly consistent reads, the follower node currently needs to request the current execution progress from the leader node (that is `ReadIndex`), which causes an additional network request overhead. Therefore, the main benefits of Follower Read are to isolate read requests from write requests in the cluster and to increase overall read throughput.

## Usage

To enable TiDB's Follower Read feature, modify the value of the `tidb_replica_read` variable to `follower` or `leader-and-follower`:

{{< copyable "sql" >}}

```sql
set [session | global] tidb_replica_read = '<target value>';
```

Scope: SESSION | GLOBAL

Default: leader

This variable is used to set the expected data read mode.

- When the value of `tidb_replica_read` is set to `leader` or an empty string, TiDB maintains its original behavior and sends all read operations to the leader replica to perform.
- When the value of `tidb_replica_read` is set to `follower`, TiDB selects a follower replica of the Region to perform all read operations.
- When the value of `tidb_replica_read` is set to `leader-and-follower`, TiDB can select any replicas to perform read operations. In this mode, read requests are load balanced between the leader and follower.
- When the value of `tidb_replica_read` is set to `closest-replicas`, TiDB prefers to select a replica in the same region to perform read operations, which can be a leader or a follower. If there is no replica in the same region, TiDB reads from the leader replica.
- When the value of `tidb_replica_read` is set to `closest-adaptive`, if the estimated result of a read request is greater than or equal to the value of [`tidb_adaptive_closest_read_threshold`](/system-variables.md#tidb_adaptive_closest_read_threshold-new-in-v630), TiDB prefers to read from a replica in the same region. Otherwise, TiDB reads from the leader replica. To prevent unbalanced read traffic distribution in various regions, TiDB dynamically detects whether the region distribution of all online TiDB and TiKV nodes is balanced. If a region contains only TiDB or TiKV nodes, TiDB forces to select the leader replica to perform read operations. For example, if all TiDB nodes in a region are down, then other online TiDB nodes are downgraded to read using leader replicas. After at least one TiDB node in this region is back online, all TiDB nodes switch back to preferring to select the replica in the same region to perform read operations.

<CustomContent platform="tidb">

> **Note:**
>
> When the value of `tidb_replica_read` is set to `closest-replicas` or `closest-adaptive`, you need to configure the cluster to ensure that replicas are distributed across regions according to the specified configuration. To configure `location-labels` for PD and set the correct `labels` for TiDB and TiKV, refer to [Schedule replicas by topology labels](/schedule-replicas-by-topology-labels.md). TiDB depends on the `zone` label to match TiKV nodes in the same region, so you need to make sure that the `zone` label is included in the `location-labels` of PD and `zone` is included in the configuration of each TiDB and TiKV node. If your cluster is deployed using TiDB Operator, refer to [High availability of data](https://docs.pingcap.com/tidb-in-kubernetes/stable/configure-a-tidb-cluster#high-availability-of-data).

</CustomContent>

## Implementation mechanism

Before the Follower Read feature was introduced, TiDB applied the strong leader principle and submitted all read and write requests to the leader node of a Region to handle. Although TiKV can distribute Regions evenly on multiple physical nodes, for each Region, only the leader can provide external services. The other followers can do nothing to handle read requests but receive the data replicated from the leader at all times and prepare for voting to elect a leader in case of a failover.

To allow data reading in the follower node without violating linearizability or affecting Snapshot Isolation in TiDB, the follower node needs to use `ReadIndex` of the Raft protocol to ensure that the read request can read the latest data that has been committed on the leader. At the TiDB level, the Follower Read feature simply needs to send the read request of a Region to a follower replica based on the load balancing policy.

### Strongly consistent reads

When the follower node processes a read request, it first uses `ReadIndex` of the Raft protocol to interact with the leader of the Region, to obtain the latest commit index of the current Raft group. After the latest commit index of the leader is applied locally to the follower, the processing of a read request starts.

### Follower replica selection strategy

Because the Follower Read feature does not affect TiDB's Snapshot Isolation transaction isolation level, TiDB adopts the round-robin strategy to select the follower replica. Currently, for the coprocessor requests, the granularity of the Follower Read load balancing policy is at the connection level. For a TiDB client connected to a specific Region, the selected follower is fixed, and is switched only when it fails or the scheduling policy is adjusted.

However, for the non-coprocessor requests, such as a point query, the granularity of the Follower Read load balancing policy is at the transaction level. For a TiDB transaction on a specific Region, the selected follower is fixed, and is switched only when it fails or the scheduling policy is adjusted.
