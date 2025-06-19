---
title: GROUP BY 修饰符
summary: 了解如何使用 TiDB GROUP BY 修饰符。
---

# GROUP BY 修饰符

从 v7.4.0 版本开始，TiDB 的 `GROUP BY` 子句支持 `WITH ROLLUP` 修饰符。

在 `GROUP BY` 子句中，你可以指定一个或多个列作为分组列表，并在列表后添加 `WITH ROLLUP` 修饰符。然后，TiDB 将基于分组列表中的列进行多维度降序分组，并在输出中为每个分组提供汇总结果。

- 分组方法：

    - 第一个分组维度包含分组列表中的所有列。
    - 后续分组维度从分组列表的右端开始，每次多排除一列来形成新的分组。

- 聚合汇总：对于每个维度，查询执行聚合操作，然后将该维度的结果与所有前序维度的结果进行聚合。这意味着你可以获得不同维度的聚合数据，从详细到整体。

通过这种分组方法，如果分组列表中有 `N` 个列，TiDB 会在 `N+1` 个分组上聚合查询结果。

例如：

```sql
SELECT count(1) FROM t GROUP BY a,b,c WITH ROLLUP;
```

在这个例子中，TiDB 将在 4 个分组（即 `{a, b, c}`、`{a, b}`、`{a}` 和 `{}`）上聚合 `count(1)` 的计算结果，并输出每个分组的汇总结果。

> **注意：**
>
> 目前，TiDB 不支持 Cube 语法。

## 使用场景

从多个列聚合和汇总数据在 OLAP（在线分析处理）场景中很常见。通过使用 `WITH ROLLUP` 修饰符，你可以在聚合结果中获得额外的行，这些行显示来自其他高级维度的超级汇总信息。然后，你可以使用这些超级汇总信息进行高级数据分析和报表生成。

## 前提条件

目前，TiDB 仅在 TiFlash MPP 模式下支持为 `WITH ROLLUP` 语法生成有效的执行计划。因此，请确保你的 TiDB 集群已部署 TiFlash 节点，并且目标事实表已正确配置 TiFlash 副本。

<CustomContent platform="tidb">

