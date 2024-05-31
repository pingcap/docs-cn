---
title: Optimizer Hints
---

# Optimizer Hints

TiDB 支持 Optimizer Hints 语法，它基于 MySQL 5.7 中介绍的类似 comment 的语法，例如 `/*+ HINT_NAME(t1, t2) */`。当 TiDB 优化器选择的不是最优查询计划时，建议使用 Optimizer Hints。

如果遇到 Hint 无法生效的情况，请参考[常见 Hint 不生效问题排查](#常见-hint-不生效问题排查)。

## 语法

Optimizer Hints 不区分大小写，通过 `/*+ ... */` 注释的形式跟在 `SELECT`、`UPDATE` 或 `DELETE` 关键字的后面。`INSERT` 关键字后不支持 Optimizer Hints。

多个不同的 Hint 之间需用逗号隔开，例如：

{{< copyable "sql" >}}

```sql
SELECT /*+ USE_INDEX(t1, idx1), HASH_AGG(), HASH_JOIN(t1) */ count(*) FROM t t1, t t2 WHERE t1.a = t2.b;
```

可以通过 [`Explain`](/sql-statements/sql-statement-explain.md)/[`Explain Analyze`](/sql-statements/sql-statement-explain-analyze.md) 语句的输出，来查看 Optimizer Hints 对查询执行计划的影响。

如果 Optimizer Hints 包含语法错误或不完整，查询语句不会报错，而是按照没有 Optimizer Hints 的情况执行。如果 Hint 不适用于当前语句，TiDB 会返回 Warning，用户可以在查询结束后通过 `Show Warnings` 命令查看具体信息。

> **注意：**
>
> 如果注释不是跟在指定的关键字后，会被当作是普通的 MySQL comment，注释不会生效，且不会上报 warning。

TiDB 目前支持的 Optimizer Hints 根据生效范围的不同可以划分为两类：第一类是在查询块范围生效的 Hint，例如 [`/*+ HASH_AGG() */`](#hash_agg)；第二类是在整个查询范围生效的 Hint，例如 [`/*+ MEMORY_QUOTA(1024 MB)*/`](#memory_quotan)。

每条语句中每一个查询和子查询都对应着一个不同的查询块，每个查询块有自己对应的名字。以下面这条语句为例：

{{< copyable "sql" >}}

```sql
SELECT * FROM (SELECT * FROM t) t1, (SELECT * FROM t) t2;
```

该查询语句有 3 个查询块，最外面一层 `SELECT` 所在的查询块的名字为 `sel_1`，两个 `SELECT` 子查询的名字依次为 `sel_2` 和 `sel_3`。其中数字序号根据 `SELECT` 出现的位置从左到右计数。如果分别用 `DELETE` 和 `UPDATE` 查询替代第一个 `SELECT` 查询，则对应的查询块名字分别为 `del_1` 和 `upd_1`。

## 查询块范围生效的 Hint

这类 Hint 可以跟在查询语句中**任意** `SELECT`、`UPDATE` 或 `DELETE` 关键字的后面。通过在 Hint 中使用查询块名字可以控制 Hint 的生效范围，以及准确标识查询中的每一个表（有可能表的名字或者别名相同），方便明确 Hint 的参数指向。若不显式地在 Hint 中指定查询块，Hint 默认作用于当前查询块。以如下查询为例：

{{< copyable "sql" >}}

```sql
SELECT /*+ HASH_JOIN(@sel_1 t1@sel_1, t3) */ * FROM (SELECT t1.a, t1.b FROM t t1, t t2 WHERE t1.a = t2.a) t1, t t3 WHERE t1.b = t3.b;
```

该 Hint 在 `sel_1` 这个查询块中生效，参数分别为 `sel_1` 中的 `t1` 表（`sel_2` 中也有一个 `t1` 表）和 `t3` 表。

如上例所述，在 Hint 中使用查询块名字的方式有两种：第一种是作为 Hint 的第一个参数，与其他参数用空格隔开。除 `QB_NAME` 外，本节所列的所有 Hint 除自身明确列出的参数外都有一个隐藏的可选参数 `@QB_NAME`，通过使用这个参数可以指定该 Hint 的生效范围；第二种在 Hint 中使用查询块名字的方式是在参数中的某一个表名后面加 `@QB_NAME`，用以明确指出该参数是哪个查询块中的表。

> **注意：**
>
> Hint 声明的位置必须在指定生效的查询块之中或之前，不能是在之后的查询块中，否则无法生效。

### QB_NAME

当查询语句是包含多层嵌套子查询的复杂语句时，识别某个查询块的序号和名字很可能会出错，Hint `QB_NAME` 可以方便我们使用查询块。`QB_NAME` 是 Query Block Name 的缩写，用于为某个查询块指定新的名字，同时查询块原本默认的名字依然有效。例如：

{{< copyable "sql" >}}

```sql
SELECT /*+ QB_NAME(QB1) */ * FROM (SELECT * FROM t) t1, (SELECT * FROM t) t2;
```

这条 Hint 将最外层 `SELECT` 查询块的命名为 `QB1`，此时 `QB1` 和默认名称 `sel_1` 对于这个查询块来说都是有效的。

> **注意：**
>
> 上述例子中，如果指定的 `QB_NAME` 为 `sel_2`，并且不给原本 `sel_2` 对应的第二个查询块指定新的 `QB_NAME`，则第二个查询块的默认名字 `sel_2` 会失效。

### MERGE_JOIN(t1_name [, tl_name ...])

`MERGE_JOIN(t1_name [, tl_name ...])` 提示优化器对指定表使用 Sort Merge Join 算法。这个算法通常会占用更少的内存，但执行时间会更久。当数据量太大，或系统内存不足时，建议尝试使用。例如：

{{< copyable "sql" >}}

```sql
SELECT /*+ MERGE_JOIN(t1, t2) */ * FROM t1, t2 WHERE t1.id = t2.id;
```

> **注意：**
>
> `MERGE_JOIN` 的别名是 `TIDB_SMJ`，在 3.0.x 及之前版本仅支持使用该别名；之后的版本同时支持使用这两种名称，但推荐使用 `MERGE_JOIN`。

### NO_MERGE_JOIN(t1_name [, tl_name ...])

`NO_MERGE_JOIN(t1_name [, tl_name ...])` 提示优化器对指定表不要使用 Sort Merge Join 算法。例如：

{{< copyable "sql" >}}

```sql
SELECT /*+ NO_MERGE_JOIN(t1, t2) */ * FROM t1, t2 WHERE t1.id = t2.id;
```

### INL_JOIN(t1_name [, tl_name ...])

> **注意：**
>
> 部分情况下 `INL_JOIN` Hint 可能无法生效，详情请参阅 [`INL_JOIN` Hint 不生效](#inl_join-hint-不生效)。

`INL_JOIN(t1_name [, tl_name ...])` 提示优化器对指定表使用 Index Nested Loop Join 算法。这个算法可能会在某些场景更快，消耗更少系统资源，有的场景会更慢，消耗更多系统资源。对于外表经过 WHERE 条件过滤后结果集较小（小于 1 万行）的场景，可以尝试使用。例如：

{{< copyable "sql" >}}

```sql
SELECT /*+ INL_JOIN(t1, t2) */ * FROM t1, t2 WHERE t1.id = t2.id;
```

`INL_JOIN()` 中的参数是建立查询计划时内表的候选表，比如 `INL_JOIN(t1)` 只会考虑使用 t1 作为内表构建查询计划。表如果指定了别名，就只能使用表的别名作为 `INL_JOIN()` 的参数；如果没有指定别名，则用表的本名作为其参数。比如在 `SELECT /*+ INL_JOIN(t1) */ * FROM t t1, t t2 WHERE t1.a = t2.b;` 中，`INL_JOIN()` 的参数只能使用 t 的别名 t1 或 t2，不能用 t。

> **注意：**
>
> `INL_JOIN` 的别名是 `TIDB_INLJ`，在 3.0.x 及之前版本仅支持使用该别名；之后的版本同时支持使用这两种名称，但推荐使用 `INL_JOIN`。

### NO_INDEX_JOIN(t1_name [, tl_name ...])

`NO_INDEX_JOIN(t1_name [, tl_name ...])` 提示优化器对指定表不要使用 Index Nested Loop Join 算法。例如：

{{< copyable "sql" >}}

```sql
SELECT /*+ NO_INDEX_JOIN(t1, t2) */ * FROM t1, t2 WHERE t1.id = t2.id;
```

### INL_HASH_JOIN

`INL_HASH_JOIN(t1_name [, tl_name])` 提示优化器使用 Index Nested Loop Hash Join 算法。该算法与 Index Nested Loop Join 使用条件完全一样，两者的区别是 `INL_JOIN` 会在连接的内表上建哈希表，而 `INL_HASH_JOIN` 会在连接的外表上建哈希表，后者对于内存的使用是有固定上限的，而前者使用的内存使用取决于内表匹配到的行数。

### NO_INDEX_HASH_JOIN(t1_name [, tl_name ...])

`NO_INDEX_HASH_JOIN(t1_name [, tl_name ...])` 提示优化器对指定表不要使用 Index Nested Loop Hash Join 算法。

### INL_MERGE_JOIN

`INL_MERGE_JOIN(t1_name [, tl_name])` 提示优化器使用 Index Nested Loop Merge Join 算法，该算法与 Index Nested Loop Join 使用条件完全一样。

### NO_INDEX_MERGE_JOIN(t1_name [, tl_name ...])

`NO_INDEX_MERGE_JOIN(t1_name [, tl_name ...])` 提示优化器对指定表不要使用 Index Nested Loop Merge Join 算法。

### HASH_JOIN(t1_name [, tl_name ...])

`HASH_JOIN(t1_name [, tl_name ...])` 提示优化器对指定表使用 Hash Join 算法。这个算法多线程并发执行，执行速度较快，但会消耗较多内存。例如：

{{< copyable "sql" >}}

```sql
SELECT /*+ HASH_JOIN(t1, t2) */ * FROM t1, t2 WHERE t1.id = t2.id;
```

> **注意：**
>
> `HASH_JOIN` 的别名是 `TIDB_HJ`，在 3.0.x 及之前版本仅支持使用该别名；之后的版本同时支持使用这两种名称，推荐使用 `HASH_JOIN`。

### NO_HASH_JOIN(t1_name [, tl_name ...])

`NO_HASH_JOIN(t1_name [, tl_name ...])` 提示优化器对指定表不要使用 Hash Join 算法。例如：

{{< copyable "sql" >}}

```sql
SELECT /*+ NO_HASH_JOIN(t1, t2) */ * FROM t1, t2 WHERE t1.id = t2.id;
```

### HASH_JOIN_BUILD(t1_name [, tl_name ...])

`HASH_JOIN_BUILD(t1_name [, tl_name ...])` 提示优化器对指定表使用 Hash Join 算法，同时将指定表作为 Hash Join 算法的 Build 端，即用指定表来构建哈希表。例如：

```sql
SELECT /*+ HASH_JOIN_BUILD(t1) */ * FROM t1, t2 WHERE t1.id = t2.id;
```

### HASH_JOIN_PROBE(t1_name [, tl_name ...])

`HASH_JOIN_PROBE(t1_name [, tl_name ...])` 提示优化器对指定表使用 Hash Join 算法，同时将指定表作为 Hash Join 算法的探测（Probe）端，即用指定表作为探测端来执行 Hash Join 算法。例如：

```sql
SELECT /*+ HASH_JOIN_PROBE(t2) */ * FROM t1, t2 WHERE t1.id = t2.id;
```

### SEMI_JOIN_REWRITE()

`SEMI_JOIN_REWRITE()` 提示优化器将查询语句中的半连接 (Semi Join) 改写为普通的内连接。目前该 Hint 只作用于 `EXISTS` 子查询。

如果不使用该 Hint 进行改写，Semi Join 在选择 Hash Join 的执行方式时，只能够使用子查询构建哈希表，因此在子查询比外查询结果集大时，执行速度可能会不及预期。Semi Join 在选择 Index Join 的执行方式时，只能够使用外查询作为驱动表，因此在子查询比外查询结果集小时，执行速度可能会不及预期。

在使用了 `SEMI_JOIN_REWRITE()` 进行改写后，优化器便可以扩大选择范围，选择更好的执行方式。

{{< copyable "sql" >}}

```sql
-- 不使用 SEMI_JOIN_REWRITE() 进行改写
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
-- 使用 SEMI_JOIN_REWRITE() 进行改写
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

在上述例子中可以看到，在使用了 Hint 之后，TiDB 可以选择由表 `t1` 作为驱动表的 IndexJoin 的执行方式。

### NO_DECORRELATE()

`NO_DECORRELATE()` 提示优化器不要尝试解除指定查询块中对应子查询的关联。该 Hint 适用于包含关联列的 `EXISTS`、`IN`、`ANY`、`ALL`、`SOME` 和标量子查询，即关联子查询。

将该 Hint 写在一个查询块中后，对于该子查询和其外部查询块之间的关联列，优化器将不再尝试解除关联，而是始终使用 Apply 算子来执行查询。

默认情况下，TiDB 会尝试对关联子查询[解除关联](/correlated-subquery-optimization.md)，以达到更高的执行效率。但是在[一部分场景](/correlated-subquery-optimization.md#限制)下，解除关联反而会降低执行效率。这种情况下，可以使用该 Hint 来人工提示优化器不要进行解除关联操作。例如：

{{< copyable "sql" >}}

```sql
create table t1(a int, b int);
create table t2(a int, b int, index idx(b));
```

{{< copyable "sql" >}}

```sql
-- 不使用 NO_DECORRELATE()
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

从以上执行计划中可以发现，优化器自动解除了关联。解除关联之后的执行计划不包含 Apply 算子，取而代之的是子查询和外部查询块之间的 Join 运算，而原本的带有关联列的过滤条件 `t2.b = t1.b` 也变成了一个普通的 join 条件。

{{< copyable "sql" >}}

```sql
-- 使用 NO_DECORRELATE()
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

从以上执行计划中可以发现，优化器没有解除关联。执行计划中包含 Apply 算子，而带有关联列的条件 `t2.b = t1.b` 仍然是访问 `t2` 表时的过滤条件。

### HASH_AGG()

`HASH_AGG()` 提示优化器对指定查询块中所有聚合函数使用 Hash Aggregation 算法。这个算法多线程并发执行，执行速度较快，但会消耗较多内存。例如：

{{< copyable "sql" >}}

```sql
SELECT /*+ HASH_AGG() */ count(*) FROM t1, t2 WHERE t1.a > 10 GROUP BY t1.id;
```

### STREAM_AGG()

`STREAM_AGG()` 提示优化器对指定查询块中所有聚合函数使用 Stream Aggregation 算法。这个算法通常会占用更少的内存，但执行时间会更久。数据量太大，或系统内存不足时，建议尝试使用。例如：

{{< copyable "sql" >}}

```sql
SELECT /*+ STREAM_AGG() */ count(*) FROM t1, t2 WHERE t1.a > 10 GROUP BY t1.id;
```

### USE_INDEX(t1_name, idx1_name [, idx2_name ...])

`USE_INDEX(t1_name, idx1_name [, idx2_name ...])` 提示优化器对指定表仅使用给出的索引。

下面例子的效果等价于 `SELECT * FROM t t1 use index(idx1, idx2);`：

{{< copyable "sql" >}}

```sql
SELECT /*+ USE_INDEX(t1, idx1, idx2) */ * FROM t1;
```

> **注意：**
>
> 当该 Hint 中只指定表名，不指定索引名时，表示不考虑使用任何索引，而是选择全表扫。

### FORCE_INDEX(t1_name, idx1_name [, idx2_name ...])

`FORCE_INDEX(t1_name, idx1_name [, idx2_name ...])` 提示优化器对指定表仅使用给出的索引。

`FORCE_INDEX(t1_name, idx1_name [, idx2_name ...])` 的使用方法、作用和 `USE_INDEX(t1_name, idx1_name [, idx2_name ...])` 相同。

以下四个查询语句的效果相同：

{{< copyable "sql" >}}

```sql
SELECT /*+ USE_INDEX(t, idx1) */ * FROM t;
SELECT /*+ FORCE_INDEX(t, idx1) */ * FROM t;
SELECT * FROM t use index(idx1);
SELECT * FROM t force index(idx1);
```

### IGNORE_INDEX(t1_name, idx1_name [, idx2_name ...])

`IGNORE_INDEX(t1_name, idx1_name [, idx2_name ...])` 提示优化器对指定表忽略给出的索引。

下面例子的效果等价于 `SELECT * FROM t t1 ignore index(idx1, idx2);`：

{{< copyable "sql" >}}

```sql
SELECT /*+ IGNORE_INDEX(t1, idx1, idx2) */ * FROM t t1;
```

### ORDER_INDEX(t1_name, idx1_name [, idx2_name ...])

`ORDER_INDEX(t1_name, idx1_name [, idx2_name ...])` 提示优化器对指定表仅使用给出的索引，并且按顺序读取指定的索引。

> **警告：**
>
> 这个 Hint 有可能会导致 SQL 语句报错，建议先进行测试。如果测试时发生报错，请移除该 Hint。如果测试时运行正常，则可以继续使用。

此 Hint 通常应用在下面这种场景中：

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

优化器对该查询会生成两类计划：`Limit + IndexScan(keep order: true)` 和 `TopN + IndexScan(keep order: false)`，当使用了 `ORDER_INDEX` Hint，优化器会选择前一种按照顺序读取索引的计划。

> **注意：**
>
> - 如果查询本身并不需要按顺序读取索引，即在不使用 Hint 的前提下，优化器在任何情况下都不会生成按顺序读取索引的计划。此时，如果指定了 `ORDER_INDEX` Hint，会出现报错 `Can't find a proper physical plan for this query`，此时应考虑移除对应的 `ORDER_INDEX` Hint。
>
> - 分区表上的索引无法支持按顺序读取，所以不应该对分区表及其相关的索引使用 `ORDER_INDEX` Hint。

### NO_ORDER_INDEX(t1_name, idx1_name [, idx2_name ...])

`NO_ORDER_INDEX(t1_name, idx1_name [, idx2_name ...])` 提示优化器对指定表仅使用给出的索引，并且不按顺序读取指定的索引。通常应用在下面这种场景中:

以下示例中查询语句的效果等价于 `SELECT * FROM t t1 use index(idx1, idx2);`：

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

和 `ORDER_INDEX` Hint 的示例相同，优化器对该查询会生成两类计划：`Limit + IndexScan(keep order: true)` 和 `TopN + IndexScan(keep order: false)`，当使用了 `NO_ORDER_INDEX` Hint，优化器会选择后一种不按照顺序读取索引的计划。

### AGG_TO_COP()

`AGG_TO_COP()` 提示优化器将指定查询块中的聚合函数下推到 coprocessor。如果优化器没有下推某些适合下推的聚合函数，建议尝试使用。例如：

{{< copyable "sql" >}}

```sql
SELECT /*+ AGG_TO_COP() */ sum(t1.a) FROM t t1;
```

### LIMIT_TO_COP()

`LIMIT_TO_COP()` 提示优化器将指定查询块中的 `Limit` 和 `TopN` 算子下推到 coprocessor。优化器没有下推 `Limit` 或者 `TopN` 算子时建议尝试使用该提示。例如：

{{< copyable "sql" >}}

```sql
SELECT /*+ LIMIT_TO_COP() */ * FROM t WHERE a = 1 AND b > 10 ORDER BY c LIMIT 1;
```

### READ_FROM_STORAGE(TIFLASH[t1_name [, tl_name ...]], TIKV[t2_name [, tl_name ...]])

`READ_FROM_STORAGE(TIFLASH[t1_name [, tl_name ...]], TIKV[t2_name [, tl_name ...]])` 提示优化器从指定的存储引擎来读取指定的表，目前支持的存储引擎参数有 `TIKV` 和 `TIFLASH`。如果为表指定了别名，就只能使用表的别名作为 `READ_FROM_STORAGE()` 的参数；如果没有指定别名，则用表的本名作为其参数。例如：

{{< copyable "sql" >}}

```sql
SELECT /*+ READ_FROM_STORAGE(TIFLASH[t1], TIKV[t2]) */ t1.a FROM t t1, t t2 WHERE t1.a = t2.a;
```

### USE_INDEX_MERGE(t1_name, idx1_name [, idx2_name ...])

`USE_INDEX_MERGE(t1_name, idx1_name [, idx2_name ...])` 提示优化器通过索引合并的方式来访问指定的表。索引合并分为并集型和交集型两种类型，详情参见[用 EXPLAIN 查看索引合并的 SQL 执行计划](/explain-index-merge.md)。

若显式地指定索引列表，优化器会尝试在索引列表中选取索引来构建索引合并。若不指定索引列表，优化器会尝试在所有可用的索引中选取索引来构建索引合并。

对于交集型索引合并，索引列表是必选参数。对于并集型索引合并，Hint 中的索引列表为可选参数。示例如下。

{{< copyable "sql" >}}

```sql
SELECT /*+ USE_INDEX_MERGE(t1, idx_a, idx_b, idx_c) */ * FROM t1 WHERE t1.a > 10 OR t1.b > 10;
```

当对同一张表有多个 `USE_INDEX_MERGE` Hint 时，优化器会从这些 Hint 指定的索引列表的并集中尝试选取索引。

> **注意：**
>
> `USE_INDEX_MERGE` 的参数是索引名，而不是列名。对于主键索引，索引名为 `primary`。

### LEADING(t1_name [, tl_name ...])

`LEADING(t1_name [, tl_name ...])` 提示优化器在生成多表连接的执行计划时，按照 hint 中表名出现的顺序来确定多表连接的顺序。例如：

{{< copyable "sql" >}}

```sql
SELECT /*+ LEADING(t1, t2) */ * FROM t1, t2, t3 WHERE t1.id = t2.id and t2.id = t3.id;
```

在以上多表连接查询语句中，`LEADING()` 中表出现的顺序决定了优化器将会先对表 `t1` 和 `t2` 进行连接，再将结果和表 `t3` 进行连接。该 hint 比 [`STRAIGHT_JOIN`](#straight_join) 更为通用。

`LEADING` hint 在以下情况下会失效：

+ 指定了多个 `LEADING` hint
+ `LEADING` hint 中指定的表名不存在
+ `LEADING` hint 中指定了重复的表名
+ 优化器无法按照 `LEADING` hint 指定的顺序进行表连接
+ 已经存在 `straight_join()` hint
+ 查询语句中包含 outer join 且同时指定了包含笛卡尔积的情况
+ 和选择 join 算法的 hint（即 `MERGE_JOIN`、`INL_JOIN`、`INL_HASH_JOIN`、`HASH_JOIN`）同时使用时

当出现了上述失效的情况，会输出 warning 警告。

```sql
-- 指定了多个 LEADING hint

SELECT /*+ LEADING(t1, t2) LEADING(t3) */ * FROM t1, t2, t3 WHERE t1.id = t2.id and t2.id = t3.id;

-- 通过执行 `show warnings` 了解具体产生冲突的原因

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
> 如果查询语句中包含了 outer join，你只能在 hint 中指定可以用于交换连接顺序的表。如果 hint 中存在不能用于交换的表，则该 hint 会失效。例如在 `SELECT * FROM t1 LEFT JOIN (t2 JOIN t3 JOIN t4) ON t1.a = t2.a;` 中，如果想要控制 `t2`、`t3`、`t4` 表的连接顺序，那么在使用 `LEADING` hint 时，hint 中不能出现 `t1` 表。

### MERGE()

在含有[公共表表达式](/develop/dev-guide-use-common-table-expression.md)的查询中使用 `MERGE()` hint，可关闭对当前子查询的物化过程，并将内部查询的内联展开到外部查询。该 hint 适用于非递归的公共表表达式查询，在某些场景下，使用该 hint 会比默认分配一块临时空间的语句执行效率更高。例如将外部查询的条件下推或在嵌套的 CTE 查询中： 

{{< copyable "sql" >}}

```sql
-- 使用 hint 将外部查询条件的谓词下推
WITH CTE AS (SELECT /*+ MERGE() */ * FROM tc WHERE tc.a < 60) SELECT * FROM CTE WHERE CTE.a <18;

-- 在嵌套 CTE 查询中使用该 hint 来指定将某个 CTE 内联展开到外部查询
WITH CTE1 AS (SELECT * FROM t1), CTE2 AS (WITH CTE3 AS (SELECT /*+ MERGE() */ * FROM t2), CTE4 AS (SELECT * FROM t3) SELECT * FROM CTE3, CTE4) SELECT * FROM CTE1, CTE2;
```

> **注意：**
>
> `MERGE()` 只适用于简单的 CTE 查询，在以下情况下无法使用该 hint：
> 
> - [递归的 CTE 查询](/develop/dev-guide-use-common-table-expression.md#递归的-cte)
> - 子查询中有无法进行内联展开的部分，例如聚合算子、窗口函数以及 `DINSTINCT` 等
> 
> 当 CTE 引用次数过多时，查询性能可能低于默认的物化方式。

## 全局生效的 Hint

全局生效的 Hint 和[视图](/views.md)有关，可以使查询中定义的 Hint 能够在视图内部生效。添加这类 Hint 需要两步：先用 `QB_NAME` Hint 为视图内的查询块命名，再以“视图名@查询块名”的方式加入实际需要的 Hint。

### 第 1 步：使用 `QB_NAME` Hint 重命名视图内的查询块

首先使用 [`QB_NAME` Hint](#qb_name) 重命名视图内部的查询块。其中针对视图的 `QB_NAME` Hint 的概念与[查询块范围生效的 `QB_NAME` Hint](#qb_name)相同，只是在语法上进行了相应的拓展。从 `QB_NAME(QB)` 拓展为 `QB_NAME(QB, 视图名@查询块名 [.视图名@查询块名 .视图名@查询块名 ...])`。

> **注意：**
>
> `@查询块名` 与后面紧跟的 `.视图名@查询块名` 部分之间需要有一个空格，否则 `.视图名@查询块名` 会被视作前面 `@查询块名` 的一部分。例如，`QB_NAME(v2_1, v2@SEL_1 .@SEL_1)` 不能写为 `QB_NAME(v2_1, v2@SEL_1.@SEL_1)`。

- 对于单个视图、不包含子查询的简单语句，下面以重命名视图 `v` 的第一个查询块为例：

    ```sql
    SELECT /* 注释：当前查询块的名字为默认的 @SEL_1 */ * FROM v;
    ```

    对于视图 `v` 来说，从查询语句开始的首个视图是 `v@SEL_1`。视图 `v` 的第一个查询块可以声明为 `QB_NAME(v_1, v@SEL_1 .@SEL_1)`，也可以省略 `@SEL_1` 简写成 `QB_NAME(v_1, v)`：

    ```sql
    CREATE VIEW v AS SELECT /* 注释：当前查询块的名字为默认的 @SEL_1 */ * FROM t;

    -- 使用全局生效的 Hint
    SELECT /*+ QB_NAME(v_1, v) USE_INDEX(t@v_1, idx) */ * FROM v;
    ```

- 对于嵌套视图和包含子查询的复杂语句，下面以重命名视图 `v1`、`v2` 的两个查询块为例：

    ```sql
    SELECT /* 注释：当前查询块的名字为默认的 @SEL_1 */ * FROM v2 JOIN (
        SELECT /* 注释：当前查询块的名字为默认的 @SEL_2 */ * FROM v2) vv;
    ```

    对于第一个视图 `v2` 来说，从上面的语句开始的首个视图是 `v2@SEL_1`。对于第二个视图 `v2` 来说，首个视图表为 `v2@SEL_2`。下面的查询部分仅考虑第一个视图 `v2`。

    视图 `v2` 的第一个查询块可以声明为 `QB_NAME(v2_1, v2@SEL_1 .@SEL_1)`，视图 `v2` 的第二个查询块可以声明为 `QB_NAME(v2_2, v2@SEL_1 .@SEL_2)`：

    ```sql
    CREATE VIEW v2 AS
        SELECT * FROM t JOIN /* 注释：对于视图 v2 来说，当前查询块的名字为默认的 @SEL_1，因此当前查询块的视图列表是 v2@SEL_1 .@SEL_1 */
        (
            SELECT COUNT(*) FROM t1 JOIN v1 /* 注释：对于视图 v2 来说，当前查询块的名字为默认的 @SEL_2，因此当前查询块的视图列表是 v2@SEL_1 .@SEL_2 */
        ) tt;
    ```

    对于视图 `v1` 来说，从上面的语句开始的首个视图是 `v2@SEL_1 .v1@SEL_2`。视图 `v1` 的第一个查询块可以声明为 `QB_NAME(v1_1, v2@SEL_1 .v1@SEL_2 .@SEL_1)`，视图 `v1` 的第二个查询块可以声明为 `QB_NAME(v1_2, v2@SEL_1 .v1@SEL_2 .@SEL_2)`：

    ```sql
    CREATE VIEW v1 AS SELECT * FROM t JOIN /* 注释：对于视图 v1 来说，当前查询块的名字为默认的 @SEL_1，因此当前查询块的视图列表是 v2@SEL_1 .v1@SEL_2 .@SEL_1 */
        (
            SELECT COUNT(*) FROM t1 JOIN t2 /* 注释：对于视图 v1 来说，当前查询块的名字为默认的 @SEL_2，因此当前查询块的视图列表是 v2@SEL_1 .v1@SEL_2 .@SEL_2 */
        ) tt;
    ```

> **注意：**
>
> - 与视图相关的全局生效的 Hint 必须先定义了对应的 `QB_NAME` Hint 才能使用。
>
> - 使用一个 Hint 来指定视图内的多个表名时，需要保证在同一个 Hint 中出现的表名处于同一个视图的同一个查询块中。
>
> - 对于最外层的查询来说，在定义和视图相关的 `QB_NAME` Hint 时：
>
>     - 对于 `QB_NAME` Hint 中视图列表序列的第一项，在不显式声明 `@SEL_` 时，默认和定义 `QB_NAME` Hint 的查询块位置保持一致，即省略 `@SEL_` 的查询 `SELECT /*+ QB_NAME(qb1, v2) */ * FROM v2 JOIN (SELECT /*+ QB_NAME(qb2, v2) */ * FROM v2) vv;` 相当于 `SELECT /*+ QB_NAME(qb1, v2@SEL_1) */ * FROM v2 JOIN (SELECT /*+ QB_NAME(qb2, v2@SEL_2) */ * FROM v2) vv;`。
>     - 对于 `QB_NAME` Hint 中视图列表序列第一项之外的其他部分，只有 `@SEL_1` 可省略。即，如果声明处于当前部分的第一个查询块中，则 `@SEL_1` 可以省略，否则，不能省略 `@SEL_`。对于上面的例子：
>         - 视图 `v2` 的第一个查询块可以声明为 `QB_NAME(v2_1, v2)`
>         - 视图 `v2` 的第二个查询块可以声明为 `QB_NAME(v2_2, v2.@SEL_2)`
>         - 视图 `v1` 的第一个查询块可以声明为 `QB_NAME(v1_1, v2.v1@SEL_2)`
>         - 视图 `v1` 的第二个查询块可以声明为 `QB_NAME(v1_2, v2.v1@SEL_2 .@SEL_2)`

### 第 2 步：添加实际需要的 Hint

在定义好视图查询块部分的 `QB_NAME` Hint 后，你可以通过查询块的名字使用[查询块范围生效的 Hint](#查询块范围生效的-hint)，以“视图名@查询块名”的方式加入实际需要的 Hint，使其在视图内部生效。例如：

- 指定视图 `v2` 中第一个查询块的 `MERGE_JOIN()` Hint：

    ```sql
    SELECT /*+ QB_NAME(v2_1, v2) merge_join(t@v2_1) */ * FROM v2;
    ```

- 指定视图 `v2` 中第二个查询块的 `MERGE_JOIN()` 和 `STREAM_AGG()` Hint：

    ```sql
    SELECT /*+ QB_NAME(v2_2, v2.@SEL_2) merge_join(t1@v2_2) stream_agg(@v2_2) */ * FROM v2;
    ```

- 指定视图 `v1` 中第一个查询块的 `HASH_JOIN()` Hint：

    ```sql
    SELECT /*+ QB_NAME(v1_1, v2.v1@SEL_2) hash_join(t@v1_1) */ * FROM v2;
    ```

- 指定视图 `v1` 中第二个查询块的 `HASH_JOIN()` 和 `HASH_AGG()` Hint：

    ```sql
    SELECT /*+ QB_NAME(v1_2, v2.v1@SEL_2 .@SEL_2) hash_join(t1@v1_2) hash_agg(@v1_2) */ * FROM v2;
    ```

## 查询范围生效的 Hint

这类 Hint 只能跟在语句中**第一个** `SELECT`、`UPDATE` 或 `DELETE` 关键字的后面，等同于在当前这条查询运行时对指定的系统变量进行修改，其优先级高于现有系统变量的值。

> **注意：**
>
> 这类 Hint 虽然也有隐藏的可选变量 `@QB_NAME`，但就算指定了该值，Hint 还是会在整个查询范围生效。

### NO_INDEX_MERGE()

`NO_INDEX_MERGE()` 会关闭优化器的 index merge 功能。

下面的例子不会使用 index merge：

{{< copyable "sql" >}}

```sql
SELECT /*+ NO_INDEX_MERGE() */ * FROM t WHERE t.a > 0 or t.b > 0;
```

除了 Hint 外，系统变量 `tidb_enable_index_merge` 也能决定是否开启该功能。

> **注意：**
>
> - `NO_INDEX_MERGE` 优先级高于 `USE_INDEX_MERGE`，当这两类 Hint 同时存在时，`USE_INDEX_MERGE` 不会生效。
> - 当存在子查询时，`NO_INDEX_MERGE` 放在最外层才能生效。

### USE_TOJA(boolean_value)

参数 `boolean_value` 可以是 `TRUE` 或者 `FALSE`。`USE_TOJA(TRUE)` 会开启优化器尝试将 in (subquery) 条件转换为 join 和 aggregation 的功能。相对地，`USE_TOJA(FALSE)` 会关闭该功能。

下面的例子会将 `in (SELECT t2.a FROM t2) subq` 转换为等价的 join 和 aggregation：

{{< copyable "sql" >}}

```sql
SELECT /*+ USE_TOJA(TRUE) */ t1.a, t1.b FROM t1 WHERE t1.a in (SELECT t2.a FROM t2) subq;
```

除了 Hint 外，系统变量 `tidb_opt_insubq_to_join_and_agg` 也能决定是否开启该功能。

### MAX_EXECUTION_TIME(N)

`MAX_EXECUTION_TIME(N)` 把语句的执行时间限制在 `N` 毫秒以内，超时后服务器会终止这条语句的执行。

下面的 Hint 设置了 1000 毫秒（即 1 秒）超时：

{{< copyable "sql" >}}

```sql
SELECT /*+ MAX_EXECUTION_TIME(1000) */ * FROM t1 inner join t2 WHERE t1.id = t2.id;
```

除了 Hint 之外，系统变量 `global.max_execution_time` 也能对语句执行时间进行限制。

### MEMORY_QUOTA(N)

`MEMORY_QUOTA(N)` 用于限制语句执行时的内存使用。该 Hint 支持 MB 和 GB 两种单位。内存使用超过该限制时会根据当前设置的内存超限行为来打出一条 log 或者终止语句的执行。

下面的 Hint 设置了 1024 MB 的内存限制：

{{< copyable "sql" >}}

```sql
SELECT /*+ MEMORY_QUOTA(1024 MB) */ * FROM t;
```

除了 Hint 外，系统变量 [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query) 也能限制语句执行的内存使用。

### READ_CONSISTENT_REPLICA()

`READ_CONSISTENT_REPLICA()` 会开启从数据一致的 TiKV follower 节点读取数据的特性。

下面的例子会从 follower 节点读取数据：

{{< copyable "sql" >}}

```sql
SELECT /*+ READ_CONSISTENT_REPLICA() */ * FROM t;
```

除了 Hint 外，环境变量 `tidb_replica_read` 设为 `'follower'` 或者 `'leader'` 也能决定是否开启该特性。

### IGNORE_PLAN_CACHE()

`IGNORE_PLAN_CACHE()` 提示优化器在处理当前 `prepare` 语句时不使用 plan cache。

该 Hint 用于在 [Prepared Plan Cache](/sql-prepared-plan-cache.md) 开启的场景下临时对某类查询禁用 plan cache。

以下示例强制该 `prepare` 语句不使用 plan cache：

{{< copyable "sql" >}}

```sql
prepare stmt FROM 'SELECT  /*+ IGNORE_PLAN_CACHE() */ * FROM t WHERE t.id = ?';
```

### STRAIGHT_JOIN()

`STRAIGHT_JOIN()` 提示优化器在生成表连接顺序时按照表名在 `FROM` 子句中出现的顺序进行连接。

{{< copyable "sql" >}}

```sql
SELECT /*+ STRAIGHT_JOIN() */ * FROM t t1, t t2 WHERE t1.a = t2.a;
```

> **注意：**
>
> - `STRAIGHT_JOIN` 优先级高于 `LEADING`，当这两类 Hint 同时存在时，`LEADING` 不会生效。
> - 建议使用 `LEADING` Hint，它比 `STRAIGHT_JOIN` Hint 更通用。

### NTH_PLAN(N)

`NTH_PLAN(N)` 提示优化器选用在物理优化阶段搜索到的第 `N` 个物理计划。`N` 必须是正整数。

如果指定的 `N` 超出了物理优化阶段的搜索范围，TiDB 会返回 warning，并根据不存在该 Hint 时一样的策略选择最优物理计划。

该 Hint 在启用 cascades planner 的情况下不会生效。

以下示例会强制优化器在物理阶段选择搜索到的第 3 个物理计划：

{{< copyable "sql" >}}

```sql
SELECT /*+ NTH_PLAN(3) */ count(*) from t where a > 5;
```

> **注意：**
>
> `NTH_PLAN(N)` 主要用于测试用途，并且在未来不保证其兼容性，请谨慎使用。

## 常见 Hint 不生效问题排查

### MySQL 命令行客户端清除 Hint 导致不生效

MySQL 命令行客户端在 5.7.7 版本之前默认清除了 Optimizer Hints。如果需要在这些早期版本的客户端中使用 Hint 语法，需要在启动客户端时加上 `--comments` 选项。例如 `mysql -h 127.0.0.1 -P 4000 -uroot --comments`。

### 创建连接时不指定库名导致 Hint 不生效

如果创建连接时未指定数据库名，则可能出现 Hint 失效的情况。例如：

使用 `mysql -h127.0.0.1 -P4000 -uroot` 命令连接数据库时，未使用 `-D` 参数指定数据库名。然后执行下面的 SQL 语句：

```sql
SELECT /*+ use_index(t, a) */ a FROM test.t;
SHOW WARNINGS;
```

由于无法识别表 `t` 对应的数据库名，因此 `use_index(t, a)` Hint 无法生效。

```sql
+---------+------+----------------------------------------------------------------------+
| Level   | Code | Message                                                              |
+---------+------+----------------------------------------------------------------------+
| Warning | 1815 | use_index(.t, a) is inapplicable, check whether the table(.t) exists |
+---------+------+----------------------------------------------------------------------+
1 row in set (0.00 sec)
```

### 跨库查询不指定库名导致 Hint 不生效

对于跨库查询中需要访问的表，需要显式地指定数据库名，否则可能出现 Hint 失效的情况。例如执行下面跨库查询的 SQL 语句：

```sql
USE test1;
CREATE TABLE t1(a INT, KEY(a));
USE test2;
CREATE TABLE t2(a INT, KEY(a));
SELECT /*+ use_index(t1, a) */ * FROM test1.t1, t2;
SHOW WARNINGS;
```

由于 `t1` 不在当前数据库 `test2` 下，因此 `use_index(t1, a)` Hint 无法被正确地识别。

```sql
+---------+------+----------------------------------------------------------------------------------+
| Level   | Code | Message                                                                          |
+---------+------+----------------------------------------------------------------------------------+
| Warning | 1815 | use_index(test2.t1, a) is inapplicable, check whether the table(test2.t1) exists |
+---------+------+----------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

此时，需要显式地指定库名，即将 `use_index(t1, a)` 修改为 `use_index(test1.t1, a)`。

### Hint 位置不正确导致不生效

如果没有按照 Optimizer Hints 语法将 Hint 正确地放在指定关键字的后面，它将无法生效。例如：

```sql
SELECT * /*+ use_index(t, a) */ FROM t;
SHOW WARNINGS;
```

Warning 信息如下：

```sql
+---------+------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Level   | Code | Message                                                                                                                                                                                                                 |
+---------+------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Warning | 1064 | You have an error in your SQL syntax; check the manual that corresponds to your TiDB version for the right syntax to use [parser:8066]Optimizer hint can only be followed by certain keywords like SELECT, INSERT, etc. |
+---------+------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.01 sec)
```

在上面的示例中，你需要将 Hint 直接放在 `SELECT` 关键字之后。具体的语法规则参见 [Hint 语法](#语法)部分。

### `INL_JOIN` Hint 不生效

#### 关联表的列上使用内置函数导致 `INL_JOIN` Hint 不生效

在某些情况下，如果在关联表的列上使用了内置函数，优化器可能无法选择 `IndexJoin` 计划，导致 `INL_JOIN` Hint 也无法生效。

例如，以下查询在关联表的列 `tname` 上使用了内置函数 `substr`：

```sql
CREATE TABLE t1 (id varchar(10) primary key, tname varchar(10));
CREATE TABLE t2 (id varchar(10) primary key, tname varchar(10));
EXPLAIN SELECT /*+ INL_JOIN(t1, t2) */ * FROM t1, t2 WHERE t1.id=t2.id and SUBSTR(t1.tname,1,2)=SUBSTR(t2.tname,1,2);
```

查询计划输出结果如下：

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

从该示例中可以看到，`INL_JOIN` Hint 没有生效。该问题的根本原因是优化器限制导致无法使用 `Projection` 或者 `Selection` 算子作为 `IndexJoin` 的探测 (Probe) 端。

从 TiDB v8.0.0 起，你通过设置 [`tidb_enable_inl_join_inner_multi_pattern`](/system-variables.md#tidb_enable_inl_join_inner_multi_pattern-从-v700-版本开始引入) 为 `ON` 来避免该问题。

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

#### 排序规则不兼容导致 `INL_JOIN` Hint 不生效

如果两个表的 Join key 的排序规则不能兼容，将无法使用 IndexJoin 来执行查询。此时 [`INL_JOIN` Hint](#inl_joint1_name--tl_name-) 将无法生效。例如：

```sql
CREATE TABLE t1 (k varchar(8), key(k)) COLLATE=utf8mb4_general_ci;
CREATE TABLE t2 (k varchar(8), key(k)) COLLATE=utf8mb4_bin;
EXPLAIN SELECT /*+ tidb_inlj(t1) */ * FROM t1, t2 WHERE t1.k=t2.k;
```

查询计划输出结果如下：

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

上面的 SQL 语句中 `t1.k` 和 `t2.k` 的排序规则不能相互兼容（分别为 `utf8mb4_general_ci` 和 `utf8mb4_bin`），导致 IndexJoin 无法适用。因此 `INL_JOIN` 或 `TIDB_INLJ` Hint 也无法生效。

```sql
SHOW WARNINGS;
+---------+------+----------------------------------------------------------------------------+
| Level   | Code | Message                                                                    |
+---------+------+----------------------------------------------------------------------------+
| Warning | 1815 | Optimizer Hint /*+ INL_JOIN(t1) */ or /*+ TIDB_INLJ(t1) */ is inapplicable |
+---------+------+----------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

#### 连接顺序导致 `INL_JOIN` Hint 不生效

[`INL_JOIN(t1, t2)`](#inl_joint1_name--tl_name-) 或 `TIDB_INLJ(t1, t2)` 的语义是让 `t1` 和 `t2` 作为 `IndexJoin` 的内表与其他表进行连接，而不是直接将 `t1` 和 `t2` 进行 `IndexJoin` 连接。例如：

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

在上面例子中，`t1` 和 `t3` 并没有直接被一个 `IndexJoin` 连接起来。

如果想要直接使用 `IndexJoin` 来连接 `t1` 和 `t3`，需要先使用 [`LEADING` Hint](#leadingt1_name--tl_name-) 指定 `t1` 和 `t3` 的连接顺序，然后再配合使用 `INL_JION`。例如：

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

### 使用 Hint 导致错误 `Can't find a proper physical plan for this query`

在下面几种情况下，可能会出现 `Can't find a proper physical plan for this query` 错误：

- 查询本身并不需要按顺序读取索引，即在不使用 Hint 的前提下，优化器在任何情况下都不会生成按顺序读取索引的计划。此时，如果指定了 `ORDER_INDEX` Hint，会出现此报错，此时应考虑移除对应的 `ORDER_INDEX` Hint。 
- 查询使用了 `NO_JOIN` 相关的 Hint 排除了所有可能的 Join 方式。

```sql
CREATE TABLE t1 (a INT);
CREATE TABLE t2 (a INT);
EXPLAIN SELECT /*+ NO_HASH_JOIN(t1), NO_MERGE_JOIN(t1) */ * FROM t1, t2 WHERE t1.a=t2.a;
ERROR 1815 (HY000): Internal : Can't find a proper physical plan for this query
```

- 系统变量 [`tidb_opt_enable_hash_join`](/system-variables.md#tidb_opt_enable_hash_join-从-v656-版本开始引入) 设置为 `OFF`，而且其他 Join 方式也都被排除了。

```sql
CREATE TABLE t1 (a INT);
CREATE TABLE t2 (a INT);
set tidb_opt_enable_hash_join=off;
EXPLAIN SELECT /*+ NO_MERGE_JOIN(t1) */ * FROM t1, t2 WHERE t1.a=t2.a;
ERROR 1815 (HY000): Internal : Can't find a proper physical plan for this query
```
