---
title: ADMIN CHECK [TABLE|INDEX] | TiDB SQL 语句参考
summary: TiDB 数据库中 ADMIN 使用概览。
category: reference
---

# ADMIN CHECK [TABLE|INDEX]

`ADMIN CHECK [TABLE|INDEX]` 语句用于检查表和索引的数据一致性。

它不支持以下功能：

- 检查 [FOREIGN KEY 约束](/foreign-key.md)。
- 如果使用了[聚簇主键](/clustered-indexes.md)，则不支持检查 PRIMARY KEY 索引。

如果 `ADMIN CHECK [TABLE|INDEX]` 发现任何问题，你可以通过删除并重新创建索引来解决这些问题。如果问题仍未解决，你可以[报告 bug](https://docs.pingcap.com/tidb/stable/support)。

## 原理

`ADMIN CHECK TABLE` 语句通过以下步骤检查表：

1. 对于每个索引，它检查索引中的记录数是否与表中的记录数相同。

2. 对于每个索引，它遍历每行中的值并将这些值与表中的值进行比较。

如果你使用 `ADMIN CHECK INDEX` 语句，它只检查指定的索引。

## 语法图

```ebnf+diagram
AdminCheckStmt ::=
    'ADMIN' 'CHECK' ( 'TABLE' TableNameList | 'INDEX' TableName Identifier ( HandleRange ( ',' HandleRange )* )? ) 

TableNameList ::=
    TableName ( ',' TableName )*

HandleRange ::= '(' Int64Num ',' Int64Num ')'
```

## 示例

要检查 `tbl_name` 表中所有数据及其对应索引的一致性，使用 `ADMIN CHECK TABLE`：

```sql
ADMIN CHECK TABLE tbl_name [, tbl_name] ...;
```

如果一致性检查通过，则返回空结果。否则，返回错误消息指示数据不一致。

```sql
ADMIN CHECK INDEX tbl_name idx_name;
```

上述语句用于检查 `tbl_name` 表中对应于 `idx_name` 索引的列数据和索引数据的一致性。如果一致性检查通过，则返回空结果；否则，返回错误消息指示数据不一致。

```sql
ADMIN CHECK INDEX tbl_name idx_name (lower_val, upper_val) [, (lower_val, upper_val)] ...;
```

上述语句用于检查 `tbl_name` 表中对应于 `idx_name` 索引的列数据和索引数据的一致性，并指定要检查的数据范围。如果一致性检查通过，则返回空结果。否则，返回错误消息指示数据不一致。

## MySQL 兼容性

该语句是 TiDB 对 MySQL 语法的扩展。

## 另请参阅

* [`ADMIN REPAIR`](/sql-statements/sql-statement-admin.md#admin-repair-statement)
