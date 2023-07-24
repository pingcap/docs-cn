---
title: 使用 Hibernate 与 TiDB 实现 Hello World 程序
summary: 介绍如何使用 Hibernate 和 TiDB 构建一个 Hello World 程序。
---

<!-- markdownlint-disable MD029 -->

# 使用 Hibernate 与 TiDB 实现 Hello World 程序

> **注意：**
>
> 本文档仅展示构建 Hello World 程序的核心部分。如需查看更全面、更详尽的增删改查及事务的程序示例，请参考 [TiDB 和 Java 的简单 CRUD 应用程序](/develop/dev-guide-sample-application-java.md)。

本文介绍如何使用 [Hibernate ORM](https://hibernate.org/orm/) 构建一个 TiDB 的 Hello World 应用程序，主要包括以下内容：

1. 连接到 TiDB 集群并执行 `SELECT 'Hello World'` SQL 查询。
2. 获取 SQL 查询的返回值。
3. 输出查询结果 `Hello World`。

## 前提条件

请在阅读本文前，准备好以下资源：

- 创建 [TiDB Serverless Tier 集群](/develop/dev-guide-build-cluster-in-cloud.md) 或 [TiDB 集群](/quick-start-with-tidb.md)。
- 安装 [JDK](https://openjdk.org/projects/jdk/17/), 要求版本 11 以上。
- 安装 [IntelliJ IDEA](https://www.jetbrains.com/idea/)。

## 1. 获取 TiDB 集群的连接参数

<SimpleTab groupId="deploy-platform">
<div label="TiDB Serverless 集群" value="serverless">

获取 TiDB Serverless 集群的连接参数，包括 `host`、`port`、`user`、`password` 和 `ssl_ca`。详细步骤，请参考[获取 TiDB Serverless 连接参数](https://docs.pingcap.com/tidbcloud/connect-via-standard-connection-serverless#obtain-tidb-serverless-connection-parameter)。

</div>

<div label="本地集群" value="self-hosted">

获取本地部署的 TiDB 集群的 `host`、`port`、`user` 和 `password` 参数。通过 `tiup playground` 部署的集群默认的连接参数如下：

```properties
host: '127.0.0.1'
port: 4000
user: 'root'
password: ''
```

</div>
</SimpleTab>

## 2. 使用 IntelliJ IDEA 创建空白 Maven 程序

- Name: 程序名称
- Location: 需要创建程序的位置
- JDK: JDK 版本（推荐 JDK 11 及以上）
- Archetype: 创建 Maven 程序的原型模板，此处使用 `org.apache.maven.archetypes:maven-archetype-quickstart` 创建命令行程序
- Advanced Settings: 将会使用 GroupID, ArtifactID, 和 Version 组合，从而标识一个唯一的包

![hello-world-java-maven-quickstart-create-project](/media/develop/hello-world-java-maven-quickstart-create-project.jpg)

经过短暂的加载时间，你将会得到一个类似下方所示的空白项目：

![hello-world-java-maven-quickstart-project-init](/media/develop/hello-world-java-maven-quickstart-project-init.jpg)

## 3. 添加依赖

将以下两个依赖添加入 `<dependencies></dependencies>` 节点中。

```xml
<dependency>
    <groupId>mysql</groupId>
    <artifactId>mysql-connector-java</artifactId>
    <version>8.0.33</version>
</dependency>

<dependency>
    <groupId>org.hibernate.orm</groupId>
    <artifactId>hibernate-core</artifactId>
    <version>6.2.3.Final</version>
</dependency>
```

随后刷新 Maven 依赖

![hello-world-java-hibernate-dep-refresh](/media/develop/hello-world-java-hibernate-dep-refresh.jpg)

## 4. 创建 Hibernate 配置文件

<SimpleTab groupId="deploy-platform">
<div label="使用 TiDB Serverless 集群" value="serverless">

在 `src/main/resources` 下创建 `hibernate.cfg.xml` 配置文件，你可复制以下配置文件模板，在配置文件模板中，将包含形如 `${host}` 的占位符：

```xml
<?xml version='1.0' encoding='utf-8'?>
<!DOCTYPE hibernate-configuration PUBLIC
        "-//Hibernate/Hibernate Configuration DTD 3.0//EN"
        "http://www.hibernate.org/dtd/hibernate-configuration-3.0.dtd">
<hibernate-configuration>
    <session-factory>

        <!-- Database connection settings -->
        <property name="hibernate.connection.driver_class">com.mysql.cj.jdbc.Driver</property>
        <property name="hibernate.dialect">org.hibernate.dialect.TiDBDialect</property>
        <property name="hibernate.connection.url">jdbc:mysql://${host}:${port}/test?sslMode=VERIFY_IDENTITY&amp;enabledTLSProtocols=TLSv1.2,TLSv1.3</property>
        <property name="hibernate.connection.username">${user}</property>
        <property name="hibernate.connection.password">${password}</property>
        <property name="hibernate.connection.autocommit">false</property>

        <!-- Optional: Show SQL output for debugging -->
        <property name="hibernate.show_sql">true</property>
        <property name="hibernate.format_sql">true</property>
    </session-factory>
</hibernate-configuration>

```

<details>

<summary>是否好奇配置中的 <code>&amp;amp;</code> 是什么？</summary>

这其实是一个转译字符，在 XML 文件里，你不应直接使用 `&`，因为这是一个特殊字符。你需要使用 `&amp;` 来替换 `&` 字符，从而让 XML 解析器正常解析你的字符串。类似的常见替换有：
>
> - `&`: `&amp;`
> - `<`: `&lt;`
> - `>`: `&gt;`
> - `"`: `&quot;`
> - `'`: `&apos;`

</details>

请使用在[获取你的 TiDB 参数信息](#获取你的-tidb-参数信息)一节中得到的 `host`, `port`, `user`, `password` 参数填充以上配置模板，配置完成后形如下图所示：

![hello-world-java-maven-quickstart-hibernate-config-serverless](/media/develop/hello-world-java-maven-quickstart-hibernate-config-serverless.jpeg)

</div>

<div label="使用本地测试集群" value="self-hosted">

在 `src/main/resources` 下创建 `hibernate.cfg.xml` 配置文件，你可复制以下配置文件模板，在配置文件模板中，将包含形如 `${host}` 的占位符：

```xml
<?xml version='1.0' encoding='utf-8'?>
<!DOCTYPE hibernate-configuration PUBLIC
        "-//Hibernate/Hibernate Configuration DTD 3.0//EN"
        "http://www.hibernate.org/dtd/hibernate-configuration-3.0.dtd">
<hibernate-configuration>
    <session-factory>

        <!-- Database connection settings -->
        <property name="hibernate.connection.driver_class">com.mysql.cj.jdbc.Driver</property>
        <property name="hibernate.dialect">org.hibernate.dialect.TiDBDialect</property>
        <property name="hibernate.connection.url">jdbc:mysql://${host}:${port}/test</property>
        <property name="hibernate.connection.username">${user}</property>
        <property name="hibernate.connection.password">${password}</property>
        <property name="hibernate.connection.autocommit">false</property>

        <!-- Optional: Show SQL output for debugging -->
        <property name="hibernate.show_sql">true</property>
        <property name="hibernate.format_sql">true</property>
    </session-factory>
</hibernate-configuration>
```

请使用在[获取你的 TiDB 参数信息](#获取你的-tidb-参数信息)一节中得到的 `host`, `port`, `user`, `password` 参数填充以上配置模板，配置完成后形如下图所示：

![hello-world-java-maven-quickstart-hibernate-config](/media/develop/hello-world-java-maven-quickstart-hibernate-config.jpg)

</div>
</SimpleTab>

## 5. 编写 Hello World 代码

更改 `App.java` 代码至：

```java
public class App  {
    public static void main( String[] args ) {
        try (SessionFactory sessionFactory = new Configuration()
                .configure("hibernate.cfg.xml")
                .buildSessionFactory(); Session session = sessionFactory.openSession()) {
            String result = session.createNativeQuery("SELECT 'Hello World'", String.class)
                    .getSingleResult();
            System.out.println(result);
        }
    }
}
```

## 6. 运行及结果

点击右上方运行按钮，输出结果如下：

![hello-world-java-hibernate-run](/media/develop/hello-world-java-hibernate-run.jpg)

## 完整 Hello World 应用程序代码

<SimpleTab groupId="deploy-platform">
<div label="TiDB Serverless 集群示例" value="serverless">

```shell
git clone https://github.com/pingcap-inc/tidb-example-java.git
cd tidb-example-java/hello-world-apps/Hibernate/serverless/TiDBHibernateServerlessExample
```

</div>

<div label="使用本地测试集群示例" value="self-hosted">

```shell
git clone https://github.com/pingcap-inc/tidb-example-java.git
cd tidb-example-java/hello-world-apps/Hibernate/normal/TiDBHibernateNormalExample
```

</div>
</SimpleTab>
