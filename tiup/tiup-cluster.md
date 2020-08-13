---
title: Deploy and Maintain an Online TiDB Cluster Using TiUP
summary: Learns how to deploy and maintain an online TiDB cluster using TiUP.
aliases: ['/docs/dev/tiup/tiup-cluster/','/docs/dev/reference/tools/tiup/cluster/']
---

# Deploy and Maintain an Online TiDB Cluster Using TiUP

This document focuses on how to use the TiUP cluster component. For the complete steps of online deployment, refer to [Deploy a TiDB Cluster Using TiUP](/production-deployment-using-tiup.md).

Similar to [the TiUP playground component](/tiup/tiup-playground.md) used for local deployment, the TiUP cluster component quickly deploys TiDB for production environment. Compared with playground, the cluster component provides more powerful cluster management features, including upgrading, scaling, and even operation and auditing.

For the help information of the cluster component, run the following command:

```bash
tiup cluster
```

```
The component `cluster` is not installed; downloading from repository.
download https://tiup-mirrors.pingcap.com/cluster-v0.4.9-darwin-amd64.tar.gz 15.32 MiB / 15.34 MiB 99.90% 10.04 MiB p/s                                                   
Starting component `cluster`: /Users/joshua/.tiup/components/cluster/v0.4.9/cluster 
Deploy a TiDB cluster for production

Usage:
  cluster [flags]
  cluster [command]

Available Commands:
  check       Perform preflight checks for the cluster
  deploy      Deploy a cluster for production
  start       Start a TiDB cluster
  stop        Stop a TiDB cluster
  restart     Restart a TiDB cluster
  scale-in    Scale in a TiDB cluster
  scale-out   Scale out a TiDB cluster
  destroy     Destroy a specified cluster
  upgrade     Upgrade a specified TiDB cluster
  exec        Run shell command on host in the tidb cluster
  display     Display information of a TiDB cluster
  list        List all clusters
  audit       Show audit log of cluster operation
  import      Import an exist TiDB cluster from TiDB-Ansible
  edit-config Edit TiDB cluster config
  reload      Reload a TiDB cluster's config and restart if needed
  patch       Replace the remote package with a specified package and restart the service
  help        Help about any command

Flags:
  -h, --help              help for cluster
      --ssh-timeout int   Timeout in seconds to connect host via SSH, ignored for operations that don't need an SSH connection. (default 5)
  -y, --yes               Skip all confirmations and assumes 'yes'
```

## Deploy the cluster

To deploy the cluster, run the `tiup cluster deploy` command. The usage of the command is as follows:

```bash
tiup cluster deploy <cluster-name> <version> <topology.yaml> [flags]
```

This command requires you to provide the cluster name, the TiDB cluster version, and a topology file of the cluster.

