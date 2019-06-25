---
title: SQL 语句诊断
category: reference
---

# SQL 语句诊断

为了方便排查问题，TiDB 提供了一些 SQL 语句和系统表以查询一些有用的信息。

`INFORMATION\_SCHEMA` 中提供了如下几个系统表，用于查询集群状态，诊断常见的集群问题。

- [`TABLES`](/reference/system-databases/information-schema.md#tables-表)
- [`TIDB_INDEXES`](/reference/system-databases/information-schema.md#tidb-indexes-表)
- [`ANALYZE_STATUS`](/reference/system-databases/information-schema.md#analyze-status-表)
- [`TIDB_HOT_REGIONS`](/reference/system-databases/information-schema.md#tidb-hot-regions-表)
- [`TIKV_STORE_STATUS`](/reference/system-databases/information-schema.md#tikv-store-status-表)
- [`TIKV_REGION_STATUS`](/reference/system-databases/information-schema.md#tikv-region-status-表)
- [`TIKV_REGION_PEERS`](/reference/system-databases/information-schema.md#tikv-region-peers-表)

除此之外，执行下列语句也可获得对排查问题或查询集群状态有用的信息：

- `ADMIN SHOW DDL` 可以获得是 `DDL owner` 角色的 TiDB 的 ID 及 `IP:PORT` 等具体信息。
- `SHOW ANALYZE STATUS` 和 [`ANALYZE_STATUS`](/reference/system-databases/information-schema.md#analyze-status-表) 表的功能相同。
- 特殊的 `EXPLAIN` 语句
    - `EXPLAIN ANALYZE` 语句可以获得一个 SQL 语句执行中的一些具体信息。
    - `EXPLAIN FOR CONNECTION` 可以获得一个连接中最后执行的查询的执行计划。可以配合 `SHOW PROCESSLIST` 使用。
    - 关于 `EXPLAIN` 相关的更具体的信息，参考文档[理解 TiDB 执行计划](/reference/performance/understanding-the-query-execution-plan.md)。
