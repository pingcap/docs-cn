---
title: tiup cluster disable
---

# tiup cluster disable

命令 `tiup cluster disable` 用于关闭集群服务所在机器重启之后的自启动，该命令会到指定的节点上去执行 `systemctl disable <service>` 来关闭服务的自启动。

## 语法

```shell
tiup cluster disable <cluster-name> [flags]
```

`<cluster-name>` 为要关闭自启的集群。

## 选项

### -N, --node

- 指定要关闭自启的节点，该选项的值为以逗号分割的节点 ID 列表，节点 ID 为[集群状态](/tiup/tiup-component-cluster-display.md)表格的第一列。
- 数据类型：`STRINGS`
- 如果不指定该选项，默认检查所有节点。
- 

> **注意：**
>
> 若同时指定了 `-R, --role`，那么将关闭它们的交集中的服务自启。

### -R, --role

- 指定要关闭自启的角色，该选项的值为以逗号分割的节点角色列表，角色为[集群状态](/tiup/tiup-component-cluster-display.md)表格的第二列。
- 数据类型：`STRINGS`
- 如果不指定该选项，默认关闭所有角色的自启。

> **注意：**
>
> 若同时指定了 `-N, --node`，那么将关闭它们的交集中的服务自启。

### -h, --help

- 输出帮助信息。
- 数据类型：`BOOLEAN`
- 该选项默认关闭，默认值为 `false`。在命令中添加该选项，并传入 `true` 值或不传值，均可开启此功能。

## 输出

tiup-cluster 的执行日志。
