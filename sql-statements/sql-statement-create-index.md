---
title: CREATE INDEX | TiDB SQL Statement Reference
summary: An overview of the usage of CREATE INDEX for the TiDB database.
aliases: ['/docs/dev/sql-statements/sql-statement-create-index/','/docs/dev/reference/sql/statements/create-index/']
---

# CREATE INDEX

This statement adds a new index to an existing table. It is an alternative syntax to `ALTER TABLE .. ADD INDEX`, and included for MySQL compatibility.

## Synopsis

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

In some scenarios, the filtering condition of a query is based on a certain expression. In these scenarios, the query performance is relatively poor because ordinary indexes cannot take effect, the query can only be executed by scanning the entire table. The expression index is a type of special index that can be created on an expression. Once an expression index is created, TiDB can use the index for the expression-based query, which significantly improves the query performance.

For example, if you want to create an index based on `lower(col1)`, execute the following SQL statement:

{{< copyable "sql" >}}

```sql
CREATE INDEX idx1 ON t1 ((lower(col1)));
```

Or you can execute the following equivalent statement:

{{< copyable "sql" >}}

```sql
ALTER TABLE t1 ADD INDEX idx1((lower(col1)));
```

You can also specify the expression index when you create the table:

{{< copyable "sql" >}}

```sql
CREATE TABLE t1(col1 char(10), col2 char(10), index((lower(col1))));
```

> **Note:**
>
> The expression in an expression index must be surrounded by `(` and `)`. Otherwise, a syntax error is reported.

You can drop an expression index in the same way as dropping an ordinary index:

{{< copyable "sql" >}}

```sql
DROP INDEX idx1 ON t1;
```

Expression index involves various kinds of expressions. To ensure correctness, only some fully tested functions are allowed for creating an expression index. This means that only these functions are allowed in expressions in a production environment. You can get these functions by querying the `tidb_allow_function_for_expression_index` variable. Currently, the allowed functions are as follows:

```
json_array, json_array_append, json_array_insert, json_contains, json_contains_path, json_depth, json_extract, json_insert, json_keys, json_length, json_merge_patch, json_merge_preserve, json_object, json_pretty, json_quote, json_remove, json_replace, json_search, json_set, json_storage_size, json_type, json_unquote, json_valid, lower, md5, reverse, tidb_shard, upper, vitess_hash
```

For the functions that are not included in the above list, those functions are not fully tested and not recommended for a production environment, which can be seen as experimental. Other expressions such as operators, `cast`, and `case when` are also seen as experimental and not recommended for production.

<CustomContent platform="tidb">

