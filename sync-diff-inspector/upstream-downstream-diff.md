---
title: TiDB 主从集群的数据校验
aliases: ['/docs-cn/dev/sync-diff-inspector/upstream-downstream-diff/','/docs-cn/dev/reference/tools/sync-diff-inspector/tidb-diff/']
---

# TiDB 主从集群的数据校验

当你使用 TiCDC 搭建 TiDB 的主从集群时，可能会需要在不停止同步的情况下对上下游的数据进行一致性验证。在普通的同步模式中，TiCDC 只提供数据的最终一致性的保证，而无法确保在同步的过程中数据的一致性。因此，对动态变更的数据进行一致性校验非常困难，为了满足这一需求，TiCDC 提供了 Syncpoint 功能。

Syncpoint 通过利用 TiDB 提供的 snapshot 特性，让 TiCDC 在同步过程中维护了一个上下游具有一致性 snapshot 的 `ts-map`。把校验动态数据的一致性问题转化为了校验静态 snapshot 数据的一致性问题，达到了接近数据一致性实时校验的效果。

要开启 SyncPoint 功能，你可以在创建同步任务时把 TiCDC 的配置项 `enable-sync-point` 设置为 `true`。开启 Syncpoint 功能后，TiCDC 在数据的同步过程中会根据你所配置的 TiCDC 参数 `sync-point-interval` 来定时对齐上下游的 snapshot，并将上下游的 TSO 对应关系保存在下游的 `tidb_cdc.syncpoint_v1` 表中。

然后，你只需要在 sync-diff-inspector 中配置 `snapshot` 即可对 TiDB 主从集群的数据进行校验。以下 TiCDC 配置示例为创建的同步任务开启 Syncpoint 功能：

```toml
# 开启 SyncPoint
enable-sync-point = true

# 每隔 5 分钟对齐一次上下游的 snapshot
sync-point-interval = "5m"

# 每隔 1 小时清理一次下游 tidb_cdc.syncpoint_v1 表中的 ts-map 数据
sync-point-retention = "1h"
```

## 获取 ts-map

在下游 TiDB 中执行以下 SQL 语句：

{{< copyable "sql" >}}

```sql
select * from tidb_cdc.syncpoint_v1;
```

```
+------------------+----------------+--------------------+--------------------+---------------------+
| ticdc_cluster_id | changefeed     | primary_ts         | secondary_ts       | created_at          |
+------------------+----------------+--------------------+--------------------+---------------------+
| default          | default_test-2 | 435953225454059520 | 435953235516456963 | 2022-09-13 08:40:15 |
+------------------+----------------+--------------------+--------------------+---------------------+
```

以上 `syncpoint_v1` 表中各列所代表的信息如下:

- `ticdc_cluster_id`：插入该条记录的 TiCDC 集群的 ID。
- `changefeed`：插入该条记录的 Changefeed 的 ID。由于不同的 TiCDC 集群可能会存在重名的 Changefeed，所以需要通过 TiCDC 集群 ID 和 Changefeed 的 ID 来确认一个 Changefeed 所插入的 `ts-map`。
- `primary_ts`：上游数据库 snapshot 的时间戳。
- `secondary_ts`：下游数据库 snapshot 的时间戳。
- `created_at`：插入该条记录的时间。

## 配置 snapshot

使用上一步骤获取的 ts-map 信息来配置上下游数据库的 snapshot 信息。其中的 `Datasource config` 部分示例配置如下：

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
    password = ""
    snapshot = "435953235516456963"
```

## 注意事项

- TiCDC 在创建 Changefeed 前，请确保 TiCDC 的配置项 `enable-sync-point` 已设置为 `true`，这样才会开启 Syncpoint 功能，在下游保存 `ts-map`。完整的配置请参考 [TiCDC 同步任务配置文件描述](/ticdc/manage-ticdc.md#同步任务配置文件描述)。
- 需要调整 TiKV 的 GC 时间，保证在校验时 snapshot 对应的历史数据不会被执行 GC。建议调整为 1 个小时，在校验后再还原 GC 设置。
- 以上配置只展示 `Datasource config` 部分，并不完全。完整配置请参考 [sync-diff-inspector 用户文档](/sync-diff-inspector/sync-diff-inspector-overview.md)。