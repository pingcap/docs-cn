---
title: 下推到 TiKV 的表达式列表
summary: TiDB 中下推到 TiKV 的表达式列表及相关设置。
category: reference
---

# 下推到 TiKV 的表达式列表

当 TiDB 从 TiKV 中读取数据的时候，TiDB 会尽量下推一些表达式运算到 TiKV 中，从而减少数据传输量以及 TiDB 单一节点的计算压力。本文将介绍 TiDB 已支持下推的表达式，以及如何禁止下推特定表达式。

## 已支持下推的表达式列表

| 表达式分类 | 具体操作 |
| :-------------- | :------------------------------------- |
| [逻辑运算](/dev/reference/sql/functions-and-operators/operators.md#逻辑操作符) | AND (&&), OR (&#124;&#124;), NOT (!) |
| [比较运算](/dev/reference/sql/functions-and-operators/operators.md#比较方法和操作符) | <, <=, =, != (<>), >, >=, [`<=>`](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_equal-to), [`IN()`](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#function_in), IS NULL, LIKE, IS TRUE, IS FALSE, [`COALESCE()`](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#function_coalesce) |
| [数值运算](/dev/reference/sql/functions-and-operators/numeric-functions-and-operators.md) | +, -, *, /, [`ABS()`](https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_abs), [`CEIL()`](https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_ceil), [`CEILING()`](https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_ceiling), [`FLOOR()`](https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_floor) |
| [控制流运算](/dev/reference/sql/functions-and-operators/control-flow-functions.md) | [`CASE`](https://dev.mysql.com/doc/refman/5.7/en/control-flow-functions.html#operator_case), [`IF()`](https://dev.mysql.com/doc/refman/5.7/en/control-flow-functions.html#function_if), [`IFNULL()`](https://dev.mysql.com/doc/refman/5.7/en/control-flow-functions.html#function_ifnull) |
| [JSON运算](/dev/reference/sql/functions-and-operators/json-functions.md) | [JSON_TYPE(json_val)][json_type],<br> [JSON_EXTRACT(json_doc, path[, path] ...)][json_extract],<br> [JSON_UNQUOTE(json_val)][json_unquote],<br> [JSON_OBJECT(key, val[, key, val] ...)][json_object],<br> [JSON_ARRAY([val[, val] ...])][json_array],<br> [JSON_MERGE(json_doc, json_doc[, json_doc] ...)][json_merge],<br> [JSON_SET(json_doc, path, val[, path, val] ...)][json_set],<br> [JSON_INSERT(json_doc, path, val[, path, val] ...)][json_insert],<br> [JSON_REPLACE(json_doc, path, val[, path, val] ...)][json_replace],<br> [JSON_REMOVE(json_doc, path[, path] ...)][json_remove] |
| [日期运算](/dev/reference/sql/functions-and-operators/date-and-time-functions.md) | [`DATE_FORMAT()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_date-format)  |

## 禁止特定表达式下推

当函数的计算过程由于下推而出现异常时，可通过黑名单功能禁止其下推来快速恢复业务。具体而言，你可以将上述支持的函数或运算符名加入黑名单 `mysql.expr_pushdown_blacklist` 中，以禁止特定表达式下推。

### 加入黑名单

执行以下步骤，可将一个或多个函数或运算符加入黑名单：

1. 向 `mysql.expr_pushdown_blacklist` 插入对应的函数名或运算符名。
2. 执行 `admin reload expr_pushdown_blacklist;`。

### 移出黑名单

执行以下步骤，可将一个或多个函数及运算符移出黑名单：

1. 从 `mysql.expr_pushdown_blacklist` 表中删除对应的函数名或运算符名。
2. 执行 `admin reload expr_pushdown_blacklist;`。

### 黑名单用法示例

以下示例首先将运算符 `<` 及 `>` 加入黑名单，然后将运算符 `>` 从黑名单中移出。

黑名单是否生效可以从 `explain` 结果中进行观察（参见[如何理解 `explain` 结果](/dev/reference/performance/understanding-the-query-execution-plan.md)）。

```sql
tidb> create table t(a int);
Query OK, 0 rows affected (0.01 sec)

tidb> explain select * from t where a < 2 and a > 2;
+---------------------+----------+------+------------------------------------------------------------+
| id                  | count    | task | operator info                                              |
+---------------------+----------+------+------------------------------------------------------------+
| TableReader_7       | 0.00     | root | data:Selection_6                                           |
| └─Selection_6       | 0.00     | cop  | gt(test.t.a, 2), lt(test.t.a, 2)                           |
|   └─TableScan_5     | 10000.00 | cop  | table:t, range:[-inf,+inf], keep order:false, stats:pseudo |
+---------------------+----------+------+------------------------------------------------------------+
3 rows in set (0.00 sec)

tidb> insert into mysql.expr_pushdown_blacklist values('<'), ('>');
Query OK, 2 rows affected (0.00 sec)
Records: 2  Duplicates: 0  Warnings: 0

tidb> admin reload expr_pushdown_blacklist;
Query OK, 0 rows affected (0.00 sec)

tidb> explain select * from t where a < 2 and a > 2;
+---------------------+----------+------+------------------------------------------------------------+
| id                  | count    | task | operator info                                              |
+---------------------+----------+------+------------------------------------------------------------+
| Selection_5         | 8000.00  | root | gt(test.t.a, 2), lt(test.t.a, 2)                           |
| └─TableReader_7     | 10000.00 | root | data:TableScan_6                                           |
|   └─TableScan_6     | 10000.00 | cop  | table:t, range:[-inf,+inf], keep order:false, stats:pseudo |
+---------------------+----------+------+------------------------------------------------------------+
3 rows in set (0.00 sec)

tidb> delete from mysql.expr_pushdown_blacklist where name = '>';
Query OK, 1 row affected (0.00 sec)

tidb> admin reload expr_pushdown_blacklist;
Query OK, 0 rows affected (0.00 sec)

tidb> explain select * from t where a < 2 and a > 2;
+-----------------------+----------+------+------------------------------------------------------------+
| id                    | count    | task | operator info                                              |
+-----------------------+----------+------+------------------------------------------------------------+
| Selection_5           | 2666.67  | root | lt(test.t.a, 2)                                            |
| └─TableReader_8       | 3333.33  | root | data:Selection_7                                           |
|   └─Selection_7       | 3333.33  | cop  | gt(test.t.a, 2)                                            |
|     └─TableScan_6     | 10000.00 | cop  | table:t, range:[-inf,+inf], keep order:false, stats:pseudo |
+-----------------------+----------+------+------------------------------------------------------------+
4 rows in set (0.00 sec)
```

> **注意：**
>
> - `admin reload expr_pushdown_blacklist` 只对执行该 SQL 语句的 TiDB server 生效。若需要集群中所有 TiDB server 生效，需要在每台 TiDB server 上执行该 SQL 语句。
> - 表达式黑名单功能在 v3.0.0 及以上版本中支持。
> - 在 v3.0.3 及以下版本中，不支持将某些运算符的原始名称文本（如 ">"、"+" 和 "is null"）加入黑名单中，部分运算符在黑名单中需使用别名。已支持下推的表达式中，别名与原始名不同的运算符见下表（区分大小写）。

| 运算符原始名称 | 运算符别名 |
| :-------- | :---------- |
| < | lt |
| > | gt |
| <= | le |
| >= | ge |
| = | eq |
| != | ne |
| <> | ne |
| <=> | nulleq |
| &#124; | bitor |
| && | bitand|
| &#124;&#124; | or |
| ! | not |
| in | in |
| + | plus|
| - | minus |
| * | mul |
| / | div |
| DIV | intdiv|
| IS NULL | isnull |
| IS TRUE | istrue |
| IS FALSE | isfalse |

[json_extract]: https://dev.mysql.com/doc/refman/5.7/en/json-search-functions.html#function_json-extract
[json_short_extract]: https://dev.mysql.com/doc/refman/5.7/en/json-search-functions.html#operator_json-column-path
[json_short_extract_unquote]: https://dev.mysql.com/doc/refman/5.7/en/json-search-functions.html#operator_json-inline-path
[json_unquote]: https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-unquote
[json_type]: https://dev.mysql.com/doc/refman/5.7/en/json-attribute-functions.html#function_json-type
[json_set]: https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-set
[json_insert]: https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-insert
[json_replace]: https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-replace
[json_remove]: https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-remove
[json_merge]: https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-merge
[json_merge_preserve]: https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-merge-preserve
[json_object]: https://dev.mysql.com/doc/refman/5.7/en/json-creation-functions.html#function_json-object
[json_array]: https://dev.mysql.com/doc/refman/5.7/en/json-creation-functions.html#function_json-array
[json_keys]: https://dev.mysql.com/doc/refman/5.7/en/json-search-functions.html#function_json-keys
[json_length]: https://dev.mysql.com/doc/refman/5.7/en/json-attribute-functions.html#function_json-length
[json_valid]: https://dev.mysql.com/doc/refman/5.7/en/json-attribute-functions.html#function_json-valid
[json_quote]: https://dev.mysql.com/doc/refman/5.7/en/json-creation-functions.html#function_json-quote
[json_contains]: https://dev.mysql.com/doc/refman/5.7/en/json-search-functions.html#function_json-contains
[json_contains_path]: https://dev.mysql.com/doc/refman/5.7/en/json-search-functions.html#function_json-contains-path
[json_arrayagg]: https://dev.mysql.com/doc/refman/5.7/en/group-by-functions.html#function_json-arrayagg
[json_depth]: https://dev.mysql.com/doc/refman/5.7/en/json-attribute-functions.html#function_json-depth
