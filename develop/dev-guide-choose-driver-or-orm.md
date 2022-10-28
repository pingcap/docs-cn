---
title: 选择驱动或 ORM 框架
summary: 选择驱动或 ORM 框架连接 TiDB。
---

# 选择驱动或 ORM 框架

> **注意：**
>
> TiDB 支持等级说明：
>
> - **Full**：此 Driver 或 ORM 没有已知的 issues。
> - **Verified**：可能会因为 TiDB 与 MySQL 的兼容性问题，导致出现错误。
>
> 关于更多 TiDB 支持的第三方工具，你可以查看 [TiDB 支持的第三方工具](/develop/dev-guide-third-party-support.md)。

TiDB 兼容 MySQL 的协议，但存在部分与 MySQL 不兼容的特性，例如：

TiDB 不支持：

- 存储过程与函数
- 触发器
- 外键约束

TiDB 与 MySQL 有差异：

- 自增 ID：可保证全局唯一，或单 TiDB 节点的自增，但无法保证全局自增。

全部兼容性差异可查看[与 MySQL 兼容性对比](/mysql-compatibility.md)

## Java

本节介绍 Java 语言的 Driver 及 ORM 的使用方式。

### Java Drivers

<SimpleTab>
<div label="MySQL-JDBC">

支持等级：**Full**

