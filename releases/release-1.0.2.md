---
title: TiDB 1.0.2 Release Notes
aliases: ['/docs/dev/releases/release-1.0.2/','/docs/dev/releases/102/']
summary: TiDB 1.0.2 was released on November 13, 2017. Updates include optimized cost estimation for index point query, support for Alter Table Add Column syntax, and improved query optimization. Placement Driver (PD) scheduling stability was enhanced, and TiKV now supports table splitting and limits key length to 4 KB. Other improvements include more accurate read traffic statistics and bug fixes for LIKE behavior and do_div_mod bug.
---

# TiDB 1.0.2 Release Notes

On November 13, 2017, TiDB 1.0.2 is released with the following updates:

## TiDB

- Optimize the cost estimation of index point query
- Support the `Alter Table Add Column (ColumnDef ColumnPosition)` syntax
- Optimize the queries whose `where` conditions are contradictory
- Optimize the `Add Index` operation to rectify the progress and reduce repetitive operations
- Optimize the `Index Look Join` operator to accelerate the query speed for small data size
- Fix the issue with prefix index judgment

## Placement Driver (PD)

- Improve the stability of scheduling under exceptional situations

## TiKV

- Support splitting table to ensure one region does not contain data from multiple tables
- Limit the length of a key to be no more than 4 KB
- More accurate read traffic statistics
- Implement deep protection on the coprocessor stack
- Fix the `LIKE` behavior and the `do_div_mod` bug
