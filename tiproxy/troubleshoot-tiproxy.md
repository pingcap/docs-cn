---
title: TiProxy 常见问题
summary: 介绍 TiProxy 的常见问题、原因及解决办法。
---

# TiProxy 常见问题

本文介绍了一些 TiProxy 常见问题、原因及解决办法。

## TiProxy 连接不上

可以通过以下步骤依次排查：

1. 检查[连接器版本](/tiproxy/tiproxy-overview.md#tiproxy-支持的连接器)是否支持。如果连接器不在列表中，请查看连接器是否支持[认证插件](https://dev.mysql.com/doc/refman/8.0/en/pluggable-authentication.html)。
2. 如果客户端报错 `No available TiDB instances, please make sure TiDB is available`，请检查是否有 TiDB server，且 TiDB server 的 SQL 端口和 HTTP 状态端口是否都可以正常连接。
3. 如果客户端报错 `Require TLS enabled on TiProxy when require-backend-tls=true`，请检查 TiProxy 是否正确配置了 TLS 证书。
4. 如果客户端报错 `Verify TiDB capability failed, please upgrade TiDB`，请检查 TiDB server 版本是否为 v6.5.0 及以上版本。
5. 如果客户端报错 `TiProxy fails to connect to TiDB, please make sure TiDB is available`，请检查 TiProxy 的节点是否能连接到 TiDB server。
6. 如果客户端报错 `Require TLS enabled on TiDB when require-backend-tls=true`，请检查 TiDB 是否配正确配置了 TLS 证书。
7. 如果客户端报错 `TiProxy fails to connect to TiDB, please make sure TiDB proxy-protocol is set correctly`，请检查是否 TiProxy 开启了 [proxy.proxy-protocol](/tiproxy/tiproxy-configuration.md#proxy-protocol) 而 TiDB server 没有开启[proxy-protocol](/tidb-configuration-file.md#proxy-protocol)。
8. 检查 TiProxy 是否配置了 [`max-connections`](/tiproxy/tiproxy-configuration.md#max-connections) 且 TiProxy 上的连接数超过了最大连接数限制。
9. 检查 TiProxy 日志，查看错误信息。

## TiProxy 没有迁移连接

可以通过以下步骤依次排查：

1. 是否没有满足 [TiProxy 的使用限制](/tiproxy/tiproxy-overview.md#使用限制)。可以结合 TiProxy 日志进一步确认。
2. 是否正确配置了 TiDB 的 [`security.session-token-signing-cert`](/tidb-configuration-file.md#session-token-signing-cert-从-v640-版本开始引入)，[`security.session-token-signing-key`](/tidb-configuration-file.md#session-token-signing-key-从-v640-版本开始引入)，和 [`graceful-wait-before-shutdown`](/tidb-configuration-file.md#graceful-wait-before-shutdown-从-v50-版本开始引入)。

## TiDB server 的 CPU 使用率不均

可以通过以下步骤依次排查：

1. 检查 TiDB server 之间的 CPU 使用率差异是否较大。TiProxy 并不保证所有 TiDB server 的 CPU 使用率接近，只有当 CPU 使用率差异较大影响查询延迟时才会进行[负载均衡](/tiproxy/tiproxy-load-balance.md)。
2. 如果有 TiDB server 的连接数逐渐降为 0，可能是受到了其他负载均衡策略的影响，你可以通过查看 Grafana 中的 [`Session Migration Reasons`](/tiproxy/tiproxy-grafana.md#balance) 检查是否有基于其他策略的迁移。
3. 检查 TiProxy 配置项 [`policy`](/tiproxy/tiproxy-configuration.md#policy) 的值是否为 `location`。采用地理位置优先的策略后，TiProxy 将不保证不同地理位置的 TiProxy 之间的 CPU 使用率均衡。
4. 检查 TiProxy 的版本，仅 v1.1.0 及以上版本支持[基于 CPU 的负载均衡](/tiproxy/tiproxy-load-balance.md#基于-cpu-的负载均衡)，较低版本基于最少连接数的策略负载均衡。
5. 如果以上情况均不符合，可能是迁移连接失败，请根据 [TiProxy 没有迁移连接](#tiproxy-没有迁移连接)排查。

## 延迟明显升高

可以通过以下步骤依次排查：

1. 通过 Grafana 监控指标检查 TiProxy 上显示的延迟。如果 TiProxy 上显示的延迟不高，则是客户端负载高或客户端与 TiProxy 之间的网络延迟高。
2. 通过 Grafana 监控指标检查 TiDB server 上显示的延迟。如果 TiDB server 上显示的延迟高，则通过 TiDB 的[延迟明显升高](/tidb-troubleshooting-map.md#2-延迟明显升高)的步骤排查。
3. 通过 Grafana 监控指标检查 [TiProxy 与 TiDB server 之间网络通信时间](/tiproxy/tiproxy-grafana.md#backend)。
4. 检查 TiProxy 的 CPU 使用率。如果 CPU 使用率超过 90%，则需要扩容 TiProxy。
