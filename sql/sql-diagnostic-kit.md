---
title: SQL diagnostic kit
category: reference
aliases: ['/docs-cn/sql/diagnostic-kit']
---

# SQL diagnostic kit

为了方便排查问题，TiDB 中提供了一些 SQL 和系统表来方便的查询到一些有用的信息。

在 `INFORMATION\_SCHEMA` 这个系统数据库中，有如下的表可供使用。

- [TABLES](../dev/reference/system-databases/information-schema.md#TABLES-Table)
- [TIDB\_INDEXES](../dev/reference/system-databases/information-schema.md#TIDB\_INDEXES)
- [ANALYZE\_STATUS](../dev/reference/system-databases/information-schema.md#ANALYZE\_STATUS)
- [TIDB\_HOT\_REGIONS](../dev/reference/system-databases/information-schema.md#TIDB\_HOT\_REGIONS)
- [TIKV\_STORE\_STATUS](../dev/reference/system-databases/information-schema.md#TIKV\_STORE\_STATUS)
- [TIKV\_REGION\_STATUS](../dev/reference/system-databases/information-schema.md#TIKV\_REGION\_STATUS)
- [TIKV\_REGION\_PEERS](../dev/reference/system-databases/information-schema.md#TIKV\_REGION\_PEERS)

除此之外，还有一些其他的命令也可以获得对于排查问题或者查询集群状态相关的有用信息。

- `ADMIN SHOW DDL` 可以获得是 `DDL owner` 角色的 TiDB 的 ID, `IP:ADDRESS` 等具体的信息。
- `SHOW ANALYZE STATUS`， 和 [`INFORMATION_SCHEMA.ANALYZE_STATUS`](../dev/reference/system-databases/information-schema.md#ANALYZE\_STATUS) 表的功能相同.
- 特殊的 `EXPLAIN` 语句
	- `EXPLAIN ANALYZE` 这个语句可以获得一个 SQL 执行中的一些具体信息
	- `EXPLAIN FOR CONNECTION` 可以获得一个连接中最后执行的查询的执行计划。可以配合 `SHOW PROCESSLIST` 来获得一些具体的信息。
	- `EXPLAIN` 相关的更具体的信息可以在文档中[理解 TiDB 执行计划](../dev/reference/performance/understanding-the-query-execution-plan.md)查看。

