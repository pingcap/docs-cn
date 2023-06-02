---
title: Build a Simple CRUD App with TiDB and JDBC
summary: Learn how to build a simple CRUD application with TiDB and JDBC.
---

<!-- markdownlint-disable MD024 -->
<!-- markdownlint-disable MD029 -->

# Build a Simple CRUD App with TiDB and JDBC

This document describes how to use TiDB and JDBC to build a simple CRUD application.

> **Note:**
>
> It is recommended to use Java 8 or a later Java version.

## Step 1. Launch your TiDB cluster

<CustomContent platform="tidb">

The following introduces how to start a TiDB cluster.

**Use a TiDB Serverless cluster**

For detailed steps, see [Create a TiDB Serverless cluster](/develop/dev-guide-build-cluster-in-cloud.md#step-1-create-a-tidb-serverless-cluster).

**Use a local cluster**

For detailed steps, see [Deploy a local test cluster](/quick-start-with-tidb.md#deploy-a-local-test-cluster) or [Deploy a TiDB Cluster Using TiUP](/production-deployment-using-tiup.md).

</CustomContent>

<CustomContent platform="tidb-cloud">

See [Create a TiDB Serverless cluster](/develop/dev-guide-build-cluster-in-cloud.md#step-1-create-a-tidb-serverless-cluster).

</CustomContent>

## Step 2. Get the code

```shell
git clone https://github.com/pingcap-inc/tidb-example-java.git
```

Change to the `plain-java-jdbc` directory:

```shell
cd plain-java-jdbc
```

The structure of this directory is as follows:

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

You can find initialization statements for the table creation in `dbinit.sql`:

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

`JDBCExample.java` is the main body of the `plain-java-jdbc`. TiDB is highly compatible with the MySQL protocol, so you need to initialize a MySQL source instance `MysqlDataSource` to connect to TiDB. Then, you can initialize `PlayerDAO` for object management and use it to read, edit, add, and delete data.

`PlayerDAO` is a class used to manage data, in which `DAO` means [Data Access Object](https://en.wikipedia.org/wiki/Data_access_object). The class defines a set of data manipulation methods to provide the ability to write data.

`PlayerBean` is a data entity class that is a mapping for tables. Each property of a `PlayerBean` corresponds to a field in the `player` table.

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

        // 3. Run some simple example.

        // Create a player, has a coin and a goods.
        dao.createPlayers(Collections.singletonList(new PlayerBean("test", 1, 1)));

        // Get a player.
        PlayerBean testPlayer = dao.getPlayer("test");
        System.out.printf("PlayerDAO.getPlayer:\n    => id: %s\n    => coins: %s\n    => goods: %s\n",
                testPlayer.getId(), testPlayer.getCoins(), testPlayer.getGoods());

        // Create players with bulk inserts, insert 1919 players totally, and per batch for 114 players.
        int addedCount = dao.bulkInsertRandomPlayers(1919, 114);
        System.out.printf("PlayerDAO.bulkInsertRandomPlayers:\n    => %d total inserted players\n", addedCount);

        // Count players amount.
        int count = dao.countPlayers();
        System.out.printf("PlayerDAO.countPlayers:\n    => %d total players\n", count);

        // Print 3 players.
        dao.printPlayers(3);

        // 4. Getting further.

        // Player 1: id is "1", has only 100 coins.
        // Player 2: id is "2", has 114514 coins, and 20 goods.
        PlayerBean player1 = new PlayerBean("1", 100, 0);
        PlayerBean player2 = new PlayerBean("2", 114514, 20);

        // Create two players "by hand", using the INSERT statement on the backend.
        addedCount = dao.createPlayers(Arrays.asList(player1, player2));
        System.out.printf("PlayerDAO.createPlayers:\n    => %d total inserted players\n", addedCount);

        // Player 1 wants to buy 10 goods from player 2.
        // It will cost 500 coins, but player 1 can't afford it.
        System.out.println("\nPlayerDAO.buyGoods:\n    => this trade will fail");
        int updatedCount = dao.buyGoods(player2.getId(), player1.getId(), 10, 500);
        System.out.printf("PlayerDAO.buyGoods:\n    => %d total update players\n", updatedCount);

        // So player 1 have to reduce his incoming quantity to two.
        System.out.println("\nPlayerDAO.buyGoods:\n    => this trade will success");
        updatedCount = dao.buyGoods(player2.getId(), player1.getId(), 2, 100);
        System.out.printf("PlayerDAO.buyGoods:\n    => %d total update players\n", updatedCount);
    }
}
```

## Step 3. Run the code

The following content introduces how to run the code step by step.

### Step 3.1 Table initialization

<CustomContent platform="tidb">

When using JDBC, you need to initialize the database tables manually. If you are using a local cluster, and MySQL client has been installed locally, you can run it directly in the `plain-java-jdbc` directory:

```shell
make mysql
```

Or you can execute the following command:

```shell
mysql --host 127.0.0.1 --port 4000 -u root<src/main/resources/dbinit.sql
```

If you are using a non-local cluster or MySQL client has not been installed, connect to your cluster and run the statement in the `src/main/resources/dbinit.sql` file.

</CustomContent>

<CustomContent platform="tidb-cloud">

When using JDBC, you need to connect to your cluster and run the statement in the `src/main/resources/dbinit.sql` file to initialize the database tables manually.

</CustomContent>

### Step 3.2 Modify parameters for TiDB Cloud

If you are using a TiDB Serverless cluster, modify the parameters of the host, port, user, and password in `JDBCExample.java`:

```java
mysqlDataSource.setServerName("localhost");
mysqlDataSource.setPortNumber(4000);
mysqlDataSource.setDatabaseName("test");
mysqlDataSource.setUser("root");
mysqlDataSource.setPassword("");
```

Suppose that the password you set is `123456`, and the connection parameters you get from the cluster details page are the following:

- Endpoint: `xxx.tidbcloud.com`
- Port: `4000`
- User: `2aEp24QWEDLqRFs.root`

In this case, you can modify the parameters as follows:

```java
mysqlDataSource.setServerName("xxx.tidbcloud.com");
mysqlDataSource.setPortNumber(4000);
mysqlDataSource.setDatabaseName("test");
mysqlDataSource.setUser("2aEp24QWEDLqRFs.root");
mysqlDataSource.setPassword("123456");
mysqlDataSource.setSslMode(PropertyDefinitions.SslMode.VERIFY_IDENTITY.name());
mysqlDataSource.setEnabledTLSProtocols("TLSv1.2,TLSv1.3");
```

### Step 3.3 Run

To run the code, you can run `make build` and `make run` respectively:

```shell
make build # this command executes `mvn clean package`
make run # this command executes `java -jar target/plain-java-jdbc-0.0.1-jar-with-dependencies.jar`
```

Or you can use the native commands:

```shell
mvn clean package
java -jar target/plain-java-jdbc-0.0.1-jar-with-dependencies.jar
```

Or run the `make` command directly, which is a combination of `make build` and `make run`.

## Step 4. Expected output

[JDBC Expected Output](https://github.com/pingcap-inc/tidb-example-java/blob/main/Expected-Output.md#plain-java-jdbc)