---
title: DDL
category: user guide
---

# 数据定义语言
DDL（Data Definition Language）用于定义和管理数据库以及数据库中各种对象的语句。

+ [CREATE DATABASE 语法](#create-database-语法)
+ ALTER TABLE 语法
+ CREATE INDEX 语法
+ CREATE TABLE 语法
+ DROP DATABASE 语法
+ DROP INDEX 语法
+ DROP TABLE 语法
+ TRUNCATE TABLE 语法
+ RENAME TABLE 语法

## CREATE DATABASE 语法

```sql
CREATE {DATABASE | SCHEMA} [IF NOT EXISTS] db_name
    [create_specification] ...

create_specification:
    [DEFAULT] CHARACTER SET [=] charset_name
  | [DEFAULT] COLLATE [=] collation_name
```

`CREATE DATABASE` 用于创建数据库，并可以指定数据库的默认属性（如数据库默认字符集,校验规则。`CREATE SCHEMA` 跟 `CREATE DATABASE` 操作效果一样。
  
当创建已存在的数据库且不指定使用 `IF NOT EXISTS` 时会报错。

`create_specification` 选项用于指定数据库具体的 `CHARACTER` 和 `COLLATE`。目前这个选项只是语法支持。