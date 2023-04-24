---
title: TiCDC 安装部署
summary: 了解 TiCDC 软硬件环境要求以及如何安装部署 TiCDC。
---

# TiCDC 安装部署

本文档介绍 TiCDC 集群的软硬件环境要求，以及如何安装部署 TiCDC 集群。你可以选择随新集群一起部署 TiCDC，也可以对原有 TiDB 集群新增 TiCDC 组件。通常推荐使用 TiUP 完成部署，如有特殊情况也可以用 binary 部署。

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

在使用 TiUP 部署全新 TiDB 集群时，支持同时部署 TiCDC 组件。只需在 TiUP 启动 TiDB 集群时的配置文件中加入 `TiCDC` 部分即可，详细操作参考[编辑初始化配置文件](/production-deployment-using-tiup.md#第-3-步初始化集群拓扑文件)，具体可配置字段参考[通过 TiUP 配置 `cdc_servers`](/tiup/tiup-cluster-topology-reference.md#cdc_servers)。

## 使用 TiUP 在原有 TiDB 集群上新增 TiCDC 组件

目前也支持在原有 TiDB 集群上使用 TiUP 新增 TiCDC 组件，操作步骤如下：

1. 首先确认当前 TiDB 的版本支持 TiCDC，否则需要先升级 TiDB 集群至 4.0.0 rc.1 或更新版本。TiCDC 在 4.0.6 版本已经 GA，建议使用 4.0.6 及以后的版本。

2. 参考[扩容 TiDB/TiKV/PD/TiCDC 节点](/scale-tidb-using-tiup.md#扩容-ticdc-节点)章节对 TiCDC 进行部署。

## 使用 binary 在原有 TiDB 集群上新增 TiCDC 组件（不推荐）

假设 PD 集群有一个可以提供服务的 PD 节点（client URL 为 `10.0.10.25:2379`）。若要部署三个 TiCDC 节点，可以按照以下命令启动集群。只需要指定相同的 PD 地址，新启动的节点就可以自动加入 TiCDC 集群。

{{< copyable "shell-regular" >}}

```shell
cdc server --pd=http://10.0.10.25:2379 --log-file=ticdc_1.log --addr=0.0.0.0:8301 --advertise-addr=127.0.0.1:8301
cdc server --pd=http://10.0.10.25:2379 --log-file=ticdc_2.log --addr=0.0.0.0:8302 --advertise-addr=127.0.0.1:8302
cdc server --pd=http://10.0.10.25:2379 --log-file=ticdc_3.log --addr=0.0.0.0:8303 --advertise-addr=127.0.0.1:8303
```

## TiCDC `cdc server` 命令行参数说明

对于 `cdc server` 命令中可用选项解释如下：

<<<<<<< HEAD
- `addr`：TiCDC 的监听地址，提供服务的 HTTP API 查询地址和 Prometheus 查询地址，默认为 `127.0.0.1:8300`。
- `advertise-addr`：TiCDC 对外开放地址，供客户端访问。如果未设置该参数值，地址默认与 `addr` 相同。
- `pd`：TiCDC 监听的 PD 节点地址，用 `,` 来分隔多个 PD 节点地址。
- `config`：可选项，表示 TiCDC 使用的配置文件地址。TiCDC 从 v5.0.0 开始支持该选项，TiUP 从 v1.4.0 开始支持在部署 TiCDC 时使用该配置。
- `data-dir`：指定 TiCDC 使用磁盘储存文件时的目录。目前 Unified Sorter 会使用该目录储存临时文件，建议确保该目录所在设备的可用空间大于等于 500 GiB。更详细的说明参见 [Unified Sorter](/ticdc/manage-ticdc.md#unified-sorter-功能)。对于使用 TiUP 的用户，本选项可以通过配置 [`cdc_servers`](/tiup/tiup-cluster-topology-reference.md#cdc_servers) 中的 `data_dir` 来指定或默认使用 `global` 中 `data_dir` 路径。
- `gc-ttl`：TiCDC 在 PD 设置的服务级别 GC safepoint 的 TTL (Time To Live) 时长，和 TiCDC 同步任务所能够停滞的时长。单位为秒，默认值为 `86400`，即 24 小时。注意：TiCDC 同步任务的停滞会影响 TiCDC GC safepoint 的推进，即会影响上游 TiDB GC 的推进，详情可以参考 [TiCDC GC safepoint 的完整行为](/ticdc/ticdc-faq.md#ticdc-gc-safepoint-的完整行为是什么)。
- `log-file`：TiCDC 进程运行时日志的输出地址，未设置时默认为标准输出 (stdout)。
- `log-level`：TiCDC 进程运行时的日志级别，默认为 `"info"`。
- `ca`：TiCDC 创建 TLS 连接时使用的 CA 证书文件路径，PEM 格式，可选。
- `cert`：TiCDC 创建 TLS 连接时使用的证书文件路径，PEM 格式，可选。
- `cert-allowed-cn`：TiCDC 创建 TLS 连接时使用的通用名称文件路径，可选。
- `key`：TiCDC 创建 TLS 连接时使用的证书密钥文件路径，PEM 格式，可选。
- `tz`：TiCDC 服务使用的时区。TiCDC 在内部转换 `TIMESTAMP` 等时间数据类型和向下游同步数据时使用该时区，默认为进程运行本地时区。（注意如果同时指定 `tz` 参数和 `sink-uri` 中的 `time-zone` 参数，TiCDC 进程内部使用 `tz` 指定的时区，sink 向下游执行时使用 `time-zone` 指定的时区）
=======
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
      - host: 10.0.1.4:8300
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
> 命令中的 `<cluster-name>` 需要替换为集群名字，`<version>` 需要替换为目标版本号，例如 v7.0.0。

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
      pump: {}
      drainer: {}
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

执行以下命令来查看 TiCDC 集群运行状态，注意需要将 `v<CLUSTER_VERSION>` 替换为 TiCDC 集群版本，例如 `v6.5.0`：

```shell
tiup ctl:v<CLUSTER_VERSION> cdc capture list --server=http://10.0.10.25:8300
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
>>>>>>> 728ad25db (tiup: fix the scale-out yaml example (#13775))
