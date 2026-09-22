---
title: ADD INDEX
summary: TiDB 数据库中 ADD INDEX 的使用概况。
aliases: ['/docs-cn/dev/sql-statements/sql-statement-add-index/','/docs-cn/dev/reference/sql/statements/add-index/']
---

# ADD INDEX

`ALTER TABLE.. ADD INDEX` 语句用于在已有表中添加一个索引。在 TiDB 中，`ADD INDEX` 为在线操作，不会阻塞表中的数据读写。

> **Tip:**
>
> 你可以使用 [TiDB 分布式执行框架](/tidb-distributed-execution-framework.md)加速该语句的执行。

> **警告：**
>
> - 在升级 TiDB 集群的过程中，**请勿执行** DDL 语句，否则可能会出现行为未定义的问题。
> - 集群中有 DDL 语句正在被执行时（通常为 `ADD INDEX` 和列类型变更等耗时较久的 DDL 语句），**请勿进行**升级操作。在升级前，建议使用 [`ADMIN SHOW DDL`](/sql-statements/sql-statement-admin-show-ddl.md) 命令查看集群中是否有正在进行的 DDL Job。如需升级，请等待 DDL 执行完成或使用 [`ADMIN CANCEL DDL`](/sql-statements/sql-statement-admin-cancel-ddl.md) 命令取消该 DDL Job 后再进行升级。
> 
> 从 TiDB v7.1 版本升级至更高的版本时，可以不遵循以上限制，建议参考[平滑升级 TiDB 的限制](/smooth-upgrade-tidb.md#使用限制)。

## 语法图

```ebnf+diagram
AlterTableStmt
         ::= 'ALTER' 'IGNORE'? 'TABLE' TableName AddIndexSpec ( ',' AddIndexSpec )*

AddIndexSpec
         ::= 'ADD' ( ( 'PRIMARY' 'KEY' | ( 'KEY' | 'INDEX' ) 'IF NOT EXISTS'? | 'UNIQUE' ( 'KEY' | 'INDEX' )? ) ( ( Identifier? 'USING' | Identifier 'TYPE' ) IndexType )? | 'FULLTEXT' ( 'KEY' | 'INDEX' )? IndexName ) '(' IndexPartSpecification ( ',' IndexPartSpecification )* ')' IndexOption*

IndexPartSpecification
         ::= ( ColumnName ( '(' LengthNum ')' )? | '(' Expression ')' ) ( 'ASC' | 'DESC' )

IndexOption
         ::= 'KEY_BLOCK_SIZE' '='? LengthNum
           | 'USING' IndexType
           | 'WITH' 'PARSER' Identifier
           | 'COMMENT' stringLit
           | 'VISIBLE'
           | 'INVISIBLE'
           | 'GLOBAL'
           | 'LOCAL'
           | 'WHERE' Expression

IndexType
         ::= 'BTREE'
           | 'HASH'
           | 'RTREE'
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
ALTER TABLE t1 ADD INDEX (c1);
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

## 部分索引 <span class="version-mark">从 v8.5.7 和 v9.0.0 开始引入</span>

部分索引是基于表中部分行构建的索引。在添加部分索引时，你可以使用条件表达式（称为谓词）来定义这些行的子集。该索引仅包含满足谓词条件的行对应的索引条目。

### 适用场景

在以下场景中，使用部分索引有助于提升查询性能或降低索引维护开销：

- **选择性过滤**：当你经常基于特定条件查询一小部分行时，可以使用部分索引。对于满足部分索引谓词的查询，TiDB 可以使用部分索引来避免扫描无关的行，并减少索引占用的存储空间。
- **条件唯一性**：当你只需要对满足特定条件的行强制执行唯一性约束时，可以使用唯一部分索引，避免对整张表应用唯一性约束。
- **减少 DML 开销**：当许多 `INSERT`、`UPDATE` 或 `DELETE` 操作会影响不需要被索引的行时，可以使用部分索引。与维护完整索引相比，维护部分索引可以减少索引维护开销。

### 添加部分索引

你可以通过在索引定义中添加 `WHERE` 子句来添加部分索引。例如：

```sql
CREATE TABLE t1 (c1 INT, c2 INT, c3 TEXT);
ALTER TABLE t1 ADD INDEX idx1 (c1) WHERE c2 > 10;
```

你也可以添加唯一部分索引：

```sql
ALTER TABLE t1 ADD UNIQUE INDEX idx2 (c1, c2) WHERE c3 = 'abc';
```

### 使用示例

以下示例演示如何有效地使用部分索引。

创建包含用户数据的表：

```sql
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    status VARCHAR(20),
    created_at DATETIME,
    score INT
);
```

为常见查询模式添加部分索引：

```sql
ALTER TABLE users ADD INDEX idx_active_users (name) WHERE status = 'active';
ALTER TABLE users ADD INDEX idx_high_score_users (created_at) WHERE score > 1000;
ALTER TABLE users ADD INDEX idx_pending_status (status) WHERE status = 'pending';
```

然后以下查询可以使用部分索引：

```sql
mysql> EXPLAIN SELECT * FROM users WHERE status = 'active' AND name = 'John';
+-------------------------------+---------+-----------+-------------------------------------------+-------------------------------------------------------+
| id                            | estRows | task      | access object                             | operator info                                         |
+-------------------------------+---------+-----------+-------------------------------------------+-------------------------------------------------------+
| IndexLookUp_9                 | 1.00    | root      |                                           |                                                       |
| ├─IndexRangeScan_6(Build)     | 10.00   | cop[tikv] | table:users, index:idx_active_users(name) | range:["John","John"], keep order:false, stats:pseudo |
| └─Selection_8(Probe)          | 1.00    | cop[tikv] |                                           | eq(test.users.status, "active")                       |
|   └─TableRowIDScan_7          | 10.00   | cop[tikv] | table:users                               | keep order:false, stats:pseudo                        |
+-------------------------------+---------+-----------+-------------------------------------------+-------------------------------------------------------+
4 rows in set (0.00 sec)

