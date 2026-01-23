---
title: Developer Guide Overview
summary: Introduce the overview of the developer guide for TiDB Cloud and TiDB Self-Managed.
aliases: ['/tidbcloud/dev-guide-overview/','/tidb/dev/dev-guide-overview/']
---

# Developer Guide Overview

<IntroHero title="Learn TiDB Cloud basics" content="TiDB Cloud is the fully-managed service built on top of TiDB, which is highly compatible with the MySQL protocol and supports most MySQL syntax and features." videoTitle="TiDB Cloud in 3 minutes">
  <IntroHeroVideo src="https://www.youtube.com/embed/skCV9BEmjbo?autoplay=1" title="TiDB Cloud in 3 minutes" />
</IntroHero>

## Guides by language and framework

Build your application with the language you use by following the guides with sample codes.

<DevLangAccordion label="JavaScript" defaultExpanded>
<DevToolCard title="Serverless Driver (beta)" logo="tidb" docLink="/developer/serverless-driver" githubLink="https://github.com/tidbcloud/serverless-js">

Connect to TiDB over HTTPS from edge environments.

</DevToolCard>
<DevToolCard title="Next.js" logo="nextjs" docLink="/developer/dev-guide-sample-application-nextjs" githubLink="https://github.com/vercel/next.js">

Connect Next.js with mysql2 to TiDB.

</DevToolCard>
<DevToolCard title="Prisma" logo="prisma" docLink="/developer/dev-guide-sample-application-nodejs-prisma" githubLink="https://github.com/prisma/prisma">

Connect to TiDB with Prisma ORM.

</DevToolCard>
<DevToolCard title="TypeORM" logo="typeorm" docLink="/developer/dev-guide-sample-application-nodejs-typeorm" githubLink="https://github.com/typeorm/typeorm">

Connect to TiDB with TypeORM.

</DevToolCard>
<DevToolCard title="Sequelize" logo="sequelize" docLink="/developer/dev-guide-sample-application-nodejs-sequelize" githubLink="https://github.com/sequelize/sequelize">

Connect to TiDB with Sequelize ORM.

</DevToolCard>
<DevToolCard title="mysql.js" logo="mysql" docLink="/developer/dev-guide-sample-application-nodejs-mysqljs" githubLink="https://github.com/mysqljs/mysql">

Connect Node.js with mysql.js module to TiDB.

</DevToolCard>
<DevToolCard title="node-mysql2" logo="mysql" docLink="/developer/dev-guide-sample-application-nodejs-mysql2" githubLink="https://github.com/sidorares/node-mysql2">

Connect Node.js with node-mysql2 module to TiDB.

</DevToolCard>
<DevToolCard title="AWS Lambda" logo="aws-lambda" docLink="/developer/dev-guide-sample-application-aws-lambda" githubLink="https://github.com/sidorares/node-mysql2">

Connect AWS Lambda Function with mysql2 to TiDB.

</DevToolCard>
</DevLangAccordion>

<DevLangAccordion label="Python" defaultExpanded>
<DevToolCard title="Django" logo="django" docLink="/developer/dev-guide-sample-application-python-django" githubLink="https://github.com/pingcap/django-tidb">

Connect Django application with django-tidb to TiDB.

</DevToolCard>
<DevToolCard title="MySQL Connector/Python" logo="python" docLink="/developer/dev-guide-sample-application-python-mysql-connector" githubLink="https://github.com/mysql/mysql-connector-python">

Connect to TiDB with the official MySQL package.

</DevToolCard>
<DevToolCard title="PyMySQL" logo="python" docLink="/developer/dev-guide-sample-application-python-pymysql" githubLink="https://github.com/PyMySQL/PyMySQL">

Connect to TiDB with PyMySQL package.

</DevToolCard>
<DevToolCard title="mysqlclient" logo="python" docLink="/developer/dev-guide-sample-application-python-mysqlclient" githubLink="https://github.com/PyMySQL/mysqlclient">

Connect to TiDB with mysqlclient package.

</DevToolCard>
<DevToolCard title="SQLAlchemy" logo="sqlalchemy" docLink="/developer/dev-guide-sample-application-python-sqlalchemy" githubLink="https://github.com/sqlalchemy/sqlalchemy">

Connect to TiDB with SQLAlchemy ORM.

