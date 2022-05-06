---
title: TiSpark 用户指南
aliases: ['/zh/tidb/v5.3/get-started-with-tispark/']
---

# TiSpark 用户指南

![TiSpark 架构](/media/tispark-architecture.png)

[TiSpark](https://github.com/pingcap/tispark) 是 PingCAP 为解决用户复杂 OLAP 需求而推出的产品。它借助 Spark 平台，同时融合 TiKV 分布式集群的优势，和 TiDB 一起为用户一站式解决 HTAP (Hybrid Transactional/Analytical Processing) 的需求。

[TiFlash](/tiflash/tiflash-overview.md) 也是一个解决 HTAP 需求的产品。TiFlash 和 TiSpark 都允许使用多个主机在 OLTP 数据上执行 OLAP 查询。TiFlash 是列式存储，这提供了更高效的分析查询。TiFlash 和 TiSpark 可以同时使用。

TiSpark 依赖于 TiKV 集群和 Placement Driver (PD)，也需要你搭建一个 Spark 集群。本文简单介绍如何部署和使用 TiSpark。本文假设你对 Spark 有基本认知。你可以参阅 [Apache Spark 官网](https://spark.apache.org/docs/latest/index.html)了解 Spark 的相关信息。

TiSpark 深度整合了 Spark Catalyst 引擎，可以对计算进行精确的控制，使 Spark 能够高效地读取 TiKV 中的数据。TiSpark 还提供索引支持，帮助实现高速点查。

TiSpark 通过将计算下推到 TiKV 中提升了数据查询的效率，减少了 Spark SQL 需要处理的数据量，通过 TiDB 内置的统计信息选择最优的查询计划。

TiSpark 和 TiDB 可以让用户无需创建和维护 ETL，直接在同一个平台上进行事务和分析两种任务。这简化了系统架构，降低了运维成本。

用户可以在 TiDB 上使用 Spark 生态圈的多种工具进行数据处理，例如：

- TiSpark：数据分析和 ETL
- TiKV：数据检索
- 调度系统：生成报表

除此之外，TiSpark 还提供了分布式写入 TiKV 的功能。与使用 Spark 结合 JDBC 写入 TiDB 的方式相比，分布式写入 TiKV 能够实现事务（要么全部数据写入成功，要么全部都写入失败）。

> **警告：**
>
> 由于 TiSpark 直接访问 TiKV，所以 TiDB Server 使用的访问控制机制并不适用于 TiSpark。

## 环境准备

现有 TiSpark 2.x 版本支持 Spark 2.3.x 和 Spark 2.4.x。如果你希望使用 Spark 2.1.x 版本，需使用 TiSpark 1.x。

TiSpark 需要 JDK 1.8+ 以及 Scala 2.11（Spark2.0+ 默认 Scala 版本）。

TiSpark 可以在 YARN，Mesos，Standalone 等任意 Spark 模式下运行。

本部分描述了 TiKV 与 TiSpark 集群分开部署、Spark 与 TiSpark 集群独立部署，以及 TiKV 与 TiSpark 集群混合部署的建议配置。

关于如何通过 TiUP 部署 TiSpark，参见 [TiSpark 部署拓扑](/tispark-deployment-topology.md)。

## 推荐配置

### TiKV 与 TiSpark 集群分开部署的配置

对于 TiKV 与 TiSpark 分开部署的场景，可以参考如下建议配置：

+ 硬件配置
    - 普通场景可以参考 [TiDB 和 TiKV 硬件配置建议](/hardware-and-software-requirements.md)。
    - 如果是更偏重于分析的场景，可以将 TiKV 节点的内存增加到至少 64G。

### Spark 与 TiSpark 集群独立部署的配置

关于 Spark 的详细硬件推荐配置请参考 [Spark 硬件配置](https://spark.apache.org/docs/latest/hardware-provisioning.html)，如下是 TiSpark 所需环境的简单描述：

- 建议为 Spark 分配 32G 以上的内存，并为操作系统和缓存保留至少 25% 的内存。
- 建议每台机器至少为 Spark 分配 8 到 16 核 CPU。起初，你可以设定将所有 CPU 核分配给 Spark。

### TiKV 与 TiSpark 集群混合部署的配置

对于 TiKV 与 TiSpark 混合部署的场景，需在原有 TiKV 预留资源之外累加 Spark 所需部分，并分配 25% 的内存作为系统本身占用。

## 部署 TiSpark 集群

你可以在 [TiSpark Releases](https://github.com/pingcap/tispark/releases) 上下载对应版本的 TiSpark 的 jar 包，并存储到 `${SPARKPATH}/jars` 目录下。

> **注意：**
>
> TiSpark 2.1.x 及更早版本的 jar 文件名形如 `tispark-core-2.1.9-spark_2.4-jar-with-dependencies.jar`。请在 [TiSpark Releases](https://github.com/pingcap/tispark/releases) 中确认你需要的 TiSpark 版本的 jar 文件名。

以下是 TiSpark 2.4.1 版本 jar 包的安装示例：

{{< copyable "shell-regular" >}}

```shell
wget https://github.com/pingcap/tispark/releases/download/v2.4.1/tispark-assembly-2.4.1.jar
mv tispark-assembly-2.4.1.jar $SPARKPATH/jars/
```

将 `spark-defaults.conf.template` 文件拷贝到 `spark-defaults.conf`：

{{< copyable "shell-regular" >}}

```shell
cp conf/spark-defaults.conf.template conf/spark-defaults.conf
```

在 `spark-defaults.conf` 文件中添加如下内容：

```
spark.tispark.pd.addresses $pd_host:$pd_port
spark.sql.extensions org.apache.spark.sql.TiExtensions
```

其中 `spark.tispark.pd.addresses` 允许输入按逗号 (',') 分隔的多个 PD 服务器，请指定每个服务器的端口号。例如，当你有多个 PD 服务器在 `10.16.20.1,10.16.20.2,10.16.20.3` 的 2379 端口上时，将配置 `spark.tispark.pd.addresses` 为 `10.16.20.1:2379,10.16.20.2:2379,10.16.20.3:2379`。

> **注意：**
>
> 如果 TiSpark 无法正常使用，请检查防火墙设置。你可以自行配置防火墙策略或者禁用防火墙。

### 在已有 Spark 集群上部署 TiSpark

如果在已有 Spark 集群上运行 TiSpark，则无需重启集群，你可以使用 Spark 的 `--jars` 参数将 TiSpark 作为依赖引入：

{{< copyable "shell-regular" >}}

```shell
spark-shell --jars $TISPARK_FOLDER/tispark-${name_with_version}.jar
```

### 没有 Spark 集群的部署方式

如果没有使用中的 Spark 集群，推荐使用 Spark Standalone 模式部署 Spark，请参考 [Spark Standalone](https://spark.apache.org/docs/latest/spark-standalone.html)。如果遇到问题，可以去 [Spark 官网](https://spark.apache.org/docs/latest/spark-standalone.html)寻求帮助，也欢迎在 TiSpark 上提 [issue](https://github.com/pingcap/tispark/issues/new)。

## 使用 Spark Shell 和 Spark SQL

假设你已经按照上述步骤成功启动了 TiSpark 集群，下面简单介绍如何使用 Spark SQL 来进行 OLAP 分析。这里我们以名为 `tpch` 数据库中的 `lineitem` 表作为范例。

首先，通过 `192.168.1.101` 上的一个 TiDB 服务器生成测试数据：

{{< copyable "shell-regular" >}}

```shell
tiup bench tpch prepare --host 192.168.1.101 --user root
```

然后，根据 PD 节点地址配置 `$SPARK_HOME/conf/spark-defaults.conf`。假设你的 PD 节点位于 `192.168.1.100`，端口为 `2379`，那么在 `$SPARK_HOME/conf/spark-defaults.conf` 加入：

{{< copyable "" >}}

```
spark.tispark.pd.addresses 192.168.1.100:2379
spark.sql.extensions org.apache.spark.sql.TiExtensions
```

接着，通过如下命令启用 Spark Shell：

{{< copyable "shell-regular" >}}

```shell
./bin/spark-shell
```

然后，你可以在 Spark Shell 里像原生 Spark 一样执行下面的命令：

{{< copyable "" >}}

```scala
spark.sql("use tpch")
spark.sql("select count(*) from lineitem").show
```

结果为：

```
+-------------+
| Count (1) |
+-------------+
| 2000      |
+-------------+
```

除了 Spark Shell 之外，还可以使用 Spark SQL，通过运行如下命令启用 Spark SQL：

{{< copyable "shell-regular" >}}

```shell
./bin/spark-sql
```

你可以运行同样的查询命令：

{{< copyable "" >}}

```scala
use tpch;
select count(*) from lineitem;
```

结果为：

```
2000
Time taken: 0.673 seconds, Fetched 1 row(s)
```

## 通过 JDBC 连接 Thrift Server

你可以在没有 JDBC 支持的情况下使用 Spark Shell 或 Spark SQL，但是对于 beeline 等工具来说，JDBC 是必要的。Thrift Server 提供了 JDBC 支持。你可以通过如下命令启用 Spark 的 Thrift Server：

{{< copyable "shell-regular" >}}

```shell
./sbin/start-thriftserver.sh
```

你可以使用 JDBC 支持的 beeline 等工具连接 Thrift Server。下面以 beeline 为例：

首先，通过如下命令启用 beeline：

{{< copyable "shell-regular" >}}

```shell
./bin/beeline jdbc:hive2://localhost:10000
```

如果显示如下信息则表示 beeline 启用成功：

```
Beeline version 1.2.2 by Apache Hive
```

然后，你可以运行如下查询命令：

```
1: jdbc:hive2://localhost:10000> use testdb;
+---------+--+
| Result  |
+---------+--+
+---------+--+
No rows selected (0.013 seconds)

select count(*) from account;
+-----------+--+
| count(1)  |
+-----------+--+
| 1000000   |
+-----------+--+
1 row selected (1.97 seconds)
```

## 和 Hive 一起使用 TiSpark

TiSpark 可以和 Hive 混合使用。在启动 Spark 之前，需要添加 `HADOOP_CONF_DIR` 环境变量指向 Hadoop 配置目录并且将 `hive-site.xml` 拷贝到 `spark/conf` 目录下。

```scala
val tisparkDF = spark.sql("select * from tispark_table").toDF
tisparkDF.write.saveAsTable("hive_table") // save table to hive
spark.sql("select * from hive_table a, tispark_table b where a.col1 = b.col1").show // join table across Hive and Tispark
```

## 通过 TiSpark 将 DataFrame 批量写入 TiDB

TiSpark 从 v2.3 版本开始原生支持将 DataFrame 批量写入 TiDB 集群，该写入模式通过 TiKV 的两阶段提交协议实现。

TiSpark 批量写入相比 Spark + JDBC 写入，有以下特点：

|  比较的方面     | TiSpark 批量写入 | Spark + JDBC 写入|
| ------- | --------------- | --------------- |
| 原子性   | DataFrame 的数据要么全部写入成功，要么全部写入失败 | 如果在写入过程中 spark 任务失败退出，会出现部分数据写入成功的情况 |
| 隔离性   | 写入过程中其他事务对正在写入的数据不可见 | 写入过程中其他事务能看到部分写入成功的数据 |
| 错误恢复 | 失败后只需要重新运行 Spark 程序 | 需要业务来实现幂等，例如失败后需要先清理部分写入成功的数据，再重新运行 Spark 程序，并且需要设置 `spark.task.maxFailures=1`，防止 task 内重试导致数据重复 |
| 速度    | 直接写入 TiKV，速度更快 | 通过 TiDB 再写入 TiKV，对速度会有影响 |

以下通过 scala API 演示如何使用 TiSpark 批量写入：

```scala
// 选择需要写入的数据
val df = spark.sql("select * from tpch.ORDERS")

// 将数据写入 tidb
df.write.
  format("tidb").
  option("tidb.addr", "127.0.0.1").
  option("tidb.port", "4000").
  option("tidb.user", "root").
  option("tidb.password", "").
  option("database", "tpch").
  option("table", "target_orders").
  mode("append").
  save()
```

如果写入的数据量比较大，且写入时间超过 10 分钟，则需要保证 GC 时间大于写入时间。

```sql
UPDATE mysql.tidb SET VARIABLE_VALUE="6h" WHERE VARIABLE_NAME="tikv_gc_life_time";
```

详细使用手册请参考 [TiDB 数据源 API 用户指南](https://github.com/pingcap/tispark/blob/master/docs/datasource_api_userguide.md)。

## 通过 JDBC 将 Dataframe 写入 TiDB

除了使用 TiSpark 将 DataFrame 批量写入 TiDB 集群以外，也可以使用 Spark 原生的 JDBC 支持进行写入：

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
// 作为测试建议设置为 150
.option(JDBCOptions.JDBC_BATCH_INSERT_SIZE, 150)
.option("dbtable", s"cust_test_select") // 数据库名和表名
.option("isolationLevel", "NONE") // 如果需要写入较大 Dataframe 那么推荐将 isolationLevel 设置为 NONE
.option("user", "root") // TiDB 用户名
.save()
```

推荐将 `isolationLevel` 设置为 `NONE`，否则单一大事务有可能造成 TiDB 服务器内存溢出。

> **注意：**
>
> TiSpark 使用 JDBC 时默认 `isolationLevel` 为 `READ_UNCOMMITTED`，会造成事务隔离级别不支持的错误。推荐将 `isolationLevel` 设置为 `NONE`。

## 统计信息

TiSpark 可以使用 TiDB 的统计信息：

1. 选择代价最低的索引或扫表访问
2. 估算数据大小以决定是否进行广播优化

如果你希望 TiSpark 使用统计信息支持，需要确保所涉及的表已经被分析。请阅读[统计信息简介](/statistics.md)了解如何进行表分析。

从 TiSpark 2.0 开始，统计信息将会默认被读取。

## TiSpark FAQ

- Q. 是独立部署还是和现有 Spark／Hadoop 集群共用资源？

    A. 可以利用现有 Spark 集群无需单独部署，但是如果现有集群繁忙，TiSpark 将无法达到理想速度。

- Q. 是否可以和 TiKV 混合部署？

    A. 如果 TiDB 以及 TiKV 负载较高且运行关键的线上任务，请考虑单独部署 TiSpark；并且考虑使用不同的网卡保证 OLTP 的网络资源不被侵占而影响线上业务。如果线上业务要求不高或者机器负载不大，可以考虑与 TiKV 混合部署。

- Q. Spark 执行中报 warning：WARN ObjectStore:568 - Failed to get database

    A. Warning 忽略即可，原因是 Spark 找不到对应的 hive 库，因为这个库是在 TIKV 中，而不是在 hive 中。可以考虑调整 [log4j 日志](https://github.com/pingcap/tidb-docker-compose/blob/master/tispark/conf/log4j.properties#L43)，将该参数添加到 spark 下 conf 里 log4j 文件（如果后缀是 template 那先 mv 成后缀 properties）。

- Q. Spark 执行中报 java.sql.BatchUpdateException: Data Truncated

    A. 写入的数据长度超过了数据库定义的数据类型的长度，可以确认 target table 的字段长度，进行调整。

- Q. TiSpark 任务是否默认读取 Hive 的元数据？

    A. TiSpark 通过读取 hive-site 里的 meta 来搜寻 hive 的库。如果搜寻不到，就通过读取 tidb meta 搜寻 tidb 库。如果不需要该行为，可不在 hive site 中配置 hive 的 meta。

- Q. TiSpark 执行 Spark 任务时报："Error：java.io.InvalidClassException: com.pingcap.tikv.region.TiRegion; local class incompatible: stream classdesc serialVersionUID ..."

    A. 该报错日志中显示 serialVersionUID 冲突，说明存在不同版本的 class 和 TiRegion。因为 TiRegion 是 TiSpark 独有的，所以可能存在多个版本的 TiSpark 包。要解决该报错，请确保集群中各节点的 TiSpark 依赖包版本一致。
