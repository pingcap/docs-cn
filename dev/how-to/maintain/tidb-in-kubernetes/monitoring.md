---
title: 监控系统部署
category: how-to
---

# 监控系统部署

基于 Kubernetes 环境部署的 TiDB 集群监控可以大体分为两个部分：对 TiDB 集群本身的监控、对 Kubernetes 集群及 TiDB Operator 的监控。本文将对两者进行简要说明。

## TiDB 集群的监控

TiDB 通过 Prometheus 和 Grafana 监控 TiDB 集群。在通过 TiDB Operator 创建新的 TiDB 集群时，对于每个 TiDB 集群，会同时创建、配置一套独立的监控系统，与 TiDB 集群运行在同一 Namespace, 包括 Prometheus 和 Grafana 两个组件。

监控数据默认没有持久化，如果由于某些原因监控容器重启，已有的监控数据会丢失。可以在 `values.yaml` 中设置 `monitor.persistent` 为 `true` 来持久化监控数据。

可以通过 `kubectl port-forward` 查看监控面板：

{{< copyable "shell-regular" >}}

```shell
kubectl port-forward -n ${namespace} svc/${releaseName}-grafana 3000:3000 &>/tmp/portforward-grafana.log
```

然后在浏览器中打开 http://localhost:3000，默认用户名和密码都为 `admin`。

Grafana 服务默认通过 `NodePort` 暴露，如果 Kubernetes 集群支持负载均衡器，你可以修改为 `LoadBalancer`，然后通过负载均衡器访问面板。

## Kubernetes 的监控

随集群部署的 TiDB 监控只关注 TiDB 本身各组件的运行情况，并不包括对容器资源、宿主机、Kubernetes 组件和 TiDB Operator 等的监控。对于这些组件或资源的监控，需要在整个 Kubernetes 集群维度部署监控系统来实现。

### 宿主机监控

对宿主机及其资源的监控与传统的服务器物理资源监控相同。

如果在你的现有基础设施中已经有针对物理服务器的监控系统，只需要通过常规方法将 Kubernetes 所在的宿主机添加到现有监控系统中即可；如果没有可用的监控系统，或者希望部署一套独立的监控系统用于监控 Kubernetes 所在的宿主机，也可以使用你熟悉的任意监控系统。

新部署的监控系统可以运行于独立的服务器、直接运行于 Kubernetes 所在的宿主机，或运行于 Kubernetes 集群内，不同部署方式除在安装配置与资源利用上存在少许差异，在使用上并没有重大区别。

常见的可用于监控服务器资源的开源监控系统有：
 - CollectD
 - Nagios
 - Prometheus & node_exporter
 - Zabbix
 - ...

一些云服务商或专门的性能监控服务提供商也有各自的免费或收费的监控解决方案可以选择。

我们推荐通过 [Prometheus Operator](https://github.com/coreos/prometheus-operator) 在 Kubernetes 集群内部署基于 [Node Exporter](https://github.com/prometheus/node_exporter) 和 Prometheus 的宿主机监控系统，这一方案同时可以兼容并用于 Kubernetes 自身组件的监控。

### Kubernetes 组件监控

对 Kubernetes 组件的监控可以参考[官方文档](https://kubernetes.io/docs/tasks/debug-application-cluster/resource-usage-monitoring/)提供的方案，也可以使用其他兼容 Kubernetes 的监控系统来进行。

一些云服务商可能提供了自己的 Kubernetes 组件监控方案，一些专门的性能监控服务商也有各自的 Kubernetes 集成方案可以选择。

由于 TiDB Operator 实际上是运行于 Kubernetes 中的容器，选择任一可以覆盖对 Kubernetes 容器状态及资源进行监控的监控系统即可覆盖对 TiDB Operator 的监控，无需再额外部署监控组件。

我们推荐通过 [Prometheus Operator](https://github.com/coreos/prometheus-operator) 部署基于 [Node Exporter](https://github.com/prometheus/node_exporter) 和 Prometheus 的宿主机监控系统，这一方案同时可以兼容并用于对宿主机资源的监控。
