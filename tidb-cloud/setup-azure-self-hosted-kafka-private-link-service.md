---
title: 在 Azure 中设置自托管 Kafka Private Link 服务
summary: 本文档说明如何在 Azure 中为自托管 Kafka 设置 Private Link 服务，以及如何使其与 TiDB Cloud 配合使用。
---

# 在 Azure 中设置自托管 Kafka Private Link 服务

本文档描述如何在 Azure 中为自托管 Kafka 设置 Private Link 服务，以及如何使其与 TiDB Cloud 配合使用。

工作机制如下：

1. TiDB Cloud 虚拟网络通过私有端点连接到 Kafka 虚拟网络。
2. Kafka 客户端需要直接与所有 Kafka broker 通信。
3. 每个 Kafka broker 都映射到 TiDB Cloud 虚拟网络中端点的唯一端口。
4. 利用 Kafka 引导机制和 Azure 资源实现映射。

下图显示了该机制。

![连接到 Azure 自托管 Kafka Private Link 服务](/media/tidb-cloud/changefeed/connect-to-azure-self-hosted-kafka-privatelink-service.png)

本文档提供了连接到 Azure 中的 Kafka Private Link 服务的示例。虽然可以基于类似的端口映射原则进行其他配置，但本文档涵盖了 Kafka Private Link 服务的基本设置过程。对于生产环境，建议使用具有增强运维可维护性和可观察性的更具弹性的 Kafka Private Link 服务。

## 前提条件

1. 确保您有以下授权来在自己的 Azure 账户中设置 Kafka Private Link 服务。

    - 管理虚拟机
    - 管理虚拟网络
    - 管理负载均衡器
    - 管理私有链接服务
    - 连接到虚拟机以配置 Kafka 节点

2. 如果您还没有在 Azure 上的 [TiDB Cloud Dedicated 集群](/tidb-cloud/create-tidb-cluster.md)，请创建一个。

