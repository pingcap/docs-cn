---
title: 使用 TiUP 命令管理组件
aliases: ['/docs-cn/dev/tiup/tiup-component-management/','/docs-cn/dev/reference/tools/tiup/manage-component/','/docs-cn/dev/reference/tools/tiup/manage-tiup-component/']
summary: TiUP 是一个用于管理组件的命令行工具。它提供了一系列命令来查询组件列表、安装、升级、运行、查看状态、清理实例和卸载组件。此外，还可以使用实验性的 `link` 和 `unlink` 命令来将组件的二进制符号链接到可执行文件目录。
---

# 使用 TiUP 命令管理组件

TiUP 主要通过以下一些命令来管理组件：

- list：查询组件列表，用于了解可以安装哪些组件，以及这些组件可选哪些版本
- install：安装某个组件的特定版本
- update：升级某个组件到最新的版本
- uninstall：卸载组件
- status：查看组件运行状态
- clean：清理组件实例
- help：打印帮助信息，后面跟其他 TiUP 命令则是打印该命令的使用方法
- link：将组件的二进制符号链接到可执行文件目录 (`$TIUP_HOME/bin/`)
- unlink：删除 `tiup link` 命令生成的软链接

本文介绍常用的组件管理操作及相应命令。

## 查询组件列表

你可以使用 `tiup list` 命令来查询组件列表。该命令用法如下：

- `tiup list`：查看当前有哪些组件可以安装
- `tiup list ${component}`：查看某个组件有哪些版本可以安装

你也可以在命令中组合使用以下参数 (flag)：

- `--installed`：查看本地已经安装了哪些组件，或者已经安装了某个组件的哪些版本
- `--all`：显式隐藏的组件
- `--verbose`：显式所有列（安装的版本、支持的平台）

示例一：查看当前已经安装的所有组件

{{< copyable "shell-regular" >}}

```shell
tiup list --installed
```

示例二：从服务器获取 TiKV 所有可安装版本组件列表

{{< copyable "shell-regular" >}}

```shell
tiup list tikv
```

## 安装组件

你可以使用 `tiup install` 命令来安装组件。该命令的用法如下：

- `tiup install <component>`：安装指定组件的最新稳定版
- `tiup install <component>:[version]`：安装指定组件的指定版本

示例一：使用 TiUP 安装最新稳定版的 TiDB

{{< copyable "shell-regular" >}}

```shell
tiup install tidb
```

示例二：使用 TiUP 安装 nightly 版本的 TiDB

{{< copyable "shell-regular" >}}

```shell
tiup install tidb:nightly
```

示例三：使用 TiUP 安装 v8.2.0 版本的 TiKV

{{< copyable "shell-regular" >}}

```shell
tiup install tikv:v8.2.0
```

## 升级组件

在官方组件提供了新版之后，你可以使用 `tiup update` 命令来升级组件。除了以下几个参数，该命令的用法基本和 `tiup install` 相同：

- `--all`：升级所有组件
- `--nightly`：升级至 nightly 版本
- `--self`：升级 TiUP 自己至最新版本
- `--force`：强制升级至最新版本

示例一：升级所有组件至最新版本

{{< copyable "shell-regular" >}}

```shell
tiup update --all
```

示例二：升级所有组件至 nightly 版本

{{< copyable "shell-regular" >}}

```shell
tiup update --all --nightly
```

示例三：升级 TiUP 至最新版本

{{< copyable "shell-regular" >}}

```shell
tiup update --self
```

## 运行组件

安装完成之后，你可以使用 `tiup <component>` 命令来启动相应的组件：

```shell
tiup [flags] <component>[:version] [args...]

Flags:
  -T, --tag string                     为组件实例指定 tag
```

该命令需要提供一个组件的名字以及可选的版本，若不提供版本，则使用该组件已安装的最新稳定版。

在组件启动之前，TiUP 会先为它创建一个目录，然后将组件放到该目录中运行。组件会将所有数据生成在该目录中，目录的名字就是该组件运行时指定的 tag 名称。如果不指定 tag，则会随机生成一个 tag 名称，并且在实例终止时*自动删除*工作目录。

如果想要多次启动同一个组件并复用之前的工作目录，就可以在启动时用 `--tag` 指定相同的名字。指定 tag 后，在实例终止时就*不会自动删除*工作目录，方便下次启动时复用。

