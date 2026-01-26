---
title: 应用开发概览
summary: TiDB Cloud 和 TiDB 的开发者指南概览。
aliases: ['zh/tidbcloud/dev-guide-overview/','zh/tidb/dev/dev-guide-overview/','zh/stable/dev/dev-guide-overview/']
---

# 应用开发概览

本指南是为应用程序开发者所编写的，如果你对 TiDB 的内部原理感兴趣，或希望参与到 TiDB 的开发中来，那么可前往阅读 [TiDB Kernel Development Guide](https://pingcap.github.io/tidb-dev-guide/) 来获取更多 TiDB 的相关信息。

此外，你还可以通过视频的形式学习免费的 [TiDB SQL 开发在线课程](https://pingkai.cn/learn)。

## 按语言和框架分类

你可以使用自己熟悉的编程语言，结合以下包含示例代码的文档来构建你的应用程序。

<DevLangAccordion label="JavaScript" defaultExpanded>
<DevToolCard title="Serverless Driver（beta）" logo="tidb" docLink="/developer/serverless-driver" githubLink="https://github.com/tidbcloud/serverless-js">

在边缘环境中通过 HTTPS 连接到 TiDB（仅适用于 TiDB Cloud）。

</DevToolCard>
<DevToolCard title="Next.js" logo="nextjs" docLink="/developer/dev-guide-sample-application-nextjs" githubLink="https://github.com/vercel/next.js">

通过 mysql2 将 Next.js 连接到 TiDB。

</DevToolCard>
<DevToolCard title="Prisma" logo="prisma" docLink="/developer/dev-guide-sample-application-nodejs-prisma" githubLink="https://github.com/prisma/prisma">

使用 Prisma ORM 连接 TiDB。

</DevToolCard>
<DevToolCard title="TypeORM" logo="typeorm" docLink="/developer/dev-guide-sample-application-nodejs-typeorm" githubLink="https://github.com/typeorm/typeorm">

使用 TypeORM 连接 TiDB。

</DevToolCard>
<DevToolCard title="Sequelize" logo="sequelize" docLink="/developer/dev-guide-sample-application-nodejs-sequelize" githubLink="https://github.com/sequelize/sequelize">

使用 Sequelize ORM 连接 TiDB。

</DevToolCard>
<DevToolCard title="mysql.js" logo="mysql" docLink="/developer/dev-guide-sample-application-nodejs-mysqljs" githubLink="https://github.com/mysqljs/mysql">

通过 mysql.js 模块将 Node.js 连接到 TiDB。

</DevToolCard>
<DevToolCard title="node-mysql2" logo="mysql" docLink="/developer/dev-guide-sample-application-nodejs-mysql2" githubLink="https://github.com/sidorares/node-mysql2">

通过 node-mysql2 模块将 Node.js 连接到 TiDB。

</DevToolCard>
<DevToolCard title="AWS Lambda" logo="aws-lambda" docLink="/developer/dev-guide-sample-application-aws-lambda" githubLink="https://github.com/sidorares/node-mysql2">

在 AWS Lambda 函数中使用 mysql2 连接 TiDB。

</DevToolCard>
</DevLangAccordion>

<DevLangAccordion label="Python" defaultExpanded>
<DevToolCard title="Django" logo="django" docLink="/developer/dev-guide-sample-application-python-django" githubLink="https://github.com/pingcap/django-tidb">

通过 django-tidb 将 Django 应用连接 TiDB。

</DevToolCard>
<DevToolCard title="MySQL Connector/Python" logo="python" docLink="/developer/dev-guide-sample-application-python-mysql-connector" githubLink="https://github.com/mysql/mysql-connector-python">

使用 MySQL Connector/Python 连接 TiDB。

</DevToolCard>
<DevToolCard title="PyMySQL" logo="python" docLink="/developer/dev-guide-sample-application-python-pymysql" githubLink="https://github.com/PyMySQL/PyMySQL">

使用 PyMySQL 包连接 TiDB。

</DevToolCard>
<DevToolCard title="mysqlclient" logo="python" docLink="/developer/dev-guide-sample-application-python-mysqlclient" githubLink="https://github.com/PyMySQL/mysqlclient">

使用 mysqlclient 包连接 TiDB。

</DevToolCard>
<DevToolCard title="SQLAlchemy" logo="sqlalchemy" docLink="/developer/dev-guide-sample-application-python-sqlalchemy" githubLink="https://github.com/sqlalchemy/sqlalchemy">

使用 SQLAlchemy ORM 连接 TiDB。

</DevToolCard>
<DevToolCard title="peewee" logo="peewee" docLink="/developer/dev-guide-sample-application-python-peewee" githubLink="https://github.com/coleifer/peewee">

使用 Peewee ORM 连接 TiDB。

</DevToolCard>
</DevLangAccordion>

<DevLangAccordion label="Java">
<DevToolCard title="JDBC" logo="java" docLink="/developer/dev-guide-sample-application-java-jdbc" githubLink="https://github.com/mysql/mysql-connector-j">

使用 JDBC（MySQL Connector/J）连接 TiDB。

</DevToolCard>
<DevToolCard title="MyBatis" logo="mybatis" docLink="/developer/dev-guide-sample-application-java-mybatis" githubLink="https://github.com/mybatis/mybatis-3">

使用 MyBatis ORM 连接 TiDB。

</DevToolCard>
<DevToolCard title="Hibernate" logo="hibernate" docLink="/developer/dev-guide-sample-application-java-hibernate" githubLink="https://github.com/hibernate/hibernate-orm">

使用 Hibernate ORM 连接 TiDB。

</DevToolCard>
<DevToolCard title="Spring Boot" logo="spring" docLink="/developer/dev-guide-sample-application-java-spring-boot" githubLink="https://github.com/spring-projects/spring-data-jpa">

使用 Spring Boot 连接 TiDB。

</DevToolCard>
</DevLangAccordion>

<DevLangAccordion label="Go">
<DevToolCard title="Go-MySQL-Driver" logo="go" docLink="/developer/dev-guide-sample-application-golang-sql-driver" githubLink="https://github.com/go-sql-driver/mysql">

使用 Go-MySQL-Driver 连接 TiDB。

</DevToolCard>
<DevToolCard title="GORM" logo="gorm" docLink="/developer/dev-guide-sample-application-golang-gorm" githubLink="https://github.com/go-gorm/gorm">

使用 GORM 连接 TiDB。

</DevToolCard>
</DevLangAccordion>

<DevLangAccordion label="Ruby">
<DevToolCard title="Ruby on Rails" logo="rails" docLink="/developer/dev-guide-sample-application-ruby-rails" githubLink="https://github.com/rails/rails/tree/main/activerecord">

使用 Rails 框架和 ActiveRecord ORM 连接 TiDB。

</DevToolCard>
<DevToolCard title="mysql2" logo="ruby" docLink="/developer/dev-guide-sample-application-ruby-mysql2" githubLink="https://github.com/brianmario/mysql2">

使用 mysql2 驱动连接 TiDB。

</DevToolCard>
</DevLangAccordion>

除了上述指南之外，PingCAP 还与社区合作，支持[第三方 MySQL 驱动、ORM 以及工具](/develop/dev-guide-third-party-support.md)。

## 使用 MySQL 客户端软件

TiDB 与 MySQL 高度兼容，你可以使用许多熟悉的 MySQL 客户端工具来连接 TiDB 并管理数据库。对于 TiDB Cloud 用户，你还可以使用 <a href="/tidbcloud/get-started-with-cli">>TiDB Cloud CLI</a> 来连接和管理数据库。

<DevToolGroup>
<DevToolCard title="MySQL Workbench" logo="mysql-1" docLink="/developer/dev-guide-gui-mysql-workbench">

使用 MySQL Workbench 连接并管理 TiDB 数据库。

</DevToolCard>
<DevToolCard title="Visual Studio Code" logo="vscode" docLink="/developer/dev-guide-gui-vscode-sqltools">

使用 VS Code 中的 SQLTools 扩展连接并管理 TiDB 数据库。

</DevToolCard>
<DevToolCard title="DBeaver" logo="dbeaver" docLink="/developer/dev-guide-gui-dbeaver">

使用 DBeaver 连接并管理 TiDB 数据库。

</DevToolCard>
<DevToolCard title="DataGrip" logo="datagrip" docLink="/developer/dev-guide-gui-datagrip">

使用 JetBrains 的 DataGrip 连接并管理 TiDB 数据库。

</DevToolCard>
</DevToolGroup>