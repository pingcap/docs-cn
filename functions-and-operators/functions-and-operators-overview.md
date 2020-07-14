---
title: Function and Operator Reference
summary: Learn how to use the functions and operators.
aliases: ['/docs/dev/functions-and-operators/functions-and-operators-overview/','/docs/dev/reference/sql/functions-and-operators/reference/']
---

# Function and Operator Reference

The usage of the functions and operators in TiDB is similar to MySQL. See [Functions and Operators in MySQL](https://dev.mysql.com/doc/refman/5.7/en/functions.html).

In SQL statements, expressions can be used on the `ORDER BY` and `HAVING` clauses of the `SELECT` statement, the `WHERE` clause of `SELECT`/`DELETE`/`UPDATE` statements, and `SET` statements.

You can write expressions using literals, column names, NULL, built-in functions, operators and so on. For expressions that TiDB supports pushing down to TiKV, see [List of Expressions for Pushdown](/functions-and-operators/expressions-pushed-down.md).
