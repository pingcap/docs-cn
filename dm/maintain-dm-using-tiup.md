---
title: Maintain a DM Cluster Using TiUP
summary: Learn how to maintain a DM cluster using TiUP.
aliases: ['/docs/tidb-data-migration/dev/cluster-operations/']
---

# Maintain a DM Cluster Using TiUP

This document introduces how to maintain a DM cluster using the TiUP DM component.

If you have not deployed a DM cluster yet, you can refer to [Deploy a DM Cluster Using TiUP](/dm/deploy-a-dm-cluster-using-tiup.md) for instructions.

> **Note:**
>
> - Make sure that the ports among the following components are interconnected
>     - The `peer_port` (`8291` by default) among the DM-master nodes are interconnected.
>     - Each DM-master node can connect to the `port` of all DM-worker nodes (`8262` by default).
>     - Each DM-worker node can connect to the `port` of all DM-master nodes (`8261` by default).
>     - The TiUP nodes can connect to the `port` of all DM-master nodes (`8261` by default).
>     - The TiUP nodes can connect to the `port` of all DM-worker nodes (`8262` by default).

For the help information of the TiUP DM component, run the following command:

```bash
tiup dm --help
```

```
Deploy a DM cluster for production

Usage:
  tiup dm [flags]
  tiup dm [command]

Available Commands:
  deploy      Deploy a DM cluster for production
  start       Start a DM cluster
  stop        Stop a DM cluster
  restart     Restart a DM cluster
  list        List all clusters
  destroy     Destroy a specified DM cluster
  audit       Show audit log of cluster operation
  exec        Run shell command on host in the dm cluster
  edit-config Edit DM cluster config
  display     Display information of a DM cluster
  reload      Reload a DM cluster's config and restart if needed
  upgrade     Upgrade a specified DM cluster
  patch       Replace the remote package with a specified package and restart the service
  scale-out   Scale out a DM cluster
  scale-in    Scale in a DM cluster
  import      Import an exist DM 1.0 cluster from dm-ansible and re-deploy 2.0 version
  help        Help about any command

Flags:
  -h, --help               help for tiup-dm
      --native-ssh         Use the native SSH client installed on local system instead of the build-in one.
      --ssh-timeout int    Timeout in seconds to connect host via SSH, ignored for operations that don't need an SSH connection. (default 5)
  -v, --version            version for tiup-dm
      --wait-timeout int   Timeout in seconds to wait for an operation to complete, ignored for operations that don't fit. (default 60)
  -y, --yes                Skip all confirmations and assumes 'yes'
```

## View the cluster list

After the cluster is successfully deployed, view the cluster list by running the following command:

{{< copyable "shell-root" >}}

```bash
tiup dm list
```

```
Name  User  Version  Path                                  PrivateKey
----  ----  -------  ----                                  ----------
prod-cluster  tidb  ${version}  /root/.tiup/storage/dm/clusters/test  /root/.tiup/storage/dm/clusters/test/ssh/id_rsa
```

## Start the cluster

After the cluster is successfully deployed, start the cluster by running the following command:

{{< copyable "shell-regular" >}}

```shell
tiup dm start prod-cluster
```

If you forget the name of your cluster, view the cluster list by running `tiup dm list`.

## Check the cluster status

TiUP provides the `tiup dm display` command to view the status of each component in the cluster. With this command, you do not have to log in to each machine to see the component status. The usage of the command is as follows:

{{< copyable "shell-root" >}}

```bash
tiup dm display prod-cluster
```

