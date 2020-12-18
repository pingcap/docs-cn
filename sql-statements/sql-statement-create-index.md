---
title: CREATE INDEX | TiDB SQL Statement Reference
summary: An overview of the usage of CREATE INDEX for the TiDB database.
aliases: ['/docs/dev/sql-statements/sql-statement-create-index/','/docs/dev/reference/sql/statements/create-index/']
---

# CREATE INDEX

This statement adds a new index to an existing table. It is an alternative syntax to `ALTER TABLE .. ADD INDEX`, and included for MySQL compatibility.

## Synopsis

**CreateIndexStmt:**

![CreateIndexStmt](/media/sqlgram/CreateIndexStmt.png)

**IndexKeyTypeOpt:**

![IndexKeyTypeOpt](/media/sqlgram/IndexKeyTypeOpt.png)

**IfNotExists:**

![IfNotExists](/media/sqlgram/IfNotExists.png)

**IndexTypeOpt:**

![IndexTypeOpt](/media/sqlgram/IndexTypeOpt.png)

**IndexPartSpecificationList:**

![IndexPartSpecificationList](/media/sqlgram/IndexPartSpecificationList.png)

**IndexOptionList:**

![IndexOptionList](/media/sqlgram/IndexOptionList.png)

**IndexLockAndAlgorithmOpt:**

![IndexLockAndAlgorithmOpt](/media/sqlgram/IndexLockAndAlgorithmOpt.png)

**IndexType:**

![IndexType](/media/sqlgram/IndexType.png)

**IndexPartSpecification:**

![IndexPartSpecification](/media/sqlgram/IndexPartSpecification.png)

**IndexOption:**

![IndexOption](/media/sqlgram/IndexOption.png)

**IndexTypeName:**

![IndexTypeName](/media/sqlgram/IndexTypeName.png)

**ColumnName:**

![ColumnName](/media/sqlgram/ColumnName.png)

**OptFieldLen:**

![OptFieldLen](/media/sqlgram/OptFieldLen.png)

**IndexNameList:**

![IndexNameList](/media/sqlgram/IndexNameList.png)

**KeyOrIndex:**

![KeyOrIndex](/media/sqlgram/KeyOrIndex.png)

## Examples

```sql
mysql> CREATE TABLE t1 (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, c1 INT NOT NULL);
Query OK, 0 rows affected (0.10 sec)

mysql> INSERT INTO t1 (c1) VALUES (1),(2),(3),(4),(5);
Query OK, 5 rows affected (0.02 sec)
Records: 5  Duplicates: 0  Warnings: 0

mysql> EXPLAIN SELECT * FROM t1 WHERE c1 = 3;
+-------------------------+----------+-----------+---------------+--------------------------------+
| id                      | estRows  | task      | access object | operator info                  |
+-------------------------+----------+-----------+---------------+--------------------------------+
| TableReader_7           | 10.00    | root      |               | data:Selection_6               |
| └─Selection_6           | 10.00    | cop[tikv] |               | eq(test.t1.c1, 3)              |
|   └─TableFullScan_5     | 10000.00 | cop[tikv] | table:t1      | keep order:false, stats:pseudo |
+-------------------------+----------+-----------+---------------+--------------------------------+
3 rows in set (0.00 sec)

mysql> CREATE INDEX c1 ON t1 (c1);
Query OK, 0 rows affected (0.30 sec)

mysql> EXPLAIN SELECT * FROM t1 WHERE c1 = 3;
+------------------------+---------+-----------+------------------------+---------------------------------------------+
| id                     | estRows | task      | access object          | operator info                               |
+------------------------+---------+-----------+------------------------+---------------------------------------------+
| IndexReader_6          | 10.00   | root      |                        | index:IndexRangeScan_5                      |
| └─IndexRangeScan_5     | 10.00   | cop[tikv] | table:t1, index:c1(c1) | range:[3,3], keep order:false, stats:pseudo |
+------------------------+---------+-----------+------------------------+---------------------------------------------+
2 rows in set (0.00 sec)

mysql> ALTER TABLE t1 DROP INDEX c1;
Query OK, 0 rows affected (0.30 sec)

mysql> CREATE UNIQUE INDEX c1 ON t1 (c1);
Query OK, 0 rows affected (0.31 sec)
```

## Expression index

> **Note:**
>
> Expression index is still an experimental feature. It is **NOT** recommended that you use it in the production environment.

To use this feature, make the following setting in [TiDB Configuration File](/tidb-configuration-file.md#allow-expression-index-new-in-v400):

{{< copyable "sql" >}}

```sql
allow-expression-index = true
```

TiDB can build indexes not only on one or more columns in a table, but also on an expression. When queries involve expressions, expression indexes can speed up those queries.

Take the following query as an example:

{{< copyable "sql" >}}

```sql
SELECT * FROM t WHERE lower(name) = "pingcap";
```

If the following expression index is built, you can use the index to speed up the above query:

{{< copyable "sql" >}}

```sql
CREATE INDEX idx ON t ((lower(name)));
```

The cost of maintaining an expression index is higher than that of maintaining other indexes, because the value of the expression needs to be calculated whenever a row is inserted or updated. The value of the expression is already stored in the index, so this value does not require recalculation when the optimizer selects the expression index.

Therefore, when the query performance outweighs the insert and update performance, you can consider indexing the expressions.

Expression indexes have the same syntax and limitations as in MySQL. They are implemented by building indexes on generated virtual columns that are invisible, so the supported expressions inherit all [limitations of virtual generated columns](/generated-columns.md#limitations).

Currently, the optimizer can use the indexed expressions when the expressions are only in the `FIELD` clause, `WHERE` clause, and `ORDER BY` clause. The `GROUP BY` clause will be supported in future updates.

## Invisible index

Invisible indexes are indexes that are ignored by the query optimizer:

```sql
CREATE TABLE t1 (c1 INT, c2 INT, UNIQUE(c2));
CREATE UNIQUE INDEX c1 ON t1 (c1) INVISIBLE;
```

For details, see [`ALTER INDEX`](/sql-statements/sql-statement-alter-index.md).

## Associated session variables

The global variables associated with the `CREATE INDEX` statement are `tidb_ddl_reorg_worker_cnt`, `tidb_ddl_reorg_batch_size` and `tidb_ddl_reorg_priority`. Refer to [system variables](/system-variables.md#tidb_ddl_reorg_worker_cnt) for details.

## MySQL compatibility

* `FULLTEXT`, `HASH` and `SPATIAL` indexes are not supported.
* Descending indexes are not supported (similar to MySQL 5.7).
* Adding the primary key constraint to a table is not supported by default. You can enable the feature by setting the `alter-primary-key` configuration item to `true`. For details, see [alter-primary-key](/tidb-configuration-file.md#alter-primary-key).

## See also

* [Index Selection](/choose-index.md)
* [Wrong Index Solution](/wrong-index-solution.md)
* [ADD INDEX](/sql-statements/sql-statement-add-index.md)
* [DROP INDEX](/sql-statements/sql-statement-drop-index.md)
* [RENAME INDEX](/sql-statements/sql-statement-rename-index.md)
* [ALTER INDEX](/sql-statements/sql-statement-alter-index.md)
* [ADD COLUMN](/sql-statements/sql-statement-add-column.md)
* [CREATE TABLE](/sql-statements/sql-statement-create-table.md)
* [EXPLAIN](/sql-statements/sql-statement-explain.md)
