---
title: TiDB 支持的第三方工具
summary: TiDB 支持的第三方工具主要包括驱动、ORM 框架和 GUI。支持等级分为 Full 和 Compatible，其中 Full 表示绝大多数功能兼容性已得到支持，Compatible 表示大部分功能可使用但未经完整验证。对于支持的 Driver 或 ORM 框架并不包括应用端事务重试和错误处理。如果在使用工具连接 TiDB 时出现问题，可在 GitHub 上提交包含详细信息的 issue 以获得进展。
aliases: ['/zh/tidb/stable/dev-guide-third-party-support/','/zh/tidb/dev/dev-guide-third-party-support/','/zh/tidbcloud/dev-guide-third-party-support/','/zh/tidb/dev/supported-by-pingcap']
---

# TiDB 支持的第三方工具

> **注意：**
>
> 本文档仅列举了常见的 TiDB 支持的[第三方工具](https://en.wikipedia.org/wiki/Third-party_source)，未被列入其中的第三方工具并非代表不支持，但 PingCAP 无法了解其是否使用到 TiDB 不支持的特性，从而无法保证兼容性。

TiDB [高度兼容 MySQL 协议](/mysql-compatibility.md)，使得大部分适配 MySQL 的 Driver、ORM 及其他工具与 TiDB 兼容。本文主要介绍这些工具和它们的支持等级。

## 支持等级

PingCAP 与开源社区合作，通过三方工具提供以下支持：

- Full：表明 PingCAP 已经支持该工具的绝大多数功能兼容性，并且在新版本中对其保持兼容，将定期地对下表中记录的新版本进行兼容性测试。
- Compatible：表明由于该工具已适配 MySQL，而 TiDB 高度兼容 MySQL 协议，因此可以使用此工具的大部分功能。但 PingCAP 并未对该工具作出完整的兼容性验证，有可能出现一些意外的行为。

> **注意：**
>
> 除非明确说明，否则对于支持的 Driver 或者 ORM 框架并不包括[应用端事务重试和错误处理](/develop/dev-guide-transaction-troubleshoot.md#应用端重试和错误处理)。

如果在使用本文列出的工具连接 TiDB 时出现问题，请在 GitHub 上提交包含详细信息的 [issue](https://github.com/pingcap/tidb/issues/new?assignees=&labels=type%2Fquestion&template=general-question.md)，以帮助在此工具的支持上得到进展。

## Driver

| 编程语言 | 驱动 | 最新已测试版本 | 支持等级 | TiDB 适配器 | 教程 |
|----------|--------|-----------------------|---------------|--------------|----------|
| Go | [go-sql-driver/mysql](https://github.com/go-sql-driver/mysql) | v1.6.0 | Full | N/A | [使用 Go-MySQL-Driver 连接到 TiDB](/develop/dev-guide-sample-application-golang-sql-driver.md) |
| Java | [MySQL Connector/J](https://dev.mysql.com/downloads/connector/j/) | 8.0 | Full | [pingcap/mysql-connector-j](/develop/dev-guide-choose-driver-or-orm.md#java-drivers) <br/> [pingcap/tidb-loadbalance](/develop/dev-guide-choose-driver-or-orm.md#java-客户端负载均衡) | [使用 JDBC 连接到 TiDB](/develop/dev-guide-sample-application-java-jdbc.md) |

## ORM

| 编程语言 | ORM 框架 | 最新已测试版本 | 支持等级 | TiDB 适配器 | 教程 |
|-------------------------|-------------------------------------------|-----------------------|-------------|--------------|----------|
| Go                      | [gorm](https://github.com/go-gorm/gorm)   | v1.23.5               | Full      | N/A           | [使用 GORM 连接到 TiDB](/develop/dev-guide-sample-application-golang-gorm.md) |
| Go                      | [beego](https://github.com/beego/beego)   | v2.0.3                | Full      | N/A           | N/A |
| Go                      | [upper/db](https://github.com/upper/db)   | v4.5.2                | Full      | N/A           | N/A |
| Go                      | [xorm](https://gitea.com/xorm/xorm)       | v1.3.1                | Full      | N/A           | N/A |
| Java                    | [Hibernate](https://hibernate.org/orm/)   | 6.1.0.Final           | Full      | N/A           | [使用 Hibernate 连接到 TiDB](/develop/dev-guide-sample-application-java-hibernate.md) |
| Java                    | [MyBatis](https://mybatis.org/mybatis-3/) | v3.5.10               | Full      | N/A           | [使用 MyBatis 连接到 TiDB](/develop/dev-guide-sample-application-java-mybatis.md) |
| Java                    | [Spring Data JPA](https://spring.io/projects/spring-data-jpa/) | 2.7.2 | Full | N/A           | [使用 Spring Boot 连接到 TiDB](/develop/dev-guide-sample-application-java-spring-boot.md) |
| Java                    | [jOOQ](https://github.com/jOOQ/jOOQ)      | v3.16.7 (Open Source) | Full      | N/A           | N/A |
| Ruby                    | [Active Record](https://guides.rubyonrails.org/active_record_basics.html) | v7.0 | Full | N/A | [使用 Rails 框架和 ActiveRecord ORM 连接到 TiDB](/develop/dev-guide-sample-application-ruby-rails.md) |
| JavaScript / TypeScript | [Sequelize](https://sequelize.org/)       | v6.20.1               | Full      | N/A           | [使用 Sequelize 连接到 TiDB](/develop/dev-guide-sample-application-nodejs-sequelize.md) |
| JavaScript / Typescript | [Prisma](https://www.prisma.io/)          | 4.16.2                | Full      | N/A           | [使用 Prisma 连接到 TiDB](/develop/dev-guide-sample-application-nodejs-prisma.md) |
| JavaScript / Typescript | [TypeORM](https://typeorm.io/)            | v0.3.17               | Full      | N/A           | [使用 TypeORM 连接到 TiDB](/develop/dev-guide-sample-application-nodejs-typeorm.md) |
| Python                  | [Django](https://www.djangoproject.com/)  | v4.2                  | Full      | [django-tidb](https://github.com/pingcap/django-tidb) | [使用 Django 连接到 TiDB](/develop/dev-guide-sample-application-python-django.md) |
| Python                  | [SQLAlchemy](https://www.sqlalchemy.org/) | v1.4.37               | Full      | N/A           | [使用 SQLAlchemy 连接到 TiDB](/develop/dev-guide-sample-application-python-sqlalchemy.md) |

## GUI

| GUI                                                       | 最新已测试版本 | 支持等级 | 教程 |
|-----------------------------------------------------------|-----------------------|---------------|-----|
| [JetBrains DataGrip](https://www.jetbrains.com/datagrip/) | 2023.2.1              | Full          | N/A |
| [DBeaver](https://dbeaver.io/)                            | 23.0.3                | Full          | N/A |
| [Visual Studio Code](https://code.visualstudio.com/)      | 1.72.0                | Full          | N/A |
| [Navicat](https://www.navicat.com)      | 17.1.6                | Full          | [使用 Navicat 连接到 TiDB](/develop/dev-guide-gui-navicat.md) |