---
title: Kubernetes 上的 TiDB 集群环境需求
category: how-to
---
# Kubernetes 上的 TiDB 集群环境需求

## 软件版本要求

| 软件名称 | 版本 |
| --- | --- |
| Docker | Docker CE 18.09.6 |
| Kubernetes |  v1.12.2 |
| CentOS |  7.6 and kernel 3.10.0-957 or later |

## 内核参数设置

| 配置项 | 设置值 |
| --- | --- |
| net.core.somaxconn | 32768 |
| vm.swappiness | 0 |
| net.ipv4.tcp_syncookies | 1 |
| net.ipv4.ip_forward | 1 |
| fs.file-max | 1000000 |
| fs.inotify.max_user_watches | 1048576 |
| fs.inotify.max_user_instances | 1024 |
| net.ipv4.neigh.default.gc_thresh1 | 80000 |
| net.ipv4.neigh.default.gc_thresh2 | 90000 |
| net.ipv4.neigh.default.gc_thresh3 | 100000 |
| net.bridge.bridge-nf-call-iptables | 1 |
| net.bridge.bridge-nf-call-arptables | 1 |
| net.bridge.bridge-nf-call-ip6tables | 1 |

在设置 `net.bridge.bridge-nf-call-*` 这几项参数时如果报选项不存在错误，通过如下命令检查是否已经加载改模块：

{{< copyable "shell-regular" >}}

```shell
lsmod|grep br_netfilter
```

如果没有加载则执行如下命令加载：

{{< copyable "shell-regular" >}}

```shell
modprobe br_netfilter
```

同时还需要关闭每个部署 Kubernetes 节点的 swap，执行命令如下：

{{< copyable "shell-regular" >}}

```shell
swapofff -a
```

执行如下命令检查 swap 是否已经关闭：

{{< copyable "shell-regular" >}}

```shell
## 执行命令后输出显示 swap 一列全是 0 则表明 swap 已经关闭
free -m
```

同时为了永久性地关闭 swap，还应该将 `/etc/fstab` 中 swap 相关的条目全部删除。

## 硬件和部署要求

