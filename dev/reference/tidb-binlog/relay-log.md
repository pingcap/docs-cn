---
title: TiDB Binlog Relay Log
category: reference
aliases: ['/docs-cn/dev/reference/tools/tidb-binlog/relay-log/']
---

# TiDB Binlog Relay Log

drainer 同步 binlog 时会拆分上游的事务并发写下游。在极端情况下，上游集群不可用并且 drainer 异常退出后，下游集群 (MySQL 或 TiDB) 可能处于数据不一致的中间状态。在此场景下，drainer 借助 relay log 可以确保将下游集群同步到一个一致的状态。

## Drainer 同步时的一致性状态

下游集群达到一致的状态是指

* 下游集群的数据等同于上游设置了 `tidb_snapshot = ts` 的快照。

checkpoint 状态一致性：

Drainer checkpoint 通过 `consistent` 保存了同步的一致性状态。Drainer 运行时 `consistence` 为 `false`，正常退出后 `consistent` 更新为 `true`。

```sql
select * from tidb_binlog.checkpoint;
+---------------------+----------------------------------------------------------------+
| clusterID           | checkPoint                                                     |
+---------------------+----------------------------------------------------------------+
| 6791641053252586769 | {"consistent":false,"commitTS":414529105591271429,"ts-map":{}} |
+---------------------+----------------------------------------------------------------+
```

## 工作原理

Drainer 开启 relay log 后会先将 binlog event 写到磁盘上，然后再同步给下游集群。

如果上游集群不可用，Drainer 可以通过读取 relay log 把下游集群恢复到一个一致的状态。

> **注意：**
>
> 若同时丢失 relay log 数据，该方法将不可用，不过这是概率极小的事件。此外可以使用 NFS 等网络文件系统来保证 relay log 的数据安全。

### 触发从 relay log 消费 binlog

Drainer 启动时连接不上上游集群的 PD 并且探测到 checkpoint 的 `consistent = false` , 会尝试读取 relay log，并将下游集群恢复到一致的状态。然后 Drainer 进程将 checkpoint 的 `status` 设置为 `0` 后主动退出。

### Relay log 的 GC 机制

Drainer 在运行时如果确认已经将一个 relay log 文件的全部数据都成功同步到下游了，就会马上删除这个文件，所以 relay log 不会占用过多空间。一个 Relay log 文件大小达到 10MB（默认）时就会做切分，数据开始写入新的 relay log 文件。

## 配置

在 Drainer 中添加以下配置来开启 relay log 功能：

```
[syncer.relay]
# 保存 relay log 的目录，空值表示不开启。
# 只有下游是 TiDB 或 MySQL 时该配置才有生效。
log-dir = "/dir/to/save/log"
```
