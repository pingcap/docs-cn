---
title: DO | TiDB SQL Statement Reference
summary: TiDB 数据库中 DO 的使用概况。
---

# DO

`DO` 语句用于执行表达式，但不返回任何结果。大部分情况下，`DO` 相当于不返回结果的 `SELECT expr, ...,`。

> **注意：**
>
> `DO` 只能执行表达式，所以不是所有能够用 `SELECT` 的地方都能用 `DO` 替换。例如 `DO id FROM t1` 就是不是合法的 SQL 语句，因为它引用了一张表。

`DO` 在 MySQL 中的一个主要应用场景是存储过程或者触发器。因为 TiDB 当前不支持存储过程和触发器，所以 `DO` 的实际使用场景较少。

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

这条 `SELECT` 语句会暂停执行，但同时也会返回一个结果集。

{{< copyable "sql" >}}

```sql
SELECT SLEEP(5);
```

```
+----------+
| SLEEP(5) |
+----------+
|        0 |
+----------+
1 row in set (5.00 sec)
```

如果使用 `DO` 的话，语句同样会暂停，但不会返回结果集。

{{< copyable "sql" >}}

```sql
DO SLEEP(5);
```

```
Query OK, 0 rows affected (5.00 sec)
```

{{< copyable "sql" >}}

```sql
DO SLEEP(1), SLEEP(1.5);
```

```
Query OK, 0 rows affected (2.50 sec)
```

## MySQL 兼容性

`DO` 语句与 MySQL 完全兼容。如发现任何兼容性差异，请在 GitHub 上提交 [issue](https://github.com/pingcap/tidb/issues/new/choose)。

## 另请参阅

* [SELECT](/sql-statements/sql-statement-select.md)
