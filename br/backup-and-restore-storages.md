---
title: 备份存储
summary: 了解 BR 支持的备份存储和使用方式。
---

# 备份存储

TiDB 支持 Amazon S3、Google Cloud Storage (GCS) 、Azure Blob Storage 和 NFS 作为备份恢复的存储。具体来说，可以在 BR 的 `--storage (-s)` 参数传入存储的 URL 来定义备份存储。

## URL 格式

本部分介绍存储服务的 URL 格式：

```shell
[scheme]://[host]/[path]?[parameters]
```

| 存储类型 | scheme | host | parameters |
| :--- | :--- | :--- | :--- |
| Amazon | `s3` | `bucket name` | `access-key`：访问密钥 </br> `secret-access-key`：secret 访问密钥 </br> `use-accelerate-endpoint`：是否在 Amazon S3 上使用加速端点（默认为 `false`）</br> `endpoint`：S3 兼容服务自定义端点的 URL（例如 `<https://s3.example.com/>`）</br> `force-path-style`：使用 path-style，而不是 virtual-hosted style（默认为 `true`）</br> `storage-class`：上传对象的存储类别（例如 `STANDARD`、`STANDARD_IA`）</br> `sse`：用于加密上传的服务器端加密算法（可以设置为空、`AES256` 或 `aws:kms`）</br> `sse-kms-key-id`：如果 `sse` 设置为 `aws:kms`，则使用该参数指定 KMS ID </br> `acl`：上传对象的 canned ACL（例如，`private`、`authenticated-read`）|
| GCS | `gcs` 或 `gs` | `bucket name` | `credentials-file`：迁移工具节点上的凭证 JSON 文件的路径 </br> `storage-class`：上传对象的存储类别（例如 `STANDARD` 或 `COLDLINE`）</br> `predefined-acl`：上传对象的预定义 ACL（例如 `private` 或 `project-private`） |
| Azure | `azure` 或 `azblob` | `container name` | `account-name`：存储账户名 </br> `account-key`：访问密钥 </br> `access-tier`：上传对象的存储类别（例如 `Hot`、`Cool`、`Archive`）。如果没有设置 `access-tier` 的值（该值为空），此值会默认设置为 `Hot`。 |
| NFS/Local | `local` | "" | N/A |

### URL 示例

本部分示例以 `bucket name` 或 `container name` 为 `external` 为例进行介绍。

<SimpleTab>
<div label="Amazon S3">

**备份快照数据到 S3**

```shell
./br backup full  -u "${PD_IP}:2379" -s "s3://external/backup-20220915?access_key=${access_key}&secret_access_key=${secret_access_key}"
```

**从 S3 恢复快照备份数据**

```shell
./br restore full  -u "${PD_IP}:2379" -s "s3://external/backup-20220915?access_key=${access_key}&secret_access_key=${secret_access_key}"
```

</div>
<div label="GCS">

**使用 BR 将数据备份至 GCS**

```shell
./br backup full --pd "${PD_IP}:2379" --Storage 'gcs://external/backup-20220915?credentials-file=${credentials-file-path}'
```

**从 GCS 恢复快照备份据**

```shell
./br restore full --pd "${PD_IP}:2379" --Storage 'gcs://external/backup-20220915?credentials-file=${credentials-file-path}'
```

</div>
<div label="Azure blob storage">

**使用 BR 将数据备份至 Azure Blob Storage**

```shell
./br backup full -u "${PD_IP}:2379" -s "azure://external/backup-20220915?account-name=${account name}&account-key=${account key}"
```

**从 Azure Blob Storage 只恢复快照备份中 test db 的数据**

```shell
./br restore db --db test -u "${PD_IP}:2379" -s "azure://external/backup-20220915account-name=${account name}&account-key=${account key}"
```

</div>
</SimpleTab>

## 鉴权

将数据存储到 cloud 存储系统时，根据 cloud 供应商的不同，需要设置不同的鉴权参数。本部分介绍使用 Amazon S3、GCS 及 Azure storage 时所用存储服务的鉴权方式。

<SimpleTab>
<div label="Amazon S3">

### S3 目录访问权限

在备份之前，为 BR 访问 S3 中的备份目录设置相应的访问权限。

- 备份时 TiKV 和 BR 需要的访问备份数据目录的最小权限： `s3:ListBucket`、`s3:PutObject` 和 `s3:AbortMultipartUpload`。
- 恢复时 TiKV 和 BR 需要的访问备份数据目录的最小权限： `s3:ListBucket` 和 `s3:GetObject`。

