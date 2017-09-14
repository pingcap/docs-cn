---
title: TiDB 用户文档
category: user guide
---

# JSON 相关的函数和语法糖

| 函数名或语法糖               | 示例                           | 功能描述                                               |
| ---------------------------- | ------------------------------ | ------------------------------------                   |
| [JSON_EXTRACT][json_extract] | JSON_EXTRACT(doc, path)        | 从JSON文档中解出某一路径对应的子文档                   |
| [JSON_UNQUOTE][json_unquote] | JSON_UNQUOTE(doc)              | 去掉JSON文档外面的引号                                 |
| [JSON_TYPE][json_type]       | JSON_TYPE(doc)                 | 检查某JSON文档内部内容的类型                           |
| [JSON_SET][json_set]         | JSON_SET(doc, path, value)     | 在JSON文档中为某一路径设置子文档                       |
| [JSON_INSERT][json_insert]   | JSON_INSERT(doc, path, value)  | 在JSON文档中在某一路径下插入子文档                     |
| [JSON_REPLACE][json_replace] | JSON_REPLACE(doc, path, value) | 替换JSON文档中的某一路径下的子文档                     |
| [JSON_REMOVE][json_remove]   | JSON_REMOVE(doc, path)         | 移除JSON文档中某一路径下的子文档                       |
| [JSON_MERGE][json_merge]     | JSON_MERGE(doc1, doc2, doc3)   | 将多个JSON文档合并成一个文档，其类型为数组             |
| [JSON_OBJECT][json_object]   | JSON_OBJECT(k1, v1, k2, v2)    | 根据一系列K/V对创建一个JSON文档                        |
| [JSON_ARRAY][json_array]     | JSON_ARRAY(doc1, doc2, doc3)   | 根据一系列元素创建一个JSON文档                         |
| ->                           | doc->'$.a[3]'                  | JSON_EXTRACT(doc, '$.a[3]') 的语法糖                   |
| ->>                          | doc->>'$.a[3]'                 | JSON_UNQUOTE(JSONJSON_EXTRACT(doc, '$.a[3]')) 的语法糖 |

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
