---
title: tiup dm patch
---

# tiup dm patch

If you need to dynamically replace the binaries of a service while the cluster is running (that is, to keep the cluster available during the replacement), you can use the `tiup dm patch` command. The command does the following:

- Uploads the binary package for replacement to the target machine.
- Takes the related nodes offline using the API.
- Stops the target service.
- Unpacks the binary package and replaces the service.
- Starts the target service.

## Syntax

```shell
tiup dm patch <cluster-name> <package-path> [flags]
```

- `<cluster-name>`: The name of the cluster to be operated.
- `<package-path>`: The path to the binary package used for replacement.

### Preparation

You need to pack the binary package required for this command in advance according to the following steps:

- Determine the name `${component}` of the component to be replaced (dm-master, dm-worker ...), the `${version}` of the component (v2.0.0, v2.0.1 ...), and the operating system `${os}` and platform `${arch}` on which the component runs.
- Download the current component package using the command `wget https://tiup-mirrors.pingcap.com/${component}-${version}-${os}-${arch}.tar.gz -O /tmp/${component}-${version}-${os}-${arch}.tar.gz`.
- Run `mkdir -p /tmp/package && cd /tmp/package` to create a temporary directory to pack files.
- Run `tar xf /tmp/${component}-${version}-${os}-${arch}.tar.gz` to unpack the original binary package.
- Run `find .` to view the file structure in the temporary package directory.
- Copy the binary files or configuration files to the corresponding locations in the temporary directory.
- Run `tar czf /tmp/${component}-hotfix-${os}-${arch}.tar.gz *` to pack the files in the temporary directory.
- Finally, you can use `/tmp/${component}-hotfix-${os}-${arch}.tar.gz` as the value of `<package-path>` in the `tiup dm patch` command.

## Options

### --overwrite

- After you patch a certain component (such as dm-worker), when the tiup-dm scales out the component, tiup-dm uses the original component version by default. To use the version that you patch when the cluster scales out in the future, you need to specify the option `--overwrite` in the command.
- Data type: `BOOLEAN`
- This option is disabled by default with the `false` value. To enable this option, add this option to the command, and either pass the `true` value or do not pass any value.

### -N, --node

- Specifies the nodes to be replaced. The value of this option is a comma-separated list of node IDs. You can get the node IDs from the first column of the cluster status table returned by the `[tiup dm display](/tiup/tiup-component-dm-display.md)` command.
- Data type: `STRING`
- If this option is not specified, TiUP selects all nodes to replace by default.

> **Note:**
>
> If the option `-R, --role` is specified at the same time, TiUP then replaces service nodes that match both the requirements of `-N, --node` and `-R, --role`.

### -R, --role

- Specifies the roles to be replaced. The value of this option is a comma-separated list of the roles of the nodes. You can get the roles of the nodes from the second column of the cluster status table returned by the `[tiup dm display](/tiup/tiup-component-dm-display.md)` command.
- Data type: `STRING`
- If this option is not specified, TiUP selects all roles to replace by default.

> **Note:**
>
> If the option `-N, --node` is specified at the same time, TiUP then replaces service nodes that match both the requirements of `-N, --node` and `-R, --role`.

### --offline

- Declares that the current cluster is offline. When this option is specified, TiUP DM only replaces the binary files of the cluster components in place without restarting the service.

### -h, --help

- Prints help information.
- Data type: `BOOLEAN`
- This option is disabled by default with the `false` value. To enable this option, add this option to the command, and either pass the `true` value or do not pass any value.

## Outputs

The execution log of tiup-dm.

[<< Back to the previous page - TiUP DM command list](/tiup/tiup-component-dm.md#command-list)
