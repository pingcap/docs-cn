---
title: 搜索 JSON 值的 JSON 函数
summary: 了解用于搜索 JSON 值的 JSON 函数。
---

# 搜索 JSON 值的 JSON 函数

本文档描述了用于搜索 JSON 值的 JSON 函数。

## [JSON_CONTAINS()](https://dev.mysql.com/doc/refman/8.0/en/json-search-functions.html#function_json-contains)

`JSON_CONTAINS(json_doc, candidate [,path])` 函数通过返回 `1` 或 `0` 来指示给定的 `candidate` JSON 文档是否包含在目标 JSON 文档中。

示例：

这里 `a` 包含在目标文档中。

```sql
SELECT JSON_CONTAINS('["a","b","c"]','"a"');
```

```
+--------------------------------------+
| JSON_CONTAINS('["a","b","c"]','"a"') |
+--------------------------------------+
|                                    1 |
+--------------------------------------+
1 row in set (0.00 sec)
```

这里 `e` 不包含在目标文档中。

```sql
SELECT JSON_CONTAINS('["a","b","c"]','"e"');
```

```
+--------------------------------------+
| JSON_CONTAINS('["a","b","c"]','"e"') |
+--------------------------------------+
|                                    0 |
+--------------------------------------+
1 row in set (0.00 sec)
```

这里 `{"foo": "bar"}` 包含在目标文档中。

```sql
SELECT JSON_CONTAINS('{"foo": "bar", "aaa": 5}','{"foo": "bar"}');
```

```
+------------------------------------------------------------+
| JSON_CONTAINS('{"foo": "bar", "aaa": 5}','{"foo": "bar"}') |
+------------------------------------------------------------+
|                                                          1 |
+------------------------------------------------------------+
1 row in set (0.00 sec)
```

这里 `"bar"` 不包含在目标文档的根部。

```sql
SELECT JSON_CONTAINS('{"foo": "bar", "aaa": 5}','"bar"');
```

```
+---------------------------------------------------+
| JSON_CONTAINS('{"foo": "bar", "aaa": 5}','"bar"') |
+---------------------------------------------------+
|                                                 0 |
+---------------------------------------------------+
1 row in set (0.00 sec)
```

这里 `"bar"` 包含在目标文档的 `$.foo` 属性中。

```sql
SELECT JSON_CONTAINS('{"foo": "bar", "aaa": 5}','"bar"', '$.foo');
```

```
+------------------------------------------------------------+
| JSON_CONTAINS('{"foo": "bar", "aaa": 5}','"bar"', '$.foo') |
+------------------------------------------------------------+
|                                                          1 |
+------------------------------------------------------------+
1 row in set (0.00 sec)
```

## [JSON_CONTAINS_PATH()](https://dev.mysql.com/doc/refman/8.0/en/json-search-functions.html#function_json-contains-path)

`JSON_CONTAINS_PATH(json_doc, all_or_one, path [,path, ...])` 函数返回 `0` 或 `1` 来指示 JSON 文档在给定路径或多个路径上是否包含数据。

示例：

这里文档包含 `$.foo`。

```sql
SELECT JSON_CONTAINS_PATH('{"foo": "bar", "aaa": 5}','all','$.foo');
```

```
+--------------------------------------------------------------+
| JSON_CONTAINS_PATH('{"foo": "bar", "aaa": 5}','all','$.foo') |
+--------------------------------------------------------------+
|                                                            1 |
+--------------------------------------------------------------+
1 row in set (0.00 sec)
```

这里文档不包含 `$.bar`。

```sql
SELECT JSON_CONTAINS_PATH('{"foo": "bar", "aaa": 5}','all','$.bar');
```

```
+--------------------------------------------------------------+
| JSON_CONTAINS_PATH('{"foo": "bar", "aaa": 5}','all','$.bar') |
+--------------------------------------------------------------+
|                                                            0 |
+--------------------------------------------------------------+
1 row in set (0.00 sec)
```

这里文档同时包含 `$.foo` 和 `$.aaa`。

