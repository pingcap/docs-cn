---
title: 身份访问管理
summary: 了解如何在 TiDB Cloud 中管理身份访问。
---

# 身份访问管理

本文档介绍如何在 TiDB Cloud 中管理组织、项目、角色和用户配置文件的访问权限。

在访问 TiDB Cloud 之前，请[创建 TiDB Cloud 账号](https://tidbcloud.com/free-trial)。你可以使用电子邮件和密码注册，这样就可以[使用 TiDB Cloud 管理密码](/tidb-cloud/tidb-cloud-password-authentication.md)，或者选择使用 Google、GitHub 或 Microsoft 账号进行单点登录（SSO）到 TiDB Cloud。

## 组织和项目

TiDB Cloud 基于组织和项目提供层级结构，以便于管理 TiDB Cloud 用户和集群。如果你是组织所有者，你可以在组织中创建多个项目。

例如：

```
- 你的组织
    - 项目 1
        - 集群 1
        - 集群 2
    - 项目 2
        - 集群 3
        - 集群 4
    - 项目 3
        - 集群 5
        - 集群 6
```

在此结构下：

- 要访问组织，用户必须是该组织的成员。
- 要访问组织中的项目，用户必须至少具有该组织中项目的读取权限。
- 要管理项目中的集群，用户必须具有 `Project Owner` 角色。

有关用户角色和权限的更多信息，请参见[用户角色](#用户角色)。

### 组织

一个组织可以包含多个项目。

TiDB Cloud 在组织级别计算账单，并提供每个项目的账单详情。

如果你是组织所有者，你拥有组织中的最高权限。

例如，你可以执行以下操作：

- 为不同目的创建不同的项目（如开发、暂存和生产）。
- 为不同用户分配不同的组织角色和项目角色。
- 配置组织设置。例如，为组织配置时区。

### 项目

一个项目可以包含多个集群。

如果你是项目所有者，你可以管理项目的集群和项目设置。

例如，你可以执行以下操作：

- 根据业务需求创建多个集群。
- 为不同用户分配不同的项目角色。
- 配置项目设置。例如，为不同项目配置不同的告警设置。

## 用户角色

TiDB Cloud 定义了不同的用户角色来管理组织、项目或两者中 TiDB Cloud 用户的不同权限。

你可以在组织级别或项目级别为用户授予角色。出于安全考虑，请仔细规划组织和项目的层级结构。

### 组织角色

在组织级别，TiDB Cloud 定义了四个角色，其中 `Organization Owner` 可以邀请成员并为成员授予组织角色。

| 权限  | `Organization Owner` | `Organization Billing Manager` | `Organization Billing Viewer` | `Organization Console Audit Manager` | `Organization Viewer` |
|---|---|---|---|---|---|
| 管理组织设置，如项目、API 密钥和时区。 | ✅ | ❌ | ❌ | ❌ | ❌ |
| 邀请用户加入组织或从组织中移除用户，并编辑用户的组织角色。 | ✅ | ❌ | ❌ | ❌ | ❌ |
| 组织中所有项目的所有 `Project Owner` 权限。 | ✅ | ❌ | ❌ | ❌ | ❌ |
| 创建启用客户管理加密密钥（CMEK）的项目。 | ✅ | ❌ | ❌ | ❌ | ❌ |
| 编辑组织的支付信息。 | ✅ | ✅ | ❌ | ❌ | ❌ |
| 查看账单并使用[成本分析器](/tidb-cloud/tidb-cloud-billing.md#cost-explorer)。 | ✅ | ✅ | ✅ | ❌ | ❌ |
| 管理组织的 TiDB Cloud [控制台审计日志](/tidb-cloud/tidb-cloud-console-auditing.md)。 | ✅ | ❌ | ❌ | ✅ | ❌ |
| 查看组织中的用户和成员所属的项目。 | ✅ | ✅ | ✅ | ✅ | ✅ |

> **注意：**
>
> - `Organization Console Audit Manager` 角色（从 `Organization Console Audit Admin` 重命名）用于管理 TiDB Cloud 控制台的审计日志，而不是数据库审计日志。要管理数据库审计，请使用项目级别的 `Project Owner` 角色。
> - `Organization Billing Manager` 角色从 `Organization Billing Admin` 重命名，`Organization Viewer` 角色从 `Organization Member` 重命名。

### 项目角色

在项目级别，TiDB Cloud 定义了三个角色，其中 `Project Owner` 可以邀请成员并为成员授予项目角色。

> **注意：**
>
> - `Organization Owner` 拥有所有项目的所有 <code>Project Owner</code> 权限，因此 `Organization Owner` 也可以邀请项目成员并为成员授予项目角色。
> - 每个项目角色默认拥有所有 <code>Organization Viewer</code> 权限。
> - 如果组织中的用户不属于任何项目，该用户没有任何项目权限。

| 权限  | `Project Owner` | `Project Data Access Read-Write` | `Project Data Access Read-Only` | `Project Viewer` |
|---|---|---|---|---|
| 管理项目设置 | ✅ | ❌ | ❌ | ❌ |
| 邀请用户加入项目或从项目中移除用户，并编辑用户的项目角色。 | ✅ | ❌ | ❌ | ❌ |
| 管理项目的[数据库审计日志](/tidb-cloud/tidb-cloud-auditing.md)。 | ✅ | ❌ | ❌ | ❌ |
| 管理项目中所有 TiDB Cloud Serverless 集群的[支出限制](/tidb-cloud/manage-serverless-spend-limit.md)。 | ✅ | ❌ | ❌ | ❌ |
| 管理项目中的集群操作，如集群创建、修改和删除。 | ✅ | ❌ | ❌ | ❌ |
| 管理项目中 TiDB Cloud Serverless 集群的分支，如分支创建、连接和删除。 | ✅ | ❌ | ❌ | ❌ |
| 管理项目中 TiDB Cloud Dedicated 集群的[恢复组](/tidb-cloud/recovery-group-overview.md)，如恢复组创建和删除。 | ✅ | ❌ | ❌ | ❌ |
| 管理集群数据，如数据导入、数据备份和恢复以及数据迁移。 | ✅ | ✅ | ❌ | ❌ |
| 管理[数据服务](/tidb-cloud/data-service-overview.md)的数据只读操作，如使用或创建端点读取数据。 | ✅ | ✅ | ✅ | ❌ |
| 管理[数据服务](/tidb-cloud/data-service-overview.md)的数据读写操作。 | ✅ | ✅ | ❌ | ❌ |
| 使用 [SQL 编辑器](/tidb-cloud/explore-data-with-chat2query.md)查看集群数据。 | ✅ | ✅ | ✅ | ❌ |
| 使用 [SQL 编辑器](/tidb-cloud/explore-data-with-chat2query.md)修改和删除集群数据。 | ✅ | ✅ | ❌ | ❌ |
| 管理[变更数据捕获](/tidb-cloud/changefeed-overview.md)。 | ✅ | ✅ | ✅ | ❌ |
| 查看和重置集群密码。 | ✅ | ❌ | ❌ | ❌ |
| 查看项目中的集群概览、备份记录、指标、事件和[变更数据捕获](/tidb-cloud/changefeed-overview.md)。 | ✅ | ✅ | ✅ | ✅ |

## 管理组织访问

### 查看和切换组织

要查看和切换组织，请执行以下步骤：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com)中，点击左上角的组合框。显示你所属的组织和项目列表。

    > **提示：**
    >
    > - 如果你当前在特定集群的页面上，点击左上角的组合框后，还需要点击组合框中的 ← 返回组织和项目列表。
    > - 如果你是多个组织的成员，可以在组合框中点击目标组织名称，在组织之间切换账号。

2. 要查看组织的详细信息（如组织 ID 和时区），请点击组织名称，然后在左侧导航栏中点击 **Organization Settings** > **General**。

### 设置组织时区

如果你具有 `Organization Owner` 角色，你可以根据时区修改系统显示时间。

要更改本地时区设置，请执行以下步骤：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com)中，使用左上角的组合框切换到目标组织。

2. 在左侧导航栏中，点击 **Organization Settings** > **General**。

3. 在 **Time Zone** 部分，从下拉列表中选择你的时区。

4. 点击 **Update**。

### 邀请组织成员

如果你具有 `Organization Owner` 角色，你可以邀请用户加入组织。

> **注意：**
>
> 你也可以根据需要直接[邀请用户加入项目](#邀请项目成员)，这样用户也会成为组织成员。

要邀请成员加入组织，请执行以下步骤：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com)中，使用左上角的组合框切换到目标组织。

2. 在左侧导航栏中，点击 **Organization Settings** > **Users**。

3. 在 **Users** 页面，点击 **By Organization** 标签页。

4. 点击 **Invite**。

5. 输入要邀请的用户的电子邮件地址，然后为该用户选择组织角色。

    > **提示：**
    >
    > - 如果你想一次邀请多个成员，可以输入多个电子邮件地址。
    > - 被邀请的用户默认不属于任何项目。要邀请用户加入项目，请参见[邀请项目成员](#邀请项目成员)。

6. 点击 **Confirm**。然后新用户成功添加到用户列表中。同时，系统会向被邀请的电子邮件地址发送一封包含验证链接的邮件。

7. 收到此邮件后，用户需要点击邮件中的链接验证身份，然后会显示一个新页面。

8. 如果被邀请的电子邮件地址尚未注册 TiDB Cloud 账号，用户将被引导到注册页面创建账号。如果该电子邮件地址已注册 TiDB Cloud 账号，用户将被引导到登录页面，登录后账号会自动加入组织。

> **注意：**
>
> 邮件中的验证链接将在 24 小时后过期。如果你要邀请的用户没有收到邮件，请点击 **Resend**。

### 修改组织角色

如果你具有 `Organization Owner` 角色，你可以修改组织中所有成员的组织角色。

要修改成员的组织角色，请执行以下步骤：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com)中，使用左上角的组合框切换到目标组织。

2. 在左侧导航栏中，点击 **Organization Settings** > **Users**。

3. 在 **Users** 页面，点击 **By Organization** 标签页。

4. 点击目标成员的角色，然后修改角色。

### 移除组织成员

如果你具有 `Organization Owner` 角色，你可以从组织中移除组织成员。

要从组织中移除成员，请执行以下步骤：

> **注意：**
>
> 如果成员从组织中移除，该成员也会从所属的项目中移除。

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com)中，使用左上角的组合框切换到目标组织。

