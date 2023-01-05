---
title: Multi-table Join Queries
summary: This document describes how to use multi-table join queries.
---

# Multi-table Join Queries

In many scenarios, you need to use one query to get data from multiple tables. You can use the `JOIN` statement to combine the data from two or more tables.

## Join types

This section describes the Join types in detail.

### INNER JOIN

The join result of an inner join returns only rows that match the join condition.

![Inner Join](/media/develop/inner-join.png)

For example, if you want to know the most prolific author, you need to join the author table named `authors` with the book author table named `book_authors`.

<SimpleTab groupId="language">
<div label="SQL" value="sql">

In the following SQL statement, use the keyword `JOIN` to declare that you want to join the rows of the left table `authors` and the right table `book_authors` as an inner join with the join condition `a.id = ba.author_id`. The result set will only contain rows that satisfy the join condition. If an author has not written any books, then his record in `authors` table will not satisfy the join condition and will therefore not appear in the result set.

```sql
SELECT ANY_VALUE(a.id) AS author_id, ANY_VALUE(a.name) AS author_name, COUNT(ba.book_id) AS books
FROM authors a
JOIN book_authors ba ON a.id = ba.author_id
GROUP BY ba.author_id
ORDER BY books DESC
LIMIT 10;
```

The query results are as follows:

```
+------------+----------------+-------+
| author_id  | author_name    | books |
+------------+----------------+-------+
|  431192671 | Emilie Cassin  |     7 |
|  865305676 | Nola Howell    |     7 |
|  572207928 | Lamar Koch     |     6 |
| 3894029860 | Elijah Howe    |     6 |
| 1150614082 | Cristal Stehr  |     6 |
| 4158341032 | Roslyn Rippin  |     6 |
| 2430691560 | Francisca Hahn |     6 |
| 3346415350 | Leta Weimann   |     6 |
| 1395124973 | Albin Cole     |     6 |
| 2768150724 | Caleb Wyman    |     6 |
+------------+----------------+-------+
10 rows in set (0.01 sec)
```

</div>
<div label="Java" value="java">

```java
public List<Author> getTop10AuthorsOrderByBooks() throws SQLException {
    List<Author> authors = new ArrayList<>();
    try (Connection conn = ds.getConnection()) {
        Statement stmt = conn.createStatement();
        ResultSet rs = stmt.executeQuery("""
        SELECT ANY_VALUE(a.id) AS author_id, ANY_VALUE(a.name) AS author_name, COUNT(ba.book_id) AS books
        FROM authors a
        JOIN book_authors ba ON a.id = ba.author_id
        GROUP BY ba.author_id
        ORDER BY books DESC
        LIMIT 10;
        """);
        while (rs.next()) {
            Author author = new Author();
            author.setId(rs.getLong("author_id"));
            author.setName(rs.getString("author_name"));
            author.setBooks(rs.getInt("books"));
            authors.add(author);
        }
    }
    return authors;
}
```

</div>
</SimpleTab>

### LEFT OUTER JOIN

The left outer join returns all the rows in the left table and the values ​​in the right table that match the join condition. If no rows are matched in the right table, it will be filled with `NULL`.

![Left Outer Join](/media/develop/left-outer-join.png)

In some cases, you want to use multiple tables to complete the data query, but do not want the data set to become too small because the join condition are not met.

For example, on the homepage of the Bookshop app, you want to display a list of new books with average ratings. In this case, the new books may not have been rated by anyone yet. Using inner joins will cause the information of these unrated books to be filtered out, which is not what you expect.

<SimpleTab groupId="language">
<div label="SQL" value="sql">

In the following SQL statement, use the `LEFT JOIN` keyword to declare that the left table `books` will be joined to the right table `ratings` in a left outer join, thus ensuring that all rows in the `books` table are returned.

```sql
SELECT b.id AS book_id, ANY_VALUE(b.title) AS book_title, AVG(r.score) AS average_score
FROM books b
LEFT JOIN ratings r ON b.id = r.book_id
GROUP BY b.id
ORDER BY b.published_at DESC
LIMIT 10;
```

The query results are as follows:

```
+------------+---------------------------------+---------------+
| book_id    | book_title                      | average_score |
+------------+---------------------------------+---------------+
| 3438991610 | The Documentary of lion         |        2.7619 |
| 3897175886 | Torey Kuhn                      |        3.0000 |
| 1256171496 | Elmo Vandervort                 |        2.5500 |
| 1036915727 | The Story of Munchkin           |        2.0000 |
|  270254583 | Tate Kovacek                    |        2.5000 |
| 1280950719 | Carson Damore                   |        3.2105 |
| 1098041838 | The Documentary of grasshopper  |        2.8462 |
| 1476566306 | The Adventures of Vince Sanford |        2.3529 |
| 4036300890 | The Documentary of turtle       |        2.4545 |
| 1299849448 | Antwan Olson                    |        3.0000 |
+------------+---------------------------------+---------------+
10 rows in set (0.30 sec)
```

It seems that the latest published book already has a lot of ratings. To verify the above method, let's delete all the ratings of the book _The Documentary of lion_ through the SQL statement:

```sql
DELETE FROM ratings WHERE book_id = 3438991610;
```

Query again. The book _The Documentary of lion_ still appears in the result set, but the `average_score` column calculated from `score` of the right table `ratings` is filled with `NULL`.

