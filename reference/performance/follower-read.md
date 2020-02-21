---
title: Follower Read
summary: This document describes the use and implementation of Follower Read.
category: reference
---

# Follower Read

When a read hotspot appears in a Region, the Region leader can become a read bottleneck for the entire system. In this situation, enabling the Follower Read feature can significantly reduce the load of the leader, and improve the throughput of the whole system by balancing the load among multiple followers. This document introduces the use and implementation mechanism of Follower Read.

## Overview

The Follower Read feature refers to using any follower replica of a Region to serve a read request under the premise of strongly consistent reads. This feature improves the throughput of the TiDB cluster and reduces the load of the leader. It contains a series of load balancing mechanisms that offload TiKV read loads from the leader replica to the follower replica in a Region. TiKV's Follower Read implementation guarantees the linearizability of data reading; combined with Snapshot Isolation in TiDB, this implementation provides users with strongly consistent reads.

> **Note:**
>
> To achieve strongly consistent reads, the follower node currently requires additional `ReadIndex` overhead. Therefore, the main benefits of Follower Read are to isolate read and write requests of the cluster and to increase overall read throughput. Regarding the latency of a single request, it requires one more interaction overhead with `ReadIndex` of the Raft protocol than the traditional leader reads.

## Usage

To enable TiDB's Follower Read feature, set the value of the `tidb_replica_read` session variable to `follower`:

{{<copyable "sql">}}

```sql
set @@tidb_replica_read = 'follower';
```

Scope: SESSION

Default: leader

This variable is used to set the data read mode expected by the current session.

- When the value of `tidb_replica_read` is set to `leader` or an empty string, TiDB maintains its original behavior and sends all read operations to the leader replica to perform.
- When the value of `tidb_replica_read` is set to `follower`, TiDB selects a follower replica of the Region to perform all read operations.

## Implementation mechanism

Before the Follower Read feature was introduced, TiDB applied the strong leader principle and submitted all read and write requests to the leader node of a Region to handle. Although TiKV can distribute Regions evenly on multiple physical nodes, for each Region, only the leader can provide external services. The other followers can do nothing to handle read requests but receive the data replicated from the leader at all times and prepare for voting to elect a leader in case of a failover.

To allow data reading in the follower node without violating linearizability or affecting Snapshot Isolation in TiDB, the follower node needs to use `ReadIndex` of the Raft protocol to ensure that the read request can read the latest data that has been committed on the leader. At the TiDB level, the Follower Read feature simply needs to send the read request of a Region to a follower replica based on the load balancing policy.

### Strongly consistent reads

When the follower node processes a read request, it first uses `ReadIndex` of the Raft protocol to interact with the leader of the Region, to obtain the latest commit index of the current Raft group. After the latest commit index of the leader is applied locally to the follower, the processing of a read request starts.

### Follower replica selection strategy

Because the Follower Read feature guarantees linearizability without affecting Snapshot Isolation, TiDB adopts the round-robin strategy to select the follower replica. Although TiKV can select any follower replica to handle any read request, considering the different replication speed among followers, if the load balancing granularity is too fine, it might cause significant fluctuation of latency. Currently, the granularity of the Follower Read load balancing policy is at the connection level. For a TiDB client connected to a specific Region, the selected follower is fixed, and is switched only when it fails or the scheduling policy is adjusted.