按照 [MySQL 文档](https://dev.mysql.com/doc/connector-j/5.1/en/)中的说明下载并配置 Java JDBC 驱动程序即可使用。

> **注意：**
>
> 强烈建议使用 JDBC 5.1 的最后一个版本 5.1.49。因为当前 8.0.29 版本有未合并的 [Bug 修复](https://bugs.mysql.com/bug.php?id=106252)，在与 TiDB 共同使用时可能会导致线程卡死。在 MySQL JDBC 8.0 未合并此修复之前，建议不要升级至 8.0 版本。

有关一个完整的实例应用程序，可参阅使用 [TiDB 和 JDBC 构建一个 Java 应用](/develop/dev-guide-sample-application-java.md#第-2-步获取代码)。

</div>
<div label="TiDB-JDBC">

支持等级：**Full**

[TiDB-JDBC](https://github.com/pingcap/mysql-connector-j) 是基于 MySQL 8.0.29 的定制版本。TiDB-JDBC 基于 MySQL 官方 8.0.29 版本编译，修复了原 JDBC 在 prepare 模式下多参数、多字段 EOF 的错误，并新增 TiCDC snapshot 自动维护和 SM3 认证插件等功能。

基于 SM3 的认证仅在 TiDB 版本的 MySQL Connector/J 中支持。

如果你使用的是 **Maven**，请将以下内容添加到你的 `<dependencies></dependencies>`：

```xml
<dependency>
  <groupId>io.github.lastincisor</groupId>
  <artifactId>mysql-connector-java</artifactId>
  <version>8.0.29-tidb-1.0.0</version>
</dependency>
```

如果你需要使用 SM3 认证，请将以下内容添加到你的 `<dependencies></dependencies>`：

```xml
<dependency>
  <groupId>io.github.lastincisor</groupId>
  <artifactId>mysql-connector-java</artifactId>
  <version>8.0.29-tidb-1.0.0</version>
</dependency>
<dependency>
    <groupId>org.bouncycastle</groupId>
    <artifactId>bcprov-jdk15on</artifactId>
    <version>1.67</version>
</dependency>
<dependency>
    <groupId>org.bouncycastle</groupId>
    <artifactId>bcpkix-jdk15on</artifactId>
    <version>1.67</version>
</dependency>
```

如果你使用的是 Gradle，请将以下内容添加到你的 `dependencies`：

```gradle
implementation group: 'io.github.lastincisor', name: 'mysql-connector-java', version: '8.0.29-tidb-1.0.0'
implementation group: 'org.bouncycastle', name: 'bcprov-jdk15on', version: '1.67'
implementation group: 'org.bouncycastle', name: 'bcpkix-jdk15on', version: '1.67'
```

</div>
</SimpleTab>

### Java ORM 框架

> **注意：**
>
> Hibernate 当前[不支持嵌套事务](https://stackoverflow.com/questions/37927208/nested-transaction-in-spring-app-with-jpa-postgres)。

<SimpleTab>
<div label="Hibernate">

支持等级：**Full**

你可以使用 [Gradle](https://gradle.org/install) 或 [Maven](https://maven.apache.org/install.html) 获取你的应用程序的所有依赖项，且会帮你下载依赖项的间接依赖，而无需你手动管理复杂的依赖关系。注意，只有 Hibernate `6.0.0.Beta2` 及以上版本才支持 TiDB 方言。

如果你使用的是 **Maven**，请将以下内容添加到你的 `<dependencies></dependencies>`：

```xml
<dependency>
    <groupId>org.hibernate.orm</groupId>
    <artifactId>hibernate-core</artifactId>
    <version>6.0.0.CR2</version>
</dependency>

<dependency>
    <groupId>mysql</groupId>
    <artifactId>mysql-connector-java</artifactId>
    <version>5.1.49</version>
</dependency>
```

如果你使用的是 `Gradle`，请将以下内容添加到你的 `dependencies`：

```gradle
implementation 'org.hibernate:hibernate-core:6.0.0.CR2'
implementation 'mysql:mysql-connector-java:5.1.49'
```

- 有关原生 Java 使用 Hibernate 进行 TiDB 应用程序构建的例子，可参阅 [TiDB 和 Java 的简单 CRUD 应用程序 - 使用 Hibernate](/develop/dev-guide-sample-application-java.md#第-2-步获取代码)。
- 有关 Spring 使用 Spring Data JPA、Hibernate 进行 TiDB 应用程序构建的例子，可参阅[使用 Spring Boot 构建 TiDB 应用程序](/develop/dev-guide-sample-application-spring-boot.md)。

额外的，你需要在 [Hibernate 配置文件](https://www.tutorialspoint.com/hibernate/hibernate_configuration.htm)中指定 TiDB 方言： `org.hibernate.dialect.TiDBDialect`，此方言在 Hibernate `6.0.0.Beta2` 以上才可支持。若你无法升级 Hibernate 版本，那么请你直接使用 MySQL 5.7 的方言 `org.hibernate.dialect.MySQL57Dialect`。但这可能造成不可预料的使用结果，及部分 TiDB 特有特性的缺失，如：[序列](/sql-statements/sql-statement-create-sequence.md)等。

</div>

<div label="MyBatis">

支持等级：**Full**

你可以使用 [Gradle](https://gradle.org/install) 或 [Maven](https://maven.apache.org/install.html) 获取应用程序的所有依赖项包括间接依赖，无需手动管理复杂的依赖关系。

如果你使用的是 Maven，请将以下内容添加到你的 `<dependencies></dependencies>`：

```xml
<dependency>
    <groupId>org.mybatis</groupId>
    <artifactId>mybatis</artifactId>
    <version>3.5.9</version>
</dependency>

<dependency>
    <groupId>mysql</groupId>
    <artifactId>mysql-connector-java</artifactId>
    <version>5.1.49</version>
</dependency>
```

如果你使用的是 Gradle，请将以下内容添加到你的 `dependencies`：

```gradle
implementation 'org.mybatis:mybatis:3.5.9'
implementation 'mysql:mysql-connector-java:5.1.49'
```

使用 MyBatis 进行 TiDB 应用程序构建的例子，可参阅 [TiDB 和 Java 的简单 CRUD 应用程序 - 使用 Mybatis](/develop/dev-guide-sample-application-java.md#第-2-步获取代码)。

</div>

</SimpleTab>

### Java 客户端负载均衡

**tidb-loadbalance**

支持等级：**Full**

[tidb-loadbalance](https://github.com/pingcap/tidb-loadbalance) 是应用端的负载均衡组件。通过 tidb-loadbalance，你可以实现自动维护 TiDB server 的节点信息，根据节点信息使用 tidb-loadbalance 策略在客户端分发 JDBC 连接。客户端应用与 TiDB server 之间使用 JDBC 直连，性能高于使用负载均衡组件。

目前 tidb-loadbalance 已实现轮询、随机、权重等负载均衡策略。

> **注意：**
>
> tidb-loadbalance 需配合 mysql-connector-j 一起使用。

如果你使用的是 **Maven**，请将以下内容添加到你的 `<dependencies></dependencies>`：

```xml
<dependency>
  <groupId>io.github.lastincisor</groupId>
  <artifactId>mysql-connector-java</artifactId>
  <version>8.0.29-tidb-1.0.0</version>
</dependency>
<dependency>
  <groupId>io.github.lastincisor</groupId>
  <artifactId>tidb-loadbalance</artifactId>
  <version>0.0.5</version>
</dependency>
```

如果你使用的是 Gradle，请将以下内容添加到你的 `dependencies`：

```gradle
implementation group: 'io.github.lastincisor', name: 'mysql-connector-java', version: '8.0.29-tidb-1.0.0'
implementation group: 'io.github.lastincisor', name: 'tidb-loadbalance', version: '0.0.5'
```

## Golang

本节介绍 Golang 语言的 Driver 及 ORM 的使用方式。

### Golang Drivers

**go-sql-driver/mysql**

支持等级：**Full**

按照 [go-sql-driver/mysql 文档](https://github.com/go-sql-driver/mysql)中的说明获取并配置 Golang 驱动程序即可使用。

有关一个完整的实例应用程序，可参阅使用 [TiDB 和 go-sql-driver/mysql 构建一个 Golang 应用](/develop/dev-guide-sample-application-golang.md#第-2-步获取代码)。

### Golang ORM 框架

**GORM**

支持等级：**Full**

GORM 是一个流行的 Golang 的 ORM 框架，你可以使用 `go get` 获取你的应用程序的所有依赖项。

```shell
go get -u gorm.io/gorm
go get -u gorm.io/driver/mysql
```

使用 GORM 进行 TiDB 应用程序构建的例子，可参阅 [TiDB 和 Golang 的简单 CRUD 应用程序 - 使用 GORM](/develop/dev-guide-sample-application-golang.md#第-2-步获取代码)。
