---
title: TiCDC 安装部署与集群运维
summary: 了解 TiCDC 软硬件环境要求以及如何安装部署 TiCDC。
---

# TiCDC 安装部署与集群运维

本文档介绍部署 TiCDC 集群的软硬件环境要求，如何安装部署 TiCDC 集群，如何对 TiCDC 集群进行运维操作。用户可以选择在安装 TiDB 集群时一起部署 TiCDC，也可以对原有 TiDB 集群新增 TiCDC 组件。

## 软件和硬件环境推荐配置

在生产环境中，TiCDC 的软件和硬件配置推荐如下：

| Linux 操作系统       | 版本         |
| :----------------------- | :----------: |
| Red Hat Enterprise Linux | 7.3 及以上   |
| CentOS                   | 7.3 及以上   |

| CPU | 内存 | 硬盘类型 | 网络 | TiCDC 集群实例数量（生产环境最低要求） |
| --- | --- | --- | --- | --- |
| 16 核+ | 64 GB+ | SSD | 万兆网卡（2 块最佳） | 2 |

更多信息参见 [TiDB 软件和硬件环境建议配置](/hardware-and-software-requirements.md)。

## 使用 TiUP 部署包含 TiCDC 组件的全新 TiDB 集群

在使用 TiUP 部署全新 TiDB 集群时，支持同时部署 TiCDC 组件。用户需要在 TiUP 启动 TiDB 集群时的配置文件中加入 TiCDC 相关的部分，以下是一个示例：

```
cdc_servers:
  - host: 10.0.1.20
    gc-ttl: 86400
    data_dir: "/cdc-data"
  - host: 10.0.1.21
    gc-ttl: 86400
    data_dir: "/cdc-data"
```

对于更详细的信息，参考[编辑初始化配置文件](/production-deployment-using-tiup.md#第-3-步初始化集群拓扑文件)，具体可配置字段参考[通过 TiUP 配置 `cdc_servers`](/tiup/tiup-cluster-topology-reference.md#cdc_servers)。部署集群的具体步骤可以参考[使用 TiUP 部署 TiDB 集群](/production-deployment-using-tiup.md)。另外，在安装之前，请确认TiUP 中控机与 TiCDC 目标主机的 [SSH 互信及 sudo 免密](/check-before-deployment.md#手动配置-ssh-互信及-sudo-免密码)已经完成配置。

## 使用 TiUP 在原有 TiDB 集群上新增或扩容 TiCDC 组件

目前也支持在原有 TiDB 集群上使用 TiUP 新增 TiCDC 组件，操作步骤如下：

1. 首先确认当前 TiDB 的版本支持 TiCDC，否则需要先升级 TiDB 集群至 4.0.0 rc.1 或更新版本。TiCDC 在 4.0.6 版本已经 GA，建议使用 4.0.6 及以后的版本。

2. 参考[扩容 TiDB/TiKV/PD/TiCDC 节点](/scale-tidb-using-tiup.md#扩容-ticdc-节点)章节对 TiCDC 进行部署。

## 使用 TiUP 在原有 TiDB 集群上移除或缩容 TiCDC 组件

## 使用 TiUP 升级 TiCDC 集群


TiCDC 从 v6.3.0 版本开始支持滚动升级，使用 TiUP 对 TiCDC 集群进行滚动升级，能够保证同步延迟稳定，不发生剧烈波动。该功能要求如下：

* 集群中至少有两个正在运行的 TiCDC 实例。
* TiUP 版本至少为 v1.11.0。

满足上述条件后，即可执行 `tiup cluster upgrade` 命令对集群进行滚动升级：

```shell
tiup cluster upgrade test-cluster ${target-version} --transfer-timeout 600
```

## 使用 TiUP 扩锁容 TiCDC 集群

## 使用 TiUP 终止和启动 TiCDC 节点

## 使用 TiUP 变更 TiCDC 集群配置



## 使用 TiUP 升级 TiCDC

本部分介绍如何使用 TiUP 来升级 TiCDC 集群。在以下例子中，假设需要将 TiCDC 组件和整个 TiDB 集群升级到 v6.3.0。

{{< copyable "shell-regular" >}}

```shell
tiup update --self && \
tiup update --all && \
tiup cluster upgrade <cluster-name> v6.3.0
```

### 升级的注意事项

* TiCDC v4.0.2 对 `changefeed` 的配置做了调整，请参阅[配置文件兼容注意事项](/ticdc/manage-ticdc.md#配置文件兼容性的注意事项)。
* 升级期间遇到的问题及其解决办法，请参阅[使用 TiUP 升级 TiDB](/upgrade-tidb-using-tiup.md#4-升级-faq)。

## 使用 TiUP 修改 TiCDC 配置

本节介绍如何使用 TiUP 的 [`tiup cluster edit-config`](/tiup/tiup-component-cluster-edit-config.md) 命令来修改 TiCDC 的配置。在以下例子中，假设需要把 TiCDC 的 `gc-ttl` 从默认值 `86400` 修改为 `3600`，即 1 小时。

首先执行以下命令。将 `<cluster-name>` 替换成实际的集群名。

{{< copyable "shell-regular" >}}

```shell
tiup cluster edit-config <cluster-name>
```

执行以上命令之后，进入到 vi 编辑器页面，修改 [`server-configs`](/tiup/tiup-cluster-topology-reference.md#server_configs) 下的 `cdc` 配置，如下所示：

```shell
 server_configs:
  tidb: {}
  tikv: {}
  pd: {}
  tiflash: {}
  tiflash-learner: {}
  pump: {}
  drainer: {}
  cdc:
    gc-ttl: 3600
```

修改完毕后执行 `tiup cluster reload -R cdc` 命令重新加载配置。

## 使用加密传输 (TLS) 功能

请参阅[为 TiDB 组件间通信开启加密传输](/enable-tls-between-components.md)。

## 使用 `cdc cli` 工具来管理集群状态和数据同步

本部分介绍如何使用 `cdc cli` 工具来管理集群状态和数据同步。`cdc cli` 是指通过 `cdc` binary 执行 `cli` 子命令。在以下描述中，通过 `cdc` binary 直接执行 `cli` 命令，TiCDC 的监听 IP 地址为 `10.0.10.25`，端口为 `8300`。

> **注意：**
>
> TiCDC 监听的 IP 和端口对应为 `cdc server` 启动时指定的 `--addr` 参数。从 TiCDC v6.2.0 开始，`cdc cli` 将通过 TiCDC 的 Open API 直接与 TiCDC server 进行交互，你可以使用 `--server` 参数指定 TiCDC 的 server 地址。`--pd` 参数将被废弃，不再推荐使用。

如果你使用的 TiCDC 是用 TiUP 部署的，需要将以下命令中的 `cdc cli` 替换为 `tiup ctl cdc`。

### 管理 TiCDC 服务进程 (`capture`)

- 查询 `capture` 列表：

    {{< copyable "shell-regular" >}}

    ```shell
    cdc cli capture list --server=http://10.0.10.25:8300
    ```

    ```
    [
      {
        "id": "806e3a1b-0e31-477f-9dd6-f3f2c570abdd",
        "is-owner": true,
        "address": "127.0.0.1:8300"
      },
      {
        "id": "ea2a4203-56fe-43a6-b442-7b295f458ebc",
        "is-owner": false,
        "address": "127.0.0.1:8301"
      }
    ]
    ```

    - `id`：服务进程的 ID。
    - `is-owner`：表示该服务进程是否为 owner 节点。
    - `address`：该服务进程对外提供接口的地址。
