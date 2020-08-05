---
title: BR 存储
summary: 了解 BR 中所用存储服务的 URL 格式。
aliases: ['/docs-cn/stable/br/backup-and-restore-storages/','/docs-cn/v4.0/br/backup-and-restore-storages/']
---

# BR 存储

Backup & Restore (BR) 支持在本地文件系统、Amazon S3 和 Google Cloud Storage (GCS) 上读写数据。通过传入 BR 的 `--storage` 参数中的不同 URL scheme，可以区分不同的存储方式。

## Scheme

BR 支持以下存储服务：

| 服务 | Scheme | 示例 |
|---------|---------|-------------|
| 本地文件系统（分布在各节点上） | local | `local:///path/to/dest/` |
| Amazon S3 及其他兼容 S3 的服务 | s3 | `s3://bucket-name/prefix/of/dest/` |
| GCS | gcs, gs | `gcs://bucket-name/prefix/of/dest/` |
| 不写入任何存储（仅作为基准测试） | noop | `noop://` |

## 参数

S3 和 GCS 等云存储有时需要额外的连接配置，你可以为这类配置指定参数。例如：

{{< copyable "shell-regular" >}}

```shell
./br backup full -u 127.0.0.1:2379 -s 's3://bucket-name/prefix?region=us-west-2'
```

### S3 参数

| 参数 | 描述 |
|----------:|---------|
| `access-key` | 访问密钥 |
| `secret-access-key` | secret 访问密钥 |
| `region` | Amazon S3 服务区域（默认为 `us-east-1`） |
| `use-accelerate-endpoint` | 是否在 Amazon S3 上使用加速端点（默认为 `false`） |
| `endpoint` | S3 兼容服务自定义端点的 URL（例如 `https://s3.example.com/`）|
| `force-path-style` | 使用 path-style，而不是 virtual-hosted style（默认为 `false`） |
| `storage-class` | 上传对象的存储类别（例如 `STANDARD`、`STANDARD_IA`） |
| `sse` | 用于加密上传的服务器端加密算法（可以设置为空，`AES256` 或 `aws:kms`） |
| `sse-kms-key-id` | 如果 `sse` 设置为 `aws:kms`，则使用该参数指定 KMS ID |
| `acl` | 上传对象的 canned ACL（例如，`private`、`authenticated-read`） |

> **注意：**
>
> 不建议在存储 URL 中直接传递访问密钥和 secret 访问密钥，因为这些密钥是明文记录的。BR 尝试按照以下顺序从环境中推断这些密钥：

1. `$AWS_ACCESS_KEY_ID` 和 `$AWS_SECRET_ACCESS_KEY` 环境变量。
2. `$AWS_ACCESS_KEY` 和 `$AWS_SECRET_KEY` 环境变量。
3. BR 节点上的共享凭证文件，路径由 `$AWS_SHARED_CREDENTIALS_FILE` 环境变量指定。
4. BR 节点上的共享凭证文件，路径为 `~/.aws/credentials`。
5. 当前 Amazon EC2 容器的 IAM 角色。
6. 当前 Amazon ECS 任务的 IAM 角色。

### GCS 参数

| 参数 | 描述 |
|----------:|---------|
| `credentials-file` | TiDB 节点上的凭证 JSON 文件的路径 |
| `storage-class` | 上传对象的存储类别（例如 `STANDARD`、`COLDLINE`） |
| `predefined-acl` | 上传对象的预定义 ACL（例如 `private`、`project-private` |

如果没有指定 `credentials-file`，BR 尝试按照以下顺序从环境中推断出凭证：

1. BR 节点上位于 `$GOOGLE_APPLICATION_CREDENTIALS` 环境变量所指定路径的文件内容。
2. BR 节点上位于 `~/.config/gcloud/application_default_credentials.json` 的文件内容。
3. 在 GCE 或 GAE 中运行时，从元数据服务器中获取的凭证。

## 向 TiKV 发送凭证

在默认情况下，使用 S3 和 GCS 存储时，BR 会将凭证发送到每个 TiKV 节点，以减少设置的复杂性。

但是，这个操作不适合云端环境，因为每个节点都有自己的角色和权限。在这种情况下，你需要用 `--send-credentials-to-tikv=false`（或简写为 `-c=0`）来禁止发送凭证：

{{< copyable "shell-regular" >}}

```shell
./br backup full -c=0 -u pd-service:2379 -s 's3://bucket-name/prefix'
```
