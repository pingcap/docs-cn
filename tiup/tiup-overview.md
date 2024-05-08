---
title: TiUP 简介
summary: TiUP 是 TiDB 生态中的包管理工具，简化了软件的安装和升级维护工作。安装 TiUP 十分简洁，只需执行一行命令即可完成。TiUP 的愿景是降低 TiDB 生态中所有工具的使用门槛，通过命令和组件来实现包管理和操作。
---

# TiUP 简介

在各种系统软件和应用软件的安装管理中，包管理器均有着广泛的应用，包管理工具的出现大大简化了软件的安装和升级维护工作。例如，几乎所有使用 RPM 的 Linux 都会使用 yum 来进行包管理，而 Anaconda 则可以非常方便地管理 Python 的环境和相关软件包。

在早期的 TiDB 生态中，没有专门的包管理工具，使用者只能通过相应的配置文件和文件夹命名来手动管理，如 Prometheus 等第三方监控报表工具甚至需要额外的特殊管理，这样大大提升了运维管理难度。

从 TiDB 4.0 版本开始，TiUP 作为新的工具，承担着包管理器的角色，管理着 TiDB 生态下众多的组件，如 TiDB、PD、TiKV 等。用户想要运行 TiDB 生态中任何组件时，只需要执行 TiUP 一行命令即可，相比以前，极大地降低了管理难度。

## 安装 TiUP

TiUP 安装过程十分简洁，无论是 Darwin 还是 Linux 操作系统，执行一行命令即可安装成功：

{{< copyable "shell-regular" >}}

```bash
curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
```

该命令将 TiUP 安装在 `$HOME/.tiup` 文件夹下，之后安装的组件以及组件运行产生的数据也会放在该文件夹下。同时，它还会自动将 `$HOME/.tiup/bin` 加入到 Shell Profile 文件的 PATH 环境变量中，这样你就可以直接使用 TiUP 了。

例如，你可以查看 TiUP 的版本：

{{< copyable "shell-regular" >}}

```bash
tiup --version
```

```bash
1.14.0 tiup
Go Version: go1.21.4
Git Ref: v1.14.0
GitHash: c3e9fc518aea0da66a37f82ee5a516171de9c372
```

> **注意：**
>
> 对于 v1.11.3 及以上版本的 TiUP，默认不会收集使用情况信息分享给 PingCAP。若要了解所收集的信息详情及如何关闭分享行为，请参见[遥测](/telemetry.md)。

## TiUP 生态介绍

TiUP 的直接功能是作为 TiDB 生态中的包管理器，但这并不是它的最终使命。TiUP 的愿景是将 TiDB 生态中所有工具的使用门槛降到极致，这个仅仅靠包管理功能是做不到的，还需要引入一些额外的包来丰富这个系统，它们一起加入到 TiUP 生态中，让 TiDB 的世界变得更简单。

TiUP 系列文档的主要内容就是介绍 TiUP 及这些包的功能和使用方式。

在 TiUP 生态中，你可以通过在任何命令后加上 `--help` 的方式来获得帮助信息，比如通过以下命令获取 TiUP 本身的帮助信息:

{{< copyable "shell-regular" >}}

```bash
tiup --help
```

```
TiUP is a command-line component management tool that can help to download and install
TiDB platform components to the local system. You can run a specific version of a component via
"tiup <component>[:version]". If no version number is specified, the latest version installed
locally will be used. If the specified component does not have any version installed locally,
the latest stable version will be downloaded from the repository.

Usage:
  tiup [flags] <command> [args...]
  tiup [flags] <component> [args...]
  tiup [command]

Examples:
  $ tiup playground                    # Quick start
  $ tiup playground nightly            # Start a playground with the latest nightly version
  $ tiup install <component>[:version] # Install a component of specific version
  $ tiup update --all                  # Update all installed components to the latest version
  $ tiup update --nightly              # Update all installed components to the nightly version
  $ tiup update --self                 # Update the "tiup" to the latest version
  $ tiup list                          # Fetch the latest supported components list
  $ tiup status                        # Display all running/terminated instances
  $ tiup clean <name>                  # Clean the data of running/terminated instance (Kill process if it's running)
  $ tiup clean --all                   # Clean the data of all running/terminated instances

Available Commands:
  install     Install a specific version of a component
  list        List the available TiDB components or versions
  uninstall   Uninstall components or versions of a component
  update      Update tiup components to the latest version
  status      List the status of instantiated components
  clean       Clean the data of instantiated components
  mirror      Manage a repository mirror for TiUP components
  telemetry   Controls things about telemetry
  env         Show the list of system environment variable that related to TiUP
  history     Display the historical execution record of TiUP, displays 100 lines by default
  link        Link component binary to $TIUP_HOME/bin/
  unlink      Unlink component binary to $TIUP_HOME/bin/
  help        Help about any command
  completion  Generate the autocompletion script for the specified shell

Flags:
      --binary <component>[:version]   Print binary path of a specific version of a component <component>[:version]
                                       and the latest version installed will be selected if no version specified
      --binpath string                 Specify the binary path of component instance
  -h, --help                           help for tiup
  -T, --tag string                     [Deprecated] Specify a tag for component instance
  -v, --version                        Print the version of tiup

Use "tiup [command] --help" for more information about a command.
```

输出的帮助信息较长，你可以只关注两部分：

- 可用的命令
    - install：用于安装特定版本的组件
    - list：查看可用组件列表或组件可用版本列表
    - uninstall：卸载组件或组件版本
    - update：更新组件版本
    - status：查看组件运行记录
    - clean：清除组件运行记录
    - mirror：从官方镜像克隆一个私有镜像
    - telemetry：控制遥测功能
    - env：显示与 TiUP 相关的系统环境变量列表
    - history：显示 TiUP 的历史执行记录，默认显示 100 行
    - link：将组件二进制文件链接到 `$TIUP_HOME/bin/`
    - unlink：取消组件二进制文件到 `$TIUP_HOME/bin/` 的链接
    - help：输出帮助信息
    - completion：为指定的 shell（bash、zsh、fish、powershell）生成命令行自动补全脚本
- 可用的组件
    - playground：在本机启动一个 TiDB 集群
    - client：连接 TiUP Playground 的客户端
    - cluster：部署用于生产环境的 TiDB 集群
    - bench：对数据库进行压力测试

> **注意：**
>
> - 可用的组件会持续增加，以 `tiup list` 输出结果为准。
> - 组件的可用版本列表也会持续增加，以 `tiup list <component>` 输出结果为准。

命令和组件的区别在于，命令是 TiUP 自带的，用于进行包管理的操作。而组件是 TiUP 通过包管理操作安装的独立组件包。比如执行 `tiup list` 命令，TiUP 会直接运行自己内部的代码，而执行 `tiup playground` 命令则会先检查本地有没有叫做 playground 的组件包，若没有则先从镜像上下载过来，然后运行这个组件包。
