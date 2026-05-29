---
title: TiProxy API 概览
summary: 了解 TiProxy 的 API。
---

# TiProxy API 概览

[TiProxy](/tiproxy/tiproxy-overview.md) 是 PingCAP 的官方代理组件，它放置在客户端和 TiDB server 之间，为 TiDB 提供负载均衡、连接保持、服务发现等功能。

TiProxy 是可选组件，你也可以使用第三方的代理组件，或者直接连接到 TiDB server。

通过 TiProxy API，你可以对 TiProxy 集群执行以下操作：

- [获取 TiProxy 配置](/tiproxy/tiproxy-api.md#获取-tiproxy-的配置)
- [设置 TiProxy 配置](/tiproxy/tiproxy-api.md#设置-tiproxy-的配置)
- [获取 TiProxy 健康状况](/tiproxy/tiproxy-api.md#获取-tiproxy-的健康状况)
- [获取 TiProxy 监控数据](/tiproxy/tiproxy-api.md#获取-tiproxy-的监控数据)

关于各个 API 的请求参数、响应示例与使用说明，请参阅 [TiProxy API](/tiproxy/tiproxy-api.md)。