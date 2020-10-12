---
title: 集合运算
summary: 了解 TiDB 支持的集合运算。
---

# 集合运算

TiDB 支持三种集合运算：并集 (UNION)，差集 (EXCEPT) 和交集 (INTERSECT)。最小的集合单位是一个 [`SELECT` 语句](/sql-statements/sql-statement-select.md)。

## 并集 (UNION)

数学上，两个集合 A 和 B 的并集是含有所有属于 A 或属于 B 的元素。下面是一个 UNION 的例子：

```sql
select 1 union select 2;
+---+
| 1 |
+---+
| 2 |
| 1 |
+---+
2 rows in set (0.00 sec)
```

TiDB 支持 `UNION ALL` 和 `UNION DISTINCT` 并集，两者区别在于 `UNION DISTINCT` 会对并集结果去重复，而 `UNION ALL` 不会。TiDB 中默认使用 `UNION DISTINCT`。

{{< copyable "sql" >}}

```sql
create table t1 (a int);
create table t2 (a int);
insert into t1 values (1),(2);
insert into t2 values (1),(3);
```

`UNION DISTINCT`与 `UNION ALL` 的结果分别如下：

```sql
select * from t1 union distinct select * from t2;
+---+
| a |
+---+
| 1 |
| 2 |
| 3 |
+---+
3 rows in set (0.00 sec)

select * from t1 union all select * from t2;
+---+
| a |
+---+
| 1 |
| 2 |
| 1 |
| 3 |
+---+
4 rows in set (0.00 sec)
```

## 差集 (EXCEPT)

若 A 和 B 是集合，则 A 与 B 的差集是由所有属于 A 但不属于 B 的元素组成的集合。

```sql
select * from t1 except select * from t2;
+---+
| a |
+---+
| 2 |
+---+
1 rows in set (0.00 sec)
```

差集 (EXCEPT) 暂时不支持 `EXCEPT ALL`。

## 交集（INTERSECT）

数学上，两个集合 A 和 B 的交集是含有所有既属于 A 又属于 B 的元素，而且没有其他元素的集合。

```sql
select * from t1 intersect select * from t2;
+---+
| a |
+---+
| 1 |
+---+
1 rows in set (0.00 sec)
```

交集 (INTERSECT) 暂时不支持 `INTERSECT ALL`。交集 (INTERSECT) 的计算优先级大于差集 (EXCEPT) 和并集 (UNION)。

```sql
select * from t1 union all select * from t1 intersect select * from t2;
+---+
| a |
+---+
| 1 |
| 1 |
| 2 |
+---+
3 rows in set (0.00 sec)
```

## 括号优先

TiDB 支持使用括号修改集合运算的优先级，如同[四则运算](https://zh.wikipedia.org/zh-hans/%E5%9B%9B%E5%88%99%E8%BF%90%E7%AE%97)中先计算括号部分，集合运算也先计算括号内的部分。

```sql
(select * from t1 union all select * from t1) intersect select * from t2;
+---+
| a |
+---+
| 1 |
+---+
1 rows in set (0.00 sec)
```

## 与 `Order By` 和 `Limit` 结合

TiDB 支持单独为整个集合运算进行 [`ORDER BY`](/media/sqlgram/OrderByOptional.png) 或者 [`LIMIT`](/media/sqlgram/LimitClause.png)。

```sql
(select * from t1 union all select * from t1 intersect select * from t2) order by a limit 2;
+---+
| a |
+---+
| 1 |
| 1 |
+---+
2 rows in set (0.00 sec)
```
