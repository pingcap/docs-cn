---
title: TiProxy 监控指标
summary: 了解 TiProxy 的监控指标。
---

# TiProxy 监控指标

本文介绍 TiProxy 的监控指标。

如果你使用 TiUP 部署 TiDB 集群，监控系统（Prometheus 和 Grafana）会同时部署。更多信息请参考[监控框架概览](/tidb-monitoring-framework.md)。

Grafana 仪表盘分为一系列子仪表盘，包括 Overview、PD、TiDB、TiKV、TiProxy 和 Node\_exporter，有很多指标可以帮助你诊断问题。每个仪表盘包含面板组和面板。

TiProxy 有四个面板组。这些面板上的指标表示 TiProxy 的当前状态。

- **TiProxy-Server**: TiProxy 实例信息。
- **TiProxy-Query-Summary**: SQL 查询指标，如 CPS。
- **TiProxy-Backend**: TiProxy 可能连接的 TiDB 节点的信息。
- **TiProxy-Balance**: 负载均衡指标。

## Server

- CPU Usage：每个 TiProxy 实例的 CPU 利用率
- Memory Usage：每个 TiProxy 实例的内存利用率
- Uptime：每个 TiProxy 实例自上次重启以来的运行时间
- Connection Count：每个 TiProxy 实例连接的客户端数量
- Create Connection OPM：每分钟在每个 TiProxy 实例上创建的连接数
- Disconnection OPM：每分钟每个原因的断开连接数。原因包括：
    - success：客户端正常断开连接。
    - client network break：客户端在断开连接前没有发送 `QUIT` 命令。这可能是由于网络问题或客户端关闭引起的。
    - client handshake fail：客户端握手失败。
    - auth fail：TiDB 拒绝访问。
    - SQL error：TiDB 返回其他 SQL 错误。
    - proxy shutdown：TiProxy 正在关闭。
    - malformed packet：TiProxy 无法解析 MySQL 数据包。
    - get backend fail：TiProxy 无法为连接找到可用的后端。
    - proxy error：其他 TiProxy 错误。
    - backend network break：无法从 TiDB 读取或写入。这可能是由于网络问题或 TiDB 服务器关闭引起的。
    - backend handshake fail：TiProxy 与 TiDB 服务器握手失败。
- Goroutine Count：每个 TiProxy 实例的 Goroutine 数量

## Query-Summary

- Duration：每个 TiProxy 实例的 SQL 语句执行的平均、P95、P99 时长。它包括 TiDB 服务器上 SQL 语句执行的时长，因此比 TiDB Grafana 面板上的时长高。
- P99 Duration By Instance：每个 TiProxy 实例的 P99 语句执行时长。
- P99 Duration By Backend：每个 TiDB 实例上执行的语句的 P99 语句执行时长。
- CPS by Instance：每个 TiProxy 实例的每秒命令数。
- CPS by Backend：每个 TiDB 实例的每秒命令数。
- CPS by CMD：按 SQL 命令类型分组的每秒命令数。
- Handshake Duration：客户端与 TiProxy 握手阶段的平均、P95、P99 时长。

## Balance

- Backend Connections：每个 TiDB 实例和每个 TiProxy 实例之间的连接数。例如，`10.24.31.1:6000 | 10.24.31.2:4000` 表示 TiProxy 实例 `10.24.31.1:6000` 和 TiDB 实例 `10.24.31.2:4000`。
- Session Migration OPM：每分钟发生的会话迁移数，记录从 TiDB 实例迁移到另一个 TiDB 实例的会话。例如，`succeed: 10.24.31.2:4000 => 10.24.31.3:4000` 表示从 TiDB 实例 `10.24.31.2:4000` 成功迁移到 TiDB 实例 `10.24.31.3:4000` 的会话数。
- Session Migration Duration：会话迁移的平均、P95、P99 时长。

## Backend

- Get Backend Duration：TiProxy 连接到 TiDB 实例的平均、P95、P99 时长。
- Ping Backend Duration：每个 TiProxy 实例和每个 TiProxy 实例之间的网络延迟。例如，`10.24.31.1:6000 | 10.24.31.2:4000` 表示 TiProxy 实例 `10.24.31.1:6000` 和 TiDB 实例 `10.24.31.2:4000` 之间的网络延迟。
- Health Check Cycle：每个 TiProxy 实例和所有 TiDB 实例之间的健康检查周期。例如，`10.24.31.1:6000` 表示 TiProxy 实例 `10.24.31.1:6000` 在所有 TiDB 实例上执行的最新健康检查的持续时间。如果此持续时间大于 3 秒，则 TiProxy 可能无法及时刷新后端 TiDB 列表。

## Traffic

- Bytes/Second from Backends：每个 TiDB 实例每秒向每个 TiProxy 实例发送的数据量，单位为字节。
- Packets/Second from Backends：每个 TiDB 实例每秒向每个 TiProxy 实例发送的 MySQL 数据包数量。
- Bytes/Second to Backends：每个 TiProxy 实例每秒向每个 TiDB 实例发送的数据量，单位为字节。
- Packets/Second to Backends：每个 TiProxy 实例每秒向每个 TiDB 实例发送的 MySQL 数据包数量。