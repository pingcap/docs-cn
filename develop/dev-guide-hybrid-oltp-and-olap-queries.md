---
title: HTAP 查询
summary: 介绍 TiDB 中的 HTAP 查询功能。
aliases: ['/zh/tidb/stable/dev-guide-hybrid-oltp-and-olap-queries/','/zh/tidb/dev/dev-guide-hybrid-oltp-and-olap-queries/','/zh/tidbcloud/dev-guide-hybrid-oltp-and-olap-queries/']
---

# HTAP 查询

HTAP 是 Hybrid Transactional / Analytical Processing 的缩写。传统意义上，数据库往往专为交易或者分析场景设计，因而数据平台往往需要被切分为 Transactional Processing 和 Analytical Processing 两个部分，而数据需要从交易库复制到分析型数据库以便快速响应分析查询。而 TiDB 数据库则可以同时承担交易和分析两种职能，这大大简化了数据平台的建设，也能让用户使用更新鲜的数据进行分析。

在 TiDB 当中，同时拥有面向在线事务处理的行存储引擎 TiKV 与面向实时分析场景的列存储引擎 TiFlash 两套存储引擎。数据在行存 (Row-Store) 与列存 (Columnar-Store) 同时存在，自动同步，保持强一致性。行存为在线事务处理 OLTP 提供优化，列存则为在线分析处理 OLAP 提供性能优化。

