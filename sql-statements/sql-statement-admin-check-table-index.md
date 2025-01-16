---
title: ADMIN CHECK [TABLE|INDEX]
summary: TiDB 数据库中 ADMIN CHECK [TABLE|INDEX] 的使用概况。
---

# ADMIN CHECK [TABLE|INDEX]

`ADMIN CHECK [TABLE|INDEX]` 语句用于校验表中数据和对应索引的一致性。

该语句不支持：

- 校验[外键约束](/foreign-key.md)。
- 当使用[聚簇索引](/clustered-indexes.md)时，校验主键索引。

如果执行 `ADMIN CHECK [TABLE|INDEX]` 发现任何问题，你可以删除并重新创建索引来解决。如果问题仍未解决，你可以尝试 [TiDB 支持资源](/support.md)。

## 原理

`ADMIN CHECK TABLE` 语句执行以下步骤来校验表：

1. 对每个索引，检查索引中的记录数是否与表中的记录数一致。
2. 对每个索引，遍历每行的值，并将其与表中的值进行比较。

如果使用 `ADMIN CHECK INDEX` 语句，它只会校验指定的索引。

## 语法图

```ebnf+diagram
AdminCheckStmt ::=
    'ADMIN' 'CHECK' ( 'TABLE' TableNameList | 'INDEX' TableName Identifier ( HandleRange ( ',' HandleRange )* )? )

TableNameList ::=
    TableName ( ',' TableName )*

HandleRange ::= '(' Int64Num ',' Int64Num ')'
```

## 示例

可以通过 `ADMIN CHECK TABLE` 语句校验 `tbl_name` 表中所有数据和对应索引的一致性：

```sql
ADMIN CHECK TABLE tbl_name [, tbl_name] ...;
```

若通过一致性校验，则返回空的查询结果；否则返回数据不一致的错误信息。

```sql
ADMIN CHECK INDEX tbl_name idx_name;
```

以上语句用于对 `tbl_name` 表中 `idx_name` 索引对应列数据和索引数据进行一致性校验。若通过校验，则返回空的查询结果；否则返回数据不一致的错误信息。

```sql
ADMIN CHECK INDEX tbl_name idx_name (lower_val, upper_val) [, (lower_val, upper_val)] ...;
```

以上语句用于对 `tbl_name` 表中 `idx_name` 索引对应列数据和索引数据进行一致性校验，并且指定了需要检查的数据范围。若通过校验，则返回空的查询结果；否则返回数据不一致的错误信息。

## MySQL 兼容性

`ADMIN CHECK [TABLE|INDEX]` 语句是 TiDB 对 MySQL 语法的扩展。

## 另请参阅

* [`ADMIN REPAIR`](/sql-statements/sql-statement-admin.md#admin-repair-table-语句)