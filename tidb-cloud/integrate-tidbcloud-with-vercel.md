---
title: 将 TiDB Cloud 与 Vercel 集成
summary: 了解如何将 TiDB Cloud 集群连接到 Vercel 项目。
---

<!-- markdownlint-disable MD029 -->

# 将 TiDB Cloud 与 Vercel 集成

[Vercel](https://vercel.com/) 是一个面向前端开发者的平台，为创新者提供灵感迸发时所需的速度和可靠性。

将 TiDB Cloud 与 Vercel 结合使用，可以让您使用 MySQL 兼容的关系模型更快地构建新的前端应用程序，并借助为弹性、可扩展性以及最高级别的数据隐私和安全性而构建的平台，让您的应用程序充满信心地成长。

本指南描述了如何使用以下方法之一将 TiDB Cloud 集群连接到 Vercel 项目：

* [通过 TiDB Cloud Vercel 集成连接](#通过-tidb-cloud-vercel-集成连接)
* [通过手动配置环境变量连接](#通过手动设置环境变量连接)

对于上述两种方法，TiDB Cloud 提供以下选项用于以编程方式连接到您的数据库：

- 集群：通过直接连接或[无服务器驱动](/tidb-cloud/serverless-driver.md)将您的 TiDB Cloud 集群连接到您的 Vercel 项目。
- [数据应用](/tidb-cloud/data-service-manage-data-app.md)：通过一组 HTTP 端点访问您的 TiDB Cloud 集群的数据。

## 前提条件

在连接之前，请确保满足以下前提条件。

### Vercel 账号和 Vercel 项目

您需要在 Vercel 中拥有一个账号和一个项目。如果您没有，请参考以下 Vercel 文档创建：

* [创建新的个人账号](https://vercel.com/docs/teams-and-accounts#creating-a-personal-account)或[创建新的团队](https://vercel.com/docs/teams-and-accounts/create-or-join-a-team#creating-a-team)。
* 在 Vercel 中[创建项目](https://vercel.com/docs/concepts/projects/overview#creating-a-project)，或者如果您没有要部署的应用程序，可以使用 [TiDB Cloud 入门模板](https://vercel.com/templates/next.js/tidb-cloud-starter)进行尝试。

一个 Vercel 项目只能连接到一个 TiDB Cloud 集群。要更改集成，您需要先断开当前集群的连接，然后再连接到新集群。

### TiDB Cloud 账号和 TiDB 集群

您需要在 TiDB Cloud 中拥有一个账号和一个集群。如果您没有，请参考以下内容创建：

- [创建 TiDB Cloud Serverless 集群](/tidb-cloud/create-tidb-cluster-serverless.md)

    > **注意：**
    >
    > TiDB Cloud Vercel 集成支持创建 TiDB Cloud Serverless 集群。您也可以在集成过程中稍后创建。

- [创建 TiDB Cloud Dedicated 集群](/tidb-cloud/create-tidb-cluster.md)

    > **注意：**
    >
    > 对于 TiDB Cloud Dedicated 集群，请确保集群的流量过滤器允许所有 IP 地址（设置为 `0.0.0.0/0`）进行连接，因为 Vercel 部署使用[动态 IP 地址](https://vercel.com/guides/how-to-allowlist-deployment-ip-address)。

要[通过 TiDB Cloud Vercel 集成进行集成](#通过-tidb-cloud-vercel-集成连接)，您需要在 TiDB Cloud 中拥有组织的`组织所有者`角色或目标项目的`项目所有者`角色。更多信息，请参阅[用户角色](/tidb-cloud/manage-user-access.md#user-roles)。

一个 TiDB Cloud 集群可以连接到多个 Vercel 项目。

### 数据应用和端点

如果您想通过[数据应用](/tidb-cloud/data-service-manage-data-app.md)连接到您的 TiDB Cloud 集群，您需要预先在 TiDB Cloud 中拥有目标数据应用和端点。如果您没有，请参考以下步骤创建：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com)中，转到项目的[**数据服务**](https://tidbcloud.com/project/data-service)页面。
2. 为您的项目[创建数据应用](/tidb-cloud/data-service-manage-data-app.md#create-a-data-app)。
3. [将数据应用链接](/tidb-cloud/data-service-manage-data-app.md#manage-linked-data-sources)到目标 TiDB Cloud 集群。
4. [管理端点](/tidb-cloud/data-service-manage-endpoint.md)，以便您可以自定义它们来执行 SQL 语句。

一个 Vercel 项目只能连接到一个 TiDB Cloud 数据应用。要更改 Vercel 项目的数据应用，您需要先断开当前应用的连接，然后再连接到新应用。

## 通过 TiDB Cloud Vercel 集成连接

要通过 TiDB Cloud Vercel 集成进行连接，请从 [Vercel 的集成市场](https://vercel.com/integrations)转到 [TiDB Cloud 集成](https://vercel.com/integrations/tidb-cloud)页面。使用此方法，您可以选择要连接的集群，TiDB Cloud 将自动为您的 Vercel 项目生成所有必要的环境变量。

> **注意：**
>
> 此方法仅适用于 TiDB Cloud Serverless 集群。如果您想连接到 TiDB Cloud Dedicated 集群，请使用[手动方法](#通过手动设置环境变量连接)。

### 集成工作流程

详细步骤如下：

<SimpleTab>
<div label="集群">

1. 在 [TiDB Cloud Vercel 集成](https://vercel.com/integrations/tidb-cloud)页面的右上角点击**添加集成**。将显示**添加 TiDB Cloud**对话框。
2. 在下拉列表中选择集成范围，然后点击**继续**。
3. 选择要添加集成的 Vercel 项目，然后点击**继续**。
4. 确认集成所需的权限，然后点击**添加集成**。然后您将被引导到 TiDB Cloud 控制台的集成页面。
5. 在集成页面上，执行以下操作：

    1. 选择您的目标 Vercel 项目，然后点击**下一步**。
    2. 选择您的目标 TiDB Cloud 组织和项目。
    3. 选择**集群**作为您的连接类型。
    4. 选择您的目标 TiDB Cloud 集群。如果**集群**下拉列表为空或您想选择新的 TiDB Cloud Serverless 集群，请在列表中点击**+ 创建集群**来创建一个。
    5. 选择您要连接的数据库。如果**数据库**下拉列表为空或您想选择新的数据库，请在列表中点击**+ 创建数据库**来创建一个。
    6. 选择您的 Vercel 项目使用的框架。如果目标框架未列出，请选择**通用**。不同的框架决定了不同的环境变量。
    7. 选择是否启用**分支**以为预览环境创建新分支。
    8. 点击**添加集成并返回 Vercel**。

![Vercel 集成页面](/media/tidb-cloud/vercel/integration-link-cluster-page.png)

6. 返回到您的 Vercel 仪表板，转到您的 Vercel 项目，点击**设置** > **环境变量**，检查是否已自动添加目标 TiDB 集群的环境变量。

    如果已添加以下变量，则集成完成。

    **通用**

    ```shell
    TIDB_HOST
    TIDB_PORT
    TIDB_USER
    TIDB_PASSWORD
    TIDB_DATABASE
    ```

    **Prisma**

    ```
    DATABASE_URL
    ```

    **TiDB Cloud 无服务器驱动**

    ```
    DATABASE_URL
    ```

</div>

<div label="数据应用">

1. 在 [TiDB Cloud Vercel 集成](https://vercel.com/integrations/tidb-cloud)页面的右上角点击**添加集成**。将显示**添加 TiDB Cloud**对话框。
2. 在下拉列表中选择集成范围，然后点击**继续**。
3. 选择要添加集成的 Vercel 项目，然后点击**继续**。
4. 确认集成所需的权限，然后点击**添加集成**。然后您将被引导到 TiDB Cloud 控制台的集成页面。
5. 在集成页面上，执行以下操作：

    1. 选择您的目标 Vercel 项目，然后点击**下一步**。
    2. 选择您的目标 TiDB Cloud 组织和项目。
    3. 选择**数据应用**作为您的连接类型。
    4. 选择您的目标 TiDB 数据应用。
    6. 点击**添加集成并返回 Vercel**。

![Vercel 集成页面](/media/tidb-cloud/vercel/integration-link-data-app-page.png)

6. 返回到您的 Vercel 仪表板，转到您的 Vercel 项目，点击**设置** > **环境变量**，检查是否已自动添加目标数据应用的环境变量。

    如果已添加以下变量，则集成完成。

    ```shell
    DATA_APP_BASE_URL
    DATA_APP_PUBLIC_KEY
    DATA_APP_PRIVATE_KEY
    ```

</div>
</SimpleTab>

### 配置连接

如果您已安装 [TiDB Cloud Vercel 集成](https://vercel.com/integrations/tidb-cloud)，您可以在集成内添加或删除连接。

1. 在您的 Vercel 仪表板中，点击**集成**。
2. 在 TiDB Cloud 条目中点击**管理**。
3. 点击**配置**。
4. 点击**添加链接**或**删除**以添加或删除连接。

    ![Vercel 集成配置页面](/media/tidb-cloud/vercel/integration-vercel-configuration-page.png)

    当您删除连接时，集成工作流程设置的环境变量也会从 Vercel 项目中删除。但是，此操作不会影响 TiDB Cloud Serverless 集群的数据。

### 使用 TiDB Cloud Serverless 分支连接

Vercel 的[预览部署](https://vercel.com/docs/deployments/preview-deployments)功能允许您在不将更改合并到 Git 项目的生产分支的情况下，在实时部署中预览应用程序的更改。使用 [TiDB Cloud Serverless 分支](/tidb-cloud/branch-overview.md)，您可以为 Vercel 项目的每个分支创建一个新实例。这允许您在实时部署中预览应用程序更改，而不会影响您的生产数据。

> **注意：**
>
> 目前，TiDB Cloud Serverless 分支仅支持[与 GitHub 仓库关联的 Vercel 项目](https://vercel.com/docs/deployments/git/vercel-for-github)。

要启用 TiDB Cloud Serverless 分支，您需要在 [TiDB Cloud Vercel 集成工作流程](#集成工作流程)中确保以下内容：

1. 选择**集群**作为您的连接类型。
2. 启用**分支**以为预览环境创建新分支。

在您将更改推送到 Git 仓库后，Vercel 将触发预览部署。TiDB Cloud 集成将自动为 Git 分支创建一个 TiDB Cloud Serverless 分支并设置环境变量。详细步骤如下：

1. 在您的 Git 仓库中创建一个新分支。

    ```shell
    cd tidb-prisma-vercel-demo1
    git checkout -b new-branch
    ```

2. 添加一些更改并将更改推送到远程仓库。
3. Vercel 将为新分支触发预览部署。

    ![Vercel 预览部署](/media/tidb-cloud/vercel/vercel-preview-deployment.png)

    1. 在部署过程中，TiDB Cloud 集成将自动创建一个与 Git 分支同名的 TiDB Cloud Serverless 分支。如果 TiDB Cloud Serverless 分支已存在，TiDB Cloud 集成将跳过此步骤。

        ![TiDB Cloud 分支检查](/media/tidb-cloud/vercel/tidbcloud-branch-check.png)

    2. TiDB Cloud Serverless 分支就绪后，TiDB Cloud 集成将在 Vercel 项目的预览部署中设置环境变量。

        ![预览环境变量](/media/tidb-cloud/vercel/preview-envs.png)

    3. TiDB Cloud 集成还将注册一个阻塞检查，以等待 TiDB Cloud Serverless 分支就绪。您可以手动重新运行检查。
4. 检查通过后，您可以访问预览部署以查看更改。

> **注意：**
>
> 由于 Vercel 部署工作流程的限制，无法确保在部署中设置环境变量。在这种情况下，您需要重新部署。

> **注意：**
>
> 对于 TiDB Cloud 中的每个组织，默认情况下最多可以创建五个 TiDB Cloud Serverless 分支。为避免超过限制，您可以删除不再需要的 TiDB Cloud Serverless 分支。更多信息，请参阅[管理 TiDB Cloud Serverless 分支](/tidb-cloud/branch-manage.md)。

## 通过手动设置环境变量连接

<SimpleTab>
<div label="集群">

1. 获取您的 TiDB 集群的连接信息。

    您可以从集群的连接对话框中获取连接信息。要打开对话框，请转到项目的[**集群**](https://tidbcloud.com/project/clusters)页面，点击目标集群的名称以进入其概览页面，然后点击右上角的**连接**。

2. 转到您的 Vercel 仪表板 > Vercel 项目 > **设置** > **环境变量**，然后根据您的 TiDB 集群的连接信息[声明每个环境变量值](https://vercel.com/docs/concepts/projects/environment-variables#declare-an-environment-variable)。

    ![Vercel 环境变量](/media/tidb-cloud/vercel/integration-vercel-environment-variables.png)

这里我们以 Prisma 应用程序为例。以下是 Prisma schema 文件中针对 TiDB Cloud Serverless 集群的数据源设置：

```
datasource db {
    provider = "mysql"
    url      = env("DATABASE_URL")
}
```

在 Vercel 中，您可以按如下方式声明环境变量：

- **Key** = `DATABASE_URL`
- **Value** = `mysql://<User>:<Password>@<Endpoint>:<Port>/<Database>?sslaccept=strict`

您可以在 TiDB Cloud 控制台中获取 `<User>`、`<Password>`、`<Endpoint>`、`<Port>` 和 `<Database>` 的信息。

</div>
<div label="数据应用">

1. 如果您尚未创建数据应用及其端点，请按照[管理数据应用](/tidb-cloud/data-service-manage-data-app.md)和[管理端点](/tidb-cloud/data-service-manage-endpoint.md)中的步骤进行操作。

2. 转到您的 Vercel 仪表板 > Vercel 项目 > **设置** > **环境变量**，然后根据您的数据应用的连接信息[声明每个环境变量值](https://vercel.com/docs/concepts/projects/environment-variables#declare-an-environment-variable)。

    ![Vercel 环境变量](/media/tidb-cloud/vercel/integration-vercel-environment-variables.png)

    在 Vercel 中，您可以按如下方式声明环境变量：

    - **Key** = `DATA_APP_BASE_URL`
    - **Value** = `<DATA_APP_BASE_URL>`
    - **Key** = `DATA_APP_PUBLIC_KEY`
    - **Value** = `<DATA_APP_PUBLIC_KEY>`
    - **Key** = `DATA_APP_PRIVATE_KEY`
    - **Value** = `<DATA_APP_PRIVATE_KEY>`

    您可以从 TiDB Cloud 控制台的[数据服务](https://tidbcloud.com/project/data-service)页面获取 `<DATA_APP_BASE_URL>`、`<DATA_APP_PUBLIC_KEY>` 和 `<DATA_APP_PRIVATE_KEY>` 的信息。

</div>
</SimpleTab>
