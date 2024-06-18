---
title: 主从集群一致性读和数据校验
aliases: ['/docs-cn/dev/sync-diff-inspector/upstream-downstream-diff/','/docs-cn/dev/reference/tools/sync-diff-inspector/tidb-diff/', '/zh/tidb/dev/upstream-downstream-diff']
summary: TiCDC 提供了 Syncpoint 功能，通过利用 TiDB 的 snapshot 特性，在同步过程中维护了一个上下游具有一致性 snapshot 的 `ts-map`。启用 Syncpoint 功能后，可以进行一致性快照读和数据一致性校验。要开启 Syncpoint 功能，只需在创建同步任务时把 TiCDC 的配置项 `enable-sync-point` 设置为 `true`。通过配置 `snapshot` 可以对 TiDB 主从集群的数据进行校验。
---

# TiDB 主从集群数据校验和快照读

当你使用 TiCDC 搭建 TiDB 的主从集群时，可能会需要在不停止同步的情况下对上下游进行一致性的快照读或者对数据进行一致性验证。在普通的同步模式中，TiCDC 只提供数据的最终一致性的保证，而无法确保在同步的过程中数据的一致性。因此，对动态变更的数据进行一致性读非常困难，为了满足这一需求，TiCDC 提供了 Syncpoint 功能。

Syncpoint 通过利用 TiDB 提供的 snapshot 特性，让 TiCDC 在同步过程中维护了一个上下游具有一致性 snapshot 的 `ts-map`。把校验动态数据的一致性问题转化为了校验静态 snapshot 数据的一致性问题，达到了接近数据一致性实时校验的效果。

## 启用 Syncpoint

启用 Syncpoint 功能后，你可以使用[一致性快照读](#一致性快照读)和[数据一致性校验](#数据一致性校验)。

要开启 Syncpoint 功能，只需在创建同步任务时把 TiCDC 的配置项 `enable-sync-point` 设置为 `true`。开启 Syncpoint 功能后，TiCDC 会向下游 TiDB 集群写入如下信息：

1. 在数据的同步过程中，TiCDC 会定期（使用 `sync-point-interval` 参数配置）对齐上下游的快照，并将上下游的 TSO 的对应关系保存在下游的 `tidb_cdc.syncpoint_v1` 表中。

2. 同步过程中，TiCDC 还会定期（使用 `sync-point-interval` 参数配置）通过执行 `SET GLOBAL tidb_external_ts = @@tidb_current_ts` ，在备用集群中设置已复制完成的一致性快照点。

以下是 TiCDC 配置示例，用于在创建同步任务时启用 Syncpoint 功能：

```toml
# 开启 SyncPoint
enable-sync-point = true

# 每隔 5 分钟对齐一次上下游的 snapshot
sync-point-interval = "5m"

# 每隔 1 小时清理一次下游 tidb_cdc.syncpoint_v1 表中的 ts-map 数据
sync-point-retention = "1h"
```

## 一致性快照读

> **注意：**
>
> 使用一致性快照读之前，请先[启用 TiCDC 的 Syncpoint 功能](#启用-syncpoint)。如果多个同步任务使用同一个下游 TiDB 集群且都开启了 Syncpoint 功能，那么这些同步任务都将根据各自的同步进度来更新 `tidb_external_ts` 和 `ts-map`。此时，你需要使用读取 `ts-map` 表中记录的方式来设置同步任务级别的一致性快照读，同时应避免下游应用程序使用 `tidb_enable_external_ts_read` 的方式读数据，因为多个同步任务之间可能存在互相干扰导致无法获得一致性的结果。

当你需要从备用集群查询数据的时候，在业务应用中设置 `SET GLOBAL|SESSION tidb_enable_external_ts_read = ON;` 就可以在备用集群上获得事务状态完成的数据。

除此之外，你也可以通过查询 `ts-map` 的方式选取之前的时间点进行快照读。

## 数据一致性校验

> **注意：**
>
> 使用数据一致性校验之前，请先[启用 TiCDC 的 Syncpoint 功能](#启用-syncpoint)。

你只需要在 sync-diff-inspector 中配置 `snapshot` 即可对 TiDB 主从集群的数据进行校验。

### 获取 ts-map

在下游 TiDB 中执行以下 SQL 语句，从结果中可以获取上游 TSO (primary_ts) 和下游 TSO (secondary_ts) 信息。

{{< copyable "sql" >}}

```sql
select * from tidb_cdc.syncpoint_v1;
```

```
+------------------+----------------+--------------------+--------------------+---------------------+
| ticdc_cluster_id | changefeed     | primary_ts         | secondary_ts       | created_at          |
+------------------+----------------+--------------------+--------------------+---------------------+
| default          | test-2         | 435953225454059520 | 435953235516456963 | 2022-09-13 08:40:15 |
+------------------+----------------+--------------------+--------------------+---------------------+
```

以上 `syncpoint_v1` 表中各列所代表的信息如下:

- `ticdc_cluster_id`：插入该条记录的 TiCDC 集群的 ID。
- `changefeed`：插入该条记录的 Changefeed 的 ID。由于不同的 TiCDC 集群可能会存在重名的 Changefeed，所以需要通过 TiCDC 集群 ID 和 Changefeed 的 ID 来确认一个 Changefeed 所插入的 `ts-map`。
- `primary_ts`：上游数据库 snapshot 的时间戳。
- `secondary_ts`：下游数据库 snapshot 的时间戳。
- `created_at`：插入该条记录的时间。

### 配置 snapshot

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

- TiCDC 在创建 Changefeed 前，请确保 TiCDC 的配置项 `enable-sync-point` 已设置为 `true`，这样才会开启 Syncpoint 功能，在下游保存 `ts-map`。配置项 `sync-point-interval` 的默认格式为 `"h m s"`，例如 `"1h30m30s"`，最小值为 `"30s"`。更多完整的配置信息请参考 [TiCDC 同步任务配置文件描述](/ticdc/ticdc-changefeed-config.md)。
- 在使用 Syncpoint 功能进行数据校验时，需要调整 TiKV 的 GC 时间，保证在校验时 snapshot 对应的历史数据不会被执行 GC。建议调整为 1 个小时，在校验后再还原 GC 设置。
- 以上配置只展示了 `Datasource config` 部分，完整配置请参考 [sync-diff-inspector 用户文档](/sync-diff-inspector/sync-diff-inspector-overview.md)。
- 从 v6.4.0 开始，TiCDC 使用 Syncpoint 功能需要同步任务拥有下游集群的 `SYSTEM_VARIABLES_ADMIN` 或者 `SUPER` 权限。
- 从 v8.2.0 开始，TiCDC 对 primary_ts 值的生成规则做了以下调整：
    - 每当 TiCDC 产生一个新的 primary_ts 时，它必须是 `sync-point-interval` 的整数倍。
    - 对于每个新的 changefeed，TiCDC 会计算出一个初始的 primary_ts。这个初始值是大于或等于 changefeed 开始时间（startTs）的最小的 `sync-point-interval` 的整数倍。

  该设定用于在数据同步过程中，对齐不同 changefeed 的 Sycnpoint。比如多个下游集群可以分别 [flash back](https://docs.pingcap.com/zh/tidb/stable/sql-statement-flashback-table) 到具有相同 primary_ts 的 Syncpoint 的 secondary_ts，从而让下游集群之间获得一致的数据。