与部署 TiDB binary 集群的服务器要求一致，选用 Intel x86-64 架构的 64 位通用硬件服务器，使用万兆网卡。关于 TiDB 集群在物理机上的具体部署需求，参考[这里](https://github.com/pingcap/docs-cn/blob/master/dev/how-to/deploy/hardware-recommendations.md)。

对于服务器 disk、memory、CPU 的选择要根据对集群的容量规划以及部署拓扑来定。线上 Kubernetes 集群部署为了保证高可用一般需要部署三个 master 节点，三个 etcd 节点，若干个 work 节点。同时，为了充分利用机器资源，master 节点一般也充当 work 节点（也就是 master 节点上也可以调度负载），通过 kubelet 设置[预留资源](https://kubernetes.io/docs/tasks/administer-cluster/reserve-compute-resources/) 来保证机器上的系统进程以及 Kubernetes 的核心进程在工作负载很高的情况下仍然有足够的资源来运行，从而保证整个系统的稳定。

下面按 3 Kubernetes master + 3 etcd + 若干 work 节点部署方案分析。Kubernetes 的多 master 节点高可用部署参考[官方文档](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/high-availability/)。

## Kubernetes 系统资源要求

1. 每个机器上的需要一块比较大的 SAS 盘(至少 1T)，这块盘用来存 docker 和 kubelet 的数据目录，docker 的数据主要包括镜像和容器日志数据，kubelet 主要占盘的数据是 [emptyDir](https://kubernetes.io/docs/concepts/storage/volumes/#emptydir) 所使用的数据。
2. 如果需要部署 Kubernetes 集群的监控系统, 且监控数据需要落盘，则也需要考虑为 Prometheus 准备一块 SAS 盘，后面日志监控系统也需要大的 SAS 盘，同时考虑到机器采购最好是同构的这一因素，因此每台机器最好有两块大的 SAS 盘。生产环境建议给这两种类型的盘做 RAID5，至于使用多少块来做 RAID5 可自己决定。
3. etcd 的分布建议是和 k8s master 节点保持一致，也就是多少个 master 节点就部署多少个 etcd 节点，etcd 数据建议使用 SSD 盘存放。

## tidb 集群资源需求

TiDB 集群由 PD、TiKV、TiDB 三个组件组成，在做容量规划的时候一般按照可以支持多少套 TiDB 集群来算。这里按照标准的 tidb 集群 3个 PD + 3 个 TiKV + 2 个 TiDB 来算，下面是对每个组件规划的一种建议：

1. PD 组件。PD 占用资源较少，这种集群规模下分配 2C 4GB 即可，占用少量本地盘，为了便于管理，我们可以将所有集群的 PD 都放在 master 节点，比如需要支持 5 套 TiDB 集群，则可以规划三个 master 节点上每个支持部署 5 个 PD 实例，5 个 PD 实例使用同一块 SSD 盘即可（两三百 GB 的盘即可），通过 bind mount 的方式在这块 SSD 上创建 5 个目录作为挂载点，操作方式见 [文档](https://github.com/kubernetes-sigs/sig-storage-local-static-provisioner/blob/master/docs/operations.md#sharing-a-disk-filesystem-by-multiple-filesystem-pvs)。如果后面集群添加了更多的机器需要支持更多的 TiDB 集群时，可以在 master 上用这种方式继续增加 PD 实例，如果 master 上资源耗尽可以找其它的 work 节点机器用同样的方式添加 PD 实例，这种方式的好处就是方便规划和管理 PD 实例，坏处就是由于 PD 实例过于集中，这些机器中如果有两台宕机会导致所有的 TiDB 集群不可用。因此这里建议从所有集群里面的机器都拿出一块 SSD 盘像 master 节点一样提供 PD 实例。比如总共 7 台机器，要支持 7 套 TiDB 标准集群的情况下，则需要每台机器上都能支持部署3个 PD 实例，如果后续有集群需要通过扩容机器增加容量，也只需要在新的机器上创建 PD 实例。
2. TiKV 组件，TiKV 组件的性能因为很依赖磁盘 I/O 且数据量一般较大，因此这里建议每个 TiKV 实例独占一块 NVMe 的盘，资源配置为 8C 32GB，如果想要在一个机器上支持部署 多个 TiKV 实例，则参考这些参数去选择合适的机器，同时在规划容量的时候应当预留出足够的 buffer。
3. TiDB 组件，TiDB 组件因为不占用磁盘，因此在规划的时候只需要考虑其占用的 cpu 和 内存资源即可，这里我们也按 8C 32 GB 的容量来计算。

## TiDB 集群规划例子

通过上面的分析，这里给出一个支持部署 5 套规模为 3个 PD + 3 个 TiKV + 2 个 TiDB 集群的例子，其中 PD 配置为 2C 4GB，TiDB 配置为 8C 32GB，TiKV 配置为 8C 32GB。 k8s 节点有 7 个，其中三个节点既是 master 又是 work 节点，另外三个是纯 work 节点。下面是各组件分布情况。

单个 master 节点:

* 1 etcd(2C 4GB) + 2 PD (2 \* 2C 2 \* 4GB) + 3 TiKV(3 \* 8C 3 \* 32GB) + 1 TiDB (8C 32GB)  总共是  38C 140GB
* 两块 SSD 盘，一块给 etcd，另外一块给 2 个 PD 实例
* 做了 RAID5 的 SAS 盘，给 docker 和 kubelet 做数据盘
* 三块 NVMe 盘给 TiKV 实例

单个 work 节点：

* 3 PD (3 \* 2C 3 \* 4GB) + 2 TiKV (2 \* 8C 2 \* 32GB) + 2 TiDB (2 \* 8C 2 \* 32GB)  总共是 38C 140GB
* 一块 SSD 盘给三个 PD 实例
* 做了 RAID5 的 SAS 盘，给 Docker 和 kubelet 做数据盘
* 两块 NVMe 盘给 TiKV 实例

从上面的分析来看要支持 5 套 tidb 集群容量共需要 7 台物理机，其中三台为 master 兼 work 节点，其余四台为 work 节点，机器配置需求如下。

master 兼 work 节点：

* 48C 192GB  2 块 SSD 盘，一块做了 RAID5 的 SAS 盘，三块 NVMe 盘

work 节点：

* 48C 192GB 1 块 SSD 盘，一块做了 RAID5 的 SAS 盘，两块 NVMe 盘

上面的机器配置刨去各个组件占用的资源还有比较多的预留资源，如果在考虑到加监控和日志组件，用同样的方法去规划需要采购的机器类型以及配置。另外在生产环境的使用上尽量不要在 master 节点部署 TiDB 实例或者尽可能少的部署 TiDB 实例，这里的主要考虑点是网卡带宽，因为如果 master 节点网卡打满会影响到 work 节点和 master 节点之间的心跳汇报信息，导致比较严重的问题。
