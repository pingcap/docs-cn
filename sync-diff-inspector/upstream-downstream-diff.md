---
title: TiDB 主从集群的数据校验
aliases: ['/docs-cn/dev/sync-diff-inspector/upstream-downstream-diff/','/docs-cn/dev/reference/tools/sync-diff-inspector/tidb-diff/']
---

# TiDB 主从集群的数据校验

用户可以使用 TiDB Binlog 搭建 TiDB 的主从集群，Drainer 在把数据同步到 TiDB 时，保存 checkpoint 的同时也会将上下游的 TSO 对应关系保存为 `ts-map`。在 sync-diff-inspector 中配置 `snapshot` 即可对 TiDB 主从集群的数据进行校验。

## 获取 ts-map

在下游 TiDB 中执行以下 SQL 语句：

{{< copyable "sql" >}}

```sql
select * from tidb_binlog.checkpoint;
```

```
+---------------------+--------------------------------------------------------------------------------------------------------------+
| clusterID           | checkPoint                                                                                                   |
+---------------------+--------------------------------------------------------------------------------------------------------------+
| 6711243465327639221 | {"commitTS":409622383615541249,"ts-map":{"primary-ts":409621863377928194,"secondary-ts":409621863377928345}} |
+---------------------+--------------------------------------------------------------------------------------------------------------+
```

从结果中可以获取 ts-map 信息。

## 配置 snapshot

使用上一步骤获取的 ts-map 信息来配置上下游数据库的 snapshot 信息。其中的 `Databases config` 部分示例配置如下：

```toml
######################### Databases config ########################
[data-sources.mysql1]
    host = "127.0.0.1"
    port = 3306
    user = "root"
    password = ""
    # remove comment if use tidb's snapshot data
    snapshot = "2016-10-08 16:45:26"

[data-sources.tidb]
    host = "127.0.0.1"
    port = 4000
    user = "root"
    password = ""
    # remove comment if use tidb's snapshot data
    snapshot = "409621863377928345"
```

## 注意事项

- Drainer 的 `db-type` 需要设置为 `tidb`，这样才会在 checkpoint 中保存 `ts-map`。
- 需要调整 TiKV 的 GC 时间，保证在校验时 snapshot 对应的历史数据不会被执行 GC。建议调整为 1 个小时，在校验后再还原 GC 设置。