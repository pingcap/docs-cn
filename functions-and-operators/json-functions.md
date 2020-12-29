---
title: JSON 函数
---

# JSON 函数

> **警告：**
>
> 当前该功能为实验特性，不建议在生产环境中使用。

TiDB 支持 MySQL 5.7 GA 版本发布的大多数 JSON 函数。MySQL 5.7 发布后，又增加了更多 JSON 函数，TiDB 并未支持所有这些函数（参见[未支持的函数](#未支持的函数)）。

## 创建 JSON 值的函数

| 函数                                                              | 功能描述                                                   |
| ------------------------------------------------------------------ | ---------------------------------------------------------- |
| [JSON_ARRAY([val[, val] ...])][json_array]                         | 根据一系列元素创建一个 JSON 文档 |
| [JSON_OBJECT(key, val[, key, val] ...)][json_object]               | 根据一系列 K/V 对创建一个 JSON 文档 |
| [JSON_QUOTE(string)][json_quote]                                   | 返回一个字符串，该字符串为带引号的 JSON 值 |

## 搜索 JSON 值的函数

| 函数                                                        | 功能描述                                                     |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| [JSON_CONTAINS(target, candidate[, path])][json_contains]    | 通过返回 1 或 0 来表示目标 JSON 文档中是否包含给定的 candidate JSON 文档 |
| [JSON_CONTAINS_PATH(json_doc, one_or_all, path[, path] ...)][json_contains_path] | 通过返回 0 或 1 来表示一个 JSON 文档在给定路径是否包含数据   |
| [JSON_EXTRACT(json_doc, path[, path] ...)][json_extract]     | 从 JSON 文档中解出某一路径对应的子文档                       |
| [->][json_short_extract]                                     | 返回执行路径后面的 JSON 列的值；`JSON_EXTRACT(doc, path_literal)` 的别名 |
| [->>][json_short_extract_unquote]                            | 返回执行路径后面的 JSON 列的值和转义后的结果； `JSON_UNQUOTE(JSON_EXTRACT(doc, path_literal))` 的别名 |
| [JSON_KEYS(json_doc[, path])][json_keys]                     | 返回从 JSON 对象的顶级值作为 JSON array 的键，如果给定了路径参数，则从选定路径中获取顶级键 |
| [JSON_SEARCH(json_doc, one_or_all, search_str[, escape_char[, path] ...])][json_search] | 返回指定字符在 JSON 文档中的路径                             |

## 修改 JSON 值的函数

| 函数        | 功能描述 |
| --------------------------------- | ----------- |
| [JSON_APPEND(json_doc, path, value)][json_append] | `JSON_ARRAY_APPEND` 的别名 |
| [JSON_ARRAY_APPEND(json_doc, path, value)][json_array_append] | 将值追加到指定路径的 JSON 数组的末尾 |
| [JSON_ARRAY_INSERT(json_doc, path, val[, path, val] ...)][json_array_insert] | 将数组插入 JSON 文档，并返回修改后的文档 |
| [JSON_INSERT(json_doc, path, val[, path, val] ...)][json_insert] | 在 JSON 文档中在某一路径下插入子文档 |
| [JSON_MERGE(json_doc, json_doc[, json_doc] ...)][json_merge]  | 已废弃的 `JSON_MERGE_PRESERVE` 别名 |
| [JSON_MERGE_PRESERVE(json_doc, json_doc[, json_doc] ...)][json_merge_preserve]  | 将两个或多个 JSON 文档合并成一个文档，并返回合并结果 |
| [JSON_REMOVE(json_doc, path[, path] ...)][json_remove]    | 移除 JSON 文档中某一路径下的子文档 |
| [JSON_REPLACE(json_doc, path, val[, path, val] ...)][json_replace] | 替换 JSON 文档中的某一路径下的子文档 |
| [JSON_SET(json_doc, path, val[, path, val] ...)][json_set]  | 在 JSON 文档中为某一路径设置子文档 |
| [JSON_UNQUOTE(json_val)][json_unquote] |  去掉 JSON 值外面的引号，返回结果为字符串 |
| [JSON_ARRAY_APPEND(json_doc, path, val[, path, val] ...)][json_array_append] | 将值添加到 JSON 文档指定数组的末尾，并返回添加结果 |
| [JSON_ARRAY_INSERT(json_doc, path, val[, path, val] ...)][json_array_insert] | 将值插入到 JSON 文档的指定位置，并返回插入结果 |

## 返回 JSON 值属性的函数

| 函数        | 功能描述 |
| --------------------------------- | ----------- |
| [JSON_DEPTH(json_doc)][json_depth] | 返回 JSON 文档的最大深度 |
| [JSON_LENGTH(json_doc[, path])][json_length] | 返回 JSON 文档的长度；如果路径参数已定，则返回该路径下值的长度 |
| [JSON_TYPE(json_val)][json_type] | 检查某 JSON 文档内部内容的类型 |
| [JSON_VALID(json_doc)][json_valid] | 检查 JSON 文档内容是否有效；用于将列转换为 JSON 类型之前对该列进行检查 |

## 效用函数

| 函数                     | 功能描述 |
| --------------------------------- | ----------- |
| [JSON_STORAGE_SIZE(json_doc)][json_storage_size] | 返回存储 JSON 值所需的大致字节大小，由于不考虑 TiKV 压缩的字节大小，因此函数的输出与 MySQL 不严格兼容 |

## 聚合函数

| 函数                    | 功能描述 |
| --------------------------------- | ----------- |
| [JSON_OBJECTAGG(key, value)][json_objectagg] | 提供给定键的值的聚合 |

## 未支持的函数

TiDB 暂未支持以下 JSON 函数。相关进展参见 [TiDB #7546](https://github.com/pingcap/tidb/issues/7546):

* `JSON_MERGE_PATCH`
* `JSON_PRETTY`
* `JSON_ARRAYAGG`

## 另请参阅

* [JSON Function Reference](https://dev.mysql.com/doc/refman/5.7/en/json-function-reference.html)
* [JSON Data Type](/data-type-json.md)

[json_extract]: https://dev.mysql.com/doc/refman/5.7/en/json-search-functions.html#function_json-extract
[json_short_extract]: https://dev.mysql.com/doc/refman/5.7/en/json-search-functions.html#operator_json-column-path
[json_short_extract_unquote]: https://dev.mysql.com/doc/refman/5.7/en/json-search-functions.html#operator_json-inline-path
[json_unquote]: https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-unquote
[json_type]: https://dev.mysql.com/doc/refman/5.7/en/json-attribute-functions.html#function_json-type
[json_set]: https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-set
[json_insert]: https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-insert
[json_replace]: https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-replace
[json_remove]: https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-remove
[json_merge]: https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-merge
[json_merge_preserve]: https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-merge-preserve
[json_object]: https://dev.mysql.com/doc/refman/5.7/en/json-creation-functions.html#function_json-object
[json_array]: https://dev.mysql.com/doc/refman/5.7/en/json-creation-functions.html#function_json-array
[json_keys]: https://dev.mysql.com/doc/refman/5.7/en/json-search-functions.html#function_json-keys
[json_length]: https://dev.mysql.com/doc/refman/5.7/en/json-attribute-functions.html#function_json-length
[json_valid]: https://dev.mysql.com/doc/refman/5.7/en/json-attribute-functions.html#function_json-valid
[json_quote]: https://dev.mysql.com/doc/refman/5.7/en/json-creation-functions.html#function_json-quote
[json_contains]: https://dev.mysql.com/doc/refman/5.7/en/json-search-functions.html#function_json-contains
[json_contains_path]: https://dev.mysql.com/doc/refman/5.7/en/json-search-functions.html#function_json-contains-path
[json_arrayagg]: https://dev.mysql.com/doc/refman/5.7/en/group-by-functions.html#function_json-arrayagg
[json_depth]: https://dev.mysql.com/doc/refman/5.7/en/json-attribute-functions.html#function_json-depth
[json_search]: https://dev.mysql.com/doc/refman/5.7/en/json-search-functions.html#function_json-search
[json_append]: https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-append
[json_array_append]: https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-array-append
[json_array_insert]: https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-array-insert
