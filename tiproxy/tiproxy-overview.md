---
title: TiProxy 简介
summary: 介绍 TiProxy 的主要功能、安装与使用方法。
---

# TiProxy 简介

TiProxy 是 PingCAP 的官方代理组件，它放置在客户端和 TiDB server 之间，为 TiDB 提供负载均衡、连接保持、服务发现等功能。

TiProxy 是可选组件，你也可以使用第三方的代理组件，或者直接连接到 TiDB server。

TiProxy 示意图如下：

<img src="https://download.pingcap.com/images/docs-cn/tiproxy/tiproxy-architecture.png" alt="TiProxy 架构" width="500" />

## 主要功能

TiProxy 提供连接迁移、故障转移、服务发现和一键部署的功能。

### 连接迁移

TiProxy 在保持客户端连接不变的情况下，能将一台 TiDB server 上的连接迁移到另一台 TiDB server。

如下图所示，原先客户端通过 TiProxy 连接到 TiDB 1 上，连接迁移之后，客户端实际连接到 TiDB 2 上。在 TiDB 1 即将下线或 TiDB 1 上的连接数比 TiDB 2 上的连接数超过设定阈值时，会触发连接迁移。连接迁移对客户端无感知。

<img src="https://download.pingcap.com/images/docs-cn/tiproxy/tiproxy-session-migration.png" alt="TiProxy 连接迁移" width="400" />

连接迁移通常发生在以下场景：

- 当 TiDB server 进行缩容、滚动升级、滚动重启操作时，TiProxy 能把连接从即将下线的 TiDB server 迁移到其他 TiDB server 上，从而保持客户端连接不断开。
- 当 TiDB server 进行扩容操作时，TiProxy 能将已有的部分连接迁移到新的 TiDB server 上，从而实现了实时的负载均衡，无需客户端重置连接池。

### 故障转移

当一台 TiDB server 存在 Out of Memory (OOM) 风险、连接 PD 或 TiKV 失败时，TiProxy 自动感知故障，并将连接迁移到其他 TiDB server 上，从而保持客户端连接不断开。

### 服务发现

当 TiDB server 进行扩容、缩容操作时，如果使用普通负载均衡器，你需要手动更新 TiDB server 列表，而 TiProxy 能自动发现 TiDB server 列表，无需人工介入。

### 一键部署

