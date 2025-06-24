---
title: 使用 GitHub 自动部署 Data App
summary: 了解如何使用 GitHub 自动部署 Data App。
---

# 使用 GitHub 自动部署 Data App

TiDB Cloud 提供了一种配置即代码（Configuration as Code，CaC）的方法，使用 JSON 语法将整个 Data App 配置表示为代码。

通过将 Data App 连接到 GitHub，TiDB Cloud 可以使用 CaC 方法，将你的 Data App 配置作为[配置文件](/tidb-cloud/data-service-app-config-files.md)推送到你指定的 GitHub 仓库和分支。

如果为你的 GitHub 连接启用了**自动同步和部署**，你还可以通过在 GitHub 上更新配置文件来修改 Data App。将配置文件更改推送到 GitHub 后，新的配置将自动部署到 TiDB Cloud。

本文档介绍如何使用 GitHub 自动部署 Data App 以及如何管理 GitHub 连接。

## 开始之前

在将 Data App 连接到 GitHub 之前，请确保你具有以下条件：

- GitHub 账户。
- 带有目标分支的 GitHub 仓库。

> **注意：**
>
> GitHub 仓库用于在将 Data App 连接到它后存储 [Data App 配置文件](/tidb-cloud/data-service-app-config-files.md)。如果配置文件中的信息（如集群 ID 和端点 URL）比较敏感，请确保使用私有仓库而不是公共仓库。

## 步骤 1. 将 Data App 连接到 GitHub

你可以在创建 App 时将 Data App 连接到 GitHub。更多信息，请参见[创建 Data App](/tidb-cloud/data-service-manage-data-app.md)。

如果你在创建 App 时没有启用 GitHub 连接，你仍然可以按照以下方式启用它：

