---
title: 更新数据
summary: 了解如何更新数据和批量更新数据。
---

# 更新数据

本文档介绍如何使用以下 SQL 语句和各种编程语言在 TiDB 中更新数据：

- [UPDATE](/sql-statements/sql-statement-update.md)：用于修改指定表中的数据。
- [INSERT ON DUPLICATE KEY UPDATE](/sql-statements/sql-statement-insert.md)：用于插入数据，如果存在主键或唯一键冲突，则更新该数据。如果存在多个唯一键（包括主键），**不建议**使用此语句。这是因为此语句在检测到任何唯一键（包括主键）冲突时都会更新数据。当存在多行冲突时，它只会更新一行。

## 开始之前

在阅读本文档之前，您需要准备以下内容：

- [构建 TiDB Cloud Serverless 集群](/develop/dev-guide-build-cluster-in-cloud.md)。
- 阅读[架构设计概述](/develop/dev-guide-schema-design-overview.md)、[创建数据库](/develop/dev-guide-create-database.md)、[创建表](/develop/dev-guide-create-table.md)和[创建二级索引](/develop/dev-guide-create-secondary-indexes.md)。
- 如果您想要 `UPDATE` 数据，需要先[插入数据](/develop/dev-guide-insert-data.md)。

## 使用 `UPDATE`

要更新表中的现有行，您需要使用带有 `WHERE` 子句的 [`UPDATE` 语句](/sql-statements/sql-statement-update.md)来过滤要更新的列。

