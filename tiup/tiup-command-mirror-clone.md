---
title: tiup mirror clone
---

# tiup mirror clone

命令 `tiup mirror clone` 用于克隆一个已经存在的镜像或克隆部分组件生成一个新的镜像。新旧镜像的组件相同，但使用的签名密钥不同。

## 语法

```sh
tiup mirror clone <target-dir> [global version] [flags]
```

- `<target-dir>` 是本地存放克隆下来的镜像的路径，如果不存在则会自动创建。
- 若指定了 `[global version]` 参数，TiUP 会尝试克隆指定版本的所有组件。若某些组件没有指定的版本，则克隆其最新版本。

## 选项

### -f, --full（boolean，默认 false）

是否克隆整个镜像。指定该选项后会完整从目标镜像克隆所有组件的所有版本，此时其他指定的选项将失效。

### -a, --arch（strings，默认 amd64,arm64）

仅克隆能在指定平台上运行的组件。

### -o, --os（strings，默认 linux,darwin）

仅克隆能在指定操作系统上运行的组件。

### --prefix（boolean，默认 false）

匹配版本时是否前缀匹配。默认情况下必须严格匹配指定的版本才会下载，指定该选项之后，仅前缀匹配指定的版本也会被下载。

### --{component}（strings，默认为空）

指定要克隆的 `{component}` 组件的版本列表。`{component}` 为组件名，可选的组件名可执行 [`tiup list --all`](/tiup/tiup-command-list.md) 查看。
