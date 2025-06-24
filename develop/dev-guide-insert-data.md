---
title: 插入数据
summary: 了解如何插入数据。
---

<!-- markdownlint-disable MD029 -->

# 插入数据

本文档介绍如何使用不同编程语言通过 SQL 语言向 TiDB 插入数据。

## 开始之前

在阅读本文档之前，你需要准备以下内容：

- [构建 TiDB Cloud Serverless 集群](/develop/dev-guide-build-cluster-in-cloud.md)。
- 阅读[架构设计概述](/develop/dev-guide-schema-design-overview.md)、[创建数据库](/develop/dev-guide-create-database.md)、[创建表](/develop/dev-guide-create-table.md)和[创建二级索引](/develop/dev-guide-create-secondary-indexes.md)。

## 插入行

有两种方式可以插入多行数据。例如，如果你需要插入 **3** 个玩家的数据。

- **多行插入语句**：

    {{< copyable "sql" >}}

    ```sql
    INSERT INTO `player` (`id`, `coins`, `goods`) VALUES (1, 1000, 1), (2, 230, 2), (3, 300, 5);
    ```

- 多个**单行插入语句**：

    {{< copyable "sql" >}}

    ```sql
    INSERT INTO `player` (`id`, `coins`, `goods`) VALUES (1, 1000, 1);
    INSERT INTO `player` (`id`, `coins`, `goods`) VALUES (2, 230, 2);
    INSERT INTO `player` (`id`, `coins`, `goods`) VALUES (3, 300, 5);
    ```

通常，`多行插入语句`的运行速度比多个`单行插入语句`更快。

<SimpleTab>
<div label="SQL">

```sql
CREATE TABLE `player` (`id` INT, `coins` INT, `goods` INT);
INSERT INTO `player` (`id`, `coins`, `goods`) VALUES (1, 1000, 1), (2, 230, 2);
```

