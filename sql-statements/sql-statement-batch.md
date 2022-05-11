---
title: BATCH 
summary: TiDB 数据库中 BATCH 的使用概况。
aliases: ['/docs-cn/dev/sql-statements/sql-statement-batch/']
---

# BATCH 

BATCH 语句将一个 DML 语句拆成多个在内部执行，因此**不保证事务的 atomicity 和 isolation 特性**，是一个“非事务”语句。

目前 BATCH 语句仅支持 DELETE。

BATCH 语句在某一列将 DML 语句涉及的范围划分为多个区间，在每个区间执行一条 SQL。

详细的说明和使用限制见 [非事务语句](/non-transactional-DML.md)。

## 语法图

```ebnf+diagram
NonTransactionalDeleteStmt ::= 
    "BATCH" ["ON" ColumnName] "LIMIT" NUM ["DRY" "RUN" ["QUERY"]] DeleteFromStmt
```

## 限制

- DELETE 语句不可以具有 ORDER BY 或 LIMIT 子句。
- 指定的用于 BATCH 的列名必须是被索引的。索引可以是单列的索引，也可以是联合索引的第一列。

## 示例

{{< copyable "sql" >}}

```sql
CREATE TABLE t(id int, v int, key(id));
```

```sql
Query OK, 0 rows affected
```

{{< copyable "sql" >}}

```sql
INSERT INTO t VALUES (1,2),(2,3),(3,4),(4,5),(5,6);
```

```sql
Query OK, 5 rows affected
```

DRY RUN QUERY 可以查询用于划分 batch 的语句。不实际执行这个查询和后续的 DML。

{{< copyable "sql" >}}

```sql
BATCH ON id LIMIT 2 DRY RUN QUERY DELETE FROM T WHERE v < 6;
```

```sql
+--------------------------------------------------------------------------------+
| query statement                                                                |
+--------------------------------------------------------------------------------+
| SELECT `id` FROM `test`.`T` WHERE (`v` < 6) ORDER BY IF(ISNULL(`id`),0,1),`id` |
+--------------------------------------------------------------------------------+
1 row in set
```

{{< copyable "sql" >}}

```sql
BATCH ON id LIMIT 2 DRY RUN DELETE FROM T where v < 6;
```

DRY RUN 可以查询第一个和最后一个 batch 对应的实际 DML。因为 batch 数量可能很多，不显示全部 batch 的。

```sql
+-------------------------------------------------------------------+
| split statement examples                                          |
+-------------------------------------------------------------------+
| DELETE FROM `test`.`T` WHERE (`id` BETWEEN 1 AND 2 AND (`v` < 6)) |
| DELETE FROM `test`.`T` WHERE (`id` BETWEEN 3 AND 4 AND (`v` < 6)) |
+-------------------------------------------------------------------+
2 rows in set
```

{{< copyable "sql" >}}

```sql
BATCH ON id LIMIT 2 DELETE FROM T where v < 6;
```

```sql
+----------------+---------------+
| number of jobs | job status    |
+----------------+---------------+
| 2              | all succeeded |
+----------------+---------------+
1 row in set
```

{{< copyable "sql" >}}

```sql
SELECT * FROM t;
```

```sql
+----+---+
| id | v |
+----+---+
| 5  | 6 |
+----+---+
1 row in set
```

## MySQL 兼容性

BATCH 语句是 TiDB 独有的语句，与 MySQL 不兼容。

## 另请参阅

* [非事务语句](/non-transactional-DML.md)
