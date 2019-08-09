---
title: Kubernetes 上的 TiDB 集群常见问题
category: FAQ
---

# Kubernetes 上的 TiDB 集群常见问题

本文介绍 Kubernetes 上的 TiDB 集群常见问题以及解决方案。

## 如何修改时区设置？

默认情况下，在 Kubernetes 集群上部署的 TiDB 集群各组件容器中的时区为 UTC，如果要修改时区配置，有下面两种情况：

* 第一次部署集群

    在 TiDB 集群的 `values.yaml` 文件中，修改 `timezone` 配置，例如：`timezone: Asia/Shanghai`，然后部署 TiDB 集群。

* 集群已经在运行

    如果 TiDB 集群已经在运行，需要做如下修改：

    * 在 TiDB 集群的 `values.yaml` 文件中，修改 `timezone` 配置，例如：`timezone: Asia/Shanghai`，然后升级 TiDB 集群。
    * 参考[时区支持](/how-to/configure/time-zone.md)，修改 TiDB 服务时区配置。

## TiDB 相关组件可以配置 HPA 或 VPA 么？

TiDB 集群目前还不支持 HPA（Horizontal Pod Autoscaling，自动水平扩缩容）和 VPA（Vertical Pod Autoscaling，自动垂直扩缩容），因为对于数据库这种有状态应用而言，实现自动扩缩容难度较大，无法仅通过 CPU 和 memory 监控数据来简单地实现。

## 使用 TiDB Operator 编排 TiDB 集群时，有什么场景需要人工介入操作吗？

如果不考虑 Kubernetes 集群本身的运维，TiDB Operator 存在以下可能需要人工介入的场景：

* TiKV 自动故障转移之后的集群调整，参考[自动故障转移](tidb-in-kubernetes/maintain/auto-failover.md)；
* 维护或下线指定的 Kubernetes 节点，参考[维护节点](tidb-in-kubernetes/maintain/kubernetes-node.md)。

## 在公有云上使用 TiDB Operator 编排 TiDB 集群时，推荐的部署拓扑是怎样的？

首先，为了实现高可用和数据安全，我们在推荐生产环境下的 TiDB 集群中至少部署在三个可用区 (Available Zone)。

当考虑 TiDB 集群与业务服务的部署拓扑关系时，TiDB Operator 支持下面几种部署形态。它们有各自的优势与劣势，具体选型需要根据实际业务需求进行权衡：

* 将 TiDB 集群与业务服务部署在同一个 VPC 中的同一个 Kubernetes 集群上；
* 将 TiDB 集群与业务服务部署在同一个 VPC 中的不同 Kubernetes 集群上；
* 将 TiDB 集群与业务服务部署在不同 VPC 中的不同 Kubernetes 集群上。

## TiDB Operator 支持 TiSpark 吗？

TiDB Operator 尚不支持自动编排 TiSpark。

假如要为 TiDB in Kubernetes 添加 TiSpark 组件，你需要在**同一个** Kubernetes 集群中自行维护 Spark，确保 Spark 能够访问到 PD 和 TiKV 实例的 IP 与端口，并为 Spark 安装 TiSpark 插件，TiSpark 插件的安装方式可以参考 [TiSpark](/reference/tispark.md#已有-Spark-集群的部署方式)。

在 Kubernetes 上维护 Spark 可以参考 Spark 的官方文档：[Spark on Kubernetes](http://spark.apache.org/docs/latest/running-on-kubernetes.html)。

## 如何查看 TiDB 集群配置？

如果需要查看当前集群的 PD、TiKV、TiDB 组件的配置信息，可以执行下列命令:

* 查看 PD 配置文件

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl exec -it <pdPodName> -n <namespace> -- cat /etc/pd/pd.toml
    ```

* 查看 TiKV 配置文件

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl exec -it <tikvPodName> -n <namespace> -- cat /etc/tikv/tikv.toml
    ```

* 查看 TiDB 配置文件

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl exec -it <tidbPodName> -c tidb -n <namespace> -- cat /etc/tidb/tidb.toml
    ```
