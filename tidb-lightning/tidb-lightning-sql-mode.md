---
title: TiDB Lightning Logical Import Mode 
---

# TiDB Lightning Logical Import Mode 

虽然 Physical Import Mode 具有高性能的优点，但由于其目前无法保证 ACID，且影响 TiDB 集群对外提供服务，因此一般建议仅用于 TiDB 集群初始化数据导入的场景。对于已有数据、对外提供服务的 TiDB 集群，推荐使用 Logical Import Mode 导入数据。Logical  Import Mode 的行为与正常执行 SQL 并无差异，可保证 ACID。

## TiDB Lightning Logical Import Mode 必要条件及限制

### 运行环境需求

**操作系统**：建议使用新的、纯净版 CentOS 7 实例，你可以在本地虚拟化一台主机，或在供应商提供的平台上部署一台小型的云虚拟主机。TiDB Lightning 运行过程中，默认会占满 CPU，建议单独部署在一台主机上。如果条件不允许，你可以将 TiDB Lightning 和其他组件（比如`tikv-server`）部署在同一台机器上，然后设置`region-concurrency` 配置项的值为逻辑 CPU 数的 75%，以限制 TiDB Lightning 对 CPU 资源的使用。

**内存和 CPU**：

建议使用 4 核以上的 CPU 和 8 GiB 以上内存以获得更好的性能。根据长期的实践经验，Lightning 的 Logical Import Mode 没有显著（5GiB 以上）的内存占用，但上调`region-concurrency`默认值将导致内存量增加。

**网络**：建议使用 1Gbps 或 10Gbps 以太网卡。

### 使用限制

- 使用多个 TiDB Lightning 向同一目标导入时，请勿混用不同的 backend，即不可同时使用 Physical Import Mode 和 Logical Import Mode 导入同一 TiDB 集群。