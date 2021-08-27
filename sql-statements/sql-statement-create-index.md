---
title: CREATE INDEX
summary: CREATE INDEX 在 TiDB 中的使用概况
---

# CREATE INDEX

`CREATE INDEX` 语句用于在已有表中添加新索引，功能等同于 `ALTER TABLE .. ADD INDEX`。包含该语句提供了 MySQL 兼容性。

## 语法图

```ebnf+diagram
CreateIndexStmt ::=
    'CREATE' IndexKeyTypeOpt 'INDEX' IfNotExists Identifier IndexTypeOpt 'ON' TableName '(' IndexPartSpecificationList ')' IndexOptionList IndexLockAndAlgorithmOpt

IndexKeyTypeOpt ::=
    ( 'UNIQUE' | 'SPATIAL' | 'FULLTEXT' )?

IfNotExists ::=
    ( 'IF' 'NOT' 'EXISTS' )?

IndexTypeOpt ::=
    IndexType?

IndexPartSpecificationList ::=
    IndexPartSpecification ( ',' IndexPartSpecification )*

IndexOptionList ::=
    IndexOption*

IndexLockAndAlgorithmOpt ::=
    ( LockClause AlgorithmClause? | AlgorithmClause LockClause? )?

IndexType ::=
    ( 'USING' | 'TYPE' ) IndexTypeName

IndexPartSpecification ::=
    ( ColumnName OptFieldLen | '(' Expression ')' ) Order

IndexOption ::=
    'KEY_BLOCK_SIZE' '='? LengthNum
|   IndexType
|   'WITH' 'PARSER' Identifier
|   'COMMENT' stringLit
|   IndexInvisible

IndexTypeName ::=
    'BTREE'
|   'HASH'
|   'RTREE'

ColumnName ::=
    Identifier ( '.' Identifier ( '.' Identifier )? )?

OptFieldLen ::=
    FieldLen?

IndexNameList ::=
    ( Identifier | 'PRIMARY' )? ( ',' ( Identifier | 'PRIMARY' ) )*

KeyOrIndex ::=
    'Key' | 'Index'
```

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
| IndexReader_6          | 10.00   | root      |                        | index:IndexRangeScan_5                      |
| └─IndexRangeScan_5     | 10.00   | cop[tikv] | table:t1, index:c1(c1) | range:[3,3], keep order:false, stats:pseudo |
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

{{< copyable "sql" >}}

```sql
CREATE UNIQUE INDEX c1 ON t1 (c1);
```

```
Query OK, 0 rows affected (0.31 sec)
```

## 表达式索引

在一些场景中，查询的条件往往是基于某个表达式进行过滤。在这些场景中，一般的索引不能生效，执行查询只能遍历整个表，导致查询性能较差。表达式索引是一种特殊的索引，能将索引建立于表达式上。在创建了表达式索引后，基于表达式的查询便可以使用上索引，极大提升查询的性能。

假设要基于 `lower(col1)` 这个表达式建立索引，示例的 SQL 语句如下：

{{< copyable "sql" >}}

```sql
CREATE INDEX idx1 ON t1 (lower(col1));
```

或者等价的语句：

{{< copyable "sql" >}}

```sql
ALTER TABLE t1 ADD INDEX idx1(lower(col1));
```

还可以在建表的同时指定表达式索引：

{{< copyable "sql" >}}

```sql
CREATE TABLE t1(col1 char(10), col2 char(10), key index(lower(col1)));
```

删除表达式索引与删除普通索引的方法一致：

{{< copyable "sql" >}}

```sql
DROP INDEX idx1 ON t1;
```