mysql> EXPLAIN SELECT * FROM users WHERE status = 'active' ORDER BY name;
+-------------------------------+----------+-----------+-------------------------------------------+---------------------------------+
| id                            | estRows  | task      | access object                             | operator info                   |
+-------------------------------+----------+-----------+-------------------------------------------+---------------------------------+
| IndexLookUp_18                | 10.00    | root      |                                           |                                 |
| ├─IndexFullScan_15(Build)     | 10000.00 | cop[tikv] | table:users, index:idx_active_users(name) | keep order:true, stats:pseudo   |
| └─Selection_17(Probe)         | 10.00    | cop[tikv] |                                           | eq(test.users.status, "active") |
|   └─TableRowIDScan_16         | 10000.00 | cop[tikv] | table:users                               | keep order:false, stats:pseudo  |
+-------------------------------+----------+-----------+-------------------------------------------+---------------------------------+
4 rows in set (0.00 sec)

mysql> EXPLAIN SELECT * FROM users WHERE score > 10000 ORDER BY created_at;
+-------------------------------+----------+-----------+-----------------------------------------------------+--------------------------------+
| id                            | estRows  | task      | access object                                       | operator info                  |
+-------------------------------+----------+-----------+-----------------------------------------------------+--------------------------------+
| IndexLookUp_18                | 3333.33  | root      |                                                     |                                |
| ├─IndexFullScan_15(Build)     | 10000.00 | cop[tikv] | table:users, index:idx_high_score_users(created_at) | keep order:true, stats:pseudo  |
| └─Selection_17(Probe)         | 3333.33  | cop[tikv] |                                                     | gt(test.users.score, 10000)     |
|   └─TableRowIDScan_16         | 10000.00 | cop[tikv] | table:users                                         | keep order:false, stats:pseudo |
+-------------------------------+----------+-----------+-----------------------------------------------------+--------------------------------+
4 rows in set (0.00 sec)

