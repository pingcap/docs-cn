---
<<<<<<< HEAD
title: 部署运维 FAQ
summary: 介绍 TiDB 集群运维部署的常见问题、原因及解决方法。
=======
title: 安装部署 FAQ
summary: 介绍 TiDB 集群安装部署的常见问题、原因及解决方法。
aliases: ['/docs-cn/dev/faq/deploy-and-maintain-faq/']
>>>>>>> 774e5da07 (Optimize the FAQ TOC (#8602))
---

# 安装部署 FAQ

本文介绍 TiDB 集群安装部署的常见问题、原因及解决方法。

## 环境准备 FAQ

操作系统版本要求如下表：

| Linux 操作系统平台 | 版本 |
| :--- | :--- |
| Red Hat Enterprise Linux | 7.3 及以上 |
| CentOS | 7.3 及以上 |
| Oracle Enterprise Linux | 7.3 及以上 |

### 为什么要在 CentOS 7 上部署 TiDB 集群？

TiDB 作为一款开源分布式 NewSQL 数据库，可以很好的部署和运行在 Intel 架构服务器环境及主流虚拟化环境，并支持绝大多数的主流硬件网络，作为一款高性能数据库系统，TiDB 支持主流的 Linux 操作系统环境，具体可以参考 TiDB 的[官方部署要求](/hardware-and-software-requirements.md)。

其中 TiDB 在 CentOS 7.3 的环境下进行大量的测试，同时也有很多这个操作系统的部署最佳实践，因此，我们推荐客户在部署 TiDB 的时候使用 CentOS 7.3+ 以上的 Linux 操作系统。

## 硬件要求 FAQ

TiDB 支持部署和运行在 Intel x86-64 架构的 64 位通用硬件服务器平台。对于开发、测试、及生产环境的服务器硬件配置有以下要求和建议：

### 开发及测试环境

| **组件** | **CPU** | **内存** | **本地存储** | **网络** | **实例数量(最低要求)** |
| --- | --- | --- | --- | --- | --- |
| TiDB | 8核+ | 16 GB+ | SAS, 200 GB+ | 千兆网卡 | 1（可与 PD 同机器） |
| PD | 8核+ | 16 GB+ | SAS, 200 GB+ | 千兆网卡 | 1（可与 TiDB 同机器） |
| TiKV | 8核+ | 32 GB+ | SSD, 200 GB+ | 千兆网卡 | 3 |
|   |   |   |   | 服务器总计 | 4 |

### 生产环境

| **组件** | **CPU** | **内存** | **硬盘类型** | **网络** | **实例数量(最低要求)** |
| --- | --- | --- | --- | --- | --- |
| TiDB | 16核+ | 48 GB+ | SAS | 万兆网卡（2块最佳） | 2 |
| PD | 8核+ | 16 GB+ | SSD | 万兆网卡（2块最佳） | 3 |
| TiKV | 16核+ | 48 GB+ | SSD | 万兆网卡（2块最佳） | 3 |
| 监控 | 8核+ | 16 GB+ | SAS | 千兆网卡 | 1 |
|   |   |   |   | 服务器总计 | 9 |

### 两块网卡的目的是？万兆的目的是？

作为一个分布式集群，TiDB 对时间的要求还是比较高的，尤其是 PD 需要分发唯一的时间戳，如果 PD 时间不统一，如果有 PD 切换，将会等待更长的时间。两块网卡可以做 bond，保证数据传输的稳定，万兆可以保证数据传输的速度，千兆网卡容易出现瓶颈，我们强烈建议使用万兆网卡。

### SSD 不做 RAID 是否可行？

资源可接受的话，我们建议做 RAID 10，如果资源有限，也可以不做 RAID。

### TiDB 集群各个组件的配置推荐？

- TiDB 需要 CPU 和内存比较好的机器，参考官网配置要求，如果后期需要开启 TiDB Binlog，根据业务量的评估和 GC 时间的要求，也需要本地磁盘大一点，不要求 SSD 磁盘；
- PD 里面存了集群元信息，会有频繁的读写请求，对磁盘 I/O 要求相对比较高，磁盘太差会影响整个集群性能，推荐 SSD 磁盘，空间不用太大。另外集群 Region 数量越多对 CPU、内存的要求越高；
- TiKV 对 CPU、内存、磁盘要求都比较高，一定要用 SSD 磁盘。

详情可参考 [TiDB 软硬件环境需求](/hardware-and-software-requirements.md)。

## 安装部署 FAQ

如果用于生产环境，推荐使用 TiUP [使用 TiUP 部署](/production-deployment-using-tiup.md) TiDB 集群。

### 为什么修改了 TiKV/PD 的 toml 配置文件，却没有生效？

这种情况一般是因为没有使用 `--config` 参数来指定配置文件（目前只会出现在 binary 部署的场景），TiKV/PD 会按默认值来设置。如果要使用配置文件，请设置 TiKV/PD 的 `--config` 参数。对于 TiKV 组件，修改配置后重启服务即可；对于 PD 组件，只会在第一次启动时读取配置文件，之后可以使用 pd-ctl 的方式来修改配置，详情可参考 [PD 配置参数](/command-line-flags-for-pd-configuration.md)。

### TiDB 监控框架 Prometheus + Grafana 监控机器建议单独还是多台部署？

监控机建议单独部署。建议 CPU 8 core，内存 16 GB 以上，硬盘 500 GB 以上。

### 有一部分监控信息显示不出来？

查看访问监控的机器时间跟集群内机器的时间差，如果比较大，更正时间后即可显示正常。

### supervise/svc/svstat 服务具体起什么作用？

- supervise 守护进程
- svc 启停服务
- svstat 查看进程状态

### inventory.ini 变量参数解读

| **变量** | **含义** |
| --- | --- |
| cluster_name | 集群名称，可调整 |
| tidb_version | TiDB 版本 |
| deployment_method | 部署方式，默认为 binary，可选 docker |
| process_supervision | 进程监管方式，默认为 systemd，可选 supervise |
| timezone | 修改部署目标机器时区，默认为 Asia/Shanghai, 可调整，与set_timezone 变量结合使用 |
| set_timezone | 默认为 True，即修改部署目标机器时区，关闭可修改为 False |
| enable_elk | 目前不支持，请忽略 |
| enable_firewalld | 开启防火墙，默认不开启 |
| enable_ntpd | 检测部署目标机器 NTP 服务，默认为 True，请勿关闭 |
| machine_benchmark | 检测部署目标机器磁盘 IOPS，默认为 True，请勿关闭 |
| set_hostname | 根据 IP 修改部署目标机器主机名，默认为 False |
| enable_binlog | 是否部署 pump 并开启 binlog，默认为 False，依赖 Kafka 集群，参见 zookeeper_addrs 变量 |
| zookeeper_addrs | binlog Kafka 集群的 zookeeper 地址 |
| enable_slow_query_log | TiDB 慢查询日志记录到单独文件({{ deploy_dir }}/log/tidb_slow_query.log)，默认为 False，记录到 tidb 日志 |
| deploy_without_tidb | KV 模式，不部署 TiDB 服务，仅部署 PD、TiKV 及监控服务，请将 inventory.ini 文件中 tidb_servers 主机组 IP 设置为空。 |

### 如何单独记录 TiDB 中的慢查询日志，如何定位慢查询 SQL？

1. TiDB 中，对慢查询的定义在 TiDB 的配置文件中。`slow-threshold: 300`，这个参数是配置慢查询记录阈值的，单位是 ms。

2. 如果出现了慢查询，可以从 Grafana 监控定位到出现慢查询的 tidb-server 以及时间点，然后在对应节点查找日志中记录的 SQL 信息。

3. 除了日志，还可以通过 `admin show slow` 命令查看，详情可参考 [`admin show slow` 命令](/identify-slow-queries.md#admin-show-slow-命令)。

### 首次部署 TiDB 集群时，没有配置 tikv 的 Label 信息，在后续如何添加配置 Label？

TiDB 的 Label 设置是与集群的部署架构相关的，是集群部署中的重要内容，是 PD 进行全局管理和调度的依据。如果集群在初期部署过程中没有设置 Label，需要在后期对部署结构进行调整，就需要手动通过 PD 的管理工具 pd-ctl 来添加 location-labels 信息，例如：`config set location-labels "zone,rack,host"`（根据实际的 label 层级名字配置）。

pd-ctl 的使用参考 [PD Control 使用说明](/pd-control.md)。

### 为什么测试磁盘的 dd 命令用 `oflag=direct` 这个选项？

Direct 模式就是把写入请求直接封装成 I/O 指令发到磁盘，这样是为了绕开文件系统的缓存，可以直接测试磁盘的真实的 I/O 读写能力。

### 如何用 fio 命令测试 TiKV 实例的磁盘性能？

- 随机读测试：

    {{< copyable "shell-regular" >}}

    ```bash
    ./fio -ioengine=psync -bs=32k -fdatasync=1 -thread -rw=randread -size=10G -filename=fio_randread_test.txt -name='fio randread test' -iodepth=4 -runtime=60 -numjobs=4 -group_reporting --output-format=json --output=fio_randread_result.json
    ```

- 顺序写和随机读混合测试：

    {{< copyable "shell-regular" >}}

    ```bash
    ./fio -ioengine=psync -bs=32k -fdatasync=1 -thread -rw=randrw -percentage_random=100,0 -size=10G -filename=fio_randread_write_test.txt -name='fio mixed randread and sequential write test' -iodepth=4 -runtime=60 -numjobs=4 -group_reporting --output-format=json --output=fio_randread_write_test.json
    ```