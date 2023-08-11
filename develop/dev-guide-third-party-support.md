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
         <td>C</td>
         <td><a href="https://dev.mysql.com/doc/c-api/8.0/en/c-api-introduction.html" target="_blank" referrerpolicy="no-referrer-when-downgrade">libmysqlclient</a></td>
         <td>8.0</td>
         <td>Compatible</td>
         <td>N/A</td>
         <td>N/A</td>
      </tr>
      <tr>
         <td>C#(.Net)</td>
         <td><a href="https://downloads.mysql.com/archives/c-net/" target="_blank" referrerpolicy="no-referrer-when-downgrade">MySQL Connector/NET</a></td>
         <td>8.0</td>
         <td>Compatible</td>
         <td>N/A</td>
         <td>N/A</td>
      </tr>
      <tr>
         <td>ODBC</td>
         <td><a href="https://downloads.mysql.com/archives/c-odbc/" target="_blank" referrerpolicy="no-referrer-when-downgrade">MySQL Connector/ODBC</a></td>
         <td>8.0</td>
         <td>Compatible</td>
         <td>N/A</td>
         <td>N/A</td>
      </tr>
      <tr>
         <td>Go</td>
         <td><a href="https://github.com/go-sql-driver/mysql" target="_blank" referrerpolicy="no-referrer-when-downgrade">Go-MySQL-Driver</a></td>
         <td>v1.6.0</td>
         <td>Full</td>
         <td>N/A</td>
         <td><a href="/tidb/dev/dev-guide-sample-application-golang-sql-driver">Build a Simple CRUD App with TiDB and Go-MySQL-Driver</a></td>
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
         <td><a href="/tidb/dev/dev-guide-sample-application-java-jdbc">Build a Simple CRUD App with TiDB and JDBC</a></td>
      </tr>
      <tr>
         <td>JavaScript</td>
         <td><a href="https://github.com/mysqljs/mysql" target="_blank" referrerpolicy="no-referrer-when-downgrade">mysql</a></td>
         <td>v2.18.1</td>
         <td>Compatible</td>
         <td>N/A</td>
         <td>N/A</td>
      </tr>
      <tr>
         <td>PHP</td>
         <td><a href="https://dev.mysql.com/downloads/connector/php-mysqlnd/" target="_blank" referrerpolicy="no-referrer-when-downgrade">mysqlnd</a></td>
         <td>PHP 5.4+</td>
         <td>Compatible</td>
         <td>N/A</td>
         <td>N/A</td>
      </tr>
      <tr>
         <td rowspan="3">Python</td>
         <td><a href="https://dev.mysql.com/doc/connector-python/en/" target="_blank" referrerpolicy="no-referrer-when-downgrade">MySQL Connector/Python</a></td>
         <td>8.0</td>
         <td>Compatible</td>
         <td>N/A</td>
         <td><a href="/tidb/dev/dev-guide-sample-application-python-mysql-connector">Build a Simple CRUD App with TiDB and MySQL Connector/Python</a></td>
      </tr>
      <tr>
         <td><a href="https://mysqlclient.readthedocs.io/" target="_blank" referrerpolicy="no-referrer-when-downgrade">mysqlclient</a></td>
         <td>2.1.1</td>
         <td>Compatible</td>
         <td>N/A</td>
         <td><a href="/tidb/dev/dev-guide-sample-application-python-mysqlclient">Build a Simple CRUD App with TiDB and mysqlclient</a></td>
      </tr>
      <tr>
         <td><a href="https://pypi.org/project/PyMySQL/" target="_blank" referrerpolicy="no-referrer-when-downgrade">PyMySQL</a></td>
         <td>1.0.2</td>
         <td>Compatible</td>
         <td>N/A</td>
         <td><a href="/tidb/dev/dev-guide-sample-application-python-pymysql">Build a Simple CRUD App with TiDB and PyMySQL</a></td>
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
         <td rowspan="5">Go</td>
         <td><a href="https://github.com/go-gorm/gorm" target="_blank" referrerpolicy="no-referrer-when-downgrade">gorm</a></td>
         <td>v1.23.5</td>
         <td>Full</td>
         <td>N/A</td>
         <td><a href="/tidb/dev/dev-guide-sample-application-golang-gorm">Build a Simple CRUD App with TiDB and GORM</a></td>
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
         <td><a href="https://github.com/ent/ent" target="_blank" referrerpolicy="no-referrer-when-downgrade">ent</a></td>
         <td>v0.11.0</td>
         <td>Compatible</td>
         <td>N/A</td>
         <td>N/A</td>
      </tr>
      <tr>
         <td rowspan="4">Java</td>
         <td><a href="https://hibernate.org/orm/" target="_blank" referrerpolicy="no-referrer-when-downgrade">Hibernate</a></td>
         <td>6.1.0.Final</td>
         <td>Full</td>
         <td>N/A</td>
         <td><a href="/tidb/dev/dev-guide-sample-application-java-hibernate">Build a Simple CRUD App with TiDB and Hibernate</a></td>
      </tr>
      <tr>
         <td><a href="https://mybatis.org/mybatis-3/" target="_blank" referrerpolicy="no-referrer-when-downgrade">MyBatis</a></td>
         <td>v3.5.10</td>
         <td>Full</td>
         <td>N/A</td>
         <td><a href="/tidb/dev/dev-guide-sample-application-java-mybatis">Build a Simple CRUD App with TiDB and MyBatis</a></td>
      </tr>
      <tr>
         <td><a href="https://spring.io/projects/spring-data-jpa/" target="_blank" referrerpolicy="no-referrer-when-downgrade">Spring Data JPA</a></td>
         <td>2.7.2</td>
         <td>Full</td>
         <td>N/A</td>
         <td><a href="/tidb/dev/dev-guide-sample-application-java-spring-boot">Build a Simple CRUD App with TiDB and Spring Boot</a></td>
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
         <td>N/A</td>
      </tr>
      <tr>
         <td rowspan="4">JavaScript / TypeScript</td>
         <td><a href="https://www.npmjs.com/package/sequelize" target="_blank" referrerpolicy="no-referrer-when-downgrade">sequelize</a></td>
         <td>v6.20.1</td>
         <td>Full</td>
         <td>N/A</td>
         <td>N/A</td>
      </tr>
      <tr>
         <td><a href="https://knexjs.org/" target="_blank" referrerpolicy="no-referrer-when-downgrade">Knex.js</a></td>
         <td>v1.0.7</td>
         <td>Compatible</td>
         <td>N/A</td>
         <td>N/A</td>
      </tr>
      <tr>
         <td><a href="https://www.prisma.io/" target="_blank" referrerpolicy="no-referrer-when-downgrade">Prisma Client</a></td>
         <td>4.16.2</td>
         <td>Full</td>
         <td>N/A</td>
         <td>N/A</td>
      </tr>
      <tr>
         <td><a href="https://www.npmjs.com/package/typeorm" target="_blank" referrerpolicy="no-referrer-when-downgrade">TypeORM</a></td>
         <td>v0.3.6</td>
         <td>Compatible</td>
         <td>N/A</td>
         <td>N/A</td>
      </tr>
      <tr>
         <td>PHP</td>
         <td><a href="https://laravel.com/" target="_blank" referrerpolicy="no-referrer-when-downgrade">laravel</a></td>
         <td>v9.1.10</td>
         <td>Compatible</td>
         <td><a href="https://github.com/colopl/laravel-tidb" target="_blank" referrerpolicy="no-referrer-when-downgrade">laravel-tidb</a></td>
         <td>N/A</td>
      </tr>
      <tr>
         <td rowspan="4">Python</td>
         <td><a href="https://pypi.org/project/Django/" target="_blank" referrerpolicy="no-referrer-when-downgrade">Django</a></td>
         <td>v4.1</td>
         <td>Full</td>
         <td><a href="https://github.com/pingcap/django-tidb" target="_blank" referrerpolicy="no-referrer-when-downgrade">django-tidb</a></td>
         <td>N/A</td>
      </tr>
      <tr>
         <td><a href="https://www.sqlalchemy.org/" target="_blank" referrerpolicy="no-referrer-when-downgrade">SQLAlchemy</a></td>
         <td>v1.4.37</td>
         <td>Full</td>
         <td>N/A</td>
         <td><a href="/tidb/dev/dev-guide-sample-application-python-sqlalchemy">Build a Simple CRUD App with TiDB and SQLAlchemy</a></td>
      </tr>
      <tr>
         <td><a href="https://github.com/coleifer/peewee/" target="_blank" referrerpolicy="no-referrer-when-downgrade">peewee</a></td>
         <td>v3.14.10</td>
         <td>Compatible</td>
         <td>N/A</td>
         <td><a href="/tidb/dev/dev-guide-sample-application-python-peewee">Build a Simple CRUD App with TiDB and peewee</a></td>
      </tr>
   </tbody>
