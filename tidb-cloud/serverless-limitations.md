---
title: TiDB Cloud Serverless 限制和配额
summary: 了解 TiDB Cloud Serverless 的限制。
aliases: ['/tidbcloud/serverless-tier-limitations']
---

# TiDB Cloud Serverless 限制和配额

<!-- markdownlint-disable MD026 -->

TiDB Cloud Serverless 几乎可以支持所有 TiDB 支持的工作负载，但在 TiDB 自管理或 TiDB Cloud Dedicated 集群与 TiDB Cloud Serverless 集群之间存在一些功能差异。本文档描述了 TiDB Cloud Serverless 的限制。

我们正在不断填补 TiDB Cloud Serverless 和 TiDB Cloud Dedicated 之间的功能差距。如果你需要这些差距中的功能或能力，请使用 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 或[联系我们](https://www.pingcap.com/contact-us/?from=en)提出功能请求。

## 限制

### 审计日志

- 目前不支持[数据库审计日志](/tidb-cloud/tidb-cloud-auditing.md)。

### 连接

- 只能使用[公共端点](/tidb-cloud/connect-via-standard-connection-serverless.md)和[私有端点](/tidb-cloud/set-up-private-endpoint-connections-serverless.md)。你不能使用 [VPC 对等连接](/tidb-cloud/set-up-vpc-peering-connections.md)连接到 TiDB Cloud Serverless 集群。
- 不支持 [IP 访问列表](/tidb-cloud/configure-ip-access-list.md)。

### 加密

- 你的 TiDB Cloud Serverless 集群中持久化的数据使用管理集群的云提供商提供的加密工具进行加密。对于[可扩展集群](/tidb-cloud/select-cluster-tier.md#scalable-cluster-plan)，在集群创建过程中可以选择使用第二层加密，在默认的静态加密之外提供额外的安全级别。
- 目前不支持使用[客户管理的加密密钥 (CMEK)](/tidb-cloud/tidb-cloud-encrypt-cmek.md)。

### 维护窗口

- 目前不支持[维护窗口](/tidb-cloud/configure-maintenance-window.md)。

### 监控和诊断

- 目前不支持[第三方监控集成](/tidb-cloud/third-party-monitoring-integrations.md)。
- 目前不支持[内置告警](/tidb-cloud/monitor-built-in-alerting.md)。
- 目前不支持 [Key Visualizer](/tidb-cloud/tune-performance.md#key-visualizer)。
- 目前不支持 [Index Insight](/tidb-cloud/tune-performance.md#index-insight-beta)。

### 自助升级

- TiDB Cloud Serverless 是 TiDB 的完全托管部署。TiDB Cloud Serverless 的主要和次要版本升级由 TiDB Cloud 处理，因此用户无法主动发起。

### 数据流

- 目前 TiDB Cloud Serverless 不支持 [Changefeed](/tidb-cloud/changefeed-overview.md)。
- 目前 TiDB Cloud Serverless 不支持[数据迁移](/tidb-cloud/migrate-from-mysql-using-data-migration.md)。

### 生存时间 (TTL)

- 在 TiDB Cloud Serverless 中，表的 [`TTL_JOB_INTERVAL`](/time-to-live.md#ttl-job) 属性固定为 `15m` 且不能修改。这意味着 TiDB Cloud Serverless 每 15 分钟调度一次后台作业来清理过期数据。

### 其他

- 事务不能持续超过 30 分钟。
- 有关 SQL 限制的更多详细信息，请参阅[受限的 SQL 功能](/tidb-cloud/limited-sql-features.md)。

## 使用配额

对于 TiDB Cloud 中的每个组织，默认最多可以创建五个[免费集群](/tidb-cloud/select-cluster-tier.md#free-cluster-plan)。要创建更多的 TiDB Cloud Serverless 集群，你需要添加信用卡并创建[可扩展集群](/tidb-cloud/select-cluster-tier.md#scalable-cluster-plan)以供使用。

对于组织中的前五个 TiDB Cloud Serverless 集群，无论是免费还是可扩展集群，TiDB Cloud 都为每个集群提供以下免费使用配额：

- 行式存储：5 GiB
- 列式存储：5 GiB
- [请求单位 (RUs)](/tidb-cloud/tidb-cloud-glossary.md#request-unit)：每月 5000 万 RU

请求单位 (RU) 是用于跟踪查询或事务资源消耗的计量单位。它是一个指标，允许你估算处理数据库中特定请求所需的计算资源。请求单位也是 TiDB Cloud Serverless 服务的计费单位。

一旦集群达到其使用配额，它会立即拒绝任何新的连接尝试，直到你[增加配额](/tidb-cloud/manage-serverless-spend-limit.md#update-spending-limit)或在新月开始时重置使用量。在达到配额之前建立的现有连接将保持活动状态，但会经历限流。

要了解不同资源（包括读取、写入、SQL CPU 和网络出口）的 RU 消耗、定价详情和限流信息，请参阅 [TiDB Cloud Serverless 定价详情](https://www.pingcap.com/tidb-cloud-serverless-pricing-details)。

如果你想创建具有额外配额的 TiDB Cloud Serverless 集群，可以选择可扩展集群计划，并在集群创建页面上编辑支出限制。有关更多信息，请参阅[创建 TiDB Cloud Serverless 集群](/tidb-cloud/create-tidb-cluster-serverless.md)。

创建 TiDB Cloud Serverless 集群后，你仍然可以在集群概览页面上查看和编辑支出限制。有关更多信息，请参阅[管理 TiDB Cloud Serverless 集群的支出限制](/tidb-cloud/manage-serverless-spend-limit.md)。
