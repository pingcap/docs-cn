---
title: 函数和运算符参考
summary: 了解如何使用函数和运算符。
---

# 函数和运算符参考

TiDB 中函数和运算符的使用方式与 MySQL 类似。请参见 [MySQL 中的函数和运算符](https://dev.mysql.com/doc/refman/8.0/en/functions.html)。

在 SQL 语句中，表达式可以用在 [`SELECT`](/sql-statements/sql-statement-select.md) 语句的 `ORDER BY` 和 `HAVING` 子句中，[`SELECT`](/sql-statements/sql-statement-select.md)/[`DELETE`](/sql-statements/sql-statement-delete.md)/[`UPDATE`](/sql-statements/sql-statement-update.md) 语句的 `WHERE` 子句中，以及 [`SET`](/sql-statements/sql-statement-set-variable.md) 语句中。

你可以使用字面量、列名、`NULL`、内置函数、运算符等来编写表达式。

- 关于 TiDB 支持下推到 TiKV 的表达式，请参见[可下推表达式列表](/functions-and-operators/expressions-pushed-down.md)。
- 关于 TiDB 支持下推到 [TiFlash](/tiflash/tiflash-overview.md) 的表达式，请参见[下推表达式](/tiflash/tiflash-supported-pushdown-calculations.md#push-down-expressions)。
