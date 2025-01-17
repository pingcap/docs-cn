---
title: 搭建私有镜像
summary: TiUP 提供了构建私有镜像的方案，使用 mirror 指令来实现，可用于离线部署。执行 `tiup mirror clone` 命令，可构建本地地镜像。克隆完成后，可以通过 SCP、NFS、HTTP 或 HTTPS 共享仓库。使用 `TIUP_MIRRORS` 环境变量来使用镜像。重新运行 `tiup mirror clone` 命令会创建新的 manifest，并下载可用的最新版本的组件。可以创建自定义仓库，并使用自己构建的 TiDB 组件。
---

# 搭建私有镜像

在构建私有云时，通常会使用隔离的网络环境，此时无法访问 TiUP 的官方镜像。因此，TiUP 提供了构建私有镜像的方案，它主要由 mirror 指令来实现，该方案也可用于离线部署。使用私有镜像，你可以使用自己构建和打包的组件。

## mirror 指令介绍

`mirror` 指令的帮助文档如下：

```bash
tiup mirror --help
```

```
The `mirror` command is used to manage a component repository for TiUP, you can use
it to create a private repository, or to add new component to an existing repository.
The repository can be used either online or offline.
It also provides some useful utilities to help manage keys, users, and versions
of components or the repository itself.

Usage:
  tiup mirror <command> [flags]

Available Commands:
  init        Initialize an empty repository
  sign        Add signatures to a manifest file
  genkey      Generate a new key pair
  clone       Clone a local mirror from remote mirror and download all selected components
  merge       Merge two or more offline mirrors
  publish     Publish a component
  show        Show the mirror address
  set         Set mirror address
  modify      Modify published component
  renew       Renew the manifest of a published component.
  grant       grant a new owner
  rotate      Rotate root.json

Flags:
  -h, --help          help for mirror
      --repo string   Path to the repository

Global Flags:
      --help Help for this command

Use "tiup mirror [command] --help" for more information about a command.
```

## 克隆镜像

执行 `tiup mirror clone` 命令，可构建本地地镜像：

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

    - 只想克隆 TiDB 的 v8.5.1 版本，则执行 `tiup mirror clone <target-dir> --tidb v8.5.1`
    - 只想克隆 TiDB 的 v8.5.1 版本，以及 TiKV 的所有版本，则执行 `tiup mirror clone <target-dir> --tidb v8.5.1 --tikv all`
    - 克隆一个集群的所有组件的 v8.5.1 版本，则执行 `tiup mirror clone <target-dir> v8.5.1`

克隆完成后，签名密钥会自动设置。

### 管理私有仓库

你可以通过 SCP 和 NFS 文件共享方式，将 `tiup mirror clone` 克隆下来的仓库共享给其他主机，也可以通过 HTTP 或 HTTPS 协议来共享。可以使用 `tiup mirror set <location>` 指定仓库的位置。

```bash
tiup mirror set /shared_data/tiup
```

```bash
tiup mirror set https://tiup-mirror.example.com/
```

> **注意：**
>
> 如果在执行了 `tiup mirror clone` 的机器上执行 `tiup mirror set`，下次执行 `tiup mirror clone` 时，机器会从本地镜像而非远程镜像进行克隆。因此，更新私有镜像前，需要执行 `tiup mirror set --reset` 来重置镜像。

还可以通过 `TIUP_MIRRORS` 环境变量来使用镜像。下面是一个使用私有仓库运行 `tiup list` 的例子。

```bash
export TIUP_MIRRORS=/shared_data/tiup
tiup list
```

设置 `TIUP_MIRRORS` 会永久改变镜像配置，例如 `tiup mirror set`。详情请参考 [tiup issue #651](https://github.com/pingcap/tiup/issues/651)。

### 更新私有仓库

如果使用同样的 `target-dir` 目录再次运行 `tiup mirror clone` 命令，机器会创建新的 manifest，并下载可用的最新版本的组件。

> **注意：**
>
> 重新创建 manifest 之前，请确保所有组件和版本（包括之前下载的早期版本）都包含在内。

## 自定义仓库

你可以创建一个自定义仓库，以使用自己构建的 TiDB 组件，例如 TiDB、TiKV 或 PD。你也可以创建自己的 TiUP 组件。

要创建自己的组件，请执行 `tiup package` 命令，并按照[组件打包](https://github.com/pingcap/tiup/blob/master/doc/user/package.md)的说明进行操作。

### 创建自定义仓库

以下命令在 `/data/mirror` 目录下创建一个空仓库：

```bash
tiup mirror init /data/mirror
```

创建仓库时，密钥会被写入 `/data/mirror/keys`。

以下命令在 `~/.tiup/keys/private.json` 中创建一个私钥：

```bash
tiup mirror genkey
```

以下命令为 `jdoe` 授予 `/data/mirror` 路径下私钥 `~/.tiup/keys/private.json` 的所有权：

```bash
tiup mirror set /data/mirror
tiup mirror grant jdoe
```

### 使用自定义组件

1. 创建一个名为 `hello` 的自定义组件：

    ```bash
    $ cat > hello.c << END
    > #include <stdio.h>
    int main() {
      printf("hello\n");
      return (0);
    }
    END
    $ gcc hello.c -o hello
    $ tiup package hello --entry hello --name hello --release v0.0.1
    ```

    `package/hello-v0.0.1-linux-amd64.tar.gz` 创建成功。

2. 创建一个仓库和一个私钥，并为仓库授予所有权：

    ```bash
    $ tiup mirror init /tmp/m
    $ tiup mirror genkey
    $ tiup mirror set /tmp/m
    $ tiup mirror grant $USER
    ```

    ```bash
    tiup mirror publish hello v0.0.1 package/hello-v0.0.1-linux-amd64.tar.gz hello
    ```

3. 运行组件。如果组件还没有安装，会先下载安装：

    ```bash
    $ tiup hello
    ```

    ```
    The component `hello` version  is not installed; downloading from repository.
    Starting component `hello`: /home/dvaneeden/.tiup/components/hello/v0.0.1/hello
    hello
    ```

    执行 `tiup mirror merge` 命令，可以将自定义组件的仓库合并到另一个仓库中。这一操作假设 `/data/my_custom_components` 中的所有组件都使用 `$USER` 签名：

    ```bash
    $ tiup mirror set /data/my_mirror
    $ tiup mirror grant $USER
    $ tiup mirror merge /data/my_custom_components
    ```
