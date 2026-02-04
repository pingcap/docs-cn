<!-- markdownlint-disable MD007 -->
<!-- markdownlint-disable MD041 -->

# 目录

## 快速上手

- [创建 {{{ .starter }}} 集群](/develop/dev-guide-build-cluster-in-cloud.md)
- [TiDB 基础](/develop/dev-guide-tidb-basics.md)
- [使用 TiDB 的增删改查 SQL](/develop/dev-guide-tidb-crud-sql.md)

## 开发指南

- 连接到 TiDB
  - [概览](/develop/dev-guide-connect-to-tidb.md)
  - 通过 CLI 或 GUI 连接
    - [MySQL Workbench](/develop/dev-guide-gui-mysql-workbench.md)
    - [Navicat](/develop/dev-guide-gui-navicat.md)
    - [Looker Studio](/develop/dev-guide-bi-looker-studio.md)
  - 通过驱动或 ORM 框架连接
    - [选择驱动或 ORM 框架](/develop/dev-guide-choose-driver-or-orm.md)
    - Java
      - [JDBC](/develop/dev-guide-sample-application-java-jdbc.md)
      - [MyBatis](/develop/dev-guide-sample-application-java-mybatis.md)
      - [Hibernate](/develop/dev-guide-sample-application-java-hibernate.md)
      - [Spring Boot](/develop/dev-guide-sample-application-java-spring-boot.md)
      - [配置连接池与连接参数](/develop/dev-guide-connection-parameters.md)
      - [开发 Java 应用的最佳实践](/develop/java-app-best-practices.md)
    - Go
      - [Go-MySQL-Driver](/develop/dev-guide-sample-application-golang-sql-driver.md)
      - [GORM](/develop/dev-guide-sample-application-golang-gorm.md)
    - Python
      - [mysqlclient](/develop/dev-guide-sample-application-python-mysqlclient.md)
      - [MySQL Connector/Python](/develop/dev-guide-sample-application-python-mysql-connector.md)
      - [PyMySQL](/develop/dev-guide-sample-application-python-pymysql.md)
      - [SQLAlchemy](/develop/dev-guide-sample-application-python-sqlalchemy.md)
      - [peewee](/develop/dev-guide-sample-application-python-peewee.md)
      - [Django](/develop/dev-guide-sample-application-python-django.md)
    - Node.js
      - [node-mysql2](/develop/dev-guide-sample-application-nodejs-mysql2.md)
      - [mysql.js](/develop/dev-guide-sample-application-nodejs-mysqljs.md)
      - [Prisma](/develop/dev-guide-sample-application-nodejs-prisma.md)
      - [Sequelize](/develop/dev-guide-sample-application-nodejs-sequelize.md)
      - [TypeORM](/develop/dev-guide-sample-application-nodejs-typeorm.md)
      - [Next.js](/develop/dev-guide-sample-application-nextjs.md)
      - [AWS Lambda](/develop/dev-guide-sample-application-aws-lambda.md)
    - Ruby
      - [mysql2](/develop/dev-guide-sample-application-ruby-mysql2.md)
      - [Rails](/develop/dev-guide-sample-application-ruby-rails.md)
    - C#
      - [C#](/develop/dev-guide-sample-application-cs.md)
  - 通过 TiDB Cloud Serverless Driver 连接 ![BETA](/media/blank_transparent_placeholder.png)
    - [概览](/develop/serverless-driver.md)
    - [Node.js 示例](/develop/serverless-driver-node-example.md)
    - [Prisma 示例](/develop/serverless-driver-prisma-example.md)
    - [Kysely 示例](/develop/serverless-driver-kysely-example.md)
    - [Drizzle 示例](/develop/serverless-driver-drizzle-example.md)
- 数据库模式设计
  - [概览](/develop/dev-guide-schema-design-overview.md)
  - [创建数据库](/develop/dev-guide-create-database.md)
  - [创建表](/develop/dev-guide-create-table.md)
  - [创建二级索引](/develop/dev-guide-create-secondary-indexes.md)
- 数据写入
  - [插入数据](/develop/dev-guide-insert-data.md)
  - [更新数据](/develop/dev-guide-update-data.md)
  - [删除数据](/develop/dev-guide-delete-data.md)
  - [使用 TTL (Time to Live) 定期删除过期数据](/time-to-live.md)
  - [预处理语句](/develop/dev-guide-prepared-statement.md)
- 数据读取
  - [单表读取](/develop/dev-guide-get-data-from-single-table.md)
  - [多表连接查询](/develop/dev-guide-join-tables.md)
  - [子查询](/develop/dev-guide-use-subqueries.md)
  - [查询结果分页](/develop/dev-guide-paginate-results.md)
  - [视图](/develop/dev-guide-use-views.md)
  - [临时表](/develop/dev-guide-use-temporary-tables.md)
  - [公共表表达式](/develop/dev-guide-use-common-table-expression.md)
  - 读取副本数据
    - [Follower Read](/develop/dev-guide-use-follower-read.md)
    - [Stale Read](/develop/dev-guide-use-stale-read.md)
  - [HTAP 查询](/develop/dev-guide-hybrid-oltp-and-olap-queries.md)
- [向量搜索](/develop/dev-guide-vector-search.md) ![BETA](/media/blank_transparent_placeholder.png)
- 事务处理
  - [概览](/develop/dev-guide-transaction-overview.md)
  - [乐观事务和悲观事务](/develop/dev-guide-optimistic-and-pessimistic-transaction.md)
  - [事务限制](/develop/dev-guide-transaction-restraints.md)
  - [事务错误处理](/develop/dev-guide-transaction-troubleshoot.md)
- 优化 SQL 性能
  - [概览](/develop/dev-guide-optimize-sql-overview.md)
  - [SQL 性能调优](/develop/dev-guide-optimize-sql.md)
  - [性能调优最佳实践](/develop/dev-guide-optimize-sql-best-practices.md)
  - [索引的最佳实践](/develop/dev-guide-index-best-practice.md)
  - 其他优化
    - [避免隐式类型转换](/develop/dev-guide-implicit-type-conversion.md)
    - [唯一序列号生成方案](/develop/dev-guide-unique-serial-number-generation.md)
- 故障诊断
  - [SQL 或事务问题](/develop/dev-guide-troubleshoot-overview.md)
  - [结果集不稳定](/develop/dev-guide-unstable-result-set.md)
  - [超时](/develop/dev-guide-timeouts-in-tidb.md)

## 集成

- 第三方工具支持
  - [TiDB 支持的第三方工具](/develop/dev-guide-third-party-support.md)
  - [已知的第三方工具兼容问题](/develop/dev-guide-third-party-tools-compatibility.md)
- [ProxySQL](/develop/dev-guide-proxysql-integration.md)
- [Amazon AppFlow](/develop/dev-guide-aws-appflow-integration.md)
- [WordPress](/develop/dev-guide-wordpress.md)

## 参考指南

- 开发规范
  - [命名规范](/develop/dev-guide-object-naming-guidelines.md)
  - [SQL 开发规范](/develop/dev-guide-sql-development-specification.md)
- [Bookshop 示例应用](/develop/dev-guide-bookshop-schema-design.md)
- 云原生开发环境
  - [Gitpod](/develop/dev-guide-playground-gitpod.md)