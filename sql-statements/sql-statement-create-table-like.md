---
title: CREATE TABLE LIKE
summary: TiDB 数据库中 CREATE TABLE LIKE 的使用概况。
---

# CREATE TABLE LIKE

`CREATE TABLE LIKE` 语句用于复制已有表的定义，但不复制任何数据。

## 语法图

```ebnf+diagram
CreateTableLikeStmt ::=
    'CREATE' OptTemporary 'TABLE' IfNotExists TableName LikeTableWithOrWithoutParen

LikeTableWithOrWithoutParen ::=
    'LIKE' TableName
|   '(' 'LIKE' TableName ')'
```

## 示例

{{< copyable "sql" >}}

```sql
CREATE TABLE t1 (a INT NOT NULL);
```

```
Query OK, 0 rows affected (0.13 sec)
```

{{< copyable "sql" >}}

```sql
INSERT INTO t1 VALUES (1),(2),(3),(4),(5);
```

```
Query OK, 5 rows affected (0.02 sec)
Records: 5  Duplicates: 0  Warnings: 0
```

{{< copyable "sql" >}}

```sql
SELECT * FROM t1;
```

```
+---+
| a |
+---+
| 1 |
| 2 |
| 3 |
| 4 |
| 5 |
+---+
5 rows in set (0.00 sec)
```

{{< copyable "sql" >}}

```sql
CREATE TABLE t2 LIKE t1;
```

```
Query OK, 0 rows affected (0.10 sec)
```

{{< copyable "sql" >}}

```sql
SELECT * FROM t2;
```

```
Empty set (0.00 sec)
```

## Region 的预切分

如果被复制的表定义了 `PRE_SPLIT_REGIONS` 属性，则通过 `CREATE TABLE LIKE` 语句复制的表，会继承该属性并在建表时预切分 Region。关于 `PRE_SPLIT_REGIONS` 属性的说明，参见 [`CREATE TABLE` 语句](/sql-statements/sql-statement-create-table.md)。

## MySQL 兼容性

`CREATE TABLE LIKE` 语句与 MySQL 完全兼容。如发现任何兼容性差异，请在 GitHub 上提交 [issue](https://github.com/pingcap/tidb/issues/new/choose)。

## 另请参阅

* [CREATE TABLE](/sql-statements/sql-statement-create-table.md)
* [SHOW CREATE TABLE](/sql-statements/sql-statement-show-create-table.md)
