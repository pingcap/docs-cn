---
title: 插入数据
summary: 插入数据、批量导入数据的方法、最佳实践及例子。
aliases: ['/zh/tidb/dev/insert-data']
---

<!-- markdownlint-disable MD029 -->

# 插入数据

此页面将展示使用 SQL 语言，配合各种编程语言将数据插入到 TiDB 中。

## 在开始之前

在阅读本页面之前，你需要准备以下事项：

- [使用 TiDB Serverless 构建 TiDB 集群](/develop/dev-guide-build-cluster-in-cloud.md)。
- 阅读[数据库模式概览](/develop/dev-guide-schema-design-overview.md)，并[创建数据库](/develop/dev-guide-create-database.md)、[创建表](/develop/dev-guide-create-table.md)、[创建二级索引](/develop/dev-guide-create-secondary-indexes.md)。

## 插入行

假设你需要插入多行数据，那么会有两种插入的办法，假设需要插入 3 个玩家数据：

- 一个**多行插入语句**：

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

一般来说使用一个`多行插入语句`，会比多个`单行插入语句`快。

<SimpleTab>
<div label="SQL">

在 SQL 中插入多行数据的示例：

```sql
CREATE TABLE `player` (`id` INT, `coins` INT, `goods` INT);
INSERT INTO `player` (`id`, `coins`, `goods`) VALUES (1, 1000, 1), (2, 230, 2);
```

