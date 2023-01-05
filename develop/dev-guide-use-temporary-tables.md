---
title: Temporary Tables
summary: Learn how to create, view, query, and delete temporary tables.
---

# Temporary Tables

Temporary tables can be thought of as a technique for reusing query results.

If you want to know something about the eldest authors in the [Bookshop](/develop/dev-guide-bookshop-schema-design.md) application, you might write multiple queries that use the list of eldest authors.

For example, you can use the following statement to get the top 50 eldest authors from the `authors` table:

```sql
SELECT a.id, a.name, (IFNULL(a.death_year, YEAR(NOW())) - a.birth_year) AS age
FROM authors a
ORDER BY age DESC
LIMIT 50;
```

The result is as follows:

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

For the convenience of subsequent queries, you need to cache the result of this query. When using general tables for storage, you should pay attention to how to avoid the table name duplication problem between different sessions, and the need of cleaning up intermediate results in time, as these tables might not be used after a batch query.

## Create a temporary table

To cache intermediate results, the temporary tables feature is introduced in TiDB v5.3.0. TiDB automatically drops a local temporary table after a session ends, which frees you from worrying about the management trouble caused by increasing intermediate results.

### Types of temporary tables

Temporary tables in TiDB are divided into two types: local temporary tables and global temporary tables.

- For a local temporary table, the table definition and data in the table are visible only to the current session. This type is suitable for temporarily storing intermediate data in the session.
- For a global temporary table, the table definition is visible to the entire TiDB cluster, and the data in the table is visible only to the current transaction. This type is suitable for temporarily storing intermediate data in a transaction.

### Create a local temporary table

Before creating a local temporary table, you need to add `CREATE TEMPORARY TABLES` permission to the current database user.

<SimpleTab groupId="language">
<div label="SQL" value="sql">

You can create a temporary table using the `CREATE TEMPORARY TABLE <table_name>` statement. The default type is a local temporary table, which is visible only to the current session.

```sql
CREATE TEMPORARY TABLE top_50_eldest_authors (
    id BIGINT,
    name VARCHAR(255),
    age INT,
    PRIMARY KEY(id)
);
```

After creating the temporary table, you can use the `INSERT INTO table_name SELECT ...` statement to insert the results of the above query into the temporary table you just created.

```sql
INSERT INTO top_50_eldest_authors
SELECT a.id, a.name, (IFNULL(a.death_year, YEAR(NOW())) - a.birth_year) AS age
FROM authors a
ORDER BY age DESC
LIMIT 50;
```

The result is as follows:

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

### Create a global temporary table

<SimpleTab groupId="language">
<div label="SQL" value="sql">

To create a global temporary table, you can add the `GLOBAL` keyword and end with `ON COMMIT DELETE ROWS`, which means the table will be deleted after the current transaction ends.

```sql
CREATE GLOBAL TEMPORARY TABLE IF NOT EXISTS top_50_eldest_authors_global (
    id BIGINT,
    name VARCHAR(255),
    age INT,
    PRIMARY KEY(id)
) ON COMMIT DELETE ROWS;
```

When inserting data to global temporary tables, you must explicitly declare the start of the transaction via `BEGIN`. Otherwise, the data will be cleared after the `INSERT INTO` statement is executed. Because in the Auto Commit mode, the transaction is automatically committed after the `INSERT INTO` statement is executed, and the global temporary table is cleared when the transaction ends.

</div>
<div label="Java" value="java">

When using global temporary tables, you need to turn off Auto Commit mode first. In Java, you can do this with the `conn.setAutoCommit(false);` statement, and you can commit the transaction explicitly with `conn.commit();`. The data added to the global temporary table during the transaction will be cleared after the transaction is committed or canceled.

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

## View temporary tables

With the `SHOW [FULL] TABLES` statement, you can view a list of existing global temporary tables, but you cannot see any local temporary tables in the list. For now, TiDB does not have a similar `information_schema.INNODB_TEMP_TABLE_INFO` system table for storing temporary table information.

For example, you can see the global temporary table `top_50_eldest_authors_global` in the table list, but not the `top_50_eldest_authors` table.

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

## Query a temporary table

Once the temporary table is ready, you can query it as a normal data table:

```sql
SELECT * FROM top_50_eldest_authors;
```

You can reference data from temporary tables to your query via [Multi-table join queries](/develop/dev-guide-join-tables.md):

```sql
EXPLAIN SELECT ANY_VALUE(ta.id) AS author_id, ANY_VALUE(ta.age), ANY_VALUE(ta.name), COUNT(*) AS books
FROM top_50_eldest_authors ta
LEFT JOIN book_authors ba ON ta.id = ba.author_id
GROUP BY ta.id;
```

Different from [view](/develop/dev-guide-use-views.md), querying a temporary table gets data directly from the temporary table instead of executing the original query used in the data insert. In some cases, this can improve the query performance.

## Drop a temporary table

A local temporary table in a session is automatically dropped after the **session** ends, along with both data and table schema. A global temporary table in a transaction is automatically cleared at the end of the **transaction**, but the table schema remains and needs to be deleted manually.

To manually drop local temporary tables, use the `DROP TABLE` or `DROP TEMPORARY TABLE` syntax. For example:

```sql
DROP TEMPORARY TABLE top_50_eldest_authors;
```

To manually drop global temporary tables, use the `DROP TABLE` or `DROP GLOBAL TEMPORARY TABLE` syntax. For example:

```sql
DROP GLOBAL TEMPORARY TABLE top_50_eldest_authors_global;
```

## Limitation

For limitations of temporary tables in TiDB, see [Compatibility restrictions with other TiDB features](/temporary-tables.md#compatibility-restrictions-with-other-tidb-features).

## Read more

- [Temporary Tables](/temporary-tables.md)
