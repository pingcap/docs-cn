---
title: Upgrade TiDB Using TiUP
summary: Learn how to upgrade TiDB using TiUP.
aliases: ['/docs/dev/upgrade-tidb-using-tiup/','/docs/dev/how-to/upgrade/using-tiup/','/tidb/dev/upgrade-tidb-using-tiup-offline','/docs/dev/upgrade-tidb-using-tiup-offline/']
---

# Upgrade TiDB Using TiUP

This document is targeted for the following upgrade paths:

- Upgrade from TiDB 4.0 versions to TiDB 6.5.
- Upgrade from TiDB 5.0-5.4 versions to TiDB 6.5.
- Upgrade from TiDB 6.0 to TiDB 6.5.
- Upgrade from TiDB 6.1 to TiDB 6.5.
- Upgrade from TiDB 6.2 to TiDB 6.5.
- Upgrade from TiDB 6.3 to TiDB 6.5.
- Upgrade from TiDB 6.4 to TiDB 6.5.

> **Warning:**
>
> - You cannot upgrade TiFlash online from versions earlier than 5.3 to 5.3 or later. Instead, you must first stop all the TiFlash instances of the early version, and then upgrade the cluster offline. If other components (such as TiDB and TiKV) do not support an online upgrade, follow the instructions in warnings in [Online upgrade](#online-upgrade).
> - **DO NOT** upgrade a TiDB cluster when a DDL statement is being executed in the cluster (usually for the time-consuming DDL statements such as `ADD INDEX` and the column type changes).
> - Before the upgrade, it is recommended to use the [`ADMIN SHOW DDL`](/sql-statements/sql-statement-admin-show-ddl.md) command to check whether the TiDB cluster has an ongoing DDL job. If the cluster has a DDL job, to upgrade the cluster, wait until the DDL execution is finished or use the [`ADMIN CANCEL DDL`](/sql-statements/sql-statement-admin-cancel-ddl.md) command to cancel the DDL job before you upgrade the cluster.
> - In addition, during the cluster upgrade, **DO NOT** execute any DDL statement. Otherwise, the issue of undefined behavior might occur.

> **Note:**
>
> If your cluster to be upgraded is v3.1 or an earlier version (v3.0 or v2.1), the direct upgrade to v6.5.0 is not supported. You need to upgrade your cluster first to v4.0 and then to v6.5.0.

## Upgrade caveat

- TiDB currently does not support version downgrade or rolling back to an earlier version after the upgrade.
- For the v4.0 cluster managed using TiDB Ansible, you need to import the cluster to TiUP (`tiup cluster`) for new management according to [Upgrade TiDB Using TiUP (v4.0)](https://docs.pingcap.com/tidb/v4.0/upgrade-tidb-using-tiup#import-tidb-ansible-and-the-inventoryini-configuration-to-tiup). Then you can upgrade the cluster to v6.5.0 according to this document.
- To update versions earlier than v3.0 to v6.5.0:
    1. Update this version to 3.0 using [TiDB Ansible](https://docs.pingcap.com/tidb/v3.0/upgrade-tidb-using-ansible).
    2. Use TiUP (`tiup cluster`) to import the TiDB Ansible configuration.
    3. Update the 3.0 version to 4.0 according to [Upgrade TiDB Using TiUP (v4.0)](https://docs.pingcap.com/tidb/v4.0/upgrade-tidb-using-tiup#import-tidb-ansible-and-the-inventoryini-configuration-to-tiup).
    4. Upgrade the cluster to v6.5.0 according to this document.
- Support upgrading the versions of TiDB Binlog, TiCDC, TiFlash, and other components.
- When upgrading TiFlash from versions earlier than v6.3.0 to v6.3.0 and later versions, note that the CPU must support the AVX2 instruction set under the Linux AMD64 architecture and the ARMv8 instruction set architecture under the Linux ARM64 architecture. For details, see the description in [v6.3.0 Release Notes](/releases/release-6.3.0.md#others).
- For detailed compatibility changes of different versions, see the [Release Notes](/releases/release-notes.md) of each version. Modify your cluster configuration according to the "Compatibility Changes" section of the corresponding release notes.
- For clusters that upgrade from versions earlier than v5.3 to v5.3 or later versions, the default deployed Prometheus will upgrade from v2.8.1 to v2.27.1. Prometheus v2.27.1 provides more features and fixes a security issue. Compared with v2.8.1, alert time representation in v2.27.1 is changed. For more details, see [Prometheus commit](https://github.com/prometheus/prometheus/commit/7646cbca328278585be15fa615e22f2a50b47d06) for more details.

## Preparations

This section introduces the preparation works needed before upgrading your TiDB cluster, including upgrading TiUP and the TiUP Cluster component.

### Step 1: Review compatibility changes

Review [the compatibility changes](/releases/release-6.5.0.md#compatibility-changes) and [deprecated features](/releases/release-6.5.0.md#deprecated-feature) in TiDB v6.5.0 release notes. If any changes affect your upgrade, take actions accordingly.

### Step 2: Upgrade TiUP or TiUP offline mirror

Before upgrading your TiDB cluster, you first need to upgrade TiUP or TiUP mirror.

#### Upgrade TiUP and TiUP Cluster

> **Note:**
>
> If the control machine of the cluster to upgrade cannot access `https://tiup-mirrors.pingcap.com`, skip this section and see [Upgrade TiUP offline mirror](#upgrade-tiup-offline-mirror).

1. Upgrade the TiUP version. It is recommended that the TiUP version is `1.11.0` or later.

    {{< copyable "shell-regular" >}}

    ```shell
    tiup update --self
    tiup --version
    ```

2. Upgrade the TiUP Cluster version. It is recommended that the TiUP Cluster version is `1.11.0` or later.

    {{< copyable "shell-regular" >}}

    ```shell
    tiup update cluster
    tiup cluster --version
    ```

#### Upgrade TiUP offline mirror

> **Note:**
>
> If the cluster to upgrade was deployed not using the offline method, skip this step.

Refer to [Deploy a TiDB Cluster Using TiUP - Deploy TiUP offline](/production-deployment-using-tiup.md#deploy-tiup-offline) to download the TiUP mirror of the new version and upload it to the control machine. After executing `local_install.sh`, TiUP will complete the overwrite upgrade.

{{< copyable "shell-regular" >}}

```shell
tar xzvf tidb-community-server-${version}-linux-amd64.tar.gz
sh tidb-community-server-${version}-linux-amd64/local_install.sh
source /home/tidb/.bash_profile
```

After the overwrite upgrade, run the following command to merge the server and toolkit offline mirrors to the server directory:

{{< copyable "shell-regular" >}}

```bash
tar xf tidb-community-toolkit-${version}-linux-amd64.tar.gz
ls -ld tidb-community-server-${version}-linux-amd64 tidb-community-toolkit-${version}-linux-amd64
cd tidb-community-server-${version}-linux-amd64/
cp -rp keys ~/.tiup/
tiup mirror merge ../tidb-community-toolkit-${version}-linux-amd64
```

After merging the mirrors, run the following command to upgrade the TiUP Cluster component:

{{< copyable "shell-regular" >}}

```shell
tiup update cluster
```

Now, the offline mirror has been upgraded successfully. If an error occurs during TiUP operation after the overwriting, it might be that the `manifest` is not updated. You can try `rm -rf ~/.tiup/manifests/*` before running TiUP again.

### Step 3: Edit TiUP topology configuration file

> **Note:**
>
> Skip this step if one of the following situations applies:
>
> + You have not modified the configuration parameters of the original cluster. Or you have modified the configuration parameters using `tiup cluster` but no more modification is needed.
> + After the upgrade, you want to use v6.5.0's default parameter values for the unmodified configuration items.

1. Enter the `vi` editing mode to edit the topology file:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster edit-config <cluster-name>
    ```

2. Refer to the format of [topology](https://github.com/pingcap/tiup/blob/master/embed/examples/cluster/topology.example.yaml) configuration template and fill the parameters you want to modify in the `server_configs` section of the topology file.

3. After the modification, enter <kbd>:</kbd> + <kbd>w</kbd> + <kbd>q</kbd> to save the change and exit the editing mode. Enter <kbd>Y</kbd> to confirm the change.

> **Note:**
>
> Before you upgrade the cluster to v6.5.0, make sure that the parameters you have modified in v4.0 are compatible in v6.5.0. For details, see [TiKV Configuration File](/tikv-configuration-file.md).

### Step 4: Check the health status of the current cluster

To avoid the undefined behaviors or other issues during the upgrade, it is recommended to check the health status of Regions of the current cluster before the upgrade. To do that, you can use the `check` sub-command.

{{< copyable "shell-regular" >}}

```shell
tiup cluster check <cluster-name> --cluster
```

After the command is executed, the "Region status" check result will be output.

+ If the result is "All Regions are healthy", all Regions in the current cluster are healthy and you can continue the upgrade.
+ If the result is "Regions are not fully healthy: m miss-peer, n pending-peer" with the "Please fix unhealthy regions before other operations." prompt, some Regions in the current cluster are abnormal. You need to troubleshoot the anomalies until the check result becomes "All Regions are healthy". Then you can continue the upgrade.

### Step 5: Check the DDL and backup status of the cluster

To avoid undefined behaviors or other unexpected problems during the upgrade, it is recommended to check the following items before the upgrade.

- Cluster DDLs: It is recommended to execute the [`ADMIN SHOW DDL`](/sql-statements/sql-statement-admin-show-ddl.md) statement to check whether there is an ongoing DDL job. If yes, wait for its execution or cancel it by executing the [`ADMIN CANCEL DDL`](/sql-statements/sql-statement-admin-cancel-ddl.md) statement before performing an upgrade.
- Cluster backup: It is recommended to execute the [`SHOW [BACKUPS|RESTORES]`](/sql-statements/sql-statement-show-backups.md) statement to check whether there is an ongoing backup or restore task in the cluster. If yes, wait for its completion before performing an upgrade.

## Upgrade the TiDB cluster

This section describes how to upgrade the TiDB cluster and verify the version after the upgrade.

### Upgrade the TiDB cluster to a specified version

You can upgrade your cluster in one of the two ways: online upgrade and offline upgrade.

By default, TiUP Cluster upgrades the TiDB cluster using the online method, which means that the TiDB cluster can still provide services during the upgrade process. With the online method, the leaders are migrated one by one on each node before the upgrade and restart. Therefore, for a large-scale cluster, it takes a long time to complete the entire upgrade operation.

If your application has a maintenance window for the database to be stopped for maintenance, you can use the offline upgrade method to quickly perform the upgrade operation.

#### Online upgrade

{{< copyable "shell-regular" >}}

```shell
tiup cluster upgrade <cluster-name> <version>
```

For example, if you want to upgrade the cluster to v6.5.0:

{{< copyable "shell-regular" >}}

```shell
tiup cluster upgrade <cluster-name> v6.5.0
```

> **Note:**
>
> + An online upgrade upgrades all components one by one. During the upgrade of TiKV, all leaders in a TiKV instance are evicted before stopping the instance. The default timeout time is 5 minutes (300 seconds). The instance is directly stopped after this timeout time.
>
> + You can use the `--force` parameter to upgrade the cluster immediately without evicting the leader. However, the errors that occur during the upgrade will be ignored, which means that you are not notified of any upgrade failure. Therefore, use the `--force` parameter with caution.
>
> + To keep a stable performance, make sure that all leaders in a TiKV instance are evicted before stopping the instance. You can set `--transfer-timeout` to a larger value, for example, `--transfer-timeout 3600` (unit: second).
>
> + To upgrade TiFlash from versions earlier than 5.3 to 5.3 or later, you should stop TiFlash and then upgrade it. The following steps help you upgrade TiFlash without interrupting other components:
>    1. Stop the TiFlash instance: `tiup cluster stop <cluster-name> -R tiflash`
>    2. Upgrade the TiDB cluster without restarting it (only updating the files): `tiup cluster upgrade <cluster-name> <version> --offline`, such as `tiup cluster upgrade <cluster-name> v6.3.0 --offline`
>    3. Reload the TiDB cluster: `tiup cluster reload <cluster-name>`. After the reload, the TiFlash instance is started and you do not need to manually start it.
>
> + Try to avoid creating a new clustered index table when you apply rolling updates to the clusters using TiDB Binlog.

#### Offline upgrade

1. Before the offline upgrade, you first need to stop the entire cluster.

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster stop <cluster-name>
    ```

2. Use the `upgrade` command with the `--offline` option to perform the offline upgrade. Fill in the name of your cluster for `<cluster-name>` and the version to upgrade to for `<version>`, such as `v6.5.0`.

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
Cluster version:    v6.5.0
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

You can specify `--force`. Then the processes of transferring PD leader and evicting TiKV leader are skipped during the upgrade. The cluster is directly restarted to update the version, which has a great impact on the cluster that runs online. In the following command, `<version>` is the version to upgrade to, such as `v6.5.0`.

{{< copyable "shell-regular" >}}

```shell
tiup cluster upgrade <cluster-name> <version> --force
```

### How to update the version of tools such as pd-ctl after upgrading the TiDB cluster?

You can upgrade the tool version by using TiUP to install the `ctl` component of the corresponding version:

{{< copyable "shell-regular" >}}

```shell
tiup install ctl:v6.5.0
```
