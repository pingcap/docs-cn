---
title: WITH (公共表表达式)
summary: TiDB 数据库中 WITH (公共表表达式) 的使用概况。
---

# WITH (公共表表达式)

`公共表表达式` 是一个临时的中间结果集，能够在语句中多次引用。

## 语法图

**WithClause:**

![WithClause](/media/sqlgram/WithClause.png)

**CommonTableExpr:**

![CommonTableExpr](/media/sqlgram/CommonTableExpr.png)

**CommonTableExpr:**

![CommonTableExpr](/media/sqlgram/CommonTableExpr.png)

**IdentListWithParenOpt:**

![IdentListWithParenOpt](/media/sqlgram/IdentListWithParenOpt.png)

## 示例

非递归的 CTE：

{{< copyable "sql" >}}

```sql
WITH CTE AS (SELECT 1, 2) SELECT * FROM cte t1, cte t2;
```

```
+---+---+---+---+
| 1 | 2 | 1 | 2 |
+---+---+---+---+
| 1 | 2 | 1 | 2 |
+---+---+---+---+
1 row in set (0.00 sec)
```

递归的 CTE：

{{< copyable "sql" >}}

```sql
WITH RECURSIVE cte(a) AS (SELECT 1 UNION SELECT a+1 FROM cte WHERE a < 5) SELECT * FROM cte;
```

```
+---+
| a |
+---+
| 1 |
| 2 |
| 3 |
| 4 |
| 5 |
+---+
5 rows in set (0.00 sec)
```

## MySQL 兼容性

CTE 语句与 MySQL 完全兼容。如发现任何兼容性差异，请在 GitHub 上提交 [issue](https://github.com/pingcap/tidb/issues/new/choose)。

## 另请参阅

* [SELECT](/sql-statements/sql-statement-select.md)
* [INSERT](/sql-statements/sql-statement-insert.md)
* [DELETE](/sql-statements/sql-statement-delete.md)
* [UPDATE](/sql-statements/sql-statement-update.md)
* [REPLACE](/sql-statements/sql-statement-replace.md)