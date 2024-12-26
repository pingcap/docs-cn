---
title: CREATE INDEX
summary: CREATE INDEX 在 TiDB 中的使用概况
---

# CREATE INDEX

`CREATE INDEX` 语句用于在已有表中添加新索引，功能等同于 [`ALTER TABLE .. ADD INDEX`](/sql-statements/sql-statement-alter-table.md)，提供了 MySQL 兼容性。

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
|   ("VISIBLE" | "INVISIBLE")

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

```sql
CREATE TABLE t1 (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, c1 INT NOT NULL);
```

```
Query OK, 0 rows affected (0.10 sec)
```

```sql
INSERT INTO t1 (c1) VALUES (1),(2),(3),(4),(5);
```

```
Query OK, 5 rows affected (0.02 sec)
Records: 5  Duplicates: 0  Warnings: 0
```

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

```sql
CREATE INDEX c1 ON t1 (c1);
```

```
Query OK, 0 rows affected (0.30 sec)
```

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

```sql
ALTER TABLE t1 DROP INDEX c1;
```

```
Query OK, 0 rows affected (0.30 sec)
```

```sql
CREATE UNIQUE INDEX c1 ON t1 (c1);
```

```
Query OK, 0 rows affected (0.31 sec)
```

## 表达式索引

在一些场景中，查询的条件往往是基于某个表达式进行过滤。在这些场景中，一般的索引不能生效，执行查询只能遍历整个表，导致查询性能较差。表达式索引是一种特殊的索引，能将索引建立于表达式上。在创建了表达式索引后，基于表达式的查询便可以使用上索引，极大提升查询的性能。

假设要基于 `LOWER(col1)` 这个表达式建立索引，示例的 SQL 语句如下：

```sql
CREATE INDEX idx1 ON t1 ((LOWER(col1)));
```

或者等价的语句：

```sql
ALTER TABLE t1 ADD INDEX idx1((LOWER(col1)));
```

还可以在建表的同时指定表达式索引：

```sql
CREATE TABLE t1 (
    col1 CHAR(10),
    col2 CHAR(10),
    INDEX ((LOWER(col1)))
);
```

> **注意：**
>
> 表达式索引中的表达式需要用 `(` 和 `)` 包围起来，否则会报语法错误。

删除表达式索引与删除普通索引的方法一致：

```sql
DROP INDEX idx1 ON t1;
```

