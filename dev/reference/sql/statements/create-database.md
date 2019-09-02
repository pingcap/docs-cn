---
title: CREATE DATABASE
summary: TiDB 数据库中 CREATE DATABASE 的使用概况。
category: reference
---

# CREATE DATABASE

`CREATE DATABASE` 语句用于在 TiDB 上创建新数据库。按照 SQL 标准，“数据库” 一词在 MySQL 术语中最接近 “schema”。

## 语法图

**CreateDatabaseStmt:**

![CreateDatabaseStmt](/media/sqlgram/CreateDatabaseStmt.png)

**DatabaseSym:**

![DatabaseSym](/media/sqlgram/DatabaseSym.png)

**IfNotExists:**

![IfNotExists](/media/sqlgram/IfNotExists.png)

**DBName:**

![DBName](/media/sqlgram/DBName.png)

**DatabaseOptionListOpt:**

![DatabaseOptionListOpt](/media/sqlgram/DatabaseOptionListOpt.png)

## 语法说明

`CREATE DATABASE` 用于创建数据库，并可以指定数据库的默认属性（如数据库默认字符集、排序规则）。`CREATE SCHEMA` 跟 `CREATE DATABASE` 操作效果一样。

```sql
CREATE {DATABASE | SCHEMA} [IF NOT EXISTS] db_name
    [create_specification] ...

create_specification:
    [DEFAULT] CHARACTER SET [=] charset_name
  | [DEFAULT] COLLATE [=] collation_name
```

当创建已存在的数据库且不指定使用 `IF NOT EXISTS` 时会报错。

`create_specification` 选项用于指定数据库具体的 `CHARACTER SET` 和 `COLLATE`。目前 TiDB 只支持部分的字符集和排序规则，请参照[字符集支持](dev/reference/sql/character-set.md)。

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

`CREATE DATABASE` 语句与 MySQL 完全兼容。如有任何兼容性差异，请在 GitHub 上提交 [issue](dev/report-issue.md)。

## 另请参阅

* [USE](dev/reference/sql/statements/use.md)
* [ALTER DATABASE](dev/reference/sql/statements/alter-database.md)
* [DROP DATABASE](dev/reference/sql/statements/drop-database.md)
* [SHOW DATABASES](dev/reference/sql/statements/show-databases.md)
