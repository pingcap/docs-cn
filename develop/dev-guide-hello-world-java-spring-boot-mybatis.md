---
title: Spring Boot, MyBatis 与 TiDB 的 Hello World 程序
summary: 给出一个 Spring Boot, MyBatis 与 TiDB 的 Hello World 程序示例。
---

<!-- markdownlint-disable MD029 -->

# Spring Boot, MyBatis 与 TiDB 的 Hello World 程序

> **注意：**
>
> 本文档仅展示 Hello World 程序构建核心片段，如需查看更全面，更详尽的增删改查及事务的程序示例，请参考 [TiDB 和 Java 的简单 CRUD 应用程序](/develop/dev-guide-sample-application-java.md)。

本文档将展示如何使用 [Spring Boot](https://spring.io/projects/spring-boot) 和 [MyBatis](http://www.mybatis.org/mybatis-3/zh/index.html) 构建一个 TiDB 的 Hello World 应用程序。在本文中，你将看到：

1. 访问 TiDB 集群，运行 `SELECT 'Hello World'`。
2. 得到 `Hello World` 的返回值。
3. HTTP 接口调用，并在返回值中展示。

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

## 使用 IntelliJ IDEA 的 Spring Initializr 创建空白 Spring Boot 程序

- Name: 程序名称
- Location: 需要创建程序的位置
- Language: 编写此程序使用的语言
- Type: 包管理器，此处使用 `Maven`
- Group, Artifact: 用于标识应用程序
- JDK: Spring Boot 3 要求 JDK 版本为 17 及以上

![hello-world-java-spring-boot-create-project](/media/develop/hello-world-java-spring-boot-create-project.jpg)

添加 `Spring Web`, `MyBatis Framework`, `MySQL Driver` 三个依赖项后，点击 **Create**。

![hello-world-java-spring-boot-create-project-mybatis](/media/develop/hello-world-java-spring-boot-create-project-mybatis.jpg)

经过短暂的加载时间，你将会得到一个类似下方所示的空白项目：

![hello-world-java-spring-boot-project-init](/media/develop/hello-world-java-spring-boot-project-init.jpg)

## 更改配置文件

<SimpleTab groupId="deploy-platform">
<div label="使用 TiDB Serverless 集群" value="serverless">

1. 将 `application.properties` 配置文件更名为 `application.yaml`。

2. 请使用在[获取你的 TiDB 参数信息](#获取你的-tidb-参数信息)一节中得到的 `host`, `port`, `user`, `password` 参数填充 `application.yaml` 配置，在配置文件中，将使用形如 `${host}` 的占位符进行配置文件编写：

```yaml
spring:
  datasource:
    url: jdbc:mysql://${host}:${port}/test?sslMode=VERIFY_IDENTITY&enabledTLSProtocols=TLSv1.2,TLSv1.3
    username: ${user}
    password: ${password}
    driver-class-name: com.mysql.cj.jdbc.Driver
```

配置完成后形如下图所示：

![hello-world-java-spring-boot-mybatis-config-serverless](/media/develop/hello-world-java-spring-boot-mybatis-config-serverless.jpg)

</div>

<div label="使用本地测试集群" value="local-test">

1. 将 `application.properties` 配置文件更名为 `application.yaml`。

2. 请使用在[获取你的 TiDB 参数信息](#获取你的-tidb-参数信息)一节中得到的 `host`, `port`, `user`, `password` 参数填充 `application.yaml` 配置，在配置文件中，将使用形如 `${host}` 的占位符进行配置文件编写：

```yaml
spring:
  datasource:
    url: jdbc:mysql://${host}:${port}/test
    username: ${user}
    password: ${password}
    driver-class-name: com.mysql.cj.jdbc.Driver
```

配置完成后形如下图所示：

![hello-world-java-spring-boot-mybatis-config](/media/develop/hello-world-java-spring-boot-mybatis-config.jpg)

</div>
</SimpleTab>

## 编写 Hello World 代码

添加 `HelloWorldController.java`：

```java
@RestController
@RequestMapping
public class HelloWorldController {
    @Autowired
    private HelloWorldMapper helloWorldMapper;

    @GetMapping("/hello")
    public Object hello() {
        return helloWorldMapper.getHelloWorld();
    }
}
```

添加 `HelloWorldMapper.java`：

```java
@Repository
public interface HelloWorldMapper {
    @Select("SELECT 'Hello World'")
    String getHelloWorld();
}
```

添加注解到启动类 `TiDBSpringBootMyBatisNormalExampleApplication`：

```java
@MapperScan("com.pingcap.example")
```

## 运行及结果

点击右上方运行按钮，应用程序启动结果如下：

![hello-world-java-spring-boot-mybatis-run](/media/develop/hello-world-java-spring-boot-mybatis-run.jpg)

使用任意可发送网络请求的浏览器访问 `http://localhost:8080/hello` ，此处使用 Chrome：

![hello-world-java-spring-boot-jpa-result](/media/develop/hello-world-java-spring-boot-jpa-result.jpg)

## 完整 Hello World 应用程序代码

<SimpleTab groupId="deploy-platform">
<div label="TiDB Serverless 集群示例" value="serverless">

```shell
git clone https://github.com/pingcap-inc/tidb-example-java.git
cd tidb-example-java/hello-world-apps/SpringBoot-MyBatis/serverless/TiDBSpringBootMyBatisServerlessExample
```

</div>

<div label="使用本地测试集群示例" value="local-test">

```shell
git clone https://github.com/pingcap-inc/tidb-example-java.git
cd tidb-example-java/hello-world-apps/SpringBoot-MyBatis/normal/TiDBSpringBootMyBatisNormalExample
```

</div>
</SimpleTab>
