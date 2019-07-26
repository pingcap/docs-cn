---
title: Deploy TiDB on General Kubernetes
summary: Learn how to deploy a TiDB cluster on general Kubernetes.
category: how-to
---

# Deploy TiDB on General Kubernetes

This document describes how to deploy a TiDB cluster on general Kubernetes.

## Prerequisites

- [Deploy TiDB Operator](tidb-in-kubernetes/deploy/tidb-operator.md);
- [Install Helm](tidb-in-kubernetes/reference/tools/tools-in-kubernetes.md)  and configure it with the official PingCAP chart.

## Configure TiDB cluster

Use the following commands to get the `values.yaml` configuration file of the tidb-cluster chart to be deployed.

{{< copyable "shell-regular" >}}

```shell
mkdir -p /home/tidb/<releaseName> && \
helm inspect values pingcap/tidb-cluster --version=<chartVersion> > /home/tidb/<releaseName>/values-<releaseName>.yaml
```

> **Note:**
>
> You can replace `/home/tidb` with any directory as you like. In the rest of this document, `values.yaml` is used to refer to `/home/tidb/<releaseName>/values-<releaseName>.yaml`.

Modify the configuratiuon above according to your needs. For more configuration details, refer to the [TiDB Cluster Configuration Document](/tidb-in-kubernetes/reference/configuration/tidb-cluster.md)。

## Deploy TiDB Cluster

After you deploy and configure TiDB Operator, deploy the TiDB cluster using the following commands:

{{< copyable "shell-regular" >}}

``` shell
helm install pingcap/tidb-cluster --name=<releaseName> --namespace=<namespace> --version=<chartVersion> -f /home/tidb/<releaseName>/values-<releaseName>.yaml
```

You can view the Pod status using the following command:

{{< copyable "shell-regular" >}}

``` shell
kubectl get po -n <namespace> -l app.kubernetes.io/instance=<releaseName>
```