---
title: PingCAP 维护的三方库
---

# PingCAP 维护的三方库

TiDB 对 MySQL 协议的支持，使得大部分适配 MySQL 的 Driver、ORM 及其他工具与 TiDB 兼容。我们将适配一组满足大多数语言和框架的工具，此页面上将展示这些工具和它们的支持等级。

## 支持等级

PingCAP 与开源社区合作，通过三方工具提供以下支持：

- Full: 表明 PingCAP 将尽力支持该工具的绝大多数功能兼容性。我们将定期地对下表中记录的最新版本进行测试。
- Beta: 表名 PingCAP 正在努力支持该工具。该工具的主要功能将与 TiDB 兼容(连接数据库及基本数据库操作)，但有可能会出现意外行为，且可能需要额外的步骤进行集成。

如果您在使用此处列出的工具连接 TiDB 时出现问题，请提出一个包含详细信息的[问题](https://github.com/pingcap/tidb/issues/new?assignees=&labels=type%2Fquestion&template=general-question.md)，以帮助我们在此工具的支持上得到进展。

## Driver

|    语言    |                                   驱动                                   |                                        最新已测试版本                                        | 支持等级 | TiDB 适配器地址 | 教程地址 |
| :--------: | :----------------------------------------------------------------------: | :------------------------------------------------------------------------------------------: | :------: | :-------------: | :------: |
|     C      |      [MySQL Connector/C](https://downloads.mysql.com/archives/c-c/)      |                                            6.1.11                                            |
|  C#(.Net)  |    [MySQL Connector/NET](https://downloads.mysql.com/archives/c-net/)    |                                            8.0.27                                            |
|     ⬆️     |   [MySQL Connector/ODBC](https://downloads.mysql.com/archives/c-odbc/)   |                                            8.0.27                                            |
|     Go     | [go-sql-driver/mysql](https://pkg.go.dev/github.com/go-sql-driver/mysql) |                                            1.6.0                                             |
|    Java    |          [JDBC](https://dev.mysql.com/doc/connector-j/8.0/en/)           | [8.0.28](https://mvnrepository.com/artifact/mysql/mysql-connector-java/8.0.28)(Maven Center) |
| JavaScript |                [mysql](https://github.com/mysqljs/mysql)                 |                    [2.18.1](https://www.npmjs.com/package/mysql)(npm.js)                     |
|    PHP     |    [MySQL Connector/PHP](https://downloads.mysql.com/archives/c-php/)    |                                            5.0.37                                            |
|   Python   | [MySQL Connector/Python](https://downloads.mysql.com/archives/c-python/) |                                            8.0.27                                            |

## ORM

|  语言  |                                                                                     框架                                                                                      | 最新已测试版本 | 支持等级 | TiDB 适配器地址 | 教程地址 |
| :----: | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------: | :------------: | :------: | :-------------: | :------: |
|   Go   |                                                                    [gorm](https://github.com/go-gorm/gorm)                                                                    |     1.23.2     |
|   ⬆️   |                                                                    [upper/db](https://github.com/upper/db)                                                                    |     4.5.2      |
|   ⬆️   |                                                                    [beego](https://github.com/beego/beego)                                                                    |     2.0.2      |
|  Java  | [Hibernate](https://hibernate.org/orm/) (including [Hibernate Spatial](https://docs.jboss.org/hibernate/orm/current/userguide/html_single/Hibernate_User_Guide.html#spatial)) |  5.6.5.Final   |
|   ⬆️   |                                                                   [MyBatis](https://mybatis.org/mybatis-3/)                                                                   |     3.5.9      |
| JS/TS  |                                                             [sequelize](https://www.npmjs.com/package/sequelize)                                                              |     6.17.0     |
|   ⬆️   |                                                                        [Knex.js](https://knexjs.org/)                                                                         |     1.0.4      |
|   ⬆️   |                                                                    [Prisma Client](https://www.prisma.io/)                                                                    |     3.10.0     |
|   ⬆️   |                                                               [TypeORM](https://www.npmjs.com/package/typeorm)                                                                |     0.2.45     |
|  PHP   |
| Python |                          [Django](https://pypi.org/project/Django/) (including [GeoDjango](https://docs.djangoproject.com/en/4.0/ref/contrib/gis/))                           |     4.0.3      |
|   ⬆️   |                                                                 [peewee](https://github.com/coleifer/peewee/)                                                                 |    3.14.10     |
|   ⬆️   |                                                                        [PonyORM](https://ponyorm.org/)                                                                        |     0.7.16     |
|   ⬆️   |                                                                   [SQLAlchemy](https://www.sqlalchemy.org/)                                                                   |     1.4.32     |

## 应用框架

| 应用框架 |    数据接入框架     | 最新已测试版本 | 支持等级 | 教程地址 |
| :------: | :-----------------: | :------------: | :------: | :------: |
|  Spring  |        JDBC         |
|    ⬆️    | JPA(with Hibernate) |
|    ⬆️    |       MyBatis       |

## GUI

|                  GUI                   | 最新已测试版本 | 支持等级 | 教程地址 |
| :------------------------------------: | :------------: | :------: | :------: |
| [Navicat](https://www.navicat.com/en/) |

## IDE

|                       IDE                        | 最新已测试版本 | 支持等级 | 教程地址 |
| :----------------------------------------------: | :------------: | :------: | :------: |
| [DataGrip](https://www.jetbrains.com/datagrip/)  |
| [IntelliJ IDEA](https://www.jetbrains.com/idea/) |
