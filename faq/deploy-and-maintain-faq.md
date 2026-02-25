---
title: TiDB 安装部署常见问题
summary: 介绍 TiDB 集群安装部署的常见问题、原因及解决方法。
---

# TiDB 安装部署常见问题

本文介绍 TiDB 集群安装部署的常见问题、原因及解决方法。

## 软硬件要求 FAQ

### TiDB 支持哪些操作系统？

关于 TiDB 支持的操作系统，参见[操作系统及平台要求](/hardware-and-software-requirements.md#操作系统及平台要求)。

### TiDB 对开发、测试、生产环境的服务器硬件配置有什么要求？

TiDB 支持部署和运行在 Intel x86-64 架构的 64 位通用硬件服务器平台。对于开发、测试、生产环境的服务器硬件配置，参见[服务器配置要求](/hardware-and-software-requirements.md#服务器配置要求)。

### 两块网卡的目的是？万兆的目的是？

作为一个分布式集群，TiDB 对时间的要求还是比较高的，尤其是 PD 需要分发唯一的时间戳，如果 PD 时间不统一，如果有 PD 切换，将会等待更长的时间。两块网卡可以做 bond，保证数据传输的稳定，万兆可以保证数据传输的速度，千兆网卡容易出现瓶颈，我们强烈建议使用万兆网卡。

### SSD 不做 RAID 是否可行？

资源可接受的话，我们建议做 RAID 10，如果资源有限，也可以不做 RAID。

### TiDB 集群各个组件的配置推荐？

- TiDB 需要 CPU 和内存比较好的机器，参考官网配置要求；
- PD 里面存了集群元信息，会有频繁的读写请求，对磁盘 I/O 要求相对比较高，磁盘太差会影响整个集群性能，推荐 SSD 磁盘，空间不用太大。另外集群 Region 数量越多对 CPU、内存的要求越高；
- TiKV 对 CPU、内存、磁盘要求都比较高，一定要用 SSD 磁盘。

详情可参考 [TiDB 软硬件环境需求](/hardware-and-software-requirements.md)。

## 安装部署 FAQ

如果用于生产环境，推荐[使用 TiUP 部署](/production-deployment-using-tiup.md) TiDB 集群。

### 为什么修改了 TiKV/PD 的 toml 配置文件，却没有生效？

这种情况一般是因为没有使用 `--config` 参数来指定配置文件（目前只会出现在 binary 部署的场景），TiKV/PD 会按默认值来设置。如果要使用配置文件，请设置 TiKV/PD 的 `--config` 参数。对于 TiKV 组件，修改配置后重启服务即可；对于 PD 组件，只会在第一次启动时读取配置文件，之后可以使用 pd-ctl 的方式来修改配置，详情可参考 [PD 配置参数](/command-line-flags-for-pd-configuration.md)。

### TiDB 监控框架 Prometheus + Grafana 监控机器建议单独还是多台部署？

监控机建议单独部署。建议 CPU 8 core，内存 16 GB 以上，硬盘 500 GB 以上。

### 有一部分监控信息显示不出来？

查看访问监控的机器时间跟集群内机器的时间差，如果比较大，更正时间后即可显示正常。

### 如何单独记录 TiDB 中的慢查询日志，如何定位慢查询 SQL？

1. TiDB 中，对慢查询的定义在 TiDB 的配置文件中。`tidb_slow_log_threshold: 300`，这个参数是配置慢查询记录阈值的，单位是 ms。

2. 如果出现了慢查询，可以从 Grafana 监控定位到出现慢查询的 tidb-server 以及时间点，然后在对应节点查找日志中记录的 SQL 信息。

3. 除了日志，还可以通过 `ADMIN SHOW SLOW` 命令查看，详情可参考 [`ADMIN SHOW SLOW` 命令](/identify-slow-queries.md#admin-show-slow-命令)。

### 首次部署 TiDB 集群时，没有配置 tikv 的 Label 信息，在后续如何添加配置 Label？

TiDB 的 Label 设置是与集群的部署架构相关的，是集群部署中的重要内容，是 PD 进行全局管理和调度的依据。如果集群在初期部署过程中没有设置 Label，需要在后期对部署结构进行调整，就需要手动通过 PD 的管理工具 pd-ctl 来添加 location-labels 信息，例如：`config set location-labels "zone,rack,host"`（根据实际的 label 层级名字配置）。

pd-ctl 的使用参考 [PD Control 使用说明](/pd-control.md)。

### 为什么测试磁盘的 dd 命令用 `oflag=direct` 这个选项？

Direct 模式就是把写入请求直接封装成 I/O 指令发到磁盘，这样是为了绕开文件系统的缓存，可以直接测试磁盘的真实的 I/O 读写能力。

### 如何用 fio 命令测试 TiKV 实例的磁盘性能？

以下示例使用 `ioengine=psync`（即同步 I/O），因此 `iodepth` 通常固定为 `1`，并发主要由 `numjobs` 控制。建议使用 `direct=1` 以绕过文件系统缓存。

- 随机读测试：

    ```bash
    ./fio -ioengine=psync -bs=32k -direct=1 -thread -rw=randread -time_based -size=10G -filename=fio_randread_test.txt -name='fio randread test' -iodepth=1 -runtime=60 -numjobs=4 -group_reporting --output-format=json --output=fio_randread_result.json
    ```

- 顺序写和随机读混合测试：

    ```bash
    ./fio -ioengine=psync -bs=32k -direct=1 -thread -rw=randrw -percentage_random=100,0 -time_based -size=10G -filename=fio_randread_write_test.txt -name='fio mixed randread and sequential write test' -iodepth=1 -runtime=60 -numjobs=4 -group_reporting --output-format=json --output=fio_randread_write_test.json
    ```

## TiDB 支持在公有云上部署吗？

TiDB 支持在以下云上部署：

- [Google Cloud GKE](https://docs.pingcap.com/zh/tidb-in-kubernetes/stable/deploy-on-gcp-gke/)
- [AWS EKS](https://docs.pingcap.com/zh/tidb-in-kubernetes/stable/deploy-on-aws-eks/)
- [Azure AKS](https://docs.pingcap.com/zh/tidb-in-kubernetes/stable/deploy-on-azure-aks/)
- [阿里云 ACK](https://docs.pingcap.com/zh/tidb-in-kubernetes/v1.5/deploy-on-alibaba-cloud/)

此外，TiDB 云上部署也已在京东云、UCloud 上线。
