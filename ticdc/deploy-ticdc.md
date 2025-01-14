---
title: TiCDC 安装部署与集群运维
summary: 了解 TiCDC 软硬件环境要求以及如何安装部署和运维 TiCDC 集群。
---

# TiCDC 安装部署与集群运维

本文档介绍部署 TiCDC 集群的软硬件环境要求，如何安装部署 TiCDC 集群，以及如何对 TiCDC 集群进行运维操作。你可以选择在安装 TiDB 集群的同时部署 TiCDC，也可以对原有 TiDB 集群新增 TiCDC 组件。

## 软件和硬件环境推荐配置

在生产环境中，TiCDC 硬件配置推荐如下：

| CPU | 内存 | 硬盘               | 网络 | TiCDC 集群实例数量（生产环境最低要求） |
| --- | --- |------------------| --- | --- |
| 16 核+ | 64 GB+ | 500 GB+ SSD 类型硬盘 | 万兆网卡（2 块最佳） | 2 |

软件配置推荐及更多信息，参见 [TiDB 软件和硬件环境需求](/hardware-and-software-requirements.md)。

## 使用 TiUP 部署包含 TiCDC 组件的全新 TiDB 集群

在使用 TiUP 部署全新 TiDB 集群时，支持同时部署 TiCDC 组件。你需要在 TiUP 启动 TiDB 集群时的配置文件中加入 TiCDC 相关的部分，以下是一个示例：

```shell
cdc_servers:
  - host: 10.0.1.20
    gc-ttl: 86400
    data_dir: "/cdc-data"
  - host: 10.0.1.21
    gc-ttl: 86400
    data_dir: "/cdc-data"
```

更多参考：

