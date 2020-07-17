---
title: 部署 TiFlash 集群
aliases: ['/docs-cn/v3.1/reference/tiflash/deploy/']
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

目前 TiFlash 的测试是基于 TiDB 3.1 版本的相关组件（包括 TiDB、PD、TiKV、TiFlash）来进行的，TiDB 3.1 版本的下载方式参考以下安装部署步骤。

## 安装部署 TiFlash

本节介绍了在不同场景下如何安装部署 TiFlash，包括以下场景：

- [全新部署 TiFlash](#全新部署-tiflash)
- [在原有 TiDB 集群上新增 TiFlash 组件](#在原有-tidb-集群上新增-tiflash-组件)

> **注意：**
>
> 1. 在开启 TiFlash 进程之前，必须确保 PD 的 Placement Rules 功能已开启（开启方法见[在原有 TiDB 集群上新增 TiFlash 组件](#在原有-tidb-集群上新增-tiflash-组件)一节的第 2 步）。
> 2. 在 TiFlash 运行期间，必须确保 PD 的 Placement Rules 功能保持开启状态。

### 全新部署 TiFlash

目前对于全新部署 TiFlash 场景，推荐通过下载离线安装包来部署 TiFlash。步骤如下：

1. 下载 TiDB 3.1 版本对应 tag 的 TiDB Ansible：

    {{< copyable "shell-regular" >}}

    ```shell
    git clone -b $tag https://github.com/pingcap/tidb-ansible.git
    ```

2. 运行如下 `local prepare` 命令下载 TiDB、TiKV、PD 等组件的二进制文件：

    {{< copyable "shell-regular" >}}

    ```shell
    ansible-playbook local_prepare.yml
    ```

3. 编辑 `inventory.ini` 配置文件，除了[部署 TiDB 集群的配置](/online-deployment-using-ansible.md#第-9-步编辑-inventoryini-文件分配机器资源)，需要额外在 `[tiflash_servers]` 下配置 tiflash servers 所在的 ip (目前只支持 ip，不支持域名)。

    如果希望自定义部署目录，需要配置 `data_dir` 参数，不需要则不加。如果希望[多盘部署](/tiflash/tiflash-configuration.md#多盘部署)，则以逗号分隔各部署目录（注意每个 `data_dir` 目录的上级目录需要赋予 tidb 用户写权限），例如：

    {{< copyable "" >}}

    ```ini
    [tiflash_servers]
    192.168.1.1 data_dir=/data1/tiflash/data,/data2/tiflash/data
    ```

4. 按照 TiDB Ansible 部署流程完成集群部署的[剩余步骤](/online-deployment-using-ansible.md#第-10-步调整-inventoryini-文件中的变量)。

5. 验证 TiFlash 已部署成功的方式：通过 [pd-ctl](/pd-control.md)（tidb-ansible 目录下的 `resources/bin` 包含对应的二进制文件）执行 `pd-ctl store http://your-pd-address` 命令，可以观测到所部署的 TiFlash 实例状态为“Up”。

### 在原有 TiDB 集群上新增 TiFlash 组件

1. 首先确认当前 TiDB 的版本支持 TiFlash，否则需要先按照 [TiDB 升级操作指南](/upgrade-tidb-using-ansible.md)升级 TiDB 集群至 3.1 rc 以上版本。

2. 在 pd-ctl（tidb-ansible 目录下的 `resources/bin` 包含对应的二进制文件）中输入 `config set enable-placement-rules true` 命令，以开启 PD 的 Placement Rules 功能。

3. 编辑 `inventory.ini` 配置文件，并在 `[tiflash_servers]` 下配置 tiflash servers 所在的 ip（目前只支持 ip，不支持域名）。

    如果希望自定义部署目录，需要配置 `data_dir` 参数，不需要则不加。如果希望[多盘部署](/tiflash/tiflash-configuration.md#多盘部署)，则以逗号分隔各部署目录（注意每个 `data_dir` 目录的上级目录需要赋予 tidb 用户写权限），例如：

    {{< copyable "" >}}

    ```ini
    [tiflash_servers]
    192.168.1.1 data_dir=/data1/tiflash/data,/data2/tiflash/data
    ```

    > **注意：**
    >
    > 即使 TiFlash 与 TiKV 同机部署，TiFlash 也会采用与 TiKV 不同的默认端口，默认 9000，无特殊需要可以不用指定，有需要也可在 inventory.ini 配置文件中新增一行 `tcp_port=xxx` 来指定。

4. 执行以下 ansible-playbook 命令部署 TiFlash：

    {{< copyable "shell-regular" >}}

    ```shell
    ansible-playbook local_prepare.yml &&
    ansible-playbook -t tiflash deploy.yml &&
    ansible-playbook -t tiflash start.yml &&
    ansible-playbook rolling_update_monitor.yml
    ```

5. 验证 TiFlash 已部署成功的方式：通过 [pd-ctl](/pd-control.md) 执行 `pd-ctl store http://your-pd-address` 命令，可以观测到所部署的 TiFlash 实例状态为“Up”。
