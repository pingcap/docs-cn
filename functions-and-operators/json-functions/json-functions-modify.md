---
title: 修改 JSON 值的 JSON 函数
summary: 了解修改 JSON 值的 JSON 函数。
---

# 修改 JSON 值的 JSON 函数

本文档介绍用于修改 JSON 值的 JSON 函数。

## [JSON_APPEND()](https://dev.mysql.com/doc/refman/8.0/en/json-modification-functions.html#function_json-append)

该函数为 [`JSON_ARRAY_APPEND()`](#json_array_append) 的别名。

## [JSON_ARRAY_APPEND()](https://dev.mysql.com/doc/refman/8.0/en/json-modification-functions.html#function_json-array-append)

`JSON_ARRAY_APPEND(json_array, path, value [,path, value] ...)` 函数将 `value` 插入 `path` 中指定的 `json_array` 数组的末尾，并返回结果。

该函数可接受成对的 `path` 和 `value` 参数。

示例：

下面示例向 JSON 文档根目录的数组添加了一个元素。

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

下面的示例向指定路径下的数组添加了一个元素。

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

`JSON_ARRAY_INSERT(json_array, path, value [,path, value] ...)` 函数将 `value` 插入 `path` 中 `json_array` 的指定位置，并返回结果。

该函数可接受成对的 `path` 和 `value` 参数。

示例：

下面的示例在数组中索引为 0 的位置插入了一个值。

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

下面的示例在数组中索引为 1 的位置插入了一个值。

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

`JSON_INSERT(json_doc,path,value[,path,value] ...)` 函数将一个或多个值插入到 JSON 文档，并返回结果。

该函数可接受成对的 `path` 和 `value` 参数。

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

请注意，该函数不会覆盖现有属性。例如，以下语句看起来会覆盖 `"a"` 属性现有的值，但实际上并不会。

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

`JSON_MERGE_PATCH(json_doc, json_doc [,json_doc] ...)` 将两个或多个 JSON 文档合并为一个 JSON 文档，但不保留重复键的值。如果其中某些 `json_doc` 参数包含重复的键，合并后的结果只保留后面指定的那个 `json_doc` 参数中的值。

示例：

在下面的示例中，可以看到合并结果中 `a` 的值被第二个参数覆盖，而 `c` 被添加为一个新属性。

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

`JSON_MERGE_PRESERVE(json_doc, json_doc [,json_doc] ...)` 函数通过保留所有键值的方式合并两个或多个 JSON 文档，并返回合并结果。

示例：

在下面的示例中，可以看到第二个参数的值被附加到了 `a` 中，并且 `c` 被添加为一个新属性。

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
> 该函数已废弃。

该函数为 [`JSON_MERGE_PRESERVE()`](#json_merge_preserve) 已废弃的别名。

## [JSON_REMOVE()](https://dev.mysql.com/doc/refman/8.0/en/json-modification-functions.html#function_json-remove)

`JSON_REMOVE(json_doc,path [,path] ...)` 函数从 JSON 文档中删除指定 `path` 的数据并返回结果。

示例：

下面示例删除了 JSON 文档中的 `b` 属性。

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

下面示例删除了 JSON 文档中的 `b` 和 `c` 属性。

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

`JSON_REPLACE(json_doc,path,value[,path,value]...)` 函数替换 JSON 文档中的现有的值并返回结果。如果指定的路径不存在，该路径对应的值不会添加到结果中。

该函数可接受成对的 `path` 和 `value` 参数。

示例：

下面的示例将 `$.b` 的值从 `62` 替换为 `42`。

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

下面的示例将 `$.b` 的值从 `62` 替换为 `42`。此外，该语句试图用 `43` 替换 `$.c` 中的值，但不会替换成功，因为在 `{"a"： 41, "b": 62}` 中 `$.c` 路径不存在。

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

`JSON_SET(json_doc,path,value[,path,value] ...)` 函数在 JSON 文档中插入或更新数据，并返回结果。

该函数可接受成对的 `path` 和 `value` 参数。

示例：

下面的示例将 `$.version` 从 `1.1` 更新为 `1.2`。

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

下面的示例将 `$.version` 从 `1.1` 更新为 `1.2`，并将之前不存在的 `$.branch` 更新为 `main`。

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

`JSON_UNQUOTE(json)` 函数去掉 JSON 值的引号，并以字符串形式返回结果。该函数与 [`JSON_QUOTE()`](/functions-and-operators/json-functions/json-functions-create.md#json_quote) 函数作用相反。

示例：

下面示例将 `"foo"` 去掉引号，变成 `foo`。

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

该函数通常与 [`JSON_EXTRACT()`](/functions-and-operators/json-functions/json-functions-search.md#json_extract) 一起使用。在下面的示例中，第一个示例提取带引号的 JSON 值，第二个示例通过将两个函数结合使用去掉提取值的引号。请注意，你可以使用 [`->>`](/functions-and-operators/json-functions/json-functions-search.md#--1) 操作符来代替 `JSON_UNQUOTE(JSON_EXTRACT(...))`。

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

- [JSON 函数](/functions-and-operators/json-functions.md)
- [JSON 数据类型](/data-type-json.md)