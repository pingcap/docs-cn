---
title: Usage Scenarios of Stale Read
summary: Learn about Stale Read and its usage scenarios.
---

# Usage Scenarios of Stale Read

This document describes the usage scenarios of Stale Read. Stale Read is a mechanism that TiDB applies to read historical versions of data stored in TiDB. Using this mechanism, you can read the corresponding historical data of a specific point in time or within a specified time range, and thus save the latency brought by data replication between storage nodes.

When you are using Steal Read, TiDB will randomly select a replica for data reading, which means that all replicas are available for data reading. If your application cannot tolerate reading non-real-time data, do not use Stale Read; otherwise, the data read from the replica might not be the latest data written into TiDB.

> **Warning:**
>
> Currently, Stale Read is an experimental feature. It is not recommended to use it in the production environment.

## Scenario examples

+ Scenario one: If a transaction only involves read operations and is tolerant of data staleness to some extent, you can use Stale Read to get historical data. Using Stale Read, TiDB makes the query requests sent to any replica at the expense of some real-time performance, and thus increases the throughput of query executions. Especially in some scenarios where small tables are queried, if strongly consistent reads are used, leader might be concentrated on a certain storage node, causing the query pressure to be concentrated on that node as well. Therefore, that node might become a bottleneck for the whole query. Stale Read, however, can improve the overall query throughput and significantly improve the query performance.

+ Scenario two: In some scenarios of geo-distributed deployment, if strongly consistent follower reads are used, to make sure that the data read from the Followers is consistent with that stored in the Leader, TiDB requests `Readindex` from different data centers for verification, which increases the access latency for the whole query process. With Stale Read, TiDB accesses the replica in the current data center to read the corresponding data at the expense of some real-time performance, which avoids network latency brought by cross-center connection and reduces the access latency for the entire query. For more information, see [Local Read under Three Data Centers Deployment](/best-practices/three-dc-local-read.md).

## Usages

In TiDB, you can specify either an exact point in time or a time range when performing stale reads:

- Specifying an exact point in time (recommended): If you need TiDB to read data that follows the global transaction consistency from a specific point in time without damaging the isolation level, you can specify the corresponding timestamp of that point in time in the query statement. For detailed usage, see [`AS OF TIMESTAMP` Clause](/as-of-timestamp.md#syntax).
- Specifying a time range: If you need TiDB to read data as new as possible within a time range without damaging the isolation level, you can specify the time range in the query statement. Then, TiDB selects a suitable timestamp within the specified time range to read the corresponding data. "Suitable" means there are no transactions that start before this timestamp and have not been committed on the accessed replica, that is, TiDB can perform read operations on the accessed replica and the read operations are not blocked. For detailed usage, refer to the introduction of the [`AS OF TIMESTAMP` clause](/as-of-timestamp.md#syntax) and the [`TIDB_BOUNDED_STALENESS` function](/as-of-timestamp.md#syntax).
