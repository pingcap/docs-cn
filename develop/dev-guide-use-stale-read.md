---
title: 历史读取
summary: 了解如何在特定条件下使用历史读取来加速查询。
---

# 历史读取

历史读取（Stale Read）是 TiDB 用于读取存储在 TiDB 中的历史版本数据的机制。使用此机制，您可以读取特定时间或指定时间范围内的相应历史数据，从而节省存储节点之间数据复制造成的延迟。当您使用历史读取时，TiDB 会随机选择一个副本进行数据读取，这意味着所有副本都可用于数据读取。

在实践中，请根据[使用场景](/stale-read.md#usage-scenarios-of-stale-read)仔细考虑是否适合在 TiDB 中启用历史读取。如果您的应用程序不能容忍读取非实时数据，请不要启用历史读取。

TiDB 提供了三个级别的历史读取：语句级别、事务级别和会话级别。

## 简介

在 [Bookshop](/develop/dev-guide-bookshop-schema-design.md) 应用程序中，您可以通过以下 SQL 语句查询最新发布的图书及其价格：

```sql
SELECT id, title, type, price FROM books ORDER BY published_at DESC LIMIT 5;
```

结果如下：

```
+------------+------------------------------+-----------------------+--------+
| id         | title                        | type                  | price  |
+------------+------------------------------+-----------------------+--------+
| 3181093216 | The Story of Droolius Caesar | Novel                 | 100.00 |
| 1064253862 | Collin Rolfson               | Education & Reference |  92.85 |
| 1748583991 | The Documentary of cat       | Magazine              | 159.75 |
|  893930596 | Myrl Hills                   | Education & Reference | 356.85 |
| 3062833277 | Keven Wyman                  | Life                  | 477.91 |
+------------+------------------------------+-----------------------+--------+
5 rows in set (0.02 sec)
```

在此时（2022-04-20 15:20:00），《The Story of Droolius Caesar》的价格是 100.0。

同时，卖家发现这本书很受欢迎，通过以下 SQL 语句将书的价格提高到 150.0：

```sql
UPDATE books SET price = 150 WHERE id = 3181093216;
```

结果如下：

```
Query OK, 1 row affected (0.00 sec)
Rows matched: 1  Changed: 1  Warnings: 0
```

通过查询最新的图书列表，您可以看到这本书的价格已经上涨。

```
+------------+------------------------------+-----------------------+--------+
| id         | title                        | type                  | price  |
+------------+------------------------------+-----------------------+--------+
| 3181093216 | The Story of Droolius Caesar | Novel                 | 150.00 |
| 1064253862 | Collin Rolfson               | Education & Reference |  92.85 |
| 1748583991 | The Documentary of cat       | Magazine              | 159.75 |
|  893930596 | Myrl Hills                   | Education & Reference | 356.85 |
| 3062833277 | Keven Wyman                  | Life                  | 477.91 |
+------------+------------------------------+-----------------------+--------+
5 rows in set (0.01 sec)
```

如果不需要使用最新数据，您可以使用历史读取进行查询，这可能会返回过期数据，以避免强一致性读取期间数据复制造成的延迟。

假设在 Bookshop 应用程序中，图书列表页面不需要实时价格，只在图书详情和订单页面需要实时价格。这时可以使用历史读取来提高应用程序的吞吐量。

## 语句级别

<SimpleTab groupId="language">
<div label="SQL" value="sql">

要查询特定时间之前的图书价格，在上述查询语句中添加 `AS OF TIMESTAMP <datetime>` 子句。

```sql
SELECT id, title, type, price FROM books AS OF TIMESTAMP '2022-04-20 15:20:00' ORDER BY published_at DESC LIMIT 5;
```

结果如下：

```
+------------+------------------------------+-----------------------+--------+
| id         | title                        | type                  | price  |
+------------+------------------------------+-----------------------+--------+
| 3181093216 | The Story of Droolius Caesar | Novel                 | 100.00 |
| 1064253862 | Collin Rolfson               | Education & Reference |  92.85 |
| 1748583991 | The Documentary of cat       | Magazine              | 159.75 |
|  893930596 | Myrl Hills                   | Education & Reference | 356.85 |
| 3062833277 | Keven Wyman                  | Life                  | 477.91 |
+------------+------------------------------+-----------------------+--------+
5 rows in set (0.01 sec)
```

除了指定确切时间外，您还可以指定以下内容：

- `AS OF TIMESTAMP NOW() - INTERVAL 10 SECOND` 查询 10 秒前的最新数据。
- `AS OF TIMESTAMP TIDB_BOUNDED_STALENESS('2016-10-08 16:45:26', '2016-10-08 16:45:29')` 查询 `2016-10-08 16:45:26` 和 `2016-10-08 16:45:29` 之间的最新数据。
- `AS OF TIMESTAMP TIDB_BOUNDED_STALENESS(NOW() -INTERVAL 20 SECOND, NOW())` 查询 20 秒内的最新数据。

请注意，指定的时间戳或间隔不能太早或晚于当前时间。此外，`NOW()` 默认为秒精度。要实现更高精度，您可以添加参数，例如使用 `NOW(3)` 获取毫秒精度。更多信息，请参见 [MySQL 文档](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_now)。

过期数据将被 TiDB 中的[垃圾回收](/garbage-collection-overview.md)回收，数据在被清除前会保留一段时间。这段时间称为 [GC Life Time（默认 10 分钟）](/system-variables.md#tidb_gc_life_time-new-in-v50)。当 GC 启动时，当前时间减去这段时间将被用作 **GC Safe Point**。如果您尝试读取 GC Safe Point 之前的数据，TiDB 将报告以下错误：

```
ERROR 9006 (HY000): GC life time is shorter than transaction duration...
```

如果给定的时间戳是未来时间，TiDB 将报告以下错误：

```
ERROR 9006 (HY000): cannot set read timestamp to a future time.
```

</div>
<div label="Java" value="java">

```java
public class BookDAO {

    // 省略部分代码...

    public List<Book> getTop5LatestBooks() throws SQLException {
        List<Book> books = new ArrayList<>();
        try (Connection conn = ds.getConnection()) {
            Statement stmt = conn.createStatement();
            ResultSet rs = stmt.executeQuery("""
            SELECT id, title, type, price FROM books ORDER BY published_at DESC LIMIT 5;
            """);
            while (rs.next()) {
                Book book = new Book();
                book.setId(rs.getLong("id"));
                book.setTitle(rs.getString("title"));
                book.setType(rs.getString("type"));
                book.setPrice(rs.getDouble("price"));
                books.add(book);
            }
        }
        return books;
    }

    public void updateBookPriceByID(Long id, Double price) throws SQLException {
        try (Connection conn = ds.getConnection()) {
            PreparedStatement stmt = conn.prepareStatement("""
            UPDATE books SET price = ? WHERE id = ?;
            """);
            stmt.setDouble(1, price);
            stmt.setLong(2, id);
            int affects = stmt.executeUpdate();
            if (affects == 0) {
                throw new SQLException("Failed to update the book with id: " + id);
            }
        }
    }

    public List<Book> getTop5LatestBooksWithStaleRead(Integer seconds) throws SQLException {
        List<Book> books = new ArrayList<>();
        try (Connection conn = ds.getConnection()) {
            PreparedStatement stmt = conn.prepareStatement("""
            SELECT id, title, type, price FROM books AS OF TIMESTAMP NOW() - INTERVAL ? SECOND ORDER BY published_at DESC LIMIT 5;
            """);
            stmt.setInt(1, seconds);
            ResultSet rs = stmt.executeQuery();
            while (rs.next()) {
                Book book = new Book();
                book.setId(rs.getLong("id"));
                book.setTitle(rs.getString("title"));
                book.setType(rs.getString("type"));
                book.setPrice(rs.getDouble("price"));
                books.add(book);
            }
        } catch (SQLException e) {
            if ("HY000".equals(e.getSQLState()) && e.getErrorCode() == 1105) {
                System.out.println("WARN: cannot set read timestamp to a future time.");
            } else if ("HY000".equals(e.getSQLState()) && e.getErrorCode() == 9006) {
                System.out.println("WARN: GC life time is shorter than transaction duration.");
            } else {
                throw e;
            }
        }
        return books;
    }
}
```

```java
List<Book> top5LatestBooks = bookDAO.getTop5LatestBooks();

if (top5LatestBooks.size() > 0) {
    System.out.println("The latest book price (before update): " + top5LatestBooks.get(0).getPrice());

    Book book = top5LatestBooks.get(0);
    bookDAO.updateBookPriceByID(book.getId(), book.price + 10);

    top5LatestBooks = bookDAO.getTop5LatestBooks();
    System.out.println("The latest book price (after update): " + top5LatestBooks.get(0).getPrice());

    // 使用历史读取
    top5LatestBooks = bookDAO.getTop5LatestBooksWithStaleRead(5);
    System.out.println("The latest book price (maybe stale): " + top5LatestBooks.get(0).getPrice());

    // 尝试读取未来时间的数据
    bookDAO.getTop5LatestBooksWithStaleRead(-5);

    // 尝试读取 20 分钟前的数据
    bookDAO.getTop5LatestBooksWithStaleRead(20 * 60);
}
```

以下结果显示历史读取返回的价格是 100.00，这是更新前的值。

```
The latest book price (before update): 100.00
The latest book price (after update): 150.00
The latest book price (maybe stale): 100.00
WARN: cannot set read timestamp to a future time.
WARN: GC life time is shorter than transaction duration.
```

</div>
</SimpleTab>

## 事务级别

使用 `START TRANSACTION READ ONLY AS OF TIMESTAMP` 语句，您可以基于历史时间启动一个只读事务，该事务从指定的历史时间戳读取历史数据。

<SimpleTab groupId="language">
<div label="SQL" value="sql">

例如：

```sql
START TRANSACTION READ ONLY AS OF TIMESTAMP NOW() - INTERVAL 5 SECOND;
```

通过查询图书的最新价格，您可以看到《The Story of Droolius Caesar》的价格仍然是 100.0，这是更新前的值。

```sql
SELECT id, title, type, price FROM books ORDER BY published_at DESC LIMIT 5;
```

结果如下：

```
+------------+------------------------------+-----------------------+--------+
| id         | title                        | type                  | price  |
+------------+------------------------------+-----------------------+--------+
| 3181093216 | The Story of Droolius Caesar | Novel                 | 100.00 |
| 1064253862 | Collin Rolfson               | Education & Reference |  92.85 |
| 1748583991 | The Documentary of cat       | Magazine              | 159.75 |
|  893930596 | Myrl Hills                   | Education & Reference | 356.85 |
| 3062833277 | Keven Wyman                  | Life                  | 477.91 |
+------------+------------------------------+-----------------------+--------+
5 rows in set (0.01 sec)
```

在使用 `COMMIT;` 语句提交事务后，您可以读取最新数据。

```
+------------+------------------------------+-----------------------+--------+
| id         | title                        | type                  | price  |
+------------+------------------------------+-----------------------+--------+
| 3181093216 | The Story of Droolius Caesar | Novel                 | 150.00 |
| 1064253862 | Collin Rolfson               | Education & Reference |  92.85 |
| 1748583991 | The Documentary of cat       | Magazine              | 159.75 |
|  893930596 | Myrl Hills                   | Education & Reference | 356.85 |
| 3062833277 | Keven Wyman                  | Life                  | 477.91 |
+------------+------------------------------+-----------------------+--------+
5 rows in set (0.01 sec)
```

</div>
<div label="Java" value="java">

您可以定义一个事务的辅助类，该类将在事务级别启用历史读取的命令封装为辅助方法。

```java
public static class StaleReadHelper {

    public static void startTxnWithStaleRead(Connection conn, Integer seconds) throws SQLException {
        conn.setAutoCommit(false);
        PreparedStatement stmt = conn.prepareStatement(
            "START TRANSACTION READ ONLY AS OF TIMESTAMP NOW() - INTERVAL ? SECOND;"
        );
        stmt.setInt(1, seconds);
        stmt.execute();
    }

}
```

然后在 `BookDAO` 类中定义一个方法，通过事务启用历史读取功能。使用该方法进行查询，而不是在查询语句中添加 `AS OF TIMESTAMP`。

```java
public class BookDAO {

    // 省略部分代码...

    public List<Book> getTop5LatestBooksWithTxnStaleRead(Integer seconds) throws SQLException {
        List<Book> books = new ArrayList<>();
        try (Connection conn = ds.getConnection()) {
            // 启动只读事务
            TxnHelper.startTxnWithStaleRead(conn, seconds);

            Statement stmt = conn.createStatement();
            ResultSet rs = stmt.executeQuery("""
            SELECT id, title, type, price FROM books ORDER BY published_at DESC LIMIT 5;
            """);
            while (rs.next()) {
                Book book = new Book();
                book.setId(rs.getLong("id"));
                book.setTitle(rs.getString("title"));
                book.setType(rs.getString("type"));
                book.setPrice(rs.getDouble("price"));
                books.add(book);
            }

            // 提交事务
            conn.commit();
        } catch (SQLException e) {
            if ("HY000".equals(e.getSQLState()) && e.getErrorCode() == 1105) {
                System.out.println("WARN: cannot set read timestamp to a future time.");
            } else if ("HY000".equals(e.getSQLState()) && e.getErrorCode() == 9006) {
                System.out.println("WARN: GC life time is shorter than transaction duration.");
            } else {
                throw e;
            }
        }
        return books;
    }
}
```

```java
List<Book> top5LatestBooks = bookDAO.getTop5LatestBooks();

if (top5LatestBooks.size() > 0) {
    System.out.println("The latest book price (before update): " + top5LatestBooks.get(0).getPrice());

    Book book = top5LatestBooks.get(0);
    bookDAO.updateBookPriceByID(book.getId(), book.price + 10);

    top5LatestBooks = bookDAO.getTop5LatestBooks();
    System.out.println("The latest book price (after update): " + top5LatestBooks.get(0).getPrice());

    // 使用历史读取
    top5LatestBooks = bookDAO.getTop5LatestBooksWithTxnStaleRead(5);
    System.out.println("The latest book price (maybe stale): " + top5LatestBooks.get(0).getPrice());

    // 在历史读取事务提交后
    top5LatestBooks = bookDAO.getTop5LatestBooks();
    System.out.println("The latest book price (after the transaction commit): " + top5LatestBooks.get(0).getPrice());
}
```

结果如下：

```
The latest book price (before update): 100.00
The latest book price (after update): 150.00
The latest book price (maybe stale): 100.00
The latest book price (after the transaction commit): 150
```

</div>
</SimpleTab>

使用 `SET TRANSACTION READ ONLY AS OF TIMESTAMP` 语句，您可以将已打开的事务或下一个事务设置为基于指定历史时间的只读事务。该事务将基于提供的历史时间读取历史数据。

<SimpleTab groupId="language">
<div label="SQL" value="sql">

例如，您可以使用以下 `AS OF TIMESTAMP` 语句将正在进行的事务切换到只读模式，并读取 5 秒前的历史数据。

```sql
SET TRANSACTION READ ONLY AS OF TIMESTAMP NOW() - INTERVAL 5 SECOND;
```

</div>
<div label="Java" value="java">

您可以定义一个事务的辅助类，该类将在事务级别启用历史读取的命令封装为辅助方法。

```java
public static class TxnHelper {

    public static void setTxnWithStaleRead(Connection conn, Integer seconds) throws SQLException {
        PreparedStatement stmt = conn.prepareStatement(
            "SET TRANSACTION READ ONLY AS OF TIMESTAMP NOW() - INTERVAL ? SECOND;"
        );
        stmt.setInt(1, seconds);
        stmt.execute();
    }

}
```

然后在 `BookDAO` 类中定义一个方法，通过事务启用历史读取功能。使用该方法进行查询，而不是在查询语句中添加 `AS OF TIMESTAMP`。

```java
public class BookDAO {

    // 省略部分代码...

    public List<Book> getTop5LatestBooksWithTxnStaleRead2(Integer seconds) throws SQLException {
        List<Book> books = new ArrayList<>();
        try (Connection conn = ds.getConnection()) {
            StaleReadHelper.setTxnWithStaleRead(conn, seconds);

            // 启动只读事务
            conn.setAutoCommit(false);

            Statement stmt = conn.createStatement();
            ResultSet rs = stmt.executeQuery("""
            SELECT id, title, type, price FROM books ORDER BY published_at DESC LIMIT 5;
            """);
            while (rs.next()) {
                Book book = new Book();
                book.setId(rs.getLong("id"));
                book.setTitle(rs.getString("title"));
                book.setType(rs.getString("type"));
                book.setPrice(rs.getDouble("price"));
                books.add(book);
            }

            // 提交事务
            conn.commit();
        } catch (SQLException e) {
            if ("HY000".equals(e.getSQLState()) && e.getErrorCode() == 1105) {
                System.out.println("WARN: cannot set read timestamp to a future time.");
            } else if ("HY000".equals(e.getSQLState()) && e.getErrorCode() == 9006) {
                System.out.println("WARN: GC life time is shorter than transaction duration.");
            } else {
                throw e;
            }
        }
        return books;
    }
}
```

</div>
</SimpleTab>

## 会话级别

为了支持读取历史数据，TiDB 从 v5.4 开始引入了一个新的系统变量 `tidb_read_staleness`。您可以使用它来设置当前会话允许读取的历史数据范围。其数据类型为 `int`，作用域为 `SESSION`。

<SimpleTab groupId="language">
<div label="SQL" value="sql">

在会话中启用历史读取：

```sql
SET @@tidb_read_staleness="-5";
```

例如，如果值设置为 `-5`，并且 TiKV 或 TiFlash 有相应的历史数据，TiDB 会在 5 秒时间范围内选择一个尽可能新的时间戳。

在会话中禁用历史读取：

```sql
set @@tidb_read_staleness="";
```

</div>
<div label="Java" value="java">

```java
public static class StaleReadHelper{

    public static void enableStaleReadOnSession(Connection conn, Integer seconds) throws SQLException {
        PreparedStatement stmt = conn.prepareStatement(
            "SET @@tidb_read_staleness= ?;"
        );
        stmt.setString(1, String.format("-%d", seconds));
        stmt.execute();
    }

    public static void disableStaleReadOnSession(Connection conn) throws SQLException {
        PreparedStatement stmt = conn.prepareStatement(
            "SET @@tidb_read_staleness=\"\";"
        );
        stmt.execute();
    }

}
```

</div>
</SimpleTab>

## 阅读更多

- [历史读取的使用场景](/stale-read.md)
- [使用 `AS OF TIMESTAMP` 子句读取历史数据](/as-of-timestamp.md)
- [使用 `tidb_read_staleness` 系统变量读取历史数据](/tidb-read-staleness.md)

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上询问社区，或[提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上询问社区，或[提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>
