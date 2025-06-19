---
title: 数据库审计日志
summary: 了解如何在 TiDB Cloud 中审计集群。
---

# 数据库审计日志

TiDB Cloud 提供数据库审计日志功能，可以在日志中记录用户访问详情的历史记录（例如执行的任何 SQL 语句）。

> **注意：**
>
> 目前，数据库审计日志功能仅供申请使用。要申请此功能，请点击 [TiDB Cloud 控制台](https://tidbcloud.com)右下角的 **?**，然后点击 **Request Support**。然后，在 **Description** 字段中填写"申请数据库审计日志"，并点击 **Submit**。

为了评估组织的用户访问策略和其他信息安全措施的有效性，定期分析数据库审计日志是一种安全最佳实践。

审计日志功能默认是禁用的。要审计集群，你需要先启用审计日志，然后指定审计过滤规则。

> **注意：**
>
> 由于审计日志会消耗集群资源，请谨慎考虑是否对集群进行审计。

## 前提条件

- 你正在使用 TiDB Cloud Dedicated 集群。TiDB Cloud Serverless 集群不支持审计日志。
- 你是组织的 `Organization Owner` 或 `Project Owner` 角色。否则，你将无法在 TiDB Cloud 控制台中看到数据库审计相关选项。有关更多信息，请参见[用户角色](/tidb-cloud/manage-user-access.md#用户角色)。

## 启用审计日志

TiDB Cloud 支持将 TiDB Cloud Dedicated 集群的审计日志记录到你的云存储服务中。在启用数据库审计日志之前，请在集群所在的云服务提供商上配置你的云存储服务。

> **注意：**
>
> 对于部署在 AWS 上的 TiDB 集群，你可以在启用数据库审计日志时选择将审计日志文件存储在 TiDB Cloud 中。目前，此功能仅供申请使用。要申请此功能，请点击 [TiDB Cloud 控制台](https://tidbcloud.com)右下角的 **?**，然后点击 **Request Support**。然后，在 **Description** 字段中填写"申请将审计日志文件存储在 TiDB Cloud 中"，并点击 **Submit**。

### 为 AWS 启用审计日志

要为 AWS 启用审计日志，请执行以下步骤：

#### 步骤 1. 创建 Amazon S3 存储桶

在你公司拥有的 AWS 账号中指定一个 Amazon S3 存储桶作为 TiDB Cloud 写入审计日志的目标位置。

> 注意：
>
> 不要在 AWS S3 存储桶上启用对象锁定。启用对象锁定将阻止 TiDB Cloud 将审计日志文件推送到 S3。

有关更多信息，请参见 AWS 用户指南中的[创建存储桶](https://docs.aws.amazon.com/AmazonS3/latest/userguide/create-bucket-overview.html)。

#### 步骤 2. 配置 Amazon S3 访问权限

1. 获取你要启用审计日志的 TiDB 集群的 TiDB Cloud 账号 ID 和外部 ID。

    1. 在 TiDB Cloud 控制台中，导航到项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面。

        > **提示：**
        >
        > 你可以使用左上角的组合框在组织、项目和集群之间切换。

    2. 点击目标集群的名称进入其概览页面，然后在左侧导航栏中点击 **Settings** > **DB Audit Logging**。
    3. 在 **DB Audit Logging** 页面，点击右上角的 **Enable**。
    4. 在 **Enable Database Audit Logging** 对话框中，找到 **AWS IAM Policy Settings** 部分，记录 **TiDB Cloud Account ID** 和 **TiDB Cloud External ID** 以供后续使用。

2. 在 AWS 管理控制台中，转到 **IAM** > **Access Management** > **Policies**，然后检查是否存在具有 `s3:PutObject` 只写权限的存储桶策略。

    - 如果存在，记录匹配的存储桶策略以供后续使用。
    - 如果不存在，转到 **IAM** > **Access Management** > **Policies** > **Create Policy**，并根据以下策略模板定义存储桶策略。

        ```json
        {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": "s3:PutObject",
                    "Resource": "<Your S3 bucket ARN>/*"
                }
            ]
        }
        ```

        在模板中，`<Your S3 bucket ARN>` 是要写入审计日志文件的 S3 存储桶的 Amazon 资源名称（ARN）。你可以转到 S3 存储桶的 **Properties** 标签页，在 **Bucket Overview** 区域获取 ARN 值。在 `"Resource"` 字段中，你需要在 ARN 后添加 `/*`。例如，如果 ARN 是 `arn:aws:s3:::tidb-cloud-test`，你需要将 `"Resource"` 字段的值配置为 `"arn:aws:s3:::tidb-cloud-test/*"`。

3. 转到 **IAM** > **Access Management** > **Roles**，然后检查是否已存在一个信任实体对应于你之前记录的 TiDB Cloud 账号 ID 和外部 ID 的角色。

    - 如果存在，记录匹配的角色以供后续使用。
    - 如果不存在，点击 **Create role**，选择 **Another AWS account** 作为信任实体类型，然后在 **Account ID** 字段中输入 TiDB Cloud 账号 ID 值。然后，选择 **Require External ID** 选项，并在 **External ID** 字段中输入 TiDB Cloud 外部 ID 值。

4. 在 **IAM** > **Access Management** > **Roles** 中，点击上一步中的角色名称进入 **Summary** 页面，然后执行以下步骤：

    1. 在 **Permissions** 标签页下，检查是否已将具有 `s3:PutObject` 只写权限的记录策略附加到角色。如果没有，选择 **Attach Policies**，搜索所需策略，然后点击 **Attach Policy**。
    2. 返回 **Summary** 页面并复制 **Role ARN** 值到剪贴板。

#### 步骤 3. 启用审计日志

在 TiDB Cloud 控制台中，返回获取 TiDB Cloud 账号 ID 和外部 ID 值的 **Enable Database Audit Logging** 对话框，然后执行以下步骤：

1. 在 **Bucket URI** 字段中，输入要写入审计日志文件的 S3 存储桶的 URI。
2. 在 **Bucket Region** 下拉列表中，选择存储桶所在的 AWS 区域。
3. 在 **Role ARN** 字段中，填入你在[步骤 2. 配置 Amazon S3 访问权限](#步骤-2-配置-amazon-s3-访问权限)中复制的 Role ARN 值。
4. 点击 **Test Connection** 验证 TiDB Cloud 是否可以访问和写入存储桶。

    如果成功，将显示 **The connection is successfully**。否则，请检查你的访问配置。

5. 点击 **Enable** 为集群启用审计日志。

    TiDB Cloud 已准备好将指定集群的审计日志写入你的 Amazon S3 存储桶。

> **注意：**
>
> - 启用审计日志后，如果你对存储桶 URI、位置或 ARN 进行任何新的更改，必须再次点击 **Test Connection** 以验证 TiDB Cloud 是否可以连接到存储桶。然后，点击 **Enable** 应用更改。
> - 要移除 TiDB Cloud 对 Amazon S3 的访问权限，只需在 AWS 管理控制台中删除授予此集群的信任策略即可。

### 为 Google Cloud 启用审计日志

要为 Google Cloud 启用审计日志，请执行以下步骤：

#### 步骤 1. 创建 GCS 存储桶

在你公司拥有的 Google Cloud 账号中指定一个 Google Cloud Storage (GCS) 存储桶作为 TiDB Cloud 写入审计日志的目标位置。

有关更多信息，请参见 Google Cloud Storage 文档中的[创建存储桶](https://cloud.google.com/storage/docs/creating-buckets)。

#### 步骤 2. 配置 GCS 访问权限

1. 获取你要启用审计日志的 TiDB 集群的 Google Cloud 服务账号 ID。

    1. 在 TiDB Cloud 控制台中，导航到项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面。

        > **提示：**
        >
        > 你可以使用左上角的组合框在组织、项目和集群之间切换。

    2. 点击目标集群的名称进入其概览页面，然后在左侧导航栏中点击 **Settings** > **DB Audit Logging**。
    3. 在 **DB Audit Logging** 页面，点击右上角的 **Enable**。
    4. 在 **Enable Database Audit Logging** 对话框中，找到 **Google Cloud Server Account ID** 部分，记录 **Service Account ID** 以供后续使用。

2. 在 Google Cloud 控制台中，转到 **IAM & Admin** > **Roles**，然后检查是否存在具有以下存储容器只写权限的角色。

    - storage.objects.create
    - storage.objects.delete

    如果存在，为 TiDB 集群记录匹配的角色以供后续使用。如果不存在，转到 **IAM & Admin** > **Roles** > **CREATE ROLE** 为 TiDB 集群定义角色。

3. 转到 **Cloud Storage** > **Browser**，选择你想要 TiDB Cloud 访问的 GCS 存储桶，然后点击 **SHOW INFO PANEL**。

    面板将显示。

4. 在面板中，点击 **ADD PRINCIPAL**。

    将显示添加主体的对话框。

5. 在对话框中，执行以下步骤：

    1. 在 **New Principals** 字段中，粘贴 TiDB 集群的 Google Cloud 服务账号 ID。
    2. 在 **Role** 下拉列表中，选择目标 TiDB 集群的角色。
    3. 点击 **SAVE**。

#### 步骤 3. 启用审计日志

在 TiDB Cloud 控制台中，返回获取 TiDB Cloud 账号 ID 的 **Enable Database Audit Logging** 对话框，然后执行以下步骤：

1. 在 **Bucket URI** 字段中，输入你的完整 GCS 存储桶名称。
2. 在 **Bucket Region** 字段中，选择存储桶所在的 GCS 区域。
3. 点击 **Test Connection** 验证 TiDB Cloud 是否可以访问和写入存储桶。

    如果成功，将显示 **The connection is successfully**。否则，请检查你的访问配置。

4. 点击 **Enable** 为集群启用审计日志。

    TiDB Cloud 已准备好将指定集群的审计日志写入你的 GCS 存储桶。

> **注意：**
>
> - 启用审计日志后，如果你对存储桶 URI 或位置进行任何新的更改，必须再次点击 **Test Connection** 以验证 TiDB Cloud 是否可以连接到存储桶。然后，点击 **Enable** 应用更改。
> - 要移除 TiDB Cloud 对 GCS 存储桶的访问权限，请在 Google Cloud 控制台中删除授予此集群的信任策略。

### 为 Azure 启用审计日志

要为 Azure 启用审计日志，请执行以下步骤：

#### 步骤 1. 创建 Azure 存储账号

在你组织的 Azure 订阅中创建一个 Azure 存储账号作为 TiDB Cloud 写入数据库审计日志的目标位置。

有关更多信息，请参见 Azure 文档中的[创建 Azure 存储账号](https://learn.microsoft.com/en-us/azure/storage/common/storage-account-create?tabs=azure-portal)。

#### 步骤 2. 配置 Azure Blob 存储访问权限

1. 在 [Azure 门户](https://portal.azure.com/)中，创建用于存储数据库审计日志的容器。

    1. 在 Azure 门户的左侧导航栏中，点击 **Storage Accounts**，然后点击用于存储数据库审计日志的存储账号。

        > **提示：**
        >
        > 如果左侧导航栏被隐藏，点击左上角的菜单按钮切换其可见性。

    2. 在所选存储账号的导航栏中，点击 **Data storage > Containers**，然后点击 **+ Container** 打开 **New container** 窗格。

    3. 在 **New container** 窗格中，输入新容器的名称，设置匿名访问级别（推荐级别是 **Private**，表示无匿名访问），然后点击 **Create**。新容器将在几秒钟内创建并显示在容器列表中。

2. 获取目标容器的 URL。

    1. 在容器列表中，选择目标容器，点击容器的 **...**，然后选择 **Container properties**。
    2. 在显示的属性页面上，复制 **URL** 值以供后续使用，然后返回容器列表。

3. 为目标容器生成 SAS 令牌。

    1. 在容器列表中，选择目标容器，点击容器的 **...**，然后选择 **Generate SAS**。
    2. 在显示的 **Generate SAS** 窗格中，为 **Signing method** 选择 **Account key**。
    3. 在 **Permissions** 下拉列表中，选择 **Read**、**Write** 和 **Create** 以允许写入审计日志文件。
    4. 在 **Start** 和 **Expiry** 字段中，指定 SAS 令牌的有效期。

        > **注意：**
        >
        > - 审计功能需要持续将审计日志写入存储账号，因此 SAS 令牌必须具有足够长的有效期。但是，较长的有效期会增加令牌泄露的风险。为了安全起见，建议每六到十二个月更换一次 SAS 令牌。
        > - 生成的 SAS 令牌无法撤销，因此你需要谨慎设置其有效期。
        > - 确保在令牌过期之前重新生成并更新 SAS 令牌，以确保审计日志的持续可用性。

    5. 对于 **Allowed protocols**，选择 **HTTPS only** 以确保安全访问。
    6. 点击 **Generate SAS token and URL**，然后复制显示的 **Blob SAS token** 以供后续使用。

#### 步骤 3. 启用审计日志

1. 在 TiDB Cloud 控制台中，导航到项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面。

    > **提示：**
    >
    > 你可以使用左上角的组合框在组织、项目和集群之间切换。

2. 点击目标集群的名称进入其概览页面，然后在左侧导航栏中点击 **Settings** > **DB Audit Logging**。
3. 在 **DB Audit Logging** 页面，点击右上角的 **Enable**。
4. 在 **Enable Database Audit Logging** 对话框中，提供从[步骤 2. 配置 Azure Blob 访问权限](#步骤-2-配置-azure-blob-存储访问权限)获取的 blob URL 和 SAS 令牌：

    - 在 **Blob URL** 字段中，输入存储审计日志的容器的 URL。
    - 在 **SAS Token** 字段中，输入用于访问容器的 SAS 令牌。

5. 点击 **Test Connection** 验证 TiDB Cloud 是否可以访问和写入容器。

    如果成功，将显示 **The connection is successfully**。否则，请检查你的访问配置。

6. 点击 **Enable** 为集群启用审计日志。

    TiDB Cloud 已准备好将指定集群的审计日志写入你的 Azure blob 容器。

> **注意：**
>
> 启用审计日志后，如果你对 **Blob URL** 或 **SAS Token** 字段进行新的更改，必须再次点击 **Test Connection** 以验证 TiDB Cloud 是否可以连接到容器。然后，点击 **Enable** 应用更改。

## 指定审计过滤规则

启用审计日志后，你必须指定审计过滤规则来控制要捕获并写入审计日志的用户访问事件。如果未指定过滤规则，TiDB Cloud 不会记录任何内容。

要为集群指定审计过滤规则，请执行以下步骤：

1. 在 **DB Audit Logging** 页面的 **Log Filter Rules** 部分，点击 **Add Filter Rule** 添加审计过滤规则。

    你一次可以添加一个审计规则。每个规则指定一个用户表达式、数据库表达式、表表达式和访问类型。你可以添加多个审计规则以满足你的审计要求。

2. 在 **Log Filter Rules** 部分，点击 **>** 展开并查看你已添加的审计规则列表。

> **注意：**
>
> - 过滤规则是正则表达式且区分大小写。如果使用通配符规则 `.*`，将记录集群中所有用户、数据库或表事件。
> - 由于审计日志会消耗集群资源，请谨慎指定过滤规则。为了最小化消耗，建议你指定过滤规则以尽可能将审计日志的范围限制在特定的数据库对象、用户和操作上。

## 查看审计日志

默认情况下，TiDB Cloud 将数据库审计日志文件存储在你的存储服务中，因此你需要从你的存储服务中读取审计日志信息。

> **注意：**
>
> 如果你已申请并选择将审计日志文件存储在 TiDB Cloud 中，你可以从 **Database Audit Logging** 页面的 **Audit Log Access** 部分下载它们。

TiDB Cloud 审计日志是可读的文本文件，文件名中包含集群 ID、Pod ID 和日志创建日期。

例如，`13796619446086334065/tidb-0/tidb-audit-2022-04-21T18-16-29.529.log`。在此示例中，`13796619446086334065` 表示集群 ID，`tidb-0` 表示 Pod ID。

## 禁用审计日志

如果你不再想审计集群，请转到集群页面，点击 **Settings** > **Audit Settings**，然后将右上角的审计设置切换为 **Off**。

> **注意：**
>
> 每当日志文件大小达到 10 MiB 时，日志文件将被推送到云存储桶。因此，在禁用审计日志后，大小小于 10 MiB 的日志文件不会自动推送到云存储桶。要在这种情况下获取日志文件，请联系 [PingCAP 支持](/tidb-cloud/tidb-cloud-support.md)。

## 审计日志字段

对于审计日志中的每个数据库事件记录，TiDB 提供以下字段：

> **注意：**
>
> 在下表中，字段的最大长度为空表示该字段的数据类型具有明确定义的固定长度（例如，INTEGER 为 4 字节）。

| 列号 | 字段名 | TiDB 数据类型 | 最大长度 | 描述 |
|---|---|---|---|---|
| 1 | N/A | N/A | N/A | 保留供内部使用 |
| 2 | N/A | N/A | N/A | 保留供内部使用 |
| 3 | N/A | N/A | N/A | 保留供内部使用 |
| 4 | ID       | INTEGER |  | 唯一事件 ID  |
| 5 | TIMESTAMP | TIMESTAMP |  | 事件时间   |
| 6 | EVENT_CLASS | VARCHAR | 15 | 事件类型     |
| 7 | EVENT_SUBCLASS     | VARCHAR | 15 | 事件子类型 |
| 8 | STATUS_CODE | INTEGER |  | 语句的响应状态   |
| 9 | COST_TIME | FLOAT |  | 语句消耗的时间    |
| 10 | HOST | VARCHAR | 16 | 服务器 IP    |
| 11 | CLIENT_IP         | VARCHAR | 16 | 客户端 IP   |
| 12 | USER | VARCHAR | 17 | 登录用户名    |
| 13 | DATABASE | VARCHAR | 64 | 事件相关的数据库      |
| 14 | TABLES | VARCHAR | 64 | 事件相关的表名          |
| 15 | SQL_TEXT | VARCHAR | 64 KB | 掩码 SQL 语句   |
| 16 | ROWS | INTEGER |  | 受影响的行数（`0` 表示没有行受影响）      |

根据 TiDB 设置的 EVENT_CLASS 字段值，审计日志中的数据库事件记录还包含以下附加字段：

- 如果 EVENT_CLASS 值为 `CONNECTION`，数据库事件记录还包含以下字段：

    | 列号 | 字段名 | TiDB 数据类型 | 最大长度 | 描述 |
    |---|---|---|---|---|
    | 17 | CLIENT_PORT | INTEGER |  | 客户端端口号 |
    | 18 | CONNECTION_ID | INTEGER |  | 连接 ID |
    | 19 | CONNECTION_TYPE  | VARCHAR | 12 | 通过 `socket` 或 `unix-socket` 连接 |
    | 20 | SERVER_ID | INTEGER |  | TiDB 服务器 ID |
    | 21 | SERVER_PORT | INTEGER |  | TiDB 服务器用于监听通过 MySQL 协议通信的客户端的端口 |
    | 22 | SERVER_OS_LOGIN_USER | VARCHAR | 17 | TiDB 进程启动系统的用户名  |
    | 23 | OS_VERSION | VARCHAR | N/A | TiDB 服务器所在操作系统的版本  |
    | 24 | SSL_VERSION | VARCHAR | 6 | TiDB 当前的 SSL 版本 |
    | 25 | PID | INTEGER |  | TiDB 进程的 PID |

- 如果 EVENT_CLASS 值为 `TABLE_ACCESS` 或 `GENERAL`，数据库事件记录还包含以下字段：

    | 列号 | 字段名 | TiDB 数据类型 | 最大长度 | 描述 |
    |---|---|---|---|---|
    | 17 | CONNECTION_ID | INTEGER |  | 连接 ID   |
    | 18 | COMMAND | VARCHAR | 14 | MySQL 协议的命令类型 |
    | 19 | SQL_STATEMENT  | VARCHAR | 17 | SQL 语句类型 |
    | 20 | PID | INTEGER |  | TiDB 进程的 PID  |
