---
title: Delete Data
summary: Learn about the SQL syntax, best practices, and examples for deleting data.
---

# Delete Data

This document describes how to use the [DELETE](/sql-statements/sql-statement-delete.md) SQL statement to delete the data in TiDB.

## Before you start

Before reading this document, you need to prepare the following:

- [Build a TiDB Cluster in TiDB Cloud (DevTier)](/develop/dev-guide-build-cluster-in-cloud.md)
- Read [Schema Design Overview](/develop/dev-guide-schema-design-overview.md), [Create a Database](/develop/dev-guide-create-database.md), [Create a Table](/develop/dev-guide-create-table.md), and [Create Secondary Indexes](/develop/dev-guide-create-secondary-indexes.md)
- [Insert Data](/develop/dev-guide-insert-data.md)

## SQL syntax

The `DELETE` statement is generally in the following form:

{{< copyable "sql" >}}

```sql
DELETE FROM {table} WHERE {filter}
```

| Parameter Name | Description |
| :--------: | :------------: |
| `{table}`  |      Table name      |
| `{filter}` | Matching conditions of the filter|

This example only shows a simple use case of `DELETE`. For detailed information, see [DELETE syntax](/sql-statements/sql-statement-delete.md).

## Best practices

The following are some best practices to follow when you delete data:

- Always specify the `WHERE` clause in the `DELETE` statement. If the `WHERE` clause is not specified, TiDB will delete **_ALL ROWS_** in the table.
- Use [bulk-delete](#bulk-delete) when you delete a large number of rows (for example, more than ten thousand), because TiDB limits the size of a single transaction ([txn-total-size-limit](/tidb-configuration-file.md#txn-total-size-limit), 100 MB by default).
- If you delete all the data in a table, do not use the `DELETE` statement. Instead, use the [`TRUNCATE`](/sql-statements/sql-statement-truncate.md) statement.
- For performance considerations, see [Performance Considerations](#performance-considerations).

## Example

Suppose you find an application error within a specific time period and you need to delete all the data for the [rating](/develop/dev-guide-bookshop-schema-design.md#ratings-table) within this period, for example, from `2022-04-15 00:00:00` to `2022-04-15 00:15:00`. In this case, you can use the `SELECT` statement to check the number of records to be deleted.

{{< copyable "sql" >}}

```sql
SELECT COUNT(*) FROM `rating` WHERE `rating_at` >= "2022-04-15 00:00:00" AND  `rating_at` <= "2022-04-15 00:15:00";
```

If more than 10,000 records are returned, use [Bulk-Delete](#bulk-delete) to delete them.

If fewer than 10,000 records are returned, use the following example to delete them.

<SimpleTab>
<div label="SQL" href="delete-sql">

{{< copyable "sql" >}}

```sql
DELETE FROM `rating` WHERE `rating_at` >= "2022-04-15 00:00:00" AND  `rating_at` <= "2022-04-15 00:15:00";
```

</div>

<div label="Java" href="delete-java">

{{< copyable "" >}}

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

> **Note:**
>
> Note that the `rating_at` field is of the `DATETIME` type in [Date and Time Types](/data-type-date-and-time.md). You can assume that it is stored as a literal quantity in TiDB, independent of the time zone. On the other hand, the `TIMESTAMP` type stores a timestamp and thus displays a different time string in a different [time zone](/configure-time-zone.md).
>
> Also, like MySQL, the `TIMESTAMP` data type is affected by the [year 2038 problem](https://en.wikipedia.org/wiki/Year_2038_problem). It is recommended to use the `DATETIME` type if you store values larger than 2038.

## Performance considerations

### TiDB GC mechanism

TiDB does not delete the data immediately after you run the `DELETE` statement. Instead, it marks the data as ready for deletion. Then it waits for TiDB GC (Garbage Collection) to clean up the outdated data. Therefore, the `DELETE` statement **_DOES NOT_** immediately reduce disk usage.

GC is triggered once every 10 minutes by default. Each GC calculates a time point called **safe_point**. Any data earlier than this time point will not be used again, so TiDB can safely clean it up.

For more information, see [GC mechanism](/garbage-collection-overview.md).

### Update statistical information

TiDB uses [statistical information](/statistics.md) to determine index selection. There is a high risk that the index is not correctly selected after a large volume of data is deleted. You can use [manual collection](/statistics.md#manual-collection) to update the statistics. It provides the TiDB optimizer with more accurate statistical information for SQL performance optimization.

## Bulk-delete

When you need to delete multiple rows of data from a table, you can choose the [`DELETE` example](#example) and use the `WHERE` clause to filter the data that needs to be deleted.

However, if you need to delete a large number of rows (more than ten thousand), it is recommended that you delete the data in an iterative way, that is, deleting a portion of the data at each iteration until the deletion is completed. This is because TiDB limits the size of a single transaction ([`txn-total-size-limit`](/tidb-configuration-file.md#txn-total-size-limit), 100 MB by default). You can use loops in your programs or scripts to perform such operations.

This section provides an example of writing a script to handle an iterative delete operation that demonstrates how you should do a combination of `SELECT` and `DELETE` to complete a bulk-delete.

### Write a bulk-delete loop

First, you write a `SELECT` query in a loop of your application or script. Use the returned value of this query as the primary key for the rows that need to be deleted. Note that when defining this `SELECT` query, you need to use the `WHERE` clause to filter the rows that need to be deleted.

### Bulk-delete example

Suppose you find an application error within a specific time period. You need to delete all the data for the [rating](/develop/dev-guide-bookshop-schema-design.md#ratings-table) within this period, for example, from `2022-04-15 00:00:00` to `2022-04-15 00:15:00`, and more than 10,000 records are written in 15 minutes. You can perform as follows.

{{< copyable "" >}}

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

In each iteration, `SELECT` selects up to 1000 rows of primary key values for data in the time period from `2022-04-15 00:00:00` to `2022-04-15 00:15:00`. Then it performs bulk-delete. Note that `TimeUnit.SECONDS.sleep(1);` at the end of each loop will cause the bulk-delete operation to pause for 1 second, preventing the bulk-delete operation from consuming too many hardware resources.