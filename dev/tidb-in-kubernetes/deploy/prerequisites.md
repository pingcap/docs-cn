---
title: Prerequisites for TiDB in Kubernetes
summary: Learn the prerequisites for TiDB in Kubernetes.
category: how-to
---

# Prerequisites for TiDB in Kubernetes

This document introduces the hardware and software prerequisites for deploying a TiDB cluster in Kubernetes.

## Software version

| Software Name | Version |
| :--- | :--- |
| Docker | Docker CE 18.09.6 |
| Kubernetes | v1.12.5+ |
| CentOS | 7.6 and kernel 3.10.0-957 or later |

## The configuration of kernel parameters

| Configuration Item | Value |
| :--- | :--- |
| net.core.somaxconn | 32768 |
| vm.swappiness | 0 |
| net.ipv4.tcp_syncookies | 1 |
| net.ipv4.ip_forward | 1 |
| fs.file-max | 1000000 |
| fs.inotify.max_user_watches | 1048576 |
| fs.inotify.max_user_instances | 1024 |
| net.ipv4.conf.all.rp_filter | 1 |
| net.ipv4.neigh.default.gc_thresh1 | 80000 |
| net.ipv4.neigh.default.gc_thresh2 | 90000 |
| net.ipv4.neigh.default.gc_thresh3 | 100000 |
| net.bridge.bridge-nf-call-iptables | 1 |
| net.bridge.bridge-nf-call-arptables | 1 |
| net.bridge.bridge-nf-call-ip6tables | 1 |

When you set `net.bridge.bridge-nf-call-*` parameters, and if your option reports an error, you can check whether this module is loaded by running the following command:

{{< copyable "shell-regular" >}}

```shell
lsmod|grep br_netfilter
```

If this module is not loaded, run the following command to load it:

{{< copyable "shell-regular" >}}

```shell
modprobe br_netfilter
```

You also need to disable swap on each deployed Kubernetes node by running:

{{< copyable "shell-regular" >}}

```shell
swapoff -a
```

To check whether swap is disabled:

{{< copyable "shell-regular" >}}

```shell
free -m
```

If the above command shows that the swap column is all `0`, then swap is disabled.

In addition, to permanently disable swaps, remove all the swap-related entries in `/etc/fstab`.

## Hardware and deployment requirements

+ 64-bit generic hardware server platform in the Intel x86-64 architecture and 10 Gigabit NIC (network interface card), which are the same as the server requirements for deploying a TiDB cluster using binary. For details, refer to [Hardware recommendations](/how-to/deploy/hardware-recommendations.md).

