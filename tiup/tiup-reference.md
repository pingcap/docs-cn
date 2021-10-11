---
title: TiUP 参考手册
---

# TiUP

TiUP 在 TiDB 生态中承担包管理器的功能，管理着 TiDB 生态下众多的组件，如 TiDB、PD、TiKV 等。

## 语法

```shell
tiup [flags] <command> [args...]        # 执行命令
# or
tiup [flags] <component> [args...]      # 运行组件
```

使用 `help` 命令可以获取特定命令的信息，每个命令的摘要都显示了其参数及其用法。必须参数显示在尖括号中，可选参数显示在方括号中。

`<command>` 代表命令名字，支持的命令列表请参考下方命令清单，`<component>` 代表组件名，支持的组件列表请参考下方组件清单。

## 选项

### -B, --binary

打印指定组件的二进制文件路径：

- 执行 `tiup -B/--binary <component>` 将打印已安装的 `<component>` 组件的最新稳定版路径，若 `<component>` 组件未安装，则报错
- 执行 `tiup -B/--binary <component>:<version>` 将打印已经安装的 `<component>` 组件的 `<version>` 版本所在的路径，若该版本未安装，则报错
- 数据类型：`BOOLEAN`
- 该选项默认关闭，默认值为 `false`。在命令中添加该选项，并传入 `true` 值或不传值，均可开启此功能。

> **注意：**
>
> 该选项只能用于 `tiup [flags] <component> [args...]` 格式的命令。

### --binpath (string)

指定要执行的组件的路径：执行一个组件时，如果不想使用 TiUP 镜像中的二进制文件，可以使用该参数使用自定义路径的二进制文件替换之。

> **注意：**
>
> 该选项只能用于 `tiup [flags] <component> [args...]` 格式的命令。

### --skip-version-check

> **注意：**
>
> 该选项自 `v1.3.0` 版本起**已废弃**。

- 跳过版本号合法性检查，默认指定的版本号只能是 Semantic Version。
- 数据类型：`BOOLEAN`
- 该选项默认关闭，默认值为 `false`。在命令中添加该选项，并传入 `true` 值或不传值，均可开启此功能。

### -T, --tag (string)

对启动的组件指定一个 `tag`：有的组件在执行过程中需要使用磁盘存储，TiUP 会分配一个临时目录作为该组件本次执行的存储目录，如果希望分配固定目录，可以用 `-T/--tag` 来指定目录名字，这样多次执行使用同样的 `tag` 就能读写到同一批文件。

### -v, --version

打印 TiUP 的版本

### --help

打印帮助信息

## 命令清单

TiUP 包含众多的命令，这些命令又包含了许多子命令，具体命令及其子命令的说明请参考对应的链接：

- [install](/tiup/tiup-command-install.md)：安装组件
- [list](/tiup/tiup-command-list.md)：查看组件列表
- [uninstall](/tiup/tiup-command-uninstall.md)：卸载组件
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