在[创建数据库](/develop/dev-guide-create-table.md#使用-htap-能力)章节当中，已经介绍了如何开启 TiDB 的 HTAP 能力。下面将进一步介绍如何使用 HTAP 能力更快地分析数据。

## 数据准备

在开始之前，你可以[通过 `tiup demo` 命令导入](/develop/dev-guide-bookshop-schema-design.md#方法一通过-tiup-demo-命令行)更加大量的示例数据，例如：

```shell
tiup demo bookshop prepare --users=200000 --books=500000 --authors=100000 --ratings=1000000 --orders=1000000 --host 127.0.0.1 --port 4000 --drop-tables
```

或[使用 TiDB Cloud 的 Import 功能导入](/develop/dev-guide-bookshop-schema-design.md#方法二通过-tidb-cloud-import-功能)预先准备好的示例数据。

## 窗口函数

在使用数据库时，除了希望它能够存储想要记录的数据，能够实现诸如下单买书、给书籍评分等业务功能外，可能还需要对已有的数据进行分析，以便根据数据作出进一步的运营和决策。

在[单表读取](/develop/dev-guide-get-data-from-single-table.md)章节当中，已经介绍了如何使用聚合查询来分析数据的整体情况，在更为复杂的使用场景下，你可能希望多个聚合查询的结果汇总在一个查询当中。例如：你想要对某一本书的订单量的历史趋势有所了解，就需要在每个月都对所有订单数据进行一次聚合求 `sum`，然后将 `sum` 结果汇总在一起才能够得到历史的趋势变化数据。

为了方便用户进行此类分析，TiDB 从 3.0 版本开始便支持了窗口函数功能，窗口函数为每一行数据提供了跨行数据访问的能力，不同于常规的聚合查询，窗口函数在对数据行进行聚合时不会导致结果集被合并成单行数据。

与聚合函数类似，窗口函数在使用时也需要搭配一套固定的语法：

```sql
SELECT
    window_function() OVER ([partition_clause] [order_clause] [frame_clause]) AS alias
FROM
    table_name
```

### `ORDER BY` 子句

例如：可以利用聚合窗口函数 `sum()` 函数的累加效果来实现对某一本书的订单量的历史趋势的分析:

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

`sum()` 函数会在 `OVER` 子句当中通过 `ORDER BY` 子句指定的排序方式按顺序对数据进行累加，累加的结果如下：

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

将得到的数据通过一个横轴为时间，纵轴为累计订单量的折线图进行可视化，便可以轻松地通过折线图的斜率变化宏观地了解到这本书的历史订单的增长趋势。

### `PARTITION BY` 子句

把需求变得更复杂一点，假设想要分析不同类型书的历史订单增长趋势，并且希望将这些数据通过同一个多系列折线图进行呈现。

可以利用 `PARTITION BY` 子句根据书的类型进行分组，对不同类型的书籍分别统计它们的订单历史订单累计量。

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

查询结果如下：

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

除此之外，TiDB 还提供了一些非聚合的[窗口函数](/functions-and-operators/window-functions.md)，可以借助这些函数实现更加丰富分析查询。

例如，在前面的[分页查询](/develop/dev-guide-paginate-results.md)章节当中，已经介绍了如何巧妙地利用 `row_number()` 函数实现高效的分页批处理能力。

## 混合负载

当将 TiDB 应用于在线实时分析处理的混合负载场景时，开发人员只需要提供一个入口，TiDB 将自动根据业务类型选择不同的处理引擎。

### 开启列存副本

TiDB 默认使用的存储引擎 TiKV 是行存的，你可以通过阅读[开启 HTAP 能力](/develop/dev-guide-create-table.md#使用-htap-能力)章节，在进行后续步骤前，先通过如下 SQL 对 `books` 与 `orders` 表添加 TiFlash 列存副本：

```sql
ALTER TABLE books SET TIFLASH REPLICA 1;
ALTER TABLE orders SET TIFLASH REPLICA 1;
```

通过执行下面的 SQL 语句可以查看到 TiDB 创建列存副本的进度：

```sql
SELECT * FROM information_schema.tiflash_replica WHERE TABLE_SCHEMA = 'bookshop' and TABLE_NAME = 'books';
SELECT * FROM information_schema.tiflash_replica WHERE TABLE_SCHEMA = 'bookshop' and TABLE_NAME = 'orders';
```

当 `PROGRESS` 列为 1 时表示同步进度完成度达到 100%，`AVAILABLE` 列为 1 表示副本当前可用。

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

副本添加完成之后，你可以通过使用 `EXPLAIN` 语句查看上面窗口函数[示例 SQL](#partition-by-子句) 的执行计划。你会发现执行计划当中已经出现了 `cop[tiflash]` 字样，说明 TiFlash 引擎已经开始发挥作用了。

再次执行[示例 SQL](#partition-by-子句)，查询结果如下：

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

通过对比前后两次的执行结果，你会发现使用 TiFlash 处理有查询速度有了较为明显的提升（当数据量更大时，提升会更为显著）。这是因为在使用窗口函数时往往需要对某些列的数据进行全表扫描，相比行存的 TiKV，列存的 TiFlash 更加适合来处理这类分析型任务的负载。而对于 TiKV 来说，如果能够通过主键或索引快速地将所要查询的行数减少，往往查询速度也会非常快，而且所消耗的资源一般相对 TiFlash 而言会更少。

### 指定查询引擎

尽管 TiDB 会使用基于成本的优化器（CBO）自动地根据代价估算选择是否使用 TiFlash 副本。但是在实际使用当中，如果你非常确定查询的类型，推荐你使用 [Optimizer Hints](/optimizer-hints.md) 明确的指定查询所使用的执行引擎，避免因为优化器的优化结果不同，导致应用程序性能出现波动。

你可以像下面的 SQL 一样在 SELECT 语句中通过 Hint `/*+ read_from_storage(engine_name[table_name]) */` 指定查询时需要使用的查询引擎。

> **注意：**
>
> 1. 如果你的表使用了别名，你应该将 Hints 当中的 table_name 替代为 alias_name，否则 Hints 会失效。
> 2. 另外，对[公共表表达式](/develop/dev-guide-use-common-table-expression.md)设置 read_from_storage Hint 是不起作用的。

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

如果你通过 `EXPLAIN` 语句查看上面 SQL 的执行计划，你会发现 task 列中会同时出现 `cop[tiflash]` 和 `cop[tikv]`，这意味着 TiDB 在处理这个查询的时候会同时调度行存查询引擎和列存查询引擎来完成查询任务。需要指出的是，因为 tiflash 和 tikv 存储引擎通常属于不同的计算节点，所以两种查询类型互相之间不受影响。

你可以通过阅读[使用 TiDB 读取 TiFlash](/tiflash/use-tidb-to-read-tiflash.md) 小节进一步了解 TiDB 如何选择使用 TiFlash 作为查询引擎。

## 扩展阅读

- TiDB Cloud 文档：[HTAP 快速上手指南](/tidb-cloud/tidb-cloud-htap-quickstart.md)
- TiDB 文档：[HTAP 快速上手指南](/quick-start-with-htap.md) 和 [HTAP 深入探索指南](/explore-htap.md)
- [窗口函数](/functions-and-operators/window-functions.md)
- [使用 TiFlash](/tiflash/tiflash-overview.md#使用-tiflash)
