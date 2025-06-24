---
title: 将 TiDB Cloud 与 n8n 集成
summary: 了解如何在 n8n 中使用 TiDB Cloud 节点。
---

# 将 TiDB Cloud 与 n8n 集成

[n8n](https://n8n.io/) 是一个可扩展的工作流自动化工具。通过 [fair-code](https://faircode.io/) 分发模式，n8n 将始终保持源代码可见，支持自托管，并允许你添加自定义函数、逻辑和应用程序。

本文介绍如何构建一个自动工作流：创建 TiDB Cloud Serverless 集群，收集 Hacker News RSS，将其存储到 TiDB 并发送简报邮件。

## 前提条件：获取 TiDB Cloud API 密钥

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com)中，使用左上角的组合框切换到目标组织。
2. 在左侧导航栏中，点击**组织设置** > **API 密钥**。
3. 在 **API 密钥**页面，点击**创建 API 密钥**。
4. 输入 API 密钥的描述，然后点击**下一步**。
5. 复制创建的 API 密钥以供后续在 n8n 中使用，然后点击**完成**。

更多信息，请参阅 [TiDB Cloud API 概览](/tidb-cloud/api-overview.md)。

## 步骤 1：安装 n8n

有两种方式可以安装自托管的 n8n。选择适合你的方式即可。

<SimpleTab>
<div label="npm">

