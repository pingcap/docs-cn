# Java 使用 TiDB 的最佳实践

本文主要介绍基于 TiDB 开发 Java 应用程序可能需要关注的问题。

## Overview

通常 Java 应用中和数据库相关的常用组件有：

- 网络协议：客户端通过标准 [MySQL 协议](https://dev.mysql.com/doc/internals/en/client-server-protocol.html) 和 TiDB 进行网络交互
- JDBC API & 实现：Java 应用通常使用 [JDBC](https://docs.oracle.com/javase/8/docs/technotes/guides/jdbc/) 来访问数据库， JDBC 定义了访问数据库 API，而 JDBC 实现完成标准 API 到 MySQL 协议的转换，常见的 JDBC 实现是 [MySQL Connector/J](https://github.com/mysql/mysql-connector-j)，此外有些用户可能使用 [MariaDB Connector/J](https://mariadb.com/kb/en/library/about-mariadb-connector-j/#about-mariadb-connectorj)
- 数据库连接池：为了避免每次创建连接，通常应用会选择使用数据库连接池来复用连接，JDBC [DataSource](https://docs.oracle.com/javase/8/docs/api/javax/sql/DataSource.html) 定义了连接池 API，开发者会根据自己选择使用某种开源连接池实现
- 数据访问框架：应用通常选择通过数据访问框架([MyBatis](http://www.mybatis.org/mybatis-3/zh/index.html), [Hibernate](https://hibernate.org/))的封装来进一步简化和管理数据库访问操作
- 业务实现：业务逻辑控制着何时发送和发送什么指令到数据库，其中有些业务会使用 [Spring Transaction](https://docs.spring.io/spring/docs/4.2.x/spring-framework-reference/html/transaction.html) 切面来控制管理事务的开始和提交逻辑

![Java Component](/media/java-practice-1.png)

如上图所示，应用可能使用 Spring Transaction 来管理控制事务非手工启停， 通过类似 MyBatis 的数据访问框架管理生成和执行 SQL，通过连接池获取已池化的长连接，最后通过 JDBC 接口调用实现通过 MySQL 协议和 TiDB 完成交互，接下来我们分别看下各个组件可能需要关注的问题。

## JDBC

Java 应用尽管可能在选择多样的框架封装，但多数情况在最底层会通过调用 JDBC 来向数据库服务器进行交互。对于 JDBC 我们需要关注的主要有：API 的使用选择和 API 实现者参数配置。

### JDBC API

对于基本的 JDBC API 使用可以参考 [JDBC 官方教程](https://docs.oracle.com/javase/tutorial/jdbc/),  这里主要强调几个可能可能响应性能的 API 选择。

#### 推荐使用 Prepare

对于 OLTP 场景， 程序的 SQL 在去除参数变化后都是可穷举的某几类，建议使用 [Prepared Statements](https://docs.oracle.com/javase/tutorial/jdbc/basics/prepared.html) 代替普通的[文本执行](https://docs.oracle.com/javase/tutorial/jdbc/basics/processingsqlstatements.html#executing_queries)并复用 Prepared 直接执行，来避免 TiDB 重复进行 Parse 和 生成 Plan 的开销。

目前多数上层框架都会调用 Prepare API 进行 SQL 执行，如果直接使用 JDBC API 进行开发主要注意选择使用 Prepare API。

另外需要注意 MySQL Connector/J 实现中默认只会做 client prepare， 会将 `?` 在客户端替换后用文本发送到客户端，所以除了使用 Prepare API 后还需要注意需要在 JDBC 连接参数中配置 `useServerPrepStmts = true` 才能让 prepare 在 TiDB 服务器端进行(下面参数配置章节有详细介绍)。

#### 批量插入更新推荐使用 Batch

对于批量插入和更新如果插入批次较大可以选择使用 [addBatch/executeBatch API](https://www.tutorialspoint.com/jdbc/jdbc-batch-processing), 通过 addBatch 的方式让 SQL 在客户端将多条插入更新记录在客户端先缓存， 然后在 executeBatch 时一起发送到数据库服务器。

同样需要注意对于 MySQL Connector/J 实现默认 Batch 只是将多次 addBatch 的 SQL 发送时机延迟到调用 executeBatch 的时候， 但实际网络发送还是会一条条的发送, 通常不会降低和 Server 的网络交互次数，如果希望 Batch 网络发送需要在 JDBC 连接参数中配置 `rewriteBatchedStatements=true` (下面参数配置章节有更详细介绍)。

#### 超大结果集流式获取

默认 JDBC 会提前将查询结果获取并保存在客户端内存中，多数场景下这样能提升执行效率，但在查询返回超大结果集的场景，client 会希望 server 减少向客户端一次返回的记录数，等客户端在有限内存处理完一部分后再去向 server 要下一批。

在 JDBC 中通常有两种处理方式：

- 设置 [FetchSize 为 Integer.MIN_VALUE](https://dev.mysql.com/doc/connector-j/5.1/en/connector-j-reference-implementation-notes.html#ResultSet) 让客户端不缓存，客户端通过 streaming 的方式从网络连接上读取
- 使用 Cursor Fetch 首先需[设置 FetchSize](http://makejavafaster.blogspot.com/2015/06/jdbc-fetch-size-performance.html) 为正整数且在 JDBC URL 中配置 `useCursorFetch=true`

TiDB 中同时支持两种方式，但更推荐使用第一种设置 FetchSize 为 Integer.MIN_VALUE 的方式，相对于第二种功能实现简单且执行效率高。

#### 批量插入后获取自增 ID

向包含自增列的表中批量插入数据后，再通过 `Statement.getGeneratedKeys()` 可以返回插入的自增列的值, 例如表 t 中 id 是自增列：

```java
pstmt = connection.prepareStatement(“insert into t (a) values(?)”, Statement.RETURN_GENERATED_KEYS);
pstmt.setInt(1, 10);
pstmt.addBatch();
pstmt.setInt(1, 11);
pstmt.addBatch();
pstmt.executeBatch();
// 获取自动生成的 id 的值
ResultSet rs = pstmt.getGeneratedKeys();
while (rs.next()) {
    System.out.println(rs.getLong(1));
}
```

### MySQL JDBC Parameter

JDBC 实现通常通过 JDBC URL 参数的形式来提供实现相关的配置， 这里我们以 MySQL 官方的 Connector/J 来看下[参数配置](https://dev.mysql.com/doc/connector-j/5.1/en/connector-j-reference-configuration-properties.html)(如使用的是 MariaDB 可以参考 [MariaDB 的类似配置](https://mariadb.com/kb/en/library/about-mariadb-connector-j/#optional-url-parameters))， 因为配置项较多，这里主要关注几个可能影响到性能的参数。

#### Prepare 相关参数

##### 1. useServerPrepStmts

默认 `useServerPrepStmts` 为 `false`, 默认情况即使使用了 prepare api， 只会在客户端做 “prepare”， 所以为了避免 server 重复 parse 的开销， 建议只要 SQL 能被多运行都建议使用 Prepare API 则建议设置该选项为 true。

在 TiDB 监控中可以通过 “Query Summary” - “QPS by Instance” 查看请求命令类型，如果请求中 `COM_QUERY` 被 `COM_STMT_EXECUTE`/`COM_STMT_PREPARE` 代替即生效。

##### 2. cachePrepStmts

默认 `cachePrepStmts` 也是为 `false`, 默认情况虽然 `useServerPrepStmts=true` 能让 prepare 在 server 端执行，但每次执行完后就会 close prepared 的语句不会复用，在不能复用的情况下 prepare 效率甚至不如文本执行， 所以建议开启 `useServerPrepStmts=true` 后同时配置 `useServerPrepStmts=true`。

在 TiDB 监控中可以通过 “Query Summary” - “QPS by Instance” 查看请求命令类型，如果类似下图，请求中 `COM_STMT_EXECUTE` 数目远远多于 `COM_STMT_PREPARE` 即生效。

![QPS By Instance](/media/java-practice-2.png)

另外， 通过 `useConfigs=maxPerformance` 配置会同时配置多个参数，其中也包括 `cachePrepStmts=true`。

##### 3. prepStmtCacheSqlLimit

在配置后 `cachePrepStmts` 后还需要注意 `prepStmtCacheSqlLimit` 配置(默认 256), 该配置控制能被客户端 Prepare 缓存的最大语句长度。

在一些场景可能会运行 SQL 的长度会超过该配置， 导致 prepared stmt 不能复用，建议根据应用 SQL 长度情况决定是否需要调大该值。

在 TiDB 监控中看到 “Query Summary” - “QPS by Instance” 查看请求命令类型， 如果已经配置了 `cachePrepStmts=true` 但 `COM_STMT_PREPARE` 还是和 `COM_STMT_EXECUTE` 基本相等且有 `COM_STMT_CLOSE` 可以检查下这个配置配置是否过小。

##### 4. prepStmtCacheSize

`prepStmtCacheSize` 控制缓存的 Prepare 语句数目(默认 25)， 如果应用需要 prepare 的 SQL 种类很多且希望复用 Prepare 可以调大该值。

和上一条类似目的是在监控中通过 “Query Summary” - “QPS by Instance” 查看请求中 `COM_STMT_EXECUTE` 数目远远多于 `COM_STMT_PREPARE` 来确认是否正常。

#### Batch 相关参数

在进行 batch 写入处理时推荐配置 `rewriteBatchedStatements=true`， 在已经使用 `addBatch`/`executeBatch` 后默认 JDBC 还是会一条条 SQL 发送， 例如：

```java
pstmt = prepare(“insert into t (a) values(?)”);
pstmt.setInt(1, 10);
pstmt.addBatch();
pstmt.setInt(1, 11);
pstmt.addBatch();
pstmt.setInt(1, 12);
pstmt.executeBatch();
```

虽然使用了 batch 但发送到 TiDB 语句还是单独的多条 insert：

```mysql
insert into t(a) values(10);
insert into t(a) values(11);
insert into t(a) values(12);
```

如果设置 `rewriteBatchedStatements=true` 后发送到 TiDB 的 SQL 将是：

```mysql
insert into t(a) values(10),(11),(12);
```

如果是批量更新如果超过 3 个以上 update 则会改写为 multiple-querys 的进行发送，这样可以有效减少 client 到 server 的请求开销，但副作用是会产生较大的 sql 语句, 例如这样：

```mysql
update t set a = 10 where id = 1; update t set a = 11 where id = 2; update t set a = 12 where id = 3;
```

另外因为一个[客户端 bug](https://bugs.mysql.com/bug.php?id=96623) 如果批量 update 希望同时 `rewriteBatchedStatements=true` 和 `useServerPrepStmts=true` 推荐同时配置 `allowMultiQueries=true` 参数来避免。

#### 执行前检查参数

通过监控可能会发现"虽然业务只向集群进行 insert 操作却看到有很多非 internal 的 select 语句", 通常是因为 JDBC 会在发一些查询设置 SQL(e.g. `select @@session.transaction_read_only` 对 TiDB 无用), 对于 TiDB 推荐配置 `useConfigs=maxPerformance` 来避免开销。

`useConfigs=maxPerformance` 会包含一组配置：

```ini
cacheServerConfiguration=true
useLocalSessionState=true
elideSetAutoCommits=true
alwaysSendSetIsolation=false
enableQueryTimeouts=false
```

配置后查看监控可以看到多余语句减少。

## Connection Pool

TiDB(MySQL) 连接建立是比较昂贵的操作(至少对于 OLTP)， 除了 TCP 建立连接外还需要进行连接鉴权操作， 所以客户端段通常会对 TiDB(MySQL) 连接保存到连接池中进行复用。

Java 的连接池实现很多([HikariCP](https://github.com/brettwooldridge/HikariCP), [tomcat-jdbc](https://tomcat.apache.org/tomcat-7.0-doc/jdbc-pool.html), [durid](https://github.com/alibaba/druid), [c3p0](https://www.mchange.com/projects/c3p0/), [dbcp](https://commons.apache.org/proper/commons-dbcp/)), TiDB 不会限定使用的连接池， 应用可以根据根据业务特点自己选择连接池实现。

### 连接数配置

比较常见的是应用需要根据自身情况配置合适的连接池大小，以 HikariCP 为例：

- `maximumPoolSize`：连接池最大连接数，配置过大会导致 TiDB 消耗资源维护无用连接，配置过小则会导致应用获取连接变慢, 所以需根据应用自身特点配置合适的值, 可以看下[这篇文章](https://github.com/brettwooldridge/HikariCP/wiki/About-Pool-Sizing)
- `minimumIdle`：连接池最大空闲连接数，主要用于在应用空闲时存留一些连接以应对突发请求，同样是需要根据业务请情况配置。

应用在使用连接池同样需要注意连接使用完成后归还连接，推荐应用对应连接池相关监控(e.g. `metricRegistry`)，通过监控能及时定位连接池大小问题。

### 探活配置

连接池维护长连接到 TiDB， TiDB 默认不会主动关闭客户端连接(除非报错)，但一般客户端到 TiDB 之间还会有 LVS 或 haproxy 之类的网络代理通常会在一定空闲后主动在 proxy 上清理连接，所以除了注意 proxy idle 配置外，连接池需要进行保活或探测连接。

如果我们常在 java 应用中看到这个错误

```
The last packet sent successfully to the server was 3600000 milliseconds ago. The driver has not received any packets from the server. com.mysql.jdbc.exceptions.jdbc4.CommunicationsException: Communications link failure
```

如果 `n milliseconds ago` 中的 `n` 如果是 0 或很小的值，则通常是执行的 SQL 导致 TiDB 异常退出引起的报错，推荐查看 TiDB stderr 日志; 如果 n 是一个非常大的值(比如这里的 3600000) 非常大概率是因为这个连接很久没人用到然后被中间 proxy 给关闭了， 通常解决方式除了调大 proxy idle 配置还可以让连接池：

- 每次使用连接前检查连接是否可用
- 单独线程定期检查连接是否可用
- 定期发送 test query 保活连接

不同的连接池实现可能会支持其中一种或多种方式，可以查看所使用的连接池文档来寻找对应配置。

## Data Access Framework

业务应用通常会使用某种数据访问框架来简化数据库的访问。

### MyBatis

[http://www.mybatis.org/mybatis-3/](http://www.mybatis.org/mybatis-3/)

MyBatis 是目前比较流行的 Java 数据访问框架, 主要用于管理 SQL 并完成结果集和 Java 对象的来回映射工作和 TiDB 兼容性很好从历史 issue 看很少有 mybatis 问题, 不过有几个配置可能需要关注：

#### Parameters

MyBatis 的 Mapper 中支持 2 种 Parameters：

- `select 1 from t where id = #{param1}` 会作为 prepare 转换为 `select 1 from t where id = ?` 进行 prepare， 并将用实际参数去复用执行, 通过配合前面的 Prepare 连接参数能获得最佳性能
- `select 1 from t where id = ${param2}` 会做文本替换为 `select 1 from t where id = 1` 执行，如果这条语句被 prepare 不同参数可能会导致大量的 prepare 语句在 TiDB 被cache，并且这种方式执行 SQL 有注入安全风险

#### Dynamic SQL Batch

[http://www.mybatis.org/mybatis-3/dynamic-sql.html#foreach](http://www.mybatis.org/mybatis-3/dynamic-sql.html#foreach)

除了前面 JDBC 配置 `rewriteBatchedStatements=true` 后支持自动将一个个执行的 insert 重写为 `insert values` 后跟很多 value 的外，mybatis 也可以使用 mybatis 的 dynamic 来半自动生成 batch insert 比如下面的 mapper:

```xml
<insert id="insertTestBatch" parameterType="java.util.List" fetchSize="1">
  insert into test
   (id, v1, v2)
  values
  <foreach item="item" index="index" collection="list" separator=",">
  (
   #{item.id}, #{item.v1}, #{item.v2}
  )
  </foreach>
  on duplicate key update v2 = v1 + values(v1)
</insert>
```

会生成一个 `insert on duplicate key update` 语句 values 后面的 `(?, ?, ?)` 数目是根据传入的 list 个数决定，最终效果和使用 `rewriteBatchStatements=true` 类似, 可以有效减少客户端和 TiDB 的网络交互次数，同样需要注意 prepare 后超过 `prepStmtCacheSqlLimit` 限制导致不被缓存频繁 prepare 的问题。

#### Streaming Result

前面介绍了在 JDBC 中如何使用流式读取结果，除了 JDBC 相应的配置外在 MyBatis 中如果希望读取超大结果集合也需要注意：

- 可以通过在 mapper 配置中对单独一条 sql 设置 `fetchSize`(见上一段代码段)， 效果等同于调用 JDBC `setFetchSize`
- 可以使用带 `ResultHandler` 的查询接口来避免一次获取整个结果 List
- 可以使用 `Cursor` 类来进行流式读取

### ExecutorType

在 `openSession` 的时候可以选择 `ExecutorType`， MyBatis 支持三种 executor：

- Simple：每次执行都会向 JDBC 进行 prepare 调用(重复的 prepare 调用如果 JDBC 配置有开启 `cachePrepStmts` 也会复用)
- Reuse：在 `executor` 中缓存 statement， 这样不用 JDBC 的 `cachePrepStmts` 也能减少重复 prepare 调用
- Batch：每次更新只会 `addBatch` 直到 query 或 commit 才会调用 `executeBatch` 执行, 如果 jdbc 层有开 `rewriteBatchStatements` 会尝试改写，没有则一条条发送

通常默认值是 Simple 且没有配置可以修改，除非主动在调用 openSession 代码时改变 executorType，如果是 Batch 会遇到情况是事务中前面的 update insert 都非常快，当遇到读或 commit 时因为实际将之前代码执行从客户端看会比较慢实际正常，但排查定位慢 SQL 时需注意。

## Spring Transaction

在应用代码中业务可能会通过使用 [Spring Transaction](https://docs.spring.io/spring/docs/4.2.x/spring-framework-reference/html/transaction.html) 来并通过 AOP 切面的方式来启停事务。

通过在方法定义上添加 @Transactional 注解标记方法，AOP 将会在方法前开启事务， 方法 return 前 commit 事务， 如果遇到类似业务可以通过查找代码 @Transactional  来确定事开启和关闭范围, 需要特别注意有内嵌的情况, 如果发生内嵌 Spring 会根据 [Propagation](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/transaction/annotation/Propagation.html) 配置使用不同的行为，因为 TiDB 未支持 savepoint 所以需要注意 NESTED 嵌套事务不支持使用。

## Misc

### Troubleshooting Tool

在 Java 应用发生问题希望进程排查在短期不知道业务逻辑情况下使用 JVM 强大的排查工具会比较有用， 这里简单介绍几个常用工具：

#### jstack

[https://docs.oracle.com/javase/7/docs/technotes/tools/share/jstack.html](https://docs.oracle.com/javase/7/docs/technotes/tools/share/jstack.html)

对应于 Go 中的 pprof/goroutine, 可以比较方便的解决卡死问题

使用方法是 `jstack pid` 即可会输出进程中所有线程的堆栈信息和线程 id 到标准输出，默认只有 java 堆栈如果希望将 jvm 中 c++ 堆栈打印可以加 `-m`

通过多次 jstack 可以方便发现卡死问题(比如：都通过 Mybatis BatchExecutor flush 调用 update) 或死锁问题(比如：测试程序都在抢占应用中某把 lock 没发 SQL)

另外，比较常用是 `top -p $PID -H` 或者 java swiss knife 可以看到线程 ID, 通过一个转换为 16 进制(`printf "%x\n" pid`) 后去 jstack 中找对应线程的栈信息来定位”某个线程 cpu 比较高不知道做什么”的问题

#### jmap & mat

[https://docs.oracle.com/javase/7/docs/technotes/tools/share/jmap.html](https://docs.oracle.com/javase/7/docs/technotes/tools/share/jmap.html)
[https://www.eclipse.org/mat/](https://www.eclipse.org/mat/)

和 Go 中的 pprof/heap 不同 jmap 会将整个进程的内存快照 dump 下来(go 是分配器的采样), 然后可以通过另一个工具 mat 做分析。

因为是快照通过 mat 可以看到进程中所有对象的关联信息和属性通常通过 mat 可以很好的观察运行中程序的状态， 比如：我们可以通过 mat 找到当前应用中有多少 mysql 连接对象，每个连接对象的地址和状态信息是什么，在有些情况下有用；需要注意 mat 默认只会处理 reachable objects，如果排查 young gc 问题可以在软件配置中设置查看 unreachable，另外对于调查 young gc 问题（或者大量生命周期较短的对象）的内存分配用 Java Flight Recorder 比较方便。

#### trace

最后在无法修改在线代码的情况下希望在 java 中做动态插桩定位问题通常会推荐使用 btrace 或 arthas trace, 可以在不重启进程的情况下动态插入 trace 代码。

#### flamegraph

Java 中获取火焰图稍微繁琐可以通过[这样](http://psy-lob-saw.blogspot.com/2017/02/flamegraphs-intro-fire-for-everyone.html)手工获取

## 总结

本文我们从常用和数据库交互的 Java 组件使用角度看了下在基于 TiDB 开发 Java 应用时需要注意的常见问题， TiDB 是高度兼容 MySQL 协议的数据库，通常基于 MySQL 开发 Java 应用的最佳实践也多适用于 TiDB， 欢迎大家通过 [ASKTUG](https://asktug.com/) 和我们分享讨论自己 Java 编写 TiDB 应用时发现的其他实践技巧或遇到的问题。
