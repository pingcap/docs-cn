---
title: 返回 JSON 值的 JSON 函数
summary: 了解返回 JSON 值的 JSON 函数。
---

# 返回 JSON 值的 JSON 函数

本文介绍返回 JSON 值的 JSON 函数。

## [JSON_DEPTH()](https://dev.mysql.com/doc/refman/8.0/en/json-attribute-functions.html#function_json-depth)

`JSON_DEPTH(json_doc)` 函数返回 JSON 文档的最大深度。

示例：

在下面的示例中，`JSON_DEPTH()` 返回 `3`，因为有三层：

- root (`$`)
- weather (`$.weather`)
- weather current (`$.weather.sunny`)

```sql
SELECT JSON_DEPTH('{"weather": {"current": "sunny"}}');
```

```
+-------------------------------------------------+
| JSON_DEPTH('{"weather": {"current": "sunny"}}') |
+-------------------------------------------------+
|                                               3 |
+-------------------------------------------------+
1 row in set (0.00 sec)
```

## [JSON_LENGTH()](https://dev.mysql.com/doc/refman/8.0/en/json-attribute-functions.html#function_json-length)

`JSON_LENGTH(json_doc [,path])` 函数返回 JSON 文档的长度。如果指定了 `path` 参数，则返回路径中的值的长度。

示例：

在下面的示例中，返回值是 `1`，因为文档根目录下仅有一个元素  `weather`。

```sql
SELECT JSON_LENGTH('{"weather": {"current": "sunny", "tomorrow": "cloudy"}}','$');
```

```
+----------------------------------------------------------------------------+
| JSON_LENGTH('{"weather": {"current": "sunny", "tomorrow": "cloudy"}}','$') |
+----------------------------------------------------------------------------+
|                                                                          1 |
+----------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

在下面的示例中，`$.weather` 包含两个元素 `current` 和`tomorrow`，因此返回值为 `2`。

```sql
SELECT JSON_LENGTH('{"weather": {"current": "sunny", "tomorrow": "cloudy"}}','$.weather');
```

```
+------------------------------------------------------------------------------------+
| JSON_LENGTH('{"weather": {"current": "sunny", "tomorrow": "cloudy"}}','$.weather') |
+------------------------------------------------------------------------------------+
|                                                                                  2 |
+------------------------------------------------------------------------------------+
1 row in set (0.01 sec)
```

## [JSON_TYPE()](https://dev.mysql.com/doc/refman/8.0/en/json-attribute-functions.html#function_json-type)

`JSON_TYPE(json_val)` 函数返回一个字符串，表示 [JSON 值的类型](/data-type-json.md#json-值的类型)。

示例：

```sql
WITH demo AS (
    SELECT 'null' AS 'v'
    UNION SELECT '"foobar"'
    UNION SELECT 'true'
    UNION SELECT '5'
    UNION SELECT '1.14'
    UNION SELECT '[]'
    UNION SELECT '{}'
    UNION SELECT POW(2,63)
)
SELECT v, JSON_TYPE(v) FROM demo ORDER BY 2;
```

```
+----------------------+--------------+
| v                    | JSON_TYPE(v) |
+----------------------+--------------+
| []                   | ARRAY        |
| true                 | BOOLEAN      |
| 1.14                 | DOUBLE       |
| 9.223372036854776e18 | DOUBLE       |
| 5                    | INTEGER      |
| null                 | NULL         |
| {}                   | OBJECT       |
| "foobar"             | STRING       |
+----------------------+--------------+
8 rows in set (0.00 sec)
```

请注意，看起来相同的值可能属于不同的类型，如下例所示。

```sql
SELECT '"2025-06-14"',CAST(CAST('2025-06-14' AS date) AS json);
```

```
+--------------+------------------------------------------+
| "2025-06-14" | CAST(CAST('2025-06-14' AS date) AS json) |
+--------------+------------------------------------------+
| "2025-06-14" | "2025-06-14"                             |
+--------------+------------------------------------------+
1 row in set (0.00 sec)
```

```sql
SELECT JSON_TYPE('"2025-06-14"'),JSON_TYPE(CAST(CAST('2025-06-14' AS date) AS json));
```

```
+---------------------------+-----------------------------------------------------+
| JSON_TYPE('"2025-06-14"') | JSON_TYPE(CAST(CAST('2025-06-14' AS date) AS json)) |
+---------------------------+-----------------------------------------------------+
| STRING                    | DATE                                                |
+---------------------------+-----------------------------------------------------+
1 row in set (0.00 sec)
```

## [JSON_VALID()](https://dev.mysql.com/doc/refman/8.0/en/json-attribute-functions.html#function_json-valid)

`JSON_VALID(str)` 函数检查输入的参数是否为有效的 JSON 格式。该函数对于在将列转换为 `JSON` 类型之前进行检查非常有用。

```sql
SELECT JSON_VALID('{"foo"="bar"}');
```

```
+-----------------------------+
| JSON_VALID('{"foo"="bar"}') |
+-----------------------------+
|                           0 |
+-----------------------------+
1 row in set (0.01 sec)
```

```sql
SELECT JSON_VALID('{"foo": "bar"}');
```

```
+------------------------------+
| JSON_VALID('{"foo": "bar"}') |
+------------------------------+
|                            1 |
+------------------------------+
1 row in set (0.01 sec)
```

## 另请参考

- [JSON 函数](/functions-and-operators/json-functions.md)
- [JSON 数据类型](/data-type-json.md)