```sql
SELECT JSON_CONTAINS_PATH('{"foo": "bar", "aaa": 5}','all','$.foo', '$.aaa');
```

```
+-----------------------------------------------------------------------+
| JSON_CONTAINS_PATH('{"foo": "bar", "aaa": 5}','all','$.foo', '$.aaa') |
+-----------------------------------------------------------------------+
|                                                                     1 |
+-----------------------------------------------------------------------+
1 row in set (0.00 sec)
```

## [JSON_EXTRACT()](https://dev.mysql.com/doc/refman/8.0/en/json-search-functions.html#function_json-extract)

`JSON_EXTRACT(json_doc, path[, path] ...)` 函数从 JSON 文档中提取数据，选择由 `path` 参数匹配的文档部分。

```sql
SELECT JSON_EXTRACT('{"foo": "bar", "aaa": 5}', '$.foo');
```

```
+---------------------------------------------------+
| JSON_EXTRACT('{"foo": "bar", "aaa": 5}', '$.foo') |
+---------------------------------------------------+
| "bar"                                             |
+---------------------------------------------------+
1 row in set (0.00 sec)
```

## [->](https://dev.mysql.com/doc/refman/8.0/en/json-search-functions.html#operator_json-column-path)

`column->path` 函数返回 `column` 中匹配 `path` 参数的数据。它是 [`JSON_EXTRACT()`](#json_extract) 的别名。

```sql
SELECT
    j->'$.foo',
    JSON_EXTRACT(j, '$.foo')
FROM (
    SELECT
        '{"foo": "bar", "aaa": 5}' AS j
    ) AS tbl;
```

```
+------------+--------------------------+
| j->'$.foo' | JSON_EXTRACT(j, '$.foo') |
+------------+--------------------------+
| "bar"      | "bar"                    |
+------------+--------------------------+
1 row in set (0.00 sec)
```

## [->>](https://dev.mysql.com/doc/refman/8.0/en/json-search-functions.html#operator_json-inline-path)

`column->>path` 函数对 `column` 中匹配 `path` 参数的数据进行去引号处理。它是 `JSON_UNQUOTE(JSON_EXTRACT(doc, path_literal))` 的别名。

```sql
SELECT
    j->'$.foo',
    JSON_EXTRACT(j, '$.foo')
    j->>'$.foo',
    JSON_UNQUOTE(JSON_EXTRACT(j, '$.foo'))
FROM (
    SELECT
        '{"foo": "bar", "aaa": 5}' AS j
    ) AS tbl;
```

```
+------------+--------------------------+-------------+----------------------------------------+
| j->'$.foo' | JSON_EXTRACT(j, '$.foo') | j->>'$.foo' | JSON_UNQUOTE(JSON_EXTRACT(j, '$.foo')) |
+------------+--------------------------+-------------+----------------------------------------+
| "bar"      | "bar"                    | bar         | bar                                    |
+------------+--------------------------+-------------+----------------------------------------+
1 row in set (0.00 sec)
```

## [JSON_KEYS()](https://dev.mysql.com/doc/refman/8.0/en/json-search-functions.html#function_json-keys)

`JSON_KEYS(json_doc [,path])` 函数以 JSON 数组的形式返回 JSON 对象的顶层键。如果提供了 `path` 参数，它将返回所选路径中的顶层键。

示例：

以下示例返回 JSON 文档中的两个顶层键。

```sql
SELECT JSON_KEYS('{"name": {"first": "John", "last": "Doe"}, "type": "Person"}');
```

```
+---------------------------------------------------------------------------+
| JSON_KEYS('{"name": {"first": "John", "last": "Doe"}, "type": "Person"}') |
+---------------------------------------------------------------------------+
| ["name", "type"]                                                          |
+---------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

以下示例返回 JSON 文档中 `$.name` 路径下的顶层键。

```sql
SELECT JSON_KEYS('{"name": {"first": "John", "last": "Doe"}, "type": "Person"}', '$.name');
```

```
+-------------------------------------------------------------------------------------+
| JSON_KEYS('{"name": {"first": "John", "last": "Doe"}, "type": "Person"}', '$.name') |
+-------------------------------------------------------------------------------------+
| ["first", "last"]                                                                   |
+-------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

## [JSON_SEARCH()](https://dev.mysql.com/doc/refman/8.0/en/json-search-functions.html#function_json-search)

`JSON_SEARCH(json_doc, one_or_all, str)` 函数在 JSON 文档中搜索一个或所有匹配的字符串。

示例：

在以下示例中，你可以搜索 `cc` 的第一个结果，它位于 `a` 数组的索引 2 位置。

```sql
SELECT JSON_SEARCH('{"a": ["aa", "bb", "cc"], "b": ["cc", "dd"]}','one','cc');
```

```
+------------------------------------------------------------------------+
| JSON_SEARCH('{"a": ["aa", "bb", "cc"], "b": ["cc", "dd"]}','one','cc') |
+------------------------------------------------------------------------+
| "$.a[2]"                                                               |
+------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

现在你执行相同的操作，但将 `one_or_all` 设置为 `all` 以获取不仅是第一个结果，而是所有结果。

```sql
SELECT JSON_SEARCH('{"a": ["aa", "bb", "cc"], "b": ["cc", "dd"]}','all','cc');
```

```
+------------------------------------------------------------------------+
| JSON_SEARCH('{"a": ["aa", "bb", "cc"], "b": ["cc", "dd"]}','all','cc') |
+------------------------------------------------------------------------+
| ["$.a[2]", "$.b[0]"]                                                   |
+------------------------------------------------------------------------+
1 row in set (0.01 sec)
```

## [MEMBER OF()](https://dev.mysql.com/doc/refman/8.0/en/json-search-functions.html#operator_member-of)

`str MEMBER OF (json_array)` 函数测试传入的值 `str` 是否是 `json_array` 的元素，如果是则返回 `1`。否则返回 `0`。如果任何参数为 `NULL`，则返回 `NULL`。

```
SELECT '🍍' MEMBER OF ('["🍍","🥥","🥭"]') AS '包含菠萝';
```

```
+----------+
| 包含菠萝 |
+----------+
|        1 |
+----------+
1 row in set (0.00 sec)
```

## [JSON_OVERLAPS()](https://dev.mysql.com/doc/refman/8.0/en/json-search-functions.html#function_json-overlaps)

`JSON_OVERLAPS(json_doc, json_doc)` 函数指示两个 JSON 文档是否有重叠部分。如果有，返回 `1`。如果没有，返回 `0`。如果任何参数为 `NULL`，则返回 `NULL`。

示例：

以下示例显示没有重叠，因为数组值的元素数量不同。

```sql
SELECT JSON_OVERLAPS(
    '{"languages": ["Go","Rust","C#"]}',
    '{"languages": ["Go","Rust"]}'
) AS '重叠';
```

```
+--------+
| 重叠   |
+--------+
|      0 |
+--------+
1 row in set (0.00 sec)
```

以下示例显示两个 JSON 文档重叠，因为它们完全相同。

```sql
SELECT JSON_OVERLAPS(
    '{"languages": ["Go","Rust","C#"]}',
    '{"languages": ["Go","Rust","C#"]}'
) AS '重叠';
```

```
+--------+
| 重叠   |
+--------+
|      1 |
+--------+
1 row in set (0.00 sec)
```

以下示例显示存在重叠，虽然第二个文档有一个额外的属性。

```sql
SELECT JSON_OVERLAPS(
    '{"languages": ["Go","Rust","C#"]}',
    '{"languages": ["Go","Rust","C#"], "arch": ["arm64"]}'
) AS '重叠';
```

```
+--------+
| 重叠   |
+--------+
|      1 |
+--------+
1 row in set (0.00 sec)
```

## 另请参阅

- [JSON 函数概览](/functions-and-operators/json-functions.md)
- [JSON 数据类型](/data-type-json.md)
