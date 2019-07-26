---
title: Local PV Configuration
summary: Learn how to manage local PV (Persistent Volume).
category: how-to
---

# Local PV Configuration

TiDB is a database with high availability. Data is stored and replicated on TiKV, the storage layer of TiDB, which can tolerate the inavailability of nodes. TiKV uses local storage with high IOPS and high throughput, such as Local SSDs, to enhance database capacity.

Kubernetes currently supports statically allocated local storage. To create a local storage object, use the `local-volume-provisioner` program in [local-static-provisioner](https://github.com/kubernetes-sigs/sig-storage-local-static-provisioner) project. The procedures are as follows:

1. Pre-allocate local storage in TiKV cluster nodes. See the [operation document](https://github.com/kubernetes-sigs/sig-storage-local-static-provisioner/blob/master/docs/operations.md) provided by Kubernetes for reference.

2. Install the `local-volume-provisioner` program. See the [Helm installation procedure](https://github.com/kubernetes-sigs/sig-storage-local-static-provisioner/tree/master/helm) for reference.

For more information, refer to [Kubernetes local storage](https://kubernetes.io/docs/concepts/storage/volumes/#local) and [local-static-provisioner document](https://github.com/kubernetes-sigs/sig-storage-local-static-provisioner#overview).
