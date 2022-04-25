---
title: 连接到 TiDB
---

# 连接到 TiDB

`TiDB` 高度兼容 `MySQL 5.7` 协议，全量的客户端链接参数列表，请参阅 [MySQL Client Options](https://dev.mysql.com/doc/refman/5.7/en/mysql-command-options.html)。

TiDB 支持 [MySQL 客户端/服务器协议](https://dev.mysql.com/doc/internals/en/client-server-protocol.html)。这使得大多数客户端驱动程序和 ORM 框架可以像连接到 MySQL 一样地连接到 TiDB。

## MySQL Client

你可以使用 MySQL Client 作为 TiDB 的命令行工具。在 [MySQL Shell 官方文档](https://dev.mysql.com/doc/mysql-shell/8.0/en/mysql-shell-install.html) 你可以找到不同操作系统的安装方式。在安装完后你可以使用如下命令行连接到 TiDB：

```bash
mysql --host <tidb_server_host> --port 4000 -u root -p --comments
```

注意：MySQL 命令行客户端在 5.7.7 版本之前默认清除了 [Optimizer Hints](https://docs.pingcap.com/zh/tidb/stable/optimizer-hints#optimizer-hints)。如果需要在这些早期版本的客户端中使用 Hint 语法，需要在启动客户端时加上 `--comments` 选项。

## JDBC

您可以使用 [JDBC](https://dev.mysql.com/doc/connector-j/8.0/en/) 驱动连接到 TiDB，这需要创建一个 `MysqlDataSource` 或 `MysqlConnectionPoolDataSource` 对象 (它们都实现了 `DataSource` 接口)，并使用 `setURL` 函数设置连接字符串。

例如：

```java
MysqlDataSource mysqlDataSource = new MysqlDataSource();
mysqlDataSource.setURL("jdbc:mysql://{host}:{port}/{database}?user={username}&password={password}");
```

有关 JDBC 连接的更多信息，可参考 [JDBC 官方文档](https://dev.mysql.com/doc/connector-j/8.0/en/)

### 连接参数

|    参数名    |                                                描述                                                |
| :----------: | :------------------------------------------------------------------------------------------------: |
| `{username}` | 需要连接到 TiDB 集群的 [SQL 用户](https://docs.pingcap.com/zh/tidb/stable/user-account-management) |
| `{password}` |                               需要连接到 TiDB 集群的 SQL 用户的密码                                |
|   `{host}`   |               TiDB 节点运行的 [Host](<https://en.wikipedia.org/wiki/Host_(network)>)               |
|   `{port}`   |                                      TiDB 节点正在监听的端口                                       |
| `{database}` |                                      (已经存在的)数据库的名称                                      |

## Hibernate

您可以使用 [Hibernate ORM](https://hibernate.org/orm/) 连接到 TiDB，请将 Hibernate 的配置中的 `hibernate.connection.url` 设置为合法的 TiDB 连接字符串。

例如，您的配置被写在 `hibernate.cfg.xml` 文件中，那么你的配置文件应该为：

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

1. 因为我们使用的配置文件 `hibernate.cfg.xml` 为 XML 格式，而 `&` 字符，在 XML 中属于特殊字符，因此，需将 `&` 更改为 `&amp;`。即，我们的连接字符串 `hibernate.connection.url` 由 `jdbc:mysql://{host}:{port}/{database}?user={user}&password={password}` 改为了 `jdbc:mysql://{host}:{port}/{database}?user={user}&amp;password={password}`。
2. 在您使用 Hibernate 时，我们建议您使用 TiDB 方言，即 `hibernate.dialect` 设置为 `org.hibernate.dialect.TiDBDialect`。
3. Hibernate 在版本 `6.0.0.Beta2` 及以上可支持 TiDB 方言，因此我们推荐使用 `6.0.0.Beta2` 及以上版本的 Hibernate。

更多有关 Hibernate 连接参数的信息，请参阅 [Hibernate 官方文档](https://hibernate.org/orm/documentation)

### 连接参数

|    参数名    |                                                描述                                                |
| :----------: | :------------------------------------------------------------------------------------------------: |
| `{username}` | 需要连接到 TiDB 集群的 [SQL 用户](https://docs.pingcap.com/zh/tidb/stable/user-account-management) |
| `{password}` |                               需要连接到 TiDB 集群的 SQL 用户的密码                                |
|   `{host}`   |               TiDB 节点运行的 [Host](<https://en.wikipedia.org/wiki/Host_(network)>)               |
|   `{port}`   |                                      TiDB 节点正在监听的端口                                       |
| `{database}` |                                      (已经存在的)数据库的名称                                      |
