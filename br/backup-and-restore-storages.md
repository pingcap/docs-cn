---
title: 外部存储
summary: 了解 BR、TiDB Lightning 和 Dumpling 中所用存储服务的 URL 格式。
aliases: ['/docs-cn/dev/br/backup-and-restore-storages/']
---

# 外部存储

Backup & Restore (BR)、TiDB Lightning 和 Dumpling 皆支持在本地文件系统和 Amazon S3 上读写数据；另外 BR 亦支持 Google Cloud Storage (GCS) 。通过传入不同 URL scheme 到 BR 的 `--storage` (`-s`) 参数、TiDB Lightning 的 `-d` 参数及 Dumpling 中的 `--output` (`-o`) 参数，可以区分不同的存储方式。

## Scheme

TiDB 迁移工具支持以下存储服务：

| 服务 | Scheme | 示例 |
|---------|---------|-------------|
| 本地文件系统（分布在各节点上） | local | `local:///path/to/dest/` |
| Amazon S3 及其他兼容 S3 的服务 | s3 | `s3://bucket-name/prefix/of/dest/` |
| GCS | gcs, gs | `gcs://bucket-name/prefix/of/dest/` |
| 不写入任何存储（仅作为基准测试） | noop | `noop://` |

## URL 参数

S3 和 GCS 等云存储有时需要额外的连接配置，你可以为这类配置指定参数。例如：

* 用 Dumpling 导出数据到 S3

    {{< copyable "shell-regular" >}}

    ```bash
    ./dumpling -u root -h 127.0.0.1 -P 3306 -B mydb -F 256MiB \
        -o 's3://my-bucket/sql-backup?region=us-west-2'
    ```

* 用 TiDB Lightning 从 S3 导入数据

    {{< copyable "shell-regular" >}}

    ```bash
    ./tidb-lightning --tidb-port=4000 --pd-urls=127.0.0.1:2379 --backend=local --sorted-kv-dir=/tmp/sorted-kvs \
        -d 's3://my-bucket/sql-backup?region=us-west-2'
    ```

* 用 TiDB Lightning 从 S3 导入数据（使用路径类型的请求模式）： 

    {{< copyable "shell-regular" >}}

    ```bash
    ./tidb-lightning --tidb-port=4000 --pd-urls=127.0.0.1:2379 --backend=local --sorted-kv-dir=/tmp/sorted-kvs \
        -d 's3://my-bucket/sql-backup?force-path-style=true&endpoint=http://10.154.10.132:8088'
    ```

* 用 BR 备份到 GCS

    {{< copyable "shell-regular" >}}

    ```bash
    ./br backup full -u 127.0.0.1:2379 \
        -s 'gcs://bucket-name/prefix'
    ```

### S3 的 URL 参数

| URL 参数 | 描述 |
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
> 不建议在存储 URL 中直接传递访问密钥和 secret 访问密钥，因为这些密钥是明文记录的。迁移工具尝试按照以下顺序从环境中推断这些密钥：

1. `$AWS_ACCESS_KEY_ID` 和 `$AWS_SECRET_ACCESS_KEY` 环境变量。
2. `$AWS_ACCESS_KEY` 和 `$AWS_SECRET_KEY` 环境变量。
3. 工具节点上的共享凭证文件，路径由 `$AWS_SHARED_CREDENTIALS_FILE` 环境变量指定。
4. 工具节点上的共享凭证文件，路径为 `~/.aws/credentials`。
5. 当前 Amazon EC2 容器的 IAM 角色。
6. 当前 Amazon ECS 任务的 IAM 角色。

### GCS 的 URL 参数

| URL 参数 | 描述 |
|----------:|---------|
| `credentials-file` | 迁移工具节点上的凭证 JSON 文件的路径 |
| `storage-class` | 上传对象的存储类别（例如 `STANDARD`、`COLDLINE`） |
| `predefined-acl` | 上传对象的预定义 ACL（例如 `private`、`project-private`） |

如果没有指定 `credentials-file`，迁移工具尝试按照以下顺序从环境中推断出凭证：

1. 工具节点上位于 `$GOOGLE_APPLICATION_CREDENTIALS` 环境变量所指定路径的文件内容。
2. 工具节点上位于 `~/.config/gcloud/application_default_credentials.json` 的文件内容。
3. 在 GCE 或 GAE 中运行时，从元数据服务器中获取的凭证。

## 命令行参数

除了使用 URL 参数，BR 和 Dumpling 工具亦支持从命令行指定这些配置，例如：

{{< copyable "shell-regular" >}}

```bash
./dumpling -u root -h 127.0.0.1 -P 3306 -B mydb -F 256MiB \
    -o 's3://my-bucket/sql-backup' \
    --s3.region 'us-west-2'
```

如果同时指定了 URL 参数和命令行参数，命令行参数会覆盖 URL 参数。

### S3 的命令行参数

| 命令行参数 | 描述 |
|----------:|------|
| `--s3.region` | Amazon S3 服务区域（默认为 `us-east-1`） |
| `--s3.endpoint` | S3 兼容服务自定义端点的 URL（例如 `https://s3.example.com/`）|
| `--s3.storage-class` | 上传对象的存储类别（例如 `STANDARD`、`STANDARD_IA`） |
| `--s3.sse` | 用于加密上传的服务器端加密算法（可以设置为空，`AES256` 或 `aws:kms`） |
| `--s3.sse-kms-key-id` | 如果 `--s3.sse` 设置为 `aws:kms`，则使用该参数指定 KMS ID |
| `--s3.acl` | 上传对象的 canned ACL（例如，`private`、`authenticated-read`） |
| `--s3.provider` | S3 兼容服务类型（支持 `aws`、`alibaba`、`ceph`、`netease` 或 `other`） |

### GCS 的命令行参数

| 命令行参数 | 描述 |
|----------:|---------|
| `--gcs.credentials-file` | 迁移工具节点上的凭证 JSON 文件的路径 |
| `--gcs.storage-class` | 上传对象的存储类别（例如 `STANDARD`、`COLDLINE`） |
| `--gcs.predefined-acl` | 上传对象的预定义 ACL（例如 `private`、`project-private`） |

## BR 向 TiKV 发送凭证

在默认情况下，使用 S3 和 GCS 存储时，BR 会将凭证发送到每个 TiKV 节点，以减少设置的复杂性。

但是，这个操作不适合云端环境，因为每个节点都有自己的角色和权限。在这种情况下，你需要用 `--send-credentials-to-tikv=false`（或简写为 `-c=0`）来禁止发送凭证：

{{< copyable "shell-regular" >}}

```bash
./br backup full -c=0 -u pd-service:2379 -s 's3://bucket-name/prefix'
```

使用 SQL 进行[备份](/sql-statements/sql-statement-backup.md)[恢复](/sql-statements/sql-statement-restore.md)时，可加上 `SEND_CREDENTIALS_TO_TIKV = FALSE` 选项：

{{< copyable "sql" >}}

```sql
BACKUP DATABASE * TO 's3://bucket-name/prefix' SEND_CREDENTIALS_TO_TIKV = FALSE;
```

此参数不适用于 TiDB Lightning 和 Dumpling，因为目前它们都是单机程序。
