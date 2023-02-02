---
title: Backup Storages
summary: Describes the storage URL format used in TiDB backup and restore.
aliases: ['/docs/dev/br/backup-and-restore-storages/','/tidb/dev/backup-storage-S3/','/tidb/dev/backup-storage-azblob/','/tidb/dev/backup-storage-gcs/','/tidb/dev/external-storage/']
---

# Backup Storages

TiDB supports storing backup data to Amazon S3, Google Cloud Storage (GCS), Azure Blob Storage, and NFS. Specifically, you can specify the URL of backup storage in the `--storage` or `-s` parameter of `br` commands. This document introduces the [URL format](#url-format) and [authentication](#authentication) of different external storage services, and [server-side encryption](#server-side-encryption).

## URL format

### URL format description

This section describes the URL format of the storage services:

```shell
[scheme]://[host]/[path]?[parameters]
```

<SimpleTab groupId="storage">
<div label="Amazon S3" value="amazon">

- `scheme`: `s3`
- `host`: `bucket name`
- `parameters`:

    - `access-key`: Specifies the access key.
    - `secret-access-key`: Specifies the secret access key.
    - `use-accelerate-endpoint`: Specifies whether to use the accelerate endpoint on Amazon S3 (defaults to `false`).
    - `endpoint`: Specifies the URL of custom endpoint for S3-compatible services (for example, `<https://s3.example.com/>`).
    - `force-path-style`: Use path style access rather than virtual hosted style access (defaults to `true`).
    - `storage-class`: Specifies the storage class of the uploaded objects (for example, `STANDARD` or `STANDARD_IA`).
    - `sse`: Specifies the server-side encryption algorithm used to encrypt the uploaded objects (value options: ``, `AES256`, or `aws:kms`).
    - `sse-kms-key-id`: Specifies the KMS ID if `sse` is set to `aws:kms`.
    - `acl`: Specifies the canned ACL of the uploaded objects (for example, `private` or `authenticated-read`).

</div>
<div label="GCS" value="gcs">

- `scheme`: `gcs` or `gs`
- `host`: `bucket name`
- `parameters`:

    - `credentials-file`: Specifies the path to the credentials JSON file on the migration tool node.
    - `storage-class`: Specifies the storage class of the uploaded objects (for example, `STANDARD` or `COLDLINE`)
    - `predefined-acl`: Specifies the predefined ACL of the uploaded objects (for example, `private` or `project-private`)

</div>
<div label="Azure Blob Storage" value="azure">

- `scheme`: `azure` or `azblob`
- `host`: `container name`
- `parameters`:

    - `account-name`: Specifies the account name of the storage.
    - `account-key`: Specifies the access key.
    - `access-tier`: Specifies the access tier of the uploaded objects, for example, `Hot`, `Cool`, or `Archive`. The value is `Hot` by default.

</div>
</SimpleTab>

### URL examples

This section provides some URL examples by using `external` as the `host` parameter (`bucket name` or `container name` in the preceding sections).

<SimpleTab groupId="storage">
<div label="Amazon S3" value="amazon">

**Back up snapshot data to Amazon S3**

```shell
./br restore full -u "${PD_IP}:2379" \
--storage "s3://external/backup-20220915?access-key=${access-key}&secret-access-key=${secret-access-key}"
```

**Restore snapshot data from Amazon S3**

```shell
./br restore full -u "${PD_IP}:2379" \
--storage "s3://external/backup-20220915?access-key=${access-key}&secret-access-key=${secret-access-key}"
```

</div>
<div label="GCS" value="gcs">

**Back up snapshot data to GCS**

```shell
./br backup full --pd "${PD_IP}:2379" \
--storage "gcs://external/backup-20220915?credentials-file=${credentials-file-path}"
```

**Restore snapshot data from GCS**

```shell
./br restore full --pd "${PD_IP}:2379" \
--storage "gcs://external/backup-20220915?credentials-file=${credentials-file-path}"
```

</div>
<div label="Azure Blob Storage" value="azure">

**Back up snapshot data to Azure Blob Storage**

```shell
./br backup full -u "${PD_IP}:2379" \
--storage "azure://external/backup-20220915?account-name=${account-name}&account-key=${account-key}"
```

**Restore the `test` database from snapshot backup data in Azure Blob Storage**

```shell
./br restore db --db test -u "${PD_IP}:2379" \
--storage "azure://external/backup-20220915account-name=${account-name}&account-key=${account-key}"
```

</div>
</SimpleTab>

## Authentication

When storing backup data in a cloud storage system, you need to configure authentication parameters depending on the specific cloud service provider. This section describes the authentication methods used by Amazon S3, GCS, and Azure Blob Storage, and how to configure the accounts used to access the corresponding storage service.

<SimpleTab groupId="storage">
<div label="Amazon S3" value="amazon">

Before backup, configure the following privileges to access the backup directory on S3.

- Minimum privileges for TiKV and Backup & Restore (BR) to access the backup directories during backup: `s3:ListBucket`, `s3:PutObject`, and `s3:AbortMultipartUpload`
- Minimum privileges for TiKV and BR to access the backup directories during restore: `s3:ListBucket` and `s3:GetObject`

If you have not yet created a backup directory, refer to [Create a bucket](https://docs.aws.amazon.com/AmazonS3/latest/userguide/create-bucket-overview.html) to create an S3 bucket in the specified region. If necessary, you can also create a folder in the bucket by referring to [Create a folder](https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-folders.html).

It is recommended that you configure access to S3 using either of the following ways:

- Method 1: Specify the access key

    If you specify an access key and a secret access key in the URL, authentication is performed using the specified access key and secret access key. Besides specifying the key in the URL, the following methods are also supported:

    - BR reads the environment variables `$AWS_ACCESS_KEY_ID` and `$AWS_SECRET_ACCESS_KEY`.
    - BR reads the environment variables `$AWS_ACCESS_KEY` and `$AWS_SECRET_KEY`.
    - BR reads the shared credentials file in the path specified by the environment variable `$AWS_SHARED_CREDENTIALS_FILE`.
    - BR reads the shared credentials file in the `~/.aws/credentials` path.

- Method 2: Access based on the IAM role

    Associate an IAM role that can access S3 with EC2 instances where the TiKV and BR nodes run. After the association, BR can directly access the backup directories in S3 without additional settings.

    ```shell
    br backup full --pd "${PD_IP}:2379" \
    --storage "s3://${host}/${path}"
    ```

</div>
<div label="GCS" value="gcs">

You can configure the account used to access GCS by specifying the access key. If you specify the `credentials-file` parameter, the authentication is performed using the specified `credentials-file`. Besides specifying the key in the URL, the following methods are also supported:

- BR reads the file in the path specified by the environment variable `$GOOGLE_APPLICATION_CREDENTIALS`
- BR reads the file `~/.config/gcloud/application_default_credentials.json`.
- BR obtains the credentials from the metadata server when the cluster is running in GCE or GAE.

</div>
<div label="Azure Blob Storage" value="azure">

- Method 1: Specify the access key

    If you specify `account-name` and `account-key` in the URL, the authentication is performed using the specified access key and secret access key. Besides the method of specifying the key in the URL, BR can also read the key from the environment variable `$AZURE_STORAGE_KEY`.

- Method 2: Use Azure AD for backup and restore

    Configure the environment variables `$AZURE_CLIENT_ID`, `$AZURE_TENANT_ID`, and `$AZURE_CLIENT_SECRET` on the node where BR is running.

    - When the cluster is started using TiUP, TiKV uses the systemd service. The following example shows how to configure the preceding three environment variables for TiKV:

        > **Note:**
        >
        > If this method is used, you need to restart TiKV in step 3. If your cluster cannot be restarted, use **Method 1: Specify the access key** for backup and restore.

        1. Suppose that the TiKV port on this node is `24000`, that is, the name of the systemd service is `tikv-24000`:

            ```shell
            systemctl edit tikv-24000
            ```

        2. Edit the TiKV configuration file to configure the three environment variables:

            ```
            [Service]
            Environment="AZURE_CLIENT_ID=aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
            Environment="AZURE_TENANT_ID=aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
            Environment="AZURE_CLIENT_SECRET=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
            ```

        3. Reload the configuration and restart TiKV:

            ```shell
            systemctl daemon-reload
            systemctl restart tikv-24000
            ```

    - To configure the Azure AD information for TiKV and BR started with command lines, you only need to check whether the environment variables `$AZURE_CLIENT_ID`, `$AZURE_TENANT_ID`, and `$AZURE_CLIENT_SECRET` are configured in the operating environment by running the following commands:

        ```shell
        echo $AZURE_CLIENT_ID
        echo $AZURE_TENANT_ID
        echo $AZURE_CLIENT_SECRET
        ```

    - Use BR to back up data to Azure Blob Storage:

        ```shell
        ./br backup full -u "${PD_IP}:2379" \
        --storage "azure://external/backup-20220915?account-name=${account-name}"
        ```

</div>
</SimpleTab>

## Server-side encryption

### Amazon S3 server-side encryption

BR supports server-side encryption when backing up data to Amazon S3. You can also use an AWS KMS key you create for S3 server-side encryption using BR. For details, see [BR S3 server-side encryption](/encryption-at-rest.md#br-s3-server-side-encryption).

## Other features supported by the storage service

BR v6.3.0 supports AWS [S3 Object Lock](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html). You can enable this feature to prevent backup data from being tampered with or deleted.
