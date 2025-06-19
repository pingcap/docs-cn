---
title: ALTER DATABASE | TiDB SQL 语句参考
summary: TiDB 数据库中 ALTER DATABASE 的使用概览。
---

# ALTER DATABASE

`ALTER DATABASE` 用于指定或修改当前数据库的默认字符集和排序规则。`ALTER SCHEMA` 与 `ALTER DATABASE` 具有相同的效果。

## 语法

```ebnf+diagram
AlterDatabaseStmt ::=
    'ALTER' 'DATABASE' DBName? DatabaseOptionList

DatabaseOption ::=
    DefaultKwdOpt ( CharsetKw '='? CharsetName | 'COLLATE' '='? CollationName | 'ENCRYPTION' '='? EncryptionOpt )
```

## 示例

修改 test 数据库架构以使用 utf8mb4 字符集：

{{< copyable "sql" >}}

```sql
ALTER DATABASE test DEFAULT CHARACTER SET = utf8mb4;
```

```sql
Query OK, 0 rows affected (0.00 sec)
```

目前，TiDB 仅支持部分字符集和排序规则。详情请参见[字符集和排序规则支持](/character-set-and-collation.md)。

## MySQL 兼容性

TiDB 中的 `ALTER DATABASE` 语句与 MySQL 完全兼容。如果您发现任何兼容性差异，请[报告问题](https://docs.pingcap.com/tidb/stable/support)。

## 另请参见

* [CREATE DATABASE](/sql-statements/sql-statement-create-database.md)
* [SHOW DATABASES](/sql-statements/sql-statement-show-databases.md)
