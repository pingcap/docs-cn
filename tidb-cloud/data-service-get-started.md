---
title: 数据服务入门
summary: 了解如何使用 TiDB Cloud 数据服务通过 HTTPS 请求访问数据。
---

# 数据服务入门

数据服务（beta）使您能够通过自定义 API 端点使用 HTTPS 请求访问 TiDB Cloud 数据，让您可以无缝集成任何支持 HTTPS 的应用程序或服务。

> **提示：**
>
> TiDB Cloud 为 TiDB 集群提供 Chat2Query API。启用后，TiDB Cloud 将自动在数据服务中创建一个名为 **Chat2Query** 的系统数据应用和一个 Chat2Data 端点。您可以调用此端点，通过提供指令让 AI 生成并执行 SQL 语句。
>
> 更多信息，请参阅[Chat2Query API 入门](/tidb-cloud/use-chat2query-api.md)。

本文介绍如何通过创建数据应用、开发、测试、部署和调用端点，快速开始使用 TiDB Cloud 数据服务（beta）。数据应用是一组端点的集合，您可以使用这些端点访问特定应用程序的数据。

## 开始之前

在创建数据应用之前，请确保您已创建了一个 [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群。如果您还没有，请按照[创建 TiDB Cloud Serverless 集群](/tidb-cloud/create-tidb-cluster-serverless.md)中的步骤创建一个。

## 从示例数据应用开始

创建示例数据应用是开始使用数据服务的最佳方式。如果您的项目还没有任何数据应用，可以按照**数据服务**页面上的屏幕说明创建一个示例数据应用，并使用此应用探索数据服务功能。

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com)中，点击左侧导航栏中的 <MDSvgIcon name="icon-left-data-service" /> **数据服务**。

2. 在**数据服务**页面，点击**创建示例数据应用**。将显示一个对话框。

3. 在对话框中，根据需要更新应用名称，选择您希望数据应用访问的集群，然后点击**创建**。

    创建过程需要几秒钟。

    > **注意：**
    >
    > 如果您当前的项目中没有集群，可以在**链接数据源**下拉列表中点击**创建新集群**先创建一个。

4. 示例数据应用自动创建后，您可以在左侧窗格中看到应用名称和端点列表，中间窗格中显示端点的 SQL 语句，右侧显示使用示例数据应用的说明。

5. 按照右侧的说明选择一个端点并使用 curl 命令调用该端点。

## 从您自己的数据应用开始

要开始使用数据服务，您也可以创建自己的数据应用，然后按照以下步骤开发、测试、部署和调用端点。

### 步骤 1. 创建数据应用

要创建数据应用，请执行以下步骤：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com)中，点击左侧导航栏中的 <MDSvgIcon name="icon-left-data-service" /> **数据服务**。

