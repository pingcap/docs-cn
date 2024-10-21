---
title: JSON 函数
summary: TiDB 支持 MySQL 8.0 中提供的大部分 JSON 函数。
---

# JSON 函数

你可以使用 JSON 函数处理 [JSON 类型](/data-type-json.md)的数据。

## 创建 JSON 值的函数

| 函数                                                              | 功能描述                                                   |
| ------------------------------------------------------------------ | ---------------------------------------------------------- |
| [JSON_ARRAY()](/functions-and-operators/json-functions/json-functions-create.md#json_array)   | 根据一系列元素（也可以为空）创建一个 JSON 数组 |
| [JSON_OBJECT()](/functions-and-operators/json-functions/json-functions-create.md#json_object) | 根据一系列包含 (key, value) 键值对的元素（也可以为空）创建一个 JSON 对象 |
| [JSON_QUOTE()](/functions-and-operators/json-functions/json-functions-create.md#json_quote)   | 返回一个字符串，该字符串为带引号的 JSON 值 |

## 搜索 JSON 值的函数

| 函数                                                        | 功能描述                                                     |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| [JSON_CONTAINS()](/functions-and-operators/json-functions/json-functions-search.md#json_contains)    | 通过返回 1 或 0 来表示目标 JSON 文档中是否包含给定的 candidate JSON 文档 |
| [JSON_CONTAINS_PATH()](/functions-and-operators/json-functions/json-functions-search.md#json_contains_path)  | 通过返回 0 或 1 来表示一个 JSON 文档在给定路径是否包含数据   |
| [JSON_EXTRACT()](/functions-and-operators/json-functions/json-functions-search.md#json_extract)   | 从 JSON 文档中解出某一路径对应的子文档                       |
| [->](/functions-and-operators/json-functions/json-functions-search.md#-)           | 返回执行路径后面的 JSON 列的值；`JSON_EXTRACT(doc, path_literal)` 的别名 |
| [->>](/functions-and-operators/json-functions/json-functions-search.md#--1)       | 返回执行路径后面的 JSON 列的值和转义后的结果； `JSON_UNQUOTE(JSON_EXTRACT(doc, path_literal))` 的别名 |
| [JSON_KEYS()](/functions-and-operators/json-functions/json-functions-search.md#json_keys)        | 返回从 JSON 对象的顶级值作为 JSON array 的键，如果给定了路径参数，则从选定路径中获取顶级键 |
| [JSON_SEARCH()](/functions-and-operators/json-functions/json-functions-search.md#json_search)    | 在 JSON 文档中搜索字符串的一个或所有匹配项                             |
| [MEMBER OF()](/functions-and-operators/json-functions/json-functions-search.md#member-of)         | 如果传入值是 JSON array 中的一个元素，返回 1，否则返回 0 |
| [JSON_OVERLAPS()](/functions-and-operators/json-functions/json-functions-search.md#json_overlaps) | 表示两个 JSON 文档中是否包含公共部分。返回 1 表示两个 JSON 文档中包含公共部分，否则返回 0 |

## 修改 JSON 值的函数

| 函数        | 功能描述 |
| --------------------------------- | ----------- |
| [JSON_APPEND()](/functions-and-operators/json-functions/json-functions-modify.md#json_append)  | `JSON_ARRAY_APPEND()` 的别名 |
| [JSON_ARRAY_APPEND()](/functions-and-operators/json-functions/json-functions-modify.md#json_array_append) | 将值添加到 JSON 文档指定数组的末尾，并返回添加结果 |
| [JSON_ARRAY_INSERT()](/functions-and-operators/json-functions/json-functions-modify.md#json_array_insert)  | 将值插入到 JSON 文档中的指定位置并返回结果 |
| [JSON_INSERT()](/functions-and-operators/json-functions/json-functions-modify.md#json_insert) | 在 JSON 文档中在某一路径下插入子文档 |
| [JSON_MERGE_PATCH()](/functions-and-operators/json-functions/json-functions-modify.md#json_merge_patch) | 将两个或多个 JSON 文档合并为一个 JSON 文档，但不保留重复键的值 |
| [JSON_MERGE_PRESERVE()](/functions-and-operators/json-functions/json-functions-modify.md#json_merge_preserve) | 通过保留所有值的方式将两个或多个 JSON 文档合并成一个文档，并返回合并结果 |
| [JSON_MERGE()](/functions-and-operators/json-functions/json-functions-modify.md#json_merge)  | 已废弃，`JSON_MERGE_PRESERVE()` 的别名 |
| [JSON_REMOVE()](/functions-and-operators/json-functions/json-functions-modify.md#json_remove)    | 移除 JSON 文档中某一路径下的子文档，并返回结果 |
| [JSON_REPLACE()](/functions-and-operators/json-functions/json-functions-modify.md#json_replace)| 替换 JSON 文档中的某一路径下的子文档，并返回结果 |
| [JSON_SET()](/functions-and-operators/json-functions/json-functions-modify.md#json_set)  | 在 JSON 文档中为某一路径设置子文档，并返回结果 |
| [JSON_UNQUOTE()](/functions-and-operators/json-functions/json-functions-modify.md#json_unquote) |  去掉 JSON 值外面的引号，返回结果为字符串 |

## 返回 JSON 值属性的函数

| 函数        | 功能描述 |
| --------------------------------- | ----------- |
| [JSON_DEPTH()](/functions-and-operators/json-functions/json-functions-return.md#json_depth) | 返回 JSON 文档的最大深度 |
| [JSON_LENGTH()](/functions-and-operators/json-functions/json-functions-return.md#json_length) | 返回 JSON 文档的长度；如果路径参数已定，则返回该路径下值的长度 |
| [JSON_TYPE()](/functions-and-operators/json-functions/json-functions-return.md#json_type)  | 检查某 JSON 文档内部内容的类型 |
| [JSON_VALID()](/functions-and-operators/json-functions/json-functions-return.md#json_valid)  | 检查 json\_doc 是否为有效的 JSON 文档  |

## 效用函数

| 函数                     | 功能描述 |
| --------------------------------- | ----------- |
| [JSON_PRETTY()](/functions-and-operators/json-functions/json-functions-utility.md#json_pretty)  |格式化 JSON 文档 |
| [JSON_STORAGE_FREE()](/functions-and-operators/json-functions/json-functions-utility.md#json_storage_free) | 返回 JSON 值在原地更新操作后释放了多少存储空间，以二进制表示。 |
| [JSON_STORAGE_SIZE()](/functions-and-operators/json-functions/json-functions-utility.md#json_storage_size) | 返回存储 JSON 值所需的大致字节大小，由于不考虑 TiKV 压缩的字节大小，因此函数的输出与 MySQL 不严格兼容 |

## 聚合函数

| 函数                    | 功能描述 |
| --------------------------------- | ----------- |
| [JSON_ARRAYAGG()](/functions-and-operators/json-functions/json-functions-aggregate.md#json_arrayagg)  | 提供指定列 key 的聚合 |
| [JSON_OBJECTAGG()](/functions-and-operators/json-functions/json-functions-aggregate.md#json_objectagg) | 提供给定两列键值对的聚合 |

## JSONPath

许多 JSON 函数都使用 [JSONPath](https://www.rfc-editor.org/rfc/rfc9535.html) 来选择 JSON 文档中的特定内容。

| 符号         | 描述                  |
| -------------- | ---------------------------- |
| `$`            | 文件根目录              |
| `.`            | 选择成员             |
| `[]`           | 选择数组            |
| `*`            | 通配符                     |
| `**`           | 路径通配符               |
| `[<n> to <n>]` | 选择数组范围       |

下面以如下 JSON 文档为例，说明如何使用 JSONPath：

```json
{
    "database": {
        "name": "TiDB",
        "features": [
            "distributed",
            "scalable",
            "relational",
            "cloud native"
        ],
        "license": "Apache-2.0 license",
        "versions": [
            {
                "version": "v8.1.1",
                "type": "lts",
                "release_date": "2024-08-27"
            },
            {
                "version": "v8.0.0",
                "type": "dmr",
                "release_date": "2024-03-29"
            }
        ]
    },
    "migration_tool": {
        "name": "TiDB Data Migration",
        "features": [
            "MySQL compatible",
            "Shard merging"
        ],
        "license": "Apache-2.0 license"
    }
}
```

| JSONPath                              | 描述                             | [`JSON_EXTRACT()`](/functions-and-operators/json-functions/json-functions-search.md#json_extract) 示例| 
|-------------------------------------- |-----------------------------------------|-------------------------------|
| `$`                                   | 文档根目录               | 返回完整文档                             |
| `$.database`                          | `database` 对象               |   返回以 `"database"` 开头的完整结构。不包括 `"migration_tool"` 和其下的结构。                            |
| `$.database.name`                     | `database` 的 `name` 值             | `"TiDB"`                      |
| `$.database.features`                 | `database` 的 `features` 值                   | `["distributed", "scalable", "relational", "cloud native"]`                              |
| `$.database.features[0]`              | `database` 的 `features` 中的第一个值            | `"distributed"`               |
| `$.database.features[2]`              | `database` 的 `features` 中的第三个值           | `"relational"`                |
| `$.database.versions[0].type`         | `database` 的 `versions` 中第一个元素的 `type` 值 | `"lts"`                       |
| `$.database.versions[*].release_date` | `versions` 中所有的 `release_date` 值     | `["2024-08-27","2024-03-29"]` |
| `$.*.features`                        | 由所有的 `features` 值组成的两个数组             | `[["distributed", "scalable", "relational", "cloud native"], ["MySQL compatible", "Shard merging"]]`                              |
| `$**.version`                         | 包含用通配符匹配到所有的 `version` 值     | `["v8.1.1","v8.0.0"]`         |
| `$.database.features[0 to 2]`         | `database` 中指定范围的 `features` 值，`features[0 to 2]` 代表从 `features` 的第一个值到第三个值            | `["scalable","relational"]`   |

更多信息，请参考 [JSONPath -- XPath for JSON](https://www.ietf.org/archive/id/draft-goessner-dispatch-jsonpath-00.html)。

## 另请参阅

- [JSON 数据类型](/data-type-json.md)

## 不支持的函数

- `JSON_SCHEMA_VALID()`
- `JSON_SCHEMA_VALIDATION_REPORT()`
- `JSON_TABLE()`
- `JSON_VALUE()`

更多信息，请参考 [#14486](https://github.com/pingcap/tidb/issues/14486)。

## MySQL 兼容性

- TiDB 支持 MySQL 8.0 中的大部分 [JSON 函数](https://dev.mysql.com/doc/refman/8.0/en/json-functions.html)。
