---
title: Back Up and Restore Data on Google Cloud Storage Using BR
summary: Learn how to use BR to back up and restore data on Google Cloud Storage.
---

# Back Up and Restore Data on Google Cloud Storage Using BR

The Backup & Restore (BR) tool supports using Google Cloud Storage (GCS) as the external storage for backing up and restoring data.

## User scenario

You can quickly back up the data of a TiDB cluster deployed in Google Compute Engine (GCE) to GCS, or quickly restore a TiDB cluster from the backup data in GCS.

## Back up data to GCS

{{< copyable "shell-regular" >}}

```shell
br backup full --pd "${PDIP}:2379" --Storage 'gcs://bucket-name/prefix?credentials-file=${credentials-file-path}' --send-credentials-to-tikv=true
```

When backing up data to GCS, you need to place a credential file in the node where BR is running. The credential file contains the account credentials for accessing GCS. If `--send-credentials-to-tikv` is displayed, it means the account access credentials of GCS will be passed to the TiKV node.

To obtain the credential files, refer to [CREATE AND DOWNLOAD THE GCS CREDENTIALS FILE](https://access.redhat.com/documentation/en-us/red_hat_openstack_platform/13/html/google_cloud_backup_guide/creds).

## Restore data from GCS

{{< copyable "shell-regular" >}}

```shell
br restore full --pd "${PDIP}:2379" --Storage 'gcs://bucket-name/prefix?credentials-file=${credentials-file-path}' --send-credentials-to-tikv=true
```

## See also

To learn other external storages supported by BR, see [External storages](/br/backup-and-restore-storages.md).