2. 在项目的[**数据服务**](https://tidbcloud.com/project/data-service)页面，点击左侧窗格中的 <MDSvgIcon name="icon-create-data-app" /> **创建数据应用**。

    > **提示：**
    >
    > 如果这是您项目中的第一个数据应用，请点击页面中间的**创建数据应用**。

3. 在**创建数据应用**对话框中，输入名称、描述，并选择您希望数据应用访问的集群。

    > **注意：**
    >
    > 默认情况下，数据应用类型为**标准数据应用**。如果您想创建 **Chat2Query 数据应用**，请参考 [Chat2Query API 入门](/tidb-cloud/use-chat2query-api.md)而不是本文档。

4. （可选）要自动将数据应用的端点部署到您首选的 GitHub 仓库和分支，请启用**连接到 GitHub**，然后执行以下操作：

    1. 点击**在 GitHub 上安装**，然后按照屏幕说明在目标仓库上安装 **TiDB Cloud Data Service** 应用。
    2. 返回 TiDB Cloud 控制台，然后点击**授权**以授权访问 GitHub 上的应用。
    3. 指定要保存数据应用配置文件的目标仓库、分支和目录。

    > **注意：**
    >
    > - 目录必须以斜杠 (`/`) 开头。例如，`/mydata`。如果您指定的目录在目标仓库和分支中不存在，将自动创建。
    > - 仓库、分支和目录的组合标识了配置文件的路径，在数据应用中必须是唯一的。如果您指定的路径已被另一个数据应用使用，您需要指定一个新路径。否则，当前数据应用在 TiDB Cloud 控制台中配置的端点将覆盖您指定路径中的文件。

5. 点击**创建数据应用**。将显示[**数据服务**](https://tidbcloud.com/project/data-service)详情页面。

6. 如果您已配置将数据应用连接到 GitHub，请检查您指定的 GitHub 目录。您会发现[数据应用配置文件](/tidb-cloud/data-service-app-config-files.md)已由 `tidb-cloud-data-service` 提交到该目录，这意味着您的数据应用已成功连接到 GitHub。

    对于您的新数据应用，默认启用了**自动同步和部署**和**审核草稿**，这样您就可以轻松地在 TiDB Cloud 控制台和 GitHub 之间同步数据应用更改，并在部署前审核更改。有关 GitHub 集成的更多信息，请参阅[使用 GitHub 自动部署数据应用更改](/tidb-cloud/data-service-manage-github-connection.md)。

### 步骤 2. 开发端点

端点是一个可以自定义执行 SQL 语句的 Web API。

要创建新端点，找到新创建的数据应用，然后点击应用名称右侧的 **+** **创建端点**。

#### 配置属性

在右侧窗格中，点击**属性**选项卡并为端点设置属性，例如：

- **路径**：用户访问端点的路径。请求方法和路径的组合在数据应用中必须是唯一的。

- **端点 URL**：（只读）URL 根据相应集群所在的区域、数据应用的服务 URL 和端点的路径自动生成。例如，如果端点的路径是 `/my_endpoint/get_id`，则端点 URL 为 `https://<region>.data.tidbcloud.com/api/v1beta/app/<App ID>/endpoint/my_endpoint/get_id`。

- **请求方法**：端点的 HTTP 方法。您可以使用 `GET` 检索数据，使用 `POST` 创建或插入数据，使用 `PUT` 更新或修改数据，使用 `DELETE` 删除数据。

有关端点属性的更多信息，请参阅[配置属性](/tidb-cloud/data-service-manage-endpoint.md#configure-properties)。

#### 编写 SQL 语句

您可以在 SQL 编辑器（即页面中间的窗格）中为端点自定义 SQL 语句。

1. 选择集群。

    > **注意：**
    >
    > 下拉列表中只显示链接到数据应用的集群。要管理链接的集群，请参阅[管理链接的集群](/tidb-cloud/data-service-manage-data-app.md#manage-linked-data-sources)。

    在 SQL 编辑器的上部，从下拉列表中选择要执行 SQL 语句的集群。然后，您可以在右侧窗格的**架构**选项卡中查看此集群的所有数据库。

2. 编写 SQL 语句。

    在查询或修改数据之前，您需要先在 SQL 语句中指定数据库。例如，`USE database_name;`。

    在 SQL 编辑器中，您可以编写表连接查询、复杂查询和聚合函数等语句。您也可以简单地输入 `--` 后跟您的指令，让 AI 自动生成 SQL 语句。

    > **注意：**
    >
    > 要尝试 TiDB Cloud 的 AI 功能，您需要允许 PingCAP 和 Amazon Bedrock 使用您的代码片段进行研究和服务改进。更多信息，请参阅[启用或禁用 AI 生成 SQL 查询](/tidb-cloud/explore-data-with-chat2query.md#enable-or-disable-ai-to-generate-sql-queries)。

    要定义参数，您可以在 SQL 语句中插入变量占位符，如 `${ID}`。例如，`SELECT * FROM table_name WHERE id = ${ID}`。然后，您可以点击右侧窗格的**参数**选项卡来更改参数定义和测试值。

    > **注意：**
    >
    > - 参数名称区分大小写。
    > - 参数不能用作表名或列名。

    - 在**定义**部分，您可以指定客户端调用端点时是否需要参数、数据类型和参数的默认值。
    - 在**测试值**部分，您可以为参数设置测试值。测试值在运行 SQL 语句或测试端点时使用。如果您没有设置测试值，将使用默认值。
    - 更多信息，请参阅[配置参数](/tidb-cloud/data-service-manage-endpoint.md#configure-parameters)。

3. 运行 SQL 语句。

    如果您在 SQL 语句中插入了参数，请确保您已在右侧窗格的**参数**选项卡中设置了测试值或默认值。否则，将返回错误。

    <SimpleTab>
    <div label="macOS">

    对于 macOS：

    - 如果编辑器中只有一条语句，要运行它，请按 **⌘ + Enter** 或点击 <svg width="1rem" height="1rem" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M6.70001 20.7756C6.01949 20.3926 6.00029 19.5259 6.00034 19.0422L6.00034 12.1205L6 5.33028C6 4.75247 6.00052 3.92317 6.38613 3.44138C6.83044 2.88625 7.62614 2.98501 7.95335 3.05489C8.05144 3.07584 8.14194 3.12086 8.22438 3.17798L19.2865 10.8426C19.2955 10.8489 19.304 10.8549 19.3126 10.8617C19.4069 10.9362 20 11.4314 20 12.1205C20 12.7913 19.438 13.2784 19.3212 13.3725C19.307 13.3839 19.2983 13.3902 19.2831 13.4002C18.8096 13.7133 8.57995 20.4771 8.10002 20.7756C7.60871 21.0812 7.22013 21.0683 6.70001 20.7756Z" fill="currentColor"></path></svg>**运行**。

    - 如果编辑器中有多条语句，要按顺序运行其中一条或几条语句，请将光标放在目标语句上或用光标选择目标语句的行，然后按 **⌘ + Enter** 或点击**运行**。

    - 要按顺序运行编辑器中的所有语句，请按 **⇧ + ⌘ + Enter**，或用光标选择所有语句的行并点击**运行**。

    </div>

    <div label="Windows/Linux">

    对于 Windows 或 Linux：

    - 如果编辑器中只有一条语句，要运行它，请按 **Ctrl + Enter** 或点击 <svg width="1rem" height="1rem" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M6.70001 20.7756C6.01949 20.3926 6.00029 19.5259 6.00034 19.0422L6.00034 12.1205L6 5.33028C6 4.75247 6.00052 3.92317 6.38613 3.44138C6.83044 2.88625 7.62614 2.98501 7.95335 3.05489C8.05144 3.07584 8.14194 3.12086 8.22438 3.17798L19.2865 10.8426C19.2955 10.8489 19.304 10.8549 19.3126 10.8617C19.4069 10.9362 20 11.4314 20 12.1205C20 12.7913 19.438 13.2784 19.3212 13.3725C19.307 13.3839 19.2983 13.3902 19.2831 13.4002C18.8096 13.7133 8.57995 20.4771 8.10002 20.7756C7.60871 21.0812 7.22013 21.0683 6.70001 20.7756Z" fill="currentColor"></path></svg>**运行**。

    - 如果编辑器中有多条语句，要按顺序运行其中一条或几条语句，请将光标放在目标语句上或用光标选择目标语句的行，然后按 **Ctrl + Enter** 或点击**运行**。

    - 要按顺序运行编辑器中的所有语句，请按 **Shift + Ctrl + Enter**，或用光标选择所有语句的行并点击**运行**。

    </div>
    </SimpleTab>

    运行语句后，您可以在页面底部的**结果**选项卡中立即看到查询结果。

### 步骤 3. 测试端点（可选）

配置端点后，您可以在部署之前测试端点，以验证它是否按预期工作。

要测试端点，请点击右上角的**测试**或按 **F5**。

然后，您可以在页面底部的 **HTTP 响应**选项卡中看到响应。有关响应的更多信息，请参阅[端点的响应](/tidb-cloud/data-service-manage-endpoint.md#response)。

### 步骤 4. 部署端点

要部署端点，请执行以下步骤：

1. 在端点详情页面，点击右上角的**部署**。

2. 点击**部署**确认部署。如果端点成功部署，您将看到**端点已部署**的提示。

    要查看部署历史记录，您可以点击左侧窗格中的数据应用名称，然后点击右侧窗格中的**部署**选项卡。

### 步骤 5. 调用端点

您可以通过发送 HTTPS 请求来调用端点。在调用端点之前，您需要先获取数据应用的 API 密钥。

#### 1. 创建 API 密钥

1. 在[**数据服务**](https://tidbcloud.com/project/data-service)页面的左侧窗格中，点击数据应用的名称以查看其详情。
2. 在**身份验证**区域，点击**创建 API 密钥**。
3. 在**创建 API 密钥**对话框中，执行以下操作：

    1. （可选）为您的 API 密钥输入描述。
    2. 为您的 API 密钥选择角色。

        角色用于控制 API 密钥是否可以读取或写入链接到数据应用的集群数据。您可以选择 `ReadOnly` 或 `ReadAndWrite` 角色：

        - `ReadOnly`：仅允许 API 密钥读取数据，如 `SELECT`、`SHOW`、`USE`、`DESC` 和 `EXPLAIN` 语句。
        - `ReadAndWrite`：允许 API 密钥读取和写入数据。您可以使用此 API 密钥执行所有 SQL 语句，如 DML 和 DDL 语句。

    3. （可选）为您的 API 密钥设置所需的速率限制。

4. 点击**下一步**。将显示公钥和私钥。

    确保您已将私钥复制并保存在安全的位置。离开此页面后，您将无法再次获取完整的私钥。

5. 点击**完成**。

有关 API 密钥的更多信息，请参阅[数据服务中的 API 密钥](/tidb-cloud/data-service-api-key.md)。

#### 2. 获取代码示例

TiDB Cloud 生成代码示例以帮助您调用端点。要获取代码示例，请执行以下步骤：

1. 在[**数据服务**](https://tidbcloud.com/project/data-service)页面的左侧窗格中，点击端点的名称，然后点击右上角的 **...** > **代码示例**。将显示**代码示例**对话框。

2. 在对话框中，选择要用于调用端点的集群和数据库，然后复制代码示例。

    以下是 curl 代码示例：

    <SimpleTab>
    <div label="测试环境">

    要调用端点的草稿版本，您需要添加 `endpoint-type: draft` 头：

    ```bash
    curl --digest --user '<Public Key>:<Private Key>' \
      --request GET 'https://<region>.data.tidbcloud.com/api/v1beta/app/<App ID>/endpoint/<Endpoint Path>' \
      --header 'endpoint-type: draft'
    ```

    </div>

    <div label="线上环境">

    在检查线上环境的代码示例之前，您必须先部署端点。

    要调用端点的当前线上版本，请使用以下命令：

    ```bash
    curl --digest --user '<Public Key>:<Private Key>' \
      --request GET 'https://<region>.data.tidbcloud.com/api/v1beta/app/<App ID>/endpoint/<Endpoint Path>'
    ```

    </div>
    </SimpleTab>

    > **注意：**
    >
    > - 通过请求区域域名 `<region>.data.tidbcloud.com`，您可以直接访问 TiDB 集群所在区域的端点。
    > - 或者，您也可以请求全局域名 `data.tidbcloud.com` 而不指定区域。这样，TiDB Cloud 将在内部将请求重定向到目标区域，但这可能会导致额外的延迟。如果您选择这种方式，请确保在调用端点时在 curl 命令中添加 `--location-trusted` 选项。

#### 3. 使用代码示例

将代码示例粘贴到您的应用程序中并运行。然后，您可以获取端点的响应。

- 您需要将 `<Public Key>` 和 `<Private Key>` 占位符替换为您的 API 密钥。
- 如果端点包含参数，请在调用端点时指定参数值。

调用端点后，您可以看到 JSON 格式的响应。以下是一个示例：

```json
{
  "type": "sql_endpoint",
  "data": {
    "columns": [
      {
        "col": "id",
        "data_type": "BIGINT",
        "nullable": false
      },
      {
        "col": "type",
        "data_type": "VARCHAR",
        "nullable": false
      }
    ],
    "rows": [
      {
        "id": "20008295419",
        "type": "CreateEvent"
      }
    ],
    "result": {
      "code": 200,
      "message": "Query OK!",
      "start_ms": 1678965476709,
      "end_ms": 1678965476839,
      "latency": "130ms",
      "row_count": 1,
      "row_affect": 0,
      "limit": 50
    }
  }
}
```

有关响应的更多信息，请参阅[端点的响应](/tidb-cloud/data-service-manage-endpoint.md#response)。

## 了解更多

- [数据服务概述](/tidb-cloud/data-service-overview.md)
- [Chat2Query API 入门](/tidb-cloud/use-chat2query-api.md)
- [管理数据应用](/tidb-cloud/data-service-manage-data-app.md)
- [管理端点](/tidb-cloud/data-service-manage-endpoint.md)
