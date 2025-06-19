---
title: 从单个表中查询数据
summary: 本文档介绍如何从数据库的单个表中查询数据。
---

<!-- markdownlint-disable MD029 -->

# 从单个表中查询数据

本文档介绍如何使用 SQL 和各种编程语言从数据库的单个表中查询数据。

## 开始之前

以下内容以[书店](/develop/dev-guide-bookshop-schema-design.md)应用程序为例，展示如何从 TiDB 中的单个表查询数据。

在查询数据之前，请确保你已完成以下步骤：

<CustomContent platform="tidb">

1. 搭建 TiDB 集群（推荐使用 [TiDB Cloud](/develop/dev-guide-build-cluster-in-cloud.md) 或 [TiUP](/production-deployment-using-tiup.md)）。

</CustomContent>

<CustomContent platform="tidb-cloud">

1. 使用 [TiDB Cloud](/develop/dev-guide-build-cluster-in-cloud.md) 搭建 TiDB 集群。

</CustomContent>

2. [导入书店应用程序的表结构和示例数据](/develop/dev-guide-bookshop-schema-design.md#import-table-structures-and-data)。

<CustomContent platform="tidb">

3. [连接到 TiDB](/develop/dev-guide-connect-to-tidb.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

3. [连接到 TiDB](/tidb-cloud/connect-to-tidb-cluster.md)。

</CustomContent>

## 执行简单查询

在书店应用程序的数据库中，`authors` 表存储了作者的基本信息。你可以使用 `SELECT ... FROM ...` 语句从数据库中查询数据。

<SimpleTab groupId="language">
<div label="SQL" value="sql">

在 MySQL 客户端中执行以下 SQL 语句：

```sql
SELECT id, name FROM authors;
```

输出结果如下：

```
+------------+--------------------------+
| id         | name                     |
+------------+--------------------------+
|       6357 | Adelle Bosco             |
|     345397 | Chanelle Koepp           |
|     807584 | Clementina Ryan          |
|     839921 | Gage Huel                |
|     850070 | Ray Armstrong            |
|     850362 | Ford Waelchi             |
|     881210 | Jayme Gutkowski          |
|    1165261 | Allison Kuvalis          |
|    1282036 | Adela Funk               |
...
| 4294957408 | Lyla Nitzsche            |
+------------+--------------------------+
20000 rows in set (0.05 sec)
```

</div>
<div label="Java" value="java">

在 Java 中，要存储作者的基本信息，你可以声明一个 `Author` 类。你应该根据数据库中的[数据类型](/data-type-overview.md)和[取值范围](/data-type-numeric.md)选择适当的 Java 数据类型。例如：

- 使用 `Int` 类型的变量存储 `int` 类型的数据。
- 使用 `Long` 类型的变量存储 `bigint` 类型的数据。
- 使用 `Short` 类型的变量存储 `tinyint` 类型的数据。
- 使用 `String` 类型的变量存储 `varchar` 类型的数据。

```java
public class Author {
    private Long id;
    private String name;
    private Short gender;
    private Short birthYear;
    private Short deathYear;

    public Author() {}

     // 省略 getter 和 setter 方法。
}
```

```java
public class AuthorDAO {

    // 省略实例变量的初始化。

    public List<Author> getAuthors() throws SQLException {
        List<Author> authors = new ArrayList<>();

        try (Connection conn = ds.getConnection()) {
            Statement stmt = conn.createStatement();
            ResultSet rs = stmt.executeQuery("SELECT id, name FROM authors");
            while (rs.next()) {
                Author author = new Author();
                author.setId(rs.getLong("id"));
                author.setName(rs.getString("name"));
                authors.add(author);
            }
        }
        return authors;
    }
}
```

<CustomContent platform="tidb">

- 在[使用 JDBC 驱动程序连接到 TiDB](/develop/dev-guide-connect-to-tidb.md#jdbc) 之后，你可以使用 `conn.createStatus()` 创建一个 `Statement` 对象。

</CustomContent>

<CustomContent platform="tidb-cloud">

- 在[使用 JDBC 驱动程序连接到 TiDB](/develop/dev-guide-choose-driver-or-orm.md#java-drivers) 之后，你可以使用 `conn.createStatus()` 创建一个 `Statement` 对象。

</CustomContent>

- 然后调用 `stmt.executeQuery("query_sql")` 向 TiDB 发起数据库查询请求。
- 查询结果存储在 `ResultSet` 对象中。通过遍历 `ResultSet`，可以将返回的结果映射到 `Author` 对象。

</div>
</SimpleTab>

## 过滤结果

要过滤查询结果，你可以使用 `WHERE` 语句。

例如，以下命令查询所有作者中出生于 1998 年的作者：

<SimpleTab groupId="language">
<div label="SQL" value="sql">

在 `WHERE` 语句中添加过滤条件：

```sql
SELECT * FROM authors WHERE birth_year = 1998;
```

</div>
<div label="Java" value="java">

在 Java 中，你可以使用相同的 SQL 来处理带有动态参数的数据查询请求。

这可以通过将参数连接到 SQL 语句中来完成。但是，这种方法可能会给应用程序的安全性带来 [SQL 注入](https://en.wikipedia.org/wiki/SQL_injection)风险。

要处理此类查询，应使用[预处理语句](/develop/dev-guide-prepared-statement.md)而不是普通语句。

```java
public List<Author> getAuthorsByBirthYear(Short birthYear) throws SQLException {
    List<Author> authors = new ArrayList<>();
    try (Connection conn = ds.getConnection()) {
        PreparedStatement stmt = conn.prepareStatement("""
        SELECT * FROM authors WHERE birth_year = ?;
        """);
        stmt.setShort(1, birthYear);
        ResultSet rs = stmt.executeQuery();
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

## 排序结果

要对查询结果进行排序，你可以使用 `ORDER BY` 语句。

例如，以下 SQL 语句是通过按照 `birth_year` 列降序（`DESC`）排序 `authors` 表来获取最年轻作者的列表。

<SimpleTab groupId="language">
<div label="SQL" value="sql">

```sql
SELECT id, name, birth_year
FROM authors
ORDER BY birth_year DESC;
```

</div>

<div label="Java" value="java">

```java
public List<Author> getAuthorsSortByBirthYear() throws SQLException {
    List<Author> authors = new ArrayList<>();
    try (Connection conn = ds.getConnection()) {
        Statement stmt = conn.createStatement();
        ResultSet rs = stmt.executeQuery("""
            SELECT id, name, birth_year
            FROM authors
            ORDER BY birth_year DESC;
            """);

        while (rs.next()) {
            Author author = new Author();
            author.setId(rs.getLong("id"));
            author.setName(rs.getString("name"));
            author.setBirthYear(rs.getShort("birth_year"));
            authors.add(author);
        }
    }
    return authors;
}
```

</div>
</SimpleTab>

结果如下：

```
+-----------+------------------------+------------+
| id        | name                   | birth_year |
+-----------+------------------------+------------+
| 83420726  | Terrance Dach          | 2000       |
| 57938667  | Margarita Christiansen | 2000       |
| 77441404  | Otto Dibbert           | 2000       |
| 61338414  | Danial Cormier         | 2000       |
| 49680887  | Alivia Lemke           | 2000       |
| 45460101  | Itzel Cummings         | 2000       |
| 38009380  | Percy Hodkiewicz       | 2000       |
| 12943560  | Hulda Hackett          | 2000       |
| 1294029   | Stanford Herman        | 2000       |
| 111453184 | Jeffrey Brekke         | 2000       |
...
300000 rows in set (0.23 sec)
```

## 限制查询结果数量

要限制查询结果的数量，你可以使用 `LIMIT` 语句。

<SimpleTab groupId="language">
<div label="SQL" value="sql">

```sql
SELECT id, name, birth_year
FROM authors
ORDER BY birth_year DESC
LIMIT 10;
```

</div>

<div label="Java" value="java">

```java
public List<Author> getAuthorsWithLimit(Integer limit) throws SQLException {
    List<Author> authors = new ArrayList<>();
    try (Connection conn = ds.getConnection()) {
        PreparedStatement stmt = conn.prepareStatement("""
            SELECT id, name, birth_year
            FROM authors
            ORDER BY birth_year DESC
            LIMIT ?;
            """);
        stmt.setInt(1, limit);
        ResultSet rs = stmt.executeQuery();
        while (rs.next()) {
            Author author = new Author();
            author.setId(rs.getLong("id"));
            author.setName(rs.getString("name"));
            author.setBirthYear(rs.getShort("birth_year"));
            authors.add(author);
        }
    }
    return authors;
}
```

</div>
</SimpleTab>

结果如下：

```
+-----------+------------------------+------------+
| id        | name                   | birth_year |
+-----------+------------------------+------------+
| 83420726  | Terrance Dach          | 2000       |
| 57938667  | Margarita Christiansen | 2000       |
| 77441404  | Otto Dibbert           | 2000       |
| 61338414  | Danial Cormier         | 2000       |
| 49680887  | Alivia Lemke           | 2000       |
| 45460101  | Itzel Cummings         | 2000       |
| 38009380  | Percy Hodkiewicz       | 2000       |
| 12943560  | Hulda Hackett          | 2000       |
| 1294029   | Stanford Herman        | 2000       |
| 111453184 | Jeffrey Brekke         | 2000       |
+-----------+------------------------+------------+
10 rows in set (0.11 sec)
```

使用 `LIMIT` 语句后，在本例中查询时间从 `0.23 秒` 显著减少到 `0.11 秒`。更多信息，请参见 [TopN 和 Limit](/topn-limit-push-down.md)。

## 聚合查询

要更好地了解整体数据情况，你可以使用 `GROUP BY` 语句来聚合查询结果。

例如，如果你想知道哪些年份出生的作者较多，可以按 `birth_year` 列对 `authors` 表进行分组，然后统计每年的数量：

<SimpleTab groupId="language">
<div label="SQL" value="sql">

```sql
SELECT birth_year, COUNT (DISTINCT id) AS author_count
FROM authors
GROUP BY birth_year
ORDER BY author_count DESC;
```

</div>

<div label="Java" value="java">

```java
public class AuthorCount {
    private Short birthYear;
    private Integer authorCount;

    public AuthorCount() {}

     // 省略 getter 和 setter 方法。
}

public List<AuthorCount> getAuthorCountsByBirthYear() throws SQLException {
    List<AuthorCount> authorCounts = new ArrayList<>();
    try (Connection conn = ds.getConnection()) {
        Statement stmt = conn.createStatement();
        ResultSet rs = stmt.executeQuery("""
            SELECT birth_year, COUNT(DISTINCT id) AS author_count
            FROM authors
            GROUP BY birth_year
            ORDER BY author_count DESC;
            """);

        while (rs.next()) {
            AuthorCount authorCount = new AuthorCount();
            authorCount.setBirthYear(rs.getShort("birth_year"));
            authorCount.setAuthorCount(rs.getInt("author_count"));
            authorCounts.add(authorCount);
        }
    }
    return authorCount;
}
```

</div>
</SimpleTab>

结果如下：

```
+------------+--------------+
| birth_year | author_count |
+------------+--------------+
|       1932 |          317 |
|       1947 |          290 |
|       1939 |          282 |
|       1935 |          289 |
|       1968 |          291 |
|       1962 |          261 |
|       1961 |          283 |
|       1986 |          289 |
|       1994 |          280 |
...
|       1972 |          306 |
+------------+--------------+
71 rows in set (0.00 sec)
```

除了 `COUNT` 函数外，TiDB 还支持其他聚合函数。更多信息，请参见[聚合（GROUP BY）函数](/functions-and-operators/aggregate-group-by-functions.md)。

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上询问社区，或[提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上询问社区，或[提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>
