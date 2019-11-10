---
title: Window Functions
summary: This document introduces window functions supported in TiDB.
category: reference
---

# Window Functions

The usage of window functions in TiDB is similar to that in MySQL 8.0. For details, see [MySQL Window Functions](https://dev.mysql.com/doc/refman/8.0/en/window-functions.html).

Because window functions reserve additional words in the parser, TiDB provides an option to disable window functions. If you receive errors parsing SQL statements after upgrading, try setting `tidb_enable_window_function=0`.

TiDB supports the following window functions:

| Function name | Feature description |
| :-------------- | :------------------------------------- |
| [`CUME_DIST()`](https://dev.mysql.com/doc/refman/8.0/en/window-function-descriptions.html#function_cume-dist) | Returns the cumulative distribution of a value within a group of values. |
| [`DENSE_RANK()`](https://dev.mysql.com/doc/refman/8.0/en/window-function-descriptions.html#function_dense-rank) | Returns the rank of the current row within the partition, and the rank is without gaps. |
| [`FIRST_VALUE()`](https://dev.mysql.com/doc/refman/8.0/en/window-function-descriptions.html#function_first-value) | Returns the expression value of the first row in the current window. |
| [`LAG()`](https://dev.mysql.com/doc/refman/8.0/en/window-function-descriptions.html#function_lag) | Returns the expression value from the row that precedes the current row by N rows within the partition. |
| [`LAST_VALUE()`](https://dev.mysql.com/doc/refman/8.0/en/window-function-descriptions.html#function_last-value) | Returns the expression value of the last row in the current window. |
| [`LEAD()`](https://dev.mysql.com/doc/refman/8.0/en/window-function-descriptions.html#function_lead) | Returns the expression value from the row that follows the current row by N rows within the partition. |
| [`NTH_VALUE()`](https://dev.mysql.com/doc/refman/8.0/en/window-function-descriptions.html#function_nth-value) | Returns the expression value from the N-th row of the current window. |
| [`NTILE()`](https://dev.mysql.com/doc/refman/8.0/en/window-function-descriptions.html#function_ntile)| Divides a partition into N buckets, assigns the bucket number to each row in the partition, and returns the bucket number of the current row within the partition. |
| [`PERCENT_RANK()`](https://dev.mysql.com/doc/refman/8.0/en/window-function-descriptions.html#function_percent-rank)| Returns the percentage of partition values that are less than the value in the current row. |
| [`RANK()`](https://dev.mysql.com/doc/refman/8.0/en/window-function-descriptions.html#function_rank)| Returns the rank of the current row within the partition. The rank may be with gaps. |
| [`ROW_NUMBER()`](https://dev.mysql.com/doc/refman/8.0/en/window-function-descriptions.html#function_row-number)| Returns the number of the current row in the partition. |