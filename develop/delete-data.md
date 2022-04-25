---
title: 删除数据
---

# 删除数据

此页面将使用 [DELETE](https://docs.pingcap.com/zh/tidb/stable/sql-statement-delete) SQL 语句，对 TiDB 中的数据进行删除。

## 在开始之前

在阅读本页面之前，你需要准备以下事项：

- [使用 TiDB Cloud(DevTier) 构建 TiDB 集群](/develop/build-cluster-in-cloud.md)
- 阅读[数据库模式概览](/develop/schema-design-overview.md)，并[创建数据库](/develop/create-database.md)、[创建表](/develop/create-table.md)、[创建二级索引](/develop/create-secondary-indexes.md)
- 需先[插入数据](/develop/insert-data.md)才可删除

## SQL 语法

在 SQL 中，`DELETE` 语句一般为以下形式：

```sql
DELETE FROM {table} WHERE {filter}
```

|    参数    |      描述      |
| :--------: | :------------: |
| `{table}`  |      表名      |
| `{filter}` | 过滤器匹配条件 |

此处仅展示 `DELETE` 的简单用法，详细文档可参考 TiDB 的 [DELETE 语法页](https://docs.pingcap.com/zh/tidb/stable/sql-statement-delete)。

## 最佳实践

以下是删除行时需要遵循的一些最佳实践：

- 始终在删除语句中指定 `WHERE` 子句。如果 `UPDATE` 没有 `WHERE` 子句，TiDB 将删除这个表内的**_所有行_**。
- 需要删除大量行(数万或更多)的时候，使用[批量删除](#批量删除)，这是因为 TiDB 单个事务大小限制为 [txn-total-size-limit](https://docs.pingcap.com/zh/tidb/stable/tidb-configuration-file#txn-total-size-limit)（默认为 100MB）。
- 如果您需要删除表内的所有数据，请勿使用 `DELETE` 语句，而应该使用 [TRUNCATE](https://docs.pingcap.com/zh/tidb/stable/sql-statement-truncate) 语句。
- 查看 [性能注意事项](#性能注意事项)

## 例子

假设我们发现在特定时间段内，发生了业务错误，需要删除这期间内的所有 [rating](/develop/bookshop-schema-design.md#ratings-表) 的数据，例如，`2022-04-15 00:00:00` 至 `2022-04-15 00:15:00` 的数据。此时，可使用 `SELECT` 语句查看需删除的数据条数：

```sql
SELECT COUNT(*) FROM `rating` WHERE `rating_at` >= "2022-04-15 00:00:00" AND  `rating_at` <= "2022-04-15 00:15:00";
```

- 若返回条数大于 1 万，请查看并使用使用[批量删除](#批量删除)。
- 若返回条数小于 1 万，可使用此处的示例进行删除：

<SimpleTab>
<div label="SQL">

```sql
DELETE FROM `rating` WHERE `rating_at` >= "2022-04-15 00:00:00" AND  `rating_at` <= "2022-04-15 00:15:00";
```

</div>

<div label="Java">

```java
// ds is an entity of com.mysql.cj.jdbc.MysqlDataSource

try (Connection connection = ds.getConnection()) {
    PreparedStatement pstmt = connection.prepareStatement("DELETE FROM `rating` WHERE `rating_at` >= ? AND  `rating_at` <= ?");
    Calendar calendar = Calendar.getInstance();
    calendar.set(Calendar.MILLISECOND, 0);

    calendar.set(2022, Calendar.APRIL, 15, 0, 0, 0);
    pstmt.setTimestamp(1, new Timestamp(calendar.getTimeInMillis()));

    calendar.set(2022, Calendar.APRIL, 15, 0, 15, 0);
    pstmt.setTimestamp(2, new Timestamp(calendar.getTimeInMillis()));
} catch (SQLException e) {
    e.printStackTrace();
}
```

</div>
</SimpleTab>

> Note:
>
> 此处需注意，`rating_at` 字段为[日期和时间类型](https://docs.pingcap.com/zh/tidb/stable/data-type-date-and-time) 中的 `DATETIME` 类型，你可以认为它在 TiDB 保存时，存储为一个字面量，与时区无关。而 `TIMESTAMP` 类型，将会保存一个时间戳，从而在不同的[时区配置](https://docs.pingcap.com/zh/tidb/dev/configure-time-zone)时，展示不同的时间字符串。
>
> 另外，和 MySQL 一样，`TIMESTAMP` 数据类型受 [2038 年问题](https://zh.wikipedia.org/wiki/2038%E5%B9%B4%E9%97%AE%E9%A2%98)的影响。如果存储的值大于 2038，建议使用 `DATETIME` 类型。

## 性能注意事项

### TiDB GC 机制

`DELETE` 语句运行之后 TiDB 并非立刻删除数据，而是将这些数据标记为可删除。然后等待 TiDB GC (Garbage Collection) 来清理不再需要的旧数据。因此，您的 `DELETE` 语句**_并不会_**立即减少磁盘用量。

GC 在默认配置中，为 10 分钟触发一次，每次 GC 都会计算出一个名为 `safe_point` 的时间点，这个时间点前的数据，都不会再被使用到，因此，TiDB 可以安全的对数据进行清除。

GC 的具体实现方案和细节此处不再展开，您可阅读 [GC 机制简介](https://docs.pingcap.com/zh/tidb/stable/garbage-collection-overview) 来获得更详细的 GC 说明。

### 更新统计信息

TiDB 使用[统计信息](https://docs.pingcap.com/zh/tidb/stable/statistics)来决定索引的选择，因此，在大批量的数据删除之后，很有可能会导致索引选择不准确的情况发生。您可以使用[手动收集](https://docs.pingcap.com/zh/tidb/stable/statistics#%E6%89%8B%E5%8A%A8%E6%94%B6%E9%9B%86)的办法，更新统计信息。用以给 TiDB 优化器以更准确的统计信息来提供 SQL 性能优化。

## 批量删除

需要删除表中多行的数据，可选择 [`DELETE` 示例](#例子)，并使用 `WHERE` 子句过滤需要删除的数据。

但如果你需要删除大量行(数万或更多)的时候，我们建议使用一个迭代，每次都只删除一部分数据，直到删除全部完成。这是因为 TiDB 单个事务大小限制为 [txn-total-size-limit](https://docs.pingcap.com/zh/tidb/stable/tidb-configuration-file#txn-total-size-limit)（默认为 100MB）。您可以在程序或脚本中使用循环来完成操作。

本页提供了编写脚本来处理循环删除的示例，该示例演示了应如何进行 `SELECT` 和 `DELETE` 的组合，完成循环删除。

### 编写批量删除循环

首先，您应在您的应用或脚本的循环中，编写一个 `SELECT` 查询。这个查询的返回值可以作为需要删除的行的主键。需要注意的是，定义这个 `SELECT` 查询时，需要注意使用 `WHERE` 子句过滤需要删除的行。

### 批量删除例子

假设我们发现在特定时间段内，发生了业务错误，需要删除这期间内的所有 [rating](/develop/bookshop-schema-design.md#ratings-表) 的数据，例如，`2022-04-15 00:00:00` 至 `2022-04-15 00:15:00` 的数据。并且在 15 分钟内，有大于 1 万条数据被写入，我们应该是用循环删除的方式进行删除：

<SimpleTab>
<div label="SQL"></div>
<div label="Java">

```java
package com.pingcap.bulkDelete;

import com.mysql.cj.jdbc.MysqlDataSource;

import java.sql.*;
import java.util.*;
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

        while (true) {
            batchDelete(mysqlDataSource);
            TimeUnit.SECONDS.sleep(1);
        }
    }

    public static void batchDelete (MysqlDataSource ds) {
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
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
}
```

每次迭代中，`SELECT` 最多选择 1000 行时间段为`2022-04-15 00:00:00` 至 `2022-04-15 00:15:00` 的数据的主键值。然后进行批量删除。每次循环末尾的 `TimeUnit.SECONDS.sleep(1);` 将使得删除程序暂停 1 秒，防止批量删除程序占用过多的硬件资源。

</div>
</SimpleTab>
