---
title: Usage Scenarios of Stale Read
summary: Learn about Stale Read and its usage scenarios.
---

# Usage Scenarios of Stale Read

This document describes the usage scenarios of Stale Read. Stale Read is a mechanism that TiDB applies to read historical versions of data stored in TiDB. Using this mechanism, you can read the corresponding historical data of a specific point in time or within a specified time range, and thus save the latency brought by data replication between storage nodes.

When you are using Stale Read, TiDB will randomly select a replica for data reading, which means that all replicas are available for data reading. If your application cannot tolerate reading non-real-time data, do not use Stale Read; otherwise, the data read from the replica might not be the latest data written into TiDB.

## Scenario examples

<CustomContent platform="tidb">

+ Scenario one: If a transaction only involves read operations and is tolerant of data staleness to some extent, you can use Stale Read to get historical data. Using Stale Read, TiDB makes the query requests sent to any replica at the expense of some real-time performance, and thus increases the throughput of query executions. Especially in some scenarios where small tables are queried, if strongly consistent reads are used, leader might be concentrated on a certain storage node, causing the query pressure to be concentrated on that node as well. Therefore, that node might become a bottleneck for the whole query. Stale Read, however, can improve the overall query throughput and significantly improve the query performance.

+ Scenario two: In some scenarios of geo-distributed deployment, if strongly consistent follower reads are used, to make sure that the data read from the Followers is consistent with that stored in the Leader, TiDB requests `Readindex` from different data centers for verification, which increases the access latency for the whole query process. With Stale Read, TiDB accesses the replica in the current data center to read the corresponding data at the expense of some real-time performance, which avoids network latency brought by cross-center connection and reduces the access latency for the entire query. For more information, see [Local Read under Three Data Centers Deployment](/best-practices/three-dc-local-read.md).

</CustomContent>

<CustomContent platform="tidb-cloud">

If a transaction only involves read operations and is tolerant of data staleness to some extent, you can use Stale Read to get historical data. Using Stale Read, TiDB makes the query requests sent to any replica at the expense of some real-time performance, and thus increases the throughput of query executions. Especially in some scenarios where small tables are queried, if strongly consistent reads are used, leader might be concentrated on a certain storage node, causing the query pressure to be concentrated on that node as well. Therefore, that node might become a bottleneck for the whole query. Stale Read, however, can improve the overall query throughput and significantly improve the query performance.

</CustomContent>

## Usages

TiDB provides the methods of performing Stale Read at the statement level, the session level and the global level as follows:

- Statement level
    - Specifying an exact point in time (**recommended**): If you need TiDB to read data that is globally consistent from a specific point in time without violating the isolation level, you can specify the corresponding timestamp of that point in time in the query statement. For detailed usage, see [`AS OF TIMESTAMP` clause](/as-of-timestamp.md#syntax).
    - Specifying a time range: If you need TiDB to read the data as new as possible within a time range without violating the isolation level, you can specify the time range in the query statement. Within the specified time range, TiDB selects a suitable timestamp to read the corresponding data. "Suitable" means there are no transactions that start before this timestamp and have not been committed on the accessed replica, that is, TiDB can perform read operations on the accessed replica and the read operations are not blocked. For detailed usage, refer to the introduction of the [`AS OF TIMESTAMP` Clause](/as-of-timestamp.md#syntax) and the [`TIDB_BOUNDED_STALENESS` function](/as-of-timestamp.md#syntax).
- Session level
    - Specifying a time range: In a session, if you need TiDB to read the data as new as possible within a time range in subsequent queries without violating the isolation level, you can specify the time range by setting the `tidb_read_staleness` system variable. For detailed usage, refer to [`tidb_read_staleness`](/tidb-read-staleness.md).

Besides, TiDB provides a way to specify an exact point in time by setting the [`tidb_external_ts`](/system-variables.md#tidb_external_ts-new-in-v640) system variable on session or global level. For detailed usage, refer to [Perform Stale Read Using `tidb_external_ts`](/tidb-external-ts.md).

### Reduce Stale Read latency

The Stale Read feature periodically advances the Resolved TS timestamp of the TiDB cluster, which ensures that TiDB reads data that meets transaction consistency. If the timestamp used by Stale Read (for example, `AS OF TIMESTAMP '2016-10-08 16:45:26'`) is greater than the Resolved TS, Stale Read will trigger TiDB to advance the Resolved TS first and wait for the advance to complete before reading the data, leading to an increase in latency.

To reduce the Stale Read latency, you can modify the following TiKV configuration item to make TiDB advance the Resolved TS timestamp more frequently:

```toml
[resolved-ts]
advance-ts-interval = "20s" # The default value is "20s". You can set it to a smaller value such as "1s" to advance the Resolved TS timestamp more frequently.
```

> **Note:**
>
> Decreasing the preceding TiKV configuration item will lead to an increase in TiKV CPU usage and traffic between nodes.

## Restrictions

When a Stale Read query for a table is pushed down to TiFlash, the query will return an error if this table has newer DDL operations executed after the read timestamp specified by the query. This is because TiFlash only supports reading data from the tables with the latest schemas.

Take the following table as an example:

```sql
create table t1(id int);
alter table t1 set tiflash replica 1;
```

Execute the following DDL operation after one minute:

```sql
alter table t1 add column c1 int not null;
```

Then, use Stale Read to query the data from one minute ago:

```sql
set @@session.tidb_enforce_mpp=1;
select * from t1 as of timestamp NOW() - INTERVAL 1 minute;
```

TiFlash will report an error as follows:

```
ERROR 1105 (HY000): other error for mpp stream: From MPP<query:<query_ts:1673950975508472943, local_query_id:18, server_id:111947, start_ts:438816196526080000>,task_id:1>: Code: 0, e.displayText() = DB::TiFlashException: Table 323 schema version 104 newer than query schema version 100, e.what() = DB::TiFlashException,
```

To avoid this error, you can change the read timestamp specified by Stale Read to the time after the DDL operation.