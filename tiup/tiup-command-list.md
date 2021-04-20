---
title: tiup list
---

# tiup list

命令 `tiup list` 用于查询镜像中可用的组件列表。

## 语法

```shell
tiup list [component] [flags]
```

`[component]` 是可选的组件名称。若指定，则列出该组件的所有版本；若不指定，则列出所有组件列表。

## 选项

### --all

- 显示所有组件。默认只显示非隐藏组件。
- 数据类型：`BOOLEAN`
- 该选项默认关闭，默认值为 `false`。在命令中添加该选项，并传入 `true` 值或不传值，均可开启此功能。

### --installed

- 只显示已经安装的组件或版本。
- 数据类型：`BOOLEAN`
- 该选项默认关闭，默认值为 `false`。在命令中添加该选项，并传入 `true` 值或不传值，均可开启此功能。

### --verbose

- 在组件列表中显示已安装的版本列表。默认组件列表不显示当前已安装的版本。
- 数据类型：`BOOLEAN`
- 该选项默认关闭，默认值为 `false`。在命令中添加该选项，并传入 `true` 值或不传值，均可开启此功能。

## 输出

- 若未指定 `[component]`
    - 若指定 --verbose：输出 `组件名 (Name)`、`已安装版本 (Installed)`、`组件管理员 (Owner)`、`组件描述 (Description)` 构成的组件信息列表
    - 若不指定 --verbose：输出 `组件名 (Name)`、`组件管理员 (Owner)`、`组件描述 (Description)` 构成的组件信息列表
- 若指定 `[component]`
    - 若 `[component]` 存在：输出 `版本 (Version)`、`是否已安装 (Installed)`、`发布时间 (Release)`、`支持的平台 (Platforms)` 构成的版本信息列表
    - 若 `[component]` 不存在：报错 `failed to fetch component: unknown component`