更多信息，请参见[扩容 TiFlash 节点](/scale-tidb-using-tiup.md#扩容-tiflash-节点)。

</CustomContent>

## 示例

假设你有一个名为 `bank` 的利润表，包含 `year`、`month`、`day` 和 `profit` 列。

```sql
CREATE TABLE bank
(
    year    INT,
    month   VARCHAR(32),
    day     INT,
    profit  DECIMAL(13, 7)
);

ALTER TABLE bank SET TIFLASH REPLICA 1; -- 为表添加 TiFlash 副本

INSERT INTO bank VALUES(2000, "Jan", 1, 10.3),(2001, "Feb", 2, 22.4),(2000,"Mar", 3, 31.6)
```

要获取银行每年的利润，你可以使用简单的 `GROUP BY` 子句，如下所示：

```sql
SELECT year, SUM(profit) AS profit FROM bank GROUP BY year;
+------+--------------------+
| year | profit             |
+------+--------------------+
| 2001 | 22.399999618530273 |
| 2000 |  41.90000057220459 |
+------+--------------------+
2 rows in set (0.15 sec)
```

除了年度利润外，银行报表通常还需要包括所有年份的总体利润或按月划分的利润，以便进行详细的利润分析。在 v7.4.0 之前，你必须在多个查询中使用不同的 `GROUP BY` 子句，并使用 UNION 连接结果以获得聚合汇总。从 v7.4.0 开始，你只需在 `GROUP BY` 子句后添加 `WITH ROLLUP` 修饰符，就可以在单个查询中实现所需的结果。

```sql
SELECT year, month, SUM(profit) AS profit from bank GROUP BY year, month WITH ROLLUP ORDER BY year desc, month desc;
+------+-------+--------------------+
| year | month | profit             |
+------+-------+--------------------+
| 2001 | Feb   | 22.399999618530273 |
| 2001 | NULL  | 22.399999618530273 |
| 2000 | Mar   | 31.600000381469727 |
| 2000 | Jan   | 10.300000190734863 |
| 2000 | NULL  |  41.90000057220459 |
| NULL | NULL  |  64.30000019073486 |
+------+-------+--------------------+
6 rows in set (0.025 sec)
```

上述结果包括不同维度的聚合数据：按年和月、按年以及总体。在结果中，没有 `NULL` 值的行表示该行的 `profit` 是通过同时按年和月分组计算得出的。`month` 列中有 `NULL` 值的行表示该行的 `profit` 是通过聚合一年中所有月份计算得出的，而 `year` 列中有 `NULL` 值的行表示该行的 `profit` 是通过聚合所有年份计算得出的。

具体来说：

- 第一行的 `profit` 值来自二维分组 `{year, month}`，表示细粒度 `{2000, "Jan"}` 分组的聚合结果。
- 第二行的 `profit` 值来自一维分组 `{year}`，表示中级 `{2001}` 分组的聚合结果。
- 最后一行的 `profit` 值来自零维分组 `{}`，表示总体聚合结果。

`WITH ROLLUP` 结果中的 `NULL` 值是在应用聚合运算符之前生成的。因此，你可以在 `SELECT`、`HAVING` 和 `ORDER BY` 子句中使用 `NULL` 值来进一步过滤聚合结果。

例如，你可以在 `HAVING` 子句中使用 `NULL` 来仅查看二维分组的聚合结果：

```sql
SELECT year, month, SUM(profit) AS profit FROM bank GROUP BY year, month WITH ROLLUP HAVING year IS NOT null AND month IS NOT null;
+------+-------+--------------------+
| year | month | profit             |
+------+-------+--------------------+
| 2000 | Mar   | 31.600000381469727 |
| 2000 | Jan   | 10.300000190734863 |
| 2001 | Feb   | 22.399999618530273 |
+------+-------+--------------------+
3 rows in set (0.02 sec)
```

请注意，如果 `GROUP BY` 列表中的列包含原生 `NULL` 值，`WITH ROLLUP` 的聚合结果可能会误导查询结果。为解决此问题，你可以使用 `GROUPING()` 函数来区分原生 `NULL` 值和由 `WITH ROLLUP` 生成的 `NULL` 值。此函数接受一个分组表达式作为参数，并返回 `0` 或 `1` 来指示当前结果中是否聚合了分组表达式。`1` 表示已聚合，`0` 表示未聚合。

以下示例展示如何使用 `GROUPING()` 函数：

```sql
SELECT year, month, SUM(profit) AS profit, grouping(year) as grp_year, grouping(month) as grp_month FROM bank GROUP BY year, month WITH ROLLUP ORDER BY year DESC, month DESC;
+------+-------+--------------------+----------+-----------+
| year | month | profit             | grp_year | grp_month |
+------+-------+--------------------+----------+-----------+
| 2001 | Feb   | 22.399999618530273 |        0 |         0 |
| 2001 | NULL  | 22.399999618530273 |        0 |         1 |
| 2000 | Mar   | 31.600000381469727 |        0 |         0 |
| 2000 | Jan   | 10.300000190734863 |        0 |         0 |
| 2000 | NULL  |  41.90000057220459 |        0 |         1 |
| NULL | NULL  |  64.30000019073486 |        1 |         1 |
+------+-------+--------------------+----------+-----------+
6 rows in set (0.028 sec)
```

从这个输出中，你可以直接从 `grp_year` 和 `grp_month` 的结果了解一行的聚合维度，这可以防止 `year` 和 `month` 分组表达式中的原生 `NULL` 值的干扰。

`GROUPING()` 函数最多可以接受 64 个分组表达式作为参数。在多个参数的输出中，每个参数生成一个 `0` 或 `1` 的结果，这些参数共同形成一个 64 位的 `UNSIGNED LONGLONG`，每个位为 `0` 或 `1`。你可以使用以下公式获取每个参数的位置：

```go
GROUPING(day, month, year):
  result for GROUPING(year)
+ result for GROUPING(month) << 1
+ result for GROUPING(day) << 2
```

通过在 `GROUPING()` 函数中使用多个参数，你可以高效地过滤任何高维度的聚合结果。例如，你可以使用 `GROUPING(year, month)` 快速过滤每年和所有年份的聚合结果。

```sql
SELECT year, month, SUM(profit) AS profit, grouping(year) as grp_year, grouping(month) as grp_month FROM bank GROUP BY year, month WITH ROLLUP HAVING GROUPING(year, month) <> 0 ORDER BY year DESC, month DESC;
+------+-------+--------------------+----------+-----------+
| year | month | profit             | grp_year | grp_month |
+------+-------+--------------------+----------+-----------+
| 2001 | NULL  | 22.399999618530273 |        0 |         1 |
| 2000 | NULL  |  41.90000057220459 |        0 |         1 |
| NULL | NULL  |  64.30000019073486 |        1 |         1 |
+------+-------+--------------------+----------+-----------+
3 rows in set (0.023 sec)
```

## 如何解读 ROLLUP 执行计划

为了满足多维度分组的要求，多维数据聚合使用 `Expand` 算子来复制数据。每个副本对应特定维度的一个分组。通过 MPP 的数据分发能力，`Expand` 算子可以在多个 TiFlash 节点之间快速重组和计算大量数据，充分利用每个节点的计算能力。

`Expand` 算子的实现类似于 `Projection` 算子。不同之处在于 `Expand` 是一个多级 `Projection`，包含多个级别的投影操作表达式。对于原始数据的每一行，`Projection` 算子在结果中只生成一行，而 `Expand` 算子在结果中生成多行（行数等于投影操作表达式的级别数）。

以下是一个执行计划示例：

```sql
explain SELECT year, month, grouping(year), grouping(month), SUM(profit) AS profit FROM bank GROUP BY year, month WITH ROLLUP;
+----------------------------------------+---------+--------------+---------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| id                                     | estRows | task         | access object | operator info                                                                                                                                                                                                                        |
+----------------------------------------+---------+--------------+---------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| TableReader_44                         | 2.40    | root         |               | MppVersion: 2, data:ExchangeSender_43                                                                                                                                                                                                |
| └─ExchangeSender_43                    | 2.40    | mpp[tiflash] |               | ExchangeType: PassThrough                                                                                                                                                                                                            |
|   └─Projection_8                       | 2.40    | mpp[tiflash] |               | Column#6->Column#12, Column#7->Column#13, grouping(gid)->Column#14, grouping(gid)->Column#15, Column#9->Column#16                                                                                                                    |
|     └─Projection_38                    | 2.40    | mpp[tiflash] |               | Column#9, Column#6, Column#7, gid                                                                                                                                                                                                    |
|       └─HashAgg_36                     | 2.40    | mpp[tiflash] |               | group by:Column#6, Column#7, gid, funcs:sum(test.bank.profit)->Column#9, funcs:firstrow(Column#6)->Column#6, funcs:firstrow(Column#7)->Column#7, funcs:firstrow(gid)->gid, stream_count: 8                                           |
|         └─ExchangeReceiver_22          | 3.00    | mpp[tiflash] |               | stream_count: 8                                                                                                                                                                                                                      |
|           └─ExchangeSender_21          | 3.00    | mpp[tiflash] |               | ExchangeType: HashPartition, Compression: FAST, Hash Cols: [name: Column#6, collate: binary], [name: Column#7, collate: utf8mb4_bin], [name: gid, collate: binary], stream_count: 8                                                  |
|             └─Expand_20                | 3.00    | mpp[tiflash] |               | level-projection:[test.bank.profit, <nil>->Column#6, <nil>->Column#7, 0->gid],[test.bank.profit, Column#6, <nil>->Column#7, 1->gid],[test.bank.profit, Column#6, Column#7, 3->gid]; schema: [test.bank.profit,Column#6,Column#7,gid] |
|               └─Projection_16          | 3.00    | mpp[tiflash] |               | test.bank.profit, test.bank.year->Column#6, test.bank.month->Column#7                                                                                                                                                                |
|                 └─TableFullScan_17     | 3.00    | mpp[tiflash] | table:bank    | keep order:false, stats:pseudo                                                                                                                                                                                                       |
+----------------------------------------+---------+--------------+---------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
10 rows in set (0.05 sec)
```

在这个执行计划示例中，你可以在 `Expand_20` 行的 `operator info` 列中查看 `Expand` 算子的多级表达式。它由二维表达式组成，你可以在该行末尾查看 `Expand` 算子的 schema 信息，即 `schema: [test.bank.profit, Column#6, Column#7, gid]`。

在 `Expand` 算子的 schema 信息中，`GID` 作为额外列生成。其值由 `Expand` 算子根据不同维度的分组逻辑计算得出，该值反映了当前数据副本与 `grouping set` 的关系。在大多数情况下，`Expand` 算子使用位与运算，可以表示 ROLLUP 的 63 种分组项组合，对应 64 个分组维度。在这种模式下，TiDB 根据当前数据副本复制时所需维度的 `grouping set` 是否包含分组表达式来生成 `GID` 值，并按待分组列的顺序填充一个 64 位的 UINT64 值。

在上述示例中，分组列表中列的顺序是 `[year, month]`，ROLLUP 语法生成的维度分组是 `{year, month}`、`{year}` 和 `{}`。对于维度分组 `{year, month}`，`year` 和 `month` 都是必需列，所以 TiDB 分别用 1 和 1 填充它们的位置。这形成了一个 UINT64 的 `11...0`，十进制为 3。因此，投影表达式为 `[test.bank.profit, Column#6, Column#7, 3->gid]`（其中 `column#6` 对应 `year`，`column#7` 对应 `month`）。

以下是原始数据的一个示例行：

```sql
+------+-------+------+------------+
| year | month | day  | profit     |
+------+-------+------+------------+
| 2000 | Jan   |    1 | 10.3000000 |
+------+-------+------+------------+
```

应用 `Expand` 算子后，你可以得到以下三行结果：

```sql
+------------+------+-------+-----+
| profit     | year | month | gid |
+------------+------+-------+-----+
| 10.3000000 | 2000 | Jan   |  3  |
+------------+------+-------+-----+
| 10.3000000 | 2000 | NULL  |  1  |
+------------+------+-------+-----+
| 10.3000000 | NULL | NULL  |  0  |
+------------+------+-------+-----+
```

注意，查询中的 `SELECT` 子句使用了 `GROUPING` 函数。当在 `SELECT`、`HAVING` 或 `ORDER BY` 子句中使用 `GROUPING` 函数时，TiDB 在逻辑优化阶段会重写它，将 `GROUPING` 函数与 `GROUP BY` 项之间的关系转换为与维度分组（也称为 `grouping set`）逻辑相关的 `GID`，并将此 `GID` 作为元数据填充到新的 `GROUPING` 函数中。
