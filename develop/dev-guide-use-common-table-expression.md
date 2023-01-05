---
title: Common Table Expression
summary: Learn the CTE feature of TiDB, which help you write SQL statements more efficiently.
---

# Common Table Expression

In some transaction scenarios, due to application complexity, you might need to write a single SQL statement of up to 2,000 lines. The statement probably contains a lot of aggregations and multi-level subquery nesting. Maintaining such a long SQL statement can be a developer's nightmare.

To avoid such a long SQL statement, you can simplify queries by using [Views](/develop/dev-guide-use-views.md) or cache intermediate query results by using [Temporary tables](/develop/dev-guide-use-temporary-tables.md).

This document introduces the Common Table Expression (CTE) syntax in TiDB, which is a more convenient way to reuse query results.

Since TiDB v5.1, TiDB supports the CTE of the ANSI SQL99 standard and recursion. With CTE, you can write SQL statements for complex application logic more efficiently and maintain the code much easier.

## Basic use

A Common Table Expression (CTE) is a temporary result set that can be referred to multiple times within a SQL statement to improve the statement readability and execution efficiency. You can apply the `WITH` statement to use CTE.

Common Table Expressions can be classified into two types: non-recursive CTE and recursive CTE.

### Non-recursive CTE

Non-recursive CTE can be defined using the following syntax:

```sql
WITH <query_name> AS (
    <query_definition>
)
SELECT ... FROM <query_name>;
```

For example, if you want to know how many books each of the 50 oldest authors have written, take the following steps:

<SimpleTab groupId="language">
<div label="SQL" value="sql">

Change the statement in [temporary tables](/develop/dev-guide-use-temporary-tables.md) to the following:

```sql
WITH top_50_eldest_authors_cte AS (
    SELECT a.id, a.name, (IFNULL(a.death_year, YEAR(NOW())) - a.birth_year) AS age
    FROM authors a
    ORDER BY age DESC
    LIMIT 50
)
SELECT
    ANY_VALUE(ta.id) AS author_id,
    ANY_VALUE(ta.age) AS author_age,
    ANY_VALUE(ta.name) AS author_name,
    COUNT(*) AS books
FROM top_50_eldest_authors_cte ta
LEFT JOIN book_authors ba ON ta.id = ba.author_id
GROUP BY ta.id;
```

The result is as follows:

```
+------------+------------+---------------------+-------+
| author_id  | author_age | author_name         | books |
+------------+------------+---------------------+-------+
| 1238393239 |         80 | Araceli Purdy       |     1 |
|  817764631 |         80 | Ivory Davis         |     3 |
| 3093759193 |         80 | Lysanne Harris      |     1 |
| 2299112019 |         80 | Ray Macejkovic      |     4 |
...
+------------+------------+---------------------+-------+
50 rows in set (0.01 sec)
```

</div>
<div label="Java" value = "java">

```java
public List<Author> getTop50EldestAuthorInfoByCTE() throws SQLException {
    List<Author> authors = new ArrayList<>();
    try (Connection conn = ds.getConnection()) {
        Statement stmt = conn.createStatement();
        ResultSet rs = stmt.executeQuery("""
            WITH top_50_eldest_authors_cte AS (
                SELECT a.id, a.name, (IFNULL(a.death_year, YEAR(NOW())) - a.birth_year) AS age
                FROM authors a
                ORDER BY age DESC
                LIMIT 50
            )
            SELECT
                ANY_VALUE(ta.id) AS author_id,
                ANY_VALUE(ta.name) AS author_name,
                ANY_VALUE(ta.age) AS author_age,
                COUNT(*) AS books
            FROM top_50_eldest_authors_cte ta
            LEFT JOIN book_authors ba ON ta.id = ba.author_id
            GROUP BY ta.id;
        """);
        while (rs.next()) {
            Author author = new Author();
            author.setId(rs.getLong("author_id"));
            author.setName(rs.getString("author_name"));
            author.setAge(rs.getShort("author_age"));
            author.setBooks(rs.getInt("books"));
            authors.add(author);
        }
    }
    return authors;
}
```

