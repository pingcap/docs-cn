---
title: 多表联接查询
summary: 本文介绍如何使用多表联接查询。
---

# 多表联接查询

在许多场景中，你需要使用一个查询从多个表中获取数据。你可以使用 `JOIN` 语句来组合来自两个或多个表的数据。

## 联接类型

本节详细介绍联接类型。

### INNER JOIN

内联接的联接结果仅返回满足联接条件的行。

![Inner Join](/media/develop/inner-join.png)

例如，如果你想知道最多产的作者，你需要将名为 `authors` 的作者表与名为 `book_authors` 的图书作者表联接起来。

<SimpleTab groupId="language">
<div label="SQL" value="sql">

在以下 SQL 语句中，使用关键字 `JOIN` 声明你要将左表 `authors` 和右表 `book_authors` 的行作为内联接进行联接，联接条件为 `a.id = ba.author_id`。结果集将只包含满足联接条件的行。如果一个作者没有写过任何书，那么他在 `authors` 表中的记录将不满足联接条件，因此不会出现在结果集中。

```sql
SELECT ANY_VALUE(a.id) AS author_id, ANY_VALUE(a.name) AS author_name, COUNT(ba.book_id) AS books
FROM authors a
JOIN book_authors ba ON a.id = ba.author_id
GROUP BY ba.author_id
ORDER BY books DESC
LIMIT 10;
```

查询结果如下：

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

左外联接返回左表中的所有行以及右表中满足联接条件的值。如果在右表中没有匹配的行，将用 `NULL` 填充。

![Left Outer Join](/media/develop/left-outer-join.png)

在某些情况下，你想使用多个表来完成数据查询，但不希望因为不满足联接条件而使数据集变得太小。

例如，在 Bookshop 应用的主页上，你想显示带有平均评分的新书列表。在这种情况下，新书可能还没有被任何人评分。使用内联接会导致这些未评分书籍的信息被过滤掉，这不是你期望的。

<SimpleTab groupId="language">
<div label="SQL" value="sql">

在以下 SQL 语句中，使用 `LEFT JOIN` 关键字声明左表 `books` 将以左外联接的方式与右表 `ratings` 联接，从而确保返回 `books` 表中的所有行。

```sql
SELECT b.id AS book_id, ANY_VALUE(b.title) AS book_title, AVG(r.score) AS average_score
FROM books b
LEFT JOIN ratings r ON b.id = r.book_id
GROUP BY b.id
ORDER BY b.published_at DESC
LIMIT 10;
```

查询结果如下：

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

看起来最新发布的书已经有很多评分了。为了验证上述方法，让我们通过 SQL 语句删除《The Documentary of lion》这本书的所有评分：

```sql
DELETE FROM ratings WHERE book_id = 3438991610;
```

再次查询。《The Documentary of lion》这本书仍然出现在结果集中，但从右表 `ratings` 的 `score` 计算得出的 `average_score` 列被填充为 `NULL`。

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

如果使用 `INNER JOIN` 会发生什么？你可以自己尝试一下。

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

右外联接返回右表中的所有记录以及左表中满足联接条件的值。如果没有匹配的值，则用 `NULL` 填充。

![Right Outer Join](/media/develop/right-outer-join.png)

### CROSS JOIN

当联接条件为常量时，两个表之间的内联接称为[交叉联接](https://en.wikipedia.org/wiki/Join_(SQL)#Cross_join)。交叉联接将左表的每条记录与右表的所有记录联接。如果左表中的记录数为 `m`，右表中的记录数为 `n`，则结果集中将生成 `m \* n` 条记录。

### LEFT SEMI JOIN

TiDB 在 SQL 语法级别不支持 `LEFT SEMI JOIN table_name`。但在执行计划级别，[子查询相关优化](/subquery-optimization.md)会使用 `semi join` 作为重写等价 JOIN 查询的默认联接方法。

## 隐式联接

在明确声明联接的 `JOIN` 语句被添加到 SQL 标准之前，可以使用 `FROM t1, t2` 子句在 SQL 语句中联接两个或多个表，并使用 `WHERE t1.id = t2.id` 子句指定联接条件。你可以将其理解为隐式联接，它使用内联接来联接表。

## 联接相关算法

TiDB 支持以下通用表联接算法。

- [Index Join](/explain-joins.md#index-join)
- [Hash Join](/explain-joins.md#hash-join)
- [Merge Join](/explain-joins.md#merge-join)

优化器会根据联接表中的数据量等因素选择合适的联接算法来执行。你可以使用 `EXPLAIN` 语句查看查询使用了哪种联接算法。

如果 TiDB 的优化器没有按照最优的联接算法执行，你可以使用[优化器提示](/optimizer-hints.md)强制 TiDB 使用更好的联接算法。

例如，假设上面的左联接查询示例使用 Hash Join 算法执行得更快，但优化器没有选择它，你可以在 `SELECT` 关键字后面添加提示 `/*+ HASH_JOIN(b, r) */`。注意，如果表有别名，在提示中使用别名。

```sql
EXPLAIN SELECT /*+ HASH_JOIN(b, r) */ b.id AS book_id, ANY_VALUE(b.title) AS book_title, AVG(r.score) AS average_score
FROM books b
LEFT JOIN ratings r ON b.id = r.book_id
GROUP BY b.id
ORDER BY b.published_at DESC
LIMIT 10;
```

与联接算法相关的提示：

- [MERGE_JOIN(t1_name [, tl_name ...])](/optimizer-hints.md#merge_joint1_name--tl_name-)
- [INL_JOIN(t1_name [, tl_name ...])](/optimizer-hints.md#inl_joint1_name--tl_name-)
- [INL_HASH_JOIN(t1_name [, tl_name ...])](/optimizer-hints.md#inl_hash_join)
- [HASH_JOIN(t1_name [, tl_name ...])](/optimizer-hints.md#hash_joint1_name--tl_name-)

## 联接顺序

在实际业务场景中，多表联接语句非常常见。联接的执行效率与每个表在联接中的顺序有关。TiDB 使用联接重排算法来确定多个表联接的顺序。

如果优化器选择的联接顺序不是最优的，你可以使用 `STRAIGHT_JOIN` 强制 TiDB 按照 `FROM` 子句中使用的表的顺序进行联接查询。

```sql
EXPLAIN SELECT *
FROM authors a STRAIGHT_JOIN book_authors ba STRAIGHT_JOIN books b
WHERE b.id = ba.book_id AND ba.author_id = a.id;
```

有关此联接重排算法的实现细节和限制的更多信息，请参阅[联接重排算法简介](/join-reorder.md)。

## 另请参阅

- [使用联接的语句的执行计划](/explain-joins.md)
- [联接重排简介](/join-reorder.md)

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上询问社区，或[提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上询问社区，或[提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>
