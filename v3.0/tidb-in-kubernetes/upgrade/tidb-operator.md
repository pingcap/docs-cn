---
title: 升级 TiDB Operator
category: how-to
aliases: ['/docs-cn/v3.0/how-to/upgrade/tidb-operator/']
---

# 升级 TiDB Operator

本文介绍如何升级 TiDB Operator。升级 TiDB Operator 和自定义 TiDB Operator 类似，修改 `values.yaml` 中的镜像版本，然后执行 `helm upgrade`：

{{< copyable "shell-regular" >}}

```shell
helm upgrade tidb-operator pingcap/tidb-operator --version=<chartVersion> -f /home/tidb/tidb-operator/values-tidb-operator.yaml
```

当新版本 tidb-operator 发布，只要更新 `values.yaml` 中的 `operatorImage` 然后执行上述命令就可以。但是安全起见，最好从新版本 `tidb-operator` chart 中获取新版本 `values.yaml` 并和旧版本 `values.yaml` 合并生成新的 `values.yaml`，然后升级。

TiDB Operator 是用来管理 TiDB 集群的，也就是说，如果 TiDB 集群已经启动并正常运行，你甚至可以停掉 TiDB Operator，而 TiDB 集群仍然能正常工作，直到你需要维护 TiDB 集群，比如伸缩、升级等等。

## 升级 Kubernetes

当你的 Kubernetes 集群有版本升级，请确保 `kubeSchedulerImageTag` 与之匹配。默认情况下，这个值是由 Helm 在安装或者升级过程中生成的，要修改它你需要执行 `helm upgrade`。
