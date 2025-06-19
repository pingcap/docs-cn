---
title: HTAP 查询
summary: 介绍 TiDB 中的 HTAP 查询。
---

# HTAP 查询

HTAP 代表混合事务和分析处理（Hybrid Transactional and Analytical Processing）。传统上，数据库通常针对事务或分析场景进行设计，因此数据平台经常需要拆分为事务处理和分析处理，并且需要将数据从事务数据库复制到分析数据库以快速响应分析查询。TiDB 数据库可以同时执行事务和分析任务，这大大简化了数据平台的构建，并允许用户使用更新鲜的数据进行分析。

TiDB 使用行式存储引擎 TiKV 进行在线事务处理（OLTP），使用列式存储引擎 TiFlash 进行在线分析处理（OLAP）。行式存储引擎和列式存储引擎共存以实现 HTAP。两种存储引擎都可以自动复制数据并保持强一致性。行式存储引擎优化 OLTP 性能，列式存储引擎优化 OLAP 性能。

[创建表](/develop/dev-guide-create-table.md#use-htap-capabilities)部分介绍了如何启用 TiDB 的 HTAP 功能。以下介绍如何使用 HTAP 更快地分析数据。

## 数据准备

在开始之前，你可以[通过 `tiup demo` 命令](/develop/dev-guide-bookshop-schema-design.md#method-1-via-tiup-demo)导入更多示例数据。例如：

```shell
tiup demo bookshop prepare --users=200000 --books=500000 --authors=100000 --ratings=1000000 --orders=1000000 --host 127.0.0.1 --port 4000 --drop-tables
```

或者你可以[使用 TiDB Cloud 的导入功能](/develop/dev-guide-bookshop-schema-design.md#method-2-via-tidb-cloud-import)导入预先准备好的示例数据。

## 窗口函数

在使用数据库时，除了存储数据和提供应用功能（如订购和评价图书）外，你可能还需要分析数据库中的数据以进行进一步的操作和决策。

[从单表查询数据](/develop/dev-guide-get-data-from-single-table.md)文档介绍了如何使用聚合查询来整体分析数据。在更复杂的场景中，你可能想要将多个聚合查询的结果聚合到一个查询中。如果你想知道特定图书订单金额的历史趋势，你可以对每个月的所有订单数据进行 `sum` 聚合，然后将 `sum` 结果聚合在一起以获得历史趋势。

为了便于此类分析，从 TiDB v3.0 开始，TiDB 支持窗口函数。对于每一行数据，此函数提供了跨多行访问数据的能力。与常规聚合查询不同，窗口函数在聚合行时不会将结果集合并为单行。

与聚合函数类似，在使用窗口函数时也需要遵循固定的语法集：

```sql
SELECT
    window_function() OVER ([partition_clause] [order_clause] [frame_clause]) AS alias
FROM
    table_name
```

### `ORDER BY` 子句

使用聚合窗口函数 `sum()`，你可以分析特定图书订单金额的历史趋势。例如：

```sql
WITH orders_group_by_month AS (
  SELECT DATE_FORMAT(ordered_at, '%Y-%c') AS month, COUNT(*) AS orders
  FROM orders
  WHERE book_id = 3461722937
  GROUP BY 1
)
SELECT
month,
SUM(orders) OVER(ORDER BY month ASC) as acc
FROM orders_group_by_month
ORDER BY month ASC;
```

`sum()` 函数按照 `OVER` 子句中 `ORDER BY` 语句指定的顺序累积数据。结果如下：

```
+---------+-------+
| month   | acc   |
+---------+-------+
| 2011-5  |     1 |
| 2011-8  |     2 |
| 2012-1  |     3 |
| 2012-2  |     4 |
| 2013-1  |     5 |
| 2013-3  |     6 |
| 2015-11 |     7 |
| 2015-4  |     8 |
| 2015-8  |     9 |
| 2017-11 |    10 |
| 2017-5  |    11 |
| 2019-5  |    13 |
| 2020-2  |    14 |
+---------+-------+
13 rows in set (0.01 sec)
```

通过以时间为横轴、累计订单金额为纵轴的折线图可视化上述数据。你可以通过斜率的变化轻松了解该书的历史订购趋势。

### `PARTITION BY` 子句

假设你想分析不同类型图书的历史订购趋势，并在同一个折线图中以多个系列进行可视化。

你可以使用 `PARTITION BY` 子句按类型对图书进行分组，并分别统计每种类型的历史订单。

```sql
WITH orders_group_by_month AS (
    SELECT
        b.type AS book_type,
        DATE_FORMAT(ordered_at, '%Y-%c') AS month,
        COUNT(*) AS orders
    FROM orders o
    LEFT JOIN books b ON o.book_id = b.id
    WHERE b.type IS NOT NULL
    GROUP BY book_type, month
), acc AS (
    SELECT
        book_type,
        month,
        SUM(orders) OVER(PARTITION BY book_type ORDER BY book_type, month ASC) as acc
    FROM orders_group_by_month
    ORDER BY book_type, month ASC
)
SELECT * FROM acc;
```

结果如下：

```
+------------------------------+---------+------+
| book_type                    | month   | acc  |
+------------------------------+---------+------+
| Magazine                     | 2011-10 |    1 |
| Magazine                     | 2011-8  |    2 |
| Magazine                     | 2012-5  |    3 |
| Magazine                     | 2013-1  |    4 |
| Magazine                     | 2013-6  |    5 |
...
| Novel                        | 2011-3  |   13 |
| Novel                        | 2011-4  |   14 |
| Novel                        | 2011-6  |   15 |
| Novel                        | 2011-8  |   17 |
| Novel                        | 2012-1  |   18 |
| Novel                        | 2012-2  |   20 |
...
| Sports                       | 2021-4  |   49 |
| Sports                       | 2021-7  |   50 |
| Sports                       | 2022-4  |   51 |
+------------------------------+---------+------+
1500 rows in set (1.70 sec)
```

### 非聚合窗口函数

TiDB 还提供了一些非聚合的[窗口函数](/functions-and-operators/window-functions.md)用于更多分析语句。

例如，[分页查询](/develop/dev-guide-paginate-results.md)文档介绍了如何使用 `row_number()` 函数实现高效的分页批处理。

## 混合负载

在混合负载场景中使用 TiDB 进行实时在线分析处理时，你只需要为你的数据提供一个 TiDB 入口点。TiDB 会根据具体业务自动选择不同的处理引擎。

### 创建 TiFlash 副本

TiDB 默认使用行式存储引擎 TiKV。要使用列式存储引擎 TiFlash，请参阅[启用 HTAP 功能](/develop/dev-guide-create-table.md#use-htap-capabilities)。在通过 TiFlash 查询数据之前，你需要使用以下语句为 `books` 和 `orders` 表创建 TiFlash 副本：

```sql
ALTER TABLE books SET TIFLASH REPLICA 1;
ALTER TABLE orders SET TIFLASH REPLICA 1;
```

你可以使用以下语句检查 TiFlash 副本的进度：

```sql
SELECT * FROM information_schema.tiflash_replica WHERE TABLE_SCHEMA = 'bookshop' and TABLE_NAME = 'books';
SELECT * FROM information_schema.tiflash_replica WHERE TABLE_SCHEMA = 'bookshop' and TABLE_NAME = 'orders';
```

`PROGRESS` 列为 1 表示进度为 100% 完成，`AVAILABLE` 列为 1 表示副本当前可用。

```
+--------------+------------+----------+---------------+-----------------+-----------+----------+
| TABLE_SCHEMA | TABLE_NAME | TABLE_ID | REPLICA_COUNT | LOCATION_LABELS | AVAILABLE | PROGRESS |
+--------------+------------+----------+---------------+-----------------+-----------+----------+
| bookshop     | books      |      143 |             1 |                 |         1 |        1 |
+--------------+------------+----------+---------------+-----------------+-----------+----------+
1 row in set (0.07 sec)
+--------------+------------+----------+---------------+-----------------+-----------+----------+
| TABLE_SCHEMA | TABLE_NAME | TABLE_ID | REPLICA_COUNT | LOCATION_LABELS | AVAILABLE | PROGRESS |
+--------------+------------+----------+---------------+-----------------+-----------+----------+
| bookshop     | orders     |      147 |             1 |                 |         1 |        1 |
+--------------+------------+----------+---------------+-----------------+-----------+----------+
1 row in set (0.07 sec)
```

添加副本后，你可以使用 `EXPLAIN` 语句检查上述窗口函数 [`PARTITION BY` 子句](#partition-by-子句)的执行计划。如果执行计划中出现 `cop[tiflash]`，表示 TiFlash 引擎已开始工作。

然后，再次执行 [`PARTITION BY` 子句](#partition-by-子句)中的示例 SQL 语句。结果如下：

```
+------------------------------+---------+------+
| book_type                    | month   | acc  |
+------------------------------+---------+------+
| Magazine                     | 2011-10 |    1 |
| Magazine                     | 2011-8  |    2 |
| Magazine                     | 2012-5  |    3 |
| Magazine                     | 2013-1  |    4 |
| Magazine                     | 2013-6  |    5 |
...
| Novel                        | 2011-3  |   13 |
| Novel                        | 2011-4  |   14 |
| Novel                        | 2011-6  |   15 |
| Novel                        | 2011-8  |   17 |
| Novel                        | 2012-1  |   18 |
| Novel                        | 2012-2  |   20 |
...
| Sports                       | 2021-4  |   49 |
| Sports                       | 2021-7  |   50 |
| Sports                       | 2022-4  |   51 |
+------------------------------+---------+------+
1500 rows in set (0.79 sec)
```

通过比较两次执行结果，你可以发现使用 TiFlash 后查询速度显著提高（在数据量大的情况下提升更明显）。这是因为窗口函数通常依赖于对某些列的全表扫描，而列式的 TiFlash 比行式的 TiKV 更适合处理这类分析任务。对于 TiKV，如果你使用主键或索引来减少需要查询的行数，查询也可以很快，并且与 TiFlash 相比消耗更少的资源。

### 指定查询引擎

TiDB 使用基于成本的优化器（CBO）根据成本估算自动选择是否使用 TiFlash 副本。但是，如果你确定你的查询是事务性的还是分析性的，你可以使用[优化器提示](/optimizer-hints.md)指定要使用的查询引擎。

要在查询中指定使用哪个引擎，你可以使用 `/*+ read_from_storage(engine_name[table_name]) */` 提示，如以下语句所示。

> **注意：**
>
> - 如果表有别名，在提示中使用别名而不是表名，否则提示不会生效。
> - `read_from_storage` 提示对[公共表表达式](/develop/dev-guide-use-common-table-expression.md)不起作用。

```sql
WITH orders_group_by_month AS (
    SELECT
        /*+ read_from_storage(tikv[o]) */
        b.type AS book_type,
        DATE_FORMAT(ordered_at, '%Y-%c') AS month,
        COUNT(*) AS orders
    FROM orders o
    LEFT JOIN books b ON o.book_id = b.id
    WHERE b.type IS NOT NULL
    GROUP BY book_type, month
), acc AS (
    SELECT
        book_type,
        month,
        SUM(orders) OVER(PARTITION BY book_type ORDER BY book_type, month ASC) as acc
    FROM orders_group_by_month mo
    ORDER BY book_type, month ASC
)
SELECT * FROM acc;
```

你可以使用 `EXPLAIN` 语句检查上述 SQL 语句的执行计划。如果任务列中同时出现 `cop[tiflash]` 和 `cop[tikv]`，表示 TiFlash 和 TiKV 都被调度来完成此查询。注意，TiFlash 和 TiKV 存储引擎通常使用不同的 TiDB 节点，因此两种查询类型不会相互影响。

有关 TiDB 如何选择使用 TiFlash 的更多信息，请参阅[使用 TiDB 读取 TiFlash 副本](/tiflash/use-tidb-to-read-tiflash.md)。

## 阅读更多

<CustomContent platform="tidb">

- [HTAP 快速上手](/quick-start-with-htap.md)
- [探索 HTAP](/explore-htap.md)

</CustomContent>

<CustomContent platform="tidb-cloud">

- [TiDB Cloud HTAP 快速上手](/tidb-cloud/tidb-cloud-htap-quickstart.md)

</CustomContent>

- [窗口函数](/functions-and-operators/window-functions.md)
- [使用 TiFlash](/tiflash/tiflash-overview.md#use-tiflash)

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上询问社区，或[提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上询问社区，或[提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>
