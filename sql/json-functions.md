---
title: JSON 相关的函数和语法糖
category: user guide
---

# JSON 相关的函数和语法糖

| 函数或语法糖                                                       | 功能描述                                                   |
| ------------------------------------------------------------------ | ---------------------------------------------------------- |
| [JSON_EXTRACT(json_doc, path[, path] ...)][json_extract]          | 从 JSON 文档中解出某一路径对应的子文档                     |
| [JSON_UNQUOTE(json_val)][json_unquote]                             | 去掉 JSON 文档外面的引号                                   |
| [JSON_TYPE(json_val)][json_type]                                   | 检查某 JSON 文档内部内容的类型                             |
| [JSON_SET(json_doc, path, val[, path, val] ...)][json_set]         | 在 JSON 文档中为某一路径设置子文档                         |
| [JSON_INSERT(json_doc, path, val[, path, val] ...)][json_insert]   | 在 JSON 文档中在某一路径下插入子文档                       |
| [JSON_REPLACE(json_doc, path, val[, path, val] ...)][json_replace] | 替换 JSON 文档中的某一路径下的子文档                       |
| [JSON_REMOVE(json_doc, path[, path] ...)][json_remove]             | 移除 JSON 文档中某一路径下的子文档                         |
| [JSON_MERGE(json_doc, json_doc[, json_doc] ...)][json_merge]       | 将多个 JSON 文档合并成一个文档，其类型为数组               |
| [JSON_OBJECT(key, val[, key, val] ...)][json_object]               | 根据一系列 K/V 对创建一个 JSON 文档                        |
| [JSON_ARRAY([val[, val] ...])][json_array]                         | 根据一系列元素创建一个 JSON 文档                           |
| ->                                                                 | JSON_EXTRACT(doc, path_literal) 的语法糖                   |
| ->>                                                                | JSON_UNQUOTE(JSONJSON_EXTRACT(doc, path_literal)) 的语法糖 |

[json_extract]: https://dev.mysql.com/doc/refman/5.7/en/json-search-functions.html#function_json-extract
[json_unquote]: https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-unquote
[json_type]: https://dev.mysql.com/doc/refman/5.7/en/json-attribute-functions.html#function_json-type
[json_set]: https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-set
[json_insert]: https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-insert
[json_replace]: https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-replace
[json_remove]: https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-remove
[json_merge]: https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-merge
[json_object]: https://dev.mysql.com/doc/refman/5.7/en/json-creation-functions.html#function_json-object
[json_array]: https://dev.mysql.com/doc/refman/5.7/en/json-creation-functions.html#function_json-array
