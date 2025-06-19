---
title: 外部存储服务的 URI 格式
summary: 了解外部存储服务的存储 URI 格式，包括 Amazon S3、GCS 和 Azure Blob Storage。
---

## 外部存储服务的 URI 格式

本文描述外部存储服务的 URI 格式，包括 Amazon S3、GCS 和 Azure Blob Storage。

URI 的基本格式如下：

```shell
[scheme]://[host]/[path]?[parameters]
```

## Amazon S3 URI 格式

<CustomContent platform="tidb">

- `scheme`：`s3`
- `host`：`bucket name`（存储桶名称）
- `parameters`：

    - `access-key`：指定访问密钥。
    - `secret-access-key`：指定秘密访问密钥。
    - `session-token`：指定临时会话令牌。BR 从 v7.6.0 版本开始支持此参数。
    - `use-accelerate-endpoint`：指定是否在 Amazon S3 上使用加速端点（默认为 `false`）。
    - `endpoint`：指定 S3 兼容服务的自定义端点 URL（例如，`<https://s3.example.com/>`）。
    - `force-path-style`：使用路径样式访问而不是虚拟托管样式访问（默认为 `true`）。
    - `storage-class`：指定上传对象的存储类（例如，`STANDARD` 或 `STANDARD_IA`）。
    - `sse`：指定用于加密上传对象的服务器端加密算法（可选值：空、`AES256` 或 `aws:kms`）。
    - `sse-kms-key-id`：如果 `sse` 设置为 `aws:kms`，则指定 KMS ID。
    - `acl`：指定上传对象的预设 ACL（例如，`private` 或 `authenticated-read`）。
    - `role-arn`：当你需要使用指定的 [IAM 角色](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html)从第三方访问 Amazon S3 数据时，可以使用 `role-arn` URL 查询参数指定 IAM 角色的 [Amazon 资源名称 (ARN)](https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html)，例如 `arn:aws:iam::888888888888:role/my-role`。有关使用 IAM 角色从第三方访问 Amazon S3 数据的更多信息，请参见 [AWS 文档](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_common-scenarios_third-party.html)。BR 从 v7.6.0 版本开始支持此参数。
    - `external-id`：当你从第三方访问 Amazon S3 数据时，可能需要指定正确的[外部 ID](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-user_externalid.html) 来承担 [IAM 角色](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html)。在这种情况下，你可以使用 `external-id` URL 查询参数指定外部 ID，以确保你可以承担该 IAM 角色。外部 ID 是由第三方与 IAM 角色 ARN 一起提供的任意字符串，用于访问 Amazon S3 数据。在承担 IAM 角色时提供外部 ID 是可选的，这意味着如果第三方不要求 IAM 角色提供外部 ID，你可以在不提供此参数的情况下承担 IAM 角色并访问相应的 Amazon S3 数据。

以下是 TiDB Lightning 和 BR 的 Amazon S3 URI 示例。在此示例中，你需要指定特定的文件路径 `testfolder`。

```shell
s3://external/testfolder?access-key=${access-key}&secret-access-key=${secret-access-key}
```

以下是 TiCDC `sink-uri` 的 Amazon S3 URI 示例。

```shell
tiup cdc:v7.5.0 cli changefeed create \
    --server=http://172.16.201.18:8300 \
    --sink-uri="s3://cdc?endpoint=http://10.240.0.38:9000&access-key=${access-key}&secret-access-key=${secret-access-key}" \
    --changefeed-id="cdcTest" \
    --config=cdc_csv.toml
```

</CustomContent>

<CustomContent platform="tidb-cloud">

