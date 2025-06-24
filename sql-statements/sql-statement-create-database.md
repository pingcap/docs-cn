---
title: CREATE DATABASE | TiDB SQL 语句参考
summary: TiDB 数据库中 CREATE DATABASE 的使用概览。
---

# CREATE DATABASE

此语句在 TiDB 中创建一个新的数据库。MySQL 中的"数据库"术语最接近于 SQL 标准中的 schema。

## 语法图

```ebnf+diagram
CreateDatabaseStmt ::=
    'CREATE' 'DATABASE' IfNotExists DBName DatabaseOptionListOpt

IfNotExists ::=
    ( 'IF' 'NOT' 'EXISTS' )?

DBName ::=
    Identifier

DatabaseOptionListOpt ::=
    DatabaseOptionList?

DatabaseOptionList ::=
    DatabaseOption ( ','? DatabaseOption )*

DatabaseOption ::=
    DefaultKwdOpt ( CharsetKw '='? CharsetName | 'COLLATE' '='? CollationName | 'ENCRYPTION' '='? EncryptionOpt )
|   DefaultKwdOpt PlacementPolicyOption

PlacementPolicyOption ::=
    "PLACEMENT" "POLICY" EqOpt PolicyName
|   "PLACEMENT" "POLICY" (EqOpt | "SET") "DEFAULT"
```

## 语法说明

`CREATE DATABASE` 语句用于创建数据库，并指定数据库的默认属性，如默认字符集和排序规则。`CREATE SCHEMA` 是 `CREATE DATABASE` 的同义词。

```sql
CREATE {DATABASE | SCHEMA} [IF NOT EXISTS] db_name
    [create_specification] ...

create_specification:
    [DEFAULT] CHARACTER SET [=] charset_name
  | [DEFAULT] COLLATE [=] collation_name
```

如果你创建一个已存在的数据库且未指定 `IF NOT EXISTS`，将显示错误。

`create_specification` 选项用于指定数据库中的特定 `CHARACTER SET` 和 `COLLATE`。目前，TiDB 仅支持部分字符集和排序规则。详情请参见[字符集和排序规则支持](/character-set-and-collation.md)。

## 示例

```sql
mysql> CREATE DATABASE mynewdatabase;
Query OK, 0 rows affected (0.09 sec)

mysql> USE mynewdatabase;
Database changed
mysql> CREATE TABLE t1 (a int);
Query OK, 0 rows affected (0.11 sec)

mysql> SHOW TABLES;
+-------------------------+
| Tables_in_mynewdatabase |
+-------------------------+
| t1                      |
+-------------------------+
1 row in set (0.00 sec)
```

## MySQL 兼容性

TiDB 中的 `CREATE DATABASE` 语句与 MySQL 完全兼容。如果发现任何兼容性差异，请[报告问题](https://docs.pingcap.com/tidb/stable/support)。

## 另请参阅

* [USE](/sql-statements/sql-statement-use.md)
* [ALTER DATABASE](/sql-statements/sql-statement-alter-database.md)
* [DROP DATABASE](/sql-statements/sql-statement-drop-database.md)
* [SHOW DATABASES](/sql-statements/sql-statement-show-databases.md)
