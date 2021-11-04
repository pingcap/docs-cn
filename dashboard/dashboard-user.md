---
title: TiDB Dashboard 用户管理
summary: 了解如何创建 TiDB Dashboard 自定义 SQL 用户
---

# TiDB Dashboard 用户管理

TiDB Dashboard 与 TiDB 使用相同的用户权限体系和登录验证方式。你可以通过控制和管理 TiDB SQL 用户，从而限制和约束这些用户对 TiDB Dashboard 的访问。本文详细描述了 TiDB SQL 用户访问 TiDB Dashboard 所需的最小权限。

另请参见 [TiDB 用户账户管理](/user-account-management.md)了解如何控制和管理 TiDB SQL 用户。

## 所需权限说明

- 当所连接的 TiDB 服务器未启用[安全增强模式 (SEM)](/system-variables.md#tidb_enable_enhanced_security) 时，要访问 TiDB Dashboard，需要为自定义的 SQL 用户赋予 `ALL PRIVILEGES` 权限或者以下**所有**权限：

    - PROCESS
    - SHOW DATABASES
    - CONFIG
    - DASHBOARD_CLIENT 或者 SUPER

- 当所连接的 TiDB 服务器启用了[安全增强模式 (SEM)](/system-variables.md#tidb_enable_enhanced_security) 时，要访问 TiDB Dashboard，需要为自定义的 SQL 用户赋予 `ALL PRIVILEGES` 权限或者以下**所有**权限：

    - PROCESS
    - SHOW DATABASES
    - CONFIG
    - DASHBOARD_CLIENT 或者 SUPER
    - RESTRICTED_TABLES_ADMIN
    - RESTRICTED_STATUS_ADMIN
    - RESTRICTED_VARIABLES_ADMIN

- 当需要自定义的 SQL 用户在登录 TiDB Dashboard 后能修改界面上的各项配置时，请为自定义的 SQL 用户赋予以下**任意**权限时。否则 SQL 用户只有读权限，无法修改配置。

    - ALL PRIVILEGES
    - SUPER
    - SYSTEM_VARIABLES_ADMIN

如果自定义的 SQL 用户的权限未满足要求时，该用户将无法登录 TiDB Dashboard。如下图所示：

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

- 当所连接的 TiDB 服务器启用了[安全增强模式 (SEM)](/system-variables.md#tidb_enable_enhanced_security) 时，你可以通过执行以下示例 SQL 语句创建一个允许登录 TiDB Dashboard 的 SQL 用户 `dashboardAdmin`：

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

创建 TiDB Dashboard 自定义 SQL 用户后，你可以使用该账号密码[登录](/dashboard/dashboard-access.md#登录) TiDB Dashboard。