- `scheme`：`s3`
- `host`：`bucket name`（存储桶名称）
- `parameters`：

    - `access-key`：指定访问密钥。
    - `secret-access-key`：指定秘密访问密钥。
    - `session-token`：指定临时会话令牌。
    - `use-accelerate-endpoint`：指定是否在 Amazon S3 上使用加速端点（默认为 `false`）。
    - `endpoint`：指定 S3 兼容服务的自定义端点 URL（例如，`<https://s3.example.com/>`）。
    - `force-path-style`：使用路径样式访问而不是虚拟托管样式访问（默认为 `true`）。
    - `storage-class`：指定上传对象的存储类（例如，`STANDARD` 或 `STANDARD_IA`）。
    - `sse`：指定用于加密上传对象的服务器端加密算法（可选值：空、`AES256` 或 `aws:kms`）。
    - `sse-kms-key-id`：如果 `sse` 设置为 `aws:kms`，则指定 KMS ID。
    - `acl`：指定上传对象的预设 ACL（例如，`private` 或 `authenticated-read`）。
    - `role-arn`：要允许 TiDB Cloud 使用特定的 [IAM 角色](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html)访问 Amazon S3 数据，请在 `role-arn` URL 查询参数中提供该角色的 [Amazon 资源名称 (ARN)](https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html)。例如：`arn:aws:iam::888888888888:role/my-role`。

        > **注意：**
        >
        > - 要自动创建 IAM 角色，请在 [TiDB Cloud 控制台](https://tidbcloud.com/)中导航到集群的**从 Amazon S3 导入数据**页面，填写**文件夹 URI**字段，在**角色 ARN**字段下点击**点击此处使用 AWS CloudFormation 创建新角色**，然后按照**添加新角色 ARN**对话框中的屏幕说明操作。
        > - 如果你在使用 AWS CloudFormation 创建 IAM 角色时遇到任何问题，请在**添加新角色 ARN**对话框中点击**遇到问题？手动创建角色 ARN**以获取 TiDB Cloud 账户 ID 和 TiDB Cloud 外部 ID，然后按照[使用角色 ARN 配置 Amazon S3 访问](https://docs.pingcap.com/tidbcloud/dedicated-external-storage#configure-amazon-s3-access-using-a-role-arn)中的步骤手动创建角色。在配置 IAM 角色时，确保在**账户 ID**字段中输入 TiDB Cloud 账户 ID，并选择**需要外部 ID**以防止[混淆代理攻击](https://docs.aws.amazon.com/IAM/latest/UserGuide/confused-deputy.html)。
        > - 为了增强安全性，你可以通过配置较短的**最大会话持续时间**来减少 IAM 角色的有效期。更多信息，请参见 AWS 文档中的[更新角色的最大会话持续时间](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_update-role-settings.html#id_roles_update-session-duration)。

    - `external-id`：指定 TiDB Cloud 外部 ID，这是 TiDB Cloud 访问 Amazon S3 数据所必需的。你可以从 [TiDB Cloud 控制台](https://tidbcloud.com/)的**添加新角色 ARN**对话框中获取此 ID。更多信息，请参见[使用角色 ARN 配置 Amazon S3 访问](https://docs.pingcap.com/tidbcloud/dedicated-external-storage#configure-amazon-s3-access-using-a-role-arn)。

以下是 [`BACKUP`](/sql-statements/sql-statement-backup.md) 和 [`RESTORE`](/sql-statements/sql-statement-restore.md) 的 Amazon S3 URI 示例。此示例使用文件路径 `testfolder`。

```shell
s3://external/testfolder?access-key=${access-key}&secret-access-key=${secret-access-key}
```

</CustomContent>

## GCS URI 格式

- `scheme`：`gcs` 或 `gs`
- `host`：`bucket name`（存储桶名称）
- `parameters`：

    - `credentials-file`：指定迁移工具节点上的凭证 JSON 文件路径。
    - `storage-class`：指定上传对象的存储类（例如，`STANDARD` 或 `COLDLINE`）。
    - `predefined-acl`：指定上传对象的预设 ACL（例如，`private` 或 `project-private`）。

<CustomContent platform="tidb">

以下是 TiDB Lightning 和 BR 的 GCS URI 示例。在此示例中，你需要指定特定的文件路径 `testfolder`。

```shell
gcs://external/testfolder?credentials-file=${credentials-file-path}
```

</CustomContent>

以下是 [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md) 的 GCS URI 示例。在此示例中，你需要指定特定的文件名 `test.csv`。

```shell
gcs://external/test.csv?credentials-file=${credentials-file-path}
```

## Azure Blob Storage URI 格式

- `scheme`：`azure` 或 `azblob`
- `host`：`container name`（容器名称）
- `parameters`：

    - `account-name`：指定存储的账户名称。
    - `account-key`：指定访问密钥。
    - `sas-token`：指定共享访问签名（SAS）令牌。
    - `access-tier`：指定上传对象的访问层级，例如 `Hot`、`Cool` 或 `Archive`。默认值是存储账户的默认访问层级。
    - `encryption-scope`：指定用于服务器端加密的[加密范围](https://learn.microsoft.com/en-us/azure/storage/blobs/encryption-scope-manage?tabs=powershell#upload-a-blob-with-an-encryption-scope)。
    - `encryption-key`：指定用于服务器端加密的[加密密钥](https://learn.microsoft.com/en-us/azure/storage/blobs/encryption-customer-provided-keys)，使用 AES256 加密算法。

以下是 BR 的 Azure Blob Storage URI 示例。在此示例中，你需要指定特定的文件路径 `testfolder`。

```shell
azure://external/testfolder?account-name=${account-name}&account-key=${account-key}
```