```
+------------+---------------------------------+---------------+
| book_id    | book_title                      | average_score |
+------------+---------------------------------+---------------+
| 3438991610 | The Documentary of lion         |          NULL |
| 3897175886 | Torey Kuhn                      |        3.0000 |
| 1256171496 | Elmo Vandervort                 |        2.5500 |
| 1036915727 | The Story of Munchkin           |        2.0000 |
|  270254583 | Tate Kovacek                    |        2.5000 |
| 1280950719 | Carson Damore                   |        3.2105 |
| 1098041838 | The Documentary of grasshopper  |        2.8462 |
| 1476566306 | The Adventures of Vince Sanford |        2.3529 |
| 4036300890 | The Documentary of turtle       |        2.4545 |
| 1299849448 | Antwan Olson                    |        3.0000 |
+------------+---------------------------------+---------------+
10 rows in set (0.30 sec)
```

What happens if you use `INNER JOIN`? It's up to you to have a try.

</div>
<div label="Java" value="java">

```java
public List<Book> getLatestBooksWithAverageScore() throws SQLException {
    List<Book> books = new ArrayList<>();
    try (Connection conn = ds.getConnection()) {
        Statement stmt = conn.createStatement();
        ResultSet rs = stmt.executeQuery("""
        SELECT b.id AS book_id, ANY_VALUE(b.title) AS book_title, AVG(r.score) AS average_score
        FROM books b
        LEFT JOIN ratings r ON b.id = r.book_id
        GROUP BY b.id
        ORDER BY b.published_at DESC
        LIMIT 10;
        """);
        while (rs.next()) {
            Book book = new Book();
            book.setId(rs.getLong("book_id"));
            book.setTitle(rs.getString("book_title"));
            book.setAverageScore(rs.getFloat("average_score"));
            books.add(book);
        }
    }
    return books;
}
```

</div>
</SimpleTab>

### RIGHT OUTER JOIN

A right outer join returns all the records in the right table and the values ​​in the left table that match the join condition. If there is no matching value, it is filled with `NULL`.

![Right Outer Join](/media/develop/right-outer-join.png)

### CROSS JOIN

When the join condition is constant, the inner join between the two tables is called a [cross join](https://en.wikipedia.org/wiki/Join_(SQL)#Cross_join). A cross join joins every record of the left table to all the records of the right table. If the number of records in the left table is `m` and the number of records in the right table is `n`, then `m \* n` records will be generated in the result set.

### LEFT SEMI JOIN

TiDB does not support `LEFT SEMI JOIN table_name` at the SQL syntax level. But at the execution plan level, [subquery-related optimizations](/subquery-optimization.md) will use `semi join` as the default join method for rewritten equivalent JOIN queries.

## Implicit join

Before the `JOIN` statement that explicitly declared a join was added to the SQL standard, it was possible to join two or more tables in a SQL statement using the `FROM t1, t2` clause, and specify the conditions for the join using the `WHERE t1.id = t2.id` clause. You can understand it as an implicit join, which uses the inner join to join tables.

## Join related algorithms

TiDB supports the following general table join algorithms.

- [Index Join](/explain-joins.md#index-join)
- [Hash Join](/explain-joins.md#hash-join)
- [Merge Join](/explain-joins.md#merge-join)

The optimizer selects an appropriate join algorithm to execute based on the factors such as the data volume in the joined table. You can see which algorithm the query uses for Join by using the `EXPLAIN` statement.

If the optimizer of TiDB does not execute according to the optimal join algorithm, you can use [Optimizer Hints](/optimizer-hints.md) to force TiDB to use a better join algorithm.

For example, assuming the example for the left join query above executes faster using the Hash Join algorithm, which is not chosen by the optimizer, you can append the hint `/*+ HASH_JOIN(b, r) */` after the `SELECT` keyword. Note that If the table has an alias, use the alias in the hint.

```sql
EXPLAIN SELECT /*+ HASH_JOIN(b, r) */ b.id AS book_id, ANY_VALUE(b.title) AS book_title, AVG(r.score) AS average_score
FROM books b
LEFT JOIN ratings r ON b.id = r.book_id
GROUP BY b.id
ORDER BY b.published_at DESC
LIMIT 10;
```

Hints related to join algorithms:

- [MERGE_JOIN(t1_name [, tl_name ...])](/optimizer-hints.md#merge_joint1_name--tl_name-)
- [INL_JOIN(t1_name [, tl_name ...])](/optimizer-hints.md#inl_joint1_name--tl_name-)
- [INL_HASH_JOIN(t1_name [, tl_name ...])](/optimizer-hints.md#inl_hash_join)
- [HASH_JOIN(t1_name [, tl_name ...])](/optimizer-hints.md#hash_joint1_name--tl_name-)

## Join orders

In real business scenarios, join statements of multiple tables are very common. The execution efficiency of join is related to the order of each table in join. TiDB uses the Join Reorder algorithm to determine the order in which multiple tables are joined.

If the join order selected by the optimizer is not optimal as expected, you can use `STRAIGHT_JOIN` to enforce TiDB to join queries in the order of the tables used in the `FROM` clause.

```sql
EXPLAIN SELECT *
FROM authors a STRAIGHT_JOIN book_authors ba STRAIGHT_JOIN books b
WHERE b.id = ba.book_id AND ba.author_id = a.id;
```

For more information about the implementation details and limitations of this Join Reorder algorithm, see [Introduction to Join Reorder Algorithm](/join-reorder.md).

## See also

- [Explain Statements That Use Joins](/explain-joins.md)
- [Introduction to Join Reorder](/join-reorder.md)
