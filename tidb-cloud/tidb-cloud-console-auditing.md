---
title: 控制台审计日志
summary: 了解 TiDB Cloud 控制台的审计日志功能。
---

# 控制台审计日志

TiDB Cloud 提供控制台审计日志功能，帮助您跟踪用户在 [TiDB Cloud 控制台](https://tidbcloud.com)上的各种行为和操作。例如，您可以跟踪邀请用户加入组织和创建集群等操作。

## 前提条件

- 您必须在 TiDB Cloud 中担任组织的 `Organization Owner` 或 `Organization Console Audit Manager` 角色。否则，您将无法在 TiDB Cloud 控制台中看到控制台审计日志相关选项。
- 您只能为您的组织启用和禁用控制台审计日志。您只能跟踪组织中用户的操作。
- 启用控制台审计日志后，将审计 TiDB Cloud 控制台的所有事件类型，您无法指定仅审计其中的某些事件。

## 启用控制台审计日志

控制台审计日志功能默认是禁用的。要启用它，请执行以下步骤：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com)中，使用左上角的组合框切换到目标组织。
2. 在左侧导航栏中，点击**控制台审计日志**。
3. 点击右上角的**设置**，启用控制台审计日志，然后点击**更新**。

## 禁用控制台审计日志

要禁用控制台审计日志，请执行以下步骤：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com)中，使用左上角的组合框切换到目标组织。
2. 在左侧导航栏中，点击**控制台审计日志**。
3. 点击右上角的**设置**，禁用控制台审计日志，然后点击**更新**。

## 查看控制台审计日志

您只能查看组织的控制台审计日志。

> **注意：**
>
> - 如果您的组织首次启用控制台审计日志，控制台审计日志将为空。执行任何被审计的事件后，您将看到相应的日志。
> - 如果控制台审计日志被禁用超过 90 天，您将无法看到任何日志。

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com)中，使用左上角的组合框切换到目标组织。
2. 在左侧导航栏中，点击**控制台审计日志**。
3. 要获取特定部分的审计日志，您可以过滤事件类型、操作状态和时间范围。
4. （可选）要过滤更多字段，点击**高级过滤器**，添加更多过滤条件，然后点击**应用**。
5. 点击日志行以在右侧窗格中查看其详细信息。

## 导出控制台审计日志

要导出组织的控制台审计日志，请执行以下步骤：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com)中，使用左上角的组合框切换到目标组织。
2. 在左侧导航栏中，点击**控制台审计日志**。
3. （可选）如果您需要导出特定部分的控制台审计日志，可以通过各种条件进行过滤。否则，跳过此步骤。
4. 点击**下载日志**，并选择所需的导出格式（JSON 或 CSV）。

## 控制台审计日志存储策略

控制台审计日志的存储时间为 90 天，之后日志将自动清理。

> **注意：**
>
> - 您无法在 TiDB Cloud 中指定控制台审计日志的存储位置。
> - 您无法手动删除审计日志。

## 控制台审计事件类型

控制台审计日志通过事件类型记录 TiDB Cloud 控制台上的各种用户活动。

> **注意：**
>
> 目前，TiDB Cloud 控制台上的大多数事件类型都可以被审计，您可以在下表中找到它们。对于尚未覆盖的其余事件类型，TiDB Cloud 将持续努力将它们也包含在内。

