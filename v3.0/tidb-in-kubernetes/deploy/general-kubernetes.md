---
title: Deploy TiDB on General Kubernetes
summary: Learn how to deploy a TiDB cluster on general Kubernetes.
category: how-to
aliases: ['/docs/v3.0/how-to/deploy/tidb-in-kubernetes/general-kubernetes/']
---

# Deploy TiDB on General Kubernetes

This document describes how to deploy a TiDB cluster on general Kubernetes.

## Prerequisites

- [Deploy TiDB Operator](tidb-in-kubernetes/deploy/tidb-operator.md);
- [Install Helm](tidb-in-kubernetes/reference/tools/in-kubernetes.md) and configure it with the official PingCAP chart.

## Configure TiDB cluster

Use the following commands to get the `values.yaml` configuration file of the tidb-cluster chart to be deployed.

{{< copyable "shell-regular" >}}

```shell
mkdir -p /home/tidb/<release-name> && \
helm inspect values pingcap/tidb-cluster --version=<chart-version> > /home/tidb/<release-name>/values-<release-name>.yaml
```

> **Note:**
>
> - You can replace `/home/tidb` with any directory as you like.
> - `release-name` is the prefix of resources used by TiDB in Kubernetes (such as Pod, Service, etc.). You can give it a name that is easy to memorize but this name must be *globally unique*. You can view existing `release-name`s in the cluster by running the `helm ls -q` command.
> - `chart-version` is the version released by the `tidb-cluster` chart. You can view the currently supported versions by running the `helm search -l tidb-cluster` command.
> - In the rest of this document, `values.yaml` refers to `/home/tidb/<release-name>/values-<releaseName>.yaml`.

Modify the configuratiuon above according to your needs. For more configuration details, refer to the [TiDB Cluster Configuration Document](/tidb-in-kubernetes/reference/configuration/tidb-cluster.md).

## Deploy TiDB Cluster

After you deploy and configure TiDB Operator, deploy the TiDB cluster using the following commands:

{{< copyable "shell-regular" >}}

``` shell
helm install pingcap/tidb-cluster --name=<release-name> --namespace=<namespace> --version=<chart-version> -f /home/tidb/<release-name>/values-<release-name>.yaml
```

You can view the Pod status using the following command:

{{< copyable "shell-regular" >}}

``` shell
kubectl get po -n <namespace> -l app.kubernetes.io/instance=<release-name>
```
