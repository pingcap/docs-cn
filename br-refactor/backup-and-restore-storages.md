---
title: 外部存储
summary: 了解 BR、TiDB Lightning 和 Dumpling 中所用存储服务的 URL 格式。
aliases: ['/docs-cn/dev/br/backup-and-restore-storages/']
---

# 外部存储

TiDB 支持本地文件系统、Amazon S3、Google Cloud Storage (GCS) 和 Azure Blob Storage 作为备份恢复的存储。具体来说，可以在 BR 的 `--storage (-s)` 参数、TiDB Lightning 的 `-d` 参数及 Dumpling 中的 `--output (-o)` 参数传入存储的 URL 来定义存储。

## URL 格式

本部分介绍使用 BR、TiDB Lightning 和 Dumpling 时所用存储服务的 URL 格式：

```shell
[scheme]://[host]/[path]?[parameters]
```

| 存储位置 | Scheme | 主机 | 参数 |
| :--- | :--- | :--- | :--- |
| Amazon | `s3` | `bucket name` | `access-key`：访问密钥 </br> `secret-access-key`：secret 访问密钥 </br> `use-accelerate-endpoint`：是否在 Amazon S3 上使用加速端点（默认为 `false`）</br> `endpoint`：S3 兼容服务自定义端点的 URL（例如 https://s3.example.com/）</br> `force-path-style`：使用 path-style，而不是 virtual-hosted style（默认为 `true`）</br> `storage-class`：上传对象的存储类别（例如 `STANDARD`、`STANDARD_IA`）</br> `sse`：用于加密上传的服务器端加密算法（可以设置为空、`AES256` 或 `aws:kms`）</br> `sse-kms-key-id`：如果 `sse` 设置为 `aws:kms`，则使用该参数指定 KMS ID </br> `acl`：上传对象的 canned ACL（例如，`private`、`authenticated-read`）|
| GCS | `gcs` 或 `gs` | `bucket name` | `credentials-file`：迁移工具节点上的凭证 JSON 文件的路径 </br> `storage-class`：上传对象的存储类别（例如 `STANDARD` 或 `COLDLINE`）</br> `predefined-acl`：上传对象的预定义 ACL（例如 `private` 或 `project-private`） |
| Azure | `azure` 或 `azblob` | `container name` | `account-name`：存储账户名 </br> `account-key`：访问密钥 </br> `access-tier`：上传对象的存储类别（例如 `Hot`、`Cool`、`Archive`）。如果没有设置 `access-tier` 的值（该值为空），此值会默认设置为 `Hot`。 |
| NFS/Local | `local` | N/A | N/A |

> **注意：**
>
> 不建议在存储 URL 中直接传递访问密钥和 secret 访问密钥，因为这些密钥是明文记录的。

### URL 示例

本部分示例以 `bucket name` 或 `container name` 为 `external` 为例进行介绍。

**使用 Dumpling 导出数据到 S3**

```
./dumpling -h ${ip} -P 3306 -u root -t 16 -r 200000 -F 256MiB -B my_db1 -f 'my_db1.table[12]' -o 's3://external/sql-backup'
```

**使用 TiDB Lightning 导入数据到 S3**

```shell
./tidb-lightning --tidb-port=4000 --pd-urls=127.0.0.1:2379 --backend=local --sorted-kv-dir=/tmp/sorted-kvs \
    -d 's3://external/sql-backup'
```

**使用 BR 将数据备份至 Azure Blob Storage**

```shell
.br backup db --db test -u 127.0.0.1:2379 \ -s 'azure://external/t1?account-name=devstoreaccount1&access-tier=Cool'
```

## 命令行格式

本部分介绍使用 BR、TiDB Lightning 和 Dumpling 时所用存储服务的命令行格式：

