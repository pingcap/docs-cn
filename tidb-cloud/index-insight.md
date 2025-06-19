---
title: 索引洞察（Beta）
summary: 了解如何使用 TiDB Cloud 中的索引洞察功能并获取慢查询的索引建议。
---

# 索引洞察（Beta）

TiDB Cloud 中的索引洞察（beta）功能通过为未有效使用索引的慢查询提供索引建议，提供了强大的查询性能优化能力。本文档将指导您完成启用和有效使用索引洞察功能的步骤。

> **注意：**
>
> 索引洞察目前处于 beta 阶段，仅适用于 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群。

## 简介

索引洞察功能为您提供以下好处：

- 增强查询性能：索引洞察识别慢查询并为其建议适当的索引，从而加快查询执行速度，减少响应时间，提升用户体验。
- 成本效益：通过使用索引洞察优化查询性能，减少了对额外计算资源的需求，使您能够更有效地使用现有基础设施。这可能带来运营成本的节省。
- 简化优化过程：索引洞察简化了索引改进的识别和实施过程，消除了手动分析和猜测的需要。因此，您可以通过准确的索引建议节省时间和精力。
- 提高应用效率：通过使用索引洞察优化数据库性能，运行在 TiDB Cloud 上的应用程序可以处理更大的工作负载并同时服务更多用户，这使应用程序的扩展操作更加高效。

## 使用方法

本节介绍如何启用索引洞察功能并获取慢查询的推荐索引。

### 开始之前

在启用索引洞察功能之前，请确保您已创建 TiDB Cloud Dedicated 集群。如果您还没有，请按照[创建 TiDB Cloud Dedicated 集群](/tidb-cloud/create-tidb-cluster.md)中的步骤创建一个。

### 步骤 1：启用索引洞察

