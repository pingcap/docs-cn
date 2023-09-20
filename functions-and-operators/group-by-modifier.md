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

对于银行报表来说，除了每年的利润之外，通常还需要计算所有年份的总利润和每个月的总利润，以进行更高层次或更详细的利润分析。在 v7.4.0 之前的版本中，你需要在多个查询中使用不同的 `GROUP BY` 子句，并将结果使用 UNION 连接，才能得到聚合汇总的结果。从 v7.4.0 起，你可以直接在单个查询的 `GROUP BY` 子句中添加 `WITH ROLLUP` 修饰符，即可得到所需的结果：

```sql
SELECT year, month, SUM(profit) AS profit from bank GROUP BY year, month WITH ROLLUP order by year desc, month desc;
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

以上结果包含了按照年份、月份、以及整体所有维度的聚合数据。其中，未出现 `NULL` 值的行表示该行 profit 是按照年份和月份分组计算的结果，`month` 列的 `NULL` 值表示该行 profit 是按照月份聚合计算的结果，`year` 列的 `NULL` 值表示该行 profit 是按照年份聚合计算的结果，

具体来说：

* 第一行的 profit 值来自 2 维分组 {year, month}，为 {2000, “Jan”} 的细粒度分组的聚合结果。
* 第二行的 profit 值来自 1 维分组 {year}，为 {2001} 的中层粒度分组下的聚合结果。
* 最后一行的 profit 值来自 0 维分组 {}，即整体的聚合结果。

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

可以看到我们不再依赖分组表达式 year 和 month 的输出去判断该聚合结果行所在的聚合维度，而是依赖于 grp_year 和 grp_month 的 GROUPING 函数结果来判断，以防止分组表达式 year 和 month 自有原生 `NULL` 值的干扰。

`GROUPING()` 函数最多可以接受 64 个分组表达式作为参数。在多参数的输出中，每个参数都可以生成一个 `0` 或 `1` 的结果，综合组成一个比特位的 `0` 或 `1` 总体是 64 位的 `UNSIGNED LONGLONG`。而其所在该比特数位中的位置可以通过以下公式计算：

```go
GROUPING(day, month, year):
  result for GROUPING(year)
+ result for GROUPING(month) << 1
+ result for GROUPING(day) << 2
```

使用组合参数的 `GROUPING()` 的函数可以快速过滤掉出任何高维度的聚合结果，就像这样只查看高维度聚合的结果：

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

多维度聚合目前依赖于 `Expand` 算子来实现底层的数据特殊复制，每个复制数据的副本都一一对应于一个特定的维度分组。`Expand` 算子依赖 MPP 的数据 shuffle 能力，能够快速的将大批量的数据在多 TiFlash 节点之间进行重组并计算，充分利用每个节点的计算能力。

目前 `Expand` 算子的实现类似 `Projection` 算子，其中区别就在于 `Expand` 是多层 `Projection` 的联合，这意味着对于每一原生数据行，`Projection` 算子根据投影运算表达式会对应生成一行结果输出，而由于 `Expand` 算子具有多层级投影运算表达式，所以对于每一原生数据行，其会依次投影输出 N 行（其中 N 等于多层级投影运算表达式的层数）。

示例参考计划: [explain](/explain-aggregation.md#多维度数据聚合-rollup)

`Expand_20` 算子信息展示了所谓生成的层级表达式：`level-projection:[test.bank.profit, <nil>->Column#6, <nil>->Column#7, 0->gid],[test.bank.profit, Column#6, <nil>->Column#7, 1->gid],[test.bank.profit, Column#6, Column#7, 3->gid]`。其由 2 维表达式组成，尾部后缀有 `Expand` 算子的 Schema 信息：`schema: [test.bank.profit,Column#6,Column#7,gid]`。

正上所示，在 `Expand` 算子的 Schema 信息中，`GID` 会作为额外的生成列来输出，其值也是由 `Expand` 算子根据不同的维度分组逻辑计算得来的，反应了当前数据副本和维度分组的关系。其中最常见的属是位掩码运算, 其可以容纳 63 种 GROUP BY ITEMS 的 ROLLUP 组合，对应维度分组的数量为 64 种。这种模式下 `GID` 值的生成根据当前数据副本复制时所需维度分组中 GROUPING EXPRESSION 的有无，按照 GROUP BY ITEMS 的序列，顺序填充一个 64 位的 UINT64 的值。

例如这里 GROUP BY ITEMS 序列顺序是 [year, month], 而 ROLLUP 的语法生成的维度分组集合为：{year, month}, {year}, {}。对于维度分组 {year, month} 来说，其 `year` 和 `month` 两个 GROUPING ITEM 都是当前维度分组所需的列，对应填充对应比特位为 1 和 1，组成 UINT64 为 11...0 即 3。相应的 `year` 和 `month` 两个 GROUPING ITEM 都是当前维度分组所需的列，所在当前投影表达式构建时要保留这两个列的完整输出，所以投影表达式为 `[test.bank.profit, Column#6, Column#7, 3->gid]`。（column#6 = year, column#7 = month）

```
以原始数据中的一行为例：
+------+-------+------+------------+
| year | month | day  | profit     |
+------+-------+------+------------+
| 2000 | Jan   |    1 | 10.3000000 |
+------+-------+------+------------+

经过 Expand 算子之后，可以得到以下三行结果：
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

注意到 select list 中使用了 `GROUPING` 函数。对于 select list / having / order by 中的使用到的 `GROUPING` 函数，TiDB 会在逻辑优化阶段对其进行改写，将函数原有的由 GROUP BY ITEM 所代表的与维度分组的关系，转化为由 `GID` 所代表的与维度分组计算逻辑，以 metadata 形式填充到新的 `GROUPING` 函数当中。