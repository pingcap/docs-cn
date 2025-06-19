---
title: JSON 函数
summary: 了解 JSON 函数。
---

# JSON 函数

您可以使用 JSON 函数来处理 [JSON 数据类型](/data-type-json.md) 中的数据。

## 创建 JSON 值的函数

| 函数名                     | 描述 |
| --------------------------------- | ----------- |
| [JSON_ARRAY()](/functions-and-operators/json-functions/json-functions-create.md#json_array) | 计算一个（可能为空的）值列表并返回包含这些值的 JSON 数组 |
| [JSON_OBJECT()](/functions-and-operators/json-functions/json-functions-create.md#json_object) | 计算一个（可能为空的）键值对列表并返回包含这些键值对的 JSON 对象 |
| [JSON_QUOTE()](/functions-and-operators/json-functions/json-functions-create.md#json_quote) | 将字符串作为带引号的 JSON 值返回 |

## 搜索 JSON 值的函数

| 函数名                     | 描述 |
| --------------------------------- | ----------- |
| [JSON_CONTAINS()](/functions-and-operators/json-functions/json-functions-search.md#json_contains) | 通过返回 1 或 0 来表示给定的候选 JSON 文档是否包含在目标 JSON 文档中 |
| [JSON_CONTAINS_PATH()](/functions-and-operators/json-functions/json-functions-search.md#json_contains_path) | 返回 0 或 1 以指示 JSON 文档在给定路径或多个路径中是否包含数据 |
| [JSON_EXTRACT()](/functions-and-operators/json-functions/json-functions-search.md#json_extract) | 从 JSON 文档中返回数据，从与 `path` 参数匹配的文档部分中选择 |
| [->](/functions-and-operators/json-functions/json-functions-search.md#-)  | 在计算路径后从 JSON 列返回值；是 `JSON_EXTRACT(doc, path_literal)` 的别名 |
| [->>](/functions-and-operators/json-functions/json-functions-search.md#--1)  | 在计算路径后从 JSON 列返回值并去除引号；是 `JSON_UNQUOTE(JSON_EXTRACT(doc, path_literal))` 的别名 |
| [JSON_KEYS()](/functions-and-operators/json-functions/json-functions-search.md#json_keys) | 以 JSON 数组的形式返回 JSON 对象顶层值的键，如果给定了路径参数，则返回所选路径的顶层键 |
| [JSON_SEARCH()](/functions-and-operators/json-functions/json-functions-search.md#json_search) | 在 JSON 文档中搜索字符串的一个或所有匹配项 |
| [MEMBER OF()](/functions-and-operators/json-functions/json-functions-search.md#member-of) | 如果传入的值是 JSON 数组的元素，则返回 1。否则返回 0。 |
| [JSON_OVERLAPS()](/functions-and-operators/json-functions/json-functions-search.md#json_overlaps) | 指示两个 JSON 文档是否有重叠部分。如果有，返回 1。如果没有，返回 0。 |

## 修改 JSON 值的函数

| 函数名                     | 描述 |
| --------------------------------- | ----------- |
| [JSON_APPEND()](/functions-and-operators/json-functions/json-functions-modify.md#json_append) | `JSON_ARRAY_APPEND()` 的别名 |
| [JSON_ARRAY_APPEND()](/functions-and-operators/json-functions/json-functions-modify.md#json_array_append) | 将值追加到 JSON 文档中指定数组的末尾并返回结果 |
| [JSON_ARRAY_INSERT()](/functions-and-operators/json-functions/json-functions-modify.md#json_array_insert) | 将值插入到 JSON 文档的指定位置并返回结果 |
| [JSON_INSERT()](/functions-and-operators/json-functions/json-functions-modify.md#json_insert) | 将数据插入 JSON 文档并返回结果 |
| [JSON_MERGE_PATCH()](/functions-and-operators/json-functions/json-functions-modify.md#json_merge_patch)  | 合并两个或多个 JSON 文档，不保留重复键的值 |
| [JSON_MERGE_PRESERVE()](/functions-and-operators/json-functions/json-functions-modify.md#json_merge_preserve)  | 通过保留所有值来合并两个或多个 JSON 文档 |
| [JSON_MERGE()](/functions-and-operators/json-functions/json-functions-modify.md#json_merge)  | `JSON_MERGE_PRESERVE()` 的已弃用别名 |
| [JSON_REMOVE()](/functions-and-operators/json-functions/json-functions-modify.md#json_remove)    | 从 JSON 文档中删除数据并返回结果 |
| [JSON_REPLACE()](/functions-and-operators/json-functions/json-functions-modify.md#json_replace) | 替换 JSON 文档中的现有值并返回结果 |
| [JSON_SET()](/functions-and-operators/json-functions/json-functions-modify.md#json_set)  | 在 JSON 文档中插入或更新数据并返回结果 |
| [JSON_UNQUOTE()](/functions-and-operators/json-functions/json-functions-modify.md#json_unquote) | 去除 JSON 值的引号并将结果作为字符串返回 |

## 返回 JSON 值属性的函数

| 函数名                     | 描述 |
| --------------------------------- | ----------- |
| [JSON_DEPTH()](/functions-and-operators/json-functions/json-functions-return.md#json_depth) | 返回 JSON 文档的最大深度 |
| [JSON_LENGTH()](/functions-and-operators/json-functions/json-functions-return.md#json_length) | 返回 JSON 文档的长度，如果给定了路径参数，则返回该路径内值的长度 |
| [JSON_TYPE()](/functions-and-operators/json-functions/json-functions-return.md#json_type) | 返回指示 JSON 值类型的字符串 |
| [JSON_VALID()](/functions-and-operators/json-functions/json-functions-return.md#json_valid) | 检查 json\_doc 是否为有效的 JSON。 |

## 实用函数

| 函数名                     | 描述 |
| --------------------------------- | ----------- |
| [JSON_PRETTY()](/functions-and-operators/json-functions/json-functions-utility.md#json_pretty) | JSON 文档的美化格式 |
| [JSON_STORAGE_FREE()](/functions-and-operators/json-functions/json-functions-utility.md#json_storage_free) | 返回 JSON 值原地更新后在其二进制表示中释放了多少存储空间。 |
| [JSON_STORAGE_SIZE()](/functions-and-operators/json-functions/json-functions-utility.md#json_storage_size) | 返回存储 JSON 值所需的大致字节数。由于该大小未考虑 TiKV 使用压缩，因此此函数的输出与 MySQL 不完全兼容。 |

## 聚合函数

| 函数名                     | 描述 |
| --------------------------------- | ----------- |
| [JSON_ARRAYAGG()](/functions-and-operators/json-functions/json-functions-aggregate.md#json_arrayagg) | 提供键的聚合。 |
| [JSON_OBJECTAGG()](/functions-and-operators/json-functions/json-functions-aggregate.md#json_objectagg) | 提供给定键的值的聚合。 |

## JSONPath

许多 JSON 函数使用 [JSONPath](https://www.rfc-editor.org/rfc/rfc9535.html) 来选择 JSON 文档的部分内容。

| 符号         | 描述                  |
| -------------- | ---------------------------- |
| `$`            | 文档根                |
| `.`            | 成员选择             |
| `[]`           | 数组选择              |
| `*`            | 通配符                     |
| `**`           | 路径通配符                |
| `[<n> to <n>]` | 数组范围选择        |

以下内容以这个 JSON 文档为例来演示如何使用 JSONPath：

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
                "version": "v8.1.2",
                "type": "lts",
                "release_date": "2024-12-26" 
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

| JSONPath                              | 描述                             | 使用 [`JSON_EXTRACT()`](/functions-and-operators/json-functions/json-functions-search.md#json_extract) 的示例 | 
|-------------------------------------- |-----------------------------------------|-------------------------------|
| `$`                                   | 文档的根                | 返回完整文档                              |
| `$.database`                          | `database` 对象                  | 返回以 `"database"` 开始的完整结构。不包括 `"migration_tool"` 及其下的结构。                             |
| `$.database.name`                     | 数据库的名称               | `"TiDB"`                      |
| `$.database.features`                 | 所有数据库特性                   | `["distributed", "scalable", "relational", "cloud native"]`                              |
| `$.database.features[0]`              | 第一个数据库特性             | `"distributed"`               |
| `$.database.features[2]`              | 第三个数据库特性             | `"relational"`                |
| `$.database.versions[0].type`         | 第一个数据库版本的类型 | `"lts"`                       |
| `$.database.versions[*].release_date` | 所有版本的发布日期      | `["2024-12-26","2024-03-29"]` |
| `$.*.features`                        | 两个特性数组                 | `[["distributed", "scalable", "relational", "cloud native"], ["MySQL compatible", "Shard merging"]]`                              |
| `$**.version`                         | 使用路径通配符的所有版本        | `["v8.1.2","v8.0.0"]`         |
| `$.database.features[0 to 2]`         | 从第一个到第三个的数据库特性范围             | `["scalable","relational"]`   |

更多信息，请参见 [IETF 的 JSONPath 草案](https://www.ietf.org/archive/id/draft-goessner-dispatch-jsonpath-00.html)。

## 另请参阅

* [JSON 数据类型](/data-type-json.md)

## 不支持的函数

- `JSON_SCHEMA_VALID()`
- `JSON_SCHEMA_VALIDATION_REPORT()`
- `JSON_TABLE()`
- `JSON_VALUE()`

更多信息，请参见 [#14486](https://github.com/pingcap/tidb/issues/14486)。

## MySQL 兼容性

- TiDB 支持 MySQL 8.0 中提供的大多数 [JSON 函数](https://dev.mysql.com/doc/refman/8.0/en/json-functions.html)。
