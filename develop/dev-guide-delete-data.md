---
title: Delete Data
summary: Learn about the SQL syntax, best practices, and examples for deleting data.
---

# Delete Data

This document describes how to use the [DELETE](/sql-statements/sql-statement-delete.md) SQL statement to delete the data in TiDB. If you need to periodically delete expired data, use the [time to live](/time-to-live.md) feature.

## Before you start

Before reading this document, you need to prepare the following:

- [Build a TiDB Serverless Cluster](/develop/dev-guide-build-cluster-in-cloud.md)
- Read [Schema Design Overview](/develop/dev-guide-schema-design-overview.md), [Create a Database](/develop/dev-guide-create-database.md), [Create a Table](/develop/dev-guide-create-table.md), and [Create Secondary Indexes](/develop/dev-guide-create-secondary-indexes.md)
- [Insert Data](/develop/dev-guide-insert-data.md)

## SQL syntax

The `DELETE` statement is generally in the following form:

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

<CustomContent platform="tidb">

- Use [bulk-delete](#bulk-delete) when you delete a large number of rows (for example, more than ten thousand), because TiDB limits the size of a single transaction ([txn-total-size-limit](/tidb-configuration-file.md#txn-total-size-limit), 100 MB by default).

</CustomContent>

<CustomContent platform="tidb-cloud">

- Use [bulk-delete](#bulk-delete) when you delete a large number of rows (for example, more than ten thousand), because TiDB limits the size of a single transaction to 100 MB by default.

</CustomContent>

- If you delete all the data in a table, do not use the `DELETE` statement. Instead, use the [`TRUNCATE`](/sql-statements/sql-statement-truncate.md) statement.
- For performance considerations, see [Performance Considerations](#performance-considerations).
- In scenarios where large batches of data need to be deleted, [Non-Transactional bulk-delete](#non-transactional-bulk-delete) can significantly improve performance. However, this will lose the transactional of the deletion and therefore **CANNOT** be rolled back. Make sure that you select the correct operation.

## Example

Suppose you find an application error within a specific time period and you need to delete all the data for the [ratings](/develop/dev-guide-bookshop-schema-design.md#ratings-table) within this period, for example, from `2022-04-15 00:00:00` to `2022-04-15 00:15:00`. In this case, you can use the `SELECT` statement to check the number of records to be deleted.

```sql
SELECT COUNT(*) FROM `ratings` WHERE `rated_at` >= "2022-04-15 00:00:00" AND `rated_at` <= "2022-04-15 00:15:00";
```

If more than 10,000 records are returned, use [Bulk-Delete](#bulk-delete) to delete them.

If fewer than 10,000 records are returned, use the following example to delete them.

<SimpleTab groupId="language">
<div label="SQL" value="sql">

In SQL, the example is as follows:

```sql
DELETE FROM `ratings` WHERE `rated_at` >= "2022-04-15 00:00:00" AND `rated_at` <= "2022-04-15 00:15:00";
```

</div>

<div label="Java" value="java">

In Java, the example is as follows:

```java
// ds is an entity of com.mysql.cj.jdbc.MysqlDataSource

try (Connection connection = ds.getConnection()) {
    String sql = "DELETE FROM `bookshop`.`ratings` WHERE `rated_at` >= ? AND `rated_at` <= ?";
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

In Golang, the example is as follows:

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

    bulkUpdateSql := fmt.Sprintf("DELETE FROM `bookshop`.`ratings` WHERE `rated_at` >= ? AND `rated_at` <= ?")
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

In Python, the example is as follows:

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

<CustomContent platform="tidb">

The `rated_at` field is of the `DATETIME` type in [Date and Time Types](/data-type-date-and-time.md). You can assume that it is stored as a literal quantity in TiDB, independent of the time zone. On the other hand, the `TIMESTAMP` type stores a timestamp and thus displays a different time string in a different [time zone](/configure-time-zone.md).

</CustomContent>

<CustomContent platform="tidb-cloud">

The `rated_at` field is of the `DATETIME` type in [Date and Time Types](/data-type-date-and-time.md). You can assume that it is stored as a literal quantity in TiDB, independent of the time zone. On the other hand, the `TIMESTAMP` type stores a timestamp and thus displays a different time string in a different time zone.

</CustomContent>

> **Note:**
>
> Like MySQL, the `TIMESTAMP` data type is affected by the [year 2038 problem](https://en.wikipedia.org/wiki/Year_2038_problem). It is recommended to use the `DATETIME` type if you store values larger than 2038.

## Performance considerations

### TiDB GC mechanism

TiDB does not delete the data immediately after you run the `DELETE` statement. Instead, it marks the data as ready for deletion. Then it waits for TiDB GC (Garbage Collection) to clean up the outdated data. Therefore, the `DELETE` statement **_DOES NOT_** immediately reduce disk usage.

GC is triggered once every 10 minutes by default. Each GC calculates a time point called **safe_point**. Any data earlier than this time point will not be used again, so TiDB can safely clean it up.

For more information, see [GC mechanism](/garbage-collection-overview.md).

### Update statistical information

TiDB uses [statistical information](/statistics.md) to determine index selection. There is a high risk that the index is not correctly selected after a large volume of data is deleted. You can use [manual collection](/statistics.md#manual-collection) to update the statistics. It provides the TiDB optimizer with more accurate statistical information for SQL performance optimization.

## Bulk-delete

When you need to delete multiple rows of data from a table, you can choose the [`DELETE` example](#example) and use the `WHERE` clause to filter the data that needs to be deleted.

<CustomContent platform="tidb">

However, if you need to delete a large number of rows (more than ten thousand), it is recommended that you delete the data in an iterative way, that is, deleting a portion of the data at each iteration until the deletion is completed. This is because TiDB limits the size of a single transaction ([`txn-total-size-limit`](/tidb-configuration-file.md#txn-total-size-limit), 100 MB by default). You can use loops in your programs or scripts to perform such operations.

</CustomContent>

<CustomContent platform="tidb-cloud">

However, if you need to delete a large number of rows (more than ten thousand), it is recommended that you delete the data in an iterative way, that is, deleting a portion of the data at each iteration until the deletion is completed. This is because TiDB limits the size of a single transaction to 100 MB by default. You can use loops in your programs or scripts to perform such operations.

</CustomContent>

This section provides an example of writing a script to handle an iterative delete operation that demonstrates how you should do a combination of `SELECT` and `DELETE` to complete a bulk-delete.

### Write a bulk-delete loop

You can write a `DELETE` statement in the loop of your application or script, use the `WHERE` clause to filter data, and use `LIMIT` to constrain the number of rows to be deleted in a single statement.

### Bulk-delete example

Suppose you find an application error within a specific time period. You need to delete all the data for the [rating](/develop/dev-guide-bookshop-schema-design.md#ratings-table) within this period, for example, from `2022-04-15 00:00:00` to `2022-04-15 00:15:00`, and more than 10,000 records are written in 15 minutes. You can perform as follows.

<SimpleTab groupId="language">
<div label="Java" value="java">

In Java, the bulk-delete example is as follows:

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
            String sql = "DELETE FROM `bookshop`.`ratings` WHERE `rated_at` >= ? AND `rated_at` <= ? LIMIT 1000";
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

In each iteration, `DELETE` deletes up to 1000 rows from `2022-04-15 00:00:00` to `2022-04-15 00:15:00`.

</div>

<div label="Golang" value="golang">

In Golang, the bulk-delete example is as follows:

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
    bulkUpdateSql := fmt.Sprintf("DELETE FROM `bookshop`.`ratings` WHERE `rated_at` >= ? AND `rated_at` <= ? LIMIT 1000")
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

In each iteration, `DELETE` deletes up to 1000 rows from `2022-04-15 00:00:00` to `2022-04-15 00:15:00`.

</div>

<div label="Python" value="python">

In Python, the bulk-delete example is as follows:

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

In each iteration, `DELETE` deletes up to 1000 rows from `2022-04-15 00:00:00` to `2022-04-15 00:15:00`.

</div>

</SimpleTab>

## Non-transactional bulk-delete

> **Note:**
>
> Since v6.1.0, TiDB supports the [non-transactional DML statements](/non-transactional-dml.md). This feature is not available for versions earlier than TiDB v6.1.0.

### Prerequisites of non-transactional bulk-delete

Before using the non-transactional bulk-delete, make sure you have read the [Non-Transactional DML statements documentation](/non-transactional-dml.md) first. The non-transactional bulk-delete improves the performance and ease of use in batch data processing scenarios but compromises transactional atomicity and isolation.

Therefore, you should use it carefully to avoid serious consequences (such as data loss) due to mishandling.

### SQL syntax for non-transactional bulk-delete

The SQL syntax for non-transactional bulk-delete statement is as follows:

```sql
BATCH ON {shard_column} LIMIT {batch_size} {delete_statement};
```

| Parameter Name | Description |
| :--------: | :------------: |
| `{shard_column}` | The column used to divide batches.      |
| `{batch_size}`   | Control the size of each batch. |
| `{delete_statement}` | The `DELETE` statement. |

The preceding example only shows a simple use case of a non-transactional bulk-delete statement. For detailed information, see [Non-transactional DML Statements](/non-transactional-dml.md).

### Example of non-transactional bulk-delete

In the same scenario as the [Bulk-delete example](#bulk-delete-example), the following SQL statement shows how to perform a non-transactional bulk-delete:

```sql
BATCH ON `rated_at` LIMIT 1000 DELETE FROM `ratings` WHERE `rated_at` >= "2022-04-15 00:00:00" AND  `rated_at` <= "2022-04-15 00:15:00";
```
