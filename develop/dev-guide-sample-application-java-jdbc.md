---
title: 使用 JDBC 连接 TiDB
summary: 学习如何使用 JDBC 连接 TiDB。本教程提供使用 JDBC 操作 TiDB 的 Java 示例代码片段。
---

# 使用 JDBC 连接 TiDB

TiDB 是一个兼容 MySQL 的数据库，而 JDBC（Java Database Connectivity）是 Java 的数据访问 API。[MySQL Connector/J](https://dev.mysql.com/downloads/connector/j/) 是 MySQL 的 JDBC 实现。

在本教程中，你可以学习如何使用 TiDB 和 JDBC 完成以下任务：

- 设置你的环境。
- 使用 JDBC 连接到你的 TiDB 集群。
- 构建并运行你的应用程序。你也可以查看基本 CRUD 操作的[示例代码片段](#示例代码片段)。

<CustomContent platform="tidb">

> **注意：**
>
> - 本教程适用于 TiDB Cloud Serverless、TiDB Cloud Dedicated 和 TiDB Self-Managed。
> - 从 TiDB v7.4 开始，如果在 JDBC URL 中未配置 `connectionCollation`，且 `characterEncoding` 未配置或设置为 `UTF-8`，JDBC 连接中使用的排序规则取决于 JDBC 驱动程序版本。更多信息，请参见 [JDBC 连接中使用的排序规则](/faq/sql-faq.md#collation-used-in-jdbc-connections)。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **注意：**
>
> - 本教程适用于 TiDB Cloud Serverless、TiDB Cloud Dedicated 和 TiDB Self-Managed。
> - 从 TiDB v7.4 开始，如果在 JDBC URL 中未配置 `connectionCollation`，且 `characterEncoding` 未配置或设置为 `UTF-8`，JDBC 连接中使用的排序规则取决于 JDBC 驱动程序版本。更多信息，请参见 [JDBC 连接中使用的排序规则](https://docs.pingcap.com/tidb/stable/sql-faq#collation-used-in-jdbc-connections)。

</CustomContent>

## 前提条件

要完成本教程，你需要：

- **Java Development Kit (JDK) 17** 或更高版本。你可以根据你的业务和个人需求选择 [OpenJDK](https://openjdk.org/) 或 [Oracle JDK](https://www.oracle.com/hk/java/technologies/downloads/)。
- [Maven](https://maven.apache.org/install.html) **3.8** 或更高版本。
- [Git](https://git-scm.com/downloads)。
- 一个 TiDB 集群。

<CustomContent platform="tidb">

**如果你还没有 TiDB 集群，可以按照以下方式创建：**

- （推荐）按照[创建 TiDB Cloud Serverless 集群](/develop/dev-guide-build-cluster-in-cloud.md)的说明创建你自己的 TiDB Cloud 集群。
- 按照[部署本地测试 TiDB 集群](/quick-start-with-tidb.md#deploy-a-local-test-cluster)或[部署生产 TiDB 集群](/production-deployment-using-tiup.md)的说明创建本地集群。

</CustomContent>
<CustomContent platform="tidb-cloud">

> **注意：**
>
> 出于安全考虑，建议你在通过互联网连接到 TiDB 集群时使用 `VERIFY_IDENTITY` 建立 TLS 连接。TiDB Cloud Serverless 和 TiDB Cloud Dedicated 都使用主体备用名称（SAN）证书，这要求 MySQL Connector/J 版本大于或等于 [8.0.22](https://dev.mysql.com/doc/relnotes/connector-j/en/news-8-0-22.html)。

**如果你还没有 TiDB 集群，可以按照以下方式创建：**

- （推荐）按照[创建 TiDB Cloud Serverless 集群](/develop/dev-guide-build-cluster-in-cloud.md)的说明创建你自己的 TiDB Cloud 集群。
- 按照[部署本地测试 TiDB 集群](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb#deploy-a-local-test-cluster)或[部署生产 TiDB 集群](https://docs.pingcap.com/tidb/stable/production-deployment-using-tiup)的说明创建本地集群。

</CustomContent>

## 运行示例应用程序连接 TiDB

本节演示如何运行示例应用程序代码并连接到 TiDB。

### 步骤 1：克隆示例应用程序仓库

在终端窗口中运行以下命令来克隆示例代码仓库：

```shell
git clone https://github.com/tidb-samples/tidb-java-jdbc-quickstart.git
cd tidb-java-jdbc-quickstart
```

### 步骤 2：配置连接信息

根据你选择的 TiDB 部署选项连接到你的 TiDB 集群。

<SimpleTab>
<div label="TiDB Cloud Serverless">

1. 导航到[**集群**](https://tidbcloud.com/project/clusters)页面，然后点击目标集群的名称进入其概览页面。

2. 点击右上角的**连接**。将显示一个连接对话框。

3. 确保连接对话框中的配置与你的操作环境匹配。

    - **连接类型**设置为 `Public`
    - **分支**设置为 `main`
    - **连接工具**设置为 `General`
    - **操作系统**与你的环境匹配。

    > **提示：**
    >
    > 如果你的程序在 Windows Subsystem for Linux (WSL) 中运行，请切换到相应的 Linux 发行版。

4. 点击**生成密码**创建一个随机密码。

    > **提示：**
    >
    > 如果你之前已经创建了密码，你可以使用原始密码，也可以点击**重置密码**生成一个新密码。

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

    TiDB Cloud Serverless 需要安全连接。因此，你需要将 `USE_SSL` 的值设置为 `true`。

7. 保存 `env.sh` 文件。

</div>
<div label="TiDB Cloud Dedicated">

1. 导航到[**集群**](https://tidbcloud.com/project/clusters)页面，然后点击目标集群的名称进入其概览页面。

2. 点击右上角的**连接**。将显示一个连接对话框。

3. 在连接对话框中，从**连接类型**下拉列表中选择 **Public**，然后点击 **CA cert** 下载 CA 证书。

    如果你还没有配置 IP 访问列表，请点击**配置 IP 访问列表**或按照[配置 IP 访问列表](https://docs.pingcap.com/tidbcloud/configure-ip-access-list)中的步骤在首次连接之前进行配置。

    除了 **Public** 连接类型外，TiDB Cloud Dedicated 还支持 **Private Endpoint** 和 **VPC Peering** 连接类型。更多信息，请参见[连接到你的 TiDB Cloud Dedicated 集群](https://docs.pingcap.com/tidbcloud/connect-to-tidb-cluster)。

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

    请确保将占位符 `{}` 替换为连接参数，并将 `USE_SSL` 设置为 `false`。如果你在本地运行 TiDB，默认主机地址是 `127.0.0.1`，密码为空。

3. 保存 `env.sh` 文件。

</div>
</SimpleTab>

### 步骤 3：运行代码并检查结果

1. 执行以下命令运行示例代码：

    ```shell
    make
    ```

2. 查看 [Expected-Output.txt](https://github.com/tidb-samples/tidb-java-jdbc-quickstart/blob/main/Expected-Output.txt) 以检查输出是否匹配。

## 示例代码片段

你可以参考以下示例代码片段来完成你自己的应用程序开发。

有关完整的示例代码及其运行方法，请查看 [tidb-samples/tidb-java-jdbc-quickstart](https://github.com/tidb-samples/tidb-java-jdbc-quickstart) 仓库。

### 连接到 TiDB

```java
public MysqlDataSource getMysqlDataSource() throws SQLException {
    MysqlDataSource mysqlDataSource = new MysqlDataSource();

    mysqlDataSource.setServerName(${tidb_host});
    mysqlDataSource.setPortNumber(${tidb_port});
    mysqlDataSource.setUser(${tidb_user});
    mysqlDataSource.setPassword(${tidb_password});
    mysqlDataSource.setDatabaseName(${tidb_db_name});
    if (${tidb_use_ssl}) {
        mysqlDataSource.setSslMode(PropertyDefinitions.SslMode.VERIFY_IDENTITY.name());
        mysqlDataSource.setEnabledTLSProtocols("TLSv1.2,TLSv1.3");
    }

    return mysqlDataSource;
}
```

使用此函数时，你需要将 `${tidb_host}`、`${tidb_port}`、`${tidb_user}`、`${tidb_password}` 和 `${tidb_db_name}` 替换为你的 TiDB 集群的实际值。

### 插入数据

```java
public void createPlayer(PlayerBean player) throws SQLException {
    MysqlDataSource mysqlDataSource = getMysqlDataSource();
    try (Connection connection = mysqlDataSource.getConnection()) {
        PreparedStatement preparedStatement = connection.prepareStatement("INSERT INTO player (id, coins, goods) VALUES (?, ?, ?)");
        preparedStatement.setString(1, player.getId());
        preparedStatement.setInt(2, player.getCoins());
        preparedStatement.setInt(3, player.getGoods());

        preparedStatement.execute();
    }
}
```

更多信息，请参考[插入数据](/develop/dev-guide-insert-data.md)。

### 查询数据

```java
public void getPlayer(String id) throws SQLException {
    MysqlDataSource mysqlDataSource = getMysqlDataSourceByEnv();
    try (Connection connection = mysqlDataSource.getConnection()) {
        PreparedStatement preparedStatement = connection.prepareStatement("SELECT * FROM player WHERE id = ?");
        preparedStatement.setString(1, id);
        preparedStatement.execute();

        ResultSet res = preparedStatement.executeQuery();
        if(res.next()) {
            PlayerBean player = new PlayerBean(res.getString("id"), res.getInt("coins"), res.getInt("goods"));
            System.out.println(player);
        }
    }
}
```

更多信息，请参考[查询数据](/develop/dev-guide-get-data-from-single-table.md)。

### 更新数据

```java
public void updatePlayer(String id, int amount, int price) throws SQLException {
    MysqlDataSource mysqlDataSource = getMysqlDataSourceByEnv();
    try (Connection connection = mysqlDataSource.getConnection()) {
        PreparedStatement transfer = connection.prepareStatement("UPDATE player SET goods = goods + ?, coins = coins + ? WHERE id=?");
        transfer.setInt(1, -amount);
        transfer.setInt(2, price);
        transfer.setString(3, id);
        transfer.execute();
    }
}
```

更多信息，请参考[更新数据](/develop/dev-guide-update-data.md)。

### 删除数据

```java
public void deletePlayer(String id) throws SQLException {
    MysqlDataSource mysqlDataSource = getMysqlDataSourceByEnv();
    try (Connection connection = mysqlDataSource.getConnection()) {
        PreparedStatement deleteStatement = connection.prepareStatement("DELETE FROM player WHERE id=?");
        deleteStatement.setString(1, id);
        deleteStatement.execute();
    }
}
```

更多信息，请参考[删除数据](/develop/dev-guide-delete-data.md)。

## 实用说明

### 使用驱动程序还是 ORM 框架？

Java 驱动程序提供对数据库的低级访问，但它要求开发人员：

- 手动建立和释放数据库连接。
- 手动管理数据库事务。
- 手动将数据行映射到数据对象。

除非你需要编写复杂的 SQL 语句，否则建议使用 [ORM](https://en.wikipedia.org/w/index.php?title=Object-relational_mapping) 框架进行开发，如 [Hibernate](/develop/dev-guide-sample-application-java-hibernate.md)、[MyBatis](/develop/dev-guide-sample-application-java-mybatis.md) 或 [Spring Data JPA](/develop/dev-guide-sample-application-java-spring-boot.md)。它可以帮助你：

- 减少管理连接和事务的[样板代码](https://en.wikipedia.org/wiki/Boilerplate_code)。
- 使用数据对象而不是大量 SQL 语句来操作数据。

## 下一步

- 从 [MySQL Connector/J 的文档](https://dev.mysql.com/doc/connector-j/en/)中了解更多用法。
- 通过[开发者指南](/develop/dev-guide-overview.md)中的章节学习 TiDB 应用程序开发的最佳实践，例如[插入数据](/develop/dev-guide-insert-data.md)、[更新数据](/develop/dev-guide-update-data.md)、[删除数据](/develop/dev-guide-delete-data.md)、[单表读取](/develop/dev-guide-get-data-from-single-table.md)、[事务](/develop/dev-guide-transaction-overview.md)和 [SQL 性能优化](/develop/dev-guide-optimize-sql-overview.md)。
- 通过专业的 [TiDB 开发者课程](https://www.pingcap.com/education/)学习，并在通过考试后获得 [TiDB 认证](https://www.pingcap.com/education/certification/)。
- 通过面向 Java 开发者的课程学习：[使用 Java 操作 TiDB](https://eng.edu.pingcap.com/catalog/info/id:212)。

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上询问社区，或[提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上询问社区，或[提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>
