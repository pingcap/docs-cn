---
title: tiup dm edit-config
---

# tiup dm edit-config

If you need to modify the cluster service configuration after the cluster is deployed, you can use the `tiup dm edit-config` command that starts an editor for you to modify the [topology file](/tiup/tiup-dm-topology-reference.md). of the specified cluster. This editor is specified in the `$EDITOR` environment variable by default. If the `$EDITOR` environment variable does not exist, the `vi` editor is used.

> **Note:**
>
> + When you modify the configuration, you cannot add or delete machines. For how to add machines, see [Scale out a cluster](/tiup/tiup-component-dm-scale-out.md). For how to delete machines, see [Scale in a cluster](/tiup/tiup-component-dm-scale-in.md).
> + After you execute the `tiup dm edit-config` command, the configuration is modified only on the control machine. Then you need to execute the `tiup dm relaod` command to reload the configuration.

## Syntax

```shell
tiup dm edit-config <cluster-name> [flags]
```

`<cluster-name>`: the cluster to operate on.

## Option

### -h, --help

- Prints the help information.
- Data type: `BOOLEAN`
- Default: false

## Output

- Normally, no output.
- If you have mistakenly modified the fields that cannot be modified, when you save the file, an error is reported, reminding you to edit the file again. For the fields that cannot be modified, see [the topology file](/tiup/tiup-dm-topology-reference.md).

[<< Back to the previous page - TiUP DM command list](/tiup/tiup-component-dm.md#command-list)
