---
title: tiup install
---

# tiup install

命令 `tiup install` 用于组件安装，它会从镜像仓库中下载指定版本的组件包，并在本地的 TiUP 数据目录中解压，以便后续使用。另外，当 TiUP 需要运行一个镜像仓库中不存在的组件时，会尝试先下载该组件，再自动运行，若仓库中不存在会报错。

## 语法

```shell
tiup install <component1>[:version] [component2...N] [flags]
```

`<component1>` 和 `<component2>` 代表组件名字，`[version]` 代表一个可选的版本号，若不加 `version`，则安装指定组件的最新稳定版本。`[component2...N]` 表示可同时指定多个组件或同一个组件的多个版本。

## 选项

无

## 输出

- 正常情况下输出组件的下载信息
- 若组件不存在则报错 `The component "%s" not found`
- 若版本不存在则报错 `version %s not supported by component %s`
