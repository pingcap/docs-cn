---
title: TiDB 软件和硬件环境建议配置
aliases: ['/docs-cn/stable/hardware-and-software-requirements/','/docs-cn/v4.0/hardware-and-software-requirements/','/docs-cn/stable/how-to/deploy/hardware-recommendations/']
---

# TiDB 软件和硬件环境建议配置

TiDB 作为一款开源分布式 NewSQL 数据库，可以很好的部署和运行在 Intel 架构服务器环境、ARM 架构的服务器环境及主流虚拟化环境，并支持绝大多数的主流硬件网络。作为一款高性能数据库系统，TiDB 支持主流的 Linux 操作系统环境。

## Linux 操作系统版本要求

| Linux 操作系统平台       | 版本         |
| :----------------------- | :----------: |
| Red Hat Enterprise Linux | 7.3 及以上的 7.x 版本   |
| CentOS                   | 7.3 及以上的 7.x 版本   |
| Oracle Enterprise Linux  | 7.3 及以上的 7.x 版本   |
| Ubuntu LTS               | 16.04 及以上的 7.x 版本 |

> **注意：**
>
> - 目前尚不支持 Red Hat Enterprise Linux 8.0、CentOS 8 Stream 和 Oracle Enterprise Linux 8.0，因为目前对这些平台的测试还在进行中。
> - 不计划支持 CentOS 8 Linux，因为 CentOS 的上游支持将于 2021 年 12 月 31 日终止。
> - TiDB 将不再支持 Ubuntu 16.04。强烈建议升级到 Ubuntu 18.04 或更高版本。

其他 Linux 操作系统版本（例如 Debian Linux 和 Fedora Linux）也许可以运行 TiDB，但尚未得到 TiDB 官方支持。

## 软件配置要求

### 中控机软件配置

| 软件 | 版本 |
| :----------------------- | :----------: |
| sshpass | 1.06 及以上 |
| TiUP | 0.6.2 及以上 |

> **注意：**
>
> 中控机需要部署 [TiUP 软件](/tiup/tiup-documentation-guide.md)来完成 TiDB 集群运维管理。

### 目标主机建议配置软件

| 软件 | 版本 |
| :----- | :----------: |
| sshpass | 1.06 及以上 |
| numa | 2.0.12 及以上 |
| tar  | 任意      |

## 服务器建议配置

TiDB 支持部署和运行在 Intel x86-64 架构的 64 位通用硬件服务器平台或者 ARM 架构的硬件服务器平台。对于开发，测试，及生产环境的服务器硬件配置（不包含操作系统 OS 本身的占用）有以下要求和建议：

### 开发及测试环境

| **组件** | **CPU** | **内存** | **本地存储** | **网络** | **实例数量(最低要求)** |
| --- | --- | --- | --- | --- | --- |
| TiDB | 8 核+ | 16 GB+ | 无特殊要求 | 千兆网卡 | 1（可与 PD 同机器） |
| PD | 4 核+ | 8 GB+ | SAS, 200 GB+ | 千兆网卡 | 1（可与 TiDB 同机器） |
| TiKV | 8 核+ | 32 GB+ | SSD, 200 GB+ | 千兆网卡 | 3 |
| TiFlash | 32 核+ | 64 GB+ | SSD, 200 GB+ | 千兆网卡 | 1 |
| TiCDC | 8 核+ | 16 GB+ | SAS, 200 GB+ | 千兆网卡 | 1 |

> **注意：**
>
> - 验证测试环境中的 TiDB 和 PD 可以部署在同一台服务器上。
> - 如进行性能相关的测试，避免采用低性能存储和网络硬件配置，防止对测试结果的正确性产生干扰。
> - TiKV 的 SSD 盘推荐使用 NVME 接口以保证读写更快。
> - 如果仅验证功能，建议使用 [TiDB 数据库快速上手指南](/quick-start-with-tidb.md)进行单机功能测试。
> - TiDB 对于磁盘的使用以存放日志为主，因此在测试环境中对于磁盘类型和容量并无特殊要求。

### 生产环境

