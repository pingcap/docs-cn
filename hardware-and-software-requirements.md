---
title: TiDB 软件和硬件环境建议配置
aliases: ['/docs-cn/dev/hardware-and-software-requirements/','/docs-cn/dev/how-to/deploy/hardware-recommendations/']
---

# TiDB 软件和硬件环境建议配置

<!-- Localization note for TiDB:

- 英文：用 distributed SQL，同时开始强调 HTAP
- 中文：可以保留 NewSQL 字眼，同时强调一栈式实时 HTAP
- 日文：NewSQL 认可度高，用 NewSQL

-->

TiDB 作为一款开源一栈式实时 HTAP 数据库，可以很好地部署和运行在 Intel 架构服务器环境、ARM 架构的服务器环境及主流虚拟化环境，并支持绝大多数的主流硬件网络。作为一款高性能数据库系统，TiDB 支持主流的 Linux 操作系统环境。

## 操作系统及平台要求

|  操作系统   |   支持的 CPU 架构   |
|   :---   |   :---   |
| Red Hat Enterprise Linux 8.4 及以上的 8.x 版本  |  <ul><li>x86_64</li><li>ARM 64</li></ul>  |
| <ul><li>Red Hat Enterprise Linux 7.3 及以上的 7.x 版本</li><li>CentOS 7.3 及以上的 7.x 版本</li></ul>  |  <ul><li>x86_64</li><li>ARM 64</li></ul>   |
|  Amazon Linux 2         |  <ul><li>x86_64</li><li>ARM 64</li></ul>   |
|  Rocky Linux 9.1 及以上的版本 |  <ul><li>x86_64</li><li>ARM 64</li></ul> |
| 麒麟欧拉版 V10 SP1/SP2   |   <ul><li>x86_64</li><li>ARM 64</li></ul>   |
| 统信操作系统 (UOS) V20                 |   <ul><li>x86_64</li><li>ARM 64</li></ul>   |
| openEuler 22.03 LTS SP1 |   <ul><li>x86_64</li><li>ARM 64</li></ul>   |
| macOS 12 (Monterey) 及以上的版本 |  <ul><li>x86_64</li><li>ARM 64</li></ul>  |
|  Oracle Enterprise Linux 8 及以上的版本  |  x86_64           |
|   Ubuntu LTS 20.04 及以上的版本  |  x86_64           |
| CentOS 8 Stream | <ul><li>x86_64</li><li>ARM 64</li></ul> |
|  Debian 10 (Buster) 及以上的版本  |  x86_64           |
|  Fedora 38 及以上的版本   |  x86_64           |
|  openSUSE Leap 15.5 以上的版本（不包含 Tumbleweed） |  x86_64           |
|  SUSE Linux Enterprise Server 15  |  x86_64                        |

