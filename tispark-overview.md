---
title: TiSpark 用户指南
summary: 使用 TiSpark 一站式解决用户的 HTAP 需求。
aliases: ['/docs-cn/dev/tispark-overview/','/docs-cn/dev/reference/tispark/']
---

# TiSpark 用户指南

![TiSpark 架构](/media/tispark-architecture.png)

[TiSpark](https://github.com/pingcap/tispark) 是 PingCAP 为解决用户复杂 OLAP 需求而推出的产品。它借助 Spark 平台，同时融合 TiKV 分布式集群的优势，和 TiDB 一起为用户一站式解决 HTAP (Hybrid Transactional/Analytical Processing) 的需求。

[TiFlash](/tiflash/tiflash-overview.md) 是另一个实现 HTAP 的产品。TiFlash 和 TiSpark 都可以实现在 OLTP 数据上使用多主机执行 OLAP 的需求。TiFlash 是列式存储，这提供了效率更高的分析查询。TiFlash 和 TiSpark 可以同时使用。

TiSpark 依赖于 TiKV 集群和 Placement Driver (PD)，也需要你搭建一个 Spark 集群。本文简单介绍如何部署和使用 TiSpark。本文假设你对 Spark 有基本认知。你可以参阅 [Apache Spark 官网](https://spark.apache.org/docs/latest/index.html)了解 Spark 的相关信息。

TiSpark 深度整合了 Spark Catalyst 引擎，可以对计算进行精确地控制，使 Spark 能够高效地读取 TiKV 中的数据。TiSpark 还提供了索引支持以实现高速的点查。

TiSpark 通过将计算下推到 TiKV 中提升了数据查询的效率，减少了 Spark SQL 需要处理的数据大小，通过利用 TiDB 内置的统计信息选择更优的查询计划。

TiSpark 和 TiDB 可以让用户无需创建和维护 ETL，直接在同一个平台上进行事务和统计分析两种任务。这简化了系统架构，降低了运维成本。

用户可以在 TiDB 上使用 Spark 生态圈的多种工具进行数据处理，例如：

- TiSpark：数据分析和 ETL
- TiKV：数据检索
- 调度系统：生成报表

除此之外，TiSpark 还提供了分布式写入 TiKV 的功能。与使用 Spark 结合 JDBC 写入 TiDB 的方式相比，分布式写入 TiKV 能够实现事务（要么全部数据写入成功，要么全部都写入失败），而且写入速度更快。

> **警告：**
>
> 由于 TiSpark 直接访问 TiKV，所以 TiDB Server 使用的访问控制机制并不适用于 TiSpark。

## 环境准备

目前 TiSpark 支持版本的兼容情况如下所示，你可以根据需要选择相应的 TiSpark 版本。

| TiSpark 版本 | TiDB、TiKV、PD 版本 | Spark 版本 | Scala 版本 |
| ---------------  | -------------------- | ------------- | ------------- |
| 2.4.x-scala_2.11 | 5.x，4.x             | 2.3.x，2.4.x   | 2.11          |
| 2.4.x-scala_2.12 | 5.x，4.x             | 2.4.x         | 2.12          |
| 2.5.x            | 5.x，4.x             | 3.0.x，3.1.x   | 2.12          |

TiSpark 可以在 YARN，Mesos，Standalone 等任意 Spark 模式下运行。

本部分描述了 TiKV 与 TiSpark 集群分开部署、Spark 与 TiSpark 集群独立部署，以及 TiKV 与 TiSpark 集群混合部署的建议配置。

关于如何通过 TiUP 部署 TiSpark，参见 [TiSpark 部署拓扑](/tispark-deployment-topology.md)。

### TiKV 与 TiSpark 集群分开部署的配置

对于 TiKV 与 TiSpark 分开部署的场景，可以参考如下建议配置：

+ 硬件配置建议

    普通场景可以参考 [TiDB 和 TiKV 硬件配置建议](/hardware-and-software-requirements.md)，但是如果是偏重分析的场景，可以将 TiKV 节点增加到至少 64G 内存。

### Spark 与 TiSpark 集群独立部署的配置

关于 Spark 的详细硬件推荐配置请参考 [Spark 硬件配置](https://spark.apache.org/docs/latest/hardware-provisioning.html)，如下是 TiSpark 所需环境的简单描述：

Spark 推荐 32G 内存以上的配额。请在配置中预留 25% 的内存给操作系统。

Spark 推荐每台计算节点配备 CPU 累计 8 到 16 核以上。你可以初始设定分配所有 CPU 核给 Spark。

### TiKV 与 TiSpark 集群混合部署的配置

对于 TiKV 与 TiSpark 混合部署的场景，需在原有 TiKV 预留资源之外累加 Spark 所需部分，并分配 25% 的内存作为系统本身占用。

### 通过 Spark Standalone 模式部署 TiSpark

关于 Spark 的具体配置方式，请参考 [Spark Standalone](https://spark.apache.org/docs/latest/spark-standalone.html)。

推荐使用 Spark Standalone 方式部署 Spark。如果遇到问题，可以去 [Spark 官网](https://spark.apache.org/docs/latest/spark-standalone.html)寻求帮助，也欢迎在 TiSpark 上提 [issue](https://github.com/pingcap/tispark/issues/new)。

#### 下载并安装

你可以从 [Apache Spark Archive](https://archive.apache.org/dist/spark/) 下载 Spark 2.x 版本。

当你不需要 Hadoop 支持的时候，选择 Spark **2.4.x** 版本，带有任意版本 Hadoop 依赖的预编译二进制包，例如 `spark-2.4.8-bin-hadoop2.7.tgz`。如果需要使用 Hadoop 集群（如 Hadoop 2.6 版本），则选择相应的 Hadoop 版本号，例如 `spark-2.4.8-bin-hadoop2.6.tgz`。对于 Hadoop 2.x 之前的版本，你可以从源代码[自行构建](https://spark.apache.org/docs/latest/building-spark.html)。

下面为 `spark-2.4.8-bin-hadoop2.7.tgz` 的下载与安装示例：

```shell
wget https://archive.apache.org/dist/spark/spark-2.4.8/spark-2.4.8-bin-hadoop2.7.tgz
tar zxf spark-2.4.8-bin-hadoop2.7.tgz
mv spark-2.4.8-bin-hadoop2.7 spark
export SPARKPATH=~/spark # 同样添加到 ~/.bashrc
cd spark
```

## 部署 TiSpark 集群

你可以在 [TiSpark Releases](https://github.com/pingcap/tispark/releases) 上下载对应版本的 TiSpark 的 jar 包，并存储到 `${SPARKPATH}/jars` 目录下。

> **注意：**
>
> TiSpark 2.1.x 及更早版本的 jar 文件名形如 `tispark-core-2.1.9-spark_2.4-jar-with-dependencies.jar`。请在 [TiSpark Releases](https://github.com/pingcap/tispark/releases) 中确认你需要的 TiSpark 版本的 jar 文件名。

以下是 TiSpark 2.4.1 版本 jar 包的安装示例：

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

```shell
spark.tispark.pd.addresses $pd_host:$pd_port
spark.sql.extensions org.apache.spark.sql.TiExtensions
```

其中 `spark.tispark.pd.addresses` 允许输入按逗号 (',') 分隔的多个 PD 服务器，请指定每个服务器的端口号。例如，当你的多个 PD 服务器在 `10.16.20.1,10.16.20.2,10.16.20.3` 的 2379 端口上时，配置 `spark.tispark.pd.addresses` 为 `10.16.20.1:2379,10.16.20.2:2379,10.16.20.3:2379`。

> **注意：**
>
> 如果 TiSpark 无法正常使用，请检查防火墙配置。你可以自行配置防火墙策略或者禁用防火墙。

### 启动 Master 节点

在选中的 Spark Master 节点执行如下命令：

{{< copyable "shell-regular" >}}

```shell
cd $SPARKPATH
./sbin/start-master.sh
```

在这步完成以后，屏幕上会打印出一个 log 文件。检查 log 文件确认 Spark-Master 是否启动成功。你可以打开 <http://spark-master-hostname:8080> 查看集群信息（如果你没有改动 Spark-Master 默认端口号）。在启动 Spark-Worker 的时候，也可以通过这个面板来确认 Worker 是否已经加入集群。

### 启动 Worker 节点

类似地，可以用如下命令启动 Spark-Worker 节点：

{{< copyable "shell-regular" >}}

```shell
./sbin/start-slave.sh spark://spark-master-hostname:7077
```

> **注意：**
>
> 如果在同一主机上启动 Master 节点和 Worker 节点，那么不能使用 `127.0.0.1` 或 `localhost`。因为 Master 进程默认仅监听外部。

命令返回以后，即可通过刚才的面板查看这个 Worker 是否已经正确地加入了 Spark 集群。在所有 Worker 节点重复刚才的命令,确认所有的 Worker 都可以正确连接 Master，这样你就拥有了一个 Standalone 模式的 Spark 集群。

### 在已有 Spark 集群上部署 TiSpark

如果在已有 Spark 集群上运行 TiSpark，无需重启集群。可以使用 Spark 的 `--jars` 参数将 TiSpark 作为依赖引入：

{{< copyable "shell-regular" >}}

```shell
spark-shell --jars $TISPARK_FOLDER/tispark-${name_with_version}.jar
```

## 使用 Spark Shell 和 Spark SQL

假设你已经按照上述步骤成功启动了 TiSpark 集群，下面简单介绍如何使用 Spark SQL 来做 OLAP 分析。这里我们用名为 `tpch` 数据库中的 `lineitem` 表作为范例。

通过 192.168.1.101 上的一个 TiDB 服务器生成测试数据：

{{< copyable "shell-regular" >}}

```shell
tiup bench tpch prepare --host 192.168.1.101 --user root
```

假设你的 PD 节点位于 `192.168.1.100`，端口为 `2379`，在 `$SPARK_HOME/conf/spark-defaults.conf` 加入：

{{< copyable "" >}}

```
spark.tispark.pd.addresses 192.168.1.100:2379
spark.sql.extensions org.apache.spark.sql.TiExtensions
```

启用 Spark Shell：

{{< copyable "shell-regular" >}}

```shell
./bin/spark-shell
```

然后在 Spark Shell 里像原生 Spark 一样输入下面的命令：

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

除了 Spark Shell 之外，还可以使用 Spark SQL，通过如下命令运行：

{{< copyable "shell-regular" >}}

```shell
./bin/spark-sql
```

你可以运行同样的查询命令：

{{< copyable "" >}}

```scala
spark-sql> use tpch;
```

```
Time taken: 0.015 seconds
```

{{< copyable "" >}}

```scala
spark-sql> select count(*) from lineitem;
```

```
2000
Time taken: 0.673 seconds, Fetched 1 row(s)
```

## 使用 JDBC 连接 ThriftServer

无需 JDBC 你同样可以使用 `spark-shell` 或 `spark-sql`，但是对于 `beeline` 工具来说，需要使用 JDBC 

You can use `spark-shell` or `spark-sql` without JDBC support. However, JDBC support is required for tools like `beeline`. JDBC support is provided by Thrift server.

To use Spark's Thrift server, run:

{{< copyable "shell-regular" >}}

```shell
./sbin/start-thriftserver.sh
```

To connect JDBC with Thrift server, you can use JDBC supported tools including beeline. For example, to use it with beeline:

{{< copyable "shell-regular" >}}

```shell
./bin/beeline jdbc:hive2://localhost:10000
Beeline version 1.2.2 by Apache Hive
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

```
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
// select data to write
val df = spark.sql("select * from tpch.ORDERS")

// write data to tidb
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
update mysql.tidb set VARIABLE_VALUE="6h" where VARIABLE_NAME="tikv_gc_life_time";
```

详细使用手册请参考[该文档](https://github.com/pingcap/tispark/blob/master/docs/datasource_api_userguide.md)。

Starting from v2.3, TiSpark natively supports batch writing DataFrames into TiDB clusters. This writing mode is implemented through the two-phase commit protocol of TiKV.

Compared with the writing through Spark + JDBC, the TiSpark batch writing has the following advantages:

|  Aspects to compare    | TiSpark batch writes | Spark + JDBC writes|
| ------- | --------------- | --------------- |
| Atomicity   | The DataFrames either are all written successfully or all fail to write. | If the Spark task fails and exits during the writing process, a part of the data might be written successfully. |
| Isolation   | During the writing process, the data being written is invisible to other transactions. | During the writing process, some successfully written data is visible to other transactions.  |
| Error recovery | If the batch write fails, you only need to re-run Spark. | An application is required to achieve idempotence. For example, if the batch write fails, you need to clean up the part of the successfully written data and re-run Spark. You need to set `spark.task.maxFailures=1` to prevent data duplication caused by task retry. |
| Speed    | Data is directly written into TiKV, which is faster. | Data is written to TiKV through TiDB, which affects the speed. |

The following example shows how to batch write data using TiSpark via the scala API:

```scala
// select data to write
val df = spark.sql("select * from tpch.ORDERS")

// write data to tidb
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

If the amount of data to write is large and the writing time exceeds ten minutes, you need to ensure that the GC time is longer than the writing time.

```sql
UPDATE mysql.tidb SET VARIABLE_VALUE="6h" WHERE VARIABLE_NAME="tikv_gc_life_time";
```

Refer to [this document](https://github.com/pingcap/tispark/blob/master/docs/datasource_api_userguide.md) for details.

## 通过 JDBC 将 Dataframe 写入 TiDB

除了使用 TiSpark 将 DataFrame 批量写入 TiDB 集群以外，也可以使用 Spark 原生的 JDBC 支持进行写入：

```scala
import org.apache.spark.sql.execution.datasources.jdbc.JDBCOptions

val customer = spark.sql("select * from customer limit 100000")
// You might repartition the source to make it balance across nodes
// and increase the concurrency.
val df = customer.repartition(32)
df.write
.mode(saveMode = "append")
.format("jdbc")
.option("driver", "com.mysql.jdbc.Driver")
 // Replace the host and port with that of your own and be sure to use the rewrite batch
.option("url", "jdbc:mysql://127.0.0.1:4000/test?rewriteBatchedStatements=true")
.option("useSSL", "false")
// As tested, 150 is good practice
.option(JDBCOptions.JDBC_BATCH_INSERT_SIZE, 150)
.option("dbtable", s"cust_test_select") // database name and table name here
.option("isolationLevel", "NONE") // recommended to set isolationLevel to NONE if you have a large DF to load.
.option("user", "root") // TiDB user here
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

## 安全性

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

更多详细信息，请参考 [TiSpark 鉴权与授权指南](https://github.com/pingcap/tispark/blob/master/docs/authorization_userguide.md)。

> **注意：**
>
> 开启鉴权功能后，TiSpark Spark SQL 只能使用 TiDB 作为数据源，切换到其他数据源（例如 Hive）会导致数据表不可见。

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
