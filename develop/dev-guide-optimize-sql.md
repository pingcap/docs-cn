---
title: SQL 性能调优
summary: 介绍 TiDB 的 SQL 性能调优方案和分析方法。
---

# SQL 性能调优

本文介绍一些常见的 SQL 语句慢的原因以及 SQL 性能调优的技巧。

## 开始之前

你可以使用 [`tiup demo` 导入](/develop/dev-guide-bookshop-schema-design.md#method-1-via-tiup-demo)准备数据：

```shell
tiup demo bookshop prepare --host 127.0.0.1 --port 4000 --books 1000000
```

或者[使用 TiDB Cloud 的导入功能](/develop/dev-guide-bookshop-schema-design.md#method-2-via-tidb-cloud-import)导入预先准备的示例数据。

## 问题：全表扫描

SQL 查询慢最常见的原因是 `SELECT` 语句执行全表扫描或使用了错误的索引。

当 TiDB 从一个大表中基于非主键列或不在二级索引中的列检索少量行时，性能通常较差：

```sql
SELECT * FROM books WHERE title = 'Marian Yost';
```

```sql
+------------+-------------+-----------------------+---------------------+-------+--------+
| id         | title       | type                  | published_at        | stock | price  |
+------------+-------------+-----------------------+---------------------+-------+--------+
| 65670536   | Marian Yost | Arts                  | 1950-04-09 06:28:58 | 542   | 435.01 |
| 1164070689 | Marian Yost | Education & Reference | 1916-05-27 12:15:35 | 216   | 328.18 |
| 1414277591 | Marian Yost | Arts                  | 1932-06-15 09:18:14 | 303   | 496.52 |
| 2305318593 | Marian Yost | Arts                  | 2000-08-15 19:40:58 | 398   | 402.90 |
| 2638226326 | Marian Yost | Sports                | 1952-04-02 12:40:37 | 191   | 174.64 |
+------------+-------------+-----------------------+---------------------+-------+--------+
5 rows in set
Time: 0.582s
```

要了解为什么这个查询很慢，你可以使用 `EXPLAIN` 查看执行计划：

```sql
EXPLAIN SELECT * FROM books WHERE title = 'Marian Yost';
```

```sql
+---------------------+------------+-----------+---------------+-----------------------------------------+
| id                  | estRows    | task      | access object | operator info                           |
+---------------------+------------+-----------+---------------+-----------------------------------------+
| TableReader_7       | 1.27       | root      |               | data:Selection_6                        |
| └─Selection_6       | 1.27       | cop[tikv] |               | eq(bookshop.books.title, "Marian Yost") |
|   └─TableFullScan_5 | 1000000.00 | cop[tikv] | table:books   | keep order:false                        |
+---------------------+------------+-----------+---------------+-----------------------------------------+
```

从执行计划中的 `TableFullScan_5` 可以看出，TiDB 对 `books` 表执行全表扫描，并检查每一行的 `title` 是否满足条件。`TableFullScan_5` 的 `estRows` 值为 `1000000.00`，这意味着优化器估计这次全表扫描需要扫描 `1000000.00` 行数据。

关于 `EXPLAIN` 的使用方法，请参见 [`EXPLAIN` 详解](/explain-walkthrough.md)。

### 解决方案：使用二级索引

要加快上述查询，可以在 `books.title` 列上添加二级索引：

```sql
CREATE INDEX title_idx ON books (title);
```

查询执行速度快了很多：

```sql
SELECT * FROM books WHERE title = 'Marian Yost';
```

```sql
+------------+-------------+-----------------------+---------------------+-------+--------+
| id         | title       | type                  | published_at        | stock | price  |
+------------+-------------+-----------------------+---------------------+-------+--------+
| 1164070689 | Marian Yost | Education & Reference | 1916-05-27 12:15:35 | 216   | 328.18 |
| 1414277591 | Marian Yost | Arts                  | 1932-06-15 09:18:14 | 303   | 496.52 |
| 2305318593 | Marian Yost | Arts                  | 2000-08-15 19:40:58 | 398   | 402.90 |
| 2638226326 | Marian Yost | Sports                | 1952-04-02 12:40:37 | 191   | 174.64 |
| 65670536   | Marian Yost | Arts                  | 1950-04-09 06:28:58 | 542   | 435.01 |
+------------+-------------+-----------------------+---------------------+-------+--------+
5 rows in set
Time: 0.007s
```

要了解为什么性能得到改善，使用 `EXPLAIN` 查看新的执行计划：

```sql
EXPLAIN SELECT * FROM books WHERE title = 'Marian Yost';
```

```sql
+---------------------------+---------+-----------+-------------------------------------+-------------------------------------------------------+
| id                        | estRows | task      | access object                       | operator info                                         |
+---------------------------+---------+-----------+-------------------------------------+-------------------------------------------------------+
| IndexLookUp_10            | 1.27    | root      |                                     |                                                       |
| ├─IndexRangeScan_8(Build) | 1.27    | cop[tikv] | table:books, index:title_idx(title) | range:["Marian Yost","Marian Yost"], keep order:false |
| └─TableRowIDScan_9(Probe) | 1.27    | cop[tikv] | table:books                         | keep order:false                                      |
+---------------------------+---------+-----------+-------------------------------------+-------------------------------------------------------+
```

从执行计划中的 `IndexLookup_10` 可以看出，TiDB 通过 `title_idx` 索引查询数据。其 `estRows` 值为 `1.27`，这意味着优化器估计只需要扫描 `1.27` 行。估计扫描的行数远少于全表扫描的 `1000000.00` 行数据。

`IndexLookup_10` 执行计划是先使用 `IndexRangeScan_8` 算子通过 `title_idx` 索引读取满足条件的索引数据，然后使用 `TableLookup_9` 算子根据索引数据中存储的 Row ID 查询对应的行。

关于 TiDB 执行计划的更多信息，请参见 [TiDB 执行计划概览](/explain-overview.md)。

### 解决方案：使用覆盖索引

如果索引是覆盖索引，包含了 SQL 语句查询的所有列，那么扫描索引数据就足够完成查询。

例如，在以下查询中，你只需要根据 `title` 查询对应的 `price`：

```sql
SELECT title, price FROM books WHERE title = 'Marian Yost';
```

```sql
+-------------+--------+
| title       | price  |
+-------------+--------+
| Marian Yost | 435.01 |
| Marian Yost | 328.18 |
| Marian Yost | 496.52 |
| Marian Yost | 402.90 |
| Marian Yost | 174.64 |
+-------------+--------+
5 rows in set
Time: 0.007s
```

因为 `title_idx` 索引只包含 `title` 列的数据，TiDB 仍然需要先扫描索引数据，然后从表中查询 `price` 列。

```sql
EXPLAIN SELECT title, price FROM books WHERE title = 'Marian Yost';
```

```sql
+---------------------------+---------+-----------+-------------------------------------+-------------------------------------------------------+
| id                        | estRows | task      | access object                       | operator info                                         |
+---------------------------+---------+-----------+-------------------------------------+-------------------------------------------------------+
| IndexLookUp_10            | 1.27    | root      |                                     |                                                       |
| ├─IndexRangeScan_8(Build) | 1.27    | cop[tikv] | table:books, index:title_idx(title) | range:["Marian Yost","Marian Yost"], keep order:false |
| └─TableRowIDScan_9(Probe) | 1.27    | cop[tikv] | table:books                         | keep order:false                                      |
+---------------------------+---------+-----------+-------------------------------------+-------------------------------------------------------+
```

要优化性能，删除 `title_idx` 索引并创建新的覆盖索引 `title_price_idx`：

```sql
ALTER TABLE books DROP INDEX title_idx;
```

```sql
CREATE INDEX title_price_idx ON books (title, price);
```

因为 `price` 数据存储在 `title_price_idx` 索引中，以下查询只需要扫描索引数据：

```sql
EXPLAIN SELECT title, price FROM books WHERE title = 'Marian Yost';
```

```sql
--------------------+---------+-----------+--------------------------------------------------+-------------------------------------------------------+
| id                 | estRows | task      | access object                                    | operator info                                         |
+--------------------+---------+-----------+--------------------------------------------------+-------------------------------------------------------+
| IndexReader_6      | 1.27    | root      |                                                  | index:IndexRangeScan_5                                |
| └─IndexRangeScan_5 | 1.27    | cop[tikv] | table:books, index:title_price_idx(title, price) | range:["Marian Yost","Marian Yost"], keep order:false |
+--------------------+---------+-----------+--------------------------------------------------+-------------------------------------------------------+
```

现在这个查询运行得更快：

```sql
SELECT title, price FROM books WHERE title = 'Marian Yost';
```

```sql
+-------------+--------+
| title       | price  |
+-------------+--------+
| Marian Yost | 174.64 |
| Marian Yost | 328.18 |
| Marian Yost | 402.90 |
| Marian Yost | 435.01 |
| Marian Yost | 496.52 |
+-------------+--------+
5 rows in set
Time: 0.004s
```

由于 `books` 表将在后面的示例中使用，删除 `title_price_idx` 索引：

```sql
ALTER TABLE books DROP INDEX title_price_idx;
```

### 解决方案：使用主键索引

如果查询使用主键过滤数据，查询运行速度很快。例如，`books` 表的主键是 `id` 列，所以你可以使用 `id` 列查询数据：

```sql
SELECT * FROM books WHERE id = 896;
```

```sql
+-----+----------------+----------------------+---------------------+-------+--------+
| id  | title          | type                 | published_at        | stock | price  |
+-----+----------------+----------------------+---------------------+-------+--------+
| 896 | Kathryne Doyle | Science & Technology | 1969-03-18 01:34:15 | 468   | 281.32 |
+-----+----------------+----------------------+---------------------+-------+--------+
1 row in set
Time: 0.004s
```

使用 `EXPLAIN` 查看执行计划：

```sql
EXPLAIN SELECT * FROM books WHERE id = 896;
```

```sql
+-------------+---------+------+---------------+---------------+
| id          | estRows | task | access object | operator info |
+-------------+---------+------+---------------+---------------+
| Point_Get_1 | 1.00    | root | table:books   | handle:896    |
+-------------+---------+------+---------------+---------------+
```

`Point_Get` 是一个非常快的执行计划。

## 使用正确的连接类型

请参见[连接的执行计划](/explain-joins.md)。

### 另请参阅

* [EXPLAIN 详解](/explain-walkthrough.md)
* [使用索引的执行计划](/explain-indexes.md)

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上询问社区，或[提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上询问社区，或[提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>
