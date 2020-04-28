---
title: Upgrade TiDB Using TiUP
summary: Learn how to upgrade TiDB using TiUP.
category: how-to
---

# Upgrade TiDB Using TiUP

This document is targeted for users who want to upgrade from TiDB 3.0 versions to TiDB 4.0 versions, or from TiDB 4.0 to a later version.

If you have deployed the TiDB cluster using TiDB Ansible, you can use TiUP to import the TiDB Ansible configuration and perform the upgrade.

## Upgrade caveat

- Rolling back to 3.0 versions after the update is not supported.
- To update versions earlier than 3.0 to 4.0, first update this version to 3.0 using TiDB Ansible, and use TiUP to import the TiDB Ansible configuration and update the 3.0 version to 4.0.
- After the TiDB Ansible configuration is imported into and managed by TiUP, you can no longer operate on the cluster using TiDB Ansible. Otherwise, conflicts might occur because of the inconsistent metadata.
- Currently, you cannot import the TiDB Ansible configuration if the cluster deployed using TiDB Ansible meets one of the following situations:
    - The TLS encryption is enabled for the cluster.
    - This is a pure key-value cluster (cluster with no TiDB instance).
    - `Kafka` is enabled for the cluster.
    - `Spark` is enabled for the cluster.
    - `Lightning` / `Importer` is enabled for the cluster.
    - You still use the `'push'` method to collect monitoring metrics (since v3.0, `pull` is the default mode, which is supported if you have not modified this mode).
    - In the `inventory.ini` configuration file, the `node_exporter` or `blackbox_exporter` item of the machine is set to non-default ports through `node_exporter_port` or `blackbox_exporter_port`, which is compatible if you have unified the configuration in the `group_vars` directory.

## Install TiUP on the Control Machine

1. Execute the following command on the Control Machine to install TiUP:

    {{< copyable "shell-regular" >}}

    ```shell
    curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
    ```

2. Redeclare the global environment variables:

    {{< copyable "shell-regular" >}}

    ```shell
    source .bash_profile
    ```

3. Check whether TiUP is installed:

    {{< copyable "shell-regular" >}}

    ```shell
    which tiup
    ```

4. Install the TiUP cluster tool:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster
    ```

If you have installed TiUP before, execute the following command to update TiUP to the latest version:

{{< copyable "shell-regular" >}}

```shell
tiup update cluster
```

## Import TiDB Ansible and the `inventory.ini` configuration to TiUP

> **Note:**
>
> + If the original cluster is deployed using TiUP, you can skip this step.
> + Currently, the `inventory.ini` configuration file is identified by default. If your configuration file uses another name, specify this name.
> + Ensure that the state of the current cluster is consistent with the topology in `inventory.ini`; that components of the cluster are operating normally. Otherwise, the cluster metadata becomes abnormal after the import.

### Import the TiDB Ansible cluster to TiUP

1. Execute the following command to import the TiDB Ansible cluster into TiUP (for example, in the `/home/tidb/tidb-ansible` path). Do not execute this command in the Ansible directory.

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster import -d /home/tidb/tidb-ansible
    ```

2. After executing the above import command, if the `Inventory` information of the cluster is parsed successfully, the following prompt appears:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster import -d /home/tidb/tidb-ansible/
    ```

    ```
    Found inventory file /home/tidb/tidb-ansible/inventory.ini, parsing...
    Found cluster "ansible-cluster" (v3.0.12), deployed with user tidb.
    Prepared to import TiDB v3.0.12 cluster ansible-cluster.
    Do you want to continue? [y/N]:
    ```

3. After checking that the parsed cluster name and the version are correct, enter `y` to continue the import process.

    + If an error occurs when parsing the `Inventory` information, the import process is stopped, which does not have any impact on the original Ansible deployment method. Then you need to adjust and retry the process according to the error prompt.

    + If the original cluster name in Ansible is the same with any existing cluster name in TiUP, a warning message is returned with a new cluster name. Therefore, **do not repeatedly import the same cluster**, which results in multiple names for the same cluster in TiUP.

After the import is complete, you can check the current cluster status by executing the `tiup cluster display <cluster-name>` command to verify the import result. Because the `display` command is used to query the real-time status of each node, it might take a little time to execute the command.

### Edit TiUP topology configuration file

> **Note:**
>
> You can skip this step for the following situations:
>
> - The configuration parameters in the original cluster have not been modified.
> - You want to use the default parameters of `4.0` after the upgrade.

1. Enter the `tidb-ansible / conf` configuration directory and confirm the modified parameters in the configuration template.

2. Enter the `vi` editing mode of the topology file:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster edit-config <cluster-name>
    ```

