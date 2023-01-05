---
title: Paginate Results
summary: Introduce paginate result feature in TiDB.
---

# Paginate Results

To page through a large query result, you can get your desired part in a "paginated" manner.

## Paginate query results

In TiDB, you can paginate query results using the `LIMIT` statement. For example:

```sql
SELECT * FROM table_a t ORDER BY gmt_modified DESC LIMIT offset, row_count;
```

`offset` indicates the beginning number of records and `row_count` indicates the number of records per page. TiDB also supports `LIMIT row_count OFFSET offset` syntax.

When pagination is used, it is recommended that you sort query results with the `ORDER BY` statement unless there is a need to display data randomly.

<SimpleTab groupId="language">
<div label="SQL" value="sql">

For example, to let users of the [Bookshop](/develop/dev-guide-bookshop-schema-design.md) application view the latest published books in a paginated manner, you can use the `LIMIT 0, 10` statement, which returns the first page of the result list, with a maximum of 10 records per page. To get the second page, you can change the statement to `LIMIT 10, 10`.

```sql
SELECT *
FROM books
ORDER BY published_at DESC
LIMIT 0, 10;
```

</div>
<div label="Java" value="java">

In application development, the backend program receives the `page_number` parameter (which means the number of the page being requested) and the `page_size` parameter (which controls how many records per page) from the frontend instead of the `offset` parameter. Therefore, some conversions needed to be done before querying.

```java
public List<Book> getLatestBooksPage(Long pageNumber, Long pageSize) throws SQLException {
    pageNumber = pageNumber < 1L ? 1L : pageNumber;
    pageSize = pageSize < 10L ? 10L : pageSize;
    Long offset = (pageNumber - 1) * pageSize;
    Long limit = pageSize;
    List<Book> books = new ArrayList<>();
    try (Connection conn = ds.getConnection()) {
        PreparedStatement stmt = conn.prepareStatement("""
        SELECT id, title, published_at
        FROM books
        ORDER BY published_at DESC
        LIMIT ?, ?;
        """);
        stmt.setLong(1, offset);
        stmt.setLong(2, limit);
        ResultSet rs = stmt.executeQuery();
        while (rs.next()) {
            Book book = new Book();
            book.setId(rs.getLong("id"));
            book.setTitle(rs.getString("title"));
            book.setPublishedAt(rs.getDate("published_at"));
            books.add(book);
        }
    }
    return books;
}
```

</div>
</SimpleTab>

## Paging batches for single-field primary key tables

Usually, you can write a pagination SQL statement using a primary key or unique index to sort results and the `offset` keyword in the `LIMIT` clause to split pages by a specified row count. Then the pages are wrapped into independent transactions to achieve flexible paging updates. However, the disadvantage is also obvious. As the primary key or unique index needs to be sorted, a larger offset consumes more computing resources, especially in the case of a large volume of data.

The following introduces a more efficient paging batching method:

<SimpleTab groupId="language">
<div label="SQL" value="sql">

First, sort the data by primary key and call the window function `row_number()` to generate a row number for each row. Then, call the aggregation function to group row numbers by the specified page size and calculate the minimum and maximum values of each page.

```sql
SELECT
    floor((t.row_num - 1) / 1000) + 1 AS page_num,
    min(t.id) AS start_key,
    max(t.id) AS end_key,
    count(*) AS page_size
FROM (
    SELECT id, row_number() OVER (ORDER BY id) AS row_num
    FROM books
) t
GROUP BY page_num
ORDER BY page_num;
```

The result is as follows:

```
+----------+------------+------------+-----------+
| page_num | start_key  | end_key    | page_size |
+----------+------------+------------+-----------+
|        1 |     268996 |  213168525 |      1000 |
|        2 |  213210359 |  430012226 |      1000 |
|        3 |  430137681 |  647846033 |      1000 |
|        4 |  647998334 |  848878952 |      1000 |
|        5 |  848899254 | 1040978080 |      1000 |
...
|       20 | 4077418867 | 4294004213 |      1000 |
+----------+------------+------------+-----------+
20 rows in set (0.01 sec)
```

