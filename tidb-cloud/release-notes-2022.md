---
title: 2022 年 TiDB Cloud 发布说明
summary: 了解 2022 年 TiDB Cloud 的发布说明。
---

# 2022 年 TiDB Cloud 发布说明

此页面列出了 2022 年 [TiDB Cloud](https://www.pingcap.com/tidb-cloud/) 的发布说明。

## 2022 年 12月 28 日

**常规变更**

- 目前，在将所有 [Serverless Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群的默认 TiDB 版本从 [v6.3.0](https://docs-archive.pingcap.com/tidb/v6.3/release-6.3.0) 升级到 [v6.4.0](https://docs-archive.pingcap.com/tidb/v6.4/release-6.4.0) 之后，在某些情况下冷启动速度变慢。 因此，我们将所有 Serverless Tier 集群的默认 TiDB 版本从 v6.4.0 回滚到 v6.3.0，然后尽快解决该问题，并在稍后再次升级。

## 2022 年 12月 27 日

**常规变更**

- 将所有[Serverless Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)集群的默认 TiDB 版本从 [v6.3.0](https://docs-archive.pingcap.com/tidb/v6.3/release-6.3.0) 升级到 [v6.4.0](https://docs-archive.pingcap.com/tidb/v6.4/release-6.4.0)。

- Dedicated Tier 集群的时间点恢复 (PITR) 现在已正式发布 (GA)。

    PITR 支持将任何时间点的数据恢复到新集群。要使用 PITR 功能，请确保您的 TiDB 集群版本至少为 v6.4.0，并且 TiKV 节点大小至少为 8 vCPU 和 16 GiB。

    您可以在 [TiDB Cloud 控制台](https://tidbcloud.com)的**备份设置**中启用或禁用 PITR 功能。

    有关更多信息，请参阅[备份和恢复 TiDB 集群数据](/tidb-cloud/backup-and-restore.md)。

- 支持管理多个 Changefeed 并编辑现有 Changefeed。

    - 您现在可以根据需要创建任意数量的 Changefeed 来管理不同的数据复制任务。目前，每个集群最多可以有 10 个 Changefeed。有关更多详细信息，请参阅[Changefeed 概述](/tidb-cloud/changefeed-overview.md)。
    - 您可以编辑处于暂停状态的现有 Changefeed 的配置。有关更多信息，请参阅[编辑 Changefeed](/tidb-cloud/changefeed-overview.md#edit-a-changefeed)。

- 支持直接将数据从 Amazon Aurora MySQL、Amazon Relational Database Service (RDS) MySQL 或自托管的 MySQL 兼容数据库在线迁移到 TiDB Cloud。此功能现已正式发布。

    - 在以下 6 个区域提供服务：
        - AWS 俄勒冈 (us-west-2)
        - AWS 北弗吉尼亚 (us-east-1)
        - AWS 孟买 (ap-south-1)
        - AWS 新加坡 (ap-southeast-1)
        - AWS 东京 (ap-northeast-1)
        - AWS 法兰克福 (eu-central-1)
    - 支持多种规格。您可以根据所需的性能选择合适的规格，以获得最佳的数据迁移体验。

  有关如何将数据迁移到 TiDB Cloud，请参阅[用户文档](/tidb-cloud/migrate-from-mysql-using-data-migration.md)。有关计费详情，请参阅[数据迁移计费](/tidb-cloud/tidb-cloud-billing-dm.md)。

- 支持将本地 CSV 文件导入到 TiDB Cloud。

    只需点击几下即可完成任务配置，然后您的本地 CSV 数据就可以快速导入到您的 TiDB 集群中。使用此方法时，您无需提供云存储桶路径和 Role ARN。整个导入过程快速而流畅。

    有关更多信息，请参阅[将本地文件导入到 TiDB Cloud](/tidb-cloud/tidb-cloud-import-local-files.md)。

## 2022 年 12月 20 日

**常规变更**

- 将标签 `project name` 添加到 [Datadog](/tidb-cloud/monitor-datadog-integration.md) 仪表盘，作为过滤器以提供项目信息。

    您可以使用过滤器 `project name` 快速找到您想要的集群。

## 2022 年 12月 13 日

**常规变更**

- 推出 TiDB Cloud SQL 编辑器（Beta）用于 Serverless Tier。

    这是一个基于 Web 的 SQL 编辑器，允许您直接编辑和运行针对 Serverless Tier 数据库的 SQL 查询。 您可以在 Serverless Tier 集群的左侧导航栏中轻松找到它。

    对于 Serverless Tier，Web SQL Shell 已被 SQL 编辑器取代。

- 支持使用 [Changefeeds](/tidb-cloud/changefeed-overview.md) 为 Dedicated Tier 流式传输数据。

    - 支持 [将数据变更日志流式传输到 MySQL](/tidb-cloud/changefeed-sink-to-mysql.md)。

      当数据从 MySQL/Aurora 迁移到 TiDB 时，通常需要使用 MySQL 作为备用数据库，以防止出现意外的数据迁移问题。 在这种情况下，您可以使用 MySQL sink 将数据从 TiDB 流式传输到 MySQL。

    - 支持 [将数据变更日志流式传输到 Apache Kafka](/tidb-cloud/changefeed-sink-to-apache-kafka.md) (Beta)。

      将 TiDB 数据流式传输到消息队列是数据集成场景中非常常见的需求。 您可以使用 Kafka sink 来实现与其他数据处理系统（例如 Snowflake）的集成，或者支持业务消费。

    有关更多信息，请参阅 [Changefeed 概述](/tidb-cloud/changefeed-overview.md)。

- 组织所有者可以在**组织设置**中编辑组织的名称。

**控制台变更**

- 优化 [TiDB Cloud 控制台](https://tidbcloud.com) 的导航布局，为用户提供全新的导航体验。

    新布局包括以下更改：

    - 引入左侧导航栏，最大限度地提高屏幕使用效率。
    - 采用更扁平的导航层次结构。

- 改善 Serverless Tier 用户的 [**连接**](/tidb-cloud/connect-to-tidb-cluster-serverless.md) 体验。

    现在，开发人员只需点击几下，即可连接到 SQL 编辑器或使用他们喜欢的工具，而无需切换上下文。

## 2022 年 12月 6 日

**常规变更**

- 将新 [专用层](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的默认 TiDB 版本从 [v6.1.2](https://docs.pingcap.com/tidb/stable/release-6.1.2) 升级到 [v6.1.3](https://docs.pingcap.com/tidb/stable/release-6.1.3)。

## 2022 年 11月 29 日

**常规变更**

- 改善来自 AWS Marketplace 和 Google Cloud Marketplace 的用户体验。

    无论您是 TiDB Cloud 的新用户还是已经拥有 TiDB Cloud 帐户，现在您都可以与您的 AWS 或 GCP 结算帐户关联，从而更轻松地完成 AWS 或 GCP Marketplace 订阅。

    有关如何建立关联，请参阅[从 AWS Marketplace 或 Google Cloud Marketplace 结算](/tidb-cloud/tidb-cloud-billing.md#billing-from-aws-marketplace-azure-marketplace-or-google-cloud-marketplace)。

## 2022 年 11月 22 日

**常规变更**

* 支持直接将数据从 Amazon Aurora MySQL、Amazon Relational Database Service (RDS) MySQL 或自托管的 MySQL 兼容数据库在线迁移到 TiDB Cloud（beta 版）。

    以前，您需要暂停业务并离线导入数据，或者使用第三方工具将数据迁移到 TiDB Cloud，这很复杂。现在，借助 **数据迁移** 功能，您只需在 TiDB Cloud 控制台上执行操作，即可安全地将数据迁移到 TiDB Cloud，且停机时间最短。

    此外，数据迁移还提供完整和增量数据迁移功能，可将现有数据和正在进行的更改从数据源迁移到 TiDB Cloud。

    目前，数据迁移功能仍处于 **beta 版**。它仅适用于 [专用层](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群，且仅在 AWS 俄勒冈 (us-west-2) 和 AWS 新加坡 (ap-southeast-1) 区域提供。每个组织可以免费创建一个迁移作业。要为一个组织创建多个迁移作业，您需要[提交工单](/tidb-cloud/tidb-cloud-support.md)。

    有关详细信息，请参阅[使用数据迁移将 MySQL 兼容数据库迁移到 TiDB Cloud](/tidb-cloud/migrate-from-mysql-using-data-migration.md)。

## 2022 年 11月 15 日

**常规变更**

* 支持[专用层](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)集群的时间点恢复 (PITR)（测试版）。

    PITR 支持将任何时间点的数据恢复到新集群。您可以使用它来：

    * 降低灾难恢复中的 RPO。
    * 通过恢复到错误事件发生前的时间点来解决数据写入错误。
    * 审计业务的历史数据。

  要使用 PITR 功能，请确保您的 TiDB 集群版本至少为 v6.3.0，并且 TiKV 节点大小至少为 8 个 vCPU 和 16 GiB。

  默认情况下，备份数据存储在创建集群的同一区域中。在日本，对于在 GCP 上托管且启用了 PITR 的 TiDB 集群，您可以选择在一个或两个区域（东京和/或大阪）中存储备份数据。从备用区域恢复数据可提供更高的数据安全性，并且可以容忍区域故障。

  有关更多信息，请参见[备份和恢复 TiDB 集群数据](/tidb-cloud/backup-and-restore.md)。

  此功能仍处于测试阶段，仅应要求提供：

    * 点击 TiDB Cloud 控制台右下角的**帮助**。
    * 在对话框中，在**描述**字段中填写“申请 PITR”，然后点击**发送**。

* 数据库审计日志记录功能现已正式发布 (GA)。

    您可以使用数据库审计日志记录来记录用户访问详细信息（例如执行的任何 SQL 语句）的历史记录，并定期分析数据库审计日志，这有助于确保数据库的安全。

    有关更多信息，请参见[数据库审计日志记录](/tidb-cloud/tidb-cloud-auditing.md)。

## 2022 年 11月 8 日

**常规变更**

* 改进用户反馈渠道。

    现在您可以在 TiDB Cloud 控制台的**支持** > **提供反馈**中请求演示或信用额度。如果您想了解更多关于 TiDB Cloud 的信息，这将很有帮助。

    收到您的请求后，我们将尽快与您联系以提供帮助。

## 2022 年 10月 28 日

**常规变更**

* 开发者层级已升级到[无服务器层级](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)。无服务器层级是 TiDB 的完全托管、自动伸缩部署，现已可用。它仍处于 Beta 阶段，可免费使用。

    * 无服务器层级集群仍然包含与专用层级集群完全相同功能的 HTAP 能力。
    * 无服务器层级为您提供更快的集群创建时间和即时冷启动时间。与开发者层级相比，创建时间从几分钟缩短到几秒钟。
    * 您无需担心部署拓扑。无服务器层级将根据您的请求自动调整。
    * 无服务器层级[为了安全起见，强制执行与集群的 TLS 连接](/tidb-cloud/secure-connections-to-serverless-clusters.md)。
    * 现有的开发者层级集群将在未来几个月 内自动迁移到无服务器层级。您使用集群的能力不应受到影响，并且您不会因在 Beta 版中使用无服务器层级集群而被收费。

  从[这里](/tidb-cloud/tidb-cloud-quickstart.md)开始。

## 2022 年 10月 25 日

**常规变更**

- 支持动态更改和持久化 TiDB 系统变量的子集（beta）。

    您可以使用标准 SQL 语句为支持的系统变量设置新值。

    ```sql
    SET [GLOBAL|SESSION] <variable>
    ```

    例如：

    ```sql
    SET GLOBAL tidb_committer_concurrency = 127;
    ```

    如果在 `GLOBAL` 级别设置变量，则该变量将应用于集群并持久化（即使在您重新启动或重新加载服务器后仍保持有效）。`SESSION` 级别的变量不是持久的，仅在当前会话中有效。

    **此功能仍处于 beta 阶段**，仅支持有限数量的变量。不建议修改其他 [系统变量](/system-variables.md)，因为存在不确定性的副作用。请参阅以下列表，了解基于 TiDB v6.1 的所有支持的变量：

    - [`require_secure_transport`](/system-variables.md#require_secure_transport-new-in-v610)
    - [`tidb_committer_concurrency`](/system-variables.md#tidb_committer_concurrency-new-in-v610)
    - [`tidb_enable_batch_dml`](/system-variables.md#tidb_enable_batch_dml)
    - [`tidb_enable_prepared_plan_cache`](/system-variables.md#tidb_enable_prepared_plan_cache-new-in-v610)
    - [`tidb_max_tiflash_threads`](/system-variables.md#tidb_max_tiflash_threads-new-in-v610)
    - [`tidb_mem_oom_action`](/system-variables.md#tidb_mem_oom_action-new-in-v610)
    - [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)
    - [`tidb_prepared_plan_cache_size`](/system-variables.md#tidb_prepared_plan_cache_size-new-in-v610)
    - [`tidb_query_log_max_len`](/system-variables.md#tidb_query_log_max_len)

- 将新的 [专用层](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的默认 TiDB 版本从 [v6.1.1](https://docs.pingcap.com/tidb/stable/release-6.1.1) 升级到 [v6.1.2](https://docs.pingcap.com/tidb/stable/release-6.1.2)。

## 2022 年 10月 19 日

**集成变更**

* 在 [Vercel Integration Marketplace](https://vercel.com/integrations#databases) 中发布 [TiDB Cloud Vercel 集成](https://vercel.com/integrations/tidb-cloud)。

    [Vercel](https://vercel.com) 是前端开发者的平台，提供创新者所需的快速性和可靠性，以便在灵感迸发时进行创作。 使用 TiDB Cloud Vercel 集成，您可以轻松地将您的 Vercel 项目连接到 TiDB Cloud 集群。 有关详细信息，请参阅文档 [将 TiDB Cloud 与 Vercel 集成](/tidb-cloud/integrate-tidbcloud-with-vercel.md)。

* 在 [Vercel 模板列表](https://vercel.com/templates) 中发布 [TiDB Cloud Starter Template](https://vercel.com/templates/next.js/tidb-cloud-starter)。

    您可以使用此模板作为尝试 Vercel 和 TiDB Cloud 的起点。 在使用此模板之前，您需要先[将数据导入到您的 TiDB Cloud 集群中](https://github.com/pingcap/tidb-prisma-vercel-demo#2-import-table-structures-and-data)。

## 2022 年 10月 18 日

**常规变更**

* 对于专用层集群，TiKV 或 TiFlash 节点的最小存储大小从 500 GiB 更改为 200 GiB。 这对于工作负载数据量较小的用户来说更具成本效益。

    有关更多详细信息，请参见 [TiKV 节点存储](/tidb-cloud/size-your-cluster.md#tikv-node-storage-size) 和 [TiFlash 节点存储](/tidb-cloud/size-your-cluster.md#tiflash-node-storage)。

* 引入在线合同以自定义 TiDB Cloud 订阅并满足合规性要求。

    [**合同** 选项卡](/tidb-cloud/tidb-cloud-billing.md#contract) 已添加到 TiDB Cloud 控制台的 **账单** 页面。 如果您已与我们的销售人员就合同达成一致，并收到一封电子邮件以在线处理合同，则可以转到 **合同** 选项卡以查看和接受合同。 要了解有关合同的更多信息，请随时[联系我们的销售](https://www.pingcap.com/contact-us/)。

**文档变更**

* 添加 [文档](/tidb-cloud/terraform-tidbcloud-provider-overview.md) 以用于 [TiDB Cloud Terraform Provider](https://registry.terraform.io/providers/tidbcloud/tidbcloud)。

    TiDB Cloud Terraform Provider 是一个插件，允许您使用 [Terraform](https://www.terraform.io/) 来管理 TiDB Cloud 资源，例如集群、备份和恢复。 如果您正在寻找一种简单的方法来自动化资源配置和基础架构工作流程，您可以根据 [文档](/tidb-cloud/terraform-tidbcloud-provider-overview.md) 试用 TiDB Cloud Terraform Provider。

## 2022 年 10月 11 日

**常规变更**

* 将新的[开发者层](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)集群的默认 TiDB 版本从 [v6.2.0](https://docs-archive.pingcap.com/tidb/v6.2/release-6.2.0) 升级到 [v6.3.0](https://docs-archive.pingcap.com/tidb/v6.3/release-6.3.0)。

**控制台变更**

* 优化[账单详情页](/tidb-cloud/tidb-cloud-billing.md#billing-details)上的账单信息：

    * 在**按服务汇总**部分提供更细粒度的节点级别账单信息。
    * 添加**使用详情**部分。您还可以将使用详情下载为 CSV 文件。

## 2022 年 9月 27 日

**常规变更**

* 支持通过邀请加入多个组织。

    在 TiDB Cloud 控制台中，您可以查看您已加入的所有组织并在它们之间切换。有关详细信息，请参阅[在组织之间切换](/tidb-cloud/manage-user-access.md#view-and-switch-between-organizations)。

* 添加用于 SQL 诊断的[慢查询](/tidb-cloud/tune-performance.md#slow-query)页面。

    在“慢查询”页面上，您可以搜索和查看 TiDB 集群中的所有慢查询，并通过查看其[执行计划](https://docs.pingcap.com/tidbcloud/explain-overview)、SQL 执行信息和其他详细信息来探索每个慢查询的瓶颈。

* 当您重置帐户密码时，TiDB Cloud 会根据您最近的四个密码检查您的新密码输入，并提醒您避免使用它们中的任何一个。不允许使用任何四个已使用的密码。

    有关详细信息，请参阅[密码验证](/tidb-cloud/tidb-cloud-password-authentication.md)。

## 2022 年 9月 20 日

**常规变更**

* 为自助服务用户引入[基于成本配额的发票](/tidb-cloud/tidb-cloud-billing.md#invoices)。

    当您的成本达到配额时，TiDB Cloud 将生成发票。要提高配额或每月 接收发票，请联系[我们的销售](https://www.pingcap.com/contact-us/)。

* 免除数据备份成本中的存储操作费用。 有关最新定价信息，请参阅[TiDB Cloud 定价详情](https://www.pingcap.com/tidb-cloud-pricing-details/)。

**控制台变更**

* 提供用于数据导入的全新 Web UI。 新的 UI 提供更好的用户体验，并使数据导入更加高效。

    使用新的 UI，您可以预览要导入的数据，查看导入过程，并轻松管理所有导入任务。

**API 变更**

* TiDB Cloud API（beta）现已向所有用户开放。

    您可以通过在 TiDB Cloud 控制台中创建 API 密钥来开始使用 API。 有关更多信息，请参阅[API 文档](/tidb-cloud/api-overview.md)。

## 2022 年 9月 15 日

**常规变更**

* 支持通过 TLS 连接到 TiDB Cloud [专用层级](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群。

    对于专用层级集群，[连接](/tidb-cloud/connect-via-standard-connection.md)对话框中的**标准连接**选项卡现在提供了一个链接，用于下载 TiDB 集群 CA，并提供 TLS 连接的连接字符串和示例代码。 您可以使用第三方 MySQL 客户端、MyCLI 以及应用程序的多种连接方法（例如 JDBC、Python、Go 和 Node.js）[通过 TLS 连接到您的专用层级集群](/tidb-cloud/connect-via-standard-connection.md)。 此功能可确保从您的应用程序到 TiDB 集群的数据传输安全。

## 2022 年 9月 14 日

**控制台变更**

* 优化[集群](https://tidbcloud.com/project/clusters)页面和集群概览页面的UI，以获得更好的用户体验。

    在新的设计中，升级到专用层、集群连接和数据导入的入口被突出显示。

* 为[开发者层](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)集群引入 Playground。

    Playground 包含一个预加载的 GitHub 事件数据集，允许您通过立即运行查询来开始使用 TiDB Cloud，而无需导入数据或连接到客户端。

## 2022 年 9月 13 日

**通用变更**

* 支持新的 Google Cloud 区域，用于 [专用层](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群：`N. Virginia (us-east4)`。

## 2022 年 9月 9 日

**常规变更**

* 在 Datadog 中提供 Dedicated Tier 集群的[更多指标](/tidb-cloud/monitor-datadog-integration.md#metrics-available-to-datadog)，以帮助您更好地了解集群性能状态。

    如果您已将 TiDB Cloud 与 [Datadog 集成](/tidb-cloud/monitor-datadog-integration.md)，则可以直接在 Datadog 仪表板中查看这些指标。

## 2022 年 9月 6 日

**通用变更**

* 将新[专用层](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)集群的默认 TiDB 版本从 [v6.1.0](https://docs.pingcap.com/tidb/stable/release-6.1.0) 升级到 [v6.1.1](https://docs.pingcap.com/tidb/stable/release-6.1.1)。

**控制台变更**

* 现在，您可以从 TiDB Cloud 控制台右上角的入口[申请 PoC](/tidb-cloud/tidb-cloud-poc.md)。

**API 变更**

* 支持通过 [TiDB Cloud API](/tidb-cloud/api-overview.md) 增加 TiKV 或 TiFlash 节点的存储。 您可以使用 API 端点的 `storage_size_gib` 字段进行扩容。

    目前，TiDB Cloud API 仍处于 Beta 阶段，仅应要求提供。

    有关详细信息，请参阅[修改专用层集群](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/UpdateCluster)。

## 2022 年 8月 30 日

**常规变更**

* 支持 AWS PrivateLink 驱动的终端节点连接，作为 TiDB Cloud [专用层](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的一种新的网络访问管理选项。

    终端节点连接是安全且私密的，不会将您的数据暴露给公共互联网。此外，终端节点连接支持 CIDR 重叠，并且更易于网络管理。

    有关更多信息，请参阅 [设置私有终端节点连接](/tidb-cloud/set-up-private-endpoint-connections.md)。

**控制台变更**

* 在 [专用层](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的 [连接](/tidb-cloud/connect-to-tidb-cluster.md) 对话框的 **VPC 对等连接** 选项卡和 **私有终端节点** 选项卡中，提供 MySQL、MyCLI、JDBC、Python、Go 和 Node.js 的示例连接字符串。

    您只需将连接代码复制并粘贴到您的应用程序中，即可轻松连接到您的专用层集群。

## 2022 年 8月 24 日

**常规变更**

* 支持暂停或恢复专用层集群。

    您可以在 TiDB Cloud 中[暂停或恢复您的专用层集群](/tidb-cloud/pause-or-resume-tidb-cluster.md)。集群暂停后，节点计算费用将不会被收取。

## 2022 年 8月 23 日

**常规变更**

* 将新的[开发者层级](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)集群的默认 TiDB 版本从 [v6.1.0](https://docs.pingcap.com/tidb/stable/release-6.1.0) 升级到 [v6.2.0](https://docs-archive.pingcap.com/tidb/v6.2/release-6.2.0)。

**API 变更**

* 引入 TiDB Cloud API 作为 beta 版本。

    通过此 API，您可以自动高效地管理 TiDB Cloud 资源（例如集群）。 有关更多信息，请参见 [TiDB Cloud API 文档](https://docs.pingcap.com/tidbcloud/api/v1beta)。

    目前，TiDB Cloud API 仍处于 beta 阶段，仅应要求提供。 您可以通过提交请求来申请 API 访问权限：

    * 点击 [TiDB Cloud 控制台](https://tidbcloud.com/project/clusters) 右下角的 **帮助**。
    * 在对话框中，在 **描述** 字段中填写“申请 TiDB Cloud API”，然后点击 **发送**。

## 2022 年 8月 16 日

* 添加 `2 vCPU, 8 GiB (Beta)` 节点大小的 TiDB 和 TiKV 作为 Beta 版本。

    * 对于每个 `2 vCPU, 8 GiB (Beta)` TiKV 节点，存储大小在 200 GiB 到 500 GiB 之间。

    * 建议的使用场景：

        * 中小企业的低负载生产环境
        * PoC 和预发布环境
        * 开发环境

* 为 PoC 用户引入 [Credits](/tidb-cloud/tidb-cloud-billing.md#credits)（之前称为试用积分）。

    现在您可以在**账单**页面的 **Credits** 选项卡上查看有关您组织积分的信息，这些积分可用于支付 TiDB Cloud 费用。 您可以<a href="mailto:tidbcloud-support@pingcap.com">联系我们</a>以获取积分。

## 2022 年 8月 9 日

* 添加对GCP区域`Osaka`的支持，用于创建[专用层](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)集群。

## 2022 年 8月 2 日

* TiDB 和 TiKV 的 `4 vCPU, 16 GiB` 节点大小现已正式发布 (GA)。

    * 对于每个 `4 vCPU, 16 GiB` TiKV 节点，存储大小在 200 GiB 到 2 TiB 之间。
    * 建议的使用场景：

        * 适用于中小企业的低工作负载生产环境
        * PoC 和暂存环境
        * 开发环境

* 在 [专用层集群](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 的 **诊断** 选项卡中添加 [监控页面](/tidb-cloud/built-in-monitoring.md)。

    监控页面提供了一个系统级的入口，用于整体性能诊断。根据自上而下的性能分析方法，监控页面根据数据库时间分解组织 TiDB 性能指标，并以不同的颜色显示这些指标。通过检查这些颜色，您可以一目了然地识别整个系统的性能瓶颈，从而大大缩短性能诊断时间，简化性能分析和诊断。

* 在 CSV 和 Parquet 源文件的 **数据导入** 页面上添加一个开关，用于启用或禁用 **自定义模式**。

    **自定义模式** 功能默认禁用。当您要将文件名与特定模式匹配的 CSV 或 Parquet 文件导入到单个目标表时，可以启用它。

    有关更多信息，请参阅 [导入 CSV 文件](/tidb-cloud/import-csv-files.md) 和 [导入 Apache Parquet 文件](/tidb-cloud/import-parquet-files.md)。

* 添加 TiDB Cloud 支持计划（基本、标准、企业和高级），以满足客户组织的不同支持需求。有关更多信息，请参阅 [TiDB Cloud 支持](/tidb-cloud/tidb-cloud-support.md)。

* 优化 [集群](https://tidbcloud.com/project/clusters) 页面和集群详细信息页面的 UI：

    * 在 **集群** 页面上添加 **连接** 和 **导入数据** 按钮。
    * 将 **连接** 和 **导入数据** 按钮移动到集群详细信息页面的右上角。

## 2022 年 7月 28 日

* 在**安全快速入门**对话框中添加**允许从任何位置访问**按钮，允许任何 IP 地址访问您的集群。 更多信息，请参阅 [配置集群安全设置](/tidb-cloud/configure-security-settings.md)。

## 2022 年 7月 26 日

* 支持新的[开发者层集群](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)的自动休眠和恢复。

    开发者层集群在不活动 7 天后不会被删除，因此您可以在一年免费试用期结束前的任何时间使用它。 不活动 24 小时后，开发者层集群将自动休眠。 要恢复集群，请向集群发送新连接，或单击 TiDB Cloud 控制台中的**恢复**按钮。 集群将在 50 秒内恢复并自动恢复服务。

* 为新的[开发者层集群](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)添加用户名前缀限制。

    无论何时使用或设置数据库用户名，都必须在用户名中包含集群的前缀。 有关更多信息，请参见[用户名前缀](/tidb-cloud/select-cluster-tier.md#user-name-prefix)。

* 禁用[开发者层集群](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)的备份和恢复功能。

    开发者层集群禁用备份和恢复功能（包括自动备份和手动备份）。 您仍然可以使用 [Dumpling](https://docs.pingcap.com/tidb/stable/dumpling-overview) 导出数据作为备份。

* 将[开发者层](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)集群的存储大小从 500 MiB 增加到 1 GiB。
* 向 TiDB Cloud 控制台添加面包屑导航，以改善导航体验。
* 支持在将数据导入 TiDB Cloud 时配置多个过滤规则。
* 从**项目设置**中删除**流量过滤器**页面，并从**连接到 TiDB** 对话框中删除**从默认集添加规则**按钮。

## 2022 年 7月 19 日

* 为 [TiKV 节点大小](/tidb-cloud/size-your-cluster.md#tikv-vcpu-and-ram) 提供一个新的选项：`8 vCPU, 32 GiB`。对于一个 8 vCPU 的 TiKV 节点，您可以选择 `8 vCPU, 32 GiB` 或 `8 vCPU, 64 GiB`。
* 在 [**连接到 TiDB**](/tidb-cloud/connect-via-standard-connection.md) 对话框中提供的示例代码中支持语法高亮，以提高代码的可读性。您可以轻松识别需要在示例代码中替换的参数。
* 支持在您确认 [**数据导入任务**](/tidb-cloud/import-sample-data.md) 页面上的导入任务后，自动验证 TiDB Cloud 是否可以访问您的源数据。
* 更改 TiDB Cloud 控制台的主题颜色，使其与 [PingCAP 网站](https://www.pingcap.com/) 的主题颜色保持一致。

## 2022 年 7月 12 日

* 在 Amazon S3 的 [**数据导入任务**](/tidb-cloud/import-sample-data.md) 页面添加 **Validate** 按钮，帮助您在数据导入开始前检测数据访问问题。
* 在 [**付款方式**](/tidb-cloud/tidb-cloud-billing.md#payment-method) 选项卡下添加 **账单资料**。 通过在 **账单资料** 中提供您的税务登记号码，某些税款可能会从您的发票中免除。 有关更多信息，请参阅 [编辑账单资料信息](/tidb-cloud/tidb-cloud-billing.md#billing-profile)。

## 2022 年 7月 5 日

* 列式存储 [TiFlash](/tiflash/tiflash-overview.md) 现已正式发布 (GA)。

    - TiFlash 使 TiDB 本质上成为混合事务/分析处理 (HTAP) 数据库。您的应用程序数据首先存储在 TiKV 中，然后通过 Raft 共识算法复制到 TiFlash。因此，它是从行存储到列存储的实时复制。
    - 对于具有 TiFlash 副本的表，TiDB 优化器会自动根据成本估算确定是使用 TiKV 还是 TiFlash 副本。

    要体验 TiFlash 带来的好处，请参阅 [TiDB Cloud HTAP 快速入门指南](/tidb-cloud/tidb-cloud-htap-quickstart.md)。

* 支持[增加 TiKV 和 TiFlash 的存储大小](/tidb-cloud/scale-tidb-cluster.md#change-storage)，适用于专用层集群。
* 支持在节点大小字段中显示内存信息。

## 2022 年 6月 28 日

* 将 TiDB Cloud Dedicated Tier 从 [TiDB v5.4.1](https://docs.pingcap.com/tidb/stable/release-5.4.1) 升级到 [TiDB v6.1.0](https://docs.pingcap.com/tidb/stable/release-6.1.0)。

## 2022 年 6月 23 日

* 增加 TiDB Cloud 上 TiKV 的最大[存储容量](/tidb-cloud/size-your-cluster.md#tikv-node-storage-size)。

    * 8 vCPU 或 16 vCPU TiKV：支持高达 4 TiB 的存储容量。
    * 4 vCPU TiKV：支持高达 2 TiB 的存储容量。

## 2022 年 6月 21 日

* 为[专用层](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)集群创建添加对GCP区域`台湾`的支持。
* 支持在TiDB Cloud控制台中[更新用户个人资料](/tidb-cloud/manage-user-access.md#manage-user-profiles)，包括名字、姓氏、公司名称、国家和电话号码。
* 在[**连接到TiDB**](/tidb-cloud/connect-via-standard-connection.md)对话框中提供MySQL、MyCLI、JDBC、Python、Go和Node.js的连接字符串，以便您可以轻松连接到您的TiDB集群。
* 支持在数据导入期间自动从存储桶URI获取存储桶区域，从而节省您填写此类信息的工作量。

## 2022 年 6月 16 日

* 简化[集群创建流程](/tidb-cloud/create-tidb-cluster.md)。

    - 创建集群时，TiDB Cloud 提供默认集群名称。 您可以使用默认名称或更新它。
    - 创建集群时，您无需在**创建集群**页面上设置密码。
    - 在集群创建期间或之后，您可以设置 root 密码以访问集群，并在**安全快速入门**对话框中设置连接到集群的 IP 地址。

## 2022 年 6月 14 日

* 将 TiDB Cloud 升级到 [TiDB v6.1.0](https://docs.pingcap.com/tidb/stable/release-6.1.0) 以用于开发者层级。
* 优化 **项目设置** 的入口。 从 TiDB Cloud 控制台，您可以选择一个目标项目，然后点击 **项目设置** 选项卡轻松进入其设置。
* 通过在 TiDB Cloud 控制台中提供过期消息，优化密码过期的体验。

## 2022 年 6月 7 日

* 添加 [免费试用](https://tidbcloud.com/free-trial) 注册页面，以便快速注册 TiDB Cloud。
* 从套餐选择页面移除 **概念验证计划** 选项。 如果您想免费申请 14 天的 PoC 试用，请<a href="mailto:tidbcloud-support@pingcap.com">联系我们</a>。 更多信息，请参见 [使用 TiDB Cloud 执行概念验证 (PoC)](/tidb-cloud/tidb-cloud-poc.md)。
* 通过提示使用电子邮件和密码注册 TiDB Cloud 的用户每 90 天重置密码来提高系统安全性。 更多信息，请参见 [密码验证](/tidb-cloud/tidb-cloud-password-authentication.md)。

## 2022 年 5月 24 日

* 支持在[创建](/tidb-cloud/create-tidb-cluster.md)或[恢复](/tidb-cloud/backup-and-restore.md#restore) Dedicated Tier 集群时自定义 TiDB 端口号。

## 2022 年 5月 19 日

* 为[开发者层](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)集群创建添加对AWS区域`Frankfurt`的支持。

## 2022 年 5月 18 日

* 支持使用 GitHub 帐户[注册](https://tidbcloud.com/signup) TiDB Cloud。

## 2022 年 5月 13 日

* 支持使用 Google 账号[注册](https://tidbcloud.com/signup) TiDB Cloud。

## 2022 年 5月 1 日

* 支持在[创建](/tidb-cloud/create-tidb-cluster.md)或[恢复](/tidb-cloud/backup-and-restore.md#restore)[专用层](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)集群时配置 TiDB、TiKV 和 TiFlash 的 vCPU 大小。
* 增加对 AWS 区域 `Mumbai` 创建集群的支持。
* 更新 [TiDB Cloud 账单](/tidb-cloud/tidb-cloud-billing.md)的计算、存储和数据传输成本。

## 2022 年 4月 7 日

* 将 TiDB Cloud 升级到 [TiDB v6.0.0](https://docs-archive.pingcap.com/tidb/v6.0/release-6.0.0-dmr)，用于开发者层。

## 2022 年 3月 31 日

TiDB Cloud 现在已正式发布 (GA)。 您可以[注册](https://tidbcloud.com/signup)并选择以下选项之一：

* 免费开始使用 [开发者层级](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)。
* <a href="mailto:tidbcloud-support@pingcap.com">联系我们</a> 申请 14 天的免费 PoC 试用。
* 通过 [专用层级](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 获得完全访问权限。

## 2022 年 3月 25 日

新功能：

* 支持 [TiDB Cloud 内置告警](/tidb-cloud/monitor-built-in-alerting.md)。

    使用 TiDB Cloud 内置告警功能，当您的项目中 TiDB Cloud 集群触发 TiDB Cloud 内置告警条件时，您可以通过电子邮件收到通知。

## 2022 年 3月 15 日

常规变更：

* 不再有固定集群大小的集群层级。您可以轻松自定义 TiDB、TiKV 和 TiFlash 的[集群大小](/tidb-cloud/size-your-cluster.md)。
* 支持为没有 TiFlash 的现有集群添加 [TiFlash](/tiflash/tiflash-overview.md) 节点。
* 支持在[创建新集群](/tidb-cloud/create-tidb-cluster.md)时指定存储大小（500 到 2048 GiB）。集群创建后，存储大小无法更改。
* 引入一个新的公共区域：`eu-central-1`。
* 弃用 8 vCPU TiFlash，并提供 16 vCPU TiFlash。
* 分离 CPU 和存储的价格（两者都有 30% 的公开预览折扣）。
* 更新[计费信息](/tidb-cloud/tidb-cloud-billing.md)和[价格表](https://www.pingcap.com/pricing/)。

新功能：

* 支持 [Prometheus 和 Grafana 集成](/tidb-cloud/monitor-prometheus-and-grafana-integration.md)。

    通过 Prometheus 和 Grafana 集成，您可以配置一个 [Prometheus](https://prometheus.io/) 服务来从 TiDB Cloud 端点读取关键指标，并使用 [Grafana](https://grafana.com/) 查看这些指标。

* 支持根据新集群的所选区域分配默认备份时间。

    有关更多信息，请参阅[备份和恢复 TiDB 集群数据](/tidb-cloud/backup-and-restore.md)。

## 2022 年 3月 4 日

新功能：

* 支持 [Datadog 集成](/tidb-cloud/monitor-datadog-integration.md)。

    通过 Datadog 集成，您可以配置 TiDB Cloud 以将有关 TiDB 集群的指标数据发送到 [Datadog](https://www.datadoghq.com/)。 之后，您可以直接在 Datadog 仪表板中查看这些指标。

## 2022 年 2月 15 日

常规变更：

* 将 TiDB Cloud 升级到 [TiDB v5.4.0](https://docs.pingcap.com/tidb/stable/release-5.4.0)，适用于开发者层级。

改进：

* 支持在将 [CSV 文件](/tidb-cloud/import-csv-files.md) 或 [Apache Parquet 文件](/tidb-cloud/import-parquet-files.md) 导入到 TiDB Cloud 时使用自定义文件名。

## 2022 年 1月 11 日

常规变更：

* 将 TiDB Operator 升级到 [v1.2.6](https://docs.pingcap.com/tidb-in-kubernetes/stable/release-1.2.6)。

改进：

* 在 [**连接**](/tidb-cloud/connect-via-standard-connection.md) 页面上的 MySQL 客户端添加建议选项 `--connect-timeout 15`。

Bug 修复：

* 修复了密码包含单引号时用户无法创建集群的问题。
* 修复了即使一个组织只有一个所有者，所有者也可以被删除或更改为其他角色的问题。