---
title: External Storages
summary: Describes the storage URL format used in BR, TiDB Lightning, and Dumpling.
---

<!--This doc is temporarily removed from TOC because it duplicates with backup-and-restore-storages.md but some descriptions about Lightning and Dumpling should be remained for successful references. Will extract Lightning and Dumpling content and add it to Lightning and Dumpling docs when bandwidth is sufficient.-->

# External Storages

br command-line tool, TiDB Lightning, and Dumpling support reading and writing data on the local file system and on Amazon S3. br command-line tool also supports reading and writing data on the Google Cloud Storage (GCS) and Azure Blob Storage (Azblob). These are distinguished by the URL scheme in the `--storage` (`-s`) parameter passed into br command-line tool, in the `-d` parameter passed into TiDB Lightning, and in the `--output` (`-o`) parameter passed into Dumpling.

## Schemes

The following services are supported:

| Service | Scheme | Example URL |
|---------|---------|-------------|
| Local file system, distributed on every node | local | `local:///path/to/dest/` |
| Amazon S3 and compatible services | s3 | `s3://bucket-name/prefix/of/dest/` |
| Google Cloud Storage (GCS) | gcs, gs | `gcs://bucket-name/prefix/of/dest/` |
| Azure Blob Storage | azure, azblob | `azure://container-name/prefix/of/dest/` |
| Write to nowhere (for benchmarking only) | noop | `noop://` |

## URL parameters

Cloud storages such as S3, GCS and Azblob sometimes require additional configuration for connection. You can specify parameters for such configuration. For example:

+ Use Dumpling to export data to S3:

    ```bash
    ./dumpling -u root -h 127.0.0.1 -P 3306 -B mydb -F 256MiB \
        -o 's3://my-bucket/sql-backup'
    ```

+ Use TiDB Lightning to import data from S3:

    ```bash
    ./tidb-lightning --tidb-port=4000 --pd-urls=127.0.0.1:2379 --backend=local --sorted-kv-dir=/tmp/sorted-kvs \
        -d 's3://my-bucket/sql-backup'
    ```

+ Use TiDB Lightning to import data from S3 (using the path-style request):

    ```bash
    ./tidb-lightning --tidb-port=4000 --pd-urls=127.0.0.1:2379 --backend=local --sorted-kv-dir=/tmp/sorted-kvs \
        -d 's3://my-bucket/sql-backup?force-path-style=true&endpoint=http://10.154.10.132:8088'
    ```

+ Use TiDB Lightning to import data from S3 (access S3 data by using a specific IAM role):

    ```bash
    ./tidb-lightning --tidb-port=4000 --pd-urls=127.0.0.1:2379 --backend=local --sorted-kv-dir=/tmp/sorted-kvs \
        -d 's3://my-bucket/test-data?role-arn=arn:aws:iam::888888888888:role/my-role'
    ```

+ Use br command-line tool to back up data to GCS:

    ```bash
    ./br backup full -u 127.0.0.1:2379 \
        -s 'gcs://bucket-name/prefix'
    ```

+ Use br command-line tool to back up data to Azblob:

    ```bash
    ./br backup full -u 127.0.0.1:2379 \
        -s 'azure://container-name/prefix'
    ```

### S3 URL parameters

| URL parameter | Description |
|:----------|:---------|
| `access-key` | The access key |
| `secret-access-key` | The secret access key |
| `use-accelerate-endpoint` | Whether to use the accelerate endpoint on Amazon S3 (default to `false`) |
| `endpoint` | URL of custom endpoint for S3-compatible services (for example, `https://s3.example.com/`) |
| `force-path-style` | Use path-style requests rather than virtual-hosted–style requests (default to `true`) |
| `storage-class` | Storage class of the uploaded objects (for example, `STANDARD`, `STANDARD_IA`) |
| `sse` | Server-side encryption algorithm used to encrypt the upload (empty, `AES256` or `aws:kms`) |
| `sse-kms-key-id` | If `sse` is set to `aws:kms`, specifies the KMS ID |
| `acl` | Canned ACL of the uploaded objects (for example, `private`, `authenticated-read`) |
| `role-arn` | When you need to access Amazon S3 data from a third party using a specified [IAM role](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html), you can specify the corresponding [Amazon Resource Name (ARN)](https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html) of the IAM role with the `role-arn` parameter, such as `arn:aws:iam::888888888888:role/my-role`. For more information, see [Providing access to AWS accounts owned by third parties](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_common-scenarios_third-party.html). |
| `external-id` | When you access Amazon S3 data from a third party, you might need to specify a correct [external ID](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-user_externalid.html) to assume [the IAM role](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html). In this case, you can use this `external-id` URL query parameter to specify the external ID. An external ID is an arbitrary string provided by the third party together with the IAM role ARN to access the Amazon S3 data. Providing an external ID is optional when assuming an IAM role, which means if the third party does not specify an external ID for the IAM role, you can assume the role and access the corresponding S3 data without providing this parameter. |

