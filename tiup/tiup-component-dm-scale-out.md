---
title: tiup dm scale-out
---

# tiup dm scale-out

`tiup dm scale-out` 命令用于集群扩容，扩容的内部逻辑与部署类似，tiup-dm 组件会先建立新节点的 SSH 连接，在目标节点上创建必要的目录，然后执行部署并且启动服务。

## 语法

```sh
tiup dm scale-out <cluster-name> <topology.yaml> [flags]
```

- `<cluster-name>` 为要操作的集群名字，如果忘记集群名字可查看[集群列表](/tiup/tiup-component-dm-list.md)
- `<topology.yaml>` 为事先编写好的扩容[拓扑文件](/tiup/tiup-dm-topology-reference.md)，该文件应当仅包含扩容部分的拓扑

## 选项

### -u, --user（string，默认为当前执行命令的用户）

指定连接目标机器的用户名，该用户在目标机器上需要有免密 sudo root 的权限。

### -i, --identity_file（string，默认 ~/.ssh/id_rsa）

指定连接目标机器的密钥文件。

### -p, --password（boolean，默认 false）

在连接目标机器时使用密码登陆，不可和 `-i/--identity_file` 同时使用。

### -h, --help（boolean，默认 false）

输出帮助信息。

## 输出

扩容日志