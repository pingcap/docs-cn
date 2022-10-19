---
title: TiFlash 计算结果物化
summary: 介绍如何在同一个事务处理中物化保存 TiFlash 的计算结果。本功能为实验功能。
---

# TiFlash 计算结果物化

本文介绍如何在同一个事务处理中实现 TiFlash 计算结果的物化保存。

## 支持下推的算子

TiFlash 查询的结果可以通过 `INSERT INTO SELECT` 语句保存在一个 TiDB 表中：

```sql
INSERT [LOW_PRIORITY | HIGH_PRIORITY] [IGNORE]
    [INTO] tbl_name
    [PARTITION (partition_name [, partition_name] ...)]
    [(col_name [, col_name] ...)]
    SELECT ...
    [ON DUPLICATE KEY UPDATE assignment_list]value:
    {expr | DEFAULT}

assignment:
    col_name = valueassignment_list:
    assignment [, assignment] ...
```


## 使用场景和限制

### Execution of query
* SELECT sub-statement will be executed by TiFlash
  1. Optimizer automatically chooses TiFlash
  2. Users can use "tidb_enforce_mpp = TRUE" (existing variable) to force the query making use of TiFlash (when necesary, say, the optimizer cannot choose the right plan)
* The results of SELECT will be handled by a single TiDB server (the most spared one if possible)
* The whole statement should hold ACID properties as other TiDB txn
System Limitation for the size of records returned by  SELECT
* The results size of TiFlash selection has a limitation:  Txn-max = 1 GB.
Conceptually, Txn size should be inside the O(100 MB) scope (roughly less than 1 million rows).
* If the SELECT returns more data than Txn-max, the whole txn will be abandoned
  * Give the error message: "The query produced a too large intermediate result and thus failed"
* Concurrency Constraints (maximum  supported concurrent queries: C_max )
  * C_max  is not an enforced value, but a recommended/reference value to users
  * When txn size = Txn-Max, C_max = 10
  * When txn size = 100 MB, C_max = 30
### User Scenarios / Story
1. Much more efficient BI solution
Many BI applications need to repeatedly run the same query as end users may refresh the dashboard at any time. However, this is not an efficient way because the results are no different in a short time. This new feature allows persistent results for BI and avoids most meaningless queries and thus saves system resources and can also boot the BI performance;
2. Serve downstream online services
TiFlash cannot serve online services because the concurrency is not that high (typically 30 ~ 50 QPS). By this feature, application developers can easily persistent analytical results inside TiDB and update when necessary, so that the application can use TiDB to serve the online services that access the results table in a very high concurrency. It became a closure inside TiDB without using 3rd party systems.
