---
title: 搭建私有镜像
---

# 搭建私有镜像

在构建私有云时，通常会使用隔离的网络环境，此时无法访问 TiUP 的官方镜像。因此，TiUP 提供了构建私有镜像的方案，它主要由 mirror 指令来实现，该方案也可用于离线部署。

## mirror 指令介绍

`mirror` 指令的帮助文档如下：

{{< copyable "shell-regular" >}}

```bash
tiup mirror --help
```

```
The 'mirror' command is used to manage a component repository for TiUP, you can use
it to create a private repository, or to add new component to an existing repository.
The repository can be used either online or offline.
It also provides some useful utilities to help managing keys, users and versions
of components or the repository itself.

Usage:
  tiup mirror <command> [flags]

Available Commands:
  init        Initialize an empty repository
  sign        Add signatures to a manifest file
  genkey      Generate a new key pair
  clone       Clone a local mirror from remote mirror and download all selected components
  publish     Publish a component

Flags:
  -h, --help          help for mirror
      --repo string   Path to the repository

Global Flags:
      --skip-version-check   Skip the strict version check, by default a version must be a valid SemVer string

Use "tiup mirror [command] --help" for more information about a command.
```

构建本地镜像将会使用 `tiup mirror clone` 指令，其基本用法如下：

{{< copyable "shell-regular" >}}

```bash
tiup mirror clone <target-dir> [global-version] [flags]
```

- `target-dir`：指需要把克隆下来的数据放到哪个目录里。
- `global-version`：用于为所有组件快速设置一个共同的版本。

`tiup mirror clone` 命令提供了很多可选参数，日后可能会提供更多。但这些参数其实可以分为四类：

1. 克隆时是否使用前缀匹配方式匹配版本

    如果指定了 `--prefix` 参数，则会才用前缀匹配方式匹配克隆的版本号。例：指定 `--prefix` 时，填写版本 "v5.0.0" 将会匹配 "v5.0.0-rc", "v5.0.0"

2. 是否全量克隆

    如果指定了 `--full` 参数，则会完整地克隆官方镜像。

    > **注意：**
    >
    > 如果既不指定 `--full` 参数，又不指定 `global-version` 或克隆的 component 版本，那么 TiUP 就只会克隆一些元信息。

3. 限定只克隆特定平台的包

    如果只想克隆某个平台的包，那么可以使用 `--os` 和 `--arch` 来限定：

    - 只想克隆 linux 平台的，则执行 `tiup mirror clone <target-dir> [global-version] --os=linux`
    - 只想克隆 amd64 架构的，则执行 `tiup mirror clone <target-dir> [global-version] --arch=amd64`
    - 只想克隆 linux/amd64 的，则执行 `tiup mirror clone <target-dir> [global-version] --os=linux --arch=amd64`

4. 限定只克隆组件的特定版本

    如果只想克隆某个组件的某一个版本而不是所有版本，则使用 `--<component>=<version>` 来限定，例如：

    - 只想克隆 TiDB 的 v5.1.0 版本，则执行 `tiup mirror clone <target-dir> --tidb v5.1.0`
    - 只想克隆 TiDB 的 v5.1.0 版本，以及 TiKV 的所有版本，则执行 `tiup mirror clone <target-dir> --tidb v5.1.0 --tikv all`
    - 克隆一个集群的所有组件的 v5.1.0 版本，则执行 `tiup mirror clone <target-dir> v5.1.0`

## 使用示例

使用 `tiup mirror clone` 命令克隆的仓库可以在主机之间共享。可以通过 SCP、NFS 共享文件，也可以通过 HTTP 或 HTTPS 协议使用仓库。用 `tiup mirror set <location>` 命令来指定仓库的位置。

参考[使用 TiUP 部署 TiDB 集群](/production-deployment-using-tiup.md#方式二离线部署-tiup-组件)安装 TiUP 离线镜像，部署并启动 TiDB 集群。
