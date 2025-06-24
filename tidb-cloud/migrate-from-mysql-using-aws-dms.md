---
title: 使用 AWS DMS 将 MySQL 兼容数据库迁移至 TiDB Cloud
summary: 了解如何使用 AWS Database Migration Service (AWS DMS) 将数据从 MySQL 兼容数据库迁移至 TiDB Cloud。
---

# 使用 AWS DMS 将 MySQL 兼容数据库迁移至 TiDB Cloud

如果你想迁移异构数据库（如 PostgreSQL、Oracle 和 SQL Server）到 TiDB Cloud，建议使用 AWS Database Migration Service (AWS DMS)。

AWS DMS 是一项云服务，可以轻松迁移关系数据库、数据仓库、NoSQL 数据库和其他类型的数据存储。你可以使用 AWS DMS 将数据迁移到 TiDB Cloud。

本文以 Amazon RDS 为例，展示如何使用 AWS DMS 将数据迁移到 TiDB Cloud。此过程也适用于将数据从自托管 MySQL 数据库或 Amazon Aurora 迁移到 TiDB Cloud。

在本例中，数据源是 Amazon RDS，数据目标是 TiDB Cloud 中的 TiDB Cloud Dedicated 集群。上游和下游数据库都在同一区域。

## 前提条件

在开始迁移之前，请确保你已阅读以下内容：

