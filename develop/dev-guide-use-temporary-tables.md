---
title: 临时表
summary: 了解如何创建、查看、查询和删除临时表。
---

# 临时表

临时表可以被视为重用查询结果的一种技术。

如果您想了解 [Bookshop](/develop/dev-guide-bookshop-schema-design.md) 应用程序中年龄最大的作者的相关信息，您可能会编写多个使用年龄最大作者列表的查询。

例如，您可以使用以下语句从 `authors` 表中获取年龄最大的前 50 位作者：

```sql
SELECT a.id, a.name, (IFNULL(a.death_year, YEAR(NOW())) - a.birth_year) AS age
FROM authors a
ORDER BY age DESC
LIMIT 50;
```

结果如下：

```
+------------+---------------------+------+
| id         | name                | age  |
+------------+---------------------+------+
| 4053452056 | Dessie Thompson     |   80 |
| 2773958689 | Pedro Hansen        |   80 |
| 4005636688 | Wyatt Keeling       |   80 |
| 3621155838 | Colby Parker        |   80 |
| 2738876051 | Friedrich Hagenes   |   80 |
| 2299112019 | Ray Macejkovic      |   80 |
| 3953661843 | Brandi Williamson   |   80 |
...
| 4100546410 | Maida Walsh         |   80 |
+------------+---------------------+------+
50 rows in set (0.01 sec)
```

为了便于后续查询，您需要缓存此查询的结果。当使用普通表进行存储时，您应该注意如何避免不同会话之间的表名重复问题，以及需要及时清理中间结果，因为这些表在批量查询后可能不会再被使用。

## 创建临时表

为了缓存中间结果，TiDB v5.3.0 引入了临时表功能。TiDB 会在会话结束后自动删除本地临时表，这使您不必担心中间结果增加带来的管理麻烦。

### 临时表的类型

TiDB 中的临时表分为两种类型：本地临时表和全局临时表。

- 对于本地临时表，表定义和表中的数据仅对当前会话可见。这种类型适合临时存储会话中的中间数据。
- 对于全局临时表，表定义对整个 TiDB 集群可见，而表中的数据仅对当前事务可见。这种类型适合临时存储事务中的中间数据。

### 创建本地临时表

在创建本地临时表之前，您需要为当前数据库用户添加 `CREATE TEMPORARY TABLES` 权限。

<SimpleTab groupId="language">
<div label="SQL" value="sql">

您可以使用 `CREATE TEMPORARY TABLE <table_name>` 语句创建临时表。默认类型是本地临时表，仅对当前会话可见。

```sql
CREATE TEMPORARY TABLE top_50_eldest_authors (
    id BIGINT,
    name VARCHAR(255),
    age INT,
    PRIMARY KEY(id)
);
```

创建临时表后，您可以使用 `INSERT INTO table_name SELECT ...` 语句将上述查询的结果插入到刚刚创建的临时表中。

```sql
INSERT INTO top_50_eldest_authors
SELECT a.id, a.name, (IFNULL(a.death_year, YEAR(NOW())) - a.birth_year) AS age
FROM authors a
ORDER BY age DESC
LIMIT 50;
```

结果如下：

```
Query OK, 50 rows affected (0.03 sec)
Records: 50  Duplicates: 0  Warnings: 0
```

</div>
<div label="Java" value="java">

```java
public List<Author> getTop50EldestAuthorInfo() throws SQLException {
    List<Author> authors = new ArrayList<>();
    try (Connection conn = ds.getConnection()) {
        Statement stmt = conn.createStatement();
        stmt.executeUpdate("""
            CREATE TEMPORARY TABLE top_50_eldest_authors (
                id BIGINT,
                name VARCHAR(255),
                age INT,
                PRIMARY KEY(id)
            );
        """);

        stmt.executeUpdate("""
            INSERT INTO top_50_eldest_authors
            SELECT a.id, a.name, (IFNULL(a.death_year, YEAR(NOW())) - a.birth_year) AS age
            FROM authors a
            ORDER BY age DESC
            LIMIT 50;
        """);

        ResultSet rs = stmt.executeQuery("""
            SELECT id, name FROM top_50_eldest_authors;
        """);

        while (rs.next()) {
            Author author = new Author();
            author.setId(rs.getLong("id"));
            author.setName(rs.getString("name"));
            authors.add(author);
        }
    }
    return authors;
}
```

</div>
</SimpleTab>

### 创建全局临时表

<SimpleTab groupId="language">
<div label="SQL" value="sql">

要创建全局临时表，您可以添加 `GLOBAL` 关键字并以 `ON COMMIT DELETE ROWS` 结尾，这表示表将在当前事务结束后被删除。

