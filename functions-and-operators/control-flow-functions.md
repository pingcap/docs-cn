---
title: 控制流程函数
aliases: ['/docs-cn/dev/functions-and-operators/control-flow-functions/','/docs-cn/dev/reference/sql/functions-and-operators/control-flow-functions/']
summary: TiDB 支持 MySQL 5.7 中的控制流程函数，包括 CASE、IF()、IFNULL() 和 NULLIF()。这些函数可以用于构建 if/else 语句和处理 NULL 值。
---

# 控制流程函数

TiDB 支持使用 MySQL 5.7 中提供的所有[控制流程函数](https://dev.mysql.com/doc/refman/5.7/en/flow-control-functions.html)。

| 函数名                                                                                            | 功能描述                       |
|:--------------------------------------------------------------------------------------------------|:----------------------------------|
| [`CASE`](https://dev.mysql.com/doc/refman/8.0/en/flow-control-functions.html#operator_case)       | Case 操作符                     |
| [`IF()`](https://dev.mysql.com/doc/refman/8.0/en/flow-control-functions.html#function_if)         | 构建 if/else                 |
| [`IFNULL()`](https://dev.mysql.com/doc/refman/8.0/en/flow-control-functions.html#function_ifnull) | 构建 Null if/else            |
| [`NULLIF()`](https://dev.mysql.com/doc/refman/8.0/en/flow-control-functions.html#function_nullif) | 如果 expr1 = expr2，返回 `NULL`    |
