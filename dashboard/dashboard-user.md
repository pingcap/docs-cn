---
title: TiDB Dashboard 用户管理
summary: 了解如何创建 SQL 用户用于访问 TiDB Dashboard
---

# TiDB Dashboard 用户管理

TiDB Dashboard 与 TiDB 使用相同的用户权限体系和登录验证方式。你可以通过控制和管理 TiDB SQL 用户，从而限制和约束这些用户对 TiDB Dashboard 的访问。本文描述了 TiDB SQL 用户访问 TiDB Dashboard 所需的最小权限，并提供了如何创建最小权限 SQL 用户的示例。

要了解如何控制和管理 TiDB SQL 用户，请参见 [TiDB 用户账户管理](/user-account-management.md)。

## 所需权限说明

- 当所连接的 TiDB 服务器未启用[安全增强模式 (SEM)](/system-variables.md#tidb_enable_enhanced_security) 时，要访问 TiDB Dashboard，SQL 用户应当拥有以下**所有**权限：

    - PROCESS
    - SHOW DATABASES
    - CONFIG
    - DASHBOARD_CLIENT

- 当所连接的 TiDB 服务器启用了[安全增强模式 (SEM)](/system-variables.md#tidb_enable_enhanced_security) 时，要访问 TiDB Dashboard，SQL 用户应当拥有以下**所有**权限：

    - PROCESS
    - SHOW DATABASES
    - CONFIG
    - DASHBOARD_CLIENT
    - RESTRICTED_TABLES_ADMIN
    - RESTRICTED_STATUS_ADMIN
    - RESTRICTED_VARIABLES_ADMIN

- 若希望 SQL 用户在登录 TiDB Dashboard 后允许修改界面上的各项配置，SQL 用户还应当拥有以下权限：

    - SYSTEM_VARIABLES_ADMIN

> **注意：**
> 
> 拥有 `ALL PRIVILEGES` 或 `SUPER` 等粗粒度高权限的用户同样可以登录 TiDB Dashboard。出于最小权限原则，强烈建议创建用户时仅使用上述精细权限，从而防止用户执行非预期操作。请参阅[权限管理](/privilege-management.md)了解这些权限的详细信息。

如果登录 TiDB Dashboard 时指定的 SQL 用户未满足上述权限需求，则登录将失败，如下图所示：

![insufficient-privileges](/media/dashboard/dashboard-user-insufficient-privileges.png)

## 示例：创建一个最小权限 SQL 用户用于登录 TiDB Dashboard

- 当所连接的 TiDB 服务器未启用[安全增强模式 (SEM)](/system-variables.md#tidb_enable_enhanced_security) 时，你可以通过执行以下示例 SQL 语句创建一个允许登录 TiDB Dashboard 的 SQL 用户 `dashboardAdmin`：

    ```sql
    CREATE USER 'dashboardAdmin'@'%' IDENTIFIED BY '<YOUR_PASSWORD>';
    GRANT PROCESS, CONFIG ON *.* TO 'dashboardAdmin'@'%';
    GRANT SHOW DATABASES ON *.* TO 'dashboardAdmin'@'%';
    GRANT DASHBOARD_CLIENT ON *.* TO 'dashboardAdmin'@'%';

    -- 如果要使自定义的 SQL 用户能修改 TiDB Dashboard 界面上的各项配置，可以增加以下权限
    GRANT SYSTEM_VARIABLES_ADMIN ON *.* TO 'dashboardAdmin'@'%';
    ```

- 当所连接的 TiDB 服务器启用了[安全增强模式 (SEM)](/system-variables.md#tidb_enable_enhanced_security) 时，先关闭 SEM，然后执行以下示例 SQL 语句创建一个允许登录 TiDB Dashboard 的 SQL 用户 `dashboardAdmin` ，创建完成后，再重新开启 SEM：

    ```sql
    CREATE USER 'dashboardAdmin'@'%' IDENTIFIED BY '<YOUR_PASSWORD>';
    GRANT PROCESS, CONFIG ON *.* TO 'dashboardAdmin'@'%';
    GRANT SHOW DATABASES ON *.* TO 'dashboardAdmin'@'%';
    GRANT DASHBOARD_CLIENT ON *.* TO 'dashboardAdmin'@'%';
    GRANT RESTRICTED_STATUS_ADMIN ON *.* TO 'dashboardAdmin'@'%';
    GRANT RESTRICTED_TABLES_ADMIN ON *.* TO 'dashboardAdmin'@'%';
    GRANT RESTRICTED_VARIABLES_ADMIN ON *.* TO 'dashboardAdmin'@'%';

    -- 如果要使自定义的 SQL 用户能修改 TiDB Dashboard 界面上的各项配置，可以增加以下权限
    GRANT SYSTEM_VARIABLES_ADMIN ON *.* TO 'dashboardAdmin'@'%';
    ```

## 登录 TiDB Dashboard

创建满足 TiDB Dashboard 权限要求的 SQL 用户后，你可以使用该用户[登录](/dashboard/dashboard-access.md#登录) TiDB Dashboard。
