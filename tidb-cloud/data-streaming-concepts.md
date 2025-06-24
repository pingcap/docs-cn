---
title: 数据流
summary: 了解 TiDB Cloud 的数据流概念。
---

# 数据流

TiDB Cloud 允许你将数据变更从 TiDB 集群流式传输到其他系统，如 Kafka、MySQL 和对象存储。

目前，TiDB Cloud 支持将数据流式传输到 Apache Kafka、MySQL、TiDB Cloud 和云存储。

## Changefeed

TiDB Cloud changefeed 是一个持续的数据流，帮助你将数据变更从 TiDB Cloud 复制到其他数据服务。

在 TiDB Cloud 控制台的 **Changefeed** 页面，你可以创建 changefeed、查看现有 changefeed 列表，以及操作现有的 changefeed（如扩展、暂停、恢复、编辑和删除 changefeed）。

默认情况下，复制仅包括增量数据变更。如果需要复制现有数据，必须在启动 changefeed 之前手动将其导出并加载到目标系统中。

在 TiDB Cloud 中，可以通过定义表过滤器（指定要复制的表）和事件过滤器（包含或排除特定类型的事件，如 INSERT 或 DELETE）来定制复制。

更多信息，请参见 [Changefeed](/tidb-cloud/changefeed-overview.md)。
