---
title: Views
summary: Learn how to use views in TiDB.
---

# Views

This document describes how to use views in TiDB.

## Overview

TiDB supports views. A view acts as a virtual table, whose schema is defined by the `SELECT` statement that creates the view.

- You can create views to expose only safe fields and data to users, which ensures the security of sensitive fields and data in the underlying tables.
- You can create views for complex queries that are frequently used to make complex queries easier and more convenient.

## Create a view

In TiDB, a complex query can be defined as a view with the `CREATE VIEW` statement. The syntax is as follows:

```sql
CREATE VIEW view_name AS query;
```

Note that you cannot create a view with the same name as an existing view or table.

For example, the [multi-table join query](/develop/dev-guide-join-tables.md) gets a list of books with average ratings by joining the `books` table and the `ratings` table through a `JOIN` statement.

For the convenience of subsequent queries, you can define the query as a view using the following statement:

```sql
CREATE VIEW book_with_ratings AS
SELECT b.id AS book_id, ANY_VALUE(b.title) AS book_title, AVG(r.score) AS average_score
FROM books b
LEFT JOIN ratings r ON b.id = r.book_id
GROUP BY b.id;
```

## Query views

Once a view is created, you can use the `SELECT` statement to query the view just like a normal table.

```sql
SELECT * FROM book_with_ratings LIMIT 10;
```

When TiDB queries a view, it queries the `SELECT` statement associated with the view.

## Update views

Currently, the view in TiDB does not support the `ALTER VIEW view_name AS query;`, you can "update" a view in the following two ways:

- Delete the old view with the `DROP VIEW view_name;` statement, and then update the view by creating a new view with the `CREATE VIEW view_name AS query;` statement.
- Use the `CREATE OR REPLACE VIEW view_name AS query;` statement to overwrite an existing view with the same name.

```sql
CREATE OR REPLACE VIEW book_with_ratings AS
SELECT b.id AS book_id, ANY_VALUE(b.title), ANY_VALUE(b.published_at) AS book_title, AVG(r.score) AS average_score
FROM books b
LEFT JOIN ratings r ON b.id = r.book_id
GROUP BY b.id;
```

## Get view related information

### Using the `SHOW CREATE TABLE|VIEW view_name` statement

```sql
SHOW CREATE VIEW book_with_ratings\G
```

The result is as follows:

```
*************************** 1. row ***************************
                View: book_with_ratings
         Create View: CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`%` SQL SECURITY DEFINER VIEW `book_with_ratings` (`book_id`, `ANY_VALUE(b.title)`, `book_title`, `average_score`) AS SELECT `b`.`id` AS `book_id`,ANY_VALUE(`b`.`title`) AS `ANY_VALUE(b.title)`,ANY_VALUE(`b`.`published_at`) AS `book_title`,AVG(`r`.`score`) AS `average_score` FROM `bookshop`.`books` AS `b` LEFT JOIN `bookshop`.`ratings` AS `r` ON `b`.`id`=`r`.`book_id` GROUP BY `b`.`id`
character_set_client: utf8mb4
collation_connection: utf8mb4_general_ci
1 row in set (0.00 sec)
```

### Query the `INFORMATION_SCHEMA.VIEWS` table

```sql
SELECT * FROM information_schema.views WHERE TABLE_NAME = 'book_with_ratings'\G
```

The result is as follows:

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

## Drop views

Use the `DROP VIEW view_name;` statement to drop a view.

```sql
DROP VIEW book_with_ratings;
```

## Limitation

For limitations of views in TiDB, see [Limitations of Views](/views.md#limitations).

## Read More

- [Views](/views.md)
- [CREATE VIEW Statement](/sql-statements/sql-statement-create-view.md)
- [DROP VIEW Statement](/sql-statements/sql-statement-drop-view.md)
- [EXPLAIN Statements Using Views](/explain-views.md)
- [TiFlink: Strongly Consistent Materialized Views Using TiKV and Flink](https://github.com/tiflink/tiflink)
