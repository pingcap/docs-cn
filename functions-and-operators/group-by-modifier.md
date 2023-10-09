---
title: GROUP BY 修饰符
summary: 了解如何使用 TiDB GROUP BY 修饰符。
---

# GROUP BY 修饰符

自 v7.4.0 起，TiDB 的 `GROUP BY` 子句支持 `WITH ROLLUP` 修饰符。

你可以在 `GROUP BY` 子句中指定一个或多个列，形成一个分组列表，然后添加 `WITH ROLLUP` 修饰符。TiDB 将会按照分组列表中的列进行多维度的递减分组，并在输出中为你提供各个分组数据的汇总结果。

- 分组方式：
    - 第一个分组维度为分组表列表中的所有列。
    - 后面的维度将从分组列表的最右侧（尾端）开始，每次递减一个元素，形成新的分组。
- 聚合汇总：在每个维度上，查询都会执行聚合操作，然后将该维度的计算结果与前面所有维度的结果进行汇总。这意味着你可以看到不同维度的聚合数据，从详细到总体。

按照这种分组方式，当分组列表中有 N 个列时，查询的计算结果将会在 N+1 个分组上进行聚合后输出。

例如：

```sql
SELECT count(1) FROM t GROUP BY a,b,c WITH ROLLUP;
```

在此示例中，count(1) 的计算结果将分别在 {a,b,c}、{a,b}、{a}、{} 一共 4 个分组上进行聚合，然后输出各分组的汇总数据。

> **注意：**
>
> TiDB 暂不支持 Cube 语法。

## 使用场景

多列数据的聚合汇总输出一般常用于 OLAP（Online Analytical Processing）场景。通过使用 `WITH ROLLUP` 修饰符，你可以在聚合结果中得到额外的行，以展示不同维度的汇总信息，从而实现高级的数据分析和报表生成。

## 准备条件

目前，TiDB 仅在 TiFlash MPP 模式下支持为 `WITH ROLLUP` 语法生成有效的执行计划，因此你的 TiDB 集群需要包含 TiFlash 节点，并且对目标分析表进行了正确的 TiFlash 副本的配置。

