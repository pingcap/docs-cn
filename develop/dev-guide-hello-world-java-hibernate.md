---
title: Hibernate 与 TiDB 的 Hello World 程序
summary: 给出一个 Hibernate 与 TiDB 的 Hello World 程序示例。
---

<!-- markdownlint-disable MD029 -->

# Hibernate 与 TiDB 的 Hello World 程序

> **注意：**
>
> 本文档仅展示 Hello World 程序构建核心片段，如需查看更全面，更详尽的增删改查及事务的程序示例，请参考 [TiDB 和 Java 的简单 CRUD 应用程序](/develop/dev-guide-sample-application-java.md)。

本文档将展示如何使用 [Hibernate ORM](https://hibernate.org/orm/) 构建一个 TiDB 的 Hello World 应用程序。在本文中，你将看到：

1. 访问 TiDB 集群，运行 `SELECT 'Hello World'`。
2. 得到 `Hello World` 的返回值。
3. 打印展示。

## 获取你的 TiDB 参数信息

<SimpleTab groupId="deploy-platform">
<div label="使用 TiDB Serverless 集群" value="serverless">

请获取 TiDB Serverless 集群的 `host`, `port`, `user`, `password`, `ssl_ca` 参数。

详细步骤，请参考：[获取 TiDB Serverless 连接参数](https://docs.pingcap.com/tidbcloud/connect-via-standard-connection-serverless#obtain-tidb-serverless-connection-parameters)。

</div>

<div label="使用本地测试集群" value="local-test">

请获取 TiDB 的 `host`, `port`, `user`, `password` 参数。

本地 TiDB 测试集群的默认参数如下：

```properties
host: 'localhost'
port: 4000
user: 'root'
password: ''
```

</div>
</SimpleTab>

## 使用 Intellij IDEA 创建空白 Maven 程序

![hello-world-java-maven-quickstart-create-project](/media/develop/hello-world-java-maven-quickstart-create-project.jpg)

- Name: 程序名称
- Location: 需要创建程序的位置
- JDK: 推荐 JDK 11 及以上
- Archetype: 创建 Maven 程序的原型模板，此处使用 `org.apache.maven.archetypes:maven-archetype-quickstart` 创建命令行程序
- Advanced Settings: 将会使用 GroupID, ArtifactID, 和 Version 组合，从而标识一个唯一的包

经过短暂的加载时间，你将会得到一个类似下方所示的空白项目：

![hello-world-java-maven-quickstart-project-init](/media/develop/hello-world-java-maven-quickstart-project-init.jpg)

## 添加依赖

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

## 创建 Hibernate 配置文件

<SimpleTab groupId="deploy-platform">
<div label="使用 TiDB Serverless 集群" value="serverless">

在 `src/main/resources` 下创建 `hibernate.cfg.xml` 配置文件，内容如下，请使用在[获取你的 TiDB 参数信息](#获取你的-tidb-参数信息)一节中得到的 `host`, `port`, `user`, `password` 参数填充以下配置，在配置文件中，将使用形如 `${host}` 的占位符进行配置文件编写：

> **建议：**
>
> 是否好奇配置中的 `&amp;` 是什么？这其实是一个转译字符，在 XML 文件里，你不应直接使用 `&`，因为这是一个特殊字符。你需要使用 `&amp;` 来替换 `&` 字符，从而让 XML 解析器正常解析你的字符串。类似的常见替换有：
>
> - `&`: `&amp;`
> - `<`: `&lt;`
> - `>`: `&gt;`
> - `"`: `&quot;`
> - `'`: `&apos;`

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

配置完成后形如下图所示：

![hello-world-java-maven-quickstart-hibernate-config-serverless](/media/develop/hello-world-java-maven-quickstart-hibernate-config-serverless.jpeg)

</div>

<div label="使用本地测试集群" value="local-test">

在 `src/main/resources` 下创建 `hibernate.cfg.xml` 配置文件，内容如下，请使用在[获取你的 TiDB 参数信息](#获取你的-tidb-参数信息)一节中得到的 `host`, `port`, `user`, `password` 参数填充以下配置，在配置文件中，将使用形如 `${host}` 的占位符进行配置文件编写：

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

配置完成后形如下图所示：

![hello-world-java-maven-quickstart-hibernate-config](/media/develop/hello-world-java-maven-quickstart-hibernate-config.jpg)

</div>
</SimpleTab>

## 编写 Hello World 代码

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

## 运行及结果

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

<div label="使用本地测试集群示例" value="local-test">

```shell
git clone https://github.com/pingcap-inc/tidb-example-java.git
cd tidb-example-java/hello-world-apps/Hibernate/normal/TiDBHibernateNormalExample
```

</div>
</SimpleTab>
