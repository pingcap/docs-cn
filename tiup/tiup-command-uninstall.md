---
title: tiup uninstall
---

# tiup uninstall

命令 `tiup uninstall` 用于卸载已安装的组件。

## 语法

```shell
tiup uninstall <component1>:<version> [component2...N] [flags]
```

- `<component1>` 表示要卸载的组件名字
- `<version>` 表示要卸载的版本，如果省略，则表示卸载该组件的全部已安装版本，因为安全原因，省略 `<version>` 时必须加上选项 `--all` 明确表示需要卸载该组件的所有版本
- `[component2...N]` 表示可指定卸载多个组件或版本

## 选项

### --all

- 卸载指定组件的全部已安装版本，省略 `<version>` 时使用。
- 数据类型：`BOOLEAN`
- 该选项默认关闭，默认值为 `false`。在命令中添加该选项，并传入 `true` 值或不传值，均可开启此功能。

### --self

- 卸载 TiUP 自身：删除所有从镜像上下载过来的数据，但会保留 TiUP 及其组件产生的数据，数据存放在 `TIUP_HOME` 环境变量指定的目录中，若未设置过 `TIUP_HOME`，则默认值为 `~/.tiup/`。
- 数据类型：`BOOLEAN`
- 该选项默认关闭，默认值为 `false`。在命令中添加该选项，并传入 `true` 值或不传值，均可开启此功能。

## 输出

- 正常退出：`Uninstalled component "%s" successfully!`
- 若未指定 `<version>` 也未指定 `--all`：报错 `Use "tiup uninstall tidbx --all" if you want to remove all versions.`

[<< 返回上一页 - TiUP 命令清单](/tiup/tiup-reference.md#命令清单)