- 如果源数据库是 Amazon RDS 或 Amazon Aurora，你需要将 `binlog_format` 参数设置为 `ROW`。如果数据库使用默认参数组，`binlog_format` 参数默认为 `MIXED` 且无法修改。在这种情况下，你需要[创建一个新的参数组](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_GettingStarted.Prerequisites.html#CHAP_GettingStarted.Prerequisites.params)，例如 `newset`，并将其 `binlog_format` 设置为 `ROW`。然后，[修改默认参数组](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithDBInstanceParamGroups.html#USER_WorkingWithParamGroups.Modifying)为 `newset`。请注意，修改参数组将重启数据库。
- 检查并确保源数据库使用与 TiDB 兼容的排序规则。TiDB 中 utf8mb4 字符集的默认排序规则是 `utf8mb4_bin`。但在 MySQL 8.0 中，默认排序规则是 `utf8mb4_0900_ai_ci`。如果上游 MySQL 使用默认排序规则，由于 TiDB 不兼容 `utf8mb4_0900_ai_ci`，AWS DMS 无法在 TiDB 中创建目标表并且无法迁移数据。要解决此问题，你需要在迁移前将源数据库的排序规则修改为 `utf8mb4_bin`。有关 TiDB 支持的字符集和排序规则的完整列表，请参见[字符集和排序规则](https://docs.pingcap.com/tidb/stable/character-set-and-collation)。
- TiDB 默认包含以下系统数据库：`INFORMATION_SCHEMA`、`PERFORMANCE_SCHEMA`、`mysql`、`sys` 和 `test`。当你创建 AWS DMS 迁移任务时，你需要过滤掉这些系统数据库，而不是使用默认的 `%` 来选择迁移对象。否则，AWS DMS 将尝试将这些系统数据库从源数据库迁移到目标 TiDB，这将导致任务失败。为避免此问题，建议填写具体的数据库和表名。
- 将 AWS DMS 的公网和私网 IP 地址添加到源数据库和目标数据库的 IP 访问列表中。否则，在某些情况下网络连接可能会失败。
- 使用 [VPC 对等连接](/tidb-cloud/set-up-vpc-peering-connections.md#在-aws-上设置-vpc-对等连接)或[私有端点连接](/tidb-cloud/set-up-private-endpoint-connections.md)来连接 AWS DMS 和 TiDB 集群。
- 建议将 AWS DMS 和 TiDB 集群使用相同的区域，以获得更好的数据写入性能。
- 建议使用 AWS DMS `dms.t3.large`（2 个 vCPU 和 8 GiB 内存）或更高实例类型。较小的实例类型可能会导致内存不足（OOM）错误。
- AWS DMS 将在目标数据库中自动创建 `awsdms_control` 数据库。

## 限制

- AWS DMS 不支持复制 `DROP TABLE`。
- AWS DMS 支持基本的架构迁移，包括创建表和主键。但是，AWS DMS 不会自动在 TiDB Cloud 中创建二级索引、外键或用户账户。如果需要，你必须手动在 TiDB 中创建这些对象，包括带有二级索引的表。更多信息，请参见 [Migration planning for AWS Database Migration Service](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_BestPractices.html#CHAP_SettingUp.MigrationPlanning)。

## 步骤 1. 创建 AWS DMS 复制实例

1. 在 AWS DMS 控制台中转到[复制实例](https://console.aws.amazon.com/dms/v2/home#replicationInstances)页面，并切换到相应的区域。建议 AWS DMS 使用与 TiDB Cloud 相同的区域。在本文档中，上游和下游数据库以及 DMS 实例都在 **us-west-2** 区域。

2. 点击**创建复制实例**。

    ![创建复制实例](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-create-instance.png)

3. 填写实例名称、ARN 和描述。

4. 填写实例配置：
    - **实例类型**：选择适当的实例类型。建议使用 `dms.t3.large` 或更高实例类型以获得更好的性能。
    - **引擎版本**：使用默认配置。
    - **多可用区**：根据业务需求选择**单可用区**或**多可用区**。

5. 在**分配存储（GiB）**字段中配置存储。使用默认配置。

6. 配置连接和安全性。
    - **网络类型 - 新**：选择 **IPv4**。
    - **IPv4 的虚拟私有云（VPC）**：选择你需要的 VPC。建议使用与上游数据库相同的 VPC 以简化网络配置。
    - **复制子网组**：为你的复制实例选择一个子网组。
    - **公共可访问**：使用默认配置。

7. 根据需要配置**高级设置**、**维护**和**标签**。点击**创建复制实例**完成实例创建。

## 步骤 2. 创建源数据库端点

1. 在 [AWS DMS 控制台](https://console.aws.amazon.com/dms/v2/home)中，点击你刚刚创建的复制实例。复制公网和私网 IP 地址，如下图所示。

    ![复制公网和私网 IP 地址](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-copy-ip.png)

2. 配置 Amazon RDS 的安全组规则。在本例中，将 AWS DMS 实例的公网和私网 IP 地址添加到安全组中。

    ![配置安全组规则](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-rules.png)

3. 点击**创建端点**以创建源数据库端点。

    ![点击创建端点](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-endpoint.png)

4. 在本例中，点击**选择 RDS DB 实例**，然后选择源 RDS 实例。如果源数据库是自托管 MySQL，你可以跳过此步骤，直接在后续步骤中填写信息。

    ![选择 RDS DB 实例](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-select-rds.png)

5. 配置以下信息：
   - **端点标识符**：为源端点创建一个标签，以帮助你在后续任务配置中识别它。
   - **描述性 Amazon Resource Name (ARN) - 可选**：为默认 DMS ARN 创建一个友好名称。
   - **源引擎**：选择 **MySQL**。
   - **访问端点数据库**：选择**手动提供访问信息**。
   - **服务器名称**：填写数据提供者的数据服务器名称。你可以从数据库控制台复制它。如果上游是 Amazon RDS 或 Amazon Aurora，名称将自动填充。如果是没有域名的自托管 MySQL，你可以填写 IP 地址。
   - 填写源数据库的**端口**、**用户名**和**密码**。
   - **安全套接字层 (SSL) 模式**：你可以根据需要启用 SSL 模式。

    ![填写端点配置](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-endpoint-config.png)

6. 对于**端点设置**、**KMS 密钥**和**标签**，使用默认值。在**测试端点连接（可选）**部分，建议选择与源数据库相同的 VPC 以简化网络配置。选择相应的复制实例，然后点击**运行测试**。状态需要为**成功**。

7. 点击**创建端点**。

    ![点击创建端点](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-connection.png)
## 步骤 3. 创建目标数据库端点

1. 在 [AWS DMS 控制台](https://console.aws.amazon.com/dms/v2/home)中，点击你刚刚创建的复制实例。复制公网和私网 IP 地址，如下图所示。

    ![复制公网和私网 IP 地址](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-copy-ip.png)

2. 在 TiDB Cloud 控制台中，转到[**集群**](https://tidbcloud.com/project/clusters)页面，点击目标集群的名称，然后点击右上角的**连接**以获取 TiDB Cloud 数据库连接信息。

3. 在对话框中的**步骤 1：创建流量过滤器**下，点击**编辑**，输入你从 AWS DMS 控制台复制的公网和私网 IP 地址，然后点击**更新过滤器**。建议同时将 AWS DMS 复制实例的公网 IP 地址和私网 IP 地址添加到 TiDB 集群的流量过滤器中。否则，在某些情况下 AWS DMS 可能无法连接到 TiDB 集群。

4. 点击**下载 CA 证书**以下载 CA 证书。在对话框中的**步骤 3：使用 SQL 客户端连接**下，记下连接字符串中的 `-u`、`-h` 和 `-P` 信息，以供后续使用。

5. 在对话框中点击 **VPC 对等连接**选项卡，然后在**步骤 1：设置 VPC**下点击**添加**，为 TiDB 集群和 AWS DMS 创建 VPC 对等连接。

6. 配置相应的信息。请参见[设置 VPC 对等连接](/tidb-cloud/set-up-vpc-peering-connections.md)。

7. 为 TiDB 集群配置目标端点。
    - **端点类型**：选择**目标端点**。
    - **端点标识符**：为端点填写一个名称。
    - **描述性 Amazon Resource Name (ARN) - 可选**：为默认 DMS ARN 创建一个友好名称。
    - **目标引擎**：选择 **MySQL**。

    ![配置目标端点](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-target-endpoint.png)

8. 在 [AWS DMS 控制台](https://console.aws.amazon.com/dms/v2/home)中，点击**创建端点**以创建目标数据库端点，然后配置以下信息：
    - **服务器名称**：填写你的 TiDB 集群的主机名，即你记录的 `-h` 信息。
    - **端口**：输入你的 TiDB 集群的端口，即你记录的 `-P` 信息。TiDB 集群的默认端口是 4000。
    - **用户名**：输入你的 TiDB 集群的用户名，即你记录的 `-u` 信息。
    - **密码**：输入你的 TiDB 集群的密码。
    - **安全套接字层 (SSL) 模式**：选择 **Verify-ca**。
    - 点击**添加新的 CA 证书**以导入之前从 TiDB Cloud 控制台下载的 CA 文件。

    ![填写目标端点信息](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-target-endpoint2.png)

9. 导入 CA 文件。

    ![上传 CA](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-upload-ca.png)

10. 对于**端点设置**、**KMS 密钥**和**标签**，使用默认值。在**测试端点连接（可选）**部分，选择与源数据库相同的 VPC。选择相应的复制实例，然后点击**运行测试**。状态需要为**成功**。

11. 点击**创建端点**。

    ![点击创建端点](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-target-endpoint3.png)

## 步骤 4. 创建数据库迁移任务

1. 在 AWS DMS 控制台中，转到[数据迁移任务](https://console.aws.amazon.com/dms/v2/home#tasks)页面。切换到你的区域。然后点击窗口右上角的**创建任务**。

    ![创建任务](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-create-task.png)

2. 配置以下信息：
    - **任务标识符**：为任务填写一个名称。建议使用容易记住的名称。
    - **描述性 Amazon Resource Name (ARN) - 可选**：为默认 DMS ARN 创建一个友好名称。
    - **复制实例**：选择你刚刚创建的 AWS DMS 实例。
    - **源数据库端点**：选择你刚刚创建的源数据库端点。
    - **目标数据库端点**：选择你刚刚创建的目标数据库端点。
    - **迁移类型**：根据需要选择迁移类型。在本例中，选择**迁移现有数据并复制持续变更**。

    ![任务配置](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-task-config.png)

3. 配置以下信息：
    - **编辑模式**：选择**向导**。
    - **源事务的自定义 CDC 停止模式**：使用默认设置。
    - **目标表准备模式**：根据需要选择**不执行任何操作**或其他选项。在本例中，选择**不执行任何操作**。
    - **完成全量加载后停止任务**：使用默认设置。
    - **在复制中包含 LOB 列**：选择**有限 LOB 模式**。
    - **最大 LOB 大小（KB）**：使用默认值 **32**。
    - **开启验证**：根据需要选择。
    - **任务日志**：选择**开启 CloudWatch 日志**以便将来进行故障排除。对相关配置使用默认设置。

    ![任务设置](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-task-settings.png)

4. 在**表映射**部分，指定要迁移的数据库。

    架构名称是 Amazon RDS 实例中的数据库名称。**源名称**的默认值是"%"，这意味着 Amazon RDS 中的所有数据库都将迁移到 TiDB。这将导致 Amazon RDS 中的系统数据库（如 `mysql` 和 `sys`）被迁移到 TiDB 集群，并导致任务失败。因此，建议填写具体的数据库名称，或过滤掉所有系统数据库。例如，根据以下截图中的设置，只有名为 `franktest` 的数据库及其所有表会被迁移。

    ![表映射](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-table-mappings.png)

5. 点击右下角的**创建任务**。

6. 返回[数据迁移任务](https://console.aws.amazon.com/dms/v2/home#tasks)页面。切换到你的区域。你可以看到任务的状态和进度。

    ![任务状态](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-task-status.png)

如果在迁移过程中遇到任何问题或失败，你可以在 [CloudWatch](https://console.aws.amazon.com/cloudwatch/home) 中查看日志信息以排除问题。

![故障排除](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-troubleshooting.png)

## 另请参阅

- 如果你想了解更多关于如何将 AWS DMS 连接到 TiDB Cloud Serverless 或 TiDB Cloud Dedicated 的信息，请参见[将 AWS DMS 连接到 TiDB Cloud 集群](/tidb-cloud/tidb-cloud-connect-aws-dms.md)。

- 如果你想从 MySQL 兼容数据库（如 Aurora MySQL 和 Amazon Relational Database Service (RDS)）迁移到 TiDB Cloud，建议使用 [TiDB Cloud 上的数据迁移](/tidb-cloud/migrate-from-mysql-using-data-migration.md)。

- 如果你想使用 AWS DMS 将 Amazon RDS for Oracle 迁移到 TiDB Cloud Serverless，请参见[使用 AWS DMS 将 Amazon RDS for Oracle 迁移到 TiDB Cloud Serverless](/tidb-cloud/migrate-from-oracle-using-aws-dms.md)。