如果你还没有创建备份数据保存目录，可以参照 [AWS 官方文档](https://docs.aws.amazon.com/zh_cn/AmazonS3/latest/user-guide/create-bucket.html)在指定的 `Region` 区域中创建一个 S3 桶 `Bucket`；如果有需要，还可以参照 [AWS 官方文档](https://docs.aws.amazon.com/zh_cn/AmazonS3/latest/user-guide/create-folder.html)在 Bucket 中创建一个文件夹 `Folder`。

### 配置访问 S3 的账户

**指定访问密钥**

如果指定访问密钥和 secret 访问密钥，将按照指定的访问密钥和 secret 访问密钥进行鉴权。除了在 URL 中指定密钥外，还支持以下的方式

1. BR 读取 `$AWS_ACCESS_KEY_ID` 和 `$AWS_SECRET_ACCESS_KEY` 环境变量
2. BR 读取 `$AWS_ACCESS_KEY` 和 `$AWS_SECRET_KEY` 环境变量
3. BR 读取共享凭证文件，路径为 `$AWS_SHARED_CREDENTIALS_FILE` 环境变量指定
4. BR 读取共享凭证文件，路径为 `~/.aws/credentials`

**基于 IAM Role 进行访问**

为运行 TiKV 和 BR 的 EC2 实例关联一个配置了访问 S3 访问权限的 IAM role，正确设置后，BR 可以直接访问对应的 S3 中的备份目录，而不需要额外的设置。

```shell
br backup full --pd "${PD_IP}:2379" --storage "s3://${host}/${path}"
```

</div>
<div label="GCS">

### 配置访问 GCS 的账户

**指定访问密钥**

如果指定了 `credentials-file` 参数，将按照指定的 `credentials-file` 进行鉴权。除了在 URL 中指定密钥文件外，还支持以下的方式

1. BR 读取位于 `$GOOGLE_APPLICATION_CREDENTIALS` 环境变量所指定路径的文件内容
2. BR 读取位于 `~/.config/gcloud/application_default_credentials.json` 的文件内容
3. 在 GCE 或 GAE 中运行时，从元数据服务器中获取的凭证

</div>
<div label="Azure storage">

### 配置访问 Azure Blob Storage 的账户

**指定访问密钥**

在 URL 配置 `account-name` 和 `account-key`，则使用该参数指定的密钥。 除了在 URL 中指定密钥文件外，还支持以下的方式

* BR 读取 `$AZURE_STORAGE_KEY`。

**使用 Azure AD 备份恢复**

在 BR 运行环境配置环境变量 `$AZURE_CLIENT_ID`、`$AZURE_TENANT_ID` 和 `$AZURE_CLIENT_SECRET`。

- 当使用 TiUP 启动的集群时，TiKV 会使用 systemd 服务。以下示例介绍如何为 TiKV 配置上述三个环境变量：

    > **注意：**
    >
    > 该流程在第 3 步中需要重启 TiKV。如果你的集群不适合重启，请使用**指定访问密钥的方式**进行备份恢复。

    1. 假设该节点上 TiKV 端口为 24000（即 systemd 服务名为 tikv-24000）：

        ```
        systemctl edit tikv-24000
        ```

    2. 填入环境变量信息：

        ```
        [Service]
        Environment="AZURE_CLIENT_ID=aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
        Environment="AZURE_TENANT_ID=aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
        Environment="AZURE_CLIENT_SECRET=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        ```

    3. 重新加载配置并重启 TiKV：

        ```
        systemctl daemon-reload
        systemctl restart tikv-24000
        ```

- 为命令行启动的 TiKV 和 BR 配置 Azure AD 的信息，只需要确定运行环境中存在 `$AZURE_CLIENT_ID`、`$AZURE_TENANT_ID` 和 `$AZURE_CLIENT_SECRET`。通过运行下列命令行，可以确认 BR 和 TiKV 运行环境中是否存在这三个环境变量：

    ```
    echo $AZURE_CLIENT_ID
    echo $AZURE_TENANT_ID
    echo $AZURE_CLIENT_SECRET
    ```

- 使用 BR 将数据备份至 Azure Blob Storage

    ```shell
    ./br backup full -u "${PD_IP}:2379" -s "azure://external/backup-20220915?account-name=${account name}"
    ```

</div>
</SimpleTab>

## 存储服务端加密

### Amazon S3 存储服务端加密备份数据

BR 支持对备份到 S3 的数据进行 S3 服务端加密 (SSE)。BR S3 服务端加密也支持使用用户自行创建的 AWS KMS 密钥进行加密，详细信息请参考 [BR S3 服务端加密](/encryption-at-rest.md#br-s3-服务端加密)。

## Cloud Storage 其他功能支持

* BR v6.3 版本支持 AWS S3 Object lock 功能。用户可以在 AWS 开启 [S3 Object Lock](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html) 功能来防止备份数据写入后被修改或者删除。