- 详细配置参数，请参考[编辑初始化配置文件](/production-deployment-using-tiup.md#第-3-步初始化集群拓扑文件)。
- 具体可配置字段，请参考[通过 TiUP 配置 `cdc_servers`](/tiup/tiup-cluster-topology-reference.md#cdc_servers)。
- 部署集群的具体步骤，请参考[使用 TiUP 部署 TiDB 集群](/production-deployment-using-tiup.md)。

> **注意：**
>
> 在安装之前，请确认 TiUP 中控机与 TiCDC 目标主机的 [SSH 互信及 sudo 免密](/check-before-deployment.md#手动配置-ssh-互信及-sudo-免密码)已经完成配置。

## 使用 TiUP 在原有 TiDB 集群上新增或扩容 TiCDC 组件

扩容的方式与部署 TiCDC 集群的方式类似，推荐使用 TiUP 工具完成。

1. 编写一个名为 `scale-out.yml` 的配置文件，包含需要扩容的节点的配置信息。下面是一个示例：

    ```shell
    cdc_servers:
      - host: 10.1.1.1
        gc-ttl: 86400
        data_dir: /tidb-data/cdc-8300
      - host: 10.1.1.2
        gc-ttl: 86400
        data_dir: /tidb-data/cdc-8300
      - host: 10.0.1.4
        gc-ttl: 86400
        data_dir: /tidb-data/cdc-8300
    ```

2. 在 TiUP 中控机上执行类似下面的命令进行扩容：

    ```shell
    tiup cluster scale-out <cluster-name> scale-out.yml
    ```

更多用例说明，请参考[扩容 TiCDC 节点](/scale-tidb-using-tiup.md#扩容-ticdc-节点)。

## 使用 TiUP 在原有 TiDB 集群上移除或缩容 TiCDC 组件

推荐使用 TiUP 完成对 TiCDC 集群节点的缩容。使用类似下面的命令完成缩容:

```shell
tiup cluster scale-in <cluster-name> --node 10.0.1.4:8300
```

更多用例说明，请参考[缩容 TiCDC 节点](/scale-tidb-using-tiup.md#缩容-ticdc-节点)。

## 使用 TiUP 升级 TiCDC 集群

TiUP 支持升级 TiDB 集群，包括 TiCDC 组件。执行升级指令时，TiUP 会自动升级 TiCDC 组件，无需额外操作。操作示例如下：

```shell
tiup update --self && \
tiup update --all && \
tiup cluster upgrade <cluster-name> <version> --transfer-timeout 600
```

> **注意：**
>
> 命令中的 `<cluster-name>` 需要替换为集群名字，`<version>` 需要替换为目标版本号，例如 v8.5.1。

### 升级的注意事项

升级 TiCDC 集群时，需要注意以下事项：

- TiCDC v4.0.2 对 `changefeed` 的配置做了调整，请参阅[配置文件兼容注意事项](/ticdc/ticdc-compatibility.md#命令行参数和配置文件兼容性)。
- 升级期间遇到的问题及其解决办法，请参阅[使用 TiUP 升级 TiDB](/upgrade-tidb-using-tiup.md#4-升级-faq)。
- TiCDC 自 v6.3.0 起支持滚动升级，使用 TiUP 升级 TiCDC 节点期间，能够保证同步延迟稳定，不发生剧烈波动。满足以下条件将自动启用滚动升级：

    - TiCDC 版本大于等于 v6.3.0。
    - TiUP 版本大于等于 v1.11.3。
    - 集群中至少有两个正在运行的 TiCDC 实例。

## 使用 TiUP 变更 TiCDC 集群配置

本节介绍如何使用 TiUP 的 [`tiup cluster edit-config`](/tiup/tiup-component-cluster-edit-config.md) 命令来修改 TiCDC 的配置。在以下例子中，假设需要把 TiCDC 的 `gc-ttl` 从默认值 `86400` 修改为 `172800`，即 48 小时。

1. 执行 `tiup cluster edit-config` 命令，注意将 `<cluster-name>` 替换成实际的集群名：

    ```shell
    tiup cluster edit-config <cluster-name>
    ```

2. 在 vi 编辑器页面，修改 [`server-configs`](/tiup/tiup-cluster-topology-reference.md#server_configs) 下的 `cdc` 配置：

    ```shell
    server_configs:
      tidb: {}
      tikv: {}
      pd: {}
      tiflash: {}
      tiflash-learner: {}
      cdc:
        gc-ttl: 172800
    ```

    以上把 TiCDC 的 `gc-ttl` 的值设置为 48 小时。

3. 执行 `tiup cluster reload -R cdc` 命令重新加载配置。

## 使用 TiUP 终止和启动 TiCDC 节点

使用 TiUP 可以方便地终止和启动 TiCDC 节点，命令如下：

- 终止 TiCDC 节点：`tiup cluster stop -R cdc`
- 启动 TiCDC 节点：`tiup cluster start -R cdc`
- 重启 TiCDC 节点：`tiup cluster restart -R cdc`

## 使用加密传输 (TLS) 功能

请参阅[为 TiDB 组件间通信开启加密传输](/enable-tls-between-components.md)。

## 使用 TiCDC 命令行工具来查看集群状态

执行以下命令来查看 TiCDC 集群运行状态，注意需要将 `v<CLUSTER_VERSION>` 替换为 TiCDC 集群版本，例如 `v8.5.1`：

```shell
tiup cdc:v<CLUSTER_VERSION> cli capture list --server=http://10.0.10.25:8300
```

```shell
[
  {
    "id": "806e3a1b-0e31-477f-9dd6-f3f2c570abdd",
    "is-owner": true,
    "address": "127.0.0.1:8300",
    "cluster-id": "default"
  },
  {
    "id": "ea2a4203-56fe-43a6-b442-7b295f458ebc",
    "is-owner": false,
    "address": "127.0.0.1:8301",
    "cluster-id": "default"
  }
]
```

- `id`：表示服务进程的 ID。
- `is-owner`：表示该服务进程是否为 owner 节点。
- `address`：该服务进程对外提供接口的地址。
- `cluster-id`：该 TiCDC 的集群 ID，默认值为 `default`。
