---
title: 创建 JSON 值的 JSON 函数
summary: 了解创建 JSON 值的 JSON 函数。
---

# 创建 JSON 值的 JSON 函数

TiDB 支持使用 MySQL 8.0 中提供的所有[用于创建 JSON 值的 JSON 函数](https://dev.mysql.com/doc/refman/8.0/en/json-creation-functions.html)。

## `JSON_ARRAY()`

`JSON_ARRAY([val[, val] ...])` 函数接受一个值列表（可能为空）作为参数，并返回一个包含这些值的 JSON 数组。

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

## `JSON_OBJECT()`

`JSON_OBJECT([key,val[,key,val]...])` 函数接受一个键值对列表（可能为空）作为参数，并返回一个包含这些键值对的 JSON 对象。

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

## `JSON_QUOTE()`

`JSON_QUOTE(str)` 函数将字符串返回为带引号的 JSON 值。

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

- [JSON 函数](/functions-and-operators/json-functions.md)
- [JSON 数据类型](/data-type-json.md)