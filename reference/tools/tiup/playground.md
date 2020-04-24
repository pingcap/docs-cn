---
title: 本地快速部署 TiDB 集群
category: tools
---

# 本地快速部署 TiDB 集群

TiDB 集群是由多个组件构成的分布式系统，一个典型的 TiDB 集群至少由 3 个 PD 节点、3 个 TiKV 节点和 2 个 TiDB 节点构成。通过手工来部署这么多组件对于想要体验 TiDB 的用户甚至是 TiDB 的开发人员来说都是非常耗时且头疼的事情。在本节中，我们将介绍 TiUP 中的 playground 组件，并且将通过这个组件搭建起一套本地的 TiDB 测试环境。

## playground 组件介绍

playground 的基本用法：

```bash
tiup playground [version] [flags]
```

最朴素的启动命令 `tiup playground` 会使用本地安装的 TiDB/TiKV/PD 或它们的稳定版本启动一个 1 KV, 1 DB, 1 PD 的集群。这个命令实际上做了以下事情：
- 因为没有指定版本，TiUP 会先查找已安装的 playground 的最新版本，假设已安装的最新版为 v0.0.6，则该命令相当于 tiup playground:v0.0.6
- 如果 playground 组件从未安装过任何版本，TiUP 会先将其安装最新稳定版，然后再启动运行实例
- 因为 playground 没有指定 TiDB/PD/TiKV 各组件的版本，默认情况下，它会使用各组件的最新 release 版本，假设当前为 v4.0.0-rc，则该命令相当于 tiup playground:v0.0.6 v4.0.0-rc
- 因为 playground 也没有指定各组件的个数，默认情况下，它会启动由 1 个 TiDB、1 个 TiKV 和 1 个 PD 构成的最小化集群
- 在依次启动完各个组件后，playground 会告诉你启动成功，并告诉你一些有用的信息，譬如如何通过 MySQL 客户端连接集群、如何访问 dashboard

playground 的命令行参数说明：

```bash
Flags:
      --db int                   设置集群中的 TiDB 数量（默认为1）
      --db.binpath string        指定 TiDB 二进制文件的位置（开发调试用，可忽略）
      --db.config string         指定 TiDB 的配置文件（开发调试用，可忽略）
  -h, --help                     打印帮助信息
      --host string              设置每个组件的监听地址（默认为 127.0.0.1），如果要提供给别的电脑访问，可设置为 0.0.0.0
      --kv int                   设置集群中的 TiKV 数量（默认为1）
      --kv.binpath string        指定 TiKV 二进制文件的位置（开发调试用，可忽略）
      --kv.config string         指定 TiKV 的配置文件（开发调试用，可忽略）
      --monitor                  是否启动监控
      --pd int                   设置集群中的 PD 数量（默认为1）
      --pd.binpath string        指定 PD 二进制文件的位置（开发调试用，可忽略）
      --pd.config string         指定 PD 的配置文件（开发调试用，可忽略）
      --tiflash int              设置集群中 TiFlash 数量（默认为0）
      --tiflash.binpath string   指定 TiFlash 的二进制文件位置（开发调试用，可忽略）
      --tiflash.config string    指定 TiFlash 的配置文件（开发调试用，可忽略）
```

## 例子

### 使用每日构建版启动一个 TiDB 集群

{{< copyable "shell-regular" >}}

```shell
tiup playground nightly
```

nightly 就是这个集群的版本号，类似的可以 `tiup playground v4.0.0-rc` 等。

### 启动一个带监控的集群

{{< copyable "shell-regular" >}}

```shell
tiup playground nightly --monitor
```

该命令会在 9090 端口启动 prometheus 用于展示集群内部的时序数据。

### 覆盖 PD 的默认配置

复制 PD 的[配置模版](https://github.com/pingcap/pd/blob/master/conf/config.toml)，修改某些内容，然后执行：

{{< copyable "shell-regular" >}}

```shell
tiup playground --pd.config ~/config/pd.toml
```

> 这里假设将配置放置在 ~/config/pd.toml

### 替换默认的二进制文件

默认启动 playground 时，各个组件都是使用官方镜像组件包中的二进制文件启动的，如果本地编译了一个临时的二进制文件想要放入集群中测试，可以使用 --{comp}.binpath 这个 flag 替换，例如替换 TiDB 的二进制文件:

{{< copyable "shell-regular" >}}

```shell
tiup playground --db.binpath /xx/tidb-server 
```

### 启动多个组件实例

默认情况下 TiDB, TiKV 和 PD 各启动一个，如果希望启动多个，可以这样：

{{< copyable "shell-regular" >}}

```shell
tiup playground v3.0.10 --db 3 --pd 3 --kv 3
```