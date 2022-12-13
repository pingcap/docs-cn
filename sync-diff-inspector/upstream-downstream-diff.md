---
title: Data Check for TiDB Upstream and Downstream Clusters
summary: Learn how to check data for TiDB upstream and downstream clusters.
aliases: ['/docs/dev/sync-diff-inspector/upstream-downstream-diff/','/docs/dev/reference/tools/sync-diff-inspector/tidb-diff/']
---

# Data Check for TiDB Upstream and Downstream Clusters

When you use TiCDC to build upstream and downstream clusters of TiDB, you might need to verify the consistency of upstream and downstream data without stopping replication. In the regular replication mode, TiCDC only guarantees that the data is eventually consistent, but cannot guarantee that the data is consistent during the replication process. Therefore, it is difficult to verify the consistency of dynamically changing data. To meet such a need, TiCDC provides the Syncpoint feature.

Syncpoint uses the snapshot feature provided by TiDB and enables TiCDC to maintain a `ts-map` that has consistency between upstream and downstream snapshots during the replication process. In this way, the issue of verifying the consistency of dynamic data is converted to the issue of verifying the consistency of static snapshot data, which achieves the effect of nearly real-time verification.

To enable the Syncpoint feature, set the value of the TiCDC configuration item `enable-sync-point` to `true` when creating a replication task. After enabling Syncpoint, TiCDC will periodically align the upstream and downstream snapshots according to the TiCDC parameter `sync-point-interval` during the data replication process, and will save the upstream and downstream TSO correspondences in the downstream `tidb_cdc.syncpoint_v1` table.

Then, you only need to configure `snapshot` in sync-diff-inspector to verify the data of the TiDB upstream-downstream clusters. The following TiCDC configuration example enables Syncpoint for a created replication task:

```toml
# Enables SyncPoint.
enable-sync-point = true

# Aligns the upstream and downstream snapshots every 5 minutes
sync-point-interval = "5m"

# Cleans up the ts-map data in the downstream tidb_cdc.syncpoint_v1 table every hour
sync-point-retention = "1h"
```

## Step 1: obtain `ts-map`

You can execute the following SQL statement in the downstream TiDB cluster to obtain the upstream TSO (`primary_ts`) and downstream TSO (`secondary_ts`):

```sql
select * from tidb_cdc.syncpoint_v1;
+------------------+----------------+--------------------+--------------------+---------------------+
| ticdc_cluster_id | changefeed     | primary_ts         | secondary_ts       | created_at          |
+------------------+----------------+--------------------+--------------------+---------------------+
| default          | test-2 | 435953225454059520 | 435953235516456963 | 2022-09-13 08:40:15 |
+------------------+----------------+--------------------+--------------------+---------------------+
```

The fields in the preceding `syncpoint_v1` table are described as follows:

- `ticdc_cluster_id`: The ID of the TiCDC cluster in this record.
- `changefeed`: The ID of the changefeed in this record. Because different TiCDC clusters might have changefeeds with the same name, you need to confirm the `ts-map` inserted by a changefeed with the TiCDC cluster ID and changefeed ID.
- `primary_ts`: The timestamp of the upstream database snapshot.
- `secondary_ts`: The timestamp of the downstream database snapshot.
- `created_at`: The time when this record is inserted.

## Step 2: configure snapshot

Then configure the snapshot information of the upstream and downstream databases by using the `ts-map` information obtained in [Step 1](#step-1-obtain-ts-map).

Here is a configuration example of the `Datasource config` section:

```toml
######################### Datasource config ########################
[data-sources.uptidb]
    host = "172.16.0.1"
    port = 4000
    user = "root"
    password = ""
    snapshot = "435953225454059520"

[data-sources.downtidb]
    host = "172.16.0.2"
    port = 4000
    user = "root"
    snapshot = "435953235516456963"
```

## Notes

- Before TiCDC creates a changefeed, make sure that the value of the TiCDC configuration item `enable-sync-point` is set to `true`. Only in this way, Syncpoint is enabled and the `ts-map` is saved in the downstream. For the complete configuration, see [TiCDC task configuration file](/ticdc/ticdc-changefeed-config.md).
- Modify the Garbage Collection (GC) time of TiKV to ensure that the historical data corresponding to snapshot is not collected by GC during the data check. It is recommended that you modify the GC time to 1 hour and recover the setting after the check.
- The above example only shows the section of `Datasource config`. For complete configuration, refer to [sync-diff-inspector User Guide](/sync-diff-inspector/sync-diff-inspector-overview.md).
- Since v6.4.0, only the changefeed with the `SYSTEM_VARIABLES_ADMIN` or `SUPER` privilege can use the TiCDC Syncpoint feature.
