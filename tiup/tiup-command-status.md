---
title: tiup status
summary: The "tiup status" command is used to view the operation information of the components after running them using the "tiup <component>" command. It shows the name, component, PID, status, created time, directory, binary, and arguments of the operating components. The component status can be Up, Down, Tombstone, Pending Offline, or Unknown. The status is derived from the PD scheduling information.
---

# tiup status

The `tiup status` command is used to view the operation information of the components after you run the components using the `tiup [flags] <component> [args...]` command.

> **Note:**
>
> You can only check the information of the following components:
>
> - Components that are still in operation
> - Components that run through the tag specified by `tiup -T/--tag`

## Syntax

```shell
tiup status [flags]
```

## Option

None

## Output

A table consisting of the following fields:

- `Name`: The tag name specified by `-T/--tag`. If not specified, it is a random string.
- `Component`: The operating components.
- `PID`: The corresponding process ID of the operating components.
- `Status`: The status of the operating components.
- `Created Time`: The starting time of the components.
- `Directory`: The data directory of the components.
- `Binary`: The binary file path of the components.
- `Args`: The starting arguments of the operating components.

### Component status

A component can run in one of the following statuses:

- Up: The component is running normally.
- Down or Unreachable: The component is not running or a network problem exists on the corresponding host.
- Tombstone: The data on the component has been completely migrated out and the scaling-in is complete. This status exists only on TiKV or TiFlash.
- Pending Offline: The data on the component is being migrated out and the scaling-in is in process. This status exists only on TiKV or TiFlash.
- Unknown: The running status of the component is unknown.

> **Note:**
>
> `Pending Offline` in TiUP, `Offline` returned by PD API, and `Leaving` in TiDB Dashboard indicate the same status.

Component status derives from the PD scheduling information. For more details, see [Information collection](/tidb-scheduling.md#information-collection).

[<< Back to the previous page - TiUP Reference command list](/tiup/tiup-reference.md#command-list)
