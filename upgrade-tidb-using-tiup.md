---
title: Upgrade TiDB Using TiUP
summary: Learn how to upgrade TiDB using TiUP.
aliases: ['/docs/dev/upgrade-tidb-using-tiup/','/docs/dev/how-to/upgrade/using-tiup/','/tidb/dev/upgrade-tidb-using-tiup-offline','/docs/dev/upgrade-tidb-using-tiup-offline/']
---

# Upgrade TiDB Using TiUP

This document is targeted for the following upgrade paths:

- Upgrade from TiDB 4.0 versions to TiDB 5.1 versions.
- Upgrade from TiDB 5.0 versions to TiDB 5.1 versions.

> **Note:**
>
> If your cluster to be upgraded is v3.1 or an earlier version (v3.0 or v2.1), the direct upgrade to v5.1 or its patch versions is not supported. You need to upgrade your cluster first to v4.0 and then to v5.1.

## Upgrade caveat

- TiDB currently does not support version downgrade or rolling back to an earlier version after the upgrade.
- For the v4.0 cluster managed using TiDB Ansible, you need to import the cluster to TiUP (`tiup cluster`) for new management according to [Upgrade TiDB Using TiUP (v4.0)](https://docs.pingcap.com/tidb/v4.0/upgrade-tidb-using-tiup#import-tidb-ansible-and-the-inventoryini-configuration-to-tiup). Then you can upgrade the cluster to v5.1 or its patch versions according to this document.
- To update versions earlier than 3.0 to 5.1:
    1. Update this version to 3.0 using [TiDB Ansible](https://docs.pingcap.com/tidb/v3.0/upgrade-tidb-using-ansible).
    2. Use TiUP (`tiup cluster`) to import the TiDB Ansible configuration.
    3. Update the 3.0 version to 4.0 according to [Upgrade TiDB Using TiUP (v4.0)](https://docs.pingcap.com/tidb/v4.0/upgrade-tidb-using-tiup#import-tidb-ansible-and-the-inventoryini-configuration-to-tiup).
    4. Upgrade the cluster to v5.1 according to this document.
- Support upgrading the versions of TiDB Binlog, TiCDC, TiFlash, and other components.
- For detailed compatibility changes of different versions, see the [Release Notes](/releases/release-notes.md) of each version. Modify your cluster configuration according to the "Compatibility Changes" section of the corresponding release notes.

> **Note:**
>
> Do not execute any DDL request during the upgrade, otherwise an undefined behavior issue might occur.

## Preparations

This section introduces the preparation works needed before upgrading your TiDB cluster, including upgrading TiUP and the TiUP Cluster component.

### Step 1: Upgrade TiUP or TiUP offline mirror

Before upgrading your TiDB cluster, you first need to upgrade TiUP or TiUP mirror.

#### Upgrade TiUP and TiUP Cluster

> **Note:**
>
> If the control machine of the cluster to upgrade cannot access `https://tiup-mirrors.pingcap.com`, skip this section and see [Upgrade TiUP offline mirror](#upgrade-tiup-offline-mirror).

1. Upgrade the TiUP version. It is recommended that the TiUP version is `1.5.0` or later.

    {{< copyable "shell-regular" >}}

    ```shell
    tiup update --self
    tiup --version
    ```

2. Upgrade the TiUP Cluster version. It is recommended that the TiUP Cluster version is `1.5.0` or later.

    {{< copyable "shell-regular" >}}

    ```shell
    tiup update cluster
    tiup cluster --version
    ```

#### Upgrade TiUP offline mirror

> **Note:**
>
> If the cluster to upgrade was deployed not using the offline method, skip this step.

Refer to [Deploy a TiDB Cluster Using TiUP - Deploy TiUP offline](/production-deployment-using-tiup.md#method-2-deploy-tiup-offline) to download the TiUP mirror of the new version and upload it to the control machine. After executing `local_install.sh`, TiUP will complete the overwrite upgrade.

{{< copyable "shell-regular" >}}

```shell
tar xzvf tidb-community-server-${version}-linux-amd64.tar.gz
sh tidb-community-server-${version}-linux-amd64/local_install.sh
source /home/tidb/.bash_profile
```

After the overwrite upgrade, execute the following command to upgrade the TiUP Cluster component.

{{< copyable "shell-regular" >}}

```shell
tiup update cluster
```

Now, the offline mirror has been upgraded successfully. If an error occurs during TiUP operation after the overwriting, it might be that the `manifest` is not updated. You can try `rm -rf ~/.tiup/manifests/*` before running TiUP again.

### Step 2: Edit TiUP topology configuration file

> **Note:**
>
> Skip this step if one of the following situations applies:
>
> + You have not modified the configuration parameters of the original cluster. Or you have modified the configuration parameters using `tiup cluster` but no more modification is needed.
> + After the upgrade, you want to use v5.1's default parameter values for the unmodified configuration items.

1. Enter the `vi` editing mode to edit the topology file:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster edit-config <cluster-name>
    ```

2. Refer to the format of [topology](https://github.com/pingcap/tiup/blob/master/embed/examples/cluster/topology.example.yaml) configuration template and fill the parameters you want to modify in the `server_configs` section of the topology file.

3. After the modification, enter <kbd>:</kbd> + <kbd>w</kbd> + <kbd>q</kbd> to save the change and exit the editing mode. Enter <kbd>Y</kbd> to confirm the change.

> **Note:**
>
> Before you upgrade the cluster to v5.1, make sure that the parameters you have modified in v4.0 are compatible in v5.1. For details, see [TiKV Configuration File](/tikv-configuration-file.md).
>
> The following three TiKV parameters are obsolete in TiDB v5.1. If the following parameters have been configured in your original cluster, you need to delete these parameters through `edit-config`:
>
> - pessimistic-txn.enabled
> - server.request-batch-enable-cross-command
> - server.request-batch-wait-duration

### Step 3: Check the health status of the current cluster

To avoid the undefined behaviors or other issues during the upgrade, it is recommended to check the health status of Regions of the current cluster before the upgrade. To do that, you can use the `check` sub-command.

{{< copyable "shell-regular" >}}

```shell
tiup cluster check <cluster-name> --cluster
```

After the command is executed, the "Region status" check result will be output.

+ If the result is "All Regions are healthy", all Regions in the current cluster are healthy and you can continue the upgrade.
+ If the result is "Regions are not fully healthy: m miss-peer, n pending-peer" with the "Please fix unhealthy regions before other operations." prompt, some Regions in the current cluster are abnormal. You need to troubleshoot the anomalies until the check result becomes "All Regions are healthy". Then you can continue the upgrade.

## Perform a rolling upgrade to the TiDB cluster

This section describes how to perform a rolling upgrade to the TiDB cluster and how to verify the version after the upgrade.

### Upgrade the TiDB cluster to a specified version

You can upgrade your cluster in one of the two ways: online upgrade and offline upgrade.

By default, TiUP Cluster upgrades the TiDB cluster using the online method, which means that the TiDB cluster can still provide services during the upgrade process. With the online method, the leaders are migrated one by one on each node before the upgrade and restart. Therefore, for a large-scale cluster, it takes a long time to complete the entire upgrade operation.

If your application has a maintenance window for the database to be stopped for maintenance, you can use the offline upgrade method to quickly perform the upgrade operation.

#### Online upgrade

{{< copyable "shell-regular" >}}

```shell
tiup cluster upgrade <cluster-name> <version>
```

For example, if you want to upgrade the cluster to v5.1.0:

{{< copyable "shell-regular" >}}

```shell
tiup cluster upgrade <cluster-name> v5.1.0
```

> **Note:**
>
> + Performing a rolling upgrade to the cluster will upgrade all components one by one. During the upgrade of TiKV, all leaders in a TiKV instance are evicted before stopping the instance. The default timeout time is 5 minutes (300 seconds). The instance is directly stopped after this timeout time.
>
> + To perform the upgrade immediately without evicting the leader, specify `--force` in the command above. This method causes performance jitter but not data loss.
>
> + To keep a stable performance, make sure that all leaders in a TiKV instance are evicted before stopping the instance. You can set `--transfer-timeout` to a larger value, for example, `--transfer-timeout 3600` (unit: second).

#### Offline upgrade

1. Before the offline upgrade, you first need to stop the entire cluster.

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster stop <cluster-name>
    ```

2. Use the `upgrade` command with the `--offline` option to perform the offline upgrade.

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster upgrade <cluster-name> <version> --offline
    ```

3. After the upgrade, the cluster will not be automatically restarted. You need to use the `start` command to restart it.

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster start <cluster-name>
    ```

### Verify the cluster version

Execute the `display` command to view the latest cluster version `TiDB Version`:

{{< copyable "shell-regular" >}}

```shell
tiup cluster display <cluster-name>
```

```
Cluster type:       tidb
Cluster name:       <cluster-name>
Cluster version:    v5.1.0
```

> **Note:**
>
> By default, TiUP and TiDB share usage details with PingCAP to help understand how to improve the product. For details about what is shared and how to disable the sharing, see [Telemetry](/telemetry.md).

## FAQ

This section describes common problems encountered when updating the TiDB cluster using TiUP.

### If an error occurs and the upgrade is interrupted, how to resume the upgrade after fixing this error?

Re-execute the `tiup cluster upgrade` command to resume the upgrade. The upgrade operation restarts the nodes that have been previously upgraded. If you do not want the upgraded nodes to be restarted, use the `replay` sub-command to retry the operation:

1. Execute `tiup cluster audit` to see the operation records:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster audit
    ```

    Find the failed upgrade operation record and keep the ID of this operation record. The ID is the `<audit-id>` value in the next step.

2. Execute `tiup cluster replay <audit-id>` to retry the corresponding operation:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster replay <audit-id>
    ```

### The evict leader has waited too long during the upgrade. How to skip this step for a quick upgrade?

You can specify `--force`. Then the processes of transferring PD leader and evicting TiKV leader are skipped during the upgrade. The cluster is directly restarted to update the version, which has a great impact on the cluster that runs online. Here is the command:

{{< copyable "shell-regular" >}}

```shell
tiup cluster upgrade <cluster-name> <version> --force
```

### How to update the version of tools such as pd-ctl after upgrading the TiDB cluster?

You can upgrade the tool version by using TiUP to install the `ctl` component of the corresponding version:

{{< copyable "shell-regular" >}}

```shell
tiup install ctl:v5.1.0
```

## TiDB 5.1 compatibility changes

- See TiDB 5.1 Release Notes for the compatibility changes.
- Try to avoid creating a new clustered index table when you apply rolling updates to the clusters using TiDB-Binlog.
