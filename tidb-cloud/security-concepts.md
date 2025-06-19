---
title: 安全性
summary: 了解 TiDB Cloud 的安全性概念。
---

# 安全性

TiDB Cloud 提供了一个强大且灵活的安全框架，旨在保护数据、执行访问控制并满足现代合规标准。该框架将高级安全功能与运营效率相结合，以支持大规模的组织需求。

**关键组件**

- **身份和访问管理（IAM）**：为 TiDB Cloud 控制台和数据库环境提供安全且灵活的身份验证和权限管理。

- **网络访问控制**：可配置的连接选项，包括私有端点、VPC 对等连接、TLS 加密和 IP 访问列表。

- **数据访问控制**：高级加密功能，如客户管理的加密密钥（CMEK），用于保护静态数据。

- **审计日志**：全面跟踪控制台操作和数据库操作，确保问责制和透明度。

通过整合这些功能，TiDB Cloud 使组织能够保护敏感数据、简化访问控制并优化安全操作。

## 身份和访问管理（IAM）

TiDB Cloud 采用身份和访问管理（IAM）来安全高效地管理控制台和数据库环境中的用户身份和权限。IAM 功能通过身份验证选项、基于角色的访问控制和分层资源结构的组合，旨在满足组织的安全性和合规性需求。

### TiDB Cloud 用户账户

TiDB Cloud 用户账户是管理平台中资源身份和访问的基础。每个账户代表平台中的个人或实体，并支持多种身份验证方法以满足组织需求：

- **默认用户名和密码**

    - 用户使用电子邮件地址和密码创建账户。

    - 适用于没有外部身份提供商的小型团队或个人。

- **标准 SSO 身份验证**

    - 用户通过 GitHub、Google 或 Microsoft 账户登录。

    - 默认为所有组织启用。

    - **最佳实践**：适用于较小的团队或没有严格合规需求的团队。

    - 更多信息，请参见[标准 SSO 身份验证](/tidb-cloud/tidb-cloud-sso-authentication.md)。

- **组织 SSO 身份验证**

    - 使用 OIDC 或 SAML 协议与企业身份提供商（IdP）集成。

    - 启用多因素认证强制执行、密码过期策略和域名限制等功能。

    - **最佳实践**：适用于具有高级安全性和合规性要求的大型组织。

    - 更多信息，请参见[组织 SSO 身份验证](/tidb-cloud/tidb-cloud-org-sso-authentication.md)。

### 数据库访问控制

TiDB Cloud 通过基于用户和基于角色的权限提供细粒度的数据库访问控制。这些机制使管理员能够安全地管理数据对象和模式的访问，同时确保符合组织的安全策略。

- **最佳实践：**

    - 通过仅授予用户其角色所需的权限来实施最小权限原则。

    - 定期审核和更新用户访问权限，以适应不断变化的组织需求。

### 数据库用户账户

数据库用户账户存储在 `mysql.user` 系统表中，并通过用户名和客户端主机唯一标识。

在数据库初始化期间，TiDB 自动创建一个默认账户：`'root'@'%'`。

