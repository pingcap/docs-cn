---
title: 选择驱动或 ORM 框架
summary: 选择驱动或 ORM 框架连接 TiDB。
aliases: ['/zh/tidb/dev/choose-driver-or-orm']
---

# 选择驱动或 ORM 框架

TiDB 兼容 MySQL 的协议，但存在部分与 MySQL 不兼容的特性，例如：

TiDB 不支持：

- 存储过程与函数
- 触发器
- 外键约束

TiDB 与 MySQL 有差异：

- 自增 ID：可保证全局唯一，或单 TiDB 节点的自增，但无法保证全局自增。

全部兼容性差异可查看[与 MySQL 兼容性对比](/mysql-compatibility.md)

## Java

支持等级说明

- Full: 此 Driver 或 ORM 没有已知的 issues
- Verified: 你可能会因为 TiDB 兼容性问题，导致出现错误

### Java Drivers

**JDBC**

支持等级：**Full**

按照 [MySQL 文档](https://dev.mysql.com/doc/connector-j/5.1/en/)中的说明下载并配置 Java JDBC 驱动程序即可使用。

> 注意：
>
> 强烈建议使用 JDBC 5.1 的最后一个版本 5.1.49。因为当前 8.0.29 版本有未合并的 [Bug 修复](https://bugs.mysql.com/bug.php?id=106252)，在与 TiDB 共同使用时可能会导致线程卡死。在 MySQL JDBC 8.0 未合并此修复之前，建议不要升级至 8.0 版本。

有关一个完整的实例应用程序，可参阅使用 [TiDB 和 JDBC 构建一个 Java 应用](/develop/dev-guide-sample-application-java.md#第-2-步获取代码)。

### Java ORM Framework

**Hibernate**

支持等级：**Full**

> **注意：**
>
> Hibernate 当前[不支持嵌套事务](https://stackoverflow.com/questions/37927208/nested-transaction-in-spring-app-with-jpa-postgres)，TiDB 从 v6.2.0 版本开始支持 [Savepoint](/sql-statements/sql-statement-savepoint.md)。
>
> 若你使用 Spring Data JPA 等框架，在 **@Transactional** 中请勿使用 `Propagation.NESTED` 事务传播选项，即：`@Transactional(propagation = Propagation.NESTED)`。

你可以使用 [Gradle](https://gradle.org/install) 或 [Maven](https://maven.apache.org/install.html) 获取你的应用程序的所有依赖项，且会帮你下载依赖项的间接依赖，而无需你手动管理复杂的依赖关系。注意，只有 Hibernate `6.0.0.Beta2` 及以上版本才支持 TiDB 方言。

如果你使用的是 **Maven**，请将以下内容添加到你的 `<dependencies></dependencies>`：

{{< copyable "" >}}

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

{{< copyable "" >}}

```gradle
implementation 'org.hibernate:hibernate-core:6.0.0.CR2'
implementation 'mysql:mysql-connector-java:5.1.49'
```

- 有关原生 Java 使用 Hibernate 进行 TiDB 应用程序构建的例子，可参阅 [TiDB 和 Java 的简单 CRUD 应用程序 - 使用 Hibernate](/develop/dev-guide-sample-application-java.md#第-2-步获取代码)。
- 有关 Spring 使用 Spring Data JPA、Hibernate 进行 TiDB 应用程序构建的例子，可参阅[使用 Spring Boot 构建 TiDB 应用程序](/develop/dev-guide-sample-application-spring-boot.md)。

额外的，你需要在 [Hibernate 配置文件](https://www.tutorialspoint.com/hibernate/hibernate_configuration.htm)中指定 TiDB 方言： `org.hibernate.dialect.TiDBDialect`，此方言在 Hibernate `6.0.0.Beta2` 以上才可支持。若你无法升级 Hibernate 版本，那么请你直接使用 MySQL 5.7 的方言 `org.hibernate.dialect.MySQL57Dialect`。但这可能造成不可预料的使用结果，及部分 TiDB 特有特性的缺失，如：[序列](/sql-statements/sql-statement-create-sequence.md)等。
