---
title: Stale Read
summary: Learn how to use Stale Read to accelerate queries under certain conditions.
---

# Stale Read

Stale Read is a mechanism that TiDB applies to read historical versions of data stored in TiDB. Using this mechanism, you can read the corresponding historical data at a specific time or within a specified time range, and thus save the latency caused by data replication between storage nodes. When you are using Steal Read, TiDB randomly selects a replica for data reading, which means that all replicas are available for data reading.

In practice, consider carefully whether it is appropriate to enable Stale Read in TiDB based on the [usage scenarios](/stale-read.md#usage-scenarios-of-stale-read). Do not enable Stale Read if your application cannot tolerate reading non-real-time data.

TiDB provides three levels of Stale Read: statement level, transaction level, and session level.

## Introduction

In the [Bookshop](/develop/dev-guide-bookshop-schema-design.md) application, you can query the latest published books and their prices through the following SQL statement:

```sql
SELECT id, title, type, price FROM books ORDER BY published_at DESC LIMIT 5;
```

The result is as follows:

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

In the list at this time (2022-04-20 15:20:00), the price of *The Story of Droolius Caesar* is 100.0.

At the same time, the seller found that the book was very popular and raised the price of the book to 150.0 through the following SQL statement:

```sql
UPDATE books SET price = 150 WHERE id = 3181093216;
```

The result is as follows:

```
Query OK, 1 row affected (0.00 sec)
Rows matched: 1  Changed: 1  Warnings: 0
```

By querying the latest books list, you can see that the price of this book has increased.

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

If it is not necessary to use the latest data, you can query with Stale Read, which might return outdated data, to avoid the latency caused by data replication during a strongly consistent read.

Assuming that in the Bookshop application, the real-time price of a book is not required on the book lists page but only required on the book details and order pages. Stale Read can be used to improve throughout of the application.

## Statement level

<SimpleTab groupId="language">
<div label="SQL" value="sql">

To query the price of a book before a specific time, add an `AS OF TIMESTAMP <datetime>` clause in the above query statement.

```sql
SELECT id, title, type, price FROM books AS OF TIMESTAMP '2022-04-20 15:20:00' ORDER BY published_at DESC LIMIT 5;
```

The result is as follows:

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

In addition to specifying an exact time, you can also specify the following:

- `AS OF TIMESTAMP NOW() - INTERVAL 10 SECOND` queries the latest data 10 seconds ago.
- `AS OF TIMESTAMP TIDB_BOUNDED_STALENESS('2016-10-08 16:45:26', '2016-10-08 16:45:29')` queries the latest data between `2016-10-08 16:45:26` and `2016-10-08 16:45:29`.
- `AS OF TIMESTAMP TIDB_BOUNDED_STALENESS(NOW() -INTERVAL 20 SECOND, NOW())` queries the latest data within 20 seconds.

Note that the specified timestamp or interval cannot be too early or later than the current time.

Expired data will be recycled by [Garbage Collection](/garbage-collection-overview.md) in TiDB, and the data will be retained for a short period before being cleared. The period is called [GC Life Time (default 10 minutes)](/system-variables.md#tidb_gc_life_time-new-in-v50). When a GC starts, the current time minus the time period will be used as the **GC Safe Point**. If you try to read the data before GC Safe Point, TiDB will report the following error:

```
ERROR 9006 (HY000): GC life time is shorter than transaction duration...
```

If the given timestamp is a future time, TiDB will report the following error:

```
ERROR 9006 (HY000): cannot set read timestamp to a future time.
```

</div>
<div label="Java" value="java">

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

The following result shows that the price returned by Stale Read is 100.00, which is the value before the update.

```
The latest book price (before update): 100.00
The latest book price (after update): 150.00
The latest book price (maybe stale): 100.00
WARN: cannot set read timestamp to a future time.
WARN: GC life time is shorter than transaction duration.
```

</div>
</SimpleTab>

## Transaction level

With the `START TRANSACTION READ ONLY AS OF TIMESTAMP` statement, you can start a read-only transaction based on historical time, which reads historical data from a specified historical timestamp.

<SimpleTab groupId="language">
<div label="SQL" value="sql">

For example:

```sql
START TRANSACTION READ ONLY AS OF TIMESTAMP NOW() - INTERVAL 5 SECOND;
```

By querying the latest price of the book, you can see that the price of *The Story of Droolius Caesar* is still 100.0, which is the value before the update.

```sql
SELECT id, title, type, price FROM books ORDER BY published_at DESC LIMIT 5;
```

The result is as follows:

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

After the transaction with the `COMMIT;` statement is committed, you can read the latest data.

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

You can define a helper class for transactions, which encapsulates the command to enable Stale Read at the transaction level as a helper method.

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

Then define a method to enable the Stale Read feature through a transaction in the `BookDAO` class. Use the method to query instead of adding `AS OF TIMESTAMP` to the query statement.

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

The result is as follows:

```
The latest book price (before update): 100.00
The latest book price (after update): 150.00
The latest book price (maybe stale): 100.00
The latest book price (after the transaction commit): 150
```

</div>
</SimpleTab>

With the `SET TRANSACTION READ ONLY AS OF TIMESTAMP` statement, you can set the opened transaction or the next transaction to be a read-only transaction based on a specified historical time. The transaction will read historical data based on the provided historical time.

<SimpleTab groupId="language">
<div label="SQL" value="sql">

For example, you can use the following `AS OF TIMESTAMP` statement to switch the ongoing transactions to the read-only mode and read historical data 5 seconds ago.

```sql
SET TRANSACTION READ ONLY AS OF TIMESTAMP NOW() - INTERVAL 5 SECOND;
```

</div>
<div label="Java" value="java">

You can define a helper class for transactions, which encapsulates the command to enable Stale Read at the transaction level as a helper method.

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

Then define a method to enable the Stale Read feature through a transaction in the `BookDAO` class. Use the method to query instead of adding `AS OF TIMESTAMP` to the query statement.

```java
public class BookDAO {

    // Omit some code...

    public List<Book> getTop5LatestBooksWithTxnStaleRead2(Integer seconds) throws SQLException {
        List<Book> books = new ArrayList<>();
        try (Connection conn = ds.getConnection()) {
            StaleReadHelper.setTxnWithStaleRead(conn, seconds);

            // Start a read only transaction.
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

## Session level

To support reading historical data, TiDB has introduced a new system variable `tidb_read_staleness` since v5.4. you can use it to set the range of historical data that the current session is allowed to read. Its data type is `int` and its scope is `SESSION`.

<SimpleTab groupId="language">
<div label="SQL" value="sql">

Enable Stale Read in a session:

```sql
SET @@tidb_read_staleness="-5";
```

For example, if the value is set to `-5` and TiKV or TiFlash has the corresponding historical data, TiDB selects a timestamp as new as possible within a 5-second time range.

Disable Stale Read in the session:

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

## Read more

- [Usage Scenarios of Stale Read](/stale-read.md)
- [Read Historical Data Using the `AS OF TIMESTAMP` Clause](/as-of-timestamp.md)
- [Read Historical Data Using the `tidb_read_staleness` System Variable](/tidb-read-staleness.md)