3. See the configuration template format of [topology](https://github.com/pingcap-incubator/tiup-cluster/blob/master/examples/topology.example.yaml) and fill in the modified parameters of the original cluster in the `server_configs` section of the topology file.

    Even if the label has been configured for the cluster, you also need to fill in the label in the configuration according to the format in the template. In later versions, the label will be automatically imported.

    After the modification is completed, execute the `wq` command to save the change and exit the editing mode. Enter `Y` to confirm the change.

> **Note:**
>
> Before upgrading to v4.0, confirm that the parameters modified in v3.0 are compatible in v4.0. See [configuration template](/reference/configuration/tikv-server/configuration-file.md) for details.

## Perform a rolling update to the TiDB cluster

This section describes how to perform a rolling update to the TiDB cluster and how to verify the version after the update.

### Perform a rolling update to the TiDB cluster (to v4.0.0-rc)

{{< copyable "shell-regular" >}}

```shell
tiup cluster upgrade <cluster-name> v4.0.0-rc
```

Performing the rolling update to the cluster will update all components one by one. During the upgrade of TiKV, all leaders in a TiKV instance are evicted before stopping the instance. The default timeout time is 5 minutes. The instance is directly stopped after this timeout time.

To perform the upgrade immediately without evicting the leader, specify `--force` in the command above. This method causes performance jitter but not data loss.

To keep a stable performance, make sure that all leaders in a TiKV instance are evicted before stopping the instance. You can set `--transfer-timeout` to a super large value, for example, `--transfer-timeout 100000000` (unit: second).

### Verify the cluster version

Execute the `display` command to view the latest cluster version `TiDB Version`:

{{< copyable "shell-regular" >}}

```shell
tiup cluster display <cluster-name>
```

```
Starting /home/tidblk/.tiup/components/cluster/v0.4.3/cluster display <cluster-name>
TiDB Cluster: <cluster-name>
TiDB Version: v4.0.0-rc
```

## FAQ

This section describes common problems encountered when updating the TiDB cluster using TiUP.

### If an error occurs and the updated is interrupted, how to resume the update from the point of the interruption after fixing this error?

You can specify `--role` or `--node` to update the specified component or node. Here is the command:

{{< copyable "shell-regular" >}}

```shell
tiup cluster upgrade <cluster-name> v4.0.0-rc --role tidb
```

or

{{< copyable "shell-regular" >}}

```shell
tiup cluster upgrade <cluster-name> v4.0.0-rc --node <ID>
```

### The evict leader has waited too long during the update. How to skip this step for a quick update?

You can specify `--force`. Then the processes of transferring PD leader and evicting TiKV leader are skipped during the update. The cluster is directly restarted to update the version, which has a great impact on the cluster that runs online. Here is the command:

{{< copyable "shell-regular" >}}

```shell
tiup cluster upgrade <cluster-name> v4.0.0-rc --force
```

### How to update the version of tools such as pd-ctl after updating the TiDB cluster?

Currently, TiUP does not update and manage the version of tools. If you need the tool package of the latest version, directly download the TiDB package and replace `{version}` with the corresponding version such as `v4.0.0-rc`. Here is the download address:

{{< copyable "" >}}

```
https://download.pingcap.org/tidb-{version}-linux-amd64.tar.gz
```

## TiDB 4.0 compatibility changes

- If you set the value of the `oom-action` parameter to `cancel`, when the query statement triggers the OOM threshold, the statement is killed. In v4.0, in addition to `select`, DML statements such as `insert`/`update`/`delete` might also be killed.
- TiDB v4.0 supports the length check for table names. The length limit is 64 characters. If you rename a table after the upgrade and the new name exceeds this length limit, an error is reported. v3.0 and earlier versions do not have this error reporting.
- In v4.0, the format of the `explain` execution plan is improved. Pay attention to any automatic analysis program that is customized for `explain`.