有关如何使用此 SQL 的更多信息，请参阅[连接到 TiDB 集群](/develop/dev-guide-build-cluster-in-cloud.md#step-2-connect-to-a-cluster)，并在使用客户端连接到 TiDB 集群后按照步骤输入 SQL 语句。

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

由于 MySQL JDBC Driver 的默认设置，你需要更改一些参数以获得更好的批量插入性能。

|            参数            |                 含义                  |   推荐场景   | 推荐配置 |
| :------------------------: | :-----------------------------------: | :-----------------------------------------------------------------------------------------------------------------------------------------------: | :----------------------: |
|    `useServerPrepStmts`    |    是否使用服务器端预处理语句    |  当你需要多次使用预处理语句时                                                             |          `true`          |
|      `cachePrepStmts`      |       客户端是否缓存预处理语句        |                                                           `useServerPrepStmts=true`                                                             |          `true`          |
|  `prepStmtCacheSqlLimit`   |  预处理语句的最大大小（默认 256 字符）  | 当预处理语句大于 256 字符时 | 根据预处理语句的实际大小配置 |
|    `prepStmtCacheSize`     | 预处理语句缓存的最大数量（默认 25） | 当预处理语句数量大于 25 时  | 根据预处理语句的实际数量配置 |
| `rewriteBatchedStatements` |          是否重写 **批处理** 语句          | 当需要批处理操作时 |          `true`          |
|    `allowMultiQueries`     |             启用批处理操作              | 由于[客户端 bug](https://bugs.mysql.com/bug.php?id=96623)，当 `rewriteBatchedStatements = true` 且 `useServerPrepStmts = true` 时需要设置此项 |          `true`          |

MySQL JDBC Driver 还提供了一个集成配置：`useConfigs`。当配置为 `maxPerformance` 时，相当于配置了一组配置。以 `mysql:mysql-connector-java:8.0.28` 为例，`useConfigs=maxPerformance` 包含：

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

你可以查看 `mysql-connector-java-{version}.jar!/com/mysql/cj/configurations/maxPerformance.properties` 获取相应版本 MySQL JDBC Driver 中 `useConfigs=maxPerformance` 包含的配置。

以下是 JDBC 连接字符串配置的典型场景。在此示例中，主机：`127.0.0.1`，端口：`4000`，用户名：`root`，密码：null，默认数据库：`test`：

```
jdbc:mysql://127.0.0.1:4000/test?user=root&useConfigs=maxPerformance&useServerPrepStmts=true&prepStmtCacheSqlLimit=2048&prepStmtCacheSize=256&rewriteBatchedStatements=true&allowMultiQueries=true
```

有关 Java 的完整示例，请参阅：

- [使用 JDBC 连接到 TiDB](/develop/dev-guide-sample-application-java-jdbc.md)
- [使用 Hibernate 连接到 TiDB](/develop/dev-guide-sample-application-java-hibernate.md)
- [使用 Spring Boot 连接到 TiDB](/develop/dev-guide-sample-application-java-spring-boot.md)

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

有关 Golang 的完整示例，请参阅：

- [使用 Go-MySQL-Driver 连接到 TiDB](/develop/dev-guide-sample-application-golang-sql-driver.md)
- [使用 GORM 连接到 TiDB](/develop/dev-guide-sample-application-golang-gorm.md)

</div>

<div label="Python">

```python
import MySQLdb
connection = MySQLdb.connect(
    host="127.0.0.1",
    port=4000,
    user="root",
    password="",
    database="bookshop",
    autocommit=True
)

with get_connection(autocommit=True) as connection:
    with connection.cursor() as cur:
        player_list = random_player(1919)
        for idx in range(0, len(player_list), 114):
            cur.executemany("INSERT INTO player (id, coins, goods) VALUES (%s, %s, %s)", player_list[idx:idx + 114])
```

有关 Python 的完整示例，请参阅：

- [使用 PyMySQL 连接到 TiDB](/develop/dev-guide-sample-application-python-pymysql.md)
- [使用 mysqlclient 连接到 TiDB](https://github.com/tidb-samples/tidb-python-mysqlclient-quickstart)
- [使用 MySQL Connector/Python 连接到 TiDB](/develop/dev-guide-sample-application-python-mysql-connector.md)
- [使用 SQLAlchemy 连接到 TiDB](/develop/dev-guide-sample-application-python-sqlalchemy.md)
- [使用 peewee 连接到 TiDB](/develop/dev-guide-sample-application-python-peewee.md)

</div>

</SimpleTab>

## 批量插入

如果你需要快速将大量数据导入到 TiDB 集群中，建议使用 **PingCAP** 提供的一系列数据迁移工具。使用 `INSERT` 语句不是最佳方式，因为它效率不高，并且需要自行处理异常和其他问题。

以下是推荐的批量插入工具：

- 数据导出：[Dumpling](https://docs.pingcap.com/tidb/stable/dumpling-overview)。你可以将 MySQL 或 TiDB 数据导出到本地或 Amazon S3。

<CustomContent platform="tidb">

- 数据导入：[TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)。你可以导入 **Dumpling** 导出的数据、**CSV** 文件或[从 Amazon Aurora 迁移数据到 TiDB](/migrate-aurora-to-tidb.md)。它还支持从本地磁盘或 Amazon S3 云盘读取数据。
- 数据复制：[TiDB Data Migration](/dm/dm-overview.md)。你可以将 MySQL、MariaDB 和 Amazon Aurora 数据库复制到 TiDB。它还支持合并和迁移源数据库中的分片实例和表。
- 数据备份和恢复：[Backup & Restore (BR)](/br/backup-and-restore-overview.md)。与 **Dumpling** 相比，**BR** 更适合**大数据**场景。

</CustomContent>

<CustomContent platform="tidb-cloud">

- 数据导入：[TiDB Cloud 控制台](https://tidbcloud.com/)中的[创建导入](/tidb-cloud/import-sample-data.md)页面。你可以上传本地 CSV 文件（仅限 TiDB Cloud Serverless），并导入存储在云存储中的 **Dumpling** 逻辑转储（架构和数据）、**CSV** 或 **Parquet** 文件。详情请参阅[将 CSV 文件导入到 TiDB Cloud Serverless](/tidb-cloud/import-csv-files-serverless.md)或[将 CSV 文件导入到 TiDB Cloud Dedicated](/tidb-cloud/import-csv-files.md)。
- 数据复制：[TiDB Data Migration](https://docs.pingcap.com/tidb/stable/dm-overview)。你可以将 MySQL、MariaDB 和 Amazon Aurora 数据库复制到 TiDB。它还支持合并和迁移源数据库中的分片实例和表。
- 数据备份和恢复：TiDB Cloud 控制台中的[备份](/tidb-cloud/backup-and-restore.md)页面。与 **Dumpling** 相比，备份和恢复更适合**大数据**场景。

</CustomContent>

## 避免热点

在设计表时，你需要考虑是否有大量的插入操作。如果有，则需要在表设计时避免热点。请参阅[选择主键](/develop/dev-guide-create-table.md#select-primary-key)部分，并遵循[选择主键时的规则](/develop/dev-guide-create-table.md#guidelines-to-follow-when-selecting-primary-key)。

<CustomContent platform="tidb">

有关如何处理热点问题的更多信息，请参阅[热点问题处理](/troubleshoot-hot-spot-issues.md)。

</CustomContent>

## 向带有 `AUTO_RANDOM` 主键的表插入数据

如果要插入的表的主键具有 `AUTO_RANDOM` 属性，则默认情况下不能指定主键。例如，在 [`bookshop`](/develop/dev-guide-bookshop-schema-design.md) 数据库中，你可以看到 [`users` 表](/develop/dev-guide-bookshop-schema-design.md#users-table)的 `id` 字段包含 `AUTO_RANDOM` 属性。

在这种情况下，你**不能**使用如下 SQL 进行插入：

```sql
INSERT INTO `bookshop`.`users` (`id`, `balance`, `nickname`) VALUES (1, 0.00, 'nicky');
```

会出现错误：

```
ERROR 8216 (HY000): Invalid auto random: Explicit insertion on auto_random column is disabled. Try to set @@allow_auto_random_explicit_insert = true.
```

不建议在插入时手动指定 `AUTO_RANDOM` 列。

有两种解决方案来处理这个错误：

- （推荐）从插入语句中删除此列，使用 TiDB 为你初始化的 `AUTO_RANDOM` 值。这符合 `AUTO_RANDOM` 的语义。

    {{< copyable "sql" >}}

    ```sql
    INSERT INTO `bookshop`.`users` (`balance`, `nickname`) VALUES (0.00, 'nicky');
    ```

- 如果你确定**必须**指定此列，则可以使用 [`SET` 语句](https://docs.pingcap.com/tidb/stable/sql-statement-set-variable)通过更改用户变量来允许在插入时指定 `AUTO_RANDOM` 列。

    {{< copyable "sql" >}}

    ```sql
    SET @@allow_auto_random_explicit_insert = true;
    INSERT INTO `bookshop`.`users` (`id`, `balance`, `nickname`) VALUES (1, 0.00, 'nicky');
    ```

## 使用 HTAP

在 TiDB 中，HTAP 功能可以让你在插入数据时无需执行额外操作。没有额外的插入逻辑。TiDB 自动保证数据一致性。你只需要在创建表后[开启列式副本同步](/develop/dev-guide-create-table.md#use-htap-capabilities)，然后直接使用列式副本来加速查询即可。

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上询问社区，或[提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上询问社区，或[提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>
