---
title: Data Migration DDL 特殊处理说明
---

# Data Migration DDL 特殊处理说明

DM 同步过程中，根据 DDL 的不同，也将采用不同的处理方式。

## 忽略的 DDL 语句

以下语句 DM 并未支持，因此解析到之后直接跳过。

```
// transaction
"^SAVEPOINT"

// skip all flush sqls
"^FLUSH"

// table maintenance
"^OPTIMIZE\\s+TABLE"
"^ANALYZE\\s+TABLE"
"^REPAIR\\s+TABLE"

// temporary table
"^DROP\\s+(\\/\\*\\!40005\\s+)?TEMPORARY\\s+(\\*\\/\\s+)?TABLE"

// trigger
"^CREATE\\s+(DEFINER\\s?=.+?)?TRIGGER"
"^DROP\\s+TRIGGER"

// procedure
"^DROP\\s+PROCEDURE"
"^CREATE\\s+(DEFINER\\s?=.+?)?PROCEDURE"
"^ALTER\\s+PROCEDURE"

// view
"^CREATE\\s*(OR REPLACE)?\\s+(ALGORITHM\\s?=.+?)?(DEFINER\\s?=.+?)?\\s+(SQL SECURITY DEFINER)?VIEW"
"^DROP\\s+VIEW"
"^ALTER\\s+(ALGORITHM\\s?=.+?)?(DEFINER\\s?=.+?)?(SQL SECURITY DEFINER)?VIEW"

// function
// user-defined function
"^CREATE\\s+(AGGREGATE)?\\s*?FUNCTION"
// stored function
"^CREATE\\s+(DEFINER\\s?=.+?)?FUNCTION"
"^ALTER\\s+FUNCTION"
"^DROP\\s+FUNCTION"

// tableSpace
"^CREATE\\s+TABLESPACE"
"^ALTER\\s+TABLESPACE"
"^DROP\\s+TABLESPACE"

// event
"^CREATE\\s+(DEFINER\\s?=.+?)?EVENT"
"^ALTER\\s+(DEFINER\\s?=.+?)?EVENT"
"^DROP\\s+EVENT"

// account management
"^GRANT"
"^REVOKE"
"^CREATE\\s+USER"
"^ALTER\\s+USER"
"^RENAME\\s+USER"
"^DROP\\s+USER"
"^SET\\s+PASSWORD"

```

## 改写的 DDL 语句

以下语句在同步到下游前会进行改写。

```
// 在结尾追加 `IF NOT EXIST`
"^CREATE DATABASE"
"^CREATE TABLE"

// 在结尾追加 `IF EXIST`
"^DROP DATABASE"
"^DROP TABLE"
```

## 合库合表迁移任务

当`shard-mode: pessimistic` 和 `shard-mode: optimistic` 时：

```
// 自动忽略
"DROP DATABASE/TABLE"
"TRUNCATE TABLE"

// 乐观模式不支持以下语句，但仍会执行，需注意避免使用，
"ALTER TABLE table_name ADD COLUMN column_name datatype NOT NULL"（添加无默认值的 not null 的列）。
"ALTER TABLE table_name ADD COLUMN column_name datetime DEFAULT NOW()"（增加的列默认值不固定）。
"ALTER TABLE table_name ADD COLUMN col1 INT DROP COLUMN col2"（在一个 DDL 语句中同时包含 ADD COLUMN 与 DROP COLUMN）。
"ALTER TABLE table_name RENAME COLUMN column_1 TO column_2"（重命名列）。
"ALTER TABLE table_name RENAME INDEX index_1 TO index_2"（重命名索引）。
```

更细节内容，请查看 [分库分表合并迁移](/dm/feature-shard-merge.md)

## 其他

Online DDL 特性也会对 DDL 事件进行特殊处理，详情可参考: [迁移使用 GH-ost/PT-osc 的源数据库](/dm/feature-online-ddl.md)
