---
title: TiCDC API 概览
summary: 了解 TiCDC 的 API。
---

# TiCDC API 概览

[TiCDC](/ticdc/ticdc-overview.md) 是一款 TiDB 增量数据同步工具，通过拉取上游 TiKV 的数据变更日志，TiCDC 可以将数据解析为有序的行级变更数据输出到下游。

TiCDC 提供以下两个版本的 API，用于查询与运维 TiCDC 集群：

- [TiCDC OpenAPI v1](/ticdc/ticdc-open-api.md)
- [TiCDC OpenAPI v2](/ticdc/ticdc-open-api-v2.md)

> **注意：**
>
> TiCDC OpenAPI v1 将在未来版本中被删除。推荐使用 TiCDC OpenAPI v2。

关于各个 API 的请求参数、响应示例与使用说明，请参阅 [TiCDC OpenAPI v1](/ticdc/ticdc-open-api.md) 与 [TiCDC OpenAPI v2](/ticdc/ticdc-open-api-v2.md)。
