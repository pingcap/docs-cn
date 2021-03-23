---
title: tiup cluster clean
---

# tiup cluster clean

In the test environment, sometimes you might need to reset the cluster back to the state as it has been just deployed, which means deleting all data. You can do that easily using the `tiup cluster clean` command. After running it, the cluster is stopped and then cluster data is deleted. After restarting the cluster manually, you will get a clean cluster.

> **Warning:**
>
> This command will first stop the cluster even if you choose only to clean up logs. Therefore, do not use it in a production environment.

## Syntax

```sh
tiup cluster clean <cluster-name> [flags]
```

`<cluster-name>` is the cluster to clean.

## Options

### --all

- Cleans data and the log at the same time. It is equivalent to specifying `--data` and `--log` at the same time.
- Data type: `BOOLEAN`
- Default: false
- If it is not specified, you must specify at lease one of the following options:
    - --data: Cleans data
    - --log: Cleans the log

### --data

- Cleans data. If neither of it nor `--all` is specified, data will not be cleaned.
- Data type: `BOOLEAN`
- Default: false

### --log

- Cleans the log. If neither of it nor `--all` is specified, the log will not be cleaned.
- Data type: `BOOLEAN`
- Default: false

### --ignore-node

- Specifies the node that does not need cleaning. To specify multiple nodes, you can use this option multiple times. For example, `--ignore-node <node-A> --ignore-node <node-B>`.
- Data type: `StringArray`
- Default: empty

### --ignore-role

- Specifies the role that does not need cleaning. To specify multiple roles, you can use this option multiple times. For example, `--ignore-role <role-A> --ignore-role <role-B>`.
- Data type: `StringArray`
- Default: empty

### -h, --help

- Prints help information.
- Data type: `BOOLEAN`
- Default: false

## Output

The execution logs of tiup-cluster.