更多信息，请参考[扩容 TiFlash 节点](/scale-tidb-using-tiup.md#扩容-tiflash-节点)。

## 使用示例

假如有一张名为 `bank` 的银行利润表，包含年（`year`）、月（`month`）、日（`day`）和利润（`profit`）列。

```sql
CREATE TABLE bank
(
    year    INT,
    month   VARCHAR(32),
    day     INT,
    profit  DECIMAL(13, 7)
);

ALTER TABLE bank SET TIFLASH REPLICA 1; -- 为该表添加一个 TiFlash 副本

INSERT INTO bank VALUES(2000, "Jan", 1, 10.3),(2001, "Feb", 2, 22.4),(2000,"Mar", 3, 31.6)
```

如需查看银行每年的利润，可以用一个简单的 `GROUP BY` 的子句来实现：

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

对于银行报表来说，除了每年的利润之外，通常还需要计算所有年份的总利润或每个月的总利润，以进行更高层次或更详细的利润分析。在 v7.4.0 之前的版本中，你需要在多个查询中使用不同的 `GROUP BY` 子句，并将结果使用 UNION 连接，才能得到聚合汇总的结果。从 v7.4.0 起，你可以直接在单个查询的 `GROUP BY` 子句中添加 `WITH ROLLUP` 修饰符，即可得到所需的结果：

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

以上结果包含了按照年份和月份、按照年份、以及整体所有维度的聚合数据。其中，未出现 `NULL` 值的行表示该行 `profit` 是同时按照年份和月份分组计算的结果，`month` 列的 `NULL` 值表示该行 `profit` 是按照该年份的所有月份聚合计算的结果，`year` 列的 `NULL` 值表示该行 `profit` 是按照所有年份聚合计算的结果。

具体来说：

* 第一行的 `profit` 值来自 2 维分组 {year, month}，为 {2000, “Jan”} 的细粒度分组的聚合结果。
* 第二行的 `profit` 值来自 1 维分组 {year}，为 {2001} 的中层粒度分组下的聚合结果。
* 最后一行的 `profit` 值来自 0 维分组 {}，即整体的聚合结果。

`WITH ROLLUP` 结果中的  `NULL` 值是在应用 Aggregate 算子之前生成的，因此你可以将 `NULL` 值应用于 `SELECT`、`HAVING`、`ORDER BY` 子句中，进一步过滤聚合结果。

例如，你可以在 `HAVING` 子句中通过 `NULL` 过滤并只看 2 维度分组下的聚合结果输出。

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

需要注意的是，如果 `GROUP BY` 分组列表中的某列包含原生的 `NULL` 值，`WITH ROLLUP` 的分组聚合可能会对查询结果产生误导。为了解决这个问题，你可以使用 `GROUPING ()` 函数区分原生的 `NULL` 值和 `WITH ROLLUP` 生成的 `NULL` 值。该函数接受分组表达式作为参数，并输出 `0` 或 `1`，表示该分组表达式是否在当前结果中被聚合。`1` 表示被聚合，`0` 表示没有。

以下是如何使用 `GROUPING ()` 函数的示例：

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

在此输出中，你可以直接通过 `grp_year` 和 `grp_month` 的结果来判断该聚合结果行所在的聚合维度，以防止分组表达式 `year` 和 `month` 原生的 `NULL` 值的干扰。

`GROUPING()` 函数最多可以接受 64 个分组表达式作为参数。在多参数的输出中，每个参数都可以生成一个 `0` 或 `1` 的结果，多个参数综合组成每一个比特位是 `0` 或 `1` 总体是 64 位的 `UNSIGNED LONGLONG`。各个参数在比特数位中的位置可以通过以下公式计算：

```go
GROUPING(day, month, year):
  result for GROUPING(year)
+ result for GROUPING(month) << 1
+ result for GROUPING(day) << 2
```

在 `GROUPING()` 的函数中使用组合参数可以快速过滤出任何高维度的聚合结果。例如，你可以通过 `GROUPING(year, month)` 快速过滤出每年以及所有年份的聚合结果：

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

## 如何阅读 ROLLUP 的执行计划

多维度数据聚合使用了 `Expand` 算子来复制数据以满足多维度分组的需求，每个复制的数据副本都对应一个特定维度的分组。通过 MPP 的数据 shuffle 能力，`Expand` 算子能够快速地在多个 TiFlash 节点之间重新组织和计算大量的数据，充分利用每个节点的计算能力。

`Expand` 算子的实现类似 `Projection` 算子，但区别在于 `Expand` 是多层级的 `Projection`，具有多层级投影运算表达式。对于每行原始数据行，`Projection` 算子只会生成一行结果输出，而 `Expand` 算子会生成多行结果（行数等于多层级投影运算表达式的层数）。

以下为一个执行计划示例：

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

在这个示例执行计划中，你可以在 `Expand_20` 这行的 `operator info` 列查看 `Expand` 算子的层级表达式，其由 2 维表达式组成，行末有 `Expand` 算子的 Schema 信息 `schema: [test.bank.profit,Column#6,Column#7,gid]`。

在 `Expand` 算子的 schema 信息中，`GID` 会作为额外的生成列来输出，其值是由 `Expand` 算子根据不同维度的分组逻辑计算得出，反映了当前数据副本和维度分组的关系。最常见的情况是使用位掩码运算, 它可以表示 63 种分组项的 ROLLUP 组合，对应 64 种维度的分组。在这种模式下，`GID` 值的生成根据当前数据副本复制时所需维度分组中是否有分组表达式，按照要进行分组的列，顺序填充一个 64 位的 UINT64 的值。

例如，这里分组列表中列的顺序是 [year, month]，而 ROLLUP 语法生成的维度分组集合为：{year, month}, {year}, {}。对于维度分组 {year, month} 来说，`year` 和 `month` 都是当前维度分组所需的列，对应填充比特位 1 和 1，组成 UINT64 为 11...0 即 3，因此投影表达式为 `[test.bank.profit, Column#6, Column#7, 3->gid]`。（`column#6` 对应 `year`，`column#7` 对应 `month`）

以原始数据中的下面这行为例：

```sql
+------+-------+------+------------+
| year | month | day  | profit     |
+------+-------+------+------------+
| 2000 | Jan   |    1 | 10.3000000 |
+------+-------+------+------------+
```

经过 `Expand` 算子之后，可以得到以下三行结果：

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

需要注意的是，该查询的 `SELECT` 子句中使用了 `GROUPING` 函数。当在 `SELECT`、`HAVING`、`ORDER BY` 子句中使用 `GROUPING` 函数时，TiDB 会在逻辑优化阶段对其进行改写，将 `GROUPING` 函数与分组项（`GROUP BY` items）之间的关系，转化为与维度分组计算逻辑有关的 `GID`，并将此 `GID` 以 metadata 形式填充到新的 `GROUPING` 函数当中。