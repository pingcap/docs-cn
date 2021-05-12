---
title: tiup mirror merge
---

# tiup mirror merge

The `tiup mirror merge` command is used to merge one or more mirrors to the current mirror.

To execute this command, the following conditions must be met:

- The owner IDs of all components of the target mirror exist in the current mirror.
- The `${TIUP_HOME}/keys` directory of the user who executes this command contains all the private keys corresponding to the above owner IDs in the current mirror (you can use the command [`tiup mirror set`](/tiup/tiup-command-mirror-set.md) to switch the current mirror to the mirror that is currently authorized to modify).

## Syntax

```shell
tiup mirror merge <mirror-dir-1> [mirror-dir-N] [flags]
```

- `<mirror-dir-1>`: the first mirror to be merged into the current mirror
- `[mirror-dir-N]`: the Nth mirror to be merged into the current mirror

## Option

None

## Outputs

- If the command is executed successfully, there is no output.
- If the current mirror does not have a component owner of the target mirror, or if `${TIUP_HOME}/keys` does not have the owner's private key, TiUP reports the `Error: missing owner keys for owner %s on component %s` error.

[<< Back to the previous page - TiUP Mirror command list](/tiup/tiup-command-mirror.md#command-list)
