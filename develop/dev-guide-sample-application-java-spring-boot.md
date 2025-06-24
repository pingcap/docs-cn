---
title: 使用 Spring Boot 连接 TiDB
summary: 了解如何使用 Spring Boot 连接 TiDB。本教程提供使用 Spring Boot 操作 TiDB 的 Java 示例代码片段。
---

# 使用 Spring Boot 连接 TiDB

TiDB 是一个兼容 MySQL 的数据库，而 [Spring](https://spring.io/) 是一个流行的开源 Java 容器框架。本文档使用 [Spring Boot](https://spring.io/projects/spring-boot) 作为使用 Spring 的方式。

在本教程中，您将学习如何使用 TiDB 以及 [Spring Data JPA](https://spring.io/projects/spring-data-jpa) 和作为 JPA 提供者的 [Hibernate](https://hibernate.org/orm/) 来完成以下任务：

- 设置环境。
- 使用 Hibernate 和 Spring Data JPA 连接到您的 TiDB 集群。
- 构建并运行您的应用程序。您也可以查看[示例代码片段](#示例代码片段)以了解基本的 CRUD 操作。

> **注意：**
>
> 本教程适用于 TiDB Cloud Serverless、TiDB Cloud Dedicated 和 TiDB Self-Managed。

## 前提条件

要完成本教程，您需要：

- **Java Development Kit (JDK) 17** 或更高版本。您可以根据您的业务和个人需求选择 [OpenJDK](https://openjdk.org/) 或 [Oracle JDK](https://www.oracle.com/hk/java/technologies/downloads/)。
- [Maven](https://maven.apache.org/install.html) **3.8** 或更高版本。
- [Git](https://git-scm.com/downloads)。
- 一个 TiDB 集群。

<CustomContent platform="tidb">

**如果您还没有 TiDB 集群，可以按照以下方式创建：**

- （推荐）按照[创建 TiDB Cloud Serverless 集群](/develop/dev-guide-build-cluster-in-cloud.md)的说明创建您自己的 TiDB Cloud 集群。
- 按照[部署本地测试 TiDB 集群](/quick-start-with-tidb.md#deploy-a-local-test-cluster)或[部署生产 TiDB 集群](/production-deployment-using-tiup.md)的说明创建本地集群。

</CustomContent>
<CustomContent platform="tidb-cloud">

**如果您还没有 TiDB 集群，可以按照以下方式创建：**

- （推荐）按照[创建 TiDB Cloud Serverless 集群](/develop/dev-guide-build-cluster-in-cloud.md)的说明创建您自己的 TiDB Cloud 集群。
- 按照[部署本地测试 TiDB 集群](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb#deploy-a-local-test-cluster)或[部署生产 TiDB 集群](https://docs.pingcap.com/tidb/stable/production-deployment-using-tiup)的说明创建本地集群。

</CustomContent>

## 运行示例应用程序连接 TiDB

本节演示如何运行示例应用程序代码并连接到 TiDB。

### 步骤 1：克隆示例应用程序仓库

在终端窗口中运行以下命令来克隆示例代码仓库：

```shell
git clone https://github.com/tidb-samples/tidb-java-springboot-jpa-quickstart.git
cd tidb-java-springboot-jpa-quickstart
```

### 步骤 2：配置连接信息

根据您选择的 TiDB 部署选项连接到您的 TiDB 集群。

<SimpleTab>
<div label="TiDB Cloud Serverless">

1. 导航到[**集群**](https://tidbcloud.com/project/clusters)页面，然后点击目标集群的名称进入其概览页面。

2. 点击右上角的**连接**。此时会显示一个连接对话框。

3. 确保连接对话框中的配置与您的操作环境相匹配。

    - **连接类型**设置为 `Public`
    - **分支**设置为 `main`
    - **连接方式**设置为 `General`
    - **操作系统**与您的环境匹配。

    > **提示：**
    >
    > 如果您的程序在 Windows Subsystem for Linux (WSL) 中运行，请切换到相应的 Linux 发行版。

4. 点击**生成密码**创建一个随机密码。

    > **提示：**
    >
    > 如果您之前已经创建了密码，您可以使用原始密码，也可以点击**重置密码**生成一个新密码。

5. 运行以下命令复制 `env.sh.example` 并将其重命名为 `env.sh`：

    ```shell
    cp env.sh.example env.sh
    ```

6. 将相应的连接字符串复制并粘贴到 `env.sh` 文件中。示例结果如下：

    ```shell
    export TIDB_HOST='{host}'  # 例如 gateway01.ap-northeast-1.prod.aws.tidbcloud.com
    export TIDB_PORT='4000'
    export TIDB_USER='{user}'  # 例如 xxxxxx.root
    export TIDB_PASSWORD='{password}'
    export TIDB_DB_NAME='test'
    export USE_SSL='true'
    ```

    请确保将占位符 `{}` 替换为从连接对话框获得的连接参数。

    TiDB Cloud Serverless 需要安全连接。因此，您需要将 `USE_SSL` 的值设置为 `true`。

7. 保存 `env.sh` 文件。

</div>
<div label="TiDB Cloud Dedicated">

1. 导航到[**集群**](https://tidbcloud.com/project/clusters)页面，然后点击目标集群的名称进入其概览页面。

2. 点击右上角的**连接**。此时会显示一个连接对话框。

3. 在连接对话框中，从**连接类型**下拉列表中选择**公共**，然后点击 **CA 证书**下载 CA 证书。

    如果您尚未配置 IP 访问列表，请点击**配置 IP 访问列表**或按照[配置 IP 访问列表](https://docs.pingcap.com/tidbcloud/configure-ip-access-list)中的步骤在首次连接之前进行配置。

    除了**公共**连接类型外，TiDB Cloud Dedicated 还支持**私有端点**和 **VPC 对等连接**连接类型。更多信息，请参见[连接到您的 TiDB Cloud Dedicated 集群](https://docs.pingcap.com/tidbcloud/connect-to-tidb-cluster)。

4. 运行以下命令复制 `env.sh.example` 并将其重命名为 `env.sh`：

    ```shell
    cp env.sh.example env.sh
    ```

5. 将相应的连接字符串复制并粘贴到 `env.sh` 文件中。示例结果如下：

    ```shell
    export TIDB_HOST='{host}'  # 例如 tidb.xxxx.clusters.tidb-cloud.com
    export TIDB_PORT='4000'
    export TIDB_USER='{user}'  # 例如 root
    export TIDB_PASSWORD='{password}'
    export TIDB_DB_NAME='test'
    export USE_SSL='false'
    ```

    请确保将占位符 `{}` 替换为从连接对话框获得的连接参数。

6. 保存 `env.sh` 文件。

</div>
<div label="TiDB Self-Managed">

1. 运行以下命令复制 `env.sh.example` 并将其重命名为 `env.sh`：

    ```shell
    cp env.sh.example env.sh
    ```

2. 将相应的连接字符串复制并粘贴到 `env.sh` 文件中。示例结果如下：

    ```shell
    export TIDB_HOST='{host}'
    export TIDB_PORT='4000'
    export TIDB_USER='root'
    export TIDB_PASSWORD='{password}'
    export TIDB_DB_NAME='test'
    export USE_SSL='false'
    ```

    请确保将占位符 `{}` 替换为连接参数，并将 `USE_SSL` 设置为 `false`。如果您在本地运行 TiDB，默认主机地址是 `127.0.0.1`，密码为空。

3. 保存 `env.sh` 文件。

</div>
</SimpleTab>

### 步骤 3：运行代码并检查结果

1. 执行以下命令运行示例代码：

    ```shell
    make
    ```

2. 在另一个终端会话中运行请求脚本：

    ```shell
    make request
    ```

3. 查看 [Expected-Output.txt](https://github.com/tidb-samples/tidb-java-springboot-jpa-quickstart/blob/main/Expected-Output.txt) 以检查输出是否匹配。

## 示例代码片段

您可以参考以下示例代码片段来完成您自己的应用程序开发。

有关完整的示例代码及其运行方法，请查看 [tidb-samples/tidb-java-springboot-jpa-quickstart](https://github.com/tidb-samples/tidb-java-springboot-jpa-quickstart) 仓库。

### 连接到 TiDB

编辑配置文件 `application.yml`：

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

配置完成后，将环境变量 `TIDB_JDBC_URL`、`TIDB_USER` 和 `TIDB_PASSWORD` 设置为您的 TiDB 集群的实际值。配置文件为这些环境变量提供了默认设置。如果您不配置环境变量，默认值如下：

- `TIDB_JDBC_URL`：`"jdbc:mysql://localhost:4000/test"`
- `TIDB_USER`：`"root"`
- `TIDB_PASSWORD`：`""`

### 数据管理：`@Repository`

Spring Data JPA 通过 `@Repository` 接口管理数据。要使用 `JpaRepository` 提供的 CRUD 操作，您需要扩展 `JpaRepository` 接口：

```java
@Repository
public interface PlayerRepository extends JpaRepository<PlayerBean, Long> {
}
```

然后，您可以在任何需要 `PlayerRepository` 的类中使用 `@Autowired` 进行自动依赖注入。这使您可以直接使用 CRUD 函数。示例如下：

```java
@Autowired
private PlayerRepository playerRepository;
```

### 插入或更新数据

```java
playerRepository.save(player);
```

更多信息，请参见[插入数据](/develop/dev-guide-insert-data.md)和[更新数据](/develop/dev-guide-update-data.md)。

### 查询数据

```java
PlayerBean player = playerRepository.findById(id).orElse(null);
```

更多信息，请参见[查询数据](/develop/dev-guide-get-data-from-single-table.md)。

### 删除数据

```java
playerRepository.deleteById(id);
```

更多信息，请参见[删除数据](/develop/dev-guide-delete-data.md)。

## 下一步

- 要了解本文档中使用的第三方库和框架的更多用法，请参考它们的官方文档：

    - [Spring Framework 的文档](https://spring.io/projects/spring-framework)
    - [Spring Boot 的文档](https://spring.io/projects/spring-boot)
    - [Spring Data JPA 的文档](https://spring.io/projects/spring-data-jpa)
    - [Hibernate 的文档](https://hibernate.org/orm/documentation)

- 通过[开发者指南](/develop/dev-guide-overview.md)中的章节学习 TiDB 应用程序开发的最佳实践，例如[插入数据](/develop/dev-guide-insert-data.md)、[更新数据](/develop/dev-guide-update-data.md)、[删除数据](/develop/dev-guide-delete-data.md)、[单表读取](/develop/dev-guide-get-data-from-single-table.md)、[事务](/develop/dev-guide-transaction-overview.md)和 [SQL 性能优化](/develop/dev-guide-optimize-sql-overview.md)。
- 学习专业的 [TiDB 开发者课程](https://www.pingcap.com/education/)，并在通过考试后获得 [TiDB 认证](https://www.pingcap.com/education/certification/)。
- 学习 Java 开发者课程：[使用 Java 操作 TiDB](https://eng.edu.pingcap.com/catalog/info/id:212)。

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上询问社区，或[提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上询问社区，或[提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>
