---
title: 第三方支持的工具
summary: 了解 TiDB 支持的第三方工具，包括 Driver, ORM 框架等。
---

# 支持级别

TiDB 支持大多数 MySQL 兼容的 Driver, ORM 框架和其他的一些数据库工具。本文会列出 TiDB 官方支持的一些流行的 MySQL 工具。

TiDB 为第三方工具提供以下级别的支持：

- Full support: 表示 TiDB 尽量保持与该工具的绝大多数功能的兼容性。定期对该工具的最新版本进行测试。
- Beta support: 表示 TiDB 正在努力为该工具提供全面支持。该工具的主要功能可以和 TiDB 兼容（例如连接和数据库的基本操作），但缺乏对该工具所有功能的支持，有可能出现一些意外的行为。

> **注意：**
>
> 除非明确说明，否则对于支持的 driver 或者 ORM 框架并不包括[应用端事务重试和错误处理](/develop/dev-guide-transaction-troubleshoot.md#应用端重试和错误处理)。

如果你在使用下列工具时遇到问题，欢迎给 [TiDB](https://github.com/pingcap/tidb) 提交 issue。

# Drivers

| 编程语言       | 驱动                                                                       | 最新测试版本  | 支持级别 | TiDB 适配器                                                                                   | 教程                                                                             |
|------------|--------------------------------------------------------------------------|---------|------|--------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------|
| C          | [MySQL Connector/C](https://downloads.mysql.com/archives/c-c/)           | 6.1.11  | Beta | N/A                                                                                        | N/A                                                                            |
| C#(.Net)   | [MySQL Connector/NET](https://downloads.mysql.com/archives/c-net/)       | 8.0.28  | Beta | N/A                                                                                        | N/A                                                                            |
| C#(.Net)   | [MySQL Connector/ODBC](https://downloads.mysql.com/archives/c-odbc/)     | 8.0.28  | Beta | N/A                                                                                        | N/A                                                                            |
| Go         | [go-sql-driver/mysql](https://github.com/go-sql-driver/mysql)            | v1.6.0  | Full | N/A                                                                                        | [TiDB 和 Golang 的简单 CRUD 应用程序](/develop/dev-guide-sample-application-golang.md) |
| Java       | [JDBC](https://dev.mysql.com/downloads/connector/j/)                     | 5.1.46  | Full | N/A                                                                                        | [TiDB 和 Java 的简单 CRUD 应用程序](/develop/dev-guide-sample-application-java.md)     |
| Java       | [JDBC](https://dev.mysql.com/downloads/connector/j/)                     | 8.0.29  | Full | [pingcap/mysql-connector-j](https://github.com/pingcap/mysql-connector-j/tree/release/8.0) | [TiDB 和 Java 的简单 CRUD 应用程序](/develop/dev-guide-sample-application-java.md)     |
| JavaScript | [mysql](https://github.com/mysqljs/mysql)                                | v2.18.1 | Beta | N/A                                                                                        | N/A                                                                            |
| PHP        | [MySQL Connector/PHP](https://downloads.mysql.com/archives/c-php/)       | 5.0.37  | Beta | N/A                                                                                        | N/A                                                                            |
| Python     | [MySQL Connector/Python](https://downloads.mysql.com/archives/c-python/) | 8.0.28  | Beta | N/A                                                                                        | N/A                                                                            |

# ORM 框架

| 编程语言                  | ORM 框架                                               | 最新测试版本   | 支持级别 | TiDB 适配器                                               | 教程                                                                             |
|-----------------------|------------------------------------------------------|----------|------|--------------------------------------------------------|--------------------------------------------------------------------------------|
| Go                    | [gorm](https://github.com/go-gorm/gorm)              | v1.23.5  | Full | N/A                                                    | [TiDB 和 Golang 的简单 CRUD 应用程序](/develop/dev-guide-sample-application-golang.md) |
| Go                    | [beego](https://github.com/beego/beego)              | v2.0.3   | Full | N/A                                                    | N/A                                                                            |
| Go                    | [upper/db](https://github.com/upper/db)              | v4.5.2   | Full | N/A                                                    | N/A                                                                            |
| Go                    | [xorm](https://gitea.com/xorm/xorm)                  | v1.3.1   | Full | N/A                                                    | N/A                                                                            |
| Java                  | [hibernate](https://hibernate.org/orm/)              | v6.0     | Beta | N/A                                                    | [TiDB 和 Java 的简单 CRUD 应用程序](/develop/dev-guide-sample-application-java.md)     |
| Java                  | [mybatis](https://mybatis.org/mybatis-3/)            | v3.5.10  | Beta | N/A                                                    | N/A                                                                            |
| JavaScript/TypeScript | [sequelize](https://www.npmjs.com/package/sequelize) | v6.20.1  | Beta | N/A                                                    | N/A                                                                            |
| JavaScript/TypeScript | [Knex.js](https://knexjs.org/)                       | v1.0.7   | Beta | N/A                                                    | N/A                                                                            |
| JavaScript/TypeScript | [Prisma](https://www.prisma.io/)                     | 3.15.1   | Beta | N/A                                                    | N/A                                                                            |
| JavaScript/TypeScript | [typeorm](https://www.npmjs.com/package/typeorm)     | v0.3.6   | Beta | N/A                                                    | N/A                                                                            |
| PHP                   | [laravel](https://laravel.com/)                      | v9.1.10  | Beta | [laravel-tidb](https://github.com/colopl/laravel-tidb) | N/A                                                                            |
| Python                | [Django](https://pypi.org/project/Django/)           | v4.0.5   | Beta | N/A                                                    | N/A                                                                            |
| Python                | [peewee](https://github.com/coleifer/peewee/)        | v3.14.10 | Beta | N/A                                                    | N/A                                                                            |
| Python                | [PonyORM](https://ponyorm.org/)                      | v0.7.16  | Beta | N/A                                                    | N/A                                                                            |
| Python                | [SQLAlchemy](https://www.sqlalchemy.org/)            | v1.4.37  | Beta | N/A                                                    | N/A                                                                            |

# GUI

| GUI                                           | 最新测试版本  | 支持级别 | 教程  |
|-----------------------------------------------|---------|------|-----|
| [DBeaver](https://dbeaver.io/)                | 22.1.0  | Beat | N/A |
| [Navicat for MySQL](https://www.navicat.com/) | 16.0.14 | Beat | N/A |
