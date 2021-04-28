---
title: EXPLAIN 概览
summary: 了解 TiDB 中 EXPLAIN 语句返回的执行计划。
aliases: ['/docs-cn/dev/query-execution-plan/','/docs-cn/dev/reference/performance/understanding-the-query-execution-plan/','/docs-cn/dev/index-merge/','/docs-cn/dev/reference/performance/index-merge/','/zh/tidb/dev/query-execution-plan/']
---

# `EXPLAIN` 概览

> **注意：**
>
> 使用 MySQL 客户端连接到 TiDB 时，为避免输出结果在终端中换行，可先执行 `pager less -S` 命令。执行命令后，新的 `EXPLAIN` 的输出结果不再换行，可按右箭头 <kbd>→</kbd> 键水平滚动阅读输出结果。

使用 `EXPLAIN` 可查看 TiDB 执行某条语句时选用的执行计划。也就是说，TiDB 在考虑上数百或数千种可能的执行计划后，最终认定该执行计划消耗的资源最少、执行的速度最快。

`EXPLAIN` 示例如下：

```sql
CREATE TABLE t (id INT NOT NULL PRIMARY KEY auto_increment, a INT NOT NULL, pad1 VARCHAR(255), INDEX(a));
INSERT INTO t VALUES (1, 1, 'aaa'),(2,2, 'bbb');
EXPLAIN SELECT * FROM t WHERE a = 1;
```

返回的结果如下：

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

