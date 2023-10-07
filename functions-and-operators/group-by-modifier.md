---
title: GROUP BY Modifiers
summary: Learn how to use TiDB GROUP BY modifiers.
---

# GROUP BY Modifiers

Starting from v7.4.0, the `GROUP BY` clause of TiDB supports the `WITH ROLLUP` modifier.

In the `GROUP BY` clause, you can specify one or more columns as a group list and append the `WITH ROLLUP` modifier after the list. Then, TiDB will conduct multidimensional descending grouping based on the columns in the group list and provide you with summary results for each group in the output.

- Grouping method:

    - The first grouping dimension includes all columns in the group list.
    - Subsequent grouping dimensions start from the right end of the grouping list and exclude one more column at a time to form new groups.

- Aggregation summaries: for each dimension, the query performs aggregation operations, and then aggregates the results of this dimension with the results of all previous dimensions. This means that you can get aggregated data at different dimensions, from detailed to overall.

With this grouping method, if there are `N` columns in the group list, TiDB aggregates the query results on `N+1` groups.

For example:：

```sql
SELECT count(1) FROM t GROUP BY a,b,c WITH ROLLUP;
```

In this example, TiDB will aggregate the calculation results of `count(1)` on 4 groups (that is, `{a, b, c}`, `{a, b}`, `{a}`, and `{}`) and output the summary results for each group.

> **Note:**
>
> Currently, TiDB does not support the Cube syntax.

## Use cases

Aggregating and summarizing data from multiple columns is commonly used in OLAP (Online Analytical Processing) scenarios. By using the `WITH ROLLUP` modifier, you can get additional rows that display super summary information from other high-level dimensions in your aggregated results. Then, you can use the super summary information for advanced data analysis and report generation.

## Prerequisites

Currently, TiDB supports generating valid execution plans for the `WITH ROLLUP` syntax only in TiFlash MPP mode. Therefore, make sure that your TiDB cluster has been deployed with TiFlash nodes and that target fact tables are configured with TiFlash replicas properly.

<CustomContent platform="tidb">

