---
title: tiup cluster upgrade
---

# tiup cluster upgrade

命令 `tiup cluster upgrade` 用于将指定集群升级到特定版本。

## 语法

```shell
tiup cluster upgrade <cluster-name> <version> [flags]
```

- `<cluster-name>` 为要操作的集群名字，如果忘记集群名字可通过[集群列表](/tiup/tiup-component-cluster-list.md)查看。
- `<version>` 为要升级到的目标版本，例如 `v7.1.5`。目前仅允许升级到比当前集群更高的版本，不允许升级到比当前集群更低的版本，即不允许降级。同时也不允许升级成 nightly 版本。

## 选项

### --force

- 升级集群需要保证集群目前是启动的，在某些情况下，可能希望在集群未启动的状态下升级，这时候可以使用 `--force` 忽略升级过程的错误，强制替换二进制文件并启动集群。
- 数据类型：`BOOLEAN`
- 该选项默认关闭，默认值为 `false`。在命令中添加该选项，并传入 `true` 值或不传值，均可开启此功能。

> **注意：**
>
> 对正在提供服务的集群强制升级可能导致集群服务不可用。对于未启动的集群，升级成功后会自动启动集群。

### --transfer-timeout（uint，默认 600）

在升级 PD 或 TiKV 时，会先将被升级节点的 leader 迁移到其他节点，迁移过程会需要一定时间，可以通过设置 `--transfer-timeout` 设置最长等待时间（单位为秒），超时之后会跳过等待直接升级服务。

> **注意：**
>
> 若出现跳过等待直接升级的情况，服务性能可能会出现抖动。

### --ignore-config-check

- 在二进制文件更新之后，TiUP 会对 TiDB，TiKV 和 PD 组件执行配置检查，检查方式为 `<binary> --config-check <config-file>`，其中 `<binary>` 为新部署的二进制文件的路径，`<config-file>` 为根据用户配置生成的配置文件。如果想要跳过该项检查，可以使用该选项。
- 数据类型：`BOOLEAN`
- 该选项默认关闭，默认值为 `false`。在命令中添加该选项，并传入 `true` 值或不传值，均可开启此功能。

### --offline

- 声明当前集群处于停止状态。指定该选项时，TiUP Cluster 仅原地替换集群组件的二进制文件，不执行迁移 Leader 以及重启服务等操作。
- 数据类型：`BOOLEAN`
- 该选项默认关闭，默认值为 `false`。在命令中添加该选项，并传入 `true` 值或不传值，均可开启此功能。

### --pd-version

- 指定 PD 的版本。指定后，PD 的版本将不再与集群版本保持一致。
- 数据类型：`STRINGS`
- 不指定该选项时，PD 的版本与集群版本保持一致。

### --tikv-version

- 指定 TiKV 的版本。指定后，TiKV 的版本将不再与集群版本保持一致。
- 数据类型：`STRINGS`
- 不指定该选项时，TiKV 的版本与集群版本保持一致。

### --tikv-cdc-version

- 指定 TiKV CDC 的版本。指定后，TiKV CDC 的版本将不再与集群版本保持一致。
- 数据类型：`STRINGS`
- 不指定该选项时，TiKV CDC 的版本与集群版本保持一致。

### --tiflash-version

- 指定 TiFlash 的版本。指定后，TiFlash 的版本将不再与集群版本保持一致。
- 数据类型：`STRINGS`
- 不指定该选项时，TiFlash 的版本与集群版本保持一致。

### --cdc-version

- 指定 TiCDC 的版本。指定后，TiCDC 的版本将不再与集群版本保持一致。
- 数据类型：`STRINGS`
- 不指定该选项时，TiCDC 的版本与集群版本保持一致。

### --tiproxy-version

- 指定 TiProxy 的版本。指定后，TiProxy 的版本将不再与集群版本保持一致。
- 数据类型：`STRINGS`
- 不指定该选项时，TiProxy 的版本与集群版本保持一致。

### --tidb-dashboard-version

- 指定 TiDB Dashboard 的版本。指定后，TiDB Dashboard 的版本将不再与集群版本保持一致。
- 数据类型：`STRINGS`
- 不指定该选项时，TiDB Dashboard 的版本与集群版本保持一致。

### --alertmanager-version

- 指定 alert manager 的版本。指定后，alert manager 的版本将不再与集群版本保持一致。
- 数据类型：`STRINGS`
- 不指定该选项时，alert manager 的版本与集群版本保持一致。

### --blackbox-exporter-version

- 指定 Blackbox Exporter 的版本。指定后，Blackbox Exporter 的版本将不再与集群版本保持一致。
- 数据类型：`STRINGS`
- 不指定该选项时，Blackbox Exporter 的版本与集群版本保持一致。

### --node-exporter-version

- 指定 Node Exporter 的版本。指定后，Node Exporter 的版本将不再与集群版本保持一致。
- 数据类型：`STRINGS`
- 不指定该选项时，Node Exporter 的版本与集群版本保持一致。

### --restart-timeout

- 指定滚动升级之间的间隔，即在升级组件后等待一段时间。
- 数据类型: `STRINGS`。支持所有 [`golang time.ParseDuration`](https://pkg.go.dev/time#ParseDuration) 能够解析的数据类型。
- 默认值：`0`
- 不指定该选项时，升级组件后不会等待。

### -h, --help

- 输出帮助信息。
- 数据类型：`BOOLEAN`
- 该选项默认关闭，默认值为 `false`。在命令中添加该选项，并传入 `true` 值或不传值，均可开启此功能。

## 输出

升级服务的日志。

[<< 返回上一页 - TiUP Cluster 命令清单](/tiup/tiup-component-cluster.md#命令清单)