If you still want to use those expressions, you can make the following configuration in the [TiDB configuration file](/tidb-configuration-file.md#allow-expression-index-new-in-v400):

{{< copyable "sql" >}}

```sql
allow-expression-index = true
```

</CustomContent>

> **Note:**
>
> An expression index cannot be created on a primary key.
>
> The expression in an expression index cannot contain the following content:
>
> - Volatile functions, such as `rand()` and `now()`.
> - System variables and user variables.
> - Subqueries.
> - `AUTO_INCREMENT` column. You can remove this restriction by setting the value of `tidb_enable_auto_increment_in_generated` (system variable) to `true`.
> - Window functions.
> - ROW functions, such as `create table t (j json, key k (((j,j))));`.
> - Aggregate functions.
>
> An expression index implicitly takes up a name (for example, `_V$_{index_name}_{index_offset}`). If you try to create a new expression index with the name that a column has already had, an error occurs. In addition, if you add a new column with the same name, an error also occurs.
>
> Make sure that the number of function parameters in the expression of an expression index is correct.
>
> When the expression of an index contains a string-related function, affected by the returned type and the length, creating the expression index might fail. In this situation, you can use the `cast()` function to explicitly specify the returned type and the length. For example, to create an expression index based on the `repeat(a, 3)` expression, you need to modify this expression to `cast(repeat(a, 3) as char(20))`.

When the expression in a query statement matches the expression in an expression index, the optimizer can choose the expression index for the query. In some cases, the optimizer might not choose an expression index depending on statistics. In this situation, you can force the optimizer to select an expression index by using optimizer hints.

In the following examples, suppose that you create the expression index `idx` on the expression `lower(col1)`:

If the results of the query statement are the same expressions, the expression index applies. Take the following statement as an example:

{{< copyable "sql" >}}

```sql
SELECT lower(col1) FROM t;
```

If the same expression is included in the filtering conditions, the expression index applies. Take the following statements as an example:

{{< copyable "sql" >}}

```sql
SELECT * FROM t WHERE lower(col1) = "a";
SELECT * FROM t WHERE lower(col1) > "a";
SELECT * FROM t WHERE lower(col1) BETWEEN "a" AND "b";
SELECT * FROM t WHERE lower(col1) in ("a", "b");
SELECT * FROM t WHERE lower(col1) > "a" AND lower(col1) < "b";
SELECT * FROM t WHERE lower(col1) > "b" OR lower(col1) < "a";
```

When the queries are sorted by the same expression, the expression index applies. Take the following statement as an example:

{{< copyable "sql" >}}

```sql
SELECT * FROM t ORDER BY lower(col1);
```

If the same expression is included in the aggregate (`GROUP BY`) functions, the expression index applies. Take the following statements as an example:

{{< copyable "sql" >}}

```sql
SELECT max(lower(col1)) FROM t;
SELECT min(col1) FROM t GROUP BY lower(col1);
```

To see the expression corresponding to the expression index, execute `show index`, or check the system tables `information_schema.tidb_indexes` and the table `information_schema.STATISTICS`. The `Expression` column in the output indicates the corresponded expression. For the non-expression indexes, the column shows `NULL`.

The cost of maintaining an expression index is higher than that of maintaining other indexes, because the value of the expression needs to be calculated whenever a row is inserted or updated. The value of the expression is already stored in the index, so this value does not require recalculation when the optimizer selects the expression index.

Therefore, when the query performance outweighs the insert and update performance, you can consider indexing the expressions.

Expression indexes have the same syntax and limitations as in MySQL. They are implemented by creating indexes on generated virtual columns that are invisible, so the supported expressions inherit all [limitations of virtual generated columns](/generated-columns.md#limitations).

## Multi-valued index

> **Warning:**
>
> For the current version, this feature is still experimental and not recommended for production environments.

Multi-valued index is a kind of secondary index defined on an array column. In a normal index, one index record corresponds to one data record (1:1). In a multi-valued index, multiple index records correspond to one data record (N:1). Multi-valued indexes are used to index JSON arrays. For example, a multi-valued index defined on the `zipcode` field will generate one index record for each element in the `zipcode` array.

```json
{
    "user":"Bob",
    "user_id":31,
    "zipcode":[94477,94536]
}
```

### Create a multi-valued index

You can create a multi-valued index by using the `CAST(... AS ... ARRAY)` expression in the index definition, as creating an expression index.

```sql
mysql> CREATE TABLE customers (
    id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name CHAR(10),
    custinfo JSON,
    INDEX zips((CAST(custinfo->'$.zipcode' AS UNSIGNED ARRAY)))
);
```

You can define a multi-valued index as a unique index.

```sql
mysql> CREATE TABLE customers (
    id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name CHAR(10),
    custinfo JSON,
    UNIQUE INDEX zips( (CAST(custinfo->'$.zipcode' AS UNSIGNED ARRAY)))
);
```

When a multi-valued index is defined as a unique index, an error is reported if you try to insert duplicate data.

```sql
mysql> INSERT INTO customers VALUES (1, 'pingcap', '{"zipcode": [1,2]}');
Query OK, 1 row affected (0.01 sec)

mysql> INSERT INTO customers VALUES (1, 'pingcap', '{"zipcode": [2,3]}');
ERROR 1062 (23000): Duplicate entry '2' for key 'customers.zips'
```

The same record can have duplicate values, but when different records have duplicate values, an error is reported.

```sql
-- Insert succeeded
mysql> INSERT INTO t1 VALUES('[1,1,2]');
mysql> INSERT INTO t1 VALUES('[3,3,3,4,4,4]');

-- Insert failed
mysql> INSERT INTO t1 VALUES('[1,2]');
mysql> INSERT INTO t1 VALUES('[2,3]');
```

You can also define a multi-valued index as a composite index:

```sql
mysql> CREATE TABLE customers (
    id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name CHAR(10),
    custinfo JSON,
    INDEX zips(name, (CAST(custinfo->'$.zipcode' AS UNSIGNED ARRAY)))
);
```

When a multi-valued index is defined as a composite index, the multi-valued part can appear in any position, but only once.

```sql
mysql> CREATE TABLE customers (
    id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name CHAR(10),
    custinfo JSON,
    INDEX zips(name, (CAST(custinfo->'$.zipcode' AS UNSIGNED ARRAY)), (CAST(custinfo->'$.zipcode' AS UNSIGNED ARRAY)))
);
ERROR 1235 (42000): This version of TiDB doesn't yet support 'more than one multi-valued key part per index'.
```

The written data must exactly match the type defined by the multi-valued index; otherwise, the data write fails:

```sql
-- All elements in the zipcode field must be the UNSIGNED type.
mysql> INSERT INTO customers VALUES (1, 'pingcap', '{"zipcode": [-1]}');
ERROR 3752 (HY000): Value is out of range for expression index 'zips' at row 1

mysql> INSERT INTO customers VALUES (1, 'pingcap', '{"zipcode": ["1"]}'); -- Incompatible with MySQL
ERROR 3903 (HY000): Invalid JSON value for CAST for expression index 'zips'

mysql> INSERT INTO customers VALUES (1, 'pingcap', '{"zipcode": [1]}');
Query OK, 1 row affected (0.00 sec)
```

### Use a multi-valued index

See [Index Selection - Use multi-valued indexes](/choose-index.md#use-a-multi-valued-index) for more details.

### Limitations

- For an empty JSON array, no corresponding index record is generated.
- The target type in `CAST(... AS ... ARRAY)` cannot be any of `BINARY`, `JSON`, `YEAR`, `FLOAT`, `DOUBLE`, and `DECIMAL`. The source type must be JSON.
- You cannot use a multi-valued index for sorting.
- You can only create a multi-valued index on a JSON array.
- A multi-valued index cannot be a primary key or a foreign key.
- The extra storage space used by a multi-valued index = the average number of array elements per row * the space used by a normal secondary index.
- Compared with normal indexes, DML operations will modify more index records for multi-valued indexes, so multi-valued indexes will have a greater performance impact than normal indexes.
- Because multi-valued indexes are a special type of expression index, multi-valued indexes have the same limitations as expression indexes.

## Invisible index

Invisible indexes are indexes that are ignored by the query optimizer:

```sql
CREATE TABLE t1 (c1 INT, c2 INT, UNIQUE(c2));
CREATE UNIQUE INDEX c1 ON t1 (c1) INVISIBLE;
```

For details, see [`ALTER INDEX`](/sql-statements/sql-statement-alter-index.md).

## Associated system variables

The system variables associated with the `CREATE INDEX` statement are `tidb_ddl_enable_fast_reorg`, `tidb_ddl_reorg_worker_cnt`, `tidb_ddl_reorg_batch_size`, `tidb_enable_auto_increment_in_generated`, and `tidb_ddl_reorg_priority`. Refer to [system variables](/system-variables.md#tidb_ddl_reorg_worker_cnt) for details.

## MySQL compatibility

* TiDB supports parsing the `FULLTEXT` and `SPATIAL` syntax but does not support using the `FULLTEXT`, `HASH`, and `SPATIAL` indexes.
* Descending indexes are not supported (similar to MySQL 5.7).
* Adding the primary key of the `CLUSTERED` type to a table is not supported. For more details about the primary key of the `CLUSTERED` type, refer to [clustered index](/clustered-indexes.md).
* Expression indexes are incompatible with views. When a query is executed using a view, the expression index cannot be used at the same time.
* Expression indexes have compatibility issues with bindings. When the expression of an expression index has a constant, the binding created for the corresponding query expands its scope. For example, suppose that the expression in the expression index is `a+1`, and the corresponding query condition is `a+1 > 2`. In this case, the created binding is `a+? > ?`, which means that the query with the condition such as `a+2 > 2` is also forced to use the expression index and results in a poor execution plan. In addition, this also affects the baseline capturing and baseline evolution in SQL Plan Management (SPM).
* The data written with the multi-valued index must exactly match the defined data type. Otherwise, data writes fail. For details, see [Creat a multi-valued index](/sql-statements/sql-statement-create-index.md#create-a-multi-valued-index).

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
