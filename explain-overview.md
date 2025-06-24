---
title: TiDB 查询执行计划概览
summary: 了解 TiDB 中 `EXPLAIN` 语句返回的执行计划信息。
---

# TiDB 查询执行计划概览

> **注意：**
>
> 当您使用 MySQL 客户端连接 TiDB 时，为了以更清晰的方式阅读输出结果而不换行，您可以使用 `pager less -S` 命令。然后，在 `EXPLAIN` 结果输出后，您可以按键盘上的右箭头键 <kbd>→</kbd> 来水平滚动输出。

SQL 是一种声明式语言。它描述了查询结果应该是什么样子，而**不是**如何获取这些结果的方法。TiDB 会考虑执行查询的所有可能方式，包括使用什么顺序来连接表以及是否可以使用任何潜在的索引。这个_考虑查询执行计划_的过程被称为 SQL 优化。

`EXPLAIN` 语句显示给定语句的选定执行计划。也就是说，在考虑了数百或数千种可能的查询执行方式之后，TiDB 认为这个_计划_将消耗最少的资源并在最短的时间内执行：

{{< copyable "sql" >}}

```sql
CREATE TABLE t (id INT NOT NULL PRIMARY KEY auto_increment, a INT NOT NULL, pad1 VARCHAR(255), INDEX(a));
INSERT INTO t VALUES (1, 1, 'aaa'),(2,2, 'bbb');
EXPLAIN SELECT * FROM t WHERE a = 1;
```

```sql
Query OK, 0 rows affected (0.96 sec)

Query OK, 2 rows affected (0.02 sec)
Records: 2  Duplicates: 0  Warnings: 0

+-------------------------------+---------+-----------+---------------------+---------------------------------------------+
| id                            | estRows | task      | access object       | operator info                               |
+-------------------------------+---------+-----------+---------------------+---------------------------------------------+
| IndexLookUp_10                | 10.00   | root      |                     |                                             |
| ├─IndexRangeScan_8(Build)     | 10.00   | cop[tikv] | table:t, index:a(a) | range:[1,1], keep order:false, stats:pseudo |
| └─TableRowIDScan_9(Probe)     | 10.00   | cop[tikv] | table:t             | keep order:false, stats:pseudo              |
+-------------------------------+---------+-----------+---------------------+---------------------------------------------+
3 rows in set (0.00 sec)
```