> **Note:**
>
> It is not recommended to pass in the access key and secret access key directly in the storage URL, because these keys are stored as plain text.

If neither the access key and secret access key nor IAM role ARN (`role-arn`) and external ID (`external-id`) are provided, the migration tools searches for these keys from the environment in the following order:

1. `$AWS_ACCESS_KEY_ID` and `$AWS_SECRET_ACCESS_KEY` environment variables
2. `$AWS_ACCESS_KEY` and `$AWS_SECRET_KEY` environment variables
3. Shared credentials file on the tool node at the path specified by the `$AWS_SHARED_CREDENTIALS_FILE` environment variable
4. Shared credentials file on the tool node at `~/.aws/credentials`
5. Current IAM role of the Amazon EC2 container
6. Current IAM role of the Amazon ECS task

### GCS URL parameters

| URL parameter | Description |
|:----------|:---------|
| `credentials-file` | The path to the credentials JSON file on the tool node |
| `storage-class` | Storage class of the uploaded objects (for example, `STANDARD`, `COLDLINE`) |
| `predefined-acl` | Predefined ACL of the uploaded objects (for example, `private`, `project-private`) |

When `credentials-file` is not specified, the migration tool searches for the credentials from the environment in the following order:

1. Content of the file on the tool node at the path specified by the `$GOOGLE_APPLICATION_CREDENTIALS` environment variable
2. Content of the file on the tool node at `~/.config/gcloud/application_default_credentials.json`
3. When running in GCE or GAE, the credentials fetched from the metadata server.

### Azblob URL parameters

| URL parameter | Description |
|:----------|:-----|
| `account-name` | The account name of the storage |
| `account-key` | The access key|
| `access-tier` | Access tier of the uploaded objects (for example, `Hot`, `Cool`, `Archive`). If `access-tier` is not set (the value is empty), the value is `Hot` by default. |

To ensure that TiKV and br use the same storage account, br determines the value of `account-name`. That is, `send-credentials-to-tikv = true` is set by default. br searches for these keys from the environment in the following order:

1. If both `account-name` **and** `account-key` are specified, the key specified by this parameter is used.
2. If `account-key` is not specified, br tries to read the related credentials from environment variables on the br node. br reads `$AZURE_CLIENT_ID`, `$AZURE_TENANT_ID`, and `$AZURE_CLIENT_SECRET` first. At the same time, br allows TiKV to read these three environment variables from the respective nodes and access the variables using Azure AD (Azure Active Directory).
3. If the preceding three environment variables are not configured in the br node, br tries to read `$AZURE_STORAGE_KEY` using an access key.

