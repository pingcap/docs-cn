---
title: TiUP Cluster
aliases: ['/docs-cn/dev/tiup/tiup-component-cluster/']
---

# TiUP Cluster

## 介绍

TiUP Cluster 是 TiUP 提供的使用 Golang 编写的集群管理组件，通过 TiUP cluster 组件就可以进行日常的运维工作，包括部署、启动、关闭、销毁、弹性扩缩容、升级 TiDB 集群；管理 TiDB 集群参数。

## 语法

```sh
tiup cluster [command] [flags]
```

`[command]` 代表命令名字，支持的命令列表请参考下方命令清单。

## 选项

### --ssh (string，默认 builtin)

通过哪种 ssh 客户端到远端（部署 TiDB 服务的机器）执行命令，支持以下几个值：

- builtin：使用 tiup-cluster 内置的 easyssh 客户端
- system：使用当前操作系统默认的 ssh 客户端
- none：不使用 ssh 客户端，这种方式只支持部署到当前机器

### --ssh-timeout（uint，默认 5）

设置 ssh 连接超时时间，单位为秒。

### --wait-timeout（uint，默认 120）

设置执行命令的超时时间，单位为秒。

### -y, --yes (boolean，默认 false)

跳过所有二次确认，除非是使用脚本调用 TiUP，否则不推荐使用。

### -v, --version（boolean，默认 false）

输出 tiup-cluster 当前版本信息。

### -h, --help（boolean，默认 false）

输出相关命令的帮助信息。

## 命令清单

- import：导入 ansible 部署的集群
- check：部署前后的集群检查
- deploy：根据指定拓扑部署集群
- list：查询已部署的集群列表
- start：启动指定集群
- display：展示指定集群状态
- stop：停止指定集群
- restart：重启指定集群
- scale-in：缩容指定集群
- scale-out：扩容指定集群
- upgrade：升级指定集群
- exec：在指定集群的指定机器上执行命令
- prune：销毁指定集群中状态为 tombstone 的实例
- edit-config：修改指定集群配置
- reload：重载指定集群配置
- patch：替换已部署集群的某个服务
- rename：重命名集群
- clean：删除指定集群数据
- destroy：销毁指定集群
- audit：查询集群操作审计日志
- enable：开启指定集群或服务开机自启动
- disable：关闭指定集群或服务开机自启动
- help：输出帮助信息