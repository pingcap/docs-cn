---
title: tiup dm upgrade
---

# tiup dm upgrade

命令 `tiup dm upgrade` 用于将指定集群升级到特定版本。

## 语法

```shell
tiup dm upgrade <cluster-name> <version> [flags]
```

- `<cluster-name>` 为要操作的集群名字，如果忘记集群名字可查看[集群列表](/tiup/tiup-component-dm-list.md)。
- `<version>` 为要升级到的目标版本，目前仅允许升级到比当前集群更高的版本，不允许升级到比当前集群更低的版本，即不允许降级。同时也不允许升级成 nightly 版本

## 选项

## --offline

声明当前集群处于离线状态。指定该选项时，TiUP DM 仅原地替换集群组件的二进制文件，不重启服务。

### -h, --help

- 输出帮助信息。
- 数据类型：`BOOLEAN`
- 该选项默认关闭，默认值为 `false`。在命令中添加该选项，并传入 `true` 值或不传值，均可开启此功能。

## 输出

升级服务的日志。
