---
title: LATERAL 派生表
summary: 了解 TiDB 中 LATERAL 派生表的语法和当前限制。
---

# LATERAL 派生表

**LATERAL 派生表**是 `FROM` 子句中的一种子查询，它可以引用同一 `FROM` 子句中更早出现的表的列。因此，它比标准派生表更强大，因为标准派生表中的子查询不能引用同一 `FROM` 子句中的外部列。

从 v8.5.7 和 v9.0.0 开始，TiDB 按照 MySQL 8.0 的语法（[WL#8652](https://dev.mysql.com/worklog/task/?id=8652)）识别用于派生表的 `LATERAL` 语法。

> **Note:**
>
> 当前，TiDB 支持解析 `LATERAL` 派生表语法，但不支持执行使用该语法的查询。如果你尝试执行此类查询，TiDB 会返回错误。你可以在 issue [#40328](https://github.com/pingcap/tidb/issues/40328) 中跟踪完整执行支持的进展。

## 语法

```sql
SELECT ... FROM table_ref, LATERAL (subquery) [AS] alias [(col_list)] ...
SELECT ... FROM table_ref [LEFT] JOIN LATERAL (subquery) [AS] alias [(col_list)] ON ...
```

- `LATERAL` 关键字必须位于派生表子查询之前。
- 子查询右括号后必须指定表别名。
- 别名前的 `AS` 关键字是可选的。
- 别名后可以跟一个可选的派生列列表，例如 `LATERAL (...) AS dt(col1, col2)`。

## 示例

### 逗号连接

```sql
SELECT * FROM t1, LATERAL (SELECT * FROM t2 WHERE t2.id = t1.id) AS dt;
```

在此示例中，子查询引用了前一个表 `t1` 中的列 `t1.id`。普通派生表（不带 `LATERAL`）无法做到这一点。

### 带派生列列表的 LEFT JOIN

```sql
SELECT t1.id, dt.val
FROM t1
LEFT JOIN LATERAL (SELECT t2.val FROM t2 WHERE t2.id = t1.id LIMIT 1) AS dt(val)
ON TRUE;
```

派生列列表 `(val)` 会重命名子查询返回的列。

## 与标准派生表的比较

| 功能 | 标准派生表 | LATERAL 派生表 |
|---|---|---|
| 是否可以引用外部 `FROM` 列 | 否 | 是 |
| 是否必须指定别名 | 是 | 是 |
| 派生列列表 | 支持 | 支持 |

## MySQL 兼容性

TiDB 的 LATERAL 派生表语法在语法级别上与 MySQL 8.0 兼容。

## 另请参阅

- [Subquery Related Optimizations](/subquery-optimization.md)
- [Decorrelation of Correlated Subquery](/correlated-subquery-optimization.md)
- [Explain Statements That Use Subqueries](/explain-subqueries.md)
- [MySQL Compatibility](/mysql-compatibility.md)