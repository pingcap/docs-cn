---
title: TiDB 用户账户管理
category: reference
aliases: ['/docs-cn/sql/user-account-management/']
---

# TiDB 用户账户管理

本文档主要介绍如何管理 TiDB 用户账户。

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

* 通过标准的用户管理的 SQL 语句创建用户以及授予权限，比如 `CREATE USER` 和 `GRANT`。
* 直接通过 `INSERT`、`UPDATE` 和 `DELETE` 操作授权表。

推荐使用第一种方式。第二种方式修改容易导致一些不完整的修改，因此不推荐。还有另一种可选方式是使用第三方工具的图形化界面工具。

```sql
CREATE USER [IF NOT EXISTS]
    user [auth_spec] [, user [auth_spec]] ...
auth_spec: {
    IDENTIFIED BY 'auth_string'
  | IDENTIFIED BY PASSWORD 'hash_string'
}
```

* `IDENTIFIED BY 'auth_string'`：设置登录密码时，`auth_string` 会被 TiDB 经过加密存储在 `mysql.user` 表中。
* `IDENTIFIED BY PASSWORD 'hash_string'`：设置登录密码，`hash_string` 是一个类似于 `*EBE2869D7542FCE37D1C9BBC724B97BDE54428F1` 的 41 位字符串，会被 TiDB 直接存储在 `mysql.user` 表中，该字符串可以通过 `SELECT password('auth_string')` 加密得到。

```sql
CREATE USER 'test'@'127.0.0.1' IDENTIFIED BY 'xxx';
```

TiDB 的用户账户名由一个用户名和一个主机名组成。账户名的语法为 `'user_name'@'host_name'`。

- `user_name` 大小写敏感。
- `host_name` 可以是一个主机名或 IP 地址。主机名或 IP 地址中允许使用通配符 `%` 和 `_`。例如，名为 `'%'` 的主机名可以匹配所有主机，`'192.168.1.%'` 可以匹配子网中的所有主机。

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

```sql
mysql> SHOW GRANTS FOR 'admin'@'localhost';
+-----------------------------------------------------+
| Grants for admin@localhost                          |
+-----------------------------------------------------+
| GRANT RELOAD, PROCESS ON *.* TO 'admin'@'localhost' |
+-----------------------------------------------------+
```

## 删除用户

使用 `DROP USER` 语句可以删除用户，例如：

```sql
mysql> DROP USER 'test'@'localhost';
```

这个操作会清除用户在 `mysql.user` 表里面的记录项，并且清除在授权表里面的相关记录。

## 保留用户账户

TiDB 在数据库初始化时会生成一个 `'root'@'%'` 的默认账户。

## 设置资源限制

暂不支持。

## 设置密码

TiDB 将密码存在 `mysql.user` 系统数据库里面。只有拥有 `CREATE USER` 权限，或者拥有 `mysql` 数据库权限（`INSERT` 权限用于创建，`UPDATE` 权限用于更新）的用户才能够设置或修改密码。

- 在 `CREATE USER` 创建用户时可以通过 `IDENTIFIED BY` 指定密码：

    ```sql
    CREATE USER 'test'@'localhost' IDENTIFIED BY 'mypass';
    ```

- 为一个已存在的账户修改密码，可以通过 `SET PASSWORD FOR` 或者 `ALTER USER` 语句完成：

    ```sql
    SET PASSWORD FOR 'root'@'%' = 'xxx';
    ```

    或者

    ```sql
    ALTER USER 'test'@'localhost' IDENTIFIED BY 'mypass';
    ```

## 忘记 `root` 密码

1. 修改配置文件，在 `security` 部分添加 `skip-grant-table`：

    > [security]
    > skip-grant-table = true

2. 使用修改后的配置启动 TiDB（需要 `root` 权限）：

    ```bash
    sudo ./tidb-server -skip-grant-table=true -store=tikv -path=...
    ```

    这个配置参数会让 TiDB 跳过权限系统。

3. 然后使用 `root` 登录后修改密码：

    ```bash
    mysql -h 127.0.0.1 -P 4000 -u root
    ```

## `FLUSH PRIVILEGES` 

如果授权表已被直接修改，运行如下命令可使改动立即生效：

```sql
FLUSH PRIVILEGES;
```

详情参见[权限管理](/dev/reference/security/privilege-system.md)。