TiProxy 集成到了 [TiUP](https://github.com/pingcap/tiup)、[TiDB Operator](https://github.com/pingcap/tidb-operator)、[TiDB Dashboard](/dashboard/dashboard-intro.md) 和 [Grafana](/tiproxy/tiproxy-grafana.md) 中，降低了部署和运维成本。

## 使用场景

TiProxy 适用于以下场景：

- 连接保持：当 TiDB 缩容、滚动升级、滚动重启操作时，客户端连接会断开，导致报错。如果客户端没有幂等的错误重试机制，则需要人工手动检查错误并修复，这大大增加了人力成本。TiProxy 能保持客户端连接，因此可以避免客户端报错。
- 频繁扩缩容：应用的负载可能周期性地变化，为了节省成本，你可以将 TiDB 部署到云上，并根据负载自动地扩缩容 TiDB server。然而，缩容可能导致客户端断连，而扩容不能及时地实现负载均衡。通过迁移连接功能，TiProxy 能保持客户端连接并实现负载均衡。
- CPU 负载不均：后台任务占用较多 CPU 资源，或者不同连接上的工作负载差异较大，导致 CPU 负载不均时，TiProxy 能根据 CPU 使用率迁移连接，实现负载均衡。请参阅[基于 CPU 的负载均衡](/tiproxy/tiproxy-load-balance.md#基于-cpu-的负载均衡)。
- TiDB server OOM：当出现 Runaway Query 导致 TiDB server OOM 时，TiProxy 能提前感知到 TiDB server OOM 的风险，并将其他正常连接迁移到其他 TiDB server 上，从而保持客户端连接不断开。请参阅[基于内存的负载均衡](/tiproxy/tiproxy-load-balance.md#基于内存的负载均衡)。

TiProxy 不适用于以下场景：

- 对性能敏感：TiProxy 的性能低于 HAProxy 等负载均衡器，因此使用 TiProxy 会降低 QPS。请参阅 [TiProxy 性能测试报告](/tiproxy/tiproxy-performance-test.md)。
- 对成本敏感：如果 TiDB 集群使用了硬件负载均衡、虚拟 IP 或 Kubernetes 自带的负载均衡器，此时增加 TiProxy 组件会增加成本。另外，如果在云上跨可用区部署 TiDB 集群，增加 TiProxy 组件也会增加跨可用区的流量费用。
- TiDB server 意外下线时的故障转移：只有当 TiDB server 在计划内的下线或重启操作时，TiProxy 才能保持连接。如果 TiDB server 意外下线，则连接仍然会断开。

当符合 TiProxy 的使用场景时，推荐使用 TiProxy。当对性能敏感时，推荐使用 HAProxy 或其他代理。

## 安装和使用

本节介绍使用 TiUP 部署和变更 TiProxy 的步骤。使用 TiDB Operator 部署的方式请参阅 [TiDB Operator](https://docs.pingcap.com/zh/tidb-in-kubernetes/stable/deploy-tiproxy) 文档。

### 部署 TiProxy

1. 对于 TiUP v1.15.0 之前的版本，需要手动生成自签名证书。

    为 TiDB 实例生成自签名证书，并把该证书放置到所有 TiDB 实例上，确保所有 TiDB 实例上有完全相同的证书。生成步骤请参阅[生成自签名证书](/generate-self-signed-certificates.md)。

2. 配置 TiDB 实例。

    使用 TiProxy 时，还需要给 TiDB 实例做如下配置：

    - 对于 TiUP v1.15.0 之前的版本，将 TiDB 实例的 [`security.session-token-signing-cert`](/tidb-configuration-file.md#session-token-signing-cert-从-v640-版本开始引入) 和 [`security.session-token-signing-key`](/tidb-configuration-file.md#session-token-signing-key-从-v640-版本开始引入) 配置为上述证书的路径，否则连接不能迁移。
    - 配置 TiDB 实例的 [`graceful-wait-before-shutdown`](/tidb-configuration-file.md#graceful-wait-before-shutdown-从-v50-版本开始引入)，它的值要大于应用程序最长的事务的持续时间，否则 TiDB server 下线时客户端可能断连。你可以通过 [TiDB 监控面板的 Transaction 指标](/grafana-tidb-dashboard.md#transaction)查看事务的持续时间。更多信息，请参阅[使用限制](#使用限制)。

    配置示例：

    ```yaml
    server_configs:
      tidb:
        security.session-token-signing-cert: "/var/sess/cert.pem"
        security.session-token-signing-key: "/var/sess/key.pem"
        security.ssl-ca: "/var/ssl/ca.pem"
        security.ssl-cert: "/var/ssl/cert.pem"
        security.ssl-key: "/var/ssl/key.pem"
        graceful-wait-before-shutdown: 15
    ```

3. 配置 TiProxy 实例。

    为了保证 TiProxy 的高可用，建议部署至少 2 台 TiProxy 实例。可以通过硬件负载均衡使流量分发到各 TiProxy 实例上，或配置虚拟 IP 使流量路由到可用的 TiProxy 实例上。

    选择 TiProxy 的机型和实例数时需要考虑以下因素：

    - 要考虑负载类型和最大 QPS，请参阅 [TiProxy 性能测试报告](/tiproxy/tiproxy-performance-test.md)。
    - 由于 TiProxy 的实例数比 TiDB server 少，TiProxy 的网络带宽相比 TiDB server 更可能成为瓶颈，因此还需要考虑网络带宽。例如，AWS 相同系列的 EC2 的基准网络带宽与 CPU 核数是不成正比的，请参阅[计算实例网络性能](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/compute-optimized-instances.html#compute-network-performance)。这种情况下，当网络带宽成为瓶颈时，把 TiProxy 实例拆分为更多更小规格的实例能提高 QPS。

    建议在拓扑配置里指定 TiProxy 的版本号，这样通过 [`tiup cluster upgrade`](/tiup/tiup-component-cluster-upgrade.md) 升级 TiDB 集群时不会升级 TiProxy，否则升级 TiProxy 会导致客户端连接断开。

    如需配置 TiProxy 配置项，请参阅 [TiProxy 配置](/tiproxy/tiproxy-configuration.md)。

    配置示例：

    ```yaml
    component_versions:
      tiproxy: "v1.0.0"
    server_configs:
      tiproxy:
        security.server-tls.ca: "/var/ssl/ca.pem"
        security.server-tls.cert: "/var/ssl/cert.pem"
        security.server-tls.key: "/var/ssl/key.pem"
    ```

4. 启动集群。

    使用 TiUP 启动集群的方式请参阅 [TiUP](/tiup/tiup-documentation-guide.md) 文档。

5. 连接到 TiProxy。

    部署集群之后，集群同时暴露了 TiDB server 的端口和 TiProxy 端口。客户端应当连接到 TiProxy 的端口，不再连接 TiDB server 的端口。

### 更改 TiProxy 配置

为了保证连接保持功能的有效性，TiProxy 不应随意重启。因此，TiProxy 的大多数配置项支持在线变更。支持在线变更的配置列表请参阅 [TiProxy 配置](/tiproxy/tiproxy-configuration.md)。

使用 TiUP 更改 TiProxy 配置时，如果要更改的配置项支持在线变更，应当带上 [`--skip-restart`](/tiup/tiup-component-cluster-reload.md#--skip-restart) 选项，避免重启 TiProxy。

### 升级 TiProxy

部署 TiProxy 时建议指定 TiProxy 的版本，使升级 TiDB 集群时不会升级 TiProxy。

如果确实要升级 TiProxy 的版本，需加上 [`--tiproxy-version`](/tiup/tiup-component-cluster-upgrade.md#--tiproxy-version) 指定 TiProxy 的版本：

```shell
tiup cluster upgrade <cluster-name> <version> --tiproxy-version <tiproxy-version>
```

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

以下情况下，TiProxy 无法进行连接迁移，因此无法正常地保持客户端连接或负载均衡：

- 单条语句或单个事务持续时间超过 TiDB server 配置的 [`graceful-wait-before-shutdown`](/tidb-configuration-file.md#graceful-wait-before-shutdown-从-v50-版本开始引入) 时间。
- 会话使用了游标读取数据，且超过 TiDB server 配置的 [`graceful-wait-before-shutdown`](/tidb-configuration-file.md#graceful-wait-before-shutdown-从-v50-版本开始引入) 时间没有读完数据或关闭游标。
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
