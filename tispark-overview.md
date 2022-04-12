---
title: TiSpark 用户指南
summary: 使用 TiSpark 为用户一站式解决 HTAP 的需求。
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

```
wget https://archive.apache.org/dist/spark/spark-2.4.8/spark-2.4.8-bin-hadoop2.7.tgz
tar zxf spark-2.4.8-bin-hadoop2.7.tgz
mv spark-2.4.8-bin-hadoop2.7 spark
export SPARKPATH=~/spark # Also add this to your ~/.bashrc
cd spark
```

## 部署 TiSpark 集群

你可以在 [TiSpark Releases](https://github.com/pingcap/tispark/releases) 上下载对应版本的 TiSpark 的 jar 包，并存储到 `${SPARKPATH}/jars` 目录下。

> **注意：**
>
> TiSpark 2.1.x 及更早版本的 jar 文件名形如 `tispark-core-2.1.9-spark_2.4-jar-with-dependencies.jar`。请在 [TiSpark Releases](https://github.com/pingcap/tispark/releases) 中确认你需要的 TiSpark 版本的 jar 文件名。

以下是 TiSpark 2.4.1 版本 jar 包的安装示例：

```
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

其中 `spark.tispark.pd.addresses` 允许输入多个 PD 服务器，请为每个指定端口号。例如，当你的多个 PD 服务器在 `10.16.20.1,10.16.20.2,10.16.20.3` 的 2379 端口上时，配置输入 `10.16.20.1:2379,10.16.20.2:2379,10.16.20.3:2379`。

CentOS 上 `firewalld` 的默认设置阻止了 TiSpark 所需的通信。因此，请先关闭 `firewalld` 以确保 TiSpark 的正常运行。

{{< copyable "bash" >}}

```bash
sudo systemctl stop firewalld.service
sudo systemctl disable firewalld.service
sudo systemctl mask --now firewalld.service
```

### 启动 Master 节点

在选中的 Spark Master 节点执行如下命令：

```bash
cd $SPARKPATH
./sbin/start-master.sh
```

在这步完成以后，屏幕上会打印出一个 log 文件。检查 log 文件确认 Spark-Master 是否启动成功。你可以打开 <http://spark-master-hostname:8080> 查看集群信息（如果你没有改动 Spark-Master 默认端口号）。在启动 Spark-Worker 的时候，也可以通过这个面板来确认 Worker 是否已经加入集群。

### 启动 Worker 节点

类似地，可以用如下命令启动 Spark-Worker 节点：

{{< copyable "bash" >}}

```bash
./sbin/start-slave.sh spark://spark-master-hostname:7077
```

请注意如果在同一主机上运行 Master 节点和 Worker 节点，那么不能使用 `127.0.0.1` 或 `localhost`。因为 Master 进程默认仅监听外部

命令返回以后，即可通过刚才的面板查看这个 Worker 是否已经正确地加入了 Spark 集群。在所有 Worker 节点重复刚才的命令。确认所有的 Worker 都可以正确连接 Master，这样你就拥有了一个 Standalone 模式的 Spark 集群。
