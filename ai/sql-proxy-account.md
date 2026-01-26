---
title: SQL Proxy Account
summary: 了解 TiDB Cloud 中的 SQL 代理账号。
---

# SQL 代理账号 <!-- Draft translated by AI -->

SQL 代理账号是 TiDB Cloud 自动为 TiDB Cloud 用户创建的 SQL 用户账号，用于通过 [SQL Editor](/ai/explore-data-with-chat2query.md) 或 [Data Service](https://docs.pingcap.com/tidbcloud/api/v1beta1/dataservice) 代表用户访问数据库。例如，`testuser@pingcap.com` 是一个 TiDB Cloud 用户账号，而 `3jhEcSimm7keKP8.testuser._41mqK6H4` 则是其对应的 SQL 代理账号。

SQL 代理账号为在 TiDB Cloud 中访问数据库提供了一种安全的、基于令牌的身份验证机制。通过消除传统的用户名和密码凭证，SQL 代理账号提升了安全性并简化了访问管理。

SQL 代理账号的主要优势如下：

- 增强安全性：通过使用 JWT 令牌，降低了与静态凭证相关的风险。
- 精简访问控制：仅限于 SQL Editor 和 Data Service 访问，确保精确的权限管理。
- 易于管理：为开发者和管理员简化了 TiDB Cloud 的身份验证流程。

## 识别 SQL 代理账号

如果你想判断某个 SQL 账号是否为 SQL 代理账号，请按照以下步骤操作：

1. 检查 `mysql.user` 表：

    ```sql
    USE mysql;
    SELECT user FROM user WHERE plugin = 'tidb_auth_token';
    ```

2. 检查该 SQL 账号的授权信息。如果授权中包含 `role_admin`、`role_readonly` 或 `role_readwrite` 等角色，则该账号为 SQL 代理账号。

    ```sql
    SHOW GRANTS for 'username';
    ```

## SQL 代理账号的创建方式

当 TiDB Cloud 用户被授予集群权限角色时，SQL 代理账号会在 TiDB Cloud 集群初始化期间自动创建。

## SQL 代理账号的删除方式

当用户被移出 [组织](/tidb-cloud/manage-user-access.md#remove-an-organization-member) 或 [项目](/tidb-cloud/manage-user-access.md#remove-a-project-member)，或者其角色变更为无权访问集群的角色时，SQL 代理账号会被自动删除。

需要注意的是，如果 SQL 代理账号被手动删除，当用户下次登录 TiDB Cloud 控制台时，该账号会被自动重新创建。

## SQL 代理账号用户名

在某些情况下，SQL 代理账号的用户名与 TiDB Cloud 用户名完全相同，但在其他情况下则不完全相同。SQL 代理账号的用户名由 TiDB Cloud 用户邮箱地址的长度决定，规则如下：

| 环境 | 邮箱长度 | 用户名格式 |
| ----------- | ------------ | --------------- |
| TiDB Cloud Dedicated | <= 32 个字符 | 完整邮箱地址 |
| TiDB Cloud Dedicated | > 32 个字符 | `prefix($email, 23)_prefix(base58(sha1($email)), 8)` |
| TiDB Cloud Serverless | <= 15 个字符 | `serverless_unique_prefix + "." + email` |
| TiDB Cloud Serverless | > 15 个字符 | `serverless_unique_prefix + "." + prefix($email, 6)_prefix(base58(sha1($email)), 8)` |

示例：

| 环境 | 邮箱地址 | SQL 代理账号用户名 |
| ----------- | ----- | -------- |
| TiDB Cloud Dedicated | `user@pingcap.com` | `user@pingcap.com` |
| TiDB Cloud Dedicated | `longemailaddressexample@pingcap.com` | `longemailaddressexample_48k1jwL9` |
| TiDB Cloud Serverless | `u1@pingcap.com` | `{user_name_prefix}.u1@pingcap.com` |
| TiDB Cloud Serverless | `longemailaddressexample@pingcap.com` | `{user_name_prefix}.longem_48k1jwL9`|

> **Note:**
>
> 在上表中，`{user_name_prefix}` 是 TiDB Cloud 为区分 TiDB Cloud Serverless 集群而生成的唯一前缀。详情请参见 TiDB Cloud Serverless 集群的 [user name prefix](/tidb-cloud/select-cluster-tier.md#user-name-prefix)。

## SQL 代理账号密码

由于 SQL 代理账号基于 JWT 令牌，因此无需为这些账号管理密码。安全令牌由系统自动管理。

## SQL 代理账号角色

SQL 代理账号的角色取决于 TiDB Cloud 用户的 IAM 角色：

- 组织级别：
    - Organization Owner: role_admin
    - Organization Billing Manager: 无代理账号
    - Organization Viewer: 无代理账号
    - Organization Console Audit Manager: 无代理账号

- 项目级别：
    - Project Owner: role_admin
    - Project Data Access Read-Write: role_readwrite
    - Project Data Access Read-Only: role_readonly

## SQL 代理账号访问控制

SQL 代理账号基于 JWT 令牌，仅可用于 Data Service 和 SQL Editor 访问。无法通过用户名和密码使用 SQL 代理账号访问 TiDB Cloud 集群。