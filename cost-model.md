---
title: Cost Model
summary: Learn how the cost model used by TiDB works during physical optimization.
---

# Cost Model

TiDB uses a cost model to choose an index and operator during [physical optimization](/sql-physical-optimization.md). The process is illustrated in the following diagram:

![CostModel](/media/cost-model.png)

TiDB calculates the access cost of each index and the execution cost of each physical operator in plans (such as HashJoin and IndexJoin) and chooses the minimum cost plan.

The following is a simplified example to explain how the cost model works. Suppose that there is a table `t`:

```sql
mysql> SHOW CREATE TABLE t;
+-------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Table | Create Table                                                                                                                                                                                        |
+-------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| t     | CREATE TABLE `t` (
  `a` int(11) DEFAULT NULL,
  `b` int(11) DEFAULT NULL,
  `c` int(11) DEFAULT NULL,
  KEY `b` (`b`),
  KEY `c` (`c`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin |
+-------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

When executing the `SELECT * FROM t WHERE b < 100 and c < 100` statement, suppose that TiDB estimates 20 rows meet the `b < 100` condition and 500 rows meet `c < 100`, and the length of `INT` type indexes is 8. Then TiDB calculates the cost for two indexes:

+ The cost of index `b` = row count of `b < 100` \* length of index `b` = 20 * 8 = 160
+ The cost of index `c` = row count of `c < 100` \* length of index `c` = 500 * 8 = 4000

Because the cost of index `b` is lower, TiDB chooses `b` as the index.

The preceding example is simplified and only used to explain the basic principle. In real SQL executions, the TiDB cost model is more complex.

## Cost Model Version 2

TiDB v6.2.0 introduces Cost Model Version 2, a new cost model.

Cost Model Version 2 provides a more accurate regression calibration of the cost formula, adjusts some of the cost formulas, and is more accurate than the previous version of the cost formula.

To switch the version of cost model, you can set the [`tidb_cost_model_version`](/system-variables.md#tidb_cost_model_version-new-in-v620) variable.

> **Note:**
>
> Switching the version of the cost model might cause changes to query plans.
