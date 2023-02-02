---
title: Insert Data
summary: Learn about how to insert data.
---

<!-- markdownlint-disable MD029 -->

# Insert Data

This document describes how to insert data into TiDB by using the SQL language with different programming languages.

## Before you start

Before reading this document, you need to prepare the following:

- [Build a TiDB Cluster in TiDB Cloud (Serverless Tier)](/develop/dev-guide-build-cluster-in-cloud.md).
- Read [Schema Design Overview](/develop/dev-guide-schema-design-overview.md), [Create a Database](/develop/dev-guide-create-database.md), [Create a Table](/develop/dev-guide-create-table.md), and [Create Secondary Indexes](/develop/dev-guide-create-secondary-indexes.md)

## Insert rows

There are two ways to insert multiple rows of data. For example, if you need to insert **3** players' data.

- A **multi-line insertion statement**:

    {{< copyable "sql" >}}

    ```sql
    INSERT INTO `player` (`id`, `coins`, `goods`) VALUES (1, 1000, 1), (2, 230, 2), (3, 300, 5);
    ```

- Multiple **single-line insertion statements**:

    {{< copyable "sql" >}}

    ```sql
    INSERT INTO `player` (`id`, `coins`, `goods`) VALUES (1, 1000, 1);
    INSERT INTO `player` (`id`, `coins`, `goods`) VALUES (2, 230, 2);
    INSERT INTO `player` (`id`, `coins`, `goods`) VALUES (3, 300, 5);
    ```

Generally the `multi-line insertion statement` runs faster than the multiple `single-line insertion statements`.

<SimpleTab>
<div label="SQL">

```sql
CREATE TABLE `player` (`id` INT, `coins` INT, `goods` INT);
INSERT INTO `player` (`id`, `coins`, `goods`) VALUES (1, 1000, 1), (2, 230, 2);
```

