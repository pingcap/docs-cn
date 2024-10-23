---
title: 删除数据
summary: 删除数据、批量删除数据的方法、最佳实践及例子。
---

# 删除数据

此页面将使用 [DELETE](/sql-statements/sql-statement-delete.md) SQL 语句，对 TiDB 中的数据进行删除。如果需要周期性地删除过期数据，可以考虑使用 TiDB 的 [TTL 功能](/time-to-live.md)。

## 在开始之前

在阅读本页面之前，你需要准备以下事项：

- [使用 TiDB Cloud Serverless 构建 TiDB 集群](/develop/dev-guide-build-cluster-in-cloud.md)。
- 阅读[数据库模式概览](/develop/dev-guide-schema-design-overview.md)，并[创建数据库](/develop/dev-guide-create-database.md)、[创建表](/develop/dev-guide-create-table.md)、[创建二级索引](/develop/dev-guide-create-secondary-indexes.md)。
- 需先[插入数据](/develop/dev-guide-insert-data.md)才可删除。

## SQL 语法

在 SQL 中，`DELETE` 语句一般为以下形式：

```sql
DELETE FROM {table} WHERE {filter}
```

|    参数    |      描述      |
| :--------: | :------------: |
| `{table}`  |      表名      |
| `{filter}` | 过滤器匹配条件 |

此处仅展示 `DELETE` 的简单用法，详细文档可参考 TiDB 的 [DELETE 语法](/sql-statements/sql-statement-delete.md)。

## 最佳实践

以下是删除行时需要遵循的一些最佳实践：

