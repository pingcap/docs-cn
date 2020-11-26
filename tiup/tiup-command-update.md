---
title: tiup update
aliases: ['/docs-cn/dev/tiup/tiup-command-update/']
---

# tiup update

## 介绍

命令 `tiup update` 用于升级已安装的组件。

## 语法

```sh
tiup update [component1][:version] [component2..N] [flags]
```

`[component1]` 表示要升级的组件名字，`[version]` 表示要卸载的版本，如果省略，则表示升级到该组件的最新稳定版本，`[component2...N]` 表示可指定升级多个组件或版本。如果一个组件也不指定：即 `[component1][:version] [component2..N]` 为空，则需要配合使用 `--all` 选项或 `--self` 选项。

升级操作不会删除旧的版本，仍然可以在执行时指定旧版本。

## 选项

### --all (boolean, 默认 false)

升级所有已安装的组件，若未指定任何组件，则必须指定该选项为 `true`。

### --force (boolean, 默认 false)

若指定的组件版本已经安装，则不进行升级操作，指定该参数可忽略已安装版本强制升级。

### --nightly (boolean, 默认 false)

将指定组件升级到 nightly：等价于 `tiup update <component>:nightly`。

### --self (boolean，默认 false)

升级 tiup 自身。

## 输出

- 升级成功：`Updated successfully!`
- 目标版本不存在：`Error: version %s not supported by component %s`