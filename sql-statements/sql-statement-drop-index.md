---
title: DROP INDEX
summary: TiDB 数据库中 DROP INDEX 的使用概况。
aliases: ['/docs-cn/dev/reference/sql/statements/drop-index/']
---

# DROP INDEX

`DROP INDEX` 语句用于从指定的表中删除索引，并在 TiKV 中将空间标记为释放。

## 语法图

**AlterTableDropIndexStmt:**

![AlterTableDropIndexStmt](/media/sqlgram/AlterTableDropIndexStmt.png)

**IgnoreOptional:**

![IgnoreOptional](/media/sqlgram/IgnoreOptional.png)

**TableName:**

![TableName](/media/sqlgram/TableName.png)

**AlterTableDropIndexSpec:**

![AlterTableDropIndexSpec](/media/sqlgram/AlterTableDropIndexSpec.png)

**KeyOrIndex:**

![KeyOrIndex](/media/sqlgram/KeyOrIndex.png)

**IfExists:**

![IfExists](/media/sqlgram/IfExists.png)

## 示例

{{< copyable "sql" >}}

```sql
CREATE TABLE t1 (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, c1 INT NOT NULL);
```

```
Query OK, 0 rows affected (0.10 sec)
```

{{< copyable "sql" >}}

```sql
INSERT INTO t1 (c1) VALUES (1),(2),(3),(4),(5);
```

```
Query OK, 5 rows affected (0.02 sec)
Records: 5  Duplicates: 0  Warnings: 0
```

{{< copyable "sql" >}}

```sql
EXPLAIN SELECT * FROM t1 WHERE c1 = 3;
```

```
+-------------------------+----------+-----------+---------------+--------------------------------+
| id                      | estRows  | task      | access object | operator info                  |
+-------------------------+----------+-----------+---------------+--------------------------------+
| TableReader_7           | 10.00    | root      |               | data:Selection_6               |
| └─Selection_6           | 10.00    | cop[tikv] |               | eq(test.t1.c1, 3)              |
|   └─TableFullScan_5     | 10000.00 | cop[tikv] | table:t1      | keep order:false, stats:pseudo |
+-------------------------+----------+-----------+---------------+--------------------------------+
3 rows in set (0.00 sec)
```

{{< copyable "sql" >}}

```sql
CREATE INDEX c1 ON t1 (c1);
```

```
Query OK, 0 rows affected (0.30 sec)
```

{{< copyable "sql" >}}

```sql
EXPLAIN SELECT * FROM t1 WHERE c1 = 3;
```

```
+------------------------+---------+-----------+------------------------+---------------------------------------------+
| id                     | estRows | task      | access object          | operator info                               |
+------------------------+---------+-----------+------------------------+---------------------------------------------+
| IndexReader_6          | 0.01    | root      |                        | index:IndexRangeScan_5                      |
| └─IndexRangeScan_5     | 0.01    | cop[tikv] | table:t1, index:c1(c1) | range:[3,3], keep order:false, stats:pseudo |
+------------------------+---------+-----------+------------------------+---------------------------------------------+
2 rows in set (0.00 sec)
```

{{< copyable "sql" >}}

```sql
ALTER TABLE t1 DROP INDEX c1;
```

```
Query OK, 0 rows affected (0.30 sec)
```

## MySQL 兼容性

* 默认不支持删除 `PRIMARY KEY`，在开启 `alter-primary-key` 配置项后可支持此功能，详情参考：[alter-primary-key](/tidb-configuration-file.md#alter-primary-key)。

## 另请参阅

* [SHOW INDEX](/sql-statements/sql-statement-show-index.md)
* [CREATE INDEX](/sql-statements/sql-statement-create-index.md)
* [ADD INDEX](/sql-statements/sql-statement-add-index.md)
* [RENAME INDEX](/sql-statements/sql-statement-rename-index.md)
* [ALTER INDEX](/sql-statements/sql-statement-alter-index.md)
