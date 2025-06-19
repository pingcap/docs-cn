---
title: 管理 Data App
summary: 了解如何在 TiDB Cloud 控制台中创建、查看、修改和删除 Data App。
---

# 管理 Data App

Data Service (beta) 中的 Data App 是一组用于访问特定应用程序数据的端点集合。你可以使用 API 密钥配置授权设置，以限制对 Data App 中端点的访问。

本文档介绍如何在 TiDB Cloud 控制台中管理你的 Data Apps。在 [**Data Service**](https://tidbcloud.com/project/data-service) 页面，你可以管理所有 Data Apps、端点和 API 密钥。

## 创建 Data App

要为你的项目创建 Data App，请执行以下步骤：

1. 在项目的 [**Data Service**](https://tidbcloud.com/project/data-service) 页面，点击左侧窗格中的 <MDSvgIcon name="icon-create-data-app" /> **Create DataApp**。

    > **提示：**
    >
    > 如果这是你项目中的第一个 Data App，请点击页面中间的 **Create Data App**。

2. 输入名称、描述，并选择你希望 Data App 访问的集群。

    > **注意：**
    >
    > 默认情况下，Data App 类型为 **Standard Data App**。如果你想创建 **Chat2Query Data App**，请参考 [Chat2Query API 入门](/tidb-cloud/use-chat2query-api.md)，而不是本文档。

3. （可选）要将 Data App 的端点自动部署到你首选的 GitHub 仓库和分支，请启用 **Connect to GitHub**，然后执行以下操作：

    1. 点击 **Install on GitHub**，然后按照屏幕上的说明将 **TiDB Cloud Data Service** 作为应用程序安装到你的目标仓库。
    2. 点击 **Authorize** 以授权访问 GitHub 上的应用程序。
    3. 指定要保存 Data App 配置文件的目标仓库、分支和目录。

        > **注意：**
        >
        > - 目录必须以斜杠（`/`）开头。例如，`/mydata`。如果你指定的目录在目标仓库和分支中不存在，它将自动创建。
        > - 仓库、分支和目录的组合标识了配置文件的路径，该路径在 Data Apps 中必须是唯一的。如果你指定的路径已被另一个 Data App 使用，你需要指定一个新路径。否则，当前 Data App 在 TiDB Cloud 控制台中配置的端点将覆盖你指定路径中的文件。
        > - 如果你指定的路径包含从另一个 Data App 复制的配置文件，并且你想将这些文件导入到当前 Data App，请参阅[导入现有 Data App 的配置](/tidb-cloud/data-service-manage-github-connection.md#import-configurations-of-an-existing-data-app)。

4. 点击 **Create Data App**。

    新创建的 Data App 将添加到列表顶部。系统会为新的 Data App 创建一个默认的 `untitled endpoint`。

5. 如果你已配置将 Data App 连接到 GitHub，请检查你指定的 GitHub 目录。你会发现 [Data App 配置文件](/tidb-cloud/data-service-app-config-files.md)已由 `tidb-cloud-data-service` 提交到该目录，这表示你的 Data App 已成功连接到 GitHub。

    对于你的新 Data App，默认启用 **Auto Sync & Deployment** 和 **Review Draft**，以便你可以轻松地在 TiDB Cloud 控制台和 GitHub 之间同步 Data App 更改，并在部署前审查更改。有关 GitHub 集成的更多信息，请参阅[使用 GitHub 自动部署 Data App 更改](/tidb-cloud/data-service-manage-github-connection.md)。

## 配置 Data App

你可以编辑 Data App 的名称、版本或描述，并管理其 GitHub 连接、链接的数据源、API 密钥、端点和部署。

### 编辑 Data App 属性

你可以编辑 Data App 的名称、版本和描述。要编辑 Data App 属性，请执行以下步骤：

1. 导航到项目的 [**Data Service**](https://tidbcloud.com/project/data-service) 页面。
2. 在左侧窗格中，点击目标 Data App 的名称以查看其详细信息。
3. 在 **Data App Properties** 区域，点击 <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" color="gray.1"><path d="M11 3.99998H6.8C5.11984 3.99998 4.27976 3.99998 3.63803 4.32696C3.07354 4.61458 2.6146 5.07353 2.32698 5.63801C2 6.27975 2 7.11983 2 8.79998V17.2C2 18.8801 2 19.7202 2.32698 20.362C2.6146 20.9264 3.07354 21.3854 3.63803 21.673C4.27976 22 5.11984 22 6.8 22H15.2C16.8802 22 17.7202 22 18.362 21.673C18.9265 21.3854 19.3854 20.9264 19.673 20.362C20 19.7202 20 18.8801 20 17.2V13M7.99997 16H9.67452C10.1637 16 10.4083 16 10.6385 15.9447C10.8425 15.8957 11.0376 15.8149 11.2166 15.7053C11.4184 15.5816 11.5914 15.4086 11.9373 15.0627L21.5 5.49998C22.3284 4.67156 22.3284 3.32841 21.5 2.49998C20.6716 1.67156 19.3284 1.67155 18.5 2.49998L8.93723 12.0627C8.59133 12.4086 8.41838 12.5816 8.29469 12.7834C8.18504 12.9624 8.10423 13.1574 8.05523 13.3615C7.99997 13.5917 7.99997 13.8363 7.99997 14.3255V16Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path></svg>，修改 App 名称、版本或描述，然后点击 **Confirm**。

### 管理 GitHub 连接

有关更多信息，请参阅[使用 GitHub 自动部署](/tidb-cloud/data-service-manage-github-connection.md)。

### 管理链接的数据源

你可以为 Data App 添加或删除链接的集群。

要将集群链接到 Data App，请执行以下步骤：

1. 导航到项目的 [**Data Service**](https://tidbcloud.com/project/data-service) 页面。
2. 在左侧窗格中，找到目标 Data App 并点击其名称以查看详细信息。
3. 在 **Linked Data Sources** 区域，点击 **Add Cluster**。
4. 在显示的对话框中，从列表中选择一个集群，然后点击 **Add**。

要从 Data App 中删除链接的集群，请执行以下步骤：

1. 导航到项目的 [**Data Service**](https://tidbcloud.com/project/data-service) 页面。
2. 在左侧窗格中，找到目标 Data App 并点击其名称以查看详细信息。
3. 在 **Linked Data Sources** 区域，找到要从 Data App 中删除的目标链接集群，然后在 **Action** 列中点击 **Delete**。
4. 在显示的对话框中确认删除。

    删除链接的集群后，该集群不会被删除，但 Data App 中的现有端点将无法访问它。

### 管理 API 密钥

有关更多信息，请参阅[管理 API 密钥](/tidb-cloud/data-service-api-key.md)。

### 管理端点

有关更多信息，请参阅[管理端点](/tidb-cloud/data-service-manage-endpoint.md)。

### 管理自定义域名

有关更多信息，请参阅[管理自定义域名](/tidb-cloud/data-service-custom-domain.md)。

### 管理部署

要管理部署，请执行以下步骤：

1. 导航到项目的 [**Data Service**](https://tidbcloud.com/project/data-service) 页面。
2. 在左侧窗格中，找到目标 Data App 并点击其名称以查看详细信息。
3. 在 **Deployment Configuration** 区域，点击 **Config**。将显示部署配置对话框。
4. 在对话框中，选择你想要的 **Auto Sync & Deployment** 和 **Review Draft** 设置。

    - **Auto Sync & Deployment**

        - 此选项仅在你的 Data App 连接到 GitHub 时才能启用。有关更多信息，请参阅[使用 GitHub 自动部署](/tidb-cloud/data-service-manage-github-connection.md)。
        - 启用后，在你指定的 GitHub 目录中所做的更改可以自动部署到 TiDB Cloud，在 TiDB Cloud 控制台中所做的更改也可以推送到 GitHub。你可以在 Data App 部署历史记录中找到相应的部署和提交信息。
        - 禁用后，在你指定的 GitHub 目录中所做的更改将**不会**部署到 TiDB Cloud，在 TiDB Cloud 控制台中所做的更改也将**不会**推送到 GitHub。

    - **Review Draft**

        - 启用后，你可以在部署前审查在 TiDB Cloud 控制台中所做的 Data App 更改。根据审查结果，你可以选择部署或放弃更改。
        - 禁用后，在 TiDB Cloud 控制台中所做的 Data App 更改将直接部署。

5. 在 **Action** 列中，你可以根据需要编辑或重新部署更改。

## 使用 OpenAPI 规范

Data Service (beta) 支持为每个 Data App 生成 OpenAPI 规范 3.0，使你能够以标准化格式与端点交互。你可以使用此规范生成标准化的 OpenAPI 文档、客户端 SDK 和服务器存根。

### 下载 OpenAPI 规范

要以 JSON 或 YAML 格式下载 Data App 的 OpenAPI 规范，请执行以下步骤：

1. 导航到项目的 [**Data Service**](https://tidbcloud.com/project/data-service) 页面。
2. 在左侧窗格中，点击目标 Data App 的名称以查看其详细信息。
3. 在 **API Specification** 区域，点击 **Download** 并选择 **JSON** 或 **YAML**。

    如果这是你第一次下载 OpenAPI 规范，系统会提示你授权请求。

4. 然后，OpenAPI 规范将下载到你的本地计算机。

### 查看 OpenAPI 文档

Data Service (beta) 为每个 Data App 提供自动生成的 OpenAPI 文档。在文档中，你可以查看端点、参数和响应，并试用端点。

要访问 OpenAPI 文档，请执行以下步骤：

1. 导航到项目的 [**Data Service**](https://tidbcloud.com/project/data-service) 页面。
2. 在左侧窗格中，点击目标 Data App 的名称以查看其详细信息。
3. 在页面右上角，点击 **View API Docs**。

    如果这是你第一次使用 OpenAPI 规范，系统会提示你授权请求。

4. 然后，OpenAPI 文档将在新标签页中打开。在文档中，你可以查看以下信息：

    - Data App 名称、版本和描述。
    - 按标签分组的端点。

5. （可选）要试用端点，请执行以下步骤：

    1. 点击 **Authorize** 并在显示的对话框中输入你的 Data App 公钥作为 **Username** 和私钥作为 **Password**。

        有关更多信息，请参阅[管理 API 密钥](/tidb-cloud/data-service-api-key.md)。

    2. 找到目标端点，提供所需参数，然后点击 **Try it out**。你可以在 **Response body** 区域查看响应。

  有关如何使用 OpenAPI 文档的更多信息，请参阅 [Swagger UI](https://swagger.io/tools/swagger-ui/)。

## 删除 Data App

> **注意：**
>
> 在删除 Data App 之前，请确保所有端点都未上线。否则，你将无法删除 Data App。要取消部署端点，请参考[取消部署端点](/tidb-cloud/data-service-manage-endpoint.md#undeploy-an-endpoint)。

要删除 Data App，请执行以下步骤：

1. 导航到项目的 [**Data Service**](https://tidbcloud.com/project/data-service) 页面。
2. 在左侧窗格中，找到目标 Data App 并点击其名称以查看详细信息。
3. 在 **Danger Zone** 区域，点击 **Delete Data App**。将显示确认对话框。
4. 输入你的 `<organization name>/<project name>/<data app name>`，然后点击 **I understand, delete**。

    一旦 Data App 被删除，Data App 中的现有端点和 API 密钥也将被删除。如果此 Data App 已连接到 GitHub，删除 App 不会删除相应 GitHub 仓库中的文件。

## 了解更多

- [在 Postman 中运行 Data App](/tidb-cloud/data-service-postman-integration.md)
