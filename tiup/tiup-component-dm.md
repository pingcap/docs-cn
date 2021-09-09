---
title: TiUP DM
---

# TiUP DM

类似于 [TiUP Cluster](/tiup/tiup-component-cluster.md) 对 TiDB 集群的管理，TiUP DM 是用于对 DM 集群的日常运维工作，包括部署、启动、关闭、销毁、弹性扩缩容、升级 DM 集群、管理 DM 集群参数。

## 语法

```shell
tiup dm [command] [flags]
```

`[command]` 代表命令名字，支持的命令列表请参考下方命令清单。

## 选项

### --ssh (string，默认 builtin)

指定 SSH 客户端连接远端（部署 TiDB 服务的机器）执行命令，支持以下几个值：

- builtin：使用 tiup-cluster 内置的 easyssh 客户端
- system：使用当前操作系统默认的 ssh 客户端
- none：不使用 ssh 客户端，这种方式只支持部署到当前机器

### --ssh-timeout（uint，默认 5）

设置 ssh 连接超时时间，单位为秒。

### --wait-timeout（uint，默认 120）

运维过程中涉及到很多操作：指定 systemctl 启动/停止服务，等待端口上线/下线等，每个操作可能会消耗数秒，`--wait-timeout` 用于设置每个步骤的最长等待时间（单位为秒），超时后报错退出。

### -y, --yes 

- 跳过所有风险操作的二次确认，除非是使用脚本调用 TiUP，否则不推荐使用。
- 数据类型：`BOOLEAN`
- 该选项默认关闭，默认值为 `false`。在命令中添加该选项，并传入 `true` 值或不传值，均可开启此功能。

### -v, --version

- 输出 tiup-dm 当前版本信息。
- 数据类型：`BOOLEAN`
- 该选项默认关闭，默认值为 `false`。在命令中添加该选项，并传入 `true` 值或不传值，均可开启此功能。

### -h, --help

- 输出相关命令的帮助信息。
- 数据类型：`BOOLEAN`
- 该选项默认关闭，默认值为 `false`。在命令中添加该选项，并传入 `true` 值或不传值，均可开启此功能。

## 命令清单

- [import](/tiup/tiup-component-dm-import.md)：导入使用  DM-Ansible 部署的 DM v1.0 集群
- [template](/tiup/tiup-component-dm-template.md)：输出拓扑模版
- [deploy](/tiup/tiup-component-dm-deploy.md)：根据指定拓扑部署集群
- [list](/tiup/tiup-component-dm-list.md)：查询已部署的集群列表
- [display](/tiup/tiup-component-dm-display.md)：展示指定集群状态
- [start](/tiup/tiup-component-dm-start.md)：启动指定集群
- [stop](/tiup/tiup-component-dm-stop.md)：停止指定集群
- [restart](/tiup/tiup-component-dm-restart.md)：重启指定集群
- [scale-in](/tiup/tiup-component-dm-scale-in.md)：缩容指定集群
- [scale-out](/tiup/tiup-component-dm-scale-out.md)：扩容指定集群
- [upgrade](/tiup/tiup-component-dm-upgrade.md)：升级指定集群
- [prune](/tiup/tiup-component-dm-prune.md)：销毁指定集群中状态为 Tombstone 的实例
- [edit-config](/tiup/tiup-component-dm-edit-config.md)：修改指定集群配置
- [reload](/tiup/tiup-component-dm-reload.md)：重载指定集群配置
- [patch](/tiup/tiup-component-dm-patch.md)：替换已部署集群的某个服务
- [destroy](/tiup/tiup-component-dm-destroy.md)：销毁指定集群
- [audit](/tiup/tiup-component-dm-audit.md)：查询集群操作审计日志
- [replay](/tiup/tiup-component-dm-replay.md)：重试指定命令
- [enable](/tiup/tiup-component-dm-enable.md)：开启指定集群或服务开机自启动
- [disable](/tiup/tiup-component-dm-disable.md)：关闭指定集群或服务开机自启动
- [help](/tiup/tiup-component-dm-help.md)：输出帮助信息

[<< 返回上一页 - TiUP 组件清单](/tiup/tiup-reference.md#组件清单)