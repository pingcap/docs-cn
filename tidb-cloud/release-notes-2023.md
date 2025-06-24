---
title: 2023 年 TiDB Cloud 发布说明
summary: 了解 2023 年 TiDB Cloud 的发布说明。
---

# 2023 年 TiDB Cloud 发布说明

本页列出了 2023 年 [TiDB Cloud](https://www.pingcap.com/tidb-cloud/) 的发布说明。

## 2023 年 12 月 5 日

**常规变更**

- [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 允许您恢复失败的 Changefeed，从而节省您重新创建 Changefeed 的精力。

    更多信息，请参见 [Changefeed 状态](/tidb-cloud/changefeed-overview.md#changefeed-states)。

**控制台变更**

- 增强 [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 的连接体验。

    优化 **连接** 对话框界面，为 TiDB Cloud Serverless 用户提供更流畅、更高效的连接体验。 此外，TiDB Cloud Serverless 引入了更多客户端类型，并允许您选择所需的连接分支。

    更多信息，请参见 [连接到 TiDB Cloud Serverless](/tidb-cloud/connect-via-standard-connection-serverless.md)。

## 2023 年 11 月 28 日

**常规变更**

- [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 支持从备份恢复 SQL 绑定。

    TiDB Cloud Dedicated 现在默认在从备份恢复时恢复用户帐户和 SQL 绑定。此增强功能适用于 v6.2.0 或更高版本的集群，从而简化了数据恢复过程。SQL 绑定的恢复确保了与查询相关的配置和优化的顺利重新集成，为您提供更全面、更高效的恢复体验。

    有关更多信息，请参阅[备份和恢复 TiDB Cloud Dedicated 数据](/tidb-cloud/backup-and-restore.md)。

**控制台变更**

- [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 支持监控 SQL 语句 RU 成本。

    TiDB Cloud Serverless 现在提供有关每个 SQL 语句的[请求单元 (RU)](/tidb-cloud/tidb-cloud-glossary.md#request-unit)的详细信息。您可以查看每个 SQL 语句的**总 RU** 和**平均 RU** 成本。此功能可帮助您识别和分析 RU 成本，从而为您的运营提供潜在的成本节省机会。

    要查看您的 SQL 语句 RU 详细信息，请导航到[您的 TiDB Cloud Serverless 集群](https://tidbcloud.com/project/clusters)的**诊断**页面，然后单击 **SQL 语句**选项卡。

## 2023 年 11 月 21 日

**常规变更**

- [数据迁移](/tidb-cloud/migrate-from-mysql-using-data-migration.md) 支持在 Google Cloud 上部署的 TiDB 集群的高速物理模式。

    现在，您可以对部署在 AWS 和 Google Cloud 上的 TiDB 集群使用物理模式。物理模式的迁移速度最高可达 110 MiB/s，比逻辑模式快 2.4 倍。改进后的性能适用于将大型数据集快速迁移到 TiDB Cloud。

    有关更多信息，请参阅[迁移现有数据和增量数据](/tidb-cloud/migrate-from-mysql-using-data-migration.md#migrate-existing-data-and-incremental-data)。

## 2023 年 11 月 14 日

**常规变更**

- 当您从 TiDB Cloud Dedicated 集群恢复数据时，默认行为现在从不恢复用户帐户修改为恢复所有用户帐户。

    更多信息，请参阅 [备份和恢复 TiDB Cloud Dedicated 数据](/tidb-cloud/backup-and-restore.md)。

- 引入 changefeed 的事件过滤器。

    此增强功能使您能够通过 [TiDB Cloud 控制台](https://tidbcloud.com/) 轻松管理 changefeed 的事件过滤器，从而简化了从 changefeed 中排除特定事件的过程，并更好地控制下游数据复制。

    更多信息，请参阅 [Changefeed](/tidb-cloud/changefeed-overview.md#edit-a-changefeed)。

## 2023 年 11 月 7 日

**常规变更**

- 添加以下资源使用率警报。 默认情况下，新警报处于禁用状态。 您可以根据需要启用它们。

    - TiDB 节点的最大内存利用率在 10 分钟内超过 70%
    - TiKV 节点的最大内存利用率在 10 分钟内超过 70%
    - TiDB 节点的最大 CPU 利用率在 10 分钟内超过 80%
    - TiKV 节点的最大 CPU 利用率在 10 分钟内超过 80%

  有关更多信息，请参阅 [TiDB Cloud 内置警报](/tidb-cloud/monitor-built-in-alerting.md#resource-usage-alerts)。

## 2023 年 10 月 31 日

**常规变更**

- 支持在 TiDB Cloud 控制台中直接升级到企业支持计划，无需联系销售。

    更多信息，请参见 [TiDB Cloud 支持](/tidb-cloud/tidb-cloud-support.md)。

## 2023 年 10 月 25 日

**常规变更**

- [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 支持 Google Cloud 上的双区域备份（beta）。

    托管在 Google Cloud 上的 TiDB Cloud Dedicated 集群可以与 Google Cloud Storage 无缝协作。 与 Google Cloud Storage 的 [双区域](https://cloud.google.com/storage/docs/locations#location-dr) 功能类似，您在 TiDB Cloud Dedicated 中用于双区域的区域对必须位于同一多区域内。 例如，东京和大阪位于同一多区域 `ASIA` 中，因此它们可以一起用于双区域存储。

    有关更多信息，请参阅 [备份和恢复 TiDB Cloud Dedicated 数据](/tidb-cloud/backup-and-restore.md#turn-on-dual-region-backup)。

- [将数据变更日志流式传输到 Apache Kafka](/tidb-cloud/changefeed-sink-to-apache-kafka.md) 的功能现已正式发布 (GA)。

    经过 10 个月的成功 Beta 试用后，将数据变更日志从 TiDB Cloud 流式传输到 Apache Kafka 的功能已正式发布。 将数据从 TiDB 流式传输到消息队列是数据集成场景中的常见需求。 您可以使用 Kafka sink 与其他数据处理系统（例如 Snowflake）集成或支持业务消费。

    有关更多信息，请参阅 [Changefeed 概述](/tidb-cloud/changefeed-overview.md)。

## 2023 年 10 月 11 日

**常规变更**

- 支持 [双区域备份 (beta)](/tidb-cloud/backup-and-restore.md#turn-on-dual-region-backup)，适用于部署在 AWS 上的 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群。

    您现在可以在云提供商内的地理区域之间复制备份。此功能提供了一个额外的数据保护层和灾难恢复能力。

    更多信息，请参阅 [备份和恢复 TiDB Cloud Dedicated 数据](/tidb-cloud/backup-and-restore.md)。

- 数据迁移现在支持物理模式和逻辑模式来迁移现有数据。

    在物理模式下，迁移速度可以达到 110 MiB/s。与逻辑模式下的 45 MiB/s 相比，迁移性能得到了显着提高。

    更多信息，请参阅 [迁移现有数据和增量数据](/tidb-cloud/migrate-from-mysql-using-data-migration.md#migrate-existing-data-and-incremental-data)。

## 2023 年 10 月 10 日

**常规变更**

- 支持在 [Vercel 预览部署](https://vercel.com/docs/deployments/preview-deployments) 中使用 TiDB Cloud Serverless 分支，通过 TiDB Cloud Vercel 集成。

    更多信息，请参考 [连接 TiDB Cloud Serverless 分支](/tidb-cloud/integrate-tidbcloud-with-vercel.md#connect-with-tidb-cloud-serverless-branching)。

## 2023 年 9 月 28 日

**API 变更**

- 引入 TiDB Cloud 账单 API 端点，用于检索特定组织在给定月份的账单。

    此账单 API 端点在 TiDB Cloud API v1beta1 中发布，这是 TiDB Cloud 的最新 API 版本。 有关更多信息，请参阅 [API 文档 (v1beta1)](https://docs.pingcap.com/tidbcloud/api/v1beta1#tag/Billing)。

## 2023 年 9 月 19 日

**常规变更**

- 从 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群中移除 2 vCPU 的 TiDB 和 TiKV 节点。

    **创建集群**页面或**修改集群**页面不再提供 2 vCPU 选项。

- 发布适用于 JavaScript 的 [TiDB Cloud serverless driver (beta)](/tidb-cloud/serverless-driver.md)。

    适用于 JavaScript 的 TiDB Cloud serverless driver 允许您通过 HTTPS 连接到您的 [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群。 它在 TCP 连接受限的边缘环境中特别有用，例如 [Vercel Edge Function](https://vercel.com/docs/functions/edge-functions) 和 [Cloudflare Workers](https://workers.cloudflare.com/)。

    有关更多信息，请参阅 [TiDB Cloud serverless driver (beta)](/tidb-cloud/serverless-driver.md)。

**控制台变更**

- 对于 [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群，您可以在**本月用量**面板中或设置消费限额时获得成本估算。

## 2023 年 9 月 5 日

**常规变更**

- [数据服务 (beta)](https://tidbcloud.com/project/data-service) 支持为每个 API 密钥自定义速率限制，以满足不同情况下的特定速率限制要求。

    您可以在[创建](/tidb-cloud/data-service-api-key.md#create-an-api-key)或[编辑](/tidb-cloud/data-service-api-key.md#edit-an-api-key)密钥时调整 API 密钥的速率限制。

    有关更多信息，请参见[速率限制](/tidb-cloud/data-service-api-key.md#rate-limiting)。

- 支持 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的新 AWS 区域：圣保罗 (sa-east-1)。

- 支持为每个 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的 IP 访问列表添加最多 100 个 IP 地址。

    有关更多信息，请参见[配置 IP 访问列表](/tidb-cloud/configure-ip-access-list.md)。

**控制台变更**

- 为 [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群引入 **Events** 页面，该页面提供集群主要变更的记录。

    在此页面上，您可以查看过去 7 天的事件历史记录，并跟踪重要详细信息，例如触发时间和发起操作的用户。

    有关更多信息，请参见 [TiDB Cloud 集群事件](/tidb-cloud/tidb-cloud-events.md)。

**API 变更**

- 发布多个 TiDB Cloud API 端点，用于管理 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的 [AWS PrivateLink](https://aws.amazon.com/privatelink/?privatelink-blogs.sort-by=item.additionalFields.createdDate&privatelink-blogs.sort-order=desc) 或 [Google Cloud Private Service Connect](https://cloud.google.com/vpc/docs/private-service-connect)：

    - 为集群创建私有端点服务
    - 检索集群的私有端点服务信息
    - 为集群创建私有端点
    - 列出集群的所有私有端点
    - 列出项目中的所有私有端点
    - 删除集群的私有端点

  有关更多信息，请参阅 [API 文档](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster)。

## 2023 年 8 月 23 日

**常规变更**

- 支持 Google Cloud [Private Service Connect](https://cloud.google.com/vpc/docs/private-service-connect)，用于 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群。

    现在，您可以创建一个私有端点，并与托管在 Google Cloud 上的 TiDB Cloud Dedicated 集群建立安全连接。

    主要优势：

    - 直观的操作：只需几个步骤即可帮助您创建私有端点。
    - 增强的安全性：建立安全连接以保护您的数据。
    - 改进的性能：提供低延迟和高带宽的连接。

  有关更多信息，请参见 [通过 Google Cloud 上的私有端点连接](/tidb-cloud/set-up-private-endpoint-connections-on-google-cloud.md)。

- 支持使用 Changefeed 将数据从 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群流式传输到 [Google Cloud Storage (GCS)](https://cloud.google.com/storage)。

    现在，您可以使用自己的帐户的存储桶并提供精确定制的权限，将数据从 TiDB Cloud 流式传输到 GCS。 将数据复制到 GCS 后，您可以根据需要分析数据中的更改。

    有关更多信息，请参见 [Sink to Cloud Storage](/tidb-cloud/changefeed-sink-to-cloud-storage.md)。

## 2023 年 8 月 15 日

**常规变更**

- [数据服务（beta）](https://tidbcloud.com/project/data-service) 支持对 `GET` 请求进行分页，以改善开发体验。

    对于 `GET` 请求，您可以通过在**高级属性**中启用**分页**，并在调用端点时将 `page` 和 `page_size` 指定为查询参数来对结果进行分页。 例如，要获取每页 10 个项目的第二页，您可以使用以下命令：

    ```bash
    curl --digest --user '<Public Key>:<Private Key>' \
      --request GET 'https://<region>.data.tidbcloud.com/api/v1beta/app/<App ID>/endpoint/<Endpoint Path>?page=2&page_size=10'
    ```

    请注意，此功能仅适用于最后一个查询是 `SELECT` 语句的 `GET` 请求。

    有关更多信息，请参见 [调用端点](/tidb-cloud/data-service-manage-endpoint.md#call-an-endpoint)。

- [数据服务（beta）](https://tidbcloud.com/project/data-service) 支持缓存 `GET` 请求的端点响应，并指定生存时间 (TTL)。

    此功能可降低数据库负载并优化端点延迟。

    对于使用 `GET` 请求方法的端点，您可以启用**缓存响应**并在**高级属性**中配置缓存的 TTL 期限。

    有关更多信息，请参见 [高级属性](/tidb-cloud/data-service-manage-endpoint.md#advanced-properties)。

- 禁用为在 AWS 上托管并在 2023 年 8 月 15 日之后创建的 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群进行的负载均衡改进，包括：

    - 当您横向扩展在 AWS 上托管的 TiDB 节点时，禁用自动将现有连接迁移到新的 TiDB 节点。
    - 当您横向缩减在 AWS 上托管的 TiDB 节点时，禁用自动将现有连接迁移到可用的 TiDB 节点。

  此更改避免了混合部署的资源争用，并且不会影响已启用此改进的现有集群。 如果您想为新集群启用负载均衡改进，请联系 [TiDB Cloud 支持](/tidb-cloud/tidb-cloud-support.md)。

## 2023 年 8 月 8 日

**常规变更**

- [数据服务 (beta)](https://tidbcloud.com/project/data-service) 现在支持基本身份验证。

    您可以在请求中使用 ['Basic' HTTP 身份验证](https://datatracker.ietf.org/doc/html/rfc7617)，并将您的公钥作为用户名，私钥作为密码提供。 与摘要身份验证相比，基本身份验证更简单，可以在调用数据服务端点时实现更直接的用法。

    有关更多信息，请参阅 [调用端点](/tidb-cloud/data-service-manage-endpoint.md#call-an-endpoint)。

## 2023 年 8 月 1 日

**常规变更**

- 支持 TiDB Cloud 中数据应用的 OpenAPI 规范 [数据服务](https://tidbcloud.com/project/data-service)。

    TiDB Cloud 数据服务为每个数据应用提供自动生成的 OpenAPI 文档。 在文档中，您可以查看端点、参数和响应，并试用这些端点。

    您还可以下载 YAML 或 JSON 格式的数据应用及其已部署端点的 OpenAPI 规范 (OAS)。 OAS 提供标准化的 API 文档、简化的集成和简单的代码生成，从而实现更快的开发和改进的协作。

    有关更多信息，请参阅 [使用 OpenAPI 规范](/tidb-cloud/data-service-manage-data-app.md#use-the-openapi-specification) 和 [将 OpenAPI 规范与 Next.js 结合使用](/tidb-cloud/data-service-oas-with-nextjs.md)。

- 支持在 [Postman](https://www.postman.com/) 中运行数据应用。

    Postman 集成使您能够将数据应用的端点作为集合导入到您首选的工作区中。 然后，您可以受益于增强的协作和无缝的 API 测试，并支持 Postman Web 和桌面应用程序。

    有关更多信息，请参阅 [在 Postman 中运行数据应用](/tidb-cloud/data-service-postman-integration.md)。

- 为 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群引入新的 **暂停中** 状态，允许以经济高效的方式暂停，在此期间不收取任何费用。

    当您单击 TiDB Cloud Dedicated 集群的**暂停**时，该集群将首先进入**暂停中**状态。 暂停操作完成后，集群状态将转换为**已暂停**。

    只有在集群状态转换为**已暂停**后才能恢复集群，这解决了因快速单击**暂停**和**恢复**而导致的异常恢复问题。

    有关更多信息，请参阅 [暂停或恢复 TiDB Cloud Dedicated 集群](/tidb-cloud/pause-or-resume-tidb-cluster.md)。

## 2023 年 7 月 26 日

**常规变更**

- 在 TiDB Cloud [数据服务](https://tidbcloud.com/project/data-service) 中引入一项强大的功能：自动端点生成。

    开发者现在可以轻松地通过最少的点击和配置来创建 HTTP 端点。 消除重复的样板代码，简化并加速端点创建，并减少潜在的错误。

    有关如何使用此功能的更多信息，请参见 [自动生成端点](/tidb-cloud/data-service-manage-endpoint.md#generate-an-endpoint-automatically)。

- 支持 TiDB Cloud [数据服务](https://tidbcloud.com/project/data-service) 中端点的 `PUT` 和 `DELETE` 请求方法。

    - 使用 `PUT` 方法更新或修改数据，类似于 `UPDATE` 语句。
    - 使用 `DELETE` 方法删除数据，类似于 `DELETE` 语句。

  有关更多信息，请参见 [配置属性](/tidb-cloud/data-service-manage-endpoint.md#configure-properties)。

- 支持 TiDB Cloud [数据服务](https://tidbcloud.com/project/data-service) 中 `POST`、`PUT` 和 `DELETE` 请求方法的**批量操作**。

    当为端点启用**批量操作**时，你将能够在单个请求中对多行执行操作。 例如，你可以使用单个 `POST` 请求插入多行数据。

    有关更多信息，请参见 [高级属性](/tidb-cloud/data-service-manage-endpoint.md#advanced-properties)。

## 2023 年 7 月 25 日

**常规变更**

- 将新的 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的默认 TiDB 版本从 [v6.5.3](https://docs.pingcap.com/tidb/v6.5/release-6.5.3) 升级到 [v7.1.1](https://docs.pingcap.com/tidb/v7.1/release-7.1.1)。

**控制台变更**

- 通过优化支持条目，简化 TiDB Cloud 用户对 PingCAP 支持的访问。改进包括：

    - 在左下角的 <MDSvgIcon name="icon-top-organization" /> 中添加 **支持** 入口。
    - 改进 [TiDB Cloud 控制台](https://tidbcloud.com/) 右下角的 **?** 图标的菜单，使其更直观。

  更多信息，请参阅 [TiDB Cloud 支持](/tidb-cloud/tidb-cloud-support.md)。

## 2023 年 7 月 18 日

**常规变更**

- 优化了组织级别和项目级别的基于角色的访问控制，使您可以向用户授予具有最低权限的角色，从而提高安全性、合规性和生产力。

    - 组织角色包括 `Organization Owner`、`Organization Billing Admin`、`Organization Console Audit Admin` 和 `Organization Member`。
    - 项目角色包括 `Project Owner`、`Project Data Access Read-Write` 和 `Project Data Access Read-Only`。
    - 要管理项目中的集群（例如集群创建、修改和删除），您需要担任 `Organization Owner` 或 `Project Owner` 角色。

  有关不同角色的权限的更多信息，请参阅 [用户角色](/tidb-cloud/manage-user-access.md#user-roles)。

- 支持用于在 AWS 上托管的 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的客户管理的加密密钥 (CMEK) 功能（beta）。

    您可以创建基于 AWS KMS 的 CMEK，以直接从 TiDB Cloud 控制台加密存储在 EBS 和 S3 中的数据。这确保了客户数据使用客户管理的密钥进行加密，从而增强了安全性。

    请注意，此功能仍有局限性，仅应要求提供。要申请此功能，请联系 [TiDB Cloud 支持](/tidb-cloud/tidb-cloud-support.md)。

- 优化 TiDB Cloud 中的导入功能，旨在增强数据导入体验。已进行以下改进：

    - 统一 TiDB Cloud Serverless 的导入入口：整合了导入数据的入口，使您可以无缝地在导入本地文件和从 Amazon S3 导入文件之间切换。
    - 简化配置：从 Amazon S3 导入数据现在只需要一个步骤，从而节省了时间和精力。
    - 增强的 CSV 配置：CSV 配置设置现在位于文件类型选项下，使您可以更轻松地快速配置必要的参数。
    - 增强的目标表选择：支持通过单击复选框来选择所需的数据导入目标表。此改进消除了对复杂表达式的需求，并简化了目标表选择。
    - 改进的显示信息：解决了与导入过程中显示的不准确信息相关的问题。此外，已删除“预览”功能，以防止不完整的数据显示并避免误导性信息。
    - 改进的源文件映射：支持定义源文件和目标表之间的映射关系。它解决了修改源文件名以满足特定命名要求的挑战。

## 2023 年 7 月 11 日

**常规变更**

- [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 现已正式发布 (Generally Available)。

- 推出 TiDB Bot (beta)，这是一个由 OpenAI 提供支持的聊天机器人，提供多语言支持、24/7 实时响应和集成的文档访问。

    TiDB Bot 为您提供以下好处：

    - 持续支持：始终可用以协助和回答您的问题，从而增强支持体验。
    - 提高效率：自动响应减少延迟，从而提高整体运营效率。
    - 无缝文档访问：直接访问 TiDB Cloud 文档，以便轻松检索信息和快速解决问题。

  要使用 TiDB Bot，请单击 [TiDB Cloud 控制台](https://tidbcloud.com) 右下角的 **?**，然后选择 **Ask TiDB Bot** 开始聊天。

- 支持 [分支功能 (beta)](/tidb-cloud/branch-overview.md)，适用于 [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群。

    TiDB Cloud 允许您为 TiDB Cloud Serverless 集群创建分支。集群的分支是一个独立的实例，其中包含来自原始集群的数据的分叉副本。它提供了一个隔离的环境，允许您连接到它并自由地进行实验，而不必担心影响原始集群。

    您可以使用 [TiDB Cloud 控制台](/tidb-cloud/branch-manage.md) 或 [TiDB Cloud CLI](/tidb-cloud/ticloud-branch-create.md) 为 2023 年 7 月 5 日之后创建的 TiDB Cloud Serverless 集群创建分支。

    如果您使用 GitHub 进行应用程序开发，则可以将 TiDB Cloud Serverless 分支集成到您的 GitHub CI/CD 管道中，这使您可以自动使用分支测试您的拉取请求，而不会影响生产数据库。有关更多信息，请参见 [将 TiDB Cloud Serverless 分支（Beta）与 GitHub 集成](/tidb-cloud/branch-github-integration.md)。

- 支持 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的每周备份。有关更多信息，请参见 [备份和恢复 TiDB Cloud Dedicated 数据](/tidb-cloud/backup-and-restore.md#turn-on-auto-backup)。

## 2023  年 7 月 4 日

**常规变更**

- 支持 [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群的时间点恢复 (PITR)（测试版）。

    现在，您可以将 TiDB Cloud Serverless 集群恢复到过去 90 天内的任何时间点。此功能增强了 TiDB Cloud Serverless 集群的数据恢复能力。例如，当发生数据写入错误并且您想要将数据恢复到较早的状态时，可以使用 PITR。

    有关更多信息，请参阅[备份和恢复 TiDB Cloud Serverless 数据](/tidb-cloud/backup-and-restore-serverless.md#restore)。

**控制台变更**

- 增强了 [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群的集群概览页面上的**本月用量**面板，以提供更清晰的当前资源使用情况视图。

- 通过进行以下更改来增强整体导航体验：

    - 将右上角的 <MDSvgIcon name="icon-top-organization" /> **组织** 和 <MDSvgIcon name="icon-top-account-settings" /> **帐户** 合并到左侧导航栏中。
    - 将左侧导航栏中的 <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke-width="1.5" xmlns="http://www.w3.org/2000/svg"><path d="M12 14.5H7.5C6.10444 14.5 5.40665 14.5 4.83886 14.6722C3.56045 15.06 2.56004 16.0605 2.17224 17.3389C2 17.9067 2 18.6044 2 20M14.5 6.5C14.5 8.98528 12.4853 11 10 11C7.51472 11 5.5 8.98528 5.5 6.5C5.5 4.01472 7.51472 2 10 2C12.4853 2 14.5 4.01472 14.5 6.5ZM22 16.516C22 18.7478 19.6576 20.3711 18.8054 20.8878C18.7085 20.9465 18.6601 20.9759 18.5917 20.9911C18.5387 21.003 18.4613 21.003 18.4083 20.9911C18.3399 20.9759 18.2915 20.9465 18.1946 20.8878C17.3424 20.3711 15 18.7478 15 16.516V14.3415C15 13.978 15 13.7962 15.0572 13.6399C15.1077 13.5019 15.1899 13.3788 15.2965 13.2811C15.4172 13.1706 15.5809 13.1068 15.9084 12.9791L18.2542 12C18.3452 11.9646 18.4374 11.8 18.4374 11.8H18.5626C18.5626 11.8 18.6548 11.9646 18.7458 12L21.0916 12.9791C21.4191 13.1068 21.5828 13.1706 21.7035 13.2811C21.8101 13.3788 21.8923 13.5019 21.9428 13.6399C22 13.7962 22 13.978 22 14.3415V16.516Z" stroke="currentColor" stroke-width="inherit" stroke-linecap="round" stroke-linejoin="round"></path></svg> **管理** 合并到左侧导航栏中的 <MDSvgIcon name="icon-left-projects" /> **项目** 中，并删除左上角的 ☰ 悬停菜单。现在，您可以单击 <MDSvgIcon name="icon-left-projects" /> 以在项目之间切换并修改项目设置。
    - 将 TiDB Cloud 的所有帮助和支持信息整合到右下角 **?** 图标的菜单中，例如文档、交互式教程、自定进度的培训和支持条目。

- TiDB Cloud 控制台现在支持暗黑模式，提供更舒适、更护眼的体验。您可以从左侧导航栏底部在浅色模式和深色模式之间切换。

## 2023 年 6 月 27 日

**常规变更**

- 移除为新创建的 [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群预置的示例数据集。

## 2023 年 6 月 20 日

**常规变更**

- 将新 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的默认 TiDB 版本从 [v6.5.2](https://docs.pingcap.com/tidb/v6.5/release-6.5.2) 升级到 [v6.5.3](https://docs.pingcap.com/tidb/v6.5/release-6.5.3)。

## 2023 年 6 月 13 日

**常规变更**

- 支持使用变更流将数据流式传输到 Amazon S3。

    这实现了 TiDB Cloud 和 Amazon S3 之间的无缝集成。它允许从 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群进行实时数据捕获和复制到 Amazon S3，确保下游应用程序和分析可以访问最新的数据。

    更多信息，请参见 [Sink to cloud storage](/tidb-cloud/changefeed-sink-to-cloud-storage.md)。

- 将 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的 16 vCPU TiKV 的最大节点存储从 4 TiB 增加到 6 TiB。

    此增强功能增加了 TiDB Cloud Dedicated 集群的数据存储容量，提高了工作负载扩展效率，并满足了不断增长的数据需求。

    更多信息，请参见 [Size your cluster](/tidb-cloud/size-your-cluster.md)。

- 将 [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群的[监控指标保留期](/tidb-cloud/built-in-monitoring.md#metrics-retention-policy) 从 3 天延长至 7 天。

    通过延长指标保留期，您现在可以访问更多历史数据。 这有助于您识别集群的趋势和模式，从而做出更好的决策并更快地进行故障排除。

**控制台变更**

- 为 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的 [**Key Visualizer**](/tidb-cloud/tune-performance.md#key-visualizer) 页面发布新的原生 Web 基础设施。

    借助新的基础设施，您可以轻松浏览 **Key Visualizer** 页面，并以更直观和高效的方式访问必要的信息。 新的基础设施还解决了 UX 上的许多问题，使 SQL 诊断过程更加用户友好。

## 2023 年 6 月 6 日

**常规变更**

- 为 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群引入 [Index Insight (beta)](/tidb-cloud/index-insight.md)，它通过为慢查询提供索引建议来优化查询性能。

    借助 Index Insight，您可以通过以下方式提高整体应用程序性能和数据库操作效率：

    - 增强的查询性能：Index Insight 识别慢查询并为其建议适当的索引，从而加快查询执行速度，缩短响应时间并改善用户体验。
    - 成本效益：通过使用 Index Insight 优化查询性能，可以减少对额外计算资源的需求，从而使您能够更有效地利用现有基础设施。 这可能会带来运营成本的节省。
    - 简化的优化过程：Index Insight 简化了索引改进的识别和实施，无需手动分析和猜测。 因此，您可以节省时间和精力，并获得准确的索引建议。
    - 提高应用程序效率：通过使用 Index Insight 优化数据库性能，在 TiDB Cloud 上运行的应用程序可以处理更大的工作负载并同时为更多用户提供服务，从而使应用程序的扩展操作更加高效。

  要使用 Index Insight，请导航到 TiDB Cloud Dedicated 集群的**诊断**页面，然后单击 **Index Insight BETA** 选项卡。

    有关更多信息，请参见 [使用 Index Insight (beta)](/tidb-cloud/index-insight.md)。

- 引入 [TiDB Playground](https://play.tidbcloud.com/?utm_source=docs&utm_medium=tidb_cloud_release_notes)，这是一个交互式平台，无需注册或安装即可体验 TiDB 的全部功能。

    TiDB Playground 是一个交互式平台，旨在为探索 TiDB 的功能（例如可伸缩性、MySQL 兼容性和实时分析）提供一站式体验。

    借助 TiDB Playground，您可以在受控环境中实时试用 TiDB 功能，而无需复杂的配置，这使其成为了解 TiDB 功能的理想选择。

    要开始使用 TiDB Playground，请转到 [**TiDB Playground**](https://play.tidbcloud.com/?utm_source=docs&utm_medium=tidb_cloud_release_notes) 页面，选择要探索的功能，然后开始您的探索。

## 2023 年 6 月 5 日

**通用变更**

- 支持将您的 [数据应用](/tidb-cloud/tidb-cloud-glossary.md#data-app) 连接到 GitHub。

    通过 [将您的数据应用连接到 GitHub](/tidb-cloud/data-service-manage-github-connection.md)，您可以将数据应用的所有配置作为 GitHub 上的 [代码文件](/tidb-cloud/data-service-app-config-files.md) 进行管理，从而将 TiDB Cloud 数据服务与您的系统架构和 DevOps 流程无缝集成。

    借助此功能，您可以轻松完成以下任务，从而改善开发数据应用的 CI/CD 体验：

    - 使用 GitHub 自动部署数据应用更改。
    - 在 GitHub 上使用版本控制配置数据应用更改的 CI/CD 管道。
    - 断开与已连接的 GitHub 存储库的连接。
    - 在部署之前查看端点更改。
    - 查看部署历史记录，并在发生故障时采取必要的措施。
    - 重新部署提交以回滚到较早的部署。

  有关更多信息，请参见 [使用 GitHub 自动部署数据应用](/tidb-cloud/data-service-manage-github-connection.md)。

## 2023 年 6 月 2 日

**常规变更**

- 为了简化和明确，我们更新了产品的名称：

    - "TiDB Cloud Serverless Tier" 现在称为 "TiDB Cloud Serverless"。
    - "TiDB Cloud Dedicated Tier" 现在称为 "TiDB Cloud Dedicated"。
    - "TiDB On-Premises" 现在称为 "TiDB Self-Managed"。

    在这些更新后的名称下享受同样的卓越性能。您的体验是我们的首要任务。

## 2023 年 5 月 30 日

**常规变更**

- 增强了 TiDB Cloud 中数据迁移功能对增量数据迁移的支持。

    现在，您可以指定一个 binlog 位置或全局事务标识符 (GTID)，仅复制指定位置之后生成的增量数据到 TiDB Cloud。此增强功能使您能够更灵活地选择和复制所需的数据，以满足您的特定需求。

    有关详细信息，请参阅[使用数据迁移将 MySQL 兼容数据库中的增量数据迁移到 TiDB Cloud](/tidb-cloud/migrate-incremental-data-from-mysql-using-data-migration.md)。

- 在 [**事件**](/tidb-cloud/tidb-cloud-events.md) 页面添加了一个新的事件类型 (`ImportData`)。

- 从 TiDB Cloud 控制台中移除 **Playground**。

    敬请期待具有优化体验的全新独立 Playground。

## 2023 年 5 月 23 日

**常规变更**

- 当上传 CSV 文件到 TiDB 时，您不仅可以使用英文字母和数字，还可以使用中文和日文等字符来定义列名。但是，对于特殊字符，仅支持下划线 (`_`)。

    有关详细信息，请参阅 [将本地文件导入到 TiDB Cloud](/tidb-cloud/tidb-cloud-import-local-files.md)。

## 2023 年 5 月 16 日

**控制台变更**

- 引入按功能类别组织的左侧导航条目，适用于专用层和无服务器层。

    新的导航使您更容易、更直观地发现功能条目。要查看新的导航，请访问集群的概览页面。

- 为专用层集群的**诊断**页面上的以下两个选项卡发布新的原生 Web 基础设施。

    - [慢查询](/tidb-cloud/tune-performance.md#slow-query)
    - [SQL 语句](/tidb-cloud/tune-performance.md#statement-analysis)

    借助新的基础设施，您可以轻松浏览这两个选项卡，并以更直观、更高效的方式访问必要的信息。新的基础设施还改善了用户体验，使 SQL 诊断过程更加用户友好。

## 2023 年 5 月 9 日

**常规变更**

- 支持更改 2023 年 4 月 26 日之后创建的 GCP 托管集群的节点大小。

    借助此功能，您可以升级到更高性能的节点以满足更高的需求，或者降级到更低性能的节点以节省成本。 凭借这种增加的灵活性，您可以调整集群的容量以适应您的工作负载并优化成本。

    有关详细步骤，请参阅[更改节点大小](/tidb-cloud/scale-tidb-cluster.md#change-vcpu-and-ram)。

- 支持导入压缩文件。 您可以导入以下格式的 CSV 和 SQL 文件：`.gzip`、`.gz`、`.zstd`、`.zst` 和 `.snappy`。 此功能提供了一种更高效且经济高效的数据导入方式，并降低了您的数据传输成本。

    有关更多信息，请参阅[将 CSV 文件从云存储导入到 TiDB Cloud Dedicated](/tidb-cloud/import-csv-files.md)和[导入示例数据](/tidb-cloud/import-sample-data.md)。

- 支持基于 AWS PrivateLink 的端点连接，作为 TiDB Cloud [Serverless Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群的一种新的网络访问管理选项。

    私有端点连接不会将您的数据暴露给公共互联网。 此外，端点连接支持 CIDR 重叠，并且更易于网络管理。

    有关更多信息，请参阅[设置私有端点连接](/tidb-cloud/set-up-private-endpoint-connections.md)。

**控制台变更**

- 将新的事件类型添加到[**事件**](/tidb-cloud/tidb-cloud-events.md)页面，以记录 [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的备份、恢复和变更数据捕获操作。

    要获取可以记录的事件的完整列表，请参阅[已记录的事件](/tidb-cloud/tidb-cloud-events.md#logged-events)。

- 在 [**SQL 诊断**](/tidb-cloud/tune-performance.md) 页面上为 [Serverless Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群引入 **SQL 语句** 选项卡。

    **SQL 语句** 选项卡提供以下内容：

    - 全面概述 TiDB 数据库执行的所有 SQL 语句，使您可以轻松识别和诊断慢查询。
    - 有关每个 SQL 语句的详细信息，例如查询时间、执行计划和数据库服务器响应，帮助您优化数据库性能。
    - 用户友好的界面，可以轻松地对大量数据进行排序、过滤和搜索，使您可以专注于最关键的查询。

  有关更多信息，请参阅[语句分析](/tidb-cloud/tune-performance.md#statement-analysis)。

## 2023 年 5 月 6 日

**常规变更**

- 支持直接访问 TiDB [Serverless 层](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群所在区域的[数据服务终端节点](/tidb-cloud/tidb-cloud-glossary.md#endpoint)。

    对于新创建的 Serverless 层集群，终端节点 URL 现在包含集群区域信息。 通过请求区域域名 `<region>.data.tidbcloud.com`，您可以直接访问 TiDB 集群所在区域的终端节点。

    或者，您也可以请求全局域名 `data.tidbcloud.com` 而不指定区域。 这样，TiDB Cloud 将在内部将请求重定向到目标区域，但这可能会导致额外的延迟。 如果您选择这种方式，请确保在调用终端节点时将 `--location-trusted` 选项添加到您的 curl 命令中。

    有关更多信息，请参阅[调用终端节点](/tidb-cloud/data-service-manage-endpoint.md#call-an-endpoint)。

## 2023 年 4 月 25 日

**常规变更**

- 对于您组织中的前五个 [Serverless Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群，TiDB Cloud 为每个集群提供如下免费使用配额：

    - 行存储：5 GiB
    - [请求单元 (RUs)](/tidb-cloud/tidb-cloud-glossary.md#request-unit)：每月 5000 万 RUs

  在 2023 年 5 月 31 日之前，Serverless Tier 集群仍然免费，享受 100% 折扣。之后，超出免费配额的使用量将被收费。

    您可以轻松地在集群**概览**页面的**本月使用量**区域[监控您的集群使用量或增加您的使用配额](/tidb-cloud/manage-serverless-spend-limit.md#manage-spending-limit-for-tidb-cloud-serverless-scalable-clusters)。一旦集群达到免费配额，该集群上的读写操作将被限制，直到您增加配额或在新月份开始时重置使用量。

    有关不同资源（包括读取、写入、SQL CPU 和网络出口）的 RU 消耗、定价详情和限制信息的更多信息，请参阅 [TiDB Cloud Serverless Tier 定价详情](https://www.pingcap.com/tidb-cloud-serverless-pricing-details)。

- 支持 TiDB Cloud [Serverless Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群的备份和恢复。

     有关更多信息，请参阅 [备份和恢复 TiDB 集群数据](/tidb-cloud/backup-and-restore-serverless.md)。

- 将新的 [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的默认 TiDB 版本从 [v6.5.1](https://docs.pingcap.com/tidb/v6.5/release-6.5.1) 升级到 [v6.5.2](https://docs.pingcap.com/tidb/v6.5/release-6.5.2)。

- 提供维护窗口功能，使您能够轻松地为 [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群安排和管理计划的维护活动。

    维护窗口是指定的时间段，在此期间会自动执行计划的维护活动，例如操作系统更新、安全补丁和基础设施升级，以确保 TiDB Cloud 服务的可靠性、安全性和性能。

    在维护窗口期间，可能会发生临时连接中断或 QPS 波动，但集群仍然可用，并且 SQL 操作、现有数据导入、备份、恢复、迁移和复制任务仍然可以正常运行。请参阅维护期间[允许和禁止的操作列表](/tidb-cloud/configure-maintenance-window.md#allowed-and-disallowed-operations-during-a-maintenance-window)。

    我们将努力尽量减少维护频率。如果计划了维护窗口，则默认开始时间为目标周的星期三 03:00（基于您的 TiDB Cloud 组织的时区）。为避免潜在的中断，重要的是要注意维护计划并相应地计划您的操作。

    - 为了让您了解情况，TiDB Cloud 将为每个维护窗口向您发送三封电子邮件通知：一封在维护任务之前，一封在维护任务开始时，一封在维护任务之后。
    - 为了最大限度地减少维护影响，您可以在**维护**页面上将维护开始时间修改为您首选的时间或推迟维护活动。

  有关更多信息，请参阅 [配置维护窗口](/tidb-cloud/configure-maintenance-window.md)。

- 改进 TiDB 的负载均衡，并减少在扩展 AWS 上托管并在 2023 年 4 月 25 日之后创建的 [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的 TiDB 节点时连接断开的情况。

    - 支持在扩展 TiDB 节点时自动将现有连接迁移到新的 TiDB 节点。
    - 支持在缩减 TiDB 节点时自动将现有连接迁移到可用的 TiDB 节点。

  目前，此功能适用于 AWS 上托管的所有 Dedicated Tier 集群。

**控制台变更**

- 为 [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的 [监控](/tidb-cloud/built-in-monitoring.md#view-the-metrics-page) 页面发布新的原生 Web 基础设施。

    借助新的基础设施，您可以轻松浏览[监控](/tidb-cloud/built-in-monitoring.md#view-the-metrics-page)页面，并以更直观和高效的方式访问必要的信息。新的基础设施还解决了 UX 上的许多问题，使监控过程更加用户友好。

## 2023 年 4 月 18 日

**常规变更**

- 支持为[专用层](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)集群向上或向下扩展[数据迁移作业规格](/tidb-cloud/tidb-cloud-billing-dm.md#specifications-for-data-migration)。

    使用此功能，您可以通过向上扩展规格来提高迁移性能，或者通过向下扩展规格来降低成本。

    有关更多信息，请参阅[使用数据迁移将 MySQL 兼容数据库迁移到 TiDB Cloud](/tidb-cloud/migrate-from-mysql-using-data-migration.md#scale-a-migration-job-specification)。

**控制台变更**

- 改进了 UI，使[集群创建](https://tidbcloud.com/clusters/create-cluster)体验更加用户友好，使您只需点击几下即可创建和配置集群。

    新设计侧重于简洁性，减少视觉混乱并提供清晰的说明。 在集群创建页面上单击**创建**后，您将被定向到集群概览页面，而无需等待集群创建完成。

    有关更多信息，请参阅[创建集群](/tidb-cloud/create-tidb-cluster.md)。

- 在**账单**页面上引入**折扣**选项卡，以显示组织所有者和账单管理员的折扣信息。

    有关更多信息，请参阅[折扣](/tidb-cloud/tidb-cloud-billing.md#discounts)。

## 2023 年 4 月 11 日

**常规变更**

- 提高 TiDB 的负载均衡，并减少在 AWS 上托管的 [专用层](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群扩展 TiDB 节点时连接断开的情况。

    - 支持在横向扩展 TiDB 节点时，自动将现有连接迁移到新的 TiDB 节点。
    - 支持在横向缩减 TiDB 节点时，自动将现有连接迁移到可用的 TiDB 节点。

  目前，此功能仅适用于托管在 AWS `俄勒冈 (us-west-2)` 区域的专用层集群。

- 支持 [New Relic](https://newrelic.com/) 集成，用于 [专用层](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群。

    通过 New Relic 集成，您可以配置 TiDB Cloud 将 TiDB 集群的指标数据发送到 [New Relic](https://newrelic.com/)。 然后，您可以在 [New Relic](https://newrelic.com/) 上监控和分析您的应用程序性能和 TiDB 数据库性能。 此功能可以帮助您快速识别和排除潜在问题，并缩短解决时间。

    有关集成步骤和可用指标，请参阅 [将 TiDB Cloud 与 New Relic 集成](/tidb-cloud/monitor-new-relic-integration.md)。

- 将以下 [changefeed](/tidb-cloud/changefeed-overview.md) 指标添加到专用层集群的 Prometheus 集成中。

    - `tidbcloud_changefeed_latency`
    - `tidbcloud_changefeed_replica_rows`

    如果您已 [将 TiDB Cloud 与 Prometheus 集成](/tidb-cloud/monitor-prometheus-and-grafana-integration.md)，则可以使用这些指标实时监控 changefeed 的性能和健康状况。 此外，您可以轻松创建警报以使用 Prometheus 监控指标。

**控制台变更**

- 更新 [专用层](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的 [监控](/tidb-cloud/built-in-monitoring.md#view-the-metrics-page) 页面，以使用 [节点级资源指标](/tidb-cloud/built-in-monitoring.md#server)。

    通过节点级资源指标，您可以更准确地了解资源消耗情况，从而更好地了解所购买服务的实际使用情况。

    要访问这些指标，请导航到集群的 [监控](/tidb-cloud/built-in-monitoring.md#view-the-metrics-page) 页面，然后选中 **指标** 选项卡下的 **服务器** 类别。

- 通过重新组织 **按项目汇总** 和 **按服务汇总** 中的计费项目来优化 [计费](/tidb-cloud/tidb-cloud-billing.md#billing-details) 页面，这使得计费信息更加清晰。

## 2023  年 4 月 4 日

**常规变更**

- 从 [TiDB Cloud 内置告警](/tidb-cloud/monitor-built-in-alerting.md#tidb-cloud-built-in-alert-conditions) 中删除以下两个告警，以防止误报。 这是因为一个节点上的临时离线或内存不足 (OOM) 问题不会显着影响集群的整体健康状况。

    - 集群中至少有一个 TiDB 节点内存不足。
    - 一个或多个集群节点处于离线状态。

**控制台变更**

- 为 [专用层](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群引入 [告警](/tidb-cloud/monitor-built-in-alerting.md) 页面，其中列出了每个专用层集群的活动和已关闭告警。

    **告警** 页面提供以下内容：

    - 直观且用户友好的用户界面。 即使您没有订阅告警通知电子邮件，也可以在此页面上查看集群的告警。
    - 高级筛选选项，可帮助您根据告警的严重性、状态和其他属性快速查找和排序告警。 它还允许您查看过去 7 天的历史数据，从而简化了告警历史记录的跟踪。
    - **编辑规则** 功能。 您可以自定义告警规则设置以满足集群的特定需求。

  有关更多信息，请参阅 [TiDB Cloud 内置告警](/tidb-cloud/monitor-built-in-alerting.md)。

- 将 TiDB Cloud 的帮助相关信息和操作整合到一个位置。

    现在，您可以通过单击 [TiDB Cloud 控制台](https://tidbcloud.com/) 右下角的 **?** 来获取所有 [TiDB Cloud 帮助信息](/tidb-cloud/tidb-cloud-support.md) 并联系支持。

- 引入 [入门](https://tidbcloud.com/getting-started) 页面，以帮助您了解 TiDB Cloud。

    **入门** 页面为您提供交互式教程、基本指南和有用的链接。 通过遵循交互式教程，您可以轻松地使用预构建的行业特定数据集（Steam 游戏数据集和 S&P 500 数据集）探索 TiDB Cloud 功能和 HTAP 功能。

    要访问 **入门** 页面，请单击 [TiDB Cloud 控制台](https://tidbcloud.com/) 左侧导航栏中的 <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M12 14.9998L9 11.9998M12 14.9998C13.3968 14.4685 14.7369 13.7985 16 12.9998M12 14.9998V19.9998C12 19.9998 15.03 19.4498 16 17.9998C17.08 16.3798 16 12.9998 16 12.9998M9 11.9998C9.53214 10.6192 10.2022 9.29582 11 8.04976C12.1652 6.18675 13.7876 4.65281 15.713 3.59385C17.6384 2.53489 19.8027 1.98613 22 1.99976C22 4.71976 21.22 9.49976 16 12.9998M9 11.9998H4C4 11.9998 4.55 8.96976 6 7.99976C7.62 6.91976 11 7.99976 11 7.99976M4.5 16.4998C3 17.7598 2.5 21.4998 2.5 21.4998C2.5 21.4998 6.24 20.9998 7.5 19.4998C8.21 18.6598 8.2 17.3698 7.41 16.5898C7.02131 16.2188 6.50929 16.0044 5.97223 15.9878C5.43516 15.9712 4.91088 16.1535 4.5 16.4998Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path></svg> **入门**。 在此页面上，您可以单击 **查询示例数据集** 以打开交互式教程，或单击其他链接以探索 TiDB Cloud。 或者，您可以单击右下角的 **?**，然后单击 **交互式教程**。

## 2023 年 3 月 29 日

**常规变更**

- [数据服务 (beta)](/tidb-cloud/data-service-overview.md) 支持对数据应用进行更细粒度的访问控制。

    在数据应用详情页面，现在您可以将集群链接到您的数据应用，并为每个 API 密钥指定角色。该角色控制 API 密钥是否可以读取或写入链接集群的数据，并且可以设置为 `ReadOnly` 或 `ReadAndWrite`。此功能为数据应用提供集群级别和权限级别的访问控制，使您可以更灵活地根据业务需求控制访问范围。

    有关更多信息，请参阅 [管理链接的集群](/tidb-cloud/data-service-manage-data-app.md#manage-linked-data-sources) 和 [管理 API 密钥](/tidb-cloud/data-service-api-key.md)。

## 2023  年 3 月 28 日

**常规变更**

- 为 [changefeeds](/tidb-cloud/changefeed-overview.md) 添加 2 RCUs、4 RCUs 和 8 RCUs 规格，并支持在 [创建 changefeed](/tidb-cloud/changefeed-overview.md#create-a-changefeed) 时选择所需的规格。

    与之前需要 16 RCUs 的场景相比，使用这些新规格，数据复制成本最多可降低 87.5%。

- 支持扩展或缩小 2023 年 3 月 28 日之后创建的 [changefeeds](/tidb-cloud/changefeed-overview.md) 的规格。

    您可以通过选择更高的规格来提高复制性能，或通过选择更低的规格来降低复制成本。

    有关更多信息，请参阅 [缩放 changefeed](/tidb-cloud/changefeed-overview.md#scale-a-changefeed)。

- 支持将 AWS 中 [专用层](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群中的增量数据实时复制到同一项目和同一区域中的 [无服务器层](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群。

    有关更多信息，请参阅 [Sink to TiDB Cloud](/tidb-cloud/changefeed-sink-to-tidb-cloud.md)。

- 为 [专用层](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的 [数据迁移](/tidb-cloud/migrate-from-mysql-using-data-migration.md) 功能支持两个新的 GCP 区域：`Singapore (asia-southeast1)` 和 `Oregon (us-west1)`。

    有了这些新区域，您可以有更多选择将数据迁移到 TiDB Cloud。如果您的上游数据存储在这些区域中或附近，您现在可以利用从 GCP 到 TiDB Cloud 更快、更可靠的数据迁移。

    有关更多信息，请参阅 [使用数据迁移将 MySQL 兼容数据库迁移到 TiDB Cloud](/tidb-cloud/migrate-from-mysql-using-data-migration.md)。

**控制台变更**

- 为 [无服务器层](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群的 [慢查询](/tidb-cloud/tune-performance.md#slow-query) 页面发布新的原生 Web 基础设施。

    借助这种新的基础设施，您可以轻松地浏览 [慢查询](/tidb-cloud/tune-performance.md#slow-query) 页面，并以更直观、更高效的方式访问必要的信息。 新的基础设施还解决了 UX 上的许多问题，使 SQL 诊断过程更加用户友好。

## 2023 年 3 月 21 日

**常规变更**

- 针对 [Serverless Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群，引入 [Data Service (beta)](https://tidbcloud.com/project/data-service)，使您能够通过使用自定义 API 端点的 HTTPS 请求来访问数据。

    借助 Data Service，您可以将 TiDB Cloud 与任何兼容 HTTPS 的应用程序或服务无缝集成。以下是一些常见场景：

    - 直接从移动或 Web 应用程序访问 TiDB 集群的数据库。
    - 使用 Serverless 边缘函数调用端点，避免数据库连接池导致的可扩展性问题。
    - 通过使用 Data Service 作为数据源，将 TiDB Cloud 与数据可视化项目集成。
    - 从 MySQL 接口不支持的环境连接到您的数据库。

    此外，TiDB Cloud 还提供 [Chat2Query API](/tidb-cloud/use-chat2query-api.md)，这是一个 RESTful 接口，允许您使用 AI 生成和执行 SQL 语句。

    要访问 Data Service，请导航到左侧导航窗格中的 [**Data Service**](https://tidbcloud.com/project/data-service) 页面。有关更多信息，请参阅以下文档：

    - [Data Service 概述](/tidb-cloud/data-service-overview.md)
    - [Data Service 入门](/tidb-cloud/data-service-get-started.md)
    - [Chat2Query API 入门](/tidb-cloud/use-chat2query-api.md)

- 支持减小 TiDB、TiKV 和 TiFlash 节点的大小，以在 AWS 上托管且在 2022 年 12 月 31 日之后创建的 [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群中进行缩容。

    您可以[通过 TiDB Cloud 控制台](/tidb-cloud/scale-tidb-cluster.md#change-vcpu-and-ram)或[通过 TiDB Cloud API (beta)](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/UpdateCluster) 减小节点大小。

- 为 [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的 [Data Migration](/tidb-cloud/migrate-from-mysql-using-data-migration.md) 功能支持新的 GCP 区域：`Tokyo (asia-northeast1)`。

    该功能可以帮助您轻松高效地将 Google Cloud Platform (GCP) 中与 MySQL 兼容的数据库中的数据迁移到您的 TiDB 集群。

    有关更多信息，请参阅 [使用 Data Migration 将与 MySQL 兼容的数据库迁移到 TiDB Cloud](/tidb-cloud/migrate-from-mysql-using-data-migration.md)。

**控制台变更**

- 为 [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群引入 **Events** 页面，该页面提供对集群的主要更改的记录。

    在此页面上，您可以查看过去 7 天的事件历史记录，并跟踪重要详细信息，例如触发时间和发起操作的用户。例如，您可以查看集群何时暂停或谁修改了集群大小等事件。

    有关更多信息，请参阅 [TiDB Cloud 集群事件](/tidb-cloud/tidb-cloud-events.md)。

- 将 **Database Status** 选项卡添加到 [Serverless Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群的 **Monitoring** 页面，该页面显示以下数据库级别指标：

    - 每个数据库的 QPS
    - 每个数据库的平均查询持续时间
    - 每个数据库的失败查询

  通过这些指标，您可以监控各个数据库的性能，做出数据驱动的决策，并采取措施来提高应用程序的性能。

  有关更多信息，请参阅 [Serverless Tier 集群的监控指标](/tidb-cloud/built-in-monitoring.md)。

## 2023 年 3 月 14 日

**常规变更**

- 将新 [专用层](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的默认 TiDB 版本从 [v6.5.0](https://docs.pingcap.com/tidb/v6.5/release-6.5.0) 升级到 [v6.5.1](https://docs.pingcap.com/tidb/v6.5/release-6.5.1)。

- 支持在上传带有标题行的本地 CSV 文件时，修改 TiDB Cloud 创建的目标表的列名。

    当将带有标题行的本地 CSV 文件导入到 [Serverless 层](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群时，如果您需要 TiDB Cloud 创建目标表，并且标题行中的列名不符合 TiDB Cloud 列命名约定，您将在相应列名旁边看到一个警告图标。要解决此警告，您可以将光标移到图标上，然后按照消息编辑现有列名或输入新的列名。

    有关列命名约定的信息，请参阅 [导入本地文件](/tidb-cloud/tidb-cloud-import-local-files.md#import-local-files)。

## 2023 年 3 月 7 日

**通用变更**

- 将所有[Serverless Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)集群的默认 TiDB 版本从 [v6.4.0](https://docs.pingcap.com/tidb/v6.4/release-6.4.0) 升级到 [v6.6.0](https://docs.pingcap.com/tidb/v6.6/release-6.6.0)。

## 2023 年 2 月 28 日

**常规变更**

- 为[Serverless Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)集群添加[SQL诊断](/tidb-cloud/tune-performance.md)功能。

    通过SQL诊断，您可以深入了解与SQL相关的运行时状态，从而更有效地进行SQL性能调优。目前，Serverless Tier的SQL诊断功能仅提供慢查询数据。

    要使用SQL诊断，请单击Serverless Tier集群页面左侧导航栏上的**SQL诊断**。

**控制台变更**

- 优化左侧导航。

    您可以更高效地浏览页面，例如：

    - 您可以将鼠标悬停在左上角以快速切换集群或项目。
    - 您可以在**集群**页面和**管理**页面之间切换。

**API变更**

- 发布了多个用于数据导入的TiDB Cloud API端点：

    - 列出所有导入任务
    - 获取导入任务
    - 创建导入任务
    - 更新导入任务
    - 上传导入任务的本地文件
    - 在启动导入任务之前预览数据
    - 获取导入任务的角色信息

  有关更多信息，请参阅[API文档](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Import)。

## 2023 年 2 月 22 日

**常规变更**

- 支持使用 [控制台审计日志](/tidb-cloud/tidb-cloud-console-auditing.md) 功能来跟踪组织成员在 [TiDB Cloud 控制台](https://tidbcloud.com/) 中执行的各种活动。

    控制台审计日志功能仅对具有 `Owner` 或 `Audit Admin` 角色的用户可见，并且默认情况下处于禁用状态。要启用它，请单击 <MDSvgIcon name="icon-top-organization" /> **组织** > **控制台审计日志**，位于 [TiDB Cloud 控制台](https://tidbcloud.com/) 的右上角。

    通过分析控制台审计日志，您可以识别组织内执行的可疑操作，从而提高组织资源和数据的安全性。

    有关更多信息，请参阅 [控制台审计日志](/tidb-cloud/tidb-cloud-console-auditing.md)。

**CLI 变更**

- 为 [TiDB Cloud CLI](/tidb-cloud/cli-reference.md) 添加了一个新命令 `ticloud cluster connect-info`。

    `ticloud cluster connect-info` 是一个允许您获取集群连接字符串的命令。要使用此命令，请[更新 `ticloud`](/tidb-cloud/ticloud-upgrade.md) 到 v0.3.2 或更高版本。

## 2023 年 2 月 21 日

**常规变更**

- 支持使用 IAM 用户的 AWS 访问密钥来访问您的 Amazon S3 存储桶，以便将数据导入到 TiDB Cloud。

    此方法比使用角色 ARN 更简单。有关更多信息，请参阅 [配置 Amazon S3 访问](/tidb-cloud/dedicated-external-storage.md#configure-amazon-s3-access)。

- 将 [监控指标保留期限](/tidb-cloud/built-in-monitoring.md#metrics-retention-policy) 从 2 天延长到更长的时间：

    - 对于专用层集群，您可以查看过去 7 天的指标数据。
    - 对于无服务器层集群，您可以查看过去 3 天的指标数据。

  通过延长指标保留期限，您现在可以访问更多历史数据。这有助于您识别集群的趋势和模式，从而更好地进行决策和更快地进行故障排除。

**控制台变更**

- 在 [无服务器层](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群的监控页面上发布新的原生 Web 基础设施。

    借助新的基础设施，您可以轻松浏览监控页面，并以更直观和高效的方式访问必要的信息。新的基础设施还解决了 UX 上的许多问题，使监控过程更加用户友好。

## 2023 年 2 月 17 日

**CLI 变更**

- 添加一个新命令 [`ticloud connect`](/tidb-cloud/ticloud-serverless-shell.md) 用于 [TiDB Cloud CLI](/tidb-cloud/cli-reference.md)。

    `ticloud connect` 是一个允许你从本地机器连接到你的 TiDB Cloud 集群而无需安装任何 SQL 客户端的命令。 连接到你的 TiDB Cloud 集群后，你可以在 TiDB Cloud CLI 中执行 SQL 语句。

## 2023 年 2 月 14 日

**常规变更**

- 支持减少 TiKV 和 TiFlash 节点数量，以在 TiDB [专用层](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群中进行缩容。

    您可以通过 [TiDB Cloud 控制台](/tidb-cloud/scale-tidb-cluster.md#change-node-number) 或 [通过 TiDB Cloud API (beta)](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/UpdateCluster) 减少节点数量。

**控制台变更**

- 为 [Serverless 层](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群引入 **监控** 页面。

    **监控** 页面提供了一系列指标和数据，例如每秒执行的 SQL 语句数量、查询的平均持续时间以及失败的查询数量，这有助于您更好地了解 Serverless 层集群中 SQL 语句的整体性能。

    有关更多信息，请参阅 [TiDB Cloud 内置监控](/tidb-cloud/built-in-monitoring.md)。

## 2023 年 2 月 2 日

**CLI 变更**

- 引入 TiDB Cloud CLI 客户端 [`ticloud`](/tidb-cloud/cli-reference.md)。

    使用 `ticloud`，您可以通过几行命令从终端或其他自动工作流程轻松管理您的 TiDB Cloud 资源。 特别是对于 GitHub Actions，我们提供了 [`setup-tidbcloud-cli`](https://github.com/marketplace/actions/set-up-tidbcloud-cli)，以便您轻松设置 `ticloud`。

    有关更多信息，请参阅 [TiDB Cloud CLI 快速入门](/tidb-cloud/get-started-with-cli.md) 和 [TiDB Cloud CLI 参考](/tidb-cloud/cli-reference.md)。

## 2023 年 1 月 18 日

**常规变更**

* 支持使用 Microsoft 帐户[注册](https://tidbcloud.com/free-trial) TiDB Cloud。

## 2023 年 1 月 17 日

**常规变更**

- 将新 [专用层](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的默认 TiDB 版本从 [v6.1.3](https://docs.pingcap.com/tidb/stable/release-6.1.3) 升级到 [v6.5.0](https://docs.pingcap.com/tidb/stable/release-6.5.0)。

- 对于新注册用户，TiDB Cloud 将自动创建一个免费的 [Serverless 层](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群，以便您可以快速开始使用 TiDB Cloud 进行数据探索之旅。

- 为 [专用层](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群支持一个新的 AWS 区域：`Seoul (ap-northeast-2)`。

    此区域启用了以下功能：

    - [使用数据迁移将 MySQL 兼容数据库迁移到 TiDB Cloud](/tidb-cloud/migrate-from-mysql-using-data-migration.md)
    - [使用变更数据捕获将数据从 TiDB Cloud 流式传输到其他数据服务](/tidb-cloud/changefeed-overview.md)
    - [备份和恢复 TiDB 集群数据](/tidb-cloud/backup-and-restore.md)

## 2023 年 1 月 10 日

**常规变更**

- 优化了从本地 CSV 文件导入数据到 TiDB 的功能，以改善 [Serverless Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群的用户体验。

    - 要上传 CSV 文件，现在您可以简单地将其拖放到 **导入** 页面上的上传区域。
    - 创建导入任务时，如果目标数据库或表不存在，您可以输入一个名称，让 TiDB Cloud 自动为您创建。 对于要创建的目标表，您可以指定主键或选择多个字段以形成复合主键。
    - 导入完成后，您可以通过单击 **通过 Chat2Query 探索您的数据** 或单击任务列表中的目标表名，使用 [AI 驱动的 Chat2Query](/tidb-cloud/explore-data-with-chat2query.md) 探索您的数据。

  有关更多信息，请参见 [将本地文件导入到 TiDB Cloud](/tidb-cloud/tidb-cloud-import-local-files.md)。

**控制台变更**

- 为每个集群添加 **获取支持** 选项，以简化请求特定集群支持的过程。

    您可以通过以下任一方式请求集群支持：

    - 在项目的 [**集群**](https://tidbcloud.com/project/clusters) 页面上，单击集群所在行的 **...**，然后选择 **获取支持**。
    - 在集群概览页面上，单击右上角的 **...**，然后选择 **获取支持**。

## 2023 年 1 月 5 日

**控制台变更**

- 将 SQL 编辑器（beta）重命名为 Chat2Query（beta），适用于 [Serverless Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群，并支持使用 AI 生成 SQL 查询。

  在 Chat2Query 中，您可以让 AI 自动生成 SQL 查询，或者手动编写 SQL 查询，并在没有终端的情况下针对数据库运行 SQL 查询。

  要访问 Chat2Query，请转到项目的 [**集群**](https://tidbcloud.com/project/clusters) 页面，点击您的集群名称，然后在左侧导航窗格中点击 **Chat2Query**。

## 2023 年 1 月 4 日

**常规变更**

- 支持通过增加在 AWS 上托管且在 2022 年 12 月 31 日之后创建的 TiDB Cloud Dedicated 集群的 **节点大小（vCPU + RAM）** 来扩展 TiDB、TiKV 和 TiFlash 节点。

    您可以使用 [TiDB Cloud 控制台](/tidb-cloud/scale-tidb-cluster.md#change-vcpu-and-ram) 或 [TiDB Cloud API (beta)](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/UpdateCluster) 来增加节点大小。

- 将 [**监控**](/tidb-cloud/built-in-monitoring.md) 页面上的指标保留期限延长至两天。

    现在您可以访问过去两天的指标数据，从而更灵活地了解集群性能和趋势。

    此改进无需额外费用，可以在集群的 [**监控**](/tidb-cloud/built-in-monitoring.md) 页面的 **诊断** 选项卡上访问。 这将帮助您识别和排除性能问题，并更有效地监控集群的整体健康状况。

- 支持为 Prometheus 集成自定义 Grafana 仪表板 JSON。

    如果您已将 [TiDB Cloud 与 Prometheus 集成](/tidb-cloud/monitor-prometheus-and-grafana-integration.md)，您现在可以导入预构建的 Grafana 仪表板来监控 TiDB Cloud 集群，并根据您的需要自定义仪表板。 此功能可以轻松快速地监控您的 TiDB Cloud 集群，并帮助您快速识别任何性能问题。

    有关更多信息，请参阅 [使用 Grafana GUI 仪表板可视化指标](/tidb-cloud/monitor-prometheus-and-grafana-integration.md#step-3-use-grafana-gui-dashboards-to-visualize-the-metrics)。

- 将所有 [Serverless Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群的默认 TiDB 版本从 [v6.3.0](https://docs.pingcap.com/tidb/v6.3/release-6.3.0) 升级到 [v6.4.0](https://docs.pingcap.com/tidb/v6.4/release-6.4.0)。 将 Serverless Tier 集群的默认 TiDB 版本升级到 v6.4.0 后，冷启动问题已得到解决。

**控制台变更**

- 简化 [**集群**](https://tidbcloud.com/project/clusters) 页面和集群概览页面的显示。

    - 您可以单击 [**集群**](https://tidbcloud.com/project/clusters) 页面上的集群名称以进入集群概览页面并开始操作集群。
    - 从集群概览页面中删除 **连接** 和 **导入** 窗格。 您可以单击右上角的 **连接** 以获取连接信息，然后单击左侧导航窗格中的 **导入** 以导入数据。
