---
title: 使用 JDBC 连接到 TiDB
summary: 了解如何使用 JDBC 连接到 TiDB。本文提供了使用 JDBC 与 TiDB 交互的 Java 示例代码片段。
aliases: ['/zh/tidb/dev/sample-application-java','/zh/tidb/dev/dev-guide-sample-application-java']
---

# 使用 JDBC 连接到 TiDB

TiDB 是一个兼容 MySQL 的数据库。JDBC 是 Java 的数据访问 API。[MySQL Connector/J](https://dev.mysql.com/downloads/connector/j/) 是 MySQL 对 JDBC 的实现。

本文档将展示如何使用 TiDB 和 JDBC 来完成以下任务：

- 配置你的环境。
- 使用 JDBC 连接到 TiDB 集群。
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
git clone https://github.com/tidb-samples/tidb-java-jdbc-quickstart.git
cd tidb-java-jdbc-quickstart
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
    export TIDB_HOST='{host}'  # e.g. gateway01.ap-northeast-1.prod.aws.tidbcloud.com
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
    export TIDB_HOST='{host}'  # e.g. tidb.xxxx.clusters.tidb-cloud.com
    export TIDB_PORT='4000'
    export TIDB_USER='{user}'  # e.g. root
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
    export TIDB_HOST='{host}'
    export TIDB_PORT='4000'
    export TIDB_USER='root'
    export TIDB_PASSWORD='{password}'
    export TIDB_DB_NAME='test'
    export USE_SSL='false'
    ```

    注意替换 `{}` 中的占位符为你的 TiDB 对应的值，并设置 `USE_SSL` 为 `false`。如果你在本机运行 TiDB，默认 Host 地址为 `127.0.0.1`，密码为空。

3. 保存 `env.sh` 文件。

</div>

</SimpleTab>

### 第 3 步：运行代码并查看结果

1. 运行下述命令，执行示例代码：

    ```shell
    make
    ```

2. 查看 [`Expected-Output.txt`](https://github.com/tidb-samples/tidb-java-jdbc-quickstart/blob/main/Expected-Output.txt)，并与你的程序输出进行比较。结果近似即为连接成功。

## 示例代码片段

你可参考以下关键代码片段，完成自己的应用开发。

完整代码及其运行方式，见代码仓库 [tidb-java-jdbc-quickstart](https://github.com/tidb-samples/tidb-java-jdbc-quickstart/blob/main/README-zh.md)。

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

### 使用驱动程序还是 ORM 框架？

Java 驱动程序提供对数据库的底层访问，但要求开发者：

- 手动建立和释放数据库连接
- 手动管理数据库事务
- 手动将数据行映射为数据对象

建议仅在需要编写复杂的 SQL 语句时使用驱动程序。其他情况下，建议使用 [ORM](https://zh.wikipedia.org/wiki/对象关系映射) 框架进行开发，例如 [Hibernate](/develop/dev-guide-sample-application-java-hibernate.md)、[MyBatis](/develop/dev-guide-sample-application-java-mybatis.md) 或 [Spring Data JPA](/develop/dev-guide-sample-application-java-spring-boot.md)。ORM 可以帮助你：

- 减少管理连接和事务的[模板代码](https://en.wikipedia.org/wiki/Boilerplate_code)
- 使用数据对象代替大量 SQL 语句来操作数据

## 下一步

- 关于 MySQL Connector/J 的更多使用方法，可以参考 [MySQL Connector/J 官方文档](https://dev.mysql.com/doc/connector-j/en/)。
- 你可以继续阅读开发者文档，以获取更多关于 TiDB 应用开发的最佳实践。例如：[插入数据](/develop/dev-guide-insert-data.md)、[更新数据](/develop/dev-guide-update-data.md)、[删除数据](/develop/dev-guide-delete-data.md)、[单表读取](/develop/dev-guide-get-data-from-single-table.md)、[事务](/develop/dev-guide-transaction-overview.md)、[SQL 性能优化](/develop/dev-guide-optimize-sql-overview.md)等。
- 如果你更倾向于参与课程进行学习，我们也提供专业的 [TiDB 开发者课程](https://cn.pingcap.com/courses-catalog/category/back-end-developer/?utm_source=docs-cn-dev-guide)支持，并在考试后提供相应的[资格认证](https://learn.pingcap.com/learner/certification-center)。
- 我们还额外提供针对 Java 开发者的课程：[使用 Connector/J - TiDB v6](https://learn.pingcap.com/learner/course/840002/?utm_source=docs-cn-dev-guide) 及[在 TiDB 上开发应用的最佳实践 - TiDB v6](https://learn.pingcap.com/learner/course/780002/?utm_source=docs-cn-dev-guide)。

## 需要帮助?

如果在开发的过程中遇到问题，可以在 [AskTUG](https://asktug.com/?utm_source=docs-cn-dev-guide) 上进行提问，寻求帮助。