Next, use the `WHERE id BETWEEN start_key AND end_key` statement to query the data of each slice. To update data more efficiently, you can use the above slice information when modifying the data.

To delete the basic information of all books on page 1, replace the `start_key` and `end_key` with values of page 1 in the above result:

```sql
DELETE FROM books
WHERE
    id BETWEEN 268996 AND 213168525
ORDER BY id;
```

</div>
<div label="Java" value="java">

In Java, define a `PageMeta` class to store page meta information.

```java
public class PageMeta<K> {
    private Long pageNum;
    private K startKey;
    private K endKey;
    private Long pageSize;

    // Skip the getters and setters.

}
```

Define a `getPageMetaList()` method to get the page meta information list, and then define a `deleteBooksByPageMeta()` method to delete data in batches according to the page meta information.

```java
public class BookDAO {
    public List<PageMeta<Long>> getPageMetaList() throws SQLException {
        List<PageMeta<Long>> pageMetaList = new ArrayList<>();
        try (Connection conn = ds.getConnection()) {
            Statement stmt = conn.createStatement();
            ResultSet rs = stmt.executeQuery("""
            SELECT
                floor((t.row_num - 1) / 1000) + 1 AS page_num,
                min(t.id) AS start_key,
                max(t.id) AS end_key,
                count(*) AS page_size
            FROM (
                SELECT id, row_number() OVER (ORDER BY id) AS row_num
                FROM books
            ) t
            GROUP BY page_num
            ORDER BY page_num;
            """);
            while (rs.next()) {
                PageMeta<Long> pageMeta = new PageMeta<>();
                pageMeta.setPageNum(rs.getLong("page_num"));
                pageMeta.setStartKey(rs.getLong("start_key"));
                pageMeta.setEndKey(rs.getLong("end_key"));
                pageMeta.setPageSize(rs.getLong("page_size"));
                pageMetaList.add(pageMeta);
            }
        }
        return pageMetaList;
    }

    public void deleteBooksByPageMeta(PageMeta<Long> pageMeta) throws SQLException {
        try (Connection conn = ds.getConnection()) {
            PreparedStatement stmt = conn.prepareStatement("DELETE FROM books WHERE id >= ? AND id <= ?");
            stmt.setLong(1, pageMeta.getStartKey());
            stmt.setLong(2, pageMeta.getEndKey());
            stmt.executeUpdate();
        }
    }
}
```

The following statement is to delete the data on page 1:

```java
List<PageMeta<Long>> pageMetaList = bookDAO.getPageMetaList();
if (pageMetaList.size() > 0) {
    bookDAO.deleteBooksByPageMeta(pageMetaList.get(0));
}
```

The following statement is to delete all book data in batches by paging:

```java
List<PageMeta<Long>> pageMetaList = bookDAO.getPageMetaList();
pageMetaList.forEach((pageMeta) -> {
    try {
        bookDAO.deleteBooksByPageMeta(pageMeta);
    } catch (SQLException e) {
        e.printStackTrace();
    }
});
```

</div>
</SimpleTab>

This method significantly improves the efficiency of batch processing by avoiding wasting computing resources caused by frequent data sorting operations.

## Paging batches for composite primary key tables

### Non-clustered index table

For non-clustered index tables (also known as "non-index-organized tables"), the internal field `_tidb_rowid` can be used as a pagination key, and the pagination method is the same as that of single-field primary key tables.

> **Tip:**
>
> You can use the `SHOW CREATE TABLE users;` statement to check whether the table primary key uses [clustered index](/clustered-indexes.md).

For example:

```sql
SELECT
    floor((t.row_num - 1) / 1000) + 1 AS page_num,
    min(t._tidb_rowid) AS start_key,
    max(t._tidb_rowid) AS end_key,
    count(*) AS page_size
FROM (
    SELECT _tidb_rowid, row_number () OVER (ORDER BY _tidb_rowid) AS row_num
    FROM users
) t
GROUP BY page_num
ORDER BY page_num;
```

