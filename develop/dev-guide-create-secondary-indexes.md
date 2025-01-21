---
title: 创建二级索引
summary: 创建二级索引的方法、规范及例子。
aliases: ['/zh/tidb/dev/create-secondary-indexes']
---

# 创建二级索引

在这个章节当中，将开始介绍如何使用 SQL 来创建二级索引，及创建二级索引时应遵守的规则。将在这个章节中围绕 [Bookshop](/develop/dev-guide-bookshop-schema-design.md) 这个应用程序来对 TiDB 的创建二级索引部分展开介绍。

## 在开始之前

在阅读本页面之前，你需要准备以下事项：

- [使用 TiDB Cloud Serverless 构建 TiDB 集群](/develop/dev-guide-build-cluster-in-cloud.md)。
- 阅读[数据库模式概览](/develop/dev-guide-schema-design-overview.md)。
- [创建一个数据库](/develop/dev-guide-create-database.md)。
- [创建表](/develop/dev-guide-create-table.md)。

## 什么是二级索引

二级索引是集群中的逻辑对象，你可以简单地认为它就是一种对数据的排序，TiDB 使用这种有序性来加速查询。TiDB 的创建二级索引的操作为在线操作，不会阻塞表中的数据读写。TiDB 会创建表中各行的引用，并按选择的列进行排序。而并非对表本身的数据进行排序。可在[二级索引](/best-practices/tidb-best-practices.md#二级索引)中查看更多信息。二级索引可[跟随表进行创建](#新建表的同时创建二级索引)，也可[在已有的表上进行添加](#在已有表中添加二级索引)。

## 在已有表中添加二级索引

如果需要对已有表中添加二级索引，可使用 [CREATE INDEX](/sql-statements/sql-statement-create-index.md) 语句。在 TiDB 中，`CREATE INDEX` 为在线操作，不会阻塞表中的数据读写。二级索引创建一般如以下形式：

```sql
CREATE INDEX {index_name} ON {table_name} ({column_names});
```

**参数描述**

- `{index_name}`: 二级索引名。
- `{table_name}`: 表名。
- `{column_names}`: 将需要索引的列名列表，以半角逗号分隔。

## 新建表的同时创建二级索引

如果你希望在创建表的同时，同时创建二级索引，可在 [CREATE TABLE](/sql-statements/sql-statement-create-table.md) 的末尾使用包含 `KEY` 关键字的子句来创建二级索引：

```sql
KEY `{index_name}` (`{column_names}`)
```

**参数描述**

- `{index_name}`: 二级索引名。
- `{column_names}`: 将需要索引的列名列表，以半角逗号分隔。

## 创建二级索引时应遵守的规则

见[索引的最佳实践](/develop/dev-guide-index-best-practice.md)。

## 例子

假设你希望 `bookshop` 应用程序有 **查询某个年份出版的所有书籍** 的功能。`books` 表如下所示:

|    字段名    |     类型      |                 含义                  |
| :----------: | :-----------: | :-----------------------------------: |
|      id      |  bigint   |            书籍的唯一标识             |
|    title     | varchar(100)  |               书籍名称                |
|     type     |     enum      | 书籍类型（如：杂志、动漫、教辅等） |
|    stock     |  bigint   |                 库存                  |
|    price     | decimal(15,2) |                 价格                  |
| published_at |   datetime    |               出版时间                |

```sql
CREATE TABLE `bookshop`.`books` (
  `id` bigint AUTO_RANDOM NOT NULL,
  `title` varchar(100) NOT NULL,
  `type` enum('Magazine', 'Novel', 'Life', 'Arts', 'Comics', 'Education & Reference', 'Humanities & Social Sciences', 'Science & Technology', 'Kids', 'Sports') NOT NULL,
  `published_at` datetime NOT NULL,
  `stock` int DEFAULT '0',
  `price` decimal(15,2) DEFAULT '0.0',
  PRIMARY KEY (`id`) CLUSTERED
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
```

因此，就需要对 **查询某个年份出版的所有书籍** 的 SQL 进行编写，以 2022 年为例，如下所示：

```sql
SELECT * FROM `bookshop`.`books` WHERE `published_at` >= '2022-01-01 00:00:00' AND `published_at` < '2023-01-01 00:00:00';
```

可以使用 [EXPLAIN](/sql-statements/sql-statement-explain.md) 进行 SQL 语句的执行计划检查：

```sql
EXPLAIN SELECT * FROM `bookshop`.`books` WHERE `published_at` >= '2022-01-01 00:00:00' AND `published_at` < '2023-01-01 00:00:00';
```

运行结果为：

```
+-------------------------+----------+-----------+---------------+--------------------------------------------------------------------------------------------------------------------------+
| id                      | estRows  | task      | access object | operator info                                                                                                            |
+-------------------------+----------+-----------+---------------+--------------------------------------------------------------------------------------------------------------------------+
| TableReader_7           | 346.32   | root      |               | data:Selection_6                                                                                                         |
| └─Selection_6           | 346.32   | cop[tikv] |               | ge(bookshop.books.published_at, 2022-01-01 00:00:00.000000), lt(bookshop.books.published_at, 2023-01-01 00:00:00.000000) |
|   └─TableFullScan_5     | 20000.00 | cop[tikv] | table:books   | keep order:false                                                                                                         |
+-------------------------+----------+-----------+---------------+--------------------------------------------------------------------------------------------------------------------------+
3 rows in set (0.61 sec)
```

可以看到返回的计划中，出现了类似 **TableFullScan** 的字样，这代表 TiDB 准备在这个查询中对 `books` 表进行全表扫描，这在数据量较大的情况下，几乎是致命的。

在 `books` 表增加一个 `published_at` 列的索引：

```sql
CREATE INDEX `idx_book_published_at` ON `bookshop`.`books` (`bookshop`.`books`.`published_at`);
```

添加索引后，再次运行 `EXPLAIN` 语句检查执行计划：

```
+-------------------------------+---------+-----------+--------------------------------------------------------+-------------------------------------------------------------------+
| id                            | estRows | task      | access object                                          | operator info                                                     |
+-------------------------------+---------+-----------+--------------------------------------------------------+-------------------------------------------------------------------+
| IndexLookUp_10                | 146.01  | root      |                                                        |                                                                   |
| ├─IndexRangeScan_8(Build)     | 146.01  | cop[tikv] | table:books, index:idx_book_published_at(published_at) | range:[2022-01-01 00:00:00,2023-01-01 00:00:00), keep order:false |
| └─TableRowIDScan_9(Probe)     | 146.01  | cop[tikv] | table:books                                            | keep order:false                                                  |
+-------------------------------+---------+-----------+--------------------------------------------------------+-------------------------------------------------------------------+
3 rows in set (0.18 sec)
```

可以看到执行计划中没有了 **TableFullScan** 的字样，取而代之的是 **IndexRangeScan**，这代表已经 TiDB 在进行这个查询时准备使用索引。

> **注意：**
>
> 上方执行计划中的的 **TableFullScan**、**IndexRangeScan** 等在 TiDB 内被称为[算子](/explain-overview.md#算子简介)。这里对执行计划的解读及算子等不做进一步的展开，若你对此感兴趣，可前往 [TiDB 执行计划概览](/explain-overview.md)文档查看更多关于执行计划与 TiDB 算子的相关知识。
>
> 执行计划并非每次返回使用的算子都相同，这是由于 TiDB 使用的优化方式为 **基于代价的优化方式 (CBO)**，执行计划不仅与规则相关，还和数据分布相关。你可以前往 [SQL 性能调优](/sql-tuning-overview.md)文档查看更多 TiDB SQL 性能的描述。
>
> TiDB 在查询时，还支持显式地使用索引，你可以使用 [Optimizer Hints](/optimizer-hints.md) 或[执行计划管理 (SPM)](/sql-plan-management.md) 来人为的控制索引的使用。但如果你不了解它内部发生了什么，请你**_暂时先不要使用它_**。

可以使用 [SHOW INDEXES](/sql-statements/sql-statement-show-indexes.md) 语句查询表中的索引：

```sql
SHOW INDEXES FROM `bookshop`.`books`;
```

运行结果为：

```
+-------+------------+-----------------------+--------------+--------------+-----------+-------------+----------+--------+------+------------+---------+---------------+---------+------------+-----------+
| Table | Non_unique | Key_name              | Seq_in_index | Column_name  | Collation | Cardinality | Sub_part | Packed | Null | Index_type | Comment | Index_comment | Visible | Expression | Clustered |
+-------+------------+-----------------------+--------------+--------------+-----------+-------------+----------+--------+------+------------+---------+---------------+---------+------------+-----------+
| books |          0 | PRIMARY               |            1 | id           | A         |           0 |     NULL | NULL   |      | BTREE      |         |               | YES     | NULL       | YES       |
| books |          1 | idx_book_published_at |            1 | published_at | A         |           0 |     NULL | NULL   |      | BTREE      |         |               | YES     | NULL       | NO        |
+-------+------------+-----------------------+--------------+--------------+-----------+-------------+----------+--------+------+------------+---------+---------------+---------+------------+-----------+
2 rows in set (1.63 sec)
```

## 更进一步

至此，你已经完成数据库、表及二级索引的创建，接下来，数据库模式已经准备好给你的应用程序提供[写入](/develop/dev-guide-insert-data.md)和[读取](/develop/dev-guide-get-data-from-single-table.md)的能力了。
