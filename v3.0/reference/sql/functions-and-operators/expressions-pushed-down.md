---
title: 下推到 TiKV 的表达式列表
category: reference
aliases: ['/docs-cn/sql/expressions-pushed-down-2-TiKV/']
---

# 下推到 TiKV 的表达式列表

| 表达式分类 | 具体操作 |
| -------------- | ------------------------------------- |
| [逻辑运算](/reference/sql/functions-and-operators/operators.md) | AND (&&), OR (&#124;&#124;), NOT (!) |
| [比较运算](/reference/sql/functions-and-operators/operators.md#比较方法和操作符) | <, <=, =, != (<>), >, >=, [`<=>`](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_equal-to), [`IN()`](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#function_in), IS NULL, LIKE, IS TRUE, IS FALSE, [`COALESCE()`](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#function_coalesce) |
| [数值运算](/reference/sql/functions-and-operators/numeric-functions-and-operators.md) | +, -, *, /, [`ABS()`](https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_abs), [`CEIL()`](https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_ceil), [`CEILING()`](https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_ceiling), [`FLOOR()`](https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_floor) |
| [控制流运算](/reference/sql/functions-and-operators/control-flow-functions.md) | [`CASE`](https://dev.mysql.com/doc/refman/5.7/en/control-flow-functions.html#operator_case), [`IF()`](https://dev.mysql.com/doc/refman/5.7/en/control-flow-functions.html#function_if), [`IFNULL()`](https://dev.mysql.com/doc/refman/5.7/en/control-flow-functions.html#function_ifnull) |
| [JSON运算](/reference/sql/functions-and-operators/json-functions.md) | [JSON_TYPE(json_val)][json_type],<br> [JSON_EXTRACT(json_doc, path[, path] ...)][json_extract],<br> [JSON_UNQUOTE(json_val)][json_unquote],<br> [JSON_OBJECT(key, val[, key, val] ...)][json_object],<br> [JSON_ARRAY([val[, val] ...])][json_array],<br> [JSON_MERGE(json_doc, json_doc[, json_doc] ...)][json_merge], [JSON_SET(json_doc, path, val[, path, val] ...)][json_set], [JSON_INSERT(json_doc, path, val[, path, val] ...)][json_insert], [JSON_REPLACE(json_doc, path, val[, path, val] ...)][json_replace], [JSON_REMOVE(json_doc, path[, path] ...)][json_remove] |
| [日期运算](/reference/sql/functions-and-operators/date-and-time-functions.md) | [`DATE_FORMAT()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_date-format)  |

注意：上述所支持下推的表达式可以被拉入黑名单mysql.expr_pushdown_blacklist中。

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
