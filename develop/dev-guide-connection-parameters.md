---
title: Connection Pools and Connection Parameters
---

# Connection Pools and Connection Parameters

This document describes how to configure connection pools and connection parameters when you use a driver or ORM framework to connect to TiDB.

<CustomContent platform="tidb">

If you are interested in more tips about Java application development, see [Best Practices for Developing Java Applications with TiDB](/best-practices/java-app-best-practices.md#connection-pool)

</CustomContent>

<CustomContent platform="tidb-cloud">

If you are interested in more tips about Java application development, see [Best Practices for Developing Java Applications with TiDB](https://docs.pingcap.com/tidb/stable/java-app-best-practices)

</CustomContent>

## Connection pool

Building TiDB (MySQL) connections is relatively expensive (for OLTP scenarios at least). Because in addition to building a TCP connection, connection authentication is also required. Therefore, the client usually saves the TiDB (MySQL) connections to the connection pool for reuse.

Java has many connection pool implementations such as [HikariCP](https://github.com/brettwooldridge/HikariCP), [tomcat-jdbc](https://tomcat.apache.org/tomcat-10.1-doc/jdbc-pool.html), [druid](https://github.com/alibaba/druid), [c3p0](https://www.mchange.com/projects/c3p0/), and [dbcp](https://commons.apache.org/proper/commons-dbcp/). TiDB does not limit which connection pool you use, so you can choose whichever you like for your application.

### Configure the number of connections

It is a common practice that the connection pool size is well adjusted according to the application's own needs. Take HikariCP as an example:

- **maximumPoolSize**: The maximum number of connections in the connection pool. If this value is too large, TiDB consumes resources to maintain useless connections. If this value is too small, the application gets slow connections. Therefore, you need to configure this value according to your application characteristics. For details, see [About Pool Sizing](https://github.com/brettwooldridge/HikariCP/wiki/About-Pool-Sizing).
- **minimumIdle**: The minimum number of idle connections in the connection pool. It is mainly used to reserve some connections to respond to sudden requests when the application is idle. You also need to configure it according to your application characteristics.

The application needs to return the connection after finishing using it. It is recommended that the application uses the corresponding connection pool monitoring (such as **metricRegistry**) to locate connection pool issues in time.

### Probe configuration

The connection pool maintains persistent connections to TiDB. TiDB does not proactively close client connections by default (unless an error is reported), but generally, there are also network proxies such as [LVS](https://en.wikipedia.org/wiki/Linux_Virtual_Server) or [HAProxy](https://en.wikipedia.org/wiki/HAProxy) between the client and TiDB. Usually, these proxies proactively clean up connections that are idle for a certain period. In addition to paying attention to the idle configuration of the proxies, the connection pool also needs to keep alive or probe connections.

If you often see the following error in your Java application:

```
The last packet sent successfully to the server was 3600000 milliseconds ago. The driver has not received any packets from the server. com.mysql.jdbc.exceptions.jdbc4.CommunicationsException: Communications link failure
```

If `n` in `n milliseconds ago` is `0` or a very small value, it is usually because the executed SQL operation causes TiDB to exit abnormally. To find the cause, it is recommended to check the TiDB stderr log.

If `n` is a very large value (such as `3600000` in the above example), it is likely that this connection was idle for a long time and then closed by the proxy. The usual solution is to increase the value of the proxy's idle configuration and allow the connection pool to:

- Check whether the connection is available before using the connection every time.
- Regularly check whether the connection is available using a separate thread.
- Send a test query regularly to keep alive connections.

Different connection pool implementations might support one or more of the above methods. You can check your connection pool documentation to find the corresponding configuration.

### Formulas based on experience

According to the [About Pool Sizing](https://github.com/brettwooldridge/HikariCP/wiki/About-Pool-Sizing) article of HikariCP, if you have no idea about how to set a proper size for the database connection pool, you can get started with a [formula based on experience](https://github.com/brettwooldridge/HikariCP/wiki/About-Pool-Sizing#connections--core_count--2--effective_spindle_count). Then, based on the performance result of the pool size calculated from the formula, you can further adjust the size to achieve the best performance.

The formula based on experience is as follows:

```
connections = ((core_count * 2) + effective_spindle_count)
```

The description of each parameter in the formula is as follows:

- **connections**: the size of connections obtained.
- **core_count**: the number of CPU cores.
- **effective_spindle_count**: the number of hard drives (not [SSD](https://en.wikipedia.org/wiki/Solid-state_drive)). Because each spinning hard disk can be called a spindle. For example, if you are using a server with a RAID of 16 disks, the **effective_spindle_count** should be 16. Because **HDD** usually can handle only one request at a time, the formula here is actually measuring how many concurrent I/O requests your server can manage.

In particular, pay attention to the following note below the [formula](https://github.com/brettwooldridge/HikariCP/wiki/About-Pool-Sizing#the-formula).

> ```
> A formula which has held up pretty well across a lot of benchmarks for years is
> that for optimal throughput the number of active connections should be somewhere
> near ((core_count * 2) + effective_spindle_count). Core count should not include
> HT threads, even if hyperthreading is enabled. Effective spindle count is zero if
> the active data set is fully cached, and approaches the actual number of spindles
> as the cache hit rate falls. ... There hasn't been any analysis so far regarding
> how well the formula works with SSDs.
> ```

This note indicates that:

- **core_count** is the number of physical cores, regardless of whether you enable [Hyper-Threading](https://en.wikipedia.org/wiki/Hyper-threading) or not.
- When data is fully cached, you need to set **effective_spindle_count** to `0`. As the hit rate of cache decreases, the count is closer to the actual number of `HDD`.
- **Whether the formula works for _SSD_ is not tested and unknown.**

When using SSDs, it is recommended that you use the following formula based on experience instead:

```
connections = (number of cores * 4)
```

Therefore, you can set the maximum connection size of the initial connection pool to `cores * 4` in the case of SSDs and further adjust the size to tune the performance.

### Tuning direction

As you can see, a size calculated from the [formulas based on experience](#formulas-based-on-experience) is just a recommended base value. To get the optimal size on a specific machine, you need to try other values around the base value and test the performance.

Here are some basic rules to help you get the optimal size:

- If your network or storage latency is high, increase your maximum number of connections to reduce the latency waiting time. Once a thread is blocked by latency, other threads can take over and continue processing.
- If you have multiple services deployed on your server and each service has a separate connection pool, consider the sum of the maximum number of connections to all connection pools.

## Connection parameters

Java applications can be encapsulated with various frameworks. In most of the frameworks, JDBC API is called on the bottommost level to interact with the database server. For JDBC, it is recommended that you focus on the following things:

- JDBC API usage choice
- API Implementer's parameter configuration

### JDBC API

For JDBC API usage, see [JDBC official tutorial](https://docs.oracle.com/javase/tutorial/jdbc/). This section covers the usage of several important APIs.

#### Use Prepare API

For OLTP (Online Transactional Processing) scenarios, the SQL statements sent by the program to the database are several types that can be exhausted after removing parameter changes. Therefore, it is recommended to use [Prepared Statements](https://docs.oracle.com/javase/tutorial/jdbc/basics/prepared.html) instead of regular [execution from a text file](https://docs.oracle.com/javase/tutorial/jdbc/basics/processingsqlstatements.html#executing_queries) and reuse Prepared Statements to execute directly. This avoids the overhead of repeatedly parsing and generating SQL execution plans in TiDB.

At present, most upper-level frameworks call the Prepare API for SQL execution. If you use the JDBC API directly for development, pay attention to choosing the Prepare API.

In addition, with the default implementation of MySQL Connector/J, only client-side statements are preprocessed, and the statements are sent to the server in a text file after `?` is replaced on the client. Therefore, in addition to using the Prepare API, you also need to configure `useServerPrepStmts = true` in JDBC connection parameters before you perform statement preprocessing on the TiDB server. For detailed parameter configuration, see [MySQL JDBC parameters](#mysql-jdbc-parameters).

#### Use Batch API

For batch inserts, you can use the [`addBatch`/`executeBatch` API](https://www.tutorialspoint.com/jdbc/jdbc-batch-processing). The `addBatch()` method is used to cache multiple SQL statements first on the client, and then send them to the database server together when calling the `executeBatch` method.

> **Note:**
>
> In the default MySQL Connector/J implementation, the sending time of the SQL statements that are added to batch with `addBatch()` is delayed to the time when `executeBatch()` is called, but the statements will still be sent one by one during the actual network transfer. Therefore, this method usually does not reduce the amount of communication overhead.
>
> If you want to batch network transfer, you need to configure `rewriteBatchedStatements = true` in the JDBC connection parameters. For the detailed parameter configuration, see [Batch-related parameters](#batch-related-parameters).

#### Use `StreamingResult` to get the execution result

In most scenarios, to improve execution efficiency, JDBC obtains query results in advance and saves them in client memory by default. But when the query returns a super large result set, the client often wants the database server to reduce the number of records returned at a time and waits until the client's memory is ready and it requests for the next batch.

Usually, there are two kinds of processing methods in JDBC:

- [Set **FetchSize** to `Integer.MIN_VALUE`](https://dev.mysql.com/doc/connector-j/en/connector-j-reference-implementation-notes.html#ResultSet) to ensure that the client does not cache. The client will read the execution result from the network connection through `StreamingResult`.

    When the client uses the streaming read method, it needs to finish reading or close `resultset` before continuing to use the statement to make a query. Otherwise, the error `No statements may be issued when any streaming result sets are open and in use on a given connection. Ensure that you have called .close() on any active streaming result sets before attempting more queries.` is returned.

    To avoid such an error in queries before the client finishes reading or closes `resultset`, you can add the `clobberStreamingResults=true` parameter in the URL. Then, `resultset` is automatically closed but the result set to be read in the previous streaming query is lost.

- To use Cursor Fetch, first [set `FetchSize`](http://makejavafaster.blogspot.com/2015/06/jdbc-fetch-size-performance.html) as a positive integer and configure `useCursorFetch=true` in the JDBC URL.

TiDB supports both methods, but it is preferred that you use the first method, because it is a simpler implementation and has a better execution efficiency.

### MySQL JDBC parameters

JDBC usually provides implementation-related configurations in the form of JDBC URL parameters. This section introduces [MySQL Connector/J's parameter configurations](https://dev.mysql.com/doc/connector-j/en/connector-j-reference-configuration-properties.html) (If you use MariaDB, see [MariaDB's parameter configurations](https://mariadb.com/kb/en/library/about-mariadb-connector-j/#optional-url-parameters)). Because this document cannot cover all configuration items, it mainly focuses on several parameters that might affect performance.

#### Prepare-related parameters

This section introduces parameters related to `Prepare`.

- **useServerPrepStmts**

    **useServerPrepStmts** is set to `false` by default, that is, even if you use the Prepare API, the "prepare" operation will be done only on the client. To avoid the parsing overhead of the server, if the same SQL statement uses the Prepare API multiple times, it is recommended to set this configuration to `true`.

    To verify that this setting already takes effect, you can do:

    - Go to TiDB monitoring dashboard and view the request command type through **Query Summary** > **CPS By Instance**.
    - If `COM_QUERY` is replaced by `COM_STMT_EXECUTE` or `COM_STMT_PREPARE` in the request, it means this setting already takes effect.

- **cachePrepStmts**

    Although `useServerPrepStmts=true` allows the server to execute Prepared Statements, by default, the client closes the Prepared Statements after each execution and does not reuse them. This means that the "prepare" operation is not even as efficient as text file execution. To solve this, it is recommended that after setting `useServerPrepStmts=true`, you should also configure `cachePrepStmts=true`. This allows the client to cache Prepared Statements.

    To verify that this setting already takes effect, you can do:

    - Go to TiDB monitoring dashboard and view the request command type through **Query Summary** > **CPS By Instance**.
    - If the number of `COM_STMT_EXECUTE` in the request is far more than the number of `COM_STMT_PREPARE`, it means this setting already takes effect.

    In addition, configuring `useConfigs=maxPerformance` will configure multiple parameters at the same time, including `cachePrepStmts=true`.

- **prepStmtCacheSqlLimit**

    After configuring `cachePrepStmts`, also pay attention to the `prepStmtCacheSqlLimit` configuration (the default value is `256`). This configuration controls the maximum length of the Prepared Statements cached on the client.

    The Prepared Statements that exceed this maximum length will not be cached, so they cannot be reused. In this case, you may consider increasing the value of this configuration depending on the actual SQL length of the application.

    You need to check whether this setting is too small if you:

    - Go to TiDB monitoring dashboard and view the request command type through **Query Summary** > **CPS By Instance**.
    - And find that `cachePrepStmts=true` has been configured, but `COM_STMT_PREPARE` is still mostly equal to `COM_STMT_EXECUTE` and `COM_STMT_CLOSE` exists.

- **prepStmtCacheSize**

    **prepStmtCacheSize** controls the number of cached Prepared Statements (the default value is `25`). If your application requires "preparing" many types of SQL statements and wants to reuse Prepared Statements, you can increase this value.

    To verify that this setting already takes effect, you can do:

    - Go to TiDB monitoring dashboard and view the request command type through **Query Summary** > **CPS By Instance**.
    - If the number of `COM_STMT_EXECUTE` in the request is far more than the number of `COM_STMT_PREPARE`, it means this setting already takes effect.

#### Batch-related parameters

While processing batch writes, it is recommended to configure `rewriteBatchedStatements=true`. After using `addBatch()` or `executeBatch()`, JDBC still sends SQL one by one by default, for example:

```java
pstmt = prepare("INSERT INTO `t` (a) values(?)");
pstmt.setInt(1, 10);
pstmt.addBatch();
pstmt.setInt(1, 11);
pstmt.addBatch();
pstmt.setInt(1, 12);
pstmt.executeBatch();
```

Although `Batch` methods are used, the SQL statements sent to TiDB are still individual `INSERT` statements:

```sql
INSERT INTO `t` (`a`) VALUES(10);
INSERT INTO `t` (`a`) VALUES(11);
INSERT INTO `t` (`a`) VALUES(12);
```

But if you set `rewriteBatchedStatements=true`, the SQL statements sent to TiDB will be a single `INSERT` statement:

```sql
INSERT INTO `t` (`a`) values(10),(11),(12);
```

Note that the rewrite of the `INSERT` statements is to concatenate the values after multiple "values" keywords into a whole SQL statement. If the `INSERT` statements have other differences, they cannot be rewritten, for example:

```sql
INSERT INTO `t` (`a`) VALUES (10) ON DUPLICATE KEY UPDATE `a` = 10;
INSERT INTO `t` (`a`) VALUES (11) ON DUPLICATE KEY UPDATE `a` = 11;
INSERT INTO `t` (`a`) VALUES (12) ON DUPLICATE KEY UPDATE `a` = 12;
```

The above `INSERT` statements cannot be rewritten into one statement. But if you change the three statements into the following ones:

```sql
INSERT INTO `t` (`a`) VALUES (10) ON DUPLICATE KEY UPDATE `a` = VALUES(`a`);
INSERT INTO `t` (`a`) VALUES (11) ON DUPLICATE KEY UPDATE `a` = VALUES(`a`);
INSERT INTO `t` (`a`) VALUES (12) ON DUPLICATE KEY UPDATE `a` = VALUES(`a`);
```

Then they meet the rewrite requirement. The above `INSERT` statements will be rewritten into the following one statement:

```sql
INSERT INTO `t` (`a`) VALUES (10), (11), (12) ON DUPLICATE KEY UPDATE a = VALUES(`a`);
```

If there are three or more updates during the batch update, the SQL statements will be rewritten and sent as multiple queries. This effectively reduces the client-to-server request overhead, but the side effect is that a larger SQL statement is generated. For example:

```sql
UPDATE `t` SET `a` = 10 WHERE `id` = 1; UPDATE `t` SET `a` = 11 WHERE `id` = 2; UPDATE `t` SET `a` = 12 WHERE `id` = 3;
```

In addition, because of a [client bug](https://bugs.mysql.com/bug.php?id=96623), if you want to configure `rewriteBatchedStatements=true` and `useServerPrepStmts=true` during batch update, it is recommended that you also configure the `allowMultiQueries=true` parameter to avoid this bug.

#### Integrate parameters

Through monitoring, you might notice that although the application only performs `INSERT` operations to the TiDB cluster, there are a lot of redundant `SELECT` statements. Usually this happens because JDBC sends some SQL statements to query the settings, for example, `select @@session.transaction_read_only`. These SQL statements are useless for TiDB, so it is recommended that you configure `useConfigs=maxPerformance` to avoid extra overhead.

`useConfigs=maxPerformance` includes a group of configurations. To get the detailed configurations in MySQL Connector/J 8.0 and those in MySQL Connector/J 5.1, see [mysql-connector-j 8.0](https://github.com/mysql/mysql-connector-j/blob/release/8.0/src/main/resources/com/mysql/cj/configurations/maxPerformance.properties) and [mysql-connector-j 5.1](https://github.com/mysql/mysql-connector-j/blob/release/5.1/src/com/mysql/jdbc/configs/maxPerformance.properties) respectively.

After it is configured, you can check the monitoring to see a decreased number of `SELECT` statements.

#### Timeout-related parameters

TiDB provides two MySQL-compatible parameters to control the timeout: [`wait_timeout`](/system-variables.md#wait_timeout) and [`max_execution_time`](/system-variables.md#max_execution_time). These two parameters respectively control the connection idle timeout with the Java application and the timeout of the SQL execution in the connection; that is to say, these parameters control the longest idle time and the longest busy time for the connection between TiDB and the Java application. Since TiDB v5.4, the default value of `wait_timeout` is `28800` seconds, which is 8 hours. For TiDB versions earlier than v5.4, the default value is `0`, which means the timeout is unlimited. The default value of `max_execution_time` is `0`, which means the maximum execution time of a SQL statement is unlimited.

However, in an actual production environment, idle connections and SQL statements with excessively long execution time negatively affect databases and applications. To avoid idle connections and SQL statements that are executed for too long, you can configure these two parameters in your application's connection string. For example, set `sessionVariables=wait_timeout=3600` (1 hour) and `sessionVariables=max_execution_time=300000` (5 minutes).
