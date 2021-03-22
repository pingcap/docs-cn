---
title: tiup cluster restart
---

# tiup cluster restart

命令 `tiup cluster restart` 用于重启指定集群的所有或部分服务。

> **注意：**
> 
> 重启过程中会有一段时间服务不可用。

## 语法

```sh
tiup cluster restart <cluster-name> [flags]
```

`<cluster-name>` 为要操作的集群名字，如果忘记集群名字可通过[集群列表](/tiup/tiup-component-cluster-list.md)查看。

## 选项

### -N, --node（strings，默认为 []，表示所有节点）

指定要重启的节点，不指定则表示所有节点。该选项的值为以逗号分割的节点 ID 列表，节点 ID 为[集群状态](/tiup/tiup-component-cluster-display.md)表格的第一列。

> **注意：**
> 
> 若同时指定了 `-R, --role`，那么将重启它们的交集中的服务。

### -R, --role strings（strings，默认为 []，表示所有角色）

指定要重启的角色，不指定则表示所有角色。该选项的值为以逗号分割的节点角色列表，角色为[集群状态](/tiup/tiup-component-cluster-display.md)表格的第二列。

> **注意：**
> 
> 若同时指定了 `-N, --node`，那么将重启它们的交集中的服务。

### -h, --help（boolean，默认 false）

输出帮助信息。

## 输出

重启服务的日志。