> **注意：**
> 
> 表达式索引涉及众多表达式。为了确保正确性，当前仅允许经充分测试的一部分函数用于创建表达式索引，即生产环境中仅允许表达式中包含这些函数。这些函数可以通过查询变量 `tidb_allow_function_for_expression_index` 得到。在后续版本中，这些函数会持续增加。
> 
> {{< copyable "sql" >}}
>
> ```sql
> mysql> select @@tidb_allow_function_for_expression_index;
> +--------------------------------------------+
> | @@tidb_allow_function_for_expression_index |
> +--------------------------------------------+
> | lower, md5, reverse, upper, vitess_hash    |
> +--------------------------------------------+
> 1 row in set (0.00 sec)
> ```
> 
> 对于以上变量返回结果之外的函数，由于未完成充分测试，当前仍为实验特性，不建议在生产环境中使用。其他的表达式例如运算符、`cast` 和 `case when` 也同样为实验特性，不建议在生产环境中使用。如果仍然希望使用，可以在 [TiDB 配置文件](/tidb-configuration-file.md#allow-expression-index-从-v400-版本开始引入)中进行以下设置：
> 
> {{< copyable "sql" >}}
> 
> ```sql
> allow-expression-index = true
> ```
>
> 表达式索引不能为主键。
>
> 表达式索引中的表达式不能包含以下内容：
>
> - 易变函数，例如 `rand()` 和 `now()` 等。
> - 系统变量以及用户变量。
> - 子查询。
> - AUTO_INCREMENT 属性的列。一个例外是设置系统变量 `tidb_enable_auto_increment_in_generated` 为 `true` 后，可以去掉该限制。
> - 窗口函数。
> - row 函数。例如 `create table t (j json, key k (((j,j))));`。
> - 聚合函数。
> 
> 表达式索引将隐式占用名字，`_V$_{index_name}_{index_offset}`，如果已有相同名字的列存在，创建表达式索引将报错。如果后续新增相同名字的列，也会报错。
>
> 在表达式索引中，表达式的函数参数个数必须正确。
> 
> 当索引的表达式使用了字符串相关的函数时，受返回类型以及其长度的影响，创建表达式索引可能会失败。这时可以使用 `cast()` 函数显式指定返回的类型以及长度。例如表达式 `repeat(a, 3)`，为了能根据该表达式建立表达式索引，需要将表达式改写为 `cast(repeat(a, 3) as char(20))` 这样的形式。

当查询语句中的表达式与表达式索引中的表达式一致时，优化器可以为该查询选择使用表达式索引。依赖于统计信息，某些情况下优化器不一定选择表达式索引。这时可以通过 hint 指定强制使用表达式索引。

在以下示例中，假设建立在 `lower(col1)` 表达式上的索引为 `idx`。

当读取的结果为相同的表达式时，可以使用表达式索引。例如：

{{< copyable "sql" >}}

```sql
SELECT lower(col1) FROM t;
```

当过滤的条件中有相同的表达式时，可以使用表达式索引。例如：

{{< copyable "sql" >}}

```sql
SELECT * FROM t WHERE lower(col1) = "a";
SELECT * FROM t WHERE lower(col1) > "a";
SELECT * FROM t WHERE lower(col1) BETWEEN "a" AND "b";
SELECT * FROM t WHERE lower(col1) in ("a", "b");
SELECT * FROM t WHERE lower(col1) > "a" AND lower(col1) < "b";
SELECT * FROM t WHERE lower(col1) > "b" OR lower(col1) < "a";
```

当查询按照相同的表达式进行排序时，可以使用表达式索引。例如：

{{< copyable "sql" >}}

```sql
SELECT * FROM t ORDER BY lower(col1);
```

当聚合函数或者 `GROUP BY` 中包含相同的表达式时，可以使用表达式索引。例如：

{{< copyable "sql" >}}

```sql
SELECT max(lower(col1)) FROM t；
SELECT min(col1) FROM t GROUP BY lower(col1);
```

要查看表达式索引对应的表达式，可执行 `show index` 或查看系统表 `information_schema.tidb_indexes` 以及 `information_schema.STATISTICS` 表，输出中 `Expression` 这一列显示对应的表达式。对于非表达式索引，该列的值为 `NULL`。

维护表达式索引的代价比一般的索引更高，因为在插入或者更新每一行时都需要计算出表达式的值。因为表达式的值已经存储在索引中，所以当优化器选择表达式索引时，表达式的值就不需要再计算。因此，当查询速度比插入速度和更新速度更重要时，可以考虑建立表达式索引。

表达式索引的语法和限制与 MySQL 相同，是通过将索引建立在隐藏的虚拟生成列 (generated virtual column) 上来实现的。因此所支持的表达式继承了虚拟生成列的所有[限制](/generated-columns.md#生成列的局限性)。

## 不可见索引

不可见索引 (Invisible Indexes) 不会被查询优化器使用：

```sql
CREATE TABLE t1 (c1 INT, c2 INT, UNIQUE(c2));
CREATE UNIQUE INDEX c1 ON t1 (c1) INVISIBLE;
```

具体可以参考 [`ALTER INDEX`](/sql-statements/sql-statement-alter-index.md)。

## 相关系统变量

和 `CREATE INDEX` 语句相关的系统变量有 `tidb_ddl_reorg_worker_cnt` 、`tidb_ddl_reorg_batch_size` 、`tidb_ddl_reorg_priority` 和 `tidb_enable_auto_increment_in_generated`，具体可以参考[系统变量](/system-variables.md#tidb_ddl_reorg_worker_cnt)。

## MySQL 兼容性

* 不支持 `FULLTEXT`，`HASH` 和 `SPATIAL` 索引。
* 不支持降序索引 （类似于 MySQL 5.7）。
* 无法向表中添加 `CLUSTERED` 类型的 `PRIMARY KEY`。要了解关于 `CLUSTERED` 主键的详细信息，请参考[聚簇索引](/clustered-indexes.md)。
* 表达式索引与视图存在兼容性问题。通过视图进行查询时，无法使用上表达式索引。
* 表达式索引与 Binding 存在兼容性问题。当表达式索引中的表达式存在常量时，对应查询所建的 Binding 会扩大范围。假设表达式索引中的表达式为 `a+1`，对应的查询条件为 `a+1 > 2`。则建立的 Binding 为 `a+? > ?`，这会导致像 `a+2 > 2` 这样的查询也会强制使用表达式索引，得到一个较差的执行计划。这同样影响 SQL Plan Management (SPM) 中的捕获和演进功能。

## 另请参阅

* [索引的选择](/choose-index.md)
* [错误索引的解决方案](/wrong-index-solution.md)
* [ADD INDEX](/sql-statements/sql-statement-add-index.md)
* [DROP INDEX](/sql-statements/sql-statement-drop-index.md)
* [RENAME INDEX](/sql-statements/sql-statement-rename-index.md)
* [ALTER INDEX](/sql-statements/sql-statement-alter-index.md)
* [ADD COLUMN](/sql-statements/sql-statement-add-column.md)
* [CREATE TABLE](/sql-statements/sql-statement-create-table.md)
* [EXPLAIN](/sql-statements/sql-statement-explain.md)
