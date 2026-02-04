---
title: 通过 MySQL 工具连接到 TiDB
summary: 介绍如何通过 MySQL 工具连接到 TiDB。
---

# 通过 MySQL 工具连接到 TiDB

**TiDB** 高度兼容 **MySQL** 协议，全量的客户端连接参数列表，请参阅 [MySQL Client Options](https://dev.mysql.com/doc/refman/8.0/en/mysql-command-options.html)。

TiDB 支持 [MySQL 客户端/服务器协议](https://dev.mysql.com/doc/dev/mysql-server/latest/PAGE_PROTOCOL.html)。这使得大多数客户端驱动程序和 ORM 框架可以像连接到 MySQL 一样地连接到 TiDB。

你可以选择使用 MySQL Client 或 MySQL Shell 连接到 TiDB。

<SimpleTab>

<div label="MySQL Client">

你可以使用 MySQL Client 作为 TiDB 的命令行工具连接到 TiDB。下面以基于 YUM 的 Linux 发行版为例，介绍如何安装 MySQL Client。

```shell
sudo yum install mysql
```

安装完成后，你可以使用如下命令连接到 TiDB：

```shell
mysql --host <tidb_server_host> --port 4000 -u root -p --comments
```

macOS 上的 MySQL v9.0 客户端无法正确加载 `mysql_native_password` 插件，导致连接 TiDB 时报错 `ERROR 2059 (HY000): Authentication plugin 'mysql_native_password' cannot be loaded`。为解决该问题，建议安装并使用 MySQL v8.0 客户端来连接 TiDB 。安装命令如下：

```shell
brew install mysql-client@8.0
brew unlink mysql
brew link mysql-client@8.0
```

如果仍然遇到问题，可以尝试指定 MySQL v8.0 客户端的安装路径来使用 MySQL v8.0 客户端连接 TiDB。连接命令如下：

```shell
/opt/homebrew/opt/mysql-client@8.0/bin/mysql --comments --host ${YOUR_IP_ADDRESS} --port ${YOUR_PORT_NUMBER} -u ${your_user_name} -p
```

请使用实际部署的 MySQL v8.0 客户端的安装路径替代上述命令中的 `/opt/homebrew/opt/mysql-client@8.0/bin/mysql`。

</div>

<div label="MySQL Shell">

你可以使用 MySQL Shell 作为 TiDB 的命令行工具连接到 TiDB。参考 [MySQL Shell 文档](https://dev.mysql.com/doc/mysql-shell/8.0/en/mysql-shell-install.html)进行安装。安装完成后，你可以使用如下命令连接到 TiDB：

```shell
mysqlsh --sql mysql://root@<tidb_server_host>:4000
```

</div>

</SimpleTab>