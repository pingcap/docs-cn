---
title: ALTER DATABASE
summary: TiDB 数据库中 ALTER DATABASE 的使用概况。
---

# ALTER DATABASE

`ALTER DATABASE` 用于修改指定或当前数据库的默认字符集和排序规则。`ALTER SCHEMA` 跟 `ALTER DATABASE` 操作效果一样。

## 语法图

```ebnf+diagram
AlterDatabaseStmt ::=
    'ALTER' 'DATABASE' DBName? DatabaseOptionList

DatabaseOption ::=
    DefaultKwdOpt ( CharsetKw '='? CharsetName | 'COLLATE' '='? CollationName | 'ENCRYPTION' '='? EncryptionOpt )
```

## 示例

修改数据库 `test` 的字符集为 `utf8mb4`：

{{< copyable "sql" >}}

```sql
ALTER DATABASE test DEFAULT CHARACTER SET = utf8mb4;
```

```sql
Query OK, 0 rows affected (0.00 sec)
```

目前 TiDB 只支持部分的字符集和排序规则，详情参阅[字符集支持](/character-set-and-collation.md)。

## MySQL 兼容性

`ALTER DATABASE` 语句与 MySQL 完全兼容。如发现任何兼容性差异，请在 GitHub 上提交 [issue](https://github.com/pingcap/tidb/issues/new/choose)。

## 另请参阅

* [CREATE DATABASE](/sql-statements/sql-statement-create-database.md)
* [SHOW DATABASES](/sql-statements/sql-statement-show-databases.md)
