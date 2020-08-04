---
title: 使用 SQL 语句检查 TiDB 集群状态
aliases: ['/docs-cn/v3.0/check-cluster-status-using-sql-statements/','/docs-cn/v3.0/reference/performance/check-cluster-status-using-sql-statements/']
---

# 使用 SQL 语句检查 TiDB 集群状态

为了方便排查问题，TiDB 提供了一些 SQL 语句和系统表以查询一些有用的信息。

`INFORMATION\_SCHEMA` 中提供了如下几个系统表，用于查询集群状态，诊断常见的集群问题。

- [`TABLES`](/system-tables/system-table-information-schema.md#tables-表)
- [`TIDB_INDEXES`](/system-tables/system-table-information-schema.md#tidb_indexes-表)
- [`ANALYZE_STATUS`](/system-tables/system-table-information-schema.md#analyze_status-表)
- [`TIDB_HOT_REGIONS`](/system-tables/system-table-information-schema.md#tidb_hot_regions-表)
- [`TIKV_STORE_STATUS`](/system-tables/system-table-information-schema.md#tikv_store_status-表)
- [`TIKV_REGION_STATUS`](/system-tables/system-table-information-schema.md#tikv_region_status-表)
- [`TIKV_REGION_PEERS`](/system-tables/system-table-information-schema.md#tikv_region_peers-表)

除此之外，执行下列语句也可获得对排查问题或查询集群状态有用的信息：

- `ADMIN SHOW DDL` 可以获得是 `DDL owner` 角色的 TiDB 的 ID 及 `IP:PORT` 等具体信息。
- `SHOW ANALYZE STATUS` 和 [`ANALYZE_STATUS`](/system-tables/system-table-information-schema.md#analyze_status-表) 表的功能相同。
- 特殊的 `EXPLAIN` 语句：
    - `EXPLAIN ANALYZE` 语句可以获得一个 SQL 语句执行中的一些具体信息。
    - `EXPLAIN FOR CONNECTION` 可以获得一个连接中最后执行的查询的执行计划。可以配合 `SHOW PROCESSLIST` 使用。
    - 关于 `EXPLAIN` 相关的更具体的信息，参考文档[理解 TiDB 执行计划](/query-execution-plan.md)。