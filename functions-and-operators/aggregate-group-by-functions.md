---
title: GROUP BY 聚合函数
aliases: ['/docs-cn/stable/functions-and-operators/aggregate-group-by-functions/','/docs-cn/v4.0/functions-and-operators/aggregate-group-by-functions/','/docs-cn/stable/reference/sql/functions-and-operators/aggregate-group-by-functions/']
---

# GROUP BY 聚合函数

本文将详细介绍 TiDB 支持的聚合函数。

## TiDB 支持的聚合函数

TiDB 支持的 MySQL `GROUP BY` 聚合函数如下所示：

| 函数名    | 功能描述              |
|:---------|:--------------------|
| [`COUNT()`](https://dev.mysql.com/doc/refman/5.7/en/aggregate-functions.html#function_count)                   | 返回检索到的行的数目|
| [`COUNT(DISTINCT)`](https://dev.mysql.com/doc/refman/5.7/en/aggregate-functions.html#function_count-distinct)  | 返回不同值的数目 |
| [`SUM()`](https://dev.mysql.com/doc/refman/5.7/en/aggregate-functions.html#function_sum)                       | 返回和         |
| [`AVG()`](https://dev.mysql.com/doc/refman/5.7/en/aggregate-functions.html#function_avg)                       | 返回平均值     |
| [`MAX()`](https://dev.mysql.com/doc/refman/5.7/en/aggregate-functions.html#function_max)                       | 返回最大值     |
| [`MIN()`](https://dev.mysql.com/doc/refman/5.7/en/aggregate-functions.html#function_min)                       | 返回最小值     |
| [`GROUP_CONCAT()`](https://dev.mysql.com/doc/refman/5.7/en/aggregate-functions.html#function_group-concat)     | 返回连接的字符串  |
| [`VARIANCE()`，`VAR_POP()`](https://dev.mysql.com/doc/refman/5.7/en/aggregate-functions.html#function_var-pop) | 返回总体标准方差 |
| [`STD()`，`STDDEV()`，`STDDEV_POP`](https://dev.mysql.com/doc/refman/5.7/en/aggregate-functions.html#function_std) | 返回总体标准差 |
| [`VAR_SAMP()`](https://dev.mysql.com/doc/refman/5.7/en/aggregate-functions.html#function_var-samp) | 返回采样方差 |
| [`STDDEV_SAMP()`](https://dev.mysql.com/doc/refman/5.7/en/aggregate-functions.html#function_stddev-samp) | 返回采样标准方差 |
| [`JSON_OBJECTAGG(key, value)`](https://dev.mysql.com/doc/refman/5.7/en/aggregate-functions.html#function_json-objectagg) | 将结果集返回为单个含 (key, value) 键值对的 JSON object |

> **注意：**
>
> - 除非另有说明，否则聚合函数默认忽略 `NULL` 值。
> - 如果在不包含 `GROUP BY` 子句的语句中使用聚合函数，则相当于对所有行进行分组。

另外，TiDB 还支持以下聚合函数：

+ `APPROX_PERCENTILE(expr, constant_integer_expr)`

    该函数用于计算 `expr` 值的百分位数。参数 `constant_integer_expr` 是一个取值为区间 `[1,100]` 内整数的常量表达式，表示百分数。一个百分位数 P<sub>k</sub>（`k`为百分数）表示数据集中至少有 `k%` 的数据小于等于 P<sub>k</sub>。

    该函数中，表达式的返回结果必须为[数值类型](/data-type-numeric.md)或[日期与时间类型](/data-type-date-and-time.md)。函数不支持计算其他类型的返回结果，并直接返回 `NULL`。

    以下是一个计算第 50 百分位数的例子：

    {{< copyable "sql" >}}

    ```sql
    drop table if exists t;
    create table t(a int);
    insert into t values(1), (2), (3);
    ```

    {{< copyable "sql" >}}

    ```sql
    select approx_percentile(a, 50) from t;
    ```

    ```sql
    +--------------------------+
    | approx_percentile(a, 50) |
    +--------------------------+
    |                        2 |
    +--------------------------+
    1 row in set (0.00 sec)
    ```

## GROUP BY 修饰符

TiDB 目前不支持 `GROUP BY` 修饰符，例如 `WITH ROLLUP`，将来会提供支持。详情参阅 [#4250](https://github.com/pingcap/tidb/issues/4250)。

## 对 SQL 模式的支持

TiDB 支持 SQL 模式 `ONLY_FULL_GROUP_BY`，当启用该模式时，TiDB 拒绝不明确的非聚合列的查询。例如，以下查询在启用 `ONLY_FULL_GROUP_BY` 时是不合规的，因为 `SELECT` 列表中的非聚合列 "b" 在 `GROUP BY` 语句中不显示：

{{< copyable "sql" >}}

```sql
drop table if exists t;
create table t(a bigint, b bigint, c bigint);
insert into t values(1, 2, 3), (2, 2, 3), (3, 2, 3);
```

{{< copyable "sql" >}}

```sql
select a, b, sum(c) from t group by a;
```

```
+------+------+--------+
| a    | b    | sum(c) |
+------+------+--------+
|    1 |    2 |      3 |
|    2 |    2 |      3 |
|    3 |    2 |      3 |
+------+------+--------+
3 rows in set (0.01 sec)
```

{{< copyable "sql" >}}

```sql
set sql_mode = 'ONLY_FULL_GROUP_BY';
```

```
Query OK, 0 rows affected (0.00 sec)
```

{{< copyable "sql" >}}

```sql
select a, b, sum(c) from t group by a;
```

```
ERROR 1055 (42000): Expression #2 of SELECT list is not in GROUP BY clause and contains nonaggregated column 'b' which is not functionally dependent on columns in GROUP BY clause; this is incompatible with sql_mode=only_full_group_by
```

目前，TiDB 默认开启 SQL 模式 [`ONLY_FULL_GROUP_BY`](/mysql-compatibility.md#sql-模式)。

### 与 MySQL 的区别

TiDB 目前实现的 `ONLY_FULL_GROUP_BY` 没有 MySQL 5.7 严格。例如，假设我们执行以下查询，希望结果按 "c" 排序：

{{< copyable "sql" >}}

```sql
drop table if exists t;
create table t(a bigint, b bigint, c bigint);
insert into t values(1, 2, 1), (1, 2, 2), (1, 3, 1), (1, 3, 2);
select distinct a, b from t order by c;
```

要对结果进行排序，必须先清除重复。但选择保留哪一行会影响 `c` 的保留值，也会影响排序，并使其具有任意性。

在 MySQL 中，`ORDER BY` 表达式需至少满足以下条件之一，否则 `DISTINCT` 和 `ORDER BY` 查询将因不合规而被拒绝：

- 表达式等同于 `SELECT` 列表中的一个。
- 表达式引用并属于查询选择表的所有列都是 `SELECT` 列表的元素。

但是在 TiDB 中，上述查询是合规的，详情参阅 [#4254](https://github.com/pingcap/tidb/issues/4254)。

TiDB 中另一个标准 SQL 的扩展允许 `HAVING` 子句中的引用使用 `SELECT` 列表中的别名表达式。例如：以下查询返回在 `orders` 中只出现一次的 `name` 值：

{{< copyable "sql" >}}

```sql
select name, count(name) from orders
group by name
having count(name) = 1;
```

这个 TiDB 扩展允许在聚合列的 `HAVING` 子句中使用别名：

{{< copyable "sql" >}}

```sql
select name, count(name) as c from orders
group by name
having c = 1;
```

标准 SQL 只支持 `GROUP BY` 子句中的列表达式，以下语句不合规，因为 `FLOOR(value/100)` 是一个非列表达式：

{{< copyable "sql" >}}

```sql
select id, floor(value/100)
from tbl_name
group by id, floor(value/100);
```

TiDB 对标准 SQL 的扩展支持 `GROUP BY` 子句中非列表达式，认为上述语句合规。

标准 SQL 也不支持 `GROUP BY` 子句中使用别名。TiDB 对标准 SQL 的扩展支持使用别名，查询的另一种写法如下：

{{< copyable "sql" >}}

```sql
select id, floor(value/100) as val
from tbl_name
group by id, val;
```

## TiDB 不支持的聚合函数

TiDB 目前不支持的聚合函数如下所示，相关进展参阅 [TiDB #7623](https://github.com/pingcap/tidb/issues/7623)。

- `JSON_ARRAYAGG`
