---
title: tiup update
---

# tiup update

命令 `tiup update` 用于升级已安装的组件或者自身。

## 语法

```shell
tiup update [component1][:version] [component2..N] [flags]
```

- `[component1]` 表示要升级的组件名字
- `[version]` 表示要升级的版本，如果省略，则表示升级到该组件的最新稳定版本
- `[component2...N]` 表示可指定升级多个组件或版本。如果一个组件也不指定：即 `[component1][:version] [component2..N]` 为空，则需要配合使用 `--all` 选项或 `--self` 选项。

升级操作不会删除旧的版本，仍然可以在执行时指定旧版本使用。

## 选项

### --all

- 若未指定任何组件，则必须指定该选项。
- 数据类型：`BOOLEAN`
- 该选项默认关闭，默认值为 `false`。在命令中添加该选项，并传入 `true` 值或不传值，均可开启此功能。

### --force

- 若指定的组件版本已经安装，则默认跳过升级操作，指定该参数可强制升级已安装版本。
- 数据类型：`BOOLEAN`
- 该选项默认关闭，默认值为 `false`。在命令中添加该选项，并传入 `true` 值或不传值，均可开启此功能。

### --nightly

- 将指定组件升级到 nightly 版本。使用该参数的命令等价于 `tiup update <component>:nightly`。
- 数据类型：`BOOLEAN`
- 该选项默认关闭，默认值为 `false`。在命令中添加该选项，并传入 `true` 值或不传值，均可开启此功能。

### --self

- 升级 TiUP 自身。
- 数据类型：`BOOLEAN`
- 该选项默认关闭，默认值为 `false`。在命令中添加该选项，并传入 `true` 值或不传值，均可开启此功能。

## 输出

- 升级成功：`Updated successfully!`
- 目标版本不存在：`Error: version %s not supported by component %s`

[<< 返回上一页 - TiUP 命令清单](/tiup/tiup-reference.md#命令清单)