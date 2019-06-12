---
title: 集群意外删除后恢复
category: troubleshooting
---

# 集群意外删除后恢复

TiDB Operator 使用 PV/PVC 来存储持久化的数据，如果不小心使用 helm delete 意外删除集群后，PV/PVC 对象以及数据都会保留下来，以最大程度保证数据安全。

此时集群恢复的办法就是使用 helm install 命令来创建一个同名的集群，之前保留下来未被删除的 PV/PVC 以及数据会被复用：

```shell
helm install charts/tidb-cluster -n ${releaseName} --namespace=${namespace}
```