+ The server's disk, memory and CPU choices depend on the capacity planning of the cluster and the deployment topology. It is recommended to deploy three master nodes, three etcd nodes, and several worker nodes to ensure high availability of the online Kubernetes cluster.

  Meanwhile, the master node often acts as a worker node (that is, load can also be scheduled to the master node) to make full use of resources. You can set [reserved resources](https://kubernetes.io/docs/tasks/administer-cluster/reserve-compute-resources/) by kubelet to ensure that the system processes on the machine and the core processes of Kubernetes have sufficient resources to run under high workloads. This ensures the stability of the entire system.

The following text analyzes the deployment plan of three Kubernetes masters, three etcd and several worker nodes. To achieve a highly available deployment of multi-master nodes in Kubernetes, see [Kubernetes official documentation](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/high-availability/).

## Kubernetes requirements for system resources

- It is required on each machine to have a relatively large SAS disk (at least 1T) to store the data directories of Docker and kubelet.

    > **Note:**
    >
    > The data from Docker mainly includes image and container logs. The data from kubelet are mainly data used in [emptyDir](https://kubernetes.io/docs/concepts/storage/volumes/#emptydir).

- If you need to deploy a monitoring system for the Kubernetes cluster and store the monitoring data on the disk, consider preparing a large SAS disk for Prometheus and also for the log monitoring system. This is also to guarantee that the purchased machines are homogeneous. For this reason, it is recommended to prepare two large SAS disks for each machine.

    > **Note:**
    >
    > In a production environment, it is recommended to use RAID 5 for the two types of disks. You can decide how many disks for which you want to use RAID 5 as needed.

- It is recommended that the number of etcd nodes be consistent with that of the Kubernetes master nodes, and you store the etcd data on the SSD disk.

## TiDB cluster's requirements for resources

The TiDB cluster consists of three components: PD, TiKV and TiDB. The following recommendations on capacity planning is based on a standard TiDB cluster, namely three PDs, three TiKVs and two TiDBs:

- PD component: 2C 4GB. PD occupies relatively less resources and only a small portion of local disks.

    > **Note:**
    >
    > For easier management, you can put the PDs of all clusters on the master node. For example, to support five TiDB clusters, you can deploy five PD instances on each of the 3 master nodes. These PD instances use the same SSD disk (200 to 300 GigaBytes disk) on which you can create five directories as a mount point by means of bind mount. For detailed operation, refer to the [documentation](https://github.com/kubernetes-sigs/sig-storage-local-static-provisioner/blob/master/docs/operations.md#sharing-a-disk-filesystem-by-multiple-filesystem-pvs).
    >
    > If more machines are added to support more TiDB clusters, you can continue to add PD instances in this way on the master. If the resources on the master are exhausted, you can add PDs on other worker nodes in the same way. This method facilitates the planning and management of PD instances, while the downside is that if two machines go down, all TiDB clusters become unavailable due to the concentration of PD instances.
    >
    > Therefore, it is recommended to take out an SSD disk from each machine in all clusters and use it to provide PD instances like the master node. If you need to increase the capacity of a cluster by adding machines, you only need to create PD instances on the newly added machines.

- TiKV component: An NVMe disk of 8C 32GB for each TiKV instance. To deploy multiple TiKV instances on one machine, you must reserve enough buffers when planning capacity.

- TiDB component: 8C 32 GB capacity. Because the TiDB component does not occupy the disk space, you only need to consider the CPU and memory resources when planning. The following example assumes that the capacity is 8C 32 GB.

## A case of planning TiDB clusters

This is an example of deploying five clusters (each cluster has 3 PDs, 3 TiKVs, and 2 TiDBs), where PD is configured as 2C 4GB, TiDB as 8C 32GB, and TiKV as 8C 32GB. There are seven Kubernetes nodes, three of which are both master and worker nodes, and the other four are purely worker nodes. The distribution of each component is as follows:

+ Single master node:

    - 1 etcd (2C 4GB) + 2 PDs (2 \* 2C 2 \* 4GB) + 3 TiKVs (3 \* 8C 3 \* 32GB) + 1 TiDB (8C 32GB), totalling 38C 140GB
    - Two SSD disks, one for etcd and one for two PD instances
    - The RAID5-applied SAS disk used for Docker and kubelet
    - Three NVMe disks for TiKV instances

+ Single worker node:

    - 3 PDs (3 \* 2C 3 \* 4GB) + 2 TiKVs (2 \* 8C 2 \* 32GB) + 2 TiDBs (2 \* 8C 2 \* 32GB), totalling 38C 140GB
    - One SSD disk for three PD instances
    - The RAID5-applied SAS disk used for Docker and kubelet
    - Two NVMe disks for TiKV instances

From the above analysis, a total of seven physical machines are required to support five sets of TiDB clusters. Three of the machines are master and worker nodes, and the remaining four are worker nodes. The configuration requirements for the machines are as follows:

- master and worker node: 48C 192GB, two SSD disks, one RAID5-applied SAS disk, three NVMe disks
- worker node: 48C 192GB, one block SSD disk, one RAID5-applied SAS disk, two NVMe disks

The above recommended configuration leaves plenty of available resources in addition to those taken by the components. If you want to add the monitoring and log components, use the same method to plan and purchase the type of machines with specific configurations.

> **Note:**
>
> In a production environment, avoid deploying TiDB instances on a master node due to the NIC bandwidth. If the NIC of the master node works at full capacity, the heartbeat report between the worker node and the master node will be affected and might lead to serious problems.
