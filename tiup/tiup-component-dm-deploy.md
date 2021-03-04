---
title: tiup dm deploy
---

# tiup dm deploy

命令 `tiup dm deploy` 用于部署一个全新的集群。

## 语法

```sh
tiup dm deploy <cluster-name> <version> <topology.yaml> [flags]
```

- `<cluster-name>` 表示新集群的名字，不能和现有集群同名
- `<version>` 为要部署的 DM 集群版本号，如 `v2.0.0`
- `<topology.yaml>` 为事先编写好的[拓扑文件](/tiup/tiup-dm-topology-reference.md)

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

部署日志。