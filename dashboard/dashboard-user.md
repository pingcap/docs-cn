---
title: TiDB Dashboard 多用户
aliases: ['/docs-cn/dev/dashboard/dashboard-user/']
---

# TiDB Dashboard 多用户

从 TiDB 5.3 开始，TiDB Dashboard 支持使用自定义的 SQL 用户登录访问。该 SQL 用户必须拥有以下权限：

- ALL PRIVILEGES

或者以下所有权限：

- PROCESS
- SHOW DATABASES
- CONFIG
- DASHBOARD_CLIENT 或者 SUPER

当 TiDB 的[安全增强模式 (SEM) 功能](/system-variables.md#tidb_enable_enhanced_security)打开时，该 SQL 用户还需要拥用以下额外的所有权限：

- RESTRICTED_TABLES_ADMIN
- RESTRICTED_STATUS_ADMIN
- RESTRICTED_VARIABLES_ADMIN

当用户的权限未满足要求时，将无法使用该用户登录 TiDB Dashboard，如下图所示：

![](/media/dashboard/dashboard-user-insufficient-privileges.png)

此外，当该 SQL 用户拥有以下**任意**权限时，登录 TiDB Dashboard 后可在界面上对各项配置进行修改，否则只有读权限，无法修改配置：

- ALL PRIVILEGES
- SUPER
- SYSTEM_VARIABLES_ADMIN

## 示例

通过执行以下示例 SQL 语句可以创建一个允许登录 TiDB Dashboard 的 SQL 用户 `dashboardAdmin`：

```sql
CREATE USER 'dashboardAdmin'@'%' IDENTIFIED BY '<YOUR_PASSWORD>';
GRANT PROCESS, CONFIG ON *.* TO 'dashboardAdmin'@'%';
GRANT SHOW DATABASES ON *.* TO 'dashboardAdmin'@'%';
GRANT DASHBOARD_CLIENT ON *.* TO 'dashboardAdmin'@'%';

-- To also allow modifying TiDB Dashboard configurations:
GRANT SYSTEM_VARIABLES_ADMIN ON *.* TO 'dashboardAdmin'@'%';
```

注意：当 TiDB 的[安全增强模式 (SEM) 功能](/system-variables.md#tidb_enable_enhanced_security)打开时，需要执行的 SQL 语句示例如下：

```sql
CREATE USER 'dashboardAdmin'@'%' IDENTIFIED BY '<YOUR_PASSWORD>';
GRANT PROCESS, CONFIG ON *.* TO 'dashboardAdmin'@'%';
GRANT SHOW DATABASES ON *.* TO 'dashboardAdmin'@'%';
GRANT DASHBOARD_CLIENT ON *.* TO 'dashboardAdmin'@'%';
GRANT RESTRICTED_STATUS_ADMIN ON *.* TO 'dashboardAdmin'@'%';
GRANT RESTRICTED_TABLES_ADMIN ON *.* TO 'dashboardAdmin'@'%';
GRANT RESTRICTED_VARIABLES_ADMIN ON *.* TO 'dashboardAdmin'@'%';

-- To also allow modifying TiDB Dashboard configurations:
GRANT SYSTEM_VARIABLES_ADMIN ON *.* TO 'dashboardAdmin'@'%';
```