有关如何使用此 SQL，可查阅[连接到 TiDB 集群](/develop/dev-guide-build-cluster-in-cloud.md#第-2-步连接到集群)文档部分，按文档步骤使用客户端连接到 TiDB 集群后，输入 SQL 语句即可。

</div>

<div label="Java">

在 Java 中插入多行数据的示例：

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

另外，由于 MySQL JDBC Driver 默认设置问题，你需更改部分参数，以获得更好的批量插入性能：

|            参数            |                 作用                  |                                                                     推荐场景                                                                      |         推荐配置         |
| :------------------------: | :-----------------------------------: | :-----------------------------------------------------------------------------------------------------------------------------------------------: | :----------------------: |
|    `useServerPrepStmts`    |   是否使用服务端开启预处理语句支持    |                                                            在需要多次使用预处理语句时                                                             |          `true`          |
|      `cachePrepStmts`      |       客户端是否缓存预处理语句        |                                                           `useServerPrepStmts=true` 时                                                            |          `true`          |
|  `prepStmtCacheSqlLimit`   |  预处理语句最大大小（默认 256 字符）  |                                                             预处理语句大于 256 字符时                                                             | 按实际预处理语句大小配置 |
|    `prepStmtCacheSize`     | 预处理语句最大缓存数量 （默认 25 条） |                                                            预处理语句数量大于 25 条时                                                             | 按实际预处理语句数量配置 |
| `rewriteBatchedStatements` |          是否重写 Batch 语句          |                                                                  需要批量操作时                                                                   |          `true`          |
|    `allowMultiQueries`     |             开启批量操作              | 因为一个[客户端 Bug](https://bugs.mysql.com/bug.php?id=96623) 在 `rewriteBatchedStatements = true` 和 `useServerPrepStmts = true` 时，需设置此项 |          `true`          |

MySQL JDBC Driver 还提供了一个集成配置项：`useConfigs`。当它配置为 `maxPerformance` 时，相当于配置了一组配置，以 `mysql:mysql-connector-java:8.0.28` 为例，`useConfigs=maxPerformance` 包含：

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

你可以自行查看 `mysql-connector-java-{version}.jar!/com/mysql/cj/configurations/maxPerformance.properties` 来获得对应版本 MySQL JDBC Driver 的 `useConfigs=maxPerformance` 包含配置。

在此处给出一个较为的通用场景的 JDBC 连接字符串配置，以 Host: `127.0.0.1`，Port: `4000`，用户名: `root`，密码: 空，默认数据库: `test`为例：

```
jdbc:mysql://127.0.0.1:4000/test?user=root&useConfigs=maxPerformance&useServerPrepStmts=true&prepStmtCacheSqlLimit=2048&prepStmtCacheSize=256&rewriteBatchedStatements=true&allowMultiQueries=true
```

有关 Java 的完整示例，可参阅：

- [TiDB 和 JDBC 的简单 CRUD 应用程序](/develop/dev-guide-sample-application-java-jdbc.md)
- [TiDB 和 Hibernate 的简单 CRUD 应用程序](/develop/dev-guide-sample-application-java-hibernate.md)
- [使用 Spring Boot 构建 TiDB 应用程序](/develop/dev-guide-sample-application-java-spring-boot.md)

</div>

<div label="Golang">

在 Golang 中插入多行数据的示例：

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

有关 Golang 的完整示例，可参阅：

- [使用 Go-MySQL-Driver 连接到 TiDB](/develop/dev-guide-sample-application-golang-sql-driver.md)
- [使用 GORM 连接到 TiDB](/develop/dev-guide-sample-application-golang-gorm.md)

</div>

<div label="Python">

在 Python 中插入多行数据的示例：

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

有关 Python 的完整示例，可参阅：

- [使用 PyMySQL 连接到 TiDB](/develop/dev-guide-sample-application-python-pymysql.md)
- [使用 mysqlclient 连接到 TiDB](/develop/dev-guide-sample-application-python-mysqlclient.md)
- [使用 MySQL Connector/Python 连接到 TiDB](/develop/dev-guide-sample-application-python-mysql-connector.md)
- [使用 SQLAlchemy 连接到 TiDB](/develop/dev-guide-sample-application-python-sqlalchemy.md)
- [使用 Django 连接到 TiDB](/develop/dev-guide-sample-application-python-django.md)
- [使用 peewee 连接到 TiDB](/develop/dev-guide-sample-application-python-peewee.md)

</div>

</SimpleTab>

## 批量插入

如果你需要快速地将大量数据导入 TiDB 集群，最好的方式并不是使用 `INSERT` 语句，这并不是最高效的方法，而且需要你自行处理异常等问题。推荐使用 PingCAP 提供的一系列工具进行数据迁移：

- 数据导出工具：[Dumpling](/dumpling-overview.md)。可以导出 MySQL 或 TiDB 的数据到本地或 Amazon S3 中。
- 数据导入工具：[TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)。可以导入 `Dumpling` 导出的数据、CSV 文件，或者 [Amazon Aurora 生成的 Apache Parquet 文件](/migrate-aurora-to-tidb.md)。同时支持在本地盘或 Amazon S3 云盘读取数据。
- 数据同步工具：[TiDB Data Migration](/dm/dm-overview.md)。可同步 MySQL、MariaDB、Amazon Aurora 数据库到 TiDB 中。且支持分库分表数据库的迁移。
- 数据备份恢复工具：[Backup & Restore (BR)](/br/backup-and-restore-overview.md)。相对于 `Dumpling`，BR 更适合**_大数据量_**的场景。

## 避免热点

在设计表时需要考虑是否存在大量插入行为，若有，需在表设计期间对热点进行规避。请查看[创建表 - 选择主键](/develop/dev-guide-create-table.md#选择主键)部分，并遵从[选择主键时应遵守的规则](/develop/dev-guide-create-table.md#选择主键时应遵守的规则)。

更多有关热点问题的处理办法，请参考 [TiDB 热点问题处理](/troubleshoot-hot-spot-issues.md)文档。

## 主键为 `AUTO_RANDOM` 表插入数据

在插入的表主键为 `AUTO_RANDOM` 时，这时默认情况下，不能指定主键。例如 [bookshop](/develop/dev-guide-bookshop-schema-design.md) 数据库中，可以看到 [users 表](/develop/dev-guide-bookshop-schema-design.md#users-表) 的 `id` 字段含有 `AUTO_RANDOM` 属性。

此时，不可使用类似以下 SQL 进行插入：

```sql
INSERT INTO `bookshop`.`users` (`id`, `balance`, `nickname`) VALUES (1, 0.00, 'nicky');
```

将会产生错误：

```
ERROR 8216 (HY000): Invalid auto random: Explicit insertion on auto_random column is disabled. Try to set @@allow_auto_random_explicit_insert = true.
```

这是旨在提示你，不建议在插入时手动指定 `AUTO_RANDOM` 的列。这时，你有两种解决办法处理此错误：

- (推荐) 插入语句中去除此列，使用 TiDB 帮你初始化的 `AUTO_RANDOM` 值。这样符合 `AUTO_RANDOM` 的语义。

    {{< copyable "sql" >}}

    ```sql
    INSERT INTO `bookshop`.`users` (`balance`, `nickname`) VALUES (0.00, 'nicky');
    ```

- 如果你确认一定需要指定此列，那么可以使用 [SET 语句](/sql-statements/sql-statement-set-variable.md)通过更改用户变量的方式，允许在插入时，指定 `AUTO_RANDOM` 的列。

    {{< copyable "sql" >}}

    ```sql
    SET @@allow_auto_random_explicit_insert = true;
    INSERT INTO `bookshop`.`users` (`id`, `balance`, `nickname`) VALUES (1, 0.00, 'nicky');
    ```

## 使用 HTAP

在 TiDB 中，使用 HTAP 能力无需你在插入数据时进行额外操作。不会有任何额外的插入逻辑，由 TiDB 自动进行数据的一致性保证。你只需要在创建表后，[开启列存副本同步](/develop/dev-guide-create-table.md#使用-htap-能力)，就可以直接使用列存副本来加速你的查询。
