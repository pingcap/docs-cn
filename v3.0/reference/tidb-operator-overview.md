---
title: TiDB Operator 简介
category: reference
---

# TiDB Operator 简介

TiDB Operator 是 Kubernetes 上的 TiDB 集群自动运维系统，提供包括部署、升级、扩缩容、备份恢复、配置变更的 TiDB 全生命周期管理。借助 TiDB Operator，TiDB 可以无缝运行在公有云或私有部署的 Kubernetes 集群上。

## TiDB Operator 整体架构

![TiDB Operator Overview](/media/tidb-operator-overview.png)

其中，`TidbCluster` 是由 CRD（`CustomResourceDefinition`）定义的自定义资源，用于描述用户期望的 TiDB 集群状态。TiDB 集群的编排和调度逻辑则由下列组件负责：

* `tidb-controller-manager` 是一组 Kubernetes 上的自定义控制器。这些控制器会不断对比 `TidbCluster` 对象中记录的期望状态与 TiDB 集群的实际状态，并调整 Kubernetes 中的资源以驱动 TiDB 集群满足期望状态；
* `tidb-scheduler` 是一个 Kubernetes 调度器扩展，它为 Kubernetes 调度器注入 TiBD 集群特有的调度逻辑；

此外，TiDB Operator 还提供了命令行接口 `tkctl` 用于运维集群和诊断集群问题。

![TiDB Operator Control Flow](/media/tidb-operator-control-flow.png)

上图是 TiDB Operator 的控制流程解析。由于 TiDB 集群还需要监控、初始化、定时备份、Binlog 等组件，TiDB Operator 中使用 Helm Chart 封装了 TiDB 集群定义。整体的控制流程如下：

1. 用户通过 Helm 创建 `TidbCluster` 对象和相应的一系列 Kubernetes 原生对象，比如执行定时备份的 `CronJob`；
2. TiDB Operator 会 watch `TidbCluster` 以及其它相关对象，基于集群的实际状态不断调整 PD、TiKV、TiDB 的 `StatefulSet` 和 `Service` 对象；
3. Kubernetes 的原生控制器根据 `StatefulSet`、`Deployment`、`CronJob` 等对象创建更新或删除对应的 `Pod`；
4. PD、TiKV、TiDB 的 `Pod` 声明中会指定使用 `tidb-scheduler` 调度器，`tidb-scheduler` 会在调度对应 `Pod` 时应用 TiDB 的特定调度逻辑。

基于上述的声明式控制流程，TiDB Operator 能够自动进行集群节点健康检查和故障恢复。部署、升级、扩缩容等操作也可以通过修改 `TidbCluster` 对象声明“一键”完成。

## 使用 TiDB Operator 管理 TiDB 集群

TiDB Operator 提供了多种方式来部署 Kubernetes 上的 TiDB 集群：

+ 测试环境：
    - [DinD](how-to/get-started/deploy-tidb-from-kubernetes-dind.md)：使用 TiDB Operator 在本地 DinD 环境部署 TiDB 集群；
    - [Minikube](how-to/get-started/deploy-tidb-from-kubernetes-minikube.md)：使用 TiDB Operator 在本地 Minikube 环境部署 TiDB 集群；
    - [GKE](how-to/get-started/deploy-tidb-from-kubernetes-gke.md)：使用 TiDB Operator 在 GKE 上部署 TiDB 集群。

+ 生产环境：

    - 公有云：参考 [AWS 部署文档](how-to/deploy/tidb-in-kubernetes/aws-eks.md)，[GKE 部署文档 (beta)](how-to/deploy/tidb-in-kubernetes/gcp-gke.md)，或[阿里云部署文档](how-to/deploy/tidb-in-kubernetes/alibaba-cloud.md)在对应的公有云上一键部署生产可用的 TiDB 集群并进行后续的运维管理；

    - 现有 Kubernetes 集群：首先按照[部署 TiDB Operator](how-to/deploy/tidb-in-kubernetes/tidb-operator.md)在集群中安装 TiDB Operator，再根据[在标准 Kubernetes 集群上部署 TiDB 集群](how-to/deploy/tidb-in-kubernetes/general-kubernetes.md)来部署你的 TiDB 集群。对于生产级 TiDB 集群，你还需要参考 [TiDB 集群环境要求](reference/configuration/tidb-in-kubernetes/local-pv-configuration.md)调整 Kubernetes 集群配置并根据[本地 PV 配置](reference/configuration/tidb-in-kubernetes/local-pv-configuration.md)为你的 Kubernetes 集群配置本地 PV，以满足 TiKV 的低延迟本地存储需求。

在任何环境上部署前，都可以参考 [TiDB 集群配置](reference/configuration/tidb-in-kubernetes/cluster-configuration.md)来自定义 TiDB 配置。

部署完成后，你可以参考下面的文档进行 Kubernetes 上 TiDB 集群的使用和运维：

+ [部署 TiDB 集群](how-to/deploy/tidb-in-kubernetes/general-kubernetes.md)
+ [访问 TiDB 集群](how-to/deploy/tidb-in-kubernetes/access-tidb.md)
+ [TiDB 集群扩缩容](how-to/scale/tidb-in-kubernetes.md)
+ [TiDB 集群升级](how-to/upgrade/tidb-in-kubernetes.md#升级-tidb-版本)
+ [TiDB 集群配置变更](how-to/upgrade/tidb-in-kubernetes.md#更新-tidb-集群配置)
+ [TiDB 集群备份恢复](how-to/maintain/tidb-in-kubernetes/backup-and-restore.md)
+ [配置 TiDB 集群故障自动转移](how-to/maintain/tidb-in-kubernetes/auto-failover.md)
+ [监控 TiDB 集群](how-to/monitor/tidb-in-kubernetes.md)
+ [TiDB 集群日志收集](how-to/maintain/tidb-in-kubernetes/log-collecting.md)
+ [维护 TiDB 所在的 Kubernetes 节点](how-to/maintain/tidb-in-kubernetes/k8s-node-for-tidb.md)

当集群出现问题需要进行诊断时，你可以：

+ 查阅 [Kubernetes 上的 TiDB FAQ](faq/tidb-in-kubernetes.md) 寻找是否存在现成的解决办法；
+ 参考 [Kubernetes 上的 TiDB 故障诊断](how-to/troubleshoot/tidb-in-kubernetes.md)解决故障。

Kubernetes 上的 TiDB 提供了专用的命令行工具 `tkctl` 用于集群管理和辅助诊断，同时，在 Kubernetes 上，TiDB 的部分生态工具的使用方法也有所不同，你可以：

+ 参考 [`tkctl` 使用指南](reference/tools/tkctl.md) 来使用 `tkctl`；
+ 参考 [Kubernetes 上的 TiDB 相关工具使用](reference/tools/tools-in-kubernetes.md) 来了解 TiDB 生态工具在 Kubernetes 上的使用方法。

最后，当 TiDB Operator 发布新版本时，你可以参考[升级 TiDB Operator](how-to/upgrade/tidb-operator.md) 进行版本更新。
