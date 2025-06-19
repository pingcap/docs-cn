---
title: 视图
summary: 了解如何在 TiDB 中使用视图。
---

# 视图

本文档介绍如何在 TiDB 中使用视图。

## 概述

TiDB 支持视图。视图充当虚拟表，其架构由创建视图的 `SELECT` 语句定义。

- 你可以创建视图来仅向用户公开安全的字段和数据，这确保了底层表中敏感字段和数据的安全性。
- 你可以为经常使用的复杂查询创建视图，使复杂查询更简单和方便。

## 创建视图

在 TiDB 中，可以使用 `CREATE VIEW` 语句将复杂查询定义为视图。语法如下：

```sql
CREATE VIEW view_name AS query;
```

注意，你不能创建与现有视图或表同名的视图。

例如，[多表联接查询](/develop/dev-guide-join-tables.md)通过 `JOIN` 语句联接 `books` 表和 `ratings` 表，获取带有平均评分的书籍列表。

为了便于后续查询，你可以使用以下语句将查询定义为视图：

```sql
CREATE VIEW book_with_ratings AS
SELECT b.id AS book_id, ANY_VALUE(b.title) AS book_title, AVG(r.score) AS average_score
FROM books b
LEFT JOIN ratings r ON b.id = r.book_id
GROUP BY b.id;
```

## 查询视图

创建视图后，你可以像查询普通表一样使用 `SELECT` 语句查询视图。

```sql
SELECT * FROM book_with_ratings LIMIT 10;
```

当 TiDB 查询视图时，它会查询与该视图关联的 `SELECT` 语句。

## 更新视图

目前，TiDB 中的视图不支持 `ALTER VIEW view_name AS query;`，你可以通过以下两种方式"更新"视图：

- 使用 `DROP VIEW view_name;` 语句删除旧视图，然后使用 `CREATE VIEW view_name AS query;` 语句创建新视图来更新视图。
- 使用 `CREATE OR REPLACE VIEW view_name AS query;` 语句覆盖同名的现有视图。

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

结果如下：

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

结果如下：

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

使用 `DROP VIEW view_name;` 语句删除视图。

```sql
DROP VIEW book_with_ratings;
```

## 限制

有关 TiDB 中视图的限制，请参见[视图的限制](/views.md#limitations)。

## 阅读更多

- [视图](/views.md)
- [CREATE VIEW 语句](/sql-statements/sql-statement-create-view.md)
- [DROP VIEW 语句](/sql-statements/sql-statement-drop-view.md)
- [使用视图的 EXPLAIN 语句](/explain-views.md)
- [TiFlink：使用 TiKV 和 Flink 的强一致性物化视图](https://github.com/tiflink/tiflink)

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上询问社区，或[提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上询问社区，或[提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>
