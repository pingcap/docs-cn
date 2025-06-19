---
title: 在 AWS 中设置自托管 Kafka Private Link 服务
summary: 本文档说明如何在 AWS 中为自托管 Kafka 设置 Private Link 服务，以及如何使其与 TiDB Cloud 配合使用。
aliases: ['/tidbcloud/setup-self-hosted-kafka-private-link-service']
---

# 在 AWS 中设置自托管 Kafka Private Link 服务

本文档描述如何在 AWS 中为自托管 Kafka 设置 Private Link 服务，以及如何使其与 TiDB Cloud 配合使用。

该机制的工作原理如下：

1. TiDB Cloud VPC 通过私有端点连接到 Kafka VPC。
2. Kafka 客户端需要直接与所有 Kafka broker 通信。
3. 每个 Kafka broker 映射到 TiDB Cloud VPC 内端点的唯一端口。
4. 利用 Kafka 引导机制和 AWS 资源实现映射。

下图显示了该机制。

![连接到 AWS 自托管 Kafka Private Link 服务](/media/tidb-cloud/changefeed/connect-to-aws-self-hosted-kafka-privatelink-service.jpeg)

本文档提供了一个连接到在 AWS 中跨三个可用区（AZ）部署的 Kafka Private Link 服务的示例。虽然可以基于类似的端口映射原理进行其他配置，但本文档涵盖了 Kafka Private Link 服务的基本设置过程。对于生产环境，建议使用具有增强运维可维护性和可观测性的更具弹性的 Kafka Private Link 服务。

## 前提条件

1. 确保你具有以下授权来在自己的 AWS 账户中设置 Kafka Private Link 服务。

    - 管理 EC2 节点
    - 管理 VPC
    - 管理子网
    - 管理安全组
    - 管理负载均衡器
    - 管理端点服务
    - 连接到 EC2 节点以配置 Kafka 节点

2. 如果你还没有 TiDB Cloud Dedicated 集群，请[创建一个](/tidb-cloud/create-tidb-cluster.md)。