1. 导航到项目的 [**Data Service**](https://tidbcloud.com/project/data-service) 页面。
2. 在左侧窗格中，点击目标 Data App 的名称以查看其详细信息。
3. 在**设置**标签页上，点击**连接到 GitHub**区域中的**连接**。将显示连接设置对话框。
4. 在对话框中，执行以下步骤：

    1. 点击**在 GitHub 上安装**，然后按照屏幕上的说明将 **TiDB Cloud Data Service** 作为应用程序安装在目标仓库上。
    2. 点击**授权**以授权访问 GitHub 上的应用程序。
    3. 指定要存储 Data App 配置文件的目标仓库、分支和目录。

        > **注意：**
        >
        > - 目录必须以斜杠 (`/`) 开头。例如，`/mydata`。如果你指定的目录在目标仓库和分支中不存在，它将自动创建。
        > - 仓库、分支和目录的组合标识了配置文件的路径，该路径在 Data App 之间必须是唯一的。如果你指定的路径已被另一个 Data App 使用，你需要指定一个新路径。否则，当前 Data App 在 TiDB Cloud 控制台中配置的端点将覆盖你指定路径中的文件。
        > - 如果你指定的路径包含从另一个 Data App 复制的配置文件，并且你想将这些文件导入到当前 Data App，请参见[导入现有 Data App 的配置](#导入现有-data-app-的配置)。

    4. 要允许在 TiDB Cloud 控制台或 GitHub 中所做的 Data App 更改相互同步，请启用**配置自动同步和部署**。

        - 启用后，在你指定的 GitHub 目录中所做的更改可以自动部署到 TiDB Cloud，在 TiDB Cloud 控制台中所做的更改也可以推送到 GitHub。你可以在 Data App 部署历史记录中找到相应的部署和提交信息。
        - 禁用后，在你指定的 GitHub 目录中所做的更改将**不会**部署到 TiDB Cloud，在 TiDB Cloud 控制台中所做的更改也将**不会**推送到 GitHub。

5. 点击**确认连接**。

## 步骤 2. 将 Data App 配置与 GitHub 同步

如果在[创建 Data App](/tidb-cloud/data-service-manage-data-app.md) 时启用了 GitHub 连接，TiDB Cloud 会在 App 创建后立即将此 Data App 的配置文件推送到 GitHub。

如果在创建 App 后启用了 GitHub 连接，你需要执行部署操作以将 Data App 配置与 GitHub 同步。例如，你可以点击**部署**标签页，然后为此 Data App 重新部署一个部署。

部署操作后，检查你指定的 GitHub 目录。你会发现 Data App 配置文件已由 `tidb-cloud-data-service` 提交到该目录，这意味着你的 Data App 已成功连接到 GitHub。目录结构如下：

```
├── <你在 GitHub 上的 Data App 目录>
│   ├── data_sources
│   │   └── cluster.json  # 指定链接的集群。
│   ├── dataapp_config.json # 指定 Data APP ID、名称、类型、版本和描述。
│   ├── http_endpoints
│   │   ├── config.json # 指定端点。
│   │   └── sql # 包含端点的 SQL 文件。
│   │       ├── <method>-<endpoint-path1>.sql
│   │       ├── <method>-<endpoint-path2>.sql
│   │       └── <method>-<endpoint-path3>.sql
```

## 步骤 3. 修改 Data App

启用**自动同步和部署**后，你可以使用 GitHub 或 TiDB Cloud 控制台修改 Data App。

- [选项 1：通过在 GitHub 上更新文件修改 Data App](#选项-1通过在-github-上更新文件修改-data-app)
- [选项 2：在 TiDB Cloud 控制台中修改 Data App](#选项-2在-tidb-cloud-控制台中修改-data-app)

> **注意：**
>
> 如果你同时在 GitHub 和 TiDB Cloud 控制台上修改了 Data App，要解决冲突，你可以选择放弃在控制台中所做的更改，或让控制台更改覆盖 GitHub 更改。

### 选项 1：通过在 GitHub 上更新文件修改 Data App

更新配置文件时，请注意以下事项：

| 文件目录  | 注意事项 |
| ---------|---------|
| `data_source/cluster.json`     | 更新此文件时，请确保你有权访问链接的集群。你可以从集群 URL 获取集群 ID。例如，如果集群 URL 是 `https://tidbcloud.com/clusters/1234567891234567890/overview`，则集群 ID 是 `1234567891234567890`。 |
| `http_endpoints/config.json`     | 修改端点时，请确保遵循[HTTP 端点配置](/tidb-cloud/data-service-app-config-files.md#http-endpoint-configuration)中描述的规则。   |
| `http_endpoints/sql/method-<endpoint-path>.sql`| 要在 `http_endpoints/sql` 目录中添加或删除 SQL 文件，你还需要更新相应的端点配置。 |
| `datapp_config.json` | 除非你的 `dataapp_config.json` 文件是从另一个 Data App 复制的，并且你想将其更新为当前 Data App 的 ID，否则不要更改此文件中的 `app_id` 字段。否则，由此修改触发的部署将失败。 |

有关这些文件中字段配置的更多信息，请参见 [Data App 配置文件](/tidb-cloud/data-service-app-config-files.md)。

文件更改提交并推送后，TiDB Cloud 将自动使用 GitHub 上的最新更改部署 Data App。你可以在部署历史记录中查看部署状态和提交信息。

### 选项 2：在 TiDB Cloud 控制台中修改 Data App

在 TiDB Cloud 控制台中[修改 Data App 端点](/tidb-cloud/data-service-manage-endpoint.md)（如修改端点）后，你可以按照以下方式审查并将更改部署到 GitHub：

1. 点击右上角的**部署**。将显示一个对话框，供你审查所做的更改。
2. 根据你的审查，执行以下操作之一：

    - 如果你仍想基于当前草稿进行进一步更改，关闭此对话框并进行更改。
    - 如果你想将当前更改恢复到上次部署，点击**放弃草稿**。
    - 如果当前更改看起来没问题，写一个更改描述（可选），然后点击**部署并推送到 GitHub**。部署状态将显示在顶部横幅中。

如果部署成功，在 TiDB Cloud 控制台中所做的更改将自动推送到 GitHub。

## 导入现有 Data App 的配置

要将现有 Data App 的配置导入到新的 Data App，请执行以下步骤：

1. 将现有 Data App 的配置文件复制到 GitHub 上的新分支或目录。
2. 在项目的 [**Data Service**](https://tidbcloud.com/project/data-service) 页面上，[创建一个新的 Data App](/tidb-cloud/data-service-manage-data-app.md#create-a-data-app)，不要连接到 GitHub。
3. 启用**自动同步和部署**，[将新的 Data App 连接到 GitHub](#步骤-1-将-data-app-连接到-github)。为新的 Data App 指定目标仓库、分支和目录时，使用包含复制的配置文件的新路径。
4. 获取新 Data App 的 ID 和名称。你可以在左侧窗格中点击新 Data App 的名称，在右侧窗格的 **Data App 属性**区域中获取 App ID 和名称。
5. 在 GitHub 上的新路径中，将 `datapp_config.json` 文件中的 `app_id` 和 `app_name` 更新为你获取的 ID 和名称，然后推送更改。

    将文件更改推送到 GitHub 后，TiDB Cloud 将自动使用最新更改部署新的 Data App。

6. 要查看从 GitHub 导入的配置，请刷新 TiDB Cloud 控制台的网页。

    你还可以在部署历史记录中查看部署状态和提交信息。

## 编辑 GitHub 连接

如果你想编辑 Data App 的 GitHub 连接（如切换仓库、分支和目录），请执行以下步骤。

1. 导航到项目的 [**Data Service**](https://tidbcloud.com/project/data-service) 页面。
2. 在左侧窗格中，点击目标 Data App 的名称以查看其详细信息。
3. 在**连接到 GitHub**区域中，点击 <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" color="gray.1"><path d="M11 3.99998H6.8C5.11984 3.99998 4.27976 3.99998 3.63803 4.32696C3.07354 4.61458 2.6146 5.07353 2.32698 5.63801C2 6.27975 2 7.11983 2 8.79998V17.2C2 18.8801 2 19.7202 2.32698 20.362C2.6146 20.9264 3.07354 21.3854 3.63803 21.673C4.27976 22 5.11984 22 6.8 22H15.2C16.8802 22 17.7202 22 18.362 21.673C18.9265 21.3854 19.3854 20.9264 19.673 20.362C20 19.7202 20 18.8801 20 17.2V13M7.99997 16H9.67452C10.1637 16 10.4083 16 10.6385 15.9447C10.8425 15.8957 11.0376 15.8149 11.2166 15.7053C11.4184 15.5816 11.5914 15.4086 11.9373 15.0627L21.5 5.49998C22.3284 4.67156 22.3284 3.32841 21.5 2.49998C20.6716 1.67156 19.3284 1.67155 18.5 2.49998L8.93723 12.0627C8.59133 12.4086 8.41838 12.5816 8.29469 12.7834C8.18504 12.9624 8.10423 13.1574 8.05523 13.3615C7.99997 13.5917 7.99997 13.8363 7.99997 14.3255V16Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path></svg>。将显示连接设置对话框。
4. 在对话框中，修改 Data App 的仓库、分支和目录。

    > **注意：**
    >
    > - 目录必须以斜杠 (`/`) 开头。例如，`/mydata`。如果你指定的目录在目标仓库和分支中不存在，它将自动创建。
    > - 仓库、分支和目录的组合标识了配置文件的路径，该路径在 Data App 之间必须是唯一的。如果你指定的路径已被另一个 Data App 使用，你需要指定一个新路径。否则，当前 Data App 在 TiDB Cloud 控制台中配置的端点将覆盖你指定路径中的文件。
    > - 如果你指定的路径包含从另一个 Data App 复制的配置文件，并且你想将这些文件导入到当前 Data App，请参见[导入现有 Data App 的配置](#导入现有-data-app-的配置)。

5. 要允许在 TiDB Cloud 控制台或 GitHub 中所做的 Data App 更改相互同步，请启用**配置自动同步和部署**。

    - 启用后，在你指定的 GitHub 目录中所做的更改可以自动部署到 TiDB Cloud，在 TiDB Cloud 控制台中所做的更改也可以推送到 GitHub。你可以在 Data App 部署历史记录中找到相应的部署和提交信息。
    - 禁用后，在你指定的 GitHub 目录中所做的更改将**不会**部署到 TiDB Cloud，在 TiDB Cloud 控制台中所做的更改也将**不会**推送到 GitHub。

6. 点击**确认连接**。

## 移除 GitHub 连接

如果你不再想将 Data App 连接到 GitHub，请执行以下步骤：

1. 导航到项目的 [**Data Service**](https://tidbcloud.com/project/data-service) 页面。
2. 在左侧窗格中，点击目标 Data App 的名称以查看其详细信息。
3. 在**设置**标签页上，点击**连接到 GitHub**区域中的**断开连接**。
4. 点击**断开连接**以确认断开连接。

断开连接操作后，你的 Data App 配置文件将保留在 GitHub 目录中，但不会再由 `tidb-cloud-data-service` 同步。