> **注意：**
>
> - TiDB 只支持 Red Hat 兼容内核 (RHCK) 的 Oracle Enterprise Linux，不支持 Oracle Enterprise Linux 提供的 Unbreakable Enterprise Kernel。
> - 根据 [CentOS Linux EOL](https://www.centos.org/centos-linux-eol/)，CentOS Linux 8 的上游支持已于 2021 年 12 月 31 日终止，但 CentOS 将继续提供对 CentOS Stream 8 的支持。
> - TiDB 将不再支持 Ubuntu 16.04。强烈建议升级到 Ubuntu 18.04 或更高版本。
> - 对于以上表格中所列操作系统的 32 位版本，TiDB 在这些 32 位操作系统以及对应的 CPU 架构上**不保障**可编译、可构建以及可部署，或 TiDB 不主动适配这些 32 位的操作系统。
> - 以上未提及的操作系统版本**也许可以**运行 TiDB，但尚未得到 TiDB 官方支持。

### 编译和运行 TiDB 所依赖的库

|  编译和构建 TiDB 所需的依赖库   |  版本   |
|   :---   |   :---   |
|   Golang  |  1.21 及以上版本  |
|   Rust    |   nightly-2022-07-31 及以上版本  |
|  GCC      |   7.x      |
|  LLVM     |  13.0 及以上版本  |

运行时所需的依赖库：glibc（2.28-151.el8 版本）

### Docker 镜像依赖

支持的 CPU 架构如下：

- x86_64，从 TiDB v6.6.0 开始，需要 [x86-64-v2 指令集](https://developers.redhat.com/blog/2021/01/05/building-red-hat-enterprise-linux-9-for-the-x86-64-v2-microarchitecture-level)
- ARM 64

## 软件配置要求

### 中控机软件配置

| 软件 | 版本 |
| :----------------------- | :----------: |
| sshpass | 1.06 及以上 |
| TiUP | 1.5.0 及以上 |

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

TiDB 支持部署和运行在 Intel x86-64 架构的 64 位通用硬件服务器平台或者 ARM 架构的硬件服务器平台。对于开发、测试及生产环境的服务器硬件配置（不包含操作系统 OS 本身的占用）有以下要求和建议：

### 开发及测试环境

| **组件** | **CPU** | **内存** | **本地存储** | **网络** | **实例数量(最低要求)** |
| --- | --- | --- | --- | --- | --- |
| TiDB | 8 核+ | 16 GB+ | [磁盘空间要求](#磁盘空间要求) | 千兆网卡 | 1（可与 PD 同机器） |
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
> - 从 v6.3.0 开始，在 Linux AMD64 架构的硬件平台部署 TiFlash 时，CPU 必须支持 AVX2 指令集。确保命令 `cat /proc/cpuinfo | grep avx2` 有输出。而在 Linux ARM64 架构的硬件平台部署 TiFlash 时，CPU 必须支持 ARMv8 架构。确保命令 `cat /proc/cpuinfo | grep 'crc32' | grep 'asimd'` 有输出。通过使用向量扩展指令集，TiFlash 的向量化引擎能提供更好的性能。

### 生产环境

| **组件** | **CPU** | **内存** | **硬盘类型** | **网络** | **实例数量(最低要求)** |
| --- | --- | --- | --- | --- | --- |
| TiDB | 16 核+ | 48 GB+ | SSD | 万兆网卡（2 块最佳） | 2 |
| PD | 8 核+ | 16 GB+ | SSD | 万兆网卡（2 块最佳） | 3 |
| TiKV | 16 核+ | 64 GB+ | SSD | 万兆网卡（2 块最佳） | 3 |
| TiFlash | 48 核+ | 128 GB+ | 1 or more SSDs | 万兆网卡（2 块最佳） | 2 |
| TiCDC | 16 核+ | 64 GB+ | SSD | 万兆网卡（2 块最佳） | 2 |
| 监控 | 8 核+ | 16 GB+ | SAS | 千兆网卡 | 1 |

> **注意：**
>
> - 生产环境中的 TiDB 和 PD 可以部署和运行在同一台服务器上，如对性能和可靠性有更高的要求，应尽可能分开部署。
> - 强烈建议分别为生产环境中的 TiDB、TiKV 和 TiFlash 配置至少 8 核的 CPU。强烈推荐使用更高的配置，以获得更好的性能。
> - TiKV 硬盘大小配置建议 PCIe SSD 不超过 4 TB，普通 SSD 不超过 1.5 TB。
> - TiFlash 支持[多盘部署](/tiflash/tiflash-configuration.md#多盘部署)。
> - TiFlash 数据目录的第一块磁盘推荐用高性能 SSD 来缓冲 TiKV 同步数据的实时写入，该盘性能应不低于 TiKV 所使用的磁盘，比如 PCIe SSD。并且该磁盘容量建议不小于总容量的 10%，否则它可能成为这个节点的能承载的数据量的瓶颈。而其他磁盘可以根据需求部署多块普通 SSD，当然更好的 PCIe SSD 硬盘会带来更好的性能。
> - TiFlash 推荐与 TiKV 部署在不同节点，如果条件所限必须将 TiFlash 与 TiKV 部署在相同节点，则需要适当增加 CPU 核数和内存，且尽量将 TiFlash 与 TiKV 部署在不同的磁盘，以免互相干扰。
> - TiFlash 硬盘总容量大致为：`整个 TiKV 集群的需同步数据容量 / TiKV 副本数 * TiFlash 副本数`。例如整体 TiKV 的规划容量为 1 TB、TiKV 副本数为 3、TiFlash 副本数为 2，则 TiFlash 的推荐总容量为 `1024 GB / 3 * 2`。用户可以选择同步部分表数据而非全部，具体容量可以根据需要同步的表的数据量具体分析。
> - TiCDC 硬盘配置建议 500 GB+ PCIe SSD。

## 网络要求

<!-- Localization note for TiDB:

- 英文：用 distributed SQL，同时开始强调 HTAP
- 中文：可以保留 NewSQL 字眼，同时强调一栈式实时 HTAP
- 日文：NewSQL 认可度高，用 NewSQL

-->

TiDB 作为开源一栈式实时 HTAP 数据库，其正常运行需要网络环境提供如下的网络端口配置要求，管理员可根据实际环境中 TiDB 组件部署的方案，在网络侧和主机侧开放相关端口：

| 组件 | 默认端口 | 说明 |
| :-- | :-- | :-- |
| TiDB |  4000  | 应用及 DBA 工具访问通信端口 |
| TiDB | 10080  | TiDB 状态信息上报通信端口 |
| TiKV |  20160 | TiKV 通信端口 |
| TiKV |  20180 | TiKV 状态信息上报通信端口 |
| PD | 2379 | 提供 TiDB 和 PD 通信端口 |
| PD | 2380 | PD 集群节点间通信端口 |
|TiFlash|9000|TiFlash TCP 服务端口|
|TiFlash|3930|TiFlash RAFT 服务和 Coprocessor 服务端口|
|TiFlash|20170|TiFlash Proxy 服务端口|
|TiFlash|20292|Prometheus 拉取 TiFlash Proxy metrics 端口|
|TiFlash|8234|Prometheus 拉取 TiFlash metrics 端口|
| Pump | 8250 | Pump 通信端口 |
| Drainer | 8249 | Drainer 通信端口 |
| CDC | 8300 | CDC 通信接口 |
| Monitoring | 9090 | Prometheus 服务通信端口 |
| Monitoring | 12020 | NgMonitoring 服务通信端口 |
| Node_exporter | 9100 | TiDB 集群每个节点的系统信息上报通信端口 |
| Blackbox_exporter | 9115 | Blackbox_exporter 通信端口，用于 TiDB 集群端口监控 |
| Grafana | 3000 | Web 监控服务对外服务和客户端(浏览器)访问端口 |
| Alertmanager | 9093 | 告警 web 服务端口 |
| Alertmanager | 9094 | 告警通信端口 |

## 磁盘空间要求

| 组件 | 磁盘空间要求 | 健康水位使用率 |
| :-- | :-- | :-- |
| TiDB | <ul><li>日志盘建议最少预留 30 GB。</li> <li>v6.5.0 及以上版本默认启用了 Fast Online DDL 对添加索引等 DDL 操作进行加速（通过变量 [`tidb_ddl_enable_fast_reorg`](/system-variables.md#tidb_ddl_enable_fast_reorg-从-v630-版本开始引入) 控制）。如果业务中可能存在针对大对象的 DDL 操作，或需要使用 [<code>IMPORT INTO</code>](/sql-statements/sql-statement-import-into.md) SQL 语句导入数据，推荐为 TiDB 准备额外的 SSD 磁盘空间（建议 100 GB+）。配置方式详见[设置 TiDB 节点的临时空间](/check-before-deployment.md#设置-tidb-节点的临时空间推荐)。</li></ul>| 低于 90% |
| PD | 数据盘和日志盘建议最少各预留 20 GB | 低于 90% |
| TiKV | 数据盘和日志盘建议最少各预留 100 GB | 低于 80% |
| TiFlash | 数据盘建议最少预留 100 GB，日志盘建议最少预留 30 GB | 低于 80% |
| TiUP | <ul><li>中控机：部署一个版本的 TiDB 集群占用不超过 1 GB 空间，部署多个版本集群所占用的空间会相应增加 </li> <li>部署服务器（实际运行 TiDB 各组件的机器）：TiFlash 占用约 700 MB 空间，其他组件（PD、TiDB、TiKV 等）各占用约 200 MB 空间。同时，部署过程会占用小于 1 MB 临时空间（/tmp）存放临时文件 </li></ul> | 不涉及|
| Ngmonitoring | <ul><li>Conprof：3 x 1 GB x 组件数量（表示每个组件每天占用约 1 GB，总共 3 天） + 20 GB 预留空间 </li><li> Top SQL：30 x 50 MB x 组件数量（每个组件每天占用约 50 MB，总共 30 天） </li><li> Top SQL 和 Conprof 共享预留空间</li></ul> | 不涉及 |

## 客户端 Web 浏览器要求

TiDB 提供了基于 [Grafana](https://grafana.com/) 的技术平台，对数据库集群的各项指标进行可视化展现。采用支持 Javascript 的微软 Edge、Apple Safari、Google Chrome、Mozilla Firefox 的较新版本即可访问监控入口。

## TiFlash 存算分离架构的软硬件要求

上面的 TiFlash 软硬件要求是针对存算一体架构的。从 v7.0.0 开始，TiFlash 支持[存算分离架构](/tiflash/tiflash-disaggregated-and-s3.md)，该架构下 TiFlash 分为 Write Node 和 Compute Node 两个角色，对应的软硬件要求如下：

- 软件：与存算一体架构一致，详见[操作系统及平台要求](#操作系统及平台要求)。
- 网络端口：与存算一体架构一致，详见[网络要求](#网络要求)。
- 磁盘空间：
    - TiFlash Write Node：推荐 200 GB+，用作增加 TiFlash 副本、Region 副本迁移时向 Amazon S3 上传数据前的本地缓冲区。此外，还需要一个与 Amazon S3 兼容的对象存储。
    - TiFlash Compute Node：推荐 100 GB+，主要用于缓存从 Write Node 读取的数据以提升性能。Compute Node 的缓存可能会被完全使用，这是正常现象。
- CPU 以及内存等要求参考下文。

### 开发及测试环境

| 组件 | CPU | 内存 | 本地存储 | 网络 | 实例数量（最低要求） |
| --- | --- | --- | --- | --- | --- |
| TiFlash Write Node | 16 核+ | 32 GB+ | SSD, 200 GB+ | 千兆网卡 | 1 |
| TiFlash Compute Node | 16 核+ | 32 GB+ | SSD, 100 GB+ | 千兆网卡 | 0（参见下文“注意”说明） |

### 生产环境

| 组件 | CPU | 内存 | 硬盘类型 | 网络 | 实例数量（最低要求） |
| --- | --- | --- | --- | --- | --- |
| TiFlash Write Node | 32 核+ | 64 GB+ | SSD, 200 GB+ | 万兆网卡（2 块最佳） | 2 |
| TiFlash Compute Node | 32 核+ | 64 GB+ | SSD, 100 GB+  | 万兆网卡（2 块最佳） | 0（参见下文“注意”说明） |

> **注意：**
>
> TiFlash Compute Node 可以使用 TiUP 等部署工具快速扩缩容，扩缩容范围是 `[0, +inf]`。
