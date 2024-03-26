---
title: 单表查询
summary: 介绍 TiDB 中的单表查询功能。
---

<!-- markdownlint-disable MD029 -->

# 单表查询

在这个章节当中，将开始介绍如何使用 SQL 来对数据库中的数据进行查询。

## 开始之前

下面将围绕 [Bookshop](/develop/dev-guide-bookshop-schema-design.md) 这个应用程序来对 TiDB 的数据查询部分展开介绍。

在阅读本章节之前，你需要做以下准备工作：

1. 构建 TiDB 集群（推荐使用 [TiDB Cloud](/develop/dev-guide-build-cluster-in-cloud.md) 或 [TiUP](/production-deployment-using-tiup.md)）。
2. [导入 Bookshop 应用程序的表结构和示例数据](/develop/dev-guide-bookshop-schema-design.md#导入表结构和数据)。
3. [连接到 TiDB](/develop/dev-guide-connect-to-tidb.md)。

## 简单的查询

在 Bookshop 应用程序的数据库当中，`authors` 表存放了作家们的基础信息，可以通过 `SELECT ... FROM ...` 语句将数据从数据库当中调取出去。

<SimpleTab groupId="language">
<div label="SQL" value="sql">

在 MySQL Client 等客户端输入并执行如下 SQL 语句：

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

在 Java 语言当中，可以通过声明一个 `Author` 类来定义如何存放作者的基础信息，根据数据的[类型](/data-type-overview.md)和[取值范围](/data-type-numeric.md)从 Java 语言当中选择合适的数据类型来存放对应的数据，例如：

- 使用 `Int` 类型变量存放 `int` 类型的数据。
- 使用 `Long` 类型变量存放 `bigint` 类型的数据。
- 使用 `Short` 类型变量存放 `tinyint` 类型的数据。
- 使用 `String` 类型变量存放 `varchar` 类型的数据。
- ...

```java
public class Author {
    private Long id;
    private String name;
    private Short gender;
    private Short birthYear;
    private Short deathYear;

    public Author() {}

     // Skip the getters and setters.
}
```

```java
public class AuthorDAO {

    // Omit initialization of instance variables.

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

- 在[获得数据库连接](/develop/dev-guide-connect-to-tidb.md#jdbc)之后，你可以通过 `conn.createStatement()` 语句创建一个 `Statement` 实例对象。
- 然后调用 `stmt.executeQuery("query_sql")` 方法向 TiDB 发起一个数据库查询请求。
- 数据库返回的查询结果将会存放到 `ResultSet` 当中，通过遍历 `ResultSet` 对象可以将返回结果映射到此前准备的 `Author` 类对象当中。

</div>
</SimpleTab>

## 对结果进行筛选

查询得到的结果非常多，但是并不都是你想要的？可以通过 `WHERE` 语句对查询的结果进行过滤，从而找到想要查询的部分。

例如，想要查找众多作家当中找出在 1998 年出生的作家：

<SimpleTab groupId="language">
<div label="SQL" value="sql">

在 SQL 中，可以使用 `WHERE` 子句添加筛选的条件：

```sql
SELECT * FROM authors WHERE birth_year = 1998;
```

</div>
<div label="Java" value="java">

对于 Java 程序而言，可以通过同一个 SQL 来处理带有动态参数的数据查询请求。

将参数拼接到 SQL 语句当中也许是一种方法，但是这可能不是一个好的主意，因为这会给应用程序带来潜在的 [SQL 注入](https://zh.wikipedia.org/wiki/SQL%E6%B3%A8%E5%85%A5)风险。

在处理这类查询时，应该使用 [PreparedStatement](/develop/dev-guide-prepared-statement.md) 来替代普通的 Statement。

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

## 对结果进行排序

使用 `ORDER BY` 语句可以让查询结果按照期望的方式进行排序。

例如，可以通过下面的 SQL 语句对 `authors` 表的数据按照 `birth_year` 列进行降序 (`DESC`) 排序，从而得到最年轻的作家列表。

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

查询结果如下：

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

如果希望 TiDB 只返回部分结果，可以使用 `LIMIT` 语句限制查询结果返回的记录数。

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

查询结果如下：

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

通过观察查询结果你会发现，在使用 `LIMIT` 语句之后，查询的时间明显缩短，这是 TiDB 对 `LIMIT` 子句进行优化后的结果，你可以通过 [TopN 和 Limit 下推](/topn-limit-push-down.md)章节了解更多细节。

## 聚合查询

如果你想要关注数据整体的情况，而不是部分数据，你可以通过使用 `GROUP BY` 语句配合聚合函数，构建一个聚合查询来帮助你对数据的整体情况有一个更好的了解。

比如说，你希望知道哪些年出生的作家比较多，你可以将作家基本信息按照 `birth_year` 列进行分组，然后分别统计在当年出生的作家数量：

<SimpleTab groupId="language">
<div label="SQL" value="sql">

```sql
SELECT birth_year, COUNT(DISTINCT id) AS author_count
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

     // Skip the getters and setters.
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

查询结果如下：

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

除了 `COUNT` 函数外，TiDB 还支持了其他聚合函数。详情请参考 [GROUP BY 聚合函数](/functions-and-operators/aggregate-group-by-functions.md)。
