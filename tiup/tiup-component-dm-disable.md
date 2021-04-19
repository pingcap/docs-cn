---
title: tiup dm disable
---

# tiup dm disable

命令 `tiup dm disable` 用于关闭集群服务所在机器重启之后的自启动，该命令会到指定的节点上去执行 `systemctl disable <service>` 来关闭服务的自启动。

## 语法

```sh
tiup dm disable <cluster-name> [flags]
```

`<cluster-name>` 为要关闭自启的集群。

## 选项

### -N, --node（strings，默认为 []，未选中任何节点）

指定要关闭自启的节点，该选项的值为以逗号分割的节点 ID 列表，节点 ID 为[集群状态](/tiup/tiup-component-dm-display.md)表格的第一列。

> **注意：**
>
> 若同时指定了 `-R, --role`，那么将关闭它们的交集中的服务自启。

### -R, --role strings（strings，默认为 []，未选中任何角色）

指定要关闭自启的角色，该选项的值为以逗号分割的节点角色列表，角色为[集群状态](/tiup/tiup-component-dm-display.md)表格的第二列。

> **注意：**
>
> 若同时指定了 `-N, --node`，那么将关闭它们的交集中的服务自启。

### -h, --help（boolean，默认 false）

输出帮助信息。

## 输出

tiup-dm 的执行日志。