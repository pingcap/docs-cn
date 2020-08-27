---
title: TiSpark Deployment Topology
summary: Learn the deployment topology of TiSpark using TiUP based on the minimal TiDB topology.
---

# TiSpark Deployment Topology

> **Warning:**
>
> TiSpark support in the TiUP cluster is still an experimental feature. It is **NOT** recommended to use it in the production environment.

This document introduces the TiSpark deployment topology and how to deploy TiSpark based on the minimum cluster topology.

TiSpark is a component built for running Apache Spark on top of TiDB/TiKV to answer complex OLAP queries. It brings benefits of both the Spark platform and the distributed TiKV cluster to TiDB and makes TiDB a one-stop solution for both online transactions and analytics.

For more information about TiSpark, see [TiSpark User Guide](/tispark-overview.md).

## Topology information

| Instance | Count | Physical machine configuration | IP | Configuration |
| :-- | :-- | :-- | :-- | :-- |
| TiDB | 3 | 16 VCore 32GB * 1 | 10.0.1.1 <br/> 10.0.1.2 <br/> 10.0.1.3 | Default port <br/>  Global directory configuration |
| PD | 3 | 4 VCore 8GB * 1 |10.0.1.4 <br/> 10.0.1.5 <br/> 10.0.1.6 | Default port <br/> Global directory configuration |
| TiKV | 3 | 16 VCore 32GB 2TB (nvme ssd) * 1 | 10.0.1.7 <br/> 10.0.1.8 <br/> 10.0.1.9 | Default port <br/> Global directory configuration |
| TiSpark | 3 | 8 VCore 16GB * 1 | 10.0.1.21 (master) <br/> 10.0.1.22 (worker) <br/> 10.0.1.23 (worker) | Default port <br/> Global directory configuration |
| Monitoring & Grafana | 1 | 4 VCore 8GB * 1 500GB (ssd) | 10.0.1.11 | Default port <br/> Global directory configuration |

## Topology templates

- [Simple TiSpark topology template](/config-templates/simple-tispark.yaml)
- [Complex TiSpark topology template](/config-templates/complex-tispark.yaml)

> **Note:**
>
> - You do not need to manually create the `tidb` user in the configuration file. The TiUP cluster component automatically creates the `tidb` user on the target machines. You can customize the user, or keep the user consistent with the control machine.
> - If you configure the deployment directory as a relative path, the cluster will be deployed in the home directory of the user.

## Prerequisites

TiSpark is based on the Apache Spark cluster, so before you start the TiDB cluster that contains TiSpark, you must ensure that Java Runtime Environment (JRE) 8 is installed on the server that deploys TiSpark. Otherwise, TiSpark cannot be started.

TiUP does not support installing JRE automatically. You need to install it on your own. For detailed installation instruction, see [How to download and install prebuilt OpenJDK packages](https://openjdk.java.net/install/).

If JRE 8 has already been installed on the deployment server but is not in the path of the system's default package management tool, you can specify the path of the JRE environment to be used by setting the `java_home` parameter in the topology configuration. This parameter corresponds to the `JAVA_HOME` system environment variable.
