---
title: 从窗口函数中推导 TopN 或 Limit
aliases: ['/docs-cn/dev/derive-topn-from-window/']
---

# 从窗口函数中推导 TopN 或 Limit

窗口函数是一种在 SQL 语句中常见的函数，而对于 row_number() 或者 rank() 等编号相关的窗口函数，一个常见的用法是在进行窗口函数求值之后，对 row_number() 或者 rank() 的结果做过滤，例如

```sql
select * from (select row_number() over (order by a) as rownumber from t) DT where rownumber <= 3
```

按照正常的 SQL 执行流程，TiDB 需要对 `t` 表的所有数据进行排序后给每一行都求得相应的 `row_number()` 结果之后再进行 `rownumber <= 3` 的过滤，而该优化可以将原始 SQL 等价改写成

```sql
WITH t_topN as (select a from t1 order by a limit 3) select * from (select row_number() over (order by a) as rownumber from t_topN) DT where rownumber <= 3
```

可以看出，该优化从窗口函数与后续的过滤条件中推导出了一个 TopN 算子，相比于原始 SQL 中的 Sort 算子，TopN 算子的运行效率远高于 Sort 算子，而且 TiKV/TiFlash 支持 TopN 算子的下推，这能进一步加速改写之后的 SQL 的性能。

