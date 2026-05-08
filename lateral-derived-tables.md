---
title: LATERAL 派生表
summary: 了解 TiDB 中 LATERAL 派生表的语法和当前限制。
---

# LATERAL 派生表

**LATERAL 派生表**是 `FROM` 子句中的一种子查询，它可以引用同一个 `FROM` 子句中位于其前面的表中的列。与标准派生表相比，LATERAL 派生表功能更强，因为标准派生表中的子查询不支持引用同一个 `FROM` 子句中的外部列。

TiDB 可识别用于派生表的 `LATERAL` 语法，该语法遵循 MySQL 8.0 语法（[WL#8652](https://dev.mysql.com/worklog/task/?id=8652)）。

> **注意：**
>
> 当前，TiDB 支持解析 `LATERAL` 派生表语法，但尚不支持执行该语法，执行时会返回错误。你可以通过 issue [#40328](https://github.com/pingcap/tidb/issues/40328) 跟踪完整执行支持的进展。

## 语法

```sql
SELECT ... FROM table_ref, LATERAL (subquery) [AS] alias [(col_list)] ...
SELECT ... FROM table_ref [LEFT] JOIN LATERAL (subquery) [AS] alias [(col_list)] ON ...
```

- `LATERAL` 关键字必须位于派生表子查询之前。
- 子查询右括号后必须指定表别名。
- 别名前的 `AS` 关键字是可选的。
- 别名后可以指定可选的派生列的列表：`LATERAL (...) AS dt(col1, col2)`。

## 示例

### 逗号连接

```sql
SELECT * FROM t1, LATERAL (SELECT * FROM t2 WHERE t2.id = t1.id) AS dt;
```

在此示例中，子查询引用了前一个表 `t1` 中的列 `t1.id`。普通派生表（不带 `LATERAL`）不能这样引用前面的表。

### 带派生列列表的 LEFT JOIN

```sql
SELECT t1.id, dt.val
FROM t1
LEFT JOIN LATERAL (SELECT t2.val FROM t2 WHERE t2.id = t1.id LIMIT 1) AS dt(val)
ON TRUE;
```

派生列列表 `(val)` 将会重命名子查询返回的列。

## 与标准派生表的比较

| 功能 | 标准派生表 | LATERAL 派生表 |
|---|---|---|
| 是否可以引用外部 `FROM` 列 | 否 | 是 |
| 是否必须指定别名 | 是 | 是 |
| 是否支持派生列列表 | 支持 | 支持 |

## MySQL 兼容性

TiDB 的 LATERAL 派生表语法与 MySQL 8.0 语法兼容。

## 另请参阅

- [子查询相关优化](/subquery-optimization.md)
- [关联子查询去关联](/correlated-subquery-optimization.md)
- [使用子查询的 Explain 语句](/explain-subqueries.md)
- [MySQL 兼容性](/mysql-compatibility.md)