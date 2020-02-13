---
title: TiDB Binlog relay log
category: reference
aliases: ['/docs-cn/dev/reference/tools/tidb-binlog/relay-log/']
---

# 关于 relay log

drainer 同步 binlog 会拆分上游的事务并发写下游，在极端情况上游集群不可用并且 drainer 异常退出后，同步的下游集群（MySQL/TiDB）可能处于数据不一致的中间状态，而 drainer 借助 relay log 可以确保将下游集群同步到一个一致的状态。

## drainer 同步的状态一致性

下游集群达到一致的状态的定义为：

* 下游集群的数据等同于设置了 _tidb_snapshot = ts_ 的快照上游 TiDB 集群的数据

checkpoint 状态一致性：

drainer checkpoint 保存了一致性状态 consistent，drainer 运行时会是 `false`，正常退出后会更新为 `true`。

```
mysql> select * from tidb_binlog.checkpoint;
+---------------------+----------------------------------------------------------------+
| clusterID           | checkPoint                                                     |
+---------------------+----------------------------------------------------------------+
| 6791641053252586769 | {"consistent":false,"commitTS":414529105591271429,"ts-map":{}} |
+---------------------+----------------------------------------------------------------+
```

## 原理

当 drainer 开启 relay log 后会先将 binlog event 写到磁盘上，然后再同步给下游集群。

如果上游集群不可用，drainer 可以通过读取 relay log 把下游集群恢复到一个一致的状态。

除非同时丢失 relay log 数据，不过这是概率极小的事件。此外可以使用 nfs 等网络文件系统来保证 relay log 的数据安全。


### 触发从 relay log 消费 binlog

当 drainer 启动时连接不上上游集群的 PD 并且探测到 checkpoint 的 `consistent = false` , 会尝试读取 relay log 将下游集群恢复到一个一致的状态，然后 drainer 进程将 checkpoint 的 status 设置为 0 后主动退出。

### relay log GC 机制

drainer 在运行时如果确认已经将一个 relay log 文件的全部数据都成功同步到下游了就会马上删除这个文件，所以不会占用很多空间，默认文件大小达到 10M 就会做切分，开始写新的文件。

## 配置

开启 relay log 功能只需要在 drainer 添加如下配置:

```
[syncer.relay]
# 保存 relay log 的目录，空值表示不开启。
# 只有下游是 TiDB/MySQL 配置才有意意义。
log-dir = "/dir/to/save/log"
```