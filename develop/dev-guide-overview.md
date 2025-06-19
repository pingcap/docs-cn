---
title: 开发者指南概览
summary: 介绍 TiDB Cloud 和 TiDB Self-Managed 的开发者指南概览。
---

# 开发者指南概览

<CustomContent platform="tidb-cloud">

<IntroHero title="了解 TiDB Cloud 基础知识" content="TiDB Cloud 是基于 TiDB 构建的全托管服务，高度兼容 MySQL 协议并支持大多数 MySQL 语法和功能。" videoTitle="3 分钟了解 TiDB Cloud">
  <IntroHeroVideo src="https://www.youtube.com/embed/skCV9BEmjbo?autoplay=1" title="3 分钟了解 TiDB Cloud" />
</IntroHero>

## 按语言和框架分类的指南

按照带有示例代码的指南，使用您熟悉的语言构建应用程序。

<DevLangAccordion label="JavaScript" defaultExpanded>
<DevToolCard title="Serverless 驱动（测试版）" logo="tidb" docLink="/tidbcloud/serverless-driver" githubLink="https://github.com/tidbcloud/serverless-js">

在 Edge Function 中通过 HTTPS 连接到 TiDB Cloud。

</DevToolCard>
<DevToolCard title="Next.js" logo="nextjs" docLink="/tidbcloud/dev-guide-sample-application-nextjs" githubLink="https://github.com/vercel/next.js">

使用 mysql2 将 Next.js 连接到 TiDB Cloud。

</DevToolCard>
<DevToolCard title="Prisma" logo="prisma" docLink="/tidbcloud/dev-guide-sample-application-nodejs-prisma" githubLink="https://github.com/prisma/prisma">

使用 Prisma ORM 连接到 TiDB Cloud。

</DevToolCard>
<DevToolCard title="TypeORM" logo="typeorm" docLink="/tidbcloud/dev-guide-sample-application-nodejs-typeorm" githubLink="https://github.com/typeorm/typeorm">

使用 TypeORM 连接到 TiDB Cloud。

</DevToolCard>
<DevToolCard title="Sequelize" logo="sequelize" docLink="/tidbcloud/dev-guide-sample-application-nodejs-sequelize" githubLink="https://github.com/sequelize/sequelize">

使用 Sequelize ORM 连接到 TiDB Cloud。

</DevToolCard>
<DevToolCard title="mysql.js" logo="mysql" docLink="/tidbcloud/dev-guide-sample-application-nodejs-mysqljs" githubLink="https://github.com/mysqljs/mysql">

使用 mysql.js 模块将 Node.js 连接到 TiDB Cloud。

</DevToolCard>
<DevToolCard title="node-mysql2" logo="mysql" docLink="/tidbcloud/dev-guide-sample-application-nodejs-mysql2" githubLink="https://github.com/sidorares/node-mysql2">

使用 node-mysql2 模块将 Node.js 连接到 TiDB Cloud。

</DevToolCard>
<DevToolCard title="AWS Lambda" logo="aws-lambda" docLink="/tidbcloud/dev-guide-sample-application-aws-lambda" githubLink="https://github.com/sidorares/node-mysql2">

使用 mysql2 将 AWS Lambda 函数连接到 TiDB Cloud。

</DevToolCard>
</DevLangAccordion>

<DevLangAccordion label="Python" defaultExpanded>
<DevToolCard title="Django" logo="django" docLink="/tidbcloud/dev-guide-sample-application-python-django" githubLink="https://github.com/pingcap/django-tidb">

使用 django-tidb 将 Django 应用程序连接到 TiDB Cloud。

</DevToolCard>
<DevToolCard title="MySQL Connector/Python" logo="python" docLink="/tidbcloud/dev-guide-sample-application-python-mysql-connector" githubLink="https://github.com/mysql/mysql-connector-python">

使用 MySQL 官方包连接到 TiDB Cloud。

</DevToolCard>
<DevToolCard title="PyMySQL" logo="python" docLink="/tidbcloud/dev-guide-sample-application-python-pymysql" githubLink="https://github.com/PyMySQL/PyMySQL">

使用 PyMySQL 包连接到 TiDB Cloud。

</DevToolCard>
<DevToolCard title="mysqlclient" logo="python" docLink="/tidbcloud/dev-guide-sample-application-python-mysqlclient" githubLink="https://github.com/PyMySQL/mysqlclient">

使用 mysqlclient 包连接到 TiDB Cloud。

</DevToolCard>
<DevToolCard title="SQLAlchemy" logo="sqlalchemy" docLink="/tidbcloud/dev-guide-sample-application-python-sqlalchemy" githubLink="https://github.com/sqlalchemy/sqlalchemy">