For more information, see [Scale out a TiFlash cluster](/scale-tidb-using-tiup.md#scale-out-a-tiflash-cluster).

</CustomContent>

## Examples

Suppose you have a profit table named `bank` with the `year`, `month`, `day`, and `profit` columns.

```sql
CREATE TABLE bank
(
    year    INT,
    month   VARCHAR(32),
    day     INT,
    profit  DECIMAL(13, 7)
);

ALTER TABLE bank SET TIFLASH REPLICA 1; -- Add a TiFlash replica for the table

INSERT INTO bank VALUES(2000, "Jan", 1, 10.3),(2001, "Feb", 2, 22.4),(2000,"Mar", 3, 31.6)
```

To get the profit for the bank per year, you can use a simple `GROUP BY` clause as follows:

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

In addition to yearly profits, bank reports usually also need to include the overall profit for all years or monthly divided profits for detailed profit analysis. Before v7.4.0, you have to use different `GROUP BY` clauses in multiple queries and join the results using UNION to obtain aggregated summaries. Starting from v7.4.0, you can simply achieve the desired results in a single query by appending the `WITH ROLLUP` modifier to the `GROUP BY` clause.

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

The preceding results include aggregated data at different dimensions: by both year and month, by year, and overall. In the results, a row without `NULL` values indicates that the `profit` in that row is calculated by grouping both year and month. A row with a `NULL` value in the `month` column indicates that `profit` in that row is calculated by aggregating all months in a year, while a row with a `NULL` value in the `year` column indicates that `profit` in that row is calculated by aggregating all years.

Specifically:

- The `profit` value in the first row comes from the 2-dimensional group `{year, month}`, representing the aggregation result for the fine-grained `{2000, "Jan"}` group.
- The `profit` value in the second row comes from the 1-dimensional group `{year}`, representing the aggregation result for the mid-level `{2001}` group.
- The `profit` value in the last row comes from the 0-dimensional grouping `{}`, representing the overall aggregation result.

`NULL` values in the `WITH ROLLUP` results are generated just before the Aggregate operator is applied. Therefore, you can use `NULL` values in `SELECT`, `HAVING`, and `ORDER BY` clauses to further filter the aggregated results.

For example, you can use `NULL` in the `HAVING` clause to filter and view the aggregated results of 2-dimensional groups only:

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

Note that if a column in the `GROUP BY` list contains native `NULL` values, the aggregation results of `WITH ROLLUP` might mislead the query results. To address this issue, you can use the `GROUPING()` function to distinguish native `NULL` values from `NULL` values generated by `WITH ROLLUP`. This function takes a grouping expression as a parameter and returns `0` or `1` to indicate whether the grouping expression is aggregated in the current result. `1` represents aggregated, and `0` represents not aggregated.

The following example shows how to use the `GROUPING()` function:

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

From this output, you can get an understanding of the aggregation dimension of a row directly from the results of `grp_year` and `grp_month`, which prevents interference from native `NULL` values in the `year` and `month` grouping expressions.

The `GROUPING()` function can accept up to 64 grouping expressions as parameters. In the output of multiple parameters, each parameter generates a result of `0` or `1`, and these parameters collectively form a 64-bit `UNSIGNED LONGLONG` with each bit as `0` or `1`. You can use the following formula to get the bit position of each parameter as follows:

```go
GROUPING(day, month, year):
  result for GROUPING(year)
+ result for GROUPING(month) << 1
+ result for GROUPING(day) << 2
```

By using multiple parameters in the `GROUPING()` function, you can efficiently filter aggregate results at any high dimension. For example, you can quickly filter the aggregate results for each year and all years by using `GROUPING(year, month)`.

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

## How to interpret the ROLLUP execution plan

To meet the requirements of multidimensional grouping, multidimensional data aggregation uses the `Expand` operator to replicate data. Each replica corresponds to a group at a specific dimension. With the data shuffling capability of MPP, the `Expand` operator can rapidly reorganize and calculate a large volume of data between multiple TiFlash nodes, fully utilizing the computational power of each node.

The implementation of the `Expand` operator is similar to that of the `Projection` operator. The difference is that `Expand` is a multi-level `Projection`, which contains multiple levels of projection operation expressions. For each row of the raw data, the `Projection` operator generates only one row in results, whereas the `Expand` operator generates multiple rows in results (the number of rows is equal to the number of levels in projection operation expressions).

The following is an example of an execution plan:

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

In this example execution plan, you can view the multiple-level expression of the `Expand` operator in the `operator info` column of the `Expand_20` row. It consists of 2-dimensional expressions, and you can view the schema information of the `Expand` operator at the end of the row, which is `schema: [test.bank.profit, Column#6, Column#7, gid]`.

In the schema information of the `Expand` operator, `GID` is generated as an additional column. Its value is calculated by the `Expand` operator based on the grouping logic of different dimensions, and the value reflects the relationship between the current data replica and the `grouping set`. In most cases, the `Expand` operator uses a Bit-And operation, which can represent 63 combinations of grouping items for ROLLUP, corresponding to 64 dimensions of grouping. In this mode, TiDB generates the `GID` value depending on whether the `grouping set` of the required dimension contains grouping expressions when the current data replica is replicated, and it fills a 64-bit UINT64 value in the order of columns to be grouped.

In the preceding example, the order of columns in the grouping list is `[year, month]`, and the dimension groups generated by the ROLLUP syntax are `{year, month}`, `{year}`, and `{}`. For the dimension group `{year, month}`, both `year` and `month` are required columns, so TiDB fills the bit positions for them with 1 and 1 correspondingly. This forms a UINT64 of `11...0`, which is 3 in decimal. Therefore, the projection expression is `[test.bank.profit, Column#6, Column#7, 3->gid]` (where `column#6` corresponds to `year`, and `column#7` corresponds to `month`).

The following is an example row of the raw data:

```sql
+------+-------+------+------------+
| year | month | day  | profit     |
+------+-------+------+------------+
| 2000 | Jan   |    1 | 10.3000000 |
+------+-------+------+------------+
```

After the `Expand` operator is applied, you can get the following three rows of results:

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

Note that the `SELECT` clause in the query uses the `GROUPING` function. When the `GROUPING` function is used in the `SELECT`, `HAVING`, or `ORDER BY` clauses, TiDB rewrites it during the logical optimization phase, transforms the relationship between the `GROUPING` function and the `GROUP BY` items into a `GID` related to the logic of dimension group (also known as `grouping set`), and fills this `GID` as metadata into the new `GROUPING` function.