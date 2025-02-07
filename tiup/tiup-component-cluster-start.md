---
title: tiup cluster start
summary: tiup cluster start 命令用于启动指定集群的所有或部分服务。语法为 tiup cluster start <cluster-name> [flags]。选项包括 --init（以安全方式启动集群）、-N, --node（指定要启动的节点）、-R, --role（指定要启动的角色）、-h, --help。输出为启动日志。
---

# tiup cluster start

命令 `tiup cluster start` 用于启动指定集群的所有或部分服务。

## 语法

```shell
tiup cluster start <cluster-name> [flags]
```

`<cluster-name>` 为要操作的集群名字，如果忘记集群名字可通过[集群列表](/tiup/tiup-component-cluster-list.md)查看。

## 选项

### --init

以安全方式启动集群。推荐在集群第一次启动时使用，该方式会在启动时自动生成 TiDB root 用户的密码，并在命令行界面返回密码。

> **注意：**
>
> - 使用安全启动方式后，不能通过无密码的 root 用户登录数据库，你需要记录命令行返回的密码进行后续操作。
> - 该自动生成的密码只会返回一次，如果没有记录或者忘记该密码，请参照[忘记 root 密码](/user-account-management.md#忘记-root-密码)修改密码。

### -N, --node（strings，默认为 []，表示所有节点）

指定要启动的节点，不指定则表示所有节点。该选项的值为以逗号分割的节点 ID 列表，节点 ID 为[集群状态](/tiup/tiup-component-cluster-display.md)表格的第一列。

> **注意：**
>
> 若同时指定了 `-R, --role`，那么将启动它们的交集中的服务。

### -R, --role（strings，默认为 []，表示所有角色）

指定要启动的角色，不指定则表示所有角色。该选项的值为以逗号分割的节点角色列表，角色为[集群状态](/tiup/tiup-component-cluster-display.md)表格的第二列。

> **注意：**
>
> 若同时指定了 `-N, --node`，那么将启动它们的交集中的服务。

### -h, --help

- 输出帮助信息。
- 数据类型：`BOOLEAN`
- 该选项默认关闭，默认值为 `false`。在命令中添加该选项，并传入 `true` 值或不传值，均可开启此功能。

## 输出

启动日志。

## 另请参阅

- [TiUP 常见运维操作](/maintain-tidb-using-tiup.md)