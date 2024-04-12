---
title: TiDB 中的各种超时
summary: 简单介绍 TiDB 中的各种超时，为排查错误提供依据。
---

# TiDB 中的各种超时

本章将介绍 TiDB 中的各种超时，为排查错误提供依据。

## 事务超时

垃圾回收 (GC) 不会影响到正在执行的事务。但悲观事务的运行仍有上限，有基于事务超时的限制（TiDB 配置文件 [performance] 类别下的 `max-txn-ttl` 修改，默认为 60 分钟）和基于事务使用内存的限制。

形如 `INSERT INTO t10 SELECT * FROM t1` 的 SQL 语句，不会受到 GC 的影响，但超过了 `max-txn-ttl` 的时间后，会由于超时而回滚。

## SQL 执行时间超时

TiDB 还提供了一个系统变量来限制单条 SQL 语句的执行时间，仅对“只读”语句生效：`max_execution_time`，它的默认值为 0，表示无限制。`max_execution_time` 的单位为 ms，但实际精度在 100ms 级别，而非更准确的毫秒级别。

## JDBC 查询超时

MySQL jdbc 的查询超时设置 `setQueryTimeout()` 对 TiDB 不起作用。这是因为现实客户端感知超时时，向数据库发送一个 KILL 命令。但是由于 tidb-server 是负载均衡的，为防止在错误的 tidb-server 上终止连接，tidb-server 不会执行这个 KILL。这时就要用 `MAX_EXECUTION_TIME` 实现查询超时的效果。

TiDB 提供了三个与 MySQL 兼容的超时控制参数：

- **wait_timeout**，控制与 Java 应用连接的非交互式空闲超时时间。在 TiDB v5.4 及以上版本中，默认值为 `28800` 秒，即空闲超时为 8 小时。在 v5.4 之前，默认值为 `0`，即没有时间限制。
- **interactive_timeout**，控制与 Java 应用连接的交互式空闲超时时间，默认值为 8 小时。
- **max_execution_time**，控制连接中 SQL 执行的超时时间，仅对“只读”语句生效，默认值是 0，即允许连接无限忙碌（一个 SQL 语句执行无限的长的时间）。

但在实际生产环境中，空闲连接和一直无限执行的 SQL 对数据库和应用都有不好的影响。你可以通过在应用的连接字符串中配置这两个 session 级的变量来避免空闲连接和执行时间过长的 SQL 语句。例如，设置 `sessionVariables=wait_timeout=3600（1 小时）`和 `sessionVariables=max_execution_time=300000（5 分钟）`。
