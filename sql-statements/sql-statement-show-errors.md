---
title: SHOW ERRORS | TiDB SQL 语句参考
summary: TiDB 数据库中 SHOW ERRORS 的使用概述。
---

# SHOW ERRORS

此语句显示之前执行的语句中的错误。当语句成功执行时，错误缓冲区会被清除。在这种情况下，`SHOW ERRORS` 将返回一个空集。

哪些语句生成错误而不是警告的行为很大程度上受当前 `sql_mode` 的影响。

## 语法概要

```ebnf+diagram
ShowErrorsStmt ::=
    "SHOW" "ERRORS" ShowLikeOrWhere?

ShowLikeOrWhere ::=
    "LIKE" SimpleExpr
|   "WHERE" Expression
```

## 示例

```sql
mysql> select invalid;
ERROR 1054 (42S22): Unknown column 'invalid' in 'field list'
mysql> create invalid;
ERROR 1064 (42000): You have an error in your SQL syntax; check the manual that corresponds to your TiDB version for the right syntax to use line 1 column 14 near "invalid"
mysql> SHOW ERRORS;
+-------+------+-----------------------------------------------------------------------------------------------------------------------------------------------------------+
| Level | Code | Message                                                                                                                                                   |
+-------+------+-----------------------------------------------------------------------------------------------------------------------------------------------------------+
| Error | 1054 | Unknown column 'invalid' in 'field list'                                                                                                                  |
| Error | 1064 | You have an error in your SQL syntax; check the manual that corresponds to your TiDB version for the right syntax to use line 1 column 14 near "invalid"  |
+-------+------+-----------------------------------------------------------------------------------------------------------------------------------------------------------+
2 rows in set (0.00 sec)

mysql> CREATE invalid2;
ERROR 1064 (42000): You have an error in your SQL syntax; check the manual that corresponds to your TiDB version for the right syntax to use line 1 column 15 near "invalid2"
mysql> SELECT 1;
+------+
| 1    |
+------+
|    1 |
+------+
1 row in set (0.00 sec)

mysql> SHOW ERRORS;
Empty set (0.00 sec)
```

## MySQL 兼容性

TiDB 中的 `SHOW ERRORS` 语句与 MySQL 完全兼容。如果发现任何兼容性差异，请[报告 bug](https://docs.pingcap.com/tidb/stable/support)。

## 另请参阅

* [SHOW WARNINGS](/sql-statements/sql-statement-show-warnings.md)
