---
title: tiup dm template
---

# tiup dm template

部署集群之前，需要准备一份集群的[拓扑文件](/tiup/tiup-dm-topology-reference.md)。TiUP 内置了拓扑文件的模版，用户可以通过修改模版来生成最终的拓扑文件。使用 `tiup dm template` 命令可以输出 TiUP 内置的模版内容。

## 语法

```shell
tiup dm template [flags]
```

如果不指定该选项，输出的默认模版包含以下角色：

- 3 个 DM-master 节点
- 3 个 DM-worker 节点
- 1 个 Prometheus
- 1 个 Grafana
- 1 个 Alertmanager

## 选项

### --full

- 输出详细的拓扑模版，该模版会以注释的形式带上可配置的参数。在命令中添加该选项，可开启该选项。
- 如果不指定该选项，默认输出最简单的拓扑模版。

### -h, --help

输出帮助信息。

## 输出

根据指定选项输出拓扑模版到标准输出，可重定向到拓扑文件中用于部署。
