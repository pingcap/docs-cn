---
title: 优化器提示
summary: 使用优化器提示来影响查询执行计划
---

# 优化器提示

TiDB 支持优化器提示（Optimizer Hints），这些提示基于 MySQL 5.7 引入的注释语法。例如，一个常见的语法是 `/*+ HINT_NAME([t1_name [, t2_name] ...]) */`。建议在 TiDB 优化器选择了次优查询计划的情况下使用优化器提示。

如果遇到提示没有生效的情况，请参考[排查提示没有生效的常见问题](#排查提示没有生效的常见问题)。

## 语法

优化器提示不区分大小写，在 SQL 语句中紧跟在 `SELECT`、`INSERT`、`UPDATE` 或 `DELETE` 关键字后的 `/*+ ... */` 注释中指定。

多个提示可以用逗号分隔。例如，以下查询使用了三个不同的提示：

{{< copyable "sql" >}}

```sql
SELECT /*+ USE_INDEX(t1, idx1), HASH_AGG(), HASH_JOIN(t1) */ count(*) FROM t t1, t t2 WHERE t1.a = t2.b;
```

可以通过 [`EXPLAIN`](/sql-statements/sql-statement-explain.md) 和 [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md) 的输出来观察优化器提示如何影响查询执行计划。

不正确或不完整的提示不会导致语句错误。这是因为提示仅对查询执行具有建议（提示）语义。同样，如果提示不适用，TiDB 最多只会返回一个警告。

> **注意：**
>
> 如果注释不是紧跟在指定的关键字后面，它们将被视为普通的 MySQL 注释。这些注释不会生效，也不会报告警告。

目前，TiDB 支持两类提示，它们的作用范围不同。第一类提示在查询块范围内生效，例如 [`/*+ HASH_AGG() */`](#hash_agg)；第二类提示在整个查询中生效，例如 [`/*+ MEMORY_QUOTA(1024 MB)*/`](#memory_quotan)。

语句中的每个查询或子查询对应一个不同的查询块，每个查询块都有自己的名称。例如：

{{< copyable "sql" >}}

```sql
SELECT * FROM (SELECT * FROM t) t1, (SELECT * FROM t) t2;
```

上述查询语句有三个查询块：最外层的 `SELECT` 对应第一个查询块，名称为 `sel_1`；两个 `SELECT` 子查询对应第二和第三个查询块，名称分别为 `sel_2` 和 `sel_3`。数字的顺序是基于 `SELECT` 从左到右出现的顺序。如果将第一个 `SELECT` 替换为 `DELETE` 或 `UPDATE`，则相应的查询块名称为 `del_1` 或 `upd_1`。

## 在查询块中生效的提示

这类提示可以跟在**任何** `SELECT`、`UPDATE` 或 `DELETE` 关键字后面。要控制提示的生效范围，可以在提示中使用查询块的名称。你可以通过准确标识查询中的每个表（以防表名或别名重复）来使提示参数更清晰。如果提示中没有指定查询块，则默认在当前块中生效。

例如：

{{< copyable "sql" >}}

```sql
SELECT /*+ HASH_JOIN(@sel_1 t1@sel_1, t3) */ * FROM (SELECT t1.a, t1.b FROM t t1, t t2 WHERE t1.a = t2.a) t1, t t3 WHERE t1.b = t3.b;
```

这个提示在 `sel_1` 查询块中生效，其参数是 `sel_1` 中的 `t1` 和 `t3` 表（`sel_2` 中也包含一个 `t1` 表）。

如上所述，你可以通过以下方式在提示中指定查询块名称：

- 将查询块名称设置为提示的第一个参数，并用空格与其他参数分隔。除了 `QB_NAME` 外，本节列出的所有提示都有另一个可选的隐藏参数 `@QB_NAME`。通过使用此参数，你可以指定此提示的生效范围。
- 在参数中的表名后附加 `@QB_NAME` 以明确指定该表属于哪个查询块。

> **注意：**
>
> 你必须将提示放在提示生效的查询块中或之前。如果提示放在查询块之后，则无法生效。

### QB_NAME

如果查询语句是包含多个嵌套查询的复杂语句，某个查询块的 ID 和名称可能会被错误识别。`QB_NAME` 提示可以帮助我们解决这个问题。

`QB_NAME` 表示 Query Block Name（查询块名称）。你可以为查询块指定一个新名称。指定的 `QB_NAME` 和之前的默认名称都是有效的。例如：

{{< copyable "sql" >}}

```sql
SELECT /*+ QB_NAME(QB1) */ * FROM (SELECT * FROM t) t1, (SELECT * FROM t) t2;
```

这个提示将外层 `SELECT` 查询块的名称指定为 `QB1`，这使得 `QB1` 和默认名称 `sel_1` 对该查询块都有效。

> **注意：**
>
> 在上面的例子中，如果提示将 `QB_NAME` 指定为 `sel_2` 并且没有为原来的第二个 `SELECT` 查询块指定新的 `QB_NAME`，那么 `sel_2` 对第二个 `SELECT` 查询块来说就变成无效名称。

### SET_VAR(VAR_NAME=VAR_VALUE)

你可以使用 `SET_VAR(VAR_NAME=VAR_VALUE)` 提示在语句执行期间临时修改系统变量的值。语句执行完成后，当前会话中系统变量的值会自动恢复为原始值。此提示可用于修改一些与优化器和执行器相关的系统变量。有关可以使用此提示修改的系统变量列表，请参考[系统变量](/system-variables.md)。

> **警告：**
>
> 强烈建议不要修改未明确支持的变量，因为这可能会导致不可预知的行为。

以下是一个示例：

```sql
SELECT /*+ SET_VAR(MAX_EXECUTION_TIME=1234) */ @@MAX_EXECUTION_TIME;
SELECT @@MAX_EXECUTION_TIME;
```

执行上述 SQL 语句后，第一个查询返回提示中设置的值 `1234`，而不是 `MAX_EXECUTION_TIME` 的默认值。第二个查询返回变量的默认值。

```sql
+----------------------+
| @@MAX_EXECUTION_TIME |
+----------------------+
|                 1234 |
+----------------------+
1 row in set (0.00 sec)
+----------------------+
| @@MAX_EXECUTION_TIME |
+----------------------+
|                    0 |
+----------------------+
1 row in set (0.00 sec)
```

### MERGE_JOIN(t1_name [, tl_name ...])

`MERGE_JOIN(t1_name [, tl_name ...])` 提示告诉优化器对指定的表使用归并连接算法。通常，这个算法消耗的内存较少但处理时间较长。如果数据量非常大或系统内存不足，建议使用此提示。例如：

{{< copyable "sql" >}}

```sql
select /*+ MERGE_JOIN(t1, t2) */ * from t1, t2 where t1.id = t2.id;
```

> **注意：**
>
> `TIDB_SMJ` 是 TiDB 3.0.x 及更早版本中 `MERGE_JOIN` 的别名。如果你使用这些版本，必须使用 `TIDB_SMJ(t1_name [, tl_name ...])` 语法作为提示。对于更新版本的 TiDB，`TIDB_SMJ` 和 `MERGE_JOIN` 都是有效的提示名称，但建议使用 `MERGE_JOIN`。

### NO_MERGE_JOIN(t1_name [, tl_name ...])

`NO_MERGE_JOIN(t1_name [, tl_name ...])` 提示告诉优化器不对指定的表使用归并连接算法。例如：

```sql
SELECT /*+ NO_MERGE_JOIN(t1, t2) */ * FROM t1, t2 WHERE t1.id = t2.id;
```

### INL_JOIN(t1_name [, tl_name ...])

> **注意：**
>
> 在某些情况下，`INL_JOIN` 提示可能不会生效。更多信息，请参见 [`INL_JOIN` 提示不生效](#inl_join-提示不生效)。

`INL_JOIN(t1_name [, tl_name ...])` 提示告诉优化器对指定的表使用索引嵌套循环连接算法。在某些场景下，这个算法可能消耗更少的系统资源并且处理时间更短，但在其他场景下可能会产生相反的结果。如果外表经过 `WHERE` 条件过滤后的结果集少于 10,000 行，建议使用此提示。例如：

{{< copyable "sql" >}}

```sql
SELECT /*+ INL_JOIN(t1, t2) */ * FROM t1, t2, t3 WHERE t1.id = t2.id AND t2.id = t3.id;
```

在上述 SQL 语句中，`INL_JOIN(t1, t2)` 提示告诉优化器对 `t1` 和 `t2` 使用索引嵌套循环连接算法。注意，这并不意味着在 `t1` 和 `t2` 之间使用索引嵌套循环连接算法。相反，该提示表示 `t1` 和 `t2` 各自与另一个表（`t3`）使用索引嵌套循环连接算法。

`INL_JOIN()` 中给出的参数是创建查询计划时内表的候选表。例如，`INL_JOIN(t1)` 意味着 TiDB 只考虑使用 `t1` 作为内表来创建查询计划。如果候选表有别名，你必须使用别名作为 `INL_JOIN()` 的参数；如果没有别名，则使用表的原始名称作为参数。例如，在 `select /*+ INL_JOIN(t1) */ * from t t1, t t2 where t1.a = t2.b;` 查询中，你必须使用 `t` 表的别名 `t1` 或 `t2` 而不是 `t` 作为 `INL_JOIN()` 的参数。

> **注意：**
>
> `TIDB_INLJ` 是 TiDB 3.0.x 及更早版本中 `INL_JOIN` 的别名。如果你使用这些版本，必须使用 `TIDB_INLJ(t1_name [, tl_name ...])` 语法作为提示。对于更新版本的 TiDB，`TIDB_INLJ` 和 `INL_JOIN` 都是有效的提示名称，但建议使用 `INL_JOIN`。

### NO_INDEX_JOIN(t1_name [, tl_name ...])

`NO_INDEX_JOIN(t1_name [, tl_name ...])` 提示告诉优化器不对指定的表使用索引嵌套循环连接算法。例如：

```sql
SELECT /*+ NO_INDEX_JOIN(t1, t2) */ * FROM t1, t2 WHERE t1.id = t2.id;
```

### INL_HASH_JOIN

`INL_HASH_JOIN(t1_name [, tl_name])` 提示告诉优化器使用索引嵌套循环哈希连接算法。使用此算法的条件与使用索引嵌套循环连接算法的条件相同。两种算法的区别在于 `INL_JOIN` 在连接的内表上创建哈希表，而 `INL_HASH_JOIN` 在连接的外表上创建哈希表。`INL_HASH_JOIN` 对内存使用有固定限制，而 `INL_JOIN` 使用的内存取决于内表中匹配的行数。

### NO_INDEX_HASH_JOIN(t1_name [, tl_name ...])

`NO_INDEX_HASH_JOIN(t1_name [, tl_name ...])` 提示告诉优化器不对指定的表使用索引嵌套循环哈希连接算法。

### INL_MERGE_JOIN

`INL_MERGE_JOIN(t1_name [, tl_name])` 提示告诉优化器使用索引嵌套循环归并连接算法。使用此算法的条件与使用索引嵌套循环连接算法的条件相同。

### NO_INDEX_MERGE_JOIN(t1_name [, tl_name ...])

`NO_INDEX_MERGE_JOIN(t1_name [, tl_name ...])` 提示告诉优化器不对指定的表使用索引嵌套循环归并连接算法。

### HASH_JOIN(t1_name [, tl_name ...])

`HASH_JOIN(t1_name [, tl_name ...])` 提示告诉优化器对指定的表使用哈希连接算法。这个算法允许查询使用多个线程并发执行，从而实现更高的处理速度，但会消耗更多内存。例如：

{{< copyable "sql" >}}

```sql
select /*+ HASH_JOIN(t1, t2) */ * from t1, t2 where t1.id = t2.id;
```

> **注意：**
>
> `TIDB_HJ` 是 TiDB 3.0.x 及更早版本中 `HASH_JOIN` 的别名。如果你使用这些版本，必须使用 `TIDB_HJ(t1_name [, tl_name ...])` 语法作为提示。对于更新版本的 TiDB，`TIDB_HJ` 和 `HASH_JOIN` 都是有效的提示名称，但建议使用 `HASH_JOIN`。

### NO_HASH_JOIN(t1_name [, tl_name ...])

`NO_HASH_JOIN(t1_name [, tl_name ...])` 提示告诉优化器不对指定的表使用哈希连接算法。例如：

```sql
SELECT /*+ NO_HASH_JOIN(t1, t2) */ * FROM t1, t2 WHERE t1.id = t2.id;
```

### HASH_JOIN_BUILD(t1_name [, tl_name ...])

`HASH_JOIN_BUILD(t1_name [, tl_name ...])` 提示告诉优化器在指定的表上使用哈希连接算法，并将这些表作为构建侧。这样，你可以使用特定的表构建哈希表。例如：

```sql
SELECT /*+ HASH_JOIN_BUILD(t1) */ * FROM t1, t2 WHERE t1.id = t2.id;
```

### HASH_JOIN_PROBE(t1_name [, tl_name ...])

`HASH_JOIN_PROBE(t1_name [, tl_name ...])` 提示告诉优化器在指定的表上使用哈希连接算法，并将这些表作为探测侧。这样，你可以使用特定的表作为探测侧执行哈希连接算法。例如：

```sql
SELECT /*+ HASH_JOIN_PROBE(t2) */ * FROM t1, t2 WHERE t1.id = t2.id;
```

### SEMI_JOIN_REWRITE()

`SEMI_JOIN_REWRITE()` 提示告诉优化器将半连接查询重写为普通连接查询。目前，此提示仅适用于 `EXISTS` 子查询。

如果不使用此提示重写查询，当选择哈希连接作为执行计划时，半连接查询只能使用子查询来构建哈希表。在这种情况下，当子查询的结果大于外部查询的结果时，执行速度可能会比预期慢。

同样，当选择索引连接作为执行计划时，半连接查询只能使用外部查询作为驱动表。在这种情况下，当子查询的结果小于外部查询的结果时，执行速度可能会比预期慢。

当使用 `SEMI_JOIN_REWRITE()` 重写查询时，优化器可以扩大选择范围以选择更好的执行计划。

{{< copyable "sql" >}}

```sql
-- 不使用 SEMI_JOIN_REWRITE() 重写查询。
EXPLAIN SELECT * FROM t WHERE EXISTS (SELECT 1 FROM t1 WHERE t1.a = t.a);
```

```sql
+-----------------------------+---------+-----------+------------------------+---------------------------------------------------+
| id                          | estRows | task      | access object          | operator info                                     |
+-----------------------------+---------+-----------+------------------------+---------------------------------------------------+
| MergeJoin_9                 | 7992.00 | root      |                        | semi join, left key:test.t.a, right key:test.t1.a |
| ├─IndexReader_25(Build)     | 9990.00 | root      |                        | index:IndexFullScan_24                            |
| │ └─IndexFullScan_24        | 9990.00 | cop[tikv] | table:t1, index:idx(a) | keep order:true, stats:pseudo                     |
| └─IndexReader_23(Probe)     | 9990.00 | root      |                        | index:IndexFullScan_22                            |
|   └─IndexFullScan_22        | 9990.00 | cop[tikv] | table:t, index:idx(a)  | keep order:true, stats:pseudo                     |
+-----------------------------+---------+-----------+------------------------+---------------------------------------------------+
```

{{< copyable "sql" >}}

```sql
-- 使用 SEMI_JOIN_REWRITE() 重写查询。
EXPLAIN SELECT * FROM t WHERE EXISTS (SELECT /*+ SEMI_JOIN_REWRITE() */ 1 FROM t1 WHERE t1.a = t.a);
```

```sql
+------------------------------+---------+-----------+------------------------+---------------------------------------------------------------------------------------------------------------+
| id                           | estRows | task      | access object          | operator info                                                                                                 |
+------------------------------+---------+-----------+------------------------+---------------------------------------------------------------------------------------------------------------+
| IndexJoin_16                 | 1.25    | root      |                        | inner join, inner:IndexReader_15, outer key:test.t1.a, inner key:test.t.a, equal cond:eq(test.t1.a, test.t.a) |
| ├─StreamAgg_39(Build)        | 1.00    | root      |                        | group by:test.t1.a, funcs:firstrow(test.t1.a)->test.t1.a                                                      |
| │ └─IndexReader_34           | 1.00    | root      |                        | index:IndexFullScan_33                                                                                        |
| │   └─IndexFullScan_33       | 1.00    | cop[tikv] | table:t1, index:idx(a) | keep order:true                                                                                               |
| └─IndexReader_15(Probe)      | 1.25    | root      |                        | index:Selection_14                                                                                            |
|   └─Selection_14             | 1.25    | cop[tikv] |                        | not(isnull(test.t.a))                                                                                         |
|     └─IndexRangeScan_13      | 1.25    | cop[tikv] | table:t, index:idx(a)  | range: decided by [eq(test.t.a, test.t1.a)], keep order:false, stats:pseudo                                   |
+------------------------------+---------+-----------+------------------------+---------------------------------------------------------------------------------------------------------------+
```

从上面的例子可以看出，当使用 `SEMI_JOIN_REWRITE()` 提示时，TiDB 可以基于驱动表 `t1` 选择 IndexJoin 的执行方式。

### SHUFFLE_JOIN(t1_name [, tl_name ...])

`SHUFFLE_JOIN(t1_name [, tl_name ...])` 提示告诉优化器在指定的表上使用 Shuffle Join 算法。此提示仅在 MPP 模式下生效。例如：

```sql
SELECT /*+ SHUFFLE_JOIN(t1, t2) */ * FROM t1, t2 WHERE t1.id = t2.id;
```

> **注意：**
>
> - 在使用此提示之前，请确保当前 TiDB 集群可以在查询中支持使用 TiFlash MPP 模式。详情请参考[使用 TiFlash MPP 模式](/tiflash/use-tiflash-mpp-mode.md)。
> - 此提示可以与 [`HASH_JOIN_BUILD` 提示](#hash_join_buildt1_name--tl_name-) 和 [`HASH_JOIN_PROBE` 提示](#hash_join_probet1_name--tl_name-) 结合使用，以控制 Shuffle Join 算法的 Build 侧和 Probe 侧。

### BROADCAST_JOIN(t1_name [, tl_name ...])

`BROADCAST_JOIN(t1_name [, tl_name ...])` 提示告诉优化器在指定的表上使用 Broadcast Join 算法。此提示仅在 MPP 模式下生效。例如：

```sql
SELECT /*+ BROADCAST_JOIN(t1, t2) */ * FROM t1, t2 WHERE t1.id = t2.id;
```

> **注意：**
>
> - 在使用此提示之前，请确保当前 TiDB 集群可以在查询中支持使用 TiFlash MPP 模式。详情请参考[使用 TiFlash MPP 模式](/tiflash/use-tiflash-mpp-mode.md)。
> - 此提示可以与 [`HASH_JOIN_BUILD` 提示](#hash_join_buildt1_name--tl_name-) 和 [`HASH_JOIN_PROBE` 提示](#hash_join_probet1_name--tl_name-) 结合使用，以控制 Broadcast Join 算法的 Build 侧和 Probe 侧。

### NO_DECORRELATE()

`NO_DECORRELATE()` 提示告诉优化器不要尝试对指定查询块中的相关子查询进行去相关处理。此提示适用于包含相关列的 `EXISTS`、`IN`、`ANY`、`ALL`、`SOME` 子查询和标量子查询（即相关子查询）。

当在查询块中使用此提示时，优化器将不会尝试对子查询和其外部查询块之间的相关列进行去相关处理，而是始终使用 Apply 运算符执行查询。

默认情况下，TiDB 会尝试对相关子查询进行[去相关处理](/correlated-subquery-optimization.md)以实现更高的执行效率。但是，在[某些场景](/correlated-subquery-optimization.md#限制)下，去相关处理实际上可能会降低执行效率。在这种情况下，你可以使用此提示手动告诉优化器不要进行去相关处理。例如：

{{< copyable "sql" >}}

```sql
create table t1(a int, b int);
create table t2(a int, b int, index idx(b));
```

{{< copyable "sql" >}}

```sql
-- 不使用 NO_DECORRELATE()。
explain select * from t1 where t1.a < (select sum(t2.a) from t2 where t2.b = t1.b);
```

```sql
+----------------------------------+----------+-----------+---------------+--------------------------------------------------------------------------------------------------------------+
| id                               | estRows  | task      | access object | operator info                                                                                                |
+----------------------------------+----------+-----------+---------------+--------------------------------------------------------------------------------------------------------------+
| HashJoin_11                      | 9990.00  | root      |               | inner join, equal:[eq(test.t1.b, test.t2.b)], other cond:lt(cast(test.t1.a, decimal(10,0) BINARY), Column#7) |
| ├─HashAgg_23(Build)              | 7992.00  | root      |               | group by:test.t2.b, funcs:sum(Column#8)->Column#7, funcs:firstrow(test.t2.b)->test.t2.b                      |
| │ └─TableReader_24               | 7992.00  | root      |               | data:HashAgg_16                                                                                              |
| │   └─HashAgg_16                 | 7992.00  | cop[tikv] |               | group by:test.t2.b, funcs:sum(test.t2.a)->Column#8                                                           |
| │     └─Selection_22             | 9990.00  | cop[tikv] |               | not(isnull(test.t2.b))                                                                                       |
| │       └─TableFullScan_21       | 10000.00 | cop[tikv] | table:t2      | keep order:false, stats:pseudo                                                                               |
| └─TableReader_15(Probe)          | 9990.00  | root      |               | data:Selection_14                                                                                            |
|   └─Selection_14                 | 9990.00  | cop[tikv] |               | not(isnull(test.t1.b))                                                                                       |
|     └─TableFullScan_13           | 10000.00 | cop[tikv] | table:t1      | keep order:false, stats:pseudo                                                                               |
+----------------------------------+----------+-----------+---------------+--------------------------------------------------------------------------------------------------------------+
```

从上面的执行计划可以看出，优化器已经自动进行了去相关处理。去相关后的执行计划没有 Apply 运算符，而是在子查询和外部查询块之间有连接操作。原始的带有相关列的过滤条件（`t2.b = t1.b`）变成了普通的连接条件。

{{< copyable "sql" >}}

```sql
-- 使用 NO_DECORRELATE()。
explain select * from t1 where t1.a < (select /*+ NO_DECORRELATE() */ sum(t2.a) from t2 where t2.b = t1.b);
```

```sql
+------------------------------------------+-----------+-----------+------------------------+--------------------------------------------------------------------------------------+
| id                                       | estRows   | task      | access object          | operator info                                                                        |
+------------------------------------------+-----------+-----------+------------------------+--------------------------------------------------------------------------------------+
| Projection_10                            | 10000.00  | root      |                        | test.t1.a, test.t1.b                                                                 |
| └─Apply_12                               | 10000.00  | root      |                        | CARTESIAN inner join, other cond:lt(cast(test.t1.a, decimal(10,0) BINARY), Column#7) |
|   ├─TableReader_14(Build)                | 10000.00  | root      |                        | data:TableFullScan_13                                                                |
|   │ └─TableFullScan_13                   | 10000.00  | cop[tikv] | table:t1               | keep order:false, stats:pseudo                                                       |
|   └─MaxOneRow_15(Probe)                  | 10000.00  | root      |                        |                                                                                      |
|     └─StreamAgg_20                       | 10000.00  | root      |                        | funcs:sum(Column#14)->Column#7                                                       |
|       └─Projection_45                    | 100000.00 | root      |                        | cast(test.t2.a, decimal(10,0) BINARY)->Column#14                                     |
|         └─IndexLookUp_44                 | 100000.00 | root      |                        |                                                                                      |
|           ├─IndexRangeScan_42(Build)     | 100000.00 | cop[tikv] | table:t2, index:idx(b) | range: decided by [eq(test.t2.b, test.t1.b)], keep order:false, stats:pseudo         |
|           └─TableRowIDScan_43(Probe)     | 100000.00 | cop[tikv] | table:t2               | keep order:false, stats:pseudo                                                       |
+------------------------------------------+-----------+-----------+------------------------+--------------------------------------------------------------------------------------+
```

从上面的执行计划可以看出，优化器没有进行去相关处理。执行计划仍然包含 Apply 运算符。带有相关列的过滤条件（`t2.b = t1.b`）仍然是访问 `t2` 表时的过滤条件。

### HASH_AGG()

`HASH_AGG()` 提示告诉优化器在指定查询块中的所有聚合函数中使用哈希聚合算法。这个算法允许查询使用多个线程并发执行，从而实现更高的处理速度，但会消耗更多内存。例如：

{{< copyable "sql" >}}

```sql
select /*+ HASH_AGG() */ count(*) from t1, t2 where t1.a > 10 group by t1.id;
```

### STREAM_AGG()

`STREAM_AGG()` 提示告诉优化器在指定查询块中的所有聚合函数中使用流式聚合算法。通常，这个算法消耗的内存较少但处理时间较长。如果数据量非常大或系统内存不足，建议使用此提示。例如：

{{< copyable "sql" >}}

```sql
select /*+ STREAM_AGG() */ count(*) from t1, t2 where t1.a > 10 group by t1.id;
```

### MPP_1PHASE_AGG()

`MPP_1PHASE_AGG()` 告诉优化器在指定查询块中的所有聚合函数中使用一阶段聚合算法。此提示仅在 MPP 模式下生效。例如：

```sql
SELECT /*+ MPP_1PHASE_AGG() */ COUNT(*) FROM t1, t2 WHERE t1.a > 10 GROUP BY t1.id;
```

> **注意：**
>
> 在使用此提示之前，请确保当前 TiDB 集群可以在查询中支持使用 TiFlash MPP 模式。详情请参考[使用 TiFlash MPP 模式](/tiflash/use-tiflash-mpp-mode.md)。

### MPP_2PHASE_AGG()

`MPP_2PHASE_AGG()` 告诉优化器在指定查询块中的所有聚合函数中使用两阶段聚合算法。此提示仅在 MPP 模式下生效。例如：

```sql
SELECT /*+ MPP_2PHASE_AGG() */ COUNT(*) FROM t1, t2 WHERE t1.a > 10 GROUP BY t1.id;
```

> **注意：**
>
> 在使用此提示之前，请确保当前 TiDB 集群可以在查询中支持使用 TiFlash MPP 模式。详情请参考[使用 TiFlash MPP 模式](/tiflash/use-tiflash-mpp-mode.md)。

### USE_INDEX(t1_name, idx1_name [, idx2_name ...])

`USE_INDEX(t1_name, idx1_name [, idx2_name ...])` 提示告诉优化器仅使用指定的索引来访问指定的 `t1_name` 表。例如，应用以下提示的效果与执行 `select * from t t1 use index(idx1, idx2);` 语句相同。

{{< copyable "sql" >}}

```sql
SELECT /*+ USE_INDEX(t1, idx1, idx2) */ * FROM t1;
```

> **注意：**
>
> 如果在此提示中只指定表名而不指定索引名，则执行时不会考虑任何索引而是扫描整个表。

### FORCE_INDEX(t1_name, idx1_name [, idx2_name ...])

`FORCE_INDEX(t1_name, idx1_name [, idx2_name ...])` 提示告诉优化器仅使用指定的索引。

`FORCE_INDEX(t1_name, idx1_name [, idx2_name ...])` 的用法和效果与 `USE_INDEX(t1_name, idx1_name [, idx2_name ...])` 相同。

以下 4 个查询具有相同的效果：

{{< copyable "sql" >}}

```sql
SELECT /*+ USE_INDEX(t, idx1) */ * FROM t;
SELECT /*+ FORCE_INDEX(t, idx1) */ * FROM t;
SELECT * FROM t use index(idx1);
SELECT * FROM t force index(idx1);
```

### IGNORE_INDEX(t1_name, idx1_name [, idx2_name ...])

`IGNORE_INDEX(t1_name, idx1_name [, idx2_name ...])` 提示告诉优化器忽略指定 `t1_name` 表的指定索引。例如，应用以下提示的效果与执行 `select * from t t1 ignore index(idx1, idx2);` 语句相同。

{{< copyable "sql" >}}

```sql
select /*+ IGNORE_INDEX(t1, idx1, idx2) */ * from t t1;
```

### ORDER_INDEX(t1_name, idx1_name [, idx2_name ...])

`ORDER_INDEX(t1_name, idx1_name [, idx2_name ...])` 提示告诉优化器仅使用指定的索引来访问指定的表，并按顺序读取指定的索引。

> **警告：**
>
> 此提示可能导致 SQL 语句执行失败。建议先进行测试。如果测试时出现错误，请移除该提示。如果测试正常运行，则可以继续使用。

此提示通常应用在以下场景：

```sql
CREATE TABLE t(a INT, b INT, key(a), key(b));
EXPLAIN SELECT /*+ ORDER_INDEX(t, a) */ a FROM t ORDER BY a LIMIT 10;
```

```sql
+----------------------------+---------+-----------+---------------------+-------------------------------+
| id                         | estRows | task      | access object       | operator info                 |
+----------------------------+---------+-----------+---------------------+-------------------------------+
| Limit_10                   | 10.00   | root      |                     | offset:0, count:10            |
| └─IndexReader_14           | 10.00   | root      |                     | index:Limit_13                |
|   └─Limit_13               | 10.00   | cop[tikv] |                     | offset:0, count:10            |
|     └─IndexFullScan_12     | 10.00   | cop[tikv] | table:t, index:a(a) | keep order:true, stats:pseudo |
+----------------------------+---------+-----------+---------------------+-------------------------------+
```

优化器为此查询生成两种类型的计划：`Limit + IndexScan(keep order: true)` 和 `TopN + IndexScan(keep order: false)`。当使用 `ORDER_INDEX` 提示时，优化器选择第一个按顺序读取索引的计划。

> **注意：**
>
> - 如果查询本身不需要按顺序读取索引（即在没有提示的情况下，优化器在任何情况下都不会生成按顺序读取索引的计划），当使用 `ORDER_INDEX` 提示时，会出现 `Can't find a proper physical plan for this query` 错误。在这种情况下，你需要移除相应的 `ORDER_INDEX` 提示。
> - 分区表上的索引无法按顺序读取，因此不要在分区表及其相关索引上使用 `ORDER_INDEX` 提示。

### NO_ORDER_INDEX(t1_name, idx1_name [, idx2_name ...])

`NO_ORDER_INDEX(t1_name, idx1_name [, idx2_name ...])` 提示告诉优化器仅使用指定的索引来访问指定的表，但不按顺序读取指定的索引。此提示通常应用在以下场景。

以下示例显示查询语句的效果等同于 `SELECT * FROM t t1 use index(idx1, idx2);`：

```sql
CREATE TABLE t(a INT, b INT, key(a), key(b));
EXPLAIN SELECT /*+ NO_ORDER_INDEX(t, a) */ a FROM t ORDER BY a LIMIT 10;
```

```sql
+----------------------------+----------+-----------+---------------------+--------------------------------+
| id                         | estRows  | task      | access object       | operator info                  |
+----------------------------+----------+-----------+---------------------+--------------------------------+
| TopN_7                     | 10.00    | root      |                     | test.t.a, offset:0, count:10   |
| └─IndexReader_14           | 10.00    | root      |                     | index:TopN_13                  |
|   └─TopN_13                | 10.00    | cop[tikv] |                     | test.t.a, offset:0, count:10   |
|     └─IndexFullScan_12     | 10000.00 | cop[tikv] | table:t, index:a(a) | keep order:false, stats:pseudo |
+----------------------------+----------+-----------+---------------------+--------------------------------+
```

与 `ORDER_INDEX` 提示的示例相同，优化器为此查询生成两种类型的计划：`Limit + IndexScan(keep order: true)` 和 `TopN + IndexScan(keep order: false)`。当使用 `NO_ORDER_INDEX` 提示时，优化器将选择后一个不按顺序读取索引的计划。

### AGG_TO_COP()

`AGG_TO_COP()` 提示告诉优化器将指定查询块中的聚合操作下推到 coprocessor。如果优化器没有下推某些适合下推的聚合函数，则建议使用此提示。例如：

{{< copyable "sql" >}}

```sql
select /*+ AGG_TO_COP() */ sum(t1.a) from t t1;
```

### LIMIT_TO_COP()

`LIMIT_TO_COP()` 提示告诉优化器将指定查询块中的 `Limit` 和 `TopN` 运算符下推到 coprocessor。如果优化器没有执行此类操作，建议使用此提示。例如：

{{< copyable "sql" >}}

```sql
SELECT /*+ LIMIT_TO_COP() */ * FROM t WHERE a = 1 AND b > 10 ORDER BY c LIMIT 1;
```

### READ_FROM_STORAGE(TIFLASH[t1_name [, tl_name ...]], TIKV[t2_name [, tl_name ...]])

`READ_FROM_STORAGE(TIFLASH[t1_name [, tl_name ...]], TIKV[t2_name [, tl_name ...]])` 提示告诉优化器从指定的存储引擎读取指定的表。目前，此提示支持两个存储引擎参数 - `TIKV` 和 `TIFLASH`。如果表有别名，使用别名作为 `READ_FROM_STORAGE()` 的参数；如果表没有别名，使用表的原始名称作为参数。例如：

{{< copyable "sql" >}}

```sql
select /*+ READ_FROM_STORAGE(TIFLASH[t1], TIKV[t2]) */ t1.a from t t1, t t2 where t1.a = t2.a;
```

### USE_INDEX_MERGE(t1_name, idx1_name [, idx2_name ...])

`USE_INDEX_MERGE(t1_name, idx1_name [, idx2_name ...])` 提示告诉优化器使用索引合并方法访问指定的表。索引合并有两种类型：交集类型和并集类型。详情请参见[使用索引合并的 Explain 语句](/explain-index-merge.md)。

如果你明确指定了索引列表，TiDB 会从列表中选择索引来构建索引合并；如果你没有指定索引列表，TiDB 会从所有可用的索引中选择索引来构建索引合并。

对于交集类型的索引合并，提示中给出的索引列表是必需的参数。对于并集类型的索引合并，提示中给出的索引列表是可选参数。请参见以下示例。

{{< copyable "sql" >}}

```sql
SELECT /*+ USE_INDEX_MERGE(t1, idx_a, idx_b, idx_c) */ * FROM t1 WHERE t1.a > 10 OR t1.b > 10;
```

当对同一个表使用多个 `USE_INDEX_MERGE` 提示时，优化器会尝试从这些提示指定的索引集合的并集中选择索引。

> **注意：**
>
> `USE_INDEX_MERGE` 的参数指的是索引名称，而不是列名。主键的索引名称是 `primary`。

### LEADING(t1_name [, tl_name ...])

`LEADING(t1_name [, tl_name ...])` 提示提醒优化器在生成执行计划时，根据提示中指定的表名顺序来确定多表连接的顺序。例如：

{{< copyable "sql" >}}

```sql
SELECT /*+ LEADING(t1, t2) */ * FROM t1, t2, t3 WHERE t1.id = t2.id and t2.id = t3.id;
```

在上述多表连接查询中，连接顺序由 `LEADING()` 提示中指定的表名顺序决定。优化器将首先连接 `t1` 和 `t2`，然后将结果与 `t3` 连接。这个提示比 [`STRAIGHT_JOIN`](#straight_join) 更通用。

在以下情况下，`LEADING` 提示不会生效：

+ 指定了多个 `LEADING` 提示。
+ `LEADING` 提示中指定的表名不存在。
+ `LEADING` 提示中指定了重复的表名。
+ 优化器无法按照 `LEADING` 提示指定的顺序执行连接操作。
+ 已存在 `straight_join()` 提示。
+ 查询同时包含外连接和笛卡尔积。

在上述情况下，会生成一个警告。

```sql
-- 指定了多个 `LEADING` 提示。
SELECT /*+ LEADING(t1, t2) LEADING(t3) */ * FROM t1, t2, t3 WHERE t1.id = t2.id and t2.id = t3.id;

-- 要了解 `LEADING` 提示为什么没有生效，执行 `show warnings`。
SHOW WARNINGS;
```

```sql
+---------+------+-------------------------------------------------------------------------------------------------------------------+
| Level   | Code | Message                                                                                                           |
+---------+------+-------------------------------------------------------------------------------------------------------------------+
| Warning | 1815 | We can only use one leading hint at most, when multiple leading hints are used, all leading hints will be invalid |
+---------+------+-------------------------------------------------------------------------------------------------------------------+
```

> **注意：**
>
> 如果查询语句包含外连接，在提示中你只能指定那些连接顺序可以交换的表。如果提示中有一个表的连接顺序不能交换，则提示将无效。例如，在 `SELECT * FROM t1 LEFT JOIN (t2 JOIN t3 JOIN t4) ON t1.a = t2.a;` 中，如果你想控制 `t2`、`t3` 和 `t4` 表的连接顺序，你不能在 `LEADING` 提示中指定 `t1`。

### MERGE()

在带有公共表表达式（CTE）的查询中使用 `MERGE()` 提示可以禁用子查询的物化，并将子查询内联展开到 CTE 中。此提示仅适用于非递归 CTE。在某些场景下，使用 `MERGE()` 比默认分配临时空间的行为具有更高的执行效率。例如，下推查询条件或在嵌套 CTE 查询中：

```sql
-- 使用提示下推外部查询的谓词。
WITH CTE AS (SELECT /*+ MERGE() */ * FROM tc WHERE tc.a < 60) SELECT * FROM CTE WHERE CTE.a < 18;

-- 在嵌套 CTE 查询中使用提示将 CTE 内联展开到外部查询。
WITH CTE1 AS (SELECT * FROM t1), CTE2 AS (WITH CTE3 AS (SELECT /*+ MERGE() */ * FROM t2), CTE4 AS (SELECT * FROM t3) SELECT * FROM CTE3, CTE4) SELECT * FROM CTE1, CTE2;
```

> **注意：**
>
> `MERGE()` 仅适用于简单的 CTE 查询。在以下情况下不适用：
>
> - [递归 CTE](https://docs.pingcap.com/tidb/stable/dev-guide-use-common-table-expression#recursive-cte)
> - 无法展开内联的子查询，如聚合运算符、窗口函数和 `DISTINCT`。
>
> 当 CTE 引用次数过高时，查询性能可能低于默认的物化行为。
## 全局生效的提示

全局提示在[视图](/views.md)中生效。当指定为全局提示时，查询中定义的提示可以在视图内部生效。要指定全局提示，首先使用 `QB_NAME` 提示定义查询块名称，然后以 `ViewName@QueryBlockName` 的形式添加目标提示。

### 步骤 1：使用 `QB_NAME` 提示定义视图的查询块名称

使用 [`QB_NAME` 提示](#qb_name)为视图的每个查询块定义新名称。视图的 `QB_NAME` 提示定义与[查询块](#qb_name)的定义相同，但语法从 `QB_NAME(QB)` 扩展为 `QB_NAME(QB, ViewName@QueryBlockName [.ViewName@QueryBlockName .ViewName@QueryBlockName ...])`。

> **注意：**
>
> `@QueryBlockName` 和紧随其后的 `.ViewName@QueryBlockName` 之间有一个空格。否则，`.ViewName@QueryBlockName` 将被视为 `QueryBlockName` 的一部分。例如，`QB_NAME(v2_1, v2@SEL_1 .@SEL_1)` 是有效的，而 `QB_NAME(v2_1, v2@SEL_1.@SEL_1)` 无法正确解析。

- 对于只有单个视图且没有子查询的简单语句，以下示例指定视图 `v` 的第一个查询块名称：

    ```sql
    SELECT /* Comment: 当前查询块的名称是默认的 @SEL_1 */ * FROM v;
    ```

    对于视图 `v`，从查询语句开始的列表（`ViewName@QueryBlockName [.ViewName@QueryBlockName .ViewName@QueryBlockName ...]`）中的第一个视图名称是 `v@SEL_1`。视图 `v` 的第一个查询块可以声明为 `QB_NAME(v_1, v@SEL_1 .@SEL_1)`，或简写为 `QB_NAME(v_1, v)`，省略 `@SEL_1`：

    ```sql
    CREATE VIEW v AS SELECT /* Comment: 当前查询块的名称是默认的 @SEL_1 */ * FROM t;

    -- 指定全局提示
    SELECT /*+ QB_NAME(v_1, v) USE_INDEX(t@v_1, idx) */ * FROM v;
    ```

- 对于包含嵌套视图和子查询的复杂语句，以下示例为视图 `v1` 和 `v2` 的每个查询块指定名称：

    ```sql
    SELECT /* Comment: 当前查询块的名称是默认的 @SEL_1 */ * FROM v2 JOIN (
        SELECT /* Comment: 当前查询块的名称是默认的 @SEL_2 */ * FROM v2) vv;
    ```

    对于第一个视图 `v2`，从第一个查询语句开始的列表中的第一个视图名称是 `v2@SEL_1`。对于第二个视图 `v2`，第一个视图名称是 `v2@SEL_2`。以下示例仅考虑第一个视图 `v2`。

    视图 `v2` 的第一个查询块可以声明为 `QB_NAME(v2_1, v2@SEL_1 .@SEL_1)`，第二个查询块可以声明为 `QB_NAME(v2_2, v2@SEL_1 .@SEL_2)`：

    ```sql
    CREATE VIEW v2 AS
        SELECT * FROM t JOIN /* Comment: 对于视图 v2，当前查询块的名称是默认的 @SEL_1。因此，当前查询块视图列表是 v2@SEL_1 .@SEL_1 */
        (
            SELECT COUNT(*) FROM t1 JOIN v1 /* Comment: 对于视图 v2，当前查询块的名称是默认的 @SEL_2。因此，当前查询块视图列表是 v2@SEL_1 .@SEL_2 */
        ) tt;
    ```

    对于视图 `v1`，从前面的语句开始的列表中的第一个视图名称是 `v2@SEL_1 .v1@SEL_2`。视图 `v1` 中的第一个查询块可以声明为 `QB_NAME(v1_1, v2@SEL_1 .v1@SEL_2 .@SEL_1)`，第二个查询块可以声明为 `QB_NAME(v1_2, v2@SEL_1 .v1@SEL_2 .@SEL_2)`：

    ```sql
    CREATE VIEW v1 AS SELECT * FROM t JOIN /* Comment: 对于视图 `v1`，当前查询块的名称是默认的 @SEL_1。因此，当前查询块视图列表是 v2@SEL_1 .@SEL_2 .v1@SEL_1 */
        (
            SELECT COUNT(*) FROM t1 JOIN t2 /* Comment: 对于视图 `v1`，当前查询块的名称是默认的 @SEL_2。因此，当前查询块视图列表是 v2@SEL_1 .@SEL_2 .v1@SEL_2 */
        ) tt;
    ```

> **注意：**
>
> - 要在视图中使用全局提示，必须在视图中定义相应的 `QB_NAME` 提示。否则，全局提示将不会生效。
>
> - 当使用提示指定视图中的多个表名时，需要确保同一个提示中出现的表名都在同一个视图的同一个查询块中。
>
> - 当你在视图中为最外层查询块定义 `QB_NAME` 提示时：
>
>     - 对于 `QB_NAME` 中视图列表的第一项，如果没有明确声明 `@SEL_`，默认与定义 `QB_NAME` 的查询块位置一致。即查询 `SELECT /*+ QB_NAME(qb1, v2) */ * FROM v2 JOIN (SELECT /*+ QB_NAME(qb2, v2) */ * FROM v2) vv;` 等同于 `SELECT /*+ QB_NAME(qb1, v2@SEL_1) */ * FROM v2 JOIN (SELECT /*+ QB_NAME(qb2, v2@SEL_2) */ * FROM v2) vv;`。
>     - 对于 `QB_NAME` 中视图列表中除第一项之外的项，只能省略 `@SEL_1`。即如果在当前视图的第一个查询块中声明了 `@SEL_1`，则可以省略 `@SEL_1`。否则，不能省略 `@SEL_`。对于前面的示例：
>
>         - 视图 `v2` 的第一个查询块可以声明为 `QB_NAME(v2_1, v2)`。
>         - 视图 `v2` 的第二个查询块可以声明为 `QB_NAME(v2_2, v2.@SEL_2)`。
>         - 视图 `v1` 的第一个查询块可以声明为 `QB_NAME(v1_1, v2.v1@SEL_2)`。
>         - 视图 `v1` 的第二个查询块可以声明为 `QB_NAME(v1_2, v2.v1@SEL_2 .@SEL_2)`。

### 步骤 2：添加目标提示

在为视图的查询块定义了 `QB_NAME` 提示后，你可以以 `ViewName@QueryBlockName` 的形式添加所需的[在查询块中生效的提示](#在查询块中生效的提示)，使其在视图内部生效。例如：

- 为视图 `v2` 的第一个查询块指定 `MERGE_JOIN()` 提示：

    ```sql
    SELECT /*+ QB_NAME(v2_1, v2) merge_join(t@v2_1) */ * FROM v2;
    ```

- 为视图 `v2` 的第二个查询块指定 `MERGE_JOIN()` 和 `STREAM_AGG()` 提示：

    ```sql
    SELECT /*+ QB_NAME(v2_2, v2.@SEL_2) merge_join(t1@v2_2) stream_agg(@v2_2) */ * FROM v2;
    ```

- 为视图 `v1` 的第一个查询块指定 `HASH_JOIN()` 提示：

    ```sql
    SELECT /*+ QB_NAME(v1_1, v2.v1@SEL_2) hash_join(t@v1_1) */ * FROM v2;
    ```

- 为视图 `v1` 的第二个查询块指定 `HASH_JOIN()` 和 `HASH_AGG()` 提示：

    ```sql
    SELECT /*+ QB_NAME(v1_2, v2.v1@SEL_2 .@SEL_2) hash_join(t1@v1_2) hash_agg(@v1_2) */ * FROM v2;
    ```

## 在整个查询中生效的提示

这类提示只能跟在**第一个** `SELECT`、`UPDATE` 或 `DELETE` 关键字后面，相当于在执行此查询时修改指定系统变量的值。提示的优先级高于现有系统变量。

> **注意：**
>
> 这类提示也有一个可选的隐藏变量 `@QB_NAME`，但即使你指定了该变量，提示仍然在整个查询中生效。

### NO_INDEX_MERGE()

`NO_INDEX_MERGE()` 提示禁用优化器的索引合并功能。

例如，以下查询将不会使用索引合并：

{{< copyable "sql" >}}

```sql
select /*+ NO_INDEX_MERGE() */ * from t where t.a > 0 or t.b > 0;
```

除了此提示外，设置 `tidb_enable_index_merge` 系统变量也可以控制是否启用此功能。

> **注意：**
>
> - `NO_INDEX_MERGE` 的优先级高于 `USE_INDEX_MERGE`。当同时使用这两个提示时，`USE_INDEX_MERGE` 不会生效。
> - 对于子查询，`NO_INDEX_MERGE` 仅在放置在子查询最外层时才会生效。

### USE_TOJA(boolean_value)

`boolean_value` 参数可以是 `TRUE` 或 `FALSE`。`USE_TOJA(TRUE)` 提示启用优化器将包含子查询的 `in` 条件转换为连接和聚合操作。相比之下，`USE_TOJA(FALSE)` 提示禁用此功能。

例如，以下查询将把 `in (select t2.a from t2) subq` 转换为相应的连接和聚合操作：

{{< copyable "sql" >}}

```sql
select /*+ USE_TOJA(TRUE) */ t1.a, t1.b from t1 where t1.a in (select t2.a from t2) subq;
```

除了此提示外，设置 `tidb_opt_insubq_to_join_and_agg` 系统变量也可以控制是否启用此功能。

### MAX_EXECUTION_TIME(N)

`MAX_EXECUTION_TIME(N)` 提示对语句的执行时间设置限制 `N`（以毫秒为单位的超时值），超过该限制服务器将终止该语句。在以下提示中，`MAX_EXECUTION_TIME(1000)` 表示超时时间为 1000 毫秒（即 1 秒）：

{{< copyable "sql" >}}

```sql
select /*+ MAX_EXECUTION_TIME(1000) */ * from t1 inner join t2 where t1.id = t2.id;
```

除了此提示外，`global.max_execution_time` 系统变量也可以限制语句的执行时间。

### MEMORY_QUOTA(N)

`MEMORY_QUOTA(N)` 提示对语句的内存使用设置限制 `N`（以 MB 或 GB 为单位的阈值）。当语句的内存使用超过此限制时，TiDB 会根据语句的超限行为生成日志消息或直接终止该语句。

在以下提示中，`MEMORY_QUOTA(1024 MB)` 表示内存使用限制为 1024 MB：

{{< copyable "sql" >}}

```sql
select /*+ MEMORY_QUOTA(1024 MB) */ * from t;
```

除了此提示外，[`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query) 系统变量也可以限制语句的内存使用。

### READ_CONSISTENT_REPLICA()

`READ_CONSISTENT_REPLICA()` 提示启用从 TiKV follower 节点读取一致性数据的功能。例如：

{{< copyable "sql" >}}

```sql
select /*+ READ_CONSISTENT_REPLICA() */ * from t;
```

除了此提示外，将 `tidb_replica_read` 环境变量设置为 `'follower'` 或 `'leader'` 也可以控制是否启用此功能。

### IGNORE_PLAN_CACHE()

`IGNORE_PLAN_CACHE()` 提示提醒优化器在处理当前 `prepare` 语句时不使用 Plan Cache。

当启用了 [prepare-plan-cache](/sql-prepared-plan-cache.md) 时，此提示用于临时禁用某类查询的 Plan Cache。

在以下示例中，执行 `prepare` 语句时强制禁用 Plan Cache：

{{< copyable "sql" >}}

```sql
prepare stmt from 'select  /*+ IGNORE_PLAN_CACHE() */ * from t where t.id = ?';
```

### STRAIGHT_JOIN()

`STRAIGHT_JOIN()` 提示提醒优化器在生成连接计划时按照 `FROM` 子句中表名的顺序连接表。

{{< copyable "sql" >}}

```sql
SELECT /*+ STRAIGHT_JOIN() */ * FROM t t1, t t2 WHERE t1.a = t2.a;
```

> **注意：**
>
> - `STRAIGHT_JOIN` 的优先级高于 `LEADING`。当同时使用这两个提示时，`LEADING` 不会生效。
> - 建议使用 `LEADING` 提示，它比 `STRAIGHT_JOIN` 提示更通用。

### NTH_PLAN(N)

`NTH_PLAN(N)` 提示提醒优化器选择物理优化过程中找到的第 `N` 个物理计划。`N` 必须是正整数。

如果指定的 `N` 超出物理优化的搜索范围，TiDB 将返回一个警告，并根据忽略此提示的策略选择最优的物理计划。

当启用级联优化器时，此提示不生效。

在以下示例中，优化器被强制选择物理优化过程中找到的第三个物理计划：

{{< copyable "sql" >}}

```sql
SELECT /*+ NTH_PLAN(3) */ count(*) from t where a > 5;
```

> **注意：**
>
> `NTH_PLAN(N)` 主要用于测试，不保证在后续版本中的兼容性。请**谨慎**使用此提示。

### RESOURCE_GROUP(resource_group_name)

`RESOURCE_GROUP(resource_group_name)` 用于[资源控制](/tidb-resource-control.md)以隔离资源。此提示临时使用指定的资源组执行当前语句。如果指定的资源组不存在，此提示将被忽略。

示例：

```sql
SELECT /*+ RESOURCE_GROUP(rg1) */ * FROM t limit 10;
```
## 排查提示没有生效的常见问题

### MySQL 命令行客户端删除提示导致提示不生效

5.7.7 之前版本的 MySQL 命令行客户端默认会删除优化器提示。如果你想在这些早期版本中使用提示语法，在启动客户端时需要添加 `--comments` 选项。例如：`mysql -h 127.0.0.1 -P 4000 -uroot --comments`。

### 未指定数据库名称导致提示不生效

如果在创建连接时没有指定数据库名称，提示可能不会生效。例如：

当连接到 TiDB 时，你使用 `mysql -h127.0.0.1 -P4000 -uroot` 命令而没有使用 `-D` 选项，然后执行以下 SQL 语句：

```sql
SELECT /*+ use_index(t, a) */ a FROM test.t;
SHOW WARNINGS;
```

因为 TiDB 无法识别表 `t` 的数据库，所以 `use_index(t, a)` 提示不会生效。

```sql
+---------+------+----------------------------------------------------------------------+
| Level   | Code | Message                                                              |
+---------+------+----------------------------------------------------------------------+
| Warning | 1815 | use_index(.t, a) is inapplicable, check whether the table(.t) exists |
+---------+------+----------------------------------------------------------------------+
1 row in set (0.00 sec)
```

### 跨表查询中未明确指定数据库名称导致提示不生效

执行跨表查询时，需要明确指定数据库名称。否则，提示可能不会生效。例如：

```sql
USE test1;
CREATE TABLE t1(a INT, KEY(a));
USE test2;
CREATE TABLE t2(a INT, KEY(a));
SELECT /*+ use_index(t1, a) */ * FROM test1.t1, t2;
SHOW WARNINGS;
```

在上述语句中，因为表 `t1` 不在当前的 `test2` 数据库中，所以 `use_index(t1, a)` 提示不会生效。

```sql
+---------+------+----------------------------------------------------------------------------------+
| Level   | Code | Message                                                                          |
+---------+------+----------------------------------------------------------------------------------+
| Warning | 1815 | use_index(test2.t1, a) is inapplicable, check whether the table(test2.t1) exists |
+---------+------+----------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

在这种情况下，你需要通过使用 `use_index(test1.t1, a)` 而不是 `use_index(t1, a)` 来明确指定数据库名称。

### 提示放置位置错误导致提示不生效

如果提示没有直接放在特定关键字后面，则无法生效。例如：

```sql
SELECT * /*+ use_index(t, a) */ FROM t;
SHOW WARNINGS;
```

警告如下：

```sql
+---------+------+---------------------------------------------------------------------------------------------------------------------------------------------------------+
| Level   | Code | Message                                                                                                                                                 |
+---------+------+---------------------------------------------------------------------------------------------------------------------------------------------------------+
| Warning | 1064 | You have an error in your SQL syntax; check the manual that corresponds to your TiDB version for the right syntax to use [parser:8066]Optimizer hint can only be followed by certain keywords like SELECT, INSERT, etc. |
+---------+------+---------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.01 sec)
```

在这种情况下，你需要将提示直接放在 `SELECT` 关键字后面。更多详情，请参见[语法](#语法)部分。

### `INL_JOIN` 提示不生效

#### 在连接表的列上使用内置函数导致 `INL_JOIN` 提示不生效

在某些情况下，如果你在连接表的列上使用内置函数，优化器可能无法选择 `IndexJoin` 计划，导致 `INL_JOIN` 提示也不会生效。

例如，以下查询在连接表的列 `tname` 上使用了内置函数 `substr`：

```sql
CREATE TABLE t1 (id varchar(10) primary key, tname varchar(10));
CREATE TABLE t2 (id varchar(10) primary key, tname varchar(10));
EXPLAIN SELECT /*+ INL_JOIN(t1, t2) */ * FROM t1, t2 WHERE t1.id=t2.id and SUBSTR(t1.tname,1,2)=SUBSTR(t2.tname,1,2);
```

执行计划如下：

```sql
+------------------------------+----------+-----------+---------------+-----------------------------------------------------------------------+
| id                           | estRows  | task      | access object | operator info                                                         |
+------------------------------+----------+-----------+---------------+-----------------------------------------------------------------------+
| HashJoin_12                  | 12500.00 | root      |               | inner join, equal:[eq(test.t1.id, test.t2.id) eq(Column#5, Column#6)] |
| ├─Projection_17(Build)       | 10000.00 | root      |               | test.t2.id, test.t2.tname, substr(test.t2.tname, 1, 2)->Column#6      |
| │ └─TableReader_19           | 10000.00 | root      |               | data:TableFullScan_18                                                 |
| │   └─TableFullScan_18       | 10000.00 | cop[tikv] | table:t2      | keep order:false, stats:pseudo                                        |
| └─Projection_14(Probe)       | 10000.00 | root      |               | test.t1.id, test.t1.tname, substr(test.t1.tname, 1, 2)->Column#5      |
|   └─TableReader_16           | 10000.00 | root      |               | data:TableFullScan_15                                                 |
|     └─TableFullScan_15       | 10000.00 | cop[tikv] | table:t1      | keep order:false, stats:pseudo                                        |
+------------------------------+----------+-----------+---------------+-----------------------------------------------------------------------+
7 rows in set, 1 warning (0.01 sec)
```

```sql
SHOW WARNINGS;
```

```
+---------+------+------------------------------------------------------------------------------------+
| Level   | Code | Message                                                                            |
+---------+------+------------------------------------------------------------------------------------+
| Warning | 1815 | Optimizer Hint /*+ INL_JOIN(t1, t2) */ or /*+ TIDB_INLJ(t1, t2) */ is inapplicable |
+---------+------+------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

从上面的示例可以看出，`INL_JOIN` 提示没有生效。这是由于优化器的一个限制，它不允许使用 `Projection` 或 `Selection` 运算符作为 `IndexJoin` 的探测侧。

从 TiDB v8.0.0 开始，你可以通过将 [`tidb_enable_inl_join_inner_multi_pattern`](/system-variables.md#tidb_enable_inl_join_inner_multi_pattern-new-in-v700) 设置为 `ON` 来避免这个问题。

```sql
SET @@tidb_enable_inl_join_inner_multi_pattern=ON;
Query OK, 0 rows affected (0.00 sec)

EXPLAIN SELECT /*+ INL_JOIN(t1, t2) */ * FROM t1, t2 WHERE t1.id=t2.id AND SUBSTR(t1.tname,1,2)=SUBSTR(t2.tname,1,2);
+------------------------------+--------------+-----------+---------------+--------------------------------------------------------------------------------------------------------------------------------------------+
| id                           | estRows      | task      | access object | operator info                                                                                                                              |
+------------------------------+--------------+-----------+---------------+--------------------------------------------------------------------------------------------------------------------------------------------+
| IndexJoin_18                 | 12500.00     | root      |               | inner join, inner:Projection_14, outer key:test.t1.id, inner key:test.t2.id, equal cond:eq(Column#5, Column#6), eq(test.t1.id, test.t2.id) |
| ├─Projection_32(Build)       | 10000.00     | root      |               | test.t1.id, test.t1.tname, substr(test.t1.tname, 1, 2)->Column#5                                                                           |
| │ └─TableReader_34           | 10000.00     | root      |               | data:TableFullScan_33                                                                                                                      |
| │   └─TableFullScan_33       | 10000.00     | cop[tikv] | table:t1      | keep order:false, stats:pseudo                                                                                                             |
| └─Projection_14(Probe)       | 100000000.00 | root      |               | test.t2.id, test.t2.tname, substr(test.t2.tname, 1, 2)->Column#6                                                                           |
|   └─TableReader_13           | 10000.00     | root      |               | data:TableRangeScan_12                                                                                                                     |
|     └─TableRangeScan_12      | 10000.00     | cop[tikv] | table:t2      | range: decided by [eq(test.t2.id, test.t1.id)], keep order:false, stats:pseudo                                                             |
+------------------------------+--------------+-----------+---------------+--------------------------------------------------------------------------------------------------------------------------------------------+
7 rows in set (0.00 sec)
```

#### 由于排序规则不兼容导致 `INL_JOIN`、`INL_HASH_JOIN` 和 `INL_MERGE_JOIN` 提示不生效

当两个表之间连接键的排序规则不兼容时，无法使用 `IndexJoin` 运算符执行查询。在这种情况下，[`INL_JOIN`](#inl_joint1_name--tl_name-)、[`INL_HASH_JOIN`](#inl_hash_join) 和 [`INL_MERGE_JOIN`](#inl_merge_join) 提示不会生效。例如：

```sql
CREATE TABLE t1 (k varchar(8), key(k)) COLLATE=utf8mb4_general_ci;
CREATE TABLE t2 (k varchar(8), key(k)) COLLATE=utf8mb4_bin;
EXPLAIN SELECT /*+ tidb_inlj(t1) */ * FROM t1, t2 WHERE t1.k=t2.k;
```

执行计划如下：

```sql
+-----------------------------+----------+-----------+----------------------+----------------------------------------------+
| id                          | estRows  | task      | access object        | operator info                                |
+-----------------------------+----------+-----------+----------------------+----------------------------------------------+
| HashJoin_19                 | 12487.50 | root      |                      | inner join, equal:[eq(test.t1.k, test.t2.k)] |
| ├─IndexReader_24(Build)     | 9990.00  | root      |                      | index:IndexFullScan_23                       |
| │ └─IndexFullScan_23        | 9990.00  | cop[tikv] | table:t2, index:k(k) | keep order:false, stats:pseudo               |
| └─IndexReader_22(Probe)     | 9990.00  | root      |                      | index:IndexFullScan_21                       |
|   └─IndexFullScan_21        | 9990.00  | cop[tikv] | table:t1, index:k(k) | keep order:false, stats:pseudo               |
+-----------------------------+----------+-----------+----------------------+----------------------------------------------+
5 rows in set, 1 warning (0.00 sec)
```

在上述语句中，`t1.k` 和 `t2.k` 的排序规则不兼容（分别是 `utf8mb4_general_ci` 和 `utf8mb4_bin`），这阻止了 `INL_JOIN` 或 `TIDB_INLJ` 提示生效。

```sql
SHOW WARNINGS;
+---------+------+----------------------------------------------------------------------------+
| Level   | Code | Message                                                                    |
+---------+------+----------------------------------------------------------------------------+
| Warning | 1815 | Optimizer Hint /*+ INL_JOIN(t1) */ or /*+ TIDB_INLJ(t1) */ is inapplicable |
+---------+------+----------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

#### 由于连接顺序导致 `INL_JOIN` 提示不生效

[`INL_JOIN(t1, t2)`](#inl_joint1_name--tl_name-) 或 `TIDB_INLJ(t1, t2)` 提示在语义上指示 `t1` 和 `t2` 作为内表在 `IndexJoin` 运算符中与其他表连接，而不是直接使用 `IndexJoin` 运算符连接它们。例如：

```sql
EXPLAIN SELECT /*+ inl_join(t1, t3) */ * FROM t1, t2, t3 WHERE t1.id = t2.id AND t2.id = t3.id AND t1.id = t3.id;
+---------------------------------+----------+-----------+---------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| id                              | estRows  | task      | access object | operator info                                                                                                                                                           |
+---------------------------------+----------+-----------+---------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| IndexJoin_16                    | 15625.00 | root      |               | inner join, inner:TableReader_13, outer key:test.t2.id, test.t1.id, inner key:test.t3.id, test.t3.id, equal cond:eq(test.t1.id, test.t3.id), eq(test.t2.id, test.t3.id) |
| ├─IndexJoin_34(Build)           | 12500.00 | root      |               | inner join, inner:TableReader_31, outer key:test.t2.id, inner key:test.t1.id, equal cond:eq(test.t2.id, test.t1.id)                                                     |
| │ ├─TableReader_40(Build)       | 10000.00 | root      |               | data:TableFullScan_39                                                                                                                                                   |
| │ │ └─TableFullScan_39          | 10000.00 | cop[tikv] | table:t2      | keep order:false, stats:pseudo                                                                                                                                          |
| │ └─TableReader_31(Probe)       | 10000.00 | root      |               | data:TableRangeScan_30                                                                                                                                                  |
| │   └─TableRangeScan_30         | 10000.00 | cop[tikv] | table:t1      | range: decided by [test.t2.id], keep order:false, stats:pseudo                                                                                                          |
| └─TableReader_13(Probe)         | 12500.00 | root      |               | data:TableRangeScan_12                                                                                                                                                  |
|   └─TableRangeScan_12           | 12500.00 | cop[tikv] | table:t3      | range: decided by [test.t2.id test.t1.id], keep order:false, stats:pseudo                                                                                               |
+---------------------------------+----------+-----------+---------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
```

在上面的示例中，`t1` 和 `t3` 没有直接通过 `IndexJoin` 连接在一起。

要在 `t1` 和 `t3` 之间执行直接的 `IndexJoin`，你可以首先使用 [`LEADING(t1, t3)` 提示](#leadingt1_name--tl_name-) 指定 `t1` 和 `t3` 的连接顺序，然后使用 `INL_JOIN` 提示指定连接算法。例如：

```sql
EXPLAIN SELECT /*+ leading(t1, t3), inl_join(t3) */ * FROM t1, t2, t3 WHERE t1.id = t2.id AND t2.id = t3.id AND t1.id = t3.id;
+---------------------------------+----------+-----------+---------------+---------------------------------------------------------------------------------------------------------------------+
| id                              | estRows  | task      | access object | operator info                                                                                                       |
+---------------------------------+----------+-----------+---------------+---------------------------------------------------------------------------------------------------------------------+
| Projection_12                   | 15625.00 | root      |               | test.t1.id, test.t1.name, test.t2.id, test.t2.name, test.t3.id, test.t3.name                                        |
| └─HashJoin_21                   | 15625.00 | root      |               | inner join, equal:[eq(test.t1.id, test.t2.id) eq(test.t3.id, test.t2.id)]                                           |
|   ├─TableReader_36(Build)       | 10000.00 | root      |               | data:TableFullScan_35                                                                                               |
|   │ └─TableFullScan_35          | 10000.00 | cop[tikv] | table:t2      | keep order:false, stats:pseudo                                                                                      |
|   └─IndexJoin_28(Probe)         | 12500.00 | root      |               | inner join, inner:TableReader_25, outer key:test.t1.id, inner key:test.t3.id, equal cond:eq(test.t1.id, test.t3.id) |
|     ├─TableReader_34(Build)     | 10000.00 | root      |               | data:TableFullScan_33                                                                                               |
|     │ └─TableFullScan_33        | 10000.00 | cop[tikv] | table:t1      | keep order:false, stats:pseudo                                                                                      |
|     └─TableReader_25(Probe)     | 10000.00 | root      |               | data:TableRangeScan_24                                                                                              |
|       └─TableRangeScan_24       | 10000.00 | cop[tikv] | table:t3      | range: decided by [test.t1.id], keep order:false, stats:pseudo                                                      |
+---------------------------------+----------+-----------+---------------+---------------------------------------------------------------------------------------------------------------------+
9 rows in set (0.01 sec)
```

### 使用提示导致出现 `Can't find a proper physical plan for this query` 错误

在以下场景中可能会出现 `Can't find a proper physical plan for this query` 错误：

- 查询本身不需要按顺序读取索引。即在没有提示的情况下，优化器在任何情况下都不会生成按顺序读取索引的计划。在这种情况下，如果指定了 `ORDER_INDEX` 提示，就会出现此错误。要解决此问题，请移除相应的 `ORDER_INDEX` 提示。
- 查询通过使用 `NO_JOIN` 相关提示排除了所有可能的连接方法。

```sql
CREATE TABLE t1 (a INT);
CREATE TABLE t2 (a INT);
EXPLAIN SELECT /*+ NO_HASH_JOIN(t1), NO_MERGE_JOIN(t1) */ * FROM t1, t2 WHERE t1.a=t2.a;
ERROR 1815 (HY000): Internal : Can't find a proper physical plan for this query
```

- 系统变量 [`tidb_opt_enable_hash_join`](/system-variables.md#tidb_opt_enable_hash_join-new-in-v656-v712-and-v740) 设置为 `OFF`，并且所有其他连接类型也被排除。

```sql
CREATE TABLE t1 (a INT);
CREATE TABLE t2 (a INT);
set tidb_opt_enable_hash_join=off;
EXPLAIN SELECT /*+ NO_MERGE_JOIN(t1) */ * FROM t1, t2 WHERE t1.a=t2.a;
ERROR 1815 (HY000): Internal : Can't find a proper physical plan for this query
```