For more information on how to use this SQL, see [Connecting to a TiDB Cluster](/develop/dev-guide-build-cluster-in-cloud.md#step-2-connect-to-a-cluster) and follow the steps to enter the SQL statement after connecting to a TiDB cluster using a client.

</div>

<div label="Java">

```java
// ds is an entity of com.mysql.cj.jdbc.MysqlDataSource
try (Connection connection = ds.getConnection()) {
    connection.setAutoCommit(false);

    PreparedStatement pstmt = connection.prepareStatement("INSERT INTO player (id, coins, goods) VALUES (?, ?, ?)"))

    // first player
    pstmt.setInt(1, 1);
    pstmt.setInt(2, 1000);
    pstmt.setInt(3, 1);
    pstmt.addBatch();

    // second player
    pstmt.setInt(1, 2);
    pstmt.setInt(2, 230);
    pstmt.setInt(3, 2);
    pstmt.addBatch();

    pstmt.executeBatch();
    connection.commit();
} catch (SQLException e) {
    e.printStackTrace();
}
```

Due to the default MySQL JDBC Driver settings, you need to change some parameters to get better bulk insert performance.

|            Parameter            |                 Means                  |   Recommended Scenario   | Recommended Configuration|
| :------------------------: | :-----------------------------------: | :-----------------------------------------------------------------------------------------------------------------------------------------------: | :----------------------: |
|    `useServerPrepStmts`    |    Whether to use the server side to enable prepared statements    |  When you need to use a prepared statement more than once                                                             |          `true`          |
|      `cachePrepStmts`      |       Whether the client caches prepared statements        |                                                           `useServerPrepStmts=true` 时                                                            |          `true`          |
|  `prepStmtCacheSqlLimit`   |  Maximum size of a prepared statement (256 characters by default)  | When the prepared statement is greater than 256 characters | Configured according to the actual size of the prepared statement |
|    `prepStmtCacheSize`     | Maximum number of prepared statement caches (25 by default) | When the number of prepared statements is greater than 25  | Configured according to the actual number of prepared statements |
| `rewriteBatchedStatements` |          Whether to rewrite **Batched** statements          | When batch operations are required |          `true`          |
|    `allowMultiQueries`     |             Start batch operations              | Because a [client bug](https://bugs.mysql.com/bug.php?id=96623) requires this to be set when `rewriteBatchedStatements = true` and `useServerPrepStmts = true` |          `true`          |

MySQL JDBC Driver also provides an integrated configuration: `useConfigs`. When it is configured with `maxPerformance`, it is equivalent to configuring a set of configurations. Taking `mysql:mysql-connector-java:8.0.28` as an example, `useConfigs=maxPerformance` contains:

```properties
cachePrepStmts=true
cacheCallableStmts=true
cacheServerConfiguration=true
useLocalSessionState=true
elideSetAutoCommits=true
alwaysSendSetIsolation=false
enableQueryTimeouts=false
connectionAttributes=none
useInformationSchema=true
```

You can check `mysql-connector-java-{version}.jar!/com/mysql/cj/configurations/maxPerformance.properties` to get the configurations contained in `useConfigs=maxPerformance` for the corresponding version of MySQL JDBC Driver.

The following is a typical scenario of JDBC connection string configurations. In this example, Host: `127.0.0.1`, Port: `4000`, User name: `root`, Password: null, Default database: `test`:

```
jdbc:mysql://127.0.0.1:4000/test?user=root&useConfigs=maxPerformance&useServerPrepStmts=true&prepStmtCacheSqlLimit=2048&prepStmtCacheSize=256&rewriteBatchedStatements=true&allowMultiQueries=true
```

For a complete example in Java, see:

- [Build a Simple CRUD App with TiDB and Java - Using JDBC](/develop/dev-guide-sample-application-java.md#step-2-get-the-code)
- [Build a Simple CRUD App with TiDB and Java - Using Hibernate](/develop/dev-guide-sample-application-java.md#step-2-get-the-code)
- [Build the TiDB Application using Spring Boot](/develop/dev-guide-sample-application-spring-boot.md)

</div>

<div label="Golang">

```go
package main

import (
    "database/sql"
    "strings"

    _ "github.com/go-sql-driver/mysql"
)

type Player struct {
    ID    string
    Coins int
    Goods int
}

func bulkInsertPlayers(db *sql.DB, players []Player, batchSize int) error {
    tx, err := db.Begin()
    if err != nil {
        return err
    }

    stmt, err := tx.Prepare(buildBulkInsertSQL(batchSize))
    if err != nil {
        return err
    }

    defer stmt.Close()

    for len(players) > batchSize {
        if _, err := stmt.Exec(playerToArgs(players[:batchSize])...); err != nil {
            tx.Rollback()
            return err
        }

        players = players[batchSize:]
    }

    if len(players) != 0 {
        if _, err := tx.Exec(buildBulkInsertSQL(len(players)), playerToArgs(players)...); err != nil {
            tx.Rollback()
            return err
        }
    }

    if err := tx.Commit(); err != nil {
        tx.Rollback()
        return err
    }

    return nil
}

func playerToArgs(players []Player) []interface{} {
    var args []interface{}
    for _, player := range players {
        args = append(args, player.ID, player.Coins, player.Goods)
    }
    return args
}

func buildBulkInsertSQL(amount int) string {
    return "INSERT INTO player (id, coins, goods) VALUES (?, ?, ?)" + strings.Repeat(",(?,?,?)", amount-1)
}
```

For a complete example in Golang, see:

- [Use go-sql-driver/mysql to build a simple CRUD app with TiDB and Golang](/develop/dev-guide-sample-application-golang.md#step-2-get-the-code)
- [Use GORM to build a simple CRUD app with TiDB and Golang](/develop/dev-guide-sample-application-java.md#step-2-get-the-code)

</div>

</SimpleTab>

## Bulk-Insert

If you need to quickly import a large amount of data into a TiDB cluster, it is recommended that you use a range of tools provided by **PingCAP** for data migration. Using the `INSERT` statement is not the best way, because it is not efficient and requires to handle exceptions and other issues on your own.

The following are the recommended tools for bulk-insert:

- Data export: [Dumpling](/dumpling-overview.md). You can export MySQL or TiDB data to local or Amazon S3.

<CustomContent platform="tidb">

- Data import: [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md). You can import **Dumpling** exported data, a **CSV** file, or [Migrate Data from Amazon Aurora to TiDB](/migrate-aurora-to-tidb.md). It also supports reading data from a local disk or Amazon S3 cloud disk.
- Data replication: [TiDB Data Migration](/dm/dm-overview.md). You can replicate MySQL, MariaDB, and Amazon Aurora databases to TiDB. It also supports merging and migrating the sharded instances and tables from the source databases.
- Data backup and restore: [Backup & Restore (BR)](/br/backup-and-restore-overview.md). Compared to **Dumpling**, **BR** is more suitable for **_big data_** scenario.

</CustomContent>

<CustomContent platform="tidb-cloud">

- Data import: [Data Import Task](/tidb-cloud/import-sample-data.md) page in the TiDB Cloud console. You can import **Dumpling** exported data, a **CSV** file, or [Migrate Data from Amazon Aurora to TiDB](/tidb-cloud/migrate-from-aurora-bulk-import.md). It also supports reading data from a local disk, Amazon S3 cloud disk, or GCS cloud disk.
- Data replication: [TiDB Data Migration](https://docs.pingcap.com/tidb/stable/dm-overview). You can replicate MySQL, MariaDB, and Amazon Aurora databases to TiDB. It also supports merging and migrating the sharded instances and tables from the source databases.
- Data backup and restore: [Backup](/tidb-cloud/backup-and-restore.md) page in the TiDB Cloud console. Compared to **Dumpling**, backup and restore is more suitable for **_big data_** scenario.

</CustomContent>

## Avoid hotspots

When designing a table, you need to consider if there is a large number of insert operations. If so, you need to avoid hotspots during table design. See the [Select primary key](/develop/dev-guide-create-table.md#select-primary-key) section and follow the [Rules when selecting primary key](/develop/dev-guide-create-table.md#guidelines-to-follow-when-selecting-primary-key).

<CustomContent platform="tidb">

For more information on how to handle hotspot issues, see [Troubleshoot Hotspot Issues](/troubleshoot-hot-spot-issues.md).

</CustomContent>

## Insert data to a table with the `AUTO_RANDOM` primary key

If the primary key of the table you insert has the `AUTO_RANDOM` attribute, then by default the primary key cannot be specified. For example, in the [`bookshop`](/develop/dev-guide-bookshop-schema-design.md) database, you can see that the `id` field of the [`users` table](/develop/dev-guide-bookshop-schema-design.md#users-table) contains the `AUTO_RANDOM` attribute.

In this case, you **cannot** use SQL like the following to insert:

```sql
INSERT INTO `bookshop`.`users` (`id`, `balance`, `nickname`) VALUES (1, 0.00, 'nicky');
```

An error will occur:

```
ERROR 8216 (HY000): Invalid auto random: Explicit insertion on auto_random column is disabled. Try to set @@allow_auto_random_explicit_insert = true.
```

It is not recommended to manually specify the `AUTO_RANDOM` column during insertion time.

There are two solutions to handle this error:

- (Recommended) Remove this column from the insert statement and use the `AUTO_RANDOM` value that TiDB initialized for you. This fits the semantics of `AUTO_RANDOM`.

    {{< copyable "sql" >}}

    ```sql
    INSERT INTO `bookshop`.`users` (`balance`, `nickname`) VALUES (0.00, 'nicky');
    ```

- If you are sure that you **_must_** specify this column, then you can use the [`SET` statement](https://docs.pingcap.com/zh/tidb/stable/sql-statement-set-variable) to allow the column of `AUTO_RANDOM` to be specified during insertion time by changing the user variable.

    {{< copyable "sql" >}}

    ```sql
    SET @@allow_auto_random_explicit_insert = true;
    INSERT INTO `bookshop`.`users` (`id`, `balance`, `nickname`) VALUES (1, 0.00, 'nicky');
    ```

## Use HTAP

In TiDB, HTAP capabilities save you from performing additional operations when inserting data. There is no additional insertion logic. TiDB automatically guarantees data consistency. All you need to do is [turn on column-oriented replica synchronization](/develop/dev-guide-create-table.md#use-htap-capabilities) after creating the table, and use the column-oriented replica to speed up your queries directly.
