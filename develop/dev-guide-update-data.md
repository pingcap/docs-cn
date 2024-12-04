---
title: 更新数据
summary: 更新数据、批量更新数据的方法、最佳实践及例子。
---

# 更新数据

此页面将展示以下 SQL 语句，配合各种编程语言 TiDB 中的数据进行更新：

- [UPDATE](/sql-statements/sql-statement-update.md): 用于修改指定表中的数据。
- [INSERT ON DUPLICATE KEY UPDATE](/sql-statements/sql-statement-insert.md): 用于插入数据，在有主键或唯一键冲突时，更新此数据。注意，**_不建议_**在有多个唯一键(包含主键)的情况下使用此语句。这是因为此语句在检测到任何唯一键(包括主键) 冲突时，将更新数据。在不止匹配到一行冲突时，将只会更新一行数据。

## 在开始之前

在阅读本页面之前，你需要准备以下事项：

- [使用 TiDB Cloud Serverless 构建 TiDB 集群](/develop/dev-guide-build-cluster-in-cloud.md)
- 阅读[数据库模式概览](/develop/dev-guide-schema-design-overview.md)，并[创建数据库](/develop/dev-guide-create-database.md)、[创建表](/develop/dev-guide-create-table.md)、[创建二级索引](/develop/dev-guide-create-secondary-indexes.md)
- 若需使用 `UPDATE` 语句更新数据，需先[插入数据](/develop/dev-guide-insert-data.md)

## 使用 `UPDATE`

需更新表中的现有行，需要使用带有 WHERE 子句的 [UPDATE 语句](/sql-statements/sql-statement-update.md)，即需要过滤列进行更新。

