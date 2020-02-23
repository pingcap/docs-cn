---
title: 函数和操作符概述
category: reference
aliases: ['/docs-cn/sql/functions-and-operators-reference/']
---

# 函数和操作符概述

TiDB 中函数和操作符使用方法与 MySQL 基本一致，详情参见: [Functions and Operators](https://dev.mysql.com/doc/refman/5.7/en/functions.html)。

在 SQL 语句中，表达式可用于诸如 `SELECT` 语句的 `ORDER BY` 或 `HAVING` 子句，`SELECT`/`DELETE`/`UPDATE` 语句的 `WHERE` 子句，或 `SET` 语句之类的地方。

可使用字面值，列名，NULL，内置函数，操作符等来书写表达式。其中有些表达式下推到 TiKV 上执行，详见[下推到 TiKV 的表达式列表](/v3.0/reference/sql/functions-and-operators/expressions-pushed-down.md)。