> **注意：**
>
> 如果您需要更新大量行，例如超过一万行，建议**_不要_**一次性完全更新，而是每次更新一部分，直到所有行都更新完成。您可以编写脚本或程序来循环执行此操作。
> 详情请参见[批量更新](#批量更新)。

### `UPDATE` SQL 语法

在 SQL 中，`UPDATE` 语句通常采用以下形式：

```sql
UPDATE {table} SET {update_column} = {update_value} WHERE {filter_column} = {filter_value}
```

| 参数名 | 描述 |
| :---------------: | :------------------: |
|     `{table}`     |         表名         |
| `{update_column}` |     要更新的列名     |
| `{update_value}`  |   要更新的列值   |
| `{filter_column}` | 匹配过滤条件的列名 |
| `{filter_value}`  | 匹配过滤条件的列值 |

详细信息，请参见 [UPDATE 语法](/sql-statements/sql-statement-update.md)。

### `UPDATE` 最佳实践

以下是一些更新数据的最佳实践：

- 始终在 `UPDATE` 语句中指定 `WHERE` 子句。如果 `UPDATE` 语句没有 `WHERE` 子句，TiDB 将更新表中的**_所有行_**。

<CustomContent platform="tidb">

- 当需要更新大量行（例如超过一万行）时，使用[批量更新](#批量更新)。因为 TiDB 限制单个事务的大小（[txn-total-size-limit](/tidb-configuration-file.md#txn-total-size-limit)，默认为 100 MB），一次性更新太多数据会导致锁定时间过长（[悲观事务](/pessimistic-transaction.md)）或引起冲突（[乐观事务](/optimistic-transaction.md)）。

</CustomContent>

<CustomContent platform="tidb-cloud">

- 当需要更新大量行（例如超过一万行）时，使用[批量更新](#批量更新)。因为 TiDB 默认限制单个事务的大小为 100 MB，一次性更新太多数据会导致锁定时间过长（[悲观事务](/pessimistic-transaction.md)）或引起冲突（[乐观事务](/optimistic-transaction.md)）。

</CustomContent>

### `UPDATE` 示例

假设一位作者将她的名字改为 **Helen Haruki**。您需要更改 [authors](/develop/dev-guide-bookshop-schema-design.md#authors-table) 表。假设她的唯一 `id` 是 **1**，过滤条件应为：`id = 1`。

<SimpleTab groupId="language">
<div label="SQL" value="sql">

```sql
UPDATE `authors` SET `name` = "Helen Haruki" WHERE `id` = 1;
```

</div>

<div label="Java" value="java">

```java
// ds 是 com.mysql.cj.jdbc.MysqlDataSource 的实例
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

如果您需要向表中插入新数据，但如果存在唯一键（主键也是唯一键）冲突，则会更新第一个冲突的记录。您可以使用 `INSERT ... ON DUPLICATE KEY UPDATE ...` 语句来插入或更新。

### `INSERT ON DUPLICATE KEY UPDATE` SQL 语法

在 SQL 中，`INSERT ... ON DUPLICATE KEY UPDATE ...` 语句通常采用以下形式：

```sql
INSERT INTO {table} ({columns}) VALUES ({values})
    ON DUPLICATE KEY UPDATE {update_column} = {update_value};
```

| 参数名 | 描述 |
| :---------------: | :--------------: |
|     `{table}`     |       表名       |
|    `{columns}`    |   要插入的列名   |
|    `{values}`     | 要插入的列值 |
| `{update_column}` |   要更新的列名   |
| `{update_value}`  | 要更新的列值 |

### `INSERT ON DUPLICATE KEY UPDATE` 最佳实践

- 仅对具有一个唯一键的表使用 `INSERT ON DUPLICATE KEY UPDATE`。此语句在检测到任何**_唯一键_**（包括主键）冲突时都会更新数据。如果存在多行冲突，只会更新一行。因此，除非您能保证只有一行冲突，否则不建议在具有多个唯一键的表中使用 `INSERT ON DUPLICATE KEY UPDATE` 语句。
- 在创建数据或更新数据时使用此语句。

### `INSERT ON DUPLICATE KEY UPDATE` 示例

例如，您需要更新 [ratings](/develop/dev-guide-bookshop-schema-design.md#ratings-table) 表以包含用户对图书的评分。如果用户尚未对图书进行评分，将创建新的评分。如果用户已经评分，将更新他之前的评分。

在以下示例中，主键是 `book_id` 和 `user_id` 的联合主键。用户 `user_id = 1` 给图书 `book_id = 1000` 评分为 `5`。

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
// ds 是 com.mysql.cj.jdbc.MysqlDataSource 的实例

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

当您需要更新表中的多行数据时，可以使用带有 `WHERE` 子句的 [`INSERT ON DUPLICATE KEY UPDATE`](#使用-insert-on-duplicate-key-update) 来过滤需要更新的数据。

<CustomContent platform="tidb">

但是，如果您需要更新大量行（例如超过一万行），建议您迭代更新数据，即每次只更新一部分数据，直到更新完成。这是因为 TiDB 限制单个事务的大小（[txn-total-size-limit](/tidb-configuration-file.md#txn-total-size-limit)，默认为 100 MB）。一次性更新太多数据会导致锁定时间过长（[悲观事务](/pessimistic-transaction.md)）或引起冲突（[乐观事务](/optimistic-transaction.md)）。您可以在程序或脚本中使用循环来完成操作。

</CustomContent>

<CustomContent platform="tidb-cloud">

但是，如果您需要更新大量行（例如超过一万行），建议您迭代更新数据，即每次只更新一部分数据，直到更新完成。这是因为 TiDB 默认限制单个事务的大小为 100 MB。一次性更新太多数据会导致锁定时间过长（[悲观事务](/pessimistic-transaction.md)）或引起冲突（[乐观事务](/optimistic-transaction.md)）。您可以在程序或脚本中使用循环来完成操作。

</CustomContent>

本节提供编写脚本处理迭代更新的示例。此示例展示了如何组合使用 `SELECT` 和 `UPDATE` 来完成批量更新。

### 编写批量更新循环

首先，您应该在应用程序或脚本的循环中编写一个 `SELECT` 查询。此查询的返回值可以用作需要更新的行的主键。请注意，在定义此 `SELECT` 查询时，需要使用 `WHERE` 子句来过滤需要更新的行。

### 示例

假设在过去一年中，您的 `bookshop` 网站收到了大量用户对图书的评分，但原来的 5 分制设计导致图书评分缺乏区分度。大多数图书的评分都是 `3` 分。您决定从 5 分制改为 10 分制，以区分评分。

您需要将 `ratings` 表中之前 5 分制的数据乘以 `2`，并在评分表中添加一个新列来指示行是否已更新。使用此列，您可以在 `SELECT` 中过滤出已更新的行，这将防止脚本崩溃并多次更新行，导致数据不合理。

例如，您创建一个名为 `ten_point` 的列，数据类型为 [BOOL](/data-type-numeric.md#boolean-type)，作为是否为 10 分制的标识符：

```sql
ALTER TABLE `bookshop`.`ratings` ADD COLUMN `ten_point` BOOL NOT NULL DEFAULT FALSE;
```

> **注意：**
>
> 此批量更新应用程序使用 **DDL** 语句对数据表进行架构更改。TiDB 的所有 DDL 更改操作都是在线执行的。更多信息，请参见 [ADD COLUMN](/sql-statements/sql-statement-add-column.md)。

<SimpleTab groupId="language">
<div label="Golang" value="golang">

在 Golang 中，批量更新应用程序类似于以下内容：

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

// updateBatch 选择最多 1000 行数据来更新分数
func updateBatch(db *sql.DB, firstTime bool, lastBookID, lastUserID int64) (bookID, userID int64) {
    // 选择最多 1000 个五分制数据的主键
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

    // 将所有 id 连接成一个列表
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

// placeHolder 格式化 SQL 占位符
func placeHolder(n int) string {
    holderList := make([]string, n/2, n/2)
    for i := range holderList {
        holderList[i] = "(?,?)"
    }
    return strings.Join(holderList, ",")
}
```

在每次迭代中，`SELECT` 按主键顺序查询。它选择最多 `1000` 行尚未更新为 10 分制（`ten_point` 为 `false`）的主键值。每个 `SELECT` 语句选择大于前一个 `SELECT` 结果中最大值的主键，以防止重复。然后，它使用批量更新，将其 `score` 列乘以 `2`，并将 `ten_point` 设置为 `true`。更新 `ten_point` 的目的是防止更新应用程序在崩溃后重启时重复更新同一行，这可能会导致数据损坏。每个循环中的 `time.Sleep(time.Second)` 使更新应用程序暂停 1 秒，以防止更新应用程序消耗过多的硬件资源。

</div>

<div label="Java (JDBC)" value="jdbc">

在 Java (JDBC) 中，批量更新应用程序可能类似于以下内容：

**代码：**

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
        // 配置示例数据库连接

        // 创建 mysql 数据源实例
        MysqlDataSource mysqlDataSource = new MysqlDataSource();

        // 设置服务器名称、端口、数据库名称、用户名和密码
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

- `hibernate.cfg.xml` 配置：

```xml
<?xml version='1.0' encoding='utf-8'?>
<!DOCTYPE hibernate-configuration PUBLIC
        "-//Hibernate/Hibernate Configuration DTD 3.0//EN"
        "http://www.hibernate.org/dtd/hibernate-configuration-3.0.dtd">
<hibernate-configuration>
    <session-factory>

        <!-- 数据库连接设置 -->
        <property name="hibernate.connection.driver_class">com.mysql.cj.jdbc.Driver</property>
        <property name="hibernate.dialect">org.hibernate.dialect.TiDBDialect</property>
        <property name="hibernate.connection.url">jdbc:mysql://localhost:4000/movie</property>
        <property name="hibernate.connection.username">root</property>
        <property name="hibernate.connection.password"></property>
        <property name="hibernate.connection.autocommit">false</property>
        <property name="hibernate.jdbc.batch_size">20</property>

        <!-- 可选：显示 SQL 输出以进行调试 -->
        <property name="hibernate.show_sql">true</property>
        <property name="hibernate.format_sql">true</property>
    </session-factory>
</hibernate-configuration>
```

在每次迭代中，`SELECT` 按主键顺序查询。它选择最多 `1000` 行尚未更新为 10 分制（`ten_point` 为 `false`）的主键值。每个 `SELECT` 语句选择大于前一个 `SELECT` 结果中最大值的主键，以防止重复。然后，它使用批量更新，将其 `score` 列乘以 `2`，并将 `ten_point` 设置为 `true`。更新 `ten_point` 的目的是防止更新应用程序在崩溃后重启时重复更新同一行，这可能会导致数据损坏。每个循环中的 `TimeUnit.SECONDS.sleep(1);` 使更新应用程序暂停 1 秒，以防止更新应用程序消耗过多的硬件资源。

</div>

</SimpleTab>

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上询问社区，或[提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上询问社区，或[提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>
