---
title: 将 TiDB Cloud 与 Airbyte 集成
summary: 了解如何使用 Airbyte TiDB 连接器。
---

# 将 TiDB Cloud 与 Airbyte 集成

[Airbyte](https://airbyte.com/) 是一个开源的数据集成引擎，用于构建提取、加载、转换（ELT）管道，并将您的数据整合到数据仓库、数据湖和数据库中。本文介绍如何将 Airbyte 作为源或目标连接到 TiDB Cloud。

## 部署 Airbyte

您只需几个步骤就可以在本地部署 Airbyte。

1. 在您的工作空间上安装 [Docker](https://www.docker.com/products/docker-desktop)。

2. 克隆 Airbyte 源代码。

    ```shell
    git clone https://github.com/airbytehq/airbyte.git && \
    cd airbyte
    ```

3. 使用 docker-compose 运行 Docker 镜像。

    ```shell
    docker-compose up
    ```

当您看到 Airbyte 横幅时，您可以使用用户名（`airbyte`）和密码（`password`）访问 [http://localhost:8000](http://localhost:8000) 来访问用户界面。

```
airbyte-server      |     ___    _      __          __
airbyte-server      |    /   |  (_)____/ /_  __  __/ /____
airbyte-server      |   / /| | / / ___/ __ \/ / / / __/ _ \
airbyte-server      |  / ___ |/ / /  / /_/ / /_/ / /_/  __/
airbyte-server      | /_/  |_/_/_/  /_.___/\__, /\__/\___/
airbyte-server      |                     /____/
airbyte-server      | --------------------------------------
airbyte-server      |  Now ready at http://localhost:8000/
airbyte-server      | --------------------------------------
```

## 设置 TiDB 连接器

无论将 TiDB 设置为源还是目标，步骤都是相同的。

1. 在侧边栏中点击**源**或**目标**，然后选择 TiDB 类型以创建新的 TiDB 连接器。

2. 填写以下参数。

    - 主机：TiDB Cloud 集群的端点
    - 端口：数据库的端口
    - 数据库：您想要同步数据的数据库
    - 用户名：访问数据库的用户名
    - 密码：用户名的密码

    您可以从集群的连接对话框中获取参数值。要打开对话框，请转到项目的[**集群**](https://tidbcloud.com/project/clusters)页面，点击目标集群的名称以进入其概览页面，然后点击右上角的**连接**。

3. 启用 **SSL 连接**，并在 **JDBC URL 参数**中将 TLS 协议设置为 **TLSv1.2** 或 **TLSv1.3**。

    > 注意：
    >
    > - TiDB Cloud 支持 TLS 连接。您可以在 **TLSv1.2** 和 **TLSv1.3** 中选择 TLS 协议，例如，`enabledTLSProtocols=TLSv1.2`。
    > - 如果您想通过 JDBC 禁用与 TiDB Cloud 的 TLS 连接，您需要在 JDBC URL 参数中特别将 useSSL 设置为 `false` 并关闭 SSL 连接，例如，`useSSL=false`。
    > - TiDB Cloud Serverless 仅支持 TLS 连接。

4. 点击**设置源**或**目标**以完成创建连接器。以下截图显示了将 TiDB 设置为源的配置。

![TiDB 源配置](/media/tidb-cloud/integration-airbyte-parameters.jpg)

您可以使用任何源和目标的组合，例如从 TiDB 到 Snowflake，或从 CSV 文件到 TiDB。

有关 TiDB 连接器的更多详细信息，请参见 [TiDB 源](https://docs.airbyte.com/integrations/sources/tidb)和 [TiDB 目标](https://docs.airbyte.com/integrations/destinations/tidb)。

## 设置连接

设置好源和目标后，您可以构建和配置连接。

以下步骤使用 TiDB 作为源和目标。其他连接器可能有不同的参数。

1. 在侧边栏中点击**连接**，然后点击**新建连接**。
2. 选择之前建立的源和目标。
3. 转到**设置**连接面板，为连接创建一个名称，例如 `${source_name} - ${destination-name}`。
4. 将**复制频率**设置为**每 24 小时**，这意味着连接每天复制一次数据。
5. 将**目标命名空间**设置为**自定义格式**，并将**命名空间自定义格式**设置为 **test**，以将所有数据存储在 `test` 数据库中。
6. 选择**同步模式**为**完全刷新 | 覆盖**。

    > **提示：**
    >
    > TiDB 连接器支持[增量和完全刷新同步](https://airbyte.com/blog/understanding-data-replication-modes)。
    >
    > - 在增量模式下，Airbyte 只读取自上次同步任务以来添加到源的记录。使用增量模式的第一次同步相当于完全刷新模式。
    > - 在完全刷新模式下，Airbyte 在每次同步任务中读取源中的所有记录并复制到目标。您可以在 Airbyte 中为每个名为**命名空间**的表单独设置同步模式。

    ![设置连接](/media/tidb-cloud/integration-airbyte-connection.jpg)

7. 将**规范化和转换**设置为**规范化表格数据**以使用默认规范化模式，或者您可以为您的任务设置 dbt 文件。有关规范化的更多信息，请参见[转换和规范化](https://docs.airbyte.com/operator-guides/transformation-and-normalization/transformations-with-dbt)。
8. 点击**设置连接**。
9. 建立连接后，点击**启用**以激活同步任务。您也可以点击**立即同步**立即同步。

![同步数据](/media/tidb-cloud/integration-airbyte-sync.jpg)

## 限制

- TiDB 连接器无法使用 TiCDC 提供的变更数据捕获（CDC）功能。增量同步基于游标机制执行。
- TiDB 目标在默认规范化模式下将 `timestamp` 类型转换为 `varchar` 类型。这是因为 Airbyte 在传输过程中将时间戳类型转换为字符串，而 TiDB 不支持 `cast ('2020-07-28 14:50:15+1:00' as timestamp)`。
- 对于一些大型 ELT 任务，您需要增加 TiDB 中[事务限制](/develop/dev-guide-transaction-restraints.md#large-transaction-restrictions)的参数。

## 另请参阅

[使用 Airbyte 将数据从 TiDB Cloud 迁移到 Snowflake](https://www.pingcap.com/blog/using-airbyte-to-migrate-data-from-tidb-cloud-to-snowflake/)。
