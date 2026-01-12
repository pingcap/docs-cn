---
title: 视图
summary: 介绍 TiDB 中的视图功能。
aliases: ['/zh/tidb/dev/use-views']
---

# 视图

本章将介绍 TiDB 中的视图功能。

## 概述

TiDB 支持视图，视图是一张虚拟表，该虚拟表的结构由创建视图时的 `SELECT` 语句定义。

- 通过视图可以对用户只暴露安全的字段及数据，进而保证底层表的敏感字段及数据的安全。
- 将频繁出现的复杂查询定义为视图，可以使复杂查询更加简单便捷。

## 创建视图

在 TiDB 当中，可以通过 `CREATE VIEW` 语句来将某个较为复杂的查询定义为视图，其语法如下：

```sql
CREATE VIEW view_name AS query;
```

请注意，创建的视图名称不能与已有的视图或表重名。

例如，在[多表连接查询](/develop/dev-guide-join-tables.md)章节当中，通过 `JOIN` 语句连接 `books` 表和 `ratings` 表查询到了带有平均评分的书籍列表。为了方便后续查询，可以将该查询语句定义为一个视图，SQL 语句如下所示：

```sql
CREATE VIEW book_with_ratings AS
SELECT b.id AS book_id, ANY_VALUE(b.title) AS book_title, AVG(r.score) AS average_score
FROM books b
LEFT JOIN ratings r ON b.id = r.book_id
GROUP BY b.id;
```

## 查询视图

视图创建完成后，便可以使用 `SELECT` 语句像查询一般数据表一样查询视图。

```sql
SELECT * FROM book_with_ratings LIMIT 10;
```

TiDB 在执行查询视图语句时，会将视图展开成创建视图时定义的 `SELECT` 语句，进而执行展开后的查询语句。

## 更新视图

目前 TiDB 中的视图不支持 `ALTER VIEW view_name AS query;` 语法，你可以通过以下两种方式实现视图的 “更新”：

- 先 `DROP VIEW view_name;` 语句删除旧视图，再通过 `CREATE VIEW view_name AS query;` 语句创建新视图的方式来更新视图。
- 使用 `CREATE OR REPLACE VIEW view_name AS query;` 语句覆盖已存在的同名视图。

```sql
CREATE OR REPLACE VIEW book_with_ratings AS
SELECT b.id AS book_id, ANY_VALUE(b.title), ANY_VALUE(b.published_at) AS book_title, AVG(r.score) AS average_score
FROM books b
LEFT JOIN ratings r ON b.id = r.book_id
GROUP BY b.id;
```

## 获取视图相关信息

### 使用 `SHOW CREATE TABLE|VIEW view_name` 语句

```sql
SHOW CREATE VIEW book_with_ratings\G
```

运行结果为：

```
*************************** 1. row ***************************
                View: book_with_ratings
         Create View: CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`%` SQL SECURITY DEFINER VIEW `book_with_ratings` (`book_id`, `ANY_VALUE(b.title)`, `book_title`, `average_score`) AS SELECT `b`.`id` AS `book_id`,ANY_VALUE(`b`.`title`) AS `ANY_VALUE(b.title)`,ANY_VALUE(`b`.`published_at`) AS `book_title`,AVG(`r`.`score`) AS `average_score` FROM `bookshop`.`books` AS `b` LEFT JOIN `bookshop`.`ratings` AS `r` ON `b`.`id`=`r`.`book_id` GROUP BY `b`.`id`
character_set_client: utf8mb4
collation_connection: utf8mb4_general_ci
1 row in set (0.00 sec)
```

### 查询 `INFORMATION_SCHEMA.VIEWS` 表

```sql
SELECT * FROM information_schema.views WHERE TABLE_NAME = 'book_with_ratings'\G
```

运行结果为：

```
*************************** 1. row ***************************
       TABLE_CATALOG: def
        TABLE_SCHEMA: bookshop
          TABLE_NAME: book_with_ratings
     VIEW_DEFINITION: SELECT `b`.`id` AS `book_id`,ANY_VALUE(`b`.`title`) AS `ANY_VALUE(b.title)`,ANY_VALUE(`b`.`published_at`) AS `book_title`,AVG(`r`.`score`) AS `average_score` FROM `bookshop`.`books` AS `b` LEFT JOIN `bookshop`.`ratings` AS `r` ON `b`.`id`=`r`.`book_id` GROUP BY `b`.`id`
        CHECK_OPTION: CASCADED
        IS_UPDATABLE: NO
             DEFINER: root@%
       SECURITY_TYPE: DEFINER
CHARACTER_SET_CLIENT: utf8mb4
COLLATION_CONNECTION: utf8mb4_general_ci
1 row in set (0.00 sec)
```

## 删除视图

通过 `DROP VIEW view_name;` 语句可以删除已经创建的视图。

```sql
DROP VIEW book_with_ratings;
```

## 局限性

关于局限性，你可以通过阅读参考文档当中的[视图](/views.md#局限性)章节进行了解。

## 扩展阅读

- [视图](/views.md)
- [CREATE VIEW 语句](/sql-statements/sql-statement-create-view.md)
- [DROP VIEW 语句](/sql-statements/sql-statement-drop-view.md)
- [用 EXPLAIN 查看带视图的 SQL 执行计划](/explain-views.md)
- [TiFlink: 使用 TiKV 和 Flink 实现强一致的物化视图](https://github.com/tiflink/tiflink)
