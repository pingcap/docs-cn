---
title: TiDB Binlog 常见错误修复
---

# TiDB Binlog 常见错误修复

本文档介绍 TiDB Binlog 中常见的错误以及修复方法。

## Drainer 同步数据到 Kafka 时报错 "kafka server: Message was too large, server rejected it to avoid allocation error"

报错原因：如果在 TiDB 中执行了大事务，则生成的 binlog 数据会比较大，可能超过了 Kafka 的消息大小限制。

解决方法：需要调整 Kafka 的配置参数，如下所示。

```
message.max.bytes=1073741824
replica.fetch.max.bytes=1073741824
fetch.message.max.bytes=1073741824
```

## Pump 报错 "no space left on device"

报错原因：本地磁盘空间不足，Pump 无法正常写 binlog 数据。

解决方法：需要清理磁盘空间，然后重启 Pump。

## Pump 启动时报错 "fail to notify all living drainer"

报错原因：Pump 启动时需要通知所有 Online 状态的 Drainer，如果通知失败则会打印该错误日志。

解决方法：可以使用 [binlogctl 工具](/tidb-binlog/binlog-control.md)查看所有 Drainer 的状态是否有异常，保证 Online 状态的 Drainer 都在正常工作。如果某个 Drainer 的状态和实际运行情况不一致，则使用 binlogctl 修改状态，然后再重启 Pump。

## TiDB Binlog 同步中发现数据丢失

需要确认所有 TiDB 实例均开启了 TiDB Binlog，并且运行状态正常。如果集群版本大于 v3.0，可以使用 `curl {TiDB_IP}:{STATUS_PORT}/info/all` 命令确认所有 TiDB 实例上的 TiDB Binlog 状态。

## 当上游事务较大时，Pump 报错 `rpc error: code = ResourceExhausted desc = trying to send message larger than max (2191430008 vs. 2147483647)`

出现该错误的原因是 TiDB 发送给 Pump 的 gRPC message 超过限值。可以在启动 Pump 时通过指定 `max-message-size` 来调整 Pump 可接受 gRPC message 的最大大小。

## Drainer 输出 file 格式的增量数据，数据有什么清理机制吗？数据会被删除吗？

+ 在 v3.0.x 版本的 Drainer 中，file 格式的增量数据没有任何清理机制。
+ 在 v4.0.x 版本中，有基于时间的数据清理机制，详见 [Drainer 的 `retention-time` 配置项](https://github.com/pingcap/tidb-binlog/blob/v4.0.9/cmd/drainer/drainer.toml#L153)。