| **组件** | **CPU** | **内存** | **硬盘类型** | **网络** | **实例数量(最低要求)** |
| --- | --- | --- | --- | --- | --- |
| TiDB | 16 核+ | 32 GB+ | SAS | 万兆网卡（2 块最佳） | 2 |
| PD | 4核+ | 8 GB+ | SSD | 万兆网卡（2 块最佳） | 3 |
| TiKV | 16 核+ | 32 GB+ | SSD | 万兆网卡（2 块最佳） | 3 |
| TiFlash | 48 核+ | 128 GB+ | 1 or more SSDs | 万兆网卡（2 块最佳） | 2 |
| TiCDC | 16 核+ | 64 GB+ | SSD | 万兆网卡（2 块最佳） | 2 |
| 监控 | 8 核+ | 16 GB+ | SAS | 千兆网卡 | 1 |

> **注意：**
>
> - 生产环境中的 TiDB 和 PD 可以部署和运行在同服务器上，如对性能和可靠性有更高的要求，应尽可能分开部署。
> - 生产环境强烈推荐使用更高的配置。
> - TiKV 硬盘大小配置建议 PCI-E SSD 不超过 2 TB，普通 SSD 不超过 1.5 TB。
> - TiFlash 支持[多盘部署](/tiflash/tiflash-configuration.md#多盘部署)。
> - TiFlash 数据目录的第一块磁盘推荐用高性能 SSD 来缓冲 TiKV 同步数据的实时写入，该盘性能应不低于 TiKV 所使用的磁盘，比如 PCI-E SSD。并且该磁盘容量建议不小于总容量的 10%，否则它可能成为这个节点的能承载的数据量的瓶颈。而其他磁盘可以根据需求部署多块普通 SSD，当然更好的 PCI-E SSD 硬盘会带来更好的性能。
> - TiFlash 推荐与 TiKV 部署在不同节点，如果条件所限必须将 TiFlash 与 TiKV 部署在相同节点，则需要适当增加 CPU 核数和内存，且尽量将 TiFlash 与 TiKV 部署在不同的磁盘，以免互相干扰。
> - TiFlash 硬盘总容量大致为：`整个 TiKV 集群的需同步数据容量 / TiKV 副本数 * TiFlash 副本数`。例如整体 TiKV 的规划容量为 1 TB、TiKV 副本数为 3、TiFlash 副本数为 2，则 TiFlash 的推荐总容量为 `1024 GB / 3 * 2`。用户可以选择同步部分表数据而非全部，具体容量可以根据需要同步的表的数据量具体分析。
> - TiCDC 硬盘配置建议 200 GB+ PCIE-SSD。

## 网络要求

TiDB 作为开源分布式 NewSQL 数据库，其正常运行需要网络环境提供如下的网络端口配置要求，管理员可根据实际环境中 TiDB 组件部署的方案，在网络侧和主机侧开放相关端口：

| 组件 | 默认端口 | 说明 |
| :-- | :-- | :-- |
| TiDB |  4000  | 应用及 DBA 工具访问通信端口 |
| TiDB | 10080  | TiDB 状态信息上报通信端口 |
| TiKV |  20160 | TiKV 通信端口 |
| TiKV |  20180 | TiKV 状态信息上报通信端口 |
| PD | 2379 | 提供 TiDB 和 PD 通信端口 |
| PD | 2380 | PD 集群节点间通信端口 |
|TiFlash|9000|TiFlash TCP 服务端口|
|TiFlash|8123|TiFlash HTTP 服务端口|
|TiFlash|3930|TiFlash RAFT 服务和 Coprocessor 服务端口|
|TiFlash|20170|TiFlash Proxy 服务端口|
|TiFlash|20292|Prometheus 拉取 TiFlash Proxy metrics 端口|
|TiFlash|8234|Prometheus 拉取 TiFlash metrics 端口|
| Pump | 8250 | Pump 通信端口 |
| Drainer | 8249 | Drainer 通信端口 |
| CDC | 8300 | CDC 通信接口 |
| Prometheus | 9090 | Prometheus 服务通信端口 |
| Node_exporter | 9100 | TiDB 集群每个节点的系统信息上报通信端口 |
| Blackbox_exporter | 9115 | Blackbox_exporter 通信端口，用于 TiDB 集群端口监控 |
| Grafana | 3000 | Web 监控服务对外服务和客户端(浏览器)访问端口 |
| Alertmanager | 9093 | 告警 web 服务端口 |
| Alertmanager | 9094 | 告警通信端口 |

## 客户端 Web 浏览器要求

TiDB 提供了基于 [Grafana](https://grafana.com/) 的技术平台，对数据库集群的各项指标进行可视化展现。采用支持 Javascript 的微软 IE、Google Chrome、Mozilla Firefox 的较新版本即可访问监控入口。
