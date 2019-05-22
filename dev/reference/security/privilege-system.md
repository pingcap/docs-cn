---
title: 权限管理
category: reference
aliases: ['/docs-cn/sql/privilege/']
---

# 权限管理

TiDB 的权限管理系统按照 MySQL 的权限管理进行实现，TiDB 支持大部分的 MySQL 的语法和权限类型。

本文档主要介绍 TiDB 权限相关操作、各项操作需要的权限以及权限系统的实现。

## 权限相关操作

### 授予权限

授予 `xxx` 用户对数据库 `test` 的读权限：

```sql
GRANT SELECT ON test.* TO 'xxx'@'%';
```

为 `xxx` 用户授予所有数据库，全部权限：

```sql
GRANT ALL PRIVILEGES ON *.* TO 'xxx'@'%';
```

如果 `GRANT` 的目标用户不存在，TiDB 会自动创建用户。

```sql
mysql> SELECT * FROM mysql.user WHERE user='xxxx';
Empty set (0.00 sec)

mysql> GRANT ALL PRIVILEGES ON test.* TO 'xxxx'@'%' IDENTIFIED BY 'yyyyy';
Query OK, 0 rows affected (0.00 sec)

mysql> SELECT user,host FROM mysql.user WHERE user='xxxx';
+------|------+
| user | host |
+------|------+
| xxxx | %    |
+------|------+
1 row in set (0.00 sec)
```

上述示例中，`xxxx@%` 即自动添加的用户。

`GRANT` 对于数据库或者表的授权，不检查数据库或表是否存在。

```sql
mysql> SELECT * FROM test.xxxx;
ERROR 1146 (42S02): Table 'test.xxxx' doesn't exist

mysql> GRANT ALL PRIVILEGES ON test.xxxx TO xxxx;
Query OK, 0 rows affected (0.00 sec)

mysql> SELECT user,host FROM mysql.tables_priv WHERE user='xxxx';
+------|------+
| user | host |
+------|------+
| xxxx | %    |
+------|------+
1 row in set (0.00 sec)
```

`GRANT` 可以模糊匹配地授予数据库和表：

```sql
mysql> GRANT ALL PRIVILEGES ON `te%`.* TO genius;
Query OK, 0 rows affected (0.00 sec)

mysql> SELECT user,host,db FROM mysql.db WHERE user='genius';
+--------|------|-----+
| user   | host | db  |
+--------|------|-----+
| genius | %    | te% |
+--------|------|-----+
1 row in set (0.00 sec)
```

这个例子中通过 `%` 模糊匹配，所有 `te` 开头的数据库，都被授予了权限。

### 收回权限

`REVOKE` 语句与 `GRANT` 对应：

```sql
REVOKE ALL PRIVILEGES ON `test`.* FROM 'genius'@'localhost';
```

> **注意：**
>
> `REVOKE` 收回权限时只做精确匹配，若找不到记录则报错。而 `GRANT` 授予权限时可以使用模糊匹配。

```sql
mysql> REVOKE ALL PRIVILEGES ON `te%`.* FROM 'genius'@'%';
ERROR 1141 (42000): There is no such grant defined for user 'genius' on host '%'
```

关于模糊匹配和转义，字符串和 identifier：

```sql
mysql> GRANT ALL PRIVILEGES ON `te\%`.* TO 'genius'@'localhost';
Query OK, 0 rows affected (0.00 sec)
```

上述例子是精确匹配名为 `te%` 的数据库，注意使用 `\` 转义字符。

以单引号包含的部分，是一个字符串。以反引号包含的部分，是一个 identifier。注意下面的区别：

```sql
mysql> GRANT ALL PRIVILEGES ON 'test'.* TO 'genius'@'localhost';
ERROR 1064 (42000): You have an error in your SQL syntax; check the
manual that corresponds to your MySQL server version for the right
syntax to use near ''test'.* to 'genius'@'localhost'' at line 1

