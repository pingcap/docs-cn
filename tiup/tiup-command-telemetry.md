---
title: tiup telemetry
---

# tiup telemetry

Starting from v1.11.3, the telemetry is disabled by default in newly deployed TiUP, and usage information is not collected and shared with PingCAP. In versions earlier than v1.11.3, the telemetry is enabled by default in TiUP, and usage information is collected and shared with PingCAP to improve the product.

When TiUP telemetry is enabled, usage information is shared with PingCAP when TiUP commands are executed, including (but not limited to):

- Randomly generated telemetry identifiers.
- The execution status of the TiUP command, such as whether the command execution is successful and the duration of command execution.
- Situations using TiUP for deployment, such as target machine hardware information, component version number, and modified deployment configuration name.

The information below is not shared:

- The accurate name of the cluster
- The cluster topology
- The cluster configuration file

TiUP uses the `tiup telemetry` command to control telemetry.

## Syntax

```shell
tiup telemetry <command>
```

`<command>` stands for sub-commands. For the list of supported sub-commands, refer to the commands section below.

## Commands

### status

The `tiup telemetry status` command is used to view the current telemetry settings and output the following information:

- `status`: specifies enabling or disabling the telemetry `(enable|disable)`.
- `uuid`: specifies the randomly generated telemetry identifiers.

### reset

The `tiup telemetry reset` command is used to reset the current telemetry identifier and replaces it with a new random identifier.

### enable

The `tiup telemetry enable` command is used to enable the telemetry.

### disable

The `tiup telemetry disable` command is used to disable the telemetry.

[<< Back to the previous page - TiUP Reference command list](/tiup/tiup-reference.md#command-list)
