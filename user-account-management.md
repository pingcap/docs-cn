---
title: TiDB 用户账户管理
summary: TiDB 用户账户管理主要包括用户名和密码设置、添加用户、删除用户、保留用户账户、设置资源限制、设置密码、忘记密码处理和刷新权限。用户可以通过 SQL 语句或图形化界面工具进行用户管理，同时可以使用 `FLUSH PRIVILEGES` 命令立即生效修改。 TiDB 在数据库初始化时会生成一个默认账户。
---

# TiDB 用户账户管理

本文档主要介绍如何管理 TiDB 用户账户。

要快速了解 TiDB 如何进行认证与赋权并创建与管理用户账户，建议先观看下面的培训视频（时长 22 分钟）。注意本视频只作为学习参考，如需了解具体的用户账户管理方法，请参考本文档的内容。

<video src="https://download.pingcap.com/docs-cn%2FLesson11_security.mp4" width="600px" height="450px" controls="controls" poster="https://download.pingcap.com/docs-cn/poster_lesson11.png"></video>

## 用户名和密码

TiDB 将用户账户存储在 [`mysql.user`](/mysql-schema/mysql-schema-user.md) 系统表里面。每个账户由用户名和 host 作为标识。每个账户可以设置一个密码。每个用户名最长为 32 个字符。

通过 MySQL 客户端连接到 TiDB 服务器，通过指定的账户和密码登录：

```shell
mysql --port 4000 --user xxx --password
```

使用缩写的命令行参数则是：

```shell
mysql -P 4000 -u xxx -p
```

## 添加用户

添加用户有两种方式：

* 通过标准的用户管理的 SQL 语句创建用户以及授予权限，比如 [`CREATE USER`](/sql-statements/sql-statement-create-user.md) 和 [`GRANT`](/sql-statements/sql-statement-grant-privileges.md)。
* 直接通过[`INSERT`](/sql-statements/sql-statement-insert.md)、[`UPDATE`](/sql-statements/sql-statement-update.md) 和 [`DELETE`](/sql-statements/sql-statement-delete.md) 操作授权表，然后执行 [`FLUSH PRIVILEGES`](/sql-statements/sql-statement-flush-privileges.md)。不推荐使用这种方式添加或修改用户，因为容易导致修改不完整。

