---
title: 2024 年 TiDB Cloud 发布说明
summary: 了解 2024 年 TiDB Cloud 的发布说明。
---

# 2024 年 TiDB Cloud 发布说明

此页面列出了 2024 年 [TiDB Cloud](https://www.pingcap.com/tidb-cloud/) 的发布说明。

## 2024 年 12 月 17 日

**常规变更**

- TiDB Cloud Serverless 备份和恢复变更

    - 支持将数据恢复到新集群，提供更大的灵活性，并确保您当前集群的运营不受中断。

    - 优化备份和恢复策略，使其与您的集群计划保持一致。 更多信息，请参见 [备份和恢复 TiDB Cloud Serverless 数据](/tidb-cloud/backup-and-restore-serverless.md#learn-about-the-backup-setting)。

    - 应用以下兼容性策略，以帮助您顺利过渡：

        - 在 2024-12-17T10:00:00Z 之前创建的备份将在所有集群中遵循之前的保留期限。
        - 可扩展集群的备份时间将保留当前配置，而免费集群的备份时间将重置为默认设置。

## 2024 年 12 月 3 日

**通用变更**

- 推出恢复组功能（beta），用于在 AWS 上部署的 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的灾难恢复。

    此功能使您能够在 TiDB Cloud Dedicated 集群之间复制数据库，从而确保在发生区域性灾难时能够快速恢复。如果您是项目所有者角色，则可以通过创建新的恢复组并将数据库分配给该组来启用此功能。通过使用恢复组复制数据库，您可以提高灾难准备能力，满足更严格的可用性 SLA，并实现更积极的恢复点目标 (RPO) 和恢复时间目标 (RTO)。

    有关更多信息，请参阅 [恢复组入门](/tidb-cloud/recovery-group-get-started.md)。

## 2024 年 11 月 26 日

**通用变更**

- 将新 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的默认 TiDB 版本从 [v7.5.4](https://docs.pingcap.com/tidb/v7.5/release-7.5.4) 升级到 [v8.1.1](https://docs.pingcap.com/tidb/stable/release-8.1.1)。

- [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 将以下场景下的大数据写入成本降低高达 80%:

    - 当你在 [自动提交模式](/transaction-overview.md#autocommit) 下执行大于 16 MiB 的写入操作时。
    - 当你在 [乐观事务模型](/optimistic-transaction.md) 下执行大于 16 MiB 的写入操作时。
    - 当你 [将数据导入到 TiDB Cloud](/tidb-cloud/tidb-cloud-migration-overview.md#import-data-from-files-to-tidb-cloud) 时。

  此改进提高了数据操作的效率和成本效益，随着工作负载的扩展，可提供更大的节省。

## 2024 年 11 月19 日

**常规变更**

- [TiDB Cloud Serverless 分支（beta）](/tidb-cloud/branch-overview.md) 引入了以下分支管理方面的改进：

    - **灵活的分支创建**：创建分支时，您可以选择特定的集群或分支作为父级，并指定要从父级使用的精确时间点。这使您可以精确控制分支中的数据。

    - **分支重置**：您可以重置分支，使其与父级的最新状态同步。

    - **改进的 GitHub 集成**：[TiDB Cloud Branching](https://github.com/apps/tidb-cloud-branching) GitHub App 引入了 [`branch.mode`](/tidb-cloud/branch-github-integration.md#branchmode) 参数，该参数控制拉取请求同步期间的行为。在默认模式 `reset` 下，该应用程序会重置分支以匹配拉取请求中的最新更改。

  有关更多信息，请参阅[管理 TiDB Cloud Serverless 分支](/tidb-cloud/branch-manage.md)和[将 TiDB Cloud Serverless 分支（Beta）与 GitHub 集成](/tidb-cloud/branch-github-integration.md)。

## 2024 年 11 月 12 日

**常规变更**

- 为 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群添加暂停时长限制。

    TiDB Cloud Dedicated 现在限制最大暂停时长为 7 天。如果您未在 7 天内手动恢复集群，TiDB Cloud 将自动恢复它。

    此更改仅适用于**2024 年 11 月 12 日之后创建的组织**。在此日期或之前创建的组织将逐步过渡到新的暂停行为，并会事先收到通知。

    有关更多信息，请参阅 [暂停或恢复 TiDB Cloud Dedicated 集群](/tidb-cloud/pause-or-resume-tidb-cluster.md)。

- [Datadog 集成（beta）](/tidb-cloud/monitor-datadog-integration.md) 增加了对新区域的支持：`AP1`（日本）。

- 支持 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的一个新的 AWS 区域：`孟买 (ap-south-1)`。

- 移除对 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的 AWS `圣保罗 (sa-east-1)` 区域的支持。

## 2024 年 10 月 29 日

**常规变更**

- 新增指标：为 Prometheus 集成添加 `tidbcloud_changefeed_checkpoint_ts`。

    此指标跟踪 changefeed 的检查点时间戳，表示成功写入下游的最大 TSO（时间戳预言机）。 有关可用指标的更多信息，请参阅 [将 TiDB Cloud 与 Prometheus 和 Grafana 集成（Beta）](/tidb-cloud/monitor-prometheus-and-grafana-integration.md#metrics-available-to-prometheus)。

## 2024 年 10 月 22 日

**常规变更**

- 将新 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的默认 TiDB 版本从 [v7.5.3](https://docs.pingcap.com/tidb/v7.5/release-7.5.3) 升级到 [v7.5.4](https://docs.pingcap.com/tidb/v7.5/release-7.5.4)。

## 2024 年 10 月 15 日

**API 变更**

* [MSP](https://docs.pingcap.com/tidbcloud/api/v1beta1/msp) 自 2024 年 10 月 15 日起已弃用，并将在未来移除。如果您目前正在使用 MSP API，请迁移到 [TiDB Cloud Partner](https://partner-console.tidbcloud.com/signin) 中的 Partner Management API。

## 2024 年 9 月 24 日

**通用变更**

- 为在 AWS 上托管的 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群提供新的 [TiFlash vCPU 和 RAM 大小](/tidb-cloud/size-your-cluster.md#tiflash-vcpu-and-ram)：`32 vCPU, 128 GiB`

**CLI 变更**

- 发布 [TiDB Cloud CLI v1.0.0-beta.2](https://github.com/tidbcloud/tidbcloud-cli/releases/tag/v1.0.0-beta.2)。

    TiDB Cloud CLI 提供以下新功能：

    - 支持通过 [`ticloud serverless sql-user`](/tidb-cloud/ticloud-serverless-sql-user-create.md) 管理 [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群的 SQL 用户。
    - 允许在 [`ticloud serverless create`](/tidb-cloud/ticloud-cluster-create.md) 和 [`ticloud serverless update`](/tidb-cloud/ticloud-serverless-update.md) 中禁用 [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群的公共端点。
    - 添加 [`ticloud auth whoami`](/tidb-cloud/ticloud-auth-whoami.md) 命令，在使用 OAuth 身份验证时获取有关当前用户的信息。
    - 在 [`ticloud serverless export create`](/tidb-cloud/ticloud-serverless-export-create.md) 中支持 `--sql`、`--where` 和 `--filter` 标志，以灵活地选择源表。
    - 支持将数据导出到 CSV 和 Parquet 文件。
    - 支持使用角色 ARN 作为凭据将数据导出到 Amazon S3，并且还支持导出到 Google Cloud Storage 和 Azure Blob Storage。
    - 支持从 Amazon S3、Google Cloud Storage 和 Azure Blob Storage 导入数据。
    - 支持从分支和特定时间戳创建分支。

  TiDB Cloud CLI 增强了以下功能：

    - 改进调试日志记录。现在它可以记录凭据和 user-agent。
    - 将本地导出文件下载速度从每秒数十 KiB 提高到每秒数十 MiB。

  TiDB Cloud CLI 替换或删除了以下功能：

    - [`ticloud serverless export create`](/tidb-cloud/ticloud-serverless-export-create.md) 中的 `--s3.bucket-uri` 标志被 `--s3.uri` 替换。
    - [`ticloud serverless export create`](/tidb-cloud/ticloud-serverless-export-create.md) 中删除了 `--database` 和 `--table` 标志。相反，您可以使用 `--sql`、`--where` 和 `--filter` 标志。
    - [`ticloud serverless update`](/tidb-cloud/ticloud-serverless-update.md) 无法再更新 annotations 字段。

## 2024 年 9 月 10 日

**常规变更**

- 发布 TiDB Cloud 合作伙伴 Web 控制台和 Open API，以增强 TiDB Cloud 合作伙伴的资源和账单管理。

    通过 AWS Marketplace Channel Partner Private Offer (CPPO) 的托管服务提供商 (MSP) 和经销商现在可以利用 [TiDB Cloud 合作伙伴 Web 控制台](https://partner-console.tidbcloud.com/) 和 Open API 来简化他们的日常运营。

    有关更多信息，请参阅 [TiDB Cloud 合作伙伴 Web 控制台](/tidb-cloud/tidb-cloud-partners.md)。

## 2024 年 9 月 3 日

**控制台变更**

- 支持使用 [TiDB Cloud 控制台](https://tidbcloud.com/) 从 TiDB Cloud Serverless 集群导出数据。

    此前，TiDB Cloud 仅支持使用 [TiDB Cloud CLI](/tidb-cloud/cli-reference.md) 导出数据。现在，您可以轻松地将 TiDB Cloud Serverless 集群中的数据导出到本地文件和 Amazon S3，通过 [TiDB Cloud 控制台](https://tidbcloud.com/)。

    有关更多信息，请参阅 [从 TiDB Cloud Serverless 导出数据](/tidb-cloud/serverless-export.md) 和 [为 TiDB Cloud Serverless 配置外部存储访问](/tidb-cloud/serverless-external-storage.md)。

- 增强 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的连接体验。

    - 修改 **连接** 对话框界面，为 TiDB Cloud Dedicated 用户提供更精简高效的连接体验。
    - 引入新的集群级别 **网络** 页面，以简化集群的网络配置。
    - 将 **安全设置** 页面替换为新的 **密码设置** 页面，并将 IP 访问列表设置移至新的 **网络** 页面。

  有关更多信息，请参阅 [连接到 TiDB Cloud Dedicated](/tidb-cloud/connect-to-tidb-cluster.md)。

- 增强 [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 和 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的数据导入体验：

    - 使用更清晰的布局优化 **导入** 页面的布局。
    - 统一 TiDB Cloud Serverless 和 TiDB Cloud Dedicated 集群的导入步骤。
    - 简化 AWS Role ARN 创建过程，以便更轻松地进行连接设置。

  有关更多信息，请参阅 [从文件导入数据到 TiDB Cloud](/tidb-cloud/tidb-cloud-migration-overview.md#import-data-from-files-to-tidb-cloud)。

## 2024 年 8 月 20 日

**控制台变更**

- 优化了**创建私有终端节点连接**页面的布局，以改善在 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群中创建新的私有终端节点连接的用户体验。

    更多信息，请参考 [通过 AWS 私有终端节点连接到 TiDB Cloud Dedicated 集群](/tidb-cloud/set-up-private-endpoint-connections.md) 和 [通过 Google Cloud Private Service Connect 连接到 TiDB Cloud Dedicated 集群](/tidb-cloud/set-up-private-endpoint-connections-on-google-cloud.md)。

## 2024 年 8 月 6 日

**通用变更**

- [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 在 AWS 上负载均衡的计费变更。

    从 2024 年 8 月 1 日起，TiDB Cloud Dedicated 的账单将包含新的 AWS 公共 IPv4 地址费用，与 [AWS 自 2024 年 2 月 1 日起生效的定价变更](https://aws.amazon.com/blogs/aws/new-aws-public-ipv4-address-charge-public-ip-insights/)保持一致。 每个公共 IPv4 地址的费用为每小时 0.005 美元，这将导致每个托管在 AWS 上的 TiDB Cloud Dedicated 集群每月大约 10 美元。

    此费用将显示在您[账单详情](/tidb-cloud/tidb-cloud-billing.md#billing-details)中现有的 **TiDB Cloud Dedicated - 数据传输 - 负载均衡** 服务下。

- 将新的 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的默认 TiDB 版本从 [v7.5.2](https://docs.pingcap.com/tidb/v7.5/release-7.5.2) 升级到 [v7.5.3](https://docs.pingcap.com/tidb/v7.5/release-7.5.3)。

**控制台变更**

- 增强 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 的集群大小配置体验。

    优化 [**创建集群**](/tidb-cloud/create-tidb-cluster.md) 和 [**修改集群**](/tidb-cloud/scale-tidb-cluster.md) 页面上 TiDB Cloud Dedicated 集群的 **集群大小** 部分的布局。 此外，**集群大小** 部分现在包含指向节点大小推荐文档的链接，这有助于您选择合适的集群大小。

## 2024 年 7 月 23 日

**常规变更**

- [数据服务（beta）](https://tidbcloud.com/project/data-service) 支持自动生成向量搜索端点。

    如果您的表包含[向量数据类型](/tidb-cloud/vector-search-data-types.md)，您可以自动生成一个向量搜索端点，该端点会根据您选择的距离函数计算向量距离。

    此功能实现了与 AI 平台（例如 [Dify](https://docs.dify.ai/guides/tools) 和 [GPTs](https://openai.com/blog/introducing-gpts)）的无缝集成，通过先进的自然语言处理和 AI 功能增强您的应用程序，从而实现更复杂的任务和智能解决方案。

    有关更多信息，请参阅[自动生成端点](/tidb-cloud/data-service-manage-endpoint.md#generate-an-endpoint-automatically)和[将数据应用与第三方工具集成](/tidb-cloud/data-service-integrations.md)。

- 引入预算功能，帮助您跟踪 TiDB Cloud 的实际成本与计划支出，防止意外成本。

    要访问此功能，您必须是您组织的 `Organization Owner` 或 `Organization Billing Admin` 角色。

    有关更多信息，请参阅[管理 TiDB Cloud 的预算](/tidb-cloud/tidb-cloud-budget.md)。

## 2024 年 7 月 9 日

**通用变更**

- 增强了[系统状态](https://status.tidbcloud.com/)页面，以提供对 TiDB Cloud 系统健康和性能的更好洞察。

    要访问它，请直接访问 <https://status.tidbcloud.com/>，或者通过 [TiDB Cloud 控制台](https://tidbcloud.com) 导航，方法是单击右下角的 **?** 并选择 **系统状态**。

**控制台变更**

- 优化了 **VPC 对等连接** 页面布局，以改善在 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群中[创建 VPC 对等连接](/tidb-cloud/set-up-vpc-peering-connections.md)的用户体验。

## 2024 年 7 月 2 日

**通用变更**

- [数据服务（beta）](https://tidbcloud.com/project/data-service) 提供了一个端点库，其中包含预定义的系统端点，您可以直接将其添加到您的数据应用中，从而减少端点开发的工作量。

    目前，该库仅包含 `/system/query` 端点，您只需在预定义的 `sql` 参数中传递 SQL 语句即可执行任何 SQL 语句。 此端点有助于立即执行 SQL 查询，从而提高灵活性和效率。

    有关更多信息，请参阅 [添加预定义的系统端点](/tidb-cloud/data-service-manage-endpoint.md#add-a-predefined-system-endpoint)。

- 增强慢查询数据存储。

    [TiDB Cloud 控制台](https://tidbcloud.com)上的慢查询访问现在更加稳定，并且不会影响数据库性能。

## 2024 年 6 月 25 日

**通用变更**

- [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 支持向量搜索（beta）。

    向量搜索（beta）功能提供了一种高级搜索解决方案，用于跨各种数据类型（包括文档、图像、音频和视频）执行语义相似性搜索。 此功能使开发人员能够使用熟悉的 MySQL 技能轻松构建具有生成式人工智能 (AI) 功能的可扩展应用程序。 主要功能包括：

    - [向量数据类型](/tidb-cloud/vector-search-data-types.md)、[向量索引](/tidb-cloud/vector-search-index.md) 和 [向量函数和运算符](/tidb-cloud/vector-search-functions-and-operators.md)。
    - 与 [LangChain](/tidb-cloud/vector-search-integrate-with-langchain.md)、[LlamaIndex](/tidb-cloud/vector-search-integrate-with-llamaindex.md) 和 [JinaAI](/tidb-cloud/vector-search-integrate-with-jinaai-embedding.md) 的生态系统集成。
    - Python 的编程语言支持：[SQLAlchemy](/tidb-cloud/vector-search-integrate-with-sqlalchemy.md)、[Peewee](/tidb-cloud/vector-search-integrate-with-peewee.md) 和 [Django ORM](/tidb-cloud/vector-search-integrate-with-django-orm.md)。
    - 示例应用程序和教程：使用 [Python](/tidb-cloud/vector-search-get-started-using-python.md) 或 [SQL](/tidb-cloud/vector-search-get-started-using-sql.md) 对文档执行语义搜索。

  有关更多信息，请参阅 [向量搜索（beta）概述](/tidb-cloud/vector-search-overview.md)。

- [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 现在为组织所有者提供每周电子邮件报告。

    这些报告提供了有关集群性能和活动的见解。 通过接收自动每周更新，您可以随时了解集群的信息，并做出数据驱动的决策来优化集群。

- 发布 Chat2Query API v3 端点并弃用 Chat2Query API v1 端点 `/v1/chat2data`。

    使用 Chat2Query API v3 端点，您可以使用会话启动多轮 Chat2Query。

    有关更多信息，请参阅 [Chat2Query API 入门](/tidb-cloud/use-chat2query-api.md)。

**控制台变更**

- 将 Chat2Query（beta）重命名为 SQL Editor（beta）。

    先前称为 Chat2Query 的界面已重命名为 SQL Editor。 此更改阐明了手动 SQL 编辑和 AI 辅助查询生成之间的区别，从而增强了可用性和您的整体体验。

    - **SQL Editor**：用于在 TiDB Cloud 控制台中手动编写和执行 SQL 查询的默认界面。
    - **Chat2Query**：AI 辅助的文本到查询功能，使您能够使用自然语言与数据库进行交互，以生成、重写和优化 SQL 查询。

  有关更多信息，请参阅 [使用 AI 辅助的 SQL Editor 探索您的数据](/tidb-cloud/explore-data-with-chat2query.md)。

## 2024 年 6 月 18 日

**常规变更**

- 将 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的 16 vCPU TiFlash 和 32 vCPU TiFlash 的最大节点存储从 2048 GiB 增加到 4096 GiB。

    此增强功能提高了 TiDB Cloud Dedicated 集群的分析数据存储容量，提高了工作负载的扩展效率，并满足了不断增长的数据需求。

    有关更多信息，请参阅 [TiFlash 节点存储](/tidb-cloud/size-your-cluster.md#tiflash-node-storage)。

- 将新的 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的默认 TiDB 版本从 [v7.5.1](https://docs.pingcap.com/tidb/v7.5/release-7.5.1) 升级到 [v7.5.2](https://docs.pingcap.com/tidb/v7.5/release-7.5.2)。

## 2024 年 6 月 4 日

**通用变更**

- 推出恢复组功能（beta），用于在 AWS 上部署的 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的灾难恢复。

    此功能使您能够在 TiDB Cloud Dedicated 集群之间复制数据库，从而确保在发生区域性灾难时快速恢复。如果您具有 `Project Owner` 角色，则可以通过创建新的恢复组并将数据库分配给该组来启用此功能。通过使用恢复组复制数据库，您可以提高灾难准备能力，满足更严格的可用性 SLA，并实现更积极的恢复点目标 (RPO) 和恢复时间目标 (RTO)。

    有关更多信息，请参阅 [恢复组入门](/tidb-cloud/recovery-group-get-started.md)。

- 推出 [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 列式存储 [TiFlash](/tiflash/tiflash-overview.md) 的计费和计量（beta）。

    在 2024 年 6 月 30 日之前，TiDB Cloud Serverless 集群中的列式存储仍然免费，享受 100% 的折扣。在此日期之后，每个 TiDB Cloud Serverless 集群将包含 5 GiB 的免费列式存储配额。超出免费配额的使用将收费。

    有关更多信息，请参阅 [TiDB Cloud Serverless 定价详情](https://www.pingcap.com/tidb-serverless-pricing-details/#storage)。

- [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 支持 [生存时间 (TTL)](/time-to-live.md)。

## 2024 年 5 月 28 日

**常规变更**

- Google Cloud `台湾 (asia-east1)` 区域支持 [数据迁移](/tidb-cloud/migrate-from-mysql-using-data-migration.md) 功能。

    托管在 Google Cloud `台湾 (asia-east1)` 区域的 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群现在支持数据迁移 (DM) 功能。如果您的上游数据存储在该区域或附近，您现在可以利用更快、更可靠的数据迁移，从 Google Cloud 迁移到 TiDB Cloud。

- 为托管在 AWS 和 Google Cloud 上的 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群提供新的 [TiDB 节点大小](/tidb-cloud/size-your-cluster.md#tidb-vcpu-and-ram)：`16 vCPU, 64 GiB`

**API 变更**

- 引入 TiDB Cloud Data Service API，用于自动高效地管理以下资源：

    * **Data App (数据应用)**：一组端点，您可以使用这些端点来访问特定应用程序的数据。
    * **Data Source (数据源)**：链接到数据应用以进行数据操作和检索的集群。
    * **Endpoint (端点)**：一个 Web API，您可以自定义它来执行 SQL 语句。
    * **Data API Key (数据 API 密钥)**：用于安全地访问端点。
    * **OpenAPI Specification (OpenAPI 规范)**：Data Service 支持为每个数据应用生成 OpenAPI 规范 3.0，使您能够以标准化格式与您的端点进行交互。

  这些 TiDB Cloud Data Service API 端点在 TiDB Cloud API v1beta1 中发布，这是 TiDB Cloud 的最新 API 版本。

    有关更多信息，请参阅 [API 文档 (v1beta1)](https://docs.pingcap.com/tidbcloud/api/v1beta1/dataservice)。

## 2024 年 5 月 21 日

**常规变更**

- 为在 Google Cloud 上托管的 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群提供一个新的 [TiDB 节点大小](/tidb-cloud/size-your-cluster.md#tidb-vcpu-and-ram)：`8 vCPU, 16 GiB`

## 2024 年 5 月 14 日

**通用变更**

- 扩展了[**时区**](/tidb-cloud/manage-user-access.md#set-the-time-zone-for-your-organization)部分中的时区选择，以更好地适应来自不同地区的客户。

- 支持[创建VPC对等连接](/tidb-cloud/set-up-vpc-peering-connections.md)，即使您的VPC与TiDB Cloud的VPC位于不同的区域。

- [数据服务 (beta)](https://tidbcloud.com/project/data-service) 除了查询参数外，还支持路径参数。

    此功能通过结构化 URL 增强了资源识别，并改善了用户体验、搜索引擎优化 (SEO) 和客户端集成，为开发人员提供了更大的灵活性和与行业标准的更好对齐。

    有关更多信息，请参阅[基本属性](/tidb-cloud/data-service-manage-endpoint.md#basic-properties)。

## 2024 年 4 月 16 日

**CLI 变更**

- 推出 [TiDB Cloud CLI 1.0.0-beta.1](https://github.com/tidbcloud/tidbcloud-cli)，构建于新的 [TiDB Cloud API](/tidb-cloud/api-overview.md) 之上。 新的 CLI 带来了以下新功能：

    - [从 TiDB Cloud Serverless 集群导出数据](/tidb-cloud/serverless-export.md)
    - [将本地存储中的数据导入到 TiDB Cloud Serverless 集群](/tidb-cloud/ticloud-import-start.md)
    - [通过 OAuth 认证](/tidb-cloud/ticloud-auth-login.md)
    - [通过 TiDB Bot 提问](/tidb-cloud/ticloud-ai.md)

  在升级您的 TiDB Cloud CLI 之前，请注意这个新的 CLI 与之前的版本不兼容。 例如，CLI 命令中的 `ticloud cluster` 现在更新为 `ticloud serverless`。 更多信息，请参阅 [TiDB Cloud CLI 参考](/tidb-cloud/cli-reference.md)。

## 2024 年 4 月 9 日

**通用变更**

- 为托管在 AWS 上的 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群提供一个新的 [TiDB 节点大小](/tidb-cloud/size-your-cluster.md#tidb-vcpu-and-ram): `8 vCPU, 32 GiB`。

## 2024 年 4 月 2 日

**通用变更**

- 为 [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群引入两种服务计划：**免费** 和 **可扩展**。

    为了满足不同的用户需求，TiDB Cloud Serverless 提供免费和可扩展的服务计划。无论您是刚开始使用还是扩展以满足不断增长的应用程序需求，这些计划都能提供您需要的灵活性和功能。

    更多信息，请参阅 [集群计划](/tidb-cloud/select-cluster-tier.md#cluster-plans)。

- 修改 TiDB Cloud Serverless 集群达到其使用配额时的限流行为。现在，一旦集群达到其使用配额，它会立即拒绝任何新的连接尝试，从而确保现有操作的不间断服务。

    更多信息，请参阅 [使用配额](/tidb-cloud/serverless-limitations.md#usage-quota)。

## 2024 年 3 月 5 日

**通用变更**

- 将新 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的默认 TiDB 版本从 [v7.5.0](https://docs.pingcap.com/tidb/v7.5/release-7.5.0) 升级到 [v7.5.1](https://docs.pingcap.com/tidb/v7.5/release-7.5.1)。

**控制台变更**

- 在 [**账单**](https://tidbcloud.com/org-settings/billing/payments) 页面引入 **成本探索器** 标签，该标签提供了一个直观的界面，用于分析和自定义您组织随时间的成本报告。

    要使用此功能，请导航到您组织的 **账单** 页面，然后单击 **成本探索器** 标签。

    有关更多信息，请参见 [成本探索器](/tidb-cloud/tidb-cloud-billing.md#cost-explorer)。

- [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 为 [节点级资源指标](/tidb-cloud/built-in-monitoring.md#server) 显示 **limit** 标签。

    **limit** 标签显示集群中每个组件的 CPU、内存和存储等资源的最大使用量。此增强功能简化了监控集群资源使用率的过程。

    要访问这些指标限制，请导航到集群的 **监控** 页面，然后查看 **指标** 选项卡下的 **服务器** 类别。

    有关更多信息，请参见 [TiDB Cloud Dedicated 集群的指标](/tidb-cloud/built-in-monitoring.md#server)。

## 2024 年 2 月 21 日

**常规变更**

- 将 [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群的 TiDB 版本从 [v6.6.0](https://docs.pingcap.com/tidb/v6.6/release-6.6.0) 升级到 [v7.1.3](https://docs.pingcap.com/tidb/v7.1/release-7.1.3)。

## 2024 年 2 月 20 日

**通用变更**

- 支持在 Google Cloud 上创建更多 TiDB Cloud 节点。

    - 通过为 Google Cloud [配置区域 CIDR 大小](/tidb-cloud/set-up-vpc-peering-connections.md#prerequisite-set-a-cidr-for-a-region) 为 `/19`，您现在可以在项目的任何区域内创建最多 124 个 TiDB Cloud 节点。
    - 如果您想在项目的任何区域中创建超过 124 个节点，您可以联系 [TiDB Cloud 支持](/tidb-cloud/tidb-cloud-support.md)，以获得定制 IP 范围大小（范围从 `/16` 到 `/18`）的帮助。

## 2024 年 1 月 23 日

**常规变更**

- 为 TiDB、TiKV 和 TiFlash 添加 32 vCPU 作为节点大小选项。

    对于每个 `32 vCPU, 128 GiB` 的 TiKV 节点，节点存储范围从 200 GiB 到 6144 GiB。

    建议在以下场景中使用此类节点：

    - 高负载生产环境
    - 极高性能

## 2024 年 1 月 16 日

**常规变更**

- 增强了项目的 CIDR 配置。

    - 您可以直接为每个项目设置区域级别的 CIDR。
    - 您可以从更广泛的 CIDR 值范围中选择您的 CIDR 配置。

    注意：先前项目的全局级别 CIDR 设置已停用，但所有处于活动状态的现有区域 CIDR 均不受影响。现有集群的网络不会受到影响。

    有关更多信息，请参阅[为区域设置 CIDR](/tidb-cloud/set-up-vpc-peering-connections.md#prerequisite-set-a-cidr-for-a-region)。

- TiDB Cloud Serverless 用户现在可以禁用集群的公共端点。

    有关更多信息，请参阅[禁用公共端点](/tidb-cloud/connect-via-standard-connection-serverless.md#disable-a-public-endpoint)。

- [数据服务 (beta)](https://tidbcloud.com/project/data-service) 支持配置自定义域名以访问数据应用中的端点。

    默认情况下，TiDB Cloud 数据服务提供域名 `<region>.data.tidbcloud.com` 以访问每个数据应用的端点。为了增强个性化和灵活性，您现在可以为您的数据应用配置自定义域名，而不是使用默认域名。此功能使您能够为您的数据库服务使用品牌 URL 并增强安全性。

    有关更多信息，请参阅[数据服务中的自定义域名](/tidb-cloud/data-service-custom-domain.md)。

## 2024 年 1 月 3 日

**常规变更**

- 支持[组织单点登录 (SSO)](https://tidbcloud.com/org-settings/authentication)，以简化企业身份验证流程。

    借助此功能，您可以使用[安全断言标记语言 (SAML)](https://en.wikipedia.org/wiki/Security_Assertion_Markup_Language) 或 [OpenID Connect (OIDC)](https://openid.net/developers/how-connect-works/) 将 TiDB Cloud 与任何身份提供商 (IdP) 无缝集成。

    有关更多信息，请参阅[组织单点登录身份验证](/tidb-cloud/tidb-cloud-org-sso-authentication.md)。

- 将新 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的默认 TiDB 版本从 [v7.1.1](https://docs.pingcap.com/tidb/v7.1/release-7.1.1) 升级到 [v7.5.0](https://docs.pingcap.com/tidb/v7.5/release-7.5.0)。

- [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 的双区域备份功能现已正式发布 (GA)。

    通过使用此功能，您可以在 AWS 或 Google Cloud 内的地理区域之间复制备份。 此功能提供了额外的数据保护层和灾难恢复能力。

    有关更多信息，请参阅[双区域备份](/tidb-cloud/backup-and-restore.md#turn-on-dual-region-backup)。