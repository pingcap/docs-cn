---
title: tiup mirror clone
---

# tiup mirror clone

命令 `tiup mirror clone` 用于克隆一个已经存在的镜像或克隆部分组件生成一个新的镜像。新旧镜像的组件相同，但使用的签名密钥不同。

## 语法

```shell
tiup mirror clone <target-dir> [global version] [flags]
```

- `<target-dir>` 是本地存放克隆下来的镜像的路径，如果不存在则会自动创建。
- 若指定了 `[global version]` 参数，TiUP 会尝试克隆指定版本的所有组件。若某些组件没有指定的版本，则克隆其最新版本。

## 选项

### -f, --full

- 是否克隆整个镜像。指定该选项后会从目标镜像完整克隆所有组件的所有版本，此时其他指定的选项将失效。
- 数据类型：`BOOLEAN`
- 该选项默认关闭，默认值为 `false`。在命令中添加该选项，并传入 `true` 值或不传值，均可开启此功能。

### -a, --arch

- 仅克隆能在指定平台上运行的组件。
- 数据类型：`STRINGS`
- 该参数接受以逗号分隔的多个平台名称，例如 `amd64,arm64`。如果未指定该选项，默认克隆 AMD64 和 ARM64 平台的组件，即 `amd64,arm64`。

### -o, --os

- 仅克隆能在指定操作系统上运行的组件。
- 数据类型：`STRINGS`
- 该参数接受以逗号分隔的多个操作系统名称，例如 `linux,darwin`。如果未指定该选项，默认克隆 Linux 和 Darwin 系统的组件，即 `linux,darwin`。

### --prefix

- 匹配版本时是否前缀匹配。默认情况下必须严格匹配指定的版本才会下载，指定该选项之后，仅前缀匹配指定的版本也会被下载。
- 数据类型：`BOOLEAN`
- 该选项默认关闭，默认值为 `false`。在命令中添加该选项，并传入 `true` 值或不传值，均可开启此功能。

### --{component}（strings，默认为空）

指定要克隆的 `{component}` 组件的版本列表。`{component}` 为组件名，可选的组件名可执行 [`tiup list --all`](/tiup/tiup-command-list.md) 查看。

[<< 返回上一页 - TiUP Mirror 命令清单](/tiup/tiup-component-mirror.md#命令清单)