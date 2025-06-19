---
title: 修改 JSON 值的 JSON 函数
summary: 了解用于修改 JSON 值的 JSON 函数。
---

# 修改 JSON 值的 JSON 函数

本文档描述用于修改 JSON 值的 JSON 函数。

## [JSON_APPEND()](https://dev.mysql.com/doc/refman/8.0/en/json-modification-functions.html#function_json-append)

[`JSON_ARRAY_APPEND()`](#json_array_append) 的别名。

## [JSON_ARRAY_APPEND()](https://dev.mysql.com/doc/refman/8.0/en/json-modification-functions.html#function_json-array-append)

`JSON_ARRAY_APPEND(json_array, path, value [,path, value] ...)` 函数将值追加到 JSON 文档中指定 `path` 的数组末尾，并返回结果。

此函数接受成对的参数，每对参数包含一个 `path` 和一个 `value`。

示例：

以下示例将一个项目添加到作为 JSON 文档根的数组中。

```sql
SELECT JSON_ARRAY_APPEND('["Car", "Boat", "Train"]', '$', "Airplane") AS "Transport options";
```

```
+--------------------------------------+
| Transport options                    |
+--------------------------------------+
| ["Car", "Boat", "Train", "Airplane"] |
+--------------------------------------+
1 row in set (0.00 sec)
```

以下示例将一个项目添加到指定路径的数组中。

```sql
SELECT JSON_ARRAY_APPEND('{"transport_options": ["Car", "Boat", "Train"]}', '$.transport_options', "Airplane") AS "Transport options";
```

```
+-------------------------------------------------------------+
| Transport options                                           |
+-------------------------------------------------------------+
| {"transport_options": ["Car", "Boat", "Train", "Airplane"]} |
+-------------------------------------------------------------+
1 row in set (0.00 sec)
```

## [JSON_ARRAY_INSERT()](https://dev.mysql.com/doc/refman/8.0/en/json-modification-functions.html#function_json-array-insert)

`JSON_ARRAY_INSERT(json_array, path, value [,path, value] ...)` 函数将 `value` 插入到 `path` 中指定的 `json_array` 位置，并返回结果。

此函数接受成对的参数，每对参数包含一个 `path` 和一个 `value`。

示例：

以下示例在数组的索引 0 位置插入一个值。

```sql
SELECT JSON_ARRAY_INSERT('["Car", "Boat", "Train"]', '$[0]', "Airplane") AS "Transport options";
```

```
+--------------------------------------+
| Transport options                    |
+--------------------------------------+
| ["Airplane", "Car", "Boat", "Train"] |
+--------------------------------------+
1 row in set (0.01 sec)
```

以下示例在数组的索引 1 位置插入一个值。

```sql
SELECT JSON_ARRAY_INSERT('["Car", "Boat", "Train"]', '$[1]', "Airplane") AS "Transport options";
```

```
+--------------------------------------+
| Transport options                    |
+--------------------------------------+
| ["Car", "Airplane", "Boat", "Train"] |
+--------------------------------------+
1 row in set (0.00 sec)
```

## [JSON_INSERT()](https://dev.mysql.com/doc/refman/8.0/en/json-modification-functions.html#function_json-insert)

`JSON_INSERT(json_doc, path, value [,path, value] ...)` 函数将一个或多个值插入到 JSON 文档中并返回结果。

此函数接受成对的参数，每对参数包含一个 `path` 和一个 `value`。

```sql
SELECT JSON_INSERT(
    '{"language": ["Go", "Rust", "C++"]}',
    '$.architecture', 'riscv',
    '$.os', JSON_ARRAY("linux","freebsd")
) AS "Demo";
```

```
+------------------------------------------------------------------------------------------+
| Demo                                                                                     |
+------------------------------------------------------------------------------------------+
| {"architecture": "riscv", "language": ["Go", "Rust", "C++"], "os": ["linux", "freebsd"]} |
+------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

注意，此函数不会覆盖现有属性的值。例如，以下语句看似要覆盖 `"a"` 属性，但实际上并不会这样做。

```sql
SELECT JSON_INSERT('{"a": 61, "b": 62}', '$.a', 41, '$.c', 63);
```

```
+---------------------------------------------------------+
| JSON_INSERT('{"a": 61, "b": 62}', '$.a', 41, '$.c', 63) |
+---------------------------------------------------------+
| {"a": 61, "b": 62, "c": 63}                             |
+---------------------------------------------------------+
1 row in set (0.00 sec)
```

## [JSON_MERGE_PATCH()](https://dev.mysql.com/doc/refman/8.0/en/json-modification-functions.html#function_json-merge-patch)

`JSON_MERGE_PATCH(json_doc, json_doc [,json_doc] ...)` 函数将两个或多个 JSON 文档合并为单个 JSON 文档，不保留重复键的值。对于具有重复键的 `json_doc` 参数，合并结果中仅保留后面指定的 `json_doc` 参数中的值。

示例：

在以下示例中，可以看到 `a` 的值被参数 2 覆盖，而 `c` 作为新属性添加到合并结果中。

```sql
SELECT JSON_MERGE_PATCH(
    '{"a": 1, "b": 2}',
    '{"a": 100}',
    '{"c": 300}'
);
```

```
+-----------------------------------------------------------------+
| JSON_MERGE_PATCH('{"a": 1, "b": 2}','{"a": 100}', '{"c": 300}') |
+-----------------------------------------------------------------+
| {"a": 100, "b": 2, "c": 300}                                    |
+-----------------------------------------------------------------+
1 row in set (0.00 sec)
```

## [JSON_MERGE_PRESERVE()](https://dev.mysql.com/doc/refman/8.0/en/json-modification-functions.html#function_json-merge-preserve)

`JSON_MERGE_PRESERVE(json_doc, json_doc [,json_doc] ...)` 函数在保留与每个键关联的所有值的同时合并两个或多个 JSON 文档，并返回合并结果。

示例：

在以下示例中，可以看到参数 2 的值被追加到 `a` 中，而 `c` 作为新属性添加。

```sql
SELECT JSON_MERGE_PRESERVE('{"a": 1, "b": 2}','{"a": 100}', '{"c": 300}');
```

```
+--------------------------------------------------------------------+
| JSON_MERGE_PRESERVE('{"a": 1, "b": 2}','{"a": 100}', '{"c": 300}') |
+--------------------------------------------------------------------+
| {"a": [1, 100], "b": 2, "c": 300}                                  |
+--------------------------------------------------------------------+
1 row in set (0.00 sec)
```

## [JSON_MERGE()](https://dev.mysql.com/doc/refman/8.0/en/json-modification-functions.html#function_json-merge)

> **警告：**
>
> 此函数已弃用。

[`JSON_MERGE_PRESERVE()`](#json_merge_preserve) 的已弃用别名。

## [JSON_REMOVE()](https://dev.mysql.com/doc/refman/8.0/en/json-modification-functions.html#function_json-remove)

`JSON_REMOVE(json_doc, path [,path] ...)` 函数从 JSON 文档中删除指定 `path` 的数据并返回结果。

示例：

此示例从 JSON 文档中删除 `b` 属性。

```sql
SELECT JSON_REMOVE('{"a": 61, "b": 62, "c": 63}','$.b');
```

```
+--------------------------------------------------+
| JSON_REMOVE('{"a": 61, "b": 62, "c": 63}','$.b') |
+--------------------------------------------------+
| {"a": 61, "c": 63}                               |
+--------------------------------------------------+
1 row in set (0.00 sec)
```

此示例从 JSON 文档中删除 `b` 和 `c` 属性。

```sql
SELECT JSON_REMOVE('{"a": 61, "b": 62, "c": 63}','$.b','$.c');
```

```
+--------------------------------------------------------+
| JSON_REMOVE('{"a": 61, "b": 62, "c": 63}','$.b','$.c') |
+--------------------------------------------------------+
| {"a": 61}                                              |
+--------------------------------------------------------+
1 row in set (0.00 sec)
```

## [JSON_REPLACE()](https://dev.mysql.com/doc/refman/8.0/en/json-modification-functions.html#function_json-replace)

`JSON_REPLACE(json_doc, path, value [, path, value] ...)` 函数替换 JSON 文档中指定路径的值并返回结果。如果指定的路径不存在，则不会将对应路径的值添加到结果中。

此函数接受成对的参数，每对参数包含一个 `path` 和一个 `value`。

示例：

在以下示例中，将 `$.b` 的值从 `62` 更改为 `42`。

```sql
SELECT JSON_REPLACE('{"a": 41, "b": 62}','$.b',42);
```

```
+---------------------------------------------+
| JSON_REPLACE('{"a": 41, "b": 62}','$.b',42) |
+---------------------------------------------+
| {"a": 41, "b": 42}                          |
+---------------------------------------------+
1 row in set (0.00 sec)
```

在以下示例中，将 `$.b` 的值从 `62` 更改为 `42`。此外，该语句尝试将 `$.c` 的值替换为 `43`，但这不起作用，因为 `$.c` 路径在 `{"a": 41, "b": 62}` 中不存在。

```sql
SELECT JSON_REPLACE('{"a": 41, "b": 62}','$.b',42,'$.c',43);
```

```
+------------------------------------------------------+
| JSON_REPLACE('{"a": 41, "b": 62}','$.b',42,'$.c',43) |
+------------------------------------------------------+
| {"a": 41, "b": 42}                                   |
+------------------------------------------------------+
1 row in set (0.00 sec)
```

## [JSON_SET()](https://dev.mysql.com/doc/refman/8.0/en/json-modification-functions.html#function_json-set)

`JSON_SET(json_doc, path, value [,path, value] ...)` 函数在 JSON 文档中插入或更新数据并返回结果。

此函数接受成对的参数，每对参数包含一个 `path` 和一个 `value`。

示例：

在以下示例中，将 `$.version` 从 `1.1` 更新为 `1.2`。

```sql
SELECT JSON_SET('{"version": 1.1, "name": "example"}','$.version',1.2);
```

```
+-----------------------------------------------------------------+
| JSON_SET('{"version": 1.1, "name": "example"}','$.version',1.2) |
+-----------------------------------------------------------------+
| {"name": "example", "version": 1.2}                             |
+-----------------------------------------------------------------+
1 row in set (0.00 sec)
```

在以下示例中，将 `$.version` 从 `1.1` 更新为 `1.2`。并将之前不存在的 `$.branch` 更新为 `main`。

```sql
SELECT JSON_SET('{"version": 1.1, "name": "example"}','$.version',1.2,'$.branch', "main");
```

```
+------------------------------------------------------------------------------------+
| JSON_SET('{"version": 1.1, "name": "example"}','$.version',1.2,'$.branch', "main") |
+------------------------------------------------------------------------------------+
| {"branch": "main", "name": "example", "version": 1.2}                              |
+------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

## [JSON_UNQUOTE()](https://dev.mysql.com/doc/refman/8.0/en/json-modification-functions.html#function_json-unquote)

`JSON_UNQUOTE(json)` 函数取消引用 JSON 值并将结果作为字符串返回。这与 [`JSON_QUOTE()`](/functions-and-operators/json-functions/json-functions-create.md#json_quote) 函数相反。

示例：

在示例中，`"foo"` 被取消引用为 `foo`。

```sql
SELECT JSON_UNQUOTE('"foo"');
```

```
+-----------------------+
| JSON_UNQUOTE('"foo"') |
+-----------------------+
| foo                   |
+-----------------------+
1 row in set (0.00 sec)
```

此函数通常与 [`JSON_EXTRACT()`](/functions-and-operators/json-functions/json-functions-search.md#json_extract) 一起使用。对于以下示例，您可以在第一个示例中提取带引号的 JSON 值，然后在第二个示例中一起使用这两个函数来取消引用该值。请注意，您可以使用 [`->>`](/functions-and-operators/json-functions/json-functions-search.md#--1) 运算符代替 `JSON_UNQUOTE(JSON_EXTRACT(...))`。

```sql
SELECT JSON_EXTRACT('{"database": "TiDB"}', '$.database');
```

```
+----------------------------------------------------+
| JSON_EXTRACT('{"database": "TiDB"}', '$.database') |
+----------------------------------------------------+
| "TiDB"                                             |
+----------------------------------------------------+
1 row in set (0.00 sec)
```

```sql
SELECT JSON_UNQUOTE(JSON_EXTRACT('{"database": "TiDB"}', '$.database'));
```

```
+------------------------------------------------------------------+
| JSON_UNQUOTE(JSON_EXTRACT('{"database": "TiDB"}', '$.database')) |
+------------------------------------------------------------------+
| TiDB                                                             |
+------------------------------------------------------------------+
1 row in set (0.00 sec)
```

## 另请参阅

- [JSON 函数概览](/functions-and-operators/json-functions.md)
- [JSON 数据类型](/data-type-json.md)
