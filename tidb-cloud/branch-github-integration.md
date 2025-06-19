---
title: 集成 TiDB Cloud Serverless 分支功能（Beta）与 GitHub
summary: 了解如何将 TiDB Cloud Serverless 分支功能与 GitHub 集成。
---

# 集成 TiDB Cloud Serverless 分支功能（Beta）与 GitHub

> **注意：**
>
> 此集成基于 [TiDB Cloud Serverless 分支功能](/tidb-cloud/branch-overview.md)构建。在阅读本文档之前，请确保您已熟悉 TiDB Cloud Serverless 分支功能。

如果您使用 GitHub 进行应用程序开发，您可以将 TiDB Cloud Serverless 分支功能集成到 GitHub CI/CD 流程中，这样您就可以使用分支自动测试您的拉取请求，而不会影响生产数据库。

在集成过程中，系统会提示您安装 [TiDB Cloud Branching](https://github.com/apps/tidb-cloud-branching) GitHub 应用程序。该应用程序可以根据 GitHub 仓库中的拉取请求自动管理 TiDB Cloud Serverless 分支。例如，当您创建拉取请求时，应用程序会为您的 TiDB Cloud Serverless 集群创建相应的分支，您可以在其中独立开发新功能或修复错误，而不会影响生产数据库。

本文档涵盖以下主题：

1. 如何将 TiDB Cloud Serverless 分支功能与 GitHub 集成
2. TiDB Cloud Branching 应用程序的工作原理
3. 如何构建基于分支的 CI 工作流，使用分支而不是生产集群来测试每个拉取请求

## 开始之前

在进行集成之前，请确保您具备以下条件：

- GitHub 账号
- 用于您应用程序的 GitHub 仓库
- [TiDB Cloud Serverless 集群](/tidb-cloud/create-tidb-cluster-serverless.md)

## 将 TiDB Cloud Serverless 分支功能与 GitHub 仓库集成

要将 TiDB Cloud Serverless 分支功能与 GitHub 仓库集成，请按照以下步骤操作：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com/)中，导航到项目的[**集群**](https://tidbcloud.com/project/clusters)页面，然后点击目标 TiDB Cloud Serverless 集群的名称以进入其概览页面。

2. 在左侧导航栏中点击**分支**。

3. 在**分支**页面的右上角，点击**连接到 GitHub**。

    - 如果您尚未登录 GitHub，系统会要求您先登录 GitHub。
    - 如果这是您第一次使用此集成，系统会要求您授权 **TiDB Cloud Branching** 应用程序。

   <img src="https://docs-download.pingcap.com/media/images/docs/tidb-cloud/branch/github-authorize.png" width="80%" />

4. 在**连接到 GitHub**对话框中，从**GitHub 账号**下拉列表中选择一个 GitHub 账号。

    如果列表中没有您的账号，请点击**安装其他账号**，然后按照屏幕上的说明安装账号。

5. 从**GitHub 仓库**下拉列表中选择您的目标仓库。如果列表较长，您可以通过输入名称来搜索仓库。

6. 点击**连接**以建立 TiDB Cloud Serverless 集群与 GitHub 仓库之间的连接。

   <img src="https://docs-download.pingcap.com/media/images/docs/tidb-cloud/branch/github-connect.png" width="40%" />

## TiDB Cloud Branching 应用程序行为

将 TiDB Cloud Serverless 集群连接到 GitHub 仓库后，[TiDB Cloud Branching](https://github.com/apps/tidb-cloud-branching) GitHub 应用程序可以自动管理该仓库中每个拉取请求对应的 TiDB Cloud Serverless 分支。以下列出了拉取请求变更的默认行为：

| 拉取请求变更 | TiDB Cloud Branching 应用程序行为 |
|------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 创建拉取请求 | 当您在仓库中创建拉取请求时，[TiDB Cloud Branching](https://github.com/apps/tidb-cloud-branching) 应用程序会为您的 TiDB Cloud Serverless 集群创建一个分支。当 `branch.mode` 设置为 `reset` 时，分支名称遵循 `${github_branch_name}_${pr_id}` 格式。当 `branch.mode` 设置为 `reserve` 时，分支名称遵循 `${github_branch_name}_${pr_id}_${commit_sha}` 格式。请注意，分支数量有[限制](/tidb-cloud/branch-overview.md#limitations-and-quotas)。 |
| 向拉取请求推送新提交 | 当 `branch.mode` 设置为 `reset` 时，每次您向仓库的拉取请求推送新提交时，[TiDB Cloud Branching](https://github.com/apps/tidb-cloud-branching) 应用程序都会重置 TiDB Cloud Serverless 分支。当 `branch.mode` 设置为 `reserve` 时，应用程序会为最新提交创建一个新分支。 |
| 关闭或合并拉取请求 | 当您关闭或合并拉取请求时，[TiDB Cloud Branching](https://github.com/apps/tidb-cloud-branching) 应用程序会删除该拉取请求的分支。 |
| 重新打开拉取请求 | 当您重新打开拉取请求时，[TiDB Cloud Branching](https://github.com/apps/tidb-cloud-branching) 应用程序会为该拉取请求的最新提交创建一个分支。 |

## 配置 TiDB Cloud Branching 应用程序

要配置 [TiDB Cloud Branching](https://github.com/apps/tidb-cloud-branching) 应用程序的行为，您可以在仓库的根目录中添加一个 `tidbcloud.yml` 文件，然后根据以下说明将所需的配置添加到该文件中。

### branch.blockList

**类型：** 字符串数组。**默认值：** `[]`。

指定禁止 TiDB Cloud Branching 应用程序使用的 GitHub 分支，即使它们在 `allowList` 中。

```yaml
github:
    branch:
        blockList:
            - ".*_doc"
            - ".*_blackList"
```

### branch.allowList

**类型：** 字符串数组。**默认值：** `[.*]`。

指定允许 TiDB Cloud Branching 应用程序使用的 GitHub 分支。

```yaml
github:
    branch:
        allowList:
            - ".*_db"
```

### branch.mode

**类型：** 字符串。**默认值：** `reset`。

指定 TiDB Cloud Branching 应用程序如何处理分支更新：

- 如果设置为 `reset`，TiDB Cloud Branching 应用程序将使用最新数据更新现有分支。
- 如果设置为 `reserve`，TiDB Cloud Branching 应用程序将为您的最新提交创建一个新分支。

```yaml
github:
    branch:
        mode: reset
```

### branch.autoDestroy

**类型：** 布尔值。**默认值：** `true`。

如果设置为 `false`，当拉取请求被关闭或合并时，TiDB Cloud Branching 应用程序将不会删除 TiDB Cloud Serverless 分支。

```yaml
github:
    branch:
        autoDestroy: true
```

## 创建分支 CI 工作流

使用分支的最佳实践之一是创建分支 CI 工作流。通过该工作流，您可以在合并拉取请求之前使用 TiDB Cloud Serverless 分支而不是生产集群来测试您的代码。您可以在[这里](https://github.com/shiyuhang0/tidbcloud-branch-gorm-example)找到一个实际示例。

以下是创建工作流的主要步骤：

1. [将 TiDB Cloud Serverless 分支功能与您的 GitHub 仓库集成](#将-tidb-cloud-serverless-分支功能与-github-仓库集成)。

2. 获取分支连接信息。

   您可以使用 [wait-for-tidbcloud-branch](https://github.com/tidbcloud/wait-for-tidbcloud-branch) action 来等待 TiDB Cloud Serverless 分支就绪并获取分支的连接信息。

    示例用法：

   ```yaml
   steps:
     - name: Wait for TiDB Cloud Serverless branch to be ready
       uses: tidbcloud/wait-for-tidbcloud-branch@v0
       id: wait-for-branch
       with:
         token: ${{ secrets.GITHUB_TOKEN }}
         public-key: ${{ secrets.TIDB_CLOUD_API_PUBLIC_KEY }}
         private-key: ${{ secrets.TIDB_CLOUD_API_PRIVATE_KEY }}

     - name: Test with TiDB Cloud Serverless branch
        run: |
           echo "The host is ${{ steps.wait-for-branch.outputs.host }}"
           echo "The user is ${{ steps.wait-for-branch.outputs.user }}"
           echo "The password is ${{ steps.wait-for-branch.outputs.password }}"
   ```
   
   - `token`：GitHub 会自动创建一个 [GITHUB_TOKEN](https://docs.github.com/en/actions/security-guides/automatic-token-authentication) 密钥。您可以直接使用它。
   - `public-key` 和 `private-key`：TiDB Cloud [API 密钥](https://docs.pingcap.com/tidbcloud/api/v1beta#section/Authentication/API-Key-Management)。

3. 修改您的测试代码。

   修改您的测试代码以接受来自 GitHub Actions 的连接信息。例如，您可以通过环境变量接受连接信息，如[实际示例](https://github.com/shiyuhang0/tidbcloud-branch-gorm-example)所示。

## 下一步

通过以下示例了解如何使用分支 GitHub 集成：

- [branching-gorm-example](https://github.com/tidbcloud/branching-gorm-example)
- [branching-django-example](https://github.com/tidbcloud/branching-django-example)
- [branching-rails-example](https://github.com/tidbcloud/branching-rails-example)

您也可以在不使用分支 GitHub 集成的情况下构建分支 CI/CD 工作流。例如，您可以使用 [`setup-tidbcloud-cli`](https://github.com/tidbcloud/setup-tidbcloud-cli) 和 GitHub Actions 来自定义您的 CI/CD 工作流。
