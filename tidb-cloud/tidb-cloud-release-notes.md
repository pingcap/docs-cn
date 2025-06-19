---
title: TiDB Cloud 2025 年发布说明
summary: 了解 TiDB Cloud 2025 年的发布说明。
aliases: ['/tidbcloud/supported-tidb-versions','/tidbcloud/release-notes']
---

# TiDB Cloud 2025 年发布说明

本页列出了 [TiDB Cloud](https://www.pingcap.com/tidb-cloud/) 在 2025 年的发布说明。

## 2025 年 6 月 17 日

**一般变更**

- 对于 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群，16 vCPU 和 32 vCPU 的 TiKV 节点的最大存储大小从 **6144 GiB** 改为 **4096 GiB**。

    更多信息，请参见 [TiKV 节点存储大小](/tidb-cloud/size-your-cluster.md#tikv-node-storage-size)。

**控制台变更**

- 重新设计左侧导航栏以改善整体导航体验。
  
    - 在左上角新增了一个 <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="none" viewBox="0 0 24 24" stroke-width="1.5" class="" style="width: calc(1.25rem * var(--mantine-scale)); height: calc(1.25rem * var(--mantine-scale));"><path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" d="M9 3v18M7.8 3h8.4c1.68 0 2.52 0 3.162.327a3 3 0 0 1 1.311 1.311C21 5.28 21 6.12 21 7.8v8.4c0 1.68 0 2.52-.327 3.162a3 3 0 0 1-1.311 1.311C18.72 21 17.88 21 16.2 21H7.8c-1.68 0-2.52 0-3.162-.327a3 3 0 0 1-1.311-1.311C3 18.72 3 17.88 3 16.2V7.8c0-1.68 0-2.52.327-3.162a3 3 0 0 1 1.311-1.311C5.28 3 6.12 3 7.8 3" stroke-width="inherit"></path></svg> 图标，让你可以根据需要轻松隐藏或显示左侧导航栏。
    - 在左上角新增了一个组合框，让你可以从一个中心位置快速切换组织、项目和集群。
  
        <img src="https://docs-download.pingcap.com/media/images/docs/tidb-cloud/tidb-cloud-combo-box.png" width="200" />

    - 左侧导航栏显示的条目现在会根据你在组合框中的当前选择动态调整，帮助你专注于最相关的功能。
    - 为了方便快速访问，**支持**、**通知**和你的账户条目现在会始终显示在所有控制台页面的左侧导航栏底部。

## 2025 年 6 月 4 日

**一般变更**

- [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 在 Microsoft Azure 上现已公开预览。
  
    随着此次发布，TiDB Cloud 现在支持所有三大公有云平台 — AWS、Google Cloud 和 Azure，使你能够在最适合你的业务需求和云战略的地方部署 TiDB Cloud Dedicated 集群。
  
    - AWS 和 Google Cloud 上可用的所有核心功能在 Azure 上都完全支持。
    - Azure 支持目前在三个区域可用：East US 2、Japan East 和 Southeast Asia，更多区域即将推出。
    - Azure 上的 TiDB Cloud Dedicated 集群需要 TiDB v7.5.3 或更高版本。
  
  要快速开始使用 Azure 上的 TiDB Cloud Dedicated，请参见以下文档：
  
    - [在 Azure 上创建 TiDB Cloud Dedicated 集群](/tidb-cloud/create-tidb-cluster.md)
    - [通过 Azure 私有端点连接 TiDB Cloud Dedicated 集群](/tidb-cloud/set-up-private-endpoint-connections-on-azure.md)
    - [将数据导入 Azure 上的 TiDB Cloud Dedicated 集群](/tidb-cloud/import-csv-files.md)

- Prometheus 集成提供更多指标以增强 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的监控能力。
  
    现在你可以将更多指标（如 `tidbcloud_disk_read_latency` 和 `tidbcloud_kv_request_duration`）集成到 Prometheus 中，以跟踪 TiDB Cloud Dedicated 性能的更多方面。
  
    有关可用指标以及如何为现有和新用户启用这些指标的更多信息，请参见[将 TiDB Cloud 与 Prometheus 和 Grafana 集成（Beta）](/tidb-cloud/monitor-prometheus-and-grafana-integration.md#metrics-available-to-prometheus)。

- TiKV [标准](/tidb-cloud/size-your-cluster.md#standard-storage)和[性能](/tidb-cloud/size-your-cluster.md#performance-and-plus-storage)存储定价正式发布。

    折扣期将于 **2025 年 6 月 5 日 00:00 UTC** 结束。之后，价格将恢复到标准价格。有关 TiDB Cloud Dedicated 价格的更多信息，请参见 [TiDB Cloud Dedicated 价格详情](https://www.pingcap.com/tidb-dedicated-pricing-details/#node-cost)。

**控制台变更**

- 增强配置 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的 TiFlash 节点大小时的交互体验。

    现在你可以在创建 TiDB Cloud Dedicated 集群时使用切换开关来控制 TiFlash 配置，使配置体验更加直观和流畅。

## 2025 年 5 月 27 日

**一般变更**

- 支持通过 changefeed 将 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的数据流式传输到 [Apache Pulsar](https://pulsar.apache.org)。

    此功能使你能够将 TiDB Cloud Dedicated 集群与更多下游系统集成，并满足额外的数据集成需求。要使用此功能，请确保你的 TiDB Cloud Dedicated 集群版本为 v7.5.1 或更高版本。

    更多信息，请参见[导出到 Apache Pulsar](/tidb-cloud/changefeed-sink-to-apache-pulsar.md)。

## 2025 年 5 月 13 日

**一般变更**

- [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 现在为 AI 应用提供全文搜索功能（beta）。

    TiDB Cloud Serverless 现在支持全文搜索（beta），使 AI 和检索增强生成（RAG）应用能够通过精确关键词检索内容。这补充了通过语义相似性检索内容的向量搜索。结合这两种方法可以显著提高 RAG 工作流中的检索准确性和答案质量。主要功能包括：

    - 直接文本搜索：无需嵌入即可直接查询字符串列。
    - 多语言支持：自动检测和分析多种语言的文本，即使在同一个表中也无需指定语言。
    - 基于相关性的排名：使用行业标准的 BM25 算法对结果进行排名，以获得最佳相关性。
    - 原生 SQL 兼容性：与全文搜索无缝使用 SQL 功能，如过滤、分组和连接。

  要开始使用，请参见[使用 SQL 进行全文搜索](/tidb-cloud/vector-search-full-text-search-sql.md)或[使用 Python 进行全文搜索](/tidb-cloud/vector-search-full-text-search-python.md)。

- 增加 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的最大 TiFlash 节点存储：

    - 8 vCPU TiFlash，从 2048 GiB 增加到 4096 GiB
    - 32 vCPU TiFlash，从 4096 GiB 增加到 8192 GiB

  此增强提高了 TiDB Cloud Dedicated 集群的分析数据存储容量，提升了工作负载扩展效率，并适应不断增长的数据需求。

    更多信息，请参见 [TiFlash 节点存储](/tidb-cloud/size-your-cluster.md#tiflash-node-storage)。

- 通过提供直观的选项来配置和重新安排维护任务，增强维护窗口配置体验。

    更多信息，请参见[配置维护窗口](/tidb-cloud/configure-maintenance-window.md)。

- 延长 TiKV [标准](/tidb-cloud/size-your-cluster.md#standard-storage)和[性能](/tidb-cloud/size-your-cluster.md#performance-and-plus-storage)存储类型的折扣期。促销现在将于 2025 年 6 月 5 日结束。在此日期之后，价格将恢复到标准费率。

**控制台变更**

- 优化**备份设置**页面布局，改善 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的备份配置体验。

    更多信息，请参见[备份和恢复 TiDB Cloud Dedicated 数据](/tidb-cloud/backup-and-restore.md)。

## 2025 年 4 月 22 日

**一般变更**

- 现在支持将数据导出到阿里云 OSS。

    [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群现在支持使用 [AccessKey 对](https://www.alibabacloud.com/help/en/ram/user-guide/create-an-accesskey-pair)将数据导出到[阿里云对象存储服务（OSS）](https://www.alibabacloud.com/en/product/object-storage-service)。

    更多信息，请参见[从 TiDB Cloud Serverless 导出数据](/tidb-cloud/serverless-export.md#alibaba-cloud-oss)。

## 2025 年 4 月 15 日

**一般变更**

- 支持从[阿里云对象存储服务（OSS）](https://www.alibabacloud.com/en/product/object-storage-service)将数据导入到 [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群。

    此功能简化了向 TiDB Cloud Serverless 的数据迁移。你可以使用 AccessKey 对进行身份验证。

    更多信息，请参见以下文档：

    - [从 Amazon S3、GCS、Azure Blob Storage 或阿里云 OSS 导入 CSV 文件到 TiDB Cloud Serverless](/tidb-cloud/import-csv-files-serverless.md)
    - [从 Amazon S3、GCS、Azure Blob Storage 或阿里云 OSS 导入 Apache Parquet 文件到 TiDB Cloud Serverless](/tidb-cloud/import-parquet-files-serverless.md)

## 2025 年 4 月 1 日

**一般变更**

- [TiDB 节点组](/tidb-cloud/tidb-node-group-overview.md)功能现在在 AWS 和 Google Cloud 上托管的 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群中正式发布（GA）。

    此功能实现了单个集群内的**细粒度计算资源隔离**，帮助你优化多租户或多工作负载场景下的性能和资源分配。

    **主要优势：**

    - **资源隔离**：

        - 将 TiDB 节点分组为逻辑隔离的单元，确保一个组中的工作负载不会影响其他组。
        - 防止应用程序或业务单位之间的资源争用。

    - **简化管理**：

        - 在单个集群内管理所有节点组，减少运维开销。
        - 根据需求独立扩展各个组。

  有关优势的更多信息，请参见[技术博客](https://www.pingcap.com/blog/tidb-cloud-node-groups-scaling-workloads-predictable-performance/)。要开始使用，请参见[管理 TiDB 节点组](/tidb-cloud/tidb-node-group-management.md)。

- 为 AWS 上托管的 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的 TiKV 节点引入[标准存储](/tidb-cloud/size-your-cluster.md#standard-storage)类型。

    标准存储类型适用于大多数工作负载，在性能和成本效益之间提供平衡。

    **主要优势：**

    - **性能提升**：为 Raft 日志保留足够的磁盘资源，减少 Raft 和数据存储之间的 I/O 争用，从而提高 TiKV 的读写性能。
    - **稳定性增强**：将关键的 Raft 操作与数据工作负载隔离，确保更可预测的性能。
    - **成本效益**：与之前的存储类型相比，以具有竞争力的价格提供更高的性能。

    **可用性：**

    标准存储类型自动应用于 2025 年 4 月 1 日或之后在 AWS 上创建的新 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群，支持的版本为（版本 >= 7.5.5、8.1.2 或 8.5.0）。现有集群仍使用之前的[基础存储](/tidb-cloud/size-your-cluster.md#basic-storage)类型，无需迁移。

    标准存储的价格与基础存储不同。更多信息，请参见[定价](https://www.pingcap.com/tidb-dedicated-pricing-details/)。

## 2025 年 3 月 25 日

**控制台变更**

- 支持 [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群的公共端点防火墙规则。

    你现在可以为 TiDB Cloud Serverless 集群配置防火墙规则，以控制通过公共端点的访问。直接在 [TiDB Cloud 控制台](https://tidbcloud.com/)中指定允许的 IP 地址或范围以增强安全性。

    更多信息，请参见[为公共端点配置 TiDB Cloud Serverless 防火墙规则](/tidb-cloud/configure-serverless-firewall-rules-for-public-endpoints.md)。

## 2025 年 3 月 18 日

**一般变更**

- 支持为部署在 Google Cloud 上的 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群创建 TiDB 节点组，以增强资源管理灵活性。

    更多信息，请参见 [TiDB 节点组概述](/tidb-cloud/tidb-node-group-overview.md)。

- 支持在 TiDB Cloud 中存储部署在 AWS 上的 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的数据库审计日志文件。

    你可以直接从 TiDB Cloud 下载这些审计日志文件。请注意，此功能仅在申请后可用。

    更多信息，请参见[数据库审计日志](/tidb-cloud/tidb-cloud-auditing.md)。

- 通过改进多因素认证（MFA）的管理来增强 TiDB Cloud 账户安全性。此功能适用于 TiDB Cloud 的基于密码的登录。

    更多信息，请参见[密码认证](/tidb-cloud/tidb-cloud-password-authentication.md)。

## 2025 年 2 月 18 日

**控制台变更**

- 推出 Connected Care，TiDB Cloud 的新支持服务。

    Connected Care 服务旨在通过现代通信工具、主动支持和先进的 AI 功能加强你与 TiDB Cloud 的连接，提供无缝和以客户为中心的体验。

    Connected Care 服务引入了以下功能：

    - **诊所服务**：先进的监控和诊断，优化性能。
    - **即时通讯中的 AI 聊天**：通过即时通讯（IM）工具获得即时 AI 帮助。
    - **告警和工单更新的即时通讯订阅**：通过即时通讯及时了解告警和工单进展。
    - **支持工单的即时通讯交互**：通过即时通讯工具创建和处理支持工单。

  更多信息，请参见 [Connected Care 概述](/tidb-cloud/connected-care-overview.md)。

- 支持从 GCS 和 Azure Blob Storage 将数据导入到 [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群。

    TiDB Cloud Serverless 现在支持从 Google Cloud Storage (GCS) 和 Azure Blob Storage 导入数据。你可以使用 Google Cloud 服务账号密钥或 Azure 共享访问签名（SAS）令牌进行身份验证。此功能简化了向 TiDB Cloud Serverless 的数据迁移。

    更多信息，请参见[从 Amazon S3、GCS 或 Azure Blob Storage 导入 CSV 文件到 TiDB Cloud Serverless](/tidb-cloud/import-csv-files-serverless.md)和[从 Amazon S3、GCS 或 Azure Blob Storage 导入 Apache Parquet 文件到 TiDB Cloud Serverless](/tidb-cloud/import-parquet-files-serverless.md)。

## 2025 年 1 月 21 日

**控制台变更**

- 支持每个任务将单个本地 CSV 文件（最大 250 MiB）导入到 [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群，从之前的 50 MiB 限制提高。

    更多信息，请参见[将本地文件导入到 TiDB Cloud](/tidb-cloud/tidb-cloud-import-local-files.md)。

## 2025 年 1 月 14 日

**一般变更**

- 支持 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的新 AWS 区域：`雅加达 (ap-southeast-3)`。

- 引入通知功能，使你能够通过 [TiDB Cloud 控制台](https://tidbcloud.com/)即时了解 TiDB Cloud 更新和告警。

    更多信息，请参见[通知](/tidb-cloud/notifications.md)。

## 2025 年 1 月 2 日

**一般变更**

- 支持为 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群创建 TiDB 节点组，以增强资源管理灵活性。

    更多信息，请参见 [TiDB 节点组概述](/tidb-cloud/tidb-node-group-overview.md)。

- 支持通过私有连接（beta）将 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群连接到 AWS 和 Google Cloud 中的通用 Kafka。

    私有连接利用云提供商的 Private Link 或 Private Service Connect 技术，使 TiDB Cloud VPC 中的 changefeed 能够使用私有 IP 地址连接到客户 VPC 中的 Kafka，就像这些 Kafka 直接托管在 TiDB Cloud VPC 中一样。此功能有助于防止 VPC CIDR 冲突并满足安全合规要求。

    - 对于 AWS 中的 Apache Kafka，请按照[在 AWS 中设置自托管 Kafka Private Link 服务](/tidb-cloud/setup-aws-self-hosted-kafka-private-link-service.md)中的说明配置网络连接。

    - 对于 Google Cloud 中的 Apache Kafka，请按照[在 Google Cloud 中设置自托管 Kafka Private Service Connect](/tidb-cloud/setup-self-hosted-kafka-private-service-connect.md)中的说明配置网络连接。
  
  请注意，使用此功能会产生额外的[私有数据链路成本](/tidb-cloud/tidb-cloud-billing-ticdc-rcu.md#private-data-link-cost)。

    更多信息，请参见[导出到 Apache Kafka](/tidb-cloud/changefeed-sink-to-apache-kafka.md#network)。

- 为 Kafka changefeed 引入额外的可配置选项：

    - 支持使用 Debezium 协议。Debezium 是一个用于捕获数据库变更的工具。它将每个捕获的数据库变更转换为称为事件的消息，并将这些事件发送到 Kafka。更多信息，请参见 [TiCDC Debezium 协议](https://docs.pingcap.com/tidb/v8.1/ticdc-debezium)。

    - 支持为所有表定义单个分区调度器，或为不同表定义不同的分区调度器。

    - 为 Kafka 消息的分区分配引入两种新的调度器类型：时间戳和列值。

  更多信息，请参见[导出到 Apache Kafka](/tidb-cloud/changefeed-sink-to-apache-kafka.md)。

- 增强 TiDB Cloud 中的角色：

    - 引入 `Project Viewer` 和 `Organization Billing Viewer` 角色，以增强 TiDB Cloud 上的细粒度访问控制。

    - 重命名以下角色：

        - `Organization Member` 改为 `Organization Viewer`
        - `Organization Billing Admin` 改为 `Organization Billing Manager`
        - `Organization Console Audit Admin` 改为 `Organization Console Audit Manager`

  更多信息，请参见[身份访问管理](/tidb-cloud/manage-user-access.md#organization-roles)。

- [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群的区域高可用性（beta）。

    此功能专为需要最大基础设施冗余和业务连续性的工作负载而设计。主要功能包括：

    - 节点分布在多个可用区，以确保在区域故障时的高可用性。
    - 关键的 OLTP（在线事务处理）组件，如 PD 和 TiKV，在可用区之间复制以实现冗余。
    - 自动故障转移最大限度地减少主要区域故障期间的服务中断。
  
  此功能目前仅在 AWS 东京（ap-northeast-1）区域可用，且只能在集群创建时启用。
  
    更多信息，请参见 [TiDB Cloud Serverless 中的高可用性](/tidb-cloud/serverless-high-availability.md)。

- 将新 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的默认 TiDB 版本从 [v8.1.1](https://docs.pingcap.com/tidb/v8.1/release-8.1.1) 升级到 [v8.1.2](https://docs.pingcap.com/tidb/v8.1/release-8.1.2)。

**控制台变更**

- 加强数据导出服务：

    - 支持通过 [TiDB Cloud 控制台](https://tidbcloud.com/)将数据从 [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 导出到 Google Cloud Storage 和 Azure Blob Storage。

    - 支持通过 [TiDB Cloud 控制台](https://tidbcloud.com/)以 Parquet 文件格式导出数据。

  更多信息，请参见[从 TiDB Cloud Serverless 导出数据](/tidb-cloud/serverless-export.md)和[为 TiDB Cloud Serverless 配置外部存储访问](/tidb-cloud/serverless-external-storage.md)。
