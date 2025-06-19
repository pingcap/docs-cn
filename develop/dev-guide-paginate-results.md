---
title: 分页结果
summary: 介绍 TiDB 中的分页结果功能。
---

# 分页结果

要对大型查询结果进行分页，您可以以"分页"方式获取所需的部分。

## 分页查询结果

在 TiDB 中，您可以使用 `LIMIT` 语句对查询结果进行分页。例如：

```sql
SELECT * FROM table_a t ORDER BY gmt_modified DESC LIMIT offset, row_count;
```

`offset` 表示记录的起始编号，`row_count` 表示每页的记录数。TiDB 也支持 `LIMIT row_count OFFSET offset` 语法。

使用分页时，建议使用 `ORDER BY` 语句对查询结果进行排序，除非需要随机显示数据。

<SimpleTab groupId="language">
<div label="SQL" value="sql">

例如，要让 [Bookshop](/develop/dev-guide-bookshop-schema-design.md) 应用程序的用户以分页方式查看最新发布的书籍，您可以使用 `LIMIT 0, 10` 语句，该语句返回结果列表的第一页，每页最多 10 条记录。要获取第二页，您可以将语句改为 `LIMIT 10, 10`。

```sql
SELECT *
FROM books
ORDER BY published_at DESC
LIMIT 0, 10;
```

</div>
<div label="Java" value="java">

在应用程序开发中，后端程序从前端接收 `page_number` 参数（表示请求的页码）和 `page_size` 参数（控制每页显示多少条记录），而不是 `offset` 参数。因此，在查询之前需要进行一些转换。

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

## 单字段主键表的分页批处理

通常，您可以使用主键或唯一索引对结果进行排序，并在 `LIMIT` 子句中使用 `offset` 关键字按指定行数分页来编写分页 SQL 语句。然后将这些页面包装到独立的事务中，以实现灵活的分页更新。但是，缺点也很明显。由于需要对主键或唯一索引进行排序，较大的偏移量会消耗更多的计算资源，特别是在数据量较大的情况下。

以下介绍一种更高效的分页批处理方法：

<SimpleTab groupId="language">
<div label="SQL" value="sql">

首先，按主键排序并调用窗口函数 `row_number()` 为每一行生成行号。然后，调用聚合函数按指定的页面大小对行号进行分组，并计算每页的最小值和最大值。

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

结果如下：

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

接下来，使用 `WHERE id BETWEEN start_key AND end_key` 语句查询每个分片的数据。为了更高效地更新数据，您可以在修改数据时使用上述分片信息。

要删除第 1 页的所有图书基本信息，请将上述结果中第 1 页的 `start_key` 和 `end_key` 替换：

```sql
DELETE FROM books
WHERE
    id BETWEEN 268996 AND 213168525
ORDER BY id;
```

</div>
<div label="Java" value="java">

在 Java 中，定义一个 `PageMeta` 类来存储页面元信息。

```java
public class PageMeta<K> {
    private Long pageNum;
    private K startKey;
    private K endKey;
    private Long pageSize;

    // 跳过 getter 和 setter。

}
```

定义一个 `getPageMetaList()` 方法来获取页面元信息列表，然后定义一个 `deleteBooksByPageMeta()` 方法根据页面元信息批量删除数据。

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

以下语句用于删除第 1 页的数据：

```java
List<PageMeta<Long>> pageMetaList = bookDAO.getPageMetaList();
if (pageMetaList.size() > 0) {
    bookDAO.deleteBooksByPageMeta(pageMetaList.get(0));
}
```

以下语句用于按分页批量删除所有图书数据：

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

这种方法通过避免频繁数据排序操作造成的计算资源浪费，显著提高了批处理效率。

## 复合主键表的分页批处理

### 非聚簇索引表

对于非聚簇索引表（也称为"非索引组织表"），可以使用内部字段 `_tidb_rowid` 作为分页键，分页方法与单字段主键表相同。

> **提示：**
>
> 您可以使用 `SHOW CREATE TABLE users;` 语句检查表主键是否使用[聚簇索引](/clustered-indexes.md)。

例如：

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

结果如下：

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

### 聚簇索引表

对于聚簇索引表（也称为"索引组织表"），您可以使用 `concat` 函数将多个列的值连接为一个键，然后使用窗口函数查询分页信息。

需要注意的是，此时键是一个字符串，必须确保字符串的长度始终相同，以通过 `min` 和 `max` 聚合函数在分片中获得正确的 `start_key` 和 `end_key`。如果用于字符串连接的字段长度不固定，可以使用 `LPAD` 函数进行填充。

例如，您可以按以下方式对 `ratings` 表中的数据进行分页批处理：

使用以下语句创建元信息表。由于 `book_id` 和 `user_id` 是 `bigint` 类型，它们连接成的键无法转换为相同的长度，因此使用 `LPAD` 函数根据 `bigint` 的最大位数 19 用 `0` 填充长度。

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

> **注意：**
>
> 上述 SQL 语句执行为 `TableFullScan`。当数据量较大时，查询会很慢，您可以[使用 TiFlash](/tiflash/tiflash-overview.md#使用-tiflash) 加速。

结果如下：

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

要删除第 1 页的所有评分记录，请将上述结果中第 1 页的 `start_key` 和 `end_key` 替换：

```sql
SELECT *
FROM ratings
WHERE (
        268996 = 140982742
        AND book_id = 268996
        AND user_id >= 92104804
        AND user_id <= 374645100
    )
    OR (
        268996 != 140982742
        AND (
            (
                book_id > 268996
                AND book_id < 140982742
            )
            OR (
                book_id = 268996
                AND user_id >= 92104804
            )
            OR (
                book_id = 140982742
                AND user_id <= 374645100
            )
        )
    )
ORDER BY book_id, user_id;
```

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上询问社区，或[提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上询问社区，或[提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>
