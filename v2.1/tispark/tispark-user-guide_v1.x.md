---
title: TiSpark 用户指南
category: tispark
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

现有 TiSpark 版本支持 Spark 2.1。对于 Spark 2.0 及 Spark 2.2 尚未经过良好的测试验证，对于更低版本暂时不支持。

TiSpark 需要 JDK 1.8+ 以及 Scala 2.11（Spark2.0+ 默认 Scala 版本）。

TiSpark 可以在 YARN，Mesos，Standalone 等任意 Spark 模式下运行。

## 推荐配置

本部分描述了 TiKV 与 TiSpark 集群分开部署、Spark 与 TiSpark 集群独立部署，以及TiSpark 与 TiKV 集群混合部署的建议配置。

### TiKV 与 TiSpark 集群分开部署的配置

对于 TiKV 与 TiSpark 分开部署的场景，可以参考如下建议配置：

+ 硬件配置建议

    普通场景可以参考 [TiDB 和 TiKV 硬件配置建议](/v2.1/how-to/deploy/hardware-recommendations.md)，但是如果是偏重分析的场景，可以将 TiKV 节点增加到至少 64G 内存。

+ TiKV 参数建议

    ```toml
    [server]
    end-point-concurrency = 8  # 如果使用场景偏向分析，则可以考虑扩大这个参数
    [raftstore]
    sync-log = false
    [rocksdb]
    max-background-compactions = 6
    max-background-flushes = 2
    [rocksdb.defaultcf]
    block-cache-size = "10GB"
    [rocksdb.writecf]
    block-cache-size = "4GB"
    [rocksdb.raftcf]
    block-cache-size = "1GB"
    [rocksdb.lockcf]
    block-cache-size = "1GB"
    [storage]
    scheduler-worker-pool-size = 4
    ```

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

### TiSpark 与 TiKV 集群混合部署的配置

对于 TiKV 与 TiSpark 混合部署的场景，需在原有 TiKV 预留资源之外累加 Spark 所需部分，并分配 25% 的内存作为系统本身占用。

## 部署 TiSpark

TiSpark 的 jar 包可以在[这里](http://download.pingcap.org/tispark-0.1.0-SNAPSHOT-jar-with-dependencies.jar)下载。

### 已有 Spark 集群的部署方式

如果在已有 Spark 集群上运行 TiSpark，无需重启集群。可以使用 Spark 的 `--jars` 参数将 TiSpark 作为依赖引入：

```
spark-shell --jars $PATH/tispark-0.1.0.jar
```

如果想将 TiSpark 作为默认组件部署，只需要将 TiSpark 的 jar 包放进 Spark 集群每个节点的 jars 路径并重启 Spark 集群：

```
${SPARK_INSTALL_PATH}/jars
```

这样无论是使用 Spark-Submit 还是 Spark-Shell 都可以直接使用 TiSpark。

### 没有 Spark 集群的部署方式

如果没有使用中的 Spark 集群，推荐使用 Saprk Standalone 方式部署。这里简单介绍下 Standalone 部署方式。如果遇到问题，可以去官网寻求[帮助](https://spark.apache.org/docs/latest/spark-standalone.html)；也欢迎在我们的 GitHub 上提 [issue](https://github.com/pingcap/tispark/issues/new)。

#### 下载安装包并安装

你可以在[这里](https://spark.apache.org/downloads.html)下载 Apache Spark。

对于 Standalone 模式且无需 Hadoop 支持，则选择 Spark 2.1.x 且带有 Hadoop 依赖的 Pre-build with Apache Hadoop 2.x 任意版本。如有需要配合使用的 Hadoop 集群，则选择对应的 Hadoop 版本号。你也可以选择从源代码[自行构建](https://spark.apache.org/docs/2.1.0/building-spark.html)以配合官方 Hadoop 2.6 之前的版本。

> **注意：**
>
> 目前 TiSpark 仅支持 Spark 2.1.x 版本。

如果你已经有了 Spark 二进制文件，并且当前 PATH 为 SPARKPATH，需将 TiSpark jar 包拷贝到 `${SPARKPATH}/jars` 目录下。

#### 启动 Master

在选中的 Spark Master 节点执行如下命令：

```
cd $SPARKPATH
./sbin/start-master.sh
```

在这步完成以后，屏幕上会打印出一个 log 文件。检查 log 文件确认 Spark-Master 是否启动成功。你可以打开 <http://spark-master-hostname:8080> 查看集群信息（如果你没有改动 Spark-Master 默认 Port Numebr）。在启动 Spark-Slave 的时候，也可以通过这个面板来确认 Slave 是否已经加入集群。

#### 启动 Slave

类似地，可以用如下命令启动 Spark-Slave 节点：

```bash
./sbin/start-slave.sh spark://spark-master-hostname:7077
```

命令返回以后，即可通过刚才的面板查看这个 Slave 是否已经正确地加入了 Spark 集群。在所有 Slave 节点重复刚才的命令。确认所有的 Slave 都可以正确连接 Master，这样你就拥有了一个 Standalone 模式的 Spark 集群。

## 一个使用范例

假设你已经按照上述步骤成功启动了 TiSpark 集群，下面简单介绍如何使用 Spark SQL 来做 OLAP 分析。这里我们用名为 tpch 数据库中的 lineitem 表作为范例。

假设你的 PD 节点位于 192.168.1.100，端口为 2379，在`$SPARK_HOME/conf/spark-defaults.conf`加入：

```
spark.tispark.pd.addresses 192.168.1.100:2379
```

然后在 Spark-Shell 里输入下面的命令：

```scala
import org.apache.spark.sql.TiContext

val ti = new TiContext(spark)

ti.tidbMapDatabase("tpch")
```

之后你可以直接调用 Spark SQL:

```scala
spark.sql("select count(*) from lineitem").show
```

结果为：

```
+-------------+
| Count (1)   |
+-------------+
| 600000000   |
+-------------+
```

## TiSpark FAQ

- Q. 是独立部署还是和现有 Spark／Hadoop 集群共用资源？

    A. 可以利用现有 Spark 集群无需单独部署，但是如果现有集群繁忙，TiSpark 将无法达到理想速度。

- Q. 是否可以和 TiKV 混合部署？

    A. 如果 TiDB 以及 TiKV 负载较高且运行关键的线上任务，请考虑单独部署 TiSpark；并且考虑使用不同的网卡保证 OLTP 的网络资源不被侵占而影响线上业务。如果线上业务要求不高或者机器负载不大，可以考虑与 TiKV 混合部署。
