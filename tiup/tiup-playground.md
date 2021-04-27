---
title: 本地快速部署 TiDB 集群
---

# 本地快速部署 TiDB 集群

TiDB 集群是由多个组件构成的分布式系统，一个典型的 TiDB 集群至少由 3 个 PD 节点、3 个 TiKV 节点和 2 个 TiDB 节点构成。对于想要快速体验 TiDB 的用户来说，手工部署这么多组件是非常耗时且麻烦的事情。本文介绍 TiUP 中的 playground 组件，以及如何通过 playground 组件快速搭建一套本地的 TiDB 测试环境。

## playground 组件介绍

playground 组件的基本用法：

```bash
tiup playground [version] [flags]
```

如果直接执行 `tiup playground` 命令，则 TiUP playground 会使用本地安装的 TiDB/TiKV/PD 组件或者安装这些组件的稳定版本，来启动一个由 1 个 TiKV、1 个 TiDB、1 个 PD 实例构成的集群。该命令实际做了以下事情：

- 因为该命令没有指定 playground 的版本，TiUP 会先查找已安装的 playground 的最新版本，假设已安装的 playground 最新版为 v1.3.0，则该命令相当于 tiup playground:v1.3.0
- 如果 playground 从未安装过任何版本的 TiDB/TiKV/PD 组件，TiUP 会先安装这些组件的最新稳定版，然后再启动运行这些组件的实例
- 因为该命令没有指定 TiDB/PD/TiKV 各组件的版本，默认情况下，它会使用各组件的最新发布版本，假设当前为 v5.0.0，则该命令相当于 tiup playground:1.3.0 v5.0.0
- 因为该命令也没有指定各组件的个数，默认情况下，它会启动由 1 个 TiDB、1 个 TiKV 和 1 个 PD 实例构成的最小化集群
- 在依次启动完各个 TiDB 组件后，playground 会提醒集群启动成功，并告诉你一些有用的信息，譬如如何通过 MySQL 客户端连接集群、如何访问 [TiDB Dashboard](/dashboard/dashboard-intro.md) 等

playground 的命令行参数说明：

```bash
Flags:
      --db int                   设置集群中的 TiDB 数量（默认为1）
      --db.binpath string        指定 TiDB 二进制文件的位置（开发调试用，可忽略）
      --db.config string         指定 TiDB 的配置文件（开发调试用，可忽略）
      --db.host host             指定 TiDB 的监听地址
      --drainer int              设置集群中 Drainer 数据
      --drainer.binpath string   指定 Drainer 二进制文件的位置（开发调试用，可忽略）
      --drainer.config string    指定 Drainer 的配置文件
  -h, --help                     打印帮助信息
      --host string              设置每个组件的监听地址（默认为 127.0.0.1），如果要提供给别的电脑访问，可设置为 0.0.0.0
      --kv int                   设置集群中的 TiKV 数量（默认为1）
      --kv.binpath string        指定 TiKV 二进制文件的位置（开发调试用，可忽略）
      --kv.config string         指定 TiKV 的配置文件（开发调试用，可忽略）
      --monitor                  是否启动监控
      --pd int                   设置集群中的 PD 数量（默认为1）
      --pd.binpath string        指定 PD 二进制文件的位置（开发调试用，可忽略）
      --pd.config string         指定 PD 的配置文件（开发调试用，可忽略）
      --pump int                 指定集群中 Pump 的数量（非 0 的时候 TiDB 会开启 TiDB Binlog）
      --pump.binpath string      指定 Pump 二进制文件的位置（开发调试用，可忽略）
      --pump.config string       指定 Pump 的配置文件（开发调试用，可忽略）
      --tiflash int              设置集群中 TiFlash 数量（默认为0）
      --tiflash.binpath string   指定 TiFlash 的二进制文件位置（开发调试用，可忽略）
      --tiflash.config string    指定 TiFlash 的配置文件（开发调试用，可忽略）
```

## 使用示例

### 使用每日构建版启动一个 TiDB 集群

{{< copyable "shell-regular" >}}

```shell
tiup playground nightly
```

nightly 就是这个集群的版本号，类似的可以 `tiup playground v5.0.0` 等。

### 启动一个带监控的集群

{{< copyable "shell-regular" >}}

```shell
tiup playground nightly --monitor
```

该命令会在 9090 端口启动 prometheus 用于展示集群内部的时序数据。

### 覆盖 PD 的默认配置

首先，你需要复制 PD 的[配置模版](https://github.com/tikv/pd/blob/release-5.0/conf/config.toml)。假设你将复制的配置文件放置在 `~/config/pd.toml`，按需修改一些内容后，执行以下命令可以覆盖 PD 的默认配置：

{{< copyable "shell-regular" >}}

```shell
tiup playground --pd.config ~/config/pd.toml
```

### 替换默认的二进制文件

默认启动 playground 时，各个组件都是使用官方镜像组件包中的二进制文件启动的，如果本地编译了一个临时的二进制文件想要放入集群中测试，可以使用 `--{comp}.binpath` 这个参数替换，例如执行以下命令替换 TiDB 的二进制文件：

{{< copyable "shell-regular" >}}

```shell
tiup playground --db.binpath /xx/tidb-server
```

### 启动多个组件实例

默认情况下各启动一个 TiDB、TiKV 和 PD 实例，如果希望启动多个，可以加上如下参数：

{{< copyable "shell-regular" >}}

```shell
tiup playground v3.0.10 --db 3 --pd 3 --kv 3
```

## 快速连接到由 playground 启动的 TiDB 集群

TiUP 提供了 `client` 组件，用于自动寻找并连接 playground 在本地启动的 TiDB 集群，使用方式为：

{{< copyable "shell-regular" >}}

```shell
tiup client
```

该命令会在控制台上提供当前机器上由 playground 启动的 TiDB 集群列表，选中需要连接的 TiDB 集群，点击回车后，可以打开一个自带的 MySQL 客户端以连接 TiDB。

## 查看已启动集群的信息

{{< copyable "shell-regular" >}}

```shell
tiup playground display
```

可以看到如下信息：

```
Pid    Role     Uptime
---    ----     ------
84518  pd       35m22.929404512s
84519  tikv     35m22.927757153s
84520  pump     35m22.92618275s
86189  tidb     exited
86526  tidb     34m28.293148663s
86190  drainer  35m19.91349249s
```

## 扩容集群

扩容集群的命令行参数与启动集群的相似。以下命令可以扩容两个 TiDB：

{{< copyable "shell-regular" >}}

```shell
tiup playground scale-out --db 2
```

## 缩容集群

可在 `tiup playground scale-in` 命令中指定 `pid`，以缩容对应的实例。可以通过 `tiup playground display` 命令查看 `pid`。

{{< copyable "shell-regular" >}}

```shell
tiup playground scale-in --pid 86526
```
