---
title: TiDB Cloud Serverless 常见问题
summary: 了解关于 TiDB Cloud Serverless 的常见问题（FAQ）。
aliases: ['/tidbcloud/serverless-tier-faqs']
---

# TiDB Cloud Serverless 常见问题

<!-- markdownlint-disable MD026 -->

本文列出了关于 TiDB Cloud Serverless 的最常见问题。

## 一般问题

### 什么是 TiDB Cloud Serverless？

TiDB Cloud Serverless 为你和你的组织提供具有完整 HTAP 功能的 TiDB 数据库。它是一个完全托管的、自动扩展的 TiDB 部署，让你可以立即开始使用数据库，无需关心底层节点即可开发和运行应用程序，并根据应用程序的工作负载变化自动扩展。

### 如何开始使用 TiDB Cloud Serverless？

参考 5 分钟[快速上手 TiDB Cloud](/tidb-cloud/tidb-cloud-quickstart.md)。

### 我可以在 TiDB Cloud 中创建多少个 TiDB Cloud Serverless 集群？

对于 TiDB Cloud 中的每个组织，默认情况下最多可以创建五个[免费集群](/tidb-cloud/select-cluster-tier.md#free-cluster-plan)。要创建更多 TiDB Cloud Serverless 集群，你需要添加信用卡并创建[可扩展集群](/tidb-cloud/select-cluster-tier.md#scalable-cluster-plan)以供使用。

### TiDB Cloud 的所有功能在 TiDB Cloud Serverless 上都完全支持吗？

某些 TiDB Cloud 功能在 TiDB Cloud Serverless 上部分支持或不支持。更多信息，请参见 [TiDB Cloud Serverless 限制和配额](/tidb-cloud/serverless-limitations.md)。

### TiDB Cloud Serverless 何时会在 AWS 以外的云平台（如 Google Cloud 或 Azure）上可用？

我们正在积极扩展 TiDB Cloud Serverless 到其他云平台，包括 Google Cloud 和 Azure。但是，由于我们目前专注于填补差距并确保所有环境中的功能无缝运行，因此目前还没有确切的时间表。请放心，我们正在努力使 TiDB Cloud Serverless 在更多云平台上可用，我们会随着进展及时更新社区。

### 我在 TiDB Cloud Serverless 可用之前创建了一个 Developer Tier 集群。我还能继续使用我的集群吗？

是的，你的 Developer Tier 集群已自动迁移到 TiDB Cloud Serverless 集群，为你提供改进的用户体验，而不会中断你之前的使用。

### TiDB Cloud Serverless 中的列式存储是什么？

TiDB Cloud Serverless 中的列式存储作为行式存储的额外副本，确保强一致性。与传统的按行存储数据的行式存储不同，列式存储按列组织数据，优化数据分析任务。

列式存储是 TiDB 的一个关键特性，通过无缝融合事务和分析工作负载，实现混合事务和分析处理（HTAP）功能。

为了高效管理列式存储数据，TiDB Cloud Serverless 使用独立的弹性 TiFlash 引擎。在查询执行期间，优化器指导集群自动决定是从行式存储还是列式存储中检索数据。

### 什么时候应该在 TiDB Cloud Serverless 中使用列式存储？

在以下场景中，考虑在 TiDB Cloud Serverless 中使用列式存储：

- 你的工作负载涉及需要高效数据扫描和聚合的分析任务。
- 你优先考虑提高性能，特别是对于分析工作负载。
- 你想要将分析处理与事务处理隔离，以防止对事务处理（TP）工作负载的性能影响。独立的列式存储有助于优化这些不同的工作负载模式。

在这些场景中，列式存储可以显著提高查询性能，并为系统中的混合工作负载提供无缝体验。

### 如何在 TiDB Cloud Serverless 中使用列式存储？

在 TiDB Cloud Serverless 中使用列式存储与在 TiFlash 中使用类似。你可以在表级和数据库级启用列式存储：

- 表级：为表分配 TiFlash 副本以启用该特定表的列式存储。
- 数据库级：为数据库中的所有表配置 TiFlash 副本，以在整个数据库中使用列式存储。

为表设置 TiFlash 副本后，TiDB 会自动将数据从该表的行式存储复制到列式存储。这确保了数据一致性并优化了分析查询的性能。

有关如何设置 TiFlash 副本的更多信息，请参见[创建 TiFlash 副本](/tiflash/create-tiflash-replicas.md)。

## 计费和计量问题

### 什么是请求单元？

TiDB Cloud Serverless 采用按需付费模式，这意味着你只需为存储空间和集群使用付费。在此模式下，所有集群活动（如 SQL 查询、批量操作和后台作业）都以[请求单元（RUs）](/tidb-cloud/tidb-cloud-glossary.md#request-unit)来量化。RU 是对集群上发起的请求的大小和复杂性的抽象度量。更多信息，请参见 [TiDB Cloud Serverless 定价详情](https://www.pingcap.com/tidb-cloud-serverless-pricing-details/)。

### TiDB Cloud Serverless 有免费计划吗？

对于组织中的前五个 TiDB Cloud Serverless 集群，TiDB Cloud 为每个集群提供以下免费使用配额：

- 行式存储：5 GiB
- 列式存储：5 GiB
- [请求单元（RUs）](/tidb-cloud/tidb-cloud-glossary.md#request-unit)：每月 5000 万 RUs

如果你使用可扩展集群，超出免费配额的使用将被收费。对于免费集群，一旦达到免费配额，该集群的读写操作将被限制，直到你升级到可扩展集群或在新月份开始时重置使用量。

更多信息，请参见 [TiDB Cloud Serverless 使用配额](/tidb-cloud/select-cluster-tier.md#usage-quota)。

### 免费计划有什么限制？

在免费计划下，由于资源不可扩展，集群性能受限。这导致每个查询的内存分配限制为 256 MiB，并可能导致每秒请求单元（RUs）的明显瓶颈。要最大化集群性能并避免这些限制，你可以升级到[可扩展集群](/tidb-cloud/select-cluster-tier.md#scalable-cluster-plan)。

### 如何估算我的工作负载所需的 RUs 数量并规划每月预算？

要获取单个 SQL 语句的 RU 消耗，你可以使用 [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md#ru-request-unit-consumption) SQL 语句。但是，需要注意的是，`EXPLAIN ANALYZE` 返回的 RUs 使用量不包括出口 RUs，因为出口使用量是在网关中单独测量的，TiDB 服务器并不知道这些信息。

要获取集群使用的 RUs 和存储量，请查看集群概览页面上的**本月使用量**面板。通过此面板中的过去资源使用数据和实时资源使用情况，你可以跟踪集群的资源消耗并估算合理的支出限额。如果免费配额无法满足你的需求，你可以升级到[可扩展集群](/tidb-cloud/select-cluster-tier.md#scalable-cluster-plan)并编辑支出限额。更多信息，请参见 [TiDB Cloud Serverless 使用配额](/tidb-cloud/select-cluster-tier.md#usage-quota)。

### 如何优化我的工作负载以最小化消耗的 RUs 数量？

确保你的查询已按照[优化 SQL 性能](/develop/dev-guide-optimize-sql-overview.md)中的指南进行了仔细优化。要识别消耗最多 RUs 的 SQL 语句，请导航到集群的[**诊断**](/tidb-cloud/tune-performance.md#view-the-diagnosis-page)页面，然后查看 **SQL 语句**标签，你可以在其中观察 SQL 执行情况并按**总 RU**或**平均 RU**查看排名靠前的语句。更多信息，请参见[语句分析](/tidb-cloud/tune-performance.md#statement-analysis)。此外，最小化出口流量的数量对于减少 RUs 消耗也很重要。为此，建议在查询中只返回必要的列和行，这反过来有助于减少网络出口流量。这可以通过仔细选择和过滤要返回的列和行来实现，从而优化网络利用率。

### TiDB Cloud Serverless 如何计量存储？

存储根据 TiDB Cloud Serverless 集群中存储的数据量计量，以每月 GiB 为单位。它通过将所有表和索引的总大小（不包括数据压缩或副本）乘以该月数据存储的小时数来计算。

### 为什么在立即删除表或数据库后存储使用量大小保持不变？

这是因为 TiDB 会在一定时间内保留已删除的表和数据库。这个保留期确保依赖这些表的事务可以继续执行而不会中断。此外，保留期使 [`FLASHBACK TABLE`](/sql-statements/sql-statement-flashback-table.md)/[`FLASHBACK DATABASE`](/sql-statements/sql-statement-flashback-database.md) 功能成为可能，允许你恢复误删的表和数据库。

### 为什么在我没有主动运行任何查询时也会有 RU 消耗？

RU 消耗可能发生在各种场景中。一个常见场景是在后台查询期间，例如在 TiDB 实例之间同步架构更改。另一个场景是当某些 Web 控制台功能生成查询时，如加载架构。即使没有明确的用户触发，这些进程也会使用 RUs。

### 为什么在我的工作负载稳定时会出现 RU 使用量的峰值？

RU 使用量的峰值可能是由 TiDB 中必要的后台作业导致的。这些作业，如自动分析表和重建统计信息，是生成优化查询计划所必需的。

### 当我的集群耗尽免费配额或超出支出限额时会发生什么？

一旦集群达到其免费配额或支出限额，集群会立即拒绝任何新的连接尝试，直到增加配额或在新月份开始时重置使用量。在达到配额之前建立的现有连接将保持活动状态，但会经历限制。更多信息，请参见 [TiDB Cloud Serverless 限制和配额](/tidb-cloud/serverless-limitations.md#usage-quota)。

### 为什么在导入数据时我观察到 RU 使用量的峰值？

在 TiDB Cloud Serverless 集群的数据导入过程中，只有在数据成功导入时才会发生 RU 消耗，这导致 RU 使用量出现峰值。

### 在 TiDB Cloud Serverless 中使用列式存储涉及哪些成本？

TiDB Cloud Serverless 中列式存储的定价与行式存储类似。当你使用列式存储时，会创建一个额外的副本来存储你的数据（不包括索引）。从行式存储到列式存储的数据复制不会产生额外费用。

有关详细定价信息，请参见 [TiDB Cloud Serverless 定价详情](https://www.pingcap.com/tidb-serverless-pricing-details/)。

### 使用列式存储是否更贵？

TiDB Cloud Serverless 中的列式存储由于额外副本而产生额外成本，需要更多存储和资源用于数据复制。但是，在运行分析查询时，列式存储变得更具成本效益。

根据 TPC-H 基准测试，在列式存储上运行分析查询的成本约为使用行式存储时成本的三分之一。

因此，虽然由于额外副本可能会有初始成本，但在分析过程中减少的计算成本可以使其对特定用例更具成本效益。特别是对于有分析需求的用户，列式存储可以显著降低成本，提供可观的成本节省机会。

## 安全问题

### 我的 TiDB Cloud Serverless 是共享的还是专用的？

serverless 技术设计用于多租户，所有集群使用的资源是共享的。要获得具有隔离基础设施和资源的托管 TiDB 服务，你可以升级到 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)。

### TiDB Cloud Serverless 如何确保安全？

- 你的连接通过传输层安全性（TLS）加密。有关使用 TLS 连接到 TiDB Cloud Serverless 的更多信息，请参见[到 TiDB Cloud Serverless 的 TLS 连接](/tidb-cloud/secure-connections-to-serverless-clusters.md)。
- TiDB Cloud Serverless 上的所有持久化数据都使用集群运行所在的云提供商的工具进行静态加密。

## 维护问题

### 我可以升级集群运行的 TiDB 版本吗？

不可以。TiDB Cloud Serverless 集群会在我们在 TiDB Cloud 上推出新的 TiDB 版本时自动升级。你可以在 [TiDB Cloud 控制台](https://tidbcloud.com/project/clusters)或最新的[发布说明](https://docs.pingcap.com/tidbcloud/tidb-cloud-release-notes)中查看集群运行的 TiDB 版本。或者，你也可以连接到集群并使用 `SELECT version()` 或 `SELECT tidb_version()` 来检查 TiDB 版本。