</div>
</SimpleTab>

It can be found that the author "Ray Macejkovic" wrote 4 books. With the CTE query, you can further get the order and rating information of these 4 books as follows:

```sql
WITH books_authored_by_rm AS (
    SELECT *
    FROM books b
    LEFT JOIN book_authors ba ON b.id = ba.book_id
    WHERE author_id = 2299112019
), books_with_average_ratings AS (
    SELECT
        b.id AS book_id,
        AVG(r.score) AS average_rating
    FROM books_authored_by_rm b
    LEFT JOIN ratings r ON b.id = r.book_id
    GROUP BY b.id
), books_with_orders AS (
    SELECT
        b.id AS book_id,
        COUNT(*) AS orders
    FROM books_authored_by_rm b
    LEFT JOIN orders o ON b.id = o.book_id
    GROUP BY b.id
)
SELECT
    b.id AS `book_id`,
    b.title AS `book_title`,
    br.average_rating AS `average_rating`,
    bo.orders AS `orders`
FROM
    books_authored_by_rm b
    LEFT JOIN books_with_average_ratings br ON b.id = br.book_id
    LEFT JOIN books_with_orders bo ON b.id = bo.book_id
;
```

The result is as follows:

```
+------------+-------------------------+----------------+--------+
| book_id    | book_title              | average_rating | orders |
+------------+-------------------------+----------------+--------+
|  481008467 | The Documentary of goat |         2.0000 |     16 |
| 2224531102 | Brandt Skiles           |         2.7143 |     17 |
| 2641301356 | Sheridan Bashirian      |         2.4211 |     12 |
| 4154439164 | Karson Streich          |         2.5833 |     19 |
+------------+-------------------------+----------------+--------+
4 rows in set (0.06 sec)
```

Three CTE blocks, which are separated by `,`, are defined in this SQL statement.

First, check out the books written by the author (ID is `2299112019`) in the CTE block `books_authored_by_rm`. Then find the average rating and order for these books respectively in `books_with_average_ratings` and `books_with_orders`. Finally, aggregate the results by the `JOIN` statement.

Note that the query in `books_authored_by_rm` executes only once, and then TiDB creates a temporary space to cache its result. When the queries in `books_with_average_ratings` and `books_with_orders` refer to `books_authored_by_rm`, TiDB gets its result directly from this temporary space.

> **Tip:**
>
> If the efficiency of the default CTE queries is not good, you can use the [`MERGE()`](/optimizer-hints.md#merge) hint to expand the CTE subquery to the outer query to improve the efficiency.

### Recursive CTE

Recursive CTE can be defined using the following syntax:

```sql
WITH RECURSIVE <query_name> AS (
    <query_definition>
)
SELECT ... FROM <query_name>;
```

A classic example is to generate a set of [Fibonacci numbers](https://en.wikipedia.org/wiki/Fibonacci_number) with recursive CTE:

```sql
WITH RECURSIVE fibonacci (n, fib_n, next_fib_n) AS
(
  SELECT 1, 0, 1
  UNION ALL
  SELECT n + 1, next_fib_n, fib_n + next_fib_n FROM fibonacci WHERE n < 10
)
SELECT * FROM fibonacci;
```

The result is as follows:

```
+------+-------+------------+
| n    | fib_n | next_fib_n |
+------+-------+------------+
|    1 |     0 |          1 |
|    2 |     1 |          1 |
|    3 |     1 |          2 |
|    4 |     2 |          3 |
|    5 |     3 |          5 |
|    6 |     5 |          8 |
|    7 |     8 |         13 |
|    8 |    13 |         21 |
|    9 |    21 |         34 |
|   10 |    34 |         55 |
+------+-------+------------+
10 rows in set (0.00 sec)
```

## Read more

- [WITH](/sql-statements/sql-statement-with.md)
