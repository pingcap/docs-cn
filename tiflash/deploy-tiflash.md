---
title: 部署 TiFlash 集群
category: reference
aliases: ['/docs-cn/dev/reference/tiflash/deploy/']
---

# 部署 TiFlash 集群

> **注意：**
>
> 体验 TiFlash RC 版建议和 [PingCAP 官方](mailto:info@pingcap.com)联系，以获得更多资讯和辅助。

本文介绍了部署 TiFlash 集群的环境要求以及不同场景下的部署方式。

## 推荐硬件配置

本节根据不同的 TiFlash 部署模式给出了硬件配置建议。

### TiFlash 单独部署模式

* 最低配置：32 VCore, 64 GB RAM, 1 SSD + n HDD
* 推荐配置：48 VCore, 128 GB RAM, 1 NVMe SSD + n SSD

部署机器不限，最少一台即可。单台机器可以使用多盘，但不推荐单机多实例部署。

推荐用一个 SSD 盘来缓冲 TiKV 同步数据的实时写入，该盘性能不低于 TiKV 所使用的硬盘，建议是性能更好的 NVMe SSD。该 SSD 盘容量建议不小于总容量的 10%，否则它可能成为这个节点的能承载的数据量的瓶颈。而其他硬盘，可以选择部署多块 HDD 或者普通 SSD，当然更好的硬盘会带来更好的性能。

TiFlash 支持[多盘部署](/tiflash/tiflash-configuration.md#多盘部署)，所以无需使用 RAID。

### TiFlash 和 TiKV 部署在相同节点模式

参考 [TiKV 节点的硬件配置](/hardware-and-software-requirements.md#服务器建议配置)，并且适当增加内存和 CPU 核数。

建议不要将 TiFlash 与 TiKV 同盘部署，以防互相干扰。

硬盘选择标准同 [TiFlash 单独部署模式](#tiflash-单独部署模式)。硬盘总容量大致为：`整个 TiKV 集群的需同步数据容量 / TiKV 副本数 * TiFlash 副本数`。例如整体 TiKV 的规划容量为 1TB、TiKV 副本数为 3、TiFlash 副本数为 2，则 TiFlash 的推荐总容量为 `1024GB / 3 * 2`。用户可以选择同步部分表数据而非全部。

## 针对 TiDB 的版本要求

目前 TiFlash 的测试是基于 TiDB 4.0 版本的相关组件（包括 TiDB、PD、TiKV、TiFlash）来进行的，TiDB 4.0 版本的下载方式参考以下安装部署步骤。

## 安装部署 TiFlash

本节介绍了在不同场景下如何安装部署 TiFlash，包括以下场景：

- [全新部署 TiFlash](#全新部署-tiflash)
- [在原有 TiDB 集群上新增 TiFlash 组件](#在原有-tidb-集群上新增-tiflash-组件)

> **注意：**
>
> 1. 在开启 TiFlash 进程之前，必须确保 PD 的 Placement Rules 功能已开启（开启方法见[在原有 TiDB 集群上新增 TiFlash 组件](#在原有-tidb-集群上新增-tiflash-组件)一节的第 2 步）。
> 2. 在 TiFlash 运行期间，必须确保 PD 的 Placement Rules 功能保持开启状态。

### 全新部署 TiFlash

TiUP Cluster 是适用于 TiDB 4.0 及以上版本的部署工具，目前推荐使用 TiUP Cluster 安装部署 TiFlash，部署流程如下：

1. 参考 [TiUP 部署文档](/production-deployment-using-tiup.md)安装 TiUP。

2. 安装 TiUP cluster 组件

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster
    ```

3. 编写 topology 配置文件，保存为 `topology.yaml`。

    可以参考[全量的配置文件模版](https://github.com/pingcap-incubator/tiup-cluster/blob/master/examples/topology.example.yaml)。

    除了部署 TiDB 集群的配置，需要额外在 `tiflash_servers` 下配置 tiflash servers 所在的 ip（目前只支持 ip，不支持域名）。

    如果需要部署 TiFlash，请把 `pd` 部分的 `replication.enable-placement-rules` 配置设置为 `true`。

    {{< copyable "" >}}

    ```ini
    server_configs:
      pd:
        replication.enable-placement-rules: true

    pd_servers:
      - host: 172.19.0.101
      - host: 172.19.0.102
      - host: 172.19.0.103

    tidb_servers:
      - host: 172.19.0.101

    tikv_servers:
      - host: 172.19.0.101
      - host: 172.19.0.102
      - host: 172.19.0.103

    tiflash_servers:
      - host: 172.19.0.103
    ```

    如果希望自定义部署目录，需要配置 data_dir 参数，不需要则不加。如果希望[多盘部署](/tiflash/tiflash-configuration.md#多盘部署)，则以逗号分隔各部署目录，例如：

    {{< copyable "" >}}

    ```ini
    tiflash_servers:
      - host: 172.19.0.103
        data_dir: /data1/tiflash/data,/data2/tiflash/data
    ```

4. 按照 TiUP 部署流程完成集群部署的剩余步骤，包括：

    部署 TiDB 集群，其中 test 为集群名：

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster deploy test v4.0.0-rc topology.yaml  -i ~/.ssh/id_rsa
    ```

    启动 TiDB 集群：

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster start test
    ```

5. 查看集群状态

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster display test
    ```

### 在原有 TiDB 集群上新增 TiFlash 组件

1. 首先确认当前 TiDB 的版本支持 TiFlash，否则需要先升级 TiDB 集群至 4.0 rc 以上版本。

2. 在 pd-ctl（目前 pd-ctl 还没有接入 TiUP Cluster，需要从 [这里](https://download.pingcap.org/tidb-v4.0.0-rc-linux-amd64.tar.gz) 手动进行下载）中输入 `config set enable-placement-rules true` 命令，以开启 PD 的 Placement Rules 功能。

3. 参考 [扩容 TiFlash 节点](/scale-tidb-using-tiup.md#2-扩容-tiflash-节点) 章节对 TiFlash 进行部署。
