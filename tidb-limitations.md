---
title: TiDB 使用限制
category: introduction
---

# 使用限制

本文会将详细描述 TiDB 中常见的使用限制，包括：标识符长度，最大支持的数据库、表、索引、分区表、序列等的个数

## 标识符长度限制

| 标识符类型 | 最大长度（字符）|
|:---------|:--------------|
| Database | 64 |
| Table    | 64 |
| Cloumn   | 64 |
| Index    | 64 |
| View     | 64 |
| Sequence | 64 |

## Databases、Tables、Views、Connections 总个数限制

| 标识符类型  | 最大个数   |
|:----------|:----------|
| Databases | unlimited |
| Tables    | unlimited |
| Views     | unlimited |
| Connections| unlimited |

## 单个 Table 相关的限制

| 类型       | 最大个数   |
|:----------|:----------|
| Cloumns   | 512       |
| Indexs    | 64        |
| Rows      | unlimited |
| Size      | unlimited |


