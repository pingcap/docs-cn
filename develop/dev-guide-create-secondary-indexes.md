---
title: 创建二级索引
summary: 学习创建二级索引的步骤、规则和示例。
---

# 创建二级索引

本文介绍如何使用 SQL 和各种编程语言创建二级索引，并列出了索引创建的规则。在本文中，以 [Bookshop](/develop/dev-guide-bookshop-schema-design.md) 应用程序为例，引导你完成二级索引创建的步骤。

## 开始之前

在创建二级索引之前，请执行以下操作：

- [构建 TiDB Cloud Serverless 集群](/develop/dev-guide-build-cluster-in-cloud.md)。
- 阅读[架构设计概述](/develop/dev-guide-schema-design-overview.md)。
- [创建数据库](/develop/dev-guide-create-database.md)。
- [创建表](/develop/dev-guide-create-table.md)。

## 什么是二级索引

二级索引是 TiDB 集群中的一个逻辑对象。你可以简单地将其视为 TiDB 用来提高查询性能的一种数据排序方式。在 TiDB 中，创建二级索引是一个在线操作，不会阻塞表上的任何数据读写操作。对于每个索引，TiDB 为表中的每一行创建引用，并按选定的列对引用进行排序，而不是直接对数据进行排序。

<CustomContent platform="tidb">

