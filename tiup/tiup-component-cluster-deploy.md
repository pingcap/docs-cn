---
title: tiup cluster deploy
---

# tiup cluster deploy

命令 `tiup cluster deploy` 用于部署一个全新的集群。

## 语法

```shell
tiup cluster deploy <cluster-name> <version> <topology.yaml> [flags]
```

- `<cluster-name>` 表示新集群的名字，不能和现有集群同名
- `<version>` 为要部署的 TiDB 集群版本号，如 `v5.2.0`
- `<topology.yaml>` 为事先编写好的[拓扑文件](/tiup/tiup-cluster-topology-reference.md)

## 选项

### -u, --user（string，默认为当前执行命令的用户）

指定连接目标机器的用户名，该用户在目标机器上需要有免密 sudo root 的权限。

### -i, --identity_file（string，默认 ~/.ssh/id_rsa）

指定连接目标机器的密钥文件。

### -p, --password

- 在连接目标机器时使用密码登录，不可和 `-i/--identity_file` 同时使用。
- 数据类型：`BOOLEAN`
- 该选项默认关闭，默认值为 `false`。在命令中添加该选项，并传入 `true` 值或不传值，均可开启此功能。

### --ignore-config-check

- 在组件二进制文件部署之后，TiUP 会对 TiDB，TiKV 和 PD 组件执行配置检查，检查方式为 `<binary> --config-check <config-file>`，其中 `<binary>` 为部署的二进制文件的路径，`<config-file>` 为根据用户配置生成的配置文件。如果想要跳过该项检查，可以使用该选项。
- 数据类型：`BOOLEAN`
- 该选项默认关闭，默认值为 `false`。在命令中添加该选项，并传入 `true` 值或不传值，均可开启此功能。

### --no-labels

- 当两个或多个 TiKV 部署到同一台机器时，会存在一个风险：由于 PD 无法感知集群的拓扑结构，可能将一个 Region 的多个副本调度到一台物理机上的不同 TiKV，这样这台物理机就成为了单点。为了避免这种情况，用户可以通过 label 来告诉 PD 不要将相同的 Region 调度到同一台机器上（配置方式参考[通过拓扑 label 进行副本调度](/schedule-replicas-by-topology-labels.md)）。
- 但是对于测试环境，可能并不在意是否将一个 Region 的副本调度到了同一台机器上，这个时候可以使用 `--no-labels` 来绕过检查。
- 数据类型：`BOOLEAN`
- 该选项默认关闭，默认值为 `false`。在命令中添加该选项，并传入 `true` 值或不传值，均可开启此功能。

### --skip-create-user

- 在部署集群时，tiup-cluster 会先检查拓扑文件中指定的用户名是否存在，如果不存在就会创建一个。指定 `--skip-create-user` 选项后不再检查用户是否存在，直接跳过创建步骤。
- 数据类型：`BOOLEAN`
- 该选项默认关闭，默认值为 `false`。在命令中添加该选项，并传入 `true` 值或不传值，均可开启此功能。

### -h, --help

- 输出帮助信息。
- 数据类型：`BOOLEAN`
- 该选项默认关闭，默认值为 `false`。在命令中添加该选项，并传入 `true` 值或不传值，均可开启此功能。

## 输出

部署日志。

[<< 返回上一页 - TiUP Cluster 命令清单](/tiup/tiup-component-cluster.md#命令清单)
