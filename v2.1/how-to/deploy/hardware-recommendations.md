---
title: TiDB 软件和硬件环境建议配置
category: how-to
---

# TiDB 软件和硬件环境建议配置

## 概述

TiDB 作为一款开源分布式 NewSQL 数据库，可以很好的部署和运行在 Intel 架构服务器环境及主流虚拟化环境，并支持绝大多数的主流硬件网络。作为一款高性能数据库系统，TiDB 支持主流的 Linux 操作系统环境。

## Linux 操作系统版本要求

| Linux 操作系统平台       | 版本         |
| :----------------------- | :----------: |
| Red Hat Enterprise Linux | 7.3 及以上   |
| CentOS                   | 7.3 及以上   |
| Oracle Enterprise Linux  | 7.3 及以上   |
| Ubuntu LTS               | 16.04 及以上 |

> **注意：**
>
> - TiDB 只支持 Red Hat 兼容内核 (RHCK) 的 Oracle Enterprise Linux，不支持 Oracle Enterprise Linux 提供的 Unbreakable Enterprise Kernel。
> - TiDB 在 CentOS 7.3 的环境下进行过大量的测试，同时社区也有很多该操作系统部署的最佳实践，因此，建议使用 CentOS 7.3 以上的 Linux 操作系统来部署 TiDB。
> - 以上 Linux 操作系统可运行在物理服务器以及 VMware、KVM、XEN 主流虚拟化环境上。

## 服务器建议配置

TiDB 支持部署和运行在 Intel x86-64 架构的 64 位通用硬件服务器平台。对于开发，测试，及生产环境的服务器硬件配置有以下要求和建议：

### 开发及测试环境

| **组件** | **CPU** | **内存** | **本地存储** | **网络** | **实例数量(最低要求)** |
| --- | --- | --- | --- | --- | --- |
| TiDB | 8核+ | 16 GB+ | 无特殊要求 | 千兆网卡 | 1（可与 PD 同机器） |
| PD | 4核+ | 8 GB+ | SAS, 200 GB+ | 千兆网卡 | 1（可与 TiDB 同机器） |
| TiKV | 8核+ | 32 GB+ | SSD, 200 GB+ | 千兆网卡 | 3 |

> **注意：**
>
> - 验证测试环境中的 TiDB 和 PD 可以部署在同一台服务器上。
> - 如进行性能相关的测试，避免采用低性能存储和网络硬件配置，防止对测试结果的正确性产生干扰。
> - 如果仅验证功能，建议使用 [Docker Compose 部署方案](/how-to/get-started/local-cluster/install-from-docker-compose.md)单机进行测试。
> - TiDB 对于磁盘的使用以存放日志为主，因此在测试环境中对于磁盘类型和容量并无特殊要求。

### 生产环境

| **组件** | **CPU** | **内存** | **硬盘类型** | **网络** | **实例数量(最低要求)** |
| --- | --- | --- | --- | --- | --- |
| TiDB | 16核+ | 32 GB+ | SAS | 万兆网卡（2块最佳） | 2 |
| PD | 4核+ | 8 GB+ | SSD | 万兆网卡（2块最佳） | 3 |
| TiKV | 16核+ | 32 GB+ | SSD | 万兆网卡（2块最佳） | 3 |
| 监控 | 8核+ | 16 GB+ | SAS | 千兆网卡 | 1 |

> **注意：**
>
> - 生产环境中的 TiDB 和 PD 可以部署和运行在同服务器上，如对性能和可靠性有更高的要求，应尽可能分开部署。
> - 生产环境强烈推荐使用更高的配置。
> - TiKV 硬盘大小配置建议 PCI-E SSD 不超过 2 TB，普通 SSD 不超过 1.5 TB。

## 网络要求

TiDB 作为开源分布式 NewSQL 数据库，其正常运行需要网络环境提供如下的网络端口配置要求，管理员可根据实际环境中 TiDB 组件部署的方案，在网络侧和主机侧开放相关端口：

| 组件 | 默认端口 | 说明 |
| :-- | :-- | :-- |
| TiDB |  4000  | 应用及 DBA 工具访问通信端口 |
| TiDB | 10080  | TiDB 状态信息上报通信端口 |
| TiKV |  20160 | TiKV 通信端口 |
| PD | 2379 | 提供 TiDB 和 PD 通信端口 |
| PD | 2380 | PD 集群节点间通信端口 |
| Pump | 8250 | Pump 通信端口 |
| Drainer | 8249 | Drainer 通信端口 |
| Prometheus |  9090 | Prometheus 服务通信端口 |
| Pushgateway |  9091 | TiDB，TiKV，PD 监控聚合和上报端口 |
| Node_exporter |  9100 | TiDB 集群每个节点的系统信息上报通信端口 |
| Blackbox_exporter | 9115 | Blackbox_exporter 通信端口，用于 TiDB 集群端口监控 |
| Grafana | 3000 | Web 监控服务对外服务和客户端(浏览器)访问端口 |
| Grafana | 8686 | grafana_collector 通信端口，用于将 Dashboard 导出为 PDF 格式 |
| Kafka_exporter | 9308 | Kafka_exporter 通信端口，用于监控 binlog kafka 集群 |

## 客户端 Web 浏览器要求

TiDB 提供了基于 [Grafana](https://grafana.com/) 的技术平台，对数据库集群的各项指标进行可视化展现。采用支持 Javascript 的微软 IE、Google Chrome、Mozilla Firefox 的较新版本即可访问监控入口。
