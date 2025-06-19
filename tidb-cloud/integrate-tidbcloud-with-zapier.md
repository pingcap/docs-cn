---
title: 将 TiDB Cloud 与 Zapier 集成
summary: 了解如何通过 Zapier 将 TiDB Cloud 连接到 5000+ 个应用。
---

# 将 TiDB Cloud 与 Zapier 集成

[Zapier](https://zapier.com) 是一个无代码自动化工具，可让你轻松创建涉及数千个应用和服务的工作流。

使用 Zapier 上的 [TiDB Cloud 应用](https://zapier.com/apps/tidb-cloud/integrations)可以让你：

- 使用 TiDB，一个兼容 MySQL 的 HTAP 数据库。无需本地构建。
- 更轻松地管理你的 TiDB Cloud。
- 将 TiDB Cloud 连接到 5000+ 个应用并自动化你的工作流。

本指南对 Zapier 上的 TiDB Cloud 应用进行高级介绍，并提供一个使用示例。

## 使用模板快速开始

[Zap 模板](https://platform.zapier.com/partners/zap-templates)是预制的集成或 Zap，已预先选择了应用和核心字段，适用于公开可用的 Zapier 集成。

在本节中，我们将使用**将新的 Github 全局事件添加到 TiDB 行**模板作为示例来创建工作流。在此工作流中，每当你的 GitHub 账户创建新的全局事件（在任何仓库中发生的任何 [GitHub 事件](https://docs.github.com/en/developers/webhooks-and-events/events/github-event-types)）时，Zapier 都会在你的 TiDB Cloud 集群中添加一个新行。

### 前提条件

在开始之前，你需要：

- 一个 [Zapier 账户](https://zapier.com/app/login)。
- 一个 [GitHub 账户](https://github.com/login)。
- 一个 [TiDB Cloud 账户](https://tidbcloud.com/signup)和 TiDB Cloud 上的 TiDB Cloud Serverless 集群。更多详情，请参阅 [TiDB Cloud 快速入门](https://docs.pingcap.com/tidbcloud/tidb-cloud-quickstart#step-1-create-a-tidb-cluster)。

### 步骤 1：获取模板

转到 [Zapier 上的 TiDB Cloud 应用](https://zapier.com/apps/tidb-cloud/integrations)。选择**将新的 Github 全局事件添加到 TiDB 行**模板，然后点击**试用**。之后你将进入编辑器页面。

### 步骤 2：设置触发器

在编辑器页面，你可以看到触发器和操作。点击触发器进行设置。

1. 选择应用和事件

    模板已默认设置了应用和事件，因此你无需在此处进行任何操作。点击**继续**。

2. 选择账户

    选择你想要与 TiDB Cloud 连接的 GitHub 账户。你可以连接新账户或选择现有账户。设置完成后，点击**继续**。

3. 设置触发器

    模板已默认设置了触发器。点击**继续**。

4. 测试触发器

    点击**测试触发器**。如果触发器设置成功，你可以看到来自 GitHub 账户的新全局事件数据。点击**继续**。

### 步骤 3：设置 `在 TiDB Cloud 中查找表` 操作

1. 选择应用和事件

    保持模板设置的默认值 `查找表`。点击**继续**。

2. 选择账户

    1. 点击**登录**按钮，你将被重定向到新的登录页面。
    2. 在登录页面，填写你的公钥和私钥。要获取 TiDB Cloud API 密钥，请按照 [TiDB Cloud API 文档](https://docs.pingcap.com/tidbcloud/api/v1beta#section/Authentication/API-Key-Management)中的说明操作。
    3. 点击**继续**。

    ![账户](/media/tidb-cloud/zapier/zapier-tidbcloud-account.png)

3. 设置操作

    在此步骤中，你需要指定 TiDB Cloud 集群中的一个表来存储事件数据。如果你还没有表，可以通过此步骤创建一个。

    1. 从下拉列表中选择项目名称和集群名称。你的集群的连接信息将自动显示。

        ![设置项目名称和集群名称](/media/tidb-cloud/zapier/zapier-set-up-tidbcloud-project-and-cluster.png)

    2. 输入你的密码。

    3. 从下拉列表中选择数据库。

        ![设置数据库名称](/media/tidb-cloud/zapier/zapier-set-up-tidbcloud-databse.png)

        Zapier 使用你输入的密码从 TiDB Cloud 查询数据库。如果在你的集群中找不到数据库，请重新输入密码并刷新页面。

    4. 在**你想要搜索的表**框中，填入 `github_global_event`。如果表不存在，模板将使用以下 DDL 创建表。点击**继续**。

        ![创建表 DDL](/media/tidb-cloud/zapier/zapier-tidbcloud-create-table-ddl.png)

4. 测试操作

    点击**测试操作**，Zapier 将创建表。你也可以跳过测试，表将在此工作流首次运行时创建。

### 步骤 4：设置 `在 TiDB Cloud 中创建行` 操作

1. 选择应用和事件

    保持模板设置的默认值。点击**继续**。

2. 选择账户

    选择你在设置 `在 TiDB Cloud 中查找表` 操作时选择的账户。点击**继续**。

    ![选择账户](/media/tidb-cloud/zapier/zapier-tidbcloud-choose-account.png)

3. 设置操作

    1. 按照前面的步骤填写**项目名称**、**集群名称**、**TiDB 密码**和**数据库名称**。

    2. 在**表名**中，从下拉列表中选择 **github_global_event** 表。表的列将显示出来。

        ![表列](/media/tidb-cloud/zapier/zapier-set-up-tidbcloud-columns.png)

    3. 在**列**框中，从触发器中选择相应的数据。填写所有列，然后点击**继续**。

        ![填写列](/media/tidb-cloud/zapier/zapier-fill-in-tidbcloud-triggers-data.png)

4. 测试操作

    点击**测试操作**在表中创建新行。如果你检查你的 TiDB Cloud 集群，你可以发现数据已成功写入。

   ```sql
   mysql> SELECT * FROM test.github_global_event;
   +-------------+-------------+------------+-----------------+----------------------------------------------+--------+---------------------+
   | id          | type        | actor      | repo_name       | repo_url                                     | public | created_at          |
   +-------------+-------------+------------+-----------------+----------------------------------------------+--------+---------------------+
   | 25324462424 | CreateEvent | shiyuhang0 | shiyuhang0/docs | https://api.github.com/repos/shiyuhang0/docs | True   | 2022-11-18 08:03:14 |
   +-------------+-------------+------------+-----------------+----------------------------------------------+--------+---------------------+
   1 row in set (0.17 sec)
   ```

### 步骤 5：发布你的 zap

点击**发布**来发布你的 zap。你可以在[主页](https://zapier.com/app/zaps)上看到 zap 正在运行。

![发布 zap](/media/tidb-cloud/zapier/zapier-tidbcloud-publish.png)

现在，这个 zap 将自动将你的 GitHub 账户的所有全局事件记录到 TiDB Cloud 中。

## 触发器和操作

[触发器和操作](https://zapier.com/how-it-works)是 Zapier 中的关键概念。通过组合不同的触发器和操作，你可以创建各种自动化工作流。

本节介绍 Zapier 上的 TiDB Cloud 应用提供的触发器和操作。

### 触发器

下表列出了 TiDB Cloud 应用支持的触发器。

| 触发器                | 描述                                                                 |
| ---------------------- |-----------------------------------------------------------------------------|
| 新集群            | 在创建新集群时触发。                                     |
| 新表              | 在创建新表时触发。                                       |
| 新行                | 在创建新行时触发。仅获取最近的 10000 个新行。 |
| 新行（自定义查询） | 在你提供的自定义查询返回新行时触发。   |

### 操作

下表列出了 TiDB Cloud 应用支持的操作。注意，某些操作需要额外的资源，你需要在使用操作之前准备相应的资源。

| 操作 | 描述 | 资源 |
|---|---|---|
| 查找集群 | 查找现有的 TiDB Cloud Serverless 或 TiDB Cloud Dedicated 集群。 | 无 |
| 创建集群 | 创建新集群。仅支持创建 TiDB Cloud Serverless 集群。 | 无 |
| 查找数据库 | 查找现有数据库。 | TiDB Cloud Serverless 集群 |
| 创建数据库 | 创建新数据库。 | TiDB Cloud Serverless 集群 |
| 查找表 | 查找现有表。 | TiDB Cloud Serverless 集群和数据库 |
| 创建表 | 创建新表。 | TiDB Cloud Serverless 集群和数据库 |
| 创建行 | 创建新行。 | TiDB Cloud Serverless 集群、数据库和表 |
| 更新行 | 更新现有行。 | TiDB Cloud Serverless 集群、数据库和表 |
| 查找行 | 通过查找列在表中查找行。 | TiDB Cloud Serverless 集群、数据库和表 |
| 查找行（自定义查询） | 通过你提供的自定义查询在表中查找行。 | TiDB Cloud Serverless 集群、数据库和表 |

## TiDB Cloud 应用模板

TiDB Cloud 在 Zapier 上提供了一些可直接使用的模板。你可以在 [TiDB Cloud 应用](https://zapier.com/apps/tidb-cloud/integrations)页面找到所有模板。

以下是一些示例：

- [在 Google Sheets 中复制新的 TiDB Cloud 行](https://zapier.com/apps/google-sheets/integrations/tidb-cloud/1134881/duplicate-new-tidb-cloud-rows-in-google-sheets)
- [从新的自定义 TiDB 查询通过 Gmail 发送邮件](https://zapier.com/apps/gmail/integrations/tidb-cloud/1134903/send-emails-via-gmail-from-new-custom-tidb-queries)
- [从新捕获的 webhook 向 TiDB Cloud 添加行](https://zapier.com/apps/tidb-cloud/integrations/webhook/1134955/add-rows-to-tidb-cloud-from-newly-caught-webhooks)
- [将新的 Salesforce 联系人存储在 TiDB 行中](https://zapier.com/apps/salesforce/integrations/tidb-cloud/1134923/store-new-salesforce-contacts-on-tidb-rows)
- [为带有简历的新 Gmail 邮件创建 TiDB 行并发送直接 Slack 通知](https://zapier.com/apps/gmail/integrations/slack/1135456/create-tidb-rows-for-new-gmail-emails-with-resumes-and-send-direct-slack-notifications)

## 常见问题

### 如何在 Zapier 中设置 TiDB Cloud 账户？

Zapier 需要你的 **TiDB Cloud API 密钥**来连接你的 TiDB Cloud 账户。Zapier 不需要你的 TiDB Cloud 登录账户。

要获取你的 TiDB Cloud API 密钥，请按照 [TiDB Cloud API 文档](https://docs.pingcap.com/tidbcloud/api/v1beta#section/Authentication/API-Key-Management)操作。

### TiDB Cloud 触发器如何执行去重？

Zapier 触发器可以通过轮询 API 调用定期检查新数据（间隔取决于你的 Zapier 计划）。

TiDB Cloud 触发器提供了一个返回大量结果的轮询 API 调用。然而，大多数结果都已被 Zapier 见过，也就是说，大多数结果都是重复的。

由于我们不希望在 API 中的项目在多个不同的轮询中存在时多次触发操作，TiDB Cloud 触发器使用 `id` 字段对数据进行去重。

`新集群`和`新表`触发器只是简单地使用 `cluster_id` 或 `table_id` 作为 `id` 字段来进行去重。你无需为这两个触发器做任何事情。

**新行触发器**

`新行`触发器在每次获取时限制 10,000 个结果。因此，如果某些新行不包含在这 10,000 个结果中，它们就无法触发 Zapier。

避免这种情况的一种方法是在触发器中指定 `Order By` 配置。例如，一旦你按创建时间对行进行排序，新行将始终包含在 10,000 个结果中。

`新行`触发器还使用灵活的策略生成 `id` 字段来进行去重。触发器按以下顺序生成 `id` 字段：

1. 如果结果包含 `id` 列，使用 `id` 列。
2. 如果你在触发器配置中指定了 `去重键`，使用 `去重键`。
3. 如果表有主键，使用主键。如果有多个主键，使用第一列。
4. 如果表有唯一键，使用唯一键。
5. 使用表的第一列。

**新行（自定义查询）触发器**

`新行（自定义查询）`触发器在每次获取时限制 1,000,000 个结果。1,000,000 是一个很大的数字，设置它只是为了保护整个系统。建议你的查询包含 `ORDER BY` 和 `LIMIT`。

要执行去重，你的查询结果必须有一个唯一的 id 字段。否则，你将收到 `你必须返回带有 id 字段的结果` 错误。

确保你的自定义查询在 30 秒内执行完成。否则，你将收到超时错误。

### 如何使用 `查找或创建` 操作？

`查找或创建`操作使你能够在资源不存在时创建它。以下是一个示例：

1. 选择 `查找表` 操作

2. 在`设置操作`步骤中，勾选 `如果表不存在则创建 TiDB Cloud 表？` 框以启用 `查找并创建`。

   ![查找并创建](/media/tidb-cloud/zapier/zapier-tidbcloud-find-and-create.png)

此工作流将在表不存在时创建表。注意，如果你测试你的操作，表将直接创建。