使用 SQLAlchemy ORM 连接到 TiDB Cloud。

</DevToolCard>
<DevToolCard title="peewee" logo="peewee" docLink="/tidbcloud/dev-guide-sample-application-python-peewee" githubLink="https://github.com/coleifer/peewee">

使用 Peewee ORM 连接到 TiDB Cloud。

</DevToolCard>
</DevLangAccordion>

<DevLangAccordion label="Java">
<DevToolCard title="JDBC" logo="java" docLink="/tidbcloud/dev-guide-sample-application-java-jdbc" githubLink="https://github.com/mysql/mysql-connector-j">

使用 JDBC（MySQL Connector/J）连接到 TiDB Cloud。

</DevToolCard>
<DevToolCard title="MyBatis" logo="mybatis" docLink="/tidbcloud/dev-guide-sample-application-java-mybatis" githubLink="https://github.com/mybatis/mybatis-3">

使用 MyBatis ORM 连接到 TiDB Cloud。

</DevToolCard>
<DevToolCard title="Hibernate" logo="hibernate" docLink="/tidbcloud/dev-guide-sample-application-java-hibernate" githubLink="https://github.com/hibernate/hibernate-orm">

使用 Hibernate ORM 连接到 TiDB Cloud。

</DevToolCard>
<DevToolCard title="Spring Boot" logo="spring" docLink="/tidbcloud/dev-guide-sample-application-java-spring-boot" githubLink="https://github.com/spring-projects/spring-data-jpa">

使用 Spring Data JPA 将基于 Spring 的应用程序连接到 TiDB Cloud。

</DevToolCard>
</DevLangAccordion>

<DevLangAccordion label="Go">
<DevToolCard title="Go-MySQL-Driver" logo="go" docLink="/tidbcloud/dev-guide-sample-application-golang-sql-driver" githubLink="https://github.com/go-sql-driver/mysql">

使用 Go 的 MySQL 驱动程序连接到 TiDB Cloud。

</DevToolCard>
<DevToolCard title="GORM" logo="gorm" docLink="/tidbcloud/dev-guide-sample-application-golang-gorm" githubLink="https://github.com/go-gorm/gorm">

使用 GORM 连接到 TiDB Cloud。

</DevToolCard>
</DevLangAccordion>

<DevLangAccordion label="Ruby">
<DevToolCard title="Ruby on Rails" logo="rails" docLink="/tidbcloud/dev-guide-sample-application-ruby-rails" githubLink="https://github.com/rails/rails/tree/main/activerecord">

使用 Active Record ORM 将 Ruby on Rails 应用程序连接到 TiDB Cloud。

</DevToolCard>
<DevToolCard title="mysql2" logo="ruby" docLink="/tidbcloud/dev-guide-sample-application-ruby-mysql2" githubLink="https://github.com/brianmario/mysql2">

使用 mysql2 驱动程序连接到 TiDB Cloud。

</DevToolCard>
</DevLangAccordion>

除了这些指南外，PingCAP 还与社区合作[支持第三方 MySQL 驱动程序、ORM 和工具](/develop/dev-guide-third-party-support.md)。

## 使用 MySQL 客户端软件

由于 TiDB 是一个兼容 MySQL 的数据库，您可以使用许多客户端工具连接到 TiDB Cloud 并像以前一样管理数据库。或者，使用我们的<a href="/tidbcloud/get-started-with-cli">命令行工具</a>连接和管理您的数据库。

<DevToolGroup>
<DevToolCard title="MySQL Workbench" logo="mysql-1" docLink="/tidbcloud/dev-guide-gui-mysql-workbench">

使用 MySQL Workbench 连接和管理 TiDB Cloud 数据库。

</DevToolCard>
<DevToolCard title="Visual Studio Code" logo="vscode" docLink="/tidbcloud/dev-guide-gui-vscode-sqltools">

使用 VSCode 中的 SQLTools 扩展连接和管理 TiDB Cloud 数据库。

</DevToolCard>
<DevToolCard title="DBeaver" logo="dbeaver" docLink="/tidbcloud/dev-guide-gui-dbeaver">

使用 DBeaver 连接和管理 TiDB Cloud 数据库。

</DevToolCard>
<DevToolCard title="DataGrip" logo="datagrip" docLink="/tidbcloud/dev-guide-gui-datagrip">

使用 JetBrains 的 DataGrip 连接和管理 TiDB Cloud 数据库。

</DevToolCard>
</DevToolGroup>

## 其他资源

了解使用 TiDB Cloud 开发的其他主题。

