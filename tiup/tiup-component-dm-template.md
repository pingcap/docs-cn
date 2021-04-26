---
title: tiup dm template
---

# tiup dm template

部署集群之前，需要准备一份集群的[拓扑文件](/tiup/tiup-dm-topology-reference.md)，TiUP 内置了拓扑文件的模版，用户可以通过修改模版来生成最终的拓扑文件。命令 `tiup dm template` 用于输出 TiUP 内置的模版内容。

## 语法

```shell
tiup dm template [flags]
```

在不指定任何选项的情况下，输出默认模版：

- 3 个 DM Master
- 3 个 DM Worker
- 1 个 Prometheus
- 1 个 Grafana
- 1 个 Alertmanager

## 选项

### --full

输出详细的拓扑模版。默认输出最简单的拓扑模版，打开该选项后，输出详细的拓扑模版，以注释的形式带上可配置的参数。

### -h, --help

输出帮助信息。

## 输出

根据指定选项输出拓扑模版到标准输出，可重定向到拓扑文件中用于部署。
