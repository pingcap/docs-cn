---
title: TiDB Dashboard 用户管理
summary: 了解如何创建 TiDB Dashboard 自定义 SQL 用户
---

# TiDB Dashboard 用户管理

从 TiDB 5.3 开始，TiDB Dashboard 支持使用自定义的 SQL 用户登录访问，你可以为自定义 SQL 用户指定所需要的权限。

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

## 创建自定义用户示例

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

## 登录 Dashboard

创建 TiDB Dashboard 自定义 SQL 用户后，你可以使用该账号密码[登录](/dashboard/dashboard-access.md#登录) TiDB Dashboard。
