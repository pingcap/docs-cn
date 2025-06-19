---
title: 连接池和连接参数
summary: 本文介绍如何配置 TiDB 的连接池和参数。涵盖了连接池大小、探测配置和最佳吞吐量公式。还讨论了 JDBC API 的使用和 MySQL Connector/J 参数配置以优化性能。
---

# 连接池和连接参数

本文介绍在使用驱动或 ORM 框架连接 TiDB 时如何配置连接池和连接参数。

<CustomContent platform="tidb">

如果你对 Java 应用程序开发的更多技巧感兴趣，请参阅[使用 TiDB 开发 Java 应用的最佳实践](/best-practices/java-app-best-practices.md#connection-pool)。

</CustomContent>

<CustomContent platform="tidb-cloud">

如果你对 Java 应用程序开发的更多技巧感兴趣，请参阅[使用 TiDB 开发 Java 应用的最佳实践](https://docs.pingcap.com/tidb/stable/java-app-best-practices)。

</CustomContent>

## 连接池

建立 TiDB (MySQL) 连接的成本相对较高（至少对于 OLTP 场景而言）。因为除了建立 TCP 连接外，还需要进行连接认证。因此，客户端通常会将 TiDB (MySQL) 连接保存到连接池中以重复使用。

Java 有许多连接池实现，如 [HikariCP](https://github.com/brettwooldridge/HikariCP)、[tomcat-jdbc](https://tomcat.apache.org/tomcat-10.1-doc/jdbc-pool.html)、[druid](https://github.com/alibaba/druid)、[c3p0](https://www.mchange.com/projects/c3p0/) 和 [dbcp](https://commons.apache.org/proper/commons-dbcp/)。TiDB 不限制你使用哪种连接池，因此你可以根据应用程序的需要选择任何一种。

### 配置连接数量

根据应用程序自身需求调整连接池大小是一种常见做法。以 HikariCP 为例：

- **maximumPoolSize**：连接池中的最大连接数。如果这个值太大，TiDB 会消耗资源来维护无用的连接。如果这个值太小，应用程序获取连接的速度会变慢。因此，你需要根据应用程序特点来配置这个值。详情请参阅[关于连接池大小](https://github.com/brettwooldridge/HikariCP/wiki/About-Pool-Sizing)。
- **minimumIdle**：连接池中的最小空闲连接数。主要用于在应用程序空闲时保留一些连接以响应突发请求。你也需要根据应用程序特点来配置它。

应用程序在使用完连接后需要归还连接。建议应用程序使用相应的连接池监控（如 **metricRegistry**）来及时定位连接池问题。

### 探测配置

连接池维护从客户端到 TiDB 的持久连接，具体如下：

- 在 v5.4 之前，TiDB 默认不会主动关闭客户端连接（除非报错）。
- 从 v5.4 开始，TiDB 默认会在连接空闲 `28800` 秒（即 `8` 小时）后自动关闭客户端连接。你可以使用 TiDB 和 MySQL 兼容的 `wait_timeout` 变量来控制这个超时设置。更多信息，请参阅 [JDBC 查询超时](/develop/dev-guide-timeouts-in-tidb.md#jdbc-query-timeout)。

此外，客户端和 TiDB 之间可能存在网络代理，如 [LVS](https://en.wikipedia.org/wiki/Linux_Virtual_Server) 或 [HAProxy](https://en.wikipedia.org/wiki/HAProxy)。这些代理通常会在特定空闲时间后（由代理的空闲配置决定）主动清理连接。除了监控代理的空闲配置外，连接池还需要维护或探测连接以保持活跃。

如果你在 Java 应用程序中经常看到以下错误：

```
The last packet sent successfully to the server was 3600000 milliseconds ago. The driver has not received any packets from the server. com.mysql.jdbc.exceptions.jdbc4.CommunicationsException: Communications link failure
```

如果 `n milliseconds ago` 中的 `n` 是 `0` 或一个很小的值，通常是因为执行的 SQL 操作导致 TiDB 异常退出。建议检查 TiDB stderr 日志以找出原因。

如果 `n` 是一个很大的值（如上例中的 `3600000`），很可能是这个连接空闲了很长时间后被代理关闭。通常的解决方案是增加代理的空闲配置值，并允许连接池：

- 每次使用连接前检查连接是否可用。
- 使用单独的线程定期检查连接是否可用。
- 定期发送测试查询以保持连接活跃。

不同的连接池实现可能支持上述一种或多种方法。你可以查看连接池文档以找到相应的配置。

### 经验公式

根据 HikariCP 的[关于连接池大小](https://github.com/brettwooldridge/HikariCP/wiki/About-Pool-Sizing)文章，如果你不知道如何为数据库连接池设置合适的大小，可以从[经验公式](https://github.com/brettwooldridge/HikariCP/wiki/About-Pool-Sizing#connections--core_count--2--effective_spindle_count)开始。然后，根据公式计算出的连接池大小的性能结果，进一步调整大小以达到最佳性能。

经验公式如下：

```
connections = ((core_count * 2) + effective_spindle_count)
```

公式中各参数的说明如下：

- **connections**：获得的连接数大小。
- **core_count**：CPU 核心数。
- **effective_spindle_count**：硬盘数量（不是 [SSD](https://en.wikipedia.org/wiki/Solid-state_drive)）。因为每个旋转硬盘可以称为一个主轴。例如，如果你使用的是具有 16 个磁盘的 RAID 服务器，那么 **effective_spindle_count** 应该是 16。因为 **HDD** 通常一次只能处理一个请求，这里的公式实际上是在衡量你的服务器可以管理多少个并发 I/O 请求。

特别注意[公式](https://github.com/brettwooldridge/HikariCP/wiki/About-Pool-Sizing#the-formula)下面的说明。

> ```
> A formula which has held up pretty well across a lot of benchmarks for years is
> that for optimal throughput the number of active connections should be somewhere
> near ((core_count * 2) + effective_spindle_count). Core count should not include
> HT threads, even if hyperthreading is enabled. Effective spindle count is zero if
> the active data set is fully cached, and approaches the actual number of spindles
> as the cache hit rate falls. ... There hasn't been any analysis so far regarding
> how well the formula works with SSDs.
> ```

这个说明表明：

- **core_count** 是物理核心数，无论你是否启用了 [Hyper-Threading](https://en.wikipedia.org/wiki/Hyper-threading)。
- 当数据完全缓存时，需要将 **effective_spindle_count** 设置为 `0`。随着缓存命中率的降低，该数值会接近实际的 `HDD` 数量。
- **该公式对 _SSD_ 的适用性尚未测试，未知。**

在使用 SSD 时，建议使用以下经验公式代替：

```
connections = (核心数 * 4)
```

因此，在使用 SSD 的情况下，你可以将初始连接池的最大连接数设置为 `核心数 * 4`，然后进一步调整大小以优化性能。

### 调优方向

如你所见，从[经验公式](#经验公式)计算出的大小只是一个推荐的基准值。要在特定机器上获得最佳大小，你需要尝试基准值附近的其他值并测试性能。

以下是一些基本规则，可以帮助你获得最佳大小：

- 如果你的网络或存储延迟较高，增加最大连接数以减少延迟等待时间。当一个线程被延迟阻塞时，其他线程可以接管并继续处理。
- 如果你在服务器上部署了多个服务，每个服务都有单独的连接池，请考虑所有连接池的最大连接数之和。

## 连接参数

Java 应用程序可以用各种框架封装。在大多数框架中，JDBC API 在最底层被调用来与数据库服务器交互。对于 JDBC，建议你关注以下几点：

- JDBC API 使用选择
- API 实现者的参数配置

### JDBC API

关于 JDBC API 的使用，请参阅 [JDBC 官方教程](https://docs.oracle.com/javase/tutorial/jdbc/)。本节介绍几个重要 API 的使用。

#### 使用 Prepare API

对于 OLTP（在线事务处理）场景，程序发送到数据库的 SQL 语句在去除参数变化后是几种可以穷举的类型。因此，建议使用 [Prepared Statements](https://docs.oracle.com/javase/tutorial/jdbc/basics/prepared.html) 而不是常规的[从文本文件执行](https://docs.oracle.com/javase/tutorial/jdbc/basics/processingsqlstatements.html#executing_queries)，并重用 Prepared Statements 直接执行。这避免了在 TiDB 中重复解析和生成 SQL 执行计划的开销。

目前，大多数上层框架都会调用 Prepare API 来执行 SQL。如果你直接使用 JDBC API 进行开发，请注意选择 Prepare API。

此外，在 MySQL Connector/J 的默认实现中，只有客户端语句被预处理，语句在客户端替换 `?` 后以文本文件形式发送到服务器。因此，除了使用 Prepare API 外，你还需要在 JDBC 连接参数中配置 `useServerPrepStmts = true`，才能在 TiDB 服务器上进行语句预处理。有关详细的参数配置，请参阅 [MySQL JDBC 参数](#mysql-jdbc-参数)。

#### 使用 Batch API

对于批量插入，你可以使用 [`addBatch`/`executeBatch` API](https://www.tutorialspoint.com/jdbc/jdbc-batch-processing)。`addBatch()` 方法用于先在客户端缓存多个 SQL 语句，然后在调用 `executeBatch` 方法时一起发送到数据库服务器。

> **注意：**
>
> 在默认的 MySQL Connector/J 实现中，使用 `addBatch()` 添加到批处理的 SQL 语句的发送时间被延迟到调用 `executeBatch()` 时，但在实际网络传输过程中，语句仍然会一条一条发送。因此，这种方法通常不会减少通信开销。
>
> 如果你想批量网络传输，需要在 JDBC 连接参数中配置 `rewriteBatchedStatements = true`。有关详细的参数配置，请参阅[批处理相关参数](#批处理相关参数)。

#### 使用 `StreamingResult` 获取执行结果

在大多数场景中，为了提高执行效率，JDBC 默认会提前获取查询结果并保存在客户端内存中。但当查询返回超大结果集时，客户端通常希望数据库服务器一次返回较少的记录，等到客户端内存就绪后再请求下一批。

通常，JDBC 中有两种处理方法：

- [将 **FetchSize** 设置为 `Integer.MIN_VALUE`](https://dev.mysql.com/doc/connector-j/en/connector-j-reference-implementation-notes.html#ResultSet) 以确保客户端不缓存。客户端将通过网络连接使用 `StreamingResult` 读取执行结果。

    当客户端使用流式读取方法时，需要在继续使用语句进行查询之前完成读取或关闭 `resultset`。否则，会返回错误 `No statements may be issued when any streaming result sets are open and in use on a given connection. Ensure that you have called .close() on any active streaming result sets before attempting more queries.`。

    要避免在客户端完成读取或关闭 `resultset` 之前的查询中出现此类错误，可以在 URL 中添加 `clobberStreamingResults=true` 参数。这样，`resultset` 会自动关闭，但之前流式查询中要读取的结果集会丢失。

- 要使用游标获取，首先[将 `FetchSize` 设置为正整数](http://makejavafaster.blogspot.com/2015/06/jdbc-fetch-size-performance.html)，并在 JDBC URL 中配置 `useCursorFetch=true`。

TiDB 支持这两种方法，但建议使用第一种方法，因为它的实现更简单，执行效率更高。

### MySQL JDBC 参数

JDBC 通常以 JDBC URL 参数的形式提供与实现相关的配置。本节介绍 [MySQL Connector/J 的参数配置](https://dev.mysql.com/doc/connector-j/en/connector-j-reference-configuration-properties.html)（如果你使用 MariaDB，请参阅 [MariaDB 的参数配置](https://mariadb.com/kb/en/library/about-mariadb-connector-j/#optional-url-parameters)）。由于本文无法涵盖所有配置项，主要关注几个可能影响性能的参数。

#### Prepare 相关参数

本节介绍与 `Prepare` 相关的参数。

- **useServerPrepStmts**

    **useServerPrepStmts** 默认设置为 `false`，即使你使用 Prepare API，"prepare" 操作也只会在客户端完成。为避免服务器的解析开销，如果同一个 SQL 语句多次使用 Prepare API，建议将此配置设置为 `true`。

    要验证此设置是否已生效，你可以：

    - 进入 TiDB 监控面板，通过 **Query Summary** > **CPS By Instance** 查看请求命令类型。
    - 如果请求中的 `COM_QUERY` 被 `COM_STMT_EXECUTE` 或 `COM_STMT_PREPARE` 替换，说明此设置已生效。

- **cachePrepStmts**

    虽然 `useServerPrepStmts=true` 允许服务器执行 Prepared Statements，但默认情况下，客户端会在每次执行后关闭 Prepared Statements 而不重用它们。这意味着 "prepare" 操作的效率甚至不如文本文件执行。要解决这个问题，建议在设置 `useServerPrepStmts=true` 后，还要配置 `cachePrepStmts=true`。这允许客户端缓存 Prepared Statements。

    要验证此设置是否已生效，你可以：

    - 进入 TiDB 监控面板，通过 **Query Summary** > **CPS By Instance** 查看请求命令类型。
    - 如果请求中 `COM_STMT_EXECUTE` 的数量远多于 `COM_STMT_PREPARE` 的数量，说明此设置已生效。

    此外，配置 `useConfigs=maxPerformance` 将同时配置多个参数，包括 `cachePrepStmts=true`。

- **prepStmtCacheSqlLimit**

    配置 `cachePrepStmts` 后，还要注意 `prepStmtCacheSqlLimit` 配置（默认值为 `256`）。此配置控制客户端缓存的 Prepared Statements 的最大长度。

    超过此最大长度的 Prepared Statements 将不会被缓存，因此无法重用。在这种情况下，你可以根据应用程序的实际 SQL 长度考虑增加此配置的值。

    如果你：

    - 进入 TiDB 监控面板，通过 **Query Summary** > **CPS By Instance** 查看请求命令类型。
    - 发现已配置 `cachePrepStmts=true`，但 `COM_STMT_PREPARE` 仍然基本等于 `COM_STMT_EXECUTE` 且存在 `COM_STMT_CLOSE`。

    则需要检查此设置是否太小。

- **prepStmtCacheSize**

    **prepStmtCacheSize** 控制缓存的 Prepared Statements 的数量（默认值为 `25`）。如果你的应用程序需要 "prepare" 多种类型的 SQL 语句并希望重用 Prepared Statements，可以增加此值。

    要验证此设置是否已生效，你可以：

    - 进入 TiDB 监控面板，通过 **Query Summary** > **CPS By Instance** 查看请求命令类型。
    - 如果请求中 `COM_STMT_EXECUTE` 的数量远多于 `COM_STMT_PREPARE` 的数量，说明此设置已生效。

#### 批处理相关参数

在处理批量写入时，建议配置 `rewriteBatchedStatements=true`。在使用 `addBatch()` 或 `executeBatch()` 后，JDBC 默认仍然一条一条地发送 SQL，例如：

```java
pstmt = prepare("INSERT INTO `t` (a) values(?)");
pstmt.setInt(1, 10);
pstmt.addBatch();
pstmt.setInt(1, 11);
pstmt.addBatch();
pstmt.setInt(1, 12);
pstmt.executeBatch();
```

虽然使用了 `Batch` 方法，但发送到 TiDB 的 SQL 语句仍然是单独的 `INSERT` 语句：

```sql
INSERT INTO `t` (`a`) VALUES(10);
INSERT INTO `t` (`a`) VALUES(11);
INSERT INTO `t` (`a`) VALUES(12);
```

但如果设置 `rewriteBatchedStatements=true`，发送到 TiDB 的 SQL 语句将是一条 `INSERT` 语句：

```sql
INSERT INTO `t` (`a`) values(10),(11),(12);
```

注意，`INSERT` 语句的重写是将多个 "values" 关键字后的值连接成一个完整的 SQL 语句。如果 `INSERT` 语句有其他差异，它们就不能被重写，例如：

```sql
INSERT INTO `t` (`a`) VALUES (10) ON DUPLICATE KEY UPDATE `a` = 10;
INSERT INTO `t` (`a`) VALUES (11) ON DUPLICATE KEY UPDATE `a` = 11;
INSERT INTO `t` (`a`) VALUES (12) ON DUPLICATE KEY UPDATE `a` = 12;
```

上述 `INSERT` 语句不能重写为一条语句。但如果你将这三条语句改为以下形式：

```sql
INSERT INTO `t` (`a`) VALUES (10) ON DUPLICATE KEY UPDATE `a` = VALUES(`a`);
INSERT INTO `t` (`a`) VALUES (11) ON DUPLICATE KEY UPDATE `a` = VALUES(`a`);
INSERT INTO `t` (`a`) VALUES (12) ON DUPLICATE KEY UPDATE `a` = VALUES(`a`);
```

那么它们就满足重写要求。上述 `INSERT` 语句将被重写为以下一条语句：

```sql
INSERT INTO `t` (`a`) VALUES (10), (11), (12) ON DUPLICATE KEY UPDATE a = VALUES(`a`);
```

如果在批量更新期间有三个或更多更新，SQL 语句将被重写并作为多个查询发送。这有效减少了客户端到服务器的请求开销，但副作用是生成了一个更大的 SQL 语句。例如：

```sql
UPDATE `t` SET `a` = 10 WHERE `id` = 1; UPDATE `t` SET `a` = 11 WHERE `id` = 2; UPDATE `t` SET `a` = 12 WHERE `id` = 3;
```

此外，由于[客户端错误](https://bugs.mysql.com/bug.php?id=96623)，如果你想在批量更新期间配置 `rewriteBatchedStatements=true` 和 `useServerPrepStmts=true`，建议你也配置 `allowMultiQueries=true` 参数以避免此错误。

#### 集成参数

通过监控，你可能会注意到，虽然应用程序只对 TiDB 集群执行 `INSERT` 操作，但有很多冗余的 `SELECT` 语句。通常这是因为 JDBC 发送一些 SQL 语句来查询设置，例如 `select @@session.transaction_read_only`。这些 SQL 语句对 TiDB 来说是无用的，因此建议配置 `useConfigs=maxPerformance` 以避免额外开销。

`useConfigs=maxPerformance` 包含一组配置。要获取 MySQL Connector/J 8.0 和 MySQL Connector/J 5.1 中的详细配置，请分别参阅 [mysql-connector-j 8.0](https://github.com/mysql/mysql-connector-j/blob/release/8.0/src/main/resources/com/mysql/cj/configurations/maxPerformance.properties) 和 [mysql-connector-j 5.1](https://github.com/mysql/mysql-connector-j/blob/release/5.1/src/com/mysql/jdbc/configs/maxPerformance.properties)。

配置后，你可以通过监控查看 `SELECT` 语句数量的减少。

#### 超时相关参数

TiDB 提供两个与 MySQL 兼容的参数来控制超时：[`wait_timeout`](/system-variables.md#wait_timeout) 和 [`max_execution_time`](/system-variables.md#max_execution_time)。这两个参数分别控制与 Java 应用程序的连接空闲超时和连接中 SQL 执行的超时；也就是说，这些参数控制 TiDB 与 Java 应用程序之间连接的最长空闲时间和最长忙碌时间。从 TiDB v5.4 开始，`wait_timeout` 的默认值为 `28800` 秒，即 8 小时。对于早于 v5.4 的 TiDB 版本，默认值为 `0`，表示超时时间无限制。`max_execution_time` 的默认值为 `0`，表示 SQL 语句的最大执行时间无限制。

[`wait_timeout`](/system-variables.md#wait_timeout) 的默认值相对较大。在事务已启动但既未提交也未回滚的场景中，你可能需要更细粒度的控制和更短的超时时间以防止长时间持有锁。在这种情况下，你可以使用 [`tidb_idle_transaction_timeout`](/system-variables.md#tidb_idle_transaction_timeout-new-in-v760)（在 TiDB v7.6.0 中引入）来控制用户会话中事务的空闲超时。

然而，在实际生产环境中，空闲连接和执行时间过长的 SQL 语句会对数据库和应用程序产生负面影响。为避免空闲连接和执行时间过长的 SQL 语句，你可以在应用程序的连接字符串中配置这两个参数。例如，设置 `sessionVariables=wait_timeout=3600`（1 小时）和 `sessionVariables=max_execution_time=300000`（5 分钟）。

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上询问社区，或[提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上询问社区，或[提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>
