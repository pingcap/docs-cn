---
title: PingCAP 维护的三方库
aliases: ['/zh/tidb/dev/supported-by-pingcap']
---

# PingCAP 维护的三方库

TiDB 对 MySQL 协议的支持，使得大部分适配 MySQL 的 Driver、ORM 及其他工具与 TiDB 兼容。本文主要介绍这些工具和它们的支持等级。

## 支持等级

PingCAP 与开源社区合作，通过三方工具提供以下支持：

- Full：表明 PingCAP 已经支持该工具的绝大多数功能兼容性，并且在新版本中对其保持兼容，将定期地对下表中记录的新版本进行兼容性测试。
- Beta：表明 PingCAP 正在努力为该工具提供支持。该工具的主要功能可以被 TiDB 兼容，但缺乏对该工具作完整的兼容性验证，有可能出现一些意外的行为。

> **注意：**
>
> 除非明确说明，否则对于支持的 Driver 或者 ORM 框架并不包括[应用端事务重试和错误处理](/develop/dev-guide-transaction-troubleshoot.md#应用端重试和错误处理)。

如果在使用本文列出的工具连接 TiDB 时出现问题，请在 GitHub 上提交包含详细信息的 [issue](https://github.com/pingcap/tidb/issues/new?assignees=&labels=type%2Fquestion&template=general-question.md)，以帮助在此工具的支持上得到进展。

## Driver

| 编程语言       | 驱动                                                                       | 最新已测试版本 | 支持等级 | TiDB 适配器                                                                                   | 教程                                                                             |
|------------|--------------------------------------------------------------------------|---------|------|--------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------|
| C          | [MySQL Connector/C](https://downloads.mysql.com/archives/c-c/)           | 6.1.11  | Beta | N/A                                                                                        | N/A                                                                            |
| C#(.Net)   | [MySQL Connector/NET](https://downloads.mysql.com/archives/c-net/)       | 8.0.28  | Beta | N/A                                                                                        | N/A                                                                            |
| C#(.Net)   | [MySQL Connector/ODBC](https://downloads.mysql.com/archives/c-odbc/)     | 8.0.28  | Beta | N/A                                                                                        | N/A                                                                            |
| Go         | [go-sql-driver/mysql](https://github.com/go-sql-driver/mysql)            | v1.6.0  | Full | N/A                                                                                        | [TiDB 和 Golang 的简单 CRUD 应用程序](/develop/dev-guide-sample-application-golang.md) |
| Java       | [JDBC](https://dev.mysql.com/downloads/connector/j/)                     | 5.1.46；8.0.29  | Full | 5.1.46：N/A；8.0.29：[pingcap/mysql-connector-j](https://github.com/pingcap/mysql-connector-j/tree/release/8.0)                                                                                     | [TiDB 和 Java 的简单 CRUD 应用程序](/develop/dev-guide-sample-application-java.md)     |
| JavaScript | [mysql](https://github.com/mysqljs/mysql)                                | v2.18.1 | Beta | N/A                                                                                        | N/A                                                                            |
| PHP        | [MySQL Connector/PHP](https://downloads.mysql.com/archives/c-php/)       | 5.0.37  | Beta | N/A                                                                                        | N/A                                                                            |
| Python     | [MySQL Connector/Python](https://downloads.mysql.com/archives/c-python/) | 8.0.28  | Beta | N/A                                                                                        | N/A                                                                            |

## ORM

| 编程语言                  | ORM 框架                                                                                                                                                                        | 最新已测试版本     | 支持等级 | TiDB 适配器                                               | 教程                                                                             |
|-----------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------|------|--------------------------------------------------------|--------------------------------------------------------------------------------|
| Go                    | [gorm](https://github.com/go-gorm/gorm)                                                                                                                                       | v1.23.5     | Full | N/A                                                    | [TiDB 和 Golang 的简单 CRUD 应用程序](/develop/dev-guide-sample-application-golang.md) |
| Go                    | [beego](https://github.com/beego/beego)                                                                                                                                       | v2.0.3      | Full | N/A                                                    | N/A                                                                            |
| Go                    | [upper/db](https://github.com/upper/db)                                                                                                                                       | v4.5.2      | Full | N/A                                                    | N/A                                                                            |
| Go                    | [xorm](https://gitea.com/xorm/xorm)                                                                                                                                           | v1.3.1      | Full | N/A                                                    | N/A                                                                            |
| Java                  | [Hibernate](https://hibernate.org/orm/) | 6.1.0.Final | Full | N/A                                                    | [TiDB 和 Java 的简单 CRUD 应用程序](/develop/dev-guide-sample-application-java.md)     |
| Java                  | [mybatis](https://mybatis.org/mybatis-3/)                                                                                                                                     | v3.5.10     | Full | N/A                                                    | N/A                                                                            |
| jOOQ                  | [jOOQ](https://github.com/jOOQ/jOOQ)                                                                                                                                     | v3.16.7 (Open Source)     | Full | N/A                                                    | N/A                                                                            |
| JavaScript/TypeScript | [sequelize](https://www.npmjs.com/package/sequelize)                                                                                                                          | v6.20.1     | Beta | N/A                                                    | N/A                                                                            |
| JavaScript/TypeScript | [Knex.js](https://knexjs.org/)                                                                                                                                                | v1.0.7      | Beta | N/A                                                    | N/A                                                                            |
| JavaScript/TypeScript | [Prisma Client](https://www.prisma.io/)                                                                                                                                       | 3.15.1      | Beta | N/A                                                    | N/A                                                                            |
| JavaScript/TypeScript | [TypeORM](https://www.npmjs.com/package/typeorm)                                                                                                                              | v0.3.6      | Beta | N/A                                                    | N/A                                                                            |
| PHP                   | [laravel](https://laravel.com/)                                                                                                                                               | v9.1.10     | Beta | [laravel-tidb](https://github.com/colopl/laravel-tidb) | N/A                                                                            |
| Python                | [Django](https://pypi.org/project/Django/)                                                  | v4.0.5      | Beta | N/A                                                    | N/A                                                                            |
| Python                | [peewee](https://github.com/coleifer/peewee/)                                                                                                                                 | v3.14.10    | Beta | N/A                                                    | N/A                                                                            |
| Python                | [PonyORM](https://ponyorm.org/)                                                                                                                                               | v0.7.16     | Beta | N/A                                                    | N/A                                                                            |
| Python                | [SQLAlchemy](https://www.sqlalchemy.org/)                                                                                                                                     | v1.4.37     | Beta | N/A                                                    | N/A                                                                            |

## GUI

| GUI                                           | 最新已测试版本  | 支持等级 | 教程  |
|-----------------------------------------------|---------|------|-----|
| [DBeaver](https://dbeaver.io/)                | 22.1.0  | Beta | N/A |
| [Navicat for MySQL](https://www.navicat.com/) | 16.0.14 | Beta | N/A |

| IDE                                              | 最新已测试版本 | 支持等级 | 教程 |
| ------------------------------------------------ | ------- | ---- | ---- |
| [DataGrip](https://www.jetbrains.com/datagrip/)  | N/A     | Beta | N/A  |
| [IntelliJ IDEA](https://www.jetbrains.com/idea/) | N/A     | Beta | N/A  |
