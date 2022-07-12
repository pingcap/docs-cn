---
title: TiDB 和 Java 的简单 CRUD 应用程序
summary: 给出一个 TiDB 和 Java 的简单 CRUD 应用程序示例。
aliases: ['/zh/tidb/dev/sample-application-java']
---

<!-- markdownlint-disable MD024 -->
<!-- markdownlint-disable MD029 -->

# TiDB 和 Java 的简单 CRUD 应用程序

本文档将展示如何使用 TiDB 和 Java 来构造一个简单的 CRUD 应用程序。

> **注意：**
>
> 推荐使用 Java 8 及以上版本进行 TiDB 的应用程序的编写。

> **建议：**
>
> 如果你希望使用 Spring Boot 进行 TiDB 应用程序的编写，可以查看 [Build the TiDB Application using Spring Boot](/develop/dev-guide-sample-application-spring-boot.md)。

## 第 1 步：启动你的 TiDB 集群

本节将介绍 TiDB 集群的启动方法。

### 使用 TiDB Cloud 免费集群

[创建免费集群](/develop/dev-guide-build-cluster-in-cloud.md#第-1-步创建免费集群)。

### 使用本地集群

此处将简要叙述启动一个测试集群的过程，若需查看正式环境集群部署，或查看更详细的部署内容，请查阅[本地启动 TiDB](/quick-start-with-tidb.md)。

**部署本地测试集群**

适用场景：利用本地 macOS 或者单机 Linux 环境快速部署 TiDB 测试集群，体验 TiDB 集群的基本架构，以及 TiDB、TiKV、PD、监控等基础组件的运行

1. 下载并安装 TiUP。

    {{< copyable "shell-regular" >}}

    ```shell
    curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
    ```

2. 声明全局环境变量。

    > **注意：**
    >
    > TiUP 安装完成后会提示对应 profile 文件的绝对路径。在执行以下 source 命令前，需要根据 profile 文件的实际位置修改命令。

    {{< copyable "shell-regular" >}}

    ```shell
    source .bash_profile
    ```

3. 在当前 session 执行以下命令启动集群。

    - 直接执行 `tiup playground` 命令会运行最新版本的 TiDB 集群，其中 TiDB、TiKV、PD 和 TiFlash 实例各 1 个：

        {{< copyable "shell-regular" >}}

        ```shell
        tiup playground
        ```

    - 也可以指定 TiDB 版本以及各组件实例个数，命令类似于：

        {{< copyable "shell-regular" >}}

        ```shell
        tiup playground v5.4.0 --db 2 --pd 3 --kv 3
        ```

        上述命令会在本地下载并启动某个版本的集群（例如 v5.4.0）。最新版本可以通过执行`tiup list tidb` 来查看。运行结果将显示集群的访问方式：

        ```
        CLUSTER START SUCCESSFULLY, Enjoy it ^-^
        To connect TiDB: mysql --comments --host 127.0.0.1 --port 4001 -u root -p (no password)
        To connect TiDB: mysql --comments --host 127.0.0.1 --port 4000 -u root -p (no password)
        To view the dashboard: http://127.0.0.1:2379/dashboard
        PD client endpoints: [127.0.0.1:2379 127.0.0.1:2382 127.0.0.1:2384]
        To view the Prometheus: http://127.0.0.1:9090
        To view the Grafana: http://127.0.0.1:3000
        ```

> **注意：**
>
> - 支持 v5.2.0 及以上版本的 TiDB 在 Apple M1 芯片的机器上运行 `tiup playground`。
> - 以这种方式执行的 playground，在结束部署测试后 TiUP 会清理掉原集群数据，重新执行该命令后会得到一个全新的集群。
> - 若希望持久化数据，可以执行 TiUP 的 `--tag` 参数：`tiup --tag <your-tag> playground ...`，详情参考 [TiUP 参考手册](/tiup/tiup-reference.md#-t---tag-string)。

### 使用云原生开发环境

基于 Git 的预配置的开发环境: [现在就试试](/develop/dev-guide-playground-gitpod.md)

该环境会自动克隆代码，并通过 TiUP 部署测试集群。

## 第 2 步：获取代码

{{< copyable "shell-regular" >}}

```shell
git clone https://github.com/pingcap-inc/tidb-example-java.git
```

<SimpleTab>

<div label="使用 JDBC" href="get-code-jdbc">

进入目录 `plain-java-jdbc`：

{{< copyable "shell-regular" >}}

```shell
cd plain-java-jdbc
```

目录结构如下所示：

```
.
├── Makefile
├── plain-java-jdbc.iml
├── pom.xml
└── src
    └── main
        ├── java
        │   └── com
        │       └── pingcap
        │            └── JDBCExample.java
        └── resources
            └── dbinit.sql
```

其中，`dbinit.sql` 为数据表初始化语句：

{{< copyable "sql" >}}

```sql
USE test;
DROP TABLE IF EXISTS player;

CREATE TABLE player (
    `id` VARCHAR(36),
    `coins` INTEGER,
    `goods` INTEGER,
   PRIMARY KEY (`id`)
);
```

`JDBCExample.java` 是 `plain-java-jdbc` 这个示例程序的主体。因为 TiDB 与 MySQL 协议兼容，因此，需要初始化一个 MySQL 协议的数据源 `MysqlDataSource`，以此连接到 TiDB。并在其后，初始化 `PlayerDAO`，用来管理数据对象，进行增删改查等操作。

`PlayerDAO` 是程序用来管理数据对象的类。其中 `DAO` 是 [Data Access Object](https://en.wikipedia.org/wiki/Data_access_object) 的缩写。在其中定义了一系列数据的操作方法，用来对提供数据的写入能力。

`PlayerBean` 是数据实体类，为数据库表在程序内的映射。`PlayerBean` 的每个属性都对应着 `player` 表的一个字段。

{{< copyable "" >}}

```java
package com.pingcap;

import com.mysql.cj.jdbc.MysqlDataSource;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.*;

/**
 * Main class for the basic JDBC example.
 **/
public class JDBCExample
{
    public static class PlayerBean {
        private String id;
        private Integer coins;
        private Integer goods;

        public PlayerBean() {
        }

        public PlayerBean(String id, Integer coins, Integer goods) {
            this.id = id;
            this.coins = coins;
            this.goods = goods;
        }

        public String getId() {
            return id;
        }

        public void setId(String id) {
            this.id = id;
        }

        public Integer getCoins() {
            return coins;
        }

        public void setCoins(Integer coins) {
            this.coins = coins;
        }

        public Integer getGoods() {
            return goods;
        }

        public void setGoods(Integer goods) {
            this.goods = goods;
        }

        @Override
        public String toString() {
            return String.format("    %-8s => %10s\n    %-8s => %10s\n    %-8s => %10s\n",
                    "id", this.id, "coins", this.coins, "goods", this.goods);
        }
    }

    /**
     * Data access object used by 'ExampleDataSource'.
     * Example for CURD and bulk insert.
     */
    public static class PlayerDAO {
        private final MysqlDataSource ds;
        private final Random rand = new Random();

        PlayerDAO(MysqlDataSource ds) {
            this.ds = ds;
        }

        /**
         * Create players by passing in a List of PlayerBean.
         *
         * @param players Will create players list
         * @return The number of create accounts
         */
        public int createPlayers(List<PlayerBean> players){
            int rows = 0;

            Connection connection = null;
            PreparedStatement preparedStatement = null;
            try {
                connection = ds.getConnection();
                preparedStatement = connection.prepareStatement("INSERT INTO player (id, coins, goods) VALUES (?, ?, ?)");
            } catch (SQLException e) {
                System.out.printf("[createPlayers] ERROR: { state => %s, cause => %s, message => %s }\n",
                        e.getSQLState(), e.getCause(), e.getMessage());
                e.printStackTrace();

                return -1;
            }

            try {
                for (PlayerBean player : players) {
                    preparedStatement.setString(1, player.getId());
                    preparedStatement.setInt(2, player.getCoins());
                    preparedStatement.setInt(3, player.getGoods());

                    preparedStatement.execute();
                    rows += preparedStatement.getUpdateCount();
                }
            } catch (SQLException e) {
                System.out.printf("[createPlayers] ERROR: { state => %s, cause => %s, message => %s }\n",
                        e.getSQLState(), e.getCause(), e.getMessage());
                e.printStackTrace();
            } finally {
                try {
                    connection.close();
                } catch (SQLException e) {
                    e.printStackTrace();
                }
            }

            System.out.printf("\n[createPlayers]:\n    '%s'\n", preparedStatement);
            return rows;
        }

        /**
         * Buy goods and transfer funds between one player and another in one transaction.
         * @param sellId Sell player id.
         * @param buyId Buy player id.
         * @param amount Goods amount, if sell player has not enough goods, the trade will break.
         * @param price Price should pay, if buy player has not enough coins, the trade will break.
         *
         * @return The number of effected players.
         */
        public int buyGoods(String sellId, String buyId, Integer amount, Integer price) {
            int effectPlayers = 0;

            Connection connection = null;
            try {
                connection = ds.getConnection();
            } catch (SQLException e) {
                System.out.printf("[buyGoods] ERROR: { state => %s, cause => %s, message => %s }\n",
                        e.getSQLState(), e.getCause(), e.getMessage());
                e.printStackTrace();
                return effectPlayers;
            }

            try {
                connection.setAutoCommit(false);

                PreparedStatement playerQuery = connection.prepareStatement("SELECT * FROM player WHERE id=? OR id=? FOR UPDATE");
                playerQuery.setString(1, sellId);
                playerQuery.setString(2, buyId);
                playerQuery.execute();

                PlayerBean sellPlayer = null;
                PlayerBean buyPlayer = null;

                ResultSet playerQueryResultSet = playerQuery.getResultSet();
                while (playerQueryResultSet.next()) {
                    PlayerBean player =  new PlayerBean(
                            playerQueryResultSet.getString("id"),
                            playerQueryResultSet.getInt("coins"),
                            playerQueryResultSet.getInt("goods")
                    );

                    System.out.println("\n[buyGoods]:\n    'check goods and coins enough'");
                    System.out.println(player);

                    if (sellId.equals(player.getId())) {
                        sellPlayer = player;
                    } else {
                        buyPlayer = player;
                    }
                }

                if (sellPlayer == null || buyPlayer == null) {
                    throw new SQLException("player not exist.");
                }

                if (sellPlayer.getGoods().compareTo(amount) < 0) {
                    throw new SQLException(String.format("sell player %s goods not enough.", sellId));
                }

                if (buyPlayer.getCoins().compareTo(price) < 0) {
                    throw new SQLException(String.format("buy player %s coins not enough.", buyId));
                }

                PreparedStatement transfer = connection.prepareStatement("UPDATE player set goods = goods + ?, coins = coins + ? WHERE id=?");
                transfer.setInt(1, -amount);
                transfer.setInt(2, price);
                transfer.setString(3, sellId);
                transfer.execute();
                effectPlayers += transfer.getUpdateCount();

                transfer.setInt(1, amount);
                transfer.setInt(2, -price);
                transfer.setString(3, buyId);
                transfer.execute();
                effectPlayers += transfer.getUpdateCount();

                connection.commit();

                System.out.println("\n[buyGoods]:\n    'trade success'");
            } catch (SQLException e) {
                System.out.printf("[buyGoods] ERROR: { state => %s, cause => %s, message => %s }\n",
                        e.getSQLState(), e.getCause(), e.getMessage());

                try {
                    System.out.println("[buyGoods] Rollback");

                    connection.rollback();
                } catch (SQLException ex) {
                    // do nothing
                }
            } finally {
                try {
                    connection.close();
                } catch (SQLException e) {
                    // do nothing
                }
            }

            return effectPlayers;
        }

        /**
         * Get the player info by id.
         *
         * @param id Player id.
         * @return The player of this id.
         */
        public PlayerBean getPlayer(String id) {
            PlayerBean player = null;

            try (Connection connection = ds.getConnection()) {
                PreparedStatement preparedStatement = connection.prepareStatement("SELECT * FROM player WHERE id = ?");
                preparedStatement.setString(1, id);
                preparedStatement.execute();

                ResultSet res = preparedStatement.executeQuery();
                if(!res.next()) {
                    System.out.printf("No players in the table with id %s", id);
                } else {
                    player = new PlayerBean(res.getString("id"), res.getInt("coins"), res.getInt("goods"));
                }
            } catch (SQLException e) {
                System.out.printf("PlayerDAO.getPlayer ERROR: { state => %s, cause => %s, message => %s }\n",
                        e.getSQLState(), e.getCause(), e.getMessage());
            }

            return player;
        }

        /**
         * Insert randomized account data (id, coins, goods) using the JDBC fast path for
         * bulk inserts.  The fastest way to get data into TiDB is using the
         * TiDB Lightning(https://docs.pingcap.com/tidb/stable/tidb-lightning-overview).
         * However, if you must bulk insert from the application using INSERT SQL, the best
         * option is the method shown here. It will require the following:
         *
         *    Add `rewriteBatchedStatements=true` to your JDBC connection settings.
         *    Setting rewriteBatchedStatements to true now causes CallableStatements
         *    with batched arguments to be re-written in the form "CALL (...); CALL (...); ..."
         *    to send the batch in as few client/server round trips as possible.
         *    https://dev.mysql.com/doc/relnotes/connector-j/5.1/en/news-5-1-3.html
         *
         *    You can see the `rewriteBatchedStatements` param effect logic at
         *    implement function: `com.mysql.cj.jdbc.StatementImpl.executeBatchUsingMultiQueries`
         *
         * @param total Add players amount.
         * @param batchSize Bulk insert size for per batch.
         *
         * @return The number of new accounts inserted.
         */
        public int bulkInsertRandomPlayers(Integer total, Integer batchSize) {
            int totalNewPlayers = 0;

            try (Connection connection = ds.getConnection()) {
                // We're managing the commit lifecycle ourselves, so we can
                // control the size of our batch inserts.
                connection.setAutoCommit(false);

                // In this example we are adding 500 rows to the database,
                // but it could be any number.  What's important is that
                // the batch size is 128.
                try (PreparedStatement pstmt = connection.prepareStatement("INSERT INTO player (id, coins, goods) VALUES (?, ?, ?)")) {
                    for (int i=0; i<=(total/batchSize);i++) {
                        for (int j=0; j<batchSize; j++) {
                            String id = UUID.randomUUID().toString();
                            pstmt.setString(1, id);
                            pstmt.setInt(2, rand.nextInt(10000));
                            pstmt.setInt(3, rand.nextInt(10000));
                            pstmt.addBatch();
                        }

                        int[] count = pstmt.executeBatch();
                        totalNewPlayers += count.length;
                        System.out.printf("\nPlayerDAO.bulkInsertRandomPlayers:\n    '%s'\n", pstmt);
                        System.out.printf("    => %s row(s) updated in this batch\n", count.length);
                    }
                    connection.commit();
                } catch (SQLException e) {
                    System.out.printf("PlayerDAO.bulkInsertRandomPlayers ERROR: { state => %s, cause => %s, message => %s }\n",
                            e.getSQLState(), e.getCause(), e.getMessage());
                }
            } catch (SQLException e) {
                System.out.printf("PlayerDAO.bulkInsertRandomPlayers ERROR: { state => %s, cause => %s, message => %s }\n",
                        e.getSQLState(), e.getCause(), e.getMessage());
            }
            return totalNewPlayers;
        }


        /**
         * Print a subset of players from the data store by limit.
         *
         * @param limit Print max size.
         */
        public void printPlayers(Integer limit) {
            try (Connection connection = ds.getConnection()) {
                PreparedStatement preparedStatement = connection.prepareStatement("SELECT * FROM player LIMIT ?");
                preparedStatement.setInt(1, limit);
                preparedStatement.execute();

                ResultSet res = preparedStatement.executeQuery();
                while (!res.next()) {
                    PlayerBean player = new PlayerBean(res.getString("id"),
                            res.getInt("coins"), res.getInt("goods"));
                    System.out.println("\n[printPlayers]:\n" + player);
                }
            } catch (SQLException e) {
                System.out.printf("PlayerDAO.printPlayers ERROR: { state => %s, cause => %s, message => %s }\n",
                        e.getSQLState(), e.getCause(), e.getMessage());
            }
        }


        /**
         * Count players from the data store.
         *
         * @return All players count
         */
        public int countPlayers() {
            int count = 0;

            try (Connection connection = ds.getConnection()) {
                PreparedStatement preparedStatement = connection.prepareStatement("SELECT count(*) FROM player");
                preparedStatement.execute();

                ResultSet res = preparedStatement.executeQuery();
                if(res.next()) {
                    count = res.getInt(1);
                }
            } catch (SQLException e) {
                System.out.printf("PlayerDAO.countPlayers ERROR: { state => %s, cause => %s, message => %s }\n",
                        e.getSQLState(), e.getCause(), e.getMessage());
            }

            return count;
        }
    }

    public static void main(String[] args) {
        // 1. Configure the example database connection.

        // 1.1 Create a mysql data source instance.
        MysqlDataSource mysqlDataSource = new MysqlDataSource();

        // 1.2 Set server name, port, database name, username and password.
        mysqlDataSource.setServerName("localhost");
        mysqlDataSource.setPortNumber(4000);
        mysqlDataSource.setDatabaseName("test");
        mysqlDataSource.setUser("root");
        mysqlDataSource.setPassword("");

        // Or you can use jdbc string instead.
        // mysqlDataSource.setURL("jdbc:mysql://{host}:{port}/test?user={user}&password={password}");

        // 2. And then, create DAO to manager your data.
        PlayerDAO dao = new PlayerDAO(mysqlDataSource);

        // 3. Run some simple examples.

        // Create a player, who has a coin and a goods..
        dao.createPlayers(Collections.singletonList(new PlayerBean("test", 1, 1)));

        // Get a player.
        PlayerBean testPlayer = dao.getPlayer("test");
        System.out.printf("PlayerDAO.getPlayer:\n    => id: %s\n    => coins: %s\n    => goods: %s\n",
                testPlayer.getId(), testPlayer.getCoins(), testPlayer.getGoods());

        // Create players with bulk inserts. Insert 1919 players totally, with 114 players per batch.
        int addedCount = dao.bulkInsertRandomPlayers(1919, 114);
        System.out.printf("PlayerDAO.bulkInsertRandomPlayers:\n    => %d total inserted players\n", addedCount);

        // Count players amount.
        int count = dao.countPlayers();
        System.out.printf("PlayerDAO.countPlayers:\n    => %d total players\n", count);

        // Print 3 players.
        dao.printPlayers(3);

        // 4. Explore more.

        // Player 1: id is "1", has only 100 coins.
        // Player 2: id is "2", has 114514 coins, and 20 goods.
        PlayerBean player1 = new PlayerBean("1", 100, 0);
        PlayerBean player2 = new PlayerBean("2", 114514, 20);

        // Create two players "by hand", using the INSERT statement on the backend.
        addedCount = dao.createPlayers(Arrays.asList(player1, player2));
        System.out.printf("PlayerDAO.createPlayers:\n    => %d total inserted players\n", addedCount);

        // Player 1 wants to buy 10 goods from player 2.
        // It will cost 500 coins, but player 1 cannot afford it.
        System.out.println("\nPlayerDAO.buyGoods:\n    => this trade will fail");
        int updatedCount = dao.buyGoods(player2.getId(), player1.getId(), 10, 500);
        System.out.printf("PlayerDAO.buyGoods:\n    => %d total update players\n", updatedCount);

        // So player 1 has to reduce the incoming quantity to two.
        System.out.println("\nPlayerDAO.buyGoods:\n    => this trade will success");
        updatedCount = dao.buyGoods(player2.getId(), player1.getId(), 2, 100);
        System.out.printf("PlayerDAO.buyGoods:\n    => %d total update players\n", updatedCount);
    }
}
```

</div>

<div label="使用 Mybatis（推荐）" href="get-code-mybatis">

可以看到，JDBC 实现的代码略显冗余，需要自己管控错误处理逻辑，且不能很好的复用代码，并非最佳实践。

[Mybatis](https://mybatis.org/mybatis-3/index.html) 是当前比较流行的开源 Java 应用持久层框架，本文将以 Maven 插件的方式使用 [MyBatis Generator](https://mybatis.org/generator/quickstart.html) 生成部分持久层代码。

进入目录 `plain-java-mybatis`：

{{< copyable "shell-regular" >}}

```shell
cd plain-java-mybatis
```

目录结构如下所示：

```
.
├── Makefile
├── pom.xml
└── src
    └── main
        ├── java
        │   └── com
        │       └── pingcap
        │           ├── MybatisExample.java
        │           ├── dao
        │           │   └── PlayerDAO.java
        │           └── model
        │               ├── Player.java
        │               ├── PlayerMapper.java
        │               └── PlayerMapperEx.java
        └── resources
            ├── dbinit.sql
            ├── log4j.properties
            ├── mapper
            │   ├── PlayerMapper.xml
            │   └── PlayerMapperEx.xml
            ├── mybatis-config.xml
            └── mybatis-generator.xml
```

其中，自动生成的文件有：

- `src/main/java/com/pingcap/model/Player.java`：Player 实体类文件
- `src/main/java/com/pingcap/model/PlayerMapper.java`：Player Mapper 的接口文件
- `src/main/resources/mapper/PlayerMapper.xml`：Player Mapper 的 XML 映射，它是 Mybatis 用于生成 Player Mapper 接口的实现类的配置

这些文件的生成策略被写在了 `mybatis-generator.xml` 配置文件内，它是 [Mybatis Generator](https://mybatis.org/generator/quickstart.html) 的配置文件，下面配置文件中添加了使用方法的说明：

{{< copyable "" >}}

```xml
<!DOCTYPE generatorConfiguration PUBLIC
 "-//mybatis.org//DTD MyBatis Generator Configuration 1.0//EN"
 "http://mybatis.org/dtd/mybatis-generator-config_1_0.dtd">

<generatorConfiguration>
    <!--
        <context/> entire document: https://mybatis.org/generator/configreference/context.html

        context.id: A unique identifier you like
        context.targetRuntime: Used to specify the runtime target for generated code.
            It has MyBatis3DynamicSql / MyBatis3Kotlin / MyBatis3 / MyBatis3Simple 4 selection to choice.
    -->
    <context id="simple" targetRuntime="MyBatis3">
        <!--
            <commentGenerator/> entire document: https://mybatis.org/generator/configreference/commentGenerator.html

            commentGenerator:
                - property(suppressDate): remove timestamp in comments
                - property(suppressAllComments): remove all comments
        -->
        <commentGenerator>
            <property name="suppressDate" value="true"/>
            <property name="suppressAllComments" value="true" />
        </commentGenerator>

        <!--
            <jdbcConnection/> entire document: https://mybatis.org/generator/configreference/jdbcConnection.html

            jdbcConnection.driverClass: The fully qualified class name for the JDBC driver used to access the database.
                Used mysql-connector-java:5.1.49, should specify JDBC is com.mysql.jdbc.Driver
            jdbcConnection.connectionURL: The JDBC connection URL used to access the database.
        -->
        <jdbcConnection driverClass="com.mysql.jdbc.Driver"
            connectionURL="jdbc:mysql://localhost:4000/test?user=root" />

        <!--
            <javaModelGenerator/> entire document: https://mybatis.org/generator/configreference/javaModelGenerator.html
            Model code file will be generated at ${targetProject}/${targetPackage}

            javaModelGenerator:
                - property(constructorBased): If it's true, generator will create constructor function in model
        -->
        <javaModelGenerator targetPackage="com.pingcap.model" targetProject="src/main/java">
            <property name="constructorBased" value="true"/>
        </javaModelGenerator>

        <!--
            <sqlMapGenerator/> entire document: https://mybatis.org/generator/configreference/sqlMapGenerator.html
            XML SQL mapper file will be generated at ${targetProject}/${targetPackage}
        -->
        <sqlMapGenerator targetPackage="." targetProject="src/main/resources/mapper"/>

        <!--
            <javaClientGenerator/> entire document: https://mybatis.org/generator/configreference/javaClientGenerator.html
            Java code mapper interface file will be generated at ${targetProject}/${targetPackage}

            javaClientGenerator.type (context.targetRuntime is MyBatis3):
                This attribute indicated Mybatis how to implement interface.
                It has ANNOTATEDMAPPER / MIXEDMAPPER / XMLMAPPER 3 selection to choice.
        -->
        <javaClientGenerator type="XMLMAPPER" targetPackage="com.pingcap.model" targetProject="src/main/java"/>

        <!--
            <table/> entire document: https://mybatis.org/generator/configreference/table.html

            table.tableName: The name of the database table.
            table.domainObjectName: The base name from which generated object names will be generated. If not specified, MBG will generate a name automatically based on the tableName.
            table.enableCountByExample: Signifies whether a count by example statement should be generated.
            table.enableUpdateByExample: Signifies whether an update by example statement should be generated.
            table.enableDeleteByExample: Signifies whether a delete by example statement should be generated.
            table.enableSelectByExample: Signifies whether a select by example statement should be generated.
            table.selectByExampleQueryId: This value will be added to the select list of the select by example statement in this form: "'<value>' as QUERYID".
        -->
        <table tableName="player" domainObjectName="Player"
               enableCountByExample="false" enableUpdateByExample="false"
               enableDeleteByExample="false" enableSelectByExample="false"
               selectByExampleQueryId="false"/>
    </context>
</generatorConfiguration>
```

`mybatis-generator.xml` 在 `pom.xml` 中，以 `mybatis-generator-maven-plugin` 插件配置的方式被引入：

```xml
<plugin>
    <groupId>org.mybatis.generator</groupId>
    <artifactId>mybatis-generator-maven-plugin</artifactId>
    <version>1.4.1</version>
    <configuration>
        <configurationFile>src/main/resources/mybatis-generator.xml</configurationFile>
        <verbose>true</verbose>
        <overwrite>true</overwrite>
    </configuration>

    <dependencies>
        <!-- https://mvnrepository.com/artifact/mysql/mysql-connector-java -->
        <dependency>
        <groupId>mysql</groupId>
        <artifactId>mysql-connector-java</artifactId>
        <version>5.1.49</version>
        </dependency>
    </dependencies>
</plugin>
```

在 Maven 插件内引入后，可删除旧的生成文件后，通过命令 `mvn mybatis-generate` 生成新的文件。或者你也可以使用已经编写好的 `make` 命令，通过 `make gen` 来同时删除旧文件，并生成新文件。

> **注意：**
>
> `mybatis-generator.xml` 中的属性 `configuration.overwrite` 仅可控制新生成的 Java 代码文件使用覆盖方式被写入，但 XML 映射文件仍会以追加方式写入。因此，推荐在 Mybaits Generator 生成新的文件前，先删除掉旧的文件。

`Player.java` 是使用 Mybatis Generator 生成出的数据实体类文件，为数据库表在程序内的映射。`Player` 类的每个属性都对应着 `player` 表的一个字段。

{{< copyable "" >}}

```java
package com.pingcap.model;

public class Player {
    private String id;

    private Integer coins;

    private Integer goods;

    public Player(String id, Integer coins, Integer goods) {
        this.id = id;
        this.coins = coins;
        this.goods = goods;
    }

    public Player() {
        super();
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public Integer getCoins() {
        return coins;
    }

    public void setCoins(Integer coins) {
        this.coins = coins;
    }

    public Integer getGoods() {
        return goods;
    }

    public void setGoods(Integer goods) {
        this.goods = goods;
    }
}
```

`PlayerMapper.java` 是使用 Mybatis Generator 生成出的映射接口文件，它仅规定了接口，接口的实现类是由 Mybatis 来通过 XML 或注解自动生成的：

{{< copyable "" >}}

```java
package com.pingcap.model;

import com.pingcap.model.Player;

public interface PlayerMapper {
    int deleteByPrimaryKey(String id);

    int insert(Player row);

    int insertSelective(Player row);

    Player selectByPrimaryKey(String id);

    int updateByPrimaryKeySelective(Player row);

    int updateByPrimaryKey(Player row);
}
```

`PlayerMapper.xml` 是使用 Mybatis Generator 生成出的映射 XML 文件，Mybatis 将使用这个文件自动生成 `PlayerMapper` 接口的实现类：

{{< copyable "" >}}

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN" "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<mapper namespace="com.pingcap.model.PlayerMapper">
  <resultMap id="BaseResultMap" type="com.pingcap.model.Player">
    <constructor>
      <idArg column="id" javaType="java.lang.String" jdbcType="VARCHAR" />
      <arg column="coins" javaType="java.lang.Integer" jdbcType="INTEGER" />
      <arg column="goods" javaType="java.lang.Integer" jdbcType="INTEGER" />
    </constructor>
  </resultMap>
  <sql id="Base_Column_List">
    id, coins, goods
  </sql>
  <select id="selectByPrimaryKey" parameterType="java.lang.String" resultMap="BaseResultMap">
    select 
    <include refid="Base_Column_List" />
    from player
    where id = #{id,jdbcType=VARCHAR}
  </select>
  <delete id="deleteByPrimaryKey" parameterType="java.lang.String">
    delete from player
    where id = #{id,jdbcType=VARCHAR}
  </delete>
  <insert id="insert" parameterType="com.pingcap.model.Player">
    insert into player (id, coins, goods
      )
    values (#{id,jdbcType=VARCHAR}, #{coins,jdbcType=INTEGER}, #{goods,jdbcType=INTEGER}
      )
  </insert>
  <insert id="insertSelective" parameterType="com.pingcap.model.Player">
    insert into player
    <trim prefix="(" suffix=")" suffixOverrides=",">
      <if test="id != null">
        id,
      </if>
      <if test="coins != null">
        coins,
      </if>
      <if test="goods != null">
        goods,
      </if>
    </trim>
    <trim prefix="values (" suffix=")" suffixOverrides=",">
      <if test="id != null">
        #{id,jdbcType=VARCHAR},
      </if>
      <if test="coins != null">
        #{coins,jdbcType=INTEGER},
      </if>
      <if test="goods != null">
        #{goods,jdbcType=INTEGER},
      </if>
    </trim>
  </insert>
  <update id="updateByPrimaryKeySelective" parameterType="com.pingcap.model.Player">
    update player
    <set>
      <if test="coins != null">
        coins = #{coins,jdbcType=INTEGER},
      </if>
      <if test="goods != null">
        goods = #{goods,jdbcType=INTEGER},
      </if>
    </set>
    where id = #{id,jdbcType=VARCHAR}
  </update>
  <update id="updateByPrimaryKey" parameterType="com.pingcap.model.Player">
    update player
    set coins = #{coins,jdbcType=INTEGER},
      goods = #{goods,jdbcType=INTEGER}
    where id = #{id,jdbcType=VARCHAR}
  </update>
</mapper>
```

由于 Mybatis Generator 需要逆向生成源码，因此，数据库中需先行有此表结构，可使用 `dbinit.sql` 生成表结构：

{{< copyable "sql" >}}

```sql
USE test;
DROP TABLE IF EXISTS player;

CREATE TABLE player (
    `id` VARCHAR(36),
    `coins` INTEGER,
    `goods` INTEGER,
    PRIMARY KEY (`id`)
);
```

额外拆分接口 `PlayerMapperEx` 继承 `PlayerMapper`，并且编写与之匹配的 `PlayerMapperEx.xml`。避免直接更改 `PlayerMapper.java` 和 `PlayerMapper.xml`。这是为了规避 Mybatis Generator 的反复生成，影响到自行编写的代码。

在 `PlayerMapperEx.java` 中定义自行增加的接口：

{{< copyable "" >}}

```java
package com.pingcap.model;

import java.util.List;

public interface PlayerMapperEx extends PlayerMapper {
    Player selectByPrimaryKeyWithLock(String id);

    List<Player> selectByLimit(Integer limit);

    Integer count();
}
```

在 `PlayerMapperEx.xml` 中定义映射规则：

{{< copyable "" >}}

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN" "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<mapper namespace="com.pingcap.model.PlayerMapperEx">
  <resultMap id="BaseResultMap" type="com.pingcap.model.Player">
    <constructor>
      <idArg column="id" javaType="java.lang.String" jdbcType="VARCHAR" />
      <arg column="coins" javaType="java.lang.Integer" jdbcType="INTEGER" />
      <arg column="goods" javaType="java.lang.Integer" jdbcType="INTEGER" />
    </constructor>
  </resultMap>
  <sql id="Base_Column_List">
    id, coins, goods
  </sql>

  <select id="selectByPrimaryKeyWithLock" parameterType="java.lang.String" resultMap="BaseResultMap">
    select 
    <include refid="Base_Column_List" />
    from player
    where `id` = #{id,jdbcType=VARCHAR}
    for update
  </select>

  <select id="selectByLimit" parameterType="java.lang.Integer" resultMap="BaseResultMap">
    select
    <include refid="Base_Column_List" />
    from player
    limit #{id,jdbcType=INTEGER}
  </select>

  <select id="count" resultType="java.lang.Integer">
    select count(*) from player
  </select>

</mapper>
```

`PlayerDAO.java` 是程序用来管理数据对象的类。其中 `DAO` 是 [Data Access Object](https://en.wikipedia.org/wiki/Data_access_object) 的缩写。在其中定义了一系列数据的操作方法，用于数据的写入。

{{< copyable "" >}}

```java
package com.pingcap.dao;

import com.pingcap.model.Player;
import com.pingcap.model.PlayerMapperEx;
import org.apache.ibatis.session.SqlSession;
import org.apache.ibatis.session.SqlSessionFactory;

import java.util.List;
import java.util.function.Function;

public class PlayerDAO {
    public static class NotEnoughException extends RuntimeException {
        public NotEnoughException(String message) {
            super(message);
        }
    }

    // Run SQL code in a way that automatically handles the
    // transaction retry logic, so we don't have to duplicate it in
    // various places.
    public Object runTransaction(SqlSessionFactory sessionFactory, Function<PlayerMapperEx, Object> fn) {
        Object resultObject = null;
        SqlSession session = null;

        try {
            // open a session with autoCommit is false
            session = sessionFactory.openSession(false);

            // get player mapper
            PlayerMapperEx playerMapperEx = session.getMapper(PlayerMapperEx.class);

            resultObject = fn.apply(playerMapperEx);
            session.commit();
            System.out.println("APP: COMMIT;");
        } catch (Exception e) {
            if (e instanceof NotEnoughException) {
                System.out.printf("APP: ROLLBACK BY LOGIC; \n%s\n", e.getMessage());
            } else {
                System.out.printf("APP: ROLLBACK BY ERROR; \n%s\n", e.getMessage());
            }

            if (session != null) {
                session.rollback();
            }
        } finally {
            if (session != null) {
                session.close();
            }
        }

        return resultObject;
    }

    public Function<PlayerMapperEx, Object> createPlayers(List<Player> players) {
        return playerMapperEx -> {
            Integer addedPlayerAmount = 0;
            for (Player player: players) {
                playerMapperEx.insert(player);
                addedPlayerAmount ++;
            }
            System.out.printf("APP: createPlayers() --> %d\n", addedPlayerAmount);
            return addedPlayerAmount;
        };
    }

    public Function<PlayerMapperEx, Object> buyGoods(String sellId, String buyId, Integer amount, Integer price) {
        return playerMapperEx -> {
            Player sellPlayer = playerMapperEx.selectByPrimaryKeyWithLock(sellId);
            Player buyPlayer = playerMapperEx.selectByPrimaryKeyWithLock(buyId);

            if (buyPlayer == null || sellPlayer == null) {
                throw new NotEnoughException("sell or buy player not exist");
            }

            if (buyPlayer.getCoins() < price || sellPlayer.getGoods() < amount) {
                throw new NotEnoughException("coins or goods not enough, rollback");
            }

            int affectRows = 0;
            buyPlayer.setGoods(buyPlayer.getGoods() + amount);
            buyPlayer.setCoins(buyPlayer.getCoins() - price);
            affectRows += playerMapperEx.updateByPrimaryKey(buyPlayer);

            sellPlayer.setGoods(sellPlayer.getGoods() - amount);
            sellPlayer.setCoins(sellPlayer.getCoins() + price);
            affectRows += playerMapperEx.updateByPrimaryKey(sellPlayer);

            System.out.printf("APP: buyGoods --> sell: %s, buy: %s, amount: %d, price: %d\n", sellId, buyId, amount, price);
            return affectRows;
        };
    }

    public Function<PlayerMapperEx, Object> getPlayerByID(String id) {
        return playerMapperEx -> playerMapperEx.selectByPrimaryKey(id);
    }

    public Function<PlayerMapperEx, Object> printPlayers(Integer limit) {
        return playerMapperEx -> {
            List<Player> players = playerMapperEx.selectByLimit(limit);

            for (Player player: players) {
                System.out.println("\n[printPlayers]:\n" + player);
            }
            return 0;
        };
    }

    public Function<PlayerMapperEx, Object> countPlayers() {
        return PlayerMapperEx::count;
    }
}
```

`MybatisExample` 是 `plain-java-mybatis` 这个示例程序的主类。其中定义了入口函数：

```java
package com.pingcap;

import com.pingcap.dao.PlayerDAO;
import com.pingcap.model.Player;
import org.apache.ibatis.io.Resources;
import org.apache.ibatis.session.SqlSessionFactory;
import org.apache.ibatis.session.SqlSessionFactoryBuilder;

import java.io.IOException;
import java.io.InputStream;
import java.util.Arrays;
import java.util.Collections;

public class MybatisExample {
    public static void main( String[] args ) throws IOException {
        // 1. Create a SqlSessionFactory based on our mybatis-config.xml configuration
        // file, which defines how to connect to the database.
        InputStream inputStream = Resources.getResourceAsStream("mybatis-config.xml");
        SqlSessionFactory sessionFactory = new SqlSessionFactoryBuilder().build(inputStream);

        // 2. And then, create DAO to manager your data
        PlayerDAO playerDAO = new PlayerDAO();

        // 3. Run some simple examples.

        // Create a player who has 1 coin and 1 goods.
        playerDAO.runTransaction(sessionFactory, playerDAO.createPlayers(
                Collections.singletonList(new Player("test", 1, 1))));

        // Get a player.
        Player testPlayer = (Player)playerDAO.runTransaction(sessionFactory, playerDAO.getPlayerByID("test"));
        System.out.printf("PlayerDAO.getPlayer:\n    => id: %s\n    => coins: %s\n    => goods: %s\n",
                testPlayer.getId(), testPlayer.getCoins(), testPlayer.getGoods());

        // Count players amount.
        Integer count = (Integer)playerDAO.runTransaction(sessionFactory, playerDAO.countPlayers());
        System.out.printf("PlayerDAO.countPlayers:\n    => %d total players\n", count);

        // Print 3 players.
        playerDAO.runTransaction(sessionFactory, playerDAO.printPlayers(3));

        // 4. Getting further.

        // Player 1: id is "1", has only 100 coins.
        // Player 2: id is "2", has 114514 coins, and 20 goods.
        Player player1 = new Player("1", 100, 0);
        Player player2 = new Player("2", 114514, 20);

        // Create two players "by hand", using the INSERT statement on the backend.
        int addedCount = (Integer)playerDAO.runTransaction(sessionFactory,
                playerDAO.createPlayers(Arrays.asList(player1, player2)));
        System.out.printf("PlayerDAO.createPlayers:\n    => %d total inserted players\n", addedCount);

        // Player 1 wants to buy 10 goods from player 2.
        // It will cost 500 coins, but player 1 cannot afford it.
        System.out.println("\nPlayerDAO.buyGoods:\n    => this trade will fail");
        Integer updatedCount = (Integer)playerDAO.runTransaction(sessionFactory,
                playerDAO.buyGoods(player2.getId(), player1.getId(), 10, 500));
        System.out.printf("PlayerDAO.buyGoods:\n    => %d total update players\n", updatedCount);

        // So player 1 has to reduce the incoming quantity to two.
        System.out.println("\nPlayerDAO.buyGoods:\n    => this trade will success");
        updatedCount = (Integer)playerDAO.runTransaction(sessionFactory,
                playerDAO.buyGoods(player2.getId(), player1.getId(), 2, 100));
        System.out.printf("PlayerDAO.buyGoods:\n    => %d total update players\n", updatedCount);
    }
}
```

</div>

<div label="使用 Hibernate（推荐）" href="get-code-hibernate">

可以看到，JDBC 实现的代码略显冗余，需要自己管控错误处理逻辑，且不能很好的复用代码。并非最佳实践。

当前开源比较流行的 Java ORM 为 Hibernate，且 Hibernate 在版本 `6.0.0.Beta2` 及以后支持了 TiDB 方言。完美适配了 TiDB 的特性。因此，此处将以 6.0.0.Beta2 + 版本进行说明。

进入目录 `plain-java-hibernate` ：

{{< copyable "shell-regular" >}}

```shell
cd plain-java-hibernate
```

目录结构如下所示：

```
.
├── Makefile
├── plain-java-hibernate.iml
├── pom.xml
└── src
    └── main
        ├── java
        │   └── com
        │       └── pingcap
        │           └── HibernateExample.java
        └── resources
            └── hibernate.cfg.xml
```

其中，`hibernate.cfg.xml` 为 Hibernate 配置文件，定义了：

{{< copyable "" >}}

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
        <property name="hibernate.connection.url">jdbc:mysql://localhost:4000/test</property>
        <property name="hibernate.connection.username">root</property>
        <property name="hibernate.connection.password"></property>
        <property name="hibernate.connection.autocommit">false</property>

        <!-- Required so a table can be created from the 'PlayerDAO' class -->
        <property name="hibernate.hbm2ddl.auto">create-drop</property>

        <!-- Optional: Show SQL output for debugging -->
        <property name="hibernate.show_sql">true</property>
        <property name="hibernate.format_sql">true</property>
    </session-factory>
</hibernate-configuration>
```

`HibernateExample.java` 是 `plain-java-hibernate` 这个示例程序的主体。使用 Hibernate 时，相较于 JDBC，这里仅需写入配置文件地址，Hibernate 屏蔽了创建数据库连接时，不同数据库差异的细节。

`PlayerDAO` 是程序用来管理数据对象的类。其中 `DAO` 是 [Data Access Object](https://en.wikipedia.org/wiki/Data_access_object) 的缩写。其中定义了一系列数据的操作方法，用来提供数据的写入能力。相较于 JDBC， Hibernate 封装了大量的操作，如对象映射、基本对象的 CRUD 等，极大的简化了代码量。

`PlayerBean` 是数据实体类，为数据库表在程序内的映射。`PlayerBean` 的每个属性都对应着 `player` 表的一个字段。相较于 JDBC，Hibernate 的 `PlayerBean` 实体类为了给 Hibernate 提供更多的信息，加入了注解，用来指示映射关系。

{{< copyable "" >}}

```java
package com.pingcap;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import org.hibernate.JDBCException;
import org.hibernate.Session;
import org.hibernate.SessionFactory;
import org.hibernate.Transaction;
import org.hibernate.cfg.Configuration;
import org.hibernate.query.NativeQuery;
import org.hibernate.query.Query;

import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.function.Function;

@Entity
@Table(name = "player_hibernate")
class PlayerBean {
    @Id
    private String id;
    @Column(name = "coins")
    private Integer coins;
    @Column(name = "goods")
    private Integer goods;

    public PlayerBean() {
    }

    public PlayerBean(String id, Integer coins, Integer goods) {
        this.id = id;
        this.coins = coins;
        this.goods = goods;
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public Integer getCoins() {
        return coins;
    }

    public void setCoins(Integer coins) {
        this.coins = coins;
    }

    public Integer getGoods() {
        return goods;
    }

    public void setGoods(Integer goods) {
        this.goods = goods;
    }

    @Override
    public String toString() {
        return String.format("    %-8s => %10s\n    %-8s => %10s\n    %-8s => %10s\n",
                "id", this.id, "coins", this.coins, "goods", this.goods);
    }
}

/**
 * Main class for the basic Hibernate example.
 **/
public class HibernateExample
{
    public static class PlayerDAO {
        public static class NotEnoughException extends RuntimeException {
            public NotEnoughException(String message) {
                super(message);
            }
        }

        // Run SQL code in a way that automatically handles the
        // transaction retry logic so we don't have to duplicate it in
        // various places.
        public Object runTransaction(Session session, Function<Session, Object> fn) {
            Object resultObject = null;

            Transaction txn = session.beginTransaction();
            try {
                resultObject = fn.apply(session);
                txn.commit();
                System.out.println("APP: COMMIT;");
            } catch (JDBCException e) {
                System.out.println("APP: ROLLBACK BY JDBC ERROR;");
                txn.rollback();
            } catch (NotEnoughException e) {
                System.out.printf("APP: ROLLBACK BY LOGIC; %s", e.getMessage());
                txn.rollback();
            }
            return resultObject;
        }

        public Function<Session, Object> createPlayers(List<PlayerBean> players) throws JDBCException {
            return session -> {
                Integer addedPlayerAmount = 0;
                for (PlayerBean player: players) {
                    session.persist(player);
                    addedPlayerAmount ++;
                }
                System.out.printf("APP: createPlayers() --> %d\n", addedPlayerAmount);
                return addedPlayerAmount;
            };
        }

        public Function<Session, Object> buyGoods(String sellId, String buyId, Integer amount, Integer price) throws JDBCException {
            return session -> {
                PlayerBean sellPlayer = session.get(PlayerBean.class, sellId);
                PlayerBean buyPlayer = session.get(PlayerBean.class, buyId);

                if (buyPlayer == null || sellPlayer == null) {
                    throw new NotEnoughException("sell or buy player not exist");
                }

                if (buyPlayer.getCoins() < price || sellPlayer.getGoods() < amount) {
                    throw new NotEnoughException("coins or goods not enough, rollback");
                }

                buyPlayer.setGoods(buyPlayer.getGoods() + amount);
                buyPlayer.setCoins(buyPlayer.getCoins() - price);
                session.persist(buyPlayer);

                sellPlayer.setGoods(sellPlayer.getGoods() - amount);
                sellPlayer.setCoins(sellPlayer.getCoins() + price);
                session.persist(sellPlayer);

                System.out.printf("APP: buyGoods --> sell: %s, buy: %s, amount: %d, price: %d\n", sellId, buyId, amount, price);
                return 0;
            };
        }

        public Function<Session, Object> getPlayerByID(String id) throws JDBCException {
            return session -> session.get(PlayerBean.class, id);
        }

        public Function<Session, Object> printPlayers(Integer limit) throws JDBCException {
            return session -> {
                NativeQuery<PlayerBean> limitQuery = session.createNativeQuery("SELECT * FROM player_hibernate LIMIT :limit", PlayerBean.class);
                limitQuery.setParameter("limit", limit);
                List<PlayerBean> players = limitQuery.getResultList();

                for (PlayerBean player: players) {
                    System.out.println("\n[printPlayers]:\n" + player);
                }
                return 0;
            };
        }

        public Function<Session, Object> countPlayers() throws JDBCException {
            return session -> {
                Query<Long> countQuery = session.createQuery("SELECT count(player_hibernate) FROM PlayerBean player_hibernate", Long.class);
                return countQuery.getSingleResult();
            };
        }
    }

    public static void main(String[] args) {
        // 1. Create a SessionFactory based on our hibernate.cfg.xml configuration
        // file, which defines how to connect to the database.
        SessionFactory sessionFactory
                = new Configuration()
                .configure("hibernate.cfg.xml")
                .addAnnotatedClass(PlayerBean.class)
                .buildSessionFactory();

        try (Session session = sessionFactory.openSession()) {
            // 2. And then, create DAO to manager your data.
            PlayerDAO playerDAO = new PlayerDAO();

            // 3. Run some simple examples.

            // Create a player who has 1 coin and 1 goods.
            playerDAO.runTransaction(session, playerDAO.createPlayers(Collections.singletonList(
                    new PlayerBean("test", 1, 1))));

            // Get a player.
            PlayerBean testPlayer = (PlayerBean)playerDAO.runTransaction(session, playerDAO.getPlayerByID("test"));
            System.out.printf("PlayerDAO.getPlayer:\n    => id: %s\n    => coins: %s\n    => goods: %s\n",
                    testPlayer.getId(), testPlayer.getCoins(), testPlayer.getGoods());

            // Count players amount.
            Long count = (Long)playerDAO.runTransaction(session, playerDAO.countPlayers());
            System.out.printf("PlayerDAO.countPlayers:\n    => %d total players\n", count);

            // Print 3 players.
            playerDAO.runTransaction(session, playerDAO.printPlayers(3));

            // 4. Explore more.

            // Player 1: id is "1", has only 100 coins.
            // Player 2: id is "2", has 114514 coins, and 20 goods.
            PlayerBean player1 = new PlayerBean("1", 100, 0);
            PlayerBean player2 = new PlayerBean("2", 114514, 20);

            // Create two players "by hand", using the INSERT statement on the backend.
            int addedCount = (Integer)playerDAO.runTransaction(session,
                    playerDAO.createPlayers(Arrays.asList(player1, player2)));
            System.out.printf("PlayerDAO.createPlayers:\n    => %d total inserted players\n", addedCount);

            // Player 1 wants to buy 10 goods from player 2.
            // It will cost 500 coins, but player 1 cannot afford it.
            System.out.println("\nPlayerDAO.buyGoods:\n    => this trade will fail");
            Integer updatedCount = (Integer)playerDAO.runTransaction(session,
                    playerDAO.buyGoods(player2.getId(), player1.getId(), 10, 500));
            System.out.printf("PlayerDAO.buyGoods:\n    => %d total update players\n", updatedCount);

            // So player 1 has to reduce the incoming quantity to two.
            System.out.println("\nPlayerDAO.buyGoods:\n    => this trade will success");
            updatedCount = (Integer)playerDAO.runTransaction(session,
                    playerDAO.buyGoods(player2.getId(), player1.getId(), 2, 100));
            System.out.printf("PlayerDAO.buyGoods:\n    => %d total update players\n", updatedCount);
        } finally {
            sessionFactory.close();
        }
    }
}
```

</div>

</SimpleTab>

## 第 3 步：运行代码

本节将逐步介绍代码的运行方法。

### 第 3 步第 1 部分：JDBC 表初始化

<SimpleTab>

<div label="使用 JDBC" href="jdbc-table-init-jdbc">

> 在 Gitpod Playground 中尝试 JDBC: [现在就试试](https://gitpod.io/#targetMode=plain-java-jdbc/https://github.com/pingcap-inc/tidb-example-java)

使用 JDBC 时，需手动初始化数据库表，若你本地已经安装了 `mysql-client`，且使用本地集群，可直接在 `plain-java-jdbc` 目录下运行：

{{< copyable "shell-regular" >}}

```shell
make mysql
```

或直接执行：

{{< copyable "shell-regular" >}}

```shell
mysql --host 127.0.0.1 --port 4000 -u root<src/main/resources/dbinit.sql
```

若你不使用本地集群，或未安装 **mysql-client**，请直接登录你的集群，并运行 `src/main/resources/dbinit.sql` 文件内的 SQL 语句。

</div>

<div label="使用 Mybatis（推荐）" href="jdbc-table-init-mybatis">

> 在 Gitpod Playground 中尝试 JDBC：[现在就试试](https://gitpod.io/#targetMode=plain-java-mybatis/https://github.com/pingcap-inc/tidb-example-java)

使用 JDBC 时，需手动初始化数据库表。若你本地已经安装了 `mysql-client`，且使用本地集群，可直接在 `plain-java-mybatis` 目录下通过 `make prepare` 运行：

{{< copyable "shell-regular" >}}

```shell
make prepare
```

或直接执行：

{{< copyable "shell-regular" >}}

```shell
mysql --host 127.0.0.1 --port 4000 -u root < src/main/resources/dbinit.sql
```

若你不使用本地集群，或未安装 `mysql-client`，请直接登录你的集群，并运行 `src/main/resources/dbinit.sql` 文件内的 SQL 语句。

</div>

<div label="使用 Hibernate（推荐）" href="jdbc-table-init-hibernate">

> 在 Gitpod Playground 中尝试 Hibernate: [现在就试试](https://gitpod.io/#targetMode=plain-java-jdbc/https://github.com/pingcap-inc/tidb-example-java)

无需手动初始化表。

</div>

</SimpleTab>

### 第 3 步第 2 部分：TiDB Cloud 更改参数

<SimpleTab>

<div label="使用 JDBC" href="tidb-cloud-jdbc">

若你使用非本地默认集群、TiDB Cloud 或其他远程集群，更改 `JDBCExample.java` 内关于 Host、Port、User、Password 的参数：

{{< copyable "" >}}

```java
mysqlDataSource.setServerName("localhost");
mysqlDataSource.setPortNumber(4000);
mysqlDataSource.setDatabaseName("test");
mysqlDataSource.setUser("root");
mysqlDataSource.setPassword("");
```

若你设定的密码为 `123456`，而且从 TiDB Cloud 得到的连接字符串为：

```
mysql --connect-timeout 15 -u root -h xxx.tidbcloud.com -P 4000 -p
```

那么此处应将参数更改为：

{{< copyable "" >}}

```java
mysqlDataSource.setServerName("xxx.tidbcloud.com");
mysqlDataSource.setPortNumber(4000);
mysqlDataSource.setDatabaseName("test");
mysqlDataSource.setUser("root");
mysqlDataSource.setPassword("123456");
```

</div>

<div label="使用 Mybatis（推荐）" href="tidb-cloud-mybatis">

若你使用非本地默认集群、TiDB Cloud 或其他远程集群，更改 `mybatis-config.xml` 内关于 `dataSource.url`、`dataSource.username`、`dataSource.password` 的参数：

{{< copyable "" >}}

```xml
<?xml version="1.0" encoding="UTF-8" ?>

<!DOCTYPE configuration
        PUBLIC "-//mybatis.org//DTD Config 3.0//EN"
        "http://mybatis.org/dtd/mybatis-3-config.dtd">

<configuration>
    <settings>
        <setting name="cacheEnabled" value="true"/>
        <setting name="lazyLoadingEnabled" value="false"/>
        <setting name="aggressiveLazyLoading" value="true"/>
        <setting name="logImpl" value="LOG4J"/>
    </settings>

    <typeAliases>
        <package name="com.pingcap.dao"/>
    </typeAliases>

    <environments default="development">
        <environment id="development">
            <!-- JDBC transaction manager -->
            <transactionManager type="JDBC"/>
            <!-- Database pool -->
            <dataSource type="POOLED">
                <property name="driver" value="com.mysql.jdbc.Driver"/>
                <property name="url" value="jdbc:mysql://127.0.0.1:4000/test"/>
                <property name="username" value="root"/>
                <property name="password" value=""/>
            </dataSource>
        </environment>
    </environments>

    <mappers>
        <mapper resource="mapper/PlayerMapper.xml"/>
        <mapper resource="mapper/PlayerMapperEx.xml"/>
    </mappers>

</configuration>
```

若你设定的密码为 `123456`，而且从 TiDB Cloud 得到的连接字符串为：

```
mysql --connect-timeout 15 -u root -h xxx.tidbcloud.com -P 4000 -p
```

那么此处应将配置文件中 `dataSource` 节点内更改为：

{{< copyable "" >}}

```xml
<?xml version="1.0" encoding="UTF-8" ?>

<!DOCTYPE configuration
        PUBLIC "-//mybatis.org//DTD Config 3.0//EN"
        "http://mybatis.org/dtd/mybatis-3-config.dtd">

        ...
            <!-- Database pool -->
            <dataSource type="POOLED">
                <property name="driver" value="com.mysql.jdbc.Driver"/>
                <property name="url" value="jdbc:mysql://xxx.tidbcloud.com:4000/test"/>
                <property name="username" value="root"/>
                <property name="password" value="123456"/>
            </dataSource>
        ...

</configuration>
```

</div>

<div label="使用 Hibernate（推荐）" href="tidb-cloud-hibernate">

若你使用非本地默认集群、TiDB Cloud 或其他远程集群，更改 `hibernate.cfg.xml` 内关于 hibernate.connection.url、hibernate.connection.username、hibernate.connection.password 的参数：

{{< copyable "" >}}

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
        <property name="hibernate.connection.url">jdbc:mysql://localhost:4000/test</property>
        <property name="hibernate.connection.username">root</property>
        <property name="hibernate.connection.password"></property>
        <property name="hibernate.connection.autocommit">false</property>

        <!-- Required so a table can be created from the 'PlayerDAO' class -->
        <property name="hibernate.hbm2ddl.auto">create-drop</property>

        <!-- Optional: Show SQL output for debugging -->
        <property name="hibernate.show_sql">true</property>
        <property name="hibernate.format_sql">true</property>
    </session-factory>
</hibernate-configuration>
```

若你设定的密码为 `123456`，而且从 TiDB Cloud 得到的连接字符串为：

```
mysql --connect-timeout 15 -u root -h xxx.tidbcloud.com -P 4000 -p
```

那么此处应将配置文件更改为：

{{< copyable "" >}}

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
        <property name="hibernate.connection.url">jdbc:mysql://xxx.tidbcloud.com:4000/test</property>
        <property name="hibernate.connection.username">root</property>
        <property name="hibernate.connection.password">123456</property>
        <property name="hibernate.connection.autocommit">false</property>

        <!-- Required so a table can be created from the 'PlayerDAO' class -->
        <property name="hibernate.hbm2ddl.auto">create-drop</property>

        <!-- Optional: Show SQL output for debugging -->
        <property name="hibernate.show_sql">true</property>
        <property name="hibernate.format_sql">true</property>
    </session-factory>
</hibernate-configuration>
```

</div>

</SimpleTab>

### 第 3 步第 3 部分：运行

<SimpleTab>

<div label="使用 JDBC" href="run-jdbc">

运行 `make`，这是以下两个操作的组合：

- 清理并构建 (make build)： `mvn clean package`
- 运行 (make run)： `java -jar target/plain-java-jdbc-0.0.1-jar-with-dependencies.jar`

你也可以单独运行这两个 make 命令或原生命令。

</div>

<div label="使用 Mybatis（推荐）" href="run-mybatis">

运行 `make`，这是以下四个操作的组合：

- 创建表 (`make prepare`)：

    {{< copyable "shell-regular" >}}

    ```shell
    mysql --host 127.0.0.1 --port 4000 -u root < src/main/resources/dbinit.sql
    mysql --host 127.0.0.1 --port 4000 -u root -e "TRUNCATE test.player"
    ```

- 清理并构建 (`make gen`)：

    {{< copyable "shell-regular" >}}

    ```shell
    rm -f src/main/java/com/pingcap/model/Player.java
    rm -f src/main/java/com/pingcap/model/PlayerMapper.java
    rm -f src/main/resources/mapper/PlayerMapper.xml
    mvn mybatis-generator:generate
    ```

- 清理并构建 (`make build`)：`mvn clean package`
- 运行 (`make run`)：`java -jar target/plain-java-mybatis-0.0.1-jar-with-dependencies.jar`

你也可以单独运行这四个 `make` 命令或原生命令。

</div>

<div label="使用 Hibernate（推荐）" href="run-hibernate">

运行 `make`，这是以下两个操作的组合：

- 清理并构建 (make build)：`mvn clean package`
- 运行 (make run)：`java -jar target/plain-java-hibernate-0.0.1-jar-with-dependencies.jar`

你也可以单独运行这两个 make 命令或原生命令。

</div>

</SimpleTab>

## 第 4 步：预期输出

<SimpleTab>

<div label="使用 JDBC" href="output-jdbc">

[JDBC 预期输出](https://github.com/pingcap-inc/tidb-example-java/blob/main/Expected-Output.md#plain-java-jdbc)

</div>

<div label="使用 Hibernate（推荐）" href="output-hibernate">

[Hibernate 预期输出](https://github.com/pingcap-inc/tidb-example-java/blob/main/Expected-Output.md#plain-java-hibernate)

</div>

</SimpleTab>
