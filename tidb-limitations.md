---
title: TiDB Limitations
summary: Learn the usage limitations of TiDB.
aliases: ['/docs/dev/tidb-limitations/']
---

# TiDB Limitations

This document describes the common usage limitations of TiDB, including the maximum identifier length and the maximum number of supported databases, tables, indexes, partitioned tables, and sequences.

## Limitations on identifier length

| Identifier type | Maximum length (number of characters allowed) |
|:---------|:--------------|
| Database | 64 |
| Table    | 64 |
| Column   | 64 |
| Index    | 64 |
| View     | 64 |
| Sequence | 64 |

## Limitations on the total number of databases, tables, views, and connections

| Identifier type  | Maximum number  |
|:----------|:----------|
| Databases | unlimited |
| Tables    | unlimited |
| Views     | unlimited |
| Connections| unlimited|

## Limitations on a single database

| Type       | Upper limit   |
|:----------|:----------|
| Tables    | unlimited  |

## Limitations on a single table

| Type       | Upper limit (default value)  |
|:----------|:----------|
| Columns   | Defaults to 1071 and can be adjusted up to 4096     |
| Indexes   |  Defaults to 64 and can be adjusted up to 512        |
| Rows      | unlimited |
| Size      | unlimited |
| Partitions | 1024      |

* The upper limit of `Columns` can be modified via [`table-column-count-limit`](/tidb-configuration-file.md#table-column-count-limit-new-in-v50).
* The upper limit of `Indexes` can be modified via [`index-limit`](/tidb-configuration-file.md#index-limit-new-in-v50).

## Limitation on a single row

| Type       | Upper limit   |
|:----------|:----------|
| Size       | 6 MB by default. You can adjust the size limit via the [`txn-entry-size-limit`](/tidb-configuration-file.md#txn-entry-size-limit-new-in-v50) configuration item. |

## Limitation on a single column

| Type       | Upper limit   |
|:----------|:----------|
| Size       | 6 MB       |

## Limitations on string types

| Type       | Upper limit   |
|:----------|:----------|
| CHAR       | 256 characters      |
| BINARY     | 256 characters      |
| VARBINARY  | 65535 characters    |
| VARCHAR    | 16383 characters    |
| TEXT       | 6 MB                |
| BLOB       | 6 MB                |

## Limitations on SQL statements

| Type       | Upper limit   |
|:----------|:----------|
| The maximum number of SQL statements in a single transaction |  When the optimistic transaction is used and the transaction retry is enabled, the default upper limit is 5000, which can be modified using [`stmt-count-limit`](/tidb-configuration-file.md#stmt-count-limit). |
