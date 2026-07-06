---
title: 横向派生表
summary: 了解 TiDB 中横向派生表 (`LATERAL` derived table) 的语法和当前限制。
---

# 横向派生表

横向派生表 (`LATERAL` derived table) 是 `FROM` 子句中的一种子查询，它可以引用同一个 `FROM` 子句中位于其前面的表中的列。相比而言，标准派生表中的子查询无法引用同一个 `FROM` 子句中其它表中的列，因此横向派生表更加灵活。

从 v8.5.7 和 v9.0.0 开始，TiDB 支持解析 `LATERAL` 派生表语法，该语法与 MySQL 8.0 的语法（[WL#8652](https://dev.mysql.com/worklog/task/?id=8652)）一致。

> **注意：**
>
> 目前，TiDB 仅支持解析 `LATERAL` 派生表语法，尚不支持执行使用该语法的查询。如果你尝试执行此类查询，TiDB 将返回错误。你可以在 issue [#40328](https://github.com/pingcap/tidb/issues/40328) 中了解该功能完整执行支持的开发进展。

## 语法

```sql
SELECT ... FROM table_ref, LATERAL (subquery) [AS] alias [(col_list)] ...
SELECT ... FROM table_ref [INNER | CROSS | LEFT [OUTER] | RIGHT [OUTER]] JOIN LATERAL (subquery) [AS] alias [(col_list)] ON ...
```

- `LATERAL` 关键字必须位于派生表子查询之前。
- 子查询的右括号后必须指定表别名。
- 别名前的 `AS` 关键字是可选的。
- 别名后可以跟一个可选的派生列列表，例如 `LATERAL (...) AS dt(col1, col2)`。

## 示例

### 使用逗号连接 `LATERAL` 派生表

```sql
SELECT * FROM t1, LATERAL (SELECT * FROM t2 WHERE t2.id = t1.id) AS dt;
```

在此示例中，`t1` 和 `LATERAL` 派生表在同一个 `FROM` 子句中使用逗号连接。`LATERAL` 派生表中的子查询引用了位于其前面的表 `t1` 中的列 `t1.id`。普通派生表（不带 `LATERAL`）不支持此功能。

### 在 `LEFT JOIN` 中使用 `LATERAL` 派生表（带派生列列表）

```sql
SELECT t1.id, dt.val
FROM t1
LEFT JOIN LATERAL (SELECT t2.val FROM t2 WHERE t2.id = t1.id LIMIT 1) AS dt(val)
ON TRUE;
```

在此示例中，`LATERAL` 派生表作为 `LEFT JOIN` 的右表，可以引用左表 `t1` 中的列 `t1.id`。派生列列表 `(val)` 会将子查询返回的列命名为 `val`。

## 与标准派生表的比较

| 功能 | 标准派生表 | 横向派生表 |
|---|---|---|
| 能否引用 `FROM` 子句中位于其前面的表中的列 | 否 | 是 |
| 是否必须指定别名 | 是 | 是 |
| 是否支持派生列列表 | 支持 | 支持 |

## MySQL 兼容性

TiDB 的 `LATERAL` 派生表语法与 MySQL 8.0 语法兼容。

## 另请参阅

- [子查询相关的优化](/subquery-optimization.md)
- [关联子查询去关联](/correlated-subquery-optimization.md)
- [用 EXPLAIN 查看子查询的执行计划](/explain-subqueries.md)
- [MySQL 兼容性](/mysql-compatibility.md)