`EXPLAIN` 实际不会执行查询。[`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md) 可用于实际执行查询并显示执行计划。如果 TiDB 所选的执行计划非最优，可用 `EXPLAIN` 或 `EXPLAIN ANALYZE` 来进行诊断。有关 `EXPLAIN` 用法的详细内容，参阅以下文档：

+ [MPP 模式查询的执行计划](/explain-mpp.md)
+ [索引查询的执行计划](/explain-indexes.md)
+ [Join 查询的执行计划](/explain-joins.md)
+ [子查询的执行计划](/explain-subqueries.md)
+ [聚合查询的执行计划](/explain-aggregation.md)
+ [视图查询的执行计划](/explain-views.md)
+ [分区查询的执行计划](/explain-partitions.md)
+ [开启 IndexMerge 查询的执行计划](/explain-index-merge.md)

## 解读 EXPLAIN 的返回结果

`EXPLAIN` 的返回结果包含以下字段：

+ `id` 为算子名，或执行 SQL 语句需要执行的子任务。详见[算子简介](#算子简介)。
+ `estRows` 为显示 TiDB 预计会处理的行数。该预估数可能基于字典信息（例如访问方法基于主键或唯一键），或基于 `CMSketch` 或直方图等统计信息估算而来。
+ `task` 显示算子在执行语句时的所在位置。详见 [Task 简介](#task-简介)。
+ `access-object` 显示被访问的表、分区和索引。显示的索引为部分索引。以上示例中 TiDB 使用了 `a` 列的索引。尤其是在有组合索引的情况下，该字段显示的信息很有参考意义。
+ `operator info` 显示访问表、分区和索引的其他信息。详见 [`operator info` 结果](#operator-info-结果)。

### 算子简介

算子是为返回查询结果而执行的特定步骤。真正执行扫表（读盘或者读 TiKV Block Cache）操作的算子有如下几类：

- **TableFullScan**：全表扫描。
- **TableRangeScan**：带有范围的表数据扫描。
- **TableRowIDScan**：根据上层传递下来的 RowID 扫描表数据。时常在索引读操作后检索符合条件的行。
- **IndexFullScan**：另一种“全表扫描”，扫的是索引数据，不是表数据。
- **IndexRangeScan**：带有范围的索引数据扫描操作。

TiDB 会汇聚 TiKV/TiFlash 上扫描的数据或者计算结果，这种“数据汇聚”算子目前有如下几类：

- **TableReader**：将 TiKV 上底层扫表算子 TableFullScan 或 TableRangeScan 得到的数据进行汇总。
- **IndexReader**：将 TiKV 上底层扫表算子 IndexFullScan 或 IndexRangeScan 得到的数据进行汇总。
- **IndexLookUp**：先汇总 Build 端 TiKV 扫描上来的 RowID，再去 Probe 端上根据这些 `RowID` 精确地读取 TiKV 上的数据。Build 端是 `IndexFullScan` 或 `IndexRangeScan` 类型的算子，Probe 端是 `TableRowIDScan` 类型的算子。
- **IndexMerge**：和 `IndexLookupReader` 类似，可以看做是它的扩展，可以同时读取多个索引的数据，有多个 Build 端，一个 Probe 端。执行过程也很类似，先汇总所有 Build 端 TiKV 扫描上来的 RowID，再去 Probe 端上根据这些 RowID 精确地读取 TiKV 上的数据。Build 端是 `IndexFullScan` 或 `IndexRangeScan` 类型的算子，Probe 端是 `TableRowIDScan` 类型的算子。

#### 算子的执行顺序

算子的结构是树状的，但在查询执行过程中，并不严格要求子节点任务在父节点之前完成。TiDB 支持同一查询内的并行处理，即子节点“流入”父节点。父节点、子节点和同级节点可能并行执行查询的一部分。

在以上示例中，`├─IndexRangeScan_8(Build)` 算子为 `a(a)` 索引所匹配的行查找内部 RowID。`└─TableRowIDScan_9(Probe)` 算子随后从表中检索这些行。

Build 总是先于 Probe 执行，并且 Build 总是出现在 Probe 前面。即如果一个算子有多个子节点，子节点 ID 后面有 Build 关键字的算子总是先于有 Probe 关键字的算子执行。TiDB 在展现执行计划的时候，Build 端总是第一个出现，接着才是 Probe 端。

#### 范围查询

在 `WHERE`/`HAVING`/`ON` 条件中，TiDB 优化器会分析主键或索引键的查询返回。如数字、日期类型的比较符，如大于、小于、等于以及大于等于、小于等于，字符类型的 `LIKE` 符号等。

若要使用索引，条件必须是 "Sargable" (Search ARGument ABLE) 的。例如条件 `YEAR(date_column) < 1992` 不能使用索引，但 `date_column < '1992-01-01` 就可以使用索引。

推荐使用同一类型的数据以及同一类型的[字符串和排序规则](/character-set-and-collation.md)进行比较，以避免引入额外的 `cast` 操作而导致不能利用索引。

可以在范围查询条件中使用 `AND`（求交集）和 `OR`（求并集）进行组合。对于多维组合索引，可以对多个列使用条件。例如对组合索引 `(a, b, c)`：

+ 当 `a` 为等值查询时，可以继续求 `b` 的查询范围。
+ 当 `b` 也为等值查询时，可以继续求 `c` 的查询范围。
+ 反之，如果 `a` 为非等值查询，则只能求 `a` 的范围。

### Task 简介

目前 TiDB 的计算任务分为两种不同的 task：cop task 和 root task。Cop task 是指使用 TiKV 中的 Coprocessor 执行的计算任务，root task 是指在 TiDB 中执行的计算任务。

SQL 优化的目标之一是将计算尽可能地下推到 TiKV 中执行。TiKV 中的 Coprocessor 能支持大部分 SQL 内建函数（包括聚合函数和标量函数）、SQL `LIMIT` 操作、索引扫描和表扫描。但是，所有的 Join 操作都只能作为 root task 在 TiDB 上执行。

### `operator info` 结果

`EXPLAIN` 返回结果中 `operator info` 列可显示诸如条件下推等信息。本文以上示例中，`operator info` 结果各字段解释如下：

+ `range: [1,1]` 表示查询的 `WHERE` 字句 (`a = 1`) 被下推到了 TiKV，对应的 task 为 `cop[tikv]`。
+ `keep order:false` 表示该查询的语义不需要 TiKV 按顺序返回结果。如果查询指定了排序（例如 `SELECT * FROM t WHERE a = 1 ORDER BY id`），该字段的返回结果为 `keep order:true`。
+ `stats:pseudo` 表示 `estRows` 显示的预估数可能不准确。TiDB 定期在后台更新统计信息。也可以通过执行 `ANALYZE TABLE t` 来手动更新统计信息。

`EXPLAIN` 执行后，不同算子返回不同的信息。你可以使用 Optimizer Hints 来控制优化器的行为，以此控制物理算子的选择。例如 `/*+ HASH_JOIN(t1, t2) */` 表示优化器将使用 Hash Join 算法。详细内容见 [Optimizer Hints](/optimizer-hints.md)。

## 算子相关的系统变量

TiDB 在 MySQL 的基础上，定义了一些专用的系统变量和语法用来优化性能。其中一些系统变量和具体的算子相关，比如算子的并发度，算子的内存使用上限，是否允许使用分区表等。这些都可以通过系统变量进行控制，从而影响各个算子执行的效率。

如果读者想要详细了解所有的系统变量及其使用规则，可以参见[系统变量和语法](/system-variables.md)。

## 另请参阅

* [`EXPLAIN`](/sql-statements/sql-statement-explain.md)
* [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md)
* [`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md)
* [`TRACE`](/sql-statements/sql-statement-trace.md)
* [`TiDB in Action`](https://book.tidb.io/session3/chapter1/sql-execution-plan.html)
* [系统变量](/system-variables.md)
