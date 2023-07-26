---
title: 使用 Spring Boot, JPA 与 TiDB 实现 Hello World 程序
summary: 介绍如何使用 Spring Boot, JPA 和 TiDB 构建一个 Hello World 程序。
---

<!-- markdownlint-disable MD029 -->

# 使用 Spring Boot, JPA 与 TiDB 实现 Hello World 程序

> **注意：**
>
> 本文档仅展示构建 Hello World 程序的核心部分。如需查看更全面、更详尽的增删改查及事务的程序示例，请参考 [TiDB 和 Java 的简单 CRUD 应用程序](/develop/dev-guide-sample-application-java.md)。

本文介绍如何使用 [Spring Boot](https://spring.io/projects/spring-boot) 和 [Spring Data JPA](https://spring.io/projects/spring-data-jpa) 构建一个 TiDB 的 Hello World 应用程序，主要包括以下内容：

1. 连接到 TiDB 集群并执行 `SELECT 'Hello World'` SQL 查询。
2. 获取 SQL 查询的返回值。
3. HTTP 接口调用，并在返回值中展示 SQL 查询结果 `Hello World`。

## 完整 Hello World 应用程序代码

<SimpleTab groupId="deploy-platform">
<div label="TiDB Serverless 集群示例" value="serverless">

完整 Hello World 应用代码详见：[TiDBSpringBootJPAServerlessExample](https://github.com/pingcap-inc/tidb-example-java/tree/main/hello-world-apps/SpringBoot-JPA/serverless/TiDBSpringBootJPAServerlessExample)。

</div>

<div label="使用本地测试集群示例" value="self-hosted">

完整 Hello World 应用代码详见：[TiDBSpringBootJPANormalExample](https://github.com/pingcap-inc/tidb-example-java/tree/main/hello-world-apps/SpringBoot-JPA/normal/TiDBSpringBootJPANormalExample)。

</div>
</SimpleTab>

## 前提条件

请在阅读本文前，准备好以下资源：

- 创建 [TiDB Serverless Tier 集群](/develop/dev-guide-build-cluster-in-cloud.md) 或 [TiDB 集群](/quick-start-with-tidb.md)。
- 安装 [JDK](https://openjdk.org/projects/jdk/17/), 要求版本 17 以上。
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

## 2. 使用 IntelliJ IDEA 的 Spring Initializr 创建空白 Spring Boot 程序

- Name: 程序名称
- Location: 需要创建程序的位置
- Language: 编写此程序使用的语言
- Type: 项目类型，此处使用 `Maven`
- Group, Artifact: 应用程序的标识符
- JDK: JDK 版本（Spring Boot 3 要求 JDK 版本为 17 及以上）

![hello-world-java-spring-boot-create-project](/media/develop/hello-world-java-spring-boot-create-project.jpg)

添加 `Spring Web`, `Spring Data JPA`, `MySQL Driver` 三个依赖项后，点击 **Create**。

![hello-world-java-spring-boot-create-project-jpa](/media/develop/hello-world-java-spring-boot-create-project-jpa.jpg)

经过短暂的加载时间，你将会得到一个类似下方所示的空白项目：

![hello-world-java-spring-boot-project-init](/media/develop/hello-world-java-spring-boot-project-init.jpg)

## 3. 更改配置文件

<SimpleTab groupId="deploy-platform">
<div label="使用 TiDB Serverless 集群" value="serverless">

1. 将 `application.properties` 配置文件更名为 `application.yaml`。

2. 你可复制以下配置文件模板，并黏贴至 `application.yaml`，在配置文件模板中，将包含形如 `${host}` 的占位符：

```yaml
spring:
  datasource:
    url: jdbc:mysql://${host}:${port}/test?sslMode=VERIFY_IDENTITY&enabledTLSProtocols=TLSv1.2,TLSv1.3
    username: ${user}
    password: ${password}
    driver-class-name: com.mysql.cj.jdbc.Driver
  jpa:
    show-sql: true
    database-platform: org.hibernate.dialect.TiDBDialect
```

3. 请使用在[获取 TiDB 集群的连接参数](#1-获取-tidb-集群的连接参数)一节中得到的 `host`, `port`, `user`, `password` 参数填充 `application.yaml` 配置文件，配置完成后形如下图所示：

![hello-world-java-spring-boot-jpa-config-serverless](/media/develop/hello-world-java-spring-boot-jpa-config-serverless.jpeg)

</div>

<div label="使用本地测试集群" value="self-hosted">

1. 将 `application.properties` 配置文件更名为 `application.yaml`。

2. 你可复制以下配置文件模板，并黏贴至 `application.yaml`，在配置文件模板中，将包含形如 `${host}` 的占位符：

```yaml
spring:
  datasource:
    url: jdbc:mysql://${host}:${port}/test
    username: ${user}
    password: ${password}
    driver-class-name: com.mysql.cj.jdbc.Driver
  jpa:
    show-sql: true
    database-platform: org.hibernate.dialect.TiDBDialect
```

3. 请使用在[获取 TiDB 集群的连接参数](#1-获取-tidb-集群的连接参数)一节中得到的 `host`, `port`, `user`, `password` 参数填充 `application.yaml` 配置文件，配置完成后形如下图所示：

![hello-world-java-spring-boot-jpa-config](/media/develop/hello-world-java-spring-boot-jpa-config.jpg)

</div>
</SimpleTab>

## 4. 编写 Hello World 代码

请在启动类的同级目录中添加 `HelloWorldController.java`：

```java
@RestController
@RequestMapping
public class HelloWorldController {
    @Autowired
    private EntityManager entityManager;

    @GetMapping("/hello")
    public Object hello() {
        return entityManager
                .createNativeQuery("SELECT 'Hello World'")
                .getSingleResult();
    }
}
```

## 5. 运行及结果

点击右上方运行按钮，应用程序启动结果如下：

![hello-world-java-spring-boot-jpa-run](/media/develop/hello-world-java-spring-boot-jpa-run.jpg)

使用任意可发送网络请求的浏览器访问 `http://localhost:8080/hello` ，此处使用 Chrome：

![hello-world-java-spring-boot-jpa-result](/media/develop/hello-world-java-spring-boot-jpa-result.jpg)

## 扩展阅读

- 如需查看更全面、更详尽的增删改查及事务的程序示例，请参考 [TiDB 和 Java 的简单 CRUD 应用程序](/develop/dev-guide-sample-application-java.md)。
- 此外，你还可以通过视频的形式学习免费的 [TiDB SQL 开发在线课程](https://pingcap.com/zh/courses-catalog/back-end-developer/?utm_source=docs-cn-dev-guide)。