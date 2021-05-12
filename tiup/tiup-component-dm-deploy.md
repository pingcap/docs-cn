---
title: tiup dm deploy
---

# tiup dm deploy

The `tiup dm deploy` command is used to deploy a new cluster.

## Syntax

```shell
tiup dm deploy <cluster-name> <version> <topology.yaml> [flags]
```

- `<cluster-name>`: the name of the new cluster, which cannot be the same as the existing cluster names.
- `<version>`: the version number of the DM cluster to be deployed, such as `v2.0.0`.
- `<topology.yaml>`: the prepared [topology file](/tiup/tiup-dm-topology-reference.md).

## Options

### -u, --user

- Specifies the user name used to connect to the target machine. This user must have the secret-free sudo root permission on the target machine.
- Data type: `STRING`
- Default: the current user who executes the command.

### -i, --identity_file

- Specifies the key file used to connect to the target machine.
- Data type: `STRING`
- Default: `~/.ssh/id_rsa`

### -p, --password

- Specifies the password used to connect to the target machine. Do not use this option and `-i/--identity_file` at the same time.
- Data type: `BOOLEAN`
- Default: false

### -h, --help

- Prints the help information.
- Data type: `BOOLEAN`
- Default: false

## Output

The deployment log.

[<< Back to the previous page - TiUP DM command list](/tiup/tiup-component-dm.md#command-list)
