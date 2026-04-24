---
title: 备份存储
summary: 了解 BR 支持的备份存储服务的 URI 格式、鉴权方案和使用方式。
aliases: ['/docs-cn/dev/br/backup-and-restore-storages/','/zh/tidb/dev/backup-storage-S3/','/zh/tidb/dev/backup-storage-azblob/','/zh/tidb/dev/backup-storage-gcs/','/zh/tidb/dev/external-storage/']
---

# 备份存储

TiDB 支持 Amazon S3、Google Cloud Storage (GCS)、Azure Blob Storage 和 NFS 作为备份恢复的存储。具体来说，可以在 `br` 的 `--storage` 或 `-s` 选项中指定备份存储的 URI。本文介绍不同外部存储服务中 [URI 的定义格式](#uri-格式)、存储过程中的[鉴权方案](#鉴权)以及[存储服务端加密](#存储服务端加密)。

## BR 向 TiKV 发送凭证

| 命令行参数 | 描述 | 默认值 |
|:----------|:-------|:-------|
| `--send-credentials-to-tikv` | 是否将 BR 获取到的权限凭证发送给 TiKV。 | `true` |

在默认情况下，使用 Amazon S3、Google Cloud Storage (GCS)、Azure Blob Storage 存储时，BR 会将凭证发送到每个 TiKV 节点，以减少设置的复杂性。该操作由参数 `--send-credentials-to-tikv`（或简写为 `-c`）控制。

但是，这个操作不适合云端环境，如果采用了 IAM Role 方式授权，那么每个节点都有自己的角色和权限。在这种情况下，你需要设置 `--send-credentials-to-tikv=false`（或简写为 `-c=0`）来禁止发送凭证：

```bash
tiup br backup full -c=0 -u pd-service:2379 --storage 's3://bucket-name/prefix'
```

使用 SQL 进行[备份](/sql-statements/sql-statement-backup.md)[恢复](/sql-statements/sql-statement-restore.md)时，可加上 `SEND_CREDENTIALS_TO_TIKV = FALSE` 选项：

```sql
BACKUP DATABASE * TO 's3://bucket-name/prefix' SEND_CREDENTIALS_TO_TIKV = FALSE;
```

## URI 格式

### 格式说明

外部存储服务的 URI 格式如下：

```shell
[scheme]://[host]/[path]?[parameters]
```

关于 URI 格式的详细信息，请参考[外部存储服务的 URI 格式](/external-storage-uri.md)。

### URI 示例

本部分示例以 `host`（上表中 `bucket name`、`container name`）为 `external` 为例进行介绍。

<SimpleTab groupId="storage">
<div label="Amazon S3" value="amazon">

**备份快照数据到 Amazon S3**

```shell
tiup br backup full -u "${PD_IP}:2379" \
--storage "s3://external/backup-20220915?access-key=${access-key}&secret-access-key=${secret-access-key}"
```

**从 Amazon S3 恢复快照备份数据**

```shell
tiup br restore full -u "${PD_IP}:2379" \
--storage "s3://external/backup-20220915?access-key=${access-key}&secret-access-key=${secret-access-key}"
```

</div>
<div label="GCS" value="gcs">

**备份快照数据到 GCS**

```shell
tiup br backup full --pd "${PD_IP}:2379" \
--storage "gcs://external/backup-20220915?credentials-file=${credentials-file-path}"
```

**从 GCS 恢复快照备份数据**

```shell
tiup br restore full --pd "${PD_IP}:2379" \
--storage "gcs://external/backup-20220915?credentials-file=${credentials-file-path}"
```

</div>
<div label="Azure Blob Storage" value="azure">

**备份快照数据到 Azure Blob Storage**

```shell
tiup br backup full -u "${PD_IP}:2379" \
--storage "azure://external/backup-20220915?account-name=${account-name}&account-key=${account-key}"
```

**从 Azure Blob Storage 恢复快照备份数据中 `test` 数据库**

```shell
tiup br restore db --db test -u "${PD_IP}:2379" \
--storage "azure://external/backup-20220915account-name=${account-name}&account-key=${account-key}"
```

</div>
</SimpleTab>

## 鉴权

将数据存储到云服务存储系统时，根据云服务供应商的不同，需要设置不同的鉴权参数。本部分介绍使用 Amazon S3、GCS 及 Azure Blob Storage 时所用存储服务的鉴权方式以及如何配置访问相应存储服务的账户。

<SimpleTab groupId="storage">
<div label="Amazon S3" value="amazon">

在备份之前，需要为 br 命令行工具访问 Amazon S3 中的备份目录设置相应的访问权限：

- 备份时 TiKV 和 br 命令行工具需要的访问备份数据目录的最小权限：`s3:ListBucket`、`s3:GetObject`、`s3:DeleteObject`、`s3:PutObject` 和 `s3:AbortMultipartUpload`。
- 恢复时 TiKV 和 br 命令行工具需要的访问备份数据目录的最小权限：`s3:ListBucket` 和 `s3:GetObject`。

如果你还没有创建备份数据保存目录，可以参考[创建存储桶](https://docs.aws.amazon.com/zh_cn/AmazonS3/latest/user-guide/create-bucket.html)在指定的区域中创建一个 S3 存储桶。如果需要使用文件夹，可以参考[使用文件夹在 Amazon S3 控制台中组织对象](https://docs.aws.amazon.com/zh_cn/AmazonS3/latest/user-guide/create-folder.html)在存储桶中创建一个文件夹。

> **注意：**
>
> AWS 在 2024 年改变了默认行为，新创建的实例默认设置仅支持 IMDSv2，详情请参考[将 IMDSv2 设为账户中所有新实例启动的默认设置](https://aws.amazon.com/cn/about-aws/whats-new/2024/03/set-imdsv2-default-new-instance-launches/)。因此从 v8.4.0 开始，BR 支持在仅开启 IMDSv2 的 Amazon EC2 实例上获取 IAM role 权限。在使用 v8.4.0 之前版本的 BR 时，需要设置实例为同时支持 IMDSv1 和 IMDSv2。

配置访问 Amazon S3 的账户可以通过以下两种方式：

- 方式一：指定访问密钥

    如果指定访问密钥和秘密访问密钥，将按照指定的访问密钥和秘密访问密钥进行鉴权。除了在 URI 中指定密钥外，还支持以下方式：

    - br 命令行工具读取 `$AWS_ACCESS_KEY_ID` 和 `$AWS_SECRET_ACCESS_KEY` 环境变量
    - br 命令行工具读取 `$AWS_ACCESS_KEY` 和 `$AWS_SECRET_KEY` 环境变量
    - br 命令行工具读取共享凭证文件，路径由 `$AWS_SHARED_CREDENTIALS_FILE` 环境变量指定
    - br 命令行工具读取共享凭证文件，路径为 `~/.aws/credentials`

- 方式二：基于 IAM Role 进行访问

    为运行 TiKV 和 br 命令行工具的 EC2 实例关联一个配置了访问 S3 访问权限的 IAM role。正确设置后，br 命令行工具可以直接访问对应的 S3 中的备份目录，而不需要额外的设置。

    ```shell
    tiup br backup full --pd "${PD_IP}:2379" \
    --storage "s3://${host}/${path}"
    ```

</div>
<div label="GCS" value="gcs">

配置访问 GCS 的账户可以通过指定访问密钥的方式。如果指定了 `credentials-file` 参数，将按照指定的 `credentials-file` 进行鉴权。除了在 URI 中指定密钥文件外，还支持以下方式：

- br 命令行工具读取位于 `$GOOGLE_APPLICATION_CREDENTIALS` 环境变量所指定路径的文件内容
- br 命令行工具读取位于 `~/.config/gcloud/application_default_credentials.json` 的文件内容
- 在 GCE 或 GAE 中运行时，从元数据服务器中获取的凭证

</div>
<div label="Azure Blob Storage" value="azure">

- 方式一：指定共享访问签名

    在 URI 中配置 `account-name` 和 `sas-token`，则使用该参数指定的存储账户名和共享访问签名令牌。由于共享访问签名令牌中带有 `&` 的字符，需要将其编码为 `%26` 后再添加到 URI 中。你也可以直接对整个 `sas-token` 进行一次百分号编码。<!-- TODO: add an example -->

- 方式二：指定访问密钥

    在 URI 中配置 `account-name` 和 `account-key`，则使用该参数指定的存储账户名和密钥。除了在 URI 中指定密钥文件外，还支持 br 命令行工具读取 `$AZURE_STORAGE_KEY` 的方式。

- 方式三：使用 Azure AD 备份恢复

    在 br 命令行工具运行环境配置环境变量 `$AZURE_CLIENT_ID`、`$AZURE_TENANT_ID` 和 `$AZURE_CLIENT_SECRET`。

    - 当集群使用 TiUP 启动时，TiKV 会使用 systemd 服务。以下示例介绍如何为 TiKV 配置上述三个环境变量：

        > **注意：**
        >
        > 该流程在第 3 步中需要重启 TiKV。如果你的集群不适合重启，请使用**指定访问密钥的方式**进行备份恢复。

        1. 假设该节点上 TiKV 端口为 `24000`，即 systemd 服务名为 `tikv-24000`：

            ```shell
            systemctl edit tikv-24000
            ```

        2. 编辑三个环境变量的信息：

            ```
            [Service]
            Environment="AZURE_CLIENT_ID=aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
            Environment="AZURE_TENANT_ID=aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
            Environment="AZURE_CLIENT_SECRET=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
            ```

        3. 重新加载配置并重启 TiKV：

            ```shell
            systemctl daemon-reload
            systemctl restart tikv-24000
            ```

    - 为命令行启动的 TiKV 和 br 命令行工具配置 Azure AD 的信息，只需要确定运行环境中存在 `$AZURE_CLIENT_ID`、`$AZURE_TENANT_ID` 和 `$AZURE_CLIENT_SECRET`。通过运行下列命令行，可以确认 br 命令行工具和 TiKV 运行环境中是否存在这三个环境变量：

        ```shell
        echo $AZURE_CLIENT_ID
        echo $AZURE_TENANT_ID
        echo $AZURE_CLIENT_SECRET
        ```

    - 使用 br 命令行工具将数据备份至 Azure Blob Storage：

        ```shell
        tiup br backup full -u "${PD_IP}:2379" \
        --storage "azure://external/backup-20220915?account-name=${account-name}"
        ```

- 方式四：使用 Azure 托管标识 (Managed Identity)

    从 v8.5.5 和 v9.0.0 起，如果你的 TiDB 集群和 br 命令行工具运行在 Azure 虚拟机 (VM) 或 Azure Kubernetes Service (AKS) 环境中，并且已为节点分配了 Azure 托管标识，则可以使用 Azure 托管标识进行鉴权。

    使用此方式前，请确保已在 [Azure Portal](https://azure.microsoft.com/) 中为对应的托管标识授予目标存储账户的访问权限（如 `Storage Blob Data Contributor`）。

    - **系统分配的托管标识 (System-assigned)**：

        使用系统分配的托管标识时，无需配置任何 Azure 相关环境变量，直接运行 br 备份命令即可。

        ```shell
        tiup br backup full -u "${PD_IP}:2379" \
        --storage "azure://external/backup-20220915?account-name=${account-name}"
        ```

        > **注意：**
        >
        > 请确保运行环境中**不存在** `AZURE_CLIENT_ID`、`AZURE_TENANT_ID` 或 `AZURE_CLIENT_SECRET` 环境变量，否则 Azure SDK 可能会优先使用其他认证方式，导致托管标识未生效。

    - **用户分配的托管标识 (User-assigned)**：

        使用用户分配的托管标识时，需要在 TiKV 运行环境和 br 命令行工具运行环境中配置环境变量 `AZURE_CLIENT_ID` （其值为该托管标识的 Client ID），然后再执行 br 备份命令。具体步骤如下：

        1. 使用 TiUP 启动时为 TiKV 配置 Client ID：

            以下步骤以 TiKV 端口 `24000`、systemd 服务名 `tikv-24000` 为例：

            1. 执行以下命令进入服务配置编辑界面：

                ```shell
                systemctl edit tikv-24000
                ```

            2. 配置 `AZURE_CLIENT_ID` 环境变量：

                ```ini
                [Service]
                Environment="AZURE_CLIENT_ID=<your-client-id>"
                ```

            3. 重新加载 systemd 配置并重启 TiKV：

                ```shell
                systemctl daemon-reload
                systemctl restart tikv-24000
                ```

        2. 为 br 命令行工具配置 `AZURE_CLIENT_ID` 环境变量：

            ```shell
            export AZURE_CLIENT_ID="<your-client-id>"
            ```

        3. 使用 br 命令行工具将数据备份至 Azure Blob Storage：

            ```shell
            tiup br backup full -u "${PD_IP}:2379" \
            --storage "azure://external/backup-20220915?account-name=${account-name}"
            ```

</div>
</SimpleTab>

## 存储服务端加密

### Amazon S3 存储服务端加密备份数据

TiDB 备份恢复功能支持对备份到 Amazon S3 的数据进行 S3 服务端加密 (SSE)。S3 服务端加密也支持使用用户自行创建的 AWS KMS 密钥，详细信息请参考 [BR S3 服务端加密](/encryption-at-rest.md#br-s3-服务端加密)。

### Azure Blob Storage 存储服务端加密备份数据

TiDB 备份恢复功能支持对备份到 Azure Blob Storage 的数据设置 Azure 服务端加密范围 (Encryption Scope) 或提供加密密钥 (Encryption Key)，为同一存储账户的不同备份数据建立安全边界。详细信息请参考 [BR Azure Blob Storage 服务端加密](/encryption-at-rest.md#br-azure-blob-storage-服务端加密)。

## 存储服务其他功能支持

Amazon [S3 对象锁定](https://docs.aws.amazon.com/zh_cn/AmazonS3/latest/userguide/object-lock.html)功能支持用户通过设置数据留存期，有效防止备份数据在指定时间内被意外或故意删除，提升了数据的安全性和完整性。从 v6.3.0 起，BR 为快照备份引入了对 Amazon S3 对象锁定功能的支持，为全量备份增加了额外的安全性保障。从 v8.0.0 起，PITR 也引入了对 Amazon S3 对象锁定功能的支持，无论是全量备份还是日志数据备份，都可以通过对象锁定功能提供更可靠的数据保护，进一步加强了数据备份和恢复的安全性，并满足了监管方面的需求。

BR 和 PITR 将自动检测 Amazon S3 对象锁定功能的开启或关闭状态，你无需进行任何额外的操作。

> **警告：**
>
> 如果在快照备份执行过程中或者 PITR 日志备份过程中，才开启了对象锁定功能，快照备份或者日志备份可能会失败。需要重新启动快照备份或者 PITR 日志备份任务来继续完成备份。
