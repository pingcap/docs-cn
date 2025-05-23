---
title: tiup cluster template
summary: TiUP 内置了拓扑文件的模版，用户可以通过修改该模版来生成最终的拓扑文件。使用 tiup cluster template 命令可以输出 TiUP 内置的模版内容。该命令有多个选项，包括输出详细的拓扑模版、输出本地集群的简单拓扑模版以及输出多数据中心的拓扑模版。根据指定选项输出拓扑模版，可重定向到拓扑文件中用于部署。
---

# tiup cluster template

部署集群之前，需要准备一份集群的[拓扑文件](/tiup/tiup-cluster-topology-reference.md)。TiUP 内置了拓扑文件的模版，用户可以通过修改该模版来生成最终的拓扑文件。使用 `tiup cluster template` 命令可以输出 TiUP 内置的模版内容。

## 语法

```shell
tiup cluster template [flags]
```

如果不指定该选项，输出的默认模版包含以下实例：

- 3 个 PD 实例
- 3 个 TiKV 实例
- 3 个 TiDB 实例
- 2 个 TiFlash 实例
- 1 个 Prometheus 实例
- 1 个 Grafana 实例
- 1 个 Alertmanager 实例

## 选项

### --full

- 输出详细的拓扑模版，该模版会以注释的形式带上可配置的参数。在命令中添加该选项，可开启该选项。
- 如果不指定该选项，默认输出最简单的拓扑模版。

### --local

- 输出本地集群的简单拓扑模版，该模版可以直接使用，该模版中的 global 参数也可以按需调整。
- 该模板会创建一个 PD 服务、一个 TiDB 服务、一个 TiKV 服务、一个 Prometheus 服务、一个 Grafana 服务。

### --multi-dc

- 输出多数据中心的拓扑模版。在命令中添加该选项，可开启该选项。
- 如果不指定该选项，默认输出单地单机房的拓扑模版。

### -h, --help

输出帮助信息。

## 输出

根据指定选项输出拓扑模版，可重定向到拓扑文件中用于部署。