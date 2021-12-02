---
title: tiup dm reload
---

# tiup dm reload

在[修改集群配置](/tiup/tiup-component-dm-edit-config.md)之后，需要通过 `tiup dm reload` 命令让集群重新加载配置才会生效，该命令会将中控机的配置发布到服务运行的远端机器，并按照升级的流程按顺序重启服务，重启过程中集群仍然可用。

## 语法

```shell
tiup dm reload <cluster-name> [flags]
```

`<cluster-name>` 代表要操作的集群名。

## 选项

### -N, --node（strings，默认为 []，表示所有节点）

指定要重启的节点，不指定则表示所有节点。该选项的值为以逗号分割的节点 ID 列表，节点 ID 为[集群状态](/tiup/tiup-component-dm-display.md)表格的第一列。

> **注意：**
>
> + 若同时指定了 `-R, --role`，那么将重启它们的交集中的服务
> + 若指定了选项 `--skip-restart`，则该选项无效

### -R, --role（strings，默认为 []，表示所有角色）

指定要重启的角色，不指定则表示所有角色。该选项的值为以逗号分割的节点角色列表，角色为[集群状态](/tiup/tiup-component-dm-display.md)表格的第二列。

> **注意：**
>
> + 若同时指定了 `-N, --node`，那么将重启它们的交集中的服务
> + 若指定了选项 `--skip-restart`，则该选项无效

### --skip-restart

- 命令 `tiup dm reload` 会执行两个操作：

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

tiup-dm 的执行日志。

[<< 返回上一页 - TiUP DM 命令清单](/tiup/tiup-component-dm.md#命令清单)