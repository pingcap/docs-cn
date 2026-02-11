---
title: 过滤
summary: 了解如何在你的应用中使用过滤功能。
---

# 过滤

作为一款关系型数据库，TiDB 支持丰富的 [SQL 运算符](https://docs.pingcap.com/tidbcloud/operators/) 以及灵活组合的过滤条件，用于实现精确查询。

## 概述

你可以对标量字段和 JSON 字段进行过滤。对 JSON 字段的过滤通常用于向量搜索中的 [元信息过滤](/ai/guides/vector-search.md#metadata-filtering)。

[`pytidb`](https://github.com/pingcap/pytidb) 是 TiDB 的官方 Python SDK，旨在帮助开发者高效构建 AI 应用。

在使用 `pytidb` 时，你可以通过将 **filters** 参数传递给 `table.query()`、`table.delete()`、`table.update()` 和 `table.search()` 方法来实现过滤。

**filters** 参数支持两种格式：[字典过滤器](#dictionary-filters) 和 [SQL 字符串过滤器](#sql-string-filters)。

## 字典过滤器

`pytidb` 允许你使用带有运算符的 Python 字典来定义过滤条件，并作为 **filters** 参数传入。

**filters** 的字典结构如下：

```python
{
    "<key>": {
        "<operator>": <value>
    },
    ...
}
```

- `<key>`：可以是列名、用于访问 JSON 字段的 JSON 路径表达式（参见 [元信息过滤](/ai/guides/vector-search.md#metadata-filtering)），或 [逻辑运算符](#logical-operators)。
- `<operator>`：可以是 [比较运算符](#compare-operators) 或 [包含运算符](#inclusion-operators)。
- `<value>`：根据运算符，可以是标量值或数组。

**示例：过滤 `created_at` 大于 2024-01-01 的记录**

```python
table.query({
    # `created_at` 是 DATETIME 类型的标量字段
    "created_at": {
        "$gt": "2024-01-01"
    }
})
```

**示例：过滤 `meta.category` 在 ["tech", "science"] 数组中的记录**

```python
results = (
    table.search("some query", search_type="vector")
        .filter({
            # `meta` 是 JSON 字段，其值为类似 {"category": "tech"} 的 JSON 对象
            "meta.category": {
                "$in": ["tech", "science"]
            }
        })
        .limit(10)
        .to_list()
)
```

### 比较运算符

你可以使用以下比较运算符来过滤记录：

| 运算符   | 描述                       |
|----------|----------------------------|
| `$eq`    | 等于指定值                 |
| `$ne`    | 不等于指定值               |
| `$gt`    | 大于指定值                 |
| `$gte`   | 大于等于指定值             |
| `$lt`    | 小于指定值                 |
| `$lte`   | 小于等于指定值             |

**示例：过滤 `user_id` 等于 1 的记录**

```python
{
    "user_id": {
        "$eq": 1
    }
}
```

你可以省略 `$eq` 运算符。以下过滤条件与上例等价：

```python
{
    "user_id": 1
}
```

### 包含运算符

你可以使用以下包含运算符来过滤记录：

| 运算符   | 描述                                 |
|----------|--------------------------------------|
| `$in`    | 在数组中（string、整数型或 float）    |
| `$nin`   | 不在数组中（string、整数型、float）   |

**示例：过滤 `category` 在 ["tech", "science"] 数组中的记录**

```python
{
    "category": {
        "$in": ["tech", "science"]
    }
}
```

### 逻辑运算符

你可以使用逻辑运算符 `$and` 和 `$or` 组合多个过滤条件。

| 运算符   | 描述                                         |
|----------|----------------------------------------------|
| `$and`   | 返回同时满足列表中**所有**过滤条件的结果      |
| `$or`    | 返回满足列表中**任意**过滤条件的结果          |

**`$and` 或 `$or` 的语法：**

```python
{
    "$and|$or": [
        {
            "field_name": {
                <operator>: <value>
            }
        },
        {
            "field_name": {
                <operator>: <value>
            }
        }
        ...
    ]
}
```

**示例：使用 `$and` 组合多个过滤条件：**

```python
{
    "$and": [
        {
            "created_at": {
                "$gt": "2024-01-01"
            }
        },
        {
            "meta.category": {
                "$in": ["tech", "science"]
            }
        }
    ]
}
```

## SQL 字符串过滤器

你也可以将 SQL 字符串作为 `filters` 使用。该字符串必须是符合 TiDB SQL 语法的有效 SQL `WHERE` 子句（不包含 `WHERE` 关键字）。

**示例：过滤 `created_at` 大于 2024-01-01 的记录**

```python
results = table.query(
    filters="created_at > '2024-01-01'",
    limit=10
).to_list()
```

**示例：过滤 JSON 字段 `meta.category` 等于 'tech' 的记录**

```python
results = table.query(
    filters="meta->>'$.category' = 'tech'",
    limit=10
).to_list()
```

你可以使用 `AND`、`OR` 和括号组合多个条件，并使用任何 TiDB 支持的 [SQL 运算符](https://docs.pingcap.com/tidbcloud/operators/)。

> **警告：**
>
> 当使用带有动态用户输入的 SQL 字符串过滤器时，务必校验输入，以防止 [SQL 注入](https://en.wikipedia.org/wiki/SQL_injection) 漏洞。