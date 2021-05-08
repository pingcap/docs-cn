---
title: tiup cluster template
---

# tiup cluster template

Before deploying the cluster, you need to prepare a [topology file](/tiup/tiup-cluster-topology-reference.md) of the cluster. TiUP has a built-in topology file template, and you can modify this template to create the final topology file. To output the built-in template content, you can use the `tiup cluster template` command.

## Syntax

```shell
tiup cluster template [flags]
```

If this option is not specified, the output default template contains the following instances:

- 3 PD instances
- 3 TiKV instances
- 1 TiDB instance
- 1 Prometheus instance
- 1 Grafana instance
- 1 Alertmanager instance

## Options

### --full

- Outputs a detailed topology template that is commented with configurable parameters. To enable this option, add it to the command.
- If this option is not specified, the simple topology template is output by default.

### --multi-dc

- Outputs the topology template of multiple data centers. To enable this option, add it to the command.
- If this option is not specified, the topology template of a single data center is output by default.

### -h, --help

Prints the help information.

## Output

Outputs the topology template according to the specified options, which can be redirected to the topology file for deployment.
