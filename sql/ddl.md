---
title: DDL
category: user guide
---

# 数据定义语言
DDL（Data Definition Language）用于定义和管理数据库以及数据库中各种对象的语句。

+ [CREATE DATABASE 语法](#create-database-语法)
+ [DROP DATABASE 语法](#drop-database-语法)
+ CREATE TABLE 语法
+ [DROP TABLE 语法](#drop-table-语法)
+ [TRUNCATE TABLE 语法](#truncate-table-语法)
+ [RENAME TABLE 语法](#rename-table-语法)
+ ALTER TABLE 语法
+ CREATE INDEX 语法
+ [DROP INDEX 语法](#drop-index-语法t)

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

## DROP DATABASE 语法

```sql
DROP {DATABASE | SCHEMA} [IF EXISTS] db_name
```

`DROP DATABASE` 用于删除指定数据库以及它其中的所用表格。

`IF EXISTS` 用于防止当数据库不存在时发生错误。

## DROP TABLE 语法

```sql
DROP [TEMPORARY] TABLE [IF EXISTS]
    tbl_name [, tbl_name] ...
```

可以同时删除多个表，表之间用 `,` 隔开。

当删除不存在的表时且不指定使用 `IF EXISTS` 时会报错。

## TRUNCATE TABLE 语法

```sql
TRUNCATE [TABLE] tbl_name
```

`TRUNCATE TABLE` 用于清除指定表中所有数据，但是保留表结构。

此操作于删除指定表全表数据的操作类似, 但是操作的执行速度会远快于删除全表的速度，且不受表内数据行数影响。

注意：使用此语句后，原先表内的 `AUTO_INCREMENT` 的值不会记录，会被重新计数。

## RENAME TABLE 语法

```sql
RENAME TABLE
    tbl_name TO new_tbl_name
```

`RENAME TABLE` 用于对一个表进行重命名。

这个语句等价于如下的 `ALTER TABLE` 语句：
```sql
ALTER TABLE old_table RENAME new_table;
```

## DROP INDEX 语法

```sql
DROP INDEX index_name ON tbl_name
```

`DROP INDEX` 用于删除表上的一个索引，目前暂不支持删除主键索引。