3. 从您的 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群获取 Kafka 部署信息。

    1. 在 [TiDB Cloud 控制台](https://tidbcloud.com)中，导航到[**集群**](https://tidbcloud.com/project/clusters)页面，然后点击目标集群的名称以进入其概览页面。
    2. 在左侧导航栏中，点击**数据** > **变更数据捕获**。
    3. 在**变更数据捕获**页面，点击右上角的**创建变更数据捕获**，然后提供以下信息：
        1. 在**目标**中，选择 **Kafka**。
        2. 在**连接方式**中，选择 **Private Link**。
    4. 记下**继续之前的提醒**中的区域信息和 TiDB Cloud Azure 账户的订阅信息。您将使用它来授权 TiDB Cloud 访问 Kafka Private Link 服务。
    5. 通过提供唯一的随机字符串为您的 Kafka Private Link 服务生成 **Kafka 广播监听器模式**。
        1. 输入唯一的随机字符串。它只能包含数字或小写字母。您稍后将使用它来生成 **Kafka 广播监听器模式**。
        2. 点击**检查使用情况并生成**以检查随机字符串是否唯一并生成 **Kafka 广播监听器模式**，该模式将用于组装 Kafka broker 的 EXTERNAL 广播监听器。

记下所有部署信息。您稍后需要使用它来配置 Kafka Private Link 服务。

下表显示了部署信息的示例。

| 信息     | 值    | 注释    |
|--------|-----------------|---------------------------|
| 区域 | 弗吉尼亚 (`eastus`) | 不适用 |
| TiDB Cloud Azure 账户的订阅 | `99549169-6cee-4263-8491-924a3011ee31` | 不适用 |
| Kafka 广播监听器模式 | 唯一随机字符串：`abc` | 生成的模式：`<broker_id>.abc.eastus.azure.3199745.tidbcloud.com:<port>` |

## 步骤 1. 设置 Kafka 集群

如果您需要部署新集群，请按照[部署新的 Kafka 集群](#部署新的-kafka-集群)中的说明进行操作。

如果您需要暴露现有集群，请按照[重新配置运行中的 Kafka 集群](#重新配置运行中的-kafka-集群)中的说明进行操作。

### 部署新的 Kafka 集群

#### 1. 设置 Kafka 虚拟网络

1. 登录 [Azure 门户](https://portal.azure.com/)，转到[虚拟网络](https://portal.azure.com/#browse/Microsoft.Network%2FvirtualNetworks)页面，然后点击**+ 创建**以创建虚拟网络。
2. 在**基本信息**选项卡中，选择您的**订阅**、**资源组**和**区域**，在**虚拟网络名称**字段中输入名称（例如 `kafka-pls-vnet`），然后点击**下一步**。
3. 在**安全性**选项卡中，启用 Azure Bastion，然后点击**下一步**。
4. 在 **IP 地址**选项卡中，执行以下操作：

    1. 设置虚拟网络的地址空间，例如 `10.0.0.0/16`。
    2. 点击**添加子网**为 broker 创建子网，填写以下信息，然后点击**添加**。
        - **名称**：`brokers-subnet`
        - **IP 地址范围**：`10.0.0.0/24`
        - **大小**：`/24（256 个地址）`

        默认情况下将创建一个 `AzureBastionSubnet`。

5. 点击**查看 + 创建**以验证信息。
6. 点击**创建**。

#### 2. 设置 Kafka broker

**2.1. 创建 broker 节点**

1. 登录 [Azure 门户](https://portal.azure.com/)，转到[虚拟机](https://portal.azure.com/#view/Microsoft_Azure_ComputeHub/ComputeHubMenuBlade/~/virtualMachinesBrowse)页面，点击**+ 创建**，然后选择 **Azure 虚拟机**。
2. 在**基本信息**选项卡中，选择您的**订阅**、**资源组**和**区域**，填写以下信息，然后点击**下一步：磁盘**。
    - **虚拟机名称**：`broker-node`
    - **可用性选项**：`可用性区域`
    - **区域选项**：`自选区域`
    - **可用性区域**：`区域 1`、`区域 2`、`区域 3`
    - **映像**：`Ubuntu Server 24.04 LTS - x64 Gen2`
    - **VM 架构**：`x64`
    - **大小**：`Standard_D2s_v3`
    - **身份验证类型**：`SSH 公钥`
    - **用户名**：`azureuser`
    - **SSH 公钥源**：`生成新的密钥对`
    - **密钥对名称**：`kafka_broker_key`
    - **公共入站端口**：`允许选定的端口`
    - **选择入站端口**：`SSH (22)`
3. 点击**下一步：网络**，然后在**网络**选项卡中填写以下信息：
    - **虚拟网络**：`kafka-pls-vnet`
    - **子网**：`brokers-subnet`
    - **公共 IP**：`无`
    - **NIC 网络安全组**：`基本`
    - **公共入站端口**：`允许选定的端口`
    - **选择入站端口**：`SSH (22)`
    - **负载均衡选项**：`无`
4. 点击**查看 + 创建**以验证信息。
5. 点击**创建**。将显示**生成新的密钥对**消息。
6. 点击**下载私钥并创建资源**将私钥下载到本地计算机。您可以看到虚拟机创建的进度。

**2.2. 准备 Kafka 运行时二进制文件**

虚拟机部署完成后，执行以下步骤：

1. 在 [Azure 门户](https://portal.azure.com/)中，转到[**资源组**](https://portal.azure.com/#view/HubsExtension/BrowseResourceGroups.ReactView)页面，点击您的资源组名称，然后导航到每个 broker 节点（`broker-node-1`、`broker-node-2` 和 `broker-node-3`）的页面。

2. 在每个 broker 节点的页面上，点击左侧导航栏中的**连接 > Bastion**，然后填写以下信息：

    - **身份验证类型**：`来自本地文件的 SSH 私钥`
    - **用户名**：`azureuser`
    - **本地文件**：选择之前下载的私钥文件
    - 选择**在新的浏览器标签页中打开**选项

3. 在每个 broker 节点的页面上，点击**连接**以打开带有 Linux 终端的新浏览器标签页。对于三个 broker 节点，您需要打开三个带有 Linux 终端的浏览器标签页。

4. 在每个 Linux 终端中，运行以下命令以在每个 broker 节点中下载二进制文件。

    ```shell
    # 下载 Kafka 和 OpenJDK，然后解压文件。您可以根据偏好选择二进制版本。
    wget https://archive.apache.org/dist/kafka/3.7.1/kafka_2.13-3.7.1.tgz
    tar -zxf kafka_2.13-3.7.1.tgz
    wget https://download.java.net/java/GA/jdk22.0.2/c9ecb94cd31b495da20a27d4581645e8/9/GPL/openjdk-22.0.2_linux-x64_bin.tar.gz
    tar -zxf openjdk-22.0.2_linux-x64_bin.tar.gz
    ```

**2.3. 在每个 broker 节点上设置 Kafka 节点**

1. 使用三个节点设置 KRaft Kafka 集群。每个节点同时作为 broker 和控制器。对于每个 broker 节点：

    1. 配置 `listeners`。所有三个 broker 都相同，并作为 broker 和控制器角色。
        1. 为所有**控制器**角色节点配置相同的 CONTROLLER 监听器。如果您只想添加 broker 角色节点，可以在 `server.properties` 中省略 CONTROLLER 监听器。
        2. 配置两个 broker 监听器：**INTERNAL** 用于内部 Kafka 客户端访问，**EXTERNAL** 用于从 TiDB Cloud 访问。

    2. 对于 `advertised.listeners`，执行以下操作：
        1. 为每个 broker 使用 broker 节点的内部 IP 地址配置 INTERNAL 广播监听器，这允许内部 Kafka 客户端通过广播地址连接到 broker。
        2. 根据从 TiDB Cloud 获取的 **Kafka 广播监听器模式**为每个 broker 节点配置 EXTERNAL 广播监听器，以帮助 TiDB Cloud 区分不同的 broker。不同的 EXTERNAL 广播监听器帮助 TiDB Cloud 端的 Kafka 客户端将请求路由到正确的 broker。
            - 使用不同的 `<port>` 值来区分 Kafka Private Link 服务访问中的 broker。为所有 broker 的 EXTERNAL 广播监听器规划端口范围。这些端口不必是 broker 实际监听的端口。它们是 Private Link 服务中负载均衡器监听的端口，将请求转发到不同的 broker。
            - 建议为不同的 broker 配置不同的 broker ID，以便于故障排除。

    3. 规划值：
        - CONTROLLER 端口：`29092`
        - INTERNAL 端口：`9092`
        - EXTERNAL 端口：`39092`
        - EXTERNAL 广播监听器端口范围：`9093~9095`

2. 使用 SSH 登录到每个 broker 节点。为每个 broker 节点分别创建配置文件 `~/config/server.properties`，内容如下：

    ```properties
    # broker-node-1 ~/config/server.properties
    # 1. 将 {broker-node-1-ip}、{broker-node-2-ip}、{broker-node-3-ip} 替换为实际的 IP 地址。
    # 2. 根据"前提条件"部分中的"Kafka 广播监听器模式"配置"advertised.listeners"中的 EXTERNAL。
    # 2.1 模式是 "<broker_id>.abc.eastus.azure.3199745.tidbcloud.com:<port>"。
    # 2.2 因此 EXTERNAL 可以是 "b1.abc.eastus.azure.3199745.tidbcloud.com:9093"。将 <broker_id> 替换为 "b" 前缀加上 "node.id" 属性，将 <port> 替换为 EXTERNAL 广播监听器端口范围内的唯一端口（9093）。
    process.roles=broker,controller
    node.id=1
    controller.quorum.voters=1@{broker-node-1-ip}:29092,2@{broker-node-2-ip}:29092,3@{broker-node-3-ip}:29092
    listeners=INTERNAL://0.0.0.0:9092,CONTROLLER://0.0.0.0:29092,EXTERNAL://0.0.0.0:39092
    inter.broker.listener.name=INTERNAL
    advertised.listeners=INTERNAL://{broker-node-1-ip}:9092,EXTERNAL://b1.abc.eastus.azure.3199745.tidbcloud.com:9093
    controller.listener.names=CONTROLLER
    listener.security.protocol.map=INTERNAL:PLAINTEXT,CONTROLLER:PLAINTEXT,EXTERNAL:PLAINTEXT,SSL:SSL,SASL_PLAINTEXT:SASL_PLAINTEXT,SASL_SSL:SASL_SSL
    log.dirs=./data
    ```

    ```properties
    # broker-node-2 ~/config/server.properties
    # 1. 将 {broker-node-1-ip}、{broker-node-2-ip}、{broker-node-3-ip} 替换为实际的 IP 地址。
    # 2. 根据"前提条件"部分中的"Kafka 广播监听器模式"配置"advertised.listeners"中的 EXTERNAL。
    # 2.1 模式是 "<broker_id>.abc.eastus.azure.3199745.tidbcloud.com:<port>"。
    # 2.2 因此 EXTERNAL 可以是 "b2.abc.eastus.azure.3199745.tidbcloud.com:9094"。将 <broker_id> 替换为 "b" 前缀加上 "node.id" 属性，将 <port> 替换为 EXTERNAL 广播监听器端口范围内的唯一端口（9094）。
    process.roles=broker,controller
    node.id=2
    controller.quorum.voters=1@{broker-node-1-ip}:29092,2@{broker-node-2-ip}:29092,3@{broker-node-3-ip}:29092
    listeners=INTERNAL://0.0.0.0:9092,CONTROLLER://0.0.0.0:29092,EXTERNAL://0.0.0.0:39092
    inter.broker.listener.name=INTERNAL
    advertised.listeners=INTERNAL://{broker-node-2-ip}:9092,EXTERNAL://b2.abc.eastus.azure.3199745.tidbcloud.com:9094
    controller.listener.names=CONTROLLER
    listener.security.protocol.map=INTERNAL:PLAINTEXT,CONTROLLER:PLAINTEXT,EXTERNAL:PLAINTEXT,SSL:SSL,SASL_PLAINTEXT:SASL_PLAINTEXT,SASL_SSL:SASL_SSL
    log.dirs=./data
    ```

    ```properties
    # broker-node-3 ~/config/server.properties
    # 1. 将 {broker-node-1-ip}、{broker-node-2-ip}、{broker-node-3-ip} 替换为实际的 IP 地址。
    # 2. 根据"前提条件"部分中的"Kafka 广播监听器模式"配置"advertised.listeners"中的 EXTERNAL。
    # 2.1 模式是 "<broker_id>.abc.eastus.azure.3199745.tidbcloud.com:<port>"。
    # 2.2 因此 EXTERNAL 可以是 "b3.abc.eastus.azure.3199745.tidbcloud.com:9095"。将 <broker_id> 替换为 "b" 前缀加上 "node.id" 属性，将 <port> 替换为 EXTERNAL 广播监听器端口范围内的唯一端口（9095）。
    process.roles=broker,controller
    node.id=3
    controller.quorum.voters=1@{broker-node-1-ip}:29092,2@{broker-node-2-ip}:29092,3@{broker-node-3-ip}:29092
    listeners=INTERNAL://0.0.0.0:9092,CONTROLLER://0.0.0.0:29092,EXTERNAL://0.0.0.0:39092
    inter.broker.listener.name=INTERNAL
    advertised.listeners=INTERNAL://{broker-node-3-ip}:9092,EXTERNAL://b3.abc.eastus.azure.3199745.tidbcloud.com:9095
    controller.listener.names=CONTROLLER
    listener.security.protocol.map=INTERNAL:PLAINTEXT,CONTROLLER:PLAINTEXT,EXTERNAL:PLAINTEXT,SSL:SSL,SASL_PLAINTEXT:SASL_PLAINTEXT,SASL_SSL:SASL_SSL
    log.dirs=./data
    ```

3. 创建脚本，然后在每个 broker 节点中执行它以启动 Kafka broker。

    ```shell
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    export JAVA_HOME="$SCRIPT_DIR/jdk-22.0.2"
    KAFKA_DIR="$SCRIPT_DIR/kafka_2.13-3.7.1/bin"
    KAFKA_STORAGE_CMD=$KAFKA_DIR/kafka-storage.sh
    KAFKA_START_CMD=$KAFKA_DIR/kafka-server-start.sh
    KAFKA_DATA_DIR=$SCRIPT_DIR/data
    KAFKA_LOG_DIR=$SCRIPT_DIR/log
    KAFKA_CONFIG_DIR=$SCRIPT_DIR/config

    KAFKA_PIDS=$(ps aux | grep 'kafka.Kafka' | grep -v grep | awk '{print $2}')
    if [ -z "$KAFKA_PIDS" ]; then
    echo "没有运行中的 Kafka 进程。"
    else
    echo "正在终止 PID 为 $KAFKA_PIDS 的 Kafka 进程"
    for PID in $KAFKA_PIDS; do
        kill -9 $PID
        echo "已终止 PID 为 $PID 的 Kafka 进程"
    done
    echo "所有 Kafka 进程已终止。"
    fi

    rm -rf $KAFKA_DATA_DIR
    mkdir -p $KAFKA_DATA_DIR
    rm -rf $KAFKA_LOG_DIR
    mkdir -p $KAFKA_LOG_DIR

    $KAFKA_STORAGE_CMD format -t "BRl69zcmTFmiPaoaANybiw" -c "$KAFKA_CONFIG_DIR/server.properties" > $KAFKA_LOG_DIR/server_format.log
    LOG_DIR=$KAFKA_LOG_DIR nohup $KAFKA_START_CMD "$KAFKA_CONFIG_DIR/server.properties" &
    ```
**2.4. 测试集群设置**

1. 测试 Kafka 引导。

    ```shell
    export JAVA_HOME=/home/azureuser/jdk-22.0.2

    # 从 INTERNAL 监听器引导
    ./kafka_2.13-3.7.1/bin/kafka-broker-api-versions.sh --bootstrap-server {one_of_broker_ip}:9092 | grep 9092
    # 预期输出（实际顺序可能不同）
    {broker-node-1-ip}:9092 (id: 1 rack: null) -> (
    {broker-node-2-ip}:9092 (id: 2 rack: null) -> (
    {broker-node-3-ip}:9092 (id: 3 rack: null) -> (

    # 从 EXTERNAL 监听器引导
    ./kafka_2.13-3.7.1/bin/kafka-broker-api-versions.sh --bootstrap-server {one_of_broker_ip}:39092
    # 最后 3 行的预期输出（实际顺序可能不同）
    # 与"从 INTERNAL 监听器引导"的输出不同之处在于，由于广播监听器无法在 kafka-pls-vnet 中解析，可能会出现异常或错误。
    # 当您创建通过 Private Link Service 连接到此 Kafka 集群的变更数据捕获时，TiDB Cloud 将使这些地址可解析并将请求路由到正确的 broker。
    b1.abc.eastus.azure.3199745.tidbcloud.com:9093 (id: 1 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
    b2.abc.eastus.azure.3199745.tidbcloud.com:9094 (id: 2 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
    b3.abc.eastus.azure.3199745.tidbcloud.com:9095 (id: 3 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
    ```

2. 在堡垒节点中创建生产者脚本 `produce.sh`。

    ```shell
    BROKER_LIST=$1

    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    export JAVA_HOME="$SCRIPT_DIR/jdk-22.0.2"
    KAFKA_DIR="$SCRIPT_DIR/kafka_2.13-3.7.1/bin"
    TOPIC="test-topic"

    create_topic() {
        echo "如果主题不存在则创建..."
        $KAFKA_DIR/kafka-topics.sh --create --topic $TOPIC --bootstrap-server $BROKER_LIST --if-not-exists --partitions 3 --replication-factor 3
    }

    produce_messages() {
        echo "向主题发送消息..."
        for ((chrono=1; chrono <= 10; chrono++)); do
            message="测试消息 "$chrono
            echo "创建 "$message
            echo $message | $KAFKA_DIR/kafka-console-producer.sh --broker-list $BROKER_LIST --topic $TOPIC
        done
    }
    create_topic
    produce_messages
    ```

3. 在堡垒节点中创建消费者脚本 `consume.sh`。

    ```shell
    BROKER_LIST=$1
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    export JAVA_HOME="$SCRIPT_DIR/jdk-22.0.2"
    KAFKA_DIR="$SCRIPT_DIR/kafka_2.13-3.7.1/bin"
    TOPIC="test-topic"
    CONSUMER_GROUP="test-group"
    consume_messages() {
        echo "从主题消费消息..."
        $KAFKA_DIR/kafka-console-consumer.sh --bootstrap-server $BROKER_LIST --topic $TOPIC --from-beginning --timeout-ms 5000 --consumer-property group.id=$CONSUMER_GROUP
    }
    consume_messages
    ```

4. 运行 `produce.sh` 和 `consume.sh` 脚本。这些脚本自动测试连接性和消息流，以验证 Kafka 集群是否正常运行。`produce.sh` 脚本使用 `--partitions 3 --replication-factor 3` 创建主题，发送测试消息，并使用 `--broker-list` 参数连接到所有三个 broker。`consume.sh` 脚本从主题读取消息以确认消息传递成功。

    ```shell
    # 测试写入消息。
    ./produce.sh {one_of_broker_ip}:9092
    ```

    ```shell
    # 预期输出
    如果主题不存在则创建...

    向主题发送消息...
    创建 测试消息 1
    >>创建 测试消息 2
    >>创建 测试消息 3
    >>创建 测试消息 4
    >>创建 测试消息 5
    >>创建 测试消息 6
    >>创建 测试消息 7
    >>创建 测试消息 8
    >>创建 测试消息 9
    >>创建 测试消息 10
    ```

    ```shell
    # 测试读取消息
    ./consume.sh {one_of_broker_ip}:9092
    ```

    ```shell
    # 预期示例输出（实际消息顺序可能不同）
    从主题消费消息...
    测试消息 3
    测试消息 4
    测试消息 5
    测试消息 9
    测试消息 10
    测试消息 6
    测试消息 8
    测试消息 1
    测试消息 2
    测试消息 7
    [2024-11-01 08:54:27,547] ERROR Error processing message, terminating consumer process:  (kafka.tools.ConsoleConsumer$)
    org.apache.kafka.common.errors.TimeoutException
    已处理共计 10 条消息
    ```
### 重新配置运行中的 Kafka 集群

确保您的 Kafka 集群部署在与 TiDB 集群相同的区域。

**1. 为 broker 配置 EXTERNAL 监听器**

以下配置适用于 Kafka KRaft 集群。ZK 模式配置类似。

1. 规划配置更改。

    1. 为每个 broker 配置一个用于从 TiDB Cloud 外部访问的 EXTERNAL **监听器**。选择一个唯一的端口作为 EXTERNAL 端口，例如 `39092`。
    2. 根据从 TiDB Cloud 获取的 **Kafka 广播监听器模式**为每个 broker 节点配置 EXTERNAL **广播监听器**，以帮助 TiDB Cloud 区分不同的 broker。不同的 EXTERNAL 广播监听器帮助 TiDB Cloud 端的 Kafka 客户端将请求路由到正确的 broker。
       - `<port>` 区分 Kafka Private Link 服务访问点的 broker。为所有 broker 的 EXTERNAL 广播监听器规划端口范围，例如 `从 9093 开始的范围`。这些端口不必是 broker 实际监听的端口。它们是 Private Link 服务的负载均衡器监听的端口，将请求转发到不同的 broker。
        - 建议为不同的 broker 配置不同的 broker ID，以便于故障排除。

2. 使用 SSH 登录到每个 broker 节点。使用以下内容修改每个 broker 的配置文件：

     ```properties
     # 添加 EXTERNAL 监听器
     listeners=INTERNAL:...,EXTERNAL://0.0.0.0:39092

     # 根据"前提条件"部分中的"Kafka 广播监听器模式"添加 EXTERNAL 广播监听器
     # 1. 模式是 "<broker_id>.abc.eastus.azure.3199745.tidbcloud.com:<port>"。
     # 2. 因此 EXTERNAL 可以是 "bx.abc.eastus.azure.3199745.tidbcloud.com:xxxx"。将 <broker_id> 替换为 "b" 前缀加上 "node.id" 属性，将 <port> 替换为 EXTERNAL 广播监听器端口范围内的唯一端口。
     # 例如
     advertised.listeners=...,EXTERNAL://b1.abc.eastus.azure.3199745.tidbcloud.com:9093

     # 配置 EXTERNAL 映射
    listener.security.protocol.map=...,EXTERNAL:PLAINTEXT
     ```

3. 重新配置所有 broker 后，逐个重启您的 Kafka broker。

**2. 在内部网络中测试 EXTERNAL 监听器设置**

您可以在 Kafka 客户端节点中下载 Kafka 和 OpenJDK。

```shell
# 下载 Kafka 和 OpenJDK，然后解压文件。您可以根据偏好选择二进制版本。
wget https://archive.apache.org/dist/kafka/3.7.1/kafka_2.13-3.7.1.tgz
tar -zxf kafka_2.13-3.7.1.tgz
wget https://download.java.net/java/GA/jdk22.0.2/c9ecb94cd31b495da20a27d4581645e8/9/GPL/openjdk-22.0.2_linux-x64_bin.tar.gz
tar -zxf openjdk-22.0.2_linux-x64_bin.tar.gz
```

执行以下脚本以测试引导是否按预期工作。

```shell
export JAVA_HOME=~/jdk-22.0.2

# 从 EXTERNAL 监听器引导
./kafka_2.13-3.7.1/bin/kafka-broker-api-versions.sh --bootstrap-server {one_of_broker_ip}:39092

# 最后 3 行的预期输出（实际顺序可能不同）
# 由于广播监听器无法在您的 Kafka 网络中解析，将会出现一些异常或错误。
# 当您创建通过 Private Link Service 连接到此 Kafka 集群的变更数据捕获时，TiDB Cloud 将使这些地址可解析并将请求路由到正确的 broker。
b1.abc.eastus.azure.3199745.tidbcloud.com:9093 (id: 1 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
b2.abc.eastus.azure.3199745.tidbcloud.com:9094 (id: 2 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
b3.abc.eastus.azure.3199745.tidbcloud.com:9095 (id: 3 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
```
## 步骤 2. 将 Kafka 集群暴露为 Private Link Service

### 1. 设置负载均衡器

1. 登录 [Azure 门户](https://portal.azure.com/)，转到[负载均衡](https://portal.azure.com/#view/Microsoft_Azure_Network/LoadBalancingHubMenuBlade/~/loadBalancers)页面，然后点击**+ 创建**以创建负载均衡器。
2. 在**基本信息**选项卡中，选择您的**订阅**、**资源组**和**区域**，填写以下实例信息，然后点击**下一步：前端 IP 配置 >**。

    - **名称**：`kafka-lb`
    - **SKU**：`标准`
    - **类型**：`内部`
    - **层级**：`区域`

3. 在**前端 IP 配置**选项卡中，点击**+ 添加前端 IP 配置**，填写以下信息，点击**保存**，然后点击**下一步：后端池 >**。

    - **名称**：`kafka-lb-ip`
    - **IP 版本**：`IPv4`
    - **虚拟网络**：`kafka-pls-vnet`
    - **子网**：`brokers-subnet`
    - **分配**：`动态`
    - **可用性区域**：`区域冗余`

4. 在**后端池**选项卡中，添加三个后端池如下，然后点击**下一步：入站规则**。

    - 名称：`pool1`；后端池配置：`NIC`；IP 配置：`broker-node-1`
    - 名称：`pool2`；后端池配置：`NIC`；IP 配置：`broker-node-2`
    - 名称：`pool3`；后端池配置：`NIC`；IP 配置：`broker-node-3`

5. 在**入站规则**选项卡中，添加三个负载均衡规则如下：

    1. 规则 1

        - **名称**：`rule1`
        - **IP 版本**：`IPv4`
        - **前端 IP 地址**：`kafka-lb-ip`
        - **后端池**：`pool1`
        - **协议**：`TCP`
        - **端口**：`9093`
        - **后端端口**：`39092`
        - **运行状况探测**：点击**创建新的**并填写探测信息。
            - **名称**：`kafka-lb-hp`
            - **协议**：`TCP`
            - **端口**：`39092`

    2. 规则 2

        - **名称**：`rule2`
        - **IP 版本**：`IPv4`
        - **前端 IP 地址**：`kafka-lb-ip`
        - **后端池**：`pool2`
        - **协议**：`TCP`
        - **端口**：`9094`
        - **后端端口**：`39092`
        - **运行状况探测**：点击**创建新的**并填写探测信息。
            - **名称**：`kafka-lb-hp`
            - **协议**：`TCP`
            - **端口**：`39092`

    3. 规则 3

        - **名称**：`rule3`
        - **IP 版本**：`IPv4`
        - **前端 IP 地址**：`kafka-lb-ip`
        - **后端池**：`pool3`
        - **协议**：`TCP`
        - **端口**：`9095`
        - **后端端口**：`39092`
        - **运行状况探测**：点击**创建新的**并填写探测信息。
            - **名称**：`kafka-lb-hp`
            - **协议**：`TCP`
            - **端口**：`39092`

6. 点击**下一步：出站规则**，点击**下一步：标记 >**，然后点击**下一步：查看 + 创建**以验证信息。

7. 点击**创建**。

### 2. 设置 Private Link Service

1. 登录 [Azure 门户](https://portal.azure.com/)，转到[私有链接服务](https://portal.azure.com/#view/Microsoft_Azure_Network/PrivateLinkCenterBlade/~/privatelinkservices)页面，然后点击**+ 创建**以为 Kafka 负载均衡器创建 Private Link Service。

2. 在**基本信息**选项卡中，选择您的**订阅**、**资源组**和**区域**，在**名称**字段中填写 `kafka-pls`，然后点击**下一步：出站设置 >**。

3. 在**出站设置**选项卡中，填写参数如下，然后点击**下一步：访问安全性 >**。

    - **负载均衡器**：`kafka-lb`
    - **负载均衡器前端 IP 地址**：`kafka-lb-ip`
    - **源 NAT 子网**：`kafka-pls-vnet/brokers-subnet`

4. 在**访问安全性**选项卡中，执行以下操作：

    - 对于**可见性**，选择**按订阅限制**或**具有您别名的任何人**。
    - 对于**订阅级别访问和自动批准**，点击**添加订阅**以添加您在[前提条件](#前提条件)中获取的 TiDB Cloud Azure 账户的订阅。

5. 点击**下一步：标记 >**，然后点击**下一步：查看 + 创建 >**以验证信息。

6. 点击**创建**。操作完成后，记下 Private Link Service 的别名，以供后续使用。
## 步骤 3. 从 TiDB Cloud 连接

1. 返回 [TiDB Cloud 控制台](https://tidbcloud.com)，通过**私有链接**为集群创建变更数据捕获以连接到 Kafka 集群。更多信息，请参阅[导出到 Apache Kafka](/tidb-cloud/changefeed-sink-to-apache-kafka.md)。

2. 当您进入**配置变更数据捕获目标 > 连接方式 > Private Link**时，使用相应的值填写以下字段和其他所需字段。

    - **Kafka 广播监听器模式**：您在[前提条件](#前提条件)中用于生成 **Kafka 广播监听器模式**的唯一随机字符串。
    - **Private Link Service 的别名**：您在[2. 设置 Private Link Service](#2-设置-private-link-service)中获取的 Private Link Service 的别名。
    - **引导端口**：`9093,9094,9095`。

3. 按照[导出到 Apache Kafka](/tidb-cloud/changefeed-sink-to-apache-kafka.md)中的步骤继续操作。

现在您已成功完成任务。

## 常见问题

### 如何从两个不同的 TiDB Cloud 项目连接到同一个 Kafka Private Link Service？

如果您已按照本文档成功设置了从第一个项目的连接，您可以按照以下步骤从第二个项目连接到同一个 Kafka Private Link Service：

1. 按照本文档从头开始操作。

2. 当您进入[步骤 1. 设置 Kafka 集群](#步骤-1-设置-kafka-集群)时，按照[重新配置运行中的 Kafka 集群](#重新配置运行中的-kafka-集群)创建另一组 EXTERNAL 监听器和广播监听器。您可以将其命名为 **EXTERNAL2**。注意，**EXTERNAL2** 的端口范围可以与 **EXTERNAL** 重叠。

3. 重新配置 broker 后，创建新的负载均衡器和新的 Private Link Service。

4. 使用以下信息配置 TiDB Cloud 连接：

    - 新的 Kafka 广播监听器组
    - 新的 Private Link Service
