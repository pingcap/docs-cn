---
title: Stale Read
summary: 使用 Stale Read 在特定情况下加速查询。
aliases: ['/zh/tidb/dev/use-stale-read','/zh/tidb/stable/dev-guide-use-stale-read/','/zh/tidb/dev/dev-guide-use-stale-read/','/zh/tidbcloud/dev-guide-use-stale-read/']
---

# Stale Read

Stale Read 是一种读取历史数据版本的机制，通过 Stale Read 功能，你能从指定时间点或时间范围内读取对应的历史数据，从而在数据强一致需求没那么高的场景降低读取数据的延迟。当使用 Stale Read 时，TiDB 默认会随机选择一个副本来读取数据，因此能利用所有保存有副本的节点的处理能力。

在实际的使用当中，请根据具体的[场景](/stale-read.md#场景描述)判断是否适合在 TiDB 当中开启 Stale Read 功能。如果你的应用程序不能容忍读到非实时的数据，请勿使用 Stale Read，否则读到的数据可能不是最新成功写入的数据。

TiDB 提供了语句级别、事务级别、会话级别三种级别的 Stale Read 功能，接下来将逐一进行介绍：

## 引入

在 [Bookshop](/develop/dev-guide-bookshop-schema-design.md) 应用程序当中，你可以通过下面的 SQL 语句查询出最新出版的书籍以及它们的价格：

```sql
SELECT id, title, type, price FROM books ORDER BY published_at DESC LIMIT 5;
```

运行结果为：

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

看到此时（2022-04-20 15:20:00）的列表中，**The Story of Droolius Caesar** 这本小说的价格为 100.0 元。

于此同时，卖家发现这本书很受欢迎，于是他通过下面的 SQL 语句将这本书的价格高到了 150.0 元。

```sql
UPDATE books SET price = 150 WHERE id = 3181093216;
```

运行结果为：

```
Query OK, 1 row affected (0.00 sec)
Rows matched: 1  Changed: 1  Warnings: 0
```

当再次查询最新书籍列表时，发现这本书确实涨价了。

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

如果不要求必须使用最新的数据，可以让 TiDB 通过 Stale Read 功能直接返回可能已经过期的历史数据，避免使用强一致性读时数据同步带来的延迟。

假设在 Bookshop 应用程序当中，在用户浏览书籍列表页时，不对书籍价格的实时性进行要求，只有用户在点击查看书籍详情页或下单时才去获取实时的价格信息，可以借助 Stale Read 能力来进一步提升应用的吞吐量。

## 语句级别

<SimpleTab groupId="language">
<div label="SQL" value="sql">

在 SQL 中，你可以在上述价格的查询语句当中添加上 `AS OF TIMESTAMP <datetime>` 语句查看到固定时间点之前这本书的价格。

```sql
SELECT id, title, type, price FROM books AS OF TIMESTAMP '2022-04-20 15:20:00' ORDER BY published_at DESC LIMIT 5;
```

运行结果为：

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

除了指定精确的时间点外，你还可以通过：

- `AS OF TIMESTAMP NOW() - INTERVAL 10 SECOND` 表示读取 10 秒前最新的数据。
- `AS OF TIMESTAMP TIDB_BOUNDED_STALENESS('2016-10-08 16:45:26', '2016-10-08 16:45:29')` 表示读取在 2016 年 10 月 8 日 16 点 45 分 26 秒到 29 秒的时间范围内尽可能新的数据。
- `AS OF TIMESTAMP TIDB_BOUNDED_STALENESS(NOW() - INTERVAL 20 SECOND, NOW())` 表示读取 20 秒前到现在的时间范围内尽可能新的数据。

需要注意的是，设定的时间戳或时间戳的范围不能过早或晚于当前时间。此外 `NOW()` 默认精确到秒，当精度要求较高时，需要添加参数，例如 `NOW(3)` 精确到毫秒。详情请参考 [MySQL 文档](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_now)。

过期的数据在 TiDB 当中会由[垃圾回收器](/garbage-collection-overview.md)进行回收，数据在被清除之前会被保留一小段时间，这段时间被称为 [GC Life Time (默认 10 分钟)](/system-variables.md#tidb_gc_life_time-从-v50-版本开始引入)。每次进行 GC 时，将以当前时间减去该时间周期的值作为 **GC Safe Point**。如果尝试读取 GC Safe Point 之前数据，TiDB 会报如下错误：

```
ERROR 9006 (HY000): GC life time is shorter than transaction duration...
```

如果给出的时间戳是一个未来的时间节点，TiDB 会报如下错误：

```
ERROR 9006 (HY000): cannot set read timestamp to a future time.
```

</div>
<div label="Java" value="java">

在 Java 中的示例如下：

```java
public class BookDAO {

    // Omit some code...

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

    // Use the stale read.
    top5LatestBooks = bookDAO.getTop5LatestBooksWithStaleRead(5);
    System.out.println("The latest book price (maybe stale): " + top5LatestBooks.get(0).getPrice());

    // Try to stale read the data at the future time.
    bookDAO.getTop5LatestBooksWithStaleRead(-5);

    // Try to stale read the data before 20 minutes.
    bookDAO.getTop5LatestBooksWithStaleRead(20 * 60);
}
```

通过结果可以看到通过 Stale Read 读取到了更新之前的价格 100.00 元。

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

通过 `START TRANSACTION READ ONLY AS OF TIMESTAMP` 语句，你可以开启一个基于历史时间的只读事务，该事务基于所提供的历史时间来读取历史数据。

<SimpleTab groupId="language">
<div label="SQL" value="sql">

在 SQL 中的示例如下：

```sql
START TRANSACTION READ ONLY AS OF TIMESTAMP NOW() - INTERVAL 5 SECOND;
```

尝试通过 SQL 查询最新书籍的价格，发现 **The Story of Droolius Caesar** 这本书的价格还是更新之前的价格 100.0 元。

```sql
SELECT id, title, type, price FROM books ORDER BY published_at DESC LIMIT 5;
```

运行结果为：

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

随后通过 `COMMIT;` 语句提交事务，当事务结束后，又可以重新读取到最新数据：

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

在 Java 中，可以先定义一个事务的工具类，将开启事务级别 Stale Read 的命令封装成工具方法。

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

然后在 `BookDAO` 类当中定义一个通过事务开启 Stale Read 功能的方法，在方法内查询最新的书籍列表，但是不再在查询语句中添加 `AS OF TIMESTAMP`。

```java
public class BookDAO {

    // Omit some code...

    public List<Book> getTop5LatestBooksWithTxnStaleRead(Integer seconds) throws SQLException {
        List<Book> books = new ArrayList<>();
        try (Connection conn = ds.getConnection()) {
            // Start a read only transaction.
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

            // Commit transaction.
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

    // Use the stale read.
    top5LatestBooks = bookDAO.getTop5LatestBooksWithTxnStaleRead(5);
    System.out.println("The latest book price (maybe stale): " + top5LatestBooks.get(0).getPrice());

    // After the stale read transaction is committed.
    top5LatestBooks = bookDAO.getTop5LatestBooks();
    System.out.println("The latest book price (after the transaction commit): " + top5LatestBooks.get(0).getPrice());
}
```

输出结果：

```
The latest book price (before update): 100.00
The latest book price (after update): 150.00
The latest book price (maybe stale): 100.00
The latest book price (after the transaction commit): 150
```

</div>
</SimpleTab>

通过 `SET TRANSACTION READ ONLY AS OF TIMESTAMP` 语句，你可以将当前事务或下一个事务设置为基于指定历史时间的只读事务。该事务将会基于所提供的历史时间来读取历史数据。

<SimpleTab groupId="language">
<div label="SQL" value="sql">

例如，可以通过下面这个 SQL 将已开启的事务切换到只读模式，通过 `AS OF TIMESTAMP` 语句开启能够读取 5 秒前的历史数据 Stale Read 功能。

```sql
SET TRANSACTION READ ONLY AS OF TIMESTAMP NOW() - INTERVAL 5 SECOND;
```

</div>
<div label="Java" value="java">

可以先定义一个事务的工具类，将开启事务级别 Stale Read 的命令封装成工具方法。

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

然后在 `BookDAO` 类当中定义一个通过事务开启 Stale Read 功能的方法，在方法内查询最新的书籍列表，但是不再在查询语句中添加 `AS OF TIMESTAMP`。

```java
public class BookDAO {

    // Omit some code...

    public List<Book> getTop5LatestBooksWithTxnStaleRead2(Integer seconds) throws SQLException {
        List<Book> books = new ArrayList<>();
        try (Connection conn = ds.getConnection()) {
            // Start a read only transaction.
            conn.setAutoCommit(false);
            StaleReadHelper.setTxnWithStaleRead(conn, seconds);

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

            // Commit transaction.
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

为支持读取历史版本数据，TiDB 从 5.4 版本起引入了一个新的系统变量 `tidb_read_staleness`。系统变量 `tidb_read_staleness` 用于设置当前会话允许读取的历史数据范围，其数据类型为 int，作用域为 SESSION。

<SimpleTab groupId="language">
<div label="SQL" value="sql">

在会话中开启 Stale Read：

```sql
SET @@tidb_read_staleness="-5";
```

比如，如果该变量的值设置为 -5，TiDB 会在 5 秒时间范围内，保证 TiKV 或者 TiFlash 拥有对应历史版本数据的情况下，选择尽可能新的一个时间戳。

关闭会话当中的 Stale Read：

```sql
set @@tidb_read_staleness="";
```

</div>
<div label="Java" value="java">

在 Java 中示例如下：

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

## 扩展阅读

- [Stale Read 功能的使用场景](/stale-read.md)
- [使用 AS OF TIMESTAMP 语法读取历史数据](/as-of-timestamp.md#语法方式)
- [通过系统变量 tidb_read_staleness 读取历史数据](/tidb-read-staleness.md)
