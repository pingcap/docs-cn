---
title: tiup cluster patch
---

# tiup cluster patch

If you need to dynamically replace the binaries of a service while the cluster is running (namely, keep the cluster available during the replacement process), you can use the `tiup cluster patch` command. After the command is executed, TiUP does the following things:

- Uploads the binary package for replacement to the target machine.
- If the target service is a storage service such as TiKV, TiFlash, or TiDB Binlog, TiUP first takes the related nodes offline via the API.
- Stops the target service.
- Unpacks the binary package and replace the service.
- Starts the target service.

## Syntax

```shell
tiup cluster patch <cluster-name> <package-path> [flags]
```

- `<cluster-name>`: The name of the cluster to be operated.
- `<package-path>`: The path to the binary package used for replacement.

### Preparation

You need to pack the binary package required for this command in advance according to the following steps:

- Determine the name `${component}` of the component to be replaced (tidb, tikv, pd...), the `${version}` of the component (v4.0.0, v4.0.1 ...), and the operating system `${os}` (`linux`) and platform `${arch}` on which the component runs.
- Download the current component package using the command `wget https://tiup-mirrors.pingcap.com/${component}-${version}-${os}-${arch}.tar.gz -O /tmp/${component}-${version}-${os}-${arch}.tar.gz`.
- Run `mkdir -p /tmp/package && cd /tmp/package` to create a temporary directory to pack files.
- Run `tar xf /tmp/${component}-${version}-${os}-${arch}.tar.gz` to unpack the original binary package.
- Run `find .` to view the file structure in the temporary package directory.
- Copy the binary files or configuration files to the corresponding locations in the temporary directory.
- Run `tar czf /tmp/${component}-hotfix-${os}-${arch}.tar.gz *` to pack the files in the temporary directory.
- Finally, you can use `/tmp/${component}-hotfix-${os}-${arch}.tar.gz` as the `<package-path>` in the `tiup cluster patch` command.

## Options

### --overwrite

- After you patch a certain component (such as TiDB or TiKV), when the tiup cluster scales out the component, TiUP uses the original component version by default. To use the version that you patch when the cluster scales out in the future, you need to specified the option `--overwrite` in the command.
- Data type: `BOOLEAN`
- This option is disabled by default with the `false` value. To enable this option, add this option to the command, and either pass the `true` value or do not pass any value.

### --transfer-timeout

- When restarting the PD or TiKV service, TiKV/PD first transfers the leader of the node to be restarted to another node. Because the transfer process takes some time, you can use the option `--transfer-timeout` to set the maximum waiting time (in seconds). After the timeout, TiUP directly restarts the service.
- Data type: `UINT`
- If this option is not specified, TiUP directly restarts the service after waiting for `300` seconds.

> **Note:**
>
> If TiUP directly restarts the service after the timeout, the service performance might jitter.

### -N, --node

- Specifies nodes to be replaced. The value of this option is a comma-separated list of node IDs. You can get the node ID from the first column of the [cluster status table](/tiup/tiup-component-cluster-display.md) returned by the `tiup cluster display` command.
- Data type: `STRINGS`
- If this option is not specified, TiUP does not select any nodes to replace by default.

> **Note:**
>
> If the option `-R, --role` is specified at the same time, TiUP then replaces service nodes that match both the requirements of `-N, --node` and `-R, --role`.

### -R, --role

- Specifies the roles to be replaced. The value of this option is a comma-separated list of the roles of the nodes. You can get the role deployed on a node from the second column of the [cluster status table](/tiup/tiup-component-cluster-display.md) returned by the `tiup cluster display` command.
- Data type: `STRINGS`
- If this option is not specified, TiUP does not select any roles to replace by default.

> **Note:**
>
> If the option `-N, --node` is specified at the same time, TiUP then replaces service nodes that match both the requirements of `-N, --node` and `-R, --role`.

### --offline

- Declares that the current cluster is not running. When the option is specified, TiUP does not evict the service leader to another node or restart the service, but only replaces the binary files of cluster components.
- Data type: `BOOLEAN`
- This option is disabled by default with the `false` value. To enable this option, add this option to the command, and either pass the `true` value or do not pass any value.

### -h, --help

- Prints help information.
- Data type: `BOOLEAN`
- This option is disabled by default with the `false` value. To enable this option, add this option to the command, and either pass the `true` value or do not pass any value.

## Outputs

The execution log of the tiup-cluster.

[<< Back to the previous page - TiUP Cluster command list](/tiup/tiup-component-cluster.md#command-list)
