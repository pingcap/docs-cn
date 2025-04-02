---
title: 权限管理
aliases: ['/docs-cn/dev/privilege-management/','/docs-cn/dev/reference/security/privilege-system/']
summary: TiDB 支持 MySQL 5.7 和 MySQL 8.0 的权限管理系统。权限相关操作包括授予权限、收回权限、查看用户权限和动态权限。权限系统的实现包括授权表和连接验证。权限生效时机是在 TiDB 启动时加载到内存，并且可以手动刷新。
---

# 权限管理

TiDB 支持 MySQL 5.7 的权限管理系统，包括 MySQL 的语法和权限类型。同时 TiDB 还支持 MySQL 8.0 的以下特性：

* 从 TiDB 3.0 开始，支持 SQL 角色。
* 从 TiDB 5.1 开始，支持动态权限。

本文档主要介绍 TiDB 权限相关操作、各项操作需要的权限以及权限系统的实现。

## 权限相关操作

### 授予权限

[`GRANT`](/sql-statements/sql-statement-grant-privileges.md) 语句用于为 TiDB 中的用户分配权限。

授予 `xxx` 用户对数据库 `test` 的读权限：

```sql
GRANT SELECT ON test.* TO 'xxx'@'%';
```

为 `xxx` 用户授予所有数据库，全部权限：

```sql
GRANT ALL PRIVILEGES ON *.* TO 'xxx'@'%';
```