```
dm Cluster: prod-cluster
dm Version: ${version}
ID                 Role          Host          Ports      OS/Arch       Status     Data Dir                           Deploy Dir
--                 ----          ----          -----      -------       ------     --------                           ----------
172.19.0.101:9093  alertmanager  172.19.0.101  9093/9094  linux/x86_64  Up         /home/tidb/data/alertmanager-9093  /home/tidb/deploy/alertmanager-9093
172.19.0.101:8261  dm-master     172.19.0.101  8261/8291  linux/x86_64  Healthy|L  /home/tidb/data/dm-master-8261     /home/tidb/deploy/dm-master-8261
172.19.0.102:8261  dm-master     172.19.0.102  8261/8291  linux/x86_64  Healthy    /home/tidb/data/dm-master-8261     /home/tidb/deploy/dm-master-8261
172.19.0.103:8261  dm-master     172.19.0.103  8261/8291  linux/x86_64  Healthy    /home/tidb/data/dm-master-8261     /home/tidb/deploy/dm-master-8261
172.19.0.101:8262  dm-worker     172.19.0.101  8262       linux/x86_64  Free       /home/tidb/data/dm-worker-8262     /home/tidb/deploy/dm-worker-8262
172.19.0.102:8262  dm-worker     172.19.0.102  8262       linux/x86_64  Free       /home/tidb/data/dm-worker-8262     /home/tidb/deploy/dm-worker-8262
172.19.0.103:8262  dm-worker     172.19.0.103  8262       linux/x86_64  Free       /home/tidb/data/dm-worker-8262     /home/tidb/deploy/dm-worker-8262
172.19.0.101:3000  grafana       172.19.0.101  3000       linux/x86_64  Up         -                                  /home/tidb/deploy/grafana-3000
172.19.0.101:9090  prometheus    172.19.0.101  9090       linux/x86_64  Up         /home/tidb/data/prometheus-9090    /home/tidb/deploy/prometheus-9090
```

The `Status` column uses `Up` or `Down` to indicate whether the service is running normally.

For the DM-master component, `|L` might be appended to a status, which indicates that the DM-master node is a Leader. For the DM-worker component, `Free` indicates that the current DM-worker node is not bound to an upstream.

## Scale in a cluster

Scaling in a cluster means making some node(s) offline. This operation removes the specified node(s) from the cluster and deletes the remaining data files.

When you scale in a cluster, DM operations on DM-master and DM-worker components are performed in the following order:

1. Stop component processes.
2. Call the API for DM-master to delete the `member`.
3. Clean up the data files related to the node.

The basic usage of the scale-in command:

```bash
tiup dm scale-in <cluster-name> -N <node-id>
```

To use this command, you need to specify at least two arguments: the cluster name and the node ID. The node ID can be obtained by using the `tiup dm display` command in the previous section.

For example, to scale in the DM-worker node on `172.16.5.140` (similar to scaling in DM-master), run the following command:

{{< copyable "shell-regular" >}}

```bash
tiup dm scale-in prod-cluster -N 172.16.5.140:8262
```

## Scale out a cluster

The scale-out operation has an inner logic similar to that of deployment: the TiUP DM component first ensures the SSH connection of the node, creates the required directories on the target node, then executes the deployment operation, and starts the node service.

For example, to scale out a DM-worker node in the `prod-cluster` cluster, take the following steps (scaling out DM-master has similar steps):

