---
title: Restore Data into TiDB in Kubernetes
summary: Learn how to quickly restore data into a TiDB cluster in Kubernetes with TiDB Lightning.
category: how-to
---

# Restore Data into TiDB in Kubernetes

This document describes how to restore data into a TiDB cluster in Kubernetes using [TiDB Lightning](https://github.com/pingcap/tidb-lightning).

TiDB Lightning contains two components: tidb-lightning and tikv-importer. In Kubernetes, the tikv-importer is inside the Helm chart of the TiDB cluster. And tikv-importer is deployed as a `StatefulSet` with `replicas=1` while tidb-lightning is in a separate Helm chart and deployed as a `Job`.

Therefore, both the tikv-importer and tidb-lightning need to be deployed to restore data with TiDB Lightning.

## Deploy tikv-importer

The tikv-importer can be enabled for an existing TiDB cluster or for a newly created one.

* Create a new TiDB cluster with tikv-importer enabled

    1. Set `importer.create` to `true` in tidb-cluster `values.yaml`

    2. Deploy the cluster

        {{< copyable "shell-regular" >}}

        ```shell
        helm install pingcap/tidb-cluster --name=<tidb-cluster-release-name> --namespace=<namespace> -f values.yaml --version=<chart-version>
        ```

* Configure an existing TiDB cluster to enable tikv-importer

    1. Set `importer.create` to `true` in the `values.yaml` file of the TiDB cluster

    2. Upgrade the existing TiDB cluster

        {{< copyable "shell-regular" >}}

        ```shell
        helm upgrade <tidb-cluster-release-name> pingcap/tidb-cluster -f values.yaml --version=<chart-version>
        ```

## Deploy tidb-lightning

1. Configure TiDB Lightning

    Use the following command to get the default configuration of TiDB Lightning.

    {{< copyable "shell-regular" >}}

    ```shell
    helm inspect values pingcap/tidb-lightning --version=<chart-version> > tidb-lightning-values.yaml
    ```

    TiDB Lightning Helm chart supports both local and remote data source.

    * Local

        Local mode requires the Mydumper backup data to be on one of the Kubernetes node. This mode can be enabled by setting `dataSource.local.nodeName` to the node name and `dataSource.local.hostPath` to the Mydumper backup data directory path which contains a file named `metadata`.

    * Remote

        Unlike local mode, remote mode needs to use [rclone](https://rclone.org) to download Mydumper backup tarball file from a network storage to a PV. Any cloud storage supported by rclone should work, but currently only the following have been tested: [Google Cloud Storage (GCS)](https://cloud.google.com/storage/), [AWS S3](https://aws.amazon.com/s3/), [Ceph Object Storage](https://ceph.com/ceph-storage/object-storage/).

        1. Make sure that `dataSource.local.nodeName` and `dataSource.local.hostPath` are commented out.

        2. Create a `Secret` containing the rclone configuration. A sample configuration is listed below. Only one cloud storage configuration is required. For other cloud storages, please refer to [rclone documentation](https://rclone.org/).

            {{< copyable "" >}}

            ```yaml
            apiVersion: v1
            kind: Secret
            metadata:
              name: cloud-storage-secret
            type: Opaque
            stringData:
              rclone.conf: |
              [s3]
              type = s3
              provider = AWS
              env_auth = false
              access_key_id = <my-access-key>
              secret_access_key = <my-secret-key>
              region = us-east-1

              [ceph]
              type = s3
              provider = Ceph
              env_auth = false
              access_key_id = <my-access-key>
              secret_access_key = <my-secret-key>
              endpoint = <ceph-object-store-endpoint>
              region = :default-placement

              [gcs]
              type = google cloud storage
              # The service account must include Storage Object Viewer role
              # The content can be retrieved by `cat <service-account-file.json> | jq -c .`
              service_account_credentials = <service-account-json-file-content>
            ```

            Fill in the placeholders with your configurations and save it as `secret.yaml`, and then create the secret via `kubectl apply -f secret.yaml -n <namespace>`.

        3. Configure the `dataSource.remote.storageClassName` to an existing storage class in the Kubernetes cluster.

2. Deploy TiDB Lightning

    {{< copyable "shell-regular" >}}

    ```shell
    helm install pingcap/tidb-lightning --name=<tidb-lightning-release-name> --namespace=<namespace> --set failFast=true -f tidb-lightning-values.yaml --version=<chart-version>
    ```

When TiDB Lightning fails to restore data, it cannot simply be restarted, but manual intervention is required. So the tidb-lightning's `Job` restart policy is set to `Never`.

> **Note:**
>
> Currently, TiDB Lightning will [exit with non-zero error code even when data is successfully restored](https://github.com/pingcap/tidb-lightning/pull/230). This will trigger the job failure. Therefore, the success status needs to be determined by viewing tidb-lightning pod's log.

If the lightning fails to restore data, follow the steps below to do manual intervention:

1. Delete the lightning job by running `kubectl delete job -n <namespace> <tidb-lightning-release-name>-tidb-lightning`.

2. Create the lightning job again with `failFast` disabled by `helm template pingcap/tidb-lightning --name <tidb-lightning-release-name> --set failFast=false -f tidb-lightning-values.yaml | kubectl apply -n <namespace> -f -`.

3. When the lightning pod is running again, use `kubectl exec -it -n <namesapce> <tidb-lightning-pod-name> sh` to `exec` into the lightning container.

4. Get the startup script by running `cat /proc/1/cmdline`.

5. Diagnose the lightning following the [troubleshooting guide](/v3.0/how-to/troubleshoot/tidb-lightning.md#tidb-lightning-troubleshooting).

## Destroy TiDB Lightning

Currently, TiDB Lightning can only restore data offline. When the restoration finishes and the TiDB cluster needs to provide service for applications, the TiDB Lightning should be deleted to save cost.

* To delete tikv-importer:
    1. In `values.yaml` of the TiDB cluster chart, set `importer.create` to `false`.
    2. Run `helm upgrade <tidb-cluster-release-name> pingcap/tidb-cluster -f values.yaml`.

* To delete tidb-lightning, run `helm delete <tidb-lightning-release-name> --purge`.