3. 从你的 TiDB Cloud Dedicated 集群获取 Kafka 部署信息。

    1. 在 [TiDB Cloud 控制台](https://tidbcloud.com)中，导航到 TiDB 集群的概览页面，然后在左侧导航栏中点击**数据** > **Changefeed**。
    2. 在概览页面上，找到 TiDB 集群的区域。确保你的 Kafka 集群将部署在相同的区域。
    3. 点击**创建 Changefeed**。
        1. 在**目标**中，选择 **Kafka**。
        2. 在**连接方式**中，选择 **Private Link**。
    4. 记下**继续前的提醒**中的 TiDB Cloud AWS 账户信息。你将使用它来授权 TiDB Cloud 为 Kafka Private Link 服务创建端点。
    5. 选择**可用区数量**。在本示例中，选择 **3 个可用区**。记下你想要部署 Kafka 集群的可用区的 ID。如果你想知道可用区名称和可用区 ID 之间的关系，请参见 [AWS 资源的可用区 ID](https://docs.aws.amazon.com/ram/latest/userguide/working-with-az-ids.html) 查找。
    6. 为你的 Kafka Private Link 服务输入唯一的 **Kafka 广播监听器模式**。
        1. 输入一个唯一的随机字符串。它只能包含数字或小写字母。你稍后将使用它来生成 **Kafka 广播监听器模式**。
        2. 点击**检查使用情况并生成**以检查随机字符串是否唯一，并生成将用于组装 Kafka broker 的 EXTERNAL 广播监听器的 **Kafka 广播监听器模式**。

记下所有部署信息。你稍后需要使用它来配置你的 Kafka Private Link 服务。

下表显示了部署信息的示例。

| 信息     | 值    | 注意    | 
|--------|-----------------|---------------------------|
| 区域    | Oregon (`us-west-2`)    |  不适用 |
| TiDB Cloud AWS 账户的主体 | `arn:aws:iam::<account_id>:root`     |    不适用  |
| 可用区 ID                              | <ul><li>`usw2-az1` </li><li>`usw2-az2` </li><li> `usw2-az3`</li></ul>  | 将可用区 ID 与你的 AWS 账户中的可用区名称对齐。<br/>示例：<ul><li> `usw2-az1` => `us-west-2a` </li><li> `usw2-az2` => `us-west-2c` </li><li>`usw2-az3` => `us-west-2b`</li></ul>  |
| Kafka 广播监听器模式   | 唯一随机字符串：`abc` <br/>为可用区生成的模式：<ul><li> `usw2-az1` => &lt;broker_id&gt;.usw2-az1.abc.us-west-2.aws.3199015.tidbcloud.com:&lt;port&gt; </li><li> `usw2-az2` => &lt;broker_id&gt;.usw2-az2.abc.us-west-2.aws.3199015.tidbcloud.com:&lt;port&gt; </li><li> `usw2-az3` => &lt;broker_id&gt;.usw2-az3.abc.us-west-2.aws.3199015.tidbcloud.com:&lt;port&gt; </li></ul>    | 将可用区名称映射到可用区指定的模式。确保稍后将正确的模式配置到特定可用区中的 broker。<ul><li> `us-west-2a` => &lt;broker_id&gt;.usw2-az1.abc.us-west-2.aws.3199015.tidbcloud.com:&lt;port&gt; </li><li> `us-west-2c` => &lt;broker_id&gt;.usw2-az2.abc.us-west-2.aws.3199015.tidbcloud.com:&lt;port&gt; </li><li> `us-west-2b` => &lt;broker_id&gt;.usw2-az3.abc.us-west-2.aws.3199015.tidbcloud.com:&lt;port&gt; </li></ul>|
## 步骤 1. 设置 Kafka 集群

如果你需要部署新集群，请按照[部署新的 Kafka 集群](#部署新的-kafka-集群)中的说明操作。

如果你需要暴露现有集群，请按照[重新配置运行中的 Kafka 集群](#重新配置运行中的-kafka-集群)中的说明操作。

### 部署新的 Kafka 集群

#### 1. 设置 Kafka VPC

Kafka VPC 需要以下内容：

- 三个用于 broker 的私有子网，每个可用区一个。
- 任意可用区中的一个公共子网，其中有一个堡垒节点，可以连接到互联网和三个私有子网，这使得设置 Kafka 集群变得容易。在生产环境中，你可能有自己的堡垒节点可以连接到 Kafka VPC。

在创建子网之前，根据可用区 ID 和可用区名称的映射在可用区中创建子网。以下面的映射为例。

- `usw2-az1` => `us-west-2a`
- `usw2-az2` => `us-west-2c`
- `usw2-az3` => `us-west-2b`

在以下可用区中创建私有子网：

- `us-west-2a`
- `us-west-2c`
- `us-west-2b`

按照以下步骤创建 Kafka VPC。

**1.1. 创建 Kafka VPC**

1. 转到 [AWS 控制台 > VPC 仪表板](https://console.aws.amazon.com/vpcconsole/home?#vpcs:)，并切换到要部署 Kafka 的区域。

2. 点击**创建 VPC**。在 **VPC 设置**页面上填写以下信息。

    1. 选择**仅 VPC**。
    2. 在**名称标签**中输入标签，例如 `Kafka VPC`。
    3. 选择 **IPv4 CIDR 手动输入**，并输入 IPv4 CIDR，例如 `10.0.0.0/16`。
    4. 其他选项使用默认值。点击**创建 VPC**。
    5. 在 VPC 详细信息页面上，记下 VPC ID，例如 `vpc-01f50b790fa01dffa`。

**1.2. 在 Kafka VPC 中创建私有子网**

1. 转到[子网列表页面](https://console.aws.amazon.com/vpcconsole/home?#subnets:)。
2. 点击**创建子网**。
3. 选择之前记下的 **VPC ID**（在本例中为 `vpc-01f50b790fa01dffa`）。
4. 使用以下信息添加三个子网。建议在子网名称中加入可用区 ID，以便稍后配置 broker 更容易，因为 TiDB Cloud 要求在 broker 的 `advertised.listener` 配置中编码可用区 ID。

    - 在 `us-west-2a` 中的子网 1
        - **子网名称**：`broker-usw2-az1`
        - **可用区**：`us-west-2a`
        - **IPv4 子网 CIDR 块**：`10.0.0.0/18`

    - 在 `us-west-2c` 中的子网 2
        - **子网名称**：`broker-usw2-az2`
        - **可用区**：`us-west-2c`
        - **IPv4 子网 CIDR 块**：`10.0.64.0/18`

    - 在 `us-west-2b` 中的子网 3
        - **子网名称**：`broker-usw2-az3`
        - **可用区**：`us-west-2b`
        - **IPv4 子网 CIDR 块**：`10.0.128.0/18`

5. 点击**创建子网**。显示**子网列表**页面。

**1.3. 在 Kafka VPC 中创建公共子网**

1. 点击**创建子网**。
2. 选择之前记下的 **VPC ID**（在本例中为 `vpc-01f50b790fa01dffa`）。
3. 使用以下信息在任意可用区中添加公共子网：

   - **子网名称**：`bastion`
   - **IPv4 子网 CIDR 块**：`10.0.192.0/18`

4. 将堡垒子网配置为公共子网。

    1. 转到 [VPC 仪表板 > 互联网网关](https://console.aws.amazon.com/vpcconsole/home#igws:)。创建一个名为 `kafka-vpc-igw` 的互联网网关。
    2. 在**互联网网关详细信息**页面上，在**操作**中，点击**连接到 VPC** 将互联网网关连接到 Kafka VPC。
    3. 转到 [VPC 仪表板 > 路由表](https://console.aws.amazon.com/vpcconsole/home#CreateRouteTable:)。在 Kafka VPC 中创建一个到互联网网关的路由表，并添加一个具有以下信息的新路由：

       - **名称**：`kafka-vpc-igw-route-table`
       - **VPC**：`Kafka VPC`
       - **路由**：
           - **目标**：`0.0.0.0/0`
           - **目标**：`互联网网关`，`kafka-vpc-igw`

    4. 将路由表附加到堡垒子网。在路由表的**详细信息**页面上，点击**子网关联** > **编辑子网关联**以添加堡垒子网并保存更改。

#### 2. 设置 Kafka broker

**2.1. 创建堡垒节点**

转到 [EC2 列表页面](https://console.aws.amazon.com/ec2/home#Instances:)。在堡垒子网中创建堡垒节点。

- **名称**：`bastion-node`
- **Amazon 机器映像**：`Amazon linux`
- **实例类型**：`t2.small`
- **密钥对**：`kafka-vpc-key-pair`。创建一个名为 `kafka-vpc-key-pair` 的新密钥对。将 **kafka-vpc-key-pair.pem** 下载到本地以供稍后配置。
- 网络设置

    - **VPC**：`Kafka VPC`
    - **子网**：`bastion`
    - **自动分配公共 IP**：`启用`
    - **安全组**：创建一个新的安全组，允许从任何地方进行 SSH 登录。在生产环境中，你可以为了安全起见缩小规则范围。

**2.2. 创建 broker 节点**

转到 [EC2 列表页面](https://console.aws.amazon.com/ec2/home#Instances:)。在 broker 子网中创建三个 broker 节点，每个可用区一个。

- 在子网 `broker-usw2-az1` 中的 Broker 1

    - **名称**：`broker-node1`
    - **Amazon 机器映像**：`Amazon linux`
    - **实例类型**：`t2.large`
    - **密钥对**：重用 `kafka-vpc-key-pair`
    - 网络设置

        - **VPC**：`Kafka VPC`
        - **子网**：`broker-usw2-az1`
        - **自动分配公共 IP**：`禁用`
        - **安全组**：创建一个新的安全组，允许来自 Kafka VPC 的所有 TCP。在生产环境中，你可以为了安全起见缩小规则范围。
            - **协议**：`TCP`
            - **端口范围**：`0 - 65535`
            - **源**：`10.0.0.0/16`

- 在子网 `broker-usw2-az2` 中的 Broker 2

    - **名称**：`broker-node2`
    - **Amazon 机器映像**：`Amazon linux`
    - **实例类型**：`t2.large`
    - **密钥对**：重用 `kafka-vpc-key-pair`
    - 网络设置

        - **VPC**：`Kafka VPC`
        - **子网**：`broker-usw2-az2`
        - **自动分配公共 IP**：`禁用`
        - **安全组**：创建一个新的安全组，允许来自 Kafka VPC 的所有 TCP。在生产环境中，你可以为了安全起见缩小规则范围。
            - **协议**：`TCP`
            - **端口范围**：`0 - 65535`
            - **源**：`10.0.0.0/16`

- 在子网 `broker-usw2-az3` 中的 Broker 3

    - **名称**：`broker-node3`
    - **Amazon 机器映像**：`Amazon linux`
    - **实例类型**：`t2.large`
    - **密钥对**：重用 `kafka-vpc-key-pair`
    - 网络设置

        - **VPC**：`Kafka VPC`
        - **子网**：`broker-usw2-az3`
        - **自动分配公共 IP**：`禁用`
        - **安全组**：创建一个新的安全组，允许来自 Kafka VPC 的所有 TCP。在生产环境中，你可以为了安全起见缩小规则范围。
            - **协议**：`TCP`
            - **端口范围**：`0 - 65535`
            - **源**：`10.0.0.0/16`

**2.3. 准备 Kafka 运行时二进制文件**

1. 转到堡垒节点的详细信息页面。获取**公共 IPv4 地址**。使用之前下载的 `kafka-vpc-key-pair.pem` 通过 SSH 登录到节点。

    ```shell
    chmod 400 kafka-vpc-key-pair.pem
    ssh -i "kafka-vpc-key-pair.pem" ec2-user@{bastion_public_ip} # 将 {bastion_public_ip} 替换为你的堡垒节点的 IP 地址，例如 54.186.149.187
    scp -i "kafka-vpc-key-pair.pem" kafka-vpc-key-pair.pem ec2-user@{bastion_public_ip}:~/
    ```

2. 下载二进制文件。

    ```shell
    # 下载 Kafka 和 OpenJDK，然后解压文件。你可以根据自己的偏好选择二进制版本。
    wget https://archive.apache.org/dist/kafka/3.7.1/kafka_2.13-3.7.1.tgz
    tar -zxf kafka_2.13-3.7.1.tgz
    wget https://download.java.net/java/GA/jdk22.0.2/c9ecb94cd31b495da20a27d4581645e8/9/GPL/openjdk-22.0.2_linux-x64_bin.tar.gz
    tar -zxf openjdk-22.0.2_linux-x64_bin.tar.gz
    ```

3. 将二进制文件复制到每个 broker 节点。

    ```shell
    # 将 {broker-node1-ip} 替换为你的 broker-node1 IP 地址
    scp -i "kafka-vpc-key-pair.pem" kafka_2.13-3.7.1.tgz ec2-user@{broker-node1-ip}:~/
    ssh -i "kafka-vpc-key-pair.pem" ec2-user@{broker-node1-ip} "tar -zxf kafka_2.13-3.7.1.tgz"
    scp -i "kafka-vpc-key-pair.pem" openjdk-22.0.2_linux-x64_bin.tar.gz ec2-user@{broker-node1-ip}:~/
    ssh -i "kafka-vpc-key-pair.pem" ec2-user@{broker-node1-ip} "tar -zxf openjdk-22.0.2_linux-x64_bin.tar.gz"

    # 将 {broker-node2-ip} 替换为你的 broker-node2 IP 地址
    scp -i "kafka-vpc-key-pair.pem" kafka_2.13-3.7.1.tgz ec2-user@{broker-node2-ip}:~/
    ssh -i "kafka-vpc-key-pair.pem" ec2-user@{broker-node2-ip} "tar -zxf kafka_2.13-3.7.1.tgz"
    scp -i "kafka-vpc-key-pair.pem" openjdk-22.0.2_linux-x64_bin.tar.gz ec2-user@{broker-node2-ip}:~/
    ssh -i "kafka-vpc-key-pair.pem" ec2-user@{broker-node2-ip} "tar -zxf openjdk-22.0.2_linux-x64_bin.tar.gz"

    # 将 {broker-node3-ip} 替换为你的 broker-node3 IP 地址
    scp -i "kafka-vpc-key-pair.pem" kafka_2.13-3.7.1.tgz ec2-user@{broker-node3-ip}:~/
    ssh -i "kafka-vpc-key-pair.pem" ec2-user@{broker-node3-ip} "tar -zxf kafka_2.13-3.7.1.tgz"
    scp -i "kafka-vpc-key-pair.pem" openjdk-22.0.2_linux-x64_bin.tar.gz ec2-user@{broker-node3-ip}:~/
    ssh -i "kafka-vpc-key-pair.pem" ec2-user@{broker-node3-ip} "tar -zxf openjdk-22.0.2_linux-x64_bin.tar.gz"
    ```