> **注意：**
>
> 如果您需要更新大量的行，比如数万甚至更多行，那么建议不要一次性进行完整的更新，而是每次迭代更新一部分，直到所有行全部更新。您可以编写脚本或程序，使用循环完成此操作。
> 您可参考[批量更新](#批量更新)获得指引。

### SQL 语法

在 SQL 中，`UPDATE` 语句一般为以下形式：

```sql
UPDATE {table} SET {update_column} = {update_value} WHERE {filter_column} = {filter_value}
```

|       参数        |         描述         |
| :---------------: | :------------------: |
|     `{table}`     |         表名         |
| `{update_column}` |     需更新的列名     |
| `{update_value}`  |   需更新的此列的值   |
| `{filter_column}` | 匹配条件过滤器的列名 |
| `{filter_value}`  | 匹配条件过滤器的列值 |

此处仅展示 `UPDATE` 的简单用法，详细文档可参考 TiDB 的 [UPDATE 语法页](/sql-statements/sql-statement-update.md)。

### `UPDATE` 最佳实践

以下是更新行时需要遵循的一些最佳实践：

- 始终在更新语句中指定 `WHERE` 子句。如果 `UPDATE` 没有 `WHERE` 子句，TiDB 将更新这个表内的**_所有行_**。
- 需要更新大量行(数万或更多)的时候，使用[批量更新](#批量更新)，这是因为 TiDB 单个事务大小限制为 [txn-total-size-limit](/tidb-configuration-file.md#txn-total-size-limit)（默认为 100MB），且一次性过多的数据更新，将导致持有锁时间过长（[悲观事务](/pessimistic-transaction.md)），或产生大量冲突（[乐观事务](/optimistic-transaction.md)）。

### `UPDATE` 例子

假设某位作者改名为 Helen Haruki，需要更改 [authors](/develop/dev-guide-bookshop-schema-design.md#authors-表) 表。假设他的唯一标识 `id` 为 1，即过滤器应为：`id = 1`。

<SimpleTab groupId="language">
<div label="SQL" value="sql">

在 SQL 中更改作者姓名的示例为：

```sql
UPDATE `authors` SET `name` = "Helen Haruki" WHERE `id` = 1;
```

</div>

<div label="Java" value="java">

在 Java 中更改作者姓名的示例为：

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

## 使用 `INSERT ON DUPLICATE KEY UPDATE`

如果你需要将新数据插入表中，但如果有任何唯一键（主键也是一种唯一键）发生冲突，则会更新第一条冲突数据，可使用 `INSERT ... ON DUPLICATE KEY UPDATE ...` 语句进行插入或更新。

### SQL 语法

在 SQL 中，`INSERT ... ON DUPLICATE KEY UPDATE ...` 语句一般为以下形式：

```sql
INSERT INTO {table} ({columns}) VALUES ({values})
    ON DUPLICATE KEY UPDATE {update_column} = {update_value};
```

|       参数        |       描述       |
| :---------------: | :--------------: |
|     `{table}`     |       表名       |
|    `{columns}`    |   需插入的列名   |
|    `{values}`     | 需插入的此列的值 |
| `{update_column}` |   需更新的列名   |
| `{update_value}`  | 需更新的此列的值 |

### `INSERT ON DUPLICATE KEY UPDATE` 最佳实践

- 在仅有一个唯一键的表上使用 `INSERT ON DUPLICATE KEY UPDATE`。此语句在检测到任何 **_唯一键_** (包括主键) 冲突时，将更新数据。在不止匹配到一行冲突时，将只会更新一行数据。因此，除非能保证仅有一行冲突，否则不建议在有多个唯一键的表中使用 `INSERT ON DUPLICATE KEY UPDATE` 语句。
- 在创建或更新的场景中使用此语句。

### `INSERT ON DUPLICATE KEY UPDATE` 例子

例如，需要更新 [ratings](/develop/dev-guide-bookshop-schema-design.md#ratings-表) 表来写入用户对书籍的评价，如果用户还未评价此书籍，将新建一条评价，如果用户已经评价过，那么将会更新他之前的评价。

此处主键为 `book_id` 和 `user_id` 的联合主键。`user_id` 为 1 的用户，给 `book_id` 为 1000 的书籍，打出的 5 分的评价。

<SimpleTab groupId="language">
<div label="SQL" value="sql">

在 SQL 中更新书籍评价的示例为：

```sql
INSERT INTO `ratings`
    (`book_id`, `user_id`, `score`, `rated_at`)
VALUES
    (1000, 1, 5, NOW())
ON DUPLICATE KEY UPDATE `score` = 5, `rated_at` = NOW();
```

</div>

<div label="Java" value="java">

在 Java 中更新书籍评价的示例为：

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

## 批量更新

需要更新表中多行的数据，可选择[使用 `UPDATE`](#使用-update)，并使用 `WHERE` 子句过滤需要更新的数据。

但如果你需要更新大量行(数万或更多)的时候，建议使用一个迭代，每次都只更新一部分数据，直到更新全部完成。这是因为 TiDB 单个事务大小限制为 [txn-total-size-limit](/tidb-configuration-file.md#txn-total-size-limit)（默认为 100MB），且一次性过多的数据更新，将导致持有锁时间过长（[悲观事务](/pessimistic-transaction.md)），或产生大量冲突（[乐观事务](/optimistic-transaction.md)）。你可以在程序或脚本中使用循环来完成操作。

本页提供了编写脚本来处理循环更新的示例，该示例演示了应如何进行 `SELECT` 和 `UPDATE` 的组合，完成循环更新。

### 编写批量更新循环

首先，你应在你的应用或脚本的循环中，编写一个 `SELECT` 查询。这个查询的返回值可以作为需要更新的行的主键。需要注意的是，定义这个 `SELECT` 查询时，需要注意使用 `WHERE` 子句过滤需要更新的行。

### 例子

假设在过去的一年里，用户在 `bookshop` 网站进行了大量的书籍打分，但是原本设计为 5 分制的评分导致书籍评分的区分度不够，大量书籍评分集中在 3 分附近，因此，决定将 5 分制改为 10 分制。用来增大书籍评分的区分度。

这时需要对 `ratings` 表内之前 5 分制的数据进行乘 2 操作，同时需向 `ratings` 表内添加一个新列，以指示行是否已经被更新了。使用此列，可以在 `SELECT` 中过滤掉已经更新的行，这将防止脚本崩溃时对行进行多次更新，导致不合理的数据出现。

例如，你可以创建一个名为 `ten_point`，数据类型为 [BOOL](/data-type-numeric.md#boolean-类型) 的列作为是否为 10 分制的标识：

```sql
ALTER TABLE `bookshop`.`ratings` ADD COLUMN `ten_point` BOOL NOT NULL DEFAULT FALSE;
```

> **注意：**
>
> 此批量更新程序将使用 **DDL** 语句将进行数据表的模式更改。TiDB 的所有 DDL 变更操作全部都是在线进行的，可查看此处，了解此处使用的 [ADD COLUMN](/sql-statements/sql-statement-add-column.md) 语句。

<SimpleTab groupId="language">
<div label="Golang" value="golang">

在 Golang 中，批量更新程序类似于以下内容：

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

每次迭代中，`SELECT` 按主键顺序进行查询，最多选择 1000 行未更新到 10 分制（`ten_point` 为 `false`）数据的主键值。每次 `SELECT` 都会选择比上一次 `SELECT` 结果的最大主键还要大的数据，防止重复。然后，使用批量更新的方式，对其 `score` 列乘 2，并且将 `ten_point` 设为 `true`，更新 `ten_point` 的意义是在于防止更新程序崩溃重启后，反复更新同一行数据，导致数据损坏。每次循环中的 `time.Sleep(time.Second)` 将使得更新程序暂停 1 秒，防止批量更新程序占用过多的硬件资源。

</div>

<div label="Java (JDBC)" value="java">

在 Java (JDBC) 中，批量更新程序类似于以下内容：

**Java 代码部分：**

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

**`hibernate.cfg.xml` 配置部分：**

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

每次迭代中，`SELECT` 按主键顺序进行查询，最多选择 1000 行未更新到 10 分制（`ten_point` 为 `false`）数据的主键值。每次 `SELECT` 都会选择比上一次 `SELECT` 结果的最大主键还要大的数据，防止重复。然后，使用批量更新的方式，对其 `score` 列乘 2，并且将 `ten_point` 设为 `true`，更新 `ten_point` 的意义是在于防止更新程序崩溃重启后，反复更新同一行数据，导致数据损坏。每次循环中的 `TimeUnit.SECONDS.sleep(1);` 将使得更新程序暂停 1 秒，防止批量更新程序占用过多的硬件资源。

</div>

</SimpleTab>
