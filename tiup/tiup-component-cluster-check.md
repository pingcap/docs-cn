---
title: tiup cluster check
---

# tiup cluster check

For a formal production environment, before the environment goes live, you need to perform a series of checks to ensure the clusters are in their best performance. To simplify the manual check steps, TiUP Cluster provides the `check` command to check whether the hardware and software environments of the target machines of a specified cluster meet the requirements to work normally.

## List of check items

### Operating system version

Check the operating system distribution and version of the deployed machines. Currently, only CentOS 7 is supported for deployment. More system versions may be supported in later releases for compatibility improvement.

### CPU EPOLLEXCLUSIVE

Check whether the CPU of the target machine supports EPOLLEXCLUSIVE.

### numactl

Check whether numactl is installed on the target machine. If tied cores are configured on the target machine, you must install numactl.

### System time

Check whether the system time of the target machine is synchronized. Compare the system time of the target machine with that of the central control machine, and report an error if the deviation exceeds a certain threshold (500 ms).

### System time zone

Check whether the system time zone of the target machines is synchronized. Compare the time zone configuration of these machines and report an error if the time zone is inconsistent.

### Time synchronization service

Check whether the time synchronization service is configured on the target machine. Namely, check whether ntpd is running.

### Swap partitioning

Check whether swap partitioning is enabled on the target machine. It is recommended to disable swap partitioning.

### Kernel parameters

Check the values of the following kernel parameters:

- `net.ipv4.tcp_tw_recycle`: 0
- `net.ipv4.tcp_syncookies`: 0
- `net.core.somaxconn`: 32768
- `vm.swappiness`: 0
- `vm.overcommit_memory`: 0 or 1
- `fs.file-max`: 1000000

### Transparent Huge Pages (THP)

Check whether THP is enabled on the target machine. It is recommended to disable THP.

### System limits

Check the limit values in the `/etc/security/limits.conf` file:

```
<deploy-user> soft nofile 1000000
<deploy-user> hard nofile 1000000
<deploy-user> soft stack 10240
```

`<deploy-user>` is the user who deploys and runs the TiDB cluster, and the last column is the minimum value required for the system.

### SELinux

Check whether SELinux is enabled. It is recommended to disable SELinux.

### Firewall

Check whether the FirewallD service is enabled. It is recommended to either disable the FirewallD service or add permission rules for each service in the TiDB cluster.

### irqbalance

Check whether the irqbalance service is enabled. It is recommended to enable the irqbalance service.

### Disk mount options

Check the mount options for ext4 partitions. Make sure the mount options include the nodelalloc option and the noatime option.

### Port usage

Check if the ports defined in the topology (including the auto-completion default ports) are already used by the processes on the target machine.

> **Note:**
>
> The port usage check assumes that a cluster is not started yet. If a cluster is already deployed and started, the port usage check on the cluster fails because the ports must be in use in this case.

### CPU core number

Check the CPU information of the target machine. For a production cluster, it is recommended that the number of the CPU logical core is greater than or equal to 16.

> **Note:**
>
> CPU core number is not checked by default. To enable the check, you need to add the `-enable-cpu` option to the command.

### Memory size

Check the memory size of the target machine. For a production cluster, it is recommended that the total memory capacity is greater than or equal to 32GB.

> **Note:**
>
> Memory size is not checked by default. To enable the check, you need to add the `-enable-mem` option to the command.

### Fio disk performance test

Use flexible I/O tester (fio) to test the performance of the disk where `data_dir` is located, including the following three test items:

- fio_randread_write_latency
- fio_randread_write
- fio_randread

> **Note:**
>
> The fio disk performance test is not performed by default. To perform the test, you need to add the `-enable-disk` option to the command.

## Syntax

```shell
tiup cluster check <topology.yml | cluster-name> [flags]
```

- If a cluster is not deployed yet, you need to pass the [topology.yml](/tiup/tiup-cluster-topology-reference.md) file that is used to deploy the cluster. According to the content in this file, tiup-cluster connects to the corresponding machine to perform the check.
- If a cluster is already deployed, you can use the `<cluster-name>` as the check object.
- If you want to check the scale-out YAML file for an existing cluster, you can use both `<scale-out.yml>` and `<cluster-name>` as the check objects.

> **Note:**
>
> If `<cluster-name>` is used for the check, you need to add the `--cluster` option in the command.

## Options

### --apply

- Attempts to automatically repair the failed check items. Currently, tiup-cluster only attempts to repair the following check items:
    - SELinux
    - firewall
    - irqbalance
    - kernel parameters
    - System limits
    - THP (Transparent Huge Pages)