1. 导航到 TiDB Cloud Dedicated 集群的[**诊断**](/tidb-cloud/tune-performance.md#查看诊断页面)页面。

2. 点击**索引洞察 BETA** 标签。将显示**索引洞察概览**页面。

3. 要使用索引洞察功能，您需要创建一个专用的 SQL 用户，该用户用于触发该功能并接收索引建议。以下 SQL 语句创建一个具有所需权限的新 SQL 用户，包括 `information_schema` 和 `mysql` 的读取权限，以及所有数据库的 `PROCESS` 和 `REFERENCES` 权限。将 `'index_insight_user'` 和 `'random_password'` 替换为您的值。

    ```sql
    CREATE user 'index_insight_user'@'%' IDENTIFIED by 'random_password';
    GRANT SELECT ON information_schema.* TO 'index_insight_user'@'%';
    GRANT SELECT ON mysql.* TO 'index_insight_user'@'%';
    GRANT PROCESS, REFERENCES ON *.* TO 'index_insight_user'@'%';
    FLUSH PRIVILEGES;
    ```

    > **注意：**
    >
    > 要连接到您的 TiDB Cloud Dedicated 集群，请参见[连接到 TiDB Cloud Dedicated 集群](/tidb-cloud/connect-to-tidb-cluster.md)。

4. 输入在前面步骤中创建的 SQL 用户的用户名和密码。然后，点击**激活**开始激活过程。

### 步骤 2：手动触发索引洞察

要获取慢查询的索引建议，您可以通过点击**索引洞察概览**页面右上角的**检查**来手动触发索引洞察功能。

然后，该功能开始扫描过去三小时的慢查询。扫描完成后，它会根据分析提供索引建议列表。

### 步骤 3：查看索引建议

要查看特定索引建议的详细信息，请从列表中点击洞察。将显示**索引洞察详情**页面。

在此页面上，您可以找到索引建议、相关慢查询、执行计划和相关指标。这些信息可帮助您更好地理解性能问题并评估实施索引建议的潜在影响。

### 步骤 4：实施索引建议

在实施索引建议之前，您需要先从**索引洞察详情**页面审查和评估建议。

要实施索引建议，请按照以下步骤操作：

1. 评估建议的索引对现有查询和工作负载的影响。
2. 考虑与索引实施相关的存储需求和潜在权衡。
3. 使用适当的数据库管理工具在相关表上创建索引建议。
4. 实施索引后监控性能以评估改进情况。

## 最佳实践

本节介绍使用索引洞察功能的一些最佳实践。

### 定期触发索引洞察

为了维护优化的索引，建议定期触发索引洞察功能，例如每天一次，或在查询或数据库架构发生重大变化时触发。

### 实施索引前分析影响

在实施索引建议之前，分析对查询执行计划、磁盘空间和任何相关权衡的潜在影响。优先实施能提供最显著性能改进的索引。

### 监控性能

实施索引建议后定期监控查询性能。这有助于您确认改进情况并在必要时进行进一步调整。

## 常见问题

本节列出了有关索引洞察功能的一些常见问题。

### 如何停用索引洞察？

要停用索引洞察功能，请执行以下步骤：

1. 在**索引洞察概览**页面的右上角，点击**设置**。将显示**索引洞察设置**页面。
2. 点击**停用**。将显示确认对话框。
3. 点击**确定**确认停用。

    停用索引洞察功能后，所有索引建议都将从**索引洞察概览**页面中删除。但是，为该功能创建的 SQL 用户不会被删除。您可以手动删除该 SQL 用户。

### 停用索引洞察后如何删除 SQL 用户？

停用索引洞察功能后，您可以执行 `DROP USER` 语句删除为该功能创建的 SQL 用户。以下是一个示例。将 `'username'` 替换为您的值。

```sql
DROP USER 'username';
```

### 为什么在激活或检查期间显示 `invalid user or password` 消息？

`invalid user or password` 消息通常在系统无法验证您提供的凭据时提示。此问题可能由各种原因引起，例如用户名或密码不正确，或用户账户已过期或被锁定。

要解决此问题，请执行以下步骤：

1. 验证您的凭据：确保您提供的用户名和密码正确。注意区分大小写。
2. 检查账户状态：确保您的用户账户处于活动状态，未过期或被锁定。您可以通过联系系统管理员或相关支持渠道确认这一点。
3. 创建新的 SQL 用户：如果通过前面的步骤未解决此问题，您可以使用以下语句创建新的 SQL 用户。将 `'index_insight_user'` 和 `'random_password'` 替换为您的值。

    ```sql
    CREATE user 'index_insight_user'@'%' IDENTIFIED by 'random_password';
    GRANT SELECT ON information_schema.* TO 'index_insight_user'@'%';
    GRANT SELECT ON mysql.* TO 'index_insight_user'@'%';
    GRANT PROCESS, REFERENCES ON *.* TO 'index_insight_user'@'%';
    FLUSH PRIVILEGES;
    ```

如果在执行上述步骤后仍然遇到问题，建议联系 [PingCAP 支持团队](/tidb-cloud/tidb-cloud-support.md)。

### 为什么在激活或检查期间显示 `no sufficient privileges` 消息？

`no sufficient privileges` 消息通常在您提供的 SQL 用户缺少从索引洞察请求索引建议所需的权限时提示。

要解决此问题，请执行以下步骤：

1. 检查用户权限：确认您的用户账户是否已被授予所需权限，包括 `information_schema` 和 `mysql` 的读取权限，以及所有数据库的 `PROCESS` 和 `REFERENCES` 权限。

2. 创建新的 SQL 用户：如果通过前面的步骤未解决此问题，您可以使用以下语句创建新的 SQL 用户。将 `'index_insight_user'` 和 `'random_password'` 替换为您的值。

    ```sql
    CREATE user 'index_insight_user'@'%' IDENTIFIED by 'random_password';
    GRANT SELECT ON information_schema.* TO 'index_insight_user'@'%';
    GRANT SELECT ON mysql.* TO 'index_insight_user'@'%';
    GRANT PROCESS, REFERENCES ON *.* TO 'index_insight_user'@'%';
    FLUSH PRIVILEGES;
    ```

如果在执行上述步骤后仍然遇到问题，建议联系 [PingCAP 支持团队](/tidb-cloud/tidb-cloud-support.md)。

### 为什么在使用索引洞察时显示 `operations may be too frequent` 消息？

`operations may be too frequent` 消息通常在您超过索引洞察设置的速率或使用限制时提示。

要解决此问题，请执行以下步骤：

1. 降低操作频率：如果您收到此消息，您需要降低对索引洞察的操作频率。
2. 联系支持：如果问题仍然存在，请联系 [PingCAP 支持团队](/tidb-cloud/tidb-cloud-support.md)并提供错误消息、您的操作以及任何其他相关信息的详细信息。

### 为什么在使用索引洞察时显示 `internal error` 消息？

`internal error` 消息通常在系统遇到意外错误或问题时提示。此错误消息是通用的，不提供有关根本原因的详细信息。

要解决此问题，请执行以下步骤：

1. 重试操作：刷新页面或重试操作。错误可能是临时的，可以通过简单的重试来解决。
2. 联系支持：如果问题仍然存在，请联系 [PingCAP 支持团队](/tidb-cloud/tidb-cloud-support.md)并提供错误消息、您的操作以及任何其他相关信息的详细信息。
