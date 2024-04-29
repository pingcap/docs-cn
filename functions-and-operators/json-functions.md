---
title: JSON 函数
---

# JSON 函数

TiDB 支持 MySQL 8.0 中提供的大部分 [JSON 函数](https://dev.mysql.com/doc/refman/8.0/en/json-functions.html)。

## 创建 JSON 值的函数

| 函数                                                              | 功能描述                                                   |
| ------------------------------------------------------------------ | ---------------------------------------------------------- |
| [JSON_ARRAY([val[, val] ...])](https://dev.mysql.com/doc/refman/8.0/en/json-creation-functions.html#function_json-array)                         | 根据一系列元素创建一个 JSON 文档 |
| [JSON_OBJECT(key, val[, key, val] ...)](https://dev.mysql.com/doc/refman/8.0/en/json-creation-functions.html#function_json-object)               | 根据一系列 K/V 对创建一个 JSON 文档 |
| [JSON_QUOTE(string)](https://dev.mysql.com/doc/refman/8.0/en/json-creation-functions.html#function_json-quote)                                   | 返回一个字符串，该字符串为带引号的 JSON 值 |

## 搜索 JSON 值的函数

| 函数                                                        | 功能描述                                                     |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| [JSON_CONTAINS(target, candidate[, path])](https://dev.mysql.com/doc/refman/8.0/en/json-search-functions.html#function_json-contains)    | 通过返回 1 或 0 来表示目标 JSON 文档中是否包含给定的 candidate JSON 文档 |
| [JSON_CONTAINS_PATH(json_doc, one_or_all, path[, path] ...)](https://dev.mysql.com/doc/refman/8.0/en/json-search-functions.html#function_json-contains-path) | 通过返回 0 或 1 来表示一个 JSON 文档在给定路径是否包含数据   |
| [JSON_EXTRACT(json_doc, path[, path] ...)](https://dev.mysql.com/doc/refman/8.0/en/json-search-functions.html#function_json-extract)     | 从 JSON 文档中解出某一路径对应的子文档                       |
| [->](https://dev.mysql.com/doc/refman/8.0/en/json-search-functions.html#operator_json-column-path)                                     | 返回执行路径后面的 JSON 列的值；`JSON_EXTRACT(doc, path_literal)` 的别名 |
| [->>](https://dev.mysql.com/doc/refman/8.0/en/json-search-functions.html#operator_json-inline-path)                            | 返回执行路径后面的 JSON 列的值和转义后的结果； `JSON_UNQUOTE(JSON_EXTRACT(doc, path_literal))` 的别名 |
| [JSON_KEYS(json_doc[, path])](https://dev.mysql.com/doc/refman/8.0/en/json-search-functions.html#function_json-keys)                     | 返回从 JSON 对象的顶级值作为 JSON array 的键，如果给定了路径参数，则从选定路径中获取顶级键 |
| [JSON_SEARCH(json_doc, one_or_all, search_str[, escape_char[, path] ...])](https://dev.mysql.com/doc/refman/8.0/en/json-search-functions.html#function_json-search) | 返回指定字符在 JSON 文档中的路径                             |
| [value MEMBER OF(json_array)](https://dev.mysql.com/doc/refman/8.0/en/json-search-functions.html#operator_member-of) | 如果传入值是 JSON array 中的一个元素，返回 1，否则返回 0 |
| [JSON_OVERLAPS(json_doc1, json_doc2)](https://dev.mysql.com/doc/refman/8.0/en/json-search-functions.html#function_json-overlaps) | 表示两个 JSON 文档中是否包含公共部分。返回 1 表示两个 JSON 文档中包含公共部分，否则返回 0 |

## 修改 JSON 值的函数

| 函数        | 功能描述 |
| --------------------------------- | ----------- |
| [JSON_APPEND(json_doc, path, value)](https://dev.mysql.com/doc/refman/8.0/en/json-modification-functions.html#function_json-append) | `JSON_ARRAY_APPEND` 的别名 |
| [JSON_ARRAY_APPEND(json_doc, path, val[, path, val] ...)](https://dev.mysql.com/doc/refman/8.0/en/json-modification-functions.html#function_json-array-append) | 将值添加到 JSON 文档指定数组的末尾，并返回添加结果 |
| [JSON_ARRAY_INSERT(json_doc, path, val[, path, val] ...)](https://dev.mysql.com/doc/refman/8.0/en/json-modification-functions.html#function_json-array-insert) | 将值插入到 JSON 文档中的指定位置并返回结果 |
| [JSON_INSERT(json_doc, path, val[, path, val] ...)](https://dev.mysql.com/doc/refman/8.0/en/json-modification-functions.html#function_json-insert) | 在 JSON 文档中在某一路径下插入子文档 |
| [JSON_MERGE_PATCH(json_doc, json_doc[, json_doc] ...)](https://dev.mysql.com/doc/refman/8.0/en/json-modification-functions.html#function_json-merge-patch)  | 合并 JSON 文档 |
| [JSON_MERGE_PRESERVE(json_doc, json_doc[, json_doc] ...)](https://dev.mysql.com/doc/refman/8.0/en/json-modification-functions.html#function_json-merge-preserve)  | 将两个或多个 JSON 文档合并成一个文档，并返回合并结果 |
| [JSON_MERGE(json_doc, json_doc[, json_doc] ...)](https://dev.mysql.com/doc/refman/8.0/en/json-modification-functions.html#function_json-merge)  | 已废弃，`JSON_MERGE_PRESERVE` 的别名 |
| [JSON_REMOVE(json_doc, path[, path] ...)](https://dev.mysql.com/doc/refman/8.0/en/json-modification-functions.html#function_json-remove)    | 移除 JSON 文档中某一路径下的子文档 |
| [JSON_REPLACE(json_doc, path, val[, path, val] ...)](https://dev.mysql.com/doc/refman/8.0/en/json-modification-functions.html#function_json-replace) | 替换 JSON 文档中的某一路径下的子文档 |
| [JSON_SET(json_doc, path, val[, path, val] ...)](https://dev.mysql.com/doc/refman/8.0/en/json-modification-functions.html#function_json-set)  | 在 JSON 文档中为某一路径设置子文档 |
| [JSON_UNQUOTE(json_val)](https://dev.mysql.com/doc/refman/8.0/en/json-modification-functions.html#function_json-unquote) |  去掉 JSON 值外面的引号，返回结果为字符串 |

## 返回 JSON 值属性的函数

| 函数        | 功能描述 |
| --------------------------------- | ----------- |
| [JSON_DEPTH(json_doc)](https://dev.mysql.com/doc/refman/8.0/en/json-attribute-functions.html#function_json-depth) | 返回 JSON 文档的最大深度 |
| [JSON_LENGTH(json_doc[, path])](https://dev.mysql.com/doc/refman/8.0/en/json-attribute-functions.html#function_json-length) | 返回 JSON 文档的长度；如果路径参数已定，则返回该路径下值的长度 |
| [JSON_TYPE(json_val)](https://dev.mysql.com/doc/refman/8.0/en/json-attribute-functions.html#function_json-type) | 检查某 JSON 文档内部内容的类型 |
| [JSON_VALID(json_doc)](https://dev.mysql.com/doc/refman/8.0/en/json-attribute-functions.html#function_json-valid) | 检查 JSON 文档内容是否有效；用于将列转换为 JSON 类型之前对该列进行检查 |

## 效用函数

| 函数                     | 功能描述 |
| --------------------------------- | ----------- |
| [JSON_PRETTY(json_doc)](https://dev.mysql.com/doc/refman/8.0/en/json-utility-functions.html#function_json-pretty) |格式化 JSON 文档 |
| [JSON_STORAGE_FREE(json_doc)](https://dev.mysql.com/doc/refman/8.0/en/json-utility-functions.html#function_json-storage-free) | 返回该 JSON 对象的存储空间中空闲的字节数。由于 TiDB 采用与 MySQL 完全不同的存储结构，本函数对合法的 JSON 值总是返回 0，主要用于兼容 MySQL 8.0 |
| [JSON_STORAGE_SIZE(json_doc)](https://dev.mysql.com/doc/refman/8.0/en/json-utility-functions.html#function_json-storage-size) | 返回存储 JSON 值所需的大致字节大小，由于不考虑 TiKV 压缩的字节大小，因此函数的输出与 MySQL 不严格兼容 |

## 聚合函数

| 函数                    | 功能描述 |
| --------------------------------- | ----------- |
| [JSON_ARRAYAGG(key)](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_json-arrayagg) | 提供指定列 key 的聚合 |
| [JSON_OBJECTAGG(key, value)](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_json-objectagg) | 提供给定两列键值对的聚合 |

## 另请参阅

* [JSON Function Reference](https://dev.mysql.com/doc/refman/8.0/en/json-function-reference.html)
* [JSON Data Type](/data-type-json.md)

## 不支持的函数

- `JSON_SCHEMA_VALID()`
- `JSON_SCHEMA_VALIDATION_REPORT()`
- `JSON_TABLE()`
- `JSON_VALUE()`

更多信息，请参考 [#14486](https://github.com/pingcap/tidb/issues/14486)。