1. 在你的工作空间安装 [node.js](https://nodejs.org/en/download/)。
2. 通过 `npx` 下载并启动 n8n。

    ```shell
    npx n8n
    ```

</div>
<div label="Docker">

1. 在你的工作空间安装 [Docker](https://www.docker.com/products/docker-desktop)。
2. 通过 `docker` 下载并启动 n8n。

    ```shell
    docker run -it --rm --name n8n -p 5678:5678 -v ~/.n8n:/home/node/.n8n n8nio/n8n
    ```

</div>
</SimpleTab>

启动 n8n 后，你可以访问 [localhost:5678](http://localhost:5678) 来试用 n8n。

## 步骤 2：在 n8n 中安装 TiDB Cloud 节点

TiDB Cloud 节点在 npm 仓库中的名称为 `n8n-nodes-tidb-cloud`。你需要手动安装此节点才能使用 n8n 控制 TiDB Cloud。

1. 在 [localhost:5678](http://localhost:5678) 页面，为自托管的 n8n 创建一个所有者账户。
2. 转到**设置** > **社区节点**。
3. 点击**安装社区节点**。
4. 在 **npm 包名称**字段中，输入 `n8n-nodes-tidb-cloud`。
5. 点击**安装**。

然后，你可以在**工作流** > 搜索栏中搜索 **TiDB Cloud** 节点，并通过将其拖动到工作区来使用 TiDB Cloud 节点。

## 步骤 3：构建工作流

在此步骤中，你将创建一个新的工作流，当你点击**执行**按钮时，它会向 TiDB 插入一些数据。

此示例工作流将使用以下节点：

- [Schedule Trigger](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.scheduletrigger/)
- [RSS Read](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.rssfeedread/)
- [Code](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.code/)
- [Gmail](https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-base.gmail/)
- [TiDB Cloud node](https://www.npmjs.com/package/n8n-nodes-tidb-cloud)

最终的工作流应如下图所示。

![img](/media/tidb-cloud/integration-n8n-workflow-rss.jpg)

### （可选）创建 TiDB Cloud Serverless 集群

如果你还没有 TiDB Cloud Serverless 集群，可以使用此节点创建一个。否则，可以跳过此操作。

1. 导航到**工作流**面板，点击**添加工作流**。
2. 在新的工作流工作区中，点击右上角的 **+** 并选择**全部**字段。
3. 搜索 `TiDB Cloud` 并将其拖动到工作区。
4. 为 TiDB Cloud 节点输入凭据，即 TiDB Cloud API 密钥。
5. 在**项目**列表中，选择你的项目。
6. 在**操作**列表中，选择 `Create Serverless Cluster`。
7. 在**集群名称**框中，输入集群名称。
8. 在**区域**列表中，选择一个区域。
9. 在**密码**框中，输入用于登录 TiDB 集群的密码。
10. 点击**执行节点**以运行节点。

> **注意：**
>
> 创建新的 TiDB Cloud Serverless 集群需要几秒钟时间。

### 创建工作流

#### 使用手动触发器作为工作流的起点

1. 如果你还没有工作流，请导航到**工作流**面板，然后点击**从头开始**。否则，请跳过此步骤。
2. 点击右上角的 **+** 并搜索 `schedule trigger`。
3. 将手动触发器节点拖动到工作区，然后双击该节点。此时会显示**参数**对话框。
4. 按如下方式配置规则：

    - **触发间隔**：`天`
    - **触发间隔天数**：`1`
    - **触发小时**：`8am`
    - **触发分钟**：`0`

此触发器将在每天早上 8 点执行你的工作流。

#### 创建用于插入数据的表

1. 点击手动触发器节点右侧的 **+**。
2. 搜索 `TiDB Cloud` 并将其添加到工作区。
3. 在**参数**对话框中，输入 TiDB Cloud 节点的凭据。凭据是你的 TiDB Cloud API 密钥。
4. 在**项目**列表中，选择你的项目。
5. 在**操作**列表中，选择 `Execute SQL`。
6. 选择集群。如果你在列表中看不到新集群，需要等待几分钟，直到集群创建完成。
7. 在**用户**列表中，选择一个用户。TiDB Cloud 始终创建一个默认用户，因此你不必手动创建。
8. 在**数据库**框中，输入 `test`。
9. 输入你的数据库密码。
10. 在 **SQL** 框中，输入以下 SQL：

    ```sql
    CREATE TABLE IF NOT EXISTS hacker_news_briefing (creator VARCHAR (200), title TEXT,  link VARCHAR(200), pubdate VARCHAR(200), comments VARCHAR(200), content TEXT, guid VARCHAR (200), isodate VARCHAR(200));
    ```

11. 点击**执行节点**以创建表。

#### 获取 Hacker News RSS

1. 点击 TiDB Cloud 节点右侧的 **+**。
2. 搜索 `RSS Read` 并将其添加到工作区。
3. 在 **URL** 框中，输入 `https://hnrss.org/frontpage`。

#### 将数据插入 TiDB

1. 点击 RSS Read 节点右侧的 **+**。
2. 搜索 `TiDB Cloud` 并将其添加到工作区。
3. 选择你在前面的 TiDB Cloud 节点中输入的凭据。
4. 在**项目**列表中，选择你的项目。
5. 在**操作**列表中，选择 `Insert`。
6. 在**集群**、**用户**、**数据库**和**密码**框中，输入相应的值。
7. 在**表**框中，输入 `hacker_news_briefing` 表。
8. 在**列**框中，输入 `creator, title, link, pubdate, comments, content, guid, isodate`。

#### 构建消息

1. 点击 RSS Feed Read 节点右侧的 **+**。
2. 搜索 `code` 并将其添加到工作区。
3. 选择 `Run Once for All Items` 模式。
4. 在 **JavaScript** 框中，复制并粘贴以下代码。

    ```javascript
    let message = "";

    // Loop the input items
    for (item of items) {
      message += `
          <h3>${item.json.title}</h3>
          <br>
          ${item.json.content}
          <br>
          `
    }

    let response =
        `
          <!DOCTYPE html>
          <html>
          <head>
          <title>Hacker News Briefing</title>
        </head>
        <body>
            ${message}
        </body>
        </html>
        `
    // Return our message
    return [{json: {response}}];
    ```

#### 通过 Gmail 发送消息

1. 点击代码节点右侧的 **+**。
2. 搜索 `gmail` 并将其添加到工作区。
3. 为 Gmail 节点输入凭据。有关详细说明，请参阅 [n8n 文档](https://docs.n8n.io/integrations/builtin/credentials/google/oauth-single-service/)。
4. 在**资源**列表中，选择 `Message`。
5. 在**操作**列表中，选择 `Send`。
6. 在**收件人**框中，输入你的电子邮件。
7. 在**主题**框中，输入 `Hacker News Briefing`。
8. 在**邮件类型**框中，选择 `HTML`。
9. 在**消息**框中，点击 `Expression` 并输入 `{{ $json["response"] }}`。

    > **注意：**
    >
    > 你必须将鼠标悬停在**消息**框上并选择 **Expression** 模式。

## 步骤 4：运行工作流

构建完工作流后，你可以点击**执行工作流**进行测试运行。

如果工作流按预期运行，你将收到 Hacker News 简报邮件。这些新闻内容将记录到你的 TiDB Cloud Serverless 集群中，因此你不必担心丢失它们。

现在你可以在**工作流**面板中激活此工作流。这个工作流将帮助你每天获取 Hacker News 的头版文章。

## TiDB Cloud 节点核心

### 支持的操作

TiDB Cloud 节点作为[常规节点](https://docs.n8n.io/workflows/nodes/#regular-nodes)运行，仅支持以下五种操作：

- **Create Serverless Cluster**：创建 TiDB Cloud Serverless 集群。
- **Execute SQL**：在 TiDB 中执行 SQL 语句。
- **Delete**：在 TiDB 中删除行。
- **Insert**：在 TiDB 中插入行。
- **Update**：在 TiDB 中更新行。

### 字段

要使用不同的操作，你需要填写不同的必填字段。以下显示了相应操作的字段说明。

<SimpleTab>
<div label="Create Serverless Cluster">

- **Credential for TiDB Cloud API**：仅支持 TiDB Cloud API 密钥。有关如何创建 API 密钥，请参阅[获取 TiDB Cloud API 密钥](#前提条件获取-tidb-cloud-api-密钥)。
- **Project**：TiDB Cloud 项目名称。
- **Operation**：此节点的操作。有关所有支持的操作，请参阅[支持的操作](#支持的操作)。
- **Cluster**：TiDB Cloud 集群名称。为你的新集群输入名称。
- **Region**：区域名称。选择将部署集群的区域。通常选择离应用程序部署最近的区域。
- **Password**：root 密码。为你的新集群设置密码。

</div>
<div label="Execute SQL">

- **Credential for TiDB Cloud API**：仅支持 TiDB Cloud API 密钥。有关如何创建 API 密钥，请参阅[获取 TiDB Cloud API 密钥](#前提条件获取-tidb-cloud-api-密钥)。
- **Project**：TiDB Cloud 项目名称。
- **Operation**：此节点的操作。有关所有支持的操作，请参阅[支持的操作](#支持的操作)。
- **Cluster**：TiDB Cloud 集群名称。你应该选择一个现有集群。
- **Password**：TiDB Cloud 集群的密码。
- **User**：TiDB Cloud 集群的用户名。
- **Database**：数据库名称。
- **SQL**：要执行的 SQL 语句。

</div>
<div label="Delete">

- **Credential for TiDB Cloud API**：仅支持 TiDB Cloud API 密钥。有关如何创建 API 密钥，请参阅[获取 TiDB Cloud API 密钥](#前提条件获取-tidb-cloud-api-密钥)。
- **Project**：TiDB Cloud 项目名称。
- **Operation**：此节点的操作。有关所有支持的操作，请参阅[支持的操作](#支持的操作)。
- **Cluster**：TiDB Cloud 集群名称。你应该选择一个现有集群。
- **Password**：TiDB Cloud 集群的密码。
- **User**：TiDB Cloud 集群的用户名。
- **Database**：数据库名称。
- **Table**：表名。你可以使用 `From list` 模式选择一个，或使用 `Name` 模式手动输入表名。
- **Delete Key**：决定数据库中哪些行被删除的项目属性名称。项目是从一个节点发送到另一个节点的数据。节点对传入数据的每个项目执行其操作。有关 n8n 中项目的更多信息，请参阅 [n8n 文档](https://docs.n8n.io/workflows/items/)。

</div>
<div label="Insert">

- **Credential for TiDB Cloud API**：仅支持 TiDB Cloud API 密钥。有关如何创建 API 密钥，请参阅[获取 TiDB Cloud API 密钥](#前提条件获取-tidb-cloud-api-密钥)。
- **Project**：TiDB Cloud 项目名称。
- **Operation**：此节点的操作。有关所有支持的操作，请参阅[支持的操作](#支持的操作)。
- **Cluster**：TiDB Cloud 集群名称。你应该选择一个现有集群。
- **Password**：TiDB Cloud 集群的密码。
- **User**：TiDB Cloud 集群的用户名。
- **Database**：数据库名称。
- **Table**：表名。你可以使用 `From list` 模式选择一个，或使用 `Name` 模式手动输入表名。
- **Columns**：用作新行列的输入项目属性的逗号分隔列表。项目是从一个节点发送到另一个节点的数据。节点对传入数据的每个项目执行其操作。有关 n8n 中项目的更多信息，请参阅 [n8n 文档](https://docs.n8n.io/workflows/items/)。

</div>
<div label="Update">

- **Credential for TiDB Cloud API**：仅支持 TiDB Cloud API 密钥。有关如何创建 API 密钥，请参阅[获取 TiDB Cloud API 密钥](#前提条件获取-tidb-cloud-api-密钥)。
- **Project**：TiDB Cloud 项目名称。
- **Operation**：此节点的操作。有关所有支持的操作，请参阅[支持的操作](#支持的操作)。
- **Cluster**：TiDB Cloud 集群名称。你应该选择一个现有集群。
- **Password**：TiDB Cloud 集群的密码。
- **User**：TiDB Cloud 集群的用户名。
- **Database**：数据库名称。
- **Table**：表名。你可以使用 `From list` 模式选择一个，或使用 `Name` 模式手动输入表名。
- **Update Key**：决定数据库中哪些行被更新的项目属性名称。项目是从一个节点发送到另一个节点的数据。节点对传入数据的每个项目执行其操作。有关 n8n 中项目的更多信息，请参阅 [n8n 文档](https://docs.n8n.io/workflows/items/)。
- **Columns**：用作要更新行的列的输入项目属性的逗号分隔列表。

</div>
</SimpleTab>

### 限制

- 通常在 **Execute SQL** 操作中只允许执行一条 SQL 语句。如果你想在单个操作中执行多条语句，需要手动启用 [`tidb_multi_statement_mode`](https://docs.pingcap.com/tidbcloud/system-variables#tidb_multi_statement_mode-new-in-v4011)。
- 对于 **Delete** 和 **Update** 操作，你需要指定一个字段作为键。例如，`Delete Key` 设置为 `id`，相当于执行 `DELETE FROM table WHERE id = ${item.id}`。目前，**Delete** 和 **Update** 操作仅支持指定一个键。
- 对于 **Insert** 和 **Update** 操作，你需要在 **Columns** 字段中指定逗号分隔的列表，并且字段名称必须与输入项目的属性相同。
