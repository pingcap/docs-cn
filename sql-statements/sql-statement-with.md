---
title: WITH | TiDB SQL 语句参考
summary: TiDB 数据库中 WITH（公用表表达式）的使用概览。
---

# WITH

公用表表达式（Common Table Expression，CTE）是一个临时结果集，可以在 SQL 语句中多次引用，以提高语句的可读性和执行效率。你可以使用 `WITH` 语句来使用公用表表达式。

## 语法

**WithClause:**

```ebnf+diagram
WithClause ::=
        "WITH" WithList
|       "WITH" "RECURSIVE" WithList
```

**WithList:**

```ebnf+diagram
WithList ::=
        WithList ',' CommonTableExpr
|       CommonTableExpr
```

**CommonTableExpr:**

```ebnf+diagram
CommonTableExpr ::=
        Identifier IdentListWithParenOpt "AS" SubSelect
```

**IdentListWithParenOpt:**

```ebnf+diagram
IdentListWithParenOpt ::=
( '(' IdentList ')' )?
```

## 示例

非递归 CTE：

```sql
WITH cte AS (SELECT 1, 2) SELECT * FROM cte t1, cte t2;
```

```
+---+---+---+---+
| 1 | 2 | 1 | 2 |
+---+---+---+---+
| 1 | 2 | 1 | 2 |
+---+---+---+---+
1 row in set (0.00 sec)
```

递归 CTE：

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

* 在严格模式下，当递归计算的数据长度超过种子部分的数据长度时，TiDB 返回警告，而 MySQL 返回错误。在非严格模式下，TiDB 的行为与 MySQL 一致。
* 递归 CTE 的数据类型由种子部分决定。在某些情况下（如函数），种子部分的数据类型与 MySQL 不完全一致。
* 在有多个 `UNION` / `UNION ALL` 运算符的情况下，MySQL 不允许 `UNION` 后面跟 `UNION ALL`，但 TiDB 允许。
* 如果 CTE 的定义有问题，TiDB 会报错，而 MySQL 在 CTE 未被引用时不会报错。

## 另请参阅

* [开发者指南：公用表表达式](/develop/dev-guide-use-common-table-expression.md)
* [SELECT](/sql-statements/sql-statement-select.md)
* [INSERT](/sql-statements/sql-statement-insert.md)
* [DELETE](/sql-statements/sql-statement-delete.md)
* [UPDATE](/sql-statements/sql-statement-update.md)
* [REPLACE](/sql-statements/sql-statement-replace.md)
