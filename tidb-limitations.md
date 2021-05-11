---
title: TiDB 使用限制
aliases: ['/docs-cn/stable/tidb-limitations/','/docs-cn/v4.0/tidb-limitations/']
---

# 使用限制

本文会将详细描述 TiDB 中常见的使用限制，包括：标识符长度，最大支持的数据库、表、索引、分区表、序列等的个数。

## 标识符长度限制

| 标识符类型 | 最大长度（字符）|
|:---------|:--------------|
| Database | 64 |
| Table    | 64 |
| Column   | 64 |
| Index    | 64 |
| View     | 64 |
| Sequence | 64 |

## Databases、Tables、Views、Connections 总个数限制

| 标识符类型  | 最大个数   |
|:----------|:----------|
| Databases | unlimited |
| Tables    | unlimited |
| Views     | unlimited |
| Connections| unlimited|

## 单个 Database 的限制

| 类型       | 最大限制   |
|:----------|:----------|
| Tables    |unlimited  |

## 单个 Table 的限制

| 类型       | 最大限制   |
|:----------|:----------|
| Columns   | 512       |
| Indexs    | 64        |
| Rows      | unlimited |
| Size      | unlimited |
| Partitions| 1024      |

## 单行的限制

| 类型       | 最大限制   |
|:----------|:----------|
| Size       | 默认为 6MB，可通过 [`txn-entry-size-limit`](/tidb-configuration-file.md#txn-entry-size-limit-从-v4010-版本开始引入) 配置项调整 |

## 单列的限制

| 类型       | 最大限制   |
|:----------|:----------|
| Size       | 6MB       |

## 字符串类型限制

| 类型       | 最大限制   |
|:----------|:----------|
| CHAR       | 256 字符      |
| BINARY     | 256 字节      |
| VARBINARY  | 65535 字节    |
| VARCHAR    | 16383 字符    |
| TEXT       | 6MB 字节      |
| BLOB       | 6MB 字节      |

## SQL Statements 的限制

| 类型       | 最大限制   |
|:----------|:----------|
| 单个事务最大语句数 |  在使用乐观事务并开启事务重试的情况下，默认限制 5000，可通过 [`stmt-count-limit`](/tidb-configuration-file.md#stmt-count-limit) 调整 |
