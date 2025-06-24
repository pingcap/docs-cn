---
title: SQL 代理账号
summary: 了解 TiDB Cloud 中的 SQL 代理账号。
---

# SQL 代理账号

SQL 代理账号是由 TiDB Cloud 自动创建的 SQL 用户账号，用于代表 TiDB Cloud 用户通过 [SQL 编辑器](/tidb-cloud/explore-data-with-chat2query.md)或[数据服务](https://docs.pingcap.com/tidbcloud/api/v1beta1/dataservice)访问数据库。例如，`testuser@pingcap.com` 是一个 TiDB Cloud 用户账号，而 `3jhEcSimm7keKP8.testuser._41mqK6H4` 是其对应的 SQL 代理账号。

SQL 代理账号为 TiDB Cloud 中的数据库访问提供了一个安全的、基于令牌的身份验证机制。通过消除传统的用户名和密码凭证的需求，SQL 代理账号增强了安全性并简化了访问管理。

SQL 代理账号的主要优势如下：

- 增强安全性：通过使用 JWT 令牌降低与静态凭证相关的风险。
- 简化访问：将访问权限特别限制在 SQL 编辑器和数据服务上，确保精确控制。
- 易于管理：简化了在 TiDB Cloud 中工作的开发人员和管理员的身份验证。

## 识别 SQL 代理账号

如果你想确定特定的 SQL 账号是否为 SQL 代理账号，请执行以下步骤：

1. 检查 `mysql.user` 表：

    ```sql
    USE mysql;
    SELECT user FROM user WHERE plugin = 'tidb_auth_token';
    ```

2. 检查该 SQL 账号的授权。如果列出了 `role_admin`、`role_readonly` 或 `role_readwrite` 等角色，则它是一个 SQL 代理账号。

    ```sql
    SHOW GRANTS for 'username';
    ```

## SQL 代理账号如何创建

当在集群中被授予具有权限的角色的 TiDB Cloud 用户，在 TiDB Cloud 集群初始化期间会自动创建 SQL 代理账号。

## SQL 代理账号如何删除

当用户从[组织](/tidb-cloud/manage-user-access.md#remove-an-organization-member)或[项目](/tidb-cloud/manage-user-access.md#remove-a-project-member)中被移除，或其角色更改为无法访问集群的角色时，SQL 代理账号会自动删除。

请注意，如果手动删除了 SQL 代理账号，当用户下次登录 TiDB Cloud 控制台时，该账号会自动重新创建。

## SQL 代理账号用户名

在某些情况下，SQL 代理账号用户名与 TiDB Cloud 用户名完全相同，但在其他情况下则不完全相同。SQL 代理账号用户名由 TiDB Cloud 用户的电子邮件地址长度决定。规则如下：

| 环境 | 邮箱长度 | 用户名格式 |
| ----------- | ------------ | --------------- |
| TiDB Cloud Dedicated | <= 32 字符 | 完整邮箱地址 |
| TiDB Cloud Dedicated | > 32 字符 | `prefix($email, 23)_prefix(base58(sha1($email)), 8)` |
| TiDB Cloud Serverless | <= 15 字符 | `serverless_unique_prefix + "." + email` |
| TiDB Cloud Serverless | > 15 字符 | `serverless_unique_prefix + "." + prefix($email, 6)_prefix(base58(sha1($email)), 8)` |

示例：

| 环境 | 邮箱地址 | SQL 代理账号用户名 |
| ----------- | ----- | -------- |
| TiDB Cloud Dedicated | `user@pingcap.com` | `user@pingcap.com` |
| TiDB Cloud Dedicated | `longemailaddressexample@pingcap.com` | `longemailaddressexample_48k1jwL9` |
| TiDB Cloud Serverless | `u1@pingcap.com` | `{user_name_prefix}.u1@pingcap.com` |
| TiDB Cloud Serverless | `longemailaddressexample@pingcap.com` | `{user_name_prefix}.longem_48k1jwL9`|

> **注意：**
>
> 在上表中，`{user_name_prefix}` 是由 TiDB Cloud 生成的唯一前缀，用于区分 TiDB Cloud Serverless 集群。详情请参见 TiDB Cloud Serverless 集群的[用户名前缀](/tidb-cloud/select-cluster-tier.md#user-name-prefix)。

## SQL 代理账号密码

由于 SQL 代理账号基于 JWT 令牌，因此无需管理这些账号的密码。安全令牌由系统自动管理。

## SQL 代理账号角色

SQL 代理账号的角色取决于 TiDB Cloud 用户的 IAM 角色：

- 组织级别：
    - 组织所有者：role_admin
    - 组织计费管理员：无代理账号
    - 组织查看者：无代理账号
    - 组织控制台审计管理员：无代理账号

- 项目级别：
    - 项目所有者：role_admin
    - 项目数据访问读写：role_readwrite
    - 项目数据访问只读：role_readonly

## SQL 代理账号访问控制

SQL 代理账号基于 JWT 令牌，只能通过数据服务和 SQL 编辑器访问。无法使用用户名和密码通过 SQL 代理账号访问 TiDB Cloud 集群。
