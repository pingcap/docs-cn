---
title: Update Data
summary: Learn about how to update data and batch update data.
---

# Update Data

This document describes how to use the following SQL statements to update the data in TiDB with various programming languages:

- [UPDATE](/sql-statements/sql-statement-update.md): Used to modify the data in the specified table.
- [INSERT ON DUPLICATE KEY UPDATE](/sql-statements/sql-statement-insert.md): Used to insert data and update this data if there is a primary key or unique key conflict. It is **not recommended** to use this statement if there are multiple unique keys (including primary keys). This is because this statement updates the data once it detects any unique key (including primary key) conflict. When there are more than one row conflicts, it updates only one row.

## Before you start

Before reading this document, you need to prepare the following:

- [Build a TiDB Serverless Cluster](/develop/dev-guide-build-cluster-in-cloud.md).
- Read [Schema Design Overview](/develop/dev-guide-schema-design-overview.md), [Create a Database](/develop/dev-guide-create-database.md), [Create a Table](/develop/dev-guide-create-table.md), and [Create Secondary Indexes](/develop/dev-guide-create-secondary-indexes.md).
- If you want to `UPDATE` data, you need to [insert data](/develop/dev-guide-insert-data.md) first.

## Use `UPDATE`

To update an existing row in a table, you need to use an [`UPDATE` statement](/sql-statements/sql-statement-update.md) with a `WHERE` clause to filter the columns for updating.

