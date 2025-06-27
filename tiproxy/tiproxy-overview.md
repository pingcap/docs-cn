---
title: TiProxy 简介
summary: 介绍 TiProxy 的主要功能、安装与使用方法。
---

# TiProxy 简介

TiProxy 是 PingCAP 的官方代理组件，它放置在客户端和 TiDB server 之间，为 TiDB 提供负载均衡、连接保持、服务发现等功能。

TiProxy 是可选组件，你也可以使用第三方的代理组件，或者直接连接到 TiDB server。

TiProxy 示意图如下：

<img src="https://docs-download.pingcap.com/media/images/docs-cn/tiproxy/tiproxy-architecture.png" alt="TiProxy 架构" width="500" />

## 主要功能

TiProxy 提供连接迁移、故障转移、服务发现和一键部署的功能。

### 连接迁移

TiProxy 在保持客户端连接不变的情况下，能将一台 TiDB server 上的连接迁移到另一台 TiDB server。

如下图所示，原先客户端通过 TiProxy 连接到 TiDB 1 上，连接迁移之后，客户端实际连接到 TiDB 2 上。在 TiDB 1 即将下线或 TiDB 1 上的连接数比 TiDB 2 上的连接数超过设定阈值时，会触发连接迁移。连接迁移对客户端无感知。

<img src="https://docs-download.pingcap.com/media/images/docs-cn/tiproxy/tiproxy-session-migration.png" alt="TiProxy 连接迁移" width="400" />

连接迁移通常发生在以下场景：

- 当 TiDB server 进行缩容、滚动升级、滚动重启操作时，TiProxy 能把连接从即将下线的 TiDB server 迁移到其他 TiDB server 上，从而保持客户端连接不断开。
- 当 TiDB server 进行扩容操作时，TiProxy 能将已有的部分连接迁移到新的 TiDB server 上，从而实现了实时的负载均衡，无需客户端重置连接池。

### 故障转移

当一台 TiDB server 存在 Out of Memory (OOM) 风险、连接 PD 或 TiKV 失败时，TiProxy 自动感知故障，并将连接迁移到其他 TiDB server 上，从而保持客户端连接不断开。

### 服务发现

当 TiDB server 进行扩容、缩容操作时，如果使用普通负载均衡器，你需要手动更新 TiDB server 列表，而 TiProxy 能自动发现 TiDB server 列表，无需人工介入。

### 一键部署

