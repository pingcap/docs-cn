---
title: 使用 JDBC 连接到 TiDB
summary: 本文描述了 TiDB 和 JDBC 的连接步骤，并给出了简单示例代码片段。
---

<!-- markdownlint-disable MD024 -->
<!-- markdownlint-disable MD029 -->

# 如何用 JDBC 连接到 TiDB

TiDB 是一个兼容 MySQL 的数据库。**JDBC** 是 Java 的数据访问 API。[MySQL Connector/J](https://dev.mysql.com/downloads/connector/j/) 是 MySQL 对 JDBC 的实现。

本文档将展示如何使用 TiDB 和 JDBC 来构造一个简单的 CRUD 应用程序。

## 前置需求

- 推荐 **Java Development Kit** (JDK) **17** 及以上版本，你可以根据公司及个人需求，自行选择 [OpenJDK](https://openjdk.org/) 或 [Oracle JDK](https://www.oracle.com/hk/java/technologies/downloads/)。
- [Maven](https://maven.apache.org/install.html) **3.8** 及以上版本。
- [Git](https://git-scm.com/downloads)。
- TiDB 集群。如果你还没有 TiDB 集群，可以按照以下方式创建：
    - （推荐方式）参考[创建 TiDB Serverless 集群](/develop/dev-guide-build-cluster-in-cloud.md#第-1-步创建-tidb-serverless-集群)，创建你自己的 TiDB Cloud 集群。
    - 参考[部署本地测试 TiDB 集群](/quick-start-with-tidb.md#部署本地测试集群)或[部署正式 TiDB 集群](/production-deployment-using-tiup.md)，创建本地集群。

## 运行代码并连接到 TiDB

本小节演示如何运行示例应用程序的代码，并连接到 TiDB。

### 第 1 步：克隆示例代码仓库到本地

```bash
git clone https://github.com/tidb-samples/tidb-java-jdbc-quickstart.git
cd tidb-java-jdbc-quickstart
```

### 第 2 步：配置连接信息

根据不同的 TiDB 部署方式，使用不同的方法连接到 TiDB 集群。

<SimpleTab>

<div label="TiDB Serverless">

1. 在 TiDB Cloud Web Console 中，选择你的 TiDB Serverless 集群，进入 **Overview** 页面，点击右上角的 **Connect** 按钮。

2. 确认窗口中的配置和你的运行环境一致。

    - Endpoint 为 **Public**
    - Connect With 选择 **General**
    - Operating System 为你的运行环境。

    <Tip>如果你在 Windows Subsystem for Linux (WSL) 中运行，请切换为对应的 Linux 发行版。</Tip>

3. 点击 **Generate Password** 生成密码。

   <Tip>如果你之前已经生成过密码，可以直接使用原密码，或点击 **Reset Password** 重新生成密码。</Tip>

4. 运行以下命令，将 `env.sh.example` 复制并重命名为 `env.sh`：

    ```bash
    cp env.sh.example env.sh
    ```

5. 复制并粘贴对应连接字符串至 `env.sh` 中。需更改部分示例结果如下。

    ```shell
    export TIDB_HOST='{gateway-region}.aws.tidbcloud.com'
    export TIDB_PORT='4000'
    export TIDB_USER='{prefix}.root'
    export TIDB_PASSWORD='{password}'
    export TIDB_DB_NAME='test'
    export USE_SSL='true'
    ```

    注意替换 `{}` 中的占位符为 **Connect** 窗口中获得的值。

    TiDB Serverless 要求使用 secure connection，因此 `USE_SSL` 的值应为 `true`。

6. 保存文件。

</div>

<div label="TiDB Dedicated">

1. 在 TiDB Cloud 的 [**Clusters**](https://tidbcloud.com/console/clusters) 页面，选择你的 TiDB Dedicated 集群，进入 **Overview** 页面。

2. 点击右上角的 **Connect** 按钮，会显示连接对话框。

3. 点击 **Allow Access from Anywhere**。

    更多配置细节，可参考 [TiDB Dedicated 标准连接教程](https://docs.pingcap.com/tidbcloud/connect-via-standard-connection)。

4. 运行以下命令，将 `env.sh.example` 复制并重命名为 `env.sh`：

    ```bash
    cp env.sh.example env.sh
    ```

5. 复制并粘贴对应的连接字符串至 `env.sh` 中。需更改部分示例结果如下。

    ```shell
    export TIDB_HOST='{host}.clusters.tidb-cloud.com'
    export TIDB_PORT='4000'
    export TIDB_USER='{prefix}.root'
    export TIDB_PASSWORD='{password}'
    export TIDB_DB_NAME='test'
    export USE_SSL='false'
    ```

    注意替换 `{}` 中的占位符为 **Connect** 窗口中获得的值。

6. 保存文件。

</div>

<div label="自建 TiDB">

1. 运行以下命令，将 `env.sh.example` 复制并重命名为 `env.sh`：

    ```bash
    cp env.sh.example env.sh
    ```

2. 复制并粘贴对应的连接字符串至 `env.sh` 中。需更改部分示例结果如下。

    ```shell
    export TIDB_HOST='{tidb_server_host}'
    export TIDB_PORT='4000'
    export TIDB_USER='root'
    export TIDB_PASSWORD='{password}'
    export TIDB_DB_NAME='test'
    export USE_SSL='false'
    ```

    注意替换 `{}` 中的占位符为你的 TiDB 对应的值，并设置 `USE_SSL` 为 `false`。如果你在本机运行 TiDB，默认 Host 地址为 `127.0.0.1`，密码为空。

3. 保存文件。

</div>

</SimpleTab>

### 第 3 步：运行代码并查看结果

1. 运行下述命令，执行示例代码：

    ```shell
    make
    ```

2. 查看[示例输出](https://github.com/tidb-samples/tidb-java-jdbc-quickstart/blob/main/Expected-Output.txt)，并与你的程序输出进行比较。结果近似即为连接成功。

## 重点代码片段

你可参考以下关键代码片段，完成自己的应用开发。

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

在使用该函数时，你需要将 `${tidb_host}`、`${tidb_port}`、`${tidb_user}`、`${tidb_password}`、`${tidb_db_name}` 等替换为你的 TiDB 集群的实际值。

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

更多信息参考[插入数据](/develop/dev-guide-insert-data.md)。

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

更多信息参考[查询数据](/develop/dev-guide-get-data-from-single-table.md)。

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

更多信息参考[更新数据](/develop/dev-guide-update-data.md)。

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

更多信息参考[删除数据](/develop/dev-guide-delete-data.md)。

## 注意事项

- 完整代码及其运行方式，见 [tidb-java-jdbc-quickstart](https://github.com/tidb-samples/tidb-java-jdbc-quickstart/blob/main/README-zh.md) GitHub 仓库。
- 关于 **MySQL Connector/J** 的更多使用方法及细节，可以参考 [MySQL Connector/J 官方文档](https://dev.mysql.com/doc/connector-j/8.1/en/)。

### 使用驱动程序还是 ORM 框架？

Java 驱动程序提供对数据库的底层访问，但需要开发人员：

- 手动建立和释放数据库连接。
- 手动管理数据库事务。
- 手动将数据行映射为数据对象。

除非需要编写复杂的 SQL 语句，否则建议使用 [ORM](https://en.wikipedia.org/w/index.php?title=Object-relational_mapping) 框架、数据持久化框架或数据持久化 API 进行开发。例如：[Hibernate](/develop/dev-guide-sample-application-java-hibernate.md)、[MyBatis](/develop/dev-guide-sample-application-java-mybatis.md) 或 [Spring Data JPA](/develop/dev-guide-sample-application-java-spring-boot.md)。它可以帮助你：

- 减少管理连接和事务的[模板代码](https://en.wikipedia.org/wiki/Boilerplate_code)。
- 使用数据对象而不是大量 SQL 语句来操作数据。

## 下一步

- 你可以继续阅读开发者文档，以获取更多关于 TiDB 的开发者知识。例如：[插入数据](/develop/dev-guide-insert-data.md)，[更新数据](/develop/dev-guide-update-data.md)，[删除数据](/develop/dev-guide-delete-data.md)，[单表读取](/develop/dev-guide-get-data-from-single-table.md)，[事务](/develop/dev-guide-transaction-overview.md)，[SQL 性能优化](/develop/dev-guide-optimize-sql-overview.md)等。
- 如果你更倾向于参与课程进行学习，我们也提供专业的 [TiDB 开发者课程](https://cn.pingcap.com/courses-catalog/back-end-developer/?utm_source=docs-cn-dev-guide)支持，并在考试后提供相应的[资格认证](https://learn.pingcap.com/learner/certification-center)。
- 我们还有额外针对 Java 开发者的课程：[使用 Connector/J - TiDB v6](https://learn.pingcap.com/learner/course/840002/?utm_source=docs-cn-dev-guide) 及[在 TiDB 上开发应用的最佳实践 - TiDB v6](https://learn.pingcap.com/learner/course/780002/?utm_source=docs-cn-dev-guide) 可供选择。