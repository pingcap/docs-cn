---
title: tiup dm upgrade
---

# tiup dm upgrade

命令 `tiup dm upgrade` 用于将指定集群升级到特定版本。

## 语法

```sh
tiup dm upgrade <cluster-name> <version> [flags]
```

- `<cluster-name>` 为要操作的集群名字，如果忘记集群名字可查看[集群列表](/tiup/tiup-component-dm-list.md)。
- `<version>` 为要升级到的目标版本，目前仅允许升级到比当前集群更高的版本，不允许升级到比当前集群更低的版本，即不允许降级。同时也不允许升级成 nightly 版本

## 选项

### -h, --help（boolean，默认 false）

输出帮助信息。

## 输出

升级服务的日志。
