---
title: ALTER DATABASE
summary: TiDB 数据库中 ALTER DATABASE 的使用概况。
category: reference
---

# ALTER DATABASE

`ALTER DATABASE` 用于修改指定或当前数据库的默认字符集和排序规则。`ALTER SCHEMA` 跟 `ALTER DATABASE` 操作效果一样。

## 示例

```sql
ALTER {DATABASE | SCHEMA} [db_name]
    alter_specification ...
alter_specification:
    [DEFAULT] CHARACTER SET [=] charset_name
  | [DEFAULT] COLLATE [=] collation_name
```

`alter_specification` 选项用于指定数据库具体的 `CHARACTER SET` 和 `COLLATE`。目前 TiDB 只支持部分的字符集和排序规则，请参照[字符集支持](/dev/reference/sql/character-set.md)。

## 另请参阅

* [CREATE DATABASE](/dev/reference/sql/statements/create-database.md)
* [SHOW DATABASES](/dev/reference/sql/statements/show-databases.md)
