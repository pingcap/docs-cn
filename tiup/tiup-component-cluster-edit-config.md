---
title: tiup cluster edit-config
---

# tiup cluster edit-config

If you need to modify the cluster configuration after the cluster is deployed, you can use the `tiup cluster edit-config` command that starts an editor for you to modify the [topology file](/tiup/tiup-cluster-topology-reference.md) of a cluster. This editor is specified in the `$EDITOR` environment variable by default. If the `$EDITOR` environment variable does not exist, the `vi` editor is used.

> **Note:**
>
> + When you modify the configuration, you cannot add or delete machines. For how to add machines, see [Scale out a cluster](/tiup/tiup-component-cluster-scale-out.md). For how to delete machines, see [Scale in a cluster](/tiup/tiup-component-cluster-scale-in.md).
> + After you execute the `tiup cluster edit-config` command, the configuration is modified only on the control machine. Then you need to execute the `tiup cluster reload` command to reload the configuration.

## Syntax

```shell
tiup cluster edit-config <cluster-name> [flags]
```

`<cluster-name>` is the cluster to operate on.

## Option

### -h, --help

- Prints help information.
- Data type: `BOOLEAN`
- This option is disabled by default and its default value is `false`. To enable this option, you can add this option to the command, and pass the `true` value or do not pass any value.

## Output

- If the command is successfully executed, there is no output.
- If you have mistakenly modified the fields that cannot be modified, when you save the file, an error will be reported, reminding you to edit the file again. For the fields that cannot be modified, see the [topology file](/tiup/tiup-cluster-topology-reference.md).

[<< Back to the previous page - TiUP Cluster command list](/tiup/tiup-component-cluster.md#command-list)