- 使用 <a href="/tidbcloud/get-started-with-cli">TiDB Cloud CLI</a> 开发、管理和部署您的应用程序。
- 探索 TiDB Cloud 与流行<a href="/tidbcloud/integrate-tidbcloud-with-airbyte">服务的集成</a>。
- 使用 [TiDB 数据库开发参考](/develop/dev-guide-schema-design-overview.md)来设计、交互、优化和排查数据和模式问题。
- 学习免费在线课程 [TiDB 入门](https://eng.edu.pingcap.com/catalog/info/id:203/?utm_source=docs-dev-guide)。

</CustomContent>

<CustomContent platform="tidb">

本指南是为应用程序开发人员编写的，但如果您对 TiDB 的内部工作原理感兴趣或想参与 TiDB 开发，请阅读 [TiDB 内核开发指南](https://pingcap.github.io/tidb-dev-guide/)以获取更多信息。

本教程展示了如何使用 TiDB 快速构建应用程序、TiDB 的可能用例以及如何处理常见问题。

在阅读本页之前，建议您阅读 [TiDB 数据库平台快速入门指南](/quick-start-with-tidb.md)。

## TiDB 基础知识

在开始使用 TiDB 之前，您需要了解 TiDB 工作原理的一些重要机制：

- 阅读 [TiDB 事务概述](/transaction-overview.md)以了解 TiDB 中事务的工作原理，或查看[应用程序开发人员的事务说明](/develop/dev-guide-transaction-overview.md)以了解应用程序开发所需的事务知识。
- 了解[应用程序与 TiDB 交互的方式](#应用程序与-tidb-交互的方式)。
- 要了解构建分布式数据库 TiDB 和 TiDB Cloud 的核心组件和概念，请参考免费在线课程 [TiDB 入门](https://eng.edu.pingcap.com/catalog/info/id:203/?utm_source=docs-dev-guide)。

## TiDB 事务机制

TiDB 支持分布式事务，并提供[乐观事务](/optimistic-transaction.md)和[悲观事务](/pessimistic-transaction.md)模式。当前版本的 TiDB 默认使用**悲观事务**模式，这使您可以像使用传统单体数据库（例如 MySQL）一样与 TiDB 进行事务操作。

您可以使用 [`BEGIN`](/sql-statements/sql-statement-begin.md) 开始事务，使用 `BEGIN PESSIMISTIC` 显式指定**悲观事务**，或使用 `BEGIN OPTIMISTIC` 显式指定**乐观事务**。之后，您可以提交（[`COMMIT`](/sql-statements/sql-statement-commit.md)）或回滚（[`ROLLBACK`](/sql-statements/sql-statement-rollback.md)）事务。

TiDB 保证 `BEGIN` 开始到 `COMMIT` 或 `ROLLBACK` 结束期间所有语句的原子性，即在此期间执行的所有语句要么全部成功，要么全部失败。这用于确保应用程序开发所需的数据一致性。

如果您不确定什么是**乐观事务**，请**_不要_**使用它。因为**乐观事务**要求应用程序能够正确处理 `COMMIT` 语句返回的[所有错误](/error-codes.md)。如果您不确定您的应用程序如何处理这些错误，请改用**悲观事务**。

## 应用程序与 TiDB 交互的方式

TiDB 高度兼容 MySQL 协议并支持[大多数 MySQL 语法和功能](/mysql-compatibility.md)，因此大多数 MySQL 连接库都与 TiDB 兼容。如果您的应用程序框架或语言没有来自 PingCAP 的官方适配，建议您使用 MySQL 的客户端库。越来越多的第三方库正在积极支持 TiDB 的不同功能。

由于 TiDB 兼容 MySQL 协议和 MySQL 语法，大多数支持 MySQL 的 ORM 也与 TiDB 兼容。

## 阅读更多

- [快速入门](/develop/dev-guide-build-cluster-in-cloud.md)
- [选择驱动程序或 ORM](/develop/dev-guide-choose-driver-or-orm.md)
- [连接到 TiDB](/develop/dev-guide-connect-to-tidb.md)
- [数据库模式设计](/develop/dev-guide-schema-design-overview.md)
- [写入数据](/develop/dev-guide-insert-data.md)
- [读取数据](/develop/dev-guide-get-data-from-single-table.md)
- [事务](/develop/dev-guide-transaction-overview.md)
- [优化](/develop/dev-guide-optimize-sql-overview.md)
- [示例应用程序](/develop/dev-guide-sample-application-java-spring-boot.md)

## 需要帮助？

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上询问社区，或[提交支持工单](/support.md)。

</CustomContent>
