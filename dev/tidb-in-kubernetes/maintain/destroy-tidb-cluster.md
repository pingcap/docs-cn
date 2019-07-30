---
title: Destroy TiDB Clusters in Kubernetes
summary: Learn how to delete TiDB Cluster in Kubernetes.
category: how-to
---

# Destroy TiDB Clusters in Kubernetes

This document describes how to deploy TiDB clusters in Kubernetes.

To destroy a TiDB cluster in Kubernetes, run the following commands:

{{< copyable "shell-regular" >}}

```shell
helm delete <releaseName> --purge
```

The above commands only removes the runining Pod with the data still retained. If you want the data to be deleted as well, you can use the following commands:

> **Warning:**
>
> The following commands deletes your data completely. Please be cautious.

{{< copyable "shell-regular" >}}

```shell
kubectl delete pvc -n <namespace> -l app.kubernetes.io/instance=<releaseName>,app.kubernetes.io/managed-by=tidb-operator
```

{{< copyable "shell-regular" >}}

```shell
kubectl get pv -l app.kubernetes.io/namespace=<namespace>,app.kubernetes.io/managed-by=tidb-operator,app.kubernetes.io/instance=<releaseName> -o name | xargs -I {} kubectl patch {} -p '{"spec":{"persistentVolumeReclaimPolicy":"Delete"}}'
```