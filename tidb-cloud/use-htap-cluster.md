---
title: Use an HTAP Cluster
summary: Learn how to use HTAP cluster in TiDB Cloud.
---

# Use an HTAP Cluster

[HTAP](https://en.wikipedia.org/wiki/Hybrid_transactional/analytical_processing) means Hybrid Transactional/Analytical Processing. The HTAP cluster in TiDB Cloud is composed of [TiKV](https://tikv.org), a row-based storage engine designed for transactional processing, and [TiFlash](https://docs.pingcap.com/tidb/stable/tiflash-overview), a columnar storage designed for analytical processing. Your application data is first stored in TiKV and then replicated to TiFlash via the Raft consensus algorithm. So it is real time replication from the row store to the columnar store.

With TiDB Cloud, you can create an HTAP cluster easily by specifying one or more TiFlash nodes according to your HTAP workload. If the TiFlash node count is not specified when you create the cluster or you want to add more TiFlash nodes, you can change the node count by [scaling the cluster](/tidb-cloud/scale-tidb-cluster.md).

> **Note:**
>
> TiFlash is always enabled for TiDB Serverless clusters. You cannot disable it.

TiKV data is not replicated to TiFlash by default. You can select which table to replicate to TiFlash using the following SQL statement:

{{< copyable "sql" >}}

```sql
ALTER TABLE table_name SET TIFLASH REPLICA 1;
```

The number of replicas count must be no larger than the number of TiFlash nodes. Setting the number of replicas to `0` means deleting the replica in TiFlash.

To check the replication progress, use the following command:

{{< copyable "sql" >}}

```sql
SELECT * FROM information_schema.tiflash_replica WHERE TABLE_SCHEMA = '<db_name>' and TABLE_NAME = '<table_name>';
```

## Use TiDB to read TiFlash replicas

After data is replicated to TiFlash, you can use one of the following three ways to read TiFlash replicas to accelerate your analytical computing.

### Smart selection

For tables with TiFlash replicas, the TiDB optimizer automatically determines whether to use TiFlash replicas based on the cost estimation. For example:

{{< copyable "sql" >}}

```sql
explain analyze select count(*) from test.t;
```

```sql
+--------------------------+---------+---------+--------------+---------------+----------------------------------------------------------------------+--------------------------------+-----------+------+
| id                       | estRows | actRows | task         | access object | execution info                                                       | operator info                  | memory    | disk |
+--------------------------+---------+---------+--------------+---------------+----------------------------------------------------------------------+--------------------------------+-----------+------+
| StreamAgg_9              | 1.00    | 1       | root         |               | time:83.8372ms, loops:2                                              | funcs:count(1)->Column#4       | 372 Bytes | N/A  |
| └─TableReader_17         | 1.00    | 1       | root         |               | time:83.7776ms, loops:2, rpc num: 1, rpc time:83.5701ms, proc keys:0 | data:TableFullScan_16          | 152 Bytes | N/A  |
|   └─TableFullScan_16     | 1.00    | 1       | cop[tiflash] | table:t       | time:43ms, loops:1                                                   | keep order:false, stats:pseudo | N/A       | N/A  |
+--------------------------+---------+---------+--------------+---------------+----------------------------------------------------------------------+--------------------------------+-----------+------+
```

`cop[tiflash]` means that the task will be sent to TiFlash for processing. If your queries have not selected a TiFlash replica, try to update the statistics using the `analyze table` statement, and then check the result using the `explain analyze` statement.

### Engine isolation

Engine isolation is to specify that all queries use a replica of the specified engine by configuring the `tidb_isolation_read_engines` variable. The optional engines are "tikv", "tidb" (indicates the internal memory table area of TiDB, which stores some TiDB system tables and cannot be actively used by users), and "tiflash".

{{< copyable "sql" >}}

```sql
set @@session.tidb_isolation_read_engines = "engine list separated by commas";
```

### Manual hint

Manual hint can force TiDB to use specified replicas for one or more specific tables on the premise of satisfying engine isolation. Here is an example of using the manual hint:

{{< copyable "sql" >}}

```sql
select /*+ read_from_storage(tiflash[table_name]) */ ... from table_name;
```

To learn more about TiFlash, refer to the documentation [here](https://docs.pingcap.com/tidb/stable/tiflash-overview/).