2. 在左侧导航栏中，点击 **Organization Settings** > **Users**。

3. 在 **Users** 页面，点击 **By Organization** 标签页。

4. 在目标成员所在行，点击 **...** > **Delete**。

## 管理项目访问

### 查看和切换项目

要查看和切换项目，请执行以下步骤：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com)中，点击左上角的组合框。显示你所属的组织和项目列表。

    > **提示：**
    >
    > - 如果你当前在特定集群的页面上，点击左上角的组合框后，还需要点击组合框中的 ← 返回组织和项目列表。
    > - 如果你是多个项目的成员，可以在组合框中点击目标项目名称，在项目之间切换。

2. 要查看项目的详细信息，请点击项目名称，然后在左侧导航栏中点击 **Project Settings**。

### 创建项目

> **注意：**
>
> 对于免费试用用户，你不能创建新项目。

如果你具有 `Organization Owner` 角色，你可以在组织中创建项目。

要创建新项目，请执行以下步骤：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com)中，使用左上角的组合框切换到目标组织。

2. 在左侧导航栏中，点击 **Projects**。

3. 在 **Projects** 页面，点击 **Create New Project**。

4. 输入项目名称。

5. 点击 **Confirm**。

### 重命名项目

如果你具有 `Organization Owner` 角色，你可以重命名组织中的任何项目。如果你具有 `Project Owner` 角色，你可以重命名你的项目。

