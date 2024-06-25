---
title: 创建 JSON 值的 JSON 函数
summary: 了解创建 JSON 值的 JSON 函数。
---

# 创建 JSON 值的 JSON 函数

本文档介绍了创建 JSON 值的 JSON 函数。

## [JSON_ARRAY()](https://dev.mysql.com/doc/refman/8.0/en/json-creation-functions.html#function_json-array)

`JSON_ARRAY([val[, val] ...])` 函数对一个值列表（可能为空）进行求值，并返回一个包含这些值的 JSON 数组。

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

`JSON_OBJECT([key,val[,key,val]...])` 函数对键值对（可能为空）列表进行评估，并返回一个包含这些键值对的 JSON 对象。

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