</DevToolCard>
<DevToolCard title="peewee" logo="peewee" docLink="/developer/dev-guide-sample-application-python-peewee" githubLink="https://github.com/coleifer/peewee">

Connect to TiDB with Peewee ORM.

</DevToolCard>
</DevLangAccordion>

<DevLangAccordion label="Java">
<DevToolCard title="JDBC" logo="java" docLink="/developer/dev-guide-sample-application-java-jdbc" githubLink="https://github.com/mysql/mysql-connector-j">

Connect to TiDB with JDBC (MySQL Connector/J).

</DevToolCard>
<DevToolCard title="MyBatis" logo="mybatis" docLink="/developer/dev-guide-sample-application-java-mybatis" githubLink="https://github.com/mybatis/mybatis-3">

Connect to TiDB with MyBatis ORM.

</DevToolCard>
<DevToolCard title="Hibernate" logo="hibernate" docLink="/developer/dev-guide-sample-application-java-hibernate" githubLink="https://github.com/hibernate/hibernate-orm">

Connect to TiDB with Hibernate ORM.

</DevToolCard>
<DevToolCard title="Spring Boot" logo="spring" docLink="/developer/dev-guide-sample-application-java-spring-boot" githubLink="https://github.com/spring-projects/spring-data-jpa">

Connect Spring based application with Spring Data JPA to TiDB.

</DevToolCard>
</DevLangAccordion>

<DevLangAccordion label="Go">
<DevToolCard title="Go-MySQL-Driver" logo="go" docLink="/developer/dev-guide-sample-application-golang-sql-driver" githubLink="https://github.com/go-sql-driver/mysql">

Connect to TiDB with MySQL driver for Go.

</DevToolCard>
<DevToolCard title="GORM" logo="gorm" docLink="/developer/dev-guide-sample-application-golang-gorm" githubLink="https://github.com/go-gorm/gorm">

Connect to TiDB with GORM.

</DevToolCard>
</DevLangAccordion>

<DevLangAccordion label="Ruby">
<DevToolCard title="Ruby on Rails" logo="rails" docLink="/developer/dev-guide-sample-application-ruby-rails" githubLink="https://github.com/rails/rails/tree/main/activerecord">

Connect Ruby on Rails application with Active Record ORM to TiDB.

</DevToolCard>
<DevToolCard title="mysql2" logo="ruby" docLink="/developer/dev-guide-sample-application-ruby-mysql2" githubLink="https://github.com/brianmario/mysql2">

Connect to TiDB with mysql2 driver.

</DevToolCard>
</DevLangAccordion>

In addition to these guides, PingCAP works with the community to support [third-party MySQL drivers, ORMs, and tools](/develop/dev-guide-third-party-support.md).

## Use MySQL client software

As TiDB is a MySQL-compatible database, you can use many familiar client software tools to connect to TiDB and manage your databases. Or, you can use our <a href="/tidbcloud/get-started-with-cli">command line tool</a> to connect and manage your databases.

<DevToolGroup>
<DevToolCard title="MySQL Workbench" logo="mysql-1" docLink="/developer/dev-guide-gui-mysql-workbench">

Connect and manage TiDB databases with MySQL Workbench.

</DevToolCard>
<DevToolCard title="Visual Studio Code" logo="vscode" docLink="/developer/dev-guide-gui-vscode-sqltools">

Connect and manage TiDB databases with the SQLTools extension in VS Code.

</DevToolCard>
<DevToolCard title="DBeaver" logo="dbeaver" docLink="/developer/dev-guide-gui-dbeaver">

Connect and manage TiDB databases with DBeaver.

</DevToolCard>
<DevToolCard title="DataGrip" logo="datagrip" docLink="/developer/dev-guide-gui-datagrip">

Connect and manage TiDB databases with DataGrip by JetBrains.

</DevToolCard>
</DevToolGroup>

## Additional resources

Learn other topics about developing with TiDB.

- Use <a href="/tidbcloud/get-started-with-cli">TiDB Cloud CLI</a> to develop, manage and deploy your applications.
- Explore popular <a href="/tidbcloud/integrate-tidbcloud-with-airbyte">service integrations</a> with TiDB Cloud.
- Follow [TiDB database development reference](/develop/dev-guide-schema-design-overview.md) to design, interact with, optimize, and troubleshoot your data and schema.
- Follow the free online course [Introduction to TiDB](https://eng.edu.pingcap.com/catalog/info/id:203/?utm_source=docs-dev-guide).