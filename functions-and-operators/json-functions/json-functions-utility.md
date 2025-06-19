---
title: JSON 实用函数
summary: 了解 JSON 实用函数。
---

# JSON 实用函数

本文档描述了 JSON 实用函数。

## [JSON_PRETTY()](https://dev.mysql.com/doc/refman/8.0/en/json-utility-functions.html#function_json-pretty)

`JSON_PRETTY(json_doc)` 函数对 JSON 文档进行美化格式化。

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

## [JSON_STORAGE_FREE()](https://dev.mysql.com/doc/refman/8.0/en/json-utility-functions.html#function_json-storage-free)

`JSON_STORAGE_FREE(json_doc)` 函数返回 JSON 值在原地更新后其二进制表示中释放的存储空间大小。

> **注意：**
>
> 由于 TiDB 的存储架构与 MySQL 不同，此函数对于有效的 JSON 值始终返回 `0`，它的实现是为了[与 MySQL 8.0 兼容](/mysql-compatibility.md)。请注意，TiDB 不进行原地更新。更多信息，请参见 [RocksDB 空间使用](/storage-engine/rocksdb-overview.md#rocksdb-space-usage)。

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

## [JSON_STORAGE_SIZE()](https://dev.mysql.com/doc/refman/8.0/en/json-utility-functions.html#function_json-storage-size)

`JSON_STORAGE_SIZE(json_doc)` 函数返回存储 JSON 值所需的大致字节数。由于此大小没有考虑 TiKV 使用压缩的情况，因此该函数的输出与 MySQL 并不严格兼容。

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

- [JSON 函数概览](/functions-and-operators/json-functions.md)
- [JSON 数据类型](/data-type-json.md)