To write a topology file, refer to [the example](https://github.com/pingcap/tiup/blob/master/examples/topology.example.yaml). The following file is an example of the simplest topology:

> **Note:**
>
> The topology file used by the TiUP cluster component for deployment and scaling is written using [yaml](https://yaml.org/spec/1.2/spec.html) syntax, so make sure that the indentation is correct.

```yaml
---

pd_servers:
  - host: 172.16.5.134
    name: pd-134
  - host: 172.16.5.139
    name: pd-139
  - host: 172.16.5.140
    name: pd-140

tidb_servers:
  - host: 172.16.5.134
  - host: 172.16.5.139
  - host: 172.16.5.140

tikv_servers:
  - host: 172.16.5.134
  - host: 172.16.5.139
  - host: 172.16.5.140

grafana_servers:
  - host: 172.16.5.134

monitoring_servers:
  - host: 172.16.5.134
```

Save the file as `/tmp/topology.yaml`. If you want to use TiDB v3.0.12 and your cluster name is `prod-cluster`, run the following command:

{{< copyable "shell-regular" >}}

```shell
tiup cluster deploy -p prod-cluster v3.0.12 /tmp/topology.yaml
```

During the execution, TiUP asks you to confirm your topology again and requires the root password of the target machine (the `-p` flag means inputting password):

```bash
Please confirm your topology:
TiDB Cluster: prod-cluster
TiDB Version: v3.0.12
Type        Host          Ports        Directories
----        ----          -----        -----------
pd          172.16.5.134  2379/2380    deploy/pd-2379,data/pd-2379
pd          172.16.5.139  2379/2380    deploy/pd-2379,data/pd-2379
pd          172.16.5.140  2379/2380    deploy/pd-2379,data/pd-2379
tikv        172.16.5.134  20160/20180  deploy/tikv-20160,data/tikv-20160
tikv        172.16.5.139  20160/20180  deploy/tikv-20160,data/tikv-20160
tikv        172.16.5.140  20160/20180  deploy/tikv-20160,data/tikv-20160
tidb        172.16.5.134  4000/10080   deploy/tidb-4000
tidb        172.16.5.139  4000/10080   deploy/tidb-4000
tidb        172.16.5.140  4000/10080   deploy/tidb-4000
prometheus  172.16.5.134  9090         deploy/prometheus-9090,data/prometheus-9090
grafana     172.16.5.134  3000         deploy/grafana-3000
Attention:
    1. If the topology is not what you expected, check your yaml file.
    1. Please confirm there is no port/directory conflicts in same host.
Do you want to continue? [y/N]:
```

After you enter the password, TiUP cluster downloads the required components and deploy them on the corresponding machines. When you see the following message, the deployment is successful:

```bash
Deployed cluster `prod-cluster` successfully
```

## View the cluster list

After the cluster is successfully deployed, view the cluster list by running the following command:

{{< copyable "shell-root" >}}

```bash
tiup cluster list
```

```
Starting /root/.tiup/components/cluster/v0.4.5/cluster list
Name          User  Version    Path                                               PrivateKey
----          ----  -------    ----                                               ----------
prod-cluster  tidb  v3.0.12    /root/.tiup/storage/cluster/clusters/prod-cluster  /root/.tiup/storage/cluster/clusters/prod-cluster/ssh/id_rsa
```

## Start the cluster

After the cluster is successfully deployed, start the cluster by running the following command:

{{< copyable "shell-regular" >}}

```shell
tiup cluster start prod-cluster
```

If you forget the name of your cluster, view the cluster list by running `tiup cluster list`.

## Check the cluster status

TiUP provides the `tiup cluster display` command to view the status of each component in the cluster. With this command, you don't have to log in to each machine to see the component status. The usage of the command is as follows:

{{< copyable "shell-root" >}}

```bash
tiup cluster display prod-cluster
```

```
Starting /root/.tiup/components/cluster/v0.4.5/cluster display prod-cluster
TiDB Cluster: prod-cluster
TiDB Version: v3.0.12
ID                  Role        Host          Ports        Status     Data Dir              Deploy Dir
--                  ----        ----          -----        ------     --------              ----------
172.16.5.134:3000   grafana     172.16.5.134  3000         Up         -                     deploy/grafana-3000
172.16.5.134:2379   pd          172.16.5.134  2379/2380    Up|L       data/pd-2379          deploy/pd-2379
172.16.5.139:2379   pd          172.16.5.139  2379/2380    Up|UI      data/pd-2379          deploy/pd-2379
172.16.5.140:2379   pd          172.16.5.140  2379/2380    Up         data/pd-2379          deploy/pd-2379
172.16.5.134:9090   prometheus  172.16.5.134  9090         Up         data/prometheus-9090  deploy/prometheus-9090
172.16.5.134:4000   tidb        172.16.5.134  4000/10080   Up         -                     deploy/tidb-4000
172.16.5.139:4000   tidb        172.16.5.139  4000/10080   Up         -                     deploy/tidb-4000
172.16.5.140:4000   tidb        172.16.5.140  4000/10080   Up         -                     deploy/tidb-4000
172.16.5.134:20160  tikv        172.16.5.134  20160/20180  Up         data/tikv-20160       deploy/tikv-20160
172.16.5.139:20160  tikv        172.16.5.139  20160/20180  Up         data/tikv-20160       deploy/tikv-20160
172.16.5.140:20160  tikv        172.16.5.140  20160/20180  Up         data/tikv-20160       deploy/tikv-20160
```

The `Status` column uses `Up` or `Down` to indicate whether the service is running normally.

For the PD component, `|L` or `|UI` might be appended to `Up` or `Down`. `|L` indicates that the PD node is a Leader, and `|UI` indicates that [TiDB Dashboard](/dashboard/dashboard-intro.md) is running on the PD node.

## Scale in a node

> **Note:**
>
> This section describes only the syntax of the scale-in command. For detailed steps of online scaling, refer to [Scale the TiDB Cluster Using TiUP](/scale-tidb-using-tiup.md).

Scaling in a node means taking the node offline. This operation removes the node from the cluster and deletes the remaining data files.

Because the offline process of the TiKV and TiDB Binlog components is asynchronous (which requires removing the node through API), and the process takes a long time (which requires continuous observation on whether the node is successfully taken offline), special treatment is given to the TiKV and TiDB Binlog components.

- For TiKV and Binlog:

    - TiUP cluster takes the node offline through API and directly exits without waiting for the process to be completed.
    - Afterwards, when a command related to the cluster operation is executed, TiUP cluster examines whether there is a TiKV/Binlog node that has been taken offline. If not, TiUP cluster continues with the specified operation; If there is, TiUP cluster takes the following steps:

        1. Stop the service of the node that has been taken offline.
        2. Clean up the data files related to the node.
        3. Remove the node from the cluster topology.

- For other components:

    - When taking the PD component down, TiUP cluster quickly deletes the specified node from the cluster through API, stops the service of the specified PD node, and deletes the related data files.
    - When taking other components down, TiUP cluster directly stops the node service and deletes the related data files.

The basic usage of the scale-in command:

```bash
tiup cluster scale-in <cluster-name> -N <node-id>
```

To use this command, you need to specify at least two flags: the cluster name and the node ID. The node ID can be obtained by using the `tiup cluster display` command in the previous section.

For example, to scale in the TiKV node on `172.16.5.140`, run the following command:

{{< copyable "shell-regular" >}}

```bash
tiup cluster scale-in prod-cluster -N 172.16.5.140:20160
```

By running `tiup cluster display`, you can see that the TiKV node is marked `Offline`:

{{< copyable "shell-root" >}}

```bash
tiup cluster display prod-cluster
```

```
Starting /root/.tiup/components/cluster/v0.4.5/cluster display prod-cluster
TiDB Cluster: prod-cluster
TiDB Version: v3.0.12
ID                  Role        Host          Ports        Status     Data Dir              Deploy Dir
--                  ----        ----          -----        ------     --------              ----------
172.16.5.134:3000   grafana     172.16.5.134  3000         Up         -                     deploy/grafana-3000
172.16.5.134:2379   pd          172.16.5.134  2379/2380    Up|L       data/pd-2379          deploy/pd-2379
172.16.5.139:2379   pd          172.16.5.139  2379/2380    Up|UI      data/pd-2379          deploy/pd-2379
172.16.5.140:2379   pd          172.16.5.140  2379/2380    Up         data/pd-2379          deploy/pd-2379
172.16.5.134:9090   prometheus  172.16.5.134  9090         Up         data/prometheus-9090  deploy/prometheus-9090
172.16.5.134:4000   tidb        172.16.5.134  4000/10080   Up         -                     deploy/tidb-4000
172.16.5.139:4000   tidb        172.16.5.139  4000/10080   Up         -                     deploy/tidb-4000
172.16.5.140:4000   tidb        172.16.5.140  4000/10080   Up         -                     deploy/tidb-4000
172.16.5.134:20160  tikv        172.16.5.134  20160/20180  Up         data/tikv-20160       deploy/tikv-20160
172.16.5.139:20160  tikv        172.16.5.139  20160/20180  Up         data/tikv-20160       deploy/tikv-20160
172.16.5.140:20160  tikv        172.16.5.140  20160/20180  Offline    data/tikv-20160       deploy/tikv-20160
```

After PD schedules the data on the node to other TiKV nodes, this node will be deleted automatically.

## Scale out a node

> **Note:**
>
> This section describes only the syntax of the scale-out command. For detailed steps of online scaling, refer to [Scale the TiDB Cluster Using TiUP](/scale-tidb-using-tiup.md).

The scale-out operation has an inner logic similar to that of deployment: the TiUP cluster component firstly ensures the SSH connection of the node, creates the required directories on the target node, then executes the deployment operation, and starts the node service.

When you scale out PD, the node is added to the cluster by `join`, and the configurations of services associated with PD are updated. When you scale out other services, the service is started directly and added to the cluster.

All services conduct correctness validation when they are scaled out. The validation results show whether the scaling-out is successful.

To scale out a TiKV node and a PD node in the `tidb-test` cluster, take the following steps:

1. Create a `scale.yaml` file, and add IPs of the new TiKV and PD nodes:

    > **Note:**
    >
    > You need to create a topology file, which includes only the description of the new nodes, not the existing nodes.

    ```yaml
    ---
    
    pd_servers:
      - ip: 172.16.5.140
    
    tikv_servers:
      - ip: 172.16.5.140
    ```

2. Perform the scale-out operation. TiUP cluster adds the corresponding nodes to the cluster according to the port, directory, and other information described in `scale.yaml`.

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster scale-out tidb-test scale.yaml
    ```

    After the command is executed, you can check the status of the scaled-out cluster by running `tiup cluster display tidb-test`.

## Rolling upgrade

> **Note:**
>
> This section describes only the syntax of the upgrade command. For detailed steps of online upgrade, refer to [Upgrade TiDB Using TiUP](/upgrade-tidb-using-tiup.md).

The rolling upgrade feature leverages the distributed capabilities of TiDB. The upgrade process is made as transparent as possible to the application, and does not affect the business.

Before the upgrade, TiUP cluster checks whether the configuration file of each component is rational. If so, the components are upgraded node by node; if not, TiUP reports an error and exits. The operations vary with different nodes.

### Operations for different nodes

- Upgrade the PD node

    - First, upgrade non-Leader nodes.
    - After all the non-Leader nodes are upgraded, upgrade the Leader node.
        - The upgrade tool sends a command to PD that migrates Leader to an already upgraded node.
        - After the Leader role is switched to another node, upgrade the previous Leader node.
    - During the upgrade, if any unhealthy node is detected, the tool stops this upgrade operation and exits. You need to manually analyze the cause, fix the issue and run the upgrade again.

- Upgrade the TiKV node

    - First, add a scheduling operation in PD that migrates the Region Leader of this TiKV node. This ensures that the upgrade process does not affect the business.
    - After the Leader is migrated, upgrade this TiKV node.
    - After the upgraded TiKV is started normally, remove the scheduling of the Leader.

- Upgrade other services

    - Stop the service normally and update the node.

### Upgrade command

The flags for the upgrade command is as follows:

```bash
Usage:
  cluster upgrade <cluster-name> <version> [flags]

Flags:
      --force                  Force upgrade won't transfer leader
  -h, --help                   help for upgrade
      --transfer-timeout int   Timeout in seconds when transferring PD and TiKV store leaders (default 300)

Global Flags:
      --ssh-timeout int   Timeout in seconds to connect host via SSH, ignored for operations that don't need an SSH connection. (default 5)
  -y, --yes               Skip all confirmations and assumes 'yes'
```

For example, the following command upgrades the cluster to v4.0.0-rc:

{{< copyable "shell-regular" >}}

```bash
tiup cluster upgrade tidb-test v4.0.0-rc
```

## Update configuration

If you want to dynamically update the component configurations, the TiUP cluster component saves a current configuration for each cluster. To edit this configuration, execute the `tiup cluster edit-config <cluster-name>` command. For example:

{{< copyable "shell-regular" >}}

```bash
tiup cluster edit-config prod-cluster
```

TiUP cluster opens the configuration file in the vi editor. If you want to use other editors, use the `EDITOR` environment variable to customize the editor, such as `export EDITOR=nano`.

After editing the file, save the changes. To apply the new configuration to the cluster, execute the following command:

{{< copyable "shell-regular" >}}

```bash
tiup cluster reload prod-cluster
```

The command sends the configuration to the target machine and restarts the cluster to make the configuration take effect.

## Update component

For normal upgrade, you can use the `upgrade` command. But in some scenarios, such as debugging, you might need to replace the currently running component with a temporary package. To achieve this, use the `patch` command:

{{< copyable "shell-root" >}}

```bash
tiup cluster patch --help
```

```
Replace the remote package with a specified package and restart the service

Usage:
  cluster patch <cluster-name> <package-path> [flags]

Flags:
  -h, --help                   help for patch
  -N, --node strings           Specify the nodes
      --overwrite              Use this package in the future scale-out operations
  -R, --role strings           Specify the role
      --transfer-timeout int   Timeout in seconds when transferring PD and TiKV store leaders (default 300)

Global Flags:
      --ssh-timeout int   Timeout in seconds to connect host via SSH, ignored for operations that don't need an SSH connection. (default 5)
  -y, --yes               Skip all confirmations and assumes 'yes'
```

If a TiDB hotfix package is in `/tmp/tidb-hotfix.tar.gz` and you want to replace all the TiDB packages in the cluster, run the following command:

{{< copyable "shell-regular" >}}

```bash
tiup cluster patch test-cluster /tmp/tidb-hotfix.tar.gz -R tidb
```

You can also replace only one TiDB package in the cluster:

{{< copyable "shell-regular" >}}

```bash
tiup cluster patch test-cluster /tmp/tidb-hotfix.tar.gz -N 172.16.4.5:4000
```

## Import TiDB Ansible cluster

Before TiUP is released, TiDB Ansible is often used to deploy TiDB clusters. To enable TiUP to take over the cluster deployed by TiDB Ansible, use the `import` command.

The usage of the `import` command is as follows:

{{< copyable "shell-root" >}}

```bash
tiup cluster import --help
```

```
Import an exist TiDB cluster from TiDB-Ansible

Usage:
  cluster import [flags]

Flags:
  -d, --dir string         The path to TiDB-Ansible directory
  -h, --help               help for import
      --inventory string   The name of inventory file (default "inventory.ini")
      --no-backup          Don't backup ansible dir, useful when there're multiple inventory files
  -r, --rename NAME        Rename the imported cluster to NAME

Global Flags:
      --ssh-timeout int   Timeout in seconds to connect host via SSH, ignored for operations that don't need an SSH connection. (default 5)
  -y, --yes               Skip all confirmations and assumes 'yes'
```

You can use either of the following commands to import a TiDB Ansible cluster:

{{< copyable "shell-regular" >}}

```bash
cd tidb-ansible
tiup cluster import
```

{{< copyable "shell-regular" >}}

```bash
tiup cluster import --dir=/path/to/tidb-ansible
```

## View the operation log

To view the operation log, use the `audit` command. The usage of the `audit` command is as follows:

```bash
Usage:
  tiup cluster audit [audit-id] [flags]

Flags:
  -h, --help   help for audit
```

If the `[audit-id]` flag is not specified, the command shows a list of commands that have been executed. For example:

{{< copyable "shell-regular" >}}

```bash
tiup cluster audit
```

```
Starting component `cluster`: /Users/joshua/.tiup/components/cluster/v0.6.0/cluster audit
ID      Time                       Command
--      ----                       -------
4BLhr0  2020-04-29T13:25:09+08:00  /Users/joshua/.tiup/components/cluster/v0.6.0/cluster deploy test v4.0.0-rc /tmp/topology.yaml
4BKWjF  2020-04-28T23:36:57+08:00  /Users/joshua/.tiup/components/cluster/v0.6.0/cluster deploy test v4.0.0-rc /tmp/topology.yaml
4BKVwH  2020-04-28T23:02:08+08:00  /Users/joshua/.tiup/components/cluster/v0.6.0/cluster deploy test v4.0.0-rc /tmp/topology.yaml
4BKKH1  2020-04-28T16:39:04+08:00  /Users/joshua/.tiup/components/cluster/v0.4.9/cluster destroy test
4BKKDx  2020-04-28T16:36:57+08:00  /Users/joshua/.tiup/components/cluster/v0.4.9/cluster deploy test v4.0.0-rc /tmp/topology.yaml
```

The first column is `audit-id`. To view the execution log of a certain command, pass the `audit-id` of a command as the flag as follows:

{{< copyable "shell-regular" >}}

```bash
tiup cluster audit 4BLhr0
```

## Run commands on a host in the TiDB cluster

To run command on a host in the TiDB cluster, use the `exec` command. The usage of the `exec` command is as follows:

```bash
Usage:
  cluster exec <cluster-name> [flags]

Flags:
      --command string   the command run on cluster host (default "ls")
  -h, --help             help for exec
  -N, --node strings     Only exec on host with specified nodes
  -R, --role strings     Only exec on host with specified roles
      --sudo            use root permissions (default false)

Global Flags:
      --ssh-timeout int   Timeout in seconds to connect host via SSH, ignored for operations that don't need an SSH connection. (default 5)
  -y, --yes               Skip all confirmations and assumes 'yes'
```

For example, to execute `ls /tmp` on all TiDB nodes, run the following command:

{{< copyable "shell-regular" >}}

```bash
tiup cluster exec test-cluster --command='ls /tmp'
```

## Cluster controllers

Before TiUP is released, you can control the cluster using `tidb-ctl`, `tikv-ctl`, `pd-ctl`, and other tools. To make the tools easier to download and use, TiUP integrates them into an all-in-one component, `ctl`.

```bash
Usage:
  tiup ctl {tidb/pd/tikv/binlog/etcd} [flags]

Flags:
  -h, --help   help for tiup
```

This command has a corresponding relationship with those of the previous tools:

```bash
tidb-ctl [args] = tiup ctl tidb [args]
pd-ctl [args] = tiup ctl pd [args]
tikv-ctl [args] = tiup ctl tikv [args]
binlogctl [args] = tiup ctl bindlog [args]
etcdctl [args] = tiup ctl etcd [args]
```

For example, if you previously view the store by running `pd-ctl -u http://127.0.0.1:2379 store`, now you can run the following command in TiUP:

{{< copyable "shell-regular" >}}

```bash
tiup ctl pd -u http://127.0.0.1:2379 store
```

## Environment checks for target machines

You can use the `check` command to perform a series of checks on the environment of the target machine and output the check results. By executing the `check` command, you can find common unreasonable configurations or unsupported situations. The command flag list is as follows:

```bash
Usage:
  tiup cluster check <topology.yml | cluster-name> [flags]
Flags:
      --apply                  Try to fix failed checks
      --cluster                Check existing cluster, the input is a cluster name.
      --enable-cpu             Enable CPU thread count check
      --enable-disk            Enable disk IO (fio) check
      --enable-mem             Enable memory size check
  -h, --help                   help for check
  -i, --identity_file string   The path of the SSH identity file. If specified, public key authentication will be used.
  -p, --password               Use password of target hosts. If specified, password authentication will be used.
      --user string            The user name to login via SSH. The user must has root (or sudo) privilege.
```

By default, this command is used to check the environment before deployment. By specifying the `--cluster` flag to switch the mode, you can also check the target machines of an existing cluster, for example:

```bash
# check deployed servers before deployment
tiup cluster check topology.yml --user tidb -p
# check deployed servers of an existing cluster
tiup cluster check <cluster-name> --cluster
```

The CPU thread count check, memory size check, and disk performance check are disabled by default. For the production environment, it is recommended that you enable the three checks and make sure they pass to obtain the best performance.

- CPU: If the number of threads is greater than or equal to 16, the check is passed.
- Memory: If the total size of physical memory is greater than or equal to 32 GB, the check is passed.
- Disk: Execute `fio` test on the partitions of `data_dir` and record the results.

When running the checks, if the `--apply` flag is specified, the program automatically repairs the failed items. Automatic repair is limited to some items that can be adjusted by modifying the configuration or system parameters. Other unrepaired items need to be handled manually according to the actual situation.

Environment checks are not necessary for deploying a cluster. For the production environment, it is recommended to perform environment checks and pass all check items before deployment. If not all the check items are passed, the cluster might be deployed and run normally, but the best performance might not be obtained.
