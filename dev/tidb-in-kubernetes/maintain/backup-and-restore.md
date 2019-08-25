---
title: Backup and Restore
summary: Learn how to back up and restore the data of TiDB cluster in Kubernetes.
category: how-to
---

# Backup and Restore

This document describes how to back up and restore the data of a TiDB cluster in Kubernetes.

TiDB in Kubernetes supports two kinds of backup strategies:

* [Full backup](#full-backup) (scheduled or ad-hoc): use [`mydumper`](/reference/tools/mydumper.md) to take a logical backup of the TiDB cluster.
* [Incremental backup](#incremental-backup): use [`TiDB-Binlog`](/reference/tidb-binlog-overview.md) to replicate data in the TiDB cluster to another database or take a real-time backup of the data.

Currently, TiDB in Kubernetes only supports automatic [restoration](#restore) for full backup taken by `mydumper`. Restoring the incremental backup data by `TiDB-Binlog` requires manual operations.

## Full backup

Full backup uses `mydumper` to take a logical backup of a TiDB cluster. The backup task creates a PVC ([PersistentVolumeClaim](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims)) to store data.

In the default configuration, the backup uses PV ([Persistent Volume](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistent-volumes)) to store backup data. You can also store the data in [Google Cloud Storage](https://cloud.google.com/storage/) buckets, [Ceph Object Storage](https://ceph.com/ceph-storage/object-storage/) or [Amazon S3](https://aws.amazon.com/s3/) by changing the configuration. In this case, the backup data is temporarily stored in the PV before it is uploaded to object storage. Refer to [TiDB cluster backup configuration](/tidb-in-kubernetes/reference/configuration/backup.md) for all configuration options you have.

You can either set up a scheduled full backup job or take a full backup in an ad-hoc manner.

### Scheduled full backup

Scheduled full backup is a task created alongside the TiDB cluster, and it runs periodically like `crontab`.

To configure a scheduled full backup, modify the `scheduledBackup` section in the `values.yaml` file of the TiDB cluster:

1. Set `scheduledBackup.create` to `true`.
2. Set `scheduledBackup.storageClassName` to the `storageClass` of the PV that stores the backup data.

    > **Note:**
    >
    > You must set the scheduled full backup PV's [reclaim policy](https://kubernetes.io/docs/tasks/administer-cluster/change-pv-reclaim-policy) to `Retain` to keep your backup data safe.

3. Configure `scheduledBackup.schedule` in the [Cron](https://en.wikipedia.org/wiki/Cron) format to define the scheduling.
4. Create a Kubernetes [Secret](https://kubernetes.io/docs/concepts/configuration/secret/) containing the username and password (the user must have the privileges to back up the data). Meanwhile, set `scheduledBackup.secretName` to the name of the created `Secret`(default to `backup-secret`):

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl create secret generic backup-secret -n <namespace> --from-literal=user=<user> --from-literal=password=<password>
    ```

5. Create a new TiDB cluster with the scheduled full backup task by running `helm install`, or enable the scheduled full backup for the existing cluster by `helm upgrade`:

    {{< copyable "shell-regular" >}}

    ```shell
    helm upgrade <release_name> pingcap/tidb-cluster -f values.yaml --version=<tidb-operator-version>
    ```

### Ad-hoc full backup

Ad-hoc full backup is encapsulated in a helm chart - `pingcap/tidb-backup`. According to the `mode` configuration in the `values.yaml` file, this chart can perform either full backup or data restoration. The [restore section](#restore) covers how to restore the backup data.

Follow the steps below to perform an ad-hoc full backup task:

1. Modify the `values.yaml` file:
    * Set `clusterName` to the target TiDB cluster name.
    * Set `mode` to `backup`.
    * Set `storage.className` to the `storageClass` of the PV that stores the backup data.
    * Adjust the `storage.size` according to your database size.

    > **Note:**
    >
    > You must set the ad-hoc full backup PV's [reclaim policy](https://kubernetes.io/docs/tasks/administer-cluster/change-pv-reclaim-policy) to `Retain` to keep your backup data safe.

2. Create a Kubernetes [Secret](https://kubernetes.io/docs/concepts/configuration/secret/) containing the username and password (the user must have the privileges to back up the data). Meanwhile, set `secretName` in the `values.yaml` file to the name of the created `Secret`(default to `backup-secret`):

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl create secret generic backup-secret -n <namespace> --from-literal=user=<user> --from-literal=password=<password>
    ```

3. Run the following command to perform an ad-hoc backup task:

    {{< copyable "shell-regular" >}}

    ```shell
    helm install pingcap/tidb-backup --name=<backup-name> --namespace=<namespace> -f values.yaml --version=<tidb-operator-version>
    ```

### View backups

For backups stored in PV, you can view them by using the following command:

{{< copyable "shell-regular" >}}

```shell
kubectl get pvc -n <namespace> -l app.kubernetes.io/component=backup,pingcap.com/backup-cluster-name=<cluster-name>
```

If you store your backup data in [Google Cloud Storage](https://cloud.google.com/storage/), [Ceph Object Storage](https://ceph.com/ceph-storage/object-storage/) or [Amazon S3](https://aws.amazon.com/s3/), you can view the backups by using the GUI or CLI tools provided by these storage providers.

## Restore

The `pingcap/tidb-backup` helm chart helps restore a TiDB cluster using backup data. Follow the steps below to restore:

1. Modify the `values.yaml` file:
    * Set `clusterName` to the target TiDB cluster name.
    * Set `mode` to `restore`.
    * Set `name` to the name of the backup you want to restore (refer to [view backups](#view-backups) to view available backups). If the backup is stored in [Google Cloud Storage](https://cloud.google.com/storage/), [Ceph Object Storage](https://ceph.com/ceph-storage/object-storage/) or [Amazon S3](https://aws.amazon.com/s3/), you must configure the corresponding sections and make sure that the same configurations are applied as you perform the [full backup](#full-backup).
2. Create a Kubernetes [Secret](https://kubernetes.io/docs/concepts/configuration/secret/) containing the user and password (the user must have the privileges to back up the data). Meanwhile, set `secretName` in the `values.yaml` file to the name of the created `Secret` (default to `backup-secret`; skip this if you have already created one when you perform [full backup](#full-backup)):

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl create secret generic backup-secret -n <namespace> --from-literal=user=<user> --from-literal=password=<password>
    ```

3. Restore the backup:

    {{< copyable "shell-regular" >}}

    ```shell
    helm install pingcap/tidb-backup --namespace=<namespace> --name=<restore-name> -f values.yaml --version=<tidb-operator-version>
    ```

## Incremental backup

Incremental backup uses [TiDB Binlog](/reference/tidb-binlog-overview.md) to collect binlog data from TiDB and provide real-time backup and replication to downstream platforms.

For the detailed guide of maintaining TiDB Binlog in Kubernetes, refer to [TiDB Binlog](/tidb-in-kubernetes/maintain/tidb-binlog.md).