The result is as follows:

```
+----------+-----------+---------+-----------+
| page_num | start_key | end_key | page_size |
+----------+-----------+---------+-----------+
|        1 |         1 |    1000 |      1000 |
|        2 |      1001 |    2000 |      1000 |
|        3 |      2001 |    3000 |      1000 |
|        4 |      3001 |    4000 |      1000 |
|        5 |      4001 |    5000 |      1000 |
|        6 |      5001 |    6000 |      1000 |
|        7 |      6001 |    7000 |      1000 |
|        8 |      7001 |    8000 |      1000 |
|        9 |      8001 |    9000 |      1000 |
|       10 |      9001 |    9990 |       990 |
+----------+-----------+---------+-----------+
10 rows in set (0.00 sec)
```

### Clustered index table

For clustered index tables (also known as "index-organized tables"), you can use the `concat` function to concatenate values of multiple columns as a key, and then use a window function to query the paging information.

It should be noted that the key is a string at this time, and you must ensure that the length of the string is always the same, to obtain the correct `start_key` and `end_key` in the slice through the `min` and `max` aggregation function. If the length of the field for string concatenation is not fixed, you can use the `LPAD` function to pad it.

For example, you can implement a paging batch for the data in the `ratings` table as follows:

Create the meta information table by using the following statement. As the key concatenated by `book_id` and `user_id`, which are `bigint` types, is unable to convert to the same length, the `LPAD` function is used to pad the length with `0` according to the maximum bits 19 of `bigint`.

```sql
SELECT
    floor((t1.row_num - 1) / 10000) + 1 AS page_num,
    min(mvalue) AS start_key,
    max(mvalue) AS end_key,
    count(*) AS page_size
FROM (
    SELECT
        concat('(', LPAD(book_id, 19, 0), ',', LPAD(user_id, 19, 0), ')') AS mvalue,
        row_number() OVER (ORDER BY book_id, user_id) AS row_num
    FROM ratings
) t1
GROUP BY page_num
ORDER BY page_num;
```

> **Note:**
>
> The preceding SQL statement is executed as `TableFullScan`. When the data volume is large, the query will be slow, and you can [use TiFlash](/tiflash/tiflash-overview.md#use-tiflash) to speed up it.

The result is as follows:

```
+----------+-------------------------------------------+-------------------------------------------+-----------+
| page_num | start_key                                 | end_key                                   | page_size |
+----------+-------------------------------------------+-------------------------------------------+-----------+
|        1 | (0000000000000268996,0000000000092104804) | (0000000000140982742,0000000000374645100) |     10000 |
|        2 | (0000000000140982742,0000000000456757551) | (0000000000287195082,0000000004053200550) |     10000 |
|        3 | (0000000000287196791,0000000000191962769) | (0000000000434010216,0000000000237646714) |     10000 |
|        4 | (0000000000434010216,0000000000375066168) | (0000000000578893327,0000000002167504460) |     10000 |
|        5 | (0000000000578893327,0000000002457322286) | (0000000000718287668,0000000001502744628) |     10000 |
...
|       29 | (0000000004002523918,0000000000902930986) | (0000000004147203315,0000000004090920746) |     10000 |
|       30 | (0000000004147421329,0000000000319181561) | (0000000004294004213,0000000003586311166) |      9972 |
+----------+-------------------------------------------+-------------------------------------------+-----------+
30 rows in set (0.28 sec)
```

To delete all rating records on page 1, replace the `start_key` and `end_key` with values of page 1 in the above result:

```sql
SELECT * FROM ratings
WHERE
    (book_id > 268996 AND book_id < 140982742)
    OR (
        book_id = 268996 AND user_id >= 92104804
    )
    OR (
        book_id = 140982742 AND user_id <= 374645100
    )
ORDER BY book_id, user_id;
```
