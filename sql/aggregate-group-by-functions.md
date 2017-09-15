---
title: GROUP BY 聚合函数
category: user guide
---

# GROUP BY 聚合函数

## GROUP BY 聚合函数功能描述

本节介绍 TiDB 中支持的 MySQL GROUP BY 聚合函数。

| 函数名    | 功能描述              |
|:---------|:--------------------|
| [`COUNT()`](https://dev.mysql.com/doc/refman/5.7/en/group-by-functions.html#function_count)                   | 返回检索到的行的数目|
| [`COUNT(DISTINCT)`](https://dev.mysql.com/doc/refman/5.7/en/group-by-functions.html#function_count-distinct)  | 返回不同值的数目 |
| [`SUM()`](https://dev.mysql.com/doc/refman/5.7/en/group-by-functions.html#function_sum)                       | 返回和         |
| [`AVG()`](https://dev.mysql.com/doc/refman/5.7/en/group-by-functions.html#function_avg)                       | 返回平均值     |
| [`MAX()`](https://dev.mysql.com/doc/refman/5.7/en/group-by-functions.html#function_max)                       | 返回最大值     |
| [`MIN()`](https://dev.mysql.com/doc/refman/5.7/en/group-by-functions.html#function_min)                       | 返回最小值     |
| [`GROUP_CONCAT()`](https://dev.mysql.com/doc/refman/5.7/en/group-by-functions.html#function_group-concat)     | 返回连接的字符串  |

> **Note**:
>
> - 除非另有说明，否则组函数默认忽略 `NULL` 值。
> - 如果在不包含 `GROUP BY` 子句的语句中使用组函数，则相当于对所有行进行分组。详情参阅 [TiDB 中的 GROUP BY](#tidb-中的-group-by)。 

## GROUP BY 修饰符

TiDB 目前不支持任何 `GROUP BY` 修饰符，将来会提供支持，详情参阅 [#4250](https://github.com/pingcap/tidb/issues/4250)。 

## TiDB 中的 GROUP BY

当 SQL 模式 [`ONLY_FULL_GROUP_BY`](https://dev.mysql.com/doc/refman/5.7/en/sql-mode.html#sqlmode_only_full_group_by) 被禁用时，TiDB 与 MySQL 等效：允许 `SELECT` 列表、`HAVING` 条件或 `ORDER BY` 列表引用非聚合列，即使这些列在功能上不依赖于 `GROUP BY` 列。

例如，在 MySQL 5.7.5 中使用 `ONLY_FULL_GROUP_BY` 的查询是不合规的，因为 `SELECT` 列表中的非聚合列 "b" 在 `GROUP BY` 中不显示：

```sql
drop table if exists t;
create table t(a bigint, b bigint, c bigint);
insert into t values(1, 2, 3), (2, 2, 3), (3, 2, 3);
select a, b, sum(c) from t group by a;
```

上述查询在 TiDB 中是合规的。TiDB 目前不支持 SQL 模式 `ONLY_FULL_GROUP_BY`，将来会提供支持，详情参阅 [#4248](https://github.com/pingcap/tidb/issues/4248)。

假设我们执行以下查询，希望结果按 `c` 排序:

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

```sql
select name, count(name) from orders
group by name
having count(name) = 1;
```

这个 TiDB 扩展允许在聚合列的 `HAVING` 子句中使用别名：

```sql
select name, count(name) as c from orders
group by name
having c = 1;
```

标准 SQL 只支持 `GROUP BY` 子句中的列表达式，以下语句不合规，因为 `FLOOR(value/100)` 是一个非列表达式：

```sql
select id, floor(value/100)
from tbl_name
group by id, floor(value/100);
```

TiDB 对标准 SQL 的扩展支持 `GROUP BY` 子句中非列表达式，认为上述语句合规。

标准 SQL 也不支持 `GROUP BY` 子句中使用别名。TiDB 对标准 SQL 的扩展支持使用别名，查询的另一种写法如下：

```sql
select id, floor(value/100) as val
from tbl_name
group by id, val;
```

## 函数依赖检测

TiDB 不支持 SQL 模式 `ONLY_FULL_GROUP_BY` 和函数依赖检测，将来会提供支持，详情参阅 [#4248](https://github.com/pingcap/tidb/issues/4248)。
