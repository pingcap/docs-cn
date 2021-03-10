---
title: tiup cluster template
---

# tiup cluster template

部署集群之前，需要准备一份集群的[拓扑文件](/tiup/tiup-cluster-topology-reference.md)，TiUP 内置了拓扑文件的模版，用户可以通过修改模版来生成最终的拓扑文件。命令 `tiup cluster template` 用于输出 TiUP 内置的模版内容。

## 语法

```sh
tiup cluster template [flags]
```

在不指定任何选项的情况下，输出默认模版：

- 3 个 PD
- 3 个 TiKV
- 1 个 TiDB
- 1 个 prometheus
- 1 个 grafana
- 1 个 alertmanager

## 选项

### --full（boolean，默认 false）

输出详细的拓扑模版。默认输出最简单的拓扑模版，打开该选项后，输出详细的拓扑模版，以注释的形式带上可配置的参数。

### --multi-dc（boolean，默认 false）

输出多数据中心的拓扑模版。默认输出单地单机房的拓扑模版，打开该选项后，会给出多数据中心的配置用例。

### -h, --help（boolean，默认 false）

输出帮助信息。

## 输出

根据指定选项输出拓扑模版，可重定向到拓扑文件中用于部署。