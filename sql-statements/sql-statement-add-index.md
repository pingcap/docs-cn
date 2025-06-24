---
title: ADD INDEX | TiDB SQL 语句参考
summary: TiDB 数据库中 ADD INDEX 的使用概述。
---

# ADD INDEX

`ALTER TABLE.. ADD INDEX` 语句用于向现有表添加索引。在 TiDB 中，这是一个在线操作，这意味着添加索引时不会阻塞对表的读取或写入操作。

> **提示：**
>
> 可以使用 [TiDB 分布式执行框架 (DXF)](/tidb-distributed-execution-framework.md) 来加速此语句的执行。

<CustomContent platform="tidb">

> **警告：**
>
> - 在集群中执行 DDL 语句时（通常是耗时的 DDL 语句，如 `ADD INDEX` 和列类型更改），**不要**升级 TiDB 集群。
> - 在升级之前，建议使用 [`ADMIN SHOW DDL`](/sql-statements/sql-statement-admin-show-ddl.md) 命令检查 TiDB 集群是否有正在进行的 DDL 任务。如果集群有 DDL 任务，要升级集群，请等待 DDL 执行完成，或使用 [`ADMIN CANCEL DDL`](/sql-statements/sql-statement-admin-cancel-ddl.md) 命令取消 DDL 任务后再升级集群。
> - 此外，在集群升级期间，**不要**执行任何 DDL 语句。否则，可能会出现未定义行为的问题。
>
> 当你将 TiDB 从 v7.1.0 升级到更高版本时，可以忽略上述限制。详情请参见 [TiDB 平滑升级的限制](/smooth-upgrade-tidb.md)。

</CustomContent>

## 语法

```ebnf+diagram
AlterTableStmt
         ::= 'ALTER' 'IGNORE'? 'TABLE' TableName AddIndexSpec ( ',' AddIndexSpec )*

AddIndexSpec
         ::= 'ADD' ( ( 'PRIMARY' 'KEY' | ( 'KEY' | 'INDEX' ) 'IF NOT EXISTS'? | 'UNIQUE' ( 'KEY' | 'INDEX' )? ) ( ( Identifier? 'USING' | Identifier 'TYPE' ) IndexType )? | 'FULLTEXT' ( 'KEY' | 'INDEX' )? IndexName ) '(' IndexPartSpecification ( ',' IndexPartSpecification )* ')' IndexOption*

IndexPartSpecification
         ::= ( ColumnName ( '(' LengthNum ')' )? | '(' Expression ')' ) ( 'ASC' | 'DESC' )

IndexOption
         ::= 'KEY_BLOCK_SIZE' '='? LengthNum
           | IndexType
           | 'WITH' 'PARSER' Identifier
           | 'COMMENT' stringLit
           | 'VISIBLE'
           | 'INVISIBLE'

IndexType
         ::= 'BTREE'
           | 'HASH'
           | 'RTREE'
```

## 示例

```sql
mysql> CREATE TABLE t1 (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, c1 INT NOT NULL);
Query OK, 0 rows affected (0.11 sec)

mysql> INSERT INTO t1 (c1) VALUES (1),(2),(3),(4),(5);
Query OK, 5 rows affected (0.03 sec)
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

mysql> ALTER TABLE t1 ADD INDEX (c1);
Query OK, 0 rows affected (0.30 sec)

mysql> EXPLAIN SELECT * FROM t1 WHERE c1 = 3;
+------------------------+---------+-----------+------------------------+---------------------------------------------+
| id                     | estRows | task      | access object          | operator info                               |
+------------------------+---------+-----------+------------------------+---------------------------------------------+
| IndexReader_6          | 0.01    | root      |                        | index:IndexRangeScan_5                      |
| └─IndexRangeScan_5     | 0.01    | cop[tikv] | table:t1, index:c1(c1) | range:[3,3], keep order:false, stats:pseudo |
+------------------------+---------+-----------+------------------------+---------------------------------------------+
2 rows in set (0.00 sec)
```

## MySQL 兼容性

* TiDB 在语法上接受 `HASH`、`BTREE` 和 `RTREE` 等索引类型以与 MySQL 兼容，但会忽略这些类型。
* 不支持 `SPATIAL` 索引。
* TiDB 支持解析 `FULLTEXT` 语法但不支持使用 `FULLTEXT` 索引。
* 不支持降序索引（类似于 MySQL 5.7）。
* 不支持向表添加 `CLUSTERED` 类型的主键。关于 `CLUSTERED` 类型的主键的更多详情，请参考[聚簇索引](/clustered-indexes.md)。

## 另请参阅

* [索引选择](/choose-index.md)
* [错误索引解决方案](/wrong-index-solution.md)
* [CREATE INDEX](/sql-statements/sql-statement-create-index.md)
* [DROP INDEX](/sql-statements/sql-statement-drop-index.md)
* [RENAME INDEX](/sql-statements/sql-statement-rename-index.md)
* [ALTER INDEX](/sql-statements/sql-statement-alter-index.md)
* [ADD COLUMN](/sql-statements/sql-statement-add-column.md)
* [CREATE TABLE](/sql-statements/sql-statement-create-table.md)
* [EXPLAIN](/sql-statements/sql-statement-explain.md)
* [TiDB 分布式执行框架 (DXF)](/tidb-distributed-execution-framework.md)
