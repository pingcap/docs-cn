---
title: 选择集群套餐
summary: 了解如何在 TiDB Cloud 上选择集群套餐。
aliases: ['/tidbcloud/developer-tier-cluster']
---

# 选择集群套餐

集群套餐决定了集群的吞吐量和性能。

TiDB Cloud 提供以下两种集群套餐选项。在创建集群之前，您需要考虑哪个选项更适合您的需求。

- [TiDB Cloud Serverless](#tidb-cloud-serverless)
- [TiDB Cloud Dedicated](#tidb-cloud-dedicated)

## TiDB Cloud Serverless

<!--To be confirmed-->
TiDB Cloud Serverless 是一个完全托管的多租户 TiDB 产品。它提供即时、自动扩展的 MySQL 兼容数据库，并提供慷慨的免费套餐，超出免费限制后按使用量计费。

### 集群方案

TiDB Cloud Serverless 提供两种服务方案以满足不同用户的需求。无论您是刚刚开始使用，还是需要扩展以满足不断增长的应用程序需求，这些服务方案都能提供您所需的灵活性和能力。

#### 免费集群方案

免费集群方案非常适合刚开始使用 TiDB Cloud Serverless 的用户。它为开发者和小型团队提供以下基本功能：

- **免费**：此方案完全免费，无需信用卡即可开始使用。
- **存储**：提供初始 5 GiB 的行存储和 5 GiB 的列存储。
- **请求单位**：包含 50 百万[请求单位 (RUs)](/tidb-cloud/tidb-cloud-glossary.md#request-unit) 用于数据库操作。
- **轻松升级**：随着需求增长，可以平滑过渡到[可扩展集群方案](#可扩展集群方案)。

#### 可扩展集群方案

对于工作负载不断增长并需要实时扩展的应用程序，可扩展集群方案通过以下功能提供灵活性和性能，以跟上您的业务增长：

- **增强功能**：包含免费集群方案的所有功能，同时具备处理更大和更复杂工作负载的能力，以及高级安全功能。
- **自动扩展**：自动调整存储和计算资源，以高效满足不断变化的工作负载需求。
- **可预测定价**：虽然此方案需要信用卡，但您只需为使用的资源付费，确保成本效益的可扩展性。

### 使用配额

对于 TiDB Cloud 中的每个组织，默认情况下您最多可以创建五个[免费集群](#免费集群方案)。要创建更多 TiDB Cloud Serverless 集群，您需要添加信用卡并创建[可扩展集群](#可扩展集群方案)。

对于您组织中的前五个 TiDB Cloud Serverless 集群，无论是免费还是可扩展集群，TiDB Cloud 都为每个集群提供以下免费使用配额：

- 行存储：5 GiB
- 列存储：5 GiB
- 请求单位 (RUs)：每月 50 百万 RUs

请求单位 (RU) 是用于表示单个数据库请求消耗的资源量的度量单位。请求消耗的 RU 数量取决于各种因素，如操作类型或正在检索或修改的数据量。

一旦集群达到其使用配额，它会立即拒绝任何新的连接尝试，直到您[增加配额](/tidb-cloud/manage-serverless-spend-limit.md#update-spending-limit)或在新月份开始时重置使用量。在达到配额之前建立的现有连接将保持活动状态，但会经历限流。例如，当免费集群的行存储超过 5 GiB 时，集群会自动限制任何新的连接尝试。

要了解不同资源（包括读取、写入、SQL CPU 和网络出口）的 RU 消耗、定价详情和限流信息，请参见 [TiDB Cloud Serverless 定价详情](https://www.pingcap.com/tidb-cloud-serverless-pricing-details)。

### 用户名前缀

<!--Important: Do not update the section name "User name prefix" because this section is referenced by TiDB backend error messages.-->

对于每个 TiDB Cloud Serverless 集群，TiDB Cloud 生成一个唯一的前缀以区分它与其他集群。

每当您使用或设置数据库用户名时，您必须在用户名中包含前缀。例如，假设您的集群前缀是 `3pTAoNNegb47Uc8`。

- 要连接到您的集群：

    ```shell
    mysql -u '3pTAoNNegb47Uc8.root' -h <host> -P 4000 -D test --ssl-mode=VERIFY_IDENTITY --ssl-ca=<CA_root_path> -p
    ```

    > **注意：**
    >
    > TiDB Cloud Serverless 需要 TLS 连接。要在您的系统上找到 CA 根路径，请参见[根证书默认路径](/tidb-cloud/secure-connections-to-serverless-clusters.md#root-certificate-default-path)。

- 要创建数据库用户：

    ```sql
    CREATE USER '3pTAoNNegb47Uc8.jeffrey';
    ```

要获取集群的前缀，请执行以下步骤：

1. 导航到[**集群**](https://tidbcloud.com/project/clusters)页面。
2. 点击目标集群的名称进入其概览页面，然后点击右上角的**连接**。此时会显示一个连接对话框。
3. 在对话框中，从连接字符串中获取前缀。

### TiDB Cloud Serverless 特殊条款和条件

某些 TiDB Cloud 功能在 TiDB Cloud Serverless 上部分支持或不支持。详细信息请参见 [TiDB Cloud Serverless 限制](/tidb-cloud/serverless-limitations.md)。

## TiDB Cloud Dedicated

TiDB Cloud Dedicated 适用于生产环境，具有跨可用区高可用性、水平扩展和 [HTAP](https://en.wikipedia.org/wiki/Hybrid_transactional/analytical_processing) 的优势。

对于 TiDB Cloud Dedicated 集群，您可以根据业务需求轻松自定义 TiDB、TiKV 和 TiFlash 的集群大小。对于每个 TiKV 节点和 TiFlash 节点，节点上的数据会在不同的可用区中复制和分布，以实现[高可用性](/tidb-cloud/high-availability-with-multi-az.md)。

要创建 TiDB Cloud Dedicated 集群，您需要[添加付款方式](/tidb-cloud/tidb-cloud-billing.md#payment-method)或[申请概念验证 (PoC) 试用](/tidb-cloud/tidb-cloud-poc.md)。

> **注意：**
>
> 集群创建后，您无法减少节点存储。
