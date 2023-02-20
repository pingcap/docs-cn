---
title: Apply Hotfix to DM Clusters Online
summary: Learn how to apply hotfix patches to DM clusters.
---

# Apply Hotfix to DM Clusters Online

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

- `<cluster-name>`: The name of the cluster to be operated
- `<package-path>`: The path to the binary package used for replacement

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

## Example

The following example shows how to apply `v5.3.0-hotfix` to the `v5.3.0` cluster deployed using TiUP. The operations might vary if you deploy the cluster using other methods.

> **Note:**
>
> Hotfix is used only for emergency fixes. Its daily maintenance is complicated. It is recommend that you upgrade the DM cluster to an official version as soon as it is released.

### Preparations

Before applying a hotfix, prepare the hotfix package `dm-linux-amd64.tar.gz` and confirm the current DM software version:

```shell
/home/tidb/dm/deploy/dm-master-8261/bin/dm-master/dm-master -V
```

Output:

```
Release Version: v5.3.0

Git Commit Hash: 20626babf21fc381d4364646c40dd84598533d66
Git Branch: heads/refs/tags/v5.3.0
UTC Build Time: 2021-11-29 08:29:49
Go Version: go version go1.16.4 linux/amd64
```

### Prepare the patch package and apply it to the DM cluster

1. Prepare the DM software package that matches the current version:

    ```shell
    mkdir -p /tmp/package
    tar -zxvf /root/.tiup/storage/dm/packages/dm-master-v5.3.0-linux-amd64.tar.gz -C /tmp/package/
    tar -zxvf /root/.tiup/storage/dm/packages/dm-worker-v5.3.0-linux-amd64.tar.gz -C /tmp/package/
    ```

2. Replace the binary file with the hotfix package:

    ```shell
    # Decompress the hotfix package and use it to replace the binary file.
    cd /root; tar -zxvf dm-linux-amd64.tar.gz
    cp /root/dm-linux-amd64/bin/dm-master /tmp/package/dm-master/dm-master
    cp /root/dm-linux-amd64/bin/dm-worker /tmp/package/dm-worker/dm-worker
    # Re-package the modified files.
    # Note that the packaging method might be different for other deployment methods.
    cd /tmp/package/ && tar -czvf dm-master-hotfix-linux-amd64.tar.gz dm-master/
    cd /tmp/package/ && tar -czvf dm-worker-hotfix-linux-amd64.tar.gz dm-worker/
    ```

3. Apply the hotfix:

    Query the cluster status. The following uses the cluster named `dm-test` as an example:

    ```shell
    tiup dm display dm-test
    ```

    Output:

    ```
    Cluster type:       dm
    Cluster name:       dm-test
    Cluster version:    v5.3.0
    Deploy user:        tidb
    SSH type:           builtin
    ID                  Role                 Host           Ports      OS/Arch       Status     Data Dir                              Deploy Dir
    --                  ----                 ----           -----      -------       ------     --------                              ----------
    172.16.100.21:9093  alertmanager         172.16.100.21  9093/9094  linux/x86_64  Up         /home/tidb/dm/data/alertmanager-9093  /home/tidb/dm/deploy/alertmanager-9093
    172.16.100.21:8261  dm-master            172.16.100.21  8261/8291  linux/x86_64  Healthy|L  /home/tidb/dm/data/dm-master-8261     /home/tidb/dm/deploy/dm-master-8261
    172.16.100.21:8262  dm-worker            172.16.100.21  8262       linux/x86_64  Free       /home/tidb/dm/data/dm-worker-8262     /home/tidb/dm/deploy/dm-worker-8262
    172.16.100.21:3000  grafana              172.16.100.21  3000       linux/x86_64  Up         -                                     /home/tidb/dm/deploy/grafana-3000
    172.16.100.21:9090  prometheus           172.16.100.21  9090       linux/x86_64  Up         /home/tidb/dm/data/prometheus-9090    /home/tidb/dm/deploy/prometheus-9090
    Total nodes: 5
    ```

    Apply the hotfix to the specified node or specified role. If both `-R` and `-N` are specified, the intersection will be taken.

    ```
    # Apply hotfix to a specified node.
    tiup dm patch dm-test dm-master-hotfix-linux-amd64.tar.gz -N 172.16.100.21:8261
    tiup dm patch dm-test dm-worker-hotfix-linux-amd64.tar.gz -N 172.16.100.21:8262
    # Apply hotfix to a specified role.
    tiup dm patch dm-test dm-master-hotfix-linux-amd64.tar.gz -R dm-master
    tiup dm patch dm-test dm-worker-hotfix-linux-amd64.tar.gz -R dm-worker
    ```

4. Query the hotfix application result:

    ```shell
    /home/tidb/dm/deploy/dm-master-8261/bin/dm-master/dm-master -V
    ```

    Output:

    ```
    Release Version: v5.3.0-20211230
    Git Commit Hash: ca7070c45013c24d34bd9c1e936071253451d707
    Git Branch: heads/refs/tags/v5.3.0-20211230
    UTC Build Time: 2022-01-05 14:19:02
    Go Version: go version go1.16.4 linux/amd64
    ```

    The cluster information changes accordingly:

    ```shell
    tiup dm display dm-test
    ```

    Output:

    ```
    Starting component `dm`: /root/.tiup/components/dm/v1.8.1/tiup-dm display dm-test
    Cluster type:       dm
    Cluster name:       dm-test
    Cluster version:    v5.3.0
    Deploy user:        tidb
    SSH type:           builtin
    ID                  Role                 Host           Ports      OS/Arch       Status     Data Dir                              Deploy Dir
    --                  ----                 ----           -----      -------       ------     --------                              ----------
    172.16.100.21:9093  alertmanager         172.16.100.21  9093/9094  linux/x86_64  Up         /home/tidb/dm/data/alertmanager-9093  /home/tidb/dm/deploy/alertmanager-9093
    172.16.100.21:8261  dm-master (patched)  172.16.100.21  8261/8291  linux/x86_64  Healthy|L  /home/tidb/dm/data/dm-master-8261     /home/tidb/dm/deploy/dm-master-8261
    172.16.100.21:8262  dm-worker (patched)  172.16.100.21  8262       linux/x86_64  Free       /home/tidb/dm/data/dm-worker-8262     /home/tidb/dm/deploy/dm-worker-8262
    172.16.100.21:3000  grafana              172.16.100.21  3000       linux/x86_64  Up         -                                     /home/tidb/dm/deploy/grafana-3000
    172.16.100.21:9090  prometheus           172.16.100.21  9090       linux/x86_64  Up         /home/tidb/dm/data/prometheus-9090    /home/tidb/dm/deploy/prometheus-9090
    Total nodes: 5
    ```

[<< Back to the previous page - TiUP DM command list](/tiup/tiup-component-dm.md#command-list)