有两种方法关闭此优化
* 设置 session 变量 [tidb_opt_derive_topn](/system-variables.md#tidb_opt_derive_topn-从-v610-版本开始引入) 为 false
* 可参照[优化规则及表达式下推的黑名单](/blocklist-control-plan.md)中的关闭方法。

## 示例

以下通过一些例子对改优化规则进行说明。

### 不带 partition by 的窗口函数
#### 示例 1：不带 order by 的窗口函数

{{< copyable "sql" >}}

```sql
create table t(id int, value int);
set tidb_opt_derive_topn=on;
explain select * from (select row_number() over () as rownumber from t) DT where rownumber <= 3;
```

```
+----------------------------------+---------+-----------+---------------+-----------------------------------------------------------------------+
| id                               | estRows | task      | access object | operator info                                                         |
+----------------------------------+---------+-----------+---------------+-----------------------------------------------------------------------+
| Projection_9                     | 2.40    | root      |               | Column#5                                                              |
| └─Selection_10                   | 2.40    | root      |               | le(Column#5, 3)                                                       |
|   └─Window_11                    | 3.00    | root      |               | row_number()->Column#5 over(rows between current row and current row) |
|     └─Limit_15                   | 3.00    | root      |               | offset:0, count:3                                                     |
|       └─TableReader_26           | 3.00    | root      |               | data:Limit_25                                                         |
|         └─Limit_25               | 3.00    | cop[tikv] |               | offset:0, count:3                                                     |
|           └─TableFullScan_24     | 3.00    | cop[tikv] | table:t       | keep order:false, stats:pseudo                                        |
+----------------------------------+---------+-----------+---------------+-----------------------------------------------------------------------+
```

在该查询中，优化器从窗口函数中推导出来了 Limit 并将它下推给了 TiKV。

#### 示例 2：带 order by 的窗口函数

{{< copyable "sql" >}}

```sql
create table t(id int, value int);
set tidb_opt_derive_topn=on;
explain select * from (select row_number() over (order by value) as rownumber from t) DT where rownumber <= 3;
```

```
+----------------------------------+----------+-----------+---------------+---------------------------------------------------------------------------------------------+
| id                               | estRows  | task      | access object | operator info                                                                               |
+----------------------------------+----------+-----------+---------------+---------------------------------------------------------------------------------------------+
| Projection_10                    | 2.40     | root      |               | Column#5                                                                                    |
| └─Selection_11                   | 2.40     | root      |               | le(Column#5, 3)                                                                             |
|   └─Window_12                    | 3.00     | root      |               | row_number()->Column#5 over(order by test.t.value rows between current row and current row) |
|     └─TopN_13                    | 3.00     | root      |               | test.t.value, offset:0, count:3                                                             |
|       └─TableReader_25           | 3.00     | root      |               | data:TopN_24                                                                                |
|         └─TopN_24                | 3.00     | cop[tikv] |               | test.t.value, offset:0, count:3                                                             |
|           └─TableFullScan_23     | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo                                                              |
+----------------------------------+----------+-----------+---------------+---------------------------------------------------------------------------------------------+
```

在该查询中，优化器从窗口函数中推导出来了 TopN 并将它下推给了 TiKV。

### 带 partition by 的窗口函数

> **注意：**
> 当窗口函数带有 partition by 时，该优化仅在 partition 列是主键的前缀且主键本身是 clustered index 的时候才能生效
>

#### 示例 3：不带 order by 的窗口函数

{{< copyable "sql" >}}

```sql
create table t(id1 int, id2 int, value1 int, value2 int, primary key(id1,id2) clustered);
set tidb_opt_derive_topn=on;
explain select * from (select row_number() over (partition by id1) as rownumber from t) DT where rownumber <= 3;
```

```
+------------------------------------+---------+-----------+---------------+-----------------------------------------------------------------------------------------------+
| id                                 | estRows | task      | access object | operator info                                                                                 |
+------------------------------------+---------+-----------+---------------+-----------------------------------------------------------------------------------------------+
| Projection_10                      | 2.40    | root      |               | Column#6                                                                                      |
| └─Selection_11                     | 2.40    | root      |               | le(Column#6, 3)                                                                               |
|   └─Shuffle_26                     | 3.00    | root      |               | execution info: concurrency:2, data sources:[TableReader_24]                                  |
|     └─Window_12                    | 3.00    | root      |               | row_number()->Column#6 over(partition by test.t.id1 rows between current row and current row) |
|       └─Sort_25                    | 3.00    | root      |               | test.t.id1                                                                                    |
|         └─TableReader_24           | 3.00    | root      |               | data:Limit_23                                                                                 |
|           └─Limit_23               | 3.00    | cop[tikv] |               | offset:0, count:3                                                                             |
|             └─TableFullScan_22     | 3.00    | cop[tikv] | table:t       | keep order:false, stats:pseudo                                                                |
+------------------------------------+---------+-----------+---------------+-----------------------------------------------------------------------------------------------+
```
在该查询中，优化器从窗口函数中推导出来了 Limit 并将它下推给了 TiKV, 值得一提的是这个 Limit 其实是 partition Limit，也就是说 Limit 实际上作用于每个不同的 id1 的值组成一个 partition 上。

#### 示例 4：带 order by 的窗口函数

{{< copyable "sql" >}}

```sql
create table t(id1 int, id2 int, value1 int, value2 int, primary key(id1,id2) clustered);
set tidb_opt_derive_topn=on;
explain select * from (select row_number() over (partition by id1 order by value1) as rownumber from t) DT where rownumber <= 3;
```

```
+------------------------------------+----------+-----------+---------------+----------------------------------------------------------------------------------------------------------------------+
| id                                 | estRows  | task      | access object | operator info                                                                                                        |
+------------------------------------+----------+-----------+---------------+----------------------------------------------------------------------------------------------------------------------+
| Projection_10                      | 2.40     | root      |               | Column#6                                                                                                             |
| └─Selection_11                     | 2.40     | root      |               | le(Column#6, 3)                                                                                                      |
|   └─Shuffle_23                     | 3.00     | root      |               | execution info: concurrency:3, data sources:[TableReader_21]                                                         |
|     └─Window_12                    | 3.00     | root      |               | row_number()->Column#6 over(partition by test.t.id1 order by test.t.value1 rows between current row and current row) |
|       └─Sort_22                    | 3.00     | root      |               | test.t.id1, test.t.value1                                                                                            |
|         └─TableReader_21           | 3.00     | root      |               | data:TopN_19                                                                                                         |
|           └─TopN_19                | 3.00     | cop[tikv] |               | partition by test.t.id1 order by test.t.value1, offset:0, count:3                                                    |
|             └─TableFullScan_18     | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo                                                                                       |
+------------------------------------+----------+-----------+---------------+----------------------------------------------------------------------------------------------------------------------+
```
在该查询中，优化器从窗口函数中推导出来了 TopN 并将它下推给了 TiKV, 值得一提的是这个 TopN 其实是 partition TopN。

#### 示例 5：partition by 列不是主键的前缀

{{< copyable "sql" >}}

```sql
create table t(id1 int, id2 int, value1 int, value2 int, primary key(id1,id2) clustered);
set tidb_opt_derive_topn=on;
explain select * from (select row_number() over (partition by value1) as rownumber from t) DT where rownumber <= 3;
```

```
+----------------------------------+----------+-----------+---------------+--------------------------------------------------------------------------------------------------+
| id                               | estRows  | task      | access object | operator info                                                                                    |
+----------------------------------+----------+-----------+---------------+--------------------------------------------------------------------------------------------------+
| Projection_9                     | 8000.00  | root      |               | Column#6                                                                                         |
| └─Selection_10                   | 8000.00  | root      |               | le(Column#6, 3)                                                                                  |
|   └─Shuffle_15                   | 10000.00 | root      |               | execution info: concurrency:5, data sources:[TableReader_13]                                     |
|     └─Window_11                  | 10000.00 | root      |               | row_number()->Column#6 over(partition by test.t.value1 rows between current row and current row) |
|       └─Sort_14                  | 10000.00 | root      |               | test.t.value1                                                                                    |
|         └─TableReader_13         | 10000.00 | root      |               | data:TableFullScan_12                                                                            |
|           └─TableFullScan_12     | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo                                                                   |
+----------------------------------+----------+-----------+---------------+--------------------------------------------------------------------------------------------------+
```
在该查询中，因为 partition 的列不是主键的前缀，所以 SQL 没有被改写。

#### 示例 6：partition by 列主键的前缀, 但是主键不是 clustered index

{{< copyable "sql" >}}

```sql
create table t(id1 int, id2 int, value1 int, value2 int, primary key(id1,id2) nonclustered);
set tidb_opt_derive_topn=on;
explain select * from (select row_number() over (partition by id1) as rownumber from t use index()) DT where rownumber <= 3;
```

```
+----------------------------------+----------+-----------+---------------+-----------------------------------------------------------------------------------------------+
| id                               | estRows  | task      | access object | operator info                                                                                 |
+----------------------------------+----------+-----------+---------------+-----------------------------------------------------------------------------------------------+
| Projection_9                     | 8000.00  | root      |               | Column#7                                                                                      |
| └─Selection_10                   | 8000.00  | root      |               | le(Column#7, 3)                                                                               |
|   └─Shuffle_15                   | 10000.00 | root      |               | execution info: concurrency:5, data sources:[TableReader_13]                                  |
|     └─Window_11                  | 10000.00 | root      |               | row_number()->Column#7 over(partition by test.t.id1 rows between current row and current row) |
|       └─Sort_14                  | 10000.00 | root      |               | test.t.id1                                                                                    |
|         └─TableReader_13         | 10000.00 | root      |               | data:TableFullScan_12                                                                         |
|           └─TableFullScan_12     | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo                                                                |
+----------------------------------+----------+-----------+---------------+-----------------------------------------------------------------------------------------------+
```
在该查询中，即使 partition 的列是主键的前缀，但是因为主键不是 clustered index，所以 SQL 没被改写。


### 限制
* 目前支持改写的窗口函数仅包括 row_number()
* 当对 row_number() 过滤条件不是 `<` 或者 `<=` 时不支持改写
* 当过滤条件不是针对 row_number() 时不支持改写
