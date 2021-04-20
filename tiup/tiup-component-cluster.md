---
title: TiUP Cluster
---

# TiUP Cluster

TiUP Cluster 是 TiUP 提供的使用 Golang 编写的集群管理组件，通过 TiUP Cluster 组件就可以进行日常的运维工作，包括部署、启动、关闭、销毁、弹性扩缩容、升级 TiDB 集群、管理 TiDB 集群参数。

## 语法

```shell
tiup cluster [command] [flags]
```

`[command]` 代表命令名字，支持的命令列表请参考下方命令清单。

## 选项

### --ssh (string，默认 builtin)

指定 SSH 客户端连接远端（部署 TiDB 服务的机器）执行命令，支持以下值：

- builtin：使用 tiup-cluster 内置的 easyssh 客户端
- system：使用当前操作系统默认的 SSH 客户端
- none：不使用 ssh 客户端，这种方式只支持部署到当前机器

### --ssh-timeout（uint，默认 5）

设置 SSH 连接超时时间，单位为秒。

### --wait-timeout（uint，默认 120）

运维过程中涉及到很多操作：指定 systemctl 启动/停止服务，等待端口上线/下线等，每个操作可能会消耗数秒。`--wait-timeout` 用于设置每个步骤的最长等待时间（单位为秒），超时后报错退出。

### -y, --yes 

- 跳过所有风险操作的二次确认，除非是使用脚本调用 TiUP，否则不推荐使用。
- 数据类型：`BOOLEAN`
- 该选项默认关闭，默认值为 `false`。在命令中添加该选项，并传入 `true` 值或不传值，均可开启此功能。

### -v, --version

- 输出 TiUP Cluster 当前版本信息。
- 数据类型：`BOOLEAN`
- 该选项默认关闭，默认值为 `false`。在命令中添加该选项，并传入 `true` 值或不传值，均可开启此功能。

### -h, --help

- 输出相关命令的帮助信息。
- 数据类型：`BOOLEAN`
- 该选项默认关闭，默认值为 `false`。在命令中添加该选项，并传入 `true` 值或不传值，均可开启此功能。

## 命令清单

- [import](/tiup/tiup-component-cluster-import.md)：导入 ansible 部署的集群
- [check](/tiup/tiup-component-cluster-check.md)：部署前后的集群检查
- [deploy](/tiup/tiup-component-cluster-deploy.md)：根据指定拓扑部署集群
- [list](/tiup/tiup-component-cluster-list.md)：查询已部署的集群列表
- [display](/tiup/tiup-component-cluster-display.md)：展示指定集群状态
- [start](/tiup/tiup-component-cluster-start.md)：启动指定集群
- [stop](/tiup/tiup-component-cluster-stop.md)：停止指定集群
- [restart](/tiup/tiup-component-cluster-restart.md)：重启指定集群
- [scale-in](/tiup/tiup-component-cluster-scale-in.md)：缩容指定集群
- [scale-out](/tiup/tiup-component-cluster-scale-out.md)：扩容指定集群
- [upgrade](/tiup/tiup-component-cluster-upgrade.md)：升级指定集群
- [prune](/tiup/tiup-component-cluster-prune.md)：销毁指定集群中状态为 Tombstone 的实例
- [edit-config](/tiup/tiup-component-cluster-edit-config.md)：修改指定集群配置
- [reload](/tiup/tiup-component-cluster-reload.md)：重载指定集群配置
- [patch](/tiup/tiup-component-cluster-patch.md)：替换已部署集群的某个服务
- [rename](/tiup/tiup-component-cluster-rename.md)：重命名集群
- [clean](/tiup/tiup-component-cluster-clean.md)：删除指定集群数据
- [destroy](/tiup/tiup-component-cluster-destroy.md)：销毁指定集群
- [audit](/tiup/tiup-component-cluster-audit.md)：查询集群操作审计日志
- [enable](/tiup/tiup-component-cluster-enable.md)：开启指定集群或服务开机自启动
- [disable](/tiup/tiup-component-cluster-disable.md)：关闭指定集群或服务开机自启动
- [help](/tiup/tiup-component-cluster-help.md)：输出帮助信息
