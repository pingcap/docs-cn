---
title: TiSpark 部署拓扑
summary: 介绍 TiUP 部署包含 TiSpark 组件的 TiDB 集群的拓扑结构。
aliases: ['/docs-cn/dev/tispark-deployment-topology/']
---

# TiSpark 部署拓扑

本文介绍 TiSpark 部署的拓扑，以及如何在最小拓扑的基础上同时部署 TiSpark。TiSpark 是 PingCAP 为解决用户复杂 OLAP 需求而推出的产品。它借助 Spark 平台，同时融合 TiKV 分布式集群的优势，和 TiDB 一起为用户一站式解决 HTAP (Hybrid Transactional/Analytical Processing) 的需求。

关于 TiSpark 的架构介绍与使用，参见 [TiSpark 用户指南](/tispark-overview.md)。

> **警告：**
>
> TiUP Cluster 的 TiSpark 支持目前为实验特性，不建议在生产环境中使用。

## 拓扑信息

|实例 | 个数 | 物理机配置 | IP |配置 |
| :-- | :-- | :-- | :-- | :-- |
| TiDB |3 | 16 VCore 32GB * 1 | 10.0.1.1 <br/> 10.0.1.2 <br/> 10.0.1.3 | 默认端口 <br/>  全局目录配置 |
| PD | 3 | 4 VCore 8GB * 1 |10.0.1.4 <br/> 10.0.1.5 <br/> 10.0.1.6 | 默认端口 <br/> 全局目录配置 |
| TiKV | 3 | 16 VCore 32GB 2TB (nvme ssd) * 1 | 10.0.1.7 <br/> 10.0.1.8 <br/> 10.0.1.9 | 默认端口 <br/> 全局目录配置 |
| TiSpark | 3 | 8 VCore 16GB * 1 | 10.0.1.21 (master) <br/> 10.0.1.22 (worker) <br/> 10.0.1.23 (worker) | 默认端口 <br/> 全局目录配置 |
| Monitoring & Grafana | 1 | 4 VCore 8GB * 1 500GB (ssd) | 10.0.1.11 | 默认端口 <br/> 全局目录配置 |

### 拓扑模版

[简单 TiSpark 配置模板](https://github.com/pingcap/docs-cn/blob/master/config-templates/simple-tispark.yaml)

[详细 TiSpark 配置模板](https://github.com/pingcap/docs-cn/blob/master/config-templates/complex-tispark.yaml)

以上 TiDB 集群拓扑文件中，详细的配置项说明见[通过 TiUP 部署 TiDB 集群的拓扑文件配置](/tiup/tiup-cluster-topology-reference.md#tispark_masters)。

> **注意：**
>
> - 无需手动创建配置文件中的 `tidb` 用户，TiUP cluster 组件会在目标主机上自动创建该用户。可以自定义用户，也可以和中控机的用户保持一致。
> - 如果部署目录配置为相对路径，会部署在用户家目录下。

## 环境要求

由于 TiSpark 基于 Apache Spark 集群，在启动包含 TiSpark 组件的 TiDB 集群前，需要在部署了 TiSpark 组件的服务器上安装 Java 运行时环境(JRE) 8，否则将无法启动相关组件。

TiUP 不提供自动安装 JRE 的支持，该操作需要用户自行完成。JRE 8 的安装方法可以参考 [OpenJDK 的文档说明](https://openjdk.java.net/install/)。

如果部署服务器上已经安装有 JRE 8，但不在系统的默认包管理工具路径中，可以通过在拓扑配置中设置 `java_home` 参数来指定要使用的 JRE 环境所在的路径。该参数对应系统环境变量 `JAVA_HOME`。

> **注意：**
> 需保证 TiUP 对应用户有权限访问自行安装的 JRE 环境所在路径

## Spark 部署方式

TiUP cluster 目前仅支持以 standalone 方式部署 Spark。

## 版本选择

TIUP 提供以下参数进行版本选择，版本选择参数仅需在 tispark_masters 下配置，无需额外在 tispark_workers 下配置：

- tispark_version
- spark_version
- scala_version

spark_version 用于指定 Spark 版本，tispark_version 用于指定 TiSpark 版本。由于 TiSpark 一个版本下可能存在多个 jar 包，因此还需要 scala_version 最终确定所需 jar 包。具体规则如下：

1. tispark_version 与 spark_version 需要同时配置或同时不配置。当不配置时，会拉取 TiUP 仓库内的最新版本
2. scala_version 是可选参数，不配置时默认为 `v2.12`
3. 若配置的版本参数无法找到对应的 jar 包，则会报错

参考 [TiSpark Wiki](https://github.com/pingcap/tispark/wiki/Getting-TiSpark#getting-tispark-jar) 来正确配置版本参数

举个例子，TiSpark 3.0.1 同时兼容 Spark 3.0.x,3.1.x 和 3.2.x，同时只支持 scala 2.12。那么如下是可行的版本参数
- tispark_version v3.0.1, spark_version 3.0.3, scala_version 2.12
- tispark_version v3.0.1, spark_version 3.1.3, scala_version 2.12
- tispark_version v3.0.1, spark_version 3.2.1, scala_version 2.12


## 配置文件

TiUP 会自动生成最简配置如下：

spark-env.sh
```
SPARK_MASTER_HOST=${ip}
SPARK_MASTER_PORT=7077
SPARK_MASTER_WEBUI_PORT=8080
SPARK_PUBLIC_DNS=${ip}
```

spark-default.conf
```
# TiSpark >= 2.5.0

spark.master   spark://${master_ip}:{master_port}
spark.sql.extensions   org.apache.spark.sql.TiExtensions
spark.tispark.pd.addresses {$pd_ip}:{$pd_port}
spark.sql.catalog.tidb_catalog  org.apache.spark.sql.catalyst.catalog.TiCatalog
spark.sql.catalog.tidb_catalog.pd.addresses {$pd_ip}:{$pd_port}

# TiSpark < 2.5.0

spark.master   spark://${master_ip}:{master_port}
spark.sql.extensions   org.apache.spark.sql.TiExtensions
spark.tispark.pd.addresses {$pd_ip}:{$pd_port}
```

还可以使用如下参数来额外配置参数

- spark_config
- spark_env

具体可参考[详细 TiSpark 配置模板](https://github.com/pingcap/docs-cn/blob/master/config-templates/complex-tispark.yaml)


## 限制

- 暂不支持 TiSpark 及其相关组件的升级，同时 TiDB 的升级不影响 TiSpark 及其相关组件
- 由于 TiSpark jar 包[命名规则的变化](https://github.com/pingcap/tispark/releases/tag/v3.0.0), TiUP 会以重命名的方式统一包名。如 `tispark-assembly-3.0-2.5.1.jar` 会被重命名为 `tispark-assembly-3.0_2.12-2.5.1.jar`