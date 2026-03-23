---
title: JSON 效用函数
summary: 了解 JSON 效用函数。
---

# JSON 效用函数

TiDB 支持使用 MySQL 8.0 中提供的所有[JSON 效用函数](https://dev.mysql.com/doc/refman/8.0/en/json-utility-functions.html)。

## `JSON_PRETTY()`

`JSON_PRETTY(json_doc)` 函数用于格式化 JSON 文档。

```sql
SELECT JSON_PRETTY('{"person":{"name":{"first":"John","last":"Doe"},"age":23}}')\G
```

```
*************************** 1. row ***************************
JSON_PRETTY('{"person":{"name":{"first":"John","last":"Doe"},"age":23}}'): {
  "person": {
    "age": 23,
    "name": {
      "first": "John",
      "last": "Doe"
    }
  }
}
1 row in set (0.00 sec)
```

## `JSON_STORAGE_FREE()`

`JSON_STORAGE_FREE(json_doc)` 函数返回 JSON 值在原地更新操作后释放了多少存储空间，以二进制表示。

> **注意：**
>
> 由于 TiDB 的存储架构与 MySQL 不同，因此对于有效的 JSON 值，该函数总是返回 `0`，而且它的实现是为了[与 MySQL 8.0 兼容](/mysql-compatibility.md)。请注意，TiDB 不能进行原地更新。更多信息，请参阅 [RocksDB 的空间占用](/storage-engine/rocksdb-overview.md#rocksdb-的空间占用)。

```sql
SELECT JSON_STORAGE_FREE('{}');
```

```
+-------------------------+
| JSON_STORAGE_FREE('{}') |
+-------------------------+
|                       0 |
+-------------------------+
1 row in set (0.00 sec)
```

## `JSON_STORAGE_SIZE()`

`JSON_STORAGE_SIZE(json_doc)` 函数返回存储 JSON 值所需的大致字节数。由于计算该大小时不考虑 TiKV 对数据的压缩，因此该函数的输出与 MySQL 并不完全兼容。

```sql
SELECT JSON_STORAGE_SIZE('{}');
```

```
+-------------------------+
| JSON_STORAGE_SIZE('{}') |
+-------------------------+
|                       9 |
+-------------------------+
1 row in set (0.00 sec)
```

## 另请参阅

- [JSON 函数](/functions-and-operators/json-functions.md)
- [JSON 数据类型](/data-type-json.md)