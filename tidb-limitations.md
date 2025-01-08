---
title: TiDB 使用限制
summary: TiDB 中的使用限制包括标识符长度限制、数据库、表、视图、连接总个数限制、单个数据库和表的限制、单行限制、数据类型限制、SQL 语句限制和 TiKV 版本限制。
---

# 使用限制

本文会将详细描述 TiDB 中常见的使用限制，包括：标识符长度，最大支持的数据库、表、索引、分区表、序列等的个数。

> **注意：**
>
> TiDB 高度兼容 MySQL 协议，也兼容了很多 MySQL 本身的限制，比如单个索引最多可包含 16 列。详细请参考[与 MySQL 兼容性对比](/mysql-compatibility.md) 和 MySQL 官方文档。

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

| 类型  | 最大个数   |
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

| 类型       | 最大限制（默认值）              |
|:----------|:------------------------------|
| Columns   | 默认为 1017，最大可调至 4096     |
| Indexes   | 默认为 64，最大可调至 512        |
| Rows      | 无限制                         |
| Size      | 无限制                         |
| Partitions| 8192                          |

* Columns 的最大限制可通过 [`table-column-count-limit`](/tidb-configuration-file.md#table-column-count-limit-从-v50-版本开始引入) 修改。
* Indexes 的最大限制可通过 [`index-limit`](/tidb-configuration-file.md#index-limit-从-v50-版本开始引入) 修改。

## 单行的限制

| 类型       | 最大限制（默认值）   |
|:----------|:----------|
| Size       | 默认为 6 MiB，可通过 [`txn-entry-size-limit`](/tidb-configuration-file.md#txn-entry-size-limit-从-v4010-和-v500-版本开始引入) 配置项调至 120 MiB |

## 数据类型限制

| 类型       | 最大限制   |
|:----------|:----------|
| CHAR       | 255 字符      |
| BINARY     | 255 字节      |
| VARBINARY  | 65535 字节    |
| VARCHAR    | 16383 字符    |
| TEXT       | 默认为 6291456 字节（即 6 MiB），可调至 125829120 字节（即 120 MiB）      |
| BLOB       | 默认为 6291456 字节（即 6 MiB），可调至 125829120 字节（即 120 MiB）      |

## SQL Statements 的限制

| 类型       | 最大限制   |
|:----------|:----------|
| 单个事务最大语句数 |  在使用乐观事务并开启事务重试的情况下，默认限制 5000，可通过 [`stmt-count-limit`](/tidb-configuration-file.md#stmt-count-limit) 调整 |

## TiKV 版本的限制

在集群中，如果 TiDB 组件的版本为 v6.2.0 及以上，则 TiKV 组件版本不得低于 v6.2.0。