更多信息，请参见 [TiDB 用户账户管理](https://docs.pingcap.com/tidb/stable/user-account-management#user-names-and-passwords)。

### SQL 代理账户

SQL 代理账户是由 TiDB Cloud 自动生成的特殊用途账户。这些账户的主要特征包括：

- **与 TiDB Cloud 用户账户关联：** 每个 SQL 代理账户对应一个特定的 TiDB Cloud 用户。

- **映射到角色：** SQL 代理账户被授予 `role_admin` 角色。

- **基于令牌：** SQL 代理账户使用安全的 JWT 令牌而不是密码，确保通过 TiDB Cloud 数据服务或 SQL 编辑器进行无缝、受限访问。

### TiDB 权限和角色

TiDB 的权限管理系统基于 MySQL 5.7，支持对数据库对象的细粒度访问。同时，TiDB 还引入了 MySQL 8.0 的 RBAC 和动态权限机制。这实现了细粒度和便捷的数据库权限管理。

**静态权限**

- 支持基于数据库对象的细粒度访问控制，包括表、视图、索引、用户和其他对象。

- *示例：向用户授予特定表的 SELECT 权限。*

**动态权限**

- 支持合理拆分数据库管理权限，实现系统管理权限的细粒度控制。

- 示例：将 `BACKUP_ADMIN` 分配给管理数据库备份的账户，而不需要更广泛的管理权限。

**SQL 角色（RBAC）**

- 将权限分组到可分配给用户的角色中，实现简化的权限管理和动态更新。

- 示例：为分析师分配读写角色以简化用户访问控制。

该系统确保了管理用户访问的灵活性和精确性，同时符合组织政策。

### 组织和项目

TiDB Cloud 使用分层结构管理用户和资源：组织、项目和集群。

**组织**

- 管理资源、角色和计费的顶级实体。

- 组织所有者拥有完整权限，包括项目创建和角色分配。

**项目**

- 组织的子部门，包含集群和特定于项目的配置。

- 由负责其范围内集群的项目所有者管理。

**集群**

- 项目内的单个数据库实例。

### 示例结构

```
- 您的组织
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

### 主要功能

- **细粒度权限**：
    - 在组织和项目级别分配特定角色，实现精确的访问控制。

    - 通过仔细规划角色分配确保灵活性和安全性。

- **计费管理**：
    - 在组织级别整合计费，并提供每个项目的详细分类。

### 身份和访问管理（IAM）角色

TiDB Cloud 提供基于角色的访问控制来管理组织和项目的权限：

- **[组织级角色](/tidb-cloud/manage-user-access.md#organization-roles)**：授予管理整个组织的权限，包括计费和项目创建。

- **[项目级角色](/tidb-cloud/manage-user-access.md#project-roles)**：分配管理特定项目的权限，包括集群和配置。

## 网络访问控制

TiDB Cloud 通过强大的网络访问控制确保集群连接和数据传输的安全性。主要功能包括：

### 私有端点

- 使您的虚拟私有云（VPC）中的 SQL 客户端能够安全连接到 TiDB Cloud Dedicated 集群。

- 支持 [AWS PrivateLink](/tidb-cloud/set-up-private-endpoint-connections.md)、[Azure Private Link](/tidb-cloud/set-up-private-endpoint-connections-on-azure.md) 和 [Google Cloud Private Service Connect](/tidb-cloud/set-up-private-endpoint-connections-on-google-cloud.md)。

**最佳实践：** 在生产环境中使用私有端点以最小化公共暴露，并定期审查配置。

### TLS（传输层安全）

- 加密客户端和服务器之间的通信以保护数据传输。

- 提供 [Serverless](/tidb-cloud/secure-connections-to-serverless-clusters.md) 和 [Dedicated](/tidb-cloud/tidb-cloud-tls-connect-to-dedicated.md) 集群的设置指南。

**最佳实践：** 确保 TLS 证书是最新的，并定期轮换。

### VPC 对等连接

- 在虚拟私有云之间建立私有连接，实现安全、无缝的通信。

- 更多信息，请参见[通过 VPC 对等连接连接到 TiDB Cloud Dedicated](/tidb-cloud/set-up-vpc-peering-connections.md)。

**最佳实践：** 用于关键工作负载以避免公共互联网暴露，并监控性能。

### IP 访问列表

- 作为防火墙限制集群访问仅限于受信任的 IP 地址。

- 更多信息，请参见[配置 IP 访问列表](/tidb-cloud/configure-ip-access-list.md)。

**最佳实践：** 定期审核和更新访问列表以维护安全性。

## 数据访问控制

TiDB Cloud 通过高级加密功能保护静态数据，确保符合行业法规的安全性和合规性。

**客户管理的加密密钥（CMEK）**

- 为组织提供对 TiDB Cloud Dedicated 集群加密的完全控制。

- 启用时使用 CMEK 密钥加密静态数据和备份。

- 对于没有 CMEK 的 TiDB Cloud Dedicated 集群，TiDB Cloud 使用托管密钥；TiDB Cloud Serverless 集群仅使用托管密钥。

**最佳实践：**

- 定期轮换 CMEK 密钥以增强安全性并满足合规标准。

- 使用 CMEK 密钥一致地加密备份以提供额外保护。

- 对于需要严格合规性的行业（如 HIPAA 和 GDPR），利用 CMEK。

更多信息，请参见[使用客户管理的加密密钥进行静态加密](/tidb-cloud/tidb-cloud-encrypt-cmek.md)。

## 审计日志

TiDB Cloud 提供全面的审计日志功能，用于监控用户活动和数据库操作，确保安全性、问责制和合规性。

### 控制台审计日志

跟踪 TiDB Cloud 控制台上的关键操作，如邀请用户或管理集群。

**最佳实践：**

- 将日志与 SIEM 工具集成以进行实时监控和告警。

- 设置保留策略以满足合规要求。

### 数据库审计日志

记录详细的数据库操作，包括执行的 SQL 语句和用户访问。

**最佳实践：**

- 定期审查日志以发现异常活动或未授权访问。

- 使用日志进行合规报告和取证分析。

更多信息，请参见[控制台审计日志](/tidb-cloud/tidb-cloud-console-auditing.md)和[数据库审计日志](/tidb-cloud/tidb-cloud-auditing.md)。
