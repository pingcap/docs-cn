---
title: SQL Physical Optimization
summary: Physical optimization is a cost-based process that creates a physical execution plan for the logical execution plan. The optimizer selects the best physical implementation for each operator based on data statistics, time complexity, and resource consumption. This includes index selection, statistics collection, using the right index, distinct keyword optimization, and cost model for optimal execution plan selection.
---

# SQL Physical Optimization

Physical optimization is cost-based optimization, which makes a physical execution plan for the logical execution plan generated in the previous stage. In this stage, the optimizer selects a specific physical implementation for each operator in the logical execution plan. Different physical implementations of logical operators have different time complexity, resource consumption and physical properties. In this process, the optimizer determines the cost of different physical implementations based on the statistics of the data, and selects the physical execution plan with the smallest overall cost.

[Understand the Query Execution Plan](/explain-overview.md) has introduced some physical operators. This chapter focuses on the following aspects:

- In [Index Selection](/choose-index.md), you will learn how to select the optimal index to access tables when TiDB has multiple indexes on a table.
- In [Introduction to Statistics](/statistics.md), you will learn what statistics TiDB collects to obtain the data distribution of a table.
- [Wrong Index Solution](/wrong-index-solution.md) introduces how to use the right index when you find the index is selected wrongly.
- [Distinct Optimization](/agg-distinct-optimization.md) introduces an optimization related to the `DISTINCT` keyword during physical optimization. In this section, you will learn its advantages and disadvantages and how to use it.
- [Cost Model](/cost-model.md) introduces how to choose a optimal execution plan based on the cost model during physical optimization.