表达式索引涉及众多表达式。为了确保正确性，当前仅允许经充分测试的一部分函数用于创建表达式索引，即生产环境中仅允许表达式中包含这些函数。这些函数可以通过查询变量 [`tidb_allow_function_for_expression_index`](/system-variables.md#tidb_allow_function_for_expression_index-从-v520-版本开始引入) 得到。在后续版本中，这些函数会持续增加。目前允许的函数如下：

- [`JSON_ARRAY()`](/functions-and-operators/json-functions.md)
- [`JSON_ARRAY_APPEND()`](/functions-and-operators/json-functions.md)
- [`JSON_ARRAY_INSERT()`](/functions-and-operators/json-functions.md)
- [`JSON_CONTAINS()`](/functions-and-operators/json-functions.md)
- [`JSON_CONTAINS_PATH()`](/functions-and-operators/json-functions.md)
- [`JSON_DEPTH()`](/functions-and-operators/json-functions.md)
- [`JSON_EXTRACT()`](/functions-and-operators/json-functions.md)
- [`JSON_INSERT()`](/functions-and-operators/json-functions.md)
- [`JSON_KEYS()`](/functions-and-operators/json-functions.md)
- [`JSON_LENGTH()`](/functions-and-operators/json-functions.md)
- [`JSON_MERGE_PATCH()`](/functions-and-operators/json-functions.md)
- [`JSON_MERGE_PRESERVE()`](/functions-and-operators/json-functions.md)
- [`JSON_OBJECT()`](/functions-and-operators/json-functions.md)
- [`JSON_PRETTY()`](/functions-and-operators/json-functions.md)
- [`JSON_QUOTE()`](/functions-and-operators/json-functions.md)
- [`JSON_REMOVE()`](/functions-and-operators/json-functions.md)
- [`JSON_REPLACE()`](/functions-and-operators/json-functions.md)
- [`JSON_SCHEMA_VALID()`](/functions-and-operators/json-functions/json-functions-validate.md)
- [`JSON_SEARCH()`](/functions-and-operators/json-functions.md)
- [`JSON_SET()`](/functions-and-operators/json-functions.md)
- [`JSON_STORAGE_SIZE()`](/functions-and-operators/json-functions.md)
- [`JSON_TYPE()`](/functions-and-operators/json-functions.md)
- [`JSON_UNQUOTE()`](/functions-and-operators/json-functions.md)
- [`JSON_VALID()`](/functions-and-operators/json-functions.md)
- [`LOWER()`](/functions-and-operators/string-functions.md#lower)
- [`MD5()`](/functions-and-operators/encryption-and-compression-functions.md)
- [`REVERSE()`](/functions-and-operators/string-functions.md#reverse)
- [`TIDB_SHARD()`](/functions-and-operators/tidb-functions.md#tidb_shard)
- [`UPPER()`](/functions-and-operators/string-functions.md#upper)
- [`VITESS_HASH()`](/functions-and-operators/tidb-functions.md)

对于以上列表之外的函数，由于未完成充分测试，当前仍为实验特性，不建议在生产环境中使用。其他的表达式例如运算符、`CAST` 和 `CASE WHEN` 也同样为实验特性，不建议在生产环境中使用。如果仍然希望使用，可以在 [TiDB 配置文件](/tidb-configuration-file.md#allow-expression-index-从-v400-版本开始引入)中进行以下设置：

```sql
allow-expression-index = true
```

> **注意：**
>
> 表达式索引不能为主键。
>
> 表达式索引中的表达式不能包含以下内容：
>
> - 易变函数，例如 `RAND()` 和 `NOW()` 等。
> - [系统变量](/system-variables.md)以及[用户变量](/user-defined-variables.md)。
> - 子查询。
> - [`AUTO_INCREMENT`](/auto-increment.md) 属性的列。一个例外是设置系统变量 [`tidb_enable_auto_increment_in_generated`](/system-variables.md#tidb_enable_auto_increment_in_generated) 为 `true` 后，可以去掉该限制。
> - [窗口函数](/functions-and-operators/window-functions.md)。
> - ROW 函数。例如 `CREATE TABLE t (j JSON, INDEX k (((j,j))));`。
> - [聚合函数](/functions-and-operators/aggregate-group-by-functions.md)。
>
> 表达式索引将隐式占用名字，`_V$_{index_name}_{index_offset}`，如果已有相同名字的列存在，创建表达式索引将报错。如果后续新增相同名字的列，也会报错。
>
> 在表达式索引中，表达式的函数参数个数必须正确。
>
> 当索引的表达式使用了字符串相关的函数时，受返回类型以及其长度的影响，创建表达式索引可能会失败。这时可以使用 `CAST()` 函数显式指定返回的类型以及长度。例如表达式 `REPEAT(a, 3)`，为了能根据该表达式建立表达式索引，需要将表达式改写为 `CAST(REPEAT(a, 3) AS CHAR(20))` 这样的形式。

当查询语句中的表达式与表达式索引中的表达式一致时，优化器可以为该查询选择使用表达式索引。依赖于统计信息，某些情况下优化器不一定选择表达式索引。这时可以通过 hint 指定强制使用表达式索引。

在以下示例中，假设建立在 `LOWER(col1)` 表达式上的索引为 `idx`。

当读取的结果为相同的表达式时，可以使用表达式索引。例如：

```sql
SELECT LOWER(col1) FROM t;
```

当过滤的条件中有相同的表达式时，可以使用表达式索引。例如：

```sql
SELECT * FROM t WHERE LOWER(col1) = "a";
SELECT * FROM t WHERE LOWER(col1) > "a";
SELECT * FROM t WHERE LOWER(col1) BETWEEN "a" AND "b";
SELECT * FROM t WHERE LOWER(col1) IN ("a", "b");
SELECT * FROM t WHERE LOWER(col1) > "a" AND LOWER(col1) < "b";
SELECT * FROM t WHERE LOWER(col1) > "b" OR LOWER(col1) < "a";
```

当查询按照相同的表达式进行排序时，可以使用表达式索引。例如：

```sql
SELECT * FROM t ORDER BY LOWER(col1);
```

当聚合函数或者 `GROUP BY` 中包含相同的表达式时，可以使用表达式索引。例如：

```sql
SELECT MAX(LOWER(col1)) FROM t;
SELECT MIN(col1) FROM t GROUP BY LOWER(col1);
```

要查看表达式索引对应的表达式，可执行 [`SHOW INDEX`](/sql-statements/sql-statement-show-indexes.md) 或查看系统表 [`information_schema.tidb_indexes`](/information-schema/information-schema-tidb-indexes.md) 以及 [`information_schema.STATISTICS`](/information-schema/information-schema-statistics.md) 表，输出中 `Expression` 这一列显示对应的表达式。对于非表达式索引，该列的值为 `NULL`。

维护表达式索引的代价比一般的索引更高，因为在插入或者更新每一行时都需要计算出表达式的值。因为表达式的值已经存储在索引中，所以当优化器选择表达式索引时，表达式的值就不需要再计算。因此，当查询速度比插入速度和更新速度更重要时，可以考虑建立表达式索引。

表达式索引的语法和限制与 MySQL 相同，是通过将索引建立在隐藏的虚拟生成列 (generated virtual column) 上来实现的。因此所支持的表达式继承了虚拟生成列的所有[限制](/generated-columns.md#生成列的局限性)。

## 多值索引

多值索引是一种定义在数组列上的二级索引。在普通索引中，一条索引记录对应一条数据记录 (1:1)。而在多值索引中，存在多条索引记录对应一条数据记录 (N:1)。多值索引用于索引 JSON 数组。例如，一个定义在 `zipcode` 字段上的多值索引会对每一个 `zipcode` 中的记录产生一条索引记录。

```json
{
    "user":"Bob",
    "user_id":31,
    "zipcode":[94477,94536]
}
```

### 创建多值索引

创建多值索引与创建表达式索引的方法一致。在索引定义中使用 [`CAST(... AS ... ARRAY)`](/functions-and-operators/cast-functions-and-operators.md#cast) 函数来创建一个多值索引。

```sql
mysql> CREATE TABLE customers (
    id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name CHAR(10),
    custinfo JSON,
    INDEX zips((CAST(custinfo->'$.zipcode' AS UNSIGNED ARRAY)))
);
```

多值索引可以被定义为唯一索引：

```sql
mysql> CREATE TABLE customers (
    id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name CHAR(10),
    custinfo JSON,
    UNIQUE INDEX zips( (CAST(custinfo->'$.zipcode' AS UNSIGNED ARRAY)))
);
```

当被定义为唯一索引时，试图插入重复数据将会报错：

```sql
mysql> INSERT INTO customers VALUES (1, 'pingcap', '{"zipcode": [1,2]}');
Query OK, 1 row affected (0.01 sec)

mysql> INSERT INTO customers VALUES (1, 'pingcap', '{"zipcode": [2,3]}');
ERROR 1062 (23000): Duplicate entry '2' for key 'customers.zips'
```

允许同一条记录存在重复的值，不同记录出现重复值时将报错：

```sql
-- 插入成功
mysql> INSERT INTO t1 VALUES('[1,1,2]');
mysql> INSERT INTO t1 VALUES('[3,3,3,4,4,4]');

-- 插入失败
mysql> INSERT INTO t1 VALUES('[1,2]');
mysql> INSERT INTO t1 VALUES('[2,3]');
```

多值索引也可以被定义为复合索引：

```sql
mysql> CREATE TABLE customers (
    id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name CHAR(10),
    custinfo JSON,
    INDEX zips(name, (CAST(custinfo->'$.zipcode' AS UNSIGNED ARRAY)))
);
```

当被定义为复合索引时，多值部分可以出现在任意位置，但是只能出现一次。

```sql
mysql> CREATE TABLE customers (
    id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name CHAR(10),
    custinfo JSON,
    INDEX zips(name, (CAST(custinfo->'$.zipcode' AS UNSIGNED ARRAY)), (CAST(custinfo->'$.zipcode' AS UNSIGNED ARRAY)))
);
ERROR 1235 (42000): This version of TiDB doesn't yet support 'more than one multi-valued key part per index'.
```

写入的数据必须与多值索引的定义类型完全匹配，否则数据写入失败：

```sql
-- zipcode 字段中的所有元素必须为 UNSIGNED 类型
mysql> INSERT INTO customers VALUES (1, 'pingcap', '{"zipcode": [-1]}');
ERROR 3752 (HY000): Value is out of range for expression index 'zips' at row 1

mysql> INSERT INTO customers VALUES (1, 'pingcap', '{"zipcode": ["1"]}'); -- 与 MySQL 不兼容
ERROR 3903 (HY000): Invalid JSON value for CAST for expression index 'zips'

mysql> INSERT INTO customers VALUES (1, 'pingcap', '{"zipcode": [1]}');
Query OK, 1 row affected (0.00 sec)
```

### 使用多值索引

请参考[索引的选择](/choose-index.md#使用多值索引)。

### 特性与限制

- 如果是空 JSON 数组，则不会有对应的索引记录。
- `CAST(... AS ... ARRAY)` 中的目标类型不能是 `BINARY`、`JSON`、`YEAR`、`FLOAT`、`DECIMAL`。其中源类型必须是 JSON。
- 无法使用多值索引进行排序。
- 只允许在 JSON 数组上建立多值索引。
- 多值索引不可以作为主键或外键。
- 多值索引使用额外的存储空间为：平均每行数组元素个数 * 普通二级索引使用空间。
- 相比于普通索引，DML 会对多值索引产生更多的索引记录的修改，因此多值索引会带来比普通索引更大的性能影响。
- 由于多值索引是一种特殊的表达式索引，因此具有表达式索引的限制。
- 使用备份恢复工具 (BR)、同步工具 (TiCDC)、导入工具 (TiDB Lightning) 无法将定义了多值索引的表备份、同步、导入到低于 v6.6.0 版本的 TiDB。
- 条件复杂的查询有可能无法选择到多值索引，多值索引支持的条件模式请参考[使用多值索引](/choose-index.md#使用多值索引)。

## 不可见索引

默认情况下，不可见索引 (Invisible Indexes) 不会被查询优化器使用：

```sql
CREATE TABLE t1 (c1 INT, c2 INT, UNIQUE(c2));
CREATE UNIQUE INDEX c1 ON t1 (c1) INVISIBLE;
```

从 TiDB v8.0.0 开始，你可以通过修改系统变量 [`tidb_opt_use_invisible_indexes`](/system-variables.md#tidb_opt_use_invisible_indexes-从-v800-版本开始引入)，允许优化器选择不可见索引。

具体可以参考 [`ALTER INDEX`](/sql-statements/sql-statement-alter-index.md)。

## 相关系统变量

和 `CREATE INDEX` 语句相关的系统变量有 `tidb_ddl_enable_fast_reorg`、`tidb_ddl_reorg_worker_cnt` 、`tidb_ddl_reorg_batch_size` 、`tidb_ddl_reorg_priority` 和 `tidb_enable_auto_increment_in_generated`，具体可以参考[系统变量](/system-variables.md#tidb_ddl_reorg_worker_cnt)。

## MySQL 兼容性

* TiDB 支持解析 `FULLTEXT` 语法，但尚不支持使用 `FULLTEXT`、`HASH` 和 `SPATIAL` 索引。
* 为了兼容 MySQL，TiDB 在语法上支持 `HASH`、`BTREE` 和 `RTREE` 等索引类型，但会忽略它们。
* 不支持降序索引 （类似于 MySQL 5.7）。
* 无法向表中添加 `CLUSTERED` 类型的 `PRIMARY KEY`。要了解关于 `CLUSTERED` 主键的详细信息，请参考[聚簇索引](/clustered-indexes.md)。
* 表达式索引与视图存在兼容性问题。通过视图进行查询时，无法使用上表达式索引。
* 表达式索引与 Binding 存在兼容性问题。当表达式索引中的表达式存在常量时，对应查询所建的 Binding 会扩大范围。假设表达式索引中的表达式为 `a+1`，对应的查询条件为 `a+1 > 2`。则建立的 Binding 为 `a+? > ?`，这会导致像 `a+2 > 2` 这样的查询也会强制使用表达式索引，得到一个较差的执行计划。这同样影响 SQL Plan Management (SPM) 中的捕获和演进功能。
* 多值索引写入的数据必须与定义类型完全匹配，否则数据写入失败。详见[创建多值索引](/sql-statements/sql-statement-create-index.md#创建多值索引)。

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
