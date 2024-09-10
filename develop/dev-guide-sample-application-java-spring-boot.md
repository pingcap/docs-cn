---
title: 使用 Spring Boot 连接到 TiDB
summary: 了解如何使用 Spring Boot 连接到 TiDB。本文提供了使用 Spring Boot 与 TiDB 交互的 Java 示例代码片段。
aliases: ['/zh/tidb/dev/dev-guide-sample-application-spring-boot', '/zh/tidb/dev/sample-application-spring-boot']
---

# 使用 Spring Boot 连接到 TiDB

TiDB 是一个兼容 MySQL 的数据库。[Spring](https://spring.io/) 是当前比较流行的开源 Java 容器框架，本文选择 [Spring Boot](https://spring.io/projects/spring-boot) 作为使用 Spring 的方式。

本文档将展示如何使用 TiDB 和 [Spring Data JPA](https://spring.io/projects/spring-data-jpa) 及 [Hibernate](https://hibernate.org/orm/) 作为 JPA 提供者来完成以下任务：

- 配置你的环境。
- 使用 Spring Data JPA 与 Hibernate 连接到 TiDB 集群。
- 构建并运行你的应用程序。你也可以参考[示例代码片段](#示例代码片段)，完成基本的 CRUD 操作。

> **注意**
>
> 本文档适用于 TiDB Cloud Serverless、TiDB Cloud Dedicated 和本地部署的 TiDB。

## 前置需求

- 推荐 **Java Development Kit** (JDK) **17** 及以上版本。你可以根据公司及个人需求，自行选择 [OpenJDK](https://openjdk.org/) 或 [Oracle JDK](https://www.oracle.com/hk/java/technologies/downloads/)。
- [Maven](https://maven.apache.org/install.html) **3.8** 及以上版本。
- [Git](https://git-scm.com/downloads)。
- TiDB 集群。如果你还没有 TiDB 集群，可以按照以下方式创建：
    - （推荐方式）参考[创建 TiDB Cloud Serverless 集群](/develop/dev-guide-build-cluster-in-cloud.md#第-1-步创建-tidb-cloud-serverless-集群)，创建你自己的 TiDB Cloud 集群。
    - 参考[部署本地测试 TiDB 集群](/quick-start-with-tidb.md#部署本地测试集群)或[部署正式 TiDB 集群](/production-deployment-using-tiup.md)，创建本地集群。

## 运行代码并连接到 TiDB

本小节演示如何运行示例应用程序的代码，并连接到 TiDB。

### 第 1 步：克隆示例代码仓库到本地

运行以下命令，将示例代码仓库克隆到本地：

```bash
git clone https://github.com/tidb-samples/tidb-java-springboot-jpa-quickstart.git
cd tidb-java-springboot-jpa-quickstart
```

### 第 2 步：配置连接信息

根据不同的 TiDB 部署方式，使用不同的方法连接到 TiDB 集群。

<SimpleTab>

<div label="TiDB Cloud Serverless">

1. 在 TiDB Cloud 的 [**Clusters**](https://tidbcloud.com/console/clusters) 页面中，选择你的 TiDB Cloud Serverless 集群，进入集群的 **Overview** 页面。

2. 点击右上角的 **Connect** 按钮，将会弹出连接对话框。

3. 确认对话框中的配置和你的运行环境一致。

    - **Connection Type** 为 `Public`。
    - **Branch** 选择 `main`。
    - **Connect With** 选择 `General`。
    - **Operating System** 为你的运行环境。

    > **Tip:**
    >
    > 如果你在 Windows Subsystem for Linux (WSL) 中运行，请切换为对应的 Linux 发行版。

4. 如果你还没有设置密码，点击 **Generate Password** 生成一个随机密码。

    > **Tip:**
    >
    > 如果你之前已经生成过密码，可以直接使用原密码，或点击 **Reset Password** 重新生成密码。

5. 运行以下命令，将 `env.sh.example` 复制并重命名为 `env.sh`：

    ```bash
    cp env.sh.example env.sh
    ```

6. 复制并粘贴对应连接字符串至 `env.sh` 中。需更改部分示例结果如下：

    ```shell
    export TIDB_HOST='{host}'  # e.g. xxxxxx.aws.tidbcloud.com
    export TIDB_PORT='4000'
    export TIDB_USER='{user}'  # e.g. xxxxxx.root
    export TIDB_PASSWORD='{password}'
    export TIDB_DB_NAME='test'
    export USE_SSL='true'
    ```

    注意替换 `{}` 中的占位符为连接对话框中获得的值。

    TiDB Cloud Serverless 要求使用 TLS (SSL) connection，因此 `USE_SSL` 的值应为 `true`。

7. 保存 `env.sh` 文件。

</div>

<div label="TiDB Cloud Dedicated">

1. 在 TiDB Cloud 的 [**Clusters**](https://tidbcloud.com/console/clusters) 页面中，选择你的 TiDB Cloud Dedicated 集群，进入集群的 **Overview** 页面。

2. 点击右上角的 **Connect** 按钮，将会出现连接对话框。

3. 在连接对话框中，从 **Connection Type** 下拉列表中选择 **Public**，并点击 **CA cert** 下载 CA 文件。

    如果你尚未配置 IP 访问列表，请在首次连接前点击 **Configure IP Access List** 或按照[配置 IP 访问列表（英文）](https://docs.pingcap.com/tidbcloud/configure-ip-access-list)中的步骤进行配置。

    除 **Public** 连接类型外，TiDB Cloud Dedicated 还支持 **Private Endpoint** 和 **VPC Peering** 连接类型。详情请参阅[连接 TiDB Cloud Dedicated 集群（英文）](https://docs.pingcap.com/tidbcloud/connect-to-tidb-cluster)。

4. 运行以下命令，将 `env.sh.example` 复制并重命名为 `env.sh`：

    ```bash
    cp env.sh.example env.sh
    ```

5. 复制并粘贴对应的连接字符串至 `env.sh` 中。需更改部分示例结果如下：

    ```shell
    export TIDB_HOST='{host}'  # e.g. xxxxxx.aws.tidbcloud.com
    export TIDB_PORT='4000'
    export TIDB_USER='{user}'  # e.g. xxxxxx.root
    export TIDB_PASSWORD='{password}'
    export TIDB_DB_NAME='test'
    export USE_SSL='false'
    ```

    注意替换 `{}` 中的占位符为连接对话框中获得的值。

6. 保存 `env.sh` 文件。

</div>

<div label="本地部署 TiDB">

1. 运行以下命令，将 `env.sh.example` 复制并重命名为 `env.sh`：

    ```bash
    cp env.sh.example env.sh
    ```

2. 复制并粘贴对应 TiDB 的连接字符串至 `env.sh` 中。需更改部分示例结果如下：

    ```shell
    export TIDB_HOST='{host}'  # e.g. xxxxxx.aws.tidbcloud.com
    export TIDB_PORT='4000'
    export TIDB_USER='root'  # e.g. xxxxxx.root
    export TIDB_PASSWORD='{password}'
    export TIDB_DB_NAME='test'
    export USE_SSL='false'
    ```

    注意替换 `{}` 中的占位符为你的 TiDB 对应的值，并设置 `USE_SSL` 为 `false`。如果你在本机运行 TiDB，默认 Host 地址为 `127.0.0.1`，密码为空。

3. 保存 `env.sh` 文件。

</div>

</SimpleTab>

### 第 3 步：运行代码并查看结果

1. 运行下述命令，启动示例代码编写的服务：

    ```shell
    make
    ```

2. 打开另一个终端，开启请求脚本：

    ```shell
    make request
    ```

3. 查看 [`Expected-Output.txt`](https://github.com/tidb-samples/tidb-java-springboot-jpa-quickstart/blob/main/Expected-Output.txt)，并与你的服务程序输出进行比较。结果近似即为连接成功。

## 示例代码片段

你可参考以下关键代码片段，完成自己的应用开发。

完整代码及其运行方式，见代码仓库 [tidb-java-springboot-jpa-quickstart](https://github.com/tidb-samples/tidb-java-springboot-jpa-quickstart/blob/main/README-zh.md)。

### 连接到 TiDB

编写配置文件 `application.yml`：

```yaml
spring:
  datasource:
    url: ${TIDB_JDBC_URL:jdbc:mysql://localhost:4000/test}
    username: ${TIDB_USER:root}
    password: ${TIDB_PASSWORD:}
    driver-class-name: com.mysql.cj.jdbc.Driver
  jpa:
    show-sql: true
    database-platform: org.hibernate.dialect.TiDBDialect
    hibernate:
      ddl-auto: create-drop
```

请在配置后将环境变量 `TIDB_JDBC_URL`、`TIDB_USER` 和 `TIDB_PASSWORD` 设置为你的 TiDB 集群的实际值。此配置文件带有环境变量默认配置，即在不配置环境变量时，变量的值为：

- `TIDB_JDBC_URL`: `"jdbc:mysql://localhost:4000/test"`
- `TIDB_USER`: `"root"`
- `TIDB_PASSWORD`: `""`

### 数据管理

Spring Data JPA 通过 `@Entity` 注册数据实体，并绑定数据库的表。

```java
@Entity
@Table(name = "player_jpa")
public class PlayerBean {
}
```

`PlayerRepository` 通过继承 `JpaRepository` 接口，由 `JpaRepositoryFactoryBean` 为其自动注册对应的 Repository Bean。同时，`JpaRepository` 接口的默认实现类 `SimpleJpaRepository` 提供了增删改查函数的具体实现。

```java
@Repository
public interface PlayerRepository extends JpaRepository<PlayerBean, Long> {
}
```

随后，在需要使用 `PlayerRepository` 的类中，你可以通过 `@Autowired` 自动装配，这样就可以直接使用增删改查函数了。示例代码如下：

```java
@Autowired
private PlayerRepository playerRepository;
```

### 插入或更新数据

```java
playerRepository.save(player);
```

更多信息参考[插入数据](/develop/dev-guide-insert-data.md)和[更新数据](/develop/dev-guide-update-data.md)。

### 查询数据

```java
PlayerBean player = playerRepository.findById(id).orElse(null);
```

更多信息参考[查询数据](/develop/dev-guide-get-data-from-single-table.md)。

### 删除数据

```java
playerRepository.deleteById(id);
```

更多信息参考[删除数据](/develop/dev-guide-delete-data.md)。

## 下一步

- 关于本文使用到的第三方库及框架，可以参考各自官方文档：

    - [Spring Framework 官方文档](https://spring.io/projects/spring-framework)
    - [Spring Boot 官方文档](https://spring.io/projects/spring-boot)
    - [Spring Data JPA 官方文档](https://spring.io/projects/spring-data-jpa)
    - [Hibernate 官方文档](https://hibernate.org/orm/documentation)
- 你可以继续阅读开发者文档，以获取更多关于 TiDB 应用开发的最佳实践。例如：[插入数据](/develop/dev-guide-insert-data.md)、[更新数据](/develop/dev-guide-update-data.md)、[删除数据](/develop/dev-guide-delete-data.md)、[单表读取](/develop/dev-guide-get-data-from-single-table.md)、[事务](/develop/dev-guide-transaction-overview.md)、[SQL 性能优化](/develop/dev-guide-optimize-sql-overview.md)等。
- 如果你更倾向于参与课程进行学习，我们也提供专业的 [TiDB 开发者课程](https://cn.pingcap.com/courses-catalog/category/back-end-developer/?utm_source=docs-cn-dev-guide)支持，并在考试后提供相应的[资格认证](https://learn.pingcap.com/learner/certification-center)。
- 我们还额外提供针对 Java 开发者的课程：[使用 Connector/J - TiDB v6](https://learn.pingcap.com/learner/course/840002/?utm_source=docs-cn-dev-guide) 及[在 TiDB 上开发应用的最佳实践 - TiDB v6](https://learn.pingcap.com/learner/course/780002/?utm_source=docs-cn-dev-guide)。

## 需要帮助?

如果在开发的过程中遇到问题，可以在 [AskTUG](https://asktug.com/?utm_source=docs-cn-dev-guide) 上进行提问，寻求帮助。
