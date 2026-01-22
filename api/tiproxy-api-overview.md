---
title: TiProxy API Overview
summary: Learn about the API for TiProxy.
---

# TiProxy API Overview

[TiProxy](/tiproxy/tiproxy-overview.md) is the official proxy component of PingCAP. It is placed between the client and the TiDB server to provide load balancing, connection persistence, service discovery, and other features for TiDB.

TiProxy is an optional component. You can also use a third-party proxy component or connect directly to the TiDB server without using a proxy.

You can use TiProxy APIs to perform the following operations on the TiProxy cluster:

- [Get TiProxy configuration](/tiproxy/tiproxy-api.md#get-tiproxy-configuration)
- [Set TiProxy configuration](/tiproxy/tiproxy-api.md#set-tiproxy-configuration)
- [Get TiProxy health status](/tiproxy/tiproxy-api.md#get-tiproxy-health-status)
- [Get TiProxy monitoring data](/tiproxy/tiproxy-api.md#get-tiproxy-monitoring-data)

For more information about each API, including request parameters, response examples, and usage instructions, see [TiProxy API](/tiproxy/tiproxy-api.md).