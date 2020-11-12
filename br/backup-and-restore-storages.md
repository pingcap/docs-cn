---
title: BR Storages
summary: Describes the storage URL format used in BR.
aliases: ['/docs/dev/br/backup-and-restore-storages/']
---

# BR Storages

BR supports reading and writing data on the local filesystem, as well as on Amazon S3 and Google Cloud Storage. These are distinguished by the URL scheme in the `--storage` parameter passed into BR.

## Schemes

The following services are supported:

| Service | Schemes | Example URL |
|---------|---------|-------------|
| Local filesystem, distributed on every node | local | `local:///path/to/dest/` |
| Amazon S3 and compatible services | s3 | `s3://bucket-name/prefix/of/dest/` |
| Google Cloud Storage (GCS) | gcs, gs | `gcs://bucket-name/prefix/of/dest/` |
| Write to nowhere (for benchmarking only) | noop | `noop://` |

## Parameters

Cloud storages such as S3 and GCS sometimes require additional configuration for connection. You can specify parameters for such configuration. For example:

{{< copyable "shell-regular" >}}

```shell
./br backup full -u 127.0.0.1:2379 -s 's3://bucket-name/prefix?region=us-west-2'
```

### S3 parameters

| Parameter | Description |
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
> It is not recommended to pass in the access key and secret access key directly in the storage URL, because these keys are logged in plain text. BR tries to infer these keys from the environment in the following order:

1. `$AWS_ACCESS_KEY_ID` and `$AWS_SECRET_ACCESS_KEY` environment variables
2. `$AWS_ACCESS_KEY` and `$AWS_SECRET_KEY` environment variables
3. Shared credentials file on the BR node at the path specified by the `$AWS_SHARED_CREDENTIALS_FILE` environment variable
4. Shared credentials file on the BR node at `~/.aws/credentials`
5. Current IAM role of the Amazon EC2 container
6. Current IAM role of the Amazon ECS task

### GCS parameters

| Parameter | Description |
|----------:|---------|
| `credentials-file` | The path to the credentials JSON file on the TiDB node |
| `storage-class` | Storage class of the uploaded objects (for example, `STANDARD`, `COLDLINE`) |
| `predefined-acl` | Predefined ACL of the uploaded objects (for example, `private`, `project-private`) |

When `credentials-file` is not specified, BR will try to infer the credentials from the environment, in the following order:

1. Content of the file on the BR node at the path specified by the `$GOOGLE_APPLICATION_CREDENTIALS` environment variable
2. Content of the file on the BR node at `~/.config/gcloud/application_default_credentials.json`
3. When running in GCE or GAE, the credentials fetched from the metadata server.

## Sending credentials to TiKV

By default, when using S3 and GCS destinations, BR will send the credentials to every TiKV nodes to reduce setup complexity.

However, this is unsuitable on cloud environment, where every node has their own role and permission. In such cases, you need to disable credentials sending with `--send-credentials-to-tikv=false` (or the short form `-c=0`):

{{< copyable "shell-regular" >}}

```shell
./br backup full -c=0 -u pd-service:2379 -s 's3://bucket-name/prefix'
```
