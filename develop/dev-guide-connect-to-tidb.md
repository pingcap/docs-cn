---
title: 连接到 TiDB
summary: 介绍连接到 TiDB 的方法。
---

# 连接到 TiDB

**TiDB** 高度兼容 **MySQL** 协议，全量的客户端连接参数列表，请参阅 [MySQL Client Options](https://dev.mysql.com/doc/refman/8.0/en/mysql-command-options.html)。

TiDB 支持 [MySQL 客户端/服务器协议](https://dev.mysql.com/doc/dev/mysql-server/latest/PAGE_PROTOCOL.html)。这使得大多数客户端驱动程序和 ORM 框架可以像连接到 MySQL 一样地连接到 TiDB。

## MySQL

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

## JDBC

你可以使用 [JDBC](https://dev.mysql.com/doc/connector-j/en/) 驱动连接到 TiDB，这需要创建一个 `MysqlDataSource` 或 `MysqlConnectionPoolDataSource` 对象（它们都实现了 `DataSource` 接口），并使用 `setURL` 函数设置连接字符串。

例如：

```java
MysqlDataSource mysqlDataSource = new MysqlDataSource();
mysqlDataSource.setURL("jdbc:mysql://{host}:{port}/{database}?user={username}&password={password}");
```

有关 JDBC 连接的更多信息，可参考 [JDBC 官方文档](https://dev.mysql.com/doc/connector-j/en/)。

**连接参数**

|    参数名    |                                                描述                                                |
| :----------: | :------------------------------------------------------------------------------------------------: |
| `{username}` | 需要连接到 TiDB 集群的 [SQL 用户](/user-account-management.md) |
| `{password}` |                               需要连接到 TiDB 集群的 SQL 用户的密码                                |
|   `{host}`   |               TiDB 节点运行的 [Host](<https://en.wikipedia.org/wiki/Host_(network)>)               |
|   `{port}`   |                                      TiDB 节点正在监听的端口                                       |
| `{database}` |                                      (已经存在的)数据库的名称                                      |

## Hibernate

你可以使用 [Hibernate ORM](https://hibernate.org/orm/) 连接到 TiDB，请将 Hibernate 的配置中的 `hibernate.connection.url` 设置为合法的 TiDB 连接字符串。

例如，你的配置被写在 `hibernate.cfg.xml` 文件中，那么你的配置文件应该为：

```xml
<?xml version='1.0' encoding='utf-8'?>
<!DOCTYPE hibernate-configuration PUBLIC
        "-//Hibernate/Hibernate Configuration DTD 3.0//EN"
        "http://www.hibernate.org/dtd/hibernate-configuration-3.0.dtd">
<hibernate-configuration>
    <session-factory>
        <property name="hibernate.connection.driver_class">com.mysql.cj.jdbc.Driver</property>
        <property name="hibernate.dialect">org.hibernate.dialect.TiDBDialect</property>
        <property name="hibernate.connection.url">jdbc:mysql://{host}:{port}/{database}?user={user}&amp;password={password}</property>
    </session-factory>
</hibernate-configuration>
```

随后，使用代码读取配置文件，从而获得 `SessionFactory` 对象：

```java
SessionFactory sessionFactory = new Configuration().configure("hibernate.cfg.xml").buildSessionFactory();
```

这里有几个需要注意的点：

1. 因为使用的配置文件 `hibernate.cfg.xml` 为 XML 格式，而 `&` 字符，在 XML 中属于特殊字符，因此，需将 `&` 更改为 `&amp;`。即，连接字符串 `hibernate.connection.url` 由 `jdbc:mysql://{host}:{port}/{database}?user={user}&password={password}` 改为了 `jdbc:mysql://{host}:{port}/{database}?user={user}&amp;password={password}`。
2. 在你使用 Hibernate 时，建议使用 TiDB 方言，即 `hibernate.dialect` 设置为 `org.hibernate.dialect.TiDBDialect`。
3. Hibernate 在版本 `6.0.0.Beta2` 及以上可支持 TiDB 方言，因此推荐使用 `6.0.0.Beta2` 及以上版本的 Hibernate。

更多有关 Hibernate 连接参数的信息，请参阅 [Hibernate 官方文档](https://hibernate.org/orm/documentation)。

**连接参数**

|    参数名    |                                                描述                                                |
| :----------: | :------------------------------------------------------------------------------------------------: |
| `{username}` | 需要连接到 TiDB 集群的 [SQL 用户](/user-account-management.md) |
| `{password}` |                               需要连接到 TiDB 集群的 SQL 用户的密码                                |
|   `{host}`   |               TiDB 节点运行的 [Host](<https://en.wikipedia.org/wiki/Host_(network)>)               |
|   `{port}`   |                                      TiDB 节点正在监听的端口                                       |
| `{database}` |                                      (已经存在的)数据库的名称                                      |
