---
title: Query data from a single table
summary: This document describes how to query data from a single table in a database.
---

<!-- markdownlint-disable MD029 -->

# Query data from a single table

This document describes how to use SQL and various programming languages to query data from a single table in a database.

## Before you begin

The following content will take the [Bookshop](/develop/dev-guide-bookshop-schema-design.md) application as an example to show how to query data from a single table in TiDB.

Before querying data, make sure that you have completed the following steps:

1. Build a TiDB cluster (using [TiDB Cloud](/develop/dev-guide-build-cluster-in-cloud.md) or [TiUP](/production-deployment-using-tiup.md) is recommended).
2. [Import table schema and sample data of the Bookshop application](/develop/dev-guide-bookshop-schema-design.md#import-table-structures-and-data).
3. [Connect to TiDB](/develop/dev-guide-connect-to-tidb.md).

## Execute a simple query

In the database of the Bookshop application, the `authors` table stores the basic information of authors. You can use the `SELECT ... FROM ...` statement to query data from the database.

<SimpleTab>
<div label="SQL" href="simple-sql">

Execute the following SQL statement in a MySQL client:

{{< copyable "sql" >}}

```sql
SELECT id, name FROM authors;
```

The output is as follows:

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
<div label="Java" href="simple-java">

In Java, authors' basic information can be stored by declaring a class `Author`. You should choose appropriate Java data types according to the [type](/data-type-overview.md) and [value range](/data-type-numeric.md) in the database. For example:

- Use a variable of type `Int` to store data of type `int`.
- Use a variable of type `Long` to store data of type `bigint`.
- Use a variable of type `Short` to store data of type `tinyint`.
- Use a variable of type `String` to store data of type `varchar`.
- ...

{{< copyable "java" >}}

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

{{< copyable "java" >}}

```java
public class AuthorDAO {

    // Omit initialization of instance variables...

    public List<Author> getAuthors() throws SQLException {
        List<Author> authors = new ArrayList<>();

        try (Connection conn = ds.getConnection()) {
            Statement stmt = conn.createStatement();
            ResultSet rs = stmt.executeQuery("SELECT id, name FROM authors");
            while (rs.next()) {
                Author author = new Author();
                author.setId( rs.getLong("id"));
                author.setName(rs.getString("name"));
                authors.add(author);
            }
        }
        return authors;
    }
}
```

- After [connecting to TiDB using the JDBC driver](/develop/dev-guide-connect-to-tidb.md#jdbc), you can create a `Statement` object with `conn.createStatus()`.
- Then call `stmt.executeQuery("query_sql")` to initiate a database query request to TiDB.
- The query results will be stored in a `ResultSet` object. By traversing `ResultSet`, the returned results can be mapped to the `Author` object.

</div>
</SimpleTab>

## Filter results

You can use the `WHERE` statement to filter query results.

For example, the following command will query authors who were born in 1998 among all authors:

<SimpleTab>
<div label="SQL" href="filter-sql">

Add filter conditions in the `WHERE` statement:

{{< copyable "sql" >}}

```sql
SELECT * FROM authors WHERE birth_year = 1998;
```

</div>
<div label="Java" href="filter-java">

In Java, you can use the same SQL to handle data query requests with dynamic parameters.

This can be done by concatenating parameters into a SQL statement. However, this method will pose a potential [SQL Injection](https://en.wikipedia.org/wiki/SQL_injection) risk to the security of the application.

To deal with such queries, use a [prepared statement](/develop/dev-guide-prepared-statement.md) instead of a normal statement.

{{< copyable "java" >}}

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
            author.setId( rs.getLong("id"));
            author.setName(rs.getString("name"));
            authors.add(author);
        }
    }
    return authors;
}
```

</div>
</SimpleTab>

## Sort results

With the `ORDER BY` statement, you can sort query results.

For example, the following SQL statement is to get a list of the youngest authors by sorting the `authors` table in descending order (`DESC`) according to the `birth_year` column.

{{< copyable "sql" >}}

```sql
SELECT id, name, birth_year
FROM authors
ORDER BY birth_year DESC;
```

The result is as follows:

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

## Limit the number of query results

You can use the `LIMIT` statement to limit the number of query results.

{{< copyable "java" >}}

```sql
SELECT id, name, birth_year
FROM authors
ORDER BY birth_year DESC
LIMIT 10;
```

The result is as follows:

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

With the `LIMIT` statement, the query time is significantly reduced from `0.23 sec` to `0.11 sec` in this example. For more information, see [TopN and Limit](/topn-limit-push-down.md).

## Aggregate queries

To have a better understanding of the overall data situation, you can use the `GROUP BY` statement to aggregate query results.

For example, if you want to know which years there are more authors born, you can group the `authors` table by the `birth_year` column, and then count for each year:

{{< copyable "java" >}}

```sql
SELECT birth_year, COUNT (DISTINCT id) AS author_count
FROM authors
GROUP BY birth_year
ORDER BY author_count DESC;
```

The result is as follows:

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

In addition to the `COUNT` function, TiDB also supports other aggregate functions. For more information, see [Aggregate (GROUP BY) Functions](/functions-and-operators/aggregate-group-by-functions.md).