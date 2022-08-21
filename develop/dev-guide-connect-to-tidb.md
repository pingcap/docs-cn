---
title: Connect to TiDB
summary: Learn how to connect to TiDB.
---

# Connect to TiDB

TiDB is highly compatible with the MySQL 5.7 protocol. For a full list of client link parameters, see [MySQL Client Options](https://dev.mysql.com/doc/refman/5.7/en/mysql-command-options.html).

TiDB supports the [MySQL Client/Server Protocol](https://dev.mysql.com/doc/internals/en/client-server-protocol.html), which allows most client drivers and ORM frameworks to connect to TiDB just as they connect to MySQL.

## MySQL Shell

You can connect to TiDB using MySQL Shell, which can be used as a command-line tool for TiDB. To install MySQL Shell, follow the instructions in the [MySQL Shell documentation](https://dev.mysql.com/doc/mysql-shell/8.0/en/mysql-shell-install.html). After the installation, you can connect to TiDB using the following command:

{{< copyable "shell-regular" >}}

```shell
mysql --host <tidb_server_host> --port 4000 -u root -p --comments
```

> **Note:**
>
> The MySQL Shell earlier than version 5.7.7 clears [Optimizer Hints](/optimizer-hints.md#optimizer-hints) by default. If you need to use the Hint syntax in an earlier MySQL Shell version, add the `--comments` option when starting the client.

## JDBC

You can connect to TiDB using the [JDBC](https://dev.mysql.com/doc/connector-j/8.0/en/) driver. To do that, you need to create a `MysqlDataSource` or `MysqlConnectionPoolDataSource` object (both objects support the `DataSource` interface), and then set the connection string using the `setURL` function.

For example:

{{< copyable "" >}}

```java
MysqlDataSource mysqlDataSource = new MysqlDataSource();
mysqlDataSource.setURL("jdbc:mysql://{host}:{port}/{database}?user={username}&password={password}");
```

For more information on JDBC connections, see the [JDBC documentation](https://dev.mysql.com/doc/connector-j/8.0/en/)

### Connection parameters

| Parameter name | Description |
| :---: | :----------------------------: |
| `{username}` | A SQL user to connect to the TiDB cluster |
| `{password}` | The password of the SQL user |
| `{host}` | [Host](https://en.wikipedia.org/wiki/Host_(network)) of a TiDB node |
| `{port}` | Port that the TiDB node is listening on |
| `{database}` | Name of an existing database |

<CustomContent platform="tidb">

For more information about TiDB SQL users, see [TiDB User Account Management](/user-account-management.md).

</CustomContent>

<CustomContent platform="tidb-cloud">

For more information about TiDB SQL users, see [TiDB User Account Management](https://docs.pingcap.com/tidb/stable/user-account-management).

</CustomContent>

## Hibernate

You can connect to TiDB using the [Hibernate ORM](https://hibernate.org/orm/). To do that, you need to set `hibernate.connection.url` in the Hibernate configuration file to a legal TiDB connection string.

For example, if you use a `hibernate.cfg.xml` configuration file, set `hibernate.connection.url` as follows:

{{< copyable "" >}}

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

After the configuration is done, you can use the following command to read the configuration file and get the `SessionFactory` object:

{{< copyable "" >}}

```java
SessionFactory sessionFactory = new Configuration().configure("hibernate.cfg.xml").buildSessionFactory();
```

Note the following:

- Because the `hibernate.cfg.xml` configuration file is in the XML format and `&` is a special character in XML, you need to change `&` to `&amp;` when configuring the file. For example, you need to change the connection string `hibernate.connection.url` from `jdbc:mysql://{host}:{port}/{database}?user={user}&password={password}` to `jdbc:mysql://{host}:{ port}/{database}?user={user}&amp;password={password}`.
- It is recommended that you use the `TiDB` dialect by setting `hibernate.dialect` to `org.hibernate.dialect.TiDBDialect`.
- Hibernate supports TiDB dialects starting from `6.0.0.Beta2`, so it is recommended that you use Hibernate `6.0.0.Beta2` or a later version to connect to TiDB.

For more information about Hibernate connection parameters, see [Hibernate documentation](https://hibernate.org/orm/documentation).

### Connection parameters

| Parameter name | Description |
| :---: | :----------------------------: |
| `{username}` |  A SQL user to connect to the TiDB cluster  |
| `{password}` | The password of the SQL user |
| `{host}` | [Host](https://en.wikipedia.org/wiki/Host_(network)) of a TiDB node |
| `{port}` | Port that the TiDB node is listening on |
| `{database}` |  Name of an existing database |

<CustomContent platform="tidb">

For more information about TiDB SQL users, see [TiDB User Account Management](/user-account-management.md).

</CustomContent>

<CustomContent platform="tidb-cloud">

For more information about TiDB SQL users, see [TiDB User Account Management](https://docs.pingcap.com/tidb/stable/user-account-management).

</CustomContent>