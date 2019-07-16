---
title: TiDB 主从集群的数据校验
category: tools
---

### TiDB 主从集群的数据校验

用户可以使用 TiDB-Binlog 搭建 TiDB 的主从集群，在 Drainer 把数据同步到 TiDB 时，Drainer 会在保存 checkpoint 时保存上下游的 tso 的对应关系 `ts-map`，在 sync-diff-inspector 中配置 `snapshot` 即可对 TiDB 主从集群的数据进行校验。

#### 获取 ts-map

在下游 TiDB 中执行以下 SQL：

```
    mysql> select * from tidb_binlog.checkpoint;
    +---------------------+---------------------------------------------------------------------------------------------+
    | clusterID           | checkPoint                                                                                  |
    +---------------------+---------------------------------------------------------------------------------------------
    | 6711243465327639221 | {"commitTS":409622383615541249,"ts-map":{"master-ts":409621863377928194,"slave-ts":409621863377928345}} |
    +---------------------+---------------------------------------------------------------------------------------------+
```

从结果中可以获取 ts-map 信息。

#### 配置 snapshot

使用上一步骤获取的 ts-map 信息来配置上下游数据库的 snapshot 信息。其中的 `Database config` 部分示例配置如下：

```

######################### Databases config #########################

# 源数据库实例的配置
[[source-db]]
    host = "127.0.0.1"
    port = 4000
    user = "root"
    password = "123456"
    # 源数据库实例的 id，唯一标识一个数据库实例
    instance-id = "source-1"
    # 使用 TiDB 的 snapshot 功能，如果开启的话会使用历史数据进行对比
    snapshot = "409621863377928194"

# 目标数据库实例的配置
[target-db]
    host = "127.0.0.1"
    port = 4001
    user = "root"
    password = "123456"
    # 使用 TiDB 的 snapshot 功能，如果开启的话会使用历史数据进行对比
    snapshot = "409621863377928345"
```


#### 注意

1. Drainer 的 `db-type` 需要设置为 `tidb` ，这样才会在 checkpoint 中保存 `ts-map`。
2. 需要调整 tikv 的 gc 时间，保证在校验时 snapshot 对应的历史数据不会被 gc。建议调整为1个小时，在校验后再还原 gc 设置。