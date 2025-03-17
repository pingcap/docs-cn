---
title: 索引推荐 (Index Advisor)
summary: 了解如何使用 TiDB 索引推荐 (Index Advisor) 功能优化查询性能。
---

# 索引推荐 (Index Advisor)

从 v8.5.0 开始，TiDB 引入索引推荐 (Index Advisor) 功能，通过推荐能够提高查询性能的索引，帮助优化工作负载。你可以使用 `RECOMMEND INDEX` SQL 语句为单个查询或整个工作负载生成索引建议。为了避免实际创建索引时消耗大量资源，TiDB 支持[虚拟索引 (Hypothetical indexes)](#虚拟索引-hypothetical-indexes)，让被评估的索引仅存在于逻辑层面，而不会被实际创建。

索引推荐功能通过分析查询语句，从 `WHERE`、`GROUP BY` 和 `ORDER BY` 等子句中识别可索引的列。然后，它会生成索引候选项 (index candidates) 并使用虚拟索引估算其性能收益。TiDB 采用遗传搜索算法从单列索引开始，逐步迭代探索多列索引组合，以选择最优索引集合。在选择的过程中，TiDB 会利用假设分析法 (What-If analysis) 评估这些潜在索引对优化器计划成本的影响。当某些索引能够降低总体查询成本时，索引推荐功能就会推荐这些索引。

除了[推荐新索引](#使用-recommend-index-语句推荐索引)，还可以通过部分系统表的信息[删除未使用的索引](#删除未使用的索引)，以确保高效的索引管理。

## 使用 `RECOMMEND INDEX` 语句推荐索引

TiDB 提供 `RECOMMEND INDEX` SQL 语句用于索引推荐任务。使用 `RUN` 子命令，可以分析历史工作负载并将推荐结果保存到系统表中。使用 `FOR` 选项，可以为特定 SQL 语句生成索引建议，即使该语句未执行过。你还可以使用[其他选项](#recommend-index-选项)进行高级控制。语法如下：

```sql
RECOMMEND INDEX RUN [ FOR <SQL> ] [<Options>]
```

### 为单个查询推荐索引

以下示例展示如何为表 `t` 上的查询生成索引推荐，该表包含 5,000 行数据。为简洁起见，以下示例省略了 `INSERT` 语句。

```sql
CREATE TABLE t (a INT, b INT, c INT);
RECOMMEND INDEX RUN for "SELECT a, b FROM t WHERE a = 1 AND b = 1"\G
*************************** 1. row ***************************
              database: test
                 table: t
            index_name: idx_a_b
         index_columns: a,b
        est_index_size: 0
                reason: Column [a b] appear in Equal or Range Predicate clause(s) in query: select `a` , `b` from `test` . `t` where `a` = ? and `b` = ?
    top_impacted_query: [{"Query":"SELECT `a`,`b` FROM `test`.`t` WHERE `a` = 1 AND `b` = 1","Improvement":0.999994}]
create_index_statement: CREATE INDEX idx_a_b ON t(a,b);
```

索引推荐功能分别评估 `a` 和 `b` 上的单列索引，并最终将它们合并为一个组合索引 `(a, b)` 推荐出来，以实现最佳性能。

以下 `EXPLAIN` 结果比较了无索引和使用推荐的两列索引的查询执行计划。索引推荐功能会内部评估这两种方案，并选择其中执行计划成本最低的方案。索引推荐功能还会考虑 `a` 和 `b` 上的单列索引，但对于该示例，这些单列索引的性能不如组合的两列索引（为简洁起见，以下示例省略了这些执行计划）。

```sql
EXPLAIN FORMAT='VERBOSE' SELECT a, b FROM t WHERE a=1 AND b=1;

+-------------------------+---------+------------+-----------+---------------+----------------------------------+
| id                      | estRows | estCost    | task      | access object | operator info                    |
+-------------------------+---------+------------+-----------+---------------+----------------------------------+
| TableReader_7           | 0.01    | 196066.71  | root      |               | data:Selection_6                 |
| └─Selection_6           | 0.01    | 2941000.00 | cop[tikv] |               | eq(test.t.a, 1), eq(test.t.b, 1) |
|   └─TableFullScan_5     | 5000.00 | 2442000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo   |
+-------------------------+---------+------------+-----------+---------------+----------------------------------+

EXPLAIN FORMAT='VERBOSE' SELECT /*+ HYPO_INDEX(t, idx_ab, a, b) */ a, b FROM t WHERE a=1 AND b=1;
+------------------------+---------+---------+-----------+-----------------------------+-------------------------------------------------+
| id                     | estRows | estCost | task      | access object               | operator info                                   |
+------------------------+---------+---------+-----------+-----------------------------+-------------------------------------------------+
| IndexReader_6          | 0.05    | 1.10    | root      |                             | index:IndexRangeScan_5                          |
| └─IndexRangeScan_5     | 0.05    | 10.18   | cop[tikv] | table:t, index:idx_ab(a, b) | range:[1 1,1 1], keep order:false, stats:pseudo |
+------------------------+---------+---------+-----------+-----------------------------+-------------------------------------------------+
```

### 为工作负载推荐索引

以下示例展示如何为整个工作负载生成索引推荐。假设表 `t1` 和 `t2` 各包含 5,000 行数据：

```sql
CREATE TABLE t1 (a INT, b INT, c INT, d INT);
CREATE TABLE t2 (a INT, b INT, c INT, d INT);

-- 在此工作负载中运行一些查询
SELECT a, b FROM t1 WHERE a=1 AND b<=5;
SELECT d FROM t1 ORDER BY d LIMIT 10;
SELECT * FROM t1, t2 WHERE t1.a=1 AND t1.d=t2.d;

RECOMMEND INDEX RUN;
+----------+-------+------------+---------------+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------------------------------+
| database | table | index_name | index_columns | est_index_size | reason                                                                                                                                                                | top_impacted_query                                                                                                                                                                                                              | create_index_statement           |
+----------+-------+------------+---------------+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------------------------------+
| test     | t1    | idx_a_b    | a,b           | 19872      | Column [a b] appear in Equal or Range Predicate clause(s) in query: select `a` , `b` from `test` . `t1` where `a` = ? and `b` <= ?                                    | [{"Query":"SELECT `a`,`b` FROM `test`.`t1` WHERE `a` = 1 AND `b` \u003c= 5","Improvement":0.998214},{"Query":"SELECT * FROM (`test`.`t1`) JOIN `test`.`t2` WHERE `t1`.`a` = 1 AND `t1`.`d` = `t2`.`d`","Improvement":0.336837}] | CREATE INDEX idx_a_b ON t1(a,b); |
| test     | t1    | idx_d      | d             | 9936       | Column [d] appear in Equal or Range Predicate clause(s) in query: select `d` from `test` . `t1` order by `d` limit ?                                                  | [{"Query":"SELECT `d` FROM `test`.`t1` ORDER BY `d` LIMIT 10","Improvement":0.999433}]                                                                                                                                          | CREATE INDEX idx_d ON t1(d);     |
| test     | t2    | idx_d      | d             | 9936       | Column [d] appear in Equal or Range Predicate clause(s) in query: select * from ( `test` . `t1` ) join `test` . `t2` where `t1` . `a` = ? and `t1` . `d` = `t2` . `d` | [{"Query":"SELECT * FROM (`test`.`t1`) JOIN `test`.`t2` WHERE `t1`.`a` = 1 AND `t1`.`d` = `t2`.`d`","Improvement":0.638567}]                                                                                                    | CREATE INDEX idx_d ON t2(d);     |
+----------+-------+------------+---------------+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------------------------------+
```

在这个示例中，索引推荐功能识别出了适用于整个工作负载的最佳索引，而不仅仅是针对单个查询。工作负载数据来源于 TiDB 系统表 `INFORMATION_SCHEMA.STATEMENTS_SUMMARY`。

工作负载中可能包含数万到数十万条查询，为了提高推荐索引的效率，此功能会优先考虑为执行频率最高的查询进行索引推荐，因为这些查询对整体工作负载性能的影响更大。默认情况下，索引推荐功能会选择执行频率最高的前 1,000 条查询，你可以使用 [`max_num_query`](#recommend-index-选项) 参数调整此值。

`RECOMMEND INDEX` 语句的结果存储在 `mysql.index_advisor_results` 表中。你可以查询此表以查看推荐的索引。以下示例为执行前两个 `RECOMMEND INDEX` 语句后此系统表的内容：

```sql
SELECT * FROM mysql.index_advisor_results;
+----+---------------------+---------------------+-------------+------------+------------+---------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------------------------+-------+
| id | created_at          | updated_at          | schema_name | table_name | index_name | index_columns | index_details                                                                                                                                                                                       | top_impacted_queries                                                                                                                                                                                                              | workload_impact                   | extra |
+----+---------------------+---------------------+-------------+------------+------------+---------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------------------------+-------+
|  1 | 2024-12-10 11:44:45 | 2024-12-10 11:44:45 | test        | t1         | idx_a_b    | a,b           | {"IndexSize": 0, "Reason": "Column [a b] appear in Equal or Range Predicate clause(s) in query: select `a` , `b` from `test` . `t1` where `a` = ? and `b` <= ?"}                                    | [{"Improvement": 0.998214, "Query": "SELECT `a`,`b` FROM `test`.`t1` WHERE `a` = 1 AND `b` <= 5"}, {"Improvement": 0.337273, "Query": "SELECT * FROM (`test`.`t1`) JOIN `test`.`t2` WHERE `t1`.`a` = 1 AND `t1`.`d` = `t2`.`d`"}] | {"WorkloadImprovement": 0.395235} | NULL  |
|  2 | 2024-12-10 11:44:45 | 2024-12-10 11:44:45 | test        | t1         | idx_d      | d             | {"IndexSize": 0, "Reason": "Column [d] appear in Equal or Range Predicate clause(s) in query: select `d` from `test` . `t1` order by `d` limit ?"}                                                  | [{"Improvement": 0.999715, "Query": "SELECT `d` FROM `test`.`t1` ORDER BY `d` LIMIT 10"}]                                                                                                                                         | {"WorkloadImprovement": 0.225116} | NULL  |
|  3 | 2024-12-10 11:44:45 | 2024-12-10 11:44:45 | test        | t2         | idx_d      | d             | {"IndexSize": 0, "Reason": "Column [d] appear in Equal or Range Predicate clause(s) in query: select * from ( `test` . `t1` ) join `test` . `t2` where `t1` . `a` = ? and `t1` . `d` = `t2` . `d`"} | [{"Improvement": 0.639393, "Query": "SELECT * FROM (`test`.`t1`) JOIN `test`.`t2` WHERE `t1`.`a` = 1 AND `t1`.`d` = `t2`.`d`"}]                                                                                                   | {"WorkloadImprovement": 0.365871} | NULL  |
+----+---------------------+---------------------+-------------+------------+------------+---------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------------------------+-------+
```

### `RECOMMEND INDEX` 选项

你可以查看 `RECOMMEND INDEX` 语句的选项，并根据你的工作负载需求配置该选项以调整索引推荐的结果，如下所示：

```sql
RECOMMEND INDEX SET <option> = <value>;
RECOMMEND INDEX SHOW OPTION;
```

以下是可用的选项：

- `timeout`：指定运行 `RECOMMEND INDEX` 语句的最长允许时间。
- `max_num_index`：指定 `RECOMMEND INDEX` 最多推荐的索引数量。
- `max_index_columns`：指定结果中多列索引允许的最大列数。
- `max_num_query`：指定为工作负载推荐索引时，每次最多能够为多少条查询提供推荐。

要查看当前的选项设置，执行 `RECOMMEND INDEX SHOW OPTION` 语句：

```sql
RECOMMEND INDEX SHOW OPTION;
+-------------------+-------+---------------------------------------------------------+
| option            | value | description                                             |
+-------------------+-------+---------------------------------------------------------+
| max_num_index     | 5     | The maximum number of indexes to recommend.             |
| max_index_columns | 3     | The maximum number of columns in an index.              |
| max_num_query     | 1000  | The maximum number of queries to recommend indexes.     |
| timeout           | 30s   | The timeout of index advisor.                           |
+-------------------+-------+---------------------------------------------------------+
4 rows in set (0.00 sec)
```

要修改选项的值，可以使用 `RECOMMEND INDEX SET` 语句。例如，修改 `timeout` 选项：

```sql
RECOMMEND INDEX SET timeout='20s';
Query OK, 1 row affected (0.00 sec)
```

### 限制

索引推荐功能目前有以下限制：

- 不支持[预处理语句](/develop/dev-guide-prepared-statement.md)。`RECOMMEND INDEX RUN` 语句无法为通过 `Prepare` 和 `Execute` 协议执行的查询推荐索引。
- 不提供删除索引的建议。
- 尚未提供图形化用户界面 (UI)。

## 删除未使用的索引

对于 TiDB v8.0.0 及以上版本，你可以使用 [`schema_unused_indexes`](/sys-schema/sys-schema-unused-indexes.md) 和 [`INFORMATION_SCHEMA.CLUSTER_TIDB_INDEX_USAGE`](/information-schema/information-schema-tidb-index-usage.md) 识别工作负载中未使用的索引。删除这些索引可以节省存储空间并减少开销。在生产环境中，强烈建议先将未使用的目标索引设为不可见，并观察一个完整业务周期的影响，然后再永久删除它们。

### 使用 `sys.schema_unused_indexes`

[`sys.schema_unused_indexes`](/sys-schema/sys-schema-unused-indexes.md) 视图显示自所有 TiDB 实例上次启动以来未被使用的索引。该视图基于包含数据库、表和列信息的系统表，提供每个索引的完整信息，包括数据库、表和索引名称。你可以查询此视图以决定哪些索引可以设为不可见或直接删除。

> **警告：**
>
> 由于 `sys.schema_unused_indexes` 视图显示自所有 TiDB 实例上次启动以来未被使用的索引，请确保 TiDB 实例已运行足够长的时间。否则，如果某些工作负载尚未运行，视图可能会将这些负载对应的索引也错误地显示出来。使用以下 SQL 查询所有 TiDB 实例的运行时间：
>
> ```sql
> SELECT START_TIME,UPTIME FROM INFORMATION_SCHEMA.CLUSTER_INFO WHERE TYPE='tidb';
> ```

### 使用 `INFORMATION_SCHEMA.CLUSTER_TIDB_INDEX_USAGE`

[`INFORMATION_SCHEMA.CLUSTER_TIDB_INDEX_USAGE`](/information-schema/information-schema-tidb-index-usage.md) 表提供了索引的行访问比例分布、最后访问时间和访问行数等指标。以下查询可用于识别未使用过的或低效的索引：

```sql
-- 查找在过去 30 天内未被访问的索引
SELECT table_schema, table_name, index_name, last_access_time
FROM information_schema.cluster_tidb_index_usage
WHERE last_access_time IS NULL
  OR last_access_time < NOW() - INTERVAL 30 DAY;

-- 查找始终扫描超过 50% 总记录的索引
SELECT table_schema, table_name, index_name,
       query_total, rows_access_total,
       percentage_access_0 as full_table_scans
FROM information_schema.cluster_tidb_index_usage
WHERE last_access_time IS NOT NULL AND percentage_access_0 + percentage_access_0_1 + percentage_access_1_10 + percentage_access_10_20 + percentage_access_20_50 = 0;
```

> **注意：**
>
> `INFORMATION_SCHEMA.CLUSTER_TIDB_INDEX_USAGE` 中的数据最多可能会有五分钟的延迟，并且每当 TiDB 节点重启时，这些数据会被重置。此外，只有在表具有有效统计信息时，才会记录该表的索引使用情况。

## 虚拟索引 (Hypothetical indexes)

虚拟索引 (Hypothetical indexes, Hypo indexes) 是通过 SQL 注释而非 `CREATE INDEX` 语句创建的，类似于 [Optimizer Hints](/optimizer-hints.md)。使用虚拟索引，你可以在不实际创建索引的情况下轻量级地测试索引对查询性能的效果。

例如，`/*+ HYPO_INDEX(t, idx_ab, a, b) */` 注释指示查询规划器在表 `t` 上为列 `a` 和 `b` 创建一个名为 `idx_ab` 的虚拟索引。优化器会生成该索引的元数据，但不会实际创建索引。在查询优化过程中，如果适用，优化器会考虑该虚拟索引，而不会产生实际创建索引的开销。

`RECOMMEND INDEX` 使用虚拟索引进行假设分析，以评估不同索引的潜在收益。你也可以直接使用虚拟索引来尝试索引设计，然后再决定是否创建它们。

以下示例展示了使用虚拟索引的查询：

```sql
CREATE TABLE t(a INT, b INT, c INT);
Query OK, 0 rows affected (0.02 sec)

EXPLAIN FORMAT='verbose' SELECT a, b FROM t WHERE a=1 AND b=1;
+-------------------------+----------+------------+-----------+---------------+----------------------------------+
| id                      | estRows  | estCost    | task      | access object | operator info                    |
+-------------------------+----------+------------+-----------+---------------+----------------------------------+
| TableReader_7           | 0.01     | 392133.42  | root      |               | data:Selection_6                 |
| └─Selection_6           | 0.01     | 5882000.00 | cop[tikv] |               | eq(test.t.a, 1), eq(test.t.b, 1) |
|   └─TableFullScan_5     | 10000.00 | 4884000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo   |
+-------------------------+----------+------------+-----------+---------------+----------------------------------+

EXPLAIN FORMAT='verbose' SELECT /*+ HYPO_INDEX(t, idx_ab, a, b) */ a, b FROM t WHERE a=1 AND b=1;
+------------------------+---------+---------+-----------+-----------------------------+-------------------------------------------------+
| id                     | estRows | estCost | task      | access object               | operator info                                   |
+------------------------+---------+---------+-----------+-----------------------------+-------------------------------------------------+
| IndexReader_6          | 0.10    | 2.20    | root      |                             | index:IndexRangeScan_5                          |
| └─IndexRangeScan_5     | 0.10    | 20.35   | cop[tikv] | table:t, index:idx_ab(a, b) | range:[1 1,1 1], keep order:false, stats:pseudo |
+------------------------+---------+---------+-----------+-----------------------------+-------------------------------------------------+
```

在这个示例中，`HYPO_INDEX` 注释指定了一个虚拟索引。通过使用该虚拟索引，优化器将全表扫描 (`TableFullScan`) 替换为索引范围扫描 (`IndexRangeScan`)，从而将查询的估计成本从 `392133.42` 降低到 `2.20`。

TiDB 可以根据工作负载中的查询自动生成对你的工作负载可能有益的索引候选项 (index candidates)。它使用虚拟索引来评估这些索引的潜在收益，并推荐最有效的索引方案。
