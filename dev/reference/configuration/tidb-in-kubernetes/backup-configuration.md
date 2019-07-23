---
title: The Backup Configuration of TiDB in Kubernetetes
summary: Learn the backup configurations of TiDB in Kubernetetes.
category: reference
---

# The Backup Configuration of TiDB in Kubernetetes

`tidb-backup` is a helm chart used for backing up and restoring TiDB clusters in Kubernetes. This document describes the configuration of `tidb-backup`.

## Configuration

### `mode`

- The operating mode
- Default: "backup"
- Options: `backup` (for backing up the data of a cluster) or `restore` (for restoring the data of a cluster)

### `clusterName`

- The name of the target cluster
- Default: "demo"
- The name of the TiDB cluster from which data is backed up or to which data is restored

### `name`

- The name of the backup
- Default: "fullbackup-{{ date "200601021504" .Release.Time }}". `date` is the starting time of the backup, which is accurate to minute.

### `secretName`

- The name of the `Secret` which stores the credential of the target cluster. See [Kubernetes Secret](https://kubernetes.io/docs/concepts/configuration/secret/) for reference.
- Default: "backup-secret"
- You can create the `Secret` by running the following command:

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl create secret generic backup-secret -n ${namespace} --from-literal=user=root --from-literal=password=<password>
    ```

### `storage.className`

- The [StorageClass](https://kubernetes.io/docs/concepts/storage/storage-classes/) is used to store backup data.
- Default: "local-storage"
- The backup job needs a Persistent Volume (PV) to store the backup data. You must ensure that `StorageClass` is available in your Kubernetes cluster.

### `storage.size`

- The storage size of the Persistence Volume
- Default: "100Gi"

### `backupOptions`

- The optional parameter specified to [`mydumper`](https://github.com/maxbube/mydumper/blob/master/docs/mydumper_usage.rst#options) used when backing up data
- Default: "--chunk-filesize=100"

### `restoreOptions`

- The optional parameter specified to [`loader`](https://www.pingcap.com/docs-cn/tools/loader/) used when backing up data
- Default: "-t 16"

### `gcp.bucket`

- The name of the GCP bucket used to store backup data
- Default: ""

> **Note:**
>
> Once you set any variable under the `gcp` section, the backup data will be uploaded to Google Cloud Storage, which means that you must keep the configuration intact.

### `gcp.secretName`

- The name of the `Secret` that stores the credential of Google Cloud Storage
- Default: ""
- See [Google Cloud Documentation](https://cloud.google.com/docs/authentication/production#obtaining_and_providing_service_account_credentials_manually) to download the credential file and create the `Secret` by the running following command:

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl create secret generic gcp-backup-secret -n ${namespace} --from-file=./credentials.json
    ```

### `ceph.endpoint`

- The endpoint of the `ceph` object storage
- Default: ""

> **Note:**
>
> Once you set any variable under the `ceph` section, the backup data will be uploaded to the `ceph` object storage, which means that you must keep the configuration intact.

### `ceph.bucket`

- The bucket name of the `ceph` object storage
- Default: ""

### `ceph.secretName`

- The name of the `Secret` that stores the credential of the `ceph` object store
- Default: ""
- You can create the `Secret` by running the following command:

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl create secret generic ceph-backup-secret -n ${namespace} --from-literal=access_key=<access-key> --from-literal=secret_key=<secret-key>
    ```