> **Note:**
>
> - When using Azure Blob Storage as the external storage, you should set `send-credentials-to-tikv = true` (which is set by default). Otherwise, the backup task will fail.
> - `$AZURE_CLIENT_ID`, `$AZURE_TENANT_ID`, and `$AZURE_CLIENT_SECRET` respectively refer to the application ID `client_id`, the tenant ID `tenant_id`, and the client password `client_secret` of the Azure application. For details about how to confirm the presence of the three environment variables, or how to configure the environment variables as parameters, see [Authentication](/br/backup-and-restore-storages.md#authentication).

## Command-line parameters

In addition to the URL parameters, br and Dumpling also support specifying these configurations using command-line parameters. For example:

{{< copyable "shell-regular" >}}

```bash
./dumpling -u root -h 127.0.0.1 -P 3306 -B mydb -F 256MiB \
    -o 's3://my-bucket/sql-backup' \
    --s3.role-arn="arn:aws:iam::888888888888:role/my-role"
```

The preceding command is equivalent to the following:

```bash
./dumpling -u root -h 127.0.0.1 -P 3306 -B mydb -F 256MiB \
     -o 's3://my-bucket/sql-backup&role-arn=arn:aws:iam::888888888888:role/my-role'
```

If you have specified URL parameters and command-line parameters at the same time, the URL parameters are overwritten by the command-line parameters.

### S3 command-line parameters

| Command-line parameter | Description |
|:----------|:------|
| `--s3.endpoint` | The URL of custom endpoint for S3-compatible services (for example, `https://s3.example.com/`) |
| `--s3.storage-class` | The storage class of the upload object (for example, `STANDARD` or `STANDARD_IA`) |
| `--s3.sse` | The server-side encryption algorithm used to encrypt the upload (value options are empty, `AES256` and `aws:kms`) |
| `--s3.sse-kms-key-id` | If `--s3.sse` is configured as `aws:kms`, this parameter is used to specify the KMS ID. |
| `--s3.acl` | The canned ACL of the upload object (for example, `private` or `authenticated-read`) |
| `--s3.provider` | The type of the S3-compatible service (supported types are `aws`, `alibaba`, `ceph`, `netease` and `other`) |
| `--s3.role-arn` | When you need to access Amazon S3 data from a third party using a specified [IAM role](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html), you can specify the corresponding [Amazon Resource Name (ARN)](https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html) of the IAM role with the `--s3.role-arn` option, such as `arn:aws:iam::888888888888:role/my-role`. For more information, see [AWS documentation](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_common-scenarios_third-party.html). |
| `--s3.external-id` | When you access Amazon S3 data from a third party, you might need to specify a correct [external ID](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-user_externalid.html) to assume [the IAM role](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html). In this case, you can use this `--s3.external-id` option to specify the external ID. An external ID is an arbitrary string provided by the third party together with the IAM role ARN to access the Amazon S3 data. Providing an external ID is optional when assuming an IAM role, which means if the third party does not specify an external ID for the IAM role, you can assume the role and access the corresponding S3 data without providing this parameter. |

To export data to non-AWS S3 cloud storage, specify the cloud provider and whether to use `virtual-hosted style`. In the following examples, data is exported to the Alibaba Cloud OSS storage:

+ Export data to Alibaba Cloud OSS using Dumpling:

    {{< copyable "shell-regular" >}}

    ```bash
    ./dumpling -h 127.0.0.1 -P 3306 -B mydb -F 256MiB \
       -o "s3://my-bucket/dumpling/" \
       --s3.endpoint="http://oss-cn-hangzhou-internal.aliyuncs.com" \
       --s3.provider="alibaba" \
       -r 200000 -F 256MiB
    ```

+ Back up data to Alibaba Cloud OSS using br command-line tool:

    {{< copyable "shell-regular" >}}

    ```bash
    ./br backup full --pd "127.0.0.1:2379" \
        --storage "s3://my-bucket/full/" \
        --s3.endpoint="http://oss-cn-hangzhou-internal.aliyuncs.com" \
        --s3.provider="alibaba" \
        --send-credentials-to-tikv=true \
        --ratelimit 128 \
        --log-file backuptable.log
    ```

+ Export data to Alibaba Cloud OSS using TiDB Lightning. You need to specify the following content in the YAML configuration file:

    {{< copyable "" >}}

    ```
    [mydumper]
    data-source-dir = "s3://my-bucket/dumpling/?endpoint=http://oss-cn-hangzhou-internal.aliyuncs.com&provider=alibaba"
    ```

### GCS command-line parameters

| Command-line parameter | Description |
|:----------|:------|
| `--gcs.credentials-file` | The path to the credentials JSON file on the tool node |
| `--gcs.storage-class` | The storage class of the upload objects (for example, `STANDARD` or `COLDLINE`)  |
| `--gcs.predefined-acl` | Predefined ACL of the uploaded objects (for example, `private` or `project-private`) |

### Azblob command-line parameters

| Command-line parameter | Description |
|:----------|:------|
| `--azblob.account-name` | The account name of the storage |
| `--azblob.account-key` | The access key |
| `--azblob.access-tier` | Access tier of the uploaded objects (for example, `Hot`, `Cool`, `Archive`). If `access-tier` is not set (the value is empty), the value is `Hot` by default. |

## br command-line tool sending credentials to TiKV

By default, when using S3, GCS, or Azblob destinations, br command-line tool will send the credentials to every TiKV node to reduce setup complexity.

However, this is unsuitable on cloud environment, where every node has their own role and permission. In such cases, you need to disable credentials sending with `--send-credentials-to-tikv=false` (or the short form `-c=0`):

{{< copyable "shell-regular" >}}

```bash
./br backup full -c=0 -u pd-service:2379 -s 's3://bucket-name/prefix'
```

When using SQL statements to [back up](/sql-statements/sql-statement-backup.md) and [restore](/sql-statements/sql-statement-restore.md) data, you can add the `SEND_CREDENTIALS_TO_TIKV = FALSE` option:

{{< copyable "sql" >}}

```sql
BACKUP DATABASE * TO 's3://bucket-name/prefix' SEND_CREDENTIALS_TO_TIKV = FALSE;
```

This option is not supported in TiDB Lightning and Dumpling, because they are currently standalone.
