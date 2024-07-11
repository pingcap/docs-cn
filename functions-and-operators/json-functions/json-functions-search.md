---
title: 搜索 JSON 值的 JSON 函数
summary: 了解搜索 JSON 值的 JSON 函数。
---

# 搜索 JSON 值的 JSON 函数

本文档介绍用于搜索 JSON 值的 JSON 函数。

## [JSON_CONTAINS()](https://dev.mysql.com/doc/refman/8.0/en/json-search-functions.html#function_json-contains)

通过返回 `1` 或 `0`，`JSON_CONTAINS(json_doc, candidate [,path])` 函数用于确认指定的 JSON 文档 `candidate` 是否包含在目标 JSON 文档中。

示例：

下面示例中，`a` 包含在了目标文档中。

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

下面示例中，`a` 没有包含在目标文档中。

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

下面示例中，`{"foo": "bar"}` 包含在了目标文档中。

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

下面示例中，`"bar"` 没有包含在目标文档的根目录中。

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

下面示例中，`"bar"` 包含在了目标文档的 `$.foo` 属性中。

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

`JSON_CONTAINS_PATH(json_doc,all_or_one,path [,path, ...])` 函数返回 `0` 或 `1`，表示 JSON 文档是否包含指定路径下的数据。

示例：

下面的示例文档中包含 `$.foo`。

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

下面的示例文档中没有包含 `$.bar`。

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

下面的示例文档中包含了 `$.foo` 和 `$.aaa`。

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

`JSON_EXTRACT(json_doc, path[, path] ...)` 函数从 JSON 文档中提取与 `path` 参数匹配的数据。

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

`column->path` 函数返回 `column` 中与 `path` 参数匹配的数据。该函数是 [`JSON_EXTRACT()`](#json_extract) 的别名。

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

`column->>path` 函数去掉 `column` 中与 `path` 参数匹配的数据的引号。它是 `JSON_UNQUOTE(JSON_EXTRACT(doc,path_literal))` 的别名。

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

`JSON_KEYS(json_doc [,path])` 函数以 JSON 数组的形式返回 JSON 对象的顶层键 (key)。如果指定了 `path` 参数，则返回所选路径的顶层键 (key)。

示例：

下面示例返回了 JSON 文档中的两个顶层键。

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

下面示例返回了 JSON 文档的 `$.name` 路径中的顶层键。

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

`JSON_SEARCH(json_doc,one_or_all,str)` 函数会在 JSON 文档中搜索与字符串匹配的一个或所有的匹配项。

示例：

在下面的示例中，搜索 `cc` 的第一个结果，它在 `a` 数组中索引为 2 的位置。

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

现在执行和上个示例类似的操作，但将 `one_or_all` 设置为 `all`。这将获取全部搜索结果，而不仅仅是第一个结果。

```json
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

`str MEMBER OF (json_array)` 函数测试传入的 `str` 值是否是 `json_array` 的元素，如果是则返回 `1`，否则返回 `0`。如果任一参数为 `NULL`，则返回 `NULL`。

```
SELECT '🍍' MEMBER OF ('["🍍","🥥","🥭"]') AS 'Contains pineapple';
```

```
+--------------------+
| Contains pineapple |
+--------------------+
|                  1 |
+--------------------+
1 row in set (0.00 sec)

```

## [JSON_OVERLAPS()](https://dev.mysql.com/doc/refman/8.0/en/json-search-functions.html#function_json-overlaps)

`JSON_OVERLAPS(json_doc, json_doc)` 函数检查两个 JSON 文档是否有重叠部分。如果有重叠，则返回 `1`，如果没有重叠，则返回 `0`。如果任一参数为 `NULL`，则返回 `NULL`。

示例：

下面的示例显示没有重叠，因为数组值的元素数量不一样。

```sql
SELECT JSON_OVERLAPS(
    '{"languages": ["Go","Rust","C#"]}',
    '{"languages": ["Go","Rust"]}'
) AS 'Overlaps';
```

```
+----------+
| Overlaps |
+----------+
|        0 |
+----------+
1 row in set (0.00 sec)
```

下面的示例显示两个 JSON 文档重叠，因为它们完全相同。

```sql
SELECT JSON_OVERLAPS(
    '{"languages": ["Go","Rust","C#"]}',
    '{"languages": ["Go","Rust","C#"]}'
) AS 'Overlaps';
```

```
+----------+
| Overlaps |
+----------+
|        1 |
+----------+
1 row in set (0.00 sec)
```

下面的示例显示存在重叠，而第二个文件有一个额外的属性。

```sql
SELECT JSON_OVERLAPS(
    '{"languages": ["Go","Rust","C#"]}',
    '{"languages": ["Go","Rust","C#"], "arch": ["arm64"]}'
) AS 'Overlaps';
```

```
+----------+
| Overlaps |
+----------+
|        1 |
+----------+
1 row in set (0.00 sec)
```

## 另请参阅

- [JSON 函数](/functions-and-operators/json-functions.md)
- [JSON 数据类型](/data-type-json.md)