---
title: 创建 JSON 值的 JSON 函数
summary: 了解用于创建 JSON 值的 JSON 函数。
---

# 创建 JSON 值的 JSON 函数

本文档描述了用于创建 JSON 值的 JSON 函数。

## [JSON_ARRAY()](https://dev.mysql.com/doc/refman/8.0/en/json-creation-functions.html#function_json-array)

`JSON_ARRAY([val[, val] ...])` 函数计算一个（可能为空的）值列表，并返回包含这些值的 JSON 数组。

```sql
SELECT JSON_ARRAY(1,2,3,4,5), JSON_ARRAY("foo", "bar");
```

```
+-----------------------+--------------------------+
| JSON_ARRAY(1,2,3,4,5) | JSON_ARRAY("foo", "bar") |
+-----------------------+--------------------------+
| [1, 2, 3, 4, 5]       | ["foo", "bar"]           |
+-----------------------+--------------------------+
1 row in set (0.00 sec)
```

## [JSON_OBJECT()](https://dev.mysql.com/doc/refman/8.0/en/json-creation-functions.html#function_json-object)

`JSON_OBJECT([key, val[, key, val] ...])` 函数计算一个（可能为空的）键值对列表，并返回包含这些键值对的 JSON 对象。

```sql
SELECT JSON_OBJECT("database", "TiDB", "distributed", TRUE);
```

```
+------------------------------------------------------+
| JSON_OBJECT("database", "TiDB", "distributed", TRUE) |
+------------------------------------------------------+
| {"database": "TiDB", "distributed": true}            |
+------------------------------------------------------+
1 row in set (0.00 sec)
```

## [JSON_QUOTE()](https://dev.mysql.com/doc/refman/8.0/en/json-creation-functions.html#function_json-quote)

`JSON_QUOTE(str)` 函数将字符串作为带引号的 JSON 值返回。

```sql
SELECT JSON_QUOTE('The name is "O\'Neil"');
```

```
+-------------------------------------+
| JSON_QUOTE('The name is "O\'Neil"') |
+-------------------------------------+
| "The name is \"O'Neil\""            |
+-------------------------------------+
1 row in set (0.00 sec)
```

## 另请参阅

- [JSON 函数概览](/functions-and-operators/json-functions.md)
- [JSON 数据类型](/data-type-json.md)
