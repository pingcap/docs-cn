---
title: TiSpark 用户指南
summary: 使用 TiSpark 一站式解决用户的 HTAP 需求。
aliases: ['/docs-cn/dev/tispark-overview/','/docs-cn/dev/reference/tispark/','/zh/tidb/dev/get-started-with-tispark/','/docs-cn/dev/get-started-with-tispark/','/docs-cn/dev/how-to/get-started/tispark/']
---

# TiSpark 用户指南

![TiSpark 架构](/media/tispark-architecture.png)

## TiSpark vs TiFlash

[TiSpark](https://github.com/pingcap/tispark) 是 PingCAP 为解决用户复杂 OLAP 需求而推出的产品。它借助 Spark 平台，同时融合 TiKV 分布式集群的优势，和 TiDB 一起为用户一站式解决 HTAP (Hybrid Transactional/Analytical Processing) 的需求。

[TiFlash](/tiflash/tiflash-overview.md) 也是一个解决 HTAP 需求的产品。TiFlash 和 TiSpark 都允许使用多个主机在 OLTP 数据上执行 OLAP 查询。TiFlash 是列式存储，这提供了更高效的分析查询。TiFlash 和 TiSpark 可以同时使用。

## TiSpark 是什么

TiSpark 依赖于 TiKV 集群和 Placement Driver (PD)，也需要你搭建一个 Spark 集群。本文简单介绍如何部署和使用 TiSpark。本文假设你对 Spark 有基本认知。你可以参阅 [Apache Spark 官网](https://spark.apache.org/docs/latest/index.html)了解 Spark 的相关信息。

TiSpark 深度整合了 Spark Catalyst 引擎，可以对计算进行精确的控制，使 Spark 能够高效地读取 TiKV 中的数据。TiSpark 还提供索引支持，帮助实现高速点查。

TiSpark 通过将计算下推到 TiKV 中提升了数据查询的效率，减少了 Spark SQL 需要处理的数据量，通过 TiDB 内置的统计信息选择最优的查询计划。

TiSpark 和 TiDB 可以让用户无需创建和维护 ETL，直接在同一个平台上进行事务和分析两种任务。这简化了系统架构，降低了运维成本。

用户可以在 TiDB 上使用 Spark 生态圈的多种工具进行数据处理，例如：

- TiSpark：数据分析和 ETL。
- TiKV：数据检索。
- 调度系统：生成报表。

除此之外，TiSpark 还提供了分布式写入 TiKV 的功能。与使用 Spark 结合 JDBC 写入 TiDB 的方式相比，分布式写入 TiKV 能够实现事务（要么全部数据写入成功，要么全部都写入失败）。

> **警告：**
>
> 由于 TiSpark 直接访问 TiKV，所以 TiDB Server 使用的访问控制机制并不适用于 TiSpark。TiSpark v2.5.0 及以上版本实现了部分鉴权与授权功能，具体信息请参考[安全](/tispark-overview.md#安全)。

## 版本要求

- TiSpark 支持 Spark 2.3 或以上版本。
- TiSpark 需要 JDK 1.8 以及 Scala 2.11/2.12 版本。
- TiSpark 可以运行在任何 Spark 模式上，如 `YARN`、`Mesos` 以及 `Standalone`。

## 推荐配置

> **警告：**
>
> [此文](/tispark-deployment-topology.md)所描述的使用 TiUP 部署 TiSpark 的方式已被废弃。

TiSpark 作为 Spark 的 TiDB 连接器，需要 Spark 集群的支持。本文仅提供部署 Spark 的参考建议，对于硬件以及部署细节，请参考 [Spark 官方文档](https://spark.apache.org/docs/latest/hardware-provisioning.html)。

对于独立部署的 Spark 集群，可以参考如下建议配置：

- 建议为 Spark 分配 32G 以上的内存，并为操作系统和缓存保留至少 25% 的内存。
- 建议每台机器至少为 Spark 分配 8 到 16 核 CPU。起初，你可以设定将所有 CPU 核分配给 Spark。

可以参考如下的 spark-env.sh 配置文件：

```
SPARK_EXECUTOR_MEMORY = 32g
SPARK_WORKER_MEMORY = 32g
SPARK_WORKER_CORES = 8
```

## 获取 TiSpark

TiSpark 是 Spark 的第三方 jar 包，提供读写 TiKV 的能力。

### 获取 mysql-connector-j

由于 GPL 许可证的限制，TiSpark 不再提供 `mysql-connector-java` 的依赖。以下版本将不再包含 `mysql-connector-java`：

- TiSpark > 3.0.1
- TiSpark > 2.5.1 (TiSpark 2.5.x)
- TiSpark > 2.4.3 (TiSpark 2.4.x)

在使用 TiSpark 写入与鉴权时，仍需要 `mysql-connector-java` 依赖，因此你需要手动下载，并使用以下方式引入：

- 将 `mysql-connector-java` 放入 Spark jars 包中。
- 在你提交 Spark 任务时，引入 `mysql-connector-java`，详见以下示例:

  ```
  spark-submit --jars tispark-assembly-3.0_2.12-3.1.0-SNAPSHOT.jar,mysql-connector-java-8.0.29.jar
  ```

### 选择 TiSpark 版本

你可以根据 TiDB 和 Spark 版本选择相应的 TiSpark 版本。

| TiSpark 版本       | TiDB、TiKV、PD 版本 | Spark 版本                   | Scala 版本 |
|------------------|-----------------|----------------------------|----------|
| 2.4.x-scala_2.11 | 5.x, 4.x        | 2.3.x, 2.4.x               | 2.11     |
| 2.4.x-scala_2.12 | 5.x, 4.x        | 2.4.x                      | 2.12     |
| 2.5.x            | 5.x, 4.x        | 3.0.x, 3.1.x               | 2.12     |
| 3.0.x            | 5.x, 4.x        | 3.0.x, 3.1.x, 3.2.x        | 2.12     |
| 3.1.x            | 6.x, 5.x, 4.x   | 3.0.x, 3.1.x, 3.2.x, 3.3.x | 2.12     |
| 3.2.x            | 6.x, 5.x, 4.x   | 3.0.x, 3.1.x, 3.2.x, 3.3.x | 2.12     |

推荐使用 TiSpark 的最新稳定版本，包括 2.4.4、2.5.2、3.0.2、3.1.1 和 3.2.3。

> **Note:**
>
> TiSpark 不保证与 TiDB v7.0.0 及之后版本兼容。

## 获取 TiSpark jar 包

你能用以下方式获取 jar 包：

- 从 [maven 中央仓库](https://search.maven.org/)获取，你可以搜索 [`pingcap`](http://search.maven.org/#search%7Cga%7C1%7Cpingcap) 关键词。
- 从 [TiSpark releases](https://github.com/pingcap/tispark/releases) 获取。
- 通过以下步骤从源码构建：

1. 下载 TiSpark 源码：

    ```
    git clone https://github.com/pingcap/tispark.git
    cd tisapark
    ```

2. 在 TiSpark 根目录运行如下命令：

    ```
    // add -Dmaven.test.skip=true to skip the tests
    mvn clean install -Dmaven.test.skip=true
    // or you can add properties to specify spark version
    mvn clean install -Dmaven.test.skip=true -Pspark3.2.1
    ```

> **注意：**
>
> 目前，你只能使用 java8 构架 TiSpark。运行 `mvn -version` 来检查 java 版本。

### TiSpark jar 包的 artifact ID

注意不同版本的 TiSpark artifact ID 也不同：

| TiSpark 版本                     | Artifact ID                                        |
|--------------------------------| -------------------------------------------------- |
| 2.4.x-\${scala_version}, 2.5.0 | tispark-assembly                                   |
| 2.5.1                          | tispark-assembly-\${spark_version}                  |
| 3.0.x, 3.1.x, 3.2.x            | tispark-assembly-\${spark_version}-\${scala_version} |

## 快速开始

本章节将以 spark-shell 为例，介绍如何使用 TiSpark。请保证您已下载 Spark。

### 启动 spark-shell

在 `spark-defaults.conf` 中添加如下配置：

```
spark.sql.extensions  org.apache.spark.sql.TiExtensions
spark.tispark.pd.addresses  ${your_pd_address}
spark.sql.catalog.tidb_catalog  org.apache.spark.sql.catalyst.catalog.TiCatalog
spark.sql.catalog.tidb_catalog.pd.addresses  ${your_pd_address}
```

启动 spark-shell：

```
spark-shell --jars tispark-assembly-{version}.jar
```

### 获取 TiSpark 版本

在 spark-shell 中运行如下命令，可获取 TiSpark 版本信息：

```scala
spark.sql("select ti_version()").collect
```

### 使用 TiSpark 读取数据

可以通过 Spark SQL 从 TiKV 读取数据：

```scala
spark.sql("use tidb_catalog")
spark.sql("select count(*) from ${database}.${table}").show
```

### 使用 TiSpark 写入数据

通过 Spark DataSource API，可以在保证 ACID 前提下写入数据到 TiKV：

```scala
val tidbOptions: Map[String, String] = Map(
  "tidb.addr" -> "127.0.0.1",
  "tidb.password" -> "",
  "tidb.port" -> "4000",
  "tidb.user" -> "root"
)

val customerDF = spark.sql("select * from customer limit 100000")

customerDF.write
.format("tidb")
.option("database", "tpch_test")
.option("table", "cust_test_select")
.options(tidbOptions)
.mode("append")
.save()
```

详见 [Data Source API User Guide](https://github.com/pingcap/tispark/blob/master/docs/features/datasource_api_userguide.md)。

在 TiSpark 3.1 之后，你还能通过 Spark SQL 写入数据到 TiSpark。详见 [Insert SQL](https://github.com/pingcap/tispark/blob/master/docs/features/insert_sql_userguide.md)。

### 通过 JDBC 数据源写入数据

你同样可以在不使用 TiSpark 的情况下使用 Spark JDBC 数据源写入 TiDB。

由于这超过了 TiSpark 的范畴，本文仅简单提供示例，详情请参考 [JDBC To Other Databases](https://spark.apache.org/docs/latest/sql-data-sources-jdbc.html)。

```scala
import org.apache.spark.sql.execution.datasources.jdbc.JDBCOptions

val customer = spark.sql("select * from customer limit 100000")
// 为了平衡各节点以及提高并发数，你可以将数据源重新分区
val df = customer.repartition(32)
df.write
.mode(saveMode = "append")
.format("jdbc")
.option("driver", "com.mysql.jdbc.Driver")
// 替换为你的主机名和端口地址，并确保开启了重写批处理
.option("url", "jdbc:mysql://127.0.0.1:4000/test?rewriteBatchedStatements=true")
.option("useSSL", "false")
// 作为测试，建议设置为 150
.option(JDBCOptions.JDBC_BATCH_INSERT_SIZE, 150)
.option("dbtable", s"cust_test_select") // 数据库名和表名
.option("isolationLevel", "NONE") // 如果需要写入较大 Dataframe，推荐将 isolationLevel 设置为 NONE
.option("user", "root") // TiDB 用户名
.save()
```

为了避免大事务导致 OOM 以及 TiDB 报 `ISOLATION LEVEL does not support` 错误（TiDB 目前仅支持 `REPEATABLE-READ`)，推荐设置 `isolationLevel` 为 `NONE`。

### 使用 TiSpark 删除数据

可以使用 Spark SQL 删除 TiKV 数据：

```
spark.sql("use tidb_catalog")
spark.sql("delete from ${database}.${table} where xxx")
```

详情请参考 [delete feature](https://github.com/pingcap/tispark/blob/master/docs/features/delete_userguide.md)。

### 与其他数据源一起使用

你可以使用多个 catalog 从不同数据源读取数据：

```
// 从 Hive 读取
spark.sql("select * from spark_catalog.default.t").show

// Join Hive 表和 TiDB 表
spark.sql("select t1.id,t2.id from spark_catalog.default.t t1 left join tidb_catalog.test.t t2").show
```

## TiSpark 配置

可以将如下参数配置在 `spark-defaults.conf` 中，也可以参考 Spark 其他配置，用同样的方式传入。

| Key                                             | Default value    | Description                                                                                                                                                                                                                                                                            |
|-------------------------------------------------|------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `spark.tispark.pd.addresses`                    | `127.0.0.1:2379` | PD 集群的地址，通过逗号分隔。                                                                                                                                                                                                                                                                       |
| `spark.tispark.grpc.framesize`                  | `2147483647`     | gRPC 的最大回复大小，单位 bytes（默认 2G）。                                                                                                                                                                                                                                                          |
| `spark.tispark.grpc.timeout_in_sec`             | `10`             | gRPC 超时时间，单位秒。                                                                                                                                                                                                                                                                         |
| `spark.tispark.plan.allow_agg_pushdown`         | `true`           | 是否运行聚合下推（为了避免 TiKV 节点繁忙）。                                                                                                                                                                                                                                                              |
| `spark.tispark.plan.allow_index_read`           | `true`           | 是否在执行计划中开启 index（可能导致 TiKV 压力过大）。                                                                                                                                                                                                                                                      |
| `spark.tispark.index.scan_batch_size`           | `20000`          | 在 index scan 的一次 batch 中 row keys 的数量。                                                                                                                                                                                                                                                 |
| `spark.tispark.index.scan_concurrency`          | `5`              | 在 index scan 中获取 row keys 的最大线程数（每个 JVM 的所有任务共享）。                                                                                                                                                                                                                                      |
| `spark.tispark.table.scan_concurrency`          | `512`            | 在 table scan 中的最大线程数（每个 JVM 的所有任务共享）。                                                                                                                                                                                                                                                  |
| `spark.tispark.request.command.priority`        | `Low`            | 可选项有 `Low`、`Normal`和`High`。修改配置会影响影响 TiKV 的资源分配。建议使用 `Low`，因为 OLTP 的负载不会被影响。                                                                                                                                                                                                           |
| `spark.tispark.coprocess.codec_format`          | `chblock`        | Coprocessor 的编码格式。可选项为 `default`、`chblock` 和 `chunk`。                                                                                                                                                                                                                                  |
| `spark.tispark.coprocess.streaming`             | `false`          | 是否在获取响应时使用 streaming（实验性质）。                                                                                                                                                                                                                                                            |
| `spark.tispark.plan.unsupported_pushdown_exprs` |                  | 表达式清单，多个表达式用逗号分隔。为了防止老版本的 TiKV 不支持某些表达式，你可以禁止下推它们。                                                                                                                                                                                                                                     |
| `spark.tispark.plan.downgrade.index_threshold`  | `1000000000`     | 如果 index scan 请求的范围超过了此限制，该 Region 请求会被降级为 table scan。降级默认关闭。                                                                                                                                                                                                                         |
| `spark.tispark.show_rowid`                      | `false`          | 是否在 row_id 存在时显示它。                                                                                                                                                                                                                                                                     |
| `spark.tispark.db_prefix`                       |                  | TiDB数据库的前缀。该配置可用于在 TiSpark 2.4 中区分同名的 TiDB 和 Hive 数据库。                                                                                                                                                                                                                                 |
| `spark.tispark.request.isolation.level`         | `SI`             | 是否为底层的 TiKV 解锁。当你使用 "RC" 级别，你将忽略锁，得到比 `tso` 更小的最新版本数据。当你使用 "SI" 级别，你将进行解锁并根据该锁对应的事务提交与否获取数据。                                                                                                                                                                                         |
| `spark.tispark.coprocessor.chunk_batch_size`    | `1024`           | 从 coprocessor 获取的一个 batch 的 Row 数量。                                                                                                                                                                                                                                                    |
| `spark.tispark.isolation_read_engines`          | `tikv,tiflash`   | TiSpark 读引擎，多个引擎使用逗号分隔。未配置的存储引擎不会被读取。                                                                                                                                                                                                                                                  |
| `spark.tispark.stale_read`                      | optional         | stale read 时间戳。详情请参考 [stale read](https://github.com/pingcap/tispark/blob/master/docs/features/stale_read.md)。                                                                                                                                                                        |
| `spark.tispark.tikv.tls_enable`                 | `false`          | 是否开启 TiSpark TLS。                                                                                                                                                                                                                                                                      |
| `spark.tispark.tikv.trust_cert_collection`      |                  | TiKV Client 的受信任根证书，用于验证 PD 证书。如 `/home/tispark/config/root.pem`，该文件需包含 X.509 证书。                                                                                                                                                                                                     |
| `spark.tispark.tikv.key_cert_chain`             |                  | TiKV Client 的 X.509 格式的客户端证书链。如 `/home/tispark/config/client.pem`。                                                                                                                                                                                                                     |
| `spark.tispark.tikv.key_file`                   |                  | TiKV Client 的 PKCS#8 私钥文件。如 `/home/tispark/client_pkcs8.key`。                                                                                                                                                                                                                          |
| `spark.tispark.tikv.jks_enable`                 | `false`          | 是否使用 `JAVA key store` 而不是 X.509 证书。                                                                                                                                                                                                                                                    |
| `spark.tispark.tikv.jks_trust_path`             |                  | TiKV Client JKS 格式的受信任根证书。由 `keytool` 生成，如 `/home/tispark/config/tikv-truststore`。                                                                                                                                                                                                   |
| `spark.tispark.tikv.jks_trust_password`         |                  | `spark.tispark.tikv.jks_trust_path` 的密码。                                                                                                                                                                                                                                               |
| `spark.tispark.tikv.jks_key_path`               |                  | TiKV Client JKS 格式的客户端证书。由 `keytool` 生成，如 `/home/tispark/config/tikv-clientstore`。                                                                                                                                                                                                   |
| `spark.tispark.tikv.jks_key_password`           |                  | `spark.tispark.tikv.jks_key_path` 的密码。                                                                                                                                                                                                                                                 |
| `spark.tispark.jdbc.tls_enable`                 | `false`          | 是否开启 JDBC connector TLS。                                                                                                                                                                                                                                                               |
| `spark.tispark.jdbc.server_cert_store`          |                  | JDBC 的受信任根证书。由 `keytool` 生产的 Java keystore (JKS) 格式的证书。如 `/home/tispark/config/jdbc-truststore`。默认值为 ""，表示 TiSpark 不会校验 TiDB 服务端。                                                                                                                                                  |
| `spark.tispark.jdbc.server_cert_password`       |                  | `spark.tispark.jdbc.server_cert_store` 的密码。                                                                                                                                                                                                                                            |
| `spark.tispark.jdbc.client_cert_store`          |                  | JDBC 的 PKCS#12 格式的客户端证书。这是由 `keytool` 生成的 JKS 格式证书。如 `/home/tispark/config/jdbc-clientstore`。默认值为 ""，表示 TiDB 不会校验 TiSpark。                                                                                                                                                          |
| `spark.tispark.jdbc.client_cert_password`       |                  | `spark.tispark.jdbc.client_cert_store` 的密码。                                                                                                                                                                                                                                             |
| `spark.tispark.tikv.tls_reload_interval`        | `10s`            | 重载证书的时间间隔。默认值为 `10s`。                                                                                                                                                                                                                                                                 |
| `spark.tispark.tikv.conn_recycle_time`          | `60s`            | 清理 TiKV 失效连接的时间间隔。默认时间为 `60s`。当重载证书开启时此配置才会生效。                                                                                                                                                                                                                                         |
| `spark.tispark.host_mapping`                    |                  | 路由映射配置。用于配置公有 IP 地址和私有 IP 地址的映射。当 TiDB 在私有网络上运行时，你可以将一系列内部 IP 地址映射到公网 IP 地址以便 Spark 集群访问。其格式为 `{Intranet IP1}:{Public IP1};{Intranet IP2}:{Public IP2}`，例如 `192.168.0.2:8.8.8.8;192.168.0.3:9.9.9.9`。                                                                                  |
| `spark.tispark.new_collation_enable`            |                  | 当 TiDB 开启 [new collation](https://docs.pingcap.com/tidb/stable/character-set-and-collation#new-framework-for-collations)，推荐将此配置设为`true`。当 TiDB 关闭 `new collation`，推荐将此配置设置为 `false`。在未配置的情况下，TiSpark 会依据 TiDB 版本自动配置 `new collation`。其规则为：当 TiDB 版本大于等于 v6.0.0 时为 `true`；否则为 `false`。 |
| `spark.tispark.replica_read`                   | `leader`         | 读取副本的类型。可选值为 `leader`、`follower`、`learner`。可以同时指定多个类型，TiSpark 会根据顺序选择。  |
| `spark.tispark.replica_read.label`             |                  | 目标 TiKV 节点的标签。格式为 `label_x=value_x,label_y=value_y`，各项之间为“逻辑与”的关系。 |

### TLS 配置

TiSpark TLS 分为两部分：TiKV Client TLS 以及 JDBC connector TLS。 前者用于创建和 TiKV/PD 的 TLS 连接，后者用于创建与 TiDB 的 TLS 连接。

当配置 TiKV Client TLS 时，你需要以 X.509 格式的证书配置 `tikv.trust_cert_collection`、`tikv.key_cert_chain` 和 `tikv.key_file`；或者以 JKS 格式的证书配置 `tikv.jks_enable`，`tikv.jks_trust_path` 和 `tikv.jks_key_path`。

当配置 JDBC connector TLS 时，你需要配置 `spark.tispark.jdbc.tls_enable`，而 `jdbc.server_cert_store` 和 `jdbc.client_cert_store` 则是可选的。

TiSpark 目前仅持 TLS 1.2 and TLS 1.3。

* 如下是使用 X.509 证书配置 TiKV Client TLS 的例子：

```
spark.tispark.tikv.tls_enable                                  true
spark.tispark.tikv.trust_cert_collection                       /home/tispark/root.pem
spark.tispark.tikv.key_cert_chain                              /home/tispark/client.pem
spark.tispark.tikv.key_file                                    /home/tispark/client.key
```

* 如下是使用 JKS 配置 TiKV Client TLS 的例子：

```
spark.tispark.tikv.tls_enable                                  true
spark.tispark.tikv.jks_enable                                  true
spark.tispark.tikv.jks_key_path                                /home/tispark/config/tikv-truststore
spark.tispark.tikv.jks_key_password                            tikv_trustore_password
spark.tispark.tikv.jks_trust_path                              /home/tispark/config/tikv-clientstore
spark.tispark.tikv.jks_trust_password                          tikv_clientstore_password
```

当你同时配置 JKS 和 X.509 证书时，JKS 优先级更高。因此，当你只想使用普通的 pem 证书时，不要同时设置 `spark.tispark.tikv.jks_enable=true`。

* 下面是一个配置 JDBC connector TLS 的例子：

```
spark.tispark.jdbc.tls_enable                                  true
spark.tispark.jdbc.server_cert_store                           /home/tispark/jdbc-truststore
spark.tispark.jdbc.server_cert_password                        jdbc_truststore_password
spark.tispark.jdbc.client_cert_store                           /home/tispark/jdbc-clientstore
spark.tispark.jdbc.client_cert_password                        jdbc_clientstore_password
```

- 对于如何开启 TiDB TLS，请参考 [Enable TLS between TiDB Clients and Servers](/enable-tls-between-clients-and-servers.md)。
- 对于如何生成 JAVA key store，请参考 [Connecting Securely Using SSL](https://dev.mysql.com/doc/connector-j/en/connector-j-reference-using-ssl.html)。

### 时区配置

使用 `-Duser.timezone` 系统参数来配置时区（比如 `-Duser.timezone=GMT-7`）。时区会影响 `Timestamp` 数据类型。

请不要使用 `spark.sql.session.timeZone`。

## 特性

TiSpark 的主要特性如下：

| 特性支持                            | TiSpark 2.4.x | TiSpark 2.5.x | TiSpark 3.0.x | TiSpark 3.1.x |
|---------------------------------| ------------- | ------------- | ----------- |---------------|
| SQL select without tidb_catalog | ✔           | ✔           |             |               |
| SQL select with tidb_catalog    |               | ✔           | ✔         | ✔             |
| DataFrame append                | ✔           | ✔           | ✔         | ✔             |
| DataFrame reads                 | ✔           | ✔           | ✔         | ✔             |
| SQL show databases              | ✔           | ✔           | ✔         | ✔             |
| SQL show tables                 | ✔           | ✔           | ✔         | ✔             |
| SQL auth                        |               | ✔           | ✔         | ✔             |
| SQL delete                      |               |               | ✔         | ✔             |
| SQL insert                      |               |               |           | ✔              |
| TLS                             |               |               | ✔         | ✔             |
| DataFrame auth                  |               |               |             | ✔             |

### Expression index 支持

TiDB v5.0 开始支持 [expression index](/sql-statements/sql-statement-create-index.md#表达式索引)。

TiSpark 目前支持从 `expression index` 的表中获取数据，但 `expression index` 不会被 TiSpark 执行计划使用。

### TiFlash 支持

TiSpark 能够通过配置 `spark.tispark.isolation_read_engines` 从 TiFlash 读取数据。

### 分区表支持

**读分区表**

TiSpark 目前支持读取 range 与 hash 分区表。

TiSpark 目前不支持 `partition table` 语法 `select col_name from table_name partition(partition_name)`。但是，你仍可以使用 `where` 条件过滤分区。

TiSpark 会根据分区类型、分区表达式以及具体 SQL 决定是否进行分区裁剪。目前，TiSpark 仅支持在 range 分区下，且在下列任一条件下进行分区裁剪：

+ 列表达式，如 `partition by col1`。
+ 形如 `YEAR($col)` 的 year 函数，其中 col 为列名且类型为 datetime、date 或能被解析为 datetime、date 的 string 字面量。
+ 形如 `TO_DAYS($col)` 的 to_days 函数，其中 col 为列名且类型为 datetime、date 或能被解析为 datetime、date 的 string 字面量。

如果分区裁剪未被应用，TiSpark 将会读取所有分区表。

**写分区表**

目前, TiSpark 仅支持写入 range 与 hash 分区表，且需满足以下任一条件：

+ 列表达式，如 `partition by col1`。
+ 形如 `YEAR($col)` 的 year 函数，其中 col 为列名且类型为 datetime、date 或能被解析为 datetime、date 的 string 字面量。

> **注意：**
>
> 目前，TiSpark 只支持在 utf8mb4_bin 字符集下写入分区表。

有两种方式写入分区表：

+ 使用支持 replace 和 append 语义的 Datasource API 写入分区表。
+ 使用 Spark SQL 删除语句。

### 安全

从 TiSpark v2.5.0 起，你可以通过 TiDB 对 TiSpark 进行鉴权与授权。

该功能默认关闭。要开启该功能，请在 Spark 配置文件 `spark-defaults.conf` 中添加以下配置项：

```
// 开启鉴权与授权功能
spark.sql.auth.enable true

// 配置 TiDB 信息
spark.sql.tidb.addr $your_tidb_server_address
spark.sql.tidb.port $your_tidb_server_port
spark.sql.tidb.user $your_tidb_server_user
spark.sql.tidb.password $your_tidb_server_password
```

更多详细信息，请参考 [TiSpark 鉴权与授权指南](https://github.com/pingcap/tispark/blob/master/docs/features/authorization_userguide.md)。

### 其他特性

- [下推](https://github.com/pingcap/tispark/blob/master/docs/features/push_down.md)
- [TiSpark 删除数据](https://github.com/pingcap/tispark/blob/master/docs/features/delete_userguide.md)
- [历史读](https://github.com/pingcap/tispark/blob/master/docs/features/stale_read.md)
- [TiSpark with multiple catalogs](https://github.com/pingcap/tispark/wiki/TiSpark-with-multiple-catalogs)
- [TiSpark TLS](#tls-配置)
- [TiSpark 执行计划](https://github.com/pingcap/tispark/blob/master/docs/features/query_execution_plan_in_TiSpark.md)

## 统计信息

TiSpark 可以使用 TiDB 的统计信息：

- 选择代价最低的索引访问
- 估算数据大小以决定是否进行广播优化

如果你希望 TiSpark 使用统计信息支持，需要确保所涉及的表已经被分析。参考[常规统计信息](/statistics.md)了解如何进行表分析。

从 TiSpark 2.0 开始，统计信息将会默认被读取。

## FAQ

详情请参考 [TiSpark FAQ](https://github.com/pingcap/tispark/wiki/TiSpark-FAQ)。
