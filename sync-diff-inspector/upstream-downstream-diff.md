---
title: Data Check for TiDB Upstream and Downstream Clusters
summary: Learn how to check data for TiDB upstream and downstream clusters.
aliases: ['/docs/dev/sync-diff-inspector/upstream-downstream-diff/','/docs/dev/reference/tools/sync-diff-inspector/tidb-diff/']
---

# Data Check for TiDB Upstream and Downstream Clusters

You can use TiDB Binlog to build upstream and downstream clusters of TiDB. When Drainer replicates data to TiDB, the checkpoint is saved and the TSO mapping relationship between the upstream and downstream is also saved as `ts-map`. To check data between the upstream and downstream, configure `snapshot` in sync-diff-inspector.

## Step 1: obtain `ts-map`

To obtain `ts-map`, execute the following SQL statement in the downstream TiDB cluster:

```sql
mysql> select * from tidb_binlog.checkpoint;
+---------------------+---------------------------------------------------------------------------------------------------------+
| clusterID           | checkPoint                                                                                              |
+---------------------+---------------------------------------------------------------------------------------------------------+
| 6711243465327639221 | {"commitTS":409622383615541249,"ts-map":{"primary-ts":409621863377928194,"secondary-ts":409621863377928345}} |
+---------------------+---------------------------------------------------------------------------------------------------------+
```

## Step 2: configure snapshot

Then configure the snapshot information of the upstream and downstream databases by using the `ts-map` information obtained in [Step 1](#step-1-obtain-ts-map).

Here is a configuration example of the `Datasource config` section:

```toml
######################### Datasource config ########################
[data-sources.mysql1]
    host = "127.0.0.1"
    port = 3306
    user = "root"
    password = ""
    snapshot = "409621863377928345"
[data-sources.tidb0]
    host = "127.0.0.1"
    port = 4000
    user = "root"
    snapshot = "409621863377928345"
```

> **Note:**
>
> - Set `db-type` of Drainer to `tidb` to ensure that `ts-map` is saved in the checkpoint.
> - Modify the Garbage Collection (GC) time of TiKV to ensure that the historical data corresponding to snapshot is not collected by GC during the data check. It is recommended that you modify the GC time to 1 hour and recover the setting after the check.
> - In some versions of TiDB Binlog, `master-ts` and `slave-ts` are stored in `ts-map`. `master-ts` is equivalent to `primary-ts` and `slave-ts` is equivalent to `secondary-ts`.
> - The above example only shows the section of `Datasource config`. For complete configuration, refer to [sync-diff-inspector User Guide](/sync-diff-inspector/sync-diff-inspector-overview.md).