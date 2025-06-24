---
title: 聚合（GROUP BY）函数
summary: 了解 TiDB 支持的聚合函数。
---

# 聚合（GROUP BY）函数

本文档详细介绍了 TiDB 支持的聚合函数。

## 支持的聚合函数

本节介绍 TiDB 支持的 MySQL `GROUP BY` 聚合函数。

| 名称                                                                                                           | 描述                                       |
|:---------------------------------------------------------------------------------------------------------------|:--------------------------------------------------|
| [`COUNT()`](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_count)                   | 返回返回行数的计数     |
| [`COUNT(DISTINCT)`](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_count-distinct)  | 返回不同值的计数  |
| [`SUM()`](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_sum)                       | 返回总和                                    |
| [`AVG()`](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_avg)                       | 返回参数的平均值          |
| [`MAX()`](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_max)                       | 返回最大值                          |
| [`MIN()`](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_min)                       | 返回最小值                          |
| [`GROUP_CONCAT()`](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_group-concat)     | 返回连接后的字符串                      |
| [`VARIANCE()`, `VAR_POP()`](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_var-pop) | 返回总体标准方差           |
| [`STD()`, `STDDEV()`, `STDDEV_POP`](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_std) | 返回总体标准差      |
| [`VAR_SAMP()`](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_var-samp)             | 返回样本方差                        |
| [`STDDEV_SAMP()`](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_stddev-samp)       | 返回样本标准差              |
| [`JSON_ARRAYAGG()`](/functions-and-operators/json-functions/json-functions-aggregate.md#json_arrayagg)         | 将结果集作为单个 JSON 数组返回      |
| [`JSON_OBJECTAGG()`](/functions-and-operators/json-functions/json-functions-aggregate.md#json_objectagg)       | 将结果集作为包含键值对的单个 JSON 对象返回 |

- 除非另有说明，分组函数会忽略 `NULL` 值。
- 如果在不包含 `GROUP BY` 子句的语句中使用分组函数，则等同于对所有行进行分组。

此外，TiDB 还提供以下聚合函数：

+ `APPROX_PERCENTILE(expr, constant_integer_expr)`

    此函数返回 `expr` 的百分位数。`constant_integer_expr` 参数表示百分比值，是范围在 `[1,100]` 内的常量整数。百分位数 P<sub>k</sub>（`k` 表示百分比）表示数据集中至少有 `k%` 的值小于或等于 P<sub>k</sub>。

    此函数仅支持 [数值类型](/data-type-numeric.md) 和 [日期时间类型](/data-type-date-and-time.md) 作为 `expr` 的返回类型。对于其他返回类型，`APPROX_PERCENTILE` 仅返回 `NULL`。

    以下示例展示如何计算 `INT` 列的第五十百分位数：

    ```sql
    DROP TABLE IF EXISTS t;
    CREATE TABLE t(a INT);
    INSERT INTO t VALUES(1), (2), (3);
    ```

    ```sql
    SELECT APPROX_PERCENTILE(a, 50) FROM t;
    ```

    ```sql
    +--------------------------+
    | APPROX_PERCENTILE(a, 50) |
    +--------------------------+
    |                        2 |
    +--------------------------+
    1 row in set (0.00 sec)
    ```

+ `APPROX_COUNT_DISTINCT(expr, [expr...])`

    此函数类似于 `COUNT(DISTINCT)`，用于计算不同值的数量，但返回的是近似结果。它使用 `BJKST` 算法，在处理具有幂律分布的大型数据集时显著减少内存消耗。此外，对于低基数数据，该函数在保持高效 CPU 利用率的同时提供高精度。

    以下示例展示如何使用此函数：

    ```sql
    DROP TABLE IF EXISTS t;
    CREATE TABLE t(a INT, b INT, c INT);
    INSERT INTO t VALUES(1, 1, 1), (2, 1, 1), (2, 2, 1), (3, 1, 1), (5, 1, 2), (5, 1, 2), (6, 1, 2), (7, 1, 2);
    ```

    ```sql
    SELECT APPROX_COUNT_DISTINCT(a, b) FROM t GROUP BY c;
    ```

    ```
    +-----------------------------+
    | approx_count_distinct(a, b) |
    +-----------------------------+
    |                           3 |
    |                           4 |
    +-----------------------------+
    2 rows in set (0.00 sec)
    ```

除了 `GROUP_CONCAT()`、`APPROX_PERCENTILE()` 和 `APPROX_COUNT_DISTINCT` 函数外，所有上述函数都可以作为[窗口函数](/functions-and-operators/window-functions.md)使用。

## GROUP BY 修饰符

从 v7.4.0 开始，TiDB 的 `GROUP BY` 子句支持 `WITH ROLLUP` 修饰符。更多信息，请参见 [GROUP BY 修饰符](/functions-and-operators/group-by-modifier.md)。

## SQL 模式支持

TiDB 支持 SQL 模式 `ONLY_FULL_GROUP_BY`，启用时 TiDB 将拒绝包含不明确非聚合列的查询。例如，当启用 `ONLY_FULL_GROUP_BY` 时，以下查询是非法的，因为 `SELECT` 列表中的非聚合列 "b" 未出现在 `GROUP BY` 语句中：

```sql
drop table if exists t;
create table t(a bigint, b bigint, c bigint);
insert into t values(1, 2, 3), (2, 2, 3), (3, 2, 3);

mysql> select a, b, sum(c) from t group by a;
+------+------+--------+
| a    | b    | sum(c) |
+------+------+--------+
|    1 |    2 |      3 |
|    2 |    2 |      3 |
|    3 |    2 |      3 |
+------+------+--------+
3 rows in set (0.01 sec)

mysql> set sql_mode = 'ONLY_FULL_GROUP_BY';
Query OK, 0 rows affected (0.00 sec)

mysql> select a, b, sum(c) from t group by a;
ERROR 1055 (42000): Expression #2 of SELECT list is not in GROUP BY clause and contains nonaggregated column 'b' which is not functionally dependent on columns in GROUP BY clause; this is incompatible with sql_mode=only_full_group_by
```

TiDB 目前默认启用 [`ONLY_FULL_GROUP_BY`](/mysql-compatibility.md#default-differences) 模式。

### 与 MySQL 的差异

当前 `ONLY_FULL_GROUP_BY` 的实现比 MySQL 5.7 中的实现要宽松。例如，假设我们执行以下查询，期望结果按 "c" 排序：

```sql
drop table if exists t;
create table t(a bigint, b bigint, c bigint);
insert into t values(1, 2, 1), (1, 2, 2), (1, 3, 1), (1, 3, 2);
select distinct a, b from t order by c;
```

要对结果进行排序，必须先消除重复项。但是，我们应该保留哪一行？这个选择会影响保留的 "c" 值，进而影响排序并使其变得任意。

在 MySQL 中，如果任何 `ORDER BY` 表达式不满足以下条件之一，则包含 `DISTINCT` 和 `ORDER BY` 的查询将被拒绝为无效：

- 该表达式等于 `SELECT` 列表中的一个表达式
- 表达式引用的所有列都属于查询的选定表，并且是 `SELECT` 列表的元素

但在 TiDB 中，上述查询是合法的，更多信息请参见 [#4254](https://github.com/pingcap/tidb/issues/4254)。

TiDB 对标准 SQL 的另一个扩展是允许在 `HAVING` 子句中引用 `SELECT` 列表中的别名表达式。例如，以下查询返回表 "orders" 中只出现一次的 "name" 值：

```sql
select name, count(name) from orders
group by name
having count(name) = 1;
```

TiDB 扩展允许在 `HAVING` 子句中使用聚合列的别名：

```sql
select name, count(name) as c from orders
group by name
having c = 1;
```

标准 SQL 仅允许在 `GROUP BY` 子句中使用列表达式，因此像这样的语句是无效的，因为 "FLOOR(value/100)" 是非列表达式：

```sql
select id, floor(value/100)
from tbl_name
group by id, floor(value/100);
```

TiDB 扩展了标准 SQL，允许在 `GROUP BY` 子句中使用非列表达式，并认为上述语句有效。

标准 SQL 也不允许在 `GROUP BY` 子句中使用别名。TiDB 扩展了标准 SQL 以允许使用别名，因此可以这样编写查询：

```sql
select id, floor(value/100) as val
from tbl_name
group by id, val;
```

## 相关系统变量

[`group_concat_max_len`](/system-variables.md#group_concat_max_len) 变量设置 `GROUP_CONCAT()` 函数的最大项目数。
