---
title: External Storages
summary: Describes the storage URL format used in BR, TiDB Lightning, and Dumpling.
aliases: ['/docs/dev/br/backup-and-restore-storages/']
---

# External Storages

Backup & Restore (BR), TiDB Lighting, and Dumpling support reading and writing data on the local filesystem and on Amazon S3. BR also supports reading and writing data on the Google Cloud Storage (GCS). These are distinguished by the URL scheme in the `--storage` parameter passed into BR, in the `-d` parameter passed into TiDB Lightning, and in the `--output` (`-o`) parameter passed into Dumpling.

## Schemes

The following services are supported:

| Service | Schemes | Example URL |
|---------|---------|-------------|
| Local filesystem, distributed on every node | local | `local:///path/to/dest/` |
| Amazon S3 and compatible services | s3 | `s3://bucket-name/prefix/of/dest/` |
| Google Cloud Storage (GCS) | gcs, gs | `gcs://bucket-name/prefix/of/dest/` |
| Write to nowhere (for benchmarking only) | noop | `noop://` |

## URL parameters

Cloud storages such as S3 and GCS sometimes require additional configuration for connection. You can specify parameters for such configuration. For example:

+ Use Dumpling to export data to S3:

    {{< copyable "shell-regular" >}}

    ```bash
    ./dumpling -u root -h 127.0.0.1 -P 3306 -B mydb -F 256MiB \
        -o 's3://my-bucket/sql-backup?region=us-west-2'
    ```

+ Use TiDB Lightning to import data from S3:

    {{< copyable "shell-regular" >}}

    ```bash
    ./tidb-lightning --tidb-port=4000 --pd-urls=127.0.0.1:2379 --backend=local --sorted-kv-dir=/tmp/sorted-kvs \
        -d 's3://my-bucket/sql-backup?region=us-west-2'
    ```

+ Use TiDB Lightning to import data from S3 (using the path style in the request mode):

    {{< copyable "shell-regular" >}}

    ```bash
    ./tidb-lightning --tidb-port=4000 --pd-urls=127.0.0.1:2379 --backend=local --sorted-kv-dir=/tmp/sorted-kvs \
        -d 's3://my-bucket/sql-backup?force-path-style=true&endpoint=http://10.154.10.132:8088'
    ```

+ Use BR to back up data to GCS:

    {{< copyable "shell-regular" >}}

    ```bash
    ./br backup full -u 127.0.0.1:2379 \
        -s 'gcs://bucket-name/prefix'
    ```

### S3 URL parameters

| URL parameter | Description |
|----------:|---------|
| `access-key` | The access key |
| `secret-access-key` | The secret access key |
| `region` | Service Region for Amazon S3 (default to `us-east-1`) |
| `use-accelerate-endpoint` | Whether to use the accelerate endpoint on Amazon S3 (default to `false`) |
| `endpoint` | URL of custom endpoint for S3-compatible services (for example, `https://s3.example.com/`) |
| `force-path-style` | Use path style access rather than virtual hosted style access (default to `false`) |
| `storage-class` | Storage class of the uploaded objects (for example, `STANDARD`, `STANDARD_IA`) |
| `sse` | Server-side encryption algorithm used to encrypt the upload (empty, `AES256` or `aws:kms`) |
| `sse-kms-key-id` | If `sse` is set to `aws:kms`, specifies the KMS ID |
| `acl` | Canned ACL of the uploaded objects (for example, `private`, `authenticated-read`) |

> **Note:**
>
> It is not recommended to pass in the access key and secret access key directly in the storage URL, because these keys are logged in plain text. The migration tools try to infer these keys from the environment in the following order:

1. `$AWS_ACCESS_KEY_ID` and `$AWS_SECRET_ACCESS_KEY` environment variables
2. `$AWS_ACCESS_KEY` and `$AWS_SECRET_KEY` environment variables
3. Shared credentials file on the tool node at the path specified by the `$AWS_SHARED_CREDENTIALS_FILE` environment variable
4. Shared credentials file on the tool node at `~/.aws/credentials`
5. Current IAM role of the Amazon EC2 container
6. Current IAM role of the Amazon ECS task

### GCS URL parameters

| URL parameter | Description |
|----------:|---------|
| `credentials-file` | The path to the credentials JSON file on the tool node |
| `storage-class` | Storage class of the uploaded objects (for example, `STANDARD`, `COLDLINE`) |
| `predefined-acl` | Predefined ACL of the uploaded objects (for example, `private`, `project-private`) |

When `credentials-file` is not specified, the migration tool will try to infer the credentials from the environment, in the following order:

1. Content of the file on the tool node at the path specified by the `$GOOGLE_APPLICATION_CREDENTIALS` environment variable
2. Content of the file on the tool node at `~/.config/gcloud/application_default_credentials.json`
3. When running in GCE or GAE, the credentials fetched from the metadata server.

## Command-line parameters

In addition to the URL parameters, BR and Dumpling also support specifying these configurations using command-line parameters. For example:

{{< copyable "shell-regular" >}}

```bash
./dumpling -u root -h 127.0.0.1 -P 3306 -B mydb -F 256MiB \
    -o 's3://my-bucket/sql-backup' \
    --s3.region 'us-west-2'
```

If you have specified URL parameters and command-line parameters at the same time, the URL parameters are overwritten by the command-line parameters.

### S3 command-line parameters

| Command-line parameter | Description |
|----------:|------|
| `--s3.region` | Amazon S3's service region, which defaults to `us-east-1`. |
| `--s3.endpoint` | The URL of custom endpoint for S3-compatible services. For example, `https://s3.example.com/`. |
| `--s3.storage-class` | The storage class of the upload object. For example, `STANDARD` and `STANDARD_IA`. |
| `--s3.sse` | The server-side encryption algorithm used to encrypt the upload. The value options are empty, `AES256` and `aws:kms`. |
| `--s3.sse-kms-key-id` | If `--s3.sse` is configured as `aws:kms`, this parameter is used to specify the KMS ID. |
| `--s3.acl` | The canned ACL of the upload object. For example, `private` and `authenticated-read`. |
| `--s3.provider` | The type of the S3-compatible service. The supported types are `aws`, `alibaba`, `ceph`, `netease` and `other`. |

### GCS command-line parameters

| Command-line parameter | Description |
|----------:|---------|
| `--gcs.credentials-file` |  The path of the JSON-formatted credential on the tool node. |
| `--gcs.storage-class` | The storage type of the upload object, such as `STANDARD` and `COLDLINE`.  |
| `--gcs.predefined-acl` | The pre-defined ACL of the upload object, such as `private` and `project-private`. |

## BR sending credentials to TiKV

By default, when using S3 and GCS destinations, BR will send the credentials to every TiKV nodes to reduce setup complexity.

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

This option is not supported in TiDB Lightning and Dumpling, because the two applications are currently standalone.
