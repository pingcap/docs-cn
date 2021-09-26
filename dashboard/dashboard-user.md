---
title: TiDB Dashboard 用户
aliases: ['/docs-cn/dev/dashboard/dashboard-user/']
---

# TiDB Dashboard 用户

从 TiDB 5.3 开始，TiDB Dashboard 支持使用任意 SQL 用户登录，该 SQL 用户必须拥有以下权限：

- ALL PRIVILEGES

或者以下所有权限：

- PROCESS
- SHOW DATABASES
- CONFIG
- DASHBOARD_CLIENT 或者 SUPER

当 TiDB SEM 功能打开时，该 SQL 用户还需要拥用以下额外的所有权限：

- RESTRICTED_TABLES_ADMIN
- RESTRICTED_STATUS_ADMIN
- RESTRICTED_VARIABLES_ADMIN

当权限未满足要求时，登录会提示该用户没有足够权限的错误。如下图所示：

![](/media/dashboard/dashboard-user-insufficient-privileges.png)

此外，当该 SQL 用户拥有以下三种权限之一时，具有写权限，登录 TiDB Dashboard 后可以进行修改配置的操作，否则只有读权限。

- ALL PRIVILEGES
- SUPER
- SYSTEM_VARIABLES_ADMIN