要重命名项目，请执行以下步骤：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com)中，使用左上角的组合框切换到目标组织。

2. 在左侧导航栏中，点击 **Projects**。

3. 在要重命名的项目所在行，点击 **...** > **Rename**。

4. 输入新的项目名称。

5. 点击 **Confirm**。

### 邀请项目成员

如果你具有 `Organization Owner` 或 `Project Owner` 角色，你可以邀请成员加入项目。

> **注意：**
>
> 当不在组织中的用户加入项目时，该用户也会自动加入组织。

要邀请成员加入项目，请执行以下步骤：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com)中，使用左上角的组合框切换到目标组织。

2. 在左侧导航栏中，点击 **Organization Settings** > **Users**。

3. 在 **Users** 页面，点击 **By Project** 标签页，然后在下拉列表中选择你的项目。

4. 点击 **Invite**。

5. 输入要邀请的用户的电子邮件地址，然后为该用户选择项目角色。

    > **提示：**
    >
    > 如果你想一次邀请多个成员，可以输入多个电子邮件地址。

6. 点击 **Confirm**。然后新用户成功添加到用户列表中。同时，系统会向被邀请的电子邮件地址发送一封包含验证链接的邮件。

7. 收到此邮件后，用户需要点击邮件中的链接验证身份，然后会显示一个新页面。

8. 如果被邀请的电子邮件地址尚未注册 TiDB Cloud 账号，用户将被引导到注册页面创建账号。如果该电子邮件地址已注册 TiDB Cloud 账号，用户将被引导到登录页面。登录后，账号会自动加入项目。

> **注意：**
>
> 邮件中的验证链接将在 24 小时后过期。如果你的用户没有收到邮件，请点击 **Resend**。

### 修改项目角色

如果你具有 `Organization Owner` 角色，你可以修改组织中所有项目成员的项目角色。如果你具有 `Project Owner` 角色，你可以修改项目中所有成员的项目角色。

要修改成员的项目角色，请执行以下步骤：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com)中，使用左上角的组合框切换到目标组织。

2. 在左侧导航栏中，点击 **Organization Settings** > **Users**。

3. 在 **Users** 页面，点击 **By Project** 标签页，然后在下拉列表中选择你的项目。

4. 在目标成员所在行，点击 **Role** 列中的角色，然后从下拉列表中选择新角色。

### 移除项目成员

如果你具有 `Organization Owner` 或 `Project Owner` 角色，你可以移除项目成员。

要从项目中移除成员，请执行以下步骤：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com)中，使用左上角的组合框切换到目标组织。

2. 在左侧导航栏中，点击 **Organization Settings** > **Users**。

3. 在 **Users** 页面，点击 **By Project** 标签页，然后在下拉列表中选择你的项目。

4. 在目标成员所在行，点击 **...** > **Delete**。

## 管理用户配置文件

在 TiDB Cloud 中，你可以轻松管理你的配置文件，包括名字、姓氏和电话号码。

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com)中，点击左下角的 <MDSvgIcon name="icon-top-account-settings" />。

2. 点击 **Account Settings**。

3. 在显示的对话框中，更新配置文件信息，然后点击 **Update**。