- 始终在删除语句中指定 `WHERE` 子句。如果 `DELETE` 没有 `WHERE` 子句，TiDB 将删除这个表内的**_所有行_**。
- 需要删除大量行(数万或更多)的时候，使用[批量删除](#批量删除)，这是因为 TiDB 单个事务大小限制为 [txn-total-size-limit](/tidb-configuration-file.md#txn-total-size-limit)（默认为 100MB）。
- 如果你需要删除表内的所有数据，请勿使用 `DELETE` 语句，而应该使用 [TRUNCATE](/sql-statements/sql-statement-truncate.md) 语句。
- 查看[性能注意事项](#性能注意事项)。
- 在需要大批量删除数据的场景下，[非事务批量删除](#非事务批量删除)对性能的提升十分明显。但与之相对的，这将丢失删除的事务性，因此**无法**进行回滚，请务必正确进行操作选择。

## 例子

假设在开发中发现在特定时间段内，发生了业务错误，需要删除这期间内的所有 [rating](/develop/dev-guide-bookshop-schema-design.md#ratings-表) 的数据，例如，`2022-04-15 00:00:00` 至 `2022-04-15 00:15:00` 的数据。此时，可使用 `SELECT` 语句查看需删除的数据条数：

```sql
SELECT COUNT(*) FROM `ratings` WHERE `rated_at` >= "2022-04-15 00:00:00" AND  `rated_at` <= "2022-04-15 00:15:00";
```

- 若返回数量大于 1 万条，请参考[批量删除](#批量删除)。
- 若返回数量小于 1 万条，可参考下面的示例进行删除：

<SimpleTab groupId="language">
<div label="SQL" value="sql">

在 SQL 中，删除数据的示例如下：

```sql
DELETE FROM `ratings` WHERE `rated_at` >= "2022-04-15 00:00:00" AND  `rated_at` <= "2022-04-15 00:15:00";
```

</div>

<div label="Java" value="java">

在 Java 中，删除数据的示例如下：

```java
// ds is an entity of com.mysql.cj.jdbc.MysqlDataSource

try (Connection connection = ds.getConnection()) {
    String sql = "DELETE FROM `bookshop`.`ratings` WHERE `rated_at` >= ? AND  `rated_at` <= ?";
    PreparedStatement preparedStatement = connection.prepareStatement(sql);
    Calendar calendar = Calendar.getInstance();
    calendar.set(Calendar.MILLISECOND, 0);

    calendar.set(2022, Calendar.APRIL, 15, 0, 0, 0);
    preparedStatement.setTimestamp(1, new Timestamp(calendar.getTimeInMillis()));

    calendar.set(2022, Calendar.APRIL, 15, 0, 15, 0);
    preparedStatement.setTimestamp(2, new Timestamp(calendar.getTimeInMillis()));

    preparedStatement.executeUpdate();
} catch (SQLException e) {
    e.printStackTrace();
}
```

</div>

<div label="Golang" value="golang">

在 Golang 中，删除数据的示例如下：

```go
package main

import (
    "database/sql"
    "fmt"
    "time"

    _ "github.com/go-sql-driver/mysql"
)

func main() {
    db, err := sql.Open("mysql", "root:@tcp(127.0.0.1:4000)/bookshop")
    if err != nil {
        panic(err)
    }
    defer db.Close()

    startTime := time.Date(2022, 04, 15, 0, 0, 0, 0, time.UTC)
    endTime := time.Date(2022, 04, 15, 0, 15, 0, 0, time.UTC)

    bulkUpdateSql := fmt.Sprintf("DELETE FROM `bookshop`.`ratings` WHERE `rated_at` >= ? AND  `rated_at` <= ?")
    result, err := db.Exec(bulkUpdateSql, startTime, endTime)
    if err != nil {
        panic(err)
    }
    _, err = result.RowsAffected()
    if err != nil {
        panic(err)
    }
}
```

</div>

<div label="Python" value="python">

在 Python 中，删除数据的示例如下：

```python
import MySQLdb
import datetime
import time

connection = MySQLdb.connect(
    host="127.0.0.1",
    port=4000,
    user="root",
    password="",
    database="bookshop",
    autocommit=True
)

with connection:
    with connection.cursor() as cursor:
        start_time = datetime.datetime(2022, 4, 15)
        end_time = datetime.datetime(2022, 4, 15, 0, 15)
        delete_sql = "DELETE FROM `bookshop`.`ratings` WHERE `rated_at` >= %s AND `rated_at` <= %s"
        affect_rows = cursor.execute(delete_sql, (start_time, end_time))
        print(f'delete {affect_rows} data')
```

</div>

</SimpleTab>

> **注意：**
>
> `rated_at` 字段为[日期和时间类型](/data-type-date-and-time.md) 中的 `DATETIME` 类型，你可以认为它在 TiDB 保存时，存储为一个字面量，与时区无关。而 `TIMESTAMP` 类型，将会保存一个时间戳，从而在不同的[时区配置](/configure-time-zone.md)时，展示不同的时间字符串。
>
> 另外，和 MySQL 一样，`TIMESTAMP` 数据类型受 [2038 年问题](https://zh.wikipedia.org/wiki/2038%E5%B9%B4%E9%97%AE%E9%A2%98)的影响。如果存储的值大于 2038，建议使用 `DATETIME` 类型。

## 性能注意事项

### TiDB GC 机制

`DELETE` 语句运行之后 TiDB 并非立刻删除数据，而是将这些数据标记为可删除。然后等待 TiDB GC (Garbage Collection) 来清理不再需要的旧数据。因此，你的 `DELETE` 语句**_并不会_**立即减少磁盘用量。

GC 在默认配置中，为 10 分钟触发一次，每次 GC 都会计算出一个名为 **safe_point** 的时间点，这个时间点前的数据，都不会再被使用到，因此，TiDB 可以安全的对数据进行清除。

GC 的具体实现方案和细节此处不再展开，请参考 [GC 机制简介](/garbage-collection-overview.md) 了解更详细的 GC 说明。

### 更新统计信息

TiDB 使用[常规统计信息](/statistics.md)来决定索引的选择，因此，在大批量的数据删除之后，很有可能会导致索引选择不准确的情况发生。你可以使用[手动收集](/statistics.md#手动收集)的办法，更新统计信息。用以给 TiDB 优化器以更准确的统计信息来提供 SQL 性能优化。

## 批量删除

需要删除表中多行的数据，可选择 [`DELETE` 示例](#例子)，并使用 `WHERE` 子句过滤需要删除的数据。

但如果你需要删除大量行（数万或更多）的时候，建议使用一个迭代，每次都只删除一部分数据，直到删除全部完成。这是因为 TiDB 单个事务大小限制为 [txn-total-size-limit](/tidb-configuration-file.md#txn-total-size-limit)（默认为 100MB）。你可以在程序或脚本中使用循环来完成操作。

本页提供了编写脚本来处理循环删除的示例，该示例演示了应如何进行 `SELECT` 和 `DELETE` 的组合，完成循环删除。

### 编写批量删除循环

在你的应用或脚本的循环中，编写一个 `DELETE` 语句，使用 `WHERE` 子句过滤需要删除的行，并使用 `LIMIT` 限制单次删除的数据条数。

### 批量删除例子

假设发现在特定时间段内，发生了业务错误，需要删除这期间内的所有 [rating](/develop/dev-guide-bookshop-schema-design.md#ratings-表) 的数据，例如，`2022-04-15 00:00:00` 至 `2022-04-15 00:15:00` 的数据。并且在 15 分钟内，有大于 1 万条数据被写入，此时请使用循环删除的方式进行删除：

<SimpleTab groupId="language">
<div label="Java" value="java">

在 Java 中，批量删除程序类似于以下内容：

```java
package com.pingcap.bulkDelete;

import com.mysql.cj.jdbc.MysqlDataSource;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.SQLException;
import java.sql.Timestamp;
import java.util.Calendar;
import java.util.concurrent.TimeUnit;

public class BatchDeleteExample
{
    public static void main(String[] args) throws InterruptedException {
        // Configure the example database connection.

        // Create a mysql data source instance.
        MysqlDataSource mysqlDataSource = new MysqlDataSource();

        // Set server name, port, database name, username and password.
        mysqlDataSource.setServerName("localhost");
        mysqlDataSource.setPortNumber(4000);
        mysqlDataSource.setDatabaseName("bookshop");
        mysqlDataSource.setUser("root");
        mysqlDataSource.setPassword("");

        Integer updateCount = -1;
        while (updateCount != 0) {
            updateCount = batchDelete(mysqlDataSource);
        }
    }

    public static Integer batchDelete (MysqlDataSource ds) {
        try (Connection connection = ds.getConnection()) {
            String sql = "DELETE FROM `bookshop`.`ratings` WHERE `rated_at` >= ? AND  `rated_at` <= ? LIMIT 1000";
            PreparedStatement preparedStatement = connection.prepareStatement(sql);
            Calendar calendar = Calendar.getInstance();
            calendar.set(Calendar.MILLISECOND, 0);

            calendar.set(2022, Calendar.APRIL, 15, 0, 0, 0);
            preparedStatement.setTimestamp(1, new Timestamp(calendar.getTimeInMillis()));

            calendar.set(2022, Calendar.APRIL, 15, 0, 15, 0);
            preparedStatement.setTimestamp(2, new Timestamp(calendar.getTimeInMillis()));

            int count = preparedStatement.executeUpdate();
            System.out.println("delete " + count + " data");

            return count;
        } catch (SQLException e) {
            e.printStackTrace();
        }

        return -1;
    }
}
```

每次迭代中，`DELETE` 最多删除 1000 行时间段为 `2022-04-15 00:00:00` 至 `2022-04-15 00:15:00` 的数据。

</div>

<div label="Golang" value="golang">

在 Golang 中，批量删除程序类似于以下内容：

```go
package main

import (
    "database/sql"
    "fmt"
    "time"

    _ "github.com/go-sql-driver/mysql"
)

func main() {
    db, err := sql.Open("mysql", "root:@tcp(127.0.0.1:4000)/bookshop")
    if err != nil {
        panic(err)
    }
    defer db.Close()

    affectedRows := int64(-1)
    startTime := time.Date(2022, 04, 15, 0, 0, 0, 0, time.UTC)
    endTime := time.Date(2022, 04, 15, 0, 15, 0, 0, time.UTC)

    for affectedRows != 0 {
        affectedRows, err = deleteBatch(db, startTime, endTime)
        if err != nil {
            panic(err)
        }
    }
}

// deleteBatch delete at most 1000 lines per batch
func deleteBatch(db *sql.DB, startTime, endTime time.Time) (int64, error) {
    bulkUpdateSql := fmt.Sprintf("DELETE FROM `bookshop`.`ratings` WHERE `rated_at` >= ? AND  `rated_at` <= ? LIMIT 1000")
    result, err := db.Exec(bulkUpdateSql, startTime, endTime)
    if err != nil {
        return -1, err
    }
    affectedRows, err := result.RowsAffected()
    if err != nil {
        return -1, err
    }

    fmt.Printf("delete %d data\n", affectedRows)
    return affectedRows, nil
}
```

每次迭代中，`DELETE` 最多删除 1000 行时间段为 `2022-04-15 00:00:00` 至 `2022-04-15 00:15:00` 的数据。

</div>

<div label="Python" value="python">

在 Python 中，批量删除程序类似于以下内容：

```python
import MySQLdb
import datetime
import time

connection = MySQLdb.connect(
    host="127.0.0.1",
    port=4000,
    user="root",
    password="",
    database="bookshop",
    autocommit=True
)

with connection:
    with connection.cursor() as cursor:
        start_time = datetime.datetime(2022, 4, 15)
        end_time = datetime.datetime(2022, 4, 15, 0, 15)
        affect_rows = -1
        while affect_rows != 0:
            delete_sql = "DELETE FROM `bookshop`.`ratings` WHERE `rated_at` >= %s AND  `rated_at` <= %s LIMIT 1000"
            affect_rows = cursor.execute(delete_sql, (start_time, end_time))
            print(f'delete {affect_rows} data')
            time.sleep(1)
```

每次迭代中，`DELETE` 最多删除 1000 行时间段为 `2022-04-15 00:00:00` 至 `2022-04-15 00:15:00` 的数据。

</div>

</SimpleTab>

## 非事务批量删除

> **注意：**
>
> TiDB 从 v6.1.0 版本开始支持[非事务 DML 语句](/non-transactional-dml.md)特性。在 TiDB v6.1.0 以下版本中无法使用此特性。

### 使用前提

在使用非事务批量删除前，请先**仔细**阅读[非事务 DML 语句](/non-transactional-dml.md)。非事务批量删除，本质是以牺牲事务的原子性、隔离性为代价，增强批量数据处理场景下的性能和易用性。

因此在使用过程中，需要极为小心，否则，因为操作的非事务特性，在误操作时会导致严重的后果（如数据丢失等）。

### 非事务批量删除 SQL 语法

非事务批量删除的 SQL 语法如下：

```sql
BATCH ON {shard_column} LIMIT {batch_size} {delete_statement};
```

|    参数    |      描述      |
| :--------: | :------------: |
| `{shard_column}`  |      非事务批量删除的划分列      |
| `{batch_size}` | 非事务批量删除的每批大小 |
| `{delete_statement}` | 删除语句 |

此处仅展示非事务批量删除的简单用法，详细文档可参考 TiDB 的[非事务 DML 语句](/non-transactional-dml.md)。

### 非事务批量删除使用示例

以上方[批量删除例子](#批量删除例子)场景为例，可使用以下 SQL 语句进行非事务批量删除：

```sql
BATCH ON `rated_at` LIMIT 1000 DELETE FROM `ratings` WHERE `rated_at` >= "2022-04-15 00:00:00" AND `rated_at` <= "2022-04-15 00:15:00";
```
