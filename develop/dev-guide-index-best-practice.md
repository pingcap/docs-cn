---
title: 索引的最佳实践
summary: 介绍 TiDB 中索引的最佳实践。
aliases: ['/zh/tidb/dev/index-best-practice']
---

<!-- markdownlint-disable MD029 -->

# 索引的最佳实践

本章会介绍在 TiDB 中使用索引的一些最佳实践。

## 准备工作

本章内容将会用 [bookshop](/develop/dev-guide-bookshop-schema-design.md) 数据库中的 `books` 表作为示例。

{{< copyable "sql" >}}

```sql
CREATE TABLE `books` (
  `id` bigint(20) AUTO_RANDOM NOT NULL,
  `title` varchar(100) NOT NULL,
  `type` enum('Magazine', 'Novel', 'Life', 'Arts', 'Comics', 'Education & Reference', 'Humanities & Social Sciences', 'Science & Technology', 'Kids', 'Sports') NOT NULL,
  `published_at` datetime NOT NULL,
  `stock` int(11) DEFAULT '0',
  `price` decimal(15,2) DEFAULT '0.0',
  PRIMARY KEY (`id`) CLUSTERED
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
```

## 创建索引的最佳实践

- 建立你需要使用的数据的所有列的组合索引，这种优化技巧被称为 [覆盖索引优化 (covering index optimization)](/explain-indexes.md#indexreader)。**覆盖索引优化**将使得 TiDB 可以直接在索引上得到该查询所需的所有数据，可以大幅提升性能。
- 避免创建你不需要的二级索引，有用的二级索引能加速查询，但是要注意新增一个索引是有副作用的。每增加一个索引，在插入一条数据的时候，就要额外新增一个 Key-Value，所以索引越多，写入越慢，并且空间占用越大。另外过多的索引也会影响优化器运行时间，并且不合适的索引会误导优化器。所以索引并不是越多越好。
- 根据具体的业务特点创建合适的索引。原则上需要对查询中需要用到的列创建索引，目的是提高性能。下面几种情况适合创建索引：

    - 区分度比较大的列，通过索引能显著地减少过滤后的行数。例如推荐在人的身份证号码这一列上创建索引，但不推荐在人的性别这一列上创建索引。
    - 有多个查询条件时，可以选择组合索引，注意需要把等值条件的列放在组合索引的前面。这里举一个例子，假设常用的查询是 `SELECT * FROM t where c1 = 10 and c2 = 100 and c3 > 10`, 那么可以考虑建立组合索引 `Index cidx (c1, c2, c3)`，这样可以用查询条件构造出一个索引前缀进行 Scan。

- 请使用有意义的二级索引名，推荐你遵循公司或组织的表命名规范。如果你的公司或组织没有相应的命名规范，可参考[索引命名规范](/develop/dev-guide-object-naming-guidelines.md#索引命名规范)。

## 使用索引的最佳实践

- 建立索引的目的是为了加速查询，所以请确保索引能在一些查询中被用上。如果一个索引不会被任何查询语句用到，那这个索引是没有意义的，请删除这个索引。
- 使用组合索引时，需要满足最左前缀原则。

    例如假设在列 `title, published_at` 上新建一个组合索引索引：

    {{< copyable "sql" >}}

    ```sql
    CREATE INDEX title_published_at_idx ON books (title, published_at);
    ```

    下面这个查询依然能用上这个组合索引：

    {{< copyable "sql" >}}

    ```sql
    SELECT * FROM books WHERE title = 'database';
    ```

    但下面这个查询由于未指定组合索引中最左边第一列的条件，所以无法使用组合索引：

    {{< copyable "sql" >}}

    ```sql
    SELECT * FROM books WHERE published_at = '2018-08-18 21:42:08';
    ```

- 在查询条件中使用索引列作为条件时，不要在索引列上做计算，函数，或者类型转换的操作，会导致优化器无法使用该索引。

    例如假设在时间类型的列 `published_at` 上新建一个索引：

    {{< copyable "sql" >}}

    ```sql
    CREATE INDEX published_at_idx ON books (published_at);
    ```

    但下面查询是无法使用 `published_at` 上的索引的：

    {{< copyable "sql" >}}

    ```sql
    SELECT * FROM books WHERE YEAR(published_at)=2022;
    ```

    可以改写成下面查询，避免在索引列上做函数计算后，即可使用 `published_at` 上的索引:

    {{< copyable "sql" >}}

    ```sql
    SELECT * FROM books WHERE published_at >= '2022-01-01' AND published_at < '2023-01-01';
    ```

    也可以使用表达式索引，例如对查询条件中的 `YEAR(published_at)` 创建一个表达式索引：

    {{< copyable "sql" >}}

    ```sql
    CREATE INDEX published_year_idx ON books ((YEAR(published_at)));
    ```

    然后通过 `SELECT * FROM books WHERE YEAR(published_at)=2022;` 查询就能使用 `published_year_idx` 索引来加速查询了。

    > **注意：**
    >
    > 表达式索引目前是 TiDB 的实验特性，需要在 TiDB 配置文件中开启表达式索引特性，详情可以参考 [表达式索引文档](/sql-statements/sql-statement-create-index.md#表达式索引)。

- 尽量使用覆盖索引，即索引列包含查询列，避免总是 `SELECT *` 查询所有列的语句。

    例如下面查询只需扫描索引 `title_published_at_idx` 数据即可获取查询列的数据：

    {{< copyable "sql" >}}

    ```sql
    SELECT title, published_at FROM books WHERE title = 'database';
    ```

    但下面查询语句虽然能用上组合索引 `(title, published_at)`, 但会多一个回表查询非索引列数据的额外开销，回表查询是指根据索引数据中存储的引用（一般是主键信息），到表中查询相应行的数据。

    {{< copyable "sql" >}}

    ```sql
    SELECT * FROM books WHERE title = 'database';
    ```

- 查询条件使用 `!=`，`NOT IN` 时，无法使用索引。例如下面查询无法使用任何索引：

    {{< copyable "sql" >}}

    ```sql
    SELECT * FROM books WHERE title != 'database';
    ```

- 使用 `LIKE` 时如果条件是以通配符 `%` 开头，也无法使用索引。例如下面查询无法使用任何索引：

    {{< copyable "sql" >}}

    ```sql
    SELECT * FROM books WHERE title LIKE '%database';
    ```

- 当查询条件有多个索引可供使用，但你知道用哪一个索引是最优的时，推荐使用 [优化器 Hint](/optimizer-hints.md) 来强制优化器使用这个索引，这样可以避免优化器因为统计信息不准或其他问题时，选错索引。

    例如下面查询中，假设在列 `id` 和 列 `title` 上都各自有索引 `id_idx` 和 `title_idx`，你知道 `id_idx` 的过滤性更好，就可以在 SQL 中使用 `USE INDEX` Hint 来强制优化器使用 `id_idx` 索引。

    {{< copyable "sql" >}}

    ```sql
    SELECT * FROM t USE INDEX(id_idx) WHERE id = 1 and title = 'database';
    ```

- 查询条件使用 `IN` 表达式时，后面匹配的条件数量建议不要超过 300 个，否则执行效率会较差。
