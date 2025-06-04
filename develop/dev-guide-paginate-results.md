---
title: 分页查询
summary: 介绍 TiDB 的分页查询功能。
aliases: ['/zh/tidb/dev/paginate-results']
---

# 分页查询

当查询结果数据量较大时，往往希望以“分页”的方式返回所需要的部分。

## 对查询结果进行分页

在 TiDB 当中，可以利用 `LIMIT` 语句来实现分页功能，常规的分页语句写法如下所示：

```sql
SELECT * FROM table_a t ORDER BY gmt_modified DESC LIMIT offset, row_count;
```

`offset` 表示起始记录数，`row_count` 表示每页记录数。除此之外，TiDB 也支持 `LIMIT row_count OFFSET offset` 语法。

除非明确要求不要使用任何排序来随机展示数据，使用分页查询语句时都应该通过 `ORDER BY` 语句指定查询结果的排序方式。

<SimpleTab groupId="language">
<div label="SQL" value="sql">

例如，在 [Bookshop](/develop/dev-guide-bookshop-schema-design.md) 应用当中，希望将最新书籍列表以分页的形式返回给用户。通过 `LIMIT 0, 10` 语句，便可以得到列表第 1 页的书籍信息，每页中最多有 10 条记录。获取第 2 页信息，则改成可以改成 `LIMIT 10, 10`，如此类推。

```sql
SELECT *
FROM books
ORDER BY published_at DESC
LIMIT 0, 10;
```

</div>
<div label="Java" value="java">

在使用 Java 开发应用程序时，后端程序从前端接收到的参数页码 `page_number` 和每页的数据条数 `page_size`，而不是起始记录数 `offset`，因此在进行数据库查询前需要对其进行一些转换。

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

常规的分页更新 SQL 一般使用主键或者唯一索引进行排序，再配合 LIMIT 语法中的 `offset`，按固定行数拆分页面。然后把页面包装进独立的事务中，从而实现灵活的分页更新。但是，劣势也很明显：由于需要对主键或者唯一索引进行排序，越靠后的页面参与排序的行数就会越多，尤其当批量处理涉及的数据体量较大时，可能会占用过多计算资源。

下面将介绍一种更为高效的分页批处理方案：

<SimpleTab groupId="language">
<div label="SQL" value="sql">

使用 SQL 实现分页批处理，可以按照如下步骤进行：

首先将数据按照主键排序，然后调用窗口函数 `row_number()` 为每一行数据生成行号，接着调用聚合函数按照设置好的页面大小对行号进行分组，最终计算出每页的最小值和最大值。

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

查询结果如下：

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

接下来，只需要使用 `WHERE id BETWEEN start_key AND end_key` 语句查询每个分片的数据即可。修改数据时，也可以借助上面计算好的分片信息，实现高效的数据更新。

例如，假如想要删除第 1 页上的所有书籍的基本信息，可以将上表第 1 页所对应的 `start_key` 和 `end_key` 填入 SQL 语句当中。

```sql
DELETE FROM books
WHERE
    id BETWEEN 268996 AND 213168525
ORDER BY id;
```

</div>
<div label="Java" value="java">

在 Java 语言当中，可以定义一个 `PageMeta` 类来存储分页元信息。

```java
public class PageMeta<K> {
    private Long pageNum;
    private K startKey;
    private K endKey;
    private Long pageSize;

    // Skip the getters and setters.

}
```

定义一个 `getPageMetaList()` 方法获取到分页元信息列表，然后定义一个可以根据页面元信息批量删除数据的方法 `deleteBooksByPageMeta()`。

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

如果想要删除第 1 页的数据，可以这样写：

```java
List<PageMeta<Long>> pageMetaList = bookDAO.getPageMetaList();
if (pageMetaList.size() > 0) {
    bookDAO.deleteBooksByPageMeta(pageMetaList.get(0));
}
```

如果希望通过分页分批地删除所有书籍数据，可以这样写：

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

改进方案由于规避了频繁的数据排序操作造成的性能损耗，显著改善了批量处理的效率。

## 复合主键表的分页批处理

### 非聚簇索引表

对于非聚簇索引表（又被称为“非索引组织表”）而言，可以使用隐藏字段 `_tidb_rowid` 作为分页的 key，分页的方法与单列主键表中所介绍的方法相同。

> **建议：**
>
> 你可以通过 `SHOW CREATE TABLE users;` 语句查看表主键是否使用了[聚簇索引](/clustered-indexes.md)。

例如：

```sql
SELECT
    floor((t.row_num - 1) / 1000) + 1 AS page_num,
    min(t._tidb_rowid) AS start_key,
    max(t._tidb_rowid) AS end_key,
    count(*) AS page_size
FROM (
    SELECT _tidb_rowid, row_number() OVER (ORDER BY _tidb_rowid) AS row_num
    FROM users
) t
GROUP BY page_num
ORDER BY page_num;
```

查询结果如下：

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

对于聚簇索引表（又被称为“索引组织表”），可以利用 `concat` 函数将多个列的值连接起来作为一个 key，然后使用窗口函数获取分页信息。

需要注意的是，这时候 key 是一个字符串，你必须确保这个字符串长度总是相等的，才能够通过 `min` 和 `max` 聚合函数得到分页内正确的 `start_key` 和 `end_key`。如果进行字符串连接的字段长度不固定，你可以通过 `LPAD` 函数进行补全。

例如，想要对 `ratings` 表里的数据进行分页批处理。

先可以通过下面的 SQL 语句来在制造元信息表。因为组成 key 的 `book_id` 列和 `user_id` 列都是 `bigint` 类型，转换为字符串是并不是等宽的，因此需要根据 `bigint` 类型的最大位数 19，使用 `LPAD` 函数在长度不够时用 `0` 补齐。

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
> 该 SQL 会以全表扫描 (TableFullScan) 方式执行，当数据量较大时，查询速度会变慢，此时可以[使用 TiFlash](/tiflash/tiflash-overview.md#使用-tiflash) 进行加速。

查询结果如下：

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

假如想要删除第 1 页上的所有评分记录，可以将上表第 1 页所对应的 `start_key` 和 `end_key` 填入 SQL 语句当中。

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
