---
title: TiSpark 用户指南
category: reference
---

# TiSpark 用户指南

TiSpark 是 PingCAP 为解决用户复杂 OLAP 需求而推出的产品。它借助 Spark 平台，同时融合 TiKV 分布式集群的优势，和 TiDB 一起为用户一站式解决 HTAP (Hybrid Transactional/Analytical Processing) 的需求。TiSpark 依赖于 TiKV 集群和 Placement Driver (PD)，也需要你搭建一个 Spark 集群。

本文简单介绍如何部署和使用 TiSpark。本文假设你对 Spark 有基本认知。你可以参阅 [Apache Spark 官网](https://spark.apache.org/docs/latest/index.html) 了解 Spark 的相关信息。

## 概述

TiSpark 是将 Spark SQL 直接运行在分布式存储引擎 TiKV 上的 OLAP 解决方案。其架构图如下：

![TiSpark Architecture](/media/tispark-architecture.png)

+ TiSpark 深度整合了 Spark Catalyst 引擎, 可以对计算提供精确的控制，使 Spark 能够高效的读取 TiKV 中的数据，提供索引支持以实现高速的点查。
+ 通过多种计算下推减少 Spark SQL 需要处理的数据大小，以加速查询；利用 TiDB 的内建的统计信息选择更优的查询计划。
+ 从数据集群的角度看，TiSpark + TiDB 可以让用户无需进行脆弱和难以维护的 ETL，直接在同一个平台进行事务和分析两种工作，简化了系统架构和运维。
+ 除此之外，用户借助 TiSpark 项目可以在 TiDB 上使用 Spark 生态圈提供的多种工具进行数据处理。例如，使用 TiSpark 进行数据分析和 ETL；使用 TiKV 作为机器学习的数据源；借助调度系统产生定时报表等等。

## 环境准备

现有 TiSpark 2.x 版本支持 Spark 2.3.x，但并不支持 Spark 2.3.x 以外的版本。如果你希望使用 Spark 2.1.x 版本，需使用 TiSpark 1.x。

TiSpark 2.x 对于 Spark 2.3.x 的不同小版本做了些微的改动。默认的 TiSpark 支持 Spark 2.3.2，若希望使用 Spark 2.3.0 或者 Spark 2.3.1，则需要自行编译相关小版本的支持，以避免出现 API 的冲突。可以参见这个[文档](https://github.com/pingcap/tispark#how-to-build-from-sources)来获知如何从源码编译支持 Spark 2.3.x 的 TiSpark 。

TiSpark 需要 JDK 1.8+ 以及 Scala 2.11（Spark2.0+ 默认 Scala 版本）。

TiSpark 可以在 YARN，Mesos，Standalone 等任意 Spark 模式下运行。

## 推荐配置

本部分描述了 TiKV 与 TiSpark 集群分开部署、Spark 与 TiSpark 集群独立部署，以及TiSpark 与 TiKV 集群混合部署的建议配置。

### TiKV 与 TiSpark 集群分开部署的配置

对于 TiKV 与 TiSpark 分开部署的场景，可以参考如下建议配置：

+ 硬件配置建议

    普通场景可以参考 [TiDB 和 TiKV 硬件配置建议](/how-to/deploy/hardware-recommendations.md)，但是如果是偏重分析的场景，可以将 TiKV 节点增加到至少 64G 内存。

### Spark 与 TiSpark 集群独立部署的配置

关于 Spark 的详细硬件推荐配置请参考[官网](https://spark.apache.org/docs/latest/hardware-provisioning.html)，如下是 TiSpark 所需环境的简单描述：

Spark 推荐 32G 内存以上的配额。请在配置中预留 25% 的内存给操作系统。

Spark 推荐每台计算节点配备 CPU 累计 8 到 16 核以上。你可以初始设定分配所有 CPU 核给 Spark。

Spark 的具体配置方式也请参考[官方说明](https://spark.apache.org/docs/latest/spark-standalone.html)。以下为根据 `spark-env.sh` 配置的范例：

```
SPARK_EXECUTOR_MEMORY=32g
SPARK_WORKER_MEMORY=32g
SPARK_WORKER_CORES=8
```

在 `spark-defaults.conf` 中，增加如下配置：

{{< copyable "" >}}

```
spark.tispark.pd.addresses $your_pd_servers
spark.sql.extensions org.apache.spark.sql.TiExtensions
```

`your_pd_servers` 是用逗号分隔的 PD 地址，每个地址使用 `地址:端口` 的格式。

例如你有一组 PD 在`10.16.20.1`，`10.16.20.2`，`10.16.20.3`，那么 PD 配置格式是`10.16.20.1:2379,10.16.20.2:2379,10.16.20.3:2379`。

### TiSpark 与 TiKV 集群混合部署的配置

对于 TiKV 与 TiSpark 混合部署的场景，需在原有 TiKV 预留资源之外累加 Spark 所需部分，并分配 25% 的内存作为系统本身占用。

## 部署 TiSpark

TiSpark 的 jar 包可以在[这里](http://download.pingcap.org/tispark-latest-linux-amd64.tar.gz)下载，解压并拷贝到合适的目录。

### 已有 Spark 集群的部署方式

如果在已有 Spark 集群上运行 TiSpark，无需重启集群。可以使用 Spark 的 `--jars` 参数将 TiSpark 作为依赖引入：

{{< copyable "" >}}

```
spark-shell --jars $TISPARK_FOLDER/tispark-core-${version}-SNAPSHOT-jar-with-dependencies.jar
```

### 没有 Spark 集群的部署方式

如果没有使用中的 Spark 集群，推荐使用 Saprk Standalone 方式部署。这里简单介绍下 Standalone 部署方式。如果遇到问题，可以去官网寻求[帮助](https://spark.apache.org/docs/latest/spark-standalone.html)；也欢迎在我们的 GitHub 上提 [issue](https://github.com/pingcap/tispark/issues/new)。

#### 下载安装包并安装

你可以在[这里](https://spark.apache.org/downloads.html)下载 Apache Spark。

对于 Standalone 模式且无需 Hadoop 支持，则选择 Spark 2.3.x 且带有 Hadoop 依赖的 Pre-build with Apache Hadoop 2.x 任意版本。如有需要配合使用的 Hadoop 集群，则选择对应的 Hadoop 版本号。你也可以选择从源代码[自行构建](https://spark.apache.org/docs/2.3.0/building-spark.html)以配合官方 Hadoop 2.x 之前的版本。

如果你已经有了 Spark 二进制文件，并且当前 PATH 为 SPARKPATH，需将 TiSpark jar 包拷贝到 `${SPARKPATH}/jars` 目录下。

#### 启动 Master

在选中的 Spark Master 节点执行如下命令：

{{< copyable "" >}}

```
cd $SPARKPATH
```

{{< copyable "" >}}

```
./sbin/start-master.sh
```

在这步完成以后，屏幕上会打印出一个 log 文件。检查 log 文件确认 Spark-Master 是否启动成功。你可以打开 [http://spark-master-hostname:8080](http://whereever-the-ip-is:8080`c) 查看集群信息（如果你没有改动 Spark-Master 默认 Port Numebr）。在启动 Spark-Slave 的时候，也可以通过这个面板来确认 Slave 是否已经加入集群。

#### 启动 Slave

类似地，可以用如下命令启动 Spark-Slave 节点：

{{< copyable "" >}}

```
./sbin/start-slave.sh spark://spark-master-hostname:7077
```

命令返回以后，即可通过刚才的面板查看这个 Slave 是否已经正确地加入了 Spark 集群。在所有 Slave 节点重复刚才的命令。确认所有的 Slave 都可以正确连接 Master，这样你就拥有了一个 Standalone 模式的 Spark 集群。

#### Spark SQL shell 和 JDBC 服务器

当前版本的 TiSpark 可以直接使用 `spark-sql`和 Spark 的 ThriftServer JDBC 服务器。

## 一个使用范例

假设你已经按照上述步骤成功启动了 TiSpark 集群，下面简单介绍如何使用 Spark SQL 来做 OLAP 分析。这里我们用名为 tpch 数据库中的 lineitem 表作为范例。

假设你的 PD 节点位于 192.168.1.100，端口为 2379，在`$SPARK_HOME/conf/spark-defaults.conf`加入：

{{< copyable "" >}}

```
spark.tispark.pd.addresses 192.168.1.100:2379
```

{{< copyable "" >}}

```
spark.sql.extensions org.apache.spark.sql.TiExtensions
```

然后在 Spark-Shell 里像原生 Spark 一样输入下面的命令：

{{< copyable "" >}}

```scala
spark.sql("use tpch")
```

{{< copyable "" >}}

```scala
spark.sql("select count(*) from lineitem").show
```

```
+-------------+
| Count (1)   |
+-------------+
| 600000000   |
+-------------+
```

Spark SQL 交互 Shell 和原生 Spark 一致：

{{< copyable "sql" >}}

```sql
use tpch;
```

```
Time taken: 0.015 seconds
```

{{< copyable "sql" >}}

```sql
select count(*) from lineitem;
```

```
2000
Time taken: 0.673 seconds, Fetched 1 row(s)
```

SQuirreLSQL 和 hive-beeline 可以使用 JDBC 连接 Thrift 服务器。
例如，使用 beeline 连接：

{{< copyable "shell-regular" >}}

```shell
./beeline
```

```
Beeline version 1.2.2 by Apache Hive
```

```shell
beeline> !connect jdbc:hive2://localhost:10000
```

{{< copyable "sql" >}}

```sql
use testdb;
```

```
+---------+--+
| Result  |
+---------+--+
+---------+--+
No rows selected (0.013 seconds)
```

{{< copyable "sql" >}}

```sql
select count(*) from account;
```

```
+-----------+--+
| count(1)  |
+-----------+--+
| 1000000   |
+-----------+--+
1 row selected (1.97 seconds)
```

## TiSparkR

TiSparkR 是为兼容 SparkR 而开发的组件。具体使用请参考[这份文档](https://github.com/pingcap/tispark/blob/master/R/README.md)。

## TiSpark on PySpark

TiSpark on PySpark 是为兼容 PySpark 而开发的组件。具体使用请参考[这份文档](https://github.com/pingcap/tispark/blob/master/python/README.md)。

## 和 Hive 一起使用 TiSpark

TiSpark 可以和 Hive 混合使用。
在启动 Spark 之前，需要添加 HADOOP_CONF_DIR 环境变量指向 Hadoop 配置目录并且将 `hive-site.xml` 拷贝到 `$SPARK_HOME/conf` 目录下。

```
val tisparkDF = spark.sql("select * from tispark_table").toDF
tisparkDF.write.saveAsTable("hive_table") // save table to hive
spark.sql("select * from hive_table a, tispark_table b where a.col1 = b.col1").show // join table across Hive and Tispark
```

## 通过 JDBC 将 DataFrame 写入 TiDB

暂时 TiSpark 不支持直接将数据写入 TiDB 集群，但可以使用 Spark 原生的 JDBC 支持进行写入：

```scala
import org.apache.spark.sql.execution.datasources.jdbc.JDBCOptions

val customer = spark.sql("select * from customer limit 100000")
// you might repartition source to make it balance across nodes
// and increase concurrency
val df = customer.repartition(32)
df.write
.mode(saveMode = "append")
.format("jdbc")
.option("driver", "com.mysql.jdbc.Driver")
 // replace host and port as your and be sure to use rewrite batch
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

## 统计信息

TiSpark 可以使用 TiDB 的统计信息：

1. 选择代价最低的索引或扫表访问
2. 估算数据大小以决定是否进行广播优化

如果希望使用统计信息支持，需要确保所涉及的表已经被分析。请阅读[这份文档](https://pingcap.com/docs-cn/dev/reference/performance/statistics/)了解如何进行表分析。

从 TiSpark 2.0 开始，统计信息将会默认被读取。

统计信息将在 Spark Driver 进行缓存，请确定 Driver 内存足够缓存统计信息。
可以在`spark-defaults.conf`中开启或关闭统计信息读取：
  
| Property Name | Default | Description
| --------   | -----:   | :----: |
| spark.tispark.statistics.auto_load | true | 是否默认进行统计信息读取 |

## TiSpark FAQ

- Q. 是独立部署还是和现有 Spark／Hadoop 集群共用资源？

  A. 可以利用现有 Spark 集群无需单独部署，但是如果现有集群繁忙，TiSpark 将无法达到理想速度。

- Q. 是否可以和 TiKV 混合部署？

  A. 如果 TiDB 以及 TiKV 负载较高且运行关键的线上任务，请考虑单独部署 TiSpark；并且考虑使用不同的网卡保证 OLTP 的网络资源不被侵占而影响线上业务。如果线上业务要求不高或者机器负载不大，可以考虑与 TiKV 混合部署。