- Data type: `BOOLEAN`
- This option is disabled by default with the `false` value. To enable this option, add this option to the command, and either pass the `true` value or do not pass any value.

> **Note:**
>
> `tiup cluster check` also supports repairing the `scale-out.yaml` file for an existing cluster with the following command format:
>
>```shell
> tiup cluster check <cluster-name> scale-out.yaml --cluster --apply --user root [-p] [-i /home/root/.ssh/gcp_rsa]
>```

### --cluster

- Indicates that the check is for a cluster that has been deployed.
- Data type: `BOOLEAN`
- This option is disabled by default with the `false` value. To enable this option, add this option to the command, and either pass the `true` value or do not pass any value.
- Command format:

    ```shell
    tiup cluster check <topology.yml | cluster-name> --cluster [flags]
    ```

> **Note:**
>
> - If the `tiup cluster check <cluster-name>` command is used, you must add the `--cluster` option: `tiup cluster check <cluster-name> --cluster`.
> - `tiup cluster check` also supports checking the `scale-out.yaml` file for an existing cluster with the following command format:
>
>   ```shell
>   tiup cluster check <cluster-name> scale-out.yaml --cluster --user root [-p] [-i /home/root/.ssh/gcp_rsa]
>   ```

### -N, --node

- Specifies the nodes to be checked. The value of this option is a comma-separated list of node IDs. You can get the node IDs from the first column of the cluster status table returned by the [`tiup cluster display`](/tiup/tiup-component-cluster-display.md) command.
- Data type: `STRINGS`
- If this option is not specified in the command, all nodes are checked by default.

> **Note:**
>
> If the `-R, --role` option is specified at the same time, only the service nodes that match both the specifications of `-N, --node` and `-R, --role` are checked.

### -R, --role

- Specifies the roles to be checked. The value of this option is a comma-separated list of node roles. You can get the roles of nodes from the second column of the cluster status table returned by the [`tiup cluster display`](/tiup/tiup-component-cluster-display.md) command.
- Data type: `STRINGS`
- If this option is not specified in the command, all roles are checked by default.

> **Note:**
>
> If the `-N, --node` option is specified at the same time, only the service nodes that match both the specifications of `-N, --node` and `-R, --role` are checked.

### --enable-cpu

- Enables the check of CPU core number.
- Data type: `BOOLEAN`
- This option is disabled by default with the `false` value. To enable this option, add this option to the command, and either pass the `true` value or do not pass any value.

### --enable-disk

- Enables the fio disk performance test.
- Data type: `BOOLEAN`
- This option is disabled by default with the `false` value. To enable this option, add this option to the command, and either pass the `true` value or do not pass any value.

### --enable-mem

- Enables the memory size check.
- Data type: `BOOLEAN`
- This option is disabled by default with the `false` value. To enable this option, add this option to the command, and either pass the `true` value or do not pass any value.

### --u, --user

- Specifies the user name to connect to the target machine. The specified user needs to have the password-free sudo root privileges on the target machine.
- Data type: `STRING`
- If this option is not specified in the command, the user who executes the command is used as the default value.

> **Note:**
>
> This option is valid only if the `-cluster` option is false. Otherwise, the value of this option is fixed to the username specified in the topology file for the cluster deployment.

### -i, --identity_file

- Specifies the key file to connect to the target machine.
- Data type: `STRING`
- The option is enabled by default with `~/.ssh/id_rsa` (the default value) passed in.

> **Note:**
>
> This option is valid only if the `--cluster` option is false. Otherwise, the value of this option is fixed to `${TIUP_HOME}/storage/cluster/clusters/<cluster-name>/ssh/id_rsa`.

### -p, --password

- Logs in with a password when connecting to the target machine.
    - If the `--cluster` option is added for a cluster, the password is the password of the user specified in the topology file when the cluster was deployed.
    - If the `--cluster` option is not added for a cluster, the password is the password of the user specified in the `-u/--user` option.
- Data type: `BOOLEAN`
- This option is disabled by default with the `false` value. To enable this option, add this option to the command, and either pass the `true` value or do not pass any value.

### -h, --help

- Prints the help information of the related commands.
- Data type: `BOOLEAN`
- This option is disabled by default with the `false` value. To enable this option, add this option to the command, and either pass the `true` value or do not pass any value.

## Output

A table containing the following fields:

- `Node`: the target node
- `Check`: the check item
- `Result`: the check result (Pass, Warn, or Fail)
- `Message`: the result description

[<< Back to the previous page - TiUP Cluster command list](/tiup/tiup-component-cluster.md#command-list)
