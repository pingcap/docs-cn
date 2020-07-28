---
title: ALTER INDEX
summary: TiDB 数据库中 ALTER INDEX 的使用概况。
aliases: ['/docs-cn/dev/reference/sql/statements/alter-index/']
---

# ALTER INDEX

`ALTER INDEX` 语句用于修改索引的可见性，可以将索引设置为 `Visible` 或者 `Invisible`。设置为 `Invisible` 的索引将无法被优化器使用。

## 语法图

**AlterTableStmt:**

![AlterTableStmt](/media/sqlgram/AlterTableStmt.png)

**AlterTableSpec:**

![AlterTableSpec](/media/sqlgram/AlterTableSpec.png)

**IndexInvisible:**

![IndexInvisible](/media/sqlgram/IndexInvisible.png)

## 语法

{{< copyable "sql" >}}

```sql
ALTER TABLE [table_name] ALTER INDEX [index_name] {VISIBLE | INVISIBLE}
```

## 示例

可以通过 `ALTER TABLE ... ALTER INDEX ...` 语句，修改索引的可见性：

{{< copyable "sql" >}}

```sql
CREATE TABLE t1 (c1 INT, UNIQUE(c1));
ALTER TABLE t1 ALTER INDEX c1 INVISIBLE;
```

```sql
Query OK, 0 rows affected (0.02 sec)
```

{{< copyable "sql" >}}

```sql
SHOW CREATE TABLE t1;
```

```sql
+-------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Table | Create Table
                                    |
+-------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| t1    | CREATE TABLE `t1` (
  `c1` int(11) DEFAULT NULL,
  UNIQUE KEY `c1` (`c1`) /*!80000 INVISIBLE */
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin |
+-------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

## 不可见索引

不可见索引 (Invisible Indexes) 是 MySQL 8.0 引入的新功能，将一个索引设置为不可见，使优化器不会再使用这条索引。这个功能可以方便地验证使用或者不使用一条索引的查询计划，避免了 `Drop index` 或 `Add index` 这种资源消耗较多的操作。

{{< copyable "sql" >}}

```sql
CREATE TABLE t1 (c1 INT, c2 INT, UNIQUE(c2));
CREATE UNIQUE INDEX c1 ON t1 (c1) INVISIBLE;
```

可以通过 `Create Table` 语句查看，不可见的索引会用 `/*!80000 INVISIBLE */` 标识出：

{{< copyable "sql" >}}

```sql
SHOW CREATE TABLE t1;
```

```sql
+-------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Table | Create Table
                                                              |
+-------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| t1    | CREATE TABLE `t1` (
  `c1` int(11) DEFAULT NULL,
  `c2` int(11) DEFAULT NULL,
  UNIQUE KEY `c2` (`c2`),
  UNIQUE KEY `c1` (`c1`) /*!80000 INVISIBLE */
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin |
+-------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

优化器将无法使用 `c1` 这个**不可见的索引**：

{{< copyable "sql" >}}

```sql
EXPLAIN SELECT c1 FROM t1 ORDER BY c1; 
```

```sql
+-------------------------+----------+-----------+---------------+--------------------------------+
| id                      | estRows  | task      | access object | operator info                  |
+-------------------------+----------+-----------+---------------+--------------------------------+
| Sort_4                  | 10000.00 | root      |               | test.t1.c1:asc                 |
| └─TableReader_8         | 10000.00 | root      |               | data:TableFullScan_7           |
|   └─TableFullScan_7     | 10000.00 | cop[tikv] | table:t1      | keep order:false, stats:pseudo |
+-------------------------+----------+-----------+---------------+--------------------------------+
3 rows in set (0.00 sec)
```

作为对比，c2 是**可见的索引**，优化器将可以使用索引：

{{< copyable "sql" >}}

```sql
EXPLAIN SELECT c2 FROM t1 ORDER BY c2; 
```

```sql
+------------------------+----------+-----------+------------------------+-------------------------------+
| id                     | estRows  | task      | access object          | operator info                 |
+------------------------+----------+-----------+------------------------+-------------------------------+
| IndexReader_13         | 10000.00 | root      |                        | index:IndexFullScan_12        |
| └─IndexFullScan_12     | 10000.00 | cop[tikv] | table:t1, index:c2(c2) | keep order:true, stats:pseudo |
+------------------------+----------+-----------+------------------------+-------------------------------+
2 rows in set (0.00 sec)
```

即使用 SQL Hint `USE INDEX` 强制使用索引，优化器也无法使用不可见索引，否则 SQL 语句会报错：

{{< copyable "sql" >}}

```sql
SELECT * FROM t1 USE INDEX(c1);
```

```sql
ERROR 1176 (42000): Key 'c1' doesn't exist in table 't1'
```

> **注意：**
>
> “不可见”是仅仅对优化器而言的，不可见索引仍然可以被修改或删除。

{{< copyable "sql" >}}

```sql
ALTER TABLE t1 DROP INDEX c1;
```

```sql
Query OK, 0 rows affected (0.02 sec)
```

### 限制

MySQL 对不可见索引有一条限制：不能将**主键**设置为不可见。TiDB 兼容这条限制，将主键设置为不可见后会抛出错误。

{{< copyable "sql" >}}

```sql
CREATE TABLE t2(c1 INT, PRIMARY KEY(c1) INVISIBLE);
```

```sql
ERROR 3522 (HY000): A primary key index cannot be invisible
```

这里的**主键**包括既包括显式的主键（通过 `PRIMARY KEY` 关键字指定的主键），也包括隐式的主键。

当表中不存在显式的主键时，第一个 `UNIQUE` 索引（要求满足索引上的每一列都是 `NOT NULL`）会自动成为隐式的主键。

即不能将隐式的主键设置为不可见的。

> **注意：**
>
> TiDB 并不会实际创建一个**隐式的主键**，这个限制仅仅在行为上兼容 MySQL。

{{< copyable "sql" >}}

```sql
CREATE TABLE t2(c1 INT NOT NULL, UNIQUE(c1) INVISIBLE);
```

```                                                                                                 
ERROR 3522 (HY000): A primary key index cannot be invisible
```

## 另请参阅

* [CREATE TABLE](/sql-statements/sql-statement-create-table.md)
* [CREATE INDEX](/sql-statements/sql-statement-create-index.md)
* [ADD INDEX](/sql-statements/sql-statement-add-index.md)
* [DROP INDEX](/sql-statements/sql-statement-drop-index.md)
* [RENAME INDEX](/sql-statements/sql-statement-rename-index.md)
