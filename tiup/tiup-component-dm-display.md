---
title: tiup dm display
---

# tiup dm display

如果想查看集群中每个组件的运行状态，逐一登录到各个机器上查看显然很低效。因此，tiup-dm 提供了 `tiup dm display` 命令来高效完成这件工作。

## 语法

```sh
tiup dm display <cluster-name> [flags]
```

`<cluster-name>` 为要操作的集群名字，如果忘记集群名字可查看[集群列表](/tiup/tiup-component-dm-list.md)。

## 选项

### -N, --node（strings，默认为 []，表示所有节点）

指定要查询的节点，不指定则表示所有节点。该选项的值为以逗号分割的节点 ID 列表，节点 ID 为[集群状态](/tiup/tiup-component-dm-display.md)表格的第一列。

> **注意：**
> 
> 若同时指定了 `-R, --role`，那么将查询它们的交集中的服务状态。

### -R, --role strings（strings，默认为 []，表示所有角色）

指定要查询的角色，不指定则表示所有角色。该选项的值为以逗号分割的节点角色列表，角色为[集群状态](/tiup/tiup-component-dm-display.md)表格的第二列。

> **注意：**
> 
> 若同时指定了 `-N, --node`，那么将查询它们的交集中的服务状态。

### -h, --help（boolean，默认 false）

输出帮助信息。

## 输出

- 集群名称
- 集群版本
- SSH 客户端类型
- 含有以下字段的表格：
    - ID：节点 ID，由 IP:PORT 构成
    - Role：该节点部署的服务角色（如 TiDB 和 TiKV 等）
    - Host：该节点对应的机器 IP
    - Ports：服务占用的端口号
    - OS/Arch：该节点的操作系统和机器架构
    - Status：该节点服务当前的状态
    - Data Dir：服务的数据目录，`-` 表示没有数据目录
    - Deploy Dir：服务的部署目录