| 控制台审计事件类型           | 描述                                                                      |
|--------------------------------|----------------------------------------------------------------------------------|
| CreateOrganization             | 创建组织                                                           |
| LoginOrganization              | 登录组织                                                        |
| SwitchOrganization             | 从当前组织切换到另一个组织                     |
| LogoutOrganization             | 从组织注销                                                     |
| InviteUserToOrganization       | 邀请用户加入组织                                           |
| DeleteInvitationToOrganization | 删除用户加入组织的邀请                              |
| ResendInvitationToOrganization | 重新发送用户加入组织的邀请                         |
| ConfirmJoinOrganization        | 被邀请的用户确认加入组织                               |
| DeleteUserFromOrganization     | 从组织中删除已加入的用户                                       |
| UpdateUserRoleInOrganization   | 更新用户在组织中的角色                                    |
| CreateAPIKey                   | 创建 API 密钥                                                                |
| EditAPIKey                     | 编辑 API 密钥                                                                |
| DeleteAPIKey                   | 删除 API 密钥                                                                |
| UpdateTimezone                 | 更新组织的时区                                        |
| ShowBill                       | 显示组织账单                                                        |
| DownloadBill                   | 下载组织账单                                                       |
| ShowCredits                    | 显示组织积分                                                        |
| AddPaymentCard                 | 添加支付卡                                                               |
| UpdatePaymentCard              | 更新支付卡                                                            |
| DeletePaymentCard              | 删除支付卡                                                            |
| SetDefaultPaymentCard          | 设置默认支付卡                                                       |
| EditBillingProfile             | 编辑账单资料信息                                                 |
| ContractAction                 | 组织合同相关活动                                             |
| EnableConsoleAuditLog          | 启用控制台审计日志                                                     |
| ShowConsoleAuditLog            | 显示控制台审计日志                                                          |
| InviteUserToProject            | 邀请用户加入项目                                                  |
| DeleteInvitationToProject      | 删除用户加入项目的邀请                                   |
| ResendInvitationToProject      | 重新发送用户加入项目的邀请                              |
| ConfirmJoinProject             | 被邀请的用户确认加入项目                                    |
| DeleteUserFromProject          | 从项目中删除已加入的用户                                            |
| CreateProject                  | 创建项目                                                                 |
| CreateProjectCIDR              | 创建新的项目 CIDR                                                        |
| CreateAWSVPCPeering            | 创建 AWS VPC 对等连接                                                        |
| DeleteAWSVPCPeering            | 删除 AWS VPC 对等连接                                                        |
| CreateGCPVPCPeering            | 创建 Google Cloud VPC 对等连接                                                         |
| DeleteGCPVPCPeering            | 删除 Google Cloud VPC 对等连接                                                         |
| CreatePrivateEndpointService   | 创建私有端点服务                                                  |
| DeletePrivateEndpointService   | 删除私有端点服务                                                  |
| CreateAWSPrivateEndPoint       | 创建 AWS 私有端点                                                   |
| DeleteAWSPrivateEndPoint       | 删除 AWS 私有端点                                                      |
| SubscribeAlerts                | 订阅警报                                                                 |
| UnsubscribeAlerts              | 取消订阅警报                                                               |
| CreateDatadogIntegration       | 创建 Datadog 集成                                                       |
| DeleteDatadogIntegration       | 删除 Datadog 集成                                                       |
| CreateVercelIntegration        | 创建 Vercel 集成                                                        |
| DeleteVercelIntegration        | 删除 Vercel 集成                                                        |
| CreatePrometheusIntegration    | 创建 Prometheus 集成                                                    |
| DeletePrometheusIntegration    | 删除 Prometheus 集成                                                    |
| CreateCluster                  | 创建集群                                                                 |
| DeleteCluster                  | 删除集群                                                                 |
| PauseCluster                   | 暂停集群                                                                  |
| ResumeCluster                  | 恢复集群                                                                 |
| ScaleCluster                   | 扩展集群                                                                  |
| DownloadTiDBClusterCA          | 下载 CA 证书                                             |
| OpenWebSQLConsole              | 通过 Web SQL 连接到 TiDB 集群                                        |
| SetRootPassword                | 设置 TiDB 集群的 root 密码                                          |
| UpdateIPAccessList             | 更新 TiDB 集群的 IP 访问列表                                      |
| SetAutoBackup                  | 设置 TiDB 集群的自动备份机制                             |
| DoManualBackup                 | 执行 TiDB 集群的手动备份                                          |
| DeleteBackupTask               | 删除备份任务                                                             |
| DeleteBackup                   | 删除备份文件                                                             |
| RestoreFromBackup              | 基于备份文件恢复到 TiDB 集群                              |
| RestoreFromTrash              | 基于回收站中的备份文件恢复到 TiDB 集群                 |
| ImportDataFromAWS              | 从 AWS 导入数据                                                             |
| ImportDataFromGCP              | 从 Google Cloud 导入数据                                                             |
| ImportDataFromLocal            | 从本地磁盘导入数据                                                     |
| CreateMigrationJob             | 创建迁移任务                                                           |
| SuspendMigrationJob            | 暂停迁移任务                                                          |
| ResumeMigrationJob             | 恢复迁移任务                                                           |
| DeleteMigrationJob             | 删除迁移任务                                                           |
| ShowDiagnose                   | 显示诊断信息                                                       |
| DBAuditLogAction               | 设置数据库审计日志活动                                       |
| AddDBAuditFilter               | 添加数据库审计日志过滤器                                                  |
| DeleteDBAuditFilter            | 删除数据库审计日志过滤器                                               |
| EditProject                    | 编辑项目信息                                                |
| DeleteProject                  | 删除项目                                                                 |
| BindSupportPlan                | 绑定支持计划                                                              |
| CancelSupportPlan              | 取消支持计划                                                            |
| UpdateOrganizationName         | 更新组织名称                                                     |
| SetSpendLimit                  | 编辑 TiDB Cloud Serverless 可扩展集群的支出限制                    |
| UpdateMaintenanceWindow        | 修改维护窗口开始时间                                             |
| DeferMaintenanceTask           | 推迟维护任务                                                         |
| CreateBranch                   | 创建 TiDB Cloud Serverless 分支                                                  |
| DeleteBranch                   | 删除 TiDB Cloud Serverless 分支                                                  |
| SetBranchRootPassword          | 为 TiDB Cloud Serverless 分支设置 root 密码                                   |
| ConnectBranchGitHub            | 将集群与 GitHub 仓库连接以启用分支集成     |
| DisconnectBranchGitHub         | 断开集群与 GitHub 仓库的连接以禁用分支集成 |

## 控制台审计日志字段

为帮助您跟踪用户活动，TiDB Cloud 为每个控制台审计日志提供以下字段：

| 字段名称 | 数据类型 | 描述 |
|---|---|---|
| type | string | 事件类型 |
| ends_at | timestamp | 事件时间 |
| operator_type | enum | 操作者类型：`user` 或 `api_key` |
| operator_id | uint64 | 操作者 ID |
| operator_name | string | 操作者名称 |
| operator_ip | string | 操作者的 IP 地址 |
| operator_login_method | enum | 操作者的登录方法：`google`、`github`、`microsoft`、`email` 或 `api_key` |
| org_id | uint64 | 事件所属的组织 ID |
| org_name | string | 事件所属的组织名称 |
| project_id | uint64 | 事件所属的项目 ID |
| project_name | string | 事件所属的项目名称 |
| cluster_id | uint64 | 事件所属的集群 ID |
| cluster_name | string | 事件所属的集群名称 |
| trace_id | string | 操作者发起请求的跟踪 ID。此字段目前为空，将在未来版本中提供。 |
| result | enum | 事件结果：`success` 或 `failure` |
| details | json | 事件的详细描述 |
