---
title: TiDB 支持的第三方工具
summary: TiDB 支持的第三方工具主要包括驱动、ORM 框架和 GUI。支持等级分为 Full 和 Compatible，其中 Full 表示绝大多数功能兼容性已得到支持，Compatible 表示大部分功能可使用但未经完整验证。对于支持的 Driver 或 ORM 框架并不包括应用端事务重试和错误处理。如果在使用工具连接 TiDB 时出现问题，可在 GitHub 上提交包含详细信息的 issue 以获得进展。
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

<table>
   <thead>
      <tr>
         <th>编程语言</th>
         <th>驱动</th>
         <th>最新已测试版本</th>
         <th>支持等级</th>
         <th>TiDB 适配器</th>
         <th>教程</th>
      </tr>
   </thead>
   <tbody>
      <tr>
         <td>Go</td>
         <td><a href="https://github.com/go-sql-driver/mysql" target="_blank" referrerpolicy="no-referrer-when-downgrade">Go-MySQL-Driver</a></td>
         <td>v1.6.0</td>
         <td>Full</td>
         <td>N/A</td>
         <td><a href="https://docs.pingcap.com/zh/tidb/dev/dev-guide-sample-application-golang-sql-driver">使用 Go-MySQL-Driver 连接到 TiDB</a></td>
      </tr>
      <tr>
         <td>Java</td>
         <td><a href="https://dev.mysql.com/downloads/connector/j/" target="_blank" referrerpolicy="no-referrer-when-downgrade">JDBC</a></td>
         <td>8.0</td>
         <td>Full</td>
         <td>
            <ul>
               <li><a href="https://docs.pingcap.com/zh/tidb/dev/dev-guide-choose-driver-or-orm#java-drivers" data-href="https://docs.pingcap.com/zh/tidb/dev/dev-guide-choose-driver-or-orm#java-drivers">pingcap/mysql-connector-j</a></li>
               <li><a href="https://docs.pingcap.com/zh/tidb/dev/dev-guide-choose-driver-or-orm#tidb-loadbalance" data-href="https://docs.pingcap.com/zh/tidb/dev/dev-guide-choose-driver-or-orm#tidb-loadbalance">pingcap/tidb-loadbalance</a></li>
            </ul>
         </td>
         <td><a href="https://docs.pingcap.com/zh/tidb/dev/dev-guide-sample-application-java-jdbc">使用 JDBC 连接到 TiDB</a></td>
      </tr>
   </tbody>
</table>

## ORM

<table>
   <thead>
      <tr>
         <th>编程语言</th>
         <th>ORM 框架</th>
         <th>最新已测试版本</th>
         <th>支持等级</th>
         <th>TiDB 适配器</th>
         <th>教程</th>
      </tr>
   </thead>
   <tbody>
      <tr>
         <td rowspan="4">Go</td>
         <td><a href="https://github.com/go-gorm/gorm" target="_blank" referrerpolicy="no-referrer-when-downgrade">gorm</a></td>
         <td>v1.23.5</td>
         <td>Full</td>
         <td>N/A</td>
         <td><a href="https://docs.pingcap.com/zh/tidb/dev/dev-guide-sample-application-golang-gorm">使用 GORM 连接到 TiDB</a></td>
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
         <td><a href="https://docs.pingcap.com/zh/tidb/dev/dev-guide-sample-application-java-hibernate">使用 Hibernate 连接到 TiDB</a></td>
      </tr>
      <tr>
         <td><a href="https://mybatis.org/mybatis-3/" target="_blank" referrerpolicy="no-referrer-when-downgrade">MyBatis</a></td>
         <td>v3.5.10</td>
         <td>Full</td>
         <td>N/A</td>
         <td><a href="https://docs.pingcap.com/zh/tidb/dev/dev-guide-sample-application-java-mybatis">使用 MyBatis 连接到 TiDB</a></td>
      </tr>
      <tr>
         <td><a href="https://spring.io/projects/spring-data-jpa/" target="_blank" referrerpolicy="no-referrer-when-downgrade">Spring Data JPA</a></td>
         <td>2.7.2</td>
         <td>Full</td>
         <td>N/A</td>
         <td><a href="https://docs.pingcap.com/zh/tidb/dev/dev-guide-sample-application-java-spring-boot">使用 Spring Boot 连接到 TiDB</a></td>
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
         <td><a href="https://docs.pingcap.com/zh/tidb/dev/dev-guide-sample-application-ruby-rails">使用 Rails 框架和 ActiveRecord ORM 连接到 TiDB</a></td>
      </tr>
      <tr>
         <td rowspan="3">JavaScript / TypeScript</td>
         <td><a href="https://sequelize.org/" target="_blank" referrerpolicy="no-referrer-when-downgrade">Sequelize</a></td>
         <td>v6.20.1</td>
         <td>Full</td>
         <td>N/A</td>
         <td>N/A</td>
      </tr>
      <tr>
         <td><a href="https://www.prisma.io/" target="_blank" referrerpolicy="no-referrer-when-downgrade">Prisma</a></td>
         <td>4.16.2</td>
         <td>Full</td>
         <td>N/A</td>
         <td><a href="https://docs.pingcap.com/zh/tidb/dev/dev-guide-sample-application-nodejs-prisma">使用 Prisma 连接到 TiDB</a></td>
      </tr>
      <tr>
         <td><a href="https://typeorm.io/" target="_blank" referrerpolicy="no-referrer-when-downgrade">TypeORM</a></td>
         <td>v0.3.17</td>
         <td>Full</td>
         <td>N/A</td>
         <td><a href="https://docs.pingcap.com/zh/tidb/dev/dev-guide-sample-application-nodejs-typeorm">使用 TypeORM 连接到 TiDB</a></td>
      </tr>
      <tr>
         <td rowspan="2">Python</td>
         <td><a href="https://pypi.org/project/Django/" target="_blank" referrerpolicy="no-referrer-when-downgrade">Django</a></td>
         <td>v4.2</td>
         <td>Full</td>
         <td><a href="https://github.com/pingcap/django-tidb" target="_blank" referrerpolicy="no-referrer-when-downgrade">django-tidb</a></td>
         <td><a href="https://docs.pingcap.com/zh/tidb/dev/dev-guide-sample-application-python-django">使用 Django 连接到 TiDB</a></td>
      </tr>
      <tr>
         <td><a href="https://www.sqlalchemy.org/" target="_blank" referrerpolicy="no-referrer-when-downgrade">SQLAlchemy</a></td>
         <td>v1.4.37</td>
         <td>Full</td>
         <td>N/A</td>
         <td><a href="https://docs.pingcap.com/zh/tidb/dev/dev-guide-sample-application-python-sqlalchemy">使用 SQLAlchemy 连接到 TiDB</a></td>
      </tr>
   </tbody>
</table>

## GUI

| GUI                                                       | 最新已测试版本 | 支持等级 | 教程 |
|-----------------------------------------------------------|-----------------------|---------------|-----|
| [JetBrains DataGrip](https://www.jetbrains.com/datagrip/) | 2023.2.1              | Full          | N/A |
| [DBeaver](https://dbeaver.io/)                            | 23.0.3                | Full          | N/A |
| [Visual Studio Code](https://code.visualstudio.com/)      | 1.72.0                | Full          | N/A |