---
title: 索引最佳实践
summary: 了解在 TiDB 中创建和使用索引的一些最佳实践。
---

<!-- markdownlint-disable MD029 -->

# 索引最佳实践

本文档介绍在 TiDB 中创建和使用索引的一些最佳实践。

## 开始之前

本节以 [bookshop](/develop/dev-guide-bookshop-schema-design.md) 数据库中的 `books` 表为例。

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

- 创建包含多个列的联合索引，这是一种称为[覆盖索引优化](/explain-indexes.md#indexreader)的优化。**覆盖索引优化**允许 TiDB 直接在索引上查询数据，这有助于提高性能。
- 避免在不经常查询的列上创建二级索引。有用的二级索引可以加快查询速度，但要注意它也有副作用。每次添加索引时，插入一行时都会添加一个额外的 Key-Value。索引越多，写入速度越慢，占用的空间也越多。此外，过多的索引会影响优化器运行时间，不恰当的索引可能会误导优化器。因此，更多的索引并不总是意味着更好的性能。
- 根据你的应用程序创建适当的索引。原则上，只在需要用于查询的列上创建索引以提高性能。以下情况适合创建索引：

    - 区分度高的列可以显著减少过滤的行数。例如，建议在身份证号码上创建索引，但不建议在性别上创建索引。
    - 在使用多个条件查询时使用联合索引。注意，等值条件的列需要放在联合索引的前面。这里有一个例子：如果经常使用 `select* from t where c1 = 10 and c2 = 100 and c3 > 10` 查询，考虑创建联合索引 `Index cidx (c1, c2, c3)`，这样可以根据查询条件构建索引前缀进行扫描。

- 为二级索引命名时要有意义，建议遵循公司或组织的表命名约定。如果不存在这样的命名约定，请遵循[索引命名规范](/develop/dev-guide-object-naming-guidelines.md)中的规则。

## 使用索引的最佳实践

- 索引是为了加快查询速度，所以要确保现有的索引实际上被某些查询使用。如果一个索引没有被任何查询使用，这个索引就是无意义的，你需要删除它。
- 使用联合索引时，遵循最左前缀原则。

    假设你在 `title` 和 `published_at` 列上创建一个新的联合索引：

    {{< copyable "sql" >}}

    ```sql
    CREATE INDEX title_published_at_idx ON books (title, published_at);
    ```

    以下查询仍然可以使用联合索引：

    {{< copyable "sql" >}}

    ```sql
    SELECT * FROM books WHERE title = 'database';
    ```

    但是，以下查询无法使用联合索引，因为没有指定索引中最左边第一列的条件：

    {{< copyable "sql" >}}

    ```sql
    SELECT * FROM books WHERE published_at = '2018-08-18 21:42:08';
    ```

- 在查询中使用索引列作为条件时，不要对其进行计算、函数运算或类型转换，这会阻止 TiDB 优化器使用索引。

    假设你在时间类型列 `published_at` 上创建一个新索引：

    {{< copyable "sql" >}}

    ```sql
    CREATE INDEX published_at_idx ON books (published_at);
    ```

    但是，以下查询无法使用 `published_at` 上的索引：

    {{< copyable "sql" >}}

    ```sql
    SELECT * FROM books WHERE YEAR(published_at)=2022;
    ```

    要使用 `published_at` 上的索引，你可以将查询重写如下，这样可以避免在索引列上使用任何函数：

    {{< copyable "sql" >}}

    ```sql
    SELECT * FROM books WHERE published_at >= '2022-01-01' AND published_at < '2023-01-01';
    ```

    你也可以使用表达式索引为查询条件中的 `YEAR(published_at)` 创建一个表达式索引：

    {{< copyable "sql" >}}

    ```sql
    CREATE INDEX published_year_idx ON books ((YEAR(published_at)));
    ```

    现在，如果你执行 `SELECT * FROM books WHERE YEAR(published_at)=2022;` 查询，查询可以使用 `published_year_idx` 索引来加速执行。

    > **警告：**
    >
    > 目前，表达式索引是一个实验性功能，需要在 TiDB 配置文件中启用。更多详情，请参阅[表达式索引](/sql-statements/sql-statement-create-index.md#expression-index)。

- 尽量使用覆盖索引，其中索引中的列包含要查询的列，避免使用 `SELECT *` 语句查询所有列。

    以下查询只需要扫描索引 `title_published_at_idx` 就能获取数据：

    {{< copyable "sql" >}}

    ```sql
    SELECT title, published_at FROM books WHERE title = 'database';
    ```

    虽然以下查询语句可以使用联合索引 `(title, published_at)`，但它会导致查询非索引列的额外开销，这需要 TiDB 根据索引数据中存储的引用（通常是主键信息）来查询行数据。

    {{< copyable "sql" >}}

    ```sql
    SELECT * FROM books WHERE title = 'database';
    ```

- 当查询条件包含 `!=` 或 `NOT IN` 时，查询无法使用索引。例如，以下查询无法使用任何索引：

    {{< copyable "sql" >}}

    ```sql
    SELECT * FROM books WHERE title != 'database';
    ```

- 如果 `LIKE` 条件在查询中以通配符 `%` 开头，查询无法使用索引。例如，以下查询无法使用任何索引：

    {{< copyable "sql" >}}

    ```sql
    SELECT * FROM books WHERE title LIKE '%database';
    ```

- 当查询条件有多个可用索引，并且你在实践中知道哪个索引是最好的，建议使用[优化器提示](/optimizer-hints.md)强制 TiDB 优化器使用这个索引。这可以防止 TiDB 优化器由于统计信息不准确或其他问题而选择错误的索引。

    在以下查询中，假设列 `id` 和 `title` 分别有可用的索引 `id_idx` 和 `title_idx`，如果你知道 `id_idx` 更好，你可以在 SQL 中使用 `USE INDEX` 提示强制 TiDB 优化器使用 `id_idx` 索引。

    {{< copyable "sql" >}}

    ```sql
    SELECT * FROM t USE INDEX(id_idx) WHERE id = 1 and title = 'database';
    ```

- 在查询条件中使用 `IN` 表达式时，建议其后匹配的值不要超过 300 个，否则执行效率会很差。

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上询问社区，或[提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上询问社区，或[提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>
