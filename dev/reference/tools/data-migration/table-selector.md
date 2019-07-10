---
title: Table Selector
summary: 介绍 DM 的 Table Selector
category: reference
---

# Table Selector

Table Selector 提供了一种基于[通配符](https://zh.wikipedia.org/wiki/%E9%80%9A%E9%85%8D%E7%AC%A6) 来匹配指定 `schema/table` 的功能。

## 通配符

table selector 在 `schema-pattern`/`table-pattern` 中可以使用以下两个通配符：

+ 星号(`*`)

    - 匹配零个或者多个字符。例如， `doc*` 匹配 `doc` 和 `document`，但是不匹配 `dodo`。
    - `*` 只能放在 pattern 的最后一位，例如，支持 `doc*`，但是不支持 `do*c`。

+ 问号(`?`)

    - 匹配任意一个空字符除外的字符。

## 匹配规则

- `schema-pattern` 限制不能为空；
- `table-pattern` 可以设置为空。设置为空时，将只根据 `schema-pattern` 对 `schema` 进行匹配，然后返回匹配结果；
- `table-pattern` 不为空时，分别根据 `schema-pattern` 和 `table-pattern` 进行匹配，两个都匹配则结果为匹配。

## 使用示例

- 匹配所有库名以 `schema_` 开头的 schema 和 table

    ```yaml
    schema-pattern： "schema_*"
    table-pattern： ""
    ```

- 匹配所有库名以 `schema_` 为前缀，并且表名以 `table_` 前缀的表

    ```yaml
    schema-pattern = "schema_*"
    table-pattern = "table_*"
    ```
