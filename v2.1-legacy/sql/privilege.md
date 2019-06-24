---
title: 权限管理
category: user guide
---

# 权限管理

## 权限管理概述

TiDB 的权限管理系统是按照 MySQL 的权限管理进行实现，大部分的 MySQL 的语法和权限类型都是支持的。如果发现行为跟 MySQL 不一致的地方，欢迎[提 issue](https://github.com/pingcap/tidb/issues/new/choose)。

## 示例

### 用户账户操作

TiDB 的用户账户名由一个用户名和一个主机名组成。账户名的语法为 `'user_name'@'host_name'`。

- `user_name` 大小写敏感。
- `host_name` 可以是一个主机名或 IP 地址。主机名或 IP 地址中允许使用通配符 `%` 和 `_`。例如，名为 `'%'` 的主机名可以匹配所有主机，`'192.168.1.%'` 可以匹配子网中的所有主机。

#### 添加用户

```sql
CREATE USER 'test'@'127.0.0.1' IDENTIFIED BY 'xxx';
```

host 支持模糊匹配，比如：

```sql
CREATE USER 'test'@'192.168.10.%';
```

允许 `test` 用户从 `192.168.10` 子网的任何一个主机登录。

如果没有指定 host，则默认是所有 IP 均可登录。如果没有指定密码，默认为空：

```sql
CREATE USER 'test';
```

等价于

```sql
CREATE USER 'test'@'%' IDENTIFIED BY '';
```

#### 更改密码

```sql
SET PASSWORD FOR 'root'@'%' = 'xxx';
```

#### 删除用户

```sql
DROP USER 'test'@'%';
```

这个操作会清除用户在 `mysql.user` 表里面的记录项，并且清除在授权表里面的相关记录。

#### 忘记 root 密码

使用一个特殊的启动参数启动 TiDB（需要 root 权限）：

```bash
sudo ./tidb-server -skip-grant-table=true
```

这个参数启动，TiDB 会跳过权限系统，然后使用 root 登录以后修改密码：

```bash
mysql -h 127.0.0.1 -P 4000 -u root
```

### 权限相关操作

#### 授予权限

授予 `xxx` 用户对数据库 `test` 的读权限：

```sql
GRANT SELECT ON test.* TO 'xxx'@'%';
```

为 test 用户授予所有数据库，全部权限：

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

例子中 `xxxx@%` 就是自动添加进去的用户。

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

#### 收回权限

`REVOKE` 语句与 `GRANT` 对应：

```sql
REVOKE ALL PRIVILEGES ON `test`.* FROM 'genius'@'localhost';
```

> **注意：**
>
> revoke 收回权限时只做精确匹配，若找不到记录则报错。而 grant 授予权限时可以使用模糊匹配。

```sql
mysql> REVOKE ALL PRIVILEGES ON `te%`.* FROM 'genius'@'%';
ERROR 1141 (42000): There is no such grant defined for user 'genius' on host '%'
```

关于模糊匹配和转义，字符串和 identifier：

```sql
mysql> GRANT ALL PRIVILEGES ON `te\%`.* TO 'genius'@'localhost';
Query OK, 0 rows affected (0.00 sec)
```

上述例子是精确匹配名叫 `te%` 的数据库，注意使用 `\` 转义字符。

以单引号包含的，是一个字符串。以反引号包含的，是一个 identifier。注意下面的区别：

```sql
mysql> GRANT ALL PRIVILEGES ON 'test'.* TO 'genius'@'localhost';
ERROR 1064 (42000): You have an error in your SQL syntax; check the
manual that corresponds to your MySQL server version for the right
syntax to use near ''test'.* to 'genius'@'localhost'' at line 1

mysql> GRANT ALL PRIVILEGES ON `test`.* TO 'genius'@'localhost';
Query OK, 0 rows affected (0.00 sec)
```

如果一些特殊的关键字想做为表名，可以用反引号包含起来。比如：

```sql
mysql> CREATE TABLE `select` (id int);
Query OK, 0 rows affected (0.27 sec)
```

#### 查看为用户分配的权限

`SHOW GRANTS` 语句可以查看为用户分配了哪些权限。例如：

```sql
SHOW GRANTS; # 查看当前用户的权限
SHOW GRANTS for 'root'@'%'; # 查看某个特定用户的权限
```

更精确的方式，可以通过直接查看授权表的数据实现。比如想知道，`test@%` 该用户是否拥有对 `db1.t` 的 `Insert` 权限。

先查看该用户是否拥有全局 `Insert` 权限：

```sql
SELECT Insert_priv FROM mysql.user WHERE user='test' AND host='%';
```

如果没有，再查看该用户是否拥有 `db1` 数据库级别的 `Insert` 权限：

```sql
SELECT Insert_priv FROM mysql.db WHERE user='test' AND host='%';
```

如果仍然没有，则继续判断是否拥有 `db1.t` 这张表的 `Insert` 权限：

```sql
SELECT table_priv FROM mysql.tables_priv WHERE user='test' AND host='%' AND db='db1';
```

### 权限系统的实现

#### 授权表

有几张系统表是非常特殊的表，权限相关的数据全部存储在这几张表内。

- mysql.user 用户账户，全局权限
- mysql.db 数据库级别的权限
- mysql.tables_priv 表级别的权限
- mysql.columns_priv 列级别的权限，当前暂不支持

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

这条记录中，Host 和 User 决定了 root 用户从任意主机（%）发送过来的连接请求可以被接受，而 `Select_priv` 和 `Insert_priv` 表示用户拥有全局的 `Select` 和 `Insert` 权限。`mysql.user` 这张表里面的生效范围是全局的。

`mysql.db` 表里面包含的 Host 和 User 决定了用户可以访问哪些数据库，权限列的生效范围是数据库。

理论上，所有权限管理相关的操作，都可以通过直接对授权表的 CRUD 操作完成。

实现层面其实也只是包装了一层语法糖。例如删除用户会执行：

```sql
DELETE FROM mysql.user WHERE user='test';
```

但是，不推荐手动修改授权表，建议使用 `DROP USER` 语句：

```sql
DROP USER 'test';
```

#### 连接验证

当客户端发送连接请求时，TiDB 服务器会对登录操作进行验证。验证过程先检查 `mysql.user` 表，当某条记录的 User 和 Host 和连接请求匹配上了，再去验证 Password。用户身份基于两部分信息，发起连接的客户端的 Host，以及用户名 User。如果 User不为空，则用户名必须精确匹配。

User+Host 可能会匹配 `user` 表里面多行，为了处理这种情况，`user` 表的行是排序过的，客户端连接时会依次去匹配，并使用首次匹配到的那一行做权限验证。排序是按 Host 在前，User 在后。

#### 请求验证

连接成功之后，请求验证会检测执行操作是否拥有足够的权限。

对于数据库相关请求 (`INSERT`，`UPDATE`)，先检查 `mysql.user` 表里面的用户全局权限，如果权限够，则直接可以访问。如果全局权限不足，则再检查 `mysql.db` 表。

`user` 表的权限是全局的，并且不管默认数据库是哪一个。比如 `user` 里面有 DELETE 权限，任何一行，任何的表，任何的数据库。

`db`表里面，User 为空是匹配匿名用户，User 里面不能有通配符。Host 和 Db 列里面可以有 `%` 和 `_`，可以模式匹配。

`user` 和 `db` 读到内存也是排序的。

`tables_priv` 和 `columns_priv` 中使用 `%` 是类似的，但是在`Db`, `Table_name`, `Column_name` 这些列不能包含 `%`。加载进来时排序也是类似的。

#### 生效时机

TiDB 启动时，将一些权限检查的表加载到内存，之后使用缓存的数据来验证权限。系统会周期性的将授权表从数据库同步到缓存，生效则是由同步的周期决定，目前这个值设定的是5分钟。

修改了授权表，如果需要立即生效，可以手动调用：

```sql
FLUSH PRIVILEGES;
```

### 限制和约束

一些使用频率偏低的权限当前版本的实现中还未做检查，比如 FILE/USAGE/SHUTDOWN/EXECUTE/PROCESS/INDEX 等等，未来会陆续完善。

现阶段对权限的支持还没有做到 column 级别。

## CREATE USER 语句

```sql
CREATE USER [IF NOT EXISTS]
    user [auth_spec] [, user [auth_spec]] ...
auth_spec: {
    IDENTIFIED BY 'auth_string'
  | IDENTIFIED BY PASSWORD 'hash_string'
}
```

User 参见[用户账号名](../sql/user-account-management.md)。

* `IDENTIFIED BY 'auth_string'`：设置登录密码时，`auth_string` 会被 TiDB 经过加密存储在 `mysql.user` 表中。
* `IDENTIFIED BY PASSWORD 'hash_string'`：设置登录密码，`hash_string` 是一个类似于 `*EBE2869D7542FCE37D1C9BBC724B97BDE54428F1` 的 41 位字符串，会被 TiDB 直接存储在 `mysql.user` 表中，该字符串可以通过 `SELECT password('auth_string')` 加密得到。