```sql
CREATE GLOBAL TEMPORARY TABLE IF NOT EXISTS top_50_eldest_authors_global (
    id BIGINT,
    name VARCHAR(255),
    age INT,
    PRIMARY KEY(id)
) ON COMMIT DELETE ROWS;
```

向全局临时表插入数据时，必须通过 `BEGIN` 显式声明事务的开始。否则，数据将在 `INSERT INTO` 语句执行后被清除。因为在自动提交模式下，事务会在 `INSERT INTO` 语句执行后自动提交，而全局临时表会在事务结束时被清除。

</div>
<div label="Java" value="java">

使用全局临时表时，您需要先关闭自动提交模式。在 Java 中，您可以使用 `conn.setAutoCommit(false);` 语句来实现，并可以使用 `conn.commit();` 显式提交事务。事务期间添加到全局临时表的数据将在事务提交或取消后被清除。

```java
public List<Author> getTop50EldestAuthorInfo() throws SQLException {
    List<Author> authors = new ArrayList<>();
    try (Connection conn = ds.getConnection()) {
        conn.setAutoCommit(false);

        Statement stmt = conn.createStatement();
        stmt.executeUpdate("""
            CREATE GLOBAL TEMPORARY TABLE IF NOT EXISTS top_50_eldest_authors (
                id BIGINT,
                name VARCHAR(255),
                age INT,
                PRIMARY KEY(id)
            ) ON COMMIT DELETE ROWS;
        """);

        stmt.executeUpdate("""
            INSERT INTO top_50_eldest_authors
            SELECT a.id, a.name, (IFNULL(a.death_year, YEAR(NOW())) - a.birth_year) AS age
            FROM authors a
            ORDER BY age DESC
            LIMIT 50;
        """);

        ResultSet rs = stmt.executeQuery("""
            SELECT id, name FROM top_50_eldest_authors;
        """);

        conn.commit();
        while (rs.next()) {
            Author author = new Author();
            author.setId(rs.getLong("id"));
            author.setName(rs.getString("name"));
            authors.add(author);
        }
    }
    return authors;
}
```

</div>
</SimpleTab>

## 查看临时表

使用 `SHOW [FULL] TABLES` 语句，您可以查看现有的全局临时表列表，但在列表中看不到任何本地临时表。目前，TiDB 没有类似 `information_schema.INNODB_TEMP_TABLE_INFO` 的系统表来存储临时表信息。

例如，您可以在表列表中看到全局临时表 `top_50_eldest_authors_global`，但看不到 `top_50_eldest_authors` 表。

```
+-------------------------------+------------+
| Tables_in_bookshop            | Table_type |
+-------------------------------+------------+
| authors                       | BASE TABLE |
| book_authors                  | BASE TABLE |
| books                         | BASE TABLE |
| orders                        | BASE TABLE |
| ratings                       | BASE TABLE |
| top_50_eldest_authors_global  | BASE TABLE |
| users                         | BASE TABLE |
+-------------------------------+------------+
9 rows in set (0.00 sec)
```

## 查询临时表

临时表准备就绪后，您可以像查询普通数据表一样查询它：

```sql
SELECT * FROM top_50_eldest_authors;
```

您可以通过[多表联接查询](/develop/dev-guide-join-tables.md)在查询中引用临时表中的数据：

```sql
EXPLAIN SELECT ANY_VALUE(ta.id) AS author_id, ANY_VALUE(ta.age), ANY_VALUE(ta.name), COUNT(*) AS books
FROM top_50_eldest_authors ta
LEFT JOIN book_authors ba ON ta.id = ba.author_id
GROUP BY ta.id;
```

与[视图](/develop/dev-guide-use-views.md)不同，查询临时表时直接从临时表获取数据，而不是执行用于数据插入的原始查询。在某些情况下，这可以提高查询性能。

## 删除临时表

会话中的本地临时表在**会话**结束后会自动删除，包括数据和表结构。事务中的全局临时表在**事务**结束时会自动清除数据，但表结构保留，需要手动删除。

要手动删除本地临时表，请使用 `DROP TABLE` 或 `DROP TEMPORARY TABLE` 语法。例如：

```sql
DROP TEMPORARY TABLE top_50_eldest_authors;
```

要手动删除全局临时表，请使用 `DROP TABLE` 或 `DROP GLOBAL TEMPORARY TABLE` 语法。例如：

```sql
DROP GLOBAL TEMPORARY TABLE top_50_eldest_authors_global;
```

## 限制

有关 TiDB 中临时表的限制，请参见[与其他 TiDB 功能的兼容性限制](/temporary-tables.md#compatibility-restrictions-with-other-tidb-features)。

## 阅读更多

- [临时表](/temporary-tables.md)

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上询问社区，或[提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上询问社区，或[提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>
