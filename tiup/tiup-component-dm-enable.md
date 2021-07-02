---
title: tiup dm enable
---

# tiup dm enable

命令 `tiup dm enable` 用于设置集群服务在机器重启后的自启动，该命令会到指定的节点上去执行 `systemctl enable <service>` 来开启服务的自启。

## 语法

```shell
tiup dm enable <cluster-name> [flags]
```

`<cluster-name>` 为要启用自启的集群。

## 选项

### -N, --node

- 指定要开启自启的节点，该选项的值为以逗号分割的节点 ID 列表，节点 ID 为[集群状态](/tiup/tiup-component-dm-display.md)表格的第一列。
- 数据类型：`STRINGS`
- 如果不指定该选项，默认开启所有节点的自启。

> **注意：**
>
> 若同时指定了 `-R, --role`，那么将开启它们的交集中的服务自启。

### -R, --role

- 指定要开启自启的角色，该选项的值为以逗号分割的节点角色列表，角色为[集群状态](/tiup/tiup-component-dm-display.md)表格的第二列。
- 数据类型：`STRINGS`
- 如果不指定该选项，默认开启所有角色的自启。

> **注意：**
>
> 若同时指定了 `-N, --node`，那么将开启它们的交集中的服务自启。

### -h, --help

输出帮助信息。

## 输出

tiup-dm 的执行日志。

[<< 返回上一页 - TiUP DM 命令清单](/tiup/tiup-component-dm.md#命令清单)