mysql> GRANT ALL PRIVILEGES ON `test`.* TO 'genius'@'localhost';
Query OK, 0 rows affected (0.00 sec)
```

如果想将一些特殊的关键字做为表名，可以用反引号包含起来。比如：

```sql
mysql> CREATE TABLE `select` (id int);
Query OK, 0 rows affected (0.27 sec)
```

### 查看为用户分配的权限

`SHOW GRANTS` 语句可以查看为用户分配了哪些权限。例如：

```sql
SHOW GRANTS; # 查看当前用户的权限
SHOW GRANTS for 'root'@'%'; # 查看某个特定用户的权限
```

更精确的方式，可以通过直接查看授权表的数据实现。比如想知道，名为 `test@%` 的用户是否拥有对 `db1.t` 的 `Insert` 权限：

1. 先查看该用户是否拥有全局 `Insert` 权限：

    ```sql
    SELECT Insert_priv FROM mysql.user WHERE user='test' AND host='%';
    ```

2. 如果没有，再查看该用户是否拥有 `db1` 数据库级别的 `Insert` 权限：

    ```sql
    SELECT Insert_priv FROM mysql.db WHERE user='test' AND host='%';
    ```

3. 如果仍然没有，则继续判断是否拥有 `db1.t` 这张表的 `Insert` 权限：

    ```sql
    SELECT table_priv FROM mysql.tables_priv WHERE user='test' AND host='%' AND db='db1';
    ```

## TiDB 各操作需要的权限

TiDB 用户目前拥有的权限可以在 `INFORMATION_SCHEMA.USER_PRIVILEGES` 表中查找到。

| 权限类型       |  权限变量名    | 权限简述                 |
| :------------ | :------------ | :---------------------- |
| ALL            | AllPriv        | 所有权限                 |
| Drop           | DropPriv       | 删除 schema/table        |
| Index          | IndexPriv      | 创建/删除 index          |
| Alter          | AlterPriv      | 执行 `ALTER` 语句          |
| Super          | SuperPriv      | 所有权限                 |
| Grant          | GrantPriv      | 授予其他用户权限         |
| Create         | CreatePriv     | 创建 schema/table        |
| Select         | SelectPriv     | 读取表内容               |
| Insert         | InsertPriv     | 插入数据到表             |
| Update         | UpdatePriv     | 更新表中数据             |
| Delete         | DeletePriv     | 删除表中数据             |
| Trigger        | TriggerPriv    | 尚未使用                 |
| Process        | ProcessPriv    | 显示正在运行的任务       |
| Execute        | ExecutePriv    | 执行 execute 语句        |
| Drop Role      | DropRolePriv   | 执行 drop role           |
| Show View      | ShowViewPriv   | 执行 show create view    |
| References     | ReferencesPriv | 尚未使用                 |
| Create View    | CreateViewPriv | 创建视图                 |
| Create User    | CreateUserPriv | 创建用户                 |
| Create Role    | CreateRolePriv | 执行 create role         |
| Show Databases | ShowDBPriv     | 显示 database 内的表情况 |

### ALTER

- 对于所有的 `ALTER` 语句，均需要用户对所操作的表拥有 `ALTER` 权限。
- 除 `ALTER...DROP` 和 `ALTER...RENAME TO` 外，均需要对所操作表拥有 `INSERT` 和 `CREATE` 权限。
- 对于 `ALTER...DROP` 语句，需要对表拥有 `DROP` 权限。
- 对于 `ALTER...RENAME TO` 语句，需要对重命名前的表拥有 `DROP` 权限，对重命名后的表拥有 `CREATE` 和 `INSERT` 权限。

> **注意：**
>
> 根据 MySQL 5.7 文档中的说明，对表进行 `ALTER` 操作需要 `INSERT` 和 `CREATE` 权限，但在 MySQL 5.7.25 版本实际情况中，该操作仅需要 `ALTER` 权限。目前，TiDB 中的 `ALTER` 权限与 MySQL 实际行为保持一致。

### CREATE DATABASE

需要对数据库拥有 `CREATE` 权限。

### CREATE INDEX

需要对所操作的表拥有 `INDEX` 权限。

### CREATE TABLE

需要对所操作的表拥有 `CREATE` 权限；若使用 `CREATE TABLE...LIKE...` 需要对相关的表拥有 `SELECT` 权限。

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

### TRUNCATE TABLE

需要对所操作的表拥有 `DROP` 权限。

### RENAME TABLE

需要对重命名前的表拥有 `ALTER` 和 `DROP` 权限，对重命名后的表拥有 `CREATE` 和 `INSERT` 权限。

### ANALYZE TABLE

需要对所操作的表拥有 `INSERT` 和 `SELECT` 权限。

### SHOW

`SHOW CREATE TABLE` 需要任意一种权限。

`SHOW CREATE VIEW` 需要 `SHOW VIEW` 权限。

### CREATE ROLE/USER

`CREATE ROLE` 需要 `CREATE ROLE` 权限。

`CREATE USER` 需要 `CREATE USER` 权限

### DROP ROLE/USER

`DROP ROLE` 需要 `DROPROLE` 权限。

`DROP USER` 需要 `CREATEUSER` 权限

### ALTER USER

`ALTER USER` 需要 `CREATEUSER` 权限。

### GRANT

`GRANT` 需要 `GRANT` 权限并且拥有 `GRANT` 所赋予的权限。

### REVOKE

`REVOKE` 需要 `SUPER` 权限。

## 权限系统的实现

### 授权表

以下几张系统表是非常特殊的表，权限相关的数据全部存储在这几张表内。

- `mysql.user`：用户账户，全局权限
- `mysql.db`：数据库级别的权限
- `mysql.tables_priv`：表级别的权限
- `mysql.columns_priv`：列级别的权限，当前暂不支持

这几张表包含了数据的生效范围和权限信息。例如，`mysql.user` 表的部分数据：

```sql
mysql> SELECT User,Host,Select_priv,Insert_priv FROM mysql.user LIMIT 1;
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