> **Note:**
>
> If you need to update a large number of rows, for example, more than ten thousand, it is recommended that you do **_NOT_** doing a complete update at once, but rather updating a portion at a time iteratively until all rows are updated. You can write scripts or programs to loop this operation.
> See [Bulk-update](#bulk-update) for details.

### `UPDATE` SQL syntax

In SQL, the `UPDATE` statement is generally in the following form:

```sql
UPDATE {table} SET {update_column} = {update_value} WHERE {filter_column} = {filter_value}
```

| Parameter Name | Description |
| :---------------: | :------------------: |
|     `{table}`     |         Table Name         |
| `{update_column}` |     Column names to be updated     |
| `{update_value}`  |   Column values to be updated   |
| `{filter_column}` | Column names matching filters |
| `{filter_value}`  | Column values matching filters |

For detailed information, see [UPDATE syntax](/sql-statements/sql-statement-update.md).

### `UPDATE` best practices

The following are some best practices for updating data:

- Always specify the `WHERE` clause in the `UPDATE` statement. If the `UPDATE` statement does not have a `WHERE` clause, TiDB will update **_ALL ROWS_** in the table.

<CustomContent platform="tidb">

- Use [bulk-update](#bulk-update) when you need to update a large number of rows (for example, more than ten thousand). Because TiDB limits the size of a single transaction ([txn-total-size-limit](/tidb-configuration-file.md#txn-total-size-limit), 100 MB by default), too many data updates at once will result in holding locks for too long ([pessimistic transactions](/pessimistic-transaction.md)) or cause conflicts ([optimistic transactions](/optimistic-transaction.md)).

</CustomContent>

<CustomContent platform="tidb-cloud">

- Use [bulk-update](#bulk-update) when you need to update a large number of rows (for example, more than ten thousand). Because TiDB limits the size of a single transaction to 100 MB by default, too many data updates at once will result in holding locks for too long ([pessimistic transactions](/pessimistic-transaction.md)) or cause conflicts ([optimistic transactions](/optimistic-transaction.md)).

</CustomContent>

### `UPDATE` example

Suppose an author changes her name to **Helen Haruki**. You need to change the [authors](/develop/dev-guide-bookshop-schema-design.md#authors-table) table. Assume that her unique `id` is **1**, and the filter should be: `id = 1`.

<SimpleTab groupId="language">
<div label="SQL" value="sql">

```sql
UPDATE `authors` SET `name` = "Helen Haruki" WHERE `id` = 1;
```

</div>

<div label="Java" value="java">

```java
// ds is an entity of com.mysql.cj.jdbc.MysqlDataSource
try (Connection connection = ds.getConnection()) {
    PreparedStatement pstmt = connection.prepareStatement("UPDATE `authors` SET `name` = ? WHERE `id` = ?");
    pstmt.setString(1, "Helen Haruki");
    pstmt.setInt(2, 1);
    pstmt.executeUpdate();
} catch (SQLException e) {
    e.printStackTrace();
}
```

</div>
</SimpleTab>

## Use `INSERT ON DUPLICATE KEY UPDATE`

If you need to insert new data into a table, but if there are unique key (a primary key is also a unique key) conflicts, the first conflicted record will be updated. You can use `INSERT ... ON DUPLICATE KEY UPDATE ...` statement to insert or update.

### `INSERT ON DUPLICATE KEY UPDATE` SQL Syntax

In SQL, the `INSERT ... ON DUPLICATE KEY UPDATE ...` statement is generally in the following form:

```sql
INSERT INTO {table} ({columns}) VALUES ({values})
    ON DUPLICATE KEY UPDATE {update_column} = {update_value};
```

| Parameter Name | Description |
| :---------------: | :--------------: |
|     `{table}`     |       Table name       |
|    `{columns}`    |   Column names to be inserted   |
|    `{values}`     | Column values to be inserted |
| `{update_column}` |   Column names to be updated   |
| `{update_value}`  | Column values to be updated |

### `INSERT ON DUPLICATE KEY UPDATE` best practices

- Use `INSERT ON DUPLICATE KEY UPDATE` only for a table with one unique key. This statement updates the data if any **_UNIQUE KEY_** (including the primary key) conflicts are detected. If there are more than one row of conflicts, only one row will be updated. Therefore, it is not recommended to use the `INSERT ON DUPLICATE KEY UPDATE` statement in tables with multiple unique keys unless you can guarantee that there is only one row of conflict.
- Use this statement when you create data or update data.

### `INSERT ON DUPLICATE KEY UPDATE` example

For example, you need to update the [ratings](/develop/dev-guide-bookshop-schema-design.md#ratings-table) table to include the user's ratings for the book. If the user has not yet rated the book, a new rating will be created. If the user has already rated it, his previous rating will be updated.

In the following example, the primary key is the joint primary keys of `book_id` and `user_id`. A user `user_id = 1` gives a rating of `5` to a book `book_id = 1000`.

<SimpleTab groupId="language">
<div label="SQL" value="sql">

```sql
INSERT INTO `ratings`
    (`book_id`, `user_id`, `score`, `rated_at`)
VALUES
    (1000, 1, 5, NOW())
ON DUPLICATE KEY UPDATE `score` = 5, `rated_at` = NOW();
```

</div>

<div label="Java" value="java">

```java
// ds is an entity of com.mysql.cj.jdbc.MysqlDataSource

try (Connection connection = ds.getConnection()) {
    PreparedStatement p = connection.prepareStatement("INSERT INTO `ratings` (`book_id`, `user_id`, `score`, `rated_at`)
VALUES (?, ?, ?, NOW()) ON DUPLICATE KEY UPDATE `score` = ?, `rated_at` = NOW()");
    p.setInt(1, 1000);
    p.setInt(2, 1);
    p.setInt(3, 5);
    p.setInt(4, 5);
    p.executeUpdate();
} catch (SQLException e) {
    e.printStackTrace();
}
```

</div>
</SimpleTab>

## Bulk-update

When you need to update multiple rows of data in a table, you can [use `INSERT ON DUPLICATE KEY UPDATE`](#use-insert-on-duplicate-key-update) with the `WHERE` clause to filter the data that needs to be updated.

<CustomContent platform="tidb">

However, if you need to update a large number of rows (for example, more than ten thousand), it is recommended that you update the data iteratively, that is, updating only a portion of the data at each iteration until the update is complete. This is because TiDB limits the size of a single transaction ([txn-total-size-limit](/tidb-configuration-file.md#txn-total-size-limit), 100 MB by default). Too many data updates at once will result in holding locks for too long ([pessimistic transactions](/pessimistic-transaction.md), or causing conflicts ([optimistic transactions](/optimistic-transaction.md)). You can use a loop in your program or script to complete the operation.

</CustomContent>

<CustomContent platform="tidb-cloud">

However, if you need to update a large number of rows (for example, more than ten thousand), it is recommended that you update the data iteratively, that is, updating only a portion of the data at each iteration until the update is complete. This is because TiDB limits the size of a single transaction to 100 MB by default. Too many data updates at once will result in holding locks for too long ([pessimistic transactions](/pessimistic-transaction.md), or causing conflicts ([optimistic transactions](/optimistic-transaction.md)). You can use a loop in your program or script to complete the operation.

</CustomContent>

This section provides examples of writing scripts to handle iterative updates. This example shows how a combination of `SELECT` and `UPDATE` should be done to complete a bulk-update.

### Write bulk-update loop

First, you should write a `SELECT` query in a loop of your application or script. The return value of this query can be used as the primary key for the rows that need to be updated. Note that when defining this `SELECT` query, you need to use the `WHERE` clause to filter the rows that need to be updated.

### Example

Suppose that you have had a lot of book ratings from users on your `bookshop` website over the past year, but the original design of a 5-point scale has resulted in a lack of differentiation in book ratings. Most books are rated `3`. You decide to switch from a 5-point scale to a 10-point scale to differentiate ratings.

You need to multiply by `2` the data in the `ratings` table from the previous 5-point scale, and add a new column to the ratings table to indicate whether the rows have been updated. Using this column, you can filter out rows that have been updated in `SELECT`, which will prevent the script from crashing and updating the rows multiple times, resulting in unreasonable data.

For example, you create a column named `ten_point` with the data type [BOOL](/data-type-numeric.md#boolean-type) as an identifier of whether it is a 10-point scale:

```sql
ALTER TABLE `bookshop`.`ratings` ADD COLUMN `ten_point` BOOL NOT NULL DEFAULT FALSE;
```

> **Note:**
>
> This bulk-update application uses the **DDL** statements to make schema changes to the data tables. All DDL change operations for TiDB are executed online. For more information, see [ADD COLUMN](/sql-statements/sql-statement-add-column.md).

<SimpleTab groupId="language">
<div label="Golang" value="golang">

In Golang, a bulk-update application is similar to the following:

```go
package main

import (
    "database/sql"
    "fmt"
    _ "github.com/go-sql-driver/mysql"
    "strings"
    "time"
)

func main() {
    db, err := sql.Open("mysql", "root:@tcp(127.0.0.1:4000)/bookshop")
    if err != nil {
        panic(err)
    }
    defer db.Close()

    bookID, userID := updateBatch(db, true, 0, 0)
    fmt.Println("first time batch update success")
    for {
        time.Sleep(time.Second)
        bookID, userID = updateBatch(db, false, bookID, userID)
        fmt.Printf("batch update success, [bookID] %d, [userID] %d\n", bookID, userID)
    }
}

// updateBatch select at most 1000 lines data to update score
func updateBatch(db *sql.DB, firstTime bool, lastBookID, lastUserID int64) (bookID, userID int64) {
    // select at most 1000 primary keys in five-point scale data
    var err error
    var rows *sql.Rows

    if firstTime {
        rows, err = db.Query("SELECT `book_id`, `user_id` FROM `bookshop`.`ratings` " +
            "WHERE `ten_point` != true ORDER BY `book_id`, `user_id` LIMIT 1000")
    } else {
        rows, err = db.Query("SELECT `book_id`, `user_id` FROM `bookshop`.`ratings` "+
            "WHERE `ten_point` != true AND `book_id` > ? AND `user_id` > ? "+
            "ORDER BY `book_id`, `user_id` LIMIT 1000", lastBookID, lastUserID)
    }

    if err != nil || rows == nil {
        panic(fmt.Errorf("error occurred or rows nil: %+v", err))
    }

    // joint all id with a list
    var idList []interface{}
    for rows.Next() {
        var tempBookID, tempUserID int64
        if err := rows.Scan(&tempBookID, &tempUserID); err != nil {
            panic(err)
        }
        idList = append(idList, tempBookID, tempUserID)
        bookID, userID = tempBookID, tempUserID
    }

    bulkUpdateSql := fmt.Sprintf("UPDATE `bookshop`.`ratings` SET `ten_point` = true, "+
        "`score` = `score` * 2 WHERE (`book_id`, `user_id`) IN (%s)", placeHolder(len(idList)))
    db.Exec(bulkUpdateSql, idList...)

    return bookID, userID
}

// placeHolder format SQL place holder
func placeHolder(n int) string {
    holderList := make([]string, n/2, n/2)
    for i := range holderList {
        holderList[i] = "(?,?)"
    }
    return strings.Join(holderList, ",")
}
```

In each iteration, `SELECT` queries in order of the primary key. It selects primary key values for up to `1000` rows that have not been updated to the 10-point scale (`ten_point` is `false`). Each `SELECT` statement selects primary keys larger than the largest of the previous `SELECT` results to prevent duplication. Then, it uses bulk-update, multiples its `score` column by `2`, and sets `ten_point` to `true`. The purpose of updating `ten_point` is to prevent the update application from repeatedly updating the same row in case of restart after crashing, which can cause data corruption. `time.Sleep(time.Second)` in each loop makes the update application pause for 1 second to prevent the update application from consuming too many hardware resources.

</div>

<div label="Java (JDBC)" value="jdbc">

In Java (JDBC), a bulk-update application might be similar to the following:

**Code:**

```java
package com.pingcap.bulkUpdate;

import com.mysql.cj.jdbc.MysqlDataSource;

import java.sql.*;
import java.util.LinkedList;
import java.util.List;
import java.util.concurrent.TimeUnit;

public class BatchUpdateExample {
    static class UpdateID {
        private Long bookID;
        private Long userID;

        public UpdateID(Long bookID, Long userID) {
            this.bookID = bookID;
            this.userID = userID;
        }

        public Long getBookID() {
            return bookID;
        }

        public void setBookID(Long bookID) {
            this.bookID = bookID;
        }

        public Long getUserID() {
            return userID;
        }

        public void setUserID(Long userID) {
            this.userID = userID;
        }

        @Override
        public String toString() {
            return "[bookID] " + bookID + ", [userID] " + userID ;
        }
    }

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

        UpdateID lastID = batchUpdate(mysqlDataSource, null);

        System.out.println("first time batch update success");
        while (true) {
            TimeUnit.SECONDS.sleep(1);
            lastID = batchUpdate(mysqlDataSource, lastID);
            System.out.println("batch update success, [lastID] " + lastID);
        }
    }

    public static UpdateID batchUpdate (MysqlDataSource ds, UpdateID lastID) {
        try (Connection connection = ds.getConnection()) {
            UpdateID updateID = null;

            PreparedStatement selectPs;

            if (lastID == null) {
                selectPs = connection.prepareStatement(
                        "SELECT `book_id`, `user_id` FROM `bookshop`.`ratings` " +
                        "WHERE `ten_point` != true ORDER BY `book_id`, `user_id` LIMIT 1000");
            } else {
                selectPs = connection.prepareStatement(
                        "SELECT `book_id`, `user_id` FROM `bookshop`.`ratings` "+
                            "WHERE `ten_point` != true AND `book_id` > ? AND `user_id` > ? "+
                            "ORDER BY `book_id`, `user_id` LIMIT 1000");

                selectPs.setLong(1, lastID.getBookID());
                selectPs.setLong(2, lastID.getUserID());
            }

            List<Long> idList = new LinkedList<>();
            ResultSet res = selectPs.executeQuery();
            while (res.next()) {
                updateID = new UpdateID(
                        res.getLong("book_id"),
                        res.getLong("user_id")
                );
                idList.add(updateID.getBookID());
                idList.add(updateID.getUserID());
            }

            if (idList.isEmpty()) {
                System.out.println("no data should update");
                return null;
            }

            String updateSQL = "UPDATE `bookshop`.`ratings` SET `ten_point` = true, "+
                    "`score` = `score` * 2 WHERE (`book_id`, `user_id`) IN (" +
                    placeHolder(idList.size() / 2) + ")";
            PreparedStatement updatePs = connection.prepareStatement(updateSQL);
            for (int i = 0; i < idList.size(); i++) {
                updatePs.setLong(i + 1, idList.get(i));
            }
            int count = updatePs.executeUpdate();
            System.out.println("update " + count + " data");

            return updateID;
        } catch (SQLException e) {
            e.printStackTrace();
        }

        return null;
    }

    public static String placeHolder(int n) {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < n ; i++) {
            sb.append(i == 0 ? "(?,?)" : ",(?,?)");
        }

        return sb.toString();
    }
}
```

- `hibernate.cfg.xml` configuration:

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
        <property name="hibernate.connection.url">jdbc:mysql://localhost:4000/movie</property>
        <property name="hibernate.connection.username">root</property>
        <property name="hibernate.connection.password"></property>
        <property name="hibernate.connection.autocommit">false</property>
        <property name="hibernate.jdbc.batch_size">20</property>

        <!-- Optional: Show SQL output for debugging -->
        <property name="hibernate.show_sql">true</property>
        <property name="hibernate.format_sql">true</property>
    </session-factory>
</hibernate-configuration>
```

In each iteration, `SELECT` queries in order of the primary key. It selects primary key values for up to `1000` rows that have not been updated to the 10-point scale (`ten_point` is `false`). Each `SELECT` statement selects primary keys larger than the largest of the previous `SELECT` results to prevent duplication. Then, it uses bulk-update, multiples its `score` column by `2`, and sets `ten_point` to `true`. The purpose of updating `ten_point` is to prevent the update application from repeatedly updating the same row in case of restart after crashing, which can cause data corruption. `TimeUnit.SECONDS.sleep(1);` in each loop makes the update application pause for 1 second to prevent the update application from consuming too many hardware resources.

</div>

</SimpleTab>