默认情况下，如果指定的用户不存在，[`GRANT`](/sql-statements/sql-statement-grant-privileges.md) 语句将报错。该行为受 [SQL 模式](/system-variables.md#sql_mode)中的 `NO_AUTO_CREATE_USER` 控制。

```sql
SET sql_mode=DEFAULT;
```

```
Query OK, 0 rows affected (0.00 sec)
```

```sql
SELECT @@sql_mode;
```

```
+-------------------------------------------------------------------------------------------------------------------------------------------+
| @@sql_mode                                                                                                                                |
+-------------------------------------------------------------------------------------------------------------------------------------------+
| ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION |
+-------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

```sql
SELECT * FROM mysql.user WHERE user='idontexist';
```

```
Empty set (0.00 sec)
```

```sql
GRANT ALL PRIVILEGES ON test.* TO 'idontexist';
```

```
ERROR 1105 (HY000): You are not allowed to create a user with GRANT
```

```sql
SELECT user,host,authentication_string FROM mysql.user WHERE user='idontexist';
```

```
Empty set (0.00 sec)
```

在下面的例子中，由于没有将 SQL 模式设置为 `NO_AUTO_CREATE_USER`，用户 `idontexist` 会被自动创建且密码为空。**不推荐**使用这种方式，因为会带来安全风险：如果用户名拼写错误，会导致新用户被创建且密码为空。

```sql
SET @@sql_mode='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';
```

```
Query OK, 0 rows affected (0.00 sec)
```

```sql
SELECT @@sql_mode;
```

```
+-----------------------------------------------------------------------------------------------------------------------+
| @@sql_mode                                                                                                            |
+-----------------------------------------------------------------------------------------------------------------------+
| ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION |
+-----------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

```sql
SELECT * FROM mysql.user WHERE user='idontexist';
```

```
Empty set (0.00 sec)
```

```sql
GRANT ALL PRIVILEGES ON test.* TO 'idontexist';
```

```
Query OK, 1 row affected (0.05 sec)
```

```sql
SELECT user,host,authentication_string FROM mysql.user WHERE user='idontexist';
```

```
+------------+------+-----------------------+
| user       | host | authentication_string |
+------------+------+-----------------------+
| idontexist | %    |                       |
+------------+------+-----------------------+
1 row in set (0.01 sec)
```

[`GRANT`](/sql-statements/sql-statement-grant-privileges.md) 还可以模糊匹配地授予用户数据库的权限：

```sql
GRANT ALL PRIVILEGES ON `te%`.* TO genius;
```

```
Query OK, 0 rows affected (0.00 sec)
```

```sql
SELECT user,host,db FROM mysql.db WHERE user='genius';
```

```
+--------|------|-----+
| user   | host | db  |
+--------|------|-----+
| genius | %    | te% |
+--------|------|-----+
1 row in set (0.00 sec)
```

这个例子中通过 `%` 模糊匹配，所有 `te` 开头的数据库，都被授予了权限。

### 收回权限

[`REVOKE`](/sql-statements/sql-statement-revoke-privileges.md) 语句允许系统管理员收回用户的权限。

`REVOKE` 语句的作用与 `GRANT` 相反：

```sql
REVOKE ALL PRIVILEGES ON `test`.* FROM 'genius'@'localhost';
```

> **注意：**
>
> `REVOKE` 收回权限时只做精确匹配，若找不到记录则报错。而 `GRANT` 授予权限时可以使用模糊匹配。

```sql
REVOKE ALL PRIVILEGES ON `te%`.* FROM 'genius'@'%';
```

```
ERROR 1141 (42000): There is no such grant defined for user 'genius' on host '%'
```

关于模糊匹配和转义，字符串和 identifier：

```sql
GRANT ALL PRIVILEGES ON `te\%`.* TO 'genius'@'localhost';
```

```
Query OK, 0 rows affected (0.00 sec)
```

上述例子是精确匹配名为 `te%` 的数据库，注意使用 `\` 转义字符。

以单引号包含的部分，是一个字符串。以反引号包含的部分，是一个 identifier。注意下面的区别：

```sql
GRANT ALL PRIVILEGES ON 'test'.* TO 'genius'@'localhost';
```

```
ERROR 1064 (42000): You have an error in your SQL syntax; check the
manual that corresponds to your MySQL server version for the right
syntax to use near ''test'.* to 'genius'@'localhost'' at line 1
```

```sql
GRANT ALL PRIVILEGES ON `test`.* TO 'genius'@'localhost';
```

```
Query OK, 0 rows affected (0.00 sec)
```

如果想将一些特殊的关键字做为表名，可以用反引号包含起来。比如：

```sql
CREATE TABLE `select` (id int);
```

```
Query OK, 0 rows affected (0.27 sec)
```

### 查看为用户分配的权限

`SHOW GRANTS` 语句可以查看为用户分配了哪些权限。例如：

查看当前用户的权限：

```sql
SHOW GRANTS;
```

```
+-------------------------------------------------------------+
| Grants for User                                             |
+-------------------------------------------------------------+
| GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' WITH GRANT OPTION |
+-------------------------------------------------------------+
```

或者：

```sql
SHOW GRANTS FOR CURRENT_USER();
```

查看某个特定用户的权限：

```sql
SHOW GRANTS FOR 'user'@'host';
```

例如，创建一个用户 `rw_user@192.168.%` 并为其授予 `test.write_table` 表的写权限，和全局读权限。

```sql
CREATE USER `rw_user`@`192.168.%`;
GRANT SELECT ON *.* TO `rw_user`@`192.168.%`;
GRANT INSERT, UPDATE ON `test`.`write_table` TO `rw_user`@`192.168.%`;
```

查看用户 `rw_user@192.168.%` 的权限。

```sql
SHOW GRANTS FOR `rw_user`@`192.168.%`;
```

```
+------------------------------------------------------------------+
| Grants for rw_user@192.168.%                                     |
+------------------------------------------------------------------+
| GRANT Select ON *.* TO 'rw_user'@'192.168.%'                     |
| GRANT Insert,Update ON test.write_table TO 'rw_user'@'192.168.%' |
+------------------------------------------------------------------+
```

### 动态权限

从 v5.1 开始，TiDB 支持 MySQL 8.0 中的动态权限特性。动态权限用于限制 `SUPER` 权限，实现对某些操作更细粒度的访问。例如，系统管理员可以使用动态权限来创建一个只能执行 `BACKUP` 和 `RESTORE` 操作的用户帐户。

动态权限包括：

* `BACKUP_ADMIN`
* `RESTORE_ADMIN`
* `SYSTEM_USER`
* `SYSTEM_VARIABLES_ADMIN`
* `ROLE_ADMIN`
* `CONNECTION_ADMIN`
* `PLACEMENT_ADMIN` 允许创建、删除和修改放置策略 (placement policy)。
* `DASHBOARD_CLIENT` 允许登录 TiDB Dashboard。
* `RESTRICTED_TABLES_ADMIN` 允许在 SEM 打开的情况下查看系统表。
* `RESTRICTED_STATUS_ADMIN` 允许在 SEM 打开的情况下查看 [`SHOW [GLOBAL|SESSION] STATUS`](/sql-statements/sql-statement-show-status.md) 中的状态变量。
* `RESTRICTED_VARIABLES_ADMIN` 允许在 SEM 打开的情况下查看所有系统变量。
* `RESTRICTED_USER_ADMIN` 不允许在 SEM 打开的情况下使用 `SUPER` 用户撤销访问权限。
* `RESTRICTED_CONNECTION_ADMIN` 允许 KILL 属于 `RESTRICTED_USER_ADMIN` 用户的连接。该权限对 `KILL` 和 `KILL TIDB` 语句生效。
* `RESTRICTED_REPLICA_WRITER_ADMIN` 允许权限拥有者在 TiDB 集群开启了只读模式的情况下不受影响地执行写入或更新操作，详见 [`tidb_restricted_read_only` 配置项](/system-variables.md#tidb_restricted_read_only-从-v520-版本开始引入)。
* `TRAFFIC_CAPTURE_ADMIN` 允许执行、查看和取消流量捕获任务。详见 [TiProxy 流量回放](/tiproxy/tiproxy-traffic-replay.md)。
* `TRAFFIC_REPLAY_ADMIN` 允许执行、查看和取消流量回放任务。详见 [TiProxy 流量回放](/tiproxy/tiproxy-traffic-replay.md)。

若要查看全部的动态权限，请执行 `SHOW PRIVILEGES` 语句。由于用户可使用插件来添加新的权限，因此可分配的权限列表可能因用户的 TiDB 安装情况而异。

## `SUPER` 权限

- 拥有 `SUPER` 权限的用户能完成几乎所有的操作，默认情况下只有 `root` 用户拥有该权限。请谨慎向其它用户授予 `SUPER` 权限。
- `SUPER` 权限[在 MySQL 8.0 中被认为是过时的](https://dev.mysql.com/doc/refman/8.0/en/privileges-provided.html#dynamic-privileges-migration-from-super)，可以通过[动态权限](#动态权限)替代 `SUPER` 权限进行更细粒度的权限控制。

## TiDB 各操作需要的权限

TiDB 用户目前拥有的权限可以在 `INFORMATION_SCHEMA.USER_PRIVILEGES` 表中查找到。例如：

```sql
SELECT * FROM INFORMATION_SCHEMA.USER_PRIVILEGES WHERE grantee = "'root'@'%'";
```

```
+------------+---------------+-------------------------+--------------+
| GRANTEE    | TABLE_CATALOG | PRIVILEGE_TYPE          | IS_GRANTABLE |
+------------+---------------+-------------------------+--------------+
| 'root'@'%' | def           | Select                  | YES          |
| 'root'@'%' | def           | Insert                  | YES          |
| 'root'@'%' | def           | Update                  | YES          |
| 'root'@'%' | def           | Delete                  | YES          |
| 'root'@'%' | def           | Create                  | YES          |
| 'root'@'%' | def           | Drop                    | YES          |
| 'root'@'%' | def           | Process                 | YES          |
| 'root'@'%' | def           | References              | YES          |
| 'root'@'%' | def           | Alter                   | YES          |
| 'root'@'%' | def           | Show Databases          | YES          |
| 'root'@'%' | def           | Super                   | YES          |
| 'root'@'%' | def           | Execute                 | YES          |
| 'root'@'%' | def           | Index                   | YES          |
| 'root'@'%' | def           | Create User             | YES          |
| 'root'@'%' | def           | Create Tablespace       | YES          |
| 'root'@'%' | def           | Trigger                 | YES          |
| 'root'@'%' | def           | Create View             | YES          |
| 'root'@'%' | def           | Show View               | YES          |
| 'root'@'%' | def           | Create Role             | YES          |
| 'root'@'%' | def           | Drop Role               | YES          |
| 'root'@'%' | def           | CREATE TEMPORARY TABLES | YES          |
| 'root'@'%' | def           | LOCK TABLES             | YES          |
| 'root'@'%' | def           | CREATE ROUTINE          | YES          |
| 'root'@'%' | def           | ALTER ROUTINE           | YES          |
| 'root'@'%' | def           | EVENT                   | YES          |
| 'root'@'%' | def           | SHUTDOWN                | YES          |
| 'root'@'%' | def           | RELOAD                  | YES          |
| 'root'@'%' | def           | FILE                    | YES          |
| 'root'@'%' | def           | CONFIG                  | YES          |
| 'root'@'%' | def           | REPLICATION CLIENT      | YES          |
| 'root'@'%' | def           | REPLICATION SLAVE       | YES          |
+------------+---------------+-------------------------+--------------+
31 rows in set (0.00 sec)
```

### ALTER

- 对于所有的 `ALTER` 语句，均需要用户对所操作的表拥有 `ALTER` 权限。
- 除 `ALTER...DROP` 和 `ALTER...RENAME TO` 外，均需要对所操作表拥有 `INSERT` 和 `CREATE` 权限。
- 对于 `ALTER...DROP` 语句，需要对表拥有 `DROP` 权限。
- 对于 `ALTER...RENAME TO` 语句，需要对重命名前的表拥有 `DROP` 权限，对重命名后的表拥有 `CREATE` 和 `INSERT` 权限。

> **注意：**
>
> 根据 MySQL 5.7 文档中的说明，对表进行 `ALTER` 操作需要 `INSERT` 和 `CREATE` 权限，但在 MySQL 5.7.25 版本实际情况中，该操作仅需要 `ALTER` 权限。目前，TiDB 中的 `ALTER` 权限与 MySQL 实际行为保持一致。

### BACKUP

需要拥有 `SUPER` 或者 `BACKUP_ADMIN` 权限。

### CANCEL IMPORT JOB

需要 `SUPER` 权限来取消属于其他用户的任务，否则只能取消当前用户创建的任务。

### CREATE DATABASE

需要拥有全局 `CREATE` 权限。

### CREATE INDEX

需要对所操作的表拥有 `INDEX` 权限。

### CREATE TABLE

需要对要创建的表所在的数据库拥有 `CREATE` 权限；若使用 `CREATE TABLE...LIKE...` 需要对相关的表拥有 `SELECT` 权限。

### CREATE VIEW

需要拥有 `CREATE VIEW` 权限。

> **注意：**
>
> 如果当前登录用户与创建视图的用户不同，除需要 `CREATE VIEW` 权限外，还需要 `SUPER` 权限。

### DROP DATABASE

需要对数据库拥有 `DROP` 权限。

### DROP INDEX

需要对所操作的表拥有 `INDEX` 权限。

### DROP TABLES

需要对所操作的表拥有 `DROP` 权限。

### IMPORT INTO

需要对目标表拥有 `SELECT`、`UPDATE`、`INSERT`、`DELETE` 和 `ALTER` 权限。如果是导入存储在 TiDB 本地的文件，还需要有 `FILE` 权限。

### LOAD DATA

`LOAD DATA` 需要对所操作的表拥有 `INSERT` 权限。执行 `REPLACE INTO` 语句还需要对所操作的表拥有 `DELETE` 权限。

### TRUNCATE TABLE

需要对所操作的表拥有 `DROP` 权限。

### RENAME TABLE

需要对重命名前的表拥有 `ALTER` 和 `DROP` 权限，对重命名后的表拥有 `CREATE` 和 `INSERT` 权限。

### ANALYZE TABLE

需要对所操作的表拥有 `INSERT` 和 `SELECT` 权限。

### LOCK STATS

需要对所操作的表拥有 `INSERT` 和 `SELECT` 权限。

### UNLOCK STATS

需要对所操作的表拥有 `INSERT` 和 `SELECT` 权限。

### SHOW

`SHOW CREATE TABLE` 需要任意一种权限。

`SHOW CREATE VIEW` 需要 `SHOW VIEW` 权限。

`SHOW GRANTS` 需要拥有对 `mysql` 数据库的 `SELECT` 权限。如果是使用 `SHOW GRANTS` 查看当前用户权限，则不需要任何权限。

`SHOW PROCESSLIST` 需要 `PROCESS` 权限来显示属于其他用户的连接。

`SHOW IMPORT JOB` 需要 `SUPER` 权限来显示属于其他用户的任务，否则只能看到当前用户创建的任务。

`SHOW STATS_LOCKED` 需要拥有 `mysql.stats_table_locked` 表的 `SELECT` 权限。

### CREATE ROLE/USER

`CREATE ROLE` 需要 `CREATE ROLE` 权限。

`CREATE USER` 需要 `CREATE USER` 权限

### DROP ROLE/USER

`DROP ROLE` 需要 `DROP ROLE` 权限。

`DROP USER` 需要 `CREATE USER` 权限

### ALTER USER

`ALTER USER` 需要 `CREATE USER` 权限。

### GRANT

`GRANT` 需要 `GRANT` 权限并且拥有 `GRANT` 所赋予的权限。

如果在 `GRANTS` 语句中创建用户，需要有 `CREATE USER` 权限。

`GRANT ROLE` 操作需要拥有 `SUPER` 或者 `ROLE_ADMIN` 权限。

### REVOKE

`REVOKE` 需要 `GRANT` 权限并且拥有 `REVOKE` 所指定要撤销的权限。

`REVOKE ROLE` 操作需要拥有 `SUPER` 或者 `ROLE_ADMIN` 权限。

### SET GLOBAL

使用 `SET GLOBAL` 设置全局变量需要拥有 `SUPER` 或者 `SYSTEM_VARIABLES_ADMIN` 权限。

### ADMIN

需要拥有 `SUPER` 权限。

### SET DEFAULT ROLE

需要拥有 `SUPER` 权限。

### KILL

使用 `KILL` 终止其他用户的会话需要拥有 `SUPER` 或者 `CONNECTION_ADMIN` 权限。

### CREATE RESOURCE GROUP

需要拥有 `SUPER` 或者 `RESOURCE_GROUP_ADMIN` 权限。

### ALTER RESOURCE GROUP

需要拥有 `SUPER` 或者 `RESOURCE_GROUP_ADMIN` 权限。

### DROP RESOURCE GROUP

需要拥有 `SUPER` 或者 `RESOURCE_GROUP_ADMIN` 权限。

### CALIBRATE RESOURCE

需要拥有 `SUPER` 或者 `RESOURCE_GROUP_ADMIN` 权限。

### SET RESOURCE GROUP

当系统变量 [`tidb_resource_control_strict_mode`](/system-variables.md#tidb_resource_control_strict_mode-从-v820-版本开始引入) 设置为 `ON` 时，你需要有 `SUPER` 或者 `RESOURCE_GROUP_ADMIN` 或者 `RESOURCE_GROUP_USER` 权限才能执行该语句。

### TRAFFIC CAPTURE

需要拥有 `SUPER` 或者 `TRAFFIC_CAPTURE_ADMIN` 权限。

### TRAFFIC REPLAY

需要拥有 `SUPER` 或者 `TRAFFIC_REPLAY_ADMIN` 权限。

### CANCEL TRAFFIC JOBS

取消捕获任务，需要拥有 `SUPER` 或者 `TRAFFIC_CAPTURE_ADMIN` 权限。

取消回放任务，需要拥有 `SUPER` 或者 `TRAFFIC_REPLAY_ADMIN` 权限。

### SHOW TRAFFIC JOBS

查看捕获任务，需要拥有 `SUPER` 或者 `TRAFFIC_CAPTURE_ADMIN` 权限。

查看回放任务，需要拥有 `SUPER` 或者 `TRAFFIC_REPLAY_ADMIN` 权限。

## 权限系统的实现

### 授权表

以下几张 [`mysql` 系统表](/mysql-schema/mysql-schema-user.md)是非常特殊的表，权限相关的数据全部存储在这几张表内。

- `mysql.user`：用户账户，全局权限
- `mysql.db`：数据库级别的权限
- `mysql.tables_priv`：表级别的权限
- `mysql.columns_priv`：列级别的权限，当前暂不支持

这几张表包含了数据的生效范围和权限信息。例如，`mysql.user` 表的部分数据：

```sql
SELECT User,Host,Select_priv,Insert_priv FROM mysql.user LIMIT 1;
```

```
+------|------|-------------|-------------+
| User | Host | Select_priv | Insert_priv |
+------|------|-------------|-------------+
| root | %    | Y           | Y           |
+------|------|-------------|-------------+
1 row in set (0.00 sec)
```

这条记录中，`Host` 和 `User` 决定了 root 用户从任意主机 (%) 发送过来的连接请求可以被接受，而 `Select_priv` 和 `Insert_priv` 表示用户拥有全局的 `Select` 和 `Insert` 权限。`mysql.user` 这张表里面的生效范围是全局的。

`mysql.db` 表里面包含的 `Host` 和 `User` 决定了用户可以访问哪些数据库，权限列的生效范围是数据库。

理论上，所有权限管理相关的操作，都可以通过直接对授权表的 CRUD 操作完成。

实现层面其实也只是包装了一层语法糖。例如删除用户会执行：

```sql
DELETE FROM mysql.user WHERE user='test';
```

但是，不推荐手动修改授权表，建议使用 `DROP USER` 语句：

```sql
DROP USER 'test';
```

### 连接验证

当客户端发送连接请求时，TiDB 服务器会对登录操作进行验证。验证过程先检查 `mysql.user` 表，当某条记录的 `User` 和 `Host` 和连接请求匹配上了，再去验证 `authentication_string`。用户身份基于两部分信息，发起连接的客户端的 `Host`，以及用户名 `User`。如果 `User` 不为空，则用户名必须精确匹配。

User+Host 可能会匹配 `user` 表里面多行，为了处理这种情况，`user` 表的行是排序过的，客户端连接时会依次去匹配，并使用首次匹配到的那一行做权限验证。排序是按 `Host` 在前，`User` 在后。

### 请求验证

连接成功之后，请求验证会检测执行操作是否拥有足够的权限。

对于数据库相关请求 (`INSERT`, `UPDATE`)，先检查 `mysql.user` 表里面的用户全局权限，如果权限够，则直接可以访问。如果全局权限不足，则再检查 `mysql.db` 表。

`user` 表的权限是全局的，并且不管默认数据库是哪一个。比如 `user` 里面有 `DELETE` 权限，任何一行，任何的表，任何的数据库。

`db`表里面，User 为空是匹配匿名用户，User 里面不能有通配符。Host 和 Db 列里面可以有 `%` 和 `_`，可以模式匹配。

`user` 和 `db` 读到内存也是排序的。

`tables_priv` 和 `columns_priv` 中使用 `%` 是类似的，但是在`Db`, `Table_name`, `Column_name` 这些列不能包含 `%`。加载进来时排序也是类似的。

### 生效时机

TiDB 启动时，会将一些权限检查的表加载到内存，之后使用缓存的数据来验证权限。执行权限管理语句（如 `GRANT`、`REVOKE`、`CREATE USER` 和 `DROP USER`）将立即生效。

使用 `INSERT`、`DELETE`、`UPDATE` 等语句手动修改 `mysql.user` 等授权表不会立即生效。该行为与 MySQL 兼容。如需立即生效，可以手动执行 [`FLUSH PRIVILEGES`](/sql-statements/sql-statement-flush-privileges.md) 语句更新权限的缓存。