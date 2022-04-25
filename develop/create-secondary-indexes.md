---
title: 创建二级索引
---

# 创建二级索引

索引是集群中的逻辑对象，可以帮助 TiDB 集群查询 更有效的查找数据。当您创建二级索引时，TiDB 会创建一个表中各行的引用，并按选择的列进行排序。而并非对表本身的数据进行排序。可在[此文档](https://docs.pingcap.com/zh/tidb/stable/tidb-best-practices#%E4%BA%8C%E7%BA%A7%E7%B4%A2%E5%BC%95)中查看关于二级索引的更多信息。

此页面提供了一个创建二级索引的最佳实践指南，并提供了一个基于 TiDB 的 [bookshop](/develop/bookshop-schema-design.md) 数据库的示例。

## 在开始之前

在阅读本页面之前，你需要准备以下事项：

- [使用 TiDB Cloud(DevTier) 构建 TiDB 集群](/develop/build-cluster-in-cloud.md)
- 阅读[数据库模式概览](/develop/schema-design-overview.md)
- [创建一个数据库](/develop/create-database.md)
- [创建表](/develop/create-table.md)

## 创建二级索引

### 在已有表中添加二级索引

如果需要对已有表中添加二级索引，可使用 [CREATE INDEX](https://docs.pingcap.com/zh/tidb/stable/sql-statement-create-index) 语句。在 TiDB 中，`CREATE INDEX` 为在线操作，不会阻塞表中的数据读写。二级索引创建一般如以下形式：

```sql
CREATE INDEX {index_name} ON {table_name} ({column_names});
```

|       参数       |                 描述                 |
| :--------------: | :----------------------------------: |
|  `{index_name}`  |              二级索引名              |
|  `{table_name}`  |                 表名                 |
| `{column_names}` | 将需要索引的列名列表，以半角逗号分隔 |

### 新建表的同时创建二级索引

如果您希望在创建表的同时，同时创建二级索引，可在 [CREATE TABLE](https://docs.pingcap.com/zh/tidb/stable/sql-statement-create-table) 的末尾使用包含 `KEY` 关键字的子句来创建二级索引：

```sql
KEY `{index_name}` (`{column_names}`)
```

|       参数       |                 描述                 |
| :--------------: | :----------------------------------: |
|  `{index_name}`  |              二级索引名              |
| `{column_names}` | 将需要索引的列名列表，以半角逗号分隔 |

## 最佳实践

以下是创建和使用索引时的一些最佳实践：

- 建立您需要使用的数据的所有列的索引，这种优化技巧被称为 [覆盖索引优化(covering index optimization)](https://docs.pingcap.com/zh/tidb/stable/explain-indexes#indexreader)。`覆盖索引优化` 将使得 TiDB 可以直接在索引上得到该查询所需的所有数据，可以大幅提升性能。
- 避免创建你不需要的二级索引，二级索引能加速查询，但是要注意新增一个索引是有副作用的。每增加一个索引，在插入一条数据的时候，就要新增一个 Key-Value，所以索引越多，写入越慢，并且空间占用越大。另外过多的索引也会影响优化器运行时间，并且不合适的索引会误导优化器。所以索引并不是越多越好。
- 根据具体的业务特点创建合适的索引。原则上需要对查询中需要用到的列创建索引，目的是提高性能。下面几种情况适合创建索引：
    - 区分度比较大的列，通过索引能显著地减少过滤后的行数
    - 有多个查询条件时，可以选择组合索引，注意需要把等值条件的列放在组合索引的前面
      这里举一个例子，假设常用的查询是 `select * from t where c1 = 10 and c2 = 100 and c3 > 10`, 那么可以考虑建立组合索引 `Index cidx (c1, c2, c3)`，这样可以用查询条件构造出一个索引前缀进行 Scan。
- 请使用有意义的二级索引名，我们推荐你遵循公司或组织的表命名规范。如果您的公司或组织没有相应的命名规范，可参考[索引命名规范](/develop/object-naming-guidelines.md#5-索引命名规范)。

## 例子

假设您希望 `bookshop` 应用程序有 `查询某个年份出版的所有书籍` 的功能。我们的 `books` 表如下所示:

|    字段名    |     类型      |                 含义                  |
| :----------: | :-----------: | :-----------------------------------: |
|      id      |  bigint(20)   |            书籍的唯一标识             |
|    title     | varchar(100)  |               书籍名称                |
|     type     |     enum      | 书籍类型（如：杂志 / 动漫 / 教辅 等） |
|    stock     |  bigint(20)   |                 库存                  |
|    price     | decimal(15,2) |                 价格                  |
| published_at |   datetime    |               出版时间                |

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

那么，我们就需要对 `查询某个年份出版的所有书籍` 的 SQL 进行编写， 以 2022 年为例，如下所示：

```sql
SELECT * FROM `bookshop`.`books` WHERE `published_at` >= '2022-01-01 00:00:00' AND `published_at` < '2023-01-01 00:00:00';
```

我们可以使用 [EXPLAIN](https://docs.pingcap.com/zh/tidb/stable/sql-statement-explain) 进行 SQL 语句的执行计划检查：

```sql
EXPLAIN SELECT * FROM `bookshop`.`books` WHERE `published_at` >= '2022-01-01 00:00:00' AND `published_at` < '2023-01-01 00:00:00';
```

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

可以看到返回的计划中，出现了类似 `TableFullScan` 的字样，这代表 TiDB 准备在这个查询中对 `books` 表进行全表扫描，这在数据量较大的情况下，几乎是致命的。

我们在 `books` 表增加一个 `published_at` 列的索引：

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

可以看到执行计划中没有了 `TableFullScan` 的字样，取而代之的是 `IndexRangeScan`，这代表已经 TiDB 在进行这个查询时准备使用索引。

> Note:
>
> 上方执行计划中的的 `TableFullScan`、`IndexRangeScan` 等在 TiDB 内被称为[算子](https://docs.pingcap.com/zh/tidb/stable/explain-overview#%E7%AE%97%E5%AD%90%E7%AE%80%E4%BB%8B)。这里对执行计划的解读及算子等不做进一步的展开，若您对此感兴趣，可点击[此处](https://docs.pingcap.com/zh/tidb/stable/explain-overview)查看更多关于执行计划与 TiDB 算子的相关知识。
>
> 执行计划并非每次返回使用的算子都相同，这是由于 TiDB 使用的优化方式为 `基于代价的优化方式 (CBO)`，执行计划不仅与规则相关，还和数据分布相关。您可以参阅[此处](https://docs.pingcap.com/zh/tidb/stable/sql-tuning-overview)获得更多 TiDB SQL 性能的描述。
>
> TiDB 在查询时，还支持显示的使用索引，你可以使用 [Optimizer Hints](https://docs.pingcap.com/zh/tidb/stable/optimizer-hints) 或 [执行计划管理 (SPM)](https://docs.pingcap.com/zh/tidb/stable/sql-plan-management) 来人为的控制索引的使用。但如果你不了解它内部发生了什么，请你**_暂时先不要使用它_**。

我们可以使用 [SHOW INDEXES](https://docs.pingcap.com/zh/tidb/stable/sql-statement-show-indexes) 语句查询表中的索引。

```sql
SHOW INDEXES FROM `bookshop`.`books`;
```

```
+-------+------------+-----------------------+--------------+--------------+-----------+-------------+----------+--------+------+------------+---------+---------------+---------+------------+-----------+
| Table | Non_unique | Key_name              | Seq_in_index | Column_name  | Collation | Cardinality | Sub_part | Packed | Null | Index_type | Comment | Index_comment | Visible | Expression | Clustered |
+-------+------------+-----------------------+--------------+--------------+-----------+-------------+----------+--------+------+------------+---------+---------------+---------+------------+-----------+
| books |          0 | PRIMARY               |            1 | id           | A         |           0 |     NULL | NULL   |      | BTREE      |         |               | YES     | NULL       | YES       |
| books |          1 | idx_book_published_at |            1 | published_at | A         |           0 |     NULL | NULL   |      | BTREE      |         |               | YES     | NULL       | NO        |
+-------+------------+-----------------------+--------------+--------------+-----------+-------------+----------+--------+------+------------+---------+---------------+---------+------------+-----------+
2 rows in set (1.63 sec)
```

至此，您已经完成数据库、表及二级索引的创建，接下来，数据库模式已经准备好给您的应用程序提供 [写入](/develop/insert-data.md) 和 [读取](/develop/get-data-from-single-table.md) 读取的能力了。
