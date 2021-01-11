---
title: TiUP 参考手册
aliases: ['/docs-cn/dev/tiup/tiup-reference/']
---

# TiUP

## 介绍

在各种系统软件和应用软件的安装管理中，包管理器均有着广泛的应用，包管理工具的出现大大简化了软件的安装和升级维护工作。例如，几乎所有使用 RPM 的 Linux 都会使用 Yum 来进行包管理，而 Anaconda 则可以非常方便地管理 python 的环境和相关软件包。

在早期的 TiDB 生态中，没有专门的包管理工具，使用者只能通过相应的配置文件和文件夹命名来手动管理，如 Prometheus 等第三方监控报表工具甚至需要额外的特殊管理，这样大大提升了运维管理难度。

从 TiDB 4.0 版本开始，TiUP 作为新的工具，承担着包管理器的角色，管理着 TiDB 生态下众多的组件，如 TiDB、PD、TiKV 等。用户想要运行 TiDB 生态中任何组件时，只需要执行 TiUP 一行命令即可，相比以前，极大地降低了管理难度。

TiUP 的使用围绕命令，组件，镜像这几个核心概念进行，我们下面先对它们进行定义。

### 命令

命令是程序功能的入口，一切功能都被实现在一个命令中，它具有以下特点：

- 内置于可执行程序
- 可以带有子命令
- 可以带有参数及选项（flags）

TiUP 集成了一系列的子命令用于组件管理和镜像管理。

### 组件

区别于命令，组件具有以下特点：

- 动态从镜像中取得
- 本身是一个或一组二进制程序
- 有自己的命令及子命令

### 镜像

镜像是一个组件仓库，它存放了一系列组件，负责在 TiUP 需要某个组件时提供它。

## 语法

```sh
tiup [flags] <command> [args...]        # 执行命令
# or
tiup [flags] <component> [args...]      # 运行组件
```

使用 `help` 命令可以获取特定命令的信息，每个命令的摘要都显示了其参数及其用法。必须参数显示在尖括号中，可选参数显示在方括号中。

`<command>` 代表命令名字，支持的命令列表请参考下方命令清单，`<component>` 代表组件名，支持的组件列表请参考下方组件清单。

## 选项

### -B, --binary (boolean，默认 false)

打印指定组件的二进制文件路径：

- 执行 `tiup -B/--binary <component>` 将打印已安装的 `<component>` 组件的最新稳定版路径，若 `<component>` 组件未安装，则报错
- 执行 `tiup -B/--binary <component>:<version>` 将答应已经安装的 `<component>` 组件的 `<version>` 版本所在的路径，若该版本未安装，则报错

> **使用限制：**
>
> 该选项只能用于 `tiup [flags] <component> [args...]` 格式的命令。

### --binpath (string)

指定要执行的组件的路径：执行一个组件时，如果不想使用 TiUP 镜像中的二进制文件，可以使用该参数使用自定义路径的二进制文件替换之。

> **使用限制：**
>
> 该选项只能用于 `tiup [flags] <component> [args...]` 格式的命令。

### --skip-version-check (boolean，默认 false)

跳过版本号合法性检查，默认指定的版本号只能是 Semantic Version。

***deprecated***

### -T, --tag (string)

对启动的组件指定一个 `tag`：有的组件在执行过程中需要使用磁盘存储，TiUP 会分配一个临时目录作为该组件本次执行的存储目录，如果希望分配固定目录，可以用 `-T/--tag` 来指定目录名字，这样多次执行使用同样的 `tag` 就能读写到同一批文件。

### -v, --version

打印 TiUP 的版本

### --help

打印帮助信息

## 命令清单

- [install](/tiup/tiup-command-install.md)：安装组件
- [list](/tiup/tiup-command-list.md)：查看组件列表
- [uniinstall](/tiup/tiup-command-uninstall.md)：卸载组件
- [update](/tiup/tiup-command-update.md)：升级已安装的组件
- [status](/tiup/tiup-command-status.md)：查看组件运行状态
- [clean](/tiup/tiup-command-clean.md)：清理组件数据目录
- [mirror](/tiup/tiup-command-mirror.md)：镜像管理
- [telemetry](/tiup/tiup-command-telemetry.md)：遥测开关
- [completion](/tiup/tiup-command-completion.md)：TiUP 命令补全
- [env](/tiup/tiup-command-env.md)：查看 TiUP 相关环境变量
- [help](/tiup/tiup-command-help.md)：查看特定命令或组件的帮助文档

## 组件清单

- [cluster](/tiup/tiup-component-cluster.md)：生产环境 TiDB 集群管理
- [dm](/tiup/tiup-component-dm.md)：生产环境 DM 集群管理