除以上两种方法外，你还可以使用[第三方图形化界面工具](/develop/dev-guide-third-party-support.md#gui)来添加用户。

```sql
CREATE USER [IF NOT EXISTS] user [IDENTIFIED BY 'auth_string'];
```

设置登录密码后，`auth_string` 会被 TiDB 加密并存储在 [`mysql.user`](/mysql-schema/mysql-schema-user.md) 表中。

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

等价于：

```sql
CREATE USER 'test'@'%' IDENTIFIED BY '';
```

为一个不存在的用户授权时，是否会自动创建用户的行为受 [`sql_mode`](/system-variables.md#sql_mode) 影响。如果 `sql_mode` 中包含 `NO_AUTO_CREATE_USER`，则 `GRANT` 不会自动创建用户并报错。

假设 `sql_mode` 不包含 `NO_AUTO_CREATE_USER`，下面的例子用 `CREATE USER` 和 `GRANT` 语句创建了四个账户：

```sql
CREATE USER 'finley'@'localhost' IDENTIFIED BY 'some_pass';
```

```sql
GRANT ALL PRIVILEGES ON *.* TO 'finley'@'localhost' WITH GRANT OPTION;
```

```sql
CREATE USER 'finley'@'%' IDENTIFIED BY 'some_pass';
```

```sql
GRANT ALL PRIVILEGES ON *.* TO 'finley'@'%' WITH GRANT OPTION;
```

```sql
CREATE USER 'admin'@'localhost' IDENTIFIED BY 'admin_pass';
```

```sql
GRANT RELOAD,PROCESS ON *.* TO 'admin'@'localhost';
```

```sql
CREATE USER 'dummy'@'localhost';
```

使用 [`SHOW GRANTS`](/sql-statements/sql-statement-show-grants.md) 可以看到为一个用户授予的权限：

```sql
SHOW GRANTS FOR 'admin'@'localhost';
```

```
+-----------------------------------------------------+
| Grants for admin@localhost                          |
+-----------------------------------------------------+
| GRANT RELOAD, PROCESS ON *.* TO 'admin'@'localhost' |
+-----------------------------------------------------+
```

使用 [`SHOW CREATE USER`](/sql-statements/sql-statement-show-create-user.md) 查看用户的定义语句：

```sql
SHOW CREATE USER 'admin'@'localhost';
```

```
+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| CREATE USER for admin@localhost                                                                                                                                                                                                      |
+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| CREATE USER 'admin'@'localhost' IDENTIFIED WITH 'mysql_native_password' AS '*14E65567ABDB5135D0CFD9A70B3032C179A49EE7' REQUIRE NONE PASSWORD EXPIRE DEFAULT ACCOUNT UNLOCK PASSWORD HISTORY DEFAULT PASSWORD REUSE INTERVAL DEFAULT  |
+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

## 删除用户

使用 [`DROP USER`](/sql-statements/sql-statement-drop-user.md) 语句可以删除用户，例如：

```sql
DROP USER 'test'@'localhost';
```

这个操作会清除用户在 [`mysql.user`](/mysql-schema/mysql-schema-user.md) 表里面的记录项，并且清除在授权表里面的相关记录。

## 保留用户账户

TiDB 在数据库初始化时会生成一个 `'root'@'%'` 的默认账户。

## 设置资源限制

TiDB 可以利用资源组对用户消耗的资源进行限制，详情参见[使用资源管控 (Resource Control) 实现资源组限制和流控](/tidb-resource-control-ru-groups.md)。

## 设置密码

TiDB 将密码存在 [`mysql.user`](/mysql-schema/mysql-schema-user.md) 系统表里面。只有拥有 `CREATE USER` 权限，或者拥有 `mysql` 数据库权限（`INSERT` 权限用于创建，`UPDATE` 权限用于更新）的用户才能够设置或修改密码。

- 在 [`CREATE USER`](/sql-statements/sql-statement-create-user.md) 创建用户时通过 `IDENTIFIED BY` 指定密码：

    ```sql
    CREATE USER 'test'@'localhost' IDENTIFIED BY 'mypass';
    ```

- 为一个已存在的账户修改密码，可以通过 [`SET PASSWORD FOR`](/sql-statements/sql-statement-set-password.md) 或者 [`ALTER USER`](/sql-statements/sql-statement-alter-user.md) 语句完成：

    ```sql
    SET PASSWORD FOR 'root'@'%' = 'xxx';
    ```

    或者：

    ```sql
    ALTER USER 'test'@'localhost' IDENTIFIED BY 'mypass';
    ```

## 忘记 `root` 密码

1. 修改 TiDB 配置文件：

    1. 登录其中一台 tidb-server 实例所在的机器。
    2. 进入 TiDB 节点的部署目录下的 `conf` 目录，找到 `tidb.toml` 配置文件。
    3. 在配置文件的 [`security`](/tidb-configuration-file.md#security) 部分添加配置项 [`skip-grant-table`](/tidb-configuration-file.md)。如无 `security` 部分，则将以下两行内容添加至 `tidb.toml` 配置文件尾部：

        ```
        [security]
        skip-grant-table = true
        ```

2. 终止该 tidb-server 的进程：

    1. 查看 tidb-server 的进程：

        ```bash
        ps aux | grep tidb-server
        ```

    2. 找到 tidb-server 对应的进程 ID (PID) 并使用 `kill` 命令停掉该进程：

        ```bash
        kill -9 <pid>
        ```

3. 使用修改之后的配置启动 TiDB：

    > **注意：**
    >
    > 设置 `skip-grant-table` 之后，启动 TiDB 进程会增加操作系统用户检查，只有操作系统的 `root` 用户才能启动 TiDB 进程。

    1. 进入 TiDB 节点部署目录下的 `scripts` 目录。
    2. 切换到操作系统 `root` 账号。
    3. 在前台执行目录中的 `run_tidb.sh` 脚本。
    4. 在新的终端窗口中使用 `root` 登录后修改密码：

        ```bash
        mysql -h 127.0.0.1 -P 4000 -u root
        ```

4. 停止运行 `run_tidb.sh` 脚本，并去掉第 1 步中在 TiDB 配置文件中添加的内容，等待 tidb-server 自启动。

## `FLUSH PRIVILEGES`

用户以及权限相关的信息都存储在 TiKV 服务器中，TiDB 在进程内部会缓存这些信息。一般通过 [`CREATE USER`](/sql-statements/sql-statement-create-user.md)、[`GRANT`](/sql-statements/sql-statement-grant-privileges.md) 等语句来修改相关信息时，可在整个集群迅速生效。如果遇到网络或者其它因素影响，由于 TiDB 会周期性地更新缓存信息，正常情况下，最多 15 分钟左右生效。

如果授权表已被直接修改，则不会通知 TiDB 节点更新缓存，执行 [`FLUSH PRIVILEGES`](/sql-statements/sql-statement-flush-privileges.md) 可使改动立即生效。

详情参见[权限管理](/privilege-management.md)。