</table>

## GUI

| GUI | Latest tested version | Support level | Tutorial |
| - | - | - | - |
| [DBeaver](https://dbeaver.io/) | 22.1.0 | Compatible | N/A |
| [Navicat for MySQL](https://www.navicat.com/) | 16.0.14 | Compatible | N/A |
| [MySQL Workbench](https://www.mysql.com/products/workbench/) | 8.0 | Compatible | N/A |

<table>
   <thead>
      <tr>
         <th>IDE</th>
         <th>Plugin</th>
         <th>Support level</th>
         <th>Tutorial</th>
      </tr>
   </thead>
   <tbody>
      <tr>
         <td><a href="https://www.jetbrains.com/datagrip/" target="_blank" referrerpolicy="no-referrer-when-downgrade">DataGrip</a></td>
         <td>N/A</td>
         <td>Compatible</td>
         <td>N/A</td>
      </tr>
      <tr>
         <td><a href="https://www.jetbrains.com/idea/" target="_blank" referrerpolicy="no-referrer-when-downgrade">IntelliJ IDEA</a></td>
         <td>N/A</td>
         <td>Compatible</td>
         <td>N/A</td>
      </tr>
      <tr>
         <td rowspan="2"><a href="https://code.visualstudio.com/" target="_blank" referrerpolicy="no-referrer-when-downgrade">Visual Studio Code</a></td>
         <td><a href="https://marketplace.visualstudio.com/items?itemName=dragonly.ticode" target="_blank" referrerpolicy="no-referrer-when-downgrade">TiDE</a></td>
         <td>Compatible</td>
         <td>N/A</td>
      </tr>
      <tr>
         <td><a href="https://marketplace.visualstudio.com/items?itemName=formulahendry.vscode-mysql" target="_blank" referrerpolicy="no-referrer-when-downgrade">MySQL</a></td>
         <td>Compatible</td>
         <td>N/A</td>
      </tr>
   </tbody>
</table>
