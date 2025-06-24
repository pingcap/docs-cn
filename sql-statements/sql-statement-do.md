---
title: DO | TiDB SQL 语句参考
summary: TiDB 数据库中 DO 的使用概述。
---

# DO

`DO` 执行表达式但不返回任何结果。在大多数情况下，`DO` 等同于不返回结果的 `SELECT expr, ...`。

> **注意：**
>
> `DO` 只执行表达式。它不能在所有可以使用 `SELECT` 的场合使用。例如，`DO id FROM t1` 是无效的，因为它引用了一个表。

在 MySQL 中，一个常见的用例是执行存储过程或触发器。由于 TiDB 不提供存储过程或触发器，此功能的使用有限。

## 语法图

```ebnf+diagram
DoStmt   ::= 'DO' ExpressionList

ExpressionList ::=
    Expression ( ',' Expression )*

Expression ::=
    ( singleAtIdentifier assignmentEq | 'NOT' | Expression ( logOr | 'XOR' | logAnd ) ) Expression
|   'MATCH' '(' ColumnNameList ')' 'AGAINST' '(' BitExpr FulltextSearchModifierOpt ')'
|   PredicateExpr ( IsOrNotOp 'NULL' | CompareOp ( ( singleAtIdentifier assignmentEq )? PredicateExpr | AnyOrAll SubSelect ) )* ( IsOrNotOp ( trueKwd | falseKwd | 'UNKNOWN' ) )?
```

## 示例

这个 SELECT 语句会暂停，但同时也会产生一个结果集。

```sql
mysql> SELECT SLEEP(5);
+----------+
| SLEEP(5) |
+----------+
|        0 |
+----------+
1 row in set (5.00 sec)
```

相比之下，DO 会暂停但不产生结果集。

```sql
mysql> DO SLEEP(5);
Query OK, 0 rows affected (5.00 sec)

mysql> DO SLEEP(1), SLEEP(1.5);
Query OK, 0 rows affected (2.50 sec)
```

## MySQL 兼容性

TiDB 中的 `DO` 语句与 MySQL 完全兼容。如果发现任何兼容性差异，请[报告问题](https://docs.pingcap.com/tidb/stable/support)。

## 另请参阅

* [SELECT](/sql-statements/sql-statement-select.md)
