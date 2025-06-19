---
title: 同步数据到 Apache Kafka
summary: 本文档说明如何创建 changefeed 将数据从 TiDB Cloud 同步到 Apache Kafka。它包括限制、前提条件以及为 Apache Kafka 配置 changefeed 的步骤。该过程涉及设置网络连接、为 Kafka ACL 授权添加权限以及配置 changefeed 规格。
---

# 同步数据到 Apache Kafka

本文档描述如何创建 changefeed 将数据从 TiDB Cloud 同步到 Apache Kafka。

> **注意：**
>
> - 要使用 changefeed 功能，请确保你的 TiDB Cloud Dedicated 集群版本是 v6.1.3 或更高版本。
> - 对于 [TiDB Cloud Serverless 集群](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)，changefeed 功能不可用。

## 限制

- 对于每个 TiDB Cloud 集群，你最多可以创建 100 个 changefeed。
- 目前，TiDB Cloud 不支持上传自签名 TLS 证书来连接 Kafka broker。
- 由于 TiDB Cloud 使用 TiCDC 建立 changefeed，它具有与 TiCDC 相同的[限制](https://docs.pingcap.com/tidb/stable/ticdc-overview#unsupported-scenarios)。
- 如果要复制的表没有主键或非空唯一索引，在某些重试场景中，由于复制过程中缺少唯一约束，可能会导致下游插入重复数据。
- 如果你选择 Private Link 或 Private Service Connect 作为网络连接方式，请确保你的 TiDB 集群版本满足以下要求：

    - 对于 v6.5.x：版本 v6.5.9 或更高版本
    - 对于 v7.1.x：版本 v7.1.4 或更高版本
    - 对于 v7.5.x：版本 v7.5.1 或更高版本
    - 对于 v8.1.x：支持所有 v8.1.x 及更高版本
- 如果你想使用 Debezium 作为数据格式，请确保你的 TiDB 集群版本是 v8.1.0 或更高版本。
- 对于 Kafka 消息的分区分布，请注意以下事项：

    - 如果你想通过指定索引名称将变更日志按主键或索引值分发到 Kafka 分区，请确保你的 TiDB 集群版本是 v7.5.0 或更高版本。
    - 如果你想将变更日志按列值分发到 Kafka 分区，请确保你的 TiDB 集群版本是 v7.5.0 或更高版本。

## 前提条件

在创建 changefeed 将数据同步到 Apache Kafka 之前，你需要完成以下前提条件：

- 设置网络连接
- 为 Kafka ACL 授权添加权限

### 网络

确保你的 TiDB 集群可以连接到 Apache Kafka 服务。你可以选择以下连接方式之一：

- Private Connect：适用于避免 VPC CIDR 冲突并满足安全合规要求，但会产生额外的[私有数据链路成本](/tidb-cloud/tidb-cloud-billing-ticdc-rcu.md#私有数据链路成本)。
- VPC 对等连接：适用于成本效益高的选项，但需要管理潜在的 VPC CIDR 冲突和安全考虑。
- 公共 IP：适用于快速设置。

<SimpleTab>
<div label="Private Connect">

Private Connect 利用云提供商的 **Private Link** 或 **Private Service Connect** 技术，使你的 VPC 中的资源能够使用私有 IP 地址连接到其他 VPC 中的服务，就像这些服务直接托管在你的 VPC 中一样。

TiDB Cloud 目前仅支持自托管 Kafka 的 Private Connect。它不支持直接集成 MSK、Confluent Kafka 或其他 Kafka SaaS 服务。要通过 Private Connect 连接到这些 Kafka SaaS 服务，你可以部署 [kafka-proxy](https://github.com/grepplabs/kafka-proxy) 作为中介，有效地将 Kafka 服务公开为自托管 Kafka。有关详细示例，请参见[在 Google Cloud 中使用 Kafka-proxy 设置自托管 Kafka Private Service Connect](/tidb-cloud/setup-self-hosted-kafka-private-service-connect.md#使用-kafka-proxy-设置自托管-kafka-private-service-connect)。这种设置在所有 Kafka SaaS 服务中都类似。

- 如果你的 Apache Kafka 服务托管在 AWS 中，请按照[在 AWS 中设置自托管 Kafka Private Link 服务](/tidb-cloud/setup-aws-self-hosted-kafka-private-link-service.md)确保网络连接正确配置。设置完成后，在 TiDB Cloud 控制台中提供以下信息以创建 changefeed：

    - Kafka 广播监听器模式中的 ID
    - 端点服务名称
    - 引导端口

- 如果你的 Apache Kafka 服务托管在 Google Cloud 中，请按照[在 Google Cloud 中设置自托管 Kafka Private Service Connect](/tidb-cloud/setup-self-hosted-kafka-private-service-connect.md)确保网络连接正确配置。设置完成后，在 TiDB Cloud 控制台中提供以下信息以创建 changefeed：

    - Kafka 广播监听器模式中的 ID
    - 服务附件
    - 引导端口

- 如果你的 Apache Kafka 服务托管在 Azure 中，请按照[在 Azure 中设置自托管 Kafka Private Link 服务](/tidb-cloud/setup-azure-self-hosted-kafka-private-link-service.md)确保网络连接正确配置。设置完成后，在 TiDB Cloud 控制台中提供以下信息以创建 changefeed：

    - Kafka 广播监听器模式中的 ID
    - Private Link 服务的别名
    - 引导端口

</div>
<div label="VPC 对等连接">

如果你的 Apache Kafka 服务在没有互联网访问的 AWS VPC 中，请执行以下步骤：

1. [设置 VPC 对等连接](/tidb-cloud/set-up-vpc-peering-connections.md)，连接 Apache Kafka 服务的 VPC 和你的 TiDB 集群。
2. 修改与 Apache Kafka 服务关联的安全组的入站规则。

    你必须将你的 TiDB Cloud 集群所在区域的 CIDR 添加到入站规则中。CIDR 可以在 **VPC 对等连接**页面找到。这样做可以允许流量从你的 TiDB 集群流向 Kafka broker。

3. 如果 Apache Kafka URL 包含主机名，你需要允许 TiDB Cloud 能够解析 Apache Kafka broker 的 DNS 主机名。

    1. 按照[为 VPC 对等连接启用 DNS 解析](https://docs.aws.amazon.com/vpc/latest/peering/vpc-peering-dns.html)中的步骤操作。
    2. 启用**接受者 DNS 解析**选项。

如果你的 Apache Kafka 服务在没有互联网访问的 Google Cloud VPC 中，请执行以下步骤：

1. [设置 VPC 对等连接](/tidb-cloud/set-up-vpc-peering-connections.md)，连接 Apache Kafka 服务的 VPC 和你的 TiDB 集群。
2. 修改 Apache Kafka 所在 VPC 的入站防火墙规则。

    你必须将你的 TiDB Cloud 集群所在区域的 CIDR 添加到入站防火墙规则中。CIDR 可以在 **VPC 对等连接**页面找到。这样做可以允许流量从你的 TiDB 集群流向 Kafka broker。

</div>
<div label="公共 IP">

如果你想为你的 Apache Kafka 服务提供公共 IP 访问，请为所有 Kafka broker 分配公共 IP 地址。

不建议在生产环境中使用公共 IP。

</div>
</SimpleTab>

### Kafka ACL 授权

要允许 TiDB Cloud changefeed 将数据同步到 Apache Kafka 并自动创建 Kafka 主题，请确保在 Kafka 中添加了以下权限：

- 为 Kafka 中的主题资源类型添加了 `Create` 和 `Write` 权限。
- 为 Kafka 中的集群资源类型添加了 `DescribeConfigs` 权限。

例如，如果你的 Kafka 集群在 Confluent Cloud 中，你可以参见 Confluent 文档中的[资源](https://docs.confluent.io/platform/current/kafka/authorization.html#resources)和[添加 ACL](https://docs.confluent.io/platform/current/kafka/authorization.html#adding-acls)了解更多信息。
