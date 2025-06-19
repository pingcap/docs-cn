---
title: 在 Google Cloud 中设置自托管 Kafka Private Service Connect
summary: 本文介绍如何在 Google Cloud 中为自托管 Kafka 设置 Private Service Connect，以及如何使其与 TiDB Cloud 配合使用。
---

# 在 Google Cloud 中设置自托管 Kafka Private Service Connect

本文介绍如何在 Google Cloud 中为自托管 Kafka 设置 Private Service Connect，以及如何使其与 TiDB Cloud 配合使用。

工作机制如下：

1. TiDB Cloud VPC 通过私有端点连接到 Kafka VPC。
2. Kafka 客户端需要直接与所有 Kafka broker 通信。
3. 每个 Kafka broker 在 TiDB Cloud VPC 中映射到一个唯一的端口。
4. 利用 Kafka 引导机制和 Google Cloud 资源实现映射。

在 Google Cloud 中为自托管 Kafka 设置 Private Service Connect 有两种方式：

- 使用 Private Service Connect (PSC) 端口映射机制。此方法需要静态的端口-broker 映射配置。你需要重新配置现有的 Kafka 集群，添加一组 EXTERNAL 监听器和广播监听器。参见[通过 PSC 端口映射设置自托管 Kafka Private Service Connect 服务](#通过-psc-端口映射设置自托管-kafka-private-service-connect-服务)。

- 使用 [Kafka-proxy](https://github.com/grepplabs/kafka-proxy)。此方法在 Kafka 客户端和 Kafka broker 之间引入一个额外的运行进程作为代理。代理动态配置端口-broker 映射并转发请求。你无需重新配置现有的 Kafka 集群。参见[通过 Kafka-proxy 设置自托管 Kafka Private Service Connect](#通过-kafka-proxy-设置自托管-kafka-private-service-connect)。

本文提供了一个在 Google Cloud 中跨三个可用区（AZ）部署的 Kafka Private Service Connect 服务的连接示例。虽然可以基于类似的端口映射原理进行其他配置，但本文主要介绍 Kafka Private Service Connect 服务的基本设置过程。对于生产环境，建议使用具有增强运维可维护性和可观测性的更具弹性的 Kafka Private Service Connect 服务。

## 前提条件

1. 确保你有以下授权来在自己的 Google Cloud 账户中设置 Kafka Private Service Connect。

    - 管理虚拟机节点
    - 管理 VPC
    - 管理子网
    - 管理负载均衡器
    - 管理 Private Service Connect
    - 连接到虚拟机节点以配置 Kafka 节点

2. 如果你还没有 TiDB Cloud Dedicated 集群，请[创建一个](/tidb-cloud/create-tidb-cluster.md)。

3. 从 TiDB Cloud Dedicated 集群获取 Kafka 部署信息。

    1. 在 [TiDB Cloud 控制台](https://tidbcloud.com)中，导航到[**集群**](https://tidbcloud.com/project/clusters)页面，然后点击目标集群的名称以进入其概览页面。
    2. 在概览页面上，找到 TiDB 集群的区域。确保你的 Kafka 集群将部署在相同的区域。
    3. 在左侧导航栏中点击**数据** > **变更数据捕获**，在右上角点击**创建 Changefeed**，然后提供以下信息：
        1. 在**目标**中，选择 **Kafka**。
        2. 在**连接方式**中，选择 **Private Service Connect**。
    4. 记下**继续前的提醒**中的 Google Cloud 项目。你将使用它来授权来自 TiDB Cloud 的自动接受端点创建请求。
    5. 记下 **TiDB 集群的可用区**。你将在这些可用区中部署 TiDB 集群。建议你在这些可用区中部署 Kafka 以减少跨区流量。
    6. 为你的 Kafka Private Service Connect 服务选择一个唯一的 **Kafka 广播监听器模式**。
        1. 输入一个唯一的随机字符串。它只能包含数字或小写字母。你稍后将使用它来生成 **Kafka 广播监听器模式**。
        2. 点击**检查使用情况并生成**以检查随机字符串是否唯一，并生成 **Kafka 广播监听器模式**，该模式将用于组装 Kafka broker 的 EXTERNAL 广播监听器，或配置 Kafka-proxy。

记下所有部署信息。你稍后需要使用它来配置 Kafka Private Service Connect 服务。

下表显示了部署信息的示例。

| 信息                        | 值                           |
|------------------------------------|---------------------------------|
| 区域                             | Oregon (`us-west1`)               |
| TiDB Cloud 的 Google Cloud 项目 | `tidbcloud-prod-000`              |
| 可用区                              | <ul><li> `us-west1-a` </li><li> `us-west1-b` </li><li> `us-west1-c` </li></ul>   |
| Kafka 广播监听器模式  | 唯一随机字符串：`abc` <br/> 生成的模式：&lt;broker_id&gt;.abc.us-west1.gcp.3199745.tidbcloud.com:&lt;port&gt; |

## 通过 PSC 端口映射设置自托管 Kafka Private Service Connect 服务

通过使用 PSC 端口映射机制，将每个 Kafka broker 暴露给 TiDB Cloud VPC，并使用唯一的端口。下图展示了其工作原理。

![通过端口映射连接到 Google Cloud 自托管 Kafka Private Service Connect](/media/tidb-cloud/changefeed/connect-to-google-cloud-self-hosted-kafka-private-service-connect-by-portmapping.jpeg)

### 步骤 1. 设置 Kafka 集群

如果你需要部署新集群，请按照[部署新的 Kafka 集群](#部署新的-kafka-集群)中的说明进行操作。

如果你需要暴露现有集群，请按照[重新配置运行中的 Kafka 集群](#重新配置运行中的-kafka-集群)中的说明进行操作。
#### 部署新的 Kafka 集群

**1. 设置 Kafka VPC**

你需要为 Kafka VPC 创建两个子网，一个用于 Kafka broker，另一个用于堡垒节点，以便于配置 Kafka 集群。

转到 [Google Cloud 控制台](https://cloud.google.com/cloud-console)，导航到 [VPC 网络](https://console.cloud.google.com/networking/networks/list)页面，使用以下属性创建 Kafka VPC：

- **名称**：`kafka-vpc`
- 子网
    - **名称**：`bastion-subnet`；**区域**：`us-west1`；**IPv4 范围**：`10.0.0.0/18`
    - **名称**：`brokers-subnet`；**区域**：`us-west1`；**IPv4 范围**：`10.64.0.0/18`
- 防火墙规则
    - `kafka-vpc-allow-custom`
    - `kafka-vpc-allow-ssh`

**2. 配置虚拟机**

转到[虚拟机实例](https://console.cloud.google.com/compute/instances)页面配置虚拟机：

1. 堡垒节点

    - **名称**：`bastion-node`
    - **区域**：`us-west1`
    - **可用区**：`任意`
    - **机器类型**：`e2-medium`
    - **镜像**：`Debian GNU/Linux 12`
    - **网络**：`kafka-vpc`
    - **子网**：`bastion-subnet`
    - **外部 IPv4 地址**：`临时`

2. Broker 节点 1

    - **名称**：`broker-node1`
    - **区域**：`us-west1`
    - **可用区**：`us-west1-a`
    - **机器类型**：`e2-medium`
    - **镜像**：`Debian GNU/Linux 12`
    - **网络**：`kafka-vpc`
    - **子网**：`brokers-subnet`
    - **外部 IPv4 地址**：`无`

3. Broker 节点 2

    - **名称**：`broker-node2`
    - **区域**：`us-west1`
    - **可用区**：`us-west1-b`
    - **机器类型**：`e2-medium`
    - **镜像**：`Debian GNU/Linux 12`
    - **网络**：`kafka-vpc`
    - **子网**：`brokers-subnet`
    - **外部 IPv4 地址**：`无`

4. Broker 节点 3

    - **名称**：`broker-node3`
    - **区域**：`us-west1`
    - **可用区**：`us-west1-c`
    - **机器类型**：`e2-medium`
    - **镜像**：`Debian GNU/Linux 12`
    - **网络**：`kafka-vpc`
    - **子网**：`brokers-subnet`
    - **外部 IPv4 地址**：`无`

**3. 准备 Kafka 运行时二进制文件**

1. 转到堡垒节点的详情页面。点击 **SSH** 登录到堡垒节点。下载二进制文件。

    ```shell
    # 下载 Kafka 和 OpenJDK，然后解压文件。你可以根据自己的偏好选择二进制版本。
    wget https://archive.apache.org/dist/kafka/3.7.1/kafka_2.13-3.7.1.tgz
    tar -zxf kafka_2.13-3.7.1.tgz
    wget https://download.java.net/java/GA/jdk22.0.2/c9ecb94cd31b495da20a27d4581645e8/9/GPL/openjdk-22.0.2_linux-x64_bin.tar.gz
    tar -zxf openjdk-22.0.2_linux-x64_bin.tar.gz
    ```

2. 将二进制文件复制到每个 broker 节点。

    ```shell
    # 运行此命令以使用 Google 用户凭据授权 gcloud 访问 Cloud Platform
    # 按照输出中的说明完成登录
    gcloud auth login

    # 将二进制文件复制到 broker 节点
    gcloud compute scp kafka_2.13-3.7.1.tgz openjdk-22.0.2_linux-x64_bin.tar.gz broker-node1:~ --zone=us-west1-a
    gcloud compute ssh broker-node1 --zone=us-west1-a --command="tar -zxf kafka_2.13-3.7.1.tgz && tar -zxf openjdk-22.0.2_linux-x64_bin.tar.gz"
    gcloud compute scp kafka_2.13-3.7.1.tgz openjdk-22.0.2_linux-x64_bin.tar.gz broker-node2:~ --zone=us-west1-b
    gcloud compute ssh broker-node2 --zone=us-west1-b --command="tar -zxf kafka_2.13-3.7.1.tgz && tar -zxf openjdk-22.0.2_linux-x64_bin.tar.gz"
    gcloud compute scp kafka_2.13-3.7.1.tgz openjdk-22.0.2_linux-x64_bin.tar.gz broker-node3:~ --zone=us-west1-c
    gcloud compute ssh broker-node3 --zone=us-west1-c --command="tar -zxf kafka_2.13-3.7.1.tgz && tar -zxf openjdk-22.0.2_linux-x64_bin.tar.gz"
    ```

**4. 配置 Kafka broker**

1. 设置一个包含三个节点的 KRaft Kafka 集群。每个节点同时作为 broker 和 controller 角色。对于每个 broker：

    1. 对于 `listeners`，所有三个 broker 都相同，并作为 broker 和 controller 角色：
        1. 为所有 **controller** 角色节点配置相同的 CONTROLLER 监听器。如果你只想添加 **broker** 角色节点，则不需要在 `server.properties` 中配置 CONTROLLER 监听器。
        2. 配置两个 **broker** 监听器。INTERNAL 用于内部访问；EXTERNAL 用于来自 TiDB Cloud 的外部访问。
    
    2. 对于 `advertised.listeners`，执行以下操作：
        1. 为每个 broker 配置一个使用 broker 节点内部 IP 地址的 INTERNAL 广播监听器，这允许内部 Kafka 客户端通过广播地址连接到 broker。
        2. 基于你从 TiDB Cloud 获取的 **Kafka 广播监听器模式**，为每个 broker 节点配置一个 EXTERNAL 广播监听器，以帮助 TiDB Cloud 区分不同的 broker。不同的 EXTERNAL 广播监听器帮助 TiDB Cloud 端的 Kafka 客户端将请求路由到正确的 broker。
            - `<port>` 用于区分 Kafka Private Service Connect 访问点的 broker。为所有 broker 的 EXTERNAL 广播监听器规划一个端口范围。这些端口不必是 broker 实际监听的端口。它们是 Private Service Connect 的负载均衡器监听的端口，负载均衡器会将请求转发到不同的 broker。
            - 建议为不同的 broker 配置不同的 broker ID，以便于故障排除。
    
    3. 规划的值：
        - CONTROLLER 端口：`29092`
        - INTERNAL 端口：`9092`
        - EXTERNAL：`39092`
        - EXTERNAL 广播监听器端口范围：`9093~9095`

2. 使用 SSH 登录到每个 broker 节点。为每个 broker 节点分别创建配置文件 `~/config/server.properties`，内容如下：

    ```properties
    # broker-node1 ~/config/server.properties
    # 1. 将 {broker-node1-ip}、{broker-node2-ip}、{broker-node3-ip} 替换为实际的 IP 地址。
    # 2. 根据"前提条件"部分中的"Kafka 广播监听器模式"配置 "advertised.listeners" 中的 EXTERNAL。
    # 2.1 模式为 "<broker_id>.abc.us-west1.gcp.3199745.tidbcloud.com:<port>"。
    # 2.2 因此 EXTERNAL 可以是 "b1.abc.us-west1.gcp.3199745.tidbcloud.com:9093"。将 <broker_id> 替换为 "b" 前缀加上 "node.id" 属性，将 <port> 替换为 EXTERNAL 广播监听器端口范围内的唯一端口（9093）。
    process.roles=broker,controller
    node.id=1
    controller.quorum.voters=1@{broker-node1-ip}:29092,2@{broker-node2-ip}:29092,3@{broker-node3-ip}:29092
    listeners=INTERNAL://0.0.0.0:9092,CONTROLLER://0.0.0.0:29092,EXTERNAL://0.0.0.0:39092
    inter.broker.listener.name=INTERNAL
    advertised.listeners=INTERNAL://{broker-node1-ip}:9092,EXTERNAL://b1.abc.us-west1.gcp.3199745.tidbcloud.com:9093
    controller.listener.names=CONTROLLER
    listener.security.protocol.map=INTERNAL:PLAINTEXT,CONTROLLER:PLAINTEXT,EXTERNAL:PLAINTEXT,SSL:SSL,SASL_PLAINTEXT:SASL_PLAINTEXT,SASL_SSL:SASL_SSL
    log.dirs=./data
    ```

    ```properties
    # broker-node2 ~/config/server.properties
    # 1. 将 {broker-node1-ip}、{broker-node2-ip}、{broker-node3-ip} 替换为实际的 IP 地址。
    # 2. 根据"前提条件"部分中的"Kafka 广播监听器模式"配置 "advertised.listeners" 中的 EXTERNAL。
    # 2.1 模式为 "<broker_id>.abc.us-west1.gcp.3199745.tidbcloud.com:<port>"。
    # 2.2 因此 EXTERNAL 可以是 "b2.abc.us-west1.gcp.3199745.tidbcloud.com:9094"。将 <broker_id> 替换为 "b" 前缀加上 "node.id" 属性，将 <port> 替换为 EXTERNAL 广播监听器端口范围内的唯一端口（9094）。
    process.roles=broker,controller
    node.id=2
    controller.quorum.voters=1@{broker-node1-ip}:29092,2@{broker-node2-ip}:29092,3@{broker-node3-ip}:29092
    listeners=INTERNAL://0.0.0.0:9092,CONTROLLER://0.0.0.0:29092,EXTERNAL://0.0.0.0:39092
    inter.broker.listener.name=INTERNAL
    advertised.listeners=INTERNAL://{broker-node2-ip}:9092,EXTERNAL://b2.abc.us-west1.gcp.3199745.tidbcloud.com:9094
    controller.listener.names=CONTROLLER
    listener.security.protocol.map=INTERNAL:PLAINTEXT,CONTROLLER:PLAINTEXT,EXTERNAL:PLAINTEXT,SSL:SSL,SASL_PLAINTEXT:SASL_PLAINTEXT,SASL_SSL:SASL_SSL
    log.dirs=./data
    ```

    ```properties
    # broker-node3 ~/config/server.properties
    # 1. 将 {broker-node1-ip}、{broker-node2-ip}、{broker-node3-ip} 替换为实际的 IP 地址。
    # 2. 根据"前提条件"部分中的"Kafka 广播监听器模式"配置 "advertised.listeners" 中的 EXTERNAL。
    # 2.1 模式为 "<broker_id>.abc.us-west1.gcp.3199745.tidbcloud.com:<port>"。
    # 2.2 因此 EXTERNAL 可以是 "b3.abc.us-west1.gcp.3199745.tidbcloud.com:9095"。将 <broker_id> 替换为 "b" 前缀加上 "node.id" 属性，将 <port> 替换为 EXTERNAL 广播监听器端口范围内的唯一端口（9095）。
    process.roles=broker,controller
    node.id=3
    controller.quorum.voters=1@{broker-node1-ip}:29092,2@{broker-node2-ip}:29092,3@{broker-node3-ip}:29092
    listeners=INTERNAL://0.0.0.0:9092,CONTROLLER://0.0.0.0:29092,EXTERNAL://0.0.0.0:39092
    inter.broker.listener.name=INTERNAL
    advertised.listeners=INTERNAL://{broker-node3-ip}:9092,EXTERNAL://b3.abc.us-west1.gcp.3199745.tidbcloud.com:9095
    controller.listener.names=CONTROLLER
    listener.security.protocol.map=INTERNAL:PLAINTEXT,CONTROLLER:PLAINTEXT,EXTERNAL:PLAINTEXT,SSL:SSL,SASL_PLAINTEXT:SASL_PLAINTEXT,SASL_SSL:SASL_SSL
    log.dirs=./data
    ```
3. 创建脚本，然后在每个 broker 节点中执行该脚本以启动 Kafka broker。

    ```shell
    #!/bin/bash

    # 获取当前脚本的目录
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    # 将 JAVA_HOME 设置为脚本目录中的 Java 安装路径
    export JAVA_HOME="$SCRIPT_DIR/jdk-22.0.2"
    # 定义变量
    KAFKA_DIR="$SCRIPT_DIR/kafka_2.13-3.7.1/bin"
    KAFKA_STORAGE_CMD=$KAFKA_DIR/kafka-storage.sh
    KAFKA_START_CMD=$KAFKA_DIR/kafka-server-start.sh
    KAFKA_DATA_DIR=$SCRIPT_DIR/data
    KAFKA_LOG_DIR=$SCRIPT_DIR/log
    KAFKA_CONFIG_DIR=$SCRIPT_DIR/config

    # 清理步骤，便于多次实验
    # 查找所有 Kafka 进程 ID
    KAFKA_PIDS=$(ps aux | grep 'kafka.Kafka' | grep -v grep | awk '{print $2}')
    if [ -z "$KAFKA_PIDS" ]; then
    echo "没有运行中的 Kafka 进程。"
    else
    # 终止每个 Kafka 进程
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

    # Magic id: BRl69zcmTFmiPaoaANybiw。你可以使用自己的 magic ID。
    $KAFKA_STORAGE_CMD format -t "BRl69zcmTFmiPaoaANybiw" -c "$KAFKA_CONFIG_DIR/server.properties" > $KAFKA_LOG_DIR/server_format.log   
    LOG_DIR=$KAFKA_LOG_DIR nohup $KAFKA_START_CMD "$KAFKA_CONFIG_DIR/server.properties" &
    ```

**5. 在堡垒节点中测试 Kafka 集群**

1. 测试 Kafka 引导。

    ```shell
    export JAVA_HOME=~/jdk-22.0.2

    # 从 INTERNAL 监听器引导
    ./kafka_2.13-3.7.1/bin/kafka-broker-api-versions.sh --bootstrap-server {one_of_broker_ip}:9092 | grep 9092
    # 预期输出（实际顺序可能不同）
    {broker-node1-ip}:9092 (id: 1 rack: null) -> (
    {broker-node2-ip}:9092 (id: 2 rack: null) -> (
    {broker-node3-ip}:9092 (id: 3 rack: null) -> (

    # 从 EXTERNAL 监听器引导
    ./kafka_2.13-3.7.1/bin/kafka-broker-api-versions.sh --bootstrap-server {one_of_broker_ip}:39092
    # 最后 3 行的预期输出（实际顺序可能不同）
    # 与"从 INTERNAL 监听器引导"的输出不同之处在于，可能会出现异常或错误，因为广播监听器在 Kafka VPC 中无法解析。
    # 当你通过 Private Service Connect 创建 changefeed 连接到此 Kafka 集群时，我们将在 TiDB Cloud 端使其可解析并将其路由到正确的 broker。
    b1.abc.us-west1.gcp.3199745.tidbcloud.com:9093 (id: 1 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
    b2.abc.us-west1.gcp.3199745.tidbcloud.com:9094 (id: 2 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
    b3.abc.us-west1.gcp.3199745.tidbcloud.com:9095 (id: 3 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
    ```

2. 在堡垒节点中创建生产者脚本 `produce.sh`。

    ```shell
    #!/bin/bash
    BROKER_LIST=$1 # "{broker_address1},{broker_address2}..."

    # 获取当前脚本的目录
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    # 将 JAVA_HOME 设置为脚本目录中的 Java 安装路径
    export JAVA_HOME="$SCRIPT_DIR/jdk-22.0.2"
    # 定义 Kafka 目录
    KAFKA_DIR="$SCRIPT_DIR/kafka_2.13-3.7.1/bin"
    TOPIC="test-topic"

    # 如果主题不存在则创建
    create_topic() {
        echo "如果主题不存在则创建..."
        $KAFKA_DIR/kafka-topics.sh --create --topic $TOPIC --bootstrap-server $BROKER_LIST --if-not-exists --partitions 3 --replication-factor 3
    }

    # 向主题发送消息
    produce_messages() {
        echo "正在向主题发送消息..."
        for ((chrono=1; chrono <= 10; chrono++)); do
            message="Test message "$chrono
            echo "创建 "$message
            echo $message | $KAFKA_DIR/kafka-console-producer.sh --broker-list $BROKER_LIST --topic $TOPIC
        done
    }
    create_topic
    produce_messages 
    ```

3. 在堡垒节点中创建消费者脚本 `consume.sh`。

    ```shell
    #!/bin/bash

    BROKER_LIST=$1 # "{broker_address1},{broker_address2}..."

    # 获取当前脚本的目录
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    # 将 JAVA_HOME 设置为脚本目录中的 Java 安装路径
    export JAVA_HOME="$SCRIPT_DIR/jdk-22.0.2"
    # 定义 Kafka 目录
    KAFKA_DIR="$SCRIPT_DIR/kafka_2.13-3.7.1/bin"
    TOPIC="test-topic"
    CONSUMER_GROUP="test-group"
    # 从主题消费消息
    consume_messages() {
        echo "正在从主题消费消息..."
        $KAFKA_DIR/kafka-console-consumer.sh --bootstrap-server $BROKER_LIST --topic $TOPIC --from-beginning --timeout-ms 5000 --consumer-property group.id=$CONSUMER_GROUP
    }
    consume_messages
    ```

4. 执行 `produce.sh` 和 `consume.sh` 以验证 Kafka 集群是否正在运行。这些脚本稍后也将用于网络连接测试。该脚本将创建一个具有 `--partitions 3 --replication-factor 3` 的主题。确保所有三个 broker 都包含数据。确保脚本将连接到所有三个 broker，以保证网络连接将被测试。

    ```shell
    # 测试写入消息
    ./produce.sh {one_of_broker_ip}:9092
    ```

    ```text
    # 预期输出
    如果主题不存在则创建...

    正在向主题发送消息...
    创建 Test message 1
    >>创建 Test message 2
    >>创建 Test message 3
    >>创建 Test message 4
    >>创建 Test message 5
    >>创建 Test message 6
    >>创建 Test message 7
    >>创建 Test message 8
    >>创建 Test message 9
    >>创建 Test message 10
    ```

    ```shell
    # 测试读取消息
    ./consume.sh {one_of_broker_ip}:9092
    ```

    ```text
    # 预期示例输出（实际消息顺序可能不同）
    正在从主题消费消息...
    Test message 3
    Test message 4
    Test message 5
    Test message 9
    Test message 10
    Test message 6
    Test message 8
    Test message 1
    Test message 2
    Test message 7
    [2024-11-01 08:54:27,547] ERROR Error processing message, terminating consumer process:  (kafka.tools.ConsoleConsumer$)
    org.apache.kafka.common.errors.TimeoutException
    共处理了 10 条消息
    ```
#### 重新配置运行中的 Kafka 集群

确保你的 Kafka 集群部署在与 TiDB 集群相同的区域。建议可用区也在相同的区域，以减少跨区流量。

**1. 为 broker 配置 EXTERNAL 监听器**

以下配置适用于 Kafka KRaft 集群。ZK 模式配置类似。

1. 规划配置更改。

    1. 为每个 broker 配置一个用于来自 TiDB Cloud 的外部访问的 EXTERNAL **监听器**。选择一个唯一的端口作为 EXTERNAL 端口，例如 `39092`。
    2. 基于你从 TiDB Cloud 获取的 **Kafka 广播监听器模式**，为每个 broker 节点配置一个 EXTERNAL **广播监听器**，以帮助 TiDB Cloud 区分不同的 broker。不同的 EXTERNAL 广播监听器帮助 TiDB Cloud 端的 Kafka 客户端将请求路由到正确的 broker。
       - `<port>` 用于区分 Kafka Private Service Connect 访问点的 broker。为所有 broker 的 EXTERNAL 广播监听器规划一个端口范围，例如 `从 9093 开始的范围`。这些端口不必是 broker 实际监听的端口。它们是 Private Service Connect 的负载均衡器监听的端口，负载均衡器会将请求转发到不同的 broker。
        - 建议为不同的 broker 配置不同的 broker ID，以便于故障排除。

2. 使用 SSH 登录到每个 broker 节点。使用以下内容修改每个 broker 的配置文件：

     ```properties
     # 添加 EXTERNAL 监听器
     listeners=INTERNAL:...,EXTERNAL://0.0.0.0:39092

     # 根据"前提条件"部分中的"Kafka 广播监听器模式"添加 EXTERNAL 广播监听器
     # 1. 模式为 "<broker_id>.abc.us-west1.gcp.3199745.tidbcloud.com:<port>"。
     # 2. 因此 EXTERNAL 可以是 "bx.abc.us-west1.gcp.3199745.tidbcloud.com:xxxx"。将 <broker_id> 替换为 "b" 前缀加上 "node.id" 属性，将 <port> 替换为 EXTERNAL 广播监听器端口范围内的唯一端口。
     # 例如
     advertised.listeners=...,EXTERNAL://b1.abc.us-west1.gcp.3199745.tidbcloud.com:9093

     # 配置 EXTERNAL 映射
    listener.security.protocol.map=...,EXTERNAL:PLAINTEXT
     ```

3. 重新配置所有 broker 后，逐个重启你的 Kafka broker。

**2. 在你的内部网络中测试 EXTERNAL 监听器设置**

你可以在 Kafka 客户端节点中下载 Kafka 和 OpenJDK。

```shell
# 下载 Kafka 和 OpenJDK，然后解压文件。你可以根据自己的偏好选择二进制版本。
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
# 会出现一些异常或错误，因为广播监听器在你的 Kafka 网络中无法解析。
# 当你通过 Private Service Connect 创建 changefeed 连接到此 Kafka 集群时，我们将在 TiDB Cloud 端使其可解析并将其路由到正确的 broker。
b1.abc.us-west1.gcp.3199745.tidbcloud.com:9093 (id: 1 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
b2.abc.us-west1.gcp.3199745.tidbcloud.com:9094 (id: 2 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
b3.abc.us-west1.gcp.3199745.tidbcloud.com:9095 (id: 3 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
```
### 步骤 2. 将 Kafka 集群暴露为 Private Service Connect

1. 转到[网络端点组](https://console.cloud.google.com/compute/networkendpointgroups/list)页面。创建一个网络端点组，如下所示：

    - **名称**：`kafka-neg`
    - **网络端点组类型**：`端口映射 NEG（区域性）`
        - **区域**：`us-west1`
        - **网络**：`kafka-vpc`
        - **子网**：`brokers-subnet`

2. 转到网络端点组的详情页面，添加网络端点以配置到 broker 节点的端口映射。

    1. 网络端点 1
        - **实例**：`broker-node1`
        - **VM 端口**：`39092`
        - **客户端端口**：`9093`
    2. 网络端点 2
        - **实例**：`broker-node2`
        - **VM 端口**：`39092`
        - **客户端端口**：`9094`
    3. 网络端点 3
        - **实例**：`broker-node3`
        - **VM 端口**：`39092`
        - **客户端端口**：`9095`

3. 转到[负载均衡](https://console.cloud.google.com/net-services/loadbalancing/list/loadBalancers)页面。创建一个负载均衡器，如下所示：

    - **负载均衡器类型**：`网络负载均衡器`
    - **代理或直通**：`直通`
    - **面向公网或内部**：`内部`
    - **负载均衡器名称**：`kafka-lb`
    - **区域**：`us-west1`
    - **网络**：`kafka-vpc`
    - 后端配置
        - **后端类型**：`端口映射网络端点组`
        - **协议**：`TCP`
        - **端口映射网络端点组**：`kafka-neg`
    - 前端配置
        - **子网**：`brokers-subnet`
        - **端口**：`全部`

4. 转到[**Private Service Connect** > **发布服务**](https://console.cloud.google.com/net-services/psc/list/producers)。

    - **负载均衡器类型**：`内部直通网络负载均衡器`
    - **内部负载均衡器**：`kafka-lb`
    - **服务名称**：`kafka-psc`
    - **子网**：`保留新子网`
        - **名称**：`psc-subnet`
        - **VPC 网络**：`kafka-vpc`
        - **区域**：`us-west1`
        - **IPv4 范围**：`10.128.0.0/18`
    - **接受的项目**：你在[前提条件](#前提条件)中获得的 TiDB Cloud 的 Google Cloud 项目，例如 `tidbcloud-prod-000`。

5. 导航到 `kafka-psc` 的详情页面。记下**服务附件**，例如 `projects/tidbcloud-dp-stg-000/regions/us-west1/serviceAttachments/kafka-psc`。你将在 TiDB Cloud 中使用它来连接到此 PSC。

6. 转到 VPC 网络 `kafka-vpc` 的详情页面。添加防火墙规则以允许 PSC 流量到达所有 broker。

    - **名称**：`allow-psc-traffic`
    - **流量方向**：`入站`
    - **匹配时的操作**：`允许`
    - **目标**：`网络中的所有实例`
    - **源过滤器**：`IPv4 范围`
    - **源 IPv4 范围**：`10.128.0.0/18`。psc-subnet 的范围。
    - **协议和端口**：允许所有

### 步骤 3. 从 TiDB Cloud 连接

1. 返回 [TiDB Cloud 控制台](https://tidbcloud.com)，为集群创建一个通过 **Private Service Connect** 连接到 Kafka 集群的 changefeed。更多信息，请参阅[同步数据到 Apache Kafka](/tidb-cloud/changefeed-sink-to-apache-kafka.md)。

2. 当你进入**配置 changefeed 目标** > **连接方式** > **Private Service Connect** 时，使用相应的值填写以下字段和其他所需字段。

    - **Kafka 广播监听器模式**：`abc`。与你在[前提条件](#前提条件)中用于生成 **Kafka 广播监听器模式** 的唯一随机字符串相同。
    - **服务附件**：PSC 的 Kafka 服务附件，例如 `projects/tidbcloud-dp-stg-000/regions/us-west1/serviceAttachments/kafka-psc`。
    - **引导端口**：`9092,9093,9094`

3. 按照[同步数据到 Apache Kafka](/tidb-cloud/changefeed-sink-to-apache-kafka.md)中的步骤继续操作。
## 通过 Kafka-proxy 设置自托管 Kafka Private Service Connect

通过使用 Kafka-proxy 动态端口映射机制，将每个 Kafka broker 暴露给 TiDB Cloud VPC，并使用唯一的端口。下图展示了其工作原理。

![通过 Kafka 代理连接到 Google Cloud 自托管 Kafka Private Service Connect](/media/tidb-cloud/changefeed/connect-to-google-cloud-self-hosted-kafka-private-service-connect-by-kafka-proxy.jpeg)

### 步骤 1. 设置 Kafka-proxy

假设你已经在与 TiDB 集群相同的区域有一个正在运行的 Kafka 集群。你可以从你的 VPC 网络连接到 Kafka 集群。Kafka 集群可以是自托管的，也可以是由第三方提供商（如 Confluent）提供的。

1. 转到[实例组](https://console.cloud.google.com/compute/instanceGroups/list)页面，为 Kafka-proxy 创建一个实例组。

    - **名称**：`kafka-proxy-ig`
    - 实例模板：
        - **名称**：`kafka-proxy-tpl`
        - **位置**：`区域`
        - **区域**：`us-west1`
        - **机器类型**：`e2-medium`。你可以根据工作负载选择自己的机器类型。
        - **网络**：你的可以连接到 Kafka 集群的 VPC 网络。
        - **子网**：你的可以连接到 Kafka 集群的子网。
        - **外部 IPv4 地址**：`临时`。启用互联网访问以便于配置 Kafka-proxy。在生产环境中，你可以选择**无**，并以你自己的方式登录节点。
    - **位置**：`单一区域`
    - **区域**：`us-west1`
    - **可用区**：选择你的 broker 所在的可用区之一。
    - **自动扩缩模式**：`关闭`
    - **最小实例数**：`1`
    - **最大实例数**：`1`。Kafka-proxy 不支持集群模式，因此只能部署一个实例。每个 Kafka-proxy 随机将本地端口映射到 broker 的端口，导致不同代理之间的映射不同。在负载均衡器后部署多个 Kafka-proxy 可能会导致问题。如果 Kafka 客户端连接到一个代理，然后通过另一个代理访问 broker，请求可能会路由到错误的 broker。

2. 转到 kafka-proxy-ig 中节点的详情页面。点击 **SSH** 登录到节点。下载二进制文件：

    ```shell
    # 你可以选择其他版本
    wget https://github.com/grepplabs/kafka-proxy/releases/download/v0.3.11/kafka-proxy-v0.3.11-linux-amd64.tar.gz
    tar -zxf kafka-proxy-v0.3.11-linux-amd64.tar.gz
    ```

3. 运行 Kafka-proxy 并连接到 Kafka broker。

    ```shell
    # 需要向 Kafka-proxy 提供三种参数
    # 1. --bootstrap-server-mapping 定义引导映射。建议配置三个映射，每个可用区一个，以提高弹性。
    #   a) Kafka broker 地址；
    #   b) Kafka-proxy 中 broker 的本地地址；
    #   c) 如果 Kafka 客户端从 Kafka-proxy 引导，则为 broker 的广播监听器
    # 2. --dynamic-sequential-min-port 定义其他 broker 的随机映射的起始端口
    # 3. --dynamic-advertised-listener 根据从"前提条件"部分获得的模式定义其他 broker 的广播监听器地址
    #   a) 模式：<broker_id>.abc.us-west1.gcp.3199745.tidbcloud.com:<port>
    #   b) 确保将 <broker_id> 替换为固定的小写字符串，例如 "brokers"。你可以使用自己的字符串。此步骤将帮助 TiDB Cloud 正确路由请求。
    #   c) 删除 ":<port>"
    #   d) 广播监听器地址将是：brokers.abc.us-west1.gcp.3199745.tidbcloud.com
    ./kafka-proxy server \
            --bootstrap-server-mapping "{address_of_broker1},0.0.0.0:9092,b1.abc.us-west1.gcp.3199745.tidbcloud.com:9092" \
            --bootstrap-server-mapping "{address_of_broker2},0.0.0.0:9093,b2.abc.us-west1.gcp.3199745.tidbcloud.com:9093" \
            --bootstrap-server-mapping "{address_of_broker3},0.0.0.0:9094,b3.abc.us-west1.gcp.3199745.tidbcloud.com:9094" \
            --dynamic-sequential-min-port=9095 \
            --dynamic-advertised-listener=brokers.abc.us-west1.gcp.3199745.tidbcloud.com > ./kafka_proxy.log 2>&1 &
    ```

4. 在 Kafka-proxy 节点中测试引导。

    ```shell
    # 下载 Kafka 和 OpenJDK，然后解压文件。你可以根据自己的偏好选择二进制版本。
    wget https://archive.apache.org/dist/kafka/3.7.1/kafka_2.13-3.7.1.tgz
    tar -zxf kafka_2.13-3.7.1.tgz
    wget https://download.java.net/java/GA/jdk22.0.2/c9ecb94cd31b495da20a27d4581645e8/9/GPL/openjdk-22.0.2_linux-x64_bin.tar.gz
    tar -zxf openjdk-22.0.2_linux-x64_bin.tar.gz

    export JAVA_HOME=~/jdk-22.0.2

    ./kafka_2.13-3.7.1/bin/kafka-broker-api-versions.sh --bootstrap-server 0.0.0.0:9092
    # 最后几行的预期输出（实际顺序可能不同）
    # 可能会出现异常或错误，因为广播监听器在你的网络中无法解析。
    # 当你通过 Private Service Connect 创建 changefeed 连接到此 Kafka 集群时，我们将在 TiDB Cloud 端使其可解析并将其路由到正确的 broker。
    b1.abc.us-west1.gcp.3199745.tidbcloud.com:9092 (id: 1 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
    b2.abc.us-west1.gcp.3199745.tidbcloud.com:9093 (id: 2 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
    b3.abc.us-west1.gcp.3199745.tidbcloud.com:9094 (id: 3 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
    brokers.abc.us-west1.gcp.3199745.tidbcloud.com:9095 (id: 4 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
    brokers.abc.us-west1.gcp.3199745.tidbcloud.com:9096 (id: 5 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
    ...
    ```
### 步骤 2. 将 Kafka-proxy 暴露为 Private Service Connect 服务

1. 转到[负载均衡](https://console.cloud.google.com/net-services/loadbalancing/list/loadBalancers)页面，创建一个负载均衡器。

    - **负载均衡器类型**：`网络负载均衡器`
    - **代理或直通**：`直通`
    - **面向公网或内部**：`内部`
    - **负载均衡器名称**：`kafka-proxy-lb`
    - **区域**：`us-west1`
    - **网络**：你的网络
    - 后端配置
        - **后端类型**：`实例组`
        - **协议**：`TCP`
        - **实例组**：`kafka-proxy-ig`
    - 前端配置
        - **子网**：你的子网
        - **端口**：`全部`
        - 健康检查：
            - **名称**：`kafka-proxy-hc`
            - **范围**：`区域`
            - **协议**：`TCP`
            - **端口**：`9092`。你可以选择 Kafka-proxy 中的一个引导端口。

2. 转到[**Private Service Connect** > **发布服务**](https://console.cloud.google.com/net-services/psc/list/producers)。

    - **负载均衡器类型**：`内部直通网络负载均衡器`
    - **内部负载均衡器**：`kafka-proxy-lb`
    - **服务名称**：`kafka-proxy-psc`
    - **子网**：`保留新子网`
        - **名称**：`proxy-psc-subnet`
        - **VPC 网络**：你的网络
        - **区域**：`us-west1`
        - **IPv4 范围**：根据你的网络规划设置 CIDR
    - **接受的项目**：你在[前提条件](#前提条件)中获得的 TiDB Cloud 的 Google Cloud 项目，例如 `tidbcloud-prod-000`。

3. 导航到 **kafka-proxy-psc** 的详情页面。记下`服务附件`，例如 `projects/tidbcloud-dp-stg-000/regions/us-west1/serviceAttachments/kafka-proxy-psc`，你将在 TiDB Cloud 中使用它来连接到此 PSC。

4. 转到你的 VPC 网络的详情页面。添加防火墙规则以允许所有 broker 的 PSC 流量。

    - **名称**：`allow-proxy-psc-traffic`
    - **流量方向**：`入站`
    - **匹配时的操作**：`允许`
    - **目标**：网络中的所有实例
    - **源过滤器**：`IPv4 范围`
    - **源 IPv4 范围**：proxy-psc-subnet 的 CIDR
    - **协议和端口**：允许所有

### 步骤 3. 从 TiDB Cloud 连接

1. 返回 [TiDB Cloud 控制台](https://tidbcloud.com)，为集群创建一个通过 **Private Service Connect** 连接到 Kafka 集群的 changefeed。更多信息，请参阅[同步数据到 Apache Kafka](/tidb-cloud/changefeed-sink-to-apache-kafka.md)。

2. 当你进入**配置 changefeed 目标** > **连接方式** > **Private Service Connect** 时，使用相应的值填写以下字段和其他所需字段。

   - **Kafka 广播监听器模式**：`abc`。与你在[前提条件](#前提条件)中用于生成 **Kafka 广播监听器模式** 的唯一随机字符串相同。
   - **服务附件**：kafka-proxy 的 PSC 服务附件，例如 `projects/tidbcloud-dp-stg-000/regions/us-west1/serviceAttachments/kafka-proxy-psc`。
   - **引导端口**：`9092,9093,9094`

3. 继续按照[同步数据到 Apache Kafka](/tidb-cloud/changefeed-sink-to-apache-kafka.md)中的指南操作。

## 常见问题

### 如何从两个不同的 TiDB Cloud 项目连接到同一个 Kafka Private Service Connect 服务？

如果你已经按照本文档中的步骤操作并成功从第一个项目建立了连接，现在想要从第二个项目建立第二个连接，你可以通过以下方式从两个不同的 TiDB Cloud 项目连接到同一个 Kafka Private Service Connect 服务：

- 如果你通过 PSC 端口映射设置 Kafka PSC，请执行以下操作：

    1. 按照本文档从头开始操作。当你进行到[步骤 1. 设置 Kafka 集群](#步骤-1-设置-kafka-集群)时，按照[重新配置运行中的 Kafka 集群](#重新配置运行中的-kafka-集群)部分创建另一组 EXTERNAL 监听器和广播监听器。你可以将其命名为 `EXTERNAL2`。注意，`EXTERNAL2` 的端口范围不能与 EXTERNAL 重叠。

    2. 重新配置 broker 后，向网络端点组添加另一组网络端点，将端口范围映射到 `EXTERNAL2` 监听器。

    3. 使用以下输入配置 TiDB Cloud 连接以创建新的 changefeed：

        - 新的引导端口
        - 新的 Kafka 广播监听器模式
        - 相同的服务附件

- 如果你[通过 Kafka-proxy 设置自托管 Kafka Private Service Connect](#通过-kafka-proxy-设置自托管-kafka-private-service-connect)，请使用新的 Kafka 广播监听器模式从头开始创建新的 Kafka-proxy PSC。
