---
title: TiDB 用户账户管理
category: user guide
---

# TiDB 用户账户管理

## 用户名和密码

TiDB 将用户账户存储在 `mysql.user` 系统表里面。每个账户由用户名和 host 作为标识。每个账户可以设置一个密码。

通过 MySQL 客户端连接到 TiDB 服务器，通过指定的账户和密码登录：

```
shell> mysql --port 4000 --user xxx --password
```

使用缩写的命令行参数则是：

```
shell> mysql -P 4000 -u xxx -p
```

## 添加用户

添加用户有两种方式：

* 通过标准的用户管理的 SQL 语句创建用户以及授予权限，比如 `CREATE USER` 和 `GRANT` 。
* 直接通过 `INSERT` ， `UPDATE` 和 `DELETE` 操作授权表。

推荐的方式是使用第一种。第二种方式修改容易导致一些不完整的修改，因此不推荐。还有另一种可选方式是使用第三方工具的图形化界面工具。

下面的例子用 `CREATE USER` 和 `GRANT` 语句创建了四个账户：

```
mysql> CREATE USER 'finley'@'localhost' IDENTIFIED BY 'some_pass';
mysql> GRANT ALL PRIVILEGES ON *.* TO 'finley'@'localhost' WITH GRANT OPTION;
mysql> CREATE USER 'finley'@'%' IDENTIFIED BY 'some_pass';
mysql> GRANT ALL PRIVILEGES ON *.* TO 'finley'@'%' WITH GRANT OPTION;
mysql> CREATE USER 'admin'@'localhost' IDENTIFIED BY 'admin_pass';
mysql> GRANT RELOAD,PROCESS ON *.* TO 'admin'@'localhost';
mysql> CREATE USER 'dummy'@'localhost';
```

使用 `SHOW GRANTS` 可以看到为一个用户授予的权限：

```
mysql> SHOW GRANTS FOR 'admin'@'localhost';
+-----------------------------------------------------+
| Grants for admin@localhost                          |
+-----------------------------------------------------+
| GRANT RELOAD, PROCESS ON *.* TO 'admin'@'localhost' |
+-----------------------------------------------------+
```

## 删除用户

使用 `DROP USER` 语句可以删除用户，例如：

```
mysql> DROP USER 'jeffrey'@'localhost';
```

## 保留用户账户

TiDB 在数据库初始化时会生成一个 `'root'@'%'` 的默认账户。

## 设置资源限制

暂不支持。

## 设置密码

TiDB 将密码存在 `mysql.user` 系统数据库里面。只有拥有 `CREATE USER` 权限，或者拥有 `mysql` 数据库权限（ `INSERT` 权限用于创建， `UPDATE` 权限用于更新）的用户才能够设置或修改密码。

在 `CREATE USER` 创建用户时可以通过 `IDENTIFIED BY` 指定密码：

```sql
CREATE USER 'jeffrey'@'localhost' IDENTIFIED BY 'mypass';
```

为一个已存在的账户修改密码，可以通过 `SET PASSWORD FOR` 或者 `ALTER USER` 语句完成：

```sql
SET PASSWORD FOR 'root'@'%' = 'xxx';
```

或者

```sql
ALTER USER 'jeffrey'@'localhost' IDENTIFIED BY 'mypass';
```