| 存储位置 | Scheme | 主机 | 参数 |
| :--- | :--- | :--- | :--- |
| Amazon | `s3` | `bucket name` | `--s3.endpoint`：S3 兼容服务自定义端点的 URL（例如 https://s3.example.com/） </br> `--s3.storage-class`：上传对象的存储类别（例如 `STANDARD` 或 `STANDARD_IA`） </br> `--s3.sse`：用于加密上传的服务器端加密算法（可以设置为空、AES256 或 aws:kms） </br> `--s3.sse-kms-key-id`：如果 `--s3.sse` 设置为 `aws:kms`，则使用该参数指定 KMS ID </br> `--s3.acl`：上传对象的 canned ACL（例如，`private` 或 `authenticated-read`） <br> `--s3.provider`：S3 兼容服务类型（支持 `aws`、`alibaba`、`ceph`、`netease` 或 `other`） |
| GCS | `gcs` 或 `gs` | `bucket name` | `--gcs.credentials-file`：迁移工具节点上的凭证 JSON 文件的路径 </br> `--gcs.storage-class`：上传对象的存储类别（例如 `STANDARD` 或 `COLDLINE`） </br> `--gcs.predefined-acl`：上传对象的预定义 ACL（例如 `private` 或 `project-private`） |
| Azure | `azure` 或 `azblob` | `container name` | `--azblob.account-name`：存储账户名 </br> `--azblob.account-key`：访问密钥 </br> `--azblob.access-tier`：上传对象的存储类别（例如 `Hot`、`Cool` 或 `Archive`）。如果没有设置 `access-tier` 的值（该值为空），此值会默认设置为 `Hot`。 |

### 命令行示例

## 鉴权

将数据存储到 cloud 存储系统时，根据 cloud 供应商的不同，需要设置不同的鉴权参数。本部分介绍使用 Amazon S3、GCS 及 Azure storage 时所用存储服务的鉴权方式。

<SimpleTab>
<div label="Amazon S3">

**指定访问**

如果指定访问密钥和 secret 访问密钥，将按照指定的访问密钥和 secret 访问密钥进行鉴权。

**未指定访问**

如果没有指定访问密钥和 secret 访问密钥，迁移工具尝试按照以下顺序从环境中推断这些密钥：

1. `$AWS_ACCESS_KEY_ID` 和 `$AWS_SECRET_ACCESS_KEY` 环境变量
2. `$AWS_ACCESS_KEY` 和 `$AWS_SECRET_KEY` 环境变量
3. 工具节点上的共享凭证文件，路径由 `$AWS_SHARED_CREDENTIALS_FILE` 环境变量指定
4. 工具节点上的共享凭证文件，路径为 `~/.aws/credentials`
5. 当前 Amazon EC2 容器的 IAM 角色
6. 当前 Amazon ECS 任务的 IAM 角色

</div>
<div label="GCS">

**指定访问**

如果指定了 `credentials-file` 参数，将按照指定的 `credentials-file` 进行鉴权。

**未指定访问**

如果没有指定 `credentials-file`，迁移工具尝试按照以下顺序从环境中推断出凭证：

1. 工具节点上位于 `$GOOGLE_APPLICATION_CREDENTIALS` 环境变量所指定路径的文件内容
2. 工具节点上位于 `~/.config/gcloud/application_default_credentials.json` 的文件内容
3. 在 GCE 或 GAE 中运行时，从元数据服务器中获取的凭证

</div>
<div label="Azure storage">

为了保证 TiKV 和迁移工具使用了同一个存储账户，`account-name` 会由迁移工具决定（即默认 `send-credentials-to-tikv = true`）。

**指定访问**

如果已指定 `account-name` 和 `account-key`，则使用该参数指定的密钥。

**未指定访问**

如果没有指定 `account-key`，则尝试从工具节点上的环境变量读取相关凭证。迁移工具会优先读取 `$AZURE_CLIENT_ID`、`$AZURE_TENANT_ID` 和 `$AZURE_CLIENT_SECRET`。与此同时，工具会允许 TiKV 从各自节点上读取上述三个环境变量，采用 Azure AD (Azure Active Directory) 访问。

如果上述三个环境变量不存在于工具节点中，则尝试读取 `$AZURE_STORAGE_KEY`，采用密钥访问。

</div>
</SimpleTab>