`EXPLAIN` 不会执行实际的查询。[`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md) 可以用来执行查询并显示 `EXPLAIN` 信息。这在诊断所选执行计划不理想的情况时很有用。有关使用 `EXPLAIN` 的更多示例，请参见以下文档：

* [索引](/explain-indexes.md)
* [连接](/explain-joins.md)
* [子查询](/explain-subqueries.md)
* [聚合](/explain-aggregation.md)
* [视图](/explain-views.md)
* [分区](/explain-partitions.md)

## 理解 EXPLAIN 输出

以下是对上述 `EXPLAIN` 语句输出的解释：

* `id` 描述了执行 SQL 语句所需的操作符或子任务的名称。有关更多详细信息，请参见[操作符概览](#操作符概览)。
* `estRows` 显示 TiDB 预计要处理的行数。这个数字可能基于字典信息（例如当访问方法基于主键或唯一键时），或者可能基于统计信息（如 CMSketch 或直方图）。
* `task` 显示操作符在哪里执行工作。有关更多详细信息，请参见[任务概览](#任务概览)。
* `access object` 显示正在访问的表、分区和索引。还显示了索引的组成部分，如上例中使用了索引中的列 `a`。这在您有复合索引的情况下很有用。
* `operator info` 显示有关访问的其他详细信息。有关更多详细信息，请参见[操作符信息概览](#操作符信息概览)。

> **注意：**
>
> 在返回的执行计划中，对于 `IndexJoin` 和 `Apply` 操作符的所有探测端（probe-side）子节点，从 v6.4.0 开始 `estRows` 的含义与 v6.4.0 之前不同。
>
> 在 v6.4.0 之前，`estRows` 表示探测端操作符对构建端（build side）操作符的每一行需要处理的估计行数。从 v6.4.0 开始，`estRows` 表示探测端操作符需要处理的估计行数的**总数**。在 `EXPLAIN ANALYZE` 结果中显示的实际行数（由 `actRows` 列表示）表示总行数，因此从 v6.4.0 开始，`IndexJoin` 和 `Apply` 操作符的探测端子节点的 `estRows` 和 `actRows` 的含义是一致的。
>
> 例如：
>
> ```sql
> CREATE TABLE t1(a INT, b INT);
> CREATE TABLE t2(a INT, b INT, INDEX ia(a));
> EXPLAIN SELECT /*+ INL_JOIN(t2) */ * FROM t1 JOIN t2 ON t1.a = t2.a;
> EXPLAIN SELECT (SELECT a FROM t2 WHERE t2.a = t1.b LIMIT 1) FROM t1;
> ```
>
> ```sql
> -- v6.4.0 之前：
> +---------------------------------+----------+-----------+-----------------------+-----------------------------------------------------------------------------------------------------------------+
> | id                              | estRows  | task      | access object         | operator info                                                                                                   |
> +---------------------------------+----------+-----------+-----------------------+-----------------------------------------------------------------------------------------------------------------+
> | IndexJoin_12                    | 12487.50 | root      |                       | inner join, inner:IndexLookUp_11, outer key:test.t1.a, inner key:test.t2.a, equal cond:eq(test.t1.a, test.t2.a) |
> | ├─TableReader_24(Build)         | 9990.00  | root      |                       | data:Selection_23                                                                                               |
> | │ └─Selection_23                | 9990.00  | cop[tikv] |                       | not(isnull(test.t1.a))                                                                                          |
> | │   └─TableFullScan_22          | 10000.00 | cop[tikv] | table:t1              | keep order:false, stats:pseudo                                                                                  |
> | └─IndexLookUp_11(Probe)         | 1.25     | root      |                       |                                                                                                                 |
> |   ├─Selection_10(Build)         | 1.25     | cop[tikv] |                       | not(isnull(test.t2.a))                                                                                          |
> |   │ └─IndexRangeScan_8          | 1.25     | cop[tikv] | table:t2, index:ia(a) | range: decided by [eq(test.t2.a, test.t1.a)], keep order:false, stats:pseudo                                    |
> |   └─TableRowIDScan_9(Probe)     | 1.25     | cop[tikv] | table:t2              | keep order:false, stats:pseudo                                                                                  |
> +---------------------------------+----------+-----------+-----------------------+-----------------------------------------------------------------------------------------------------------------+
> +---------------------------------+----------+-----------+-----------------------+------------------------------------------------------------------------------+
> | id                              | estRows  | task      | access object         | operator info                                                                |
> +---------------------------------+----------+-----------+-----------------------+------------------------------------------------------------------------------+
> | Projection_12                   | 10000.00 | root      |                       | test.t2.a                                                                    |
> | └─Apply_14                      | 10000.00 | root      |                       | CARTESIAN left outer join                                                    |
> |   ├─TableReader_16(Build)       | 10000.00 | root      |                       | data:TableFullScan_15                                                        |
> |   │ └─TableFullScan_15          | 10000.00 | cop[tikv] | table:t1              | keep order:false, stats:pseudo                                               |
> |   └─Limit_17(Probe)             | 1.00     | root      |                       | offset:0, count:1                                                            |
> |     └─IndexReader_21            | 1.00     | root      |                       | index:Limit_20                                                               |
> |       └─Limit_20                | 1.00     | cop[tikv] |                       | offset:0, count:1                                                            |
> |         └─IndexRangeScan_19     | 1.00     | cop[tikv] | table:t2, index:ia(a) | range: decided by [eq(test.t2.a, test.t1.b)], keep order:false, stats:pseudo |
> +---------------------------------+----------+-----------+-----------------------+------------------------------------------------------------------------------+
> 
> -- 从 v6.4.0 开始：
>
> -- 您可以发现从 v6.4.0 开始，`IndexLookUp_11`、`Selection_10`、`IndexRangeScan_8` 和 `TableRowIDScan_9` 的 `estRows` 列值与 v6.4.0 之前不同。
> +---------------------------------+----------+-----------+-----------------------+-----------------------------------------------------------------------------------------------------------------+
> | id                              | estRows  | task      | access object         | operator info                                                                                                   |
> +---------------------------------+----------+-----------+-----------------------+-----------------------------------------------------------------------------------------------------------------+
> | IndexJoin_12                    | 12487.50 | root      |                       | inner join, inner:IndexLookUp_11, outer key:test.t1.a, inner key:test.t2.a, equal cond:eq(test.t1.a, test.t2.a) |
> | ├─TableReader_24(Build)         | 9990.00  | root      |                       | data:Selection_23                                                                                               |
> | │ └─Selection_23                | 9990.00  | cop[tikv] |                       | not(isnull(test.t1.a))                                                                                          |
> | │   └─TableFullScan_22          | 10000.00 | cop[tikv] | table:t1              | keep order:false, stats:pseudo                                                                                  |
> | └─IndexLookUp_11(Probe)         | 12487.50 | root      |                       |                                                                                                                 |
> |   ├─Selection_10(Build)         | 12487.50 | cop[tikv] |                       | not(isnull(test.t2.a))                                                                                          |
> |   │ └─IndexRangeScan_8          | 12500.00 | cop[tikv] | table:t2, index:ia(a) | range: decided by [eq(test.t2.a, test.t1.a)], keep order:false, stats:pseudo                                    |
> |   └─TableRowIDScan_9(Probe)     | 12487.50 | cop[tikv] | table:t2              | keep order:false, stats:pseudo                                                                                  |
> +---------------------------------+----------+-----------+-----------------------+-----------------------------------------------------------------------------------------------------------------+
>
> -- 您可以发现从 v6.4.0 开始，`Limit_17`、`IndexReader_21`、`Limit_20` 和 `IndexRangeScan_19` 的 `estRows` 列值与 v6.4.0 之前不同。
> +---------------------------------+----------+-----------+-----------------------+------------------------------------------------------------------------------+
> | id                              | estRows  | task      | access object         | operator info                                                                |
> +---------------------------------+----------+-----------+-----------------------+------------------------------------------------------------------------------+
> | Projection_12                   | 10000.00 | root      |                       | test.t2.a                                                                    |
> | └─Apply_14                      | 10000.00 | root      |                       | CARTESIAN left outer join                                                    |
> |   ├─TableReader_16(Build)       | 10000.00 | root      |                       | data:TableFullScan_15                                                        |
> |   │ └─TableFullScan_15          | 10000.00 | cop[tikv] | table:t1              | keep order:false, stats:pseudo                                               |
> |   └─Limit_17(Probe)             | 10000.00 | root      |                       | offset:0, count:1                                                            |
> |     └─IndexReader_21            | 10000.00 | root      |                       | index:Limit_20                                                               |
> |       └─Limit_20                | 10000.00 | cop[tikv] |                       | offset:0, count:1                                                            |
> |         └─IndexRangeScan_19     | 10000.00 | cop[tikv] | table:t2, index:ia(a) | range: decided by [eq(test.t2.a, test.t1.b)], keep order:false, stats:pseudo |
> +---------------------------------+----------+-----------+-----------------------+------------------------------------------------------------------------------+
> ```

### 操作符概览

操作符是执行查询结果返回过程中的特定步骤。执行表扫描（磁盘或 TiKV Block Cache）的操作符列表如下：

- **TableFullScan**：全表扫描
- **TableRangeScan**：带指定范围的表扫描
- **TableRowIDScan**：基于 RowID 的表数据扫描。通常在索引读取操作后执行，用于检索匹配的数据行。
- **IndexFullScan**：类似于"全表扫描"，但扫描的是索引而不是表数据。
- **IndexRangeScan**：带指定范围的索引扫描。

TiDB 聚合从 TiKV/TiFlash 扫描的数据或计算结果。数据聚合操作符可以分为以下几类：

- **TableReader**：聚合 TiKV 中 `TableFullScan` 或 `TableRangeScan` 等底层操作符获取的数据。
- **IndexReader**：聚合 TiKV 中 `IndexFullScan` 或 `IndexRangeScan` 等底层操作符获取的数据。
- **IndexLookUp**：首先聚合 `Build` 端扫描的 RowID（在 TiKV 中）。然后在 `Probe` 端，基于这些 RowID 从 TiKV 中准确读取数据。在 `Build` 端有 `IndexFullScan` 或 `IndexRangeScan` 等操作符；在 `Probe` 端有 `TableRowIDScan` 操作符。
- **IndexMerge**：类似于 `IndexLookUp`。`IndexMerge` 可以看作是 `IndexLookupReader` 的扩展。`IndexMerge` 支持同时读取多个索引。有多个 `Build` 和一个 `Probe`。`IndexMerge` 的执行过程与 `IndexLookUp` 相同。

虽然结构看起来像一棵树，但执行查询并不严格要求子节点在父节点之前完成。TiDB 支持查询内并行，所以更准确的描述执行方式是子节点_流入_它们的父节点。父节点、子节点和兄弟节点_可能_会并行执行查询的各个部分。

在前面的示例中，`├─IndexRangeScan_8(Build)` 操作符找到匹配 `a(a)` 索引的行的内部 `RowID`。然后 `└─TableRowIDScan_9(Probe)` 操作符从表中检索这些行。

#### 范围查询

在 `WHERE`/`HAVING`/`ON` 条件中，TiDB 优化器分析主键查询或索引键查询返回的结果。例如，这些条件可能包括数字和日期类型的比较运算符，如 `>`、`<`、`=`、`>=`、`<=`，以及字符类型如 `LIKE`。

> **注意：**
>
> - 为了使用索引，条件必须是_可查询的_。例如，条件 `YEAR(date_column) < 1992` 不能使用索引，但 `date_column < '1992-01-01'` 可以。
> - 建议比较相同类型和[字符集和排序规则](/character-set-and-collation.md)的数据。混合类型可能需要额外的 `cast` 操作，或阻止使用索引。
> - 您也可以使用 `AND`（交集）和 `OR`（并集）来组合一个列的范围查询条件。对于多维复合索引，您可以使用多列中的条件。例如，对于复合索引 `(a, b, c)`：
>     - 当 `a` 是等值查询时，继续确定 `b` 的查询范围；当 `b` 也是等值查询时，继续确定 `c` 的查询范围。
>     - 否则，如果 `a` 是非等值查询，则只能确定 `a` 的范围。

### 任务概览

目前，TiDB 的计算任务可以分为两类：cop 任务和 root 任务。`cop[tikv]` 任务表示操作符在 TiKV 协处理器内执行。`root` 任务表示它将在 TiDB 内完成。

SQL 优化的目标之一是尽可能多地将计算下推到 TiKV。TiKV 中的协处理器支持大多数内置 SQL 函数（包括聚合函数和标量函数）、SQL `LIMIT` 操作、索引扫描和表扫描。

### 操作符信息概览

`operator info` 可以显示有用的信息，例如哪些条件可以被下推：

* `range: [1,1]` 显示查询的 where 子句中的谓词（`a = 1`）被直接下推到 TiKV（任务是 `cop[tikv]`）。
* `keep order:false` 显示此查询的语义不要求 TiKV 按顺序返回结果。如果查询被修改为需要排序（例如 `SELECT * FROM t WHERE a = 1 ORDER BY id`），则此条件将为 `keep order:true`。
* `stats:pseudo` 显示 `estRows` 中显示的估计可能不准确。TiDB 作为后台操作定期更新统计信息。也可以通过运行 `ANALYZE TABLE t` 手动更新。

不同的操作符在执行 `EXPLAIN` 语句后输出不同的信息。您可以使用优化器提示来控制优化器的行为，从而控制物理操作符的选择。例如，`/*+ HASH_JOIN(t1, t2) */` 表示优化器使用 `Hash Join` 算法。有关更多详细信息，请参见[优化器提示](/optimizer-hints.md)。
