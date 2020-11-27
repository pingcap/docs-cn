---
title: ALTER DATABASE
summary: TiDB 数据库中 ALTER DATABASE 的使用概况。
aliases: ['/docs-cn/dev/sql-statements/sql-statement-alter-database/','/docs-cn/dev/reference/sql/statements/alter-database/']
---

# ALTER DATABASE

`ALTER DATABASE` 用于修改指定或当前数据库的默认字符集和排序规则。`ALTER SCHEMA` 跟 `ALTER DATABASE` 操作效果一样。

## 语法图

**AlterDatabaseStmt:**

![AlterDatabaseStmt](/media/sqlgram/AlterDatabaseStmt.png)

**DatabaseOption:**

![DatabaseOption](/media/sqlgram/DatabaseOption.png)

## 示例

{{< copyable "sql" >}}

```sql
ALTER {DATABASE | SCHEMA} [db_name]
    alter_specification ...
alter_specification:
    [DEFAULT] CHARACTER SET [=] charset_name
  | [DEFAULT] COLLATE [=] collation_name
```

`alter_specification` 选项用于指定数据库具体的 `CHARACTER SET` 和 `COLLATE`。目前 TiDB 只支持部分的字符集和排序规则，请参照[字符集支持](/character-set-and-collation.md)。

## MySQL 兼容性

`ALTER DATABASE` 语句与 MySQL 完全兼容。如发现任何兼容性差异，请在 GitHub 上提交 [issue](https://github.com/pingcap/tidb/issues/new/choose)。

## 另请参阅

* [CREATE DATABASE](/sql-statements/sql-statement-create-database.md)
* [SHOW DATABASES](/sql-statements/sql-statement-show-databases.md)
