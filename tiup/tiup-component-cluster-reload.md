---
title: tiup cluster reload
---

# tiup cluster reload

在[修改集群配置](/tiup/tiup-component-cluster-edit-config.md)之后，需要通过 `tiup cluster reload` 命令让集群重新加载配置才会生效，该命令会将中控机的配置发布到服务运行的远端机器，并按照升级的流程按顺序重启服务，重启过程中集群仍然可用。

## 语法

```shell
tiup cluster reload <cluster-name> [flags]
```

`<cluster-name>` 代表要操作的集群名。

## 选项

### --force

- 忽略重新加载过程中的错误，强制 reload。
- 数据类型：`BOOLEAN`
- 该选项默认关闭，默认值为 `false`。在命令中添加该选项，并传入 `true` 值或不传值，均可开启此功能。

### --transfer-timeout（uint，默认 300）

在重启 PD 或 TiKV 时，会先将被重启节点的 leader 迁移到其他节点，迁移过程会需要一定时间，可以通过设置 `--transfer-timeout` 设置最长等待时间（单位为秒），超时之后会跳过等待直接重启服务。

> **注意：**
>
> 若出现跳过等待直接重启的情况，服务性能可能会出现抖动。

### --ignore-config-check

- 在组件二进制文件部署之后，TiUP 会对 TiDB，TiKV 和 PD 组件执行配置检查，检查方式为 `<binary> --config-check <config-file>`，其中 `<binary>` 为部署的二进制文件的路径，`<config-file>` 为根据用户配置生成的配置文件。如果想要跳过该项检查，可以使用该选项。
- 数据类型：`BOOLEAN`
- 该选项默认关闭，默认值为 `false`。在命令中添加该选项，并传入 `true` 值或不传值，均可开启此功能。

### -N, --node（strings，默认为 []，表示所有节点）

指定要重启的节点，不指定则表示所有节点。该选项的值为以逗号分割的节点 ID 列表，节点 ID 为[集群状态](/tiup/tiup-component-cluster-display.md)表格的第一列。

> **注意：**
>
> + 若同时指定了 `-R, --role`，那么将重启它们的交集中的服务
> + 若指定了选项 `--skip-restart`，则该选项无效

### -R, --role（strings，默认为 []，表示所有角色）

指定要重启的角色，不指定则表示所有角色。该选项的值为以逗号分割的节点角色列表，角色为[集群状态](/tiup/tiup-component-cluster-display.md)表格的第二列。

> **注意：**
>
> 1. 若同时指定了 `-N, --node`，那么将重启它们的交集中的服务
> 2. 若指定了选项 `--skip-restart`，则该选项无效

### --skip-restart

- 命令 `tiup cluster reload` 会执行两个操作：

    - 刷新所有节点配置
    - 重启指定节点

- 该选项指定后仅刷新配置，不重启任何节点，这样刷新的配置也不会应用，需要等对应服务下次重启才会生效。
- 数据类型：`BOOLEAN`
- 该选项默认关闭，默认值为 `false`。在命令中添加该选项，并传入 `true` 值或不传值，均可开启此功能。

### -h, --help

- 输出帮助信息。
- 数据类型：`BOOLEAN`
- 该选项默认关闭，默认值为 `false`。在命令中添加该选项，并传入 `true` 值或不传值，均可开启此功能。

## 输出

tiup-cluster 的执行日志。
