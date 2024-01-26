---
title: 连接池与连接参数
summary: 针对开发者的 TiDB 连接池与连接参数的说明。
aliases: ['/zh/tidb/dev/connection-parameters']
---

# 连接池与连接参数

> - 连接池参数 - 连接数配置、探活配置两节摘自[开发 Java 应用使用 TiDB 的最佳实践 - 连接池](/best-practices/java-app-best-practices.md#连接池)。
> - 连接参数摘自[开发 Java 应用使用 TiDB 的最佳实践 - JDBC](/best-practices/java-app-best-practices.md#jdbc)。

## 连接池参数

TiDB (MySQL) 连接建立是比较昂贵的操作（至少对于 OLTP 来讲），除了建立 TCP 连接外还需要进行连接鉴权操作，所以客户端通常会把 TiDB (MySQL) 连接保存到连接池中进行复用。

Java 的连接池实现很多 ([HikariCP](https://github.com/brettwooldridge/HikariCP), [tomcat-jdbc](https://tomcat.apache.org/tomcat-10.1-doc/jdbc-pool.html), [druid](https://github.com/alibaba/druid), [c3p0](https://www.mchange.com/projects/c3p0/), [dbcp](https://commons.apache.org/proper/commons-dbcp/))，TiDB 不会限定使用的连接池，应用可以根据业务特点自行选择连接池实现。

### 连接数配置

比较常见的是应用需要根据自身情况配置合适的连接池大小，以 HikariCP 为例：

**maximumPoolSize**：连接池最大连接数，配置过大会导致 TiDB 消耗资源维护无用连接，配置过小则会导致应用获取连接变慢，所以需根据应用自身特点配置合适的值，可参考[这篇文章](https://github.com/brettwooldridge/HikariCP/wiki/About-Pool-Sizing)。

**minimumIdle**：连接池最小空闲连接数，主要用于在应用空闲时存留一些连接以应对突发请求，同样是需要根据业务情况进行配置。

应用在使用连接池时，需要注意连接使用完成后归还连接，推荐应用使用对应的连接池相关监控（如 **metricRegistry**），通过监控能及时定位连接池问题。

### 探活配置

连接池维护到 TiDB 的长连接，TiDB 默认不会主动关闭客户端连接（除非报错），但一般客户端到 TiDB 之间还会有 [LVS](https://en.wikipedia.org/wiki/Linux_Virtual_Server) 或 [HAProxy](https://en.wikipedia.org/wiki/HAProxy) 之类的网络代理，它们通常会在连接空闲一定时间后主动清理连接。除了注意代理的 idle 配置外，连接池还需要进行保活或探测连接。

如果常在 Java 应用中看到以下错误：

```
The last packet sent successfully to the server was 3600000 milliseconds ago. The driver has not received any packets from the server. com.mysql.jdbc.exceptions.jdbc4.CommunicationsException: Communications link failure
```

如果 `n milliseconds ago` 中的 n 如果是 0 或很小的值，则通常是执行的 SQL 导致 TiDB 异常退出引起的报错，推荐查看 TiDB stderr 日志；如果 n 是一个非常大的值（比如这里的 3600000），很可能是因为这个连接空闲太久然后被中间 proxy 关闭了，通常解决方式除了调大 proxy 的 idle 配置，还可以让连接池执行以下操作：

- 每次使用连接前检查连接是否可用。
- 使用单独线程定期检查连接是否可用。
- 定期发送 test query 保活连接。

不同的连接池实现可能会支持其中一种或多种方式，可以查看所使用的连接池文档来寻找对应配置。

### 经验公式

在 HikariCP 的 [About Pool Sizing](https://github.com/brettwooldridge/HikariCP/wiki/About-Pool-Sizing) 一文中可以了解到，在完全不知道如何设置数据库连接池大小的时候，可以考虑以以下[经验公式](https://github.com/brettwooldridge/HikariCP/wiki/About-Pool-Sizing#connections--core_count--2--effective_spindle_count)为起点，在此基础上，围绕该结果进行尝试，以得到最高性能的连接池大小。

该经验公式描述如下：

```
connections = ((core_count * 2) + effective_spindle_count)
```

解释一下参数含义：

- **connections**: 得出的连接数大小。
- **core_count**: CPU 核心数。
- **effective_spindle_count**: 直译为**有效主轴数**，实际上是说你有多少个硬盘（非 [SSD](https://en.wikipedia.org/wiki/Solid-state_drive)），因为每个旋转的硬盘可以被称为是一个旋转轴。例如，你使用的是一个有 16 个磁盘组成的 [RAID](https://en.wikipedia.org/wiki/RAID) 阵列的服务器，那么 **effective_spindle_count** 应为 16。此处经验公式，实际上是衡量你的服务器可以管理多少 I/O 并发请求，因为 **HDD** 通常只能串行请求。

要特别说明的是，在这个经验公式的的下方，也看到了一处说明：

> ```
> A formula which has held up pretty well across a lot of benchmarks for years is
> that for optimal throughput the number of active connections should be somewhere
> near ((core_count * 2) + effective_spindle_count). Core count should not include
> HT threads, even if hyperthreading is enabled. Effective spindle count is zero if
> the active data set is fully cached, and approaches the actual number of spindles
> as the cache hit rate falls. ... There hasn't been any analysis so far regarding
> how well the formula works with SSDs.
> ```

这个说明指出：

1. **core_count** 就是_物理核心数_，与你是否开启[超线程](https://en.wikipedia.org/wiki/Hyper-threading)无关。
2. 数据被全量缓存时，**effective_spindle_count** 应被设置为 0，随着命中率的下降，会更加接近实际的 HDD 个数。
3. **这里没有任何基于 _SSD_ 的经验公式。**

这里的说明让你在使用 SSD 时，需探求其他的经验公式。

可以参考 CockroachDB 对[数据库连接池](https://www.cockroachlabs.com/docs/stable/connection-pooling.html?#sizing-connection-pools)中的描述，推荐的连接数大小公式为：

```
connections = (number of cores * 4)
```

因此，你在使用 SSD 的情况下可以将连接数设置为 `CPU 核心数 * 4`。以此来达到初始的连接池最大连接数大小，并以此数据周围进行进一步的调整。

### 调整方向

可以看到，在上方的[经验公式](#经验公式)中得到的，是一个推荐的初始值，若需得到某台具体机器上的最佳值，需在推荐值周围，通过尝试，得到最佳值。

此最佳值的获取，会有一些基本规律，此处罗列如下：

1. 如果你的网络或存储延迟较大，请增大你的最大连接数，可以进行等待，从而让线程在被阻塞时，其他的线程可继续进行处理。
2. 如果你的服务器上部署了多个服务，并且每个服务拥有独立的连接池时，请关注它们的连接池的最大连接数总和。

## 连接参数

Java 应用尽管可以选择在不同的框架中封装，但在最底层一般会通过调用 JDBC 来与数据库服务器进行交互。对于 JDBC，需要关注的主要有：API 的使用选择和 API Implementer 的参数配置。

### JDBC API

对于基本的 JDBC API 使用可以参考 [JDBC 官方教程](https://docs.oracle.com/javase/tutorial/jdbc/)，本文主要强调几个比较重要的 API 选择。

### 使用 Prepare API

对于 OLTP 场景，程序发送给数据库的 SQL 语句在去除参数变化后都是可穷举的某几类，因此建议使用[预处理语句 (Prepared Statements)](https://docs.oracle.com/javase/tutorial/jdbc/basics/prepared.html) 代替普通的[文本执行](https://docs.oracle.com/javase/tutorial/jdbc/basics/processingsqlstatements.html#executing_queries)，并复用预处理语句来直接执行，从而避免 TiDB 重复解析和生成 SQL 执行计划的开销。

目前多数上层框架都会调用 Prepare API 进行 SQL 执行，如果直接使用 JDBC API 进行开发，注意选择使用 Prepare API。

另外需要注意 MySQL Connector/J 实现中默认只会做客户端的语句预处理，会将 `?` 在客户端替换后以文本形式发送到服务端，所以除了要使用 Prepare API，还需要在 JDBC 连接参数中配置 `useServerPrepStmts = true`，才能在 TiDB 服务器端进行语句预处理（下面参数配置章节有详细介绍）。

### 使用 Batch 批量插入更新

对于批量插入更新，如果插入记录较多，可以选择使用 [addBatch/executeBatch API](https://www.tutorialspoint.com/jdbc/jdbc-batch-processing)。通过 addBatch 的方式将多条 SQL 的插入更新记录先缓存在客户端，然后在 executeBatch 时一起发送到数据库服务器。

> **注意：**
>
> 对于 MySQL Connector/J 实现，默认 Batch 只是将多次 addBatch 的 SQL 发送时机延迟到调用 executeBatch 的时候，但实际网络发送还是会一条条的发送，通常不会降低与数据库服务器的网络交互次数。
>
> 如果希望 Batch 网络发送，需要在 JDBC 连接参数中配置 `rewriteBatchedStatements = true`（下面参数配置章节有详细介绍）。

### 使用 StreamingResult 流式获取执行结果

一般情况下，为提升执行效率，JDBC 会默认提前获取查询结果并将其保存在客户端内存中。但在查询返回超大结果集的场景中，客户端会希望数据库服务器减少向客户端一次返回的记录数，等客户端在有限内存处理完一部分后再去向服务器要下一批。

在 JDBC 中通常有以下两种处理方式：

- 设置 [**FetchSize** 为 `Integer.MIN_VALUE`](https://dev.mysql.com/doc/connector-j/en/connector-j-reference-implementation-notes.html#ResultSet) 让客户端不缓存，客户端通过 StreamingResult 的方式从网络连接上流式读取执行结果。
- 使用 Cursor Fetch，首先需[设置 **FetchSize**](http://makejavafaster.blogspot.com/2015/06/jdbc-fetch-size-performance.html) 为正整数，且在 JDBC URL 中配置 `useCursorFetch = true`。

TiDB 中同时支持两种方式，但更推荐使用第一种将 **FetchSize** 设置为 `Integer.MIN_VALUE` 的方式，比第二种功能实现更简单且执行效率更高。

### MySQL JDBC 参数

JDBC 实现通常通过 JDBC URL 参数的形式来提供实现相关的配置。这里以 MySQL 官方的 Connector/J 来介绍[参数配置](https://dev.mysql.com/doc/connector-j/en/connector-j-reference-configuration-properties.html)（如果使用的是 MariaDB，可以参考 [MariaDB 的类似配置](https://mariadb.com/kb/en/library/about-mariadb-connector-j/#optional-url-parameters)）。因为配置项较多，这里主要关注几个可能影响到性能的参数。

#### Prepare 相关参数

- **useServerPrepStmts**

    默认情况下，**useServerPrepStmts** 的值为 `false`，即尽管使用了 Prepare API，也只会在客户端做 “prepare”。因此为了避免服务器重复解析的开销，如果同一条 SQL 语句需要多次使用 Prepare API，则建议设置该选项为 `true`。

    在 TiDB 监控中可以通过 **Query Summary > CPS By Instance** 查看请求命令类型，如果请求中 `COM_QUERY` 被 `COM_STMT_EXECUTE` 或 `COM_STMT_PREPARE` 代替即生效。

- **cachePrepStmts**

    虽然 `useServerPrepStmts = true` 能让服务端执行预处理语句，但默认情况下客户端每次执行完后会 close 预处理语句，并不会复用，这样预处理的效率甚至不如文本执行。所以建议开启 `useServerPrepStmts = true` 后同时配置 `cachePrepStmts = true`，这会让客户端缓存预处理语句。

    在 TiDB 监控中可以通过 **Query Summary > CPS By Instance** 查看请求命令类型，如果请求中 `COM_STMT_EXECUTE` 数目远远多于 `COM_STMT_PREPARE` 即生效。

    另外，通过 `useConfigs = maxPerformance` 配置会同时配置多个参数，其中也包括 `cachePrepStmts = true`。

- **prepStmtCacheSqlLimit**

    在配置 **cachePrepStmts** 后还需要注意 **prepStmtCacheSqlLimit** 配置（默认为 `256`），该配置控制客户端缓存预处理语句的最大长度，超过该长度将不会被缓存。

    在一些场景 SQL 的长度可能超过该配置，导致预处理 SQL 不能复用，建议根据应用 SQL 长度情况决定是否需要调大该值。

    在 TiDB 监控中通过 **Query Summary > CPS By Instance** 查看请求命令类型，如果已经配置了 `cachePrepStmts = true`，但 `COM_STMT_PREPARE` 还是和 `COM_STMT_EXECUTE` 基本相等且有 `COM_STMT_CLOSE`，需要检查这个配置项是否设置得太小。

- **prepStmtCacheSize**

    控制缓存的预处理语句数目（默认为 `25`），如果应用需要预处理的 SQL 种类很多且希望复用预处理语句，可以调大该值。

    和上一条类似，在监控中通过 **Query Summary > CPS By Instance** 查看请求中 `COM_STMT_EXECUTE` 数目是否远远多于 `COM_STMT_PREPARE` 来确认是否正常。

#### Batch 相关参数

在进行 batch 写入处理时推荐配置 `rewriteBatchedStatements = true`，在已经使用 `addBatch` 或 `executeBatch` 后默认 JDBC 还是会一条条 SQL 发送，例如：

```java
pstmt = prepare("INSERT INTO `t` (`a`) VALUES(?)");
pstmt.setInt(1, 10);
pstmt.addBatch();
pstmt.setInt(1, 11);
pstmt.addBatch();
pstmt.setInt(1, 12);
pstmt.executeBatch();
```

虽然使用了 batch 但发送到 TiDB 语句还是单独的多条 insert：

```sql
INSERT INTO `t` (`a`) VALUES(10);
INSERT INTO `t` (`a`) VALUES(11);
INSERT INTO `t` (`a`) VALUES(12);
```

如果设置 `rewriteBatchedStatements = true`，发送到 TiDB 的 SQL 将是：

```sql
INSERT INTO `t` (`a`) VALUES(10),(11),(12);
```

需要注意的是，insert 语句的改写，只能将多个 values 后的值拼接成一整条 SQL, insert 语句如果有其他差异将无法被改写。例如：

```sql
INSERT INTO `t` (`a`) VALUES (10) ON DUPLICATE KEY UPDATE `a` = 10;
INSERT INTO `t` (`a`) VALUES (11) ON DUPLICATE KEY UPDATE `a` = 11;
INSERT INTO `t` (`a`) VALUES (12) ON DUPLICATE KEY UPDATE `a` = 12;
```

上述 insert 语句将无法被改写成一条语句。该例子中，如果将 SQL 改写成如下形式：

```sql
INSERT INTO `t` (`a`) VALUES (10) ON DUPLICATE KEY UPDATE `a` = values(`a`);
INSERT INTO `t` (`a`) VALUES (11) ON DUPLICATE KEY UPDATE `a` = values(`a`);
INSERT INTO `t` (`a`) VALUES (12) ON DUPLICATE KEY UPDATE `a` = values(`a`);
```

即可满足改写条件，最终被改写成：

```sql
INSERT INTO `t` (`a`) VALUES (10), (11), (12) ON DUPLICATE KEY UPDATE `a` = values(`a`);
```

批量更新时如果有 3 处或 3 处以上更新，则 SQL 语句会改写为 multiple-queries 的形式并发送，这样可以有效减少客户端到服务器的请求开销，但副作用是会产生较大的 SQL 语句，例如这样：

```sql
UPDATE `t` SET `a` = 10 WHERE `id` = 1;
UPDATE `t` SET `a` = 11 WHERE `id` = 2;
UPDATE `t` SET `a` = 12 WHERE `id` = 3;
```

另外，因为一个[客户端 bug](https://bugs.mysql.com/bug.php?id=96623)，批量更新时如果要配置 `rewriteBatchedStatements = true` 和 `useServerPrepStmts = true`，推荐同时配置 `allowMultiQueries = true` 参数来避免这个 bug。

#### 集成参数

通过监控可能会发现，虽然业务只向集群进行 insert 操作，却看到有很多多余的 select 语句。通常这是因为 JDBC 发送了一些查询设置类的 SQL 语句（例如 `select @@session.transaction_read_only`）。这些 SQL 对 TiDB 无用，推荐配置 `useConfigs = maxPerformance` 来避免额外开销。

`useConfigs = maxPerformance` 会包含一组配置，可查看 MySQL Connector/J [8.0 版本](https://github.com/mysql/mysql-connector-j/blob/release/8.0/src/main/resources/com/mysql/cj/configurations/maxPerformance.properties) 或 [5.1 版本](https://github.com/mysql/mysql-connector-j/blob/release/5.1/src/com/mysql/jdbc/configs/maxPerformance.properties) 来确认当前 MySQL Connector/J 中 `maxPerformance` 包含的具体配置。

配置后查看监控，可以看到多余语句减少。

#### 超时参数

TiDB 提供两个与 MySQL 兼容的超时控制参数，[`wait_timeout`](/system-variables.md#wait_timeout) 和 [`max_execution_time`](/system-variables.md#max_execution_time)。这两个参数分别控制与 Java 应用连接的空闲超时时间和连接中 SQL 执行的超时时间，即控制 TiDB 与 Java 应用的连接最长闲多久和最长忙多久。在 TiDB v5.4 及以上版本中，`wait_timeout` 参数默认值为 `28800` 秒，即空闲超时为 8 小时。在 v5.4 之前，`wait_timeout` 参数的默认值为 `0`，即没有时间限制。 `max_execution_time` 参数的默认值为 `0`，即不限制一条 SQL 语句的执行时间。

但是 [`wait_timeout`](/system-variables.md#wait_timeout) 的默认值比较大，在事务已启动但未提交或回滚的情况下，你可能需要更细粒度的控制和更短的超时，以避免持有锁的时间过长。此时，你可以使用 TiDB 在 v7.6.0 引入的 [`tidb_idle_transaction_timeout`](/system-variables.md#tidb_idle_transaction_timeout-从-v760-版本开始引入) 控制用户会话中事务的空闲超时。

但在实际生产环境中，空闲连接和一直无限执行的 SQL 对数据库和应用都有不好的影响。你可以通过在应用的连接字符串中配置这两个参数来避免空闲连接和执行时间过长的 SQL 语句。例如，设置 `sessionVariables=wait_timeout=3600`（1 小时）和 `sessionVariables=max_execution_time=300000`（5 分钟）。
