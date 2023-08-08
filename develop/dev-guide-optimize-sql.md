---
title: SQL 性能调优
summary: 介绍 TiDB 的 SQL 性能调优方案和分析办法。
---

# SQL 性能调优

本章介绍常见的 SQL 性能调优，你将会了解导致 SQL 执行慢的常见的原因。

## 准备工作

在开始之前，你可以[通过 `tiup demo` 命令导入](/develop/dev-guide-bookshop-schema-design.md#方法一通过-tiup-demo-命令行)示例数据：

```shell
tiup demo bookshop prepare --books 1000000 --host 127.0.0.1 --port 4000
```

或[使用 TiDB Cloud 的 Import 功能导入](/develop/dev-guide-bookshop-schema-design.md#方法二通过-tidb-cloud-import-功能)预先准备好的示例数据。

## 问题：全表扫描

慢查询最常见的原因就是 `SELECT` 语句执行是全表扫描，或者是用了不合适的索引。

当基于不在主键或任何二级索引中的列从大表中检索少量行时，通常会获得较差的性能：

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

可以使用 `EXPLAIN` 来查看这个查询的执行计划，看看为什么查询这么慢：

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

从执行计划中的 **TableFullScan_5** 可以看出，TiDB 将会对表 `books` 进行全表扫描，然后对每一行都判断 `title` 是否满足条件。**TableFullScan_5** 的 `estRows` 值为 `1000000.00`，说明优化器估计这个全表扫描会扫描 `1000000.00` 行数据。

更多关于 `EXPLAIN` 的使用介绍，可以阅读[使用 EXPLAIN 解读执行计划](/explain-walkthrough.md)。

### 解决方案：使用索引过滤数据

为了加速上面的查询，可以在 `books.title` 列创建一个索引：

```sql
CREATE INDEX title_idx ON books (title);
```

现在再执行这个查询将会快很多：

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

可以使用 `EXPLAIN` 来查看这个查询的执行计划，看看为什么查询变快了：

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

从执行计划中的 **IndexLookUp_10** 可以看出，TiDB 将会通过索引 `title_idx` 来查询数据，其 `estRows` 值为 `1.27`，说明优化器估计只会扫描 `1.27` 行数据，远远小于之前全表扫的 `1000000.00` 行数据。

**IndexLookUp_10** 执行计划的执行流程是先用 **IndexRangeScan_8** 算子通过 `title_idx` 索引获取符合条件的索引数据，然后 **TableRowIDScan_9** 再更据索引数据里面的 Row ID 回表查询相应的行数据。

更多关于 TiDB 执行计划的内容，可以阅读[TiDB 执行计划概览](/explain-overview.md)。

### 解决方案：使用索引查询数据

上述解决方案中，需要先读取索引信息，再回表查询对应的行数据。但如果索引数据中包含了 SQL 查询所需的所有信息，就可以省去回表查询这个步骤。

例如下面查询中，仅需要根据 `title` 查询对应的 `price`：

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

由于索引 `title_idx` 仅包含 `title` 列的信息，所以 TiDB 还是需要扫描索引数据，然后回表查询 `price` 数据：

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

删除 `title_idx` 索引，并新建一个 `title_price_idx` 索引：

```sql
ALTER TABLE books DROP INDEX title_idx;
```

```sql
CREATE INDEX title_price_idx ON books (title, price);
```

现在，`price` 数据已经存储在索引 `title_price_idx` 中了，所以下面查询仅需扫描索引数据，无需回表查询了。这种索引通常被叫做覆盖索引：

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

现在这条查询的速度将会更快：

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

由于后面的示例还会用到这个库，删除 `title_price_idx` 索引。

```sql
ALTER TABLE books DROP INDEX title_price_idx;
```

### 解决方案：使用主键查询数据

如果查询中使用主键过滤数据，这条查询的执行速度会非常快，例如表 `books` 的主键是列 `id`，使用列 `id` 来查询数据：

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

使用 `EXPLAIN` 查看执行计划:

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

**Point_Get**，又名 “点查”，它的执行速度也非常快。

## 选择合适的 Join 执行计划

见 [JOIN 查询的执行计划](/explain-joins.md)。

## 推荐阅读

- [使用 EXPLAIN 解读执行计划](/explain-walkthrough.md)。
- [用 EXPLAIN 查看索引查询的执行计划](/explain-indexes.md)。