当客户端发送连接请求时，TiDB 服务器会对登录操作进行验证。验证过程先检查 `mysql.user` 表，当某条记录的 `User` 和 `Host` 和连接请求匹配上了，再去验证 Password。用户身份基于两部分信息，发起连接的客户端的 `Host`，以及用户名 `User`。如果 `User` 不为空，则用户名必须精确匹配。

User+Host 可能会匹配 `user` 表里面多行，为了处理这种情况，`user` 表的行是排序过的，客户端连接时会依次去匹配，并使用首次匹配到的那一行做权限验证。排序是按 `Host` 在前，`User` 在后。

### 请求验证

连接成功之后，请求验证会检测执行操作是否拥有足够的权限。

对于数据库相关请求 (`INSERT`，`UPDATE`)，先检查 `mysql.user` 表里面的用户全局权限，如果权限够，则直接可以访问。如果全局权限不足，则再检查 `mysql.db` 表。

`user` 表的权限是全局的，并且不管默认数据库是哪一个。比如 `user` 里面有 `DELETE` 权限，任何一行，任何的表，任何的数据库。

`db`表里面，User 为空是匹配匿名用户，User 里面不能有通配符。Host 和 Db 列里面可以有 `%` 和 `_`，可以模式匹配。

`user` 和 `db` 读到内存也是排序的。

`tables_priv` 和 `columns_priv` 中使用 `%` 是类似的，但是在`Db`, `Table_name`, `Column_name` 这些列不能包含 `%`。加载进来时排序也是类似的。

### 生效时机

TiDB 启动时，将一些权限检查的表加载到内存，之后使用缓存的数据来验证权限。系统会周期性的将授权表从数据库同步到缓存，生效则是由同步的周期决定，目前这个值设定的是 5 分钟。

修改了授权表，如果需要立即生效，可以手动调用：

```sql
FLUSH PRIVILEGES;
```

### 限制和约束

一些使用频率偏低的权限当前版本的实现中还未做检查，比如 `FILE`/`USAGE`/`SHUTDOWN`/`EXECUTE`/`PROCESS`/`INDEX` 等等，未来会陆续完善。

现阶段对权限的支持还没有做到 column 级别。
