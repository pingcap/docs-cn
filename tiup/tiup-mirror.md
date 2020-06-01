---
title: 搭建私有镜像
category: tools
aliases: ['/docs-cn/dev/reference/tools/tiup/mirror/']
---

# 搭建私有镜像

在构建私有云时，通常会使用隔离的网络环境，此时无法访问 TiUP 的官方镜像。因此，我们提供了构建私有镜像的方案，它主要由 mirror 指令来实现，该方案也可用于离线部署。

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

`tiup mirror` 命令提供了很多可选参数，日后可能会提供更多。但这些参数其实可以分为四类：

1. 克隆时是否使用前缀匹配方式匹配版本

    如果指定了 `--prefix` 参数，则会才用前缀匹配方式匹配克隆的版本号。例：指定 `--prefex` 时填写版本 "v4.0.0" 将会匹配 "v4.0.0-rc.1", "v4.0.0-rc.2", "v4.0.0"

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

    - 只想克隆 TiDB 的 v4.0.0 版本，则执行 `tiup mirror clone <target-dir> --tidb v4.0.0`
    - 只想克隆 TiDB 的 v4.0.0 版本，以及 TiKV 的所有版本，则执行 `tiup mirror clone <target-dir> --tidb v4.0.0 --tikv all`
    - 克隆一个集群的所有组件的 v4.0.0 版本，则执行 `tiup mirror clone <target-dir> v4.0.0`

## 使用示例

### 使用 TiUP 离线安装 TiDB 集群

以在隔离的环境中安装一个 v4.0.0-rc 的 TiDB 集群为例，可以执行以下步骤：

1. 在一台和外网相通的机器上拉取需要的组件：

    {{< copyable "shell-regular" >}}

    ```bash
    tiup mirror clone package v4.0.0-rc --os=linux
    ```

    该命令会在当前目录下创建一个名叫 `package` 的目录，里面有启动一个集群必要的组件包。

2. 通过 tar 命令将该组件包打包然后发送到隔离环境的中控机：

    {{< copyable "shell-regular" >}}

    ```bash
    tar czvf package.tar.gz package
    ```

    此时，`package.tar.gz` 就是一个独立的离线环境。

3. 将包发送到目标集群的中控机后，执行以下命令安装 TiUP：

    {{< copyable "shell-regular" >}}

    ```bash
    tar xzvf package.tar.gz
    cd package
    sh local_install.sh
    ```

4. 根据提示安装完 TiUP 之后，再部署 TiDB 集群：

    {{< copyable "shell-regular" >}}

    ```bash
    export TIUP_MIRRORS=/path/to/mirror
    tiup cluster deploy <cluster-name> <cluster-version> <topology-file>
    tiup cluster start <cluster-name>
    ```

    `/path/to/mirror` 是执行 `local_install.sh` 命令时输出的离线镜像包的位置，如果在 `/tmp/package` 则：

    ```bash
    export TIUP_MIRRORS=/tmp/package
    ```

部署完成后，集群相关操作可参考 [cluster 命令](/tiup/tiup-cluster.md)。

### 构建私有镜像

构建私有镜像的方式和离线安装包的制作过程相同，只需要将 package 目录中的内容上传到 CDN 或者文件服务器即可，最简单的方式是：

{{< copyable "shell-regular" >}}

```bash
cd package
python -m SimpleHTTPServer 8000
```

这样就在 <http://127.0.0.1:8000> 这个地址建立了私有镜像。

通过私有镜像安装 TiUP：

{{< copyable "shell-regular" >}}

```bash
export TIUP_MIRRORS=http://127.0.0.1:8000
curl $TIUP_MIRRORS/local_install.sh | sh
```

导入 PATH 变量之后就可以正常使用 TiUP 了（需要保持 `TIUP_MIRRORS` 变量指向私有镜像）。
