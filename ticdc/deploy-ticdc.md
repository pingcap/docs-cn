---
title: TiCDC 集群部署运维
summary: 了解 TiCDC 软硬件环境要求以及如何部署运维 TiCDC。
---

# TiCDC 集群部署

本文档主要包括如下内容：

* 介绍 TiCDC 集群的软硬件环境要求。
* 使用 TiUP 部署运维 TiCDC 集群。

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

## 使用 TiUP 部署运维 TiCDC

TiCDC 支持基于 Kubernetes 环境部署，详情参考 [在 Kubernetes 上部署 TiCDC](https://docs.pingcap.com/zh/tidb-in-kubernetes/dev/deploy-ticdc)。

本文档主要介绍如何使用 TiUP 部署运维 TiCDC 集群，如有特殊情况也可以用 binary 部署。用户可以选择在部署新的 TiDB 集群时一起部署 TiCDC，也可以对原有 TiDB 集群新增 TiCDC 组件。

### 部署全新含有 TiCDC 组件的 TiDB 集群

在使用 TiUP 部署全新 TiDB 集群时，支持同时部署 TiCDC 组件。只需在 TiUP 启动 TiDB 集群时的配置文件中加入 `TiCDC` 部分即可，详细操作参考[编辑初始化配置文件](/production-deployment-using-tiup.md#第-3-步初始化集群拓扑文件)，具体可配置字段参考[通过 TiUP 配置 `cdc_servers`](/tiup/tiup-cluster-topology-reference.md#cdc_servers)。

### 在原有 TiDB 集群新增 TiCDC 组件

目前也支持在原有 TiDB 集群上使用 TiUP 新增 TiCDC 组件，操作步骤如下：

1. 首先确认当前 TiDB 的版本支持 TiCDC，否则需要先升级 TiDB 集群至 4.0.0 rc.1 或更新版本。TiCDC 在 4.0.6 版本已经 GA，建议使用 4.0.6 及以后的版本。

2. 参考[扩容 TiDB/TiKV/PD/TiCDC 节点](/scale-tidb-using-tiup.md#扩容-ticdc-节点)章节对 TiCDC 进行部署。

## 使用 binary 在原有 TiDB 集群上新增 TiCDC 组件（不推荐）

假设 PD 集群有一个可以提供服务的 PD 节点（client URL 为 `10.0.10.25:2379`）。若要部署三个 TiCDC 节点，可以按照以下命令启动集群。只需要指定相同的 PD 地址，新启动的节点就可以自动加入 TiCDC 集群。

{{< copyable "shell-regular" >}}

```shell
cdc server --cluster-id=default --pd=http://10.0.10.25:2379 --log-file=ticdc_1.log --addr=0.0.0.0:8301 --advertise-addr=127.0.0.1:8301
cdc server --cluster-id=default --pd=http://10.0.10.25:2379 --log-file=ticdc_2.log --addr=0.0.0.0:8302 --advertise-addr=127.0.0.1:8302
cdc server --cluster-id=default --pd=http://10.0.10.25:2379 --log-file=ticdc_3.log --addr=0.0.0.0:8303 --advertise-addr=127.0.0.1:8303
```

## TiCDC `cdc server` 命令行参数说明

对于 `cdc server` 命令中可用选项解释如下：

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
- `cluster-id`：TiCDC 集群的 ID。可选，默认值为 `default`。`cluster-id` 是 TiCDC 集群的唯一标识，拥有相同 `cluster-id` 的 TiCDC 节点同属一个集群。长度最大为 128，需要符合正则表达式 `^[a-zA-Z0-9]+(-[a-zA-Z0-9]+)*$`，且不能是以下值：`owner`，`capture`，`task`，`changefeed`，`job`，`meta`。


## 基于 TiUP 运维 TiCDC 集群

TiCDC 从 v6.3.0 版本开始在内部实现了支持滚动升级的能力。v1.11.0 及之后版本之后的 TiUP 使用了由 TiCDC 提供的 OpenAPI，在执行对 TiCDC 集群进行滚动升级，扩容 / 缩容操作时，同步延迟保持平稳。该功能要求如下:

* TiCDC 版本至少为 v6.3.0
* TiUP 版本至少为 v1.11.0
* TiCDC 集群中至少存在 2 个正在运行的实例

如果上述条件无法满足，将会强制执行相关操作，完成升级，扩缩容。

假设当前版本为 v6.3.0，使用 TiUP 升级集群到 v6.4.0 ：

{{< copyable "shell-regular" >}}
```shell
tiup cluster upgrade test-cluster v6.4.0
```

该操作在执行时对每一个 TiCDC 实例依次执行，将正在被升级的 TiCDC 实例上的工作负载表迁移到其他 TiCDC 实例上，然后执行下线节点，升级节点，上线新节点等操作。与之前版本的 TiCDC 升级过程相比，耗时变长，但是在升级过程中同步任务延迟不因为升级原因而上升，该功能同样被应用于缩容 TiCDC 节点的场景。

### TiUP 滚动升级部署有 TiCDC 的 TiDB 集群

运维升级 / 缩容一个 TiCDC 节点的耗时，和该节点上当前被分配的表同步任务数量相关，以及被连接的 regions 数量相关。表数量越多，regions 数量也就越多，迁移表耗时越长。TiUP 默认由 `--transfer-timeout` 参数控制该过程的时长，默认为 `600s`。如果在该时间范围内，TiCDC 节点上的表没能被完全迁移到其他节点上，那么执行强制升级 / 缩容操作，这种情况下不保证同步延迟。你可以根据当前集群中表的数量，在执行命令时设置修改该参数，保证每个节点滚动升级过程能够平稳执行。

我们的测试结果表明，升级 TiKV 的过程中，每秒平均迁移约 192 个 region leader 到其他 TiKV 节点；升级 TiCDC 的过程中，每秒平均迁移约 4 张表到其他节点，和当前集群写入流量有关。
