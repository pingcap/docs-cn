---
title: 使用 MyBatis 与 TiDB 实现 Hello World 程序
summary: 介绍如何使用 MyBatis 和 TiDB 构建一个 Hello World 程序。
---

<!-- markdownlint-disable MD029 -->

# 使用 MyBatis 与 TiDB 实现 Hello World 程序

> **注意：**
>
> 本文档仅展示构建 Hello World 程序的核心部分。如需查看更全面、更详尽的增删改查及事务的程序示例，请参考 [TiDB 和 Java 的简单 CRUD 应用程序](/develop/dev-guide-sample-application-java.md)。

本文介绍如何使用 [Mybatis](https://mybatis.org/mybatis-3/index.html) 构建一个 TiDB 的 Hello World 应用程序，主要包括以下内容：

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
- JDK: 推荐 JDK 11 及以上
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
    <groupId>org.mybatis</groupId>
    <artifactId>mybatis</artifactId>
    <version>3.5.13</version>
</dependency>
```

随后刷新 Maven 依赖

![hello-world-java-mybatis-dep-refresh](/media/develop/hello-world-java-mybatis-dep-refresh.jpg)

## 4. 创建 MyBatis 配置文件

<SimpleTab groupId="deploy-platform">
<div label="使用 TiDB Serverless 集群" value="serverless">

在 `src/main/resources` 下创建 `mybatis-config.xml` 配置文件，内容如下，请使用在[获取你的 TiDB 参数信息](#获取你的-tidb-参数信息)一节中得到的 `host`, `port`, `user`, `password` 参数填充以下配置，在配置文件中，将使用形如 `${host}` 的占位符进行配置文件编写：

```xml
<?xml version="1.0" encoding="UTF-8" ?>

<!DOCTYPE configuration
        PUBLIC "-//mybatis.org//DTD Config 3.0//EN"
        "http://mybatis.org/dtd/mybatis-3-config.dtd">

<configuration>
    <environments default="development">
        <environment id="development">
            <transactionManager type="JDBC"/>
            <dataSource type="POOLED">
                <property name="driver" value="com.mysql.cj.jdbc.Driver"/>
                <property name="url" value="jdbc:mysql://${host}:${port}/test?sslMode=VERIFY_IDENTITY&amp;enabledTLSProtocols=TLSv1.2,TLSv1.3"/>
                <property name="username" value="${user}"/>
                <property name="password" value="${password}"/>
            </dataSource>
        </environment>
    </environments>
    <mappers>
        <mapper class="com.pingcap.HelloWorldMapper"/>
    </mappers>
</configuration>

```

<details>

<summary>是否好奇配置中的 <code>&amp;</code> 是什么？</summary>

这其实是一个转译字符，在 XML 文件里，你不应直接使用 `&`，因为这是一个特殊字符。你需要使用 `&amp;` 来替换 `&` 字符，从而让 XML 解析器正常解析你的字符串。类似的常见替换有：
>
> - `&`: `&amp;`
> - `<`: `&lt;`
> - `>`: `&gt;`
> - `"`: `&quot;`
> - `'`: `&apos;`

</details>

配置完成后形如下图所示：

![hello-world-java-maven-quickstart-mybatis-config-serverless](/media/develop/hello-world-java-maven-quickstart-mybatis-config-serverless.jpeg)

</div>

<div label="使用本地测试集群" value="self-hosted">

在 `src/main/resources` 下创建 `mybatis-config.xml` 配置文件，内容如下，请使用在[获取你的 TiDB 参数信息](#获取你的-tidb-参数信息)一节中得到的 `host`, `port`, `user`, `password` 参数填充以下配置，在配置文件中，将使用形如 `${host}` 的占位符进行配置文件编写：

```xml
<?xml version="1.0" encoding="UTF-8" ?>

<!DOCTYPE configuration
        PUBLIC "-//mybatis.org//DTD Config 3.0//EN"
        "http://mybatis.org/dtd/mybatis-3-config.dtd">

<configuration>
    <environments default="development">
        <environment id="development">
            <transactionManager type="JDBC"/>
            <dataSource type="POOLED">
                <property name="driver" value="com.mysql.cj.jdbc.Driver"/>
                <property name="url" value="jdbc:mysql://${host}:${port}/test"/>
                <property name="username" value="${user}"/>
                <property name="password" value="${password}"/>
            </dataSource>
        </environment>
    </environments>
    <mappers>
        <mapper class="com.pingcap.HelloWorldMapper"/>
    </mappers>
</configuration>
```

配置完成后形如下图所示：

![hello-world-java-maven-quickstart-mybatis-config](/media/develop/hello-world-java-maven-quickstart-mybatis-config.jpg)

</div>
</SimpleTab>

## 5. 编写 Hello World 代码

如果你有注意到我们上一步有创建一个 `<mapper>` 节点，`class` 属性为 `com.pingcap.HelloWorldMapper`。这代表着我们需要创建一个 `HelloWorldMapper` 接口在相应的位置，并且添加代码：

```java
public interface HelloWorldMapper {
    @Select("SELECT 'Hello World'")
    String helloWorld();
}
```

并更改 `App.java` 代码至：

```java
public class App {
    public static void main( String[] args ) throws IOException {
        InputStream inputStream = Resources.getResourceAsStream("mybatis-config.xml");
        SqlSessionFactory sqlSessionFactory = new SqlSessionFactoryBuilder().build(inputStream);
        try (SqlSession session = sqlSessionFactory.openSession()) {
            HelloWorldMapper mapper = session.getMapper(HelloWorldMapper.class);
            System.out.println(mapper.helloWorld());
        }
    }
}

```

## 6. 运行及结果

点击右上方运行按钮，输出结果如下：

![hello-world-java-mybatis-run](/media/develop/hello-world-java-mybatis-run.jpg)

## 完整 Hello World 应用程序代码

<SimpleTab groupId="deploy-platform">
<div label="TiDB Serverless 集群示例" value="serverless">

```shell
git clone https://github.com/pingcap-inc/tidb-example-java.git
cd tidb-example-java/hello-world-apps/MyBatis/serverless/TiDBMyBatisServerlessExample
```

</div>

<div label="使用本地测试集群示例" value="self-hosted">

```shell
git clone https://github.com/pingcap-inc/tidb-example-java.git
cd tidb-example-java/hello-world-apps/MyBatis/normal/TiDBMyBatisNormalExample
```

</div>
</SimpleTab>
