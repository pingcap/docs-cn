---
title: SQL 语句诊断工具箱
category: reference
aliases: ['/docs-cn/sql/diagnostic-kit']
---

# SQL 语句诊断工具箱

为了方便排查问题，TiDB 提供了一些 SQL 语句和系统表以查询一些有用的信息。

`INFORMATION\_SCHEMA` 中提供了如下几个系统表，用于查询集群状态，诊断常见的集群问题。

- [`TABLES`](/dev/reference/system-databases/information-schema.md#TABLES-表)
- [`TIDB\_INDEXES`](/dev/reference/system-databases/information-schema.md#TIDB\_INDEXES-表)
- [`ANALYZE\_STATUS`](/dev/reference/system-databases/information-schema.md#ANALYZE\_STATUS-表)
- [`TIDB\_HOT\_REGIONS`](/dev/reference/system-databases/information-schema.md#TIDB\_HOT\_REGIONS-表)
- [`TIKV\_STORE\_STATUS`](/dev/reference/system-databases/information-schema.md#TIKV\_STORE\_STATUS-表)
- [`TIKV\_REGION\_STATUS`](/dev/reference/system-databases/information-schema.md#TIKV\_REGION\_STATUS-表)
- [`TIKV\_REGION\_PEERS`](/dev/reference/system-databases/information-schema.md#TIKV\_REGION\_PEERS-表)

除此之外，执行下列语句也可获得对排查问题或查询集群状态有用的信息：

- `ADMIN SHOW DDL` 可以获得是 `DDL owner` 角色的 TiDB 的 ID 及 `IP:PORT` 等具体信息。
- `SHOW ANALYZE STATUS` 和 [`ANALYZE_STATUS`](/dev/reference/system-databases/information-schema.md#ANALYZE\_STATUS-表) 表的功能相同。
- 特殊的 `EXPLAIN` 语句
    - `EXPLAIN ANALYZE` 语句可以获得一个 SQL 语句执行中的一些具体信息。
    - `EXPLAIN FOR CONNECTION` 可以获得一个连接中最后执行的查询的执行计划。可以配合 `SHOW PROCESSLIST` 使用。
    - 关于 `EXPLAIN` 相关的更具体的信息，参考文档[理解 TiDB 执行计划](/dev/reference/performance/understanding-the-query-execution-plan.md)。

