---
title: 导出到 Apache Pulsar
summary: 本文档说明如何创建 changefeed 将数据从 TiDB Cloud 流式传输到 Apache Pulsar。它包括限制、前提条件以及为 Apache Pulsar 配置 changefeed 的步骤。该过程涉及设置网络连接和配置 changefeed 规格。
---

# 导出到 Apache Pulsar

本文档描述如何创建 changefeed 将数据从 TiDB Cloud 流式传输到 Apache Pulsar。

> **注意：**
>
> - 要使用 changefeed 功能将数据复制到 Apache Pulsar，请确保你的 TiDB Cloud Dedicated 集群版本为 v7.5.1 或更高版本。
> - 对于 [TiDB Cloud Serverless 集群](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)，changefeed 功能不可用。

## 限制

- 每个 TiDB Cloud 集群最多可以创建 100 个 changefeed。
- 目前，TiDB Cloud 不支持上传自签名 TLS 证书来连接 Pulsar broker。
- 由于 TiDB Cloud 使用 TiCDC 建立 changefeed，因此它具有与 [TiCDC 相同的限制](https://docs.pingcap.com/tidb/stable/ticdc-overview#unsupported-scenarios)。
- 如果要复制的表没有主键或非空唯一索引，在某些重试场景下，复制过程中缺少唯一约束可能导致下游插入重复数据。
- 目前，TiCDC 不会自动创建 Pulsar 主题。在向主题发送事件之前，请确保该主题在 Pulsar 中存在。

## 前提条件

在创建 changefeed 将数据流式传输到 Apache Pulsar 之前，你需要完成以下前提条件：

- 设置网络连接
- 添加 Pulsar ACL 授权的权限
- 在 Apache Pulsar 中手动创建主题，或在 Apache Pulsar broker 配置中启用 [`allowAutoTopicCreation`](https://pulsar.apache.org/reference/#/4.0.x/config/reference-configuration-broker?id=allowautotopiccreation)

### 网络

确保你的 TiDB 集群可以连接到 Apache Pulsar 服务。你可以选择以下连接方法之一：

- VPC 对等连接：需要进行网络规划以避免潜在的 VPC CIDR 冲突，并考虑安全问题。
- 公共 IP：适用于 Pulsar 公布公共 IP 的设置。此方法不建议在生产环境中使用，需要仔细考虑安全问题。

<SimpleTab>
<div label="VPC 对等连接">

如果你的 Apache Pulsar 服务位于没有互联网访问的 AWS VPC 中，请执行以下步骤：

1. 在 Apache Pulsar 服务的 VPC 和你的 TiDB 集群之间[设置 VPC 对等连接](/tidb-cloud/set-up-vpc-peering-connections.md)。
2. 修改与 Apache Pulsar 服务关联的安全组的入站规则。

    你必须将 TiDB Cloud 集群所在区域的 CIDR 添加到入站规则中。可以在 **VPC 对等连接**页面找到 CIDR。这样做可以允许流量从你的 TiDB 集群流向 Pulsar broker。

3. 如果 Apache Pulsar URL 包含主机名，你需要允许 TiDB Cloud 解析 Apache Pulsar broker 的 DNS 主机名。

    1. 按照[为 VPC 对等连接启用 DNS 解析](https://docs.aws.amazon.com/vpc/latest/peering/vpc-peering-dns.html)中的步骤操作。
    2. 启用**接受者 DNS 解析**选项。

如果你的 Apache Pulsar 服务位于没有互联网访问的 Google Cloud VPC 中，请执行以下步骤：

1. 在 Apache Pulsar 服务的 VPC 和你的 TiDB 集群之间[设置 VPC 对等连接](/tidb-cloud/set-up-vpc-peering-connections.md)。
2. 修改 Apache Pulsar 所在 VPC 的入站防火墙规则。

    你必须将 TiDB Cloud 集群所在区域的 CIDR 添加到入站防火墙规则中。可以在 **VPC 对等连接**页面找到 CIDR。这样做可以允许流量从你的 TiDB 集群流向 Pulsar broker。

</div>
<div label="公共 IP">

如果你想为 Apache Pulsar 服务提供公共 IP 访问，请为所有 Pulsar broker 分配公共 IP 地址。

**不建议**在生产环境中使用公共 IP。

</div>
</SimpleTab>

### 在 Apache Pulsar 中创建主题

目前，TiCDC 不会自动创建 Pulsar 主题。你需要在创建 changefeed 之前在 Pulsar 中创建所需的主题。主题的数量和命名取决于你首选的分发模式：

- 要将所有 Pulsar 消息分发到单个主题：创建一个具有你首选名称的主题。
- 要将每个表的 Pulsar 消息分发到专用主题，为每个要复制的表创建格式为 `<主题前缀><数据库名称><分隔符><表名称><主题后缀>` 的主题。
- 要将数据库的 Pulsar 消息分发到专用主题，为每个要复制的数据库创建格式为 `<主题前缀><数据库名称><主题后缀>` 的主题。

根据你的配置，你可能还需要一个用于非行事件（如架构更改）的默认主题。

更多信息，请参见 Apache Pulsar 文档中的[如何创建主题](https://pulsar.apache.org/docs/4.0.x/tutorials-topic/)。

## 步骤 1. 打开 Apache Pulsar 的 Changefeed 页面

1. 登录 [TiDB Cloud 控制台](https://tidbcloud.com)。
2. 导航到将作为 changefeed 事件源的 TiDB 集群的概览页面，然后在左侧导航栏中点击**数据** > **Changefeed**。
3. 点击**创建 Changefeed**。

## 步骤 2. 配置 changefeed 目标

1. 在**目标**部分，选择 **Pulsar**。
2. 在**连接**部分，输入以下信息：

    - **目标协议**：选择 **Pulsar** 或 **Pulsar+SSL**。
    - **连接方式**：根据你计划如何连接到 Pulsar 端点，选择 **VPC 对等连接**或**公共**。
    - **Pulsar Broker**：输入 Pulsar broker 的端点。使用冒号分隔端口和域名或 IP 地址，例如 `example.org:6650`。

3. 在**认证**部分，根据你的 Pulsar 认证配置选择 **Auth Type** 选项。根据你的选择输入所需的凭据信息。
4. 可选：在**高级设置**部分，配置其他设置：

    - **压缩**：为此 changefeed 中的数据选择可选的压缩算法。
    - **每批最大消息数**和**最大发布延迟**：指定发送到 Pulsar 的事件消息的批处理。**每批最大消息数**设置每批的最大消息数，而**最大发布延迟**设置发送批次前的最大等待时间。
    - **连接超时**：调整建立到 Pulsar 的 TCP 连接的超时时间。
    - **操作超时**：调整使用 TiCDC Pulsar 客户端启动操作的超时时间。
    - **发送超时**：调整 TiCDC Pulsar 生产者发送消息的超时时间。

5. 点击**下一步**以测试网络连接。如果测试成功，你将进入下一步。

## 步骤 3. 配置 changefeed 复制

1. 自定义**表过滤器**以过滤要复制的表。有关规则语法，请参考[表过滤规则](/table-filter.md)。

    - **过滤规则**：你可以在此列中设置过滤规则。默认有一个规则 `*.*`，表示复制所有表。当你添加新规则时，TiDB Cloud 会查询 TiDB 中的所有表，并仅在右侧框中显示匹配规则的表。你最多可以添加 100 个过滤规则。
    - **具有有效键的表**：此列显示具有有效键（包括主键或唯一索引）的表。
    - **没有有效键的表**：此列显示缺少主键或唯一键的表。这些表在复制过程中会带来挑战，因为缺少唯一标识符可能会导致下游处理重复事件时数据不一致。为确保数据一致性，建议在开始复制之前为这些表添加唯一键或主键。或者，你可以添加过滤规则来排除这些表。例如，你可以使用规则 `"!test.tbl1"` 排除表 `test.tbl1`。

2. 自定义**事件过滤器**以过滤要复制的事件。

    - **匹配表**：你可以在此列中设置事件过滤器将应用于哪些表。规则语法与前面的**表过滤器**区域使用的语法相同。每个 changefeed 最多可以添加 10 个事件过滤规则。
    - **忽略的事件**：你可以设置事件过滤器将从 changefeed 中排除的事件类型。

3. 在**开始复制位置**区域，选择 changefeed 开始将数据复制到 Pulsar 的起点：

    - **从现在开始复制**：changefeed 将从当前点开始复制数据。
    - **从特定 TSO 开始复制**：changefeed 将从指定的 [TSO](/tso.md) 开始复制数据。指定的 TSO 必须在[垃圾回收安全点](/read-historical-data.md#tidb-如何管理数据版本)内。
    - **从特定时间开始复制**：changefeed 将从指定的时间戳开始复制数据。指定的时间戳必须在垃圾回收安全点内。

4. 在**数据格式**区域，选择你想要的 Pulsar 消息格式。

    - Canal-JSON 是一种易于解析的纯 JSON 文本格式。更多信息，请参见 [TiCDC Canal-JSON 协议](https://docs.pingcap.com/tidb/stable/ticdc-canal-json/)。

    - 要在 Pulsar 消息正文中添加 TiDB 扩展字段，请启用 **TiDB 扩展**选项。更多信息，请参见 [TiCDC Canal-JSON 协议中的 TiDB 扩展字段](https://docs.pingcap.com/tidb/stable/ticdc-canal-json/#tidb-extension-field)。

5. 在**主题分发**区域，选择分发模式，然后根据模式填写主题名称配置。

    分发模式控制 changefeed 如何将事件消息分发到 Pulsar 主题，可以将所有消息发送到一个主题，或按表或按数据库发送到特定主题。

    > **注意：**
    >
    > 当你选择 Pulsar 作为下游时，changefeed 不会自动创建主题。你必须提前创建所需的主题。

    - **将所有变更日志发送到一个指定的 Pulsar 主题**

        如果你希望 changefeed 将所有消息发送到单个 Pulsar 主题，请选择此模式。你可以在**主题名称**字段中指定主题名称。

    - **按表将变更日志分发到 Pulsar 主题**

        如果你希望 changefeed 将每个表的所有 Pulsar 消息发送到专用的 Pulsar 主题，请选择此模式。你可以通过设置**主题前缀**、数据库名称和表名称之间的**分隔符**以及**主题后缀**来为表指定主题名称。例如，如果你将分隔符设置为 `_`，Pulsar 消息将被发送到格式为 `<主题前缀><数据库名称>_<表名称><主题后缀>` 的主题。你需要提前在 Pulsar 上创建这些主题。

        对于非行事件（如创建架构事件）的变更日志，你可以在**默认主题名称**字段中指定主题名称。changefeed 将非行事件发送到此主题以收集此类变更日志。

    - **按数据库将变更日志分发到 Pulsar 主题**

        如果你希望 changefeed 将每个数据库的所有 Pulsar 消息发送到专用的 Pulsar 主题，请选择此模式。你可以通过设置**主题前缀**和**主题后缀**来为数据库指定主题名称。

        对于非行事件（如已解析的 Ts 事件）的变更日志，你可以在**默认主题名称**字段中指定主题名称。changefeed 将非行事件发送到此主题以收集此类变更日志。

    由于 Pulsar 支持多租户，如果租户和命名空间与默认值不同，你可能还需要设置 **Pulsar 租户**和 **Pulsar 命名空间**。

6. 在**分区分发**区域，你可以决定将 Pulsar 消息发送到哪个分区。你可以定义**所有表使用单个分区调度器**或**不同表使用不同的分区调度器**。TiDB Cloud 提供四个规则选项来将变更事件分发到 Pulsar 分区：

    - **主键或唯一索引**

        如果你希望 changefeed 将表的 Pulsar 消息发送到不同的分区，请选择此分发方法。行变更日志的主键或索引值决定将变更日志发送到哪个分区。此分发方法提供更好的分区平衡，并确保行级有序性。

    - **表**

        如果你希望 changefeed 将表的 Pulsar 消息发送到一个 Pulsar 分区，请选择此分发方法。行变更日志的表名决定将变更日志发送到哪个分区。此分发方法确保表有序性，但可能导致分区不平衡。

    - **时间戳**

        如果你希望 changefeed 根据时间戳将 Pulsar 消息发送到不同的 Pulsar 分区，请选择此分发方法。行变更日志的 commitTs 决定将变更日志发送到哪个分区。此分发方法提供更好的分区平衡，并确保每个分区内的有序性。但是，数据项的多个更改可能会被发送到不同的分区，不同消费者的消费进度可能不同，这可能导致数据不一致。因此，消费者需要在消费之前按 commitTs 对来自多个分区的数据进行排序。

    - **列值**

        如果你希望 changefeed 将表的 Pulsar 消息发送到不同的分区，请选择此分发方法。行变更日志的指定列值将决定将变更日志发送到哪个分区。此分发方法确保每个分区内的有序性，并保证具有相同列值的变更日志被发送到同一个分区。

7. 点击**下一步**。

## 步骤 4. 配置规格并审查

1. 在**规格和名称**部分：

    - 为 changefeed 指定[复制容量单位（RCU）](/tidb-cloud/tidb-cloud-billing-ticdc-rcu.md)的数量。
    - 为 changefeed 输入名称。

2. 审查所有 changefeed 配置。

    - 如果发现问题，你可以返回前面的步骤解决问题。
    - 如果没有问题，你可以点击**提交**创建 changefeed。
