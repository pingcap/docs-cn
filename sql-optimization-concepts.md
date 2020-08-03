---
title: SQL Optimization Process
summary: Learn about the logical and physical optimization of SQL in TiDB.
aliases: ['/docs/dev/sql-optimization-concepts/','/docs/dev/reference/performance/sql-optimizer-overview/']
---

# SQL Optimization Process

In TiDB, the process from inputting a query to getting the execution result according to the final execution plan is illustrated as follows:

![SQL Optimization Process](/media/sql-optimization.png)

After parsing the original query text by `parser` and some simple validity checks, TiDB first makes some logically equivalent changes to the query. For detailed changes, see [SQL Logical Optimization](/sql-logical-optimization.md).

Through these equivalent changes, this query becomes easier to handle in the logical execution plan. After the equivalent change is done, TiDB obtains a query plan structure equivalent to the original query, and then obtains a final execution plan based on the data distribution and the specific execution cost of an operator. For details, see [SQL Physical Optimization](/sql-physical-optimization.md).

At the same time, when TiDB executes the [`PREPARE`](/sql-statements/sql-statement-prepare.md) statement, you can choose to enable caching to reduce the cost of generating the execution plan in TiDB. For details, see [Execution Plan Cache](/sql-prepare-plan-cache.md).