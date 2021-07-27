---
title: TiCDC 安装部署
summary: 了解 TiCDC 软硬件环境要求以及如何安装部署 TiCDC。
---

# TiCDC 安装部署

本文档介绍 TiCDC 集群的软硬件环境要求，以及如何安装部署 TiCDC 集群。你可以选择随新集群一起部署 TiCDC，也可以对原有 TiDB 集群新增 TiCDC 组件。通常推荐使用 TiUP 完成部署，如有特殊情况也可以用 binary 部署。

## 软件和硬件环境推荐配置

在生产环境中，TiCDC 的软件和硬件配置推荐如下：

| Linux 操作系统平台       | 版本         |
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

- `gc-ttl`：TiCDC 在 PD 设置的服务级别 GC safepoint 的 TTL (Time To Live) 时长，单位为秒，默认值为 `86400`，即 24 小时。
- `pd`：PD client 的 URL。
- `addr`：TiCDC 的监听地址，提供服务的 HTTP API 查询地址和 Prometheus 查询地址。
- `advertise-addr`：TiCDC 对外访问地址。
- `tz`：TiCDC 服务使用的时区。TiCDC 在内部转换 timestamp 等时间数据类型和向下游同步数据时使用该时区，默认为进程运行本地时区。（注意如果同时指定 `tz` 参数和 `sink-uri` 中的 `time-zone` 参数，TiCDC 进程内部使用 `tz` 指定的时区，sink 向下游执行时使用 `time-zone` 指定的时区）
- `log-file`：TiCDC 进程运行日志的地址，默认为 `cdc.log`。
- `log-level`：TiCDC 进程运行时默认的日志级别，默认为 `info`。
- `ca`：TiCDC 使用的 CA 证书文件路径，PEM 格式，可选。
- `cert`：TiCDC 使用的证书文件路径，PEM 格式，可选。
- `key`：TiCDC 使用的证书密钥文件路径，PEM 格式，可选。
- `config`：可选项，表示 TiCDC 使用的配置文件地址。TiCDC 从 v5.0.0 开始支持该选项，TiUP 从 v1.4.0 开始支持在部署 TiCDC 时使用该配置。
- `sort-dir`：指定排序引擎使用的临时文件目录。该配置项的默认值为 `/tmp/sorter`。在开启 Unified Sorter 的情况下，如果服务器的该目录不可写或可用空间不足，请手动指定 `sort-dir`。需确保 TiCDC 在该 `sort-dir` 路径下可读写数据。从 v4.0.14 和 v5.0.3 开始，该参数将不起作用，推荐使用 `data-dir` 参数启动 TiCDC。
- `data-dir`：指定 TiCDC 运行过程中使用的临时文件目录，从 v4.0.14 和 v5.0.3 开始支持。推荐在启动 TiCDC 时指定该参数，建议其所在磁盘至少有 500GB 的可用空间。如果启动时未指定该参数，将会参考已有 changefeed 的 `sort-dir` 设置情况初始化该参数，默认值为 `/tmp/cdc_data`。在运行过程中，如果 `data-dir` 所在磁盘可用磁盘空间不足 10%, 运行在该 TiCDC server 上的 changefeed 将会报错并停止运行，用户需要重新设置 `data-dir` 所在磁盘, 在至少保证有 10% 可用空间之后，手动重启相关 changefeed。排序引擎使用的临时文件目录，即 `sort-dir`，会被设置为 `{data-dir}/tmp/sorter`。
