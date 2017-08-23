---
title: Create Database 语句
category: user guide
---

# CREATE DATABASE 语法

```sql
CREATE {DATABASE | SCHEMA} [IF NOT EXISTS] db_name
    [create_specification] ...

create_specification:
    [DEFAULT] CHARACTER SET [=] charset_name
  | [DEFAULT] COLLATE [=] collation_name
```
```CREATE DATABASE``` 用于创建数据库，并可以指定数据库的默认属性（如数据库默认字符集,校验规则。```CREATE SCHEMA``` 跟 ```CREATE DATABASE``` 操作效果一样。
  
当创建已存在的数据库且不指定使用 ```IF NOT EXISTS``` 时会报错。

```create_specification``` 选项用于指定数据库具体的 ```CHARACTER``` 和 ```COLLATE```。目前这个选只是语法支持。