TiProxy 集成到了 [TiUP](https://github.com/pingcap/tiup)、[TiDB Operator](https://github.com/pingcap/tidb-operator)、[TiDB Dashboard](/dashboard/dashboard-intro.md) 和 [Grafana](/tiproxy/tiproxy-grafana.md) 中，且内置虚拟 IP 管理，降低了部署和运维成本。

## 使用场景

TiProxy 适用于以下场景：

- 连接保持：当 TiDB 缩容、滚动升级、滚动重启操作时，客户端连接会断开，导致报错。如果客户端没有幂等的错误重试机制，则需要人工手动检查错误并修复，这大大增加了人力成本。TiProxy 能保持客户端连接，因此可以避免客户端报错。
- 频繁扩缩容：应用的负载可能周期性地变化，为了节省成本，你可以将 TiDB 部署到云上，并根据负载自动地扩缩容 TiDB server。然而，缩容可能导致客户端断连，而扩容不能及时地实现负载均衡。通过迁移连接功能，TiProxy 能保持客户端连接并实现负载均衡。
- CPU 负载不均：后台任务占用较多 CPU 资源，或者不同连接上的工作负载差异较大，导致 CPU 负载不均时，TiProxy 能根据 CPU 使用率迁移连接，实现负载均衡。请参阅[基于 CPU 的负载均衡](/tiproxy/tiproxy-load-balance.md#基于-cpu-的负载均衡)。
- TiDB server OOM：当出现 Runaway Query 导致 TiDB server OOM 时，TiProxy 能提前感知到 TiDB server OOM 的风险，并将其他正常连接迁移到其他 TiDB server 上，从而保持客户端连接不断开。请参阅[基于内存的负载均衡](/tiproxy/tiproxy-load-balance.md#基于内存的负载均衡)。

TiProxy 不适用于以下场景：

- 对性能敏感：TiProxy 的性能低于 HAProxy 等负载均衡器，因此使用 TiProxy 需要预留更多 CPU 资源。请参阅 [TiProxy 性能测试报告](/tiproxy/tiproxy-performance-test.md)。
- 对成本敏感：如果 TiDB 集群使用了硬件负载均衡、虚拟 IP 或 Kubernetes 自带的负载均衡器，此时增加 TiProxy 组件会增加成本。另外，如果在云上跨可用区部署 TiDB 集群，增加 TiProxy 组件也会增加跨可用区的流量费用。
- TiDB server 意外下线时的故障转移：只有当 TiDB server 在计划内的下线或重启操作时，TiProxy 才能保持连接。如果 TiDB server 意外下线，则连接仍然会断开。

当符合 TiProxy 的使用场景时，推荐使用 TiProxy。当对性能敏感时，推荐使用 HAProxy 或其他代理。

## 安装和使用

本节介绍使用 TiUP 部署和变更 TiProxy 的步骤。你可以在[创建新集群时部署 TiProxy](#创建带有-tiproxy-的集群)，也可以通过扩容的方式[为已有集群启用 TiProxy](#为已有集群启用-tiproxy)。

> **注意：**
>
> 请确保 TiUP 为 v1.16.1 或之后版本。

其他部署方式，请参考以下文档：

- 使用 TiDB Operator 部署 TiProxy，请参见 [TiDB Operator](https://docs.pingcap.com/zh/tidb-in-kubernetes/stable/deploy-tiproxy) 文档。
- 使用 TiUP 本地快速部署 TiProxy，请参见[部署 TiProxy](/tiup/tiup-playground.md#部署-tiproxy)。

### 创建带有 TiProxy 的集群

以下步骤介绍如何在创建新集群时部署 TiProxy。

1. 配置 TiDB 实例。

    使用 TiProxy 时，需要为 TiDB 配置 [`graceful-wait-before-shutdown`](/tidb-configuration-file.md#graceful-wait-before-shutdown-从-v50-版本开始引入)。该值应比应用程序最长事务的持续时间大 10 秒以上，以避免 TiDB server 下线时客户端连接中断。你可以通过 [TiDB 监控面板的 Transaction 指标](/grafana-tidb-dashboard.md#transaction) 查看事务持续时间。更多信息，请参阅[使用限制](#使用限制)。

    配置示例：

    ```yaml
    server_configs:
      tidb:
        graceful-wait-before-shutdown: 30
    ```

2. 配置 TiProxy 实例。

    为了保证 TiProxy 的高可用，建议部署至少 2 个 TiProxy 实例，并配置虚拟 IP [`ha.virtual-ip`](/tiproxy/tiproxy-configuration.md#virtual-ip) 和 [`ha.interface`](/tiproxy/tiproxy-configuration.md#interface)，以便流量能够路由到可用的 TiProxy 实例。

    注意事项：

    - 要根据负载类型和最大 QPS 选择 TiProxy 的机型和实例数。更多详情，请参阅 [TiProxy 性能测试报告](/tiproxy/tiproxy-performance-test.md)。
    - 由于 TiProxy 实例通常少于 TiDB server 实例，TiProxy 的网络带宽更容易成为瓶颈。例如，在 AWS 上，同系列 EC2 的基准网络带宽与 CPU 核数并不成正比。当网络带宽成为瓶颈时，可以把 TiProxy 实例拆分为更多更小规格的实例，从而提高 QPS。更多详情，请参阅[网络规格](https://docs.aws.amazon.com/zh_cn/ec2/latest/instancetypes/co.html#co_network)。
    - 建议在拓扑配置中指定 TiProxy 的版本号。这样在执行 [`tiup cluster upgrade`](/tiup/tiup-component-cluster-upgrade.md) 升级 TiDB 集群时，可以避免 TiProxy 被一并升级，从而避免因 TiProxy 升级导致客户端连接断开。

    关于 TiProxy 的配置模板，请参见 [TiProxy 配置模板](/tiproxy/tiproxy-deployment-topology.md)。

    关于 TiDB 集群拓扑文件中的配置项说明，请参见[通过 TiUP 部署 TiDB 集群的拓扑文件配置](/tiup/tiup-cluster-topology-reference.md)。

    配置示例：

    ```yaml
    component_versions:
      tiproxy: "v1.2.0"
    server_configs:
      tiproxy:
        ha.virtual-ip: "10.0.1.10/24"
        ha.interface: "eth0"
    tiproxy_servers:
      - host: 10.0.1.11
        port: 6000
        status_port: 3080
      - host: 10.0.1.12
        port: 6000
        status_port: 3080
    ```

3. 启动集群。

    使用 TiUP 启动集群的方式，请参阅 [TiUP](/tiup/tiup-documentation-guide.md) 文档。

4. 连接到 TiProxy。

    集群部署完成后，会同时暴露 TiDB server 端口和 TiProxy 端口。客户端应当连接到 TiProxy 的端口，而不是直接连接 TiDB server。

### 为已有集群启用 TiProxy

对于未启用 TiProxy 的集群，可以通过扩容的方式启用 TiProxy。

1. 配置 TiProxy 实例。

    在单独的拓扑文件中配置 TiProxy，例如 `tiproxy.toml`：

    ```yaml
    component_versions:
      tiproxy: "v1.2.0"
    server_configs:
      tiproxy:
        ha.virtual-ip: "10.0.1.10/24"
        ha.interface: "eth0"
    tiproxy_servers:
      - host: 10.0.1.11
        deploy_dir: "/tiproxy-deploy"
        port: 6000
        status_port: 3080
      - host: 10.0.1.12
        deploy_dir: "/tiproxy-deploy"
        port: 6000
        status_port: 3080
    ```

2. 扩容 TiProxy。

    使用 [`tiup cluster scale-out`](/tiup/tiup-component-cluster-scale-out.md) 命令扩容 TiProxy 实例，例如：

    ```shell
    tiup cluster scale-out <cluster-name> tiproxy.toml
    ```

    扩容 TiProxy 时，TiUP 会自动为 TiDB 配置自签名证书 [`security.session-token-signing-cert`](/tidb-configuration-file.md#session-token-signing-cert-从-v640-版本开始引入) 和 [`security.session-token-signing-key`](/tidb-configuration-file.md#session-token-signing-key-从-v640-版本开始引入)，该证书用于迁移连接。

3. 修改 TiDB 配置。

    使用 TiProxy 时，需要为 TiDB 配置 [`graceful-wait-before-shutdown`](/tidb-configuration-file.md#graceful-wait-before-shutdown-从-v50-版本开始引入)。该值应比应用程序最长事务的持续时间大 10 秒以上，以避免 TiDB server 下线时客户端连接中断。你可以通过 [TiDB 监控面板的 Transaction 指标](/grafana-tidb-dashboard.md#transaction) 查看事务持续时间。更多信息，请参阅[使用限制](#使用限制)。

    配置示例：

    ```yaml
    server_configs:
      tidb:
        graceful-wait-before-shutdown: 30
    ```

4. 重新加载 TiDB 配置。

    由于 TiDB 配置了自签名证书和 `graceful-wait-before-shutdown`，需要使用 [`tiup cluster reload`](/tiup/tiup-component-cluster-reload.md) 命令重新加载配置使它们生效。注意，重新加载配置后，TiDB 会滚动重启，此时客户端连接会断开。

    ```shell
    tiup cluster reload <cluster-name> -R tidb
    ```

5. 连接到 TiProxy。

    启用 TiProxy 后，客户端应连接 TiProxy 端口，而不是 TiDB server 端口。

### 更改 TiProxy 配置

为了保证连接保持功能的有效性，TiProxy 不应随意重启。因此，TiProxy 的大多数配置项支持在线变更。支持在线变更的配置列表请参阅 [TiProxy 配置](/tiproxy/tiproxy-configuration.md)。

使用 TiUP 更改 TiProxy 配置时，如果要更改的配置项支持在线变更，应当带上 [`--skip-restart`](/tiup/tiup-component-cluster-reload.md#--skip-restart) 选项，避免重启 TiProxy。

### 升级 TiProxy

部署 TiProxy 时建议指定 TiProxy 的版本，使升级 TiDB 集群时不会升级 TiProxy。

如果确实要升级 TiProxy 的版本，需加上 [`--tiproxy-version`](/tiup/tiup-component-cluster-upgrade.md#--tiproxy-version) 指定 TiProxy 的版本：

```shell
tiup cluster upgrade <cluster-name> <version> --tiproxy-version <tiproxy-version>
```

> **注意：**
>
> 该命令将会同时升级 TiDB 集群。即使 TiDB 版本没有变化，也会重启 TiDB 集群。

### 重启 TiDB 集群

使用 [`tiup cluster restart`](/tiup/tiup-component-cluster-restart.md) 重启 TiDB 集群时，TiDB server 不是滚动重启，会导致连接断开，请尽量避免使用。

使用 [`tiup cluster upgrade`](/tiup/tiup-component-cluster-upgrade.md) 升级集群和 [`tiup cluster reload`](/tiup/tiup-component-cluster-reload.md) 重新加载配置时，TiDB server 是滚动重启的，因此连接不会断开。

## TiProxy 与其他组件的兼容性

- TiProxy 仅支持 TiDB v6.5.0 及以上版本。
- TiProxy 的 TLS 连接与 TiDB 有不兼容的功能，请参阅[安全](#安全)。
- TiDB Dashboard 和 Grafana 从 v7.6.0 开始支持 TiProxy。
- TiUP 从 v1.14.1 开始支持 TiProxy，TiDB Operator 从 v1.5.1 开始支持 TiProxy。
- 由于 TiProxy 的状态端口提供的接口与 TiDB server 不同，使用 [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md) 导入数据时，目标数据库应当填写 TiDB server 的地址，不能是 TiProxy 的地址。

## 安全

TiProxy 提供了 TLS 连接。客户端与 TiProxy 之间的 TLS 连接按照如下规则开启：

- 当 TiProxy 的 [`security.server-tls`](/tiproxy/tiproxy-configuration.md#server-tls) 配置为不使用 TLS 连接时，无论客户端是否开启 TLS 连接，客户端与 TiProxy 之间都不开启 TLS 连接。
- 当 TiProxy 的 [`security.server-tls`](/tiproxy/tiproxy-configuration.md#server-tls) 配置为使用 TLS 连接时，仅当客户端开启 TLS 连接时，客户端与 TiProxy 才开启 TLS 连接。

TiProxy 与 TiDB server 之间的 TLS 连接按照如下规则开启：

- 当 TiProxy 的 [`security.require-backend-tls`](/tiproxy/tiproxy-configuration.md#require-backend-tls) 设置为 `true` 时，无论客户端与 TiProxy 之间是否开启了 TLS 连接，TiProxy 和 TiDB server 之间都会开启 TLS 连接。如果 TiProxy 的 [`security.sql-tls`](/tiproxy/tiproxy-configuration.md#sql-tls) 配置为不使用 TLS 或 TiDB server 没有配置 TLS 证书，则客户端报错。
- 当 TiProxy 的 [`security.require-backend-tls`](/tiproxy/tiproxy-configuration.md#require-backend-tls) 设置为 `false`，TiProxy 的 [`security.sql-tls`](/tiproxy/tiproxy-configuration.md#sql-tls) 配置了 TLS 且 TiDB server 配置了 TLS 证书时，仅当客户端与 TiProxy 之间开启了 TLS 时，TiProxy 与 TiDB server 之间才开启 TLS 连接。
- 当 TiProxy 的 [`security.require-backend-tls`](/tiproxy/tiproxy-configuration.md#require-backend-tls) 设置为 `false`，TiProxy 的 [`security.sql-tls`](/tiproxy/tiproxy-configuration.md#sql-tls) 没有配置 TLS 或 TiDB server 没有配置 TLS 证书时，TiProxy 与 TiDB server 之间不开启 TLS 连接。

TiProxy 的以下行为与 TiDB 不兼容：

- 执行 `STATUS` 和 `SHOW STATUS` 语句显示的 TLS 信息可能不一致。`STATUS` 语句显示的是客户端到 TiProxy 之间的 TLS 信息，而 `SHOW STATUS` 语句显示的是 TiProxy 与 TiDB server 之间的 TLS 信息。
- TiProxy 不支持[基于证书鉴权的登录方式](/certificate-authentication.md)，否则客户端可能会登录失败，因为客户端与 TiProxy 之间的 TLS 证书和 TiProxy 与 TiDB server 之间的 TLS 证书是不同的，TiDB server 根据 TiProxy 上的 TLS 证书校验。

## 使用限制

以下情况下，TiProxy 不能保持客户端连接：

- TiDB 意外下线。TiProxy 仅支持 TiDB server 在计划内的下线或重启时保持客户端连接，不支持 TiDB server 的故障转移。
- TiProxy 进行缩容、升级、重启等下线操作。一旦 TiProxy 下线，客户端连接也会断开。
- TiDB 主动断开连接。例如会话超过 `wait_timeout` 的时间没有发送请求时，TiDB 会主动断开连接，此时 TiProxy 也会断开客户端连接。

在以下情况下，TiProxy 将无法完成连接迁移，会导致客户端连接中断或负载均衡失效：

- 长时间运行的单条语句或单个事务：其执行时间超过了 TiDB Server 配置的 [`graceful-wait-before-shutdown`](/tidb-configuration-file.md#graceful-wait-before-shutdown-从-v50-版本开始引入) 的值减去 10 秒的时间窗口。
- 使用游标且未及时完成：会话使用游标读取数据，但超过 TiDB Server 配置的 [`graceful-wait-before-shutdown`](/tidb-configuration-file.md#graceful-wait-before-shutdown-从-v50-版本开始引入) 的值减去 10 秒后，仍未完成数据读取或关闭游标。
- 会话创建了[本地临时表](/temporary-tables.md#本地临时表)。
- 会话持有了[用户级锁](/functions-and-operators/locking-functions.md)。
- 会话持有了[表锁](/sql-statements/sql-statement-lock-tables-and-unlock-tables.md)。
- 会话创建了[预处理语句](/develop/dev-guide-prepared-statement.md)，且该预处理语句失效，例如创建预处理语句之后相关的表被删除。
- 会话创建了会话级的[执行计划绑定](/sql-plan-management.md#执行计划绑定-sql-binding)，且该执行计划绑定失效，例如创建执行计划绑定之后相关的表被删除。
- 创建会话后，该会话使用的用户被删除或用户名被更改。

## TiProxy 支持的连接器

TiProxy 要求客户端使用的连接器支持[认证插件](https://dev.mysql.com/doc/refman/8.0/en/pluggable-authentication.html)，否则可能会连接失败。

以下列举了部分支持的连接器：

| 编程语言       | 连接器                     | 支持的最低版本   |
|------------|-------------------------|-----------|
| Java       | MySQL Connector/J       | 5.1.19    |
| C          | libmysqlclient          | 5.5.7     |
| Go         | Go SQL Driver           | 1.4.0     |
| JavaScript | MySQL Connector/Node.js | 1.0.2     |
| JavaScript | mysqljs/mysql           | 2.15.0    |
| JavaScript | node-mysql2             | 1.0.0-rc-6 |
| PHP        | mysqlnd                 | 5.4       |
| Python     | MySQL Connector/Python  | 1.0.7     |
| Python     | PyMySQL                 | 0.7       |

注意，某些连接器调用公共的库连接数据库，这些连接器没有在表中列出，请在上述列表中查询对应的库所需的版本。例如，MySQL/Ruby 使用 libmysqlclient 连接数据库，因此要求它使用的 libmysqlclient 为 5.5.7 及以上版本。

## 资源

- [TiProxy 版本发布历史](https://github.com/pingcap/tiproxy/releases)
- [TiProxy Issues](https://github.com/pingcap/tiproxy/issues)：TiProxy GitHub Issues 列表
