---
title: 提高 TiDB Dashboard 安全性
aliases: ['/docs-cn/dev/dashboard/dashboard-ops-security/']
---

# 提高 TiDB Dashboard 安全性

尽管访问 TiDB Dashboard 需要登录，但它被设计为默认供可信的用户实体访问。当你希望将 TiDB Dashboard 提供给外部网络用户或不可信用户访问时，需要注意采取以下措施以避免安全漏洞。

## 为 TiDB `root` 用户设置强密码

TiDB Dashboard 的账号体系与 TiDB SQL 用户一致。默认部署情况下，TiDB 的 `root` 用户没有密码，因而访问 TiDB Dashboard 也不需要密码验证。这将会给恶意访问者极大的集群权限，包括执行特权 SQL 等。

建议的措施：

- 为 TiDB `root` 用户设置一个强密码。请参见 [TiDB 用户账户管理](/user-account-management.md)了解详情。

## 使用防火墙阻止不可信访问

TiDB Dashboard 通过 PD Client 端口提供服务，默认为 <http://IP:2379/dashboard/>。尽管 TiDB Dashboard 需要验证身份，但 PD Client 端口上承载的其他 PD 内部特权接口不需要验证身份，且能进行特权操作，例如 <http://IP:2379/pd/api/v1/members>。因此，将 PD Client 端口直接暴露给外部网络具有极大的风险。

建议的措施：

1. 使用防火墙禁止组件外部网络或不可信网络访问**任何** PD 组件的 Client 端口。

   注意，TiDB、TiKV 等组件需要通过 PD Client 端口与 PD 组件进行通信，因此请勿对组件内部网络阻止访问，这将导致集群不可用。

2. 参见[通过反向代理使用 TiDB Dashboard](/dashboard/dashboard-ops-reverse-proxy.md) 了解如何配置反向代理将 TiDB Dashboard 服务在另一个端口上安全地提供给外部网络。

### 如何在多 PD 实例部署时开放 TiDB Dashboard 端口访问

> **警告：**
>
> 本章节描述了一个不安全的访问方案，仅供测试环境使用。在生产环境中，不要使用本方案。请参见本文的其余章节。

在测试环境中，您可能需要配置防火墙开放 TiDB Dashboard 端口供外部访问。

当部署了多个 PD 实例时，其中仅有一个 PD 实例会真正运行 TiDB Dashboard，访问其他 PD 实例时会发生浏览器重定向，因此需要确保防火墙配置了正确的 IP 地址。关于该机制的详情，可参阅 [TiDB Dashboard 多 PD 实例部署](/dashboard/dashboard-ops-deploy.md#多-pd-实例部署)章节。

使用 TiUP 部署工具时，可使用以下命令查看实际运行 TiDB Dashboard 的 PD 实例地址（将 `CLUSTER_NAME` 替换为集群名称）：

```bash
tiup cluster display CLUSTER_NAME --dashboard
```

输出即为实际 TiDB Dashboard 地址。

> **注意：**
>
> 该功能在 TiUP Cluster v1.0.3 或更高版本部署工具中提供。
>
> <details>
> <summary>升级 TiUP Cluster 步骤</summary>
>
> ```shell
> tiup update --self
> tiup update cluster --force
> ```
>
> </details>

以下是一个样例输出：

```
http://192.168.0.123:2379/dashboard/
```

在这个样例中，需要为防火墙配置开放 IP `192.168.0.123` 的 `2379` 端口入站访问，并通过 <http://192.168.0.123:2379/dashboard/> 访问 TiDB Dashboard。

## 反向代理仅代理 TiDB Dashboard

如前文所述，PD Client 端口下提供的服务不仅有 TiDB Dashboard（位于 <http://IP:2379/dashboard/>），还有其他 PD 内部特权接口（如 <http://IP:2379/pd/api/v1/members>）。因此，使用反向代理将 TiDB Dashboard 提供给外部网络时，应当确保仅提供 `/dashboard` 前缀下的服务，而非该端口下所有服务，避免外部网络能通过反向代理访问到 PD 内部特权接口。

建议的措施：

- 参见[通过反向代理使用 TiDB Dashboard](/dashboard/dashboard-ops-reverse-proxy.md) 了解安全且推荐的反向代理配置。

## 为反向代理开启 TLS

为了进一步加强传输层安全性，可以为反向代理开启 TLS，甚至可以引入 mTLS 实现访问用户的证书验证。

请参阅 [NGINX 文档](http://nginx.org/en/docs/http/configuring_https_servers.html)或 [HAProxy 文档](https://www.haproxy.com/blog/haproxy-ssl-termination/)了解如何为它们开启 TLS。

## 其他建议的安全措施

- [为 TiDB 组件间通信开启加密传输](/enable-tls-between-components.md)
- [为 TiDB 客户端服务端间通信开启加密传输](/enable-tls-between-clients-and-servers.md)
