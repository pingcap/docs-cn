---
title: EXPLAIN Overview
summary: Learn about the execution plan information returned by the `EXPLAIN` statement in TiDB.
<<<<<<< HEAD:query-execution-plan.md
aliases: ['/docs/stable/query-execution-plan/','/docs/v4.0/query-execution-plan/','/docs/stable/reference/performance/understanding-the-query-execution-plan/','/docs/stable/index-merge/','/docs/v4.0/index-merge/','/docs/stable/reference/performance/index-merge/','/tidb/stable/index-merge']
=======
aliases: ['/docs/dev/query-execution-plan/','/docs/dev/reference/performance/understanding-the-query-execution-plan/','/docs/dev/index-merge/','/docs/dev/reference/performance/index-merge/','/tidb/dev/index-merge','/tidb/dev/query-execution-plan']
>>>>>>> ebbdd50b... performance tuning: change SQL tuning TOC (#3858):explain-overview.md
aliases: ['/docs/stable/query-execution-plan/','/docs/v4.0/query-execution-plan/','/docs/stable/reference/performance/understanding-the-query-execution-plan/','/docs/stable/index-merge/','/docs/v4.0/index-merge/','/docs/stable/reference/performance/index-merge/','/tidb/stable/index-merge','/tidb/stable/query-execution-plan']
---

# `EXPLAIN` Overview

Based on the latest statistics of your tables, the TiDB optimizer chooses the most efficient query execution plan, which consists of a series of operators. This document details the execution plan in TiDB.

## Introduction

You can use the `EXPLAIN` command in TiDB to view the execution plan. The result of the `EXPLAIN` statement provides information about how TiDB executes SQL queries:

- `EXPLAIN` works together with statements such as `SELECT` and `DELETE`.
- When you execute the `EXPLAIN` statement, TiDB returns the final optimized physical execution plan. In other words, `EXPLAIN` displays the complete information about how TiDB executes the SQL statement, such as in which order, how tables are joined, and what the expression tree looks like.
- For more information about each column of `EXPLAIN`, see [`EXPLAIN` Output Format](/sql-statements/sql-statement-explain.md).

The results of `EXPLAIN` shed light on how to index the data tables so that the execution plan can use the index to speed up the execution of SQL statements. You can also use `EXPLAIN` to check if the optimizer chooses the optimal order to join tables.

---
<<<<<<< HEAD:query-execution-plan.md
aliases: ['/docs/stable/query-execution-plan/','/docs/v4.0/query-execution-plan/','/docs/stable/reference/performance/understanding-the-query-execution-plan/','/docs/stable/index-merge/','/docs/v4.0/index-merge/','/docs/stable/reference/performance/index-merge/','/tidb/stable/index-merge']
=======
aliases: ['/docs/dev/query-execution-plan/','/docs/dev/reference/performance/understanding-the-query-execution-plan/','/docs/dev/index-merge/','/docs/dev/reference/performance/index-merge/','/tidb/dev/index-merge','/tidb/dev/query-execution-plan']
>>>>>>> ebbdd50b... performance tuning: change SQL tuning TOC (#3858):explain-overview.md
aliases: ['/docs/stable/query-execution-plan/','/docs/v4.0/query-execution-plan/','/docs/stable/reference/performance/understanding-the-query-execution-plan/','/docs/stable/index-merge/','/docs/v4.0/index-merge/','/docs/stable/reference/performance/index-merge/','/tidb/stable/index-merge','/tidb/stable/query-execution-plan']
---

## `EXPLAIN` Overview

Based on the latest statistics of your tables, the TiDB optimizer chooses the most efficient query execution plan, which consists of a series of operators. This document details the execution plan in TiDB.

## Introduction

You can use the `EXPLAIN` command in TiDB to view the execution plan. The result of the `EXPLAIN` statement provides information about how TiDB executes SQL queries:

- `EXPLAIN` works together with statements such as `SELECT` and `DELETE`.
- When you execute the `EXPLAIN` statement, TiDB returns the final optimized physical execution plan. In other words, `EXPLAIN` displays the complete information about how TiDB executes the SQL statement, such as in which order, how tables are joined, and what the expression tree looks like.
- For more information about each column of `EXPLAIN`, see [`EXPLAIN` Output Format](/sql-statements/sql-statement-explain.md).

The results of `EXPLAIN` shed light on how to index the data tables so that the execution plan can use the index to speed up the execution of SQL statements. You can also use `EXPLAIN` to check if the optimizer chooses the optimal order to join tables.