---
title: 搭建私有镜像
category: tools
---

# 搭建私有镜像

在构建私有云时，通常会使用隔离的网络环境，这个时候访问不了 TiUP 的官方镜像，于是我们提供了构建私有镜像的方案，它主要由 mirros 组件来实现，该方案也可用于离线部署。

## mirros 组件介绍

首先我们看 `mirrors` 的帮助文档：

```bash
$ tiup mirrors --help
Starting component `mirrors`: /Users/joshua/.tiup/components/mirrors/v0.0.1/mirrors
Build a local mirrors and download all selected components

Usage:
  tiup mirrors <target-dir> [global-version] [flags]

Examples:
  tiup mirrors local-path --arch amd64,arm --os linux,darwin    # Specify the architectures and OSs
  tiup mirrors local-path --full                                # Build a full local mirrors
  tiup mirrors local-path --tikv v4                             # Specify the version via prefix
  tiup mirrors local-path --tidb all --pd all                   # Download all version for specific component

Flags:
      --overwrite                   Overwrite the exists tarball
  -f, --full                        Build a full mirrors repository
  -a, --arch strings                Specify the downloading architecture (default [amd64])
  -o, --os strings                  Specify the downloading os (default [linux,darwin])
      --tidb strings                Specify the versions for component tidb
      --tikv strings                Specify the versions for component tikv
      --pd strings                  Specify the versions for component pd
      --playground strings          Specify the versions for component playground
      --client strings              Specify the versions for component client
      --prometheus strings          Specify the versions for component prometheus
      --package strings             Specify the versions for component package
      --grafana strings             Specify the versions for component grafana
      --alertmanager strings        Specify the versions for component alertmanager
      --blackbox_exporter strings   Specify the versions for component blackbox_exporter
      --node_exporter strings       Specify the versions for component node_exporter
      --pushgateway strings         Specify the versions for component pushgateway
      --tiflash strings             Specify the versions for component tiflash
      --drainer strings             Specify the versions for component drainer
      --pump strings                Specify the versions for component pump
      --cluster strings             Specify the versions for component cluster
      --mirrors strings             Specify the versions for component mirrors
      --bench strings               Specify the versions for component bench
      --insight strings             Specify the versions for component insight
      --doc strings                 Specify the versions for component doc
      --ctl strings                 Specify the versions for component ctl
  -h, --help                        help for tiup
```

它的基本用法是 `tiup mirrors <target-dir> [global-version] [flags]`，这个 target-dir 是说需要把克隆下来的数据放到哪个目录里。global-version 用于快速为所有组件设置一个共同的版本。
然后这个命令有很吓人的几十个 flag，以后甚至更多。但是完全不必被这些 flag 的数量吓倒，其实它们也就四类：

### 1. 指定是否覆盖本地的包

`--overwrite` 参数的意义是说，如果指定的 <target-dir> 中已经有想要下载的包了，是否要用官方镜像的包覆盖，如果设置了这个 flag 就会覆盖。

### 2. 是否全量克隆

如果指定了 `--full`，则会完整的克隆官方镜像。

> **注意：**
>
> 如果不指定 `--full` 也不指定其它 flag，那么就只会克隆一些元信息

### 3. 平台限定

如果只想克隆某个平台的包，那么可以使用 `--os` 和 `--arch` 来限定:

- 只想克隆 linux 平台的: `tiup mirros <target-dir> --os=linux`
- 只想克隆 amd64 架构的: `tiup mirros <target-dir> --arch=amd64`
- 只想克隆 linux/amd64 的: `tiup mirros <target-dir> --os=linux --arch=amd64`

### 4. 组件版本限定

如果只想克隆某个组件的某一个版本而不是所有版本，则使用 `--<component>=<version>` 来限定，比如“

- 只想克隆 tidb 的 v4 版本: `tiup mirrors <target-dir> --tidb v4`
- 只想克隆 tidb 的 v4 版本，以及 tikv 的所有版本: `tiup mirros <target-dir> --tidb v4 --tikv all` 
- 克隆启动一个集群的所有组件的特定版本：`tiup mirrors <target-dir> v4.0.0-rc`

## 实战

### 离线安装

例如我们想在隔离的环境中安装一个 v4.0.0-rc 的 TiDB 集群，则可以在一台和外网相通的机器上执行以下命令拉取需要的组件：

```bash
tiup mirrors package --os=linux v4.0.0-rc
```

该命令会在当前目录下创建一个名叫 `package` 的目录，里面有启动一个集群必要的组件包，通过 tar 命令将其打包然后发送到隔离环境的中控机：

```bash
tar czvf package.tar.gz package
```

package.tar.gz 就是一个独立的离线环境了，将其发送到目标集群的中控机后，执行以下命令安装 TiUP:

```bash
tar xzvf package.tar.gz
cd package
sh local_install.sh
```

根据提示安装完 TiUP 之后，再部署 TiDB 集群 (假设工作目录还在 package 内)：

```bash
export TIUP_MIRRORS=/path/to/mirror
tiup cluster xxx
```

`/path/to/mirror` 是 `tiup mirrors <target-dir>` 中 <target-dir> 所在的位置，如果在 /tmp/package 则：

```bash
export TIUP_MIRRORS=/tmp/package
```

集群相关操作可参考 [cluster 命令](/reference/tools/tiup/cluster.md) 的相关介绍。

### 私有镜像

构建私有镜像的方式和离线安装包的制作过程相同，只需要将 package 目录中的内容上传到 CDN 或者文件服务器即可，最简单的方式是：

```bash
cd package
python -m SimpleHTTPServer 8000
```

这样就在 `http://127.0.0.1:8000` 这个地址建立了私有镜像。通过私有镜像安装 TiUP:

```bash
export TIUP_MIRRORS=http://127.0.0.1:8000
curl $TIUP_MIRRORS/install.sh | sh
```

导入 PATH 变量之后就可以正常使用 TiUP 了（需要保持 TIUP_MIRRORS 变量指向私有的镜像）。