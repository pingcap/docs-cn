---
title: DELETE
summary: TiDB 数据库中 DELETE 的使用概况。
---

# DELETE

`DELETE` 语句用于从指定的表中删除行。

## 语法图

```ebnf+diagram
DeleteFromStmt ::=
    'DELETE' TableOptimizerHints PriorityOpt QuickOptional IgnoreOptional ( 'FROM' ( TableName TableAsNameOpt IndexHintListOpt WhereClauseOptional OrderByOptional LimitClause | TableAliasRefList 'USING' TableRefs WhereClauseOptional ) | TableAliasRefList 'FROM' TableRefs WhereClauseOptional )
```

## 示例

{{< copyable "sql" >}}

```sql
CREATE TABLE t1 (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, c1 INT NOT NULL);
```

```
Query OK, 0 rows affected (0.11 sec)
```

{{< copyable "sql" >}}

```sql
INSERT INTO t1 (c1) VALUES (1),(2),(3),(4),(5);
```

```
Query OK, 5 rows affected (0.03 sec)
Records: 5  Duplicates: 0  Warnings: 0
```

{{< copyable "sql" >}}

```sql
SELECT * FROM t1;
```

```
+----+----+
| id | c1 |
+----+----+
|  1 |  1 |
|  2 |  2 |
|  3 |  3 |
|  4 |  4 |
|  5 |  5 |
+----+----+
5 rows in set (0.00 sec)
```

{{< copyable "sql" >}}

```sql
DELETE FROM t1 WHERE id = 4;
```

```
Query OK, 1 row affected (0.02 sec)
```

{{< copyable "sql" >}}

```sql
SELECT * FROM t1;
```

```
+----+----+
| id | c1 |
+----+----+
|  1 |  1 |
|  2 |  2 |
|  3 |  3 |
|  5 |  5 |
+----+----+
4 rows in set (0.00 sec)
```

## MySQL 兼容性

`DELETE` 语句与 MySQL 完全兼容。如发现任何兼容性差异，请在 GitHub 上提交 [issue](https://github.com/pingcap/tidb/issues/new/choose)。

## 另请参阅

* [INSERT](/sql-statements/sql-statement-insert.md)
* [SELECT](/sql-statements/sql-statement-select.md)
* [UPDATE](/sql-statements/sql-statement-update.md)
* [REPLACE](/sql-statements/sql-statement-replace.md)
