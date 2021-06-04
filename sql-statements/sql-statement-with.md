---
title: WITH
summary: TiDB 数据库中 WITH (公共表表达式) 的使用概况。
---

# WITH (公共表表达式)

公共表表达式 (CTE) 是一个临时的中间结果集，能够在 SQL 语句中引用多次，提高 SQL 语句的可读性与执行效率。

## 语法图

**WithClause:**

``` ebnf
WithClause ::=
        "WITH" WithList
|       "WITH" recursive WithList
```

**WithList:**

``` ebnf
WithList ::=
        WithList ',' CommonTableExpr
|       CommonTableExpr
```

**CommonTableExpr:**

``` ebnf
CommonTableExpr ::=
        Identifier IdentListWithParenOpt "AS" SubSelect
```

**IdentListWithParenOpt:**

``` ebnf
IdentListWithParenOpt ::=

|       '(' IdentList ')'
```

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

* 在严格模式下，当递归部分算出的数据长度超过初始部分的数据长度时，TiDB 会返回警告，而 MySQL 会返回错误。在非严格模式下，TiDB 与 MySQL 行为一致。
* 递归 CTE 所使用的数据类型由初始部分决定。初始部分的类型在某些情况（例如函数）下并不与 MySQL 完全一致。
* 多个 UNION / UNION ALL 情况下，MySQL 不允许 UNION 后面加 UNION ALL，TiDB 允许。
* 如果 CTE 的定义存在问题，TiDB 会报错，而 MySQL 在未引用的情况下不报错。

## 另请参阅

* [SELECT](/sql-statements/sql-statement-select.md)
* [INSERT](/sql-statements/sql-statement-insert.md)
* [DELETE](/sql-statements/sql-statement-delete.md)
* [UPDATE](/sql-statements/sql-statement-update.md)
* [REPLACE](/sql-statements/sql-statement-replace.md)
