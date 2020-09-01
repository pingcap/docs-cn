---
title: TiDB Binlog 常见错误修复
aliases: ['/docs-cn/v3.0/tidb-binlog/handle-tidb-binlog-errors/','/docs-cn/v3.0/reference/tidb-binlog/troubleshoot/error-handling/']
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

解决方法：可以使用 [binlogctl 工具](/tidb-binlog/maintain-tidb-binlog-cluster.md#binlogctl-工具)查看所有 Drainer 的状态是否有异常，保证 Online 状态的 Drainer 都在正常工作。如果某个 Drainer 的状态和实际运行情况不一致，则使用 binlogctl 修改状态，然后再重启 Pump。
