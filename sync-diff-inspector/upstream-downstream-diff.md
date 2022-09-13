---
title: TiDB 主从集群的数据校验
aliases: ['/docs-cn/dev/sync-diff-inspector/upstream-downstream-diff/','/docs-cn/dev/reference/tools/sync-diff-inspector/tidb-diff/']
---

# TiDB 主从集群的数据校验

在你使用 TiCDC 搭建 TiDB 的主从集群时，如果开启了 sync point 功能，那么 TiCDC 在数据的同步过程中会根据你所配置的 `sync-point-interval` 来定时对齐上下游的 snapshot, 并将上下游的 TSO 对应关系保存为 `ts-map`。在 sync-diff-inspector 中配置 `snapshot` 即可对 TiDB 主从集群的数据进行校验。

## 获取 ts-map

在下游 TiDB 中执行以下 SQL 语句：

{{< copyable "sql" >}}

```sql
select * from tidb_cdc.syncpoint_v1;;
```

```
+------------------+----------------+--------------------+--------------------+---------------------+
| ticdc_cluster_id | changefeed     | primary_ts         | secondary_ts       | created_at          |
+------------------+----------------+--------------------+--------------------+---------------------+
| default          | default_test-2 | 435953225454059520 | 435953235516456963 | 2022-09-13 08:40:15 |
+------------------+----------------+--------------------+--------------------+---------------------+
```

以上 `syncpoint_v1` 表中各列所代表的信息如下:

- `ticdc_cluster_id`: 插入该条记录的 TiCDC 集群的 ID。
- `changefeed`: 插入该条记录的 Changefeed 的 ID，由于不同的 TiCDC 集群可能会存在重名的 Changefeed，所以需要通过 TiCDC 集群 ID 和 Changefeed 的 ID 来唯一确认一个 Changefeed 所插入的 `ts-map`。
- `primary_ts`: 上游数据库 snapshot 的 ts。
- `secondary_ts`: 下游数据库 snapshot 的 ts。
- `created_at`: 插入该条记录的时间。


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

- TiCDC 在创建 Changefeed 时， `enable-sync-point` 需要设置为 `true`，这样才会开启 sync point 功能，在下游保存 `ts-map`。完整的配置请参考 [TiCDC 同步任务配置文件描述](/ticdc/manage-ticdc.md#同步任务配置文件描述)
- 需要调整 TiKV 的 GC 时间，保证在校验时 snapshot 对应的历史数据不会被执行 GC。建议调整为 1 个小时，在校验后再还原 GC 设置。
- 以上配置只展示 `Datasource config` 部分，并不完全。完整配置请参考 [sync-diff-inspector 用户文档](/sync-diff-inspector/sync-diff-inspector-overview.md)。