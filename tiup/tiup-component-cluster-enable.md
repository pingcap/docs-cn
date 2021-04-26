---
title: tiup cluster enable
---

# tiup cluster enable

命令 `tiup cluster enable` 用于设置集群服务在机器重启后的自启动，该命令会到指定的节点上去执行 `systemctl enable <service>` 来开启服务的自启。

> **注意：**
>
> 集群全部关机重启时，服务启动的顺序由节点的操作系统启动顺序决定。重启顺序不正确时，在某些情况下，重启后的集群仍然不能提供服务（比如先启动了 TiKV 但未启动 PD，systemd 重启 TiKV 多次仍未找到 PD 则会放弃）。

## 语法

```shell
tiup cluster enable <cluster-name> [flags]
```

`<cluster-name>` 为要启用自启的集群。

## 选项

### -N, --node

- 指定要开启自启的节点，该选项的值为以逗号分割的节点 ID 列表，节点 ID 为[集群状态](/tiup/tiup-component-cluster-display.md)表格的第一列。
- 数据类型：`STRINGS`
- 如果不指定该选项，默认开启所有节点的自启。

> **注意：**
>
> 若同时指定了 `-R, --role`，那么将开启它们的交集中的服务自启。

### -R, --role

指定要开启自启的角色，该选项的值为以逗号分割的节点角色列表，角色为[集群状态](/tiup/tiup-component-cluster-display.md)表格的第二列。

> **注意：**
>
> 若同时指定了 `-N, --node`，那么将开启它们的交集中的服务自启。

### -h, --help

- 输出帮助信息。
- 数据类型：`BOOLEAN`
- 该选项默认关闭，默认值为 `false`。在命令中添加该选项，并传入 `true` 值或不传值，均可开启此功能。

## 输出

tiup-cluster 的执行日志。
