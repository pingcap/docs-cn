---
title: Third-Party Tools Supported by TiDB
summary: Learn about third-party tools supported by TiDB.
---

# Third-Party Tools Supported by TiDB

> **Note:**
>
> This document only lists common [third-party tools](https://en.wikipedia.org/wiki/Third-party_source) supported by TiDB. Some other third-party tools are not listed, not because they are not supported, but because PingCAP is not sure whether they use features that are incompatible with TiDB.

TiDB is [highly compatible with the MySQL protocol](/mysql-compatibility.md), so most of the MySQL drivers, ORM frameworks, and other tools that adapt to MySQL are compatible with TiDB. This document focuses on these tools and their support levels for TiDB.

## Support Level

PingCAP works with the community and provides the following support levels for third-party tools:

- **_Full_**: Indicates that TiDB is already compatible with most functionalities of the corresponding third-party tool, and maintains compatibility with its newer versions. PingCAP will periodically conduct compatibility tests with the latest version of the tool.
- **_Compatible_**: Indicates that because the corresponding third-party tool is adapted to MySQL and TiDB is highly compatible with the MySQL protocol, so TiDB can use most features of the tool. However, PingCAP has not completed a full test on all features of the tool, which might lead to some unexpected behaviors.

> **Note:**
>
> Unless specified, support for [Application retry and error handling](/develop/dev-guide-transaction-troubleshoot.md#application-retry-and-error-handling) is not included for **Driver** or **ORM frameworks**.

If you encounter problems when connecting to TiDB using the tools listed in this document, please submit an [issue](https://github.com/pingcap/tidb/issues/new?assignees=&labels=type%2Fquestion&template=general-question.md) on GitHub with details to promote support on this tool.

## Driver

<table>
   <thead>
      <tr>
         <th>Language</th>
         <th>Driver</th>
         <th>Latest tested version</th>
         <th>Support level</th>
         <th>TiDB adapter</th>
         <th>Tutorial</th>
      </tr>
   </thead>
   <tbody>
      <tr>
         <td>Go</td>
         <td><a href="https://github.com/go-sql-driver/mysql" target="_blank" referrerpolicy="no-referrer-when-downgrade">Go-MySQL-Driver</a></td>
         <td>v1.6.0</td>
         <td>Full</td>
         <td>N/A</td>
         <td><a href="/tidb/dev/dev-guide-sample-application-golang-sql-driver">Connect to TiDB with Go-MySQL-Driver</a></td>
      </tr>
      <tr>
         <td>Java</td>
         <td><a href="https://dev.mysql.com/downloads/connector/j/" target="_blank" referrerpolicy="no-referrer-when-downgrade">JDBC</a></td>
         <td>8.0</td>
         <td>Full</td>
         <td>
            <ul>
               <li><a href="/tidb/dev/dev-guide-choose-driver-or-orm#java-drivers" data-href="/tidb/dev/dev-guide-choose-driver-or-orm#java-drivers">pingcap/mysql-connector-j</a></li>
               <li><a href="/tidb/dev/dev-guide-choose-driver-or-orm#tidb-loadbalance" data-href="/tidb/dev/dev-guide-choose-driver-or-orm#tidb-loadbalance">pingcap/tidb-loadbalance</a></li>
            </ul>
         </td>
         <td><a href="/tidb/dev/dev-guide-sample-application-java-jdbc">Connect to TiDB with JDBC</a></td>
      </tr>
   </tbody>
</table>

## ORM

<table>
   <thead>
      <tr>
         <th>Language</th>
         <th>ORM framework</th>
         <th>Latest tested version</th>
         <th>Support level</th>
         <th>TiDB adapter</th>
         <th>Tutorial</th>
      </tr>
   </thead>
   <tbody>
      <tr>
         <td rowspan="4">Go</td>
         <td><a href="https://github.com/go-gorm/gorm" target="_blank" referrerpolicy="no-referrer-when-downgrade">gorm</a></td>
         <td>v1.23.5</td>
         <td>Full</td>
         <td>N/A</td>
         <td><a href="/tidb/dev/dev-guide-sample-application-golang-gorm">Connect to TiDB with GORM</a></td>
      </tr>
      <tr>
         <td><a href="https://github.com/beego/beego" target="_blank" referrerpolicy="no-referrer-when-downgrade">beego</a></td>
         <td>v2.0.3</td>
         <td>Full</td>
         <td>N/A</td>
         <td>N/A</td>
      </tr>
      <tr>
         <td><a href="https://github.com/upper/db" target="_blank" referrerpolicy="no-referrer-when-downgrade">upper/db</a></td>
         <td>v4.5.2</td>
         <td>Full</td>
         <td>N/A</td>
         <td>N/A</td>
      </tr>
      <tr>
         <td><a href="https://gitea.com/xorm/xorm" target="_blank" referrerpolicy="no-referrer-when-downgrade">xorm</a></td>
         <td>v1.3.1</td>
         <td>Full</td>
         <td>N/A</td>
         <td>N/A</td>
      </tr>
      <tr>
         <td rowspan="4">Java</td>
         <td><a href="https://hibernate.org/orm/" target="_blank" referrerpolicy="no-referrer-when-downgrade">Hibernate</a></td>
         <td>6.1.0.Final</td>
         <td>Full</td>
         <td>N/A</td>
         <td><a href="/tidb/dev/dev-guide-sample-application-java-hibernate">Connect to TiDB with Hibernate</a></td>
      </tr>
      <tr>
         <td><a href="https://mybatis.org/mybatis-3/" target="_blank" referrerpolicy="no-referrer-when-downgrade">MyBatis</a></td>
         <td>v3.5.10</td>
         <td>Full</td>
         <td>N/A</td>
         <td><a href="/tidb/dev/dev-guide-sample-application-java-mybatis">Connect to TiDB with MyBatis</a></td>
      </tr>
      <tr>
         <td><a href="https://spring.io/projects/spring-data-jpa/" target="_blank" referrerpolicy="no-referrer-when-downgrade">Spring Data JPA</a></td>
         <td>2.7.2</td>
         <td>Full</td>
         <td>N/A</td>
         <td><a href="/tidb/dev/dev-guide-sample-application-java-spring-boot">Connect to TiDB with Spring Boot</a></td>
      </tr>
      <tr>
         <td><a href="https://github.com/jOOQ/jOOQ" target="_blank" referrerpolicy="no-referrer-when-downgrade">jOOQ</a></td>
         <td>v3.16.7 (Open Source)</td>
         <td>Full</td>
         <td>N/A</td>
         <td>N/A</td>
      </tr>
      <tr>
         <td>Ruby</td>
         <td><a href="https://guides.rubyonrails.org/active_record_basics.html" target="_blank" referrerpolicy="no-referrer-when-downgrade">Active Record</a></td>
         <td>v7.0</td>
         <td>Full</td>
         <td>N/A</td>
         <td><a href="/tidb/dev/dev-guide-sample-application-ruby-rails">Connect to TiDB with Rails Framework and ActiveRecord ORM</a></td>
      </tr>
      <tr>
         <td rowspan="3">JavaScript / TypeScript</td>
         <td><a href="https://sequelize.org/" target="_blank" referrerpolicy="no-referrer-when-downgrade">Sequelize</a></td>
         <td>v6.20.1</td>
         <td>Full</td>
         <td>N/A</td>
         <td><a href="/tidb/dev/dev-guide-sample-application-nodejs-sequelize">Connect to TiDB with Sequelize</a></td>
      </tr>
      <tr>
         <td><a href="https://www.prisma.io/" target="_blank" referrerpolicy="no-referrer-when-downgrade">Prisma</a></td>
         <td>4.16.2</td>
         <td>Full</td>
         <td>N/A</td>
         <td><a href="/tidb/dev/dev-guide-sample-application-nodejs-prisma">Connect to TiDB with Prisma</a></td>
      </tr>
      <tr>
         <td><a href="https://typeorm.io/" target="_blank" referrerpolicy="no-referrer-when-downgrade">TypeORM</a></td>
         <td>v0.3.17</td>
         <td>Full</td>
         <td>N/A</td>
         <td><a href="/tidb/dev/dev-guide-sample-application-nodejs-typeorm">Connect to TiDB with TypeORM</a></td>
      </tr>
      <tr>
         <td rowspan="2">Python</td>
         <td><a href="https://pypi.org/project/Django/" target="_blank" referrerpolicy="no-referrer-when-downgrade">Django</a></td>
         <td>v4.2</td>
         <td>Full</td>
         <td><a href="https://github.com/pingcap/django-tidb" target="_blank" referrerpolicy="no-referrer-when-downgrade">django-tidb</a></td>
         <td><a href="/tidb/dev/dev-guide-sample-application-python-django">Connect to TiDB with Django</a></td>
      </tr>
      <tr>
         <td><a href="https://www.sqlalchemy.org/" target="_blank" referrerpolicy="no-referrer-when-downgrade">SQLAlchemy</a></td>
         <td>v1.4.37</td>
         <td>Full</td>
         <td>N/A</td>
         <td><a href="/tidb/dev/dev-guide-sample-application-python-sqlalchemy">Connect to TiDB with SQLAlchemy</a></td>
      </tr>
   </tbody>
</table>

## GUI

| GUI                                                       | Latest tested version | Support level | Tutorial                                                                      |
|-----------------------------------------------------------|-----------------------|---------------|-------------------------------------------------------------------------------|
| [JetBrains DataGrip](https://www.jetbrains.com/datagrip/) | 2023.2.1              | Full          | [Connect to TiDB with JetBrains DataGrip](/develop/dev-guide-gui-datagrip.md) |
| [DBeaver](https://dbeaver.io/)                            | 23.0.3                | Full          | [Connect to TiDB with DBeaver](/develop/dev-guide-gui-dbeaver.md)             |
| [Visual Studio Code](https://code.visualstudio.com/)                            | 1.72.0                | Full          | [Connect to TiDB with Visual Studio Code](/develop/dev-guide-gui-vscode-sqltools.md)             |
