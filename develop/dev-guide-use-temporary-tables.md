---
title: 临时表
summary: 介绍 TiDB 临时表创建、删除、限制。
---

# 临时表

临时表可以被认为是一种复用查询结果的技术。

假设希望知道 [Bookshop](/develop/dev-guide-bookshop-schema-design.md) 应用当中最年长的作家们的一些情况，可能需要编写多个查询，而这些查询都需要使用到这个最年长作家列表。可以通过下面的 SQL 语句从 `authors` 表当中找出最年长的前 50 位作家作为研究对象。

```sql
SELECT a.id, a.name, (IFNULL(a.death_year, YEAR(NOW())) - a.birth_year) AS age
FROM authors a
ORDER BY age DESC
LIMIT 50;
```

查询结果如下：

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

在找到这 50 位最年长的作家后，希望缓存这个查询结果，以便后续的查询能够方便地使用到这组数据。如果使用一般的数据库表进行存储的话，在创建这些表时，需要考虑如何避免不同会话之间的表重名问题，而且可能在一批查询结束之后就不再需要这些表了，还需要及时地对这些中间结果表进行清理。

## 创建临时表

为了满足这类缓存中间结果的需求，TiDB 在 v5.3.0 版本中引入了临时表功能，对于临时表当中的本地临时表而言，TiDB 将会在会话结束的一段时间后自动清理这些已经没用的临时表，用户无需担心中间结果表的增多会带来管理上的麻烦。

### 临时表类型

TiDB 的临时表分为本地临时表和全局临时表：

- 本地临时表的表定义和表内数据只对当前会话可见，适用于暂存会话内的中间数据。
- 全局临时表的表定义对整个 TiDB 集群可见，表内数据只对当前事务可见，适用于暂存事务内的中间数据。

### 创建本地临时表

在创建本地临时表前，你需要给当前数据库用户添加上 `CREATE TEMPORARY TABLES` 权限。

<SimpleTab groupId="language">
<div label="SQL" value="sql">

在 SQL 中，通过 `CREATE TEMPORARY TABLE <table_name>` 语句创建临时表，默认临时表的类型为本地临时表，它只能被当前会话所访问。

```sql
CREATE TEMPORARY TABLE top_50_eldest_authors (
    id BIGINT,
    name VARCHAR(255),
    age INT,
    PRIMARY KEY(id)
);
```

在创建完临时表后，你可以通过 `INSERT INTO table_name SELECT ...` 语句，将上述查询得到的结果导入到刚刚创建的临时表当中。

```sql
INSERT INTO top_50_eldest_authors
SELECT a.id, a.name, (IFNULL(a.death_year, YEAR(NOW())) - a.birth_year) AS age
FROM authors a
ORDER BY age DESC
LIMIT 50;
```

运行结果为：

```
Query OK, 50 rows affected (0.03 sec)
Records: 50  Duplicates: 0  Warnings: 0
```

</div>
<div label="Java" value="java">

在 Java 中创建本地临时表的示例如下：

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

在 SQL 中，你可以通过加上 `GLOBAL` 关键字来声明你所创建的是全局临时表。创建全局临时表时必须在末尾 `ON COMMIT DELETE ROWS` 修饰，这表明该全局数据表的所有数据行将在事务结束后被删除。

```sql
CREATE GLOBAL TEMPORARY TABLE IF NOT EXISTS top_50_eldest_authors_global (
    id BIGINT,
    name VARCHAR(255),
    age INT,
    PRIMARY KEY(id)
) ON COMMIT DELETE ROWS;
```

在对全局临时表导入数据时，你需要特别注意，你必须通过 `BEGIN` 显式声明事务的开始。否则导入的数据在 `INSERT INTO` 语句执行后就清除掉，因为 Auto Commit 模式下，`INSERT INTO` 语句的执行结束，事务会自动被提交，事务结束，全局临时表的数据便被清空了。

</div>
<div label="Java" value="java">

在 Java 中使用全局临时表时，你需要将 Auto Commit 模式先关闭。在 Java 语言当中，你可以通过 `conn.setAutoCommit(false);` 语句来实现，当你使用完成后，可以通过 `conn.commit();` 显式地提交事务。事务在提交或取消后，在事务过程中对全局临时表添加的数据将会被清除。

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

## 查看临时表信息

通过 `SHOW [FULL] TABLES` 语句可以查看到已经创建的全局临时表，但是无法看到本地临时表的信息，TiDB 暂时也没有类似的 `information_schema.INNODB_TEMP_TABLE_INFO` 系统表存放临时表的信息。

例如，你可以在 table 列表当中查看到全局临时表 `top_50_eldest_authors_global`，但是无法查看到 `top_50_eldest_authors` 表。

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

在临时表准备就绪之后，你便可以像对一般数据表一样对临时表进行查询：

```sql
SELECT * FROM top_50_eldest_authors;
```

你可以通过[表连接](/develop/dev-guide-join-tables.md)将临时表中的数据引用到你的查询当中：

```sql
EXPLAIN SELECT ANY_VALUE(ta.id) AS author_id, ANY_VALUE(ta.age), ANY_VALUE(ta.name), COUNT(*) AS books
FROM top_50_eldest_authors ta
LEFT JOIN book_authors ba ON ta.id = ba.author_id
GROUP BY ta.id;
```

与[视图](/develop/dev-guide-use-views.md)有所不同，在对临时表进行查询时，不会再执行导入数据时所使用的原始查询，而是直接从临时表中获取数据。在一些情况下，这会帮助你提高查询的效率。

## 删除临时表

本地临时表会在**会话**结束后连同数据和表结构都进行自动清理。全局临时表在**事务**结束后会自动清除数据，但是表结构依然保留，需要手动删除。

你可以通过 `DROP TABLE` 或 `DROP TEMPORARY TABLE` 语句手动删除**本地临时表**。例如：

```sql
DROP TEMPORARY TABLE top_50_eldest_authors;
```

你还可以通过 `DROP TABLE` 或 `DROP GLOBAL TEMPORARY TABLE` 语句手动删除**全局临时表**。例如：

```sql
DROP GLOBAL TEMPORARY TABLE top_50_eldest_authors_global;
```

## 限制

关于 TiDB 在临时表功能上的一些限制，你可以通过阅读参考文档中的[临时表与其他 TiDB 功能的兼容性限制](/temporary-tables.md#与其他-tidb-功能的兼容性限制)小节进行了解。

## 扩展阅读

- [临时表](/temporary-tables.md)