有关二级索引的更多信息，请参阅[二级索引](/best-practices/tidb-best-practices.md#secondary-index)。

</CustomContent>

<CustomContent platform="tidb-cloud">

有关二级索引的更多信息，请参阅[二级索引](https://docs.pingcap.com/tidb/stable/tidb-best-practices#secondary-index)。

</CustomContent>

在 TiDB 中，你可以[为现有表添加二级索引](#为现有表添加二级索引)或[在创建新表时创建二级索引](#在创建新表时创建二级索引)。

## 为现有表添加二级索引

要为现有表添加二级索引，你可以使用 [CREATE INDEX](/sql-statements/sql-statement-create-index.md) 语句，如下所示：

```sql
CREATE INDEX {index_name} ON {table_name} ({column_names});
```

参数说明：

- `{index_name}`：二级索引的名称。
- `{table_name}`：表名。
- `{column_names}`：要建立索引的列名，用逗号分隔。

## 在创建新表时创建二级索引

要在创建表的同时创建二级索引，你可以在 [CREATE TABLE](/sql-statements/sql-statement-create-table.md) 语句的末尾添加包含 `KEY` 关键字的子句：

```sql
KEY `{index_name}` (`{column_names}`)
```

参数说明：

- `{index_name}`：二级索引的名称。
- `{column_names}`：要建立索引的列名，用逗号分隔。

## 创建二级索引的规则

请参阅[索引的最佳实践](/develop/dev-guide-index-best-practice.md)。

## 示例

假设你希望 `bookshop` 应用程序支持**搜索指定年份发布的所有图书**。

`books` 表中的字段如下：

| 字段名        | 类型          | 字段说明                                                          |
|--------------|---------------|------------------------------------------------------------------|
| id           | bigint(20)    | 图书的唯一 ID                                                     |
| title        | varchar(100)  | 图书标题                                                          |
| type         | enum          | 图书类型（例如，杂志、动漫和教辅）                                  |
| stock        | bigint(20)    | 库存                                                              |
| price        | decimal(15,2) | 价格                                                              |
| published_at | datetime      | 发布日期                                                          |

使用以下 SQL 语句创建 `books` 表：

```sql
CREATE TABLE `bookshop`.`books` (
  `id` bigint(20) AUTO_RANDOM NOT NULL,
  `title` varchar(100) NOT NULL,
  `type` enum('Magazine', 'Novel', 'Life', 'Arts', 'Comics', 'Education & Reference', 'Humanities & Social Sciences', 'Science & Technology', 'Kids', 'Sports') NOT NULL,
  `published_at` datetime NOT NULL,
  `stock` int(11) DEFAULT '0',
  `price` decimal(15,2) DEFAULT '0.0',
  PRIMARY KEY (`id`) CLUSTERED
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
```

要支持按年份搜索功能，你需要编写一个 SQL 语句来**搜索指定年份发布的所有图书**。以 2022 年为例，编写如下 SQL 语句：

```sql
SELECT * FROM `bookshop`.`books` WHERE `published_at` >= '2022-01-01 00:00:00' AND `published_at` < '2023-01-01 00:00:00';
```

要检查 SQL 语句的执行计划，你可以使用 [`EXPLAIN`](/sql-statements/sql-statement-explain.md) 语句。

```sql
EXPLAIN SELECT * FROM `bookshop`.`books` WHERE `published_at` >= '2022-01-01 00:00:00' AND `published_at` < '2023-01-01 00:00:00';
```

以下是执行计划的示例输出：

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

在示例输出中，`id` 列显示了 **TableFullScan**，这意味着 TiDB 准备在这个查询中对 `books` 表进行全表扫描。然而，在数据量较大的情况下，全表扫描可能会非常慢，并造成致命影响。

为避免这种影响，你可以为 `books` 表的 `published_at` 列添加一个索引，如下所示：

```sql
CREATE INDEX `idx_book_published_at` ON `bookshop`.`books` (`bookshop`.`books`.`published_at`);
```

添加索引后，再次执行 `EXPLAIN` 语句来检查执行计划。

以下是示例输出：

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

在输出中，显示了 **IndexRangeScan** 而不是 **TableFullScan**，这意味着 TiDB 准备使用索引来执行这个查询。

执行计划中的 **TableFullScan** 和 **IndexRangeScan** 等词是 TiDB 中的[算子](/explain-overview.md#operator-overview)。有关执行计划和算子的更多信息，请参阅 [TiDB 执行计划概览](/explain-overview.md)。

<CustomContent platform="tidb">

执行计划不会每次都返回相同的算子。这是因为 TiDB 使用**基于成本的优化 (CBO)** 方法，其中执行计划取决于规则和数据分布。有关 TiDB SQL 性能的更多信息，请参阅 [SQL 调优概述](/sql-tuning-overview.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

执行计划不会每次都返回相同的算子。这是因为 TiDB 使用**基于成本的优化 (CBO)** 方法，其中执行计划取决于规则和数据分布。有关 TiDB SQL 性能的更多信息，请参阅 [SQL 调优概述](/tidb-cloud/tidb-cloud-sql-tuning-overview.md)。

</CustomContent>

> **注意：**
>
> TiDB 还支持在查询时显式使用索引，你可以使用[优化器提示](/optimizer-hints.md)或 [SQL 计划管理 (SPM)](/sql-plan-management.md)来人为控制索引的使用。但如果你对索引、优化器提示或 SPM 不够了解，**不要**使用此功能，以避免任何意外结果。

要查询表上的索引，你可以使用 [SHOW INDEXES](/sql-statements/sql-statement-show-indexes.md) 语句：

```sql
SHOW INDEXES FROM `bookshop`.`books`;
```

以下是示例输出：

```
+-------+------------+-----------------------+--------------+--------------+-----------+-------------+----------+--------+------+------------+---------+---------------+---------+------------+-----------+
| Table | Non_unique | Key_name              | Seq_in_index | Column_name  | Collation | Cardinality | Sub_part | Packed | Null | Index_type | Comment | Index_comment | Visible | Expression | Clustered |
+-------+------------+-----------------------+--------------+--------------+-----------+-------------+----------+--------+------+------------+---------+---------------+---------+------------+-----------+
| books |          0 | PRIMARY               |            1 | id           | A         |           0 |     NULL | NULL   |      | BTREE      |         |               | YES     | NULL       | YES       |
| books |          1 | idx_book_published_at |            1 | published_at | A         |           0 |     NULL | NULL   |      | BTREE      |         |               | YES     | NULL       | NO        |
+-------+------------+-----------------------+--------------+--------------+-----------+-------------+----------+--------+------+------------+---------+---------------+---------+------------+-----------+
2 rows in set (1.63 sec)
```

## 下一步

在创建数据库并向其添加表和二级索引后，你可以开始向应用程序添加数据[写入](/develop/dev-guide-insert-data.md)和[读取](/develop/dev-guide-get-data-from-single-table.md)功能。

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上询问社区，或[提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上询问社区，或[提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>
