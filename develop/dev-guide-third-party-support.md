---
title: TiDB 支持的第三方工具
summary: 了解 TiDB 支持的第三方工具。
---

# TiDB 支持的第三方工具

> **注意：**
>
> 本文档仅列出 TiDB 支持的常见[第三方工具](https://en.wikipedia.org/wiki/Third-party_source)。一些其他第三方工具未被列出，这并不是因为它们不受支持，而是因为 PingCAP 不确定它们是否使用了与 TiDB 不兼容的功能。

TiDB [高度兼容 MySQL 协议](/mysql-compatibility.md)，因此大多数适配 MySQL 的驱动程序、ORM 框架和其他工具都与 TiDB 兼容。本文档重点介绍这些工具及其对 TiDB 的支持级别。

## 支持级别

PingCAP 与社区合作，为第三方工具提供以下支持级别：

- **_完全_**：表示 TiDB 已经与相应第三方工具的大多数功能兼容，并保持与其新版本的兼容性。PingCAP 会定期对该工具的最新版本进行兼容性测试。
- **_兼容_**：表示由于相应的第三方工具适配了 MySQL，而 TiDB 高度兼容 MySQL 协议，因此 TiDB 可以使用该工具的大多数功能。但是，PingCAP 尚未对该工具的所有功能进行完整测试，这可能会导致一些意外行为。

> **注意：**
>
> 除非特别说明，**驱动程序**或 **ORM 框架**不包括对[应用程序重试和错误处理](/develop/dev-guide-transaction-troubleshoot.md#application-retry-and-error-handling)的支持。

如果你在使用本文档列出的工具连接 TiDB 时遇到问题，请在 GitHub 上提交[问题](https://github.com/pingcap/tidb/issues/new?assignees=&labels=type%2Fquestion&template=general-question.md)并提供详细信息，以促进对该工具的支持。

## 驱动程序

<table>
   <thead>
      <tr>
         <th>语言</th>
         <th>驱动程序</th>
         <th>最新测试版本</th>
         <th>支持级别</th>
         <th>TiDB 适配器</th>
         <th>教程</th>
      </tr>
   </thead>
   <tbody>
      <tr>
         <td>Go</td>
         <td><a href="https://github.com/go-sql-driver/mysql" target="_blank" referrerpolicy="no-referrer-when-downgrade">Go-MySQL-Driver</a></td>
         <td>v1.6.0</td>
         <td>完全</td>
         <td>N/A</td>
         <td><a href="/tidb/v8.1/dev-guide-sample-application-golang-sql-driver">使用 Go-MySQL-Driver 连接 TiDB</a></td>
      </tr>
      <tr>
         <td>Java</td>
         <td><a href="https://dev.mysql.com/downloads/connector/j/" target="_blank" referrerpolicy="no-referrer-when-downgrade">JDBC</a></td>
         <td>8.0</td>
         <td>完全</td>
         <td>
            <ul>
               <li><a href="/tidb/v8.1/dev-guide-choose-driver-or-orm#java-drivers" data-href="/tidb/v8.1/dev-guide-choose-driver-or-orm#java-drivers">pingcap/mysql-connector-j</a></li>
               <li><a href="/tidb/v8.1/dev-guide-choose-driver-or-orm#tidb-loadbalance" data-href="/tidb/v8.1/dev-guide-choose-driver-or-orm#tidb-loadbalance">pingcap/tidb-loadbalance</a></li>
            </ul>
         </td>
         <td><a href="/tidb/v8.1/dev-guide-sample-application-java-jdbc">使用 JDBC 连接 TiDB</a></td>
      </tr>
   </tbody>
</table>

## ORM

<table>
   <thead>
      <tr>
         <th>语言</th>
         <th>ORM 框架</th>
         <th>最新测试版本</th>
         <th>支持级别</th>
         <th>TiDB 适配器</th>
         <th>教程</th>
      </tr>
   </thead>
   <tbody>
      <tr>
         <td rowspan="4">Go</td>
         <td><a href="https://github.com/go-gorm/gorm" target="_blank" referrerpolicy="no-referrer-when-downgrade">gorm</a></td>
         <td>v1.23.5</td>
         <td>完全</td>
         <td>N/A</td>
         <td><a href="/tidb/v8.1/dev-guide-sample-application-golang-gorm">使用 GORM 连接 TiDB</a></td>
      </tr>
      <tr>
         <td><a href="https://github.com/beego/beego" target="_blank" referrerpolicy="no-referrer-when-downgrade">beego</a></td>
         <td>v2.0.3</td>
         <td>完全</td>
         <td>N/A</td>
         <td>N/A</td>
      </tr>
      <tr>
         <td><a href="https://github.com/upper/db" target="_blank" referrerpolicy="no-referrer-when-downgrade">upper/db</a></td>
         <td>v4.5.2</td>
         <td>完全</td>
         <td>N/A</td>
         <td>N/A</td>
      </tr>
      <tr>
         <td><a href="https://gitea.com/xorm/xorm" target="_blank" referrerpolicy="no-referrer-when-downgrade">xorm</a></td>
         <td>v1.3.1</td>
         <td>完全</td>
         <td>N/A</td>
         <td>N/A</td>
      </tr>
      <tr>
         <td rowspan="4">Java</td>
         <td><a href="https://hibernate.org/orm/" target="_blank" referrerpolicy="no-referrer-when-downgrade">Hibernate</a></td>
         <td>6.1.0.Final</td>
         <td>完全</td>
         <td>N/A</td>
         <td><a href="/tidb/v8.1/dev-guide-sample-application-java-hibernate">使用 Hibernate 连接 TiDB</a></td>
      </tr>
      <tr>
         <td><a href="https://mybatis.org/mybatis-3/" target="_blank" referrerpolicy="no-referrer-when-downgrade">MyBatis</a></td>
         <td>v3.5.10</td>
         <td>完全</td>
         <td>N/A</td>
         <td><a href="/tidb/v8.1/dev-guide-sample-application-java-mybatis">使用 MyBatis 连接 TiDB</a></td>
      </tr>
      <tr>
         <td><a href="https://spring.io/projects/spring-data-jpa/" target="_blank" referrerpolicy="no-referrer-when-downgrade">Spring Data JPA</a></td>
         <td>2.7.2</td>
         <td>完全</td>
         <td>N/A</td>
         <td><a href="/tidb/v8.1/dev-guide-sample-application-java-spring-boot">使用 Spring Boot 连接 TiDB</a></td>
      </tr>
      <tr>
         <td><a href="https://github.com/jOOQ/jOOQ" target="_blank" referrerpolicy="no-referrer-when-downgrade">jOOQ</a></td>
         <td>v3.16.7（开源版）</td>
         <td>完全</td>
         <td>N/A</td>
         <td>N/A</td>
      </tr>
      <tr>
         <td>Ruby</td>
         <td><a href="https://guides.rubyonrails.org/active_record_basics.html" target="_blank" referrerpolicy="no-referrer-when-downgrade">Active Record</a></td>
         <td>v7.0</td>
         <td>完全</td>
         <td>N/A</td>
         <td><a href="/tidb/v8.1/dev-guide-sample-application-ruby-rails">使用 Rails 框架和 ActiveRecord ORM 连接 TiDB</a></td>
      </tr>
      <tr>
         <td rowspan="3">JavaScript / TypeScript</td>
         <td><a href="https://sequelize.org/" target="_blank" referrerpolicy="no-referrer-when-downgrade">Sequelize</a></td>
         <td>v6.20.1</td>
         <td>完全</td>
         <td>N/A</td>
         <td><a href="/tidb/v8.1/dev-guide-sample-application-nodejs-sequelize">使用 Sequelize 连接 TiDB</a></td>
      </tr>
      <tr>
         <td><a href="https://www.prisma.io/" target="_blank" referrerpolicy="no-referrer-when-downgrade">Prisma</a></td>
         <td>4.16.2</td>
         <td>完全</td>
         <td>N/A</td>
         <td><a href="/tidb/v8.1/dev-guide-sample-application-nodejs-prisma">使用 Prisma 连接 TiDB</a></td>
      </tr>
      <tr>
         <td><a href="https://typeorm.io/" target="_blank" referrerpolicy="no-referrer-when-downgrade">TypeORM</a></td>
         <td>v0.3.17</td>
         <td>完全</td>
         <td>N/A</td>
         <td><a href="/tidb/v8.1/dev-guide-sample-application-nodejs-typeorm">使用 TypeORM 连接 TiDB</a></td>
      </tr>
      <tr>
         <td rowspan="2">Python</td>
         <td><a href="https://pypi.org/project/Django/" target="_blank" referrerpolicy="no-referrer-when-downgrade">Django</a></td>
         <td>v4.2</td>
         <td>完全</td>
         <td><a href="https://github.com/pingcap/django-tidb" target="_blank" referrerpolicy="no-referrer-when-downgrade">django-tidb</a></td>
         <td><a href="/tidb/v8.1/dev-guide-sample-application-python-django">使用 Django 连接 TiDB</a></td>
      </tr>
      <tr>
         <td><a href="https://www.sqlalchemy.org/" target="_blank" referrerpolicy="no-referrer-when-downgrade">SQLAlchemy</a></td>
         <td>v1.4.37</td>
         <td>完全</td>
         <td>N/A</td>
         <td><a href="/tidb/v8.1/dev-guide-sample-application-python-sqlalchemy">使用 SQLAlchemy 连接 TiDB</a></td>
      </tr>
   </tbody>
</table>

## GUI

| GUI                                                       | 最新测试版本 | 支持级别 | 教程                                                                             |
|-----------------------------------------------------------|-----------------------|---------------|--------------------------------------------------------------------------------------|
| [Beekeeper Studio](https://www.beekeeperstudio.io/)       | 4.3.0                 | 完全          | N/A                                                                                  |
| [JetBrains DataGrip](https://www.jetbrains.com/datagrip/) | 2023.2.1              | 完全          | [使用 JetBrains DataGrip 连接 TiDB](/develop/dev-guide-gui-datagrip.md)        |
| [DBeaver](https://dbeaver.io/)                            | 23.0.3                | 完全          | [使用 DBeaver 连接 TiDB](/develop/dev-guide-gui-dbeaver.md)                    |
| [Visual Studio Code](https://code.visualstudio.com/)      | 1.72.0                | 完全          | [使用 Visual Studio Code 连接 TiDB](/develop/dev-guide-gui-vscode-sqltools.md) |

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上向社区提问，或[提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上向社区提问，或[提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>
