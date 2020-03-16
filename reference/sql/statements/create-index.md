---
title: CREATE INDEX | TiDB SQL Statement Reference
summary: An overview of the usage of CREATE INDEX for the TiDB database.
category: reference
---

# CREATE INDEX

This statement adds a new index to an existing table. It is an alternative syntax to `ALTER TABLE .. ADD INDEX`, and included for MySQL compatibility.

## Synopsis

**CreateIndexStmt:**

![CreateIndexStmt](/media/sqlgram-dev/CreateIndexStmt.png)

**CreateIndexStmtUnique:**

![CreateIndexStmtUnique](/media/sqlgram-dev/CreateIndexStmtUnique.png)

**Identifier:**

![Identifier](/media/sqlgram-dev/Identifier.png)

**IndexTypeOpt:**

![IndexTypeOpt](/media/sqlgram-dev/IndexTypeOpt.png)

**TableName:**

![TableName](/media/sqlgram-dev/TableName.png)

**IndexColNameList:**

![IndexColNameList](/media/sqlgram-dev/IndexColNameList.png)

**IndexOptionList:**

![IndexOptionList](/media/sqlgram-dev/IndexOptionList.png)

**IndexOption:**

![IndexOption](/media/sqlgram-dev/IndexOption.png)

## Examples

```sql
mysql> CREATE TABLE t1 (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, c1 INT NOT NULL);
Query OK, 0 rows affected (0.10 sec)

mysql> INSERT INTO t1 (c1) VALUES (1),(2),(3),(4),(5);
Query OK, 5 rows affected (0.02 sec)
Records: 5  Duplicates: 0  Warnings: 0

mysql> EXPLAIN SELECT * FROM t1 WHERE c1 = 3;
+---------------------+----------+------+-------------------------------------------------------------+
| id                  | count    | task | operator info                                               |
+---------------------+----------+------+-------------------------------------------------------------+
| TableReader_7       | 10.00    | root | data:Selection_6                                            |
| └─Selection_6       | 10.00    | cop  | eq(test.t1.c1, 3)                                           |
|   └─TableScan_5     | 10000.00 | cop  | table:t1, range:[-inf,+inf], keep order:false, stats:pseudo |
+---------------------+----------+------+-------------------------------------------------------------+
3 rows in set (0.00 sec)

mysql> CREATE INDEX c1 ON t1 (c1);
Query OK, 0 rows affected (0.30 sec)

mysql> EXPLAIN SELECT * FROM t1 WHERE c1 = 3;
+-------------------+-------+------+-----------------------------------------------------------------+
| id                | count | task | operator info                                                   |
+-------------------+-------+------+-----------------------------------------------------------------+
| IndexReader_6     | 10.00 | root | index:IndexScan_5                                               |
| └─IndexScan_5     | 10.00 | cop  | table:t1, index:c1, range:[3,3], keep order:false, stats:pseudo |
+-------------------+-------+------+-----------------------------------------------------------------+
2 rows in set (0.00 sec)

mysql> ALTER TABLE t1 DROP INDEX c1;
Query OK, 0 rows affected (0.30 sec)

mysql> CREATE UNIQUE INDEX c1 ON t1 (c1);
Query OK, 0 rows affected (0.31 sec)
```

## Expression index

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

Expression indexes have the same syntax and limitations as in MySQL. They are implemented by building indexes on generated virtual columns that are invisible, so the supported expressions inherit all [limitations of virtual generated columns](/reference/sql/generated-columns.md#limitations).

Currently, the optimizer can use the indexed expressions when the expressions are only in the `FIELD` clause, `WHERE` clause, and `ORDER BY` clause. The `GROUP BY` clause will be supported in future updates.

## Associated session variables

The global variables associated with the `CREATE INDEX` statement are `tidb_ddl_reorg_worker_cnt`, `tidb_ddl_reorg_batch_size` and `tidb_ddl_reorg_priority`. Refer to [TiDB-specific system variables](/reference/configuration/tidb-server/tidb-specific-variables.md#tidb_ddl_reorg_worker_cnt) for details.

## MySQL compatibility

* `FULLTEXT`, `HASH` and `SPATIAL` indexes are not supported.
* Descending indexes are not supported (similar to MySQL 5.7).
* Adding the primary key constraint to a table is not supported by default. You can enable the feature by setting the `alter-primary-key` configuration item to `true`. For details, see [alter-primary-key](/reference/configuration/tidb-server/configuration-file.md#alter-primary-key).

## See also

* [ADD INDEX](/reference/sql/statements/add-index.md)
* [DROP INDEX](/reference/sql/statements/drop-index.md)
* [RENAME INDEX](/reference/sql/statements/rename-index.md)
* [ADD COLUMN](/reference/sql/statements/add-column.md)
* [CREATE TABLE](/reference/sql/statements/create-table.md)
* [EXPLAIN](/reference/sql/statements/explain.md)
