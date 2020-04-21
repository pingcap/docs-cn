---
title: TiUP 常见运维操作
category: how-to
---

# TiUP 常见运维操作

## 查看集群列表

一个 TiUP 可以管理多个集群，在集群部署完毕之后它会出现在 TiUP 的集群列表里，可以使用 list 命令来查看。

{{< copyable "shell-regular" >}}

```bash
tiup cluster list
```

## 启动集群

此操作会按顺序启动整个 TiDB 集群所有组件（包括 PD、TiDB、TiKV 等组件和监控组件）。

{{< copyable "shell-regular" >}}

```bash
tiup cluster start <cluster-name>
```

> 请将 `<cluster-name>` 替换成实际的集群名字，若忘记集群名字，可通过 `tiup cluster list` 查看

该命令支持通过 `-R` 和 `-N` 参数来只启动部分组件，例如下面的命令只启动 test-cluster 的 pd 组件

```bash
tiup cluster start test-cluster -R pd
```

而下面的命令只启动 `1.2.3.4` 和 `1.2.3.5` 这两台机器上的 pd 组件

```bash
tiup cluster start test-cluster -R pd -N 1.2.3.4:2379,1.2.3.5:2379
```

> **注意：**
>
> 若通过 `-R` 和 `-N` 启动指定组件，需要保证启动顺序正确（例如要先启动 PD 才能启动 TiKV），否则可能启动失败

## 查看集群状态

集群启动之后可能需要检查每个组件的运行状态，以确保每个组件工作正常，TiUP 提供了 display 命令可以免去登陆到每台机器上去查看进程的烦恼。

{{< copyable "shell-regular" >}}

```bash
tiup cluster display <cluster-name>
```

## 关闭集群

此操作会按顺序关闭整个 TiDB 集群所有组件（包括 PD、TiDB、TiKV 等组件和监控组件）

{{< copyable "shell-regular" >}}

```bash
tiup cluster stop <cluster-name>
```

和 `start` 命令类似，`stop` 命令也支持通过 `-R` 和 `-N` 参数来只停止部分组件，例如下面的命令只停止 test-cluster 的 tidb 组件

```bash
tiup cluster start test-cluster -R tidb
```

而下面的命令只启动 `1.2.3.4` 和 `1.2.3.5` 这两台机器上的 tidb 组件

```bash
tiup cluster start test-cluster -R tidb -N 1.2.3.4:4000,1.2.3.5:4000
```

## 销毁集群

此操作会关闭服务，清空数据目录和部署目录，并且无法恢复，请谨慎操作。

{{< copyable "shell-regular" >}}

```bash
tiup cluster stop <cluster-name>
```