1. Create a `scale.yaml` file and add information of the new worker node:

    > **Note:**
    >
    > You need to create a topology file, which includes only the description of the new nodes, not the existing nodes.
    > For more configuration items (such as the deployment directory), refer to this [TiUP configuration parameter example](https://github.com/pingcap/tiup/blob/master/embed/examples/dm/topology.example.yaml).

    ```yaml
    ---

    worker_servers:
      - host: 172.16.5.140

    ```

2. Perform the scale-out operation. TiUP DM adds the corresponding nodes to the cluster according to the port, directory, and other information described in `scale.yaml`.

    {{< copyable "shell-regular" >}}

    ```shell
    tiup dm scale-out prod-cluster scale.yaml
    ```

    After the command is executed, you can check the status of the scaled-out cluster by running `tiup dm display prod-cluster`.

## Rolling upgrade

> **Note:**
>
> Since v2.0.5, dmctl support [Export and Import Data Sources and Task Configuration of Clusters](/dm/dm-export-import-config.md).
>
> Before upgrading, you can use `config export` to export the configuration files of clusters. After upgrading, if you need to downgrade to an earlier version, you can first redeploy the earlier cluster and then use `config import` to import the previous configuration files.
>
> For clusters earlier than v2.0.5, you can use dmctl v2.0.5 or later to export and import the data source and task configuration files.
>
> For clusters later than v2.0.2, currently, it is not supported to automatically import the configuration related to relay worker. You can use `start-relay` command to manually [start relay log](/dm/relay-log.md#start-and-stop-the-relay-log-feature).

The rolling upgrade process is made as transparent as possible to the application, and does not affect the business. The operations vary with different nodes.

### Upgrade command

You can run the `tiup dm upgrade` command to upgrade a DM cluster. For example, the following command upgrades the cluster to `${version}`. Modify `${version}` to your needed version before running this command:

{{< copyable "shell-regular" >}}

```bash
tiup dm upgrade prod-cluster ${version}
```

## Update configuration

If you want to dynamically update the component configurations, the TiUP DM component saves a current configuration for each cluster. To edit this configuration, execute the `tiup dm edit-config <cluster-name>` command. For example:

{{< copyable "shell-regular" >}}

```bash
tiup dm edit-config prod-cluster
```

TiUP DM opens the configuration file in the vi editor. If you want to use other editors, use the `EDITOR` environment variable to customize the editor, such as `export EDITOR=nano`. After editing the file, save the changes. To apply the new configuration to the cluster, execute the following command:

{{< copyable "shell-regular" >}}

```bash
tiup dm reload prod-cluster
```

The command sends the configuration to the target machine and restarts the cluster to make the configuration take effect.

## Update component

For normal upgrade, you can use the `upgrade` command. But in some scenarios, such as debugging, you might need to replace the currently running component with a temporary package. To achieve this, use the `patch` command:

{{< copyable "shell-root" >}}

```bash
tiup dm patch --help
```

```
Replace the remote package with a specified package and restart the service

Usage:
  tiup dm patch <cluster-name> <package-path> [flags]

Flags:
  -h, --help                   help for patch
  -N, --node strings           Specify the nodes
      --overwrite              Use this package in the future scale-out operations
  -R, --role strings           Specify the role
      --transfer-timeout int   Timeout in seconds when transferring dm-master leaders (default 300)

Global Flags:
      --native-ssh         Use the native SSH client installed on local system instead of the build-in one.
      --ssh-timeout int    Timeout in seconds to connect host via SSH, ignored for operations that don't need an SSH connection. (default 5)
      --wait-timeout int   Timeout in seconds to wait for an operation to complete, ignored for operations that don't fit. (default 60)
  -y, --yes                Skip all confirmations and assumes 'yes'
```

If a DM-master hotfix package is in `/tmp/dm-master-hotfix.tar.gz` and you want to replace all the DM-master packages in the cluster, run the following command:

{{< copyable "shell-regular" >}}

```bash
tiup dm patch prod-cluster /tmp/dm-master-hotfix.tar.gz -R dm-master
```

You can also replace only one DM-master package in the cluster:

{{< copyable "shell-regular" >}}

```bash
tiup dm patch prod-cluster /tmp/dm--hotfix.tar.gz -N 172.16.4.5:8261
```

## Import and upgrade a DM 1.0 cluster deployed using DM-Ansible

> **Note:**
>
> - TiUP does not support importing the DM Portal component in a DM 1.0 cluster.
> - You need to stop the original cluster before importing.
> - Don't run `stop-task` for tasks that need to be upgraded to 2.0.
> - TiUP only supports importing to a DM cluster of v2.0.0-rc.2 or a later version.
> - The `import` command is used to import data from a DM 1.0 cluster to a new DM 2.0 cluster. If you need to import DM migration tasks to an existing DM 2.0 cluster, refer to [Manually Upgrade TiDB Data Migration from v1.0.x to v2.0+](/dm/manually-upgrade-dm-1.0-to-2.0.md).
> - The deployment directories of some components are different from those of the original cluster. You can execute the `display` command to view the details.
> - Run `tiup update --self && tiup update dm` before importing to make sure that the TiUP DM component is the latest version.
> - Only one DM-master node exists in the cluster after importing. Refer to [Scale out a cluster](#scale-out-a-cluster) to scale out the DM-master.

Before TiUP is released, DM-Ansible is often used to deploy DM clusters. To enable TiUP to take over the DM 1.0 cluster deployed by DM-Ansible, use the `import` command.

For example, to import a cluster deployed using DM Ansible:

{{< copyable "shell-regular" >}}

```bash
tiup dm import --dir=/path/to/dm-ansible --cluster-version ${version}
```

Execute `tiup list dm-master` to view the latest cluster version supported by TiUP.

The process of using the `import` command is as follows:

1. TiUP generates a topology file [`topology.yml`](https://github.com/pingcap/tiup/blob/master/embed/examples/dm/topology.example.yaml) based on the DM cluster previously deployed using DM-Ansible.
2. After confirming that the topology file has been generated, you can use it to deploy the DM cluster of v2.0 or later versions.

After the deployment is completed, you can execute the `tiup dm start` command to start the cluster and begin the process of upgrading the DM kernel.

## View the operation log

To view the operation log, use the `audit` command. The usage of the `audit` command is as follows:

```bash
Usage:
  tiup dm audit [audit-id] [flags]

Flags:
  -h, --help   help for audit
```

If the `[audit-id]` argument is not specified, the command shows a list of commands that have been executed. For example:

{{< copyable "shell-regular" >}}

```bash
tiup dm audit
```

```
ID      Time                  Command
--      ----                  -------
4D5kQY  2020-08-13T05:38:19Z  tiup dm display test
4D5kNv  2020-08-13T05:36:13Z  tiup dm list
4D5kNr  2020-08-13T05:36:10Z  tiup dm deploy -p prod-cluster ${version} ./examples/dm/minimal.yaml
```

The first column is `audit-id`. To view the execution log of a certain command, pass the `audit-id` argument as follows:

{{< copyable "shell-regular" >}}

```bash
tiup dm audit 4D5kQY
```

## Run commands on a host in the DM cluster

To run commands on a host in the DM cluster, use the `exec` command. The usage of the `exec` command is as follows:

```bash
Usage:
  tiup dm exec <cluster-name> [flags]

Flags:
      --command string   the command run on cluster host (default "ls")
  -h, --help             help for exec
  -N, --node strings     Only exec on host with specified nodes
  -R, --role strings     Only exec on host with specified roles
      --sudo             use root permissions (default false)
```

For example, to execute `ls /tmp` on all DM nodes, run the following command:

{{< copyable "shell-regular" >}}

```bash
tiup dm exec prod-cluster --command='ls /tmp'
```

## dmctl

TiUP integrates the DM cluster controller `dmctl`.

Run the following command to use dmctl:

```bash
tiup dmctl [args]
```

Specify the version of dmctl. Modify `${version}` to your needed version before running this command:

```
tiup dmctl:${version} [args]
```

The previous dmctl command to add a source is `dmctl --master-addr master1:8261 operate-source create /tmp/source1.yml`. After dmctl is integrated into TiUP, the command is:

{{< copyable "shell-regular" >}}

```bash
tiup dmctl --master-addr master1:8261 operate-source create /tmp/source1.yml
```

## Use the system's native SSH client to connect to cluster

All operations above performed on the cluster machine use the SSH client embedded in TiUP to connect to the cluster and execute commands. However, in some scenarios, you might also need to use the SSH client native to the control machine system to perform such cluster operations. For example:

- To use a SSH plug-in for authentication
- To use a customized SSH client

Then you can use the `--native-ssh` command-line flag to enable the system-native command-line tool:

- Deploy a cluster: `tiup dm deploy <cluster-name> <version> <topo> --native-ssh`. Fill in the name of your cluster for `<cluster-name>`,  the DM version to be deployed (such as `v6.5.0`) for `<version>` , and the topology file name for `<topo>`.
- Start a cluster: `tiup dm start <cluster-name> --native-ssh`.
- Upgrade a cluster: `tiup dm upgrade ... --native-ssh`

You can add `--native-ssh` in all cluster operation commands above to use the system's native SSH client.

To avoid adding such a flag in every command, you can use the `TIUP_NATIVE_SSH` system variable to specify whether to use the local SSH client:

```sh
export TIUP_NATIVE_SSH=true
# or
export TIUP_NATIVE_SSH=1
# or
export TIUP_NATIVE_SSH=enable
```

If you specify this environment variable and `--native-ssh` at the same time, `--native-ssh` has higher priority.

> **Note:**
>
> During the process of cluster deployment, if you need to use a password for connection or `passphrase` is configured in the key file, you must ensure that `sshpass` is installed on the control machine; otherwise, a timeout error is reported.
