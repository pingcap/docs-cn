---
title: 公共表表达式 (CTE)
summary: 介绍 TiDB 公共表表达式能力，用以简化 SQL。
aliases: ['/zh/tidb/dev/use-common-table-expression','/zh/tidb/stable/dev-guide-use-common-table-expression/','/zh/tidb/dev/dev-guide-use-common-table-expression/','/zh/tidbcloud/dev-guide-use-common-table-expression/']
---

# 公共表表达式 (CTE)

由于业务的客观复杂性，有时候会写出长达 2000 行的单条 SQL 语句，其中包含大量的聚合和多层子查询嵌套，维护此类 SQL 堪称开发人员的噩梦。

在前面的小节当中已经介绍了如何使用[视图](/develop/dev-guide-use-views.md)简化查询，也介绍了如何使用[临时表](/develop/dev-guide-use-temporary-tables.md)来缓存中间查询结果。

在这一小节当中，将介绍 TiDB 当中的公共表表达式（CTE）语法，它是一种更加便捷的复用查询结果的方法。

TiDB 从 5.1 版本开始支持 ANSI SQL 99 标准的 CTE 及其递归的写法，极大提升开发人员和 DBA 编写复杂业务逻辑 SQL 的效率，增强代码的可维护性。

## 基本使用

公共表表达式 (CTE) 是一个临时的中间结果集，能够在 SQL 语句中引用多次，提高 SQL 语句的可读性与执行效率。在 TiDB 中可以通过 [`WITH`](/sql-statements/sql-statement-with.md) 语句使用公共表表达式。

公共表表达式可以分为非递归和递归两种类型。

### 非递归的 CTE

非递归的 CTE 使用如下语法进行定义：

```sql
WITH <query_name> AS (
    <query_definition>
)
SELECT ... FROM <query_name>;
```

例如，假设还想知道最年长的 50 位作家分别编写过多少书籍。

<SimpleTab>
<div label="SQL">

在 SQL 中，可以将[临时表](/develop/dev-guide-use-temporary-tables.md)小节当中的例子改为以下 SQL 语句：

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

查询结果如下：

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
<div label="Java">

在 Java 中的示例如下：

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

这时，可以发现名为 “Ray Macejkovic” 的作者写了 4 本书，继续通过 CTE 查询来了解这 4 本书的销量和评分：

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

查询结果如下：

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

在这个 SQL 语句，定义了三个 CTE 块，CTE 块之间使用 `,` 进行分隔。

先在 CTE 块 `books_authored_by_rm` 当中将该作者（作者 ID 为 `2299112019`）所编写的书查出来，然后在 `books_with_average_ratings` 和 `books_with_orders` 中分别查出这些书的平均评分和订单数，最后通过 `JOIN` 语句进行汇总。

值得注意的是，`books_authored_by_rm` 中的查询只会执行一次，TiDB 会开辟一块临时空间对查询的结果进行缓存，当 `books_with_average_ratings` 和 `books_with_orders` 引用时会直接从该临时空间当中获取数据。

> **建议：**
>
> 当默认的 CTE 查询执行效率不高时，你可以使用 [`MERGE()`](/optimizer-hints.md#merge) hint，将 CTE 子查询拓展到外部查询，以此提高执行效率。

### 递归的 CTE

递归的公共表表达式可以使用如下语法进行定义：

```sql
WITH RECURSIVE <query_name> AS (
    <query_definition>
)
SELECT ... FROM <query_name>;
```

比较经典的例子是通过递归的 CTE 生成一组[斐波那契数](https://zh.wikipedia.org/wiki/%E6%96%90%E6%B3%A2%E9%82%A3%E5%A5%91%E6%95%B0)：

```sql
WITH RECURSIVE fibonacci (n, fib_n, next_fib_n) AS
(
  SELECT 1, 0, 1
  UNION ALL
  SELECT n + 1, next_fib_n, fib_n + next_fib_n FROM fibonacci WHERE n < 10
)
SELECT * FROM fibonacci;
```

查询结果如下：

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

## 扩展阅读

- [WITH](/sql-statements/sql-statement-with.md)
