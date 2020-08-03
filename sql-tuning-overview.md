---
title: SQL Tuning Overview
---

# SQL Tuning Overview

The previous "Troubleshoot" chapter describes some ways to locate some queries that affect the cluster, and that if some queries' execution time does not meet expectations, you need to analyze the execution result to find the cause. In this chapter, the following sections introduce how to tune a specific query:

- In the first section, [Understand the Query Execution Plan](/query-execution-plan.md) introduces how to use the `EXPLAIN` and `EXPLAIN ANALYZE` statements to understand how TiDB executes a query.
- In the second section, [SQL Optimization Process](/sql-optimization-concepts.md) introduces the optimizations used internally by TiDB, which involves some equivalent SQL conversions and the selection of physical plans. This section helps you understand how TiDB generates the final execution plan.
- In the third section, [Control Execution Plan](/control-execution-plan.md) introduces the ways to control the generation of the execution plan, which improves the execution speed of the query and reduces its impact on the overall performance of the cluster or online business.
