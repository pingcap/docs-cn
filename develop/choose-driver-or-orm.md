---
title: 选择驱动或 ORM 框架
---

# 选择驱动或 ORM 框架

TiDB 兼容 MySQL 的协议，但存在部分与 MySQL 不兼容的特性，例如：

不支持：

- 存储过程与函数
- 触发器
- 外键约束

有差异：

- 自增 ID：可保证全局唯一，或单 TiDB 节点的自增，但无法保证全局自增

全部兼容性差异可查看：[与 MySQL 兼容性对比](https://docs.pingcap.com/zh/tidb/stable/mysql-compatibility)

其余语言：`JavaScript/TypeScript Python Go Ruby C C#(.Net)`

## Java

> 支持等级说明
>
> - \*Full: 此 Driver 或 ORM 没有已知的 issues
> - \*Verified: 你可能会因为 TiDB 兼容性问题，导致出现错误

### Java Drivers

#### JDBC

支持等级：`Full`

按照[官方文档](https://dev.mysql.com/doc/connector-j/8.0/en/)中的说明下载并配置 Java JDBC 驱动程序即可使用。

> 注意：
>
> 强烈建议使用 8.0.16 及以上版本，其修复了两个 CVE ：
>
> - \*CVE-2019-2692 直接引入
> - \*CVE-2021-22569 间接引入

有关一个完整的实例应用程序，可参阅使用 [TiDB 和 JDBC 构建一个 Java 应用](/develop/sample-application-java.md#步骤-2-获取代码)

### Java ORM Framework

#### Hibernate

支持等级：`Full`

> 注意：
>
> Hibernate 当前 [不支持嵌套事务](https://stackoverflow.com/questions/37927208/nested-transaction-in-spring-app-with-jpa-postgres)，TiDB 当前版本也 [不支持 Savepoint](https://github.com/pingcap/tidb/issues/6840)。
> 若您使用 Spring Data JPA 等框架，在 `@Transactional` 中请勿使用 `Propagation.NESTED` 事务传播选项，即：`@Transactional(propagation = Propagation.NESTED)`
>
> 你可以使用[这个例子](https://github.com/Icemap/tidb-savepoint)，快速复现 TiDB 与 MySQL 对 Savepoint 的输出结果：
>
> ```
> MySQL:
> id: 1, coins: 1, goods: 1
> id: 3, coins: 1, goods: 1
>
> TiDB:
>
> 2022/04/02 13:59:48 /<path>/go/pkg/mod/gorm.io/driver/mysql@v1.3.2/mysql.go:397 Error 1064: You have an error in your SQL syntax; check the manual that corresponds to your TiDB version for the right syntax to use line 1 column 9 near "SAVEPOINT sp0x102cf8960"
> [1.119ms] [rows:0] SAVEPOINT sp0x102cf8960
>
> 2022/04/02 13:59:48 /<path>/go/pkg/mod/gorm.io/driver/mysql@v1.3.2/mysql.go:397 Error 1064: You have an error in your SQL syntax; check the manual that corresponds to your TiDB version for the right syntax to use line 1 column 9 near "SAVEPOINT sp0x102cf8960"
> [0.001ms] [rows:0] SAVEPOINT sp0x102cf8a00
> id: 1, coins: 1, goods: 1
> ```

您可以使用 [Gradle](https://gradle.org/install) 或 [Maven](https://maven.apache.org/install.html) 获取您的应用程序的所有依赖项，且会帮您下载依赖项的间接依赖，而无需您手动管理复杂的依赖关系。注意，只有 Hibernate `6.0.0.Beta2` 及以上版本才支持 TiDB 方言。

如果您使用的是 `Maven`，请将以下内容添加到您的 `<dependencies></dependencies>`：

```xml
<dependency>
    <groupId>org.hibernate.orm</groupId>
    <artifactId>hibernate-core</artifactId>
    <version>6.0.0.CR2</version>
</dependency>

<dependency>
    <groupId>mysql</groupId>
    <artifactId>mysql-connector-java</artifactId>
    <version>8.0.28</version>
</dependency>
```

如果您使用的是 `Gradle`， 请将以下内容添加到您的 `dependencies`：

```gradle
implementation 'org.hibernate:hibernate-core:6.0.0.CR2'
implementation 'mysql:mysql-connector-java:8.0.28'
```

- 有关原生 Java 使用 Hibernate 进行 TiDB 应用程序构建的例子，可参阅 [TiDB 和 Java 的简单 CRUD 应用程序 - 使用 Hibernate](/develop/sample-application-java.md#步骤-2-获取代码)。
- 有关 Spring 使用 Spring Data JPA / Hibernate 进行 TiDB 应用程序构建的例子，可参阅 [使用 Spring Boot 构建 TiDB 应用程序](/develop/sample-application-spring-boot.md)

额外的，您需要在 [Hibernate 配置文件](https://www.tutorialspoint.com/hibernate/hibernate_configuration.htm) 中指定 TiDB 方言： `org.hibernate.dialect.TiDBDialect`，此方言在 Hibernate `6.0.0.Beta2` 以上才可支持。若您无法升级 Hibernate 版本，那么请您直接使用 MySQL 5.7 的方言 `org.hibernate.dialect.MySQL57Dialect`。但这可能造成不可预料的使用结果，及部分 TiDB 特有特性的缺失，如：[序列](https://docs.pingcap.com/zh/tidb/stable/sql-statement-create-sequence) 等。