mysql> EXPLAIN SELECT * FROM users WHERE status = 'pending';
+-------------------------------+---------+-----------+-----------------------------------------------+-------------------------------------------------------------+
| id                            | estRows | task      | access object                                 | operator info                                               |
+-------------------------------+---------+-----------+-----------------------------------------------+-------------------------------------------------------------+
| IndexLookUp_7                 | 10.00   | root      |                                               |                                                             |
| ├─IndexRangeScan_5(Build)     | 10.00   | cop[tikv] | table:users, index:idx_pending_status(status) | range:["pending","pending"], keep order:false, stats:pseudo |
| └─TableRowIDScan_6(Probe)     | 10.00   | cop[tikv] | table:users                                   | keep order:false, stats:pseudo                              |
+-------------------------------+---------+-----------+-----------------------------------------------+-------------------------------------------------------------+
3 rows in set (0.00 sec)
```

如果查询谓词不满足部分索引定义的条件，即使使用 hint，TiDB 也不会选择该部分索引。例如，以下语句无法使用部分索引 `idx_high_score_users`，因为查询谓词 `score > 100` 不满足部分索引定义 `score > 1000`：

```sql
mysql> EXPLAIN SELECT * FROM users USE INDEX(idx_high_score_users) WHERE score > 100 ORDER BY created_at;
+---------------------------+----------+-----------+---------------+--------------------------------+
| id                        | estRows  | task      | access object | operator info                  |
+---------------------------+----------+-----------+---------------+--------------------------------+
| Sort_5                    | 3333.33  | root      |               | test.users.created_at          |
| └─TableReader_10          | 3333.33  | root      |               | data:Selection_9               |
|   └─Selection_9           | 3333.33  | cop[tikv] |               | gt(test.users.score, 100)      |
|     └─TableFullScan_8     | 10000.00 | cop[tikv] | table:users   | keep order:false, stats:pseudo |
+---------------------------+----------+-----------+---------------+--------------------------------+
```

### 限制

- 部分索引的 `WHERE` 子句支持基本比较运算符（`=`、`!=`、`<`、`<=`、`>`、`>=`）、`IS NULL`、`IS NOT NULL` 和包含常量值的 `IN` 谓词。
- 谓词中的列和常量值必须具有相同的数据类型。
- 谓词只能引用同一表中的列。
- 不能在表达式索引上创建部分索引。

## MySQL 兼容性

* 为了兼容 MySQL，TiDB 在语法上支持 `HASH`、`BTREE` 和 `RTREE` 等索引类型，但会忽略它们。
* 不支持 `SPATIAL` 索引。
* TiDB 支持解析 `FULLTEXT` 语法，但不支持使用 `FULLTEXT` 索引。
* 不支持降序索引（类似于 MySQL 5.7）。
* 无法向表中添加 `CLUSTERED` 类型的 `PRIMARY KEY`。要了解关于 `CLUSTERED` 主键的详细信息，请参考[聚簇索引](/clustered-indexes.md)。
* TiDB 对[分区表](/partitioned-table.md)进行了扩展。你可以指定 `GLOBAL` 索引选项将 `PRIMARY KEY` 或 `UNIQUE INDEX` 设置为[全局索引](/global-indexes.md)。该扩展与 MySQL 不兼容。

## 另请参阅

* [索引的选择](/choose-index.md)
* [错误索引的解决方案](/wrong-index-solution.md)
* [CREATE INDEX](/sql-statements/sql-statement-create-index.md)
* [DROP INDEX](/sql-statements/sql-statement-drop-index.md)
* [RENAME INDEX](/sql-statements/sql-statement-rename-index.md)
* [ALTER INDEX](/sql-statements/sql-statement-alter-index.md)
* [ADD COLUMN](/sql-statements/sql-statement-add-column.md)
* [CREATE TABLE](/sql-statements/sql-statement-create-table.md)
* [EXPLAIN](/sql-statements/sql-statement-explain.md)
* [TiDB 分布式执行框架](/tidb-distributed-execution-framework.md)