示例一：运行 v8.2.0 版本的 TiDB

{{< copyable "shell-regular" >}}

```shell
tiup tidb:v8.2.0
```

示例二：指定 tag 运行 TiKV

{{< copyable "shell-regular" >}}

```shell
tiup --tag=experiment tikv
```

### 查询组件运行状态

你可以使用 `tiup status` 命令来查看组件的运行状态：

{{< copyable "shell-regular" >}}

```shell
tiup status
```

运行该命令会得到一个实例列表，每行一个实例。列表中包含这些列：

- Name：实例的 tag 名称
- Component：实例的组件名称
- PID：实例运行的进程 ID
- Status：实例状态，`RUNNING` 表示正在运行，`TERM` 表示已经终止
- Created Time：实例的启动时间
- Directory：实例的工作目录，可以通过 `--tag` 指定
- Binary：实例的可执行程序，可以通过 `--binpath` 指定
- Args：实例的运行参数

### 清理组件实例

你可以使用 `tiup clean`  命令来清理组件实例，并删除工作目录。如果在清理之前实例还在运行，会先 kill 相关进程。该命令用法如下：

{{< copyable "shell-regular" >}}

```bash
tiup clean [tag] [flags]
```

支持以下参数：

- `--all`：清除所有的实例信息

其中 tag 表示要清理的实例 tag，如果使用了 `--all` 则不传递 tag。

示例一：清理 tag 名称为 `experiment` 的组件实例

{{< copyable "shell-regular" >}}

```shell
tiup clean experiment
```

示例二：清理所有组件实例

{{< copyable "shell-regular" >}}

```shell
tiup clean --all
```

### 卸载组件

TiUP 安装的组件会占用本地磁盘空间，如果不想保留过多老版本的组件，可以先查看当前安装了哪些版本的组件，然后再卸载某个组件。

你可以使用 `tiup uninstall` 命令来卸载某个组件的所有版本或者特定版本，也支持卸载所有组件。该命令用法如下：

{{< copyable "shell-regular" >}}

```bash
tiup uninstall [component][:version] [flags]
```

支持的参数：

- `--all`：卸载所有的组件或版本
- `--self`：卸载 TiUP 自身

component 为要卸载的组件名称，version 为要卸载的版本，这两个都可以省略，省略任何一个都需要加上 `--all` 参数：

- 若省略版本，加 `--all` 表示卸载该组件所有版本
- 若版本和组件都省略，则加 `--all` 表示卸载所有组件及其所有版本

示例一：卸载 v8.2.0 版本的 TiDB

{{< copyable "shell-regular" >}}

```shell
tiup uninstall tidb:v8.2.0
```

示例二：卸载所有版本的 TiKV

{{< copyable "shell-regular" >}}

```shell
tiup uninstall tikv --all
```

示例三：卸载所有已经安装的组件

{{< copyable "shell-regular" >}}

```shell
tiup uninstall --all
```

### 链接组件

TiUP v1.13.0 添加了实验性的 `link` 和 `unlink` 命令，用于将组件的二进制符号链接到可执行文件目录 (`$TIUP_HOME/bin/`) 和删除链接。这个功能可以让用户不必在每次都经过 TiUP 来调用组件，同时保留了多版本切换的能力。然而，这种方式缺少了自动检查更新和设置某些环境变量的过程，一些组件（例如 ctl）可能无法使用，请只在必要的场景来使用它。

示例一：安装并链接 cluster 组件的最新版本

```shell
tiup install cluster
tiup link cluster
```

示例二：切换 cluster 组件到 v1.13.0 版本

```shell
tiup link cluster：v1.13.0
```

`tiup link cluster` 命令会输出如下的内容：

```shell
package cluster provides these executables: tiup-cluster
```

代表 cluster 组件的二进制文件名为 tiup-cluster。link 命令完成后，你可以直接在命令行输入 tiup-cluster 来使用 cluster 组件。

示例三：取消 cluster 组件的链接

```shell
tiup unlink cluster
```

示例四：对 TiUP 自身进行版本管理

在 v1.13.0 之前的版本，TiUP 自身被安装到 `~/.tiup/bin/` 下，不能多版本共存。自 v1.13.0 开始，可以将 TiUP 和所有其他组件一样进行安装、链接。

```shell
tiup update --self # update tiup itself to a version that supports link
tiup link tiup：v1.13.0
```