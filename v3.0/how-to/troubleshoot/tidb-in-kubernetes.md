---
title: Kubernetes 上的 TiDB 集群故障诊断
category: how-to
---

# Kubernetes 上的 TiDB 集群故障诊断

本文介绍 Kubernetes 上的 TiDB 集群的一些常见故障以及如何诊断解决。

## 集群意外删除后恢复

TiDB Operator 使用 PV (Persistent Volume)/PVC (Persistent Volume Claim) 来存储持久化的数据，如果不小心使用 `helm delete` 意外删除了集群，PV/PVC 对象以及数据都会保留下来，以最大程度保证数据安全。

此时集群恢复的办法就是使用 `helm install` 命令来创建一个同名的集群，之前保留下来未被删除的 PV/PVC 以及数据会被复用：

{{< copyable "shell-regular" >}}

```shell
helm install pingcap/tidb-cluster -n ${releaseName} --namespace=${namespace} --version=v1.0.0-beta.3 -f values.yaml
```
