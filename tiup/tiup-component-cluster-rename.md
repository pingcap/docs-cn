---
title: tiup cluster rename
---

# tiup cluster rename

集群名字是[部署集群](/tiup/tiup-component-cluster-deploy.md)时指定的，在集群部署之后，如果想更改集群名字，可以通过 `tiup cluster rename` 命令来实现。

> **注意：**
>
> 如果配置了 `grafana_servers` 的 `dashboard_dir` 字段，在执行 tiup cluster rename 命令进行集群重命名后，需要额外做以下操作：
>
> + 对于本地的 dashboards 目录中的 `*.json` 文件，将 datasource 字段的值更新为新的集群名（这是因为 datasource 是以集群名命名的）
> + 执行 `tiup cluster reload -R grafana` 命令

## 语法

```shell
tiup cluster rename <old-cluster-name> <new-cluster-name> [flags]
```

- `<old-cluster-name>` 老的集群名
- `<new-cluster-name>` 新的集群名

## 选项

### -h, --help

- 输出帮助信息。
- 数据类型：`BOOLEAN`
- 该选项默认关闭，默认值为 `false`。在命令中添加该选项，并传入 `true` 值或不传值，均可开启此功能。

## 输出

tiup-cluster 的执行日志。

[<< 返回上一页 - TiUP Cluster 命令清单](/tiup/tiup-component-cluster.md#命令清单)